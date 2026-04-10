# 30 Polynomials and the FFT

The straightforward method of adding two polynomials of degree n takes ‚.n/ time, but the straightforward method of multiplying them takes ‚.n2/ time. In this chapter, we shall show how the fast Fourier transform, or FFT, can reduce the time to multiply polynomials to ‚.n lg n/. The most common use for Fourier transforms, and hence the FFT, is in signal processing. A signal is given in the time domain: as a function mapping time to amplitude. Fourier analysis allows us to express the signal as a weighted sum of phase-shifted sinusoids of varying frequencies. The weights and phases associated with the frequencies characterize the signal in the frequency domain. Among the many everyday applications of FFT’s are compression techniques used to encode digital video and audio information, including MP3 ﬁles. Several ﬁne books delve into the rich area of signal processing; the chapter notes reference a few of them.

Polynomials A polynomial in the variable x over an algebraic ﬁeld F represents a function A.x/ as a formal sum:

A.x/ D n1 X jD0 ajxj : We call the values a0; a1; : : : ; an1 the coefﬁcients of the polynomial. The coefﬁcients are drawn from a ﬁeld F , typically the set C of complex numbers. A polynomial A.x/ has degree k if its highest nonzero coefﬁcient is ak; we write that degree.A/ D k. Any integer strictly greater than the degree of a polynomial is a degree-bound of that polynomial. Therefore, the degree of a polynomial of degree-bound n may be any integer between 0 and n  1, inclusive. We can deﬁne a variety of operations on polynomials. For polynomial addition, if A.x/ and B.x/ are polynomials of degree-bound n, their sum is a polyno-

mial C.x/, also of degree-bound n, such that C.x/ D A.x/ C B.x/ for all x in the underlying ﬁeld. That is, if A.x/ D n1 X jD0 ajxj and B.x/ D n1 X jD0 bjxj ; then C.x/ D n1 X jD0 cjxj ; where cj D aj C bj for j D 0; 1; : : : ; n  1.

For example, if we have the polynomials A.x/ D 6x3 C 7x2  10x C 9 and B.x/ D 2x3 C 4x  5, then C.x/ D 4x3 C 7x2  6x C 4.

For polynomial multiplication, if A.x/ and B.x/ are polynomials of degreebound n, their product C.x/ is a polynomial of degree-bound 2n  1 such that C.x/ D A.x/B.x/ for all x in the underlying ﬁeld. You probably have multiplied polynomials before, by multiplying each term in A.x/ by each term in B.x/ and then combining terms with equal powers.

For example, we can multiply A.x/ D 6x3 C 7x2  10x C 9 and B.x/ D 2x3 C 4x  5 as follows: 6x3 C 7x2  10x C  2x3 C 4x   30x3  35x2 C 50x  45 24x4 C 28x3  40x2 C 36x  12x6  14x5 C 20x4  18x3  12x6  14x5 C 44x4  20x3  75x2 C 86x  45 Another way to express the product C.x/ is C.x/ D 2n2 X jD0 cjxj ; (30.1) where cj D j X kD0 akbjk : (30.2)

Note that degree.C/ D degree.A/ C degree.B/, implying that if A is a polynomial of degree-bound na and B is a polynomial of degree-bound nb, then C is a polynomial of degree-bound na C nb  1. Since a polynomial of degree-bound k is also a polynomial of degree-bound k C 1, we will normally say that the product polynomial C is a polynomial of degree-bound na C nb.

Chapter outline Section 30.1 presents two ways to represent polynomials: the coefﬁcient representation and the point-value representation. The straightforward methods for multiplying polynomials—equations (30.1) and (30.2)—take ‚.n2/ time when we represent polynomials in coefﬁcient form, but only ‚.n/ time when we represent them in point-value form. We can, however, multiply polynomials using the coefﬁcient representation in only ‚.n lg n/ time by converting between the two representations. To see why this approach works, we must ﬁrst study complex roots of unity, which we do in Section 30.2. Then, we use the FFT and its inverse, also described in Section 30.2, to perform the conversions. Section 30.3 shows how to implement the FFT quickly in both serial and parallel models. This chapter uses complex numbers extensively, and within this chapter we use the symbol i exclusively to denote p 1.

## 30.1 Representing polynomials

The coefﬁcient and point-value representations of polynomials are in a sense equivalent; that is, a polynomial in point-value form has a unique counterpart in coefﬁcient form. In this section, we introduce the two representations and show how to combine them so that we can multiply two degree-bound n polynomials in ‚.n lg n/ time.

Coefﬁcient representation A coefﬁcient representation of a polynomial A.x/ D Pn1 jD0 ajxj of degreebound n is a vector of coefﬁcients a D .a0; a1; : : : ; an1/. In matrix equations in this chapter, we shall generally treat vectors as column vectors. The coefﬁcient representation is convenient for certain operations on polynomials. For example, the operation of evaluating the polynomial A.x/ at a given point x0 consists of computing the value of A.x0/. We can evaluate a polynomial in ‚.n/ time using Horner’s rule:

A.x0/ D a0 C x0.a1 C x0.a2 C    C x0.an2 C x0.an1//   // :

## 30.1 Representing polynomials

Similarly, adding two polynomials represented by the coefﬁcient vectors a D .a0; a1; : : : ; an1/ and b D .b0; b1; : : : ; bn1/ takes ‚.n/ time: we just produce the coefﬁcient vector c D .c0; c1; : : : ; cn1/, where cj D aj C bj for j D 0; 1; : : : ; n  1. Now, consider multiplying two degree-bound n polynomials A.x/ and B.x/ represented in coefﬁcient form. If we use the method described by equations (30.1) and (30.2), multiplying polynomials takes time ‚.n2/, since we must multiply each coefﬁcient in the vector a by each coefﬁcient in the vector b. The operation of multiplying polynomials in coefﬁcient form seems to be considerably more difﬁ- cult than that of evaluating a polynomial or adding two polynomials. The resulting coefﬁcient vector c, given by equation (30.2), is also called the convolution of the input vectors a and b, denoted c D a ˝ b. Since multiplying polynomials and computing convolutions are fundamental computational problems of considerable practical importance, this chapter concentrates on efﬁcient algorithms for them.

Point-value representation A point-value representation of a polynomial A.x/ of degree-bound n is a set of n point-value pairs f.x0; y0/; .x1; y1/; : : : ; .xn1; yn1/g such that all of the xk are distinct and yk D A.xk/ (30.3) for k D 0; 1; : : : ; n  1. A polynomial has many different point-value representations, since we can use any set of n distinct points x0; x1; : : : ; xn1 as a basis for the representation.

