# 03 · Six-Week Plan (15 hrs/week ≈ 90 hrs total)

**Calendar:** Week 1 starts **Mon 5 Oct 2026** → Week 6 ends **Sun 15 Nov 2026**.
**Daily budget:** Mon–Fri **2 h** · Sat **2.5 h** · Sun **2.5 h**.
**Principle:** Pareto first (projects + metrics + validation framework ≈ 65% of interview score), apply from Week 1, mock from Week 3.

---

## 0. Rules that make 90 hours enough

1. **Output every session.** Each block ends with a written artifact (answer, code, story). Reading without output doesn't count.
2. **Say it out loud.** Interviews are spoken. Record 1–2 answers per day on your phone; listen back once a week.
3. **Error log.** One sheet: `date | question | what I said | correct answer | tag`. Review it every Sunday. Your error log *is* your personalised Pareto.
4. **Tier discipline.** In the question bank, Tier 1 = must answer cold. Tier 2 = can reason through. Tier 3 = skip unless a JD demands it.
5. **Mock with me.** Message: *"Mock: Technical 2 for Wells Fargo LQAS, grill me on IFRS 9"* — I'll run it and score you.

---

## 1. Week-by-week overview

| Week | Theme | Hours | Exit criteria (must be true by Sunday) |
|---|---|---|---|
| **1** (5–11 Oct) | Foundations + your story + start applying | 15 | 90-sec intro recorded; 5 project sheets drafted; LR/WoE/IV/scorecard explainable cold; resume v2 live; 10 applications out |
| **2** (12–18 Oct) | Monitoring metrics + validation core + Python metrics | 15 | KS/Gini/PSI/CSI/HL/binomial/Jeffreys computed by hand **and** in Python; validation workstreams listed from memory; 10 more applications |
| **3** (19–25 Oct) | Your domains: credit fundamentals, IFRS 9/CECL/RBI ECL, IRB, stress testing | 15 | Can whiteboard ECL formula, staging/SICR, IRB capital intuition, stress-test model diagnostics; Mock 1 done |
| **4** (26 Oct–1 Nov) | Governance (SR 11-7 → SR 26-2, PRA, OSFI, RBI) + ML/AI validation + SQL/SAS | 15 | SR 26-2 changes in 2 minutes; ML validation checklist; 2 timed coding sets passed; Mock 2 done |
| **5** (2–8 Nov, Diwali ≈ 8 Nov) | Grilling drills + cases + behavioral + negotiation | 15 (front-load Mon–Sat) | 15 cases answered; 10 STAR stories; negotiation script; Mock 3 (full loop) done |
| **6** (9–15 Nov) | Interview mode: JD-specific prep, spaced repetition, polish | 15 | Tier-1 bank ≥ 90% cold recall; company dossiers for every live process |

---

## 2. Day-by-day

### Week 1 — Foundations + your story + start applying
| Day | Block (time) | Do | Output |
|---|---|---|---|
| Mon | 2 h | Read `README.md`, `01_market_reality_and_targets.md`, `02_interview_process_map.md`. Install Anaconda or use Google Colab. | Target list (10 Tier A, 10 Tier B) in a sheet |
| Tue | 2 h | `01_foundations/01_statistics_from_scratch.md` §1–5 (distributions, sampling, hypothesis tests, p-values, CIs) | 10 flash answers in error log |
| Wed | 2 h | Stats §6–10 (tests used in validation, regression basics, MLE, time-series diagnostics) | Table: test → what it checks → when used |
| Thu | 2 h | `01_foundations/02_logistic_regression_and_scorecards.md` §1–5 (LR, odds, MLE, assumptions, WoE/IV) | Explain WoE/IV aloud in 90 sec (record) |
| Fri | 2 h | Scorecards §6–11 (sample design, binning, scaling/PDO, reject inference, segmentation, calibration) | Whiteboard the end-to-end scorecard build |
| Sat | 2.5 h | `05_coding/01_python_for_validation.md` Part A (Python + pandas basics); run `validation_toolkit.py` demo once | Notebook with your first decile table |
| Sun | 2.5 h | `00_strategy/04_positioning_resume_and_stories.md`: fill **5 project sheets** (SBSS BCC/non-BCC, SmarterPay, IFRS 9, IRB, stress testing); update resume + LinkedIn; **apply to 10** | 5 sheets + resume v2 + 10 applications |

