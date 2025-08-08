import aiohttp
import os
from datetime import datetime
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()

class NewsCollector:
    def __init__(self):
        self.client_id = "5vs7W5qwlVVfQxqf1vUY"  # 네이버 개발자 센터에서 발급받은 클라이언트 ID
        self.client_secret = "L2CB2x88s4"  # 네이버 개발자 센터에서 발급받은 클라이언트 시크릿
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

    async def fetch_news(self, query: str = "kwater OR 한국수자원공사", max_results: int = 100) -> List[Dict[str, Any]]:
        all_articles = []
        start = 1
        display = 100  # 최대 표시 개수

        while len(all_articles) < max_results:
            params = {
                "query": query,
                "display": display,
                "start": start,
                "sort": "date"
            }

            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, headers=self.headers, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to fetch news: {response.status}")
                    
                    data = await response.json()
                    items = data.get("items", [])
                    
                    if not items:  # 더 이상 결과가 없으면 종료
                        break
                    
                    filtered_items = self._filter_articles(items)
                    all_articles.extend(filtered_items)
                    
                    if len(items) < display:  # 마지막 페이지면 종료
                        break
                    
                    start += display  # 다음 페이지로 이동

        return all_articles[:max_results]  # 요청한 개수만큼 반환

    def _filter_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        keywords = ["kwater", "한국수자원공사"]
        filtered_articles = []

        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            
            if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
                try:
                    published_at = datetime.strptime(article.get("pubDate", ""), "%a, %d %b %Y %H:%M:%S %z")
                except:
                    published_at = datetime.now()
                
                filtered_articles.append({
                    "title": article.get("title", "").replace("<b>", "").replace("</b>", ""),
                    "content": article.get("description", "").replace("<b>", "").replace("</b>", ""),
                    "url": article.get("link", ""),
                    "published_at": published_at
                })

        return filtered_articles 