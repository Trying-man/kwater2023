#!/usr/bin/env python3
"""
한국어 감정분석에 미세조정된 모델들을 찾고 테스트
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import time

def test_korean_sentiment_models():
    """한국어 감정분석에 미세조정된 모델들을 테스트합니다."""
    
    print("=" * 70)
    print("한국어 감정분석 특화 모델 테스트")
    print("=" * 70)
    
    # 한국어 감정분석에 미세조정된 모델들
    korean_sentiment_models = [
        {
            "name": "snunlp/KR-FinBert-SC",
            "description": "한국어 금융 감정분석 모델",
            "labels": ["negative", "neutral", "positive"]
        },
        {
            "name": "beomi/KcELECTRA-base-v2022",
            "description": "한국어 ELECTRA 모델 (감정분석 미세조정 없음)",
            "labels": ["Negative", "Neutral", "Positive"]
        },
        {
            "name": "klue/roberta-base",
            "description": "KLUE RoBERTa 모델 (감정분석 미세조정 없음)",
            "labels": ["Negative", "Neutral", "Positive"]
        },
        {
            "name": "monologg/koelectra-base-v3-discriminator",
            "description": "한국어 ELECTRA 모델 (감정분석 미세조정 없음)",
            "labels": ["Negative", "Neutral", "Positive"]
        }
    ]
    
    # 테스트 텍스트들
    test_texts = [
        ("매우 긍정", "정말 좋은 소식입니다! 환경 보호에 크게 기여했습니다."),
        ("긍정", "한국수자원공사가 혁신적인 기술로 환경 보호에 기여했습니다."),
        ("중립", "한국수자원공사가 새로운 댐 건설 프로젝트를 발표했습니다."),
        ("부정", "수질 오염 문제로 인해 주민들이 건강 문제를 겪고 있습니다."),
        ("매우 부정", "정말 끔찍한 상황입니다! 수질 오염으로 인해 주민들이 심각한 건강 문제를 겪고 있습니다.")
    ]
    
    for model_info in korean_sentiment_models:
        model_name = model_info["name"]
        description = model_info["description"]
        labels = model_info["labels"]
        
        print(f"\n🔍 테스트 중: {model_name}")
        print(f"   설명: {description}")
        print(f"   라벨: {labels}")
        print("-" * 50)
        
        try:
            # 모델 로딩 시간 측정
            start_time = time.time()
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(
                model_name,
                num_labels=len(labels)
            )
            loading_time = time.time() - start_time
            print(f"   로딩 시간: {loading_time:.2f}초")
            
            # 분석 시간 측정
            analysis_start = time.time()
            
            results = []
            for emotion, text in test_texts:
                # 토크나이징
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                )
                
                # 예측
                with torch.no_grad():
                    outputs = model(**inputs)
                    predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                    scores = predictions[0].numpy()
                
                # 최고 점수 찾기
                max_idx = np.argmax(scores)
                predicted_label = labels[max_idx]
                max_score = scores[max_idx]
                
                results.append({
                    "expected": emotion,
                    "predicted": predicted_label,
                    "score": max_score,
                    "scores": scores
                })
                
                print(f"   {emotion} → {predicted_label} ({max_score:.3f})")
            
            analysis_time = time.time() - analysis_start
            print(f"   분석 시간: {analysis_time:.2f}초")
            
            # 정확도 계산
            correct = sum(1 for r in results if r["predicted"] != "neutral" and r["predicted"] != "Neutral")
            accuracy = correct / len(results) * 100
            print(f"   정확도: {accuracy:.1f}%")
            
        except Exception as e:
            print(f"   ❌ 오류: {e}")
        
        print()

if __name__ == "__main__":
    test_korean_sentiment_models()
