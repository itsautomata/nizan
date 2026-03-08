"""nizan: the scale that weighs both sides."""

import os
import re
import sys
from datetime import date
from core.sigil import Sigil
from agents import moderator, advocate, critic, judge
from config import ROUNDS, DEFAULT_MODE
from core import rag

RECORD_DIRS = {
    "normal": os.path.join(os.path.dirname(__file__), "sigil"),
    "decision": os.path.join(os.path.dirname(__file__), "ruling"),
}


def slugify(text):
    """turn a topic into a filename-safe slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[\s_]+", "-", text)[:60]


def run(topic, mode=DEFAULT_MODE, rounds=ROUNDS, priorities=None, context_file=None, interactive=True):
    context = None
    context_source = None

    if context_file:
        context_source = os.path.basename(context_file)
        print(f"\n  loading context from {context_source}...")
        n = rag.load(context_file)
        context = rag.retrieve(topic)
        print(f"  {n} chunks indexed, top 5 retrieved.\n")

    sigil = Sigil(topic, mode=mode, priorities=priorities, context=context, context_source=context_source)

    label = "structured debate" if mode == "normal" else "decision analysis"
    print(f"\nnizan: {label}\n")
    print(f"topic: {topic}")
    header = f"mode: {mode} | rounds: {rounds}"
    if priorities:
        header += f" | priorities: {', '.join(priorities)}"
    if context_source:
        header += f" | context: {context_source}"
    print(header + "\n")
    print("=" * 60)

    # moderator frames the debate
    print("\n[MODERATOR] framing the debate...\n")
    framing = moderator.respond(topic, mode=mode)
    sigil.add("moderator", framing)
    print("\n\n" + "-" * 60)

    # debate rounds
    for round_num in range(1, rounds + 1):
        if round_num == 1:
            adv_label = "opening argument"
            crt_label = "counter-argument" if mode == "normal" else "opening argument"
        else:
            adv_label = f"rebuttal (round {round_num})"
            crt_label = f"rebuttal (round {round_num})"

        print(f"\n[ADVOCATE] {adv_label}...\n")
        adv_response = advocate.respond(sigil, mode=mode)
        sigil.add("advocate", adv_response)
        print("\n\n" + "-" * 60)

        print(f"\n[CRITIC] {crt_label}...\n")
        crt_response = critic.respond(sigil, mode=mode)
        sigil.add("critic", crt_response)
        print("\n\n" + "-" * 60)

    # judge delivers verdict
    judge_label = "evaluating" if mode == "normal" else "analyzing"
    print(f"\n[JUDGE] {judge_label}...\n")
    verdict = judge.respond(sigil, mode=mode, priorities=priorities)
    sigil.add("judge", verdict)
    print("\n\n" + "=" * 60)

    # reopening loop (decision mode, interactive only)
    if mode == "decision" and interactive:
        reopen_num = 0
        while True:
            factor = input("\n  new factor? (enter to finish): ").strip()
            if not factor:
                break
            reopen_num += 1

            sigil.add("new_factor", factor)
            print(f"\n[NEW FACTOR #{reopen_num}] {factor}")
            print("\n" + "-" * 60)

            print("\n[ADVOCATE] reopening argument...\n")
            adv_response = advocate.respond(sigil, mode="reopen")
            sigil.add("advocate", adv_response)
            print("\n\n" + "-" * 60)

            print("\n[CRITIC] reopening argument...\n")
            crt_response = critic.respond(sigil, mode="reopen")
            sigil.add("critic", crt_response)
            print("\n\n" + "-" * 60)

            print("\n[JUDGE] re-evaluating...\n")
            verdict = judge.respond(sigil, mode="reopen", priorities=priorities)
            sigil.add("judge", verdict)
            print("\n\n" + "=" * 60)

    # save the record
    artifact = "sigil" if mode == "normal" else "ruling"
    record_dir = RECORD_DIRS[mode]
    os.makedirs(record_dir, exist_ok=True)

    auto_slug = slugify(topic)
    if interactive:
        custom = input(f"\n  save as ({auto_slug}): ").strip()
        if custom:
            auto_slug = slugify(custom)

    filename = f"{date.today()}_{auto_slug}.md"
    path = os.path.join(record_dir, filename)
    sigil.save(path)
    print(f"\ncomplete. {artifact} saved to: {artifact}/{filename}\n")


def reopen(ruling_path, priorities=None):
    """reopen a saved ruling with new factors."""
    sigil = Sigil.load(ruling_path)

    print(f"\nnizan: reopening\n")
    print(f"topic: {sigil.topic}")
    print(f"original ruling: {os.path.basename(ruling_path)}\n")
    print("=" * 60)

    # print the original judge's ruling (last judge entry)
    for entry in reversed(sigil._entries):
        if entry["role"] == "judge":
            print(f"\n[JUDGE] previous ruling:\n\n{entry['content']}")
            break
    print("\n" + "=" * 60)

    reopen_num = 0
    while True:
        factor = input("\n  new factor? (enter to finish): ").strip()
        if not factor:
            if reopen_num == 0:
                print("\n  no factors introduced.\n")
                return
            break
        reopen_num += 1

        sigil.add("new_factor", factor)
        print(f"\n[NEW FACTOR #{reopen_num}] {factor}")
        print("\n" + "-" * 60)

        print("\n[ADVOCATE] reopening argument...\n")
        adv_response = advocate.respond(sigil, mode="reopen")
        sigil.add("advocate", adv_response)
        print("\n\n" + "-" * 60)

        print("\n[CRITIC] reopening argument...\n")
        crt_response = critic.respond(sigil, mode="reopen")
        sigil.add("critic", crt_response)
        print("\n\n" + "-" * 60)

        print("\n[JUDGE] re-evaluating...\n")
        verdict = judge.respond(sigil, mode="reopen", priorities=priorities or sigil.priorities)
        sigil.add("judge", verdict)
        print("\n\n" + "=" * 60)

    # save updated ruling
    record_dir = RECORD_DIRS["decision"]
    os.makedirs(record_dir, exist_ok=True)

    auto_slug = slugify(sigil.topic) + "-reopened"
    custom = input(f"\n  save as ({auto_slug}): ").strip()
    if custom:
        auto_slug = slugify(custom)

    filename = f"{date.today()}_{auto_slug}.md"
    path = os.path.join(record_dir, filename)
    sigil.save(path)
    print(f"\ncomplete. ruling saved to: ruling/{filename}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('usage: python debate.py "your debate topic here"')
        sys.exit(1)
    run(sys.argv[1], interactive=False)
