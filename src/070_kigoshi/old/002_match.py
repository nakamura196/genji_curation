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

df = pd.read_excel('/Users/nakamura/git/d_genji/kouigenjimonogatari.github.io/src/data/metadata_all.xlsx', header=None, index_col=None)

configs = {}

for i in range(len(df.index)):

    uri = df.iloc[i, 0]
    if not pd.isnull(uri):
        row_num = df.iloc[i, 2]
        if int(row_num) == 1:
            title = df.iloc[i, 3]
            vol = df.iloc[i, 6]
            page = df.iloc[i, 1]

            if vol not in configs:
                configs[vol] = {
                    "data" : {}
                }

            configs[vol]["data"][title] = page

for vol in configs:

    config = configs[vol]

    koui = config["data"]

    VOL = str(vol).zfill(2)

    print(VOL)

    path = '../../docs/iiif/kuronet/'+VOL+'.json'

    if not os.path.exists(path):
        continue

    with open(path) as f:
        df = json.load(f)
        members = df["selections"][0]["members"]

    map = {}

    for line in koui:
        map[line] = []
        for i in range(len(members)):
            label = ""
            if i - 1 >= 0:
                label += members[i-1]["label"] + "／"

            member = members[i]
            label += member["label"]

            if i + 1 <= len(members) - 1:
                label += "／" + members[i+1]["label"]

            
            score = Levenshtein.distance(line, label)
            map[line].append ({
                "label" : label,
                "main" : member["label"],
                "score" : score,
                "member_id" : member["@id"],
                "index" : i
            })

    # print(map)

    # print("----------------")

    prev_index = 0

    ##################
    # members = []

    for line in map:
        # print(line)

        # print(prev_index)

        obj = map[line]

        obj = obj[prev_index:]

        score_sorted = sorted(obj, key=lambda x:x["score"])

        flg = True

        for i in range(len(score_sorted)):

            
            data = score_sorted[i]

            index = data["index"]
            
            if i < 5:
                print(data["index"], data["score"], data["member_id"], data["label"])

            if index - prev_index < 50:

                if flg:
                    print("******:")
                    prev_index = index + 1

                    table = '''
                    <table class="table">
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
                        <tr>
                            <td>大成番号</td>
                            <td>'''+str(koui[line])+'''</td>
                        </tr>
                        <tr>
                            <td>校異源氏テキスト</td>
                            <td>'''+line+'''</td>
                        </tr>
                        <tr>
                            <td>KuroNet翻刻</td>
                            <td>'''+data["main"]+'''</td>
                        </tr>
                        <tr>
                            <td>KuroNet翻刻（前後を含む3行）</td>
                            <td>'''+data["label"]+'''</td>
                        </tr>
                    </table>
                    '''

                    members.append({
                        "@id" : data["member_id"],
                        "@type": "sc:Canvas",
                        "description": "",
                        "label": "["+str(len(members) + 1)+"]",
                        "metadata": [
                            {
                                "label": "p",
                                "value": koui[line]
                            },
                            {
                                "label": "校異源氏テキスト",
                                "value": line
                            },
                            {
                                "label": "KuroNet翻刻",
                                "value": data["main"]
                            },
                            {
                                "label": "KuroNet翻刻（前後を含む3行）",
                                "value": data["label"]
                            },
                            {
                                "label": "Annotation",
                                "value": [
                                    {
                                        "@id": data["member_id"],
                                        "@type": "oa:Annotation",
                                        "motivation": "sc:painting",
                                        "resource": {
                                            "@type": "cnt:ContentAsText",
                                            "chars": table,
                                            "format": "text/html",
                                            "marker": {
                                                "border-color": "red"
                                            }
                                        },
                                        "on": data["member_id"]
                                    }
                                ]
                            }
                        ]
                    })

                    flg = False

        print("----------------")

    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": df["@id"],
        "@type": "cr:Curation",
        "label": "Character List",
        "selections": [
            {
                "@id": df["@id"] + "/range1",
                "@type": "sc:Range",
                "label": "Characters",
                "members": members,
                "within" : df["selections"][0]["within"]
            }
        ]
    }

    f2 = open(path.replace("/kuronet/", "/taisei/"), 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))