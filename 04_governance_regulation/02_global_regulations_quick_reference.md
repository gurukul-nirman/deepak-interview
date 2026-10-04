# 04.2 · Global Regulations — Quick Reference (status as of Oct 2026)

> Learn the **one-line summary** and **interview line** for each. Go deep only on the ones your target employer's regulator uses: US banks → SR 26-2/SR 11-7, CCAR, CECL · UK banks → PRA SS1/23, IRB · EU banks → ECB guide, EBA GLs · Canadian → OSFI E-23 · Indian lenders → RBI · UAE → CBUAE.

---

## 1. Summary table
| Regulation | Jurisdiction | Status / key dates | One-liner |
|---|---|---|---|
| **SR 26-2** (+ OCC 2026-13, FDIC FIL-15-2026) | US | Issued **17 Apr 2026**; replaces SR 11-7 | Principles-based, risk-tiered MRM; narrower model definition; GenAI/agentic AI out of scope |
| **SR 11-7 / OCC 2011-12** | US | 2011 → **rescinded Apr 2026** | The foundational MRM guidance; vocabulary still everywhere |
| **PRA SS1/23** | UK | Published May 2023; **effective 17 May 2024** | Five MRM principles for banks with internal-model approval; SMF accountability; PMA governance |
| **ECB Guide to internal models** | Euro area (SSM) | **Revised 28 Jul 2025** | New "overarching principles" chapter (MRM framework, data governance, **ML in internal models**); CRR3 alignment |
| **EBA Guidelines** | EU | GL/2017/16 (PD/LGD), GL/2016/07 (DoD), GL/2019/03 (downturn LGD), GL/2020/06 (loan origination & monitoring) | Detailed IRB estimation and default rules; automated-model expectations in origination |
| **OSFI E-23** | Canada | Final **11 Sep 2025**; **effective 1 May 2027** | Enterprise-wide MRM for all federally regulated FIs; broad model definition explicitly incl. AI/ML |
| **RBI draft MRM guidance** | India | Draft **24 Jun 2026**; comments closed 24 Jul 2026; final pending | Board-approved MRM framework for all REs (banks, NBFCs, etc.), all models incl. third-party and AI/ML |
| **RBI ECL directions** | India | Final **27 Apr 2026**; **effective 1 Apr 2027** | Three-stage ECL for commercial banks with prudential floors and MRM for ECL models |
| **EU AI Act** (Reg. 2024/1689) | EU | In force Aug 2024; high-risk obligations for stand-alone systems (incl. **credit scoring of natural persons**) deferred to **2 Dec 2027** (Digital Omnibus; Council approval 29 Jun 2026) | Risk management, data governance, documentation, logging, transparency, human oversight, accuracy/robustness for high-risk AI |
| **MAS AI Risk Management Guidelines** | Singapore | Consultation 13 Nov 2025 – 31 Jan 2026; final pending | Supervisory expectations for AI oversight, AI inventories, life-cycle controls across all FIs |
| **CBUAE Model Management Standards & Guidance** | UAE | 2022 **[Likely]** | Comprehensive model-management expectations for UAE banks (IFRS 9-heavy market) |
| **Basel III final ("3.1")** | Global / UK / EU / US | EU CRR3 from Jan 2025; UK from 1 Jan 2027 **[Likely]**; US pending | Output floor 72.5%, IRB input floors |
| **NIST AI RMF 1.0** (+ GenAI profile) | US (voluntary) | Jan 2023; GenAI profile Jul 2024 | Govern · Map · Measure · Manage |
| **ISO/IEC 42001** | Global (certifiable) | Dec 2023 | AI management system standard |

---

## 2. PRA SS1/23 (UK) — the five principles
**Scope:** UK-incorporated banks, building societies and PRA-designated investment firms with internal-model approval for regulatory capital (IRB, IMA, IMM); proportionate application expected. **[Certain]**

| Principle | Key expectations |
|---|---|
| **1. Model identification & risk classification** | Clear (broad) model definition; complete inventory; risk-based **tiering** (materiality + complexity) |
| **2. Governance** | Board-approved MRM policy; **SMF (senior manager) accountable** for the MRM framework; model risk appetite; reporting |
| **3. Development, implementation & use** | Development standards; data quality; testing; documentation; use within limits |
| **4. Independent model validation** | Independent review incl. conceptual soundness, outcomes, process verification; periodic revalidation; validation of changes |
| **5. Model risk mitigants** | Policies for **post-model adjustments (PMAs)** with independent review; restrictions on use; procedures for models used pending validation |

**Interview line:** "SS1/23 is the UK's first standalone MRM supervisory statement — it formalises SMF accountability, model tiering, and PMA governance, and applies to IRB/IMA/IMM firms since May 2024. For a UK group entity, SR 26-2 doesn't reduce these expectations."
**Recent:** PRA held an MRM roundtable on AI/ML (Nov 2025); supervisors have flagged inconsistent tiering and incomplete AI inventories as industry gaps. **[Likely]**

