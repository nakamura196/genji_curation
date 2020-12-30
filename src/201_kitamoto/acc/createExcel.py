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

name = "taisei_all"

name = "湖月抄・NIJL・鵜飼文庫本への大成番号付与"

df = pd.read_excel('data/'+name+'.xlsx', index_col=None, sheet_name=None)

map = {}

for sheet_name in df:
    

    if len(sheet_name.split(" ")) < 2:
        continue

    vol = int(sheet_name.split(" ")[0])

    '''
    if vol != 34:
        continue
    '''

    print(sheet_name)

    map[vol] = {
        "h" : {},
        "m" : {}
    }

    obj = map[vol]

    table = df[sheet_name]

    for i in range(0, len(table.index)):
        m_page = table.loc[i, "大成番号"]

        if not pd.isnull(m_page) and "脱文あり" not in str(m_page) and "自信なし" not in str(m_page) and "多分" not in str(m_page):
            obj["m"][int(m_page)] = i

name = "大成番号付与"
name = "湖月抄・NIJL・鵜飼文庫本への大成番号付与"

df = pd.read_excel('data/'+name+'.xlsx', index_col=None, sheet_name=None)

for sheet_name in df:
    

    if len(sheet_name.split(" ")) < 2:
        continue

    vol = int(sheet_name.split(" ")[0])

    if name == "湖月抄・NIJL・鵜飼文庫本への大成番号付与" and vol > 23:
        continue

    print(sheet_name)

    obj = map[vol]

    table = df[sheet_name]

    for i in range(0, len(table.index)):
        h_page = table.loc[i, "結果"]
        if not pd.isnull(h_page):
            obj["h"][int(h_page)] = i

    point = 0

    for h_page in obj["h"]:
        h_row = obj["h"][h_page]

        if h_page in obj["m"]:
            m_row = obj["m"][h_page]

            if h_row <= m_row + 1 and h_row >= m_row - 1:
                point += 1

    obj["a"] = point
    obj["size"] = len(obj["h"])

rows = []
rows.append(["巻", "正解数", "頁数", "精度"])

for vol in map:
    obj = map[vol]

    if "a" not in obj:
        continue
    
    a = obj["a"]
    s = obj["size"]
    row = [vol, a, s, a /s * 100]
    rows.append(row)

df = pd.DataFrame(rows)

# convert from pandas data to excel
writer = pd.ExcelWriter('data/result_'+name+'.xlsx', options={'strings_to_urls':False})
df.to_excel(writer,index=False, header=False)
writer.close()