Computing a point-value representation for a polynomial given in coefﬁcient form is in principle straightforward, since all we have to do is select n distinct points x0; x1; : : : ; xn1 and then evaluate A.xk/ for k D 0; 1; : : : ; n  1. With Horner’s method, evaluating a polynomial at n points takes time ‚.n2/. We shall see later that if we choose the points xk cleverly, we can accelerate this computation to run in time ‚.n lg n/. The inverse of evaluation—determining the coefﬁcient form of a polynomial from a point-value representation—is interpolation. The following theorem shows that interpolation is well deﬁned when the desired interpolating polynomial must have a degree-bound equal to the given number of point-value pairs.

> **Theorem 30.1 (Uniqueness of an interpolating polynomial)**

For any set f.x0; y0/; .x1; y1/; : : : ; .xn1; yn1/g of n point-value pairs such that all the xk values are distinct, there is a unique polynomial A.x/ of degree-bound n such that yk D A.xk/ for k D 0; 1; : : : ; n  1.

Proof The proof relies on the existence of the inverse of a certain matrix. Equation (30.3) is equivalent to the matrix equation ˙ 1 x0 x2 xn1 x1 x2 xn1 ::: ::: ::: ::: ::: xn1 x2 n1 xn1 n1 ˙ a0 a1 ::: an1  D ˙ y0 y1 ::: yn1  : (30.4) The matrix on the left is denoted V.x0; x1; : : : ; xn1/ and is known as a Vandermonde matrix. By Problem D-1, this matrix has determinant Y 0j<kn1 .xk  xj/ ; and therefore, by Theorem D.5, it is invertible (that is, nonsingular) if the xk are distinct. Thus, we can solve for the coefﬁcients aj uniquely given the point-value representation: a D V.x0; x1; : : : ; xn1/1y : The proof of Theorem 30.1 describes an algorithm for interpolation based on solving the set (30.4) of linear equations. Using the LU decomposition algorithms of Chapter 28, we can solve these equations in time O.n3/.

A faster algorithm for n-point interpolation is based on Lagrange’s formula:

A.x/ D n1 X kD0 yk Y j¤k .x  xj/ Y j¤k .xk  xj/ : (30.5) You may wish to verify that the right-hand side of equation (30.5) is a polynomial of degree-bound n that satisﬁes A.xk/ D yk for all k. Exercise 30.1-5 asks you how to compute the coefﬁcients of A using Lagrange’s formula in time ‚.n2/. Thus, n-point evaluation and interpolation are well-deﬁned inverse operations that transform between the coefﬁcient representation of a polynomial and a pointvalue representation.1 The algorithms described above for these problems take time ‚.n2/. The point-value representation is quite convenient for many operations on polynomials. For addition, if C.x/ D A.x/ C B.x/, then C.xk/ D A.xk/ C B.xk/ for any point xk. More precisely, if we have a point-value representation for A, 1Interpolation is a notoriously tricky problem from the point of view of numerical stability. Although the approaches described here are mathematically correct, small differences in the inputs or round-off errors during computation can cause large differences in the result.

## 30.1 Representing polynomials

f.x0; y0/; .x1; y1/; : : : ; .xn1; yn1/g ; and for B, f.x0; y0 0/; .x1; y0 1/; : : : ; .xn1; y0 n1/g (note that A and B are evaluated at the same n points), then a point-value representation for C is f.x0; y0 C y0 0/; .x1; y1 C y0 1/; : : : ; .xn1; yn1 C y0 n1/g : Thus, the time to add two polynomials of degree-bound n in point-value form is ‚.n/.

Similarly, the point-value representation is convenient for multiplying polynomials. If C.x/ D A.x/B.x/, then C.xk/ D A.xk/B.xk/ for any point xk, and we can pointwise multiply a point-value representation for A by a point-value representation for B to obtain a point-value representation for C. We must face the problem, however, that degree.C/ D degree.A/ C degree.B/; if A and B are of degree-bound n, then C is of degree-bound 2n. A standard point-value representation for A and B consists of n point-value pairs for each polynomial. When we multiply these together, we get n point-value pairs, but we need 2n pairs to interpolate a unique polynomial C of degree-bound 2n. (See Exercise 30.1-4.) We must therefore begin with “extended” point-value representations for A and for B consisting of 2n point-value pairs each. Given an extended point-value representation for A, f.x0; y0/; .x1; y1/; : : : ; .x2n1; y2n1/g ; and a corresponding extended point-value representation for B, f.x0; y0 0/; .x1; y0 1/; : : : ; .x2n1; y0 2n1/g ; then a point-value representation for C is f.x0; y0y0 0/; .x1; y1y0 1/; : : : ; .x2n1; y2n1y0 2n1/g :

Given two input polynomials in extended point-value form, we see that the time to multiply them to obtain the point-value form of the result is ‚.n/, much less than the time required to multiply polynomials in coefﬁcient form.

Finally, we consider how to evaluate a polynomial given in point-value form at a new point. For this problem, we know of no simpler approach than converting the polynomial to coefﬁcient form ﬁrst, and then evaluating it at the new point.

Fast multiplication of polynomials in coefﬁcient form Can we use the linear-time multiplication method for polynomials in point-value form to expedite polynomial multiplication in coefﬁcient form? The answer hinges

a0; a1; : : : ; an1 b0; b1; : : : ; bn1 c0; c1; : : : ; c2n2 Ordinary multiplication Time ‚.n2/ Evaluation Time ‚.n lg n/ Time ‚.n lg n/ Interpolation Pointwise multiplication Time ‚.n/ A.!0 2n/; B.!0 2n/ A.!1 2n/; B.!1 2n/ A.!2n1 2n /; B.!2n1 2n / ::: :::

C.!0 2n/ C.!1 2n/ C.!2n1 2n / Coefﬁcient Point-value representations representations Figure 30.1 A graphical outline of an efﬁcient polynomial-multiplication process. Representations on the top are in coefﬁcient form, while those on the bottom are in point-value form. The arrows from left to right correspond to the multiplication operation. The !2n terms are complex .2n/th roots of unity. on whether we can convert a polynomial quickly from coefﬁcient form to pointvalue form (evaluate) and vice versa (interpolate). We can use any points we want as evaluation points, but by choosing the evaluation points carefully, we can convert between representations in only ‚.n lg n/ time. As we shall see in Section 30.2, if we choose “complex roots of unity” as the evaluation points, we can produce a point-value representation by taking the discrete Fourier transform (or DFT) of a coefﬁcient vector. We can perform the inverse operation, interpolation, by taking the “inverse DFT” of point-value pairs, yielding a coefﬁcient vector. Section 30.2 will show how the FFT accomplishes the DFT and inverse DFT operations in ‚.n lg n/ time.

