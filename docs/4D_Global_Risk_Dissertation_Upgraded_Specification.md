# A Four-Dimensional Probabilistic Framework for Modelling the Evolution, Interaction, and Propagation of Multidisciplinary Global Risks Through Time

**Upgraded Master Dissertation Specification — Reconciled Integrated Edition**  
*Academic Standard: Empirical, Probabilistic, Bayesian, Dynamic, and Out-of-Sample Validated*

---

## Table of Contents
1. Executive Research Statement
2. Abstract
3. Research Integrity and the Evidentiary Hierarchy
4. Research Problem
5. Research Aim and Objectives
6. Research Questions and Hypotheses
7. The Four-Dimensional Conceptual Framework
8. Formal Model Specification & Identifiability
9. Empirical Design & Outcome Architecture
10. Data Architecture & Point-in-Time Hygiene
11. Origin-Safe Feature Engineering & Salience Normalization
12. Model Hierarchy and Benchmarks (M0 to M7)
13. Dynamic Bayesian & State-Space Inference Architecture (Two-Tier Protocol)
14. Model Validation & Diagnostic Hierarchy
15. Cross-Domain Propagation Analysis
16. Operationalized Scenario & Early-Warning Dynamics
17. Rolling-Origin Out-of-Sample Evaluation Protocol
18. Forecast Verification & Rare-Event Scoring Hygiene
19. Dynamic Calibration Procedure
20. Forecast Comparison and Statistical Testing
21. Ablation Analysis
22. Crisis, Regime, and Structural-Break Analysis
23. Distribution-Shift and Robustness Test Suite
24. Forecast Updating and Vintage Archive
25. Causal Demarcation, Statistical Reporting & Decision Utility
26. Contemporary Information Environment
27. Data Quality Risks and Limitations
28. Preregistered Falsification Criteria
29. Preregistration Requirements
30. Reproducible Computational Architecture
31. Algorithmic Pipeline & Execution Logic
32. Immediate Empirical Execution Plan
33. Tables and Figures to Be Produced
34. Empirical Results Chapter Template
35. Dissertation Chapter Structure
36. Expected Scientific & Practical Decision Contribution
37. Conceptual Priors Versus Empirical Posteriors
38. Dissertation Readiness Gate
39. References
40. Final Methodological Statement
41. Proposed Research Identity

---

## 1. Executive Research Statement
This dissertation establishes a four-dimensional probabilistic framework for modelling the evolution, interaction, and propagation of multidisciplinary global risks through time.

Conventional global risk analysis predominantly relies on static, annual survey perceptions (e.g., WEF Global Risks Report) or isolated single-domain econometric models. This framework extends risk science by making **time an explicit modelling dimension** across rolling near-term horizons ($h \in \{1, 3, 7, 14\}$ days). The four structural dimensions are:
1. **State ($S_t$)**: The latent joint condition of multiple interacting risk domains at time $t$.
2. **Interaction ($A_t$)**: Time-varying dependencies and feedback loops among domains.
3. **Propagation ($\Pi_h$)**: Multi-step transmission of localized shocks across the interconnected global network.
4. **Time ($t+h$)**: The dynamic evolution of states, uncertainty distributions, and scenario probabilities under strict point-in-time information sets.

The core scientific question is:
> *Given the information available at forecast origin $t$, what is the joint probability distribution over near-term global-risk states and events at $t+h$, how do disturbances propagate across domains, and how well-calibrated are those probabilities?*

---

## 2. Abstract
Global risks do not occur in disciplinary silos. Geopolitical friction triggers energy benchmark shocks; energy shocks feed inflation expectations and sovereign yield spreads; credit tightness constrains policy maneuverability; elevated information velocity amplifies social panic; and extreme climatic anomalies compound structural stress. 

This dissertation develops and empirically evaluates the **4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)**. The empirical architecture assembles a versioned, timestamped panel from 2015 onward, combining high-frequency media data (GDELT), political violence/protest events (ACLED), financial and commodity benchmarks, market-implied high-frequency macroeconomic proxies, policy signals, and observational climate indicators.

