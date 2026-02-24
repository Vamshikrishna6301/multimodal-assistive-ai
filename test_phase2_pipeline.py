from core.fusion_engine import FusionEngine

engine = FusionEngine()

commands = [
    "open chrome",
    "delete report.pdf",
    "yes",  # confirm delete
    "delete all files in system",
    "no",   # cancel
    "shutdown now",
    "open notepad"
]

for cmd in commands:
    decision = engine.process_text(cmd)

    print("\n" + "=" * 60)
    print("Input:", cmd)

    if decision is None:
        print("System waiting for confirmation or no action taken.")
        continue

    print("Intent Type:", decision.intent_type.name)
    print("Action:", decision.action)
    print("Target:", decision.target)
    print("Mode:", decision.mode.name)
    print("Risk Level:", decision.risk_level)
    print("Requires Confirmation:", decision.requires_confirmation)
    print("Blocked:", decision.blocked_reason)
    print("Confidence:", round(decision.confidence, 3))
    print("Structured Output:", decision.to_dict())