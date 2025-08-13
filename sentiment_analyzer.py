import logging
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self, model_name="snunlp/KR-FinBert-SC"):
        self.model_name = model_name
        logger.info(f"Loading Korean sentiment analysis model: {self.model_name}")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=3
            )
            
            # 모델별 라벨과 임계값 설정
            if "KR-FinBert-SC" in model_name:
                self.labels = ["negative", "neutral", "positive"]
                self.threshold = 0.1  # 금융 감정분석 모델용 낮은 임계값
            elif "KcELECTRA" in model_name:
                self.labels = ["Negative", "Neutral", "Positive"]
                self.threshold = 0.4
            else:
                self.labels = ["Negative", "Neutral", "Positive"]
                self.threshold = 0.6
                
            logger.info(f"Model loaded successfully! Threshold: {self.threshold}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            logger.info("Falling back to klue/bert-base")
            self.model_name = "klue/bert-base"
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name,
                num_labels=3
            )
            self.labels = ["Negative", "Neutral", "Positive"]
            self.threshold = 0.6

    def analyze(self, text: str) -> str:
        text = self._preprocess_text(text)
        logger.info(f"Analyzing text: {text[:100]}...")
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
            scores = predictions[0].numpy()
            logger.info(f"Sentiment scores: {dict(zip(self.labels, scores))}")
            result = self._classify_sentiment(scores)
            logger.info(f"Final sentiment: {result}")
            return result

    def _preprocess_text(self, text: str) -> str:
        text = " ".join(text.split())
        text = text.replace("&amp;", "&")
        text = text.replace("&lt;", "<")
        text = text.replace("&gt;", ">")
        return text

    def _classify_sentiment(self, scores: np.ndarray) -> str:
        sorted_indices = np.argsort(scores)[::-1]
        max_score = scores[sorted_indices[0]]
        second_score = scores[sorted_indices[1]]
        score_diff = max_score - second_score
        if score_diff < self.threshold:
            return "neutral" if "neutral" in self.labels else "Neutral"
        else:
            return self.labels[sorted_indices[0]]

    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "labels": self.labels,
            "threshold": self.threshold
        }

# 사용 가능한 한국어 감정분석 모델들
KOREAN_SENTIMENT_MODELS = {
    "kr_finbert": {
        "name": "snunlp/KR-FinBert-SC",
        "description": "한국어 금융 감정분석 모델 (감정분석 특화)",
        "labels": ["negative", "neutral", "positive"],
        "threshold": 0.1
    },
    "kc_electra": {
        "name": "beomi/KcELECTRA-base-v2022",
        "description": "한국어 ELECTRA 모델",
        "labels": ["Negative", "Neutral", "Positive"],
        "threshold": 0.4
    },
    "klue_roberta": {
        "name": "klue/roberta-base",
        "description": "KLUE RoBERTa 모델",
        "labels": ["Negative", "Neutral", "Positive"],
        "threshold": 0.6
    }
} 