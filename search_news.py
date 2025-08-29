import requests
import json
from datetime import datetime

def search_news(keyword="", limit=10, sentiment=None, days=None):
    """뉴스 검색 기능"""
    try:
        # 검색 파라미터 구성
        params = {
            "keyword": keyword,
            "limit": limit
        }
        
        if sentiment:
            params["sentiment"] = sentiment
        
        if days:
            params["days"] = days
        
        # API 호출
        response = requests.get("http://localhost:8000/news/search", params=params)
        data = response.json()
        
        if data["status"] != "success":
            print("❌ 검색 실패")
            return
        
        articles = data["articles"]
        total_count = data["total_count"]
        
        print(f"🔍 검색 결과: '{keyword}'")
        print(f"📊 총 {total_count}개 기사 중 {len(articles)}개 표시")
        print("=" * 80)
        
        if not articles:
            print("검색 결과가 없습니다.")
            return
        
        # 검색 결과 표시
        for i, article in enumerate(articles, 1):
            title = article.get("title", "제목 없음")
            content = article.get("content", "내용 없음")
            sentiment = article.get("sentiment", {})
            published_at = article.get("published_at", "")
            
            # 감정 분석 결과
            if isinstance(sentiment, dict):
                sentiment_type = sentiment.get("sentiment", "unknown")
                confidence = sentiment.get("confidence", 0)
            else:
                sentiment_type = sentiment
                confidence = 0
            
            # 감정 이모지
            if sentiment_type == "positive":
                emoji = "😊"
            elif sentiment_type == "negative":
                emoji = "😞"
            else:
                emoji = "😐"
            
            print(f"{i:2d}. {emoji} {title}")
            print(f"    📅 {published_at}")
            print(f"    💭 감정: {sentiment_type} (신뢰도: {confidence:.2f})")
            print(f"    📝 내용: {content[:100]}...")
            print(f"    🔗 URL: {article.get('url', 'N/A')}")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def advanced_search(title_keyword="", content_keyword="", sentiment=None, limit=10):
    """고급 검색 기능"""
    try:
        # 검색 파라미터 구성
        params = {
            "title_keyword": title_keyword,
            "content_keyword": content_keyword,
            "limit": limit
        }
        
        if sentiment:
            params["sentiment"] = sentiment
        
        # API 호출
        response = requests.get("http://localhost:8000/news/search/advanced", params=params)
        data = response.json()
        
        if data["status"] != "success":
            print("❌ 고급 검색 실패")
            return
        
        articles = data["articles"]
        total_count = data["total_count"]
        
        print(f"🔍 고급 검색 결과")
        print(f"   제목 키워드: '{title_keyword}'")
        print(f"   내용 키워드: '{content_keyword}'")
        print(f"📊 총 {total_count}개 기사 중 {len(articles)}개 표시")
        print("=" * 80)
        
        if not articles:
            print("검색 결과가 없습니다.")
            return
        
        # 검색 결과 표시
        for i, article in enumerate(articles, 1):
            title = article.get("title", "제목 없음")
            content = article.get("content", "내용 없음")
            sentiment = article.get("sentiment", {})
            published_at = article.get("published_at", "")
            
            # 감정 분석 결과
            if isinstance(sentiment, dict):
                sentiment_type = sentiment.get("sentiment", "unknown")
                confidence = sentiment.get("confidence", 0)
            else:
                sentiment_type = sentiment
                confidence = 0
            
            # 감정 이모지
            if sentiment_type == "positive":
                emoji = "😊"
            elif sentiment_type == "negative":
                emoji = "😞"
            else:
                emoji = "😐"
            
            print(f"{i:2d}. {emoji} {title}")
            print(f"    📅 {published_at}")
            print(f"    💭 감정: {sentiment_type} (신뢰도: {confidence:.2f})")
            print(f"    📝 내용: {content[:100]}...")
            print(f"    🔗 URL: {article.get('url', 'N/A')}")
            print("-" * 80)
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def show_search_help():
    """검색 도움말 표시"""
    print("🔍 뉴스 검색 도움말")
    print("=" * 50)
    print("1. 기본 검색: search_news('키워드')")
    print("2. 감정별 검색: search_news('키워드', sentiment='positive')")
    print("3. 최근 기사: search_news('키워드', days=7)")
    print("4. 고급 검색: advanced_search(title_keyword='제목', content_keyword='내용')")
    print()
    print("감정 옵션: positive, negative, neutral")
    print("예시:")
    print("  search_news('수자원공사')")
    print("  search_news('댐', sentiment='positive')")
    print("  search_news('물관리', days=30)")
    print("  advanced_search(title_keyword='공모전', content_keyword='수자원')")

if __name__ == "__main__":
    print("🔍 뉴스 검색 시스템")
    print("=" * 50)
    
    # 기본 검색 예시
    print("\n1️⃣ 기본 검색 예시:")
    search_news("수자원공사", limit=3)
    
    print("\n2️⃣ 긍정적 기사 검색 예시:")
    search_news("공모전", sentiment="positive", limit=3)
    
    print("\n3️⃣ 고급 검색 예시:")
    advanced_search(title_keyword="공사", content_keyword="물", limit=3)
    
    print("\n" + "=" * 50)
    show_search_help()
