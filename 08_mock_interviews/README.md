# Mock Interviews — how to use them

You type a command in the chat; Claude becomes the interviewer, asks one question at a time, drills into your answers, and — when the interview ends — writes a scored document with model answers and your knowledge gaps. Your progress files and revision notes update automatically.

---

## Two routes
| Route | Use it for | Commands |
|---|---|---|
| **1 · Topic / coding interviews** | Learning loop: test one topic or one coding area at a time, see gaps, fix, re-test | `START TOPIC …` · `START CODING …` · `START DIAGNOSTIC` · `REVISE …` |
| **2 · Full selection process** | Rehearse a real company's loop end-to-end, round by round, with a strict pass/fail gate | `START PROCESS …` → `NEXT ROUND` |

## Commands (copy-paste)
| You type | What happens |
|---|---|
| `START DIAGNOSTIC` | 35–45 min baseline: ~24 short questions across all P1 topics → your starting skills matrix |
| `START TOPIC T03` (or `START TOPIC monitoring metrics`) | Standard 50-min in-depth interview on that topic at VP/Lead bar |
| `START TOPIC T05 short` · `START TOPIC T09 deep AVP` | Shorter (25 min) / longer (80 min); AVP bar instead of VP |
| `START CODING python` · `START CODING sql hard` · `START CODING mixed` | 2–3 problems; your code is run against tests |
| `START PROCESS WF-LQAS` · `START PROCESS Barclays IVU AVP` · `START PROCESS JD: <paste>` | New selection process (own folder); Round 0 starts |
| `NEXT ROUND` | Start the next round of the current process (only if the last round was cleared) |
| `PAUSE` / `RESUME <interview id>` | Stop now and continue later from where you left off |
| `END` | Finish the current interview early; the document is written from what was covered |
| `REVISE T03` | 10-minute rapid refresher with instant short feedback |
| `STATUS` | Where you stand: topic statuses, recent scores, open gaps, what to do next |
| `EXPLAIN <concept>` | Teaching mode (not an interview) — e.g., `EXPLAIN Jeffreys test` |

Plain English works too ("let's do a mock on IFRS 9").

## During an interview (exam mode)
- One question at a time; follow-ups depend on your answer (see `INTERVIEW_PROTOCOL.md` §3).
- No hints, corrections or scores until the end. Saying "I don't know" is fine — bluffing is penalised.
- You may ask a clarifying question, just like in a real interview.
- For coding: paste your code in a code block; you'll see visible-test results like an online assessment; hidden tests are revealed at the end.

## After an interview you get
1. A document in `08_mock_interviews/<type>/…` with: transcript (verbatim) · scorecard (accuracy, depth, clarity, to-the-point, application) · model answers + deeper explanation · knowledge gaps & corrections · next actions.
2. Updates to `09_progress/` (interview log, skills matrix, gap log) and `10_revision/` (quick refresher items).
3. A git commit + push, so nothing is lost.

## Where things live
```
08_mock_interviews/
├── INTERVIEW_PROTOCOL.md   rules: drill-down, scoring, round clearance, outputs
├── topic_catalog.md        T01–T18 topics, C1–C7 coding areas
├── process_personas.md     company loops (India now; Europe/Singapore ready for later)
├── _templates/             document templates
├── diagnostic/  topic/  coding/  processes/   ← your interview records
└── coding_harness/         auto-grader for Python & SQL problems
```

## Keeping your history in one place
Each new chat session works on its own branch. At the end of a session, say **"open a PR to main"** (and merge it on GitHub, or tell me "merge it") so the next session starts with all your interview records and progress.
