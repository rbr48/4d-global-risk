# Chapter 2: Literature Review

---

## 2.1 The Evolution of Global Risk Conceptualization

For decades, the study of global risk has developed along two largely non-intersecting intellectual traditions: institutional horizon scanning and disciplinary quantitative econometrics. 

Institutional risk analysis—epitomized by the annual *Global Risks Report* published by the World Economic Forum (WEF)—emerged from the strategic planning traditions of royal Dutch Shell in the 1970s (Wack 1985). This paradigm relies on multistakeholder perception surveys, Delphi consensus methods, and qualitative scenario planning. While successful in establishing a shared vocabulary for systemic vulnerabilities, this approach exhibits severe epistemological limitations. As Tetlock and Gardner (2015) demonstrate, unstructured expert consensus frequently underperforms naive statistical baselines due to overconfidence, hindsight bias, and narrative availability cascades (Kahneman 2011). Crucially, survey-based risk matrices produce ordinal severity-likelihood scores that cannot be validated out-of-sample or calibrated against real-world frequency distributions.

In contrast, quantitative risk modelling has evolved within narrow disciplinary boundaries:
* **Macroeconomic & Financial Risk**: Econometricians focus on Vector Autoregressions (VARs), Structural VARs, and Dynamic Stochastic General Equilibrium (DSGE) models (Hamilton 1994; Box et al. 2015). In finance, systemic risk measurement focuses on co-dependence structures in market returns, such as CoVaR (Adrian & Brunnermeier 2016) and Marginal Expected Shortfall (Acharya et al. 2017). While mathematically rigorous, these models treat geopolitical shocks, social unrest, and technological ruptures as unmodeled exogenous residual disturbances.
* **Political Violence & Geopolitical Telemetry**: Quantitative political science has transitioned from static conflict databases toward high-frequency event monitoring, notably through the Armed Conflict Location & Event Data Project (ACLED) and the Global Database of Events, Language, and Tone (GDELT) (Leetaru & Schrodt 2013). Systems like ACLED’s Conflict Alert System (CAST) use rolling time-series techniques to anticipate localized violence. However, these systems rarely incorporate macro-financial feedback loops, sovereign debt stress, or global commodity markets.
* **Complex Adaptive Systems**: A third literature rooted in cybernetics and systems dynamics (Meadows 2008; Castells 1996) conceptualizes global society as a dense network of feedback loops where localized perturbations trigger nonlinear cascades (Taleb 2007). Yet, systems literature has often remained descriptive or simulation-based, lacking formal empirical verification under strict out-of-sample scoring rules.

This dissertation bridges these disparate fields by formalizing a dynamic, multidisciplinary system that integrates high-frequency conflict telemetry, macro-financial barometers, digital media velocity, and environmental anomalies under a unified probabilistic architecture.

---

## 2.2 Probabilistic Forecasting & Verification Science

Forecasting in complex, open systems cannot generate deterministic point predictions. Modern forecasting science therefore requires **probabilistic forecasting**, where the forecast target is a full probability distribution over future states (Gneiting 2011).

### Strictly Proper Scoring Rules
A foundational principle established by Brier (1950), Murphy (1973), and generalized by Gneiting and Raftery (2007) is that probability forecasts must be evaluated using **strictly proper scoring rules**. A scoring rule assigns a numerical penalty $S(P, y)$ to a predictive distribution $P$ when outcome $y$ materializes. It is strictly proper if and only if:
$$\mathbb{E}_{y \sim Q}[S(P, y)] \ge \mathbb{E}_{y \sim Q}[S(Q, y)]$$
with equality holding if and only if $P = Q$. Proper scoring rules eliminate incentives for forecasters to hedge, distort, or overstate certainty.

The dissertation relies on three primary proper scoring rules:
1. **The Brier Score (BS)**:
   $$\text{BS} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2$$
   Murphy (1973) showed that the Brier score decomposes orthogonally into $\text{BS} = \text{Reliability} - \text{Resolution} + \text{Uncertainty}$.
