
import json
import requests
import openpyxl

book = openpyxl.Workbook()

vols = [
    # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21
    22, 23, 24, 25, 26, 27, 28, 29, 30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50,
        51, 52, 53, 54
]

with open("data/ids.json") as f:
    ids = json.load(f)

sheet = book.create_sheet(index=0)
sheet.append(["vol", "url"])

for vol in vols:
    gid = ids[str(vol).zfill(2)]

    url = "https://tei-eaj.github.io/parallel_text_editor/app/#/v2?main=https://docs.google.com/document/d/"+gid+"/edit&sub=https://genji.dl.itc.u-tokyo.ac.jp/data/tei/yosano/"+str(vol).zfill(2)+".xml"


    sheet.append([vol, url])
    
book.save('data/result.xlsx')