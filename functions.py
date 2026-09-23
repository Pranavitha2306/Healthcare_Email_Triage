import csv
import os
import json

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
       if "error" in email.lower():
           return None

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
       High = urgent issue that needs immediate attention.
       
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
       return result

   except Exception as e:
      print("Error:", e)
      return None

def get_department(Category):
    if Category == "Appointment":
        return "Scheduling"
    elif Category == "Billing":
        return "Billing"
    elif Category == "Prescription":
        return "Prescription"
    else:
        return "Human Review"



