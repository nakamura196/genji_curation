import csv
import json
import requests
import copy

start = 2546278
end = 2546337

count = 1
for i in range(start, end+1):
    url = "https://www.dl.ndl.go.jp/api/iiif/"+str(i)+"/manifest.json"
    index = str(count).zfill(2)
    count += 1

    df = requests.get(url).json()

    f2 = open("../../docs/iiif/ndl/"+index+".json", 'w')
    json.dump(df, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))