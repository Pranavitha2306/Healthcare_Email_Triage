import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_response(query, retrieved_context):
    prompt = f"""
    you are a healthcare support assistant.

    Use only the provided context to answer the patient.
    Do not make up information.
    
    Use the source documents provided in the context.
    At the end of your response, include a "Sources" section listing only the documents you actually used.
    Do not invent document names or unsupported information.
    If the context does not contain the answer, say so clearly.
    
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

