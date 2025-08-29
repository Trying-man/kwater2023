import aiohttp
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv
import logging
import html
import re
import asyncio
from database_mongo import get_async_collection, create_indexes
from bson import ObjectId

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class NewsCollectorMongo:
    def __init__(self):
        self.client_id = os.getenv("NAVER_CLIENT_ID", "5vs7W5qwlVVfQxqf1vUY")
        self.client_secret = os.getenv("NAVER_CLIENT_SECRET", "L2CB2x88s4")
        self.base_url = "https://openapi.naver.com/v1/search/news.json"
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }
        
        # MongoDB 인덱스 생성
        try:
            create_indexes()
        except Exception as e:
            logger.warning(f"MongoDB 인덱스 생성 실패: {e}")

    def _clean_text(self, text: str) -> str:
        """
        텍스트를 정리하고 인코딩 문제를 해결합니다.
        """
        if not text:
            return ""
        
        # HTML 엔티티 디코딩
        text = html.unescape(text)
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        
        # 특수 문자 정리
        text = text.replace('&quot;', '"')
        text = text.replace('&amp;', '&')
        text = text.replace('&lt;', '<')
        text = text.replace('&gt;', '>')
        text = text.replace('&nbsp;', ' ')
        
        # 연속된 공백 제거
        text = re.sub(r'\s+', ' ', text)
        
        # 앞뒤 공백 제거
        text = text.strip()
        
        return text

    async def save_articles_to_mongo(self, articles: List[Dict[str, Any]], sentiment_analyzer=None) -> Dict[str, Any]:
        """
        수집된 기사들을 MongoDB에 저장합니다.
        """
        try:
            collection = await get_async_collection()
            
            saved_count = 0
            duplicate_count = 0
            error_count = 0
            
            for article in articles:
                try:
                    # URL이 이미 존재하는지 확인
                    existing = await collection.find_one({"url": article["url"]})
                    if existing:
                        duplicate_count += 1
                        continue
                    
                    # 감정분석 수행
                    if sentiment_analyzer:
                        text_for_analysis = f"{article['title']} {article['content']}"
                        sentiment = sentiment_analyzer.analyze(text_for_analysis)
                        article["sentiment"] = sentiment
                    else:
                        article["sentiment"] = None
                    
                    # MongoDB 문서 형식으로 변환
                    mongo_doc = {
                        "title": article["title"],
                        "content": article["content"],
                        "url": article["url"],
                        "published_at": article["published_at"],
                        "sentiment": article["sentiment"],
                        "created_at": datetime.now(),
                        "updated_at": datetime.now()
                    }
                    
                    # MongoDB에 저장
                    result = await collection.insert_one(mongo_doc)
                    saved_count += 1
                    
                except Exception as e:
                    logger.error(f"기사 저장 실패: {str(e)}")
                    error_count += 1
                    continue
            
            return {
                "status": "success",
                "saved_count": saved_count,
                "duplicate_count": duplicate_count,
                "error_count": error_count,
                "total_processed": len(articles)
            }
            
        except Exception as e:
            logger.error(f"MongoDB 저장 실패: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }

    async def fetch_news_extensive(self, query: str = "kwater OR 한국수자원공사", max_results: int = 1000) -> List[Dict[str, Any]]:
        """
        방대한 양의 뉴스를 수집합니다. 여러 키워드와 기간을 조합하여 수집합니다.
        """
        all_articles = []
        
        # 다양한 검색 키워드 조합
        search_queries = [
            "kwater OR 한국수자원공사",
            "한국수자원공사",
            "K-water",
            "수자원공사",
            "물관리",
            "댐",
            "수도",
            "상수도",
            "하수도",
            "물산업"
        ]
        
        # 각 키워드별로 수집
        for search_query in search_queries:
            try:
                logger.info(f"키워드 '{search_query}'로 뉴스 수집 중...")
                articles = await self._fetch_news_by_query(search_query, max_results // len(search_queries))
                all_articles.extend(articles)
                logger.info(f"키워드 '{search_query}'에서 {len(articles)}개 기사 수집 완료")
                
                # API 호출 제한을 위한 대기
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.error(f"키워드 '{search_query}' 수집 중 오류: {str(e)}")
                continue
        
        # 중복 제거 (URL 기준)
        unique_articles = self._remove_duplicates(all_articles)
        logger.info(f"총 {len(all_articles)}개 기사 수집, 중복 제거 후 {len(unique_articles)}개")
        
        return unique_articles[:max_results]

    async def _fetch_news_by_query(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        특정 쿼리로 뉴스를 수집합니다.
        """
        all_articles = []
        start = 1
        display = 100  # 최대 표시 개수
        max_pages = 10  # 최대 페이지 수 제한

        page_count = 0
        while len(all_articles) < max_results and page_count < max_pages:
            params = {
                "query": query,
                "display": display,
                "start": start,
                "sort": "date"
            }

            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.base_url, headers=self.headers, params=params) as response:
                        if response.status != 200:
                            logger.warning(f"API 호출 실패: {response.status}")
                            break
                        
                        data = await response.json()
                        items = data.get("items", [])
                        
                        if not items:  # 더 이상 결과가 없으면 종료
                            break
                        
                        filtered_items = self._filter_articles(items)
                        all_articles.extend(filtered_items)
                        
                        if len(items) < display:  # 마지막 페이지면 종료
                            break
                        
                        start += display  # 다음 페이지로 이동
                        page_count += 1
                        
            except Exception as e:
                logger.error(f"페이지 {page_count} 수집 중 오류: {str(e)}")
                break

        return all_articles

    def _remove_duplicates(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        URL 기준으로 중복을 제거합니다.
        """
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get("url", "")
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles

    async def fetch_news(self, query: str = "kwater OR 한국수자원공사", max_results: int = 100) -> List[Dict[str, Any]]:
        """
        기본 뉴스 수집 메서드 (기존 호환성 유지)
        """
        return await self._fetch_news_by_query(query, max_results)

    def _filter_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        keywords = ["kwater", "한국수자원공사", "수자원", "물관리", "댐", "수도", "상수도", "하수도"]
        filtered_articles = []

        for article in articles:
            title = article.get("title", "").lower()
            description = article.get("description", "").lower()
            
            # 키워드 매칭 조건을 완화
            if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
                try:
                    published_at = datetime.strptime(article.get("pubDate", ""), "%a, %d %b %Y %H:%M:%S %z")
                except:
                    published_at = datetime.now()
                
                # 텍스트 정리
                clean_title = self._clean_text(article.get("title", ""))
                clean_content = self._clean_text(article.get("description", ""))
                
                filtered_articles.append({
                    "title": clean_title,
                    "content": clean_content,
                    "url": article.get("link", ""),
                    "published_at": published_at.isoformat() if published_at else None
                })

        return filtered_articles

    async def collect_and_save_news(self, query: str = "kwater OR 한국수자원공사", max_results: int = 100, sentiment_analyzer=None) -> Dict[str, Any]:
        """
        뉴스를 수집하고 MongoDB에 저장합니다.
        """
        try:
            # 뉴스 수집
            articles = await self.fetch_news_extensive(query, max_results)
            
            # MongoDB에 저장
            save_result = await self.save_articles_to_mongo(articles, sentiment_analyzer)
            
            return {
                "status": "success",
                "collected_count": len(articles),
                "save_result": save_result
            }
            
        except Exception as e:
            logger.error(f"뉴스 수집 및 저장 실패: {str(e)}")
            return {
                "status": "error",
                "message": str(e)
            }
