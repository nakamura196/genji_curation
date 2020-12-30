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
LOGIN_COUNT = 1000

def login(driver, waitTime=10, preTime=10):
    # GoogleログインURL
    url = 'https://mp.ex.nii.ac.jp/kuronet/'

    try:
        driver.get(url)

        time.sleep(preTime)

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

def main(userDataDir, profileDirectory, localPath, waitTime=10, preTime=10, check=False):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir='+userDataDir)
    options.add_argument('--profile-directory='+profileDirectory)  # この行を省略するとDefaultフォルダが指定されます

    driver = webdriver.Chrome(options=options) #, executable_path=driver_path
    driver.set_page_load_timeout(TIME_OUT)

    urls = []
    map = {}

    login(driver, waitTime, preTime)

    # ローカルファイルからの読み込み
    if localPath != None:
        soup = BeautifulSoup(open(localPath), "lxml")
    else:
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")

    if soup.find("tbody"):
        trs = soup.find("tbody").find_all("tr")

        for i in range(len(trs)):
            index = i
            tr = trs[index]

            tds = tr.find_all("td")
            if len(tds) < 4:
                print("err", tds)
                continue

            td3 = tds[3]
            id = tds[0].text

            cr = tds[1].find("a").get("href")
            time_str = tds[1].find_all("div")[1].text

            if len(td3.find_all("div")) == 1:
                if td3.find("a") == None:
                    print("err", td3)
                sequence = "https://mp.ex.nii.ac.jp" + td3.find("a").get("href")
                urls.append(sequence)
                map[sequence] = id + " - " + time_str + " - " + cr

        print("len(trs)", len(trs))

        for i in range(len(urls)):
            url = urls[i]

            print("index", i+1, "残りの行数", len(urls), "全行数", len(trs))

            if check:
                print(map[url])

            try:
                driver.get(url)
                html = driver.page_source.encode('utf-8')

                soup = BeautifulSoup(html, features="lxml")

                if "キュレーションが不正" in str(soup) or "Internal Server Error" in str(soup):
                    print("err", map[url])
                    # time.sleep(5)
            except Exception as e:
                print(e)

            if (i + 1) % LOGIN_COUNT == 0:
                login(driver)

    #全てのウィンドウを閉じる
    driver.quit()