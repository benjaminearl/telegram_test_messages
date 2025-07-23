import os
import requests
import json
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]  # Should be a string

# Telegram API endpoint
url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

response = requests.get(url)
data = response.json().get("result", [])

messages = []

for upd in data:
    msg = upd.get("message")
    if not msg:
        continue

    # Only process messages from the correct chat/group
    if str(msg["chat"]["id"]) != CHAT_ID:
        continue

    # Only handle text messages
    if "text" not in msg:
        continue

    message_data = {
        "user": msg["from"]["username"] if "username" in msg["from"] else "unknown",
        "text": msg["text"],
        "date": datetime.fromtimestamp(msg["date"]).isoformat()
    }
    messages.append(message_data)

# Save to JSON file
with open("messages.json", "w", encoding="utf-8") as f:
    json.dump(messages, f, indent=2)

print(f"Saved {len(messages)} messages to messages.json")