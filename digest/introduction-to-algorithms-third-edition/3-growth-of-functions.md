# 3 Growth of Functions

```markdown
# Growth of Functions Study Notes

## Overview
The growth of functions allows us to analyze how algorithms scale with input size (denoted `n`). This analysis focuses on understanding the asymptotic behavior of algorithms, abstracting away constants and smaller-order terms, and comparing algorithms' efficiency in terms of their worst-case, average-case, or best-case running times. Asymptotic notations like Big-Θ (Θ), Big-O (O), and Big-Ω (Ω) are the standard tools for expressing and formalizing this concept.

---

## Key Concepts

- **Order of growth**: Describes how an algorithm's running time or space requirement grows with input size. It's critical when comparing algorithms, as constants and lower-order terms become negligible for sufficiently large inputs.
  
- **Asymptotic analysis**: Focuses on the behavior of a function as the input size (`n`) approaches infinity, simplifying the performance analysis to major terms affecting runtime.

- **Asymptotic notations**:
  - **Big-Θ (Θ):** Describes a tight bound, implying the function grows asymptotically within constant factors of a given function (`g(n)`).
  - **Big-O (O):** Gives an asymptotic upper bound, emphasizing the maximum growth rate.
  - **Big-Ω (Ω):** Represents an asymptotic lower bound, emphasizing the minimum growth rate.

- **Applications of asymptotic analysis**: 
  - Abstracts away constants and focuses on performance for large inputs.
  - Helps compare algorithms' efficiency regardless of implementation details.

---

## Asymptotic Notations

### Big-Θ (Θ) Notation
- **Purpose**: Provides a tight bound for functions.
- **Definition**: A function `f(n)` is Θ(`g(n)`) if there exist constants `c1`, `c2 > 0` and `n₀ > 0` such that:
  \[
  c_1 g(n) \leq f(n) \leq c_2 g(n) \quad \forall n \geq n₀
  \]
- **Significance**: Indicates `g(n)` is an asymptotically tight bound for `f(n)` and represents the core growth component of the algorithm.

- **Example**:
  The quadratic function \( f(n) = \frac{1}{2}n^2 + 3n \):
  - Take constants: \( c_1 = \frac{1}{14} \), \( c_2 = \frac{1}{2} \), \( n_0 = 7 \).
  - Show: \( c_1 n^2 \leq f(n) \leq c_2 n^2 \), thus proving \( f(n) = Θ(n^2) \).

---

### Big-O (O) Notation
- **Purpose**: Provides an upper bound, indicating the maximum growth rate of a function.
- **Definition**: A function `f(n)` is \( O(g(n)) \) if there exist constants \( c > 0 \) and \( n₀ > 0 \) such that:
  \[
  0 \leq f(n) \leq c \cdot g(n) \quad \forall n \geq n₀
  \]
- **Significance**: Describes the worst-case growth and is often used in runtime guarantees.

- **Example**:
  \( n \log n \text{ (merge sort's run time) } \) is \( O(n^2) \). However, it is asymptotically tighter to express as \( Θ(n \log n) \).

---

### Big-Ω (Ω) Notation
- **Purpose**: Provides a lower bound indicating the minimum growth rate of a function.
- **Definition**: A function `f(n)` belongs to \( Ω(g(n)) \) if there exist constants \( c > 0 \) and \( n₀ > 0 \) such that:
  \[
  f(n) \geq c \cdot g(n) \quad \forall n \geq n₀
  \]
- **Significance**: Ensures that the function grows at least as fast as \( g(n) \).

- **Example**:
  Insertion sort's worst-case running time \( f(n) = \frac{1}{2} n^2 + 7n \) is \( Ω(n^2) \) because lower-order terms become negligible as \( n \rightarrow \infty \).

---

## Behavior of Common Functions

### Growth Rates (From Slowest to Fastest)
1. **Constant**: \( O(1) \)
2. **Logarithmic**: \( O(\log n) \)
3. **Linear**: \( O(n) \)
4. **Linearithmic**: \( O(n \log n) \)
5. **Polynomial**: \( O(n^2), O(n^3), \dots, O(n^k) \)
6. **Exponential**: \( O(2^n) \)
7. **Factorial**: \( O(n!) \)

---

## Comparison Table: Common Growth Rates

| Function Class   | Example Algorithm      | Time Complexity  | Relative Growth at Large n  |
|------------------|------------------------|------------------|-----------------------------|
| Constant         | Hash table lookup     | \( O(1) \)       | Slowest (always constant)   |
| Logarithmic      | Binary search         | \( O(\log n) \)  | Extremely efficient         |
| Linear           | Linear search         | \( O(n) \)       | Scales proportionally       |
| Linearithmic     | Merge sort            | \( O(n \log n) \)| Efficient for sorting       |
| Polynomial       | Bubble/insertion sort | \( O(n^2) \)     | Slower as input grows       |
| Exponential      | Recursive Fibonacci   | \( O(2^n) \)     | Impractical for large n     |
| Factorial        | Recursive permutations| \( O(n!) \)      | Fastest growth, least efficient|

---

## Theoretical Insights and Practical Examples

### Polynomial Functions
- **Theorem**: Any polynomial \( p(n) = \sum_{i=0}^d a_i n^i \) where \( a_d > 0 \), is \( Θ(n^d) \). Lower-order (smaller \( i \)) terms and constants \( a_0, \dots, a_{d-1} \) are asymptotically insignificant.

- **Example**:
  \( f(n) = 3n^3 + 5n^2 - 7n + 4 \) is \( Θ(n^3) \).

- **Significance**: This captures why algorithms with different leading terms scale differently.

### Logarithms and Linearithmic Growth
- Algorithms like merge sort (\( Θ(n \log n) \)) or binary search (\( Θ(\log n) \)) are supremely efficient because logarithmic terms grow much slower than polynomial or exponential counterparts.

---

## Applications in Algorithms

### Merge Sort (Time: \( Θ(n \log n) \))
- Employs divide-and-conquer: divides the array, sorts each subarray recursively, and merges them.
- Example pseudocode:
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)
```
- Analysis:
  - Divide: \( O(\log n) \) levels due to halving.
  - Conquer (merge step): Linear \( O(n) \) work per level.
- Total: \( O(n \log n) \).

### Insertion Sort (Time: \( Θ(n^2) \))
- Simple sorting; iteratively builds a sorted array.
- The quadratic nature is derived from nested loops to reinsert items.

---

## Key Takeaways
- Growth of functions is critical for analyzing and comparing algorithmic scalability.
- Asymptotic notations (Θ, O, Ω) provide different ways to bound complexity.
- Polynomial and exponential functions frequently arise in algorithm analysis, with polynomial growth being practical and exponential impractical at scale.
- Efficient sorting algorithms like merge sort (\( Θ(n \log n) \)) outperform simpler approaches like insertion sort (\( Θ(n^2) \)).

Use this reference as a guide for understanding algorithmic efficiency and recognizing when specific algorithms are more suitable depending on the input size and context.
```
