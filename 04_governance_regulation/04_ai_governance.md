# 04.4 · AI Governance for Banks — frameworks, regulation, operating model (Oct 2026)

> **Why this matters for you:** MRM teams are absorbing AI governance. In 2026 interviews you'll be asked *how a bank should govern AI*, not just how to validate a model. And SR 26-2 **excludes GenAI and agentic AI**, so banks must govern them through broader AI risk frameworks — exactly the gap interviewers probe. This file is the governance layer; validation of ML/GenAI is in `01_foundations/03_ml_for_credit_risk.md` and `03_ai_ml_genai_model_risk.md`.

---

## 1. AI governance vs model risk management vs data governance
| | **Model risk management (MRM)** | **AI governance** | **Data governance** |
|---|---|---|---|
| Question it answers | Is this model sound, validated and used correctly? | Should we use AI here at all, and under what conditions, controls and accountability? | Is the data fit for purpose, lawful, and controlled? |
| Scope | Models (incl. non-generative ML under SR 26-2) | All AI use cases incl. GenAI, agents, vendor AI, embedded AI in software | All data, incl. training/RAG data |
| Key outputs | Inventory, tiering, validation reports, findings | AI policy, use-case register, risk tiering, impact assessments, approvals, controls, monitoring, incident handling | Lineage, quality rules, ownership, privacy compliance |
| Typical owner | CRO / Head of MRM | AI governance council/committee (CRO, CDO/CDAO, CISO, DPO, Legal, Compliance, business) | CDO |

**Interview line:** "MRM is one control inside AI governance. AI governance decides whether and how a use case may proceed — including risks MRM doesn't cover well: privacy, IP, security, conduct, and agentic actions."

---

## 2. Operating model (three lines of defence for AI)
| Line | Who | Responsibilities |
|---|---|---|
| **Board & senior management** | Board risk committee; accountable executive (e.g., SMF in the UK) | Set AI risk appetite; approve AI policy; oversee high-risk use cases; receive AI risk reporting |
| **AI governance council** | CRO, CDAO/CDO, CISO, DPO, Legal, Compliance, Model Risk, business heads | Approve high-risk use cases; resolve escalations; maintain standards |
| **1st line** | Use-case owner, developers, product, operations | Register use case, impact assessment, build/test, human oversight, monitoring, incidents |
| **2nd line** | Model risk / AI risk, Compliance, Privacy, Information Security, Operational Risk | Independent challenge & validation; policy; risk tiering oversight; testing standards |
| **3rd line** | Internal audit | Assess whether AI governance is designed and operating effectively |

**RACI tip:** the business owner is **accountable** for the outcome; developers are **responsible** for build/testing; second line **consulted** and challenges; the council **approves** high-risk use.

---

## 3. Policy stack
1. **AI policy** (board-approved): principles, scope, roles, risk appetite, prohibited uses, approval tiers.
2. **AI risk management standard:** inventory, tiering, impact assessment, lifecycle gates, testing standards, monitoring, incidents.
3. **GenAI acceptable-use policy** for staff: approved tools only, no confidential/personal data in public tools, human review of outputs, disclosure rules.
4. Linked policies: model risk, data/privacy, information security, third-party risk, conduct/fair lending, records retention.

---

## 4. AI inventory (use-case register) — fields
Use case & business purpose · owner · AI type (traditional ML / GenAI / agentic) · build vs buy (vendor, foundation model, version) · data used (personal? sensitive? RAG sources) · decision impact (advisory vs automated; customer-facing?) · human oversight design · jurisdictions & regulatory classification (e.g., EU AI Act high-risk?) · **risk tier** · impact assessments done · validation/testing status · controls & guardrails · monitoring metrics · incidents · approval date & review date · retirement date.

> Incomplete AI inventories (especially AI embedded in vendor tools and "shadow AI") are a recurring supervisory concern (e.g., PRA observations). **[Likely]**

