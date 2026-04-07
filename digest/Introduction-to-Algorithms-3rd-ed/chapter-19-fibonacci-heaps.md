# Chapter 19: Fibonacci Heaps

## Overview
Fibonacci heaps are a sophisticated implementation of mergeable heaps that achieve excellent amortized time bounds by deferring consolidation work. They support INSERT, UNION, and DECREASE-KEY in O(1) amortized time, and EXTRACT-MIN and DELETE in O(lg n) amortized time. These bounds make Fibonacci heaps theoretically optimal for algorithms like Dijkstra's shortest paths and Prim's minimum spanning tree, where DECREASE-KEY is called frequently.

## Key Concepts
- **Mergeable heap interface**: MAKE-HEAP, INSERT, MINIMUM, EXTRACT-MIN, UNION, plus DECREASE-KEY and DELETE.
- **Structure**: A Fibonacci heap is a collection of min-heap-ordered rooted trees. Roots are linked in a circular, doubly linked *root list*. A pointer H.min points to the overall minimum node.
- **Node attributes**: Each node x has x.key, x.degree (number of children), x.p (parent), x.child (one child pointer), x.left/x.right (sibling pointers in circular doubly linked lists), and x.mark (whether x has lost a child since last becoming a child of another node).
- **Lazy design philosophy**: Operations like INSERT and UNION do minimal work (O(1)), accumulating structural debt. EXTRACT-MIN pays off this debt by *consolidating* the root list.
- **Potential function**: Φ(H) = t(H) + 2·m(H), where t(H) is the number of trees in the root list and m(H) is the number of marked nodes. This function drives the amortized analysis.
- **Maximum degree bound**: D(n) = O(lg n), proved via Fibonacci numbers (the source of the data structure's name).

## Algorithms and Techniques

### FIB-HEAP-INSERT(H, x)
Initializes x (degree 0, unmarked, no parent/child) and adds it to the root list. Updates H.min if x.key < H.min.key. Increments H.n. Amortized cost: O(1) (potential increases by 1).

### FIB-HEAP-UNION(H1, H2)
Concatenates the root lists of H1 and H2, updates the min pointer, and sets H.n = H1.n + H2.n. Amortized cost: O(1) (potential change is 0).

### FIB-HEAP-EXTRACT-MIN(H)
The most complex operation:
1. Add all children of the minimum node z to the root list.
2. Remove z from the root list.
3. **CONSOLIDATE(H)**: Repeatedly link roots with the same degree until all roots have distinct degrees. Uses an auxiliary array A[0..D(H.n)] indexed by degree. For each root w, if another root y in A has the same degree, link the one with the larger key under the one with the smaller key, incrementing the winner's degree.
4. Rebuild the root list from array A and find the new minimum.
- **FIB-HEAP-LINK(H, y, x)**: Makes y a child of x, increments x.degree, clears y.mark.
- Amortized cost: O(D(n)) = O(lg n).

### FIB-HEAP-DECREASE-KEY(H, x, k)
1. Decrease x.key to k.
2. If min-heap order is violated (x.key < parent's key), **CUT(H, x, y)**: remove x from its parent y's child list, add x to the root list, unmark x.
3. **CASCADING-CUT(H, y)**: If y is marked (already lost one child), cut y from its parent too and recurse. If y is unmarked, mark it.
4. Update H.min if needed.
- The mark mechanism ensures at most O(1) amortized cost: each cascading cut reduces the number of marked nodes, offsetting the potential increase from new root-list trees.

### FIB-HEAP-DELETE(H, x)
Decrease x's key to −∞, then extract the minimum. Amortized cost: O(D(n)) = O(lg n).

### Bounding the Maximum Degree (Section 19.4)
- **Lemma 19.1**: If x has degree k and children y₁, y₂, …, y_k (in link order), then y_i.degree ≥ i − 2 for i ≥ 2.
- **Lemma 19.4**: size(x) ≥ F_{k+2} ≥ φ^k, where F_k is the kth Fibonacci number and φ = (1+√5)/2.
- **Corollary 19.5**: D(n) = O(lg n), since n ≥ φ^k implies k ≤ log_φ n.

## Complexity Analysis
| Operation | Binary Heap (worst-case) | Fibonacci Heap (amortized) |
|-----------|------------------------|---------------------------|
| MAKE-HEAP | Θ(1) | Θ(1) |
| INSERT | Θ(lg n) | Θ(1) |
| MINIMUM | Θ(1) | Θ(1) |
| EXTRACT-MIN | Θ(lg n) | O(lg n) |
| UNION | Θ(n) | Θ(1) |
| DECREASE-KEY | Θ(lg n) | Θ(1) |
| DELETE | Θ(lg n) | O(lg n) |

Space: O(n) for an n-node Fibonacci heap.

## Key Takeaways
- Fibonacci heaps achieve their performance by being *lazy*: INSERT and UNION just add to the root list, deferring structural cleanup to EXTRACT-MIN's consolidation phase.
- The O(1) amortized DECREASE-KEY is the primary theoretical advantage, enabling faster graph algorithms (e.g., Dijkstra in O(V lg V + E) time with Fibonacci heaps vs. O((V + E) lg V) with binary heaps).
- The mark/cascading-cut mechanism limits tree degradation: a node is cut from its parent after losing two children, ensuring the subtree size remains exponential in the node's degree.
- The name "Fibonacci heap" comes from the Fibonacci number lower bound on subtree sizes, which is key to proving D(n) = O(lg n).
- In practice, the constant factors and programming complexity make Fibonacci heaps less attractive than binary heaps for most applications, but they remain important theoretically.
