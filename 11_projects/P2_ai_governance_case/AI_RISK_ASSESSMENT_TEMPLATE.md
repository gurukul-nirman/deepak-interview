# AI Risk Assessment — [Use-case name]

> **How to use:** copy to `report/AI_RISK_ASSESSMENT.md` and replace every `[…]`. Guidance is in *italics*; delete it
> when you finish. Target length: 6–10 pages. Label legal and regulatory statements **[Certain] / [Likely] / [Assumption]**.
> Your conclusion must follow from your evidence.
> **Disclaimer (keep it):** *Personal portfolio case; fictional bank, vendor and data. Not legal advice.*

| Field | Value |
|---|---|
| Use case / ID | […] |
| Business owner | […] |
| Assessor | [Your name] — AI risk / model risk (second line) |
| Date | […] |
| Decision requested | […] |
| Jurisdictions | […] |
| Inherent risk tier → residual (after conditions) | [… → …] |
| **Recommendation** | [Approve · Approve with conditions (scope-limited) · Do not approve] |

---

## 1. Executive summary
*Six to eight sentences: what the tool does, why the business wants it, the three biggest risks (with pilot evidence),
your recommendation, and the conditions that change the risk.*

[…]

## 2. Use-case description (as assessed — correct the intake form where it is wrong)
- **Purpose and users:** […]
- **Decisions influenced (directly / indirectly):** […]
- **Inputs (data categories, sources, who supplies them):** […]
- **Outputs and where they go:** […]
- **Architecture and AI value chain (foundation model → vendor → bank):** […]
- **Volumes and rollout plan:** […]

## 3. Classification and scope
*Answer each question with your reasoning and a confidence label.*

| Question | Answer and reasoning | Confidence |
|---|---|---|
| Is any component a **model** under the bank's MRM policy (quantitative output used in decisions)? | […] | […] |
| Is it an **AI system** under the bank's AI policy? | […] | […] |
| **India:** RBI FREE-AI expectations; DPDP Act 2023 / Rules 2025; credit-information rules | […] | […] |
| **EU (Amsterdam):** AI Act role (provider or deployer?) and risk class; GDPR | […] | […] |
| **Singapore:** MAS expectations (FEAT; AI risk-management guidelines status); PDPA | […] | […] |
| **US:** does SR 26-2 apply? | […] | […] |

## 4. Inherent risk tiering
| Dimension | Rating (L / M / H) | Rationale |
|---|---|---|
| Decision materiality (credit exposure, customer impact) | […] | […] |
| Autonomy and human reliance (how much does the human actually check?) | […] | […] |
| Data sensitivity (personal, bureau, confidential) | […] | […] |
| Complexity and opacity (third-party foundation model, RAG, agents) | […] | […] |
| Regulatory exposure | […] | […] |
| Scale (volume, number of users, jurisdictions) | […] | […] |
| **Inherent tier** | **[…]** | […] |

## 5. Risk identification

### 5.1 GenAI risks (NIST AI 600-1)
*Use the risks that apply. Each row needs a concrete mechanism in this use case and, where it exists, pilot evidence.*

| NIST AI 600-1 risk | How it arises here | Pilot evidence | Inherent rating |
|---|---|---|---|
| Confabulation | […] | […] | […] |
| Data privacy | […] | […] | […] |
| Information integrity | […] | […] | […] |
| Information security | […] | […] | […] |
| Harmful bias and homogenisation | […] | […] | […] |
| Human–AI configuration | […] | […] | […] |
| Value chain and component integration | […] | […] | […] |
| Intellectual property / other | […] | […] | […] |

### 5.2 Application-security view (OWASP Top 10 for LLM Applications, 2025)
| OWASP item | Exposure in this design | Control needed |
|---|---|---|
| LLM01 Prompt injection (direct and indirect) | […] | […] |
| LLM02 Sensitive information disclosure | […] | […] |
| LLM03 Supply chain | […] | […] |
| LLM05 Improper output handling | […] | […] |
| LLM06 Excessive agency | […] | […] |
| LLM08 Vector and embedding weaknesses | […] | […] |
| LLM09 Misinformation | […] | […] |
| *(others if relevant)* | […] | […] |

### 5.3 Other risks
Third-party and outsourcing; cross-border data transfer; explainability and customer rights; conduct and fairness;
operational resilience; cost.
[…]

## 6. Assessment of the business's claims
*Quote each claim in the intake form, vendor sheet or pilot report that you disagree with, and say why. This section shows
effective challenge.*

| Claim | Assessment | Evidence / criteria |
|---|---|---|
| "[…]" | […] | […] |

## 7. Controls (required before / after go-live)
| # | Control | Type (preventive / detective / corrective) | Addresses risk | Owner | Before go-live? |
|---|---|---|---|---|---|
| 1 | […] | […] | […] | […] | […] |

## 8. Testing and validation plan
| Test | Method | Metric and threshold | Sample | Owner |
|---|---|---|---|---|
| Numeric extraction accuracy | […] | […] | […] | […] |
| Faithfulness / hallucination on the bank's documents | […] | […] | […] | […] |
| Prompt-injection red-team (documents and portal) | […] | […] | […] | […] |
| Cross-application leakage | […] | […] | […] | […] |
| Grade suggestion (if retained) — validated as a rating model | […] | […] | […] | […] |
| Bias / segment performance (sector, region, language) | […] | […] | […] | […] |
| Human-review effectiveness (automation bias) | […] | […] | […] | […] |
| Vendor version change — regression suite | […] | […] | […] | […] |

## 9. Monitoring and KRIs
| KRI | Frequency | Green / Amber / Red | Escalation |
|---|---|---|---|
| […] | […] | […] | […] |

**Incident management and kill switch:** […]

## 10. Recommendation, conditions and residual risk
*State the decision, the scope it covers, and each condition with an owner and date. Say what stays out of scope (and why),
and the residual tier once the conditions are met.*

| # | Condition | Owner | Due |
|---|---|---|---|
| C1 | […] | […] | […] |

**Residual risk and review date:** […]

## 11. Sign-offs required
Business owner · Model Risk / AI Risk · CISO · Data Protection Officer · Compliance · Legal · Outsourcing / third-party risk
· (Amsterdam / Singapore local sign-off before those rollouts)

## Appendix
- A. Open questions for the business and the vendor
- B. Assumptions
- C. Regulatory references (with confidence labels)
