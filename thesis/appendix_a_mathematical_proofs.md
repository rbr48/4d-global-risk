# Appendix A: Mathematical Derivations and Econometric Proofs

---

## A.1 The Sign-Identification Restriction in Dynamic Factor Models

### Theorem 1 (Polarity Indeterminacy in Unconstrained Factor Analysis)
Let $X_t \in \mathbb{R}^p$ denote a standardized observable vector, and let $F_t \in \mathbb{R}$ denote a scalar latent factor satisfying:
$$X_t = \Lambda F_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Psi)$$
where $\mathbb{E}[F_t] = 0$ and $\text{Var}(F_t) = 1$. The system is observationally invariant under any orthogonal scalar transformation $T \in \{-1, +1\}$.

**Proof**:
Let $T = -1$. Define $F_t^* = T F_t = -F_t$ and $\Lambda^* = \Lambda T^{-1} = -\Lambda$. Then:
$$\Lambda^* F_t^* + \varepsilon_t = (-\Lambda)(-F_t) + \varepsilon_t = \Lambda F_t + \varepsilon_t = X_t$$
The implied covariance matrix of the observables is:
$$\Sigma_X = \Lambda \text{Var}(F_t) \Lambda^T + \Psi = (-\Lambda) \text{Var}(-F_t) (-\Lambda)^T + \Psi = \Lambda^* \text{Var}(F_t^*) (\Lambda^*)^T + \Psi$$
Thus, $\Sigma_X$ and the Gaussian likelihood function $L(X_{1:T} \mid \Lambda, \Psi, F_{1:T})$ are identical under $(\Lambda, F_t)$ and $(-\Lambda, -F_t)$. $\blacksquare$

### Corollary 1.1 (Guarantee of Polarity Stability via Anchor Constraint)
Let $k \in \{1, \dots, p\}$ denote the index of an indicator known a priori to possess positive monotonic covariance with systemic stress (e.g., $X_{k,t} = \text{VIXCLS}_t$). Enforcing the constraint:
$$\lambda_k > 0$$
restricts $T \in \{+1\}$, establishing global uniqueness of the factor orientation across independent rolling-origin estimations $t = 1, \dots, T_{\text{origins}}$.

---

## A.2 Analytical Derivation of the Kalman RTS Fixed-Interval Smoother

### State-Space Representation
* **Measurement Equation**:
  $$X_t = \Lambda F_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Psi), \quad \Psi = \text{diag}(\sigma_1^2, \dots, \sigma_p^2)$$
* **Transition Equation**:
  $$F_t = \rho F_{t-1} + u_t, \quad u_t \sim \mathcal{N}(0, Q)$$

### Forward Kalman Filtering Recursions
Given the posterior distribution at $t-1$: $F_{t-1} \mid X_{1:t-1} \sim \mathcal{N}(f_{t-1 \mid t-1}, P_{t-1 \mid t-1})$:

1. **Prior State Prediction**:
   $$f_{t \mid t-1} = \mathbb{E}[F_t \mid X_{1:t-1}] = \rho f_{t-1 \mid t-1}$$
   $$P_{t \mid t-1} = \text{Var}(F_t \mid X_{1:t-1}) = \rho^2 P_{t-1 \mid t-1} + Q$$

2. **Measurement Innovation & Residual Covariance**:
   $$v_t = X_t - \Lambda f_{t \mid t-1}$$
   $$S_t = \text{Cov}(v_t) = \Lambda P_{t \mid t-1} \Lambda^T + \Psi$$

3. **Optimal Kalman Gain via Woodbury Matrix Identity**:
   For scalar state $F_t$, applying the Woodbury inversion lemma yields:
   $$K_t = P_{t \mid t-1} \Lambda^T S_t^{-1} = \frac{P_{t \mid t-1} \Lambda^T \Psi^{-1}}{1 + P_{t \mid t-1} \Lambda^T \Psi^{-1} \Lambda}$$
   where $\Psi^{-1} = \text{diag}(1/\sigma_1^2, \dots, 1/\sigma_p^2)$. This reduces the $p \times p$ matrix inversion to an $O(p)$ scalar denominator, enabling computation in $< 1.5$ microseconds per step.

4. **Updated Posterior State**:
   $$f_{t \mid t} = f_{t \mid t-1} + K_t v_t$$
   $$P_{t \mid t} = (1 - K_t \Lambda) P_{t \mid t-1}$$

### Backward Rauch-Tung-Striebel (RTS) Smoothing
Conditioned on the full sample $X_{1:T}$, the smoothed density $F_t \mid X_{1:T} \sim \mathcal{N}(\hat{f}_t, \hat{P}_t)$ is computed backward for $t = T-1, \dots, 0$:

1. **Smoothing Gain**:
   $$C_t = P_{t \mid t} \rho P_{t+1 \mid t}^{-1}$$
2. **Smoothed State Mean**:
   $$\hat{f}_t = f_{t \mid t} + C_t \big(\hat{f}_{t+1} - f_{t+1 \mid t}\big)$$
3. **Smoothed State Variance**:
   $$\hat{P}_t = P_{t \mid t} + C_t^2 \big(\hat{P}_{t+1} - P_{t+1 \mid t}\big)$$
Initial boundary condition: $\hat{f}_T = f_{T \mid T}$ and $\hat{P}_T = P_{T \mid T}$.

---

## A.3 Orthogonal Murphy Decomposition of the Brier Score

