# Chapter 21: Data Structures for Disjoint Sets

## Overview
This chapter presents data structures for maintaining a collection of disjoint dynamic sets under MAKE-SET, UNION, and FIND-SET operations. The disjoint-set forest with union by rank and path compression achieves a nearly linear running time of O(m · α(n)) for m operations on n elements, where α is the inverse Ackermann function—a function so slowly growing that α(n) ≤ 4 for all practical input sizes. A key application is efficiently computing connected components of a graph.

## Key Concepts
- **Disjoint-set operations**:
  - MAKE-SET(x): Create a singleton set {x} with x as its representative.
  - UNION(x, y): Merge the sets containing x and y; the two sets must be disjoint.
  - FIND-SET(x): Return the representative of x's set.
- **Parameters**: n = number of MAKE-SET operations (thus n elements); m = total number of MAKE-SET, UNION, and FIND-SET operations. At most n − 1 UNION operations can occur (each reduces the set count by one), and m ≥ n.
- **Connected components application**: Process edges of an undirected graph: for each edge (u, v), if FIND-SET(u) ≠ FIND-SET(v), call UNION(u, v). Afterward, SAME-COMPONENT(u, v) checks if FIND-SET(u) = FIND-SET(v).

## Algorithms and Techniques

### Linked-List Representation (Section 21.2)
Each set is a linked list; the representative is the first element. Each node has a pointer back to the set object (with head and tail pointers).
- MAKE-SET and FIND-SET: O(1).
- UNION: Append one list to another; must update back-pointers for all elements in the appended list. A naive sequence of n − 1 UNIONs can cost Θ(n²) total.
- **Weighted-union heuristic**: Always append the shorter list to the longer one.
  - **Theorem 21.1**: With weighted union, m MAKE-SET, UNION, and FIND-SET operations (n of which are MAKE-SET) take O(m + n lg n) time. Each element's back-pointer is updated at most ⌈lg n⌉ times because each update at least doubles the element's set size.

### Disjoint-Set Forest (Section 21.3)
Each set is represented as a rooted tree; each node points to its parent (roots point to themselves). The representative is the root.

**Two heuristics** transform this from a potentially linear-time-per-operation structure to a nearly constant-time one:

1. **Union by rank**: Each node maintains a rank (upper bound on its height). During LINK(x, y), make the root with smaller rank point to the root with larger rank. If ranks are equal, choose one arbitrarily and increment its rank.

2. **Path compression**: During FIND-SET(x), make every node on the find path point directly to the root. Implemented via a simple two-pass recursive procedure:
   ```
   FIND-SET(x)
     if x ≠ x.p
       x.p = FIND-SET(x.p)
     return x.p
   ```

**Pseudocode**:
- MAKE-SET(x): x.p = x; x.rank = 0
- UNION(x, y): LINK(FIND-SET(x), FIND-SET(y))
- LINK(x, y): If x.rank > y.rank, y.p = x; else x.p = y, and if ranks equal, increment y.rank.

**Running times**:
- Union by rank alone: O(m lg n)
- Path compression alone: Θ(n + f · (1 + log_{2+f/n} n)) for f FIND-SET operations
- Both together: **O(m · α(n))** — nearly linear

### Amortized Analysis with α(n) (Section 21.4)
The analysis uses the Ackermann-like function A_k(j):
- A₀(j) = j + 1
- A_k(j) = A_{k−1}^{(j+1)}(j) for k ≥ 1 (applying A_{k−1} repeatedly j + 1 times starting from j)

This function grows astronomically fast:
- A₁(1) = 3, A₂(1) = 7, A₃(1) = 2047, A₄(1) > 10^{80}

The inverse α(n) = min{k : A_k(1) ≥ n} grows incredibly slowly:
- α(n) = 0 for n ≤ 2; α(n) = 1 for n = 3; α(n) = 2 for 4 ≤ n ≤ 7; α(n) = 3 for 8 ≤ n ≤ 2047; α(n) = 4 for 2048 ≤ n ≤ A₄(1) (an astronomically large number).

**Potential function**: For each node x, φ(x) = α(n)·x.rank if x is a root or has rank 0; otherwise φ(x) = (α(n) − level(x))·x.rank − iter(x), where level(x) and iter(x) track how quickly x.p.rank grows relative to iterated applications of A_{level(x)} to x.rank.

**Key lemmas**:
- **Lemma 21.4**: x.rank < x.p.rank for non-root x (ranks strictly increase toward root).
- **Lemma 21.6**: All ranks are at most n − 1 (tighter bound: ⌊lg n⌋).
- **Lemma 21.8**: 0 ≤ φ(x) ≤ α(n)·x.rank for all x.
- **Lemma 21.11**: Amortized cost of MAKE-SET is O(1).
- **Lemma 21.12**: Amortized cost of LINK is O(α(n)).
- **Lemma 21.13**: Amortized cost of FIND-SET is O(α(n)) — at least s − (α(n) + 2) nodes on the find path of length s have their potential decrease by ≥ 1.

**Theorem 21.14**: A sequence of m MAKE-SET, UNION, and FIND-SET operations, n of which are MAKE-SET, runs in O(m · α(n)) worst-case time on a disjoint-set forest with union by rank and path compression.

## Complexity Analysis
| Implementation | MAKE-SET | UNION | FIND-SET | m operations total |
|---------------|----------|-------|----------|-------------------|
| Linked list (naive) | O(1) | O(n) amortized | O(1) | O(m · n) |
| Linked list + weighted union | O(1) | O(lg n) amortized | O(1) | O(m + n lg n) |
| Forest (union by rank only) | O(1) | O(lg n) | O(lg n) | O(m lg n) |
| Forest (path compression only) | O(1) | — | O(log n) amortized | Θ(n + f·(1 + log_{2+f/n} n)) |
| **Forest (both heuristics)** | **O(1)** | **O(α(n))** | **O(α(n))** | **O(m · α(n))** |

## Key Takeaways
- The disjoint-set forest with both union by rank and path compression is the gold standard: O(m · α(n)) is effectively linear since α(n) ≤ 4 for all practically conceivable inputs.
- **Union by rank** keeps trees balanced (height O(lg n)); **path compression** flattens find paths so future operations are faster. Together, they are more powerful than either alone.
- The inverse Ackermann function α(n) arises naturally from the amortized potential analysis and captures how slowly the amortized cost grows beyond constant.
- Key applications include Kruskal's minimum spanning tree algorithm, computing connected components, and maintaining equivalence classes under dynamic merging.
- The analysis is one of the most sophisticated amortized arguments in CLRS, using a two-parameter potential function (level and iter) that tracks how far each node's parent rank has progressed through the Ackermann hierarchy.
