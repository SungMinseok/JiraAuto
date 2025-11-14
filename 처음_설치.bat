@echo off
chcp 65001 > nul
echo ================================
echo JIRA 자동화 도구 - 처음 설치
echo ================================
echo.

REM 1. 가상환경 생성
echo [1/4] 가상환경 생성 중...
if not exist venv (
    python -m venv venv
    if errorlevel 1 (
        echo 가상환경 생성 실패!
        pause
        exit /b 1
    )
    echo 가상환경 생성 완료!
) else (
    echo 가상환경이 이미 존재합니다.
)
echo.

REM 2. 가상환경 활성화 및 pip 업그레이드
echo [2/4] pip 업그레이드 중...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
echo.

REM 3. 패키지 설치
echo [3/4] 필요한 패키지 설치 중...
pip install -r requirements.txt
if errorlevel 1 (
    echo 패키지 설치 실패!
    pause
    exit /b 1
)
echo 패키지 설치 완료!
echo.

REM 4. Ollama 확인
echo [4/4] Ollama 설치 확인 중...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ================================
    echo 경고: Ollama가 설치되지 않았습니다!
    echo ================================
    echo.
    echo AI 기능을 사용하려면 Ollama를 설치해야 합니다.
    echo.
    echo 1. https://ollama.com/download 에서 Ollama 다운로드
    echo 2. 설치 후 터미널에서 다음 명령어 실행:
    echo    ollama pull gemma2:2b
    echo.
    echo 자세한 내용은 'OLLAMA_설치가이드.md' 파일을 참고하세요.
    echo.
) else (
    echo Ollama가 설치되어 있습니다!
    echo.
    echo 모델 다운로드를 위해 다음 명령어를 실행하세요:
    echo ollama pull gemma2:2b
    echo.
)

echo ================================
echo 설치 완료!
echo ================================
echo.
echo '실행.bat' 파일을 실행하여 프로그램을 시작하세요.
echo.
pause






