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

curation = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/pt/image_map.json").json()

members = curation["selections"][1]["members"]

members2 = []

for member in members:
    labels = member["label"].split(" ")

    if labels[0] == "新編日本古典文学全集":
        member["metadata"] = [{
            "label" : "p",
            "value" : int(labels[1].split(".")[1])
        }]

        members2.append(member)

curation_uri = "https://nakamura196.github.io/genji_curation/saga/01.json"

curation2 = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": curation_uri,
    "@type": "cr:Curation",
    "label": "Character List",
    "selections": [
        {
            "@id": curation_uri + "/range1",
            "@type": "sc:Range",
            "label": "Manual curation by IIIF Curation Viewer",
            "members": members2,
            "within": {
                "@id": "https://nakamura196.github.io/genji/ugm/utokyo/manifest/01.json",
                "@type": "sc:Manifest",
                "label": "きりつぼ"
            }
        }
    ]
}


f2 = open("../../docs/iiif/saga/"+str("01").zfill(2)+".json", 'w')
json.dump(curation2, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))