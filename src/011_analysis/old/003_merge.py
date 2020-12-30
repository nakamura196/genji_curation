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



# https://us-central1-genji-5ca47.cloudfunctions.net/api/curation/

df = pd.read_excel('/Users/nakamura/git/d_genji/kouigenjimonogatari.github.io/src/data/metadata_all.xlsx', header=None, index_col=None)

configs = {}
pages = {}

for i in range(len(df.index)):

    uri = df.iloc[i, 0]
    if not pd.isnull(uri):
        row_num = df.iloc[i, 2]
        if int(row_num) == 1:
            title = df.iloc[i, 3]
            vol = df.iloc[i, 6]
            page = df.iloc[i, 1]

            if vol not in configs:
                configs[vol] = {
                    "data" : {}
                }

            page = int(page)
            configs[vol]["data"][title] = page
            pages[page] = title

for vol in man:

    VOL = str(vol).zfill(2)

    print(VOL)

    config = configs[vol]

    koui = config["data"]

    

    path = '../../docs/iiif/taisei/'+VOL+'.json'

    if not os.path.exists(path):
        continue

    map = {}

    with open(path) as f:
        df = json.load(f)
        members = df["selections"][0]["members"]

        for member in members:
            index = getIndex(member)
            if index not in map:
                map[index] = []
            map[index].append(member)
 

    ################ Manual
    mc = requests.get(man[vol]).json()
    print(mc)

    for member in mc["selections"][0]["members"]:
        index = getIndex(member)
        if index not in map:
            map[index] = []

        page =  int(member["metadata"][0]["value"])

        chars = "大成番号: " + str(page) + " - " + pages[page]

        sss = member["@id"].split("#xywh=")
        canvas_id = sss[0]
        xywh = sss[1].split(",")

        member_id = canvas_id + "#xywh=" + str(xywh[0])+",10," + str(xywh[2]) + "," + str(int(int(xywh[3]) / 2))

        member["@id"] = member_id

        member["metadata"].append({
            "label": "Annotation",
            "value": [
                {
                    "@id": member["@id"],
                    "@type": "oa:Annotation",
                    "motivation": "sc:painting",
                    "on": member["@id"],
                    "resource": {
                        "@type": "cnt:ContentAsText",
                        "chars": chars,
                        "format": "text/plain",
                        "marker": {
                            "border-color": "blue"
                        }
                    }
                }
            ]
        })

        map[index].append(member)

    members = []
    for index in sorted(map):
        arr = map[index]
        for member in arr:
            members.append(member)

    df["selections"][0]["members"] = members

    f2 = open(path.replace("/taisei/", "/check/"), 'w')
    json.dump(df, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))