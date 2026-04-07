# Chapter 26: Maximum Flow

## Overview
Maximum flow addresses the problem of pushing as much "flow" as possible through a directed network from a source to a sink without exceeding edge capacities. The chapter develops two major algorithmic paradigms—augmenting-path methods (Ford-Fulkerson, Edmonds-Karp) and push-relabel methods—and connects them through the max-flow min-cut theorem, one of the most important duality results in combinatorial optimization. A direct application to maximum bipartite matching demonstrates how flow techniques solve seemingly unrelated graph problems.

## Key Concepts

- **Flow network**: A directed graph G = (V, E) where every edge (u, v) carries a non-negative capacity c(u, v). The graph has a designated source s and sink t, contains no self-loops, and forbids antiparallel edges (if (u, v) ∈ E then (v, u) ∉ E).
- **Flow**: A function f : V × V → ℝ obeying two constraints: (1) *capacity constraint*—0 ≤ f(u, v) ≤ c(u, v) for every edge, and (2) *flow conservation*—for every vertex except s and t the total flow entering equals the total flow leaving. The *value* |f| is the net flow leaving the source.
- **Residual graph G_f**: Encodes remaining capacity. For each edge (u, v) with unused capacity, a forward residual edge has capacity c_f(u, v) = c(u, v) − f(u, v). For each edge carrying positive flow, a backward residual edge has capacity c_f(v, u) = f(u, v), allowing flow to be "cancelled."
- **Augmenting path**: A simple s‑to‑t path in the residual graph. Its bottleneck (minimum residual capacity along the path) determines how much additional flow can be pushed.
- **Cut (S, T)**: A partition of V with s ∈ S and t ∈ T. The *capacity* c(S, T) is the sum of capacities on edges crossing from S to T. The *net flow* across any cut equals |f|.
- **Preflow**: A relaxation of flow used in push-relabel algorithms where flow conservation is replaced by the weaker condition that flow into a non-source vertex is at least as large as flow out, creating non-negative *excess* e(u) at interior vertices.
- **Height function**: An integer labelling h : V → ℕ with h(s) = |V|, h(t) = 0, and the constraint h(u) ≤ h(v) + 1 for every residual edge (u, v). Heights guide push operations downhill and determine when relabelling is needed.
- **Handling modelling issues**: Antiparallel edges are eliminated by splitting one edge with an intermediate vertex. Multiple sources or sinks are unified by adding a supersource or supersink connected via infinite-capacity edges.

## Algorithms and Techniques

### 1. Ford-Fulkerson Method (Section 26.2)
- **Approach**: Start with zero flow. Repeatedly find an augmenting path p from s to t in the residual graph, then push c_f(p) = min{c_f(u, v) : (u, v) on p} additional units of flow along every edge of p—increasing flow on forward edges and decreasing it on backward edges. Terminate when no augmenting path exists.
- **Correctness (Lemma 26.1)**: If f is a flow in G and f′ is a flow in G_f, then the augmented flow f ↑ f′ is a valid flow in G with value |f| + |f′|.
- **Basic implementation**: Using DFS to find augmenting paths yields O(E · |f*|) time where f* is the maximum flow value. This bound is *pseudo-polynomial*—it depends on the magnitude of the answer, not just the graph size—and can be pathological for large or irrational capacities.

### 2. Max-Flow Min-Cut Theorem (Theorem 26.6)
The following three statements are equivalent for any flow f in a flow network G:
1. f is a maximum flow in G.
2. The residual graph G_f contains no augmenting path from s to t.
3. |f| = c(S, T) for some cut (S, T) of G.

The theorem establishes a strong duality: the maximum amount of flow equals the minimum capacity over all cuts separating s from t. It also certifies optimality—when Ford-Fulkerson terminates, the set of vertices reachable from s in G_f defines a minimum cut.

### 3. Edmonds-Karp Algorithm (Section 26.2)
- **Refinement**: Choose the augmenting path with the fewest edges (BFS from s to t in G_f).
- **Key insight (Theorem 26.8)**: Shortest-path distances in the residual graph are monotonically non-decreasing across augmentations. This limits the total number of augmentations to O(VE).
- **Time**: O(VE²). Because each BFS takes O(E) time and there are at most O(VE) augmentations. This is a *strongly polynomial* bound, independent of capacity values.

### 4. Maximum Bipartite Matching (Section 26.3)
- **Problem**: Given a bipartite graph G = (L ∪ R, E), find a maximum-cardinality set of edges such that no vertex is matched more than once.
- **Reduction to max flow**: Construct a flow network G′ by adding source s connected to every vertex in L and sink t connected from every vertex in R, all with unit capacity. Direct original edges from L to R, also with unit capacity.
- **Integrality theorem (Theorem 26.10)**: When all capacities are integers, there exists a maximum flow that is integer-valued. In the bipartite setting, this means every edge carries 0 or 1 unit of flow, directly encoding a matching.
- **Correctness (Lemma 26.9)**: A matching of size k in G corresponds to an integer flow of value k in G′ and vice versa. The maximum matching cardinality equals the maximum flow value.
- **Time**: O(VE) by running Ford-Fulkerson on the unit-capacity network, since |f*| ≤ |V|/2 and each augmentation takes O(E).

