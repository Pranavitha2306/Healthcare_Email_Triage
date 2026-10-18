from typing import TypedDict
from dotenv import load_dotenv
from openai import OpenAI
from functions import classify_email, get_action, get_department, ClassificationError
from vector_store import retrieve_context
from llm_service import generate_response
from database import save_to_database
from langgraph.graph import StateGraph, START, END
from routing import after_search, after_classify

load_dotenv()
client = OpenAI()

class EmailState(TypedDict, total=False):
    # Filled in at the start(from Gmail)
    email_text: str
    sender: str
    subject: str
    gmail_message_id: str

    # Filled in by the classify step
    category: str
    priority: str
    reason: str
    action: str
    department: str

    # Filled in by the search step
    context: str

    # Filled in by the draft step
    draft_response: str

    # which part the agent took (useful for the reviewer and for testing)
    route: str

    # Filled in by the save step
    email_id: int


def classify_node(state: EmailState):
    try:
        result = classify_email(client, state["email_text"])
    except ClassificationError as error:
        result = {"Category": "Human Review","Priority": "Medium",
                  "Reason": f"Automatic classification failed: {error}"}

    return {
        "category": result["Category"],
        "priority": result["Priority"],
        "reason": result["Reason"],
        "action": get_action(result["Priority"]),
        "department": get_department(result["Category"]),
    }


def search_node(state: EmailState):
    context = retrieve_context(state["email_text"])

    if context.lower().startswith("no relevant information"):
        return {"context": context, "route": "no_documents", "department": "Human Review"}

    return {"context": context, "route": "normal"}

def emergency_node(state: EmailState):
    return {"route": "emergency",
            "context": "",
            "priority": "High",
            "action": get_action("High"),
            "department": "Human Review",
            }

FALLBACK_REPLY = (
    "Dear Patient, \n\n"
    "Thank you for your message. A member of our team will review your request"
    "and get back to you as soon as possible.\n\n"
    "Best Regards,\n"
    "Patient Support Team"
)

def fallback_node(state: EmailState):
    return{"draft_response": FALLBACK_REPLY}

def draft_node(state:EmailState):
    draft = generate_response(
        state["email_text"],
        state.get("context", ""),
        state["category"],
        state["priority"],
    )
    return {"draft_response": draft}

def save_node(state: EmailState):
    result = {
        "Category": state["category"],
        "Priority": state["priority"],
        "Reason": state["reason"],
        "Department": state["department"],
    }
    email_id = save_to_database(
        state["email_text"], result, state["action"],
        state.get("gmail_message_id"), state["draft_response"],
        sender=state.get("sender"), subject=state.get("subject"),
    )
    return{"email_id" : email_id}

graph = StateGraph(EmailState)

graph.add_node("classify", classify_node)
graph.add_node("emergency", emergency_node)
graph.add_node("search", search_node)
graph.add_node("fallback", fallback_node)
graph.add_node("draft", draft_node)
graph.add_node("save", save_node)

graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", after_classify, ["emergency", "search"])
graph.add_edge("emergency", "draft")
graph.add_conditional_edges("search", after_search, ["fallback", "draft"])
graph.add_edge("fallback", "save")
graph.add_edge("draft", "save")
graph.add_edge("save", END)

agent = graph.compile()



