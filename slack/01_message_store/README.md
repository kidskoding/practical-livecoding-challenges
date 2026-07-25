# Slack (a Salesforce company) — 60 Minute Practical Coding Challenge: In-Memory Message Store

You're building the storage layer behind a chat product's channel view.
Everything lives in memory in a single `MessageStore` object — no database, no
threads, no network. Timestamps are supplied by the caller (`ts: float`),
never generated inside the store, so behavior is reproducible.

A message is a plain `dict` like the one shown below:

```python
{
    "id": "<unique string>",
    "channel": "#general",
    "user": "ana",
    "text": "deploy is red",
    "ts": 1.0,
    "reply_count": 0,        # top-level messages only
    "last_reply_ts": None,   # top-level messages only; ts of the newest reply
}
```

Replies carry `id`, `channel`, `user`, `text`, `ts` — nothing reads any other
field off them.

Work in `message_store.py`. The method signatures are already stubbed there;
implement them in part order. How you store things internally is entirely your
call — that decision is the point of the exercise.

Examples below write results as message texts for brevity; the real return
value is the list of message dicts.

---

## Part 1 — channel history

### 1.1 — `post_message`

Write a function called `post_message` that records a new top-level message in a channel
and returns its id.

- `channel` is a string like `"#general"`. Channels are never created
  explicitly — the first message posted to a name brings it into existence.
- `user` is a string like `"ana"`. There is no user registry either.
- `text` is the message body, stored verbatim: no trimming, no escaping, no
  length limit.
- `ts` is a float supplied by the caller. Assume messages arrive in
  non-decreasing `ts` order within a channel, but say out loud what breaks if
  they don't.
- The returned id is a string, unique across the **entire store** — not just
  within the channel. Its format is yours to choose; nothing parses it. It is
  the handle callers use later for `before` cursors and thread parents.
- Every stored message carries all seven fields from the shape above.
  `reply_count` starts at `0` and `last_reply_ts` starts at `None`.

#### Examples

##### Example 1

```text
Input:
    channel = "#general", user = "ana", text = "one", ts = 1.0

Output:
    a new id string, and the stored message reads
    {"id": <that id>, "channel": "#general", "user": "ana", "text": "one",
     "ts": 1.0, "reply_count": 0, "last_reply_ts": None}

Explanation:
    A freshly posted message carries all seven fields, with the thread
    fields at their starting values.
```

##### Example 2

Two calls, one after the other:

```text
Input:
    channel = "#general", user = "ana", text = "one", ts = 1.0
    channel = "#random",  user = "cy",  text = "one", ts = 1.0

Output:
    two different id strings

Explanation:
    Same text, same timestamp, different channels — still distinct ids.
    Ids are unique across the whole store, not per channel.
```

### 1.2 — `history`

Then write a function called `history` that returns one page of a channel's top-level
messages, **newest first**.

- Return the message dicts themselves, not ids.
- `limit` caps the page size. A `limit` larger than the number of available
  messages returns everything available — never pad, never error.
- `before` is a message id and is **exclusive**: return only messages strictly
  older than that message. `before=None` (the default) starts from the newest
  message in the channel.
- Together, `limit` and `before` give cursor pagination: a client renders a
  page, takes the id of the last (oldest) message it received, and passes it
  back as `before` to get the next page going backwards in time.
- An unknown channel returns `[]`. A channel with no messages returns `[]`.
  Neither is an error.
- A `before` cursor pointing at the oldest message in the channel returns `[]`.
- Replies (Part 2) never appear here — only top-level messages.

#### Examples

All three examples run against this channel:

```text
#general holds  "one" (ana, ts 1.0, id = oldest)
                "two" (bo,  ts 2.0)
                "three" (ana, ts 3.0, id = third)
```

##### Example 1

```text
Input:
    channel = "#general"
    channel = "#general", limit = 2
    channel = "#general", limit = 99

Output:
    ["three", "two", "one"]
    ["three", "two"]
    ["three", "two", "one"]

Explanation:
    Newest first. A limit past the end of the channel returns what exists —
    no padding, no error.
```

##### Example 2

```text
Input:
    channel = "#general", limit = 1, before = third
    channel = "#general", before = third

Output:
    ["two"]
    ["two", "one"]

Explanation:
    `before` is exclusive, so `third` itself is never in the page. This is
    how a client walks backwards: render a page, then pass the id of its
    last message back as the next `before`.
```

