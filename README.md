# 4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Research Standard](https://img.shields.io/badge/preregistered-OSF%20Ready-green.svg)](preregistration/preregistration.md)

An integrated Bayesian, Dynamic-System, and Probabilistic Forecasting architecture for near-term global developments across Geopolitics, Economics, Technology, Society/Information, and the Environment at horizons $h \in \{1, 3, 7, 14\}$ days.

---

## 1. Key Architectural Principles

1. **The Four Dimensions**:
   * **State ($S_t$)**: Latent Dynamic Global Risk State (DGRS) factor vector across 5 domains.
   * **Interaction ($A_t$)**: Time-varying cross-domain transmission matrix with shrinkage priors.
   * **Propagation ($\Pi_h$)**: Horizon-dependent multi-step impulse response and transmission matrices.
   * **Time ($t+h$)**: Strict rolling-origin evaluation without lookahead bias.
2. **The 6-Layer Evidentiary Hierarchy**: Clear separation between Conceptual Priors, Observed Evidence, Statistical Estimates, Posterior Forecasts, Scenario Probabilities, and Empirical Findings.
3. **Point-in-Time Data Provenance**: Guarantees zero leakage by filtering available information sets strictly by $I_t = \{x : \text{first\_available}(x) \le t\}$.
4. **Two-Tier Inference Protocol**:
   * *Tier 1*: Fast, analytical Kalman Filter & Smoother (Dynamic Linear Models) for daily rolling origins ($~3,650$ origins).
   * *Tier 2*: Full Hamiltonian Monte Carlo (NUTS in PyMC) at quarterly checkpoint origins for rigorous posterior validation.
5. **Rare-Event & Decision-Theoretic Verification**: Evaluation via Brier Skill Score (BSS) against climatology, Precision-Recall AUC (PR-AUC), and the Richardson/Murphy-Winkler Relative Value Score ($V(\alpha)$).

---

## 2. Repository Structure

```
4d-global-risk/
├── README.md
├── pyproject.toml
├── docs/
│   └── 4D_Global_Risk_Dissertation_Upgraded_Specification.md
├── preregistration/
│   └── preregistration.md
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── metadata/
├── src/
│   ├── acquisition/     # DuckDB point-in-time schema & scrapers
│   ├── validation/      # Vintage and leakage verification
│   ├── features/        # Origin-safe features, relative velocity
│   ├── statespace/      # DGRS sign-constrained Kalman filter/smoother
│   ├── bayesian/        # TVP Bayesian model & shrinkage priors
│   ├── propagation/     # Multi-step impulse response & transmission matrices
│   ├── scenarios/       # S1, S2, S3 Markov transition dynamics
│   ├── calibration/     # Dynamic conformal & Platt calibration
│   └── evaluation/      # BS, BSS, PR-AUC, ECE, Value Score
├── models/
│   ├── baselines/       # M0 (Persistence), M1 (Climatology)
│   ├── single_domain/   # M2 (Single-domain logistic)
│   ├── dynamic/         # M3 (ElasticNet), M4 (Dynamic AR), M5 (LightGBM)
│   └── full_4d/         # M6 (Bayesian TVP), M7 (Full 4D DLM)
├── forecasts/
│   ├── raw/
│   ├── calibrated/
│   └── archive/
├── results/
│   ├── tables/          # Auto-generated Tables 1-10
│   ├── figures/         # Auto-generated Figures 1-20
│   └── diagnostics/     # MCMC diagnostics & Kalman residuals
└── tests/               # Unit & econometric validation tests
```

---

## 3. Quickstart

```bash
# Clone and set up environment
pip install -e .

# Run validation and test suite
pytest tests/
```
