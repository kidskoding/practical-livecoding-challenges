# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

Mock live technical / practical coding challenges from companies that **don't** interview with LeetCode-style algorithm puzzles — Slack, Cloudflare, Neuralink, and similar. These interviews are open-ended technical problem solving: build a small working system, parse and process real data, extend a given codebase, debug something live. Correctness and working code under time pressure matter more than recognizing a pattern.

Pure algorithm drilling lives in the sibling repos (`../dsa`, `../leetcode`, `../faang-dsa`, `../graph-theory`) — keep it out of this one.

## Layout and commands

One directory per company, one numbered directory per challenge inside it. A challenge is a prompt and a stub file, nothing more:

```
slack/01_message_store/
├── README.md            # the 60-minute prompt: spec, timed parts, evaluation notes
└── message_store.py     # stubs with `pass` bodies — the file you solve in
```

`uv`-managed, Python 3.12 (`.python-version`), zero dependencies. Run a challenge module directly:

```bash
uv run python slack/01_message_store/message_store.py
```

**There are no tests in this repo, and pytest is not a dependency.** Don't add a suite unless explicitly asked. A practical interview hands you a prompt and a blank editor; a red suite hands over the edge cases you were supposed to find yourself and turns the exercise into chasing assertions. The README is the spec — it states the exact return and dict shapes so nothing has to be guessed — and any checks you write while solving are throwaway (`assert` in a `__main__` block, or a REPL).

Python is 3.12, so `X | None` annotations work natively — no `from __future__ import annotations`.

## Writing a new challenge

Follow the `challenge-scaffold` skill. In short: pick a problem off the company's real product surface, write the README as a product requirement with an exact contract and per-part time budgets, and leave the stub bodies as `pass` (never `raise NotImplementedError`).

- Timestamps and ids are supplied by the caller, never generated inside the module, so behavior is reproducible when discussing it.
- Parts must be independently demoable — a candidate who runs out of time still has something that runs.
- Verify a working reference implementation before committing the challenge, then throw it away; reference solutions are not checked in.
- Never name the intended data structure or pattern in the prompt. The modeling choice is the thing being practiced.

## Skills in this repo

Both live under `.claude/skills/` and are written for this repo specifically (they were adapted from the sibling DSA repos — ignore any DSA-shaped advice you remember from those).

- `challenge-scaffold` — the mechanical convention: folder layout, README section order, stub format, and what to verify before committing.
- `company-framing` — how to choose a problem that is genuinely a given company's, and write it as a product requirement rather than a puzzle.

Invoke either via the Skill tool when the task matches.
