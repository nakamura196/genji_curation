import urllib.request
from bs4 import BeautifulSoup
import csv
from time import sleep
import pandas as pd
import json
import urllib.request
import os
from PIL import Image
import yaml
import requests
import sys
import argparse
import Levenshtein

VOL = "54"

koui = {
    "やまにおはしてれいせさせ給やうに經佛なとくやうせさせ給又の日はよかはに" : 2055,
    
    "はゝかられ侍れとかの山さとにしるへき人のかくろへて侍るやうにきゝ侍" : 2056,
    "とさゝめきておやのしにかへるをはさしをきてもてあつかひなけきてなん侍り" : 2057,
    
    "てこの人いたつらになしたてまつらしとまとひいられてなくなくいみしきこと" : 2058,
    "ことゝあやまちしたる心ちしてつみふかけれはあしきものにらうせられ給けん" : 2059,

    "との給けしきいとあはれと思たまへれはかたちをかへよをそむきにきと" : 2060,
    "てたのもしけなき身ひとつをよすかにおほしたるかさりかたきほたしにおほ" : 2061,

    "てあそひ給へよとすゝろなるやうにはおほすましきゆへもありけりとうちかた" : 2062,
    "にかよふ人のみなんこのわたりにはちかきたよりなりけるかの殿はこのこをや" : 2063,

    "こともおほかれとけふあすゝくしてさふらふへしとかき給へりこれはなに事そ" : 2064,
    "たつねとひ給はしめよりありしやうくはしくきこえ侍ぬおほん心さしふかゝり" : 2065,
    
    "てほろほろとなかれぬいとおかしけにてすこしうちおほえたまへる心ちもす" : 2066,
    "もしよにものしたまはゝそれひとりになんたいめんせまほしくおもひ侍このそ" : 2067,
    
    "とて侍つるいかてたてまつらんといへはいとことはりなり猶いとかくう" : 2068,
    "ほとのはしたなさなとをおもひみたれていとゝはれはれしからぬ心はいひやる" : 2069,
    
    "いとゝかゝることゝもにおほしみたるゝにやつねよりも物おほえさせ給はぬさ" : 2070
}

with open('../docs/iiif/kuronet/'+VOL+'.json') as f:
    df = json.load(f)
    members = df["selections"][0]["members"]

map = {}

for line in koui:
    map[line] = []
    for i in range(len(members)):
        label = ""
        if i - 1 >= 0:
            label += members[i-1]["label"] + "／"

        member = members[i]
        label += member["label"]

        if i + 1 <= len(members) - 1:
            label += "／" + members[i+1]["label"]

        
        score = Levenshtein.distance(line, label)
        map[line].append ({
            "label" : label,
            "main" : member["label"],
            "score" : score,
            "member_id" : member["@id"],
            "index" : i
        })

print(map)

print("----------------")

prev_index = 0

members = []

for line in map:
    print(line)

    print(prev_index)

    obj = map[line]

    obj = obj[prev_index:]

    # print(obj)

    score_sorted = sorted(obj, key=lambda x:x["score"])

    flg = True

    for i in range(len(score_sorted)):

        
        data = score_sorted[i]

        index = data["index"]
        
        if i < 5:
            print(data["index"], data["score"], data["member_id"], data["label"])

        if index - prev_index < 50:

            if flg:
                print("******:")
                prev_index = index + 1

                members.append({
                    "@id" : data["member_id"],
                    "@type": "sc:Canvas",
                    "description": "",
                    "label": "["+str(len(members) + 1)+"]",
                    "metadata": [
                        {
                            "label": "p",
                            "value": koui[line]
                        },
                        {
                            "label": "校異源氏テキスト",
                            "value": line
                        },
                        {
                            "label": "KuroNet翻刻",
                            "value": data["main"]
                        },
                        {
                            "label": "KuroNet翻刻（前後を含む3行）",
                            "value": data["label"]
                        }
                    ]
                })

                flg = False

    print("----------------")

curation = {
    "@context": [
        "http://iiif.io/api/presentation/2/context.json",
        "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/090075d0-3e81-8414-5d57-62c516f49e47/manifest/curation.json",
    "@type": "cr:Curation",
    "label": "Character List",
    "selections": [
        {
            "@id": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/090075d0-3e81-8414-5d57-62c516f49e47/manifest/range1",
            "@type": "sc:Range",
            "label": "Characters",
            "members": members,
            "within" : {
                "@id": "https://iiif.dl.itc.u-tokyo.ac.jp/repo/iiif/090075d0-3e81-8414-5d57-62c516f49e47/manifest",
                "@type": "sc:Manifest",
                "label": "夢浮橋"
            }
        }
    ]
}

f2 = open("../docs/iiif/taisei/"+VOL+".json", 'w')
json.dump(curation, f2, ensure_ascii=False, indent=4,
    sort_keys=True, separators=(',', ': '))