# Chapter 10: Elementary Data Structures

## Overview
This chapter introduces the fundamental building blocks for representing dynamic sets using simple pointer-based data structures. It covers stacks, queues, linked lists, and rooted trees—the rudimentary structures upon which more complex data structures are built. The chapter also demonstrates how to synthesize objects and pointers from arrays, which is essential for languages or environments without native pointer support.

## Key Concepts

- **Dynamic sets**: Collections of elements that support operations like INSERT, DELETE, and SEARCH. The data structures in this chapter provide different tradeoffs for these operations.
- **Stacks (LIFO policy)**: The element removed by DELETE is always the most recently inserted element. Supported by PUSH (insert) and POP (delete) operations. Implemented using an array `S[1..n]` with a `top` attribute tracking the most recently inserted element. An empty stack has `S.top = 0`. Underflow occurs when popping an empty stack; overflow when the stack exceeds capacity.
- **Queues (FIFO policy)**: The element removed by DELETE is the one that has been in the set the longest. Supported by ENQUEUE (insert at tail) and DEQUEUE (delete from head). Implemented using a circular array `Q[1..n]` with `head` and `tail` attributes that wrap around, enabling the queue to use all `n − 1` available slots.
- **Linked lists**: Objects arranged in a linear order determined by pointers (not array indices). A **doubly linked list** stores `key`, `next`, and `prev` pointers in each node. Variations include singly linked, sorted/unsorted, and circular lists.
- **Sentinels**: Dummy objects (e.g., `L.nil`) that simplify boundary-condition handling. A sentinel turns a regular doubly linked list into a **circular doubly linked list**, eliminating special cases for head/tail operations. Sentinels rarely improve asymptotic bounds but simplify code and may reduce constant factors.
- **Multiple-array representation of objects**: Simulates objects using parallel arrays (e.g., `key[]`, `next[]`, `prev[]`) where a common index represents one object.
- **Single-array representation of objects**: Stores each object in a contiguous subarray, with offsets for each attribute. A pointer is simply the starting index of the subarray.
- **Free lists**: A singly linked list of unused object slots managed like a stack. `ALLOCATE-OBJECT` pops from the free list; `FREE-OBJECT` pushes onto it. Both run in O(1) time.
- **Rooted trees**: Represented using pointer-based nodes. Binary trees use `p`, `left`, and `right` attributes. Trees with unbounded branching use the **left-child, right-sibling representation**, which stores only `left-child` and `right-sibling` pointers per node, achieving O(n) space for any n-node tree.

## Algorithms and Techniques

### Stack Operations
- **STACK-EMPTY(S)**: Returns TRUE if `S.top == 0`.
- **PUSH(S, x)**: Increments `S.top` and stores `x` at the new top position.
- **POP(S)**: Checks for underflow, decrements `S.top`, and returns the element that was at the top.

### Queue Operations
- **ENQUEUE(Q, x)**: Stores `x` at `Q[Q.tail]`, then advances `Q.tail` circularly (wrapping from position `n` back to position 1).
- **DEQUEUE(Q)**: Reads and returns `Q[Q.head]`, then advances `Q.head` circularly.

### Linked List Operations
- **LIST-SEARCH(L, k)**: Linear scan from `L.head` following `next` pointers until key `k` is found or the list is exhausted.
- **LIST-INSERT(L, x)**: Splices node `x` at the front of the list in O(1) time by updating head and predecessor pointers.
- **LIST-DELETE(L, x)**: Removes node `x` by updating its predecessor's `next` and successor's `prev` pointers. Runs in O(1) given a pointer to `x`; but finding `x` by key requires Θ(n) search.

### Sentinel-Based Variants
- `LIST-SEARCH'`, `LIST-INSERT'`, `LIST-DELETE'` use the sentinel `L.nil` to eliminate boundary checks, producing simpler code.

### Object Allocation
- **ALLOCATE-OBJECT()**: Pops the head of the free list and returns it. Signals an error if the free list is empty.
- **FREE-OBJECT(x)**: Pushes `x` onto the free list by setting `x.next = free` and `free = x`.

### Tree Representations
- **Binary trees**: Each node stores `p` (parent), `left`, and `right` pointers.
- **Left-child, right-sibling representation**: For trees with unbounded branching. Each node stores `p`, `left-child`, and `right-sibling`. The leftmost child is accessed via `left-child`, and siblings are traversed via `right-sibling`.

## Complexity Analysis

| Operation | Data Structure | Time Complexity |
|---|---|---|
| PUSH, POP, STACK-EMPTY | Stack (array) | O(1) |
| ENQUEUE, DEQUEUE | Queue (circular array) | O(1) |
| LIST-INSERT | Doubly linked list | O(1) |
| LIST-DELETE (given pointer) | Doubly linked list | O(1) |
| LIST-SEARCH | Doubly linked list | Θ(n) worst case |
| ALLOCATE-OBJECT | Free list | O(1) |
| FREE-OBJECT | Free list | O(1) |

- **Space**: All representations use O(n) space for n elements. Sentinels add O(1) overhead per list but can waste significant memory when many small lists each carry their own sentinel.
- **COMPACT-LIST-SEARCH** (Problem 10-3): A randomized algorithm for searching a sorted compact linked list achieves O(√n) expected time by combining random skipping with sequential traversal.

## Key Takeaways

- **Stacks and queues** are the simplest dynamic sets, both achievable with arrays in O(1) time per operation. Stacks enforce LIFO order; queues enforce FIFO order using a circular buffer.
- **Linked lists** offer flexible, pointer-based storage where insertion and deletion (given a pointer) are O(1), but search is O(n). Doubly linked lists allow O(1) deletion; singly linked lists require traversal to find the predecessor.
- **Sentinels** simplify code by eliminating boundary-condition checks but do not improve asymptotic performance. Use them judiciously—they waste memory when applied to many small lists.
- **Objects can be simulated with arrays** using either multiple parallel arrays or a single array with offsets, enabling linked data structures in environments without pointers.
- **The left-child, right-sibling representation** is an elegant O(n)-space scheme for representing rooted trees with arbitrary branching factor, avoiding the waste of fixed child-pointer arrays.
