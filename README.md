# Healthcare Email Triage

An AI-powered email triage systemdesigned to automatically process incoming healthcare emails, classify their category and priority, determine the required action, and route them to the appropriate department.

The system integrates Gmail, AI-based classification, FastAPI, PostgreSQL, Docker, automated testing, and GitHub Actions CI to demonstrate an end-to-end production-oriented workflow.

## Key Features
- Reads incoming emails through the Gmail API
- Extracts and processes Gmail content automatically
- Classifies emails by category and priority
- Determines the recommended action and responsible department
- Stores processed results in PostgreSQL
- Prevents duplicate processing using Gmail
- Exposes triage functionally through a FastAPI REST API
- Includes automated testing with Pytest
- Supports containerized execution with Docker
- Runs automated CI tests using GitHub Actions

## How It Works

Reads incoming emails from Gmail.
Extracts the email content for processing.
Classifies the email into the appropriate category.
Assigns  priority level based on the email content.
Determines the required action and responsible department.
Stores the processed email and classification results in PostgresSQL.
Uses the Gmail message ID to prevent duplicate email processing.


## Technologies Used
Python
FastAPI
Gmail API
PostgresSQL
Docker
Pytest
Git & GitHub

## Project Architecture
Gmail → Gmail API → Python Email Reader → AI Classification → Priority & Department Assignment → PostgreSQL Database → FastAPI

## API Endpoint
The API accepts an email subject and body, process the email through the triage system, and returns the category, priority, reason, action, and responsible department.

## Testing
The project includes automated API tests using Pytest and FastAPI TestClient.
The tests validate the triage API response and use mocking to test the API without making real AI API calls.

## Docker
The application is containerized using Docker.
Docker compose is used to run the application and PostgreSQL database together in separate containers.

## Database
PostgreSQL is used to store processed healthcare emails and their triage results.
Each record stores the email information along with its category, priority, reason, recommended action, and assigned department.
The Gmail message ID is used to prevent the same email from being processed and stored more than once.

## Security & Configuration
sensitive configuration values such as API keys, database credentials, and Gmail credentials are managed through environment variables.
The .env file is excluded from GitHub using .gitignore to prevent credentials from being committed to the repository.

## Running the Project
Clone the repository.
Create a '.env' file and configure the required environment variables.
Make sure Docker Desktop is running.
Start the application and PostgreSQL database:
  docker compose up --build
The FastAPI application will be available on port 8000.
PostgreSQL runs inside Docker and is exposed on port 5434.

