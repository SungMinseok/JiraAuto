from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import requests

def start_driver():
    chrome_debugging_address = "http://127.0.0.1:9222/json"
    chrome_user_data_dir = r'"C:\ChromeTEMP"'
    chrome_executable_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
    
    try:
        # Check if Chrome is already running with remote debugging
        response = requests.get(chrome_debugging_address)
        if response.status_code == 200:
            # If running, connect to the existing instance
            chrome_options = Options()
            chrome_options.debugger_address = "127.0.0.1:9222"


            # 크롬 드라이버 설치 시도
            try:
                path = chromedriver_autoinstaller.install(True)
                if not path or not os.path.exists(path):
                    raise FileNotFoundError("ChromeDriver installation failed or not found.")
                print(f"✅ ChromeDriver installed at: {path}")
            except Exception as e:
                print(f"❌ ChromeDriver 자동 설치 실패: {e}")
                print("크롬과 ChromeDriver가 올바르게 설치되어 있는지 확인하세요.")
                raise


            # 🔥 Selenium에 경로 직접 넘기기 (핵심 포인트!)
            service = Service(path)
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            #driver = webdriver.Chrome(options=chrome_options)
            
            # Open a new tab and switch to it
            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            
            return driver
    except requests.ConnectionError:
        pass # Continue to start a new instance

    # If not running, start a new instance
    subprocess.Popen(f'{chrome_executable_path} --remote-debugging-port=9222 --user-data-dir={chrome_user_data_dir}')

    # Wait for the Chrome instance to start
    time.sleep(2)

    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"


    # 크롬 드라이버 설치 시도
    try:
        path = chromedriver_autoinstaller.install(True)
        if not path or not os.path.exists(path):
            raise FileNotFoundError("ChromeDriver installation failed or not found.")
        print(f"✅ ChromeDriver installed at: {path}")
    except Exception as e:
        print(f"❌ ChromeDriver 자동 설치 실패: {e}")
        print("크롬과 ChromeDriver가 올바르게 설치되어 있는지 확인하세요.")
        raise


    #chromedriver_autoinstaller.install(True)
        
    # 🔥 Selenium에 경로 직접 넘기기 (핵심 포인트!)
    service = Service(path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    #driver = webdriver.Chrome(options=chrome_options)
    
    # Open a new tab and switch to it
    driver.execute_script("window.open('');")
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    
    return driver


def create_issue(summary, linkedIssues, issue, parent, reviewer, branch, build, fixversion, component, label, priority, severity, prevalence, repro_rate, steps, description,team):
    driver = start_driver()

    driver.implicitly_wait(10)
    driver.get("https://jira.krafton.com/secure/Dashboard.jspa")
    driver.implicitly_wait(10)
    try:
        driver.find_element(By.XPATH,'//*[@id="_r1_"]/span/div[2]/span/div/div/div[1]/button').click() #//*[@id=":r0:"]/span/div[2]/span/div/button
    except :
        print("Create Issue button not found, trying to click the 'Create' button")
        driver.find_element(By.XPATH,'/html/body/div[4]/div[2]/header/span/div[2]/span/div/button').click()
    driver.implicitly_wait(5)
    #time.sleep(5)

    #Issue Type //*[@id="issue-create.ui.modal.create-form.type-picker.issue-type-select"]/div
    # dropdown_issuetype = f'//*[@id="issue-create.ui.modal.create-form.type-picker.issue-type-select"]/div'
    # driver.find_element(By.XPATH,dropdown_issuetype).click()
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,dropdown_issuetype).send_keys(Keys.SPACE)
    # time.sleep(2)
    # driver.implicitly_wait(5)
    # driver.find_element(By.XPATH,dropdown_issuetype).send_keys(Keys.RETURN)
    #time.sleep(0.5)

    # time.sleep(2)

    # dropdown_issuetype = driver.find_element(By.XPATH, '/html/body/div[20]/div[1]/div/div[2]/div/div/section/div[2]/div/div/div/div/div[1]/div/div/div[3]/div/div/div[1]/div/div[1]/div[2]')
    # print(dropdown_issuetype.text)
    # if dropdown_issuetype.text != 'Bug' :
    #     time.sleep(2)  # 요소가 나타날 시간을 줌
    #     dropdown_issuetype.click()
    #     time.sleep(1)  # 요소가 나타날 시간을 줌
    #         # "Bug" 옵션 찾기
    #     option_xpath = '//*[contains(text(), "Bug")]'  # "Bug" 옵션이 있는 태그
    #     bug_option = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, option_xpath))
    #     )

    #     time.sleep(1)  # 요소가 나타날 시간을 줌
    #     # "Bug" 옵션 클릭
    #     bug_option.click()
    #     # dropdown_issuetype.send_keys('bug')
    #     # dropdown_issuetype.send_keys(Keys.ENTER)
    # time.sleep(1)

    #Team
    select_dropdown_item(driver,'//*[@id="customfield_10937-container"]/div/div/div/div/div/div[1]/div[2]',team,True)
    driver.implicitly_wait(1)
    time.sleep(1.5)  # 요소가 나타날 시간을 줌
    
    #Summary
    driver.find_element(By.XPATH,'//*[@id="summary-field"]').send_keys(summary)

    #Assign to me
    driver.find_element(By.XPATH,'//*[@id="assignee-container"]/div/div/div/div/button').click()
    driver.implicitly_wait(1)

    #Reviewer
    #select_dropdown_item(driver,'//*[@id="customfield_10629-field"]',reviewer)
    driver.find_element(By.XPATH,'//*[@id="customfield_10629-field"]').send_keys(reviewer)
    #driver.implicitly_wait(1)
    time.sleep(1.5)  # 요소가 나타날 시간을 줌
    driver.find_element(By.XPATH,'//*[@id="customfield_10629-field"]').send_keys(Keys.RETURN)
    time.sleep(0.5)  # 요소가 나타날 시간을 줌

    
    #Linked Issues
    field_linkedIssues = '//*[@id="issuelinks-container"]/div/div/div/div[1]/div/div/div[1]/div[2]'
    select_dropdown_item(driver,field_linkedIssues,linkedIssues,True,multipleValues=True)

    #driver.find_element(By.XPATH,field_linkedIssues).send_keys(linkedIssues)
    #driver.find_element(By.XPATH,field_linkedIssues).send_keys(Keys.RETURN)

    # if issue != "":
    #     select_dropdown_item(driver,'//*[@id="react-select-35-input"]',issue)
    
    
    field_targetLinkedIssues = '//*[@id="issuelinks-container"]/div/div/div/div[2]/div/div/div/div[1]/div[2]'
    if issue != "":
        time.sleep(0.5)  # 요소가 나타날 시간을 줌
        select_dropdown_item(driver,field_targetLinkedIssues,issue,False,multipleValues=False)
        
        #driver.find_element(By.XPATH,field_targetLinkedIssues).send_keys(issue)
        #time.sleep(0.5)
        #driver.find_element(By.XPATH,field_targetLinkedIssues).send_keys(Keys.RETURN)

    #Parent Issue
    field_parentIssue = '//*[@id="parent-container"]/div/div/div/div[1]/div/div[1]/div[2]'
    time.sleep(0.5)  # 요소가 나타날 시간을 줌
    if issue != "":
        select_dropdown_item(driver,field_parentIssue,parent,True,multipleValues=False)
        #driver.find_element(By.XPATH,field_parentIssue).send_keys(parent)
        #time.sleep(0.5)
        #driver.find_element(By.XPATH,field_parentIssue).send_keys(Keys.RETURN)


    #Branch
    select_dropdown_item(driver,'//*[@id="customfield_10623-field"]',branch,True,multipleValues=True)
    #driver.find_element(By.XPATH,'//*[@id="customfield_10623-field"]').send_keys(branch)
    
    #Build
    select_dropdown_item(driver,'//*[@id="customfield_10627-field"]',build,multipleValues=True)
    
    #Fix version
    #js_select_input(driver, '//*[@id="fixVersions-field"]', fixversion)
    select_dropdown_item(driver,'//*[@id="fixVersions-field"]',fixversion,True,multipleValues=True)
    #driver.find_element(By.XPATH,'//*[@id="fixVersions-field"]').send_keys(fixversion)

    #Components
    select_dropdown_item(driver,'//*[@id="components-field"]',component,multipleValues=True)

    #Label
    select_dropdown_item(driver,'//*[@id="labels-field"]',label,True,multipleValues=True)

    #Priority
    select_dropdown_item(driver,'//*[@id="priority-field"]',priority)
    #driver.find_element(By.XPATH,'//*[@id="priority-field"]').click()
    # driver.find_element(By.XPATH,'//*[@id="priority-field"]').send_keys(priority)
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,'//*[@id="priority-field"]').send_keys(Keys.RETURN)
    # driver.implicitly_wait(1)

    #Severity
    select_dropdown_item(driver,'//*[@id="customfield_10626-field"]',severity)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14610"]').send_keys(severity)
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14610"]').send_keys(Keys.RETURN)


    #Prevalence
    select_dropdown_item(driver,'//*[@id="customfield_10628-field"]',prevalence)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14611"]').send_keys(prevalence)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14611"]').send_keys(Keys.RETURN)

    
    #Reproduction Rate
    select_dropdown_item(driver,'//*[@id="customfield_10634-field"]',repro_rate)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14612"]').send_keys(repro_rate)
    # driver.find_element(By.XPATH,'//*[@id="customfield_14612"]').send_keys(Keys.RETURN)

    #Steps
    #select_dropdown_item(driver,'//*[@id="customfield_11306"]',steps)
    driver.find_element(By.XPATH,'//*[@id="customfield_10399-field"]').send_keys(steps)
    # driver.find_element(By.XPATH,'//*[@id="description-wiki-edit"]/nav/div/div/ul/li[2]/button').click()
    # driver.implicitly_wait(2)

    #Description
    driver.find_element(By.XPATH,'//*[@id="ak-editor-textarea"]').send_keys(description)

    #driver.find_element(By.XPATH,'//*[@id="issuelinks-linktype"]').send_keys(Keys.RETURN)
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,'//*[@id="fixVersions-textarea"]').send_keys(Keys.RETURN)


    
    #driver.implicitly_wait(2)
    #driver.find_element(By.XPATH,'//*[@id="description-wiki-edit"]/nav/div/div/ul/li[1]/button').click()

    os.system("pause")

