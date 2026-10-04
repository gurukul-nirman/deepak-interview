# 03.1 · Performance Monitoring Metrics — definition → intuition → formula → when it breaks

> This is your home turf, which is exactly why it gets grilled hardest. At VP bar, knowing the formula is table stakes; what scores is **diagnosis** (§6) and **what you'd do next** (§7).

All numbers in worked examples are verified in Python (`05_coding/code/`).

---

## 0. The four questions every monitoring pack must answer

| Question | Metric family | Typical metrics |
|---|---|---|
| 1. Is the population still the one the model was built on? | **Stability** | PSI (score), CSI (characteristics), characteristic analysis, mix shift, missing rates |
| 2. Does the model still separate goods from bads? | **Discrimination** | KS, Gini/AR, AUC, rank-ordering, capture rate, lift |
| 3. Are the predicted *levels* right? | **Calibration / accuracy** | Actual-vs-expected (A/E), binomial, Jeffreys, Hosmer–Lemeshow, Brier, LGD/EAD back-tests |
| 4. Is it being used as designed? | **Usage / operational** | Override rates & performance, policy-rule hits, overlays, exceptions, data-quality KRIs |

> **Interview line:** "Discrimination tells me the model ranks correctly; calibration tells me the numbers are right; stability tells me whether I'm even looking at the same population. I never conclude from one family alone."

---

## 1. Discrimination

### 1.1 KS (Kolmogorov–Smirnov)
- **Definition:** maximum vertical distance between the cumulative distributions of goods and bads across the score.
- **Formula:** `KS = max_s | F_bad(s) − F_good(s) |` (sort riskiest first; cumulative % of bads − cumulative % of goods).
- **Intuition:** the best single cutoff's separation. 0 = no separation, 1 (100) = perfect.
- **Worked example (verify by hand):**

| Band (riskiest first) | Goods | Bads | Cum % bads | Cum % goods | Difference |
|---|---|---|---|---|---|
| 1 | 50 | 30 | 30% | 5% | 25 |
| 2 | 100 | 25 | 55% | 15% | **40** |
| 3 | 200 | 20 | 75% | 35% | **40** |
| 4 | 300 | 15 | 90% | 65% | 25 |
| 5 | 350 | 10 | 100% | 100% | 0 |
| **Total** | 1000 | 100 | | | **KS = 40** |

- **Where it breaks:** depends on binning if computed on deciles (compute on raw scores where possible); sensitive to a single point; doesn't use the whole curve; says nothing about calibration.
- **Rules of thumb [Assumption — bank thresholds vary]:** application scorecards often 30–50; behavioural scorecards often 45–65+.

### 1.2 ROC, AUC, Gini, Accuracy Ratio
- **AUC:** probability that a randomly chosen bad gets a riskier score than a randomly chosen good (ties count ½). Equivalent to the Mann–Whitney U statistic.
- **Gini = 2·AUC − 1** = Accuracy Ratio (from the CAP curve) = Somers' D (shown in SAS PROC LOGISTIC).
- **Worked example (same table):** ROC points (cum % goods, cum % bads) = (0,0), (.05,.30), (.15,.55), (.35,.75), (.65,.90), (1,1) → trapezoid area **AUC = 0.76 → Gini = 0.52**.
- **CAP curve:** x = cumulative % of *all* accounts, y = cumulative % of bads. AR = area between model and random ÷ area between perfect and random. Numerically equals Gini.
- **Where it breaks:**
  - **Truncation/selection:** if only applicants above a cutoff are booked, the observed range is narrower → Gini falls mechanically even if the model is fine. *(VP-level point.)*
  - **Mix:** Gini isn't comparable across portfolios with very different bad rates or homogeneity.
  - **Noise:** small bad counts → wide confidence intervals. Use **bootstrap CIs** or **DeLong's test** before calling a drop real.
