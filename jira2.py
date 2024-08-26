from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os

def start_driver():
    driver_name = fr"C:\chromedriver-win64\chromedriver.exe"
    subprocess.Popen(fr'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeTEMP')

    chrome_options = Options()
    chrome_options.debugger_address = "127.0.0.1:9222"
    #chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    try:
        driver = webdriver.Chrome(driver_name, options=chrome_options)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome( options=chrome_options)
    
    return driver

def create_issue(summary, reviewer, branch, build, fixversion, component, label, priority, severity, prevalence, repro_rate, steps, description):
    driver = start_driver()
    # driver_name = fr"C:\chromedriver-win64\chromedriver.exe"
    # subprocess.Popen(fr'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\ChromeTEMP')

    # chrome_options = Options()
    # chrome_options.debugger_address = "127.0.0.1:9222"
    # #chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]

    # try:
    #     driver = webdriver.Chrome(driver_name, options=chrome_options)
    # except:
    #     chromedriver_autoinstaller.install(True)
    #     driver = webdriver.Chrome( options=chrome_options)

    driver.implicitly_wait(10)
    driver.get("https://jira.krafton.com/secure/Dashboard.jspa")
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,'//*[@id="create_link"]').click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'//*[@id="summary"]').send_keys(summary)
    driver.find_element(By.XPATH,'//*[@id="assign-to-me-trigger"]').click()
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,'//*[@id="customfield_14311-field"]').send_keys(reviewer)
    time.sleep(1)
    driver.find_element(By.XPATH,'//*[@id="customfield_14311-field"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="issuelinks-linktype"]').send_keys('bug')
    #driver.find_element(By.XPATH,'//*[@id="issuelinks-linktype"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="customfield_19300-textarea"]').send_keys(branch)
    driver.find_element(By.XPATH,'//*[@id="customfield_14805-textarea"]').send_keys(build)
    driver.find_element(By.XPATH,'//*[@id="fixVersions-textarea"]').send_keys(fixversion)
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,'//*[@id="fixVersions-textarea"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="components-textarea"]').send_keys(component)
    driver.find_element(By.XPATH,'//*[@id="labels-textarea"]').send_keys(label)
    time.sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="labels-textarea"]').send_keys(Keys.RETURN)
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,'//*[@id="priority-field"]').click()
    driver.find_element(By.XPATH,'//*[@id="priority-field"]').send_keys(priority)
    time.sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="priority-field"]').send_keys(Keys.RETURN)
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,'//*[@id="customfield_14610"]').send_keys(severity)
    time.sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="customfield_14610"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="customfield_14611"]').send_keys(prevalence)
    driver.find_element(By.XPATH,'//*[@id="customfield_14611"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="customfield_14612"]').send_keys(repro_rate)
    driver.find_element(By.XPATH,'//*[@id="customfield_14612"]').send_keys(Keys.RETURN)
    driver.find_element(By.XPATH,'//*[@id="customfield_11306"]').send_keys(steps)
    driver.find_element(By.XPATH,'//*[@id="description-wiki-edit"]/nav/div/div/ul/li[2]/button').click()
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH,'//*[@id="description"]').send_keys(description)
    driver.implicitly_wait(2)
    driver.find_element(By.XPATH,'//*[@id="description-wiki-edit"]/nav/div/div/ul/li[1]/button').click()

    os.system("pause")
