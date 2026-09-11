# Chapter 3: The Four-Dimensional Theoretical Framework

---

## 3.1 Introduction to Multidisciplinary Global Risk

Contemporary global risk analysis has historically oscillated between two unsatisfactory extremes. On one hand, qualitative horizon scanning—typified by institutional reports such as the World Economic Forum's *Global Risks Report*—synthesizes expert stakeholder perception into descriptive network diagrams and ordinal severity rankings. While valuable for broad agenda-setting, these qualitative frameworks lack explicit mathematical formalization, do not generate testable out-of-sample probabilistic forecasts, and are prone to cognitive availability cascades and narrative bias (Kahneman 2011; Tetlock & Gardner 2015).

On the other hand, quantitative forecasting has predominantly evolved in strict disciplinary silos. Macroeconometricians estimate structural vector autoregressions (SVARs) or dynamic stochastic general equilibrium (DSGE) models restricted to output, interest rates, and inflation (Hamilton 1994); quantitative finance focuses on localized option-implied volatility surfaces and credit default spreads; computational political scientists construct conflict event-count monitors (e.g., ACLED CAST); and climatologists develop physical Earth-system simulations.

However, historical crisis episodes demonstrate that catastrophic systemic disruptions are fundamentally multidisciplinary and dynamic. A localized geopolitical shock (such as maritime interdiction in energy chokepoints) transmits directly into commodity volatility; energy spikes alter forward inflation expectations and sovereign yield spreads; credit tightness constrains fiscal policy; information velocity across digital networks amplifies narrative contagion; and underlying environmental stress exacerbates localized conflict vulnerability.

To capture these interconnected dynamics without succumbing to ungrounded qualitative prophecy, this dissertation introduces the **4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)**. The framework conceptualizes global risk as an evolving dynamic system defined across four coupled dimensions: **State**, **Interaction**, **Propagation**, and **Time**.

---

## 3.2 Dimension 1: The Latent Systemic State ($S_t$)

The first dimension defines the condition of the global system at discrete time $t$ across $D = 5$ core domains:
$$S_t = \big(S_{G,t}, S_{E,t}, S_{T,t}, S_{I,t}, S_{C,t}\big)^T \in \mathbb{R}^D$$
where:
* $S_{G,t}$: Geopolitical stress (diplomatic friction, kinetic conflict intensity, regional territorial dispute severity);
* $S_{E,t}$: Economic and financial pressure (credit spreads, monetary conditions, commodity volatility);
* $S_{T,t}$: Technological and AI disruption (cybersecurity incidents, critical infrastructure friction, compute policy restrictions);
* $S_{I,t}$: Information and societal stress (narrative velocity, media polarization, coordinated digital information operations);
* $S_{C,t}$: Climatic and environmental anomalies (extreme weather occurrences, biosphere indicators).

### The Latent Factor Formulation: Dynamic Global Risk State (DGRS)
Crucially, $S_t$ is not directly observable through any single instrument. Relying on a single metric—such as using raw news headlines to measure geopolitics or stock indices to measure economics—introduces fatal measurement error and source-specific bias. 

The framework formulates the observable high-frequency indicator vector $X_t \in \mathbb{R}^p$ ($p \gg D$) as a noisy measurement of underlying latent states:
$$X_t = \Lambda S_t + \varepsilon_t, \quad \varepsilon_t \sim \mathcal{N}(0, \Psi)$$
where $\Lambda \in \mathbb{R}^{p \times D}$ is the factor loading matrix, and $\Psi = \text{diag}(\sigma_1^2, \dots, \sigma_p^2)$ represents idiosyncratic measurement noise.

To capture broad common pressure across the entire international system, the framework identifies a central scalar factor—the **Dynamic Global Risk State (DGRS)**, denoted $F_t$:
$$X_t = \lambda F_t + e_t, \quad F_t = \rho F_{t-1} + u_t, \quad u_t \sim \mathcal{N}(0, \sigma_u^2)$$
where $\rho \in (-1, 1)$ reflects systemic persistence. The DGRS does not imply that all global risks are identical; rather, it formalizes the empirical reality that during systemic crises, covariance across disparate domains rises sharply.

---

## 3.3 Dimension 2: Dynamic Cross-Domain Interaction ($A_t$)

The domains in $S_t$ do not evolve independently. The second dimension models time-varying interdependence:
$$S_t = A_t S_{t-1} + B_t X_t + \eta_t, \quad \eta_t \sim \mathcal{N}(0, Q)$$
where $A_t \in \mathbb{R}^{D \times D}$ is the dynamic interaction matrix. The element $a_{ij,t}$ represents the predictive transmission strength from domain $j$ to domain $i$ at time $t$.

### Parameter Evolution & Shrinkage
Because global relationships are non-stationary, $A_t$ cannot be assumed constant across decade-long samples. The interaction parameters evolve as a multivariate random walk:
$$a_{ij,t} = a_{ij,t-1} + \nu_{ij,t}, \quad \nu_{ij,t} \sim \mathcal{N}(0, \tau_{ij}^2)$$
To prevent parameter proliferation and over-fitting, the variance parameters $\tau_{ij}^2$ are governed by hierarchical shrinkage priors:
$$\tau_{ij} \sim \text{Half-Cauchy}(0, \sigma_{\tau})$$
This shrinks unstable or spurious cross-domain correlations toward zero while permitting persistent structural relationships to be estimated from data.

