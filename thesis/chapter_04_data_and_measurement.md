# Chapter 4: Data Architecture and Point-in-Time Measurement

---

## 4.1 The Lookahead Leakage Trap in Empirical Forecasting

In empirical time-series forecasting, a substantial proportion of published "breakthroughs" are artifacts of insidious **lookahead data leakage**. In quantitative social science and macro-finance, leakage typically enters through three pervasive vectors:

1. **Global Preprocessing Leakage**: Standardizing an entire 10-year dataset using the global sample mean $\mu_{\text{global}}$ and standard deviation $\sigma_{\text{global}}$ before splitting into train/test sets. This injects future variance information into the training window.
2. **Publication-Timestamp Asynchrony**: Using macroeconomic series indexed by reference event date $t$ rather than first-available publication timestamp $t_{\text{pub}}$. For example, US Q1 GDP reflects economic activity through March 31, but the advance estimate is not published until late April. Conditioning a forecast at April 5 on Q1 GDP represents temporal lookahead bias.
3. **Retrospective Revision Contamination**: Incorporating revised historical values rather than real-time data vintages. Macroeconomic agencies (e.g., IMF, Bureau of Economic Analysis) revise historical estimates years after the event. Evaluating historical forecasts on today's revised numbers evaluates model performance on information that no decision-maker possessed at the time.

To eliminate these vulnerabilities, this dissertation implements a **strict point-in-time data architecture** that operates as an uncompromised firewall against all lookahead contamination.

---

## 4.2 The Point-in-Time Provenance Schema

All data entering the 4D-MGRFF framework are stored in an immutable, long-form relational database schema (`global_risk_provenance`):

```sql
CREATE TABLE global_risk_provenance (
    observation_id VARCHAR PRIMARY KEY,
    event_time TIMESTAMP NOT NULL,
    publication_time TIMESTAMP NOT NULL,
    first_available_timestamp TIMESTAMP NOT NULL,
    revision_timestamp TIMESTAMP,
    forecast_origin TIMESTAMP,
    horizon INTEGER,
    source VARCHAR NOT NULL,
    source_version VARCHAR NOT NULL,
    domain VARCHAR NOT NULL,
    country VARCHAR,
    region VARCHAR,
    indicator VARCHAR NOT NULL,
    raw_value DOUBLE,
    transformed_value DOUBLE,
    unit VARCHAR,
    transformation VARCHAR,
    missing_flag BOOLEAN DEFAULT FALSE,
    revision_flag BOOLEAN DEFAULT FALSE,
    eligibility_at_origin BOOLEAN DEFAULT TRUE
);
```

### The Point-in-Time Information Set Rule
At any historical forecast origin $t$, the permissible information set $\mathcal{I}_t$ is defined strictly as:
$$\mathcal{I}_t = \big\{ x \in \text{Database} \;\big|\; \text{first\_available\_timestamp}(x) \le t \big\}$$
Equivalently:
$$\mathcal{D}_t = \{x : \text{availability}(x) \le t\}, \quad \text{NOT} \quad \mathcal{D}_t = \{x : \text{event\_time}(x) \le t\}$$

The ingestion engine enforces an automated validation check (`assert_zero_leakage`) that scans every test slice and raises a fatal exception if any observation has a `first_available_timestamp` exceeding the forecast origin.

---

## 4.3 High-Frequency Macro Proxies: Resolving the Latency Paradox

The dissertation targets near-term daily horizons: $h \in \{1, 3, 7, 14\}$ days. A significant methodological hazard in multidisciplinary forecasting is **frequency mismatch**. 

Traditional macroeconomic indicators (e.g., IMF World Economic Outlook, national GDP, consumer price indices) are released monthly or semi-annually. Over a 7-day or 14-day forecast window, an IMF WEO projection is a flat constant. It provides zero daily variance. In an out-of-sample ablation analysis, the "Economics" domain would appear to carry zero marginal predictive skill solely because of **temporal latency death**.

To resolve this paradox, the framework establishes a **High-Frequency Market-Implied Macroeconomic Proxy Layer** drawn from the Federal Reserve Bank of St. Louis (FRED), updating daily:

