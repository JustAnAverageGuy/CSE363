#!/usr/bin/env python3
# vim: fdm=marker nowrap

from heapq import heappushpop
import json
import re as regex
from collections import defaultdict
from pathlib import Path
import sys
from math import log

from nltk.stem.snowball import EnglishStemmer as stemmer
from tqdm import tqdm


BASE_PATH = Path(__file__).parent
DIRECTORY_PATH = "../IR_Assignment_Dataset/english/"
TERM_PATTERN = regex.compile(r"[a-zA-Z\-]+")

# Maximum number of documents which will be retrieved
DOCS_RETRIEVED = 50


###  Note
###  Keys in key/value pairs of JSON are always of the type str.
###  When a dictionary is converted into JSON, all the keys of the dictionary are coerced to strings.
###  As a result of this, if a dictionary is converted into JSON and then back into a dictionary,
###  the dictionary may not equal the original one.
###  That is, loads(dumps(x)) != x if x has non-string keys.
# hence I have explicitly converted keys to strs

root = BASE_PATH / Path(DIRECTORY_PATH)
files_list_path = BASE_PATH / Path("./file-order-en.json")
vocabulary_path = BASE_PATH / Path("./vocab-en.json")
doc_vs_termcounts_path = BASE_PATH / Path("./doc-term-count-en.json")


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


def get_text(path):  # {{{
    with open(path) as f:
        s = f.read()
    i = s.find("<TEXT>")
    if i == -1:
        return
    j = s.find("</TEXT>", i)
    if j == -1:
        return
    return s[i + 6 : j]


# }}}


def to_words(path):  # {{{
    global wc
    text = get_text(path)
    if text is None:
        return
    return regex.findall(TERM_PATTERN, text)  # }}}


files = []
vocab = []  # vocab is a list of uniq terms
inv_vocab = {}  # inv_vocab is a dictionary with inverse indices in vocab
file_vs_term_counts = defaultdict(lambda: defaultdict(int))
# dictionary with
#   {
#       docid : {
#        term_idx : count_of_term_in_doc, # eventually modified inplace to have tf*idf weights
#       },
#   }
idf = {}


sno = stemmer(ignore_stopwords=True)


# [[ load data ]] {{{
def load_data():
    global files
    global vocab
    global inv_vocab
    global file_vs_term_counts
    global idf
    if not (
        files_list_path.is_file()
        and vocabulary_path.is_file()
        and doc_vs_termcounts_path.is_file()
    ):
        print("Indexing...", flush=True)
        print(
            f"Takes ~{COLORS['BLUE']}9{COLORS['RESET']} mins on my machine",
            flush=True,
        )
        files = [i for i in root.glob("**/*") if i.is_file()]
        df_frequencies = defaultdict(
            int
        )  # I know it expands to 'document frequency frequencies', but whatever
        print("> Collecting term/document frequencies", flush=True)
        for idx, fname in enumerate(tqdm(files)):
            words = to_words(fname)
            if words is None:
                continue
            for word in words:
                stemmd = sno.stem(word).lower()
                if stemmd in sno.stopwords:
                    continue
                if stemmd not in inv_vocab:
                    inv_vocab[stemmd] = str(len(vocab))
                    vocab.append(stemmd)
                file_vs_term_counts[str(idx)][str(inv_vocab[stemmd])] += 1
                if file_vs_term_counts[str(idx)][str(inv_vocab[stemmd])] == 1:
                    df_frequencies[str(inv_vocab[stemmd])] += 1

        print("> computing idf from dfs", flush=True)
        lg_N = log(len(files))
        for c, cnt in tqdm(df_frequencies.items()):
            idf[str(c)] = lg_N - log(cnt)

        print("> for each term, computing the weights", flush=True)
        for idx in tqdm(file_vs_term_counts):
            for wrd in file_vs_term_counts[idx]:
                file_vs_term_counts[idx][wrd] = idf[wrd] * (
                    1 + log(1 + file_vs_term_counts[idx][wrd])
                )

        print("> normalizing the weight for each document", flush=True)
        for idx in tqdm(file_vs_term_counts):
            norm = sum(j * j for j in file_vs_term_counts[idx].values()) ** 0.5
            for wrd in file_vs_term_counts[idx]:
                file_vs_term_counts[idx][wrd] /= norm

        with open(files_list_path, "w") as f:
            json.dump([str(i) for i in files], f)
        with open(vocabulary_path, "w") as f:
            json.dump([vocab, inv_vocab, idf], f)
        with open(doc_vs_termcounts_path, "w") as f:
            json.dump(file_vs_term_counts, f)
    else:
        print(
            f"\x1b[2J\n\n{COLORS['MAGENTA']}###################################\n#### {COLORS['YELLOW']}Loading index, takes ~{COLORS['BLUE']}20{COLORS['YELLOW']}s{COLORS['MAGENTA']} ####\n###################################{COLORS['RESET']}",
            flush=True,
        )
        with open(files_list_path) as f:
            files = json.load(f)
        with open(vocabulary_path) as f:
            vocab, inv_vocab, idf = json.load(f)
        with open(doc_vs_termcounts_path) as f:
            file_vs_term_counts = json.load(f)


