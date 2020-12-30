import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests
import sys
import argparse
import Levenshtein

vols = [1, 2, 3, 4, 5]




man = {
    '''
    1 : "https://nakamura196.github.io/genji_curation/iiif/saga/01.json",
    2 : "https://nakamura196.github.io/genji_curation/iiif/saga/02.json",
    3 : "https://nakamura196.github.io/genji_curation/iiif/saga/03.json",
    4 : "https://nakamura196.github.io/genji_curation/iiif/saga/04.json",
    5 : "https://nakamura196.github.io/genji_curation/iiif/saga/05.json"
    '''
}

for vol in vols:
    man[vol] = "https://nakamura196.github.io/genji_curation/iiif/saga/"+str(vol).zfill(2)+".json"

def getIndex(member):
    return int(member["@id"].split("#")[0].split("/p")[1])

import glob

dir_name = "121_saga"

files = sorted(glob.glob("/Users/nakamura/git/d_genji/genji_curation/docs/iiif/"+dir_name+"/*.json"))

for file in files:
    with open(file) as f:

        vol = int(file.split("/")[-1].split(".json")[0])

        if vol not in man:
            continue

        map = {}

        ###########################

        df = json.load(f)

        members = df["selections"][0]["members"]

        for member in members:
            index = getIndex(member)
            if index not in map:
                map[index] = []
            map[index].append(member)

        ############################

        mc = requests.get(man[vol]).json()

        for member in mc["selections"][0]["members"]:
            index = getIndex(member)
            if index not in map:
                map[index] = []

            ########### マーカーのためのID作成

            member_id = member["@id"]
            sss = member_id.split("#xywh=")

            canvas_id = sss[0]
            xywh = sss[1].split(",")

            d = 2

            y = int(int(xywh[1]) * d / (d+1))

            x = int(xywh[0]) + int(int(xywh[2]) / 2)

            # 例外処理
            if y == 0:
                y = 800
                x = int(xywh[0])
            
            w = 1

            member_id = canvas_id+"#xywh="+str(x)+","+str(y)+","+str(w)+",1"

            ###########

            page = "新編日本古典文学全集・番号: " + str(member["metadata"][0]["value"])

            member["metadata"].append({
                "label": "Annotation",
                "value": [
                    {
                        "@id": member_id,
                        "@type": "oa:Annotation",
                        "motivation": "sc:painting",
                        "resource": {
                            "@type": "cnt:ContentAsText",
                            "chars": page,
                            "format": "text/html",
                            "marker": {
                                "border-color": "red",
                                "@type": "dctypes:Image",
                                "@id": "https://nakamura196.github.io/genji_curation/icon/blue.png#xy=16,16"
                            }
                        },
                        "on": member_id
                    }
                ]
            })

            map[index].append(member)

        print(map)
    
        ############################

        members = []
        for index in sorted(map):
            arr = map[index]
            for member in arr:
                members.append(member)

        df["selections"][0]["members"] = members

        f2 = open(file.replace(dir_name, "131_check_s"), 'w')
        json.dump(df, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

    # break