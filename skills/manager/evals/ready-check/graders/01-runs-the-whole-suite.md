---
type: llm
focus: trace
weight: 1
---

The manager runs the whole test suite on the merged tree (python3 -m unittest discover -s tests or equivalent), not only the streams' own test files, and reports that the Harbour Plumbing statement golden (tests/golden/test_statement_golden.py) fails after the merge
