# 02 · Interview Process Map — First Call to Offer

Goal: know **what each round is really testing**, so every answer is aimed at the scorer, not the question.

---

## 1. The typical loop for AVP/VP/Lead validation roles (India GCCs)

| Stage | Format | Duration | What they're really scoring | Kill-shots to avoid |
|---|---|---|---|---|
| 0. Recruiter / HR screen | Phone/Teams | 15–30 min | Fit to band, notice period, CTC expectation, communication | Rambling intro; quoting a number with no anchor; "just looking for growth" |
| 1. Online assessment *(some firms)* | HackerRank / Codility / Mettl / HireVue | 45–90 min | Python/SQL basics, stats MCQs, probability; HireVue = structured video answers | Freezing on pandas groupby; not practising timed |
| 2. Technical 1 — stats & modeling | Live | 45–60 min | LR, scorecards, metrics, tests, ML basics — **can you explain from first principles?** | Formula without intuition; can't say *why* |
| 3. Technical 2 — domain & validation case | Live | 45–75 min | **Your projects under pressure** + IFRS 9 / IRB / stress testing + "validate this model" | Over-claiming; not knowing your model's numbers |
| 4. Coding / exercise *(some firms)* | Live share-screen or take-home (1–3 days) | 30–90 min or take-home | Compute KS/PSI/Gini, write SQL, critique code, or validate a dataset and write findings | Untidy code; no commentary; no findings |
| 5. Hiring manager / Director | Live | 45–60 min | Judgment, independence, findings severity, stakeholder pushback, SR 11-7/SR 26-2 | Being a "metric runner"; caving under pushback |
| 6. Senior leader / global counterpart | Live (often US/UK hours) | 30–45 min | Big picture, communication to non-technical seniors, culture | Jargon; no opinion |
| 7. HR final + offer | Phone | 20–30 min | Compensation close, joining date | Accepting first number; misstatement of CTC (BGV risk) |

**Pareto of interview time** (my estimate across the loop) **[Assumption]**:

```
Your own projects (deep-dive + grilling)      ██████████████  30%
Metrics + LR/scorecards fundamentals          █████████       20%
Validation framework + findings + challenge   ███████         15%
IFRS 9/CECL + IRB + stress testing            ███████         15%
MRM governance + regulation                   ████             8%
Coding (Python/SQL/SAS)                       ███              7%
Behavioral / motivation                       ██               5%
```
→ Your own projects + metrics + validation framework ≈ **65% of the score**. Prep accordingly.

---

## 2. Stage-by-stage playbook

### Stage 0 — Recruiter screen
**Questions:** Tell me about yourself · Why are you looking to change? · Current CTC / expected CTC · Notice period · Are you open to [location]? · Which models have you worked on?

**How to pass**
- 60-second pitch (template in `04_positioning_resume_and_stories.md`). Lead with **model types + regulatory context + scope**, end with **why validation**.
- CTC: state current CTC factually (BGV will verify). For expected, anchor to the **role band**, not your current pay:
  > "I'm targeting the Lead/VP band for this scope — in the range of 40–45 fixed. I'm flexible on structure if the role and level are right."
- Notice: state it, and say whether buy-out/early release is possible.
- Ask: *"What level is this role graded at, and what does the interview loop look like?"* → tells you whether to push for a higher grade early.

### Stage 1 — Online assessment (where used)
**Likely at:** Goldman Sachs (HackerRank: math/stats/coding), JPMorgan (HireVue for some roles), AmEx (SQL/analytics test), some Wells Fargo/Citi roles. **[Likely — based on candidate reports; varies by team]**

**Content seen in this space:** pandas groupby/merge/pivot; computing KS/AUC/PSI; SQL joins + window functions; probability (Bayes, expected value, conditional probability); distributions; hypothesis tests; LR interpretation.
→ Drill with `05_coding/` timed sets (45 min each).

### Stage 2 — Technical 1 (stats & modeling)
**Top questions (from `06_interview_bank/01_question_bank_tier1.md`):**
1. Walk me through building an application scorecard end-to-end.
2. Why logistic regression for PD? Assumptions? Why not linear regression?
3. WoE and IV — formula, interpretation, thresholds, why WoE?
4. KS vs Gini vs AUC — definitions, relationship (Gini = 2·AUC − 1), typical values.
5. PSI — formula, thresholds, what you do at 0.27.
6. Multicollinearity — detection (VIF, correlation), impact, fixes.
7. Reject inference — why, methods, limitations.
8. Overfitting — how you detect it (train vs OOT gap), how you prevent it.
9. Calibration vs discrimination — difference; tests for each.
10. When would you use XGBoost over LR? How do you explain it (SHAP)?

**How to pass:** answer in the **"definition → intuition → formula → when it breaks"** order. Example on PSI: *"PSI measures distribution shift between a reference and a current population; it's the sum over bins of (A−E)·ln(A/E); <0.1 stable, 0.1–0.25 monitor, >0.25 investigate; it breaks with tiny bins or empty bins, and it doesn't tell you whether performance changed — you pair it with KS/Gini and calibration."*