def select_dropdown_item(driver, dropdown_xpath, item="Bug", exact_match=False, timeout=0.1, multipleValues=False):
    """
    드롭다운에서 특정 항목을 선택하는 함수

    :param driver: Selenium WebDriver 객체
    :param dropdown_xpath: 드롭다운 요소의 XPath
    :param item: 선택할 항목 (기본값: "Bug")
    """
    if multipleValues:
        values = item.strip().split()
    else:
        values = [item]

    for val in values:
        found = False
        # 1. send_keys 방식 먼저 시도
        try:
            driver.find_element(By.XPATH, dropdown_xpath).send_keys(val)
            time.sleep(1.5)
            driver.find_element(By.XPATH, dropdown_xpath).send_keys(Keys.RETURN)
            print(f"✅ {val} (send_keys 방식 입력 시도 성공)")
            found = True
        except Exception as e:
            print(f"❌ {val} (send_keys 방식 입력 실패, 드롭다운 클릭 방식 시도)")

        # 2. send_keys 실패 시 드롭다운 클릭 방식 반복 시도
        if not found:
            for attempt in range(3):  # 최대 3회 반복 시도
                try:
                    dropdown_element = WebDriverWait(driver, timeout).until(
                        EC.presence_of_element_located((By.XPATH, dropdown_xpath))
                    )
                    current_text = dropdown_element.text
                    if current_text != val:
                        time.sleep(0.1)
                        dropdown_element.click()
                        time.sleep(0.1)

                        if exact_match:
                            option_xpath = f'//*[text()="{val}"]'
                        else:
                            option_xpath = f'//*[contains(text(), "{val}")]'

                        item_option = WebDriverWait(driver, timeout).until(
                            EC.element_to_be_clickable((By.XPATH, option_xpath))
                        )
                        time.sleep(0.1)
                        try:
                            item_option.click()
                            found = True
                            print(f"✅ {val} (Dropdown)")
                            break  # 성공하면 반복 종료
                        except:
                            dropdown_element.send_keys(Keys.RETURN)
                            found = True
                            print(f"✅ {val} (Dropdown - RETURN)")
                            break  # 성공하면 반복 종료
                    else:
                        found = True
                        print(f"✅ {val} (이미 선택됨)")
                        break  # 이미 선택되어 있으면 반복 종료
                except Exception as e:
                    time.sleep(0.3)  # 다음 시도 전 대기
        if not found:
            print(f"❌ {val} (드롭다운 항목을 10회 시도해도 선택할 수 없음)")
            # send_keys 방식 입력 시도
            try:
                driver.find_element(By.XPATH,dropdown_xpath).send_keys(val)
                time.sleep(1.5)
                driver.find_element(By.XPATH,dropdown_xpath).send_keys(Keys.RETURN)
                print(f"✅ {val} (send_keys 방식 입력 시도 성공)")
            except Exception as e:
                print(f"❌ {val} (드롭다운 항목 선택 실패)")

