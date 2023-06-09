# https://github.com/asajadi/fast-pagerank/blob/master/fast_pagerank/fast_pagerank.py

import scipy as sp
import scipy.sparse as sprs


def pagerank(
    A,
    p=0.85,
    personalize=None,
    reverse=False,
    solver=sprs.linalg.gmres,
    **kwargs,
):
    """
    Calculates PageRank given a csr graph

    Inputs:
    -------
    G: a csr graph.
    p: damping factor
    personlize: if not None, should be an array with the size of the nodes
                containing probability distributions.
                It will be normalized automatically
    reverse: If true, returns the reversed-PageRank

    outputs
    -------
    PageRank Scores for the nodes
    """
    # In Moler's algorithm, $A_{ij}$ represents the existences of an edge
    # from node $j$ to $i$, while we have assumed the opposite!
    if reverse:
        A = A.T

    n, _ = A.shape
    r = sp.asarray(A.sum(axis=1)).reshape(-1)

    k = r.nonzero()[0]

    D_1 = sprs.csr_matrix((1 / r[k], (k, k)), shape=(n, n))

    if personalize is None:
        personalize = sp.ones(n)
    personalize = personalize.reshape(n, 1)
    s = (personalize / personalize.sum()) * n

    I = sprs.eye(n)
    x = solver((I - p * A.T @ D_1), s)
    if isinstance(x, tuple):
        if x[1] != 0:
            raise ValueError(
                'pagerank not able to converge, might want to change `solver` function.')
        x = x[0]

    x = x / x.sum()
    return x
