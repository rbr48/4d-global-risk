"""
4D-MGRFF Master Dissertation Monograph Compiler
Assembles Front Matter, Chapters 1-11, Appendices, and References into
thesis/DISSERTATION_MASTER_MANUSCRIPT.md.
"""

import os

FRONT_MATTER = r"""# A Four-Dimensional Probabilistic Framework for Modelling the Evolution, Interaction, and Propagation of Multidisciplinary Global Risks Through Time

**A Dissertation Submitted in Partial Fulfillment of the Requirements for the Degree of Doctor of Philosophy in Advanced Quantitative Risk Analysis and Econometrics**

**Author**: Doctoral Researcher in Advanced Quantitative Risk Analysis  
**Institutional Affiliation**: Izhaan Intellect Advanced Research Institute  
**Date of Submission**: September 2026  
**Academic Standard**: Probabilistic, Bayesian, Dynamic Systems, and Out-of-Sample Validated  

---

## Abstract
Global risks do not occur in disciplinary silos. Geopolitical friction triggers energy benchmark shocks; energy shocks feed inflation expectations and sovereign yield spreads; credit tightness constrains policy maneuverability; elevated information velocity amplifies social panic; and extreme climatic anomalies compound structural stress. 

This dissertation develops and empirically evaluates the **4D Multidisciplinary Global Risk Forecasting Framework (4D-MGRFF)**. The framework conceptualizes global risk across four structural dimensions: **State** ($S_t$), **Interaction** ($A_t$), **Propagation** ($\Pi_h$), and **Time** ($t+h$). The empirical architecture assembles a versioned, timestamped panel combining high-frequency media data (GDELT), political violence telemetry (ACLED), financial and commodity benchmarks, market-implied high-frequency macroeconomic proxies, policy signals, and observational climate indicators.

To guarantee computational tractability and empirical rigor across ~3,650 daily rolling origins, the methodology defines a **Two-Tier Inference Protocol**: daily rolling estimation uses analytical Dynamic Linear Models (Kalman Filter and Fixed-Interval Smoother) for all empirical evaluations, while specifying a quarterly checkpoint Bayesian MCMC validation layer for production deployment. Latent factor states are identified via strict sign constraints ($\lambda_{\text{stress}} > 0$) to eliminate rolling polarity inversions.

Evaluation uses strictly proper scoring rules (Brier Score, Brier Skill Score against climatology, Logarithmic Score, and CRPS), Precision-Recall AUC for rare multi-domain escalation events ($S_3$), reliability curves, Expected Calibration Error (ECE), and a decision-theoretic Relative Value Score ($V$). The dissertation enforces explicit preregistered falsification criteria, ensuring that null results are preserved as valid scientific findings.

**Keywords**: four-dimensional forecasting; probabilistic forecasting; Bayesian state-space models; dynamic systems; global risk; geopolitical risk; shock propagation; calibration; decision utility; systemic volatility.

---

## Table of Contents
* **Chapter 1**: Introduction
* **Chapter 2**: Literature Review
* **Chapter 3**: The Four-Dimensional Theoretical Framework
* **Chapter 4**: Data Architecture and Point-in-Time Measurement
* **Chapter 5**: Methodology and Two-Tier Inference Architecture
* **Chapter 6**: Empirical Results and Model Benchmark Evaluation
* **Chapter 7**: Dynamic Risk Propagation Analysis
* **Chapter 8**: Operationalized Scenario and Early-Warning Dynamics
* **Chapter 9**: Robustness, Placebo, and Falsification Results
* **Chapter 10**: Discussion and Practical Decision Utility
* **Chapter 11**: Conclusion and Scientific Limits
* **Appendix A**: Mathematical Derivations and Econometric Proofs
* **Appendix B**: Data Codebook and Provenance Dictionary

---

## List of Figures
* **Figure 4**: Dynamic Global Risk State (DGRS) Latent Factor Trajectory with 90% Credible Intervals
* **Figure 7**: Cross-Domain Dynamic Propagation Heatmaps ($\Pi_1$ vs $\Pi_7$)
* **Figure 11**: Out-of-Sample Model Ladder Verification Bar Charts (Horizon = 1 Day)

---

## List of Tables
* **Table 5**: Out-of-Sample Forecast Performance Across Model Ladder (M0 to M7) and Horizons
* **Table 7.1 / 8**: Cross-Domain Dynamic Propagation Matrices ($\Pi_1$ vs $\Pi_7$)
* **Table 8.1**: Empirical $3 \times 3$ Markov Scenario Transition Matrix
* **Table 8.2**: Early-Warning Indicator Sensitivity Ranking ($h=3$ Days)
* **Table 9.1**: Audit of the 10 Preregistered Falsification Criteria
* **Table 9.2**: Event Threshold Sensitivity Analysis (80th to 95th Percentiles)
* **Table 9.3**: Training Window Sensitivity (Expanding vs Fixed Rolling)
* **Table B.1**: Empirical Data Provenance and Ticker Codebook

---

## Glossary of Mathematical Notation
* $S_t \in \mathbb{R}^D$: Latent multidisciplinary global-risk state vector across 5 domains.
* $F_t \in \mathbb{R}$: Dynamic Global Risk State (DGRS) scalar common factor.
* $X_t \in \mathbb{R}^p$: Vector of observed high-frequency domain indicators.
* $A_t \in \mathbb{R}^{D \times D}$: Time-varying cross-domain interaction matrix.
* $\Pi_h \in \mathbb{R}^{p \times p}$: Horizon-specific dynamic shock propagation matrix.
* $h \in \{1, 3, 7, 14\}$: Forecast horizons in calendar days.
* $\mathcal{I}_t$: Point-in-time information set strictly available at origin $t$.
* $\lambda_{\text{stress}} > 0$: Strict sign-identification anchor on factor loadings.
* $\widetilde{IV}_{d,t}$: Salience-normalized robust information velocity.
* $\text{BS}, \text{BSS}$: Brier Score and Brier Skill Score relative to climatology.
* $V(\alpha)$: Richardson / Murphy-Winkler Relative Decision Value under cost-loss ratio $\alpha = C/L$.

---
"""

CHAPTER_FILES = [
    "thesis/chapter_01_introduction.md",
    "thesis/chapter_02_literature_review.md",
    "thesis/chapter_03_theoretical_framework.md",
    "thesis/chapter_04_data_and_measurement.md",
    "thesis/chapter_05_methodology.md",
    "thesis/chapter_06_empirical_results.md",
    "thesis/chapter_07_propagation_analysis.md",
    "thesis/chapter_08_scenario_dynamics.md",
    "thesis/chapter_09_robustness_and_falsification.md",
    "thesis/chapter_10_discussion_and_policy_utility.md",
    "thesis/chapter_11_conclusion.md",
    "thesis/appendix_a_mathematical_proofs.md",
    "thesis/appendix_b_data_codebook.md"
]


def compile_manuscript(output_path: str = "thesis/DISSERTATION_MASTER_MANUSCRIPT.md"):
    print("Compiling Master Dissertation Monograph...")
    full_text = [FRONT_MATTER.strip(), "\n\n---\n\n"]
    
    for ch_path in CHAPTER_FILES:
        if os.path.exists(ch_path):
            with open(ch_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                full_text.append(content)
                full_text.append("\n\n---\n\n")
            print(f"  + Appended {ch_path}")
        else:
            print(f"  ! Warning: Missing {ch_path}")
            
    monograph = "".join(full_text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(monograph)
        
    size_kb = os.path.getsize(output_path) / 1024.0
    print(f"\nSUCCESS: Compiled {output_path} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    compile_manuscript()
