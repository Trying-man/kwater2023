#!/usr/bin/env python3
"""
간단한 감정분석 테스트 - 점수와 분류 과정 확인
"""

from sentiment_analyzer import SentimentAnalyzer
import numpy as np

def test_simple_sentiment():
    """간단한 감정분석 테스트"""
    
    print("=" * 60)
    print("간단한 감정분석 테스트")
    print("=" * 60)
    
    # 모델 로딩
    analyzer = SentimentAnalyzer("beomi/KcELECTRA-base-v2022")
    analyzer.threshold = 0.05  # 매우 민감하게 설정
    
    print(f"모델: {analyzer.model_name}")
    print(f"임계값: {analyzer.threshold}")
    print(f"라벨: {analyzer.labels}")
    print()
    
    # 테스트 텍스트들
    test_cases = [
        ("강한 긍정", "한국수자원공사가 혁신적인 기술로 환경 보호에 크게 기여했습니다."),
        ("약한 긍정", "정부가 물 관리 정책을 개선하여 환경 보호에 기여할 예정입니다."),
        ("중립", "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."),
        ("약한 부정", "수질 오염 문제로 인해 지역 주민들이 우려를 표명하고 있습니다."),
        ("강한 부정", "수질 오염으로 인해 주민들이 심각한 건강 문제를 겪고 있습니다.")
    ]
    
    for emotion, text in test_cases:
        print(f"🔍 {emotion}: {text}")
        
        # 텍스트 전처리
        processed_text = analyzer._preprocess_text(text)
        print(f"   전처리: {processed_text[:50]}...")
        
        # 토크나이징
        inputs = analyzer.tokenizer(processed_text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        # 예측
        import torch
        with torch.no_grad():
            outputs = analyzer.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            scores = predictions[0].numpy()
        
        # 점수 출력
        print("   점수:")
        for label, score in zip(analyzer.labels, scores):
            print(f"     {label}: {score:.4f} ({score*100:.1f}%)")
        
        # 분류 과정
        sorted_indices = np.argsort(scores)[::-1]
        max_score = scores[sorted_indices[0]]
        second_score = scores[sorted_indices[1]]
        score_diff = max_score - second_score
        
        print(f"   최고 점수: {analyzer.labels[sorted_indices[0]]} ({max_score:.4f})")
        print(f"   두 번째 점수: {analyzer.labels[sorted_indices[1]]} ({second_score:.4f})")
        print(f"   점수 차이: {score_diff:.4f}")
        print(f"   임계값: {analyzer.threshold}")
        
        # 최종 분류
        if score_diff < analyzer.threshold:
            result = "Neutral"
        else:
            result = analyzer.labels[sorted_indices[0]]
        
        print(f"   최종 분류: {result}")
        print()

if __name__ == "__main__":
    test_simple_sentiment()
