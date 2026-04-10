# III Data Structures

# Study Notes: Part III - Data Structures (Introduction to Algorithms)

## Overview

**Dynamic sets** are central to the field of data structures since they represent collections where elements can be inserted, deleted, and manipulated during the runtime of an algorithm. They are distinct from static mathematical sets as their size and contents change dynamically. This section explores the fundamental data structures and techniques for implementing dynamic sets, focusing on their operations, use cases, and performance. The chapter also emphasizes how the choice of data structure is guided by the specific operations required by the algorithm using the set.

Key dynamic set operations include **queries** (e.g., searching for an element) and **modifications** (e.g., inserting or deleting an element). These operations are analyzed in terms of computational cost, measured as a function of the number of elements in the set. Subsequent chapters delve into specific data structures that support these operations efficiently, including **stacks**, **queues**, **linked lists**, **hashing**, and **trees** (binary search trees, red-black trees, and their augmentations).

---

## Key Concepts

- **Dynamic Set**: A collection of elements where insertions, deletions, and changes can occur during program execution.
- **Dictionary**: A common implementation of a dynamic set that supports insertion, deletion, and membership testing.
- **Key-based Sets**: Dynamic sets where each element is identified by a unique key, allowing operations like finding the minimum, maximum, successor, or predecessor.
- **Operation Types**:
  - **Queries**: Retrieve information about the set without modifying it (e.g., search, minimum, maximum).
  - **Modifications**: Change the state of the set (e.g., insert, delete).

Key definitions for operations:
- **SEARCH(S, k)**: Finds an element with the specified key `k`.
- **INSERT(S, x)**: Adds element `x` to the set `S`.
- **DELETE(S, x)**: Removes a specific element `x` from the set `S`.
- **MINIMUM(S)** and **MAXIMUM(S)**: Define the smallest and largest key in the set, respectively (with respect to a total ordering).
- **SUCCESSOR(S, x)** and **PREDECESSOR(S, x)**: Find the next larger or smaller key for element `x` in a totally ordered set.

---

## Algorithms and Techniques

### Operations on Dynamic Sets

#### Search Operation (SEARCH)
- **Description**: Given a dynamic set `S` and a key `k`, find an element in `S` with a matching key.
- **Input**: Dynamic set `S`, key `k`.
- **Output**: Either an element `x` such that `x.key = k`, or `NIL` if no such element exists.

#### Insert Operation (INSERT)
- **Description**: Add a new element `x` to the dynamic set `S`. This operation assumes that all necessary attributes of `x` are initialized before insertion.
- **Input**: Dynamic set `S`, element `x`.
- **Output**: The modified set `S` containing `x`.

#### Delete Operation (DELETE)
- **Description**: Remove an element `x` from the dynamic set `S`. This operation works using a pointer to `x`, not the key value.
- **Input**: Dynamic set `S`, pointer to element `x`.
- **Output**: The modified set `S` without `x`.

#### Minimum and Maximum (MINIMUM / MAXIMUM)
- **Description**: Find the smallest or largest element in a totally ordered dynamic set.

#### Successor and Predecessor (SUCCESSOR / PREDECESSOR)
- **Description**: For an element `x`, find the next larger key (successor) or next smaller key (predecessor) in a totally ordered dynamic set.

### Data Structure-Specific Algorithms
The efficient implementation of the above operations depends on utilizing appropriate data structures. The following sections from the textbook introduce specific structures:

1. **Chapter 10**: Stacks, Queues, Linked Lists, Rooted Trees.
2. **Chapter 11**: Hash Tables.
3. **Chapter 12**: Binary Search Trees.
4. **Chapter 13**: Red-Black Trees (balance-enforced binary search trees).
5. **Chapter 14**: Augmented Red-Black Trees for advanced functionality.

---

## Complexity Analysis of Basic Operations

The computational complexity of basic dynamic set operations varies based on the data structure used. Below is a summary of the underlying data structures and their complexities for common operations:

| Data Structure             | Search          | Insert          | Delete          | Minimum/Maximum | Successor/Predecessor |
|----------------------------|-----------------|-----------------|-----------------|-----------------|-----------------------|
| Stack                      | O(1)            | O(1)            | O(1)            | N/A             | N/A                   |
| Queue                      | O(1)            | O(1)            | O(1)            | N/A             | N/A                   |
| Singly Linked List         | O(n)            | O(1) (at head)  | O(1) (at head)  | O(n)            | O(n)                  |
| Hash Table (expected case) | O(1)            | O(1)            | O(1)            | N/A             | N/A                   |
| BST (average case)         | O(log n)        | O(log n)        | O(log n)        | O(log n)        | O(log n)              |
| Red-Black Tree (worst case)| O(log n)        | O(log n)        | O(log n)        | O(log n)        | O(log n)              |

---

## Data Structures with Operations and Examples

### Stacks and Queues
- **Key Operations**: PUSH, POP (stack), ENQUEUE, DEQUEUE (queue).
- **Complexities**:
  - All operations execute in `O(1)` time, as they operate only on the ends of the data structure.

### Hash Tables
- **Key Operations**: INSERT, DELETE, SEARCH.
- **Complexities**:
  - **Expected Time**: O(1) for each operation due to uniform hashing.
  - **Worst Case**: O(n) if all elements hash to the same bucket.
- **Concrete Scenario**: A hash table storing a dictionary of words with constant-time lookup for key-based retrieval.

### Binary Search Trees
- **Key Operations**: All fundamental set operations (SEARCH, INSERT, DELETE, MINIMUM, etc.).
- **Complexities**:
  - **Worst Case**: O(n) (e.g., when the tree becomes linear/unbalanced).
  - **Average Case**: O(log n) for balanced trees.
- **Use Case**: Efficient implementations where in-order traversal is required to retrieve elements in sorted order.

### Red-Black Trees
- **Description**: A balanced binary search tree that guarantees logarithmic complexities for all standard operations.
- **Key Operations**: INSERT, DELETE, SEARCH, MINIMUM, etc.
- **Complexities**:
  - **Worst Case**: O(log n) for all operations.
- **Use Case**: Applications requiring worst-case guarantees for dynamic balance (e.g., priority queues, interval trees).

---

## Summary and Significance

Dynamic sets offer a flexible way to manage and manipulate collections of data in programs. The choice of data structure depends on the required operations and performance guarantees. Part III of the book is a foundational section that prepares readers for specialized applications of these structures in algorithms, such as priority queues, balanced search trees, and augmented set functions.
