# Syllabus — everything you need to know, in priority order

> **This is the complete map.** P1 = must be interview-ready (the 20% that drives ~80% of questions) · P2 = important for many roles · P3 = role-specific.
> **Depth target:** **K** know (define) · **E** explain (why/how) · **A** apply (compute/use) · **C** challenge (limits, judgment — the validator's level).
> Tick a box when done: 📖 studied · 🔁 revision file read · 🎤 interviewed (score ≥ 75).

---

## Module 1 — Foundations
| Code | Topic | Subtopics | Prio | Depth | Study | 📖 | 🔁 | 🎤 |
|---|---|---|---|---|---|---|---|---|
| T01 | Statistics for validation | distributions; SE & CIs; p-values; Type I/II; binomial/Jeffreys/HL/KS/t/χ²/DeLong; correlation; OLS assumptions & diagnostics; MLE; stationarity | P1 | C | `01_foundations/01_statistics_from_scratch.md` | ☐ | ☐ | ☐ |
| T02 | Logistic regression & scorecards | odds/logit; MLE; assumptions; WoE/IV; binning; selection; reject inference; PDO scaling; oversampling correction; segmentation; swap sets | P1 | C | `01_foundations/02_logistic_regression_and_scorecards.md` | ☐ | ☐ | ☐ |
| T10 | ML model validation | trees/GBM; hyperparameters; overfitting & leakage; calibration; SHAP/PDP; reason codes; fairness; monotonic constraints; fraud models | P1 | A→C | `01_foundations/03_ml_for_credit_risk.md` | ☐ | ☐ | ☐ |

## Module 2 — Credit risk domain
| Code | Topic | Subtopics | Prio | Depth | Study | 📖 | 🔁 | 🎤 |
|---|---|---|---|---|---|---|---|---|
| T11 | Credit risk fundamentals | lifecycle; products; DPD/default/charge-off; PD/LGD/EAD/CCF; EL/UL; vintages; roll rates; bureaus & SBSS; capital basics; card economics | P1 | A | `02_credit_risk/01_credit_risk_fundamentals.md` | ☐ | ☐ | ☐ |
| T05 | IFRS 9 / ECL & CECL | stages; SICR; ECL formula; lifetime PD; TTC→PIT; scenarios; overlays; LGD/EAD; CECL differences; RBI ECL 2027 | P1 | C | `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` | ☐ | ☐ | ☐ |
| T06 | Basel IRB | approaches; ASRF formula; correlations; floors; LRADR; MoC; downturn LGD; DoD; PIT/TTC; LDPs; ECB tests | P1 | C | `02_credit_risk/03_basel_irb.md` | ☐ | ☐ | ☐ |
| T07 | Stress testing & econometrics | CCAR/DFAST/SCB & 2026 changes; ICAAP; top-down vs bottom-up; MEVs; stationarity; HAC; BG; dynamic back-tests; sensitivity; COVID | P1 | C | `02_credit_risk/04_stress_testing_ccar.md` | ☐ | ☐ | ☐ |
| T15 | Wholesale/commercial credit | obligor vs facility ratings; master scale; ratio scorecards; overrides; LDPs; CRE; commercial CCAR/CECL | P2 | E | `02_credit_risk/05_wholesale_commercial_credit_models.md` | ☐ | ☐ | ☐ |

## Module 3 — Monitoring & validation (your core)
| Code | Topic | Subtopics | Prio | Depth | Study | 📖 | 🔁 | 🎤 |
|---|---|---|---|---|---|---|---|---|
| T03 | Monitoring metrics | KS; Gini/AUC/AR; CAP/ROC; rank-ordering; A/E; binomial/Jeffreys/HL/Brier; PSI/CSI; characteristic analysis; RAG; diagnosis matrix; root-cause playbook | P1 | C | `03_monitoring_validation/01_performance_monitoring_metrics.md` | ☐ | ☐ | ☐ |
| T04 | Validation process & findings | types; tiering; process; workstreams A–J; replication; benchmarking; sensitivity; implementation testing; findings & severity; outcomes; pushback; vendor models | P1 | C | `03_monitoring_validation/02_independent_validation_playbook.md` | ☐ | ☐ | ☐ |
| T16 | Data, implementation & documentation review | lineage & reconciliation; data quality; prod-vs-dev parity; EUCs; reading an MDD critically | P2 | A | playbook §5B/§5H | ☐ | ☐ | ☐ |

## Module 4 — Governance, regulation & AI
| Code | Topic | Subtopics | Prio | Depth | Study | 📖 | 🔁 | 🎤 |
|---|---|---|---|---|---|---|---|---|
| T08 | MRM governance & regulation | SR 11-7 concepts; **SR 26-2 changes**; 3LoD; inventory; tiering; change mgmt; PMAs; KRIs; PRA SS1/23; ECB guide 2025; OSFI E-23; RBI MRM draft | P1 | C | `04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md`, `02_global_regulations_quick_reference.md` | ☐ | ☐ | ☐ |
| T09 | AI governance & AI regulation | AI gov vs MRM; operating model; policy stack; AI inventory; tiering; lifecycle gates; EU AI Act; NIST AI RMF + 600-1; ISO 42001/23894/42005; FREE-AI; MAS; OSFI; DPDP; OWASP LLM; KRIs | P1 | E→C | `04_governance_regulation/04_ai_governance.md` | ☐ | ☐ | ☐ |
| T14 | GenAI/LLM & agentic AI risk | risk taxonomy; 5-pillar validation; evaluation metrics; red-teaming; agent controls; vendor models | P2 | E | `04_governance_regulation/03_ai_ml_genai_model_risk.md` | ☐ | ☐ | ☐ |

## Module 5 — You (projects, behaviour, offer)
| Code | Topic | Subtopics | Prio | Depth | Study | 📖 | 🔁 | 🎤 |
|---|---|---|---|---|---|---|---|---|
| T12 | Your projects deep-dive | SBSS BCC/non-BCC; IFRS 9; IRB; stress testing; one breach story each; numbers; limitations (SmarterPay after KT) | P1 | C | `00_strategy/04_positioning_resume_and_stories.md` | ☐ | ☐ | ☐ |
| T13 | Behavioural, HR & negotiation | STAR-L stories; why validation/leave/us; pushback; notice (3 months); CTC & negotiation | P1 | A | `06_interview_bank/04_behavioral_hr_negotiation.md` | ☐ | ☐ | ☐ |

## Module 6 — Coding
| Code | Area | What "ready" means | Prio | Practice | 📖 | 🎤 |
|---|---|---|---|---|---|---|
| C1 | Python/pandas | groupby/merge/window logic without bugs | P1 | `05_coding/01_python_for_validation.md`, harness P01/P02/P10/P11 | ☐ | ☐ |
| C2 | Metrics from scratch | KS, Gini, PSI, WoE/IV, HL, binomial/Jeffreys | P1 | harness P03–P08 | ☐ | ☐ |
| C3 | Modeling in Python | LR by MLE, interpretation, calibration, GBM challenger | P2 | harness P09, demo | ☐ | ☐ |
| C4 | SQL | performance windows, roll rates, vintages, deciles/KS, PSI, top-N, anti-joins | P1 | `05_coding/02_sql_for_credit_risk.md`, harness S01–S10 | ☐ | ☐ |
| C5 | SAS | data step traps, PROCs, PSI/KS macros | P2 | `05_coding/03_sas_essentials.md` | ☐ | ☐ |
| C6 | Code review | spot bugs in validation code | P2 | interviewer-generated | ☐ | ☐ |
| C7 | Time-series diagnostics | ADF/KPSS, HAC, BG, dynamic back-test | P2 | `05_coding/code/stress_test_diagnostics.py` | ☐ | ☐ |

## Module 7 — Role-specific (P3)
| Code | Topic | Study |
|---|---|---|
| T17 | Fraud & AML model validation | `01_foundations/03_ml_for_credit_risk.md` §8b |
| T18 | Probability & quant screen | `06_interview_bank/07_probability_quant_screen.md` |
| — | Market/counterparty risk validation | on request, only if a JD needs it |

---

## When are you "interview-ready"?
- [ ] All **P1 topics** at 🟢 (latest ≥ 75 and previous ≥ 70) in `skills_matrix.md`
- [ ] **C2 and C4** coding mocks ≥ 70 with hidden tests passing
- [ ] **One full process** cleared through R7 at the VP/Lead bar
- [ ] Project P1 (validation report) finished and on your resume/LinkedIn
- [ ] No open **Critical** gaps in `gap_log.md`
