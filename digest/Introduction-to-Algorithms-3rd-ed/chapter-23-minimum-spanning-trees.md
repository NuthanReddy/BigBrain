# Chapter 23: Minimum Spanning Trees

## Overview
Given a connected, undirected graph G = (V, E) with a real-valued weight function w : E → ℝ, a minimum spanning tree (MST) is an acyclic edge subset T ⊆ E that connects every vertex and minimizes the total weight w(T) = Σ_{(u,v)∈T} w(u,v). The chapter develops a generic greedy framework based on the concept of safe edges and cuts, then instantiates it with two classical algorithms — Kruskal's and Prim's — each leveraging a different data-structure strategy to efficiently identify safe edges.

## Key Concepts

- **Spanning tree**: An acyclic, connected subgraph that includes all |V| vertices and exactly |V|−1 edges. Among all spanning trees, an MST has the smallest total edge weight.
- **Cut (S, V−S)**: A partition of the vertex set V into two non-empty subsets. An edge *crosses* the cut if its endpoints lie in different sides of the partition.
- **Respecting a set A**: A cut *respects* edge set A if no edge of A crosses it. This property is central to the safe-edge recognition theorem.
- **Light edge**: An edge of minimum weight among all edges crossing a given cut. Ties may be broken arbitrarily.
- **Safe edge**: An edge (u, v) is *safe* for a set A (where A ⊆ some MST) if A ∪ {(u, v)} is also a subset of some MST. The generic method grows A one safe edge at a time.
- **Forest G_A = (V, A)**: The subgraph induced by the edges accumulated so far. Each connected component of G_A is a tree fragment of the eventual MST; safe edges always connect distinct components.
- **Greedy choice property**: Both Kruskal's and Prim's algorithms make a locally optimal choice (lightest qualifying edge) at each step, and the cut-based theorem guarantees this choice is globally safe.

## Algorithms and Techniques

### Generic MST Method (Section 23.1)

The generic approach maintains an edge set A that is always a subset of some MST. At each iteration it identifies an edge that can be added to A without violating this invariant:

```
GENERIC-MST(G, w):
    A = ∅
    while A does not form a spanning tree:
        find an edge (u, v) that is safe for A
        A = A ∪ {(u, v)}
    return A
```

The entire correctness argument hinges on two results:

- **Theorem 23.1 (Safe-edge recognition)**: Let A be a subset of some MST, let (S, V−S) be any cut that respects A, and let (u, v) be a light edge crossing that cut. Then (u, v) is safe for A. The proof uses a cut-and-paste argument: if (u, v) is not already in MST T, adding it creates a unique cycle; removing a different crossing edge from that cycle produces a new spanning tree whose total weight is no greater than w(T).
- **Corollary 23.2**: If (u, v) is a light edge connecting any two connected components of the forest G_A = (V, A), then (u, v) is safe for A. This follows directly by choosing the cut that separates one component from the rest.

### Kruskal's Algorithm (Section 23.2)

Kruskal's algorithm processes edges globally in non-decreasing weight order and adds each edge that does not create a cycle. It uses a **disjoint-set (union-find)** data structure to track connected components efficiently:

```
MST-KRUSKAL(G, w):
    A = ∅
    for each vertex v ∈ V:
        MAKE-SET(v)
    sort edges of E by non-decreasing weight
    for each edge (u, v) in sorted order:
        if FIND-SET(u) ≠ FIND-SET(v):
            A = A ∪ {(u, v)}
            UNION(u, v)
    return A
```

**Correctness**: When edge (u, v) is added, u and v reside in different components. The cut that separates u's component from the rest respects A (no edge of A crosses it), and (u, v) is the lightest crossing edge — all lighter edges were already processed and either added to A or discarded because both endpoints were already connected. By Theorem 23.1, (u, v) is safe.

**Characteristics**: Kruskal's algorithm is edge-centric: it considers the entire edge set sorted by weight and builds the MST by merging components. It naturally suits sparse graphs and scenarios where edges are easily enumerable.

### Prim's Algorithm (Section 23.2)

