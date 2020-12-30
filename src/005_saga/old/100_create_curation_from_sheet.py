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

vol = 6

curation_uri = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/kuronet/"+str(vol).zfill(2)+".json"

curation_data = requests.get(curation_uri).json()

page_text_map = {}

with open('data/'+str(vol)+".csv", 'r') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時

    index = 0

    for row in reader:
        if row[1] != "":
            page_text_map[index] = int(row[1])

        index += 1

members2 = []

members = curation_data["selections"][0]["members"]

for index in page_text_map:
    member = members[index]

    p = int(page_text_map[index])

    member2 = {
        "@id": member["@id"],
        "@type": "sc:Canvas",
        "description": "",
        "label": "新編日本古典文学全集 p."+str(p),
        "metadata": [
            {
                "label": "p",
                "value": p
            }
        ]
    }

    members2.append(member2)

curation_data["selections"][0]["members"] = members2

f2 = open("../../docs/iiif/saga/"+str(vol).zfill(2)+".json", 'w')
json.dump(curation_data, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))