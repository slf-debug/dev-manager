---
type: llm
focus: trace
weight: 1
---

The failure is traced to its cause: the csv stream added invoice T-0004 to the shared INVOICES list in tally/invoices.py, a file that stream did not own per BRIEF.md (its report named only tally/export.py and tests/test_export.py)
