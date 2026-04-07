# Chapter 6: Heapsort

## Overview

This chapter introduces **heapsort**, a comparison-based sorting algorithm that combines the best attributes of merge sort and insertion sort: it runs in O(n lg n) time like merge sort, yet sorts **in place** like insertion sort. The chapter also introduces the **heap** data structure—a nearly complete binary tree stored as an array—which is not only the engine behind heapsort but also the foundation for an efficient **priority queue** implementation used extensively in later chapters (e.g., Dijkstra's algorithm, Prim's MST).

## Key Concepts

### 6.1 — Heaps

- A **(binary) heap** is an array that can be viewed as a nearly complete binary tree. The tree is completely filled on all levels except possibly the lowest, which is filled from the left.
- An array `A` representing a heap has two attributes:
  - `A.length` — total number of elements in the array.
  - `A.heap-size` — how many elements in `A[1..A.heap-size]` are valid heap elements (≤ `A.length`).
- **Navigating the tree** is done with simple index arithmetic (1-based indexing):
  - `PARENT(i) = ⌊i/2⌋`
  - `LEFT(i) = 2i`
  - `RIGHT(i) = 2i + 1`
  - These can be computed in one instruction via bit-shifting, making them extremely fast.
- **Max-heap property**: For every node `i` other than the root, `A[PARENT(i)] ≥ A[i]`. The largest element is at the root.
- **Min-heap property**: For every node `i` other than the root, `A[PARENT(i)] ≤ A[i]`. The smallest element is at the root.
- **Height** of a node is the number of edges on the longest downward path to a leaf. The height of an n-element heap is **⌊lg n⌋**.
- Leaves occupy indices `⌊n/2⌋ + 1, ⌊n/2⌋ + 2, …, n` (Exercise 6.1-7), which is important for BUILD-MAX-HEAP.

### 6.2 — Maintaining the Heap Property (MAX-HEAPIFY)

- **MAX-HEAPIFY(A, i)** is the key subroutine for maintaining the max-heap property. It assumes the left and right subtrees of node `i` are already max-heaps, but `A[i]` may be smaller than its children.
- The algorithm "floats down" the offending value:
  1. Compare `A[i]`, `A[LEFT(i)]`, and `A[RIGHT(i)]` to find the `largest`.
  2. If `largest ≠ i`, swap `A[i]` with `A[largest]` and recurse on the subtree rooted at `largest`.
  3. If `A[i]` is already the largest, the subtree is a valid max-heap — terminate.
- The worst-case subtree size for a child is **2n/3** (when the bottom level is exactly half full), giving the recurrence `T(n) ≤ T(2n/3) + Θ(1)`, which solves to **O(lg n)** by case 2 of the Master Theorem.
- Equivalently, MAX-HEAPIFY on a node of height `h` runs in **O(h)** time.

### 6.3 — Building a Heap (BUILD-MAX-HEAP)

- **BUILD-MAX-HEAP(A)** converts an arbitrary array into a max-heap using a bottom-up approach:
  1. Set `A.heap-size = A.length`.
  2. Iterate `i` from `⌊A.length/2⌋` downto `1`, calling `MAX-HEAPIFY(A, i)` at each step.
- Leaves (indices `⌊n/2⌋ + 1` to `n`) are trivially 1-element max-heaps, so only internal nodes need processing.
- **Loop invariant**: At the start of each iteration, every node `i+1, i+2, …, n` is the root of a max-heap. This guarantees that when MAX-HEAPIFY is called on node `i`, both its children are already roots of valid max-heaps—exactly the precondition MAX-HEAPIFY requires.
- **Naïve bound**: O(n) calls × O(lg n) each = O(n lg n). This is correct but **not tight**.
- **Tight bound — O(n)**: Most nodes have small height. An n-element heap has at most ⌈n / 2^(h+1)⌉ nodes of height `h`. Summing the work across all heights:
  - `Σ (h=0 to ⌊lg n⌋) ⌈n / 2^(h+1)⌉ · O(h) = O(n · Σ h/2^h) = O(n · 2) = O(n)`
  - The key identity is `Σ (h=0 to ∞) h/2^h = 2` (obtained by substituting x = 1/2 into formula A.8).
- **BUILD-MIN-HEAP** is analogous, replacing MAX-HEAPIFY with MIN-HEAPIFY.

### 6.4 — The Heapsort Algorithm

