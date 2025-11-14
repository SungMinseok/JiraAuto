@echo off
chcp 65001 > nul
echo ================================
echo JIRA 자동화 도구 실행
echo ================================
echo.

REM 가상환경 활성화
echo [1/2] 가상환경 활성화 중...
call venv\Scripts\activate.bat

REM Python 스크립트 실행
echo [2/2] 애플리케이션 실행 중...
echo.
python main_application.py

REM 에러 발생 시 대기
if errorlevel 1 (
    echo.
    echo ================================
    echo 오류가 발생했습니다!
    echo ================================
    pause
)






