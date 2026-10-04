"""
Problem bank for coding mock interviews (auto-graded).

Interviewer usage: `python grade.py show <ID>` prints ONLY the statement for the candidate.
Each Python problem defines visible tests (shown during the interview, like an online
assessment) and hidden tests (edge cases + larger data, revealed afterwards).
SQL problems run on the practice database (visible: seed 2026) and on a re-seeded
database (hidden: seed 7) to catch hard-coded answers.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np
import pandas as pd

import solutions as ref

# ----------------------------------------------------------------------------- comparison helpers
def close(a: float, b: float, rtol=1e-6, atol=1e-9) -> bool:
    return bool(np.isclose(float(a), float(b), rtol=rtol, atol=atol))


def cmp_float(out, exp, rtol=1e-6):
    if out is None:
        return False, "returned None"
    try:
        ok = close(out, exp, rtol=rtol)
    except Exception as e:  # noqa: BLE001
        return False, f"not a number: {e}"
    return ok, "" if ok else f"expected {exp:.6f}, got {float(out):.6f}"


def cmp_frame(out, exp, key: list | None, cols: list, rtol=1e-6, order_matters=False):
    if not isinstance(out, pd.DataFrame):
        return False, f"expected a DataFrame, got {type(out).__name__}"
    o = out.copy()
    e = exp.copy()
    if key is None:  # compare on index
        o.index = o.index.astype(str)
        e.index = e.index.astype(str)
        o.columns = [str(c) for c in o.columns]
        e.columns = [str(c) for c in e.columns]
        missing = [c for c in map(str, cols) if c not in o.columns]
        if missing:
            return False, f"missing columns {missing}"
        if set(o.index) != set(e.index):
            return False, f"index mismatch: expected {sorted(e.index)[:6]}…, got {sorted(o.index)[:6]}…"
        if not order_matters:
            o = o.loc[e.index]
        elif list(o.index) != list(e.index):
            return False, "row order differs from the required order"
        for c in map(str, cols):
            if not np.allclose(o[c].astype(float).to_numpy(), e[c].astype(float).to_numpy(), rtol=rtol, atol=1e-9):
                return False, f"values differ in column '{c}'"
        return True, ""
    missing = [c for c in key + cols if c not in o.columns]
    if missing:
        return False, f"missing columns {missing}"
    if len(o) != len(e):
        return False, f"expected {len(e)} rows, got {len(o)}"
    if order_matters:
        if list(o[key].astype(str).agg("|".join, axis=1)) != list(e[key].astype(str).agg("|".join, axis=1)):
            return False, "row order differs from the required order"
    else:
        o = o.sort_values(key).reset_index(drop=True)
        e = e.sort_values(key).reset_index(drop=True)
        if not (o[key].astype(str).to_numpy() == e[key].astype(str).to_numpy()).all():
            return False, "key values differ"
    for c in cols:
        if not np.allclose(o[c].astype(float).to_numpy(), e[c].astype(float).to_numpy(), rtol=rtol, atol=1e-9):
            return False, f"values differ in column '{c}'"
    return True, ""


# ----------------------------------------------------------------------------- data generators
def scored_sample(n: int, seed: int, integer_scores: bool = False, power: float = 1.2):
    rng = np.random.default_rng(seed)
    x = rng.normal(size=n)
    p = 1 / (1 + np.exp(-(-2.2 + power * x)))
    y = rng.binomial(1, p)
    s = np.round(500 + 40 * x) if integer_scores else p
    return y, s, p


def segment_df(n: int, seed: int, with_missing: bool):
    rng = np.random.default_rng(seed)
    seg = rng.choice(["Retail", "Services", "Construction", "Healthcare"], n).astype(object)
    if with_missing:
        seg[rng.random(n) < 0.05] = None
    y = rng.binomial(1, np.where(seg == "Construction", 0.15, 0.08))
    return pd.DataFrame({"industry": seg, "bad": y})


def month_add(m: str, k: int) -> str:
    y, mo = int(m[:4]), int(m[5:7])
    t = y * 12 + mo - 1 + k
    return f"{t // 12:04d}-{t % 12 + 1:02d}-01"


def apps_perf(seed: int, n: int = 300, dup: bool = False):
    rng = np.random.default_rng(seed)
    apps = pd.DataFrame({"acct_id": np.arange(1, n + 1),
                         "obs_month": [month_add("2024-01-01", int(k)) for k in rng.integers(0, 6, n)]})
    rows = []
    for a in apps.itertuples(index=False):
        for k in range(-2, 15):  # some months before obs and beyond the 12-month window
            if rng.random() < 0.9:
                rows.append((a.acct_id, month_add(a.obs_month, k), int(rng.choice([0, 0, 0, 0, 15, 45, 75, 95]))))
    perf = pd.DataFrame(rows, columns=["acct_id", "month", "dpd"])
    if dup:
        perf = pd.concat([perf, perf.sample(frac=0.1, random_state=seed)], ignore_index=True)
    return apps, perf


def boundary_apps_perf():
    apps = pd.DataFrame({"acct_id": [1, 2, 3, 4, 5], "obs_month": ["2024-03-01"] * 5})
    perf = pd.DataFrame({
        "acct_id": [1, 2, 3, 4, 4, 1],
        "month": ["2024-03-01", "2025-03-01", "2025-04-01", "2024-08-01", "2024-08-01", "2024-04-01"],
        "dpd": [120, 95, 100, 30, 91, 10],
    })
    # acct1: 90+ only in the obs month itself → 0 ; acct2: month 12 → 1 ; acct3: month 13 → 0
    # acct4: duplicate rows in month 5, max 91 → 1 ; acct5: no rows → 0
    return apps, perf


def panel(seed: int, n: int = 400):
    rng = np.random.default_rng(seed)
    T = np.array([[.93, .06, .01, 0, 0], [.5, .25, .25, 0, 0], [.2, .1, .3, .4, 0],
                  [.1, .02, .08, .2, .6], [.03, 0, .02, .05, .9]])
    rows = []
    for a in range(1, n + 1):
        b = 0
        for t in range(int(rng.integers(3, 13))):
            rows.append((a, month_add("2025-01-01", t), b))
            b = int(rng.choice(5, p=T[b]))
    return pd.DataFrame(rows, columns=["acct_id", "month", "bucket"]).sample(frac=1, random_state=seed)


def vintage_data(seed: int, n: int = 600):
    rng = np.random.default_rng(seed)
    acc = pd.DataFrame({"acct_id": np.arange(1, n + 1),
                        "open_month": [month_add("2023-01-01", int(k)) for k in rng.integers(0, 12, n)]})
    rows = []
    for a in acc.itertuples(index=False):
        for mob in range(0, int(rng.integers(4, 16))):
            rows.append((a.acct_id, mob, int(rng.choice([0, 0, 0, 0, 0, 0, 35, 65, 95]))))
    return acc, pd.DataFrame(rows, columns=["acct_id", "mob", "dpd"])


def logit_data(seed: int, n: int = 4000):
    rng = np.random.default_rng(seed)
    X = pd.DataFrame({"util": rng.uniform(0, 1, n), "delinq": rng.poisson(0.4, n), "tenure": rng.gamma(3, 20, n)})
    z = -2.5 + 2.0 * X["util"] + 0.6 * X["delinq"] - 0.01 * X["tenure"]
    X["bad"] = rng.binomial(1, 1 / (1 + np.exp(-z)))
    return X


def grades_df(seed: int, n: int = 6000):
    rng = np.random.default_rng(seed)
    g = rng.choice(["G1", "G2", "G3", "G4", "G5"], n, p=[.25, .25, .2, .2, .1])
    base = {"G1": .01, "G2": .03, "G3": .06, "G4": .12, "G5": .25}
    pdv = np.array([base[k] for k in g]) * rng.uniform(0.8, 1.2, n)
    y = rng.binomial(1, np.clip(pdv * 1.15, 0, 1))
    return pd.DataFrame({"grade": g, "pd": pdv, "y": y})


# ----------------------------------------------------------------------------- problem definitions
@dataclass
class Test:
    name: str
    args: tuple
    kwargs: dict = field(default_factory=dict)


@dataclass
class Problem:
    pid: str
    title: str
    area: str
    language: str
    difficulty: str
    statement: str
    func_name: str = ""
    reference: Callable | None = None
    compare: Callable | None = None
    visible: Callable[[], list] = lambda: []
    hidden: Callable[[], list] = lambda: []
    order_matters: bool = False


def _frame_cmp(key, cols, order=False):
    return lambda out, exp: cmp_frame(out, exp, key, cols, order_matters=order)


PROBLEMS: dict[str, Problem] = {}


def add(p: Problem):
    PROBLEMS[p.pid] = p


add(Problem(
    "P01", "Bad rate by segment", "C1", "python", "easy",
    """Write `bad_rate_by_segment(df, seg_col, target_col) -> pd.DataFrame`.
