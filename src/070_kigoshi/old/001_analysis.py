import bs4
import requests
from classes import test

soup = bs4.BeautifulSoup(open("data/index.html"), 'html.parser')

arr = []

for link in soup.find_all("a"):
    if "http://codh.rois.ac.jp/software/kuronet-text-editor/demo/?curation=https://mp.ex.nii.ac.jp/api/curation/json/" in link.get("href"): # "mp4"を含むリンクを抽出
        uri = link.get("href").split("=")[1]
        print(uri)
        arr.append(uri)

arr.reverse()

map = {}

for i in range(len(arr)):
    
    print(str(i+1) + "/" + str(len(arr)))
    
    uri = arr[i]

    curation_data = requests.get(uri).json()
    manifest = curation_data["selections"][0]["within"]["@id"]

    vol = int(manifest.split("/")[-1].split(".")[0])
    # print(vol, curation_data["selections"][0]["members"][0]["@id"])

    if vol not in map:
        map[vol] = []

    map[vol].append(uri)

for vol in sorted(map):
    print(vol)
    uris = map[vol]
    opath = "../../docs/iiif/kuronet/"+str(vol).zfill(2)+".json"
    test.Item.main(opath, uris)

