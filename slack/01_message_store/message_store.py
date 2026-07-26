class MessageStore:
    def __init__(self) -> None:
        pass

    # --- Part 1: channel history ---

    def post_message(self, channel: str, user: str, text: str, ts: float) -> str:
        # Record a message in a channel. Return its id.

        pass

    def history(
        self, channel: str, limit: int = 50, before: str | None = None
    ) -> list[dict]:
        # Return a page of a channel's messages.

        pass

    # --- Part 2: threads ---

    def reply(self, parent_id: str, user: str, text: str, ts: float) -> str:
        # Attach a reply to an existing message. Return the reply's id.

        pass

    def thread(self, parent_id: str) -> list[dict]:
        # Return the conversation hanging off one message.

        pass

    # --- Part 3: unread counts ---

    def mark_read(self, user: str, channel: str, ts: float) -> None:
        # Record how far `user` has read in `channel`.

        pass

    def unread_count(self, user: str, channel: str) -> int:
        # How many messages in `channel` has `user` not seen?

        pass

    # --- Part 4 (stretch): search ---

    def search(self, query: str, channel: str | None = None) -> list[dict]:
        # Find messages by their text, optionally scoped to one channel.

        pass