To guarantee computational tractability and empirical rigor across ~3,650 daily rolling origins, the methodology defines a **Two-Tier Inference Protocol**: daily rolling estimation uses analytical Dynamic Linear Models (Kalman Filter and Fixed-Interval Smoother) for all empirical evaluations, while specifying a quarterly checkpoint Bayesian MCMC validation layer for production deployment. Latent factor states are identified via strict sign constraints ($\lambda_{\text{stress}} > 0$) to eliminate rolling polarity inversions.

Evaluation uses strictly proper scoring rules (Brier Score, Brier Skill Score against climatology, Logarithmic Score, and CRPS), Precision-Recall AUC for rare multi-domain escalation events ($S_3$), reliability curves, Expected Calibration Error (ECE), and a decision-theoretic Relative Value Score ($V$). The dissertation enforces explicit preregistered falsification criteria, ensuring that null results are preserved as valid scientific findings.

---

## 3. Research Integrity and the Evidentiary Hierarchy
The dissertation enforces a strict six-layer firewall between analytical assumptions and empirical findings:

| Layer | Scientific Meaning | Permissible Treatment |
|---|---|---|
| **Layer 1: Conceptual Prior** | Analytical expectation or subjective baseline | Benchmark reference point only; never an empirical finding. |
| **Layer 2: Observed Evidence** | Timestamped data strictly available at origin $t$ | Information set $\mathcal{I}_t = \{x : \text{availability}(x) \le t\}$. |
| **Layer 3: Statistical Estimate** | Model parameter estimated from training data | Point estimate or posterior distribution conditional on $\mathcal{I}_t$. |
| **Layer 4: Posterior Forecast** | Probability distribution for $t+h$ | Model-generated probability subject to evaluation. |
| **Layer 5: Scenario Probability** | Model-derived probability of defined joint state | Evaluated against realized multi-domain threshold breaches. |
| **Layer 6: Empirical Finding** | Out-of-sample result surviving validation | Verified only after comparison with subsequently observed outcomes. |

*Fundamental Rule*: No numerical probability may be presented as a validated finding until it has been generated from information available at the forecast origin and evaluated against subsequently realized outcomes under proper scoring rules.

---

## 4. Research Problem
Conventional forecasting models evaluate single-domain conditional distributions:
$$P(Y_{t+h} \mid X_t)$$
The 4D framework instead estimates the joint, evolving density of outcomes, indicators, and latent states:
$$P(Y_{t+h}, X_{t+h}, S_{t+h} \mid \mathcal{D}_{1:t})$$
where:
* $S_t \in \mathbb{R}^d$: Latent multidisciplinary risk state vector;
* $X_t \in \mathbb{R}^p$: Observed high-frequency domain indicators;
* $Y_{t+h} \in \{0, 1\}$ or $\mathbb{R}$: Future event or continuous volatility target;
* $\mathcal{D}_{1:t}$: Point-in-time information set up to origin $t$;
* $h \in \{1, 3, 7, 14\}$ days.

---

## 5. Research Aim and Objectives
**Aim**: To formulate, estimate, validate, and dynamically calibrate a four-dimensional probabilistic framework for near-term global-risk forecasting that models cross-domain interaction, shock propagation, and decision utility.

**Objectives**:
1. Construct a leakage-proof, point-in-time timestamped multidisciplinary global database.
2. Formulate a sign-identified Dynamic Global Risk State (DGRS) latent factor model.
3. Establish a Two-Tier computational engine (Kalman Smoother daily + Checkpoint MCMC).
4. Estimate time-varying cross-domain interaction matrices ($A_t$) and horizon propagation matrices ($\Pi_h$).
5. Benchmark the full 4D model against an escalating ladder of alternatives (M0 to M6).
6. Evaluate probabilistic skill using Brier Skill Score, Log Score, CRPS, and ECE.
7. Overcome rare-event evaluation bias via PR-AUC and cost-loss decision utility ($V$).
8. Conduct full ablation analysis across all 5 domains and structural components.
9. Execute preregistered robustness checks across crises, alternative thresholds, and placebo tests.
10. Test all 10 preregistered falsification criteria.

