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