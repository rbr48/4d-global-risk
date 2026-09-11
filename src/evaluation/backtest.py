"""
4D-MGRFF Rolling-Origin Out-of-Sample Backtesting Engine
Executes Section 17 & 31 pseudocode across the full model ladder (M0 to M7).
Computes Brier Score, Brier Skill Score, Log Score, ECE, PR-AUC, and Relative Value Score.
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np
import pandas as pd

from models.baselines import PersistenceModel, ClimatologyModel
from models.statistical_models import (
    SingleDomainLogisticModel,
    MultidisciplinaryRegularizedModel,
    DynamicAutoregressiveModel
)
from models.nonlinear_model import NonlinearGBDTModel
from models.full_4d_dlm import Full4DDLMModel

from .scoring import (
    compute_brier_score,
    compute_brier_skill_score,
    compute_logarithmic_score,
    compute_expected_calibration_error,
    compute_pr_auc,
    compute_relative_value_score
)


class RollingOriginBacktester:
    """
    Executes expanding-window rolling-origin evaluation without lookahead bias.
    """

    def __init__(
        self,
        horizons: List[int] = None,
        min_train_size: int = 50,
        cost_loss_ratio: float = 0.2
    ):
        self.horizons = horizons or [1, 3, 7, 14]
        self.min_train_size = min_train_size
        self.cost_loss_ratio = cost_loss_ratio
        self.forecast_records: List[Dict] = []
        self.score_summary: pd.DataFrame = pd.DataFrame()

    def run_backtest(
        self,
        df_features: pd.DataFrame,
        target_series: pd.Series,
        step_size: int = 1,
        anchor_indicator: str = "vix"
    ) -> pd.DataFrame:
        """
        Runs rolling-origin evaluation across df_features predicting target_series.
        """
        T = len(df_features)
        y = target_series.values
        
        self.forecast_records = []
        
        # Instantiate Model Suite
        model_factories = {
            "M0_Persistence": lambda: PersistenceModel(),
            "M1_Climatology": lambda: ClimatologyModel(),
            "M2_SingleDomain": lambda: SingleDomainLogisticModel(target_domain_cols=[anchor_indicator]),
            "M3_ElasticNet": lambda: MultidisciplinaryRegularizedModel(),
            "M4_DynamicAR": lambda: DynamicAutoregressiveModel(),
            "M5_LightGBM": lambda: NonlinearGBDTModel(),
            "M7_Full4D": lambda: Full4DDLMModel(anchor_indicator=anchor_indicator, horizons=self.horizons)
        }
        
        # Rolling origin loop
        origin_indices = range(self.min_train_size, T - max(self.horizons), step_size)
        
        for t in origin_indices:
            # Training window strictly prior to or at origin t
            X_train = df_features.iloc[:t].copy()
            y_train = y[:t].copy()
            
            # Realized future states for testing
            X_test_slice = df_features.iloc[t:t+1].copy()
            
            # Fit and evaluate each model in the ladder
            for model_name, factory in model_factories.items():
                model = factory()
                model.fit(X_train, y_train)
                
                for h in self.horizons:
                    realized_idx = t + h
                    if realized_idx >= T:
                        continue
                    realized_outcome = float(y[realized_idx])
                    
                    # Generate out-of-sample probability
                    pred_prob = float(model.predict_proba(X_test_slice, horizon=h)[0])
                    
                    self.forecast_records.append({
                        "origin_idx": t,
                        "horizon": h,
                        "model": model_name,
                        "prob": pred_prob,
                        "realized": realized_outcome
                    })
                    
        df_results = pd.DataFrame(self.forecast_records)
        self.score_summary = self._compute_performance_table(df_results)
        return self.score_summary

    def _compute_performance_table(self, df_results: pd.DataFrame) -> pd.DataFrame:
        """
        Calculates verification metrics per Model x Horizon.
        """
        if df_results.empty:
            return pd.DataFrame()
            
        rows = []
        models = df_results["model"].unique()
        
        for h in self.horizons:
            df_h = df_results[df_results["horizon"] == h]
            if df_h.empty:
                continue
                
            # Compute climatology baseline for BSS reference
            clim_subset = df_h[df_h["model"] == "M1_Climatology"]
            clim_prob = float(np.mean(clim_subset["realized"])) if not clim_subset.empty else 0.1
            
            for m in models:
                sub = df_h[df_h["model"] == m]
                if sub.empty:
                    continue
                    
                p = sub["prob"].values
                y = sub["realized"].values
                
                bs = compute_brier_score(p, y)
                bss = compute_brier_skill_score(p, y, climatology_prob=clim_prob)
                ls = compute_logarithmic_score(p, y)
                ece, _ = compute_expected_calibration_error(p, y, num_bins=5)
                pr_auc = compute_pr_auc(p, y)
                val_score = compute_relative_value_score(p, y, cost_loss_ratio=self.cost_loss_ratio)
                
                rows.append({
                    "Horizon": f"{h}d",
                    "Model": m,
                    "Brier_Score": round(bs, 4),
                    "BSS_vs_Clim": round(bss, 4),
                    "Log_Score": round(ls, 4),
                    "ECE": round(ece, 4),
                    "PR_AUC": round(pr_auc, 4),
                    "Relative_Value": round(val_score, 4)
                })
                
        return pd.DataFrame(rows)
