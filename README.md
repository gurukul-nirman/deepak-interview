# Credit-Risk Model Validation & MRM — Interview Prep System (Oct–Nov 2026)

**Goal:** clear every round, first call to offer, for credit-risk **model validation / MRM / monitoring** roles at
**≥ ₹40L fixed**. India first; Europe and Singapore later.

**Profile:**
- 5 years of credit-risk performance monitoring at an analytics vendor/KPO.
- Models: IFRS 9/CECL, Basel IRB, CCAR stress testing, FICO SBSS (BCC and non-BCC). SmarterPay is pending its knowledge
  transfer, so don't claim it yet.
- Tools: SQL, SAS, some Python, a little Tableau.
- B.Tech (EEE). Notice period 3 months, no buy-out.

**Constraints:** 6 weeks (5 Oct → 15 Nov 2026) · about 15 h/week · Pareto-first · starts from zero knowledge.

---

## 1. Start here

**Very first session (Mon 5 Oct):**
1. Open a Claude Code session on this repo and type **`START DIAGNOSTIC`** (about 45 minutes, exam mode).
2. Then type **`STATUS`**. You get your starting skills matrix and the three things to do next.
3. Follow `00_strategy/03_six_week_plan.md` day by day.

**Every session:**

| When | Say | Why |
|---|---|---|
| Start (optional) | `STATUS` | Shows what's due: re-tests, open gaps, the next plan item |
| During | Any command below, or plain English ("let's do a mock on IFRS 9") | |
| End | **"commit and push"**, then **"open a PR to main"** — then **merge the PR** on GitHub (or ask me to) | Records live on the session branch until merged. A new session starts from `main` **[Likely]**, so an unmerged PR means the next session can't see your history |

---

## 2. How it works — two routes

```
         ┌──────────────── Route 1: learn topic by topic ────────────────┐
 study ──► START TOPIC / START CODING ──► record: Q&A, scorecard, gaps, ──► fix gaps ──► REVISE ──► re-test
 (01–05)        (exam mode, drill-down)    corrections, model answers                         (spacing rule)
                                                     │
                                                     ▼  updates 09_progress/ and 10_revision/ automatically
         ┌──────────────── Route 2: full selection process ──────────────┐
 START PROCESS <persona | JD> ──► R0 recruiter ──► R1 online test ──► R2 Tech 1 ──► R3 Tech 2 ──► R4 validation exercise
     ──► R5 hiring manager ──► R6 senior leader ──► R7 HR & offer.  Each round is its own .md file.
     Strict gate: a round you don't clear ends the process (final debrief written).
```

**How the interviews behave:**
- **Exam mode.** One question at a time. No hints or scores until the end.
- **Drill-down follow-ups** adapt to your answer — escalate, probe a gap, ask for specifics, challenge, anchor, ask why,
  add a constraint — up to five levels deep (define → explain → apply → critique → judge). This mirrors how real panels
  grill.

**What every interview record contains:**
- every question and your verbatim answer;
- a scorecard per answer (accuracy, depth, clarity, to-the-point, application);
- the model answer with a deeper explanation;
- **knowledge gaps and corrections** with severity and study links;
- communication feedback, revision items and next actions.

Full rules: `08_mock_interviews/INTERVIEW_PROTOCOL.md` · user guide: `08_mock_interviews/README.md`.

---

## 3. Commands
| You type | What happens |
|---|---|
| `START DIAGNOSTIC` | Baseline across all core topics → initial skills matrix |
| `START TOPIC T05` · `START TOPIC IFRS 9 deep` · `START TOPIC T04 short AVP` | In-depth topic interview (short ≈ 25 min / standard ≈ 50 / deep ≈ 80; VP bar by default) |
| `START CODING python` · `START CODING sql hard` · `START CODING mixed` | Coding interview; your code runs against visible and hidden tests |
| `START PROCESS WF-LQAS` · `START PROCESS JD: <paste JD>` | New full selection process in its own folder; Round 0 starts |
| `NEXT ROUND` | Next round of the current process (only if the last one was cleared) |
| `PAUSE` · `RESUME <id>` · `END` | Pause; continue later; finish early and write the record |
| `REVISE T03` | 10 rapid questions from the topic's refresher, instant feedback |
| `STATUS` | Statuses, recent scores, open gaps, next three actions |
| `EXPLAIN <concept>` | Teaching mode, e.g., `EXPLAIN Jeffreys test` |
| `REVIEW PROJECT P1` · `REVIEW PROJECT P2` | Head-of-MRM review of your portfolio report |

