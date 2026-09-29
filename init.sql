CREATE TABLE IF NOT EXISTS emails (
id SERIAL PRIMARY KEY,
email_text TEXT NOT NULL,
category VARCHAR(100),
priority VARCHAR(50),
reason TEXT,
action VARCHAR(100),
department VARCHAR(100),
status VARCHAR(50) DEFAULT 'NEW',
gmail_message_id VARCHAR(100)
);