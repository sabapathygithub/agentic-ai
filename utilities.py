
from dotenv import load_dotenv
import requests
import os


def send_message(message: str):
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    group_chat_id = os.getenv('GROUP_CHAT_ID')
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": group_chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, data=payload)
    return response.json()