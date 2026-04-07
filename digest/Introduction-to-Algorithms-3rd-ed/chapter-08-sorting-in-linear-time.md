# Chapter 8: Sorting in Linear Time

## Overview

This chapter establishes a fundamental lower bound showing that **no comparison-based sort can do better than Ω(n lg n)** in the worst case, then presents three algorithms—counting sort, radix sort, and bucket sort—that bypass this barrier by exploiting properties of the input beyond pairwise comparisons. These linear-time sorts demonstrate that when additional assumptions about the data hold (integer keys in a known range, fixed-length digit representation, or uniform distribution), sorting can be achieved in Θ(n) time.

## Key Concepts

- **Comparison sort model**: Any sort that determines order solely by comparing pairs of elements (e.g., merge sort, heapsort, quicksort). All such algorithms obey the Ω(n lg n) lower bound.
- **Decision-tree model**: An abstraction where each internal node represents a comparison (aᵢ ≤ aⱼ), each leaf represents one of the n! permutations of the input, and the height of the tree equals the worst-case number of comparisons. Any correct comparison sort's decision tree must have at least n! reachable leaves.
- **Non-comparison sorts**: Counting sort, radix sort, and bucket sort use information beyond element comparisons—such as digit values or distribution properties—to sort faster than Ω(n lg n).
- **Stability**: A sort is *stable* if elements with equal keys retain their original relative order in the output. Stability is critical for radix sort's correctness, since it sorts digit-by-digit from least significant to most significant, relying on earlier passes' ordering being preserved.

## Algorithms and Techniques

### 8.1 — Lower Bounds for Comparison Sorting (Decision-Tree Argument)

The chapter opens by proving that every comparison sort must perform at least Ω(n lg n) comparisons in the worst case. The argument proceeds via the decision-tree model:

