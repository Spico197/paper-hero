from src.interfaces.aclanthology import AclanthologyPaperList
from src.interfaces.arxiv import ArxivPaperList
from src.interfaces.dblp import DblpPaperList
from src.utils import (
    dump_paper_list_to_jsonlines,
    dump_paper_list_to_markdown_checklist,
)

if __name__ == "__main__":
    # use `bash scripts/get_aclanthology.sh` to download and prepare anthology data first
    acl_paper_list = AclanthologyPaperList("cache/aclanthology.json")
    ee_query = {
        "title": [
            ["information extraction"],
            ["event", "extraction"],
            ["event", "argument", "extraction"],
            ["event", "detection"],
            ["event", "classification"],
            ["event", "tracking"],
            ["event", "relation", "extraction"],
            ["event", "prediction"],
            ["script", "learning"],
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
    ee_papers = acl_paper_list.search(ee_query)
    dump_paper_list_to_markdown_checklist(ee_papers, "results/ee-paper-list.md")
    dump_paper_list_to_jsonlines(ee_papers, "results/ee-paper-list.jsonl")

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
    doc_papers = acl_paper_list.search(doc_query)
    dump_paper_list_to_markdown_checklist(doc_papers, "results/doc-paper-list.md")
    dump_paper_list_to_jsonlines(doc_papers, "results/doc-paper-list.jsonl")

    # arxiv papers
    arxiv_paper_list = ArxivPaperList(
        "cache/ee-arxiv.xml",
        use_cache=True,
        title=(
            "Event Extraction OR Event Argument Extraction OR Event Detection"
            " OR Event Classification OR Event Tracking"
            " OR Event Relation Extraction OR Information Extraction"
            " OR Event Prediction OR Script Learning"
        ),
        category="cs.CL",
    )
    arxiv_ee_query = {
        "title": [
            ["information extraction"],
            ["event", "extraction"],
            ["event", "argument", "extraction"],
            ["event", "detection"],
            ["event", "classification"],
            ["event", "tracking"],
            ["event", "relation", "extraction"],
            ["event", "prediction"],
            ["script", "learning"],
        ],
        "venue": [
            ["cs.CL"],
        ],
    }
    arxiv_ee_papers = arxiv_paper_list.search(arxiv_ee_query)
    dump_paper_list_to_markdown_checklist(
        arxiv_ee_papers, "results/arxiv-ee-paper-list.md"
    )
    dump_paper_list_to_jsonlines(arxiv_ee_papers, "results/arxiv-ee-paper-list.jsonl")

    # dblp papers
    dblp_paper_list = DblpPaperList(
        "./cache/dblp.json",
        use_cache=True,
        query="Event|Information|Argument|Script Extraction|Classification|Tracking|Prediction|Learning",
        max_results=50000,
    )
    dblp_ee_query = {
        "title": [
            ["information extraction"],
            ["event", "extraction"],
            ["event", "argument", "extraction"],
            ["event", "detection"],
            ["event", "classification"],
            ["event", "tracking"],
            ["event", "relation", "extraction"],
            ["event", "prediction"],
            ["script", "learning"],
        ],
        "venue": [
            ["aaai"],
            ["ijcai"],
            ["icml"],
            ["iclr"],
            ["nips"],
            ["neurips"],
            ["sigir"],
            ["cvpr"],
            ["iccv"],
        ],
    }
    dblp_ee_papers = dblp_paper_list.search(dblp_ee_query)
    dump_paper_list_to_markdown_checklist(
        dblp_ee_papers, "results/dblp-ee-paper-list.md"
    )
    dump_paper_list_to_jsonlines(dblp_ee_papers, "results/dblp-ee-paper-list.jsonl")
