# 2 Getting Started

```markdown
# Study Notes: Chapter 2 - Getting Started

This document provides comprehensive study notes on **Chapter 2: Getting Started** from _Introduction to Algorithms, Third Edition_. These notes introduce fundamental ideas in algorithm design and analysis, focusing on two sorting algorithms: **Insertion Sort** and **Merge Sort**. The chapter explores pseudocode conventions, correctness proofs using loop invariants, and time complexity analysis.

## Overview

The chapter covers:

1. **Insertion Sort** for small-scale sorting, explaining its working mechanism, pseudocode, and runtime analysis.
2. **Merge Sort**, an example of the divide-and-conquer design paradigm, including its recursive structure and time complexity analysis.

It also introduces the use of **pseudocode** to represent algorithms concisely and the framework of **loop invariants** to prove algorithm correctness.

---

## Key Concepts

- **Pseudocode**:
  - A high-level description of algorithms, blending English and programming constructs.
  - Focuses on clarity and skipping software engineering concerns (e.g., modularity, error handling).

- **Sorting Problem**:
  - Input: A sequence of \( n \) numbers stored in an array.
  - Output: A permutation of the numbers such that they are in non-decreasing order.

- **Loop Invariants**:
  - Technique for proving algorithm correctness by maintaining certain properties.
  - Prove correctness using **initialization**, **maintenance**, and **termination** of the invariant.

- **Complexity Analysis**:
  - Focuses on how the running time grows with input size, using asymptotic notations such as \( O \), \( \Theta \), and \( \Omega \).

---

## Algorithms and Techniques

### Insertion Sort

#### Introduction
Insertion Sort is an efficient algorithm for sorting small arrays. It works similarly to arranging a hand of cards, repeatedly inserting the current card into its correct position in the sorted portion.

#### How it Works
1. Treat the first element as sorted.
2. For each remaining element:
   - Compare it to elements in the sorted portion (from right to left).
   - Shift larger elements one position to the right.
   - Insert the current element in its correct position.
3. Continue until all elements are sorted.

#### Pseudocode
```plaintext
INSERTION-SORT(A)
1  for j = 2 to A.length
2      key = A[j]  // Current element to be inserted
3      i = j - 1
4      while i > 0 and A[i] > key
5          A[i + 1] = A[i]  // Shift element to the right
6          i = i - 1
7      A[i + 1] = key  // Place key in the correct position
```

#### Correctness Proof Using Loop Invariant
- **Invariant** (at the start of each iteration): Subarray \( A[1..j-1] \) is sorted.
- **Initialization**: Before the first loop iteration (\( j = 2 \)), \( A[1..1] \) is trivially sorted.
- **Maintenance**: During each iteration, the algorithm inserts \( A[j] \) into its correct position within the sorted subarray \( A[1..j-1] \), maintaining the invariant.
- **Termination**: When \( j > n \), the entire array \( A[1..n] \) is sorted.

#### Time Complexity
- **Best Case**: \( O(n) \) if the array is already sorted (no shifting is required).
- **Worst Case**: \( O(n^2) \) for a reverse-sorted array (maximum shifting in each step).
- **Average Case**: \( O(n^2) \) across random permutations.

#### Space Complexity
- **In-place**: \( O(1) \) additional space.

#### Example (Walkthrough)
Input: \( A = [5, 2, 4, 6, 1, 3] \)

1. Iteration 1 (\( j = 2 \)): Insert 2 into sorted subarray [5] → [2, 5].
2. Iteration 2 (\( j = 3 \)): Insert 4 into sorted subarray [2, 5] → [2, 4, 5].
3. Continue until all elements are sorted → Output: [1, 2, 3, 4, 5, 6].

**Figures:**
![Insertion Sort Demonstration](images/p39_fig2.svg)

---

## Complexity Analysis

The following table compares the **time complexity** of Insertion Sort in various scenarios:

| Algorithm      | Best Case (\( \Omega \)) | Worst Case (\( O \)) | Average Case (\( \Theta \)) |
|----------------|--------------------------|-----------------------|----------------------------|
| Insertion Sort | \( O(n) \)              | \( O(n^2) \)         | \( O(n^2) \)              |

---

## Appendix: Tools for Proof and Pseudocode Conventions

### Loop Invariants Framework
- To prove an algorithm correct:
  1. **Initialization**: Show the invariant holds before the first loop iteration.
  2. **Maintenance**: Show it holds after each iteration.
  3. **Termination**: Use the invariant and loop termination condition to derive the correctness.

### Pseudocode Conventions
- **Indentation**: Indicates block structure.
- **Commenting**: Use `//` for comments.
- **Variable Scope**: All variables are local unless stated otherwise.
- **Array Notation**:
  - \( A[i] \): Accesses the \( i \)-th element.
  - \( A[1:j] \): Accesses a subarray.

---

This concludes the study notes for Section 2.1 of the chapter. Further sections cover algorithms like Merge Sort and the divide-and-conquer paradigm.
```
