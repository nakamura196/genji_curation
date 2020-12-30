import sys
sys.path.append('../500_common')
import lib

images = lib.get_images("../500_common/data/result.html")

collectionUrl = "https://utda.github.io/genji/iiif/ndl-2610583/top.json"
areas = ["3600,370,3000,4400", "560,370,3000,4400"]
countMax = 5

token = lib.get_token("../token.yml")

lib.post(collectionUrl, areas, countMax, token, images, "Collection")