"""
설정 상수 및 기본값들을 관리하는 모듈
"""
import os
from typing import Dict, List

# 디렉토리 경로
DIR_PRESET = 'preset'
DIR_CHROME_TEMP = r"C:\ChromeTEMP"
DIR_RESULT = 'result'

# Chrome 실행 파일 경로 (여러 경로 시도)
CHROME_POSSIBLE_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Users\{username}\AppData\Local\Google\Chrome\Application\chrome.exe'
]

def get_chrome_executable_path():
    """Chrome 실행 파일 경로를 찾아서 반환"""
    import os
    import getpass
    
    # 사용자명을 가져와서 경로에 적용
    username = getpass.getuser()
    paths_to_try = []
    
    for path in CHROME_POSSIBLE_PATHS:
        if '{username}' in path:
            path = path.format(username=username)
        paths_to_try.append(path)
    
    # 존재하는 첫 번째 경로 반환
    for path in paths_to_try:
        if os.path.exists(path):
            return path
    
    # 기본값 반환 (첫 번째 경로)
    return paths_to_try[0]

CHROME_EXECUTABLE_PATH = get_chrome_executable_path()

# Chrome 디버깅 설정
CHROME_DEBUG_PORT = 9222
CHROME_DEBUG_ADDRESS = f"http://127.0.0.1:{CHROME_DEBUG_PORT}/json"

# 파일 경로
BUILD_NAME_FILE = 'buildname.txt'
FIX_VERSION_FILE = 'fixversion.txt'
SETTINGS_FILE = f'{DIR_PRESET}/settings.json'
EXCEL_EXPORT_FILE = f'{DIR_RESULT}/bug_reports.xlsx'
APP_SETTINGS_FILE = f'{DIR_PRESET}/app_settings.json'

# JIRA 설정
JIRA_BASE_URL = "https://jira.krafton.com/secure/Dashboard.jspa"

# XPath 상수들
class JiraXPaths:
    """JIRA 웹페이지의 XPath들을 관리하는 클래스"""
    CREATE_BUTTON = '//*[@id="_r1_"]/span/div[2]/span/div/div/div[1]/button'
    CREATE_BUTTON_ALT = '/html/body/div[4]/div[2]/header/span/div[2]/span/div/button'
    
    TEAM_FIELD = '//*[@id="customfield_10937-container"]/div/div/div/div/div/div[1]/div[2]'
    SUMMARY_FIELD = '//*[@id="summary-field"]'
    ASSIGNEE_BUTTON = '//*[@id="assignee-container"]/div/div/div/div/button'
    REVIEWER_FIELD = '//*[@id="customfield_10629-field"]'
    
    LINKED_ISSUES = '//*[@id="issuelinks-container"]/div/div/div/div[1]/div/div/div[1]/div[2]'
    TARGET_LINKED_ISSUES = '//*[@id="issuelinks-container"]/div/div/div/div[2]/div/div/div/div[1]/div[2]'
    PARENT_ISSUE = '//*[@id="parent-container"]/div/div/div/div[1]/div/div[1]/div[2]'
    
    BRANCH_FIELD = '//*[@id="customfield_10623-field"]'
    BUILD_FIELD = '//*[@id="customfield_10627-field"]'
    FIX_VERSION_FIELD = '//*[@id="fixVersions-field"]'
    COMPONENTS_FIELD = '//*[@id="components-field"]'
    LABELS_FIELD = '//*[@id="labels-field"]'
    
    PRIORITY_FIELD = '//*[@id="priority-field"]'
    SEVERITY_FIELD = '//*[@id="customfield_10626-field"]'
    PREVALENCE_FIELD = '//*[@id="customfield_10628-field"]'
    REPRO_RATE_FIELD = '//*[@id="customfield_10634-field"]'
    
    STEPS_FIELD = '//*[@id="customfield_10399-field"]'
    DESCRIPTION_FIELD = '//*[@id="ak-editor-textarea"]'

# 드롭다운 옵션들
class DropdownOptions:
    """각 필드의 드롭다운 옵션들"""
    PRIORITY_OPTIONS = ["Blocker", "Critical", "High", "Medium", "Low"]
    SEVERITY_OPTIONS = ["1 - Critical", "2 - Major", "3 - Minor"]
    PREVALENCE_OPTIONS = [
        "1 - All users", 
        "2 - The majority of users", 
        "3 - Half Of users", 
        "4 - Almost no users", 
        "5 - Encountered by single user"
    ]
    REPRO_RATE_OPTIONS = [
        "1 - 100% reproducible", 
        "2 - Most times", 
        "3 - Approximately half the time", 
        "4 - Rare", 
        "5 - Seen Once"
    ]
    GENERATE_OPTIONS = ["기본값", "클라크래쉬", "서버크래쉬"]

