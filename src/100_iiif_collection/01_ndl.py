import pandas as pd
from rdflib import URIRef, BNode, Literal, Graph
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from rdflib import Namespace
import numpy as np
import math
import sys
import argparse
import json
from urllib import request
from bs4 import BeautifulSoup
import hashlib
import os
import requests

import csv

uuid = "1288440"
file = 'data/ndl-'+uuid+'.csv'
genji_dir = "/Users/nakamurasatoru/git/d_genji"

prefix = "https://utda.github.io/genji"

with open(file, 'r') as f:
    reader = csv.reader(f)
    label = next(reader)[0]  # ヘッダーを読み飛ばしたい時

    id = file.split("/")[-1].split(".")[0]

    manifests = []

    for row in reader:
        manifest = row[0]

        print(manifest)

        m_data = requests.get(manifest).json()

        manifests.append({
            "@id": m_data["@id"],
            "@type": "sc:Manifest",
            "attribution": m_data["attribution"],
            "label": m_data["label"],
            "license": m_data["license"],
            "thumbnail": m_data["sequences"][0]["thumbnail"]["@id"]
        })

    collection = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": prefix + "/iiif/"+id+"/top.json",
        "@type": "sc:Collection",
        "label": label,
        "manifests" : manifests,
        "vhint": "use-thumb"
    }

    opath = genji_dir + "/genji/static/iiif/"+id+"/top.json"
    dirname = os.path.dirname(opath)

    os.makedirs(dirname, exist_ok=True)

    with open(opath, 'w') as f:
        json.dump(collection, f, ensure_ascii=False, indent=4,
                    sort_keys=True, separators=(',', ': '))
