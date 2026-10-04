# Credit Risk Model Validation & MRM — Interview Prep Kit (Oct–Nov 2026)

**Goal:** clear every round, first call to offer, for credit-risk **model validation / MRM / monitoring** roles paying **≥ ₹40L fixed** (India first; UAE/Singapore/UK in parallel).
**Profile:** 5 years of credit-risk performance monitoring at an analytics vendor (IFRS 9/CECL, Basel IRB, CCAR stress testing, FICO SBSS BCC/non-BCC, SmarterPay); SQL, SAS, some Python and Tableau.
**Constraints:** 6 weeks · ~15 hrs/week · Pareto-first · assumes no prior knowledge.

---

## 1. What the research says (bottom line)
1. **₹40L fixed at ~5 years is a top-decile outcome.** Typical AVP risk pay at large GCCs is ₹29–40L CTC; 40 fixed sits in VP-equivalent bands → target **AmEx Sr Manager (Band 40), Wells Fargo Lead QAS (JD floor 5 yrs), top-of-band Citi/JPM/GS, VP roles (stretch), fintech leads, or UAE**. → `00_strategy/01_market_reality_and_targets.md`
2. **SR 11-7 was replaced by SR 26-2 on 17 Apr 2026.** Most candidates still quote SR 11-7 as current. Knowing both is a cheap differentiator. → `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md`
3. **2026–27 regulatory wave = hiring demand:** RBI ECL (effective 1 Apr 2027), RBI draft MRM guidance (Jun 2026), OSFI E-23 (May 2027), EU AI Act credit scoring (Dec 2027), AI/ML validation teams.
4. **The interview is ~65% three things:** your own projects under grilling, monitoring metrics + scorecard fundamentals, and the validation framework (findings, severity, independence).
5. **Your edge:** breadth across provisioning, capital and stress models + a vendor model (SBSS). **Your gaps:** monitoring→validation framing, Python depth, possibly a Master's-degree screen on some quant titles.

---

## 2. Start here (today)
1. Read `00_strategy/01_market_reality_and_targets.md` and `00_strategy/02_interview_process_map.md` (40 min).
2. Open `00_strategy/03_six_week_plan.md` — it tells you exactly what to do each day.
3. Fill the project sheets in `00_strategy/04_positioning_resume_and_stories.md` — highest-ROI hour of the whole plan.
4. Update resume/LinkedIn and **apply to 10 roles this week** — don't wait until prep is "done".
5. Send me JDs as you find them → I'll build a tailored pack in `07_jd_analysis/`.

---

## 3. Pareto map — where interview points come from
| Share of interview time **[Assumption]** | Topic | Files |
|---|---|---|
| ~30% | **Your projects** (deep-dive + grilling) | `00_strategy/04_positioning_resume_and_stories.md` · `06_interview_bank/02_question_bank_tier2_grilling.md` (ladder I) |
| ~20% | **Metrics + LR/scorecards** | `03_monitoring_validation/01_performance_monitoring_metrics.md` · `01_foundations/02_logistic_regression_and_scorecards.md` |
| ~15% | **Validation framework + findings** | `03_monitoring_validation/02_independent_validation_playbook.md` · `06_interview_bank/03_case_studies.md` |
| ~15% | **IFRS 9/CECL, IRB, stress testing** | `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md`, `03_basel_irb.md`, `04_stress_testing_ccar.md` |
| ~8% | **Governance & regulation** | `04_governance_regulation/` |
| ~7% | **Coding** | `05_coding/` |
| ~5% | **Behavioural / HR** | `06_interview_bank/04_behavioral_hr_negotiation.md` |

---