Prim's algorithm is vertex-centric: it grows a single tree from an arbitrary root vertex r by always attaching the nearest non-tree vertex. A **min-priority queue** Q holds all vertices not yet in the tree, keyed by the lightest edge connecting each vertex to the current tree:

```
MST-PRIM(G, w, r):
    for each u ∈ V:
        u.key = ∞
        u.π = NIL
    r.key = 0
    Q = V                          // min-priority queue on key values
    while Q ≠ ∅:
        u = EXTRACT-MIN(Q)
        for each v ∈ Adj[u]:
            if v ∈ Q and w(u, v) < v.key:
                v.π = u
                v.key = w(u, v)    // implicit DECREASE-KEY
    // The MST edges are {(v, v.π) : v ∈ V − {r}}
```

**Correctness**: At each extraction, the edge (u.π, u) is a light edge crossing the cut between the vertices already extracted and those still in Q. By Corollary 23.2, every such edge is safe.

**Characteristics**: Prim's algorithm resembles Dijkstra's shortest-paths algorithm in structure — both use a priority queue and relax adjacent vertices — but the key semantics differ: Prim stores the minimum edge weight to the tree, not accumulated distance from a source. Prim's approach naturally suits dense graphs, especially with a Fibonacci-heap implementation.

## Complexity Analysis

### Kruskal's Algorithm

| Operation | Cost |
|---|---|
| Sort all edges | O(E lg E) |
| |V| MAKE-SET operations | O(V) |
| 2|E| FIND-SET + |V|−1 UNION (with union by rank and path compression) | O((V + E) α(V)) |
| **Total** | **O(E lg E) = O(E lg V)** |

The sorting step dominates. Because |E| < |V|², we have lg|E| = O(lg V), so O(E lg E) = O(E lg V). The union-find operations contribute a nearly-linear term involving the inverse Ackermann function α, which is at most 4 for all practical input sizes.

### Prim's Algorithm

| Priority Queue | BUILD | EXTRACT-MIN (×V) | DECREASE-KEY (×E) | **Total** |
|---|---|---|---|---|
| Binary min-heap | O(V) | O(V lg V) | O(E lg V) | **O(E lg V)** |
| Fibonacci heap | O(V) | O(V lg V) amortized | O(E) amortized | **O(E + V lg V)** |

With a binary min-heap, Prim matches Kruskal's O(E lg V) bound. With a Fibonacci heap, the amortized O(1) DECREASE-KEY reduces the total to O(E + V lg V), which is asymptotically faster for dense graphs where |E| ≫ |V|. For sparse graphs (|E| = O(V)), both implementations yield O(V lg V).

### Theorem Summary

| Result | Statement |
|---|---|
| Theorem 23.1 | A light edge crossing any cut that respects A is safe for A. |
| Corollary 23.2 | A light edge connecting two components of G_A is safe for A. |

These two results form the theoretical backbone: every greedy MST algorithm is an instantiation of the generic method, differentiated only by *how* it identifies the cut and the light edge.

## Key Takeaways

- **One theorem, two algorithms**: Theorem 23.1 provides a unified correctness proof. Kruskal's and Prim's algorithms are two different strategies for finding a safe edge — Kruskal via global edge sorting and union-find, Prim via local priority-queue relaxation.
- **Greedy works because of cuts**: The cut property guarantees that picking the lightest qualifying edge is always globally optimal, not just locally optimal. This is more powerful than a generic greedy argument — it is a structural property of spanning trees.
- **Data-structure choice drives performance**: Both algorithms have the same asymptotic cost with simple data structures, O(E lg V). Prim with a Fibonacci heap achieves O(E + V lg V), making it preferable for dense graphs; Kruskal's simpler union-find approach is often preferred in practice for sparse graphs.
- **Kruskal is edge-centric; Prim is vertex-centric**: Kruskal considers all edges globally and merges components; Prim grows one tree outward from a root. This distinction influences which algorithm is more natural for a given problem variant or graph representation.
- **Connections to other algorithms**: Prim's algorithm mirrors the structure of Dijkstra's algorithm (both use EXTRACT-MIN and key relaxation), while Kruskal's reliance on union-find connects it to problems in dynamic connectivity and offline minimum queries.
