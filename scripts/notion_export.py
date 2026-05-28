"""
Notion 데이터베이스 내보내기 스크립트.
실제 저장은 사용자 승인 후에만 실행한다.
"""
import os
import csv
from datetime import date
import requests

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_DATABASE_ID = os.environ.get("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1"
HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def check_duplicate(url):
    payload = {
        "filter": {
            "property": "URL",
            "url": {"equals": url},
        }
    }
    resp = requests.post(
        f"{NOTION_API_URL}/databases/{NOTION_DATABASE_ID}/query",
        headers=HEADERS,
        json=payload,
        timeout=10,
    )
    results = resp.json().get("results", [])
    return results[0]["id"] if results else None


def create_or_update_page(row):
    existing_id = check_duplicate(row.get("url", ""))

    properties = {
        "날짜": {"date": {"start": row.get("date", "")}},
        "카테고리": {"select": {"name": row.get("category", "")}},
        "트렌드 키워드": {"rich_text": [{"text": {"content": row.get("trend_keywords", "")}}]},
        "출처": {"rich_text": [{"text": {"content": row.get("source_name", "")}}]},
        "URL": {"url": row.get("url", "")},
        "핵심 요약": {"rich_text": [{"text": {"content": row.get("summary", "")[:2000]}}]},
        "상태": {"select": {"name": "수집"}},
    }

    if existing_id:
        resp = requests.patch(
            f"{NOTION_API_URL}/pages/{existing_id}",
            headers=HEADERS,
            json={"properties": properties},
            timeout=10,
        )
        return "updated", resp.status_code
    else:
        payload = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": properties,
        }
        resp = requests.post(
            f"{NOTION_API_URL}/pages",
            headers=HEADERS,
            json=payload,
            timeout=10,
        )
        return "created", resp.status_code


def load_sources(data_dir):
    today = date.today().isoformat()
    filepath = os.path.join(data_dir, f"{today}-sources.csv")
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"소스 파일 없음: {filepath}")
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f))


if __name__ == "__main__":
    print("Notion 내보내기 시작 중...")
    print("중요: 실제 저장은 사용자 승인 후에만 실행됩니다.")

    sources = load_sources(os.path.join("data", "raw"))
    for row in sources:
        action, status = create_or_update_page(row)
        print(f"{action}: {row.get('title', '')} (HTTP {status})")

    print("Notion 내보내기 완료.")
