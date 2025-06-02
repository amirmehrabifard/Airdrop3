import os
import json
import telebot
from flask import Flask, request

# دریافت متغیرهای محیطی از Vercel
BOT_TOKEN = os.environ.get("BOT_TOKEN")
PRIVATE_KEY = os.environ.get("PRIVATE_KEY")
PORT = int(os.environ.get("PORT", 8000))

# تنظیم Flask
app = Flask(__name__)
bot = telebot.TeleBot(BOT_TOKEN)

# مسیر تست برای بررسی اجرا در Vercel
@app.route("/", methods=["GET"])
def home():
    return "✅ Bot is running on Vercel!"

# مسیر اصلی برای دریافت آپدیت‌های تلگرام
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json()
        if json_data is None:
            return "❌ Error: No JSON data received", 400
        
        # نمایش داده دریافتی برای بررسی خطاها
        print(f"📌 Received data: {json_data}")  

        # بررسی اعتبار داده دریافتی و جلوگیری از خطاهای پردازش
        if "message" not in json_data:
            return "❌ Error: Invalid data format", 400

        bot.process_new_updates([telebot.types.Update.de_json(json_data)])
        return "✅ OK", 200
    except Exception as e:
        print(f"❌ Webhook Error: {e}")  # نمایش جزئیات خطای داخلی در لاگ‌ها
        return f"❌ Internal Server Error: {e}", 500

# ذخیره اطلاعات کاربران
DATA_FILE = "users.json"

def load_users():
    """ خواندن اطلاعات کاربران از JSON """
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = file.read().strip()
            return json.loads(data) if data else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    """ ذخیره اطلاعات کاربران در JSON """
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(users, file, indent=4)

# اجرای برنامه روی پورت صحیح
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
# Redeploy update - تغییر کوچک برای اجرای دیپلوی مجدد
# Redeploy triggered with new BOT_TOKEN
print("📌 BOT_TOKEN Loaded:", BOT_TOKEN)
