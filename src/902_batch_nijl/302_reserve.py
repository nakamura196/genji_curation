import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# モジュールのインポート
from bs4 import BeautifulSoup

import chromedriver_binary

# chromedriverのPATHを指定（Pythonファイルと同じフォルダの場合）
# driver_path = '/usr/local/bin/chromedriver'

options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=/Users/nakamurasatoshi/Desktop/chrome')
options.add_argument('--profile-directory=Default')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options) #options=options, executable_path=driver_path

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
    index = len(trs) - (1 + i)
    tr = trs[index]
    print(str(i+1) + "/" + str(len(trs)) + " reserve")
    tds = tr.find_all("td")
    td2 = tds[2]
    reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
    seqs = td2.find_all("div")
    l_seqs = len(seqs)
    if l_seqs == 2 or (l_seqs == 3 and seqs[2].text == "失敗：消去"):
        # time.sleep(6)
        time.sleep(3)
        driver.get(reserve)
        # time.sleep(1)
        # time.sleep(1)

        '''

        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        a_arr = soup.find_all("a")
        for a in a_arr:
            href = a.get("href")
            if "index" in href:
                href = "https://mp.ex.nii.ac.jp" + href
                driver.get(href)
        '''

        '''
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        href = soup.find("a").get("href")
        driver.get(href)
        '''

        # time.sleep(1)

        # id = reserve.split("=")[1].split("&")[0]
        # driver.get("https://mp.ex.nii.ac.jp/api/kuronet/index#" + id)

#全てのウィンドウを閉じる
driver.quit()