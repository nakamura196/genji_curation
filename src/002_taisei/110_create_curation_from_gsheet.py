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

df = pd.read_excel('data/大成番号付与.xlsx', index_col=None, sheet_name=None)

map = {}

for sheet_name in df:
    print(sheet_name)

    if len(sheet_name.split(" ")) < 2:
        continue

    vol = int(sheet_name.split(" ")[0])

    obj = {}

    map[vol] = obj

    table = df[sheet_name]

    for i in range(0, len(table.index)):
        page = table.loc[i, "結果"]
        if not pd.isnull(page):
            obj[i] = {
                "page" : int(page),
                "text" : table.loc[i, "OCRテキスト"]
            }

for vol in range(50, 52):
    print(vol)
    curation_uri = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/kuronet/"+str(vol).zfill(2)+".json"

    curation_data = requests.get(curation_uri).json()

    page_text_map = map[vol]

    members2 = []

    members = curation_data["selections"][0]["members"]
    curation_data["selections"][0]["within"]["label"] = "東大本"

    members_map = {}
    for member in members:
        members_map[member["label"]] = member

    for index in page_text_map:
        # 行の重複が発生しているため、暫定的な処理

        res = page_text_map[index]
        p = res["page"]
        text = res["text"]

        member = members_map[text]

        # label = member["label"]

        member2 = {
            "@id": member["@id"],
            "@type": "sc:Canvas",
            "description": "",
            "label": "源氏物語大成 p."+str(p),
            "metadata": [
                {
                    "label": "p",
                    "value": p
                }
            ]
        }

        members2.append(member2)

    curation_data["selections"][0]["members"] = members2

    f2 = open("../../docs/iiif/fb/"+str(vol).zfill(2)+"/東大本.json", 'w')
    json.dump(curation_data, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))