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
3. `## Part N — <name>` — the body of the prompt, see below. No per-part time
   estimate in the heading: the total duration is in the title, and a candidate
   watching a per-part clock is optimizing the wrong thing. Size the parts so
   the whole thing fits the duration with room for questions at the end, then
   leave the pacing unstated.
4. `## What candidates are being evaluated on` — plus an explicit not-evaluated list (scaling,
   persistence, auth) so the candidate doesn't wander out of scope.
5. `## Complexity to be ready to discuss` — 3–5 questions the interviewer asks,
   phrased as questions and left unanswered.

## Writing A Part (the important bit)

A part is one numbered block per function, repeated: a heading, a dictated
sentence, the bulleted contract, then that function's examples.

````markdown
### 2.1 — `reply`

Write a function called `reply` that attaches a reply to an existing top-level
message and returns the reply's own id.

- `parent_id` is the id returned by a previous `post_message`.
- The reply **inherits the parent's channel** — the caller doesn't pass one.

#### Examples

##### Example 1

```text
Input:
    parent = post_message("#general", "ana", "deploy is red", 1.0)
             reply(parent, "bo", "looking", 2.0)

Output:
    a new id, different from parent
```

### 2.2 — `thread`

Then write a function called `thread` that …
````

- The heading is `### <part>.<n> — \`function_name\`` — the function's **name
  only**, never its signature or return type. The number makes it referrable
  out loud ("skip 3.2 if you're short on time") and gives the candidate a
  visible checklist of what's left.
- Number within the part: `1.1`, `1.2`, then `2.1`, `2.2`. The digit before the
  dot always matches the part number.
- Under a function heading, examples sit at `#### Examples`, and each case at
  `##### Example N`.

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
- **Never put the signature in the heading.** `### 1.2 — \`history\``, not
  `### \`history(channel, limit=50, before=None) -> list[dict]\``. The stub file
  already carries the signature and the bullets name every parameter, so a
  repeated signature is noise that also goes stale.
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
- **Give examples per function, not per part**, under a `#### Examples` heading
  after that function's bullets, each case its own `##### Example N` with an
  `Input:` / `Output:` / `Explanation:` block — the shape a real OA doc uses:

````markdown
#### Examples

##### Example 1

```text
Input:
    oldest = post_message("#general", "ana", "one",   1.0)
             post_message("#general", "bo",  "two",   2.0)
    third  = post_message("#general", "ana", "three", 3.0)

    history("#general", limit=2)
    history("#general", before=third)

Output:
    ["three", "two"]
    ["two", "one"]

Explanation:
    Newest first, and `before` is exclusive — `third` itself is never in
    the page.
```
````

- `Input:` is the call sequence, indented, including whatever setup the case
  needs. `Output:` lists one result per call, in the same order. Both are plain
  text, not Python — this is a spec, not a doctest.
- `Explanation:` goes **inside** the block, last, and only when the output
  isn't self-evident. A case that speaks for itself (`search("nothing")` → `[]`)
  gets no explanation; don't pad one in. Never leave the prose floating outside
  the fence.
- **1–3 examples, however many the contract actually needs** — not three by
  default. Stop when every rule in the bullets has a case. One is plenty for a
  function with a single behavior; three is the ceiling, not the target. Two
  cases that differ only cosmetically should be one case with two calls in it.
- **At least one example is an edge case,** and it's the one the bullets are
  most likely to be misread on: empty input, unknown key, cursor at the oldest
  item, single element, the user's own message, an out-of-order write. If a rule
  is stated in bold, some example pins it.
- Where several cases share setup, state it once above `##### Example 1`
  ("Both examples start from this channel:") and write `(same channel as above)`
  in the later `Input:` blocks.
- **Every function gets its own `#### Examples`, no sharing.** The block goes
  immediately after that function's bullets and before the next function's
  prose — never one combined block at the end of the part. A candidate reads one
  function, sees its cases, writes it, moves on; a merged block forces them to
  hold two contracts in their head at once.
- A function that returns nothing still gets examples. Describe the resulting
  state as the `Output:` (`bo's marker in #general is 5.0`). Reach for the
  reader function only if the state is otherwise impossible to express.
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

Check that the whole thing is satisfiable in the stated duration, that no example in
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
  and boundary rules stop being arguable — and one happy-path case alone doesn't
  do that. Pair it with the edge case.
- **Padding to three examples.** 1–3 means as many as the contract needs. Three
  near-identical cases read as filler and cost the candidate time.
- **Explanation prose left outside the block.** It belongs on an
  `Explanation:` line inside the fence, or nowhere.
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
