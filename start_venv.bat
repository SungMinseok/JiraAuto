@echo off
echo ==========================================
echo JIRA Auto Enhanced - 가상환경 활성화
echo ==========================================
echo.

REM 가상환경 활성화
call venv\Scripts\activate.bat

echo 가상환경이 활성화되었습니다.
echo.
echo 사용 가능한 명령어:
echo   python main_application.py  - 애플리케이션 실행
echo   ollama list                 - 설치된 AI 모델 확인
echo   ollama pull gemma2:2b       - AI 모델 다운로드
echo   pip list                    - 설치된 패키지 목록
echo.
echo Ollama 설치가 필요하면 OLLAMA_설치가이드.md 파일을 확인하세요!
echo ==========================================
echo.

REM 새 명령 프롬프트 유지
cmd /k

