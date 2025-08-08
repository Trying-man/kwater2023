#!/usr/bin/env python3
"""
감정분석 결과 확인 스크립트
"""

import requests
import json

def check_sentiment_results():
    """감정분석 결과를 확인합니다."""
    
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("뉴스 수집 및 감정 분석 시스템 - 감정분석 결과 확인")
    print("=" * 60)
    print()
    
    # 1. 감정분석 모델 상태 확인
    print("1. 감정분석 모델 상태 확인")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/sentiment/status", timeout=10)
        if response.status_code == 200:
            status = response.json()
            print(f"✓ 모델 사용 가능: {status.get('available', False)}")
            print(f"✓ 모델 이름: {status.get('model_name', 'N/A')}")
        else:
            print(f"✗ 상태 확인 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 오류: {e}")
    
    print()
    
    # 2. 감정분석 포함 뉴스 조회
    print("2. 감정분석 포함 뉴스 조회")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/news/kwater/with-sentiment", 
                              params={"max_results": 10}, timeout=60)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            print(f"✓ 조회된 기사 수: {len(articles)}")
            print()
            
            print("감정분석 결과:")
            print("-" * 40)
            for i, article in enumerate(articles, 1):
                title = article.get('title', 'No title')
                sentiment = article.get('sentiment', 'Unknown')
                content = article.get('content', '')[:100] + "..."
                
                # 감정에 따른 이모지 표시
                sentiment_emoji = {
                    'Positive': '😊',
                    'Neutral': '😐', 
                    'Negative': '😞'
                }.get(sentiment, '❓')
                
                print(f"{i}. {sentiment_emoji} {sentiment}")
                print(f"   제목: {title}")
                print(f"   내용: {content}")
                print()
        else:
            print(f"✗ 뉴스 조회 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 오류: {e}")
    
    print()
    
    # 3. 감정별 통계
    print("3. 감정별 통계")
    print("-" * 40)
    try:
        response = requests.get(f"{base_url}/news/kwater/with-sentiment", 
                              params={"max_results": 20}, timeout=60)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            
            sentiment_counts = {}
            for article in articles:
                sentiment = article.get('sentiment', 'Unknown')
                sentiment_counts[sentiment] = sentiment_counts.get(sentiment, 0) + 1
            
            total = len(articles)
            print(f"총 기사 수: {total}")
            print()
            
            for sentiment, count in sentiment_counts.items():
                percentage = (count / total) * 100 if total > 0 else 0
                emoji = {
                    'Positive': '😊',
                    'Neutral': '😐',
                    'Negative': '😞'
                }.get(sentiment, '❓')
                
                print(f"{emoji} {sentiment}: {count}개 ({percentage:.1f}%)")
        else:
            print(f"✗ 통계 생성 실패: {response.status_code}")
    except Exception as e:
        print(f"✗ 오류: {e}")
    
    print()
    print("=" * 60)
    print("감정분석 결과 확인 완료!")
    print("웹 브라우저에서 더 자세한 정보를 확인하세요:")
    print("- API 문서: http://localhost:8000/docs")
    print("- 감정분석 뉴스: http://localhost:8000/news/kwater/with-sentiment")
    print("=" * 60)

if __name__ == "__main__":
    check_sentiment_results()
