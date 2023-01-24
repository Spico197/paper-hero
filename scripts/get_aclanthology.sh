set -ex

mkdir cache
cd cache
if ! [ -f acl-anthology/bin/anthology/anthology.py ]; then
    git clone https://github.com/acl-org/acl-anthology
else
    cd acl-anthology
    git pull
    cd ..
fi
cd acl-anthology/bin

pip install --no-cache-dir -r ./requirements.txt

python -c '
import json
from anthology import Anthology

anthology = Anthology(importdir="../data")
pops = ["xml_booktitle", "xml_title", "xml_url", "xml_abstract"]
papers = []
for paper in anthology.papers.values():
    p = paper.as_dict()
    if "xml_abstract" in p:
        p["abstract"] = paper.get_abstract(form="latex")
    for popkey in pops:
        if popkey in p:
            p.pop(popkey)
    if "author" in p:
        p["author"] = [a[0].as_dict() for a in p["author"]]
    if "editor" in p:
        p["editor"] = [a[0].as_dict() for a in p["editor"]]
    papers.append(p)

with open("../../aclanthology.json", "wt", encoding="utf8") as fout:
    json.dump(papers, fout, ensure_ascii=False)
'
