# Chapter 35: Approximation Algorithms

## Overview

Since many important problems are NP-complete and unlikely to have exact polynomial-time solutions, this chapter presents polynomial-time approximation algorithms that find near-optimal solutions with provable quality guarantees. The chapter introduces the concepts of approximation ratios, polynomial-time approximation schemes (PTAS), and fully polynomial-time approximation schemes (FPTAS), and demonstrates these through five concrete problems: vertex cover, the traveling-salesman problem, set cover, MAX-3-CNF satisfiability (with randomization and linear programming), and the subset-sum problem.

## Key Concepts

- **Approximation Ratio ρ(n)**: For an optimization problem, an algorithm has approximation ratio ρ(n) if for every input of size n, max(C/C*, C*/C) ≤ ρ(n), where C is the algorithm's cost and C* is the optimal cost. A ratio of 1 means optimal; larger ratios mean worse guarantees.
- **ρ(n)-Approximation Algorithm**: An algorithm that achieves an approximation ratio of ρ(n) for all inputs of size n.
- **Polynomial-Time Approximation Scheme (PTAS)**: An algorithm parameterized by ε > 0 that achieves a (1+ε)-approximation ratio and runs in time polynomial in n for any fixed ε. The running time may grow rapidly as ε decreases (e.g., O(n^{2/ε})).
- **Fully Polynomial-Time Approximation Scheme (FPTAS)**: A PTAS whose running time is polynomial in both n and 1/ε (e.g., O((1/ε)² · n³)). This is the strongest form of approximation guarantee.
- **Lower Bound Technique**: Most proofs of approximation ratios work by comparing the algorithm's solution to a lower bound on the optimal solution (for minimization problems) or an upper bound (for maximization), rather than computing the optimal solution itself.
- **Randomized Approximation**: A randomized ρ(n)-approximation algorithm guarantees that the *expected* cost is within a factor ρ(n) of optimal.

## Algorithms and Techniques

### 1. Vertex Cover — APPROX-VERTEX-COVER (Section 35.1)
- **Problem**: Find a minimum-size vertex cover in an undirected graph.
- **Approach**: Repeatedly pick an arbitrary uncovered edge (u, v), add both endpoints to the cover, and remove all edges incident on u or v.
- **Key Insight**: The set of picked edges forms a maximal matching. No two picked edges share an endpoint, so the optimal cover must include at least one endpoint of each — giving a lower bound of |A| on OPT. The algorithm returns exactly 2|A| vertices.
- **Approximation Ratio**: 2 (Theorem 35.1).
- **Running Time**: O(V + E).

### 2. Traveling-Salesman Problem (Section 35.2)

#### 2a. TSP with Triangle Inequality — APPROX-TSP-TOUR
- **Problem**: Find a minimum-cost Hamiltonian cycle in a complete graph where costs satisfy the triangle inequality.
- **Approach**: (1) Compute a minimum spanning tree T using MST-PRIM. (2) Perform a preorder walk of T to order vertices. (3) Return the Hamiltonian cycle visiting vertices in preorder order.
- **Key Insight**: The MST cost is a lower bound on the optimal tour (deleting one edge from a tour gives a spanning tree). The full walk of the MST costs 2·c(T). By the triangle inequality, skipping repeated vertices does not increase cost, so the preorder tour costs at most 2·c(T) ≤ 2·c(H*).
- **Approximation Ratio**: 2 (Theorem 35.2).
- **Running Time**: Θ(V²).

#### 2b. General TSP — Inapproximability (Theorem 35.3)
- **Result**: If P ≠ NP, then for any constant ρ ≥ 1, there is no polynomial-time ρ-approximation algorithm for the general TSP (without the triangle inequality).
- **Proof Technique**: Given a hypothetical ρ-approximation algorithm, construct a TSP instance from a Hamiltonian-cycle instance where "yes" instances have tour cost |V| and "no" instances have tour cost > ρ|V|. The approximation algorithm would then solve the NP-complete Hamiltonian-cycle problem.

### 3. Set Cover — GREEDY-SET-COVER (Section 35.3)
- **Problem**: Given a universe X and a family F of subsets covering X, find a minimum-size subfamily that still covers X.
- **Approach**: Greedily select the set that covers the most uncovered elements; repeat until all elements are covered.
- **Key Insight**: Each greedy step assigns a cost of 1/(number of newly covered elements) to each newly covered element. A telescoping-sum argument shows the total cost assigned to any set S is at most H(|S|).
- **Approximation Ratio**: H(max{|S| : S ∈ F}), where H(d) is the d-th harmonic number (Theorem 35.4). Equivalently, the ratio is at most ln|X| + 1 (Corollary 35.5).
- **Running Time**: O(|X| · |F| · min(|X|, |F|)), with a linear-time implementation possible.

