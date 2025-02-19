import os
import requests
import json

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

STATE_FILE = "notion_state.json"

def get_latest_notion_entries():
    """Notion API에서 모든 학습 데이터를 가져옴"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    results = []
    start_cursor = None

    while True:
        params = {"start_cursor": start_cursor} if start_cursor else {}
        response = requests.post(url, headers=headers, json=params)
        data = response.json()

        if "results" in data:
            results.extend(data["results"])

        # 더 이상 가져올 데이터가 없으면 종료
        if "next_cursor" not in data or not data["next_cursor"]:
            break

        start_cursor = data["next_cursor"]

    return results

def send_discord_alert(message):
    """Discord 웹훅으로 알림 전송"""
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def load_previous_state():
    """이전 상태를 JSON 파일에서 로드"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return []

def save_current_state(data):
    """현재 상태를 JSON 파일에 저장"""
    with open(STATE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def check_for_updates():
    """Notion Database의 변경 사항을 감지하여 Discord 알림 전송"""
    previous_entries = load_previous_state()
    latest_entries = get_latest_notion_entries()

    # 기존 데이터와 최신 데이터를 비교하기 위한 Dictionary 변환
    previous_data = {entry["id"]: entry["properties"]["Title"]["title"][0]["text"]["content"] for entry in previous_entries}
    latest_data = {entry["id"]: entry["properties"]["Title"]["title"][0]["text"]["content"] for entry in latest_entries}

    # 변경 사항 감지
    new_entries = [entry for entry in latest_entries if entry["id"] not in previous_data]
    updated_entries = [entry for entry in latest_entries if entry["id"] in previous_data and previous_data[entry["id"]] != latest_data[entry["id"]]]

    if new_entries or updated_entries:
        message = "✅ **Notion Database 업데이트 감지!**\n"

        if new_entries:
            message += f"\n📌 **새로운 학습 콘텐츠 ({len(new_entries)}개 추가됨)**:\n"
            for entry in new_entries:
                title = entry["properties"]["Title"]["title"][0]["text"]["content"]
                message += f"- 🆕 {title}\n"

        if updated_entries:
            message += f"\n✏️ **수정된 학습 콘텐츠 ({len(updated_entries)}개 변경됨)**:\n"
            for entry in updated_entries:
                title = entry["properties"]["Title"]["title"][0]["text"]["content"]
                message += f"- 🔄 {title}\n"

        send_discord_alert(message)
        save_current_state(latest_entries)
        print("📢 Discord 알림 전송 완료!")
    else:
        print("🔄 변경 사항 없음.")

# 실행
check_for_updates()
