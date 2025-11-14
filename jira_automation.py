"""
JIRA 자동화를 위한 Selenium 기반 클래스 모듈
"""
import os
import time
import logging
import subprocess
from typing import Optional, List
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

from config import (
    CHROME_DEBUG_ADDRESS, CHROME_EXECUTABLE_PATH, DIR_CHROME_TEMP, 
    CHROME_DEBUG_PORT, JIRA_BASE_URL, JiraXPaths, Timeouts
)

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ChromeDriverManager:
    """Chrome 드라이버 관리 클래스"""
    
    @staticmethod
    def install_chromedriver() -> str:
        """ChromeDriver를 설치하고 경로를 반환"""
        try:
            path = chromedriver_autoinstaller.install(True)
            if not path or not os.path.exists(path):
                raise FileNotFoundError("ChromeDriver installation failed or not found.")
            logger.info(f"✅ ChromeDriver installed at: {path}")
            return path
        except Exception as e:
            logger.error(f"❌ ChromeDriver 자동 설치 실패: {e}")
            logger.error("크롬과 ChromeDriver가 올바르게 설치되어 있는지 확인하세요.")
            raise

    @staticmethod
    def is_chrome_running() -> bool:
        """Chrome이 디버깅 모드로 실행 중인지 확인"""
        try:
            response = requests.get(CHROME_DEBUG_ADDRESS)
            return response.status_code == 200
        except requests.ConnectionError:
            return False

    @staticmethod
    def start_chrome_instance():
        """새로운 Chrome 인스턴스를 디버깅 모드로 시작"""
        import os
        
        # Chrome 실행 파일 존재 확인
        if not os.path.exists(CHROME_EXECUTABLE_PATH):
            error_msg = (f"Chrome 실행 파일을 찾을 수 없습니다: {CHROME_EXECUTABLE_PATH}\n"
                        "Chrome이 설치되어 있는지 확인하세요.")
            logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        cmd = [
            CHROME_EXECUTABLE_PATH,
            f'--remote-debugging-port={CHROME_DEBUG_PORT}',
            f'--user-data-dir={DIR_CHROME_TEMP}'
        ]
        try:
            subprocess.Popen(cmd)
            logger.info(f"Chrome 실행 성공: {CHROME_EXECUTABLE_PATH}")
        except Exception as e:
            error_msg = f"Chrome 실행 실패: {e}\n경로: {CHROME_EXECUTABLE_PATH}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
        time.sleep(Timeouts.CHROME_START_WAIT)


