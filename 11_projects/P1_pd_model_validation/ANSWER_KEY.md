# ⚠️ ANSWER KEY — Project P1 (CC-PD-01)

> **Spoiler.** Open this only after your findings list and overall conclusion are written down. The learning comes from
> finding the issues yourself; reading this first turns a portfolio project into a reading exercise.
> Do **not** include this file in a public portfolio repo.

Labels used: **[Certain]** = fact you can quote · **[Likely]** = well supported; verify on your copy of the data or source
· **[Assumption]** = illustrative.

---

## 1. Self-scoring (100 points)

| Component | Points | How to score |
|---|---|---|
| High findings found (F1–F4) | 24 | 6 each — the issue *and* the right evidence |
| Medium findings found (F5–F12) | 24 | 3 each |
| Low finding found (F13) | 2 | |
| Write-up quality | 20 | Condition–Criteria–Cause–Effect–Recommendation present; numbers; impact quantified; no blame language |
| Severity calibration | 10 | Your severities within one level of the key, with a reason; no inflating, no downgrading without evidence |
| Overall conclusion & conditions | 10 | "Not approved" for the intended uses, with a credible remediation path (and an optional restricted interim use) |
| Reproducibility | 10 | Code runs end-to-end; report numbers match `validation_evidence.md` |

**Bands:** ≥ 85 portfolio-ready · 70–84 fix the gaps, then publish · < 70 redo the weak sections before using it in interviews.
Log every miss in `09_progress/gap_log.md`.

**Expected overall outcome: Not approved for the intended uses** (four High findings). A defensible extra: a restricted
interim use as a *next-month* collections-prioritisation ranking tool, only after F2 and F4 are fixed, because ranking
does not need calibrated PD levels.

---

## 2. Findings at a glance

| ID | Finding | Severity | Where the evidence is |
|---|---|---|---|
| F1 | Target–use mismatch: next-month "default payment" target used as a 12-month PD (IFRS 9, pricing) | **High** | MDD §1–2; evidence §1 (target note) |
| F2 | Protected characteristics (sex, marital status, age) used as predictors | **High** | MDD §4, §8; evidence §3, §9 |
| F3 | PD level overstated: 50/50 undersampling without prior correction; calibration claim invalid | **High** | MDD §3, §6; evidence §5 |
| F4 | Implementation defect: 4-d.p. coefficient table zeroes the amount coefficients in production | **High** | MDD §9 + Appendix A; evidence §10 |
| F5 | Model risk tier understated (Tier 3 proposed for a financial-reporting and customer-decision model) | Medium | MDD §1 |
| F6 | Performance evidence is in-sample only; no holdout exists | Medium | MDD §3, §5; evidence §4 |
| F7 | Stability claim unsupported; the PSI test does not measure model stability; no out-of-time evidence | Medium | MDD §7; evidence §6 |
| F8 | Undocumented codes and nominal codes modelled as continuous; "no data treatment required" | Medium | MDD §2, §4; evidence §1, §3 |
| F9 | Multicollinearity (BILL_AMT1–6) with sign reversals; unreliable reason codes | Medium | Evidence §3 |
| F10 | Cut-off 0.50 set on the balanced sample; no business rationale | Medium | MDD §1, §5; evidence §9 |
| F11 | No fairness testing; "data-driven = unbiased" fallacy | Medium | MDD §8; evidence §9 |
| F12 | No ongoing-monitoring plan ("annual review" by the developer) | Medium | MDD §10 |
| F13 | Limitations "None identified"; no benchmark or challenger | Low | MDD §11 |

Reasonable people differ on F5, F6 and F11 by one level. Defend your choice with evidence.

---

## 3. Findings in detail

### F1 — HIGH — The target does not support the intended use
- **What was planted:** the target is "default payment next month" — a **one-month** outcome after a six-month observation
  window — but the MDD sells the model as a **12-month PD** for IFRS 9 Stage 1 and pricing.