> **Implementation Note on Dimensional Reduction**: The full $D \times D$ interaction matrix $A_t$ represents the theoretically complete specification. In the implemented empirical system, the computational intractability of estimating $D^2$ time-varying parameters across rolling origins motivates a rank-one approximation: the Dynamic Global Risk State (DGRS, §3.2) extracts a single scalar common factor $F_t$ ($m = 1$), with cross-domain interaction captured implicitly through the indicator loadings $\Lambda \in \mathbb{R}^{p \times 1}$. The empirical propagation matrix $\Pi_h$ (§3.4) then recovers pairwise lead-lag transmission directly from the observed indicator panel. This rank-one factorization is a standard econometric simplification (Stock & Watson 2002) that preserves the essential co-movement structure while avoiding the curse of dimensionality. Extension to a multi-factor state vector ($m > 1$) with explicit $A_t$ estimation is identified as future work (§11.4).

---

## 3.4 Dimension 3: Multi-Step Dynamic Propagation ($\Pi_h$)

While *Interaction* describes contemporaneous and one-step dependencies, **Propagation** models the transmission of localized shocks through multi-step network chains over lag $k$.

Consider an exogenous shock vector $U_t$ entering domain $j$ at time $t$. The $h$-step impulse propagation across the interconnected system is formalized as:
$$P_{t,h} = \left(\prod_{m=0}^{h-1} A_{t+h-m}\right) B_t U_t$$

### The Propagation Matrix $\Pi_h$
To make propagation empirically testable, the framework defines the horizon-specific propagation matrix:
$$\Pi_h = [\pi_{ij,h}] \in \mathbb{R}^{p \times p}, \quad h \in \{1, 3, 7, 14\}$$
where each cell denotes the conditional probability or standardized transmission magnitude:
$$\pi_{ij,h} = P(X_{j,t+h} > q_j \mid \text{Shock}_{i,t})$$

This formulation captures multi-step transmission pathways:
$$\text{Geopolitics}_t \xrightarrow{\text{Lag 1}} \text{Energy}_{t+1} \xrightarrow{\text{Lag 2}} \text{Financial Spread}_{t+3} \xrightarrow{\text{Lag 4}} \text{Societal Stress}_{t+7}$$
The empirical objective is to determine whether source-domain information provides statistically significant **incremental predictive skill** for target domains:
$$\Delta \text{Skill}_{ij,h} = \text{Skill}(\text{Model}_{i \leftarrow j}) - \text{Skill}(\text{Model}_i) > 0$$

---

## 3.5 Dimension 4: Time as a Structural Dimension ($t+h$)

In conventional cross-sectional or static forecasting, time is merely an external index or a single fixed horizon. In the 4D framework, **Time** is an explicit structural dimension:

1. **Horizon-Dependent Coefficients ($\beta_h$)**: Predictive relationships are not assumed identical across time horizons. High-frequency signals (such as digital information velocity and equity volatility) dominate near-term horizons ($h=1, 3$), while structural macroeconomic and environmental variables dominate longer horizons ($h=7, 14$).
2. **Point-in-Time Conditioning ($\mathcal{I}_t$)**: All forecasts are strictly conditioned on information available prior to or at forecast origin $t$:
   $$P(Y_{t+h} \mid \mathcal{I}_t), \quad \mathcal{I}_t = \{x : \text{first\_available}(x) \le t\}$$
3. **Dynamic Recalibration**: Forecast uncertainty intervals expand nonlinearly with $h$, requiring horizon-specific dynamic calibration.

---

## 3.6 The Six-Layer Evidentiary Firewall

To maintain absolute research integrity, the dissertation enforces an unyielding separation between theoretical expectations and empirical validation:

```
[ Layer 1: Conceptual Prior ]      (Subjective baseline scenario, e.g. S1 = 65%)
            │
            ▼
[ Layer 2: Observed Evidence ]     (Point-in-time timestamped data at origin t)
            │
            ▼
[ Layer 3: Statistical Estimate ]   (State-space loadings and interaction matrices)
            │
            ▼
[ Layer 4: Posterior Forecast ]     (Out-of-sample probability distribution)
            │
            ▼
[ Layer 5: Scenario Probability ]   (Model-derived joint threshold exceedance)
            │
            ▼
[ Layer 6: Empirical Finding ]     (Verified out-of-sample proper scoring result)
```

**Cardinal Rule**: A numerical probability is never an empirical finding until it has been estimated from information strictly available at the forecast origin and verified against subsequently observed outcomes under strictly proper scoring rules.

---

## 3.7 Chapter Summary & Formal Hypotheses

The four-dimensional framework yields seven testable, preregistered hypotheses:
* **H1 (Multidisciplinary Value)**: Multidisciplinary models achieve positive Brier Skill Score ($\text{BSS} > 0$) relative to single-domain models.
* **H2 (Cross-Domain Lagged Skill)**: Source-domain indicators contain incremental out-of-sample predictive information for other domains ($\Delta \text{Skill}_{ij,h} > 0$).
* **H3 (Propagation Superiority)**: Explicit propagation modelling improves multi-horizon forecast accuracy relative to static benchmarks.
* **H4 (Temporal Persistence)**: The latent DGRS exhibits positive autoregressive persistence ($\rho > 0$).
* **H5 (Dynamic Calibration)**: Dynamic calibration achieves lower Expected Calibration Error (ECE) than uncalibrated models.
* **H6 (Horizon Dependency)**: The relative predictive contribution of individual domains shifts systematically as $h$ increases from 1 to 14 days.
* **H7 (Information Velocity Association)**: Salience-normalized information velocity ($\widetilde{IV}_t$) positively predicts subsequent systemic volatility.