2. **The Brier Skill Score (BSS)**:
   $$\text{BSS} = 1 - \frac{\text{BS}_{\text{model}}}{\text{BS}_{\text{reference}}}$$
   Mandatory in rare-event settings to prevent trivial base-rate predictors from gaming raw loss.
3. **Continuous Ranked Probability Score (CRPS)**:
   $$\text{CRPS}(F, y) = \int_{-\infty}^{\infty} \big(F(z) - \mathbb{I}\{z \ge y\}\big)^2 dz$$
   Used for verifying continuous systemic volatility trajectories $\Delta S_t^{(h)}$.

### Probability Calibration vs. Discrimination
Gneiting, Balabdaoui, and Raftery (2007) formalized the goal of probabilistic forecasting as **maximizing sharpness subject to calibration**:
* **Calibration (Reliability)**: The statistical consistency between forecast probabilities and observed empirical event frequencies. If an event is forecast with probability $p=0.70$, it must occur 70% of the time across a large collection of independent trials.
* **Sharpness**: The concentration of the predictive distribution. A forecast that always issues the historical base rate (e.g., $p=0.15$) is perfectly calibrated but exhibits zero sharpness.

Recent methodological advances have highlighted that under regime change, calibration degrades rapidly. Wessel et al. (2026) emphasize the necessity of enforcing tail calibration during model training, while Oancea (2026) and Li, Koa, and Huang (2026) introduce dynamic conformal prediction and sample-cloud ellipsoids to maintain valid predictive coverage under multiple distribution shifts.

---

## 2.3 Bayesian Time-Varying State-Space Econometrics

To model evolving global relationships without assuming fixed parameters, the econometric literature has increasingly adopted **State-Space Models** and **Time-Varying Parameter Vector Autoregressions (TVP-VARs)** (Hamilton 1994; Primiceri 2005; Gelman et al. 2013).

In a Bayesian dynamic linear model, unobserved states evolve via Markovian transition equations. However, scaling dynamic Bayesian models to high-dimensional multidisciplinary panels encounters the **curse of dimensionality**: an unconstrained 5-domain TVP model with 3 lags contains hundreds of drifting coefficients. 

To prevent catastrophic overfitting, recent Bayesian literature relies on **hierarchical shrinkage priors**, such as the Horseshoe prior (Carvalho, Polson & Scott 2010), spike-and-slab priors, and Dirichlet-Laplace shrinkage. These priors exert severe shrinkage on noise terms while leaving large structural signals unpenalized. Furthermore, Carter and Kohn (1994) developed the forward-filtering backward-sampling algorithm that makes state extraction computationally tractable.

This dissertation builds upon this foundation by introducing a **Two-Tier Inference Architecture** that pairs lightning-fast analytical Kalman smoothing for daily rolling updates with quarterly checkpoint Markov Chain Monte Carlo (MCMC) sampling.

---

## 2.4 Gaps in the Literature & Scientific Contribution

Despite substantial progress across these distinct disciplines, four critical gaps remain:
1. **The Disciplinary Divide**: No existing framework provides a continuous, daily, point-in-time probabilistic architecture uniting conflict telemetry, macro-financial indicators, digital media velocity, and climate anomalies.
2. **The Lookahead Leakage Vulnerability**: Existing quantitative studies routinely utilize retrospective revisions (e.g., modern IMF data) or global-sample preprocessing, artificially inflating historical forecast performance.
3. **The Rare-Event Climatology Blindspot**: Evaluations in political forecasting frequently rely on ROC-AUC or raw accuracy, which are completely blind to severe probability miscalibration during low-base-rate crises.
4. **Lack of Preregistered Falsification**: Quantitative social science rarely preregisters explicit falsification criteria, creating severe confirmation bias where negative or null findings are buried.

This dissertation directly fills these gaps by providing an empirically verified, point-in-time, preregistered four-dimensional forecasting architecture.
