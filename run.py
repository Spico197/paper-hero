from src.interfaces.aclanthology import AclanthologyPaperList
from src.utils import dump_paper_list_to_markdown_checklist

if __name__ == "__main__":
    # use `bash scripts/get_aclanthology.sh` to download and prepare anthology data
    paper_list = AclanthologyPaperList("cache/aclanthology.json")
    ee_query = {
        "title": [
            ["information extraction"],
            ["event", "extraction"],
            ["event", "argument", "extraction"],
            ["event", "detection"],
            ["event", "classification"],
            ["event", "tracking"],
            ["event", "relation", "extraction"],
        ],
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

    doc_query = {
        "title": [
            ["document-level"],
        ],
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
    doc_papers = paper_list.search(doc_query)
    dump_paper_list_to_markdown_checklist(doc_papers, "results/doc-paper-list.md")
