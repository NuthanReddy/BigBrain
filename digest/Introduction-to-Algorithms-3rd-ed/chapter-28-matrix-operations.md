# Chapter 28: Matrix Operations

## Overview
This chapter addresses fundamental matrix computations central to scientific computing: solving systems of linear equations via LUP decomposition, the relationship between matrix multiplication and matrix inversion, and symmetric positive-definite matrices with their application to least-squares approximation. The focus is on practical, numerically stable algorithms rather than purely theoretical constructs.

## Key Concepts

- **Systems of linear equations** Ax = b: the core computational problem, where A is an n×n matrix. When A is nonsingular, a unique solution x = A⁻¹b exists.
- **LUP decomposition**: factors PA = LU where L is unit lower-triangular, U is upper-triangular, and P is a permutation matrix. This is more numerically stable than direct matrix inversion.
- **Forward substitution**: solves Ly = Pb in Θ(n²) time by working from the first equation to the last.
- **Back substitution**: solves Ux = y in Θ(n²) time by working from the last equation to the first.
- **LU decomposition** (without pivoting): a special case where P = I. Works when all leading submatrices have nonzero determinants, but can be numerically unstable.
- **Pivoting**: selecting the element with largest absolute value as the pivot to reduce numerical instability. **Partial pivoting** (permuting rows only) is the most common strategy.
- **Schur complement**: after eliminating the first variable, the remaining (n-1)×(n-1) system involves the Schur complement S = A' - vwᵀ/a₁₁, a key concept in the recursive structure of Gaussian elimination.
- **Symmetric positive-definite (SPD) matrices**: matrices A where xᵀAx > 0 for all nonzero vectors x. They arise frequently in applications (e.g., covariance matrices, finite element methods).
- **Cholesky decomposition**: for SPD matrices, A = LLᵀ where L is lower-triangular with positive diagonal entries. More efficient than general LUP decomposition.
- **Least-squares approximation**: for overdetermined systems (more equations than unknowns), finds x̂ minimizing ‖Ax - b‖² by solving the normal equations AᵀAx̂ = Aᵀb.

## Algorithms and Techniques

### LUP-SOLVE(L, U, π, b)
- Combines forward substitution (lines 3-4) and back substitution (lines 5-6).
- Takes L, U, permutation array π, and vector b; returns solution x.
- Running time: Θ(n²).

### LU-DECOMPOSITION(A)
- Computes L and U in place using Gaussian elimination without pivoting.
- Iteratively computes each column of L and row of U via the Schur complement.
- Running time: Θ(n³).

### LUP-DECOMPOSITION(A)
- Extends LU decomposition with partial pivoting for numerical stability.
- At each step, selects the row with the largest absolute value in the current column as the pivot, swaps rows, then performs elimination.
- Running time: Θ(n³).
- In practice, LUP decomposition is preferred over direct inversion due to better numerical stability.

### Matrix Inversion via Matrix Multiplication
- **Theorem 28.1**: if we can multiply two n×n matrices in time M(n), then we can compute the inverse of a nonsingular n×n matrix in time O(M(n)), provided M(n) satisfies a regularity condition (M(n) = Ω(n²) and M(3n) ≤ c·M(n) for some constant c < 27).
- The proof uses a block-matrix recursive decomposition, computing A⁻¹ via Schur complements and matrix multiplications.
- **Theorem 28.2** (converse): matrix multiplication can be reduced to matrix inversion, so the two problems are computationally equivalent (up to constant factors with Strassen-like algorithms).

### Least-Squares Approximation
- Given an overdetermined system Ax = b (A is m×n with m > n, full column rank), the pseudoinverse solution is x̂ = (AᵀA)⁻¹Aᵀb.
- The matrix AᵀA is symmetric positive-definite when A has full column rank.
- Solved efficiently using Cholesky decomposition of AᵀA.

## Complexity Analysis

| Operation | Time Complexity |
|---|---|
| Forward/Back substitution | Θ(n²) |
| LU decomposition | Θ(n³) |
| LUP decomposition | Θ(n³) |
| Solving Ax = b via LUP | Θ(n³) |
| Matrix inversion | O(M(n)) where M(n) is matrix multiplication time |
| Cholesky decomposition | Θ(n³) |
| Least-squares via normal equations | Θ(n²m + n³) for m×n system |

**Lemma 28.3**: If A is SPD, then every leading submatrix of A is SPD.

**Lemma 28.4**: If A is SPD, then a₁₁ > 0 and the Schur complement with respect to a₁₁ is also SPD.

**Lemma 28.5 (Cholesky decomposition)**: If A is an n×n SPD matrix, there exists a unique lower-triangular matrix L with positive diagonal entries such that A = LLᵀ.

**Corollary 28.6**: The determinant of a symmetric positive-definite matrix is positive.

## Key Takeaways

- **LUP decomposition** is the workhorse for solving linear systems: factor once in Θ(n³), then solve for any right-hand side b in Θ(n²). This is far more efficient than recomputing for each b.
- **Pivoting is essential** for numerical stability in practice—LU decomposition without pivoting can amplify rounding errors dramatically.
- **Matrix inversion and matrix multiplication are computationally equivalent**: any improvement in one (e.g., Strassen's O(n^2.81) algorithm) automatically yields an improvement in the other.
- **Symmetric positive-definite matrices** enjoy special structure that enables the more efficient and stable Cholesky decomposition (A = LLᵀ), which requires roughly half the work of general LUP decomposition.
- **Least-squares fitting** reduces to solving SPD systems via the normal equations, connecting matrix decomposition to practical statistical and engineering applications.