# 필드명 목록
FIELD_NAMES = [
    "summary", "team", "linkedIssues", "issue", "parent", 
    "assignee", "reviewer", "label"
]

# 콤보박스로 변환할 필드들
COMBO_FIELD_NAMES = ["branch", "build", "fixversion", "component"]

# 옵션 파일들
OPTIONS_FILES = {
    'branch': 'branch_options.json',
    'build': 'build_options.json', 
    'fixversion': 'fixversion_options.json',
    'component': 'component_options.json'
}

# AI 설정
class AIConfig:
    """AI 어시스턴트 관련 설정"""
    # 기본 모델 (가벼운 모델)
    DEFAULT_MODEL = "gemma2:2b"
    
    # 추천 모델 목록
    RECOMMENDED_MODELS = [
        "gemma2:2b",       # 가벼운 모델 (~1.6GB, RAM ~4GB)
        "llama3.2:3b",     # 균형잡힌 모델 (~2GB, RAM ~6GB)
        "qwen2.5:3b",      # 다국어 지원 (~2GB, RAM ~6GB)
        "llama3.1:8b"      # 고성능 모델 (~4.7GB, RAM ~10GB)
    ]
    
    # AI 생성에 사용할 preset 예시 개수
    MAX_EXAMPLE_PRESETS = 5
    
    # AI 생성 타임아웃 (초)
    GENERATION_TIMEOUT = 60
    
    # AI 생성 기본 옵션
    TEMPERATURE = 0.7  # 창의성 조절 (0~1)
    TOP_P = 0.9
    TOP_K = 40

# 웹 대기 시간 (초)
class Timeouts:
    IMPLICIT_WAIT = 10
    SHORT_WAIT = 0.5
    MEDIUM_WAIT = 1.5
    CHROME_START_WAIT = 2
    DROPDOWN_RETRY = 3

# 스타일시트
DARK_THEME_STYLE = """
    QWidget {
        background-color: #1a1a1a;
        color: #ffffff;
        font-family: 'Malgun Gothic', sans-serif;
        font-size: 11pt;
        font-weight: bold;
    }

    QLineEdit {
        background-color: #333333;
        border: 1px solid #555555;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QTextEdit {
        background-color: #333333;
        border: 1px solid #555555;
        font-family: 'Malgun Gothic', sans-serif;
    }
    
    QPushButton {
        background-color: #444444;
        border: 1px solid #666666;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QPushButton:hover {
        background-color: #555555;
    }

    QPushButton:pressed {
        background-color: #666666;
    }

    QComboBox {
        background-color: #333333;
        border: 1px solid #555555;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QCheckBox {
        background-color: transparent;
        border: none;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QProgressDialog {
        background-color: #1a1a1a;
        color: #ffffff;
        border-radius: 10px;
        border: 1px solid #333333;
        font-family: 'Malgun Gothic', sans-serif;
    }

    QTimeEdit {
        background-color: #333333;
        border: 1px solid #555555;
        font-family: 'Malgun Gothic', sans-serif;
    }
"""

def ensure_directories():
    """필요한 디렉토리들이 존재하는지 확인하고 생성"""
    if not os.path.exists(DIR_PRESET):
        os.makedirs(DIR_PRESET)
    if not os.path.exists(DIR_RESULT):
        os.makedirs(DIR_RESULT)

# 텍스트 대체 규칙
TEXT_REPLACEMENT_RULES = [
    ('다른 현상', '동일해야 합니다.'),
    ('하지 않는 현상', '해야 합니다.'),
    ('되는 현상', '되지 않아야 합니다.'),
    ('하는 현상', '하지 않아야 합니다.'),
    ('되지 않는 현상', '되어야 합니다.'),
    ('되지 않은 현상', '되어야 합니다.'),
    ('없는 현상', '있어야 합니다.'),
    ('있는 현상', '있지 않아야 합니다.'),
    ('지는 현상', '지지 않아야 합니다.'),
    ('크래쉬 발생', '크래쉬가 발생하지 않아야 합니다.'),
    ('열리는 현상', '열리지 않아야 합니다.'),
    ('가능한 현상', '불가해야 합니다.'),
    ('진 현상', '지지않아야 합니다.'),
    ('일부', '모든'),
    ('가리는 현상', '가리지 않아야 합니다.'),
    ('불가한 현상', '가능해야 합니다.'),
    ('\n', '')  # 줄바꿈 제거
]