---

## 5. Risk tiering of AI use cases (example matrix)
Score each dimension 1 (low) – 3 (high):
| Dimension | 1 | 3 |
|---|---|---|
| **Decision impact** | Internal productivity | Consequential decisions on people (credit, pricing, hiring) |
| **Autonomy** | Human makes the decision | Fully automated / agent can act |
| **Customer exposure** | Internal only | Direct customer interaction |
| **Data sensitivity** | Public/non-personal | Personal/sensitive/confidential |
| **Opacity & novelty** | Simple, well-understood | Opaque, novel (LLM, agents) |
| **Scale** | Small user base/exposure | Enterprise-wide, high volume |
| **Regulatory classification** | None | High-risk (e.g., EU AI Act credit scoring) |

Tier 1 (high) = total ≥ 16 or any "3" on decision impact + autonomy; Tier 2 = 11–15; Tier 3 ≤ 10. **[Assumption — illustrative thresholds]** Tier drives: approval level, depth of testing/validation, monitoring frequency, review cadence.

---

## 6. Lifecycle controls (gates)
```
Intake/registration → Risk tiering → Impact assessment (AI impact / DPIA / EU FRIA where required)
 → Design requirements (fairness, explainability, oversight, security, privacy)
 → Build & developer testing → Independent validation/testing (tier-based)
 → Approval (owner → 2nd line → council for Tier 1) → Deployment with guardrails & access control
 → Monitoring (performance, drift, fairness, incidents, user feedback) → Change management → Periodic review → Retirement
```
**Change triggers:** new data source, new population, new vendor model version, prompt/RAG changes for GenAI, expanded autonomy/tools for agents, regulatory change.

---

## 7. Risk areas and typical controls
| Risk | Typical controls |
|---|---|
| **Fairness / bias** | Prohibited features & proxy review; disparity testing (e.g., adverse impact ratio); mitigation; documented trade-offs; periodic re-testing |
| **Explainability & transparency** | Explanation standards by tier; reason codes for adverse decisions; customer disclosure of AI use; model cards |
| **Human oversight** | Human-in-the-loop (approves each decision), on-the-loop (monitors, can intervene), in-command (sets limits); override rights and logs; avoid automation bias with training & sampling |
| **Privacy** | Lawful basis/consent, minimisation, retention, DPIA; India **DPDP Act 2023 + DPDP Rules 2025** (phased: Nov 2025 → Nov 2026 → May 2027); GDPR Art. 22 for automated decisions in the EU |
| **Security** | Threat modelling; **OWASP Top 10 for LLM Apps (2025)**: prompt injection, sensitive information disclosure, supply chain, data & model poisoning, improper output handling, excessive agency, system prompt leakage, vector/embedding weaknesses, misinformation, unbounded consumption |
| **Reliability / hallucination** | Grounding (RAG), evaluation on golden sets, confidence thresholds, human review, output filters |
| **Third-party / foundation models** | Due diligence (training data, evaluations, security, data use/retention, location), contractual rights (audit, notification of model changes), version pinning, exit plans, concentration risk |
| **IP & content** | Licensing checks, output filters, provenance |
| **Agentic AI** | Least-privilege tool permissions, sandboxing, spend/step limits, human approval for high-impact actions, full action logs, kill switch |
| **Operational resilience** | Fallbacks when the AI service fails; incident response; capacity limits |

---

