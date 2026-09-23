# Docker rebuild test

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from functions import classify_email, get_action, get_department
from database import save_to_database, get_all_emails, get_emails_by_department, get_emails_by_Priority, update_email_status
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

client = OpenAI()

app = FastAPI()
@app.get("/")
def home():
    return {"message": "Healthcare Email Triage API is running"}

class EmailRequest(BaseModel):
    email:str

@app.post("/triage")
def triage_email(request: EmailRequest):

    logger.info("Received email for triage")

    if not request.email.strip():
        raise HTTPException(status_code=400, detail="Email cannot be empty")

    try:
        result = classify_email(client, request.email)
        action = get_action(result["Priority"])
        department = get_department(result["Category"])
        result["Action"] = action
        result["Department"] = department
        save_to_database(request.email, result, action, )

        logger.info("Email triage completed successfully")
        return result

    except Exception as e:
        logger.error(f"Email triage failed: {e}")

        raise HTTPException(
            status_code=500,
            detail="Email triage failed"
        )


@app.get("/emails")
def read_emails():
    return get_all_emails()

@app.get("/emails/{department}")
def read_emails_by_department(department: str):
    return get_emails_by_department(department)

@app.get("/emails/Priority/{Priority}")
def read_emails_by_Priority(Priority: str):
    return get_emails_by_Priority(Priority)

@app.put("/emails/{email_id}/status")
def change_email_status(email_id: int, status: Literal["New", "InReview", "Completed"]):
    updated = update_email_status(email_id, status)
    if updated ==0:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )

    return{
        "message": "Status updated successfully",
        "email_id": email_id,
        "status": status
    }

