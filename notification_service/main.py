from fastapi import FastAPI
from pydantic import BaseModel, EmailStr
import smtplib
from email.mime.text import MIMEText

# Initialize FastAPI app
app = FastAPI()

# Pydantic Model for Notification
class Notification(BaseModel):
    email: EmailStr
    message: str

# Function to Send Email
def send_email(email: str, message: str):
    try:
        msg = MIMEText(message)
        msg["Subject"] = "Security Alert!"
        msg["From"] = "your_email@example.com"
        msg["To"] = email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("your_email@example.com", "your_password")
            server.send_message(msg)
        print("Alert email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.post("/send-notification/")
async def send_notification(notification: Notification):
    send_email(notification.email, notification.message)
    return {"status": "Notification sent"}
