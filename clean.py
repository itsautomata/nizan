"""nizan: clean saved records."""

import os
import glob
from simple_term_menu import TerminalMenu
from core import theme as t

BASE_DIR = os.path.dirname(__file__)

TARGETS = {
    "sigil": os.path.join(BASE_DIR, "sigil"),
    "ruling": os.path.join(BASE_DIR, "ruling"),
}


def count_files(path):
    return len(glob.glob(os.path.join(path, "*.md")))


def clean(name, path):
    files = glob.glob(os.path.join(path, "*.md"))
    if not files:
        print(f"\n  {t.dim(f'{name}/ is already empty.')}\n")
        return

    print(f"\n  {t.label(f'{len(files)} file(s) in {name}/:')}\n")
    for f in sorted(files):
        print(f"    {t.dim(os.path.basename(f))}")

    confirm = input(f"\n  {t.label('delete all?')} {t.dim('[y/N]')} ").strip().lower()
    if confirm != "y":
        print(f"\n  {t.dim('cancelled.')}\n")
        return

    for f in files:
        os.remove(f)
    print(f"\n  {t.header(f'{name}/ cleaned.')} {t.dim(f'{len(files)} file(s) removed.')}\n")


def main():
    options = []
    for name, path in TARGETS.items():
        n = count_files(path)
        options.append(f"{name}  ({n} files)")

    print(f"\n{t.header('nizan: clean records')}\n")
    print(f"  {t.label('select folder to clean:')}\n")
    menu = TerminalMenu(
        options,
        title="",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
    )
    idx = menu.show()
    if idx is None:
        print(f"\n  {t.dim('cancelled.')}\n")
        return

    name = list(TARGETS.keys())[idx]
    clean(name, TARGETS[name])


if __name__ == "__main__":
    main()
