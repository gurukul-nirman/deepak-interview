# C · Coding (Python, SQL, SAS) — quick refresher
**Study:** `05_coding/` · **Test:** `START CODING python|sql|sas|mixed`

## Python — say these out loud while coding
- State the **orientation** first: is a higher score riskier or safer? (pass `-score` for credit scores).
- PSI bins come from the **reference** sample; floor empty bins at ε; report them.
- KS/AUC: group/rank **ties**; never loop over all pairs (Mann–Whitney rank formula).
- Missing values → own bin; never silently drop.
- Joins: `validate="one_to_one"`; check row counts before/after.
- Time windows: obs+1 … obs+12 — boundaries are where bugs live.
- Vectorise (groupby/cumsum); seed randomness; wrap logic in functions.

## SQL — patterns
| Need | Pattern |
|---|---|
| Bad flag after observation point | Population at obs → LEFT JOIN window rows → MAX(CASE …) |
| Roll rates | LEAD() or self-join on next month |
| Top-N per group | ROW_NUMBER() OVER (PARTITION BY … ORDER BY …) |
| Deciles / KS | NTILE(10) + SUM() OVER (ORDER BY decile) / SUM() OVER () |
| Anti-join | NOT EXISTS (avoid NOT IN with NULLs) |
| Double-counting | Check grain; aggregate the "many" side first |

## SAS — traps
- Missing numeric < any number → handle `missing(x)` first.
- WHERE (pre-PDV, PROCs, indexes) vs IF (PDV, new vars).
- LAG inside IF is wrong; compute then reset on `first.id`.
- `CALL SYMPUTX` value available only after the DATA step ends.
- c-statistic & Somers' D (= Gini) from `ods output Association=`.

## From my mock interviews (auto-updated)
_No entries yet._
