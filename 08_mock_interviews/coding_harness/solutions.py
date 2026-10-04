"""
Reference solutions for the coding-interview problem bank.

⚠️  Interviewer material — don't read this before a coding mock; it contains the answers.
    After an interview, `python grade.py solution <ID>` prints the relevant one.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats

EPS = 1e-6


# ----------------------------------------------------------------------------- C1 · pandas
def bad_rate_by_segment(df: pd.DataFrame, seg_col: str, target_col: str) -> pd.DataFrame:
    seg = df[seg_col].astype(object).where(df[seg_col].notna(), "MISSING").astype(str)
    out = (pd.DataFrame({seg_col: seg, "y": df[target_col].astype(int)})
           .groupby(seg_col, as_index=False)
           .agg(n=("y", "size"), bads=("y", "sum")))
    out["bad_rate"] = out["bads"] / out["n"]
    return out.sort_values(["bad_rate", seg_col], ascending=[False, True]).reset_index(drop=True)


def _month_index(m: pd.Series) -> pd.Series:
    d = pd.to_datetime(m)
    return d.dt.year * 12 + d.dt.month


def bad_flag_12m(apps: pd.DataFrame, perf: pd.DataFrame) -> pd.DataFrame:
    a = apps.copy()
    a["_obs"] = _month_index(a["obs_month"])
    p = perf.groupby(["acct_id", "month"], as_index=False)["dpd"].max()   # de-duplicate
    p["_m"] = _month_index(p["month"])
    j = p.merge(a[["acct_id", "_obs"]], on="acct_id", how="inner")
    inwin = j[(j["_m"] > j["_obs"]) & (j["_m"] <= j["_obs"] + 12)]
    bad = inwin.assign(b=(inwin["dpd"] >= 90).astype(int)).groupby("acct_id")["b"].max()
    out = apps.copy()
    out["bad_12m"] = out["acct_id"].map(bad).fillna(0).astype(int)
    return out


# ----------------------------------------------------------------------------- C2 · metrics
def ks_statistic(y, risk_score) -> float:
    d = pd.DataFrame({"s": np.asarray(risk_score, float), "y": np.asarray(y, int)})
    g = d.groupby("s")["y"].agg(["sum", "count"]).sort_index(ascending=False)
    goods = g["count"] - g["sum"]
    return float((g["sum"].cumsum() / g["sum"].sum() - goods.cumsum() / goods.sum()).abs().max())


def gini_coefficient(y, risk_score) -> float:
    y = np.asarray(y, int)
    r = stats.rankdata(np.asarray(risk_score, float))
    nb, ng = y.sum(), len(y) - y.sum()
    auc = (r[y == 1].sum() - nb * (nb + 1) / 2) / (nb * ng)
    return float(2 * auc - 1)


def psi(expected, actual, n_bins: int = 10) -> float:
    e = np.asarray(expected, float)
    a = np.asarray(actual, float)
    edges = np.unique(np.quantile(e, np.linspace(0, 1, n_bins + 1)))
    edges[0], edges[-1] = -np.inf, np.inf
    nb = len(edges) - 1
    ec = np.bincount(pd.cut(e, edges, right=True, labels=False), minlength=nb)
    ac = np.bincount(pd.cut(a, edges, right=True, labels=False), minlength=nb)
    ep = np.maximum(ec / ec.sum(), EPS)
    ap = np.maximum(ac / ac.sum(), EPS)
    return float(np.sum((ap - ep) * np.log(ap / ep)))


def woe_iv(bins, y):
    b = pd.Series(bins).astype(object)
    b = b.where(b.notna(), "MISSING").astype(str)
    t = pd.DataFrame({"bin": b.to_numpy(), "y": np.asarray(y, int)}).groupby("bin").agg(
        n=("y", "size"), bads=("y", "sum"))
    t["goods"] = t["n"] - t["bads"]
    t["pct_good"] = np.maximum(t["goods"] / t["goods"].sum(), EPS)
    t["pct_bad"] = np.maximum(t["bads"] / t["bads"].sum(), EPS)
    t["woe"] = np.log(t["pct_good"] / t["pct_bad"])
    t["iv_contrib"] = (t["pct_good"] - t["pct_bad"]) * t["woe"]
    return t, float(t["iv_contrib"].sum())


def hosmer_lemeshow(y, p, g: int = 10):
    d = pd.DataFrame({"y": np.asarray(y, int), "p": np.asarray(p, float)})
    d["grp"] = pd.qcut(d["p"].rank(method="first"), g, labels=False)
    t = d.groupby("grp").agg(n=("y", "size"), O=("y", "sum"), pbar=("p", "mean"))
    stat = float((((t["O"] - t["n"] * t["pbar"]) ** 2) / (t["n"] * t["pbar"] * (1 - t["pbar"]))).sum())
    return stat, float(stats.chi2.sf(stat, g - 2))


def grade_backtest(df: pd.DataFrame) -> pd.DataFrame:
    t = df.groupby("grade").agg(N=("y", "size"), D=("y", "sum"), PD=("pd", "mean")).sort_index()
    t["DR"] = t["D"] / t["N"]
    t["binom_p"] = stats.binom.sf(t["D"] - 1, t["N"], t["PD"])
    t["jeffreys_p"] = stats.beta.cdf(t["PD"], t["D"] + 0.5, t["N"] - t["D"] + 0.5)
    return t[["N", "D", "PD", "DR", "binom_p", "jeffreys_p"]]


# ----------------------------------------------------------------------------- C3 · modeling
def fit_logistic(df: pd.DataFrame, features: list, target: str) -> dict:
    import statsmodels.api as sm
    m = sm.Logit(df[target].astype(float), sm.add_constant(df[features].astype(float))).fit(disp=0)
    return {k: float(v) for k, v in m.params.items()}


# ----------------------------------------------------------------------------- C1/C2 · portfolio analytics
def roll_rate_matrix(panel: pd.DataFrame) -> pd.DataFrame:
    p = panel.sort_values(["acct_id", "month"]).copy()
    p["next"] = p.groupby("acct_id")["bucket"].shift(-1)
    p = p.dropna(subset=["next"])
    p["next"] = p["next"].astype(int)
    m = pd.crosstab(p["bucket"], p["next"], normalize="index")
    m = m.reindex(columns=range(5), fill_value=0.0)
    m.index.name, m.columns.name = "from_bucket", "to_bucket"
    return m.sort_index()


def vintage_curve(accounts: pd.DataFrame, perf: pd.DataFrame, mobs=(3, 6, 9, 12)) -> pd.DataFrame:
    d = pd.to_datetime(accounts["open_month"])
    vint = d.dt.year.astype(str) + "-Q" + ((d.dt.month - 1) // 3 + 1).astype(str)
    a = pd.DataFrame({"acct_id": accounts["acct_id"].to_numpy(), "vintage": vint.to_numpy()})
    first60 = perf[perf["dpd"] >= 60].groupby("acct_id")["mob"].min()
    a["first60"] = a["acct_id"].map(first60)
    out = pd.DataFrame({m: a.assign(f=(a["first60"] <= m)).groupby("vintage")["f"].mean() for m in mobs})
    out.index.name = "vintage"
    return out.sort_index()


# ----------------------------------------------------------------------------- SQL reference solutions
SQL = {
    "S01": """
