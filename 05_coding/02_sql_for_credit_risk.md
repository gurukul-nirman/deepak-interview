# 05.2 · SQL for Credit Risk — patterns, drills, and interview traps

**Why it matters:** almost every monitoring/validation role tests SQL (live or online). The bar is not exotic syntax — it's **correct credit-risk logic**: performance windows, roll rates, vintages, deciles, PSI, and data-quality checks — using joins and window functions without double-counting.

**Practice DB:** `python 05_coding/code/sql_practice.py` builds `credit_practice.db` (SQLite) and prints the expected output of every drill below. Open it in DB Browser for SQLite / DBeaver and **write each query before reading the solution**.

---

## 1. The 10 concepts that cover ~90% of credit-risk SQL

| # | Concept | Where it bites in credit risk |
|---|---|---|
| 1 | `GROUP BY` + aggregates, `HAVING` | Bad rate by segment; duplicates check |
| 2 | `CASE WHEN` | DPD → delinquency buckets; bad flags |
| 3 | Joins (`INNER` / `LEFT` / anti-join `LEFT … IS NULL`) | Attaching performance to an observation snapshot without losing accounts |
| 4 | **Join grain** | Joining account-level to account-month data multiplies rows → inflated sums. Always state the grain of each table |
| 5 | CTEs (`WITH …`) | Readable multi-step logic; interviewers love it |
| 6 | Window functions: `ROW_NUMBER`, `RANK`, `NTILE` | Latest record per account; top-N; deciles |
| 7 | `LAG` / `LEAD` | Month-on-month transitions (roll rates), consecutive delinquencies |
| 8 | Running totals `SUM() OVER (ORDER BY …)` | Cumulative % bads/goods → KS |
| 9 | Date windows | 12-month performance window after an observation point |
| 10 | NULL semantics | `NULL = NULL` is not true; `COUNT(col)` skips NULLs; `AVG` ignores NULLs |

**Tables in the practice DB**

| Table | Grain | Columns |
|---|---|---|
| `accounts` | 1 row per account | acct_id, open_month, product (BCC/LOAN), segment, orig_score (0–300), credit_limit |
| `monthly_perf` | 1 row per account-month | acct_id, month ('YYYY-MM-01'), mob, balance, dpd, charged_off |
| `scores` | 1 row per account-snapshot | acct_id, snapshot ('DEV'/'CURRENT'), score |

---

## 2. Drills (solutions are exactly what `sql_practice.py` runs)

### D1 — Portfolio summary by product/segment
Warm-up. Interviewers watch for clean aliasing and ordering.

```sql
SELECT product, segment,
       COUNT(*)                         AS n_accounts,
       ROUND(AVG(credit_limit), 0)      AS avg_limit,
       ROUND(AVG(orig_score), 1)        AS avg_orig_score
FROM accounts
GROUP BY product, segment
ORDER BY product, segment;
```

### D2 — Delinquency buckets with CASE WHEN
Bucket boundaries must be exhaustive and non-overlapping. Say which DPD convention you use (contractual vs. days since last full payment).

```sql
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
```

### D3 — Roll-rate matrix (month t -> t+1) with LEAD
`LEAD` avoids a self-join. Each row = an account-month transition. Read the 2→3 cell: **% of 30–59 that roll to 60–89 next month** (the 'flow rate'). Exclude the last month per account (no next).

```sql
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
```

### D4 — Bad flag: ever 90+ DPD or charge-off within 12 months after observation point
The heart of model development: **observation point → performance window → bad flag**. Traps: (1) select the population at the observation point only; (2) window = months 1–12 *after* it; (3) `LEFT JOIN` so accounts with no future rows aren't silently dropped; (4) report incomplete windows.

```sql
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
```

### D5 — Vintage curve: cumulative 60+ DPD rate by MOB per origination quarter
Cumulative bad rate by months-on-book per cohort. Compare cohorts at the **same MOB**, never calendar month. Note immature cohorts can't have MOB 12 values yet in real data.

```sql
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
```

### D6 — Score deciles, bad rate and KS using NTILE + running sums
`NTILE` for deciles + window running sums for KS. For a proper KS use a fixed performance window (D4) — this drill uses 'ever bad' for brevity.

```sql
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
```

### D7 — PSI between DEV and CURRENT score snapshots (fixed bins)
PSI with fixed bins. If your SQL engine lacks `LN`, compute in Python/SAS. Bins must come from the reference (DEV) distribution.

```sql
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
```

### D8 — Top-N per group: 3 highest balances per segment in Jun-2025 (ROW_NUMBER)
Classic top-N-per-group. `ROW_NUMBER` gives unique ranks; `RANK`/`DENSE_RANK` keep ties.

```sql
WITH r AS (
  SELECT a.segment, p.acct_id, p.balance,
         ROW_NUMBER() OVER (PARTITION BY a.segment ORDER BY p.balance DESC) AS rn
  FROM monthly_perf p JOIN accounts a USING (acct_id)
  WHERE p.month = '2025-06-01'
)
SELECT segment, acct_id, balance, rn FROM r WHERE rn <= 3 ORDER BY segment, rn;
```

### D9 — Three consecutive delinquent months (LAG twice)
Consecutive-event logic with two `LAG`s. Gaps-and-islands is the general version for 'N consecutive'.

