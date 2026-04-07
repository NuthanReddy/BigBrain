# Chapter 2: Getting Started

## Overview
This chapter introduces the fundamental framework for designing and analyzing algorithms using two sorting algorithms—insertion sort and merge sort—as case studies. It establishes key concepts including pseudocode conventions, loop invariants for proving correctness, the RAM computational model, worst-case analysis, order of growth, and the divide-and-conquer paradigm.

## Key Concepts
- **Pseudocode conventions**: The book uses a pseudocode similar to C/Java/Python with indentation-based block structure, 1-indexed arrays, dot notation for attributes (e.g., `A.length`), pass-by-value semantics (but pointers to arrays/objects are copied), short-circuit boolean operators, and sentinel values.
- **Loop invariants**: A formal technique for proving algorithm correctness, requiring three properties:
  - **Initialization**: The invariant is true before the first iteration.
  - **Maintenance**: If true before an iteration, it remains true before the next.
  - **Termination**: When the loop ends, the invariant yields a useful correctness property.
- **RAM model**: The Random Access Machine model assumes a single processor executing instructions sequentially, with constant-time arithmetic, data movement, and control operations. Word size is c lg n bits for constant c ≥ 1.
- **Input size**: Depends on the problem—number of items for sorting, number of bits for integer multiplication, or vertices and edges for graph problems.
- **Running time**: The number of primitive operations (steps) executed, where each line of pseudocode takes constant time cᵢ.
- **Worst-case vs. average-case analysis**: The book primarily focuses on worst-case analysis because it provides a guaranteed upper bound, worst cases occur frequently in practice, and the average case is often roughly as bad as the worst case.
- **Order of growth**: Focuses on the leading term of the running time formula, ignoring lower-order terms and constant coefficients. Uses Θ-notation informally (formalized in Chapter 3).

## Algorithms and Techniques

### Insertion Sort
- **Approach**: Incremental—maintains a sorted subarray A[1..j−1] and inserts each new element A[j] into its correct position by shifting larger elements rightward.
- **Pseudocode logic**:
  1. For j = 2 to A.length:
  2. Store key = A[j]
  3. Scan backward through A[1..j−1], shifting elements greater than key one position right
  4. Place key in the vacated position
- **Loop invariant**: At the start of each iteration, A[1..j−1] contains the original elements of those positions, but in sorted order.
- **In-place**: Uses only constant extra memory.

### Merge Sort
- **Approach**: Divide-and-conquer paradigm:
  - **Divide**: Split the n-element array into two subarrays of n/2 elements each.
  - **Conquer**: Recursively sort both subarrays.
  - **Combine**: Merge the two sorted subarrays using the MERGE procedure.
- **MERGE procedure**: Takes sorted subarrays A[p..q] and A[q+1..r], copies them into auxiliary arrays L and R with sentinel values (∞), then repeatedly selects the smaller of the two front elements to fill A[p..r].
- **MERGE-SORT(A, p, r)**: Base case is p ≥ r (single element); otherwise computes midpoint q = ⌊(p+r)/2⌋, recursively sorts both halves, and merges.
- **Correctness**: Proved via loop invariant on the MERGE procedure's main loop.

### Additional Algorithms Mentioned
- **Selection sort** (Exercise 2.2-2): Find the minimum, swap with first position; repeat for remaining elements. Θ(n²) in all cases.
- **Bubble sort** (Problem 2-2): Repeatedly swap adjacent out-of-order elements. Θ(n²) worst case.
- **Binary search** (Exercise 2.3-5): Halve the search space each step; Θ(lg n) worst case.
- **Horner's rule** (Problem 2-3): Evaluate a degree-n polynomial in Θ(n) time.

## Complexity Analysis

### Insertion Sort
| Case | Running Time | When It Occurs |
|------|-------------|----------------|
| Best case | Θ(n) | Input already sorted (tⱼ = 1 for all j) |
| Worst case | Θ(n²) | Input in reverse sorted order (tⱼ = j for all j) |
| Average case | Θ(n²) | Random input (tⱼ ≈ j/2 on average) |

- Space: O(1) auxiliary (in-place).

### Merge Sort
- **Recurrence**: T(n) = 2T(n/2) + Θ(n) for n > 1, with T(1) = Θ(1).
- **Solution**: T(n) = Θ(n lg n) in all cases.
- **Recursion tree argument**: The tree has lg n + 1 levels, each contributing cn total cost, yielding cn lg n + cn = Θ(n lg n).
- **Space**: Θ(n) auxiliary for the L and R arrays in MERGE.

### MERGE Procedure
- Time: Θ(n) where n = r − p + 1 (linear in the number of elements being merged).

## Key Takeaways
- **Loop invariants** are the primary tool for proving algorithm correctness—analogous to mathematical induction but with a termination condition that yields the desired result.
- **Insertion sort** is efficient for small or nearly-sorted inputs (Θ(n) best case) but degrades to Θ(n²) in the worst case.
- **Merge sort** guarantees Θ(n lg n) worst-case performance via the divide-and-conquer paradigm, making it asymptotically superior to insertion sort for large inputs.
- The **divide-and-conquer** pattern (divide → conquer → combine) naturally leads to recursive algorithms whose running times are described by recurrences of the form T(n) = aT(n/b) + D(n) + C(n).
- For large inputs, **order of growth** matters far more than constant factors—a Θ(n lg n) algorithm on slow hardware beats a Θ(n²) algorithm on fast hardware.
