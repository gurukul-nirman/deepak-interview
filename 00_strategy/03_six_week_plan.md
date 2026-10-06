# 03 · Six-Week Plan (15 h/week ≈ 90 h)

**Calendar:** Week 1 starts **Mon 5 Oct 2026**; Week 6 ends **Sun 15 Nov 2026**. Diwali is about **Sun 8 Nov** (Week 5 is
front-loaded).
**Daily budget:** Mon–Fri **2 h** · Sat **2.5 h** · Sun **2.5 h**.

**Notice period:**
- Your notice is **3 months with no buy-out**. An offer in Nov–Dec 2026 means joining in **Feb–Mar 2027**.
- Start applying in Week 1, and keep 1–2 applications a week flowing after Week 6.

**The loop:**
1. **Study** a topic (with written output).
2. **Test** it in a mock interview (`START TOPIC` / `START CODING`).
3. **Fix** the gaps listed in the interview record.
4. **Revise** it with `REVISE`.
5. **Re-test** on the spacing rule.
6. Once the core is solid, run **full selection processes** (`START PROCESS`).

**Where the 90 hours go:**

| Bucket | Hours | Why |
|---|---|---|
| Study with output (`01_`–`05_` folders) | 32 | Knowledge you'll be drilled on |
| Topic mock interviews + fixing gaps | 12 | Finds what you *think* you know; builds spoken answers |
| Coding practice + coding mocks | 9 | Python/SQL rounds are pass/fail gates |
| Projects P1 + P2 | 20 | Closes the validation-experience and AI-governance gaps |
| Full selection processes (2) | 11 | Stamina, round transitions, the strict gate |
| Résumé, applications, referrals | 6 | No pipeline means no interviews |

---

## Rules that make 90 hours enough
1. **Output every session.** Each block ends with something written: an answer, code, a finding, a story. Reading without
   output doesn't count.
2. **The diagnostic decides.** Skim topics the diagnostic marks 🟢; spend saved time on 🔴/🟠 topics. `STATUS` tells you
   what's weakest.
3. **Exam mode is uncomfortable — that's the point.** No hints during mocks. Feedback comes at the end, in the record file.
4. **Close the loop the same week.** After every mock, study the gaps it listed (links are in the record) and do the
   `REVISE` drill a few days later.
5. **Say it out loud.** Interviews are spoken. Answer in mocks as you would on a call: conclusion first, then evidence.
6. **End every session** with "commit and push". On Sundays (or when a session ends), ask for a PR to `main` and
   **merge it**, so the next session starts with all your records. See the root `README.md`.

---

## Week-by-week overview

| Week | Theme | Exit criteria (true by Sunday) |
|---|---|---|
| **1** (5–11 Oct) | Diagnostic · statistics · LR/scorecards · your story | Diagnostic done and matrix set; T01/T02 studied; 4 project sheets; résumé v2 live; 10 applications |
| **2** (12–18 Oct) | Monitoring metrics · validation process · start P1 | T03 mock ≥ 65 (🟡); P1 running on real data with MDD challenge list; Python mock done; 20 applications; 5 referral asks |
| **3** (19–25 Oct) | Your domains: IFRS 9 / CECL / RBI ECL · IRB · stress testing · P1 analysis | T05 mock ≥ 65; P1 TODOs done and findings list drafted; SQL mock done; 30 applications |
| **4** (26 Oct–1 Nov) | Governance (SR 26-2 etc.) · AI governance · P1 report · P2 | P1 report self-scored; P2 drafted; T08 or T09 mock done; T06 short mock done |
| **5** (2–8 Nov) | ML validation · behavioural · projects deep-dive · **Process 1 (WF-LQAS)** R0–R4 | T10 and T12 mocks done; 10 STAR stories; Process 1 at R4 or later (or debriefed) |
| **6** (9–15 Nov) | Process 1 finish · **Process 2 (live JD or second persona)** · revision | Process 1 complete; Process 2 complete or at R4+; P1 published (if self-score ≥ 85); next-2-weeks plan |

**When a real interview gets scheduled:**
1. Swap the next 2–3 sessions for: `07_jd_analysis/` prep → `START PROCESS JD: <paste JD>` (run the rounds you'll
   face) → `REVISE` the topics the JD stresses.
2. Return to the plan afterwards.

---

## Day by day

