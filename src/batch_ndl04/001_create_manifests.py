import csv
import json
import requests
import copy
import os

arr = []

dirname = "ndl04"

collection_url = "https://utda.github.io/genji/iiif/ndl-2610583/top.json"
collection = requests.get(collection_url).json()

manifests = collection["manifests"]

for i in range(len(manifests)):
    manifest = manifests[i]["@id"]
    print(manifest)
    vol = i + 1
    df2 = requests.get(manifest).json()

    VOL = str(vol).zfill(2)

    path = "../../docs/iiif/"+dirname+"/"+VOL+".json"

    dirpath = os.path.dirname(path)

    os.makedirs(dirpath, exist_ok=True)

    f2 = open(path, 'w')
    json.dump(df2, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))