- `df[target_col]` is 1 for bad, 0 for good. Missing segment values must be grouped as the string `"MISSING"`.
- Return columns `[seg_col, "n", "bads", "bad_rate"]`, one row per segment,
  sorted by `bad_rate` descending (ties: segment ascending), index reset.""",
    "bad_rate_by_segment", ref.bad_rate_by_segment,
    lambda o, e: cmp_frame(o, e, ["industry"], ["n", "bads", "bad_rate"], order_matters=True),
    lambda: [Test("small, no missing", (segment_df(200, 1, False), "industry", "bad"))],
    lambda: [Test("with missing segments", (segment_df(5000, 2, True), "industry", "bad")),
             Test("large", (segment_df(20000, 3, True), "industry", "bad"))],
))

add(Problem(
    "P02", "12-month bad flag after an observation point", "C1", "python", "medium",
    """Write `bad_flag_12m(apps, perf) -> pd.DataFrame`.
- `apps`: columns `acct_id`, `obs_month` (string 'YYYY-MM-01'), one row per account.
- `perf`: columns `acct_id`, `month` ('YYYY-MM-01'), `dpd`; may contain duplicate (acct_id, month) rows (use the max dpd).
- Add an int column `bad_12m` = 1 if `dpd >= 90` in any month **strictly after** `obs_month` and **within 12 months**
  (obs+1 … obs+12 inclusive), else 0. Accounts with no rows in the window get 0.
