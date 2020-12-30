import sys
import urllib
import json
import argparse
import urllib.request
import unicodedata
import collections
import os
import xml.etree.ElementTree as ET
import csv
import glob
import urllib.parse

csv_file = open("data/genjitext.csv")

f = csv.reader(csv_file, delimiter=",")
header = next(f)
print(header)

map = {}

for row in f:
    #rowはList
    #row[0]で必要な項目を取得することができる
    print(row)

    id = row[0].split("/")[1]
    text = row[1]

    id_spl = id.split("_")

    # print(id_spl[0])

    vol = int(id_spl[0])

    if vol not in map:
        map[vol] = []

    text = text.replace("\"", "")
    print(text)

    map[vol].append([text])

# print(map)

for vol in map:
    vol_str = str(vol).zfill(2)

    with open('data/new/'+vol_str+'.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
        writer.writerows(map[vol]) # 2次元配列も書き込める



'''
files = []
files2 = glob.glob("../../docs/iiif/kuronet/*.json")

for f in files2:
    files.append(f)

files2 = glob.glob("../../docs/iiif/nijl_kuronet/*.json")

for f in files2:
    files.append(f)

pages = []
total = 0

for file in sorted(files):

    with open(file, 'r') as f:
        data = json.load(f)

        members = data["selections"][0]["members"]

        for member in members:
            page = member["@id"].split("#xywh=")[0]
            text = member["label"]

            size = len(text)

            total += size

            if page not in pages:
                pages.append(page)

print("pages", len(pages))
print("total", total)
'''