---

## 6. Research Questions and Hypotheses

| RQ | Research Question | Testable Hypothesis |
|---|---|---|
| **RQ1** | Does multidisciplinary data improve probabilistic skill over single-domain models? | **H1**: Multidisciplinary models achieve strictly lower out-of-sample proper-scoring loss and positive Brier Skill Score ($\text{BSS} > 0$) relative to the best single-domain benchmark. |
| **RQ2** | Are there measurable lagged predictive relationships across risk domains? | **H2**: Lagged source-domain indicators provide statistically significant incremental predictive skill ($\Delta \text{Skill}_{ij,h} > 0$) for target domains. |
| **RQ3** | Does explicit shock-propagation modelling improve multi-horizon forecasts? | **H3**: Propagation-aware models ($\Pi_h$) outperform static or non-propagating benchmarks at $h \in \{7, 14\}$ days. |
| **RQ4** | Are systemic global risk states temporally persistent? | **H4**: The latent DGRS factor displays positive autoregressive persistence ($\rho > 0$) after controlling for exogenous shocks. |
| **RQ5** | Does dynamic Bayesian/state-space calibration improve probability reliability? | **H5**: Dynamic calibration yields significantly lower Expected Calibration Error (ECE) and slope closer to 1 than static benchmarks. |
| **RQ6** | Does domain predictive contribution vary across forecast horizons? | **H6**: High-frequency indicators (information velocity, financial volatility) dominate at $h=1,3$, while structural/macro proxies dominate at $h=7,14$. |
| **RQ7** | Does normalized information velocity predict subsequent systemic volatility? | **H7**: Salience-normalized information velocity ($\widetilde{IV}_t$) exhibits positive predictive association with subsequent 3-day and 7-day systemic volatility. |

---

## 7. The Four-Dimensional Conceptual Framework

### 7.1 Dimension 1 — State ($S_t$)
The system represents global stress as a 5-dimensional latent vector:
$$S_t = \big(S_{G,t}, S_{E,t}, S_{T,t}, S_{I,t}, S_{C,t}\big)^T$$
representing Geopolitics ($G$), Economics/Finance ($E$), Technology/AI ($T$), Information/Society ($I$), and Climate/Environment ($C$).

### 7.2 Dimension 2 — Interaction ($A_t$)
Cross-domain transmission is governed by a time-varying transition matrix:
$$S_t = A_t S_{t-1} + B_t X_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, Q)$$
where $a_{ij,t}$ reflects the transmission from domain $j$ to domain $i$. Relationships evolve as:
$$a_{ij,t} = a_{ij,t-1} + \nu_{ij,t}, \quad \nu_{ij,t} \sim \mathcal{N}(0, \tau_{ij}^2)$$
regularized via hierarchical horseshoe shrinkage priors to avoid overparameterization.

### 7.3 Dimension 3 — Propagation ($\Pi_h$)
The multi-step propagated impact of an innovation $U_t$ across horizon $h$ is:
$$P_{t,h} = \left(\prod_{k=0}^{h-1} A_{t+h-k}\right) B_t U_t$$
Pairwise propagation is summarized in the matrix $\Pi_h = [\pi_{ij,h}]$, where:
$$\pi_{ij,h} = P(X_{j,t+h} > q_j \mid \text{Shock}_{i,t})$$

### 7.4 Dimension 4 — Time ($t+h$)
All information sets, transformations, and predictive densities are strictly indexed by forecast origin $t$, generating explicit horizon-dependent trajectories:
$$p(X_{t+h} \mid \mathcal{I}_t), \quad h \in \{1, 3, 7, 14\}$$

---

## 8. Formal Model Specification & Identifiability

### 8.1 State-Space Representation & Strict Sign-Anchoring
To prevent rotational indeterminacy and sign-flipping across rolling origins:
* **Measurement Equation**:
  $$X_t = \Lambda S_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Psi)$$
* **Transition Equation**:
  $$S_t = \Phi S_{t-1} + \Gamma U_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, Q)$$

