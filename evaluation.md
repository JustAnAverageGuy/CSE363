
## what to evaulate

-  coverage of information
- form of presentatino
- effort required/ ease of use
- time and space efficiency

## Metrics

### Recall

Proportion of relevant materials actually retrieved

TP / (TP + FN)

### Precision

Proportion of retrieved material actually relevant

TP/(TP+FP)

### P@K

Precision after retrieving K documents

- R-Precision = Precision after retrieving R dcouments, where R is the total
number of relevant documents for a query
    - At this point, precision = recall, since (number of retrieved docs  = number
of relevant docs)

Area fo Precsision vs Recall curve = Average Precision

### Reciprocal Rank

Reciprocal Rank = $\frac{1}{rank of first relevant doc}$

MRR = Mean Reciprocal Rank

## Identifying relevant documents

### Pooling

Exhaustively judging each and every doc for a query is impossible for a large collection.
The doc-collection and the query set are shared among diff diverse systems and they are asked to retrieve at least 1000 docs for each query in descending order of the similarity scores to each query

- Use multiple systems (say n $\approx$ 10)
- for each query, ask each system to retrieve ~1000 documents it considers most relevant (i.e. ranked retrieval)
- Create a pool of top-k (~100) docs form the ranked list of retrieved docs
- This pool is exhaustively judged for each query

*Assumptions*

- All the rel docs are retrieved and belong to the pool
- there are no reldocs outside the pool created for each query

If the K is sufficiently deep and n is adequately large, the assumptions give reliable estimates of reldocs

