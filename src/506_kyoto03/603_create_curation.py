import sys
sys.path.append('../500_common')
import lib_curation
import lib_ss
import time
from bs4 import BeautifulSoup
#--------------

# soup = lib_ss.main("/Users/nakamurasatoru/git/d_genji/genji_curation/src/500_common/Chrome11", "Profile 1")
soup = BeautifulSoup(open("data/result.html"), "lxml")

tr_list = soup.find_all("tr")
print(len(tr_list))

time.sleep(5)

dirname0 = "kyoto02"
dirname = "kyoto02_kuronet"
manifests = [
    "https://rmda.kulib.kyoto-u.ac.jp/iiif/metadata_manifest/RB00007030/manifest.json"
]

lib_curation.main(dirname0, dirname, manifests, soup)