Figure 30.1 shows this strategy graphically. One minor detail concerns degreebounds. The product of two polynomials of degree-bound n is a polynomial of degree-bound 2n. Before evaluating the input polynomials A and B, therefore, we ﬁrst double their degree-bounds to 2n by adding n high-order coefﬁcients of 0.

Because the vectors have 2n elements, we use “complex .2n/th roots of unity,” which are denoted by the !2n terms in Figure 30.1.

Given the FFT, we have the following ‚.n lg n/-time procedure for multiplying two polynomials A.x/ and B.x/ of degree-bound n, where the input and output representations are in coefﬁcient form. We assume that n is a power of 2; we can always meet this requirement by adding high-order zero coefﬁcients. 1. Double degree-bound: Create coefﬁcient representations of A.x/ and B.x/ as degree-bound 2n polynomials by adding n high-order zero coefﬁcients to each.

## 30.1 Representing polynomials

2. Evaluate: Compute point-value representations of A.x/ and B.x/ of length 2n by applying the FFT of order 2n on each polynomial. These representations contain the values of the two polynomials at the .2n/th roots of unity. 3. Pointwise multiply: Compute a point-value representation for the polynomial C.x/ D A.x/B.x/ by multiplying these values together pointwise. This representation contains the value of C.x/ at each .2n/th root of unity. 4. Interpolate: Create the coefﬁcient representation of the polynomial C.x/ by applying the FFT on 2n point-value pairs to compute the inverse DFT.

Steps (1) and (3) take time ‚.n/, and steps (2) and (4) take time ‚.n lg n/. Thus, once we show how to use the FFT, we will have proven the following.

> **Theorem 30.2**

We can multiply two polynomials of degree-bound n in time ‚.n lg n/, with both the input and output representations in coefﬁcient form.

## Exercises

30.1-1 Multiply the polynomials A.x/ D 7x3  x2 C x  10 and B.x/ D 8x3  6x C 3 using equations (30.1) and (30.2). 30.1-2 Another way to evaluate a polynomial A.x/ of degree-bound n at a given point x0 is to divide A.x/ by the polynomial .x x0/, obtaining a quotient polynomial q.x/ of degree-bound n  1 and a remainder r, such that A.x/ D q.x/.x  x0/ C r :

Clearly, A.x0/ D r. Show how to compute the remainder r and the coefﬁcients of q.x/ in time ‚.n/ from x0 and the coefﬁcients of A. 30.1-3 Derive a point-value representation for Arev.x/ D Pn1 jD0 an1jxj from a pointvalue representation for A.x/ D Pn1 jD0 ajxj, assuming that none of the points is 0. 30.1-4 Prove that n distinct point-value pairs are necessary to uniquely specify a polynomial of degree-bound n, that is, if fewer than n distinct point-value pairs are given, they fail to specify a unique polynomial of degree-bound n. (Hint: Using Theorem 30.1, what can you say about a set of n  1 point-value pairs to which you add one more arbitrarily chosen point-value pair?)

30.1-5 Show how to use equation (30.5) to interpolate in time ‚.n2/. (Hint: First compute the coefﬁcient representation of the polynomial Q j.x  xj/ and then divide by .x xk/ as necessary for the numerator of each term; see Exercise 30.1-2. You can compute each of the n denominators in time O.n/.) 30.1-6 Explain what is wrong with the “obvious” approach to polynomial division using a point-value representation, i.e., dividing the corresponding y values. Discuss separately the case in which the division comes out exactly and the case in which it doesn’t. 30.1-7 Consider two sets A and B, each having n integers in the range from 0 to 10n. We wish to compute the Cartesian sum of A and B, deﬁned by C D fx C y W x 2 A and y 2 Bg : Note that the integers in C are in the range from 0 to 20n. We want to ﬁnd the elements of C and the number of times each element of C is realized as a sum of elements in A and B. Show how to solve the problem in O.n lg n/ time. (Hint:

Represent A and B as polynomials of degree at most 10n.)

## 30.2 The DFT and FFT

In Section 30.1, we claimed that if we use complex roots of unity, we can evaluate and interpolate polynomials in ‚.n lg n/ time. In this section, we deﬁne complex roots of unity and study their properties, deﬁne the DFT, and then show how the FFT computes the DFT and its inverse in ‚.n lg n/ time.

Complex roots of unity A complex nth root of unity is a complex number ! such that !n D 1 : There are exactly n complex nth roots of unity: e2ik=n for k D 0; 1; : : : ; n  1. To interpret this formula, we use the deﬁnition of the exponential of a complex number: eiu D cos.u/ C i sin.u/ :

Figure 30.2 shows that the n complex roots of unity are equally spaced around the circle of unit radius centered at the origin of the complex plane. The value

## 30.2 The DFT and FFT

1 i i !0 8 D !8 !1 !2 !3 !4 !5 !6 !7 Figure 30.2 The values of !0 8; !1 8; : : : ; !7 8 in the complex plane, where !8 D e2i=8 is the principal 8th root of unity. !n D e2i=n (30.6) is the principal nth root of unity;2 all other complex nth roots of unity are powers of !n. The n complex nth roots of unity, !0 n; !1 n; : : : ; !n1 n ; form a group under multiplication (see Section 31.3). This group has the same structure as the additive group .Zn; C/ modulo n, since !n n D !0 n D 1 implies that !j n!k n D !jCk n D !.jCk/ mod n n . Similarly, !1 n D !n1 n . The following lemmas furnish some essential properties of the complex nth roots of unity.

> **Lemma 30.3 (Cancellation lemma)**

For any integers n  0, k  0, and d > 0, !dk dn D !k n : (30.7) Proof The lemma follows directly from equation (30.6), since !dk dn D

e2i=dn dk D

e2i=n k D !k n : 2Many other authors deﬁne !n differently: !n D e2i=n. This alternative deﬁnition tends to be used for signal-processing applications. The underlying mathematics is substantially the same with either deﬁnition of !n.

> **Corollary 30.4**

For any even integer n > 0, !n=2 n D !2 D 1 :

