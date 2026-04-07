# Chapter 25: All-Pairs Shortest Paths

## Overview
The all-pairs shortest-paths problem asks us to find the shortest-path weights δ(i, j) for every pair of vertices (i, j) in a weighted, directed graph G = (V, E). Where single-source algorithms compute distances from one vertex, this chapter attacks the full n × n distance matrix simultaneously. Three progressively more practical algorithms are developed: a matrix-multiplication–based dynamic programming approach (Θ(n³ lg n)), the Floyd-Warshall algorithm (Θ(n³), elegant and in-place), and Johnson's algorithm (O(V² lg V + VE), optimal for sparse graphs with negative edges). Each exploits a different structural decomposition of shortest paths—by edge count, by intermediate vertex set, or by vertex reweighting—and together they illustrate how problem structure dictates algorithm design.

## Key Concepts

- **Problem representation**: The graph is given as an n × n weight matrix W where w_ij = 0 if i = j, the edge weight if (i, j) ∈ E, and ∞ otherwise. The output is a distance matrix D (with d_ij = δ(i, j)) and a predecessor matrix Π for path reconstruction.
- **Predecessor matrix Π**: π_ij is the predecessor of j on a shortest path from i to j (or NIL if no path exists or i = j). PRINT-ALL-PAIRS-SHORTEST-PATH(Π, i, j) recursively follows predecessors to print the actual path, analogous to single-source path printing.
- **Naive baselines**: Running a single-source algorithm |V| times gives a valid all-pairs solution. With Dijkstra (nonneg weights) this costs O(V³) with an adjacency matrix, O(VE lg V) with a binary heap, or O(V² lg V + VE) with Fibonacci heaps. With Bellman-Ford (allowing negative weights) the cost is O(V²E), which is O(V⁴) on dense graphs. The chapter's algorithms aim to improve on or match these bounds more elegantly.
- **Three decomposition strategies**: (1) Decompose by number of edges on the path (§25.1), (2) decompose by the set of intermediate vertices allowed (§25.2), (3) decompose by reweighting edges so that a fast nonneg-weight algorithm can be reused (§25.3).
- **Negative-weight edges vs. cycles**: Floyd-Warshall and Johnson both handle negative-weight edges. Negative-weight *cycles* are detected (Floyd-Warshall checks the diagonal of D; Johnson's Bellman-Ford step catches them) but make shortest paths undefined.

## Algorithms and Techniques

### 25.1 Shortest Paths and Matrix Multiplication

- **Subproblem definition**: Let l^(m)\_ij be the minimum weight of any path from i to j using at most m edges.
- **Base case**: L^(0) is the "identity" matrix for the (min, +) semiring: l^(0)\_ij = 0 if i = j, ∞ otherwise.
- **Recurrence**: l^(m)\_ij = min₁≤k≤n { l^(m−1)\_ik + w_kj }. This mirrors standard matrix multiplication with min replacing + and + replacing ×.
- **EXTEND-SHORTEST-PATHS(L, W)**: Computes L' = L ⊙ W (the "min-plus product") in Θ(n³) via three nested loops, directly analogous to the inner kernel of matrix multiplication.
- **Slow approach**: Compute L^(1) = L^(0) ⊙ W, then L^(2) = L^(1) ⊙ W, ..., up to L^(n−1). Since any shortest path (without negative cycles) uses at most n − 1 edges, D = L^(n−1). This requires n − 2 matrix products → **Θ(n⁴)** total.
- **Repeated squaring**: Because L^(n−1) = L^(2(n−1)) = ⋯ (the sequence stabilises once the exponent reaches n − 1), we can square: L^(1), L^(2), L^(4), ..., L^(2^⌈lg(n−1)⌉). Only ⌈lg(n − 1)⌉ products are needed → **Θ(n³ lg n)** total.
- **Significance**: While not the fastest all-pairs method in practice, this connection to matrix multiplication is theoretically important. Any faster algorithm for min-plus matrix multiplication (e.g., Fredman's O(n³ / lg n) or truly subcubic results) would immediately improve all-pairs shortest paths.

### 25.2 The Floyd-Warshall Algorithm

- **Subproblem definition**: Let d^(k)\_ij be the shortest-path weight from i to j using only vertices {1, 2, ..., k} as intermediates.
- **Base case**: d^(0)\_ij = w_ij (no intermediate vertices allowed, so only direct edges contribute).
- **Recurrence**: d^(k)\_ij = min( d^(k−1)\_ij,  d^(k−1)\_ik + d^(k−1)\_kj ). The first term represents the shortest path *not* passing through k; the second represents a path that decomposes into i ⇝ k ⇝ j, each subpath using intermediates from {1, ..., k − 1}.
- **FLOYD-WARSHALL(W)**:
  1. Set D^(0) ← W.
  2. For k = 1 to n: for each (i, j), update d^(k)\_ij using the recurrence.
  3. Return D^(n).
- **In-place update**: Because d^(k)\_ik and d^(k)\_kj equal their (k−1) versions (the k-th row and k-th column are unchanged when processing vertex k), the algorithm can safely update D in place, using only **Θ(n²)** space.
- **Predecessor matrix**: Updated alongside D. Set π^(0)\_ij = i if w_ij < ∞ and i ≠ j, NIL otherwise. At step k: π^(k)\_ij = π^(k−1)\_ij if the path through k is not shorter; otherwise π^(k)\_ij = π^(k−1)\_kj (the predecessor of j on the i ⇝ k ⇝ j path).
- **Negative-cycle detection**: After computing D^(n), inspect the main diagonal. If any d_ii < 0, vertex i lies on a negative-weight cycle.

#### Transitive Closure

- **Problem**: Given a directed (unweighted) graph G, compute the transitive closure G\* where (i, j) ∈ E\* iff some path from i to j exists in G.
- **Approach**: Adapt Floyd-Warshall by replacing (min, +) with (∨, ∧). Define t^(k)\_ij = t^(k−1)\_ij ∨ (t^(k−1)\_ik ∧ t^(k−1)\_kj).
- **TRANSITIVE-CLOSURE(G)**: Initialise T^(0) with t_ij = 1 if i = j or (i, j) ∈ E, 0 otherwise. Iterate k = 1 to n with the Boolean recurrence above.
- **Complexity**: Θ(n³) time, but substantially faster in practice because Boolean operations can be packed into machine words (bitwise OR/AND), processing up to 64 vertices per operation.

### 25.3 Johnson's Algorithm for Sparse Graphs

- **Motivation**: Floyd-Warshall's Θ(n³) is optimal for dense graphs, but on sparse graphs (|E| ≪ |V|²) it is wasteful. If all edge weights were nonneg, we could run Dijkstra from each vertex in O(V² lg V + VE) with Fibonacci heaps—much faster when E = o(V²). Johnson's algorithm makes this possible even when negative edges exist.
- **Reweighting idea**: Assign a height function h : V → ℝ. Define new weights ŵ(u, v) = w(u, v) + h(u) − h(v). For any path p from u to v, the reweighted path weight satisfies ŵ(p) = w(p) + h(u) − h(v)—the h-terms telescope. Hence shortest paths under ŵ are exactly the shortest paths under w (only the path weights shift by a constant depending on the endpoints), and relative path ordering is preserved.
- **Computing h**: Add a new source vertex s with zero-weight edges to every vertex. Run Bellman-Ford from s. Set h(v) = δ(s, v). By the triangle inequality for shortest paths, δ(s, v) ≤ δ(s, u) + w(u, v), which rearranges to w(u, v) + h(u) − h(v) ≥ 0 (Lemma 25.1). So all reweighted edges are nonneg.
- **JOHNSON(G, w)**:
  1. Construct G' by adding vertex s and edges (s, v) with weight 0 for all v ∈ V.
  2. Run BELLMAN-FORD(G', w, s). If it reports a negative-weight cycle, halt.
  3. For each v ∈ V: set h(v) = δ(s, v).
  4. For each (u, v) ∈ E: set ŵ(u, v) = w(u, v) + h(u) − h(v).
  5. For each source u ∈ V: run DIJKSTRA(G, ŵ, u) to obtain δ̂(u, v) for all v.
  6. Recover original distances: d_uv = δ̂(u, v) − h(u) + h(v).
- **Correctness**: Follows from the telescoping property of reweighted paths and the nonnegativity guarantee from Lemma 25.1.

## Complexity Analysis

| Algorithm | Time | Space | Negative Weights? | Best For |
|---|---|---|---|---|
| Matrix mult. (slow) | Θ(n⁴) | Θ(n²) | Yes (no neg cycles) | Theoretical baseline |
| Matrix mult. (repeated squaring) | Θ(n³ lg n) | Θ(n²) | Yes (no neg cycles) | Theory / reductions |
| Floyd-Warshall | **Θ(n³)** | Θ(n²) | Yes (detects neg cycles) | Dense graphs |
| Transitive closure | Θ(n³) | Θ(n²) | N/A (unweighted) | Reachability queries |
| Johnson's | **O(V² lg V + VE)** | O(V² + E) | Yes (detects neg cycles) | Sparse graphs |

**Key analytical points:**

- Floyd-Warshall's Θ(n³) beats the repeated-squaring method's Θ(n³ lg n) and matches the best dense-graph Dijkstra variant.
- Johnson's algorithm breaks down as: O(VE) for Bellman-Ford + O(V · (V lg V + E)) for |V| Dijkstra runs with Fibonacci heaps = O(V² lg V + VE). On sparse graphs where E = O(V), this is O(V² lg V), vastly better than Θ(V³).
- On dense graphs where E = Θ(V²), Johnson's O(V² lg V + V³) = O(V³), matching Floyd-Warshall asymptotically but with higher constant factors and more complex implementation.
- The matrix-multiplication approach, while not the fastest, opens the door to leveraging any advancement in (min, +)-matrix multiplication for shortest-path improvements.

## Key Takeaways

- **Problem decomposition drives design**: The same all-pairs problem yields fundamentally different algorithms depending on how subproblems are defined—by edge count (matrix multiplication), by intermediate vertex set (Floyd-Warshall), or by edge reweighting (Johnson). Recognising the right decomposition is the central algorithmic skill.
- **Floyd-Warshall is the workhorse for dense graphs**: With a clean three-loop structure, in-place Θ(n²) space, built-in predecessor tracking, and negative-cycle detection via the diagonal, it is the default choice when |E| = Θ(|V|²).
- **Johnson's algorithm is the sparse-graph champion**: By cleverly reducing the negative-weight problem to |V| nonneg single-source problems, it achieves O(V² lg V + VE)—a decisive win when the graph is sparse.
- **Reweighting is a powerful general technique**: The idea of shifting edge weights by a potential function h while preserving shortest-path structure has applications beyond this chapter, including minimum-cost flow and A\* search.
- **Algebraic structure matters**: The (min, +) semiring connection between shortest paths and matrix multiplication is not just a curiosity—it links shortest-path complexity to fundamental open questions in combinatorial optimisation and has inspired subcubic algorithms.
