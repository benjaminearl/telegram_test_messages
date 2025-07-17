# fetch_telegram.py
import requests
import json
from datetime import datetime

BOT_TOKEN = "7988675078:AAEfOv03wcZQ_Ooa9-kHYWU9qOSoLP8ZGp8"
CHAT_ID = "-1002840300565"
LIMIT = 50

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

resp = requests.get(url)
data = resp.json()

messages = []
for item in data.get("result", []):
    msg = item.get("message")
    if msg and str(msg["chat"]["id"]) == CHAT_ID:
        messages.append({
            "user": msg["from"].get("username") or msg["from"].get("first_name"),
            "text": msg.get("text"),
            "date": datetime.fromtimestamp(msg["date"]).isoformat()
        })

with open("messages.json", "w", encoding="utf-8") as f:
    json.dump(messages[-LIMIT:], f, indent=2, ensure_ascii=False)