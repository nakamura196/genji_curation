import requests
from bs4 import BeautifulSoup
import re
from bs4 import BeautifulSoup

import requests
import openpyxl

import pandas as pd

df = pd.read_excel('data/map.xlsx', index_col=None, sheet_name=None)

map = {}

for sheet_name in df:
    print(sheet_name)

    table = df[sheet_name]

    for i in range(0, len(table.index)):
        old_id = table.loc[i, "old_id"]
        if not pd.isnull(old_id):
            map[old_id] = table.loc[i, "new_id"]

with open("data/replace/01_koui_yosano.xml") as f:
    s = f.read()

    for key in map:
        if not pd.isnull(map[key]):
            s = s.replace(key, map[key])

    with open("data/replace/01_koui_yosano_replace.xml", mode='w') as f:
        f.write(s)
    