# 05.1 · Python for Validation — from zero to interview-ready

**Your fastest path:** you already think in SAS and SQL. Learn Python as a *translation* of what you know (§A4 Rosetta table), then implement the 8 core metrics yourself (§B), then do 4 timed sets (§C).

**Code in this repo (all tested, Python 3.11):**
| File | What it is |
|---|---|
| `code/validation_toolkit.py` | KS, AUC/Gini, gains table, bootstrap CI, DeLong, PSI/CSI, binning, WoE/IV, calibration table, HL, binomial/Jeffreys by grade, Brier, VIF, roll rates, vintages. `python validation_toolkit.py` runs self-tests. |
| `code/demo_end_to_end.py` | Synthetic SBSS-style business-card portfolio → WoE scorecard → points → monitoring → validation → auto-drafted findings. Output saved in `code/demo_output.txt`. |
| `code/stress_test_diagnostics.py` | ADF/KPSS, OLS with HAC SEs, DW/BG/BP/JB, VIF, dynamic out-of-time backtest, sensitivity, rolling-coefficient stability. Output in `code/stress_test_output.txt`. |
| `code/sql_practice.py` | Builds a SQLite DB and runs the 12 SQL drills. |
| `04_pyspark_primer.md` | PySpark DataFrame API mapped to pandas/SQL; PSI, KS and roll rates at scale; what to say if you haven't used Spark in production. |

---

## Part A — Setup and essentials (Week 1)

### A1. Setup (pick one)
- **Easiest:** Google Colab (browser, nothing to install). Upload the `code/` files.
- **Local:** Anaconda → `pip install -r 05_coding/code/requirements.txt` → `jupyter lab` or VS Code.

### A2. Python basics you actually need (30 minutes)
```python
x = 0.05                      # float
n = 1000                      # int
name = "BCC"                  # string
grades = ["G1", "G2", "G3"]   # list (ordered, mutable)
pd_by_grade = {"G1": 0.01, "G2": 0.03}   # dict (key → value)

for g in grades:              # loop
    print(g, pd_by_grade.get(g, "n/a"))

def bad_rate(bads, total):    # function
    return bads / total if total else float("nan")

rates = [bad_rate(b, 100) for b in [3, 5, 8]]   # list comprehension
print(f"Bad rate = {rates[0]:.2%}")             # f-string formatting → 'Bad rate = 3.00%'
```

### A3. pandas — the 25 operations that cover ~90% of validation work
```python
import numpy as np
import pandas as pd

df = pd.read_csv("dev.csv")                 # also: read_sas("x.sas7bdat"), read_parquet, read_excel
df.head(); df.info(); df.describe()         # first look: types, missing, ranges
df["bad"].mean()                            # bad rate
df["industry"].value_counts(normalize=True) # distribution of a categorical
df.isna().mean().sort_values()              # missing rate per column  ← data-quality check

sub = df.loc[df["product"].eq("BCC") & (df["score"] < 150), ["acct_id", "score", "bad"]]  # filter + select
df = df.assign(high_util=np.where(df["utilization"] > 0.8, 1, 0))                         # new column
df["tib_filled"] = df["months_in_business"].fillna(df["months_in_business"].median())     # impute (be careful!)

# groupby with named aggregations (≈ PROC MEANS / SQL GROUP BY)
summary = df.groupby("industry").agg(n=("bad", "size"), bads=("bad", "sum"), bad_rate=("bad", "mean"))

# binning (≈ PROC RANK / PROC FORMAT)
df["score_decile"] = pd.qcut(df["score"], 10, labels=False, duplicates="drop")   # equal-count bins
df["util_band"] = pd.cut(df["utilization"], [0, 0.3, 0.6, 0.9, np.inf], include_lowest=True)  # fixed edges

# joins (≈ MERGE / SQL JOIN)
m = df.merge(scores, on="acct_id", how="left", validate="one_to_one")   # validate= catches dup keys!

# pivots / crosstabs
pd.pivot_table(df, index="vintage", columns="mob", values="bad60", aggfunc="mean")
pd.crosstab(df["bucket_t"], df["bucket_t1"], normalize="index")         # roll-rate matrix

# time series per account (≈ RETAIN / LAG)
df = df.sort_values(["acct_id", "month"])
df["dpd_prev"] = df.groupby("acct_id")["dpd"].shift(1)
df["bal_ma3"] = df.groupby("acct_id")["balance"].transform(lambda s: s.rolling(3).mean())

# stacking, dedup, ranking, cumulative
both = pd.concat([dev.assign(sample="DEV"), rec.assign(sample="REC")], ignore_index=True)
latest = sc.sort_values("score_date").drop_duplicates("acct_id", keep="last")
df["cum_bads"] = df.sort_values("score")["bad"].cumsum()

summary.to_csv("summary.csv"); summary.to_excel("summary.xlsx")
```