- **HEAPSORT(A)** sorts an array in place in O(n lg n) time:
  1. Call `BUILD-MAX-HEAP(A)` to arrange the array into a max-heap.
  2. Iterate `i` from `A.length` downto `2`:
     - Exchange `A[1]` (the current max) with `A[i]`, placing the max in its final sorted position.
     - Decrement `A.heap-size` by 1 (shrink the heap, excluding the sorted tail).
     - Call `MAX-HEAPIFY(A, 1)` to restore the max-heap property on the reduced heap.
- **Loop invariant** (Exercise 6.4-2): At the start of each iteration, `A[1..i]` is a max-heap containing the `i` smallest elements, and `A[i+1..n]` contains the `n − i` largest elements in sorted order.

### 6.5 — Priority Queues

- A **priority queue** maintains a dynamic set `S` where each element has a **key**. Two flavors exist:
  - **Max-priority queue**: supports INSERT, MAXIMUM, EXTRACT-MAX, INCREASE-KEY.
  - **Min-priority queue**: supports INSERT, MINIMUM, EXTRACT-MIN, DECREASE-KEY.
- Practical applications:
  - **Job scheduling** (max-priority queue): always run the highest-priority job; add/remove jobs dynamically.
  - **Event-driven simulation** (min-priority queue): process events in chronological order.
  - **Graph algorithms** (min-priority queue): Dijkstra's shortest paths (Ch. 24), Prim's MST (Ch. 23).

#### Priority Queue Operations (max-heap based)

| Operation | Procedure | Idea | Time |
|---|---|---|---|
| **MAXIMUM** | `HEAP-MAXIMUM(A)` | Return `A[1]` (root of max-heap). | Θ(1) |
| **EXTRACT-MAX** | `HEAP-EXTRACT-MAX(A)` | Save `A[1]`, move last element to root, shrink heap, call MAX-HEAPIFY(A, 1). | O(lg n) |
| **INCREASE-KEY** | `HEAP-INCREASE-KEY(A, i, key)` | Set `A[i] = key`, then bubble up: repeatedly swap with parent while `A[i] > A[PARENT(i)]`. Error if `key < A[i]`. | O(lg n) |
| **INSERT** | `MAX-HEAP-INSERT(A, key)` | Expand heap by one, set new element to −∞, then call HEAP-INCREASE-KEY to set the correct value and bubble up. | O(lg n) |

- **Handle management**: In practice, each heap element stores a handle (pointer/index) to its application object and vice versa. When elements move during heap operations, these handles must be updated.
- **Summary**: A heap supports any priority-queue operation on a set of size n in **O(lg n)** time.

## Algorithms and Techniques

### MAX-HEAPIFY — Restore the heap property at a single node

```
MAX-HEAPIFY(A, i):
  l = LEFT(i)
  r = RIGHT(i)
  if l ≤ A.heap-size and A[l] > A[i]
      largest = l
  else largest = i
  if r ≤ A.heap-size and A[r] > A[largest]
      largest = r
  if largest ≠ i
      exchange A[i] with A[largest]
      MAX-HEAPIFY(A, largest)        // recurse on affected subtree
```

**Key insight**: Only one path from the node to a leaf is followed, so the work is proportional to the node's height.

### BUILD-MAX-HEAP — Convert an array into a max-heap

```
BUILD-MAX-HEAP(A):
  A.heap-size = A.length
  for i = ⌊A.length / 2⌋ downto 1
      MAX-HEAPIFY(A, i)
```

**Key insight**: Process nodes bottom-up so that both children of any node are already valid max-heaps when we heapify that node. Leaves need no work.

### HEAPSORT — In-place O(n lg n) sort

```
HEAPSORT(A):
  BUILD-MAX-HEAP(A)
  for i = A.length downto 2
      exchange A[1] with A[i]
      A.heap-size = A.heap-size - 1
      MAX-HEAPIFY(A, 1)
```

**Key insight**: Repeatedly extract the maximum and place it at the end of the array. The sorted portion grows from right to left.

### HEAP-EXTRACT-MAX — Remove and return the maximum

```
HEAP-EXTRACT-MAX(A):
  if A.heap-size < 1
      error "heap underflow"
  max = A[1]
  A[1] = A[A.heap-size]
  A.heap-size = A.heap-size - 1
  MAX-HEAPIFY(A, 1)
  return max
```

### HEAP-INCREASE-KEY — Increase a key and bubble up