### Week 2 — Monitoring + validation core + Python metrics
| Day | Block | Do | Output |
|---|---|---|---|
| Mon | 2 h | `03_monitoring_validation/01_performance_monitoring_metrics.md` §1–4 (KS, Gini/AUC/AR, CAP/ROC, rank ordering) | Compute KS & Gini **by hand** on the worked example |
| Tue | 2 h | Metrics §5–8 (PSI/CSI, calibration tests, thresholds/RAG, diagnosis matrix) | "PSI 0.27 — what do you do?" answer recorded |
| Wed | 2 h | `02_independent_validation_playbook.md` §1–5 (lifecycle, tiering, scoping, data, conceptual soundness, replication) | Validation plan for *your* SBSS model (1 page) |
| Thu | 2 h | Playbook §6–10 (benchmarking, sensitivity, outcomes, implementation, monitoring review, outcome ratings) + findings section | 3 findings written in condition/criteria/cause/effect/recommendation format |
| Fri | 2 h | `06_interview_bank/01_question_bank_tier1.md` sections A–C (stats, LR/scorecards, metrics) — answer aloud, then check | Error log +15 entries |
| Sat | 2.5 h | `05_coding` Part B: implement KS, Gini, PSI, WoE/IV **from scratch** (don't copy); compare to toolkit | Your own `my_metrics.py` |
| Sun | 2.5 h | `05_coding/02_sql_for_credit_risk.md` drills 1–8 (joins, windows, vintage, roll rates); **apply to 10**; reach out to 5 people for referrals | SQL solutions + 10 apps + 5 referral asks |

### Week 3 — Your domains (these are *your* claimed areas → highest grilling risk)
| Day | Block | Do | Output |
|---|---|---|---|
| Mon | 2 h | `02_credit_risk/01_credit_risk_fundamentals.md` (EL, PD/LGD/EAD/CCF, delinquency, vintage, roll rates, charge-off, SBSS) | Formula sheet page 1 |
| Tue | 2 h | `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` | Whiteboard: ECL = Σ PD·LGD·EAD·DF across scenarios; staging rules |
| Wed | 2 h | `02_credit_risk/03_basel_irb.md` | Explain PIT vs TTC, LRADR, MoC, downturn LGD in 3 min |
| Thu | 2 h | `02_credit_risk/04_stress_testing_ccar.md` | Diagnostics checklist for a macro-regression; 2026 Fed changes |
| Fri | 2 h | Tier-1 bank sections D–F (IFRS 9, IRB, stress testing) + case studies 1–5 | Error log +15 |
| Sat | 2.5 h | `05_coding/03_sas_essentials.md` (PROC LOGISTIC, NPAR1WAY, RANK, SQL, macros); rewrite your monitoring report logic in SAS pseudocode | 1 SAS macro for PSI |
| Sun | 2.5 h | **Mock 1** (Technical 2: your projects + one domain) with me or a friend — 60 min; review; **apply to 10** | Mock scorecard + fixes |

### Week 4 — Governance, ML/AI, coding polish
| Day | Block | Do | Output |
|---|---|---|---|
| Mon | 2 h | `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md` | 2-minute "what changed in SR 26-2" answer recorded |
| Tue | 2 h | `04_governance_regulation/02_global_regulations_quick_reference.md` (PRA SS1/23, OSFI E-23, RBI MRM draft + ECL, ECB/EBA, EU AI Act, MAS) | One-line summary per regulation |
| Wed | 2 h | `01_foundations/03_ml_for_credit_risk.md` (trees, GBM, overfitting, SHAP, fairness, monotonic constraints) | "LR vs XGBoost — which and why?" answer |
| Thu | 2 h | `04_governance_regulation/03_ai_ml_genai_model_risk.md` | ML validation checklist from memory; GenAI 5-pillar answer |
| Fri | 2 h | Tier-1 sections G–I (validation, governance, ML) + case studies 6–10 | Error log +15 |
| Sat | 2.5 h | Timed coding set 1 (Python, 45 min) + set 2 (SQL, 45 min); run `demo_end_to_end.py` and explain every output | Scored attempts |
| Sun | 2.5 h | **Mock 2** (Hiring manager + case) — 60 min; JD-specific prep for any live process; **apply to 10** | Mock scorecard |

### Week 5 — Grilling drills + behavioral + negotiation (Diwali ≈ Sun 8 Nov: front-load)
| Day | Block | Do | Output |
|---|---|---|---|
| Mon | 2 h | `06_interview_bank/02_question_bank_tier2_grilling.md` ladders A–F (have someone read them to you) | Error log +10 |
| Tue | 2 h | Tier-2 ladders G–L | Error log +10 |
| Wed | 2 h | Case studies 11–15 | Written answers (bullet form) |
| Thu | 2 h | `06_interview_bank/04_behavioral_hr_negotiation.md`: 10 STAR-L stories + "Why validation / why leave / why us" | Stories doc |
| Fri | 2 h | Negotiation script + offer comparison sheet; company dossiers for live processes | Script + dossiers |
| Sat | 4.5 h | **Mock 3 — full loop** (screen + tech 1 + tech 2 + HM) back-to-back; timed coding set 3 | Final gap list |
| Sun | 0.5 h | Diwali — rest. Review error log only. | — |

### Week 6 — Interview mode
| Day | Block | Do | Output |
|---|---|---|---|
| Mon–Fri | 2 h/day | 60 min spaced repetition (Tier-1 questions from error log) + 60 min company-specific prep for scheduled interviews (`07_jd_analysis/`) | Cold-recall ≥ 90% |
| Sat | 2.5 h | Timed coding set 4 + one case aloud | — |
| Sun | 2.5 h | Final review of 1-page cheat sheets; plan next 2 weeks of interviews | — |

---

## 3. If an interview lands early (before Week 3) — the 10-hour emergency path

| Hours | Do |
|---|---|
| 2 | Your 5 project sheets + 90-sec intro (the 30% bucket) |
| 2 | Metrics doc §1–8 (KS/Gini/PSI/calibration + diagnosis matrix) |
| 2 | Validation playbook (workstreams + findings + outcomes) |
| 1.5 | SR 11-7 core + SR 26-2 changes |
| 1.5 | Domain doc for the JD's main area (IFRS 9 *or* IRB *or* stress testing) |
| 1 | Tier-1 question bank — only the sections the JD emphasises |

---

## 4. Job-search track (runs in parallel, inside the Sunday blocks)

| Week | Action |
|---|---|
| 1 | Resume v2 + LinkedIn headline/about (templates in `04_positioning_resume_and_stories.md`); set Naukri/LinkedIn/iimjobs/Instahyre alerts: "model validation", "model risk", "credit risk modelling", "quantitative analytics specialist", "IFRS 9", "IRB", "CCAR"; apply to 10 |
| 2 | 10 applications + **5 referral requests** (ex-colleagues now at banks; alumni); register with 3 specialist recruiters (risk/quant desks) |
| 3 | 10 applications incl. 3 UAE (LinkedIn, Bayt, bank career sites); follow up on Week-1 apps |
| 4 | 10 applications; schedule interviews to cluster Weeks 4–7 so offers land close together |
| 5–6 | Interviews; keep 1–2 new applications/week flowing so the pipeline doesn't dry up |

**Referral message (short):**
> Hi <Name> — I'm a credit risk modeler (5 yrs: IFRS 9/CECL, Basel IRB, CCAR stress-testing models, FICO SBSS scorecards) moving into model validation/MRM. I saw <Role, Req ID> on your team at <Bank>. Would you be open to referring me? Resume attached; happy to share a 3-line summary for the referral form. Thanks!

---

## 5. Weekly self-check (Sunday, 10 min)

- [ ] Hours logged ≥ 14
- [ ] Error log reviewed; top 5 weak areas scheduled into next week
- [ ] Applications sent this week ≥ 10 (Weeks 1–4)
- [ ] One recorded answer listened to; one fix made
- [ ] Next week's interviews have a dossier started
