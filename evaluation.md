
## what to evaulate

-  coverage of information
- form of presentatino
- effort required/ ease of use
- time and space efficiency

## Metrics

### Recall

Proportion of relevant materials actually retrieved

$$ \frac{TP}{TP + FN} $$

### Precision

Proportion of retrieved material actually relevant

$$ \frac{TP}{TP + FP} $$

### P@K

Precision after retrieving K documents

- R-Precision = Precision after retrieving R dcouments, where R is the total
number of relevant documents for a query
    - At this point, precision = recall, since (number of retrieved docs  = number
of relevant docs)

Area fo Precsision vs Recall curve = Average Precision

### Reciprocal Rank

Reciprocal Rank = $\frac{1}{\text{rank of first relevant doc}}$

MRR = Mean Reciprocal Rank

## Identifying relevant documents

### Pooling

Exhaustively judging each and every doc for a query is impossible for a large collection.
The doc-collection and the query set are shared among diff diverse systems and they are asked to retrieve at least 1000 docs for each query in descending order of the similarity scores to each query

- Use multiple systems (say $n \approx 10$)
- ask each system to perform ranked retrieval and select top $k$ ~100 documents for each
- This pool is exhaustively (e.g. manually) judged for each query
    - there needs to be mulitple independent judges, otherwise bias will creep in

*Assumptions*

- All the rel docs are retrieved and belong to the pool
- there are no reldocs outside the pool created for each query

If the K is sufficiently deep and n is adequately large, the assumptions give reliable estimates of reldocs

## Agreement between judges

$$ \text{Agreement }= \kappa = \frac{P(A) - P(E)}{1-P(E)} \in [-1, 1] $$

where 

$$ \begin{aligned}
    P(A) &= \text{observed agreement}\\
    P(E) &= \text{agreement by chance} \\
&= P(\text{Agreement on Rel by chance}) + P(\text{Agreement on NR by chance}) \\
&= P(Rel_A \cap Rel_B  ) + P(NR_A \cap NR_B) \text{(assuming A and B are independent)} \\
\end{aligned} $$


TODO: use `cases` latex construct

$$ \begin{aligned}
\kappa > 0.8  &\text{Good agreement} \\
0.67 < \kappa < 0.8  &\text{Fair agreement} \\
\kappa < 0.67 &\text{not good} \\
\end{aligned} $$

Usually two judges are good enough

For exapmle

 |                 | *Rel_B*         | *NR_B*          |                 |
 | --------------- | --------------- | --------------- | --------------- |
 | *Rel_A*         | 75              | 25              | 100             |
 | *NR_A*          | 75              | 225             | 300             |
 |                 | 150             | 250             | 400             |


$$ \begin{aligned}
P( \text{ agreement } ) &= \frac{75 + 225}{400} \approx& 0.75 \\
P(\text{ Random }) &= \frac{100}{400} \cdot \frac{150}{400} + \frac{ 300 }{ 400 } \cdot \frac{ 250 }{ 400 } =& 0.5625 \\
\kappa &= \frac{0.75-0.5625}{1-0.5625} \approx& 0.4286
\end{aligned} $$



