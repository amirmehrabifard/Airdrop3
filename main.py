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
    json_data = request.get_json()
    if json_data:
        bot.process_new_updates([telebot.types.Update.de_json(json_data)])
    return "OK", 200

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

# مدیریت عضویت و پاداش
@bot.message_handler(commands=["start"])
def send_welcome(message):
    users = load_users()
    user_id = str(message.chat.id)

    if user_id not in users:
        users[user_id] = {"tokens": 500}  # پاداش اولیه عضویت
        save_users(users)
        bot.reply_to(message, "🚀 خوش آمدید! ۵۰۰ توکن به حساب شما اضافه شد.")
    else:
        bot.reply_to(message, "✅ شما قبلاً عضو شده‌اید!")

# سیستم ارجاع کاربران
@bot.message_handler(commands=["invite"])
def invite_user(message):
    users = load_users()
    user_id = str(message.chat.id)

    referral_link = f"https://t.me/{bot.get_me().username}?start={user_id}"
    bot.reply_to(message, f"🔗 لینک دعوت اختصاصی شما: {referral_link}")

@bot.message_handler(commands=["claim"])
def claim_tokens(message):
    users = load_users()
    user_id = str(message.chat.id)

    if len(message.text.split()) > 1:
        inviter_id = message.text.split()[1]
        if inviter_id in users and user_id not in users:
            users[user_id] = {"tokens": 500}
            users[inviter_id]["tokens"] += 100  # پاداش دعوت
            save_users(users)
            bot.reply_to(message, "✅ عضویت شما موفق بود! ۵۰۰ توکن دریافت کردید.")
            bot.send_message(inviter_id, "🎉 یک کاربر جدید دعوت شد! ۱۰۰ توکن به حساب شما اضافه شد.")
        else:
            bot.reply_to(message, "❌ لینک دعوت معتبر نیست.")
    else:
        bot.reply_to(message, "❌ لطفاً لینک دعوت را همراه دستور ارسال کنید.")

# اجرای برنامه روی پورت صحیح
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
# Updated for redeploy
