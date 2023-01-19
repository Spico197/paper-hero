import pathlib
import re

from src.engine import SearchAPI
from src.interfaces import Paper
from src.utils import load_json, parse_bib_month


class AclanthologyPaperList(SearchAPI):
    def __init__(self, cache_filepath: pathlib.Path) -> None:
        super().__init__()

        data = load_json(cache_filepath)

        self.papers = []
        for d in data:
            authors = " , ".join(
                [self.extract_author_full(author) for author in d.get("authors", [])]
            )
            venue = d.get("venue", [])
            if venue:
                venue = venue[0]
            year = int(d.get("year", "9999"))
            month = parse_bib_month(d.get("month", "99"))
            paper = Paper(
                d.get("title", ""),
                authors,
                d.get("abstract", ""),
                d.get("url", ""),
                d.get("doi", ""),
                venue,
                year,
                month,
            )
            if not paper.title:
                continue
            self.papers.append(paper)

    def extract_author_full(self, name: str) -> str:
        match = re.search(r".*?\((.*?)\)", name)
        if match:
            return match.group(1)
        else:
            return name
