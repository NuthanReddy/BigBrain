# 10 Elementary Data Structures

# Elementary Data Structures — Study Notes

## Overview
Elementary data structures are fundamental building blocks in computer science used for organizing and managing data. This chapter discusses the representation of dynamic sets using simple pointer-based structures. Specifically, the text covers **stacks**, **queues**, **linked lists**, and **rooted trees**, along with array-based implementations for some of these structures.

Stacks and queues are dynamic sets where the order of element deletion is prespecified (LIFO for stacks, FIFO for queues), while linked lists provide flexible data storage and manipulation. These structures serve as the backbone for more complex data structures and algorithms.

---

## Key Concepts

- **Dynamic sets**: Collections of elements where operations like insertion, deletion, and queries are supported.
- **Stack (LIFO)**: A data structure where the most recent element added is the first to be removed (Last-In, First-Out).
- **Queue (FIFO)**: A data structure where the first element added is the first to be removed (First-In, First-Out).
- **Linked list**: A collection of nodes arranged linearly using pointers, allowing efficient insertion and deletion.
- **Operations**:
  - **Stack Operations**: `PUSH` (Insert), `POP` (Delete), `STACK-EMPTY` (Check if empty).
  - **Queue Operations**: `ENQUEUE` (Insert), `DEQUEUE` (Delete), `QUEUE-EMPTY` (Check if empty).
  - **Linked List Operations**: `LIST-INSERT`, `LIST-DELETE`, `LIST-SEARCH`.

---

## Algorithms and Techniques

### Stacks
A **stack** is a data structure that supports a LIFO discipline. Only the top item of the stack is accessible at any time.

#### Implementation
A stack of size `n` can be implemented using an array with the following attributes:
- **`S.top`**: Tracks the index of the most recently inserted element in the array.
- **Operations**:
  - When `S.top = 0`, the stack is empty.
  - When `S.top > n`, the stack overflows.

#### Pseudocode

1. **STACK-EMPTY(S)**: Check if the stack is empty.
    ```python
    STACK-EMPTY(S)
    1 if S.top == 0
    2     return TRUE
    3 else 
    4     return FALSE
    ```
    **Time Complexity**: \( O(1) \)

2. **PUSH(S, x)**: Insert an element `x` at the top of the stack.
    ```python
    PUSH(S, x)
    1 S.top = S.top + 1
    2 S[S.top] = x
    ```
    **Time Complexity**: \( O(1) \)

3. **POP(S)**: Remove and return the top element of the stack.
    ```python
    POP(S)
    1 if STACK-EMPTY(S)
    2     error "underflow"
    3 else 
    4     S.top = S.top - 1
    5     return S[S.top + 1]
    ```
    **Time Complexity**: \( O(1) \)

#### Example Illustration
A stack initially empty (`S[1:6]`) undergoes the sequence of operations:

- `PUSH(S, 4)` → {4}
- `PUSH(S, 1)` → {4, 1}
- `PUSH(S, 3)` → {4, 1, 3}
- `POP(S)` → {4, 1} (returns 3)
- `PUSH(S, 8)` → {4, 1, 8}
- `POP(S)` → {4, 1} (returns 8)

#### Edge Cases
- **Stack underflow** occurs if `POP(S)` is called on an empty stack.
- **Stack overflow** occurs if elements exceed the allocated space.

---

### Queues
A **queue** is a data structure that enforces a FIFO discipline. Elements are inserted at the `tail` and removed from the `head`.

#### Implementation
A queue of at most \( n - 1 \) elements can be implemented using an array:
- **Head (`Q.head`)**: Index of the front of the queue.
- **Tail (`Q.tail`)**: Index of the next vacant spot.
- **Circular behavior**: When the `tail` reaches the end of the array, it wraps around to the beginning (index `1`).

#### Operations

1. **ENQUEUE(Q, x)**: Insert an element at the rear of the queue.
    ```python
    ENQUEUE(Q, x)
    1 Q[Q.tail] = x
    2 if Q.tail == Q.length
    3     Q.tail = 1
    4 else 
    5     Q.tail = Q.tail + 1
    ```
    **Time Complexity**: \( O(1) \)

2. **DEQUEUE(Q)**: Remove and return the front element of the queue.
    ```python
    DEQUEUE(Q)
    1 x = Q[Q.head]
    2 if Q.head == Q.length
    3     Q.head = 1
    4 else 
    5     Q.head = Q.head + 1
    6 return x
    ```
    **Time Complexity**: \( O(1) \)

#### Example Illustration
A queue initially empty (`Q[1:6]`) undergoes the sequence of operations:

- `ENQUEUE(Q, 4)` → **Queue:** {4}
- `ENQUEUE(Q, 1)` → **Queue:** {4, 1}
- `ENQUEUE(Q, 3)` → **Queue:** {4, 1, 3}
- `DEQUEUE(Q)` → **Queue:** {1, 3} (returns 4)
- `ENQUEUE(Q, 8)` → **Queue:** {1, 3, 8}
- `DEQUEUE(Q)` → **Queue:** {3, 8} (returns 1)

#### Edge Cases
- **Queue underflow** occurs if `DEQUEUE(Q)` is called on an empty queue.
- **Queue overflow** occurs if elements exceed the allocated space.

---

### Linked Lists
A **linked list** consists of nodes where each node contains:
- A **key** (data).
- **Pointer(s)** to its successor (`next`) and (optionally) predecessor (`prev`).

#### Operations

1. **Search**: Traverse the list to find a node with a specified key.
    ```python
    LIST-SEARCH(L, k)
    1 x = L.head
    2 while x != NIL and x.key != k
    3     x = x.next
    4 return x
    ```
    **Time Complexity**: \( O(n) \)

2. **Insert**: Insert a node at the head of the list.
    ```python
    LIST-INSERT(L, x)
    1 x.next = L.head
    2 if L.head != NIL
    3     L.head.prev = x
    4 L.head = x
    5 x.prev = NIL
    ```
    **Time Complexity**: \( O(1) \)

3. **Delete**: Remove a node from the list using its pointer.
    ```python
    LIST-DELETE(L, x)
    1 if x.prev != NIL
    2     x.prev.next = x.next
    3 else 
    4     L.head = x.next
    5 if x.next != NIL
    6     x.next.prev = x.prev
    ```
    **Time Complexity**: \( O(1) \)

#### Example Illustration
Consider the doubly linked list `{1, 4, 9, 16}`:
- Insert `25`: `{25, 1, 4, 9, 16}`
- Delete `4`: `{25, 1, 9, 16}`

#### Circular Lists
If implemented as circular, the last node points to the first node, simplifying some operations.

---

## Complexity Analysis

| Data Structure | Insert          | Delete          | Search          |
|----------------|-----------------|-----------------|-----------------|
| Stack          | \( O(1) \)     | \( O(1) \)     | \( O(n) \)     |
| Queue          | \( O(1) \)     | \( O(1) \)     | \( O(n) \)     |
| Linked List    | \( O(1) \)     | \( O(1) \)     | \( O(n) \)     |

---

## Conclusion
Elementary data structures like **stacks**, **queues**, and **linked lists** are crucial for many algorithms. Mastery of their implementation and operations enables efficient data management and lays the foundation for understanding more complex data structures. Use these structures as building blocks for dynamic memory allocation, buffering systems, and more.
