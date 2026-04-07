# Chapter 30: Polynomials and the FFT

## Overview
This chapter shows how the **Fast Fourier Transform (FFT)** enables polynomial multiplication in Θ(n lg n) time, dramatically improving on the straightforward Θ(n²) approach. The key insight is that polynomials can be represented in two forms—coefficient and point-value—and the FFT provides an efficient way to convert between them using complex roots of unity. The FFT is one of the most important algorithms in computer science, with applications spanning signal processing, audio/video compression (MP3, etc.), and scientific computing.

## Key Concepts

- **Polynomial representations**:
  - **Coefficient representation**: a vector of coefficients a = (a₀, a₁, …, aₙ₋₁) for A(x) = Σaⱼxʲ.
  - **Point-value representation**: a set of n point-value pairs {(x₀, y₀), (x₁, y₁), …, (xₙ₋₁, yₙ₋₁)} where yₖ = A(xₖ).
  - By the **uniqueness of interpolation** (Theorem 30.1), a polynomial of degree-bound n is uniquely determined by its values at n distinct points.

- **Operations in each representation**:
  - Addition: Θ(n) in both representations.
  - Evaluation at a single point (Horner's rule): Θ(n) in coefficient form.
  - Multiplication: Θ(n²) in coefficient form, but only Θ(n) in point-value form (pointwise multiply).
  - The bottleneck is **converting between representations** efficiently.

- **Strategy for fast polynomial multiplication** (degree-bound n):
  1. **Evaluate** both polynomials at 2n points → point-value form. (This is the "DFT" step.)
  2. **Pointwise multiply** the 2n point-values in Θ(n) time.
  3. **Interpolate** the product back to coefficient form. (This is the "inverse DFT" step.)
  - Using FFT for steps 1 and 3, total time is Θ(n lg n).

- **Complex roots of unity**: the n complex nth roots of unity are ωₙᵏ = e^(2πik/n) for k = 0, 1, …, n-1, where ωₙ = e^(2πi/n) is the **principal nth root of unity**.
  - **Cancellation lemma (Lemma 30.5)**: ωₙᵏ = ωₙ/₂^(k/2) when n is even—halving and squaring properties enable the divide-and-conquer strategy.
  - **Halving lemma (Corollary 30.4)**: squaring the n nth roots of unity yields the n/2 (n/2)th roots of unity, each obtained exactly twice.
  - **Summation lemma (Lemma 30.6)**: Σₖ₌₀ⁿ⁻¹ (ωₙ)ᵏʲ = 0 for any j not divisible by n (cancellation property).

- **Discrete Fourier Transform (DFT)**: evaluating a polynomial at all nth roots of unity: yₖ = A(ωₙᵏ) = Σⱼ aⱼ ωₙᵏʲ. Written as y = DFTₙ(a), or equivalently y = Vₙa where Vₙ is the Vandermonde matrix of roots of unity.

- **Inverse DFT**: recovers coefficients from point values. aⱼ = (1/n) Σₖ yₖ ωₙ⁻ᵏʲ. Computed by running FFT with ωₙ⁻¹ replacing ωₙ and dividing by n.

## Algorithms and Techniques

### RECURSIVE-FFT(a)
- Computes DFTₙ(a) using divide-and-conquer on even/odd-indexed coefficients.
- **Divide**: split a into even-indexed coefficients a⁰ = (a₀, a₂, …) and odd-indexed a¹ = (a₁, a₃, …).
- **Conquer**: recursively compute DFTₙ/₂(a⁰) and DFTₙ/₂(a¹).
- **Combine**: for k = 0, …, n/2 - 1:
  - yₖ = yₖ⁰ + ωₙᵏ · yₖ¹
  - yₖ₊ₙ/₂ = yₖ⁰ − ωₙᵏ · yₖ¹
- The factors ωₙᵏ used in the combine step are called **twiddle factors**.
- The combine step exploits the **butterfly operation**: each pair of outputs uses both addition and subtraction of the same product, halving the number of multiplications.

### ITERATIVE-FFT(a)
- Bottom-up iterative version that avoids recursion overhead.
- Uses **BIT-REVERSE-COPY** to reorder input elements so that the iterative combination proceeds naturally.
- **Bit-reversal permutation**: element at position k is moved to position rev(k), where rev(k) reverses the binary representation of k.
- Processes lg n stages, each combining pairs of sub-results from the previous stage.
- Better cache behavior and lower constant factors than RECURSIVE-FFT.

### Inverse FFT
- Identical to FFT except: replace ωₙ with ωₙ⁻¹, and divide each output by n.
- Justified by **Theorem 30.7**: V⁻¹ₙ has (j,k) entry ωₙ⁻ᵏʲ/n.

### Polynomial Multiplication via FFT
1. Pad both input polynomials (degree-bound n each) with zeros to length 2n.
2. Apply FFT to both → two point-value vectors of length 2n.
3. Pointwise multiply the two vectors → product in point-value form.
4. Apply inverse FFT → coefficient vector of the product polynomial.

## Complexity Analysis

| Operation | Time Complexity |
|---|---|
| Polynomial evaluation (Horner's) | Θ(n) |
| Naive polynomial multiplication | Θ(n²) |
| RECURSIVE-FFT | Θ(n lg n) |
| ITERATIVE-FFT | Θ(n lg n) |
| Inverse FFT | Θ(n lg n) |
| Polynomial multiplication via FFT | Θ(n lg n) |

**Theorem 30.2**: Polynomial multiplication can be performed in Θ(n lg n) time using the coefficient representation, by converting to/from point-value form at the complex roots of unity.

**Theorem 30.8 (Convolution Theorem)**: For vectors a and b of length n: a ⊗ b = DFT⁻¹₂ₙ(DFT₂ₙ(a) · DFT₂ₙ(b)), where ⊗ denotes convolution and · denotes pointwise multiplication.

## Key Takeaways

- **The FFT reduces polynomial multiplication from Θ(n²) to Θ(n lg n)** by cleverly exploiting the algebraic structure of complex roots of unity—specifically, the halving lemma that enables divide-and-conquer.
- **Two equivalent representations** of polynomials (coefficient and point-value) have complementary strengths: the FFT bridges them in Θ(n lg n) time, enabling fast multiplication.
- **The inverse DFT is essentially another FFT** with conjugate roots and a scaling factor, so both directions cost Θ(n lg n).
- **The iterative FFT** with bit-reversal permutation is the form used in practice (e.g., in libraries like FFTW), avoiding recursion overhead and enabling efficient memory access patterns.
- **Convolution in the time/spatial domain equals pointwise multiplication in the frequency domain**—this fundamental principle (the Convolution Theorem) underlies applications in signal processing, image filtering, and far beyond polynomial multiplication.
