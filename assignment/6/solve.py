#!/usr/bin/env python3

from collections import defaultdict, deque
import json
from pathlib import Path
from time import sleep
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin

CACHE_FILE_PATH = Path("records.json")

session = requests.Session()

COLORS = {
    "BLACK": "\x1b[30m",
    "RED": "\x1b[31m",
    "GREEN": "\x1b[32m",
    "YELLOW": "\x1b[33m",
    "BLUE": "\x1b[34m",
    "MAGENTA": "\x1b[35m",
    "CYAN": "\x1b[36m",
    "WHITE": "\x1b[37m",
    "RESET": "\x1b[0m",
}

seed = "https://en.wikipedia.org/wiki/Main_Page"

graph = defaultdict(set)
qu = deque([seed])
seen = {seed}

req_count = 0


def make_request(url: str):
    global req_count
    req_count += 1
    print(f"[{req_count}]> Getting {url}")
    return session.get(url)


def dump_data(file_path=CACHE_FILE_PATH):
    global graph, qu
    serializable_graph = {i: list(j) for i, j in graph.items()}
    serializable_qu = list(qu)
    with open(file_path, "w") as f:
        json.dump([serializable_graph, serializable_qu], f)


def load_data(file_path=CACHE_FILE_PATH):
    global graph, qu
    with open(file_path) as f:
        serializable_graph, serializable_qu = json.load(f)
    graph = defaultdict(set)
    for i, j in serializable_graph.items():
        graph[i] = set(j)
    qu = deque(serializable_qu)
    return graph, qu


def extract_urls(html: str, base_url: str) -> list[str]:
    soup = BeautifulSoup(html, features="html.parser")
    return [
        urljoin(base_url, anchor["href"])  # type: ignore
        for anchor in soup.find_all(
            lambda tag: tag.name == "a" and tag.has_attr("href")
        )
    ]

def main():
    if CACHE_FILE_PATH.exists() and  CACHE_FILE_PATH.is_file():
        load_data()
        return
    while qu and len(graph) < 100:
        url = qu.pop()
        res = make_request(url)
        if res.status_code != 200:
            print(res.url, res.status_code, res.content)
            sleep(1)
            continue
        urls = extract_urls(res.text, url)
        for child in urls:
            if child in seen:
                continue
            seen.add(child)
            graph[url].add(child)
            if child not in graph:
                graph[child] = {}
            qu.appendleft(child)

    dump_data()

if __name__ == "__main__":
    main()
