from llm import ask_llm

ROLE = """You are the CMO agent in a virtual startup founding team.
Focus on customers, positioning, acquisition, marketing channels, messaging,
competition, and market risks."""

def run(state_snapshot: str) -> str:
    return ask_llm(
        ROLE,
        f"""Analyze the startup from a marketing perspective.

{state_snapshot}

Produce:
1. Primary customer persona
2. Customer problem
3. Positioning
4. Marketing channels
5. Customer acquisition strategy
6. Competitive considerations
7. Recommendation

If previous feedback exists, explicitly address it."""
    )