```sql
WITH x AS (
  SELECT acct_id, month, dpd,
         LAG(dpd, 1) OVER (PARTITION BY acct_id ORDER BY month) AS dpd_m1,
         LAG(dpd, 2) OVER (PARTITION BY acct_id ORDER BY month) AS dpd_m2
  FROM monthly_perf
)
SELECT COUNT(DISTINCT acct_id) AS accts_with_3_consecutive_delinquent_months
FROM x WHERE dpd > 0 AND dpd_m1 > 0 AND dpd_m2 > 0;
```

### D10 — Anti-join: accounts with no CURRENT score
Anti-join. Equivalent: `WHERE NOT EXISTS (…)`. Avoid `NOT IN` with a subquery that can return NULL.

```sql
SELECT COUNT(*) AS accts_without_current_score
FROM accounts a
LEFT JOIN scores s ON s.acct_id = a.acct_id AND s.snapshot = 'CURRENT'
WHERE s.acct_id IS NULL;
```

### D11 — Month-over-month balance change and 3-month moving average (portfolio)
Running/moving windows. `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` = 3-month moving average.

```sql
WITH m AS (SELECT month, SUM(balance) AS bal FROM monthly_perf GROUP BY month)
SELECT month, ROUND(bal, 0) AS balance,
       ROUND(bal - LAG(bal) OVER (ORDER BY month), 0) AS mom_change,
       ROUND(AVG(bal) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 0) AS ma_3m
FROM m WHERE month BETWEEN '2025-01-01' AND '2025-06-01' ORDER BY month;
```

### D12 — Data-quality checks: duplicates, nulls, out-of-range
Data-quality checks a validator runs before trusting any metric. Add: future-dated records, impossible transitions (e.g., 0 → 90+ in one month), default definition consistency.

```sql
SELECT 'duplicate acct-month rows' AS check_name,
       (SELECT COUNT(*) FROM (SELECT acct_id, month FROM monthly_perf GROUP BY acct_id, month HAVING COUNT(*) > 1)) AS issues
UNION ALL SELECT 'null dpd', (SELECT COUNT(*) FROM monthly_perf WHERE dpd IS NULL)
UNION ALL SELECT 'negative balance', (SELECT COUNT(*) FROM monthly_perf WHERE balance < 0)
UNION ALL SELECT 'orig_score outside 0-300', (SELECT COUNT(*) FROM accounts WHERE orig_score NOT BETWEEN 0 AND 300)
UNION ALL SELECT 'perf before open_month', (SELECT COUNT(*) FROM monthly_perf p JOIN accounts a USING (acct_id) WHERE p.month < a.open_month);
```

---

## 3. Dialect differences you may meet (bank stacks: Oracle, Teradata, SQL Server, Snowflake, Hive/Spark)

| Need | SQLite (practice) | Oracle | SQL Server | Snowflake / Spark SQL |
|---|---|---|---|---|
| Add months | `date(m, '+1 month')` | `ADD_MONTHS(m, 1)` | `DATEADD(month, 1, m)` | `DATEADD(month, 1, m)` / `add_months(m, 1)` |
| Natural log | `LN(x)` (math functions build) | `LN(x)` | `LOG(x)` | `LN(x)` |
| Top N | `LIMIT 10` | `FETCH FIRST 10 ROWS ONLY` | `TOP 10` | `LIMIT 10` |
| Boolean avg | `AVG(cond)` | `AVG(CASE WHEN cond THEN 1 ELSE 0 END)` | same as Oracle | `AVG(IFF(cond,1,0))` |
| Filter on window | CTE then `WHERE rn = 1` | same | same | `QUALIFY rn = 1` |

---

## 4. SQL interview questions (with the answer they want)

1. **WHERE vs HAVING?** WHERE filters rows before aggregation; HAVING filters groups after.
2. **INNER vs LEFT JOIN — which for attaching performance to an observation snapshot?** LEFT — otherwise accounts without future records disappear and the bad rate is biased.
3. **ROW_NUMBER vs RANK vs DENSE_RANK?** Unique sequence vs ties share rank with gaps vs ties share rank without gaps.
4. **COUNT(*) vs COUNT(col)?** COUNT(col) skips NULLs.
5. **Why did my bad count double after a join?** Grain mismatch (one-to-many). Aggregate the many side first or join on the full key.
6. **Find duplicates** → `GROUP BY key HAVING COUNT(*) > 1`.
7. **Second-highest balance per segment** → `DENSE_RANK() … = 2`.
8. **Ever-30+ in last 6 months** → `MAX(CASE WHEN dpd >= 30 THEN 1 ELSE 0 END)` over a date-bounded join (pattern D4).
9. **Roll rate from current to 30+** → `LEAD` transition (pattern D3).
10. **Why can `NOT IN` return nothing?** If the subquery contains NULL, `x NOT IN (…, NULL)` is never true. Use `NOT EXISTS`.
11. **Performance tuning basics?** Filter early, select only needed columns, index/partition on join keys and dates, avoid functions on indexed columns in WHERE, check the plan.
12. **How do you make a monitoring query reproducible?** Fixed snapshot dates, documented filters/exclusions, versioned code, row-count reconciliation to source.