- **Criteria:** IFRS 9 Stage 1 = 12-month ECL (IFRS 9 §5.5.5) **[Certain]**; Basel PD is a one-year probability
  (CRR Art. 4(1)(54)) **[Certain]**; IFRS 9 default definition has a 90-days-past-due rebuttable presumption (B5.5.37)
  **[Certain]**. The dataset's "default payment" is not documented as 90+ DPD **[Likely]**. SR 11-7 / SR 26-2: use must
  be consistent with the model's design and purpose **[Certain]**.
- **Effect:** a one-month PD understates 12-month default risk for most accounts, yet here it is also inflated by F3, so
  the net error is unknown in both size and direction. The model cannot be relied on for ECL or pricing.
- **Recommendation:** rebuild on account-month panel data with a 12-month outcome window and a default definition
  aligned to the bank's IFRS 9 policy. Until then, restrict any use to short-horizon ranking (for example, collections
  prioritisation).
- **Interview line:** "The first thing I check is whether the target matches the use. This one didn't, and no amount of
  calibration fixes a horizon mismatch."

### F2 — HIGH — Protected characteristics used as predictors
- **What was planted:** SEX, MARRIAGE and AGE are entered directly. The MDD defends them as "improving fit".
- **Criteria:**
  - **US:** ECOA / Regulation B prohibits considering sex and marital status (12 CFR 1002.6(b)) **[Certain]**. Age may be
    used only in an empirically derived, demonstrably and statistically sound system, and applicants aged 62+ must not
    receive a negative factor **[Certain on substance]**.
  - **EU:** the Consumer Credit Directive (EU) 2023/2225 non-discrimination provisions **[Likely]**, and AI Act Art. 10
    bias examination for high-risk credit scoring (from 2 Dec 2027) **[Certain]**.
  - **India:** the RBI Fair Practices Code bars discrimination on grounds of sex, caste and religion **[Likely]**.
  - **Singapore:** MAS FEAT fairness principle **[Certain]**.
- **Evidence to show:**
  - The coefficients and their contribution.
  - Holdout Gini of the champion **without** SEX/MARRIAGE/AGE vs with them, with the DeLong p-value (§7). On synthetic
    data the difference is about 0.0001 (p ≈ 0.70). Removing them costs almost nothing in power while removing a legal
    exposure.
  - The AGE coefficient sign and the 62+ flag rate (§9).
- **Recommendation:**
  - Remove the protected attributes.
  - Test the remaining variables for proxy effects (AIR before and after).
  - Document a less-discriminatory-alternative search.
  - Get Compliance / Legal sign-off.
- **Trap:** "statistically significant" is not a defence. Legality decides admissibility, not p-values. Direct use is
  disparate *treatment*, whichever group it disadvantages.

### F3 — HIGH — PD level overstated (uncorrected undersampling)
- **What was planted:** the model is estimated on a 50/50 sample, with no prior correction or weighting. The MDD then
  calls it "well calibrated" because mean PD equals 50% *on the balanced development sample*, and HL passes there.