- Return all rows of `apps` in the original order (no duplication, no drops).""",
    "bad_flag_12m", ref.bad_flag_12m,
    lambda o, e: cmp_frame(o, e, ["acct_id"], ["bad_12m"], order_matters=True),
    lambda: [Test("random sample", apps_perf(11, 50))],
    lambda: [Test("window boundaries & duplicates", boundary_apps_perf()),
             Test("larger with duplicate rows", apps_perf(12, 400, dup=True))],
))

add(Problem(
    "P03", "KS statistic", "C2", "python", "easy",
    """Write `ks_statistic(y, risk_score) -> float`.
- `y`: 0/1 array (1 = bad); `risk_score`: higher = riskier.
- KS = max over all thresholds of |cumulative % of bads − cumulative % of goods|, scanning from the riskiest score down.
  Accounts with the same score must move together (no splitting ties). Return a value in [0, 1].""",
    "ks_statistic", ref.ks_statistic, cmp_float,
    lambda: [Test("continuous scores", scored_sample(1000, 5)[:2])],
    lambda: [Test("integer scores with many ties", scored_sample(8000, 6, integer_scores=True)[:2]),
             Test("weak model", scored_sample(5000, 7, power=0.2)[:2])],
))

add(Problem(
    "P04", "Gini coefficient (from AUC)", "C2", "python", "easy",
    """Write `gini_coefficient(y, risk_score) -> float`.
- `y`: 0/1 (1 = bad); `risk_score`: higher = riskier.
- Gini = 2·AUC − 1, where AUC = P(score of a random bad > score of a random good) + 0.5·P(tie).
- Must handle ties correctly. Don't loop over all bad–good pairs (n can be 100k).""",
    "gini_coefficient", ref.gini_coefficient, cmp_float,
    lambda: [Test("continuous", scored_sample(1000, 8)[:2])],
    lambda: [Test("ties", scored_sample(20000, 9, integer_scores=True)[:2]),
             Test("large", scored_sample(100000, 10)[:2])],
))