**Identifiability Restrictions**:
1. $\Psi = \text{diag}(\sigma_{\varepsilon,1}^2, \dots, \sigma_{\varepsilon,p}^2)$ is diagonal.
2. $\Lambda$ is constrained to be block-diagonal or lower-triangular with positive diagonal elements.
3. **Sign Anchor**: The factor loading of known stress barometers is constrained to be strictly positive:
   $$\lambda_{\text{VIX}} > 0, \quad \lambda_{\text{ACLED\_fatalities}} > 0$$
This guarantees that an increase in $S_t$ always signifies an increase in systemic stress, preserving interpretation across all 3,650+ rolling origins.

### 8.2 Dynamic Global Risk State (DGRS)
The common scalar systemic pressure factor $F_t$ satisfies:
$$Y_t = \Lambda F_t + \varepsilon_t, \quad F_t = \rho F_{t-1} + u_t, \quad u_t \sim \mathcal{N}(0, \sigma_u^2)$$
with $\rho \in (-1, 1)$ regularized via a Beta-transformed prior.

---

## 9. Empirical Design & Outcome Architecture

### 9.1 Unit of Analysis & Timeframe
* **Unit**: Global-day observation $(t)$.
* **Sample Period**: 2015-01-01 to present (frozen historical test window).
* **Horizons**: $h \in \{1, 3, 7, 14\}$ calendar days ahead.

### 9.2 Outcome Targets
1. **Binary Systemic Episode ($Y_t^{(h)}$)**:
   $$Y_t^{(h)} = \mathbb{I}(S_{t+h} \ge q_{0.90})$$
   where $q_{0.90}$ is frozen from training-window data.
2. **Continuous Systemic Volatility ($\Delta S_t^{(h)}$)**:
   $$\Delta S_t^{(h)} = S_{t+h} - S_t$$
   evaluated using Continuous Ranked Probability Score (CRPS).
3. **Multi-Domain Escalation ($S_3$)**:
   $$Y_{\text{multi},t}^{(h)} = \mathbb{I}\left(\sum_{d=1}^5 \mathbb{I}(R_{d,t+h} \ge c_d) \ge 3\right)$$
   representing simultaneous threshold breaches across at least 3 independent domains.

---

## 10. Data Architecture & Point-in-Time Hygiene

### 10.1 High-Frequency Domain Indicators & Macro Proxies

| Domain | Primary Source | Daily Indicator / Market-Implied Proxy | Role in 4D Framework |
|---|---|---|---|
| **Geopolitics** | GDELT & ACLED | CAMEO QuadClass Conflict events, Fatalities, Protests | Physical & rhetorical geopolitical tension |
| **Economics** | FRED / Treasury | 10Y-2Y Yield Curve Slope, 5y5y Inflation Breakeven (`T5YIFR`) | Real-time high-frequency macro state |
| **Finance** | CBOE / ICE BofA | VIX Index, High Yield OAS (`BAMLH0A0HYM2`), FX Volatility | Systemic financial and liquidity stress |
| **Energy** | Commodities | Brent / WTI Daily Return Volatility, Natural Gas spreads | Commodity supply-shock transmission |
| **Technology/AI** | Curated Corpus | AI incident volume, Frontier release velocity, Chip export alerts | Technological disruption signals |
| **Information** | GDELT 2.0 | Salience-Normalized Information Velocity ($\widetilde{IV}_t$) | Narrative amplification and social velocity |
| **Climate** | NOAA / Copernicus | Global surface temperature anomaly, extreme weather index | Physical environmental baseline stress |

### 10.2 Vintage Control & Leakage Firewall
For every data record $x$:
$$\text{Eligible at origin } t \iff \text{first\_available\_timestamp}(x) \le t$$
All macroeconomic indicators that undergo retrospective revisions (e.g., IMF WEO, GDP prints) must be loaded using their **historical point-in-time release vintages**. Current revised values are strictly prohibited.

---

## 11. Origin-Safe Feature Engineering & Salience Normalization

