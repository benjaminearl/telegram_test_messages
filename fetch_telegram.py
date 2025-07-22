# fetch_telegram.py
import os, requests, json
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
LIMIT     = 50

# 1) get all pending updates
resp = requests.get(f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates")
data = resp.json().get("result", [])

messages = []
for upd in data:
    msg = upd.get("message")
    if not msg or str(msg["chat"]["id"]) != CHAT_ID:
        continue

    record = {
      "user": msg["from"].get("username") or msg["from"]["first_name"],
      "text": msg.get("text"),
      "date": datetime.fromtimestamp(msg["date"]).isoformat()
    }

    # 2) if there are photos attached
    if "photo" in msg:
        # largest photo is the last in the list
        file_id = msg["photo"][-1]["file_id"]
        # fetch its path
        file_info = requests.get(
            f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
        ).json()["result"]
        file_path = file_info["file_path"]
        # 3) build a direct URL
        record["photo_url"] = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"

    messages.append(record)

# only keep the last LIMIT messages
with open("messages.json", "w", encoding="utf-8") as f:
    json.dump(messages[-LIMIT:], f, ensure_ascii=False, indent=2)