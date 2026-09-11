"""
4D-MGRFF Real Data Empirical Backtester
Pulls real-world daily point-in-time time-series from data/processed/global_risk_database.db,
aligns them across business days, and executes the M0-M7 rolling backtester.
"""

from datetime import datetime
import os
import sqlite3
import numpy as np
import pandas as pd

from src.evaluation.backtest import RollingOriginBacktester
from models.full_4d_dlm import Full4DDLMModel
from src.evaluation.plotting import (
    plot_dgrs_trajectory,
    plot_propagation_heatmaps,
    plot_model_comparison_bars
)
from src.statespace.dgrs import SignIdentifiedDGRS


def run_real_fred_backtest(db_path: str = "data/processed/global_risk_database.db"):
    print("=" * 75)
    print(" 4D-MGRFF: EXECUTING BACKTEST ON REAL-WORLD FRED MACRO & FINANCIAL DATA ")
    print("=" * 75)
    
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Database {db_path} not found. Run fetch_live_fred_data.py first.")
        
    conn = sqlite3.connect(db_path)
    
    # Query all records
    query = """
        SELECT event_time, indicator, raw_value
        FROM global_risk_provenance
        WHERE indicator IN ('T10Y2Y', 'T5YIFR', 'BAMLH0A0HYM2', 'VIXCLS', 'DCOILBRENTEU', 'DTWEXBGS')
        ORDER BY event_time ASC
    """
    df_raw = pd.read_sql_query(query, conn)
    df_raw["event_time"] = pd.to_datetime(df_raw["event_time"])
    
    # Pivot into wide daily panel: index = date, columns = indicators
    df_pivot = df_raw.pivot_table(index="event_time", columns="indicator", values="raw_value", aggfunc="last")
    
    # Resample to daily business days and forward fill market closures (max 3 days)
    df_aligned = df_pivot.dropna().sort_index()
    print(f"\n[Phase 1] Aligned Real Data Panel:")
    print(f"  - Sample Range: {df_aligned.index.min().strftime('%Y-%m-%d')} to {df_aligned.index.max().strftime('%Y-%m-%d')}")
    print(f"  - Total Observations: {len(df_aligned)} daily business trading days")
    print(f"  - Indicators: {list(df_aligned.columns)}")
    
    # Define primary systemic risk episode: 85th percentile of VIXCLS
    q85_vix = np.percentile(df_aligned["VIXCLS"], 85)
    target_event = (df_aligned["VIXCLS"] >= q85_vix).astype(int)
    print(f"  - Primary Systemic Stress Event (VIX >= {q85_vix:.2f}): Base Rate = {np.mean(target_event):.2%}")
    
    # 2. Run Rolling-Origin Out-of-Sample Evaluation
    print("\n[Phase 2] Executing Rolling-Origin Out-of-Sample Backtest on Real Data...")
    backtester = RollingOriginBacktester(
        horizons=[1, 3, 7, 14],
        min_train_size=100,
        cost_loss_ratio=0.20
    )
    
    perf_table = backtester.run_backtest(
        df_features=df_aligned,
        target_series=target_event,
        step_size=3,
        anchor_indicator="VIXCLS"
    )
    
    # 3. Export Table 5 (Real Data Forecast Performance)
    os.makedirs("results/tables", exist_ok=True)
    perf_table.to_csv("results/tables/table_5_real_fred_performance.csv", index=False)
    perf_table.to_markdown("results/tables/table_5_real_fred_performance.md", index=False)
    
    print("\n" + "=" * 75)
    print(" TABLE 5 (REAL FRED DATA): OUT-OF-SAMPLE FORECAST PERFORMANCE ")
    print("=" * 75)
    print(perf_table.to_string(index=False))
    
    # 4. Compute Real Propagation Matrix Pi_h
    print("\n[Phase 3] Estimating Real Cross-Domain Propagation Matrices (Pi_h)...")
    m7 = Full4DDLMModel(anchor_indicator="VIXCLS", horizons=[1, 7])
    m7.fit(df_aligned, target_event.values)
    
    pi_1 = m7.get_propagation_matrix(horizon=1)
    pi_7 = m7.get_propagation_matrix(horizon=7)
    
    cols = list(df_aligned.columns)
    df_pi_1 = pd.DataFrame(np.round(pi_1, 3), index=cols, columns=cols)
    df_pi_7 = pd.DataFrame(np.round(pi_7, 3), index=cols, columns=cols)
    
    df_pi_1.to_csv("results/tables/table_8_real_fred_propagation_h1.csv")
    df_pi_7.to_csv("results/tables/table_8_real_fred_propagation_h7.csv")
    
    print("\n" + "=" * 75)
    print(" TABLE 8 (REAL FRED DATA): CROSS-DOMAIN PROPAGATION MATRIX (Pi_1: 1-Day) ")
    print("=" * 75)
    print(df_pi_1.to_string())
    
    # 5. Export Real Figures
    print("\n[Phase 4] Generating Publication Figures on Real Data...")
    dgrs = SignIdentifiedDGRS(anchor_indicator="VIXCLS")
    dgrs.fit(df_aligned)
    _, _, ci_df = dgrs.smooth(df_aligned)
    
    plot_dgrs_trajectory(ci_df, output_path="results/figures/figure_4_real_dgrs_trajectory.png")
    plot_propagation_heatmaps(df_pi_1, df_pi_7, output_path="results/figures/figure_7_real_propagation_heatmaps.png")
    plot_model_comparison_bars(perf_table, output_path="results/figures/figure_11_real_model_comparison.png")
    
    print("\n[Phase 5] Real Data Empirical Backtest Successfully Completed!")
    return perf_table


if __name__ == "__main__":
    run_real_fred_backtest()