### 11.1 Salience-Normalized Information Velocity
To prevent raw wire-service syndication cascades from masquerading as physical conflict surges:
$$\widetilde{IV}_{d,t} = \frac{\text{Salience}_{d,t} - \text{median}(\text{Salience}_{d, t-L:t-1})}{\text{MAD}(\text{Salience}_{d, t-L:t-1}) + \varepsilon}$$
where:
$$\text{Salience}_{d,t} = \frac{N_{d,t}}{\text{TotalGlobalArticles}_t}$$
Filtering is restricted to **CAMEO QuadClass Material Conflict** with **Goldstein Conflict Scale $\le -5.0$**.

### 11.2 Origin-Safe Standardizers
All rolling transformations are computed strictly within training history:
$$Z_{j,t} = \frac{X_{j,t} - \mu_{j,\text{train}}}{\sigma_{j,\text{train}}}$$
Global-sample normalization prior to rolling evaluation is prohibited.

---

## 12. Model Hierarchy and Benchmarks (M0 to M7)

To ensure that complexity is quantitatively justified:
* **M0 (Persistence)**: $\hat{p}_{t+h} = Y_t$
* **M1 (Climatology)**: $P(Y=1) = \bar{Y}_{\text{train}}$
* **M2 (Single-Domain Logistic)**: Separate univariate models per domain: $\text{logit}(p_t) = \beta_0 + \beta_d^T X_{d,t}$
* **M3 (Multidisciplinary ElasticNet)**: Pooled $L_1/L_2$ regularized logistic model
* **M4 (Dynamic Autoregressive)**: Autoregressive outcome lags + domain indicators
* **M5 (Nonlinear ML)**: LightGBM / Gradient Boosted Decision Trees with early stopping
* **M6 (Dynamic Bayesian TVP)**: Time-varying parameter model with random walk slopes
* **M7 (Full 4D Model)**: Joint State + Interaction + Propagation + Horizon Model

---

## 13. Dynamic Bayesian & State-Space Inference Architecture (Two-Tier Protocol)

To eliminate the computational barrier of running 3,650+ daily MCMC chains while maintaining full Bayesian rigor:

```
[ Daily Rolling Origins (t = 1..3,650) ]
        │
        ▼ (Fast Analytical Inference)
[ Tier 1: Dynamic Linear Model (DLM) ]
  • Kalman Filter & Fixed-Interval Smoother (Carter-Kohn)
  • State estimation in < 50ms per origin
  • Zero MCMC convergence failures in rolling loop
        │
        ▼ (Quarterly Checkpoint Origins & Stress Windows)
[ Tier 2: Checkpoint Bayesian MCMC (NUTS in PyMC) ]
  • Full posterior sampling across 4 chains (2,000 warmup, 2,000 draws)
  • Hierarchical shrinkage priors (Horseshoe / HalfNormal)
  • Validation of Tier 1 Kalman state approximations (KL-divergence test)
```

---

## 14. Model Validation & Diagnostic Hierarchy
1. **Prior Predictive Checks**: Sample priors to confirm implied event rates and variance boundaries fall within scientifically plausible limits.
2. **Posterior Predictive Checks**: Validate that simulated trajectories replicate observed volatility clustering and autocorrelation.
3. **MCMC Convergence Standards**: Enforce $\hat{R} < 1.05$, Effective Sample Size $\text{ESS} > 400$, and zero divergent transitions for all Tier 2 runs.
4. **Kalman Innovation Diagnostics**: Verify innovation residuals $v_t = X_t - \hat{X}_{t \mid t-1}$ exhibit zero serial correlation via Ljung-Box tests.

---

## 15. Cross-Domain Propagation Analysis
Estimates whether source domain $j$ provides incremental out-of-sample skill for target domain $i$:
$$S_{i,t+h} = \alpha_{i,h} + \sum_{k=1}^K \beta_{ij,h,k} S_{j,t-k} + \theta_{i,h}^T X_t + \varepsilon_{i,t+h}$$
The primary propagation metric is:
$$\Delta \text{Skill}_{ij,h} = \text{Skill}(\text{Model}_{i \leftarrow j}) - \text{Skill}(\text{Model}_i)$$
Negative control placebo tests (e.g., shuffling lag structures or testing theoretically impossible pathways) must yield $\Delta \text{Skill} \approx 0$.