- **Evidence:**
  - Holdout at the natural default rate: mean PD ≈ **40.6%** vs observed **23.8%**, A/E ≈ **0.59**, HL rejects
    (synthetic run).
  - **Real data:** expect roughly 0.40–0.45 vs 0.22 **[Likely]**.
  - The one-sided per-grade Jeffreys tests show **all GREEN**. They only test *under*-prediction, so they cannot see this
    problem. Say so in the report.
  - After prior correction (your TODO #2), mean PD ≈ 24.1% vs 23.8% and HL p ≈ 0.11 on synthetic data.
- **Why Gini is unaffected:**
  - ROC/AUC depends only on the class-conditional score distributions, which random within-class sampling preserves.
  - Logistic-regression slopes are consistent under outcome-based (case-control) sampling (Prentice & Pyke, 1979); only
    the intercept shifts, by ln[(ȳ/(1−ȳ))·((1−τ)/τ)] **[Certain]**.
- **Criteria:** IFRS 9 requires an unbiased, probability-weighted ECL (§5.5.17) **[Certain]**. Pricing and limit
  decisions need calibrated levels.
- **Effect:** "conservative" is not acceptable here:
  - IFRS 9 provisions are overstated (financial misstatement).
  - Line-increase pricing overcharges, which brings conduct risk and adverse selection.
  - Too many customers get line decreases.
- **Recommendation:**
  - Prior-correct the intercept, or weight the sample (King & Zeng, 2001).
  - Recalibrate on representative data with the right horizon (F1).
  - Re-test calibration with two-sided tests and A/E.

### F4 — HIGH — Production does not implement the validated model
- **What was planted:**
  - IT implemented the Appendix A table at 4 d.p. Coefficients on raw NT$ amounts are around 10⁻⁶ and become **0.0000**.
    On synthetic data that is LIMIT_BAL, BILL_AMT1–6 and PAY_AMT1–6 — 13 coefficients. Count yours in the §10 table.
  - The clue was visible in the MDD: a coefficient printed as −0.0000 with p = 0.000.
- **Evidence (synthetic):**
  - 100% of PDs differ.
  - Mean PD 40.5% → 48.0%; Gini 0.694 → 0.680.
  - Flag rate at 0.50 rises from 34.9% to 48.2%, and **13.3% of accounts change decision**.
- **Criteria:** the model in production must be the model that was validated. SR 11-7 process verification and
  implementation testing **[Certain]**; PRA SS1/23 Principle 4 (development, implementation and use) **[Likely numbering]**.
- **Recommendation:**
  - Rescale inputs (per NT$1,000, or logs) or implement full precision.
  - Add an automated parallel-run reconciliation with a tolerance (e.g., |ΔPD| < 10⁻⁶) as a go-live gate.
  - Re-score affected accounts.
  - Treat the coefficient table as a controlled artefact.
- **Trap:** calling this "Low — rounding". The size of the error is in the decision impact, not the decimal places.

### F5 — MEDIUM — Model tier understated
- **Condition:** Tier 3 is proposed because "the model is a standard logistic regression". Its uses are IFRS 9 ECL
  (financial reporting), pricing and customer-impacting line decreases.
- **Criteria:** tiering is driven by materiality and use as well as complexity (SR 26-2 risk-based approach; PRA SS1/23
  tiering by materiality and complexity) **[Likely wording]**. Method simplicity does not lower the tier.
- **Recommendation:** Tier 1 (or the bank's highest tier for financial-reporting models). Apply the matching validation
  depth and monitoring frequency.

### F6 — MEDIUM — Performance evidence is in-sample only
- **Condition:** every defaulter was used in estimation, so no independent test set exists. The Gini is reported on the
  estimation sample.
- **Evidence:** re-apply the developer's method on a 70/30 split. Synthetic results: in-sample Gini 0.701 vs holdout
  0.688; 95% CI [0.670, 0.704].
- **Nuance:** the gap is small. A 23-variable logistic regression on about 13k rows has low variance. **The finding is
  about missing evidence, not a measured collapse.** Say that; don't inflate it.
- **Recommendation:** a holdout plus out-of-time test as standard. Report confidence intervals.

### F7 — MEDIUM — Stability claim unsupported
- **Condition:** the "stability test" is PSI(PAY_6 → PAY_0): April vs September repayment status of the *same* accounts.
  That compares two input distributions within one snapshot. It does not test score stability or whether the
  score–default relationship holds over time.
- **Extra catch:** code 1 ("one month late") is common in PAY_0 but almost absent from PAY_2–PAY_6. So that PSI is partly
  a coding artefact (see F8) **[Likely — check the code-count table in §1]**.
- **Representativeness:** one six-month window from 2005 Taiwan. That period likely coincides with the Taiwanese
  card-debt crisis, a stressed environment **[Likely]**.
- **Recommendation:**
  - Obtain multiple vintages.
  - Run out-of-time validation.
  - Disclose the limitation.
  - Put tight early monitoring in place (F12).

### F8 — MEDIUM — Data dictionary violations and inappropriate variable treatment
- **Condition:**
  - EDUCATION 0/5/6, MARRIAGE 0 and PAY codes −2 and 0 are not in the data dictionary.
  - Code 1 is inconsistent across months.
  - Nominal variables (EDUCATION, MARRIAGE) and repayment status (where −2/−1/0 are not on a months-late scale) are
    entered as linear numbers. Bad rate by PAY_0 code is strongly non-linear (§1).
  - "No missing values → no data treatment" is wrong: undocumented codes *are* unknown values.
- **Recommendation:**
  - Data-owner sign-off on the dictionary.
  - Explicit mapping of undocumented codes, with rationale.
  - Binning / WoE or dummies for the repayment status variables.

### F9 — MEDIUM — Multicollinearity with sign reversals
- **Condition:** BILL_AMT1–6 VIFs are far above 10 (about 90 on synthetic data; real-data correlations are typically
  0.8–0.95 **[Likely]**). Coefficient signs alternate across months, and some PAY_x / PAY_AMT signs are counter-intuitive.
- **Effect:**
  - Coefficients are unstable and uninterpretable.
  - Adverse-action reason codes become unreliable.
  - Behaviour changes if the correlation structure shifts.
- **Recommendation:** replace the raw series with utilisation, average balance and trend, drop redundant terms or
  regularise, then re-check signs.

### F10 — MEDIUM — Cut-off without rationale
- **Condition:** 0.50 was chosen on a balanced sample, where it flags about 49% of accounts. On the natural population the
  same threshold flags a different share (synthetic holdout: 35.3%). After prior correction it would flag far fewer.
  The threshold sits on an uncalibrated scale.
- **Recommendation:**
  - Set the cut-off on calibrated PDs using expected loss, profit and operational capacity.
  - Document the customer impact.
  - Monitor the flag rate (F12).

### F11 — MEDIUM — No fairness testing
- **Condition:** no outcome testing. The MDD argues that a data-driven model is unbiased.
- **Evidence:** flag rates by sex, marital status and age band; AIR (TODO #4; synthetic SEX AIR = 0.976).
- **Nuance:**
  - AIR measures outcome disparity (disparate impact). It is a different question from direct use (F2).
  - The four-fifths rule is a screening heuristic from the US employment Uniform Guidelines, not a legal safe harbour
    **[Certain]**.
  - A disparity explained by legitimate risk factors still needs a documented business-necessity review.
- **Recommendation:** fairness testing at every cut-off change and quarterly, with AIR by group plus a proxy analysis.

### F12 — MEDIUM — No monitoring plan
- **Condition:** "reviewed annually by the development team". No metrics, thresholds, frequency, escalation or second-line
  oversight.
- **Criteria:** SR 11-7 ongoing monitoring (process verification, benchmarking, outcomes analysis) **[Certain]**.
- **Recommendation:** see the TODO #6 solution below. Justify each threshold.

### F13 — LOW — Limitations not identified
- **Condition:** "None identified."
- **The MDD should list at least:**
  - one-month horizon;
  - single 2005 snapshot (likely stressed);
  - balanced sampling;
  - undocumented codes;
  - no out-of-time test;
  - no macro sensitivity (needed for IFRS 9 forward-looking information);
  - no benchmark or challenger.
- **Recommendation:** add a complete limitations section, with compensating controls.

---

## 4. Common mistakes (check your report against these)
1. **"Undersampling biased the Gini."** Wrong. It biases the PD *level*, not the ranking (§F3).
2. **Treating the HL rejection as the headline.** On large samples HL rejects small, immaterial gaps. The headline is A/E
   ≈ 0.6, which is huge, plus the decile table.
3. **Trusting all-GREEN Jeffreys results.** They are one-sided (under-prediction only).
4. **"Remove SEX and the model is fair."** Proxies remain. Test outcomes.
5. **Rating F4 Low.** Model-as-implemented ≠ model-as-validated is High by default.
6. **Over-claiming F6.** The measured in-sample/holdout gap is small. The issue is evidence.
7. **Recommending "rebuild with better data" without saying what.** Name the horizon, default definition, panel
   structure and out-of-time design.
8. **Blame language.** Write "the model…" and "the documentation…", never "the developer failed…".

---

## 5. Pipeline checkpoints (run with `--data synthetic` to check your TODO code)

| TODO | Expected on synthetic data |
|---|---|
| #1 undocumented_codes | EDUCATION 0/5/6 = 27/303/148 rows; MARRIAGE 0 = 63; PAY_0 −2 = 6,177 and 0 = 7,337 |
| #2 prior_correct | Mean PD 24.13% vs DR 23.82%; HL 15.6, p = 0.111 |
| #3 sensitivity | PAY_0 +1 → mean PD +0.0748; BILL_AMT +10% → +0.0001; PAY_AMT −50% → +0.0003 |
| #4 AIR (SEX 1 vs 2) | 0.976 |
| #5 parallel run | pct_mismatch 100%; max abs diff 0.672; mean PD 0.4047 → 0.4795; Gini 0.694 → 0.680; flags 34.9% → 48.2%; 13.3% changed |

Your real-data numbers will differ. Those are the ones that go in the report.

---

## 6. Interview kit

**60-second pitch (fill in your real numbers):**
> "To build validation depth beyond monitoring, I independently validated a credit-card PD model on public data, using a
> simulated developer pack. I replicated the model; tested data, conceptual soundness, discrimination, calibration,
> stability, fairness and implementation; and wrote a committee-style report. It failed for four High reasons:
> - a one-month target sold as a 12-month IFRS 9 PD;
> - sex and marital status used as predictors;
> - PDs about [x]× the observed default rate because 50/50 undersampling wasn't corrected;
> - a production defect where 4-d.p. rounding removed [n] coefficients and changed the decision for [x]% of accounts.
>
> I recommended non-approval with a remediation path. My WoE and monotonic-GBM challengers matched the performance
> without any demographic variables."

**Drill-downs to rehearse:**

| Question | Crisp answer |
|---|---|
| Why doesn't undersampling change Gini? | ROC depends on class-conditional score distributions, which random within-class sampling preserves. LR slopes are consistent under case-control sampling; only the intercept shifts. |
| How did you fix the PD level? | Prior correction: subtract ln[(ȳ/(1−ȳ))·((1−τ)/τ)] from the log-odds. Alternatives: weights, or recalibration on representative data. But the horizon problem (F1) remains. |
| Over-prediction is conservative — why is it High? | IFRS 9 requires unbiased estimates (§5.5.17). Pricing overcharges, which is conduct risk. Wrong customers get line cuts. Conservatism is a capital concept with explicit MoC, not a licence for bias. |
| SEX is significant — why drop it? | Admissibility is legal, not statistical. Removing it cost about 0 Gini (DeLong p ≈ [x]). Then test proxies with AIR. |
| Why is rounding High? | It touches 100% of PDs and changes [x]% of decisions. The model in production is not the model validated. |
| What would you approve today? | Nothing for the intended uses. Possibly a next-month collections ranking, after F2/F4 fixes, with monitoring. |
| What tier? | Tier 1: financial reporting plus customer decisions. Simplicity of method doesn't lower materiality. |
| Developer: "We only had one month of outcome." | Then that is a limitation and a use restriction. It does not justify relabelling a one-month model as 12-month. |
| What would change with real bank data? | Out-of-time vintages, reject inference (if application), macro sensitivity for IFRS 9, override analysis, implementation UAT evidence. |

**Résumé line (personal project — say so):**
"Independent validation of a credit-card PD model (personal project, public UCI data, Python): replicated the model and
raised 13 findings, including a target–use mismatch, miscalibration from uncorrected undersampling (A/E [x]),
protected-attribute use and a production rounding defect affecting [x]% of decisions. Built WoE-LR and monotonic-GBM
challengers (DeLong-tested) and wrote a committee-style report."

---

## 7. TODO solutions

```python
def undocumented_codes(df):
    parts = []
    for col, codes in DOCUMENTED_CODES.items():
        off = df.loc[~df[col].isin(codes)]
        if off.empty:
            continue
        g = off.groupby(col)[TARGET].agg(n="size", bad_rate="mean")
        g["share"] = g["n"] / len(df)
        g.index = pd.MultiIndex.from_product([[col], g.index], names=["variable", "code"])
        parts.append(g[["n", "share", "bad_rate"]])
    return pd.concat(parts)


def prior_correct(pd_sample, sample_bad_rate, population_bad_rate):
    p = np.clip(pd_sample, 1e-12, 1 - 1e-12)
    offset = np.log(sample_bad_rate / (1 - sample_bad_rate) * (1 - population_bad_rate) / population_bad_rate)
    return 1 / (1 + np.exp(-(np.log(p / (1 - p)) - offset)))


def sensitivity_scenarios(df):
    s1 = df.copy()
    m = s1["PAY_0"] >= 0
    s1.loc[m, "PAY_0"] = (s1.loc[m, "PAY_0"] + 1).clip(upper=8)
    s2 = df.copy(); s2[BILL] = s2[BILL] * 1.10
    s3 = df.copy(); s3[PAYAMT] = s3[PAYAMT] * 0.50
    return {"PAY_0 +1 month": s1, "BILL_AMT +10%": s2, "PAY_AMT −50%": s3}


def adverse_impact_ratio(favourable, group, protected, reference):
    fav = pd.Series(np.asarray(favourable, dtype=float), index=group.index)
    return float(fav[group == protected].mean() / fav[group == reference].mean())


def parallel_run_summary(y, dev_pd, prod_pd, tol=1e-6, cut_off=dm.CUT_OFF):
    d = np.abs(dev_pd - prod_pd)
    fd, fp = dev_pd >= cut_off, prod_pd >= cut_off
    return pd.Series({"n": len(y), "pct_mismatch": (d > tol).mean(), "max_abs_diff": d.max(),
                      "mean_pd_dev": dev_pd.mean(), "mean_pd_prod": prod_pd.mean(),
                      "gini_dev": vt.gini_score(y, dev_pd), "gini_prod": vt.gini_score(y, prod_pd),
                      "flag_rate_dev": fd.mean(), "flag_rate_prod": fp.mean(), "pct_flag_changed": (fd != fp).mean()})


def write_monitoring_plan():
    rows = [
        ("Score PSI (vs development)", "Monthly", "< 0.10", "0.10–0.25", "> 0.25", "CSI root cause; assess recalibration", "1LoD monitoring"),
        ("CSI — PAY_0, utilisation, limit", "Monthly", "< 0.10", "0.10–0.25", "> 0.25", "Investigate drivers; data checks", "1LoD monitoring"),
        ("Gini (12m outcome) with 95% CI", "Quarterly", "drop < 10% rel.", "10–20%", "> 20% or CI excludes dev", "Root cause; redevelopment assessment", "1LoD; 2LoD review"),
        ("Calibration A/E + Jeffreys by grade", "Quarterly", "A/E 0.9–1.1, all grades green", "any amber", "any red / A/E outside 0.8–1.25", "Overlay; recalibrate", "1LoD; MRM approval of overlay"),
        ("Flag rate at cut-off", "Monthly", "within ±2pp of plan", "±2–5pp", "> ±5pp", "Review cut-off and strategy", "Business owner"),
        ("Overrides (count, bad rate)", "Monthly", "< 5%", "5–10%", "> 10%", "Override governance review", "Credit policy"),
        ("Data quality (missing, undocumented codes, volumes)", "Each run", "0 breaks", "minor", "any critical", "Stop-the-line; fix feed", "Data owner"),
        ("Fairness — AIR at cut-off (sex, age 62+)", "Quarterly", "≥ 0.90", "0.80–0.90", "< 0.80", "Fair-lending review; less discriminatory alternative search", "Compliance + MRM"),
    ]
    return pd.DataFrame(rows, columns=["metric", "frequency", "green", "amber", "red", "action_if_red", "owner"])
```
Thresholds above are common conventions **[Assumption — bank-specific]**. In your report, justify each one: a sampling
argument for Gini and A/E, materiality for flag rate, the regulatory heuristic for AIR.
