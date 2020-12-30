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
    2 : {
        "uri" : "https://mp.ex.nii.ac.jp/api/curation/json/9124ba23-3ffa-407a-9ecb-874d6a7e6c66",
        "start" : 53,
        "end": 113
    },
    3 : {
        "uri" : "https://mp.ex.nii.ac.jp/api/curation/json/f5599c37-b10a-48ff-959a-c425b6994a95",
        "start": 117,
        "end" : 131
    },
    4 : {
        "uri" : "https://mp.ex.nii.ac.jp/api/curation/json/ad63c9ae-43ce-49a2-9e33-ca503cd0b3bc",
        "start" : 135,
        "end" : 196
    },
    5 : {
        "uri" : "https://mp.ex.nii.ac.jp/api/curation/json/efbf06db-ae28-4308-a4db-549a41f73d00",
        "start": 199,
        "end" : 262
    }
 }


for vol in man:
    obj = man[vol]

    curation = requests.get(obj["uri"]).json()

    members = curation["selections"][0]["members"]

    page = obj["start"]

    for member in members:
        member["metadata"] = [{
            "label" : "p",
            "value" : page
        }]

        member["label"] = "新編日本古典文学全集 p."+str(page)

        page += 1

    f2 = open("../../docs/iiif/saga/"+str(vol).zfill(2)+".json", 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))