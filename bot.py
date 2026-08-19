import os
from flask import Flask, request
import requests

app = Flask(__name__)

# التوكن والأيدي الصحيحة والمحدثة
TELEGRAM_BOT_TOKEN = "8663724548:AAEinbKIc1AfAs6BP9ZVSUqv1OW-n9G12A4"
TELEGRAM_CHAT_ID = "5668101416"

def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "Bot is running!"

# مسار استقبال تنبيهات تريدينج فيو
@app.route("/webhook", methods=["POST"])
def webhook():
    if request.is_json:
        data = request.json
        message = data.get("text", "تنبيه جديد من تريدينج فيو")
    else:
        message = request.data.decode("utf-8") or "تنبيه جديد من تريدينج فيو"

    send_telegram_message(TELEGRAM_CHAT_ID, message)
    return "OK", 200

# مسار تفاعل تليجرام (لما ترسل للبوت رسالة أو أمر)
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.startswith("/start"):
            reply = "حياك الله يا طويل العمر! منصة تداول الأسهم جاهزة وتستقبل تنبيهات تريدينج فيو بكفاءة عالية. 📈🚀"
        else:
            reply = f"أهلاً بك! وصلني ردك: ({text}). البوت شغال وجاهز لأي تنبيه."

        send_telegram_message(chat_id, reply)
        
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
