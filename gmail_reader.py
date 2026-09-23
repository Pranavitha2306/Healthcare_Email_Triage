import os
import email
import imaplib
import time
from dotenv import load_dotenv
from functions import classify_email, get_action, get_department
from openai import OpenAI
from database import save_to_database, email_already_processed
load_dotenv()

client = OpenAI()

gmail_address = os.getenv("GMAIL_ADDRESS")
gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")

def check_gmail():
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    mail.login(gmail_address, gmail_app_password)
    mail.select("inbox")
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()

    for email_id in email_ids:
        print(email_id)
        status, msg_data = mail.fetch(email_id, "(RFC822)")
        raw_email = msg_data[0][1]
        msg = email.message_from_bytes(raw_email)
        gmail_message_id = msg["Message-ID"]

        if email_already_processed(gmail_message_id):
            print("Email already processed. Skipping.")
            continue
        sender = msg["From"]
        subject = msg["Subject"]
        body = ""
        for part in msg.walk(): #basically msg.walk means walk through every part inside this email, one by one
            print("Content tye:", part.get_content_type())

            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                break

        print("Sender: ", sender)
        print("Subject: ", subject)
        print("Body: ", body)

        result = classify_email(client, body)
        action = get_action(result["Priority"])
        department = get_department(result["Category"])
        result["Department"] = department
        save_to_database(body, result, action, gmail_message_id)
        print("AI Result:", result)

    mail.close()
    mail.logout()


while True:
    try:
      check_gmail()
    except Exception as error:
        print("Error while processing Gmail:", error)

    time.sleep(30)