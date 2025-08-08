# 뉴스 수집 및 감정 분석 시스템 서버 실행 스크립트

Write-Host "뉴스 수집 및 감정 분석 시스템 서버를 시작합니다..." -ForegroundColor Green
Write-Host ""

# 현재 디렉토리 확인
Write-Host "현재 디렉토리: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Python 버전 확인
Write-Host "Python 버전 확인 중..." -ForegroundColor Yellow
$pythonCmd = $null

try {
    $result = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        $pythonCmd = "python"
        Write-Host "Python 발견: $result" -ForegroundColor Green
    }
} catch {
    Write-Host "python 명령어를 찾을 수 없습니다." -ForegroundColor Yellow
}

if (-not $pythonCmd) {
    try {
        $result = py --version 2>&1
        if ($LASTEXITCODE -eq 0) {
            $pythonCmd = "py"
            Write-Host "Python 발견: $result" -ForegroundColor Green
        }
    } catch {
        Write-Host "py 명령어를 찾을 수 없습니다." -ForegroundColor Yellow
    }
}

if (-not $pythonCmd) {
    Write-Host "Python이 설치되지 않았습니다." -ForegroundColor Red
    Read-Host "계속하려면 아무 키나 누르세요"
    exit 1
}

Write-Host ""
Write-Host "서버를 시작합니다..." -ForegroundColor Green
Write-Host "서버 주소: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API 문서: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "서버를 중지하려면 Ctrl+C를 누르세요." -ForegroundColor Yellow
Write-Host ""

# 서버 실행
try {
    & $pythonCmd main.py
} catch {
    Write-Host "서버 실행 중 오류가 발생했습니다: $_" -ForegroundColor Red
    Read-Host "계속하려면 아무 키나 누르세요"
} 