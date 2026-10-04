"""
validation_toolkit.py — credit risk model monitoring & validation metrics, from scratch.

Every function is written so you can explain it line by line in an interview.
Dependencies: numpy, pandas, scipy (statsmodels/sklearn only in the demo).

Orientation convention (the #1 source of bugs in interviews):
    risk_score: HIGHER = RISKIER (e.g., a PD).  For a credit score where higher = safer
    (FICO, SBSS, scorecard points), pass  -score  or 1 - pd.
    y / target: 1 = bad / default, 0 = good.

Run `python validation_toolkit.py` to execute the self-tests.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

EPS = 1e-6  # floor for empty bins in PSI / WoE


# ---------------------------------------------------------------------------
# 1. Discrimination: KS, AUC, Gini, decile (gains) table
# ---------------------------------------------------------------------------
def ks_statistic(y, risk_score) -> float:
    """KS = max over thresholds of |cum% bads − cum% goods|, scanning riskiest first.

    Ties are grouped (all accounts with the same score move together),
    which makes the result equal to scipy.stats.ks_2samp on bads vs goods.
    """
    df = pd.DataFrame({"s": np.asarray(risk_score, dtype=float), "y": np.asarray(y, dtype=int)})
    g = df.groupby("s")["y"].agg(bads="sum", n="count").sort_index(ascending=False)
    goods = g["n"] - g["bads"]
    cum_bad = g["bads"].cumsum() / g["bads"].sum()
    cum_good = goods.cumsum() / goods.sum()
    return float((cum_bad - cum_good).abs().max())


def auc_score(y, risk_score) -> float:
    """AUC via the Mann–Whitney rank formula (handles ties with average ranks).

    AUC = P(score of a random bad > score of a random good) + 0.5 * P(tie).
    """
    y = np.asarray(y, dtype=int)
    s = np.asarray(risk_score, dtype=float)
    ranks = stats.rankdata(s)  # average ranks for ties
    n_bad = y.sum()
    n_good = len(y) - n_bad
    if n_bad == 0 or n_good == 0:
        raise ValueError("Need both bads and goods to compute AUC.")
    rank_sum_bad = ranks[y == 1].sum()
    return float((rank_sum_bad - n_bad * (n_bad + 1) / 2) / (n_bad * n_good))


def gini_score(y, risk_score) -> float:
    """Gini (Accuracy Ratio, Somers' D) = 2·AUC − 1."""
    return 2 * auc_score(y, risk_score) - 1


def gains_table(y, risk_score, n_bins: int = 10) -> pd.DataFrame:
    """Decile / gains table, riskiest bin first. Columns interviewers expect to see."""
    df = pd.DataFrame({"s": np.asarray(risk_score, dtype=float), "y": np.asarray(y, dtype=int)})
    # rank first so ties don't break qcut; bin 1 = riskiest
    df["bin"] = pd.qcut(df["s"].rank(method="first", ascending=False), n_bins, labels=range(1, n_bins + 1))
    t = df.groupby("bin", observed=True).agg(
        n=("y", "size"), bads=("y", "sum"), min_score=("s", "min"), max_score=("s", "max")
    )
    t["goods"] = t["n"] - t["bads"]
    t["bad_rate"] = t["bads"] / t["n"]
    t["cum_bad_pct"] = t["bads"].cumsum() / t["bads"].sum()
    t["cum_good_pct"] = t["goods"].cumsum() / t["goods"].sum()
    t["ks"] = (t["cum_bad_pct"] - t["cum_good_pct"]).abs()
    t["lift"] = t["bad_rate"] / (t["bads"].sum() / t["n"].sum())
    return t


def rank_order_breaks(table: pd.DataFrame, col: str = "bad_rate") -> int:
    """Number of breaks in monotonic (non-increasing, riskiest-first) bad rates."""
    br = table[col].to_numpy()
    return int(np.sum(np.diff(br) > 0))


def bootstrap_gini_ci(y, risk_score, n_boot: int = 300, alpha: float = 0.05, seed: int = 7):
    """Percentile bootstrap CI for Gini — use it before calling a Gini drop 'real'."""
    rng = np.random.default_rng(seed)
    y = np.asarray(y, dtype=int)
    s = np.asarray(risk_score, dtype=float)
    n = len(y)
    ginis = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        if y[idx].sum() in (0, n):
            continue
        ginis.append(gini_score(y[idx], s[idx]))
    lo, hi = np.quantile(ginis, [alpha / 2, 1 - alpha / 2])
    return float(lo), float(hi)


def _midrank(x: np.ndarray) -> np.ndarray:
    order = np.argsort(x)
    z = x[order]
    n = len(x)
    t = np.zeros(n)
    i = 0
    while i < n:
        j = i
        while j < n and z[j] == z[i]:
            j += 1
        t[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    out = np.empty(n)
    out[order] = t
    return out


def delong_test(y, risk_score_a, risk_score_b):
    """DeLong test for two correlated AUCs on the SAME sample (champion vs challenger).

    Returns (auc_a, auc_b, z, two-sided p-value).
    """
    y = np.asarray(y, dtype=int)
    order = np.argsort(-y, kind="mergesort")  # bads (positives) first
    preds = np.vstack([np.asarray(risk_score_a, float), np.asarray(risk_score_b, float)])[:, order]
    m = int(y.sum())
    n = preds.shape[1] - m
    pos, neg = preds[:, :m], preds[:, m:]
    tx = np.vstack([_midrank(pos[r]) for r in range(2)])
    ty = np.vstack([_midrank(neg[r]) for r in range(2)])
    tz = np.vstack([_midrank(preds[r]) for r in range(2)])
    aucs = tz[:, :m].sum(axis=1) / m / n - (m + 1.0) / 2.0 / n
    v01 = (tz[:, :m] - tx) / n
    v10 = 1.0 - (tz[:, m:] - ty) / m
    cov = np.cov(v01) / m + np.cov(v10) / n
    diff_var = cov[0, 0] + cov[1, 1] - 2 * cov[0, 1]
    if diff_var <= 0:  # identical rankings → no evidence of a difference
        return float(aucs[0]), float(aucs[1]), 0.0, 1.0
    z = (aucs[0] - aucs[1]) / np.sqrt(diff_var)
    p = 2 * stats.norm.sf(abs(z))
    return float(aucs[0]), float(aucs[1]), float(z), float(p)


# ---------------------------------------------------------------------------
# 2. Stability: PSI / CSI
# ---------------------------------------------------------------------------
def psi(expected, actual, n_bins: int = 10, bin_edges=None, return_table: bool = False):
    """Population Stability Index = Σ (A% − E%) · ln(A% / E%).

    Bins are defined on the EXPECTED (reference / development) distribution.
    Rule of thumb: < 0.10 stable · 0.10–0.25 monitor · > 0.25 significant shift.
    """
    expected = np.asarray(expected, dtype=float)
    actual = np.asarray(actual, dtype=float)
    if bin_edges is None:
        qs = np.unique(np.quantile(expected, np.linspace(0, 1, n_bins + 1)))
        bin_edges = qs.copy()
    edges = np.asarray(bin_edges, dtype=float).copy()
    edges[0], edges[-1] = -np.inf, np.inf
    e_cnt = np.histogram(expected, edges)[0]
    a_cnt = np.histogram(actual, edges)[0]
    e_pct = np.maximum(e_cnt / e_cnt.sum(), EPS)
    a_pct = np.maximum(a_cnt / a_cnt.sum(), EPS)
    contrib = (a_pct - e_pct) * np.log(a_pct / e_pct)
    value = float(contrib.sum())
    if not return_table:
        return value
    table = pd.DataFrame(
        {"bin_low": edges[:-1], "bin_high": edges[1:], "expected_pct": e_pct, "actual_pct": a_pct, "psi_contrib": contrib}
    )
    return value, table


def csi_categorical(expected, actual) -> tuple[float, pd.DataFrame]:
    """Characteristic Stability Index for a categorical/binned variable (same formula as PSI)."""
    e = pd.Series(expected).astype(str).value_counts(normalize=True)
    a = pd.Series(actual).astype(str).value_counts(normalize=True)
    t = pd.concat([e.rename("expected_pct"), a.rename("actual_pct")], axis=1).fillna(0.0).clip(lower=EPS)
    t["csi_contrib"] = (t["actual_pct"] - t["expected_pct"]) * np.log(t["actual_pct"] / t["expected_pct"])
    return float(t["csi_contrib"].sum()), t


# ---------------------------------------------------------------------------
# 3. Characteristic analysis: binning, WoE, IV
# ---------------------------------------------------------------------------
def quantile_bins(x: pd.Series, n_bins: int = 5) -> np.ndarray:
    """Bin edges from quantiles of non-missing values (edges are de-duplicated)."""
    x = pd.Series(x).dropna()
    edges = np.unique(np.quantile(x, np.linspace(0, 1, n_bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    return edges


def apply_bins(x: pd.Series, edges: np.ndarray) -> pd.Series:
    """Assign bins; missing values get their own 'MISSING' bin (never drop them silently)."""
    x = pd.Series(x)
    binned = pd.cut(x, edges, include_lowest=True).astype(str)
    return binned.where(x.notna(), "MISSING")


def woe_iv(binned: pd.Series, y, convention: str = "good_over_bad"):
    """Weight of Evidence and Information Value.

    convention='good_over_bad' (Siddiqi): WoE = ln(%Good / %Bad)  -> higher WoE = SAFER.
        With a logistic regression predicting BAD, WoE coefficients come out NEGATIVE.
    convention='bad_over_good':          WoE = ln(%Bad / %Good)  -> coefficients positive.
    IV = Σ (%Good − %Bad) · ln(%Good / %Bad)  (identical under both conventions).
    IV guide: <0.02 useless · 0.02–0.1 weak · 0.1–0.3 medium · 0.3–0.5 strong · >0.5 suspicious.
    """
    df = pd.DataFrame({"bin": pd.Series(binned).astype(str).to_numpy(), "y": np.asarray(y, dtype=int)})
    t = df.groupby("bin").agg(n=("y", "size"), bads=("y", "sum"))
    t["goods"] = t["n"] - t["bads"]
    pct_good = np.maximum(t["goods"] / t["goods"].sum(), EPS)
    pct_bad = np.maximum(t["bads"] / t["bads"].sum(), EPS)
    t["pct_good"], t["pct_bad"] = pct_good, pct_bad
    t["bad_rate"] = t["bads"] / t["n"]
    woe = np.log(pct_good / pct_bad)
    t["woe"] = woe if convention == "good_over_bad" else -woe
    t["iv_contrib"] = (pct_good - pct_bad) * np.log(pct_good / pct_bad)
    return t, float(t["iv_contrib"].sum())


# ---------------------------------------------------------------------------
# 4. Calibration: HL, binomial, Jeffreys, normal test, Brier, calibration table
# ---------------------------------------------------------------------------
def calibration_table(y, pd_pred, n_bins: int = 10) -> pd.DataFrame:
    df = pd.DataFrame({"y": np.asarray(y, dtype=int), "pd": np.asarray(pd_pred, dtype=float)})
    df["bin"] = pd.qcut(df["pd"].rank(method="first"), n_bins, labels=range(1, n_bins + 1))
    t = df.groupby("bin", observed=True).agg(n=("y", "size"), defaults=("y", "sum"), avg_pd=("pd", "mean"))
    t["observed_dr"] = t["defaults"] / t["n"]
    t["expected_defaults"] = t["avg_pd"] * t["n"]
    return t


def hosmer_lemeshow(y, pd_pred, n_bins: int = 10, dof_adjust: int = 2):
    """HL = Σ_g (O_g − E_g)² / (n_g · p̄_g · (1 − p̄_g)), ~ χ² with (g − 2) dof on the dev sample.

    On an independent validation sample some teams use g dof (dof_adjust=0).
    Large samples make HL reject almost always — read it with the calibration table.
    """
    t = calibration_table(y, pd_pred, n_bins)
    num = (t["defaults"] - t["expected_defaults"]) ** 2
    den = t["n"] * t["avg_pd"] * (1 - t["avg_pd"])
    hl = float((num / den).sum())
    dof = len(t) - dof_adjust
    return hl, float(stats.chi2.sf(hl, dof)), t


def grade_calibration_tests(df: pd.DataFrame, grade_col: str, pd_col: str, y_col: str) -> pd.DataFrame:
    """Per-grade PD back-test: one-sided tests of H0 'PD is adequate' vs H1 'PD is too low'.

    - binomial p = P(X ≥ D | N, PD)  (assumes independent defaults → too strict when defaults correlate)
    - Jeffreys p = Beta CDF at PD with a = D + 0.5, b = N − D + 0.5  (ECB IRB validation reporting)
    - normal-approx z = (DR − PD) / sqrt(PD(1−PD)/N)
    Small p (< 0.05) → PD likely UNDER-estimates risk for that grade.
    """
    g = df.groupby(grade_col, observed=True).agg(N=(y_col, "size"), D=(y_col, "sum"), PD=(pd_col, "mean"))
    g["DR"] = g["D"] / g["N"]
    g["binomial_p"] = stats.binom.sf(g["D"] - 1, g["N"], g["PD"])
    g["jeffreys_p"] = stats.beta.cdf(g["PD"], g["D"] + 0.5, g["N"] - g["D"] + 0.5)
    g["z"] = (g["DR"] - g["PD"]) / np.sqrt(g["PD"] * (1 - g["PD"]) / g["N"])
    g["result"] = np.where(g["jeffreys_p"] < 0.01, "RED", np.where(g["jeffreys_p"] < 0.05, "AMBER", "GREEN"))
    return g


def brier_score(y, pd_pred) -> float:
    y = np.asarray(y, dtype=float)
    p = np.asarray(pd_pred, dtype=float)
    return float(np.mean((p - y) ** 2))


# ---------------------------------------------------------------------------
# 5. Multicollinearity
# ---------------------------------------------------------------------------
def vif(df: pd.DataFrame) -> pd.Series:
    """VIF_j = 1 / (1 − R²_j), regressing x_j on all other columns (with intercept).

    Guide: < 5 fine · 5–10 investigate · > 10 serious.
    """
    X = df.to_numpy(dtype=float)
    out = {}
    for j, col in enumerate(df.columns):
        yj = X[:, j]
        others = np.delete(X, j, axis=1)
        A = np.column_stack([np.ones(len(yj)), others])
        beta, *_ = np.linalg.lstsq(A, yj, rcond=None)
        resid = yj - A @ beta
        r2 = 1 - resid.var() / yj.var()
        out[col] = np.inf if r2 >= 1 else 1 / (1 - r2)
    return pd.Series(out, name="VIF")


# ---------------------------------------------------------------------------
# 6. Portfolio analytics: roll rates, vintages
# ---------------------------------------------------------------------------
def roll_rate_matrix(panel: pd.DataFrame, id_col: str, month_col: str, bucket_col: str) -> pd.DataFrame:
    """Month-on-month transition matrix of delinquency buckets (row-normalised)."""
    p = panel.sort_values([id_col, month_col]).copy()
    p["next_bucket"] = p.groupby(id_col)[bucket_col].shift(-1)
    p = p.dropna(subset=["next_bucket"])
    return pd.crosstab(p[bucket_col], p["next_bucket"], normalize="index")


def vintage_curves(panel: pd.DataFrame, id_col: str, cohort_col: str, mob_col: str, bad_flag_col: str) -> pd.DataFrame:
    """Cumulative bad rate by months-on-book for each origination cohort."""
    first_bad = panel[panel[bad_flag_col] == 1].groupby(id_col)[mob_col].min()
    cohort_size = panel.groupby(cohort_col)[id_col].nunique()
    acct_cohort = panel.groupby(id_col)[cohort_col].first()
    fb = pd.DataFrame({"cohort": acct_cohort.loc[first_bad.index], "mob": first_bad})
    counts = fb.groupby(["cohort", "mob"]).size().unstack(fill_value=0).cumsum(axis=1)
    return counts.div(cohort_size, axis=0)


# ---------------------------------------------------------------------------
# 7. RAG helper
# ---------------------------------------------------------------------------
def rag(value: float, amber: float, red: float, higher_is_worse: bool = True) -> str:
    if higher_is_worse:
        return "RED" if value > red else "AMBER" if value > amber else "GREEN"
    return "RED" if value < red else "AMBER" if value < amber else "GREEN"


# ---------------------------------------------------------------------------
# Self-tests (run: python validation_toolkit.py)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    n = 5000
    x = rng.normal(size=n)
    p = 1 / (1 + np.exp(-(-2.5 + 1.2 * x)))
    y = rng.binomial(1, p)

    ks_ours = ks_statistic(y, p)
    ks_scipy = stats.ks_2samp(p[y == 1], p[y == 0]).statistic
    assert abs(ks_ours - ks_scipy) < 1e-9, (ks_ours, ks_scipy)

    try:
        from sklearn.metrics import roc_auc_score

        assert abs(auc_score(y, p) - roc_auc_score(y, p)) < 1e-12
    except ImportError:
        pass

    # Orientation check: a 'credit score' (higher = safer) must be negated
    credit_score = 600 - 50 * np.log(p / (1 - p))
    assert abs(auc_score(y, -credit_score) - auc_score(y, p)) < 1e-12

    # PSI of a distribution against itself is 0; against a shifted one is > 0
    assert psi(x, x) < 1e-12 and psi(x, x + 0.5) > 0.1

    # VIF: collinear column blows up
    X = pd.DataFrame({"a": x, "b": rng.normal(size=n)})
    X["c"] = X["a"] * 0.95 + rng.normal(scale=0.1, size=n)
    assert vif(X)["c"] > 10

    # DeLong: identical scores → z = 0
    a1, a2, z, pval = delong_test(y, p, p + 1e-12 * rng.normal(size=n))
    assert abs(a1 - a2) < 1e-6

    print(f"All self-tests passed. KS={ks_ours:.4f}  AUC={auc_score(y, p):.4f}  Gini={gini_score(y, p):.4f}")