add(Problem(
    "P05", "Population Stability Index", "C2", "python", "medium",
    """Write `psi(expected, actual, n_bins=10) -> float`.
- Bin edges come from the EXPECTED sample: `np.quantile(expected, np.linspace(0, 1, n_bins + 1))`,
  keep unique values, then replace the first and last edge with -inf and +inf.
- Assign values with right-closed intervals `(a, b]` (pandas `pd.cut` default).
- Proportions per bin; floor each proportion at 1e-6 before the formula.
- PSI = Σ (A − E) · ln(A / E).""",
    "psi", ref.psi, cmp_float,
    lambda: [Test("shifted normal", (np.random.default_rng(1).normal(0, 1, 5000),
                                     np.random.default_rng(2).normal(0.3, 1, 5000)))],
    lambda: [Test("identical samples → 0", (np.random.default_rng(3).normal(size=3000),) * 2),
             Test("integer scores with ties", (np.round(np.random.default_rng(4).normal(600, 40, 8000)),
                                               np.round(np.random.default_rng(5).normal(585, 45, 6000)))),
             Test("empty current bins", (np.random.default_rng(6).normal(size=4000),
                                         np.random.default_rng(7).normal(3, 0.2, 1000)))],
))

add(Problem(
    "P06", "WoE and IV", "C2", "python", "medium",
    """Write `woe_iv(bins, y) -> (pd.DataFrame, float)`.
- `bins`: array-like of bin labels (may contain NaN → label `"MISSING"`); `y`: 0/1 (1 = bad).
- Table indexed by bin label (string) with columns `n, bads, goods, pct_good, pct_bad, woe, iv_contrib`.
- `pct_good = goods/total_goods`, `pct_bad = bads/total_bads`, each floored at 1e-6;
  `woe = ln(pct_good / pct_bad)`; `iv_contrib = (pct_good − pct_bad) · woe`; IV = Σ iv_contrib.""",
    "woe_iv", ref.woe_iv,
    lambda o, e: (lambda r1, r2: (r1[0] and r2[0], r1[1] or r2[1]))(
        cmp_frame(o[0], e[0], None, ["woe", "iv_contrib"]), cmp_float(o[1], e[1])) if isinstance(o, tuple) and len(o) == 2
        else (False, "must return (table, iv)"),
    lambda: [Test("5 bins", (pd.cut(np.random.default_rng(1).normal(size=3000), 5, labels=list("ABCDE")).astype(str),
                             np.random.default_rng(2).binomial(1, 0.2, 3000)))],
    lambda: [Test("missing labels + a bin with zero bads",
                  (pd.Series(["A"] * 50 + ["B"] * 500 + [None] * 100 + ["C"] * 400, dtype=object),
                   np.r_[np.zeros(50, int), np.random.default_rng(3).binomial(1, .1, 500),
                         np.random.default_rng(4).binomial(1, .3, 100), np.random.default_rng(5).binomial(1, .2, 400)]))],
))

add(Problem(
    "P07", "Hosmer–Lemeshow test", "C2", "python", "medium",
    """Write `hosmer_lemeshow(y, p, g=10) -> (stat, p_value)`.
- Sort by predicted PD `p` and form `g` groups of (near) equal size; break ties by original order
  (e.g., `pd.qcut(pd.Series(p).rank(method="first"), g, labels=False)`).
- stat = Σ_groups (O − n·p̄)² / (n · p̄ · (1 − p̄)), where O = observed bads, p̄ = mean PD in the group.
- p_value from a chi-square with g − 2 degrees of freedom.""",
    "hosmer_lemeshow", ref.hosmer_lemeshow,
    lambda o, e: (lambda a, b: (a[0] and b[0], a[1] or b[1]))(cmp_float(o[0], e[0]), cmp_float(o[1], e[1], rtol=1e-5))
        if isinstance(o, tuple) else (False, "must return (stat, p_value)"),
    lambda: [Test("calibrated PD", (lambda y, s, p: (y, p))(*scored_sample(3000, 21)))],
    lambda: [Test("miscalibrated PD (×1.4)", (lambda y, s, p: (y, np.clip(p * 1.4, 0, 0.99)))(*scored_sample(20000, 22))),
             Test("g = 8", (lambda y, s, p: (y, p))(*scored_sample(5000, 23)), {"g": 8})],
))

