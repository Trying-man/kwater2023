# News Collector API

네이버 API를 활용한 뉴스 수집 및 감정분석 시스템입니다.

## 주요 기능

### 1. 뉴스 수집 및 저장
- 네이버 뉴스 API를 통한 실시간 뉴스 수집
- PostgreSQL 데이터베이스에 자동 저장
- **중복 기사 방지** (URL 기반 unique constraint)
- 감정분석 결과와 함께 저장

### 2. 스케줄링
- **매일 오전 9시 자동 뉴스 수집**
- APScheduler를 활용한 백그라운드 스케줄링
- 서버 시작/종료 시 자동 스케줄러 관리

### 3. 감정분석
- 한국어 감정분석 모델 활용
- Positive, Neutral, Negative 분류
- 실시간 및 배치 처리 지원

### 4. API 엔드포인트
- 뉴스 검색 및 조회
- DB 저장된 뉴스 조회
- 통계 정보 제공
- 스케줄러 상태 확인

## 설치 및 설정

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경변수 설정
`.env` 파일을 생성하고 다음 정보를 설정하세요:

```env
# 네이버 API 설정
NAVER_CLIENT_ID=your_naver_client_id
NAVER_CLIENT_SECRET=your_naver_client_secret

# 데이터베이스 설정
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### 3. 데이터베이스 초기화
```bash
python init_db.py
```

## 사용법

### 1. 서버 실행
```bash
python main.py
```

### 2. 독립 스케줄러 실행 (선택사항)
```bash
python scheduler.py
```

### 3. 테스트 실행
```bash
python test_news_collection.py
```

## API 엔드포인트

### 뉴스 수집 및 저장
- `POST /news/collect-and-save` - 뉴스 수집 및 DB 저장
- `GET /news/db` - DB에서 저장된 뉴스 조회
- `GET /news/db/stats` - 뉴스 통계 정보

### 스케줄러 관리
- `GET /scheduler/status` - 스케줄러 상태 확인
- `POST /scheduler/trigger` - 즉시 뉴스 수집 실행

### 기존 기능
- `GET /news` - 뉴스 검색
- `GET /news/with-sentiment` - 감정분석과 함께 뉴스 검색
- `POST /sentiment/analyze` - 텍스트 감정분석

## 데이터베이스 스키마

### articles 테이블
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url VARCHAR(500) UNIQUE NOT NULL,
    published_at TIMESTAMP NOT NULL,
    sentiment VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## 중복 방지 기능

- **URL 기반 중복 체크**: 동일한 URL의 기사는 자동으로 건너뜀
- **데이터베이스 제약조건**: URL 컬럼에 unique constraint 적용
- **실시간 중복 검사**: 저장 전 URL 중복 여부 확인

## 스케줄링 설정

- **실행 시간**: 매일 오전 9시
- **수집 키워드**: "kwater OR 한국수자원공사"
- **최대 수집 개수**: 100개
- **자동 감정분석**: 수집된 모든 기사에 대해 감정분석 수행

## 모니터링

### 로그 확인
- 뉴스 수집 과정이 상세한 로그로 기록됩니다
- 중복 건너뛴 기사, 저장된 기사, 오류 발생 기사 수를 확인할 수 있습니다

### 통계 확인
```bash
curl http://localhost:8000/news/db/stats
```

### 스케줄러 상태 확인
```bash
curl http://localhost:8000/scheduler/status
```

## 문제 해결

### 1. 데이터베이스 연결 오류
- PostgreSQL 서버가 실행 중인지 확인
- DATABASE_URL 설정이 올바른지 확인
- 데이터베이스가 생성되어 있는지 확인

### 2. 네이버 API 오류
- NAVER_CLIENT_ID와 NAVER_CLIENT_SECRET이 올바른지 확인
- 네이버 개발자 센터에서 API 사용량 제한 확인

### 3. 스케줄러가 작동하지 않는 경우
- 서버 로그에서 스케줄러 시작 메시지 확인
- `/scheduler/status` 엔드포인트로 상태 확인
- 수동으로 `/scheduler/trigger` 실행하여 테스트

## 개발 정보

- **Python**: 3.8+
- **FastAPI**: 0.95.2
- **PostgreSQL**: 12+
- **APScheduler**: 3.10.1
- **SQLAlchemy**: 1.4.41 