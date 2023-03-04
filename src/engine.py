from collections import defaultdict

import spacy
from tqdm import tqdm

from src.interfaces import Paper


class SearchAPI:
    SEARCH_PRIORITY = ["year", "month", "venue", "author", "title", "abstract"]

    def __init__(self) -> None:
        self.papers: list[Paper] = []
        self.nlp = None

    def in_string(self, statement: str, string: str, lemmatization: bool = False):
        _stmt = " ".join(self.tokenize(statement, lemmatization=lemmatization))
        _string = " ".join(self.tokenize(string, lemmatization=lemmatization))

        return _stmt in _string

    def exhausted_lemma_search(
        self, query: dict[str, tuple[tuple[str]]], lemmatization: bool = False
    ) -> list[Paper]:
        """Exhausted search papers by matching query"""
        results = []
        fields = []
        time_spans = defaultdict(list)
        for f in self.SEARCH_PRIORITY:
            if f in query:
                fields.append(f)
                if f in ["year", "month"]:
                    for span in query[f]:
                        assert len(span) == 2
                        assert all(num.isdigit() for num in span)
                        time_spans[f].append((int(span[0]), int(span[1])))

        pbar = tqdm(self.papers)
        found = 0
        for p in pbar:
            for f in fields:
                matched = False
                or_statements = query[f]

                if f in time_spans:
                    for s, e in time_spans[f]:
                        if s <= p[f] <= e:
                            matched = True
                            break
                else:
                    for and_statements in or_statements:
                        if all(
                            self.in_string(stmt, p[f], lemmatization=lemmatization)
                            for stmt in and_statements
                        ):
                            matched = True
                            break
                if not matched:
                    break
            else:
                results.append(p)
                found += 1
                pbar.set_postfix({"found": found})

        return results

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
            papers = self.exhausted_lemma_search(query)
        elif method == "exhausted_lemma":
            if self.nlp is None:
                self.nlp = spacy.load("en_core_web_sm")
            papers = self.exhausted_lemma_search(query, lemmatization=True)
        else:
            raise NotImplementedError

        if papers:
            papers = sorted(set(papers), key=lambda p: (p.year, p.month), reverse=True)
        return papers

    def tokenize(self, string: str, lemmatization: bool = False) -> list[str]:
        _string = string.lower()
        if lemmatization:
            doc = self.nlp(_string)
            return [str(t.lemma_) for t in doc]
        else:
            return _string.split()

    @classmethod
    def build_paper_list(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def build_and_search(cls, *args, **kwargs) -> list[Paper]:
        raise NotImplementedError
