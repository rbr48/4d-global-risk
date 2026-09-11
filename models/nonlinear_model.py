"""
4D-MGRFF Nonlinear Machine Learning Benchmark (M5)
Gradient Boosted Decision Tree (GBDT) with LightGBM or self-contained Boosting Ensemble.
"""

from typing import List
import numpy as np
import pandas as pd

try:
    import lightgbm as lgb

    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


class DecisionStump:
    """Fast decision stump for self-contained boosting fallback."""

    def __init__(self):
        self.feature_idx: int = 0
        self.threshold: float = 0.0
        self.val_left: float = 0.0
        self.val_right: float = 0.0

    def fit(self, X: np.ndarray, residuals: np.ndarray):
        n_samples, n_features = X.shape
        best_loss = float("inf")

        # Grid search over feature quantiles
        for feat in range(n_features):
            vals = X[:, feat]
            thresholds = np.quantile(vals, [0.2, 0.4, 0.6, 0.8])
            for thresh in thresholds:
                left_mask = vals <= thresh
                right_mask = ~left_mask
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                v_l = float(np.mean(residuals[left_mask]))
                v_r = float(np.mean(residuals[right_mask]))
                loss = np.sum((residuals[left_mask] - v_l) ** 2) + np.sum((residuals[right_mask] - v_r) ** 2)
                if loss < best_loss:
                    best_loss = loss
                    self.feature_idx = feat
                    self.threshold = float(thresh)
                    self.val_left = v_l
                    self.val_right = v_r

    def predict(self, X: np.ndarray) -> np.ndarray:
        left_mask = X[:, self.feature_idx] <= self.threshold
        out = np.empty(len(X))
        out[left_mask] = self.val_left
        out[~left_mask] = self.val_right
        return out


class NonlinearGBDTModel:
    """
    M5: Nonlinear Machine Learning Benchmark.
    Uses LightGBM when available, otherwise self-contained gradient boosting.
    """

    def __init__(self, n_estimators: int = 35, learning_rate: float = 0.08):
        self.n_estimators = n_estimators
        self.learning_rate = learning_rate
        self.lgb_model = None
        self.stumps: List[DecisionStump] = []
        self.base_log_odds: float = 0.0
        self.feature_names: List[str] = []

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "NonlinearGBDTModel":
        self.feature_names = list(X_train.columns)
        X = X_train.values
        y = np.asarray(y_train, dtype=float)

        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        self.base_log_odds = float(np.log(base_rate / (1.0 - base_rate)))

        if HAS_LIGHTGBM and len(X) >= 20:
            try:
                self.lgb_model = lgb.LGBMClassifier(
                    n_estimators=self.n_estimators,
                    learning_rate=self.learning_rate,
                    max_depth=3,
                    num_leaves=7,
                    min_child_samples=5,
                    verbose=-1,
                )
                self.lgb_model.fit(X, y)
                return self
            except Exception:
                self.lgb_model = None  # Fallback to internal boosting

        # Self-contained gradient boosting
        current_pred = np.full(len(X), self.base_log_odds)
        self.stumps = []

        for _ in range(self.n_estimators):
            p = _sigmoid(current_pred)
            pseudo_res = y - p  # negative gradient of log-loss
            stump = DecisionStump()
            stump.fit(X, pseudo_res)
            update = stump.predict(X)
            current_pred += self.learning_rate * update
            self.stumps.append(stump)

        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X = X_test[self.feature_names].values
        if self.lgb_model is not None:
            try:
                probs = self.lgb_model.predict_proba(X)[:, 1]
                return np.clip(probs, 0.001, 0.999)
            except Exception:
                pass

        pred = np.full(len(X), self.base_log_odds)
        for stump in self.stumps:
            pred += self.learning_rate * stump.predict(X)
        return np.clip(_sigmoid(pred), 0.001, 0.999)
