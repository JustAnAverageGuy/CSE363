#!/usr/bin/env python3
# vim: fdm=marker

import argparse
import json
from math import log
import re
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm


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

BASE_PATH = Path(__file__).parent

RANGE = (1801, 1840)
DATASET_PATH = BASE_PATH / Path("./20_newsgroups")
CACHE_FILE = BASE_PATH / Path("wcs.json")


def get_data(file):
    with open(file, encoding="latin1") as f:
        s = f.read()
    x = s.split("\n\n", maxsplit=1)
    if len(x) == 2:
        return x[1]
    return s


PATTERN = re.compile(r"\w+")


def extract_words(data: str):
    return (i.group().lower() for i in re.finditer(PATTERN, data))


category_wc: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(lambda: 1))
priors: dict[str, int] = defaultdict(int)
total_weight_category: dict[str, int] = defaultdict(int)

# category_wc[category_name][word]     -> number of times word occurs in category_name
# priors[category_name]                -> number of document for a particular category
# total_weight_category[category_name] -> total number of words in a category

def make_counter(refresh=False):
    global category_wc
    global priors
    global total_weight_category
    if not refresh and CACHE_FILE.exists() and CACHE_FILE.is_file():
        with open(CACHE_FILE) as f: category_wc, priors, total_weight_category = json.load( f)
        return
    categories = [i for i in DATASET_PATH.iterdir()]
    for category in tqdm(categories, leave=False):
        for file in category.iterdir():
            priors[category.name] += 1
            for word in extract_words(get_data(file)):
                category_wc[category.name][word] += 1
                total_weight_category[category.name] += 1
    with open(CACHE_FILE, "w") as f:
        json.dump([category_wc, priors, total_weight_category], f)
    return

def make_prediction(file) -> str:

    words = defaultdict(int)

    for word in extract_words(get_data(file)): words[word] += 1

    catress:list[tuple[float, str]] = []

    for category in priors:
        value = log(priors[category]) # irrelevant to divide by sum(priors)
        for word, count in words.items():
            value += count * log(category_wc[category].get(word, 1))
            value -= count * log(total_weight_category[category])
        catress.append((value, category))

    return max(catress)[1]


def main():
    make_counter()

    print(f'[*] classifying files {COLORS["YELLOW"]}test_documents/{RANGE[0]}{COLORS["RESET"]} .. {COLORS["YELLOW"]}test_documents/{RANGE[1]}{COLORS["RESET"]}')

    directory = Path(ARGS.testfolder)
    files = [i for i in directory.iterdir() if RANGE[0] <= int(i.name) <= RANGE[1]]
    outfile = ARGS.outfile

    for file in sorted(files):
        predicted_class = make_prediction(file)
        outfile.write(f'{file.name}, {predicted_class}\n')
    outfile.close()
    print(f"[*] {COLORS['BLUE']}DONE{COLORS['RESET']}")
    print(f"[*] OUTPUT FILE: {COLORS['GREEN']}{outfile.name}{COLORS['RESET']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="categorizes the input files based on the dataset and Naive Bayes classifier"
    )

    parser.add_argument(
        "testfolder",
        type=str,
        help="Folder containing the test documents",
    )
    # parser.add_argument(
    #     "testfiles",
    #     nargs='+',
    #     type=argparse.FileType("r"),
    # )

    parser.add_argument(
        "outfile",
        type=argparse.FileType("w"),
        help="output file path",
    )

    ARGS = parser.parse_args()
    main()
