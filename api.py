
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal
from dotenv import load_dotenv
from openai import OpenAI
from functions import classify_email, get_action, get_department, ClassificationError
from database import save_to_database, get_all_emails, get_emails_by_department, get_emails_by_Priority, update_email_status, get_email_by_id, get_email_status
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

    except ClassificationError as e:
        logger.error(f"Classification failed: {e}")
        raise HTTPException(
            status_code=502,
            detail="AI classification failed. Please try again."
        )

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
def change_email_status(
        email_id: int,
        status: Literal["PENDING_REVIEW", "APPROVED", "REJECTED"],
        reviewer: str
):
    email = get_email_by_id(email_id)

    if email is None:
        raise HTTPException(
            status_code = 404,
            detail = "Email not found"
        )

    current_status = get_email_status(email_id)
    if current_status in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code = 400,
            detail = "This email has already been reviewed"
        )

    if current_status == "NEW" and status != "PENDING_REVIEW":
        raise HTTPException(
            status_code=400,
            detail="New emails must be moved to PENDING_REVIEW first"
        )

    if current_status == "PENDING_REVIEW" and status not in ["APPROVED", "REJECTED"]:
        raise HTTPException(
            status_code=400,
            detail="Pending emails can only be APPROVED or REJECTED"
        )

    updated = update_email_status(email_id, status, reviewer)
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

@app.get("/emails/id/{email_id}")
def read_email_by_id(email_id: int):
    email = get_email_by_id(email_id)
    if email is None:
        raise HTTPException(
            status_code=404,
            detail="Email not found"
        )
    return email

