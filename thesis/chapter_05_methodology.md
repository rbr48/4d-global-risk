# Chapter 5: Methodology and Two-Tier Inference Architecture

---

## 5.1 State-Space Formulation & The Sign-Identification Proof

The foundational econometric engine of the 4D framework is a dynamic factor state-space model that maps observable multi-domain signals into a low-dimensional systemic risk process.

### Mathematical Specification
* **Measurement Equation**:
  $$X_t = \Lambda S_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Psi)$$
* **Transition Equation**:
  $$S_t = \Phi S_{t-1} + \Gamma U_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, Q)$$
where $X_t \in \mathbb{R}^p$ represents the standardized multi-domain indicator vector, $S_t \in \mathbb{R}^D$ is the latent risk state vector, $\Lambda \in \mathbb{R}^{p \times D}$ is the factor loading matrix, and $\Phi \in \mathbb{R}^{D \times D}$ governs state persistence and cross-domain feedback.

### The Factor Rotational Indeterminacy & Sign-Flipping Trap
In standard unconstrained dynamic factor analysis, latent states and factor loadings are identified only up to an orthogonal rotation matrix $T$ such that $T T^T = I$:
$$X_t = \Lambda S_t + \varepsilon_t = (\Lambda T)(T^T S_t) + \varepsilon_t$$
In the scalar case ($D=1$, the Dynamic Global Risk State $F_t$), this simplifies to sign indeterminacy:
$$\Lambda F_t = (-\Lambda)(-F_t)$$
If factor estimation is executed independently across hundreds of daily rolling-origin windows, the numerical optimization algorithm (e.g., SVD or EM) will arbitrarily flip the polarity of the estimated state on certain days. A sudden sign inversion causes an acute crisis state ($F_t = +3.0$) to be estimated as extreme tranquility ($F_t = -3.0$), silently destroying out-of-sample forecast evaluation, continuous difference metrics ($\Delta S_t^{(h)}$), and time-series persistence diagnostics.

### The Sign-Identification Restriction
To guarantee mathematical uniqueness and polarity stability across all rolling origins, the framework imposes two formal restrictions:
1. **Triangular Structure**: The loading matrix $\Lambda$ is constrained to be block-triangular with non-negative diagonal elements: $\lambda_{dd} > 0$.
2. **Strict Anchor Constraint**: At least one primary, unambiguous barometer of systemic stress is selected as an anchor indicator. In the empirical specification, the CBOE Volatility Index (`VIXCLS`) serves as the financial anchor:
   $$\lambda_{\text{VIX}} > 0$$
   If an empirical extraction yields $\lambda_{\text{VIX}} < 0$, both the loading vector and the latent state trajectory are multiplied by $-1$:
   $$\Lambda^* = -\Lambda, \quad F_t^* = -F_t$$
This ensures that a higher value of $F_t$ unconditionally denotes higher systemic stress across every origin $t \in [1, T]$.

---

## 5.2 The Two-Tier Computational Inference Protocol

A major hurdle in dynamic Bayesian econometrics is computational intractability. Estimating time-varying parameter (TVP) models with hierarchical shrinkage priors via Hamiltonian Monte Carlo (NUTS in PyMC or Stan) requires thousands of gradient evaluations per origin. In an expanding-window rolling backtest over 10 years (~3,650 origins) across 4 horizons and multiple ablations, running full MCMC daily would require **hundreds of millions of iterations**, demanding months of high-performance compute time and risking frequent MCMC convergence failures in rolling loops.

To solve this bottleneck without sacrificing Bayesian rigor, the framework architecture defines a **Two-Tier Inference Protocol**:

```
[ Tier 1: Daily Rolling Origins — IMPLEMENTED (Current Evaluation) ]
  • Engine: Dynamic Linear Model (DLM) & Analytical Kalman Filter / RTS Smoother
  • Execution Speed: < 2.0 ms per origin
  • Output: Closed-form posterior state mean F_t and 90% credible intervals
  • Convergence: 100% analytical stability, zero divergences
  • Status: ✓ Fully operational. All empirical results in Chapter 6 use Tier 1.
            │
            ▼
[ Tier 2: Checkpoint Bayesian MCMC — ARCHITECTURAL SPECIFICATION (Future Work) ]
  • Intended Engine: No-U-Turn Sampler (NUTS in PyMC)
  • Intended Configuration: 4 chains × 2,000 warmup + 2,000 sampling draws
  • Intended Output: Full non-Gaussian posterior parameter distributions
  • Intended Function: Formal validation of Tier 1 Kalman Gaussian
    approximations via KL-divergence at quarterly checkpoint origins
  • Status: ✗ Not yet implemented. Defined as a production deployment
    extension for validating Gaussian sufficiency at structural break points.
```

