from core.intent_parser import IntentParser
from core.intent_schema import Mode

parser = IntentParser()

tests = [
    "open the chrome.",
    "please open chrome",
    "delete the report.pdf",
    "search for transformers",
    "what is bert"
]

for t in tests:
    intent = parser.parse(t, current_mode=Mode.COMMAND)

    print("\nInput:", t)
    print("Intent Type:", intent.intent_type)
    print("Action:", intent.action)
    print("Target:", intent.target)
    print("Confidence:", intent.confidence)
    print("Entities:", {k: v.value for k, v in intent.entities.items()})
