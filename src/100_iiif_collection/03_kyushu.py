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

id = "kyushu-mu"
collection_label = "九大本（無跋無刊記整版本）"

for i in range(1, 55):
    manifest = "https://utda.github.io/genji/data/iiif/org/"+collection_label+"/"+str(i).zfill(2)+"/manifest.json"

    print(manifest)

    try:
        m_data = requests.get(manifest).json()
    except Exception as e:
        print(i, e)

    thumbnail = m_data["thumbnail"]["@id"]

    thumbnail_split = thumbnail.split("/")
    id1 = thumbnail_split[5]
    id2 = thumbnail_split[6]

    new_manfiest = "https://catalog.lib.kyushu-u.ac.jp/image/manifest/"+id1+"/"+id2+".json"

    manifests.append({
        "@id": new_manfiest,
        "@type": "sc:Manifest",
        "attribution": "Kyushu University Library Collections",
        "label": "源氏物語",
        "license": "https://www.lib.kyushu-u.ac.jp/reuse",
        "thumbnail": thumbnail
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
