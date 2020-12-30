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

start_map = {
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

start_r_map = {}

start_arr = []

for key in start_map:
    start_arr.append({
        "vol" : key,
        "text" : start_map[key]
    })

    start_r_map[start_map[key]] = key

print(start_arr)

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

        '''
        if len(line) < 10:
            # line = prev_line + line
            line += df[ids[k+1]]
        '''

        # sss = id.split("-")

        if id in start_r_map:
            VOL_ = start_r_map[id]

        # print(sss)

        # "先頭行ならば"
        # if sss[2] == "01":
        '''
        for j in range(len(arr)):
            if arr[j]["text"] <= id and id < (arr[j+1]["text"] if j < len(arr)-1 else "999999999999999999999"):
                VOL_ = arr[j]["vol"]
                # print(VOL_)
                break
        '''

        # print("vol", VOL_)

        if VOL_ not in configs:
            configs[VOL_] = {
                # "data" : {}
            }

        # line = id + " " + line

        # configs[VOL_]["data"][line] = id # int(sss[1])
        configs[VOL_][id] = line

        # prev_line = line


'''
for vol in configs:
    print(vol)
    print(configs[vol]["data"])
    print("------------")
'''

### configs : 新編の
### vol毎のID毎のテキスト

print(configs[35])

################################################

def convert_line(line, prev_line):

    text = line

    if len(text) < 10:
        text = prev_line + text
        print("######## 文字数が少ない行", prev_line, line)

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

    return text

def convert_ocr(line, prev):
    aaa = "がぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽ"
    bbb = "かきくけこさしすせそたちつてとはひふへほはひふへほ"

    label = ""

    # -1行
    if prev != "":
        label += prev + "／"

    # 該当行
    label += line

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

    return label, text2


def main():

    rows = []
    rows.append(["新編日本古典文学全集・テキスト", "KuroNet翻刻", "KuroNet翻刻（前行を含む）", "巻", "ID"])

    line = "磯づたひせず　とてはしたなかめりとや"
    # line = "とてはしたなかめりとや"
    # line = "く中〱なりとおほすとさま"
    # line = "いそづたひせずとてはしたなかめりとや"
    # line = "よるべなみ風のさわがす舟人も思はぬかたに磯づた"

    text = convert_line(line, "")

    print(text)

    map = {}
    map[line] = []

    # print(configs)

    count = 0

    for vol in configs:

        config = configs[vol]

        print(config)

        # koui = config["data"]

        VOL = str(vol).zfill(2)

        
        if VOL != "35" and False:
            continue
        

        print(VOL)

        path = '../../docs/iiif/kuronet/'+VOL+'.json'

        if not os.path.exists(path):
            continue

        with open(path) as f:
            df = json.load(f)
            members = df["selections"][0]["members"]



        ################## マッチング

        

        indexedObj = {}

        prev_line = ""
        

        for i in range(len(members)):

            member = members[i]

            prev_label = ""

            # -1行
            if i - 1 >= 0:
                prev_label = members[i-1]["label"]
            
            label, text2 = convert_ocr(members[i]["label"], prev_label)

            print(VOL, i, text, text2)
            
            score = Levenshtein.distance(text, text2)
            score = score / max(len(text), len(text2)) # 正規化

            obj = {
                "label" : label,
                "main" : member["label"],
                "score" : score,
                "member_id" : member["@id"],
                "index" : i,
                "vs" : "【新編】" + text + "---【OCR】" + text2,
                "vol" : VOL
            }

            map[line].append (obj)

            indexedObj[count] = obj

            count += 1


    ##################　集計

    size = len(map)

    count = 0

    # 校異のライン毎に
    for line in map:

        count += 1

        print(count, size)

        # print(str(koui[line])+"\t"+line)

        obj = map[line]

        # スコアが小さい順に並び替え
        score_sorted = sorted(obj, key=lambda x:x["score"])

        flg = True

        for i in range(len(score_sorted)):

            data = score_sorted[i]

            if i < 25:
                print(data)

                row = [line, data["main"], data["label"], data["vol"], data["member_id"]]
                rows.append(row)

    df = pd.DataFrame(rows)

    df.to_excel('data/check.xlsx',index=False, header=False)


main()