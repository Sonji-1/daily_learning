# -*- coding: utf-8 -*-
import os
import requests

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "19fd9a3d0f1c80ccb5e0e22df67d39ce"

def add_to_notion(content):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Title": {"title": [{"text": {"content": "Daily Learning"}}]},
            "Content": {"rich_text": [{"text": {"content": content}}]}
        }
    }
    response = requests.post(url, json=data, headers=headers)
    print(response.json())
    return response.json()

if __name__ == "__main__":
    # 테스트용으로 한 번만 실행
    add_to_notion("Test data for daily learning.")
