# Chapter 3: Growth of Functions

## Overview
This chapter formalizes the asymptotic notation introduced informally in Chapter 2 and catalogs the standard mathematical functions that arise in algorithm analysis. It provides the precise definitions of Θ, O, Ω, o, and ω notations, establishes their properties, and reviews floors, ceilings, logarithms, exponentials, factorials, Fibonacci numbers, and the iterated logarithm function.

## Key Concepts

### Asymptotic Notations (Section 3.1)

- **Θ-notation (Theta)** — Asymptotically tight bound:
  - Θ(g(n)) = {f(n) : ∃ positive constants c₁, c₂, n₀ such that 0 ≤ c₁g(n) ≤ f(n) ≤ c₂g(n) for all n ≥ n₀}
  - f(n) is "sandwiched" between c₁g(n) and c₂g(n) for sufficiently large n.
  - Example: ½n² − 3n = Θ(n²) (choose c₁ = 1/14, c₂ = 1/2, n₀ = 7).

- **O-notation (Big-Oh)** — Asymptotic upper bound:
  - O(g(n)) = {f(n) : ∃ positive constants c, n₀ such that 0 ≤ f(n) ≤ cg(n) for all n ≥ n₀}
  - Gives an upper bound to within a constant factor. Note: Θ(g(n)) ⊆ O(g(n)).
  - Bounding the worst-case running time with O-notation bounds the running time on every input.

- **Ω-notation (Big-Omega)** — Asymptotic lower bound:
  - Ω(g(n)) = {f(n) : ∃ positive constants c, n₀ such that 0 ≤ cg(n) ≤ f(n) for all n ≥ n₀}
  - Stating a running time is Ω(g(n)) means no input causes the algorithm to run faster than cg(n).

- **Theorem 3.1**: f(n) = Θ(g(n)) if and only if f(n) = O(g(n)) and f(n) = Ω(g(n)).

- **o-notation (little-oh)** — Upper bound that is NOT tight:
  - For **any** positive constant c > 0, 0 ≤ f(n) < cg(n) for all sufficiently large n.
  - Equivalently: lim(n→∞) f(n)/g(n) = 0.
  - Example: 2n = o(n²), but 2n² ≠ o(n²).

- **ω-notation (little-omega)** — Lower bound that is NOT tight:
  - f(n) ∈ ω(g(n)) ⟺ g(n) ∈ o(f(n)).
  - Equivalently: lim(n→∞) f(n)/g(n) = ∞.

- **Asymptotic notation in equations**: When Θ/O/Ω appears in a formula, it represents an anonymous function in that set. On the right-hand side of an equation, "=" means set membership. On the left-hand side, it means "for any function chosen on the left, there exists a function on the right making it valid."

### Properties of Asymptotic Notations
- **Transitivity**: Holds for all five notations (Θ, O, Ω, o, ω).
- **Reflexivity**: f(n) = Θ(f(n)), f(n) = O(f(n)), f(n) = Ω(f(n)).
- **Symmetry**: f(n) = Θ(g(n)) ⟺ g(n) = Θ(f(n)).
- **Transpose symmetry**: f(n) = O(g(n)) ⟺ g(n) = Ω(f(n)); f(n) = o(g(n)) ⟺ g(n) = ω(f(n)).
- **Analogy to real numbers**: O ↔ ≤, Ω ↔ ≥, Θ ↔ =, o ↔ <, ω ↔ >.
- **Trichotomy does NOT hold**: Not all functions are asymptotically comparable (e.g., n vs. n^(1+sin n)).

### Standard Notations and Common Functions (Section 3.2)

- **Floors and ceilings**: ⌊x⌋ and ⌈x⌉ with identities like ⌈n/2⌉ + ⌊n/2⌋ = n.
- **Modular arithmetic**: a mod n = a − n⌊a/n⌋.
- **Polynomials**: p(n) = Σaᵢnⁱ with degree d satisfies p(n) = Θ(n^d) when a_d > 0.
- **Exponentials**: aⁿ grows faster than any polynomial nᵇ for a > 1 (i.e., nᵇ = o(aⁿ)). Key approximation: eˣ ≥ 1 + x with equality only at x = 0.
- **Logarithms**: lg n = log₂ n, ln n = logₑ n. Changing base changes by a constant factor: log_b(a) = log_c(a) / log_c(b). Important identity: a^(log_b c) = c^(log_b a).
- **Polylogarithmic vs. polynomial**: lgᵇ n = o(nᵃ) for any constant a > 0—any positive polynomial grows faster than any polylogarithmic function.
- **Factorials**: n! with Stirling's approximation: n! = √(2πn)(n/e)ⁿ(1 + Θ(1/n)). Key results: n! = o(nⁿ), n! = ω(2ⁿ), lg(n!) = Θ(n lg n).
- **Iterated logarithm (lg★ n)**: The number of times you must take lg before the result drops to ≤ 1. Extremely slow-growing: lg★(2^65536) = 5. For all practical input sizes, lg★ n ≤ 5.
- **Fibonacci numbers**: Defined by F₀ = 0, F₁ = 1, Fᵢ = Fᵢ₋₁ + Fᵢ₋₂. Closed form: Fᵢ = (φⁱ − ψⁱ)/√5 where φ = (1+√5)/2 ≈ 1.618 (golden ratio) and ψ = (1−√5)/2 ≈ −0.618. Fibonacci numbers grow exponentially.

## Algorithms and Techniques
This chapter is primarily theoretical and does not introduce new algorithms. Instead, it provides the mathematical toolkit for analyzing algorithms:
- How to formally prove that a function belongs to Θ, O, or Ω of another function.
- How to use asymptotic notation within equations and inequalities to simplify recurrences.
- The standard mathematical functions (logarithms, exponentials, factorials, etc.) needed throughout the rest of the book.

## Complexity Analysis
- **General polynomial**: Any degree-d polynomial p(n) = Θ(n^d).
- **Growth hierarchy** (from slowest to fastest): 1, lg★ n, lg lg n, lg n, lgᵏ n, n^ε (0 < ε < 1), n, n lg n, n², n³, ..., 2ⁿ, n!, nⁿ.
- **Key inequalities**:
  - nᵇ = o(aⁿ) for all b and a > 1 (exponentials dominate polynomials).
  - lgᵇ n = o(nᵃ) for all b and a > 0 (polynomials dominate polylogarithms).
  - n! = ω(2ⁿ) and n! = o(nⁿ).

## Key Takeaways
- **Θ, O, and Ω** provide precise mathematical tools for describing algorithm efficiency; Θ is the strongest (tight bound), while O and Ω give one-sided bounds.
- **Theorem 3.1** is the bridge: proving both O and Ω establishes Θ.
- **Asymptotic notation in equations** is a powerful shorthand—it represents anonymous functions and allows chaining equalities at different levels of detail.
- The **growth hierarchy** of standard functions is essential knowledge: constants < logarithmic < polynomial < exponential < factorial.
- The **iterated logarithm** lg★ is so slow-growing that it is effectively constant (≤ 5) for any conceivable input size, yet it still appears in the analysis of certain advanced data structures (e.g., union-find).
