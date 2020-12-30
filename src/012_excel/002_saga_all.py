import requests
import openpyxl
import json

book = openpyxl.Workbook()

for vol in range(1, 55):
    print(vol)

    if vol != 35 and False:
        continue

    type = "all"

    rows = []
    rows.append(["担当", "結果", "新編全集番号", "新編全集テキスト", "OCRテキスト", "東大本ページ番号", "URL"])

    # try:

    url = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/121_saga_all/"+str(vol).zfill(2)+".json"
    
    with open("/Users/nakamura/git/d_genji/genji_curation/docs/iiif/121_saga_all/"+str(vol).zfill(2)+".json") as f:
        curation_data = json.load(f)
    
    pages = []

    # print(curation_data)

    # curation_data = requests.get(url).json()

    selection = curation_data["selections"][0]

    within = selection["within"]

    members = selection["members"]

    manifest = within["@id"]

    map = {}

    for member in members:
        metadata = member["metadata"]

        member_id = member["@id"].split("#xywh=")
        page = int(member_id[0].split("/canvas/p")[1])

        # print("page", page)


        link = "http://codh.rois.ac.jp/software/iiif-curation-viewer/demo/?curation="+url+"&mode=annotation&pos="+str(page)+"&lang=ja"

        if len(metadata) > 1:
            p = -1
            koui = ""
            text = ""
            for obj in metadata:
                if obj["label"] == "編日本古典文学全集テキスト":
                    koui = obj["value"]
                elif obj["label"] == "KuroNet翻刻":
                    text = obj["value"]
                elif obj["label"] == "p":
                    # p = int(obj["value"])
                    p = obj["value"]

                    pages.append(p)

            text = str(page)+ " " + text

            map[text] = {
                "p" : p,
                "koui" : koui
            }
        else:
            text = metadata[0]["value"]
            text = str(page)+ " " + text

            if text not in map:
                map[text] = {
                    "p" : "",
                    "koui" : ""
                }


        map[text]["url"] = link
        map[text]["page"] = page

    for text in map:
        obj = map[text]
        tmp = obj["p"].split("-")

        a = ""
        b = ""
        
        if len(tmp) == 3:
            a = int(tmp[1])
            try:
                b = int(tmp[2])
            except Exception as e:
                print(e)
        row = ["", a, b, obj["koui"], text, obj["page"], obj["url"]]
        rows.append(row)

    '''
    count = pages[-1] - pages[0] + 1
    if count != len(pages):
        print(pages)
        print(len(pages) - count)
    

    for i in range(len(pages)):
        if i > 0:
            if pages[i] - pages[i-1] != 1:
                print(pages[i]-1)

    print("-----------")

    '''

    # except Exception as e:
    #     print(e)

    
    sheet = book.create_sheet(index=(vol-1), title=str(vol)+" "+within["label"])

    for row in rows:
        sheet.append(row)
    # break

    # print(map)

book.save('data/saga_'+type+'.xlsx')