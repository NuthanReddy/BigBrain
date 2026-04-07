# Chapter 15: Dynamic Programming

## Overview
Dynamic programming solves optimization problems by breaking them into overlapping subproblems, solving each subproblem only once, and storing results in a table to avoid redundant computation. Unlike divide-and-conquer, which partitions problems into disjoint subproblems, dynamic programming exploits the fact that subproblems recur, transforming exponential-time recursive algorithms into efficient polynomial-time solutions. The chapter introduces the method through four canonical problems: rod cutting, matrix-chain multiplication, longest common subsequence (LCS), and optimal binary search trees.

## Key Concepts

- **Four-step development method**: (1) Characterize the structure of an optimal solution, (2) recursively define the value of an optimal solution, (3) compute the optimal value bottom-up (or top-down with memoization), (4) construct an optimal solution from the computed information.
- **Optimal substructure**: A problem exhibits optimal substructure if an optimal solution contains within it optimal solutions to subproblems. This is verified using a "cut-and-paste" argument: if a subproblem solution were not optimal, replacing it would improve the overall solution, yielding a contradiction.
- **Overlapping subproblems**: The recursive solution to the problem solves the same subproblems repeatedly. The total number of distinct subproblems is typically polynomial in the input size, even though a naive recursion tree is exponentially large.
- **Top-down with memoization**: Write a recursive solution naturally, but cache results in a table; on each call, check whether the result is already stored before computing it.
- **Bottom-up method**: Sort subproblems by size and solve them smallest-first; when a subproblem is reached, all prerequisite subproblems are already solved. Often has better constant factors due to no recursion overhead.
- **Subproblem graph**: A directed graph where each vertex is a distinct subproblem and edges represent direct dependencies. The running time of a DP algorithm is often linear in the number of vertices and edges of this graph.
- **Independence of subproblems**: For DP to work, subproblems must be independent (they do not share resources). The longest simple path problem fails this requirement because using vertices in one subproblem prevents their use in another.
- **Reconstructing solutions**: Store the choice made at each subproblem in an auxiliary table (e.g., s[i,j]) to reconstruct the actual optimal solution in addition to its value.

## Algorithms and Techniques

### 1. Rod Cutting
- **Problem**: Given a rod of length n and a price table p[1..n], determine cuts that maximize revenue.
- **Recurrence**: r_n = max_{1 ≤ i ≤ n} (p_i + r_{n−i}), with r_0 = 0.
- **Naive CUT-ROD**: Exponential time T(n) = 2^n due to recomputing the same subproblems.
- **MEMOIZED-CUT-ROD**: Top-down recursive approach with an array r[0..n] initialized to −∞; returns cached results on revisits.
- **BOTTOM-UP-CUT-ROD**: Iterates j = 1 to n, computing r[j] = max_{1 ≤ i ≤ j} (p[i] + r[j−i]). Both approaches run in Θ(n²).
- **EXTENDED-BOTTOM-UP-CUT-ROD**: Also records s[j] (the optimal first-piece size) to enable solution reconstruction via PRINT-CUT-ROD-SOLUTION.

### 2. Matrix-Chain Multiplication
- **Problem**: Given matrices A₁, A₂, ..., Aₙ with dimensions p₀×p₁, p₁×p₂, ..., pₙ₋₁×pₙ, find a parenthesization that minimizes total scalar multiplications.
- **Recurrence**: m[i,j] = 0 if i = j; otherwise m[i,j] = min_{i ≤ k < j} {m[i,k] + m[k+1,j] + p_{i−1}·p_k·p_j}.
- **Number of parenthesizations**: P(n) = Ω(4^n / n^{3/2}) (Catalan numbers), so brute force is impractical.
- **MATRIX-CHAIN-ORDER**: Bottom-up algorithm filling table m[1..n, 1..n] by increasing chain length l = 2 to n. Also stores s[i,j] = k for solution reconstruction.
- **PRINT-OPTIMAL-PARENS**: Recursively prints the optimal parenthesization using the s table.
- **MEMOIZED-MATRIX-CHAIN / LOOKUP-CHAIN**: Top-down memoized version achieving the same O(n³) time.

