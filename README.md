# 김용태 브런치 자동화 시스템

매일 13:00 KST 기준으로 AI·창업·부업·정부지원사업 트렌드를 수집하고, 브런치 초안·PDF 리포트·Gmail 초안·Notion 표를 자동 생성하는 시스템이다.

## 빠른 시작

### 1. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일에 각 API 키 입력
```

### 2. 의존성 설치

```bash
pip install google-api-python-client google-auth requests notion-client
```

### 3. 오늘 리포트 실행 (Claude Code)

```text
오늘 날짜 기준으로 김용태 브런치 데일리 트렌드 리포트를 생성해줘.
CLAUDE.md의 전체 지침을 따라줘.
```

또는 slash command 사용:

```
/daily-report
```

## Slash Commands

| 명령어 | 설명 |
|---|---|
| `/daily-report` | 전체 워크플로우 실행 |
| `/draft-brunch` | 브런치 초안만 생성 |
| `/make-pdf` | PDF 리포트용 Markdown 생성 |
| `/notion-table` | Notion 붙여넣기용 표 생성 |

## 산출물 구조

매일 `outputs/YYYY-MM-DD/` 폴더에 다음 파일이 생성된다.

| 파일 | 설명 |
|---|---|
| `sources.csv` | 수집 원천 데이터 |
| `trend_report.md` | 트렌드 분석 리포트 |
| `brunch_draft.md` | 내일 발행용 브런치 초안 |
| `notion_table.md` | Notion 붙여넣기용 표 |
| `email_draft.md` | Gmail 발송문 초안 |

## 중요 원칙

- Gmail 발송, 브런치 업로드, Notion 저장은 사용자 승인 후에만 실행한다.
- 확인되지 않은 수치는 `확인 불가`로 표기한다.
- 허구 사례, 허위 수치, 과장된 수익 표현은 생성하지 않는다.
- API 키는 절대 커밋하지 않는다.

## 브런치 주소

https://brunch.co.kr/@baf3dc9ab38e4a8
