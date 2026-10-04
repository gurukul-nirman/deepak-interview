"""
sql_practice.py — builds a small credit-card/loan database in SQLite and runs every SQL drill
from 05_coding/02_sql_for_credit_risk.md, so you can see the expected output.

Run:  python sql_practice.py            (creates credit_practice.db next to this file)
Then practise: open the .db in DBeaver / DB Browser for SQLite / `sqlite3 credit_practice.db`
and write each query yourself BEFORE looking at the solution.

Tables
  accounts(acct_id, open_month, product, segment, orig_score, credit_limit)
  monthly_perf(acct_id, month, mob, balance, dpd, charged_off)      -- one row per account-month
  scores(acct_id, snapshot, score)                                   -- snapshot in ('DEV','CURRENT')
Months are stored as first-of-month ISO strings 'YYYY-MM-01' (safe for SQLite date arithmetic).
"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

DB = Path(__file__).with_name("credit_practice.db")
rng = np.random.default_rng(2026)


def month_add(m: str, k: int) -> str:
    y, mo = int(m[:4]), int(m[5:7])
    t = y * 12 + (mo - 1) + k
    return f"{t // 12:04d}-{t % 12 + 1:02d}-01"


def build() -> sqlite3.Connection:
    n = 3000
    open_months = [month_add("2023-01-01", int(k)) for k in rng.integers(0, 24, n)]
    product = rng.choice(["BCC", "LOAN"], n, p=[0.6, 0.4])
    segment = rng.choice(["Micro", "Small"], n, p=[0.55, 0.45])
    orig_score = np.clip(rng.normal(190, 40, n), 0, 300).round().astype(int)
    limit = (np.where(product == "BCC", 15000, 50000) * rng.lognormal(0, 0.4, n)).round(-2)
    accounts = pd.DataFrame({"acct_id": np.arange(1, n + 1), "open_month": open_months, "product": product,
                             "segment": segment, "orig_score": orig_score, "credit_limit": limit})

    # delinquency Markov chain on buckets 0..4 (0=current, 1=1-29, 2=30-59, 3=60-89, 4=90+)
    base = np.array([
        [0.955, 0.040, 0.005, 0.000, 0.000],
        [0.550, 0.250, 0.200, 0.000, 0.000],
        [0.250, 0.100, 0.250, 0.400, 0.000],
        [0.100, 0.020, 0.080, 0.200, 0.600],
        [0.030, 0.000, 0.020, 0.050, 0.900],
    ])
    rows = []
    last = "2025-12-01"
    for a in accounts.itertuples(index=False):
        risk = np.exp(-(a.orig_score - 190) / 60)  # >1 for weak scores
        state, months_90 = 0, 0
        m, mob = a.open_month, 0
        bal = a.credit_limit * rng.uniform(0.2, 0.7)
        while m <= last and mob <= 30:
            p = base[state].copy()
            if state < 4:  # stress: shift probability mass from 'cure/stay current' towards worsening
                worsen = p[state + 1:].sum()
                extra = min(worsen * (risk - 1), p[0] * 0.5) if risk > 1 else worsen * (risk - 1)
                p[0] -= extra
                p[state + 1] += extra
                p = np.clip(p, 0, None)
                p /= p.sum()
            if mob > 0:
                state = rng.choice(5, p=p)
            dpd = 0 if state == 0 else int(rng.integers([1, 30, 60, 90][state - 1], [30, 60, 90, 180][state - 1]))
            months_90 = months_90 + 1 if state == 4 else 0
            charged_off = int(months_90 >= 3)
            bal = max(0.0, bal * rng.uniform(0.9, 1.08))
            rows.append((a.acct_id, m, mob, round(bal, 2), dpd, charged_off))
            if charged_off:
                break
            m, mob = month_add(m, 1), mob + 1
    perf = pd.DataFrame(rows, columns=["acct_id", "month", "mob", "balance", "dpd", "charged_off"])

    # two score snapshots for PSI: development-era population vs current population (shifted)
    dev_ids = accounts.loc[accounts["open_month"] < "2024-01-01", "acct_id"]
    cur_ids = accounts.loc[accounts["open_month"] >= "2024-01-01", "acct_id"]
    scores = pd.concat([
        pd.DataFrame({"acct_id": dev_ids, "snapshot": "DEV",
                      "score": np.clip(rng.normal(560, 40, len(dev_ids)), 300, 850).round()}),
        pd.DataFrame({"acct_id": cur_ids, "snapshot": "CURRENT",
                      "score": np.clip(rng.normal(540, 45, len(cur_ids)), 300, 850).round()}),
    ])

    if DB.exists():
        DB.unlink()
    con = sqlite3.connect(DB)
    accounts.to_sql("accounts", con, index=False)
    perf.to_sql("monthly_perf", con, index=False)
    scores.to_sql("scores", con, index=False)
    con.execute("CREATE INDEX ix_perf ON monthly_perf(acct_id, month)")
    con.commit()
    return con


# --------------------------------------------------------------------------------------------
# Drills (same numbering as the markdown file)
# --------------------------------------------------------------------------------------------
DRILLS = {
    "D1 Portfolio summary by product/segment": """
