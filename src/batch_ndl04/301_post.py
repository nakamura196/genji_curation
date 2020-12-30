# coding: utf-8
import requests
import time
import json
import os
import time
import yaml
import hashlib

skip_index = 1409
collectionUrl = "https://utda.github.io/genji/iiif/ndl-2610583/top.json"
areas = ["3600,370,3000,4400", "560,370,3000,4400"]
countMax = 5

def aaa(message):
    
    url = "https://notify-api.line.me/api/notify"
    token = 'XHy7UYt3LljhlDnTD8uKii5hfS1MGAUrGMij0gkQC25'
    headers = {"Authorization" : "Bearer "+ token}
    payload = {"message" :  message}

    requests.post(url ,headers = headers ,params=payload)

with open('../token.yml') as file:
    obj = yaml.safe_load(file)
    token = obj["token"]

count = 0

aaa("start")

manifests = requests.get(collectionUrl).json()["manifests"]

arr = []

for i in range(len(manifests)):

    if i > 0:
        print(i)
    else:
        continue

    manifest = manifests[i]["@id"]

    name = hashlib.md5(manifest.encode('utf-8')).hexdigest()

    path = "data/" + name + ".json"

    if not os.path.exists(path):

        df = requests.get(manifest).json()

        fw = open(path, 'w')
        json.dump(df, fw, ensure_ascii=False, indent=4, separators=(',', ': '))
        fw.close()

    with open(path) as f:
        df = json.load(f)

    canvases = df["sequences"][0]["canvases"]

    for canvas in canvases:
        canvas["manifest"] = manifest

        arr.append(canvas)

canvases = arr

# areas = ["3600,1000,2400,3000", "1200,1000,2400,3000"]

# areas = ["1000,900,5000,3200"]

flg = True

for j in range(len(canvases)):

    canvas = canvases[j]

    if j < skip_index:
        continue

    manifest = canvas["manifest"]

    print("canvas_index", j, "canvas_size", len(canvases))

    prefix = canvas["images"][0]["resource"]["service"]["@id"]

    for xywh in areas:
        # time.sleep(0.5)

        time_sta = time.time()

        #POSTパラメータは二つ目の引数に辞書で指定する
        response = requests.post(
            'https://mp.ex.nii.ac.jp/api/kuronet/post',
            {
                'image':prefix + '/'+xywh+'/full/0/default.jpg',
                'manifest' : manifest,
                'canvas' : canvas["@id"],
                'xywh' : xywh,
                'token' : token
                })
        #レスポンスオブジェクトのjsonメソッドを使うと、
        #JSONデータをPythonの辞書オブジェクトに変換して取得できる
        

        time_end = time.time()

        tim = time_end- time_sta

        print(response, "time", tim, "count", count)

        if tim < 1:
            count += 1

        if count > countMax:
            message = "post end "+str(j)
            aaa(message)
            flg = False

    if not flg:
        break
            