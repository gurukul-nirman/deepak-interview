# 06.2 · Tier-2 "Grilling Ladders" — how interviewers push 5–7 levels deep

> Senior interviewers don't ask 30 unrelated questions; they pick 3–4 topics and **drill until you break**. Each ladder below simulates one drill. Practise by having someone read the questions in order without letting you see the next one. Your goal: reach level 5+ on every ladder.

---

## A. Stability (PSI) ladder
1. **What's PSI?** Σ(A−E)·ln(A/E) over bins of the reference distribution; < 0.1 / 0.1–0.25 / > 0.25.
2. **Why the log term?** It's a symmetric KL divergence — each bin contributes (A−E)·ln(A/E) ≥ 0, so shifts in either direction add up.
3. **Where do the bins come from?** The reference (development/baseline) sample — deciles of the reference score; apply the same edges to the current sample.
4. **What if a current bin is empty?** ln(0) is undefined → floor at a small ε (e.g., 1e-4/1e-6) and report it; consider merging bins.
5. **Does PSI depend on the number of bins and sample size?** Yes — more bins and smaller samples inflate PSI through noise; that's why thresholds are conventions, not statistical tests. For small samples, bootstrap a null distribution of PSI or use a χ² test of distributions.
6. **PSI 0.30, KS unchanged, A/E 1.15. Story and action?** Population shift with intact ranking but a level shift in risk → recalibrate intercept or overlay, confirm the business change, re-baseline the reference if intentional, monitor monthly.
7. **What would make you ignore a high PSI?** An intended, documented strategy change (e.g., new channel) where discrimination and calibration hold on the new population — record rationale and update the reference period.

## B. Discrimination ladder
1. **KS vs Gini — which do you prefer?** Gini uses the whole ranking (area); KS is the single best cut-off. I report both; Gini is more stable, KS is intuitive for cut-off strategy.
2. **Gini = 2AUC − 1 — derive the intuition.** AUC is P(bad scored riskier than good); Gini rescales so random = 0 and perfect = 1.
3. **Your Gini fell from 0.59 to 0.50. Significant?** Check bootstrap CI / standard errors; in the demo the recent 95% CI [0.478, 0.534] excludes 0.589 → significant.
4. **What could cause it besides model deterioration?** Truncation from tighter cut-offs, mix shift towards a segment where the model is weaker, bad-definition or data changes, immature performance window.
5. **How do you find which variable lost power?** Characteristic-level IV/WoE on recent data vs development; univariate Gini of each input over time; SHAP/attribution drift; segment decomposition.
6. **Would you redevelop?** If the loss is significant, persistent (2+ periods), material (cut-off/ECL impact), and not fixable by recalibration — after a challenger shows a better specification exists.

## C. Calibration ladder
1. **How do you test calibration?** Predicted vs observed by grade; binomial/Jeffreys per grade; HL overall; A/E; Brier.
2. **Binomial test assumptions?** Independent defaults, fixed PD within grade — both questionable.
3. **What happens to the test when defaults are correlated?** True variance is higher → binomial test rejects too often (Type I inflation). Vasicek-adjusted binomial or a traffic-light approach with wider bands fixes it.
4. **TTC model failing calibration in a recession — finding?** Not automatically: TTC PDs are expected to deviate from realised one-year default rates over the cycle; compare to the long-run average and check grade migration behaves as designed.
5. **HL p-value 0.0001 on 500k accounts — reject the model?** Large-sample over-power; look at the calibration table and effect size (A/E by decile), business impact.
6. **How would you recalibrate?** Intercept shift to recent default experience (calibration-in-the-large) or logistic recalibration (slope + intercept), on a clean recent window; validate on holdout; govern as a model change per policy.

