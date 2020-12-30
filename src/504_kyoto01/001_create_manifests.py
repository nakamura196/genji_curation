import csv
import json
import requests
import copy
import os

arr = []

dirname = "kyoto01"
manifest_uri = "https://kotenseki.nijl.ac.jp/biblio/100153620/manifest"

with open('data/map.csv') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時
    for row in reader:

        if row[2] != "":
        
            arr.append({
                "vol" : int(row[0]),
                "label" : row[1],
                "start" : int(row[2]),
                "end" : int(row[3])
            })



df = requests.get(manifest_uri).json()
canvases = df["sequences"][0]["canvases"]

for obj in arr:
    df2 = copy.deepcopy(df) #変更行
    df2["label"] = obj["label"]
    df2["sequences"][0]["canvases"] = canvases[obj["start"] - 1 : obj["end"]]

    VOL = str(obj["vol"]).zfill(2)

    path = "../../docs/iiif/"+dirname+"/"+VOL+".json"

    dirpath = os.path.dirname(path)

    os.makedirs(dirpath, exist_ok=True)

    f2 = open(path, 'w')
    json.dump(df2, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

