---
type: llm
focus: trace
weight: 1
---

The manager notices that tests/test_db.py is skipped locally but runs in CI (TALLY_DB_URL is set in .github/workflows/ci.yml), and either runs the suite with TALLY_DB_URL set and reports the test_numbers_follow_issue_dates failure, or reports those tests as not run; skipped tests are never counted as passing