### Stage 3 — Technical 2 (domain + validation case) — the round that decides the level
**Format:** 20–30 minutes on *your* projects, then a case: *"Here's a PD model with Gini 0.62 in dev and 0.48 now, PSI 0.18. Validate it / what would you do?"*

**What VP-bar looks like:**
- You know **your model's numbers** (sample sizes, bad rates, Gini/KS, PSI history, thresholds, the last breach and what happened).
- You separate **population drift** from **performance deterioration** from **calibration drift**.
- You propose **actions with governance** (monitor → overlay → recalibrate → redevelop → restrict use), and you say **who decides**.
- You raise **findings with severity** without being asked.

### Stage 4 — Coding / exercise
**Live:** "Here's a dataframe with `score`, `bad_flag`. Compute KS and Gini." / "Bin this variable and compute IV." / "Write SQL for 30+ DPD roll rates by month."
**Take-home (common in fintech/consulting; occasional at banks):** dataset + "validate this model, write a 2-page memo."
**How to pass:** narrate as you code; use functions; check edge cases (empty bins, ties); end with **interpretation and a finding**, not just a number.

### Stage 5 — Hiring manager (judgment + independence)
**Top questions:**
- "The model owner disagrees with your High-severity finding and the business wants to go live Monday. What do you do?"
- "How do you decide validation scope for a Tier 2 vs Tier 1 model?"
- "What changed from SR 11-7 to SR 26-2? What would you change in our MRM framework?"
- "How do you validate a vendor model when the vendor won't share code?" (← your SBSS experience)
- "Tell me about a time you found an error that others missed."
**How to pass:** structured, calm, evidence-first. Show **independence without hostility**: *"I don't negotiate on evidence; I'm flexible on remediation path and timeline — e.g., approve with conditions plus an overlay and a 90-day remediation."*

### Stage 6 — Senior leader
Explain one of your models to a non-technical MD in 2 minutes. Opinion questions: *"Biggest model risk in retail lending in 2027?"* (good answers: post-pandemic data distortions in macro-models, ML/AI explainability and fairness, data drift from new products/channels, ECL transition in India, GenAI governance gap given SR 26-2 excludes it.)

### Stage 7 — HR final & negotiation
See `06_interview_bank/04_behavioral_hr_negotiation.md`. Core rules: never accept on the call; ask for written breakup; negotiate **level first, fixed second, joining bonus third**; use competing offers truthfully.

---

## 3. Company patterns (to calibrate prep; verify with the recruiter)

| Firm | Pattern | Confidence |
|---|---|---|
| **Wells Fargo** (QAS ladders, CMoR) | Technical-heavy; project deep-dives; replication/benchmarking mindset; ML increasingly; regulator/audit-facing behaviours | Likely |
| **American Express** | Analytics/SQL test; business case; "How does Amex make money?"; product/credit-policy sense; modeling depth for Band 40 | Likely (candidate reports) |
| **Citi** | MRM is large and regulatory-driven; expect validation process + documentation + regulatory questions; GenAI validation team exists | Likely |
| **JPMorgan (MRGR)** | Rigorous stats/math; CCAR/CECL context for credit; structured behavioral; HireVue for some roles | Likely |
| **Goldman Sachs / Morgan Stanley** | Online test (math/stats/coding); several technical rounds; probability puzzles possible | Likely |
| **Barclays / HSBC / StanChart / DB / UBS / SocGen** | IRB + IFRS 9 depth; PRA SS1/23 (UK) or ECB guide (EU) awareness; 2–3 technical + manager | Likely |
| **Big 4 (FRM practices)** | Case + client communication; IFRS 9 / ECL heavy (RBI ECL 2027 is a big India pipeline); lighter coding | Likely |
| **Fintech lenders** | Python/ML take-home; feature engineering; deployment/monitoring | Likely |

---

## 4. Universal answer frameworks (use everywhere)

**A. Technical concept — DIFW:** Definition → Intuition → Formula → Where it breaks (+ what you'd pair it with).

**B. Validation case — 6-step "SCOPE-D":**
1. **S**ituate: purpose, use, tier, portfolio, regulatory use.
2. **C**heck data: lineage, quality, representativeness, default definition.
3. **O**utcomes: discrimination, calibration, stability — vs thresholds and vs development.
4. **P**robe concept: methodology, assumptions, segmentation, variables, expert judgment.
5. **E**xamine alternatives: benchmark/challenger, sensitivity, implementation.
6. **D**ecide: findings with severity → validation outcome (approve / approve with conditions / reject) → monitoring + remediation.

**C. Behavioral — STAR-L:** Situation, Task, Action (what *you* did), Result (number), **Learning** (what you'd do differently). VP-bar answers always include the L.

**D. "I don't know" protocol:** *"I haven't done X directly. Here's how I'd reason about it…, and here's the closest thing I've done…"* — never bluff; interviewers in this niche drill until they find the edge.
