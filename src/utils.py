import functools
import gzip
import json
import pathlib
import re
import shutil

import requests
from tqdm.auto import tqdm

from src.interfaces import Paper


def download(url: str, filepath: str) -> pathlib.Path:
    """Download file from url

    Returns:
        filepath of the saved file
    """
    r = requests.get(url, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {url} returned status code {r.status_code}")
    file_size = int(r.headers.get("Content-Length", 0))

    path = pathlib.Path(filepath).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(
        r.raw.read, decode_content=True
    )  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)

    return path


def parse_bib(
    input_filepath: pathlib.Path, output_filepath: pathlib.Path
) -> list[dict]:
    if input_filepath.suffix == ".gz":
        open_func = gzip.open
    else:
        open_func = open

    data = []
    with open_func(input_filepath, "rt", encoding="utf8") as fin:
        tot_bib_string = fin.read()
        tot_bib_string = re.sub(
            r"  and\n\s+", "  and  ", tot_bib_string, flags=re.MULTILINE
        )
        tot_entries = tot_bib_string.count("@")
        for bib in tqdm(
            re.finditer(
                r"@(\w+)\{(.+?),\n(.*?)\}$",
                tot_bib_string,
                flags=re.MULTILINE | re.DOTALL,
            ),
            desc="parse bib",
            total=tot_entries,
        ):
            bib_type = bib.group(1)
            bib_key = bib.group(2)
            bib_content = {}
            content_string = bib.group(3).strip()
            for val in re.finditer(
                r"\s*(.*?)\s*=\s*(.+?),$\n", content_string, flags=re.MULTILINE
            ):
                bib_content[val.group(1).strip()] = (
                    val.group(2).strip().removeprefix('"').removesuffix('"')
                )
            ins = {"type": bib_type, "key": bib_key, "content": bib_content}

            if bib_type == "article":
                ins["content"]["volume"] = ins["content"]["journal"]
            elif bib_type == "inproceedings":
                ins["content"]["volume"] = ins["content"]["booktitle"]

            data.append(ins)

    with open_func(output_filepath, "wt", encoding="utf8") as fout:
        json.dump(data, fout, ensure_ascii=False)

    return data


# fmt: off
MONTH_MAP = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
# fmt: one


def parse_bib_month(month: str) -> int:
    if month.isdigit():
        return int(month)
    elif month.lower() in MONTH_MAP:
        return MONTH_MAP[month.lower()]
    else:
        return 99


def load_json(filepath: pathlib.Path) -> dict | list:
    if isinstance(filepath, str):
        filepath = pathlib.Path(filepath)

    if filepath.suffix == ".gz":
        open_func = gzip.open
    else:
        open_func = open

    with open_func(filepath, "rt", encoding="utf8") as fin:
        data = json.load(fin)
        return data


def dump_json(data: list | dict, filepath: str | pathlib.Path, **kwargs):
    with open(filepath, "wt", encoding="utf8") as fout:
        json.dump(data, fout, ensure_ascii=False, **kwargs)


def load_jsonlines(filepath, **kwargs):
    data = list()
    with open(filepath, "rt", encoding="utf-8") as fin:
        for line in fin:
            line_data = json.loads(line.strip())
            data.append(line_data)
    return data


def dump_jsonlines(obj, filepath, **kwargs):
    with open(filepath, "wt", encoding="utf-8") as fout:
        for d in obj:
            line_d = json.dumps(
                d, ensure_ascii=False, **kwargs
            )
            fout.write("{}\n".format(line_d))


def dump_list_to_markdown_checklist(str_list: list[str], filepath: str | pathlib.Path):
    md_string = ""
    for string in str_list:
        md_string += f"- [ ] {string}\n"

    if isinstance(filepath, str):
        filepath = pathlib.Path(filepath)
    if not filepath.parent.exists():
        filepath.parent.mkdir(parents=True)

    with open(filepath, "wt", encoding="utf8") as fout:
        fout.write(f"{md_string}")


def dump_paper_list_to_markdown_checklist(papers: list[Paper], filepath: str | pathlib.Path):
    string_list = [
        f"[{paper.venue.upper()}, {paper.year}] [{paper.title}]({paper.url})"
        for paper in papers
    ]
    dump_list_to_markdown_checklist(string_list, filepath)


def dump_paper_list_to_jsonlines(papers: list[Paper], filepath: str | pathlib.Path):
    dump = []
    for paper in papers:
        dump.append(paper.as_dict())
    dump_jsonlines(dump, filepath)


if __name__ == "__main__":
    parse_bib(
        pathlib.Path("cache/anthology+abstracts.bib.gz"),
        pathlib.Path("cache/anthology+abstracts.json.gz"),
    )
