# 8 Sorting in Linear Time

```markdown
# Sorting in Linear Time: Study Notes

## Overview
In earlier sections, sorting algorithms like Merge Sort, QuickSort, and HeapSort were introduced, all achieving an **O(n lg n)** complexity, which is the optimal bound for comparison-based sorting algorithms. However, these algorithms rely exclusively on comparison operations. In this chapter, we examine **non-comparison-based sorting algorithms** like **Counting Sort**, **Radix Sort**, and **Bucket Sort**, which can sort in **linear time** (i.e., **O(n)**) under certain conditions. These algorithms achieve improved performance by leveraging additional constraints, such as assumptions about the input distribution.

This chapter also introduces the **decision-tree model**, a theoretical foundation to prove that comparison-based sorts have a worst-case lower bound of **Ω(n lg n)**.

---

## Key Concepts

- **Comparison Sorts**:
    - Sorting algorithms that rely solely on comparisons to determine order.
    - Examples: Merge Sort, QuickSort, HeapSort.
    - Lower bound for worst-case running time: **Ω(n lg n)** (proven using decision trees).

- **Non-Comparison Sorts**:
    - Algorithms that use operations on the input elements beyond comparisons.
    - Leverage properties like input distribution or integer-based keys.
    - Can achieve linear time complexity under certain conditions.

- **Decision Tree Model**:
    - Abstract representation of a comparison sort as a full binary tree.
    - Nodes represent comparisons, and leaves represent possible sorted permutations.
    - Height of the decision tree determines the worst-case number of comparisons.

- **Stability**:
    - A sorting algorithm is stable if two elements with the same value appear in the same relative order in both input and output.
    - Stability is vital in algorithms like radix sort that rely on intermediate sorting.

---

## Algorithms and Techniques

### Decision Tree Model and Lower Bounds

#### How It Works
- The **decision tree model** abstracts a comparison sort algorithm as a binary tree:
    - Internal nodes represent comparisons (e.g., `ai ≤ aj`).
    - Leaves represent sorted permutations.
    - A path from the root to a leaf corresponds to the sequence of comparisons made by the algorithm for a specific input.

#### Key Theorem
**Theorem 8.1**  
- Any comparison sort algorithm requires **Ω(n lg n)** comparisons in the worst case.

**Proof**:  
1. A correct comparison sort must account for all possible permutations of the input, i.e., **n!** permutations.
2. Each permutation must correspond to a distinct leaf in the decision tree.
3. A binary tree with height `h` has at most `2^h` leaves.
4. For a valid decision tree:
   \[
   n! \leq 2^h
   \]
   Taking logarithms:
   \[
   h \geq \lg(n!)
   \]
   Using the asymptotic bound for \(\lg(n!)\), \(h = Ω(n \lg n)\).

#### Significance
This theorem establishes that **Ω(n lg n)** is a fundamental lower bound for comparison-based sorting; no comparison sort can be asymptotically faster.

---

### Counting Sort

#### How It Works
Counting Sort is a **non-comparison-based** algorithm that sorts integers by counting the frequency of each value. It uses these counts to place the integers into their correct positions in the sorted array.

**Conditions for Counting Sort**:
- Input values fall within a known range **[0, k]**.
- Convenient when **k = O(n)**.

#### Steps in Counting Sort:
1. Count occurrences of each input value using an auxiliary array.
2. Compute the cumulative sum of these counts to determine the positions of elements.
3. Place each element into the sorted output array using its position information.

#### Pseudocode: Counting Sort
```pseudo
COUNTING-SORT(A, B, k)
1. Let C[0:k] be a new array, initialized to 0
2. for i = 0 to k
       C[i] = 0
3. for j = 1 to A.length
       C[A[j]] = C[A[j]] + 1
4. for i = 1 to k
       C[i] = C[i] + C[i - 1]
5. for j = A.length downto 1
       B[C[A[j]]] = A[j]
       C[A[j]] = C[A[j]] - 1
```

#### Time Complexity
| Step                          | Time Complexity |
|-------------------------------|-----------------|
| Initialization and frequency count | **O(n + k)**        |
| Cumulative sum computation    | **O(k)**             |
| Sorting the output            | **O(n)**             |

**Overall**: **O(n + k)**  
When **k = O(n)**, Counting Sort runs in **O(n)** time.

#### Example
Input: `A = [2, 5, 3, 0, 2, 3, 0, 3]`, `k = 5`  
Intermediate arrays during computation:
- Frequency array `C[i]`: `[2, 0, 2, 3, 0, 1]`
- Cumulative count: `[2, 2, 4, 7, 7, 8]`
- Result after sorting: `[0, 0, 2, 2, 3, 3, 3, 5]`

#### Properties
- Stable: Uses cumulative counts to maintain relative order of elements with the same value.
- Efficient: Best suited for integer sorting in a limited range.

---

### Complexity Analysis

| Algorithm       | Best Case   | Worst Case  | Space Complexity | Stable?       |
|-----------------|-------------|-------------|-------------------|---------------|
| Merge Sort      | O(n lg n)   | O(n lg n)   | O(n)             | Yes           |
| Heap Sort       | O(n lg n)   | O(n lg n)   | O(1)             | No            |
| Counting Sort   | O(n + k)    | O(n + k)    | O(n + k)         | Yes           |
| QuickSort       | O(n lg n)   | O(n^2)      | O(log n) (avg)   | No            |

---

## Additional Exercises and Theorems

### Exercise 8.1-1
Using **Counting Sort**, sort input `A = [6, 0, 2, 0, 1, 3, 4, 6, 1, 3, 2]` with `k = 6`.  
Solution steps will resemble the example provided above.

### Corollary 8.2
- **Heapsort** and **Merge Sort** are asymptotically optimal comparison-based sort algorithms because they achieve the lower bound of **O(n lg n)**.

---

## Conclusion
This chapter highlights the limitations of comparison-based sorting algorithms and introduces non-comparison-based alternatives that can achieve optimal linear time under specific constraints. The decision tree model serves as the theoretical foundation for understanding these limitations. Algorithms like Counting Sort demonstrate how leveraging input structure can bypass the **Ω(n lg n)** bound.
```
