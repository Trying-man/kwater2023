@echo off
echo 뉴스 수집 및 감정 분석 시스템 서버를 시작합니다...
echo.

REM 현재 디렉토리 확인
echo 현재 디렉토리: %CD%
echo.

REM Python 버전 확인
echo Python 버전 확인 중...
python --version
if %errorlevel% neq 0 (
    echo Python을 찾을 수 없습니다. py 명령어를 시도합니다...
    py --version
    if %errorlevel% neq 0 (
        echo Python이 설치되지 않았습니다.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo.
echo 서버를 시작합니다...
echo 서버 주소: http://localhost:8000
echo API 문서: http://localhost:8000/docs
echo.
echo 서버를 중지하려면 Ctrl+C를 누르세요.
echo.

REM 서버 실행
%PYTHON_CMD% main.py

pause 