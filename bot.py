import os
import telebot
from flask import Flask

TOKEN = "8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg"
bot = telebot.TeleBot(TOKEN)
TRADING_URL = "https://v0-project-g8tug0vv-aaa-2545.vercel.app"

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    markup = telebot.types.InlineKeyboardMarkup()
    btn_trading = telebot.types.InlineKeyboardButton(text="🚀 فتح منصة التداول", url=TRADING_URL)
    markup.add(btn_trading)
    
    welcome_text = (
        f"مرحباً بك يا {user_name} في بوت منصة تداول الأسهم 📈\n\n"
        "يسعدنا خدمتك. يمكنك الانتقال إلى منصة التداول مباشرة عبر الزر أدناه:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_trading = telebot.types.InlineKeyboardButton(text="🚀 فتح منصة التداول", url=TRADING_URL)
    markup.add(btn_trading)
    
    bot.send_message(
        message.chat.id, 
        "للدخول إلى المنصة وبدء التداول، اضغط على الزر أدناه:", 
        reply_markup=markup
    )

def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    import threading
    t = threading.Thread(target=run_bot)
    t.start()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
    
