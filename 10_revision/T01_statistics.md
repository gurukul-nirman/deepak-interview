# T01 · Statistics for validation — quick refresher
**Study:** `01_foundations/01_statistics_from_scratch.md` · **Test:** `START TOPIC T01` · `REVISE T01`

## 60-second summary
- A **p-value** is P(data at least this extreme | H0 true) — not P(H0 true).
- PD back-tests are **one-sided** (worry = under-estimation). Binomial/Jeffreys assume **independent defaults** → too strict when defaults correlate.
- Big samples make everything significant → judge **effect size**; tiny bad counts → wide CIs.
- Time series: check **stationarity** (ADF H0 = unit root; KPSS H0 = stationary) before trusting a regression.
- OLS violations mostly break **standard errors** (autocorrelation, heteroskedasticity) → HAC/robust SEs.

## Quick Q → short answer
| Q | A |
|---|---|
| 95% CI for a 5% bad rate on 2,000 accounts? | SE = √(0.05·0.95/2000) ≈ 0.49% → 4.0%–6.0% |
| Type I vs Type II in monitoring? | False alarm on a good model vs missing a broken model |
| Power? | 1 − P(Type II): chance of detecting a real problem |
| Test for PD per grade? | One-sided binomial or Jeffreys; normal approx. for large N·PD |
| Test for overall logistic calibration? | Hosmer–Lemeshow (χ², g−2 dof on dev sample) |
| Compare champion vs challenger AUC on the same data? | DeLong test |
| Are two score distributions different? | Two-sample KS test |
| LGD realised vs predicted? | Paired/one-sample t-test on the difference |
| Pearson vs Spearman? | Linear vs rank (monotonic) association |
| Multicollinearity effect? | Unstable coefficients, sign flips, inflated SEs; predictions often fine |
| VIF rule? | > 5 investigate, > 10 serious |
| Heteroskedasticity test & fix? | Breusch–Pagan/White; robust SEs, WLS, transform |
| Autocorrelation test with a lagged dependent variable? | Breusch–Godfrey (DW is biased) |
| Spurious regression? | Non-stationary series look related; difference or test cointegration |
| MLE in one line? | Choose parameters that make the observed data most likely |
| AIC vs BIC? | Both penalise complexity; BIC more strongly (k·ln n) |
| Bayes example? | 1% prevalence, 90% detection, 5% false alerts → only ~15% of alerts are true |

## Formulas
`SE(p)=√(p(1−p)/n)` · `z=(p̂−p0)/√(p0(1−p0)/n)` · `VIF=1/(1−R²)` · `AIC=2k−2lnL` · `BIC=k·ln n−2lnL` · `HL=Σ(O−E)²/(n·p̄(1−p̄))`

## Traps
- "p = 0.03 means 3% chance the model is fine" ✗
- "Not significant ⇒ no effect" ✗ (may be low power)
- Using DW with a lagged dependent variable ✗

## From my mock interviews (auto-updated)
_No entries yet._
