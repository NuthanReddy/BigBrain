# Chapter 24: Single-Source Shortest Paths

## Overview

This chapter addresses the fundamental problem of finding shortest paths from a single
source vertex to every other vertex in a weighted directed graph. It develops three
major algorithms—Bellman-Ford, DAG shortest paths, and Dijkstra's—each suited to
different graph structures, and establishes the theoretical properties (relaxation,
optimal substructure, triangle inequality) that underpin their correctness. An elegant
application to systems of difference constraints demonstrates the reach of shortest-path
machinery beyond traditional graph problems.

## Key Concepts

### Problem Definition

- **Input:** A weighted directed graph G = (V, E) with weight function w : E → ℝ and
  a distinguished source vertex s.
- **Goal:** Compute the shortest-path weight δ(s, v) for every vertex v, where
  δ(s, v) = min{ w(p) : p is a path from s to v }, or ∞ if v is unreachable.
- **Optimal substructure (Lemma 24.1):** Every subpath of a shortest path is itself a
  shortest path. This property is the foundation for all dynamic-programming and greedy
  approaches in the chapter.

### Negative Weights and Negative-Weight Cycles

- Negative-weight edges are permitted in principle, but if a negative-weight cycle is
  reachable from s, the shortest-path weight for any vertex reachable from that cycle
  is −∞ (one can loop indefinitely to reduce cost).
- Bellman-Ford explicitly detects such cycles; Dijkstra avoids the issue by requiring
  nonnegative weights; DAG shortest paths sidestep it because DAGs are acyclic.

### Problem Variants

| Variant | Description |
|---|---|
| Single-source | Shortest paths from one source to all vertices (this chapter) |
| Single-destination | Shortest paths from all vertices to one target (reverse edges, solve single-source) |
| Single-pair | Shortest path between a specific (u, v) pair (no known algorithm faster than single-source in worst case) |
| All-pairs | Shortest paths between every pair of vertices (Chapter 25) |

### Data Structures and Representations

- **Shortest-path estimate v.d:** An upper bound on δ(s, v) that is progressively
  tightened. Initialized to ∞ for all vertices except the source (s.d = 0).
- **Predecessor pointer v.π:** Records the vertex that last improved v.d, enabling
  reconstruction of actual shortest paths.
- **Shortest-paths tree:** The subgraph induced by predecessor pointers forms a rooted
  tree (rooted at s) encoding shortest paths to all reachable vertices.

### Initialization and Relaxation

These two subroutines are shared by every algorithm in the chapter.

**INITIALIZE-SINGLE-SOURCE(G, s):**
Set v.d = ∞ and v.π = NIL for every vertex v, then set s.d = 0.

**RELAX(u, v, w):**
If v.d > u.d + w(u, v), update v.d = u.d + w(u, v) and set v.π = u. Relaxation is
the only operation that modifies distance estimates; the algorithms differ solely in
the *order* and *frequency* with which they relax edges.

### Fundamental Properties of Relaxation

These lemmas hold for every algorithm that uses INITIALIZE-SINGLE-SOURCE followed by
any sequence of RELAX operations:

| Property | Statement |
|---|---|
| **Triangle inequality** (Lemma 24.10) | δ(s, v) ≤ δ(s, u) + w(u, v) for every edge (u, v) |
| **Upper-bound property** (Lemma 24.11) | v.d ≥ δ(s, v) always; once v.d equals δ(s, v) it never changes |
| **No-path property** (Corollary 24.12) | If no path from s to v exists, v.d = ∞ permanently |
| **Convergence property** (Lemma 24.14) | If u.d = δ(s, u) before relaxing edge (u, v) on a shortest path s ⤳ u → v, then v.d = δ(s, v) afterward |
| **Path-relaxation property** (Lemma 24.15) | If the edges of a shortest path ⟨v₀, v₁, …, vₖ⟩ are relaxed in order (possibly with other relaxations interleaved), then vₖ.d = δ(s, vₖ) |
| **Predecessor-subgraph property** (Lemma 24.17) | Once v.d = δ(s, v) for all v, the predecessor subgraph is a shortest-paths tree |

The path-relaxation property is especially powerful: it does not require that the
relaxations happen consecutively—only that they occur *in order* among whatever other
relaxations take place.

## Algorithms and Techniques

### 24.1 The Bellman-Ford Algorithm

**Applicability:** General weighted graphs, including those with negative-weight edges.

**Strategy:** Perform |V| − 1 passes over the entire edge set, relaxing every edge on
each pass. After pass *i*, the algorithm has correctly computed shortest paths that use
at most *i* edges. Since any shortest path (in a graph without negative-weight cycles)
uses at most |V| − 1 edges, all shortest-path weights are correct after the final pass.

**Pseudocode sketch:**

```
BELLMAN-FORD(G, w, s):
    INITIALIZE-SINGLE-SOURCE(G, s)
    for i = 1 to |V| − 1:
        for each edge (u, v) ∈ E:
            RELAX(u, v, w)
    // Negative-cycle detection
    for each edge (u, v) ∈ E:
        if v.d > u.d + w(u, v):
            return FALSE
    return TRUE
```

