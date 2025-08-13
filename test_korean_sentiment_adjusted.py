#!/usr/bin/env python3
"""
임계값 조정된 한국어 감정분석 모델 테스트 스크립트
"""

from sentiment_analyzer import SentimentAnalyzer, KOREAN_SENTIMENT_MODELS
import time

def test_adjusted_thresholds():
    """임계값을 조정하여 한국어 감정분석 모델들을 테스트합니다."""
    
    # 테스트할 한국어 텍스트들 (더 명확한 감정 표현)
    test_texts = [
        # 긍정적 텍스트들
        "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다.",
        "청정 에너지 개발로 인해 지역 경제가 활성화되어 주민들이 만족하고 있습니다.",
        "물 절약 캠페인이 성공적으로 진행되어 시민들의 참여율이 크게 높아졌습니다.",
        "하천 정화 사업이 완료되어 주변 환경이 크게 개선되어 주민들이 기뻐하고 있습니다.",
        "친환경 물 관리 기술 개발로 해외에서도 높은 평가를 받고 있습니다.",
        
        # 부정적 텍스트들
        "수질 오염 문제로 인해 지역 주민들이 심각한 건강 문제를 겪고 있습니다.",
        "홍수로 인한 피해가 발생하여 주민들이 큰 어려움을 겪고 있습니다.",
        "수돗물 품질 문제로 인해 주민들이 불안해하고 있습니다.",
        "기후 변화로 인한 가뭄이 심화되어 농작물 피해가 심각합니다.",
        "환경 오염으로 인해 생태계가 파괴되어 우려가 커지고 있습니다."
    ]
    
    # 조정된 임계값 설정 (더 낮게)
    adjusted_thresholds = {
        "kc_electra": 0.05,       # KcELECTRA 모델들: 매우 민감하게
        "klue_roberta": 0.08,     # KLUE RoBERTa: 민감하게
        "kc_electra_old": 0.05,   # KcELECTRA-base: 매우 민감하게
        "klue_bert": 0.1,         # KLUE BERT: 민감하게
        "korean_bert": 0.1        # Korean BERT: 민감하게
    }
    
    print("=" * 80)
    print("임계값 조정된 한국어 감정분석 모델 테스트")
    print("=" * 80)
    print()
    
    # 각 모델별로 테스트
    for model_key, model_name in KOREAN_SENTIMENT_MODELS.items():
        print(f"🔍 테스트 중: {model_key}")
        print(f"   모델: {model_name}")
        print(f"   조정된 임계값: {adjusted_thresholds.get(model_key, 0.3)}")
        print("-" * 60)
        
        try:
            # 모델 로딩 시간 측정
            start_time = time.time()
            analyzer = SentimentAnalyzer(model_name)
            
            # 임계값 조정
            if model_key in adjusted_thresholds:
                analyzer.threshold = adjusted_thresholds[model_key]
                print(f"   원래 임계값: {analyzer.threshold}")
                analyzer.threshold = adjusted_thresholds[model_key]
                print(f"   조정된 임계값: {analyzer.threshold}")
            
            load_time = time.time() - start_time
            
            print(f"   로딩 시간: {load_time:.2f}초")
            print()
            
            # 테스트 텍스트 분석
            results = []
            analysis_start = time.time()
            
            for i, text in enumerate(test_texts, 1):
                sentiment = analyzer.analyze(text)
                results.append(sentiment)
                emotion_type = "긍정" if i <= 5 else "부정"
                print(f"   {i}. {sentiment} ({emotion_type}): {text[:50]}...")
            
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
            
            # 정확도 계산 (예상 감정과 비교)
            correct_predictions = 0
            for i, result in enumerate(results):
                expected = "Positive" if i < 5 else "Negative"
                if result == expected:
                    correct_predictions += 1
            
            accuracy = (correct_predictions / len(results)) * 100
            print(f"   예상 정확도: {accuracy:.1f}%")
            
            print()
            print("✅ 테스트 완료")
            print()
            
        except Exception as e:
            print(f"❌ 오류 발생: {e}")
            print()

def test_specific_model_with_adjusted_threshold():
    """특정 모델을 조정된 임계값으로 상세히 테스트합니다."""
    
    model_name = "beomi/KcELECTRA-base-v2022"
    print(f"🔍 상세 테스트: {model_name} (조정된 임계값)")
    print("=" * 60)
    
    try:
        analyzer = SentimentAnalyzer(model_name)
        original_threshold = analyzer.threshold
        analyzer.threshold = 0.2  # 더 민감하게 조정
        
        print(f"원래 임계값: {original_threshold}")
        print(f"조정된 임계값: {analyzer.threshold}")
        print()
        
        # 다양한 감정의 텍스트 테스트
        test_cases = [
            ("강한 긍정", "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다."),
            ("약한 긍정", "정부가 물 관리 정책을 개선하여 환경 보호에 기여할 예정입니다."),
            ("중립", "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."),
            ("약한 부정", "수질 오염 문제로 인해 지역 주민들이 우려를 표명하고 있습니다."),
            ("강한 부정", "수질 오염으로 인해 주민들이 심각한 건강 문제를 겪고 있습니다.")
        ]
        
        for emotion, text in test_cases:
            sentiment = analyzer.analyze(text)
            print(f"{emotion}: {sentiment}")
            print(f"  텍스트: {text}")
            print()
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    print("임계값 조정된 한국어 감정분석 모델 테스트를 시작합니다...")
    print()
    
    # 1. 모든 모델 테스트 (조정된 임계값)
    test_adjusted_thresholds()
    
    # 2. 최신 모델 상세 테스트 (조정된 임계값)
    print("\n" + "=" * 80)
    print("조정된 임계값으로 최신 한국어 ELECTRA 모델 상세 테스트")
    print("=" * 80)
    test_specific_model_with_adjusted_threshold()
