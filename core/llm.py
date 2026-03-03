import sys
import litellm
from config import MODEL


def call(system_prompt, transcript_text):
    """send a system prompt and the debate transcript to the configured model.
    streams tokens to stdout as they arrive, returns the full response."""
    response = litellm.completion(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": transcript_text},
        ],
        max_tokens=1024,
        stream=True,
    )
    chunks = []
    for chunk in response:
        delta = chunk.choices[0].delta.content
        if delta:
            sys.stdout.write(delta)
            sys.stdout.flush()
            chunks.append(delta)
    return "".join(chunks)
