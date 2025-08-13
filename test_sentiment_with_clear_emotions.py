#!/usr/bin/env python3
"""
명확한 감정이 있는 텍스트로 감정분석 테스트
"""

from sentiment_analyzer import SentimentAnalyzer
import time

def test_sentiment_with_clear_emotions():
    """명확한 감정이 있는 텍스트들로 감정분석을 테스트합니다."""
    
    print("=" * 60)
    print("명확한 감정이 있는 텍스트 감정분석 테스트")
    print("=" * 60)
    
    # 감정분석 모델 로딩
    analyzer = SentimentAnalyzer("snunlp/KR-FinBert-SC")
    
    # 명확한 감정이 있는 테스트 텍스트들
    test_cases = [
        # 긍정적인 뉴스
        ("매우 긍정", "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다. 이는 정말 놀라운 성과입니다!"),
        ("긍정", "한국수자원공사가 새로운 친환경 기술을 개발하여 환경 보호에 기여했습니다."),
        ("약간 긍정", "한국수자원공사가 지역 주민들과 협력하여 물 관리 시스템을 개선했습니다."),
        
        # 중립적인 뉴스
        ("중립", "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."),
        ("중립", "한국수자원공사가 내년도 예산 계획을 발표했습니다."),
        ("중립", "한국수자원공사가 새로운 사업 계획을 발표했습니다."),
        
        # 부정적인 뉴스
        ("약간 부정", "수질 오염 문제로 인해 지역 주민들이 우려를 표명하고 있습니다."),
        ("부정", "수질 오염 문제로 인해 주민들이 건강 문제를 겪고 있습니다."),
        ("매우 부정", "심각한 수질 오염으로 인해 주민들이 생명의 위협을 받고 있습니다. 이는 정말 끔찍한 상황입니다!"),
        
        # 실제 뉴스와 유사한 텍스트들
        ("실제 긍정", "한국수자원공사가 혁신적인 물 정화 기술을 개발하여 해외에서도 높은 평가를 받고 있습니다."),
        ("실제 중립", "한국수자원공사가 새로운 연구개발 과제를 공모합니다."),
        ("실제 부정", "수돗물 품질 문제로 인해 주민들이 불안해하고 있습니다."),
    ]
    
    print("🔍 감정분석 테스트:")
    print("-" * 50)
    
    results = []
    for emotion, text in test_cases:
        print(f"📝 {emotion}: {text}")
        
        # 감정분석 수행
        start_analysis = time.time()
        sentiment = analyzer.analyze(text)
        analysis_time = time.time() - start_analysis
        
        results.append({
            "expected": emotion,
            "predicted": sentiment,
            "time": analysis_time
        })
        
        print(f"   결과: {sentiment} (소요시간: {analysis_time:.3f}초)")
        print()
    
    # 결과 요약
    print("📊 테스트 결과 요약:")
    print("-" * 30)
    
    # 감정별 분류
    positive_count = 0
    neutral_count = 0
    negative_count = 0
    
    for result in results:
        expected = result["expected"]
        predicted = result["predicted"]
        
        if predicted == "positive":
            positive_count += 1
        elif predicted == "neutral":
            neutral_count += 1
        elif predicted == "negative":
            negative_count += 1
        
        print(f"   {expected} → {predicted}")
    
    print(f"\n📈 감정별 분포:")
    print(f"   Positive: {positive_count}개")
    print(f"   Neutral: {neutral_count}개")
    print(f"   Negative: {negative_count}개")
    
    # 정확도 계산 (예상 감정과 실제 감정 비교)
    correct = 0
    for result in results:
        expected = result["expected"]
        predicted = result["predicted"]
        
        # 예상 감정과 실제 감정이 일치하는지 확인
        if ("긍정" in expected and predicted == "positive") or \
           ("중립" in expected and predicted == "neutral") or \
           ("부정" in expected and predicted == "negative"):
            correct += 1
    
    accuracy = correct / len(results) * 100
    print(f"\n✅ 정확도: {accuracy:.1f}% ({correct}/{len(results)})")
    
    # 실제 뉴스 데이터로 테스트
    print("\n🔍 실제 뉴스 데이터 테스트:")
    print("-" * 50)
    
    # 더 다양한 뉴스 텍스트들
    news_texts = [
        "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다.",
        "수질 오염 문제로 인해 지역 주민들이 심각한 건강 문제를 겪고 있습니다.",
        "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다.",
        "한국수자원공사가 해외에서 높은 평가를 받고 있습니다.",
        "수돗물 품질 문제로 인해 주민들이 불안해하고 있습니다.",
        "한국수자원공사가 지역 경제 활성화에 기여하고 있습니다."
    ]
    
    for i, text in enumerate(news_texts, 1):
        sentiment = analyzer.analyze(text)
        print(f"   뉴스 {i}: {sentiment} - {text[:50]}...")

if __name__ == "__main__":
    test_sentiment_with_clear_emotions()
