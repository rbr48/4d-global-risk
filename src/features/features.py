"""
4D-MGRFF Feature Engineering Layer
Strictly origin-safe transformations, salience normalization, and rolling volatility.
"""

from typing import Dict, Tuple
import numpy as np
import pandas as pd


def compute_salience_normalized_velocity(
    event_counts: pd.Series, total_articles: pd.Series, window_length: int = 14, epsilon: float = 1e-6
) -> pd.Series:
    """
    Computes Robust Salience-Normalized Information Velocity (§11.1).
    Avoids media scraper expansion and wire syndication artifacts.

    Salience_t = N_{d,t} / TotalGlobalArticles_t
    IV_t = (Salience_t - median(Salience_{t-L:t-1})) / (MAD(Salience_{t-L:t-1}) + eps)
    """
    # Relative event salience
    salience = event_counts / (total_articles + epsilon)

    # Trailing window median & MAD strictly over past observations
    rolling_median = salience.shift(1).rolling(window=window_length, min_periods=3).median()

    def calc_mad(window_vals):
        med = np.median(window_vals)
        return np.median(np.abs(window_vals - med))

    rolling_mad = salience.shift(1).rolling(window=window_length, min_periods=3).apply(calc_mad, raw=True)

    # 1.4826 normal consistency constant for MAD
    normalized_velocity = (salience - rolling_median) / (1.4826 * rolling_mad + epsilon)
    return normalized_velocity.fillna(0.0)


def compute_rolling_volatility(prices: pd.Series, window_length: int = 7) -> pd.Series:
    """
    Computes rolling standard deviation of log returns strictly over trailing window.
    r_t = 100 * ln(P_t / P_{t-1})
    sigma_{t,k} = SD(r_{t-k+1}, ..., r_t)
    """
    returns = 100.0 * np.log(prices / prices.shift(1))
    rolling_vol = returns.rolling(window=window_length, min_periods=2).std()
    return rolling_vol.fillna(0.0)


class OriginSafeStandardizer:
    """
    Standardizer that fits statistics (mean, std) strictly on training window
    and transforms test observations without future lookahead.
    """

    def __init__(self):
        self.means: Dict[str, float] = {}
        self.stds: Dict[str, float] = {}

    def fit(self, df_train: pd.DataFrame) -> "OriginSafeStandardizer":
        """Compute training window moments."""
        numeric_cols = df_train.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            self.means[col] = float(df_train[col].mean())
            std_val = float(df_train[col].std())
            self.stds[col] = std_val if std_val > 1e-8 else 1.0
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply frozen training statistics."""
        df_out = df.copy()
        for col, mean_val in self.means.items():
            if col in df_out.columns:
                std_val = self.stds[col]
                df_out[col] = (df_out[col] - mean_val) / std_val
        return df_out

    def fit_transform(self, df_train: pd.DataFrame) -> pd.DataFrame:
        self.fit(df_train)
        return self.transform(df_train)


def compute_shock_indicators(
    standardized_df: pd.DataFrame, threshold_percentile: float = 90.0
) -> Tuple[pd.DataFrame, Dict[str, float]]:
    """
    Constructs binary shock indicators Shock_{d,t} = I(Z_{d,t} > c_d).
    Thresholds c_d are derived strictly from input training distribution.
    """
    shock_df = pd.DataFrame(index=standardized_df.index)
    thresholds = {}

    for col in standardized_df.columns:
        c_d = float(np.percentile(standardized_df[col].dropna(), threshold_percentile))
        thresholds[col] = c_d
        shock_df[f"{col}_shock"] = (standardized_df[col] >= c_d).astype(int)

    return shock_df, thresholds
