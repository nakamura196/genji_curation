import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
# モジュールのインポート
from bs4 import BeautifulSoup

import chromedriver_binary

TIME_OUT = 10
LOGIN_COUNT = 100

def login(driver, waitTime=10):
    # GoogleログインURL
    url = 'https://mp.ex.nii.ac.jp/kuronet/'

    try:
        driver.get(url)

        time.sleep(10)

        # ログイン
        
        driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

        print("logged in")

        time.sleep(waitTime)

        print("wait finish", waitTime)

        try:
            driver.execute_script("window.stop();")
        except Exception as e:
            print(e)

        print("window stop finished")

    except Exception as e:
            print(e)

def main(userDataDir, profileDirectory, waitTime=10):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir='+userDataDir)
    options.add_argument('--profile-directory='+profileDirectory)  # この行を省略するとDefaultフォルダが指定されます

    driver = webdriver.Chrome(options=options) #options=options, executable_path=driver_path
    driver.set_page_load_timeout(TIME_OUT)

    login(driver, waitTime)

    # ローカルファイルからの読み込み
    if False:
        soup = BeautifulSoup(open("XXX/data/result.html"), "lxml")
    else:
        try:
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "lxml")
        except Exception as e:
            print(e)

    #全てのウィンドウを閉じる
    driver.quit()

    return soup