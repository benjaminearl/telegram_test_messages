import os, requests, json
from datetime import datetime

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]
VALID_IDS = {"one", "two", "three"}  # Allowed div targets

url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
resp = requests.get(url)
data = resp.json().get("result", [])

backgrounds = {}

for upd in data:
    msg = upd.get("message")
    if not msg or str(msg["chat"]["id"]) != CHAT_ID:
        continue

    # Only process if it has a photo and a caption that matches a div ID
    if "photo" in msg and "caption" in msg:
        caption = msg["caption"].strip().lower()
        if caption in VALID_IDS:
            file_id = msg["photo"][-1]["file_id"]
            file_info = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
            ).json()["result"]
            file_path = file_info["file_path"]
            image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
            backgrounds[caption] = image_url

# Save a JSON file mapping div IDs to background image URLs
with open("backgrounds.json", "w", encoding="utf-8") as f:
    json.dump(backgrounds, f, indent=2)