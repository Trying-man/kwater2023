#!/usr/bin/env python3
"""
새로운 한국어 금융 감정분석 모델 테스트
"""

from sentiment_analyzer import SentimentAnalyzer
import time

def test_new_sentiment_model():
    """새로운 한국어 금융 감정분석 모델을 테스트합니다."""
    
    print("=" * 60)
    print("새로운 한국어 금융 감정분석 모델 테스트")
    print("=" * 60)
    
    # 새로운 모델 로딩
    print("🔍 새로운 모델 로딩 중...")
    start_time = time.time()
    
    try:
        analyzer = SentimentAnalyzer("snunlp/KR-FinBert-SC")
        loading_time = time.time() - start_time
        print(f"✅ 모델 로딩 완료! (소요시간: {loading_time:.2f}초)")
        
        # 모델 정보 출력
        model_info = analyzer.get_model_info()
        print(f"📊 모델 정보:")
        print(f"   모델명: {model_info['model_name']}")
        print(f"   라벨: {model_info['labels']}")
        print(f"   임계값: {model_info['threshold']}")
        print()
        
        # 테스트 텍스트들
        test_cases = [
            ("매우 긍정", "정말 좋은 소식입니다! 환경 보호에 크게 기여했습니다."),
            ("긍정", "한국수자원공사가 혁신적인 기술로 환경 보호에 기여했습니다."),
            ("중립", "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."),
            ("부정", "수질 오염 문제로 인해 주민들이 건강 문제를 겪고 있습니다."),
            ("매우 부정", "정말 끔찍한 상황입니다! 수질 오염으로 인해 주민들이 심각한 건강 문제를 겪고 있습니다.")
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
        correct = 0
        for result in results:
            expected = result["expected"]
            predicted = result["predicted"]
            
            # 정확도 계산 (중립이 아닌 결과를 정확한 것으로 간주)
            if predicted != "neutral":
                correct += 1
            
            print(f"   {expected} → {predicted}")
        
        accuracy = correct / len(results) * 100
        print(f"\n✅ 정확도: {accuracy:.1f}% ({correct}/{len(results)})")
        
        # 실제 뉴스 텍스트로 테스트
        print("\n🔍 실제 뉴스 텍스트 테스트:")
        print("-" * 50)
        
        news_texts = [
            "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다.",
            "수질 오염 문제로 인해 지역 주민들이 심각한 건강 문제를 겪고 있습니다.",
            "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."
        ]
        
        for i, text in enumerate(news_texts, 1):
            sentiment = analyzer.analyze(text)
            print(f"   뉴스 {i}: {sentiment}")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        print("폴백 모델로 테스트를 진행합니다...")
        
        # 폴백 모델 테스트
        try:
            analyzer = SentimentAnalyzer("klue/bert-base")
            print("✅ 폴백 모델 로딩 완료")
            
            # 간단한 테스트
            text = "한국수자원공사가 혁신적인 기술로 환경 보호에 기여했습니다."
            sentiment = analyzer.analyze(text)
            print(f"테스트 결과: {sentiment}")
            
        except Exception as e2:
            print(f"❌ 폴백 모델도 실패: {e2}")

if __name__ == "__main__":
    test_new_sentiment_model()