### A4. SAS ↔ pandas ↔ SQL Rosetta (learn by translation)
| Task | SAS | pandas | SQL |
|---|---|---|---|
| Filter rows | `data b; set a; where score<150; run;` | `a[a.score < 150]` | `WHERE score < 150` |
| New column | `x = log(y);` | `a["x"] = np.log(a["y"])` | `LN(y) AS x` |
| If/else | `if u>0.8 then f=1; else f=0;` | `np.where(a.u > 0.8, 1, 0)` | `CASE WHEN u>0.8 THEN 1 ELSE 0 END` |
| Group summary | `proc means; class seg; var bad;` | `a.groupby("seg")["bad"].agg(["size","mean"])` | `GROUP BY seg` |
| Frequency | `proc freq; tables seg;` | `a["seg"].value_counts()` | `COUNT(*) GROUP BY seg` |
| Deciles | `proc rank groups=10 out=r; var score; ranks d;` | `pd.qcut(a.score, 10, labels=False)` | `NTILE(10) OVER (ORDER BY score)` |
| Join | `merge a(in=x) b; by id; if x;` | `a.merge(b, on="id", how="left")` | `LEFT JOIN b USING (id)` |
| Sort / dedup | `proc sort nodupkey; by id;` | `a.drop_duplicates("id")` | `ROW_NUMBER() ... = 1` |
| Lag | `lag(dpd)` + `by id` + `first.id` | `groupby("id")["dpd"].shift(1)` | `LAG(dpd) OVER (PARTITION BY id ORDER BY m)` |
| Logistic | `proc logistic; model bad(event='1')=x1 x2;` | `sm.Logit(y, sm.add_constant(X)).fit()` | — |
| KS | `proc npar1way edf; class bad; var score;` | `stats.ks_2samp(s[y==1], s[y==0])` | running sums (drill D6) |
| Macro loop | `%do i=1 %to 10;` | `for i in range(1, 11):` | — |

### A5. Modeling libraries — the 12 calls you'll use
```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tsa.stattools import adfuller, kpss
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import HistGradientBoostingClassifier
from scipy import stats

logit = sm.Logit(y, sm.add_constant(X)).fit(disp=0); print(logit.summary())   # coefficients, p-values
pd_hat = logit.predict(sm.add_constant(X_new, has_constant="add"))
auc = roc_auc_score(y, pd_hat); gini = 2 * auc - 1
ks = stats.ks_2samp(pd_hat[y == 1], pd_hat[y == 0]).statistic
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
gbm = HistGradientBoostingClassifier(max_depth=3, learning_rate=0.05, monotonic_cst=[-1, 1, 1]).fit(X_tr, y_tr)
adf_p = adfuller(series)[1]          # H0: unit root
ols = sm.OLS(y_ts, sm.add_constant(X_ts)).fit(cov_type="HAC", cov_kwds={"maxlags": 4})
```

---

## Part B — Build-it-yourself (Weeks 1–3, alongside the 20-minute harness drills). Don't copy; write, then compare with the toolkit.

Use this data for all exercises:
```python
import sys; sys.path.append("05_coding/code")
from demo_end_to_end import simulate
dev = simulate(30_000, seed=1)
rec = simulate(10_000, seed=3, shift=1.5, drift=1.0)
```