### Week 1 — Diagnostic, foundations, your story (15 h)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | Read the root `README.md` (15 min). **`START DIAGNOSTIC`** (≈ 45 min). Set up Python or Colab, run `python 05_coding/code/validation_toolkit.py` and the P1 pipeline check (`11_projects/P1_pd_model_validation/README.md`, Setup). Then `STATUS` | Baseline skills matrix; adjusted priorities |
| Tue | 2 h | `01_foundations/01_statistics_from_scratch.md` (T01) — skim what's 🟢 | Table: test → what it checks → when used |
| Wed | 2 h | `01_foundations/02_logistic_regression_and_scorecards.md` §1–8 (T02) | WoE/IV explained aloud in 90 seconds |
| Thu | 2 h | Scorecards §9–13; skim `02_credit_risk/01_credit_risk_fundamentals.md` (T11) | End-to-end scorecard build, from memory |
| Fri | 2 h | `05_coding/01_python_for_validation.md` Part A. Coding harness: `python grade.py list`, solve P01–P03 on your own (practice, not a mock) | 3 passing submissions |
| Sat | 2.5 h | `00_strategy/04_positioning_resume_and_stories.md`: 4 project sheets (SBSS BCC/non-BCC, IFRS 9, IRB, stress testing; **not SmarterPay** until you've worked on it); 90-second intro | Sheets + intro |
| Sun | 2.5 h | Résumé v2 + LinkedIn; job alerts; **apply to 10**; `REVISE T01` | 10 applications |

### Week 2 — Monitoring + validation core + P1 start (15 h)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | `03_monitoring_validation/01_performance_monitoring_metrics.md` §0–2 (T03) | KS, Gini and a binomial test by hand |
| Tue | 2 h | Metrics §3–8 (PSI/CSI, RAG, diagnosis matrix, root cause) | Answer to "PSI 0.27 — what do you do?" |
| Wed | 2 h | `03_monitoring_validation/02_independent_validation_playbook.md` §1–5 (T04) | One-page validation plan for your SBSS model |
| Thu | 2 h | Playbook §6–11 | 3 findings in CCCER format |
| Fri | 2 h | **`START TOPIC T03`** (≈ 50 min), then fix the top 3 gaps from the record | Record + fixes |
| Sat | 2.5 h | **P1 steps 1–2:** real data, run `developer_model.py`, read the MDD as a sceptic (`11_projects/P1_pd_model_validation/`); `REVISE T02` | Challenge list |
| Sun | 2.5 h | **`START CODING python`** (≈ 70 min); **apply to 10**; 5 referral requests | Coding record; applications |

### Week 3 — Your domains (highest grilling risk) + P1 analysis (15 h)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` (T05) | ECL formula, staging/SICR and scenarios, whiteboarded |
| Tue | 2 h | `02_credit_risk/03_basel_irb.md` (T06) | PIT/TTC, LRADR, MoC and downturn LGD in 3 minutes |
| Wed | 2 h | `02_credit_risk/04_stress_testing_ccar.md` (T07); run `05_coding/code/stress_test_diagnostics.py` | Diagnostics checklist |
| Thu | 2 h | **`START TOPIC T05`**, then fixes | Record + fixes |
| Fri | 2 h | **P1 step 3:** TODO #1–#3 | Evidence §1–§8 |
| Sat | 2.5 h | **P1 step 3–4:** TODO #4–#6, findings list and overall outcome | Findings list |
| Sun | 2.5 h | **`START TOPIC T04 short`** (≈ 25 min); **`START CODING sql`** (≈ 70 min); **apply to 10** | Two records |

### Week 4 — Governance, AI governance, P1 report, P2 (15 h)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md` + `02_global_regulations_quick_reference.md` (T08) | Two-minute "what changed in SR 26-2" answer |
| Tue | 2 h | `04_governance_regulation/03_ai_ml_genai_model_risk.md` + `04_ai_governance.md` (T09, T14) | AI governance vs MRM in 90 seconds |
| Wed | 2 h | **P1 step 5:** report, sections 1–4 | Draft |
| Thu | 2 h | **P1 step 5–6:** findings and conclusion; self-score with `ANSWER_KEY.md`; log misses | Report + score |
| Fri | 2 h | **P2 steps 1–3** (`11_projects/P2_ai_governance_case/`) | Classification + risks |
| Sat | 2.5 h | **P2 steps 4–5** (controls, tests, recommendation; self-score); **`REVIEW PROJECT P1`** | P2 draft; P1 review |
| Sun | 2.5 h | **`START TOPIC T09`** (or T08 if `STATUS` shows it weaker); **`START TOPIC T06 short`**; apply | Two records |

### Week 5 — ML, behavioural, Process 1 (≈ 14 h; Diwali ≈ Sun 8 Nov)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | `01_foundations/03_ml_for_credit_risk.md` (T10); **`START TOPIC T10 short`** | Record |
| Tue | 2 h | `06_interview_bank/04_behavioral_hr_negotiation.md` (T13): 10 STAR-L stories, notice-period answer, CTC script | Stories doc |
| Wed | 2 h | **`START TOPIC T12`** (your work projects + P1/P2 deep-dive), then fixes | Record |
| Thu | 2 h | **`START PROCESS WF-LQAS`**: R0 recruiter, then R1 online assessment (coding + MCQs) | Process folder |
| Fri | 2 h | `NEXT ROUND` → R2 Technical 1; read feedback; **`REVIEW PROJECT P2`** | R2 record |
| Sat | 3.5 h | `NEXT ROUND` → R3 Technical 2, then R4 validation exercise | R3–R4 records |
| Sun | 0.5 h | Diwali. `REVISE` one weak topic only | — |

A round that isn't cleared **ends the process**. You get `99_final_debrief.md`. Spend the next 2–3 sessions on its gaps,
then start a new process.

### Week 6 — Finish Process 1, run Process 2, polish (15 h)
| Day | Time | Do | Output |
|---|---|---|---|
| Mon | 2 h | `NEXT ROUND` → R5 hiring manager, then R6 senior leader | Records |
| Tue | 2 h | `NEXT ROUND` → R7 HR & offer simulation; final debrief; study its top gaps | Debrief |
| Wed | 2 h | **`START PROCESS <live JD or second persona>`** (e.g., `JD: <paste>`, `AMEX-SM`, `CITI-MRM`): R0 + R1 | Process 2 folder |
| Thu | 2 h | R2 + R3 | Records |
| Fri | 2 h | R4 validation exercise | Record |
| Sat | 2.5 h | R5–R7 | Records + debrief |
| Sun | 2.5 h | `STATUS`; `REVISE` the 3 weakest topics; add P1/P2 to the résumé; publish P1 if self-score ≥ 85; plan the next 2 weeks | Plan |

---

## If an interview lands before Week 3 — 10-hour emergency path
| Hours | Do |
|---|---|
| 2 | Project sheets + 90-second intro (`04_positioning_resume_and_stories.md`) |
| 2 | Metrics doc (KS/Gini/PSI/calibration + diagnosis matrix), then `REVISE T03` |
| 2 | Validation playbook (workstreams, findings, outcomes), then `REVISE T04` |
| 1.5 | SR 11-7 core + SR 26-2 changes, then `REVISE T08` |
| 1.5 | The domain doc for the JD's main area, then `REVISE` it |
| 1 | `START PROCESS JD: <paste>` — just the round you're about to face |

---

## Job-search track (inside the Sunday blocks)
| Week | Action |
|---|---|
| 1 | Résumé v2 + LinkedIn (templates in `04_positioning_resume_and_stories.md`). Alerts on Naukri, LinkedIn, iimjobs and Instahyre: "model validation", "model risk", "credit risk modelling", "quantitative analytics specialist", "IFRS 9", "IRB", "CCAR". Apply to 10 |
| 2 | 10 applications + **5 referral requests** (ex-colleagues at banks, alumni); register with 3 specialist risk/quant recruiters |
| 3 | 10 applications; follow up on Week 1 |
| 4 | 10 applications; try to cluster interviews in Weeks 5–8 so offers land close together |
| 5–6 | Interviews; 1–2 new applications a week. Europe/Singapore pack after Week 6 (agreed to do later) |

**Referral message (short):**
> Hi <Name> — I work in credit-risk model performance monitoring (5 yrs: IFRS 9/CECL, Basel IRB, CCAR stress-testing
> and FICO SBSS scorecards) and I'm moving into model validation/MRM. I saw <Role, Req ID> on your team at <Bank>. Would
> you be open to referring me? Résumé attached; happy to share a 3-line summary for the form. Thanks!

---

## Sunday self-check (10 min)
- [ ] Hours ≥ 14
- [ ] `STATUS` run. Re-tests due this week are scheduled (spacing: 🔴/🟠 3–4 days · 🟡 7 days · 🟢 14 days)
- [ ] Every gap from this week's mocks studied, or scheduled for next week
- [ ] Applications this week ≥ 10 (Weeks 1–4)
- [ ] Session records committed; PR to `main` opened **and merged**
