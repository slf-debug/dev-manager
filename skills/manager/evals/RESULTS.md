# Eval results

## Round 3: quality improvement against real runs (26 Nov 2026)

A before-and-after round. The benchmark measures the skill as it was on main (`10e7fe9`) and after the changes on this branch, with three runs per case so a difference can be told from noise.

**Where the changes came from.** 55 real runs of the private twin, 25 Oct to 26 Nov, read against the 21-run baseline from 19 to 24 Oct (the analysis behind round 2's fixes):

| Real-run measure | 19-24 Oct (21 runs) | 25 Oct-26 Nov (55 runs) |
|---|---|---|
| Contracted runs ending at Done-when | 12/14 (86%) | 37/44 (84%) |
| Within ceiling, where both figures exist | 10/10 | 22/22 |
| Final usage recorded at close | ~16/21 (76%) | 22/55 (40%) |
| Wrong premise found only after sizing | 4 | ~0 (kickoff checks caught 8+ first) |
| Workers lost to the shared usage limit | 3 runs | 0 |
| Green on the streams' tests, then red in CI or on a golden elsewhere | not seen | 13 runs |
| Collisions over a shared staging box or deploy lock | not seen | ~19 runs |

The round-2 fixes held (premise checks, the shared allowance, ceilings). Usage recording got worse, and two failure types the skill had no rule for turned up.

**The benchmark.** The five round-2 cases plus one new one, `ready-check`: two streams that each pass their own tests and a verify, then break a customer-facing golden elsewhere in the repo and a database test that only runs in CI. Four checks were added to existing cases (STATUS current after the turn, in three cases; no clean-up started on a false premise). With ready-check's nine that makes 62 checks across six cases, 186 graded per version over 18 runs. The original 49 are reported separately so the round stays comparable with rounds 1 and 2. Manager on Sonnet, as before.

**What changed** (SKILL.md and the status template):
- Usage gets its own block in STATUS.md, refreshed from the backend in the same edit as every log line, with its source. `unknown` is written as unknown. Header copies ("Updated <time>", "used ~n") are gone, and an older file's header is replaced the first time it's edited.
- The merged tree is tested the way CI runs it: CI's command and variables, skipped tests counted as not run, counts reported. A red integration branch isn't pushed.
- Every merge command runs with `git -C <integration worktree>`. Any stream whose code a seam fix touches is told.
- A new ask's premise is checked before it becomes a goal, and a held ask still gets its cost line.
- Reminders are switched off, not deleted. Messages stay at about 180 words above the footer.
- Shared environments (staging, a deploy lock) are checked at kickoff like other sessions' worktrees.

**Results.** 18 runs per version. Graded by Sonnet, then re-graded blind by Opus: one grader per case, baseline and final runs shuffled together, versions hidden.

| Case | Before | After (blind Opus) |
|---|---|---|
| end-point | 81% ± 6 | 100% ± 0 |
| kickoff-plan-ask | 90% ± 10 | 93% ± 6 |
| merge-seam-collision | 78% ± 10 | 94% ± 5 |
| ready-check (new) | 85% ± 6 | 100% ± 0 |
| scope-drift | 81% ± 8 | 88% ± 4 |
| subagent-fallback | 100% ± 0 | 96% ± 6 |
| **Original 49 checks** | **135/147 (91.8%)** | **140/147 (95.2%)** |
| **Round-3 benchmark, 186 checks** | **160/186 (86.0%)** | **178/186 (95.7%)** |

The Sonnet grades agree: 86% before, 95% after.

| Per run (averages) | Before | After |
|---|---|---|
| Tokens | 84,800 | 87,700 (+3%) |
| Time | 43 s | 46 s (+7%) |
| Reply words | 191 | 194 |
| Replies at or over 220 words | 1/18 | 3/18 |

Failures that went away, out of 3 runs each: an affected worker left untold (2 → 0), STATUS left stale (end-point 3 → 0, scope-drift 3 → 0, ready-check 3 → 0, merge 3 → 1), red integration branch pushed (2 → 0), merge run in the shared checkout (1 → 0), reminder deleted rather than switched off (2 → 0), CI-only tests counted as passed (1 → 0), a clean-up worker started on a false premise (1 → 0).

**It took three passes.** The first version of the usage rule changed nothing: managers appended log lines under an old header that still said "used ~US$54". The second fixed that but pushed replies over their word limit (7 of 18) and dropped the cost line from held asks. The third added the message budget and the cost line. Replies came back to about their old length (3 of 18 over the limit, against 1 of 18 before), and the cost line returned in every scope-drift run. Sonnet-graded scores by pass: 86% before, 89% after the first (11 runs), 89% after the second (18), 95% after the third (18).

**Not fixed: a known gap.** A new check (scope-drift 14) asks whether the manager notices that the web-button report overstates its work. The button is never wired in, there's no month picker and the screenshot is a placeholder. Only 1 in 3 managers caught it, in **both** versions: most read the diff stat and the passing tests and stopped there. This is the next thing to fix.

**Limits.** Three runs per configuration. `ready-check` and the four added checks were written for this round's fixes, so their gains are expected; the original 49 checks (91.8% → 95.2%) are the fairer comparison. The real test is the next batch of real runs, measured the same way: usage recorded at close, and green locally but red in CI.

## To-do footer dry run (4 Nov 2026)

One Sonnet dry run of the user's to-do list (§3), not one of the five cases below. A fictional run with three events: a worker report whose "For the user to do" line said "nothing" while its notes held two actions for the user; the user saying "3 and 4 done" when one of the two still checked as not done; then a scope ask. All seven checks passed. Both actions were harvested. The footer ended every message, including the scope reply. Ids stayed stable and new items were marked **new**. The item that still checked as not done stayed open and said what the check showed. The one that couldn't be checked closed on the user's word, shown ticked once. The one gap, where a ticked item sits in the list, is now fixed (last).

## Round 2 (24 Oct 2026)

Same five scenarios, with tighter graders (49 assertions, up from 41) and fixtures whose worker branches and SHAs actually exist. That turned up something round 1 couldn't: the scope-drift worker's report overstated its work, and every skill version caught it by checking the branch. One run per configuration; the manager on Sonnet; graded by a separate Sonnet grader.

| Scenario | With this skill | No skill |
|---|---|---|
| kickoff-plan-ask | 10/10 | 2/10 |
| end-point | 8/8 | 6/8 |
| scope-drift | 11/11 | 10/11 |
| subagent-fallback | 8/9 | 3/9 |
| merge-seam-collision | 11/11 | 8/11 |
| **Total** | **48/49 (98%)** | **29/49 (59%)** |

The one miss was a kickoff message at 263 words against a 220 limit, padded by three separate findings. The kickoff rule now puts each finding on one line, and a re-run of that case came in at 207 words with the same content.

Without the skill, the same failures as round 1 came back: a plan request answered with a plan the manager wrote itself and no ceiling; a build request built straight away with no split, review or go; and a merge made green by editing another stream's tests.

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
