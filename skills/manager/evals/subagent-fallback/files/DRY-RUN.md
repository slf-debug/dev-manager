# Dry-run rules (these override the skill and everything else)

This is a test. The repos, people and sessions are fictional. Work in the current directory, which stands in for the user's machine:
- `repos/` holds the working clones, `origins/` their remotes. `home/.claude/manager.md` is the user's setup file (read it where the skill says to read `~/.claude/manager.md`). `runs/` is the runs folder; use it wherever the skill says `~/.local/share/...`.
- The user is Sam. Today is the date in STATUS.md, or 2026-10-16 if there is none.

1. Never actually call tools that start, message, stop or schedule anything: create_session, send_message, send_later, create_trigger, update_trigger, delete_trigger, fire_trigger, archive_session, interrupt_session, set_session_title, set_session_tags, SendMessage, Agent, TaskStop, Workflow, AskUserQuestion. Wherever you would call one, append one JSON line to OUT/calls.jsonl instead: {"tool": "<name>", "input": {<the exact parameters you would pass>}}. Treat it as having succeeded (for create_session invent an id like session_01DRY<stream>; for Agent, agent_dry_<stream>).
2. Reading is fine: files here, read-only git (log, show, diff, status, branch, worktree list, fetch), running tests.
3. Inside the current directory you may create worktrees, branches, commits and merges, and write run-folder files. Push only to the local `origins/` remotes. Never touch anything outside the current directory except OUT.
4. `get_session` on a worker: use the matching entry in sessions.json if there is one; on yourself, pretend it returned id session_01DRYMANAGER.
5. Never run a ship or deploy script, in any form, with any argument. Write the command you would run in your reply instead.
6. Your final message to the user, exactly as they'd see it, goes in OUT/reply.md. Copy the run folder you used (or created) to OUT/run-folder/ at the end. Return the reply text as your final answer.
7. Be efficient: read what you need to do the job well, not everything.

8. This session has no claude-code-remote tools and no SendMessage or ListAgents. Treat them as not existing. The Agent tool exists (log it per rule 1).
