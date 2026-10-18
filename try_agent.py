from agent import agent

test_emails = [
    "I've had crushing chest pain for 20 minutes and i'm sweating. I want to make appointment",
    "Can I set up a payment plan for my bill?",
    "Can I bring my service dog to my appointment?"
]

for text in test_emails:
    result = agent.invoke({"email_text": text})

    print("EMAIL:", text)
    print("ROUTE:", result["route"])
    print("CLASS:", result["category"], "/", result["priority"], "->", result["department"])
    print("DRAFT:", result["draft_response"][:200])
    print("-" * 60)