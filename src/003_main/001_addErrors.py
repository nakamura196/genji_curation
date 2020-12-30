import pandas as pd
import requests
import json
import os
import xml.etree.ElementTree as ET
import time
import glob



genji_dir = "/Users/nakamurasatoru/git/d_genji"

data = {}

with open(genji_dir + "/genji/static/data/ds.json") as f:
    df = json.load(f)

    selections = df["selections"]

    for selection in selections:
        members = selection["members"]

        for member in members:
            # print(member)

            metadata = member["metadata"]

            map = {}

            for i in range(len(metadata)):
                m = metadata[i]
                map[m["label"]] = m["value"]

            map["id"] = member["@id"]

            # print(map)

            vol = map["Vol"]

            if vol not in data:
                data[vol] = []

            data[vol].append(map)

# print(data)

files = glob.glob(genji_dir+"/genji_curation/docs/iiif/fb/*/東大本.json")

for file in files:
    with open(file) as f:
        df = json.load(f)

    vol = file.split("/fb/")[1].split("/")[0]
    vol = str(int(vol))

    
    
    if vol in data:
        arr = data[vol]
        members = df["selections"][0]["members"]
        for obj in arr:

            metadata = []

            for key in obj:
                if key != "id":
                    metadata.append({
                        "label" : key,
                        "value" : obj[key]
                    })

            member = {
                "@id": obj["id"],
                "@type": "sc:Canvas",
                "description": "",
                "label": "脱文・錯簡",
                "metadata": metadata
            }

            

            members.append(member)

    fw = open(file.replace("/fb/", "/fb2/"), 'w')
    json.dump(df, fw, ensure_ascii=False, indent=4, separators=(',', ': '))



# print(df)
