import json
import glob

path = "/Users/nakamurasatoru/git/d_genji/genji_curation/docs/iiif/nijl"

files = glob.glob(path + "/*.json")

for file in files:

    print(file)

    with open(file) as f:
        curation_data = json.load(f)
        if "viewingHint" in curation_data:
            del curation_data["viewingHint"]

    f2 = open(file, 'w')
    json.dump(curation_data, f2, ensure_ascii=False, indent=4,
        sort_keys=True, separators=(',', ': '))