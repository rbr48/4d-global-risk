"""
Automated Test Suite for 4D-MGRFF Core Modules
Verifies factor sign stability, zero-leakage enforcement, scoring consistency, and speed.
"""

from datetime import datetime, timedelta
import time
import numpy as np
import pandas as pd
import pytest

from src.acquisition.schema import PointInTimeDatabase, PointInTimeRecord
from src.features.features import (
    compute_salience_normalized_velocity,
    compute_rolling_volatility,
    OriginSafeStandardizer
)
from src.statespace.dgrs import SignIdentifiedDGRS
from src.evaluation.scoring import (
    compute_brier_score,
    compute_brier_skill_score,
    compute_expected_calibration_error,
    compute_pr_auc,
    compute_relative_value_score
)


def test_zero_leakage_enforcement():
    """Verify DuckDB point-in-time schema enforces I_t = {x: availability <= t}."""
    db = PointInTimeDatabase(":memory:")
    t_origin = datetime(2026, 6, 1, 12, 0, 0)
    
    records = [
        PointInTimeRecord(
            observation_id="obs_valid_1",
            event_time=datetime(2026, 5, 30),
            publication_time=datetime(2026, 5, 31),
            first_available_timestamp=datetime(2026, 5, 31),
            source="FRED",
            source_version="v1",
            domain="Economics",
            indicator="T10Y2Y",
            raw_value=-0.45
        ),
        PointInTimeRecord(
            observation_id="obs_leaked_2",
            event_time=datetime(2026, 5, 30),
            publication_time=datetime(2026, 6, 2),  # Published after origin
            first_available_timestamp=datetime(2026, 6, 2),
            source="IMF_WEO",
            source_version="Apr2026",
            domain="Economics",
            indicator="GDP_Growth",
            raw_value=2.1
        )
    ]
    db.insert_records(records)
    
    # Query data at origin
    eligible_df = db.get_eligible_slice(forecast_origin=t_origin)
    assert len(eligible_df) == 1
    assert eligible_df.iloc[0]["observation_id"] == "obs_valid_1"
    
    # Assert zero leakage passes
    assert db.assert_zero_leakage(eligible_df, t_origin) is True
    
    # If someone manually forces a leaked record, assertion must raise ValueError
    leaked_slice = pd.DataFrame([{
        "observation_id": "bad",
        "first_available_timestamp": datetime(2026, 6, 5)
    }])
    with pytest.raises(ValueError, match="POINT-IN-TIME LEAKAGE DETECTED"):
        db.assert_zero_leakage(leaked_slice, t_origin)


def test_factor_sign_stability():
    """
    Verify that SignIdentifiedDGRS strictly anchors the factor sign to the anchor indicator,
    preventing sign-flipping across rolling-origin iterations.
    """
    np.random.seed(42)
    T_steps = 150
    # Simulate a true positive systemic stress factor
    true_stress = np.sin(np.linspace(0, 10, T_steps)) + np.random.normal(0, 0.2, T_steps)
    
    # Create indicators: VIX positively correlated with stress
    vix = 15.0 + 5.0 * true_stress + np.random.normal(0, 0.5, T_steps)
    acled = np.maximum(0, 20.0 + 8.0 * true_stress + np.random.normal(0, 1.0, T_steps))
    equity = 100.0 - 10.0 * true_stress + np.random.normal(0, 1.0, T_steps)  # negatively correlated
    
    df = pd.DataFrame({"vix": vix, "acled_events": acled, "equity_index": equity})
    
    # Run across 5 different rolling origin cuts
    cutoffs = [70, 90, 110, 130, 150]
    estimated_correlations = []
    
    for cut in cutoffs:
        sub_df = df.iloc[:cut].copy()
        model = SignIdentifiedDGRS(anchor_indicator="vix", rho=0.85)
        model.fit(sub_df)
        
        # Check loading on vix is strictly positive
        anchor_loading = model.lambda_loadings[model.anchor_idx, 0]
        assert anchor_loading > 0.0, f"Anchor loading was non-positive: {anchor_loading}"
        
        f_smooth, _, _ = model.smooth(sub_df)
        
        # Correlation between estimated factor and anchor indicator must remain strongly positive
        corr = np.corrcoef(f_smooth, sub_df["vix"])[0, 1]
        estimated_correlations.append(corr)
        assert corr > 0.7, f"Sign flipped! Correlation was negative or weak: {corr}"
        
    # Verify all correlations remain positive and consistent
    assert all(c > 0.7 for c in estimated_correlations)


