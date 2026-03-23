import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import anthropic
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

conversation_history = {}

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    sender = request.values.get("From", "")

    if sender not in conversation_history:
        conversation_history[sender] = []

    conversation_history[sender].append({
        "role": "user",
        "content": incoming_msg
    })

    # שמירה על היסטוריה מקסימלית של 20 הודעות
    if len(conversation_history[sender]) > 20:
        conversation_history[sender] = conversation_history[sender][-20:]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=conversation_history[sender]
    )

    reply = response.content[0].text

    conversation_history[sender].append({
        "role": "assistant",
        "content": reply
    })

    twiml = MessagingResponse()
    twiml.message(reply)
    return str(twiml)

@app.route("/", methods=["GET"])
def health():
    return "צ'אטבוט קבוצת צוקים פעיל ✅"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
