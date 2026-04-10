# II Sorting and Order Statistics

# Study Notes: Sorting and Order Statistics

These notes provide a detailed review of **Part II: Sorting and Order Statistics** from *Introduction to Algorithms, Third Edition*. This section introduces fundamental sorting algorithms and explores techniques for finding order statistics such as the ith smallest element.  

---

## Overview

Sorting is a fundamental problem in computer science with broad applications and significance. This section examines algorithms for sorting a sequence of numbers or records that include associated satellite data. Sorting not only facilitates many real-world tasks (e.g., preparing customer statements or layering graphical objects) but also uses foundational algorithmic design and analysis techniques. Additionally, this section discusses **order statistics**, which involves finding specific elements based on their rank (e.g., the smallest or kth smallest). Several algorithms with varying time complexities and data assumptions are explored.  

---

## Key Concepts

- **Sorting Problem**: Rearrange a sequence \( a_1, a_2, \dots, a_n \) into a permutation \( a'_1, a'_2, \dots, a'_n \) such that \( a'_1 \leq a'_2 \leq \dots \leq a'_n \).  
  - Sorting can involve keys with associated satellite data that must move in sync with the keys.  
  - In practice, sorting numbers is often analogous to sorting pointers or records for large datasets.

- **Order Statistics**: The ith smallest element in a dataset is called the ith order statistic. Applications include finding medians, minimums, maximums, and other ranked elements.  
  - Sophisticated algorithms (e.g., randomized and deterministic approaches) can achieve linear time complexity for this task.

- **Comparison Sorts**: Sorting methods that derive element order strictly by comparing keys. These algorithms have a theoretical lower bound of \( \Omega(n \log n) \) for worst-case performance.

- **Non-Comparison Sorts**: Methods like counting sort, radix sort, and bucket sort achieve better-than-\( \Omega(n \log n) \) time by leveraging additional properties of the keys (e.g., bounds on their range or uniform distributions).

- **Key Algorithms**:  
  - **Insertion Sort**: Simple, fast for small inputs; \( O(n^2) \) worst-case.  
  - **Merge Sort**: A divide-and-conquer algorithm; \( O(n \log n) \).  
  - **Heapsort**: Combines heap data structures with sorting; \( O(n \log n) \).  
  - **Quicksort**: Highly efficient on average but can degrade to \( O(n^2) \) in the worst case.  
  - **Counting Sort**: Linear sort when input values have a finite range \( [0, k] \).  
  - **Radix Sort**: Extension of counting sort for multi-digit numbers, achieving linear time when digit values are bounded.  
  - **Bucket Sort**: Probabilistically linear when inputs are uniformly distributed.

---

## Algorithms and Techniques

### Insertion Sort
- **Description**: Iteratively inserts an element into its correct position in an already sorted portion of the array.
- **Pseudocode Sketch**:
    ```plaintext
    INSERTION-SORT(A):
    for j = 2 to A.length:
        key = A[j]
        i = j - 1
        while i > 0 and A[i] > key:
            A[i + 1] = A[i]
            i = i - 1
        A[i + 1] = key
    ```
- **Time Complexity**:  
  - Worst-case: \( O(n^2) \) (when array is sorted in reverse order).  
  - Best-case: \( O(n) \) (when array is already sorted).  
- **Space Complexity**: \( O(1) \), **in-place sorting**.  

---

### Merge Sort
- **Description**: A divide-and-conquer algorithm. The array is recursively divided into halves, sorted individually, and then merged.
- **Pseudocode Sketch**:
    ```plaintext
    MERGE-SORT(A, p, r):
        if p < r:
            q = floor((p + r) / 2)
            MERGE-SORT(A, p, q)
            MERGE-SORT(A, q + 1, r)
            MERGE(A, p, q, r)
    ```
- **Time Complexity**:  
  - Worst-case: \( O(n \log n) \).  
  - Best-case: \( O(n \log n) \) (always splits equally).  
- **Space Complexity**: \( O(n) \) (due to additional space for merging).  

