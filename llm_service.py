import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(query, retrieved_context, category=None, priority=None):
    prompt = f"""
    you are a healthcare support assistant.
    You write DRAFT replies. A staff member reviews every draft before it is sent.
    
    SAFETY RULES (always follow these first):
    - If the patient describes symptoms that could be an emergency (for example chest pain, trouble breathing, severe bleeding, signs of stroke, thoughts of self-harm), start the reply by telling them to call 911 or go to the nearest emergency room right away.
    - Never diagnose, never recommend medicines or doses, and never change a treatment.
      For medical questions, say a member of the care team will follow up.
    
    Use only the provided context to answer the patient.
    Do not make up information.
    
    Do not mention documents, file names, pr a "Sources" section in the reply.
    Do not invent information that is not in the context.
    If the context does not contain the answer, say so clearly.
    
    Email category: {category or "Unknown"}
    Email priority: {priority or "Unknown"}
    
    Context:
    {retrieved_context}

    Patient message:
    {query}

    Generate a helpful response.
    """

    response = client.responses.create(
        model="gpt-6-luna",
        input=prompt

    )
    return response.output_text

