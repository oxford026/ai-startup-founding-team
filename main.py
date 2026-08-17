from orchestrator import run_startup_team

def main():
    print("\n=== AI Virtual Startup Founding Team ===")
    print("Enter a startup idea. Type 'quit' to exit.\n")

    while True:
        idea = input("Startup idea: ").strip()
        if idea.lower() in {"quit", "exit"}:
            break
        if not idea:
            print("Please enter an idea.\n")
            continue

        result = run_startup_team(idea)

        print("\n" + "=" * 70)
        print("FINAL BUSINESS PLAN")
        print("=" * 70)
        print(result["final_plan"])
        print("\nIterations:", result["iterations"])
        print("Agents consulted:", ", ".join(result["agents_consulted"]))

if __name__ == "__main__":
    main()
