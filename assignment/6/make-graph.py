#!/usr/bin/env python3

from collections import defaultdict, deque
import json
from pathlib import Path
import requests

CACHE_FILE_PATH = Path("records.json")

session = requests.Session()

seed = "https://deadcells.wiki.gg/"


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
        # nodes.update(graph[node])

    nodelist = list(nodes)
    revnodes = {
        j:i for i,j in enumerate(nodelist)
    }

    DQUOTE = '"'
    ESCAPED_DQUOTE = r'\"'

    with open(GRAPH_FILE, "w") as f:
        f.write("digraph {\n\n")
        f.write(f'    node [shape=box,style=filled];\n')
        for idx, label in enumerate(nodelist):
            f.write(f'    {idx} [label="{label.replace(DQUOTE, ESCAPED_DQUOTE)}"{"" if label != seed else ",color=lightyellow,root=true"}];\n')
        f.write("\n")
        for node in graph:
            for child in graph[node]:
                if child in revnodes:
                    f.write(f'    {revnodes[node]} -> {revnodes[child]} ;\n')
        f.write("\n}")



if __name__ == "__main__":
    load_data()
    main()
