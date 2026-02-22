from knowledge.knowledge_engine import KnowledgeEngine

engine = KnowledgeEngine()

questions = [
    "What are transformers in AI?",
    "Who is Isaac Newton?",
    "who is who"
]

for q in questions:
    print("\nQuestion:", q)
    response = engine.handle({
        "action": "KNOWLEDGE_QUERY",
        "target": q
    })
    print("Spoken:", response.spoken_message)