# 05 · Gap Analysis of the First Version — and What Was Upgraded

> You asked for an honest check of whether the first kit is worth it. Short answer: **the content is solid, but the first version was a library, not a training system.** It told you *what* to know but gave you no way to practise, get scored, see your gaps, or revise quickly. This upgrade turns it into a system.

---

## 1. What was already strong (keep using)
| Area | Why it's worth it |
|---|---|
| Market research | Real 2026 pay bands; shows 40L fixed is top-decile and which titles can pay it |
| Regulatory currency | SR 26-2 (Apr 2026), RBI ECL/MRM (2026), OSFI E-23, EU AI Act timing, SBA's SBSS change — most candidates won't know these |
| Core technical content | Metrics, scorecards, IFRS 9/IRB/stress testing, validation playbook, findings writing |
| Tested code | Toolkit, end-to-end validation demo, stress-test diagnostics, SQL practice DB |
| Pareto focus | ~65% of interview time = your projects + metrics/scorecards + validation framework |

## 2. Gaps found (and the fix in this upgrade)
| # | Gap | Impact | Fix |
|---|---|---|---|
| 1 | **No operating system** — 24 files, no clear way to use them | You didn't know where to start or how mocks would work | `README.md` is now a dashboard + commands; `CLAUDE.md` makes every future chat run the same way |
| 2 | **Mocks were static scripts** — no adaptive follow-ups | Real interviews drill into *your* answer | Adaptive drill-down protocol (`08_mock_interviews/INTERVIEW_PROTOCOL.md`) |
| 3 | **No recorded outputs or scores** | No evidence of progress; feedback lost | Every interview produces a document: transcript, scorecard, model answers, gaps & corrections |
| 4 | **No full selection-process simulation** | Never practised the whole loop under pressure | Route 2: one folder per process, one file per round, strict pass/fail gate |
| 5 | **No coding simulation with real grading** | Can't tell if your code is actually correct | Auto-grader runs your Python/SQL against hidden tests (`08_mock_interviews/coding_harness/`) |
| 6 | **No way to know what you know** | Study time spread evenly instead of on weak spots | Diagnostic + skills matrix + gap log (`09_progress/`) |
| 7 | **No quick revision** | Cheat sheet was generic and static | Per-topic refreshers that get updated after every interview (`10_revision/`) |
| 8 | **AI governance was thin** (validation of AI, not governance) | AI governance is now a standard MRM interview topic | Full AI governance module + topic interview + revision file + portfolio case |
| 9 | **No wholesale/commercial credit** | Wells Fargo CMoR and other roles validate commercial models | New primer `02_credit_risk/05_wholesale_commercial_credit_models.md` |
| 10 | **No portfolio** | B.Tech (no Master's) + monitoring→validation move needs proof | Two projects: PD-model validation report + AI-governance risk assessment (`11_projects/`) |
| 11 | **Outdated profile assumptions** (SmarterPay claimed; UAE-first; notice/degree unknown) | Risky claims; wrong targeting | Updated: SmarterPay not claimed; Europe/SG preferred (pack later); 3-month notice and B.Tech EEE built into targeting and HR answers |
| 12 | **Plan had no mocks/projects/revision loop** | Learning without testing | New plan: learn → test → fix → re-test, with two full processes in Weeks 5–6 |
| 13 | **Kit lived only on a side branch** | New chats wouldn't see it | PR to `main` so every session loads the kit and the protocol |

## 3. Known limits (on request, not built yet)
> **Update 7 Oct 2026:** a second audit — this time from a hiring manager's seat — is in `06_prep_audit_2026-10-07.md`.
> It re-weights the plan towards your own evidence, résumé and pipeline, fixes Windows-breaking bugs in the code, and adds
> the evidence bank, applications tracker, real-interview debriefs and a PySpark primer.
- Market/counterparty credit risk model validation (VaR, FRTB, CVA) — only if a JD needs it.
- AML/transaction-monitoring model validation in depth (fraud basics are covered).
- PySpark at scale (a primer now exists: `05_coding/04_pyspark_primer.md`).
- Europe/Singapore abroad pack (you asked to do it later).
- Some figures remain labelled **[Likely]/[Assumption]** (e.g., AmEx band mapping, RBI ECL floors) — verify in the source before quoting in an interview.

## 4. How the new system fits together
```
            ┌──────────── 09_progress/syllabus.md (what to learn, priority, depth) ────────────┐
            │                                                                                  │
 Study (00–07 docs) ─► Topic / coding interview (08) ─► Scorecard + gaps ─► Revision file (10) ─► Re-test
            │                                   │                                              │
            └────────── skills_matrix.md (status 🔴🟡🟢⭐) ◄── gap_log.md ◄────────────────────┘
                                                │
                       Weeks 5–6: full selection processes (strict gate) ─► real interviews
```
