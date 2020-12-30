import requests
from bs4 import BeautifulSoup
import re
import urllib

prefix = ".//{http://www.tei-c.org/ns/1.0}"
xml = ".//{http://www.w3.org/XML/1998/namespace}"

start = 5016 # 1は除く
end = 5071

index = 1 #1 は除く
seq = 1

info = requests.get("https://genji.dl.itc.u-tokyo.ac.jp/data/info.json").json()

map = {}

count = 0

selections = info["selections"]

for selection in selections:

    members = selection["members"]

    for i in range(len(members)):
        map[count+1] = members[i]["label"]
        count += 1

for i in range(start, end + 1):
    url = "https://www.aozora.gr.jp/cards/000052/card"+str(i)+".html"

    r = requests.get(url)
    #要素を抽出
    soup = BeautifulSoup(r.content, 'lxml')

    a_arr = soup.find_all("a")

    for a in a_arr:
        href = a.get("href")

        if href != None and "files/"+str(i)+"_" in href and ".html" in href:
            target_url = "https://www.aozora.gr.jp/cards/000052/files/" + href.split("/files/")[1]
            

            xml_url = target_url.replace("https://www.aozora.gr.jp/cards/", "https://tei-eaj.github.io/auto_aozora_tei/data/").replace(".html", ".xml")
            
            
            filename = xml_url.split("/")[-1]
            
            print("https://genji.dl.itc.u-tokyo.ac.jp/data/tei/"+filename)

            req = urllib.request.Request(xml_url)

            with urllib.request.urlopen(req) as response:
                XmlData = response.read()

            import xml.etree.ElementTree as ET

            root = ET.fromstring(XmlData)

            root.find(prefix+"title").text = "源氏物語・" + map[index]+"・与謝野晶子訳"

            segs = root.findall(prefix+"seg") #"*[@style]")

            for seg in segs:
                style = seg.get("style")
                if style != None:
                    style = style.replace("margin-right: 3em", "")
                    seg.set("style", style)

            if filename == "5058_14558.xml":
                root.find(prefix+"title").text = "源氏物語・雲隠・与謝野晶子訳"

            resps = root.findall(prefix+"respStmt")
            for respStmt in resps:
                resp = respStmt.find(prefix+"resp").text
                if resp == "TEI Encoding":
                    respStmt.find(prefix+"name").text = "Satoru Nakamura"

            ET.register_namespace('', "http://www.tei-c.org/ns/1.0")
            ET.register_namespace('xml', "http://www.w3.org/XML/1998/namespace")

            #XMLファイルの生成
            tree = ET.ElementTree(root) 
            
            tree.write("data/xml/"+str(seq).zfill(2)+".xml", encoding='UTF-8')

            if filename != "5054_10249.xml" and filename != "5058_14558.xml":
                index += 1

            seq += 1

            break
        
    