class JiraAutomation:
    """JIRA 자동화 클래스"""
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.chrome_manager = ChromeDriverManager()
    
    def start_driver(self) -> webdriver.Chrome:
        """Chrome 드라이버를 시작하고 반환"""
        try:
            # Chrome이 이미 실행 중인지 확인
            if self.chrome_manager.is_chrome_running():
                logger.info("기존 Chrome 인스턴스에 연결 중...")
                driver = self._connect_to_existing_chrome()
            else:
                logger.info("새로운 Chrome 인스턴스 시작 중...")
                self.chrome_manager.start_chrome_instance()
                driver = self._connect_to_existing_chrome()
            
            self.driver = driver
            return driver
            
        except Exception as e:
            logger.error(f"Chrome 드라이버 시작 실패: {e}")
            raise
    
    def _connect_to_existing_chrome(self) -> webdriver.Chrome:
        """기존 Chrome 인스턴스에 연결"""
        chrome_options = Options()
        chrome_options.debugger_address = f"127.0.0.1:{CHROME_DEBUG_PORT}"
        
        path = self.chrome_manager.install_chromedriver()
        service = Service(path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # 새 탭 열기
        driver.execute_script("window.open('');")
        new_tab = driver.window_handles[-1]
        driver.switch_to.window(new_tab)
        
        return driver
    
    def create_issue(self, issue_data: dict, pause_for_review: bool = True):
        """JIRA 이슈를 생성"""
        if not self.driver:
            self.start_driver()
        
        try:
            #이슈 생성 시간 측정
            start_time = time.time()    
            #JIRA 대시보드로 이동
            self._navigate_to_jira()
            #Create Issue 버튼 클릭
            self._click_create_button()
            #이슈 폼 채우기
            self._fill_issue_form(issue_data)
            #이슈 생성 시간 측정
            end_time = time.time()
            logger.info(f"이슈 생성 소요 시간: {end_time - start_time}초")
            
            # 사용자 확인을 위해 일시정지 (옵션)
            if pause_for_review:
                os.system("pause")
            
        except Exception as e:
            logger.error(f"이슈 생성 중 오류 발생: {e}")
            raise
    
    def _navigate_to_jira(self):
        """JIRA 대시보드로 이동"""
        self.driver.implicitly_wait(Timeouts.IMPLICIT_WAIT)
        self.driver.get(JIRA_BASE_URL)
        self.driver.implicitly_wait(3)
    
    def _click_create_button(self):
        """Create Issue 버튼 클릭"""
        try:
            self.driver.find_element(By.XPATH, JiraXPaths.CREATE_BUTTON).click()
        except:
            logger.info("Create Issue 버튼을 찾을 수 없어 대체 버튼을 시도합니다")
            self.driver.implicitly_wait(1)
            self.driver.find_element(By.XPATH, JiraXPaths.CREATE_BUTTON_ALT).click()
        
        self.driver.implicitly_wait(5)
    
    def _fill_issue_form(self, data: dict):
        """이슈 폼을 채우는 메인 함수"""
        # Team
        self._select_dropdown_item(JiraXPaths.TEAM_FIELD, data.get('team', ''), exact_match=True)
        time.sleep(Timeouts.MEDIUM_WAIT)
        
        # Summary
        self.driver.find_element(By.XPATH, JiraXPaths.SUMMARY_FIELD).send_keys(data.get('summary', ''))
        
        # Assign to me
        self.driver.find_element(By.XPATH, JiraXPaths.ASSIGNEE_BUTTON).click()
        self.driver.implicitly_wait(1)
        
        # Reviewer
        reviewer_field = self.driver.find_element(By.XPATH, JiraXPaths.REVIEWER_FIELD)
        reviewer_field.send_keys(data.get('reviewer', ''))
        time.sleep(Timeouts.MEDIUM_WAIT)
        reviewer_field.send_keys(Keys.RETURN)
        time.sleep(Timeouts.SHORT_WAIT)
        
        # Linked Issues
        linked_issues = data.get('linkedIssues', '')
        if linked_issues:
            self._select_dropdown_item(JiraXPaths.LINKED_ISSUES, linked_issues, 
                                     exact_match=True, multiple_values=True)
        
        # Target Linked Issues
        issue = data.get('issue', '')
        if issue:
            time.sleep(Timeouts.SHORT_WAIT)
            self._select_dropdown_item(JiraXPaths.TARGET_LINKED_ISSUES, issue, 
                                     exact_match=False, multiple_values=False)
        
        # Parent Issue
        parent = data.get('parent', '')
        if parent:
            time.sleep(Timeouts.SHORT_WAIT)
            self._select_dropdown_item(JiraXPaths.PARENT_ISSUE, parent, 
                                     exact_match=True, multiple_values=False)
        
        # 나머지 필드들 채우기
        self._fill_remaining_fields(data)
    
    def _fill_remaining_fields(self, data: dict):
        """나머지 필드들을 채우는 함수"""
        field_mapping = {
            'branch': JiraXPaths.BRANCH_FIELD,
            'build': JiraXPaths.BUILD_FIELD, 
            'fixversion': JiraXPaths.FIX_VERSION_FIELD,
            'component': JiraXPaths.COMPONENTS_FIELD,
            'label': JiraXPaths.LABELS_FIELD,
            'priority': JiraXPaths.PRIORITY_FIELD,
            'severity': JiraXPaths.SEVERITY_FIELD,
            'prevalence': JiraXPaths.PREVALENCE_FIELD,
            'repro_rate': JiraXPaths.REPRO_RATE_FIELD
        }
        
        multiple_value_fields = {'branch', 'build', 'fixversion', 'component', 'label'}
        
        for field_name, xpath in field_mapping.items():
            value = data.get(field_name, '')
            if value:
                multiple = field_name in multiple_value_fields
                self._select_dropdown_item(xpath, value, multiple_values=multiple)
        
        # Steps
        steps = data.get('steps', '')
        if steps:
            self.driver.find_element(By.XPATH, JiraXPaths.STEPS_FIELD).send_keys(steps)
        
        # Description
        description = data.get('description', '')
        if description:
            #Send key하기전에 해당 필드에 기본 내용을 모두 삭제 해야함
            self.driver.find_element(By.XPATH, JiraXPaths.DESCRIPTION_FIELD).clear()
            time.sleep(Timeouts.SHORT_WAIT)
            self.driver.find_element(By.XPATH, JiraXPaths.DESCRIPTION_FIELD).send_keys(description)
    
    def _select_dropdown_item(self, dropdown_xpath: str, item: str = "Bug", 
                            exact_match: bool = False, timeout: float = 0.1, 
                            multiple_values: bool = False):
        """드롭다운에서 특정 항목을 선택하는 함수"""
        if not item:
            return
            
        values = item.strip().split() if multiple_values else [item]
        
        for val in values:
            self._select_single_value(dropdown_xpath, val, exact_match, timeout)
    
    def _select_single_value(self, dropdown_xpath: str, value: str, 
                           exact_match: bool, timeout: float):
        """단일 값을 선택하는 내부 함수"""
        found = False
        
        # 1. send_keys 방식 먼저 시도
        try:
            element = self.driver.find_element(By.XPATH, dropdown_xpath)
            element.send_keys(value)
            time.sleep(Timeouts.MEDIUM_WAIT)
            element.send_keys(Keys.RETURN)
            logger.info(f"✅ {value} (send_keys 방식 성공)")
            found = True
        except Exception as e:
            logger.warning(f"❌ {value} (send_keys 방식 실패, 드롭다운 클릭 방식 시도)")
        
        # 2. send_keys 실패 시 드롭다운 클릭 방식 반복 시도
        if not found:
            for attempt in range(Timeouts.DROPDOWN_RETRY):
                try:
                    dropdown_element = WebDriverWait(self.driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, dropdown_xpath))
                    )
                    
                    # 이미 선택된 항목인지 확인 (대소문자 무시)
                    current_text = dropdown_element.text.strip().lower()
                    if current_text == value.lower():
                        logger.info(f"✅ {value} (이미 선택됨)")
                        found = True
                        break
                    
                    # 드롭다운 클릭
                    time.sleep(0.2)
                    dropdown_element.click()
                    time.sleep(0.3)  # 드롭다운이 펼쳐질 시간 증가
                    
                    # 여러 XPath 패턴으로 시도 (대소문자 구분 없이)
                    option_xpaths = []
                    
                    if exact_match:
                        # 정확히 일치하는 텍스트 (대소문자 무시)
                        option_xpaths.append(f'//*[translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz")="{value.lower()}"]')
                        option_xpaths.append(f'//*[text()="{value}"]')
                        # 첫 글자만 대문자인 경우 (Bug, High 등)
                        option_xpaths.append(f'//*[text()="{value.capitalize()}"]')
                    else:
                        # 포함하는 텍스트 (대소문자 무시)
                        option_xpaths.append(f'//*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "{value.lower()}")]')
                        option_xpaths.append(f'//*[contains(text(), "{value}")]')
                        option_xpaths.append(f'//*[contains(text(), "{value.capitalize()}")]')
                    
                    # 각 XPath 패턴 시도
                    item_option = None
                    for option_xpath in option_xpaths:
                        try:
                            item_option = WebDriverWait(self.driver, timeout).until(
                                EC.element_to_be_clickable((By.XPATH, option_xpath))
                            )
                            if item_option:
                                break
                        except:
                            continue
                    
                    if not item_option:
                        raise Exception(f"항목을 찾을 수 없음: {value}")
                    
                    time.sleep(0.1)
                    
                    # 클릭 시도
                    try:
                        # JavaScript로 클릭 시도
                        self.driver.execute_script("arguments[0].click();", item_option)
                        found = True
                        logger.info(f"✅ {value} (Dropdown - JS Click)")
                        break
                    except:
                        try:
                            # 일반 클릭 시도
                            item_option.click()
                            found = True
                            logger.info(f"✅ {value} (Dropdown - Click)")
                            break
                        except:
                            # RETURN 키로 시도
                            dropdown_element.send_keys(Keys.RETURN)
                            found = True
                            logger.info(f"✅ {value} (Dropdown - RETURN)")
                            break
                        
                except Exception as e:
                    logger.debug(f"시도 {attempt + 1}/{Timeouts.DROPDOWN_RETRY} 실패: {e}")
                    time.sleep(0.3)
            
        if not found:
            logger.warning(f"❌ {value} (드롭다운 항목을 선택할 수 없음)")
            # 마지막으로 send_keys 방식 재시도
            try:
                element = self.driver.find_element(By.XPATH, dropdown_xpath)
                element.clear()
                time.sleep(0.1)
                element.send_keys(value)
                time.sleep(Timeouts.MEDIUM_WAIT)
                element.send_keys(Keys.RETURN)
                logger.info(f"✅ {value} (send_keys 방식 재시도 성공)")
            except Exception as e:
                logger.error(f"❌ {value} (드롭다운 항목 선택 최종 실패: {e})")
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def close_current_tab(self):
        """현재 탭만 닫기 (드라이버는 유지)"""
        if self.driver:
            try:
                # 현재 탭 닫기
                self.driver.close()
                # 남은 탭이 있으면 첫 번째 탭으로 전환
                if len(self.driver.window_handles) > 0:
                    self.driver.switch_to.window(self.driver.window_handles[0])
                else:
                    self.driver = None
            except Exception as e:
                logger.error(f"탭 닫기 실패: {e}")
    
    def create_new_tab(self):
        """새 탭을 생성하고 전환"""
        if self.driver:
            try:
                # 새 탭 열기
                self.driver.execute_script("window.open('');")
                # 새로 생성된 탭으로 전환
                new_tab = self.driver.window_handles[-1]
                self.driver.switch_to.window(new_tab)
            except Exception as e:
                logger.error(f"새 탭 생성 실패: {e}")
                raise


