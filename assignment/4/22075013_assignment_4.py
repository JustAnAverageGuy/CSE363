#!/usr/bin/env python3
# vim: fdm=marker

import argparse
from collections import defaultdict

# [ parsing files ] {{{


def parse_actual_relevancy(actual: str) -> dict[str, dict[str, bool]]:  # {{{
    "returns a defaultdict which is keyed by qnum and the values are defaultdicts having docid s as keys and isrelevant as value (default False), hence any document not mentioned is assumed irrelevant"

    parsed: dict[str, dict[str, bool]] = defaultdict(lambda: defaultdict(lambda: False))

    for i in actual.splitlines():
        qnum, itr, docid, isrel = i.split(" ")  # ignoring itr number
        assert itr == "Q0"
        parsed[qnum][docid] = isrel == "1"

    return parsed
    # }}}


def parse_predicted_relevancy( results: str,) -> dict[str, list[tuple[int, str, float]]]:  # {{{
    """
    Parses the predicted relevancy results from a string input.

    Returns a dictionary where:
        - Keys are query numbers (qnum).
        - Values are lists of tuples, each containing:
            - rank (int): The rank of the document.
            - docid (str): The document identifier.
            - score (float): The relevance score of the document.

    The results for each query are sorted by rank in ascending order.
    """
    parsed = defaultdict(list)

    for i in results.splitlines():
        qnum, itr, docid, rank, score, modelname = i.split(
            " "
        )  # ignoring itr, modelname
        assert itr == "Q0"
        assert modelname == "BM25b0.4"
        rank = int(rank)
        score = float(score)
        parsed[qnum].append((rank, docid, score))
        parsed[qnum].sort()
        # there maybe a better way given the rank information,
        # but python's sort utilizes the partial orderings nicely and hence this is good enough

    return parsed
    # }}}


# }}}



from IPython import embed # DEBUG

def compute_AP_nat(ranking:list[tuple[int, str, float]], isrelevant: dict[str, bool]):
    ...
def compute_AP_int(ranking:list[tuple[int, str, float]], isrelevant: dict[str, bool]):...

def main():
    predicted = args.queryres.read();args.queryres.close()
    actual    = args.rels.read();args.rels.close()
    qnum      = args.qnum

    predicted = parse_predicted_relevancy(predicted)
    actual    = parse_actual_relevancy(actual)

    ap_nat = compute_AP_nat(predicted[qnum], actual[qnum])
    ap_int = compute_AP_int(predicted[qnum], actual[qnum])

    embed() # DEBUG


if __name__ == "__main__":  # {{{
    parser = argparse.ArgumentParser(
        description="calculates average precision (AP) for a ranked query"
    )
    parser.add_argument(
        "queryres",
        type=argparse.FileType("r"),
        help="file containing query results",
    )
    parser.add_argument(
        "rels",
        type=argparse.FileType("r"),
        help="file containing relevancy information",
    )
    parser.add_argument(
        "qnum",
        type=str,
        help="query number to calculate AP for",
        default="52",  # my allotment
    )
    args = parser.parse_args()
    main()
# }}}