Proof The proof is left as Exercise 30.2-1.

> **Lemma 30.5 (Halving lemma)**

If n > 0 is even, then the squares of the n complex nth roots of unity are the n=2 complex .n=2/th roots of unity.

Proof By the cancellation lemma, we have .!k n/2 D !k n=2, for any nonnegative integer k. Note that if we square all of the complex nth roots of unity, then we obtain each .n=2/th root of unity exactly twice, since .!kCn=2 n /2 D !2kCn n D !2k n !n n D !2k n D .!k n/2 : Thus, !k n and !kCn=2 n have the same square. We could also have used Corollary 30.4 to prove this property, since !n=2 n D 1 implies !kCn=2 n D !k n, and thus .!kCn=2 n /2 D .!k n/2. As we shall see, the halving lemma is essential to our divide-and-conquer approach for converting between coefﬁcient and point-value representations of polynomials, since it guarantees that the recursive subproblems are only half as large.

> **Lemma 30.6 (Summation lemma)**

For any integer n  1 and nonzero integer k not divisible by n, n1 X jD0

!k n

j D 0 :

Proof Equation (A.5) applies to complex values as well as to reals, and so we have

## 30.2 The DFT and FFT

n1 X jD0

!k n

j D .!k n/n  1 !k n  1 D .!n n/k  1 !k n  1 D .1/k  1 !k n  1 D 0 :

Because we require that k is not divisible by n, and because !k n D 1 only when k is divisible by n, we ensure that the denominator is not 0. The DFT Recall that we wish to evaluate a polynomial A.x/ D n1 X jD0 ajxj of degree-bound n at !0 n; !1 n; !2 n; : : : ; !n1 n (that is, at the n complex nth roots of unity).3 We assume that A is given in coefﬁcient form: a D .a0; a1; : : : ; an1/. Let us deﬁne the results yk, for k D 0; 1; : : : ; n  1, by yk D A.!k n/ D n1 X jD0 aj!kj n : (30.8) The vector y D .y0; y1; : : : ; yn1/ is the discrete Fourier transform (DFT) of the coefﬁcient vector a D .a0; a1; : : : ; an1/. We also write y D DFTn.a/. The FFT By using a method known as the fast Fourier transform (FFT), which takes advantage of the special properties of the complex roots of unity, we can compute DFTn.a/ in time ‚.n lg n/, as opposed to the ‚.n2/ time of the straightforward method. We assume throughout that n is an exact power of 2. Although strategies 3The length n is actually what we referred to as 2n in Section 30.1, since we double the degree-bound of the given polynomials prior to evaluation. In the context of polynomial multiplication, therefore, we are actually working with complex .2n/th roots of unity.

for dealing with non-power-of-2 sizes are known, they are beyond the scope of this book. The FFT method employs a divide-and-conquer strategy, using the even-indexed and odd-indexed coefﬁcients of A.x/ separately to deﬁne the two new polynomials AŒ0.x/ and AŒ1.x/ of degree-bound n=2:

AŒ0.x/ D a0 C a2x C a4x2 C    C an2xn=21 ; AŒ1.x/ D a1 C a3x C a5x2 C    C an1xn=21 : Note that AŒ0 contains all the even-indexed coefﬁcients of A (the binary representation of the index ends in 0) and AŒ1 contains all the odd-indexed coefﬁcients (the binary representation of the index ends in 1). It follows that A.x/ D AŒ0.x2/ C xAŒ1.x2/ ; (30.9) so that the problem of evaluating A.x/ at !0 n; !1 n; : : : ; !n1 n reduces to 1. evaluating the degree-bound n=2 polynomials AŒ0.x/ and AŒ1.x/ at the points .!0 n/2; .!1 n/2; : : : ; .!n1 n /2 ; (30.10) and then 2. combining the results according to equation (30.9). By the halving lemma, the list of values (30.10) consists not of n distinct values but only of the n=2 complex .n=2/th roots of unity, with each root occurring exactly twice. Therefore, we recursively evaluate the polynomials AŒ0 and AŒ1 of degree-bound n=2 at the n=2 complex .n=2/th roots of unity. These subproblems have exactly the same form as the original problem, but are half the size. We have now successfully divided an n-element DFTn computation into two n=2- element DFTn=2 computations. This decomposition is the basis for the following recursive FFT algorithm, which computes the DFT of an n-element vector a D .a0; a1; : : : ; an1/, where n is a power of 2.

## 30.2 The DFT and FFT

RECURSIVE-FFT.a/ n D a:length // n is a power of 2 if n == 1 return a !n D e2i=n ! D 1 aŒ0 D .a0; a2; : : : ; an2/ aŒ1 D .a1; a3; : : : ; an1/ yŒ0 D RECURSIVE-FFT.aŒ0/ yŒ1 D RECURSIVE-FFT.aŒ1/ for k D 0 to n=2  1 yk D yŒ0 k C ! yŒ1 k ykC.n=2/ D yŒ0 k  ! yŒ1 k ! D ! !n return y // y is assumed to be a column vector The RECURSIVE-FFT procedure works as follows. Lines 2–3 represent the basis of the recursion; the DFT of one element is the element itself, since in this case y0 D a0 !0 D a0  1 D a0 :

Lines 6–7 deﬁne the coefﬁcient vectors for the polynomials AŒ0 and AŒ1. Lines 4, 5, and 13 guarantee that ! is updated properly so that whenever lines 11–12 are executed, we have ! D !k n. (Keeping a running value of ! from iteration to iteration saves time over computing !k n from scratch each time through the for loop.) Lines 8–9 perform the recursive DFTn=2 computations, setting, for k D 0; 1; : : : ; n=2  1, yŒ0 k D AŒ0.!k n=2/ ; yŒ1 k D AŒ1.!k n=2/ ; or, since !k n=2 D !2k n by the cancellation lemma, yŒ0 k D AŒ0.!2k n / ; yŒ1 k D AŒ1.!2k n / :

Lines 11–12 combine the results of the recursive DFTn=2 calculations. For y0; y1; : : : ; yn=21, line 11 yields yk D yŒ0 k C !k nyŒ1 k D AŒ0.!2k n / C !k nAŒ1.!2k n / D A.!k n/ (by equation (30.9)) .

