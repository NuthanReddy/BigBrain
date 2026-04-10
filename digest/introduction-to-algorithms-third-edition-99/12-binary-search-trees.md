# 12 Binary Search Trees

```markdown
# Binary Search Trees (BSTs)

## Overview
Binary Search Trees (BSTs) are hierarchical data structures used for organizing keys to support efficient dynamic set operations. They are widely utilized both as dictionaries (searching for keys) and as priority queues (finding maximum/minimum values). The organization of nodes in a BST ensures sorted ordering of keys, enabling efficient querying of specific values.

Operations such as **SEARCH**, **MINIMUM**, **MAXIMUM**, **PREDECESSOR**, **SUCCESSOR**, **INSERT**, and **DELETE** can typically be performed in time proportional to the height of the tree. The time complexity varies depending on the balance of the tree:
- A balanced BST has a height of \(O(\log n)\), ensuring efficient operations.
- A highly unbalanced BST can degrade to a linear chain, with a height of \(O(n)\), leading to poor performance.

## Key Concepts
- **Binary-Search-Tree Property**: For any node \(x\), all keys in the left subtree of \(x\) are less than or equal to \(x\)'s key, and all keys in the right subtree of \(x\) are greater than or equal to \(x\)'s key.
- **Tree Organization**: BSTs utilize a linked data structure where:
  - Each node contains a key and optional satellite data.
  - A node has pointers to its left child (\(x.left\)), right child (\(x.right\)), and parent (\(x.p\)).
  - The root is the only node in the tree with no parent (\(x.p = NIL\)).
- **Traversal**:
  - **Inorder traversal**: Visits nodes in increasing key order.
  - **Preorder traversal**: Visits the root before its subtrees.
  - **Postorder traversal**: Visits the root after its subtrees.

## Algorithms and Techniques

### Inorder Traversal
**Purpose**: Print all keys in sorted order.
The recursive inorder traversal visits the left subtree, the root, and the right subtree. 

#### Pseudocode:
```
INORDER-TREE-WALK(x)
1   if x != NIL
2       INORDER-TREE-WALK(x.left)
3       print x.key
4       INORDER-TREE-WALK(x.right)
```

#### Time Complexity:
- **Time**: \(O(n)\), since every node is visited exactly once during traversal.
- **Space**: \(O(h)\), where \(h\) is the height of the tree (due to the recursion stack).

#### Example:
For the BST illustrated in Figure 12.1(a):  
Keys: `{6, 5, 2, 5, 7, 8}`  
The **inorder walk** will print: `2, 5, 5, 6, 7, 8`.

### Search in BST
**Purpose**: Find the node containing a particular key.

1. Compare the key \(k\) with the current node \(x.key\).
2. If \(k = x.key\), the node is found.
3. If \(k < x.key\), search the left subtree.
4. If \(k > x.key\), search the right subtree.

#### Pseudocode:
Recursive:
```
TREE-SEARCH(x, k)
1   if x == NIL or k == x.key
2       return x
3   if k < x.key
4       return TREE-SEARCH(x.left, k)
5   else
6       return TREE-SEARCH(x.right, k)
```

Iterative (space-efficient):
```
ITERATIVE-TREE-SEARCH(x, k)
1   while x != NIL and k != x.key
2       if k < x.key
3           x = x.left
4       else
5           x = x.right
6   return x
```

#### Time Complexity:
- **Time**: \(O(h)\), where \(h\) is the height of the tree.
- **Space**: \(O(h)\) for recursive, \(O(1)\) for iterative.

#### Example:
Search for key `13` in the tree Figure 12.2:
- Start at root \(15\).
- Move to \(6 \to 7 \to 13\) (path traced down the tree).

### Finding Minimum and Maximum
**Purpose**:
- **Minimum**: Find the smallest key.
- **Maximum**: Find the largest key.
- Navigate down the leftmost path (for minimum) or the rightmost path (for maximum).

#### Pseudocode:
Minimum:
```
TREE-MINIMUM(x)
1   while x.left != NIL
2       x = x.left
3   return x
```

Maximum:
```
TREE-MAXIMUM(x)
1   while x.right != NIL
2       x = x.right
3   return x
```

#### Time Complexity:
- **Time**: \(O(h)\), height of the tree.
- **Space**: \(O(1)\).

#### Example:
In Figure 12.2:
- Minimum: Follow left pointers \(15 \to 6 \to 2\).
- Maximum: Follow right pointers \(15 \to 17 \to 20\).

### Successor and Predecessor
**Purpose**: Find the next larger (successor) or smaller (predecessor) key of a node.

1. Successor:
   - If the node has a right subtree, its successor is the minimum of the right subtree.
   - Otherwise, follow parent pointers until reaching a node that is a **left** child of its parent.

2. Predecessor:
   - Analogous logic, using the left child and maximum in left subtree.

#### Pseudocode:
```
TREE-SUCCESSOR(x)
1   if x.right != NIL
2       return TREE-MINIMUM(x.right)
3   y = x.p
4   while y != NIL and x == y.right
5       x = y
6       y = y.p
7   return y
```

#### Time Complexity:
- **Time**: \(O(h)\), as we follow a path up or down the tree.
- **Space**: \(O(1)\).

#### Example:
In Figure 12.2:
- Successor of `13`: Follow to its parent `15`.
- Predecessor of `6`: Follow left subtree to maximum \(6.left → 5\).

## Complexity Analysis
| Operation              | Best Case (\(O\)) | Worst Case (\(O\)) |
|------------------------|--------------------|--------------------|
| Search                | \(\log n\)        | \(n\)             |
| Minimum/Maximum       | \(\log n\)        | \(n\)             |
| Successor/Predecessor | \(\log n\)        | \(n\)             |
| Inorder Traversal     | \(n\)             | \(n\)             |

## Theorems

### Theorem 12.1: Time for Inorder Traversal
**Statement**: If \(x\) is the root of an \(n\)-node subtree, `INORDER-TREE-WALK(x)` takes \(O(n)\) time.

**Proof Outline**:
- Traverses all \(n\) nodes exactly once.
- Base case: Time for an empty subtree is constant (\(T(0) = c\)).
- Recursive case: \(T(n) = T(k) + T(n - k - 1) + d\) (left + right + constant work for root).
- Using induction, it can be shown \(T(n) \in O(n)\).

**Significance**:
Provides a formal guarantee of linear runtime for traversal.

## Data Structures: Binary Search Tree
### Operations and their Complexities
| Operation              | Time Complexity   |
|------------------------|--------------------|
| Insert                | \(O(h)\)          |
| Delete                | \(O(h)\)          |
| Search                | \(O(h)\)          |
| Minimum/Maximum       | \(O(h)\)          |
| Successor/Predecessor | \(O(h)\)          |

## Conclusion
Binary Search Trees are a foundational data structure useful in a variety of applications requiring sorted dynamic data. Understanding their operations, traversals, and associated complexities is critical for designing efficient algorithms.
```