---

### Heapsort
- **Description**: Utilizes a **heap data structure** to sort an array. The heap allows efficient extraction of maximum or minimum elements.
- **Process**: Build a max-heap from the input array, then repeatedly extract the maximum (or root) and rebuild the heap on the remaining elements.
- **Key Operations**:
  - Heapify: \( O(\log n) \), Build heap: \( O(n) \).  
- **Time Complexity**:  
  - Worst-case: \( O(n \log n) \).  
- **Space Complexity**: \( O(1) \), **in-place sorting**.  

---

### Quicksort
- **Description**: Efficient divide-and-conquer algorithm. Selects a "pivot" element, partitions elements into left (< pivot) and right (>= pivot), and recursively sorts partitions.
- **Pseudocode Sketch**:
    ```plaintext
    QUICKSORT(A, p, r):
        if p < r:
            q = PARTITION(A, p, r)
            QUICKSORT(A, p, q - 1)
            QUICKSORT(A, q + 1, r)
    ```
- **Time Complexity**:
  - Worst-case: \( O(n^2) \) (e.g., when pivot splits unequally).  
  - Average-case: \( O(n \log n) \).  
- **Space Complexity**: Depends on recursion depth.  

---

### Counting Sort
- **Description**: Non-comparison sort where values are used as indices in a counting array.
- **Assumptions**: Keys are integers in \( [0, k] \).
- **Time Complexity**: \( O(n + k) \).  
- **Space Complexity**: \( O(n + k) \).  

---

### Radix Sort
- **Description**: Uses counting sort as a subroutine to sort numbers digit by digit, starting from the least significant digit.
- **Time Complexity**: \( O(d \cdot (n + k)) \), where \( d \) is the number of digits and \( k \) is the range of a single digit.  

---

### Bucket Sort
- **Description**: Distributes input uniformly into buckets (e.g., based on intervals) and sorts each bucket individually. Works best when data is uniformly distributed.
- **Time Complexity**: Average: \( O(n) \), Worst: \( O(n^2) \).  

---

## Complexity Analysis (Table)

| **Algorithm**     | **Worst-Case Time** | **Best/Average Time** | **Space Complexity** | **Comparison-Based** |
|--------------------|---------------------|------------------------|-----------------------|-----------------------|
| Insertion Sort     | \( O(n^2) \)       | \( O(n) \)            | \( O(1) \)           | Yes                   |
| Merge Sort         | \( O(n \log n) \)  | \( O(n \log n) \)     | \( O(n) \)           | Yes                   |
| Heapsort           | \( O(n \log n) \)  | -                    | \( O(1) \)           | Yes                   |
| Quicksort          | \( O(n^2) \)       | \( O(n \log n) \)     | \( O(\log n) \)      | Yes                   |
| Counting Sort      | \( O(n + k) \)     | \( O(n + k) \)        | \( O(n + k) \)       | No                    |
| Radix Sort         | \( O(d(n + k)) \)  | \( O(d(n + k)) \)     | \( O(n + k) \)       | No                    |
| Bucket Sort        | \( O(n^2) \)       | \( O(n) \)           | \( O(n) \)           | No                    |  

---

## Key Theorems

### Theorem: Lower Bound for Comparison Sorts
- **Statement**: Any comparison-based sorting algorithm has a worst-case lower bound of \( \Omega(n \log n) \).  
- **Significance**: Demonstrates that algorithms like Merge Sort and Heapsort are asymptotically optimal among comparison sorts.

---

## Order Statistics
- **Problem**: Finding the ith smallest element in a set of \( n \) values.
- **Key Approaches**:
  - **Sorting**: Sort the array and directly index. Complexity: \( O(n \log n) \).  
  - **Linear-Time Selection**: Algorithms like Randomized SELECT or Deterministic Median-of-Medians achieve \( O(n) \).

Example Applications: Median finding in linear time for robust statistical analysis!

--- 

These study notes serve as a detailed, comprehensive reference for Part II: Sorting and Order Statistics.
