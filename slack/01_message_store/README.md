# Software Engineering Intern Slack (a Salesforce company) — Mock Interview (Techinical Live Coding)

You're building the storage layer behind a chat product's channel view.
Everything lives in memory in a single `MessageStore` object — no database, no
network, no concurrency.

A message is a plain `dict` like the one shown below:

```python
{
    "id": "<unique string>",
    "channel": "#general",
    "user": "ana",
    "text": "deploy is red",
    "ts": 1.0,
    "reply_count": 0,
    "last_reply_ts": None,
}
```

---

## Part 1 — channel history

### 1.1 — `post_message`

Write a function called `post_message` that records a new message in a channel
and hands back something the caller can refer to it by later.

#### Example

```text
Input:
    channel = "#general", user = "ana", text = "one", ts = 1.0

Output:
    an id for the stored message
```

### 1.2 — `history`

Then write a function called `history` that returns a page of a channel's
messages. It takes a `limit` and a `before` cursor.

The client renders a channel by asking for a page, then asks for the next page
as the user scrolls up.

#### Example

```text
#general holds  "one"   (ana, ts 1.0)
                "two"   (bo,  ts 2.0)
                "three" (ana, ts 3.0, id = third)

Input:
    channel = "#general", limit = 2
    channel = "#general", limit = 2, before = third

Output:
    ["three", "two"]
    the next page of two, continuing from `third`
```

Results are written as message texts for brevity; the real return value is the
message dicts.

---

## Part 2 — threads

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

Then write a function called `thread` that returns the conversation hanging off
one message.

#### Example

```text
#general holds  "deploy is red" (ana, ts 1.0, id = parent)
                  └ "looking" (bo,  ts 2.0)
                  └ "fixed"   (ana, ts 5.0)

Input:
    parent_id = parent

Output:
    ["deploy is red", "looking", "fixed"]
```

---

## Part 3 — unread counts

### 3.1 — `mark_read`

Write a function called `mark_read` that records how far a user has read in a
channel.

#### Example

```text
#general holds  "one" (ana, ts 1.0)
                "two" (bo,  ts 2.0)

Input:
    user = "bo", channel = "#general", ts = 2.0

Output:
    nothing; bo's read position in #general is recorded
```

### 3.2 — `unread_count`

Then write a function called `unread_count` that returns how many messages in a
channel a user hasn't seen.

#### Example

```text
#general holds  "one"   (ana, ts 1.0)
                "two"   (bo,  ts 2.0)
                "three" (ana, ts 3.0)

    bo has read up to ts 2.0

Input:
    user = "bo", channel = "#general"

Output:
    1
```

---

## Part 4 — search, if time remains

### 4.1 — `search`

Write a function called `search` that finds messages by their text, optionally
scoped to one channel.

#### Example

```text
#general holds  "deploy is red" (ana, ts 1.0)
#random  holds  "lunch?"        (cy,  ts 2.0)

Input:
    query = "red"
    query = "red", channel = "#random"

Output:
    ["deploy is red"]
    []
```
