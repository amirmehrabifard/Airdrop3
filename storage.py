import json
import os

DATA_FILE = "users.json"

def load_users():
    """ خواندن اطلاعات کاربران از JSON """
    if not os.path.exists(DATA_FILE):
        return {}  # اگر فایل موجود نباشد، مقدار خالی برگردانده شود

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
