# Chapter 22: Elementary Graph Algorithms

## Overview

This chapter establishes the foundational toolkit for working with graphs algorithmically. It begins with how to represent graphs in memory, then develops two cornerstone traversal strategies—breadth-first search and depth-first search—each of which reveals different structural properties of the graph. These traversals serve as building blocks for two powerful applications: topological sorting of directed acyclic graphs and decomposing a directed graph into its strongly connected components.

## Key Concepts

### Graph Representations (§22.1)

- A graph G = (V, E) can be stored as either an **adjacency-list** or an **adjacency-matrix**.
- **Adjacency lists** maintain an array of |V| linked lists. Vertex u's list contains every vertex v such that (u, v) ∈ E. For a directed graph the total number of list entries equals |E|; for an undirected graph each edge appears in two lists, giving 2|E| entries overall. This representation uses Θ(V + E) space and is preferred when the graph is **sparse** (|E| much less than |V|²).
- **Adjacency matrices** use a |V| × |V| boolean matrix A where entry a_{ij} = 1 when edge (i, j) exists. Lookups are O(1), but space is always Θ(V²) regardless of how many edges exist. This representation suits **dense** graphs or situations requiring constant-time edge queries.
- For undirected graphs the adjacency matrix is symmetric (A = Aᵀ), so in principle only half the matrix needs to be stored.
- Both representations extend naturally to **weighted graphs**: adjacency lists store the weight alongside each neighbor, and the matrix stores the weight in place of the boolean indicator.

### Vertex Coloring Convention

Both BFS and DFS use a three-color scheme to track progress:

| Color | Meaning |
|-------|---------|
| **WHITE** | Undiscovered — the algorithm has not yet encountered this vertex |
| **GRAY** | Discovered but not fully explored — currently in the frontier |
| **BLACK** | Finished — all neighbors have been examined |

### Predecessor Subgraph

Both traversals build a **predecessor (or parent) subgraph** through π pointers. Following π links from any vertex back to the source traces a path in the search tree (or forest). This structure is central to reconstructing paths and understanding reachability.

## Algorithms and Techniques

### Breadth-First Search (§22.2)

BFS systematically explores a graph outward from a source vertex s, visiting all vertices at distance k before any vertex at distance k + 1.

**Mechanism:**

1. Initialize every vertex as WHITE with distance d = ∞ and predecessor π = NIL.
2. Mark s GRAY, set s.d = 0, and place s in a FIFO queue.
3. Repeatedly dequeue a vertex u. For each neighbor v of u that is still WHITE: mark v GRAY, set v.d = u.d + 1 and v.π = u, then enqueue v.
4. After processing all of u's neighbors, color u BLACK.

**Key properties:**

- BFS computes **shortest-path distances** measured in number of edges (unweighted shortest paths). When the algorithm finishes, v.d = δ(s, v) for every vertex v, where δ(s, v) is the minimum number of edges on any s↝v path (or ∞ if v is unreachable).
- The queue satisfies a **monotonicity** invariant: at any moment the distances in the queue differ by at most 1, and they appear in non-decreasing order.
- The predecessor subgraph forms a **breadth-first tree** rooted at s. Every tree path from s to a vertex v is a shortest path in the original graph.
- A simple PRINT-PATH routine follows π pointers from v back to s and prints the vertices in order, yielding a shortest path.

### Depth-First Search (§22.3)

DFS explores as far as possible along each branch before backtracking, naturally modeling recursive exploration.

**Mechanism:**

1. Initialize all vertices WHITE with π = NIL. Set a global clock `time = 0`.
2. Iterate over all vertices; for each WHITE vertex u, call DFS-VISIT(u).
3. DFS-VISIT(u): increment time and record u.d (discovery time), color u GRAY. For each WHITE neighbor v, set v.π = u and recurse on v. After all neighbors are explored, color u BLACK, increment time, and record u.f (finishing time).

Unlike BFS, DFS may restart from multiple sources, producing a **depth-first forest** of several trees.

**Timestamps and the Parenthesis Theorem:**

Every vertex receives two timestamps in the range 1 to 2|V|. The **parenthesis theorem** states that for any two vertices u and v, exactly one of three relationships holds:

- The intervals [u.d, u.f] and [v.d, v.f] are entirely **disjoint** — neither is an ancestor of the other in the DFS forest.
- [u.d, u.f] **contains** [v.d, v.f] — v is a descendant of u.
- [v.d, v.f] **contains** [u.d, u.f] — u is a descendant of v.

This gives the nesting corollary: v is a proper descendant of u in the DFS forest if and only if u.d < v.d < v.f < u.f.

**White-Path Theorem:**

Vertex v becomes a descendant of u in the DFS forest if and only if, at the moment u is discovered, there exists a path from u to v consisting entirely of WHITE vertices. This theorem is the key tool for reasoning about what DFS "captures."

**Edge Classification:**

DFS partitions every edge of a directed graph into four categories based on the color of the destination vertex when the edge is explored:

| Type | Destination color | Intuition |
|------|-------------------|-----------|
| **Tree edge** | WHITE | Part of the DFS forest; the edge that first discovers v |
| **Back edge** | GRAY | Points to an ancestor on the current DFS path; signals a cycle |
| **Forward edge** | BLACK, v.d > u.d | Points to a descendant that was already finished |
| **Cross edge** | BLACK, v.d < u.d | Points to a vertex in a different branch or earlier tree |

In an **undirected graph**, every edge is classified as either a tree edge or a back edge — forward and cross edges cannot occur.

### Topological Sort (§22.4)

A topological sort of a directed acyclic graph (DAG) produces a linear ordering of vertices such that for every edge (u, v), vertex u appears before v.

