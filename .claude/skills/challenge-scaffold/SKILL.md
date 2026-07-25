---
name: challenge-scaffold
description: 'Use when adding a practical live-coding challenge to this repo — e.g. "create a 60-minute Cloudflare challenge", "add another Slack practical", "scaffold challenge 02" — to reproduce the exact folder layout, README section order, and stub format, and to know what to verify before committing.'
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Challenge Scaffold

The mechanical convention for one timed practical challenge in this repo. The
canonical reference is `slack/01_message_store/`. This skill nails the files and
their shape; `company-framing` decides the company-specific story and problem.

## When To Use

- "Create a `<duration>` challenge for `<company>`."
- "Add challenge NN to `<company>`."
- "Scaffold the stubs and README for `<problem>`."

## Folder Layout

```text
<company>/NN_<slug>/
├── README.md              # the prompt: spec, timed parts, evaluation notes
└── <slug>.py              # stubs, `pass` bodies — the file solved in
```

- Lowercase company dir (`slack/`, `cloudflare/`, `neuralink/`), zero-padded
  challenge number, snake_case slug naming the *thing built*, not the pattern.
- Module filename matches the slug.
- Two files, nothing else. No test file, no `conftest.py`, no `__init__.py`, no
  per-challenge config. The repo root `pyproject.toml` is `uv init` output with
  zero dependencies — leave it that way.

**There are no tests in this repo, and pytest is not installed.** A practical
interview hands you a prompt and a blank editor; a suite hands over the edge
cases you were supposed to find yourself and reduces the exercise to chasing
red. The README is the spec; throwaway `assert`s in a `__main__` block are how
you check your work while solving.

**No reference solution is checked in either.** Verify one while authoring, then
delete it — a `SOLUTION.md` sitting next to the prompt is too easy to open at
minute 20.

## README Format

Sections in this order:

1. `# <Company> — <Duration> Practical: <Title>`
2. The scenario in two or three sentences, plus the **exact** data shape (dict
   keys, return types, who supplies timestamps and ids) and where to work. A
   candidate must never have to guess a field name.
3. `## Part N — <name> (~N min)` — the body of the prompt, see below. Budget the
   parts to the stated duration and leave ~5 minutes at the end for questions.
4. `## What's being evaluated` — plus an explicit not-evaluated list (scaling,
   persistence, auth) so the candidate doesn't wander out of scope.
5. `## Complexity to be ready to discuss` — 3–5 questions the interviewer asks,
   phrased as questions and left unanswered.

## Writing A Part (the important bit)

A part is continuous prose that dictates each function the way an interviewer
talks it through live — no signature headings, no per-function subsections.
**Be exhaustive.** Ambiguity in a live interview gets resolved by asking; on
paper it just wastes the rep.

```markdown
Then write a function called `history` that returns one page of a channel's
top-level messages, **newest first**.

- Return the message dicts themselves, not ids.
- `limit` caps the page size. A `limit` larger than the number of available
  messages returns everything available — never pad, never error.
- `before` is a message id and is **exclusive**: return only messages strictly
  older than that message. `before=None` starts from the newest message.
- An unknown channel returns `[]`. So does a channel with no messages. Neither
  is an error.
```

Rules for that prose:

- Open with ``Write a function called `name` that …`` — or
  ``Then write a function called `name` that …`` for the second and later
  functions in a part. Name the function: this is a dictated task, not a puzzle
  where the candidate invents the API.
