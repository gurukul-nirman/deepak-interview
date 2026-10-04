# 06.1 · Tier-1 Question Bank — must answer cold (≈130 questions)

> **How to use:** cover the answer, say yours aloud (≤ 45 seconds), then compare. Log misses in your error log. These are the highest-frequency questions for credit-risk monitoring/validation/MRM roles at 5–8 years (compiled from 2026 JDs, candidate reports and standard practice — frequency is my estimate **[Assumption]**). Deeper material sits in the linked files.

**Sections:** A Credit fundamentals & statistics · B Logistic regression & scorecards · C Monitoring metrics · D IFRS 9 / CECL / RBI ECL · E Basel IRB · F Stress testing · G Validation process & findings · H Governance & regulation · I ML/AI · J Your projects (templates)

---

## A. Credit fundamentals & statistics

**A1. What are PD, LGD, EAD and EL?**
PD = probability of default over a horizon; LGD = % of exposure lost given default (1 − recovery); EAD = exposure at the time of default; EL = PD × LGD × EAD — the expected loss covered by pricing/provisions; capital covers unexpected loss.

**A2. How do you compute EAD for a credit card?**
EAD = drawn balance + CCF × undrawn limit, where CCF is estimated from how much of the undrawn line is drawn down before default (reference date ~12 months before default).

**A3. What's the difference between default and charge-off?**
Default is a risk/regulatory event (e.g., 90 DPD or unlikely to pay); charge-off is an accounting write-off — in the US cards at 180 DPD, closed-end loans at 120 DPD.

**A4. What is a vintage analysis and why do you need it?**
Cumulative bad rate by months-on-book per origination cohort. It shows when performance matures (to set the performance window) and compares cohort quality at equal age.

**A5. What is a roll-rate analysis?**
Month-on-month transition rates between delinquency buckets. Used to define "bad" (the bucket from which most accounts roll forward rather than cure) and to forecast collections and losses.

**A6. Marginal vs cumulative PD?**
Cumulative PD(t) = probability of default by time t; marginal PD(t) = probability of defaulting in period t = cumPD(t) − cumPD(t−1). Cumulative = 1 − Π(1 − hazard).

**A7. PIT vs TTC PD?**
PIT moves with the economic cycle (current conditions); TTC averages over a cycle and is stable. IFRS 9 wants PIT; IRB tends to TTC/hybrid.

**A8. What does a p-value mean?**
The probability of observing results at least this extreme if the null hypothesis is true — not the probability the null is true.

**A9. Type I vs Type II error in model monitoring?**
Type I: flagging a good model as broken (false alarm); Type II: missing a deteriorated model. Thresholds trade them off; low bad counts raise Type II risk.

**A10. What's the 95% CI for a 5% bad rate on 2,000 accounts?**
SE = √(0.05×0.95/2000) ≈ 0.49% → CI ≈ 4.0%–6.0%.

**A11. Pearson vs Spearman correlation?**
Pearson measures linear association; Spearman is rank-based and captures monotonic non-linear relationships, more robust to outliers.

**A12. What is multicollinearity and why does it matter?**
High correlation among predictors; predictions may be fine but coefficients become unstable, signs can flip and SEs inflate — unacceptable in an interpretable credit model. Detect with VIF (> 5–10), correlations; fix by dropping/combining variables.

**A13. What is heteroskedasticity / autocorrelation and how do you handle them?**
Non-constant error variance / correlated errors over time; both make OLS standard errors wrong. Detect with Breusch–Pagan / Breusch–Godfrey; fix with robust/HAC SEs, transformations, AR terms.

**A14. What is stationarity and why does it matter?**
Constant mean/variance/autocorrelation over time. Regressing non-stationary series on each other gives spurious relationships. Test with ADF (H0: unit root) and KPSS (H0: stationary); difference or use cointegration.

**A15. Explain Bayes' theorem with a credit/fraud example.**
P(fraud | alert) = P(alert | fraud)·P(fraud)/P(alert). With 1% prevalence, 90% detection and 5% false alerts → only ~15% of alerts are fraud.

