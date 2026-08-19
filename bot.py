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
    return "AI Master Bot is running!"

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

# مسار تليجرام الذكي الشامل
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    update = request.get_json()
    if update and "message" in update:
        chat_id = update["message"]["chat"]["id"]
        text = update["message"].get("text", "")

        if text.startswith("/start"):
            reply = "مرحباً بك يا طويل العمر! أنا ذكاؤك الاصطناعي الشامل، فاهم في الأسهم، البرمجة، العلوم، وكل ما يخطر على بالك زي النماذج الكبيرة. اسألني عن أي شي وبتلقى الإجابة اللي تثلج صدرك."
        else:
            # هنا يمكنك لاحقاً ربط الكود بمحرك API خارجي (مثل Grok أو OpenAI) لأخذ إجابة ذكية 100%
            reply = f"أهلاً بك! بخصوص سؤالك عن ({text}): بصفتي نموذج ذكاء اصطناعي شامل، أعطيك الخلاصة وأقول لك إن الموضوع يدرس من عدة جوانب (تقنية وتحليلية). تبي نتعمق في تفاصيله الدقيقة ولا نعطيك الخلاصة المفيدة؟"

        send_telegram_message(chat_id, reply)
        
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
