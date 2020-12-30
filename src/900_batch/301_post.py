# coding: utf-8
import requests
import time

for i in range(1, 55):

    if i == 53 or i == 54 or i < 50:
        continue
    

    manifest = "https://nakamura196.github.io/genji/ugm/utokyo/manifest/"+str(i).zfill(2)+".json"

    df = requests.get(manifest).json()

    canvases = df["sequences"][0]["canvases"]

    # areas = ["3600,1000,2400,3000", "1200,1000,2400,3000"]
    areas = ["3500,950,2500,3200", "1000,900,2500,3200"]
    # areas = ["1000,900,5000,3200"]

    for j in range(len(canvases)):

        canvas = canvases[j]

        if i == 50 and j < 45:
            continue

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
                    'token' : 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjBiYWJiMjI0NDBkYTAzMmM1ZDAwNDJjZGFhOWQyODVjZjhkMjAyYzQiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoi5Lit5p2R6KaaIiwicGljdHVyZSI6Imh0dHBzOi8vbGg1Lmdvb2dsZXVzZXJjb250ZW50LmNvbS8tR0tBdEFxVkdRRVEvQUFBQUFBQUFBQUkvQUFBQUFBQUFvQmcva1JUei1RS21LSG8vcGhvdG8uanBnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2NvZGgtODEwNDEiLCJhdWQiOiJjb2RoLTgxMDQxIiwiYXV0aF90aW1lIjoxNTg2OTMzMjI5LCJ1c2VyX2lkIjoiRmR6QVFvUzU4NGVXYUpOUmY1TndSTUR5QndXMiIsInN1YiI6IkZkekFRb1M1ODRlV2FKTlJmNU53Uk1EeUJ3VzIiLCJpYXQiOjE1ODY5OTQ2NTAsImV4cCI6MTU4Njk5ODI1MCwiZW1haWwiOiJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExNTMxMTk4NTgxMjgyNzQ1Mjg0MiJdLCJlbWFpbCI6WyJuYS5rYW11cmEuMTI2M0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJnb29nbGUuY29tIn19.EwHl6bwIZMXGVmVQrCLVVmmg3KYH5Rb6Ned2ToB5OK5acF6rnQn2sAkXeA2d1ZDlwj-OfDbSZ74lHSac5-15Lab8t18heL76PldWckC_cJpgyvNU5ugJE17Vj3XsK8KCoO_HwIou74K54KIqRsbJk2m43mnnQLccpySV6hOzxDadqxtr9yyj5r1JGXxnOt3A0Dzzc7xT6iO-YQb_Q_7Ww8-vX8pTiAKpIFYAmT0jIPHLTuQqFsaRoCzqPr4f542YAVGcDsxAmzLkZsBVrTkKljMPE4TNl9y-jJ4JyDfnoiGNrKWCDlND30usOKTsclEnNmxjxSqiaX_oFk-dM7wbLQ'
                    })
            #レスポンスオブジェクトのjsonメソッドを使うと、
            #JSONデータをPythonの辞書オブジェクトに変換して取得できる
            print(response)