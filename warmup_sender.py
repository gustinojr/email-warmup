import time
import random
import resend
import os
from datetime import datetime
from flask import Flask, jsonify
import threading

# Flask web server (required for Render)
app = Flask(__name__)

# --- RESEND CONFIGURATION ---
resend.api_key = os.getenv("RESEND_API_KEY")

SENDER = "Gustino's SPA <staff@gustinospa.dpdns.org>"
BCC = "gustinosspa@gmail.com"

# --- RANDOM EMAIL CONTENT OPTIONS ---
GREETINGS = ["Ciao", "Buongiorno", "Salve", "Hey", "Un saluto da noi"]
CLOSINGS = ["A presto 🌸", "Un caro saluto", "Con affetto 💆‍♀️", "Buona giornata ☀️", "Alla prossima 👋"]

SUBJECTS = [
    "Un saluto da Gustino's SPA 💆‍♀️",
    "Ti auguriamo una splendida giornata",
    "Grazie per essere parte della nostra community",
    "Un pensiero rilassante da Gustino's SPA",
    "Oggi pensa a te stesso 🌿"
]

BODY_TEMPLATES = [
    "{greet},<br><br>Speriamo che la tua giornata stia andando bene!<br>Ti mandiamo un pensiero di relax da <strong>Gustino's SPA</strong>.<br><br>{close}<br><em>Lo staff di Gustino's SPA</em>",
    "{greet},<br><br>Solo un piccolo messaggio per augurarti un po' di serenità.<br>Ci piacerebbe rivederti presto alla nostra spa!<br><br>{close}<br><em>Lo staff di Gustino's SPA</em>",
    "{greet},<br><br>Ogni giornata è migliore con un momento di relax.<br>Ti ricordiamo che Gustino's SPA è sempre pronta ad accoglierti!<br><br>{close}<br><em>Gustino's SPA</em>"
]

# --- SEND FUNCTION ---
def send_email(to_email):
    subject = random.choice(SUBJECTS)
    greeting = random.choice(GREETINGS)
    closing = random.choice(CLOSINGS)
    body_template = random.choice(BODY_TEMPLATES)

    html_content = body_template.format(greet=greeting, close=closing)

    try:
        resend.Emails.send({
            "from": SENDER,
            "to": [to_email],
            "bcc": [BCC],
            "subject": subject,
            "html": html_content
        })
        print(f"[{datetime.now().isoformat()}] ✅ Sent to {to_email} | Subject: {subject}")
        return {"status": "success", "to": to_email, "subject": subject}
    except Exception as e:
        print(f"[{datetime.now().isoformat()}] ❌ Failed for {to_email}: {e}")
        return {"status": "error", "to": to_email, "error": str(e)}

# --- MANUAL SEND ROUTE ---
@app.route("/send_mail")
def manual_send():
    """
    Trigger an email manually by calling this route.
    Randomly selects a recipient from recipients.txt
    """
    try:
        with open("recipients.txt") as f:
            recipients = [line.strip() for line in f if line.strip()]
        if not recipients:
            return jsonify({"error": "No recipients found in recipients.txt"}), 400

        recipient = random.choice(recipients)
        result = send_email(recipient)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- BACKGROUND AUTO WARM-UP LOOP ---
def warmup_loop():
    """
    Continuously sends emails every 2–6 hours to random recipients.
    """
    try:
        with open("recipients.txt") as f:
            recipients = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ recipients.txt not found — auto warm-up disabled until file exists.")
        recipients = []

    while recipients:
        recipient = random.choice(recipients)
        send_email(recipient)

        # Random delay between 2 and 6 hours
        delay_hours = random.uniform(2, 6)
        delay_seconds = delay_hours * 3600

        print(f"⏱ Waiting {delay_hours:.2f} hours before next email...\n")
        time.sleep(delay_seconds)

@app.route('/')
def home():
    return "✅ Gustino's SPA Email Warm-up is running"

# --- START SERVER AND BACKGROUND THREAD ---
threading.Thread(target=warmup_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
