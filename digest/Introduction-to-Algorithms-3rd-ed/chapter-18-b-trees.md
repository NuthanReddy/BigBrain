# Chapter 18: B-Trees

## Overview
B-trees are balanced search trees specifically designed to minimize disk I/O operations, making them ideal for database systems and secondary storage applications. Unlike binary search trees, B-tree nodes can have thousands of children, yielding a very low height of O(log_t n) where t is the minimum degree. This chapter defines B-trees, presents search, insertion (with proactive node splitting), and deletion operations—all executable in a single downward pass through the tree.

## Key Concepts
- **B-tree properties**: Every node x stores x.n keys in sorted order; internal nodes have x.n + 1 children. All leaves reside at the same depth. A fixed integer t ≥ 2 (the *minimum degree*) constrains node sizes: every non-root node has at least t − 1 keys and at most 2t − 1 keys.
- **Disk-access model**: Data is read/written in whole pages via DISK-READ and DISK-WRITE. B-tree nodes are sized to match disk pages, so each node access costs one disk I/O.
- **Branching factor**: Typical branching factors range from 50 to 2000. A B-tree of height 2 with branching factor 1001 can store over one billion keys, searchable with at most two disk accesses beyond the root.
- **2-3-4 trees**: The simplest B-tree occurs when t = 2, where every internal node has 2, 3, or 4 children.
- **Variants**: B⁺-trees store all satellite data in leaves; B*-trees require nodes to be at least 2/3 full.

## Algorithms and Techniques

### B-TREE-SEARCH(x, k)
Generalizes binary search tree lookup to multiway branching. At each node x, a linear scan finds the smallest index i such that k ≤ x.key_i, then either returns the key (if found), reports failure (if x is a leaf), or recurses into the appropriate child after a DISK-READ.

### B-TREE-CREATE(T)
Allocates an empty root node, sets it as a leaf with zero keys, writes it to disk. Runs in O(1) time and O(1) disk operations.

### B-TREE-INSERT(T, k) — Single-pass insertion with proactive splitting
- **B-TREE-SPLIT-CHILD(x, i)**: Splits a full child y = x.c_i (with 2t − 1 keys) around its median key. The median moves up into x, and the t − 1 largest keys go into a new node z. Uses Θ(t) CPU time and O(1) disk operations.
- **B-TREE-INSERT**: If the root is full, creates a new root and splits the old root first (the only way the tree grows in height—at the top). Then calls B-TREE-INSERT-NONFULL.
- **B-TREE-INSERT-NONFULL(x, k)**: Descends from x, splitting any full node encountered along the way, guaranteeing the recursion never reaches a full node. Inserts k into a leaf.

### B-TREE-DELETE(x, k) — Single-pass deletion
Handles three main cases in a single downward pass:
1. **Case 1**: k is in leaf node x — simply remove it.
2. **Case 2**: k is in internal node x — replace k with its predecessor (case 2a) or successor (case 2b) from a child with ≥ t keys, or merge the two adjacent children if both have t − 1 keys (case 2c).
3. **Case 3**: k is not in internal node x — ensure the child to descend into has ≥ t keys by borrowing from a sibling (case 3a) or merging with a sibling (case 3b).

If the root becomes empty after a merge, the tree's height shrinks by one.

## Complexity Analysis
| Operation | Disk Accesses | CPU Time |
|-----------|--------------|----------|
| SEARCH | O(h) = O(log_t n) | O(t · h) = O(t · log_t n) |
| CREATE | O(1) | O(1) |
| INSERT | O(h) | O(t · h) = O(t · log_t n) |
| SPLIT-CHILD | O(1) | Θ(t) |
| DELETE | O(h) | O(t · h) = O(t · log_t n) |

**Theorem 18.1**: For any n-key B-tree T of height h and minimum degree t ≥ 2, h ≤ log_t((n + 1)/2). The proof counts the minimum number of nodes at each depth: 1 root with ≥ 1 key, 2 nodes at depth 1, 2t at depth 2, …, 2t^(h−1) at depth h, giving n ≥ 2t^h − 1.

## Key Takeaways
- B-trees minimize disk I/O by matching node sizes to disk pages and keeping tree height very low through high branching factors.
- All operations (search, insert, delete) run in O(h) disk accesses and O(t·h) CPU time, where h = O(log_t n).
- Insertion uses proactive splitting on the way down to avoid backtracking; deletion uses proactive merging/borrowing for the same single-pass guarantee.
- The tree grows and shrinks at the root, not at the leaves, preserving the equal-depth-of-all-leaves invariant.
- B-trees save roughly a factor of lg t in disk accesses compared to red-black trees, which is substantial when t is in the hundreds or thousands.
