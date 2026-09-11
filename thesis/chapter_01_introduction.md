# Chapter 1: Introduction

---

## 1.1 The Poly-Crisis Era & The Limits of Single-Domain Forecasting

The international system in the mid-2020s is characterized by what historians and social scientists describe as a "poly-crisis": an interconnected matrix of geopolitical friction, macro-financial tightening, technological disruption, hyper-speed information flows, and accelerating climatic anomalies (Tooze 2022). In this environment, systemic risks do not respect traditional academic jurisdictions. A naval skirmish near an energy chokepoint instantaneously ripples into sovereign bond yields, commodity derivatives, domestic food inflation, social polarization, and national electoral volatility.

Despite this evident interconnectedness, the dominant paradigms in predictive risk analysis remain deeply fragmented:
1. **Institutional Horizon Scanning**: Elite forums rely on Delphi surveys, qualitative risk matrices, and thematic narratives. These provide intuitive conceptual vocabulary but produce zero calibrated probabilities, cannot be subjected to out-of-sample statistical verification, and frequently succumb to recency bias.
2. **Disciplinary Econometrics**: Quantitative forecasting models are predominantly univariate or single-domain. Macroeconomists build vector autoregressions that omit digital information velocity and conflict telemetry; political scientists track local protest violence without integrating high-frequency financial or commodity feedback.
3. **Black-Box Predictive AI**: Contemporary deep learning algorithms often achieve high uncalibrated accuracy on historical benchmarks, but they operate as uninterpretable black boxes, fail to quantify epistemic parameter uncertainty, and deteriorate rapidly when underlying regimes shift.

This dissertation addresses these structural shortcomings by developing, mathematically formalizing, and empirically verifying the **4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)**.

---

## 1.2 Central Scientific Question

The overarching research question of this dissertation is:
> *Given the multidisciplinary information set $\mathcal{I}_t$ available at forecast origin $t$, what is the joint probability distribution over near-term global-risk states and discrete escalation events at horizon $t+h$, how do localized disturbances propagate across domains, and how well-calibrated are those predictive distributions under strict out-of-sample evaluation?*

---

## 1.3 The Four Core Dimensions of the Framework

The dissertation formalizes global risk as a dynamic multidimensional system across four coupled dimensions:
* **Dimension 1 — State ($S_t$)**: Global stress is represented as a latent multidimensional state across five core domains: Geopolitics ($G$), Economics/Finance ($E$), Technology/AI ($T$), Information/Society ($I$), and Climate/Environment ($C$). Common systemic pressure is extracted via a sign-anchored **Dynamic Global Risk State (DGRS)** latent factor model ($F_t$).
* **Dimension 2 — Interaction ($A_t$)**: Domains are structurally coupled through a dynamic, time-varying transmission matrix regularized with hierarchical shrinkage priors.
* **Dimension 3 — Propagation ($\Pi_h$)**: Disturbances transmit through multi-step network pathways over lag $k$, summarized in a horizon-dependent propagation matrix $\Pi_h$.
* **Dimension 4 — Time ($t+h$)**: Relationships and predictive distributions are indexed by time under expanding rolling-origin evaluations across horizons $h \in \{1, 3, 7, 14\}$ days.

---

## 1.4 Research Aim & Specific Objectives

**Aim**: To develop, mathematically formalize, estimate, and out-of-sample validate a four-dimensional probabilistic framework for near-term multidisciplinary global-risk forecasting.

**Specific Objectives**:
1. **Data Architecture**: Construct a point-in-time relational data pipeline enforcing zero lookahead leakage ($I_t = \{x : \text{first\_available}(x) \le t\}$).
2. **Identification & Computation**: Establish a sign-anchored state-space formulation ($\lambda_{\text{stress}} > 0$) and a computationally tractable **Two-Tier Inference Protocol** (daily analytical Kalman RTS smoother + quarterly checkpoint Bayesian MCMC).
3. **Model Benchmark Ladder**: Implement and evaluate an escalating benchmark ladder: M0 (Persistence), M1 (Climatology), M2 (Single-Domain), M3 (ElasticNet), M4 (Dynamic AR), M5 (LightGBM), and M7 (Full 4D Model).
4. **Proper Scoring Verification**: Evaluate forecasts using strictly proper scoring rules (Brier Score, Brier Skill Score against climatology, Logarithmic Score) and Precision-Recall AUC for rare crisis events.
5. **Decision Utility**: Operationalize the Richardson / Murphy-Winkler Relative Value Score ($V(\alpha)$) to quantify real-world economic risk-mitigation value under varying cost-loss ratios.
6. **Preregistered Falsification**: Test the framework against 10 explicit falsification criteria, ensuring that null results are preserved as valid scientific findings.

---

## 1.5 Dissertation Organization

The dissertation is structured into 11 chapters:
* **Chapter 1: Introduction**: Motivates the research problem, states core questions, and outlines objectives.
* **Chapter 2: Literature Review**: Surveys probabilistic forecasting, Bayesian time-series econometrics, complex dynamic systems, and multidisciplinary risk paradigms.
* **Chapter 3: Theoretical Framework**: Formalizes the 4D conceptual model, state-space equations, and the six-layer evidentiary hierarchy.
* **Chapter 4: Data Architecture & Measurement**: Details point-in-time provenance, high-frequency FRED macro proxies, salience-normalized GDELT velocity, and leakage controls.
* **Chapter 5: Methodology**: Details the sign-identification proof, Two-Tier inference engine, model ladder (M0–M7), and verification metrics.
* **Chapter 6: Empirical Results**: Analyzes the latent DGRS trajectory, out-of-sample model benchmark ladder, and dynamic propagation matrices.
* **Chapter 7: Dynamic Propagation**: Dissects multi-step cross-domain transmission channels and impulse attenuation.
* **Chapter 8: Operationalized Scenarios**: Translates predictive densities into multinomial scenario probabilities ($S_1, S_2, S_3$) and early-warning sensitivities.
* **Chapter 9: Robustness & Falsification**: Evaluates model resilience under regime shifts, crisis exclusion, and tests the 10 falsification criteria.
* **Chapter 10: Discussion & Practical Utility**: Translates probabilistic findings into operational risk-management decisions.
* **Chapter 11: Conclusion**: Summarizes core findings, acknowledges scientific limitations, and outlines future research trajectories.
