# Preregistration Protocol: 4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)

**Date of Preregistration Freeze**: September 2026  
**Status**: Frozen prior to final out-of-sample test window evaluation  
**Design**: Longitudinal, probabilistic, rolling-origin out-of-sample forecasting  

---

## 1. Core Research Questions & Hypotheses
* **RQ1 / H1**: Multidisciplinary models achieve strictly lower out-of-sample proper-scoring loss and positive Brier Skill Score ($\text{BSS} > 0$) relative to the best single-domain benchmark.
* **RQ2 / H2**: Lagged source-domain indicators provide incremental out-of-sample predictive skill ($\Delta \text{Skill}_{ij,h} > 0$) for target domains.
* **RQ3 / H3**: Propagation-aware models ($\Pi_h$) outperform static models at horizons $h \in \{7, 14\}$ days.
* **RQ4 / H4**: The latent DGRS factor exhibits statistically significant autoregressive persistence ($\rho > 0$).
* **RQ5 / H5**: The Two-Tier dynamic calibration procedure yields lower Expected Calibration Error (ECE) and calibration slope closer to 1 than static baselines.
* **RQ6 / H6**: High-frequency indicators dominate at $h=1,3$, while structural/macro proxies dominate at $h=7,14$.
* **RQ7 / H7**: Salience-normalized information velocity ($\widetilde{IV}_t$) positively predicts subsequent systemic volatility.

---

## 2. Frozen Outcome Definitions & Thresholds
1. **Primary Binary Event ($Y_t^{(h)}$)**:
   $$Y_t^{(h)} = \mathbb{I}(S_{t+h} \ge q_{0.90})$$
   where $q_{0.90}$ is the 90th percentile of standardized latent DGRS stress computed **exclusively** on the training window.
2. **Continuous Volatility Target ($\Delta S_t^{(h)}$)**:
   $$\Delta S_t^{(h)} = S_{t+h} - S_t$$
3. **Multi-Domain Escalation ($S_3$)**:
   $$Y_{\text{multi},t}^{(h)} = \mathbb{I}\left(\sum_{d=1}^5 \mathbb{I}(R_{d,t+h} \ge c_d) \ge 3\right)$$
   where $c_d$ is the 90th percentile of domain-specific stress within the training window.

---

## 3. Frozen Forecast Horizons & Vintages
* **Horizons**: $h \in \{1, 3, 7, 14\}$ days ahead.
* **Point-in-Time Rule**:
  $$I_t = \{x : \text{first\_available\_timestamp}(x) \le t\}$$
  Any data item published after forecast origin $t$ is strictly excluded from feature generation, state estimation, and model fitting at origin $t$.

---

## 4. Frozen Model Ladder
* **M0**: Persistence Baseline ($\hat{p}_{t+h} = Y_t$)
* **M1**: Climatology / Unconditional Training Base Rate ($P(Y=1) = \bar{Y}_{\text{train}}$)
* **M2**: Single-Domain Logistic Models
* **M3**: Multidisciplinary Regularized ElasticNet ($L_1/L_2$)
* **M4**: Dynamic Autoregressive Models
* **M5**: LightGBM Nonlinear Machine Learning Benchmark
* **M6**: Dynamic Linear Model (DLM) / State-Space with Kalman Smoother
* **M7**: Full 4D Model (State + Interaction + Propagation + Horizon dynamics)

---

## 5. Frozen Evaluation Metrics
* **Brier Score (BS)**: $\frac{1}{N} \sum (p_t - y_t)^2$
* **Brier Skill Score (BSS)**: $1 - \frac{\text{BS}_{\text{model}}}{\text{BS}_{\text{climatology}}}$ (Must be $> 0$)
* **Logarithmic Score (LS)**: Cross-entropy loss
* **Continuous Ranked Probability Score (CRPS)**: For continuous state predictions
* **Expected Calibration Error (ECE)** & Reliability Curves (10 bins)
* **Precision-Recall AUC (PR-AUC)**: Primary discrimination metric for rare $S_3$ events
* **Relative Value Score ($V(\alpha)$)**: Richardson / Murphy-Winkler cost-loss decision utility

---

## 6. The 10 Preregistered Falsification Criteria
The 4D framework will be officially deemed **unsupported** if:
1. M7 fails to achieve $\text{BSS} > 0$ relative to M1 (Climatology) and M5 (LightGBM).
2. Propagation matrices ($\Pi_h$) add zero out-of-sample skill over static models.
3. Latent state ($F_t$) provides no incremental predictive value over raw predictors.
4. Out-of-sample probabilities display uncorrectable miscalibration ($\text{ECE} > 0.15$).
5. Predictive relationships evaporate under independent data source substitution.
6. Results rely entirely on a single data source (e.g., GDELT alone).
7. Strict publication-delay buffers (+24h, +48h) eliminate all apparent predictive power.
8. The model performs solely during historical crises and fails in normal periods.
9. Domain ablations reveal zero marginal contribution from 3 or more domains.
10. The Relative Value Score $V(\alpha) \le 0$ across operational cost-loss ratios.

*Any null finding under these criteria will be reported fully in Chapter 9 (Robustness & Falsification).*
