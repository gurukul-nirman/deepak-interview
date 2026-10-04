# 06.3 · Case Studies — 16 scenarios with model answers

> Use **SCOPE-D** (Situate → Check data → Outcomes → Probe concept → Examine alternatives → Decide) or the **diagnosis matrix** (`03_monitoring_validation/01_...` §6). Time yourself: 5 minutes per case, spoken. Model answers are deliberately bullet-dense — say them in sentences.

---

### Case 1 — PSI breach, discrimination intact (application scorecard)
**Facts:** Score PSI 0.31; KS 41 vs 42 at development; A/E 1.03; marketing launched a digital channel 2 quarters ago (now 35% of applications).
**Answer:**
- Data first: volumes, missing rates by channel, field mapping for the new channel.
- Decompose by channel: PSI driven by digital applicants (younger businesses, lower vendor scores) — CSI on time-in-business and inquiries.
- Performance holds (KS, A/E) overall — **check by channel** (early-read delinquency for digital vintages; small bad counts → CIs).
- **Decision:** population shift with intact performance → no model change now; document the business change, add channel-level monitoring, re-baseline the PSI reference once digital volume stabilises; re-assess at maturity.
- **Finding?** Low/Medium: monitoring plan lacks channel segmentation.

### Case 2 — Discrimination drop + calibration failure (behavioural/PD model)
**Facts:** Gini 0.59 → 0.50 (95% CI 0.48–0.53); PSI 0.35; Jeffreys RED in low-risk grades G2–G4; overall A/E 1.07 (the repo demo).
**Answer:**
- Significant drop (CI excludes dev value) + slope flattening (low grades under-predicted) → a key input lost power.
- Characteristic analysis: vendor score CSI 0.30 and its univariate power fell; utilisation more predictive now.
- Findings: **High** (calibration in low grades — under-provisioning/under-pricing), **Medium** (discrimination), **Medium** (population shift).
- **Decision:** approve with conditions — interim overlay calibrated to last 4 quarters for G1–G4; recalibration in 1 quarter; redevelopment assessment (challenger shows richer specification helps); monthly monitoring.

### Case 3 — IFRS 9 staging relies on the backstop; big overlay
**Facts:** 85% of Stage 2 transfers via 30 DPD backstop; overlay = 18% of ECL for 6 quarters; Stage 2 coverage 4%.
**Answer:**
- SICR quantitative criteria aren't catching deterioration early → Stage 2 recognised late → ECL understated in the period before delinquency.
- Test alternative thresholds: hit rate (share of defaults previously in Stage 2), time in Stage 2 before default, false positives.
- Overlay: what limitation, how quantified, approval, sunset; likely compensating for the SICR weakness → double-counting risk when fixed.
- **Findings:** High — SICR thresholds ineffective; Medium — overlay governance. **Recommendation:** recalibrate SICR (relative + absolute PD thresholds), reconcile overlay, re-run ECL impact.

### Case 4 — Macro model under-predicts after rate hikes
**Facts:** IFRS 9/CCAR loss model fitted 2005–2019 under-predicted 2023–2025 losses by 15% cumulatively; MEVs: unemployment, GDP.
**Answer:**
- Under-prediction is the dangerous direction. Hypotheses: missing driver (interest rates/debt-service burden), post-COVID structural break, mix change.
- Tests: add rate/affordability variables with economic rationale; Chow test around 2020–22; re-estimate including recent data; dynamic OOT back-test; sensitivity.
- **Decision:** interim overlay sized to back-test error; model enhancement; document COVID treatment both ways.

### Case 5 — IRB PD fails calibration in a downturn
**Facts:** TTC/hybrid PD; Jeffreys RED in 3 grades this year; default rates up 40%.
**Answer:**
- For TTC models, one-year deviations in a downturn are expected; compare to LRADR and check migration behaviour (TTC = fewer migrations, DR within grade rises).
- Check DoD/data changes and representativeness.
- If deviation persists beyond what the cycle explains or appears in benign years → recalibrate/increase MoC.
- **Report** per ECB/PRA expectations with rationale; no automatic redevelopment.

### Case 6 — Stress model gives non-monotonic losses
**Facts:** Severely adverse losses below baseline in 3 of 9 quarters; GDP coefficient positive in one segment.
**Answer:**
- Wrong-sign coefficient (likely multicollinearity with unemployment or spurious correlation) → **High** finding.
- Check MEV correlations/VIF, lag structure, segment data sufficiency; re-specify with sign constraints/parsimony.
- Scenario monotonicity and peak timing as explicit validation tests; benchmark with top-down model.

