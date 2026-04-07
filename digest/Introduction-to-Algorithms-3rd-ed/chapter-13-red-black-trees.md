# Chapter 13: Red-Black Trees

## Overview
Red-black trees are self-balancing binary search trees that guarantee O(lg n) worst-case time for all basic dynamic-set operations. By augmenting each node with a single color bit (red or black) and enforcing five structural properties, red-black trees ensure that no root-to-leaf path is more than twice as long as any other, keeping the tree approximately balanced. This chapter covers the red-black properties, rotations, and the intricate insertion and deletion fixup algorithms that maintain balance.

## Key Concepts

- **Red-black properties**: A red-black tree is a BST satisfying these five invariants:
  1. Every node is either red or black.
  2. The root is black.
  3. Every leaf (NIL) is black. (Leaves are sentinels, not key-bearing nodes.)
  4. If a node is red, both its children are black. (No two consecutive red nodes on any path.)
  5. For each node, all simple paths from that node to descendant leaves contain the same number of black nodes.

- **Sentinel T.nil**: A single sentinel node (colored black) replaces all NIL pointers. Simplifies boundary-condition handling in the code. The root's parent is also T.nil.

- **Black-height (bh(x))**: The number of black nodes on any simple path from node x down to a leaf, not counting x itself. Well-defined by property 5.

- **Lemma 13.1**: A red-black tree with n internal nodes has height at most **2 lg(n + 1)**.
  - Proof sketch: The subtree rooted at any node x contains at least 2^(bh(x)) − 1 internal nodes (by induction). By property 4, at least half the nodes on any root-to-leaf path are black, so bh(root) ≥ h/2. Thus n ≥ 2^(h/2) − 1, giving h ≤ 2 lg(n + 1).

- **Immediate consequence**: SEARCH, MINIMUM, MAXIMUM, SUCCESSOR, and PREDECESSOR all run in O(lg n) time, since they depend only on tree height.

- **Rotations**: Local operations that restructure the tree while preserving the BST property. Two types:
  - **LEFT-ROTATE(T, x)**: Makes x's right child y the new subtree root, with x becoming y's left child and y's former left subtree becoming x's right subtree.
  - **RIGHT-ROTATE(T, y)**: The symmetric inverse.
  - Both run in O(1) time, changing only a constant number of pointers.

## Algorithms and Techniques

### Insertion: RB-INSERT and RB-INSERT-FIXUP

**RB-INSERT(T, z)**: Inserts node z as in a standard BST (using T.nil instead of NIL), then colors z **red** and calls RB-INSERT-FIXUP to restore properties.

Coloring z red preserves property 5 (black-height unchanged) but may violate:
- Property 2 (if z is the root) or
- Property 4 (if z's parent is also red)

**RB-INSERT-FIXUP(T, z)** uses a while loop that iterates while z.p is red. At each iteration, z's grandparent z.p.p exists (since the root is black). There are three cases (and three symmetric cases when z.p is a right child):

- **Case 1: z's uncle y is red**. Recolor z.p and y to black, z.p.p to red, and move z up two levels to z.p.p. This fixes the local violation but may create a new one higher up. The loop continues.

- **Case 2: z's uncle y is black and z is a right child**. Left-rotate on z.p to transform into Case 3. (z moves down, but the key identity is preserved.)

- **Case 3: z's uncle y is black and z is a left child**. Recolor z.p to black and z.p.p to red, then right-rotate on z.p.p. This fixes the violation and the loop terminates.

Finally, line 16 ensures the root is black (restoring property 2 if needed).

**Loop invariant** (three parts):
(a) z is red.
(b) If z.p is the root, z.p is black.
(c) At most one red-black property is violated: either property 2 (z is the root and red) or property 4 (z and z.p are both red).

### Deletion: RB-DELETE and RB-DELETE-FIXUP

**RB-DELETE(T, z)**: Based on TREE-DELETE but tracks:
- Node **y**: the node removed or moved in the tree (y = z if z has < 2 children; y = z's successor otherwise).
- **y-original-color**: y's color before modification.
- Node **x**: the node that moves into y's original position.

If y-original-color was BLACK, red-black properties may be violated (property 5 in particular), so RB-DELETE-FIXUP(T, x) is called.

**RB-DELETE-FIXUP(T, x)**: The key idea is that x carries an "extra black"—it is conceptually "doubly black" or "red-and-black." The while loop moves this extra black up the tree until:
1. x is red-and-black → color it black (line 23);
2. x is the root → remove the extra black; or
3. Rotations and recolorings resolve the issue.

**Four cases** (with symmetric cases when x is a right child):
- **Case 1: x's sibling w is red**. Switch colors of w and x.p, left-rotate on x.p. Converts to Case 2, 3, or 4 (w is now black).
- **Case 2: w is black, both w's children are black**. Remove one black from both x and w (w becomes red), push extra black up to x.p. Loop repeats with x = x.p. If entered through Case 1, x.p is red, so the loop terminates.
- **Case 3: w is black, w's left child is red, w's right child is black**. Switch colors of w and w.left, right-rotate on w. Converts to Case 4.
- **Case 4: w is black, w's right child is red**. Recolor w with x.p's color, color x.p black, color w.right black, left-rotate on x.p. Removes the extra black from x. Set x = T.root to terminate the loop.

### Helper: RB-TRANSPLANT
Replaces subtree rooted at u with subtree rooted at v. Differs from TRANSPLANT by using T.nil instead of NIL and unconditionally assigning v.p = u.p (even when v = T.nil).

## Complexity Analysis

| Operation | Time Complexity | Rotations |
|---|---|---|
| SEARCH, MIN, MAX, SUCCESSOR, PREDECESSOR | O(lg n) | 0 |
| RB-INSERT (total) | O(lg n) | ≤ 2 |
| RB-DELETE (total) | O(lg n) | ≤ 3 |

- **Height bound**: h ≤ 2 lg(n + 1) (Lemma 13.1). All operations are O(h) = O(lg n).
- **Insertion**: Phase 1 (standard BST insert) is O(lg n). Phase 2 (fixup) iterates O(lg n) times in Case 1 (moving z up two levels) but performs at most 2 rotations total before terminating via Case 2/3.
- **Deletion**: Phase 1 (removal/transplant) is O(lg n). Phase 2 (fixup) iterates O(lg n) times in Case 2 (moving x up one level) and performs at most 3 rotations total. Cases 1, 3, 4 each do a constant amount of work and lead to termination.
- **Space**: O(n) for n nodes (1 extra bit per node for color, plus the single sentinel T.nil).

## Key Takeaways

- **Red-black trees guarantee O(lg n) worst-case performance** for all basic dynamic-set operations, unlike plain BSTs whose worst case is O(n). The height bound of 2 lg(n + 1) ensures this.
- **The five red-black properties** are carefully chosen to keep the tree balanced: property 5 (equal black-height) is the core balancing constraint, while property 4 (no consecutive reds) limits how much "extra" height red nodes can add.
- **Rotations are the key structural tool**: they rearrange the tree locally in O(1) time while preserving the BST property. Insertion uses at most 2 rotations; deletion uses at most 3.
- **Insertion fixup is driven by the uncle's color**: red uncle → recolor and propagate upward (Case 1); black uncle → 1–2 rotations and terminate (Cases 2–3).
- **Deletion fixup is driven by the sibling's and its children's colors**: the "extra black" concept elegantly tracks the property-5 deficit until it can be resolved by recoloring (Case 2) or rotations (Cases 1, 3, 4).