def create_issue(summary: str, linkedIssues: str, issue: str, parent: str, 
                reviewer: str, branch: str, build: str, fixversion: str, 
                component: str, label: str, priority: str, severity: str, 
                prevalence: str, repro_rate: str, steps: str, description: str, team: str):
    """이슈 생성을 위한 편의 함수 (기존 호환성 유지)"""
    issue_data = {
        'summary': summary,
        'linkedIssues': linkedIssues,
        'issue': issue,
        'parent': parent,
        'reviewer': reviewer,
        'branch': branch,
        'build': build,
        'fixversion': fixversion,
        'component': component,
        'label': label,
        'priority': priority,
        'severity': severity,
        'prevalence': prevalence,
        'repro_rate': repro_rate,
        'steps': steps,
        'description': description,
        'team': team
    }
    
    automation = JiraAutomation()
    try:
        automation.create_issue(issue_data)
    finally:
        automation.close()


if __name__ == "__main__":
    # 예제 사용법
    example_data = {
        'summary': "App crashes when clicking the login button",
        'linkedIssues': 'relates to',
        'issue': "P2-55506",
        'parent': "P2-55506",
        'reviewer': "성민석",
        'branch': "game test",
        'build': "CompileBuild_DEV_game_SEL236613_r263331",
        'fixversion': "CBT",
        'component': "Tech_UXUI",
        'label': "facility",
        'priority': "High",
        'severity': "Critical",
        'prevalence': "All",
        'repro_rate': "100%",
        'steps': "1. Open the app\n2. Click on Login button\n3. Observe the crash",
        'description': "The application crashes when the login button is clicked.",
        'team': "Progression"
    }
    
    automation = JiraAutomation()
    try:
        automation.create_issue(example_data)
    finally:
        automation.close()


