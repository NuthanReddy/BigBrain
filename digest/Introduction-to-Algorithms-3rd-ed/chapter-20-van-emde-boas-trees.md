# Chapter 20: van Emde Boas Trees

## Overview
Van Emde Boas (vEB) trees support all priority-queue operations—MEMBER, INSERT, DELETE, MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR—in O(lg lg u) worst-case time, where u is the universe size. The key constraint is that keys must be integers in {0, 1, …, u − 1} with no duplicates. The chapter develops this structure incrementally: starting from direct addressing and superimposed binary trees, through proto van Emde Boas structures that expose the recursive strategy, and finally the full vEB tree that achieves O(lg lg u) per operation.

## Key Concepts
- **Universe size u**: Keys are integers in {0, …, u − 1}. We assume u = 2^k for integer k ≥ 1. The parameter n denotes the number of elements currently stored.
- **√u-way decomposition**: The universe is divided into ⌈√u⌉ clusters, each of size ⌊√u⌋. A key x maps to cluster high(x) = ⌊x/⌊√u⌋⌋ at position low(x) = x mod ⌊√u⌋. The function index(x, y) = x·⌊√u⌋ + y reconstructs the key.
- **Upper and lower square roots**: When u = 2^(2k+1) (odd power of 2), ⌈√u⌉ = 2^⌈(lg u)/2⌉ and ⌊√u⌋ = 2^⌊(lg u)/2⌋, ensuring clean recursion regardless of whether lg u is even or odd.
- **Summary structure**: A separate vEB tree of size ⌈√u⌉ tracks which clusters are non-empty, enabling fast navigation.
- **min and max attributes**: The minimum element is stored *outside* the recursive cluster structure (not inserted into any cluster), while max is stored inside. This asymmetry is crucial for reducing recursive calls from two to one.
- **Recurrence**: T(u) = T(⌈√u⌉) + O(1), which solves to T(u) = O(lg lg u) via the substitution m = lg u → S(m) = S(⌈m/2⌉) + O(1) = O(lg m) = O(lg lg u).

## Algorithms and Techniques

### Preliminary Approaches (Section 20.1)
1. **Direct addressing (bit vector)**: INSERT, DELETE, MEMBER in O(1), but MINIMUM, MAXIMUM, SUCCESSOR, PREDECESSOR in Θ(u).
2. **Superimposed binary tree**: Overlay a binary tree of bits on the bit vector. Each internal node stores the OR of its children. Operations drop to O(lg u).
3. **Tree of degree √u (constant height 2)**: Introduces the cluster/summary decomposition. INSERT in O(1), other operations in O(√u). This is the key idea that vEB trees recursivize.

### Proto van Emde Boas Structures (Section 20.2)
Recursively apply the √u-way decomposition: a proto-EB(u) contains √u clusters (each proto-EB(√u)) and a summary (also proto-EB(√u)).

- **PROTO-VEB-MEMBER(V, x)**: Recurses into cluster[high(x)] with low(x). One recursive call → T(u) = T(√u) + O(1) = O(lg lg u). ✓
- **PROTO-VEB-MINIMUM(V)**: Finds the first non-empty cluster via summary, then finds the minimum within that cluster. **Two** recursive calls → T(u) = 2T(√u) + O(1) = Θ(lg u). ✗
- **PROTO-VEB-SUCCESSOR(V, x)**: Searches within x's cluster, then in the summary. **Two** recursive calls plus one MINIMUM call → T(u) = Θ(lg u · lg lg u). ✗
- **PROTO-VEB-INSERT(V, x)**: Inserts into cluster and updates summary. **Two** recursive calls → T(u) = Θ(lg u). ✗

The proto-vEB structure demonstrates the recursive strategy but fails to achieve O(lg lg u) because most operations make two recursive calls.

### van Emde Boas Trees (Section 20.3)
Adds min and max attributes to eliminate the second recursive call:

**VEB-TREE-MINIMUM(V)** / **VEB-TREE-MAXIMUM(V)**: Return V.min / V.max in O(1).

**VEB-TREE-MEMBER(V, x)**: Check if x equals min or max first (O(1)), then recurse into cluster[high(x)]. One recursive call → O(lg lg u).

**VEB-TREE-SUCCESSOR(V, x)**:
1. Base case (u = 2): return 1 if x = 0 and max = 1.
2. If x < V.min, return V.min.
3. Check if x's successor is within its cluster by comparing low(x) with the cluster's max (O(1) via VEB-TREE-MAXIMUM).
4. If yes, recurse into the cluster. If no, find the next non-empty cluster via the summary, then return its minimum.
- Only **one** recursive call (either into a cluster or into the summary, never both) → O(lg lg u).

**VEB-TREE-PREDECESSOR(V, x)**: Symmetric to SUCCESSOR with one extra case: if the predecessor is not in any cluster, it might be V.min (which is stored outside all clusters).

**VEB-TREE-INSERT(V, x)**:
1. If V is empty, set min = max = x (O(1)).
2. If x < V.min, swap x with V.min (new x will be inserted into a cluster).
3. If x's cluster is empty, insert the cluster number into summary and do a trivial insert. If non-empty, recurse into the cluster.
- Only **one** recursive call → O(lg lg u).

**VEB-TREE-DELETE(V, x)**:
1. If V has one element, set min = max = NIL.
2. If u = 2, update min and max directly.
3. If x = V.min, find the actual minimum from the first cluster and replace V.min, then delete that element from its cluster.
4. After deleting from a cluster, if the cluster becomes empty, remove it from the summary.
5. Update max if necessary.
- At most **one** recursive call into a cluster and possibly one into the summary, but they handle different cases → O(lg lg u).

## Complexity Analysis
| Operation | Time |
|-----------|------|
| MINIMUM / MAXIMUM | O(1) |
| MEMBER | O(lg lg u) |
| SUCCESSOR / PREDECESSOR | O(lg lg u) |
| INSERT | O(lg lg u) |
| DELETE | O(lg lg u) |

- **Space**: O(u) total (Problem 20-1).
- **Creation**: O(u) time to initialize an empty vEB tree.
- The O(lg lg u) bound comes from the recurrence T(u) ≤ T(⌈√u⌉) + O(1), which halves the number of bits (lg u) at each level of recursion.

## Key Takeaways
- Van Emde Boas trees break the Ω(lg n) comparison-based barrier by exploiting the integer structure of keys, achieving O(lg lg u) per operation.
- The critical design insight is storing min outside the recursive structure and max inside, which reduces every operation to at most one recursive call on a universe of size ≈ √u.
- The √u-way recursive decomposition halves the bit-length at each level, giving lg lg u levels of recursion.
- The O(u) space and creation time is a drawback for sparse sets; vEB trees are most beneficial when many operations are performed on a reasonably sized universe.
- vEB trees are useful as building blocks in other algorithms and as a conceptual bridge to more practical structures like x-fast and y-fast tries.