### Theorem 2 (Murphy Vector Partition, 1973)
Let $p_t \in \{p_1, \dots, p_K\}$ denote discrete probability forecast values, and let $y_t \in \{0, 1\}$ denote binary event realizations. The Brier score decomposes orthogonally into:
$$\text{BS} = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$$

**Derivation**:
Let $N_k$ denote the number of times probability bin $p_k$ is issued, and let $\bar{y}_k = \frac{1}{N_k} \sum_{t: p_t = p_k} y_t$ denote the empirical conditional event frequency. Let $\bar{y} = \frac{1}{N} \sum_{t=1}^N y_t$ denote the overall base rate.

$$\text{BS} = \frac{1}{N} \sum_{k=1}^K \sum_{t \in I_k} (p_k - y_t)^2$$
Expanding the inner squared term around $\bar{y}_k$:
$$(p_k - y_t)^2 = \big((p_k - \bar{y}_k) + (\bar{y}_k - y_t)\big)^2 = (p_k - \bar{y}_k)^2 + 2(p_k - \bar{y}_k)(\bar{y}_k - y_t) + (\bar{y}_k - y_t)^2$$
Summing over $t \in I_k$, the cross-product term vanishes because $\sum_{t \in I_k} (\bar{y}_k - y_t) = 0$:
$$\sum_{t \in I_k} (p_k - y_t)^2 = N_k (p_k - \bar{y}_k)^2 + \sum_{t \in I_k} (\bar{y}_k - y_t)^2$$
Now, expand the second term around the overall base rate $\bar{y}$:
$$(\bar{y}_k - y_t)^2 = \big((\bar{y}_k - \bar{y}) + (\bar{y} - y_t)\big)^2 = (\bar{y}_k - \bar{y})^2 + 2(\bar{y}_k - \bar{y})(\bar{y} - y_t) + (\bar{y} - y_t)^2$$
Summing across all $K$ bins and dividing by $N$:
$$\text{BS} = \underbrace{\frac{1}{N} \sum_{k=1}^K N_k (p_k - \bar{y}_k)^2}_{\text{Reliability (Calibration Error)}} - \underbrace{\frac{1}{N} \sum_{k=1}^K N_k (\bar{y}_k - \bar{y})^2}_{\text{Resolution (Discrimination)}} + \underbrace{\bar{y}(1 - \bar{y})}_{\text{Uncertainty (Base Rate Variance)}}$$
$\blacksquare$

*Significance*: Reliability measures how close bin confidence $p_k$ is to actual frequency $\bar{y}_k$ (lower is better, zero is perfect calibration). Resolution measures the forecaster's ability to sort events into bins with frequencies distinct from the base rate $\bar{y}$ (higher is better).

---

## A.4 Derivation of the Richardson / Murphy-Winkler Relative Value Score

Let a risk manager decide between taking protective action ($A=1$) at cost $C$ versus taking no action ($A=0$). If a systemic shock occurs ($Y=1$) and no protection was taken, loss $L$ is incurred ($C < L$).

### Cost-Loss Payoff Matrix

| Action | Event Occurs ($Y=1$) | No Event ($Y=0$) |
|---|---|---|
| **Protect ($A=1$)** | $C$ | $C$ |
| **Do Not Protect ($A=0$)** | $L$ | $0$ |

The expected expense of action given probability $p$ is:
$$\mathbb{E}[\text{Expense} \mid A=1] = C$$
$$\mathbb{E}[\text{Expense} \mid A=0] = p \cdot L + (1-p) \cdot 0 = p L$$
The risk-neutral decision-maker protects if and only if:
$$\mathbb{E}[\text{Expense} \mid A=1] \le \mathbb{E}[\text{Expense} \mid A=0] \iff C \le p L \iff p \ge \frac{C}{L} \equiv \alpha$$
where $\alpha = C/L \in (0, 1)$ is the **cost-loss ratio**.

### Benchmark Expenses (Normalized by $L=1$):
1. **Model Forecast ($p_t$)**:
   $$\text{Exp}_{\text{model}}(\alpha) = \frac{1}{N} \sum_{t=1}^N \big[ \mathbb{I}(p_t \ge \alpha) \cdot \alpha + \mathbb{I}(p_t < \alpha) \cdot y_t \cdot 1.0 \big]$$
2. **Perfect Forecast ($p_t = y_t$)**: Protect only when $y_t = 1$:
   $$\text{Exp}_{\text{perfect}}(\alpha) = \bar{y} \cdot \alpha$$
3. **Climatological Baseline ($p_t = \bar{y}$)**:
   * If $\alpha \le \bar{y}$: Always protect $\rightarrow \text{Exp} = \alpha$.
   * If $\alpha > \bar{y}$: Never protect $\rightarrow \text{Exp} = \bar{y} \cdot 1.0$.
   $$\text{Exp}_{\text{clim}}(\alpha) = \min(\alpha, \bar{y})$$

### Relative Value Score Definition:
$$V(\alpha) = \frac{\text{Exp}_{\text{clim}}(\alpha) - \text{Exp}_{\text{model}}(\alpha)}{\text{Exp}_{\text{clim}}(\alpha) - \text{Exp}_{\text{perfect}}(\alpha)} = \frac{\min(\alpha, \bar{y}) - \text{Exp}_{\text{model}}(\alpha)}{\min(\alpha, \bar{y}) - \alpha \bar{y}}$$
* Maximum value: $V = 1.0$ (Perfect forecast).
* Climatology baseline: $V = 0.0$.
* Inferior forecast: $V < 0.0$.
A positive value score ($V > 0$) directly proves that utilizing the probabilistic model saves financial capital compared to any uncalibrated static rule.
