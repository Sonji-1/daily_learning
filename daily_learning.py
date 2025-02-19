# -*- coding: utf-8 -*-

import os
import requests
import openai
from datetime import datetime  

# 환경 변수에서 API 키 가져오기
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# OpenAI 클라이언트 초기화
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# 학습 카테고리 및 GPT 프롬프트 설정 (링크만 제공)
categories = {
    "Reading": "Please recommend 1 good looking English article to improve my reading skills",
    "Writing": "Please recommend one easy topic to write down to improve my English writing skills",
    "Listening": "Please recommend a short TED lecture or a link to BBC Learning English to improve my English listening skills",
    "Grammar": "Please choose one topic from English grammar and recommend one link that is good for studying it",
    "Coding": "Can you recommend me a medium level coding problem that is good to solve with C++ from Leetcode or Programmers",
    "Computer System": "Please recommend one keyword related to the computer system that I can look up and study today"
}

# GPT를 이용해 학습용 링크를 가져온 후 Notion에 저장
def save_learning_links():
    today = datetime.today().strftime("%Y-%m-%d")

    for category, prompt in categories.items():
        # GPT에서 학습 관련 링크 추천 요청
        response = client.chat.completions.create(
            model="gpt-4o", 
            messages=[{"role": "user", "content": prompt}]
        )
        link = response.choices[0].message.content.strip()

        # Notion에 데이터 저장
        notion_data = {
            "parent": {"database_id": DATABASE_ID},
            "properties": {
                "Title": {"title": [{"text": {"content": f"{category} Learning Link"}}]},
                "Content": {"rich_text": [{"text": {"content": link}}]},
                "Category": {"select": {"name": category}},
                "Date": {"date": {"start": today}},
                "Completed": {"checkbox": False}
            }
        }
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        response = requests.post("https://api.notion.com/v1/pages", json=notion_data, headers=headers)
        print(f"✅ {category} 학습 링크 저장 완료!" if response.status_code == 200 else f"❌ 오류 발생: {response.json()}")

# 실행
save_learning_links()