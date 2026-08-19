import os
from flask import Flask, request
import telebot

# المفاتيح هنا
TOKEN = "8663724548:AAEinbKIc1AfAs6BP9ZVSUqv1OW-n9G12A4"
CHAT_ID = "5668101416"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "البوت يعمل بشكل ممتاز، جاهز لاستقبال تنبيهات TradingView!", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    # استقبال التنبيه من TradingView
    if request.is_json:
        data = request.json
        # نقوم بتحويل البيانات إلى نص مفهوم
        message = str(data)
    else:
        message = request.data.decode("utf-8") or "تنبيه جديد من TradingView"
    
    # إرسال التنبيه فوراً لتليجرام
    bot.send_message(CHAT_ID, f"🔔 تنبيه تداول جديد:\n\n{message}")
    return "تم الإرسال بنجاح", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
  
