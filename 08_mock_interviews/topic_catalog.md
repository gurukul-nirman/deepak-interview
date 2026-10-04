# Topic Catalog — what each topic / coding interview covers

> Use the **code** (e.g., `START TOPIC T03`) or the name. Priority: **P1** must be interview-ready · **P2** important for many roles · **P3** role-specific. Each entry lists scope, the points a strong answer must hit, typical opening questions, where the drill goes, common misconceptions the interviewer probes, and your study + revision files.

---

## P1 — must be interview-ready

### T01 · Statistics & hypothesis testing — `01_foundations/01_statistics_from_scratch.md` · `10_revision/T01_statistics.md`
- **Scope:** distributions, SE/CIs, p-values, Type I/II, power, tests used in validation (binomial, Jeffreys, HL, KS, t, χ², DeLong), correlation, OLS assumptions, MLE, stationarity.
- **Must hit:** correct p-value meaning; which test for which question; one-sided PD back-tests; large-sample over-power; independence assumption of binomial test.
- **Openers:** "What does a p-value of 0.03 mean?" · "Which test would you use to back-test PD by grade, and why?" · "What's heteroskedasticity and why do validators care?"
- **Drill to:** CI arithmetic, ADF vs KPSS nulls, correlated defaults, multiple testing across grades.
- **Misconceptions probed:** p-value = probability H0 true · "insignificant = no effect" · DW valid with lagged dependent variable.

### T02 · Logistic regression & scorecards — `01_foundations/02_logistic_regression_and_scorecards.md` · `10_revision/T02_scorecards.md`
- **Scope:** why LR, odds/log-odds, MLE, assumptions, WoE/IV, binning, variable selection, reject inference, scaling/PDO, oversampling correction, segmentation.
- **Must hit:** 13-step build; WoE/IV formulas & thresholds; WoE coefficient sign logic (−1 univariate); performance window via vintages, bad definition via roll rates; PDO arithmetic.
- **Openers:** "Walk me through building an application scorecard." · "Why WoE?" · "Your WoE coefficient is positive — why?"
- **Drill to:** IV > 0.5 leakage, separation, indeterminates, swap sets, prior correction.
- **Misconceptions probed:** LR needs normal errors · IV higher is always better · stepwise = good selection.

### T03 · Monitoring metrics — `03_monitoring_validation/01_performance_monitoring_metrics.md` · `10_revision/T03_monitoring_metrics.md`
- **Scope:** KS, Gini/AUC/AR, CAP/ROC, rank-ordering, calibration tests (A/E, binomial, Jeffreys, HL, Brier), PSI/CSI, characteristic analysis, RAG thresholds, diagnosis matrix, root-cause playbook, model-type monitoring.
- **Must hit:** formulas + intuition; discrimination vs calibration vs stability; significance of changes (bootstrap/DeLong); truncation effect; action ladder with governance.
- **Openers:** "PSI is 0.27 — what do you do?" · "Gini fell from 0.59 to 0.50 — is that real?" · "How do you monitor a model with an 18-month performance window?"
- **Drill to:** empty bins, bin counts, TTC calibration expectations, slope flattening, early-read metrics.
- **Misconceptions probed:** PSI is a performance metric · calibration fine overall = fine everywhere · KS/Gini comparable across portfolios.

### T04 · Validation process, findings & effective challenge — `03_monitoring_validation/02_independent_validation_playbook.md` · `10_revision/T04_validation_process.md`
- **Scope:** validation types, tiering, end-to-end process, workstreams A–J, replication, benchmarking/challenger, sensitivity, implementation testing, findings anatomy & severity, outcomes, pushback, vendor models (SBSS).
- **Must hit:** SCOPE-D structure; CCCER findings; approve/conditions/reject; independence without hostility; vendor-model local validation.
- **Openers:** "Validate this PD model — what do you do in week 1?" · "Write me a finding for a calibration failure." · "The owner disputes your High finding the day before go-live."
- **Drill to:** severity calibration, compensating controls, escalation path, evidence of effective challenge.
- **Misconceptions probed:** validation = rerunning metrics · challenger replaces champion · downgrading under pressure.

### T05 · IFRS 9 / ECL & CECL — `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` · `10_revision/T05_ifrs9_ecl.md`
- **Scope:** stages, SICR, 30/90 DPD presumptions, ECL formula, lifetime PD, TTC→PIT (Vasicek), scenarios/weights, overlays, LGD/EAD for IFRS 9, CECL differences, RBI ECL 2027.
- **Must hit:** relative-to-origination SICR; convexity → multiple scenarios; component tests (hit rate, backstop share); overlay challenge; RBI ECL facts.
- **Openers:** "Explain staging and SICR." · "How do you validate SICR thresholds?" · "Why probability-weighted scenarios?"
- **Drill to:** behavioural life for cards, Z-factor maths, ECL movement attribution, COVID treatment.
- **Misconceptions probed:** SICR = absolute PD level · IFRS 9 PD = Basel PD · one scenario is enough.

