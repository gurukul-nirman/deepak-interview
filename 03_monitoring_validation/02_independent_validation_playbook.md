# 03.2 · Independent Validation Playbook — how a second-line validator actually works

> The VP-bar question is never "what is validation?" It's **"Here's a model — validate it. What do you do, in what order, what do you find, and what do you conclude?"** This file gives you the end-to-end process, the workstreams, how to write findings, and how to defend them.

---

## 1. What validation is (regulatory definition you can quote)

- **SR 11-7 (2011):** validation is "the set of processes and activities intended to verify that models are performing as expected, in line with their design objectives and business uses." Core elements: **(1) evaluation of conceptual soundness, (2) ongoing monitoring (incl. process verification and benchmarking), (3) outcomes analysis (incl. back-testing).** **[Certain]**
- **SR 26-2 (17 Apr 2026)** keeps the three components — **conceptual soundness, outcomes analysis, ongoing monitoring** — but states that the "nature and rigor of validation generally align with the model's approach, use, and materiality," that timing/frequency vary by purpose, methodology, change frequency and data, and that validation quality "depends on the rigor and effectiveness of the review rather than on organizational structure." **[Certain — primary text]**
- **PRA SS1/23 (UK):** Principle 4 — independent model validation. **[Certain]**

**Three lines of defence:** 1st line = model owners/developers/users · **2nd line = MRM/validation (you)** · 3rd line = internal audit (tests whether MRM itself works).

---

## 2. Validation types

| Type | Trigger | Depth |
|---|---|---|
| **Initial (pre-implementation)** | New model | Full scope |
| **Periodic revalidation** | Risk-based cadence (Tier 1 often annual or 1–2 yrly; SR 26-2 removed the "at least annually" default) | Full or targeted |
| **Change validation** | Material model change (re-estimation, new variable, new segment, new use) | Scope = the change + its impact |
| **Annual review / monitoring review** | Ongoing monitoring results; breaches | Light; escalates if Red |
| **Targeted / thematic review** | Specific concern (e.g., overlay, data issue) | Narrow |
| **Vendor model validation** | Third-party model (e.g., FICO SBSS) | Conceptual soundness from vendor docs + local outcomes |
| **Temporary approval / use-before-validation** | Urgent business need | Allowed with limits, extra monitoring, stakeholder notice (SR 26-2 recognises this) |

---

## 3. Model tiering (risk-based scoping)

Inputs (SR 26-2 language): **inherent risk** (complexity, assumptions, data quality/constraints) in the context of **materiality** = **exposure** (portfolio size/impact) + **purpose** (regulatory/financial-reporting/risk uses rank higher).

| Tier | Example | Validation depth | Typical cadence |
|---|---|---|---|
| **1 (High)** | IRB PD for a large retail book; IFRS 9/CECL ECL engine; CCAR loss models | Full scope incl. independent replication & challenger | Frequent full review + quarterly monitoring |
| **2 (Medium)** | Behavioural scorecard for a mid-size portfolio; collections model | Full scope, lighter replication | Every 2–3 yrs + monitoring |
| **3 (Low)** | Marketing response model; small portfolio tool | Light / desk review | Every 3+ yrs; monitoring only |

*Cadences are examples — set by each bank's MRM policy.* **[Assumption]**

---

## 4. End-to-end process (Tier 1 initial validation, ~8–12 weeks) **[Assumption — typical]**

```
Intake → Scoping memo → Document request → Kick-off → Workstreams (A–J) → Draft findings
   → Factual-accuracy review with owner → Final report + rating → Committee approval
   → Remediation tracking → Issue-closure validation → Monitoring
```

**Document request list (ask on day 1):** model development document (MDD), technical/user guides, data dictionary & lineage, development code + datasets (or extracts), performance results, prior validation reports & open findings, monitoring reports, implementation/UAT evidence, overlay/override policies, vendor documentation (for vendor models).

---

## 5. Workstreams — what to test, what good looks like, typical findings

### A. Purpose, scope, use, limitations
- Test: is the intended use documented and aligned with actual use? Are limitations explicit?
- Typical finding: model used for a product/segment not in the development sample (e.g., SBSS cut-offs applied to a new non-BCC loan product).

### B. Data
- **Lineage & reconciliation:** dev data reconciles to source (counts, balances, defaults).
- **Quality:** completeness, accuracy, consistency, timeliness; missing/outlier treatment.
- **Sample design:** observation & performance windows, bad/default definition (consistent with policy/regulation), exclusions (fraud, deceased, closed, VIP) and their impact, indeterminates.
- **Representativeness:** development vs current portfolio (PSI/CSI on inputs); downturn coverage for IRB/stress models.
- Typical findings: default definition in dev ≠ production; exclusions remove 12% of bads without rationale; COVID-period data used without treatment.

