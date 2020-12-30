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

path = "data/ほぼ揃い(50冊以上)源氏物語_NIJLrev.xlsx"

df = pd.read_excel(path, sheet_name="ほぼ揃い源氏", header=None, index_col=None)

genji_dir = "/Users/nakamurasatoru/git/d_genji"

r_count = len(df.index)
c_count = len(df.columns)

print(r_count)

collections = []

prefix = "https://utda.github.io/genji"

for j in range(1, r_count):
    url = str(df.iloc[j, 4])

    manifest = str(df.iloc[j, 6])
    print(manifest)

    try:

        headers = {"content-type": "application/json"}
        r = requests.get(manifest, headers=headers)
        data = r.json()

        type_ = "sc:Manifest"
        if prefix in manifest:
            type_ = "sc:Collection"

        description = ""
        value = df.iloc[j, 3]
        if not pd.isnull(value) and value != 0:
            description = value

        collections.append(
            {
                "@id": manifest,
                "@type": type_,
                "label": data["label"],
                "description": str(df.iloc[j, 0]),
                "license": str(df.iloc[j, 5]),
                "type": str(df.iloc[j, 1]),
                "volume": str(df.iloc[j, 2]),
                "note": description
            }
        )
    except Exception as e:
        print(e)

collection_data = {
  "@context": "http://iiif.io/api/presentation/2/context.json",
  "@id": prefix + "/iiif/collection/top.json",
  "@type": "sc:Collection",
  "label": "IIIF対応源氏物語リスト",
  "collections": collections
}


with open(genji_dir + "/genji/static/iiif/collection/top.json", 'w') as f:
    json.dump(collection_data, f, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
