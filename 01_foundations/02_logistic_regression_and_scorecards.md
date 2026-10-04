# 01.2 · Logistic Regression & Scorecards — end to end

> **Most-asked technical question at every level:** "Walk me through building an application scorecard." The answer in §7 is your script. Everything else in this file is the follow-up ammunition.

---

## §1. Why logistic regression for PD
- Binary target (default / no default) → need a probability bounded in [0, 1].
- **Interpretable & stable:** each coefficient is a log-odds effect; regulators and business understand it; easy to implement and monitor.
- Works naturally with **WoE-binned** variables → monotonic, explainable points.
- Downsides: additive (misses interactions unless engineered), assumes linearity in the logit (handled by binning).

**Why not linear regression?** Predictions can fall outside [0,1]; errors are heteroskedastic and non-normal for a binary y; the effect of x on probability isn't constant.

---

## §2. The math in five lines
```
odds        = p / (1 − p)                      (p = 0.2 → odds 0.25, i.e., 1:4)
log-odds    = ln(p / (1 − p)) = β0 + β1·x1 + … + βk·xk = z
probability = p = 1 / (1 + e^(−z))             (the sigmoid)
odds ratio  = e^β  → +1 unit of x multiplies the odds by e^β
```
*Example:* β(utilisation, per 10 pts) = 0.18 → e^0.18 = 1.20 → each +10 pts of utilisation raises the **odds** of default by 20% (not the probability by 20%).

---

## §3. Estimation
- **Maximum likelihood:** maximise Σ[y·ln p + (1 − y)·ln(1 − p)]; solved iteratively (Newton–Raphson / IRLS).
- **Convergence problems:** (quasi-)complete separation — a variable/bin perfectly predicts outcome (e.g., a bin with zero bads) → coefficients explode. Fix: merge bins, Firth penalised regression, or drop the variable.

---

## §4. Assumptions — and the non-assumptions (common trap)
**Required:** binary outcome · independent observations (one record per account per observation point) · **linearity of the logit** in each predictor (binning/WoE solves) · no severe multicollinearity · enough events (heuristic: ≥ 10–20 bads per parameter) **[Assumption — rule of thumb]** · no overly influential outliers.

**NOT required:** normally distributed errors · homoskedasticity · a linear relationship between x and the *probability*.

---

## §5. Fit and significance
| Measure | What it tells you |
|---|---|
| Wald χ² per coefficient | Is β ≠ 0? |
| Likelihood-ratio test | Does adding a set of variables improve fit? (Δ deviance ~ χ²) |
| −2LL, AIC, BIC | Model comparison (lower = better) |
| McFadden pseudo-R² | 1 − lnL(model)/lnL(null); values 0.2–0.4 are already good |
| c-statistic (= AUC) and Somers' D (= Gini) | Discrimination (SAS "Association" table) |
| Hosmer–Lemeshow | Calibration |

---

## §6. Scorecard types
| Type | Population | Typical inputs | Performance window | Use |
|---|---|---|---|---|
| **Application** | Applicants (through-the-door) | Bureau, application, vendor scores (e.g., SBSS) | 12–24 months | Approve/decline, limit, price |
| **Behavioural** | Existing accounts | Payment history, utilisation, balances, delinquency trends | 6–12 months | Line management, cross-sell, early warning, IFRS 9 PD input |
| **Collections** | Delinquent accounts | Roll history, contact data | 1–6 months | Prioritise collection effort |
| **Fraud** | Transactions/applications | Velocity, device, mismatch signals | Days–weeks | Block/review |

---

## §7. Building an application scorecard — the 13-step script

1. **Objective & scope** — product (e.g., business credit card), segment, decision it supports, regulatory uses.
2. **Data & sample design**
   - **Observation point** (application date) and **performance window** chosen from a **vintage analysis**: cumulative bad rate by months-on-book flattens ("matures") — e.g., 12–18 months for cards, longer for loans.
   - **Bad definition** chosen with **roll-rate analysis**: the delinquency level from which most accounts don't cure (e.g., 90+ DPD ever in the window, or charge-off/bankruptcy).
   - **Indeterminates** (e.g., worst status 30–59 DPD) excluded from development to sharpen separation; **exclusions** (fraud, deceased, staff, VIP, policy declines) documented with counts.
3. **Sampling** — development / in-time holdout / out-of-time; stratify by vintage/segment; oversample bads if rare (fix later — §11).
4. **Data preparation** — missing values (keep as own bin), outliers (cap), derived variables (ratios, trends, utilisation), data-quality checks.
5. **Fine classing** (10–20 bins) → **coarse classing** (4–8 bins): monotonic bad rate/WoE where business logic expects it, each bin ≥ ~5% of the population with enough bads.
6. **WoE & IV** per variable; screen weak variables (IV < 0.02–0.1), flag "too good" ones (IV > 0.5: check leakage — e.g., data captured after the observation point).
7. **Multivariate selection** — correlation/VIF, variable clustering (PROC VARCLUS), stepwise/backward elimination **plus business review**; check signs; target ~8–15 characteristics.
8. **Reject inference** (application only) — §10.
9. **Final logistic regression** on WoE variables; check significance, signs, stability across samples.
10. **Scaling** to points (PDO) — §9.
11. **Validation by the developer** — holdout & OOT KS/Gini, rank-ordering, calibration, stability; segment checks.
12. **Cut-off strategy** — approval rate vs bad rate trade-off, **swap-set analysis** (swap-ins/swap-outs vs old score), profitability, override policy.
13. **Documentation, independent validation (MRM), implementation testing, monitoring plan.**

