import smtplib, ssl, os
import streamlit as st

def send_email(user_input):
    """Send an email using SMTP with the provided input."""
    host = "smtp.gmail.com"  # SMTP server for Gmail
    port = 465  # Port for SSL

    # Email credentials
    username = "ssk98.automations@gmail.com"
    password = st.secrets["EmailsAppPassword"]  # Fetch password from environment variables
    #password = os.getenv("PortfolioEmailsAppPassword")
    receiver = "sathiyanarayanan.au@gmail.com"  # Receiver email address

    context = ssl.create_default_context()  # SSL context for secure connection

    message = f"From: SuperCoach Stats App\n"
    message += "Subject: Feedback Received\n\n"
    message += user_input

    # Send the email using SMTP_SSL
    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(username, password)
        server.sendmail(username, receiver, message)

