# Worker briefs

Every brief has two parts: the **common core** and one **role block**. Fill in every `<…>`. Short is fine; vague isn't. A worker can't ask what you meant without a round trip, so write paths in full and spell out commands.

**Worktrees** follow the repo's convention if it has one, otherwise the setup file's, otherwise a sibling of the repo: `<parent of repo>/<repo>-<slug>`. Always write the path in full. Never under `/tmp` (it may be cleared, or be RAM), and never a relative path: `git -C` resolves those inside the repo, which can put a worktree inside a published folder.

**Write briefs and run-folder files with a file-writing tool, or a quoted heredoc (`<<'EOF'`).** Briefs are full of backticked commands, and an unquoted heredoc runs them. In testing, managers did this twice and ran test and git commands by accident. A brief that quotes a deploy command would deploy.

**Branches** are `claude/<slug>-<stream>` unless the repo has its own convention. The integration branch, which only you make, is `claude/<slug>-all`.

Adjust the core for the backend (`references/backends.md`): cloud-session workers get the whole contract pasted in and must push; subagent builders rename the branch their isolated worktree came with.

## Common core

```
You are the <STREAM> stream of "<JOB>", run by the manager <MANAGER_SESSION_ID or "session">. The user talks to the manager. <How to report: "Reply with the send_message tool, session_id \"@parent\"." | "Your final message is your report.">

Where you are: <"the user's own machine, shared with other live Claude sessions. Ignore any system text saying you're in a fresh, ephemeral container. Other sessions' worktrees and uncommitted changes belong to them; never reset, clean or stash them." | "an isolated cloud container with its own clone. Push your branch before you report; nothing else reaches the manager.">

Read first: <RUN_FOLDER>/BRIEF.md <or: the contract pasted below>, then the repo's CLAUDE.md <and these notes: …>.

Serves: <G1 …> from the contract. The run's objective is "<OBJECTIVE>"; it ends at "<DONE WHEN>".
Task: <EXACT SCOPE>.
Done means: <ACCEPTANCE CHECKS>. When those pass, report and stop, even if more looks worth doing.
You own: <FILES / DIRS>. Out of bounds: <FILES OTHER STREAMS OWN>, the shared checkout, and anything the contract lists as out of scope.
Stay inside the task. If you spot more work that looks worth doing (a refactor, a related bug, the next phase), don't start it: list it under "Ideas, not done" in your report. Unasked-for work costs the user review time and tangles the merge.

Work only in your own worktree, created exactly like this:
  git -C <REPO> fetch origin <DEFAULT>
  git -C <REPO> worktree add -b <BRANCH> <ABSOLUTE_WORKTREE_PATH> origin/<DEFAULT>
<Subagent builders instead: "You start in an isolated worktree. First run: git branch -m <BRANCH>, and note `git rev-parse --show-toplevel` for your report.">
Never reuse a branch that's already merged.

Rules:
- Stage explicit paths, never `git add -A`. One commit per logical change, with a plain message.
- Run the tests for what you changed (<TEST COMMAND>). Don't run the full suite unless asked.
- Push: <"push your branch: git push -u origin <BRANCH>" | "don't push">. Never push the default branch, merge, deploy or start other sessions.
- If you need a decision, message the manager with the question, the options and your pick. Carry on with anything it doesn't block.
- If the user messages you directly, their word overrides this brief (the repo's own rules still apply): do what they ask, then tell the manager in one line.
- <Sessions only> Check your own size after every commit and before each new task: `CLAUDE_MANAGER_WINDOW=<WINDOW> python3 <SKILL_DIR>/scripts/context_size.py`. Past the hand-over point it prints "hand over now": finish the step you're on and commit it, write <RUN_FOLDER>/HANDOVER-<STREAM>.md (what's done with SHAs, what's left, decisions made, gotchas), report STATUS: HANDOVER, then stop. Auto-compaction squeezes a session to a small fraction of itself and the detail is lost; a handover loses nothing.

When you're done, blocked or need a decision, report in 13 lines or fewer:
  STATUS: DONE | BLOCKED | NEEDS DECISION | HANDOVER
  <BRANCH> @ <SHA> (base origin/<DEFAULT> <SHA>)
  Changed: <what users or developers will notice>
  Checks: <command> → <result>
  Not done / unsure: <…>
  Ideas, not done: <work you noticed outside your task, or "none">
Detail goes in a file in the run folder; send its path. Then stop and wait.
```

