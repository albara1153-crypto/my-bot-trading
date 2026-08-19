import threading
from flask import Flask, request, jsonify, send_from_directory
import os
import telebot

# 1. إعداد السيرفر المدمج لعرض منصة التداول واستقبال الويب هوك
app = Flask(__name__, static_folder='.')

# توكن البوت ومعرف الشات الخاص بك
TELEGRAM_BOT_TOKEN = "8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg"
TELEGRAM_CHAT_ID = "1972212718"

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# 2. مسار الويب هوك المخصص لاستقبال تنبيهات TradingView
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json(silent=True)
    
    # لو البيانات وصلت كـ نص عادي (Text) من تريدينج فيو
    if not data and request.data:
        raw_text = request.data.decode('utf-8')
        message_text = f"🚨 **تنبيه جديد من التداول** 🚨\n\n{raw_text}"
    elif data:
        # لو البيانات وصلت بصيغة JSON منظمة
        action = data.get('action', 'تنبيه')
        ticker = data.get('ticker', 'غير محدد')
        price = data.get('price', 'غير محدد')
        message_text = (
            f"🚨 **تنبيه تداول جديد** 🚨\n"
            f"📌 السهم/العملة: {ticker}\n"
            f"⚙️ الإجراء: {action}\n"
            f"💰 السعر: {price}"
        )
    else:
        message_text = "🚨 وصل تنبيه فارغ من TradingView!"

    try:
        # إرسال الرسالة إلى تليجرام مباشرة
        bot.send_message(TELEGRAM_CHAT_ID, message_text, parse_mode="Markdown")
        return jsonify({"status": "success", "message": "Sent to Telegram"}), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

def run_web():
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# تشغيل السيرفر في خلفية البوت
threading.Thread(target=run_web).start()

# 3. أوامر بوت تيليجرام العادية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! بوت التنبيهات يعمل الآن وجاهز لاستقبال إشارات TradingView.")

print("البوت والسيرفر يعملان الآن...")
bot.infinity_polling()
