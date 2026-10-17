from fastapi.testclient import TestClient
from api import app
from functions import get_action
from unittest.mock import patch

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_empty_email():
    response = client.post("/triage", json = {"email" : " "})
    assert response.status_code==400

def test_get_action():
    result = get_action("High")
    assert result == "Send for urgent review"

def test_email_not_found():
    response = client.put("/emails/999/status?status=APPROVED&reviewer=tester")
    assert response.status_code==404

@patch("api.save_to_database", return_value=1)
@patch("api.classify_email")
def test_triage_with_mock(mock_classify_email, mock_save):
    mock_classify_email.return_value = {
        "Category" : "Prescription",
        "Priority" : "High",
        "Reason" : "Test reason"
    }

    response = client.post(
        "/triage",
        json={"email" : "I need a prescription refill"}
    )

    assert response.status_code ==200

@patch("api.get_email_status", return_value="PENDING_REVIEW")
@patch("api.get_email_by_id", return_value={"id":5, "status": "PENDING_REVIEW"})
def test_reject_without_reason(mock_get_email, mock_get_status):
    response = client.put("/emails/5/status?status=REJECTED&reviewer=Lisa")
    assert response.status_code == 400

@patch("api.get_email_by_id", return_valur={"id":5, "status": "APPRIVED"})
def test_edit_approved_draft(mock_get_email):
    response = client.put("/emails/5/draft", json={"final_response": "New reply"})
    assert response.status_code == 400

