class Sigil:
    """sigil, the shared record of the debate. every agent reads it before speaking."""

    def __init__(self, topic, mode="normal", priorities=None):
        self._entries = []
        self.topic = topic
        self.mode = mode
        self.priorities = priorities

    def add(self, role, content):
        self._entries.append({"role": role, "content": content})

    def render(self):
        lines = []
        for entry in self._entries:
            lines.append(f"[{entry['role'].upper()}]:\n{entry['content']}")
        return "\n\n---\n\n".join(lines)

    def save(self, path):
        """save the full record as markdown."""
        artifact = "debate sigil" if self.mode == "normal" else "ruling"
        lines = [f"# nizan: {artifact}\n"]
        lines.append(f"topic: {self.topic}\n")
        lines.append(f"mode: {self.mode}\n")
        if self.priorities:
            lines.append(f"priorities: {', '.join(self.priorities)}\n")
        lines.append("---\n")
        for entry in self._entries:
            lines.append(f"## {entry['role']}\n")
            lines.append(f"{entry['content']}\n")
            lines.append("---\n")
        with open(path, "w") as f:
            f.write("\n".join(lines))

    def is_empty(self):
        return len(self._entries) == 0

    def __len__(self):
        return len(self._entries)
