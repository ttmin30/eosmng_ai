import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 환경변수 로드
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

class VulnAnalyzer:
    def __init__(self):
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("❌ .env 파일에 GOOGLE_API_KEY가 없습니다.")

        # 환경에 맞는 모델
        self.llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

        # [1단계] 제목 필터링
        self.filter_chain = (
            PromptTemplate.from_template("""
                [자산 목록] {assets}
                [뉴스 제목] {titles_text}
                
                위 뉴스 제목들 중 내 자산(제품명)과 관련 있어 보이는 뉴스의 '번호(ID)'를 모두 찾으세요.
                관련 없으면 "NONE" 출력.
                
                답변 형식: 번호만 쉼표로 구분 (예: 0, 2, 5)
            """) 
            | self.llm 
            | StrOutputParser()
        )

        # [2단계] 상세 분석 (JSON)
        self.analyze_chain = (
            PromptTemplate.from_template("""
                당신은 보안 분석가입니다. [뉴스 텍스트]를 분석해 [자산 목록]에 대한 위험 여부를 판단하세요.

                [자산 목록] {assets}
                [뉴스 텍스트] {news_list_text}

                [판단 기준]
                1. 뉴스 본문에 내 자산명(MongoDB, React 등)이 명시되어야 함. (CISA 공지 주의)
                2. 버전 범위("4.4.0 이상 ~ 4.4.30 미만")를 수학적으로 계산하여 내 버전이 포함되면 RISK.
                3. 버전 정보가 없으면 "버전 미표기 위험"으로 RISK 처리.

                [답변 형식 (JSON List)]
                [
                    {{
                        "index": 뉴스번호(정수),
                        "status": "RISK" 또는 "SAFE",
                        "asset": "자산명 (버전)",
                        "reason": "이유 요약"
                    }}
                ]
            """) 
            | self.llm 
            | StrOutputParser()
        )

    def filter_by_title(self, assets_str, news_list):
        titles = "".join([f"{i}. {n['title']}\n" for i, n in enumerate(news_list)])
        try:
            res = self.filter_chain.invoke({"assets": assets_str, "titles_text": titles})
            if "NONE" in res: return []
            return [int(x) for x in res.split(',') if x.strip().isdigit()]
        except: return []

    def analyze_risks(self, assets_str, news_list):
        if not news_list: return []
        
        # 뉴스 텍스트 생성 (인덱스 포함)
        block = ""
        for item in news_list:
            idx = item['original_index']
            block += f"\n[뉴스 {idx}]\n제목: {item['title']}\n내용: {item['description']}\n"

        try:
            raw = self.analyze_chain.invoke({"assets": assets_str, "news_list_text": block})
            # 마크다운 제거 후 파싱
            clean_json = raw.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_json)
        except Exception as e:
            print(f"❌ JSON 파싱 에러: {e}\n원본응답: {raw}")
            return []