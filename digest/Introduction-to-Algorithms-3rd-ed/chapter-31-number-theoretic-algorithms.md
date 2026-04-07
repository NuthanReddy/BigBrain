# Chapter 31: Number-Theoretic Algorithms

## Overview
This chapter covers algorithms rooted in number theory that have become critically important due to their role in modern cryptography. Topics range from foundational concepts like divisibility and modular arithmetic through Euclid's algorithm for GCD computation, the Chinese Remainder Theorem, the RSA public-key cryptosystem, randomized primality testing (Miller-Rabin), and integer factorization (Pollard's rho heuristic). The chapter emphasizes that while finding large primes is efficient, factoring the product of two large primes remains computationally hard—the asymmetry that underpins RSA security.

## Key Concepts

- **Divisibility**: d | a means a = kd for some integer k. Every positive integer a has trivial divisors 1 and a.
- **Primes and composites**: a prime p > 1 has no divisors other than 1 and p. A composite has additional divisors.
- **Fundamental Theorem of Arithmetic (Theorem 31.8)**: every positive integer has a unique prime factorization.
- **Greatest common divisor**: gcd(a, b) is the largest integer dividing both a and b. If gcd(a, b) = 1, then a and b are **relatively prime** (coprime).
- **Modular arithmetic**: a ≡ b (mod n) means n | (a − b). The integers modulo n form the group Zₙ = {0, 1, …, n−1} under addition, and Z*ₙ (integers coprime to n) forms a group under multiplication mod n.
- **Euler's totient function** φ(n): the number of integers in {1, …, n} coprime to n. For prime p, φ(p) = p − 1.
- **Euler's theorem (Theorem 31.31)**: a^φ(n) ≡ 1 (mod n) for a ∈ Z*ₙ.
- **Fermat's little theorem (Theorem 31.32)**: if p is prime, then aᵖ⁻¹ ≡ 1 (mod p) for a not divisible by p.
- **Chinese Remainder Theorem (Theorem 31.27)**: if n₁, n₂, …, nₖ are pairwise coprime, then the system x ≡ aᵢ (mod nᵢ) has a unique solution mod n = n₁n₂⋯nₖ. Provides an isomorphism Zₙ ≅ Zₙ₁ × Zₙ₂ × ⋯ × Zₙₖ.
- **Quadratic residues**: a is a quadratic residue mod n if x² ≡ a (mod n) has a solution.
- **Primitive roots / generators**: g is a primitive root mod n if it generates Z*ₙ (i.e., every element of Z*ₙ is a power of g).
- **Discrete logarithm**: given g, a, and n, finding x such that gˣ ≡ a (mod n) is believed to be computationally hard.

## Algorithms and Techniques

### EUCLID(a, b) — GCD Computation
- Classic recursive algorithm: gcd(a, b) = gcd(b, a mod b), with base case gcd(a, 0) = a.
- **Theorem 31.9 (Lamé's theorem)**: the number of recursive calls is at most ⌊log_φ(min(a,b))⌋ + 1, making it O(lg(min(a,b))) arithmetic operations, or O(β³) bit operations for β-bit inputs.

### EXTENDED-EUCLID(a, b)
- Returns (d, x, y) such that d = gcd(a, b) = ax + by (Bézout's identity).
- Essential for computing modular inverses: if gcd(a, n) = 1, then a⁻¹ mod n = x from extended GCD of (a, n).

### MODULAR-LINEAR-EQUATION-SOLVER(a, b, n)
- Solves ax ≡ b (mod n).
- Uses EXTENDED-EUCLID to find gcd(a, n). If gcd(a, n) | b, there are exactly gcd(a, n) solutions mod n; otherwise no solution exists.

### MODULAR-EXPONENTIATION(a, b, n) — Repeated Squaring
- Computes aᵇ mod n efficiently by scanning bits of b from left to right.
- At each step: square the accumulator, and if the current bit of b is 1, multiply by a.
- Running time: O(β) modular multiplications, or O(β³) bit operations for β-bit numbers.
- Critical subroutine for RSA encryption/decryption and primality testing.

### RSA Public-Key Cryptosystem
- **Key generation**: choose two large primes p, q; compute n = pq and φ(n) = (p−1)(q−1). Choose e coprime to φ(n); compute d = e⁻¹ mod φ(n). Public key = (e, n), secret key = (d, n).
- **Encryption**: C = Mᵉ mod n.
- **Decryption**: M = Cᵈ mod n.
- **Correctness**: Mᵉᵈ ≡ M (mod n), which follows from Euler's theorem and the Chinese Remainder Theorem.
- **Security**: relies on the computational difficulty of factoring n = pq.

### MILLER-RABIN(n, s) — Randomized Primality Testing
- Tests whether n is prime by checking s randomly chosen **witnesses**.
- For odd n > 2, write n − 1 = 2ᵗu where u is odd.
- For a random base a ∈ {2, …, n−2}, the **WITNESS** procedure:
  1. Computes a^u mod n, then repeatedly squares t times.
  2. If the sequence does not start at 1 or ±1 and does not pass through −1 before reaching 1, then a is a **witness** to n's compositeness.
- **Theorem 31.38**: if n is an odd composite, at least 3/4 of all values in {1, …, n−1} are witnesses.
- **Theorem 31.39**: the error probability after s rounds is at most 4⁻ˢ—making the test highly reliable with modest s (e.g., s = 50).

### POLLARD-RHO(n) — Integer Factorization Heuristic
- Uses Floyd's cycle-detection ("tortoise and hare") on the pseudorandom sequence xᵢ₊₁ = (xᵢ² − 1) mod n.
- Computes gcd(|xᵢ − x₂ᵢ|, n) at each step; a nontrivial GCD reveals a factor.
- **Expected running time**: O(n^(1/4)) arithmetic operations (heuristic analysis via the birthday paradox—expects a collision after about √p iterations where p is the smallest prime factor).

## Complexity Analysis

| Algorithm | Arithmetic Operations | Bit Operations |
|---|---|---|
| EUCLID(a, b) | O(lg b) | O(β³) |
| EXTENDED-EUCLID(a, b) | O(lg b) | O(β³) |
| MODULAR-EXPONENTIATION | O(β) multiplications | O(β³) |
| MILLER-RABIN (s rounds) | O(sβ) multiplications | O(sβ³) |
| POLLARD-RHO | O(n^(1/4)) expected | O(n^(1/4) β²) expected |

(β = number of bits in the input numbers)

## Key Takeaways

- **Euclid's algorithm** is one of the oldest known algorithms and remains highly efficient: O(lg n) recursive divisions to compute gcd, with the extended version providing Bézout coefficients essential for modular inverses.
- **Modular exponentiation by repeated squaring** is the computational engine behind RSA and primality testing, computing aᵇ mod n in O(lg b) multiplications.
- **RSA security rests on the factoring gap**: generating large primes is easy (Miller-Rabin), but factoring their product is believed to be computationally infeasible—no known polynomial-time algorithm exists for general integer factorization.
- **Miller-Rabin primality testing** is both practical and theoretically sound: with s = 50 independent trials, the error probability is at most 4⁻⁵⁰ ≈ 10⁻³⁰, making it effectively deterministic for all practical purposes.
- **The Chinese Remainder Theorem** provides a powerful decomposition tool: computations modulo a composite n can be split into independent computations modulo its prime-power factors, then reassembled.
