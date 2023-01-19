from src.interfaces.aclanthology import AclanthologyPaperList
from src.interfaces.arxiv import ArxivPaperList
from src.utils import dump_paper_list_to_markdown_checklist

if __name__ == "__main__":
    # # use `bash scripts/get_aclanthology.sh` to download and prepare anthology data
    # acl_paper_list = AclanthologyPaperList("cache/aclanthology.json")
    # ee_query = {
    #     "title": [
    #         ["information extraction"],
    #         ["event", "extraction"],
    #         ["event", "argument", "extraction"],
    #         ["event", "detection"],
    #         ["event", "classification"],
    #         ["event", "tracking"],
    #         ["event", "relation", "extraction"],
    #     ],
    #     "venue": [
    #         ["acl"],
    #         ["emnlp"],
    #         ["naacl"],
    #         ["coling"],
    #         ["findings"],
    #         ["tacl"],
    #         ["cl"],
    #     ],
    # }
    # ee_papers = acl_paper_list.search(ee_query)
    # dump_paper_list_to_markdown_checklist(ee_papers, "results/ee-paper-list.md")

    # doc_query = {
    #     "title": [
    #         ["document-level"],
    #     ],
    #     "venue": [
    #         ["acl"],
    #         ["emnlp"],
    #         ["naacl"],
    #         ["coling"],
    #         ["findings"],
    #         ["tacl"],
    #         ["cl"],
    #     ],
    # }
    # doc_papers = acl_paper_list.search(doc_query)
    # dump_paper_list_to_markdown_checklist(doc_papers, "results/doc-paper-list.md")

    arxiv_paper_list = ArxivPaperList(
        "cache/ee-arxiv.xml",
        use_cache=True,
        title="Event Extraction OR Event Argument Extraction OR Event Detection OR Event Classification OR Event Tracking OR Event Relation Extraction OR Information Extraction",
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
        ],
        "venue": [
            ["cs.CL"],
        ],
    }
    arxiv_ee_papers = arxiv_paper_list.search(arxiv_ee_query)
    dump_paper_list_to_markdown_checklist(arxiv_ee_papers, "results/arxiv-ee-paper-list.md")