| Indicator ID | Source | Frequency | Description | Theoretical Function |
|---|---|---|---|---|
| `T10Y2Y` | FRED / Treasury | Daily | 10-Year Minus 2-Year Treasury Yield Spread | Real-time monetary policy stance and recession expectations |
| `T5YIFR` | FRED | Daily | 5-Year, 5-Year Forward Inflation Expectation | Market-based expectation of long-term price stability |
| `BAMLH0A0HYM2` | ICE BofA | Daily | US High Yield Index Option-Adjusted Spread | Systemic corporate credit and default liquidity stress |
| `VIXCLS` | CBOE | Daily | CBOE Volatility Index (VIX) | Systemic equity market fear and risk aversion barometer |
| `DCOILBRENTEU` | EIA / Benchmark | Daily | Brent Crude Oil Daily Benchmark Price | Physical commodity supply-shock transmission channel |
| `DTWEXBGS` | Federal Reserve | Daily | Nominal Broad Trade-Weighted U.S. Dollar Index | Global dollar liquidity and foreign exchange stress |

By ingesting **43,707 point-in-time daily records** across these six series spanning 1976 to September 2026, the framework endows the Economic and Financial domains with high-frequency variance matching the daily resolution of political violence and digital media.

### 4.3.1 Data Provenance Disclosure: Implemented vs. Conceptual Sources

In the interest of scientific transparency, this section makes an explicit distinction between the data layer that is **actually implemented and ingested** and the data layer that remains **conceptual specification** in the current build of the framework:

* **Implemented (real, live-fetched data)**: The six FRED/CBOE/ICE/EIA series in §4.3 above are ingested by a live HTTP client (`src/acquisition/fred_ingestor.py`) directly from the St. Louis Fed's public CSV endpoints, with no synthetic substitution. This is the only fully real, externally-sourced data pathway currently wired into the codebase.
* **Conceptual (not yet implemented)**: GDELT (news salience), ACLED (conflict events), the AI/technology incident corpus, and the NOAA/Copernicus climate anomaly feed described in §4.4–4.5 and Appendix B are **architectural specifications only**. No ingestion client for any of these four sources exists in the repository at the time of writing. Wherever the dissertation needs data resembling these domains for methodological demonstration (Chapter 6, Chapter 7), it uses a **calibrated synthetic multidisciplinary panel** (`src/acquisition/synthetic_stream.py`) that generates columns with matching names and a known, hand-specified cross-domain propagation structure (`geo_conflict`, `geo_news_salience`, `energy_vol`, `tech_velocity`, `climate_anomaly`).

Chapter 6 therefore reports **two distinct empirical tracks**, and readers should not conflate them:
1. A **synthetic-panel validation track**, used to demonstrate that the estimation and backtesting machinery (Kalman/RTS smoothing, the M0–M7 model ladder, rolling-origin scoring) behaves correctly against a data-generating process with a *known* ground-truth propagation structure. Results on this track are a software/methodology check, not an empirical finding about the real world.
2. A **real FRED-data validation track**, restricted to the six genuinely-ingested financial/macro series, which is the only track that supports substantive claims about real-world predictability.

Any claim in this dissertation phrased as an empirical finding about geopolitical, informational, technological, or climate risk transmission should be read as a **demonstration on the calibrated synthetic panel**, not as a validated finding about actual GDELT/ACLED/NOAA data, until those ingestion pathways are built and the corresponding backtest is re-run.

---

## 4.4 Robust Salience Normalization for GDELT Information Velocity ($\widetilde{IV}_t$)

