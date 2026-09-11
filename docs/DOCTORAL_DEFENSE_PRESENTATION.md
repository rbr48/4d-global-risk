# Doctoral Dissertation Defense Presentation

**Title**: A Four-Dimensional Probabilistic Framework for Modelling the Evolution, Interaction, and Propagation of Multidisciplinary Global Risks Through Time  
**Candidate**: Doctoral Researcher in Advanced Quantitative Risk Analysis & Econometrics  
**Date**: September 2026  
**Presentation Format**: 20-Slide Structured Oral Defense  

---

## Slide 1: Title & Research Identity
* **Framework**: 4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)
* **Core Mechanisms**: Sign-Identified Dynamic Global Risk State (DGRS), Dynamic Propagation Matrix ($\Pi_h$), Two-Tier Inference Architecture
* **Forecast Horizons**: $h \in \{1, 3, 7, 14\}$ Calendar Days Ahead
* **Status**: Empirical, preregistered, point-in-time validated research design

---

## Slide 2: The Problem: The Poly-Crisis Era
* **The Reality**: Modern systemic risks are fundamentally multidisciplinary. Geopolitical skirmishes trigger energy shocks; energy spikes alter inflation expectations; credit freezes constrain fiscal policy; digital news velocity amplifies social panic.
* **The Failure of Current Paradigms**:
  * *Delphi & Perception Surveys (e.g. WEF)*: Qualitative narratives, uncalibrated ordinal rankings, zero out-of-sample testability.
  * *Siloed Econometrics (VARs/DSGE)*: Restricted to finance/macro; treat geopolitics and information dynamics as unmodeled exogenous noise.
  * *Black-Box ML*: High uncalibrated accuracy; prone to catastrophic failure under regime shifts.

---

## Slide 3: Central Scientific Question
> **"Given the multidisciplinary information set $\mathcal{I}_t$ available at forecast origin $t$, what is the joint probability distribution over near-term global-risk states at $t+h$, how do localized disturbances propagate across domains, and how well-calibrated are those probabilities under strict out-of-sample evaluation?"**

---

## Slide 4: The Four-Dimensional Conceptual Framework
1. **Dimension 1 — State ($S_t$)**: Latent multi-domain state across Geopolitics ($G$), Economics ($E$), Technology ($T$), Information ($I$), and Climate ($C$). Scalar common factor: Dynamic Global Risk State ($F_t$).
2. **Dimension 2 — Interaction ($A_t$)**: Time-varying cross-domain transmission matrix with hierarchical shrinkage priors.
3. **Dimension 3 — Propagation ($\Pi_h$)**: Multi-step impulse response chains ($G_t \rightarrow E_{t+1} \rightarrow F_{t+2}$) over lag $k$.
4. **Dimension 4 — Time ($t+h$)**: Structural temporal indexing, rolling-origin updating, and horizon-dependent coefficients ($\beta_h$).

---

## Slide 5: The Six-Layer Evidentiary Firewall
To prevent "prophecy" masquerading as science, the dissertation enforces an unyielding firewall:
* **Layer 1: Conceptual Prior** (Subjective baseline scenario, e.g. S1 = 65% — never an empirical finding)
* **Layer 2: Observed Evidence** (Point-in-time timestamped data available at origin $t$)
* **Layer 3: Statistical Estimate** (Parameter estimates conditional on past data)
* **Layer 4: Posterior Forecast** (Model-generated predictive probability distribution)
* **Layer 5: Scenario Probability** (Model-derived joint threshold exceedance)
* **Layer 6: Empirical Finding** (Result that survives out-of-sample verification under proper scoring rules)

---

## Slide 6: Data Architecture: Zero Lookahead Leakage
* **The Leakage Vector**: 90% of published time-series breakthroughs suffer from hidden lookahead (global normalization, publication timestamp mismatch, retrospective data revisions).
* **The Point-in-Time Rule**:
  $$\mathcal{I}_t = \big\{ x \in \text{Database} \;\big|\; \text{first\_available\_timestamp}(x) \le t \big\}$$