## 8. Frameworks and standards (know what each is for)
| Framework | What it is | Remember |
|---|---|---|
| **NIST AI RMF 1.0** (Jan 2023, voluntary, US) | Risk-management framework | Four functions **GOVERN · MAP · MEASURE · MANAGE**; seven trustworthiness characteristics: valid & reliable · safe · secure & resilient · accountable & transparent · explainable & interpretable · privacy-enhanced · fair with harmful bias managed |
| **NIST AI 600-1** (Jul 2024) | Generative AI profile of the RMF | **12 GenAI risks** (list below) with suggested actions mapped to the four functions |
| **ISO/IEC 42001:2023** | Certifiable AI **management system** (like ISO 27001 for AI) | Plan-Do-Check-Act, clauses 4–10; **Annex A: 38 controls in 9 objectives** |
| **ISO/IEC 23894:2023** | Guidance on AI risk management | Adapts ISO 31000 to AI |
| **ISO/IEC 42005:2025** | AI system **impact assessment** | Published May 2025 |
| **OECD AI Principles** (2019, updated 2024) | Intergovernmental principles | Basis for many national frameworks |

**NIST AI 600-1 — the 12 GenAI risks:** (1) CBRN information or capabilities · (2) confabulation ("hallucination") · (3) dangerous, violent or hateful content · (4) data privacy · (5) environmental impacts · (6) harmful bias and homogenisation · (7) human–AI configuration (e.g., automation bias) · (8) information integrity · (9) information security · (10) intellectual property · (11) obscene, degrading and/or abusive content · (12) value chain and component integration. **[Likely — the draft used slightly different names; check the final text before quoting verbatim]**

---

## 9. Regulation by jurisdiction (financial-services view)
### EU — AI Act (Regulation (EU) 2024/1689)
- **Risk classes:** prohibited (e.g., social scoring) · **high-risk** (Annex III incl. **creditworthiness assessment / credit scoring of natural persons**, life & health insurance pricing; fraud detection is excluded) · limited-risk transparency duties (chatbots, deepfakes) · minimal risk. Profiling of natural persons in Annex III areas is always high-risk. **[Certain]**
- **Roles:** provider (builds/places on market), **deployer** (uses it — e.g., a bank using a vendor score), importer, distributor.
- **High-risk provider obligations (Arts. 9–15, 17):** risk-management system, data governance, technical documentation, record-keeping/logging, transparency to deployers, human oversight, accuracy/robustness/cybersecurity, quality-management system; conformity assessment, registration, post-market monitoring, serious-incident reporting.
- **Deployer obligations (Art. 26):** use per instructions, competent human oversight, input-data relevance, monitoring, log retention, inform affected persons; **Art. 27 FRIA** — deployers of credit-scoring systems must complete a **fundamental rights impact assessment before first use**; **Art. 86** right to an explanation of individual decisions. **[Likely — summary]**
- **AI literacy (Art. 4)** has applied since **2 Feb 2025**. The AI Omnibus (Regulation (EU) 2026/1744) softened it: providers and deployers must *take measures to support the development of* AI literacy, with no specific level guaranteed. Deployers of high-risk systems must still train oversight staff (Art. 26). **[Certain]** The Omnibus also added Art. 4a, permitting special-category data processing where strictly necessary for bias detection and correction. **[Likely]**
- GPAI (foundation-model) obligations have applied since **2 Aug 2025** (GPAI Code of Practice, Jul 2025). **[Likely]**
- **Timeline:** stand-alone high-risk obligations deferred to **2 Dec 2027** (Digital Omnibus; Council approval 29 Jun 2026). **[Certain]**
- **Penalties:** up to **€35m or 7%** of global turnover (prohibited practices); **€15m or 3%** (most other obligations, incl. FRIA); **€7.5m or 1%** (misleading information). **[Likely]**
- **Banking supervisors:** ECB Guide to internal models (2025) — ML in internal models must be explainable and justify its complexity; EBA follow-up report on ML for IRB models (2023). **[Likely]**

