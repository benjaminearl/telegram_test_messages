import os
import requests
import json

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

CAPTION_TO_ID = {
    "1": "one",
    "2": "two",
    "3": "three"
}

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}"
IMAGE_DIR = "images"
os.makedirs(IMAGE_DIR, exist_ok=True)

response = requests.get(f"{API_URL}/getUpdates")
data = response.json().get("result", [])

backgrounds = {}

for upd in data:
    msg = upd.get("message")
    if not msg or str(msg["chat"]["id"]) != CHAT_ID:
        continue

    if "photo" in msg and "caption" in msg:
        caption = msg["caption"].strip()
        div_id = CAPTION_TO_ID.get(caption)

        if not div_id:
            print(f"Unknown caption: {caption}")
            continue

        file_id = msg["photo"][-1]["file_id"]
        file_info = requests.get(f"{API_URL}/getFile", params={"file_id": file_id}).json()
        file_path = file_info["result"]["file_path"]

        image_url = f"{FILE_URL}/{file_path}"
        image_name = file_path.split("/")[-1]
        local_path = os.path.join(IMAGE_DIR, image_name)

        # Download the image and save locally
        image_data = requests.get(image_url).content
        with open(local_path, "wb") as img_file:
            img_file.write(image_data)

        # Use local path in JSON (for GitHub Pages)
        backgrounds[div_id] = f"{IMAGE_DIR}/{image_name}"
        print(f"Saved image for div '{div_id}' → {local_path}")

# Save to JSON
with open("backgrounds.json", "w", encoding="utf-8") as f:
    json.dump(backgrounds, f, indent=2)

print("Finished writing backgrounds.json")
