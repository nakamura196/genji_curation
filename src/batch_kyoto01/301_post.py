# coding: utf-8
import requests
import time
import json
import yaml

with open('../token.yml') as file:
    obj = yaml.safe_load(file)
    token = obj["token"]

for i in range(1, 2):

    if i > 0:
        print(i)
    else:
        continue

    manifest = "https://kotenseki.nijl.ac.jp/biblio/100153620/manifest"

    print(manifest)

    df = requests.get(manifest).json()

    sequence = df["sequences"][0]

    if "canvases" not in sequence:
        continue

    canvases = sequence["canvases"]

    # areas = ["3600,1000,2400,3000", "1200,1000,2400,3000"]
    areas = ["3000,300,3000,4000", "145,300,3000,4000"]
    # areas = ["1000,900,5000,3200"]

    for j in range(len(canvases)):

        if j < 202:
            continue

        canvas = canvases[j]

        print(i, canvas["@id"])

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

            time_end = time.time()

            tim = time_end- time_sta

            print(response, "time", tim)