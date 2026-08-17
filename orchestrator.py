import json
import re

from config import MAX_ITERATIONS
from llm import ask_llm
from state import StartupState
from agents import ceo, cto, cmo, cfo


AGENTS = {
    "ceo": ceo.run,
    "cto": cto.run,
    "cmo": cmo.run,
    "cfo": cfo.run,
}


ROUTER_INSTRUCTIONS = """You are the Orchestrator of a multi-agent startup founding team.

You must decide which specialist should act next based on the current shared state.

Available agents: ceo, cto, cmo, cfo, final.

Rules:
- Select an agent when its perspective is missing, weak, or needs revision.
- Do not automatically call every agent on every iteration.
- If the analyses are sufficiently complete and consistent, choose final.
- If agents disagree, route the issue to the most relevant specialist.
- Return ONLY valid JSON in this exact shape:

{"next_agent":"ceo|cto|cmo|cfo|final","reason":"short reason"}
"""


FINAL_INSTRUCTIONS = """You are the final decision-making agent of a virtual startup founding team.

Synthesize the shared state into one realistic, structured business plan.

IMPORTANT RULES:

1. Do not present invented information as verified facts.
2. Clearly label estimates, projections, and assumptions as "Assumption" or "Estimate".
3. Do not invent market statistics, competitor data, legal requirements, or customer research.
4. If the user did not provide a location, do not assume a specific country.
5. Prioritize a realistic and achievable MVP.
6. When agents disagree, explain the chosen approach briefly.
7. Keep financial numbers simple and clearly mark them as illustrative estimates.
8. Base the final plan primarily on the analyses produced by the specialist agents.

The final plan should distinguish between:
- User-provided information
- Agent recommendations
- Assumptions and estimates

Produce a practical startup plan rather than making unsupported claims.
"""


def parse_router(text: str):
    try:
        data = json.loads(text)
        return data.get("next_agent"), data.get("reason", "")
    except Exception:
        match = re.search(
            r'"next_agent"\s*:\s*"(ceo|cto|cmo|cfo|final)"',
            text.lower()
        )

        if match:
            return match.group(1), text

        return "final", "Router response could not be parsed; using final synthesis."


def route(state: StartupState):
    required_agents = ["ceo", "cfo", "cto", "cmo"]

    # First prioritize missing specialist perspectives.
    missing_agents = [
        agent for agent in required_agents
        if agent not in state.analyses
    ]

    if missing_agents:
        next_agent = missing_agents[0]

        return (
            next_agent,
            f"{next_agent.upper()} has not provided an analysis yet."
        )

    # Once all specialists have contributed, let the LLM
    # dynamically decide whether another revision is necessary.
    raw = ask_llm(
        ROUTER_INSTRUCTIONS,
        state.snapshot()
    )

    return parse_router(raw)


def final_plan(state: StartupState):
    return ask_llm(
        FINAL_INSTRUCTIONS,
        f"""Create the final business plan from this shared state:

{state.snapshot()}

Include:

- Executive summary
- Problem and solution
- Target customers
- Value proposition
- Business model
- MVP features
- Technology approach
- Marketing strategy
- Basic financial considerations
- Main risks
- 30/60/90-day priorities
- Final recommendation
"""
    )


def run_startup_team(idea: str):

    state = StartupState(idea=idea)
    consulted = []

    print("\n" + "=" * 70)
    print("STARTING MULTI-AGENT STARTUP TEAM")
    print("=" * 70)

    # ---------------------------------------------------------
    # Initial analysis
    # ---------------------------------------------------------

    for agent_name in ("ceo", "cfo"):

        print(
            f"\n[{agent_name.upper()}] "
            "Analyzing startup idea..."
        )

        state.analyses[agent_name] = AGENTS[agent_name](
            state.snapshot()
        )

        print(
            f"[{agent_name.upper()}] "
            "Analysis completed."
        )

        consulted.append(agent_name)

    # ---------------------------------------------------------
    # Dynamic routing + feedback loop
    # ---------------------------------------------------------

    while state.iterations < MAX_ITERATIONS:

        state.iterations += 1

        print(
            f"\n[ORCHESTRATOR] "
            f"Reviewing team state "
            f"(iteration {state.iterations})..."
        )

        next_agent, reason = route(state)

        print(
            f"[ORCHESTRATOR] "
            f"Decision: {next_agent.upper()}"
        )

        print(
            f"[ORCHESTRATOR] "
            f"Reason: {reason}"
        )

        state.decisions.append(
            f"Iteration {state.iterations}: "
            f"{next_agent} — {reason}"
        )

        # -----------------------------------------------------
        # Consensus reached
        # -----------------------------------------------------

        if next_agent == "final":

            print(
                "\n[ORCHESTRATOR] "
                "Team has reached sufficient agreement."
            )

            break

        # -----------------------------------------------------
        # Invalid routing decision
        # -----------------------------------------------------

        if next_agent not in AGENTS:

            print(
                "[ORCHESTRATOR] "
                "Invalid agent selected. Ending routing."
            )

            break

        # -----------------------------------------------------
        # Feedback + revision
        # -----------------------------------------------------

        state.feedback.append(
            f"Orchestrator: {reason}"
        )

        print(
            f"\n[{next_agent.upper()}] "
            "Revising/analyzing based on team feedback..."
        )

        state.analyses[next_agent] = AGENTS[next_agent](
            state.snapshot()
        )

        print(
            f"[{next_agent.upper()}] "
            "Analysis completed."
        )

        consulted.append(next_agent)

    # ---------------------------------------------------------
    # Ensure CTO and CMO have contributed
    # ---------------------------------------------------------

    for agent_name in ("cto", "cmo"):

        if agent_name not in state.analyses:

            print(
                f"\n[{agent_name.upper()}] "
                "Providing required specialist analysis..."
            )

            state.analyses[agent_name] = AGENTS[agent_name](
                state.snapshot()
            )

            print(
                f"[{agent_name.upper()}] "
                "Analysis completed."
            )

            consulted.append(agent_name)

    # ---------------------------------------------------------
    # Final synthesis
    # ---------------------------------------------------------

    print(
        "\n[FINAL DECISION MAKER] "
        "Generating final business plan..."
    )

    final = final_plan(state)

    print(
        "[FINAL DECISION MAKER] "
        "Business plan completed."
    )

    return {
        "final_plan": final,
        "iterations": state.iterations,
        "agents_consulted": list(dict.fromkeys(consulted)),
        "decisions": state.decisions,
        "state": state,
    }