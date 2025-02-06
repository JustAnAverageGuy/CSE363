#!/usr/bin/env python3
# vim: fdm=marker nowrap

import regex
import json
from collections import defaultdict
from pathlib import Path
import sys

from tqdm import tqdm


BASE_PATH = Path(__file__).parent
DIRECTORY_PATH = "../IR_Assignment_Dataset/hindi/"
TERM_PATTERN = regex.compile(r"\w+", regex.UNICODE | regex.I)

root             = BASE_PATH /  Path(DIRECTORY_PATH)
files_list_path  = BASE_PATH /  Path("./file-order-hi.json")
postings_path    = BASE_PATH /  Path("./postings-hi.json")
word_counts_path = BASE_PATH /  Path("./term-counts-hi.json")

COLORS = {
    "BLACK"   : "\x1b[30m",
    "RED"     : "\x1b[31m",
    "GREEN"   : "\x1b[32m",
    "YELLOW"  : "\x1b[33m",
    "BLUE"    : "\x1b[34m",
    "MAGENTA" : "\x1b[35m",
    "CYAN"    : "\x1b[36m",
    "WHITE"   : "\x1b[37m",
    "RESET"   : "\x1b[0m",
}

def get_text(path):
    with open(path) as f: s = f.read()
    i = s.find("<TEXT>")
    if i == -1: return
    j = s.find("</TEXT>", i)
    if j == -1: return
    return s[i + 6 : j]


def to_words(path):
    global wc
    text = get_text(path)
    if text is None: return
    return regex.findall(TERM_PATTERN, text)


postings = defaultdict(list)
files = []
wcs = defaultdict(int)


# [[ load data ]] {{{
def load_data():
    global postings
    global files
    global wcs
    if not (files_list_path.is_file() and postings_path.is_file() and word_counts_path.is_file()):
        print("Indexing...", flush=True)
        print(f"Takes ~{COLORS['BLUE']}2.5{COLORS['RESET']} mins on my machine", flush=True)
        files = [i for i in root.glob("**/*") if i.is_file()]
        # file_ids = { j:i for i,j in enumerate(files) }
        wcs = defaultdict(int)
        for idx, fname in enumerate(tqdm(files)):
            words = to_words(fname)
            if words is None: continue
            # for word in tqdm(words, leave=False):
            for word in words:
                stemmd = word
                if postings[stemmd] and postings[stemmd][-1] == idx: 
                    wcs[stemmd] += 1
                    continue
                postings[stemmd].append(idx)
                wcs[stemmd] += 1
        with open(files_list_path,  "w") as f: json.dump([str(i) for i in files], f)
        with open(postings_path,    "w") as f: json.dump(postings,                f)
        with open(word_counts_path, "w") as f: json.dump(wcs,                     f)
    else:
        print(f"\x1b[2J\n\n{COLORS['MAGENTA']}#######################\n#### {COLORS['YELLOW']}Loading index{COLORS['MAGENTA']} ####\n#######################{COLORS['RESET']}", flush =  True)
        with open(files_list_path)   as f: files    = json.load(f)
        with open(postings_path)     as f: postings = json.load(f)
        with open(word_counts_path)  as f: wcs      = json.load(f)
# }}}

load_data()

def query(term1:str|list[int], term2:str|list[int], typ=0):#  {{{
    """
    typ 0 is AND
    typ 1 is OR
    """
    # # 2 is term1 AND NOT term2
    # # 3 is (NOT term1) AND term2
    # # 4 is (NOT term1) AND (NOT term2)
    if type(term1) is str:
        a = postings.get(term1,[])
    else:
        a = term1
    if type(term2) is str:
        b = postings.get(term2,[])
    else:
        b = term2
    pl,pr = 0,0
    res = []
    if typ == 0: # AND query{{{
        while pl < len(a) and pr < len(b):
            if a[pl] == b[pr]:
                res.append(a[pl])
                pl += 1
                pr += 1
            else:
                if a[pl] < b[pr]:
                    pl += 1
                else:
                    pr += 1
    # }}}
    elif typ == 1: # OR query {{{
        while pl < len(a) and pr < len(b):
            if a[pl] == b[pr]:
                res.append(a[pl])
                pl += 1
                pr += 1
            else:
                if a[pl] < b[pr]:
                    res.append(a[pl])
                    pl += 1
                else:
                    res.append(a[pr])
                    pr += 1
    # }}}
    # # alternative efficient way to implement some NOT queries {{{
    # elif typ == 2:
    #     while pl < len(a) and pr < len(b):
    #         if a[pl] == b[pr]:
    #             pl += 1
    #             pr += 1
    #         else:
    #             if a[pl] < b[pr]:
    #                 res.append(a[pl])
    #                 pl += 1
    #             else:
    #                 pr += 1
    #     while pl < len(a):
    #         res.append(a[pl])
    #         pl += 1
    # elif typ == 3:
    #     while pl < len(a) and pr < len(b):
    #         if a[pl] == b[pr]:
    #             pl += 1
    #             pr += 1
    #         else:
    #             if a[pl] < b[pr]:
    #                 pl += 1
    #             else:
    #                 res.append(b[pr])
    #                 pr += 1
    #     while pr < len(b):
    #         res.append(b[pr])
    #         pr += 1
    # }}}
    else:
        print(f"Unknown Query type {typ}", file=sys.stderr)
        return []
    return res # }}}

