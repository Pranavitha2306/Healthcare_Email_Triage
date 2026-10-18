
EMERGENCY_WORDS = [
    "chest pain", "can't breathe", "cannot breathe","trouble breathing",
    "difficulty breathing", "difficulty to breath", "shortness of breath",
    "stroke", "unconscious", "severe bleeding", "suicide", "kill myself", "overdose"
]

def has_emergency_words(text):
    text =text.lower()
    return any(word in text for word in EMERGENCY_WORDS)

def after_classify(state: dict):
    if has_emergency_words(state["email_text"]):
        return "emergency"

    if state["priority"] == "High" and state["category"] in ["Medical Questions", "Human Review"]:
        return "emergency"
    return "search"

def after_search(state: dict):
    if state["route"] == "no_documents":
        return "fallback"
    return "draft"