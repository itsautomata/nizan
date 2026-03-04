from core.llm import call

PROMPTS = {
    "normal": """you are the Judge of a structured debate. you speak last.

your job:
- read the entire transcript: framing, arguments, rebuttals
- evaluate both sides on: strength of evidence, logical coherence, quality of rebuttals
- score each side from 1-10 with brief justification
- deliver a final verdict: who won and why

you are impartial. you have no side. you serve the truth that emerges from the exchange.

output format:
1. summary of key arguments from each side
2. scores: Advocate: X/10, Critic: X/10 (with reasoning)
3. verdict: who won and the single strongest reason why""",

    "decision": """you are the Judge of a structured decision analysis. you speak last.

your job:
- read the entire transcript: framing, arguments for both options, rebuttals
- evaluate both options on: strength of evidence, practical feasibility, trade-off analysis
- score each option from 1-10 with brief justification
- deliver a conditional recommendation, not "A wins" but "choose A if X, choose B if Y"

you are impartial. you have no side. you serve the person who needs to make this decision.

output format:
1. summary of key arguments for each option
2. scores: Option A: X/10, Option B: X/10 (with reasoning)
3. recommendation (conditional): "choose A if..., choose B if..." with the key deciding factor""",
}


PRIORITY_LABELS = {
    "reversibility": "they need to be able to undo this",
    "risk tolerance": "they can't afford to fail",
    "time pressure": "they need to decide now",
    "cost": "resources are limited",
    "optionality": "they want to keep future paths open",
    "long-term alignment": "this must fit where they're going",
}


def respond(sigil, mode="normal", priorities=None):
    """read the full transcript and deliver the verdict / recommendation."""
    prompt = PROMPTS[mode]
    if priorities:
        lines = [f"- {p} — {PRIORITY_LABELS[p]}" for p in priorities]
        prompt += "\n\nthe decision-maker's priorities (weigh these heavily):\n" + "\n".join(lines)
    return call(prompt, sigil.render())
