"""
4D-MGRFF Dynamic Global Risk State (DGRS)
State-Space Latent Factor Estimator with Sign-Identification Anchoring.
Tier 1: Analytical Kalman Filter & Rauch-Tung-Striebel (RTS) Smoother.
"""

from typing import List, Tuple
import numpy as np
import pandas as pd


class SignIdentifiedDGRS:
    """
    Dynamic Global Risk State (DGRS) Latent Factor Estimator.

    Measurement Equation:
        X_t = Lambda * F_t + e_t,   e_t ~ N(0, Psi)
    Transition Equation:
        F_t = rho * F_{t-1} + u_t,  u_t ~ N(0, Q)

    Sign-Identification:
        Guarantees that Lambda[anchor_idx] > 0.
        If initial estimation yields Lambda[anchor_idx] < 0,
        both Lambda and F_t are multiplied by -1.
        This eliminates sign-flipping across rolling-origin iterations.
    """

    def __init__(
        self, anchor_indicator: str = "vix", rho: float = 0.85, process_variance: float = 0.1, max_iter: int = 50
    ):
        self.anchor_indicator = anchor_indicator
        self.rho = rho
        self.q = process_variance
        self.max_iter = max_iter

        # Estimated parameters
        self.indicators: List[str] = []
        self.lambda_loadings: np.ndarray = np.array([])
        self.psi_diag: np.ndarray = np.array([])
        self.anchor_idx: int = 0
        self.fitted: bool = False
        self.train_mean: np.ndarray = np.array([])
        self.train_std: np.ndarray = np.array([])

    def fit(self, df_train: pd.DataFrame) -> "SignIdentifiedDGRS":
        """
        Fits factor loadings Lambda and measurement variances Psi
        using an anchored principal component / EM initialization.
        """
        self.indicators = list(df_train.columns)
        p = len(self.indicators)

        if self.anchor_indicator.lower() in [ind.lower() for ind in self.indicators]:
            self.anchor_idx = [ind.lower() for ind in self.indicators].index(self.anchor_indicator.lower())
        else:
            self.anchor_idx = 0  # fallback to first column

        X = df_train.values  # (T, p)
        # Center and scale, saving training moments
        self.train_mean = np.nanmean(X, axis=0)
        self.train_std = np.nanstd(X, axis=0)
        self.train_std[self.train_std < 1e-6] = 1.0
        X_norm = (X - self.train_mean) / self.train_std
        X_clean = np.nan_to_num(X_norm, nan=0.0)

        # Initial SVD factor extraction
        u, s, vt = np.linalg.svd(X_clean, full_matrices=False)
        loadings = vt[0, :] * s[0] / np.sqrt(len(X_clean))

        # STRICT SIGN IDENTIFICATION ANCHOR
        # Ensure loading on anchor indicator (e.g. VIX or fatalities) is strictly positive
        if loadings[self.anchor_idx] < 0:
            loadings = -loadings

        self.lambda_loadings = loadings.reshape(p, 1)

        # Measurement error variance: Psi = diag(var(X - Lambda * F))
        f_init = X_clean @ self.lambda_loadings / (self.lambda_loadings.T @ self.lambda_loadings)
        residuals = X_clean - f_init @ self.lambda_loadings.T
        self.psi_diag = np.var(residuals, axis=0)
        self.psi_diag[self.psi_diag < 1e-4] = 1e-4

        self.fitted = True
        return self

    def smooth(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.DataFrame]:
        """
        Executes Kalman Filter and RTS Smoother over observations.
        Returns:
            - smoothed_state: Posterior mean of DGRS F_t
            - smoothed_std: Posterior standard deviation of F_t
            - credible_intervals: 90% credible intervals [P05, P95]
        """
        if not self.fitted:
            raise ValueError("DGRS model must be fit before smoothing.")

        cols = [c for c in self.indicators if c in df.columns]
        if len(cols) == len(self.indicators):
            X = df[self.indicators].values
        else:
            X = df.values

        if len(self.train_mean) > 0 and len(self.train_std) > 0:
            X_norm = (X - self.train_mean) / self.train_std
        else:
            X_norm = X
        X_clean = np.nan_to_num(X_norm, nan=0.0)
        T_steps, p = X_clean.shape

        # State dimension m = 1
        # System matrices
        F = np.array([[self.rho]])
        Q = np.array([[self.q]])
        inv_R = np.diag(1.0 / self.psi_diag)

        # Storage
        f_pred = np.zeros(T_steps)
        p_pred = np.zeros(T_steps)
        f_filt = np.zeros(T_steps)
        p_filt = np.zeros(T_steps)

        # Prior at t=0
        f_prev = 0.0
        p_prev = float(self.q / (1.0 - self.rho**2 + 1e-5))

        # 1. Forward Kalman Filter
        for t in range(T_steps):
            # Time update (Predict)
            f_p = float(F[0, 0] * f_prev)
            p_p = float(F[0, 0] * p_prev * F[0, 0] + Q[0, 0])
            f_pred[t] = f_p
            p_pred[t] = p_p

            # Measurement update (Correct)
            y_t = X_clean[t, :]
            # Information form / Woodbury for scalar state
            denom = float(1.0 / p_p + (self.lambda_loadings.T @ inv_R @ self.lambda_loadings).item())
            p_c = 1.0 / denom
            k_gain = p_c * (self.lambda_loadings.T @ inv_R)  # (1, p)

            err = y_t - (self.lambda_loadings.flatten() * f_p)
            f_c = float(f_p + (k_gain @ err).item())

            f_filt[t] = f_c
            p_filt[t] = p_c
            f_prev = f_c
            p_prev = p_c

        # 2. Backward RTS Smoother
        f_smooth = np.zeros(T_steps)
        p_smooth = np.zeros(T_steps)
        f_smooth[-1] = f_filt[-1]
        p_smooth[-1] = p_filt[-1]

        for t in range(T_steps - 2, -1, -1):
            c_t = float(p_filt[t] * F[0, 0] / p_pred[t + 1])
            f_smooth[t] = float(f_filt[t] + c_t * (f_smooth[t + 1] - f_pred[t + 1]))
            p_smooth[t] = float(p_filt[t] + c_t**2 * (p_smooth[t + 1] - p_pred[t + 1]))

        smoothed_std = np.sqrt(np.maximum(p_smooth, 1e-6))

        # 90% Credible Interval (z = 1.645)
        p05 = f_smooth - 1.645 * smoothed_std
        p95 = f_smooth + 1.645 * smoothed_std

        res_df = pd.DataFrame(
            {"dgrs_mean": f_smooth, "dgrs_std": smoothed_std, "dgrs_ci_lower_90": p05, "dgrs_ci_upper_90": p95},
            index=df.index,
        )

        return res_df["dgrs_mean"], res_df["dgrs_std"], res_df