def js_select_input(driver, field_xpath, value, timeout=5):
    """
    검색형 드롭다운 필드(input 기반)에 값을 입력하고 선택하는 범용 함수

    :param driver: Selenium WebDriver 객체
    :param field_xpath: 드롭다운 input 요소의 XPath
    :param value: 선택할 항목 텍스트
    :param timeout: 요소 로딩 대기 시간 (기본값: 5초)
    """
    try:
        # 입력 필드 로딩 대기 (요소가 DOM에 있어야만 함)
        input_elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, field_xpath))
        )

        # JS로 포커스 & 값 입력 & 이벤트 디스패치
        driver.execute_script("""
            arguments[0].scrollIntoView({block: 'center'});
            arguments[0].focus();
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, input_elem, value)

        time.sleep(1)
        input_elem.send_keys(Keys.RETURN)

        print(f"✅ 입력 필드 '{field_xpath}'에 '{value}' 선택 완료")

    except Exception as e:
        print(f"❌ '{field_xpath}' 필드 선택 실패: {e}")

if __name__ == "__main__":
    # 예제 데이터
    summary = "App crashes when clicking the login button"
    linkedIssues = 'relates to'
    issue = "P2-55506"
    parent = "P2-55506"
    reviewer = "성민석"
    branch = "game test"
    build = "CompileBuild_DEV_game_SEL236613_r263331"
    fixversion = "CBT"
    component = "Tech_UXUI"
    label = "facility"
    priority = "High"
    severity = "Critical"
    prevalence = "All"
    repro_rate = "100%"
    steps = "1. Open the app\n2. Click on Login button\n3. Observe the crash"
    description = "The application crashes when the login button is clicked. This happens on all tested devices."
    team = "Progression"
    create_issue(summary, linkedIssues, issue, parent, reviewer, branch, build, fixversion, component, label, priority, severity, prevalence, repro_rate, steps, description, team)