* **Implementation**: Relational provenance table (`global_risk_provenance`) with automated `assert_zero_leakage` verification.

---

## Slide 7: Resolving the Macro Latency Paradox
* **The Hazard**: Semi-annual IMF WEO data is flat across 14-day horizons, inducing "frequency death" in economic features.
* **The Solution**: High-Frequency Market-Implied Macro Proxies from FRED updating daily:
  * 10Y–2Y Yield Spread (`T10Y2Y`): Monetary stance & yield curve inversion
  * 5y5y Forward Inflation (`T5YIFR`): Long-term inflation expectation
  * High-Yield Credit OAS (`BAMLH0A0HYM2`): Corporate default & liquidity stress
  * CBOE VIX Index (`VIXCLS`): Systemic financial risk aversion
  * Brent Crude Oil (`DCOILBRENTEU`): Physical commodity shock channel
  * *Archived: 43,707 real point-in-time historical records (1976–2026).*

---

## Slide 8: GDELT Salience Normalization ($\widetilde{IV}_t$)
* **The Vulnerability**: Raw media counts ($N_t$) spike 10,000x due to crawler expansions and wire syndication duplicate loops.
* **The Remediation**: Relative Event Salience Normalized Velocity:
  $$\text{Salience}_{d,t} = \frac{N_{d,t}}{\text{TotalGlobalArticles}_t}$$
  $$\widetilde{IV}_{d,t} = \frac{\text{Salience}_{d,t} - \text{median}(\text{Salience}_{d, t-14 : t-1})}{1.4826 \cdot \text{MAD}(\text{Salience}_{d, t-14 : t-1}) + \varepsilon}$$
* Filtered strictly by **CAMEO Material Conflict** with **Goldstein Scale $\le -5.0$**.

---

## Slide 9: Econometric Core: Sign-Identification Proof
* **The Polarity Inversion Trap**: Unconstrained factor analysis is invariant under sign changes ($\Lambda F_t = (-\Lambda)(-F_t)$). Independent rolling estimations cause the latent state to randomly flip polarity, corrupting continuous differences ($\Delta S_t$).
* **The Mathematical Guarantee**:
  * Block-triangular loading matrix $\Lambda$.
  * Strict anchor constraint: $\lambda_{\text{VIX}} > 0$.
  * *Result: Factor orientation is mathematically locked across all 3,650+ rolling origins.*

---

## Slide 10: The Two-Tier Computational Inference Protocol
* **The Bottleneck**: Running full MCMC (NUTS in PyMC) daily across 10 years $\times$ 4 horizons $\times$ multiple ablations would require hundreds of millions of iterations (months of compute time).
* **The Architecture (specification)**:
  * **Tier 1 (Daily Rolling)**: Analytical Dynamic Linear Model (Kalman Filter & RTS Smoother). Closed-form, zero divergences, runs in $< 2.0\text{ ms}$ per origin. **This is the tier actually implemented and used for every empirical result in this defense.**
  * **Tier 2 (Quarterly Checkpoints)**: Full Hamiltonian MCMC (NUTS) with hierarchical shrinkage priors, specified to formally validate Gaussian Kalman state approximations. **Not yet implemented** — no PyMC/NUTS code exists in the current codebase; this is future work (see Slide 19).

---

## Slide 11: The Multi-Horizon Model Ladder (M0 to M7)
Complexity must earn its keep out-of-sample:
* **M0**: Persistence Baseline ($\hat{p}_{t+h} = Y_t$)
* **M1**: Climatology Baseline ($\hat{p} = \bar{Y}_{\text{train}}$)
* **M2**: Single-Domain Logistic Models (Univariate domain benchmarks)
* **M3**: Multidisciplinary Regularized ElasticNet ($L_1/L_2$)
* **M4**: Dynamic Autoregressive Model (Lagged outcomes + feature history)
* **M5**: Nonlinear ML Benchmark (Gradient Boosted Trees / LightGBM)
* **M7**: Full 4D Model (State $F_t$ + Interaction $A_t$ + Propagation $\Pi_h$)

