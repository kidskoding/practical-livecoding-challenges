class MessageStore:
    def __init__(self) -> None:
        pass

    # --- Part 1: channel history ---

    def post_message(self, channel: str, user: str, text: str, ts: float) -> str:
        # Store a top-level message in a channel. Return its id.

        pass

    def history(
        self, channel: str, limit: int = 50, before: str | None = None
    ) -> list[dict]:
        # Newest-first page of top-level messages. `before` is a message id,
        # exclusive: return only messages older than it.

        pass

    # --- Part 2: threads ---

    def reply(self, parent_id: str, user: str, text: str, ts: float) -> str:
        # Reply to a top-level message. Return the reply's id.

        pass

    def thread(self, parent_id: str) -> list[dict]:
        # Oldest-first: the parent followed by all of its replies.

        pass

    # --- Part 3: unread counts ---

    def mark_read(self, user: str, channel: str, ts: float) -> None:
        # Record that `user` has read `channel` up to and including `ts`.

        pass

    def unread_count(self, user: str, channel: str) -> int:
        # Top-level messages newer than the user's read marker, excluding
        # the user's own messages.

        pass

    # --- Part 4 (stretch): search ---

    def search(self, query: str, channel: str | None = None) -> list[dict]:
        # Newest-first messages whose text contains `query`, case-insensitive.
        # Searches replies too. `channel` scopes the search when given.

        pass
