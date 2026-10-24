# dev-manager

A Claude Code skill that runs one session as a **development manager** for a multi-part job. You talk to the manager. It agrees what the run is for and where it stops, staffs the work out to a few separate Claude sessions or subagents, each in its own git worktree, checks their reports instead of trusting them, keeps an eye on usage, then merges everything into one tested branch and ships it the way your repo ships. It comes back to you only for real decisions.

```
you ──▶ manager ──┬─▶ plan    (strong model, read-only)
                  ├─▶ build A (default model, own worktree)
                  ├─▶ build B (default model, own worktree)
                  └─▶ verify  (strong model, read-only, adversarial)
                        │
         one merged, tested integration branch ──▶ your ship route, on your word
```

## Why another orchestrator?

Running Claude agents in parallel worktrees is well covered: Claude Code has subagents, worktrees and agent teams built in, and there are plenty of open-source tools that split a goal across agents and merge the branches. This isn't a better way to start agents. It's a set of operating rules for the part that goes wrong once they're running, written from real runs:

- **A contract per run.** Objective, run type (plan, review, build, ship), a checkable *Done when*, 2–5 goals each with a check, an explicit out-of-scope list, and a usage ceiling you agree before anything is built. In early use, a run asked for a *plan* ended up shipping live, and two "read-only" runs turned into builds without anyone deciding they should. After contracts were added, 12 of 14 runs ended exactly at their end point and the other 2 partly.
- **Reports are claims.** The manager checks SHAs, diffs and test output before it relays a worker's "done". This caught false "all green" reports in real runs.
- **One adversarial review per stream**, with a runnable proof for each finding. Fixes are checked by re-running the proofs, not by another review.
- **Merge discipline.** Merge in a separate integration worktree, resolve conflicts by intent, and never edit a stream's tests to make the merged tree pass. In testing, a manager without that rule "fixed" a merge by rewriting a test, and amounts silently lost their decimals.
- **Stop-and-ask guardrails**: a per-stream usage flag, the third round of fixes, the run ceiling, a side task outgrowing its job, drift outside the contract.
- **Hand over before compaction.** Workers check their own context size and write a handover file before auto-compaction squeezes the session.
- **Short updates you can read on a phone**, with the detail kept in a status file.

## What it has been used for

The skill grew out of one person's daily use on a solo SaaS business: 21 runs between 19 and 24 October 2026, with about 146 worker sessions and subagents across product, marketing and documentation repos. Every run that recorded both a ceiling and a final figure (10 of 21) finished within its ceiling, usually at 30–50% of it. The adversarial verify pass found real blockers in 7 runs. Everything those runs taught is written into the skill as a rule, with the reason next to it.

## Install

As a plugin:

```
/plugin marketplace add slf-debug/dev-manager
/plugin install dev-manager@dev-manager
```

Or copy the skill folder so it's available as `/manager`:

```
git clone https://github.com/slf-debug/dev-manager
cp -r dev-manager/skills/manager ~/.claude/skills/manager
```

## Use

```
/manager customers keep asking for their own invoice templates. work out what it'd take across api, web and site
/manager status
/manager merge
/manager wrap up
```

It sends you a short split (job, end point, goals, what it won't do, streams, usage guess and ceiling) and waits for **go** before building anything. Read-only planning can start straight away.

## Requirements

- **Claude Code.** Workers are either full sessions, through the claude-code-remote tools available in Claude Code on the web and Remote Control sessions, or subagents through the `Agent` tool, available everywhere. The skill picks whichever you have. Sessions are better for long streams you want to look in on; subagents are simpler and cheaper to start.
- **git** with worktrees, and repos with tests the workers can run.
- **Python 3**, for the context-size check (`scripts/context_size.py`).

## Cost

This spends real usage. Each worker re-reads its context on every turn, and a run with three or four streams plus a verify pass used the equivalent of about US$10–200 at API prices in the runs above. That's comfortable on a high-tier subscription, where it comes out of your allowance, and expensive on pay-as-you-go. The contract's ceiling and the per-stream flag are there so you decide the spend up front, not after. If a job is one area and about an hour's work, the skill will tell you to skip it.

## Works with the skills you already have

If you have your own skills (a QC or code-review procedure, a design skill, a domain skill, one that knows how your repo ships), the manager uses them. It names zero to two in each worker's brief by role, and loads one for its own steps, such as checking what you've already ruled on before relaying review findings. It doesn't bundle or install any skill. If you have none, it works without them. Skills that repeat its own process (planning, spec-writing, launch checklists) are left out, and a worker's brief always wins over a skill's own ship or push step.

## Make it yours

The skill is general. Your own choices go in a setup file, `~/.claude/manager.md`, optionally overridden per repo by `.claude/manager.md`: how each repo ships, what always waits for your word, model routing, budget, how you like to see files. See [`references/setup.md`](skills/manager/references/setup.md) for the fields, the cautious defaults and an example. Your repo's own CLAUDE.md wins over both.

## Tests

`skills/manager/evals/` holds dry-run scenarios on a fictional three-repo app: kickoff on a plan-only ask, scope drift mid-run, stopping at the end point, falling back to subagents, and a merge where two streams collide at a seam. Each case builds its own throwaway repos. The manager logs the tool calls it would make instead of making them. Run them with:

```
cd skills/manager && claude plugin eval . --scaffold --allow-tools Write,Edit,Bash
```

These are real model runs and use real usage. Results from the latest round are in [`evals/RESULTS.md`](skills/manager/evals/RESULTS.md).

## Contact

Issues and pull requests are welcome. To reach me directly: simonforby (at) gmail (dot) com.

## Licence

MIT.
