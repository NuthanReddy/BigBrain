# 3 Growth of Functions

```markdown
# Study Notes: Growth of Functions (Section 3, Introduction to Algorithms, 3rd Edition)

## Overview
The growth of functions is foundational to understanding the efficiency of algorithms, as it focuses on how an algorithm's running time or resource usage increases with input size, particularly for large inputs. This chapter introduces **asymptotic analysis**, which simplifies the complexity of algorithms by ignoring constant factors and lower-order terms. Such analysis relies on standard **asymptotic notations** to express bounds (upper, lower, and tight) on function growth.

By abstracting away fine-grained details, asymptotic analysis enables comparisons between algorithms and helps identify the most efficient one for large inputs. This study note systematically covers the definitions, properties, and examples of asymptotic notations including Big-Theta (Θ), Big-O, and Big-Omega (Ω).

---

## Key Concepts
- **Order of Growth**: Measures the efficiency of an algorithm as a function of input size `n`. This is central to determining the algorithm’s performance for large inputs.
  
- **Asymptotic Analysis**: A technique to study an algorithm’s running time (or space usage) as `n` approaches infinity. It focuses only on the dominant term, ignoring constants and lower-order terms.

- **Asymptotic Notations**:
  - **Θ-notation (Theta)**: Describes tight bounds on growth, meaning a function is bounded both above and below by another function within constant factors.
  - **O-notation (Big-O)**: Provides an asymptotic upper bound, describing the worst-case growth of a function.
  - **Ω-notation (Big-Omega)**: Provides an asymptotic lower bound, describing the best-case growth of a function.

- **Asymptotic Tight Bound**: If a function is both O(g(n)) and Ω(g(n)), it is said to have a tight bound described by Θ(g(n)).

- **Dominant Term**: For large `n`, the term with the highest growth rate dominates, so lower-order terms and multiplicative constants can be ignored.

- **Abuse of Notation**: Occasionally, asymptotic notation may be extended to domains other than `n ∈ ℕ` (e.g., real numbers) or for non-runtime measures (e.g., space usage).

---

## Algorithms and Techniques

### Θ-notation (Big-Theta)
#### Definition and Explanation:
- Θ-notation defines a tight bound on a function `f(n)` in terms of a reference function `g(n)`. Formally:
  - `f(n) ∈ Θ(g(n))` if there exist positive constants `c1`, `c2`, and `n0` such that for all `n ≥ n0`:
    ```
    c1 * g(n) ≤ f(n) ≤ c2 * g(n)
    ```
- This means that `f(n)` grows at the same rate as `g(n)` within constant factors.

#### Significance:
- Captures the asymptotic behavior of an algorithm's runtime, both in the worst and best case.
- Eliminates the need to analyze exact runtimes, focusing instead on trends for large `n`.

#### Example:
For the quadratic function `f(n) = (1/2)n^2 + 3n`, it can be shown that:
- `f(n)` is in Θ(n²) because constants `c1` and `c2` exist that bound `f(n)` between `c1 * n²` and `c2 * n²` for all sufficiently large `n`.

---

### O-notation (Big-O)
#### Definition and Explanation:
- O-notation provides an asymptotic upper bound for a function `f(n)` in relation to a reference function `g(n)`. Formally:
  - `f(n) ∈ O(g(n))` if there exist positive constants `c` and `n0` such that for all `n ≥ n0`:
    ```
    f(n) ≤ c * g(n)
    ```
- Emphasizes the **worst-case growth** of `f(n)`.

#### Significance:
- Allows us to make guarantees that the algorithm will never exceed a particular growth rate for large enough `n`.

#### Example:
For the quadratic function `f(n) = (1/2)n^2 + 3n`, it is clear that:
- `f(n) ∈ O(n²)` because `f(n)` never exceeds a constant multiple of `n²` for all sufficiently large `n`.
- However, "informally" claiming `n ∈ O(n²)` implies linear growth (`n`) is part of O(quadratic growth) due to modular properties of O-notation. This highlights the importance of clarity in bounds.

---

### Ω-notation (Big-Omega)
#### Definition and Explanation:
- Ω-notation provides an asymptotic lower bound for `f(n)` in relation to `g(n)`. Formally:
  - `f(n) ∈ Ω(g(n))` if there exist positive constants `c` and `n0` such that for all `n ≥ n0`:
    ```
    f(n) ≥ c * g(n)
    ```
- Emphasizes the **best-case growth** of `f(n)`.

#### Significance:
- Used to identify the **minimum guaranteed performance** of an algorithm in the best possible case.

#### Example:
For the quadratic function `f(n) = (1/2)n^2 + 3n`, we conclude:
- `f(n) ∈ Ω(n²)` because there exists a constant multiple of `n²` below which `f(n)` does not fall for all sufficiently large `n`.

---

## Complexity Analysis
The following table compares the asymptotic growth bounds:

| **Notation** | **Definition**                                             | **Use Case**                     |
|--------------|-------------------------------------------------------------|-----------------------------------|
| Θ(g(n))      | Upper *and* lower bound (tight bound on `f(n)`)             | Precise asymptotic characterization |
| O(g(n))      | Upper bound only (no claim about lower bound)               | Describes worst-case complexity   |
| Ω(g(n))      | Lower bound only (no claim about upper bound)               | Describes best-case complexity    |

### Example of Relationships:
1. If `f(n) ∈ Θ(g(n))`, then `f(n) ∈ O(g(n))` **and** `f(n) ∈ Ω(g(n))`.
2. However, `f(n) ∈ O(g(n))` does **not** imply `f(n) ∈ Ω(g(n))`.

---

## Common Theorems
### Polynomial Growth
**Theorem**: For any polynomial `p(n) = a_d*n^d + a_(d-1)*n^(d-1) + ... + a_0` where `a_d > 0`, we have:
- `p(n) ∈ Θ(n^d)`.

**Explanation**:
- Higher-order terms dominate lower-order terms as `n` becomes large.
- The leading coefficient has a constant-factor impact and is ignored in asymptotics.

---

## Summary
- Use Θ when both bounds matter, O for worst-case, and Ω for best-case guarantees.
- Constants and low-order terms are insignificant for asymptotic growth.
- A rigorous understanding of asymptotic notations helps accurately analyze algorithmic efficiency and choose the right tool for large-scale problems.

These foundational principles underlie all further analysis of algorithms and data structures.
```
