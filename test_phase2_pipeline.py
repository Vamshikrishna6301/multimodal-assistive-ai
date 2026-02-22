from core.fusion_engine import FusionEngine

engine = FusionEngine()

commands = [
    "open chrome",
    "delete report.pdf",
    "yes",
    "delete all files in system",
    "no",
    "shutdown now",
    "open notepad"
]

for cmd in commands:
    decision = engine.process_text(cmd)
    print("\nInput:", cmd)
    print(decision.to_dict())