### T06 · Basel IRB — `02_credit_risk/03_basel_irb.md` · `10_revision/T06_basel_irb.md`
- **Scope:** approaches, ASRF formula intuition, correlations, floors, LRADR/CT, MoC A/B/C, downturn LGD, DoD, PIT/TTC/hybrid, LDPs, use test, ECB validation tests.
- **Must hit:** why EL is subtracted; why correlation falls with PD; calibration sequence; Jeffreys per grade; TTC calibration expectations.
- **Openers:** "Explain the IRB capital formula intuitively." · "How is an IRB PD calibrated?" · "Your PD fails Jeffreys in 3 grades in a downturn — finding?"
- **Drill to:** MoC examples, DoD change impact, Pluto–Tasche, output floor.
- **Misconceptions probed:** IRB PD should match each year's DR · capital covers EL.

### T07 · Stress testing & econometrics — `02_credit_risk/04_stress_testing_ccar.md` · `10_revision/T07_stress_testing.md`
- **Scope:** CCAR/DFAST/SCB (+ 2026 Fed changes), ICAAP, top-down vs bottom-up, MEV selection, stationarity/cointegration, HAC SEs, BG vs DW, dynamic back-tests, sensitivity, COVID treatment, common findings.
- **Must hit:** spurious regression; sign expectations upfront; dynamic vs one-step back-test; long-run effect β/(1−ρ); overlay governance.
- **Openers:** "How do you choose macro variables?" · "Your target is non-stationary — what now?" · "How do you back-test a stress model?"
- **Drill to:** non-monotonic scenario losses, under-prediction post-2022, COVID dummy vs exclusion.
- **Misconceptions probed:** high R² = good model · DW is fine with a lagged dependent variable.

### T08 · MRM governance & regulation — `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md`, `02_global_regulations_quick_reference.md` · `10_revision/T08_mrm_governance.md`
- **Scope:** SR 11-7 concepts, SR 26-2 changes, 3LoD, inventory, tiering, model change, overlays/PMAs, KRIs, PRA SS1/23, ECB guide 2025, OSFI E-23, RBI MRM draft, vendor models.
- **Must hit:** SR 26-2 key changes (scope, definition, materiality, cadence, GenAI out); SS1/23 five principles; what's a model; IA's role.
- **Openers:** "What changed with SR 26-2?" · "Is a spreadsheet a model?" · "How would you redesign validation cadence?"
- **Drill to:** global-bank implications, aggregate model risk, temporary approvals.
- **Misconceptions probed:** SR 11-7 still current · SR 26-2 means less rigour everywhere.

### T09 · AI governance & AI regulation — `04_governance_regulation/04_ai_governance.md` · `10_revision/T09_ai_governance.md`
- **Scope:** AI governance vs MRM, operating model & RACI, AI policy stack, AI inventory & risk tiering, lifecycle controls, impact assessments, EU AI Act (classes, roles, high-risk obligations, FRIA, AI literacy, penalties, timeline), NIST AI RMF + GenAI profile, ISO/IEC 42001/23894/42005, RBI FREE-AI, MAS AIRM, OSFI E-23, SR 26-2 GenAI gap, fairness, privacy (DPDP), security (OWASP LLM Top 10), third-party AI, KRIs.
- **Must hit:** governance ≠ validation; tiering dimensions; EU AI Act credit scoring = high-risk (Dec 2027) with FRIA for deployers; NIST four functions; FREE-AI 7 Sutras/26 recs; who owns what.
- **Openers:** "How would you set up AI governance at a bank?" · "How do you tier AI use cases?" · "What does the EU AI Act require of a bank using a vendor credit-scoring model?"
- **Drill to:** GenAI use-case approval, shadow AI, agentic AI permissions, AI incidents, conflicts between frameworks.
- **Misconceptions probed:** AI governance = model validation · EU AI Act applies only to providers · GenAI is covered by SR 26-2.

