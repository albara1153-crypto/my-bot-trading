import os
from flask import Flask, request
import requests

app = Flask(__name__)

# التوكن والأيدي الصحيحة والمحدثة
TELEGRAM_BOT_TOKEN = "8663724548:AAEinbKIc1AfAs6BP9ZVSUqv1OW-n9G12A4"
TELEGRAM_CHAT_ID = "5668101416"

@app.route("/")
def home():
    return "Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    # يدعم استقبال النصوص العادية أو الـ JSON من تريدينج فيو بكل سهولة
    if request.is_json:
        data = request.json
        message = data.get("text", "تنبيه جديد من TradingView")
    else:
        message = request.data.decode("utf-8") or "تنبيه جديد من TradingView"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, json=payload)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
