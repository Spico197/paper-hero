import logging
import os
import pathlib
import tempfile
import uuid

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from src.interfaces.aclanthology import AclanthologyPaperList
from src.interfaces.arxiv import ArxivPaperList
from src.interfaces.dblp import DblpPaperList
from src.utils import dump_json, load_json


class SearchQuery(BaseModel):
    method: str
    query: dict
    max_results: int = 1000
    return_content: bool = False


REMOVE_CACHE = False
ACL_CACHE_FILEPATH = "./cache/aclanthology.json"
app = FastAPI()
logger = logging.getLogger("uvicorn.default")


def get_uid():
    return uuid.uuid4().urn.split(":")[-1]


@app.get("/")
async def api():
    return FileResponse("./index.html", media_type="text/html")


@app.post("/api/")
async def api(q: SearchQuery):  # noqa: F811
    ret = {
        "ok": False,
        "cand": 0,
        "paper": 0,
        "url": "",
        "token": "",
        "msg": "",
        "content": [],
    }
    if q.method not in ["aclanthology", "arxiv", "dblp"]:
        ret["msg"] = f"{q.method} method not supported"
        return ret

    papers = []
    cache_filepath = ""
    if q.method == "aclanthology":
        cache_filepath = ACL_CACHE_FILEPATH
        plist = AclanthologyPaperList.build_paper_list(ACL_CACHE_FILEPATH)
        papers = plist.search(q.query)[: q.max_results]
        ret["ok"] = True
        ret["msg"] = f"#candidates: {len(plist.papers)}"
        ret["cand"] = len(plist.papers)
    elif q.method == "arxiv":
        _, cache_filepath = tempfile.mkstemp(
            prefix="arxiv.cache.", suffix=".xml", text=True
        )
        plist = ArxivPaperList.build_paper_list(
            cache_filepath, q.query, max_results=q.max_results
        )
        papers = plist.search(q.query)[: q.max_results]
        ret["ok"] = True
        ret["msg"] = f"#candidates: {len(plist.papers)}"
        ret["cand"] = len(plist.papers)
    elif q.method == "dblp":
        _, cache_filepath = tempfile.mkstemp(
            prefix="dblp.cache.", suffix=".json", text=True
        )
        plist = DblpPaperList.build_paper_list(
            cache_filepath, q.query, max_results=q.max_results
        )
        papers = plist.search(q.query)[: q.max_results]
        ret["ok"] = True
        ret["msg"] = f"#candidates: {len(plist.papers)}"
        ret["cand"] = len(plist.papers)

    if papers:
        papers = [p.as_dict() for p in papers]
        ret["paper"] = len(papers)
        if q.return_content:
            ret["content"] = papers
        else:
            _, result_filepath = tempfile.mkstemp(
                prefix=f"{q.method}.search.", suffix=".json", text=True
            )
            ret["url"] = result_filepath
            ret["token"] = get_uid()
            cache = {
                "token": ret["token"],
                "url": ret["url"],
                "content": papers,
            }
            dump_json(cache, result_filepath)

    if REMOVE_CACHE and q.method != "aclanthology":
        os.remove(cache_filepath)

    logger.info(
        (
            f"m: {q.method}, q: {q.query}, cands: {len(plist.papers)},"
            f" max: {q.max_results}, #papers: {len(papers)}, cache: {cache_filepath}"
            f" ret.url: {ret.get('url', '')}"
        )
    )

    return ret


@app.get("/download/")
async def download(u: str, t: str):  # noqa: F811
    logger.info(f"{u=}, {t=}")
    results_filepath = pathlib.Path(u)
    token = t
    if results_filepath.exists():
        data = load_json(results_filepath)
        if data["token"] == token:
            filename = results_filepath.name
            prefix, _, middle, suffix = filename.split(".")
            _, download_filepath = tempfile.mkstemp(
                prefix=f"{prefix}.download.", suffix=".json"
            )
            dump_json(data["content"], download_filepath, indent=2)
            logger.info(f"Download: from {u} to {download_filepath}")
            return FileResponse(download_filepath, filename=f"{prefix}.json")
    return {"ok": False, "msg": "file not exist or token mismatch"}


if __name__ == "__main__":
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = (
        "%(asctime)s | " + log_config["formatters"]["access"]["fmt"]
    )
    log_config["formatters"]["default"]["fmt"] = (
        "%(asctime)s | " + log_config["formatters"]["default"]["fmt"]
    )
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=7860,
        log_level="debug",
        log_config=log_config,
        reload=False,
    )
