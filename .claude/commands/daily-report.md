오늘 날짜 기준으로 CLAUDE.md의 전체 워크플로우를 실행하라.

필수 조건:
- 최신 자료를 웹에서 확인한다.
- YouTube, 뉴스, 정부 공고를 우선한다.
- 수치가 확인되지 않으면 확인 불가로 표기한다.
- 허구 사례를 만들지 않는다.
- 브런치 초안은 2,500~3,500자로 작성한다.
- PDF와 Gmail은 초안만 만든다.
- 실제 발송은 하지 않는다.

중복 체크 (필수):
- 실행 전 drafts/published_titles.txt 를 반드시 읽는다.
- 파일에 있는 제목·주제와 겹치는 글감은 선정하지 않는다.
- 리포트 완료 후 오늘 선정된 글 제목을 published_titles.txt 에 자동 추가한다.
  형식: YYYY-MM-DD | 제목

brunch_publish.txt 작성 규칙:
- ##, **, # 등 Markdown 특수문자 사용 금지
- 섹션 구분은 빈 줄 2개로 처리
- 파일 맨 끝에 이미지 생성 프롬프트 2개를 항상 포함한다
  - 이미지 1: 커버/썸네일용 (16:9), 글의 핵심 분위기를 반영
  - 이미지 2: 본문 삽입용 (4:3), 핵심 개념을 시각화
  - 딥네이비 + 화이트 + 민트 컬러 스키마 유지
  - 이미지 안에 텍스트 없음

출력 파일:
- outputs/YYYY-MM-DD/sources.csv
- outputs/YYYY-MM-DD/trend_report.md
- outputs/YYYY-MM-DD/brunch_draft.md       ← Markdown 유지, 수정·참고용
- outputs/YYYY-MM-DD/brunch_publish.txt    ← 특수문자 없음 + 이미지 프롬프트 포함, 브런치 복붙 전용
- outputs/YYYY-MM-DD/notion_table.md
- outputs/YYYY-MM-DD/email_draft.md
