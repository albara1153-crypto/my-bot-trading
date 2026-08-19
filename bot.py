import os
from flask import Flask, request
import requests
import google.generativeai as genai

app = Flask(__name__)

# يسحب مفتاح جميني من إعدادات ريندر بأمان
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# يسحب توكن تليجرام والشات من إعدادات ريندر
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

def send_telegram_message(chat_id, text):
    if not TELEGRAM_BOT_TOKEN:
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

@app.route("/")
def home():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.is_json:
        data = request.json
        message = data.get("text", "TradingView Alert")
    else:
        message = request.data.decode("utf-8") or "TradingView Alert"
    if TELEGRAM_CHAT_ID:
        send_telegram_message(TELEGRAM_CHAT_ID, message)
    return "OK", 200

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if not model:
            reply = "Error: API key not configured."
        else:
            try:
                response = model.generate_content(text)
                reply = response.text
            except Exception as e:
                reply = f"Error: {str(e)}"

        send_telegram_message(chat_id, reply)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
