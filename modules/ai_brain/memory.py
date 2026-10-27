class ConversationMemory:
    """Stores recent conversation history for context-aware responses."""

    def __init__(self, max_messages=10):
        self.max_messages = max_messages
        self.messages = []
        print(f"[MEMORY] Initialized with max {max_messages} messages.")

    def add_user(self, text):
        """Add user message to memory."""
        self.messages.append({"role": "user", "content": text})
        self._trim()

    def add_assistant(self, text):
        """Add assistant message to memory."""
        self.messages.append({"role": "assistant", "content": text})
        self._trim()

    def get_history(self):
        """Return copy of conversation history for LLM context."""
        return self.messages.copy()

    def _trim(self):
        """Keep only last N messages to prevent context overflow."""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]

    def clear(self):
        """Clear all memory (for new session)."""
        self.messages = []