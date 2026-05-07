# I Foundations

# Foundations: Study Notes for "Introduction to Algorithms, Third Edition"

## Overview

The "Foundations" section of *Introduction to Algorithms* serves as the introductory part of the book and establishes the groundwork for studying algorithm design and analysis. This part introduces essential concepts, such as what an algorithm is, how to analyze its efficiency, and various fundamental paradigms for solving problems algorithmically. Topics covered include sorting algorithms, asymptotic notation, divide-and-conquer strategies, recurrence relations, and randomized algorithms. The material provides the theoretical and practical tools necessary to understand and evaluate algorithms throughout the book.

This document offers a detailed breakdown of the concepts, techniques, and examples presented in Part I: *Foundations*.

---

## Key Concepts

- **Definition of an Algorithm**: 
  An algorithm is a well-defined computational procedure that takes some value or set of values as input and produces some value or set of values as output. Algorithms are abstract and independent of programming language.

- **Algorithms as a Technology**: 
  Just as advances in hardware, software methodologies (e.g., object-oriented programming), and networking have driven computer system capabilities, the development and improvement of algorithms form a key technological advance.

- **Divide-and-Conquer**: 
  A technique for designing algorithms that recursively split a problem into "smaller" subproblems, solve each subproblem, and combine their solutions to solve the original problem.

- **Probabilistic Analysis**: 
  The study of the average-case complexity of algorithms assuming a probability distribution over inputs.

- **Randomized Algorithms**: 
  Algorithms that make random choices during their computation to influence their behavior or result. These introduce randomness to improve performance or robustness.

- **Asymptotic Notation**: 
  A framework for analyzing and describing the growth of algorithms' running time or space requirements in terms of their input size, using notations such as \(O\)-notation, \(\Omega\)-notation, and \(\Theta\)-notation.

---

## Algorithms and Techniques

### Insertion Sort

#### How It Works
- Insertion Sort works by building the sorted array element by element. Initially, the first element is considered sorted. Each subsequent element is inserted into its correct position relative to the elements already sorted.

#### Pseudocode (Sketch)

```python
INSERTION-SORT(A)
1. for j = 2 to A.length
2.     key = A[j]
3.     i = j - 1
4.     while i > 0 and A[i] > key
5.         A[i + 1] = A[i]
6.         i = i - 1
7.     A[i + 1] = key
```

#### Time Complexity
- **Best Case**: \(O(n)\) (when the array is already sorted)
- **Worst Case**: \(O(n^2)\) (when the array is reverse-sorted)
- **Average Case**: \(O(n^2)\)

#### Space Complexity
- \(O(1)\) (In-place sorting algorithm)

#### Example
Sort the array \([5, 2, 4, 6, 1, 3]\):
```
[2, 5, 4, 6, 1, 3] -> [2, 4, 5, 6, 1, 3] -> [2, 4, 5, 6, 1, 3] -> [1, 2, 4, 5, 6, 3] -> [1, 2, 3, 4, 5, 6]
```

---

### Merge Sort

#### How It Works
- Merge Sort uses a recursive "divide-and-conquer" approach:
  1. Divide the array into two halves.
  2. Recursively sort each half.
  3. Merge the two sorted halves into a single sorted array.

#### Pseudocode (Sketch)

```python
MERGE(A, p, q, r)
1. Create two subarrays L = A[p..q] and R = A[q+1..r]
2. Compare elements from L and R, copy the smaller element back to A
3. Copy any remaining elements from L and R to A

MERGE-SORT(A, p, r)
1. if p < r
2.     q = floor((p + r) / 2)
3.     MERGE-SORT(A, p, q)
4.     MERGE-SORT(A, q + 1, r)
5.     MERGE(A, p, q, r)
```

#### Time Complexity
- **Best Case**: \(O(n \log n)\)
- **Worst Case**: \(O(n \log n)\)
- **Average Case**: \(O(n \log n)\)

#### Space Complexity
- \(O(n)\) (Requires additional memory for temporary arrays during the merge step)

#### Example
Sort the array \([5, 2, 4, 6, 1, 3]\):
1. Divide into \([5, 2, 4]\) and \([6, 1, 3]\)
2. Recursively sort these halves: \([2, 4, 5]\) and \([1, 3, 6]\)
3. Merge: \([1, 2, 3, 4, 5, 6]\)

---

## Complexity Analysis Table

| Algorithm       | Best Case  | Average Case | Worst Case  | Space Complexity | Stable? |
|-----------------|------------|--------------|-------------|------------------|---------|
| Insertion Sort  | \(O(n)\)   | \(O(n^2)\)    | \(O(n^2)\)   | \(O(1)\)         | Yes     |
| Merge Sort      | \(O(n \log n)\) | \(O(n \log n)\) | \(O(n \log n)\) | \(O(n)\)         | Yes     |

---

## Additional Techniques

### Recurrence Relations & The Master Method
#### Definition
Recurrence relations describe the running time of recursive algorithms in terms of the size of their inputs. The *Master Theorem* is a formula that provides asymptotic bounds for recurrences of the form:
\[
T(n) = aT\left(\frac{n}{b}\right) + f(n)
\]
where \(a \geq 1\), \(b > 1\), and \(f(n)\) is asymptotically positive.

#### Theorem (Master Theorem)
For the recurrence \(T(n)\):
1. If \(f(n) = O(n^{\log_b a - \epsilon})\) for some \(\epsilon > 0\), then \(T(n) = \Theta(n^{\log_b a})\).
2. If \(f(n) = \Theta(n^{\log_b a})\), then \(T(n) = \Theta(n^{\log_b a} \cdot \log n)\).
3. If \(f(n) = \Omega(n^{\log_b a + \epsilon})\) for some \(\epsilon > 0\), and if the "regularity condition" holds, then \(T(n) = \Theta(f(n))\).

#### Example
For merge sort:
\[
T(n) = 2T\left(\frac{n}{2}\right) + O(n)
\]
Here, \(a = 2\), \(b = 2\), and \(f(n) = O(n)\). Since \(f(n) = \Theta(n^{\log_2 2}) = \Theta(n)\), case 2 of the Master Theorem applies:
\[
T(n) = \Theta(n \log n)
\]

---

### Probabilistic Analysis and Randomized Algorithms
- **Probabilistic Analysis** allows for determining average-case complexity based on the probability distribution of inputs.
- **Randomized Algorithms** inject randomness into their behavior to:
  - Avoid worst-case inputs.
  - Enforce uniform distributions over inputs.
  - Bound the probability of errors (useful for algorithms like Monte Carlo methods).

#### Example
Randomized Quicksort:
The pivot is chosen randomly, preventing consistently poor performance on already sorted or reverse-sorted inputs. Expected time complexity: \(O(n \log n)\).

---

## Summary
- Part I lays the foundational concepts in algorithm design and analysis.
- Sorting algorithms such as Insertion Sort and Merge Sort are introduced and analyzed.
- Tools like asymptotic notation and the Master Method simplify the analysis of algorithm efficiency.
- Randomized algorithms and probabilistic analysis provide additional flexibility for solving complex problems. 

These topics form the building blocks for understanding more advanced algorithms and techniques explored in later chapters.