> **Transparency Note**: All empirical results reported in this dissertation (Chapter 6) are produced exclusively using **Tier 1 analytical Kalman inference**. Tier 2 MCMC checkpoint validation is defined as an architectural specification for production-grade deployment where formal non-Gaussianity diagnostics are required at quarterly review intervals. The Tier 2 specification is included here to document the complete intended inference architecture; its implementation is identified as future work (§11.4). The validity of Tier 1 Gaussian approximations rests on the well-established theoretical guarantees of the Kalman filter for linear-Gaussian state-space models, which is the model class implemented in this dissertation.

### The Analytical Kalman RTS Smoother
For Tier 1, the scalar DGRS state $F_t$ is updated via the forward Kalman Filter and backward Rauch-Tung-Striebel (RTS) smoother.
1. **Forward Time Update (Predict)**:
   $$f_{t \mid t-1} = \rho f_{t-1 \mid t-1}, \quad P_{t \mid t-1} = \rho^2 P_{t-1 \mid t-1} + Q$$
2. **Forward Measurement Update (Correct)**:
   $$K_t = P_{t \mid t-1} \Lambda^T \left(\Lambda P_{t \mid t-1} \Lambda^T + \Psi\right)^{-1}$$
   $$f_{t \mid t} = f_{t \mid t-1} + K_t \big(X_t - \Lambda f_{t \mid t-1}\big)$$
   $$P_{t \mid t} = (I - K_t \Lambda) P_{t \mid t-1}$$
3. **Backward RTS Smoother**:
   $$C_t = P_{t \mid t} \rho P_{t+1 \mid t}^{-1}$$
   $$\hat{f}_t = f_{t \mid t} + C_t \big(\hat{f}_{t+1} - f_{t+1 \mid t}\big), \quad \hat{P}_t = P_{t \mid t} + C_t^2 \big(\hat{P}_{t+1} - P_{t+1 \mid t}\big)$$
The resulting 90% credible intervals are:
$$\text{CI}_{90\%}(F_t) = \big[ \hat{f}_t - 1.645 \sqrt{\hat{P}_t}, \; \hat{f}_t + 1.645 \sqrt{\hat{P}_t} \big]$$

---

## 5.3 The Multi-Horizon Model Ladder (M0 to M7)

To prove that complexity is empirically justified, the dissertation constructs an escalating ladder of alternative models evaluated under identical rolling conditions:

* **M0: Persistence Baseline**: Predicts the most recent outcome state: $\hat{p}_{t+h} = Y_t$.
* **M1: Climatology Baseline**: Predicts the unconditional historical base rate: $\hat{p}_{t+h} = \bar{Y}_{\text{train}(t)}$.
* **M2: Single-Domain Logistic**: Univariate models estimated independently for each domain to test whether cross-domain pooling adds value.
* **M3: Multidisciplinary Regularized Logistic**: Pooled $L_1/L_2$ regularized logistic regression across all observed indicators without dynamic latent states.
* **M4: Dynamic Autoregressive Model**: Augments indicator features with historical outcome lags ($Y_{t-1}, \dots, Y_{t-k}$) to capture autoregressive inertia.
* **M5: Nonlinear ML Benchmark**: Gradient Boosted Decision Trees (LightGBM) to establish a competitive non-parametric predictive ceiling.
* **M7: Full 4D Model**: Integrates the sign-anchored DGRS state ($F_t$), dynamic cross-domain interaction ($A_t$), and the multi-step horizon propagation matrix ($\Pi_h$).

---

## 5.4 Forecast Verification & Strictly Proper Scoring Rules