### Case 7 — Vendor score drift (FICO SBSS) + regulatory change
**Facts:** SBSS-based BCC model: local KS 36 → 30 over 4 quarters; SBA discontinued SBSS screening for 7(a) small loans from 1 Mar 2026.
**Answer:**
- Local outcomes analysis: bad rate by score band vs vendor odds; segment (young businesses, thin files); input-mapping checks.
- SBA change: is the bank's SBA-backed flow now underwritten differently (population shift)? Is SBSS still used for SBA loans or replaced by internal scoring (new model → validation)?
- **Findings:** Medium — discrimination decline; model-use review required.
- **Actions:** benchmark an internal scorecard using SBSS as an input; update inventory use description; re-baseline thresholds.

### Case 8 — Model used outside scope
**Facts:** BCC scorecard used for non-BCC term loans since March (14% of volume).
**Answer:** SR 26-2: use beyond intended purpose needs additional analysis and controls. Assess performance on the new segment (early reads), conceptual fit (installment vs revolving behaviour), and restrict use until evidence exists; Medium/High finding depending on exposure.

### Case 9 — CSI spike from a data change
**Facts:** CSI on "inquiries_6m" = 0.73 overnight; no business change.
**Answer:** Classic data/definition change (bureau attribute redefinition, look-back window change, mapping error). Reconcile to source, check bureau release notes, compare distributions by data vendor batch. Fix the feed or re-map; quantify score impact (characteristic analysis); log as a data-quality incident; add a control.

### Case 10 — Implementation error
**Facts:** Production assigns missing time-in-business to the lowest-risk bin (3.7% of accounts).
**Answer:** High finding (systematic score overstatement up to ~22 points); fix mapping; re-score affected population; impact on approvals/losses; add implementation reconciliation tests (dev vs prod on a sample, edge cases) to change-management controls.

### Case 11 — ML challenger beats the champion
**Facts:** GBM OOT Gini +0.04 vs scorecard (DeLong p = 0.006).
**Answer:** Significant isn't enough: materiality ($ at the cut-off), stability across periods/segments, explainability (SHAP reason codes), fairness, calibration, implementation and monitoring cost. Options: adopt constrained GBM; or engineer the discovered interactions into the scorecard; or keep GBM as monitored challenger. Decide with evidence and governance.

### Case 12 — Low-default portfolio
**Facts:** Corporate PD model; 12 defaults in 8 years; 9 grades.
**Answer:** Statistical calibration tests have little power; use Pluto–Tasche upper bounds, external ratings benchmarks (agency default studies), expert review, conservative MoC; focus validation on rank-ordering vs external ratings and qualitative factors; document limitations.

### Case 13 — Designing validation cadence after SR 26-2
**Facts:** 300 models; current policy: all Tier 1 annually.
**Answer:** Re-tier on inherent risk × materiality; define triggers (material change, Red monitoring, use change, data change) + maximum intervals by tier (e.g., Tier 1 ≤ 2 years with annual review of monitoring); keep regulator-specific requirements for group entities (PRA/ECB/OSFI); pilot, measure validator capacity freed, report to committee. **[Assumption — illustrative cadences]**

### Case 14 — LGD under-prediction
**Facts:** Realised LGD 48% vs predicted 38% on closed workouts; many open workouts.
**Answer:** Check workout-completion bias (closed cases skew), discounting, cost allocation, collateral valuation timing, cure-rate shifts; t-test by segment; downturn adequacy (IRB) or PIT forward-looking adjustments (IFRS 9); recalibrate or MoC; treat open workouts properly.

### Case 15 — Pressure and independence
**Facts:** Go-live in 3 days; you raised a High finding; business head and your manager push to downgrade.
**Answer:** Re-verify evidence; offer conditional approval (overlay, restricted use, monitoring, deadline); don't downgrade without new evidence; document; escalate via committee. Independence + solution-orientation.

### Case 16 — Validating an Indian bank's new ECL model (RBI 2027)
**Facts:** Bank moving from IRAC provisioning to ECL from 1 Apr 2027.
**Answer:** Start with **data** (DPD history, default/NPA alignment, restructured accounts, write-offs, EIR computation), **staging** (30/90 DPD + SICR criteria, prudential floors), **PD/LGD/EAD** methodologies with macro linkage (limited Indian macro history → parsimony), **scenarios & weights**, **overlays**, **floors vs model outputs** (which binds and why), **transition impact** (CET1), **governance** (board committee incl. CFO/CRO), and **MRM** alignment with the RBI draft guidance. Expect data quality to be the biggest finding area.
