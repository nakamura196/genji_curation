import sys
sys.path.append('../500_common')
import lib_seq
import requests

a = "/Users/nakamurasatoru/git/d_genji/genji_curation/src/500_common/Chrome1seq"
b = "Profile 1"

path = "data/result.html"

########

manifests = ["https://kokusho.nijl.ac.jp/biblio/100153621/manifest"]

#########

lib_seq.main(a, b, path, manifests, waitTime=10, preTime=20, check=False)