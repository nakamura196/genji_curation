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
options.add_argument('--user-data-dir=/Users/nakamurasatoru/git/d_genji/genji_curation/src/batch_kyoto01/tmp3')
options.add_argument('--profile-directory=tmp')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options) #options=options, executable_path=driver_path

# Chrome起動
# driver.maximize_window() # 画面サイズ最大化

urls = []
map = {}

try:

    # GoogleログインURL
    url = 'https://mp.ex.nii.ac.jp/kuronet/'
    driver.get(url)

    time.sleep(10)

    print("click")

    driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

    time.sleep(10)

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, "lxml")
    
    if soup.find("tbody"):
        trs = soup.find("tbody").find_all("tr")


    for i in range(len(trs)):
    
        # index = len(trs) - (1 + i)
        index = i
        tr = trs[index]
        # print(str(i+1) + "/" + str(len(trs)) + " reserve")
        tds = tr.find_all("td")
        td2 = tds[2]
        reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
        seqs = td2.find_all("div")
        l_seqs = len(seqs)

        id = tds[0].text
        if l_seqs == 2 or (l_seqs == 3 and seqs[2].text == "失敗：消去"):
            urls.append(reserve)
            map[reserve] = id

except Exception as e:
    print(e)

for i in range(len(urls)):
    url = urls[i]
    print("index", i+1, "残りの行数", len(urls), "全行数", len(trs), "行ID", map[url])
    time.sleep(2)
    driver.get(url)

#全てのウィンドウを閉じる
driver.quit()