SELECT product, COUNT(*) AS n_accounts, ROUND(AVG(orig_score), 1) AS avg_score, SUM(credit_limit) AS total_limit
FROM accounts GROUP BY product ORDER BY product;""",
    "S02": """
SELECT CASE WHEN dpd = 0 THEN 'B0_current' WHEN dpd < 30 THEN 'B1_1_29' WHEN dpd < 60 THEN 'B2_30_59'
            WHEN dpd < 90 THEN 'B3_60_89' ELSE 'B4_90p' END AS bucket,
       COUNT(*) AS n, ROUND(SUM(balance), 2) AS balance
FROM monthly_perf WHERE month = '2025-03-01'
GROUP BY bucket ORDER BY bucket;""",
    "S03": """
WITH cur AS (SELECT acct_id, month FROM monthly_perf
             WHERE month BETWEEN '2025-01-01' AND '2025-06-01' AND dpd BETWEEN 30 AND 59),
nxt AS (SELECT c.month, c.acct_id, n.dpd AS next_dpd
        FROM cur c JOIN monthly_perf n ON n.acct_id = c.acct_id AND n.month = date(c.month, '+1 month'))
SELECT month, COUNT(*) AS n_30_59, SUM(CASE WHEN next_dpd BETWEEN 60 AND 89 THEN 1 ELSE 0 END) AS rolled,
       ROUND(1.0 * SUM(CASE WHEN next_dpd BETWEEN 60 AND 89 THEN 1 ELSE 0 END) / COUNT(*), 4) AS roll_rate
FROM nxt GROUP BY month ORDER BY month;""",
    "S04": """
WITH obs AS (SELECT acct_id FROM monthly_perf WHERE month = '2024-01-01' AND dpd = 0),
f AS (SELECT o.acct_id,
             MAX(CASE WHEN p.dpd >= 90 OR p.charged_off = 1 THEN 1 ELSE 0 END) AS bad
      FROM obs o LEFT JOIN monthly_perf p
        ON p.acct_id = o.acct_id AND p.month BETWEEN '2024-02-01' AND '2024-10-01'
      GROUP BY o.acct_id)
