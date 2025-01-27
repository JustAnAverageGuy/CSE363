import json
import regex
# import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from tqdm import tqdm

wc = Counter()

BASE_PATH = Path(__file__).parent
HINDI_PATH = "../../IR_Assignment_Dataset/english/"
TERM_PATTERN = regex.compile(r"\w+", regex.UNICODE | regex.I)

root = BASE_PATH / Path(HINDI_PATH)
processed_hindi_path = BASE_PATH / Path("./english_terms.json")

files = [i for i in root.glob("**/*") if i.is_file()]


def get_text(path):
    # root = ET.parse(path).getroot().find("TEXT")
    # if root is not None:
    #     return root.text
    with open(path) as f:
        s = f.read()
    i = s.find('<TEXT>')
    if i == -1: return
    j = s.find('</TEXT>', i)
    if j == -1: return
    return s[i+6:j]


def to_words(path):
    text = get_text(path)
    if text is None:
        return []
    words = [i.lower() for i in regex.findall(TERM_PATTERN, text)]
    return words


def to_words_inplace(path):
    global wc
    text = get_text(path)
    if text is None:
        return
    for word in regex.findall(TERM_PATTERN, text): wc[word.lower()] += 1

if not processed_hindi_path.is_file():
    errored = []
    for f in tqdm(files):
        try:
            to_words_inplace(f)
        except Exception as e:
            print(e, f)
            errored.append(f)
    with open(processed_hindi_path, "w") as f:
        json.dump(list(wc), f)
else:
    with open(processed_hindi_path) as f:
        wc = list(json.load(f))

