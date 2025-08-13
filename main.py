from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from news_collector import NewsCollector
from sentiment_analyzer import SentimentAnalyzer
from typing import List, Dict, Any
import uvicorn

app = FastAPI(title="News Collector API", description="네이버 뉴스 수집 API")

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# NewsCollector 인스턴스 생성
news_collector = NewsCollector()

# SentimentAnalyzer 인스턴스 생성
sentiment_analyzer = None
sentiment_available = False

try:
    print("감정분석 모델을 로딩 중입니다...")
    sentiment_analyzer = SentimentAnalyzer("snunlp/KR-FinBert-SC")
    sentiment_available = True
    print("감정분석 모델 로딩 완료!")
except Exception as e:
    print(f"감정분석 모델 로딩 실패: {e}")
    print("폴백 모델로 시도합니다...")
    try:
        sentiment_analyzer = SentimentAnalyzer("klue/bert-base")
        sentiment_available = True
        print("폴백 모델 로딩 완료!")
    except Exception as e2:
        print(f"폴백 모델도 실패: {e2}")
        print("감정분석 기능 없이 서버를 시작합니다.")
        sentiment_analyzer = None
        sentiment_available = False

@app.get("/")
async def root():
    return {"message": "News Collector API is running!"}

@app.get("/news")
async def get_news(query: str = "kwater OR 한국수자원공사", max_results: int = 100):
    """
    뉴스를 검색하고 반환합니다.
    
    Args:
        query: 검색할 키워드 (기본값: "kwater OR 한국수자원공사")
        max_results: 최대 결과 개수 (기본값: 100)
    
    Returns:
        뉴스 기사 목록
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

@app.get("/news/kwater")
async def get_kwater_news(max_results: int = 50):
    """
    K-water 관련 뉴스만 검색합니다.
    
    Args:
        max_results: 최대 결과 개수 (기본값: 50)
    
    Returns:
        K-water 관련 뉴스 기사 목록
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
    
    Args:
        query: 검색할 키워드 (기본값: "kwater OR 한국수자원공사")
        max_results: 최대 결과 개수 (기본값: 50)
    
    Returns:
        뉴스 기사 목록 (감정분석 결과 포함)
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        # 뉴스 수집
        articles = await news_collector.fetch_news(query, max_results)
        
        # 각 기사에 대해 감정분석 수행
        articles_with_sentiment = []
        for article in articles:
            # 제목과 내용을 합쳐서 감정분석
            text_for_analysis = f"{article['title']} {article['content']}"
            sentiment = sentiment_analyzer.analyze(text_for_analysis)
            
            # 감정분석 결과를 기사에 추가
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
    
    Args:
        max_results: 최대 결과 개수 (기본값: 30)
    
    Returns:
        K-water 관련 뉴스 기사 목록 (감정분석 결과 포함)
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        # K-water 뉴스 수집
        articles = await news_collector.fetch_news("kwater OR 한국수자원공사", max_results)
        
        # 각 기사에 대해 감정분석 수행
        articles_with_sentiment = []
        for article in articles:
            # 제목과 내용을 합쳐서 감정분석
            text_for_analysis = f"{article['title']} {article['content']}"
            sentiment = sentiment_analyzer.analyze(text_for_analysis)
            
            # 감정분석 결과를 기사에 추가
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
async def analyze_sentiment(text: str):
    """
    텍스트의 감정을 분석합니다.
    
    Args:
        text: 분석할 텍스트
    
    Returns:
        감정 분석 결과
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        sentiment = sentiment_analyzer.analyze(text)
        return {
            "status": "success",
            "text": text,
            "sentiment": sentiment
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sentiment/analyze-batch")
async def analyze_sentiment_batch(texts: List[str]):
    """
    여러 텍스트의 감정을 일괄 분석합니다.
    
    Args:
        texts: 분석할 텍스트 리스트
    
    Returns:
        감정 분석 결과 리스트
    """
    if not sentiment_available:
        raise HTTPException(status_code=503, detail="감정분석 모델이 로딩되지 않았습니다.")
    
    try:
        results = sentiment_analyzer.analyze_batch(texts)
        return {
            "status": "success",
            "results": [
                {"text": text, "sentiment": sentiment}
                for text, sentiment in zip(texts, results)
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 