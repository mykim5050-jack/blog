# CLAUDE.md

## 프로젝트 한 줄 정의

이 프로젝트는 김용태 브런치 브랜드를 위해 매일 최신 AI, 창업, 부업, 콘텐츠 수익화, 1인 창업, 정부지원사업 트렌드를 수집·검증·분석하고, 브런치 글감, 발행 초안, PDF 리포트, Gmail 승인 발송문, Notion 누적 저장용 데이터를 생성하는 블로그 작성 자동화 시스템이다.

## 최종 목표

단순한 뉴스 요약기가 아니라, 사용자의 전문성과 관점을 반영한 브런치 콘텐츠 생산 에이전트로 작동한다.

핵심 목표는 다음과 같다.

1. 매일 20:00 KST 기준 최신 트렌드 수집
2. 출처, 날짜, 반응 수, 조회수 등 확인 가능한 데이터 검증
3. 김용태 브런치 브랜드에 맞는 글감 10개 추천
4. 가장 적합한 글감 1개를 내일 오전 발행용 브런치 초안으로 작성
5. 다음 주 평일 콘텐츠 캘린더 작성
6. 10~15페이지 브랜드 PDF 리포트 구성
7. Gmail 발송용 문안 작성
8. Notion 붙여넣기용 데이터베이스 표 생성
9. 사용자의 승인 전 Gmail 발송 금지
10. 허위 수치, 허구 사례, 과장된 수익 표현 금지

## Claude Code 운영 원칙

Claude Code는 다음 순서로 작업한다.

1. 먼저 저장소 구조와 기존 파일을 확인한다.
2. 바로 작성하지 말고, 수집 범위와 산출물 구조를 먼저 짧게 계획한다.
3. 웹 자료, YouTube, 정부 공고, 뉴스, Product Hunt, Reddit 등 최신 자료를 확인한다.
4. 출처별 사실과 수치를 검증한다.
5. 수치가 확인되지 않으면 `확인 불가`로 표기한다.
6. 사용자의 실제 경험으로 확인되지 않은 사례는 만들지 않는다.
7. 결과물을 Markdown, PDF 리포트용 Markdown, Notion 표, Gmail 초안으로 분리해 저장한다.
8. 작업 후 자체 품질 검증 체크리스트를 반드시 실행한다.
9. Gmail 발송, Notion API 저장, 브런치 업로드 등 외부 반영 작업은 사용자 승인 전 실행하지 않는다.

## 권장 프로젝트 구조

```text
블로그 작성/
├── CLAUDE.md
├── README.md
├── .env.example
├── .claude/
│   ├── commands/
│   │   ├── daily-report.md
│   │   ├── draft-brunch.md
│   │   ├── make-pdf.md
│   │   └── notion-table.md
│   └── settings.json
├── data/
│   ├── raw/
│   ├── processed/
│   └── notion/
├── reports/
│   ├── markdown/
│   ├── pdf/
│   └── email/
├── drafts/
│   ├── brunch/
│   └── titles/
├── templates/
│   ├── report-template.md
│   ├── brunch-template.md
│   ├── email-template.md
│   └── notion-schema.md
├── scripts/
│   ├── collect_youtube.py
│   ├── collect_news.py
│   ├── collect_government.py
│   ├── collect_producthunt.py
│   ├── collect_reddit.py
│   ├── generate_report.py
│   ├── export_pdf.py
│   ├── create_gmail_draft.py
│   └── notion_export.py
└── outputs/
    └── YYYY-MM-DD/
        ├── sources.csv
        ├── trend_report.md
        ├── brunch_draft.md
        ├── notion_table.md
        ├── email_draft.md
        └── pdf_report.pdf
```

## 매일 실행 기준

실행 시간은 매일 20:00 KST로 한다.

GitHub Actions를 사용할 때는 KST 기준 20:00가 되도록 시간대를 명확히 지정한다.

```yaml
name: Daily Brunch Trend Report

on:
  schedule:
    - cron: "0 20 * * *"
      timezone: "Asia/Seoul"
  workflow_dispatch:

jobs:
  create-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Claude Code daily report
        run: |
          claude -p "Run the daily Brunch trend report workflow based on CLAUDE.md. Do not send email. Create draft outputs only."
```

UTC 방식 대체:

```yaml
on:
  schedule:
    - cron: "0 11 * * *"
```

## 사용자 브랜드 정보

브런치 주소: https://brunch.co.kr/@baf3dc9ab38e4a8

브랜드 방향:

- AI를 실무와 창업에 연결하는 글
- 1인 창업자와 예비창업자를 위한 실행 전략
- 정부지원사업, 사업계획서, 평가위원 관점
- AI 시대에 창업자가 살아남는 방법
- 부업, 콘텐츠 수익화, 1인 비즈니스
- 이론보다 실제 경험, 실패, 심사, 수주, 투자 관점이 들어간 글
- 담백하고 현실적인 문장
- 과장보다 검증, 유행보다 실행, 정보보다 관점

신뢰 자산:

