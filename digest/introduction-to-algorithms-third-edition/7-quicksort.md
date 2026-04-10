# 7 Quicksort

# Study Notes: Section 7 - Quicksort  
These study notes cover the _Quicksort_ algorithm from "Introduction to Algorithms, Third Edition." Quicksort is one of the most efficient and widely used sorting algorithms due to its simplicity and excellent average-case performance. These notes detail its key concepts, divide-and-conquer paradigm, partitioning scheme, and performance properties.

---

## Overview  
Quicksort is a comparison-based, in-place sorting algorithm that utilizes the **divide-and-conquer** paradigm. Despite its \( O(n^2) \) **worst-case time complexity**, it is favored for its \( \Theta(n \lg n) \) **average-case and best-case performance**. Its efficiency stems from its recursive nature and reliance on dynamically partitioning the data around a selected pivot.

Key attributes:  
- **Divide-and-Conquer Paradigm**: The problem is recursively divided into smaller subproblems.  
- **In-place Sorting**: Requires only a small amount of additional memory \(( O(\lg n) \) auxiliary stack memory).  
- **Performance Dependence**: The running time is strongly influenced by the choice of pivot and the balance of partitions.  
- **Randomized Optimization**: A randomized version of Quicksort mitigates the worst-case for specific inputs.

---

## Key Concepts  
- **Pivot Selection**: The central element for partitioning, which determines how well-balanced the two resulting subarrays are. Poor pivot choices lead to unbalanced partitions and degrade performance.
- **Partitioning**: Rearranges the input so that:
  - All elements less than or equal to the pivot appear before the pivot.
  - All elements greater than the pivot appear after it.
- **Divide-and-Conquer Steps**:
  1. **Divide**: Partition the array into two subarrays around a pivot.
  2. **Conquer**: Recursively sort the subarrays.
  3. **Combine**: No action needed, as the array is formed in sorted order after partitioning.
- **Worst-case Performance**: Occurs with extremely unbalanced partitions (e.g., sorted or almost sorted arrays without a randomized pivot).
- **Randomized Optimization**: A randomized pivot ensures the algorithm performs well on any input with high probability.

---

## Algorithms and Techniques  

### Quicksort Algorithm: Implementation  

**How it works**:  
1. **Select a Pivot**: Often the last element in the subarray, though other strategies (like random selection) may be used for optimization.
2. **Partition the Array**: Rearrange elements around the pivot such that smaller elements appear to its left and larger ones to its right.
3. **Recursively Sort Two Subarrays**: Apply Quicksort to the partitions.

#### Pseudocode  

```plaintext
QUICKSORT(A, p, r)  
1. if p < r  
2.     q = PARTITION(A, p, r)  
3.     QUICKSORT(A, p, q - 1)  
4.     QUICKSORT(A, q + 1, r)
```

```plaintext
PARTITION(A, p, r)  
1. x = A[r]  // Choose pivot  
2. i = p - 1  
3. for j = p to r - 1  
4.     if A[j] <= x  
5.         i = i + 1  
6.         exchange A[i] with A[j]  
7. exchange A[i + 1] with A[r]  
8. return i + 1
```

**Key Example**:  
Given the array \( A = [2, 8, 7, 1, 3, 5, 6, 4] \), and executing `PARTITION` with \( p = 1, r = 8 \):  
1. Choose pivot \( x = 4 \).  
2. Rearrange the array around 4, resulting in \( A = [2, 1, 3, 4, 7, 5, 6, 8] \).  
3. Return \( q = 4 \) as the pivot index.  

---

### Complexity Analysis  

| **Configuration**        | **Partitioning Behavior** | **Time Complexity**       | **Explanation**                                      |
|-------------------------------|--------------------------|---------------------------|------------------------------------------------------|
| **Best Case**                 | Balanced partitions (\( n/2 \)) | \( \Theta(n \lg n) \)         | Divide evenly at each level of recursion.            |
| **Average Case**              | Approximately balanced partitions | \( \Theta(n \lg n) \)         | Random or average input guarantees balanced splits.  |
| **Worst Case**                | Unbalanced partitions (1 element vs \( n - 1 \)) | \( \Theta(n^2) \)           | Pivot leads to no significant partitioning at each recursion. |
| **Space Complexity**          | N/A                      | \( O(\lg n) \) (expected) | Stack frame usage for recursion depth.              |

#### Observations on Performance:  
- Pivot selection is crucial to mitigating worst-case performance.  
- Randomized pivot selection makes the worst-case extremely rare.  
- Even slightly unbalanced splits \( (e.g., 9:1) \) lead to \( O(n \lg n) \) performance.

---

### Randomized Quicksort  

**Random Pivot Selection**:  
Instead of using the last element as the pivot, the algorithm picks a random element in the subarray. This ensures that:  
1. The pivot choice is not influenced by the input order.  
2. The worst-case scenarios occur with steadily decreasing probability.  

#### Randomized Partition Pseudocode  

```plaintext
RANDOMIZED-PARTITION(A, p, r)  
1. i = RANDOM(p, r)  // Choose pivot randomly
2. exchange A[i] with A[r]  
3. return PARTITION(A, p, r)
```

#### Randomized Quicksort Pseudocode  

```plaintext
RANDOMIZED-QUICKSORT(A, p, r)  
1. if p < r  
2.     q = RANDOMIZED-PARTITION(A, p, r)  
3.     RANDOMIZED-QUICKSORT(A, p, q - 1)  
4.     RANDOMIZED-QUICKSORT(A, q + 1, r)
```

**Expected Time Complexity**:  
- \( \Theta(n \lg n) \): On any input distribution, randomized pivot selection places the algorithm's performance closer to the average case.  
- **Practical Implications**: Randomization ensures robust performance regardless of input.

---

## Theoretical Results  

### **Theorem 1** (Quicksort Worst-Case):  
Let \( T(n) \) denote the worst-case runtime of Quicksort. If PARTITION produces unbalanced partitions at every level, \( T(n) = \Theta(n^2) \).  

### **Theorem 2** (Quicksort Average-Case):  
Given a uniformly random input, the expected runtime of Quicksort is \( T(n) = \Theta(n \lg n) \). This also applies to the Randomized Quicksort variant.

**Proof Outline**:  
Follows directly from a recurrence tree analysis and the Master Theorem for divide-and-conquer recurrences. Balanced or nearly-balanced splits lead to \( O(\lg n) \) depth and \( O(n) \) work per level.

---

## Insights into Recursive Partitioning  

### Loop Invariant in `PARTITION`  

Invariant Properties (maintained during array traversal):  
1. \( A[p \ldots i] \leq x \) (Elements less than/equal to the pivot).
2. \( A[i+1 \ldots j-1] > x \) (Elements greater than the pivot).
3. \( A[r] = x \) (Pivot remains unchanged).

These invariants ensure correctness of the partitioning process. Upon termination, \( A[q] \) (pivot's final position) divides the subarray into two valid partitions.

---

## Conclusion  
Quicksort demonstrates the elegance of the divide-and-conquer approach. Though its worst-case complexity \( O(n^2) \) may appear prohibitive, its average-case efficiency and in-place nature make it optimal for numerous practical applications. Randomized pivot selection further strengthens its performance regardless of input. Mastery of this algorithm is fundamental to understanding advanced sorting techniques.
