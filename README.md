# News Sentiment Analysis System

네이버 News API를 이용한 뉴스 수집 및 감정분석 시스템입니다.

## 기능

- 네이버 News API를 통한 뉴스 수집
- "kwater" 및 "한국수자원공사" 키워드 기반 필터링
- KoBERT를 이용한 감정분석 (Positive/Neutral/Negative)
- RESTful API를 통한 데이터 조회

## 설치 방법

1. Python 3.8 이상 설치

2. 의존성 설치:
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정:
`.env` 파일을 생성하고 다음 내용을 추가:
```
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
DATABASE_URL=sqlite:///./news.db  # 또는 PostgreSQL URL
```

## 실행 방법

```bash
python main.py
```

서버가 http://localhost:8000 에서 실행됩니다.

## API 엔드포인트

- `GET /api/articles`: 저장된 기사 목록 조회
  - 쿼리 파라미터:
    - `sentiment`: 감정 분류 필터링 (Positive/Neutral/Negative)
    - `page`: 페이지 번호 (기본값: 1)
    - `size`: 페이지당 항목 수 (기본값: 10)

- `GET /api/articles/{id}`: 특정 기사 상세 조회

- `POST /api/trigger-fetch`: 뉴스 수집 및 감정분석 배치 실행

- `POST /api/trigger-sentiment`: 미분류 기사 대상 감정분석 실행

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc 