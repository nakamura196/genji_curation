import time
# モジュールのインポート
from bs4 import BeautifulSoup
import requests
import yaml
import json
import hashlib
import os

def get_images_by_soup(soup):

    tr_list = soup.find_all("tr")

    print("len(trs)", len(tr_list))

    images = []

    prefixes = {}
    sizes = {}

    for i in range(1, len(tr_list)):

        tds = tr_list[i].find_all("td")

        img = tds[1].find("img")

        if img == None:
            print("img None", tds)
        else:
            src = img.get("src")

            images.append(src)

            prefix = src.split("/")[2]
            size = src.split("/")[-3]

            if prefix not in prefixes:
                prefixes[prefix] = 0
            prefixes[prefix] += 1

            if size not in sizes:
                sizes[size] = 0
            sizes[size] += 1

    print("sizes", sizes)
    print("prefixes", prefixes)

    return images


def get_images(result_path):

    soup = BeautifulSoup(open(result_path), "lxml")

    return get_images_by_soup(soup)


def line(message):
    url = "https://notify-api.line.me/api/notify"
    token = 'XHy7UYt3LljhlDnTD8uKii5hfS1MGAUrGMij0gkQC25'
    headers = {"Authorization": "Bearer " + token}
    payload = {"message":  message}

    requests.post(url, headers=headers, params=payload)


def get_token(path):
    with open(path) as file:
        obj = yaml.safe_load(file)
        token = obj["token"]
        return token


def load_remote_json(uri, path):
    name = hashlib.md5(uri.encode('utf-8')).hexdigest()
    path = path + "/" + name + ".json"

    dirname = os.path.dirname(path)
    os.makedirs(dirname, exist_ok=True)

    if not os.path.exists(path):

        df = requests.get(uri).json()

        fw = open(path, 'w')
        json.dump(df, fw, ensure_ascii=False, indent=4, separators=(',', ': '))
        fw.close()

    with open(path) as f:
        df = json.load(f)

    return df


def post(url, areas, count_max, token, exist_images, type):

    merged_canvases = []

    if type == "Collection":

        manifests = requests.get(url).json()["manifests"]

        for i in range(len(manifests)):

            manifest = manifests[i]["@id"]

            df = load_remote_json(manifest, "data/manifests")

            canvases = df["sequences"][0]["canvases"]

            for canvas in canvases:
                canvas["manifest"] = manifest

                merged_canvases.append(canvas)

    elif type == "Manifest":

        df = load_remote_json(url, "data/manifests")

        canvases = df["sequences"][0]["canvases"]

        for canvas in canvases:
            canvas["manifest"] = url

            merged_canvases.append(canvas)

    params = []

    count_all = 0

    print("len(merged_canvases)", len(merged_canvases) * 2)

    for j in range(len(merged_canvases)):

        canvas = merged_canvases[j]

        manifest = canvas["manifest"]

        prefix = canvas["images"][0]["resource"]["service"]["@id"]

        for xywh in areas:

            image = prefix + '/'+xywh+'/full/0/default.jpg'

            count_all += 1

            if image.replace("/full/", "/100,/") in exist_images:
                continue
            else:
                params.append({
                    'image': image,
                    'manifest': manifest,
                    'canvas': canvas["@id"],
                    'xywh': xywh,
                    'token': token
                })

    exist_count = 0
    for i in range(len(params)):

        param = params[i]

        print(i+1, len(params), "count_all", count_all)

        # time_sta = time.time()

        try:
            requests.post('https://mp.ex.nii.ac.jp/api/kuronet/post',
                          param, timeout=0.5)
            
        except requests.exceptions.ReadTimeout:
            print("err")
            # pass
        except Exception as e:
            print(e)
        
        '''
        time_end = time.time()
        tim = time_end- time_sta

        if tim < 1:
            exist_count += 1

        print("time", tim, "exist_count", exist_count)
        
        if exist_count > count_max:
            message = "post end "+str(j)
            line(message)
            break
        '''