##### Example 3

```text
Input:
    channel = "#general", before = oldest
    channel = "#nope"

Output:
    []
    []

Explanation:
    Nothing is older than `oldest`, and `#nope` has never been posted to.
    Both are empty pages, not errors.
```

---

## Part 2 — threads

### 2.1 — `reply`

Write a function called `reply` that attaches a reply to an existing top-level message
and returns the reply's own id.

- `parent_id` is the id returned by a previous `post_message`.
- The reply **inherits the parent's channel** — the caller doesn't pass one.
- The reply gets its own unique id, distinct from the parent's.
- Threads are one level deep. Replying to a reply is out of scope; you may
  assume it doesn't happen, but say what you'd do about it.
- Posting a reply updates the parent in place: `reply_count` increments by one,
  and `last_reply_ts` becomes the timestamp of the newest reply so far. If a
  reply somehow arrives with an older `ts` than one already recorded,
  `last_reply_ts` must not move backwards.

#### Examples

Both examples run against this message:

```text
#general holds  "deploy is red" (ana, ts 1.0, id = parent)
```

##### Example 1

```text
Input:
    parent_id = parent, user = "bo", text = "looking", ts = 2.0

Output:
    a new id, different from parent, in channel "#general"
    the parent now reads reply_count = 1, last_reply_ts = 2.0

Explanation:
    The reply's channel is inherited — nobody passed one. The parent's
    counters move on every reply so the channel view can render "1 reply"
    without loading the thread.
```

##### Example 2

Three calls, one after the other:

```text
Input:
    parent_id = parent, user = "bo",  text = "looking",   ts = 2.0
    parent_id = parent, user = "ana", text = "fixed",     ts = 5.0
    parent_id = parent, user = "cy",  text = "late note", ts = 3.0

Output:
    the parent reads reply_count = 3, last_reply_ts = 5.0

Explanation:
    The third reply is older than the second. The count still goes up, but
    last_reply_ts stays at 5.0 — it never moves backwards.
```

### 2.2 — `thread`

Then write a function called `thread` that returns the full conversation for one
top-level message: the **parent first**, then its replies **oldest-first**.

- A parent with no replies returns a one-element list containing just the
  parent.
- The ordering here is deliberately the opposite of `history` — a channel reads
  newest-first, a thread reads top-to-bottom like a transcript.

#### Examples

Both examples run against this channel:

```text
#general holds  "deploy is red" (ana, ts 1.0, id = parent)
                  └ "looking" (bo,  ts 2.0)
                  └ "fixed"   (ana, ts 5.0)
                "standup in 5" (cy, ts 6.0, id = solo, no replies)
```

##### Example 1

```text
Input:
    parent_id = parent

Output:
    ["deploy is red", "looking", "fixed"]

Explanation:
    Parent first, then replies oldest-first — the opposite order from
    history().
```

##### Example 2

```text
Input:
    parent_id = solo

Output:
    ["standup in 5"]

Explanation:
    A message with no replies is a one-element thread, not an empty one.
```

### The constraint that matters

Replies must **not** appear in `history()`. The channel view renders a parent
with `"2 replies"` underneath it and only loads the thread when the user clicks
in — so the counts have to live on the parent and be readable without touching
the replies at all.

---

## Part 3 — unread counts

### 3.1 — `mark_read`

Write a function called `mark_read` that records how far a given user has read
in a given channel. Returns nothing.

- The marker is per `(user, channel)` pair. Reading `#general` says nothing
  about `#random`, and one user's marker never affects another's.
- The marker is a high-water mark: calling it with an **older** `ts` than the
  one already recorded must leave the marker where it is. Scrolling back
  through old history can't make read messages unread again.
- Marking read on a channel the user has never seen, or that has no messages,
  is legal and does nothing surprising.

#### Examples

##### Example 1

Three calls, one after the other:

```text
Input:
    user = "bo", channel = "#general", ts = 2.0
    user = "bo", channel = "#general", ts = 5.0
    user = "bo", channel = "#general", ts = 1.0

Output:
    bo's marker in #general is 5.0

Explanation:
    The third call is older than what's already recorded, so it's ignored —
    the marker only ever moves forward.
```