### United States
- **SR 26-2 (Apr 2026):** applies to traditional and non-generative, non-agentic AI models; **GenAI and agentic AI out of scope** → governed under broader risk management; an interagency **RFI on MRM and AI** has been announced. **[Certain]**
- **Fair lending & adverse action:** ECOA/Reg B require specific reasons for adverse action even for complex models (CFPB Circular 2022-03). **[Certain]**
- **NIST AI RMF** is the de facto voluntary framework. State AI laws (e.g., Colorado's AI Act on "consequential decisions" incl. lending) have shifting effective dates — **verify current status** before citing.

### United Kingdom
- **PRA SS1/23** treats AI/ML models as models (tiering, validation, PMAs; SMF accountability). FCA/PRA take a principles-based, technology-neutral approach (Consumer Duty, SM&CR accountability). **[Likely]**

### Singapore
- **MAS proposed Guidelines on AI Risk Management** (consultation 13 Nov 2025 – 31 Jan 2026): four areas — board & senior-management oversight, AI risk-management systems & policies (incl. AI inventory and materiality), AI life-cycle controls, and capabilities/capacity; covers GenAI and AI agents. **Not finalised as of Aug 2026** (MAS said "soon"). An **AI Risk Management Toolkit** (MindForge, Mar 2026) gives implementation handbooks. Earlier: FEAT principles (2018) and Veritas. **[Likely]**

### India
- **RBI FREE-AI report (13 Aug 2025):** **7 Sutras** — public trust as foundation; disclosure of AI use and individuals' final authority to override AI; responsible innovation over cautionary restraint; fairness, equity and inclusion; accountability of deploying entities; understandable by design; safe, sustainable and resilient — and **26 recommendations under 6 strategic pillars** (innovation enablement + risk mitigation). Key recommendations: **board-approved AI policies**, **AI inventories** (and a sector repository), **graded liability/supervisory approach**, **AI incident reporting and audits**, **AI disclosures in annual reports**, AI sandbox, financial-sector data infrastructure as DPI, indigenous sector models. **[Certain on Sutras/structure; Likely on pillar names]**
- **RBI draft MRM guidance (24 Jun 2026):** covers all models incl. AI/ML and third-party; board-approved MRM framework; explainability and human oversight for AI decisions; GenAI safeguards. **[Likely]**
- **DPDP Act 2023 + Rules 2025** (phased to May 2027) for personal data in AI.

### Canada
- **OSFI E-23** (effective 1 May 2027): enterprise MRM explicitly including AI/ML. **[Certain]**

---

## 10. GenAI-specific governance (what a bank should have)
1. Approved-tool list and staff acceptable-use policy (stop "shadow AI").
2. Use-case intake with tiering; customer-facing GenAI = high tier by default.
3. Vendor/foundation-model due diligence and contract terms (data use, retention, change notification).
4. Evaluation standards: golden datasets, faithfulness/hallucination metrics, red-teaming, bias tests.
5. Guardrails: input/output filtering, PII redaction, grounding, refusal policies.
6. Human review rules and disclosure to customers.
7. Logging, monitoring, incident response, version pinning, rollback.
8. Agentic AI: permissions, sandboxing, approvals, kill switch.

---

## 11. AI governance KRIs (what goes to the board)
% of AI use cases inventoried and tiered · % of high-risk use cases with completed impact assessments and independent testing · overdue reviews · AI incidents (count, severity) · fairness-test breaches · drift alerts unresolved · shadow-AI detections · vendor model changes without re-assessment · time-to-approve (to show governance isn't blocking value).

---

## 12. Interview questions (with the core of the answer)
1. **How would you set up AI governance at a bank?** Policy + council + 3LoD roles → inventory → tiering → impact assessment → lifecycle gates → testing → monitoring → incidents → reporting; proportionate by tier.
2. **AI governance vs MRM?** §1.
3. **How do you tier AI use cases?** §5 dimensions; tier drives approvals, testing, monitoring.
4. **SR 26-2 excludes GenAI — so who governs a GenAI chatbot?** The AI governance framework, with MRM-style evidence standards; legal/compliance/infosec/privacy involved; Tier by customer exposure.
5. **What does the EU AI Act require from a bank using a vendor credit-scoring model?** Deployer duties (Art. 26), FRIA before first use (Art. 27), human oversight, logging, informing applicants, explanation rights (Art. 86); obligations apply from 2 Dec 2027.
6. **NIST AI RMF in one breath?** Govern, Map, Measure, Manage; seven trustworthiness characteristics; GenAI profile adds 12 risks.
7. **ISO 42001 vs NIST AI RMF?** Certifiable management system vs voluntary risk framework; complementary.
8. **What's in an AI inventory?** §4.
9. **How do you manage third-party AI risk?** Due diligence, contracts (audit, change notice, data use), local testing, version pinning, monitoring, exit plan.
10. **How do you prevent shadow AI?** Approved tools, acceptable-use policy, technical blocks/DLP, training, an easy intake path.
11. **What is human-in-the-loop vs on-the-loop?** Approves each decision vs supervises with ability to intervene.
12. **How do you govern agentic AI?** Least privilege, sandbox, limits, human approval for high-impact actions, logs, kill switch.
13. **What did RBI's FREE-AI propose?** 7 Sutras; 26 recommendations; board AI policy, inventories, incident reporting, disclosures, graded liability, sandbox.
14. **What's an AI incident?** An AI-caused harm or near miss (wrong customer outcome, data leak, harmful output) → logged, triaged, root-caused, reported per policy (FREE-AI recommends incident reporting).
15. **How do you balance governance and innovation?** Proportionality by tier, fast-track for low-risk, sandboxes, reusable controls, clear SLAs.
16. **What would you put in a board AI-risk report?** §11 KRIs + top risks + decisions needed.

---

## 13. Career angle
AI risk & governance roles inside MRM/second line are growing (e.g., GenAI validation teams at large banks). Your credit-model validation background + this governance layer is a credible path; hands-on GenAI evaluation experience is the gap to close over 12–18 months. **[Assumption]**

## Sources
[Fed SR 26-2](https://www.federalreserve.gov/supervisionreg/srletters/SR2602.pdf) · [OCC on revised MRM guidance & AI RFI plan](https://www.occ.gov/news-issuances/news-releases/2026/nr-occ-2026-29.html) · [EU AI Act omnibus timeline (Gibson Dunn)](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/) · [EC AI-literacy Q&A (post-Omnibus)](https://digital-strategy.ec.europa.eu/en/faqs/ai-literacy-questions-answers) · [FPF on the AI Omnibus timeline](https://fpf.org/blog/the-ai-act-implementation-timeline-what-changes-under-the-ai-omnibus/) · [Freshfields on FRIA](https://technologyquotient.freshfields.com/post/102j941/eu-ai-act-unpacked-6-fundamental-rights-impact-assessment) · [RBI FREE-AI press release](https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=61018) · [Khaitan & Co FREE-AI summary](https://www.khaitanco.com/sites/default/files/2025-08/Ergo%20-%20FREE%20AI%20Framework%20-%2028%20Augusut%202025.pdf) · [MAS AI RM consultation (Bird & Bird)](https://www.twobirds.com/en/insights/2026/singapore/mas-consults-on-proposed-guidelines-on-artificial-intelligence-risk-management) · [MAS AI RM toolkit](https://www.mas.gov.sg/news/media-releases/2026/mas-partners-industry-to-develop-ai-risk-management-toolkit-for-the-financial-sector) · [NIST AI 600-1](https://airc.nist.gov/docs/NIST.AI.600-1.GenAI-Profile.ipd.pdf) · [ISO/IEC 42005 (CMS)](https://cms.law/en/gbr/legal-updates/iso-iec-42005-2025-a-new-blueprint-for-legal-and-commercial-leaders-navigating-ai-risk-and-governance) · [ISO 42001 Annex A overview](https://certpro.com/hub/iso-42001/controls/iso-42001-controls-list/) · [DPDP Rules 2025 (AZB)](https://www.azbpartners.com/bank/indias-digital-personal-data-protection-act-phased-rollout-and-key-compliance-milestones/)
