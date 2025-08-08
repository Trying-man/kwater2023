# GitHub 저장소 수동 설정 가이드

## 🚀 단계별 GitHub 저장소 설정

### 1단계: GitHub에서 새 저장소 생성

1. **GitHub.com 접속**
   - 브라우저에서 https://github.com 접속
   - GitHub 계정으로 로그인

2. **새 저장소 생성**
   - 우측 상단의 **"+"** 버튼 클릭
   - **"New repository"** 선택

3. **저장소 정보 입력**
   - **Repository name**: `soocrap` (또는 원하는 이름)
   - **Description**: `뉴스 수집 및 감정 분석 시스템`
   - **Visibility**: `Public` (또는 `Private`)
   - **Initialize this repository with**: 체크하지 않음
   - **"Create repository"** 클릭

### 2단계: 로컬 저장소와 GitHub 연결

GitHub에서 저장소를 생성한 후, 터미널에서 다음 명령어를 실행하세요:

```bash
# 원격 저장소 추가 (YOUR_USERNAME을 실제 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/soocrap.git

# 메인 브랜치를 main으로 변경
git branch -M main

# GitHub에 푸시
git push -u origin main
```

### 3단계: 인증 설정

GitHub에 푸시할 때 인증이 필요할 수 있습니다:

#### 방법 1: Personal Access Token 사용 (권장)
1. GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. **"Generate new token"** 클릭
3. **"Generate new token (classic)"** 선택
4. 권한 설정:
   - `repo` (전체 저장소 접근)
   - `workflow` (선택사항)
5. **"Generate token"** 클릭
6. 생성된 토큰을 복사하여 안전한 곳에 보관
7. 푸시 시 사용자명과 토큰을 입력

#### 방법 2: GitHub CLI 사용
```bash
# GitHub CLI 설치 (Windows)
winget install GitHub.cli

# 또는 Chocolatey 사용
choco install gh

# GitHub CLI 로그인
gh auth login
```

### 4단계: 푸시 확인

성공적으로 푸시되면 다음 메시지가 표시됩니다:
```
Enumerating objects: 18, done.
Counting objects: 100% (18/18), done.
Delta compression using up to 8 threads
Compressing objects: 100% (16/16), done.
Writing objects: 100% (18/18), done.
Total 18 (delta 0), reused 0 (delta 0), pack-reused 18
To https://github.com/YOUR_USERNAME/soocrap.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

## 📋 프로젝트 정보

### 저장소 URL
```
https://github.com/YOUR_USERNAME/soocrap
```

### 주요 파일
- `main.py` - FastAPI 서버 메인 파일
- `news_collector.py` - 뉴스 수집 모듈
- `sentiment_analyzer.py` - 감정분석 모듈
- `README.md` - 프로젝트 설명서
- `기능명세서.md` - 상세 기능 명세서
- `SERVER_GUIDE.md` - 서버 실행 가이드

### 기술 스택
- **Backend**: FastAPI (Python)
- **AI Model**: KoBERT (KLUE/bert-base)
- **External API**: 네이버 News API
- **Database**: PostgreSQL (설정 가능)

## 🔧 추가 설정

### 1. GitHub Pages 설정 (선택사항)
1. 저장소 Settings → Pages
2. Source: Deploy from a branch
3. Branch: main
4. Save

### 2. GitHub Actions 설정 (선택사항)
`.github/workflows/ci.yml` 파일 생성:
```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python test_server.py
```

### 3. Issues 및 Projects 설정
1. **Issues**: 버그 리포트나 기능 요청
2. **Projects**: 프로젝트 관리
3. **Wiki**: 문서화
4. **Security**: 보안 취약점 보고

## 📊 저장소 통계

GitHub에서 다음 정보를 확인할 수 있습니다:
- **Stars**: 프로젝트 인기도
- **Forks**: 포크된 저장소 수
- **Issues**: 열린 이슈 수
- **Pull Requests**: 열린 PR 수
- **Contributors**: 기여자 수

## 🎯 다음 단계

1. **README.md 확인**: 프로젝트 설명서가 올바르게 표시되는지 확인
2. **Issues 생성**: 향후 개선사항이나 버그를 이슈로 등록
3. **Wiki 작성**: 상세한 문서화
4. **Actions 설정**: 자동화된 테스트 및 배포 설정
5. **Security 설정**: 보안 취약점 스캔 설정

## 🆘 문제 해결

### 푸시 실패 시
```bash
# 원격 저장소 확인
git remote -v

# 원격 저장소 제거 후 재추가
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/soocrap.git

# 강제 푸시 (주의: 기존 내용 덮어씀)
git push -u origin main --force
```

### 인증 오류 시
1. Personal Access Token 재생성
2. GitHub CLI 재로그인
3. SSH 키 설정 (선택사항)

### 브랜치 충돌 시
```bash
# 원격 브랜치 정보 가져오기
git fetch origin

# 로컬 브랜치를 원격과 동기화
git reset --hard origin/main
```

## 📞 지원

문제가 발생하면:
1. GitHub Help: https://help.github.com
2. Git Documentation: https://git-scm.com/doc
3. 프로젝트 Issues에 등록
