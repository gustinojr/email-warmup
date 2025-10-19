import time
import random
import resend
import os
from datetime import datetime
from flask import Flask
import threading

# ------------------------
# Minimal web server (keep Render happy)
# ------------------------
app = Flask(__name__)

@app.route('/')
def home():
    return "Email warm-up running"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# ------------------------
# Resend setup
# ------------------------
resend.api_key = os.getenv("RESEND_API_KEY")
SENDER = "Gustino's SPA <staff@gustinospa.dpdns.org>"
BCC = "gustinosspa@gmail.com"

# ------------------------
# Subjects and bodies (Italian content)
# ------------------------
EMAIL_SUBJECTS = [
    "Ciao da Gustino's SPA",
    "Benvenuto da Gustino's SPA",
    "Ti auguriamo una buona giornata",
    "Un saluto dal team di Gustino's SPA",
    "Notifica di test dal nostro sistema",
    "Messaggio di cortesia da Gustino's SPA",
    "Verifica email automatica",
    "Test di funzionalità email",
    "Controllo automatico invio messaggi",
    "Piccolo promemoria dal team Gustino"
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
    """,
    """
    <p>Ciao,</p>
    <p>Questo è un messaggio automatico per verificare che il sistema email funzioni correttamente.</p>
    <p>Lo staff di Gustino's SPA</p>
    """,
    """
    <p>Ciao,</p>
    <p>Controllo periodico: stiamo verificando l'invio corretto delle email.</p>
    <p>Grazie per la collaborazione 🌿</p>
    """
]

# ------------------------
# Send email function
# ------------------------
def send_email(to_email):
    subject = random.choice(EMAIL_SUBJECTS)
    html_content = random.choice(EMAIL_BODIES)
    text_content = "Messaggio di verifica dal team Gustino's SPA."

    try:
        resend.Emails.send({
            "from": SENDER,
            "to": [to_email],
            "bcc": [BCC],
            "subject": subject,
            "html": html_content,
            "text": text_content
        })
        print(f"[{datetime.now().isoformat()}] ✅ Sent to {to_email} | Subject: {subject}")
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ❌ Failed for {to_email}: {e}")

# ------------------------
# Warm-up loop
# ------------------------
def warmup_loop():
    # Load recipients from a file
    with open("recipients.txt") as f:
        recipients = [line.strip() for line in f if line.strip()]

    while True:
        recipient = random.choice(recipients)
        send_email(recipient)

        # Random delay between 2 and 5 hours
        delay_hours = random.uniform(2, 5)
        delay_seconds = delay_hours * 3600
        print(f"⏱ Waiting {delay_hours:.2f} hours before next email...\n")
        time.sleep(delay_seconds)

# ------------------------
# Start Flask server in background
# ------------------------
threading.Thread(target=run_flask, daemon=True).start()

# ------------------------
# Start warm-up loop
# ------------------------
if __name__ == "__main__":
    warmup_loop()