---

## B. Logistic regression & scorecards

**B1. Walk me through building an application scorecard.**
Objective → sample design (observation point, performance window from vintage analysis, bad definition from roll rates, indeterminates/exclusions) → dev/holdout/OOT samples → data prep → fine & coarse classing → WoE/IV screening → correlation/VIF and stepwise with business review → reject inference → logistic regression → scaling (PDO) → validation (KS/Gini, calibration, stability) → cut-off strategy (swap sets) → documentation, independent validation, implementation, monitoring. *(Full script: `01_foundations/02_logistic_regression_and_scorecards.md` §7.)*

**B2. Why logistic regression for PD and not linear regression?**
Binary target needs a bounded probability; linear regression can predict < 0 or > 1, has heteroskedastic non-normal errors. LR models log-odds linearly, is interpretable, stable, and regulator-friendly.

**B3. Assumptions of logistic regression?**
Binary outcome, independent observations, linearity of the logit in predictors, no severe multicollinearity, enough events per variable. Not required: normal errors or homoskedasticity.

**B4. How do you interpret a coefficient?**
A one-unit increase in x changes the log-odds by β; odds multiply by e^β. E.g., β = 0.18 → odds × 1.20.

**B5. What is WoE?**
WoE = ln(%Good/%Bad) per bin (Siddiqi convention). Positive = safer than average. It linearises the variable's relationship with log-odds and handles missing/outliers as bins.

**B6. What is IV and its thresholds?**
IV = Σ(%Good − %Bad)·WoE. < 0.02 useless, 0.02–0.1 weak, 0.1–0.3 medium, 0.3–0.5 strong, > 0.5 suspicious (check leakage; strong bureau scores can legitimately exceed it).

**B7. Why is a WoE coefficient around −1?**
In a single-variable WoE logistic regression predicting bad, the coefficient is exactly −1 (intercept = overall log-odds). In multivariate models it deviates due to correlations; a positive sign signals multicollinearity. (Sign flips if WoE is defined as ln(%Bad/%Good).)

**B8. How do you choose the number of bins?**
Fine-class into 10–20, then coarse-class to 4–8 with monotonic WoE (where logical), ≥ ~5% population and enough bads per bin, business sense, and stability across samples.

**B9. How do you treat missing values in a scorecard?**
As their own bin with its own WoE (missingness is often predictive); never silently impute to the mean or score as zero points.

**B10. What's reject inference and its methods?**
Correcting for the fact that only approved applicants have outcomes. Methods: hard cut-off augmentation, parcelling, fuzzy augmentation, re-weighting, external bureau performance of rejects, below-cut-off test approvals. Validate sensitivity — it's an assumption.

**B11. How do you scale a scorecard?**
Score = Offset + Factor·ln(odds); Factor = PDO/ln2; Offset = Base − Factor·ln(BaseOdds). For 600 at 50:1, PDO 20: Factor 28.85, Offset 487.1; points per attribute = −(β·WoE + β0/n)·Factor + Offset/n.

**B12. What is PDO?**
Points to double the odds — e.g., every 20 points doubles good:bad odds.

**B13. How do you select variables?**
IV screening, stability (CSI dev vs OOT), correlation/VIF, variable clustering, stepwise/backward as an aid, then business review for intuition, explainability, data availability and regulatory acceptability. Aim for 8–15.

**B14. What is an indeterminate and why exclude it?**
Neither clearly good nor bad (e.g., worst status 30–59 DPD). Excluding sharpens separation; score them afterwards to confirm they fall between goods and bads.

**B15. What's the difference between application and behavioural scorecards?**
Application: applicants, bureau/application data, longer performance window, approve/limit/price. Behavioural: existing accounts, payment/utilisation history, monthly scoring, line management and collections; better PIT PD drivers.

**B16. How do you correct for oversampled bads?**
Adjust the intercept: β0 + ln(π1/π0) − ln(ρ1/ρ0) (population vs sample bad odds), or use sampling weights.