> Deliver this in ~3 minutes, then stop and let them pick a step to drill into.

---

## §8. WoE & IV — deep dive
```
WoE_bin = ln( %Good_bin / %Bad_bin )            (Siddiqi convention: higher WoE = safer)
IV      = Σ_bins (%Good_bin − %Bad_bin) × WoE_bin
```
**IV guide:** < 0.02 useless · 0.02–0.1 weak · 0.1–0.3 medium · 0.3–0.5 strong · > 0.5 "suspicious" (check for leakage — but strong bureau/vendor scores often legitimately exceed 0.5; in the demo the SBSS-like score has IV ≈ 0.9).

**Why WoE:** linearises the relationship with log-odds · handles missing values and outliers as bins · puts all variables on one scale · produces monotonic, explainable points · makes implementation simple.

**Costs:** loses within-bin information · results depend on binning choices · IV inflates with more bins and small bins (overfitting) · can't extrapolate beyond observed ranges · WoE must be fixed from development data (monitor bins that become empty or new categories).

**Sign trap (asked a lot):**
- With WoE = ln(%G/%B) and a model predicting **bad**, a **single-variable** WoE logistic regression has coefficient **exactly −1** (and intercept = overall log-odds of bad).
- In a multivariate model, coefficients move away from −1 because of correlation between variables.
- A **positive** coefficient (wrong sign) means multicollinearity/suppression → remove or recombine the variable.
- If your team defines WoE = ln(%B/%G), all of this flips sign (≈ +1). **State your convention first.**

---

## §9. Scaling: from log-odds to points (PDO)
```
Score       = Offset + Factor × ln(odds_good)
Factor      = PDO / ln(2)
Offset      = BaseScore − Factor × ln(BaseOdds)
Points_ij   = −(β_i × WoE_ij + β0/n) × Factor + Offset/n     (model predicts log-odds of BAD; n = # variables)
```
**Worked example (verified):** 600 points at 50:1 good:bad odds, PDO = 20 → **Factor = 28.85, Offset = 487.12**.
PD 2% → score ≈ **599** · PD 5% → **572** · PD 10% → **551**. Every 20 points doubles the good:bad odds.

**Missing values:** score them via the MISSING bin's WoE (never default to 0 points silently — a classic implementation finding).

---

## §10. Reject inference
**Problem:** you only observe performance for *approved* applicants; the model will score the whole *through-the-door* population → selection bias, especially near/below the cut-off.

| Method | How | Watch-outs |
|---|---|---|
| Hard cut-off / simple augmentation | Score rejects with the accepts model; label below a threshold as bad | Arbitrary threshold |
| **Parcelling** | Within score bands, assign rejects good/bad in proportion to (often inflated) accepted bad rates | Inflation factor is judgmental |
| **Fuzzy augmentation** | Each reject enters twice (good & bad) weighted by p(good)/p(bad) | Relies on the accepts model being right |
| Re-weighting | Weight accepts by 1/P(accept) in their band | Fails where acceptance ≈ 0 |
| **External performance (bureau)** | Use rejects' performance on credit obtained elsewhere | Best empirical evidence; product mismatch |
| Below-cut-off test approvals | Approve a random sample of would-be rejects | Gold standard; costly |

**Validator's angle:** test the **sensitivity** of the final model and cut-off to the reject-inference choice; it's an assumption, not a fact.

---

## §11. Calibration & oversampling correction
- If bads were oversampled (sample bad rate ρ₁ vs true π₁), correct the intercept (prior correction):
  `β0_true = β0_sample + ln(π₁/π₀) − ln(ρ₁/ρ₀)`  (π₀ = 1 − π₁, ρ₀ = 1 − ρ₁), or use sampling weights.
- **Score-to-PD mapping** for downstream uses: logistic calibration on a recent window, isotonic regression, or binning to grades.
- **Calibration target depends on use:** business decisioning (recent PIT), IFRS 9 (PIT + forward-looking), IRB (long-run average default rate + MoC). The same score can feed different calibrations.

---

## §12. Segmentation
- **Why:** different populations behave differently (new-to-credit vs established; BCC vs term loans; thin vs thick bureau files).
- **How:** business logic first; supported by trees/CHAID on the target.
- **Test:** does the segmented solution beat a single model by enough (Gini uplift in each segment, stability, enough bads per segment) to justify extra models to maintain? Validators ask for this evidence.

---

## §13. Interview traps (one-line answers)
1. *Can a variable with IV 0.01 be in the model?* Rarely justified; maybe for business/policy reasons, documented.
2. *Your coefficient is positive with WoE — why?* Multicollinearity/suppressor effect or a binning issue.
3. *Why exclude indeterminates?* Sharper good/bad separation; but score them later to check behaviour.
4. *Why not use the whole history as the performance window?* Unequal exposure time across accounts; use a fixed window from a maturity analysis.
5. *How many variables?* Enough to be stable and explainable — typically 8–15.
6. *What if a bin has zero bads?* Merge bins (or apply a smoothing constant) — otherwise WoE is infinite and MLE may not converge.
7. *How do you choose PDO and base?* Business convention/continuity with the old scorecard; doesn't affect ranking.
8. *Stepwise selection — good or bad?* Fast, but unstable and ignores business sense; use it as a screening aid with manual review.
9. *Why OOT and not just holdout?* Holdout tests sampling noise; OOT tests time stability — the real use case.
10. *Behavioural vs application score in IFRS 9?* Behavioural scores are usually better PIT PD drivers for existing accounts.
