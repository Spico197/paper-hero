# 💪 Paper Hero

A toolkit to help search for papers from aclanthology, arXiv and dblp.

## 🌴 Setup

1. Make sure you have [Git](https://git-scm.com/) and [Python](https://www.python.org/downloads/) 3.10.8 installed (or Python >= 3.9).
2. Install dependencies: `pip install -r requirements.txt`

## 🚀 QuickStart

Run the example in `run.py`:

```bash
$ python run.py
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

## 🗺️ Roadmap

- [x] aclanthology
- [x] arXiv
- [x] dblp