SELECT product, segment,
       COUNT(*)                         AS n_accounts,
       ROUND(AVG(credit_limit), 0)      AS avg_limit,
       ROUND(AVG(orig_score), 1)        AS avg_orig_score
FROM accounts
GROUP BY product, segment
ORDER BY product, segment;
""",
    "D2 Delinquency buckets with CASE WHEN": """
SELECT CASE WHEN dpd = 0              THEN '0 Current'
            WHEN dpd BETWEEN 1  AND 29 THEN '1 1-29'
            WHEN dpd BETWEEN 30 AND 59 THEN '2 30-59'
            WHEN dpd BETWEEN 60 AND 89 THEN '3 60-89'
            ELSE                            '4 90+' END AS bucket,
       COUNT(*)                         AS account_months,
       ROUND(SUM(balance), 0)           AS balance
FROM monthly_perf
WHERE month = '2025-06-01'
GROUP BY bucket
ORDER BY bucket;
""",
    "D3 Roll-rate matrix (month t -> t+1) with LEAD": """
WITH b AS (
  SELECT acct_id, month,
         CASE WHEN dpd = 0 THEN 0 WHEN dpd < 30 THEN 1 WHEN dpd < 60 THEN 2
              WHEN dpd < 90 THEN 3 ELSE 4 END AS bucket
  FROM monthly_perf
), t AS (
  SELECT acct_id, month, bucket,
         LEAD(bucket) OVER (PARTITION BY acct_id ORDER BY month) AS next_bucket
  FROM b
)
SELECT bucket AS from_bucket,
       ROUND(AVG(next_bucket = 0), 3) AS to_0,
       ROUND(AVG(next_bucket = 1), 3) AS to_1,
       ROUND(AVG(next_bucket = 2), 3) AS to_2,
       ROUND(AVG(next_bucket = 3), 3) AS to_3,
       ROUND(AVG(next_bucket = 4), 3) AS to_4,
       COUNT(*) AS n
FROM t
WHERE next_bucket IS NOT NULL
GROUP BY bucket
ORDER BY bucket;
""",
    "D4 Bad flag: ever 90+ DPD or charge-off within 12 months after observation point": """
