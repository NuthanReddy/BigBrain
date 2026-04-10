# 4 Divide-and-Conquer

# Divide-and-Conquer (Chapter 4)

## Overview

Divide-and-Conquer is a fundamental algorithmic paradigm widely used in computer science for solving recursive problems efficiently. It structures an algorithm by dividing the problem into smaller subproblems, solving these subproblems recursively, and combining the solutions to address the original problem. This paradigm has wide applications, from sorting (e.g., Merge Sort), finding maximum subarrays, to efficient matrix multiplication.

Recurrences naturally arise in the analysis of divide-and-conquer algorithms, as they describe the algorithm's running time in relation to the size of the problem.

---

## Key Concepts

- **Divide-and-Conquer Paradigm**:
    - **Divide** the problem into smaller instances of the same problem.
    - **Conquer** the subproblems recursively (solve the base cases directly).
    - **Combine** the solutions to form the solution of the original problem.
  
- **Base Case**: Recursion ends when subproblems become small or trivial enough to solve directly.

- **Recurrence**:
  - A mathematical equation or inequality that describes the running time of a recursive algorithm.
  - It expresses the time required for a problem of size `n` in terms of smaller problem sizes.

- **Recurrence Solving Techniques**:
    - **Substitution Method**: Guess the solution and validate using induction.
    - **Recursion-Tree Method**: Expand recurrence as a tree and sum costs across levels.
    - **Master Theorem**: Provides asymptotic bounds for divide-and-conquer recurrences of the format:
      \[
      T(n) = aT\left(\frac{n}{b}\right) + f(n)
      \]
      where \(a \geq 1\), \(b > 1\), and \(f(n)\) describes the time to divide and combine.

- **Technicalities in Recurrence Analysis**:
    - Floors and ceilings are often omitted for simplicity.
    - Boundary conditions (e.g., base cases) are not explicitly stated unless necessary.

---

## Algorithms and Techniques

### Maximum-Subarray Problem

#### Problem Definition:
Given an array \(A[1 \dots n]\) of numbers (representing daily stock price changes), find the non-empty, contiguous subarray with the maximum sum.

#### Brute-Force Solution:
- **Approach**:
  - Iterate over all possible subarrays \(A[i \dots j]\) for \(1 \leq i \leq j \leq n\).
  - Compute the sum of each subarray and track the maximum.
- **Pseudocode Sketch**:
    ```python
    def max_subarray_brute_force(A):
        n = len(A)
        max_sum = float('-inf')
        for i in range(n):
            for j in range(i, n):
                current_sum = sum(A[i:j+1])
                max_sum = max(max_sum, current_sum)
        return max_sum
    ```
- **Time Complexity**: \(O(n^2)\) (since there are \(O(n^2)\) subarrays, and summing each takes \(O(1)\) under precomputed prefix sums).
- **Space Complexity**: \(O(1)\).

#### Optimized Divide-and-Conquer Solution:

This approach further reduces complexity by dividing the array and constructing the solution recursively.

- **Approach**:
  - Divide the array \(A\) into two halves: \(A_{\text{left}}\) and \(A_{\text{right}}\).
  - The maximum subarray must either:
    1. Be entirely within \(A_{\text{left}}\),
    2. Be entirely within \(A_{\text{right}}\),
    3. Cross the boundary between \(A_{\text{left}}\) and \(A_{\text{right}}\).
  - Recursively solve for the left and right halves, and calculate the cross-boundary maximum subarray using a linear-time operation.
- **Pseudocode Sketch**:
    ```python
    def find_max_crossing_subarray(A, low, mid, high):
        left_sum = float('-inf')
        sum = 0
        max_left = mid
        for i in range(mid, low - 1, -1):
            sum += A[i]
            if sum > left_sum:
                left_sum = sum
                max_left = i

        right_sum = float('-inf')
        sum = 0
        max_right = mid + 1
        for j in range(mid + 1, high + 1):
            sum += A[j]
            if sum > right_sum:
                right_sum = sum
                max_right = j

        return max_left, max_right, left_sum + right_sum

    def max_subarray_divide_and_conquer(A, low, high):
        if low == high:
            return low, high, A[low]  # Base case: single element

        mid = (low + high) // 2
        left_low, left_high, left_sum = max_subarray_divide_and_conquer(A, low, mid)
        right_low, right_high, right_sum = max_subarray_divide_and_conquer(A, mid + 1, high)
        cross_low, cross_high, cross_sum = find_max_crossing_subarray(A, low, mid, high)

        if left_sum >= right_sum and left_sum >= cross_sum:
            return left_low, left_high, left_sum
        elif right_sum >= left_sum and right_sum >= cross_sum:
            return right_low, right_high, right_sum
        else:
            return cross_low, cross_high, cross_sum
    ```
- **Time Complexity**:
    - The recurrence for this algorithm is:
      \[
      T(n) = 2T\left(\frac{n}{2}\right) + O(n)
      \]
      Solving this recurrence gives \(T(n) = O(n \log n)\).
- **Space Complexity**: \(O(\log n)\) (space for recursion stack).

---

## Complexity Comparison Table

| **Algorithm**                  | **Time Complexity** | **Space Complexity** | **Notes**                                                    |
|--------------------------------|---------------------|-----------------------|-------------------------------------------------------------|
| Brute-Force Solution           | \(O(n^2)\)         | \(O(1)\)             | Simple, but inefficient for large \(n\).                   |
| Divide-and-Conquer Solution    | \(O(n \log n)\)    | \(O(\log n)\)        | More efficient, uses recursive divide-and-conquer.         |

---

## Relevant Theorem: Master Theorem

For recurrences of the form:
\[
T(n) = aT\left(\frac{n}{b}\right) + f(n)
\]
where \(a \geq 1\), \(b > 1\):
- Let \(p = \log_b a\).
- Compare \(f(n)\) with \(n^p\):
    1. If \(f(n) \in O(n^{p-\epsilon})\) for some \(\epsilon > 0\), then \(T(n) \in \Theta(n^p)\).
    2. If \(f(n) \in \Theta(n^p \log^k n)\), then \(T(n) \in \Theta(n^p \log^{k+1} n)\).
    3. If \(f(n) \in \Omega(n^{p+\epsilon})\) for some \(\epsilon > 0\), and if \(af\left(\frac{n}{b}\right) \leq cf(n)\) for some \(c < 1\) and sufficiently large \(n\), then \(T(n) \in \Theta(f(n))\).

---

## Concrete Example: Maximum-Subarray Problem

For the array \(A = [13, -3, -25, 20, -3, -16, -23, 18, 20, -7, 12, -5, -22, 15, -4, 7]\):
- Using the divide-and-conquer algorithm:
    - Left subarray: \(A[1 \dots 8]\), with sum \(18 + 20 = 43\).
    - Maximum subarray is identified as \(A[8 \dots 11]\), with sum \(43\).
