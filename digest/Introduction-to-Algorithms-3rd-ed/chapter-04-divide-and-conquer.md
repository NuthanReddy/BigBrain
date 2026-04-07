# Chapter 4: Divide-and-Conquer

## Overview
This chapter dives deep into the divide-and-conquer paradigm—splitting a problem into smaller subproblems, solving them recursively, and combining the results. It presents two major algorithmic applications (maximum subarray and matrix multiplication) and three methods for solving the recurrences that characterize divide-and-conquer running times: the substitution method, the recursion-tree method, and the master method.

## Key Concepts
- **Divide-and-conquer paradigm**: Three steps at each level of recursion:
  1. **Divide** the problem into smaller subproblems.
  2. **Conquer** the subproblems by solving them recursively (or directly if small enough—the base case).
  3. **Combine** the subproblem solutions into the overall solution.
- **Recurrences**: Equations or inequalities that describe a function in terms of its value on smaller inputs. They naturally characterize divide-and-conquer running times.
- **Technicalities**: Floors, ceilings, and boundary conditions are typically ignored in recurrence formulations because they don't affect the asymptotic solution (justified by Theorem 4.1).

## Algorithms and Techniques

### Maximum-Subarray Problem (Section 4.1)
- **Problem**: Given an array of numbers (some negative), find the contiguous subarray with the largest sum.
- **Motivation**: Modeled as a stock-trading problem—find the best time to buy and sell by transforming prices into daily changes.
- **Brute-force**: Check all Θ(n²) subarrays → Θ(n²) time.
- **Divide-and-conquer solution**:
  - Divide at the midpoint.
  - A maximum subarray is either entirely in the left half, entirely in the right half, or crosses the midpoint.
  - FIND-MAX-CROSSING-SUBARRAY finds the best crossing subarray in Θ(n) time by extending left and right from the midpoint.
  - FIND-MAXIMUM-SUBARRAY recursively solves left and right halves, finds the crossing subarray, and returns the best of the three.
  - **Recurrence**: T(n) = 2T(n/2) + Θ(n), giving T(n) = Θ(n lg n).
- **Note**: A linear-time O(n) solution exists using Kadane's algorithm (Exercise 4.1-5).

### Matrix Multiplication (Section 4.2)
- **Standard algorithm (SQUARE-MATRIX-MULTIPLY)**: Triple nested loop computing cᵢⱼ = Σaᵢₖ·bₖⱼ → Θ(n³) time.
- **Naive divide-and-conquer**: Partition each n×n matrix into four n/2 × n/2 submatrices; perform 8 recursive multiplications and 4 additions.
  - Recurrence: T(n) = 8T(n/2) + Θ(n²) → T(n) = Θ(n³). No improvement!
- **Strassen's algorithm**: The key insight is reducing 8 recursive multiplications to 7 by cleverly constructing 10 auxiliary matrices (S₁–S₁₀) and 7 products (P₁–P₇):
  - Step 1: Partition A, B, C into n/2 × n/2 submatrices — Θ(1) time.
  - Step 2: Create 10 sum/difference matrices S₁–S₁₀ — Θ(n²) time.
  - Step 3: Recursively compute 7 products P₁–P₇ — 7T(n/2) time.
  - Step 4: Compute C₁₁, C₁₂, C₂₁, C₂₂ from the Pᵢ matrices — Θ(n²) time.
  - **Recurrence**: T(n) = 7T(n/2) + Θ(n²) → T(n) = Θ(n^(lg 7)) ≈ Θ(n^2.81).

### Solving Recurrences

#### Substitution Method (Section 4.3)
- **Two steps**: (1) Guess the form of the solution. (2) Use mathematical induction to prove it correct.
- **Example**: T(n) = 2T(⌊n/2⌋) + n. Guess T(n) = O(n lg n), prove T(n) ≤ cn lg n by induction. The key step: T(n) ≤ cn lg n − cn + n ≤ cn lg n for c ≥ 1.
- **Subtlety — subtracting lower-order terms**: When a direct induction proof fails (e.g., T(n) ≤ cn gives cn + 1), try T(n) ≤ cn − d. The extra constant d absorbed in each recursive term provides slack.
- **Pitfall**: Must prove the exact form of the hypothesis (e.g., T(n) ≤ cn), not just T(n) = O(n). Concluding "≤ cn + n = O(n)" is an error.
- **Changing variables**: Transform unfamiliar recurrences (e.g., T(n) = 2T(⌊√n⌋) + lg n) via substitution (m = lg n) into familiar forms.

