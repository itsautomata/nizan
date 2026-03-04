"""nizan: interactive menu entry point."""

from simple_term_menu import TerminalMenu
from config import MAX_ROUNDS, DEFAULT_MODE
from debate import run

GUIDELINES = {
    "normal": """
  ┌─────────────────────────────────────────────────┐
  │  NORMAL MODE: structured debate                  │
  │                                                 │
  │  frame your topic as a debatable question       │
  │  with two genuine sides.                        │
  │                                                 │
  │  good:                                          │
  │    "should AI models be open source?"            │
  │    "is remote work better than office work?"     │
  │                                                 │
  │  bad:                                           │
  │    "what is machine learning?"  (not debatable)  │
  │    "list the benefits of X"    (one-sided)       │
  └─────────────────────────────────────────────────┘
""",
    "decision": """
  ┌─────────────────────────────────────────────────┐
  │  DECISION MODE: structured decision analysis     │
  │                                                 │
  │  frame your topic as a choice between two       │
  │  specific alternatives.                         │
  │                                                 │
  │  good:                                          │
  │    "rust vs go for a new CLI tool"               │
  │    "postgres vs mongodb for user analytics"      │
  │                                                 │
  │  bad:                                           │
  │    "what database should I use?"  (too vague)    │
  │    "is rust good?"               (not a choice)  │
  └─────────────────────────────────────────────────┘
""",
}

MODES = ["normal", "decision"]


def select_mode():
    print("\nnizan\n")
    print("select mode:\n")
    menu = TerminalMenu(
        MODES,
        title="",
        cursor_index=MODES.index(DEFAULT_MODE),
    )
    idx = menu.show()
    if idx is None:
        return None
    return MODES[idx]


def show_guidelines(mode):
    print(GUIDELINES[mode])


def get_topic():
    topic = input("  enter your topic: ").strip()
    if not topic:
        return None
    return topic


PRIORITIES = [
    "reversibility       — I need to be able to undo this",
    "risk tolerance      — I can't afford to fail",
    "time pressure       — I need to decide now",
    "cost                — resources are limited",
    "optionality         — keep future paths open",
    "long-term alignment — must fit where I'm going",
]

PRIORITY_KEYS = [
    "reversibility",
    "risk tolerance",
    "time pressure",
    "cost",
    "optionality",
    "long-term alignment",
]


def select_priorities():
    print("\nwhat matters most? (pick up to 3, space to select, enter to confirm)\n")
    menu = TerminalMenu(
        PRIORITIES,
        title="",
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        multi_select_empty_ok=True,
    )
    indices = menu.show()
    if indices is None:
        return None
    if isinstance(indices, int):
        indices = (indices,)
    selected = [PRIORITY_KEYS[i] for i in indices]
    return selected[:3] if selected else None


def select_rounds():
    options = [str(r) for r in range(1, MAX_ROUNDS + 1)]
    print("\nselect number of rounds:\n")
    menu = TerminalMenu(
        options,
        title="",
        cursor_index=1,  # default to 2 rounds
    )
    idx = menu.show()
    if idx is None:
        return None
    return int(options[idx])


def main():
    mode = select_mode()
    if mode is None:
        print("\n  cancelled.\n")
        return

    show_guidelines(mode)

    topic = get_topic()
    if topic is None:
        print("\n  no topic entered.\n")
        return

    priorities = None
    if mode == "decision":
        priorities = select_priorities()

    rounds = select_rounds()
    if rounds is None:
        print("\n  cancelled.\n")
        return

    print()
    run(topic, mode=mode, rounds=rounds, priorities=priorities)


if __name__ == "__main__":
    main()