---

## 16. Operationalized Scenario & Early-Warning Dynamics
Scenarios are operationalized as a multinomial categorical variable $S_t \in \{1, 2, 3\}$:
* **$S_1$ — Managed Volatility**: Elevated background stress without multi-domain cascades.
* **$S_2$ — Signal Shock**: Isolated acute threshold breach in 1 or 2 domains.
* **$S_3$ — Multi-Domain Escalation**: Simultaneous breach in $\ge 3$ domains.

Outputs include:
1. **Time-Evolving Trajectory**: $P(S_k, t+1), P(S_k, t+3), P(S_k, t+7), P(S_k, t+14)$.
2. **$3 \times 3$ Markov Transition Matrix**: $P(S_{t+1} = j \mid S_t = i, \mathcal{D}_t)$.
3. **Early-Warning Indicator Sensitivity**:
   $$EW_j(h) = \frac{\partial P(S_{t+h} = \text{Escalation})}{\partial X_{j,t}}$$

---

## 17. Rolling-Origin Out-of-Sample Evaluation Protocol
* **Expanding Window**:
  $$\text{Train}_t = [t_{\text{start}}, t], \quad \text{Predict} = t+h$$
* **Zero Leakage**: All normalizations, feature selectors, and calibrations are fitted exclusively on $\text{Train}_t$.
* **Realization Evaluation**: Outcomes are evaluated only after $t+h$ has elapsed.

---

## 18. Forecast Verification & Rare-Event Scoring Hygiene

To prevent the "Climatology Illusion" where naive base-rate predictors game proper scoring on rare events ($S_3 < 1.5\%$ of days):

1. **Brier Score (BS)**:
   $$\text{BS} = \frac{1}{N} \sum_{t=1}^N (p_t - y_t)^2$$
2. **Brier Skill Score (BSS)**:
   $$\text{BSS} = 1 - \frac{\text{BS}_{\text{model}}}{\text{BS}_{\text{climatology}}}$$
   *$\text{BSS} \le 0$ indicates zero skill beyond the historical base rate.*
3. **Precision-Recall AUC (PR-AUC)**: Mandatory over ROC-AUC for evaluating rare multi-domain escalation events.
4. **Logarithmic Score (Cross-Entropy)**: $-\frac{1}{N} \sum_t [y_t \ln p_t + (1 - y_t) \ln(1 - p_t)]$.
5. **Expected Calibration Error (ECE)** & Reliability Curves across 10 probability bins.

---

## 19. Dynamic Calibration Procedure
Probabilities undergo out-of-sample calibration via:
* Platt Logistic Recalibration;
* Dynamic Conformal Calibration (Oancea 2026);
* Tail-calibrated scaling (Wessel et al. 2026).
Both raw and calibrated probabilities must be reported to disentangle model discrimination from post-hoc correction.

---

## 20. Forecast Comparison and Statistical Testing
* **Loss Differential**: $d_t = L(e_{1,t}) - L(e_{2,t})$.
* **Diebold-Mariano Test**: Heteroskedasticity and Autocorrelation Consistent (HAC) adjusted to account for $h$-step serial correlation.
* **Block Bootstrap**: Stationary block bootstrap for dependent time-series confidence intervals.
* **Primary Comparison**: M7 (Full 4D Model) vs. the best non-4D benchmark (M5 or M3).

---

## 21. Ablation Analysis
Quantifies the marginal value of each component:
$$\text{Contribution}_d = \text{Score}(\text{Model}_{-d}) - \text{Score}(\text{Model}_{\text{full}})$$
Evaluated across all 5 domains, interaction terms ($A_t$), propagation lags ($\Pi_h$), and dynamic latent states ($F_t$).

---

