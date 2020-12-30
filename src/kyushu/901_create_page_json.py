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
    vol = int(df_item.iloc[i, 0])
    n = df_item.iloc[i, 3]
    koui = "https://dl.ndl.go.jp/info:ndljp/pid/" + str(df_item.iloc[i, 4]) + "/" + str(df_item.iloc[i, 5])
    map[vol] = {
        "size" : int(n),
        "koui" : koui,
        "start" : int(df_item.iloc[i, 1]),
        "end" : int(df_item.iloc[i, 2]),
     }


f2 = open("pages.json", 'w')
json.dump(map, f2, ensure_ascii=False, indent=4,
          separators=(',', ': '))