- **Statistical test for a change:** DeLong (two correlated AUCs on the same sample — champion vs challenger); for dev vs current (independent samples): compare with bootstrap CIs or a z-test on the AUC difference using each AUC's standard error.

### 1.3 Rank-ordering, capture, lift
- **Rank-ordering:** bad rate should increase monotonically from safest to riskiest band. Count "breaks". One small break in the middle with low volume is usually noise; breaks at the tails matter (that's where cutoffs sit).
- **Capture rate:** % of all bads in the riskiest 10% / 20%.
- **Lift:** band bad rate ÷ overall bad rate.

---

## 2. Calibration / accuracy

### 2.1 Calibration in the large vs calibration slope
- **In the large:** overall actual-vs-expected (A/E = observed default rate ÷ average PD).
- **Slope:** are low-PD bands under-predicted and high-PD bands over-predicted (slope flattening → discrimination has weakened) or vice versa?
- Always show **predicted vs observed by decile/grade** — a single A/E ratio hides offsetting errors.
  *In the demo (`demo_output.txt`), overall A/E is only 1.07 but grades G2–G4 fail the Jeffreys test — a classic flattening pattern.*

### 2.2 Tests (know which is which)
| Test | H0 / mechanics | Use | Caveats |
|---|---|---|---|
| **Binomial (one-sided)** | H0: PD is correct; p = P(X ≥ D \| N, PD) | Per grade PD back-test | Assumes independent defaults → **too strict** when defaults are correlated; Vasicek-adjusted version widens the interval |
| **Normal approximation** | z = (DR − PD)/√(PD(1−PD)/N) | Quick check, large N | Poor for small N·PD |
| **Jeffreys** | Posterior Beta(D+½, N−D+½); p = BetaCDF(PD) | ECB IRB validation reporting per grade | Same independence caveat; one-sided (under-estimation) |
| **Hosmer–Lemeshow** | Σ_g (O_g − E_g)² / (n_g p̄_g(1 − p̄_g)) ~ χ²(g−2) | Overall calibration of a logistic PD | Rejects almost always on very large samples; bin-dependent |
| **Chi-square across grades** | Σ (O−E)²/E-type statistic | Multi-grade calibration | Needs enough expected defaults per cell |
| **Brier score** | mean (PD − y)² | Overall accuracy (calibration + discrimination) | Scale depends on bad rate; compare like with like |
| **Traffic-light approach** | Green/Amber/Red bands from confidence levels (e.g., 95% / 99%) | Regulatory-style reporting | Choose levels in policy, not after seeing results |

**Worked binomial example:** grade PD = 2%, N = 1,000 accounts, D = 30 defaults (expected 20).
- Exact binomial p = **0.021**, normal-approx p = **0.012**, Jeffreys p = **0.016** → reject "PD adequate" at 5% (Amber), not at 1%.
- At 5%, the **first rejecting default count is 29** — say this kind of thing to show you can reason about critical values.

### 2.3 Model-type specifics
- **PIT vs TTC:** a TTC (through-the-cycle) PD is *supposed* to deviate from realised default rates in booms and busts. Calibration tests on TTC models must be judged against the long-run average, not one year. (Common interview trap.)
- **LGD:** realised vs predicted LGD by segment (paired t-test), with cure/workout-period completeness considered (incomplete workouts bias realised LGD).
- **EAD/CCF:** realised vs predicted CCF for revolving products (12 months before default → default date).
- **Low-default portfolios:** confidence intervals, pooling years, Pluto–Tasche upper bounds, benchmarking to external ratings.

---

## 3. Stability

### 3.1 PSI (Population Stability Index)
- **Formula:** `PSI = Σ_i (A_i − E_i) · ln(A_i / E_i)` with A = actual (current) %, E = expected (reference) % per bin.
- **Intuition:** symmetric Kullback–Leibler divergence (KL(A‖E) + KL(E‖A)) between two distributions.
- **Thresholds (industry convention):** **< 0.10 stable · 0.10–0.25 monitor/investigate · > 0.25 significant shift**.
- **Worked example:** E = 20/20/20/20/20%, A = 30/25/20/15/10% → contributions 0.0406 + 0.0112 + 0 + 0.0144 + 0.0693 = **PSI 0.135 (Amber)**.
- **Where it breaks:**
  - Bins must come from the **reference** sample; recompute edges on the current sample = bug.
  - Empty bins → infinite contribution → floor at ε and *report it*.
  - Bin count changes the value (10 vs 20 bins).
  - **Small samples inflate PSI** through noise alone.
  - **PSI is not a performance metric.** High PSI with stable Gini and calibration may need no model action.

### 3.2 CSI and characteristic analysis
- **CSI:** same formula applied to each characteristic's bins → tells you *which* variables moved.
- **Characteristic analysis (score-points view):** `Index_var = Σ_attributes (A% − E%) × points_attribute` = how many points the average score moved because of that characteristic.
  *Example:* utilisation points [115, 107, 98, 91, 72], E = 20% each, A = 12/15/20/23/30% → **−4.6 points** → utilisation alone moved the average score down ~4.6 points.
- **Prioritise:** a RED CSI on a low-IV variable matters less than an AMBER CSI on the dominant variable.

### 3.3 Other stability signals
Score mean/median shift · approval rate and volume trends · channel/product/segment mix · missing-value rates and out-of-range values · default-definition or data-source changes (often the real culprit).

---

## 4. Usage / operational monitoring
- **Overrides:** high-side (declined despite passing score) and low-side (approved despite failing) rates — and their *performance*. Rising low-side overrides with high bad rates = a governance finding.
- **Policy-rule hits** and their interaction with the score.
- **Overlays / post-model adjustments:** size, trigger, sunset date, whether still justified.
- **Exceptions:** model used outside intended scope (new product, new channel) → model-use finding.

---

## 5. Example RAG framework *(illustrative — every bank sets its own in MRM policy)*

| Metric | Green | Amber | Red |
|---|---|---|---|
| Score PSI | < 0.10 | 0.10–0.25 | > 0.25 |
| CSI (key variables) | < 0.10 | 0.10–0.25 | > 0.25 |
| Gini relative drop vs development | < 10% | 10–20% | > 20% |
| KS absolute drop | < 5 pts | 5–10 pts | > 10 pts |
| A/E ratio (portfolio) | 0.9–1.1 | 0.8–0.9 or 1.1–1.25 | < 0.8 or > 1.25 |
| Grades failing calibration test (95%) | 0 | 1–2 | ≥ 3 or any at 99% |
| Missing rate of key input | < 2% | 2–5% | > 5% |

**Escalation:** Amber → investigate & document within the cycle; Red → notify model owner + MRM, root-cause within N days, consider overlay/restriction; repeated Red → trigger revalidation/redevelopment.

---

## 6. Diagnosis matrix — the answer to "Metric X breached, what do you do?"

| PSI | Discrimination (KS/Gini) | Calibration | Most likely story | What you do |
|---|---|---|---|---|
| Low | Stable | OK | Healthy | Continue; document |
| **High** | Stable | OK | Population moved, relationship intact (e.g., new channel, marketing) | Confirm with business; check segments; update reference period if the change is intended |
| **High** | Stable | **Off** | Population moved → level shift in risk | Recalibrate intercept / overlay; monitor monthly |
| Low | **Drop** | OK/Off | Relationship change (concept drift), data issue, policy truncation | Data checks first; characteristic-level drill-down; redevelopment assessment |
| **High** | **Drop** | **Off** | Both drift types | Escalate; interim overlay; redevelopment; restrict use if material |
| Low | Stable | **Off (level only)** | Macro/cycle (PIT model) or default-definition change | Confirm definition; recalibrate or apply macro overlay (IFRS 9: check FLI) |
| Any | Drop only in one segment | — | Segment-specific issue (e.g., BCC vs non-BCC) | Segment-level remediation; consider segmentation change |

**Always rule out data first:** a broken feed, a changed bureau attribute definition, or a default-flag change produces every pattern above.

---

## 7. Root-cause playbook (say these steps in order)
1. **Data integrity:** volumes, missing rates, out-of-range, reconciliation to source, definition changes.
2. **Decompose:** by segment, channel, product, vintage, geography.
3. **Characteristics:** CSI + characteristic analysis → which inputs drove the shift; WoE/bad-rate pattern still monotonic?
4. **Strategy/policy:** cutoff changes, credit-line policy, marketing campaigns, collections changes.
5. **External:** macro (rates, unemployment), regulation (e.g., SBA's SBSS change from 1 Mar 2026), competitor actions.
6. **Quantify impact:** on losses/ECL/capital/approval rates → drives severity.
7. **Recommend with governance:** monitor → overlay → recalibrate → redevelop → restrict/retire; owner, due date, re-test plan.

---

## 8. Model-type monitoring checklists

**Application scorecard:** PSI/CSI on through-the-door population · KS/Gini on booked accounts at maturity (+ early-read at 6/9 months) · reject-inference sensitivity · override monitoring · approval-rate trend.

**Behavioural scorecard:** monthly score stability · roll-rate alignment with score bands · KS/Gini at 12-month horizon · line-management strategy outcomes.

**Vendor score (e.g., FICO SBSS):** local discrimination & bad-rate-by-band vs vendor odds chart · stability · segment performance (BCC vs non-BCC, young businesses, thin files) · version-change impact analysis · vendor documentation & change notices · use-case changes (SBA dropped SBSS screening for 7(a) small loans from 1 Mar 2026).

**IFRS 9 / CECL:** 12m PD back-test by stage/segment · lifetime PD term-structure back-test (cumulative curves by vintage) · LGD/EAD back-tests · staging: stage migration matrix, % of Stage 3 that came via Stage 2 (SICR effectiveness), time in Stage 2, cure rates · macro model performance with realised macro · overlay tracking · ECL movement attribution.

**IRB:** per grade binomial/Jeffreys; AUC current vs initial validation; migration matrix stability & concentration (HHI); override rates; LGD (realised vs estimated, t-test) and CCF back-tests; default-definition consistency; representativeness of current portfolio vs calibration sample.

**Stress-testing models:** annual performance assessment: re-estimate with new data, coefficient stability (rolling windows), out-of-time back-test using *realised* macro paths, sensitivity to each MEV, benchmark/challenger comparison, overlay review.

**ML models:** all of the above **plus** feature drift (PSI per feature), SHAP-importance drift, fairness metrics by protected-class proxies where lawful, retraining governance (what counts as a model change).

---

## 9. Rapid-fire (answer in ≤ 20 seconds each)
1. *Gini vs AUC?* Gini = 2·AUC − 1.
2. *KS 45 → 38: worry?* Check CI/bad count; 7 points is material if significant; diagnose before acting.
3. *PSI 0.27 but Gini stable?* Population shift, ranking intact → check calibration and business change; maybe no model action.
4. *Why might Gini fall after tightening cutoffs?* Truncation — booked population is more homogeneous.
5. *Calibration fine overall, failing in low grades?* Slope flattening → discrimination weakening → investigate drivers.
6. *Binomial test too strict?* Assumes independent defaults; correlated defaults widen the true interval.
7. *Which test does the ECB use for PD calibration reporting?* Jeffreys test per grade.
8. *PSI symmetric?* Yes — swapping A and E gives the same value.
9. *How many defaults do you need?* Enough for stable estimates — a common heuristic is ≥ 100–200 bads for development; for monitoring report CIs. **[Assumption — policy-dependent]**
10. *Monitoring frequency?* Risk-based: monthly/quarterly for material retail PD; annual for stress-test models; SR 26-2 explicitly ties cadence to materiality.