WITH obs AS (                       -- observation point: accounts open and current on 2024-06-01
  SELECT acct_id FROM monthly_perf WHERE month = '2024-06-01' AND dpd = 0
), perf AS (
  SELECT o.acct_id,
         MAX(CASE WHEN p.dpd >= 90 OR p.charged_off = 1 THEN 1 ELSE 0 END) AS bad_12m,
         COUNT(p.month) AS months_observed
  FROM obs o
  LEFT JOIN monthly_perf p
    ON p.acct_id = o.acct_id
   AND p.month BETWEEN date('2024-06-01', '+1 month') AND date('2024-06-01', '+12 months')
  GROUP BY o.acct_id
)
SELECT a.product,
       COUNT(*)                    AS n_obs,
       SUM(bad_12m)                AS bads,
       ROUND(AVG(bad_12m), 4)      AS bad_rate,
       SUM(months_observed < 12)   AS incomplete_window   -- e.g., charged off early or data gaps
FROM perf JOIN accounts a USING (acct_id)
GROUP BY a.product;
""",
    "D5 Vintage curve: cumulative 60+ DPD rate by MOB per origination quarter": """
WITH first60 AS (
  SELECT acct_id, MIN(mob) AS mob_first60
  FROM monthly_perf WHERE dpd >= 60 GROUP BY acct_id
), coh AS (
  SELECT acct_id,
         substr(open_month, 1, 4) || '-Q' || ((CAST(substr(open_month, 6, 2) AS INTEGER) + 2) / 3) AS vintage
  FROM accounts
), mobs AS (SELECT 3 AS mob UNION ALL SELECT 6 UNION ALL SELECT 9 UNION ALL SELECT 12)
SELECT c.vintage, m.mob,
       ROUND(1.0 * SUM(CASE WHEN f.mob_first60 <= m.mob THEN 1 ELSE 0 END) / COUNT(*), 4) AS cum_60plus_rate
FROM coh c CROSS JOIN mobs m
LEFT JOIN first60 f ON f.acct_id = c.acct_id
GROUP BY c.vintage, m.mob
ORDER BY c.vintage, m.mob;
""",
    "D6 Score deciles, bad rate and KS using NTILE + running sums": """
WITH bad AS (
  SELECT acct_id, MAX(CASE WHEN dpd >= 90 OR charged_off = 1 THEN 1 ELSE 0 END) AS bad
  FROM monthly_perf GROUP BY acct_id
), s AS (
  SELECT a.acct_id, a.orig_score, b.bad,
         NTILE(10) OVER (ORDER BY a.orig_score ASC) AS decile        -- decile 1 = lowest score = riskiest
  FROM accounts a JOIN bad b USING (acct_id)
), d AS (
  SELECT decile, COUNT(*) AS n, SUM(bad) AS bads, COUNT(*) - SUM(bad) AS goods,
         MIN(orig_score) AS min_score, MAX(orig_score) AS max_score
  FROM s GROUP BY decile
)
SELECT decile, min_score, max_score, n, bads,
       ROUND(1.0 * bads / n, 4) AS bad_rate,
       ROUND(1.0 * SUM(bads)  OVER (ORDER BY decile) / SUM(bads)  OVER (), 4) AS cum_bad_pct,
       ROUND(1.0 * SUM(goods) OVER (ORDER BY decile) / SUM(goods) OVER (), 4) AS cum_good_pct,
       ROUND(ABS(1.0 * SUM(bads)  OVER (ORDER BY decile) / SUM(bads)  OVER ()
               - 1.0 * SUM(goods) OVER (ORDER BY decile) / SUM(goods) OVER ()), 4) AS ks_at_decile
FROM d ORDER BY decile;
""",
    "D7 PSI between DEV and CURRENT score snapshots (fixed bins)": """
WITH binned AS (
  SELECT snapshot,
         CASE WHEN score < 500 THEN '1 <500'
              WHEN score < 525 THEN '2 500-524'
              WHEN score < 550 THEN '3 525-549'
              WHEN score < 575 THEN '4 550-574'
              WHEN score < 600 THEN '5 575-599'
              ELSE                  '6 600+' END AS bin
  FROM scores
), dist AS (
  SELECT bin,
         1.0 * SUM(snapshot = 'DEV')     / (SELECT COUNT(*) FROM scores WHERE snapshot = 'DEV')     AS e_pct,
         1.0 * SUM(snapshot = 'CURRENT') / (SELECT COUNT(*) FROM scores WHERE snapshot = 'CURRENT') AS a_pct
  FROM binned GROUP BY bin
)
SELECT bin, ROUND(e_pct, 4) AS expected_pct, ROUND(a_pct, 4) AS actual_pct,
       ROUND((a_pct - e_pct) * LN(a_pct / e_pct), 5) AS psi_contrib,
       ROUND(SUM((a_pct - e_pct) * LN(a_pct / e_pct)) OVER (), 4) AS total_psi
