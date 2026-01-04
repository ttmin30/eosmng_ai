import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from modules.prompts import FILTER_TEMPLATE, ANALYZE_TEMPLATE

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
            PromptTemplate.from_template(FILTER_TEMPLATE) 
            | self.llm 
            | StrOutputParser()
        )

        # [2단계] 상세 분석 (JSON)
        self.analyze_chain = (
            PromptTemplate.from_template(ANALYZE_TEMPLATE) 
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