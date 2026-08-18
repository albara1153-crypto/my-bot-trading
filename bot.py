import os
import telebot
from flask import Flask
import threading

# ضع التوكن الذي نسخته من BotFather بين علامات التنصيص هنا
TOKEN = "8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg"

bot = telebot.TeleBot(TOKEN)
TRADING_URL = "https://v0-project-xi-nine-20.vercel.app"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_trading = telebot.types.InlineKeyboardButton(text="Open Trading Platform", url=TRADING_URL)
    markup.add(btn_trading)
    bot.send_message(message.chat.id, "Welcome! Click below to open the platform:", reply_markup=markup)

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
