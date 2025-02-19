import requests
import schedule
import time

NOTION_API_KEY = "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"
DATABASE_ID = "19fd9a3d0f1c80ccb5e0e22df67d39ce"

def add_learning_content():
    content = "GPT에게 받은 학습 콘텐츠"
    url = f"https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": "Today's Learning"}}]},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    }
    requests.post(url, json=data, headers=headers)

# 매일 아침 8시에 실행
schedule.every().day.at("08:00").do(add_learning_content)

while True:
    schedule.run_pending()
    time.sleep(60)