### 5. Generic Push-Relabel (Section 26.4)
- **Paradigm shift**: Instead of finding global s‑to‑t paths, push-relabel works locally at individual vertices. It maintains a *preflow* (flow conservation is relaxed) and iteratively moves excess flow toward the sink or, when blocked, back toward the source.
- **Initialization**: Saturate every edge leaving s (push capacity units along each), set h(s) = |V|, h(v) = 0 for all v ≠ s.
- **PUSH(u, v)**: Applicable when vertex u has positive excess, residual edge (u, v) exists, and h(u) = h(v) + 1 (flow goes "downhill"). Pushes δ = min(e(u), c_f(u, v)) units from u to v. A *saturating push* uses all residual capacity; a *non-saturating push* drains all excess at u.
- **RELABEL(u)**: Applicable when u has positive excess but no admissible (downhill) residual neighbour. Raises h(u) to 1 + min{h(v) : (u, v) ∈ E_f}, creating at least one admissible edge.
- **Termination**: When no vertex (other than s, t) has excess, the preflow is a valid maximum flow.

### 6. Relabel-to-Front Algorithm (Section 26.5)
- **Strategy**: Maintains a linked list L of all vertices in V − {s, t}. Processes the front vertex u by *discharging* it (alternating pushes and relabels until e(u) = 0). If u was relabelled during discharge, it moves to the front of L, ensuring recently active vertices are revisited first.
- **DISCHARGE(u)**: Scans u's neighbour list with a *current-edge* pointer. If the current neighbour v admits a push (h(u) = h(v) + 1 and c_f(u, v) > 0), push flow. If the pointer falls off the end of the list, relabel u and reset the pointer.
- **Traversal**: After discharging the current vertex, advance to the next in L. A relabel-and-move-to-front event restarts the scan, guaranteeing progress.

## Complexity Analysis

| Algorithm | Time Complexity | Notes |
|---|---|---|
| Ford-Fulkerson (DFS) | O(E · \|f*\|) | Pseudo-polynomial; depends on max-flow value |
| Edmonds-Karp (BFS) | O(VE²) | Strongly polynomial; O(VE) augmentations × O(E) per BFS |
| Bipartite matching via flow | O(VE) | Unit capacities bound \|f*\| ≤ V/2 |
| Generic push-relabel | O(V²E) | ≤ O(V²) relabels, O(VE) saturating pushes, O(V²E) non-saturating pushes |
| Relabel-to-front | O(V³) | Better for dense graphs (E = Θ(V²)); O(V²) relabels × O(V) work per pass |

**Important bounds within push-relabel analysis:**
- Heights never decrease, and h(u) ≤ 2|V| − 1 for all u (Lemma 26.14).
- Total relabel operations across all vertices: O(V²) (Lemma 26.18), since each vertex is relabelled at most 2|V| − 1 times.
- Saturating pushes: O(VE) (Lemma 26.20). After a saturating push on edge (u, v), the edge must refill via a push in the reverse direction, which requires two relabel events, bounding the count.
- Non-saturating pushes: O(V²E) (Lemma 26.21). Proved via a potential function Φ = Σ h(u) over vertices with excess; each non-saturating push reduces Φ while relabels and saturating pushes only increase it by bounded amounts.
- Relabel-to-front achieves O(V³) because between consecutive relabels the algorithm processes at most O(V) vertices from the list, and there are O(V²) relabels total.

**Max-flow min-cut theorem** provides the optimality certificate: the value of any maximum flow equals the capacity of every minimum cut.

**Integrality theorem** guarantees that integer-capacity networks always admit an integer-valued maximum flow, which is critical for combinatorial applications like bipartite matching.

## Key Takeaways

- **Duality is powerful**: The max-flow min-cut theorem reveals that computing a maximum flow simultaneously solves the minimum-cut problem. The residual graph at termination directly encodes the minimum cut as the vertices reachable from s.
- **Algorithm choice depends on graph density**: Edmonds-Karp's O(VE²) suits sparse graphs, while relabel-to-front's O(V³) is preferable for dense graphs where E = Θ(V²). Generic push-relabel at O(V²E) lies between the two.
- **Residual graphs are the central abstraction**: Every Ford-Fulkerson-family algorithm works by transforming the residual graph until no s‑t path remains. Backward edges in the residual graph allow the algorithm to implicitly "undo" poor routing decisions.
- **Reduction to max flow solves matching**: The bipartite matching reduction, combined with the integrality theorem, shows that max-flow machinery extends far beyond its literal setting—any problem expressible as an integer flow on a unit-capacity network can leverage these algorithms.
- **Push-relabel is a fundamentally different paradigm**: By maintaining a preflow and working locally with height-guided pushes, push-relabel avoids the global path searches of augmenting-path methods, often yielding better practical and theoretical performance on dense instances.