Evaluating probabilistic forecasts requires scoring rules that encourage honest probability reporting (Gneiting & Raftery 2007). A scoring rule $S(p, y)$ is **strictly proper** if the expected score is uniquely minimized when the forecaster issues their true subjective probability distribution.

### 1. Brier Score (BS)
$$\text{BS} = \frac{1}{N} \sum_{t=1}^N (p_t - y_t)^2$$
The Brier score measures combined reliability and sharpness (Murphy 1973). Lower values indicate superior accuracy.

### 2. Brier Skill Score (BSS)
In extreme rare-event settings (e.g., systemic crises occurring on $< 15\%$ of days), a naive forecaster who constantly predicts the low base rate will achieve an artificially low Brier score (e.g., $BS = 0.08$). To prevent this "Climatology Illusion," the dissertation mandates the **Brier Skill Score (BSS)**:
$$\text{BSS} = 1 - \frac{\text{BS}_{\text{model}}}{\text{BS}_{\text{climatology}}}$$
* $\text{BSS} > 0$: The model provides genuine predictive skill over the historical base rate.
* $\text{BSS} = 0$: The model is no better than predicting the unconditional base rate.
* $\text{BSS} < 0$: The model is worse than a trivial climatology baseline.

### 3. Logarithmic Score (LS)
$$\text{LS} = - \frac{1}{N} \sum_{t=1}^N \big[ y_t \ln p_t + (1 - y_t) \ln(1 - p_t) \big]$$
Penalizes severe overconfidence heavily when extreme events occur unexpectedly.

### 4. Precision-Recall AUC (PR-AUC)
Because standard ROC curves are notoriously over-optimistic under severe class imbalance, the dissertation uses PR-AUC as the primary discrimination metric for rare escalation events ($S_3$).

---

## 5.5 Decision-Theoretic Policy Utility ($V(\alpha)$)

Statistical loss functions satisfy econometricians, but institutional decision-makers require quantifiable economic or strategic utility. The dissertation bridges this gap by operationalizing the **Richardson / Murphy-Winkler Relative Value Score**:

Let $C$ denote the cost of taking proactive protective action (e.g., hedging commodity exposure, raising alert postures), and let $L$ denote the catastrophic loss incurred if an unmitigated systemic shock strikes ($C < L$). The decision-maker's cost-loss ratio is:
$$\alpha = \frac{C}{L} \in (0, 1)$$

Under the optimal probability decision threshold $p^* = \alpha$:
$$V(\alpha) = \frac{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{model}}(\alpha)}{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{perfect}}(\alpha)}$$
where:
$$\text{Expense}_{\text{model}}(\alpha) = \frac{1}{N} \sum_{t=1}^N \big[ \mathbb{I}(p_t \ge \alpha) \cdot \alpha + \mathbb{I}(p_t < \alpha) \cdot y_t \cdot 1.0 \big]$$
$$\text{Expense}_{\text{clim}}(\alpha) = \min(\alpha, \bar{y}), \quad \text{Expense}_{\text{perfect}}(\alpha) = \bar{y} \cdot \alpha$$

A forecasting model is operationally valuable to a risk manager if and only if $V(\alpha) > 0$.

---

## 5.6 The 10 Preregistered Falsification Criteria

The 4D framework is formally declared **unsupported** if any of the following occur under preregistered tests:
1. M7 fails to achieve a statistically superior Brier Skill Score ($\text{BSS} > 0$) over M1 (Climatology) and M5 (LightGBM).
2. Propagation matrices ($\Pi_h$) add zero out-of-sample skill over non-propagating static models.
3. Latent state ($F_t$) provides no incremental predictive value over raw predictors.
4. Out-of-sample probabilities display uncorrectable miscalibration ($\text{ECE} > 0.15$).
5. Predictive relationships evaporate under independent data source substitution.
6. Results rely entirely on a single data source (e.g., GDELT alone).
7. Strict publication-delay buffers (+24h, +48h) eliminate all apparent predictive power.
8. The model performs solely during historical crises and fails in normal periods.
9. Domain ablations reveal zero marginal contribution from 3 or more domains.
10. The Relative Value Score $V(\alpha) \le 0$ across all operational cost-loss ratios.

*A null result on any criterion is reported with complete transparency as a valid scientific finding.*
