"""nizan: clean saved records."""

import os
import glob
from simple_term_menu import TerminalMenu

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
        print(f"\n  {name}/ is already empty.\n")
        return

    print(f"\n  {len(files)} file(s) in {name}/:\n")
    for f in sorted(files):
        print(f"    {os.path.basename(f)}")

    confirm = input(f"\n  delete all? [y/N] ").strip().lower()
    if confirm != "y":
        print("\n  cancelled.\n")
        return

    for f in files:
        os.remove(f)
    print(f"\n  {name}/ cleaned. {len(files)} file(s) removed.\n")


def main():
    options = []
    for name, path in TARGETS.items():
        n = count_files(path)
        options.append(f"{name}  ({n} files)")

    print("\nnizan: clean records\n")
    print("select folder to clean:\n")
    menu = TerminalMenu(options, title="")
    idx = menu.show()
    if idx is None:
        print("\n  cancelled.\n")
        return

    name = list(TARGETS.keys())[idx]
    clean(name, TARGETS[name])


if __name__ == "__main__":
    main()
