# 04 · Positioning, Resume & Project Stories

> **Why this file is #1 priority:** ~30% of interview time is spent drilling *your own* projects. Interviewers at this level don't stop at the first answer — they push 4–5 follow-ups deep until they find the edge of your knowledge. The goal here is to move that edge further out and to make every claim defensible.

---

## 1. Your positioning (one sentence)

> **"Credit risk model specialist with 5 years across IFRS 9/CECL, Basel IRB and CCAR stress-testing models plus FICO SBSS small-business scorecards — moving from first-line performance monitoring into independent validation / MRM."**

Three ideas to land in every round:
1. **Breadth across all three regulatory uses** (provisioning, capital, stress testing) — rare at 5 years. **[Likely — most candidates have one or two]**
2. **Vendor-model experience** (FICO SBSS) — directly relevant to a core MRM problem: validating models you don't own the code for.
3. **You already think like a validator** — root causes, thresholds, challenge, remediation — and want to own it end to end.

---

## 2. Framing the KPO / vendor-side experience

Interviewers will probe: *"Were you executing a client's process, or making judgments?"*

| Don't say | Say instead |
|---|---|
| "I ran the monitoring code every quarter." | "I owned the quarterly monitoring for [N] models — execution, breach diagnosis, and the commentary that went to the model owner and MRM." |
| "The client decided." | "I recommended the action; the model owner/MRM approved it. In [example] my recommendation was [accepted/modified] because…" |
| "I'm an analyst at a vendor." | "I'm embedded with a [top-10 US bank] client's credit risk modeling team, working to their MRM standards and supporting their validation and audit reviews." |

**Confidentiality:** Name the client only if your contract allows. "A top-10 US bank" is acceptable and common. **[Likely]**

---

## 3. Monitoring → validation bridge (use this vocabulary)

| What you did | Validation term (SR 11-7/SR 26-2 language) | How to say it in an interview |
|---|---|---|
| Quarterly KS/Gini/PSI/CSI, bad-rate by band | **Ongoing monitoring + outcomes analysis** | "I executed the ongoing-monitoring component — discrimination, calibration and stability against MRM thresholds." |
| Investigated a breach | **Root-cause analysis, effective challenge** | "I separated population shift from performance deterioration before recommending action." |
| Wrote breach commentary | **Findings & recommendations** | "I wrote the finding, its likely cause, impact, and the recommended remediation." |
| Reconciled monitoring data to source | **Data integrity / process verification** | "I reconciled monitoring inputs to the system of record and flagged [N] data issues." |
| Rebuilt or reviewed monitoring code | **Replication / implementation testing** | "I independently re-coded the metrics and matched production outputs." |
| Compared segments (BCC vs non-BCC), vintages | **Segmentation & sensitivity analysis** | "I tested whether performance held across segments and vintages." |
| Supported MRM validation / audit / regulator requests | **Governance & regulatory interaction** | "I prepared evidence and responses for [validation/audit] reviews." |
| Tracked overlay / PMA usage | **Model limitations & compensating controls** | "I monitored the overlay and its trigger conditions." |

---

## 4. Resume — structure and bullet formula

**Structure (2 pages max):**
1. Header + headline: *Credit Risk Model Monitoring & Validation | IFRS 9 / CECL | Basel IRB | CCAR | SAS · SQL · Python*
2. Summary (3 lines — your positioning sentence + scale + what you want)
3. Experience (5–7 bullets per role, **numbers in every bullet**)
4. Skills (Regulatory: SR 11-7 / SR 26-2, IFRS 9, CECL, Basel IRB, CCAR/DFAST, PRA SS1/23 awareness · Techniques: LR, scorecards, WoE/IV, KS/Gini/PSI, calibration tests, time-series diagnostics, GBM/SHAP · Tools: SAS, SQL, Python, Tableau)
5. Education, certifications (FRM/CFA/CQF if any — "FRM Part I candidate, May 2027" is acceptable only if registered)

**Bullet formula:** `Verb + model/portfolio + method + scale + outcome`

**Templates — fill with your real numbers; never invent:**
- Owned quarterly performance monitoring for **[N] credit risk models** (IFRS 9 PD/LGD/EAD, Basel IRB PD, CCAR loss models, FICO SBSS small-business scorecards) for a **top-[X] US bank** client covering **$[X] bn** exposure; tested discrimination (KS/Gini), calibration (binomial/HL) and stability (PSI/CSI) against MRM thresholds.
- Diagnosed a **[PSI 0.2x / Gini drop of x pts]** breach in the **[BCC]** segment, traced to **[root cause]**; recommended **[recalibration/overlay/redevelopment]**, adopted by model owner and MRM, **[impact: $ / bps / approval-rate change]**.
- Built/automated the monitoring pack in **SAS/SQL [and Python]**, cutting cycle time from **[X] to [Y] days** and removing **[N]** manual steps.
- Supported **[MRM validation / internal audit / regulatory exam]** by preparing evidence and responses for **[N]** requests/findings.
- Performed backtesting of **[stress-test loss model]** against realised outcomes; identified **[issue]**; informed the **[annual model review]**.
- Reviewed code and outputs of **[N]** junior analysts; created **[standard/checklist]** adopted by team.

