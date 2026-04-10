# I Foundations

# Study Notes: Part I - Foundations (Introduction to Algorithms, Third Edition)

## Overview
Part I of *Introduction to Algorithms, Third Edition* introduces the fundamental concepts that underpin the design and analysis of algorithms. It covers basic definitions, techniques, and tools that are critical for understanding algorithms, their performance, and their correctness. Topics include sorting algorithms, divide-and-conquer, asymptotic notation, recurrences, and probabilistic analysis. These concepts form the foundation for more complex algorithms covered in later sections of the book.

---

## Key Concepts

- **What is an Algorithm?**
  - A step-by-step computational procedure that takes input and produces output.
  - Algorithms solve specific computational problems and are central to computer science.

- **Algorithms as Technology:**
  - Algorithms are as important as hardware or software systems.
  - Efficient algorithms save resources, enabling practical solutions otherwise infeasible with brute force.

- **Sorting Algorithms:**
  - Sorting is a foundational problem in computer science.
  - Two major techniques:
    - **Incremental approach** (Insertion Sort).
    - **Divide-and-conquer approach** (Merge Sort).
  - Sorting serves as an entry point for analyzing algorithm efficiency.

- **Asymptotic Notation:**
  - Used to formally describe the performance of algorithms as input size grows.
  - Big-O, Omega, and Theta notations are introduced to bound running times from above, below, or both.

- **Divide-and-Conquer:**
  - A common algorithm design paradigm.
  - Break a problem into smaller subproblems, solve them recursively, and combine their solutions.
  - Illustrated using examples like **Merge Sort** and **Strassen’s Matrix Multiplication**.

- **Recurrences:**
  - Mathematical expressions that describe the running time of recursive algorithms.
  - Solved via techniques like the **Master Theorem**, substitution, and recursion trees.

- **Probabilistic Analysis:**
  - Analyzing the expected running time or performance of an algorithm when input or algorithm behavior involves randomness.

- **Randomized Algorithms:**
  - Algorithms that make random choices during execution.
  - Useful for reducing worst-case performance or achieving probabilistic guarantees.

---

## Algorithms and Techniques

### Insertion Sort
#### How It Works
- Incrementally builds a sorted subsection of the array by repeatedly inserting new elements into their correct positions.
- Uses a comparison-based approach.

#### Pseudocode Sketch
```text
for i = 2 to n:
    key = A[i]
    j = i - 1
    while j > 0 and A[j] > key:
        A[j + 1] = A[j]
        j = j - 1
    A[j + 1] = key
```

#### Time/Space Complexity
- Best Case: \( O(n) \) (already sorted input).
- Average Case: \( O(n^2) \).
- Worst Case: \( O(n^2) \) (reverse-sorted input).
- Space Complexity: \( O(1) \) (in-place sorting).

---

### Merge Sort
#### How It Works
- Divides the array into two halves, recursively sorts each half, and then merges them into a fully sorted array.
- Uses the divide-and-conquer paradigm.

#### Pseudocode Sketch
```text
MERGE-SORT(A, p, r):
    if p < r:
        q = floor((p + r) / 2)
        MERGE-SORT(A, p, q)
        MERGE-SORT(A, q + 1, r)
        MERGE(A, p, q, r)
```

#### Time/Space Complexity
- Best Case: \( O(n \log n) \).
- Average Case: \( O(n \log n) \).
- Worst Case: \( O(n \log n) \).
- Space Complexity: \( O(n) \) (extra space for merging).

---

### Strassen's Matrix Multiplication
#### How It Works
- Multiplies two \( n \times n \) matrices faster than the traditional \( O(n^3) \) algorithm.
- Uses divide-and-conquer with fewer recursive multiplications.

#### Significance
- Reduces the complexity to \( O(n^{\log_2 7}) \), approximately \( O(n^{2.81}) \).

---

### Randomized Algorithms
#### Example: Randomized QuickSort
- Randomly selects a pivot element to improve expected performance.
- Prevents worst-case scenarios caused by poor pivot choices in standard QuickSort.

#### Key Idea
- Randomized approach ensures balanced partitioning (on average).

#### Example Application
Used in cases where average performance is preferred over deterministic guarantees.

---

## Complexity Analysis Table

| Algorithm                  | Best Case   | Average Case     | Worst Case      | Space Complexity |
|----------------------------|-------------|------------------|-----------------|------------------|
| **Insertion Sort**         | \( O(n) \)  | \( O(n^2) \)     | \( O(n^2) \)    | \( O(1) \)       |
| **Merge Sort**             | \( O(n \log n) \) | \( O(n \log n) \) | \( O(n \log n) \) | \( O(n) \)       |
| **Strassen's Multiplication** | -           | -                | \( O(n^{2.81}) \) | \( O(n^2) \)     |

---

## Theorems

### **Master Theorem for Divide-and-Conquer**
#### Formal Statement
For a recurrence of the form:
\[
T(n) = aT\left(\frac{n}{b}\right) + f(n)
\]
where:
- \( a \geq 1 \),
- \( b > 1 \), and
- \( f(n) \) is asymptotically positive,

The solution to the recurrence is:
1. If \( f(n) = O(n^{c}) \) and \( c < \log_b a \), then \( T(n) = \Theta(n^{\log_b a}) \).
2. If \( f(n) = \Theta(n^{c}) \) and \( c = \log_b a \), then \( T(n) = \Theta(n^{c} \log n) \).
3. If \( f(n) = \Omega(n^c) \) and \( c > \log_b a \), and \( af(n/b) \leq kf(n) \) for \( k < 1 \), then \( T(n) = \Theta(f(n)) \).

#### Significance
- Provides a shortcut to solve many recurrences arising in divide-and-conquer algorithms.

---

## Data Structures
No new data structures are introduced explicitly in this section. Sorting algorithms discussed operate directly on arrays.

---

## Concrete Examples

### Example of Insertion Sort:
Input array: [5, 2, 4, 6, 1, 3]

#### Iteration-by-Iteration Process:
1. Initially [5] is sorted.
2. Insert 2: [2, 5]
3. Insert 4: [2, 4, 5]
4. Insert 6: [2, 4, 5, 6]
5. Insert 1: [1, 2, 4, 5, 6]
6. Insert 3: [1, 2, 3, 4, 5, 6]

### Example of Merge Sort
Input array: [5, 2, 4, 6, 1, 3]

#### Steps:
1. Divide: [5, 2, 4] and [6, 1, 3].
2. Recursively sort: [2, 4, 5] and [1, 3, 6].
3. Merge: [1, 2, 3, 4, 5, 6].

---

## Summary
Part I of *Introduction to Algorithms* sets the stage for designing and analyzing algorithms with foundational concepts like sorting, asymptotic analysis, divide-and-conquer, recurrences, and probabilistic methods. It emphasizes understanding both the theoretical and practical aspects of algorithm performance.
