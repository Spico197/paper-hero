import pathlib
import re

import feedparser

from src.engine import SearchAPI
from src.interfaces import Paper
from src.utils import download


class ArxivPaperList(SearchAPI):
    """arXiv API

    Inputs:
        cache_filepath: Filepath to save cached file
        use_cache: will use cached file if `True`
        raw: Raw api query, e.g. `cat:cs.CL AND ti:event`. If set, others will be disabled
        title: String of title you wanna search
        author: Author string
        abstract: Abstract string
        comment: Comment string
        category: arXiv category, e.g. "cs.CL"
        max_results: Maximal returned papers
        sort_by: `submittedDate` (default) or `lastUpdatedDate`
        sort_order: `descending` (default) or `ascending`

    Doc:
        prefix	explanation
        - ti	Title
        - au	Author
        - abs	Abstract
        - co	Comment
        - jr	Journal Reference
        - cat	Subject Category
        - rn	Report Number
        - id	Id (use id_list instead)
        - all	All of the above

        logics:
        - AND
        - OR
        - ANDNOT

        symbol	encoding	explanation
        - ( )	%28 %29	Used to group Boolean expressions for Boolean operator precedence.
        - double quotes	%22 %22	Used to group multiple words into phrases to search a particular field.
        - space	+	Used to extend a search_query to include multiple fields.

        e.g. https://export.arxiv.org/api/query?search_query=cat:cs.CL+AND+ti:event&start=0&max_results=2000&sortBy=submittedDate&sortOrder=descending

    References:
        https://arxiv.org/help/api/user-manual#title_id_published_updated
    """

    API_URL = "https://export.arxiv.org/api/query?search_query="

    def __init__(
        self,
        cache_filepath: str | pathlib.Path,
        use_cache: bool = False,
        raw: str = "",
        title: str = "",
        author: str = "",
        abstract: str = "",
        comment: str = "",
        category: str = "cs.CL",
        max_results: int = 5000,
        sort_by: str = "submittedDate",
        sort_order: str = "descending",
    ) -> None:
        super().__init__()

        if isinstance(cache_filepath, str):
            cache_filepath = pathlib.Path(cache_filepath)
        if (not cache_filepath.exists()) or (not use_cache):
            cache_filepath.parent.mkdir(parents=True, exist_ok=True)

            query: str = ""
            if raw:
                query = raw
            else:
                if title:
                    if len(query) > 0:
                        query += " AND "
                    query += f"ti:{title.strip()}"
                if author:
                    if len(query) > 0:
                        query += " AND "
                    query += f"au:{author.strip()}"
                if abstract:
                    if len(query) > 0:
                        query += " AND "
                    query += f"abs:{abstract.strip()}"
                if comment:
                    if len(query) > 0:
                        query += " AND "
                    query += f"co:{comment.strip()}"
                if category:
                    if len(query) > 0:
                        query += " AND "
                    query += f"cat:{category.strip()}"

            query = query.strip().replace(" ", "+")
            query = query.replace("(", "%28")
            query = query.replace(")", "%29")
            query = query.replace('"', "%22")

            url = f"{self.API_URL}{query}&start=0&max_results={max_results}&sortBy={sort_by}&sortOrder={sort_order}"
            download(url, cache_filepath)

        feed_string = cache_filepath.open("rt", encoding="utf8").read()
        feed = feedparser.parse(feed_string)
        for entry in feed.entries:
            author = ""
            if hasattr(entry, "authors"):
                author = " , ".join(author.name for author in entry.authors)
            url = ""
            doi = ""
            for link in entry.links:
                if link.rel == "alternate":
                    url = link.href
                if "doi" in link.href:
                    doi = link.href
            if not url:
                url = entry.links[0].href
            if sort_by == "submittedDate":
                date = entry.published_parsed
            else:
                date = entry.updated_parsed

            title = re.sub(r"[\s\n]+", " ", entry.title, flags=re.MULTILINE).strip()
            abstract = re.sub(
                r"[\s\n]+", " ", entry.summary, flags=re.MULTILINE
            ).strip()
            paper = Paper(
                title,
                author,
                abstract,
                url,
                doi,
                " , ".join([t["term"] for t in entry.tags]),
                str(date.tm_year),
                str(date.tm_mon),
            )
            self.papers.append(paper)
