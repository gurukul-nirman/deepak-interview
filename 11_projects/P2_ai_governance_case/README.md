# P2 · AI-governance case: risk assessment of a GenAI credit-memo assistant

**What you do:** act as the second-line AI / model-risk reviewer for "CreditCopilot". This is a GenAI tool a fictional
bank (Kestrel Bank, India HQ, with Amsterdam and Singapore branches) wants to roll out for SME credit memos. You:
1. Read the business's submission.
2. Challenge its claims.
3. Classify the use case across jurisdictions.
4. Identify risks and controls.
5. Design a testing plan.
6. Make an approval recommendation with conditions.

**Why it matters for you:**
- AI governance is the fastest-growing part of MRM. JDs at the ≥ ₹40L level increasingly ask for it, and you have no
  work exposure yet.
- This case gives you a concrete, defensible story covering:
  - RBI FREE-AI;
  - EU AI Act (provider vs deployer, high-risk scoping, FRIA);
  - DPDP / GDPR;
  - NIST AI 600-1;
  - OWASP LLM Top 10;
  - human-oversight design.

**Time:** about 5 hours in week 4 (`00_strategy/03_six_week_plan.md`).
**Study first:** `04_governance_regulation/04_ai_governance.md` and `04_governance_regulation/03_ai_ml_genai_model_risk.md`.

## Files
| File | What it is |
|---|---|
| `CASE_PACK.md` | The business's submission: intake form, architecture, vendor sheet, pilot report, incident notes |
| `AI_RISK_ASSESSMENT_TEMPLATE.md` | Your deliverable's structure |
| `ANSWER_KEY.md` | ⚠️ Spoiler: planted issues, model recommendation, rubric, interview kit |

## Steps
| # | Step | Time |
|---|---|---|
| 1 | Read `CASE_PACK.md` twice. On the second pass, mark every claim as **wrong**, **unsupported** or **OK** | 45 min |
| 2 | Fill template §2–§4: corrected description, classification per jurisdiction, inherent tier | 1 h |
| 3 | Fill §5–§6: risks (NIST AI 600-1, OWASP) tied to case evidence, and the claims you challenge | 1 h 15 min |
| 4 | Fill §7–§10: controls, testing plan, KRIs, recommendation and conditions | 1 h 15 min |
| 5 | Write the executive summary last. Then self-score against `ANSWER_KEY.md` §1 and log misses in `09_progress/gap_log.md` | 30 min |
| 6 | Ask Claude `REVIEW PROJECT P2`. Rehearse the 60-second pitch and the drill-downs | 30 min |

Save your work as `report/AI_RISK_ASSESSMENT.md` in this folder.

## Rules
- **Fictional case** — say so whenever you present it. Don't add real bank or vendor names.
- **Label confidence** on every legal or regulatory statement. AI regulation moves fast: re-check any date or status
  before an interview (the repo's facts are as of Oct 2026).
- **Publish** (optional, after a self-score ≥ 85) as a PDF in the same public repo as P1, or as a LinkedIn article
  summarising your approach. Keep the answer key private.

## Where it pays off in interviews
- "How would you govern a GenAI use case?"
- "Is an LLM a model under SR 11-7 / SR 26-2?"
- "How do you validate an LLM?"
- "What does the EU AI Act require of a bank?"
- "Human-in-the-loop — is it enough?"
- Topic interviews T09 and T14, and the AI-governance threads in senior-leader rounds.