SELECT a.segment, COUNT(*) AS n_obs, SUM(COALESCE(f.bad, 0)) AS bads,
       ROUND(1.0 * SUM(COALESCE(f.bad, 0)) / COUNT(*), 4) AS bad_rate
FROM f JOIN accounts a ON a.acct_id = f.acct_id
GROUP BY a.segment ORDER BY a.segment;""",
    "S05": """
WITH r AS (SELECT a.product, p.acct_id, p.balance,
                  ROW_NUMBER() OVER (PARTITION BY a.product ORDER BY p.balance DESC, p.acct_id ASC) AS rank_in_product
           FROM monthly_perf p JOIN accounts a ON a.acct_id = p.acct_id
           WHERE p.month = '2025-06-01')
SELECT product, acct_id, balance, rank_in_product FROM r WHERE rank_in_product <= 2 ORDER BY product, rank_in_product;""",
    "S06": """
WITH ev AS (SELECT acct_id, MAX(CASE WHEN dpd >= 60 THEN 1 ELSE 0 END) AS bad FROM monthly_perf GROUP BY acct_id),
s AS (SELECT sc.acct_id, sc.score, COALESCE(ev.bad, 0) AS bad,
             NTILE(10) OVER (ORDER BY sc.score ASC, sc.acct_id ASC) AS decile
      FROM scores sc LEFT JOIN ev ON ev.acct_id = sc.acct_id WHERE sc.snapshot = 'CURRENT'),
d AS (SELECT decile, COUNT(*) AS n, SUM(bad) AS bads, COUNT(*) - SUM(bad) AS goods FROM s GROUP BY decile)
SELECT decile, n, bads, ROUND(1.0 * bads / n, 4) AS bad_rate,
       ROUND(1.0 * SUM(bads) OVER (ORDER BY decile) / SUM(bads) OVER (), 4) AS cum_bad_pct,
       ROUND(1.0 * SUM(goods) OVER (ORDER BY decile) / SUM(goods) OVER (), 4) AS cum_good_pct,
       ROUND(ABS(1.0 * SUM(bads) OVER (ORDER BY decile) / SUM(bads) OVER ()
               - 1.0 * SUM(goods) OVER (ORDER BY decile) / SUM(goods) OVER ()), 4) AS ks
FROM d ORDER BY decile;""",
    "S07": """
WITH b AS (SELECT snapshot,
                  CASE WHEN score < 500 THEN 1 WHEN score < 550 THEN 2 WHEN score < 600 THEN 3 ELSE 4 END AS bin
           FROM scores),
d AS (SELECT bin,
             1.0 * SUM(CASE WHEN snapshot = 'DEV' THEN 1 ELSE 0 END) / (SELECT COUNT(*) FROM scores WHERE snapshot = 'DEV') AS e,
             1.0 * SUM(CASE WHEN snapshot = 'CURRENT' THEN 1 ELSE 0 END) / (SELECT COUNT(*) FROM scores WHERE snapshot = 'CURRENT') AS a
      FROM b GROUP BY bin)
SELECT ROUND(SUM((a - e) * LN(a / e)), 4) AS psi FROM d;""",
    "S08": """
WITH x AS (SELECT acct_id, dpd, LAG(dpd) OVER (PARTITION BY acct_id ORDER BY month) AS prev_dpd FROM monthly_perf)
SELECT COUNT(DISTINCT acct_id) AS n_accounts FROM x WHERE dpd >= 30 AND prev_dpd >= 30;""",
    "S09": """
WITH c AS (SELECT acct_id,
                  substr(open_month, 1, 4) || '-Q' || ((CAST(substr(open_month, 6, 2) AS INTEGER) + 2) / 3) AS vintage
           FROM accounts WHERE open_month BETWEEN '2023-01-01' AND '2023-12-01'),
f AS (SELECT acct_id, MIN(mob) AS mob90 FROM monthly_perf WHERE dpd >= 90 GROUP BY acct_id)
SELECT c.vintage, COUNT(*) AS n_accounts,
       ROUND(1.0 * SUM(CASE WHEN f.mob90 <= 6 THEN 1 ELSE 0 END) / COUNT(*), 4) AS cum_90_mob6,
       ROUND(1.0 * SUM(CASE WHEN f.mob90 <= 12 THEN 1 ELSE 0 END) / COUNT(*), 4) AS cum_90_mob12
FROM c LEFT JOIN f ON f.acct_id = c.acct_id
GROUP BY c.vintage ORDER BY c.vintage;""",
    "S10": """
SELECT COUNT(*) AS n_accounts
FROM accounts a
WHERE NOT EXISTS (SELECT 1 FROM scores s WHERE s.acct_id = a.acct_id AND s.snapshot = 'CURRENT')
  AND EXISTS (SELECT 1 FROM monthly_perf p WHERE p.acct_id = a.acct_id AND p.month >= '2025-01-01');""",
}
