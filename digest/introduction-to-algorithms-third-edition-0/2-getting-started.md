# 2 Getting Started

# Study Notes: Getting Started (Chapter 2 of *Introduction to Algorithms, Third Edition*)

## Overview

Chapter 2 introduces a fundamental framework for the design and analysis of algorithms. The goal of the chapter is to establish an understanding of pseudocode for specifying algorithms, reasoning about their correctness, and analyzing their efficiency. Specifically, this chapter covers two core algorithms for sorting: **Insertion Sort** and **Merge Sort**, along with their analyses and correctness proofs. Concepts such as **loop invariants** are introduced as tools for proving algorithm correctness.

The chapter assumes familiarity with basic programming concepts and introduces pseudocode conventions that will be used throughout the book.

---

## Key Concepts

- **Insertion Sort**: 
  - A simple algorithm suitable for small datasets.
  - Mimics how people sort playing cards, starting with an empty hand and inserting each card in the correct position.
  - Operates in-place on an array using comparisons and shifts.
  
- **Pseudocode Conventions**:
  - Indentation indicates block structure (no explicit `begin-end` blocks).
  - Use of constructs like `for`, `while`, and `if-else`.
  - Supports concise representation through constructs like range (e.g., `A[1:j]`).
  - Local variables are used unless explicitly indicated.

- **Loop Invariants**:
  - Critical for proving algorithm correctness.
  - Require three components:
    1. **Initialization**: Establishing that the invariant holds prior to the first loop iteration.
    2. **Maintenance**: Demonstrating that the invariant holds across iterations.
    3. **Termination**: Showing that when the loop ends, the invariant implies correctness.

- **Divide-and-Conquer**:
  - A fundamental algorithm design paradigm used throughout the book.
  - Recursively breaks the problem into smaller subproblems, solves each subproblem, and combines their solutions.

---

## Algorithms and Techniques

### Insertion Sort

#### How It Works:
- **Insertion Sort** processes an array by dividing it into two regions: **sorted** and **unsorted**.
- Starting with the first element (already sorted), each subsequent element is "inserted" into its correct position within the sorted region.
- This insertion is done by performing comparisons and shifting larger elements within the sorted region.

#### Pseudocode:
```plaintext
INSERTION-SORT(A)
1 for j = 2 to A.length
2     key = A[j]
3     // Insert A[j] into the sorted sequence A[1 : j-1]
4     i = j - 1
5     while i > 0 and A[i] > key
6         A[i + 1] = A[i]
7         i = i - 1
8     A[i + 1] = key
```

#### Example (Step-by-Step):
**Input array:** `[5, 2, 4, 6, 1, 3]`

| Step    | Key | A (Array State)          | Notes                                      |
|---------|-----|--------------------------|--------------------------------------------|
| Initial |  -  | [5, 2, 4, 6, 1, 3]      | The array is unsorted.                     |
| Pass 1  | 2   | [2, 5, 4, 6, 1, 3]      | Compare `2` with `5` and insert before `5`.|
| Pass 2  | 4   | [2, 4, 5, 6, 1, 3]      | Compare `4` with `5`; insert before `5`.   |
| Pass 3  | 6   | [2, 4, 5, 6, 1, 3]      | `6` is already in correct position.        |
| Pass 4  | 1   | [1, 2, 4, 5, 6, 3]      | Compare and insert `1` at the beginning.   |
| Pass 5  | 3   | [1, 2, 3, 4, 5, 6]      | Compare and insert `3` before `4`.         |

**Output array:** `[1, 2, 3, 4, 5, 6]`

#### Complexity:
- **Best-case (when the array is already sorted):**  
  Time: \( O(n) \)  
  Explanation: The algorithm performs one comparison per element; no swaps are needed.

- **Worst-case (when the array is reverse sorted):**  
  Time: \( O(n^2) \)  
  Explanation: Comparisons and shifts occur for each element, resulting in a triangular number of operations (\(1 + 2 + 3 + \dots + (n - 1)\)).

- **Average-case:**  
  Time: \( O(n^2) \)  
  Explanation: On average, half the elements in the sorted region are shifted for every inserted element.

- **Space complexity:**
  Space: \( O(1) \)  
  Explanation: Sorting is done in-place.

---

### Merge Sort

#### How It Works:
- **Merge Sort** applies the **divide-and-conquer** strategy:
  1. Divide the input array into two halves.
  2. Recursively sort each half.
  3. Merge the two sorted halves back together.

- The merging step ensures that the entire array is sorted at each recursive level.

#### Pseudocode:
```plaintext
MERGE-SORT(A, p, r)
1 if p < r
2     q = floor((p + r) / 2)
3     MERGE-SORT(A, p, q)
4     MERGE-SORT(A, q + 1, r)
5     MERGE(A, p, q, r)

MERGE(A, p, q, r)
1 n1 = q - p + 1
2 n2 = r - q
3 let L[1 : n1 + 1] and R[1 : n2 + 1] be new arrays
4 for i = 1 to n1
5     L[i] = A[p + i - 1]
6 for j = 1 to n2
7     R[j] = A[q + j]
8 L[n1 + 1] = ∞
9 R[n2 + 1] = ∞
10 i = 1
11 j = 1
12 for k = p to r
13     if L[i] ≤ R[j]
14         A[k] = L[i]
15         i = i + 1
16     else A[k] = R[j]
17         j = j + 1
```

#### Complexity:
- **Time Complexity:**  
  - Recursive division takes \( \log n \) levels.  
  - Merging at each level involves \( O(n) \) work.  
  Total: \( O(n \log n) \).

- **Space Complexity:**  
  \( O(n) \) due to the creation of temporary arrays during the merge step.

#### Example:
To sort `[5, 2, 9, 1]`:  
- Divide: `[5, 2]` and `[9, 1]`  
- Recursively sort: `[2, 5]` and `[1, 9]`  
- Merge: `[1, 2, 5, 9]`

---

## Complexity Analysis Comparison

| Algorithm       | Time Complexity          | Space Complexity | Best Application                          |
|-----------------|--------------------------|------------------|-------------------------------------------|
| **Insertion Sort** | \( O(n^2) \) (worst)     | \( O(1) \)        | Small datasets or nearly sorted arrays.   |
| **Merge Sort**    | \( O(n \log n) \) (all)  | \( O(n) \)        | Large datasets where additional memory is available. |

---

## Key Takeaways:
- **Insertion Sort** is fast for small datasets and nearly sorted data due to its low overhead and in-place operations.
- **Merge Sort** is an efficient general-purpose algorithm for larger datasets but requires additional memory.
- Understanding loop invariants is crucial for proving the correctness of algorithms (Initialization, Maintenance, and Termination steps must be verified).

Both algorithms are fundamental building blocks that are explored further in more complex scenarios throughout the book.
