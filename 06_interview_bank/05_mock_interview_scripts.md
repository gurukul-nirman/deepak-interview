# 06.5 · Mock Interview Scripts & Scoring Rubric

> Three mocks are scheduled in the plan (Weeks 3, 4, 5). Run them **out loud, timed, recorded**. The fastest way: ask me in chat — I'll play the interviewer, follow up like a real panel, and score you.

**Prompts to use with me:**
- `Mock 1: Technical 2 for Wells Fargo Lead QAS. Grill me on my SBSS and IFRS 9 projects, then one case. 60 minutes.`
- `Mock 2: Hiring manager at Barclays model validation (IRB/IFRS 9). Include a pushback scenario and SR 26-2.`
- `Mock 3: Full loop for AmEx Sr Manager credit risk modeling — screen, SQL/Python questions, case, HM.`
- `Rapid fire: 20 Tier-1 questions on monitoring metrics, one at a time, score each.`

---

## Mock 1 — Technical 2 (projects + domain), 60 min
| Min | Interviewer does | You must show |
|---|---|---|
| 0–3 | "Tell me about yourself." | 90-sec pitch with one number |
| 3–20 | Project deep-dive: pick SBSS or IFRS 9; ladder to level 5 (data, bad definition, metrics, thresholds, breach, root cause, approvals) | Your numbers; separation of drift types; evidence for root cause |
| 20–35 | Domain probe: SICR validation **or** IRB calibration **or** stress-test diagnostics | Correct mechanics + validator's angle |
| 35–55 | Case (pick from `03_case_studies.md`, e.g., Case 2 or 3) | SCOPE-D; findings with severity; outcome |
| 55–60 | "Questions for us?" | One SR 26-2 or AI-validation question |

## Mock 2 — Hiring manager + case, 60 min
| Min | Interviewer does | You must show |
|---|---|---|
| 0–10 | Why validation / why us / why leave | Crisp, positive, specific |
| 10–25 | "Validate our new behavioural PD model — plan your first 4 weeks" | Scoping by tier, document request, workstreams, timeline |
| 25–40 | **Pushback scenario** (Case 15) | Independence + solution path + escalation process |
| 40–50 | "What changed with SR 26-2; what would you change in our framework?" | 2-minute answer (`04_governance_regulation/01_mrm_sr11-7_to_sr26-2.md` §4) |
| 50–60 | Behavioural: conflict, mistake, mentoring | STAR-L with numbers |

## Mock 3 — Full loop, ~3.5 hours (Week 5 Saturday)
1. **Recruiter screen (15 min):** intro, CTC, notice, expected CTC script.
2. **Technical 1 (45 min):** 15 Tier-1 questions across B, C, I (LR, metrics, ML).
3. **Coding (45 min):** Timed Set 3 or 4 from `05_coding/01_python_for_validation.md` + one SQL drill.
4. **Technical 2 (60 min):** Mock 1 format on a different project.
5. **Hiring manager (45 min):** Mock 2 format, different case.

---

## Scoring rubric (score each 1–5; target ≥ 4 average by Week 5)
| Dimension | 1 (weak) | 3 (AVP bar) | 5 (VP/Lead bar) |
|---|---|---|---|
| **Technical accuracy** | Errors in basics | Correct definitions & formulas | Correct + edge cases + when it breaks |
| **Depth under follow-ups** | Breaks at level 2 | Reaches level 3–4 | Reaches level 5+, says "here's how I'd find out" at the edge |
| **Structure** | Rambling | Mostly structured | Signposted (e.g., "three things…"), concise |
| **Judgment & independence** | Metric runner | Recommends actions | Severity + governance + trade-offs + escalation path |
| **Evidence & numbers** | Vague | Some numbers | Numbers in every story; quantified impact |
| **Regulatory currency** | Quotes SR 11-7 as current | Knows main regs | SR 26-2, RBI 2026, OSFI E-23, EU AI Act timelines — applied to the employer |
| **Communication** | Jargon-heavy | Clear | Adapts to audience; one-line summaries |

## Post-mock review (10 minutes, write it down)
1. Three questions I answered best — why?
2. Three questions I fumbled — correct answer + the file/section to revise.
3. One habit to fix (filler words, no numbers, too long).
4. Add every miss to the error log; schedule into next week.
