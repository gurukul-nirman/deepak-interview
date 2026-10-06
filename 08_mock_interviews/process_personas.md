# Process Personas — realistic selection processes to simulate

> Start one with `START PROCESS <persona code or company/role>` or paste a JD (`START PROCESS JD: …`). Round structures are based on public candidate reports and typical practice **[Likely — varies by team]**; interviewers are fictional titles, not real people. All personas use the strict gate in `INTERVIEW_PROTOCOL.md` §5.

Default round set (R0–R7) is in `_templates/process_overview.md`. Personas change **emphasis, regulatory lens and quirks**.

---

## India (current priority)
| Code | Company · role | Emphasis by round | Regulatory lens | Quirks to expect |
|---|---|---|---|---|
| **WF-LQAS** *(default)* | Wells Fargo · Lead Quantitative Analytics Specialist, Corporate Model Risk (credit) | R1 Python + SQL · R2 stats/ML · R3 projects + CCAR/CECL · R4 replication & benchmarking exercise · R5 independence, auditors/regulators | SR 26-2 (formerly SR 11-7), CCAR, CECL | ML/fraud model validation questions; "would you build a challenger?"; Master's listed on JD — expect "why no Master's?" |
| **AMEX-SM** | American Express · Sr Manager, Credit & Fraud Risk (model development/risk) | R1 SQL-heavy analytics test · R2 modeling & metrics · R3 business case ("approve or decline this segment?") · R5 leadership | US regs + business economics | "How does Amex make money?"; guesstimates; P&L impact of model decisions |
| **CITI-MRM** | Citi · Model Risk Management, AVP/VP (credit models) | R2 metrics/scorecards · R3 IFRS 9/CECL/CCAR · R4 written validation memo · R5 MRM framework & AI validation | SR 26-2, OCC, CCAR, CECL | Written exercise graded on structure; GenAI validation team exists — expect an AI question |
| **JPM-MRGR** | JPMorgan · Model Risk Governance & Review, Associate/VP (credit) | R1 math/stats-heavy · R2 rigorous stats · R3 CCAR/CECL models · R5 behavioural (structured) | SR 26-2, CCAR, CECL | Proofs/derivations (MLE, Gini–AUC); probability questions; Master's/PhD-heavy team |
| **BARC-IVU** | Barclays · Independent Validation Unit, AVP/VP (IRB/IFRS 9) | R2 metrics · R3 IRB calibration, MoC, DoD · R4 IRB/IFRS 9 exercise · R5 PRA SS1/23 | PRA SS1/23, UK IRB, Basel 3.1 (2027), IFRS 9 | Expect PRA-specific questions (SMF accountability, PMAs) |
| **HSBC-MRM** | HSBC · Model Risk Management, AVP (credit/IFRS 9) | R2 stats/metrics · R3 IFRS 9 + stress · R5 governance & stakeholder | PRA SS1/23, HKMA/EU exposure, IFRS 9 | Global-team interviews in UK hours |
| **GS-MRM** | Goldman Sachs · Model Risk, Associate | R1 HackerRank (math/stats/coding) · R2–R3 back-to-back technical · R5 behavioural | SR 26-2 | Probability puzzles; speed |
| **SCB-MV** | Standard Chartered · Model Validation Manager (credit) | R3 IRB + IFRS 9 · R4 case · R5 governance | PRA SS1/23, multiple host regulators | Emerging-market data issues, LDPs |
| **DB-MRM** | Deutsche Bank · Model Risk Management, AVP (credit) | R3 IRB/ECB · R4 exercise | ECB Guide to internal models (2025), EBA GLs, CRR3 | ECB TRIM-style expectations |
| **BIG4-ECL** | Big 4 · FRM Manager (ECL/IFRS 9) | R3 ECL case for an Indian bank (RBI 2027) · R5 client-handling | RBI ECL 2026, Ind AS 109, IFRS 9 | "Explain ECL to a bank CFO"; proposal/pricing thinking |
| **FIN-LEAD** | Indian fintech/NBFC · Lead, Credit Risk Modeling | R1 Python/ML take-home-lite · R3 alternative data, bureau, GST/AA data · R5 speed vs governance | RBI digital lending, RBI MRM draft, DPDP | Heavier Python/ML; build vs validate |

## Europe (your later preference — usable now for practice)
| Code | Company · role | Emphasis | Regulatory lens |
|---|---|---|---|
| **ING-MV** | ING (Netherlands) · Model Validation, credit risk | IRB/IFRS 9 + competency-based behavioural (STAR) | ECB guide, EBA GLs, EU AI Act |
| **ABN-MV** | ABN AMRO (Netherlands) · Model Validator | IRB, ML in internal models, Python | ECB guide 2025 (ML), EU AI Act |
| **UBS-MRM** | UBS (Switzerland/Poland) · Model Risk, credit | Validation process, documentation, governance | FINMA/ECB-style, SR 26-2 for US entities |
| **UK-BANK** | Lloyds/NatWest/Barclays UK · Model Validation Manager | IRB mortgages, IFRS 9, PRA SS1/23 | PRA SS1/23, Basel 3.1 |

## Singapore
| Code | Company · role | Emphasis | Regulatory lens |
|---|---|---|---|
| **DBS-MV** | DBS · Model Validation (credit/AI) | IFRS 9 (SFRS(I) 9), ML validation, AI governance | MAS AIRM (proposed), FEAT, MAS 637 (IRB) |
| **OCBC-MRM** | OCBC/UOB · Model Risk Management | IRB + IFRS 9 + AI | MAS guidelines |

---

## Offer simulation (R7)
The offer reflects your performance across rounds **[Assumption — illustrative, India personas]**:
| Overall process score | Grade offered | Fixed (indicative) |
|---|---|---|
| ≥ 85 | VP / Lead / Band 40 | ₹42–48L |
| 75–84 | VP-lite or top-of-band AVP | ₹37–42L |
| 70–74 | AVP / Senior | ₹32–36L |
R7 then tests your negotiation (level first, fixed second, joining bonus third — see `06_interview_bank/04_behavioral_hr_negotiation.md`).
