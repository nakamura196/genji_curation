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

man = {
    1 : "https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/f170ac10-3b5a-11ea-9af3-6d38dcecde57",
    2 : "https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/751c9880-376e-11ea-864a-b7309a5f3851",
    3 : "https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/eef01090-5d18-11ea-9a21-bd6034644602",
    4 : "https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/fae795f0-672a-11ea-ad88-a155c528a51a",
    5 : "https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/acf18b50-7d53-11ea-add7-93ffe60ca00e"
}

def getIndex(member):
    return int(member["@id"].split("#")[0].split("/p")[1])

import glob

type = "_all"

dir_name = "021_taisei"+type

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

            if y == 0:
                y = 800
            
            if vol == 1:
                w = 1
            else:
                # w = int(int(xywh[2]) / 2)
                w = 1

            x = int(xywh[0]) + int(int(xywh[2]) / 2)

            member_id = canvas_id+"#xywh="+str(x)+","+str(y)+","+str(w)+",1"

            ###########

            page = "源氏物語大成・番号: " + str(member["metadata"][0]["value"])

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

        f2 = open(file.replace(dir_name, "031_check"+type), 'w')
        json.dump(df, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))