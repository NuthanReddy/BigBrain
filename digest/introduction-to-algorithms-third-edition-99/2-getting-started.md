# 2 Getting Started

# Study Notes on **Getting Started** from *Introduction to Algorithms, Third Edition*

## Overview

This chapter introduces the foundational concepts of algorithm design and analysis. It is self-contained, providing insights into pseudocode conventions, algorithm correctness through loop invariants, and runtime analysis. The chapter primarily focuses on **insertion sort**, a simple sorting algorithm, and briefly introduces the **divide-and-conquer approach** via **merge sort**. The explanations are supplemented with illustrations and step-by-step walkthroughs for clarity.

---

## Key Concepts

- **Pseudocode**:
  - The algorithms in this book are described using pseudocode: concise, language-agnostic, and clear representations resembling programming languages.
  - Does not focus on software engineering aspects like data abstraction or error handling.
  - Adopts conventions like indentation to represent block structure.

- **Loop Invariants**:
  - Used to demonstrate the correctness of an algorithm.
  - A statement about a loop that holds true:
    - Before the first iteration (`Initialization`).
    - During every iteration (`Maintenance`).
    - At the end of the loop (`Termination`).

- **Algorithm Correctness**:
  - Correctness for sorting algorithms is proven by ensuring the output is a permutation of the input where elements are sorted.

- **Complexity Analysis**:
  - Introduces runtime complexity as a function of input size, focusing on "growth rates" of algorithms.
  - Example metrics: **best-case**, **worst-case**, and **average-case runtime**.

- **Sorting Problem**:
  - Input: A sequence of numbers stored in an array.
  - Output: A permutation of this sequence such that elements are in non-decreasing order.

---

## Algorithms and Techniques

### 1. Insertion Sort

#### **How It Works**

Insertion sort is an intuitive algorithm mimicking how people sort playing cards. Initially, an empty "hand" is considered sorted, and one card is added to it from the table at each step. The algorithm inserts each card into its correct position in the sorted hand by comparing it with previously placed cards (right-to-left comparisons).

Key Procedure for Insertion Sort:
1. Consider the array divided into a **sorted** part and an **unsorted** part.
2. For each element in the unsorted part, insert it into its correct position in the sorted part by shifting elements to make room.

---

#### **Pseudocode**

```
// A: Array to be sorted
// n: Number of elements in A

INSERTION-SORT(A):
1. for j = 2 to A.length
2.    key = A[j]     // Current element being inserted 
3.    i = j - 1      // Pointer to compare with elements in sorted subarray A[1:j-1]
4.    while i > 0 and A[i] > key
5.        A[i + 1] = A[i]   // Shift larger elements to the right
6.        i = i - 1
7.    A[i + 1] = key        // Insert key in the correct position
```

---

#### **Example**  
Given the array `A = [5, 2, 4, 6, 1, 3]`, let us sort it using insertion sort:

- **Pass 1** (`j = 2`): `5` is already considered sorted. Insert `2` → `[2, 5, 4, 6, 1, 3]`  
- **Pass 2** (`j = 3`): Insert `4` → `[2, 4, 5, 6, 1, 3]`
- **Pass 3** (`j = 4`): Insert `6` → `[2, 4, 5, 6, 1, 3]` (no change as `6` is in position)
- **Pass 4** (`j = 5`): Insert `1` → `[1, 2, 4, 5, 6, 3]`
- **Pass 5** (`j = 6`): Insert `3` → `[1, 2, 3, 4, 5, 6]`

**Final sorted Array:** `[1, 2, 3, 4, 5, 6]`

---

#### **Time Complexity Analysis**

- **Best-case Runtime**: \( O(n) \)
  - When the array is already sorted, the algorithm merely traverses the array, performing no shifting.

- **Worst-case Runtime**: \( O(n^2) \)
  - When the array is sorted in reverse order, every insertion requires comparing and shifting \( j - 1 \) elements.

- **Average-case Runtime**: \( O(n^2) \)
  - The average occurs when half the elements need to be shifted.

- **Space Complexity**: \( O(1) \)
  - The algorithm operates in-place with no additional memory requirements.

---

### 2. Correctness of Insertion Sort Using Loop Invariant

We prove the correctness of the algorithm by showing it maintains the **loop invariant**:

#### **Loop Invariant Statement**:

*"At the start of each iteration of the for loop, the subarray \( A[1 \dots j-1] \) consists of the elements originally in \( A[1 \dots j-1] \), but in sorted order."*

#### **Proof Steps**:
1. **Initialization**:
   - Before the first iteration (\( j = 2 \)), the subarray \( A[1 \dots j-1] = A[1] \) contains a single element and is trivially sorted.

2. **Maintenance**:
   - During each iteration, the `key` is compared with elements in the sorted portion \( A[1 \dots j-1] \). These elements are shifted right until the correct position for `key` is found. This maintains the sorted order in \( A[1 \dots j] \).

3. **Termination**:
   - When \( j = n + 1 \) (loop terminates), the entire array \( A[1 \dots n] \) is sorted.

By showing these conditions hold, we conclude that insertion sort correctly sorts the array.

---

### 3. Divide-and-Conquer: Merge Sort (Introduced Briefly)

While the chapter dives deeper into **merge sort** in later sections, it highlights the key divide-and-conquer strategy:
- **Divide** the array into two halves.
- **Conquer** by recursively sorting both halves.
- **Combine** the two sorted halves into a unified sorted array.

Merge sort demonstrates better performance with a runtime of \( O(n \log n) \) compared to insertion sort's \( O(n^2) \), especially for larger arrays.

---

## Complexity Analysis

| **Algorithm**    | **Best-Case Time Complexity** | **Worst-Case Time Complexity** | **Average-Case Time Complexity** | **Space Complexity** |
|-------------------|-------------------------------|---------------------------------|-----------------------------------|-----------------------|
| **Insertion Sort**| \( O(n) \)                   | \( O(n^2) \)                   | \( O(n^2) \)                     | \( O(1) \)           |
| **Merge Sort**    | \( O(n \log n) \)            | \( O(n \log n) \)              | \( O(n \log n) \)                | \( O(n) \)           |

---

## Conclusion

This chapter forms the cornerstone for understanding algorithm design and analysis:
1. **Insertion Sort** serves as an approachable example, demonstrating pseudocode structure, loop invariants, and runtime analysis.
2. **Merge Sort**, while only briefly referenced here, showcases the potential of more efficient techniques like divide-and-conquer for larger datasets.
Proper understanding of these basics will enable the exploration of more sophisticated algorithms later in the book.
