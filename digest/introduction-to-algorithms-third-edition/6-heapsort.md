# 6 Heapsort

# Heapsort Study Notes

Heapsort is an efficient comparative sorting algorithm that leverages the properties of the **heap data structure** to perform in-place sorting with a time complexity of \(O(n \lg n)\). This algorithm combines the advantages of **merge sort** (efficient \(O(n \lg n)\) running time) and **insertion sort** (in-place sorting) while introducing the **heap** as an auxiliary data structure. This study note summarizes the key concepts, heap operations, critical algorithms used in Heapsort, and its overall complexity.

---

## Overview
Heapsort is a comparison-based sorting algorithm that efficiently organizes and sorts an array by converting it into a **binary heap** (a nearly complete binary tree data structure). Key features include:
- **Time Complexity**: \(O(n \lg n)\) in all cases (best, worst, and average).
- **In-Place Nature**: Requires constant \(O(1)\) additional space beyond the input array.
- **Binary Heap**: The underlying data structure, where elements are organized to satisfy **max-heap** or **min-heap** properties.

---

## Key Concepts

1. **Heap Data Structure**:
   - A binary tree with elements organized in a way that satisfies the **Heap Property**:
     - **Max-Heap**: The key at each node is greater than or equal to the keys of its children.
     - **Min-Heap**: The key at each node is less than or equal to the keys of its children.
   - In Heapsort, a **max-heap** is used.

2. **Array Representation of a Heap**:
   - A heap can be stored as an array:
     - The element at index \(i\) corresponds to:
       - **Parent**: \(\text{index} = \lfloor i/2 \rfloor\)
       - **Left Child**: \(\text{index} = 2i\)
       - **Right Child**: \(\text{index} = 2i + 1\)
   - This representation eliminates the need for explicit pointers, making traversal and manipulation efficient.

3. **Height of a Heap**:
   - For a heap storing \(n\) elements, the height is \(O(\lg n)\) since it is based on a complete binary tree.

4. **Heap Operations**:
   - Operations such as **inserting**, **extracting maximum/minimum**, and **adjusting the heap** (\(MAX\_HEAPIFY\)) are central to Heapsort and have a time complexity of \(O(\lg n)\).

5. **Heapsort Algorithm**:
   - Uses two main steps for sorting:
     1. **Building a Max-Heap**: Rearranges an unsorted array into a max-heap.
     2. **Sorting Phase**: Repeatedly extracts the maximum element and restores the heap property for the remaining elements.

---

## Algorithms and Techniques

### MAX-HEAPIFY
#### Description
The **MAX-HEAPIFY** procedure ensures that the **max-heap property** is maintained at a given node index \(i\) in the array. It assumes that the subtrees rooted at the left and right children of \(i\) are valid max-heaps, but the node at \(i\) may violate the heap property.

#### Pseudocode
```plaintext
MAX-HEAPIFY(A, i)
1   l = LEFT(i)
2   r = RIGHT(i)
3   if l ≤ A.heap-size and A[l] > A[i]
4       largest = l
5   else
6       largest = i
7   if r ≤ A.heap-size and A[r] > A[largest]
8       largest = r
9   if largest ≠ i
10      exchange A[i] with A[largest]
11      MAX-HEAPIFY(A, largest)
```

#### Example
For array \(A = [16, 4, 10, 14, 7, 9, 3, 2, 8, 1]\), calling `MAX-HEAPIFY(A, 2)` results in the following changes:
1. Node 2 violates the property (\(4 < 14\)): swap node 2 (\(4\)) with node 4 (\(14\)).
2. Recursively call on the subtree rooted at node 4 to fix further violations.

#### Complexity
- Time: \(O(\lg n)\), proportional to the height of the heap.
- Space: Recursive call stack uses \(O(\lg n)\) space; iterative implementations can reduce it to constant.

---

### BUILD-MAX-HEAP
#### Description
Transforms an unordered array into a valid max-heap. It works by calling `MAX-HEAPIFY` on all non-leaf nodes in reverse level order, starting with the last internal node.

#### Pseudocode
```plaintext
BUILD-MAX-HEAP(A)
1   A.heap-size = A.length
2   for i = ⌊A.length / 2⌋ downto 1
3       MAX-HEAPIFY(A, i)
```

#### Example
For array \(A = [4, 10, 3, 5, 1]\):
1. Start with \(i = 2\): Fix the subtree rooted at index 2.
2. Move to \(i = 1\): Fix the subtree rooted at index 1.

Result: \(A = [10, 5, 3, 4, 1]\).

#### Complexity
- Time: \(O(n)\). Detailed analysis reveals that most heap adjustments occur on smaller trees.

---

### HEAPSORT
#### Description
Sorts an array by:
1. Building a max-heap from the input array.
2. Iteratively extracting the root (maximum value), placing it at the end, and reconstructing the heap for the remaining unsorted portion.

#### Pseudocode
```plaintext
HEAPSORT(A)
1   BUILD-MAX-HEAP(A)
2   for i = A.length downto 2
3       exchange A[1] with A[i]
4       A.heap-size = A.heap-size - 1
5       MAX-HEAPIFY(A, 1)
```

#### Example
Input: \(A = [4, 10, 3, 5, 1]\)
1. Convert to max-heap: \(A = [10, 5, 3, 4, 1]\).
2. Iteratively move the largest element (root) to the end and shrink the heap.

Output (sorted array): \(A = [1, 3, 4, 5, 10]\).

#### Complexity
- Time: \(O(n \lg n)\) due to \(n\) calls to `MAX-HEAPIFY`, each taking \(O(\lg n)\).
- Space: \(O(1)\) (in-place sorting).

---

## Complexity Analysis
| Algorithm       | Time Complexity | Space Complexity | Notes                         |
|------------------|----------------|-------------------|-------------------------------|
| MAX-HEAPIFY     | \(O(\lg n)\)   | \(O(1)\)          | Restores heap property.       |
| BUILD-MAX-HEAP  | \(O(n)\)       | \(O(1)\)          | Converts array to max-heap.   |
| HEAPSORT        | \(O(n \lg n)\) | \(O(1)\)          | In-place sorting algorithm.   |

---

## Data Structure: Heap

The **heap** is a complete binary tree that satisfies the heap property. Using an array-based implementation:

- **Basic Operations**:
  - **Insert**: \(O(\lg n)\)
  - **Extract-Max/Min**: \(O(\lg n)\)
  - **Increase/Decrease Key**: \(O(\lg n)\)
  - **Build-Heap**: \(O(n)\)

- **Applications**:
  - Sorting (Heapsort)
  - Priority Queues
  - Median Finding

---

## Theorems and Properties

### 1. **Heap Height**:
An \(n\)-element heap has a height of \(\lfloor \lg n \rfloor\).

#### Proof:
Since the heap is a complete binary tree, the height corresponds to the longest path from the root to a leaf and is proportional to \(\lg n\).

---

Heapsort provides an elegant example of combining data structure design (heaps) with efficient algorithmic techniques for sorting. With its \(O(n \lg n)\) complexity and in-place behavior, it remains important in both theoretical computer science and practical applications.
