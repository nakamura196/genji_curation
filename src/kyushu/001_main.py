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
import sys
import time

s_thres = 80

target = sys.argv[1]

org_flg = False if target == "kyushu" else True

margin = 10 if target == "kyushu" else 6

map = {
    "12": 395,
    "13": 441,
    "14": 483,
    "15": 519,
    "16": 547,
    "17": 557,
    "18": 579,
    "19": 603,
    "20": 639,
    "21": 665,
    "22": 719,
    "23": 763,
    "24": 781,
    "25": 805,
    "26": 829,
    "27": 855,
    "28": 863,
    "29": 885,
    "30": 917,
    "31": 935,
    "32": 975,
    "33": 997,
    "34": 1025,
    "35": 1125,
    "36": 1227,
    "37": 1269,
    "38": 1291,
    "39": 1309,
    "40": 1381,
    "41": 1403,
    "42": 1429,
    "43": 1447,
    "44": 1463,
    "45": 1507,
    "46": 1547,
    "47": 1587,
    "48": 1677,
    "49": 1701,
    "50": 1793,
    "51": 1859,
    "52": 1931,
    "53": 1989,
    "54": 2055
}

def find_rect_of_target_color(image):
  hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
  h = hsv[:, :, 0]
  s = hsv[:, :, 1]
  mask = np.zeros(h.shape, dtype=np.uint8)
  mask[((h < 20) | (h > 200)) & (s < s_thres)] = 255
  contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  rects = []
  for contour in contours:
    approx = cv2.convexHull(contour)
    rect = cv2.boundingRect(approx)
    rects.append(np.array(rect))
  return rects

def download_img(url, file_name):    
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)


def getCropStart(input_path, uuid, canvas):
    img = cv2.imread(input_path)
    rects = find_rect_of_target_color(img)
    if len(rects) > 0:
        rect = max(rects, key=(lambda x: x[2] * x[3]))
        crop_start = rect[0:2][1] - 1
    else:
        crop_start = 0
    return crop_start

def save_img2(input_path):
    img = cv2.imread(input_path)

    # グレースケール変換
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 方法2 （OpenCVで実装）
    ret, th = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    cv2.imwrite(input_path, th)


def save_crop(input_path, crop_start, canvas):
    im = Image.open(input_path)
    im = im.crop((0, crop_start, canvas["width"], canvas["height"]))
    im.save(input_path)

collection_uri = "https://nakamura196.github.io/genji/ugm/"+target+"/collection.json"

collection = requests.get(collection_uri).json()

manifests = collection["manifests"]


for manifest_data in manifests:

    manifest = manifest_data["@id"]

    uuid = manifest.split("/")[-1].split(".")[0]

    if uuid not in map:
        continue

    opath = "../../docs/iiif/curations/"+target+"/"+uuid+".json"
    if os.path.exists(opath):
        continue

    df = requests.get(manifest).json()

    canvases = df["sequences"][0]["canvases"]

    previous_page = map[uuid] - 1

    members = []
    members_raw = []

    for canvas in canvases:

        canvas_uri = canvas["@id"]

        page = canvas_uri.split("/p")[1]

        id = uuid+"_"+page

        image_url = canvas["images"][0]["resource"]["@id"]

        path = "/Users/nakamura/git/thumbnail/genji/"+target+"/" + id + ".jpg"

        # time.sleep(0.5)
        # print("start dwn\t"+image_url)
        download_img(image_url, path)
        # print("end_dwn")

        input_path = path

        # save original
        if org_flg:
            cv2.imwrite(input_path.replace(".jpg", "_org.jpg"), cv2.imread(input_path))

        # クロップ箇所の取得
        crop_start = getCropStart(input_path, uuid, canvas)

        canvas_height = canvas["height"]

        d = 13

        tmp_height = int(canvas_height * d / (d + 1))

        if crop_start < tmp_height:
            crop_start = tmp_height

        # にちがぞうの保存
        save_img2(input_path)

        # Crop
        save_crop(input_path, crop_start, canvas)

        filename = id

        dir = "data"

        pytesseract.pytesseract.run_tesseract(
            input_path, dir + "/" + filename, lang=None, config="hocr", extension="jpg")

        filepath = dir + "/" + filename+".hocr"

        with open(filepath, encoding='utf-8') as f:
            html = f.read()

        soup = BeautifulSoup(html, 'lxml')

        ocrxs = soup.find_all(class_="ocrx_word")

        

        for ocrx in ocrxs:
            text = ocrx.text

            title = ocrx.get("title").split(" ")

            x = int(title[1])
            w = int(title[3]) - x
            y = crop_start + int(title[2])
            h = crop_start + int(title[4].split(";")[0]) - y

            member_raw = {
                "@id": canvas_uri + "#xywh=" + str(x) + "," + str(y) + ","+str(w)+"," + str(h),
                "@type": "sc:Canvas",
                "description": "",
                "label": page,
                "metadata": [
                    {
                        "label": "p",
                        "value": text
                    }
                ]
            }

            members_raw.append(member_raw)

            if text.isdecimal():

                text = int(text)

                if previous_page < text and text < previous_page + 20:

                    previous_page = text

                    start_height = int(title[2])

                    print(text, id)

                    y2 = int(canvas_height / margin)
                    h2 = y - y2

                    member = {
                        "@id": canvas_uri + "#xywh=" + str(x) + "," + str(y2) + ","+str(w)+"," + str(h2),
                        "@type": "sc:Canvas",
                        "description": "",
                        "label": page,
                        "metadata": [
                            {
                                "label": "p",
                                "value": text
                            }
                        ]
                    }

                    members.append(member)

        if False and len(members) > 0:
            break

    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": "http://mp.ex.nii.ac.jp/api/curation/json/" + uuid,
        "@type": "cr:Curation",
        "label": "Curating list",
        "selections": [
            {
                "@id": "http://mp.ex.nii.ac.jp/api/curation/json/" + uuid + "/range1",
                "@type": "sc:Range",
                "label": "Manual curation by IIIF Curation Viewer",
                "members": members,
                "within": {
                    "@id": manifest,
                    "@type": "sc:Manifest",
                    "label": df["label"]
                }
            }
        ]
    }

    curation_raw = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": "http://mp.ex.nii.ac.jp/api/curation/json/" + uuid,
        "@type": "cr:Curation",
        "label": "Curating list",
        "selections": [
            {
                "@id": "http://mp.ex.nii.ac.jp/api/curation/json/" + uuid + "/range1",
                "@type": "sc:Range",
                "label": "Manual curation by IIIF Curation Viewer",
                "members": members_raw,
                "within": {
                    "@id": manifest,
                    "@type": "sc:Manifest",
                    "label": df["label"]
                }
            }
        ]
    }

    f2 = open(opath, 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))

    f2 = open(opath.replace("curations", "curations_raw"), 'w')
    json.dump(curation_raw, f2, ensure_ascii=False, indent=4,
              sort_keys=True, separators=(',', ': '))
