# 11 Hash Tables

```markdown
# Hash Tables Study Notes

## Overview
This study note covers Chapter 11 of "Introduction to Algorithms, Third Edition," which focuses on **Hash Tables**, a practical and efficient way of implementing dictionaries. Hash tables use a hashing strategy for storage and retrieval, ensuring average-case constant time complexity, i.e., **O(1)**, for operations like `INSERT`, `SEARCH`, and `DELETE`. Key concepts include **direct addressing**, **hashing functions**, **collision resolution strategies** (chaining and open addressing), and **perfect hashing**. These methods play a fundamental role in computing, such as storing symbol tables in compilers.

---

## Key Concepts
- **Dynamic Set**: A data structure supporting three key operations:
  - `INSERT(x)`: Adds an element `x` to the set.
  - `SEARCH(k)`: Finds an element with key `k`.
  - `DELETE(x)`: Removes an element `x` from the set.
  
- **Direct Addressing**:
  - A technique where each key maps directly to an index in an array.
  - Efficient when the key space (`U`) is small.
  - Operations perform in **O(1)** time in the worst case.

- **Hashing**:
  - Reduces storage requirements and maps keys via a **hash function** to a smaller table.
  - Effective when the key set size (`K`) is much smaller than the key universe (`U`).

- **Collisions**:
  - Occur when two keys map to the same location in a hash table.
  - Resolved using strategies such as **chaining** or **open addressing**.

- **Chaining**:
  - Colliding elements are stored in linked lists at the same index.

- **Load Factor (α)**:
  - Defined as `n / m`, where `n` is the number of elements in the table and `m` is the number of slots.
  - Performance depends on the load factor.

- **Hash Functions**:
  - Deterministic functions that map keys to indices in a hash table.
  - Good hash functions aim to uniformly distribute keys to minimize collisions.

- **Average-Case Performance**:
  - Though the worst-case search time can be **O(n)**, a properly designed hash function ensures average-case performance of constant time.

- **Perfect Hashing**:
  - Ensures no collisions occur when the key set is static.

---

## Algorithms and Techniques

### Direct Addressing

#### How It Works
When the size of the key universe (`U`) is small, each key can map directly to its slot in an array. If the set of keys (`K`) is sparse relative to `U`, unused slots hold a default value, e.g., `NIL`. It assumes keys are unique.

#### Pseudocode
```plaintext
DIRECT-ADDRESS-SEARCH(T, k)
  return T[k]

DIRECT-ADDRESS-INSERT(T, x)
  T[x.key] = x

DIRECT-ADDRESS-DELETE(T, x)
  T[x.key] = NIL
```

#### Time Complexity
- **INSERT**: **O(1)**
- **SEARCH**: **O(1)**
- **DELETE**: **O(1)**

#### Example
Given a key universe `U = {0,1,...,9}` and the set `K = {2,3,5,8}`:
- `T[2]`, `T[3]`, `T[5]`, and `T[8]` point to elements, while other slots are `NIL`.

---

### Hashing with Chaining

#### How It Works
To handle collisions, each slot in the hash table contains a linked list of all elements that hash to the same value using hash function `h(k)`. Each operation performs on the linked list at the hashed index.

#### Pseudocode
```plaintext
CHAINED-HASH-INSERT(T, x)
  insert x at the head of list T[h(x.key)]

CHAINED-HASH-SEARCH(T, k)
  search for key k in list T[h(k)]

CHAINED-HASH-DELETE(T, x)
  delete x from list T[h(x.key)]
```

#### Time Complexity
- **INSERT**: **O(1)** average, **O(1)** worst-case (prepend element to the list).
- **SEARCH**: **O(1)** average (short lists due to uniform distribution), **O(n)** worst-case.
- **DELETE**: **O(1)** average if using doubly linked lists.

#### Example with Collisions
Let `h(k) = k mod 3` on keys `K = {0,3,6,4,7,2}`. `T` contains:
- `T[0]` -> `6 -> 3 -> 0`
- `T[1]` -> `7 -> 4`
- `T[2]` -> `2`

---

### Hashing with Open Addressing

#### How It Works
Collisions are resolved by searching other slots within the hash table based on a probing sequence. Common strategies include:
- **Linear Probing**: Sequentially check slots starting from `h(k)` until an empty one is found.
- **Quadratic Probing**: Check slots as per a quadratic formula.
- **Double Hashing**: Use two hash functions to determine the probing sequence.

#### Pseudocode
```plaintext
OPEN-ADDRESS-SEARCH(T, k)
  i = 0
  repeat
    j = (h(k) + i) mod m
    if T[j] == k
      return j
    i = i + 1
  until T[j] == NIL
  return NIL
```

#### Time Complexity
- **INSERT**/**SEARCH**/**DELETE**: Constant **O(1)** on average when the load factor `α` is small; **O(n)** in the worst case when the table is full.

---

### Perfect Hashing

#### How It Works
For static key sets, perfect hashing ensures no collisions using a two-level hash table structure:
1. First level hashes keys into buckets.
2. Second level uses a hash function tailored for each bucket.

#### Time Complexity
- **INSERT**, **SEARCH**: Worst-case **O(1)**.
  
---

## Complexity Analysis Table
| Method                | Average-Case Complexity | Worst-Case Complexity | Space Complexity  |
|-----------------------|--------------------------|------------------------|-------------------|
| Direct Addressing     | O(1)                    | O(1)                  | **Θ(m)**          |
| Hashing (Chaining)    | O(1)                    | O(n)                  | **Θ(n + m)**      |
| Hashing (Open Addressing) | O(1)              | O(n)                  | **Θ(m)**          |
| Perfect Hashing       | O(1)                    | O(1)                  | **Θ(n)** for static keys |

---

## Key Data Structures and Operations

### Direct Address Table
- **Key Operations**: 
  - INSERT: Place the key at its corresponding slot.
  - SEARCH: Direct access using the key.
  - DELETE: Set slot to `NIL`.
- **Time Complexity**: O(1) for all operations.

### Hash Table with Chaining
- **Key Operations**: 
  - INSERT: Prepend to the linked list at the hashed index.
  - SEARCH: Scan the linked list at the hash index.
  - DELETE: Remove from the linked list.
- **Time Complexity**: O(1) average, O(n) worst-case.

---

## Concluding Notes
Hash tables are a core data structure in computing due to their efficiency and widespread applications. While collisions and space constraints impose challenges, techniques like chaining, open addressing, and perfect hashing resolve them effectively. Understanding design trade-offs and hash function characteristics is crucial for optimizing performance.

```
