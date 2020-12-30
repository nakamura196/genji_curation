import requests
import openpyxl
import json
import os

book = openpyxl.Workbook()

for vol in range(1, 55):
    print(vol)

    type = "all"

    prefix = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif"
    prefix2 = "/Users/nakamurasatoshi/git/d_genji/genji_curation/docs/iiif"

    url = prefix + "/nijl_kuronet_taisei_"+type+"/"+str(vol).zfill(2)+".json"
    # curation_data = requests.get(url).json()

    path = prefix2 + "/nijl_kuronet_taisei_"+type+"/"+str(vol).zfill(2)+".json"
    if not os.path.exists(path):
        continue

    with open(path) as f:
        curation_data = json.load(f)

    selection = curation_data["selections"][0]

    within = selection["within"]

    members = selection["members"]

    manifest = within["@id"]

    

    canvas_pos_map = {}
    tmp = {}

    for member in members:
        metadata = member["metadata"]

        member_id = member["@id"].split("#xywh=")
        canvas_id = member_id[0]
        page = int(member_id[0].split("/canvas/")[1]) # NIJL仕様

        tmp[page] = canvas_id

    pos = 1
    for page in sorted(tmp):
        canvas_pos_map[tmp[page]] = pos
        pos += 1

    '''
    with open(prefix2 + "/nijl/"+str(vol).zfill(2)+".json") as f:
        manifest_data = json.load(f)

    canvases = manifest_data["sequences"][0]["canvases"]

    for i in range(len(canvases)):
        canvas = canvases[i]
        canvas_pos_map[canvas["@id"]] = i + 1
    '''


    map = {}

    for member in members:
        metadata = member["metadata"]

        member_id = member["@id"].split("#xywh=")
        print(member_id)
        page = int(member_id[0].split("/canvas/")[1]) # NIJL仕様

        pos = canvas_pos_map[member_id[0]]


        link = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation="+url+"&mode=annotation&pos="+str(pos)+"&lang=ja"

        if len(metadata) > 1:
            p = -1
            koui = ""
            text = ""
            for obj in metadata:
                if obj["label"] == "校異源氏テキスト":
                    koui = obj["value"]
                elif obj["label"] == "KuroNet翻刻":
                    text = obj["value"]
                elif obj["label"] == "p":
                    p = int(obj["value"])

            map[text] = {
                "p" : p,
                "koui" : koui
            }
        else:
            text = metadata[0]["value"]
            if text not in map:
                map[text] = {
                    "p" : "",
                    "koui" : ""
                }


        map[text]["url"] = link
        map[text]["page"] = page

    rows = []
    rows.append(["担当", "結果", "大成番号", "校異テキスト", "OCRテキスト", "鵜飼文庫ページ番号", "URL"])

    for text in map:
        obj = map[text]
        row = ["", obj["p"], obj["p"], obj["koui"], text, obj["page"], obj["url"]]
        rows.append(row)

    
    sheet = book.create_sheet(index=(vol-1), title=str(vol)+" "+within["label"])

    for row in rows:
        sheet.append(row)
    # break

    # print(map)

book.save('data/taisei_'+type+'.xlsx')