**ATS keywords to include (from 2026 JDs):** model validation, model risk management, effective challenge, conceptual soundness, outcomes analysis, backtesting, benchmarking, challenger model, sensitivity analysis, replication, PD/LGD/EAD, IFRS 9, CECL, IRB, CCAR/DFAST, SR 11-7, SR 26-2, Python, PySpark (only if true), SAS, SQL, machine learning, SHAP.

---

## 5. "Tell me about yourself" — 90-second script (customise, then record)

> "I'm [Name], a credit risk modeling professional with five years in model performance monitoring for a [top-10 US bank] client through [Company].
> I've worked across all three regulatory uses of credit models — **IFRS 9/CECL provisioning, Basel IRB capital, and CCAR stress testing** — plus **FICO SBSS-based small-business scorecards** for business credit cards and loans.
> My core work is testing discrimination, calibration and stability in SAS and SQL, diagnosing breaches, and writing the commentary that goes to model owners and MRM.
> For example, [one 20-second breach story: metric → root cause → action → result].
> Over the past year more of my work has looked like validation — challenging root causes, benchmarking, reviewing remediation — and that's what I want to own end to end in an independent second-line role.
> That's why this [role] at [bank] appeals to me: [one specific reason — their model mix / AI validation / regulatory scope]."

**Rules:** ≤ 90 seconds; one number; end with *why this role*. Practise until it sounds unrehearsed.

---

## 6. Project deep-dive sheets (fill one per project — this is your highest-ROI prep)

### 6.0 Universal sheet (copy for each project)

```
PROJECT: ______________________   CLIENT/PORTFOLIO: ______________
Model purpose & use (decisions it drives): __________________________
Regulatory use (IFRS9 / CECL / IRB / CCAR / business): _______________
Model type & method (LR scorecard, vendor score, PD term structure, time-series regression…): ____
Owner / developer / validator / you (3 lines of defence): ______________
Data: source, period, # obs, # bads/defaults, default/bad definition, performance window: ____
Key variables / MEVs (top 5) and signs: ______________________________
Development performance (Gini/KS/AUC, R²/MAPE for regressions): _______
Monitoring metrics you ran + thresholds (Green/Amber/Red): ____________
Frequency & tooling (SAS/SQL/Python, automation): ____________________
Latest results (numbers!): __________________________________________
A breach/issue you handled: metric → root cause → action → who approved → outcome
Limitations of the model (3): _______________________________________
What you'd improve / do differently: _________________________________
```

### 6.1 FICO SBSS scorecards — Business Credit Card (BCC) and non-BCC

*Confirmed: BCC = business credit card; non-BCC = other small-business products (loans/lines).*

**Facts you must know cold [Certain]:**
- **SBSS = FICO® Small Business Scoring Service** — a **vendor** score for small-business credit, range **0–300** (higher = lower risk).
- Blends **consumer credit of the principal(s)**, **business bureau data**, and application/financial data. **[Likely — vendor-described inputs]**
- Used by SBA for 7(a) small-loan prescreening; minimum raised 155 → **165** (2025). **SBA discontinued SBSS screening for 7(a) small loans effective 1 Mar 2026** (Procedural Notice 5000-875701, 16 Jan 2026; supplemental 5000-876777, 20 Feb 2026); lenders may use their own internal scoring as long as it doesn't rely solely on consumer scores.