### C. Conceptual soundness
- Methodology choice vs alternatives (why LR not GBM; why survival vs Markov for lifetime PD).
- Theory/business intuition: signs, monotonicity, magnitudes.
- Segmentation rationale and testing.
- Variable selection: statistical (IV, significance, stability) **and** business sense; multicollinearity.
- Transformations (binning, WoE, capping), assumptions (e.g., stationarity, independence), expert judgment documented and evidenced.
- Regulatory compliance (IRB requirements, IFRS 9 SICR principles, CECL R&S forecast).
- Typical findings: counter-intuitive sign kept "because significant"; binning not monotonic; segmentation not tested; expert-judgment overlay with no evidence.

### D. Replication / independent re-performance
- Re-run developer code **and/or** independently re-code key steps; reproduce coefficients/outputs within tolerance.
- Typical finding: cannot reproduce dev sample counts → undocumented filters.

### E. Outcomes analysis / performance testing
- In-sample, out-of-sample (holdout), **out-of-time**; discrimination, calibration, stability; back-testing against realised outcomes; segment-level results.
- Typical finding: strong in-sample, weak OOT → overfitting or regime change.

### F. Benchmarking & challenger models
- Alternative method (GBM vs LR), alternative segmentation, vendor/bureau scores, industry/agency benchmarks.
- **Purpose:** test whether the chosen approach is reasonable — the challenger *informs*, it doesn't *replace*.
- Typical finding: challenger materially outperforms in a segment → model misses non-linearity/interaction → recommend enhancement.

### G. Sensitivity & stress analysis
- Shock inputs/assumptions one at a time and jointly; scenario sensitivity; parameter uncertainty (bootstrap CIs on coefficients/ECL).
- Typical finding: ECL highly sensitive to one macro variable's lag choice; not disclosed as a limitation.

### H. Implementation testing / process verification
- Production vs development code/output (parallel run), input feed mapping, scoring logic, rounding, cut-off application, controls and change management (incl. EUCs/spreadsheets).
- Typical finding: production uses an older WoE mapping; missing values default to 0 instead of the MISSING bin.

### I. Ongoing-monitoring plan review
- Right metrics? Thresholds justified? Frequency appropriate to tier? Owners and escalation defined? Early-read metrics for long performance windows?
- Typical finding: thresholds set after seeing results; no calibration test in the plan.

### J. Use, overrides, overlays, documentation
- Override and overlay governance; documentation sufficient for a knowledgeable third party to understand/replicate.
- Typical finding: overlay in place for 6 quarters with no sunset or re-justification.

---

## 6. Findings — how to write them (this is a scored skill)

**Anatomy (CCCER + action):**
| Element | Meaning |
|---|---|
| **Title** | Short, specific |
| **Severity** | High / Medium / Low (definitions below) |
| **Condition (observation)** | What you found — with evidence and numbers |
| **Criteria** | The expectation: policy, regulation, standard, best practice |
| **Cause** | Why it happened (if known) |
| **Effect (impact)** | Risk/financial/regulatory consequence — quantified where possible |
| **Recommendation** | Specific, testable action |
| **Owner / due date / compensating control** | Accountability and interim mitigation |

**Severity scale (typical; bank-specific) [Assumption]:**
- **High:** material impact on model output/decisions or regulatory non-compliance; model shouldn't be used (or only with restrictions/overlay) until resolved. Typical remediation ≤ 3–6 months.
- **Medium:** weakness that could materially affect outputs under some conditions or that undermines confidence; remediation ≤ 6–12 months.
- **Low:** best-practice or documentation gap with limited impact.
- (Some banks add **Critical** or use **Level 1/2/3**.)

### Sample findings (use these as templates)

**F1 — HIGH — PD under-estimation in low-risk grades (calibration)**
- *Condition:* On the Q2-2026 monitoring sample (N=10,000), observed default rates exceed predicted PDs in grades G2–G4 (e.g., G3: DR 6.2% vs PD 3.5%; Jeffreys p < 0.001). Portfolio A/E = 1.07.
- *Criteria:* MRM policy requires PD calibration within tolerance at grade level (95% confidence).
- *Cause:* Reduced predictive power of the vendor score input post development (characteristic drift).
- *Effect:* Under-provisioning / under-pricing for ~27% of accounts; ECL understated by an estimated $[x]m.
- *Recommendation:* Interim overlay calibrated to the last 4 quarters; recalibrate PD by Q1-2027; back-test after two quarters.

**F2 — MEDIUM — Discrimination deterioration**
- *Condition:* Gini fell from 0.589 (development holdout) to 0.504 (14% relative); 95% bootstrap CI [0.478, 0.534] excludes the development value.
- *Criteria:* Policy Amber threshold: relative Gini decline 10–20%.
- *Effect:* Weaker cut-off effectiveness; higher bad rates at current approval rate.
- *Recommendation:* Characteristic-level root cause; assess redevelopment; monthly monitoring until resolved.

**F3 — MEDIUM — Model used outside development scope**
- *Condition:* Scorecard developed on business credit cards (BCC) is applied to non-BCC term loans since Mar-2026 (14% of new volume).
- *Criteria:* SR 26-2: using a model beyond its intended purpose introduces additional risk; sound practice involves additional analysis of the new usage and controls.
- *Recommendation:* Restrict use to BCC pending a segment-specific performance assessment; document as a limitation.

