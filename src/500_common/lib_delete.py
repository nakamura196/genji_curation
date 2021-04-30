import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import chromedriver_binary
# モジュールのインポート
from bs4 import BeautifulSoup

import requests

TIME_OUT = 10
LOGIN_COUNT = 100

########

collection_url = "https://utda.github.io/genji/iiif/ndl-8943312/top.json"
collection = requests.get(collection_url).json()

manifests_arr = collection["manifests"]
manifests = []
for i in range(len(manifests_arr)):
    manifest = manifests_arr[i]["@id"]
    manifests.append(manifest)

#########

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

        try:
            driver.execute_script("window.stop();")
        except Exception as e:
            print(e)
    
    except Exception as e:
        print(e)

def main(userDataDir, profileDirectory, manifests, path):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir='+userDataDir)
    options.add_argument('--profile-directory='+profileDirectory)  # この行を省略するとDefaultフォルダが指定されます

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(TIME_OUT)

    waitTime = 10

    flg = True

    prev_size = -1

    while flg:

        login(driver, waitTime)

        # ローカルファイルからの読み込み
        if path != None:
            soup = BeautifulSoup(open(path), "lxml")
        else:
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "lxml")

        if soup.find("tbody"):
            trs = soup.find("tbody").find_all("tr")

            # 予約の実行

            urls = []

            exists = []

            for tr in trs:
                tds = tr.find_all("td")

                td = tds[1]
                if td.find("a") == None:
                    print("err", td)
                    continue

                icv = td.find("a").get("href")
                
                manifest = icv.split("manifest=")[1].split("&")[0]

                if manifest not in exists:
                    exists.append(manifest)

                # if manifest in manifests:
                if "ndl.go.jp" in manifest:
                    td2 = tds[2]
                    reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
                    
                    delete = reserve.replace("reserve", "delete")
                    urls.append(delete)

            print(len(urls))

            if prev_size == len(urls):
                flg = False
                urls = []
            else:
                prev_size = len(urls)

            if len(urls) == 0:
                flg = False

            for i in range(len(urls)):
                print(i, len(urls))

                url = urls[i]

                # time.sleep(1)
                try:
                    driver.get(url)
                except Exception as e:
                    print(e)

    #全てのウィンドウを閉じる
    driver.quit()