- 창업/벤처 분야 경영학 박사
- 정부지원사업 50건 이상 직접 수주 경험
- IITP, NIPA, 창업진흥원 등 정부기관 평가위원 경험
- 수천 개 사업제안서 심사 경험
- 스타트업 투자심사역 경험
- 저서: AI가 말하는 창업 성공 전략

블로그 하단 저자 소개 고정 문구:

```text
필자는 IITP, NIPA, 창업진흥원(예창패·초창패) 등 정부기관 평가위원으로 수천 개의 사업제안서를 심사했다. 동시에 50건 이상의 정부지원사업을 직접 수주한 창업자이자 스타트업 투자심사역으로 활동했다. 경영학 박사(창업/벤처), 저서 『AI가 말하는 창업 성공 전략』(2024)
```

## 문체 규칙

- 제목 바로 아래에 부제목을 넣는다.
- 문장은 짧고 담백하게 쓴다.
- AI가 쓴 글처럼 보이는 과한 특수문자, 이모지, 별표 강조를 사용하지 않는다.
- 자극적인 돈벌이 표현을 피한다.
- "월 1,000만 원 가능" 같은 검증 불가능한 문구를 쓰지 않는다.
- AI를 만능 도구로 말하지 않는다.
- AI는 실행과 검증을 빠르게 돕는 도구로 설명한다.
- 독자가 읽고 바로 실행할 수 있는 체크리스트를 포함한다.
- 사용자의 경험은 사실 기반으로만 활용한다.
- 구체 사례가 부족한 경우 `이 부분에는 사용자의 실제 사례를 한 문단 추가하세요.`라고 표시한다.

선호하는 문장 흐름:

```text
결론부터 말하면, 지금 창업자에게 필요한 것은 더 많은 도구가 아니라 더 빠른 검증 구조다.

내가 평가위원으로 사업계획서를 보면서 자주 느낀 것은, 많은 창업자가 기술보다 실행 구조를 설명하지 못한다는 점이다.

AI는 이 문제를 일부 줄여줄 수 있다. 하지만 AI가 사업을 대신해주지는 않는다.
```

피해야 할 문장 흐름:

```text
이제 누구나 AI로 쉽게 돈을 벌 수 있습니다.
하루 10분이면 자동 수익이 가능합니다.
무조건 성공하는 방법을 알려드립니다.
```

## 수집 우선순위

1순위: YouTube, 뉴스, 정부 공고
2순위: 해외 AI 뉴스레터, Product Hunt, Reddit
3순위: 블로그, X, 커뮤니티 반응

## 수집 주제

다음 주제 중 하나 이상과 연결되는 자료만 저장한다.

- AI 실무, 생성형 AI, AI 자동화, 업무 자동화, 노코드 자동화
- Claude Code, ChatGPT, Gemini, Perplexity, Notion AI
- 부업, 콘텐츠 수익화, 1인 창업, 솔로프러너, 마이크로 SaaS
- 전자책, 강의, 템플릿, 뉴스레터
- 정부지원사업, 예비창업패키지, 초기창업패키지, 청년창업사관학교
- 소상공인 지원사업, 사업계획서, 투자유치, MVP, 고객 검증, 랜딩페이지

## 출처별 수집 기준

### YouTube

YouTube Data API `videos.list`에서 `statistics.viewCount`, `likeCount`, `commentCount`를 확인한다.

수집 필드: URL, 영상 제목, 채널명, 업로드일, 조회수, 좋아요 수, 댓글 수, 영상 설명, 댓글 반복 질문, 썸네일 제목 패턴, 콘텐츠 구성 방식, 브런치 글감 전환 가능성

검색 키워드: AI 자동화 실무, AI 부업, ChatGPT 업무 자동화, Claude Code 사용법, Notion 자동화, n8n AI workflow, AI agent business, solopreneur AI automation, 정부지원사업 사업계획서, 예비창업패키지 선정 팁

### 뉴스

- 최근 7일 이내 자료 우선
- 동일 이슈는 최소 2개 출처로 교차 확인
- 수집 필드: 제목, 매체명, 발행일, URL, 핵심 사실, 브런치 관점 전환 포인트, 독자에게 주는 실행 시사점

### 정부 공고

우선 확인 사이트: K-Startup, 기업마당, 중소벤처기업부, 창업진흥원, 소상공인시장진흥공단, NIPA, IITP, 지역 창조경제혁신센터

수집 필드: 사업명, 기관명, 신청 기간, 지원 대상, 지원 금액, 지원 내용, URL, 브런치 글감 연결 포인트, 사업계획서 작성 관점, 평가위원 관점 주의사항

### Product Hunt

수집 기준: AI, productivity, marketing, automation, no-code, creator, startup 관련 제품 우선. upvotes, comments, launch date 확인.

### Reddit

수집 서브레딧: r/Entrepreneur, r/SideProject, r/SaaS, r/ArtificialInteligence, r/ChatGPT, r/n8n, r/Notion, r/solopreneur, r/smallbusiness

## 데이터 저장 형식

매일 수집 원천 데이터는 `data/raw/YYYY-MM-DD-sources.csv`로 저장한다.

```csv
date,category,source_type,source_name,title,url,published_at,views,likes,comments,reactions,summary,trend_keywords,verification_status,notes
```

