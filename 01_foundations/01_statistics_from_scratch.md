# 01.1 · Statistics from Scratch (only what validation interviews use)

> Assume nothing. Each section ends with the interview-ready one-liner. Pareto: §5 (hypothesis testing), §6 (validation tests table), §8 (regression assumptions) and §10 (time series) produce most of the questions.

---

## §1. Describing data
- **Variable types:** continuous (balance), discrete (# inquiries), categorical (industry), ordinal (risk grade), binary (default flag).
- **Centre:** mean (sensitive to outliers), median (robust — use for skewed balances/income), mode.
- **Spread:** variance σ² = average squared deviation; standard deviation σ; percentiles; IQR = P75 − P25.
- **Shape:** skewness (credit balances are right-skewed), kurtosis (fat tails → losses).
- **Outliers:** IQR rule (beyond P75 + 1.5·IQR), capping/winsorising at P1/P99 — *document it; validators check it.*

> **One-liner:** "For skewed credit variables I look at medians and percentiles, and I cap outliers at documented percentiles rather than delete them."

---

## §2. Probability you actually use
- **Conditional probability:** P(A|B) = P(A∩B)/P(B). *Bad rate in a score band is P(bad | band).*
- **Bayes' theorem:** P(A|B) = P(B|A)·P(A)/P(B).
  *Example:* fraud prevalence 1%; alert catches 90% of frauds; false-alert rate 5%. P(fraud | alert) = 0.9×0.01 / (0.9×0.01 + 0.05×0.99) = 0.009 / 0.0585 = **15.4%**. → Low prevalence crushes precision. (Classic quant-screen question.)
- **Independence:** P(A∩B) = P(A)P(B). *Defaults are NOT independent in reality (common macro factor) — which is why binomial tests are too strict and why Basel uses an asset correlation.*
- **Expected value:** E[X] = Σ x·p(x). *Expected loss EL = PD × LGD × EAD is an expected value.*

---

## §3. Distributions (what each models in credit)
| Distribution | Models | Key facts |
|---|---|---|
| Bernoulli / **Binomial** (n, p) | Default yes/no; # defaults in a grade | mean np, variance np(1−p) |
| Poisson (λ) | Counts: inquiries, delinquencies | mean = variance = λ |
| **Normal** (μ, σ) | Test statistics; Vasicek factor model | 68–95–99.7 rule; z-scores |
| Log-normal | Exposures, balances | log is normal; right-skewed |
| **Beta** (a, b) | LGD (bounded 0–1); uncertainty about a PD (Jeffreys) | flexible on [0,1] |
| t | Small-sample mean tests | fatter tails than normal |
| **χ²** | HL test, goodness-of-fit, independence | sum of squared normals |
| F | Joint significance in regression | ratio of χ²'s |

- **Law of Large Numbers:** sample average → true mean as n grows.
- **Central Limit Theorem:** the sampling distribution of the mean is ~normal for large n (whatever the underlying distribution) → justifies z-tests and CIs.

---

## §4. Sampling, standard errors, confidence intervals
- **Standard error of a proportion:** SE = √(p(1−p)/n).
- **95% CI:** p ± 1.96·SE. *Example:* bad rate 5% on 2,000 accounts → SE = 0.49% → **CI 4.0%–6.0%**. With 200 accounts → ±3.0% — useless for fine conclusions.
- **Sampling designs:** simple random · **stratified** (by segment/vintage — keeps mix) · **oversampling bads** (fix later with weights or an intercept adjustment, see scorecards §11).
- **Bootstrap:** resample with replacement many times → distribution of any statistic (e.g., Gini CI) without formulas.

> **One-liner:** "Before calling a change real I look at its confidence interval — with 40 bads, a 5-point Gini move is noise."

---

## §5. Hypothesis testing (the most misunderstood topic)
- **H0** (null: no effect / model is fine) vs **H1** (alternative).
- **Test statistic** → **p-value** = probability of data at least this extreme **if H0 were true**. It is **not** the probability that H0 is true.
- **α (significance level, e.g., 5%)**: reject H0 if p < α.
- **Type I error** (false positive): reject a true H0 — e.g., flag a good model as broken. Probability = α.
- **Type II error** (false negative): fail to reject a false H0 — e.g., miss a broken model. **Power** = 1 − P(Type II).
- **One-sided vs two-sided:** PD back-testing is usually **one-sided** (worried about *under*-estimation).
- **Large samples:** everything becomes "significant" → judge **practical significance** (effect size) too.
- **Multiple testing:** testing 20 grades at 5% → ~1 false alarm expected; use traffic-light logic or adjust.

> **One-liner:** "A p-value of 0.03 means that if the PD were correct, results this extreme would occur 3% of the time — so I reject at 5% but I also look at the size of the gap and its business impact."

---

## §6. The tests validators use (memorise the purpose column)
| Test | Purpose | H0 | Used for |
|---|---|---|---|
| **t-test** (one/two-sample, paired) | Compare means | means equal | LGD realised vs predicted |
| **χ² goodness-of-fit / independence** | Observed vs expected counts | fit is good / independent | Calibration across grades; variable vs target |
| **Binomial test** | # defaults vs PD | PD correct | PD back-test per grade |
| **Jeffreys test** | Bayesian PD back-test | PD ≥ true DR (not under-estimated) | ECB IRB reporting |
| **Hosmer–Lemeshow** | Logistic calibration | model calibrated | PD models |
| **KS two-sample** | Two distributions equal | same distribution | Score separation goods vs bads; drift |
| **Mann–Whitney U** | Rank difference | same distribution | = AUC |
| **DeLong** | Two correlated AUCs | AUCs equal | Champion vs challenger |
| **Spearman / Kendall** | Rank correlation | no monotonic association | Rank-ordering; variable screening |
| **Shapiro–Wilk / Jarque–Bera** | Normality | normal | Regression residuals |
| **ADF / Phillips–Perron** | Unit root | **non-stationary** (unit root) | Stress-test series |
| **KPSS** | Stationarity | **stationary** | Complements ADF |
| **Durbin–Watson / Breusch–Godfrey / Ljung–Box** | Autocorrelation | no autocorrelation | Time-series residuals (BG valid with lagged dependent variable; DW isn't) |
| **Breusch–Pagan / White** | Heteroskedasticity | constant variance | Regression residuals |
| **Chow** | Structural break | no break | Pre/post-COVID, regime changes |
| **Engle–Granger / Johansen** | Cointegration | no cointegration | Levels regressions with non-stationary series |
| **Wald / Likelihood-ratio / Score** | Coefficient significance; nested models | coefficient(s) = 0 | Logistic regression |
| **F-test** | Joint significance | all slopes = 0 | OLS |
| **VIF** (diagnostic, not a test) | Multicollinearity | — | > 5–10 is a concern |

**Trap:** ADF and KPSS have **opposite nulls**. Stationary if ADF rejects *and* KPSS does not. (In statsmodels the KPSS p-value is capped at 0.10 — "≥ 0.10" means you can't reject stationarity.)

---

## §7. Correlation
- **Pearson:** linear association (−1 to 1); sensitive to outliers.
- **Spearman:** rank-based; captures monotonic non-linear relationships. **Kendall's τ:** another rank measure, robust in small samples.
- **Correlation ≠ causation.** In time series, two trending series correlate spuriously — difference them or test cointegration.

---

## §8. Linear regression (OLS) — needed for stress testing, LGD, and as the foundation for logistic
**Model:** y = β₀ + β₁x₁ + … + ε, estimated by minimising Σ residuals².

**Assumptions & what breaks if violated:**
| Assumption | Violation | Consequence | Detect | Fix |
|---|---|---|---|---|
| Linearity | Curved relationship | Biased predictions | Residual plots | Transform, splines, bins |
| Independence of errors | Autocorrelation (time series) | SEs too small → false significance | DW, BG, Ljung–Box | Lags, HAC (Newey–West) SEs, ARIMA errors |
| Homoskedasticity | Variance changes with x | SEs wrong | BP, White | Robust SEs, WLS, log transform |
| Normality of errors | Fat tails/skew | Inference unreliable in small samples | JB, QQ-plot | Transform; large n helps (CLT) |
| No perfect multicollinearity | Correlated X's | Unstable coefficients, sign flips, inflated SEs | VIF, correlations, condition index | Drop/combine variables, PCA, regularisation |
| Exogeneity | Omitted variable / reverse causality | Biased coefficients | Theory, tests | Add variables, instruments |

**Read-outs:** coefficient (effect of +1 unit), t-stat & p-value, R² (share of variance explained), adjusted R² (penalises extra variables), F-test (joint), AIC/BIC (lower is better; BIC penalises complexity more).

> **One-liner on multicollinearity:** "It doesn't bias predictions much, but it makes individual coefficients unstable and can flip signs — fatal for an interpretable credit model, so I check VIF and economic signs."

---

## §9. Maximum likelihood (why logistic regression works)
- **Likelihood:** probability of the observed data given parameters. **MLE** picks parameters that maximise it.
- For logistic regression: log-likelihood = Σ [y·ln p + (1−y)·ln(1−p)] — no closed form → iterative (Newton–Raphson / IRLS).
- **Deviance** = −2 × log-likelihood; **LR test** compares nested models: Δdeviance ~ χ²(Δparameters).
- **AIC** = 2k − 2lnL; **BIC** = k·ln(n) − 2lnL.
- **Separation:** if a variable perfectly predicts the outcome, MLE doesn't converge (coefficients → ∞) — merge bins or use penalised (Firth) regression.

---

## §10. Time-series essentials (for stress testing & IFRS 9 macro models)
- **Stationarity:** constant mean/variance/autocorrelation over time. Most macro *levels* (GDP, house prices, unemployment level) aren't; *changes/growth rates* usually are.
- **Spurious regression:** regressing one non-stationary series on another gives high R² and "significant" coefficients with no real relationship. Fix: difference, or confirm **cointegration** (a stationary linear combination exists → levels regression is meaningful; error-correction model).
- **Autocorrelation:** residuals correlated over time → understated SEs. ACF/PACF plots; AR terms or HAC SEs.
- **Lags:** macro shocks hit losses with delay (unemployment → delinquencies 2–4 quarters later). Choose lags with theory + information criteria, not data-mining.
- **ARIMA(p,d,q):** AR order p, differencing d, MA order q; **ARIMAX** adds exogenous macro drivers.
- **Structural breaks:** 2008–09, COVID-2020 (government support broke the unemployment→loss link). Test (Chow), then treat (dummy, exclusion with justification, or robustness checks).
- **Dynamic forecasting:** in a 9-quarter stress projection the model feeds on its own lagged predictions — errors compound, so back-test dynamically, not one-step-ahead.

See `05_coding/code/stress_test_diagnostics.py` for every test above, run on synthetic data.

---

## §11. Overfitting and validation samples
- **Bias–variance trade-off:** simple models underfit (bias); complex models overfit (variance).
- **Samples:** train (fit) · in-time holdout/test (generalisation) · **out-of-time** (later period — the real test for credit) · out-of-population (new segment).
- **Cross-validation:** k-fold for tuning; use time-aware splits for temporal data.
- **Signs of overfitting:** train Gini ≫ test/OOT Gini; many tiny bins; unstable coefficients across samples.

---

## §12. Formula sheet (write these from memory by end of Week 1)
```
SE(p)            = sqrt(p(1−p)/n)               95% CI = p ± 1.96·SE
z (proportion)   = (p̂ − p0) / sqrt(p0(1−p0)/n)
Bayes            P(A|B) = P(B|A)P(A) / P(B)
EL               = PD × LGD × EAD
logit            ln(p/(1−p)) = β0 + Σβx      p = 1/(1+e^(−z))
Odds ratio       e^β  (multiplicative change in odds for +1 unit)
VIF_j            = 1/(1 − R²_j)
AIC = 2k − 2lnL   BIC = k·ln(n) − 2lnL
Gini             = 2·AUC − 1
KS               = max |F_bad − F_good|
PSI              = Σ (A − E)·ln(A/E)
WoE              = ln(%Good/%Bad)      IV = Σ (%Good − %Bad)·WoE
HL               = Σ (O − E)² / (n·p̄·(1 − p̄))  ~ χ²(g−2)
```
