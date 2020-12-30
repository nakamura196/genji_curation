import time
# モジュールのインポート
from bs4 import BeautifulSoup
import requests
import yaml
import json
import hashlib
import os
import glob

def getLine(start, map):
    text = ""
    uri = start
    flg = True

    x_min = 1000000000
    y_min = 1000000000
    x_max = -1
    y_max = -1

    while flg:

        obj = map[uri]

        text += obj["text"]

        x = int(obj["xywh"][0])
        y = int(obj["xywh"][1])
        xw = x + 1
        yh = y + 1

        if x < x_min:
            x_min = x
        if y < y_min:
            y_min = y
        if xw > x_max:
            x_max = xw
        if yh > y_max:
            y_max = yh

        if "next" not in obj:
            flg = False
        else:
            uri = obj["next"]

    member_id = obj["canvas_id"].split("#xywh=")[0] + "#xywh=" + ",".join([str(x_min), str(y_min), str(x_max - x_min), str(y_max - y_min)])

    member = {
        "@id": member_id,
        "@type": "sc:Canvas",
        "label": text,
        "metadata": [
            {
                "label": "Text",
                "value": text
            }
        ]
    }

    return member, obj["canvas_id"], x_min

def getText(start, map, members):
    member, canvas_id, x = getLine(start, map)
    if canvas_id not in members:
        members[canvas_id] = {}

    if x not in members[canvas_id]:
        members[canvas_id][x] = []

    members[canvas_id][x].append(member)

    if "next_line" in map[start]:
        members = getText(map[start]["next_line"], map, members)    

    return members

def main(dirname0, dirname, manifests, soup):

    map = {}

    new_canvas_map = {}

    files = glob.glob("../../docs/iiif/"+dirname0+"/*.json")
    for file in files:
        with open(file) as f:
            df = json.load(f)

        canvases = df["sequences"][0]["canvases"]

        manifest = file.replace("../../docs", "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs")

        map[manifest] = {}

        for canvas in canvases:
            # vol = file.split("/")[-1].split(".")[0]
            # canvases[canvas["@id"]] = vol
            map[manifest][canvas["@id"]] = {}

            new_canvas_map[canvas["@id"]] = manifest



    flg_right_to_left = True

    count = 1

    tr_list = soup.find_all("tr")

    targets = []

    for i in range(1, len(tr_list)):

        tds = tr_list[i].find_all("td")

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

        if len(tds) < 4:
            print("err", tds)
            continue

        a_arr = tds[3].find_all("a")
        if len(a_arr) < 2:
            continue

        a = a_arr[1]

        if a == None:
            continue
        
        curation = a.get("href").split("=")[1]

        targets.append({
            "manifest" : manifest,
            "curation" : curation
        })

    for i in range(len(targets)):

        target = targets[i]

        if i % 200 == 0:
            print("target", i+1, len(targets))

        curation = target["curation"]
        manifest = target["manifest"]

        uri = curation

        # print("uri", count, uri)
        count += 1

        filename = curation.split("/")[-1]
        path = "data/curations/" + filename + ".json"
        dirname = os.path.dirname(path)
        os.makedirs(dirname, exist_ok=True)

        if not os.path.exists(path):

            # continue

            print("downloading", uri)

            df = requests.get(uri).json()

            f2 = open(path, 'w')
            json.dump(df, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
            f2.close()

        with open(path) as f:
            df = json.load(f)

        # -----------------------

        members = df["selections"][0]["members"]
        # manifest = df["selections"][0]["within"]["@id"]

        '''
        if manifest not in map:
            map[manifest] = {}
        '''

        tmp = {}

        start = ""

        for member in members:
            value = member["metadata"][0]["value"][0]
            marker = value["resource"]["marker"]

            id = value["@id"]

            if "next_line" in marker and "prev_line" not in marker:
                start = id
            
            member_id = value["on"].split("#xywh=")
            canvas_id = member_id[0]
            marker["canvas_id"] = canvas_id
            marker["xywh"] = member_id[1].split(",")

            tmp[id] = marker

        if start == "": #startがないものあり
            continue
        
        members_map = getText(start, tmp, {})

        for canvas_id in members_map:

            '''
            if canvas_id not in map[manifest]:
                map[manifest][canvas_id] = {}
            '''

            manifest = new_canvas_map[canvas_id]

            tmp = map[manifest][canvas_id]
            for x in members_map[canvas_id]:
                if x not in tmp:
                    tmp[x] = []
                
                for member in members_map[canvas_id][x]:

                    tmp[x].append(member)

        
    # count = 1

    # print(map)

    for manifest in sorted(map):

        print(manifest)

        # count += 1

        members_map = map[manifest]

        members = []

        uuid = hashlib.md5(manifest.encode('utf-8')).hexdigest()

        path = "data/manifests/"+uuid+".json"
        dirpath = os.path.dirname(path)
        os.makedirs(dirpath, exist_ok=True)

        if not os.path.exists(path):

            # continue

            df = requests.get(manifest).json()

            f2 = open(path, 'w')
            json.dump(df, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))
            f2.close()

        with open(path) as f:
            manifest_data = json.load(f)

        for canvas in manifest_data["sequences"][0]["canvases"]:
            canvas_id = canvas["@id"]

            text = ""

            if canvas_id in members_map:
                tmp = members_map[canvas_id]

                keys = sorted(tmp, reverse=flg_right_to_left)

                for x in keys:
                    arr = tmp[x]
                    for obj in arr:
                        members.append(obj)

                        text += obj["label"] + "\n"

            # print(text)

        curation = {
            "@context": [
                "http://iiif.io/api/presentation/2/context.json",
                "http://codh.rois.ac.jp/iiif/curation/1/context.json"
            ],
            "@id": manifest + "/curation.json",
            "@type": "cr:Curation",
            "label": "Character List",
            "selections": [
                {
                    "@id": manifest + "/range1",
                    "@type": "sc:Range",
                    "label": "Characters",
                    "members": members,
                    "within": {
                        "@id": manifest,
                        "@type": "sc:Manifest",
                        "label": manifest_data["label"]
                    }
                }
            ]
        }

        VOL = manifest.split("/")[-1].split(".json")[0]

        path = "../../docs/iiif/"+dirname+"/"+VOL+".json"
        dirpath = os.path.dirname(path)
        os.makedirs(dirpath, exist_ok=True)

        f2 = open(path, 'w')
        json.dump(curation, f2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))