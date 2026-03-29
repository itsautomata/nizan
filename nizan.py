"""nizan: interactive menu entry point."""

import os
import glob
from simple_term_menu import TerminalMenu
from config import MAX_ROUNDS, DEFAULT_MODE
from debate import run, reopen, RECORD_DIRS
from core import theme as t

GUIDELINES = {
    "normal": f"""
  {t.GREEN}┌─────────────────────────────────────────────────┐
  │  {t.BRIGHT_GREEN}{t.BOLD}NORMAL MODE{t.RESET}{t.GREEN}: structured debate                 │
  │                                                 │
  │  {t.RESET}frame your topic as a debatable question{t.GREEN}       │
  │  {t.RESET}with two genuine sides.{t.GREEN}                        │
  │                                                 │
  │  {t.BRIGHT_GREEN}good:{t.GREEN}                                          │
  │    {t.RESET}"should AI models be open source?"{t.GREEN}            │
  │    {t.RESET}"is remote work better than office work?"{t.GREEN}     │
  │                                                 │
  │  {t.DIM}bad:{t.RESET}{t.GREEN}                                           │
  │    {t.DIM}"what is machine learning?"  (not debatable){t.RESET}{t.GREEN}  │
  │    {t.DIM}"list the benefits of X"    (one-sided){t.RESET}{t.GREEN}       │
  └─────────────────────────────────────────────────┘{t.RESET}
""",
    "decision": f"""
  {t.GREEN}┌─────────────────────────────────────────────────┐
  │  {t.BRIGHT_GREEN}{t.BOLD}DECISION MODE{t.RESET}{t.GREEN}: structured decision analysis    │
  │                                                 │
  │  {t.RESET}frame your topic as a choice between two{t.GREEN}       │
  │  {t.RESET}specific alternatives.{t.GREEN}                         │
  │                                                 │
  │  {t.BRIGHT_GREEN}good:{t.GREEN}                                          │
  │    {t.RESET}"rust vs go for a new CLI tool"{t.GREEN}               │
  │    {t.RESET}"postgres vs mongodb for user analytics"{t.GREEN}      │
  │                                                 │
  │  {t.DIM}bad:{t.RESET}{t.GREEN}                                           │
  │    {t.DIM}"what database should I use?"  (too vague){t.RESET}{t.GREEN}    │
  │    {t.DIM}"is rust good?"               (not a choice){t.RESET}{t.GREEN}  │
  └─────────────────────────────────────────────────┘{t.RESET}
""",
}

MODES = ["normal", "decision", "reopen"]


def select_mode():
    print(t.banner())
    print(f"  {t.label('select mode:')}\n")
    menu = TerminalMenu(
        MODES,
        title="",
        cursor_index=MODES.index(DEFAULT_MODE),
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    idx = menu.show()
    if idx is None:
        return None
    return MODES[idx]


def show_guidelines(mode):
    print(GUIDELINES[mode])


def get_topic():
    topic = input(f"  {t.label('enter your topic:')} ").strip()
    if not topic:
        return None
    return topic


def get_context_file():
    path = input(f"  {t.dim('context file (optional, enter to skip):')} ").strip()
    if not path:
        return None
    path = os.path.expanduser(path)
    if not os.path.isfile(path):
        print(f"  {t.dim('file not found:')} {path}")
        return None
    return path


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
    print(f"\n  {t.label('what matters most?')} {t.dim('(pick up to 3, space to select, enter to confirm)')}\n")
    menu = TerminalMenu(
        PRIORITIES,
        title="",
        multi_select=True,
        show_multi_select_hint=True,
        multi_select_select_on_accept=False,
        multi_select_empty_ok=True,
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    indices = menu.show()
    if indices is None:
        return None
    if isinstance(indices, int):
        indices = (indices,)
    selected = [PRIORITY_KEYS[i] for i in indices]
    return selected[:3] if selected else None


def select_ruling():
    """list saved rulings and let the user pick one to reopen."""
    ruling_dir = RECORD_DIRS["decision"]
    if not os.path.isdir(ruling_dir):
        print(f"\n  {t.dim('no rulings found.')}\n")
        return None

    files = sorted(glob.glob(os.path.join(ruling_dir, "*.md")))
    if not files:
        print(f"\n  {t.dim('no rulings found.')}\n")
        return None

    names = [os.path.basename(f) for f in files]
    print(f"\n  {t.label('select ruling to reopen:')}\n")
    menu = TerminalMenu(
        names,
        title="",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    idx = menu.show()
    if idx is None:
        return None
    return files[idx]


def select_stress_test():
    print(f"\n  {t.label('stress-test the verdict?')} {t.dim('(challenges the ruling after it lands)')}\n")
    menu = TerminalMenu(
        ["no", "yes"],
        title="",
        cursor_index=0,
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    idx = menu.show()
    return idx == 1


def select_rounds():
    options = [str(r) for r in range(1, MAX_ROUNDS + 1)]
    print(f"\n  {t.label('select number of rounds:')}\n")
    menu = TerminalMenu(
        options,
        title="",
        cursor_index=1,  # default to 2 rounds
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    idx = menu.show()
    if idx is None:
        return None
    return int(options[idx])


def main():
    mode = select_mode()
    if mode is None:
        print(f"\n  {t.dim('cancelled.')}\n")
        return

    if mode == "reopen":
        ruling_path = select_ruling()
        if ruling_path is None:
            print(f"\n  {t.dim('cancelled.')}\n")
            return
        print()
        reopen(ruling_path)
        return

    show_guidelines(mode)

    topic = get_topic()
    if topic is None:
        print(f"\n  {t.dim('no topic entered.')}\n")
        return

    context_file = get_context_file()

    priorities = None
    if mode == "decision":
        priorities = select_priorities()

    rounds = select_rounds()
    if rounds is None:
        print(f"\n  {t.dim('cancelled.')}\n")
        return

    stress_test = select_stress_test()

    print()
    run(topic, mode=mode, rounds=rounds, priorities=priorities, context_file=context_file, stress_test=stress_test)


if __name__ == "__main__":
    main()
