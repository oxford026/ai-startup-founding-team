from llm import ask_llm

ROLE = """You are the CTO agent in a virtual startup founding team.
Focus on technical feasibility, MVP scope, architecture, technology choices,
security, scalability, and technical risks."""

def run(state_snapshot: str) -> str:
    return ask_llm(
        ROLE,
        f"""Analyze the startup from a technology perspective.

{state_snapshot}

Produce:
1. MVP features
2. Suggested architecture
3. Main technologies
4. Data/security considerations
5. Technical risks
6. Estimated implementation complexity
7. Recommendation

If previous feedback exists, explicitly address it."""
    )
