import bs4
import requests
from urllib.parse import urljoin
import uuid
import json
import pandas as pd
import openpyxl

confs = [
    ["12 すま", 12, 391],
    ["13 あかし", 13, 437],
    ["14 みをつくし", 14, 479],
    ["15 よもきふ", 15, 515],
    ["16 せきや", 16, 543],
    ["17 ゑあはせ", 17, 553],
    ["18 松かせ", 18, 575],
    ["19 うす雲", 19, 599],
    ["20 あさかほ", 20, 635],
    ["21 をとめ", 21, 661],
    ["22 玉かつら", 22, 715],
    ["23 初音", 23, 759],
    ["24 こてふ", 24, 777],
    ["25 ほたる", 25, 801],
    ["26 とこなつ", 26, 825],
    ["27 かゝり火", 27, 851],
    ["28 野わき", 28, 859],
    ["29 みゆき", 29, 881],
    ["30 藤はかま", 30, 913],
    ["31 まきはしら", 31, 931],
    ["32 梅かえ", 32, 971],
    ["33 藤のうらは", 33, 993],
    ["34 わかな上", 34, 1021],
    ["35 わかな下", 35, 1121],
    ["36 かしは木", 36, 1223],
    ["37 よこ笛", 37, 1265],
    ["38 すゝむし", 38, 1287],
    ["39 夕きり", 39, 1305],
    ["40 みのり", 40, 1377],
    ["41 まほろし", 41, 1399],
    ["42 にほふ兵部卿", 42, 1425],
    ["43 こうはい", 43, 1443],
    ["44 たけ川", 44, 1459],
    ["45 はし姬", 45, 1503],
    ["46 しゐかもと", 46, 1543],
    ["47 あけまき", 47, 1583],
    ["48 さわらひ", 48, 1673],
    ["49 やとり木", 49, 1697],
    ["50 あつまや", 50, 1789],
    ["51 うき舟", 51, 1855],
    ["52 かけろふ", 52, 1927],
    ["53 てならひ", 53, 1985],
    ["54 夢のうきはし", 54, 2051]
]

itaiji = {}

import csv

with open('data2/itaiji.csv', 'r') as f:
    reader = csv.reader(f)
    header = next(reader)

    for row in reader:
        key = row[1]
        text = row[2]
        elements = text.split("　")
        for e in elements:
            itaiji[e] = key

rows = []

for conf in confs:
    title = conf[0]
    vol = conf[1]
    start_page = conf[2] + 4

    print(vol)

    file = "data/"+title+".json"

    with open(file, 'r') as f:
        data = json.load(f)

        members = data["selections"][0]["members"]

        manifest = data["selections"][0]["within"]["@id"]

        for i in range(len(members)):
            member = members[i]

            text = member["metadata"][0]["value"].split("\n")

            canvas_uri = member["@id"].split("#")[0]

            canvas_id = canvas_uri.split("/")[-1]
            # page = start_page + (canvas_id - start_canvas)

            line_num = 1

            for line in text:

                if line.strip() != "":

                    line = line.strip()

                    for key in itaiji:
                        line = line.replace(key, itaiji[key])

                    row = [
                        "https://w3id.org/kouigenjimonogatari/data/" + str(start_page).zfill(4) + "-" + str(line_num).zfill(2) + ".json",
                        start_page,
                        line_num,
                        line,
                        "http://creativecommons.org/publicdomain/zero/1.0/",
                        title,
                        vol,
                        "源氏物語",
                        "https://jpsearch.go.jp/term/type/文章要素",
                        "",
                        "",
                        canvas_id,
                        canvas_uri,
                        manifest,
                        "http://da.dl.itc.u-tokyo.ac.jp/mirador/?params=[{%22manifest%22:%22"+manifest+"%22,%22canvas%22:%22"+canvas_uri+"%22}]"
                    ]

                    rows.append(row)

                    line_num += 1
                else:
                    # 空行の場合
                    line_num = 1
                    start_page += 1

            
            start_page += 1


df = pd.DataFrame(rows)

# convert from pandas data to excel
writer = pd.ExcelWriter('data2/result.xlsx', options={'strings_to_urls':False})
df.to_excel(writer,index=False, header=False)
writer.close()
