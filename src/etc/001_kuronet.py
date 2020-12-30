import gspread
import json
import requests

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

VOL = "54"

###############################

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

###############################



#2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#認証情報設定
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
credentials = ServiceAccountCredentials.from_json_keyfile_name('strategic-ivy-210006-fa7510547ccc.json', scope)

#OAuth2の資格情報を使用してGoogle APIにログインします。
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートキーを変数[SPREADSHEET_KEY]に格納する。
SPREADSHEET_KEY = '1iMmn7R7GMaPjWuSOh15YZ9FqZOwbjhqWdRQLC9JeCLg'



#共有設定したスプレッドシートのシート1を開く
sheets = gc.open_by_key(SPREADSHEET_KEY)
print(sheets)
worksheet = sheets.worksheet(VOL)

###############################

map = {}

flg_right_to_left = True

for i in range(2, worksheet.row_count):
    cell_value = worksheet.cell(i, 5).value

    if cell_value == "":
        break

    print(i)

    uri = cell_value

    df = requests.get(uri).json()

    members = df["selections"][0]["members"]
    manifest = df["selections"][0]["within"]["@id"]

    if manifest not in map:
        map[manifest] = {}

    tmp = {}

    start = ""

    for member in members:
        value = member["metadata"][0]["value"][0]
        marker = value["resource"]["marker"]

        id = value["@id"]

        if "next_line" in marker and "prev_line" not in marker:
            start = id
        
        member_id = value["on"].split("#xywh=")
        marker["canvas_id"] = member_id[0]
        marker["xywh"] = member_id[1].split(",")

        tmp[id] = marker
    
    members_map = getText(start, tmp, {})

    for canvas_id in members_map:
        if canvas_id not in map[manifest]:
            map[manifest][canvas_id] = {}

        tmp = map[manifest][canvas_id]
        for x in members_map[canvas_id]:
            if x not in tmp:
                tmp[x] = []
            
            for member in members_map[canvas_id][x]:

                tmp[x].append(member)

    


for manifest in map:

    members_map = map[manifest]

    members = []

    manifest_data = requests.get(manifest).json()

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

        print(text)

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

    f2 = open("../docs/iiif/kuronet/"+VOL+".json", 'w')
    json.dump(curation, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))