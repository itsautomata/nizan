import re


class Sigil:
    """sigil, the shared record of the debate. every agent reads it before speaking."""

    def __init__(self, topic, mode="normal", priorities=None, context=None, context_source=None):
        self._entries = []
        self.topic = topic
        self.mode = mode
        self.priorities = priorities
        self.context = context
        self.context_source = context_source

    @classmethod
    def load(cls, path):
        """reconstruct a sigil from a saved ruling/sigil markdown file."""
        with open(path) as f:
            text = f.read()

        # parse metadata from header
        topic = ""
        mode = "normal"
        priorities = None
        context_source = None

        topic_match = re.search(r"^topic: (.+)$", text, re.MULTILINE)
        if topic_match:
            topic = topic_match.group(1).strip()

        mode_match = re.search(r"^mode: (.+)$", text, re.MULTILINE)
        if mode_match:
            mode = mode_match.group(1).strip()

        pri_match = re.search(r"^priorities: (.+)$", text, re.MULTILINE)
        if pri_match:
            priorities = [p.strip() for p in pri_match.group(1).split(",")]

        ctx_match = re.search(r"^context: (.+)$", text, re.MULTILINE)
        if ctx_match:
            context_source = ctx_match.group(1).strip()

        sigil = cls(topic, mode=mode, priorities=priorities, context_source=context_source)

        # parse entries: ## role followed by content until next --- or end
        parts = re.split(r"^## (\w+)\n", text, flags=re.MULTILINE)
        # parts[0] is header, then alternating: role, content, role, content...
        for i in range(1, len(parts) - 1, 2):
            role = parts[i].strip()
            content = parts[i + 1].strip()
            # remove trailing ---
            content = re.sub(r"\n---\s*$", "", content).strip()
            sigil.add(role, content)

        return sigil

    def add(self, role, content):
        self._entries.append({"role": role, "content": content})

    def render(self):
        lines = []
        if self.context:
            lines.append(f"[CONTEXT]:\n{self.context}")
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
        if self.context_source:
            lines.append(f"context: {self.context_source}\n")
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
