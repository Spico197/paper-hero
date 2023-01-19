from dataclasses import dataclass


@dataclass
class Paper:
    title: str
    authors: str  # People Name1, People Name2: split by `, `
    abstract: str
    url: str
    doi: str
    venue: str
    year: int
    month: int

    def as_dict(self):
        return {
            "title": self.title,
            "author": self.authors,
            "abstract": self.abstract,
            "url": self.url,
            "doi": self.doi,
            "venue": self.venue,
        }

    def __getitem__(self, attr_key: str):
        return getattr(self, attr_key)
