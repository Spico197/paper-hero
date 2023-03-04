---
title: Paper Hero
emoji: 💪
colorFrom: indigo
colorTo: yellow
sdk: docker
app_port: 7860
pinned: true
license: apache-2.0
---
![hf workflow](https://github.com/Spico197/paper-hero/actions/workflows/hf_spaces.yml/badge.svg)


# 💪 Paper Hero

A toolkit to help search for papers from aclanthology, arXiv and dblp.

🎉 We have a live demo at hugginface spaces. Check it out [[here]](https://huggingface.co/spaces/Spico/paper-hero) !

## 🌴 Setup

1. Make sure you have [Git](https://git-scm.com/) and [Python](https://www.python.org/downloads/) 3.10.8 installed (or Python >= 3.9).
2. Install dependencies: `pip install -r requirements.txt`, `python -m spacy download en_core_web_sm`

## 🚀 QuickStart

Run the example in `run.py`:

```bash
# clone this repo
$ git clone https://github.com/Spico197/paper-hero.git
$ cd paper-hero
# download and install dependencies
$ pip install -r requirements.txt
$ python -m spacy download en_core_web_sm
# get ready for the acl data, since it is cache-based
$ bash scripts/get_aclanthology.sh
$ python run.py
# the results will be saved into `results/`, check them out 🎉
$ ls results
```

```python
from src.interfaces.aclanthology import AclanthologyPaperList
from src.utils import dump_paper_list_to_markdown_checklist

if __name__ == "__main__":
    # use `bash scripts/get_aclanthology.sh` to download and prepare anthology data first
    paper_list = AclanthologyPaperList("cache/aclanthology.json")
    ee_query = {
        "title": [
            # Any of the strings below is matched
            ["information extraction"],
            ["event", "extraction"],    # title must include `event` and `extraction`
            ["event", "argument", "extraction"],
            ["event", "detection"],
            ["event", "classification"],
            ["event", "tracking"],
            ["event", "relation", "extraction"],
        ],
        # Besides the title constraint, venue must also meet the needs
        "venue": [
            ["acl"],
            ["emnlp"],
            ["naacl"],
            ["coling"],
            ["findings"],
            ["tacl"],
            ["cl"],
        ],
    }
    ee_papers = paper_list.search(ee_query)
    dump_paper_list_to_markdown_checklist(ee_papers, "results/ee-paper-list.md")
```

## 🪧 Live Demo Usage

https://user-images.githubusercontent.com/22840952/214235971-fb685f82-ff24-4854-9922-dc5554e4951f.mp4

## 🗺️ Roadmap

- [x] aclanthology
- [x] arXiv
- [x] dblp
- [x] add frontend support for building a demo
- [x] year and month searching
