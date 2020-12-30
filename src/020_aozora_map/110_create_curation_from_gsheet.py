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

import requests
import openpyxl

book = openpyxl.Workbook()

vols = [
    2
]

for vol in vols:
    print(vol)

    sheet = book.create_sheet(index=vol-1)

    rows = []
    rows.append(["現代語訳ID", "現代語訳テキスト", "結果", "校異源氏テキスト"])

    # 与謝野

    soup = BeautifulSoup(open('data/yosano/'+str(vol).zfill(2)+'.xml','r'), "lxml")

    # main_text.contents = all
    s_arr = soup.find_all("s")
    for s in s_arr:
        id = s.get("xml:id")
        text = s.get_text().replace(" ", "").replace("\n", "")

        print(id, text)
        rows.append([id, text, "", ""])

    # 校異

    soup = BeautifulSoup(open('data/koui/'+str(vol).zfill(2)+'.xml','r'), "lxml")

    # main_text.contents = all
    s_arr = soup.find_all("seg")
    for i in range(len(s_arr)):
        s = s_arr[i]
        id = s.get("corresp").split("/")[-1].split(".json")[0]
        text = s.get_text().replace(" ", "").replace("\n", "")

        print(id, text)

        if i + 2 > len(rows):
            rows.append(["", "", "", ""])
        rows[i+1][3] = id + " " + text

    print(rows)

    for row in rows:
        sheet.append(row)
    
book.save('data/result.xlsx')