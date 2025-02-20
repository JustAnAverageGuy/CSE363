


Aim: to calculate $P(R=1|\text{document}_i,\text{query})$ for each document and to produce a ranking based on this

R is indicator variable representing that the document is relevant for the query

## Probability Ranking Principle

Let x represent a document in the collection

Let R represent the relevance of a document wrt given (fixed) query
R = 1 represent relevant
R = 0 represent irrelevant

Need to find $p(R=1|x)$

$$ \begin{aligned}
    p(R=1|x) &= \frac{p(x|R=1)p(R=1)}{p(x)} \\
    p(R=0|x) &= \frac{p(x|R=0)p(R=0)}{p(x)} \\
    p(R=1|x) + p(R=0|x) &= 1 \\
\end{aligned} $$

NOTE: Instead of working with probabilities directly, we work with odds, because they are easier to compute under bayesian model.

$$O(A) = \text{odds}(A) = \frac{P(A)}{P(\bar{A})} =\frac{P(A)}{1-P(A)} $$

### Binary Independence Model
We also model documents as binary term vectors $\vec{x} = (0,1,0,0,\dots,1)$

$$
    O(R=1|q,x) = \frac{P(R=1|q,x)}{P(R=0|q,x)} 
= \frac{\frac{P(R=1|q)P(x|R=1,q)}{P(x|q)}}{\frac{P(R=0|q)P(x|R=0,q)}{P(x|q)}}
= \underbrace{\frac{P(R=1|q)}{P(R=0|q)}}_{\text{constant for a given query}} \cdot \overbrace{\frac{P(x|R=1,q)}{P(x|R=0,q)}}^{\text{needs to be estimated for each document}}
$$

To compute $\frac{P(x|R=1,q)}{P(x|R=0,q)}$, using independence assumptions, we can write

$$\frac{P(x|R=1,q)}{P(x|R=0,q)} = \prod_{t=1}^M \frac{P(x_t|R=1,q)}{P(x_t|R=0,q)}$$

Now, in [BIM](#binary-independence-model), $x_t \in \{0,1\}$

hence we can write

$$\frac{P(x|R=1,q)}{P(x|R=0,q)} = \prod_{t:x_t=1} \frac{P(x_t=1|R=1,q)}{P(x_t=1|R=0,q)} \prod_{t:x_t=0} \frac{P(x_t=0|R=1,q)}{P(x_t=0|R=0,q)}$$















