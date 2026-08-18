import os
import telebot
from flask import Flask
import threading

TOKEN = "8998639329:AAGIDfxr687Thz28O1IrUKtDjGv0VYu-yJiU"
bot = telebot.TeleBot(TOKEN)
TRADING_URL = "https://v0-project-xi-nine-20.vercel.app"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    markup = telebot.types.InlineKeyboardMarkup()
    btn_trading = telebot.types.InlineKeyboardButton(text="Open Trading Platform", url=TRADING_URL)
    markup.add(btn_trading)
    
    welcome_text = f"Welcome {user_name} to the trading platform. Click the button below:"
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

def run_bot():
    bot.infinity_polling(none_stop=True)

if __name__ == "__main__":
    # تشغيل البوت في الخلفية بشكل مستقل تماماً
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
    
    # تشغيل خادم Flask ليفتح المنفذ فوراً لـ Render
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