### 3. Longest Common Subsequence (LCS)
- **Problem**: Given sequences X = ⟨x₁, ..., xₘ⟩ and Y = ⟨y₁, ..., yₙ⟩, find a maximum-length common subsequence.
- **Theorem 15.1 (Optimal substructure)**: If x_m = y_n, the last LCS element is x_m = y_n and the rest is an LCS of X_{m−1} and Y_{n−1}. If x_m ≠ y_n, the LCS is the longer of LCS(X_{m−1}, Y) and LCS(X, Y_{n−1}).
- **Recurrence**: c[i,j] = 0 if i=0 or j=0; c[i−1,j−1]+1 if x_i = y_j; max(c[i−1,j], c[i,j−1]) otherwise.
- **LCS-LENGTH**: Fills tables c[0..m, 0..n] and b[1..m, 1..n] in row-major order. The b table stores directional arrows ("↖", "↑", "←") for backtracking.
- **PRINT-LCS**: Traces the b table from b[m,n] back to reconstruct the LCS in O(m+n) time.
- **Space optimization**: The b table can be eliminated; only two rows of c are needed to compute the LCS length, reducing space to O(min(m,n)).

### 4. Optimal Binary Search Trees
- **Problem**: Given n sorted keys k₁ < k₂ < ... < kₙ with search probabilities p_i, and n+1 dummy keys d₀, ..., dₙ with probabilities q_i, construct a BST minimizing expected search cost.
- **Expected cost**: E[search cost in T] = 1 + Σ depth_T(k_i)·p_i + Σ depth_T(d_i)·q_i.
- **Recurrence**: e[i,j] = q_{i−1} if j = i−1; otherwise min_{i ≤ r ≤ j} {e[i,r−1] + e[r+1,j] + w(i,j)}, where w(i,j) = Σ_{l=i}^{j} p_l + Σ_{l=i−1}^{j} q_l.
- **Weight computation**: w[i,j] = w[i,j−1] + p_j + q_j, computed incrementally in Θ(1) per entry.
- **OPTIMAL-BST**: Bottom-up algorithm computing e[1..n+1, 0..n], w[1..n+1, 0..n], and root[1..n, 1..n] tables. Structurally similar to MATRIX-CHAIN-ORDER.
- **Knuth's optimization** (Exercise 15.5-4): Using the property root[i,j−1] ≤ root[i,j] ≤ root[i+1,j], the algorithm can be improved to Θ(n²) time.

## Complexity Analysis

| Algorithm | Time Complexity | Space Complexity |
|---|---|---|
| CUT-ROD (naive) | Θ(2^n) | Θ(n) stack depth |
| MEMOIZED-CUT-ROD | Θ(n²) | Θ(n) |
| BOTTOM-UP-CUT-ROD | Θ(n²) | Θ(n) |
| MATRIX-CHAIN-ORDER | Θ(n³) | Θ(n²) |
| MEMOIZED-MATRIX-CHAIN | O(n³) | Θ(n²) |
| RECURSIVE-MATRIX-CHAIN | Ω(2^n) | Θ(n) stack depth |
| LCS-LENGTH | Θ(mn) | Θ(mn) (reducible to Θ(min(m,n))) |
| PRINT-LCS | O(m+n) | O(m+n) stack depth |
| OPTIMAL-BST | Θ(n³) | Θ(n²) |

- **Key theorem**: The running time of a DP algorithm is typically proportional to the number of vertices times the time per vertex in the subproblem graph, which equals the sum of out-degrees — i.e., it is linear in the number of vertices and edges of the subproblem graph.

## Key Takeaways

- **Two hallmarks for DP applicability**: A problem must exhibit both optimal substructure and overlapping subproblems. Optimal substructure alone may suggest a greedy approach instead (Chapter 16).
- **Top-down vs. bottom-up**: Both yield the same asymptotic running time. Bottom-up is generally faster due to lower overhead; top-down with memoization can be advantageous when not all subproblems need to be solved.
- **Exponential to polynomial**: Dynamic programming transforms naive exponential-time recursive algorithms into polynomial-time solutions by caching subproblem results — a time-memory trade-off that can yield dramatic speedups.
- **Subproblem independence matters**: The longest simple path problem illustrates that when subproblems share resources (vertices), optimal substructure breaks down and DP does not apply — the problem is NP-complete.
- **Practice the four-step method**: Characterize optimal substructure → define the recurrence → compute bottom-up → reconstruct the solution. This disciplined framework applies to a wide range of optimization problems including edit distance, sequence alignment, and planning problems.
