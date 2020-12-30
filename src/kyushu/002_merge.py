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

with open('genji-5ca47-export.json') as f:
    df = json.load(f)

files = glob.glob("../../docs/iiif/curations/*/*.json")

for file in files:

    print(file)

    with open(file) as f:
        curation_data = json.load(f)

    count = len(curation_data["selections"][0]["members"])

    _createdAt = int(time.time() * 1000)

    act_db_id = str(uuid.uuid4())
    cur_db_id = str(uuid.uuid4())
    curation_id = str(uuid.uuid4())

    label = "九大本（無跋無刊記版）" if "kyushu2" in file else "九大本（古活字版）"

    vol = file.split("/")[-1].split(".")[0]

    df["activities"][act_db_id] = {
        "_createdAt": _createdAt,
        "count": count,
        "id": curation_id,
        "label": label,
        "userName": "Satoru Nakamura",
        "userPic": "https://pbs.twimg.com/profile_images/877300861252231173/kSJygg6x_normal.jpg",
        "vol": vol
    }

    selection = curation_data["selections"][0]

    manifest = selection["within"]["@id"]

    manifest_data = requests.get(manifest).json()

    selection["within"] = manifest_data

    df["curations"][cur_db_id] = {
        "_createdAt": _createdAt,
        "_updatedAt": _createdAt,
        "data": curation_data,
        "id": curation_id,
        "name": label,
        "vol": vol
    }


f2 = open("merged.json", 'w')
json.dump(df, f2, ensure_ascii=False, indent=4,
          separators=(',', ': '))
