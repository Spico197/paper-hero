from src.interfaces import Paper


class SearchAPI:
    SEARCH_PRIORITY = ["year", "month", "venue", "author", "title", "abstract"]

    def __init__(self) -> None:
        self.papers: list[Paper] = []

    def exhausted_search(self, query: dict[str, tuple[tuple[str]]]) -> list[Paper]:
        """Exhausted search papers by matching query"""
        def _in_string(statement, string):
            stmt_in_string = False
            if " " in statement and statement.lower() in string.lower():
                stmt_in_string = True
            else:
                tokens = self.tokenize(string.lower())
                if statement.lower() in tokens:
                    stmt_in_string = True
            return stmt_in_string

        papers = self.papers
        for field in self.SEARCH_PRIORITY:
            if field in query:
                req = query[field]
                time_spans = []
                if field in ["year", "month"]:
                    for span in req:
                        assert len(span) == 2
                        assert all(num.isdigit() for num in span)
                        time_spans.append((int(span[0]), int(span[1])))

                paper_indices = []
                for i, p in enumerate(papers):
                    matched = False
                    if time_spans:
                        if any(s <= p[field] <= e for s, e in time_spans):
                            matched = True
                    else:
                        if any(
                            all(
                                _in_string(stmt, p[field])
                                for stmt in and_statements
                            )
                            for and_statements in req
                        ):
                            matched = True

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

    @classmethod
    def build_paper_list(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def build_and_search(cls, *args, **kwargs) -> list[Paper]:
        raise NotImplementedError
