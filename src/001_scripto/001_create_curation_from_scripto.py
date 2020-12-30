import bs4
import requests
from urllib.parse import urljoin
import uuid
import json

def media(url):

    print("media", url)

    r = requests.get(url)         #requestsを使って、webから取得
    soup = bs4.BeautifulSoup(r.text, 'lxml') #要素を抽出

    image_api = soup.find(class_="post-subtitle").text.split("Original title: ")[1]

    image_api = image_api.replace("https://dl.ndl.go.jp/", "https://www.dl.ndl.go.jp/")

    #######

    tmp = url.split("/")

    api = "https://diyhistory.org/public/genji/wiki2/api.php?titles="+ tmp[-3] +  ":" + tmp[-2] + ":" + tmp[-1] +"&action=query&format=json&rvprop=content&prop=revisions"

    df = requests.get(api).json()

    pages = df["query"]["pages"]

    text = ""

    for page in pages:

        if page != "-1":

            text = pages[page]["revisions"][0]["*"]

    return image_api, text.strip()


def item(base, dir):

    page = 1

    flg = True

    data = []

    manifest = ""
    title = ""

    while flg:

        url = base + "?page=" + str(page)

        r = requests.get(url)         #requestsを使って、webから取得
        soup = bs4.BeautifulSoup(r.text, 'lxml') #要素を抽出

        divs = soup.find_all(class_="resource-tile")

        print(len(divs))

        if page == 1:
            start = 1
        else:
            start = 0

        for d in range(start, len(divs)):
            div = divs[d]
            href = div.find("a").get("href")
            href = urljoin(url, href)

            print("*", d+1, href)

            image_api, text = media(href)

            print(image_api)

            if text != "":

                data.append({
                    "image_api" : image_api,
                    "text" : text
                })

        if len(divs) == 0:
            flg = False

        ##################

        if page == 1:
            properties = soup.find(class_="resource-metadata").find_all(class_="property")

            for prop in properties:
                term = prop.find(class_="field-term").text
                
                value = prop.find(class_="value").text.strip()
                if term == "(dcterms:relation)":
                    manifest = value
                elif term == "(dcterms:title)":
                    title = value

            map = {}

            if manifest != "":
                manifest_data = requests.get(manifest).json()

                canvases = manifest_data["sequences"][0]["canvases"]



                for canvas in canvases:
                    api = canvas["images"][0]["resource"]["service"]["@id"] + "/info.json"
                    map[api] = canvas["@id"] + "#xywh=0,0," + str(canvas["width"]) + "," + str(canvas["height"])

        ##################

        page += 1

    members = []

    for i in range(len(data)):
        obj = data[i]
        api = obj["image_api"]

        members.append({
            "@id" : map[api],
            "@type": "sc:Canvas",
            "label": "["+str(i+1)+"]",
            "metadata": [
                {
                "label": "Text",
                "value": obj["text"]
                }
            ]
        })

    curation_uri = "https://curation/" + str(uuid.uuid4())

    curation = {
        "@context": [
            "http://iiif.io/api/presentation/2/context.json",
            "http://codh.rois.ac.jp/iiif/curation/1/context.json"
        ],
        "@id": curation_uri,
        "@type": "cr:Curation",
        "label": "Character List",
        "selections": [

            {
                "@id": curation_uri + "/range1",
                "@type": "sc:Range",
                "label": "Characters",
                "members": members,
                "within" : {
                    "@id" : manifest,
                    "@type" : "sc:Manifest",
                    "label" : title
                }
            }
        ]
    }

    fw = open(dir + "/" + title + ".json", 'w')
    json.dump(curation, fw, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

page = 1

base = "https://diyhistory.org/public/genji8/scripto/s/koui/1/1/item"

flg = True

while(flg):

    url = base + "?page=" + str(page)
    r = requests.get(url)         #requestsを使って、webから取得
    soup = bs4.BeautifulSoup(r.text, 'lxml') #要素を抽出

    divs = soup.find_all(class_="resource-tile")
    for div in divs:
        href = div.find("a").get("href")
        href = urljoin(url, href)
        print(href)

        # if "/5" in href or "/6" in href or "/7" in href or "/8" in href or "/233" in href or "/225" in href:


        item(href, "data")

    page += 1

    if len(divs) == 0:
        flg = False