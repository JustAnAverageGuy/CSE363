import json
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
from tqdm import tqdm

wc = Counter()
ENGLISH_PATH = "../IR_Assignment_Dataset/english/TELEGRAPH_UTF8/"
SHOW_PLOT = False

root = Path(ENGLISH_PATH)
processed_english_path = Path("english_freq.json")

files = [i for i in root.glob("**/*") if i.is_file()]


def get_text(path):
    root = ET.parse(path).getroot().find("TEXT")
    if root is not None:
        return root.text


def to_words(path):
    text = get_text(path)
    if text is None:
        return []
    words = [i.lower() for i in re.findall(r"[\w\-]+", text)]
    return words


def to_words_inplace(path):
    global wc
    text = get_text(path)
    if text is None:
        return
    for word in re.findall(r"[\w\-]+", text):
        wc[word.lower()] += 1


if not processed_english_path.is_file():
    errored = []
    for f in tqdm(files):
        try:
            to_words_inplace(f)
        except Exception as e:
            print(e, f)
            errored.append(f)
    with open(processed_english_path, "w") as f:
        json.dump(wc, f)
else:
    with open(processed_english_path) as f:
        wc = Counter(json.load(f))

if SHOW_PLOT:
    import matplotlib.pyplot as plt

    data = wc.most_common(100)
    words, frequencies = zip(*data)

    print("PLOTTING SOMETHING")
    print("""
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⠛⢩⣴⣶⣶⣶⣌⠙⠫⠛⢋⣭⣤⣤⣤⣤⡙⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⡟⢡⣾⣿⠿⣛⣛⣛⣛⣛⡳⠆⢻⣿⣿⣿⠿⠿⠷⡌⠻⣿⣿⣿⣿
    ⣿⣿⣿⣿⠏⣰⣿⣿⣴⣿⣿⣿⡿⠟⠛⠛⠒⠄⢶⣶⣶⣾⡿⠶⠒⠲⠌⢻⣿⣿
    ⣿⣿⠏⣡⢨⣝⡻⠿⣿⢛⣩⡵⠞⡫⠭⠭⣭⠭⠤⠈⠭⠒⣒⠩⠭⠭⣍⠒⠈⠛
    ⡿⢁⣾⣿⣸⣿⣿⣷⣬⡉⠁⠄⠁⠄⠄⠄⠄⠄⠄⠄⣶⠄⠄⠄⠄⠄⠄⠄⠄⢀
    ⢡⣾⣿⣿⣿⣿⣿⣿⣿⣧⡀⠄⠄⠄⠄⠄⠄⠄⢀⣠⣿⣦⣤⣀⣀⣀⣀⠄⣤⣾
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⡶⢇⣰⣿⣿⣟⠿⠿⠿⠿⠟⠁⣾⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⡟⢛⡛⠿⠿⣿⣧⣶⣶⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣧⠸⣿⣿
    ⠘⢿⣿⣿⣿⣿⣿⡇⢿⡿⠿⠦⣤⣈⣙⡛⠿⠿⠿⣿⣿⣿⣿⠿⠿⠟⠛⡀⢻⣿
    ⠄⠄⠉⠻⢿⣿⣿⣷⣬⣙⠳⠶⢶⣤⣍⣙⡛⠓⠒⠶⠶⠶⠶⠖⢒⣛⣛⠁⣾⣿
    ⠄⠄⠄⠄⠄⠈⠛⠛⠿⠿⣿⣷⣤⣤⣈⣉⣛⣛⣛⡛⠛⠛⠿⠿⠿⠟⢋⣼⣿⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠉⠉⣻⣿⣿⣿⣿⡿⠿⠛⠃⠄⠙⠛⠿⢿⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢬⣭⣭⡶⠖⣢⣦⣀⠄⠄⠄⠄⢀⣤⣾⣿
    ⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢰⣶⣶⣶⣾⣿⣿⣿⣿⣷⡄⠄⢠⣾⣿⣿⣿
    """)
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Word Frequency")
    plt.xticks(rotation=90)
    plt.tight_layout()  # Adjust layout to make room for x-axis labels
    plt.show()

data = wc.most_common()

# on data fitting to
# $frequency \approx \frac{1}{(index + b)^a}$

# b = 2.632e-4
# a = 1.815705

b = 0
a = 1

ziphy = [
    ((rank + b) ** (a)) * freq 
    # freq
    for rank, (word, freq) in enumerate(data, start=1)
]


plt.plot(
    [*range(len(ziphy))],
    ziphy,
    "o",
    markersize=3,
)

plt.xlabel("rank")
plt.ylabel("rank * count")
plt.text(2e5, 4e6, "rank*count vs rank,\nexpected linearish for ziphy")
plt.title("english verdict: not ziphy")

plt.show()