| # | Exercise | Hint | Check against |
|---|---|---|---|
| B1 | **KS** of `vendor_score` on `dev` | Higher score = safer → use `-vendor_score` as risk score. Sort riskiest first; cumulative % bads − cumulative % goods; max abs. Group ties. | `vt.ks_statistic`, `scipy.stats.ks_2samp` |
| B2 | **AUC & Gini** | AUC = P(random bad scores riskier than random good). Rank formula: (R_bad − n_b(n_b+1)/2)/(n_b·n_g). Gini = 2·AUC − 1 | `vt.auc_score`, `sklearn.metrics.roc_auc_score` |
| B3 | **Gains table** with 10 bins, bad rate, cumulative %, KS per bin, lift | `pd.qcut` on rank to avoid tie errors | `vt.gains_table` |
| B4 | **PSI** of `vendor_score` dev → rec | Deciles from **dev** only; apply edges to rec; floor empty bins | `vt.psi` (expect ≈ 0.33 → RED) |
| B5 | **WoE & IV** for `utilization` (5 quantile bins) | WoE = ln(%G/%B); IV = Σ(%G−%B)·WoE; missing = own bin | `vt.woe_iv` |
| B6 | **Hosmer–Lemeshow** for a logistic PD | 10 bins by predicted PD; Σ(O−E)²/(n·p̄(1−p̄)); χ²(8) | `vt.hosmer_lemeshow` |
| B7 | **Binomial + Jeffreys test** per grade | `stats.binom.sf(D−1, N, PD)`; `stats.beta.cdf(PD, D+0.5, N−D+0.5)` | `vt.grade_calibration_tests` |
| B8 | **VIF** for 4 numeric drivers | Regress each on the others; 1/(1−R²) | `vt.vif`, statsmodels `variance_inflation_factor` |

**Mini-solutions (read only after trying):**
```python
# B1 KS — the 6-line version
s = -dev["vendor_score"]; y = dev["bad"]
g = pd.DataFrame({"s": s, "y": y}).groupby("s")["y"].agg(["sum", "count"]).sort_index(ascending=False)
cb = g["sum"].cumsum() / g["sum"].sum()
cg = (g["count"] - g["sum"]).cumsum() / (g["count"] - g["sum"]).sum()
ks = (cb - cg).abs().max()

# B4 PSI
edges = np.unique(np.quantile(dev["vendor_score"], np.linspace(0, 1, 11))); edges[0], edges[-1] = -np.inf, np.inf
e = np.histogram(dev["vendor_score"], edges)[0] / len(dev)
a = np.histogram(rec["vendor_score"], edges)[0] / len(rec)
e, a = np.clip(e, 1e-6, None), np.clip(a, 1e-6, None)
psi = np.sum((a - e) * np.log(a / e))
```

---

## Part C — Timed sets (45 minutes each, camera on, narrate aloud) — extra practice whenever C1/C2 are below 🟢

**Set 1 — Monitoring basics**
1. Bad rate and count by `industry` in `dev`, sorted descending by bad rate.
2. Gains table and KS for `vendor_score` (orientation!). Is rank-ordering monotonic?
3. PSI for `vendor_score` dev → rec. RAG it. One sentence of interpretation.

**Set 2 — SQL** → drills D3, D4, D6 from `02_sql_for_credit_risk.md` without looking.

**Set 3 — Model build & calibration**
1. WoE/IV for `utilization`, `delinq_12m`, `months_in_business` (missing as own bin). Rank by IV.
2. Logistic regression of `bad` on the 3 WoE variables (statsmodels). Interpret signs (why negative?).
3. Calibration table + HL test on `rec`. What does the pattern of O vs E across deciles tell you?

**Set 4 — Validation judgment**
1. Assign 7 PD grades (quantiles of dev PD); binomial & Jeffreys tests on `rec`. Which grades fail?
2. Bootstrap 95% CI for Gini on `rec`; is the drop vs dev statistically meaningful?
3. Write a 5-line finding (Observation, Criteria, Cause, Impact, Recommendation, Severity).

**Scoring yourself:** correct (40%) · clean code with functions and comments (20%) · edge cases handled — ties, empty bins, missing (20%) · interpretation + finding (20%).

---

## Part D — What live-coding interviewers watch for

1. **Orientation sanity:** "Is a higher score riskier or safer?" — say it before coding.
2. **Reference vs current:** PSI bins come from the reference sample. Say so.
3. **Edge cases:** empty bins (floor at ε), ties (group or rank), missing values (own bin), tiny bad counts (CIs).
4. **Vectorise:** groupby/cumsum over Python loops.
5. **Narrate the "so what":** every number ends with an interpretation and a next action.
6. **Reproducibility:** fixed seeds, functions, no hard-coded paths.

Common prompts: compute KS/Gini/PSI from a dataframe · write WoE/IV · build a logistic regression and interpret · roll-rate matrix · vintage curve · detect data-quality issues · "this code computes PSI — find the bug" (usual bugs: bins from the current sample, no ε for empty bins, `ln(E/A)` sign flipped, percentages not normalised).
