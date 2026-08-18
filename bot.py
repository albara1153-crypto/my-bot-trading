import os
import telebot
from flask import Flask
import threading

# إعداد البوت
TOKEN = "8663724548:AAF00y05Fxyz9NBkDTm5zzbbJNVuhyHPy0g"
bot = telebot.TeleBot(TOKEN)
TRADING_URL = "https://v0-project-xi-nine-20.vercel.app"

# إعداد خادم Flask للعمل مع الاستضافة
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

# التعامل مع أمر /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    # إنشاء زر يفتح المنصة كـ Web App داخل تليجرام
    markup = telebot.types.InlineKeyboardMarkup()
    web_app = telebot.types.WebAppInfo(url=TRADING_URL)
    btn_trading = telebot.types.InlineKeyboardButton(text="🚀 فتح منصة التداول", web_app=web_app)
    markup.add(btn_trading)
    
    welcome_text = (
        f"مرحباً بك يا {user_name} في منصة التداول 📈\n\n"
        "تم تحديث البوت ليعمل مباشرة داخل تليجرام. اضغط الزر أدناه للدخول:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# تشغيل البوت في مسار منفصل
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    t = threading.Thread(target=run_bot)
    t.start()
    
    # تشغيل خادم Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
