# Chapter 29: Linear Programming

## Overview
This chapter introduces linear programming (LP), a powerful optimization framework for maximizing or minimizing a linear objective function subject to linear constraints. Linear programming has vast practical applications—from resource allocation and scheduling to network flow and approximation algorithms. The chapter develops the **simplex algorithm**, a practical (though worst-case exponential) method for solving LPs, and establishes the theoretical foundation of **LP duality**, which proves that every LP has a dual whose optimal value equals that of the primal.

## Key Concepts

- **Linear program**: optimize a linear function (the **objective function**) subject to a finite set of linear equalities and inequalities (the **constraints**). Variables may be subject to nonnegativity constraints.
- **Standard form**: maximize cᵀx subject to Ax ≤ b and x ≥ 0, where A is an m×n matrix, b ∈ ℝᵐ, and c ∈ ℝⁿ.
- **Slack form**: convert inequality constraints to equalities by introducing **slack variables**: xₙ₊ᵢ = bᵢ - Σaᵢⱼxⱼ. The LP is then represented by equalities and nonnegativity constraints on all variables.
  - **Basic variables**: the left-hand side variables in the slack-form equations (initially the slack variables).
  - **Nonbasic variables**: the right-hand side variables (initially the original decision variables).
  - A **basic feasible solution** sets all nonbasic variables to 0 and reads off basic variable values.
- **Feasible solution**: any assignment of variables satisfying all constraints.
- **Feasible region**: the set of all feasible solutions—a convex polytope in n-dimensional space.
- **Optimal solution**: a feasible solution that achieves the best (max or min) objective value.
- **Unbounded LP**: feasible but the objective can be made arbitrarily large (for maximization).
- **Infeasible LP**: no feasible solution exists.
- Any LP can be converted to standard form via variable substitution (replacing unconstrained variables with pairs of nonneg variables, flipping inequality directions, converting equalities to pairs of inequalities).
- LP generalizes many optimization problems: shortest paths, maximum flow, minimum-cost flow, and multicommodity flow can all be formulated as LPs.

## Algorithms and Techniques

### The Simplex Algorithm (SIMPLEX)
The simplex method iteratively moves from one vertex (basic feasible solution) of the feasible polytope to an adjacent vertex with a better objective value.

**Each iteration (pivot step):**
1. **Select entering variable**: choose a nonbasic variable xₑ with a positive coefficient in the objective function (entering the basis increases the objective value).
2. **Select leaving variable**: among basic variables, find the one that most tightly constrains how much xₑ can increase (prevents any basic variable from going negative). This variable xₗ leaves the basis.
3. **Pivot**: rewrite the equation for xₗ to express xₑ, then substitute throughout to maintain slack form.

**Termination**: when no nonbasic variable has a positive coefficient in the objective function, the current solution is optimal.

### PIVOT(N, B, A, b, c, v, l, e)
- Performs one pivot operation: swaps the leaving variable xₗ and entering variable xₑ between the basis and non-basis.
- Rewrites all equations and the objective function accordingly.
- Running time: O(nm) per pivot.

### INITIALIZE-SIMPLEX(A, b, c)
- Handles the problem of finding an initial basic feasible solution.
- If all bᵢ ≥ 0, the origin (all nonbasic variables = 0) is feasible.
- Otherwise, constructs an **auxiliary LP** (Lₐᵤₓ) by adding an extra variable x₀ and minimizing x₀ subject to modified constraints. If the optimal value of x₀ is 0, a feasible starting point for the original LP exists; otherwise the original LP is infeasible.
- Running time: dominated by simplex iterations on the auxiliary problem.

### LP Duality
- Every LP (the **primal**) has an associated **dual LP**.
- If the primal is: maximize cᵀx subject to Ax ≤ b, x ≥ 0, then the dual is: minimize bᵀy subject to Aᵀy ≥ c, y ≥ 0.
- **Weak duality (Lemma 29.8)**: any feasible dual solution provides an upper bound on the optimal primal value.
- **Strong duality / LP Duality Theorem (Theorem 29.10)**: if the primal has an optimal solution x* with value z*, then the dual also has an optimal solution y* with value z* = bᵀy*. The optimal values are equal.
- Duality provides optimality certificates: if primal and dual feasible solutions achieve the same objective, both are optimal.

### Fundamental Theorem of Linear Programming (Theorem 29.13)
For any LP in standard form:
1. If it has no optimal solution, it is either infeasible or unbounded.
2. If it has a feasible solution, it has a basic feasible solution.
3. If it has an optimal solution, it has an optimal basic feasible solution.

This justifies the simplex algorithm's strategy of searching only vertices.

## Complexity Analysis

- **Simplex algorithm**: each pivot takes O(nm) time. The number of pivots can be exponential in the worst case (there exist pathological examples), but in practice simplex is very efficient—typically polynomial in the number of constraints and variables.
- **Bland's rule** (choosing the smallest-index entering/leaving variable) guarantees termination by preventing cycling, ensuring the simplex algorithm always terminates.
- **Lemma 29.2**: slack-form representations are unique for a given set of basic variables.
- **Lemma 29.1**: the conversion between standard form and slack form is straightforward and takes O(nm) time.
- While the simplex algorithm is not polynomial-time in the worst case, polynomial-time algorithms for LP exist:
  - **Ellipsoid method** (Khachiyan, 1979): first polynomial-time LP algorithm.
  - **Interior-point methods** (Karmarkar, 1984): practical polynomial-time algorithms.

## Key Takeaways

- **Linear programming is extraordinarily versatile**: shortest paths, max flow, min-cost flow, and many other optimization problems reduce to LP, making it one of the most broadly applicable optimization frameworks.
- **The simplex algorithm** works by walking along vertices of the feasible polytope, always improving the objective, until reaching an optimum. Despite exponential worst-case behavior, it is fast in practice.
- **LP duality** is both theoretically elegant and practically useful: it provides optimality certificates and is foundational to approximation algorithms and combinatorial optimization.
- **Every LP is either infeasible, unbounded, or has an optimal solution at a vertex** of the feasible region (Fundamental Theorem), which justifies vertex-enumeration approaches.
- **Initialization matters**: finding an initial feasible solution when the origin is infeasible requires solving an auxiliary LP, which is a nontrivial algorithmic step handled by INITIALIZE-SIMPLEX.