##### Example 2

Three calls, one after the other:

```text
Input:
    user = "bo", channel = "#general", ts = 5.0
    user = "cy", channel = "#general", ts = 1.0
    user = "bo", channel = "#random",  ts = 3.0

Output:
    bo/#general = 5.0, cy/#general = 1.0, bo/#random = 3.0

Explanation:
    Markers are per (user, channel), so cy's read state never touches bo's.
    #random has no messages yet, which is still a legal call.
```

### 3.2 — `unread_count`

Then write a function called `unread_count` that returns how many messages in
that channel the user hasn't seen.

- Count top-level messages with `ts` **strictly greater** than the user's
  marker. The marker is inclusive of itself: after `mark_read(user, ch, 2.0)`,
  the message at exactly `ts=2.0` counts as read.
- **Exclude the user's own messages.** You never have unreads from yourself.
- A user with no marker for the channel has everything unread — minus their own
  messages.
- An unknown or empty channel returns `0`.
- Replies do **not** count toward channel unreads. Thread unreads are a
  separate product surface; mention how you'd approach it, don't build it.

#### Examples

Both examples run against this channel:

```text
#general holds  "one"   (ana, ts 1.0)
                "two"   (bo,  ts 2.0)
                "three" (ana, ts 3.0)
```

##### Example 1

Nobody has read anything yet:

```text
Input:
    user = "bo", channel = "#general"
    user = "cy", channel = "#general"

Output:
    2
    3

Explanation:
    Everything is unread — except that "two" is bo's own message and never
    counts against bo.
```

##### Example 2

Now bo's marker in `#general` is 5.0, having been rewound to 1.0 and ignored:

```text
Input:
    user = "bo", channel = "#general"
    user = "bo", channel = "#random"

Output:
    0
    0

Explanation:
    Everything up to 5.0 is read, so nothing is left. A channel that doesn't
    exist has no unreads either.
```

---

## Part 4 — search, if time remains

### 4.1 — `search`

Write a function called `search` that returns every message whose `text`
contains `query`, **newest first**.

- Matching is a case-insensitive substring test: `"RED"` matches
  `"Deploy is red"` and `"redis is slow"`. No tokenizing, no stemming, no
  ranking beyond recency.
- Replies **are** searchable, unlike in `history`.
- `channel=None` searches everywhere; passing a channel scopes results to it.
- No match returns `[]`.

#### Examples

Both examples run against these messages:

```text
#general holds  "Deploy is red" (ana, ts 1.0)
                  └ "rolled back" (bo, ts 3.0)
#random  holds  "redis is slow" (cy, ts 2.0)
```

##### Example 1

```text
Input:
    query = "RED"
    query = "rolled"

Output:
    ["redis is slow", "Deploy is red"]
    ["rolled back"]

Explanation:
    Matching ignores case and matches inside words, so "RED" hits both
    "Deploy is red" and "redis is slow". Replies are searchable even though
    they never appear in history().
```

##### Example 2

```text
Input:
    query = "red", channel = "#general"
    query = "nothing"

Output:
    ["Deploy is red"]
    []
```

Leave the last ~5 minutes for questions.

---

## What candidates are being evaluated on

- Working code that matches the spec above. Correctness first, prettiness
  second.
- Data modeling: what you index by, and why. There's more than one reasonable
  layout — pick one and defend it.
- Edge cases you handle without being told (unknown channel, empty result,
  cursor pointing at the oldest message, `limit` larger than the channel).
- Narration: say what you're about to do before you do it. Silence is the most
  common way this interview goes badly.
- Knowing what you skipped. "Linear scan for search is fine at this size; a
  real one needs an inverted index" scores better than silently doing either.

Not evaluated: distributed design, persistence, concurrency, auth. If you find
yourself reaching for those, you've left the scope — say the tradeoff out loud
and move on.

## Complexity to be ready to discuss

- `history` with a `before` cursor — what does resolving that cursor cost in
  your layout, and what would make it O(log n) or better?
- `unread_count` — you can recount on every call or maintain a counter on
  write. Which did you pick, and what does the other one cost?
- `search` — why is a linear scan acceptable here, and what changes at 10M
  messages?
- Posts arriving out of `ts` order — what breaks, and what's the smallest fix?
