import os
import requests
import json

# 환경 변수 설정
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 상태 저장 파일
STATE_FILE = "notion_count_state.json"

def get_notion_entry_count():
    """현재 Notion Database의 항목 개수를 가져옴"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    data = response.json()
    
    count = len(data.get("results", []))
    print(f"📌 현재 Notion 데이터 개수: {count}")  # ✅ 디버깅용 출력
    return count

def send_discord_alert(message):
    """Discord 웹훅을 통해 알림 전송"""
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def load_previous_count():
    """이전 저장된 데이터 개수를 로드"""
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f).get("count", 0)
    return 0

def save_current_count(count):
    """현재 데이터 개수를 저장"""
    with open(STATE_FILE, "w") as f:
        json.dump({"count": count}, f, indent=4)

def check_for_count_changes():
    """Notion Database의 항목 개수 변경 감지"""
    previous_count = load_previous_count()
    current_count = get_notion_entry_count()

    print(f"🔍 이전 개수: {previous_count}, 현재 개수: {current_count}")  # ✅ 디버깅용 출력

    if current_count != previous_count:
        if current_count > previous_count:
            diff = current_count - previous_count
            message = f"✅ Notion Database에 {diff}개 항목이 추가되었습니다! 📈"
        else:
            diff = previous_count - current_count
            message = f"❌ Notion Database에서 {diff}개 항목이 삭제되었습니다! 📉"

        send_discord_alert(message)
        save_current_count(current_count)
        print("📢 Discord 알림 전송 완료!")
    else:
        print("🔄 데이터 개수 변경 없음.")

# 실행
check_for_count_changes()
