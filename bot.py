import threading
from flask import Flask, send_from_directory
import os
import telebot

# 1. إعداد السيرفر المدمج لعرض منصة التداول
app = Flask(__name__, static_folder='.')

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر في خلفية البوت
threading.Thread(target=run_web).start()

# 2. كود بوت تيليجرام (pyTelegramBotAPI)
bot = telebot.TeleBot("8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! المنصة تعمل الآن: https://my-bot-trading-p1mn.onrender.com")

print("البوت يعمل الآن...")
bot.infinity_polling()
