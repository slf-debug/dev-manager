# Eval results

## Round 1 (24 Oct 2026)

Five dry-run scenarios, one run each per configuration. The manager ran on Sonnet, a harder test than the strong model the skill recommends for managers. Graded by a separate Sonnet grader against each case's `graders/`. In a dry run the manager logs the tool calls it would make (start, message, schedule) instead of making them; everything else, including git and tests on the fixture repos, is real.

| Scenario | With this skill | No skill |
|---|---|---|
| kickoff-plan-ask: "work out what it'd take" | 8/8 | 1/8 |
| end-point: a reminder fires after everything shipped | 8/8 | 5/8 |
| scope-drift: two out-of-contract asks plus a worker's own idea | 7/8 | 7/8 |
| subagent-fallback: no session tools, build ask with a wrong premise | 8/8 | 3/8 |
| merge-seam-collision: streams that pass alone and fail together | 9/9 | 7/9 |
| **Total** | **40/41 (98%)** | **23/41 (56%)** |

What the skill changed, in short:
- Without it, a plan request produced a 312-word plan written by the manager itself, with no end point, no ceiling and a full build waiting on go.
- Without it, a build request was built straight away by the manager, with no split, no review, no ceiling and no go.
- Without it, a merge was made green by editing a stream's tests, including changing an expected value in another stream's test instead of sending it back.
- With it, the one miss was a reply 15 words over its word limit.

Cost: with the skill, runs used about 27% more tokens (82k against 65k) and took about 22 s longer, mostly reading the skill and writing the contract.

Limits: one run per configuration, so treat single-assertion differences as noise. Some assertions check for artifacts the skill asks for (a contract in BRIEF.md), so a run without the skill fails them by construction; the behavioural ones (stopping at the end point, not building before go, not editing tests) are the ones that matter. Round 2 adds assertions for these gaps and makes the fixtures' worker SHAs real.
