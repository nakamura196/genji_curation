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
options.add_argument('--user-data-dir=/Users/nakamurasatoru/git/d_genji/genji_curation/src/batch_kyoto01/tmp2')
options.add_argument('--profile-directory=tmp')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options) #, executable_path=driver_path

# Chrome起動
# driver.maximize_window() # 画面サイズ最大化
urls = []
map = {}

# GoogleログインURL
try:
    url = 'https://mp.ex.nii.ac.jp/kuronet/'
    driver.get(url)

    time.sleep(10)

    driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

    time.sleep(10)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")

    trs = soup.find("tbody").find_all("tr")

    # check

    

    for i in range(len(trs)):
    
        # index = len(trs) - (1 + i)
        index = i
        tr = trs[index]
        # print(str(i+1) + "/" + str(len(trs)) + " sequence")
        tds = tr.find_all("td")
        td3 = tds[3]
        id = tds[0].text

        cr = tds[1].find("a").get("href")
        time_str = tds[1].find_all("div")[1].text

        if len(td3.find_all("div")) == 1:
            sequence = "https://mp.ex.nii.ac.jp" + td3.find("a").get("href")
            urls.append(sequence)
            map[sequence] = id + " - " + time_str + " - " + cr
except Exception as e:
    print(e, id)

for i in range(len(urls)):
    url = urls[i]

    '''
    if "kotenseki" in map[url]:
        break
    '''

    print("index", i+1, "残りの行数", len(urls), "全行数", len(trs))

    driver.get(url)
    html = driver.page_source.encode('utf-8')

    soup = BeautifulSoup(html, features="lxml")

    if "キュレーションが不正" in str(soup) or "Internal Server Error" in str(soup):
        print("err", map[url])
        # time.sleep(5)

#全てのウィンドウを閉じる
driver.quit()