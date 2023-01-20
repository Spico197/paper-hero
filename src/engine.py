from src.interfaces import Paper


class SearchAPI:
    # fmt: off
    SEARCH_PRIORITY = ["doi", "url", "year", "month", "venue", "authors", "title", "abstract"]
    # fmt: on

    def __init__(self) -> None:
        self.papers: list[Paper] = []

    def exhausted_search(self, query: dict[str, tuple[tuple[str]]]) -> list[Paper]:
        """Exhausted search papers by matching query"""
        papers = self.papers
        for field in self.SEARCH_PRIORITY:
            if field in query:
                req = query[field]
                paper_indices = []
                for i, p in enumerate(papers):
                    for or_conditions in req:
                        matched = True
                        for and_cond_string in or_conditions:
                            if " " in and_cond_string:
                                if not and_cond_string.lower() in p[field].lower():
                                    matched = False
                                    break
                            else:
                                p_field = self.tokenize(p[field].lower())
                                if not and_cond_string.lower() in p_field:
                                    matched = False
                                    break
                        if matched:
                            paper_indices.append(i)
                papers = [papers[i] for i in paper_indices]

        return papers

    def search(
        self, query: dict[str, tuple[tuple[str]]], method: str = "exhausted"
    ) -> list[Paper]:
        """Search papers

        Args:
            query: A dict of queries on different field.
                A query in a field is a tuple of strings, where strings are AND
                and tuple means OR. Strings are case-insensitive.
                e.g. {
                    "venue": (("EMNLP", ), ("ACL",)),
                    "title": (("parsing", "tree-crf"), ("event extraction",))
                }
                This query means we want to find papers in EMNLP or ACL,
                AND the title either contains ("parsing" AND "tree-crf") OR "event extraction"
            method: choice from:
                - `exhausted`: brute force mathing

        Returns:
            a list of `Paper`
        """
        papers = []
        if method == "exhausted":
            papers = self.exhausted_search(query)
        else:
            raise NotImplementedError

        if papers:
            papers = sorted(set(papers), key=lambda p: (p.year, p.month), reverse=True)
        return papers

    def tokenize(self, string: str) -> list[str]:
        return string.lower().split()
