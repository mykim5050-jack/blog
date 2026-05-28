import os
import csv
from datetime import date, datetime
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

SEARCH_KEYWORDS = [
    "AI 자동화 실무",
    "AI 부업",
    "ChatGPT 업무 자동화",
    "Claude Code 사용법",
    "Notion 자동화",
    "n8n AI workflow",
    "AI agent business",
    "solopreneur AI automation",
    "정부지원사업 사업계획서",
    "예비창업패키지 선정 팁",
    "초기창업패키지 평가위원",
]

def search_youtube(keyword, max_results=5):
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_response = youtube.search().list(
        q=keyword,
        part="snippet",
        maxResults=max_results,
        order="viewCount",
        publishedAfter=(datetime.utcnow().replace(day=datetime.utcnow().day - 7)).isoformat() + "Z",
        type="video",
    ).execute()

    video_ids = [item["id"]["videoId"] for item in search_response.get("items", [])]
    if not video_ids:
        return []

    stats_response = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids),
    ).execute()

    results = []
    for item in stats_response.get("items", []):
        stats = item.get("statistics", {})
        results.append({
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "title": item["snippet"]["title"],
            "channel": item["snippet"]["channelTitle"],
            "published_at": item["snippet"]["publishedAt"][:10],
            "views": stats.get("viewCount", "확인 불가"),
            "likes": stats.get("likeCount", "확인 불가"),
            "comments": stats.get("commentCount", "확인 불가"),
            "description": item["snippet"]["description"][:300],
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
                "category": "AI 실무",
                "source_type": "YouTube",
                "source_name": r["channel"],
                "title": r["title"],
                "url": r["url"],
                "published_at": r["published_at"],
                "views": r["views"],
                "likes": r["likes"],
                "comments": r["comments"],
                "reactions": "확인 불가",
                "summary": r["description"],
                "trend_keywords": r["keyword"],
                "verification_status": "metric_unavailable" if r["views"] == "확인 불가" else "verified",
                "notes": "",
            })
    return filepath


if __name__ == "__main__":
    all_results = []
    for keyword in SEARCH_KEYWORDS:
        results = search_youtube(keyword)
        all_results.extend(results)

    output_dir = os.path.join("data", "raw")
    filepath = save_to_csv(all_results, output_dir)
    print(f"YouTube 데이터 저장 완료: {filepath} ({len(all_results)}건)")
