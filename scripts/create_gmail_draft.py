"""
Gmail 초안 생성 스크립트.
실제 발송은 사용자 승인 후에만 실행한다.
"""
import os
import base64
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

RECIPIENT = "mykim5050@gmail.com"

def load_email_draft(draft_path):
    if not os.path.exists(draft_path):
        raise FileNotFoundError(f"이메일 초안 파일 없음: {draft_path}")
    with open(draft_path, encoding="utf-8") as f:
        return f.read()


def create_draft(subject, body, recipient=RECIPIENT):
    creds = Credentials(
        token=None,
        refresh_token=os.environ.get("GMAIL_REFRESH_TOKEN"),
        client_id=os.environ.get("GMAIL_CLIENT_ID"),
        client_secret=os.environ.get("GMAIL_CLIENT_SECRET"),
        token_uri="https://oauth2.googleapis.com/token",
    )
    service = build("gmail", "v1", credentials=creds)

    message = MIMEMultipart()
    message["to"] = recipient
    message["subject"] = subject
    message.attach(MIMEText(body, "plain", "utf-8"))

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw}},
    ).execute()
    return draft["id"]


if __name__ == "__main__":
    today = date.today().isoformat()
    draft_path = os.path.join("reports", "email", f"{today}-email-draft.md")

    print("Gmail 초안 생성 중...")
    print("중요: 실제 발송은 사용자 승인 후에만 실행됩니다.")

    content = load_email_draft(draft_path)
    lines = content.split("\n")

    subject = f"[{today}] 김용태 AI·창업·부업 트렌드 리포트"
    draft_id = create_draft(subject, content)
    print(f"Gmail 초안 생성 완료. Draft ID: {draft_id}")
    print("Gmail에서 초안을 확인하고 승인 후 발송하세요.")
