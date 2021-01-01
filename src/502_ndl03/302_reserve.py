import sys
sys.path.append('../500_common')
import lib_reserve

import requests

a = "/Users/nakamurasatoru/git/d_genji/genji_curation/src/500_common/Chrome3res"
b = "Profile 3"

path = "data/result.html"

########

collection_url = "https://utda.github.io/genji/iiif/ndl-2610937/top.json"
collection = requests.get(collection_url).json()

manifests_arr = collection["manifests"]
manifests = []
for i in range(len(manifests_arr)):
    manifest = manifests_arr[i]["@id"]
    manifests.append(manifest)

#########


lib_reserve.main(a, b, path, manifests, waitTime=10, preTime=20)