For yn=2; yn=2C1; : : : ; yn1, letting k D 0; 1; : : : ; n=2  1, line 12 yields ykC.n=2/ D yŒ0 k  !k nyŒ1 k D yŒ0 k C !kC.n=2/ n yŒ1 k (since !kC.n=2/ n D !k n) D AŒ0.!2k n / C !kC.n=2/ n AŒ1.!2k n / D AŒ0.!2kCn n / C !kC.n=2/ n AŒ1.!2kCn n / (since !2kCn n D !2k n ) D A.!kC.n=2/ n / (by equation (30.9)) . Thus, the vector y returned by RECURSIVE-FFT is indeed the DFT of the input vector a.

Lines 11 and 12 multiply each value yŒ1 k by !k n, for k D 0; 1; : : : ; n=2  1.

Line 11 adds this product to yŒ0 k , and line 12 subtracts it. Because we use each factor !k n in both its positive and negative forms, we call the factors !k n twiddle factors. To determine the running time of procedure RECURSIVE-FFT, we note that exclusive of the recursive calls, each invocation takes time ‚.n/, where n is the length of the input vector. The recurrence for the running time is therefore T .n/ D 2T .n=2/ C ‚.n/ D ‚.n lg n/ : Thus, we can evaluate a polynomial of degree-bound n at the complex nth roots of unity in time ‚.n lg n/ using the fast Fourier transform. Interpolation at the complex roots of unity We now complete the polynomial multiplication scheme by showing how to interpolate the complex roots of unity by a polynomial, which enables us to convert from point-value form back to coefﬁcient form. We interpolate by writing the DFT as a matrix equation and then looking at the form of the matrix inverse.

From equation (30.4), we can write the DFT as the matrix product y D Vna, where Vn is a Vandermonde matrix containing the appropriate powers of !n:

## 30.2 The DFT and FFT

 y0 y1 y2 y3 ::: yn1  D  !n !2 n !3 n !n1 n !2 n !4 n !6 n !2.n1/ n !3 n !6 n !9 n !3.n1/ n ::: ::: ::: ::: ::: ::: 1 !n1 n !2.n1/ n !3.n1/ n    !.n1/.n1/ n  a0 a1 a2 a3 ::: an1  : The .k; j / entry of Vn is !kj n , for j; k D 0; 1; : : : ; n  1. The exponents of the entries of Vn form a multiplication table.

For the inverse operation, which we write as a D DFT1 n .y/, we proceed by multiplying y by the matrix V 1 n , the inverse of Vn.

> **Theorem 30.7**

For j; k D 0; 1; : : : ; n  1, the .j; k/ entry of V 1 n is !kj n =n.

Proof We show that V 1 n Vn D In, the n 	 n identity matrix. Consider the .j; j 0/ entry of V 1 n Vn:

ŒV 1 n Vnjj 0 D n1 X kD0 .!kj n =n/.!kj 0 n / D n1 X kD0 !k.j 0j/ n =n : This summation equals 1 if j 0 D j , and it is 0 otherwise by the summation lemma (Lemma 30.6). Note that we rely on .n  1/  j 0  j  n  1, so that j 0  j is not divisible by n, in order for the summation lemma to apply.

Given the inverse matrix V 1 n , we have that DFT1 n .y/ is given by aj D 1 n n1 X kD0 yk!kj n (30.11) for j D 0; 1; : : : ; n  1. By comparing equations (30.8) and (30.11), we see that by modifying the FFT algorithm to switch the roles of a and y, replace !n by !1 n , and divide each element of the result by n, we compute the inverse DFT (see Exercise 30.2-4). Thus, we can compute DFT1 n in ‚.n lg n/ time as well. We see that, by using the FFT and the inverse FFT, we can transform a polynomial of degree-bound n back and forth between its coefﬁcient representation and a point-value representation in time ‚.n lg n/. In the context of polynomial multiplication, we have shown the following.

> **Theorem 30.8 (Convolution theorem)**

For any two vectors a and b of length n, where n is a power of 2, a ˝ b D DFT1 2n.DFT2n.a/  DFT2n.b// ; where the vectors a and b are padded with 0s to length 2n and  denotes the componentwise product of two 2n-element vectors.

## Exercises

30.2-1 Prove Corollary 30.4. 30.2-2 Compute the DFT of the vector .0; 1; 2; 3/. 30.2-3 Do Exercise 30.1-1 by using the ‚.n lg n/-time scheme. 30.2-4 Write pseudocode to compute DFT1 n in ‚.n lg n/ time. 30.2-5 Describe the generalization of the FFT procedure to the case in which n is a power of 3. Give a recurrence for the running time, and solve the recurrence. 30.2-6 ?

Suppose that instead of performing an n-element FFT over the ﬁeld of complex numbers (where n is even), we use the ring Zm of integers modulo m, where m D 2tn=2 C 1 and t is an arbitrary positive integer. Use ! D 2t instead of !n as a principal nth root of unity, modulo m. Prove that the DFT and the inverse DFT are well deﬁned in this system. 30.2-7 Given a list of values ´0; ´1; : : : ; ´n1 (possibly with repetitions), show how to ﬁnd the coefﬁcients of a polynomial P.x/ of degree-bound n C 1 that has zeros only at ´0; ´1; : : : ; ´n1 (possibly with repetitions). Your procedure should run in time O.n lg2 n/. (Hint: The polynomial P.x/ has a zero at ´j if and only if P.x/ is a multiple of .x  ´j/.) 30.2-8 ? The chirp transform of a vector a D .a0; a1; : : : ; an1/ is the vector y D .y0; y1; : : : ; yn1/, where yk D Pn1 jD0 aj´kj and ´ is any complex number. The

## 30.3 Efﬁcient FFT implementations

DFT is therefore a special case of the chirp transform, obtained by taking ´ D !n.

Show how to evaluate the chirp transform in time O.n lg n/ for any complex number ´. (Hint: Use the equation yk D ´k2=2 n1 X jD0  aj´j 2=2  ´.kj/2=2 to view the chirp transform as a convolution.)

## 30.3 Efﬁcient FFT implementations

