# Chapter 16: Greedy Algorithms

## Overview
Greedy algorithms solve optimization problems by making a sequence of locally optimal choices, each of which looks best at the moment, with the hope of arriving at a globally optimal solution. Unlike dynamic programming, which considers all subproblem solutions before choosing, a greedy algorithm commits to a choice first and then solves the resulting subproblem. The chapter develops the greedy method through the activity-selection problem and Huffman coding, formalizes when greedy works via the greedy-choice property and optimal substructure, and presents a rigorous matroid-theoretic framework that unifies many greedy algorithms.

## Key Concepts

- **Greedy-choice property**: A globally optimal solution can be assembled by making locally optimal (greedy) choices. At each decision point, the algorithm makes the choice that seems best without considering solutions to subproblems — in contrast to dynamic programming, which solves subproblems first.
- **Optimal substructure**: After making the greedy choice, the remaining subproblem has the property that combining its optimal solution with the greedy choice yields an optimal solution to the original problem. This property is shared with dynamic programming.
- **Greedy vs. dynamic programming**: DP proceeds bottom-up, solving subproblems before making choices; greedy proceeds top-down, making a choice and then solving a single remaining subproblem. Greedy algorithms are simpler and more efficient when they yield optimal solutions, but they do not always do so.
- **Proof technique**: Correctness of a greedy algorithm is typically proved by an exchange argument — showing that any optimal solution can be modified to include the greedy choice without worsening its quality.
- **Design steps for greedy algorithms**: (1) Cast the problem as one where making a choice leaves a single subproblem; (2) prove the greedy choice is always safe (part of some optimal solution); (3) demonstrate optimal substructure.
- **Prefix codes**: A binary code where no codeword is a prefix of another. Prefix codes can always achieve optimal data compression and are naturally represented as binary trees (leaves = characters).
- **Matroids**: A combinatorial structure M = (S, 𝓘) with a finite ground set S and a hereditary family of independent subsets 𝓘 satisfying the exchange property. When a matroid is weighted, the GREEDY algorithm (sort by decreasing weight, greedily add elements that maintain independence) always finds an optimal independent subset.
- **Graphic matroid**: M_G = (S_G, 𝓘_G) where S_G is the edge set of a graph and A ∈ 𝓘_G iff A is acyclic (a forest). Maximal independent subsets are spanning trees, connecting the greedy matroid framework to minimum spanning tree algorithms.

## Algorithms and Techniques

### 1. Activity-Selection Problem
- **Problem**: Given n activities with start times s_i and finish times f_i, select a maximum-size subset of mutually compatible (non-overlapping) activities.
- **Dynamic programming formulation**: Define S_{ij} as activities that start after a_i finishes and finish before a_j starts. Recurrence: c[i,j] = max_{a_k ∈ S_{ij}} {c[i,k] + c[k,j] + 1}.
- **Greedy insight**: Always choose the activity with the earliest finish time from the remaining compatible activities. This leaves the resource available for the maximum number of future activities.
- **Theorem 16.1**: For any nonempty subproblem S_k, the activity a_m with the earliest finish time is included in some maximum-size compatible subset. Proved by an exchange argument: swapping a_m for the first-finishing activity in any optimal set does not reduce compatibility.
- **RECURSIVE-ACTIVITY-SELECTOR(s, f, k, n)**: Scans activities in finish-time order starting from a_k; finds first compatible activity a_m (where s[m] ≥ f[k]) and recurses on S_m. Runs in Θ(n) assuming pre-sorted input.
- **GREEDY-ACTIVITY-SELECTOR(s, f)**: Iterative version. Maintains the most recent selection k; for each activity m, adds it if s[m] ≥ f[k]. Also Θ(n) time with pre-sorted input.

### 2. Huffman Codes
- **Problem**: Given an alphabet C with character frequencies, construct a binary prefix code that minimizes the total encoded file length B(T) = Σ_{c ∈ C} c.freq · d_T(c), where d_T(c) is the depth of character c's leaf in the code tree T.
- **HUFFMAN(C)**: A bottom-up greedy algorithm using a min-priority queue:
  1. Initialize Q with all characters.
  2. Repeat |C| − 1 times: extract the two lowest-frequency nodes x, y; create a new internal node z with z.freq = x.freq + y.freq; set z.left = x, z.right = y; insert z back into Q.
  3. Return the remaining node (the root).