**Topic codes (full list in `09_progress/syllabus.md`):**
- **Core:** T01 statistics · T02 LR & scorecards · T03 monitoring metrics · T04 validation process & findings · T05 IFRS
  9/CECL · T06 Basel IRB · T07 stress testing · T08 MRM governance · T09 AI governance · T10 ML validation · T11 credit
  fundamentals · T12 your projects · T13 behavioural/HR.
- **As needed:** T14 GenAI risk · T15 wholesale credit · T16 data/implementation · T17 fraud/AML · T18 quant puzzles.
- **Coding:** C1–C7.

**Personas for `START PROCESS`** (`08_mock_interviews/process_personas.md`):
- **India:** WF-LQAS (default), AMEX-SM, CITI-MRM, JPM-MRGR, BARC-IVU, HSBC-MRM, GS-MRM, SCB-MV, DB-MRM, BIG4-ECL,
  FIN-LEAD.
- **Europe:** ING-MV, ABN-MV, UBS-MRM, UK-BANK.
- **Singapore:** DBS-MV, OCBC-MRM.

---

## 4. Dashboard — where you stand
| What | File |
|---|---|
| Everything to learn: topics → subtopics → priority → depth → study file → "interview-ready" criteria | `09_progress/syllabus.md` |
| **What you know well / what to improve / what to study** — status per topic, scores, re-test dates, project stages | `09_progress/skills_matrix.md` |
| Every knowledge gap found in mocks (and when it was fixed) | `09_progress/gap_log.md` |
| Every interview and process with scores | `09_progress/interview_log.md` |
| Quick refreshers (short answers), updated after every mock | `10_revision/` |

**Current status:** not yet assessed. Run `START DIAGNOSTIC`.

**Status key:**
- ⚪ not assessed
- 🔴 < 50
- 🟠 50–64
- 🟡 65–74
- 🟢 ≥ 75 twice
- ⭐ ≥ 85 twice

**Re-test spacing:** 🔴/🟠 3–4 days · 🟡 7 days · 🟢 14 days.

---

## 5. The six weeks at a glance (`00_strategy/03_six_week_plan.md`)
| Week | Focus | Mocks / projects |
|---|---|---|
| 1 · 5–11 Oct | Diagnostic · statistics · LR/scorecards · your story · résumé · 10 applications | `START DIAGNOSTIC` |
| 2 · 12–18 Oct | Monitoring metrics · validation process | T03 · coding (Python) · **P1 starts** |
| 3 · 19–25 Oct | IFRS 9/CECL/RBI ECL · IRB · stress testing | T05 · T04 short · coding (SQL) · P1 analysis |
| 4 · 26 Oct–1 Nov | SR 26-2 & global MRM · AI governance | T09 or T08 · T06 short · **P1 report · P2** |
| 5 · 2–8 Nov | ML validation · behavioural · projects deep-dive | T10 · T12 · **Process 1 (WF-LQAS)** |
| 6 · 9–15 Nov | Finish Process 1 · Process 2 (live JD or second persona) · revision | Process 2 · publish P1 |

When a real interview is scheduled: paste the JD (`07_jd_analysis/`) and run `START PROCESS JD: <paste>` for the
rounds you'll face.

---

## 6. Portfolio projects (`11_projects/`)

| Project | What you do | Time |
|---|---|---|
| **P1 · PD-model validation** | Validate a deliberately flawed credit-card PD model on public UCI data: replicate, test, find the 13 planted issues, write a committee-style report | ~15 h, weeks 2–4 |
| **P2 · AI-governance case** | Assess a GenAI credit-memo assistant across RBI / EU / Singapore rules, NIST AI 600-1 and OWASP LLM Top 10; recommend with conditions | ~5 h, week 4 |

**Why these two:** they close your three biggest profile gaps — monitoring → validation, no AI-governance exposure, and
degree screens. Each project has an answer key (open it only after writing), a self-scoring rubric and an interview kit.