FROM dist ORDER BY bin;
""",
    "D8 Top-N per group: 3 highest balances per segment in Jun-2025 (ROW_NUMBER)": """
WITH r AS (
  SELECT a.segment, p.acct_id, p.balance,
         ROW_NUMBER() OVER (PARTITION BY a.segment ORDER BY p.balance DESC) AS rn
  FROM monthly_perf p JOIN accounts a USING (acct_id)
  WHERE p.month = '2025-06-01'
)
SELECT segment, acct_id, balance, rn FROM r WHERE rn <= 3 ORDER BY segment, rn;
""",
    "D9 Three consecutive delinquent months (LAG twice)": """
WITH x AS (
  SELECT acct_id, month, dpd,
         LAG(dpd, 1) OVER (PARTITION BY acct_id ORDER BY month) AS dpd_m1,
         LAG(dpd, 2) OVER (PARTITION BY acct_id ORDER BY month) AS dpd_m2
  FROM monthly_perf
)
SELECT COUNT(DISTINCT acct_id) AS accts_with_3_consecutive_delinquent_months
FROM x WHERE dpd > 0 AND dpd_m1 > 0 AND dpd_m2 > 0;
""",
    "D10 Anti-join: accounts with no CURRENT score": """
SELECT COUNT(*) AS accts_without_current_score
FROM accounts a
LEFT JOIN scores s ON s.acct_id = a.acct_id AND s.snapshot = 'CURRENT'
WHERE s.acct_id IS NULL;
""",
    "D11 Month-over-month balance change and 3-month moving average (portfolio)": """
WITH m AS (SELECT month, SUM(balance) AS bal FROM monthly_perf GROUP BY month)
SELECT month, ROUND(bal, 0) AS balance,
       ROUND(bal - LAG(bal) OVER (ORDER BY month), 0) AS mom_change,
       ROUND(AVG(bal) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS ma_3m
FROM m WHERE month BETWEEN '2025-01-01' AND '2025-06-01' ORDER BY month;
""",
    "D12 Data-quality checks: duplicates, nulls, out-of-range": """
SELECT 'duplicate acct-month rows' AS check_name,
       (SELECT COUNT(*) FROM (SELECT acct_id, month FROM monthly_perf GROUP BY acct_id, month HAVING COUNT(*) > 1)) AS issues
UNION ALL SELECT 'null dpd', (SELECT COUNT(*) FROM monthly_perf WHERE dpd IS NULL)
UNION ALL SELECT 'negative balance', (SELECT COUNT(*) FROM monthly_perf WHERE balance < 0)
UNION ALL SELECT 'orig_score outside 0-300', (SELECT COUNT(*) FROM accounts WHERE orig_score NOT BETWEEN 0 AND 300)
UNION ALL SELECT 'perf before open_month', (SELECT COUNT(*) FROM monthly_perf p JOIN accounts a USING (acct_id) WHERE p.month < a.open_month);
""",
}


def main():
    con = build()
    con.create_function("LN", 1, lambda v: float(np.log(v)) if v and v > 0 else None)  # SQLite lacks LN in some builds
    print(f"Database built: {DB}")
    for name, sql in DRILLS.items():
        print("\n" + "=" * 90 + f"\n{name}\n" + "-" * 90)
        print(pd.read_sql_query(sql, con).to_string(index=False))
    con.close()


if __name__ == "__main__":
    main()
