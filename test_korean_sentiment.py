#!/usr/bin/env python3
"""
한국어 감정분석 모델 테스트 스크립트
"""

from sentiment_analyzer import SentimentAnalyzer, KOREAN_SENTIMENT_MODELS
import time

def test_korean_sentiment_models():
    """한국어 감정분석 모델들을 테스트합니다."""
    
    # 테스트할 한국어 텍스트들
    test_texts = [
        "한국수자원공사가 새로운 댐 건설 프로젝트를 성공적으로 완료했습니다.",
        "수질 오염 문제로 인해 지역 주민들이 심각한 우려를 표명하고 있습니다.",
        "정부가 물 관리 정책을 개선하여 환경 보호에 기여할 예정입니다.",
        "홍수로 인한 피해가 발생하여 복구 작업이 진행 중입니다.",
        "청정 에너지 개발을 위한 투자가 확대되어 긍정적인 반응을 얻고 있습니다.",
        "기후 변화로 인한 가뭄이 심화되어 농작물 피해가 우려됩니다.",
        "물 절약 캠페인이 성공적으로 진행되어 시민들의 참여율이 높아졌습니다.",
        "하천 정화 사업이 완료되어 주변 환경이 크게 개선되었습니다.",
        "수돗물 품질 문제로 인해 주민들이 불안해하고 있습니다.",
        "친환경 물 관리 기술 개발로 해외에서도 주목받고 있습니다."
    ]
    
    print("=" * 80)
    print("한국어 감정분석 모델 테스트")
    print("=" * 80)
    print()
    
    # 각 모델별로 테스트
    for model_key, model_name in KOREAN_SENTIMENT_MODELS.items():
        print(f"🔍 테스트 중: {model_key}")
        print(f"   모델: {model_name}")
        print("-" * 60)
        
        try:
            # 모델 로딩 시간 측정
            start_time = time.time()
            analyzer = SentimentAnalyzer(model_name)
            load_time = time.time() - start_time
            
            print(f"   로딩 시간: {load_time:.2f}초")
            print(f"   임계값: {analyzer.threshold}")
            print()
            
            # 테스트 텍스트 분석
            results = []
            analysis_start = time.time()
            
            for i, text in enumerate(test_texts, 1):
                sentiment = analyzer.analyze(text)
                results.append(sentiment)
                print(f"   {i}. {sentiment}: {text[:50]}...")
            
            analysis_time = time.time() - analysis_start
            avg_time = analysis_time / len(test_texts)
            
            print()
            print(f"   분석 시간: {analysis_time:.2f}초 (평균 {avg_time:.2f}초/텍스트)")
            
            # 결과 통계
            sentiment_counts = {}
            for result in results:
                sentiment_counts[result] = sentiment_counts.get(result, 0) + 1
            
            print("   결과 분포:")
            for sentiment, count in sentiment_counts.items():
                percentage = (count / len(results)) * 100
                print(f"     {sentiment}: {count}개 ({percentage:.1f}%)")
            
            print()
            print("✅ 테스트 완료")
            print()
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            print()
    
    print("=" * 80)
    print("모든 모델 테스트 완료!")
    print("=" * 80)

def test_specific_model(model_name: str):
    """특정 모델을 상세히 테스트합니다."""
    
    print(f"🔍 상세 테스트: {model_name}")
    print("=" * 60)
    
    try:
        analyzer = SentimentAnalyzer(model_name)
        model_info = analyzer.get_model_info()
        
        print(f"모델 정보:")
        print(f"  - 이름: {model_info['model_name']}")
        print(f"  - 라벨: {model_info['labels']}")
        print(f"  - 임계값: {model_info['threshold']}")
        print(f"  - 최대 길이: {model_info['max_length']}")
        print()
        
        # 다양한 감정의 텍스트 테스트
        test_cases = [
            ("긍정적", "한국수자원공사가 환경 보호에 기여하는 혁신적인 기술을 개발했습니다."),
            ("부정적", "수질 오염으로 인해 주민들이 심각한 건강 문제를 겪고 있습니다."),
            ("중립적", "정부가 물 관리 정책에 대한 보고서를 발표했습니다."),
            ("복합적", "새로운 댐 건설은 경제적 이익을 가져오지만 환경 문제도 우려됩니다.")
        ]
        
        for emotion, text in test_cases:
            sentiment = analyzer.analyze(text)
            print(f"{emotion}: {sentiment}")
            print(f"  텍스트: {text}")
            print()
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("한국어 감정분석 모델 테스트를 시작합니다...")
    print()
    
    # 1. 모든 모델 테스트
    test_korean_sentiment_models()
    
    # 2. 최신 모델 상세 테스트
    print("\n" + "=" * 80)
    print("최신 한국어 ELECTRA 모델 상세 테스트")
    print("=" * 80)
    test_specific_model("beomi/KcELECTRA-base-v2022")
