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
    response = client.put("/emails/999/status?status=Completed")
    assert response.status_code==404

@patch("api.classify_email")
def test_triage_with_mock(mock_classify_email):
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

