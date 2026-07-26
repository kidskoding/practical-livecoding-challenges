# Interviewer notes — In-Memory Message Store

Spoilers. Read after the attempt, not during. If you had to open this to get
unstuck, the thing to practice is asking, not coding.

## What candidates are being evaluated on

- **Questions asked before code is written.** Half the contract is missing on
  purpose. Working out what's missing, and pinning it down before you type, is
  the single strongest signal in this round.
- Working code for whatever contract you settled on. An assumption you named
  and coded against is a pass; an assumption you made silently is the failure
  mode this round is built to catch.
- Data modeling: what you index by, and why. More than one layout is
  reasonable — pick one and defend it.
- The edge cases you go looking for. Nothing in the prompt tells you which ones
  exist or what they should do. Finding them is the point; raising one out loud
  is worth as much as handling it.
- Narration. Say what you're about to do before you do it — silence is the most
  common way this interview goes badly.
- Knowing what you skipped. Naming a shortcut and its ceiling as you take it
  scores better than either silently taking it or silently avoiding it.

Not evaluated: distributed design, persistence, concurrency, auth. A candidate
reaching for those has left the scope — the good version says the tradeoff out
loud and moves on.

## Complexity to be ready to discuss

Expect to be asked, for any function you wrote:

- What it costs in your layout, and what a faster layout would trade away.
- Which work you chose to do on write versus on read, and what the other choice
  would have cost.
- What holds up at a thousand messages and stops holding up at ten million.
- Which assumption your implementation quietly depends on, and what breaks when
  it stops being true.

## The withheld contract

**`post_message`**

- Channels and users are never created explicitly; the first message posted to
  a name brings the channel into existence.
- `text` is stored verbatim — no trimming, no escaping, no length limit.
- The id is a string, unique across the **entire store**, not per channel. The
  format is the candidate's choice; nothing parses it.
- Every stored message carries all seven fields, with `reply_count = 0` and
  `last_reply_ts = None`.
- `ts` is supplied by the caller, never generated inside the store. Messages
  arrive in non-decreasing `ts` order — a candidate who asks what happens
  otherwise gets credit; one who assumes it silently doesn't.

**`history`**

- Newest first. Returns the message dicts, not ids.
- `limit` defaults to 50 and caps the page. A limit past the end returns what
  exists — no padding, no error.
- `before` is a message id and is **exclusive**: only messages strictly older.
  `before=None` starts from the newest.
- Unknown channel → `[]`. Empty channel → `[]`. Cursor at the oldest message →
  `[]`. None of these raise.
- Replies never appear here — top-level messages only.

**`reply`**

- The reply **inherits the parent's channel**; the caller doesn't pass one.
- It gets its own unique id, distinct from the parent's.
- Threads are one level deep. Replying to a reply is out of scope.
- The parent updates in place: `reply_count` increments, `last_reply_ts` moves
  to the newest reply's `ts` — and **never backwards** if a reply arrives with
  an older `ts`.

**`thread`**

- Parent first, then replies **oldest-first** — the opposite of `history`.
- A parent with no replies returns a one-element list, not an empty one.

**`mark_read`**

- Returns nothing. The marker is per `(user, channel)`; one user's marker never
  affects another's.
- It's a high-water mark: marking read at an **older** `ts` than the recorded
  one leaves the marker alone.
- Marking read on an unseen or empty channel is legal.

**`unread_count`**

- Counts top-level messages **strictly newer** than the marker. The marker is
  inclusive of itself: after `mark_read(user, ch, 2.0)`, the message at exactly
  `2.0` is read.
- **The user's own messages never count.**
- No marker → everything unread, minus their own.
- Unknown or empty channel → `0`.
- Replies don't count toward channel unreads; thread unreads are a separate
  surface.

**`search`**

- Case-insensitive substring match on `text`, newest first. No tokenizing, no
  stemming, no ranking beyond recency.
- Replies **are** searchable, unlike in `history`.
- `channel=None` searches everywhere; a channel scopes results.
- No match → `[]`.
