import sys
sys.path.append('../500_common')
import lib_curation
import lib_ss
import time
from bs4 import BeautifulSoup
import requests
#--------------

# soup = lib_ss.main("/Users/nakamurasatoru/git/d_genji/genji_curation/src/500_common/Chrome11", "Profile 1")
soup = BeautifulSoup(open("data/result.html"), "lxml")

tr_list = soup.find_all("tr")
print(len(tr_list))

time.sleep(5)

dirname0 = "ndl02"
dirname = "ndl02_kuronet"

########

collection_url = "https://utda.github.io/genji/iiif/ndl-8943312/top.json"
collection = requests.get(collection_url).json()

manifests_arr = collection["manifests"]
manifests = []
for i in range(len(manifests_arr)):
    manifest = manifests_arr[i]["@id"]
    manifests.append(manifest)

#########

lib_curation.main(dirname0, dirname, manifests, soup)