# 5 Probabilistic Analysis and Randomized Algorithms

# Probabilistic Analysis and Randomized Algorithms Study Notes

## Overview
This topic introduces the concepts of **probabilistic analysis** and **randomized algorithms**. These techniques are key for analyzing algorithms under uncertainty and designing algorithms that leverage randomization. Probabilistic analysis uses principles of probability theory to evaluate the performance of an algorithm, often in terms of average-case or expected values. Randomized algorithms introduce randomness explicitly into their logic, making their behavior partly dependent on random choices. This approach is useful when the input distribution is unknown or non-random.

In this chapter, we explore the **hiring problem**, a key example showcasing how probabilistic analysis and randomization are applied.

---

## Key Concepts

- **Probabilistic Analysis**
  - Uses probability to estimate the average-case behavior of algorithms.
  - Assumes a model or distribution for the input data.
  - Focuses on expected costs (e.g., expected runtime or total cost) over all possible inputs based on their probabilities.

- **Randomized Algorithms**
  - Algorithms whose behavior depends partially on random decisions.
  - Do not rely on assumptions about input distribution; instead, they generate randomness internally.
  - Useful when input distributions are unknown, adversarial, or hard to model.
  - Characterized by expected running time (averaged over random choices made by the algorithm).

- **Indicator Random Variables**
  - A mathematical tool to convert probabilities into expectations.
  - Simplifies the analysis of probabilistic events, especially in repeated random trials.
  - Defined as \( I_A = 1 \) if event \( A \) occurs, and \( I_A = 0 \) otherwise.

- **Hiring Problem Example**
  - Models scenarios where selections are dynamic, and decisions are based on pairwise comparisons.
  - Illustrates worst-case, average-case, and randomized analysis approaches.
  - Provides practice in designing algorithms with probabilistic and randomized techniques.

---

## Algorithms and Techniques

### 5.1 The Hiring Problem

#### Problem Description
You want to hire an office assistant. You:
1. Interview candidates one at a time.
2. Hire a candidate if they are better qualified than the current hire.
Each interview incurs cost \( c_i \), and each hire incurs a higher cost, \( c_h \). The goal is to analyze the total cost of the hiring process and propose possible optimizations.

#### Pseudocode: HIRE-ASSISTANT Algorithm

```plaintext
HIRE-ASSISTANT(n):
  best = 0  // Candidate 0 is a dummy least-qualified candidate
  for i = 1 to n:
    interview candidate i
    if candidate i is better than candidate best:
      best = i
      hire candidate i
```

- Assumptions:
  1. Candidates arrive in arbitrary order.
  2. Each candidate is compared to the best so far using a simple pairwise comparison.

---

### Complexity Analysis

#### 1. Cost Analysis
- **Interview Cost**: A total of \( n \) interviews implies a cost of \( c_i n \).
- **Hiring Cost**:
  - Worst case: \( m = n \) (i.e., every candidate is hired because they arrive in increasing quality order). 
  - Average case: Computed probabilistically under random input distributions.

#### 2. Worst-Case Analysis (Deterministic Ordering)
- In the worst case, all \( n \) candidates are hired. Hence, the hiring cost is:
  \[
  ch \times n = O(c_h n)
  \]

- Total cost: 
  \[
  O(c_i n + c_h n) = O(n)
  \]

#### 3. Probabilistic Analysis (Random Ordering)
- Assumption: Candidates arrive in **random order**. 
- Each candidate has equal probability, so the expected hiring cost depends on how often the "current winner" changes.
- **Expected hires**: Approximately \( \ln n \) for \( n \) candidates.
- Total cost under probabilistic analysis:
  \[
  O(c_i n + c_h \ln n)
  \]

---

### Randomized HIRE-ASSISTANT Algorithm

#### Key Idea
To enforce randomness, we shuffle the order of candidates. This ensures a uniform random input sequence, sidestepping reliance on external randomness.

#### Pseudocode

```plaintext
RANDOMIZED-HIRE-ASSISTANT(n):
  perm = RANDOM-PERMUTATION(1, ..., n)  // Randomly shuffle candidates
  best = 0
  for i = 1 to n:
    interview candidate perm[i]
    if perm[i] is better than candidate best:
      best = perm[i]
      hire candidate perm[i]
```

- **Randomization Method**: RANDOM-PERMUTATION generates a random permutation using calls to a random number generator. Each possible arrangement appears with equal probability.

---

### Complexity Comparisons

| **Algorithm**             | **Interview Cost** | **Hiring Cost (Worst)** | **Hiring Cost (Expected)** | **Total Cost**        |
|----------------------------|--------------------|--------------------------|----------------------------|-----------------------|
| HIRE-ASSISTANT             | \( O(n) \)        | \( O(n) \)               | \( O(\ln n) \)             | \( O(c_i n + c_h n) \) |
| RANDOMIZED-HIRE-ASSISTANT  | \( O(n) \)        | \( O(n) \)               | \( O(\ln n) \)             | \( O(c_i n + c_h \ln n) \) |

---

## Theorems

### Lemma 5.1: Expected Value of an Indicator Random Variable
**Statement:**
Let \( A \) be an event in the sample space \( S \), and \( I_A \) be its indicator random variable. Then:
\[
E[I_A] = \Pr[A]
\]

**Proof**:
1. By definition of \( I_A \): \( I_A = 1 \) if \( A \) occurs, and \( I_A = 0 \) otherwise.
2. Using expectation formula:
   \[
   E[I_A] = 1 \cdot \Pr[A] + 0 \cdot \Pr[\neg A]
   \]
   Simplifies to:
   \[
   E[I_A] = \Pr[A]
   \]

**Significance**:
Indicator random variables enable easy computation of expected outcomes in probabilistic models.

---

## Concrete Example: Hiring Problem
Consider \( n = 5 \) candidates arriving in random order, with cost \( c_i = 1 \) and \( c_h = 10 \):
1. If the order is fixed deterministically, all \( n \) hires could occur in the worst case.
2. With probabilistic analysis, expected hires \( \approx \ln(5) \approx 1.6 \), so:
   \[
   Total Cost = c_i n + c_h \ln n = 1(5) + 10(\ln 5) \approx 5 + 16 \approx 21
   \]

---

## Key Takeaways
- Probabilistic analysis helps derive average-case guarantees based on input distributions.
- Randomized algorithms trade exact execution patterns for probabilistic guarantees, often improving performance on average.
- The **hiring problem** serves as an intuitive example for applying these concepts, emphasizing both worst-case and expected analyses.
