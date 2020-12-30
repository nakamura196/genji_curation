import json
import requests

class Item:

    @classmethod
    def main(self, opath, uris):

        map = {}

        flg_right_to_left = True

        for uri in uris:

            df = requests.get(uri).json()

            members = df["selections"][0]["members"]
            manifest = df["selections"][0]["within"]["@id"]

            if manifest not in map:
                map[manifest] = {}

            tmp = {}

            start = ""

            for member in members:
                value = member["metadata"][0]["value"][0]
                marker = value["resource"]["marker"]

                id = value["@id"]

                if "next_line" in marker and "prev_line" not in marker:
                    start = id
                
                member_id = value["on"].split("#xywh=")
                marker["canvas_id"] = member_id[0]
                marker["xywh"] = member_id[1].split(",")

                tmp[id] = marker
            
            members_map = self.getText(start, tmp, {})

            for canvas_id in members_map:
                if canvas_id not in map[manifest]:
                    map[manifest][canvas_id] = {}

                tmp = map[manifest][canvas_id]
                for x in members_map[canvas_id]:
                    if x not in tmp:
                        tmp[x] = []
                    
                    for member in members_map[canvas_id][x]:

                        tmp[x].append(member)

        for manifest in map:

            members_map = map[manifest]

            members = []

            manifest_data = requests.get(manifest).json()

            for canvas in manifest_data["sequences"][0]["canvases"]:
                canvas_id = canvas["@id"]

                text = ""

                if canvas_id in members_map:
                    tmp = members_map[canvas_id]

                    keys = sorted(tmp, reverse=flg_right_to_left)

                    for x in keys:
                        arr = tmp[x]
                        for obj in arr:
                            members.append(obj)

                            text += obj["label"] + "\n"

                # print(text)

            curation = {
                "@context": [
                    "http://iiif.io/api/presentation/2/context.json",
                    "http://codh.rois.ac.jp/iiif/curation/1/context.json"
                ],
                "@id": manifest + "/curation.json",
                "@type": "cr:Curation",
                "label": "Character List",
                "selections": [
                    {
                        "@id": manifest + "/range1",
                        "@type": "sc:Range",
                        "label": "Characters",
                        "members": members,
                        "within": {
                            "@id": manifest,
                            "@type": "sc:Manifest",
                            "label": manifest_data["label"]
                        }
                    }
                ]
            }

            f2 = open(opath, 'w')
            json.dump(curation, f2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    @classmethod
    def getLine(self, start, map):
        text = ""
        uri = start
        flg = True

        x_min = 1000000000
        y_min = 1000000000
        x_max = -1
        y_max = -1

        while flg:

            obj = map[uri]

            text += obj["text"]

            x = int(obj["xywh"][0])
            y = int(obj["xywh"][1])
            xw = x + 1
            yh = y + 1

            if x < x_min:
                x_min = x
            if y < y_min:
                y_min = y
            if xw > x_max:
                x_max = xw
            if yh > y_max:
                y_max = yh

            if "next" not in obj:
                flg = False
            else:
                uri = obj["next"]

        member_id = obj["canvas_id"].split("#xywh=")[0] + "#xywh=" + ",".join([str(x_min), str(y_min), str(x_max - x_min), str(y_max - y_min)])

        member = {
            "@id": member_id,
            "@type": "sc:Canvas",
            "label": text,
            "metadata": [
                {
                    "label": "Text",
                    "value": text
                }
            ]
        }

        return member, obj["canvas_id"], x_min

    @classmethod
    def getText(self, start, map, members):

        if start == "":
            return members

        # startに基づき、行のmember, canvas_id, x座標を取得する
        member, canvas_id, x = self.getLine(start, map)
        
        # 結果をmembersに追加

        # ① canvas_id毎
        if canvas_id not in members:
            members[canvas_id] = {}

        # ② x座標毎
        if x not in members[canvas_id]:
            members[canvas_id][x] = []

        members[canvas_id][x].append(member)

        # 次の行があれば繰り返す
        if "next_line" in map[start]:
            members = self.getText(map[start]["next_line"], map, members)    

        return members

###############################