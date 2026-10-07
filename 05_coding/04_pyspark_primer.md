# 05.4 · PySpark primer — enough to answer honestly and code the basics

> **Why:** several target JDs list "Python + PySpark" (e.g., the Wells Fargo Lead QAS posting in
> `00_strategy/01_market_reality_and_targets.md` §4). You don't need production Spark experience to clear most validation
> loops, but you must not freeze when asked. The logic is the SQL and pandas you already know; only the API differs.
> **Time:** 60–90 minutes once (Colab: `!pip install pyspark`), then one drill a week.
>
> **Honest line if asked:** "I haven't run PySpark in production. I know the DataFrame API — groupBy/agg, joins, window
> functions — and it's the same logic as my SQL and pandas work. For example, here's how I'd compute PSI at scale…"
> Don't list PySpark on your résumé until you've done the drills below.

---

## 1. Mental model in five lines
- A **DataFrame** is a distributed table split into **partitions** across executors.
- **Transformations** (`select`, `filter`, `withColumn`, `groupBy`, `join`) are **lazy**: they build a plan.
- **Actions** (`count`, `show`, `first`, `collect`, `toPandas`, `write`) execute the plan.
- **Shuffles** (`groupBy`, `join`, `orderBy`, window functions) move data across the network; they are what makes jobs
  slow.
- Prefer **built-in functions** (`pyspark.sql.functions`) to Python UDFs: built-ins run inside the JVM; Python UDFs
  serialise every row.

## 2. Rosetta: pandas ↔ PySpark ↔ SQL
| Task | pandas | PySpark | SQL |
|---|---|---|---|
| Filter | `df[df.score < 150]` | `df.filter(F.col("score") < 150)` | `WHERE score < 150` |
| New column | `np.where(df.u > 0.8, 1, 0)` | `F.when(F.col("u") > 0.8, 1).otherwise(0)` | `CASE WHEN u > 0.8 THEN 1 ELSE 0 END` |
| Group summary | `df.groupby("seg").agg(n=("bad","size"))` | `df.groupBy("seg").agg(F.count("*").alias("n"))` | `GROUP BY seg` |
| Join | `a.merge(b, on="id", how="left")` | `a.join(b, on="id", how="left")` | `LEFT JOIN b USING (id)` |
| Lag | `groupby("id")["dpd"].shift(1)` | `F.lag("dpd", 1).over(Window.partitionBy("id").orderBy("month"))` | `LAG(dpd) OVER (PARTITION BY id ORDER BY month)` |
| Latest row per id | `sort + drop_duplicates(keep="last")` | `row_number()` over a window, then `filter("rn = 1")` | `ROW_NUMBER() … = 1` |
| Deciles | `pd.qcut(s, 10)` | `approxQuantile` edges + `Bucketizer` (scales) or `F.ntile(10)` (small data only) | `NTILE(10)` |
| Missing as a group | `fillna("MISSING")` | `F.coalesce(F.col("seg"), F.lit("MISSING"))` | `COALESCE(seg, 'MISSING')` |

## 3. Core patterns (run these once)
```python
from pyspark.sql import SparkSession, Window, functions as F
from pyspark.ml.feature import Bucketizer

spark = SparkSession.builder.appName("validation").getOrCreate()
df = spark.read.csv("dev.csv", header=True, inferSchema=True)   # or spark.read.parquet(...)
df.printSchema(); df.show(5)

# Bad rate by segment, missing as its own group
summary = (df.withColumn("seg", F.coalesce(F.col("segment"), F.lit("MISSING")))
             .groupBy("seg")
             .agg(F.count("*").alias("n"), F.sum("bad").alias("bads"), F.avg("bad").alias("bad_rate"))
             .orderBy(F.desc("bad_rate")))

# Previous month's DPD and the latest record per account
w = Window.partitionBy("acct_id").orderBy("month")
perf = perf.withColumn("dpd_prev", F.lag("dpd", 1).over(w))
latest = (perf.withColumn("rn", F.row_number().over(Window.partitionBy("acct_id").orderBy(F.desc("month"))))
              .filter("rn = 1").drop("rn"))
```

