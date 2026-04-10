# I Foundations

# Study Notes: Foundations (Part I)

## Overview

The "Foundations" section of "Introduction to Algorithms, Third Edition" serves as an introductory part to algorithm design and analysis. It provides the necessary background knowledge and strategies for building and evaluating algorithms, as well as the mathematical tools required for analyzing their efficiency. This section lays a crucial groundwork for studying advanced topics in later chapters. It starts with the definition of algorithms and their role in computing, dives into specific fundamental algorithms like sorting, introduces asymptotic notation to express algorithm growth rates, explains recursive divide-and-conquer techniques, and concludes with probabilistic analysis and randomized algorithms.

This part teaches concepts core to computer science, emphasizing both clarity in algorithm design and rigor in performance analysis.

---

## Key Concepts

- **Definition of an Algorithm:**
  - A well-defined computational procedure that takes inputs and produces outputs after a series of steps.
  - Algorithms solve specific problems and play a pivotal role in computing technologies.

- **Algorithm as Technology:**
  - Algorithms are foundational to modern computing systems, influencing hardware development, object-oriented systems, networks, and GUIs.

- **Sorting Algorithms:**
  - Sorting is a fundamental problem in computer science.
  - Two main approaches are discussed:
    - **Insertion sort**: Incremental approach.
    - **Merge sort**: Divide-and-conquer technique.

- **Asymptotic Notation:**
  - Used to describe the growth of an algorithm's running time as input size increases.
  - Includes notations like Big-O, Omega, and Theta for bounding growth from above, below, or tightly around.

- **Divide-and-Conquer:**
  - A design technique that breaks a problem into smaller subproblems, solves them recursively, and combines their results.
  - Covered more thoroughly in later chapters, with specific methods such as Strassen's algorithm for matrix multiplication.

- **Recurrence Relations:**
  - Equations that describe the running times of recursive algorithms.
  - Solving recurrences helps predict the performance of divide-and-conquer algorithms.

- **Probabilistic Analysis:**
  - Averages the running time over all inputs based on an assumed probability distribution.
  - Often involves randomized algorithms that use random number generators to produce results.

- **Randomized Algorithms:**
  - Algorithms influenced by random choices made during execution.
  - Useful for ensuring no input consistently produces poor performance and for probabilistic error bounds.

---

## Algorithms and Techniques

### Insertion Sort

#### How It Works
- Incremental sorting method: builds the sorted array one element at a time.
- For each element in the array, insertion sort finds the correct position in the sorted portion and inserts it, shifting other elements if necessary.

#### Pseudocode Sketch
```plaintext
INSERTION-SORT(A)
1. for j = 2 to A.length
2.     key = A[j]
3.     Insert A[j] into the sorted sequence A[1..j-1].
4.     i = j - 1
5.     while i > 0 and A[i] > key
6.         A[i+1] = A[i]
7.         i = i - 1
8.     A[i+1] = key
```

#### Time Complexity
- Best case (already sorted): **O(n)**.
- Worst case (reverse sorted): **O(n²)**.
- Average case: **O(n²)**.

#### Space Complexity
- **O(1)** (in-place sorting).

---

### Merge Sort

#### How It Works
- Recursive divide-and-conquer algorithm:
  1. Divide the array into two halves.
  2. Recursively sort both halves.
  3. Merge the two sorted halves into a single sorted array.

#### Pseudocode Sketch
```plaintext
MERGE-SORT(A, p, r)
1. if p < r
2.     q = ⌊(p + r) / 2⌋
3.     MERGE-SORT(A, p, q)
4.     MERGE-SORT(A, q + 1, r)
5.     MERGE(A, p, q, r)

MERGE(A, p, q, r)
1. Create two temporary arrays for left and right halves.
2. Compare elements and merge them into A[p..r] in sorted order.
```

#### Time Complexity
- Best/Average/Worst case: **O(n log n)** due to logarithmic recursion depth with linear merging at each level.

#### Space Complexity
- **O(n)** (additional memory for merging).

---

### Strassen’s Algorithm for Matrix Multiplication

#### How It Works
- A divide-and-conquer algorithm for multiplying two \(n \times n\) matrices.
- Reduces the number of recursive multiplications from 8 (standard approach) to 7, improving asymptotic complexity.

#### Time Complexity
- **O(n^{\log_2 7}) \approx O(n^{2.81})**.

---

### Master Theorem (for Divide-and-Conquer Recurrences)

#### Formal Statement
If a recurrence relation is of the form:
\[
T(n) = aT\left(\frac{n}{b}\right) + f(n),
\]
where \(a \geq 1\), \(b > 1\), and \(f(n)\) is asymptotically positive, then:

- If \(f(n) = O(n^{\log_b a-\epsilon})\) for some \(\epsilon > 0\), \(T(n) = \Theta(n^{\log_b a})\).
- If \(f(n) = \Theta(n^{\log_b a})\), \(T(n) = \Theta(n^{\log_b a} \log n)\).
- If \(f(n) = \Omega(n^{\log_b a+\epsilon})\) for some \(\epsilon > 0\) and the regularity condition \(a f(n/b) \leq cf(n)\) holds for \(c < 1\), \(T(n) = \Theta(f(n))\).

#### Significance
- The Master Theorem provides a systematic way to solve divide-and-conquer recurrences without tedious expansion.

---

## Complexity Analysis

| Algorithm          | Best Case  | Average Case | Worst Case  | Space Complexity |
|--------------------|------------|--------------|-------------|-------------------|
| Insertion Sort     | \(O(n)\)   | \(O(n^2)\)   | \(O(n^2)\)  | \(O(1)\)          |
| Merge Sort         | \(O(n \log n)\) | \(O(n \log n)\) | \(O(n \log n)\) | \(O(n)\)          |
| Strassen’s Algorithm | N/A         | N/A          | \(O(n^{2.81})\) | \(O(n^2)\)         |

---

## Concrete Examples

1. **Insertion Sort Example:**
   - Input: [5, 2, 4, 6, 1, 3]
   - Process:
     - First pass: [2, 5, 4, 6, 1, 3]
     - Second pass: [2, 4, 5, 6, 1, 3]
     - Continue until sorted.

2. **Merge Sort Example:**
   - Input: [5, 2, 4, 6, 1, 3]
   - Process:
     - Divide: [5, 2, 4] and [6, 1, 3].
     - Recursively sort: [2, 4, 5] and [1, 3, 6].
     - Merge: [1, 2, 3, 4, 5, 6].

---

## Miscellaneous Notes

- **Probabilistic Analysis Example:**
  - QuickSort's randomized partitioning improves average performance.
  - Without randomization, carefully crafted inputs could consistently produce poor performance.

- **Asymptotic Notation:**
  - Formal definitions include:
    - \(f(n) = O(g(n))\): Growth of \(f(n)\) is bounded above by \(g(n)\) for large \(n\).
    - \(f(n) = \Omega(g(n))\): Growth of \(f(n)\) is bounded below by \(g(n)\) for large \(n\).
    - \(f(n) = \Theta(g(n))\): Growth of \(f(n)\) is tightly bounded by \(g(n)\) for large \(n\).

- Appendices (A–D) provide supplementary mathematical background and are excellent references for quick lookup.

This concludes the study notes for *Foundations.*
