import json
import regex
# import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from tqdm import tqdm

wc = Counter()

BASE_PATH = Path(__file__).parent
HINDI_PATH = "../../IR_Assignment_Dataset/hindi/"
SHOW_PLOT = False
SHOW_PLOT = True
TERM_PATTERN = regex.compile(r"\w+", regex.UNICODE | regex.I)

root = BASE_PATH / Path(HINDI_PATH)
processed_hindi_path = BASE_PATH / Path("./hindi_freq.json")

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
    for word in regex.findall(TERM_PATTERN, text):
        wc[word.lower()] += 1

def get_r(y_actual, y_approx):
    y_bar = sum(y_actual)/len(y_actual)
    ss_reg = sum( (yhat - y_bar)**2 for yhat in y_approx)
    ss_tot = sum( (y-y_bar)**2 for y in y_actual )
    rsqr = ss_reg / ss_tot
    return rsqr ** 0.5

def plot_word_vs_freq():
    data = wc.most_common(100)
    words, frequencies = zip(*data)
    plt.rcParams['font.family'] = 'Lohit Devanagari'
    plt.figure(figsize=(10, 6))
    plt.bar(words, frequencies, color="skyblue")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.title("Word Frequency")
    plt.xticks(rotation=90)
    plt.tight_layout()  # Adjust layout to make room for x-axis labels
    plt.show()

if not processed_hindi_path.is_file():
    errored = []
    for f in tqdm(files):
        try:
            to_words_inplace(f)
        except Exception as e:
            print(e, f)
            errored.append(f)
    with open(processed_hindi_path, "w") as f:
        json.dump(wc, f)
else:
    with open(processed_hindi_path) as f:
        wc = Counter(json.load(f))



data = wc.most_common()

if SHOW_PLOT: plot_word_vs_freq()

# on data fitting to
# $frequency \approx \frac{1}{(index + b)^a}$
# b = 2.632e-4
# a = 1.815705

b = 0
a = 1

ziphy = [
    # ((rank + b) ** (a)) * freq 
    freq
    for rank, (word, freq) in enumerate(data, start=1)
]



x = np.log10([*range(1,len(ziphy)+ 1)])
y = np.log10(ziphy)

m, b = np.polyfit(x, y, 1) # y = mx+b

plt.title("log-log plot of frequency vs rank")

plt.plot(
    x, y,
    "o",
    markersize=2,
)

yhat = m*x+b
print(f'R^2 = {get_r(y, yhat)**2}')
# plt.plot(x, yhat)
# plt.xlim(left=-0.5)

# m2, b2 = np.polyfit(x[:100], y[:100], 1)
# plt.plot(x, m2*x+b2 )

plt.ylabel("log(freq)")
plt.xlabel("log(rank)")
# plt.text(2e5, 4e6, "rank*count vs rank,\nexpected linearish for ziphy")

plt.show()
