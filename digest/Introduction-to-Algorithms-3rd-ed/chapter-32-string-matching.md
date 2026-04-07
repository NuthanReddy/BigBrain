# Chapter 32: String Matching

## Overview
This chapter addresses the fundamental problem of finding all occurrences of a pattern string P of length m within a text string T of length n. It presents four algorithms with progressively better performance: the naive brute-force method, Rabin-Karp (hashing-based), finite-automaton matching, and the Knuth-Morris-Pratt (KMP) algorithm. The chapter develops the theoretical foundation of the **suffix function** to rigorously analyze these algorithms and prove their correctness.

## Key Concepts

- **String-matching problem**: given text T[1..n] and pattern P[1..m] over alphabet Σ, find all **valid shifts** s (0 ≤ s ≤ n−m) where T[s+1..s+m] = P[1..m].
- **Suffix function σ(x)**: for a string x, σ(x) is the length of the longest prefix of P that is a suffix of x. A valid shift s occurs exactly when σ(Tₛ₊ₘ) = m.
- **Overlapping-suffix lemma (Lemma 32.1)**: if x ⊐ z and y ⊐ z (both are suffixes of z), then the shorter is a suffix of the longer (or they are equal if same length). This lemma is fundamental to correctness proofs.
- **Prefix function π**: used in KMP; π[q] is the length of the longest proper prefix of P[1..q] that is also a suffix of P[1..q]. Captures the self-overlap structure of the pattern.

| Algorithm | Preprocessing Time | Matching Time |
|---|---|---|
| Naive | 0 | O((n − m + 1)m) |
| Rabin-Karp | Θ(m) | O((n − m + 1)m) worst case |
| Finite automaton | O(m|Σ|) | Θ(n) |
| Knuth-Morris-Pratt | Θ(m) | Θ(n) |

## Algorithms and Techniques

### NAIVE-STRING-MATCHER(T, P)
- Checks every possible shift s = 0, 1, …, n−m by comparing P[1..m] to T[s+1..s+m] character by character.
- Worst-case: O((n − m + 1)m) — e.g., T = aⁿ, P = aᵐ.
- No preprocessing; conceptually simple but slow for large inputs.

### RABIN-KARP-MATCHER(T, P, d, q)
- Uses **hashing** to speed up matching in practice.
- Treats each m-character substring as a number in base d (the alphabet size), computed modulo a prime q.
- **Rolling hash**: computes the hash of T[s+2..s+m+1] from T[s+1..s+m] in O(1) time using the recurrence: tₛ₊₁ = (d(tₛ − T[s+1]·dᵐ⁻¹) + T[s+m+1]) mod q.
- When hashes match (**hit**), performs explicit character comparison to confirm (avoids false positives / **spurious hits**).
- **Expected running time**: O(n + m) when q is chosen well (number of spurious hits is O(n/q)).
- **Worst case**: O((n − m + 1)m) — but this is rare in practice.
- **Advantage**: generalizes well to 2D pattern matching and multiple pattern search.

### FINITE-AUTOMATON-MATCHER(T, δ, m)
- Builds a deterministic finite automaton (DFA) with states {0, 1, …, m} where state q means the longest prefix of P matching a suffix of text seen so far has length q.
- **Transition function**: δ(q, a) = σ(P[1..q]a) for each state q and character a.
- Matching: process T left to right, transitioning states. Report a match when state m is reached.
- **Matching time**: Θ(n) — exactly one transition per text character.
- **Preprocessing**: COMPUTE-TRANSITION-FUNCTION builds the DFA in O(m|Σ|) time by checking all state-character combinations.
- **Correctness** (Theorem 32.4): after scanning T[1..i], the automaton is in state σ(Tᵢ), which is proved using the suffix-function recursion lemma (Lemma 32.3).

### KMP-MATCHER(T, P) — Knuth-Morris-Pratt
- Achieves Θ(n) matching with only Θ(m) preprocessing—better than the finite-automaton approach.
- **Key idea**: instead of precomputing the full transition function δ(q, a) for all characters, use the **prefix function** π to efficiently compute transitions on the fly.
- **Prefix function π[q]**: the length of the longest proper prefix of P[1..q] that is also a suffix of P[1..q]. This encodes how to "fall back" after a mismatch without re-examining characters.
- **COMPUTE-PREFIX-FUNCTION(P)**: computes π[1..m] in Θ(m) time using an amortized analysis (the pointer k can increase at most m−1 times total across all iterations, so total decreases via π are also bounded).
- **Matching procedure**: maintains state q (number of characters matched so far). On mismatch at position q+1, sets q = π[q] and retries. On match, increments q. Reports match when q = m, then sets q = π[q] to continue searching.
- **Amortized analysis** via potential function: q increases by at most 1 per text character, and each π lookup decreases q, so total work is O(n).

## Complexity Analysis

**Lemma 32.2 (Suffix-function inequality)**: σ(xa) ≤ σ(x) + 1 — appending one character can increase the suffix function by at most 1.

**Lemma 32.3 (Suffix-function recursion)**: σ(xa) = σ(P_q · a) where q = σ(x). This enables computing σ incrementally.

**Theorem 32.4**: The finite automaton correctly tracks σ(Tᵢ) after reading each character T[i].

**Lemma 32.5 (Prefix-function iteration)**: the sequence π[q], π[π[q]], π[π[π[q]]], … enumerates all lengths k < q such that Pₖ ⊐ P_q, in decreasing order. This "failure chain" is the backbone of KMP.

**Lemma 32.6**: the transition function δ(q, a) equals the value obtained by following the π chain from q until a match or exhaustion—proving KMP correctly simulates the DFA.

**Corollary 32.7**: KMP-MATCHER correctly finds all occurrences of P in T.

## Key Takeaways

- **Rabin-Karp** is the most practical for many real-world scenarios: its rolling hash gives O(n + m) expected time, it handles multiple patterns efficiently, and it generalizes to 2D matching.
- **KMP achieves the optimal Θ(n + m) worst-case bound** by precomputing the prefix function in Θ(m) time, avoiding redundant character comparisons through intelligent backtracking.
- **The prefix function π encodes the self-overlap structure** of the pattern: it tells us the longest proper prefix that is also a suffix, enabling the algorithm to never backtrack in the text.
- **The finite-automaton approach** provides the clearest theoretical framework—the suffix function σ unifies the correctness analysis of all four algorithms—but its O(m|Σ|) preprocessing makes it less practical for large alphabets.
- **String matching is a gateway to more complex pattern-matching** problems, including regular expression matching, approximate matching, and multi-pattern matching (Aho-Corasick).
