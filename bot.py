import os
import requests
from flask import Flask, request

app = Flask(__name__)

# التوكن والأيدي الصحيحة والمحدثة
TELEGRAM_BOT_TOKEN = "8663724548:AAFO0y05Fxyz9NBkDTm5zzbbJNVuhyHPyOg"
TELEGRAM_CHAT_ID = "5668101416"


@app.route("/")
def home():
  return "Bot is running!"


@app.route("/webhook", methods=["POST"])
def webhook():
  try:
    data = request.data.decode("utf-8")
    print(f"Received data: {data}")

    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
      url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
      payload = {
          "chat_id": TELEGRAM_CHAT_ID,
          "text": f"🚨 تنبيه جديد من TradingView:\n\n{data}",
          "parse_mode": "Markdown",
      }
      requests.post(url, json=payload)

    return "Success", 200
  except Exception as e:
    print(f"Error: {e}")
    return str(e), 400


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)
