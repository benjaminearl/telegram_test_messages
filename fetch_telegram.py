import os, requests, json

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

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
    if not msg:
        continue

    print("Checking message from chat:", msg["chat"]["id"], "vs expected", CHAT_ID)

    if str(msg["chat"]["id"]) != CHAT_ID:
        print("Skipping: chat ID doesn't match.")
        continue

    if "photo" in msg and "caption" in msg:
        caption = msg["caption"].strip()
        print("Photo caption:", caption)

        div_id = CAPTION_TO_ID.get(caption)
        if div_id:
            file_id = msg["photo"][-1]["file_id"]

            file_response = requests.get(
                f"https://api.telegram.org/bot{BOT_TOKEN}/getFile?file_id={file_id}"
            )
            file_response_json = file_response.json()
            print("getFile response:", file_response_json)

            if "result" in file_response_json:
                file_path = file_response_json["result"]["file_path"]
                image_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
                print(f"Adding image URL for div '{div_id}': {image_url}")
                backgrounds[div_id] = image_url
            else:
                print("Failed to get file_path for file_id", file_id)
        else:
            print(f"Caption '{caption}' not found in CAPTION_TO_ID map")
    else:
        print("No photo or caption in this message")

print("Final backgrounds dict:", backgrounds)

print("Saving backgrounds.json in:", os.path.abspath("backgrounds.json"))
print("Final backgrounds dict:", backgrounds)

with open("backgrounds.json", "w") as f:
    f.write('{"test":123}')

if backgrounds:
    with open("backgrounds.json", "w", encoding="utf-8") as f:
        json.dump(backgrounds, f, indent=2)
    print("Saved backgrounds.json")
else:
    print("No backgrounds to save")


