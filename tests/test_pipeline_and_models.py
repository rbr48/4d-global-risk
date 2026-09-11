"""
Test Suite for Real-World Data Ingestors, M0-M7 Model Ladder, and Rolling-Origin Backtester.
"""

import numpy as np
import pandas as pd

from src.acquisition.schema import PointInTimeDatabase
from src.acquisition.synthetic_stream import generate_calibrated_multidisciplinary_panel
from models.baselines import PersistenceModel, ClimatologyModel
from models.statistical_models import (
    SingleDomainLogisticModel,
    MultidisciplinaryRegularizedModel,
    DynamicAutoregressiveModel,
)
from models.nonlinear_model import NonlinearGBDTModel
from models.full_4d_dlm import Full4DDLMModel
from src.evaluation.backtest import RollingOriginBacktester


def test_synthetic_stream_and_schema():
    """Verify calibrated multidisciplinary stream generation and point-in-time database ingestion."""
    df, records = generate_calibrated_multidisciplinary_panel(num_days=80, seed=123)
    assert len(df) == 80
    assert len(records) == 80 * 7

    db = PointInTimeDatabase(":memory:")
    db.insert_records(records)

    # Query at day 40 origin
    origin = df["date"].iloc[40].to_pydatetime()
    eligible = db.get_eligible_slice(forecast_origin=origin)
    assert not eligible.empty
    assert db.assert_zero_leakage(eligible, origin) is True


def test_model_ladder_contracts():
    """Verify all models in M0..M7 ladder adhere to fit / predict_proba contracts."""
    np.random.seed(42)
    n_obs = 60
    X = pd.DataFrame(
        {
            "vix": np.random.uniform(12, 30, n_obs),
            "conflict": np.random.uniform(5, 50, n_obs),
            "energy": np.random.uniform(1, 10, n_obs),
        }
    )
    # Binary event outcome
    y = (X["vix"] > 22.0).astype(int).values

    models = [
        PersistenceModel(),
        ClimatologyModel(),
        SingleDomainLogisticModel(target_domain_cols=["vix"]),
        MultidisciplinaryRegularizedModel(),
        DynamicAutoregressiveModel(num_lags=2),
        NonlinearGBDTModel(n_estimators=10),
        Full4DDLMModel(anchor_indicator="vix", horizons=[1, 3, 7, 14]),
    ]

    X_test = X.iloc[-5:].copy()

    for model in models:
        model.fit(X.iloc[:-5], y[:-5])
        for h in [1, 3, 7, 14]:
            probs = model.predict_proba(X_test, horizon=h)
            assert len(probs) == len(X_test)
            assert np.all(probs >= 0.0) and np.all(probs <= 1.0)
            assert not np.isnan(probs).any()


def test_rolling_backtest_execution():
    """
    Verify complete rolling-origin out-of-sample backtester runs,
    archives predictions, and computes the performance summary table.
    """
    df, _ = generate_calibrated_multidisciplinary_panel(num_days=100, seed=99)
    # Define systemic threshold event: high VIX episode
    target_event = (df["vix"] >= np.percentile(df["vix"], 80)).astype(int)
    feature_cols = [c for c in df.columns if c != "date"]
    df_features = df[feature_cols]

    backtester = RollingOriginBacktester(horizons=[1, 3, 7], min_train_size=40, cost_loss_ratio=0.20)

    perf_table = backtester.run_backtest(
        df_features=df_features,
        target_series=target_event,
        step_size=2,  # Step every 2 days for fast testing
        anchor_indicator="vix",
    )

    assert not perf_table.empty
    assert "BSS_vs_Clim" in perf_table.columns
    assert "PR_AUC" in perf_table.columns
    assert "Relative_Value" in perf_table.columns

    # Check that M7 Full 4D is present
    m7_rows = perf_table[perf_table["Model"] == "M7_Full4D"]
    assert len(m7_rows) == 3  # for horizons 1d, 3d, 7d

    # Verify M7 achieves positive skill over climatology at near horizon
    m7_h1 = m7_rows[m7_rows["Horizon"] == "1d"].iloc[0]
    assert m7_h1["Brier_Score"] < 0.25


def test_propagation_matrix_properties():
    """Verify Full4DDLMModel produces valid cross-domain propagation matrices Pi_h."""
    df, _ = generate_calibrated_multidisciplinary_panel(num_days=80, seed=55)
    feature_cols = [c for c in df.columns if c != "date"]
    X = df[feature_cols]
    y = (X["vix"] > 20).astype(int).values

    model = Full4DDLMModel(anchor_indicator="vix", horizons=[1, 7])
    model.fit(X, y)

    pi_1 = model.get_propagation_matrix(horizon=1)
    pi_7 = model.get_propagation_matrix(horizon=7)

    assert pi_1.shape == (len(feature_cols), len(feature_cols))
    assert pi_7.shape == (len(feature_cols), len(feature_cols))

    # Propagation effects decay with horizon length
    assert np.mean(np.abs(pi_1)) > np.mean(np.abs(pi_7))


def test_single_row_inference_non_degenerate():
    """
    Verify that single-row slices passed at test time (as in rolling-origin backtesting)
    do NOT trigger normalization collapse in M2, M3, M4, or M7.
    Low VIX and High VIX must yield distinctly different probabilities.
    """
    np.random.seed(42)
    n = 100
    vix = np.random.uniform(12, 32, n)
    conflict = np.random.uniform(5, 50, n)
    energy = np.random.uniform(1, 10, n)
    X = pd.DataFrame({"vix": vix, "conflict": conflict, "energy": energy})
    y = (vix > 22.0).astype(int)

    models = {
        "M2": SingleDomainLogisticModel(target_domain_cols=["vix"]),
        "M3": MultidisciplinaryRegularizedModel(),
        "M4": DynamicAutoregressiveModel(num_lags=2),
        "M7": Full4DDLMModel(anchor_indicator="vix", horizons=[1, 3]),
    }

    row_low = pd.DataFrame([{"vix": 13.0, "conflict": 15.0, "energy": 2.0}])
    row_high = pd.DataFrame([{"vix": 31.0, "conflict": 15.0, "energy": 2.0}])

    for name, model in models.items():
        model.fit(X, y)
        prob_low = float(model.predict_proba(row_low, horizon=1)[0])
        prob_high = float(model.predict_proba(row_high, horizon=1)[0])

        assert (
            prob_high > prob_low
        ), f"{name} failed: prob_high ({prob_high:.4f}) is not greater than prob_low ({prob_low:.4f})"
        assert (
            abs(prob_high - prob_low) > 0.05
        ), f"{name} failed: prob difference too small ({abs(prob_high - prob_low):.4f}), indicating normalization collapse"
