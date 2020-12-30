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
options.add_argument('--user-data-dir=/Users/nakamurasatoru/git/d_genji/genji_curation/src/batch_kyoto01/tmp3')
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

trs = soup.find("tbody").find_all("tr")

# 予約の実行

urls = []

for tr in trs:
    tds = tr.find_all("td")

    icv = tds[1].find("a").get("href")

    if not "dl.ndl.go.jp" in icv:
        continue
    else:
        td2 = tds[2]
        reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
        
        delete = reserve.replace("reserve", "delete")
        urls.append(delete)
        

for i in range(len(urls)):
    print(i, len(urls))

    url = urls[i]

    time.sleep(1)
    driver.get(url)
