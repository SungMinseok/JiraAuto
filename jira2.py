from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import subprocess
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
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
            driver = webdriver.Chrome(options=chrome_options)
            
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
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(options=chrome_options)
    
    # Open a new tab and switch to it
    driver.execute_script("window.open('');")
    new_tab = driver.window_handles[-1]
    driver.switch_to.window(new_tab)
    
    return driver


def create_issue(summary, linkedIssues, issue, reviewer, branch, build, fixversion, component, label, priority, severity, prevalence, repro_rate, steps, description):
    driver = start_driver()

    driver.implicitly_wait(10)
    driver.get("https://jira.krafton.com/secure/Dashboard.jspa")
    driver.implicitly_wait(10)
    driver.find_element(By.XPATH,'//*[@id="create_link"]').click()
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH,'//*[@id="summary"]').send_keys(summary)
    driver.find_element(By.XPATH,'//*[@id="assign-to-me-trigger"]').click()
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,'//*[@id="customfield_14311-field"]').send_keys(reviewer)
    #driver.implicitly_wait(1)
    time.sleep(0.5)
    driver.find_element(By.XPATH,'//*[@id="customfield_14311-field"]').send_keys(Keys.RETURN)
    driver.implicitly_wait(1)
    driver.find_element(By.XPATH,'//*[@id="issuelinks-linktype"]').send_keys(linkedIssues)
    driver.find_element(By.XPATH,'//*[@id="issuelinks-issues-textarea"]').send_keys(issue)
    time.sleep(0.5)

    driver.find_element(By.XPATH,'//*[@id="issuelinks-issues-textarea"]').send_keys(Keys.RETURN)
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