**Grilling questions to prepare (answer each in 3–5 sentences on your sheet):**
1. What is SBSS, what's the range, what goes into it?
2. It's a vendor model — how do you monitor/validate it without the code? *(conceptual soundness from vendor docs; local outcomes analysis on your population; stability; score-to-odds alignment; segment testing; limitations; vendor change management)*
3. What's the bad definition and performance window for BCC vs non-BCC — and why might they differ? *(revolving vs installment behaviour; charge-off timing; utilisation)*
4. Development vs latest KS/Gini for each segment. Thresholds used. Trend.
5. How was PSI computed — reference period, bins, any empty-bin handling?
6. A breach you saw — root cause — action — approval.
7. How is the score *used*: cutoffs, line assignment, pricing, manual review bands? Did you monitor approval rates, overrides, swap-in/swap-out?
8. How do you assess calibration of a score that isn't a PD? *(odds-by-score-band vs expected log-odds line; compare to vendor odds chart; logistic recalibration if needed)*
9. Low bad counts in a segment — how did you handle significance? *(pool periods, confidence intervals, bootstrap Gini, binomial CIs)*
10. Thin-file / no-hit businesses and young businesses — performance and treatment?
11. **SBA's March 2026 SBSS change — what are the implications for the bank's models and monitoring?** *(use-case change → model-use review; population shift if SBA small loans now underwritten differently; possible move to internal scorecard → new model validation; monitor approval/default mix; update the inventory's use description)*
12. Generic vendor score vs custom scorecard — pros/cons.
13. FICO releases a new SBSS version — what's your process? *(model change → impact analysis: parallel run, swap-set, re-baseline thresholds; MRM notification/validation)*
14. Any overlays or policy rules layered on the score?
15. What would you change in the monitoring design?

### 6.2 SmarterPay models — **not yet started (KT expected Oct 2026)**
- **Do not claim it** in your resume or interviews until you've actually worked on it. If asked about current work: *"I'm being onboarded to the SmarterPay models; knowledge transfer starts this month."*
- **After the KT:** capture purpose, target definition, method, data, monitoring metrics, thresholds and limitations in the universal sheet (§6.0); then ask me for `START TOPIC T12 SmarterPay` to build and test the story.

### 6.3 IFRS 9 / CECL models
**Grilling questions:**
1. Which portfolio and components did you monitor (12m PD, lifetime PD term structure, LGD, EAD/CCF, staging/SICR, macro satellite models)?
2. How is lifetime PD constructed (transition matrices / survival / vintage-hazard / PIT-adjusted)?
3. What are the SICR rules — relative/absolute PD thresholds, watchlist, 30 DPD backstop? How did you monitor staging quality? *(stage migration, % of Stage 3 previously in Stage 2, time in Stage 2, cure rates)*
4. PD backtesting approach and results (by stage/segment; observed vs predicted 12m default rate).
5. Macro scenarios: how many, weights, MEVs, source; how did you check scenario reasonableness?
6. Overlays/PMAs: how big, why, how governed, how monitored?
7. ECL movement analysis: what drove last quarter's change? *(volume, mix, staging, model, macro, overlay)*
8. IFRS 9 PD vs Basel PD — differences and why. *(PIT vs TTC, no MoC/downturn, lifetime, discounting at EIR)*
9. CECL vs IFRS 9 — key differences. *(no staging, lifetime from day 1, reversion, Q-factors)*
10. COVID-era data: how treated?

### 6.4 Basel IRB models
1. Asset class (retail mortgage / QRRE / other retail / corporate)? Which parameters (PD/LGD/EAD-CCF)?
2. Rating philosophy (PIT / TTC / hybrid) — evidence?
3. Calibration: long-run average default rate, central tendency, margin of conservatism (EBA categories A/B/C).
4. Monitoring tests per grade: binomial/Jeffreys, Hosmer–Lemeshow; AUC vs development; migration matrix; concentration (HHI); override rates.
5. Downturn LGD approach; LGD backtesting (realised vs estimated).
6. Default definition (90 DPD + unlikeliness-to-pay; materiality thresholds; probation) — any change and its impact?
7. Use test — where are IRB parameters used beyond capital?
8. How did monitoring results feed the annual validation / regulatory reporting?

### 6.5 Stress testing (CCAR / DFAST / ICAAP)
1. Which models: loss (PD/LGD/EAD or NCO-rate), balance, PPNR? Top-down or bottom-up?
2. Dependent variable, MEVs, transformations (diff, YoY, lags) — and economic rationale for each sign.
3. Diagnostics: stationarity (ADF/KPSS), multicollinearity (VIF), autocorrelation (DW/Breusch–Godfrey), heteroskedasticity (Breusch–Pagan/White), normality, structural breaks.
4. Backtesting / out-of-sample results (e.g., MAPE, cumulative error over 9 quarters).
5. Sensitivity analysis and scenario reasonableness (severely adverse vs baseline).
6. Overlays / management adjustments — governance.
7. COVID period treatment (dummy, exclusion, robustness checks).
8. Ongoing monitoring for a stress model (annual performance assessment, realised-macro backtest, benchmark).
9. 2026 Fed changes (scenario/model public comment; SCB averaging from 2028; two global market shocks). **[Certain — Fed press release 30 Sep 2026]**

---

## 7. LinkedIn

- **Headline:** Credit Risk Model Monitoring & Validation | IFRS 9 / CECL | Basel IRB | CCAR Stress Testing | SAS · SQL · Python
- **About (4 lines):** positioning sentence · scale (models, exposure) · 2 achievements with numbers · "Open to model validation / MRM roles (India, UAE)".
- Turn on **Open to Work → recruiters only**.

---

## 8. Questions to ask interviewers (signal VP-level thinking)

1. "With SR 26-2 replacing SR 11-7, are you moving Tier 1 models off a fixed annual cycle to a risk-based cadence? How is that being decided?"
2. "What share of the inventory is ML/AI now, and how do you validate explainability and fairness?"
3. "How are validation findings tracked and challenged at committee — what's the typical time-to-closure for High findings?"
4. "What would make someone in this role exceptional in the first 90 days?"
5. "How much of the work is initial validation vs periodic review vs change validation?"
