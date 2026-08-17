from llm import ask_llm

ROLE = """You are the CFO agent in a virtual startup founding team.
Focus on financial feasibility, startup costs, revenue assumptions, pricing,
cash risks, and financial priorities. Clearly label estimates as assumptions."""

def run(state_snapshot: str) -> str:
    return ask_llm(
        ROLE,
        f"""Analyze the startup from a financial perspective.

{state_snapshot}

Produce:
1. Main cost categories
2. Revenue model
3. Pricing assumptions
4. Financial risks
5. Budget-saving recommendations
6. Basic viability assessment
7. Recommendation

Do not present invented figures as verified facts."""
    )
