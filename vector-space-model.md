# Vector Space Model

## Term Frequency

term-frequency ($tf_{ij}$) = number of times term i is present in document j

## Document Frequency

$df_{i}$ = number of docs where aterm $t_i$ is present

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

One of the popular choices for this sort of variation is 
$$
w_{ij} \propto \underbrace{\log(1+tf)}_{\text{tf}}\overbrace{\log\left(\frac{N+1}{df+0.5}\right)}^{\text{idf}}
$$