```
HEAP-INCREASE-KEY(A, i, key):
  if key < A[i]
      error "new key is smaller than current key"
  A[i] = key
  while i > 1 and A[PARENT(i)] < A[i]
      exchange A[i] with A[PARENT(i)]
      i = PARENT(i)
```

### MAX-HEAP-INSERT — Insert a new element

```
MAX-HEAP-INSERT(A, key):
  A.heap-size = A.heap-size + 1
  A[A.heap-size] = -∞
  HEAP-INCREASE-KEY(A, A.heap-size, key)
```

## Complexity Analysis

| Procedure | Time Complexity | Space | Notes |
|---|---|---|---|
| PARENT / LEFT / RIGHT | Θ(1) | O(1) | Bit-shift operations |
| MAX-HEAPIFY | O(lg n) or O(h) | O(lg n) recursion stack* | Worst case: T(n) ≤ T(2n/3) + Θ(1); Master Theorem case 2 |
| BUILD-MAX-HEAP | **O(n)** | O(1) auxiliary | Tight bound via Σ h/2^h = 2; naïve O(n lg n) is loose |
| HEAPSORT | O(n lg n) | O(1) auxiliary | BUILD-MAX-HEAP is O(n); n−1 calls to MAX-HEAPIFY at O(lg n) each |
| HEAP-MAXIMUM | Θ(1) | O(1) | Simply returns A[1] |
| HEAP-EXTRACT-MAX | O(lg n) | O(1)* | Constant work + one MAX-HEAPIFY call |
| HEAP-INCREASE-KEY | O(lg n) | O(1) | Path from node to root has length O(lg n) |
| MAX-HEAP-INSERT | O(lg n) | O(1) | Expand + HEAP-INCREASE-KEY |

*MAX-HEAPIFY uses O(lg n) stack space if implemented recursively; an iterative version (Exercise 6.2-5) reduces this to O(1).

### Important results

- **Theorem (tight bound for BUILD-MAX-HEAP)**: Building a max-heap from an unordered array of n elements takes **O(n)** time, not O(n lg n). The proof relies on the fact that most nodes in a heap are near the bottom (small height), so the total work is dominated by the geometric series Σ h/2^h which converges to 2.
- **Worst-case heapsort is Θ(n lg n)**: Both the best case and worst case of heapsort on distinct elements are Θ(n lg n) (Exercises 6.4-4 and 6.4-5).
- An n-element heap has height **⌊lg n⌋** (Exercise 6.1-2), and at most **⌈n / 2^(h+1)⌉** nodes at any height h (Exercise 6.3-3).

### Additional topics (Problems)

- **Problem 6-1 (BUILD-MAX-HEAP via insertion)**: Building a heap by repeated MAX-HEAP-INSERT (top-down) requires **Θ(n lg n)** in the worst case—strictly worse than the bottom-up BUILD-MAX-HEAP which is O(n). The two methods may also produce different heaps on the same input.
- **Problem 6-2 (d-ary heaps)**: Generalizes binary heaps to d children per node. Height becomes O(log_d n). EXTRACT-MAX takes O(d log_d n) and INSERT/INCREASE-KEY take O(log_d n).
- **Problem 6-3 (Young tableaux)**: An m × n matrix with sorted rows and columns. EXTRACT-MIN and INSERT both run in O(m + n), and sorting n² numbers takes O(n³).

## Key Takeaways

- **Heapsort is an in-place, O(n lg n) comparison sort** — it never needs more than O(1) extra memory, making it useful when memory is constrained. However, a well-tuned quicksort typically outperforms it in practice due to better constant factors and cache behavior.
- **BUILD-MAX-HEAP runs in O(n), not O(n lg n)** — this is a crucial and somewhat counterintuitive result. The tight analysis exploits the fact that most heap nodes have small heights, so the total heapification cost is linear.
- **The heap data structure is more important than heapsort itself** — heaps provide an elegant O(lg n) implementation of priority queues, which are essential building blocks in graph algorithms (Dijkstra, Prim), event-driven simulations, and job schedulers.
- **MAX-HEAPIFY is the workhorse** — nearly every heap operation (build, sort, extract, insert) ultimately relies on MAX-HEAPIFY to restore the heap property, either by floating a value *down* (heapify) or bubbling a value *up* (increase-key / insert).
- **Two directions of repair**: MAX-HEAPIFY fixes violations by sifting *down* (used in build, sort, extract-max), while HEAP-INCREASE-KEY fixes violations by bubbling *up* (used in insert and key updates). Together they cover all cases where the heap property might be violated at a single node.