검증 상태 값: `verified`, `partially_verified`, `metric_unavailable`, `source_unreliable`, `excluded`

## 트렌드 점수화 기준 (35점 만점)

| 항목 | 기준 | 점수 |
|---|---|---|
| 최신성 | 최근 7일 또는 30일 내 상승 중인가 | 1~5 |
| 독자성 | 브런치 독자에게 실질 도움이 되는가 | 1~5 |
| 전문성 | 사용자 경험과 신뢰 자산을 녹일 수 있는가 | 1~5 |
| 수익성 | 강의, 전자책, 컨설팅, 템플릿으로 확장 가능한가 | 1~5 |
| 지속성 | 시리즈로 확장 가능한가 | 1~5 |
| 차별성 | 일반 요약이 아니라 사용자의 관점이 들어가는가 | 1~5 |
| 실행성 | 독자가 바로 적용할 수 있는가 | 1~5 |

동점 시 우선순위: 사용자 전문성 → 정부지원사업 확장 가능성 → 내일 오전 발행 가능 → 후속 상품화 가능성

## 분석 페르소나

매일 결과를 낼 때 아래 6개 관점을 독립적으로 적용한 뒤 편집장이 통합한다.

- **페르소나 A: AI 실무 자동화 전문가** — 자동화 아이디어, 실무 적용 예시, 프롬프트/템플릿화 가능성
- **페르소나 B: 1인 창업 전략가** — 1인 창업자 관점 인사이트, 실행 체크리스트, 주의사항
- **페르소나 C: 정부지원사업 평가위원** — 사업계획서 연결 포인트, 평가위원 관점 경고, 지원사업 글감 확장 가능성
- **페르소나 D: 투자심사역** — 투자자 관점 핵심 질문, 검증해야 할 지표, 투자 가능성과 리스크
- **페르소나 E: 콘텐츠 수익화 전략가** — 수익화 가능성, 후속 상품 아이디어, 제목/썸네일/시리즈 전략
- **페르소나 F: 브런치 에디터** — 추천 제목, 도입부 문장, 본문 목차, 개인 스토리 삽입 위치, 마지막 문장

## 매일 최종 출력 순서

1. 오늘의 트렌드 한 줄 요약
2. 상위 트렌드 표
3. 추천 글감 10개
4. 내일 발행용 브런치 초안
5. 다음 주 콘텐츠 캘린더
6. PDF 리포트 구성안
7. Gmail 발송문
8. Notion 저장용 표
9. 오늘의 최종 추천 3개
10. 다음 실행 액션

## 검증 규칙

- 모든 자료는 URL을 저장한다.
- 수치 데이터는 원문 또는 API에서 확인된 경우만 사용한다.
- 확인되지 않은 수치는 `확인 불가`로 표기한다.
- 여러 출처의 수치가 충돌하면 최신 원문 또는 공식 API를 우선한다.
- 사용자의 실제 이력으로 제공된 사실만 사용한다.
- 사례가 필요한 경우: `이 부분에는 사용자의 실제 사례를 한 문단 추가하세요.`
- 정부지원사업 선정 가능성을 보장하지 않는다.
- API 키 또는 토큰 노출 금지

## 품질 검증 체크리스트

최종 결과 전 다음 10개 질문에 답한다.

```markdown
## 품질 검증 결과

1. 이 글감은 단순 정보 요약이 아니라 사용자 관점이 들어가는가? 예/아니오
2. AI, 창업, 부업, 정부지원사업 중 최소 하나와 명확히 연결되는가? 예/아니오
3. 독자가 읽고 바로 실행할 수 있는가? 예/아니오
4. 제목이 너무 흔하지 않은가? 예/아니오
5. 사용자 경험을 억지로 끼워 넣지 않았는가? 예/아니오
6. 브런치 글로 읽히는 서사가 있는가? 예/아니오
7. 후속 콘텐츠나 수익화로 확장 가능한가? 예/아니오
8. 출처와 데이터가 명확한가? 예/아니오
9. 과장된 돈벌이 문구를 쓰지 않았는가? 예/아니오
10. 사용자 브랜드 자산을 강화하는가? 예/아니오
```

하나라도 `아니오`가 있으면 해당 부분을 수정한 뒤 최종 산출물을 저장한다.

## 최종 금지사항

절대 하지 말 것:

- 사용자의 승인 없이 Gmail 발송
- 사용자의 승인 없이 브런치 업로드
- 사용자의 승인 없이 Notion API에 실제 저장
- 확인되지 않은 조회수, 좋아요, 댓글 수 생성
- 실제 경험처럼 보이는 허구 사례 작성
- 정부지원사업 선정 가능성 보장
- AI로 쉽게 돈 번다는 식의 과장 표현
- 출처 없는 최신 정보 단정
- API 키 또는 토큰 노출

항상 할 것:

- 출처 URL 저장
- 수치 미확인 시 `확인 불가` 표기
- 사용자의 평가위원, 수주 경험, 투자심사 관점을 자연스럽게 반영
- 브런치 제목 아래 부제목 삽입
- 실행 체크리스트 포함
- 승인 후 발송 원칙 준수
