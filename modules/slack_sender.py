import os
import requests
import json
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class SlackSender:
    def __init__(self):
        self.webhook_url = os.getenv("SLACK_WEBHOOK_URL")

    def send_alert(self, risk_list):
        """
        위험 리스트를 받아 슬랙으로 전송하는 함수
        """
        if not self.webhook_url:
            print("⚠️ [경고] .env에 SLACK_WEBHOOK_URL이 없어 알림을 보낼 수 없습니다.")
            return

        if not risk_list:
            return

        # 1. 메시지 헤더 (제목)
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "🚨 [긴급] 보안 위협 탐지 알림",
                    "emoji": True
                }
            },
            {"type": "divider"}
        ]

        # 2. 각 위험 항목을 블록으로 만들어 추가
        for risk in risk_list:
            # 위험한 자산 이름과 뉴스 제목
            content = (
                f"*📢 {risk['title']}*\n"
                f"🎯 **타겟 자산:** `{risk['asset']}`\n"
                f"📝 **분석 결과:** {risk['reason']}\n"
                f"🔗 <{risk['link']}|원문 보러가기>"
            )
            
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content
                }
            })
            blocks.append({"type": "divider"})

        # 3. 최종 전송 (JSON Payload)
        payload = {"blocks": blocks}
        
        try:
            response = requests.post(
                self.webhook_url, 
                data=json.dumps(payload),
                headers={'Content-Type': 'application/json'}
            )
            if response.status_code == 200:
                print("📨 [Slack] 알림 전송 성공!")
            else:
                print(f"❌ [Slack] 전송 실패: {response.text}")
        except Exception as e:
            print(f"❌ [Slack] 연결 오류: {e}")