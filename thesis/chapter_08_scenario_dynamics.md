# Chapter 8: Operationalized Scenario and Early-Warning Dynamics

---

## 8.1 From Qualitative Narratives to Operationalized Regimes

Scenario planning has long been a staple of strategic foresight, offering narrative descriptions of potential futures (e.g., Wack 1985; Peterson et al. 2003). However, conventional scenarios suffer from three fundamental deficiencies:
1. **Static Categorization**: Scenarios are typically depicted as fixed future states (e.g., "World in 2030") rather than dynamically evolving trajectories.
2. **Arbitrary Likelihoods**: Scenario planning exercises frequently assign subjective probabilities (e.g., "Scenario A has a 60% probability") without mathematical grounding or calibration.
3. **Absence of Quantitative Trigger Thresholds**: Qualitative narratives fail to specify what precise observable data prints would signal a transition from one scenario to another.

To overcome these deficiencies, the 4D framework **operationalizes qualitative scenarios into three mutually exclusive, mathematically defined discrete regimes**:

```
[ S1: Managed Volatility ]       Systemic volatility elevated, but NO multi-domain threshold breach
            │
      (Single Shock)
            ▼
[ S2: Signal Shock ]             Isolated acute threshold breach in 1 or 2 domains (localized contagion)
            │
   (Multi-Domain Cascade)
            ▼
[ S3: Multi-Domain Escalation ]  Simultaneous threshold breaches in >= 3 independent domains
```

### Mathematical Definitions
Let $R_{d,t}$ represent the standardized stress index for domain $d \in \{G, E, T, I, C\}$, and let $c_d$ denote its frozen 90th percentile threshold derived strictly from training data:
* **$S_1$ (Managed Volatility)**:
  $$\sum_{d=1}^5 \mathbb{I}(R_{d,t} \ge c_d) = 0 \quad \text{and} \quad F_t \in [q_{0.50}, q_{0.85})$$
* **$S_2$ (Signal Shock)**:
  $$\sum_{d=1}^5 \mathbb{I}(R_{d,t} \ge c_d) \in \{1, 2\}$$
* **$S_3$ (Multi-Domain Escalation)**:
  $$\sum_{d=1}^5 \mathbb{I}(R_{d,t} \ge c_d) \ge 3$$

Under this architecture, scenario assignments are completely deterministic conditional on observed data, allowing empirical model posteriors to be scored against ground-truth regime realizations.

---

## 8.2 Time-Evolving Scenario Probability Trajectories

A foundational innovation of the 4D framework is that scenario probabilities are not static single-point estimates; they are **continuous dynamic trajectories** across forecast horizons:
$$\mathbf{P}_t(h) = \Big[ P(S_{1, t+h} \mid \mathcal{I}_t), \; P(S_{2, t+h} \mid \mathcal{I}_t), \; P(S_{3, t+h} \mid \mathcal{I}_t) \Big]^T, \quad h \in \{1, 3, 7, 14\}$$

Estimated via a multinomial dynamic logistic formulation:
$$P(S_{k, t+h} = 1 \mid \mathcal{I}_t) = \frac{\exp\big(\alpha_{k,h} + \beta_{k,h}^T X_t + \delta_{k,h} F_t\big)}{\sum_{j=1}^3 \exp\big(\alpha_{j,h} + \beta_{j,h}^T X_t + \delta_{j,h} F_t\big)}$$

### Empirical Trajectory Dynamics
During non-crisis baseline periods, the empirical posterior assigns:
* $P(S_1) \approx 0.82$ (Managed Volatility dominant)
* $P(S_2) \approx 0.16$ (Low background probability of isolated shock)
* $P(S_3) \approx 0.02$ (Rare probability of systemic cascade)

However, when an acute kinetic conflict shock strikes ($X_{G,t} > +2.5\sigma$) accompanied by an abnormal surge in digital news salience velocity ($\widetilde{IV}_t > +3.0$), the trajectory shifts nonlinearly:
* At $h=1$ day: $P(S_2)$ surges to **0.68**, while $P(S_3)$ rises to **0.14**.
* At $h=3$ days: As the shock propagates through energy and credit markets (§7.3), $P(S_3)$ reaches its peak at **0.31**.
* At $h=7$ and $h=14$ days: As market adaptation and policy stabilization take effect, $P(S_3)$ attenuates back toward **0.06**, and $P(S_1)$ recovers to **0.78**.

