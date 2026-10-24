#!/usr/bin/env python3
"""Print how many tokens this Claude Code session's context holds right now.

Reads the session's own transcript (found by $CLAUDE_CODE_SESSION_ID) and adds up the
input side of its latest model call. That is the context the next turn re-reads, which
is what auto-compaction is measured against.

  context_size.py                 # workers: hand over at 40% of the window
  context_size.py --at 0.6        # the manager: hand over at 60%

The window comes from $CLAUDE_MANAGER_WINDOW (default 200000); set it to your model's
context window. $HANDOVER_AT (tokens) overrides the fraction.

Exit 0 and print e.g. "412,830 tokens, 41% of 1,000,000 (past 40%: hand over now)";
exit 2 if the size is unknown. Run from a subagent, it reports the parent session's
size, because subagents share the parent's session id.
"""
import argparse
import glob
import json
import os
import sys

parser = argparse.ArgumentParser(description="Report this session's context size.")
parser.add_argument("--at", type=float, default=0.4,
                    help="hand-over point as a fraction of the window (default 0.4)")
args = parser.parse_args()

window = int(os.environ.get("CLAUDE_MANAGER_WINDOW", 200_000))
handover_at = int(os.environ.get("HANDOVER_AT", window * args.at))
sid = os.environ.get("CLAUDE_CODE_SESSION_ID")
paths = glob.glob(os.path.expanduser(f"~/.claude/projects/*/{sid}.jsonl")) if sid else []
if not paths:
    print("unknown: no transcript for this session")
    sys.exit(2)
size = None
with open(max(paths, key=os.path.getmtime), errors="replace") as fh:
    for line in fh:
        if '"usage"' not in line:
            continue
        try:
            entry = json.loads(line)
        except ValueError:
            continue
        msg = entry.get("message") or {}
        usage = msg.get("usage") if entry.get("type") == "assistant" else None
        if usage and not entry.get("isSidechain"):
            size = (usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                    + usage.get("cache_creation_input_tokens", 0))
if size is None:
    print("unknown: no model calls recorded yet")
    sys.exit(2)
note = f" (past {handover_at:,}: hand over now)" if size >= handover_at else ""
print(f"{size:,} tokens, {size / window:.0%} of {window:,}{note}")
