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
options.add_argument('--user-data-dir=/Users/nakamura/Desktop/ch_user/data1')
options.add_argument('--profile-directory=Profile 1')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options, executable_path=driver_path)

# Chrome起動
# driver.maximize_window() # 画面サイズ最大化

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
for i in range(len(trs)):
    tr = trs[i]
    print(str(i+1) + "/" + str(len(trs)) + " sequence")
    tds = tr.find_all("td")
    td3 = tds[3]
    if len(td3.find_all("div")) == 1:
        sequence = "https://mp.ex.nii.ac.jp" + td3.find("a").get("href")
        time.sleep(1)
        driver.get(sequence)
        # driver.back()
        # time.sleep(2)
        
        # id = sequence.split("=")[1].split("&")[0]
        # driver.get("https://mp.ex.nii.ac.jp/api/kuronet/index#" + id)

#全てのウィンドウを閉じる
driver.quit()