# T14 · GenAI/LLM & agentic AI risk — quick refresher
**Study:** `04_governance_regulation/03_ai_ml_genai_model_risk.md`, `04_ai_governance.md` · **Test:** `START TOPIC T14`

## 60-second summary
- Five-pillar validation: **scope & tier → data/knowledge (RAG) → performance on golden sets (faithfulness, hallucination rate) → robustness & safety (prompt injection, bias, PII) → controls & monitoring (guardrails, human review, version pinning, drift)**.
- Agents: validate what it can **do** (permissions, tools), not just what it says.

## Quick Q → short answer
| Q | A |
|---|---|
| Measure hallucination? | Golden set + factual consistency vs sources (humans or calibrated LLM judge); report rate with CIs |
| LLM-as-judge OK? | Yes if agreement with human experts is measured and acceptable |
| Biggest customer-facing risk? | Hallucination + prompt injection |
| Vendor model updates silently? | Version pinning, change notification in contract, re-testing on change |
| NIST GenAI risks (examples)? | Confabulation, data privacy, information security, harmful bias, value-chain integration |
| Validate an LLM credit-memo summariser? | Tier (human reviews → medium), golden set with expert summaries, faithfulness of numbers/covenants, injection & PII tests, sign-off control, drift on vendor updates |

## From my mock interviews (auto-updated)
_No entries yet._
