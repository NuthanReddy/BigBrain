# Chapter 7: Quicksort

## Overview

Quicksort is a highly efficient comparison-based sorting algorithm that uses the divide-and-conquer paradigm. Despite having a worst-case running time of Θ(n²), it is often the practical sorting algorithm of choice because its expected running time is Θ(n lg n) with very small constant factors. It also sorts **in place** (requiring only O(lg n) additional stack space) and performs well in virtual-memory environments.

The chapter covers the core algorithm and its PARTITION subroutine (Section 7.1), intuitive and formal performance analysis for worst-case, best-case, and average-case scenarios (Sections 7.2 and 7.4), and a randomized variant that eliminates dependence on input ordering (Section 7.3).

## Key Concepts

- **Divide-and-conquer structure**: Quicksort partitions the array around a *pivot* element, recursively sorts the two resulting subarrays, and requires no combine step since the subarrays are sorted in place.
- **Pivot selection**: The standard PARTITION procedure uses the last element A[r] as the pivot. The randomized variant selects a uniformly random element, ensuring no particular input triggers worst-case behavior.
- **In-place partitioning**: The PARTITION procedure (Lomuto's scheme) rearranges elements using only constant extra memory by maintaining two regions — elements ≤ pivot and elements > pivot — separated by index pointers.
- **Loop invariant for PARTITION**: At the start of each iteration of the for loop, three regions are maintained:
  1. A[p..i] contains elements ≤ x (the pivot).
  2. A[i+1..j−1] contains elements > x.
  3. A[r] = x (the pivot itself).
  This invariant is proved via initialization, maintenance, and termination arguments.
- **Performance depends on partition balance**: Balanced splits yield O(n lg n); maximally unbalanced splits yield Θ(n²). The key insight is that even moderately unbalanced splits (e.g., 9-to-1) still produce O(n lg n) performance.
- **Comparison-driven analysis**: The total running time is O(n + X), where X is the total number of element comparisons across all PARTITION calls (Lemma 7.1). Analyzing X via indicator random variables yields the expected-case bound.

## Algorithms and Techniques

### QUICKSORT(A, p, r)

The main recursive procedure:

1. **Base case**: If p ≥ r, the subarray has zero or one element — do nothing.
2. **Partition**: Call PARTITION(A, p, r) to get pivot index q, placing A[q] in its final sorted position.
3. **Recurse**: Recursively sort A[p..q−1] (elements ≤ pivot) and A[q+1..r] (elements > pivot).
4. **No combine step** is needed — the array is sorted in place after the recursive calls return.

Initial invocation: QUICKSORT(A, 1, A.length).

### PARTITION(A, p, r) — Lomuto's Scheme

Rearranges A[p..r] in place around pivot x = A[r]:

1. Set x = A[r] (pivot), i = p − 1.
2. Scan j from p to r − 1:
   - If A[j] ≤ x: increment i, then swap A[i] with A[j] (grow the "≤ pivot" region).
   - If A[j] > x: just advance j (the element naturally falls into the "> pivot" region).
3. After the loop, swap A[i+1] with A[r] to place the pivot between the two regions.
4. Return i + 1 (the pivot's final index).

**Running time**: Θ(n) for a subarray of size n = r − p + 1.

### RANDOMIZED-PARTITION(A, p, r)

Eliminates input-dependent worst-case behavior:

1. Choose i = RANDOM(p, r) uniformly at random.
2. Swap A[r] with A[i] — this makes the pivot a random element.
3. Return PARTITION(A, p, r).

### RANDOMIZED-QUICKSORT(A, p, r)

Identical to QUICKSORT but calls RANDOMIZED-PARTITION instead of PARTITION. This ensures the pivot is chosen randomly at each level, making the expected running time O(n lg n) regardless of the input ordering.

### Hoare's Partition (Problem 7-1)

The original partition algorithm by C.A.R. Hoare uses two pointers that scan inward from both ends of the subarray. It selects A[p] as the pivot and uses two `repeat` loops: one scanning rightward until finding an element ≥ x, and one scanning leftward until finding an element ≤ x. Elements are swapped when both pointers have stopped, and the procedure terminates when the pointers cross, returning the crossing index j (where p ≤ j < r).

### Tail-Recursive Quicksort (Problem 7-4)

Replaces the second recursive call with an iterative loop (`p = q + 1` in a while loop), reducing stack usage. By always recursing on the *smaller* subarray and iterating on the larger, the worst-case stack depth can be reduced from Θ(n) to Θ(lg n).

### Three-Way Partition — PARTITION′ (Problem 7-2)

A variant for handling equal elements efficiently. Returns two indices q and t such that:
- A[p..q−1] contains elements < pivot,
- A[q..t] contains elements = pivot,
- A[t+1..r] contains elements > pivot.

Recursion is only applied to the "< pivot" and "> pivot" regions, avoiding redundant work on equal elements.

## Complexity Analysis

### Time Complexity

| Scenario | Recurrence | Solution |
|---|---|---|
| **Worst case** | T(n) = T(n−1) + T(0) + Θ(n) | **Θ(n²)** |
| **Best case** | T(n) = 2T(n/2) + Θ(n) | **Θ(n lg n)** |
| **Expected (randomized)** | Analyzed via comparisons | **Θ(n lg n)** |

**Worst-case analysis (Section 7.4.1)**:

The worst case arises when every partition produces maximally unbalanced splits (one subproblem of size n−1, one of size 0). The recurrence is:

> T(n) = max₀≤q≤n−1 [T(q) + T(n−q−1)] + Θ(n)

Using the substitution method with the guess T(n) ≤ cn², the expression q² + (n−q−1)² is maximized at the endpoints q = 0 or q = n−1 (since its second derivative with respect to q is positive). This yields T(n) ≤ cn² − c(2n−1) + Θ(n) ≤ cn² for large enough c. A matching lower bound Ω(n²) confirms T(n) = Θ(n²).

This occurs, for example, when the input is already sorted (each partition produces one empty subarray).

**Best-case analysis (Section 7.2)**:

When PARTITION always splits evenly — one subproblem of size ⌊n/2⌋ and one of size ⌈n/2⌉ − 1 — the recurrence T(n) = 2T(n/2) + Θ(n) solves to Θ(n lg n) by case 2 of the Master Theorem (Theorem 4.1).

**Any constant-proportion split is still O(n lg n)**: Even a 9-to-1 split gives T(n) = T(9n/10) + T(n/10) + cn. The recursion tree has depth Θ(lg n) (between log₁₀ n and log₁₀/₉ n), with cost ≤ cn at each level, yielding O(n lg n). In general, *any* split with constant proportionality results in O(n lg n).

**Expected-case analysis of RANDOMIZED-QUICKSORT (Section 7.4.2)**:

The analysis counts the total number of comparisons X across all PARTITION calls.

- **Lemma 7.1**: The running time of QUICKSORT is O(n + X), where X is the total comparisons in line 4 of PARTITION (since there are at most n calls to PARTITION, each doing O(1) work plus the comparison loop).

- Rename sorted elements as z₁ < z₂ < ⋯ < zₙ. Define Zᵢⱼ = {zᵢ, zᵢ₊₁, …, zⱼ}.

- **Key insight**: zᵢ and zⱼ are compared if and only if the *first* pivot chosen from Zᵢⱼ is either zᵢ or zⱼ. If any element strictly between them is chosen first, they are separated into different partitions and never compared.

- Since |Zᵢⱼ| = j − i + 1, each element is equally likely to be the first pivot, so:

  > Pr{zᵢ is compared to zⱼ} = 2 / (j − i + 1)

- The expected total comparisons:

  > E[X] = Σᵢ₌₁ⁿ⁻¹ Σⱼ₌ᵢ₊₁ⁿ 2/(j−i+1) < Σᵢ₌₁ⁿ⁻¹ Σₖ₌₁ⁿ 2/k = Σᵢ₌₁ⁿ⁻¹ O(lg n) = **O(n lg n)**

  (Using the harmonic series bound Σ 1/k = O(lg n).)

Combined with the best-case lower bound Ω(n lg n), the expected running time is **Θ(n lg n)**.

### Space Complexity

- **In place**: Quicksort requires no auxiliary arrays; partitioning is done in place.
- **Stack space**: O(n) in the worst case for the recursive call stack, but O(lg n) if tail-call optimization is used (recurse on the smaller partition, iterate on the larger — Problem 7-4).

### Important Insight: Alternating Good and Bad Splits

If bad splits (worst-case: n−1 to 0) and good splits (best-case: even halves) alternate at successive recursion levels, the combined cost of two levels is Θ(n) + Θ(n−1) = Θ(n), which is equivalent to a single good split. The Θ(n−1) cost of the bad split is "absorbed" into the Θ(n) cost of the good split. Therefore, alternating good/bad splits still yields an overall O(n lg n) running time. This is why the average case is so much closer to the best case.

## Key Takeaways

- **Quicksort is Θ(n lg n) expected, Θ(n²) worst-case.** The worst case is rare in practice and can be mitigated by randomized pivot selection, which makes no specific input trigger worst-case behavior.
- **PARTITION is the engine of quicksort.** Its efficiency (Θ(n) per call) and the balance of the split it produces determine overall performance. The Lomuto scheme is elegant and easy to analyze; Hoare's original scheme is slightly more efficient in practice.
- **Randomization decouples performance from input distribution.** RANDOMIZED-QUICKSORT achieves Θ(n lg n) expected time for *all* inputs by choosing pivots uniformly at random. The analysis via indicator random variables (counting pairwise comparisons) is a powerful probabilistic technique.
- **Any constant-proportion split gives O(n lg n).** The algorithm does not need perfectly balanced partitions — even 99-to-1 splits at every level result in O(n lg n) time (just with a larger constant). This explains why quicksort performs well in practice despite imperfect pivot choices.
- **Practical optimizations matter.** Switching to insertion sort for small subarrays (≤ k elements) yields O(nk + n lg(n/k)) expected time. Median-of-3 pivot selection improves the constant factor. Tail-recursion optimization reduces stack depth to Θ(lg n).