- **Lemma 16.2 (Greedy-choice property)**: The two characters with the lowest frequencies can always be made siblings at maximum depth in some optimal code tree. Proved by swapping: replacing any deepest pair with the two lowest-frequency characters does not increase cost.
- **Lemma 16.3 (Optimal substructure)**: Replacing a leaf z (representing merged characters x, y) with an internal node having x and y as children transforms an optimal tree for the reduced alphabet into an optimal tree for the original alphabet. Relationship: B(T) = B(T') + x.freq + y.freq.
- **Theorem 16.4**: HUFFMAN produces an optimal prefix code, following directly from Lemmas 16.2 and 16.3.

### 3. Matroid-Based Greedy Algorithm
- **Matroid definition**: M = (S, 𝓘) where S is finite, 𝓘 is hereditary (if B ∈ 𝓘 and A ⊆ B, then A ∈ 𝓘), and satisfies the exchange property (if A, B ∈ 𝓘 and |A| < |B|, then ∃ x ∈ B − A with A ∪ {x} ∈ 𝓘).
- **Theorem 16.5**: The graphic matroid M_G = (E, 𝓘_G) is indeed a matroid. Proof shows that forests satisfy hereditary and exchange properties (a forest with more edges has fewer trees, so an edge connecting different trees in the smaller forest can be safely added).
- **Theorem 16.6**: All maximal independent subsets in a matroid have the same size (follows immediately from the exchange property).
- **GREEDY(M, w)**: Sort elements of S by decreasing weight w; greedily add each element x to the accumulating set A if A ∪ {x} remains independent. Returns an optimal (maximum-weight) independent subset.
- **Lemma 16.7 (Greedy-choice for matroids)**: The heaviest element x such that {x} is independent belongs to some optimal subset.
- **Lemma 16.10 (Optimal substructure for matroids)**: After selecting x, the remaining problem reduces to finding an optimal subset in the contraction M' = (S', 𝓘') of M by x.
- **Theorem 16.11**: GREEDY(M, w) returns an optimal subset for any weighted matroid.

### 4. Task Scheduling with Deadlines
- **Problem**: Given n unit-time tasks with deadlines d_i and penalties w_i, schedule tasks on a single processor to minimize total late penalty.
- **Formulation as a matroid**: A set A of tasks is independent if they can all be scheduled before their deadlines (equivalently, for each t, the number of tasks in A with deadline ≤ t does not exceed t — Lemma 16.12).
- **Theorem 16.13**: The system (S, 𝓘) of tasks and independent sets forms a matroid, enabling use of the GREEDY algorithm to find a maximum-weight (minimum-penalty) schedule.
- **Scheduling**: Sort tasks by decreasing penalty, greedily add each task to the early set if independence is maintained. Schedule early tasks in deadline order; late tasks fill remaining slots.

### Greedy vs. DP: The Knapsack Problems
- **Fractional knapsack**: Items can be taken in fractions. Greedy strategy (sort by value per pound, take greedily) yields an optimal solution in O(n lg n) time.
- **0-1 knapsack**: Items must be taken whole or not at all. The greedy strategy fails because taking the highest value-per-pound item may prevent filling the knapsack to capacity. Requires dynamic programming with O(nW) time.

## Complexity Analysis

| Algorithm | Time Complexity | Notes |
|---|---|---|
| GREEDY-ACTIVITY-SELECTOR | Θ(n) | Assumes activities pre-sorted by finish time; O(n lg n) with sorting |
| RECURSIVE-ACTIVITY-SELECTOR | Θ(n) | Same as iterative with pre-sorted input |
| HUFFMAN | O(n lg n) | Using binary min-heap; O(n lg lg n) with van Emde Boas tree |
| GREEDY (matroid) | O(n lg n + n·f(n)) | Where f(n) is cost of independence check; sorting dominates if f(n) = O(lg n) |
| Task scheduling | O(n²) | O(n) independence checks each costing O(n); faster with disjoint-set forests |

## Key Takeaways

- **Greedy algorithms are simpler and faster than DP** when they work. They commit to locally optimal choices without needing to solve all subproblems first, yielding efficient top-down solutions.
- **Not every problem admits a greedy solution**: The 0-1 knapsack problem illustrates that even when a problem has optimal substructure, the greedy-choice property may not hold. Always verify both properties before applying a greedy strategy.
- **The exchange argument is the standard proof technique**: Show that any optimal solution can be transformed to include the greedy choice without loss of quality. This pattern appears in activity selection (Theorem 16.1), Huffman coding (Lemma 16.2), and matroid theory (Lemma 16.7).
- **Matroid theory provides a unifying framework**: Many greedy-solvable problems (minimum spanning trees, task scheduling, maximum-weight forests) can be cast as finding optimal subsets in weighted matroids, where the generic GREEDY algorithm is guaranteed to produce optimal results.
- **Huffman coding is a foundational greedy algorithm**: It achieves optimal prefix-free compression by always merging the two lowest-frequency symbols, saving 20–90% in typical data compression scenarios. Its correctness depends on both the greedy-choice property and optimal substructure of the code tree.
