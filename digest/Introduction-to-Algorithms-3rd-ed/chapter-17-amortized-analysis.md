# Chapter 17: Amortized Analysis

## Overview
Amortized analysis determines the average cost per operation over a worst-case sequence of operations on a data structure, without using probability. Even though a single operation may occasionally be expensive, amortized analysis shows that the average cost across all operations is small. The chapter presents three techniques — aggregate analysis, the accounting method, and the potential method — applying each to stack operations with MULTIPOP and binary counter INCREMENT. It culminates with a detailed analysis of dynamic tables that expand and contract, proving O(1) amortized cost per insertion and deletion.

## Key Concepts

- **Amortized vs. average-case analysis**: Amortized analysis guarantees average performance per operation in the worst case over any sequence of operations. It does not use probability or assume anything about the input distribution — it is a worst-case guarantee on the total cost of n operations.
- **Three techniques**:
  - **Aggregate analysis**: Compute an upper bound T(n) on the total cost of n operations; the amortized cost per operation is T(n)/n. All operations receive the same amortized cost.
  - **Accounting method**: Assign different amortized costs (charges) to different operation types. Early operations may be overcharged, storing the excess as "credit" on objects; later operations spend this credit. The key invariant: total credit must remain nonnegative at all times.
  - **Potential method**: Define a potential function Φ mapping data structure states to real numbers. The amortized cost of operation i is ĉ_i = c_i + Φ(D_i) − Φ(D_{i−1}). If Φ(D_n) ≥ Φ(D_0) for all n, total amortized cost upper-bounds total actual cost.
- **Charges are for analysis only**: Amortized costs and credits/potentials are analytical tools. They do not appear in the code or affect the algorithm's behavior.
- **The potential function telescopes**: Total amortized cost = total actual cost + Φ(D_n) − Φ(D_0). Choosing Φ(D_0) = 0 and ensuring Φ(D_i) ≥ 0 guarantees the upper bound.
- **Load factor**: For dynamic tables, α(T) = T.num / T.size measures how full the table is. Maintaining a constant lower bound on α ensures wasted space is bounded.

## Algorithms and Techniques

### 1. Stack with MULTIPOP — All Three Methods

**Setup**: A stack supports PUSH (cost 1), POP (cost 1), and MULTIPOP(S, k) (pops min(k, s) items, cost = min(k, s), where s is stack size).

**Aggregate analysis**:
- Naive bound: Each MULTIPOP costs O(n), giving O(n²) for n operations.
- Tighter: Each item can be popped at most once per push. Total POPs (including within MULTIPOP) ≤ total PUSHes ≤ n. So total cost = O(n), amortized O(1) per operation.

**Accounting method**:
- Assign amortized costs: PUSH = 2, POP = 0, MULTIPOP = 0.
- On each PUSH, pay 1 for the actual push and place 1 credit on the item.
- POP and MULTIPOP consume pre-placed credits. Credit is always nonnegative (every item on the stack has exactly 1 credit), so total amortized cost O(n) upper-bounds total actual cost.

