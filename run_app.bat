@echo off
echo ==========================================
echo JIRA Auto Enhanced - 애플리케이션 시작
echo ==========================================
echo.

REM 가상환경이 있는지 확인
if not exist "venv\Scripts\activate.bat" (
    echo [오류] 가상환경을 찾을 수 없습니다.
    echo.
    echo 먼저 다음 명령으로 가상환경을 생성하세요:
    echo   python -m venv venv
    echo   venv\Scripts\pip.exe install -r requirements.txt
    echo.
    pause
    exit /b 1
)

REM 가상환경 활성화
call venv\Scripts\activate.bat

echo 애플리케이션을 시작합니다...
echo.

REM Python 애플리케이션 실행
python main_application.py

REM 애플리케이션 종료 후
echo.
echo 애플리케이션이 종료되었습니다.
pause

