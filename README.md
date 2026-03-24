# 📧 Bulk Email Sender Automation

## 📌 Description
This project is a Python-based bulk email automation tool powered by the Gmail API. It securely handles authentication, composes messages, and sends them to recipients listed in a CSV file. Designed for efficiency, it streamlines repetitive email tasks such as announcements, notifications, or campaigns, making communication faster and more reliable.

---

## 🚀 Features
```
- Gmail API integration for secure email sending  
- OAuth2 authentication flow for user accounts  
- Compose and send custom email messages  
- Bulk recipient handling via CSV file  
- Error handling and logging for failed deliveries  
```
---

## 🛠️ Installation
1. Clone the repository:
```
git clone https://github.com/sanchayan7432/Bulk-Email-Sender-Automation.git
cd Bulk-Email-Sender-Automation/bulk_email_sender
```
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows
```
3. - Install dependencies:
```
pip install -r requirements.txt
```
4. - Set up Gmail API credentials:
- Enable Gmail API in Google Cloud Console
- Download credentials.json and place it in the project root
---

## Usage
- Prepare a CSV file (recipients.csv) with email addresses:
```
email
example1@gmail.com
example2@gmail.com
- Run the script:
python send_emails.py
```
- Follow the authentication prompt in your browser to grant access.
---

## 📑 Example
```
message = create_message(
    sender="youremail@gmail.com",
    to="recipient@gmail.com",
    subject="Test Email",
    body="Hello, this is a test email sent via Gmail API!"
)
send_message(service, "me", message)
```
---

## ⚠️ Notes
- Ensure you have enabled Gmail API and set up OAuth2 credentials correctly.
- Google may restrict bulk sending; use responsibly to avoid account suspension.
- This project is intended for educational and productivity purposes.
---

## 📜 License
This project is licensed under the MIT License. See the [Looks like the result wasn't safe to show. Let's switch things up and try something else!] file for details.
---

## Author
```
Sanchayan Ghosh
Email me at sanchayan.ghosh2022@uem.edu.in
```
Thank You visit again!
