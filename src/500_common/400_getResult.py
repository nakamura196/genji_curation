import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import chromedriver_binary
# モジュールのインポート
from bs4 import BeautifulSoup

# chromedriverのPATHを指定（Pythonファイルと同じフォルダの場合）
driver_path = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=tmp3')
options.add_argument('--profile-directory=tmp')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options)

# options=options, executable_path=driver_path

# Chrome起動
driver.maximize_window() # 画面サイズ最大化

# GoogleログインURL
url = 'https://mp.ex.nii.ac.jp/kuronet/'
driver.get(url)

time.sleep(5)

driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

time.sleep(5)

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "lxml")

with open("data/result.html", mode='w') as f:
    f.write(str(soup))

#全てのウィンドウを閉じる
driver.quit()