- **Don't restate the signature as a heading.** No `### \`history(channel,
  limit=50, before=None) -> list[dict]\``. The stub file already carries the
  signature, and the bullets name every parameter — repeating it is noise.
  Headings inside a part are for genuine asides ("The constraint that
  matters"), not for function names.
- One bullet per rule, and cover **every** parameter: what it means, its
  default, what an out-of-range or unknown value does.
- Pin down every ordering (`newest-first` / `oldest-first`), every boundary
  (`inclusive` / `exclusive`, `strictly greater`), and every "does X count"
  question (own messages, replies, soft-deleted rows). Bold the words that
  invert behavior if misread.
- Spell out the empty and unknown cases explicitly, and say **returns `[]`/`0`,
  not an error** — otherwise half the candidates raise.
- Give the product reason for any rule that looks arbitrary ("the channel view
  renders `2 replies` without loading the thread"). That's how a real ticket
  reads, and it tells the candidate which invariant actually matters.
- **Give examples per function, not per part** — 1–3 of them, right after that
  function's bullets, the way an interviewer scribbles cases in the shared doc.
  One is enough for a trivial function; use two or three when ordering,
  boundaries, or filtering are involved.
- **At least one of those examples is an edge case,** and it's the edge case the
  bullets are most likely to be misread on: empty input, unknown key, cursor at
  the oldest item, single element, the user's own message, an out-of-order
  write. If a function has a rule stated in bold, there's an example pinning it.
- Format each as a short call sequence with the expected result in a trailing
  comment. Never write the implementation — only calls and results:

  ```python
  store.history("#general", limit=2)                # three, two
  store.history("#general", before=third)           # two, one
  store.history("#nope")                            # []  — unknown channel
  ```

- Label an example when its point isn't obvious from the call
  (`# []  — unknown channel`, `# 1  — bo's own message doesn't count`).
- Functions that are only meaningful in combination (a writer and its reader,
  `mark_read` then `unread_count`) share one example block placed after the
  second one. Don't invent a standalone example for a setter that returns
  nothing.
- State any assumption the candidate is allowed to make ("assume messages
  arrive in non-decreasing `ts` order"), and ask them to say what breaks if it
  doesn't hold. That converts a shortcut into a discussion.
- Mark what's explicitly out of scope inside the part ("threads are one level
  deep; say what you'd do about deeper nesting, don't build it").
- Separate parts with `---`. Each part must be runnable on its own.

## Stub Format

```python
class MessageStore:
    def __init__(self) -> None:
        pass

    # --- Part 1: channel history ---

    def post_message(self, channel: str, user: str, text: str, ts: float) -> str:
        # Store a top-level message in a channel. Return its id.

        pass
```

- Type-hint every signature. Python is 3.12, so `X | None` needs no
  `from __future__ import annotations`.
- One `# --- Part N: <name> ---` comment per README part, methods in part order.
- One-line comment per method restating the contract in the caller's terms.
- Body is `pass`, never `raise NotImplementedError` — a stub that returns `None`
  fails as a wrong value, not a traceback.
- Caller supplies timestamps and any ids (`ts: float`); nothing generates
  wall-clock time inside the module, so behavior is reproducible in discussion.

## Verify (then throw it away)

Before committing a challenge, write a working reference **in a scratch file
outside the repo** and exercise every part of the spec:

```bash
uv run python <scratch>/<slug>.py
```

Check that each part is satisfiable inside its time budget, that no example in
the README contradicts the reference, and that every rule the reference relies
on is actually stated in the prompt (inclusive bounds, ordering, what counts as
whose message). Then delete the scratch file — a challenge whose reference was
never run isn't finished, and one whose reference ships isn't a challenge.

The reference's ceilings — linear scans, in-order-write assumptions — belong in
the README's `## Complexity to be ready to discuss` as open questions, never as
answers.

## Gotchas

- **Under-specifying is the real failure.** Inclusive or exclusive cursor?
  Newest-first or oldest-first? Does a user's own message count? What does an
  unknown key return? Unstated means the candidate guesses, and a guessed spec
  can't be practiced against. Err heavily toward more prose per function.
- **Terse signature dumps aren't prompts.** A line like
  ``` `mark_read(user, channel, ts) -> None` ``` with one sentence under it is a
  note-to-self, not a live-coding prompt. Every function gets a dictated
  sentence and its own bulleted contract — but no heading; see above.
- **A function without examples is unfinished.** Examples are where ordering
  and boundary rules stop being arguable — and one happy-path example alone
  doesn't do that. Pair it with the edge case.
- **Don't reach for DSA-repo conventions.** `problem_set/` dirs, namespace
  packages, `pythonpath` wiring, per-category stub files, pytest suites — all of
  that belongs to `../dsa` and friends. Challenges here are one self-contained
  module plus a prompt.
- **Don't leave a solution behind.** Reference implementations, filled-in stubs,
  and worked examples in the README all defeat the exercise.
- **Scope creep dressed as realism.** Persistence, concurrency, and auth turn a
  60-minute build into a system-design interview. Put them in the not-evaluated
  list instead.
- **Parts must be independently demoable.** If Part 2 can't run until Part 3
  exists, a candidate who runs out of time has nothing to show.
- **Don't name the pattern in the README.** "Use a hash map keyed by channel"
  removes the decision being tested; state the requirement, not the structure.