## 22. Crisis, Regime, and Structural-Break Analysis
The framework is evaluated separately across:
* Normal operational periods;
* Acute geopolitical flare-ups;
* Financial volatility spikes (e.g., 2020 market shock, 2022 rate surge);
* Large climate/environmental anomalies.
Tests whether model parameters and calibration degrade under severe regime shift.

---

## 23. Distribution-Shift and Robustness Test Suite
1. Alternative event thresholds (80th, 90th, 95th percentiles).
2. Alternative training windows (expanding vs. 3-year fixed rolling).
3. Data source substitutions.
4. Strict publication-delay buffers (+24h, +48h).
5. Prior sensitivity analysis in Tier 2 MCMC.
6. Crisis-exclusion vs. Crisis-only testing.
7. Negative-control placebo propagation pathways.

---

## 24. Forecast Updating and Vintage Archive
Every forecast record is immutably archived with:
`forecast_id`, `forecast_origin`, `horizon`, `model_version`, `dataset_version`, `raw_probability`, `calibrated_probability`, `realized_outcome`, `brier_score`, `random_seed`.

---

## 25. Causal Demarcation, Statistical Reporting & Decision Utility

### 25.1 Causal Demarcation
Predictive association does not imply structural causation. Language like *"Geopolitical stress causes market decline"* is forbidden. Approved language: *"Geopolitical event intensity carries statistically significant incremental predictive skill for subsequent financial volatility."*

### 25.2 Decision-Theoretic Policy Utility Layer
To demonstrate real-world operational value to policymakers and risk managers, models are evaluated under the **Richardson / Murphy-Winkler Relative Value Score ($V$)**:
$$V(\alpha) = \frac{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{model}}(\alpha)}{\text{Expense}_{\text{climatology}}(\alpha) - \text{Expense}_{\text{perfect}}(\alpha)}$$
across a spectrum of cost-loss ratios ($\alpha = C/L$, cost of proactive mitigation vs. loss from an unmitigated systemic shock). A model is operationally valuable only if $V(\alpha) > 0$.

---

## 26. Contemporary Information Environment
Captures the multi-domain interaction observable in modern global affairs (e.g., energy market sensitivity to Middle Eastern chokepoints, AI infrastructure power constraints, sovereign debt dynamics). Treated strictly as qualitative motivation, never empirical proof.

---

## 27. Data Quality Risks and Limitations
Transparently documents:
* GDELT scraper changes, translation imbalances, and Western media concentration;
* ACLED reporting lags and localized verification delays;
* Implied market proxy noise (risk premia vs. true physical risk);
* Structural unobservability of covert statecraft and surprise events.

---

## 28. Preregistered Falsification Criteria

The 4D framework is formally declared **unsupported** if any of the following occur under preregistered tests:
1. M7 fails to achieve a statistically superior Brier Skill Score ($\text{BSS} > 0$) over M1 (Climatology) and M5 (LightGBM).
2. Propagation matrices ($\Pi_h$) add zero out-of-sample skill over non-propagating static models.
3. Latent state ($F_t$) provides no incremental predictive value over raw predictors.
4. Out-of-sample probabilities display uncorrectable miscalibration ($\text{ECE} > 0.15$).
5. Predictive relationships evaporate under independent data source substitution.
6. Results rely entirely on a single data source (e.g., GDELT alone).
7. Strict publication-delay buffers eliminate all apparent predictive power.
8. The model performs solely during historical crises and fails in normal periods (overfitting crises).
9. Domain ablations reveal zero marginal contribution from 3 or more domains.
10. The Relative Value Score $V(\alpha) \le 0$ across all operational cost-loss ratios.

*A null result on any criterion is a valid, publishable scientific contribution.*

---

## 29. Preregistration Requirements
All outcome thresholds, candidate predictors, source vintages, prior distributions, model hierarchies, and scoring metrics are frozen prior to final test-window execution.

---

## 30. Reproducible Computational Architecture
Layout structured under `4d-global-risk/` adhering to the complete repository blueprint (§30.1).

---

