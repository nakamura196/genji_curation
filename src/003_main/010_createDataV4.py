import pandas as pd
import requests
import json
import os
import xml.etree.ElementTree as ET
import time
import glob
import math

stage = ""
# stage = "_dev"

genji_dir = "/Users/nakamurasatoru/git/d_genji"

hostPrefix = "https://genji.dl.itc.u-tokyo.ac.jp"
# hostPrefix = "https://utda.github.io/genji"
dir = genji_dir + "/genji/static/data"
dir2 = genji_dir + "/genji/static/data/iiif"+stage+"/org"


def create_members_map(members_map, members):
  for member in members:
    member_id = member["@id"]
    canvas_id = member_id.split("#")[0]
    if canvas_id not in members_map:
      members_map[canvas_id] = []
    members_map[canvas_id].append(member)

  return members_map


def create_anno(canvas, members_map, odir, index, info):

  canvas_id = canvas["@id"]

  if canvas_id not in members_map:
    return None

  odir = odir + "/list"
  os.makedirs(odir, exist_ok=True)

  opath = odir+"/p"+str(index)+".json"

  annoListUri = opath.replace(opath.split("/data/")[0], hostPrefix)

  members = members_map[canvas_id]

  resources = []

  for i in range(len(members)):
    member = members[i]

    xywh = member["@id"].split("#xywh=")[1]

    areas = xywh.split(",")

    w = int(float(areas[2]))

    h = int(float(areas[3]))

    d2 = int(h / 150)

    


    # d2 = 30

    x = int(float(areas[0])) + int(w / 2)
    y = int(float(areas[1]))#  + int(float(areas[3]))#  + w #d2 * 2

    w = w / 2

    if w > 100:
     w = 100

    y -= w / 1.14

    x = int(x)
    y = int(y)

    member_label = member["label"]

    if "metadata" not in member:
      continue

    # print("create_anno", "label", member_label)

    if member_label == "脱文・錯簡":

      # descripiton = ""
      # url = ""

      metadata = member["metadata"]

      m_map = {}



      for obj in metadata:
        label = obj["label"]
        value = obj["value"]

        m_map[label] = value

        '''
        if label == "url":
          url = value
        else:
          descripiton = value
        '''

      chars = m_map["Type"]+"<p>" + m_map["Text"] + "</p><p><a href=\""+hostPrefix + "/ds"+"\" target=\"_blank\" rel=\"noopener noreferrer\">脱文錯簡リスト</p>"
      fill = "#FF0000"
      stroke = "#FF0000"

      # w = d2

      d = "M"+str(int(x))+" "+str(int(y))+" l-"+str(int(w/2))+" "+str(int(w / 1.14))+" l"+str(int(w))+" 0 z"

      dw = w /20

      d1 = "M"+str(x - dw)+" "+str(y + w * 3/10)+" l-0 "+str(w + 2/10)+" "+str(dw * 2)+" 0 l0 -"+str(w + 2/10)+" z"

      d3 = "M"+str(x - dw)+" "+str(y + w * 6.5/10)+" l-0 "+str(dw)+" "+str(dw * 2)+" 0 l0 -"+str(dw)+" z"

      opa = str(0.5)

      '''
      <path xmlns=\"http://www.w3.org/2000/svg\" d=\""+d1 + \
          "\" id=\"pin_" + "abc" + "\" fill=\"" + \
              fill+"\" stroke=\""+stroke+"\"/><path xmlns=\"http://www.w3.org/2000/svg\" d=\""+d2 + \
          "\" id=\"pin_" + "abc2" + "\" fill=\"" + \
              fill+"\" stroke=\""+stroke+"\"/>
              '''
      
      svg = "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\""+d + \
          "\" id=\"pin_" + "abc3" + "\" fill-opacity=\""+opa+"\" fill=\"" + \
              fill+"\" stroke=\""+stroke+"\"/></svg>"

      y -= d2 * 6

    else:

      page = int(member["metadata"][0]["value"])

      # https://japanknowledge.com/lib/display/?lid=80110V00200017

      if "新編日本古典文学全集" in member_label:
        sagaId = info["jk_front"][0:-3] + str(page).zfill(3)
        chars = "新編日本古典文学全集 p."+str(page)+" 開始位置<p><a href=\"https://japanknowledge.com/lib/display/?lid=" + \
                                    str(sagaId)+"\" target=\"_blank\" rel=\"noopener noreferrer\">ジャパンナレッジ Lib</a>でみる</p><p><a href=\"https://japanknowledge.com/psnl/display/?lid=" + \
                                    str(sagaId)+"\" target=\"_blank\" rel=\"noopener noreferrer\">ジャパンナレッジ Personal</a>でみる</p>"
        fill = "#2E89D9"
        stroke = "#2E89D9"

        # 新編の場合は上にずらす
        y -= d2 * 6
      else:
        ndlId = info["ndl"].split("/")[-2]

        # front 20 page 5 koui front 1

        ndlPage = info["ndl_front"] + math.floor((page - info["koui_front"] + 1) / 2)
        chars = "校異源氏物語 p."+str(page)+" 開始位置<p><a href=\"http://dl.ndl.go.jp/info:ndljp/pid/"+ndlId+"/"+str(
            ndlPage)+"\" target=\"_blank\" rel=\"noopener noreferrer\">国立国会図書館デジタルコレクション</a>でみる</p>" # 校異源氏物語を

        '''
        if page == 594 and "/東大本/" in odir:
          chars = "<div><b>【脱文あり】</b></div>" + chars
        '''

        fill = "#F3AA00"
        stroke = "#f38200"

        if info["vol"] >= 2 and info["vol"] <= 6 and "東大本" in opath and info["vol"] != 3:
          y += 200

      d = "M" + str(int(x)) + "," + str(int(y)) + "c0,-" + str(d2 * 2) + " " + str(d2) + ",-" +str(d2 * 4) + " " +str(d2 * 3) + ",-" + str(d2 * 6) + "c0,-" + str(d2 * 2) + " -" + str(d2) + ",-" + str(d2 * 3) + " -" + str(d2 * 3) + ",-" + str(d2 * 3) + "c-" + str(d2 * 2) + ",0 -" + str(d2 * 3) + "," + str(d2) + " -" + str(d2 * 3) + "," + str(d2 * 3) + "c" + str(d2 * 2) + "," + str(d2 * 2) + " " + str(d2 * 3) + "," + str(d2 * 4) + " " + str(d2 * 3) + "," + str(d2 * 6) + "z"

      opa = str(0.5)
      
      svg = "<svg xmlns='http://www.w3.org/2000/svg'><path xmlns=\"http://www.w3.org/2000/svg\" d=\""+d + \
          "\" id=\"pin_" + "abc" + "\" fill-opacity=\""+opa+"\" fill=\"" + \
              fill+"\" stroke=\""+stroke+"\"/></svg>"

    resources.append({
      "@id": annoListUri + "#" + str(i+1),
      "@type": "oa:Annotation",
      "motivation": "sc:painting",
      "on": [
          {
              "@type": "oa:SpecificResource",
              "full": canvas_id,
              "selector": {
                  "@type": "oa:Choice",
                  "default": {
                      "@type": "oa:FragmentSelector",
                      "value": "xywh=" + xywh
                  },
                  "item": {
                      "@type": "oa:SvgSelector",
                      "value": svg
                  }
              },
              "within": {
                "@id": info["manifest"],
                "@type": "sc:Manifest"
            }
          }
      ],
      "resource": {
          "@type": "dctypes:Text",
          "chars": chars,
          "format": "text/html"
      }
  })

  annoList = {
    "@context": "http://iiif.io/api/presentation/2/context.json",
    "@id": annoListUri,
    "@type": "sc:AnnotationList",
    "resources": resources
  }

  fw = open(opath, 'w')
  json.dump(annoList, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

  return annoListUri

### リターン Curation
def create_manifest(selection, info):

  within = selection["within"]

  label = within["label"] #########################

  vol = info["vol"]

  odir = dir2+"/"+label + "/" + str(vol).zfill(2)
  os.makedirs(odir, exist_ok=True)

  opath = odir+"/manifest.json"

  ##########

  members = selection["members"]
  members_map = {}
  members_map = create_members_map(members_map, members)

  # print("*", label)

  # 東大本の場合は、新編も（あれば）

  if "東大本" in label:

    try:
      with open(genji_dir + "/genji_curation/docs/iiif/saga/"+str(vol).zfill(2)+".json") as f:
        saga_curation = json.load(f)

      members = saga_curation["selections"][0]["members"]
      members_map = create_members_map(members_map, members)
    except:
      aaa = "bbb"

  ##########

  manifest_uri = selection["within"]["@id"]

  
  # print(manifest_uri)

  path = "data/"+label + "/" + str(vol).zfill(2) + "/manifest.json"

  if not os.path.exists(path):
    
    time.sleep(3)
    manifest_data = requests.get(manifest_uri).json()

    dirname = os.path.dirname(path)

    os.makedirs(dirname, exist_ok=True)

    fw = open(path, 'w')
    json.dump(manifest_data, fw, ensure_ascii=False, indent=4, separators=(',', ': '))
  
  else:
    with open(path) as f:
      manifest_data = json.load(f)

  canvases = manifest_data["sequences"][0]["canvases"]

  canvases_rev = {}

  for i in range(len(canvases)):

    canvas = canvases[i]

    canvases_rev[canvas["@id"]] = i # canvasの順番を保持

    otherContentUri = create_anno(canvas, members_map, odir, i+1, info)
    if otherContentUri:
      canvas["otherContent"] = [
          {
              "@id": otherContentUri,
              "@type": "sc:AnnotationList"
          }
      ]
    else:

      if "otherContent" in canvas:
        del canvas["otherContent"]

  ##########

  manifest_uri = opath.replace(opath.split("/data/")[0], hostPrefix)

  manifest_data["@id"] = manifest_uri
  manifest_data["label"] = label

  ##### TOCの作成

  structures = []
  manifest_data["structures"] = structures

  # print(members_map)

  count = 1

  structures_map = {}

  for canvas_id in members_map:
    members = members_map[canvas_id]

    for member in members:

      label = member["label"]
    
      if "新編日本古典文学全" in member["label"] or "源氏物語大成" in member["label"]:
        # label = member["label"]
        label = label.replace("源氏物語大成", "校異源氏物語")
        aaa = "bbb"
      elif label == "脱文・錯簡":
        # print(label)
        # print(member)
        aaa = "bbb"
      elif "metadata" in member:
        label = "校異源氏物語 p."+ str(member["metadata"][0]["value"])
      else:
        aaa = "bbb"
        # print("***********************", label, member)

      member["label"] = label #ラベルの修正

      canvas_id = member["@id"].split("#xywh=")[0]

      index = canvases_rev[canvas_id]

      x = -int(member["@id"].split("#xywh=")[1].split(",")[0].split(".")[0])

      if index not in structures_map:
        structures_map[index] = {}

      if x not in structures_map[index]:
        structures_map[index][x] = []

      structures_map[index][x].append({
        "@id": member["@id"] + "/r"+str(count),
        "@type": "sc:Range",
        "canvases": [
          canvas_id
        ],
        "label": label #member["label"]
      })

      count += 1

  for index in sorted(structures_map):
    obj = structures_map[index]
    for x in sorted(obj):
      arr = obj[x]
      for e in arr:
        structures.append(e)

  fw = open(opath, 'w')
  json.dump(manifest_data, fw, ensure_ascii=False,
            indent=4, separators=(',', ': '))

  ##########

  selection["within"]["@id"] = manifest_uri

  members = []

  for canvas_id in members_map:
    for member in members_map[canvas_id]:

      # print("aaa", member)

      page = -1
      err = False

      label = member["label"]
      
      if "metadata" not in member:
        
        if " p." in label:
          page = label.split(".")[1]
      else:
        # print(member)
        
        if label == "脱文・錯簡":
          err = True

          print(label)
        
        metadata = member["metadata"]
        for obj in metadata:
          if obj["label"] == "p":
            page = int(obj["value"])
        
      

      if page == -1 and not err:
        continue

      if not err:

        # 校異 Line IDの付与
        if "新編日本古典文学全集" not in member["label"]:
          member["lineId"] = "https://w3id.org/kouigenjimonogatari/data/" + \
                str(page).zfill(4)+"-01.json"

      # 出力用に削除
      # 錯簡は残す
      if "metadata" in member and not err:
        # del member["metadata"]
        member["metadata"] = [{
          "label" : "Page",
          "value" : label
        }]

      if "description" in member:
        del member["description"]

      members.append(member)

  selection["members"] = members

  selection["@id"] = hostPrefix + "/data/vol"+stage+"/"+str(vol).zfill(2)+"/curation.json#"+within["label"]

  return selection


def create_ndl(info):

  members = []

  vol = info["vol"]

  vol_str = str(vol).zfill(2)

  tei = "https://kouigenjimonogatari.github.io/tei/"+vol_str+".xml"

  response = requests.get(tei)
  if response.status_code < 400:

    xmlData = requests.get(tei).text

    root = ET.fromstring(xmlData)
    ET.register_namespace('', "http://www.tei-c.org/ns/1.0")

    prefix = ".//{http://www.tei-c.org/ns/1.0}"

    surfaces = root.findall(prefix+"surface")

    for surface in surfaces:
      graphic = surface.find(prefix+"graphic")
      canvas_id = graphic.get("n")

      zones = surface.findall(prefix+"zone")

      for zone in zones:

        x = int(zone.get("ulx"))
        y = int(zone.get("uly"))

        w = int(zone.get("lrx")) - x
        h = int(zone.get("lry")) - y

        xywh = str(x) + "," + str(y) + "," + str(w) + "," + str(h)

        member_id = canvas_id+"#xywh="+xywh

        zone_id = zone.get("{http://www.w3.org/XML/1998/namespace}id")
        lineId = "https://w3id.org/kouigenjimonogatari/data/" + \
            zone_id.split("_")[1]+"-01.json"

        members.append({
          "@id": member_id,
          "@type": "sc:Canvas",
          "label": "校異源氏物語 p." + str(int(lineId.split("/")[-1].split("-")[0])), # lineId,
          "lineId": lineId
        })

  selection = {
    "@id": hostPrefix + "/data/vol"+stage+"/"+vol_str+"/curation.json#校異源氏物語",
    "@type": "sc:Range",
    "label": "Manual curation by IIIF Curation Viewer",
    "members": members,
    "within": {
      "@id": info["manifest"],
      "@type": "sc:Manifest",
      "label": "校異源氏物語"
    }
  }

  return selection

def create_curations(info):
    vol = info["vol"]

    files = glob.glob(genji_dir + "/genji_curation/docs/iiif/fb2/"+str(vol).zfill(2)+"/*.json")

    orderedSelections = {}
    notOrderedSelections = []

    orderedLabels = ["東大本", "九大本（古活字版）", "九大本（無跋無刊記整版本）", "湖月抄・NIJL・鵜飼文庫本"]
    selections = []

    for file in files:
      with open(file) as f:
        df = json.load(f)

      selection = df["selections"][0]
    
    
      if "members" not in selection:
        continue
      members = selection["members"]

      # すべてのアノテーション付与が完了しているもののみ
      if len(members) != info["koui_count"]:
        # continue
        print("アノテーションが一部欠落しています！", file)

      label = selection["within"]["label"]

      if "古活字版" in label:
        label = "九大本（古活字版）"
      elif "無跋" in label or label == "源氏物語":
        label = "九大本（無跋無刊記整版本）"
      elif "湖月抄・NIJL・鵜飼文庫本" in label:
        label = "湖月抄（国文研所蔵）"

      selection["within"]["label"] = label

      if label in orderedLabels:
          orderedSelections[label] = selection

      else:
          # print("****************", label)
          notOrderedSelections.append(selection)

    for label in orderedLabels:
      if label in orderedSelections:
          selection = orderedSelections[label]
          # manifestの生成
          selectionResult = create_manifest(selection, info)
          if len(selectionResult) > 0:
              selections.append(selectionResult)

    for selection in notOrderedSelections:
      # manifestの生成
      selectionResult = create_manifest(selection, info)
      if len(selectionResult) > 0:
          selections.append(selectionResult)

    return selections

def create_image_map(info, vol, dir):
  selections = []

  selections.append(create_ndl(info))

  curations = create_curations(info)

  for selection in curations:
    selections.append(selection)

  vol_str = str(vol).zfill(2)

  curation = {
    "@context": [
      "http://iiif.io/api/presentation/2/context.json",
      "http://codh.rois.ac.jp/iiif/curation/1/context.json"
    ],
    "@id": hostPrefix + "/data/vol"+stage+"/"+vol_str+"/curation.json",
    "@type": "cr:Curation",
    "label": info["label"],
    "selections": selections
  }

  odir = dir+"/vol"+stage+"/"+vol_str
  os.makedirs(odir, exist_ok=True)

  fw = open(odir+"/curation.json", 'w')
  json.dump(curation, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

def create_config(info, vol, dir):
  
  vol_str = str(vol).zfill(2)

  url_main = "https://w3id.org/kouigenjimonogatari/tei/"+vol_str+".xml"

  # 対応付がなされていれば
  if os.path.exists(genji_dir + "/genji/static/data/tei/koui/"+vol_str+".xml"):
    url_main = hostPrefix + "/data/tei/koui/"+vol_str+".xml"
  

  config = {
    "returnUrl": hostPrefix,
    "returnLabel": "デジタル源氏物語",
    "urlMain": url_main,
    "urlSub": info["tei"],
    "imageMap": hostPrefix + "/data/vol"+stage+"/"+vol_str+"/curation.json",
    "direction": "vertical"
  }

  odir = dir+"/vol"+stage+"/"+vol_str

  os.makedirs(odir, exist_ok=True)

  fw = open(odir+"/config.json", 'w')
  json.dump(config, fw, ensure_ascii=False, indent=4, separators=(',', ': '))

if __name__ == '__main__':
  path = genji_dir + "/genji/static/data/info.json"

  with open(path) as f:
    info = json.load(f)
  # info = requests.get("https://raw.githubusercontent.com/nakamura196/genji_vue/master/docs/data/info.json").json()

  info_map = {}

  for selection in info["selections"]:
    members = selection["members"]

    manifest = selection["within"]["@id"]

    for member in members:
      metadata = member["metadata"]
      
      map = {}

      map["label"] = member["label"]
      map["manifest"] = manifest
      
      for obj in metadata:
        map[obj["label"]] = obj["value"]

        if obj["label"] == "vol":
          vol = obj["value"]

      info_map[vol] = map



  for vol in range(1, 55):

    
    if vol != 10 and False:
      continue

    print("vol", vol)
    info = info_map[vol]

    # print(info)

    create_image_map(info, vol, dir)
    create_config(info, vol, dir)

    # break
