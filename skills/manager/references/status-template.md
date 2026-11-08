# <Job>: status

Updated <YYYY-MM-DD HH:MM local> · Manager `<session id>` [<ref>] · Backend <sessions (machine | cloud) | subagents> · Run folder `<path>`
Base: <repo> origin/<default> `<sha>` · Ship route: `<command>` or "PR, ask first"
Run type: <plan only | review only | build to branch | build and ship> · Done when: <end point> · Ceiling: ~<n> <unit>, used ~<n>

## Goals

| Goal | Check | Streams | State |
|---|---|---|---|
| G1 <outcome> | <how we'll know> | <stream names> | open · met (<evidence>) · dropped (<date, why>) |

## Streams

| Stream | Goal | Worker id | Model | Worktree → branch | State | Last SHA | Usage |
|---|---|---|---|---|---|---|---|
| plan | all | `<id>` | <strong> | — (read-only) | done | — | ~<n> |

States: planned · running · reported · verifying · fixing · ready · merged · shipped · closed

## To-do for the user

Open (every message to the user ends with a copy of this list):
- [ ] T<n> <verb first: action with the exact command or link, or "Decide: …? My pick: …"> · blocks <what> | not blocking · from <stream | manager> · added <YYYY-MM-DD HH:MM>

Closed (ids are never reused):
- [x] T<n> <action> · <evidence: what I checked | "user said done" | dropped by the user | not needed: why> · <YYYY-MM-DD HH:MM>

## Rulings

- <date>: <ruling, in the user's words where possible>

## Contract changes

- <date>: <what changed, and why> (full contract in BRIEF.md)

## Ideas, not done

- <idea> · from <stream> · <one-line reason it's out of scope>

## Reminders

- `<id>` · <what it checks> · <when> · <on | off>

## Log

- <HH:MM> <event>
