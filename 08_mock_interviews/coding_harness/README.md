# Coding Harness — auto-graded coding interviews

21 problems (11 Python, 10 SQL) with **visible tests** (shown during the interview, like an online assessment) and **hidden tests** (edge cases, larger data, a re-seeded database) revealed afterwards. Every reference solution passes all tests; deliberately buggy solutions (PSI bins from the wrong sample, split ties in KS, wrong time window, INNER instead of LEFT join) fail — so a pass means your code is actually right.

> ⚠️ Don't open `solutions.py` before a coding mock — it contains the answers. `problems.py` contains statements and test data only.

## How a coding interview runs
1. You say `START CODING python` (or `sql`, `mixed`, plus `easy|medium|hard`).
2. Claude shows a problem statement (`python grade.py show <ID>`) — or writes a fresh problem on the spot.
3. You paste your code in the chat. Claude saves it to `08_mock_interviews/coding/submissions/<interview-id>_<ID>.py|.sql` and runs the **visible** tests: `python grade.py run <ID> <file>` → you see PASS/FAIL like HackerRank.
4. You may fix and resubmit (each attempt is recorded).
5. Follow-up questions: complexity, edge cases, "how would you test this?", "what does the number mean for the model?".
6. At the end Claude runs `--all` (hidden tests), writes the scored document and shows the reference solution.

## Commands (for practice on your own machine)
```bash
cd 08_mock_interviews/coding_harness
python grade.py list                 # all problems (or: list python / list sql)
python grade.py show P05             # statement only
python grade.py run P05 my_psi.py    # visible tests
python grade.py run P05 my_psi.py --all   # + hidden tests
python grade.py solution P05         # reference solution (after attempting!)
```
Requirements: `pip install -r 05_coding/code/requirements.txt` (numpy, pandas, scipy, statsmodels, scikit-learn). SQL problems build SQLite practice databases automatically (git-ignored).

## Problem list
| ID | Area | Level | Problem |
|---|---|---|---|
| P01 | C1 pandas | easy | Bad rate by segment (missing as its own group) |
| P02 | C1 pandas | medium | 12-month bad flag after an observation point (window edges, duplicate rows) |
| P03 | C2 metrics | easy | KS statistic with ties |
| P04 | C2 metrics | easy | Gini from AUC, vectorised, ties |
| P05 | C2 metrics | medium | PSI (reference bins, empty bins) |
| P06 | C2 metrics | medium | WoE & IV (missing bin, zero-bad bin) |
| P07 | C2 metrics | medium | Hosmer–Lemeshow |
| P08 | C2 metrics | medium | PD back-test by grade (binomial, Jeffreys) |
| P09 | C3 modeling | medium | Logistic regression by MLE |
| P10 | C1 pandas | hard | Roll-rate matrix from an unsorted panel |
| P11 | C1 pandas | hard | Vintage curves |
| S01–S10 | C4 SQL | easy→hard | Summaries, buckets, roll rates, performance-window bad rates, top-N, deciles+KS, PSI, consecutive delinquency, vintages, anti-join |

SAS (C5), code review (C6) and time-series (C7) problems are generated and reviewed by the interviewer (no auto-grading).
