import sys
sys.path.append('../500_common')
import lib

images = lib.get_images("../500_common/data/result.html")

collectionUrl = "https://utda.github.io/genji/iiif/ndl-2610937/top.json"
areas = ["3200,250,2800,2600", "430,250,2800,2600"]
countMax = 5

token = lib.get_token("../token.yml")

lib.post(collectionUrl, areas, countMax, token, images, "Collection")