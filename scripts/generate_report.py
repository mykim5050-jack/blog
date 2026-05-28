import os
import csv
from datetime import date

def load_sources(data_dir):
    today = date.today().isoformat()
    filepath = os.path.join(data_dir, f"{today}-sources.csv")
    if not os.path.exists(filepath):
        print(f"소스 파일 없음: {filepath}")
        return []
    with open(filepath, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def generate_trend_report(sources, output_dir):
    today = date.today().isoformat()
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, f"{today}-trend_report.md")

    categories = {}
    for row in sources:
        cat = row.get("category", "기타")
        categories.setdefault(cat, []).append(row)

    lines = [f"# {today} 트렌드 리포트\n"]
    lines.append("## 오늘의 트렌드 한 줄 요약\n\n[작성 필요]\n")
    lines.append("## 상위 트렌드 표\n")
    lines.append("| 순위 | 트렌드 | 근거 데이터 | 왜 뜨는가 | 내 브런치와의 연결성 | 추천 점수 |")
    lines.append("|---|---|---|---|---|---|")

    for i, row in enumerate(sources[:10], 1):
        lines.append(f"| {i} | {row.get('title','')} | {row.get('source_name','')} | | | |")

    lines.append("\n## 수집 데이터 요약\n")
    for cat, items in categories.items():
        lines.append(f"\n### {cat} ({len(items)}건)\n")
        for item in items[:3]:
            lines.append(f"- [{item.get('title','')}]({item.get('url','')})")
            lines.append(f"  - 출처: {item.get('source_name','')} | 날짜: {item.get('published_at','')}")
            lines.append(f"  - 검증: {item.get('verification_status','')}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filepath


if __name__ == "__main__":
    sources = load_sources(os.path.join("data", "raw"))
    if sources:
        filepath = generate_trend_report(sources, os.path.join("reports", "markdown"))
        print(f"트렌드 리포트 생성 완료: {filepath}")
    else:
        print("수집된 소스 데이터가 없습니다. 수집 스크립트를 먼저 실행하세요.")
