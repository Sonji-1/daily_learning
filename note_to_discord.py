import os
import requests
import json

# 환경 변수 설정
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 상태 저장 파일
STATE_FILE = "notion_count_state.json"

def get_notion_entries():
    """현재 Notion Database의 모든 항목을 가져옴"""
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post(url, headers=headers)
    data = response.json()

    if "error" in data:
        print("❌ API 오류 발생:", data["error"])
        return []

    return data.get("results", [])

def send_discord_alert(message):
    """Discord 웹훅을 통해 알림 전송"""
    data = {"content": message}
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def load_previous_state():
    """이전 저장된 데이터 상태 로드 (없으면 기본값 반환)"""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                data = json.load(f)
                return {
                    "ids": data.get("ids", []),  # 기존에 "ids"가 없으면 빈 리스트 반환
                    "count": data.get("count", 0)  # 기존에 "count"가 없으면 0 반환
                }
        except Exception as e:
            print(f"❌ JSON 파일 읽기 오류 발생: {e}")
            return {"ids": [], "count": 0}  # 오류 발생 시 기본값 반환
    return {"ids": [], "count": 0}  # 파일이 없을 경우 기본값 반환

def save_current_state(entry_ids, count):
    """현재 데이터 상태 저장"""
    try:
        with open(STATE_FILE, "w") as f:
            json.dump({"ids": list(entry_ids), "count": count}, f, indent=4)
        print(f"📌 새로운 상태 저장 완료: {count} 개 항목")
    except Exception as e:
        print(f"❌ JSON 파일 저장 오류 발생: {e}")

def check_for_new_entries():
    """Notion Database의 새 항목을 감지하고 Discord로 Title만 전송"""
    previous_state = load_previous_state()
    previous_ids = set(previous_state["ids"])  # KeyError 방지

    current_entries = get_notion_entries()
    current_ids = {entry["id"] for entry in current_entries}

    new_entries = [entry for entry in current_entries if entry["id"] not in previous_ids]

    if new_entries:
        message = f"✅ 새로운 학습 콘텐츠 {len(new_entries)}개가 추가되었습니다!\n"
        for entry in new_entries:
            title = entry["properties"]["Title"]["title"][0]["text"]["content"]
            message += f"- {title}\n"

        send_discord_alert(message)
        save_current_state(list(current_ids), len(current_ids))
        print("📢 Discord 알림 전송 완료!")
    else:
        print("🔄 새로운 항목 없음.")

# 실행
check_for_new_entries()