### 4. Randomization and Linear Programming (Section 35.4)

#### 4a. MAX-3-CNF Satisfiability — Randomized Algorithm
- **Problem**: Given a 3-CNF formula, find an assignment maximizing the number of satisfied clauses.
- **Approach**: Independently set each variable to 1 with probability 1/2 and to 0 with probability 1/2.
- **Key Insight**: Each clause has 3 distinct literals with independent settings. A clause is unsatisfied only when all 3 literals are 0, which happens with probability (1/2)³ = 1/8. So each clause is satisfied with probability 7/8, and the expected number of satisfied clauses is 7m/8, where m is the total number of clauses.
- **Approximation Ratio**: 8/7 (randomized) (Theorem 35.6).

#### 4b. Weighted Vertex Cover — APPROX-MIN-WEIGHT-VC via LP Relaxation
- **Problem**: Find a minimum-weight vertex cover in a weighted graph.
- **Approach**: (1) Formulate as a 0-1 integer linear program. (2) Relax integer constraints to get an LP (0 ≤ x(v) ≤ 1). (3) Solve the LP. (4) Round: include vertex v in the cover if x̄(v) ≥ 1/2.
- **Key Insight**: The LP optimal value z̄ is a lower bound on the optimal integer solution (and hence on OPT). Rounding at threshold 1/2 ensures every edge is covered (since x(u) + x(v) ≥ 1 implies at least one is ≥ 1/2). The rounded solution's weight satisfies w(C) ≤ 2z̄ ≤ 2·w(C*).
- **Approximation Ratio**: 2 (Theorem 35.7).

### 5. Subset-Sum — APPROX-SUBSET-SUM (Section 35.5)
- **Problem**: Given a set S of positive integers and a target t, find a subset whose sum is as large as possible without exceeding t.
- **Approach**: Start with an exact exponential-time algorithm (EXACT-SUBSET-SUM) that iteratively builds lists of all achievable sums. Then apply *trimming* — remove elements from each list that are within a (1 + δ) factor of a retained element, where δ = ε/(2n). This keeps list sizes polynomial.
- **Trimming Procedure**: Scan sorted list L; keep element y only if y > last · (1 + δ). Each retained element "represents" nearby removed elements.
- **Key Insight**: After n iterations of trimming with parameter ε/(2n), the compounded approximation error is at most (1 + ε/(2n))^n ≤ e^{ε/2} ≤ 1 + ε. List sizes are bounded by O(n ln t / ε), making the algorithm polynomial in both n and 1/ε.
- **Approximation Ratio**: (1 + ε) for any ε > 0.
- **Classification**: Fully Polynomial-Time Approximation Scheme (FPTAS) (Theorem 35.8).
- **Running Time**: Polynomial in n, lg t, and 1/ε.

## Complexity Analysis

| Problem | Algorithm | Approximation Ratio | Running Time | Type |
|---|---|---|---|---|
| Vertex Cover | APPROX-VERTEX-COVER | 2 | O(V + E) | Deterministic |
| TSP (triangle ineq.) | APPROX-TSP-TOUR | 2 | Θ(V²) | Deterministic |
| General TSP | — | No constant ratio (unless P=NP) | — | Inapproximable |
| Set Cover | GREEDY-SET-COVER | H(d) ≈ ln n + 1 | O(\|X\|·\|F\|·min(\|X\|,\|F\|)) | Deterministic |
| MAX-3-CNF SAT | Random assignment | 8/7 | O(n + m) | Randomized |
| Weighted Vertex Cover | LP relaxation + rounding | 2 | Poly (LP solve) | Deterministic |
| Subset Sum | APPROX-SUBSET-SUM | 1 + ε | Poly in n, lg t, 1/ε | FPTAS |

## Key Takeaways

- **NP-completeness is not the end of the road.** When a problem is NP-complete, approximation algorithms can deliver provably near-optimal solutions in polynomial time, making them practically useful.
- **Lower bound arguments are central.** Approximation proofs typically compare the algorithm's output to a lower bound on OPT (e.g., maximal matching size, MST cost, LP relaxation value) rather than to OPT itself, which is unknown.
- **Different problems admit different levels of approximability.** Vertex cover and TSP (with triangle inequality) admit constant-factor approximations; set cover admits a logarithmic-factor approximation; subset-sum admits an FPTAS; and the general TSP cannot be approximated at all (unless P = NP).
- **Randomization and LP relaxation are powerful techniques** for designing approximation algorithms, often yielding simple algorithms with strong guarantees.
- **The hierarchy of approximation schemes** — from constant-factor algorithms through PTAS to FPTAS — captures increasingly refined tradeoffs between solution quality, running time, and problem structure.
