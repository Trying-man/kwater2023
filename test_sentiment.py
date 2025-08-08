from sentiment_analyzer import SentimentAnalyzer

def test_sentiment_analysis():
    print("감정분석 테스트를 시작합니다...")
    
    # 감정분석기 초기화
    print("모델을 로딩 중입니다...")
    analyzer = SentimentAnalyzer()
    print("모델 로딩 완료!")
    
    # 테스트 텍스트들
    test_texts = [
        "오늘 날씨가 정말 좋네요! 기분이 상쾌합니다.",
        "이 뉴스는 정말 실망스럽고 안타깝습니다.",
        "보통의 일상적인 소식입니다.",
        "K-water의 새로운 프로젝트가 성공적으로 완료되었습니다.",
        "환경 오염 문제가 심각해지고 있습니다."
    ]
    
    print("\n=== 단일 텍스트 감정분석 ===")
    for i, text in enumerate(test_texts, 1):
        print(f"\n{i}. 텍스트: {text}")
        sentiment = analyzer.analyze(text)
        print(f"   감정: {sentiment}")
    
    print("\n=== 일괄 감정분석 ===")
    results = analyzer.analyze_batch(test_texts)
    for i, (text, sentiment) in enumerate(zip(test_texts, results), 1):
        print(f"{i}. {sentiment}: {text[:30]}...")

if __name__ == "__main__":
    test_sentiment_analysis() 