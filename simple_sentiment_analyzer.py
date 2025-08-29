import re
from typing import Dict, List, Any

class SimpleSentimentAnalyzer:
    def __init__(self):
        self.model_name = "Simple Rule-based Sentiment Analyzer"
        
        # 긍정 키워드
        self.positive_keywords = [
            '좋다', '훌륭하다', '우수하다', '성공', '발전', '증가', '향상', '개선',
            '긍정적', '낙관적', '희망', '기대', '만족', '감사', '축하', '환영',
            '도움', '지원', '협력', '성장', '혁신', '창의', '효율', '효과',
            '안정', '신뢰', '투명', '공정', '책임', '지속가능', '친환경'
        ]
        
        # 부정 키워드
        self.negative_keywords = [
            '나쁘다', '문제', '실패', '실망', '우려', '걱정', '불안', '분노',
            '부정적', '비관적', '절망', '실패', '손실', '감소', '악화', '퇴보',
            '부패', '비리', '사기', '폭력', '사고', '재난', '위험', '위협',
            '불만', '항의', '반발', '갈등', '대립', '분쟁', '혼란', '혼돈'
        ]
        
        # 중립 키워드
        self.neutral_keywords = [
            '발표', '공지', '보고', '검토', '분석', '연구', '조사', '평가',
            '계획', '정책', '제도', '시스템', '프로그램', '프로젝트', '사업',
            '회의', '협의', '토론', '논의', '검토', '심의', '의결', '결정'
        ]

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        텍스트의 감정을 분석합니다.
        
        Args:
            text: 분석할 텍스트
            
        Returns:
            감정 분석 결과
        """
        if not text or not isinstance(text, str):
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "positive_score": 0.0,
                "negative_score": 0.0,
                "neutral_score": 0.0
            }
        
        # 텍스트 정규화
        text = text.lower()
        
        # 키워드 카운트
        positive_count = sum(1 for keyword in self.positive_keywords if keyword in text)
        negative_count = sum(1 for keyword in self.negative_keywords if keyword in text)
        neutral_count = sum(1 for keyword in self.neutral_keywords if keyword in text)
        
        # 총 키워드 수
        total_keywords = positive_count + negative_count + neutral_count
        
        if total_keywords == 0:
            return {
                "sentiment": "neutral",
                "confidence": 0.0,
                "positive_score": 0.0,
                "negative_score": 0.0,
                "neutral_score": 0.0
            }
        
        # 점수 계산
        positive_score = positive_count / total_keywords
        negative_score = negative_count / total_keywords
        neutral_score = neutral_count / total_keywords
        
        # 감정 결정
        if positive_score > negative_score and positive_score > neutral_score:
            sentiment = "positive"
            confidence = positive_score
        elif negative_score > positive_score and negative_score > neutral_score:
            sentiment = "negative"
            confidence = negative_score
        else:
            sentiment = "neutral"
            confidence = neutral_score
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 3),
            "positive_score": round(positive_score, 3),
            "negative_score": round(negative_score, 3),
            "neutral_score": round(neutral_score, 3)
        }

    def analyze_batch(self, texts: List[str]) -> List[Dict[str, Any]]:
        """
        여러 텍스트의 감정을 일괄 분석합니다.
        
        Args:
            texts: 분석할 텍스트 리스트
            
        Returns:
            감정 분석 결과 리스트
        """
        return [self.analyze(text) for text in texts]

    def get_sentiment_label(self, sentiment_result: Dict[str, Any]) -> str:
        """
        감정 분석 결과를 라벨로 변환합니다.
        
        Args:
            sentiment_result: 감정 분석 결과
            
        Returns:
            감정 라벨
        """
        sentiment = sentiment_result.get("sentiment", "neutral")
        confidence = sentiment_result.get("confidence", 0.0)
        
        if confidence < 0.3:
            return "neutral"
        
        if sentiment == "positive":
            return "긍정"
        elif sentiment == "negative":
            return "부정"
        else:
            return "중립" 