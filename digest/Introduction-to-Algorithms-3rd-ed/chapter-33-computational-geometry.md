# Chapter 33: Computational Geometry

## Overview
This chapter introduces algorithmic techniques for solving geometric problems in two dimensions. It covers foundational primitives (cross products, segment intersection tests), the **sweep line** paradigm for detecting segment intersections, two algorithms for computing **convex hulls** (Graham's scan and Jarvis's march), and a divide-and-conquer algorithm for the **closest pair of points** problem. These techniques illustrate how geometric structure can be exploited for efficient algorithms that avoid expensive operations like division and trigonometry.

## Key Concepts

- **Cross product** of vectors p₁ = (x₁, y₁) and p₂ = (x₂, y₂): p₁ × p₂ = x₁y₂ − x₂y₁. This gives the signed area of the parallelogram formed by the vectors.
  - Positive: p₂ is counterclockwise from p₁.
  - Negative: p₂ is clockwise from p₁.
  - Zero: p₁ and p₂ are collinear.
- **Determining turns**: given consecutive points p₀, p₁, p₂, the cross product (p₁ − p₀) × (p₂ − p₀) determines whether the path p₀→p₁→p₂ turns left (positive), right (negative), or goes straight (zero).
- **Segment intersection test** (SEGMENTS-INTERSECT): two segments p₁p₂ and p₃p₄ intersect if and only if they **straddle** each other's lines—determined entirely by cross products and an on-segment collinearity check. Runs in O(1) time using only additions, subtractions, multiplications, and comparisons (no division or trig).
- **Convex hull** CH(Q): the smallest convex polygon containing all points in Q. Vertices of the convex hull are a subset of Q. Can be visualized as the shape formed by a rubber band stretched around all points.
- **Sweep line** technique: an imaginary vertical line sweeps left to right across the plane, maintaining a data structure of "active" objects ordered by their y-coordinate at the sweep line's current position. Events (segment endpoints) trigger updates.

## Algorithms and Techniques

### SEGMENTS-INTERSECT(p₁, p₂, p₃, p₄)
- Uses four cross-product computations (directions) to determine if segments straddle each other.
- Handles the special case of collinear segments via the ON-SEGMENT test.
- Running time: O(1).

### ANY-SEGMENTS-INTERSECT(S) — Sweep Line Algorithm
- Determines whether **any pair** among n line segments intersects.
- **Approach**: sweep a vertical line from left to right; maintain a balanced BST (ordered by y-coordinate) of segments currently crossing the sweep line.
- **Events** (sorted by x-coordinate):
  - **Left endpoint**: insert segment into the BST; check for intersection with its neighbors above and below.
  - **Right endpoint**: remove segment from BST; check if its former neighbors (now adjacent) intersect.
- **Correctness** (Theorem 33.1): if any intersection exists, the algorithm detects it—proved by showing that intersecting segments must become adjacent in the sweep-line order at some point before they actually cross.
- Running time: **O(n lg n)** — sorting endpoints takes O(n lg n), and each of the 2n events involves O(lg n) BST operations.
- Simplifying assumption: no three segments share a common point, no vertical segments, and no two endpoints share the same x-coordinate.

### GRAHAM-SCAN(Q) — Convex Hull
- Computes the convex hull of n points using a **stack-based rotational sweep**.
- **Algorithm**:
  1. Choose p₀ as the point with the lowest y-coordinate (leftmost if tied)—guaranteed to be on the hull.
  2. Sort remaining points by polar angle relative to p₀.
  3. Process points in sorted order, maintaining a stack S of hull candidates.
  4. For each new point pᵢ: while the angle at TOP(S) between NEXT-TO-TOP(S), TOP(S), and pᵢ makes a non-left turn (clockwise or collinear), pop from S. Then push pᵢ.
- **Correctness**: at termination, S contains exactly the vertices of CH(Q) in counterclockwise order.
- Running time: **O(n lg n)** — dominated by sorting. The stack operations are O(n) amortized (each point is pushed and popped at most once).

### JARVIS-MARCH(Q) — Gift Wrapping
- Constructs the convex hull by **wrapping** around the point set, one edge at a time.
- Starting from the lowest point, repeatedly selects the point that makes the smallest counterclockwise angle from the current edge direction.
- Each step involves a linear scan of all points to find the next hull vertex.
- Running time: **O(nh)** where h is the number of hull vertices. This is **output-sensitive**: efficient when h is small, but can be O(n²) in the worst case (e.g., when all points are on the hull).

### CLOSEST-PAIR(Q) — Divide and Conquer
- Finds the two closest points among n points in the plane.
- **Algorithm**:
  1. **Divide**: sort points by x-coordinate. Split into left half Pₗ and right half Pᵣ at the median x-coordinate.
  2. **Conquer**: recursively find closest pairs in Pₗ and Pᵣ. Let δ = min(δₗ, δᵣ).
  3. **Combine**: the closest pair might span the dividing line. Consider only points within distance δ of the dividing line (the **strip**). For each point in the strip (sorted by y), compare it with at most 7 subsequent points in the strip (a key geometric argument limits comparisons).
- The O(n) combine step relies on a **sparsity argument**: at most 8 points can lie in any δ × 2δ rectangle straddling the dividing line.
- Running time: T(n) = 2T(n/2) + O(n) = **O(n lg n)** — using a presorted list by y-coordinate passed through the recursion to avoid re-sorting.

## Complexity Analysis

| Algorithm | Time Complexity | Notes |
|---|---|---|
| Segment intersection test | O(1) | Cross products only |
| ANY-SEGMENTS-INTERSECT | O(n lg n) | Sweep line + BST |
| GRAHAM-SCAN | O(n lg n) | Sort + amortized stack |
| JARVIS-MARCH | O(nh) | Output-sensitive; h = hull vertices |
| CLOSEST-PAIR | O(n lg n) | Divide and conquer |

## Key Takeaways

- **Cross products are the fundamental primitive** of 2D computational geometry: they determine turns, orientation, and collinearity using only multiplication and subtraction—avoiding numerically unstable division and trigonometry.
- **The sweep-line technique** is a powerful paradigm that transforms 2D geometric problems into 1D data structure problems, enabling O(n lg n) solutions for intersection detection and many other problems.
- **Graham's scan** computes the convex hull optimally in O(n lg n) time; Jarvis's march is preferred when the hull has few vertices (h ≪ n), achieving O(nh) time. The best known algorithm achieves O(n lg h).
- **The closest-pair algorithm** demonstrates how divide-and-conquer applies to geometric problems: the critical insight is that the "combine" step only needs to check a constant number of neighbors per point in the boundary strip.
- **Avoiding numerical pitfalls** is a recurring theme: all algorithms in this chapter carefully avoid division and trigonometric functions, relying instead on cross products and integer/exact arithmetic for robustness.
