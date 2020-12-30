import pandas as pd
import numpy as np
import math
import sys
import argparse
import json
from urllib import request
from bs4 import BeautifulSoup
import hashlib
import os
import requests

import csv

genji_dir = "/Users/nakamurasatoru/git/d_genji"

prefix = "https://utda.github.io/genji"

manifests = []

id = "utokyo"
collection_label = "東大本"

for i in range(1, 55):
    manifest = "https://utda.github.io/genji/data/iiif/org/東大本/"+str(i).zfill(2)+"/manifest.json"

    print(manifest)

    try:
        m_data = requests.get(manifest).json()
    except Exception as e:
        print(i, e)

    uuid = m_data["related"].split("/")[-1]

    metadata = m_data["metadata"]

    label = m_data["label"]

    for m in metadata:
        if m["label"] == "Title":
            label = m["value"]

    manifests.append({
        "@id": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/"+uuid+"/manifest",
        "@type": "sc:Manifest",
        "attribution": "東京大学総合図書館 General Library, The University of Tokyo, JAPAN",
        "label": label,
        "license": m_data["license"],
        "thumbnail": m_data["thumbnail"]
    })        

collection = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": prefix + "/iiif/"+id+"/top.json",
    "@type": "sc:Collection",
    "label": collection_label,
    "manifests" : manifests,
    "vhint": "use-thumb"
}

opath = genji_dir + "/genji/static/iiif/"+id+"/top.json"
dirname = os.path.dirname(opath)

os.makedirs(dirname, exist_ok=True)

with open(opath, 'w') as f:
    json.dump(collection, f, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