#### Recursion-Tree Method (Section 4.4)
- Visualize the recurrence as a tree where each node represents the cost of a subproblem.
- Sum costs within each level, then sum across all levels.
- **Example**: T(n) = 3T(n/4) + cn²
  - Tree height: log₄ n. Level i has 3ⁱ nodes, each costing c(n/4ⁱ)².
  - Per-level cost: (3/16)ⁱ · cn². This is a decreasing geometric series.
  - Total: < (16/13)cn² + Θ(n^(log₄ 3)) = O(n²).
- **Example**: T(n) = T(n/3) + T(2n/3) + cn
  - Longest root-to-leaf path has height log₃/₂ n, each full level costs cn.
  - Solution: O(n lg n).
- Best used to generate guesses, then verified by substitution method.

#### Master Method (Section 4.5)
- **Applies to**: T(n) = aT(n/b) + f(n) where a ≥ 1, b > 1.
- **Master Theorem (Theorem 4.1)** — Compare f(n) with n^(log_b a):
  1. **Case 1**: If f(n) = O(n^(log_b a − ε)) for some ε > 0, then T(n) = Θ(n^(log_b a)).
     - The recursive work dominates.
  2. **Case 2**: If f(n) = Θ(n^(log_b a)), then T(n) = Θ(n^(log_b a) · lg n).
     - Work is evenly distributed across levels.
  3. **Case 3**: If f(n) = Ω(n^(log_b a + ε)) for some ε > 0, AND af(n/b) ≤ cf(n) for some c < 1 (regularity condition), then T(n) = Θ(f(n)).
     - The divide/combine work dominates.
- **Gaps**: The theorem does not cover cases where f(n) differs from n^(log_b a) by less than a polynomial factor (e.g., f(n) = n lg n with n^(log_b a) = n).

**Key master method applications**:
| Recurrence | a | b | f(n) | n^(log_b a) | Case | Solution |
|---|---|---|---|---|---|---|
| T(n) = 9T(n/3) + n | 9 | 3 | n | n² | 1 | Θ(n²) |
| T(n) = T(2n/3) + 1 | 1 | 3/2 | 1 | 1 | 2 | Θ(lg n) |
| T(n) = 3T(n/4) + n lg n | 3 | 4 | n lg n | n^0.793 | 3 | Θ(n lg n) |
| T(n) = 2T(n/2) + Θ(n) | 2 | 2 | n | n | 2 | Θ(n lg n) |
| T(n) = 8T(n/2) + Θ(n²) | 8 | 2 | n² | n³ | 1 | Θ(n³) |
| T(n) = 7T(n/2) + Θ(n²) | 7 | 2 | n² | n^2.81 | 1 | Θ(n^(lg 7)) |

## Complexity Analysis

| Algorithm / Problem | Time Complexity | Notes |
|---|---|---|
| Maximum subarray (brute force) | Θ(n²) | Check all pairs |
| Maximum subarray (divide & conquer) | Θ(n lg n) | Same recurrence as merge sort |
| Maximum subarray (Kadane's) | Θ(n) | Non-recursive, linear scan |
| Standard matrix multiply | Θ(n³) | Triple nested loop |
| Recursive matrix multiply (naive) | Θ(n³) | 8 subproblems of size n/2 |
| Strassen's matrix multiply | Θ(n^(lg 7)) ≈ Θ(n^2.81) | 7 subproblems of size n/2 |

## Key Takeaways
- **Divide-and-conquer** is a powerful paradigm: divide into subproblems, conquer recursively, combine. Its running time is naturally expressed as a recurrence.
- **Strassen's algorithm** demonstrates that reducing the number of recursive calls (from 8 to 7) at the cost of extra additions can yield an asymptotically faster algorithm—trading constant-factor overhead for improved recurrence structure.
- **Three methods for solving recurrences**: substitution (guess and verify), recursion trees (visualize and sum), and the master theorem (cookbook for T(n) = aT(n/b) + f(n)). The master theorem is the most convenient but has gaps; the other methods cover those gaps.
- The **master theorem** boils down to comparing f(n) with n^(log_b a): whichever is polynomially larger determines the solution (or they're equal, adding a log factor).
- In the substitution method, **subtracting lower-order terms** from the inductive hypothesis is a common trick to make the proof work when the naive guess fails.
