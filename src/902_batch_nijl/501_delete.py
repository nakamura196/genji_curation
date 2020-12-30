import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# モジュールのインポート
from bs4 import BeautifulSoup

# chromedriverのPATHを指定（Pythonファイルと同じフォルダの場合）
driver_path = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/Users/nakamura/Library/Application Support/Google/Chrome')
options.add_argument('--profile-directory=Profile 1')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options, executable_path=driver_path)

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

trs = soup.find("tbody").find_all("tr")

# 予約の実行

for tr in trs:
    tds = tr.find_all("td")
    td2 = tds[2]
    reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
    delete = reserve.replace("reserve", "delete")
    time.sleep(3)
    driver.get(delete)
    time.sleep(3)

    id = reserve.split("=")[1].split("&")[0]


    driver.get("https://mp.ex.nii.ac.jp/api/kuronet/index#" + id)