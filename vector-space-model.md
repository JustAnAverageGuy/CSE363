# Vector Space Model

## Term Frequency

term-frequency ($tf_{ij}$) = number of times term i is present in document j

## Document Frequency

$df_{i}$ = number of docs where aterm $t_i$ is present

## Collection Frequency

$cf_t$ = total number of occurrences of t in the collection

--- 

$l_j$ represents the length of document j

term-weight ($w_{ij}$) in a doc $d_j$ 

$$
\begin{aligned}
    w_{ij} &\propto tf_{ij}\\
     &\propto \frac{1}{df_{i}}\\
     &\propto \frac{1}{l_j}\\
\end{aligned}
$$

The proportionality should be sub linear to better capture the nature of information distribution.

One of the popular choices for this sort of variation is 

$$
w_{ij} = \underbrace{\left[1+\log(1+tf)\right]}_{\text{tf}}\overbrace{\log\left(\frac{N+1}{df+0.5}\right)}^{\text{idf}}
$$

Currently a "*bag of words*" model, don't consider ordering of words, only the occurrences and count of occurrences.

Example:

query: 
q = "gold silver truck"

d1 = "Shipment of gold damaged in a fire"
d2 = "Delivery of silver arrived in a silver truck"
d3 = "Shipment of gold arrived in a truck"

ignoring stop words "in", "a", "of",
we have term document matrix


Filtering: 
- query is static
- the document collection is dynamic
- e.g. tracking user preferences etc. and then filtering and tailoring contents. etc based on that

