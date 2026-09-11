# Appendix B: Data Codebook and Provenance Dictionary

---

## B.1 High-Frequency Market-Implied & Observational Series

This table documents the primary empirical series ingested into the 4D-MGRFF database, their source provenance, publication lag rules, and mathematical transformations.

| Variable Name | Database Identifier | Domain | Primary Source | Sampling Frequency | Publication Delay ($t_{\text{pub}} - t_{\text{event}}$) | Unit | Transformation | Theoretical Function in 4D Framework |
|---|---|---|---|---|---|---|---|---|
| **10Y–2Y Yield Spread** | `T10Y2Y` | Economics | FRED / U.S. Treasury | Daily (Business) | +18 Hours (Market Close) | Percent | $Z$-score | Monetary stance and yield curve inversion signal |
| **5y5y Forward Inflation** | `T5YIFR` | Economics | FRED / St. Louis Fed | Daily (Business) | +18 Hours (Market Close) | Percent | $Z$-score | Market expectation of medium-term price stability |
| **High Yield Credit OAS** | `BAMLH0A0HYM2` | Finance | ICE Data Indices / FRED | Daily (Business) | +24 Hours (Next Morning) | Percent | $Z$-score | Corporate default liquidity and credit risk aversion |
| **CBOE Volatility Index** | `VIXCLS` | Finance | CBOE / FRED | Daily (Trading) | +18 Hours (Market Close) | Index Points | $Z$-score & $\lambda_{\text{stress}} > 0$ Anchor | Equity fear gauge & global latent state anchor |
| **Brent Crude Oil Benchmark**| `DCOILBRENTEU` | Economics | EIA / FRED | Daily (Trading) | +24 Hours | USD / Barrel | $\sigma_{t, 7} = \text{SD}(100 \Delta \ln P)$ | Commodity supply-shock transmission channel |
| **Broad U.S. Dollar Index** | `DTWEXBGS` | Economics | Federal Reserve / FRED | Daily (Business) | +24 Hours | Index (2006=100) | Log-Return | Global dollar funding and currency stress |
| **Kinetic Conflict Events** | `geo_conflict` | Geopolitics | ACLED / Global Telemetry | Daily (Global) | +24 Hours | Event Count | Weighted Count $\sum w_e$ | Physical political violence and protest severity |
| **News Salience Velocity** | `geo_news_salience` | Information | GDELT 2.0 Project | Daily (Global) | +18 Hours | Relative Salience | $\widetilde{IV}_t = \frac{\text{Salience} - \text{Med}}{\text{MAD}}$ | Narrative acceleration and social panic channel |
| **AI Disruption Velocity** | `tech_velocity` | Technology | Curated Incident Corpus | Daily (Global) | +24 Hours | Incident Count | Trailing 7-day Sum | Frontier compute and technological friction |
| **Global Climate Anomaly** | `climate_anomaly` | Climate | NOAA / Copernicus | Daily / Monthly | +48 Hours | Celsius Anomaly | Baseline Deviation | Slow-moving biophysical background stress |

> **Implementation Note**: The first six series (`T10Y2Y` through `DTWEXBGS`) are ingested through the operational FRED programmatic fetcher with full point-in-time provenance. The final four series (`geo_conflict`, `geo_news_salience`, `tech_velocity`, `climate_anomaly`) are **theoretical framework data contracts** specifying intended production ingestors. In the current empirical evaluation, these non-financial indicators are represented through calibrated simulation proxies in the Cross-Domain Benchmark Panel (see Chapter 4, §4.7 and Chapter 6, Table 5B).

---

## B.2 Feature Transformation Formalizations

### 1. Robust Salience-Normalized Information Velocity ($\widetilde{IV}_t$)
$$\text{Salience}_{d,t} = \frac{N_{d,t}}{\text{TotalGlobalArticles}_t}$$
$$\widetilde{IV}_{d,t} = \frac{\text{Salience}_{d,t} - \text{median}(\text{Salience}_{d, t-14 : t-1})}{1.4826 \cdot \text{MAD}(\text{Salience}_{d, t-14 : t-1}) + 10^{-6}}$$
Filtered exclusively by **CAMEO QuadClass 4 (Material Conflict)** with **Goldstein Conflict Scale $\le -5.0$**.

### 2. Rolling Log-Return Volatility ($\sigma_{t,k}$)
$$r_t = 100 \cdot \ln\left(\frac{P_t}{P_{t-1}}\right)$$
$$\sigma_{t,k} = \sqrt{\frac{1}{k-1} \sum_{m=0}^{k-1} (r_{t-m} - \bar{r}_t)^2}, \quad k = 7 \text{ days}$$

### 3. Origin-Safe $Z$-Score Normalization
$$Z_{j,t} = \frac{X_{j,t} - \mu_{j,\text{train}(t)}}{\sigma_{j,\text{train}(t)}}$$
Parameters $\mu_{j,\text{train}(t)}$ and $\sigma_{j,\text{train}(t)}$ are computed strictly using data available up to origin $t$, guaranteeing zero lookahead leakage into test slices.