# }}}

load_data()


# [prompt for query]{{{
def get_input():
    inp = input(
        f"""
{COLORS["YELLOW"]}----------------------------------------------------{COLORS["RESET"]}
{COLORS["YELLOW"]}>{COLORS["RESET"]} Query as a sequence of double quoted terms
{COLORS["YELLOW"]}>{COLORS["RESET"]} input {COLORS["RED"]}EXIT{COLORS["RESET"]} to exit
{COLORS["YELLOW"]}>{COLORS["RESET"]} e.g.: {COLORS["MAGENTA"]}"short" "watch"{COLORS["RESET"]}
{COLORS["YELLOW"]}>{COLORS["RESET"]} e.g.: {COLORS["MAGENTA"]}"hello" "world" "web"{COLORS["RESET"]}
{COLORS["YELLOW"]}>{COLORS["MAGENTA"]} """
    ).strip()
    if inp == "EXIT":
        print(f"\n{COLORS['GREEN']}bye {COLORS['CYAN']}:){COLORS['RESET']}")
        sys.exit()
    # print(f"got `{inp}` {inp == 'EXIT'}")
    print(COLORS["RESET"])
    return inp  # }}}


# [parse and run query] {{{
def str_query(inp):
    terms = regex.findall(r'"(.+?)"', inp)
    print(
        f"{COLORS['YELLOW']}[*]{COLORS['RESET']} parsed query: {COLORS['GREEN']}{' '.join(terms)}{COLORS['RESET']}"
    )
    query = defaultdict(int)
    for word in terms:
        stemmd = sno.stem(word).lower()
        if stemmd in sno.stopwords:
            continue
        if stemmd not in inv_vocab:
            continue
        query[stemmd] += 1
    for word in query:
        query[word] = (1 + log(1 + query[word])) * idf[inv_vocab[word]]
    print(
        f'{COLORS["YELLOW"]}[*]{COLORS["RESET"]} Unnormalized "query vector": {COLORS["BLUE"]}{query}{COLORS["RESET"]}',
        flush=True,
    )

    res = [(0.0, "")] * DOCS_RETRIEVED
    for fidx in file_vs_term_counts:
        s = 0
        for term, weigh in query.items():
            termid = inv_vocab[term]
            s += file_vs_term_counts[fidx].get(termid, 0) * weigh
        if res[0][0] < s:
            heappushpop(res, (s, fidx))
    res.sort(reverse=True)
    return [i for i in res if i != (0.0, "")]  # }}}


# [interpret results] {{{
def reldocs_name(result: list[tuple[float, str]], with_color=True):
    if with_color:
        return [
            f"{COLORS['GREEN']}{i[0]:6.4}{COLORS['CYAN']} {files[int(i[1])]}"
            for i in result
        ]
    return [f"{i[0]:6.4} {files[int(i[1])]}" for i in result]


# }}}

# [[ main loop ]] {{{
while True:
    result: list[tuple[float, str]] = str_query(get_input())
    print(
        f"{COLORS['GREEN']}[#]{COLORS['RESET']} Got {COLORS['BLUE']}{'>=' if len(result) == DOCS_RETRIEVED else ''}{len(result)}{COLORS['RESET']} matches"
    )
    # print(result)
    # continue
    i = 0
    resp = "w"
    while i < len(result):
        resp = input(
            f"{COLORS['YELLOW']}|->{COLORS['RESET']} print some results? {COLORS['GREEN']}y{COLORS['RESET']}/{COLORS['GREEN']}n{COLORS['RESET']}/({COLORS['GREEN']}w{COLORS['RESET']} to save to file results.txt): "
        )
        if resp[0].lower() == "y":
            print(COLORS["CYAN"])
            print(*reldocs_name(result[i : i + 10]), sep="\n")
            print(COLORS["RESET"])
            i += 10
        elif resp[0].lower() == "w":
            with open("results.txt", "w") as f:
                print(*reldocs_name(result, with_color=False), sep="\n", file=f)
            print(
                f"{COLORS['GREEN']}|->{COLORS['RESET']} written matches to {COLORS['YELLOW']}results.txt{COLORS['RESET']} :)"
            )
        else:
            break  # }}}