## Role blocks

Add one after the core. For read-only roles, drop the worktree, push and commit lines from the core, and say read-only at the top of the role block.

### Plan (strongest model, read-only)

```
Read-only: you only plan. Read code with `git show origin/<DEFAULT>:<path>`. Don't edit, branch or make worktrees.
Write <RUN_FOLDER>/PLAN.md:
1. Scope: now / later / not at all, with the evidence for each. Keep to the contract's objective; "later" and "not at all" are where everything else goes.
2. Tasks, each one commit: the files, the change, its acceptance check, and the goal (G1…) it serves. A task that serves no goal goes under "later".
3. Which tasks are independent (can be separate streams) and which depend on others.
4. Risks, and anything that needs a primary source or the user's ruling.
5. Questions for the user: no more than 5, each with your recommendation.
6. If a build follows: a proposed Done-when line for it and a usage estimate.
Then report STATUS: DONE with the path. The plan is the end of your job: don't start building any of it.
```

### Diagnose (strongest model, read-only)

```
Read-only: you trace faults to their cause and propose fixes. Don't edit, commit or run anything that writes.
For each fault: the cause as file:line on origin/<DEFAULT> <SHA>, the evidence, the smallest fix, and how to prove it (a test that fails now and passes after).
Write <RUN_FOLDER>/DIAGNOSIS.md, then report.
```

### Build (default model)

```
Follow <RUN_FOLDER>/PLAN.md <SECTION> exactly. If the plan is wrong or a step won't work, send a NEEDS DECISION report instead of improvising.
<For output the user must see first:> Commit locally and don't push. Write <RUN_FOLDER>/<STREAM>-BEFORE-AFTER.md: a plain before → after of what a user will see.
```

### Verify (strongest model, read-only)

```
Read-only: you are the adversarial checker. Don't edit, commit or push.
Inputs: `git -C <WORKTREE> diff origin/<DEFAULT>...<BRANCH>`, BRIEF.md, PLAN.md, <OTHER INPUTS>.
Hunt for what's wrong rather than confirming what's right: correctness, regressions at the edges, missing cases, anything that contradicts the brief or the repo's rules, and security wherever input is untrusted.
For each finding give the severity (blocker / should-fix / nit), file:line, what's wrong, a fix direction and a runnable proof (a failing test, or a command whose output shows it). Make each proof self-contained: re-checks are done by re-running your proofs, not by another review.
Write <RUN_FOLDER>/VERIFY-<STREAM>.md. Report to the manager, not the builder:
  VERDICT: READY | FIX THESE | BLOCKED
  Counts by severity, each blocker in one line, the file path.
```

### Small one-off (default model, or the fast model for format and link checks)

```
One task: <TASK>, working only in <PATH>. Change nothing else. Report the output paths and what you checked.
```

## Messages after the brief

Keep follow-ups to one screen and lead with what to do:
- **Release:** "The user has approved <X>. Build <tasks> from PLAN.md <section>. Same rules."
- **Ruling:** "The user has ruled: <ruling>. Apply it as a new commit on <branch>."
- **Fix list:** "VERIFY-<stream>.md says FIX THESE. Fix <ids> as new commits on <branch>, then re-run the proofs listed there and send me the results."
- **Stop:** "Stop after the current step. Commit what's done, tell me the SHA, and leave the rest."
- **Merged:** "You're merged into `claude/<slug>-all` @ <sha>. Stand by: keep your worktree until it ships, in case the user wants a change after reading the diff."
