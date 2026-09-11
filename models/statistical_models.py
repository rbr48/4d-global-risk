"""
4D-MGRFF Statistical Benchmark Models (M2, M3, M4)
M2: Single-Domain Logistic Models
M3: Multidisciplinary Regularized Logistic (L2 Ridge / ElasticNet)
M4: Dynamic Autoregressive Model

Fixed: Caches training mean and std moments during fit() to prevent
single-row inference feature collapse in rolling-origin backtests.
"""

from typing import List, Optional
import numpy as np
import pandas as pd
from scipy.optimize import minimize


def _sigmoid(z: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(z, -25.0, 25.0)))


class SingleDomainLogisticModel:
    """
    M2: Fits a separate logistic model per domain and evaluates the best single-domain predictor.
    """

    def __init__(self, target_domain_cols: Optional[List[str]] = None):
        self.target_domain_cols = target_domain_cols or []
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "SingleDomainLogisticModel":
        cols = [c for c in self.target_domain_cols if c in X_train.columns]
        if not cols:
            cols = list(X_train.columns)

        X = X_train[cols].values
        self.train_mean = np.mean(X, axis=0)
        self.train_std = np.std(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        X_norm = (X - self.train_mean) / self.train_std
        y = np.asarray(y_train, dtype=float)

        n_features = X_norm.shape[1]

        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = 0.1 * np.sum(w**2)
            return nll + reg

        init_params = np.zeros(n_features + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_params[0] = np.log(base_rate / (1.0 - base_rate))

        res = minimize(loss, init_params, method="BFGS")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        self.target_domain_cols = cols
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X = X_test[self.target_domain_cols].values
        # Use frozen training moments to normalize test data
        X_norm = (X - self.train_mean) / self.train_std
        probs = _sigmoid(self.intercept + X_norm @ self.weights)
        return np.clip(probs, 0.001, 0.999)


class MultidisciplinaryRegularizedModel:
    """
    M3: Pooled Multidisciplinary Regularized Logistic Regression with L2 shrinkage.
    """

    def __init__(self, l2_penalty: float = 1.0):
        self.l2_penalty = l2_penalty
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.feature_names: List[str] = []
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "MultidisciplinaryRegularizedModel":
        self.feature_names = list(X_train.columns)
        X = X_train.values
        self.train_mean = np.mean(X, axis=0)
        self.train_std = np.std(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        X_norm = (X - self.train_mean) / self.train_std
        y = np.asarray(y_train, dtype=float)

        n_features = X_norm.shape[1]

        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = self.l2_penalty * np.sum(w**2)
            return nll + reg

        init_params = np.zeros(n_features + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_params[0] = np.log(base_rate / (1.0 - base_rate))

        res = minimize(loss, init_params, method="BFGS")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X = X_test[self.feature_names].values
        # Use frozen training moments to normalize test data
        X_norm = (X - self.train_mean) / self.train_std
        probs = _sigmoid(self.intercept + X_norm @ self.weights)
        return np.clip(probs, 0.001, 0.999)


class DynamicAutoregressiveModel:
    """
    M4: Dynamic Autoregressive Model including lagged domain indicators and historical outcome persistence.
    """

    def __init__(self, num_lags: int = 3, l2_penalty: float = 0.5):
        self.num_lags = num_lags
        self.l2_penalty = l2_penalty
        self.weights: np.ndarray = np.array([])
        self.intercept: float = 0.0
        self.cols: List[str] = []
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])
        self.X_history: np.ndarray = np.array([])

    def fit(self, X_train: pd.DataFrame, y_train: np.ndarray) -> "DynamicAutoregressiveModel":
        self.cols = list(X_train.columns)
        X_mat = X_train.values
        T, p = X_mat.shape

        # Save trailing history for building true lags at inference time
        self.X_history = X_mat[-self.num_lags :, :].copy()

        lag_features = [X_mat]
        for lag in range(1, self.num_lags + 1):
            shifted = np.roll(X_mat, shift=lag, axis=0)
            shifted[:lag, :] = shifted[lag, :]  # pad start
            lag_features.append(shifted)

        X_all = np.hstack(lag_features)
        self.train_mean = np.mean(X_all, axis=0)
        self.train_std = np.std(X_all, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0

        X_norm = (X_all - self.train_mean) / self.train_std
        y = np.asarray(y_train, dtype=float)

        n_features = X_norm.shape[1]

        def loss(params):
            b0 = params[0]
            w = params[1:]
            p = _sigmoid(b0 + X_norm @ w)
            p = np.clip(p, 1e-12, 1.0 - 1e-12)
            nll = -np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p))
            reg = self.l2_penalty * np.sum(w**2)
            return nll + reg

        init_params = np.zeros(n_features + 1)
        base_rate = np.clip(np.mean(y), 0.01, 0.99)
        init_params[0] = np.log(base_rate / (1.0 - base_rate))

        res = minimize(loss, init_params, method="BFGS")
        self.intercept = float(res.x[0])
        self.weights = res.x[1:]
        return self

    def predict_proba(self, X_test: pd.DataFrame, horizon: int = 1) -> np.ndarray:
        X_mat = X_test[self.cols].values
        n_test = len(X_mat)

        # Build lag features using training history when test length is short
        if n_test <= self.num_lags and len(self.X_history) >= self.num_lags:
            full_series = np.vstack([self.X_history, X_mat])
            # For each row in X_test, slice the appropriate lags
            test_rows = []
            for i in range(n_test):
                target_idx = len(self.X_history) + i
                row_features = [full_series[target_idx : target_idx + 1, :]]
                for lag in range(1, self.num_lags + 1):
                    lag_row = full_series[target_idx - lag : target_idx - lag + 1, :]
                    row_features.append(lag_row)
                test_rows.append(np.hstack(row_features))
            X_all = np.vstack(test_rows)
        else:
            lag_features = [X_mat]
            for lag in range(1, self.num_lags + 1):
                shifted = np.roll(X_mat, shift=lag, axis=0)
                lag_features.append(shifted)
            X_all = np.hstack(lag_features)

        # Use frozen training moments to normalize test data
        X_norm = (X_all - self.train_mean) / self.train_std
        probs = _sigmoid(self.intercept + X_norm @ self.weights)
        return np.clip(probs, 0.001, 0.999)
