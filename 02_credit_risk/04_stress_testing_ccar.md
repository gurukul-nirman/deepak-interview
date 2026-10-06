# 02.4 · Stress Testing (CCAR/DFAST, ICAAP) — models, diagnostics, validation

> You've monitored stress-testing models, so you'll be asked to defend econometric choices. Run `05_coding/code/stress_test_diagnostics.py` once — every number in §6 comes from it.

---

## 1. What and why
- **Purpose:** will the bank stay adequately capitalised (and keep lending) in a severe but plausible recession?
- **Types:** regulatory (supervisory scenarios) · internal/ICAAP (Pillar 2) · sensitivity (one factor) · **reverse stress test** (what scenario breaks us?).

## 2. US: DFAST and CCAR (what to know cold)
- Large US bank holding companies (≥ $100bn, tailored by category) are subject to the Fed's **supervisory stress test (DFAST)** and the **capital plan rule (CCAR)**. **[Likely — category details vary]**
- Fed scenarios: **baseline** and **severely adverse**; **9-quarter** projection horizon. **[Certain]**
- **Stress capital buffer (SCB)** = max(2.5%, peak-to-trough decline in CET1 ratio under the severely adverse scenario + four quarters of planned common dividends as % of RWA). **[Certain]**
- Banks also run **company-run** stress tests with their own models (that's what GCC teams build/monitor/validate).

### 2026 changes — say this and you sound current **[Certain — Fed press release, 30 Sep 2026]**
- Final rules require the Fed to **invite public comment annually on stress-test scenarios and material model changes**; update the scenario-design framework; adopt the models for the **2027** test; adjust the calendar.
- Banks with large trading books face **two global market shock components** each year (the worse one counts).
- **SCB averaging:** use the average of the **two most recent** stress tests — **starting 2028**.
- A proposal to revise the Fed's **non-interest income model** to capture business-model differences.
- Expected effect: ~**50% lower year-over-year volatility** in capital requirements, without materially changing aggregate requirements.

## 3. Other regimes (one line each)
- **EU:** EBA EU-wide stress test (biennial; next 2027) with a constrained bottom-up methodology. **[Likely]**
- **UK:** Bank of England system-wide stress testing; PRA expectations for ICAAP. **[Likely]**
- **ICAAP (Pillar 2):** firm-specific scenarios, including reverse stress tests.
- **India:** stress testing within banks' ICAAP and RBI's macro stress tests in the Financial Stability Report. **[Likely]**

## 4. Model landscape
| Model type | Target | Approach |
|---|---|---|
| **Credit loss — top-down** | Portfolio NCO rate / loss rate | Time-series regression on macro variables (MEVs), often with an AR term |
| **Credit loss — bottom-up** | Account/segment PD, LGD, EAD | Loan-level PD/LGD models with macro drivers (or Z-factor shifts), aggregated |
| **Balance / volume** | Balances, originations, paydowns | Regression on macro + management assumptions |
| **PPNR** | Net interest income, non-interest income, expenses | Rate-path models, fee models, expense regressions |
| **Operational risk** | Op-risk losses | Regression/frequency-severity |
| **Market shock** | Trading/counterparty losses | Instantaneous shocks |

Bottom-up = granular, consistent with BAU models, data-hungry; top-down = simple, robust, less granular. Validators check that both tell a consistent story where both exist.

## 5. Building a macro-driven loss model (the steps you'll be asked to defend)
1. **Target:** e.g., quarterly NCO rate for business cards; define clearly (gross vs net, annualised).
2. **Data:** history covering at least one full cycle (2005+ captures the GFC); document structural breaks (product/policy changes, COVID).
3. **MEV candidates with economic rationale:** unemployment (level/change), GDP growth, house prices, CRE prices, rates/spreads (BBB spread), equity/VIX, small-business indicators for SME books.
4. **Transformations:** differences, YoY growth, logit of rates; **lags** (unemployment hits losses with a 1–4 quarter delay).
5. **Expected signs** written *before* estimation (unemployment ↑ → losses ↑; GDP ↑ → losses ↓).
6. **Estimation:** OLS/ARIMAX/panel; keep it parsimonious (2–4 MEVs).
7. **Diagnostics** (§6) and **selection** on out-of-sample performance, not in-sample R².
8. **Scenario projection** (dynamic, 9 quarters), **sensitivity** to each MEV, **overlays** with governance.

## 6. Diagnostic battery (verified output of the practice script)
| Check | Test | Practice-script result | Read |
|---|---|---|---|
| Stationarity | ADF (H0 unit root) + KPSS (H0 stationary) | Δunemployment stationary; NCO level ADF p = 0.27 | Persistent target → AR term or differencing; test cointegration for level models |
| Signs/significance | OLS with **Newey–West (HAC) SEs** | ΔUR +0.50, GDP −0.04, NCO lag +0.77, COVID dummy −0.11 | Signs intuitive; COVID dummy captures stimulus-suppressed losses |
| Autocorrelation | **Breusch–Godfrey** (DW biased with a lagged dependent variable) | BG p = 0.16; DW 2.01 | No evidence of residual autocorrelation |
| Heteroskedasticity | Breusch–Pagan | p = 0.17 | OK |
| Normality | Jarque–Bera | p = 0.64 | OK |
| Multicollinearity | VIF | max ≈ 2.4 | OK |
| Out-of-time back-test | Fit 2005–2019, dynamic forecast 2022–2025 | MAPE 10.9%, cumulative error +8.4% | Over-predicts slightly (conservative) |
| Sensitivity | +1pp shock to ΔUR | +0.59pp immediate; **+2.16pp long-run** (β/(1−ρ)) | Persistence amplifies shocks — explain this |
| Stability | Rolling 40-quarter coefficients | ΔUR coefficient 0.56–0.61 | Stable; sign flips would be a finding |

## 7. Back-testing and ongoing performance assessment
- **Dynamic back-test** (model feeds on its own lags, like a 9-quarter projection), not one-step-ahead.
- **Realised-macro back-test:** re-run last year's projection with the *actual* macro path; compare to actual losses.
- Metrics: MAPE, cumulative error over the horizon, peak-loss error, direction of error (under-prediction is worse).
- Annual: re-estimate with new data; coefficient stability; benchmark/challenger; overlay review.

## 8. Sensitivity and scenario analysis
- Shock each MEV ±1σ and joint shocks; check **monotonicity** (more severe scenario → higher losses) and **timing** (peak loss quarters plausible).
- Check scenario **expansion** (national → regional variables) is validated too.

## 9. Common validation findings (memorise 8)
1. **Spurious regression** — non-stationary levels without cointegration.
2. **Counter-intuitive signs** retained for fit.
3. **Overfitting** — too many MEVs/lags for ~60–80 quarterly observations.
4. **Ignored autocorrelation** → overstated significance.
5. **Insufficient downturn coverage** → under-prediction in severe scenarios.
6. **COVID anomaly** untreated — support schemes broke the unemployment→loss link; needs dummies/exclusion **with sensitivity** shown both ways.
7. **Non-monotonic or too-fast-reverting** responses under the severely adverse scenario.
8. **Overlays** without quantification, approval or sunset; inconsistent assumptions between loss, balance and PPNR models.

## 10. Interview questions
1. **How do you choose MEVs?** Economic rationale first, then correlation/lag analysis, then out-of-sample performance; parsimony; expected signs documented upfront.
2. **Your target isn't stationary — what do you do?** Difference/transform, add an AR term, or test cointegration and use an error-correction model.
3. **Why HAC standard errors?** Autocorrelation/heteroskedasticity make OLS SEs too small.
4. **Durbin–Watson with a lagged dependent variable?** Biased toward 2 → use Breusch–Godfrey or Durbin's h.
5. **How do you treat COVID data?** Identify the break, test dummy vs exclusion vs robust estimation, show sensitivity, document the judgment; overlays where models can't capture support effects.
6. **How do you back-test a stress-test model when stress scenarios never happen?** Back-test on realised macro paths, dynamic out-of-time, historical episodes (GFC), benchmarks, sensitivity.
7. **What is the SCB and what changes from 2028?** §2.
8. **Top-down vs bottom-up?** §4.
9. **How would you validate scenario reasonableness?** Severity vs history, internal consistency across MEVs, monotonic loss response, comparison with supervisory scenarios.
10. **What's the long-run effect of a shock in an AR(1) loss model?** β/(1 − ρ).