add(Problem(
    "P08", "PD back-test by grade (binomial & Jeffreys)", "C2", "python", "medium",
    """Write `grade_backtest(df) -> pd.DataFrame`. `df` has columns `grade`, `pd`, `y` (1 = default).
- One row per grade, index = grade (sorted ascending), columns in this order:
  `N` (count), `D` (defaults), `PD` (mean pd), `DR` (D/N),
  `binom_p` = P(X ≥ D) for X ~ Binomial(N, PD),
  `jeffreys_p` = CDF of Beta(D + 0.5, N − D + 0.5) evaluated at PD.""",
    "grade_backtest", ref.grade_backtest,
    lambda o, e: cmp_frame(o, e, None, ["N", "D", "PD", "DR", "binom_p", "jeffreys_p"], rtol=1e-5),
    lambda: [Test("5 grades", (grades_df(31, 3000),))],
    lambda: [Test("larger, under-estimated PDs", (grades_df(32, 30000),))],
))

add(Problem(
    "P09", "Fit a logistic regression (MLE, no regularisation)", "C3", "python", "medium",
    """Write `fit_logistic(df, features, target) -> dict`.
- Maximum-likelihood logistic regression **with an intercept and no regularisation**.
- Return `{"const": b0, "<feature>": b, ...}` for every feature (floats).
  (statsmodels `Logit` or scikit-learn `LogisticRegression(penalty=None)` both work.)""",
    "fit_logistic", ref.fit_logistic,
    lambda o, e: (all(k in o and close(o[k], v, rtol=2e-3, atol=2e-3) for k, v in e.items()),
                  "" if isinstance(o, dict) and all(k in o and close(o[k], v, rtol=2e-3, atol=2e-3) for k, v in e.items())
                  else f"expected ≈ { {k: round(v, 4) for k, v in e.items()} }") if isinstance(o, dict) else (False, "must return a dict"),
    lambda: [Test("3 features", (logit_data(41), ["util", "delinq", "tenure"], "bad"))],
    lambda: [Test("different sample", (logit_data(42, 10000), ["util", "delinq", "tenure"], "bad"))],
))

add(Problem(
    "P10", "Roll-rate matrix", "C1", "python", "hard",
    """Write `roll_rate_matrix(panel) -> pd.DataFrame`.
- `panel`: columns `acct_id`, `month` ('YYYY-MM-01'), `bucket` (int 0–4); rows are NOT sorted; monthly records have no gaps.
- For each account, a transition is (bucket in month t → bucket in the account's next month).
- Return a row-normalised matrix: index = from bucket (sorted), columns = to buckets 0,1,2,3,4 (all five, fill 0),
  values = share of transitions. Only from-buckets that have at least one transition appear.""",
    "roll_rate_matrix", ref.roll_rate_matrix,
    lambda o, e: cmp_frame(o, e, None, [0, 1, 2, 3, 4]),
    lambda: [Test("small panel", (panel(51, 60),))],
    lambda: [Test("large shuffled panel", (panel(52, 3000),))],
))

add(Problem(
    "P11", "Vintage curves", "C1", "python", "hard",
    """Write `vintage_curve(accounts, perf, mobs=(3, 6, 9, 12)) -> pd.DataFrame`.
- `accounts`: `acct_id`, `open_month` ('YYYY-MM-01'); `perf`: `acct_id`, `mob` (int, months on book), `dpd`.
- Vintage = calendar quarter of `open_month` as 'YYYY-Qn'.
- For each vintage and each m in `mobs`: share of the vintage's accounts whose FIRST dpd ≥ 60 happens at mob ≤ m.
  Denominator = all accounts in the vintage (even if not observed that long).
- Index = vintage (sorted), columns = the mobs values.""",
    "vintage_curve", ref.vintage_curve,
    lambda o, e: cmp_frame(o, e, None, list(e.columns)),
    lambda: [Test("one year of vintages", vintage_data(61, 200))],
    lambda: [Test("larger", vintage_data(62, 2000)), Test("custom mobs", vintage_data(63, 800), {"mobs": (1, 2, 6)})],
))

# ----------------------------------------------------------------------------- SQL problems
SCHEMA = """Tables (SQLite):
  accounts(acct_id, open_month 'YYYY-MM-01', product 'BCC'|'LOAN', segment 'Micro'|'Small', orig_score 0–300, credit_limit)
  monthly_perf(acct_id, month 'YYYY-MM-01', mob, balance, dpd, charged_off 0/1)   -- one row per account-month, no gaps
  scores(acct_id, snapshot 'DEV'|'CURRENT', score)
  LN(x) is available. Use date(month, '+1 month') for month arithmetic."""

