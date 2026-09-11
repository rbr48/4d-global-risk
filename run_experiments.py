"""
4D-MGRFF Master Experiment Runner
Executes the full rolling-origin backtest across M0-M7 and generates:
  - Table 5 (Forecast Performance Across Models & Horizons)
  - Table 8 (Cross-Domain Dynamic Propagation Matrix Pi_h)
  - Figure 4 (Dynamic Global Risk State Trajectory with 90% Credible Intervals)
  - Figure 7 (Cross-Domain Propagation Heatmaps)
  - Figure 11 (Out-of-Sample Model Comparison Bar Charts)
"""

from datetime import datetime
import os
import numpy as np
import pandas as pd

from src.acquisition.synthetic_stream import generate_calibrated_multidisciplinary_panel
from src.evaluation.backtest import RollingOriginBacktester
from src.statespace.dgrs import SignIdentifiedDGRS
from models.full_4d_dlm import Full4DDLMModel
from src.evaluation.plotting import (
    plot_dgrs_trajectory,
    plot_propagation_heatmaps,
    plot_model_comparison_bars
)


def run_full_dissertation_experiment():
    print("=" * 75)
    print(" 4D-MGRFF: EXECUTING FULL OUT-OF-SAMPLE ROLLING BACKTEST PIPELINE ")
    print("=" * 75)
    
    # 1. Generate / Load Multidisciplinary Global Risk Panel
    print("\n[Phase 1] Assembling Multidisciplinary Global Risk Panel (5 Domains)...")
    df_panel, records = generate_calibrated_multidisciplinary_panel(
        start_date=datetime(2020, 1, 1),
        num_days=250,
        seed=42
    )
    feature_cols = [c for c in df_panel.columns if c != "date"]
    df_features = df_panel[feature_cols]
    
    # Define primary systemic risk episode: 85th percentile stress on VIX
    q85 = np.percentile(df_panel["vix"], 85)
    target_event = (df_panel["vix"] >= q85).astype(int)
    print(f"  - Observations: {len(df_panel)} global-days")
    print(f"  - Features: {len(feature_cols)} ({', '.join(feature_cols)})")
    print(f"  - Primary Event Base Rate: {np.mean(target_event):.2%}")
    
    # 2. Run Rolling-Origin Out-of-Sample Evaluation
    print("\n[Phase 2] Executing Rolling-Origin Out-of-Sample Backtest (Horizons: 1d, 3d, 7d, 14d)...")
    backtester = RollingOriginBacktester(
        horizons=[1, 3, 7, 14],
        min_train_size=60,
        cost_loss_ratio=0.20
    )
    
    perf_table = backtester.run_backtest(
        df_features=df_features,
        target_series=target_event,
        step_size=2,
        anchor_indicator="vix"
    )
    
    # 3. Export Table 5 (Forecast Performance Across Model Ladder)
    os.makedirs("results/tables", exist_ok=True)
    csv_path = "results/tables/table_5_forecast_performance.csv"
    md_path = "results/tables/table_5_forecast_performance.md"
    
    perf_table.to_csv(csv_path, index=False)
    perf_table.to_markdown(md_path, index=False)
    
    print("\n" + "=" * 75)
    print(" TABLE 5: OUT-OF-SAMPLE FORECAST PERFORMANCE (MODEL LADDER M0 TO M7) ")
    print("=" * 75)
    print(perf_table.to_string(index=False))
    
    # 4. Compute and Export Table 8 (Propagation Matrix Pi_h for Horizon 1d and 7d)
    print("\n[Phase 3] Estimating Cross-Domain Dynamic Propagation Matrices (Pi_h)...")
    m7_model = Full4DDLMModel(anchor_indicator="vix", horizons=[1, 7])
    m7_model.fit(df_features, target_event.values)
    
    pi_1 = m7_model.get_propagation_matrix(horizon=1)
    pi_7 = m7_model.get_propagation_matrix(horizon=7)
    
    df_pi_1 = pd.DataFrame(np.round(pi_1, 3), index=feature_cols, columns=feature_cols)
    df_pi_7 = pd.DataFrame(np.round(pi_7, 3), index=feature_cols, columns=feature_cols)
    
    df_pi_1.to_csv("results/tables/table_8_propagation_matrix_h1.csv")
    df_pi_7.to_csv("results/tables/table_8_propagation_matrix_h7.csv")
    
    # 5. Generate Publication Figures (§33.2)
    print("\n[Phase 4] Generating Publication Figures (Figures 4, 7, 11)...")
    os.makedirs("results/figures", exist_ok=True)
    
    # Figure 4: DGRS Trajectory
    dgrs = SignIdentifiedDGRS(anchor_indicator="vix")
    dgrs.fit(df_features)
    _, _, ci_df = dgrs.smooth(df_features)
    plot_dgrs_trajectory(ci_df, output_path="results/figures/figure_4_dgrs_trajectory.png")
    
    # Figure 7: Propagation Heatmaps
    plot_propagation_heatmaps(df_pi_1, df_pi_7, output_path="results/figures/figure_7_propagation_heatmaps.png")
    
    # Figure 11: Model Comparison Bar Charts
    plot_model_comparison_bars(perf_table, output_path="results/figures/figure_11_model_comparison.png")
    
    print("\n[Phase 5] All Empirical Tables & Figures Successfully Exported!")
    return perf_table


if __name__ == "__main__":
    run_full_dissertation_experiment()
