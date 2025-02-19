import os
import requests
import json

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

STATE_FILE = "notion_state.json"

def get_latest_notion_entries():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    response = requests.post(url, headers=headers)
    return response.json().get("results", [])

def send_discord_alert(message):
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def load_previous_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return []

def save_current_state(data):
    with open(STATE_FILE, "w") as f:
        json.dump(data, f)

def check_for_updates():
    previous_entries = load_previous_state()
    latest_entries = get_latest_notion_entries()

    previous_ids = {entry["id"] for entry in previous_entries}
    latest_ids = {entry["id"] for entry in latest_entries}

    new_entries = [entry for entry in latest_entries if entry["id"] not in previous_ids]

    if new_entries:
        message = f"✅ 새로운 학습 콘텐츠 {len(new_entries)}개가 추가되었습니다!\n"
        for entry in new_entries:
            title = entry["properties"]["Title"]["title"][0]["text"]["content"]
            message += f"- {title}\n"

        send_discord_alert(message)
        save_current_state(latest_entries)
        print("📢 Discord 알림 전송 완료!")
    else:
        print("🔄 변경 사항 없음.")

# 실행
check_for_updates()