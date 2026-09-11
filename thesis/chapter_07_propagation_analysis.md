# Chapter 7: Dynamic Risk Propagation Analysis

---

> **Correction notice.** The propagation matrix estimator was previously implemented as a **fixed, hand-picked exponential decay applied uniformly to a static correlation matrix** ($\pi_{ij,h} = \rho_{ij} \cdot \exp(-0.15h)$), rather than something estimated from data. Because that formula multiplies every cell by the *same* scalar $\exp(-0.15h)$, it mathematically guaranteed an identical ~59.3–59.4% "decay" for every indicator pair at $h=7$ regardless of the underlying data — a tautology of the formula, not an empirical finding. `models/full_4d_dlm.py` now estimates $\Pi_h$ directly as an empirical lead-lag standardized cross-covariance,
> $$\pi_{ij,h} = \frac{\widehat{\text{Cov}}(X_{i,t+h}, X_{j,t})}{\widehat{\text{Var}}(X_{j,t}) + \varepsilon},$$
> computed from the training window at each rolling origin. This chapter has been rewritten against the corrected estimator and regenerated numbers. As disclosed in §4.3.1, the panel used below is the **calibrated synthetic panel**, not real GDELT/ACLED/NOAA data.

## 7.1 The Mechanics of Cross-Domain Contagion

The 4D framework's working hypothesis is that global disruptions do not remain confined to their originating domain but propagate through the interconnected network of global affairs. This chapter provides a structural analysis of the **transmission pathways and horizon-dependent attenuation** recovered by the corrected empirical estimator, on the calibrated synthetic panel described in §6.1.

### Predictive Propagation vs. Causal Identification
As before, the estimands in this chapter represent **predictive propagation** (lead-lag statistical association) rather than structural causal identification:
$$\pi_{ij,h} = \frac{\widehat{\text{Cov}}(X_{i,t+h}, X_{j,t})}{\widehat{\text{Var}}(X_{j,t})}$$
This measures the standardized statistical association between indicator $j$ at time $t$ and indicator $i$ at $t+h$; it does not, by itself, establish a causal transmission mechanism.

---

## 7.2 The Horizon Propagation Matrices ($\Pi_1$ vs. $\Pi_7$) — Corrected Empirical Estimates

Table 7.1 reports the empirical pairwise transmission matrices, re-estimated with the corrected estimator. Rows are the **response (target) indicator** $i$; columns are the **shock-origin indicator** $j$; cell $(i,j)$ is $\pi_{ij,h}$.

### Table 7.1: Estimated Cross-Domain Dynamic Propagation Matrices ($\Pi_1$ vs $\Pi_7$)

**Horizon $h=1$ Day ($\Pi_1$)**

| Response ($i$) \ Origin ($j$) | Conflict | Salience | Energy | VIX | Spread | Tech | Climate |
|---|---|---|---|---|---|---|---|
| **Conflict (`geo_conflict`)** | 0.712 | 0.705 | 0.392 | 0.506 | 0.470 | 0.484 | -0.119 |
| **Salience (`geo_news_salience`)** | 0.717 | 0.684 | 0.381 | 0.530 | 0.514 | 0.473 | -0.084 |
| **Energy (`energy_vol`)** | 0.570 | 0.551 | 0.776 | 0.422 | 0.365 | 0.450 | -0.142 |
| **VIX (`vix`)** | 0.700 | 0.712 | 0.336 | 0.900 | 0.850 | 0.504 | -0.022 |
| **Spread (`hy_spread`)** | 0.619 | 0.621 | 0.273 | 0.834 | 0.789 | 0.469 | -0.055 |
| **Tech (`tech_velocity`)** | 0.570 | 0.559 | 0.351 | 0.405 | 0.366 | 0.413 | -0.083 |
| **Climate (`climate_anomaly`)** | -0.064 | -0.036 | -0.081 | 0.016 | 0.017 | -0.117 | -0.003 |

**Horizon $h=7$ Days ($\Pi_7$)**

| Response ($i$) \ Origin ($j$) | Conflict | Salience | Energy | VIX | Spread | Tech | Climate |
|---|---|---|---|---|---|---|---|
| **Conflict (`geo_conflict`)** | 0.258 | 0.261 | 0.328 | 0.145 | 0.163 | 0.214 | -0.011 |
| **Salience (`geo_news_salience`)** | 0.275 | 0.283 | 0.323 | 0.153 | 0.172 | 0.230 | 0.000 |
| **Energy (`energy_vol`)** | 0.378 | 0.375 | 0.416 | 0.247 | 0.210 | 0.301 | -0.035 |
| **VIX (`vix`)** | 0.186 | 0.183 | 0.224 | 0.162 | 0.182 | 0.131 | 0.001 |
| **Spread (`hy_spread`)** | 0.137 | 0.148 | 0.181 | 0.169 | 0.191 | 0.079 | 0.025 |
| **Tech (`tech_velocity`)** | 0.161 | 0.175 | 0.298 | 0.122 | 0.130 | 0.138 | 0.087 |
| **Climate (`climate_anomaly`)** | -0.070 | -0.080 | 0.041 | 0.030 | 0.056 | -0.101 | 0.101 |

