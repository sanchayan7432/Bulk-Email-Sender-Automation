import os
import time
import base64
import schedule
import csv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


# -----------------------------
# Gmail Authentication
# -----------------------------
def get_service():

    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    service = build("gmail", "v1", credentials=creds)

    return service


# -----------------------------
# Load Email List
# -----------------------------
def load_emails(file_path):

    emails = []

    with open(file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            emails.append(row["email"])

    return emails


# -----------------------------
# Create Email Message
# -----------------------------
def create_message(sender, to, subject, body, attachment=None):

    message = MIMEMultipart()

    message["to"] = to
    message["from"] = sender
    message["subject"] = subject

    message.attach(MIMEText(body, "plain"))

    # attachment optional
    if attachment and os.path.exists(attachment):

        with open(attachment, "rb") as f:

            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())

        encoders.encode_base64(part)

        filename = os.path.basename(attachment)

        part.add_header(
            "Content-Disposition",
            f"attachment; filename={filename}"
        )

        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {"raw": raw}


# -----------------------------
# Send Email
# -----------------------------
def send_email(service, message):

    service.users().messages().send(
        userId="me",
        body=message
    ).execute()


# -----------------------------
# Bulk Email Sender
# -----------------------------
def send_bulk_emails(attachment):

    service = get_service()

    emails = load_emails("emails.csv")

    subject = "Automated Email Test"

    with open("message.txt") as f:
        body = f.read()

    print(f"\nSending emails to {len(emails)} recipients...\n")

    for email in emails:

        try:

            message = create_message(
                "me",
                email,
                subject,
                body,
                attachment
            )

            send_email(service, message)

            print(f"✅ Sent to {email}")

        except Exception as e:

            print(f"❌ Failed {email} | {e}")

    print("\nFinished sending emails.\n")


# -----------------------------
# Scheduler Job
# -----------------------------
def job(attachment):

    print("\n⏰ Running scheduled email job...\n")

    send_bulk_emails(attachment)


# -----------------------------
# MAIN PROGRAM
# -----------------------------
def main():

    print("📧 Automated Email Scheduler\n")

    attachment = input(
        "Enter attachment file path (optional, press Enter to skip): "
    ).strip()

    if attachment == "":
        attachment = None

    print("\nChoose schedule type")

    print("1. Daily")
    print("2. Every X hours")
    print("3. Run once at specific time")

    choice = input("Enter option (1/2/3): ")

    if choice == "1":

        time_input = input("Enter time (HH:MM) e.g. 14:30 : ")

        schedule.every().day.at(time_input).do(job, attachment)

    elif choice == "2":

        print("\nSelect interval type:")
        print("1. Minutes")
        print("2. Hours")

        interval_type = input("Choose (1/2): ")

        if interval_type == "1":

            minutes = int(input("Run every how many minutes?: "))
            schedule.every(minutes).minutes.do(job, attachment)

        elif interval_type == "2":

            hours = int(input("Run every how many hours?: "))
            schedule.every(hours).hours.do(job, attachment)

        else:
            print("Invalid interval")
            return

    elif choice == "3":

        time_input = input("Enter time (HH:MM): ")

        schedule.every().day.at(time_input).do(job, attachment)

    else:

        print("Invalid option")
        return

    print("\n📅 Scheduler started...\n")

    while True:

        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()