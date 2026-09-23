from dotenv import load_dotenv
from openai import OpenAI
import json
import csv
import os

load_dotenv()

client = OpenAI()

email = input("Enter Patient Email: ")

response = client.responses.create(
    model="gpt-5-nano",
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
Give a short reason for your decision.

Return the result only as valid JSON exactly like this:
{{
  "Category": "<category>"
  "Priority": "<priority>"
  "Reason": "<reason>"
}}
"""
)

result = json.loads(response.output_text)
print(result)
print(result["Category"])
print(result["Priority"])
print(result["Reason"])

if result["Priority"] == "High":
    action = "Send for urgent review"
elif result["Priority"] == "Medium":
    action = "Review soon"
else:
    action = "Normal queue"

print("Action:", action)

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