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

files = glob.glob("../../docs/iiif/kuronet/*.json")

for file in files:
    with open(file, 'r') as f:

        vol_str = file.split("/")[-1].split(".")[0]

        data = json.load(f)

        rows = []

        members = data["selections"][0]["members"]

        for member in members:
            label = member["label"]
            rows.append([label])

        with open('data/old/'+vol_str+'.csv', 'w') as f:
            writer = csv.writer(f, lineterminator='\n') # 改行コード（\n）を指定しておく
            writer.writerows(rows) # 2次元配列も書き込める
        
