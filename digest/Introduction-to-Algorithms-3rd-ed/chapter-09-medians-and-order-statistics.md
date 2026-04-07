# Chapter 9: Medians and Order Statistics

## Overview

This chapter tackles the **selection problem**: given a set of *n* distinct numbers, find the *i*-th smallest element (the *i*-th order statistic). While sorting solves this in O(*n* lg *n*) time, the chapter demonstrates that selection can be performed in **Θ(*n*)** time — both in expectation (via a randomized algorithm) and in the worst case (via the deterministic median-of-medians strategy). These results are significant because they show that selection is fundamentally easier than sorting, bypassing the Ω(*n* lg *n*) comparison-sort lower bound without making any assumptions about the input.

## Key Concepts

- **Order statistic:** The *i*-th order statistic of a set is its *i*-th smallest element. The minimum is the 1st order statistic; the maximum is the *n*-th.
- **Median:** The "halfway point" of a set. For odd *n* the median is unique at position (*n* + 1)/2. For even *n* there are two medians; the text adopts the **lower median** at position ⌊(*n* + 1)/2⌋ by convention.
- **Selection problem (formal):** Given a set *A* of *n* distinct numbers and an integer *i* (1 ≤ *i* ≤ *n*), return the element in *A* that is larger than exactly *i* − 1 other elements.
- **Comparison lower bound for minimum:** Any comparison-based algorithm needs at least *n* − 1 comparisons to find the minimum, since every non-minimum element must "lose" at least one comparison (tournament argument).
- **Simultaneous min and max:** Both the minimum and maximum can be found together using at most 3⌊*n*/2⌋ comparisons, rather than the naïve 2*n* − 2, by processing elements in pairs.
- **Selection vs. sorting:** Selection algorithms determine relative order information only as needed, allowing them to run in linear time — they are not subject to the Ω(*n* lg *n*) sorting lower bound.

## Algorithms and Techniques

### 9.1 — MINIMUM (and MAXIMUM)

**Idea:** Scan the array once, tracking the smallest element seen so far.

```
MINIMUM(A):
  min = A[1]
  for i = 2 to A.length:
      if A[i] < min:
          min = A[i]
  return min
```

- Uses exactly *n* − 1 comparisons, which is **optimal** by the tournament lower-bound argument.
- MAXIMUM is symmetric, also using *n* − 1 comparisons.

**Simultaneous min and max (pairwise technique):**

Rather than finding min and max independently (2*n* − 2 comparisons), process elements in **pairs**:

1. Compare the two elements of each pair with each other (1 comparison).
2. Compare the smaller of the pair against the running minimum (1 comparison).
3. Compare the larger of the pair against the running maximum (1 comparison).

This yields **3 comparisons per 2 elements**, for a total of at most **3⌊*n*/2⌋** comparisons. Initialization depends on parity: if *n* is odd, set both min and max to the first element; if *n* is even, compare the first two elements to seed min and max.

---

### 9.2 — RANDOMIZED-SELECT (Expected Linear Time)

**Idea:** A divide-and-conquer algorithm modeled on quicksort, but only **recursing into one side** of the partition — the side that contains the desired order statistic.

```
RANDOMIZED-SELECT(A, p, r, i):
  if p == r:
      return A[p]
  q = RANDOMIZED-PARTITION(A, p, r)
  k = q - p + 1                       // rank of pivot within A[p..r]
  if i == k:
      return A[q]                      // pivot is the answer
  else if i < k:
      return RANDOMIZED-SELECT(A, p, q-1, i)
  else:
      return RANDOMIZED-SELECT(A, q+1, r, i - k)
```

**How it works:**

1. **Partition** the subarray A[*p*..*r*] around a randomly chosen pivot (via `RANDOMIZED-PARTITION`), placing the pivot at index *q*.
2. Compute the **rank** *k* of the pivot within the subarray.
3. If *k* = *i*, the pivot is the answer; return it.
4. If *i* < *k*, recurse on the **left** subarray A[*p*..*q*−1].
5. If *i* > *k*, recurse on the **right** subarray A[*q*+1..*r*], looking for the (*i* − *k*)-th smallest element.

**Key property:** Unlike quicksort, only **one** recursive call is made per level, which is why the expected time drops from Θ(*n* lg *n*) to Θ(*n*).

---

### 9.3 — SELECT / Median-of-Medians (Worst-Case Linear Time)

**Idea:** Guarantee a good pivot by choosing the **median of medians** — the median of the group medians — so that each recursive call eliminates a guaranteed fraction of the elements.

**Five steps of SELECT:**

1. **Divide** the *n* elements into ⌈*n*/5⌉ groups of 5 (the last group may have fewer).
2. **Find the median** of each group by insertion-sorting the 5 elements and picking the middle one.
3. **Recursively call SELECT** to find the median *x* of the ⌈*n*/5⌉ group medians (the "median of medians").
4. **Partition** the entire array around *x* using a modified PARTITION. Let *k* be the rank of *x*.
5. If *i* = *k*, return *x*. Otherwise, **recurse** into whichever side contains the *i*-th element.

