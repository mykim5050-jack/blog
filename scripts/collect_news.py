import os
import csv
from datetime import date, datetime, timedelta
import requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
BASE_URL = "https://newsapi.org/v2/everything"

KEYWORDS = [
    "AI 창업", "AI 자동화", "생성형 AI 부업", "정부지원사업 AI",
    "Claude Code", "ChatGPT 업무", "노코드 자동화", "1인 창업 AI",
]

def fetch_news(keyword, days=7):
    from_date = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
    params = {
        "q": keyword,
        "from": from_date,
        "sortBy": "popularity",
        "language": "ko",
        "apiKey": NEWS_API_KEY,
    }
    resp = requests.get(BASE_URL, params=params, timeout=10)
    if resp.status_code != 200:
        print(f"뉴스 API 오류: {resp.status_code}")
        return []

    articles = resp.json().get("articles", [])
    results = []
    for a in articles[:5]:
        results.append({
            "title": a.get("title", ""),
            "source": a.get("source", {}).get("name", "확인 불가"),
            "published_at": (a.get("publishedAt") or "")[:10],
            "url": a.get("url", ""),
            "summary": a.get("description", "") or "",
            "keyword": keyword,
        })
    return results


def save_to_csv(results, output_dir):
    today = date.today().isoformat()
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}-sources.csv")

    fieldnames = [
        "date", "category", "source_type", "source_name", "title", "url",
        "published_at", "views", "likes", "comments", "reactions",
        "summary", "trend_keywords", "verification_status", "notes"
    ]

    with open(filepath, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if f.tell() == 0:
            writer.writeheader()
        for r in results:
            writer.writerow({
                "date": today,
                "category": "뉴스",
                "source_type": "뉴스",
                "source_name": r["source"],
                "title": r["title"],
                "url": r["url"],
                "published_at": r["published_at"],
                "views": "확인 불가",
                "likes": "확인 불가",
                "comments": "확인 불가",
                "reactions": "확인 불가",
                "summary": r["summary"][:300],
                "trend_keywords": r["keyword"],
                "verification_status": "partially_verified",
                "notes": "",
            })
    return filepath


if __name__ == "__main__":
    all_results = []
    for keyword in KEYWORDS:
        results = fetch_news(keyword)
        all_results.extend(results)

    output_dir = os.path.join("data", "raw")
    filepath = save_to_csv(all_results, output_dir)
    print(f"뉴스 데이터 저장 완료: {filepath} ({len(all_results)}건)")
