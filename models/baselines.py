"""
4D-MGRFF Baseline Models (M0 & M1)
M0: Persistence Baseline (hat p_{t+h} = Y_t)
M1: Climatology / Unconditional Base Rate (hat p = bar Y_{train})
"""

import numpy as np
import pandas as pd


class PersistenceModel:
    """M0: Persistence Baseline. Predicts most recently observed outcome."""

    def __init__(self):
        self.last_state: float = 0.0

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "PersistenceModel":
        if len(y_train) > 0:
            self.last_state = float(y_train[-1])
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        # At origin t, outcome is Y_t. For binary episode, if current state is 1, predict 1, else 0.
        # Softened slightly to avoid log-loss infinity: clip to [0.01, 0.99]
        n_samples = len(X_test)
        prob = np.clip(self.last_state, 0.01, 0.99)
        return np.full(n_samples, prob)


class ClimatologyModel:
    """M1: Climatological / Historical Base Rate Baseline."""

    def __init__(self):
        self.base_rate: float = 0.10

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "ClimatologyModel":
        if len(y_train) > 0:
            rate = float(np.mean(y_train))
            self.base_rate = np.clip(rate, 0.001, 0.999)
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        n_samples = len(X_test)
        return np.full(n_samples, self.base_rate)