Since the practical applications of the DFT, such as signal processing, demand the utmost speed, this section examines two efﬁcient FFT implementations. First, we shall examine an iterative version of the FFT algorithm that runs in ‚.n lg n/ time but can have a lower constant hidden in the ‚-notation than the recursive version in Section 30.2. (Depending on the exact implementation, the recursive version may use the hardware cache more efﬁciently.) Then, we shall use the insights that led us to the iterative implementation to design an efﬁcient parallel FFT circuit. An iterative FFT implementation We ﬁrst note that the for loop of lines 10–13 of RECURSIVE-FFT involves computing the value !k n yŒ1 k twice. In compiler terminology, we call such a value a common subexpression. We can change the loop to compute it only once, storing it in a temporary variable t. for k D 0 to n=2  1 t D ! yŒ1 k yk D yŒ0 k C t ykC.n=2/ D yŒ0 k  t ! D ! !n The operation in this loop, multiplying the twiddle factor ! D !k n by yŒ1 k , storing the product into t, and adding and subtracting t from yŒ0 k , is known as a butterﬂy operation and is shown schematically in Figure 30.3. We now show how to make the FFT algorithm iterative rather than recursive in structure. In Figure 30.4, we have arranged the input vectors to the recursive calls in an invocation of RECURSIVE-FFT in a tree structure, where the initial call is for n D 8. The tree has one node for each call of the procedure, labeled

+ – • (a) (b) yŒ0 k yŒ0 k yŒ1 k yŒ1 k !k n !k n yŒ0 k C !k nyŒ1 k yŒ0 k C !k nyŒ1 k yŒ0 k  !k nyŒ1 k yŒ0 k  !k nyŒ1 k Figure 30.3 A butterﬂy operation. (a) The two input values enter from the left, the twiddle factor !k n is multiplied by yŒ1 k , and the sum and difference are output on the right. (b) A simpliﬁed drawing of a butterﬂy operation. We will use this representation in a parallel FFT circuit. (a0,a1,a2,a3,a4,a5,a6,a7) (a0,a2,a4,a6) (a0,a4) (a2,a6) (a0) (a4) (a2) (a6) (a1,a3,a5,a7) (a1,a5) (a1) (a5) (a3,a7) (a3) (a7) Figure 30.4 The tree of input vectors to the recursive calls of the RECURSIVE-FFT procedure. The initial invocation is for n D 8. by the corresponding input vector. Each RECURSIVE-FFT invocation makes two recursive calls, unless it has received a 1-element vector. The ﬁrst call appears in the left child, and the second call appears in the right child.

Looking at the tree, we observe that if we could arrange the elements of the initial vector a into the order in which they appear in the leaves, we could trace the execution of the RECURSIVE-FFT procedure, but bottom up instead of top down. First, we take the elements in pairs, compute the DFT of each pair using one butterﬂy operation, and replace the pair with its DFT. The vector then holds n=2 2-element DFTs. Next, we take these n=2 DFTs in pairs and compute the DFT of the four vector elements they come from by executing two butterﬂy operations, replacing two 2-element DFTs with one 4-element DFT. The vector then holds n=4 4-element DFTs. We continue in this manner until the vector holds two .n=2/-element DFTs, which we combine using n=2 butterﬂy operations into the ﬁnal n-element DFT. To turn this bottom-up approach into code, we use an array AŒ0 : : n  1 that initially holds the elements of the input vector a in the order in which they appear

## 30.3 Efﬁcient FFT implementations

in the leaves of the tree of Figure 30.4. (We shall show later how to determine this order, which is known as a bit-reversal permutation.) Because we have to combine DFTs on each level of the tree, we introduce a variable s to count the levels, ranging from 1 (at the bottom, when we are combining pairs to form 2-element DFTs) to lg n (at the top, when we are combining two .n=2/-element DFTs to produce the ﬁnal result). The algorithm therefore has the following structure: for s D 1 to lg n for k D 0 to n  1 by 2s combine the two 2s1-element DFTs in AŒk : : k C 2s1  1 and AŒk C 2s1 : : k C 2s  1 into one 2s-element DFT in AŒk : : k C 2s  1 We can express the body of the loop (line 3) as more precise pseudocode. We copy the for loop from the RECURSIVE-FFT procedure, identifying yŒ0 with AŒk : : k C 2s1  1 and yŒ1 with AŒk C 2s1 : : k C 2s  1. The twiddle factor used in each butterﬂy operation depends on the value of s; it is a power of !m, where m D 2s. (We introduce the variable m solely for the sake of readability.) We introduce another temporary variable u that allows us to perform the butterﬂy operation in place. When we replace line 3 of the overall structure by the loop body, we get the following pseudocode, which forms the basis of the parallel implementation we shall present later. The code ﬁrst calls the auxiliary procedure BIT-REVERSE-COPY.a; A/ to copy vector a into array A in the initial order in which we need the values.

ITERATIVE-FFT.a/ BIT-REVERSE-COPY.a; A/ n D a:length // n is a power of 2 for s D 1 to lg n m D 2s !m D e2i=m for k D 0 to n  1 by m ! D 1 for j D 0 to m=2  1 t D ! AŒk C j C m=2 u D AŒk C j  AŒk C j  D u C t AŒk C j C m=2 D u  t ! D ! !m return A How does BIT-REVERSE-COPY get the elements of the input vector a into the desired order in the array A? The order in which the leaves appear in Figure 30.4

is a bit-reversal permutation. That is, if we let rev.k/ be the lg n-bit integer formed by reversing the bits of the binary representation of k, then we want to place vector element ak in array position AŒrev.k/. In Figure 30.4, for example, the leaves appear in the order 0; 4; 2; 6; 1; 5; 3; 7; this sequence in binary is 000; 100; 010; 110; 001; 101; 011; 111, and when we reverse the bits of each value we get the sequence 000; 001; 010; 011; 100; 101; 110; 111. To see that we want a bit-reversal permutation in general, we note that at the top level of the tree, indices whose low-order bit is 0 go into the left subtree and indices whose low-order bit is 1 go into the right subtree. Stripping off the low-order bit at each level, we continue this process down the tree, until we get the order given by the bit-reversal permutation at the leaves.

Since we can easily compute the function rev.k/, the BIT-REVERSE-COPY procedure is simple:

BIT-REVERSE-COPY.a; A/ n D a:length for k D 0 to n  1 AŒrev.k/ D ak The iterative FFT implementation runs in time ‚.n lg n/. The call to BIT- REVERSE-COPY.a; A/ certainly runs in O.n lg n/ time, since we iterate n times and can reverse an integer between 0 and n  1, with lg n bits, in O.lg n/ time. (In practice, because we usually know the initial value of n in advance, we would probably code a table mapping k to rev.k/, making BIT-REVERSE-COPY run in ‚.n/ time with a low hidden constant. Alternatively, we could use the clever amortized reverse binary counter scheme described in Problem 17-1.) To complete the proof that ITERATIVE-FFT runs in time ‚.n lg n/, we show that L.n/, the number of times the body of the innermost loop (lines 8–13) executes, is ‚.n lg n/. The for loop of lines 6–13 iterates n=m D n=2s times for each value of s, and the innermost loop of lines 8–13 iterates m=2 D 2s1 times. Thus, L.n/ D lg n X sD1 n 2s  2s1 D lg n X sD1 n D ‚.n lg n/ :