def test_scoring_engine_consistency():
    """Verify Brier Skill Score and Value Score properties."""
    np.random.seed(123)
    y_true = np.array([0, 0, 0, 0, 0, 0, 0, 0, 1, 1])  # 20% base rate
    
    # 1. Climatology forecast: p = 0.2 everywhere
    p_clim = np.full_like(y_true, 0.2, dtype=float)
    bss_clim = compute_brier_skill_score(p_clim, y_true)
    assert abs(bss_clim - 0.0) < 1e-6, f"Climatology BSS should be 0.0, got {bss_clim}"
    
    # 2. Perfect forecast: p = y_true
    bss_perfect = compute_brier_skill_score(y_true, y_true)
    assert abs(bss_perfect - 1.0) < 1e-6, f"Perfect BSS should be 1.0, got {bss_perfect}"
    
    # 3. Informative forecast: superior to climatology
    p_informative = np.array([0.05, 0.1, 0.05, 0.1, 0.15, 0.05, 0.1, 0.2, 0.8, 0.9])
    bss_info = compute_brier_skill_score(p_informative, y_true)
    assert bss_info > 0.0, f"Informative model must have positive BSS, got {bss_info}"
    
    # 4. Calibration ECE
    ece, _ = compute_expected_calibration_error(p_informative, y_true, num_bins=5)
    assert 0.0 <= ece <= 1.0
    
    # 5. Relative Value Score
    # For cost-loss ratio alpha = 0.2 matching base rate
    v_score = compute_relative_value_score(p_informative, y_true, cost_loss_ratio=0.2)
    assert v_score > 0.0, f"Informative forecast should yield positive economic value, got {v_score}"


def test_feature_engineering_safety():
    """Verify salience normalized velocity and origin-safe standardizer."""
    np.random.seed(99)
    T = 40
    events = pd.Series(np.random.poisson(lam=10, size=T))
    total_arts = pd.Series(np.random.normal(loc=1000, scale=50, size=T))
    
    # Induce artificial media surge in both events and total volume (e.g. general news crawler expansion)
    events.iloc[20:25] = events.iloc[20:25] * 5
    total_arts.iloc[20:25] = total_arts.iloc[20:25] * 5
    
    norm_vel = compute_salience_normalized_velocity(events, total_arts, window_length=7)
    assert len(norm_vel) == T
    assert not norm_vel.isna().any()
    
    # OriginSafeStandardizer test
    df_train = pd.DataFrame({"a": [10.0, 20.0, 30.0], "b": [100.0, 200.0, 300.0]})
    df_test = pd.DataFrame({"a": [40.0], "b": [400.0]})
    
    scaler = OriginSafeStandardizer()
    scaler.fit(df_train)
    
    df_test_trans = scaler.transform(df_test)
    # Mean of 'a' in train is 20, std is 10 -> 40 transformed should be (40-20)/10 = 2.0
    assert abs(df_test_trans.iloc[0]["a"] - 2.0) < 1e-4


def test_kalman_smoother_benchmark():
    """Verify analytical Kalman smoother runs in < 50ms per origin."""
    np.random.seed(77)
    df = pd.DataFrame(np.random.normal(0, 1, (300, 8)), columns=[f"ind_{i}" for i in range(8)])
    df["vix"] = df["ind_0"] * 2.0 + np.random.normal(0, 0.5, 300)
    
    model = SignIdentifiedDGRS(anchor_indicator="vix")
    model.fit(df)
    
    t0 = time.perf_counter()
    f_mean, f_std, ci_df = model.smooth(df)
    elapsed_ms = (time.perf_counter() - t0) * 1000.0
    
    assert len(f_mean) == 300
    assert elapsed_ms < 50.0, f"Kalman smoother took too long: {elapsed_ms:.2f} ms (expected < 50 ms)"