**Correctness (Theorem 24.4):**
- If no negative-weight cycle is reachable from s, the algorithm sets v.d = δ(s, v) for
  all v and returns TRUE. This follows from the path-relaxation property: any shortest
  path has at most |V| − 1 edges, and pass *i* relaxes the *i*-th edge of every such
  path.
- If a negative-weight cycle *is* reachable from s, the final check finds at least one
  edge that can still be relaxed, and the algorithm returns FALSE.

**Why |V| − 1 passes suffice:** A simple shortest path visits at most |V| vertices and
therefore contains at most |V| − 1 edges. Each pass correctly extends all known shortest
paths by one edge, so |V| − 1 passes cover every possible shortest path length.

---

### 24.2 Shortest Paths in Directed Acyclic Graphs

**Applicability:** DAGs with arbitrary (including negative) edge weights.

**Strategy:** Topologically sort the vertices, then relax edges in topological order.
Because a DAG has no cycles, a topological ordering processes every vertex before any of
its successors, guaranteeing that edges along every shortest path are relaxed in sequence.

**Pseudocode sketch:**

```
DAG-SHORTEST-PATHS(G, w, s):
    topologically sort G
    INITIALIZE-SINGLE-SOURCE(G, s)
    for each vertex u in topological order:
        for each v ∈ Adj[u]:
            RELAX(u, v, w)
```

**Correctness:** Follows directly from the path-relaxation property. Topological order
ensures that for any shortest path ⟨v₀, v₁, …, vₖ⟩, edge (vᵢ₋₁, vᵢ) is relaxed
before edge (vᵢ, vᵢ₊₁).

**Key advantages over Bellman-Ford:**
- Runs in Θ(V + E), a single pass through edges rather than |V| − 1 passes.
- Handles negative-weight edges naturally (no cycles exist to cause problems).

**Application — PERT charts and critical paths:**
In project scheduling (Program Evaluation and Review Technique), tasks are DAG edges
weighted by duration. The *critical path*—the longest path from start to finish—determines
the minimum project completion time. By negating all edge weights and running
DAG-SHORTEST-PATHS, one obtains the longest path efficiently.

---

### 24.3 Dijkstra's Algorithm

**Applicability:** Graphs with nonnegative edge weights (w(u, v) ≥ 0 for all edges).

**Strategy:** A greedy algorithm that maintains a set S of vertices whose shortest-path
weights are finalized, and a min-priority queue Q of remaining vertices keyed by their
current d values. At each step, extract the vertex u with minimum d value, add it to S,
and relax all edges leaving u.

**Pseudocode sketch:**

```
DIJKSTRA(G, w, s):
    INITIALIZE-SINGLE-SOURCE(G, s)
    S = ∅
    Q = V    // min-priority queue keyed by v.d
    while Q ≠ ∅:
        u = EXTRACT-MIN(Q)
        S = S ∪ {u}
        for each v ∈ Adj[u]:
            RELAX(u, v, w)   // includes DECREASE-KEY on Q
```

**Correctness (Theorem 24.6):** When vertex u is extracted from Q, u.d = δ(s, u).

*Proof intuition:* Suppose for contradiction that u.d > δ(s, u) when u is extracted.
Consider the true shortest path from s to u; it must cross from S to V \ S at some edge
(x, y). Because x ∈ S, x.d = δ(s, x) (by induction). Relaxing (x, y) set
y.d = δ(s, y). Since all edge weights are nonnegative, δ(s, y) ≤ δ(s, u) ≤ u.d. But u
was extracted before y, meaning u.d ≤ y.d—a contradiction unless u.d = δ(s, u).

**Why nonnegative weights are essential:** The greedy choice—committing to the smallest
d value—relies on the guarantee that no future path through unprocessed vertices could
offer a cheaper route. A single negative-weight edge can violate this, making it possible
to discover a shorter path after a vertex has already been finalized.

**Priority queue implementation trade-offs:**

| Implementation | EXTRACT-MIN | DECREASE-KEY | Total time |
|---|---|---|---|
| Unsorted array | O(V) | O(1) | O(V²) |
| Binary min-heap | O(lg V) | O(lg V) | O((V + E) lg V) |
| Fibonacci heap | O(lg V) amortized | O(1) amortized | O(V lg V + E) |

- **Dense graphs** (E ≈ V²): The array implementation's O(V²) matches or beats the
  heap-based approaches.
- **Sparse graphs** (E ≈ V): The Fibonacci heap's O(V lg V + E) is asymptotically
  optimal.
- **In practice:** Binary heaps are the most common choice, offering a good balance of
  simplicity and performance.

---

### 24.4 Difference Constraints and Shortest Paths

**Problem:** Solve a system of *m* difference constraints on *n* unknowns:

> x_j − x_i ≤ b_k  for k = 1, …, m

