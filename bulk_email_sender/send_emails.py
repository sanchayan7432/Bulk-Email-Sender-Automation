import os
import csv
import base64
import time
from email.mime.text import MIMEText
from datetime import datetime

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Gmail API permission
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


# Authenticate user
def authenticate():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    return service


# Create email message
def create_message(sender, to, subject, message_text):

    message = MIMEText(message_text)

    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {"raw": raw_message}


# Send email
def send_email(service, user_id, message):

    try:
        sent_message = service.users().messages().send(
            userId=user_id,
            body=message
        ).execute()

        return sent_message

    except Exception as e:
        print("Error sending email:", e)
        return None


# Load emails from CSV
def load_emails():

    email_list = []

    with open("emails.csv", "r", encoding="utf-8") as file:

        reader = csv.reader(file)

        next(reader)  # skip header

        for row in reader:

            if row:
                email_list.append(row[0].strip())

    return email_list


# Load message template
def load_message():

    with open("message.txt", "r", encoding="utf-8") as file:
        return file.read()


# Logging
def log_result(text):

    with open("logs.txt", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - {text}\n")


# Main program
def main():

    print("\nStarting Gmail Bulk Sender...\n")

    service = authenticate()

    emails = load_emails()
    message_text = load_message()

    subject = "Automated Email System Test Notification"

    print(f"Sending emails to {len(emails)} recipients...\n")

    for email in emails:

        msg = create_message("me", email, subject, message_text)

        result = send_email(service, "me", msg)

        if result:

            print(f"✅ Sent to {email}")
            log_result(f"SUCCESS {email}")

        else:

            print(f"❌ Failed {email}")
            log_result(f"FAILED {email}")

        # delay to avoid rate limits
        time.sleep(3)

    print("\nFinished sending emails.\n")


if __name__ == "__main__":
    main()