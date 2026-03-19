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

REST_AUTH_URL = "https://identitytoolkit.googleapis.com/v1/accounts"

def register_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    url = f"{REST_AUTH_URL}:signUp?key={FIREBASE_API_KEY}"
    response = requests.post(url, json=payload)
    return response.json()


def login_user(email, password):
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    try:
        url = f"{REST_AUTH_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
        res = requests.post(url, json=payload)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.HTTPError as err:
        return {"error": str(err), "details": res.json()}