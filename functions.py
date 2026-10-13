import csv
import os
import json

CATEGORIES =[
    "Billing",
    "Appointment",
    "Medical Records",
    "Prescription",
    "Insurance",
    "Medical Questions",
    "Human Review",
]
PRIORITIES = ["Low", "Medium", "High"]

class ClassificationError(Exception):
    """Raised when the AI's answer is missing, not JSON, or has invalid values."""

def get_action(Priority):
    if Priority == "High":
        return "Send for urgent review"
    elif Priority == "Medium":
         return "Review soon"
    else:
        return "Normal queue"


def save_to_csv(email, result, action):
    file_exists = os.path.exists("email_result.csv")

    with open("email_result.csv", "a", newline ="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
             writer.writerow(["Email", "Category", "Priority", "Reason", "Action"])

        writer.writerow([
            email,
            result["Category"],
            result["Priority"],
            result["Reason"],
            action
    ])

def classify_email(client, email):
   try:
       response = client.responses.create(
       model="gpt-5-nano",
       text={"format": {"type" : "json_object"}},
       input=f"""
       Classify this healthcare email into only one category:

       Billing
       Appointment
       Medical Records
       Prescription
       Insurance
       Medical Questions
       Human Review

       Email:
       {email}

       Also determine the priority as Low, Medium, or High
       Priority rules:
       Low = routine request with no urgency.
       Medium = time-sensitive request that needs attention soon.
       High = urgent issue that needs immediate attention, including any possible medical emergency.
       
       Give a short reason for your decision.

       Return the result only as valid JSON exactly like this:
       {{
          "Category": "<category>",
          "Priority": "<priority>",
          "Reason": "<reason>"
      }}
      """
       )

       result = json.loads(response.output_text)
       return validate_classification(result)

   except json.JSONDecodeError as error:
       raise ClassificationError(f"Model did not return valid JSON: {error}")


def get_department(Category):
    if Category == "Appointment":
        return "Scheduling"
    elif Category == "Billing":
        return "Billing"
    elif Category == "Prescription":
        return "Prescription"
    else:
        return "Human Review"


def validate_classification(result):
    if not isinstance(result, dict):
        raise ClassificationError("Result is not a JSON object")

    for field in ["Category", "Priority", "Reason"]:
        if field not in result:
            raise ClassificationError(f"Missing field: {field}")

        if result["Category"] not in CATEGORIES:
            raise ClassificationError(f"Invalid category: {result['Category']}")

        if result["Priority"] not in PRIORITIES:
            raise ClassificationError(f"Invalid priority: {result['Priority']}")

        return result
