import pytesseract
import requests
from bs4 import BeautifulSoup
import shutil
import hashlib
import os
import json
import cv2
import numpy as np
from PIL import Image

import uuid
import time
import glob
import pandas as pd
import csv

df_item = pd.read_excel("pages.xlsx", sheet_name="Sheet1", header=None, index_col=None)

map = {}

for i in range(1, len(df_item.index)):
    vol = df_item.iloc[i, 0]
    n = df_item.iloc[i, 3]
    map[vol] = int(n)


files = sorted(glob.glob("../../docs/iiif/curations/*/*.json"))

result = {}

rows = []
rows.append(["vol", "k - 九大本（古活字版）", "m - 九大本（無跋無刊記版）"])

for file in files:

    with open(file) as f:
        curation_data = json.load(f)

    vol = int(file.split("/")[-1].split(".")[0])

    count = len(curation_data["selections"][0]["members"])

    p = int(count / map[vol] * 100)

    if p > 100:
        p = 101

    if vol not in result:
        result[vol] = [-1, -1]
    
    if "kyushu2" in file:
        result[vol][1] = p
    else:
        result[vol][0] = p

for vol in sorted(result):
    obj = result[vol]
    print(vol, obj)
    if len(obj) == 1:
        obj = ["-1", obj[0]]
    row = [vol, obj[0], obj[1]]
    rows.append(row)

f = open("check.csv", 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()