**Potential method**:
- Define Φ(D_i) = number of items on stack after the ith operation.
- Φ(D_0) = 0, Φ(D_i) ≥ 0 always.
- PUSH: ĉ = 1 + (s+1 − s) = 2.
- POP: ĉ = 1 + (s−1 − s) = 0.
- MULTIPOP(k'): ĉ = k' + (s−k' − s) = 0.
- All amortized costs are O(1); total is O(n).

### 2. Binary Counter INCREMENT — All Three Methods

**Setup**: A k-bit counter A[0..k−1] counts upward. INCREMENT flips bits from low to high: reset consecutive 1s to 0, then set the next 0 to 1.

**Aggregate analysis**:
- Naive: Each INCREMENT flips up to k bits → O(nk) for n operations.
- Tighter: Bit A[i] flips ⌊n/2^i⌋ times. Total flips = Σ_{i=0}^{k−1} ⌊n/2^i⌋ < n · Σ_{i=0}^{∞} 1/2^i = 2n.
- Amortized cost per INCREMENT: O(2n)/n = O(1).

**Accounting method**:
- Charge 2 to set a bit to 1 (1 for the set, 1 as credit on the bit).
- Resetting a bit to 0 costs 0 (paid by the credit on that bit).
- Each INCREMENT sets at most one bit to 1 → amortized cost ≤ 2 per INCREMENT.
- Total credit (number of 1s × $1) is always nonnegative.

**Potential method**:
- Define Φ(D_i) = b_i (number of 1-bits after the ith INCREMENT).
- If INCREMENT resets t_i bits: actual cost c_i ≤ t_i + 1; potential change ≤ (b_{i−1} − t_i + 1) − b_{i−1} = 1 − t_i.
- Amortized cost: ĉ_i ≤ (t_i + 1) + (1 − t_i) = 2.
- For a counter starting at b_0: total actual cost ≤ 2n − b_n + b_0. If n = Ω(k), this is O(n) regardless of initial value.

### 3. Dynamic Tables (Section 17.4)

**Table Expansion (TABLE-INSERT only)**:
- **Strategy**: When the table is full (T.num = T.size), allocate a new table of double the size, copy all items.
- **TABLE-INSERT cost**: 1 for a normal insert; i for the ith insert if it triggers expansion (copy i−1 items plus the new insert).
- **Aggregate analysis**: Expansions occur when i−1 is an exact power of 2. Total cost ≤ n + Σ_{j=0}^{⌊lg n⌋} 2^j < 3n. Amortized cost per insert ≤ 3.
- **Accounting method intuition**: Charge 3 per insert — 1 for the insert itself, 1 as credit on the item, 1 as credit on an existing item. By the next expansion, every item has a dollar to pay for being copied.
- **Potential method**: Φ(T) = 2·T.num − T.size. Φ = 0 right after expansion; Φ = T.num right before expansion. Amortized cost of each TABLE-INSERT = 3 (whether or not expansion occurs).

**Table Expansion and Contraction (TABLE-INSERT and TABLE-DELETE)**:
- **Naive contraction at 1/2 full fails**: Alternating inserts and deletes near the threshold causes Θ(n) work per operation (thrashing between expansion and contraction).
- **Better strategy**: Double on full (α = 1), halve when α drops below 1/4 (not 1/2). This ensures α ≥ 1/4 always.
- **Potential function** (equation 17.6):
  - Φ(T) = 2·T.num − T.size if α(T) ≥ 1/2
  - Φ(T) = T.size/2 − T.num if α(T) < 1/2
- **Properties**: Φ = 0 when α = 1/2 (ideal); Φ = T.num when α = 1 (ready to pay for expansion); Φ = T.num when α = 1/4 (ready to pay for contraction). Φ ≥ 0 always.
- **Amortized costs**: TABLE-INSERT ≤ 3, TABLE-DELETE ≤ 2. Both are O(1).
- **Result**: Any sequence of n TABLE-INSERT and TABLE-DELETE operations on a dynamic table takes O(n) total time.

## Complexity Analysis

| Data Structure / Operation | Worst-case per op | Amortized per op | Total for n ops |
|---|---|---|---|
| Stack PUSH | O(1) | O(1) | O(n) |
| Stack POP | O(1) | O(1) | O(n) |
| Stack MULTIPOP(k) | O(n) | O(1) | O(n) |
| Binary counter INCREMENT | O(k) | O(1) | O(n) |
| TABLE-INSERT (expansion only) | O(n) | O(1) (≤ 3) | O(n) |
| TABLE-INSERT (with contraction) | O(n) | O(1) (≤ 3) | O(n) |
| TABLE-DELETE (with contraction) | O(n) | O(1) (≤ 2) | O(n) |

**Key insight**: Operations that are occasionally expensive (MULTIPOP, INCREMENT with many flips, table expansion/contraction) cannot happen frequently — the expensive operations are "paid for" by the cheaper ones.

## Key Takeaways

- **Amortized ≠ average-case**: Amortized analysis provides worst-case guarantees on total cost without probabilistic assumptions. It is a deterministic analysis technique that bounds the cost of any sequence of n operations.
- **Three complementary techniques**: Aggregate analysis is simplest (assigns uniform amortized cost). The accounting method offers intuition through credits on objects. The potential method is most powerful and flexible — a well-chosen potential function makes complex analyses tractable.
- **The potential method is the go-to for complex structures**: For dynamic tables with both expansion and contraction, the piecewise potential function Φ elegantly captures how the data structure "saves up" for expensive restructuring operations, yielding O(1) amortized bounds.
- **Avoid thrashing in dynamic tables**: Contracting at α = 1/2 (the expansion threshold) causes pathological behavior. The asymmetric strategy — expand at α = 1, contract at α = 1/4 — ensures the load factor stays in [1/4, 1] and amortized costs remain O(1).
- **Amortized analysis has broad applications**: Beyond the examples in this chapter, it is fundamental to analyzing union-find data structures (Chapter 21), splay trees, Fibonacci heaps, and many other advanced data structures where occasional costly restructuring is amortized over many cheap operations.
