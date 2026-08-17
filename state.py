from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class StartupState:
    idea: str
    analyses: Dict[str, str] = field(default_factory=dict)
    feedback: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    iterations: int = 0

    def snapshot(self) -> str:
        analyses_text = "\n\n".join(
            f"[{agent.upper()}]\n{text[:1800]}"
            for agent, text in self.analyses.items()
        )

        feedback_text = "\n".join(
            f"- {x[:500]}"
            for x in self.feedback[-5:]
        )

        return (
            f"STARTUP IDEA:\n{self.idea[:1200]}\n\n"
            f"CURRENT ANALYSES:\n{analyses_text or 'None yet'}\n\n"
            f"RECENT FEEDBACK:\n{feedback_text or 'None'}\n"
        )
