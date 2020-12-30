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
LOGIN_COUNT = 100

def login(driver):
    # GoogleログインURL
    url = 'https://mp.ex.nii.ac.jp/kuronet/'

    driver.get(url)

    time.sleep(2)

    # ログイン
    
    driver.find_element_by_xpath('//*[@onclick="dashboard();"]').click()

    print("logged in")

    time.sleep(2)

    try:
        driver.execute_script("window.stop();")
    except Exception as e:
        print(e)

def main(userDataDir, profileDirectory):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir='+userDataDir)
    options.add_argument('--profile-directory='+profileDirectory)  # この行を省略するとDefaultフォルダが指定されます

    driver = webdriver.Chrome(options=options) #options=options, executable_path=driver_path
    driver.set_page_load_timeout(TIME_OUT)

    urls = []
    map = {}

    login(driver)

    # ローカルファイルからの読み込み
    if False:
        soup = BeautifulSoup(open("XXX/data/result.html"), "lxml")
    else:
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")

    if soup.find("tbody"):
        trs = soup.find("tbody").find_all("tr")

        for i in range(len(trs)):

            index = i
            tr = trs[index]

            tds = tr.find_all("td")

            if len(tds) < 3:
                print(tds)
                continue
            
            td2 = tds[2]
            if td2.find("a") == None:
                print("err", td2)
                continue
            reserve = "https://mp.ex.nii.ac.jp" + td2.find("a").get("href")
            seqs = td2.find_all("div")
            l_seqs = len(seqs)

            id = tds[0].text
            if l_seqs == 2 or (l_seqs == 3 and seqs[2].text == "失敗：消去"):
                urls.append(reserve)
                map[reserve] = id

        print("len(trs)", len(trs))

        for i in range(len(urls)):
            url = urls[i]
            print("index", i+1, "残りの行数", len(urls), "全行数", len(trs), "行ID", map[url])
            time.sleep(5)
            driver.get(url)

            if (i + 1) % LOGIN_COUNT == 0:
                login(driver)

    #全てのウィンドウを閉じる
    driver.quit()