**Algorithm:**

1. Run a full DFS on the graph.
2. As each vertex finishes (turns BLACK), prepend it to a linked list.
3. Return the list — it is a valid topological ordering.

**Why it works:** For any edge (u, v) in a DAG, DFS guarantees v.f < u.f (v finishes before u). Since vertices are prepended on finishing, u ends up before v in the output list. The absence of back edges (which would indicate a cycle) is both necessary and sufficient for the graph to be a DAG, confirming the ordering is well-defined.

**Applications:** Topological sort is essential for scheduling tasks with dependency constraints, ordering compilation units, resolving symbol dependencies, and determining evaluation order in data-flow graphs.

### Strongly Connected Components (§22.5)

A strongly connected component (SCC) of a directed graph is a maximal set of vertices C such that every vertex in C is reachable from every other vertex in C. Decomposing a graph into its SCCs reveals its coarse-grained, DAG-shaped macro-structure.

**Algorithm (Kosaraju's method):**

1. **First DFS pass:** Run DFS on the original graph G. Record the finishing time u.f for every vertex.
2. **Compute the transpose:** Build Gᵀ by reversing the direction of every edge.
3. **Second DFS pass:** Run DFS on Gᵀ, but process vertices in **decreasing** order of the finishing times computed in step 1.
4. **Read off the SCCs:** Each tree produced by the second DFS corresponds to exactly one SCC.

**Why it works:**

- G and Gᵀ share the same set of SCCs (reversing edges preserves mutual reachability within a component).
- The **component graph** G^SCC — obtained by collapsing each SCC into a single super-vertex — is always a DAG.
- The first DFS establishes finishing-time ordering: if there is an edge from component C to component C' in the component graph, then f(C) > f(C'), where f(C) is the maximum finishing time among vertices in C.
- Processing Gᵀ in decreasing finishing-time order ensures each second-pass DFS tree stays confined to a single SCC. Edges that cross between components in Gᵀ point from lower to higher finishing times, so the second DFS never "leaks" into an unrelated component.

## Complexity Analysis

| Algorithm | Time | Space |
|-----------|------|-------|
| BFS | O(V + E) | O(V) for color/distance/predecessor arrays + O(V) queue |
| DFS | Θ(V + E) | O(V) for color/timestamp/predecessor arrays + O(V) implicit recursion stack |
| Topological Sort | Θ(V + E) | Same as DFS plus O(V) linked list |
| SCC (Kosaraju) | Θ(V + E) | O(V + E) for Gᵀ plus DFS overhead |

**Representation costs:**

| Representation | Space | Edge query | Iterate neighbors of u |
|----------------|-------|------------|------------------------|
| Adjacency list | Θ(V + E) | O(degree(u)) | O(degree(u)) |
| Adjacency matrix | Θ(V²) | O(1) | O(V) |

### Important Theorems and Lemmas

- **Lemma 22.1 (Triangle inequality):** For any edge (u, v), δ(s, v) ≤ δ(s, u) + 1. Shortest-path distance can improve by at most one hop along any single edge.
- **Lemma 22.2 (Upper-bound property):** BFS never underestimates — at every point during execution, v.d ≥ δ(s, v).
- **Lemma 22.3 (Queue monotonicity):** If vertices are dequeued in order v₁, v₂, …, then their d-values form a non-decreasing sequence that spans at most two consecutive integer values at any moment.
- **Theorem 22.5 (BFS correctness):** Upon termination v.d = δ(s, v) for all v ∈ V, and the predecessor subgraph is a shortest-path tree.
- **Theorem 22.7 (Parenthesis theorem):** DFS discovery/finishing intervals are properly nested or disjoint.
- **Theorem 22.9 (White-path theorem):** Descendancy in the DFS forest is characterized by the existence of a white path at discovery time.
- **Theorem 22.10:** In an undirected graph, DFS produces only tree edges and back edges.
- **Lemma 22.11:** A directed graph is acyclic if and only if DFS yields no back edges.
- **Theorem 22.12:** Topological sort is correct — the output respects all edge directions in the DAG.
- **Lemma 22.13:** The component graph G^SCC is a DAG.
- **Lemma 22.14 / Corollary 22.15:** Edges between SCCs respect the finishing-time order, ensuring the second DFS pass correctly isolates components.
- **Theorem 22.16:** Kosaraju's algorithm correctly identifies all SCCs.

## Key Takeaways

- **Representation choice matters.** Adjacency lists are space-efficient for sparse graphs and dominate in practice; adjacency matrices offer constant-time edge lookup and simplify certain matrix-based algorithms. Choosing wisely affects every downstream algorithm's constant factors.
- **BFS and DFS are complementary workhorses.** BFS discovers shortest (unweighted) paths and explores level by level; DFS discovers deep structure—timestamps, back edges, and reachability—by probing exhaustively before backtracking. Nearly every graph algorithm builds on one of these two traversals.
- **DFS timestamps encode rich structural information.** The parenthesis theorem, white-path theorem, and edge classification all derive from the interplay of discovery and finishing times. Understanding timestamps is the key to reasoning about DFS-based algorithms.
- **Topological sort reduces to DFS.** A single depth-first traversal of a DAG, with vertices recorded in reverse finishing order, yields a valid topological ordering — an elegant and efficient solution to dependency scheduling.
- **SCC decomposition reveals macro-structure.** Kosaraju's two-pass DFS algorithm decomposes any directed graph into its strongly connected components in linear time, exposing the underlying DAG of component-level dependencies. This is foundational for program analysis, model checking, and 2-SAT solving.