**F4 — HIGH — Implementation mismatch**
- *Condition:* Production assigns missing time-in-business to the lowest-risk bin instead of the MISSING bin (3.7% of accounts).
- *Effect:* Scores overstated by up to 22 points for affected accounts.
- *Recommendation:* Fix mapping; re-score affected population; add an implementation reconciliation control.

**F5 — LOW — Documentation**
- *Condition:* MDD doesn't document binning rationale for 3 of 6 variables.
- *Recommendation:* Update MDD before next annual review.

**More finding themes to know:** undocumented exclusions · default definition inconsistency · COVID data treatment not justified · insufficient downturn data (IRB/stress) · overlays without sunset · macro scenario weights unsupported (IFRS 9) · SICR thresholds not back-tested · counter-intuitive signs · multicollinearity hiding true effects · OOT not performed · vendor model not locally validated · monitoring thresholds not justified.

**Writing rules:** evidence + numbers · criteria cited · impact quantified · recommendation testable · no blame language ("the model…" not "the developer failed…") · separate **findings** (must fix) from **recommendations/observations** (should consider).

---

## 7. Validation outcome (overall rating)

| Outcome | Meaning |
|---|---|
| **Approved / Fit for purpose** | No High findings; Mediums with plans |
| **Approved with conditions (restrictions)** | Use permitted with limits (scope restriction, overlay, enhanced monitoring) and remediation deadlines |
| **Not approved / Rejected** | Material deficiencies; can't be used (or must be replaced) |

Plus: **model risk rating** for the inventory (e.g., inherent risk × residual risk after findings).

---

## 8. Effective challenge — and handling pushback

- **SR 11-7:** effective challenge depends on **incentives, competence, and influence**. **SR 26-2:** requires **appropriate expertise, sufficient independence to maintain objectivity, and organizational standing and influence to effect change.** **[Certain]**
- **Evidence of effective challenge:** documented questions, responses, and how the model changed as a result.

**Pushback script (owner disputes a High finding before go-live):**
> "Let's separate the evidence from the remediation. I'm happy to re-check the analysis together — if there's an error in my work I'll correct it. If the evidence stands, the severity stands. What I'm flexible on is the path: we can approve with conditions — an overlay sized to the observed gap, use restricted to segment X, monthly monitoring — with a 90-day remediation date. If we still disagree, we escalate through the Model Risk Committee with both positions documented."

Key behaviours: **calm, evidence-first, solution-oriented, escalation as a process (not a threat)**.

---

## 9. Validation report — template

1. Executive summary: model, purpose, tier, scope, **overall outcome**, key findings (by severity), conditions.
2. Model overview: purpose & use, methodology, data, owner/developer, change history.
3. Scope & approach: what was tested and what wasn't (and why).
4. Assessment by area: data · conceptual soundness · replication · outcomes · benchmarking · sensitivity · implementation · monitoring plan · use/governance.
5. Findings table: ID, title, severity, owner, due date.
6. Model limitations & compensating controls.
7. Conclusion & conditions of use.
8. Appendices: test results, code references, evidence.

---

## 10. Vendor model validation (your SBSS edge)

Principles still apply (SR 26-2 §VII): develop an understanding of the vendor model's **conceptual soundness, design, development data, and performance**; perform **ongoing monitoring and outcomes analysis**; document and justify **customisations**.

**Checklist:** vendor documentation & validation summaries · input data mapping (what the bank sends vs what the vendor expects) · **local performance** (KS/Gini, bad rate by score band vs vendor odds chart) · stability · segment performance · limitations (thin-file, start-ups) · version-change process (parallel run, swap-set, threshold re-baseline) · contractual rights to information · contingency if the vendor model is withdrawn or its use changes (e.g., SBA dropping SBSS screening for 7(a) small loans from 1 Mar 2026).

---

## 11. Quick checklists by model type

**Retail PD scorecard:** sample design · bad definition · exclusions · reject inference · binning/WoE monotonicity · variable selection (IV, VIF, signs) · scaling · OOT · cut-off strategy impact · overrides.

**IFRS 9:** segmentation · 12m & lifetime PD construction · PIT adjustment / macro linkage · SICR thresholds (back-tested) · 30 DPD backstop · LGD (cures, discounting at EIR, collateral) · EAD/CCF (behavioural life for revolving) · scenarios & weights · overlays/PMAs · ECL reconciliation to GL.

**IRB:** rating philosophy · LRADR & calibration · MoC (EBA categories) · downturn LGD · CCF · default definition (DoD) · representativeness · use test · regulatory-template tests (Jeffreys, AUC change, migration/HHI).

**Stress testing:** MEV selection rationale · stationarity & cointegration · signs/magnitudes · autocorrelation · OOT back-test with realised macro · sensitivity · scenario reasonableness (severely adverse > baseline losses, timing) · COVID treatment · overlays · aggregation consistency.

**ML model:** why ML · leakage checks · hyperparameter governance · monotonic/interaction constraints · explainability (SHAP global/local; reason codes) · fairness · robustness (perturbation, seeds) · benchmark vs LR · drift monitoring · retraining = model change?
