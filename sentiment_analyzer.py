from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        # 한국어 감정분석에 특화된 모델 사용
        self.model_name = "klue/bert-base"
        logger.info(f"Loading model: {self.model_name}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, num_labels=3)
        self.labels = ["Negative", "Neutral", "Positive"]
        
        # 임계값 설정 - 더 엄격하게 설정
        self.threshold = 0.6  # 감정 점수가 이 값보다 높아야 해당 감정으로 분류

    def analyze(self, text: str) -> str:
        # 입력 텍스트 로깅
        logger.info(f"Analyzing text: {text[:100]}...")  # 처음 100자만 로깅
        
        # 토크나이징 및 모델 입력 준비
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        
        # 예측 수행
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            scores = predictions[0].numpy()
            
            # 점수 로깅
            logger.info(f"Sentiment scores: {dict(zip(self.labels, scores))}")
            
            # 가장 높은 점수와 두 번째로 높은 점수의 차이가 임계값보다 작으면 중립으로 분류
            sorted_scores = np.sort(scores)[::-1]
            if sorted_scores[0] - sorted_scores[1] < self.threshold:
                result = "Neutral"
            else:
                result = self.labels[np.argmax(scores)]
            
            logger.info(f"Final sentiment: {result}")
            return result

    def analyze_batch(self, texts: list) -> list:
        results = []
        for text in texts:
            result = self.analyze(text)
            results.append(result)
        return results 