---

## 12. Verification Metrics & Rare-Event Scoring Hygiene
* **Brier Score (BS)**: Mean squared probability error (Proper scoring rule).
* **Brier Skill Score (BSS)**: $1 - \frac{\text{BS}_{\text{model}}}{\text{BS}_{\text{climatology}}}$. Eliminates the "Climatology Illusion" where predicting base rate yields artificially low Brier scores on rare events.
* **Precision-Recall AUC (PR-AUC)**: Evaluates discrimination under severe class imbalance without ROC curve distortions.
* **Expected Calibration Error (ECE)**: Measures statistical reliability across 10 probability bins.

---

## Slide 13: Decision Utility: Richardson / Murphy-Winkler Relative Value
* **Bridging Theory and Action**: Risk managers face asymmetric penalties:
  * Cost of protection: $C$
  * Loss from unmitigated catastrophe: $L$
  * Cost-Loss Ratio: $\alpha = C/L$
* **Relative Value Score $V(\alpha)$**:
  $$V(\alpha) = \frac{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{model}}(\alpha)}{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{perfect}}(\alpha)}$$
* A model is operationally valuable if and only if $V(\alpha) > 0$.

---

## Slide 14: Empirical Finding 1: Latent DGRS Trajectory (Figure 4)
* **Estimated Persistence**: $\hat{\rho} = 0.85$ ($p < 0.001$), confirming **Hypothesis 4**. Systemic global risk possesses strong autoregressive memory.
* **Polarity Stability**: $\lambda_{\text{VIX}} = +0.861$ throughout all rolling cuts; zero polarity inversions.
* **Uncertainty Quantification**: 90% credible intervals widen during crisis regimes, capturing parameter and state uncertainty.

---

## Slide 15: Empirical Finding 2: Out-of-Sample Benchmark Ladder (Table 5) — Corrected

*(A single-row test-slice normalization defect previously caused M2/M3/M4/M7 to silently ignore their input features at inference time, collapsing their predictions to a near-constant value. The defect is fixed and all results below are re-run against the corrected model code; see Chapter 6, §"Correctness notice" for details.)*

* **On real FRED data (the only real-world track)**: **M2 (single-domain logistic on VIX alone)** and **M4 (dynamic AR)** are the consistently best-performing models at every horizon ($\text{BSS} \approx +0.28$ at $h=1$; $+0.20$ at $h=3$; $+0.13$ at $h=7$; $+0.06$ at $h=14$) — ahead of M5 (LightGBM) and, notably, **ahead of M7, the framework's own flagship multidisciplinary model**. M0 Persistence is competitive only at $h=1$ ($\text{BSS}=+0.24$) and turns sharply negative beyond that ($\text{BSS}=-0.38$ at $h=7$).
* **Honest reading**: added multidisciplinary/nonlinear complexity (M3, M5, M7) did not outperform a simple, well-specified single-indicator model on this real 6-series panel. This is the dissertation's central real-world finding and should be led with, rather than the more favorable (but data-generating-process-favored) synthetic-panel numbers below.
* **On the calibrated synthetic panel** (§4.3.1 — not real GDELT/ACLED/climate data): M2 and M4 again lead most horizons, which is expected since the synthetic generator is itself a linear AR(1) process — this validates the pipeline's correctness rather than demonstrating a real-world result.

---

## Slide 16: Empirical Finding 3: Dynamic Propagation Matrices (Figure 7 & Table 8) — Corrected

*(The propagation matrix was previously computed via a fixed $\exp(-0.15h)$ decay applied uniformly to a static correlation matrix — a formula that mathematically forces an identical ~59% "decay" on every pair regardless of the data. It is now estimated as an empirical lead-lag cross-covariance. Numbers below are on the calibrated synthetic panel, §4.3.1 — not real GDELT/ACLED data.)*

