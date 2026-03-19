import firebase_admin
from firebase_admin import credentials, db
import os
import requests
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Берем значения из .env
cred_path = os.getenv("FIREBASE_CREDENTIALS")
db_url = os.getenv("FIREBASE_DB_URL")
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Инициализация Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': db_url
    })


def get_user_profile(user_id, id_token):
    url = f"{db_url}/users/{user_id}.json?auth={id_token}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"ERROR БД при чтении: {response.status_code}")
            return None
    except Exception as e:
        print(f"ERROR запроса чтения: {e}")
        return None


def save_user_profile(user_id, profile_data, id_token):
    url = f"{db_url}/users/{user_id}.json?auth={id_token}"
    try:
        response = requests.put(url, json=profile_data)
        if response.status_code == 200:
            return True
        else:
            print(f"Ошибка БД: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return False