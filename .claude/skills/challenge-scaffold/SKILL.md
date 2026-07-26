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
2. The scenario in two or three sentences, plus the data shape (dict keys and
   types) — guessing a field name isn't a skill. Then a line saying the prompt
   is deliberately underspecified, that asking is graded, and that
   `## Interviewer notes` holds the answers for afterwards.
3. `## Part N — <name>` — the body of the prompt, see below. No per-part time
   estimate in the heading: the total duration is in the title, and a candidate
   watching a per-part clock is optimizing the wrong thing. Size the parts so
   the whole thing fits the duration with room for questions at the end, then
   leave the pacing unstated.
4. `## What candidates are being evaluated on` — questions asked before code
   goes first, since that's what the withheld contract is there to test. Then an
   explicit not-evaluated list (scaling, persistence, auth) so the candidate
   doesn't wander out of scope. **Don't enumerate the edge cases here.** Listing
   "unknown channel, empty result, cursor at the end" hands over the exact
   questions the parts withheld — say that edge cases exist and finding them is
   graded, and stop there.
5. `## Complexity to be ready to discuss` — 3–5 questions, phrased generically
   ("what it costs in your layout", "which work you do on write versus read")
   rather than named against a specific function. A question like "`history`
   with a `before` cursor — what does resolving it cost?" tells the candidate
   the cursor is worth resolving carefully, which is a design hint.
6. `## Interviewer notes` — the withheld contract, in full. Last section, see
   below.

## Writing A Part (the important bit)

**Underspecify on purpose.** These prompts mimic a live round, where the
interviewer states the goal and waits to see which questions come back. Half
the contract is withheld: ordering, boundaries, empty cases, tie-breaks. A
prompt that answers everything trains the candidate to implement a spec, which
is the one skill the real round doesn't test.

Everything withheld from the parts is written down once in `## Interviewer
notes` at the end, so the exercise stays checkable solo.

A part is one numbered block per function: a heading, one or two sentences of
intent, sometimes a product detail, and usually one example.

````markdown
### 2.1 — `reply`

Write a function called `reply` that hangs a reply off an existing message.

The channel view renders `"2 replies"` under a parent and only loads the thread
when the user clicks in.

#### Example

```text
#general holds  "deploy is red" (ana, ts 1.0, id = parent)

Input:
    parent_id = parent, user = "bo", text = "looking", ts = 2.0

Output:
    an id for the reply
```

### 2.2 — `thread`

Then write a function called `thread` that …
````

### What to state

- **The function name and what it's for**, in one or two sentences. Open with
  ``Write a function called `name` that …``, or ``Then write …`` for the second
  and later functions in a part. The candidate designs the internals, not the
  API surface.
- **The data shape**, once, in the intro — dict keys and types. Guessing a field
  name isn't a skill; guessing a boundary is.
- **The parameters by name** where they aren't obvious from the sentence
  (`It takes a \`limit\` and a \`before\` cursor`) — but not what they do.
