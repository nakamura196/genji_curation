# coding: utf-8
import requests
import time
import json

DIR_NAME = "ndl"

token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImMzZjI3NjU0MmJmZmU0NWU5OGMyMGQ2MDNlYmUyYmExMTc2ZWRhMzMiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoidS5uYWthbXVyYS5zYXRvcnUgdSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLXBZeVhMVEpMeFE0L0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FDSGkzcmVWR21aMzNBQTRXSGloWGQ0aGZfSUcyNHpIX1EvcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTkyMzk3NTgyLCJ1c2VyX2lkIjoiUGwySXNUNWlVV1Z5SVZQUFFkNVNZbHZkdmV6MiIsInN1YiI6IlBsMklzVDVpVVdWeUlWUFBRZDVTWWx2ZHZlejIiLCJpYXQiOjE1OTI1MTc1MTcsImV4cCI6MTU5MjUyMTExNywiZW1haWwiOiJ1Lm5ha2FtdXJhLnNhdG9ydUBnLmVjYy51LXRva3lvLmFjLmpwIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZ29vZ2xlLmNvbSI6WyIxMDExNzI0MzcwNTUzMjI0MjcwMDYiXSwiZW1haWwiOlsidS5uYWthbXVyYS5zYXRvcnVAZy5lY2MudS10b2t5by5hYy5qcCJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.ORLwowbWPDczX92pSumFVXXgkT7NQnhf4em-0tQtdZyGoC0kFBSq_PG-fqDHxv56B_RU4Dwa_yNSN6tJcJHFnO3XMYMdyNiIlpGRM4IUzmnKirZ8fIBg1H_6j0Abw32wP3v3LF2KzVNwL0SqIa_MGCTP3hpV5JnQY_PznwRGjdL_LxbJVzD6RP_XUrBh-PFb9xoFn3R0AGilFTUrc1OZTnnWDab7KzavOmTMml-DNn9-L1El-qCJpj0bjcFu2csmZX0krugAwjoILlfDNMi4AhkpptWQfjgG6bDFGZ6xGMexbfKRb6cwCHgyLAuaRzxPrX9mnMHr_3eksy2vZHat2A"

for i in range(1, 55):

    if i >= 1:
        print(i)
    else:
        continue

    manifest = "https://raw.githubusercontent.com/nakamura196/genji_curation/master/docs/iiif/"+DIR_NAME+"/"+str(i).zfill(2)+".json"

    print(manifest)

    with open("../../docs/iiif/"+DIR_NAME+"/"+str(i).zfill(2)+".json") as f:
        df = json.load(f)

    # df = requests.get(manifest).json()

    sequence = df["sequences"][0]

    if "canvases" not in sequence:
        continue

    canvases = sequence["canvases"]

    # areas = ["3600,1000,2400,3000", "1200,1000,2400,3000"]
    areas = ["3400,2000,2900,2800", "400,2000,2900,2800"]
    # areas = ["1000,900,5000,3200"]

    for j in range(len(canvases)):

        canvas = canvases[j]

        print(i, canvas["@id"])

        prefix = canvas["images"][0]["resource"]["service"]["@id"]

        for xywh in areas:
            time.sleep(0.5)

            #POSTパラメータは二つ目の引数に辞書で指定する
            response = requests.post(
                'https://mp.ex.nii.ac.jp/api/kuronet/post',
                {
                    'image':prefix + '/'+xywh+'/full/0/default.jpg',
                    'manifest' : manifest,
                    'canvas' : canvas["@id"],
                    'xywh' : xywh,
                    'token' : token
                    })
            #レスポンスオブジェクトのjsonメソッドを使うと、
            #JSONデータをPythonの辞書オブジェクトに変換して取得できる
            print(response)