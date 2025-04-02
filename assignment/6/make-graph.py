#!/usr/bin/env python3

from collections import defaultdict, deque
import json
from pathlib import Path
import requests

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

def load_data(file_path=CACHE_FILE_PATH):
    global graph, qu
    with open(file_path) as f:
        serializable_graph, serializable_qu = json.load(f)
    graph = defaultdict(set)
    for i, j in serializable_graph.items():
        graph[i] = set(j)
    qu = deque(serializable_qu)
    return graph, qu

GRAPH_FILE = Path("graph.gv")

def main():
    nodes = set()
    for node in graph:
        nodes.add(node)
        nodes.update(graph[node])

    nodelist = list(nodes)
    revnodes = {
        j:i for i,j in enumerate(nodelist)
    }

    DQUOTE = '"'
    ESCAPED_DQUOTE = r'\"'

    with open(GRAPH_FILE, "w") as f:
        f.write("digraph {\n\n")
        for idx, label in enumerate(nodelist):
            f.write(f'    {idx} [label="{label.replace(DQUOTE, ESCAPED_DQUOTE)}"];\n')
        f.write("\n")
        for node in graph:
            for child in graph[node]:
                f.write(f'    {revnodes[node]} -> {revnodes[child]} ;\n')
        f.write("\n}")



if __name__ == "__main__":
    load_data()
    main()
