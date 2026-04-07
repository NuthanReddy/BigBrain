# Chapter 5: Probabilistic Analysis and Randomized Algorithms

## Overview
This chapter introduces two complementary ideas: **probabilistic analysis**, which analyzes algorithm performance by assuming a probability distribution over inputs, and **randomized algorithms**, which use random choices within the algorithm itself to achieve good expected performance regardless of input. The hiring problem serves as the central motivating example, and the chapter develops indicator random variables as a key analytical tool.

## Key Concepts

### Probabilistic Analysis vs. Randomized Algorithms
- **Probabilistic analysis**: Assumes a distribution over inputs (e.g., uniform random permutation) to compute an **average-case** running time. The algorithm itself is deterministic—the randomness is in the input.
- **Randomized algorithm**: Introduces randomness into the algorithm (e.g., randomly permuting input before processing). The running time is an **expected** running time over the algorithm's random choices, with no assumptions about the input.
- **Key distinction**: In probabilistic analysis, bad inputs can cause bad performance. In a randomized algorithm, no input can consistently cause bad performance—only "unlucky" random choices can.

### Indicator Random Variables (Section 5.2)
- For a sample space S and event A, the indicator random variable is: I{A} = 1 if A occurs, 0 otherwise.
- **Lemma 5.1**: E[I{A}] = Pr{A}. This simple relationship is the foundation of many analyses.
- **Power of linearity**: Even when random variables are dependent, linearity of expectation (E[X₁ + X₂ + ... + Xₙ] = E[X₁] + E[X₂] + ... + E[Xₙ]) applies, making indicator random variables extremely useful for counting expected occurrences.

### The Hiring Problem (Section 5.1)
- **Model**: Interview n candidates sequentially; hire a candidate if they're better than all previous hires. Cost = cᵢn (interviews) + cₕm (hires), where m is the number of hires.
- **Worst case**: Candidates arrive in increasing order of quality → hire every candidate → O(cₕn).
- **Analysis with indicator variables**: Let Xᵢ = I{candidate i is hired}. Since candidate i is hired iff they're the best of the first i, Pr{Xᵢ = 1} = 1/i.
  - E[X] = Σᵢ₌₁ⁿ (1/i) = ln n + O(1) (harmonic series).
  - **Lemma 5.2**: Average-case hiring cost is O(cₕ ln n) assuming random input order.
  - **Lemma 5.3**: Randomized version (permute first) has expected hiring cost O(cₕ ln n) for any input.

### Random Permutation Algorithms (Section 5.3)
- **PERMUTE-BY-SORTING**: Assign each element a random priority from [1, n³], then sort by priority. Runs in Θ(n lg n). **Lemma 5.4** proves this produces a uniform random permutation (each of n! permutations equally likely).
- **RANDOMIZE-IN-PLACE (Fisher-Yates shuffle)**: For i = 1 to n, swap A[i] with A[RANDOM(i, n)]. Runs in O(n). **Lemma 5.5** proves this produces a uniform random permutation via a loop invariant on k-permutations.
  - Loop invariant: Before iteration i, A[1..i−1] is any particular (i−1)-permutation with probability (n−i+1)!/n!.

## Algorithms and Techniques

### HIRE-ASSISTANT
- Sequentially examines candidates, maintaining the best seen so far, and hires whenever a better candidate is found.
- Deterministic: for a fixed input, the number of hires is fixed.

### RANDOMIZED-HIRE-ASSISTANT
- Randomly permutes the candidate list before applying the same hiring logic.
- Expected number of hires is O(ln n) regardless of input ordering.

### ON-LINE-MAXIMUM (Secretary Problem, Section 5.4.4)
- **Constraint**: Must hire exactly once; must decide immediately after each interview.
- **Strategy**: Interview and reject the first k candidates (learning phase), then hire the first subsequent candidate who beats all previously seen.
- **Optimal k**: k = n/e (approximately 37% of candidates rejected).
- **Success probability**: At least 1/e ≈ 0.368 of hiring the best candidate overall.

## Complexity Analysis

### Hiring Problem
| Scenario | Hiring Cost |
|---|---|
| Worst case (deterministic) | O(cₕn) |
| Average case (random input) | O(cₕ ln n) |
| Randomized algorithm (any input) | O(cₕ ln n) expected |

### Random Permutation
| Algorithm | Time | Space |
|---|---|---|
| PERMUTE-BY-SORTING | Θ(n lg n) | Θ(n) |
| RANDOMIZE-IN-PLACE | Θ(n) | Θ(1) |

### Advanced Examples (Section 5.4)

**Birthday Paradox (5.4.1)**:
- With k people and n = 365 days, the probability of at least one shared birthday exceeds 1/2 when k ≥ 23.
- Using indicator variables: expected number of matching pairs is k(k−1)/(2n); this reaches 1 when k ≈ √(2n) ≈ 28 for n = 365.
- General result: Θ(√n) people suffice.

**Balls and Bins (5.4.2)**:
- Tossing balls into b bins uniformly at random:
  - Expected balls in a given bin after n tosses: n/b.
  - Expected tosses until a specific bin gets a ball: b.
  - Expected tosses until every bin has at least one ball (**coupon collector's problem**): b ln b + O(b) ≈ b ln b.

**Streaks (5.4.3)**:
- In n fair coin flips, the expected length of the longest consecutive-heads streak is **Θ(lg n)**.
  - Upper bound: O(lg n) — probability of a streak ≥ 2⌈lg n⌉ is at most 1/n.
  - Lower bound: Ω(lg n) — partitioning into groups of ⌊(lg n)/2⌋ flips, at least one group is likely all-heads.

## Key Takeaways
- **Indicator random variables** combined with **linearity of expectation** provide a powerful and often simpler alternative to direct probability calculations, especially for counting expected occurrences across many events.
- **Randomized algorithms** offer a fundamental advantage: they guarantee good expected performance for **any** input, unlike probabilistic analysis which relies on input distribution assumptions.
- **RANDOMIZE-IN-PLACE** (Fisher-Yates shuffle) is the gold standard for generating uniform random permutations in O(n) time and O(1) extra space.
- The **birthday paradox** illustrates that collisions happen surprisingly early: only Θ(√n) trials are needed for a 50% chance of a match among n possibilities—important for hashing analysis and cryptography.
- The **coupon collector's problem** (b ln b expected trials to cover all b bins) appears frequently in analysis of randomized algorithms and hashing schemes.