## 31. Algorithmic Pipeline & Execution Logic
```python
for origin in rolling_forecast_origins:
    data_t = load_point_in_time_data(cutoff=origin)
    features_t = compute_origin_safe_features(data_t)
    
    # Tier 1 Fast Analytical Inference
    dgrs_state_t = fit_kalman_dgrs(features_t, sign_anchor="VIX > 0")
    
    for h in [1, 3, 7, 14]:
        forecasts_h = generate_probabilistic_forecasts(dgrs_state_t, horizon=h)
        archive_forecast_record(forecasts_h, origin, h)
        
    # Tier 2 Periodic Checkpoint MCMC Validation
    if is_quarterly_checkpoint(origin):
        run_nuts_mcmc_validation(features_t, dgrs_state_t)

# Once horizons elapse
score_all_forecasts(metrics=["BSS", "LogScore", "CRPS", "ECE", "ValueScore"])
execute_falsification_tests()
```

---

## 32. Immediate Empirical Execution Plan
Phases A through I: Ingestion $\rightarrow$ Provenance Verification $\rightarrow$ Feature Engineering $\rightarrow$ State Estimation $\rightarrow$ Forecasting $\rightarrow$ Verification $\rightarrow$ Propagation $\rightarrow$ Robustness $\rightarrow$ Automated Dissertation Artifact Export.

---

## 33. Tables and Figures to Be Produced
Automated export of Tables 1–10 (LaTeX/Markdown) and Figures 1–20 (High-res PDF/PNG) from frozen model outputs.

---

## 34. Empirical Results Chapter Template
Structured reporting of Descriptive Findings, Latent State Trajectories, Model Benchmark Ladder, Calibration Curves, Propagation Matrices, Scenario Dynamics, Ablations, and Robustness Findings.

---

## 35. Dissertation Chapter Structure
1. Introduction
2. Literature Review
3. Four-Dimensional Theoretical Framework
4. Data Architecture & Point-in-Time Hygiene
5. Methodology & Two-Tier Inference Architecture
6. Empirical Forecasting Results & Model Ladder
7. Cross-Domain Dynamic Propagation
8. Operationalized Scenario & Early-Warning Analysis
9. Robustness, Placebo & Falsification Results
10. Discussion & Practical Decision Utility
11. Conclusion & Scientific Limits

---

## 36. Expected Scientific & Practical Decision Contribution
1. **Theoretical**: Formalization of global risk as an interconnected 4D dynamic system.
2. **Methodological**: Development of the Two-Tier Kalman/MCMC inference engine and sign-anchored factor estimation.
3. **Empirical**: First rigorous, point-in-time, multi-horizon benchmark test of multidisciplinary risk propagation.
4. **Decision Utility**: Operational translation of calibrated probabilities into quantified risk-mitigation value ($V$).

---

## 37. Conceptual Priors Versus Empirical Posteriors
Conceptual percentages from early qualitative frameworks are classified strictly as Layer 1 benchmark priors. Final dissertation figures must derive exclusively from empirical posterior outputs.

---

## 38. Dissertation Readiness Gate
All 32 pre-flight checkboxes (Conceptual, Data, Modelling, Validation, Robustness, Reproducibility) must pass before submission.

---

## 39. References
Complete bibliography spanning time-series econometrics (Hamilton, Box-Jenkins), probabilistic verification (Gneiting, Brier, Murphy), Bayesian computation (Gelman, McElreath), systems theory (Meadows), and contemporary 2026 conformal calibration literature (Wessel et al., Oancea, Li et al.).

---

## 40. Final Methodological Statement
The dissertation does not claim success because its conceptual architecture is elegant. Its scientific contribution rests entirely on whether the 4D framework demonstrates reproducible, out-of-sample, properly calibrated predictive value over strong, simpler benchmarks while surviving strict falsification testing.

---

## 41. Proposed Research Identity
* **Framework**: 4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)
* **Latent State**: Dynamic Global Risk State (DGRS)
* **Inference**: Two-Tier Kalman-MCMC Protocol
* **Core Metric**: Brier Skill Score (BSS) & Relative Decision Value ($V$)
* **Horizons**: 1, 3, 7, and 14 Days
