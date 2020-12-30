import gspread
import json
import requests
import time

#ServiceAccountCredentials：Googleの各サービスへアクセスできるservice変数を生成します。
from oauth2client.service_account import ServiceAccountCredentials 

VOL = "54"

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
workbook = gc.open_by_key(SPREADSHEET_KEY)

###############################

collection = requests.get("https://nakamura196.github.io/genji/ugm/utokyo/collection.json").json()

manifests = collection["manifests"]

###############################

for vol in range(1, len(manifests)):

    title = str(vol)

    print(title)

    workbook.add_worksheet(title=title, rows=0, cols=0)

    worksheet = workbook.worksheet(title)

    manifest_data = manifests[vol - 1]

    manifest = manifest_data["@id"]

    manifest_data = requests.get(manifest).json()

    rows = []

    row0 = ["Vol", "作品", "ページ", "左右", "Curation URI", "担当", "manifest", "kuronet"]
    rows.append(row0)

    curation_url = "http://codh.rois.ac.jp/kuronet/iiif-curation-viewer/?manifest=" + manifest

    row1 = [vol, manifest_data["label"], "---", "---", "---", "---", manifest, curation_url]
    rows.append(row1)

    canvas_length = len(manifest_data["sequences"][0]["canvases"])

    for i in range(0, canvas_length):
        rows.append(["---", "---", i+1, "r", "", "---", "---", curation_url+"&pos=" + str(i+1)])
        rows.append(["---", "---", i+1, "l", "", "---", "---", curation_url+"&pos=" + str(i+1)])

    r_len = len(rows)

    df = []
    for r in range(len(rows)):
        row = rows[r]
        for c in range(len(row)):
            df.append(row[c])

    range_str = "A1:H"+str(r_len)
    cell_list = worksheet.range(range_str)

    count = 0

    for cell in cell_list:
        cell.value = df[count]
        count += 1

    worksheet.update_cells(cell_list)

    '''

    for r in range(len(rows)):
        row = rows[r]
        for i in range(len(row)):
            time.sleep(0.5)
            worksheet.update_cell(r + 1, i + 1, row[i])

    '''