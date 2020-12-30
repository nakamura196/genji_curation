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
options.add_argument('--user-data-dir=Chrome12')
options.add_argument('--profile-directory=Profile 1')  # この行を省略するとDefaultフォルダが指定されます

driver = webdriver.Chrome(options=options)

# GoogleログインURL
url = 'https://mp.ex.nii.ac.jp/kuronet/'
driver.get(url)

time.sleep(5)

# ログイン
driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

time.sleep(10)


# ローカルファイルからの読み込み
# soup = BeautifulSoup(open("data/result.html"), "lxml")

html = driver.page_source.encode('utf-8')
soup = BeautifulSoup(html, "lxml")

trs = soup.find("tbody").find_all("tr")

# 予約の実行

urls = []

for tr in trs:
    tds = tr.find_all("td")

    td = tds[1]
    if td.find("a") == None:
        print("err", td)
        continue

    icv = td.find("a").get("href")

    if "rmda.kulib.kyoto-u.ac.jp" not in icv:
        continue
    else:
        if len(tds) < 3:
            print("err", tds)
            continue
        td2 = tds[2]

        if td2 == None:
            print("err", td2)
            continue

        reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
        
        delete = reserve.replace("reserve", "delete")
        urls.append(delete)

print(len(urls))

for i in range(len(urls)):
    print(i, len(urls))

    url = urls[i]

    # time.sleep(1)
    driver.get(url)

#全てのウィンドウを閉じる
driver.quit()
