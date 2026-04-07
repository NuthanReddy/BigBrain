# Chapter 12: Binary Search Trees

## Overview
This chapter introduces binary search trees (BSTs), a fundamental data structure that supports all major dynamic-set operations—SEARCH, MINIMUM, MAXIMUM, PREDECESSOR, SUCCESSOR, INSERT, and DELETE—in time proportional to the tree's height. BSTs serve as both dictionaries and priority queues. The chapter covers the BST property, tree traversals, querying, insertion, deletion, and proves that a randomly built BST has expected height O(lg n).

## Key Concepts

- **Binary search tree property**: For any node x, all keys in x's left subtree are ≤ x.key, and all keys in x's right subtree are ≥ x.key. This ordering invariant enables efficient searching by eliminating half the remaining candidates at each step.
- **Node structure**: Each node stores `key`, `left`, `right`, and `p` (parent) pointers, plus optional satellite data. `T.root` points to the root; NIL represents absent children or parent.
- **Height**: The critical parameter. Operations run in O(h) where h is the tree height. For n nodes, h ranges from ⌊lg n⌋ (balanced) to n − 1 (degenerate chain).
- **Tree walks**: Recursive traversals that visit every node.
  - **Inorder walk**: Visit left subtree, then root, then right subtree. Produces keys in sorted order.
  - **Preorder walk**: Visit root before subtrees.
  - **Postorder walk**: Visit root after subtrees.
- **Randomly built BST**: A BST formed by inserting n keys in a uniformly random order (each of the n! permutations equally likely). Its expected height is O(lg n) (Theorem 12.4).

## Algorithms and Techniques

### Inorder Tree Walk
**INORDER-TREE-WALK(x)**: If x ≠ NIL, recursively walk x.left, print x.key, then recursively walk x.right. Produces sorted output.
- **Theorem 12.1**: Takes Θ(n) time on an n-node subtree (each node visited exactly once; proof by substitution with T(n) ≤ (c+d)n + c).

### Searching
- **TREE-SEARCH(x, k)**: Recursive—compare k with x.key; go left if k < x.key, right if k > x.key, return x if equal or NIL if absent.
- **ITERATIVE-TREE-SEARCH(x, k)**: Same logic in a while loop, typically more efficient on real hardware.
- Both run in O(h) time, following a single root-to-leaf path.

### Minimum and Maximum
- **TREE-MINIMUM(x)**: Follow left pointers from x until reaching NIL. Returns the leftmost node.
- **TREE-MAXIMUM(x)**: Follow right pointers from x until reaching NIL. Returns the rightmost node.
- Both run in O(h) time.

### Successor and Predecessor
- **TREE-SUCCESSOR(x)**: If x has a right subtree, return TREE-MINIMUM(x.right). Otherwise, walk up via parent pointers until finding a node that is the left child of its parent; return that parent. The successor is the node with the smallest key greater than x.key.
- **TREE-PREDECESSOR(x)**: Symmetric to TREE-SUCCESSOR.
- Both run in O(h) time.

**Theorem 12.2**: SEARCH, MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR each run in O(h) time on a BST of height h.

### Insertion
**TREE-INSERT(T, z)**: Traces a path from the root downward, maintaining a trailing pointer y. Compares z.key with each node to decide left/right, until reaching NIL. Then sets z's parent to y and inserts z as y's left or right child.
- Runs in O(h) time.

### Deletion
Deletion has three cases:
1. **z has no children**: Simply remove z (replace with NIL).
2. **z has one child**: Replace z with its single child (elevate the child).
3. **z has two children**: Find z's successor y (the minimum of z's right subtree, which has no left child). Splice y out and have it replace z.

The helper **TRANSPLANT(T, u, v)** replaces subtree rooted at u with subtree rooted at v by updating u's parent's pointer.

**TREE-DELETE(T, z)** handles four sub-cases:
- z has no left child → replace z with z.right
- z has no right child → replace z with z.left
- z has two children and y = z's successor is z's right child → replace z by y directly
- z has two children and y ≠ z.right → first replace y by y.right, then replace z by y

**Theorem 12.3**: INSERT and DELETE each run in O(h) time on a BST of height h.

### Randomly Built BSTs (Section 12.4)
**Theorem 12.4**: The expected height of a randomly built BST on n distinct keys is O(lg n).

**Proof technique**: Define the exponential height Y_n = 2^(X_n) where X_n is the actual height. When the root has rank i, Y_n = 2·max(Y_{i−1}, Y_{n−i}). Using indicator random variables and independence:
- E[Y_n] ≤ (4/n) · Σ E[Y_i] for i = 0 to n−1
- By substitution, E[Y_n] ≤ (1/4)·C(n+3, 3)
- Since 2^(E[X_n]) ≤ E[Y_n] (Jensen's inequality, as 2^x is convex), taking logarithms yields E[X_n] = O(lg n).

The connection to **Randomized Quicksort** is deep: the comparisons made during BST construction from a random permutation are exactly the same comparisons made by randomized quicksort (Problem 12-3).

## Complexity Analysis

| Operation | Time Complexity |
|---|---|
| INORDER-TREE-WALK | Θ(n) |
| TREE-SEARCH | O(h) |
| TREE-MINIMUM / TREE-MAXIMUM | O(h) |
| TREE-SUCCESSOR / TREE-PREDECESSOR | O(h) |
| TREE-INSERT | O(h) |
| TREE-DELETE | O(h) |

Where h is the tree height:
- **Best case**: h = Θ(lg n) for a balanced tree → all operations O(lg n)
- **Worst case**: h = n − 1 for a degenerate chain → all operations O(n)
- **Average case** (random insertion): E[h] = O(lg n) (Theorem 12.4)

**Space**: O(n) for n nodes.

**Number of distinct BSTs on n keys**: The nth Catalan number, C(2n, n)/(n+1) = Θ(4ⁿ / n^(3/2)) (Problem 12-4).

## Key Takeaways

- **The BST property enables efficient sorted-order operations**: inorder traversal produces sorted output in Θ(n) time, and all point queries (search, min, max, successor, predecessor) run in O(h).
- **All basic operations run in O(h) time**, so the tree's height is the critical performance factor. An unbalanced BST degrades to a linked list with O(n) operations.
- **Randomly built BSTs have O(lg n) expected height**, analogous to how randomized quicksort achieves O(n lg n) expected time. However, interleaved insertions and deletions can degrade height, motivating balanced BST variants.
- **Deletion is the trickiest operation**, requiring careful handling of the two-children case via the successor node and the TRANSPLANT helper.
- **Balanced BST variants** (Chapter 13: red-black trees, Chapter 18: B-trees) guarantee O(lg n) worst-case height, ensuring O(lg n) time for all operations regardless of input order.
