# 한국어 감정분석 모델 가이드

## 🎯 개요

한국어 감정분석에 특화된 다양한 모델들을 제공합니다. 각 모델은 한국어 텍스트의 감정을 Positive(긍정), Neutral(중립), Negative(부정)으로 분류합니다.

## 📊 사용 가능한 모델들

### 1. 🏆 KcELECTRA-base-v2022 (권장)
- **모델명**: `beomi/KcELECTRA-base-v2022`
- **특징**: 
  - 최신 한국어 ELECTRA 모델
  - 감정분석에 특화된 성능
  - 빠른 처리 속도
  - 높은 정확도
- **임계값**: 0.4 (민감한 분류)
- **용도**: 실시간 감정분석, 뉴스 분석

### 2. 🥈 KLUE RoBERTa
- **모델명**: `klue/roberta-base`
- **특징**:
  - KLUE 데이터셋으로 학습된 RoBERTa
  - 한국어 성능 우수
  - 안정적인 분류
- **임계값**: 0.6 (엄격한 분류)
- **용도**: 정확도가 중요한 분석

### 3. 🥉 KcELECTRA-base
- **모델명**: `beomi/KcELECTRA-base`
- **특징**:
  - ELECTRA 기반 한국어 모델
  - 이전 버전이지만 안정적
- **임계값**: 0.4
- **용도**: 호환성이 중요한 경우

### 4. 🔄 KLUE BERT
- **모델명**: `klue/bert-base`
- **특징**:
  - 기존 BERT 모델
  - 안정적이고 검증됨
- **임계값**: 0.6
- **용도**: 기본 감정분석

## 🔧 모델 선택 가이드

### 성능 우선
```python
analyzer = SentimentAnalyzer("beomi/KcELECTRA-base-v2022")
```

### 안정성 우선
```python
analyzer = SentimentAnalyzer("klue/roberta-base")
```

### 호환성 우선
```python
analyzer = SentimentAnalyzer("klue/bert-base")
```

## 📈 성능 비교

| 모델 | 정확도 | 속도 | 메모리 | 특화도 |
|------|--------|------|--------|--------|
| KcELECTRA-v2022 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| KLUE RoBERTa | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| KcELECTRA-base | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| KLUE BERT | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🧪 테스트 방법

### 1. 모든 모델 테스트
```bash
python test_korean_sentiment.py
```

### 2. 특정 모델 테스트
```python
from sentiment_analyzer import SentimentAnalyzer

# 최신 모델 테스트
analyzer = SentimentAnalyzer("beomi/KcELECTRA-base-v2022")
result = analyzer.analyze("한국수자원공사가 환경 보호에 기여하는 기술을 개발했습니다.")
print(result)  # Positive
```

### 3. 배치 처리
```python
texts = [
    "긍정적인 뉴스입니다.",
    "부정적인 상황입니다.",
    "중립적인 정보입니다."
]

results = analyzer.analyze_batch(texts)
print(results)  # ['Positive', 'Negative', 'Neutral']
```

## 📊 한국어 감정분석 특징

### 1. 한국어 특화 처리
- **형태소 분석**: 한국어 문법 구조 고려
- **조사 처리**: 조사에 따른 감정 변화 반영
- **어미 처리**: 동사/형용사 어미에 따른 감정 분석

### 2. 뉴스 텍스트 최적화
- **객관적 표현**: 뉴스의 객관적 톤 고려
- **사실 중심**: 감정보다는 사실 전달에 중점
- **문맥 이해**: 전체 문맥을 통한 감정 파악

### 3. 도메인 특화
- **환경/수자원**: K-water 관련 뉴스에 특화
- **정책/행정**: 정부 정책 관련 뉴스 분석
- **기술/혁신**: 기술 개발 관련 뉴스 분석

## 🔍 감정 분류 기준

### Positive (긍정)
- 성공, 완료, 개선, 혁신, 긍정적 효과
- 예: "성공적으로 완료", "개선된 성능", "혁신적인 기술"

### Negative (부정)
- 문제, 피해, 우려, 부정적 영향
- 예: "심각한 문제", "피해 발생", "우려 표명"

### Neutral (중립)
- 사실 전달, 객관적 정보, 중립적 표현
- 예: "보고서 발표", "정책 발표", "현황 보고"

## ⚙️ 설정 옵션

### 임계값 조정
```python
# 더 민감하게 설정
analyzer.threshold = 0.3

# 더 엄격하게 설정
analyzer.threshold = 0.7
```

### 모델 정보 확인
```python
info = analyzer.get_model_info()
print(info)
# {
#     'model_name': 'beomi/KcELECTRA-base-v2022',
#     'labels': ['Negative', 'Neutral', 'Positive'],
#     'threshold': 0.4,
#     'max_length': 512
# }
```

## 🚀 성능 최적화

### 1. 배치 처리
```python
# 여러 텍스트를 한 번에 처리
texts = ["텍스트1", "텍스트2", "텍스트3"]
results = analyzer.analyze_batch(texts)
```

### 2. 캐싱 활용
```python
# 동일한 텍스트 재분석 시 캐싱 활용
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_analyze(text):
    return analyzer.analyze(text)
```

### 3. 비동기 처리
```python
import asyncio

async def async_analyze(text):
    # 비동기로 감정분석 수행
    return analyzer.analyze(text)
```

## 📝 사용 예시

### 뉴스 감정분석
```python
from sentiment_analyzer import SentimentAnalyzer

# 최신 한국어 모델 사용
analyzer = SentimentAnalyzer("beomi/KcELECTRA-base-v2022")

# 뉴스 제목 분석
news_titles = [
    "한국수자원공사, 친환경 기술 개발 성공",
    "수질 오염 문제로 주민 우려",
    "정부, 물 관리 정책 발표"
]

for title in news_titles:
    sentiment = analyzer.analyze(title)
    print(f"{sentiment}: {title}")
```

### 실시간 분석
```python
# 실시간 뉴스 피드 분석
def analyze_news_feed(news_items):
    results = []
    for item in news_items:
        sentiment = analyzer.analyze(item['title'] + " " + item['content'])
        results.append({
            'id': item['id'],
            'sentiment': sentiment,
            'confidence': analyzer.get_confidence()
        })
    return results
```

## 🔧 문제 해결

### 모델 로딩 실패
```python
# 폴백 모델 자동 사용
analyzer = SentimentAnalyzer("beomi/KcELECTRA-base-v2022")
# 실패 시 자동으로 klue/bert-base 사용
```

### 메모리 부족
```python
# 더 작은 모델 사용
analyzer = SentimentAnalyzer("klue/bert-base")
```

### 속도 개선
```python
# 배치 크기 조정
results = analyzer.analyze_batch(texts, batch_size=32)
```

## 📚 참고 자료

- [KcELECTRA GitHub](https://github.com/Beomi/KcELECTRA)
- [KLUE GitHub](https://github.com/KLUE-benchmark/KLUE)
- [Hugging Face 한국어 모델](https://huggingface.co/models?language=ko&sort=downloads)
