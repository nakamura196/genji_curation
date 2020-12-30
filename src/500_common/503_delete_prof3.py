import sys
sys.path.append('../500_common')
import lib_delete

a = "Chrome3del"
b = "Profile 3"

########

collection_url = "https://utda.github.io/genji/iiif/ndl-8943312/top.json"
collection = requests.get(collection_url).json()

manifests_arr = collection["manifests"]
manifests = []
for i in range(len(manifests_arr)):
    manifest = manifests_arr[i]["@id"]
    manifests.append(manifest)

#########

lib_delete.main(a, b, manifests)