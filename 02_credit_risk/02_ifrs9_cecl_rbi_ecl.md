# 02.2 · IFRS 9, CECL and RBI ECL — build, monitor, validate

> You've monitored these models, so expect depth: staging/SICR mechanics, lifetime PD construction, PIT conversion, scenarios, overlays, and how you'd validate each. The India ECL transition (effective 1 Apr 2027) makes this the hottest topic for India-based roles in 2026–27.

---

## 1. IFRS 9 impairment in one page
- Effective for periods beginning **1 Jan 2018**, replacing IAS 39's *incurred-loss* model with an *expected-loss* model. **[Certain]**
- Applies to amortised-cost and FVOCI debt instruments, loan commitments, financial guarantees; trade/lease receivables can use the **simplified approach** (always lifetime ECL).
- ECL must be **unbiased and probability-weighted**, reflect the **time value of money**, and use **reasonable and supportable** information about past events, current conditions and forecasts.

### The three stages
| Stage | Condition | Allowance | Interest revenue on |
|---|---|---|---|
| **1** | Performing; no significant increase in credit risk (SICR) since origination | **12-month ECL** (lifetime losses from defaults possible in the next 12 months) | Gross carrying amount |
| **2** | **SICR** since initial recognition, not credit-impaired | **Lifetime ECL** | Gross carrying amount |
| **3** | Credit-impaired (default) | **Lifetime ECL** | Net carrying amount (amortised cost) |
| POCI | Purchased/originated credit-impaired | Lifetime ECL changes since recognition | Credit-adjusted EIR |

### SICR — the most-grilled IFRS 9 topic
- **Relative** comparison: credit risk now vs **at initial recognition** (not "is it risky now?").
- **Quantitative:** lifetime (or 12m as proxy) PD now vs origination — e.g., ratio > 2–3× **and** absolute increase > a floor (to avoid triggering on tiny PDs). **[Assumption — calibrated per bank]**
- **Qualitative:** watchlist, forbearance, significant adverse changes.
- **Backstop:** **30 DPD** rebuttable presumption. Default: **90 DPD** rebuttable presumption. **[Certain]**
- **Low credit risk** simplification (e.g., investment-grade): may assume no SICR.
- **Movement back:** assets return to Stage 1 when SICR no longer holds (often with probation rules).

> **Validator red flag:** if most Stage 2 transfers come via the 30 DPD backstop, the quantitative SICR criteria aren't working (they should catch deterioration *before* delinquency).

---

## 2. The ECL formula
```
ECL_s = Σ_{t=1..T}  PD_marginal(t | s) × LGD(t | s) × EAD(t) × DF(t)      (per scenario s)
ECL   = Σ_s  w_s × ECL_s                                                   (probability-weighted)
DF(t) = 1 / (1 + EIR)^t        (discount at the original effective interest rate)
```
- **Stage 1:** T covers defaults in the next 12 months. **Stages 2/3:** T = remaining lifetime.
- **Revolving products (cards):** lifetime = the period of actual credit-risk exposure (behavioural life), not the contractual period (IFRS 9 ¶5.5.20). **[Certain]**

**Worked toy example (per 100 of exposure):** cumulative PD 2% / 4.5% / 7% over 3 years → marginal 2.0% / 2.5% / 2.5%; EAD 100 / 70 / 40 (amortising); LGD 40%; EIR 10%.
→ **12-month ECL = 0.73**, **lifetime ECL = 1.61** → moving this loan to Stage 2 more than doubles its allowance (the "cliff effect").

