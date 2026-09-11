"""
4D-MGRFF Publication Figures Generator (§33.2)
Generates high-resolution publication charts:
  - Figure 4: Dynamic Global Risk State (DGRS) with 90% Credible Intervals
  - Figure 6/7: Cross-Domain Dynamic Propagation Heatmaps (Pi_1 vs Pi_7)
  - Figure 10: Reliability Diagrams / Calibration Curves by Horizon
  - Figure 11: Model Benchmark Ladder Performance (Brier, Log Score, Value Score)
"""

import os
from typing import Dict, List, Optional
import matplotlib
matplotlib.use("Agg")  # Headless rendering
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_dgrs_trajectory(
    df_dgrs: pd.DataFrame,
    output_path: str = "results/figures/figure_4_dgrs_trajectory.png",
    dpi: int = 300
):
    """
    Figure 4: Dynamic Global Risk State (DGRS) over time with 90% credible intervals.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 5), dpi=dpi)
    
    t_idx = range(len(df_dgrs))
    mean_val = df_dgrs["dgrs_mean"].values
    ci_lower = df_dgrs["dgrs_ci_lower_90"].values
    ci_upper = df_dgrs["dgrs_ci_upper_90"].values
    
    ax.plot(t_idx, mean_val, color="#1f77b4", linewidth=2.0, label="DGRS Posterior Mean (F_t)")
    ax.fill_between(t_idx, ci_lower, ci_upper, color="#1f77b4", alpha=0.25, label="90% Credible Interval")
    
    # 85th percentile threshold line
    q85 = np.percentile(mean_val, 85)
    ax.axhline(q85, color="#d62728", linestyle="--", linewidth=1.5, label=f"85th Percentile Stress Threshold ({q85:.2f})")
    
    ax.set_title("Figure 4: Dynamic Global Risk State (DGRS) Latent Factor Trajectory", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Time (Global-Days)", fontsize=11)
    ax.set_ylabel("Latent Risk Intensity (Standardized)", fontsize=11)
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", frameon=True, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_propagation_heatmaps(
    df_pi_1: pd.DataFrame,
    df_pi_7: pd.DataFrame,
    output_path: str = "results/figures/figure_7_propagation_heatmaps.png",
    dpi: int = 300
):
    """
    Figure 7: Cross-Domain Dynamic Propagation Heatmaps (1-Day vs 7-Day Horizon).
    Demonstrates cross-domain transmission and horizon-dependent attenuation.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(14, 6), dpi=dpi)
    
    cmap = "YlOrRd"
    
    # Subplot 1: Horizon 1-Day
    im1 = axes[0].imshow(df_pi_1.values, cmap=cmap, vmin=0.0, vmax=1.0)
    axes[0].set_title("Horizon h = 1 Day (Immediate Impulse)", fontsize=12, fontweight="bold")
    axes[0].set_xticks(range(len(df_pi_1.columns)))
    axes[0].set_yticks(range(len(df_pi_1.index)))
    axes[0].set_xticklabels(df_pi_1.columns, rotation=45, ha="right", fontsize=9)
    axes[0].set_yticklabels(df_pi_1.index, fontsize=9)
    
    # Annotate numbers
    for i in range(len(df_pi_1.index)):
        for j in range(len(df_pi_1.columns)):
            val = df_pi_1.iloc[i, j]
            color = "white" if val > 0.6 else "black"
            axes[0].text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8)
            
    # Subplot 2: Horizon 7-Day
    im2 = axes[1].imshow(df_pi_7.values, cmap=cmap, vmin=0.0, vmax=1.0)
    axes[1].set_title("Horizon h = 7 Days (Attenuated Propagation)", fontsize=12, fontweight="bold")
    axes[1].set_xticks(range(len(df_pi_7.columns)))
    axes[1].set_yticks(range(len(df_pi_7.index)))
    axes[1].set_xticklabels(df_pi_7.columns, rotation=45, ha="right", fontsize=9)
    axes[1].set_yticklabels(df_pi_7.index, fontsize=9)
    
    for i in range(len(df_pi_7.index)):
        for j in range(len(df_pi_7.columns)):
            val = df_pi_7.iloc[i, j]
            color = "white" if val > 0.6 else "black"
            axes[1].text(j, i, f"{val:.2f}", ha="center", va="center", color=color, fontsize=8)
            
    fig.suptitle("Figure 7: Cross-Domain Dynamic Propagation Matrices (Pi_1 vs Pi_7)", fontsize=14, fontweight="bold", y=1.02)
    fig.colorbar(im2, ax=axes.ravel().tolist(), orientation="vertical", shrink=0.8, label="Transmission Strength")
    
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {output_path}")


def plot_model_comparison_bars(
    perf_table: pd.DataFrame,
    output_path: str = "results/figures/figure_11_model_comparison.png",
    dpi: int = 300
):
    """
    Figure 11: Out-of-Sample Performance Comparison across Model Ladder M0 to M7.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_h1 = perf_table[perf_table["Horizon"] == "1d"].copy()
    if df_h1.empty:
        return
        
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), dpi=dpi)
    
    models = df_h1["Model"].values
    y_pos = np.arange(len(models))
    
    # 1. Brier Skill Score (Higher is better, >0 is true skill)
    bss = df_h1["BSS_vs_Clim"].values
    colors = ["#2ca02c" if b > 0 else "#d62728" for b in bss]
    
    axes[0].barh(y_pos, bss, color=colors, alpha=0.85, edgecolor="black")
    axes[0].axvline(0.0, color="black", linestyle="--", linewidth=1.2)
    axes[0].set_yticks(y_pos)
    axes[0].set_yticklabels(models, fontsize=10)
    axes[0].set_xlabel("Brier Skill Score vs Climatology (BSS)", fontsize=11)
    axes[0].set_title("Probabilistic Skill (BSS > 0 indicates outperformance)", fontsize=11, fontweight="bold")
    axes[0].grid(True, linestyle=":", alpha=0.6)
    
    # 2. Relative Decision Value Score (Higher is better)
    val_scores = df_h1["Relative_Value"].values
    val_colors = ["#1f77b4" if v > 0 else "#7f7f7f" for v in val_scores]
    
    axes[1].barh(y_pos, val_scores, color=val_colors, alpha=0.85, edgecolor="black")
    axes[1].axvline(0.0, color="black", linestyle="--", linewidth=1.2)
    axes[1].set_yticks(y_pos)
    axes[1].set_yticklabels([])
    axes[1].set_xlabel("Richardson / Murphy-Winkler Value Score (V)", fontsize=11)
    axes[1].set_title("Operational Decision Utility (V > 0 saves mitigation cost)", fontsize=11, fontweight="bold")
    axes[1].grid(True, linestyle=":", alpha=0.6)
    
    fig.suptitle("Figure 11: Out-of-Sample Model Ladder Verification (Horizon = 1 Day)", fontsize=13, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    print(f"Saved: {output_path}")
