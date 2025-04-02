#!/usr/bin/env python3

import json
from collections import defaultdict, deque
from pathlib import Path
from random import shuffle
from time import sleep
from urllib.parse import urljoin, urlparse, urlunparse

import requests
from bs4 import BeautifulSoup

CACHE_FILE_PATH = Path("records.json")
IGNORE_CACHE = True
GRAPH_FILE = Path("graph.gv")


session = requests.Session()


seed = "https://deadcells.wiki.gg/"

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
        urljoin(base_url, urlunparse(urlparse(anchor["href"])._replace(query="")))  # type: ignore
        for anchor in soup.find_all(
            lambda tag: tag.name == "a" and tag.has_attr("href")
        )
    ]


def main():
    if not IGNORE_CACHE and CACHE_FILE_PATH.exists() and CACHE_FILE_PATH.is_file():
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
        shuffle(urls)
        for child in urls[:10]:
            if child in seen:
                continue
            seen.add(child)
            graph[url].add(child)
            qu.appendleft(child)

    dump_data()


def export_graph():
    nodes = set()
    for node in graph:
        nodes.add(node)
        # nodes.update(graph[node])

    nodelist = list(nodes)
    revnodes = {j: i for i, j in enumerate(nodelist)}

    DQUOTE = '"'
    ESCAPED_DQUOTE = r"\""

    with open(GRAPH_FILE, "w") as f:
        f.write("digraph {\n\n")
        f.write(f"    node [shape=box,style=filled];\n")
        for idx, label in enumerate(nodelist):
            f.write(
                f'    {idx} [label="{label.replace(DQUOTE, ESCAPED_DQUOTE)}"{"" if label != seed else ",color=lightyellow,root=true"}];\n'
            )
        f.write("\n")
        for node in graph:
            for child in graph[node]:
                if child in revnodes:
                    f.write(f"    {revnodes[node]} -> {revnodes[child]} ;\n")
        f.write("\n}")


if __name__ == "__main__":
    main()
    export_graph()
    # can render the graph using a variety of tools
    # e.g.
    # twopi -Tsvg graph.gv > graph.svg
    # firefox ./graph.svg
    # I manually cleaned it up using gephi
