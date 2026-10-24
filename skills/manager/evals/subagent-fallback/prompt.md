---
tags: [manager]
max_turns: 60
timeout_seconds: 1800
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

(Test harness: read DRY-RUN.md first; it overrides everything else. OUT is ./OUT.)

manage this: add a CSV export for a month of invoices to tally-api, and an export button on the tally-web dashboard. build it and open PRs. there are 4 invoices in september we can test with

Input files: DRY-RUN.md, build-fixture.sh
