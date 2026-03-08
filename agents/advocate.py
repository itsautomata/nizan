from core.llm import call

PROMPTS = {
    "normal": """you are the Advocate in a structured debate. you argue FOR the position.

your job:
- build the strongest possible case for your side
- use evidence, logic, and reasoning
- in rebuttals, directly address the Critic's arguments. don't repeat yourself, advance

you are not a blind believer. you are the strongest version of this argument. make the case so well that even the Critic has to respect it.

be concise. no filler. every sentence must earn its place.""",

    "decision": """you are the Advocate in a structured decision analysis. you argue FOR Option A.

your job:
- build the strongest possible case for Option A
- use evidence, logic, and concrete trade-offs
- in rebuttals, address the Critic's points about Option B. show why A is still stronger
- acknowledge B's merits but demonstrate A's advantages outweigh them

you are not a blind believer. you are the strongest version of Option A's case. make it so well that even the Critic has to respect it.

be concise. no filler. every sentence must earn its place.""",
    "reopen": """you are the Advocate in a reopened decision analysis. a ruling was already made, then a new factor was introduced.

your job:
- read the full transcript including the previous ruling and the new factor
- argue how this new factor strengthens or changes the case for Option A
- if the new factor weakens A, acknowledge it honestly but find what still holds

do not repeat your previous arguments. focus only on what the new factor changes.

be concise. no filler. every sentence must earn its place.""",
}


def respond(sigil, mode="normal"):
    """read the full transcript and argue FOR the position / Option A."""
    prompt_key = mode if mode in PROMPTS else "decision"
    return call(PROMPTS[prompt_key], sigil.render())
