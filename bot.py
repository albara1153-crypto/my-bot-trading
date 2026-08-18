import threading
from flask import Flask, send_from_directory
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

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

# تشغيل السيرفر في خلفية البوت ليعمل رابط المنصة:
# https://my-bot-trading-p1mn.onrender.com
threading.Thread(target=run_web).start()

# 2. كود بوت تيليجرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! بوت التداول ومنصة التحليل يعملان بنجاح.')

if __name__ == '__main__':
    # التوكن الخاص بك
    application = ApplicationBuilder().token("8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg").build()
    
    application.add_handler(CommandHandler("start", start))
    
    print("البوت يعمل الآن...")
    application.run_polling()