## D. Scorecard ladder
1. **Why WoE binning?** Linearises log-odds, handles missing/outliers, monotonic explainable points.
2. **What does WoE lose?** Within-bin variation; depends on binning choices; can't extrapolate; overfits small bins.
3. **Your WoE coefficient is +0.4 (Siddiqi convention). Why?** Multicollinearity/suppressor effect — the variable's marginal effect is explained by correlated variables; check VIF/correlations; remove or recombine.
4. **IV of 0.9 — keep it?** Investigate leakage (timing of capture), definition overlap with target; strong bureau scores can legitimately be high — document.
5. **How did you choose the performance window and bad definition?** Vintage maturity curve and roll-rate "point of no return" — with evidence tables.
6. **Reject inference choice affects cut-off by 15 points — what does a validator say?** It's a key assumption: require sensitivity analysis, conservative choice, and monitoring of below-cut-off performance (test approvals if feasible).

## E. IFRS 9 ladder
1. **Explain staging.** (Tier-1 D1.)
2. **Relative vs absolute SICR thresholds — why both?** Relative alone over-triggers on very low PDs (0.01% → 0.03% is 3× but immaterial); absolute floor prevents noise.
3. **How do you test whether SICR works?** Hit rate, time in Stage 2 before default, backstop share, false positives, stability.
4. **85% of Stage 2 transfers come from the 30 DPD backstop — finding?** Yes — quantitative criteria aren't detecting deterioration early; recalibrate thresholds; potentially understated ECL.
5. **Lifetime PD for a revolving card — what horizon?** Behavioural life (period of exposure), evidenced from account-closure/charge-off data.
6. **How do scenario weights get set and validated?** Economics/risk committee governance; test plausibility, consistency with planning, sensitivity of ECL to weights; document rationale.
7. **Overlay = 18% of ECL for 6 quarters — challenge?** What limitation, quantification method, why the model hasn't been fixed, sunset date, double counting, disclosure; likely a finding requiring remediation plan.

## F. IRB ladder
1. **How is a PD calibrated for IRB?** Rank model → central tendency (LRADR) → calibrate grades (odds shift) → MoC → floors.
2. **How many years for LRADR and which years?** ≥ 5 years minimum; must be representative of the cycle (include downturns); justify the window.
3. **MoC — give real examples.** A: missing data history; B: new underwriting policy; C: statistical uncertainty in LRADR.
4. **Downturn LGD — how identified?** Downturn periods via macro and realised loss data (EBA approach); estimate or add-on; consider incomplete workouts.
5. **DoD changed last year — what happens to your PD?** Re-simulate historical defaults under the new definition; recalibrate; assess impact; may need MoC category A/B; supervisory notification of material change.
6. **AUC at annual validation is 4 points below initial validation — what do regulators expect?** A test of the difference (ECB reporting), investigation of cause, and remediation if significant.

## G. Stress-testing ladder
1. **How do you pick MEVs?** Rationale + sign expectations → lag/correlation → stationarity → parsimony → OOT.
2. **Your NCO series is non-stationary. Your model regresses it on unemployment level. Problem?** Spurious regression risk; test cointegration or difference; add AR term.
3. **You included the lagged dependent variable — consequences?** DW biased; use Breusch–Godfrey; dynamic forecasts compound errors; long-run effect β/(1−ρ).
4. **Your severely adverse losses peak in Q2 and drop fast — plausible?** Probably not; losses usually lag unemployment by quarters; check lag structure and mean reversion.
5. **Model under-predicted 2022–2025 by 15% cumulatively — action?** Finding (under-prediction is the dangerous direction); investigate structural break (post-COVID), re-estimate or overlay, benchmark.
6. **How do you treat 2020–21?** Dummy vs exclusion vs robust; show both; document.

## H. Validation-judgment ladder
1. **Walk me through validating a model.** SCOPE-D (process map §4).
2. **You found a High finding 3 days before go-live. What now?** Confirm evidence, communicate early, propose conditional approval (overlay/restricted use/extra monitoring) with remediation date, escalate per policy.
3. **The business head says the delay costs ₹50 crore. Your response?** Quantify the model-risk impact on the same scale; present options (conditional approval vs delay) to the decision body; my job is to make the risk visible and the decision informed — not to own the business decision.
4. **Your manager asks you to downgrade the finding to Medium. What do you do?** Ask for the evidence that changes my assessment; if none, document my view; escalate through the proper channel; independence is non-negotiable.
5. **How do you know your validation was effective?** Findings led to model changes/restrictions; issues closed with evidence; no post-validation surprises; audit/regulator didn't find what we missed.
6. **What's the most common thing validators get wrong?** Over-focusing on statistics and under-reviewing data, implementation and use — where most real losses come from.

