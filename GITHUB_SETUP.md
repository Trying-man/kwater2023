# GitHub 저장소 설정 가이드

## 🚀 GitHub에 프로젝트 업로드하기

### 1. GitHub에서 새 저장소 생성

1. **GitHub.com 접속**: https://github.com
2. **로그인** 후 우측 상단의 **"+"** 버튼 클릭
3. **"New repository"** 선택
4. **저장소 정보 입력**:
   - Repository name: `news-sentiment-analysis`
   - Description: `뉴스 수집 및 감정 분석 시스템`
   - Public/Private 선택
   - **"Create repository"** 클릭

### 2. 로컬 저장소와 GitHub 연결

GitHub에서 저장소를 생성한 후, 다음 명령어를 실행하세요:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/news-sentiment-analysis.git

# 메인 브랜치를 main으로 변경 (최신 GitHub 표준)
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3. 자동화 스크립트 사용

또는 다음 스크립트를 실행하여 자동으로 설정할 수 있습니다:

```bash
python setup_github.py
```

## 📋 프로젝트 정보

### 프로젝트 이름
**뉴스 수집 및 감정 분석 시스템**

### 주요 기능
- 네이버 News API를 통한 뉴스 수집
- KoBERT를 이용한 감정분석 (Positive/Neutral/Negative)
- RESTful API를 통한 데이터 조회
- "kwater" 및 "한국수자원공사" 키워드 기반 필터링

### 기술 스택
- **Backend**: FastAPI (Python)
- **AI Model**: KoBERT (KLUE/bert-base)
- **External API**: 네이버 News API
- **Database**: PostgreSQL (설정 가능)

## 📁 프로젝트 구조

```
news-sentiment-analysis/
├── main.py                 # FastAPI 서버 메인 파일
├── news_collector.py       # 뉴스 수집 모듈
├── sentiment_analyzer.py   # 감정분석 모듈
├── database.py            # 데이터베이스 설정
├── models.py              # 데이터 모델
├── requirements.txt       # Python 의존성
├── README.md             # 프로젝트 설명서
├── 기능명세서.md          # 상세 기능 명세서
├── SERVER_GUIDE.md       # 서버 실행 가이드
├── check_sentiment.py    # 감정분석 결과 확인 스크립트
├── test_server.py        # 서버 테스트 스크립트
├── run_server.py         # 서버 실행 스크립트
├── start_server.bat      # Windows 배치 파일
├── start_server.ps1      # PowerShell 스크립트
└── .gitignore           # Git 제외 파일 설정
```

## 🔧 설치 및 실행

### 1. 의존성 설치
```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정
`.env` 파일 생성:
```env
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 3. 서버 실행
```bash
python main.py
```

### 4. 서버 접속
- **서버 주소**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 📊 API 엔드포인트

### 기본 엔드포인트
- `GET /` - 서버 상태 확인
- `GET /news` - 뉴스 조회
- `GET /news/kwater` - K-water 뉴스 조회

### 감정분석 엔드포인트
- `GET /news/with-sentiment` - 감정분석 포함 뉴스 조회
- `GET /news/kwater/with-sentiment` - K-water 뉴스 감정분석
- `POST /sentiment/analyze` - 단일 텍스트 감정분석
- `GET /sentiment/status` - 감정분석 모델 상태

## 🧪 테스트

### 서버 테스트
```bash
python test_server.py
```

### 감정분석 결과 확인
```bash
python check_sentiment.py
```

## 📈 성능 지표

- **뉴스 수집**: 최대 100건/요청
- **감정 분석**: 약 1-2초/텍스트
- **API 응답**: 평균 200ms 이내
- **메모리 사용량**: 약 1GB (모델 로딩 후)

## 🔒 보안

- API 키는 환경변수로 관리
- CORS 설정 (개발환경: 모든 도메인 허용)
- SQL Injection 방지 (SQLAlchemy ORM)

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.8 이상)
2. 필요한 패키지 설치 여부
3. 네트워크 연결 상태
4. 시스템 메모리 사용량
5. 포트 8000 사용 여부
