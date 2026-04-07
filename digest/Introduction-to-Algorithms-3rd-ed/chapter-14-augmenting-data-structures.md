# Chapter 14: Augmenting Data Structures

## Overview
This chapter teaches a general methodology for extending ("augmenting") standard data structures with additional information to support new operations efficiently. Rather than designing entirely new data structures from scratch, we add attributes to existing ones and show how to maintain them during modifications. The chapter demonstrates this approach with two concrete augmented red-black trees: **order-statistic trees** (supporting rank queries in O(lg n)) and **interval trees** (supporting overlap queries in O(lg n)), and presents a general theorem (Theorem 14.1) that simplifies augmenting red-black trees.

## Key Concepts

- **Augmentation methodology** (four steps):
  1. **Choose an underlying data structure** (e.g., red-black tree).
  2. **Determine additional information** to store in each node.
  3. **Verify** that the additional information can be maintained during basic modifying operations (INSERT, DELETE) without increasing asymptotic cost.
  4. **Develop new operations** that exploit the additional information.

- **Order-statistic tree**: A red-black tree augmented with a `size` attribute in each node x, where `x.size` = number of internal nodes in the subtree rooted at x (including x). The identity `x.size = x.left.size + x.right.size + 1` holds, with `T.nil.size = 0`.

- **Interval tree**: A red-black tree augmented with a `max` attribute in each node x, where `x.max` = maximum endpoint of any interval stored in the subtree rooted at x. Keyed by the low endpoint of each interval. The identity `x.max = max(x.int.high, x.left.max, x.right.max)` holds.

- **Interval trichotomy**: For any two intervals i and i', exactly one holds: (a) they overlap, (b) i is entirely to the left of i', or (c) i is entirely to the right of i'.

- **Theorem 14.1 (Augmenting a red-black tree)**: If an attribute f in each node x depends only on the information in x, x.left, and x.right (including x.left.f and x.right.f), then f can be maintained during insertion and deletion without affecting the O(lg n) performance. The key insight: changes to f propagate only upward to ancestors, and rotations affect only O(1) nodes each.

## Algorithms and Techniques

### Order-Statistic Operations

**OS-SELECT(x, i)**: Retrieves the ith smallest key in the subtree rooted at x.
1. Compute r = x.left.size + 1 (the rank of x within its subtree).
2. If i = r, return x.
3. If i < r, recurse into x.left with the same i.
4. If i > r, recurse into x.right with i − r.

Each recursive call descends one level, so the running time is O(lg n).

**OS-RANK(T, x)**: Determines the rank (position in sorted order) of node x in tree T.
1. Initialize r = x.left.size + 1.
2. Walk upward from x to the root. Each time the current node y is a right child, add y.p.left.size + 1 to r (counting the left subtree and parent that precede x in inorder).
3. Return r when y reaches the root.

Uses a loop invariant: r is the rank of x.key in the subtree rooted at the current node y. Running time: O(lg n).

### Maintaining Size During Modifications

**During insertion** (Phase 1): Increment x.size for each node x on the path from root to the insertion point. Cost: O(lg n). Phase 2 (fixup): At most 2 rotations. After each rotation, update sizes in O(1):
```
y.size = x.size
x.size = x.left.size + x.right.size + 1
```

**During deletion** (Phase 1): Decrement x.size for each node on the path from the removed/moved node up to the root. Cost: O(lg n). Phase 2 (fixup): At most 3 rotations, each with O(1) size updates.

Total cost for both insertion and deletion remains O(lg n).

### Interval Tree Operations

**INTERVAL-INSERT(T, x)** and **INTERVAL-DELETE(T, x)**: Standard red-black tree insert/delete using x.int.low as the key, maintaining x.max via `x.max = max(x.int.high, x.left.max, x.right.max)`. By Theorem 14.1, this takes O(lg n) time.

**INTERVAL-SEARCH(T, i)**: Finds any node whose interval overlaps i, or returns T.nil.
1. Start at x = T.root.
2. While x ≠ T.nil and i does not overlap x.int:
   - If x.left ≠ T.nil and x.left.max ≥ i.low, go left (x = x.left).
   - Else go right (x = x.right).
3. Return x.

**Correctness (Theorem 14.2)**: The algorithm maintains the invariant that if any interval in T overlaps i, then the subtree rooted at x contains such an interval.
- Going right is safe: if x.left = T.nil or x.left.max < i.low, then no interval in the left subtree can overlap i (all their high endpoints are ≤ x.left.max < i.low).
- Going left is safe (contrapositive): if no interval in the left subtree overlaps i, then since some interval i' in the left subtree has i'.high = x.left.max ≥ i.low, it must be that i.high < i'.low. By the BST property (keyed on low endpoints), all intervals i'' in the right subtree satisfy i''.low ≥ i'.low > i.high, so none overlap i either.

Running time: O(lg n) (one path from root to leaf).

## Complexity Analysis

### Order-Statistic Tree
| Operation | Time |
|---|---|
| OS-SELECT(x, i) | O(lg n) |
| OS-RANK(T, x) | O(lg n) |
| INSERT (with size maintenance) | O(lg n) |
| DELETE (with size maintenance) | O(lg n) |
| SEARCH, MIN, MAX, SUCCESSOR, PREDECESSOR | O(lg n) |

Space: O(n) — one extra integer (size) per node.

### Interval Tree
| Operation | Time |
|---|---|
| INTERVAL-INSERT(T, x) | O(lg n) |
| INTERVAL-DELETE(T, x) | O(lg n) |
| INTERVAL-SEARCH(T, i) | O(lg n) |

Space: O(n) — one extra value (max) per node plus the interval per node.

### Theorem 14.1 Applicability
Any attribute f computable from x, x.left, x.right (and their f values) can be maintained in O(lg n) time during insertion and deletion. This covers:
- Subtree sizes, subtree sums, subtree maxima/minima
- Any associative aggregate over the subtree's elements (Exercise 14.2-3 shows O(1) per rotation for associative operators)

## Key Takeaways

- **Augmentation is a powerful design paradigm**: rather than building data structures from scratch, extend proven structures (like red-black trees) with additional attributes to support new operations. This leverages existing correctness and performance guarantees.
- **Theorem 14.1 provides a simple "litmus test"**: if the new attribute depends only on a node and its immediate children, it can be maintained for free (asymptotically) during red-black tree modifications. This covers a wide range of useful attributes.
- **Order-statistic trees** add a single `size` field to enable O(lg n) selection-by-rank and rank-finding—operations that would require O(n) time on a plain BST or sorted array.
- **Interval trees** elegantly solve the dynamic interval overlap problem by augmenting with a `max` field and using a simple one-path search algorithm with a subtle correctness proof.
- **The four-step augmentation methodology** (choose structure, add information, verify maintenance, develop operations) provides a systematic framework applicable far beyond the two examples in this chapter.