## I. Vendor model (SBSS) ladder
1. **What is SBSS?** FICO small-business score, 0–300, blending principal and business credit data.
2. **No code access — how do you validate?** Vendor documentation review, local outcomes analysis and stability, segment checks, limitations, version control, customisations documented (SR 26-2 §VII).
3. **Vendor claims KS 45; you observe 32 on your population. Why?** Population differences (your applicants are a narrower band after policy rules), different bad definition/window, data-mapping issues, segment mix.
4. **SBA stopped using SBSS for 7(a) small-loan screening from 1 Mar 2026 — implications?** Model-use review (the use case changed), possible population shift in SBA-backed originations, potential move to internal scorecards (new model → validation), inventory update, monitoring re-baselining.
5. **FICO issues a new SBSS version — process?** Treat as model change: parallel run, swap-set, re-baseline thresholds and cut-offs, MRM review before switching.
6. **Would you build an internal scorecard instead?** If the uplift is material and stable, data is sufficient (enough bads), and governance cost is justified — use the vendor score as a benchmark/input.

## J. ML ladder
1. **XGBoost vs LR?** (Tier-1 I1.)
2. **Your GBM has Gini 0.04 higher on OOT — enough?** Test significance (DeLong), materiality ($ impact at the cut-off), stability across periods/segments, and the cost of explainability/governance.
3. **How do you explain one decline to a customer?** Top adverse SHAP contributors → mapped reason codes.
4. **SHAP says income is the top driver but it isn't in the model — how?** Leakage via a correlated proxy or a data bug; investigate feature lineage. (Or the interviewer is testing whether you check.)
5. **How would you detect bias?** Disparity metrics on proxies, proxy-variable analysis, ablation.
6. **Retraining monthly — how do you govern it?** Define in policy: same-spec refits within thresholds = monitored non-material change; spec/feature changes = re-validation.

## K. Governance ladder
1. **What's SR 11-7?** (H2.)
2. **What replaced it and what changed?** (H3.)
3. **If SR 26-2 is lighter, should our bank reduce validation?** Not automatically: group entities are subject to PRA/ECB/OSFI; internal risk appetite and past findings matter; use it to re-tier and focus effort, not to cut rigour on material models.
4. **How would you re-design validation cadence?** Tier + change velocity + monitoring signals + data availability → triggers (material change, Red monitoring, use change) + maximum interval per tier.
5. **GenAI chatbots — who validates them now?** Under the AI risk framework with MRM-style evidence (scope, testing, controls), because they're out of SR 26-2's formal scope.
6. **What should the board see on model risk?** Inventory and tier mix, validation coverage, overdue items, High findings and restrictions, overlays, monitoring breaches, aggregate model risk and emerging risks (AI).

## L. Behavioural grilling ladder
1. **You've done monitoring, not validation — why should we hire you for validation?** Monitoring is the outcomes/ongoing-monitoring pillar of validation; I've done root-cause and remediation work across IFRS 9, IRB and stress models plus a vendor model; I've practised full validations (show your sample memo).
2. **Give an example where you challenged something.** STAR-L with numbers.
3. **What if the developer is more senior than you?** Evidence over hierarchy; respectful, documented, escalate via process.
4. **Why leave a vendor/KPO?** To own validation decisions end-to-end inside the bank, closer to governance and regulators.
5. **Why this bank?** Specific: their model mix, regulatory scope, AI validation work, team reputation.
6. **What's your expected CTC?** Anchor to role band; see `04_behavioral_hr_negotiation.md`.
