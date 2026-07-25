---
name: company-framing
description: 'Use when choosing and framing the problem for a practical live-coding challenge in this repo — e.g. "what should the Cloudflare challenge be?", "frame this as a Neuralink problem", "make this Slack-specific" — to pick a problem drawn from the company''s real domain and write the prompt the way that company actually interviews.'
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Company Framing

These companies don't ask LeetCode. They hand you a small piece of the product
they actually run and watch you build it. Framing means picking a problem that
is genuinely theirs and writing it as a product requirement, not a puzzle.

Use with `challenge-scaffold`: this skill decides *what the problem is and how
it reads*; that one decides *which files exist and their shape*.

## When To Use

- "What should the `<company>` challenge be?"
- "Frame this as a `<company>` problem."
- "Rewrite this prompt so it sounds like a real `<company>` interview."

## Pick From The Company's Real Surface

The problem must be a component the company plausibly runs in production, small
enough to build in the time budget.

| Company    | Domain surface                          | Challenge-sized pieces                                                        |
| ---------- | --------------------------------------- | ----------------------------------------------------------------------------- |
| Slack      | messaging, channels, presence           | message store with threads/unreads, mention parsing, `/remind` scheduling      |
| Cloudflare | edge proxy, DNS, caching, rate limiting | sliding-window rate limiter, LRU cache with TTL, CIDR match, log aggregation   |
| Neuralink  | signal streams, device telemetry        | spike detection over a sample buffer, ring buffer, sensor calibration table    |
| Stripe     | payments, ledgers, idempotency          | idempotency key store, currency-safe ledger, webhook retry with backoff        |
| Figma      | documents, layers, multiplayer          | layer tree with z-order, undo/redo stack, cursor presence                      |

If a chosen problem would work unchanged for any other company, it isn't framed
— it's a generic exercise with a logo on it.

## Write It As A Product Requirement

- **State the scenario in the company's nouns.** Channels and replies, not
  "nodes and children". Requests and edge PoPs, not "items and buckets". The
  vocabulary is the frame; a themed first sentence over generic prose is not.
- **Give the exact contract.** Method signatures, dict keys, return types, who
  supplies timestamps. The candidate designs the internals — never the API
  surface, and never the field names.
- **Requirements, not structures.** "Unknown channel returns `[]`" is a
  requirement. "Use a `defaultdict`" is the answer. Say the first.
- **Name the product reason for each rule.** "The channel list renders `2
  replies` under the parent without loading the thread" tells the candidate why
  `reply_count` lives on the parent, which is how a real ticket reads.
- **Bound the scope explicitly.** One in-memory object; no database, no
  network, no concurrency. State it in the prompt so nobody builds a service.
- **Stage it in independently demoable parts,** each with a time budget. A
  practical interview is graded partly on shipping something that runs at the
  30-minute mark.

## Hard Rules

- **No `Difficulty:` label, no pattern name.** Never say "this is a hash-map
  problem" or "you'll want two pointers". State the requirement.
- **No source link.** Unlike the DSA repos, these aren't LeetCode reskins. If
  the problem was adapted from a public write-up, leave the citation out of the
  prompt entirely — it spoils the modeling decision.
- **No hints about the intended data model.** The modeling choice is the thing
  being graded.
- **Ambiguity is a bug, not a test.** If a rule can be read two ways, pin it
  down. Practical interviews reward asking clarifying questions live; a written
  practice prompt has nobody to ask.
- **Company-plausible, not company-confidential.** Model the public product
  surface. Don't dress an exercise up as leaked internal work.

## Multi-Part And Follow-Ups

A later part may extend the same scenario into materially harder territory
(channel history → threads → per-user unreads). Keep the story continuous and
change the contract slightly at each step so earlier code has to be revisited,
not just called again. Extensions that don't fit the time budget are verbal
follow-ups — mention them in `## Complexity to be ready to discuss` as
questions, and leave them out of the parts.

## Gotchas

- **Logo-swapping.** Renaming `Cache` to `EdgeCache` and shipping the same
  generic exercise is the most common failure. Ask: would this problem exist on
  that company's roadmap? If not, pick a different one.
- **Framing that hides the requirement.** Story is the wrapper, not a riddle.
  If a candidate has to reverse-engineer what "settle the ledger" means, the
  prompt failed — the ask is always a plain directive.
- **Puzzle smuggled in as product.** If the interesting part is an algorithmic
  trick rather than modeling and edge cases, it belongs in the DSA repos.
- **Time budget written after the fact.** Decide the minutes per part while
  choosing the problem; a part that can't be built in its budget is a scoping
  error you'll only find by trying it.
- **Follow-ups leaking into the prompt.** "Later we'll add reactions" invites
  premature abstraction. Keep future work out of the parts entirely.
