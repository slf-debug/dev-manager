# The setup file

The skill is general. The setup file is where your own way of working goes: how each repo ships, what waits for your word, which models do what, how much a run may spend before it asks. Without one the manager uses the defaults below, which are deliberately cautious.

**Where it lives:** `~/.claude/manager.md` for everything, and optionally `.claude/manager.md` in a repo for that repo. The repo file wins where the two differ. The repo's own CLAUDE.md, CONTRIBUTING and CI config win over both.

It's plain Markdown, read by the manager rather than parsed, so write it the way you'd brief a new colleague. Every section is optional.

## Fields and defaults

| Section | What it says | Default when missing |
|---|---|---|
| **About me** | Name, how to address you, language and spelling, where you usually read replies (phone, laptop) | Match the language you write in; assume replies may be read on a phone, so keep them short |
| **Ship routes** | For each repo: the exact ship command, whether branch pushes are fine, whether PRs are the gate | Push the integration branch and open a PR, after asking. Never push the default branch |
| **Needs my word** | What always waits for you | Production deploys; pushes to the default branch; anything published or sent to people (packages, posts, emails); prices; legal copy; anything that spends money |
| **Wording that matters** | Output where the words carry weight (clinical, legal, financial, safety text): committed but not pushed until you've seen a before → after | None beyond the line above |
| **Skills** | Which of your skills fit which worker role (verify, UI, a domain), and any to keep out of workers | The manager matches skills from the session's list to roles; none that repeat its own process |
| **Models** | Which model for each role, with current ids for the sessions backend | Strongest available model for manager, plan and verify; the default model for builders; the fastest for mechanical checks |
| **Budget** | The unit (API-equivalent dollars, tokens, or "allowance"), a typical run ceiling, the per-stream flag | Per-stream flag at about a third of the run ceiling. Say which unit you're quoting |
| **Context** | Your context window, and when to hand over | The window your model actually has (system prompt or model id); hand over at 40% of it for workers, 60% for the manager. `context_size.py` reads `CLAUDE_MANAGER_WINDOW`, and falls back to 200,000, which is safe but hands over early on 1M-token models |
| **Showing files** | How you want to see files: a link, a path, an artifact | The absolute path, or the session's own file-sharing tool |
| **Machine** | Shared machine or cloud containers; anything workers must know (other sessions share it, paths to avoid, worktree location) | Worktrees as siblings of the repo (`<repo>-<slug>`), never under `/tmp` |
| **Runs folder** | Where run folders go | `~/.local/share/manager-runs/` |
| **Approval style** | Which routine steps may run without asking | Everything routine in SKILL.md §1 runs without asking; "Needs my word" items always wait |

## Example

A fictional solo developer with three repos, on a subscription plan, reading on a phone:

```markdown
# Manager setup

## About me
Alex. Plain English, short bullets. I read on my phone most of the day.

## Ship routes
- api: `make ship ENV=prod` after CI is green. Staging: `make ship ENV=staging`, no need to ask.
- web: merging to main deploys. PRs are the gate: push the branch, open the PR, I merge.
- docs: push straight to main.

## Needs my word
Production deploys, anything emailed to customers, pricing page, terms.

## Wording that matters
Anything in api/reports/ that a customer reads: commit it, don't push it, and show me before → after.

## Models
Manager, plan, verify: Opus. Build: Sonnet. Link and format checks: Haiku.

## Budget
Usage is API-equivalent dollars from get_session; it's my plan's allowance, not a bill.
Typical run ceiling ~$100. Flag any stream past ~$40.

## Context
1M window. Workers hand over at 400k, manager at 600k.

## Showing files
Give me the path; I'll open it in the editor.

## Machine
Workers run on my own machine through Remote Control and share it with my other sessions.
Don't touch other sessions' worktrees or uncommitted changes. Stage explicit paths only.
```

## Why a separate file

The rules in SKILL.md came from real runs and apply to anyone. The choices in this file are yours, and they're the ones that change: a new repo, a new deploy script, a bigger budget. Keeping them apart means you can update the skill without losing your setup, and change your setup without editing the skill.
