from fastapi import APIRouter, HTTPException
from models.contactCollection import ContactForm
from email.message import EmailMessage
import smtplib
import os

router = APIRouter()

@router.post("/send/message")
async def send_email(form: ContactForm):
    if not form.name or not form.email or not form.message:
        raise HTTPException(status_code=400, detail="All fields are required")
    
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")

    if not EMAIL_USER or not EMAIL_PASS:
        raise HTTPException(status_code=500, detail="Email credentials are missing in .env file")
    

    # create email
    msg = EmailMessage()
    msg["Subject"] = f"Message from {form.name}"
    msg["From"] = form.email
    msg["To"] = EMAIL_USER
    msg.set_content(f"Sender: {form.name} <{form.email}>\n\nMessage:\n{form.message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)
        
        return {"message": "Email sent successfully"}
    
    except Exception as e:
        print(f"Error sending email: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    



