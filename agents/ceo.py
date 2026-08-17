from llm import ask_llm

ROLE = """You are the CEO agent in a virtual startup founding team.
Focus on business strategy, value proposition, business model, priorities,
risks, and overall viability. Be practical and concise."""

def run(state_snapshot: str) -> str:
    return ask_llm(
        ROLE,
        f"""Analyze the startup using the shared state below.

{state_snapshot}

Produce:
1. Business objective
2. Target customer
3. Value proposition
4. Business model
5. Strategic priorities
6. Major business risks
7. Recommendation

If previous feedback exists, explicitly address it."""
    )
