import os
from flask import Flask, request
import requests

app = Flask(__name__)

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

# مسار تفاعل تليجرام الذكي
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        # ردود تفاعلية وذكية حسب سؤالك
        if text.startswith("/start"):
            reply = "حياك الله يا طويل العمر! أنا بوت منصة تداول الأسهم وذراعك الأيمن، اسألني عن أي شي وياليت تفيدني وتامرني."
        elif "الجني الأزرق" in text:
            reply = "هههههه يا طويل العمر الجني الأزرق هذا طال عمرك عالم ثاني وأساطير قديمة، بس أبشر بعزك لو تبي أسئله وألغاز ولا تحليل أسهم، أنا حاضر لك بكل علومها!"
        else:
            reply = f"يا هلا بك! وصلني سؤالك: ( {text} ). أبشر بالسعد، السيرفر يقرأ كلامك وجاهز أخدمك باللي تبيه وأعطيك العلم الوكاد."

        send_telegram_message(chat_id, reply)
        
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
