# T16 · Data, implementation & documentation review — quick refresher
**Study:** `03_monitoring_validation/02_independent_validation_playbook.md` §5B, §5H · **Test:** `START TOPIC T16`

| Q | A |
|---|---|
| Data checks before trusting metrics? | Volumes, missing/out-of-range, duplicates, reconciliation to source, definition changes, impossible transitions |
| Lineage? | Trace each input from source system to model, with transformations documented |
| Implementation testing? | Prod vs dev outputs on a sample (parallel run), feed mapping, edge cases (missing, boundaries), rounding, cut-off logic |
| Classic implementation bug? | Missing values mapped to the wrong bin / default points |
| EUC controls? | Inventory, access control, versioning, review, reconciliation |
| Reading an MDD critically? | Purpose vs use, sample design, exclusions with counts, default definition, variable rationale, OOT, limitations, monitoring plan |
| BCBS 239 in one line? | Principles for risk-data aggregation and reporting (accuracy, completeness, timeliness, adaptability) |

## From my mock interviews (auto-updated)
_No entries yet._
