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
LOGIN_COUNT = 500

def login(driver, waitTime=10, preTime=10):
    try:
        # GoogleログインURL
        url = 'https://mp.ex.nii.ac.jp/kuronet/'

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

def main(userDataDir, profileDirectory, localPath, manifests, waitTime=10, preTime=10):

    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir='+userDataDir)
    options.add_argument('--profile-directory='+profileDirectory)  # この行を省略するとDefaultフォルダが指定されます

    driver = webdriver.Chrome(options=options) #options=options, executable_path=driver_path
    driver.set_page_load_timeout(TIME_OUT)

    

    flg = True

    while flg:

        urls = []
        map = {}
        target_size = 0

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

                if len(tds) < 3:
                    print(tds)
                    continue

                td = tds[1]
                if td.find("a") == None:
                    print("err", td)
                    continue

                icv = td.find("a").get("href")
                
                manifest = icv.split("manifest=")[1].split("&")[0]

                if manifests != None and manifest not in manifests:
                    continue
                else:
                    target_size += 1
                
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
            print("target size", target_size)

            if len(urls) == 0:
                flg = False

            for i in range(len(urls)):
                url = urls[i]
                print("index", i+1, "残りの行数", len(urls), "全行数", len(trs), "行ID", map[url])
                

                try:
                    driver.get(url)

                    html = driver.page_source.encode('utf-8')
                    soup = BeautifulSoup(html, "lxml")

                    wait = -1

                    
                    
                    try:
                        wait = int(str(soup).split("現在")[1].split("件待")[0])
                    except Exception as e:
                        print(e)

                    print("wait", wait)

                    time.sleep(2) # 終了後の待ち時間（必須）
                    # driver.get("http://localhost")

                    if wait > 3:
                        time.sleep(wait) # ここを変える
                except Exception as e:
                    print(e)
                

                if (i + 1) % LOGIN_COUNT == 0:
                    login(driver)

    #全てのウィンドウを閉じる
    driver.quit()