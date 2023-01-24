from dataclasses import dataclass


@dataclass
class Paper:
    title: str
    author: str  # People Name1, People Name2: split by `, `
    abstract: str
    url: str
    doi: str
    venue: str
    year: int
    month: int

    def as_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "abstract": self.abstract,
            "url": self.url,
            "doi": self.doi,
            "venue": self.venue,
            "year": self.year,
            "month": self.month,
        }

    def as_tuple(self) -> tuple:
        return (
            self.title,
            self.author,
            self.abstract,
            self.url,
            self.doi,
            self.venue,
            self.year,
            self.month,
        )

    def __getitem__(self, attr_key: str):
        return getattr(self, attr_key)

    def __hash__(self) -> int:
        return hash(self.as_tuple())