**Why groups of 5?** This size is carefully chosen so that the two recursive calls (step 3 on ⌈*n*/5⌉ elements, step 5 on at most 7*n*/10 + 6 elements) sum to a fraction strictly less than *n*, ensuring linear time. Groups of 7 also work; groups of 3 do **not** guarantee linear time because the fractions no longer sum to less than 1.

**Guarantee on partitioning quality:** At least 3⌈½⌈*n*/5⌉⌉ − 6 ≈ 3*n*/10 − 6 elements are guaranteed to be greater than *x* (and similarly, at least that many are less than *x*). Therefore, the recursive call in step 5 operates on at most **7*n*/10 + 6** elements.

## Complexity Analysis

| Algorithm | Best Case | Expected Case | Worst Case | Space |
|---|---|---|---|---|
| MINIMUM / MAXIMUM | Θ(*n*) | Θ(*n*) | Θ(*n*) — exactly *n*−1 comparisons | O(1) |
| Simultaneous min & max | — | — | 3⌊*n*/2⌋ comparisons | O(1) |
| RANDOMIZED-SELECT | Θ(*n*) | **Θ(*n*)** | Θ(*n*²) | O(1) expected (in-place) |
| SELECT (median-of-medians) | Θ(*n*) | Θ(*n*) | **Θ(*n*)** | O(*n*) (recursion stack) |

### Analysis of RANDOMIZED-SELECT (Expected Θ(*n*))

Using indicator random variables *X_k* (= 1 if the partition has exactly *k* elements on the low side):

- The recurrence is: T(*n*) ≤ Σ_{k=1}^{n} X_k · T(max(*k*−1, *n*−*k*)) + O(*n*)
- Taking expectations and noting E[*X_k*] = 1/*n*: E[T(*n*)] ≤ (2/*n*) Σ_{k=⌊n/2⌋}^{n−1} E[T(*k*)] + O(*n*)
- Solving by substitution yields **E[T(*n*)] = O(*n*)**, choosing constant *c* > 4*a* (where *a* bounds the non-recursive work).
- The worst case is Θ(*n*²), occurring if the pivot is always the extreme element.

### Analysis of SELECT (Worst-Case Θ(*n*))

The recurrence is:

```
T(n) = O(1)                                if n < 140
T(n) ≤ T(⌈n/5⌉) + T(7n/10 + 6) + O(n)    if n ≥ 140
```

- **T(⌈*n*/5⌉):** cost of recursively finding the median of medians (step 3).
- **T(7*n*/10 + 6):** cost of the recursive selection on the larger partition side (step 5).
- **O(*n*):** dividing into groups, finding group medians via insertion sort on constant-size groups, and partitioning.

By substitution (assuming T(*n*) ≤ *cn*):

- *cn*/5 + *c* + 7*cn*/10 + 6*c* + *an* = 9*cn*/10 + 7*c* + *an* ≤ *cn* when *c* ≥ 20*a* and *n* ≥ 140.
- The base-case threshold of **140** comes from requiring *n*/(*n* − 70) ≤ 2, i.e., *n* ≥ 140. Any constant strictly greater than 70 works with an appropriately chosen *c*.
- This proves **T(*n*) = O(*n*)** in the worst case.

### Historical Notes on Comparison Bounds for Median

- Lower bound for median finding: 2*n* comparisons (Bent and John).
- Upper bound: approximately 2.95*n* comparisons (Dor and Zwick).
- The exact number of comparisons needed remains an open problem.

## Key Takeaways

- **Selection is easier than sorting.** Finding the *i*-th smallest element takes O(*n*) time, whereas sorting requires Ω(*n* lg *n*) — solving selection by sorting is asymptotically wasteful.
- **RANDOMIZED-SELECT** is the practical choice: simple, in-place, and Θ(*n*) expected time, though its worst case is Θ(*n*²). It works by partitioning around a random pivot and recurring on only one side.
- **SELECT (median-of-medians)** achieves **O(*n*) worst-case** time by deterministically choosing a pivot that guarantees at least 30% of elements fall on each side of the partition. It divides elements into groups of 5, finds each group's median, and recursively selects the median of those medians.
- **Simultaneous min and max** can be found in 3⌊*n*/2⌋ comparisons (instead of 2*n* − 2) by processing elements in pairs — a useful constant-factor optimization.
- The **group size of 5** in SELECT is critical: it ensures the two sub-problem sizes (≈ *n*/5 and ≈ 7*n*/10) sum to less than *n*, guaranteeing linear convergence. Groups of 3 fail this condition; groups of 7 succeed but with a larger constant factor.
