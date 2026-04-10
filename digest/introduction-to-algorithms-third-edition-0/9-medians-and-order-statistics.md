# 9 Medians and Order Statistics

# Study Notes: Medians and Order Statistics

## Overview
In the study of algorithms, finding the "order statistics" of a dataset refers to identifying the ith smallest element in a collection of n elements. Special cases of this problem include finding the minimum, maximum, and median. This section introduces algorithms to solve the **selection problem**, including simple comparison-based methods for minimum/maximum and more advanced, theoretically significant algorithms for general selection. The goal is often to achieve optimal complexity, either in the expected sense or in the worst-case sense.

This section particularly highlights:
1. The **minimum/maximum problem**, including its optimal solution.
2. Algorithms for **general selection**: finding the ith smallest element.
   - A **randomized algorithm** achieving **expected O(n)** time.
   - A **deterministic algorithm** guaranteeing **O(n)** time in the worst case.
3. Insight into analysis techniques for randomized algorithms.

---

## Key Concepts

- **Order Statistics**: The ith smallest element in a set of n elements.
  - **Minimum**: The 1st order statistic.
  - **Maximum**: The nth order statistic.
  - **Median**:
    - For odd `n`, the unique median is at position `i = (n + 1) / 2`.
    - For even `n`, there are two medians at indices `⌊(n + 1) / 2⌋` (lower median) and `⌈(n + 1) / 2⌉` (upper median).
- **Selection Problem**:
  - **Input**: A set `A` of n elements and an integer `i (1 ≤ i ≤ n)`.
  - **Output**: The ith smallest element in `A`.

- **Finding min and max**:
  - Solution with \( \Theta(n) \) comparisons.
  - Optimal simultaneous computation of both min and max using \( \lceil 3n/2 \rceil - 2 \) comparisons.

- **Randomized Algorithms**:
  - Probabilistic algorithms whose performance depends on random choices made during execution.
  - For selection, the **Randomized-Select** algorithm (based on quicksort) achieves \( O(n) \) expected running time.

- **Divide-and-Conquer Strategy**:
  - Key to both randomized and deterministic selection algorithms.
  - Break the problem into smaller subproblems, recursively solve, and combine results.
  - Example: Partitioning in **Randomized-Select** only recurses on **one side** of the partition.

---

## Algorithms and Techniques

### Minimum and Maximum of a Set

#### **Finding a Minimum**
- Compare each element with the current known minimum.
- Algorithm:
  ```plaintext
  1. Set `min = A[1]`.
  2. For each element A[i] (i = 2 to n):
     3. If A[i] < min:
           Update `min = A[i]`.
  4. Return `min`.
  ```
- **Time Complexity**: \( \Theta(n) \), achieved with \( n-1 \) comparisons.
- **Space Complexity**: \( O(1) \).

#### **Simultaneous Min and Max**
- Strategy: Process elements in pairs to reduce comparisons.
- Key Idea:
  1. Compare elements within each pair.
  2. Update current min/max based on the smaller/larger of the pair.
- **Number of Comparisons**: At most \( \lceil 3n/2 \rceil - 2 \).
- **Process**:
  - For odd \( n \), handle the first element separately.
  - For even \( n \), initialize min/max with one comparison from the first two elements.

#### Comparison Summary:
| Task                   | Comparisons      | Optimal? |
|-------------------------|------------------|----------|
| Minimum **or** Maximum | \( n-1 \)        | Yes      |
| Simultaneous Min & Max | \( \lceil 3n/2 \rceil - 2 \) | Yes |

---

### Randomized-Select Algorithm (General Selection)

#### Overview
The **Randomized-Select** algorithm selects the ith smallest element in \( O(n) \) expected time. It uses the same partitioning strategy as **randomized quicksort** but only recurses on one side of the partition.

#### Algorithm Description
1. **Base Case**: If the subarray contains only one element, return it.
2. **Partition**: Randomly partition the array into two subarrays relative to a pivot.
3. **Recursive Case**:
   - If the ith smallest element lies on the low side of the partition, recurse there.
   - If it lies on the high side, adjust `i` and recurse.

#### Pseudocode
```plaintext
RANDOMIZED-SELECT(A, p, r, i)
1. If p == r:
       Return A[p]
2. q = RANDOMIZED-PARTITION(A, p, r)
3. k = q - p + 1  // Number of elements in low partition + pivot
4. If i == k:
       Return A[q]
5. Else if i < k:
       Return RANDOMIZED-SELECT(A, p, q-1, i)
6. Else:
       Return RANDOMIZED-SELECT(A, q+1, r, i - k)
```

#### Complexity
- **Expected Time**: \( O(n) \), due to equal likelihood of partition sizes.
- **Worst Time**: \( O(n^2) \), occurs if partitions are highly unbalanced.
- **Space Complexity**: \( O(\log n) \) due to recursion stack.

---

### Deterministic-Select Algorithm (General Selection)

#### Overview
This algorithm guarantees \( O(n) \) time in the **worst case**. The deterministic-constant partition ensures a good balance for divide-and-conquer.

#### Key Steps
1. Divide input into \( \lceil n/5 \rceil \) groups of size 5 (last group may have fewer elements).
2. Find the "median of each group" using insertion sort.
3. Recursively determine the median-of-medians as a pivot.
4. Partition the array around the pivot and select recursively.

#### Complexity Analysis
- **Worst-Case Time**: \( O(n) \).
- **Space Complexity**: \( O(\log n) \).

---

## Complexity Analysis Table

| Algorithm            | Type        | Best Case | Worst Case    | Expected Case | Space  |
|-----------------------|-------------|-----------|---------------|---------------|--------|
| Randomized-Select     | Randomized  | \( O(n) \) | \( O(n^2) \)   | \( O(n) \)     | \( O(\log n) \) |
| Deterministic-Select  | Deterministic | \( O(n) \) | \( O(n) \)     | \( O(n) \)     | \( O(\log n) \) |
| Simultaneous Min/Max  | Deterministic | \( \Theta(n) \) | \( \Theta(n) \) | \( \Theta(n) \) | \( O(1) \) |

---

## Theorems

### Theorem: \( O(n) \) Expected Time for Randomized-Select
#### Statement:
The **RANDOMIZED-SELECT** algorithm has an **expected running time** of \( O(n) \).
#### Significance:
The algorithm is efficient for practical applications as it achieves linear time on average, regardless of input distribution.

---

## Concrete Examples

### Example: Finding Minimum and Maximum
Given array \( A = [3, 7, 2, 5, 9, 1] \):
1. Compare pairs: (3,7), (2,5), (9,1):
   - \( \text{min = 1}, \, \text{max = 9} \).
2. Total comparisons: \( 3*(3/2) = 9 \) comparisons.

---

These notes cover the critical topics and provide a strong reference base for further study of medians and order statistics.
