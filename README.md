# 4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Research Standard](https://img.shields.io/badge/preregistered-OSF%20Ready-green.svg)](preregistration/preregistration.md)
[![Verification](https://img.shields.io/badge/tests-10%2F10%20passing-brightgreen.svg)](tests/)
[![Monograph PDF](https://img.shields.io/badge/monograph-PDF%20Available-blue.svg)](thesis/DISSERTATION_MONOGRAPH.pdf)

An integrated Bayesian, Dynamic State-Space, and Probabilistic Forecasting architecture for near-term global risk forecasting across Geopolitics, Economics, Technology, Society/Information, and the Environment at horizons $h \in \{1, 3, 7, 14\}$ calendar days ahead.

---

## 1. Key Methodological Contributions

1. **The Four Dimensions of Global Risk**:
   * **State ($S_t$)**: Latent system stress captured via a sign-anchored **Dynamic Global Risk State (DGRS)** common factor $F_t$ ($m=1$) with guaranteed polarity identification ($\lambda_{\text{VIX}} > 0$).
   * **Interaction ($A_t$)**: Time-varying cross-domain transmission dynamics with dimensional reduction and regularized shrinkage.
   * **Propagation ($\Pi_h$)**: Horizon-dependent empirical lead-lag cross-covariance matrices estimating structural shock transmission across time.
   * **Time ($t+h$)**: Expanding-window rolling-origin evaluation strictly preventing temporal lookahead bias.

2. **Dual-Track Empirical Evaluation**:
   * **Primary Real-World Track**: 43,707 point-in-time daily records from the Federal Reserve Bank of St. Louis (FRED) spanning 733 continuous trading days (September 2023 – September 2026), evaluating 211 rolling origins.
   * **Calibrated Cross-Domain Simulation Benchmark**: A 250-day 7-variable panel modeling digital information velocity (GDELT salience) and political conflict escalation (ACLED intensity) under controlled conditions.

3. **Strict Point-in-Time Data Provenance**:
   * Eliminates lookahead contamination, global preprocessing leakage, and revision bias via immutable publication timestamping:
     $$\mathcal{I}_t = \{x \in \text{Database} \mid \text{first\_available\_timestamp}(x) \le t\}$$

4. **Two-Tier Inference Architecture**:
   * **Tier 1 (Operational)**: Fast, analytical Dynamic Linear Model (Kalman Filter and Rauch-Tung-Striebel Smoother) executing in $< 2.0\text{ ms}$ per origin with closed-form posterior credible intervals. Powers 100% of empirical backtesting.
   * **Tier 2 (Architectural Target)**: Quarterly checkpoint Hamiltonian MCMC (NUTS in PyMC) defined as a production specification for non-Gaussian validation.

5. **Proper Scoring & Decision Utility**:
   * Evaluated under strictly proper scoring rules: Brier Score (BS), Brier Skill Score (BSS vs. climatology), Expected Calibration Error (ECE), and Richardson / Murphy-Winkler Relative Value Score ($V(\alpha)$).

---

## 2. Repository Structure

```
4d-global-risk/
├── README.md                                # Project overview and execution guide
├── Makefile                                 # Build, test, lint, and formatting targets
├── pyproject.toml                           # Package metadata and dependencies
├── reproduce_all.py                         # Single-command master scientific replication engine
├── compile_master_manuscript.py             # Master markdown monograph assembler
├── fetch_live_fred_data.py                  # Live FRED API ingestion script
├── run_real_data_experiment.py              # Primary 733-day FRED empirical backtest
├── run_experiments.py                       # Calibrated simulation panel benchmark
│
├── .github/
│   └── workflows/
│       └── ci.yml                           # GitHub Actions CI matrix (Ubuntu/Windows, Py3.11/3.12)
│
├── data/
│   ├── raw/                                 # Raw downloaded data feeds
│   ├── interim/                             # Intermediate processing cache
│   ├── processed/                           # Relational point-in-time provenance SQLite database
│   │   └── global_risk_database.db          # 43,707 verified historical records (10.42 MB)
│   └── metadata/                            # Data dictionary and series codebooks
│
├── models/
│   ├── baselines.py                         # M0 (Persistence) & M1 (Climatology)
│   ├── statistical_models.py                # M2 (Single-Domain), M3 (ElasticNet), M4 (Dynamic AR)
│   ├── nonlinear_model.py                   # M5 (LightGBM Nonlinear Machine Learning Benchmark)
│   └── full_4d_dlm.py                       # M7 (Full 4D Dynamic Linear State-Space Model)
│
├── src/
│   ├── acquisition/                         # Point-in-time schema & FRED ingestor
│   │   ├── schema.py                        # SQLite provenance database & zero-leakage assertions
│   │   ├── fred_ingestor.py                 # Programmatic FRED historical data loader
│   │   └── synthetic_stream.py              # Calibrated cross-domain simulation generator
│   ├── statespace/                          # State-space latent factor estimation
│   │   └── dgrs.py                          # Sign-Identified Kalman Filter & RTS Smoother
│   ├── features/                            # Feature engineering & origin-safe standardization
│   │   └── features.py                      # Robust salience velocity & rolling volatility
│   └── evaluation/                          # Verification engine
│       ├── backtest.py                      # Expanding rolling-origin evaluation engine
│       ├── scoring.py                       # BSS, ECE, Log-Score, PR-AUC, Relative Value
│       └── plotting.py                      # Publication heatmap and trajectory plotting
│
├── scripts/
│   └── export_monograph.py                  # MathJax HTML & Headless Edge PDF compilation
│
├── results/
│   ├── tables/                              # Empirical results (Table 5 & 8, Real & Sim)
│   └── figures/                             # High-resolution figures (Figures 4, 7, 11)
│
├── tests/
│   ├── test_core_modules.py                 # Factor stability, leakage & scoring tests
│   └── test_pipeline_and_models.py          # Model ladder contracts & backtest tests
│
├── docs/
│   ├── DOCTORAL_DEFENSE_PRESENTATION.md     # 20-Slide Structured Oral Defense Deck
│   └── 4D_Global_Risk_Dissertation_Upgraded_Specification.md
│
├── preregistration/
│   └── preregistration.md                   # Frozen preregistration protocol & 10 falsification criteria
│
└── thesis/
    ├── DISSERTATION_MASTER_MANUSCRIPT.md    # Complete 11-chapter dissertation monograph (129.8 KB)
    ├── DISSERTATION_MONOGRAPH.html          # Interactive MathJax web monograph
    ├── DISSERTATION_MONOGRAPH.pdf           # Publication-grade formatted PDF monograph (2.95 MB)
    ├── chapters 01–11                       # Individual chapter markdown sources
    └── appendices a–b                       # Proofs and Data Codebook
```

---

## 3. Quickstart & Turnkey Replication

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/4d-global-risk.git
cd 4d-global-risk

# Install in editable mode with development dependencies
pip install -e .[dev]
```

### Complete End-to-End Scientific Replication

Run the entire pipeline—from data audit, unit tests, and empirical backtests to figures, tables, and PDF monograph export—in a single command (~32 seconds):

```bash
python reproduce_all.py
```

### Running Individual Components

```bash
# Run 10 formal contract and unit tests
python -m pytest tests/ -v

# Run real FRED macroeconomic empirical backtest (733 trading days)
python run_real_data_experiment.py

# Run calibrated multidisciplinary simulation benchmark (250 days)
python run_experiments.py

# Recompile the master dissertation monograph
python compile_master_manuscript.py

# Export publication-grade HTML and PDF monographs
python scripts/export_monograph.py
```

---

## 4. Key Empirical Findings

1. **Complexity vs. Parsimony on Real Macro-Financial Data**:
   * On the real-world 6-indicator FRED panel, **M2 (Single-Domain Logistic)** and **M4 (Dynamic AR)** achieve the highest discrimination skill at near-term horizons ($\text{BSS} \approx +0.28$ at $h=1\text{d}$; $\text{BSS} \approx +0.20$ at $h=3\text{d}$).
   * **M7 (Full 4D DLM)** delivers the lowest **Expected Calibration Error ($\text{ECE} = 0.0430$)**, confirming that dynamic factor regularization prevents probability overconfidence.
   * **M5 (LightGBM)** provides strong long-horizon decision utility ($V = +0.2500$ at $h=14\text{d}$).

2. **Empirical Lead-Lag Shock Transmission**:
   * Yield curve inversion (`T10Y2Y`) transmits with a $-0.530$ coefficient into high-yield credit risk and $+0.396$ into equity fear (`VIXCLS`).

3. **Persistence Semantics**:
   * M0 Persistence achieves positive skill only at $h=1\text{d}$ ($\text{BSS} = +0.2405$) due to 24-hour financial market autocorrelation, but collapses beyond 24 hours ($\text{BSS} = -0.3847$ at $h=14\text{d}$), confirming that persistence contains zero forward-looking intelligence.

---

## 5. License & Academic Citation

This project is licensed under the MIT License. If using this framework or codebase in academic work, please cite:

```bibtex
@phdthesis{mgrff2026,
  title={A Four-Dimensional Probabilistic Framework for Modelling the Evolution, Interaction, and Propagation of Multidisciplinary Global Risks Through Time},
  author={Izhaan Intellect Research},
  year={2026},
  school={Advanced Quantitative Risk Analysis and Econometrics}
}
```
