
# JiraAuto Enhanced (v2.0)

PyQt5 기반 GUI와 Selenium 자동화를 결합하여 JIRA 버그 리포트 생성을 단순화/자동화하는 도구입니다. v2.0에서 전체 구조를 모듈화하고 프리셋/옵션 관리, 어두운 테마 UI, 로컬 LLM(Ollama) 기반 AI 보조 생성 기능을 추가/강화했습니다.

## 주요 기능

- **직관적 GUI**: 요약, 담당/리뷰어, 브랜치/빌드/픽스버전/컴포넌트, 라벨, 우선순위/심각도/발생범위/재현율, Steps/Description 입력 지원
- **프리셋 관리(버전 포함)**: 카테고리(prefix) → 이름(name) → 버전(version) 3단계 구조로 저장/적용/삭제, 최신순/이름순 정렬
- **옵션 관리(+/-)**: `branch`, `build`, `fixversion`, `component` 필드에서 콤보 옵션을 추가/삭제하며 JSON 파일로 유지
- **자동 설명 생성**: 선택 옵션에 맞춘 템플릿으로 Description 자동 생성
- **AI 보조 생성(선택)**: 로컬 LLM을 통해 Priority/Severity/Steps/Description 자동 제안 (Ollama 필요)
- **JIRA 자동화**: Selenium을 통한 필드 입력 및 이슈 생성 플로우 자동화
- **다크 테마**: 일관된 어두운 테마 스타일
- **단축키**: F2 실행, F5 새로고침, F6 적용, F12 디버그

## 실행 환경

- Python 3.11 권장 (가상환경 포함됨)
- Windows 10/11
- Google Chrome 설치 필요

## 설치

1) 의존성 설치

```bash
pip install -r requirements.txt
```

2) (선택) AI 기능 사용 시 Ollama 설치 및 모델 다운로드

- 설치 가이드: `OLLAMA_설치가이드.md`
- 예: `ollama pull gemma2:2b`

## 실행 방법

- 직접 실행:

```bash
python main_application.py
```

- 배치 파일 실행: `run_app.bat`

## 사용 방법 요약

1) 상단 Preset 섹션에서 카테고리/이름/버전을 선택하여 적용(F6)하거나 새로 저장(💾)
2) Summary/세부 필드 입력, 필요 시 Generate(템플릿) 또는 🤖 AI 생성 사용
3) Execute(F2)로 JIRA 이슈 생성 진행

## 모듈 구조

- `main_application.py`: 메인 애플리케이션(QMainWindow)과 이벤트/스레드/설정 저장/로드
- `gui_widgets.py`: 폼 빌더, 프리셋 섹션, 콤보(+/-), 텍스트/액션 버튼, 메뉴바 구성
- `jira_automation.py`: ChromeDriver 연결/시작, JIRA 페이지 이동, 필드 자동 입력 및 이슈 생성
- `config.py`: 상수/스타일/필드 정의, 경로/크롬/타임아웃/AI 설정, 프리셋 디렉토리 보장
- `utils.py`: 파일/JSON/로깅, 텍스트 치환/템플릿, 프리셋 버전 관리, 옵션 추가/삭제
- `ai_assistant.py`: Ollama 연동, 요약 기반 JSON 결과 파싱/회복, 모델 확인/목록

## 크롬/환경 설정

- 사용자 데이터 디렉터리: `C:\\ChromeTEMP`
- 디버그 포트: `9222`
- 실행 파일 경로 자동 탐색(표준 경로 우선)

## JIRA 설정

- 기본 URL: `https://jira.krafton.com/secure/Dashboard.jspa`
- XPath 상수는 `config.JiraXPaths` 참고

## 문제 해결

- 크롬 연결 실패: 크롬 설치/경로 확인 → 디버그 포트 중복 점검 → `chromedriver-autoinstaller` 재설치
- 입력 필드 선택 실패: 드롭다운 재시도 로직 포함(키 입력/클릭/JS Click) — 로그 확인
- AI 생성 실패: Ollama 실행/모델 설치 확인(`ollama list`) 후 재시도

## 라이선스

MIT License