---

## 7. Where interview points come from (Pareto) **[Assumption — synthesised from research]**
| Share | Topic | Main files |
|---|---|---|
| ~30% | **Your projects** under grilling | `00_strategy/04_positioning_resume_and_stories.md` · `06_interview_bank/02_question_bank_tier2_grilling.md` |
| ~20% | **Metrics + LR/scorecards** | `03_monitoring_validation/01_performance_monitoring_metrics.md` · `01_foundations/02_logistic_regression_and_scorecards.md` |
| ~15% | **Validation framework + findings** | `03_monitoring_validation/02_independent_validation_playbook.md` · `06_interview_bank/03_case_studies.md` |
| ~15% | **IFRS 9/CECL, IRB, stress testing** | `02_credit_risk/` |
| ~8% | **Governance, regulation, AI governance** | `04_governance_regulation/` |
| ~7% | **Coding** (Python, SQL, SAS) | `05_coding/` · `08_mock_interviews/coding_harness/` |
| ~5% | **Behavioural / HR / negotiation** | `06_interview_bank/04_behavioral_hr_negotiation.md` |

---

## 8. What the research says (bottom line)
1. **₹40L fixed at about 5 years is a top-decile outcome.** Realistic targets: AmEx Senior Manager, Wells Fargo Lead
   QAS, top-of-band Citi/JPM/GS, VP-level roles (stretch), fintech leads; Europe/Singapore later.
   → `00_strategy/01_market_reality_and_targets.md`
2. **SR 11-7 was replaced by SR 26-2 on 17 Apr 2026.** Most candidates still quote SR 11-7 as current, so knowing both
   is a cheap differentiator. → `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md`
3. **The 2026–27 regulatory wave drives hiring:**
   - RBI ECL (1 Apr 2027) and RBI draft MRM guidance (Jun 2026);
   - OSFI E-23 (May 2027);
   - EU AI Act high-risk credit scoring (2 Dec 2027);
   - the build-out of AI/ML validation teams.
4. **Your edge:** breadth across provisioning, capital and stress models, plus a vendor model (SBSS).
   **Your gaps:** monitoring → validation framing, Python depth, AI governance, possible Master's screens.
   → `00_strategy/05_gap_analysis_and_upgrades.md`

---

## 9. Repo map
| Folder | Contents |
|---|---|
| `00_strategy/` | Market & targets · interview process map · six-week plan · positioning & project sheets · gap analysis |
| `01_foundations/` | Statistics · logistic regression & scorecards · ML for credit risk |
| `02_credit_risk/` | Fundamentals · IFRS 9/CECL/RBI ECL · Basel IRB · stress testing · wholesale/commercial models |
| `03_monitoring_validation/` | Metrics (formulas, worked examples, diagnosis matrix) · independent validation playbook |
| `04_governance_regulation/` | SR 11-7 → SR 26-2 · global regulations · AI/ML/GenAI model risk · AI governance |
| `05_coding/` | Python, SQL, SAS guides · tested toolkit and demos in `code/` |
| `06_interview_bank/` | Tier-1 Q&A · grilling ladders · 16 cases · behavioural & negotiation · mock scripts · cheat sheet · quant screen |
| `07_jd_analysis/` | Paste a JD → tailored prep pack |
| `08_mock_interviews/` | Protocol, topic catalog, personas, templates, coding auto-grader, and **all your interview records** |
| `09_progress/` | Syllabus, skills matrix, gap log, interview log |
| `10_revision/` | One quick-refresher file per topic |
| `11_projects/` | Portfolio projects P1 and P2 |

**Run the code:**
1. Install dependencies: `pip install -r 05_coding/code/requirements.txt`.
2. Then any of:
   - `python 05_coding/code/validation_toolkit.py`
   - `python 05_coding/code/demo_end_to_end.py`
   - `python 08_mock_interviews/coding_harness/grade.py list`

> **Confidence labels used throughout:**
> - **[Certain]** — verified from primary or official sources, or hard data.
> - **[Likely]** — consistent across credible secondary sources, or a strong industry pattern.
> - **[Assumption]** — judgment; verify before relying on it.
>
> Regulatory facts are as of Oct 2026.
