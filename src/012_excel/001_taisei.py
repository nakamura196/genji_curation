import requests
import openpyxl

book = openpyxl.Workbook()

for vol in range(1, 55):
    print(vol)

    url = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/021_taisei/"+str(vol).zfill(2)+".json"
    curation_data = requests.get(url).json()

    selection = curation_data["selections"][0]

    within = selection["within"]

    members = selection["members"]

    manifest = within["@id"]

    map = {}

    for member in members:
        metadata = member["metadata"]

        member_id = member["@id"].split("#xywh=")
        page = int(member_id[0].split("/canvas/p")[1])


        link = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation="+url+"&mode=annotation&pos="+str(page)+"&lang=ja"

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
    rows.append(["担当", "結果", "大成番号", "校異テキスト", "OCRテキスト", "東大本ページ番号", "URL"])

    for text in map:
        obj = map[text]
        row = ["", obj["p"], obj["p"], obj["koui"], text, obj["page"], obj["url"]]
        rows.append(row)

    
    sheet = book.create_sheet(index=(vol-1), title=str(vol)+" "+within["label"])

    for row in rows:
        sheet.append(row)
    # break

    # print(map)

book.save('data/data.xlsx')