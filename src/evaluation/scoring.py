"""
4D-MGRFF Forecast Verification & Scoring Engine
Strictly proper scoring rules, Brier Skill Score, rare-event metrics, and decision utility.
Natively implemented in NumPy / SciPy without external heavy dependencies.
"""

from typing import Dict, List, Optional, Tuple
import numpy as np


def compute_brier_score(probabilities: np.ndarray, outcomes: np.ndarray) -> float:
    """
    Brier Score: BS = (1/N) * sum((p_i - y_i)^2).
    Lower is better. Range: [0, 1].
    """
    p = np.asarray(probabilities, dtype=float)
    y = np.asarray(outcomes, dtype=float)
    return float(np.mean((p - y) ** 2))


def compute_brier_skill_score(
    probabilities: np.ndarray,
    outcomes: np.ndarray,
    climatology_prob: Optional[float] = None
) -> float:
    """
    Brier Skill Score (BSS) relative to unconditional base rate / Climatology.
    BSS = 1 - (BS_model / BS_climatology).
    Positive (>0) indicates genuine skill over historical base rate.
    Zero (0) indicates skill no better than predicting base rate.
    Negative (<0) indicates inferior performance to naive baseline.
    """
    y = np.asarray(outcomes, dtype=float)
    bs_model = compute_brier_score(probabilities, y)
    
    if climatology_prob is None:
        climatology_prob = float(np.mean(y))
        
    bs_clim = float(np.mean((climatology_prob - y) ** 2))
    
    if bs_clim < 1e-12:
        return 0.0  # Degenerate baseline (no variance)
        
    return float(1.0 - (bs_model / bs_clim))


def compute_logarithmic_score(
    probabilities: np.ndarray,
    outcomes: np.ndarray,
    epsilon: float = 1e-15
) -> float:
    """
    Logarithmic Score (Cross-Entropy):
    LS = - (1/N) * sum(y * ln(p) + (1 - y) * ln(1 - p)).
    Lower is better.
    """
    p = np.clip(np.asarray(probabilities, dtype=float), epsilon, 1.0 - epsilon)
    y = np.asarray(outcomes, dtype=float)
    return float(-np.mean(y * np.log(p) + (1.0 - y) * np.log(1.0 - p)))


def compute_expected_calibration_error(
    probabilities: np.ndarray,
    outcomes: np.ndarray,
    num_bins: int = 10
) -> Tuple[float, Dict[str, np.ndarray]]:
    """
    Expected Calibration Error (ECE):
    ECE = sum( (n_b / N) * |acc_b - conf_b| ).
    Also returns bin edges, accuracies, and confidences for reliability diagrams.
    """
    p = np.asarray(probabilities, dtype=float)
    y = np.asarray(outcomes, dtype=float)
    N = len(p)
    
    bin_edges = np.linspace(0.0, 1.0, num_bins + 1)
    ece = 0.0
    
    bin_confs = []
    bin_accs = []
    bin_counts = []
    
    for i in range(num_bins):
        low, high = bin_edges[i], bin_edges[i + 1]
        mask = (p >= low) & (p <= high if i == num_bins - 1 else p < high)
        n_b = np.sum(mask)
        
        if n_b > 0:
            conf_b = float(np.mean(p[mask]))
            acc_b = float(np.mean(y[mask]))
            ece += (n_b / N) * abs(acc_b - conf_b)
            bin_confs.append(conf_b)
            bin_accs.append(acc_b)
            bin_counts.append(n_b)
        else:
            bin_confs.append((low + high) / 2.0)
            bin_accs.append(0.0)
            bin_counts.append(0)
            
    diagram_data = {
        "bin_edges": bin_edges,
        "bin_confs": np.array(bin_confs),
        "bin_accs": np.array(bin_accs),
        "bin_counts": np.array(bin_counts)
    }
    return float(ece), diagram_data


def compute_pr_auc(probabilities: np.ndarray, outcomes: np.ndarray) -> float:
    """
    Precision-Recall Area Under Curve (PR-AUC) implemented in pure NumPy.
    Mandatory metric for evaluating severe class imbalance (e.g. rare escalation S3).
    """
    p = np.asarray(probabilities, dtype=float)
    y = np.asarray(outcomes, dtype=int)
    
    n_pos = np.sum(y == 1)
    if n_pos == 0 or n_pos == len(y):
        return 0.0
        
    desc_idx = np.argsort(-p)
    y_sorted = y[desc_idx]
    
    tp = np.cumsum(y_sorted)
    fp = np.cumsum(1 - y_sorted)
    recalls = tp / n_pos
    precisions = tp / (tp + fp)
    
    recalls = np.concatenate(([0.0], recalls))
    precisions = np.concatenate(([precisions[0]], precisions))
    
    # Trapezoidal rule
    area = np.sum((recalls[1:] - recalls[:-1]) * (precisions[1:] + precisions[:-1]) / 2.0)
    return float(area)


def compute_relative_value_score(
    probabilities: np.ndarray,
    outcomes: np.ndarray,
    cost_loss_ratio: float,
    threshold: Optional[float] = None
) -> float:
    """
    Richardson / Murphy-Winkler Relative Value Score V(alpha).
    Demonstrates decision utility for a decision maker with cost-loss ratio alpha = C / L.
    
    V(alpha) = (Expense_climatology - Expense_model) / (Expense_climatology - Expense_perfect).
    """
    p = np.asarray(probabilities, dtype=float)
    y = np.asarray(outcomes, dtype=float)
    alpha = float(cost_loss_ratio)
    
    p_star = threshold if threshold is not None else alpha
    actions = (p >= p_star).astype(float)
    base_rate = float(np.mean(y))
    
    expense_model = float(np.mean(actions * alpha + (1.0 - actions) * y * 1.0))
    expense_perfect = base_rate * alpha
    expense_clim = min(alpha, base_rate)
    
    denom = expense_clim - expense_perfect
    if abs(denom) < 1e-12:
        return 0.0
        
    val_score = (expense_clim - expense_model) / denom
    return float(val_score)
