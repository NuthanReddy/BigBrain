# Chapter 27: Multithreaded Algorithms

## Overview
This chapter extends the algorithmic model from serial computation to parallel computation using dynamic multithreading. It introduces a programming model based on three concurrency keywords—**spawn**, **sync**, and **parallel**—and develops the theoretical framework of **work** and **span** to analyze parallel algorithm performance. The chapter demonstrates how divide-and-conquer algorithms naturally adapt to parallel execution, covering multithreaded matrix multiplication and merge sort as key applications.

## Key Concepts

- **Dynamic multithreading** allows programmers to express logical parallelism without worrying about load balancing, communication, or scheduling—the concurrency platform handles these automatically.
- **Three concurrency keywords**:
  - `spawn`: launches a subroutine asynchronously, allowing the caller to proceed in parallel with the spawned child.
  - `sync`: waits for all spawned children to complete before proceeding.
  - `parallel` (used with `for`): indicates that loop iterations may execute concurrently.
- **Serialization**: removing concurrency keywords from multithreaded pseudocode yields a correct serial algorithm for the same problem.
- **Computation DAG (Directed Acyclic Graph)**: represents the parallel execution structure, where vertices are instructions (grouped into **strands**) and edges represent dependencies (continuation edges, spawn edges, call edges, and return edges).
- **Work (T₁)**: the total time to execute the entire computation on a single processor—equivalent to the sum of all strand execution times.
- **Span (T∞)**: the longest path in the computation DAG, representing the minimum possible execution time with unlimited processors (also called the **critical-path length**).
- **Parallelism**: defined as T₁/T∞, the maximum theoretical speedup achievable. A ratio of at least 10× the number of processors (called **parallel slackness**) generally ensures good speedup.
- **Speedup**: T₁/Tₚ, where Tₚ is running time on P processors. **Linear speedup** occurs when T₁/Tₚ = Θ(P).
- **Determinacy races** (also called data races): occur when two logically parallel instructions access the same memory location and at least one is a write; these lead to nondeterministic behavior and must be avoided.

## Algorithms and Techniques

### P-FIB (Parallel Fibonacci)
- Spawns recursive calls to `P-FIB(n-1)` and `P-FIB(n-2)` in parallel, syncs, then adds results.
- Work: T₁(n) = Θ(φⁿ) (same as serial FIB).
- Span: T∞(n) = Θ(n) (follows the longer recursive path).
- Parallelism: Θ(φⁿ/n)—extremely high, demonstrating that even simple recursive algorithms can expose massive parallelism.

### Parallel Matrix-Vector Multiplication (MAT-VEC)
- Uses `parallel for` to compute each row of the result vector independently.
- A nested `parallel for` implementation is shown, along with a divide-and-conquer auxiliary (MAT-VEC-MAIN-LOOP) that the compiler generates.
- Work: Θ(n²). Span: Θ(lg n). Parallelism: Θ(n²/lg n).

### P-SQUARE-MATRIX-MULTIPLY and P-MATRIX-MULTIPLY-RECURSIVE
- **P-SQUARE-MATRIX-MULTIPLY**: parallelizes the two outer loops of the standard Θ(n³) algorithm.
  - Work: Θ(n³). Span: Θ(n). Parallelism: Θ(n²).
- **P-MATRIX-MULTIPLY-RECURSIVE**: uses divide-and-conquer, partitioning matrices into four n/2 × n/2 submatrices and performing 8 recursive multiplications.
  - Work: T₁(n) = Θ(n³). Span: T∞(n) = Θ(lg² n). Parallelism: Θ(n³/lg² n).
  - The recursive version achieves much higher parallelism than the loop-based version.

### Multithreaded Merge Sort (P-MERGE-SORT)
- Spawns two recursive sorting calls in parallel, then merges using a parallel merge subroutine.
- **P-MERGE**: the key innovation—performs a parallel merge of two sorted arrays using a divide-and-conquer strategy:
  1. Picks the median of the larger array.
  2. Uses binary search to find its position in the smaller array.
  3. Recursively merges the two resulting subproblems in parallel.
- P-MERGE: Work = Θ(n), Span = Θ(lg² n).
- P-MERGE-SORT: Work = Θ(n lg n), Span = Θ(lg³ n), Parallelism = Θ(n/lg² n).

## Complexity Analysis

| Algorithm | Work T₁ | Span T∞ | Parallelism |
|---|---|---|---|
| P-FIB(n) | Θ(φⁿ) | Θ(n) | Θ(φⁿ/n) |
| MAT-VEC (n×n) | Θ(n²) | Θ(lg n) | Θ(n²/lg n) |
| P-SQUARE-MATRIX-MULTIPLY | Θ(n³) | Θ(n) | Θ(n²) |
| P-MATRIX-MULTIPLY-RECURSIVE | Θ(n³) | Θ(lg² n) | Θ(n³/lg² n) |
| P-MERGE (n elements) | Θ(n) | Θ(lg² n) | Θ(n/lg² n) |
| P-MERGE-SORT (n elements) | Θ(n lg n) | Θ(lg³ n) | Θ(n/lg² n) |

**Theorem 27.1 (Greedy Scheduler Bound):** On P processors, a greedy scheduler executes a multithreaded computation with work T₁ and span T∞ in time Tₚ ≤ T₁/P + T∞.

**Corollary 27.2:** A greedy scheduler achieves Tₚ ≤ 2·T₁/P when P ≤ T₁/T∞ (i.e., near-linear speedup when sufficient parallel slackness exists).

**Corollary 27.3 (Work Law):** Tₚ ≥ T₁/P. **(Span Law):** Tₚ ≥ T∞.

## Key Takeaways

- **Work and span** provide a clean, hardware-independent framework for analyzing parallel algorithms: work captures total computation, span captures the inherent sequential bottleneck.
- **Greedy scheduling** guarantees near-optimal performance: with sufficient parallel slackness (parallelism ≫ P), a greedy scheduler achieves near-linear speedup.
- **Divide-and-conquer** naturally maps to multithreaded algorithms—recursion exposes parallelism, and spawn/sync cleanly express it.
- **Parallel merge** is the critical technique for achieving Θ(n lg n) work parallel sorting with high parallelism; a naive sequential merge would bottleneck the span.
- **Avoiding determinacy races** is essential for correctness; the serialization of a correct multithreaded algorithm must also be correct.