---

## 3. ECB / EBA (EU)
- **TRIM (2016–2021)** harmonised internal-model supervision; the **ECB Guide to internal models** is the living reference — **2025 revision** adds an *overarching principles* chapter (MRM framework, data governance) and expectations that **ML-based internal models be adequately explainable and that performance justifies complexity**. **[Certain]**
- **EBA GLs you should name:** PD/LGD estimation & defaulted exposures (GL/2017/16 — incl. **MoC categories A/B/C**), definition of default (GL/2016/07), downturn LGD (GL/2019/03), loan origination & monitoring (GL/2020/06 — governance of automated credit-decision models).
- **Validation reporting:** ECB 2019 instructions (Jeffreys test, AUC change, LGD/CCF t-tests, gAUC) — see `02_credit_risk/03_basel_irb.md` §10.

---

## 4. OSFI E-23 (Canada)
- Final **11 Sep 2025**, effective **1 May 2027** (18-month transition). **[Certain]**
- Applies to federally regulated financial institutions — banks, insurers, trust & loan companies, foreign bank branches. **[Certain]**
- **Broadened model definition**, explicitly including **AI/ML**; risk-based, enterprise-wide MRM across the model lifecycle; inventory; governance and accountability. **[Certain]**
- **Interview line:** "Unlike SR 26-2, which carves GenAI out, OSFI E-23 pulls AI/ML squarely into the model definition — so Canadian banks are building AI validation capacity now."

---

## 5. RBI (India) — two 2026 milestones
**(a) Draft Guidance on Regulatory Principles for Model Risk Management (24 Jun 2026)** **[Certain on issuance/scope; Likely on details from law-firm summaries]**
- Applies to **11 categories of regulated entities**: commercial banks, small finance banks, payments banks, local area banks, regional rural banks, urban & rural co-operative banks, AIFIs, **NBFCs**, ARCs, credit information companies.
- Covers **all models** — internal, third-party and **AI/ML**.
- Expects a **board-approved MRM framework**, model inventory, **independent validation**, explainability and **human oversight** for AI-driven decisions (e.g., loan approvals, fraud), safeguards for customer-facing GenAI, and clear accountability even when models are outsourced.
- Lineage: Aug 2024 draft on *model risks in credit* → **FREE-AI** committee report (13 Aug 2025) → this draft.

**(b) ECL directions (27 Apr 2026; effective 1 Apr 2027)** — see `02_credit_risk/02_ifrs9_cecl_rbi_ecl.md` §7.

**Interview line:** "India is moving from rule-based provisioning to ECL in April 2027 and has a draft MRM framework covering AI — so independent validation capacity is being built across banks and NBFCs for the first time at scale."

---

## 6. EU AI Act — what a credit validator needs
- **High-risk (Annex III):** AI used to evaluate **creditworthiness / establish credit scores of natural persons** (fraud detection excluded). **[Certain]**
- **Obligations (providers/deployers):** risk-management system, **data governance** (representative, bias-examined data), technical documentation, logging, transparency to deployers, **human oversight**, accuracy/robustness/cybersecurity, post-market monitoring; deployers may need a fundamental-rights impact assessment. **[Likely — summary]**
- **Timeline:** in force Aug 2024 → prohibitions Feb 2025 → GPAI obligations Aug 2025 → **stand-alone high-risk: 2 Dec 2027** (after the Digital Omnibus deferral). **[Certain]**

---

## 7. MAS (Singapore)
- Consultation on **Guidelines on AI Risk Management** (13 Nov 2025 – 31 Jan 2026): board/senior-management oversight, AI inventories and risk materiality, life-cycle controls, capabilities; applies to **all FIs**. Final pending as of Oct 2026. **[Certain on consultation; Likely on status]**
- Earlier: FEAT principles (fairness, ethics, accountability, transparency) and the Veritas toolkit. **[Likely]**

---

## 8. One-line answers to "which regulation applies?"
- *US bank GCC in Bengaluru validating CCAR models?* SR 26-2 (formerly SR 11-7), Fed capital plan rule/stress testing rules, CECL.
- *UK bank (e.g., Barclays/HSBC UK entity) IRB validation?* PRA SS1/23 + UK IRB rules (and Basel 3.1 from 2027).
- *EU bank (DB/SocGen/BNP) IRB validation?* ECB Guide to internal models (2025) + EBA GLs + CRR3.
- *Indian bank ECL model validation?* RBI ECL directions (2026) + RBI MRM guidance (draft 2026).
- *UAE bank IFRS 9 model validation?* IFRS 9 + CBUAE model management standards.
- *AI credit-scoring model for EU consumers?* EU AI Act high-risk obligations (from Dec 2027) + MRM framework.
