# Backends: the exact tools for each step

The manager works the same way whatever starts the workers. This file maps each step to the tools for the two backends. Read it once at kickoff.

| Step | Sessions (claude-code-remote tools) | Subagents (`Agent` tool) |
|---|---|---|
| Your own id | `get_session` with no arguments | none needed |
| Start a worker | `create_session` with `environment_id`, `model`, `title`, `tags`, `permission_mode`, `prompt` (the brief) | `Agent` with `prompt` (the brief), `model` (`opus` / `sonnet` / `haiku`), `isolation: "worktree"` for builders, `run_in_background: true` |
| Worker reports to you | worker calls `send_message` with `session_id: "@parent"` | the completion notification carries its final message |
| You message a worker | `send_message` with its `session_id` | `SendMessage` to its agent id (resumes it with its context) |
| Stop a worker | `interrupt_session`, then a message saying what to do | `TaskStop`, if available; otherwise let it finish and ignore the rest |
| Check-in | one `send_later` reminder into your own session for the whole run; when it's no longer needed, switch it off with `update_trigger` (`enabled: false`) and set a fresh one for the next due item | not needed: the notification arrives when it finishes |
| Worker state | `get_session`: `status_bucket`, `context_usage.used_tokens`, usage/cost fields, any rate-limit info; then `list_events` (pass `kinds: ["assistant", "result"]`) for what it last said | the notification's `total_tokens` and `duration_ms` |
| Close a worker | `archive_session` | nothing to do |
| See the team | `list_sessions` filtered by the run's tag; `set_session_title` / `set_session_tags` to group them | the agent ids in STATUS.md |
| User talks to a worker | they open it (claude.ai/code, the desktop or mobile app) and type; its brief says to tell you | not possible: they tell you, and you pass it on |

Tool names and fields change between versions. If one isn't there, look for the closest match before deciding the backend is missing.

## Sessions

**Where workers run.** `list_environments` shows the environments you can start sessions in. They come in two kinds, and the difference matters more than anything else on this page:

- **On the user's machine** (a Remote Control or self-hosted environment). Workers share the filesystem with you and with each other. Worktrees, the run folder, `HANDOVER-*.md` files and merging local branches all work as written in SKILL.md. Pick the environment for the project directory the work is in, so workers start with that project's CLAUDE.md and memory. Environment ids can change when the user re-links a machine, so look them up every run.
- **In the cloud** (Claude Code on the web). Each worker gets its own fresh container with its own clone. It can't see your run folder, your worktrees or the other workers. So:
  - the brief must carry the whole contract and everything else the worker needs, not a path to BRIEF.md;
  - workers don't make worktrees (their clone is already theirs); they work on their branch and **push it**, because pushing is the only way their work reaches you;
  - you merge by fetching their branches into your own integration worktree;
  - handover notes go in the report message, or as a file committed on the worker's branch;
  - the brief's "where you are" line says it's in an isolated container and must push before it reports.

If you're unsure which kind an environment is, start the first worker with a brief that asks it to report `pwd`, `hostname` and whether it can read your run folder.

**Messages.** Sessions you created reply with `send_message` to `@parent`, and you answer with `send_message` and their `session_id`. Sessions the user started themselves are reached another way, usually `SendMessage` with the name `ListAgents` shows. The two routes don't cross: a message sent on the wrong one never arrives. If a worker's reply doesn't arrive, read its last assistant message with `list_events` before assuming it's stuck.

**Silence.** A session reports only when it finishes a turn cleanly. One that errors, stalls or hits a usage limit goes quiet, which is why every dispatch gets a `send_later` check-in. When it fires: `get_session`, then `list_events` if that's unclear. Prefer switching reminders off (`update_trigger` with `enabled: false`) to deleting them; deletion is often left behind a permission prompt on purpose, so that no session can delete the user's other scheduled tasks.

**Permissions.** A worker can't be given a wider permission mode than yours. Asking for `auto` when your own session isn't in auto mode gets the `create_session` call refused, which in real use happened in four runs. So match the worker's mode to your own, or leave `permission_mode` out so it inherits yours. If the user wants workers that don't stop to ask, the fix is to run the manager in that mode. If your own coordination calls keep hitting permission prompts, the fix is allow rules in the user's settings. A skill can't grant those itself, and you shouldn't try to edit them: tell the user which tools prompted and let them decide.

**If sessions are refused and you fall back to subagents,** say so on the board, because subagents live inside your session: if the user stops your session, they stop too, and if you hand over to a fresh manager, the old manager's subagents can't report to the new one. Before a manager handover with subagents still running, wait for them to finish or stop them and record where each got to.

**Usage.** `get_session` reports usage per session, often as an API-equivalent cost. On a subscription plan that measures allowance, not money; say which.

## Subagents

**Starting.** One `Agent` call per worker, in the background. `isolation: "worktree"` gives a builder its own worktree of the repo *your* session is in, on its own branch; the brief's first step is then to rename that branch to the run's naming (`git branch -m <BRANCH>`) and report its worktree path. For any other repo, and for every repo when your session isn't inside one, leave isolation off and put the explicit `git worktree add` command in the brief, as with sessions. Read-only roles (plan, diagnose, verify) don't need isolation; their brief says they're read-only.

**Limits that change the rules.**
- Subagents can't start subagents, so the flat-team rule holds by itself.
- The user can't talk to a subagent. Anything they want changed comes through you.
- A subagent runs one task and returns. Size streams so each one finishes in a single run. If a stream is too big for that, split it into steps and resume the same agent with `SendMessage` for the next step, so it keeps what it learned.
- `scripts/context_size.py` reports *your* session's size, not a subagent's, because subagents share your session id. Their notification's `total_tokens` is the only size signal you get.
- Usage comes as tokens, not cost. Keep a running total in STATUS.md and set the ceiling in tokens.

**Your own size matters more here**, because every report lands in your context. Ask for the 13-line report format and nothing more; have workers write detail to files in the run folder and send you the path.

## Mixing

Use subagents for quick read-only questions even in a sessions run ("is this already on main?", "where is X handled?"). They're far cheaper than a new session and don't need a check-in.