### T10 · ML model validation — `01_foundations/03_ml_for_credit_risk.md` · `10_revision/T10_ml_validation.md`
- **Scope:** trees/GBM, hyperparameters, overfitting, leakage, calibration, SHAP/PDP/ALE, reason codes, fairness metrics, monotonic constraints, ML validation checklist, fraud models.
- **Must hit:** justify complexity with significant OOT uplift; SHAP properties & limits; calibration after resampling; fairness trade-offs; retraining governance.
- **Openers:** "XGBoost or LR for our new card PD?" · "How do you validate explainability?" · "How do you test fairness?"
- **Drill to:** SHAP with correlated features, adverse-action reasons, seed stability, training–serving skew.
- **Misconceptions probed:** SHAP = causality · SMOTE harmless for PD · higher AUC always wins.

### T11 · Credit risk fundamentals — `02_credit_risk/01_credit_risk_fundamentals.md` · `10_revision/T11_credit_fundamentals.md`
- **Scope:** lifecycle & models, products, DPD/default/charge-off, EL/UL, PD/LGD/EAD/CCF, vintages, roll rates, migration matrices, bureaus & SBSS, capital basics, card economics.
- **Must hit:** EAD for revolving; cure-adjusted LGD; cumulative vs marginal PD; 180/120 DPD charge-off.
- **Openers:** "Define PD, LGD, EAD." · "How does a card issuer make money?" · "What does a vintage curve tell you?"

### T12 · Your projects deep-dive — `00_strategy/04_positioning_resume_and_stories.md` · `10_revision/T12_my_projects.md`
- **Scope:** SBSS BCC/non-BCC vendor scorecards, IFRS 9, IRB and stress-testing monitoring; your role vs client's; breaches & root causes; SBA's 2026 SBSS change. (SmarterPay only after its KT.)
- **Must hit:** your numbers; bad definitions & windows; thresholds; one breach story end-to-end; limitations; what you'd change.
- **Openers:** "Walk me through the SBSS model you monitor." · "Tell me about a breach you diagnosed." · "What exactly was your role?"
- **Drill to:** every claim, 4–5 levels deep — this is where real panels go hardest.

### T13 · Behavioural & situational — `06_interview_bank/04_behavioral_hr_negotiation.md` · `10_revision/T13_behavioural.md`
- **Scope:** STAR-L stories (challenge, error found, pressure, mistake, conflict, communication, mentoring), why validation/leave/us, pushback/ethics scenarios, HR/CTC/notice.
- **Must hit:** specific actions with numbers; independence with collaboration; honest notice-period handling.

---

## P2 — important for many roles

### T14 · GenAI / LLM & agentic AI risk — `04_governance_regulation/03_ai_ml_genai_model_risk.md`, `04_ai_governance.md` · `10_revision/T14_genai_risk.md`
Risk taxonomy (NIST AI 600-1), 5-pillar validation approach, evaluation metrics (faithfulness, hallucination rate), red-teaming, OWASP LLM Top 10, agentic controls, vendor/foundation-model risk.

### T15 · Wholesale / commercial credit models — `02_credit_risk/05_wholesale_commercial_credit_models.md` · `10_revision/T15_wholesale_credit.md`
Obligor/facility ratings, master scale, financial-ratio scorecards, expert judgment & overrides, LDP methods, CRE models (DSCR/LTV), commercial CCAR/CECL models, validation specifics.

### T16 · Data quality, implementation testing & documentation review — `03_monitoring_validation/02_independent_validation_playbook.md` §5B/§5H · `10_revision/T16_data_implementation.md`
Lineage & reconciliation, BCBS 239 basics, production-vs-development parity, edge-case testing, EUC controls, reading an MDD critically.

---

## P3 — role-specific
### T17 · Fraud & AML model validation — `01_foundations/03_ml_for_credit_risk.md` §8b · `10_revision/T17_fraud_aml.md`
### T18 · Probability & quant screen — `06_interview_bank/07_probability_quant_screen.md` · `10_revision/T18_quant_puzzles.md`

---

## Coding catalog (`START CODING …`)
| Code | Area | Typical problems | Auto-graded |
|---|---|---|---|
| C1 | Python/pandas | bad rate by segment, merges without duplication, monthly flags | ✅ |
| C2 | Metrics from scratch | KS, AUC/Gini, PSI, WoE/IV, HL, binomial/Jeffreys by grade | ✅ |
| C3 | Modeling | logistic regression & interpretation, calibration table, GBM challenger | ✅ (partly) |
| C4 | SQL | performance-window bad flags, roll rates, vintages, deciles/KS, PSI, dedup | ✅ |
| C5 | SAS | data step logic, PROC choice, macro for PSI, read-and-debug | Reviewed by interviewer |
| C6 | Code review | find the bugs in a PSI/KS/WoE implementation | Reviewed |
| C7 | Time series | ADF/KPSS, HAC OLS, BG test, dynamic back-test | Reviewed |
