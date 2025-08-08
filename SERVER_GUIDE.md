# 뉴스 수집 및 감정 분석 시스템 서버 실행 가이드

## 🚀 서버 실행 방법

### 1. 기본 실행 방법

#### Windows 명령 프롬프트
```cmd
python main.py
```

#### Windows PowerShell
```powershell
py main.py
```

### 2. 자동화 스크립트 사용

#### 배치 파일 실행 (Windows)
```cmd
start_server.bat
```

#### PowerShell 스크립트 실행
```powershell
.\start_server.ps1
```

#### Python 스크립트 실행
```cmd
python run_server.py
```

### 3. 서버 상태 확인

서버가 성공적으로 시작되면 다음 메시지가 표시됩니다:
```
감정분석 모델을 로딩 중입니다...
감정분석 모델 로딩 완료!
INFO:     Started server process [xxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

## 📋 서버 접속 정보

- **서버 주소**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs
- **ReDoc 문서**: http://localhost:8000/redoc

## 🧪 서버 테스트

서버가 정상적으로 작동하는지 테스트하려면:

```cmd
python test_server.py
```

이 스크립트는 다음 항목들을 테스트합니다:
1. 기본 엔드포인트 연결
2. 감정분석 모델 상태
3. 뉴스 조회 기능
4. 감정분석 포함 뉴스 조회

## 🔧 문제 해결

### 1. Python이 인식되지 않는 경우
```cmd
# Python 버전 확인
python --version
py --version

# PATH 환경변수 확인
echo %PATH%
```

### 2. 의존성 패키지 오류
```cmd
# 패키지 재설치
pip install -r requirements.txt

# 개별 패키지 설치
pip install fastapi uvicorn aiohttp python-dotenv transformers torch numpy
```

### 3. 포트 8000이 이미 사용 중인 경우
```cmd
# 포트 사용 확인
netstat -an | findstr :8000

# 다른 포트로 실행 (main.py 수정)
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### 4. 감정분석 모델 로딩 실패
- 메모리 부족: 최소 4GB RAM 필요
- 인터넷 연결 확인: 모델 다운로드 필요
- 디스크 공간 확인: 모델 파일 저장 공간 필요

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

## 🔒 보안 설정

### 환경 변수 설정 (.env 파일)
```env
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### CORS 설정
현재 모든 도메인에서 접근 가능하도록 설정되어 있습니다.
프로덕션 환경에서는 특정 도메인만 허용하도록 수정하세요.

## 📈 모니터링

### 로그 확인
서버 실행 시 다음 로그들이 표시됩니다:
- 감정분석 모델 로딩 상태
- API 요청/응답 로그
- 에러 메시지

### 성능 모니터링
- API 응답 시간: 평균 200ms 이내
- 감정분석 처리 시간: 1-2초/텍스트
- 메모리 사용량: 약 1GB (모델 로딩 후)

## 🛑 서버 중지

서버를 중지하려면:
1. 터미널에서 `Ctrl+C` 누르기
2. 또는 터미널 창 닫기

## 🔄 서버 재시작

서버를 재시작하려면:
1. 현재 서버 중지 (`Ctrl+C`)
2. 다시 실행 명령어 입력

## 📝 로그 파일

서버 실행 중 발생하는 로그는 터미널에 출력됩니다.
로그를 파일로 저장하려면:

```cmd
python main.py > server.log 2>&1
```

## 🆘 지원

문제가 발생하면 다음을 확인하세요:
1. Python 버전 (3.8 이상)
2. 필요한 패키지 설치 여부
3. 네트워크 연결 상태
4. 시스템 메모리 사용량
5. 포트 8000 사용 여부 