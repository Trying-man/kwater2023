import requests
import json
from datetime import datetime

def view_sentiment_results():
    """감정분석 결과를 가독성 있게 출력"""
    try:
        # API 호출
        response = requests.get("http://localhost:8000/news/kwater/with-sentiment")
        data = response.json()
        
        if data["status"] != "success":
            print("❌ API 호출 실패")
            return
        
        articles = data["articles"]
        print(f"📊 감정분석 결과 (총 {len(articles)}개 기사)")
        print("=" * 60)
        
        # 감정별 분류
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        for article in articles:
            sentiment = article.get("sentiment", {})
            if isinstance(sentiment, dict):
                sentiment_type = sentiment.get("sentiment", "unknown")
            else:
                sentiment_type = sentiment
            
            if sentiment_type == "positive":
                positive_count += 1
            elif sentiment_type == "negative":
                negative_count += 1
            else:
                neutral_count += 1
        
        # 감정별 통계
        print(f"😊 긍정적: {positive_count}개 ({positive_count/len(articles)*100:.1f}%)")
        print(f"😐 중립적: {neutral_count}개 ({neutral_count/len(articles)*100:.1f}%)")
        print(f"😞 부정적: {negative_count}개 ({negative_count/len(articles)*100:.1f}%)")
        print("=" * 60)
        
        # 상위 10개 기사 표시
        print("📰 최근 기사 10개:")
        print("-" * 60)
        
        for i, article in enumerate(articles[:10], 1):
            title = article.get("title", "제목 없음")
            sentiment = article.get("sentiment", {})
            
            if isinstance(sentiment, dict):
                sentiment_type = sentiment.get("sentiment", "unknown")
                confidence = sentiment.get("confidence", 0)
                positive_score = sentiment.get("positive_score", 0)
                negative_score = sentiment.get("negative_score", 0)
                neutral_score = sentiment.get("neutral_score", 0)
            else:
                sentiment_type = sentiment
                confidence = 0
                positive_score = 0
                negative_score = 0
                neutral_score = 0
            
            # 감정 이모지
            if sentiment_type == "positive":
                emoji = "😊"
            elif sentiment_type == "negative":
                emoji = "😞"
            else:
                emoji = "😐"
            
            print(f"{i:2d}. {emoji} {title}")
            print(f"    감정: {sentiment_type} (신뢰도: {confidence:.2f})")
            print(f"    점수: 긍정({positive_score:.2f}) 중립({neutral_score:.2f}) 부정({negative_score:.2f})")
            print()
        
        # 감정별 상위 기사
        print("🏆 감정별 대표 기사:")
        print("-" * 60)
        
        # 긍정적 기사
        positive_articles = [a for a in articles if isinstance(a.get("sentiment"), dict) and a["sentiment"].get("sentiment") == "positive"]
        if positive_articles:
            best_positive = max(positive_articles, key=lambda x: x["sentiment"].get("confidence", 0))
            print(f"😊 최고 긍정 기사 (신뢰도: {best_positive['sentiment']['confidence']:.2f})")
            print(f"   {best_positive['title']}")
            print()
        
        # 부정적 기사
        negative_articles = [a for a in articles if isinstance(a.get("sentiment"), dict) and a["sentiment"].get("sentiment") == "negative"]
        if negative_articles:
            best_negative = max(negative_articles, key=lambda x: x["sentiment"].get("confidence", 0))
            print(f"😞 최고 부정 기사 (신뢰도: {best_negative['sentiment']['confidence']:.2f})")
            print(f"   {best_negative['title']}")
            print()
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    view_sentiment_results()
