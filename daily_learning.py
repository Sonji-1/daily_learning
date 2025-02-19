# -*- coding: utf-8 -*-

import requests
import schedule
import time
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = "19fd9a3d0f1c80ccb5e0e22df67d39ce"

def add_learning_content():
    content = "Learning contents from GPT"
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

# run every 8 am
schedule.every().day.at("08:00").do(add_learning_content)

# test code
add_to_notion("today's learning data automatic recording")

while True:
    schedule.run_pending()
    time.sleep(60)

