# fetch_telegram.py
import os, requests, json
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

# Map numeric captions to valid div IDs
CAPTION_TO_ID = {
    "1": "one",
    "2": "two",
    "3": "three"
}

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
resp = requests.get(url)
data = resp.json().get("result", [])

backgrounds = {}

for upd in data:
    msg = upd.get("message")
    if not msg or str(msg["chat"]["id"]) != CHAT_ID:
        continue

    if "photo" in msg and "caption" in msg:
        caption = msg["caption"].strip()
        div_id = CAPTION_TO_ID.get(caption)

        if div_id:
            file_id = msg["photo"][-1]["file_id"]
            file_info = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
            ).json()["result"]
            file_path = file_info["file_path"]
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            backgrounds[div_id] = image_url

with open("backgrounds.json", "w", encoding="utf-8") as f:
    json.dump(backgrounds, f, indent=2)