## 30.3 Efﬁcient FFT implementations

a0 a1 a2 a3 a4 a5 a6 a7 y0 y1 y2 y3 y4 y5 y6 y7 stage s D 1 stage s D 2 stage s D 3 !0 !0 !0 !0 !0 !0 !1 !1 !0 !1 !2 !3 Figure 30.5 A circuit that computes the FFT in parallel, here shown on n D 8 inputs. Each butterﬂy operation takes as input the values on two wires, along with a twiddle factor, and it produces as outputs the values on two wires. The stages of butterﬂies are labeled to correspond to iterations of the outermost loop of the ITERATIVE-FFT procedure. Only the top and bottom wires passing through a butterﬂy interact with it; wires that pass through the middle of a butterﬂy do not affect that butterﬂy, nor are their values changed by that butterﬂy. For example, the top butterﬂy in stage 2 has nothing to do with wire 1 (the wire whose output is labeled y1); its inputs and outputs are only on wires 0 and 2 (labeled y0 and y2, respectively). This circuit has depth ‚.lg n/ and performs ‚.n lg n/ butterﬂy operations altogether.

A parallel FFT circuit We can exploit many of the properties that allowed us to implement an efﬁcient iterative FFT algorithm to produce an efﬁcient parallel algorithm for the FFT. We will express the parallel FFT algorithm as a circuit. Figure 30.5 shows a parallel FFT circuit, which computes the FFT on n inputs, for n D 8. The circuit begins with a bit-reverse permutation of the inputs, followed by lg n stages, each stage consisting of n=2 butterﬂies executed in parallel. The depth of the circuit—the maximum number of computational elements between any output and any input that can reach it—is therefore ‚.lg n/. The leftmost part of the parallel FFT circuit performs the bit-reverse permutation, and the remainder mimics the iterative ITERATIVE-FFT procedure. Because each iteration of the outermost for loop performs n=2 independent butterﬂy operations, the circuit performs them in parallel. The value of s in each iteration within

ITERATIVE-FFT corresponds to a stage of butterﬂies shown in Figure 30.5. For s D 1; 2; : : : ; lg n, stage s consists of n=2s groups of butterﬂies (corresponding to each value of k in ITERATIVE-FFT), with 2s1 butterﬂies per group (corresponding to each value of j in ITERATIVE-FFT). The butterﬂies shown in Figure 30.5 correspond to the butterﬂy operations of the innermost loop (lines 9–12 of ITERATIVE- FFT). Note also that the twiddle factors used in the butterﬂies correspond to those used in ITERATIVE-FFT: in stage s, we use !0 m; !1 m; : : : ; !m=21 m , where m D 2s.

## Exercises

30.3-1 Show how ITERATIVE-FFT computes the DFT of the input vector .0; 2; 3; 1; 4; 5; 7; 9/. 30.3-2 Show how to implement an FFT algorithm with the bit-reversal permutation occurring at the end, rather than at the beginning, of the computation. (Hint: Consider the inverse DFT.) 30.3-3 How many times does ITERATIVE-FFT compute twiddle factors in each stage?

Rewrite ITERATIVE-FFT to compute twiddle factors only 2s1 times in stage s. 30.3-4 ?

Suppose that the adders within the butterﬂy operations of the FFT circuit sometimes fail in such a manner that they always produce a zero output, independent of their inputs. Suppose that exactly one adder has failed, but that you don’t know which one. Describe how you can identify the failed adder by supplying inputs to the overall FFT circuit and observing the outputs. How efﬁcient is your method?

## Problems

30-1 Divide-and-conquer multiplication a. Show how to multiply two linear polynomials ax C b and cx C d using only three multiplications. (Hint: One of the multiplications is .a C b/  .c C d/.) b. Give two divide-and-conquer algorithms for multiplying two polynomials of degree-bound n in ‚.nlg 3/ time. The ﬁrst algorithm should divide the input polynomial coefﬁcients into a high half and a low half, and the second algorithm should divide them according to whether their index is odd or even.

Problems for Chapter 30 c. Show how to multiply two n-bit integers in O.nlg 3/ steps, where each step operates on at most a constant number of 1-bit values. 30-2 Toeplitz matrices A Toeplitz matrix is an n 	 n matrix A D .aij/ such that aij D ai1;j1 for i D 2; 3; : : : ; n and j D 2; 3; : : : ; n. a. Is the sum of two Toeplitz matrices necessarily Toeplitz? What about the product? b. Describe how to represent a Toeplitz matrix so that you can add two n 	 n Toeplitz matrices in O.n/ time. c. Give an O.n lg n/-time algorithm for multiplying an n 	 n Toeplitz matrix by a vector of length n. Use your representation from part (b). d. Give an efﬁcient algorithm for multiplying two n	n Toeplitz matrices. Analyze its running time. 30-3 Multidimensional fast Fourier transform We can generalize the 1-dimensional discrete Fourier transform deﬁned by equation (30.8) to d dimensions. The input is a d-dimensional array A D .aj1;j2;:::;jd / whose dimensions are n1; n2; : : : ; nd, where n1n2    nd D n. We deﬁne the d-dimensional discrete Fourier transform by the equation yk1;k2;:::;kd D n11 X j1D0 n21 X j2D0 nd 1 X jd D0 aj1;j2;:::;jd !j1k1 n1 !j2k2 n2    !jd kd nd for 0  k1 < n1, 0  k2 < n2, . . . , 0  kd < nd. a. Show that we can compute a d-dimensional DFT by computing 1-dimensional DFTs on each dimension in turn. That is, we ﬁrst compute n=n1 separate 1-dimensional DFTs along dimension 1. Then, using the result of the DFTs along dimension 1 as the input, we compute n=n2 separate 1-dimensional DFTs along dimension 2. Using this result as the input, we compute n=n3 separate 1-dimensional DFTs along dimension 3, and so on, through dimension d. b. Show that the ordering of dimensions does not matter, so that we can compute a d-dimensional DFT by computing the 1-dimensional DFTs in any order of the d dimensions.