*(Archived in `results/tables/table_8_propagation_matrix_h1.csv` and `_h7.csv`, regenerated from the corrected estimator.)*

---

## 7.3 Dissecting the Primary Contagion Channels

### 1. Geopolitics/Information $\rightarrow$ VIX $\rightarrow$ Credit Spread
Conflict transmits into VIX with $\pi_{\text{VIX}\leftarrow\text{Conflict},1\text{d}} = 0.700$, and VIX transmits into the credit spread with $\pi_{\text{Spread}\leftarrow\text{VIX},1\text{d}} = 0.850$. By $h=7$, these fall to $0.186$ and $0.169$ respectively.

### 2. The Information Channel
Salience-normalized news velocity transmits into VIX at $\pi_{\text{VIX}\leftarrow\text{Salience},1\text{d}} = 0.712$, comparable in magnitude to the direct conflict $\rightarrow$ VIX channel above, falling to $0.183$ by $h=7$.

### 3. Domain Orthogonality: The Climate Disconnect
The climate anomaly indicator shows near-zero or slightly negative transmission to/from every other domain at both horizons (e.g. $\pi_{\text{VIX}\leftarrow\text{Climate},1\text{d}} = -0.022$, $\pi_{\text{VIX}\leftarrow\text{Climate},7\text{d}} = 0.001$), consistent with the synthetic generator's design (climate is drawn independently of the shared latent factor).

---

## 7.4 Temporal Attenuation & Impulse Kinetics — Corrected

Unlike the previous (tautological) fixed-decay formula, the corrected estimator produces **pair-specific attenuation rates** that are no longer forced to a single constant:

| Channel | $\pi_{h=1}$ | $\pi_{h=7}$ | Attenuation ($h{=}1\to7$) |
|---|---|---|---|
| Conflict $\rightarrow$ VIX | 0.700 | 0.186 | -73.4% |
| Salience $\rightarrow$ VIX | 0.712 | 0.183 | -74.3% |
| VIX $\rightarrow$ Spread | 0.850 | 0.169 | -80.1% |
| Conflict $\rightarrow$ Energy | 0.570 | 0.378 | -33.7% |
| Conflict $\rightarrow$ Tech | 0.570 | 0.161 | -71.8% |
| Climate $\rightarrow$ VIX | -0.022 | 0.001 | negligible in both periods |

Attenuation across these channels ranges from roughly **34% to 80%** over a one-week horizon — a substantively wider and more informative spread than the previous implementation's mathematically-forced ~59% for every pair. The Conflict $\rightarrow$ Energy channel decays markedly more slowly (-34%) than the financial-market channels (-70% to -80%), consistent with energy markets clearing shocks more slowly than equity volatility. **This heterogeneity should still be read as a property of the synthetic generator's specific parameterization** (§4.3.1) rather than a validated real-world finding, pending real GDELT/ACLED/NOAA ingestion.

---

## 7.5 Negative-Control Placebo Tests

To assess whether estimated propagation pathways reflect genuine lead-lag structure rather than spurious artifacts of the estimator itself, two placebo checks are informative:
1. **Temporal Lag Inversion**: Estimating $\pi_{ij,h}$ with the roles of "future" and "past" reversed ($S_{i,t} \to S_{j,t+h}$, i.e., testing whether current values predict *past* values of another series) should yield near-zero coefficients under a correctly time-ordered estimator, since $\widehat{\text{Cov}}(X_{i,t-h}, X_{j,t})$ for large $h$ captures only the same underlying AR(1) persistence, not a reversed arrow of time.
2. **Indicator Shuffling**: Randomly permuting the time index of the origin series before computing $\widehat{\text{Cov}}$ should collapse the estimated coefficient toward zero, since covariance under permutation has expectation zero.

*(These two checks were previously reported with a specific placebo-distribution p-value and confidence interval computed against the old fixed-decay implementation's numbers. Because the estimator has since changed, those specific figures no longer apply and are removed pending a re-run of the placebo protocol against the corrected `Full4DDLMModel.get_propagation_matrix` implementation. The qualitative logic of the placebo test — and the expectation that a genuine lead-lag estimator should fail both checks by producing near-zero coefficients — still holds and should be re-verified before being cited as a completed robustness result.)*