def invert(term:str|list[int]): # {{{
    res = []
    pl, pr = 0,0
    if type(term) is str:
        a = postings.get(term, [])
    else:
        a = term
    while pl < len(a) and pr < len(files):
        if a[pl] == pr:
            pl += 1
            pr += 1
        else:
            if a[pl] > pr:
                res.append(pr)
                pr += 1
            else:
                assert False, "in no case should pr be more than a[pl], that will imply missing terms"
    while pr < len(files):
        res.append(pr)
        pr += 1
    return res # }}}

def invalid(stk):
    print(f"{COLORS['RED']}Invalid{COLORS['RESET']}", file=sys.stderr, flush=True)
    print(f"stack: {stk}", file=sys.stderr, flush=True)
    return

def parse_and_eval_query(terms, calc=False):# {{{
    stk = []
    for t in terms:
        if t == '&' or t == '|':
            if len(stk) < 2: 
                invalid(stk)
                return False
            r,l = stk.pop(), stk.pop()  # noqa: E741
            if not calc:
                stk.append(f'({l}{t}{r})')
            else:
                if t == '&':
                    stk.append(query(l,r,0))
                else:
                    stk.append(query(l,r,1))
        elif t == '~':
            if len(stk) < 1: 
                invalid(stk)
                return False
            last = stk.pop()
            if not calc:
                stk.append(f'~({last})')
            else:
                stk.append(invert(last))
        else:
            if not calc:
                stk.append(f'({t})')
            else:
                stk.append(t)
    if len(stk) != 1:
        invalid(stk)
        return False

    if not calc:
        return True, stk[0]
    return stk[0]
    
# }}}

def get_input():# {{{
    inp = input(
f"""
{COLORS["YELLOW"]}----------------------------------------------------{COLORS["RESET"]}
{COLORS['YELLOW']}>{COLORS['RESET']} Query in postfix notation
{COLORS['YELLOW']}>{COLORS['RESET']} input {COLORS['RED']}EXIT{COLORS['RESET']} to exit
{COLORS['YELLOW']}>{COLORS['RESET']} available operators - AND: use {COLORS['GREEN']}"&"{COLORS['RESET']}
                      - OR : use {COLORS['GREEN']}"|"{COLORS['RESET']}
                      - NOT: use {COLORS['GREEN']}"~"{COLORS['RESET']}
{COLORS['YELLOW']}>{COLORS['RESET']} e.g.: {COLORS['MAGENTA']}"काम" "अधिक" "&"{COLORS['RESET']}
{COLORS['YELLOW']}>{COLORS['MAGENTA']} """).strip()
    if inp == "EXIT": 
        print(f'\n{COLORS["GREEN"]}bye {COLORS["CYAN"]}:){COLORS["RESET"]}')
        sys.exit()
    # print(f"got `{inp}` {inp == 'EXIT'}")
    print(COLORS["RESET"])
    return inp # }}}

def str_query(inp):# {{{
    terms = regex.findall(r'"(.+?)"', inp)
    res = parse_and_eval_query(terms, False)
    if not res: return []
    print(f"parsed query: {COLORS['GREEN']}{res[1]}{COLORS['RESET']}")
    res = parse_and_eval_query(terms, True)
    if type(res) is str:
        return postings.get(res,[])
    return res # }}}

def reldocs_name(result:list[int]):
    return [files[i] for i in result]

# [[ main loop ]] {{{
while True:
    result:list[int] = str_query(get_input())
    print(f'Got {COLORS["BLUE"]}{len(result)}{COLORS["RESET"]} matches')
    i = 0
    resp = "w"
    while i < len(result):
        resp = input(f"{COLORS['YELLOW']}|->{COLORS['RESET']} print some results? {COLORS['GREEN']}y{COLORS['RESET']}/{COLORS['GREEN']}n{COLORS['RESET']}/({COLORS['GREEN']}w{COLORS['RESET']} to save to file results.txt): ")
        if resp[0].lower() == "y": 
            print(COLORS["CYAN"])
            print(*reldocs_name(result[i:i+10]), sep="\n")
            print(COLORS["RESET"])
            i += 10
        elif resp[0].lower() == "w":
            with open("results.txt","w") as f:
                print(*reldocs_name(result), sep="\n",file=f)
            print(f"{COLORS['GREEN']}|->{COLORS['RESET']} written matches to {COLORS['YELLOW']}results.txt{COLORS['RESET']} :)")
        else:
            break# }}}
