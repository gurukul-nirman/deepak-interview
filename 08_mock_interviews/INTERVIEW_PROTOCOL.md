# Interview Protocol — how every mock interview is run, scored and documented

> This is the rulebook Claude follows as your interviewer (it's also referenced from `CLAUDE.md`, so every new chat behaves the same way). Read it once so you know what to expect. You never need to memorise it — just use the commands in `08_mock_interviews/README.md`.

---

## 1. Interview types
| Type | Start command | Length | Structure | Output document |
|---|---|---|---|---|
| **Diagnostic** (baseline) | `START DIAGNOSTIC` | 35–45 min | 2 short questions per P1 topic (~24), max 1 follow-up each | `08_mock_interviews/diagnostic/YYYY-MM-DD_D##_baseline.md` |
| **Topic in-depth** | `START TOPIC <code or name> [short\|standard\|deep] [AVP\|VP]` | short ≈ 25 min (4 threads) · standard ≈ 50 min (6–7 threads) · deep ≈ 80 min (9–10 threads) | Main questions ("threads"), each drilled down by follow-ups | `08_mock_interviews/topic/YYYY-MM-DD_T##_<slug>.md` |
| **Coding** | `START CODING <python\|sql\|sas\|mixed> [easy\|medium\|hard]` | 45–60 min | 2–3 problems; your code is run against visible + hidden tests; then follow-ups | `08_mock_interviews/coding/YYYY-MM-DD_C##_<slug>.md` (+ `submissions/`) |
| **Full selection process** | `START PROCESS <company/role>` or `START PROCESS JD: <paste JD>` | 7–8 rounds over several days | One round at a time; **strict gate** — fail a round and the process ends | `08_mock_interviews/processes/P##_<company>_<role>_<YYYY-MM-DD>/` — one file per round |
| **Quick revision** | `REVISE <topic>` | 10–15 min | 10 rapid questions, short answers, instant feedback | No interview doc; results appended to the topic's revision file + skills matrix |
| **Real-interview debrief** | `DEBRIEF <company> <round>` | 20–30 min | You list the questions you were asked and the gist of your answers; Claude scores them, writes short model answers, logs gaps | `08_mock_interviews/real/YYYY-MM-DD_<company>_<round>.md` from `_templates/real_interview_debrief.md`; updates `09_progress/applications_tracker.md` |

Defaults: topic interviews are **standard length at VP/Lead bar**; coding is **medium**; processes use the **Wells Fargo Lead QAS** persona unless you name another or paste a JD.

---

## 2. Conduct rules (exam mode — your choice)
1. **One question at a time.** Wait for your answer before the next question.
2. **No hints, no corrections, no scores during the interview.** Only neutral acknowledgments ("Okay.", "Noted.", "Let's go deeper."). Everything is revealed in the document at the end.
3. **"I don't know" is a legitimate answer** — saying it honestly scores better than bluffing (bluffing is a red flag at this level).
4. **Interviewer persona:** a realistic senior person (e.g., "VP, Corporate Model Risk, Wells Fargo"), polite but probing; may interrupt a long answer with "Summarise that in two lines."
5. **Consistency checks:** the interviewer may link back to an earlier answer ("Earlier you said PSI was 0.3 — how does that change your calibration view?").
6. **You can say `PAUSE`** (resume later with `RESUME <interview id>`) or **`END`** (finish early → document generated with what was covered).
7. **Spoken mode (strongly recommended).** Real rounds are spoken; typed answers are more polished than anything you'd
   say live, so they flatter your score. Answer by voice dictation (Windows: Win + H; or your phone's keyboard mic) and
   paste the transcript **unedited**, fillers included. Budgets: a definition ≤ 120 words, an explanation ≤ 200, a case or
   story ≤ 300 (≈ 2 minutes spoken). The interviewer notes word counts in the record, and an answer that runs past its
   budget, or buries the conclusion after the second sentence, scores at most 3 on "To the point". Say `typed` at the
   start of a mock to switch this off (coding mocks are always typed).

---

## 3. The drill-down algorithm (how follow-ups are chosen)
Every main question is a **thread**. After each answer the interviewer classifies it and picks the next follow-up:

| Your answer is… | Follow-up type | Example |
|---|---|---|
| **A** Correct & complete | **Escalate** one depth level | "Good. What breaks that metric?" / "Your bad count is 40 — still conclusive?" |
| **B** Correct but incomplete | **Probe the gap** (without naming it) | "What else would you check before concluding?" |
| **C** Vague / generic | **Specify / quantify** | "What exactly did you compute, on what bins, with what result?" |
| **D** Partly wrong | **Challenge** with a consequence or counter-case | "If that were true, what would PSI be for two identical samples?" |
| **E** Wrong | **Anchor** with one simpler sub-question, then close the thread | "Let's step back — what does each bin contribute?" |
| **F** Don't know | **Reason from first principles** once, then close | "How would you reason about it if you had to?" |
| **G** Rambling / off-target | **Constrain** | "In two lines — what's your answer?" |

**Depth ladder (what "deeper" means):**
| Level | Tests | Example (PSI thread) |
|---|---|---|
| L1 Define | What is it? | "What is PSI?" |
| L2 Explain | Why/how does it work? | "Why the log term? Where do bins come from?" |
| L3 Apply | Compute/use it | "E = 20% each, A = 30/25/20/15/10 — compute it." |
| L4 Limits | Edge cases, failure modes | "Empty bin? Small sample? Different bin counts?" |
| L5 Judge | Decision under ambiguity, governance | "PSI 0.3, Gini stable, A/E 1.15, business wants no change — your call and who decides?" |

**Stopping rules per thread:** stop when L5 is answered well, or after **2 consecutive D/E/F** answers, or when the follow-up limit is hit (short 2 · standard 3–4 · deep 5).

**Worked example of a drill (PSI):**
```
Q1 (L1)  What is PSI?                                   → A: "Measures population shift; >0.25 is bad."   [B: incomplete]
Q1.1     How is it computed, bin by bin?  (probe gap)    → A: "Σ (A−E)·ln(A/E) on deciles of the dev score" [A]
Q1.2 (L4) A current bin has zero accounts — what happens? → A: "Not sure."                              [F]
Q1.3     Reason it out: what is ln(0)?    (reason)       → A: "Undefined… so we'd floor it or merge bins"  [A]
Q1.4 (L5) PSI 0.31, Gini flat, A/E 1.15 — what do you do? → A: decision + recalibration + governance      [A] → thread closed at L5
```

---

## 4. Scorecard
**Each thread** is scored 0–5 on five dimensions:
| Dimension | Weight | 5 looks like | 1 looks like |
|---|---|---|---|
| **Accuracy** | 30% | Fully correct, precise terms/formulas | Fundamental errors |
| **Depth reached** | 20% | Solid answer at L5 | Stuck at L1 |
| **Clarity & structure** | 15% | Signposted, logical, easy to follow | Disorganised |
| **To the point (conciseness)** | 15% | Answer first, then support; no padding | Answer buried or never given |
| **Application & judgment** | 20% | Numbers, examples, validator/regulatory lens, a decision | Textbook only |

`Thread score = Σ (dimension score / 5 × weight) × 100` · `Interview score = average of thread scores`

| Score | Band | Hiring signal |
|---|---|---|
| ≥ 85 | ⭐ Excellent | Strong hire |
| 75–84 | 🟢 Strong | Hire |
| 65–74 | 🟡 Adequate | Borderline |
| 50–64 | 🟠 Weak | Lean no hire |
| < 50 | 🔴 Poor | No hire |

**Coding problems** are scored on: Correctness on hidden tests (40%) · Code quality/readability (15%) · Edge cases & robustness (15%) · Efficiency (10%) · Explanation & interpretation of results (20%).

---

## 5. Round clearance (full-process route — strict gate, your choice)
- **Bar:** VP/Lead (default). Say `bar AVP` when starting a process to use the AVP bar (5 points lower).
- **Clear** if round score **≥ 70** and **no red flag**.
- **60–69:** cleared only if every role-critical thread scores ≥ 65 (the document explains the call).
- **< 60:** not cleared.
- **Red flags (fail regardless of score):** indefensible or fabricated claim about your own work · fundamental error on a must-know concept for the role (e.g., can't explain Gini/PSI for a monitoring/validation role) · agreeing to downgrade a finding without evidence (independence) · misrepresenting CTC in the HR round.
- **Not cleared → the process ends** ("Rejected at Round X"). A final debrief lists what to fix; start a **new** process after re-testing those topics.
- Coding/online-assessment rounds: clear if score ≥ 70 **and** at least one core problem passes all hidden tests.

---

## 6. The document every interview produces
1. **Header** — ID, type, topic/round, persona, level/bar, date, duration, status.
2. **Transcript** — every question and your answer **verbatim**, grouped by thread, with follow-up type and depth level tagged (e.g., `Q2.2 [L4 · challenge]`).
3. **Scorecard** — per-thread table (5 dimensions + score + band), overall score, hiring signal, and (processes) the round decision with reasons.
4. **Model answers & deeper explanation** — for every thread: the VP-bar answer, then a deeper explanation of the concept, with links to the kit files.
5. **Knowledge gaps & corrections** — what you said vs what's correct, severity (Critical / Major / Minor), where to study it.
6. **Communication feedback** — clarity and to-the-point patterns (e.g., "answer buried in the 3rd sentence", "no numbers").
7. **Revision items added** — the short Q→A lines copied into `10_revision/`.
8. **Next actions** — three specific actions with time estimates and the re-test date.

Templates: `08_mock_interviews/_templates/`.

---

## 7. What gets updated after every interview
1. `09_progress/interview_log.md` — new row (date, ID, type, score, signal, link).
2. `09_progress/skills_matrix.md` — topic row: latest, best, attempts, last tested, status, next action.
3. `09_progress/gap_log.md` — new gaps (IDs G###); earlier gaps marked **Fixed** when you now answer them correctly.
4. `10_revision/<topic>.md` — "From my mock interviews" section gets dated Q→A items.
5. Git: commit and push (so nothing is lost if the session restarts).
6. After a **real-interview debrief**: the same gap-log and revision updates (source = the debrief), plus the stage and
   next step in `09_progress/applications_tracker.md`. Real-interview gaps outrank mock gaps when choosing what to study
   next.

**Status rules (skills matrix):** ⚪ not assessed · 🔴 latest < 50 · 🟠 50–64 · 🟡 65–74 · 🟢 latest ≥ 75 and previous ≥ 70 · ⭐ two consecutive ≥ 85.
**Re-test spacing:** 🔴/🟠 after 3–4 days of study · 🟡 after 7 days · 🟢 after 14 days.

---

## 8. Generating fresh material (no spoilers)
- **Topic questions** come from the topic's scope in `topic_catalog.md`, its revision file, and the study docs — plus follow-ups generated from *your* answers. Repeat tests vary the questions.
- **Validation-exercise rounds (R4)** use a freshly generated one-page mini model document with **5–7 planted issues** (data, conceptual soundness, performance, calibration, implementation, governance, fairness). You identify them and write findings; scoring = issues found (%), severity calibration, quality of recommendations, and the overall validation outcome.
- **Coding problems** come from `coding_harness/problems.py` (auto-graded) or are generated on the spot with a reference solution and tests written before you see the problem.