*(Note: as disclosed in §4.3.1, no GDELT ingestion client exists yet. The transformation below is implemented and unit-tested in `src/features/features.py::compute_salience_normalized_velocity` and is exercised in this dissertation against the synthetic panel's `geo_news_salience` column, which is designed to mimic GDELT-style salience series but is not derived from real GDELT data.)*

The Global Database of Events, Language, and Tone (GDELT) monitors broadcast, print, and web news globally in over 100 languages. While GDELT provides unparalleled high-frequency coverage, using raw daily event counts ($N_t$) introduces severe measurement artifacts:
* **Crawler Additions**: When GDELT adds new web scrapers or server clusters, raw event volume jumps by 300% without any change in physical conflict.
* **Wire Syndication Cascades**: A single wire report from Reuters syndicated to 5,000 regional outlets produces 5,000 duplicate events, creating artificial spikes in apparent event intensity.

### The Relative Event Salience Formulation
To eliminate crawler expansion artifacts and media syndication noise, the framework reformulates Information Velocity as **Relative Event Salience**:
$$\text{Salience}_{d,t} = \frac{N_{d,t}}{\text{TotalGlobalArticles}_t}$$
The normalized velocity is computed via a robust $Z$-score against a 14-day trailing window strictly preceding origin $t$:
$$\widetilde{IV}_{d,t} = \frac{\text{Salience}_{d,t} - \text{median}\big(\text{Salience}_{d, t-L : t-1}\big)}{1.4826 \cdot \text{MAD}\big(\text{Salience}_{d, t-L : t-1}\big) + \varepsilon}$$
where $\text{MAD}$ is the Median Absolute Deviation, and $1.4826$ is the normal consistency scale factor. Furthermore, events are filtered strictly by **CAMEO QuadClass 4 (Material Conflict)** and the **Goldstein Conflict Scale ($\le -5.0$)**, isolating physical conflict escalation from diplomatic rhetoric.

---

## 4.5 Political Violence & Event Aggregation (ACLED)

Physical protest, civil disorder, and armed conflict data are sourced from the Armed Conflict Location & Event Data Project (ACLED). ACLED provides structured event records detailing:
* Precise event date and geographic coordinates;
* Event type (Battles, Explosions/Remote Violence, Riots, Protests);
* Actor categories and reported fatalities.

Because fatality numbers undergo localized revision as field reports verify casualties, ACLED records are tagged with their initial database publication timestamp ($t_{\text{pub}}$). The daily aggregated conflict intensity is computed as:
$$EI_{G,t} = \sum_{e \in \text{Events}_t} w_e \cdot \text{Fatalities}_e$$
where $w_e$ represents preregistered event-severity weights.

---

## 4.7 Implementation Status and Data Source Availability Disclosure

> **Transparency Statement**: In the interest of full scientific transparency, this section explicitly documents the current implementation status of each data source described in this chapter.

**Operational Real-Time Ingestors (Fully Implemented)**:

The primary empirical evaluation relies exclusively on the **High-Frequency Market-Implied Macroeconomic Proxy Layer** described in §4.3. The six FRED-sourced daily indicators (`T10Y2Y`, `T5YIFR`, `BAMLH0A0HYM2`, `VIXCLS`, `DCOILBRENTEU`, `DTWEXBGS`) are ingested through a fully operational programmatic fetcher (`src/acquisition/fred_ingestor.py`) with point-in-time provenance stamping. This panel comprises 43,707 real-world daily records stored in the relational provenance database.

**Theoretical Framework Specifications (Not Yet Operational)**:

The GDELT salience-normalized information velocity (§4.4), the ACLED political violence aggregation (§4.5), the NOAA/Copernicus global climate anomaly, and the curated AI disruption incident corpus described in Appendix B represent the **intended production-grade ingestion pipeline** for the full five-domain architecture. These field-level specifications—including CAMEO QuadClass 4 filtering, Goldstein conflict scale thresholds, and fatality-weighted event intensity formulas—define the precise data contracts under which future ingestors will be implemented.

In the current empirical evaluation, these non-financial domains are represented through **calibrated simulation proxies** in the Cross-Domain Benchmark Panel (Chapter 6, Table 5B). The synthetic generator (`src/acquisition/synthetic_stream.py`) produces columns with matching variable names (`geo_conflict`, `geo_news_salience`, `tech_velocity`, `climate_anomaly`) using controlled random processes that preserve the statistical properties (variance, autocorrelation, cross-correlation) described in the theoretical specification. **No empirical claim in Chapter 6 is based on these simulated series without explicit labeling.** All primary quantitative findings (Table 5A, Table 8A) are derived exclusively from the verified FRED real-data panel.

The development of operational GDELT, ACLED, NOAA, and AI-incident ingestors is identified as a priority extension in §11.4.

---

## 4.6 Origin-Safe Preprocessing & Freezing Protocol

To guarantee mathematical hygiene across all $T$ rolling origins:
1. **Origin-Safe Standardization**:
   $$Z_{j,t} = \frac{X_{j,t} - \mu_{j,\text{train}(t)}}{\sigma_{j,\text{train}(t)}}$$
   where $\mu_{j,\text{train}(t)}$ and $\sigma_{j,\text{train}(t)}$ are fitted **exclusively on the training window** $\tau \le t$.
2. **Threshold Freezing**:
   The primary systemic risk episode threshold:
   $$Y_t^{(h)} = \mathbb{I}(S_{t+h} \ge q_{0.90})$$
   uses a quantile $q_{0.90}$ estimated strictly on the initial historical training sample and held frozen throughout subsequent rolling out-of-sample evaluation.
