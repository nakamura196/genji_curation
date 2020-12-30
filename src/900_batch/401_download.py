# coding: utf-8
import requests
import time
import os
import shutil

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

for i in range(1, 55):
    print(str(i) + "/" + str(54))

    manifest = "https://nakamura196.github.io/genji/ugm/utokyo/manifest/"+str(i).zfill(2)+".json"

    df = requests.get(manifest).json()

    canvases = df["sequences"][0]["canvases"]

    path = "/Volumes/HDCL-UT/genji/" + str(i).zfill(2)
    os.makedirs(path, exist_ok=True)

    for j in range(len(canvases)):
        print(str(j + 1) + "/" + str(len(canvases)))
        canvas = canvases[j]

        opath = path + "/" + str(j + 1).zfill(3) + ".jpg"

        if not os.path.exists(opath):


            prefix = canvas["images"][0]["resource"]["service"]["@id"]

            url = prefix + "/full/full/0/default.jpg"

            download_img(url, opath)

        