import os
import telebot
from flask import Flask
import threading

# التوكن الجديد
TOKEN = "8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg"
bot = telebot.TeleBot(TOKEN)

# رابط المنصة والتطبيق الصحيح
TRADING_URL = "https://v0-project-g8tug0vvb-aaa-2545.vercel.app/"

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
    bot.send_message(message.chat.id, f"أهلاً بك {user_name} في منصة التداول. اضغط على الزر أدناه لفتح المنصة:", reply_markup=markup)

if __name__ == "__main__":
    def run_polling():
        try:
            bot.infinity_polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Polling error: {e}")

    t = threading.Thread(target=run_polling)
    t.daemon = True
    t.start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