**Why multiple scenarios?** Losses are **convex** in the economy (bad states hurt more than good states help), so ECL at the average scenario < average ECL across scenarios (Jensen's inequality). E.g., base/upside/downside ECL = 1.00 / 0.80 / 2.00 with weights 50/30/20% → weighted ECL = 0.50 + 0.24 + 0.40 = **1.14**, i.e., 14% above the base case: the upside saves only 0.20, the downside adds 1.00. **[Certain on principle]**
*(Sanity check an interviewer may run on you: upside ECL must be **below** base ECL, and the weighted ECL sits above base only because the downside is further from base than the upside is.)*

---

## 3. Building IFRS 9 PD (what you should be able to whiteboard)
1. **Start point:** often the Basel/behavioural model's rank-ordering (scores/grades).
2. **Strip regulatory conservatism:** remove MoC, downturn adjustments (IFRS 9 wants *unbiased* estimates).
3. **TTC → PIT:** link to the cycle. Common approach — **Vasicek one-factor (Z-factor):**
   ```
   PD_PIT(Z) = N( (N⁻¹(PD_TTC) − √ρ · Z) / √(1 − ρ) )      Z < 0 = bad economy
   ```
   *Example (verified):* PD_TTC 2%, ρ = 0.10 → Z = −1: **3.35%**; Z = −2: **6.70%**; Z = +1: **0.62%**; Z = 0: **1.52%** (below 2% because the default-rate distribution is right-skewed — the mean includes bad years).
   Estimate historical Z_t from observed default rates, regress Z on macro variables, then project Z under each scenario.
   *(This answers the common "how do you convert TTC PD to PIT PD?" question.)*
4. **Term structure (lifetime):**
   - **Markov chains:** cumulative PD from powers of the transition matrix (assumes time-homogeneity unless macro-adjusted).
   - **Survival / hazard models:** discrete-time hazard (logit on month-on-book + macro) or Cox models.
   - **Vintage/curve extrapolation:** fit default-timing curves by cohort.
5. **Forward-looking adjustment:** macro scenarios over the forecast horizon, then **mean reversion** to long-run levels.

**LGD (IFRS 9):** PIT, no downturn add-on, recoveries discounted at **EIR**, forward-looking collateral (house-price paths), cure modelling. **EAD:** amortisation and prepayment; CCF and behavioural life for revolving.

---

## 4. Scenarios and overlays
- **Scenarios:** typically 3–5 (base, upside, downside, severe), weights set by economics/risk committees; sources: in-house economists or vendors (e.g., Moody's Analytics, Oxford Economics). **[Likely]**
- **Validate:** scenario severity ordering, weight rationale, consistency with planning/ICAAP, MEV paths plausibility, sensitivity of ECL to weights.
- **Post-model adjustments (PMAs) / overlays:** used for model limitations, emerging risks (e.g., COVID support schemes, sector stress), data gaps.
  - **Validator questions:** what limitation does it address? how was it quantified? who approved it? when does it sunset? is it double-counting something the model already captures? is it monitored?

---

## 5. Monitoring & validation tests for IFRS 9 (component by component)
| Component | Tests |
|---|---|
| **Staging / SICR** | Stage migration matrix; % of new Stage 3 that were in Stage 2 beforehand ("hit rate"); time spent in Stage 2 before default; false-positive rate (Stage 2 cures); share of transfers via backstop; stability of Stage 2 volume |
| **12m PD** | Back-test by stage/segment (binomial, A/E); discrimination; PIT responsiveness |
| **Lifetime PD** | Cumulative default curves by vintage vs predicted |
| **LGD** | Realised vs predicted (completed workouts); cure-rate back-test; discount-rate correctness |
| **EAD / CCF** | Realised vs predicted; behavioural life evidence |
| **Macro models** | Stationarity, signs, back-test with realised macro, sensitivity (see `04_stress_testing_ccar.md`) |
| **Scenarios & weights** | Governance, reasonableness, sensitivity |
| **Overlays** | Quantification, governance, sunset, double-counting |
| **Implementation** | ECL engine replication on a sample; reconciliation to GL; data lineage |
| **ECL movement analysis** | Attribution: volume, mix, stage transfers, model/parameter changes, macro, overlays, write-offs |

---

## 6. CECL (US GAAP, ASC 326) — and how it differs
- Effective **2020** for SEC filers (excluding smaller reporting companies), **2023** for all others. **[Certain]**
- **Lifetime ECL from day one** — no staging.
- **Reasonable & supportable (R&S) forecast period**, then **reversion** to historical loss experience (immediate, straight-line or other systematic).
- **Methods:** discounted cash flow, loss-rate (pooled), vintage, roll-rate, PD × LGD, WARM (weighted-average remaining maturity) — choice depends on data and portfolio.
- **Qualitative (Q-) factors** adjust for conditions not in the model.
- **Unfunded commitments:** allowance only if **not unconditionally cancellable** — so card lines (unconditionally cancellable) carry no CECL allowance on the undrawn part, unlike IFRS 9's revolving treatment. **[Likely — check product terms]**
- **Regulatory capital:** transition options (3-year, and a 2020 COVID "2+3" relief). **[Likely]**

### IFRS 9 vs CECL vs Basel IRB
| Dimension | IFRS 9 | CECL | Basel IRB |
|---|---|---|---|
| Purpose | Accounting allowance | Accounting allowance | Regulatory capital |
| Horizon | 12m (Stage 1) / lifetime (2–3) | Lifetime always | 1-year PD |
| PD | PIT, forward-looking, unbiased | PIT/lifetime, R&S then reversion | TTC/hybrid, long-run average + MoC |
| LGD | PIT, EIR discounting | Varies by method | **Downturn**, conservative |
| Scenarios | Multiple, probability-weighted | Forecast + reversion (multiple optional) | No (stress tested separately) |
| Conservatism | None (unbiased) | None | MoC, floors |
| Undrawn revolving | Included (behavioural life) | Only if not unconditionally cancellable | CCF |

---

## 7. RBI ECL framework (India) — what's new in 2026
- **Final directions issued 27 Apr 2026** (after the **7 Oct 2025** draft); **effective 1 Apr 2027**. **[Certain]**
- **Applies to** commercial banks (excluding small finance banks, payments banks and local area banks), corresponding new banks and SBI. **[Certain — per KPMG summary]**
- **Three-stage** classification; **Stage 2 = 30–90 DPD** (plus SICR) with a **5% minimum provision**; **Stage 1 floor 0.40%** for standard corporate and retail loans; other product-wise prudential floors. Banks' requests for lower floors and softer Stage 2 thresholds were **not** accepted in the final text. **[Likely — per Uniqus/CRISIL summaries of the final Directions; read the floor table in the Directions before quoting product-level numbers]**
- Requires **EIR** method (legacy loans must move to EIR by **31 Mar 2030**), PD/LGD/EAD models with **macroeconomic inputs**, **board oversight via a committee including CFO and CRO**, and **model risk management** for ECL models. **[Certain on governance — KPMG; Likely on the EIR legacy date]**
- **Transition:** the one-time CET1 hit is added back on a **4-year taper — 4/5, 3/5, 2/5, 1/5 from FY2027-28 to FY2030-31**; CRISIL estimates a one-time net **CET1 impact of up to ~120 bps**. **[Likely]**
- **Interview angle (VP bar):** the floors mean that for many low-risk books the *floor*, not the model, sets the provision — so a validator must report "floor-binding vs model-driven" exposure, and model-performance tests still matter because Stage 2/3 lifetime ECL and SICR are model-driven.
- **NBFCs** already apply **Ind AS 109** ECL (phased in from FY2018–19 for large NBFCs). **[Likely]**
- **Why it matters for you:** Indian banks, Big 4 and GCCs serving Indian banks need ECL modellers *and validators* through 2027 — and the RBI's draft MRM guidance (Jun 2026) raises the validation bar further.

---

## 8. Interview questions (with the core of the answer)
1. **Explain the three stages.** (Table §1, + interest-revenue basis.)
2. **What triggers SICR at your client?** (Your actual criteria; then: relative vs origination, quantitative + qualitative + 30 DPD backstop.)
3. **How do you validate SICR thresholds?** (Hit rate, time in Stage 2, false positives, backstop share, stability; compare alternative thresholds.)
4. **12-month vs lifetime PD — how built?** (§3.)
5. **TTC → PIT conversion?** (Vasicek Z-factor; or macro regression on PD/default rates.)
6. **Why multiple scenarios?** (Convexity/Jensen.)
7. **What's an overlay and how do you challenge it?** (§4.)
8. **IFRS 9 PD vs Basel PD?** (PIT vs TTC; no MoC/downturn; lifetime; discounting.)
9. **IFRS 9 vs CECL?** (Staging, horizon, reversion, unfunded commitments.)
10. **What drove last quarter's ECL change?** (Movement analysis: volume, mix, staging, parameters, macro, overlays, write-offs.)
11. **RBI ECL — key features and impact?** (§7.)
12. **How did COVID affect your models?** (Support schemes suppressed defaults → macro-default links broke → overlays; data treatment in re-estimation.)