**PSI at scale — bins from the reference sample, empty bins floored:**
```python
def psi(ref, cur, col, n_bins=10, eps=1e-6):
    cuts = ref.approxQuantile(col, [i / n_bins for i in range(1, n_bins)], 0.0001)
    splits = [-float("inf")] + sorted(set(cuts)) + [float("inf")]
    bk = Bucketizer(splits=splits, inputCol=col, outputCol="bin", handleInvalid="keep")  # NaN → own bucket

    def dist(d, name):
        n = d.count()
        return bk.transform(d).groupBy("bin").agg((F.count("*") / F.lit(n)).alias(name))

    t = (dist(ref, "e").join(dist(cur, "a"), on="bin", how="full").fillna(0.0, subset=["e", "a"])
         .withColumn("e", F.greatest(F.col("e"), F.lit(eps)))
         .withColumn("a", F.greatest(F.col("a"), F.lit(eps))))
    return t.select(F.sum((F.col("a") - F.col("e")) * F.log(F.col("a") / F.col("e"))).alias("psi")).first()["psi"]
```

**KS with ties grouped** (here a higher score is safer, so the riskiest are the lowest scores — say this out loud):
```python
def ks(scored, score_col="score", bad_col="bad"):
    g = scored.groupBy(score_col).agg(F.sum(bad_col).alias("b"), (F.count("*") - F.sum(bad_col)).alias("g"))
    tot = g.agg(F.sum("b").alias("B"), F.sum("g").alias("G")).first()
    w = Window.orderBy(F.col(score_col).asc()).rowsBetween(Window.unboundedPreceding, Window.currentRow)
    return (g.withColumn("cb", F.sum("b").over(w) / tot["B"])
             .withColumn("cg", F.sum("g").over(w) / tot["G"])
             .select(F.max(F.abs(F.col("cb") - F.col("cg"))).alias("ks")).first()["ks"])
```
*(The un-partitioned window runs on one partition. That is fine here because it runs on one row per distinct score, not
per account. Say so if asked.)*

**Roll-rate matrix (month t → t+1):**
```python
w = Window.partitionBy("acct_id").orderBy("month")
t = (perf.withColumn("bucket", F.when(F.col("dpd") == 0, 0).when(F.col("dpd") < 30, 1)
                                 .when(F.col("dpd") < 60, 2).when(F.col("dpd") < 90, 3).otherwise(4))
         .withColumn("next_bucket", F.lead("bucket").over(w))
         .filter(F.col("next_bucket").isNotNull()))
counts = t.groupBy("bucket").pivot("next_bucket", [0, 1, 2, 3, 4]).count().fillna(0)
# divide each row by its total (in Spark, or after .toPandas() — the matrix is tiny)
```

## 4. Performance and correctness — what interviewers ask
| Question | Answer |
|---|---|
| Transformation vs action? | Transformations are lazy and build a plan; actions run it. `count()` inside a loop re-runs the whole plan each time — cache the DataFrame if you reuse it. |
| Why is my job slow? | Usually shuffles (wide joins, `groupBy`, global sorts) or **skew** (one key, e.g., a default segment, holds most rows). Check the Spark UI stages; filter and select early; broadcast small tables. |
| Broadcast join? | `big.join(F.broadcast(small), "key")` ships the small table to every executor and avoids shuffling the big one. Use it for dimension tables (product, segment mapping). |
| Deciles on 50 million rows? | `F.ntile(10)` over a global window pulls all rows into one partition. Use `approxQuantile` for edges (state the relative error) plus `Bucketizer`. |
| `cache()` vs `persist()`? | `cache()` is `persist()` with the default storage level; use either when a DataFrame is reused by several actions, and `unpersist()` afterwards. |
| Python UDF vs built-in? | Built-ins run in the JVM and are optimised; Python UDFs serialise each row to Python. Use built-ins or vectorised pandas UDFs. |
| How would you migrate a SAS monitoring job to PySpark? | Map each DATA step / PROC to DataFrame operations; then run both in parallel and **reconcile** — row counts at each step, metrics (KS, PSI, bad rates) within a stated tolerance, edge cases (missing values, boundaries). That's implementation testing, the validator's home ground. |

## 5. Drills (Colab, 20 minutes each)
1. Load `05_coding/code` demo data (`simulate()` → `spark.createDataFrame(pandas_df)`), compute bad rate by industry.
2. Compute PSI of `vendor_score` dev → recent with the function above; compare with `validation_toolkit.psi` (expect
   small differences: approximate quantiles).
3. KS of `vendor_score` on dev; compare with the toolkit.
4. Roll-rate matrix on the SQL practice database's `monthly_perf` (read it with pandas, then `createDataFrame`).
