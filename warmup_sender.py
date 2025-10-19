import time
import random
import resend
import os
from datetime import datetime

# Load Resend API key from environment variable
resend.api_key = os.getenv("RESEND_API_KEY")

SENDER = "Gustino's SPA <info@send.gustinospa.dpdns.org>"
BCC = "gustinosspa@gmail.com"

EMAIL_SUBJECTS = [
    "Ciao da Gustino's SPA",
    "Benvenuto da Gustino's SPA",
    "Ti auguriamo una buona giornata",
]

EMAIL_BODIES = [
    """
    <p>Ciao,</p>
    <p>Ti scriviamo solo per augurarti una splendida giornata 🌿</p>
    <p>Lo staff di <strong>Gustino's SPA</strong></p>
    """,
    """
    <p>Ciao,</p>
    <p>Grazie per averci contattato! Speriamo di vederti presto alla nostra spa.</p>
    <p>Un saluto, <br> <strong>Gustino's SPA</strong></p>
    """,
    """
    <p>Ciao,</p>
    <p>Solo un piccolo messaggio di cortesia per salutarti e ringraziarti.</p>
    <p>Buona giornata 🌸<br>Lo staff di Gustino's SPA</p>
    """
]

def send_email(to_email):
    subject = random.choice(EMAIL_SUBJECTS)
    body = random.choice(EMAIL_BODIES)

    try:
        resend.Emails.send({
            "from": SENDER,
            "to": [to_email],
            "bcc": [BCC],
            "subject": subject,
            "html": body
        })
        print(f"[{datetime.now().isoformat()}] ✅ Sent to {to_email} | Subject: {subject}")
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ❌ Failed for {to_email}: {e}")

def warmup_loop():
    with open("recipients.txt") as f:
        recipients = [line.strip() for line in f if line.strip()]

    while True:
        recipient = random.choice(recipients)
        send_email(recipient)

        delay_hours = random.uniform(2, 5)
        delay_seconds = delay_hours * 3600

        print(f"⏱ Waiting {delay_hours:.2f} hours before next email...\n")
        time.sleep(delay_seconds)

if __name__ == "__main__":
    warmup_loop()
