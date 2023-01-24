import pathlib
import random
import re
import time
import logging

import requests
from tqdm import trange

from src.engine import SearchAPI
from src.interfaces import Paper
from src.utils import dump_json, load_json


logger = logging.getLogger("uvicorn.default")


class DblpPaperList(SearchAPI):
    """DBLP paper list

    Inputs:
        cache_filepath: Filepath to save cached file
        use_cache: will use cached file if `True`, otherwise download again
        query: Query string, basically the title
            you wanna search in a search box.
            Special logical grammars refer to the reference.
        max_results: Maximal returned papers
        request_time_inteval: Seconds to sleep when calling DBLP API

    References:
        https://dblp.org/faq/How+to+use+the+dblp+search+API.html
    """

    API_URL = "https://dblp.org/search/publ/api"

    def __init__(
        self,
        cache_filepath: pathlib.Path,
        use_cache: bool = False,
        query: str = "",
        max_results: int = 5000,
        request_time_inteval: float = 3,
    ) -> None:
        super().__init__()

        if isinstance(cache_filepath, str):
            cache_filepath = pathlib.Path(cache_filepath)
        if (not cache_filepath.exists()) or (not use_cache):
            query = query.strip()
            query = re.sub(r"\s+?\|\s+?", "|", query)
            query = re.sub(r"\s+", "+", query)

            searched_results = []
            # max capacity is 1000
            h = 1000
            for f in trange(0, max_results, h, desc="DBLP Downloading"):
                url = f"{self.API_URL}?q={query}&format=json&c=0&f={f}&h={h}"
                try:
                    response = requests.get(url)
                    response.raise_for_status()
                    page = response.json()
                    page_data = page["result"]["hits"]["hit"]
                    if page_data:
                        searched_results.extend(page_data)
                    else:
                        break
                except KeyboardInterrupt:
                    raise KeyboardInterrupt
                except Exception as err:
                    logger.info(err)
                    break
                time.sleep((random.random() + 0.5) * request_time_inteval)
            dump_json(searched_results, cache_filepath)

        data = load_json(cache_filepath)
        for d in data:
            # dblp does not provide abstract and month data
            authors = []
            if "authors" in d["info"]:
                if isinstance(d["info"]["authors"]["author"], dict):
                    authors.append(d["info"]["authors"]["author"]["text"])
                else:
                    authors = [a["text"] for a in d["info"]["authors"]["author"]]

            venues = []
            if "venue" in d["info"]:
                if isinstance(d["info"]["venue"], str):
                    venues.append(d["info"]["venue"])
                else:
                    for venue in d["info"]["venue"]:
                        venues.append(venue)
            paper = Paper(
                d["info"]["title"],
                " , ".join(authors),
                "",
                d["info"].get("ee", d["info"].get("url", "")),
                d["info"].get("doi", ""),
                " , ".join(venues),
                d["info"].get("year", "9999"),
                "99",
            )
            self.papers.append(paper)

    @classmethod
    def build_paper_list(
        cls, cache_filepath: str, query: dict, max_results: int = 1000
    ):
        title = query.get("title", [])
        abstract = query.get("abstract", [])

        cls_q = ""
        for t in title:
            cls_q += " ".join(t)
        for a in abstract:
            cls_q += " ".join(a)
        return cls(
            cache_filepath,
            use_cache=False,
            query=cls_q,
            max_results=max_results,
        )

    @classmethod
    def build_and_search(
        cls, cache_filepath: str, query: dict, max_results: int = 1000
    ) -> list[Paper]:
        obj = cls.build_paper_list(cache_filepath, query, max_results=max_results)
        return obj.search(query)[:max_results]
