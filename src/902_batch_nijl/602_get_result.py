import json
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
import os
import glob
from lxml import etree
import sys
import requests
import hashlib
import difflib
import time
import urllib

manifests = []

for i in range(1, 55):
    manifests.append("https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/"+str(i).zfill(2)+".json")

'''
manifests = [
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/01.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/02.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/03.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/04.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/05.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/06.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/07.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/08.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/09.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/10.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/11.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/12.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/13.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/14.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/15.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/16.json",
    "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/nijl/17.json"
]
'''

# htmlをBeautifulSoupで扱う
soup = BeautifulSoup(open("data/result.html"), "lxml")

tr_list = soup.find_all("tr")

rows = []
rows.append(["manifest", "canvas", "curation"])

print(len(tr_list))

for i in range(1, len(tr_list)):
    print(i)
    tds = tr_list[i].find_all("td")

    # print(tds)

    a = tds[1].find("a")

    '''
    print(a)

    if a == None:
        continue
    '''

    url_1 = a.get("href").split("?")[1].split("&")
    manifest = url_1[0].split("=")[1]

    
    if manifest not in manifests:
        continue


    canvas = url_1[1].split("=")[1]

    a_arr = tds[3].find_all("a")
    if len(a_arr) < 2:
        continue

    a = a_arr[1]

    if a == None:
        continue
    
    curation = a.get("href").split("=")[1]

    rows.append([manifest, canvas, curation])

import csv

f = open('data/result.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(rows)

f.close()