## 4. Kit map
| Folder / file | What it is | Plan week |
|---|---|---|
| **00_strategy/** | | |
| `01_market_reality_and_targets.md` | Real 2026 pay data (India + abroad), target tiers, visa notes, risks | 1 |
| `02_interview_process_map.md` | Every round: what's scored, top questions, company patterns, answer frameworks | 1 |
| `03_six_week_plan.md` | Day-by-day plan, emergency 10-hour path, job-search track | 1 |
| `04_positioning_resume_and_stories.md` | Positioning, resume formula, 90-sec pitch, **project grilling sheets** | 1 |
| **01_foundations/** | Statistics from scratch · Logistic regression & scorecards · ML for credit risk | 1, 4 |
| **02_credit_risk/** | Fundamentals · IFRS 9/CECL/RBI ECL · Basel IRB · Stress testing (CCAR/ICAAP) | 3 |
| **03_monitoring_validation/** | Metrics (formulas, worked examples, diagnosis matrix) · Independent validation playbook (workstreams, findings, outcomes, pushback) | 2 |
| **04_governance_regulation/** | SR 11-7 → SR 26-2 · Global regs quick reference · AI/ML/GenAI model risk | 4 |
| **05_coding/** | Python (from zero, SAS↔pandas↔SQL Rosetta, exercises, timed sets) · SQL drills · SAS macros | 1–5 |
| `05_coding/code/` | **Tested** toolkit, end-to-end demo, stress-test diagnostics, SQL practice DB builder (+ saved outputs) | 1–5 |
| **06_interview_bank/** | Tier-1 Q&A (≈130) · Grilling ladders · 16 cases · Behavioural & negotiation · Mock scripts · Cheat sheet | 2–6 |
| **07_jd_analysis/** | JD → prep-pack process, template, keyword→file map | as JDs arrive |

**Run the code:** `pip install -r 05_coding/code/requirements.txt` then
`python 05_coding/code/validation_toolkit.py` · `python 05_coding/code/demo_end_to_end.py` · `python 05_coding/code/stress_test_diagnostics.py` · `python 05_coding/code/sql_practice.py`

---

## 5. Progress tracker
**Week 1** — [ ] targets list · [ ] stats §1–10 · [ ] scorecard script cold · [ ] Python basics + demo run · [ ] 5 project sheets · [ ] resume v2 · [ ] 10 applications
**Week 2** — [ ] KS/Gini/PSI by hand · [ ] diagnosis matrix · [ ] validation workstreams from memory · [ ] 3 findings written · [ ] own metrics code · [ ] SQL D1–D8 · [ ] 10 applications + 5 referrals
**Week 3** — [ ] fundamentals · [ ] IFRS 9/CECL/RBI ECL · [ ] IRB · [ ] stress testing · [ ] cases 1–5 · [ ] SAS PSI macro · [ ] **Mock 1** · [ ] 10 applications
**Week 4** — [ ] SR 26-2 2-min answer · [ ] global regs · [ ] ML + AI risk · [ ] cases 6–10 · [ ] timed coding sets 1–2 · [ ] **Mock 2** · [ ] 10 applications
**Week 5** — [ ] ladders A–L · [ ] cases 11–16 · [ ] 10 STAR-L stories · [ ] negotiation script + decision matrix · [ ] **Mock 3 (full loop)**
**Week 6** — [ ] Tier-1 cold recall ≥ 90% · [ ] dossiers for every live process · [ ] cheat sheet review

---

## 6. Open questions for you (answers will sharpen targeting)
1. **Education:** degree, field, college? (Wells Fargo/JPM/Citi quant titles list a Master's in a quantitative field as *required* — this decides which titles we prioritise.)
2. **SmarterPay models:** what do they predict and how are they used? (I'll build the grilling ladder.)
3. **BCC:** confirm it means *business credit card* (I've assumed so).
4. **Notice period** and buy-out policy at your current employer.
5. **Certifications** (FRM/CFA/CQF) — any in progress?
6. **Abroad:** should I build a UAE-specific pack (IFRS 9 + CBUAE model management standards) now?

---

## 7. How to use me alongside this kit
- **Mock interviews:** "Mock: Technical 2 for <company/role>, grill me on <project/topic>" — I'll follow up like a panel and score you on the rubric in `06_interview_bank/05_mock_interview_scripts.md`.
- **JD packs:** paste a JD → tailored pack in `07_jd_analysis/`.
- **Explain anything:** "Explain the Jeffreys test like I'm new to it, then quiz me."
- **Review your writing:** send your 90-sec pitch, resume bullets or a practice validation memo for critique.

> **Confidence labels used throughout:** **[Certain]** verified from primary/official sources or hard data · **[Likely]** consistent across credible secondary sources or strong industry pattern · **[Assumption]** my judgment — verify before relying on it. Sources are listed at the end of `00_strategy/01_market_reality_and_targets.md` and linked inline where used.