**Constraint graph construction:**
1. Create a vertex v_i for each variable x_i (i = 1, …, n).
2. Add a source vertex v₀ with edges (v₀, v_i) of weight 0 for every i.
3. For each constraint x_j − x_i ≤ b_k, add edge (v_i, v_j) with weight b_k.

**Connection to shortest paths (Theorem 24.9):**
- If the constraint graph contains no negative-weight cycle, then setting
  x_i = δ(v₀, v_i) yields a feasible solution. The triangle inequality on shortest
  paths directly mirrors the difference constraints.
- If a negative-weight cycle exists, the system has no feasible solution (the
  constraints are contradictory).

**Solution method:** Run Bellman-Ford on the constraint graph. If it returns TRUE, the
shortest-path weights give a valid assignment; if FALSE, no solution exists.

**Practical relevance:** Difference constraints arise in scheduling, verification of
timing constraints in circuits, and compiler optimization (e.g., instruction scheduling).

---

### 24.5 Proofs of Shortest-Paths Properties

Section 24.5 provides rigorous proofs for all the relaxation properties listed earlier.
The key insights are:

- **Triangle inequality:** Follows from the definition of shortest-path weight—any
  shortest path to v is at most as long as a shortest path to u plus the direct edge
  (u, v).
- **Upper-bound property:** Proved by induction on the number of relaxation steps.
  Relaxation can only decrease v.d, and it can never push v.d below δ(s, v).
- **Convergence and path-relaxation properties:** Build on the upper-bound property to
  show that relaxing edges in the right order (not necessarily exclusively) drives
  estimates to their true values.
- **Predecessor-subgraph property:** Once all estimates are correct, the predecessor
  pointers form a tree because each vertex has exactly one predecessor on its shortest
  path from s.

These properties are algorithm-independent—they hold for *any* sequence of relaxations
following a proper initialization. This generality is what allows the same framework to
prove correctness of Bellman-Ford, DAG shortest paths, and Dijkstra's algorithm.

## Complexity Analysis

### Algorithm Comparison

| Algorithm | Graph type | Negative weights? | Negative-cycle detection? | Time | Space |
|---|---|---|---|---|---|
| Bellman-Ford | General | ✅ Yes | ✅ Yes | O(VE) | O(V) |
| DAG Shortest Paths | DAG only | ✅ Yes | N/A (no cycles) | Θ(V + E) | O(V) |
| Dijkstra (array) | General | ❌ No | ❌ No | O(V²) | O(V) |
| Dijkstra (binary heap) | General | ❌ No | ❌ No | O(E lg V) | O(V) |
| Dijkstra (Fibonacci heap) | General | ❌ No | ❌ No | O(V lg V + E) | O(V) |
| Difference constraints | Constraint graph | ✅ Yes | ✅ Yes | O(nm) | O(n) |

### Important Complexity Observations

- **Bellman-Ford vs. Dijkstra:** Bellman-Ford's O(VE) is significantly slower than
  Dijkstra's O(V lg V + E), but Bellman-Ford handles negative weights and detects
  negative cycles.
- **DAG shortest paths** is the fastest algorithm when applicable, achieving linear time
  in the size of the graph.
- **Dijkstra's queue choice matters:** For dense graphs where E = Θ(V²), the simple
  array implementation at O(V²) is preferable to a binary heap at O(V² lg V). For sparse
  graphs where E = O(V), the Fibonacci heap's O(V lg V) is superior.

### Key Theorems

- **Theorem 24.4 (Bellman-Ford correctness):** Guarantees correct shortest-path weights
  when no negative-weight cycle is reachable, and reliable detection when one exists.
- **Theorem 24.6 (Dijkstra correctness):** Each EXTRACT-MIN produces a vertex with its
  final shortest-path weight, assuming nonnegative edge weights.
- **Theorem 24.9 (Difference constraints):** Establishes the exact correspondence between
  feasibility of a constraint system and the absence of negative-weight cycles in its
  constraint graph.

## Key Takeaways

- **Relaxation is the universal primitive.** All three algorithms use the same RELAX
  operation; they differ only in the order and number of relaxation steps. Understanding
  relaxation properties is the key to understanding (and proving) every algorithm in the
  chapter.

- **Match the algorithm to the graph structure.** Use DAG shortest paths for acyclic
  graphs (Θ(V + E)), Dijkstra for nonnegative-weight graphs (as fast as O(V lg V + E)),
  and Bellman-Ford as the general-purpose fallback that handles negative weights and
  detects negative cycles (O(VE)).

- **Nonnegative weights enable greediness.** Dijkstra's algorithm is faster precisely
  because nonnegative weights let it commit to each vertex's shortest-path weight at
  extraction time. Negative edges break this invariant, which is why Dijkstra fails on
  such graphs.

- **Shortest-path theory has surprising applications.** The reduction from difference
  constraints to shortest paths illustrates how graph algorithms solve problems that
  don't initially look like graph problems—a recurring theme in algorithm design.

- **The predecessor subgraph encodes all shortest paths.** Maintaining v.π alongside v.d
  is not just bookkeeping—the resulting shortest-paths tree is the deliverable that lets
  us reconstruct actual paths, not just their weights.
