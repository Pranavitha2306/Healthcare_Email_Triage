import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
load_dotenv()
import os
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "5434")
print("DB_HOST =", repr(DB_HOST))
print("DB_PORT =", repr(DB_PORT))

connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database="healthcare_email_triage",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

print("Database connected successfully!")

def save_to_database(email, result, action, gmail_message_id):

    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO emails (email_text, category, priority, reason, action, department, gmail_message_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (
            email,
            result["Category"],
            result["Priority"],
            result["Reason"],
            action,
            result["Department"],
            gmail_message_id
        )

    )
    connection.commit()
    print("Saved to PostgreSQL successfully!")


def email_already_processed(gmail_message_id):
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id FROM emails WHERE gmail_message_id = %s",(gmail_message_id,)
    )
    existing_email = cursor.fetchone()
    return existing_email is not None

def get_all_emails():
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database="healthcare_email_triage",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")

    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM emails ORDER BY id DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_emails_by_department(department):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database="healthcare_email_triage",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")

    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute(
        "SELECT * FROM emails WHERE department = %s ORDER BY id DESC",
        (department,)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_emails_by_Priority(Priority):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database="healthcare_email_triage",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")

    )
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM emails WHERE Priority = %s ORDER BY id DESC",
                   (Priority,)
                   )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def update_email_status(email_id, status):
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        database="healthcare_email_triage",
        user="postgres",
        password=os.getenv("POSTGRES_PASSWORD")

    )
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE emails SET STATUS = %s WHERE id = %s",
        (status, email_id,)
    )
    updated = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return updated





