import os
from flask import Flask, request
import telebot
import google.generativeai as genai

# المفاتيح هنا
TOKEN = "8663724548:AAEinbKIc1AfAs6BP9ZVSUqv1OW-n9G12A4"
GOOGLE_API_KEY = "AQ.Ab8RN6IGiNI75quDoyofLB6_o210UBmo961yXzo8cl8nPpft-Q"
CHAT_ID = "5668101416"

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

app = Flask(__name__)

@app.route("/")
def home():
    return "OK", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.is_json:
        data = request.json
        message = data.get("text", "TradingView Alert")
    else:
        message = request.data.decode("utf-8") or "TradingView Alert"
    bot.send_message(CHAT_ID, message)
    return "OK", 200

@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    if update and update.message:
        chat_id = update.message.chat.id
        text = update.message.text

        try:
            response = model.generate_content(text)
            reply = response.text
        except Exception as e:
            reply = f"Error: {str(e)}"

        bot.send_message(chat_id, reply)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
  
