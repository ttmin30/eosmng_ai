import feedparser
import re

class RSSReader:
    def __init__(self):
        # ✅ 보안 권고문(상세 정보 포함) URL 사용
        self.rss_url = "https://knvd.krcert.or.kr/rss/securityNotice.do"

    def clean_html(self, raw_html):
        """HTML 태그 제거 (<br>, <table> 등)"""
        if not raw_html: return ""
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, ' ', raw_html) # 태그를 공백으로 치환
        return cleantext.strip()

    def get_latest_news(self, limit=30):
        try:
            feed = feedparser.parse(self.rss_url)
            if not feed.entries: return []
            
            news_list = []
            for i, entry in enumerate(feed.entries[:limit]):
                raw_desc = getattr(entry, 'description', '')
                clean_desc = self.clean_html(raw_desc)[:800] # 내용은 넉넉히
                
                news_list.append({
                    "original_index": i, # 원본 순서 기억
                    "title": entry.title,
                    "link": entry.link,
                    "description": clean_desc
                })
            return news_list
        except Exception as e:
            print(f"❌ RSS 에러: {e}")
            return []