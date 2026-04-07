# Chapter 34: NP-Completeness

## Overview

This chapter introduces the theory of NP-completeness, which provides a framework for understanding computational intractability. It formalizes the complexity classes P, NP, and NPC (NP-complete), and establishes the foundational methodology of polynomial-time reductions for proving that problems are NP-complete. The chapter demonstrates this methodology through a chain of reductions starting from the circuit-satisfiability problem and extending to several classic NP-complete problems.

## Key Concepts

- **Class P**: The set of decision problems solvable in polynomial time O(n^k) for some constant k. Problems in P are considered "tractable."
- **Class NP**: The set of decision problems for which a proposed solution (certificate) can be *verified* in polynomial time. Every problem in P is also in NP (P ⊆ NP).
- **NP-Complete (NPC)**: A problem is NP-complete if (1) it is in NP, and (2) every problem in NP is polynomial-time reducible to it. These are the "hardest" problems in NP.
- **NP-Hard**: A problem satisfying condition (2) above, but not necessarily in NP itself. NP-hard problems are at least as hard as any NP problem.
- **The P ≠ NP Question**: The central open question — whether every problem whose solution can be verified quickly can also be *solved* quickly. Most researchers believe P ≠ NP.
- **Decision vs. Optimization Problems**: NP-completeness applies to decision problems (yes/no answers). Optimization problems can be cast as decision problems by bounding the value to be optimized.
- **Certificates and Verification**: A certificate is a proposed solution; a verifier checks it in polynomial time. For example, a Hamiltonian cycle in a graph serves as a certificate for HAM-CYCLE.
- **Encodings**: Problems must be encoded as binary strings. The choice of encoding matters (e.g., unary vs. binary), but "reasonable" encodings are polynomially related and do not affect membership in P.
- **Formal Language Framework**: Decision problems are modeled as languages over {0,1}*. A language L is in P if there is a polynomial-time algorithm that decides L (accepts strings in L, rejects strings not in L).
- **co-NP**: The class of languages whose complements are in NP. Whether NP = co-NP is an open question.

## Algorithms and Techniques

### Polynomial-Time Reductions
- A language L₁ is polynomial-time reducible to L₂ (written L₁ ≤_P L₂) if there exists a polynomial-time computable function f such that x ∈ L₁ if and only if f(x) ∈ L₂.
- If L₁ ≤_P L₂ and L₂ ∈ P, then L₁ ∈ P (Lemma 34.3).
- Reductions are transitive: if L₁ ≤_P L₂ and L₂ ≤_P L₃, then L₁ ≤_P L₃.

### Methodology for Proving NP-Completeness
1. Show that L ∈ NP (exhibit a polynomial-time verifier with a certificate).
2. Select a known NP-complete language L'.
3. Describe a polynomial-time reduction from L' to L.
4. Prove correctness: x ∈ L' if and only if f(x) ∈ L.
5. Prove the reduction runs in polynomial time.

### The Chain of Reductions
The chapter establishes NP-completeness through a chain of reductions:

- **CIRCUIT-SAT** (circuit satisfiability) — the "first" NP-complete problem, proved directly by showing every NP language reduces to it (Theorem 34.7). The proof constructs a combinational circuit that simulates the computation of any polynomial-time verifier.
- **CIRCUIT-SAT →_P SAT** (formula satisfiability) — introduces a variable for each wire and expresses gate operations as clauses (Theorem 34.9, the Cook-Levin theorem).
- **SAT →_P 3-CNF-SAT** — converts arbitrary Boolean formulas to 3-CNF through parse-tree transformation, truth-table-based CNF conversion, and padding clauses to exactly 3 literals (Theorem 34.10).
- **3-CNF-SAT →_P CLIQUE** — maps each clause to a triple of vertices; edges connect consistent literals from different clauses. A satisfying assignment corresponds to a k-clique (Theorem 34.11).
- **CLIQUE →_P VERTEX-COVER** — uses graph complementation: G has a clique of size k if and only if the complement graph has a vertex cover of size |V| − k (Theorem 34.12).
- **VERTEX-COVER →_P HAM-CYCLE** — uses a widget construction with 12 vertices per edge to encode the structure of vertex covers as Hamiltonian paths through widgets (Theorem 34.13).
- **HAM-CYCLE →_P TSP** (Traveling Salesman Problem) — assigns cost 0 to edges in G and cost 1 to non-edges; G has a Hamiltonian cycle iff the complete graph has a tour of cost 0 (Theorem 34.14).
- **3-CNF-SAT →_P SUBSET-SUM** — encodes variables and clauses as digits in base-10 numbers; a satisfying assignment corresponds to a subset summing to a target value (Theorem 34.15).

## Complexity Analysis

- **Theorem 34.2**: P equals the class of languages accepted in polynomial time (acceptance and decision are equivalent for polynomial-time).
- **Lemma 34.1**: If two encodings are polynomially related, membership in P is encoding-independent.
- **Theorem 34.4**: If any NP-complete problem is in P, then P = NP. Equivalently, if any NP problem is not in P, then no NP-complete problem is in P.
- **Theorem 34.7**: CIRCUIT-SAT is NP-complete — proved by showing every NP language reduces to it via simulation of the verifier's computation as a Boolean circuit of polynomial size.
- **Contrasting tractable and intractable pairs**:
  - Shortest path (polynomial) vs. Longest simple path (NP-complete)
  - Euler tour O(E) vs. Hamiltonian cycle (NP-complete)
  - 2-CNF satisfiability (polynomial) vs. 3-CNF satisfiability (NP-complete)
- All reductions in the chapter are polynomial-time, preserving the structure of NP-completeness proofs.

## Key Takeaways

- **NP-completeness is the gold standard for evidence of intractability.** If you prove a problem is NP-complete, you provide strong evidence (though not proof) that no polynomial-time algorithm exists for it.
- **The reduction methodology is cumulative.** Once one problem is proved NP-complete, others follow by polynomial-time reduction from any known NP-complete problem, creating a growing catalog.
- **Proving NP-completeness has practical value.** If your problem is NP-complete, invest effort in approximation algorithms, heuristics, or solving tractable special cases rather than searching for an exact polynomial-time algorithm.
- **P ⊆ NP is known, but whether P = NP remains open.** This is one of the deepest questions in computer science and mathematics, with implications across all of science and engineering.
- **The chapter establishes a reduction tree rooted at CIRCUIT-SAT**, branching through SAT, 3-CNF-SAT, CLIQUE, VERTEX-COVER, HAM-CYCLE, TSP, and SUBSET-SUM — demonstrating the universality and interconnectedness of NP-complete problems across logic, graphs, and arithmetic.
