from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from time import sleep
from colorama import init, Fore
import os
import pyfiglet
import time
import json

init()

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


options = webdriver.ChromeOptions()
options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.add_argument('--headless')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--no-sandbox")
options.add_argument('--window-size=1920x1080')

driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
driver.implicitly_wait(3)
wait = WebDriverWait(driver, 5, 0.2)

cls()
f = pyfiglet.Figlet()
f2 = pyfiglet.Figlet(font='alphabet')
print(Fore.LIGHTRED_EX + f.renderText('Self-diagnosis') + Fore.LIGHTCYAN_EX + f.renderText('Automation') + Fore.RESET + 'Covid 19 Self-diagnosis Automation V3')
print('')

jindan_URL = 'https://hcs.eduro.go.kr/#/loginHome'

with open('settings.json', 'r') as f:
    json_data = json.load(f)

student_name = json_data["STUDENT"]["NAME"]
student_birth = json_data["STUDENT"]["BIRTH"]
student_pass = json_data["STUDENT"]["PASS"]

school_location = json_data["SCHOOL"]["LOCATION"]
school_level = json_data["SCHOOL"]["LEVEL"]
school_name = json_data["SCHOOL"]["NAME"]

print("현재 시각 : " + time.strftime('%X %x %Z'))

print('')
try:
    driver.delete_all_cookies()

    print('')
    print('자가진단 페이지 접속...: ', end="")
    driver.get(jindan_URL)
    sleep(2)
    driver.find_element_by_id('btnConfirm2').click()
    driver.find_element_by_class_name('searchBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')

    print('')
    print('지역 선택...: ', end="")
    Select(driver.find_element_by_id('sidolabel')).select_by_visible_text(school_location)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교급 선택...: ', end="")
    Select(driver.find_element_by_id('crseScCode')).select_by_visible_text(school_level)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교 이름 입력...: ', end="")
    driver.find_element_by_id('orgname').send_keys(school_name)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('검색 버튼 클릭...: ', end="")
    driver.find_element_by_class_name('searchBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학교 선택...: ', end="")
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a')))
    driver.find_element_by_xpath('//*[@id="softBoardListLayer"]/div[2]/div[1]/ul/li/a').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('확인 버튼 클릭...: ', end="")
    driver.find_element_by_class_name('layerFullBtn').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('')
    print('학생 이름 입력...: ', end="")
    driver.find_element_by_id('user_name_input').send_keys(student_name)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    print('학생 생년월일 입력...: ', end="")
    driver.find_element_by_id('birthday_input').send_keys(student_birth)
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')    
    print('확인 버튼 클릭...: ', end="")
    driver.find_element_by_id("btnConfirm").click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('')
    print('비밀번호 입력', end="")
    driver.find_element_by_xpath('//*[@id="password"]').click()
    for i in student_pass:
      print('.', end="")
      driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(f"//*[@aria-label='{i}']"))
    print(':', end="")
    wait.until(expected_conditions.presence_of_element_located((By.ID, 'btnConfirm')))
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'btnConfirm')))
    driver.find_element_by_xpath('//*[@id="btnConfirm"]').click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
    sleep(1)

    print('자가진단을 수행합니다...')

    items = driver.find_element_by_xpath('//*[@id="container"]/div/section[2]/div[2]/ul').find_elements_by_tag_name('li')

    sleep(0.5)
    item = items[0]
    name = item.find_element_by_class_name('name').get_attribute('innerHTML')
      
    item.find_element_by_class_name('name').click()
    print('')
    print('자가진단 대상 : ' + name)
    wait.until(expected_conditions.element_to_be_clickable((By.ID, 'survey_q1a1')))
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath('//*[@id="survey_q1a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="survey_q1a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="survey_q2a1"]'))
    driver.execute_script("arguments[0].click();", driver.find_element_by_xpath('//*[@id="survey_q3a1"]'))

    sleep(2)
    print('확인 버튼 클릭...: ', end="")    
    driver.find_element_by_id("btnConfirm").click()
    print('[' + Fore.LIGHTGREEN_EX + 'OK' + Fore.RESET + ']')
      
    print('')
    print('자가진단이 완료되었습니다.')
  
except:
    print('[' + Fore.LIGHTRED_EX + 'ERROR' + Fore.RESET + ']')
    print("과정중 오류가 발생하였습니다.")
finally:
    driver.stop_client()
