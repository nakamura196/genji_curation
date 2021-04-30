import sys
sys.path.append('../500_common')
import lib_delete
import requests
import lib_ss
import lib

a = "Chrome1del"
b = "Profile 1"

print("lib_ss.main")
soup = lib_ss.main(a, b, 60)

print("lib.get_images_by_soup")
images = lib.get_images_by_soup(soup)

########

collections = [
    "https://utda.github.io/genji/iiif/ndl-2610937/top.json", 
    "https://utda.github.io/genji/iiif/ndl-2610583/top.json"
]
manifests = []

for collection_url in collections:
    collection = requests.get(collection_url).json()

    manifests_arr = collection["manifests"]
    
    for i in range(len(manifests_arr)):
        manifest = manifests_arr[i]["@id"]
    manifests.append(manifest)

manifests.append("https://kotenseki.nijl.ac.jp/biblio/100153620/manifest")

#########

path = "../506_nijl02/data/result.html"

lib_delete.main(a, b, manifests, path)

