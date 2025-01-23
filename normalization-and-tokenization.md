# Normalization and Tokenization
[Book Link](https://nlp.stanford.edu/IR-book/pdf/02voc.pdf) 

- Document Unit: ...

- Language independent stemmers
    - YASS
    - GRAS
    - FBS etc.
- Frequency Distribution of words in a document collection
    - Zipf's Law
        - Rank * frequency 󰾞 constant
        - For English, the constant is approximately equal to n/10, where n is number of unique words in the document collection
- Vocabulary growth
    - *Heaps' Law*
        - v(ocab) increases with corpus size (n)
        - $v = k \cdot n^\beta$
        - $10 \le k \le 100$
        - $\beta \approx 0.5$
    - *Luhn* Analysis
        - has to have an upper cutoff and lower cutoff
        - lower cutoff to remove rarely occurring words
        - upper cutoff to remove stop words like `and`, `the`, etc.