**B17. What is swap-set analysis?**
Comparing who the new and old scorecards approve at the same approval rate: swap-ins (new approves, old declined) vs swap-outs — their bad rates show whether the new card adds value.

**B18. How do you decide segmentation?**
Business logic + tree/CHAID evidence; accept segments only if the segmented model gives material, stable uplift with enough bads per segment.

---

## C. Monitoring metrics (your home turf — expect follow-ups)

**C1. Define KS.**
Maximum difference between cumulative distributions of bads and goods across the score; the best single cut-off's separation (0–100).

**C2. Define Gini and AUC and their relationship.**
AUC = probability a random bad is scored riskier than a random good; Gini (= Accuracy Ratio = Somers' D) = 2·AUC − 1.

**C3. Typical KS/Gini values?**
Bank-specific, but application scorecards commonly KS 30–50 / Gini 0.4–0.6; behavioural higher. Compare to development, not to an absolute number. **[Assumption]**

**C4. What is PSI and its thresholds?**
PSI = Σ(A − E)·ln(A/E) across bins defined on the reference sample; < 0.1 stable, 0.1–0.25 monitor, > 0.25 significant shift.

**C5. PSI is 0.27 — what do you do?**
Confirm data integrity; find which characteristics moved (CSI, characteristic analysis); ask the business what changed (channel, marketing, policy); check whether discrimination and calibration still hold. If only the population moved and performance holds → document/possibly re-baseline; if calibration is off → recalibrate/overlay; if discrimination drops → redevelopment assessment.

**C6. What's CSI?**
PSI applied to each characteristic's bins — tells you which inputs drove the score shift.

**C7. What's characteristic analysis?**
Σ(A% − E%) × points per attribute — how many points the average score moved because of each characteristic.

**C8. Discrimination vs calibration?**
Discrimination = ranking (who is riskier); calibration = levels (are PDs right). A model can rank perfectly and be badly calibrated.

**C9. How do you test calibration?**
Predicted vs observed by grade/decile; binomial (or Jeffreys) per grade; Hosmer–Lemeshow overall; A/E ratio; Brier score; traffic-light reporting.

**C10. Why might Gini fall after the bank tightens its cut-off?**
Truncation: the booked population is more homogeneous, so separation looks weaker even if the model hasn't changed.

**C11. Gini dropped 5 points — is that significant?**
Check bad counts and a bootstrap CI (or DeLong for paired comparisons); with few bads a 5-point move can be noise.

**C12. What's the Hosmer–Lemeshow test?**
Groups by predicted PD deciles and compares observed vs expected defaults: Σ(O−E)²/(n·p̄(1−p̄)) ~ χ²(g−2). Rejects easily in large samples — read with the calibration table.

**C13. Binomial test — and its weakness?**
P(X ≥ D | N, PD) per grade; assumes independent defaults, so it's too strict when defaults are correlated (Vasicek-adjusted versions widen bounds).

**C14. What's the Jeffreys test?**
Bayesian calibration test: p = BetaCDF(PD; D+0.5, N−D+0.5). Small p → PD likely under-estimated. Used by the ECB for IRB validation reporting.

**C15. What monitoring would you set for a new model?**
Stability (PSI, CSI, missing rates), discrimination (KS/Gini, rank-ordering, early-read metrics before maturity), calibration (A/E, grade tests), usage (overrides, overlays, approval rates), with RAG thresholds, frequency by tier, owners and escalation.

**C16. How do you monitor a model whose performance window is 18 months?**
Early-read metrics (e.g., 3/6/9-month delinquency vs expected), stability measures, and back-testing on matured cohorts; vintage comparisons.

**C17. Calibration is fine overall but fails in low-risk grades — what's happening?**
Slope flattening: low grades under-predicted, high grades over-predicted → discrimination weakening (e.g., a key input lost power). Investigate drivers; recalibrate and assess redevelopment.

**C18. How do you set monitoring thresholds?**
By policy, before seeing results; based on statistical significance and materiality (business impact), aligned with model tier; reviewed periodically.

---

## D. IFRS 9 / CECL / RBI ECL

**D1. Explain IFRS 9's three stages.**
Stage 1: performing, 12-month ECL; Stage 2: significant increase in credit risk since origination, lifetime ECL; Stage 3: credit-impaired, lifetime ECL with interest on net carrying amount.

**D2. What is SICR and how is it determined?**
Significant increase in credit risk since initial recognition — relative change in lifetime PD vs origination (quantitative thresholds), qualitative indicators (watchlist, forbearance), and the 30 DPD rebuttable backstop.

**D3. ECL formula?**
Σ_t marginal PD(t) × LGD(t) × EAD(t) × discount factor at EIR, computed per scenario and probability-weighted.

**D4. Why multiple macro scenarios?**
Credit losses are convex in the economy, so the average of scenario ECLs exceeds ECL at the average scenario — IFRS 9 requires an unbiased, probability-weighted estimate.

**D5. How do you convert TTC PD to PIT PD?**
Vasicek one-factor: PD_PIT = N((N⁻¹(PD_TTC) − √ρ·Z)/√(1−ρ)), with Z the systematic factor estimated from history and projected from macro scenarios; or regress default rates on macro variables.

**D6. How is lifetime PD built?**
Transition matrices (Markov), survival/hazard models, or vintage-curve extrapolation — with macro adjustments over the forecast horizon and reversion beyond it.

**D7. How do you validate SICR thresholds?**
Hit rate (share of new defaults previously in Stage 2), time in Stage 2 before default, false positives/cures, share of transfers via the 30 DPD backstop (high = criteria not working), stability, alternative-threshold comparison.

**D8. What are overlays/PMAs and how do you challenge them?**
Adjustments outside the model for limitations/emerging risks. Challenge: what limitation, how quantified, approval, sunset, monitoring, double counting.

**D9. IFRS 9 PD vs Basel PD?**
IFRS 9: PIT, forward-looking, lifetime where needed, unbiased (no MoC/downturn). Basel: 1-year, TTC/hybrid, long-run average plus MoC and floors.

**D10. IFRS 9 vs CECL?**
CECL: lifetime ECL from day one (no staging), reasonable-and-supportable forecast then reversion, Q-factors; unfunded commitments only if not unconditionally cancellable.

**D11. What drives ECL movements quarter to quarter?**
Volume and mix, stage transfers, parameter/model changes, macro/scenario updates, overlays, write-offs/recoveries, FX.

**D12. Behavioural life for credit cards — why?**
IFRS 9 requires measuring ECL over the period of exposure for revolving facilities even beyond the contractual (cancellable) term.

**D13. What's new in India's ECL?**
RBI final directions 27 Apr 2026, effective 1 Apr 2027, for commercial banks (excl. SFBs, payments banks, LABs): three-stage ECL, Stage 2 at 30–90 DPD with a 5% minimum provision, product-wise floors, EIR, board oversight, MRM for ECL models, impact spread over ~4 years.

**D14. How did COVID affect ECL models?**
Government support suppressed defaults despite macro shocks → macro-default links broke → large overlays; re-estimation needs explicit treatment of 2020–21 data.

---

## E. Basel IRB

**E1. Standardised vs F-IRB vs A-IRB?**
Standardised: prescribed risk weights. F-IRB: bank PD, supervisory LGD/EAD. A-IRB: bank PD, LGD, EAD (M). Retail IRB: bank estimates all three.

**E2. Explain the IRB capital formula intuitively.**
Vasicek one-factor model: capital covers losses at the 99.9th percentile of a one-year systematic shock, minus EL: K = LGD·[N((N⁻¹(PD)+√R·N⁻¹(0.999))/√(1−R)) − PD]·MA; RWA = 12.5·K·EAD.

**E3. Why does asset correlation fall as PD rises?**
High-PD obligors default for idiosyncratic reasons; low-PD ones mostly in systemic downturns.

**E4. Correlations for retail classes?**
Residential mortgages 0.15, QRRE 0.04, other retail 0.03–0.16 depending on PD.

**E5. What's LRADR / central tendency?**
Long-run average of annual default rates over a representative cycle including downturn years; PDs are calibrated so the portfolio average matches it (≥ 5 years of data minimum).

**E6. What is MoC? Categories?**
Margin of conservatism for estimation uncertainty — EBA: A (data/methodological deficiencies), B (relevant changes in processes/environment), C (general estimation error).

**E7. What is downturn LGD?**
LGD reflecting economic downturn conditions — estimated from identified downturn periods or via a calibrated add-on (EBA GL/2019/03).

**E8. PD and LGD floors (Basel III final)?**
PD 0.05% (0.10% QRRE revolvers); A-IRB LGD floors e.g. 25% corporate unsecured, 5% mortgages, 50% QRRE, 30% other unsecured retail. (Check local rules.)

**E9. What is the EU definition of default materiality threshold for retail?**
€100 absolute and 1% relative, 90 consecutive days; plus unlikeliness-to-pay; ≥ 3-month probation.

**E10. How do you validate an IRB PD model?**
Discrimination (AUC vs initial validation), calibration (Jeffreys/binomial per grade vs LRADR expectations), stability (migration matrices, HHI concentration), overrides, representativeness, DoD consistency, MoC adequacy, use test.

**E11. What is the use test?**
IRB parameters must be used meaningfully in internal risk management — credit decisions, limits, pricing, provisioning inputs, capital allocation.

**E12. What's the output floor?**
Aggregate IRB RWA can't fall below 72.5% of standardised RWA (phased in).

**E13. How do you handle low-default portfolios?**
Pluto–Tasche upper bounds, benchmarking to external ratings, Bayesian/expert approaches with conservatism.

---

## F. Stress testing

**F1. What is CCAR/DFAST?**
Fed supervisory stress tests and capital-plan review for large US BHCs: baseline and severely adverse scenarios over 9 quarters; results set the stress capital buffer.

**F2. What is the SCB?**
Max(2.5%, peak-to-trough CET1 decline under severely adverse + 4 quarters of planned dividends/RWA). From 2028 it will average the two most recent tests (Fed final rule, 30 Sep 2026).

**F3. Top-down vs bottom-up loss models?**
Top-down: portfolio loss rate regressed on macro variables — simple, robust. Bottom-up: loan-level PD/LGD/EAD conditioned on macro — granular, consistent with BAU, data-hungry.

**F4. How do you choose macro variables?**
Economic rationale and expected sign first, correlation/lag analysis, stationarity checks, parsimony, out-of-sample performance, stability.

**F5. What diagnostics do you run on a stress-test regression?**
Stationarity (ADF/KPSS), cointegration if levels, signs/significance with HAC SEs, autocorrelation (Breusch–Godfrey; DW is biased with a lagged dependent variable), heteroskedasticity, normality, VIF, structural breaks, OOT dynamic back-test, sensitivity, rolling-coefficient stability.

**F6. How do you back-test a stress-test model?**
Dynamic out-of-time projections, back-tests using realised macro paths, historical episodes (GFC), benchmarks; report MAPE and cumulative error, flag under-prediction.

**F7. How do you treat COVID data?**
Identify the break; test dummy vs exclusion vs robust estimation; show sensitivity both ways; document; overlays if needed.

**F8. Long-run effect of a shock in a model with a lagged dependent variable?**
β/(1 − ρ) — persistence amplifies shocks.

**F9. What are common stress-model findings?**
Spurious regression, counter-intuitive signs, overfitting, ignored autocorrelation, insufficient downturn data, untreated COVID, non-monotonic responses, ungoverned overlays.

**F10. What changed in the Fed's stress test in 2026?**
Annual public comment on scenarios and material model changes; adoption of models for 2027; two global market shocks; SCB averaging from 2028; proposal to revise the non-interest-income model.

---

## G. Validation process & findings

**G1. What are the core components of model validation?**
Conceptual soundness, ongoing monitoring (incl. process verification/benchmarking), outcomes analysis (incl. back-testing) — plus data, implementation and use reviews.

**G2. Walk me through how you'd validate a PD model.**
Scope & tier → document request → data (lineage, quality, sample design, default definition) → conceptual soundness (method, variables, signs, segmentation) → replication → performance (in-sample/OOS/OOT discrimination, calibration, stability) → benchmark/challenger → sensitivity → implementation testing → monitoring-plan review → findings with severity → outcome.

**G3. What is conceptual soundness?**
Whether the design, theory, assumptions, data choices and methodology are appropriate for the purpose — evaluated against alternatives and evidence.

**G4. What's replication and why do it?**
Independently re-performing development steps (re-running or re-coding) to confirm results are reproducible and the documentation is complete.

**G5. Benchmarking vs challenger model?**
Benchmark: any comparison point (vendor score, industry, alternative data). Challenger: an alternative model built to test whether the chosen approach is reasonable — it informs, not replaces.

**G6. What is sensitivity analysis?**
Varying inputs/assumptions to see how outputs respond; tests robustness and reveals hidden dependencies.

**G7. What is implementation testing / process verification?**
Checking production code, data feeds and outputs match the approved model (parallel runs, reconciliations, edge cases).

**G8. How do you write a finding?**
Title, severity, condition (evidence/numbers), criteria (policy/regulation), cause, effect (quantified), recommendation, owner, due date, compensating controls.

**G9. Severity levels?**
High (material impact/non-compliance; restrict use until fixed), Medium (could materially affect outputs under some conditions), Low (best-practice/documentation). Bank-specific.

**G10. Possible validation outcomes?**
Approved; approved with conditions/restrictions; not approved.

**G11. The model owner disagrees with your finding. What do you do?**
Re-check evidence together; correct if wrong; if it stands, keep the severity but be flexible on remediation path (overlay, restricted use, timeline); escalate through committee with both views documented if unresolved.

**G12. What is effective challenge?**
Critical, objective analysis by people with the expertise, independence and standing to make change happen (SR 26-2) — SR 11-7: incentives, competence, influence.

**G13. How do you validate a vendor model?**
Understand conceptual soundness from vendor documentation; local outcomes analysis and stability on your population; segment checks; limitations; version-change process; document customisations.

**G14. Validation vs monitoring?**
Monitoring is the ongoing first-line tracking against thresholds; validation is the independent second-line assessment of the whole model (design, data, implementation, performance, use).

**G15. How do you decide validation scope?**
By tier (materiality × inherent risk), change since last validation, monitoring results, open findings, regulatory use.

---

## H. Governance & regulation

**H1. What is model risk?**
Potential adverse consequences from decisions based on incorrect or misused model outputs.

**H2. What is SR 11-7?**
2011 US supervisory guidance on model risk management (development/use, validation, governance) — **replaced by SR 26-2 on 17 Apr 2026**.

**H3. What changed with SR 26-2?**
Most relevant > $30bn assets; non-compliance isn't supervisory criticism per se; narrower "complex" model definition with carve-outs; materiality-based (exposure + purpose) intensity; risk-based validation cadence; GenAI/agentic AI out of scope; stand-alone vendor section; BSA/AML statement rescinded.

**H4. What are the three lines of defence in MRM?**
1st owners/developers/users; 2nd MRM/validation; 3rd internal audit.

**H5. What's in a model inventory?**
ID, purpose/uses, owner/developer/user/validator, tier, methodology, inputs, vendor/version, platform, dependencies, validation dates/outcomes, findings/restrictions, monitoring status, overlays.

**H6. How do you tier models?**
Inherent risk (complexity, assumptions, data) × materiality (exposure, purpose/regulatory use) → Tier 1–3 → validation depth/cadence.

**H7. What is PRA SS1/23?**
UK MRM supervisory statement (effective 17 May 2024) with five principles: model identification & classification, governance (SMF accountability), development/implementation/use, independent validation, model risk mitigants (incl. PMAs).

**H8. What is OSFI E-23?**
Canada's MRM guideline (final Sep 2025, effective 1 May 2027), enterprise-wide, explicitly covering AI/ML.

**H9. What's RBI doing on MRM?**
Draft Guidance on Regulatory Principles for MRM (24 Jun 2026) covering all regulated entities and all models incl. AI/ML and third-party; board-approved framework, inventory, independent validation, explainability/human oversight.

**H10. What is a model change and when does it need re-validation?**
Changes to methodology, variables, segmentation, data sources, use or material output impact → re-validation; minor within-methodology recalibrations → lighter review per policy.

**H11. What are MRM KRIs?**
Overdue validations, open/overdue High findings, models used with restrictions/exceptions, unresolved monitoring breaches, inventory completeness, overlay size.

**H12. What is aggregate model risk?**
Risk from shared data/assumptions/methods across models (e.g., one macro scenario set feeding ECL, CCAR, ICAAP).

**H13. Is a spreadsheet a model?**
Under SR 26-2, simple arithmetic spreadsheets and deterministic rules are excluded; a spreadsheet implementing a statistical model is in scope. Under PRA SS1/23 simple tools still need proportionate controls.

---

## I. ML / AI

**I1. When would you use ML instead of logistic regression?**
When there's material, stable, significant uplift (non-linearity/interactions, rich data) and the use can tolerate added complexity — with constraints, calibration, explainability, fairness and monitoring.

**I2. How does gradient boosting work?**
Sequentially adds shallow trees that fit the errors (gradients) of the current ensemble, scaled by a learning rate.

**I3. How do you prevent overfitting in XGBoost?**
Shallow depth, learning rate + early stopping, min child weight, subsampling, L1/L2 regularisation, OOT validation, no tuning on test.

**I4. What are SHAP values?**
Additive feature contributions from Shapley values: base value + Σ SHAP = model output for that record; used for global importance and local reason codes; not causal.

**I5. How do you generate adverse-action reasons from an ML model?**
Top adverse SHAP contributions mapped to stable plain-language reason codes, validated for consistency (ECOA/Reg B in the US).

**I6. How do you test fairness?**
Approval/outcome disparity metrics (e.g., adverse impact ratio), score distribution differences, error-rate parity on lawful protected-class proxies; investigate proxies; document trade-offs.

**I7. What is data leakage?**
Using information not available at decision time (post-observation variables, target-derived fields), inflating performance.

**I8. Is GenAI within SR 26-2?**
No — explicitly out of scope; governed under broader risk management; RFI pending. OSFI E-23 and the RBI draft include AI more broadly.

**I9. How would you validate an LLM use case?**
Scope/tier → data/knowledge sources → performance on golden datasets (faithfulness, hallucination rate) → robustness & safety (prompt injection, bias, PII) → controls & monitoring (guardrails, human review, version pinning, drift).

**I10. Why do monotonic constraints matter?**
They force intuitive directions (e.g., higher bureau score → lower risk), improving explainability and regulatory acceptance with little performance cost.

---

## J. Your projects — templates (fill in from `00_strategy/04_positioning_resume_and_stories.md`)

**J1. Tell me about yourself.** → 90-second script.
**J2. Walk me through a model you monitored end to end.** → purpose, data, method, metrics, thresholds, a breach story, limitation, what you'd change.
**J3. What was the most significant issue you found?** → metric → root cause → action → approval → $ impact.
**J4. How did you decide the root cause wasn't a data issue?** → reconciliations, missing-rate checks, definition checks.
**J5. What thresholds did you use and who set them?**
**J6. What's SBSS and how do you validate a vendor score?**
**J7. How did SBA's SBSS change (1 Mar 2026) affect your models?**
**J8. Which IFRS 9 component did you work on — how was SICR defined?**
**J9. Which IRB tests did you run and what were the results?**
**J10. What diagnostics did you run on stress-test models?**
**J11. What was your exact role vs the client's?**
**J12. What would you do differently?**
