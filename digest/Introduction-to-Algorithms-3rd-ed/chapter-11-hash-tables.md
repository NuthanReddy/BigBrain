# Chapter 11: Hash Tables

## Overview
This chapter presents hash tables, one of the most practical and widely used data structures for implementing dictionaries (supporting INSERT, SEARCH, and DELETE). While worst-case search time can degrade to Θ(n), hash tables deliver O(1) average-case performance under reasonable assumptions. The chapter progresses from direct-address tables through chaining and open addressing, covers the design of hash functions (division, multiplication, and universal hashing), and concludes with perfect hashing for static key sets.

## Key Concepts

- **Direct-address tables**: When the universe of keys U = {0, 1, ..., m−1} is small, store elements directly in an array `T[0..m−1]` indexed by key. All dictionary operations run in O(1) worst-case time. Impractical when |U| is large.
- **Hash tables**: Map keys from a large universe U into a table of size m using a **hash function** `h: U → {0, 1, ..., m−1}`. The table size m is typically proportional to the number of keys actually stored, not the universe size. Element with key k is stored at slot `h(k)`.
- **Collisions**: When two distinct keys k₁ ≠ k₂ satisfy `h(k₁) = h(k₂)`. Collisions are unavoidable when |U| > m (pigeonhole principle).
- **Load factor**: α = n/m, where n is the number of stored elements and m is the table size. A critical parameter governing performance.
- **Simple uniform hashing assumption**: Each key is equally likely to hash to any of the m slots, independently of other keys.
- **Chaining**: Each slot `T[j]` holds a linked list of all elements that hash to slot j. Supports all dictionary operations.
- **Open addressing**: All elements reside within the hash table array itself (no external lists). The hash function produces a **probe sequence** `⟨h(k,0), h(k,1), ..., h(k,m−1)⟩` that is a permutation of `⟨0, 1, ..., m−1⟩`. Load factor α ≤ 1.
- **Universal hashing**: A family H of hash functions such that for any two distinct keys k, l, at most |H|/m functions in H cause k and l to collide. Choosing h randomly from H defeats adversarial key distributions.
- **Perfect hashing**: A two-level hashing scheme for static key sets that guarantees O(1) worst-case search time using O(n) total space.

## Algorithms and Techniques

### Chaining
- **CHAINED-HASH-INSERT(T, x)**: Insert x at the head of list `T[h(x.key)]`. Runs in O(1).
- **CHAINED-HASH-SEARCH(T, k)**: Search for key k in list `T[h(k)]`. Worst case O(n) but Θ(1 + α) on average.
- **CHAINED-HASH-DELETE(T, x)**: Delete element x from its list. O(1) with doubly linked lists (given a pointer to x).

### Open Addressing
- **HASH-INSERT(T, k)**: Probe slots in order `h(k,0), h(k,1), ...` until an empty slot is found; store k there. Signals overflow if table is full.
- **HASH-SEARCH(T, k)**: Probe the same sequence used for insertion. Returns the slot index if k is found, or NIL if an empty slot is encountered.
- **Deletion**: Problematic in open addressing. Cannot simply set a slot to NIL (breaks search chains). Instead, mark deleted slots with a special DELETED sentinel, which HASH-INSERT treats as empty but HASH-SEARCH skips over. This degrades performance, making chaining preferable when deletions are common.

### Probing Strategies
- **Linear probing**: `h(k,i) = (h'(k) + i) mod m`. Simple but suffers from **primary clustering**—long runs of occupied slots build up, increasing average search times. Only m distinct probe sequences.
- **Quadratic probing**: `h(k,i) = (h'(k) + c₁i + c₂i²) mod m`. Reduces primary clustering but introduces **secondary clustering** (keys with the same initial probe share the same probe sequence). Only m distinct probe sequences.
- **Double hashing**: `h(k,i) = (h₁(k) + i·h₂(k)) mod m`. Uses two independent hash functions, producing Θ(m²) distinct probe sequences. The best practical approximation to uniform hashing. Requires h₂(k) to be relatively prime to m.

