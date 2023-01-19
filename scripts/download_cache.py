from src.utils import download

FILES = {
    "aclanthology": "https://aclanthology.org/anthology+abstracts.bib.gz",
    "dblp": "https://dblp.uni-trier.de/xml/dblp.xml.gz",
}


if __name__ == "__main__":
    # download(FILES["aclanthology"], "./cache/anthology+abstracts.bib.gz")
    download(FILES["dblp"], "./cache/dblp.xml.gz")