- **The product detail that motivates the invariant**, when there is one ("the
  channel view renders `2 replies` without loading the thread"). It's a hint
  that something has to live on the parent, not a spec of what.
- **Hard scope bounds** — one in-memory object, no database, no concurrency —
  so nobody builds a service.

### What to withhold

Everything a careful engineer would ask about:

- Ordering. Newest-first or oldest-first, and whether two parts disagree.
- Boundaries. Inclusive or exclusive cursors, `>` vs `>=` on a marker.
- Empty and unknown cases. Missing key, empty collection, cursor at the end —
  and whether those return empty or raise.
- "Does X count." Own messages, replies, soft-deleted rows.
- Defaults, and what an out-of-range argument does.
- Whether an assumption holds at all (in-order writes, one level of nesting).

Withholding is not vagueness about the *goal*. "Return the page a client would
render" is a clear goal with an unstated contract; "do something with messages"
is just a bad prompt.

### Headings and numbering

- The heading is `### <part>.<n> — \`function_name\`` — the function's **name
  only**, never its signature or return type. The number makes it referrable out
  loud ("skip 3.2 if you're short on time") and gives a visible checklist.
- Number within the part: `1.1`, `1.2`, then `2.1`, `2.2`. The digit before the
  dot always matches the part number.
- Examples sit at `#### Example` under a function heading — `#### Examples` plus
  `##### Example N` when a function genuinely needs more than one.
- Separate parts with `---`. Each part must be attemptable on its own.

### Examples

**One example per function, happy path only.** The example exists to fix the
shape of the input and output, not to enumerate behavior. Edge cases are the
thing being withheld — an example showing `[]` for an unknown channel answers a
question the candidate was supposed to ask.

````markdown
#### Example

```text
#general holds  "one"   (ana, ts 1.0)
                "two"   (bo,  ts 2.0)
                "three" (ana, ts 3.0)

Input:
    channel = "#general", limit = 2

Output:
    ["three", "two"]
```
````

- **`Input:` holds only that function's arguments** — `channel = "#general",
  limit = 2`, one line per call, no function name, no other function's calls.
  `Output:` gives the result. Plain text, not Python: a spec, not a doctest.
- **Setup goes above `Input:` as state, not as calls.** Describe what the store
  holds. Setup written as `post_message(...)` calls drags another function's
  signature into an example that isn't about it — and writing it as state is
  what keeps functions independently attemptable, since a candidate stuck on 1.1
  is handed 1.2's starting contents outright.
- **An example never asserts through another function.** Calling `history` to
  show what `post_message` stored makes `history` a prerequisite for reading
  `post_message`. Describe the state instead: `an id for the stored message`.
- Keep the output loose where the contract is deliberately open — `an id for the
  reply`, not `"m2"`. A precise-looking output invites the candidate to infer a
  rule you meant to withhold.
- A second example is justified only when one can't show the input shape at all
  (a function whose arguments vary in kind). Never add one to cover an edge case.
- **Every function gets one, including the ones that look self-evident.** A
  function returning nothing still needs its argument shape pinned and its
  no-return-value stated: `Output: nothing; bo's read position in #general is
  recorded`. A missing example reads as an oversight and makes the candidate
  wonder what else was left out.
- Choose example data that can't be reverse-engineered into the withheld rules.
  A search example matching two messages leaks the result ordering; one that
  matches a single message shows the shape and nothing else. Same for a case
  whose query differs in case from the text — that answers whether matching is
  case-sensitive.

### Interviewer notes

The last section of the README, after the evaluation and complexity sections:

- A short line saying these are the answers to the withheld questions, to be
  read after the attempt.
- One bold sub-heading per function, then the bullets that would have been the
  spec: ordering, boundaries, empty cases, defaults, what doesn't count.
- Bold the words that invert behavior if misread (**exclusive**, **strictly
  newer**, **never backwards**).
- Note where asking is itself the graded behavior ("a candidate who asks what
  happens with out-of-order writes gets credit; one who assumes it silently
  doesn't").

This section is the only place the exhaustive contract exists. It's what makes
the prompt vague without making it unusable alone.

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

- **Over-specifying the part is the real failure.** The instinct is to write the
  complete contract into the bullets — inclusive cursor, empty-case behavior,
  what doesn't count. That produces a spec to implement, and implementing a spec
  is the one thing the live round doesn't test. Those rules go in
  `## Interviewer notes`, not the part.
- **Leaking the contract through an example.** An example showing `[]` for an
  unknown channel, or `["three", "two", "one"]` for an unfiltered call, answers
  a question the candidate was supposed to ask. One happy-path case, shaped to
  show the input and output types and nothing more.
- **Leaking it through the back sections instead.** The evaluation and
  complexity sections are the easiest place to give the game away — an
  edge-case checklist, or a complexity question naming the exact parameter that
  needs care. Keep both generic; the specifics live in the interviewer notes.
- **Vague about the goal instead of the contract.** "Do something with messages"
  is a bad prompt; "return the page a client would render" is a clear goal with
  a withheld contract. Withhold rules, never intent.
- **Forgetting the interviewer notes.** Without them nothing can be checked
  after the attempt, and the prompt becomes a guessing game with no answer key.
- **Asserting through a function the candidate hasn't written.** Setup describes
  state; the `Output:` line never calls another function. Demoing 1.1 via 1.2
  quietly makes the second function a prerequisite for the first.
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
