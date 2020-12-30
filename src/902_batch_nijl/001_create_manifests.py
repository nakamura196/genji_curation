import csv
import json
import requests
import copy

'''
    {
        "vol" : 4,
        "label" : "夕顔",
        "start" : 106,
        "end" : 162
    },
    {
        "vol" : 5,
        "label" : "若紫",
        "start" : 163,
        "end" : 219
    },
    {
        "vol" : 6,
        "label" : "末摘花",
        "start" : 220,
        "end" : 259
    },
    {
        "vol" : 7,
        "label" : "紅葉賀",
        "start" : 260,
        "end" : 294
    },
    {
        "vol" : 8,
        "label" : "花宴",
        "start" : 295,
        "end" : 311
    },
    {
        "vol" : 9,
        "label" : "葵",
        "start" : 312,
        "end" : 367
    },
    {
        "vol" : 10,
        "label" : "賢木",
        "start" : 368,
        "end" : 428
    },
    {
        "vol" : 11,
        "label" : "花散里",
        "start" : 429,
        "end" : 438
    },
    {
        "vol" : 12,
        "label" : "須磨",
        "start" : 439,
        "end" : 491
    },
    {
        "vol" : 13,
        "label" : "明石",
        "start" : 492,
        "end" : 542
    },
    {
        "vol" : 14,
        "label" : "澪標",
        "start" : 543,
        "end" : 583
    },
    {
        "vol" : 15,
        "label" : "蓬生",
        "start" : 584,
        "end" : 613
    },
    {
        "vol" : 16,
        "label" : "関屋",
        "start" : 614,
        "end" : 624
    },
    {
        "vol" : 17,
        "label" : "絵合",
        "start" : 625,
        "end" : 651
    }
'''

arr = [
   
    
]

with open('data/巻の分割 - 国文学研究資料館 鵜飼文庫.csv') as f:
    reader = csv.reader(f)
    header = next(reader)  # ヘッダーを読み飛ばしたい時
    for row in reader:
        
        arr.append({
            "vol" : int(row[0]),
            "label" : row[1],
            "start" : int(row[2]),
            "end" : int(row[3])
        })


path = "data/manifest.json"

with open(path) as f:
    df = json.load(f)
canvases = df["sequences"][0]["canvases"]

for obj in arr:
    df2 = copy.deepcopy(df) #変更行
    df2["label"] = obj["label"]
    df2["sequences"][0]["canvases"] = canvases[obj["start"] - 1 : obj["end"]]

    VOL = str(obj["vol"]).zfill(2)

    f2 = open("../../docs/iiif/nijl/"+VOL+".json", 'w')
    json.dump(df2, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))

