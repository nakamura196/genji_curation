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
import re

tmp = {
    1: "001-017-01",
    2: "001-053-01",
    3: "001-117-01",
    4: "001-135-01",
    5: "001-199-01",
    6: "001-265-01",
    7: "001-311-01",
    8: "001-353-01",


    9: "002-017-01",
    10: "002-083-01",
    11: "002-153-01",
    12: "002-161-01",
    13: "002-223-01",
    14: "002-279-01",
    15: "002-325-01",
    16: "002-359-01",
    17: "002-369-01",
    18: "002-397-01",
    19: "002-427-01",
    20: "002-469-01",

    21: "003-017-01",
    22: "003-087-01",
    23: "003-143-01",
    24: "003-165-01",
    25: "003-195-01",
    26: "003-223-01",
    27: "003-255-01",
    28: "003-263-01",
    29: "003-289-01",
    30: "003-327-01",

    31: "003-349-01",
    32: "003-403-01",
    33: "003-431-01",
    34: "004-017-01",
    35: "004-153-01",
    36: "004-289-01",
    37: "004-345-01",
    38: "004-373-01",
    39: "004-395-01",
    40: "004-493-01",


    41: "004-521-01",
    42: "005-017-01",
    43: "005-039-01",
    44: "005-059-01",
    45: "005-117-01",
    46: "005-169-01",
    47: "005-223-01",
    48: "005-345-01",
    49: "005-373-01",
    50: "006-017-01",


    51: "006-105-01",
    52: "006-201-01",
    53: "006-279-01",
    54: "006-373-01"
}

arr = []

for key in tmp:
    arr.append({
        "vol" : key,
        "text" : tmp[key]
    })

print(arr)

configs = {}

path = "/Users/nakamura/git/d_genji/genji_private/src/org/saga/data/data_mod.json"

with open(path) as f:
    
    df = json.load(f)

    VOL_ = -1

    prev_line = ""

    ids = list(df.keys())

    for k in range(len(ids)):
        id = ids[k]

        # for id in df:
        line = df[id]
        # print("id", id)

        if len(line) < 10:
            # line = prev_line + line
            line += df[ids[k+1]]

        sss = id.split("-")
        # print(sss)

        # "先頭行ならば"
        if sss[2] == "01":
            for j in range(len(arr)):
                if arr[j]["text"] <= id and id < (arr[j+1]["text"] if j < len(arr)-1 else "999999999999999999999"):
                    VOL_ = arr[j]["vol"]
                    # print(VOL_)
                    break

            # print("vol", VOL_)

            if VOL_ not in configs:
                configs[VOL_] = {
                    "data" : {}
                }

            configs[VOL_]["data"][line] = int(sss[1])

        prev_line = line

'''
for vol in configs:
    print(vol)
    print(configs[vol]["data"])
    print("------------")
'''

# print(configs)

for vol in configs:

    config = configs[vol]

    koui = config["data"]

    VOL = str(vol).zfill(2)

    
    if VOL != "35" and True:
        continue
    

    print(VOL)

    path = '../../docs/iiif/kuronet/'+VOL+'.json'

    if not os.path.exists(path):
        continue

    with open(path) as f:
        df = json.load(f)
        members = df["selections"][0]["members"]

    ################## マッチング

    map = {}

    indexedObj = {}

    prev_line = ""

    for line in koui:
        map[line] = []

        # 新編テキストの修正

        text = line

        if len(text) < 10:
            print(line)
            text = prev_line + text
            print(prev_line, line)
            print("########")

        text = text.replace("「", "").replace("」", "").replace("、", "").replace("。", "")
        text = re.sub('（.*）', '', text)

        aaa = "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
        bbb = "かきくけこさしすせそたちつてとはひふへほはひふへほ"

        for j in range(len(aaa)):
            text = text.replace(aaa[j], bbb[j])

        ccc = {
            "今日" : "けう",
            "明日" : "あす"
        }

        for c in ccc:
            text = text.replace(c, ccc[c])

        prev_line = line

        ########

        for i in range(len(members)):
            label = ""

            # -1行
            if i - 1 >= 0:
                label += members[i-1]["label"] + "／"

            # 該当行
            member = members[i]
            label += member["label"]

            # +1行
            '''
            if i + 1 <= len(members) - 1:
                label += "／" + members[i+1]["label"]
            '''

            # OCR
            text2 = label.replace("／", "")

            ccc = {
                "侍": "はへ",
                "哀" : "あはれ",
                "給" : "たま",
                "物" : "もの",
                
            }

            for c in ccc:
                text2 = text2.replace(c, ccc[c])

            for j in range(len(aaa)):
                text2 = text2.replace(aaa[j], bbb[j])
            
            score = Levenshtein.distance(text, text2)
            score = score / max(len(text), len(text2)) # 正規化

            obj = {
                "label" : label,
                "main" : member["label"],
                "score" : score,
                "member_id" : member["@id"],
                "index" : i,
                "vs" : "【新編】" + text + "---【OCR】" + text2
            }

            map[line].append (obj)

            indexedObj[i] = obj

    ##################　集計

    prev_index = 0

    INTERVAL_a = 50 #20
    INTERVAL_b = 10
    type = "b"

    # 校異のライン毎に
    for line in map:
        print(str(koui[line])+"\t"+line)

        print("prev_index", prev_index)

        obj = map[line]

        obj = obj[prev_index:]

        # スコアが小さい順に並び替え
        score_sorted = sorted(obj, key=lambda x:x["score"])

        flg = True

        for i in range(len(score_sorted)):

            
            data = score_sorted[i]

            index = data["index"]
            
            '''
            if i < 10:
                print(i, data["index"], round(data["score"], 2), data["member_id"].split("/canvas/")[1], data["label"])
                print(data["vs"])
            '''

            dist = index - prev_index

            if (prev_index == 0 or INTERVAL_b / 2 < dist) and dist < INTERVAL_a or True:                

                if flg:
                    # print("******:")
                    
                    ###################################
                    # prev_index = index + 1

                    # if prev_index - 1 < len(obj):
                    #    data = obj[prev_index - 1]

                    index = data["index"]
                    if index > 0:
                        data = indexedObj[index - 1]

                    member_id = data["member_id"]
                    sss = member_id.split("#xywh=")

                    canvas_id = sss[0]
                    xywh = sss[1].split(",")

                    d = 5

                    y = int(int(xywh[1]) * d / (d+1))

                    data["member_id"] = canvas_id+"#xywh="+xywh[0]+","+str(y)+","+xywh[2]+",1"

                    table = '''
                    <table class="table">
                        <tr>
                            <th>項目</th>
                            <th>値</th>
                        </tr>
                        <tr>
                            <td>新編日本古典文学全集・番号</td>
                            <td>'''+str(koui[line])+'''</td>
                        </tr>
                        <tr>
                            <td>新編日本古典文学全集・テキスト</td>
                            <td>'''+line+'''</td>
                        </tr>
                        <tr>
                            <td>KuroNet翻刻</td>
                            <td>'''+data["main"]+'''</td>
                        </tr>
                        <tr>
                            <td>KuroNet翻刻（前行を含む）</td>
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
                                "label": "編日本古典文学全集テキスト",
                                "value": line
                            },
                            {
                                "label": "KuroNet翻刻",
                                "value": data["main"]
                            },
                            {
                                "label": "KuroNet翻刻（前行を含む）",
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
                                                "border-color": "red",
                                                "@type": "dctypes:Image",
                                                "@id": "https://nakamura196.github.io/genji_curation/icon/red.png#xy=16,16"
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

    f2 = open(path.replace("/kuronet/", "/121_saga/"), 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))