SQL_STATEMENTS = {
    "S01": ("Portfolio summary by product", "easy", True,
            "For each product: number of accounts (n_accounts), average orig_score rounded to 1 dp (avg_score), "
            "total credit_limit (total_limit). Order by product."),
    "S02": ("Delinquency buckets for one month", "easy", True,
            "For month '2025-03-01': by bucket return n (account-months) and balance (sum, rounded to 2 dp). Bucket labels exactly: "
            "'B0_current' (dpd=0), 'B1_1_29', 'B2_30_59', 'B3_60_89', 'B4_90p'. Order by bucket."),
    "S03": ("Roll rate 30–59 → 60–89", "medium", True,
            "For each month m from '2025-01-01' to '2025-06-01': among accounts with 30 ≤ dpd ≤ 59 in month m that have a record "
            "in month m+1, return month, n_30_59, rolled (count with 60 ≤ dpd ≤ 89 in m+1), roll_rate = rolled/n_30_59 rounded "
            "to 4 dp. Order by month."),
    "S04": ("Bad rate after an observation point", "medium", True,
            "Population: accounts with a record in '2024-01-01' and dpd = 0 that month. Bad = any month from '2024-02-01' to "
            "'2024-10-01' inclusive with dpd ≥ 90 or charged_off = 1 (accounts with no rows in the window are good). Return segment, "
            "n_obs, bads, bad_rate (4 dp). Order by segment."),
    "S05": ("Top-2 balances per product", "medium", True,
            "For month '2025-06-01': the top 2 accounts by balance within each product (ties: lower acct_id first). Columns: "
            "product, acct_id, balance, rank_in_product. Order by product, rank_in_product."),
    "S06": ("Deciles and KS on current scores", "hard", True,
            "Use CURRENT snapshot scores. bad = 1 if the account ever had dpd ≥ 60 (0 if no performance rows). Decile with "
            "NTILE(10) over score ASC then acct_id ASC (decile 1 = lowest score). Return decile, n, bads, bad_rate, cum_bad_pct, "
            "cum_good_pct, ks — all ratios rounded to 4 dp. Order by decile."),
    "S07": ("PSI between DEV and CURRENT", "hard", False,
            "Bins on score: < 500, [500, 550), [550, 600), ≥ 600. e = DEV share per bin, a = CURRENT share per bin. "
            "Return one row with column psi = Σ (a − e)·ln(a/e), rounded to 4 dp."),
    "S08": ("Two consecutive months at 30+", "medium", False,
            "Count accounts that have at least one pair of consecutive monthly records both with dpd ≥ 30. Column: n_accounts."),
    "S09": ("2023 vintages: cumulative 90+ by MOB 6 and 12", "hard", True,
            "Accounts opened in 2023, grouped by vintage 'YYYY-Qn'. Return vintage, n_accounts, cum_90_mob6, cum_90_mob12 = share "
            "of accounts whose first dpd ≥ 90 happened at mob ≤ 6 / ≤ 12 (denominator = all accounts in the vintage), 4 dp. "
            "Order by vintage."),
    "S10": ("Anti-join", "easy", False,
            "Count accounts with NO 'CURRENT' score but at least one performance record from '2025-01-01' onwards. Column: n_accounts."),
}

# Extra hidden edge cases: applied to a copy of the re-seeded DB for specific problems
SQL_HIDDEN_MODS = {
    # 30 accounts current at the observation point disappear afterwards (closed/sold) → must stay in the population as goods
    "S04": "DELETE FROM monthly_perf WHERE month > '2024-01-01' AND acct_id IN "
           "(SELECT acct_id FROM monthly_perf WHERE month = '2024-01-01' AND dpd = 0 ORDER BY acct_id LIMIT 30);",
    # accounts with performance in 2025 but whose CURRENT score row is missing for extra accounts
    "S10": "DELETE FROM scores WHERE snapshot = 'CURRENT' AND acct_id IN "
           "(SELECT acct_id FROM scores WHERE snapshot = 'CURRENT' ORDER BY acct_id LIMIT 25);",
}

for sid, (title, diff, order, text) in SQL_STATEMENTS.items():
    add(Problem(sid, title, "C4", "sql", diff, f"{text}\n\n{SCHEMA}", order_matters=order))