### Hash Function Design
- **Division method**: `h(k) = k mod m`. Fast (single division). Choose m as a prime not too close to a power of 2 for good distribution.
- **Multiplication method**: `h(k) = ⌊m(kA mod 1)⌋` for a constant 0 < A < 1. Value of m is not critical (typically a power of 2). Knuth suggests A ≈ (√5 − 1)/2 ≈ 0.618.
- **Universal hashing**: The family H_pm = {h_ab : a ∈ Z*_p, b ∈ Z_p} where `h_ab(k) = ((ak + b) mod p) mod m`, with p a prime larger than any key value. Contains p(p−1) hash functions and is proven universal (Theorem 11.5).

### Perfect Hashing (Section 11.5)
- **Two-level scheme**: The first level hashes n keys into m = n slots using a universal hash function h. The second level uses a separate hash table S_j of size m_j = n_j² for each slot j (where n_j keys hash to slot j), with its own universal hash function h_j chosen to be collision-free.
- Guarantees O(1) worst-case lookup for static key sets.
- **Theorem 11.9**: With m = n² and a universal hash function, the probability of any collision is < 1/2.
- **Theorem 11.10**: With first-level table size m = n, the expected total size of all secondary tables is < 2n, ensuring O(n) expected total space.
- **Corollary 11.12**: The probability that total secondary storage exceeds 4n is less than 1/2.

## Complexity Analysis

### Chaining
| Operation | Worst Case | Average Case (simple uniform hashing) |
|---|---|---|
| INSERT | O(1) | O(1) |
| SEARCH (unsuccessful) | Θ(n) | Θ(1 + α) — Theorem 11.1 |
| SEARCH (successful) | Θ(n) | Θ(1 + α) — Theorem 11.2 |
| DELETE | O(1) with doubly linked list | O(1) |

When n = O(m), α = O(1), and all operations are O(1) on average.

### Open Addressing (assuming uniform hashing, α < 1)
| Operation | Expected Probes |
|---|---|
| Unsuccessful search | ≤ 1/(1 − α) — Theorem 11.6 |
| Insertion | ≤ 1/(1 − α) — Corollary 11.7 |
| Successful search | ≤ (1/α) ln(1/(1 − α)) — Theorem 11.8 |

Examples: At α = 0.5, unsuccessful search averages ≤ 2 probes; at α = 0.9, ≤ 10 probes. Successful search at α = 0.5 averages < 1.387 probes; at α = 0.9, < 2.559 probes.

### Universal Hashing
- **Theorem 11.3**: With universal hashing, expected chain length for an unsuccessful search is ≤ α; for a successful search, ≤ 1 + α.
- **Corollary 11.4**: Any sequence of n INSERT, SEARCH, DELETE operations (with O(m) inserts) takes Θ(n) expected total time.

### Perfect Hashing
- **Space**: O(n) expected total.
- **Search**: O(1) worst case.
- **Construction**: Expected O(n) time (try random hash functions until collision-free ones are found).

## Key Takeaways

- **Hash tables achieve O(1) average-case dictionary operations**, making them one of the most practical data structures. The key design choices are the hash function and the collision resolution strategy.
- **Chaining is simpler and handles deletions gracefully**; open addressing avoids pointer overhead and can be more cache-friendly, but deletions are messy and performance degrades sharply as α → 1.
- **Universal hashing provides provable average-case guarantees** regardless of the input distribution, defeating adversarial inputs through randomization. The family h_ab(k) = ((ak + b) mod p) mod m is a practical universal class.
- **Perfect hashing solves the static dictionary problem** with O(1) worst-case search and O(n) space, using a clever two-level scheme with universal hashing at each level.
- **The load factor α is the single most important performance parameter**: keep α = O(1) for chaining or α well below 1 for open addressing to maintain constant-time operations.
