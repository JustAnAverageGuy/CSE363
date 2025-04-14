#!/usr/bin/env python3

Graph = dict[str, list[str]]


def hits(graph):
    raise NotImplementedError

 # {{{ pagerank
def pagerank(graph: Graph, alpha=0.1, iterations=100) -> dict[str, float]:
    "graph: adjacency list, alpha: teleportation probability"

    distribution = {i: 1 / len(graph) for i in graph}

    for i in range(iterations):
        new_rank = {node: 0.0 for node in graph}
        for node, neighbours in graph.items():
            # link traversal
            for n in neighbours:
                new_rank[n] += (1 - alpha) * distribution[node] / len(neighbours)
            # teleportation
            val = (
                (alpha if len(neighbours) != 0 else 1) * distribution[node] / len(graph)
            )
            for n in graph:
                new_rank[n] += val
        distribution = new_rank.copy()

    return distribution
# }}}

def print_graph_as_txt(graph:Graph):
    for node, neighbours in graph.items():
        print(f' {node} -> {"  ".join(neighbours)}')

# {{{ export graph as graphviz
def print_graph(graph: Graph, outfile="graph.gv", labels: None | dict[str, str] = None):
    with open(outfile, "w") as f:
        f.write("#!/home/aks/.local/bin/showgraph\n")
        f.write("digraph G {\n")
        f.write("    node [shape=box];\n\n")
        f.write("    edge [arrowsize=0.5];\n\n")
        for node, neighbours in graph.items():
            if labels is not None and node in labels:
                f.write(f'    {node} [label="{labels[node]}"];')
            if neighbours:
                f.write(f"    {node} -> {{{','.join(neighbours)}}};\n")
            else:
                f.write(f"    {node};\n")
        f.write("}\n")
    print(f"> written graph to {outfile}")
# }}}

def main():

    # graph taken from the book, Example 21.1 (figure 21.4)
    graph = {
        '0': ['2'],
        '1': ['1', '2'],
        '2': ['0', '2', '3'],
        '3': ['3', '4'],
        '4': ['6'],
        '5': ['5', '6'],
        '6': ['3', '4', '6'],
    }


    print("input graph:")
    print_graph_as_txt(graph)

    print("\n---------------")

    res = pagerank(graph, 0.14)

    print('node : pagerank')
    print('---------------')
    for node, val in res.items():
        print(f"{node:5}: {val:.3f}")
    print('---------------')

    print_graph(graph, labels={i: f"{i} | {j:.3f}" for i, j in res.items()})
    # print_graph(graph)


if __name__ == "__main__":
    main()

# vim: fdm=marker