1. Model any comparison sort on n elements as a binary decision tree.
2. Each leaf corresponds to a permutation of the input; a correct sort must have all n! permutations reachable.
3. A binary tree of height h has at most 2ʰ leaves, so n! ≤ 2ʰ.
4. Taking logarithms: h ≥ lg(n!) = Ω(n lg n) (using Stirling's approximation).

This establishes **Theorem 8.1**: any comparison sort requires Ω(n lg n) comparisons in the worst case.

**Corollary 8.2**: Merge sort and heapsort, which run in O(n lg n) worst-case time, are *asymptotically optimal* among comparison sorts.

---

### 8.2 — Counting Sort

**Idea**: Given n integers each in the range 0 to k, determine for every element x how many elements are ≤ x, then place x directly into its correct output position.

**How it works (COUNTING-SORT(A, B, k))**:
1. **Initialize**: Create auxiliary array C[0..k], set all entries to 0.
2. **Count**: For each element A[j], increment C[A[j]]. After this step, C[i] holds the count of elements equal to i.
3. **Prefix sum**: Compute cumulative sums so that C[i] holds the number of elements ≤ i.
4. **Place**: Iterate through A from right to left. For each A[j], place it at position C[A[j]] in output array B, then decrement C[A[j]] (to handle duplicates and preserve stability).

**Key properties**:
- **Not a comparison sort** — it indexes into arrays using element values, so the Ω(n lg n) bound does not apply.
- **Stable** — processing A right-to-left ensures equal-valued elements appear in B in the same order they had in A. This stability is essential when counting sort is used as a subroutine in radix sort.
- Requires auxiliary arrays B[1..n] and C[0..k], so it is **not in-place**.

---

### 8.3 — Radix Sort

**Idea**: Sort multi-digit numbers by processing digits one at a time, from least significant to most significant, using a stable sort (typically counting sort) at each digit position.

**How it works (RADIX-SORT(A, d))**:
```
for i = 1 to d
    use a stable sort to sort array A on digit i
```
The counterintuitive insight is to sort on the **least significant digit first**. Because the intermediate sort is stable, the relative order established by earlier passes is preserved whenever later digits are equal, yielding a fully sorted result after all d passes.

**Correctness**: Proved by induction on the digit column being sorted. After sorting on digit i, elements are correctly ordered with respect to the lowest i digits, assuming the intermediate sort is stable.

**Choosing how to break keys into digits (Lemma 8.4)**: Given n numbers with b-bit keys and a chosen radix r ≤ b, treat each key as d = ⌈b/r⌉ digits in base 2ʳ. Each counting-sort pass costs Θ(n + 2ʳ), for a total of Θ((b/r)(n + 2ʳ)).
- If b < ⌊lg n⌋: choose r = b → running time Θ(n).
- If b ≥ ⌊lg n⌋: choose r = ⌊lg n⌋ → running time Θ(bn / lg n).

**Practical note**: Although radix sort can have a better asymptotic count of passes than quicksort, each pass may be slower in practice due to poor cache utilization and the overhead of not sorting in place. The best choice depends on machine architecture and data characteristics.

---

### 8.4 — Bucket Sort

**Idea**: When input is drawn uniformly from [0, 1), divide the interval into n equal-sized buckets, distribute elements, sort each bucket individually, then concatenate.

**How it works (BUCKET-SORT(A))**:
1. Create an array B[0..n−1] of empty linked lists (buckets).
2. For each element A[i], insert it into bucket B[⌊n · A[i]⌋].
3. Sort each bucket individually using insertion sort.
4. Concatenate buckets B[0], B[1], …, B[n−1] in order.

**Correctness**: If A[i] ≤ A[j], then ⌊n·A[i]⌋ ≤ ⌊n·A[j]⌋, so A[i] either lands in the same bucket (where insertion sort orders them) or in an earlier bucket (where concatenation orders them).

**Why it's fast on average**: Under the uniform distribution assumption, each bucket receives a constant expected number of elements. The expected size of the sum of squared bucket sizes is Θ(n), keeping the total insertion-sort work linear.

**Beyond uniform input**: Bucket sort runs in linear time whenever the sum of the squares of the bucket sizes is linear in n—even for non-uniform distributions, if the bucket boundaries are chosen appropriately.

## Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Stable? | In-Place? |
|---|---|---|---|---|
| **Any comparison sort** (lower bound) | Ω(n lg n) worst case | — | — | — |
| **Counting Sort** | Θ(n + k) | Θ(n + k) | Yes | No |
| **Radix Sort** (with counting sort) | Θ(d(n + k)) where d = digits, k = digit range | Θ(n + k) | Yes | No |
| **Radix Sort** (b-bit keys, radix r) | Θ((b/r)(n + 2ʳ)) | Θ(n + 2ʳ) | Yes | No |
| **Bucket Sort** | Θ(n) average; Θ(n²) worst case | Θ(n) | Yes (with stable sub-sort) | No |

### Important Theorems and Lemmas

- **Theorem 8.1**: Any comparison sort requires Ω(n lg n) comparisons in the worst case. Proved via the decision-tree model: a tree with ≥ n! leaves must have height ≥ lg(n!) = Ω(n lg n).
- **Corollary 8.2**: Heapsort and merge sort are asymptotically optimal comparison sorts (their O(n lg n) upper bound matches the Ω(n lg n) lower bound).
- **Lemma 8.3**: Radix sort correctly sorts n d-digit numbers in Θ(d(n + k)) time when each digit ranges from 0 to k − 1 and the stable sub-sort takes Θ(n + k).
- **Lemma 8.4**: For n b-bit numbers with chosen radix r ≤ b, radix sort runs in Θ((b/r)(n + 2ʳ)). Optimal choice: r = min(b, ⌊lg n⌋).
- **Bucket sort expected time (Equation 8.1–8.2)**: Under uniform distribution on [0, 1), the expected value of nᵢ² (square of bucket size) is 2 − 1/n, yielding E[T(n)] = Θ(n).

## Key Takeaways

- **The Ω(n lg n) barrier is fundamental but conditional**: it applies only to comparison-based sorts. By exploiting additional structure in the keys (integer values, digit decomposition, distributional properties), linear-time sorting is achievable.
- **Counting sort** is the workhorse: it sorts integers in range [0, k] in Θ(n + k) time and its **stability** is the linchpin that makes radix sort correct.
- **Radix sort** achieves linear time for fixed-width keys by performing d passes of a stable Θ(n + k) sort; the key design decision is choosing the radix r to balance the number of passes against the cost per pass.
- **Bucket sort** achieves Θ(n) average time by leveraging distributional assumptions; its worst case is Θ(n²), but substituting a Θ(n lg n) sort per bucket (e.g., merge sort) caps the worst case at O(n lg n).
- **Practical tradeoffs matter**: radix sort and counting sort are not in-place and may have poor cache behavior compared to quicksort; the theoretically fastest algorithm is not always the best choice for real-world workloads.
