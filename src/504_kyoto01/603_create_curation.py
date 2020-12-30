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

dirname0 = "kyoto01"
dirname = "kyoto01_kuronet"
manifests = [
    "https://kotenseki.nijl.ac.jp/biblio/100153620/manifest"
]

lib_curation.main(dirname0, dirname, manifests, soup)