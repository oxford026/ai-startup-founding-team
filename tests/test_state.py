from state import StartupState

def test_state_snapshot():
    state = StartupState("Test startup")
    state.analyses["ceo"] = "Strategy"
    state.feedback.append("Needs technical review")

    snapshot = state.snapshot()

    assert "Test startup" in snapshot
    assert "Strategy" in snapshot
    assert "Needs technical review" in snapshot