This horizon trajectory provides decision-makers with a quantitative window of maximum vulnerability (Days 2 to 4 post-shock), enabling targeted pre-emptive mitigation before multi-domain contagion solidifies.

---

## 8.3 The $3 \times 3$ Markov Scenario Transition Matrix

To analyze regime persistence and escalation dynamics, the framework estimates the empirical one-step transition matrix:
$$\mathbf{T} = [T_{ij}] \in \mathbb{R}^{3 \times 3}, \quad T_{ij} = P\big(S_{t+1} = j \;\big|\; S_t = i, \;\mathcal{D}_t\big)$$

### Table 8.1: Empirical Scenario Transition Matrix

| Current State ($S_t$) | Transition to $S_1$ (Managed Vol) | Transition to $S_2$ (Signal Shock) | Transition to $S_3$ (Escalation) | Regime Half-Life ($t_{1/2}$) |
|---|---|---|---|---|
| **$S_1$: Managed Volatility** | **0.912** | 0.078 | 0.010 | ~7.5 days |
| **$S_2$: Signal Shock**        | 0.345     | **0.582** | 0.073 | ~1.3 days |
| **$S_3$: Multi-Domain Escalation** | 0.082 | 0.328 | **0.590** | ~1.3 days |

### Structural Insights:
1. **High Inertia of Managed Volatility**: $S_1$ is an absorbing attractor ($T_{11} = 0.912$). In the absence of acute exogenous impulses, global stability displays strong self-reinforcing persistence.
2. **Transient Nature of Signal Shocks**: $S_2$ has a self-transition probability of only $0.582$. An isolated shock resolves back into managed volatility within 24–48 hours ($T_{21} = 0.345$) 4.7 times more frequently than it escalates into full multi-domain crisis ($T_{23} = 0.073$).
3. **Escalation De-escalation Asymmetry**: Once the system enters $S_3$ (Multi-Domain Escalation), direct transition back to tranquil stability is virtually impossible ($T_{31} = 0.082$). The system de-escalates step-wise, passing first through isolated signal shocks ($T_{32} = 0.328$) as individual markets stabilize asynchronously.

---

## 8.4 Early-Warning Indicator Sensitivities ($EW_j(h)$)

A critical requirement for institutional early warning is determining which specific indicators are the most dangerous harbingers of systemic escalation. The framework defines the **Early-Warning Sensitivity** as the partial derivative of the multi-domain escalation probability with respect to standardized indicator $X_{j,t}$:
$$EW_j(h) = \frac{\partial P(S_{t+h} = \text{Escalation})}{\partial X_{j,t}} = p_3(h) \big(1 - p_3(h)\big) \cdot \beta_{3,j,h}$$

### Table 8.2: Empirical Early-Warning Sensitivity Ranking ($h=3$ Days)

| Rank | Indicator | Domain | Sensitivity Score ($EW_j$) | Operational Interpretation |
|---|---|---|---|---|
| **1** | `vix` | Finance | **+0.142** | Financial panic acts as the primary transmission hub across all domains. |
| **2** | `geo_news_salience` | Information | **+0.118** | Abnormal media velocity precedes physical escalation by 48–72 hours. |
| **3** | `energy_vol` | Economics | **+0.094** | Crude oil price instability accelerates cross-border supply chain stress. |
| **4** | `geo_conflict` | Geopolitics | **+0.088** | Physical violence triggers localized shocks that feed energy markets. |
| **5** | `hy_spread` | Finance | **+0.065** | Corporate credit widening reflects liquidity withdrawal. |
| **6** | `tech_velocity` | Technology | **+0.032** | AI incident surges introduce regulatory and cyber friction. |
| **7** | `climate_anomaly` | Climate | **+0.004** | Environmental stress operates as a slow background variable. |

This ranking provides institutional risk managers with an objective, empirically validated hierarchy: **surges in equity volatility (`vix`) and digital news salience (`geo_news_salience`) carry the highest marginal threat of tipping the global system into multi-domain escalation**.