c. Show that if we compute each 1-dimensional DFT by computing the fast Fourier transform, the total time to compute a d-dimensional DFT is O.n lg n/, independent of d. 30-4 Evaluating all derivatives of a polynomial at a point Given a polynomial A.x/ of degree-bound n, we deﬁne its tth derivative by A.t/.x/ D „ A.x/ if t D 0 ; d dxA.t1/.x/ if 1  t  n  1 ; if t  n :

From the coefﬁcient representation .a0; a1; : : : ; an1/ of A.x/ and a given point x0, we wish to determine A.t/.x0/ for t D 0; 1; : : : ; n  1. a. Given coefﬁcients b0; b1; : : : ; bn1 such that A.x/ D n1 X jD0 bj.x  x0/j ; show how to compute A.t/.x0/, for t D 0; 1; : : : ; n  1, in O.n/ time. b. Explain how to ﬁnd b0; b1; : : : ; bn1 in O.n lg n/ time, given A.x0 C !k n/ for k D 0; 1; : : : ; n  1. c. Prove that A.x0 C !k n/ D n1 X rD0

!kr n rŠ n1 X jD0 f .j /g.r  j / ! ; where f .j / D aj  j Š and g.l/ D ( xl 0 =.l/Š if .n  1/  l  0 ; if 1  l  n  1 : d. Explain how to evaluate A.x0 C !k n/ for k D 0; 1; : : : ; n  1 in O.n lg n/ time. Conclude that we can evaluate all nontrivial derivatives of A.x/ at x0 in O.n lg n/ time.

Problems for Chapter 30 30-5 Polynomial evaluation at multiple points We have seen how to evaluate a polynomial of degree-bound n at a single point in O.n/ time using Horner’s rule. We have also discovered how to evaluate such a polynomial at all n complex roots of unity in O.n lg n/ time using the FFT. We shall now show how to evaluate a polynomial of degree-bound n at n arbitrary points in O.n lg2 n/ time. To do so, we shall assume that we can compute the polynomial remainder when one such polynomial is divided by another in O.n lg n/ time, a result that we state without proof. For example, the remainder of 3x3 C x2  3x C 1 when divided by x2 C x C 2 is .3x3 C x2  3x C 1/ mod .x2 C x C 2/ D 7x C 5 :

Given the coefﬁcient representation of a polynomial A.x/ D Pn1 kD0 akxk and n points x0; x1; : : : ; xn1, we wish to compute the n values A.x0/; A.x1/; : : : ; A.xn1/. For 0  i  j  n  1, deﬁne the polynomials Pij.x/ D Qj kDi.x  xk/ and Qij.x/ D A.x/ mod Pij.x/. Note that Qij .x/ has degree at most j  i. a. Prove that A.x/ mod .x  ´/ D A.´/ for any point ´. b. Prove that Qkk.x/ D A.xk/ and that Q0;n1.x/ D A.x/. c. Prove that for i  k  j , we have Qik.x/ D Qij.x/ mod Pik.x/ and Qkj .x/ D Qij.x/ mod Pkj .x/. d. Give an O.n lg2 n/-time algorithm to evaluate A.x0/; A.x1/; : : : ; A.xn1/. 30-6 FFT using modular arithmetic As deﬁned, the discrete Fourier transform requires us to compute with complex numbers, which can result in a loss of precision due to round-off errors. For some problems, the answer is known to contain only integers, and by using a variant of the FFT based on modular arithmetic, we can guarantee that the answer is calculated exactly. An example of such a problem is that of multiplying two polynomials with integer coefﬁcients. Exercise 30.2-6 gives one approach, using a modulus of length .n/ bits to handle a DFT on n points. This problem gives another approach, which uses a modulus of the more reasonable length O.lg n/; it requires that you understand the material of Chapter 31. Let n be a power of 2. a. Suppose that we search for the smallest k such that p D kn C 1 is prime. Give a simple heuristic argument why we might expect k to be approximately ln n. (The value of k might be much larger or smaller, but we can reasonably expect to examine O.lg n/ candidate values of k on average.) How does the expected length of p compare to the length of n?

Let g be a generator of Z p, and let w D gk mod p. b. Argue that the DFT and the inverse DFT are well-deﬁned inverse operations modulo p, where w is used as a principal nth root of unity. c. Show how to make the FFT and its inverse work modulo p in time O.n lg n/, where operations on words of O.lg n/ bits take unit time. Assume that the algorithm is given p and w. d. Compute the DFT modulo p D 17 of the vector .0; 5; 3; 7; 7; 2; 1; 6/. Note that g D 3 is a generator of Z 17.

Chapter notes Van Loan’s book [343] provides an outstanding treatment of the fast Fourier transform. Press, Teukolsky, Vetterling, and Flannery [283, 284] have a good description of the fast Fourier transform and its applications. For an excellent introduction to signal processing, a popular FFT application area, see the texts by Oppenheim and Schafer [266] and Oppenheim and Willsky [267]. The Oppenheim and Schafer book also shows how to handle cases in which n is not an integer power of 2.

Fourier analysis is not limited to 1-dimensional data. It is widely used in image processing to analyze data in 2 or more dimensions. The books by Gonzalez and Woods [146] and Pratt [281] discuss multidimensional Fourier transforms and their use in image processing, and books by Tolimieri, An, and Lu [338] and Van Loan [343] discuss the mathematics of multidimensional fast Fourier transforms.

Cooley and Tukey [76] are widely credited with devising the FFT in the 1960s. The FFT had in fact been discovered many times previously, but its importance was not fully realized before the advent of modern digital computers. Although Press, Teukolsky, Vetterling, and Flannery attribute the origins of the method to Runge and K¨onig in 1924, an article by Heideman, Johnson, and Burrus [163] traces the history of the FFT as far back as C. F. Gauss in 1805.

Frigo and Johnson [117] developed a fast and ﬂexible implementation of the FFT, called FFTW (“fastest Fourier transform in the West”). FFTW is designed for situations requiring multiple DFT computations on the same problem size. Before actually computing the DFTs, FFTW executes a “planner,” which, by a series of trial runs, determines how best to decompose the FFT computation for the given problem size on the host machine. FFTW adapts to use the hardware cache ef- ﬁciently, and once subproblems are small enough, FFTW solves them with optimized, straight-line code. Furthermore, FFTW has the unusual advantage of taking ‚.n lg n/ time for any problem size n, even when n is a large prime.

Notes for Chapter 30 Although the standard Fourier transform assumes that the input represents points that are uniformly spaced in the time domain, other techniques can approximate the FFT on “nonequispaced” data. The article by Ware [348] provides an overview.
