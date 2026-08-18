import os
import telebot
from flask import Flask
import threading

TOKEN = "8663724548:AAF00y05Fxyz9NBkDTm5zzbbJNVuhyHPy0g"
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
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
  
