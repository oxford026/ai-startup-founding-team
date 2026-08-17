# AI Virtual Startup Founding Team

A multi-agent orchestration project for SENG 456.

## Agents

- CEO: business strategy
- CTO: technical feasibility
- CMO: marketing and customers
- CFO: financial feasibility
- Orchestrator: shared-state management, dynamic routing, and feedback decisions
- Final Decision Maker: synthesizes the final business plan

## Course concepts demonstrated

### State Management
`StartupState` stores the startup idea, agent analyses, feedback, decisions, and iteration count.

### Reflection & Feedback Loops
Agents receive the current shared state and can revise their analysis after the Orchestrator identifies unresolved issues.

### Dynamic Routing
The Orchestrator decides which specialist should act next. It can route to CEO, CTO, CMO, CFO, or final synthesis rather than following a fixed sequence.

## Setup

1. Create a virtual environment.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Add your API key to `.env`.
5. Run:
   `python main.py`

## Example

Input:
"I want to create an app that connects university students with affordable tutors."

The system creates specialist analyses, identifies missing or conflicting perspectives,
routes additional work when necessary, and produces a final business plan.

## Security

Never commit `.env` or API keys. The `.gitignore` file excludes `.env`.