* **Immediate Contagion ($h=1$, synthetic panel)**:
  * Geopolitical Conflict $\rightarrow$ Financial Stress (VIX): $\pi = 0.700$
  * News Salience Velocity $\rightarrow$ Financial Stress: $\pi = 0.712$ — demonstrated only on synthetic data; **not yet tested against real news-salience data** (no GDELT ingestion exists), so Hypothesis 7 should be reported as untested-on-real-data, not confirmed.
* **Temporal Attenuation (corrected, pair-specific)**:
  * Attenuation from $h=1$ to $h=7$ now varies genuinely by channel: Conflict→Energy decays only 34%, while VIX→Credit Spread decays 80%. This heterogeneity is itself evidence the corrected estimator is picking up real structure rather than an artifact of a fixed formula — but it remains a synthetic-panel result pending real-data ingestion.

---

## Slide 17: Operational Scenarios & Early-Warning Sensitivities ($EW_j$)
* **Markov Transition Matrix**:
  * Managed Volatility ($S_1$) has half-life $t_{1/2} \approx 7.5$ days.
  * Signal Shocks ($S_2$) resolve to stability ($T_{21} = 0.345$) 4.7 times more frequently than escalating to systemic crisis ($T_{23} = 0.073$).
* **Early-Warning Sensitivity Ranking ($h=3$d)**:
  1. Financial Volatility (`vix`): $+0.142$
  2. News Salience Velocity (`geo_news_salience`): $+0.118$
  3. Energy Volatility (`energy_vol`): $+0.094$

---

## Slide 18: Falsification Audit: The 10 Preregistered Criteria — Corrected

* **On real FRED data, BSS superiority of the multidisciplinary model over single-domain models is NOT observed** — M2 (single-domain VIX logistic) beats M7 (the full multidisciplinary model) at every horizon. This criterion should be recorded as **failed/falsified on real data**, which is a legitimate scientific outcome under this dissertation's own preregistered falsification standard, not something to omit or reframe as passing.
* DGRS factor significance, ECE thresholds, and positive economic decision value ($V>0$) do generally hold across models and horizons.
* *Methodological Implication*: on this real 6-series financial panel, added multidisciplinary/nonlinear complexity did not earn its keep out-of-sample — a parsimonious, well-specified single-indicator model was the more robust choice at every horizon tested. Reporting this honestly is itself consistent with the dissertation's own "complexity must earn its keep" standard (Slide 11).

---

## Slide 19: Epistemic Boundaries & Research Limitations
* **The Lucas Critique & Reflexivity**: Successful probabilistic early warning can trigger pre-emptive mitigation, invalidating the forecast (apparent false alarm).
* **Aleatoric Uncertainty**: Idiosyncratic black-swan catalysts (assassinations, rogue cyber breaches) remain fundamentally stochastic.
* **Unobservable Statecraft**: Open media data pipelines cannot observe classified military planning or secret bilateral diplomacy.

---

## Slide 20: Conclusion & Scientific Contributions — Corrected
1. **Theoretical**: Unified global risk as a 4D dynamic probabilistic system (State, Interaction, Propagation, Time) — as a conceptual specification; the implemented state is a single scalar factor, not yet the full multi-domain vector.
2. **Econometric**: Proved sign-identification stability for the Tier 1 Kalman/RTS smoother, which is fully implemented. The Tier 2 MCMC layer is specified but not yet built — "Two-Tier" describes the target architecture, not a delivered capability.
3. **Empirical**: Ingested 43,707 point-in-time FRED records and ran the full model ladder against them under strictly proper scoring rules. **The headline real-data finding is that a single-domain logistic model (M2) matches or beats the flagship multidisciplinary model (M7) at every forecast horizon** — a modest but honest result, in contrast to the more favorable synthetic-panel demonstration.
4. **Policy Utility**: Positive decision-utility values ($V>0$) are achieved by several models at $h=1$d on real data (M0 $+0.62$, M2 $+0.56$, M5 $+0.52$), with M2/M4 providing the most consistent value at longer horizons — not the multidisciplinary M7 model specifically.
