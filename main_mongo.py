from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
from news_collector_mongo import NewsCollectorMongo
from simple_sentiment_analyzer import SimpleSentimentAnalyzer
from database_mongo import get_async_collection, get_collection, create_indexes
from typing import List, Dict, Any
import uvicorn
from datetime import datetime, timedelta
from bson import ObjectId
import json

# MongoDB 인덱스 생성
try:
    create_indexes()
    print("MongoDB 인덱스 생성 완료!")
except Exception as e:
    print(f"MongoDB 인덱스 생성 실패: {e}")

# Pydantic 모델 정의
class SentimentRequest(BaseModel):
    text: str

class SentimentBatchRequest(BaseModel):
    texts: List[str]

class NewsCollectionRequest(BaseModel):
    query: str = "kwater OR 한국수자원공사"
    max_results: int = 100

app = FastAPI(title="News Collector API (MongoDB)", description="MongoDB 기반 네이버 뉴스 수집 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NewsCollector 인스턴스 생성
news_collector = NewsCollectorMongo()

# SentimentAnalyzer 인스턴스 생성
sentiment_analyzer = None
sentiment_available = False

# 간단한 규칙 기반 감정분석 모델 로딩
try:
    print("감정분석 모델을 로딩 중입니다...")
    sentiment_analyzer = SimpleSentimentAnalyzer()
    sentiment_available = True
    print("감정분석 모델 로딩 완료!")
except Exception as e:
    print(f"감정분석 모델 로딩 실패: {e}")
    print("감정분석 기능 없이 서버를 시작합니다.")
    sentiment_analyzer = None
    sentiment_available = False

@app.get("/")
async def root():
    return {"message": "News Collector API (MongoDB) is running!"}

@app.get("/news")
async def get_news(query: str = "kwater OR 한국수자원공사", max_results: int = 100):
    """
    뉴스를 검색하고 반환합니다.
    """
    try:
        articles = await news_collector.fetch_news(query, max_results)
        return {
            "status": "success",
            "count": len(articles),
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/search")
async def search_news_in_db(
    keyword: str = "",
    limit: int = 50,
    offset: int = 0,
    sentiment: str = None,
    days: int = None
):
    """
    MongoDB에 저장된 뉴스에서 제목과 내용으로 검색합니다.
    """
    try:
        collection = await get_async_collection()
        
        # 검색 조건 구성
        query = {}
        
        # 키워드 검색 (제목과 내용에서 검색)
        if keyword:
            query["$or"] = [
                {"title": {"$regex": keyword, "$options": "i"}},
                {"content": {"$regex": keyword, "$options": "i"}}
            ]
        
        # 감정 필터
        if sentiment:
            query["sentiment.sentiment"] = sentiment
        
        # 날짜 필터
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            query["published_at"] = {"$gte": cutoff_date.isoformat()}
        
        # 검색 실행
        cursor = collection.find(query).sort("published_at", -1).skip(offset).limit(limit)
        articles = await cursor.to_list(length=limit)
        
        # 총 검색 결과 수 계산
        total_count = await collection.count_documents(query)
        
        # 결과 포맷팅
        result_articles = []
        for article in articles:
            article["_id"] = str(article["_id"])
            if "created_at" in article:
                article["created_at"] = article["created_at"].isoformat()
            if "updated_at" in article:
                article["updated_at"] = article["updated_at"].isoformat()
            result_articles.append(article)
        
        return {
            "status": "success",
            "keyword": keyword,
            "total_count": total_count,
            "count": len(result_articles),
            "offset": offset,
            "limit": limit,
            "articles": result_articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/search/advanced")
async def advanced_search_news(
    title_keyword: str = "",
    content_keyword: str = "",
    sentiment: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 50,
    offset: int = 0
):
    """
    고급 검색 기능 - 제목과 내용을 별도로 검색할 수 있습니다.
    """
    try:
        collection = await get_async_collection()
        
        # 검색 조건 구성
        query = {}
        
        # 제목 검색
        if title_keyword:
            query["title"] = {"$regex": title_keyword, "$options": "i"}
        
        # 내용 검색
        if content_keyword:
            query["content"] = {"$regex": content_keyword, "$options": "i"}
        
        # 감정 필터
        if sentiment:
            query["sentiment.sentiment"] = sentiment
        
        # 날짜 범위 필터
        if start_date or end_date:
            date_query = {}
            if start_date:
                date_query["$gte"] = start_date
            if end_date:
                date_query["$lte"] = end_date
            query["published_at"] = date_query
        
        # 검색 실행
        cursor = collection.find(query).sort("published_at", -1).skip(offset).limit(limit)
        articles = await cursor.to_list(length=limit)
        
        # 총 검색 결과 수 계산
        total_count = await collection.count_documents(query)
        
        # 결과 포맷팅
        result_articles = []
        for article in articles:
            article["_id"] = str(article["_id"])
            if "created_at" in article:
                article["created_at"] = article["created_at"].isoformat()
            if "updated_at" in article:
                article["updated_at"] = article["updated_at"].isoformat()
            result_articles.append(article)
        
        return {
            "status": "success",
            "title_keyword": title_keyword,
            "content_keyword": content_keyword,
            "total_count": total_count,
            "count": len(result_articles),
            "offset": offset,
            "limit": limit,
            "articles": result_articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/extensive")
async def get_news_extensive(max_results: int = 500):
    """
    방대한 양의 뉴스를 수집합니다.
    """
    try:
        articles = await news_collector.fetch_news_extensive(max_results=max_results)
        return {
            "status": "success",
            "count": len(articles),
            "articles": articles,
            "message": f"총 {len(articles)}개의 기사를 수집했습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/extensive/with-sentiment")
async def get_news_extensive_with_sentiment(max_results: int = 200):
    """
    방대한 양의 뉴스를 수집하고 감정분석을 수행합니다.
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        articles = await news_collector.fetch_news_extensive(max_results=max_results)
        
        articles_with_sentiment = []
        for i, article in enumerate(articles):
            try:
                text_for_analysis = f"{article['title']} {article['content']}"
                sentiment = sentiment_analyzer.analyze(text_for_analysis)
                
                article_with_sentiment = {
                    **article,
                    "sentiment": sentiment
                }
                articles_with_sentiment.append(article_with_sentiment)
                
                if (i + 1) % 50 == 0:
                    print(f"감정분석 진행률: {i + 1}/{len(articles)}")
                    
            except Exception as e:
                print(f"기사 {i + 1} 감정분석 실패: {str(e)}")
                article_with_sentiment = {
                    **article,
                    "sentiment": {"sentiment": "neutral", "confidence": 0.0}
                }
                articles_with_sentiment.append(article_with_sentiment)
        
        return {
            "status": "success",
            "count": len(articles_with_sentiment),
            "articles": articles_with_sentiment,
            "message": f"총 {len(articles_with_sentiment)}개의 기사를 수집하고 감정분석을 완료했습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/news/collect-and-save")
async def collect_and_save_news(request: NewsCollectionRequest):
    """
    뉴스를 수집하고 MongoDB에 저장합니다.
    """
    try:
        result = await news_collector.collect_and_save_news(
            query=request.query,
            max_results=request.max_results,
            sentiment_analyzer=sentiment_analyzer
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/db")
async def get_news_from_db(
    limit: int = 50,
    offset: int = 0,
    sentiment: str = None,
    days: int = None
):
    """
    MongoDB에서 저장된 뉴스를 조회합니다.
    """
    try:
        collection = await get_async_collection()
        
        # 쿼리 조건 구성
        query = {}
        
        if sentiment:
            query["sentiment.sentiment"] = sentiment
        
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            query["published_at"] = {"$gte": cutoff_date.isoformat()}
        
        # MongoDB에서 조회
        cursor = collection.find(query).sort("published_at", -1).skip(offset).limit(limit)
        articles = await cursor.to_list(length=limit)
        
        # ObjectId를 문자열로 변환
        result_articles = []
        for article in articles:
            article["_id"] = str(article["_id"])
            if "created_at" in article:
                article["created_at"] = article["created_at"].isoformat()
            if "updated_at" in article:
                article["updated_at"] = article["updated_at"].isoformat()
            result_articles.append(article)
        
        return {
            "status": "success",
            "count": len(result_articles),
            "articles": result_articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/db/stats")
async def get_news_stats():
    """
    MongoDB에 저장된 뉴스 통계를 조회합니다.
    """
    try:
        collection = await get_async_collection()
        
        # 총 기사 수
        total_articles = await collection.count_documents({})
        
        # 감정별 통계
        pipeline = [
            {"$group": {"_id": "$sentiment.sentiment", "count": {"$sum": 1}}}
        ]
        sentiment_stats = await collection.aggregate(pipeline).to_list(length=None)
        sentiment_counts = {stat["_id"] or "Unknown": stat["count"] for stat in sentiment_stats}
        
        # 최근 7일간 통계
        week_ago = datetime.now() - timedelta(days=7)
        recent_articles = await collection.count_documents({
            "published_at": {"$gte": week_ago.isoformat()}
        })
        
        # 가장 오래된 기사와 최신 기사
        oldest_article = await collection.find_one({}, sort=[("published_at", 1)])
        newest_article = await collection.find_one({}, sort=[("published_at", -1)])
        
        return {
            "status": "success",
            "stats": {
                "total_articles": total_articles,
                "recent_articles_7days": recent_articles,
                "sentiment_distribution": sentiment_counts,
                "oldest_article_date": oldest_article["published_at"] if oldest_article else None,
                "newest_article_date": newest_article["published_at"] if newest_article else None
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/kwater")
async def get_kwater_news(max_results: int = 50):
    """
    K-water 관련 뉴스만 검색합니다.
    """
    try:
        articles = await news_collector.fetch_news("kwater OR 한국수자원공사", max_results)
        return {
            "status": "success",
            "count": len(articles),
            "articles": articles
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/with-sentiment")
async def get_news_with_sentiment(query: str = "kwater OR 한국수자원공사", max_results: int = 50):
    """
    뉴스를 검색하고 각 기사에 대해 감정분석을 수행합니다.
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        articles = await news_collector.fetch_news(query, max_results)
        
        articles_with_sentiment = []
        for article in articles:
            text_for_analysis = f"{article['title']} {article['content']}"
            sentiment = sentiment_analyzer.analyze(text_for_analysis)
            
            article_with_sentiment = {
                **article,
                "sentiment": sentiment
            }
            articles_with_sentiment.append(article_with_sentiment)
        
        return {
            "status": "success",
            "count": len(articles_with_sentiment),
            "articles": articles_with_sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/news/kwater/with-sentiment")
async def get_kwater_news_with_sentiment(max_results: int = 30):
    """
    K-water 관련 뉴스를 검색하고 각 기사에 대해 감정분석을 수행합니다.
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        articles = await news_collector.fetch_news("kwater OR 한국수자원공사", max_results)
        
        articles_with_sentiment = []
        for article in articles:
            text_for_analysis = f"{article['title']} {article['content']}"
            sentiment = sentiment_analyzer.analyze(text_for_analysis)
            
            article_with_sentiment = {
                **article,
                "sentiment": sentiment
            }
            articles_with_sentiment.append(article_with_sentiment)
        
        return {
            "status": "success",
            "count": len(articles_with_sentiment),
            "articles": articles_with_sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment/analyze")
async def analyze_sentiment(sentiment_request: SentimentRequest):
    """
    텍스트의 감정을 분석합니다.
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        sentiment = sentiment_analyzer.analyze(sentiment_request.text)
        return {
            "status": "success",
            "text": sentiment_request.text,
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment/analyze-batch")
async def analyze_sentiment_batch(sentiment_batch_request: SentimentBatchRequest):
    """
    여러 텍스트의 감정을 일괄 분석합니다.
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        results = sentiment_analyzer.analyze_batch(sentiment_batch_request.texts)
        return {
            "status": "success",
            "results": [
                {"text": text, "sentiment": sentiment}
                for text, sentiment in zip(sentiment_batch_request.texts, results)
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sentiment/status")
async def get_sentiment_status():
    """
    감정분석 모델의 상태를 확인합니다.
    """
    return {
        "available": sentiment_available,
        "model_name": sentiment_analyzer.model_name if sentiment_available else None
    }

@app.get("/health")
async def health_check():
    """
    서버 상태를 확인합니다.
    """
    try:
        # MongoDB 연결 테스트
        collection = await get_async_collection()
        await collection.find_one()
        
        return {
            "status": "healthy",
            "database": "MongoDB",
            "sentiment_available": sentiment_available,
            "message": "News Collector API (MongoDB) is running successfully!"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "MongoDB",
            "error": str(e),
            "message": "MongoDB 연결에 문제가 있습니다."
        }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
