# 31 Number-Theoretic Algorithms

Number theory was once viewed as a beautiful but largely useless subject in pure mathematics. Today number-theoretic algorithms are used widely, due in large part to the invention of cryptographic schemes based on large prime numbers. These schemes are feasible because we can ﬁnd large primes easily, and they are secure because we do not know how to factor the product of large primes (or solve related problems, such as computing discrete logarithms) efﬁciently. This chapter presents some of the number theory and related algorithms that underlie such applications.

Section 31.1 introduces basic concepts of number theory, such as divisibility, modular equivalence, and unique factorization. Section 31.2 studies one of the world’s oldest algorithms: Euclid’s algorithm for computing the greatest common divisor of two integers. Section 31.3 reviews concepts of modular arithmetic. Section 31.4 then studies the set of multiples of a given number a, modulo n, and shows how to ﬁnd all solutions to the equation ax  b .mod n/ by using Euclid’s algorithm. The Chinese remainder theorem is presented in Section 31.5. Section 31.6 considers powers of a given number a, modulo n, and presents a repeated-squaring algorithm for efﬁciently computing ab mod n, given a, b, and n. This operation is at the heart of efﬁcient primality testing and of much modern cryptography. Section 31.7 then describes the RSA public-key cryptosystem. Section 31.8 examines a randomized primality test. We can use this test to ﬁnd large primes efﬁciently, which we need to do in order to create keys for the RSA cryptosystem. Finally, Section 31.9 reviews a simple but effective heuristic for factoring small integers. It is a curious fact that factoring is one problem people may wish to be intractable, since the security of RSA depends on the difﬁculty of factoring large integers.

Size of inputs and cost of arithmetic computations Because we shall be working with large integers, we need to adjust how we think about the size of an input and about the cost of elementary arithmetic operations. In this chapter, a “large input” typically means an input containing “large integers” rather than an input containing “many integers” (as for sorting). Thus,

## 31.1 Elementary number-theoretic notions

we shall measure the size of an input in terms of the number of bits required to represent that input, not just the number of integers in the input. An algorithm with integer inputs a1; a2; : : : ; ak is a polynomial-time algorithm if it runs in time polynomial in lg a1; lg a2; : : : ; lg ak, that is, polynomial in the lengths of its binaryencoded inputs. In most of this book, we have found it convenient to think of the elementary arithmetic operations (multiplications, divisions, or computing remainders) as primitive operations that take one unit of time. By counting the number of such arithmetic operations that an algorithm performs, we have a basis for making a reasonable estimate of the algorithm’s actual running time on a computer. Elementary operations can be time-consuming, however, when their inputs are large. It thus becomes convenient to measure how many bit operations a number-theoretic algorithm requires. In this model, multiplying two ˇ-bit integers by the ordinary method uses ‚.ˇ2/ bit operations. Similarly, we can divide a ˇ-bit integer by a shorter integer or take the remainder of a ˇ-bit integer when divided by a shorter integer in time ‚.ˇ2/ by simple algorithms. (See Exercise 31.1-12.) Faster methods are known. For example, a simple divide-and-conquer method for multiplying two ˇ-bit integers has a running time of ‚.ˇlg 3/, and the fastest known method has a running time of ‚.ˇ lg ˇ lg lg ˇ/. For practical purposes, however, the ‚.ˇ2/ algorithm is often best, and we shall use this bound as a basis for our analyses. We shall generally analyze algorithms in this chapter in terms of both the number of arithmetic operations and the number of bit operations they require.

## 31.1 Elementary number-theoretic notions

This section provides a brief review of notions from elementary number theory concerning the set Z D f: : : ; 2; 1; 0; 1; 2; : : :g of integers and the set N D f0; 1; 2; : : :g of natural numbers.

Divisibility and divisors The notion of one integer being divisible by another is key to the theory of numbers. The notation d j a (read “d divides a”) means that a D kd for some integer k.

Every integer divides 0. If a > 0 and d j a, then jdj  jaj. If d j a, then we also say that a is a multiple of d. If d does not divide a, we write d −a. If d j a and d  0, we say that d is a divisor of a. Note that d j a if and only if d j a, so that no generality is lost by deﬁning the divisors to be nonnegative, with the understanding that the negative of any divisor of a also divides a. A

divisor of a nonzero integer a is at least 1 but not greater than jaj. For example, the divisors of 24 are 1, 2, 3, 4, 6, 8, 12, and 24.

Every positive integer a is divisible by the trivial divisors 1 and a. The nontrivial divisors of a are the factors of a. For example, the factors of 20 are 2, 4, 5, and 10.

Prime and composite numbers An integer a > 1 whose only divisors are the trivial divisors 1 and a is a prime number or, more simply, a prime. Primes have many special properties and play a critical role in number theory. The ﬁrst 20 primes, in order, are 2; 3; 5; 7; 11; 13; 17; 19; 23; 29; 31; 37; 41; 43; 47; 53; 59; 61; 67; 71 :

Exercise 31.1-2 asks you to prove that there are inﬁnitely many primes. An integer a > 1 that is not prime is a composite number or, more simply, a composite. For example, 39 is composite because 3 j 39. We call the integer 1 a unit, and it is neither prime nor composite. Similarly, the integer 0 and all negative integers are neither prime nor composite. The division theorem, remainders, and modular equivalence Given an integer n, we can partition the integers into those that are multiples of n and those that are not multiples of n. Much number theory is based upon reﬁning this partition by classifying the nonmultiples of n according to their remainders when divided by n. The following theorem provides the basis for this reﬁnement. We omit the proof (but see, for example, Niven and Zuckerman [265]).

> **Theorem 31.1 (Division theorem)**

For any integer a and any positive integer n, there exist unique integers q and r such that 0  r < n and a D qn C r. The value q D ba=nc is the quotient of the division. The value r D a mod n is the remainder (or residue) of the division. We have that n j a if and only if a mod n D 0. We can partition the integers into n equivalence classes according to their remainders modulo n. The equivalence class modulo n containing an integer a is Œan D fa C kn W k 2 Zg :

For example, Œ37 D f: : : ; 11; 4; 3; 10; 17; : : :g; we can also denote this set by Œ47 and Œ107. Using the notation deﬁned on page 54, we can say that writing a 2 Œbn is the same as writing a  b .mod n/. The set of all such equivalence classes is

## 31.1 Elementary number-theoretic notions

Zn D fŒan W 0  a  n  1g : (31.1) When you see the deﬁnition Zn D f0; 1; : : : ; n  1g ; (31.2) you should read it as equivalent to equation (31.1) with the understanding that 0 represents Œ0n, 1 represents Œ1n, and so on; each class is represented by its smallest nonnegative element. You should keep the underlying equivalence classes in mind, however. For example, if we refer to 1 as a member of Zn, we are really referring to Œn  1n, since 1  n  1 .mod n/.

Common divisors and greatest common divisors If d is a divisor of a and d is also a divisor of b, then d is a common divisor of a and b. For example, the divisors of 30 are 1, 2, 3, 5, 6, 10, 15, and 30, and so the common divisors of 24 and 30 are 1, 2, 3, and 6. Note that 1 is a common divisor of any two integers. An important property of common divisors is that d j a and d j b implies d j .a C b/ and d j .a  b/ : (31.3) More generally, we have that d j a and d j b implies d j .ax C by/ (31.4) for any integers x and y. Also, if a j b, then either jaj  jbj or b D 0, which implies that a j b and b j a implies a D ˙b : (31.5) The greatest common divisor of two integers a and b, not both zero, is the largest of the common divisors of a and b; we denote it by gcd.a; b/. For example, gcd.24; 30/ D 6, gcd.5; 7/ D 1, and gcd.0; 9/ D 9. If a and b are both nonzero, then gcd.a; b/ is an integer between 1 and min.jaj ; jbj/. We deﬁne gcd.0; 0/ to be 0; this deﬁnition is necessary to make standard properties of the gcd function (such as equation (31.9) below) universally valid. The following are elementary properties of the gcd function: gcd.a; b/ D gcd.b; a/ ; (31.6) gcd.a; b/ D gcd.a; b/ ; (31.7) gcd.a; b/ D gcd.jaj ; jbj/ ; (31.8) gcd.a; 0/ D jaj ; (31.9) gcd.a; ka/ D jaj for any k 2 Z : (31.10) The following theorem provides an alternative and useful characterization of gcd.a; b/.

> **Theorem 31.2**

If a and b are any integers, not both zero, then gcd.a; b/ is the smallest positive element of the set fax C by W x; y 2 Zg of linear combinations of a and b.

Proof Let s be the smallest positive such linear combination of a and b, and let s D ax C by for some x; y 2 Z. Let q D ba=sc. Equation (3.8) then implies a mod s D a  qs D a  q.ax C by/ D a .1  qx/ C b .qy/ ; and so a mod s is a linear combination of a and b as well.

But, since 0  a mod s < s, we have that a mod s D 0, because s is the smallest positive such linear combination. Therefore, we have that s j a and, by analogous reasoning, s j b. Thus, s is a common divisor of a and b, and so gcd.a; b/  s. Equation (31.4) implies that gcd.a; b/ j s, since gcd.a; b/ divides both a and b and s is a linear combination of a and b. But gcd.a; b/ j s and s > 0 imply that gcd.a; b/  s.

Combining gcd.a; b/  s and gcd.a; b/  s yields gcd.a; b/ D s. We conclude that s is the greatest common divisor of a and b.

> **Corollary 31.3**

For any integers a and b, if d j a and d j b, then d j gcd.a; b/.

Proof This corollary follows from equation (31.4), because gcd.a; b/ is a linear combination of a and b by Theorem 31.2.

> **Corollary 31.4**

For all integers a and b and any nonnegative integer n, gcd.an; bn/ D n gcd.a; b/ :

Proof If n D 0, the corollary is trivial. If n > 0, then gcd.an; bn/ is the smallest positive element of the set fanx C bny W x; y 2 Zg, which is n times the smallest positive element of the set fax C by W x; y 2 Zg.

> **Corollary 31.5**

For all positive integers n, a, and b, if n j ab and gcd.a; n/ D 1, then n j b.

Proof We leave the proof as Exercise 31.1-5.

## 31.1 Elementary number-theoretic notions

Relatively prime integers Two integers a and b are relatively prime if their only common divisor is 1, that is, if gcd.a; b/ D 1. For example, 8 and 15 are relatively prime, since the divisors of 8 are 1, 2, 4, and 8, and the divisors of 15 are 1, 3, 5, and 15. The following theorem states that if two integers are each relatively prime to an integer p, then their product is relatively prime to p.

> **Theorem 31.6**

For any integers a, b, and p, if both gcd.a; p/ D 1 and gcd.b; p/ D 1, then gcd.ab; p/ D 1.

Proof It follows from Theorem 31.2 that there exist integers x, y, x0, and y0 such that ax C py D 1 ; bx0 C py0 D 1 :

Multiplying these equations and rearranging, we have ab.xx0/ C p.ybx0 C y0ax C pyy0/ D 1 :

Since 1 is thus a positive linear combination of ab and p, an appeal to Theorem 31.2 completes the proof. Integers n1, n2, . . . , nk are pairwise relatively prime if, whenever i ¤ j , we have gcd.ni; nj/ D 1.

Unique factorization An elementary but important fact about divisibility by primes is the following.

> **Theorem 31.7**

For all primes p and all integers a and b, if p j ab, then p j a or p j b (or both).

Proof Assume for the purpose of contradiction that p j ab, but that p −a and p −b. Thus, gcd.a; p/ D 1 and gcd.b; p/ D 1, since the only divisors of p are 1 and p, and we assume that p divides neither a nor b. Theorem 31.6 then implies that gcd.ab; p/ D 1, contradicting our assumption that p j ab, since p j ab implies gcd.ab; p/ D p. This contradiction completes the proof.

A consequence of Theorem 31.7 is that we can uniquely factor any composite integer into a product of primes.

> **Theorem 31.8 (Unique factorization)**

There is exactly one way to write any composite integer a as a product of the form a D pe1 1 pe2 2    per r ; where the pi are prime, p1 < p2 <    < pr, and the ei are positive integers.

Proof We leave the proof as Exercise 31.1-11. As an example, the number 6000 is uniquely factored into primes as 24  3  53.

## Exercises

31.1-1 Prove that if a > b > 0 and c D a C b, then c mod a D b. 31.1-2 Prove that there are inﬁnitely many primes. (Hint: Show that none of the primes p1; p2; : : : ; pk divide .p1p2    pk/ C 1.) 31.1-3 Prove that if a j b and b j c, then a j c. 31.1-4 Prove that if p is prime and 0 < k < p, then gcd.k; p/ D 1. 31.1-5 Prove Corollary 31.5. 31.1-6 Prove that if p is prime and 0 < k < p, then p j

p k

. Conclude that for all integers a and b and all primes p, .a C b/p  ap C bp .mod p/ : 31.1-7 Prove that if a and b are any positive integers such that a j b, then .x mod b/ mod a D x mod a for any x. Prove, under the same assumptions, that x  y .mod b/ implies x  y .mod a/ for any integers x and y.

## 31.2 Greatest common divisor

31.1-8 For any integer k > 0, an integer n is a kth power if there exists an integer a such that ak D n. Furthermore, n > 1 is a nontrivial power if it is a kth power for some integer k > 1. Show how to determine whether a given ˇ-bit integer n is a nontrivial power in time polynomial in ˇ. 31.1-9 Prove equations (31.6)–(31.10). 31.1-10 Show that the gcd operator is associative. That is, prove that for all integers a, b, and c, gcd.a; gcd.b; c// D gcd.gcd.a; b/; c/ : 31.1-11 ?

Prove Theorem 31.8. 31.1-12 Give efﬁcient algorithms for the operations of dividing a ˇ-bit integer by a shorter integer and of taking the remainder of a ˇ-bit integer when divided by a shorter integer. Your algorithms should run in time ‚.ˇ2/. 31.1-13 Give an efﬁcient algorithm to convert a given ˇ-bit (binary) integer to a decimal representation. Argue that if multiplication or division of integers whose length is at most ˇ takes time M.ˇ/, then we can convert binary to decimal in time ‚.M.ˇ/ lg ˇ/. (Hint: Use a divide-and-conquer approach, obtaining the top and bottom halves of the result with separate recursions.)

## 31.2 Greatest common divisor

In this section, we describe Euclid’s algorithm for efﬁciently computing the greatest common divisor of two integers. When we analyze the running time, we shall see a surprising connection with the Fibonacci numbers, which yield a worst-case input for Euclid’s algorithm. We restrict ourselves in this section to nonnegative integers. This restriction is justiﬁed by equation (31.8), which states that gcd.a; b/ D gcd.jaj ; jbj/.

In principle, we can compute gcd.a; b/ for positive integers a and b from the prime factorizations of a and b. Indeed, if a D pe1 1 pe2 2    per r ; (31.11) b D pf1 1 pf2 2    pfr r ; (31.12) with zero exponents being used to make the set of primes p1; p2; : : : ; pr the same for both a and b, then, as Exercise 31.2-1 asks you to show, gcd.a; b/ D pmin.e1;f1/ pmin.e2;f2/    pmin.er;fr/ r : (31.13) As we shall show in Section 31.9, however, the best algorithms to date for factoring do not run in polynomial time. Thus, this approach to computing greatest common divisors seems unlikely to yield an efﬁcient algorithm.

Euclid’s algorithm for computing greatest common divisors relies on the following theorem.

> **Theorem 31.9 (GCD recursion theorem)**

For any nonnegative integer a and any positive integer b, gcd.a; b/ D gcd.b; a mod b/ :

Proof We shall show that gcd.a; b/ and gcd.b; a mod b/ divide each other, so that by equation (31.5) they must be equal (since they are both nonnegative). We ﬁrst show that gcd.a; b/ j gcd.b; a mod b/. If we let d D gcd.a; b/, then d j a and d j b. By equation (3.8), a mod b D a  qb, where q D ba=bc.

Since a mod b is thus a linear combination of a and b, equation (31.4) implies that d j .a mod b/. Therefore, since d j b and d j .a mod b/, Corollary 31.3 implies that d j gcd.b; a mod b/ or, equivalently, that gcd.a; b/ j gcd.b; a mod b/: (31.14) Showing that gcd.b; a mod b/ j gcd.a; b/ is almost the same. If we now let d D gcd.b; a mod b/, then d j b and d j .a mod b/. Since a D qb C .a mod b/, where q D ba=bc, we have that a is a linear combination of b and .a mod b/. By equation (31.4), we conclude that d j a. Since d j b and d j a, we have that d j gcd.a; b/ by Corollary 31.3 or, equivalently, that gcd.b; a mod b/ j gcd.a; b/: (31.15) Using equation (31.5) to combine equations (31.14) and (31.15) completes the proof.

## 31.2 Greatest common divisor

Euclid’s algorithm The Elements of Euclid (circa 300 B.C.) describes the following gcd algorithm, although it may be of even earlier origin. We express Euclid’s algorithm as a recursive program based directly on Theorem 31.9. The inputs a and b are arbitrary nonnegative integers.

EUCLID.a; b/ if b == 0 return a else return EUCLID.b; a mod b/ As an example of the running of EUCLID, consider the computation of gcd.30; 21/:

EUCLID.30; 21/ D EUCLID.21; 9/ D EUCLID.9; 3/ D EUCLID.3; 0/ D 3 : This computation calls EUCLID recursively three times. The correctness of EUCLID follows from Theorem 31.9 and the property that if the algorithm returns a in line 2, then b D 0, so that equation (31.9) implies that gcd.a; b/ D gcd.a; 0/ D a. The algorithm cannot recurse indeﬁnitely, since the second argument strictly decreases in each recursive call and is always nonnegative. Therefore, EUCLID always terminates with the correct answer. The running time of Euclid’s algorithm We analyze the worst-case running time of EUCLID as a function of the size of a and b. We assume with no loss of generality that a > b  0. To justify this assumption, observe that if b > a  0, then EUCLID.a; b/ immediately makes the recursive call EUCLID.b; a/. That is, if the ﬁrst argument is less than the second argument, EUCLID spends one recursive call swapping its arguments and then proceeds. Similarly, if b D a > 0, the procedure terminates after one recursive call, since a mod b D 0. The overall running time of EUCLID is proportional to the number of recursive calls it makes. Our analysis makes use of the Fibonacci numbers Fk, deﬁned by the recurrence (3.22).

> **Lemma 31.10**

If a > b  1 and the call EUCLID.a; b/ performs k  1 recursive calls, then a  FkC2 and b  FkC1.

Proof The proof proceeds by induction on k. For the basis of the induction, let k D 1. Then, b  1 D F2, and since a > b, we must have a  2 D F3. Since b > .a mod b/, in each recursive call the ﬁrst argument is strictly larger than the second; the assumption that a > b therefore holds for each recursive call. Assume inductively that the lemma holds if k  1 recursive calls are made; we shall then prove that the lemma holds for k recursive calls. Since k > 0, we have b > 0, and EUCLID.a; b/ calls EUCLID.b; a mod b/ recursively, which in turn makes k  1 recursive calls. The inductive hypothesis then implies that b  FkC1 (thus proving part of the lemma), and a mod b  Fk. We have b C .a mod b/ D b C .a  b ba=bc/  a ; since a > b > 0 implies ba=bc  1. Thus, a  b C .a mod b/  FkC1 C Fk D FkC2 : The following theorem is an immediate corollary of this lemma.

> **Theorem 31.11 (Lam´e’s theorem)**

For any integer k  1, if a > b  1 and b < FkC1, then the call EUCLID.a; b/ makes fewer than k recursive calls. We can show that the upper bound of Theorem 31.11 is the best possible by showing that the call EUCLID.FkC1; Fk/ makes exactly k  1 recursive calls when k  2. We use induction on k. For the base case, k D 2, and the call EUCLID.F3; F2/ makes exactly one recursive call, to EUCLID.1; 0/. (We have to start at k D 2, because when k D 1 we do not have F2 > F1.) For the inductive step, assume that EUCLID.Fk; Fk1/ makes exactly k  2 recursive calls. For k > 2, we have Fk > Fk1 > 0 and FkC1 D Fk CFk1, and so by Exercise 31.1-1, we have FkC1 mod Fk D Fk1. Thus, we have gcd.FkC1; Fk/ D gcd.Fk; FkC1 mod Fk/ D gcd.Fk; Fk1/ : Therefore, the call EUCLID.FkC1; Fk/ recurses one time more than the call EUCLID.Fk; Fk1/, or exactly k  1 times, meeting the upper bound of Theorem 31.11.

Since Fk is approximately k= p 5, where  is the golden ratio .1 C p 5/=2 de- ﬁned by equation (3.24), the number of recursive calls in EUCLID is O.lg b/. (See

## 31.2 Greatest common divisor

a b ba=bc d x y 11 11 2 2 — Figure 31.1 How EXTENDED-EUCLID computes gcd.99; 78/. Each line shows one level of the recursion: the values of the inputs a and b, the computed value ba=bc, and the values d, x, and y returned. The triple .d; x; y/ returned becomes the triple .d 0; x0; y0/ used at the next higher level of recursion. The call EXTENDED-EUCLID.99; 78/ returns .3; 11; 14/, so that gcd.99; 78/ D 3 D 99  .11/ C 78  14.

Exercise 31.2-5 for a tighter bound.) Therefore, if we call EUCLID on two ˇ-bit numbers, then it performs O.ˇ/ arithmetic operations and O.ˇ3/ bit operations (assuming that multiplication and division of ˇ-bit numbers take O.ˇ2/ bit operations). Problem 31-2 asks you to show an O.ˇ2/ bound on the number of bit operations. The extended form of Euclid’s algorithm We now rewrite Euclid’s algorithm to compute additional useful information.

Speciﬁcally, we extend the algorithm to compute the integer coefﬁcients x and y such that d D gcd.a; b/ D ax C by : (31.16) Note that x and y may be zero or negative. We shall ﬁnd these coefﬁcients useful later for computing modular multiplicative inverses. The procedure EXTENDED- EUCLID takes as input a pair of nonnegative integers and returns a triple of the form .d; x; y/ that satisﬁes equation (31.16).

EXTENDED-EUCLID.a; b/ if b == 0 return .a; 1; 0/ else .d 0; x0; y0/ D EXTENDED-EUCLID.b; a mod b/ .d; x; y/ D .d 0; y0; x0  ba=bc y0/ return .d; x; y/ Figure 31.1 illustrates how EXTENDED-EUCLID computes gcd.99; 78/. The EXTENDED-EUCLID procedure is a variation of the EUCLID procedure.

Line 1 is equivalent to the test “b == 0” in line 1 of EUCLID. If b D 0, then

EXTENDED-EUCLID returns not only d D a in line 2, but also the coefﬁcients x D 1 and y D 0, so that a D ax C by. If b ¤ 0, EXTENDED-EUCLID ﬁrst computes .d 0; x0; y0/ such that d 0 D gcd.b; a mod b/ and d 0 D bx0 C .a mod b/y0 : (31.17) As for EUCLID, we have in this case d D gcd.a; b/ D d 0 D gcd.b; a mod b/. To obtain x and y such that d D ax C by, we start by rewriting equation (31.17) using the equation d D d 0 and equation (3.8): d D bx0 C .a  b ba=bc/y0 D ay0 C b.x0  ba=bc y0/ : Thus, choosing x D y0 and y D x0 ba=bc y0 satisﬁes the equation d D ax Cby, proving the correctness of EXTENDED-EUCLID.

Since the number of recursive calls made in EUCLID is equal to the number of recursive calls made in EXTENDED-EUCLID, the running times of EUCLID and EXTENDED-EUCLID are the same, to within a constant factor. That is, for a > b > 0, the number of recursive calls is O.lg b/.

## Exercises

31.2-1 Prove that equations (31.11) and (31.12) imply equation (31.13). 31.2-2 Compute the values .d; x; y/ that the call EXTENDED-EUCLID.899; 493/ returns. 31.2-3 Prove that for all integers a, k, and n, gcd.a; n/ D gcd.a C kn; n/ : 31.2-4 Rewrite EUCLID in an iterative form that uses only a constant amount of memory (that is, stores only a constant number of integer values). 31.2-5 If a > b  0, show that the call EUCLID.a; b/ makes at most 1 C log b recursive calls. Improve this bound to 1 C log.b= gcd.a; b//. 31.2-6 What does EXTENDED-EUCLID.FkC1; Fk/ return? Prove your answer correct.

## 31.3 Modular arithmetic

31.2-7 Deﬁne the gcd function for more than two arguments by the recursive equation gcd.a0; a1; : : : ; an/ D gcd.a0; gcd.a1; a2; : : : ; an//. Show that the gcd function returns the same answer independent of the order in which its arguments are speci- ﬁed. Also show how to ﬁnd integers x0; x1; : : : ; xn such that gcd.a0; a1; : : : ; an/ D a0x0 C a1x1 C    C anxn. Show that the number of divisions performed by your algorithm is O.n C lg.max fa0; a1; : : : ; ang//. 31.2-8 Deﬁne lcm.a1; a2; : : : ; an/ to be the least common multiple of the n integers a1; a2; : : : ; an, that is, the smallest nonnegative integer that is a multiple of each ai.

Show how to compute lcm.a1; a2; : : : ; an/ efﬁciently using the (two-argument) gcd operation as a subroutine. 31.2-9 Prove that n1, n2, n3, and n4 are pairwise relatively prime if and only if gcd.n1n2; n3n4/ D gcd.n1n3; n2n4/ D 1 :

More generally, show that n1; n2; : : : ; nk are pairwise relatively prime if and only if a set of dlg ke pairs of numbers derived from the ni are relatively prime.

## 31.3 Modular arithmetic

Informally, we can think of modular arithmetic as arithmetic as usual over the integers, except that if we are working modulo n, then every result x is replaced by the element of f0; 1; : : : ; n  1g that is equivalent to x, modulo n (that is, x is replaced by x mod n). This informal model sufﬁces if we stick to the operations of addition, subtraction, and multiplication. A more formal model for modular arithmetic, which we now give, is best described within the framework of group theory.

Finite groups A group .S; ˚/ is a set S together with a binary operation ˚ deﬁned on S for which the following properties hold: 1. Closure: For all a, b 2 S, we have a ˚ b 2 S. 2. Identity: There exists an element e 2 S, called the identity of the group, such that e ˚ a D a ˚ e D a for all a 2 S. 3. Associativity: For all a, b, c 2 S, we have .a ˚ b/ ˚ c D a ˚ .b ˚ c/.

4. Inverses: For each a 2 S, there exists a unique element b 2 S, called the inverse of a, such that a ˚ b D b ˚ a D e. As an example, consider the familiar group .Z; C/ of the integers Z under the operation of addition: 0 is the identity, and the inverse of a is a. If a group .S; ˚/ satisﬁes the commutative law a ˚ b D b ˚ a for all a; b 2 S, then it is an abelian group. If a group .S; ˚/ satisﬁes jSj < 1, then it is a ﬁnite group. The groups deﬁned by modular addition and multiplication We can form two ﬁnite abelian groups by using addition and multiplication modulo n, where n is a positive integer. These groups are based on the equivalence classes of the integers modulo n, deﬁned in Section 31.1. To deﬁne a group on Zn, we need to have suitable binary operations, which we obtain by redeﬁning the ordinary operations of addition and multiplication. We can easily deﬁne addition and multiplication operations for Zn, because the equivalence class of two integers uniquely determines the equivalence class of their sum or product. That is, if a  a0 .mod n/ and b  b0 .mod n/, then a C b  a0 C b0 .mod n/ ; ab  a0b0 .mod n/ : Thus, we deﬁne addition and multiplication modulo n, denoted Cn and n, by Œan Cn Œbn D Œa C bn ; (31.18) Œan n Œbn D Œabn : (We can deﬁne subtraction similarly on Zn by Œan n Œbn D Œa  bn, but division is more complicated, as we shall see.) These facts justify the common and convenient practice of using the smallest nonnegative element of each equivalence class as its representative when performing computations in Zn. We add, subtract, and multiply as usual on the representatives, but we replace each result x by the representative of its class, that is, by x mod n.

Using this deﬁnition of addition modulo n, we deﬁne the additive group modulo n as .Zn; Cn/. The size of the additive group modulo n is jZnj D n.

Figure 31.2(a) gives the operation table for the group .Z6; C6/.

> **Theorem 31.12**

The system .Zn; Cn/ is a ﬁnite abelian group.

Proof Equation (31.18) shows that .Zn; Cn/ is closed. Associativity and commutativity of Cn follow from the associativity and commutativity of C:

## 31.3 Modular arithmetic

(a) (b) +6 ·15 Figure 31.2 Two ﬁnite groups. Equivalence classes are denoted by their representative elements. (a) The group .Z6; C6/. (b) The group .Z 15; 15/. .Œan Cn Œbn/ Cn Œcn D Œa C bn Cn Œcn D Œ.a C b/ C cn D Œa C .b C c/n D Œan Cn Œb C cn D Œan Cn .Œbn Cn Œcn/ ; Œan Cn Œbn D Œa C bn D Œb C an D Œbn Cn Œan : The identity element of .Zn; Cn/ is 0 (that is, Œ0n). The (additive) inverse of an element a (that is, of Œan) is the element a (that is, Œan or Œn  an), since Œan Cn Œan D Œa  an D Œ0n.

Using the deﬁnition of multiplication modulo n, we deﬁne the multiplicative group modulo n as .Z n; n/. The elements of this group are the set Z n of elements in Zn that are relatively prime to n, so that each one has a unique inverse, modulo n:

Z n D fŒan 2 Zn W gcd.a; n/ D 1g : To see that Z n is well deﬁned, note that for 0  a < n, we have a  .a C kn/ .mod n/ for all integers k. By Exercise 31.2-3, therefore, gcd.a; n/ D 1 implies gcd.a C kn; n/ D 1 for all integers k. Since Œan D fa C kn W k 2 Zg, the set Z n is well deﬁned. An example of such a group is Z 15 D f1; 2; 4; 7; 8; 11; 13; 14g ;

where the group operation is multiplication modulo 15. (Here we denote an element Œa15 as a; for example, we denote Œ715 as 7.) Figure 31.2(b) shows the group .Z 15; 15/. For example, 8  11  13 .mod 15/, working in Z 15. The identity for this group is 1.

> **Theorem 31.13**

The system .Z n; n/ is a ﬁnite abelian group.

Proof

> **Theorem 31.6 implies that .Z**

n; n/ is closed. Associativity and commutativity can be proved for n as they were for Cn in the proof of Theorem 31.12. The identity element is Œ1n. To show the existence of inverses, let a be an element of Z n and let .d; x; y/ be returned by EXTENDED-EUCLID.a; n/. Then, d D 1, since a 2 Z n, and ax C ny D 1 (31.19) or, equivalently, ax  1 .mod n/ : Thus, Œxn is a multiplicative inverse of Œan, modulo n. Furthermore, we claim that Œxn 2 Z n. To see why, equation (31.19) demonstrates that the smallest positive linear combination of x and n must be 1. Therefore, Theorem 31.2 implies that gcd.x; n/ D 1. We defer the proof that inverses are uniquely deﬁned until

> **Corollary 31.26.**

As an example of computing multiplicative inverses, suppose that a D 5 and n D 11. Then EXTENDED-EUCLID.a; n/ returns .d; x; y/ D .1; 2; 1/, so that 1 D 5  .2/ C 11  1. Thus, Œ211 (i.e., Œ911) is the multiplicative inverse of Œ511.

When working with the groups .Zn; Cn/ and .Z n; n/ in the remainder of this chapter, we follow the convenient practice of denoting equivalence classes by their representative elements and denoting the operations Cn and n by the usual arithmetic notations C and  (or juxtaposition, so that ab D a  b) respectively. Also, equivalences modulo n may also be interpreted as equations in Zn. For example, the following two statements are equivalent: ax  b .mod n/ ; Œan n Œxn D Œbn : As a further convenience, we sometimes refer to a group .S; ˚/ merely as S when the operation ˚ is understood from context. We may thus refer to the groups .Zn; Cn/ and .Z n; n/ as Zn and Z n, respectively. We denote the (multiplicative) inverse of an element a by .a1 mod n/. Division in Z n is deﬁned by the equation a=b  ab1 .mod n/. For example, in Z

## 31.3 Modular arithmetic

we have that 71  13 .mod 15/, since 7  13 D 91  1 .mod 15/, so that 4=7  4  13  7 .mod 15/. The size of Z n is denoted .n/. This function, known as Euler’s phi function, satisﬁes the equation .n/ D n Y p W p is prime and p j n  1  1 p  ; (31.20) so that p runs over all the primes dividing n (including n itself, if n is prime). We shall not prove this formula here. Intuitively, we begin with a list of the n remainders f0; 1; : : : ; n  1g and then, for each prime p that divides n, cross out every multiple of p in the list. For example, since the prime divisors of 45 are 3 and 5, .45/ D  1  1   1  1  D 2  4  D 24 : If p is prime, then Z p D f1; 2; : : : ; p  1g, and .p/ D p  1  1 p  D p  1 : (31.21) If n is composite, then .n/ < n  1, although it can be shown that .n/ > n e ln ln n C ln ln n (31.22) for n  3, where D 0:5772156649 : : : is Euler’s constant. A somewhat simpler (but looser) lower bound for n > 5 is .n/ > n 6 ln ln n : (31.23) The lower bound (31.22) is essentially the best possible, since lim inf n!1 .n/ n= ln ln n D e : (31.24) Subgroups If .S; ˚/ is a group, S 0  S, and .S 0; ˚/ is also a group, then .S 0; ˚/ is a subgroup of .S; ˚/. For example, the even integers form a subgroup of the integers under the operation of addition. The following theorem provides a useful tool for recognizing subgroups.

> **Theorem 31.14 (A nonempty closed subset of a ﬁnite group is a subgroup)**

If .S; ˚/ is a ﬁnite group and S 0 is any nonempty subset of S such that a ˚ b 2 S 0 for all a; b 2 S 0, then .S 0; ˚/ is a subgroup of .S; ˚/.

Proof We leave the proof as Exercise 31.3-3.

For example, the set f0; 2; 4; 6g forms a subgroup of Z8, since it is nonempty and closed under the operation C (that is, it is closed under C8). The following theorem provides an extremely useful constraint on the size of a subgroup; we omit the proof.

> **Theorem 31.15 (Lagrange’s theorem)**

If .S; ˚/ is a ﬁnite group and .S 0; ˚/ is a subgroup of .S; ˚/, then jS 0j is a divisor of jSj.

A subgroup S 0 of a group S is a proper subgroup if S 0 ¤ S. We shall use the following corollary in our analysis in Section 31.8 of the Miller-Rabin primality test procedure.

> **Corollary 31.16**

If S 0 is a proper subgroup of a ﬁnite group S, then jS 0j  jSj =2.

Subgroups generated by an element

> **Theorem 31.14 gives us an easy way to produce a subgroup of a ﬁnite group .S; ˚/:**

choose an element a and take all elements that can be generated from a using the group operation. Speciﬁcally, deﬁne a.k/ for k  1 by a.k/ D k M iD1 a D a ˚ a ˚    ˚ a œ k :

For example, if we take a D 2 in the group Z6, the sequence a.1/; a.2/; a.3/; : : : is 2; 4; 0; 2; 4; 0; 2; 4; 0; : : : : In the group Zn, we have a.k/ D ka mod n, and in the group Z n, we have a.k/ D ak mod n. We deﬁne the subgroup generated by a, denoted hai or .hai; ˚/, by hai D fa.k/ W k  1g : We say that a generates the subgroup hai or that a is a generator of hai. Since S is ﬁnite, hai is a ﬁnite subset of S, possibly including all of S. Since the associativity of ˚ implies

## 31.3 Modular arithmetic

a.i/ ˚ a.j/ D a.iCj/ ; hai is closed and therefore, by Theorem 31.14, hai is a subgroup of S. For example, in Z6, we have h0i D f0g ; h1i D f0; 1; 2; 3; 4; 5g ; h2i D f0; 2; 4g :

Similarly, in Z 7, we have h1i D f1g ; h2i D f1; 2; 4g ; h3i D f1; 2; 3; 4; 5; 6g : The order of a (in the group S), denoted ord.a/, is deﬁned as the smallest positive integer t such that a.t/ D e.

> **Theorem 31.17**

For any ﬁnite group .S; ˚/ and any a 2 S, the order of a is equal to the size of the subgroup it generates, or ord.a/ D jhaij.

Proof Let t D ord.a/. Since a.t/ D e and a.tCk/ D a.t/ ˚ a.k/ D a.k/ for k  1, if i > t, then a.i/ D a.j/ for some j < i. Thus, as we generate elements by a, we see no new elements after a.t/. Thus, hai D fa.1/; a.2/; : : : ; a.t/g, and so jhaij  t. To show that jhaij  t, we show that each element of the sequence a.1/; a.2/; : : : ; a.t/ is distinct. Suppose for the purpose of contradiction that a.i/ D a.j/ for some i and j satisfying 1  i < j  t. Then, a.iCk/ D a.jCk/ for k  0. But this equality implies that a.iC.tj// D a.jC.tj// D e, a contradiction, since i C.t j / < t but t is the least positive value such that a.t/ D e. Therefore, each element of the sequence a.1/; a.2/; : : : ; a.t/ is distinct, and jhaij  t. We conclude that ord.a/ D jhaij.

> **Corollary 31.18**

The sequence a.1/; a.2/; : : : is periodic with period t D ord.a/; that is, a.i/ D a.j/ if and only if i  j .mod t/.

Consistent with the above corollary, we deﬁne a.0/ as e and a.i/ as a.i mod t/, where t D ord.a/, for all integers i.

> **Corollary 31.19**

If .S; ˚/ is a ﬁnite group with identity e, then for all a 2 S, a.jSj/ D e :

Proof Lagrange’s theorem (Theorem 31.15) implies that ord.a/ j jSj, and so jSj  0 .mod t/, where t D ord.a/. Therefore, a.jSj/ D a.0/ D e.

## Exercises

31.3-1 Draw the group operation tables for the groups .Z4; C4/ and .Z 5; 5/. Show that these groups are isomorphic by exhibiting a one-to-one correspondence ˛ between their elements such that a C b  c .mod 4/ if and only if ˛.a/  ˛.b/  ˛.c/ .mod 5/. 31.3-2 List all subgroups of Z9 and of Z 13. 31.3-3 Prove Theorem 31.14. 31.3-4 Show that if p is prime and e is a positive integer, then .pe/ D pe1.p  1/ : 31.3-5 Show that for any integer n > 1 and for any a 2 Z n, the function fa W Z n ! Z n deﬁned by fa.x/ D ax mod n is a permutation of Z n.

## 31.4 Solving modular linear equations

We now consider the problem of ﬁnding solutions to the equation ax  b .mod n/ ; (31.25) where a > 0 and n > 0. This problem has several applications; for example, we shall use it as part of the procedure for ﬁnding keys in the RSA public-key cryptosystem in Section 31.7. We assume that a, b, and n are given, and we wish to ﬁnd all values of x, modulo n, that satisfy equation (31.25). The equation may have zero, one, or more than one such solution.

Let hai denote the subgroup of Zn generated by a. Since hai D fa.x/ W x > 0g D fax mod n W x > 0g, equation (31.25) has a solution if and only if Œb 2 hai. Lagrange’s theorem (Theorem 31.15) tells us that jhaij must be a divisor of n. The following theorem gives us a precise characterization of hai.

## 31.4 Solving modular linear equations

> **Theorem 31.20**

For any positive integers a and n, if d D gcd.a; n/, then hai D hdi D f0; d; 2d; : : : ; ..n=d/  1/dg (31.26) in Zn, and thus jhaij D n=d :

Proof We begin by showing that d 2 hai. Recall that EXTENDED-EUCLID.a; n/ produces integers x0 and y0 such that ax0 C ny0 D d. Thus, ax0  d .mod n/, so that d 2 hai. In other words, d is a multiple of a in Zn.

Since d 2 hai, it follows that every multiple of d belongs to hai, because any multiple of a multiple of a is itself a multiple of a. Thus, hai contains every element in f0; d; 2d; : : : ; ..n=d/  1/dg. That is, hdi  hai. We now show that hai  hdi. If m 2 hai, then m D ax mod n for some integer x, and so m D ax C ny for some integer y. However, d j a and d j n, and so d j m by equation (31.4). Therefore, m 2 hdi.

Combining these results, we have that hai D hdi. To see that jhaij D n=d, observe that there are exactly n=d multiples of d between 0 and n1, inclusive.

> **Corollary 31.21**

The equation ax  b .mod n/ is solvable for the unknown x if and only if d j b, where d D gcd.a; n/.

Proof The equation ax  b .mod n/ is solvable if and only if Œb 2 hai, which is the same as saying .b mod n/ 2 f0; d; 2d; : : : ; ..n=d/  1/dg ; by Theorem 31.20. If 0  b < n, then b 2 hai if and only if d j b, since the members of hai are precisely the multiples of d. If b < 0 or b  n, the corollary then follows from the observation that d j b if and only if d j .b mod n/, since b and b mod n differ by a multiple of n, which is itself a multiple of d.

> **Corollary 31.22**

The equation ax  b .mod n/ either has d distinct solutions modulo n, where d D gcd.a; n/, or it has no solutions.

Proof If ax  b .mod n/ has a solution, then b 2 hai. By Theorem 31.17, ord.a/ D jhaij, and so Corollary 31.18 and Theorem 31.20 imply that the sequence ai mod n, for i D 0; 1; : : :, is periodic with period jhaij D n=d. If b 2 hai, then b appears exactly d times in the sequence ai mod n, for i D 0; 1; : : : ; n  1, since

the length-.n=d/ block of values hai repeats exactly d times as i increases from 0 to n1. The indices x of the d positions for which ax mod n D b are the solutions of the equation ax  b .mod n/.

> **Theorem 31.23**

Let d D gcd.a; n/, and suppose that d D ax0 C ny0 for some integers x0 and y0 (for example, as computed by EXTENDED-EUCLID). If d j b, then the equation ax  b .mod n/ has as one of its solutions the value x0, where x0 D x0.b=d/ mod n :

Proof We have ax0  ax0.b=d/ .mod n/  d.b=d/ .mod n/ (because ax0  d .mod n/)  b .mod n/ ; and thus x0 is a solution to ax  b .mod n/.

> **Theorem 31.24**

Suppose that the equation ax  b .mod n/ is solvable (that is, d j b, where d D gcd.a; n/) and that x0 is any solution to this equation. Then, this equation has exactly d distinct solutions, modulo n, given by xi D x0 C i.n=d/ for i D 0; 1; : : : ; d  1.

Proof Because n=d > 0 and 0  i.n=d/ < n for i D 0; 1; : : : ; d  1, the values x0; x1; : : : ; xd1 are all distinct, modulo n. Since x0 is a solution of ax  b .mod n/, we have ax0 mod n  b .mod n/. Thus, for i D 0; 1; : : : ; d  1, we have axi mod n D a.x0 C in=d/ mod n D .ax0 C ain=d/ mod n D ax0 mod n (because d j a implies that ain=d is a multiple of n)  b .mod n/ ; and hence axi  b .mod n/, making xi a solution, too. By Corollary 31.22, the equation ax  b .mod n/ has exactly d solutions, so that x0; x1; : : : ; xd1 must be all of them. We have now developed the mathematics needed to solve the equation ax  b .mod n/; the following algorithm prints all solutions to this equation. The inputs a and n are arbitrary positive integers, and b is an arbitrary integer.

## 31.4 Solving modular linear equations

MODULAR-LINEAR-EQUATION-SOLVER.a; b; n/ .d; x0; y0/ D EXTENDED-EUCLID.a; n/ if d j b x0 D x0.b=d/ mod n for i D 0 to d  1 print .x0 C i.n=d// mod n else print “no solutions” As an example of the operation of this procedure, consider the equation 14x  30 .mod 100/ (here, a D 14, b D 30, and n D 100). Calling EXTENDED- EUCLID in line 1, we obtain .d; x0; y0/ D .2; 7; 1/. Since 2 j 30, lines 3–5 execute. Line 3 computes x0 D .7/.15/ mod 100 D 95. The loop on lines 4–5 prints the two solutions 95 and 45. The procedure MODULAR-LINEAR-EQUATION-SOLVER works as follows.

Line 1 computes d D gcd.a; n/, along with two values x0 and y0 such that d D ax0 C ny0, demonstrating that x0 is a solution to the equation ax0  d .mod n/. If d does not divide b, then the equation ax  b .mod n/ has no solution, by

> **Corollary 31.21. Line 2 checks to see whether d j b; if not, line 6 reports that there**

are no solutions. Otherwise, line 3 computes a solution x0 to ax  b .mod n/, in accordance with Theorem 31.23. Given one solution, Theorem 31.24 states that adding multiples of .n=d/, modulo n, yields the other d  1 solutions. The for loop of lines 4–5 prints out all d solutions, beginning with x0 and spaced n=d apart, modulo n.

MODULAR-LINEAR-EQUATION-SOLVER performs O.lg n C gcd.a; n// arithmetic operations, since EXTENDED-EUCLID performs O.lg n/ arithmetic operations, and each iteration of the for loop of lines 4–5 performs a constant number of arithmetic operations. The following corollaries of Theorem 31.24 give specializations of particular interest.

> **Corollary 31.25**

For any n > 1, if gcd.a; n/ D 1, then the equation ax  b .mod n/ has a unique solution, modulo n. If b D 1, a common case of considerable interest, the x we are looking for is a multiplicative inverse of a, modulo n.

> **Corollary 31.26**

For any n > 1, if gcd.a; n/ D 1, then the equation ax  1 .mod n/ has a unique solution, modulo n. Otherwise, it has no solution.

Thanks to Corollary 31.26, we can use the notation a1 mod n to refer to the multiplicative inverse of a, modulo n, when a and n are relatively prime. If gcd.a; n/ D 1, then the unique solution to the equation ax  1 .mod n/ is the integer x returned by EXTENDED-EUCLID, since the equation gcd.a; n/ D 1 D ax C ny implies ax  1 .mod n/. Thus, we can compute a1 mod n efﬁciently using EXTENDED-EUCLID.

## Exercises

31.4-1 Find all solutions to the equation 35x  10 .mod 50/. 31.4-2 Prove that the equation ax  ay .mod n/ implies x  y .mod n/ whenever gcd.a; n/ D 1. Show that the condition gcd.a; n/ D 1 is necessary by supplying a counterexample with gcd.a; n/ > 1. 31.4-3 Consider the following change to line 3 of the procedure MODULAR-LINEAR- EQUATION-SOLVER: x0 D x0.b=d/ mod .n=d/ Will this work? Explain why or why not. 31.4-4 ?

Let p be prime and f .x/  f0 C f1x C    C ftxt .mod p/ be a polynomial of degree t, with coefﬁcients fi drawn from Zp. We say that a 2 Zp is a zero of f if f .a/  0 .mod p/.

Prove that if a is a zero of f , then f .x/  .x  a/g.x/ .mod p/ for some polynomial g.x/ of degree t  1. Prove by induction on t that if p is prime, then a polynomial f .x/ of degree t can have at most t distinct zeros modulo p.

## 31.5 The Chinese remainder theorem

Around A.D. 100, the Chinese mathematician Sun-Ts˘u solved the problem of ﬁnding those integers x that leave remainders 2, 3, and 2 when divided by 3, 5, and 7 respectively. One such solution is x D 23; all solutions are of the form 23 C 105k

## 31.5 The Chinese remainder theorem

for arbitrary integers k. The “Chinese remainder theorem” provides a correspondence between a system of equations modulo a set of pairwise relatively prime moduli (for example, 3, 5, and 7) and an equation modulo their product (for example, 105). The Chinese remainder theorem has two major applications.

Let the integer n be factored as n D n1n2    nk, where the factors ni are pairwise relatively prime. First, the Chinese remainder theorem is a descriptive “structure theorem” that describes the structure of Zn as identical to that of the Cartesian product Zn1 	 Zn2 	    	 Znk with componentwise addition and multiplication modulo ni in the ith component. Second, this description helps us to design efﬁcient algorithms, since working in each of the systems Zni can be more efﬁcient (in terms of bit operations) than working modulo n.

> **Theorem 31.27 (Chinese remainder theorem)**

Let n D n1n2    nk, where the ni are pairwise relatively prime. Consider the correspondence a $ .a1; a2; : : : ; ak/ ; (31.27) where a 2 Zn, ai 2 Zni, and ai D a mod ni for i D 1; 2; : : : ; k. Then, mapping (31.27) is a one-to-one correspondence (bijection) between Zn and the Cartesian product Zn1 	Zn2 	   	Znk. Operations performed on the elements of Zn can be equivalently performed on the corresponding k-tuples by performing the operations independently in each coordinate position in the appropriate system. That is, if a $ .a1; a2; : : : ; ak/ ; b $ .b1; b2; : : : ; bk/ ; then .a C b/ mod n $ ..a1 C b1/ mod n1; : : : ; .ak C bk/ mod nk/ ; (31.28) .a  b/ mod n $ ..a1  b1/ mod n1; : : : ; .ak  bk/ mod nk/ ; (31.29) .ab/ mod n $ .a1b1 mod n1; : : : ; akbk mod nk/ : (31.30) Proof Transforming between the two representations is fairly straightforward.

Going from a to .a1; a2; : : : ; ak/ is quite easy and requires only k “mod” operations.

Computing a from inputs .a1; a2; : : : ; ak/ is a bit more complicated. We begin by deﬁning mi D n=ni for i D 1; 2; : : : ; k; thus mi is the product of all of the nj’s other than ni: mi D n1n2    ni1niC1    nk. We next deﬁne

ci D mi.m1 i mod ni/ (31.31) for i D 1; 2; : : : ; k. Equation (31.31) is always well deﬁned: since mi and ni are relatively prime (by Theorem 31.6), Corollary 31.26 guarantees that m1 i mod ni exists. Finally, we can compute a as a function of a1, a2, . . . , ak as follows: a  .a1c1 C a2c2 C    C akck/ .mod n/ : (31.32) We now show that equation (31.32) ensures that a  ai .mod ni/ for i D 1; 2; : : : ; k. Note that if j ¤ i, then mj  0 .mod ni/, which implies that cj  mj  0 .mod ni/. Note also that ci  1 .mod ni/, from equation (31.31). We thus have the appealing and useful correspondence ci $ .0; 0; : : : ; 0; 1; 0; : : : ; 0/ ; a vector that has 0s everywhere except in the ith coordinate, where it has a 1; the ci thus form a “basis” for the representation, in a certain sense. For each i, therefore, we have a  aici .mod ni/  aimi.m1 i mod ni/ .mod ni/  ai .mod ni/ ; which is what we wished to show: our method of computing a from the ai’s produces a result a that satisﬁes the constraints a  ai .mod ni/ for i D 1; 2; : : : ; k. The correspondence is one-to-one, since we can transform in both directions.

Finally, equations (31.28)–(31.30) follow directly from Exercise 31.1-7, since x mod ni D .x mod n/ mod ni for any x and i D 1; 2; : : : ; k. We shall use the following corollaries later in this chapter.

> **Corollary 31.28**

If n1; n2; : : : ; nk are pairwise relatively prime and n D n1n2    nk, then for any integers a1; a2; : : : ; ak, the set of simultaneous equations x  ai .mod ni/ ; for i D 1; 2; : : : ; k, has a unique solution modulo n for the unknown x.

> **Corollary 31.29**

If n1; n2; : : : ; nk are pairwise relatively prime and n D n1n2    nk, then for all integers x and a, x  a .mod ni/ for i D 1; 2; : : : ; k if and only if x  a .mod n/ :

## 31.5 The Chinese remainder theorem

Figure 31.3 An illustration of the Chinese remainder theorem for n1 D 5 and n2 D 13. For this example, c1 D 26 and c2 D 40. In row i, column j is shown the value of a, modulo 65, such that a mod 5 D i and a mod 13 D j. Note that row 0, column 0 contains a 0. Similarly, row 4, column 12 contains a 64 (equivalent to 1). Since c1 D 26, moving down a row increases a by 26.

Similarly, c2 D 40 means that moving right by a column increases a by 40. Increasing a by 1 corresponds to moving diagonally downward and to the right, wrapping around from the bottom to the top and from the right to the left. As an example of the application of the Chinese remainder theorem, suppose we are given the two equations a  2 .mod 5/ ; a  3 .mod 13/ ; so that a1 D 2, n1 D m2 D 5, a2 D 3, and n2 D m1 D 13, and we wish to compute a mod 65, since n D n1n2 D 65. Because 131  2 .mod 5/ and 51  8 .mod 13/, we have c1 D 13.2 mod 5/ D 26 ; c2 D 5.8 mod 13/ D 40 ; and a  2  26 C 3  40 .mod 65/  52 C 120 .mod 65/  .mod 65/ :

See Figure 31.3 for an illustration of the Chinese remainder theorem, modulo 65. Thus, we can work modulo n by working modulo n directly or by working in the transformed representation using separate modulo ni computations, as convenient. The computations are entirely equivalent.

## Exercises

31.5-1 Find all solutions to the equations x  4 .mod 5/ and x  5 .mod 11/.

31.5-2 Find all integers x that leave remainders 1, 2, 3 when divided by 9, 8, 7 respectively. 31.5-3 Argue that, under the deﬁnitions of Theorem 31.27, if gcd.a; n/ D 1, then .a1 mod n/ $ ..a1 mod n1/; .a1 mod n2/; : : : ; .a1 k mod nk// : 31.5-4 Under the deﬁnitions of Theorem 31.27, prove that for any polynomial f , the number of roots of the equation f .x/  0 .mod n/ equals the product of the number of roots of each of the equations f .x/  0 .mod n1/, f .x/  0 .mod n2/, . . . , f .x/  0 .mod nk/.

## 31.6 Powers of an element

Just as we often consider the multiples of a given element a, modulo n, we consider the sequence of powers of a, modulo n, where a 2 Z n: a0; a1; a2; a3; : : : ; (31.33) modulo n. Indexing from 0, the 0th value in this sequence is a0 mod n D 1, and the ith value is ai mod n. For example, the powers of 3 modulo 7 are i 3i mod 7 whereas the powers of 2 modulo 7 are i 2i mod 7 In this section, let hai denote the subgroup of Z n generated by a by repeated multiplication, and let ordn.a/ (the “order of a, modulo n”) denote the order of a in Z n. For example, h2i D f1; 2; 4g in Z 7, and ord7.2/ D 3. Using the deﬁnition of the Euler phi function .n/ as the size of Z n (see Section 31.3), we now translate

> **Corollary 31.19 into the notation of Z**

n to obtain Euler’s theorem and specialize it to Z p, where p is prime, to obtain Fermat’s theorem.

> **Theorem 31.30 (Euler’s theorem)**

For any integer n > 1, a.n/  1 .mod n/ for all a 2 Z n :

## 31.6 Powers of an element

> **Theorem 31.31 (Fermat’s theorem)**

If p is prime, then ap1  1 .mod p/ for all a 2 Z p :

Proof By equation (31.21), .p/ D p  1 if p is prime.

Fermat’s theorem applies to every element in Zp except 0, since 0 62 Z p. For all a 2 Zp, however, we have ap  a .mod p/ if p is prime. If ordn.g/ D jZ nj, then every element in Z n is a power of g, modulo n, and g is a primitive root or a generator of Z n. For example, 3 is a primitive root, modulo 7, but 2 is not a primitive root, modulo 7. If Z n possesses a primitive root, the group Z n is cyclic. We omit the proof of the following theorem, which is proven by Niven and Zuckerman [265].

> **Theorem 31.32**

The values of n > 1 for which Z n is cyclic are 2, 4, pe, and 2pe, for all primes p > 2 and all positive integers e. If g is a primitive root of Z n and a is any element of Z n, then there exists a ´ such that g´  a .mod n/. This ´ is a discrete logarithm or an index of a, modulo n, to the base g; we denote this value as indn;g.a/.

> **Theorem 31.33 (Discrete logarithm theorem)**

If g is a primitive root of Z n, then the equation gx  gy .mod n/ holds if and only if the equation x  y .mod .n// holds.

Proof Suppose ﬁrst that x  y .mod .n//. Then, x D y C k.n/ for some integer k. Therefore, gx  gyCk.n/ .mod n/  gy  .g.n//k .mod n/  gy  1k .mod n/ (by Euler’s theorem)  gy .mod n/ :

Conversely, suppose that gx  gy .mod n/. Because the sequence of powers of g generates every element of hgi and jhgij D .n/, Corollary 31.18 implies that the sequence of powers of g is periodic with period .n/. Therefore, if gx  gy .mod n/, then we must have x  y .mod .n//. We now turn our attention to the square roots of 1, modulo a prime power. The following theorem will be useful in our development of a primality-testing algorithm in Section 31.8.

> **Theorem 31.34**

If p is an odd prime and e  1, then the equation x2  1 .mod pe/ (31.34) has only two solutions, namely x D 1 and x D 1.

Proof Equation (31.34) is equivalent to pe j .x  1/.x C 1/ :

Since p > 2, we can have p j .x  1/ or p j .x C 1/, but not both. (Otherwise, by property (31.3), p would also divide their difference .x C 1/  .x  1/ D 2.) If p −.x  1/, then gcd.pe; x  1/ D 1, and by Corollary 31.5, we would have pe j .x C 1/. That is, x  1 .mod pe/. Symmetrically, if p −.x C 1/, then gcd.pe; x C 1/ D 1, and Corollary 31.5 implies that pe j .x  1/, so that x  1 .mod pe/. Therefore, either x  1 .mod pe/ or x  1 .mod pe/.

A number x is a nontrivial square root of 1, modulo n, if it satisﬁes the equation x2  1 .mod n/ but x is equivalent to neither of the two “trivial” square roots: 1 or 1, modulo n. For example, 6 is a nontrivial square root of 1, modulo 35. We shall use the following corollary to Theorem 31.34 in the correctness proof in Section 31.8 for the Miller-Rabin primality-testing procedure.

> **Corollary 31.35**

If there exists a nontrivial square root of 1, modulo n, then n is composite.

Proof By the contrapositive of Theorem 31.34, if there exists a nontrivial square root of 1, modulo n, then n cannot be an odd prime or a power of an odd prime. If x2  1 .mod 2/, then x  1 .mod 2/, and so all square roots of 1, modulo 2, are trivial. Thus, n cannot be prime. Finally, we must have n > 1 for a nontrivial square root of 1 to exist. Therefore, n must be composite.

Raising to powers with repeated squaring A frequently occurring operation in number-theoretic computations is raising one number to a power modulo another number, also known as modular exponentiation. More precisely, we would like an efﬁcient way to compute ab mod n, where a and b are nonnegative integers and n is a positive integer. Modular exponentiation is an essential operation in many primality-testing routines and in the RSA public-key cryptosystem. The method of repeated squaring solves this problem efﬁciently using the binary representation of b.

Let hbk; bk1; : : : ; b1; b0i be the binary representation of b. (That is, the binary representation is k C 1 bits long, bk is the most signiﬁcant bit, and b0 is the least

## 31.6 Powers of an element

i bi c d Figure 31.4 The results of MODULAR-EXPONENTIATION when computing ab .mod n/, where a D 7, b D 560 D h1000110000i, and n D 561. The values are shown after each execution of the for loop. The ﬁnal result is 1. signiﬁcant bit.) The following procedure computes ac mod n as c is increased by doublings and incrementations from 0 to b.

MODULAR-EXPONENTIATION.a; b; n/ c D 0 d D 1 let hbk; bk1; : : : ; b0i be the binary representation of b for i D k downto 0 c D 2c d D .d  d/ mod n if bi == 1 c D c C 1 d D .d  a/ mod n return d The essential use of squaring in line 6 of each iteration explains the name “repeated squaring.” As an example, for a D 7, b D 560, and n D 561, the algorithm computes the sequence of values modulo 561 shown in Figure 31.4; the sequence of exponents used appears in the row of the table labeled by c. The variable c is not really needed by the algorithm but is included for the following two-part loop invariant:

Just prior to each iteration of the for loop of lines 4–9, 1. The value of c is the same as the preﬁx hbk;bk1;: : : ;biC1i of the binary representation of b, and 2. d D ac mod n. We use this loop invariant as follows: Initialization: Initially, i D k, so that the preﬁx hbk; bk1; : : : ; biC1i is empty, which corresponds to c D 0. Moreover, d D 1 D a0 mod n.

Maintenance: Let c0 and d 0 denote the values of c and d at the end of an iteration of the for loop, and thus the values prior to the next iteration. Each iteration updates c0 D 2c (if bi D 0) or c0 D 2c C1 (if bi D 1), so that c will be correct prior to the next iteration. If bi D 0, then d 0 D d 2 mod n D .ac/2 mod n D a2c mod n D ac0 mod n. If bi D 1, then d 0 D d 2a mod n D .ac/2a mod n D a2cC1 mod n D ac0 mod n. In either case, d D ac mod n prior to the next iteration.

Termination: At termination, i D 1. Thus, c D b, since c has the value of the preﬁx hbk; bk1; : : : ; b0i of b’s binary representation. Hence d D ac mod n D ab mod n. If the inputs a, b, and n are ˇ-bit numbers, then the total number of arithmetic operations required is O.ˇ/ and the total number of bit operations required is O.ˇ3/.

## Exercises

31.6-1 Draw a table showing the order of every element in Z 11. Pick the smallest primitive root g and compute a table giving ind11;g.x/ for all x 2 Z 11. 31.6-2 Give a modular exponentiation algorithm that examines the bits of b from right to left instead of left to right. 31.6-3 Assuming that you know .n/, explain how to compute a1 mod n for any a 2 Z n using the procedure MODULAR-EXPONENTIATION.

## 31.7 The RSA public-key cryptosystem

With a public-key cryptosystem, we can encrypt messages sent between two communicating parties so that an eavesdropper who overhears the encrypted messages will not be able to decode them. A public-key cryptosystem also enables a party to append an unforgeable “digital signature” to the end of an electronic message.

Such a signature is the electronic version of a handwritten signature on a paper document. It can be easily checked by anyone, forged by no one, yet loses its validity if any bit of the message is altered. It therefore provides authentication of both the identity of the signer and the contents of the signed message. It is the perfect tool

## 31.7 The RSA public-key cryptosystem

for electronically signed business contracts, electronic checks, electronic purchase orders, and other electronic communications that parties wish to authenticate. The RSA public-key cryptosystem relies on the dramatic difference between the ease of ﬁnding large prime numbers and the difﬁculty of factoring the product of two large prime numbers. Section 31.8 describes an efﬁcient procedure for ﬁnding large prime numbers, and Section 31.9 discusses the problem of factoring large integers.

Public-key cryptosystems In a public-key cryptosystem, each participant has both a public key and a secret key. Each key is a piece of information. For example, in the RSA cryptosystem, each key consists of a pair of integers. The participants “Alice” and “Bob” are traditionally used in cryptography examples; we denote their public and secret keys as PA, SA for Alice and PB, SB for Bob.

Each participant creates his or her own public and secret keys. Secret keys are kept secret, but public keys can be revealed to anyone or even published. In fact, it is often convenient to assume that everyone’s public key is available in a public directory, so that any participant can easily obtain the public key of any other participant. The public and secret keys specify functions that can be applied to any message.

Let D denote the set of permissible messages. For example, D might be the set of all ﬁnite-length bit sequences. In the simplest, and original, formulation of publickey cryptography, we require that the public and secret keys specify one-to-one functions from D to itself. We denote the function corresponding to Alice’s public key PA by PA./ and the function corresponding to her secret key SA by SA./. The functions PA./ and SA./ are thus permutations of D. We assume that the functions PA./ and SA./ are efﬁciently computable given the corresponding key PA or SA. The public and secret keys for any participant are a “matched pair” in that they specify functions that are inverses of each other. That is, M D SA.PA.M// ; (31.35) M D PA.SA.M// (31.36) for any message M 2 D. Transforming M with the two keys PA and SA successively, in either order, yields the message M back. In a public-key cryptosystem, we require that no one but Alice be able to compute the function SA./ in any practical amount of time. This assumption is crucial to keeping encrypted mail sent to Alice private and to knowing that Alice’s digital signatures are authentic. Alice must keep SA secret; if she does not, she loses her uniqueness and the cryptosystem cannot provide her with unique capabilities. The assumption that only Alice can compute SA./ must hold even though everyone

decrypt communication channel encrypt Bob Alice eavesdropper M M PA SA C C D PA.M/ Figure 31.5 Encryption in a public key system. Bob encrypts the message M using Alice’s public key PA and transmits the resulting ciphertext C D PA.M/ over a communication channel to Alice. An eavesdropper who captures the transmitted ciphertext gains no information about M. Alice receives C and decrypts it using her secret key to obtain the original message M D SA.C/. knows PA and can compute PA./, the inverse function to SA./, efﬁciently. In order to design a workable public-key cryptosystem, we must ﬁgure out how to create a system in which we can reveal a transformation PA./ without thereby revealing how to compute the corresponding inverse transformation SA./. This task appears formidable, but we shall see how to accomplish it. In a public-key cryptosystem, encryption works as shown in Figure 31.5. Suppose Bob wishes to send Alice a message M encrypted so that it will look like unintelligible gibberish to an eavesdropper. The scenario for sending the message goes as follows.  Bob obtains Alice’s public key PA (from a public directory or directly from Alice).  Bob computes the ciphertext C D PA.M/ corresponding to the message M and sends C to Alice.  When Alice receives the ciphertext C, she applies her secret key SA to retrieve the original message: SA.C/ D SA.PA.M// D M.

Because SA./ and PA./ are inverse functions, Alice can compute M from C. Because only Alice is able to compute SA./, Alice is the only one who can compute M from C. Because Bob encrypts M using PA./, only Alice can understand the transmitted message. We can just as easily implement digital signatures within our formulation of a public-key cryptosystem. (There are other ways of approaching the problem of constructing digital signatures, but we shall not go into them here.) Suppose now that Alice wishes to send Bob a digitally signed response M 0. Figure 31.6 shows how the digital-signature scenario proceeds.  Alice computes her digital signature 	 for the message M 0 using her secret key SA and the equation 	 D SA.M 0/.

## 31.7 The RSA public-key cryptosystem

sign communication channel verify =? accept Bob Alice M 0 M 0 PA SA

.M 0; 	/ D SA.M 0/ Figure 31.6 Digital signatures in a public-key system. Alice signs the message M 0 by appending her digital signature 	 D SA.M 0/ to it. She transmits the message/signature pair .M 0; 	/ to Bob, who veriﬁes it by checking the equation M 0 D PA.	/. If the equation holds, he accepts .M 0; 	/ as a message that Alice has signed.  Alice sends the message/signature pair .M 0; 	/ to Bob.  When Bob receives .M 0; 	/, he can verify that it originated from Alice by using Alice’s public key to verify the equation M 0 D PA.	/. (Presumably, M 0 contains Alice’s name, so Bob knows whose public key to use.) If the equation holds, then Bob concludes that the message M 0 was actually signed by Alice. If the equation fails to hold, Bob concludes either that the message M 0 or the digital signature 	 was corrupted by transmission errors or that the pair .M 0; 	/ is an attempted forgery.

Because a digital signature provides both authentication of the signer’s identity and authentication of the contents of the signed message, it is analogous to a handwritten signature at the end of a written document.

A digital signature must be veriﬁable by anyone who has access to the signer’s public key. A signed message can be veriﬁed by one party and then passed on to other parties who can also verify the signature. For example, the message might be an electronic check from Alice to Bob. After Bob veriﬁes Alice’s signature on the check, he can give the check to his bank, who can then also verify the signature and effect the appropriate funds transfer.

A signed message is not necessarily encrypted; the message can be “in the clear” and not protected from disclosure. By composing the above protocols for encryption and for signatures, we can create messages that are both signed and encrypted. The signer ﬁrst appends his or her digital signature to the message and then encrypts the resulting message/signature pair with the public key of the intended recipient. The recipient decrypts the received message with his or her secret key to obtain both the original message and its digital signature. The recipient can then verify the signature using the public key of the signer. The corresponding combined process using paper-based systems would be to sign the paper document and

then seal the document inside a paper envelope that is opened only by the intended recipient. The RSA cryptosystem In the RSA public-key cryptosystem, a participant creates his or her public and secret keys with the following procedure: 1. Select at random two large prime numbers p and q such that p ¤ q. The primes p and q might be, say, 1024 bits each. 2. Compute n D pq. 3. Select a small odd integer e that is relatively prime to .n/, which, by equation (31.20), equals .p  1/.q  1/. 4. Compute d as the multiplicative inverse of e, modulo .n/. (Corollary 31.26 guarantees that d exists and is uniquely deﬁned. We can use the technique of Section 31.4 to compute d, given e and .n/.) 5. Publish the pair P D .e; n/ as the participant’s RSA public key. 6. Keep secret the pair S D .d; n/ as the participant’s RSA secret key.

For this scheme, the domain D is the set Zn. To transform a message M associated with a public key P D .e; n/, compute P.M/ D M e mod n : (31.37) To transform a ciphertext C associated with a secret key S D .d; n/, compute S.C/ D C d mod n : (31.38) These equations apply to both encryption and signatures. To create a signature, the signer applies his or her secret key to the message to be signed, rather than to a ciphertext. To verify a signature, the public key of the signer is applied to it, rather than to a message to be encrypted. We can implement the public-key and secret-key operations using the procedure MODULAR-EXPONENTIATION described in Section 31.6. To analyze the running time of these operations, assume that the public key .e; n/ and secret key .d; n/ satisfy lg e D O.1/, lg d  ˇ, and lg n  ˇ. Then, applying a public key requires O.1/ modular multiplications and uses O.ˇ2/ bit operations. Applying a secret key requires O.ˇ/ modular multiplications, using O.ˇ3/ bit operations.

> **Theorem 31.36 (Correctness of RSA)**

The RSA equations (31.37) and (31.38) deﬁne inverse transformations of Zn satisfying equations (31.35) and (31.36).

## 31.7 The RSA public-key cryptosystem

Proof From equations (31.37) and (31.38), we have that for any M 2 Zn, P.S.M// D S.P.M// D M ed .mod n/ :

Since e and d are multiplicative inverses modulo .n/ D .p  1/.q  1/, ed D 1 C k.p  1/.q  1/ for some integer k. But then, if M 6 0 .mod p/, we have M ed  M.M p1/k.q1/ .mod p/  M..M mod p/p1/k.q1/ .mod p/  M.1/k.q1/ .mod p/ (by Theorem 31.31)  M .mod p/ :

Also, M ed  M .mod p/ if M  0 .mod p/. Thus, M ed  M .mod p/ for all M. Similarly, M ed  M .mod q/ for all M. Thus, by Corollary 31.29 to the Chinese remainder theorem, M ed  M .mod n/ for all M. The security of the RSA cryptosystem rests in large part on the difﬁculty of factoring large integers. If an adversary can factor the modulus n in a public key, then the adversary can derive the secret key from the public key, using the knowledge of the factors p and q in the same way that the creator of the public key used them. Therefore, if factoring large integers is easy, then breaking the RSA cryptosystem is easy. The converse statement, that if factoring large integers is hard, then breaking RSA is hard, is unproven. After two decades of research, however, no easier method has been found to break the RSA public-key cryptosystem than to factor the modulus n. And as we shall see in Section 31.9, factoring large integers is surprisingly difﬁcult. By randomly selecting and multiplying together two 1024-bit primes, we can create a public key that cannot be “broken” in any feasible amount of time with current technology. In the absence of a fundamental breakthrough in the design of number-theoretic algorithms, and when implemented with care following recommended standards, the RSA cryptosystem is capable of providing a high degree of security in applications. In order to achieve security with the RSA cryptosystem, however, we should use integers that are quite long—hundreds or even more than one thousand bits

long—to resist possible advances in the art of factoring.

At the time of this writing (2009), RSA moduli were commonly in the range of 768 to 2048 bits. To create moduli of such sizes, we must be able to ﬁnd large primes efﬁciently.

Section 31.8 addresses this problem.

For efﬁciency, RSA is often used in a “hybrid” or “key-management” mode with fast non-public-key cryptosystems. With such a system, the encryption and decryption keys are identical. If Alice wishes to send a long message M to Bob privately, she selects a random key K for the fast non-public-key cryptosystem and encrypts M using K, obtaining ciphertext C. Here, C is as long as M, but K is quite short. Then, she encrypts K using Bob’s public RSA key. Since K is short, computing PB.K/ is fast (much faster than computing PB.M/). She then transmits .C; PB.K// to Bob, who decrypts PB.K/ to obtain K and then uses K to decrypt C, obtaining M. We can use a similar hybrid approach to make digital signatures efﬁciently. This approach combines RSA with a public collision-resistant hash function h—a function that is easy to compute but for which it is computationally infeasible to ﬁnd two messages M and M 0 such that h.M/ D h.M 0/. The value h.M/ is a short (say, 256-bit) “ﬁngerprint” of the message M. If Alice wishes to sign a message M, she ﬁrst applies h to M to obtain the ﬁngerprint h.M/, which she then encrypts with her secret key. She sends .M; SA.h.M/// to Bob as her signed version of M. Bob can verify the signature by computing h.M/ and verifying that PA applied to SA.h.M// as received equals h.M/. Because no one can create two messages with the same ﬁngerprint, it is computationally infeasible to alter a signed message and preserve the validity of the signature.

Finally, we note that the use of certiﬁcates makes distributing public keys much easier. For example, assume there is a “trusted authority” T whose public key is known by everyone. Alice can obtain from T a signed message (her certiﬁcate) stating that “Alice’s public key is PA.” This certiﬁcate is “self-authenticating” since everyone knows PT . Alice can include her certiﬁcate with her signed messages, so that the recipient has Alice’s public key immediately available in order to verify her signature. Because her key was signed by T , the recipient knows that Alice’s key is really Alice’s.

## Exercises

31.7-1 Consider an RSA key set with p D 11, q D 29, n D 319, and e D 3. What value of d should be used in the secret key? What is the encryption of the message M D 100?

## 31.8 Primality testing

31.7-2 Prove that if Alice’s public exponent e is 3 and an adversary obtains Alice’s secret exponent d, where 0 < d < .n/, then the adversary can factor Alice’s modulus n in time polynomial in the number of bits in n. (Although you are not asked to prove it, you may be interested to know that this result remains true even if the condition e D 3 is removed. See Miller [255].) 31.7-3 ?

Prove that RSA is multiplicative in the sense that PA.M1/PA.M2/  PA.M1M2/ .mod n/ :

Use this fact to prove that if an adversary had a procedure that could efﬁciently decrypt 1 percent of messages from Zn encrypted with PA, then he could employ a probabilistic algorithm to decrypt every message encrypted with PA with high probability. ?

## 31.8 Primality testing

In this section, we consider the problem of ﬁnding large primes. We begin with a discussion of the density of primes, proceed to examine a plausible, but incomplete, approach to primality testing, and then present an effective randomized primality test due to Miller and Rabin. The density of prime numbers For many applications, such as cryptography, we need to ﬁnd large “random” primes. Fortunately, large primes are not too rare, so that it is feasible to test random integers of the appropriate size until we ﬁnd a prime. The prime distribution function .n/ speciﬁes the number of primes that are less than or equal to n.

For example, .10/ D 4, since there are 4 prime numbers less than or equal to 10, namely, 2, 3, 5, and 7. The prime number theorem gives a useful approximation to .n/.

> **Theorem 31.37 (Prime number theorem)**

lim n!1 .n/ n= ln n D 1 : The approximation n= ln n gives reasonably accurate estimates of .n/ even for small n. For example, it is off by less than 6% at n D 109, where .n/ D

50,847,534 and n= ln n  48,254,942. (To a number theorist, 109 is a small number.) We can view the process of randomly selecting an integer n and determining whether it is prime as a Bernoulli trial (see Section C.4). By the prime number theorem, the probability of a success—that is, the probability that n is prime—is approximately 1= ln n. The geometric distribution tells us how many trials we need to obtain a success, and by equation (C.32), the expected number of trials is approximately ln n. Thus, we would expect to examine approximately ln n integers chosen randomly near n in order to ﬁnd a prime that is of the same length as n.

For example, we expect that ﬁnding a 1024-bit prime would require testing approximately ln 21024  710 randomly chosen 1024-bit numbers for primality. (Of course, we can cut this ﬁgure in half by choosing only odd integers.) In the remainder of this section, we consider the problem of determining whether or not a large odd integer n is prime. For notational convenience, we assume that n has the prime factorization n D pe1 1 pe2 2    per r ; (31.39) where r  1, p1; p2; : : : ; pr are the prime factors of n, and e1; e2; : : : ; er are positive integers. The integer n is prime if and only if r D 1 and e1 D 1. One simple approach to the problem of testing for primality is trial division. We try dividing n by each integer 2; 3; : : : ; bpnc. (Again, we may skip even integers greater than 2.) It is easy to see that n is prime if and only if none of the trial divisors divides n. Assuming that each trial division takes constant time, the worst-case running time is ‚.pn/, which is exponential in the length of n. (Recall that if n is encoded in binary using ˇ bits, then ˇ D dlg.n C 1/e, and so pn D ‚.2ˇ=2/.) Thus, trial division works well only if n is very small or happens to have a small prime factor. When it works, trial division has the advantage that it not only determines whether n is prime or composite, but also determines one of n’s prime factors if n is composite. In this section, we are interested only in ﬁnding out whether a given number n is prime; if n is composite, we are not concerned with ﬁnding its prime factorization. As we shall see in Section 31.9, computing the prime factorization of a number is computationally expensive. It is perhaps surprising that it is much easier to tell whether or not a given number is prime than it is to determine the prime factorization of the number if it is not prime.

Pseudoprimality testing We now consider a method for primality testing that “almost works” and in fact is good enough for many practical applications. Later on, we shall present a re-

## 31.8 Primality testing

ﬁnement of this method that removes the small defect. Let ZC n denote the nonzero elements of Zn:

ZC n D f1; 2; : : : ; n  1g : If n is prime, then ZC n D Z n. We say that n is a base-a pseudoprime if n is composite and an1  1 .mod n/ : (31.40) Fermat’s theorem (Theorem 31.31) implies that if n is prime, then n satisﬁes equation (31.40) for every a in ZC n . Thus, if we can ﬁnd any a 2 ZC n such that n does not satisfy equation (31.40), then n is certainly composite. Surprisingly, the converse almost holds, so that this criterion forms an almost perfect test for primality. We test to see whether n satisﬁes equation (31.40) for a D 2. If not, we declare n to be composite by returning COMPOSITE. Otherwise, we return PRIME, guessing that n is prime (when, in fact, all we know is that n is either prime or a base-2 pseudoprime). The following procedure pretends in this manner to be checking the primality of n. It uses the procedure MODULAR-EXPONENTIATION from Section 31.6. We assume that the input n is an odd integer greater than 2.

PSEUDOPRIME.n/ if MODULAR-EXPONENTIATION.2; n  1; n/ 6 1 .mod n/ return COMPOSITE // deﬁnitely else return PRIME // we hope! This procedure can make errors, but only of one type. That is, if it says that n is composite, then it is always correct. If it says that n is prime, however, then it makes an error only if n is a base-2 pseudoprime.

How often does this procedure err? Surprisingly rarely. There are only 22 values of n less than 10,000 for which it errs; the ﬁrst four such values are 341, 561, 645, and 1105. We won’t prove it, but the probability that this program makes an error on a randomly chosen ˇ-bit number goes to zero as ˇ ! 1. Using more precise estimates due to Pomerance [279] of the number of base-2 pseudoprimes of a given size, we may estimate that a randomly chosen 512-bit number that is called prime by the above procedure has less than one chance in 1020 of being a base-2 pseudoprime, and a randomly chosen 1024-bit number that is called prime has less than one chance in 1041 of being a base-2 pseudoprime. So if you are merely trying to ﬁnd a large prime for some application, for all practical purposes you almost never go wrong by choosing large numbers at random until one of them causes PSEUDOPRIME to return PRIME. But when the numbers being tested for primality are not randomly chosen, we need a better approach for testing primality.

As we shall see, a little more cleverness, and some randomization, will yield a primality-testing routine that works well on all inputs.

Unfortunately, we cannot entirely eliminate all the errors by simply checking equation (31.40) for a second base number, say a D 3, because there exist composite integers n, known as Carmichael numbers, that satisfy equation (31.40) for all a 2 Z n. (We note that equation (31.40) does fail when gcd.a; n/ > 1—that is, when a 62 Z n—but hoping to demonstrate that n is composite by ﬁnding such an a can be difﬁcult if n has only large prime factors.) The ﬁrst three Carmichael numbers are 561, 1105, and 1729. Carmichael numbers are extremely rare; there are, for example, only 255 of them less than 100,000,000. Exercise 31.8-2 helps explain why they are so rare. We next show how to improve our primality test so that it won’t be fooled by Carmichael numbers. The Miller-Rabin randomized primality test The Miller-Rabin primality test overcomes the problems of the simple test PSEU- DOPRIME with two modiﬁcations:  It tries several randomly chosen base values a instead of just one base value.  While computing each modular exponentiation, it looks for a nontrivial square root of 1, modulo n, during the ﬁnal set of squarings. If it ﬁnds one, it stops and returns COMPOSITE. Corollary 31.35 from Section 31.6 justiﬁes detecting composites in this manner. The pseudocode for the Miller-Rabin primality test follows. The input n > 2 is the odd number to be tested for primality, and s is the number of randomly chosen base values from ZC n to be tried. The code uses the random-number generator RANDOM described on page 117: RANDOM.1; n  1/ returns a randomly chosen integer a satisfying 1  a  n1. The code uses an auxiliary procedure WITNESS such that WITNESS.a; n/ is TRUE if and only if a is a “witness” to the compositeness of n—that is, if it is possible using a to prove (in a manner that we shall see) that n is composite. The test WITNESS.a; n/ is an extension of, but more effective than, the test an1 6 1 .mod n/ that formed the basis (using a D 2) for PSEUDOPRIME. We ﬁrst present and justify the construction of WITNESS, and then we shall show how we use it in the Miller-Rabin primality test. Let n  1 D 2tu where t  1 and u is odd; i.e., the binary representation of n  1 is the binary representation of the odd integer u followed by exactly t zeros. Therefore, an1  .au/2t .mod n/, so that we can

## 31.8 Primality testing

compute an1 mod n by ﬁrst computing au mod n and then squaring the result t times successively.

WITNESS.a; n/ let t and u be such that t  1, u is odd, and n  1 D 2tu x0 D MODULAR-EXPONENTIATION.a; u; n/ for i D 1 to t xi D x2 i1 mod n if xi == 1 and xi1 ¤ 1 and xi1 ¤ n  1 return TRUE if xt ¤ 1 return TRUE return FALSE This pseudocode for WITNESS computes an1 mod n by ﬁrst computing the value x0 D au mod n in line 2 and then squaring the result t times in a row in the for loop of lines 3–6. By induction on i, the sequence x0, x1, . . . , xt of values computed satisﬁes the equation xi  a2iu .mod n/ for i D 0; 1; : : : ; t, so that in particular xt  an1 .mod n/. After line 4 performs a squaring step, however, the loop may terminate early if lines 5–6 detect that a nontrivial square root of 1 has just been discovered. (We shall explain these tests shortly.) If so, the algorithm stops and returns TRUE. Lines 7–8 return TRUE if the value computed for xt  an1 .mod n/ is not equal to 1, just as the PSEUDOPRIME procedure returns COMPOSITE in this case. Line 9 returns FALSE if we haven’t returned TRUE in lines 6 or 8. We now argue that if WITNESS.a; n/ returns TRUE, then we can construct a proof that n is composite using a as a witness. If WITNESS returns TRUE from line 8, then it has discovered that xt D an1 mod n ¤ 1. If n is prime, however, we have by Fermat’s theorem (Theorem 31.31) that an1  1 .mod n/ for all a 2 ZC n . Therefore, n cannot be prime, and the equation an1 mod n ¤ 1 proves this fact. If WITNESS returns TRUE from line 6, then it has discovered that xi1 is a nontrivial square root of 1, modulo n, since we have that xi1 6 ˙1 .mod n/ yet xi  x2 i1  1 .mod n/. Corollary 31.35 states that only if n is composite can there exist a nontrivial square root of 1 modulo n, so that demonstrating that xi1 is a nontrivial square root of 1 modulo n proves that n is composite. This completes our proof of the correctness of WITNESS. If we ﬁnd that the call WITNESS.a; n/ returns TRUE, then n is surely composite, and the witness a, along with the reason that the procedure returns TRUE (did it return from line 6 or from line 8?), provides a proof that n is composite.

At this point, we brieﬂy present an alternative description of the behavior of WITNESS as a function of the sequence X D hx0; x1; : : : ; xti, which we shall ﬁnd useful later on, when we analyze the efﬁciency of the Miller-Rabin primality test. Note that if xi D 1 for some 0  i < t, WITNESS might not compute the rest of the sequence. If it were to do so, however, each value xiC1; xiC2; : : : ; xt would be 1, and we consider these positions in the sequence X as being all 1s. We have four cases: 1. X D h: : : ; di, where d ¤ 1: the sequence X does not end in 1. Return TRUE in line 8; a is a witness to the compositeness of n (by Fermat’s Theorem). 2. X D h1; 1; : : : ; 1i: the sequence X is all 1s. Return FALSE; a is not a witness to the compositeness of n. 3. X D h: : : ; 1; 1; : : : ; 1i: the sequence X ends in 1, and the last non-1 is equal to 1. Return FALSE; a is not a witness to the compositeness of n. 4. X D h: : : ; d; 1; : : : ; 1i, where d ¤ ˙1: the sequence X ends in 1, but the last non-1 is not 1. Return TRUE in line 6; a is a witness to the compositeness of n, since d is a nontrivial square root of 1. We now examine the Miller-Rabin primality test based on the use of WITNESS.

Again, we assume that n is an odd integer greater than 2.

MILLER-RABIN.n; s/ for j D 1 to s a D RANDOM.1; n  1/ if WITNESS.a; n/ return COMPOSITE // deﬁnitely return PRIME // almost surely The procedure MILLER-RABIN is a probabilistic search for a proof that n is composite. The main loop (beginning on line 1) picks up to s random values of a from ZC n (line 2). If one of the a’s picked is a witness to the compositeness of n, then MILLER-RABIN returns COMPOSITE on line 4. Such a result is always correct, by the correctness of WITNESS. If MILLER-RABIN ﬁnds no witness in s trials, then the procedure assumes that this is because no witnesses exist, and therefore it assumes that n is prime. We shall see that this result is likely to be correct if s is large enough, but that there is still a tiny chance that the procedure may be unlucky in its choice of a’s and that witnesses do exist even though none has been found. To illustrate the operation of MILLER-RABIN, let n be the Carmichael number 561, so that n  1 D 560 D 24  35, t D 4, and u D 35. If the procedure chooses a D 7 as a base, Figure 31.4 in Section 31.6 shows that WIT- NESS computes x0  a35  241 .mod 561/ and thus computes the sequence

## 31.8 Primality testing

X D h241; 298; 166; 67; 1i. Thus, WITNESS discovers a nontrivial square root of 1 in the last squaring step, since a280  67 .mod n/ and a560  1 .mod n/. Therefore, a D 7 is a witness to the compositeness of n, WITNESS.7; n/ returns TRUE, and MILLER-RABIN returns COMPOSITE. If n is a ˇ-bit number, MILLER-RABIN requires O.sˇ/ arithmetic operations and O.sˇ3/ bit operations, since it requires asymptotically no more work than s modular exponentiations.

Error rate of the Miller-Rabin primality test If MILLER-RABIN returns PRIME, then there is a very slim chance that it has made an error. Unlike PSEUDOPRIME, however, the chance of error does not depend on n; there are no bad inputs for this procedure. Rather, it depends on the size of s and the “luck of the draw” in choosing base values a. Moreover, since each test is more stringent than a simple check of equation (31.40), we can expect on general principles that the error rate should be small for randomly chosen integers n. The following theorem presents a more precise argument.

> **Theorem 31.38**

If n is an odd composite number, then the number of witnesses to the compositeness of n is at least .n  1/=2.

Proof The proof shows that the number of nonwitnesses is at most .n  1/=2, which implies the theorem. We start by claiming that any nonwitness must be a member of Z n. Why?

Consider any nonwitness a. It must satisfy an1  1 .mod n/ or, equivalently, a  an2  1 .mod n/. Thus, the equation ax  1 .mod n/ has a solution, namely an2. By Corollary 31.21, gcd.a; n/ j 1, which in turn implies that gcd.a; n/ D 1. Therefore, a is a member of Z n; all nonwitnesses belong to Z n. To complete the proof, we show that not only are all nonwitnesses contained in Z n, they are all contained in a proper subgroup B of Z n (recall that we say B is a proper subgroup of Z n when B is subgroup of Z n but B is not equal to Z n). By Corollary 31.16, we then have jBj  jZ nj =2. Since jZ nj  n  1, we obtain jBj  .n  1/=2. Therefore, the number of nonwitnesses is at most .n  1/=2, so that the number of witnesses must be at least .n  1/=2. We now show how to ﬁnd a proper subgroup B of Z n containing all of the nonwitnesses. We break the proof into two cases.

Case 1: There exists an x 2 Z n such that xn1 6 1 .mod n/ :

In other words, n is not a Carmichael number.

Because, as we noted earlier, Carmichael numbers are extremely rare, case 1 is the main case that arises “in practice” (e.g., when n has been chosen randomly and is being tested for primality).

Let B D fb 2 Z n W bn1  1 .mod n/g. Clearly, B is nonempty, since 1 2 B.

Since B is closed under multiplication modulo n, we have that B is a subgroup of Z n by Theorem 31.14. Note that every nonwitness belongs to B, since a nonwitness a satisﬁes an1  1 .mod n/. Since x 2 Z n  B, we have that B is a proper subgroup of Z n.

Case 2: For all x 2 Z n, xn1  1 .mod n/ : (31.41) In other words, n is a Carmichael number. This case is extremely rare in practice. However, the Miller-Rabin test (unlike a pseudo-primality test) can efﬁciently determine that Carmichael numbers are composite, as we now show. In this case, n cannot be a prime power. To see why, let us suppose to the contrary that n D pe, where p is a prime and e > 1. We derive a contradiction as follows. Since we assume that n is odd, p must also be odd. Theorem 31.32 implies that Z n is a cyclic group: it contains a generator g such that ordn.g/ D jZ nj D .n/ D pe.1  1=p/ D .p  1/pe1. (The formula for .n/ comes from equation (31.20).) By equation (31.41), we have gn1  1 .mod n/. Then the discrete logarithm theorem (Theorem 31.33, taking y D 0) implies that n  1  0 .mod .n//, or .p  1/pe1 j pe  1 : This is a contradiction for e > 1, since .p  1/pe1 is divisible by the prime p but pe  1 is not. Thus, n is not a prime power.

Since the odd composite number n is not a prime power, we decompose it into a product n1n2, where n1 and n2 are odd numbers greater than 1 that are relatively prime to each other. (There may be several ways to decompose n, and it does not matter which one we choose. For example, if n D pe1 1 pe2 2    per r , then we can choose n1 D pe1 1 and n2 D pe2 2 pe3 3    per r .) Recall that we deﬁne t and u so that n  1 D 2tu, where t  1 and u is odd, and that for an input a, the procedure WITNESS computes the sequence X D hau; a2u; a22u; : : : ; a2tui (all computations are performed modulo n).

Let us call a pair .; j / of integers acceptable if  2 Z n, j 2 f0; 1; : : : ; tg, and 2j u  1 .mod n/ :

## 31.8 Primality testing

Acceptable pairs certainly exist since u is odd; we can choose  D n  1 and j D 0, so that .n1; 0/ is an acceptable pair. Now pick the largest possible j such that there exists an acceptable pair .; j /, and ﬁx  so that .; j / is an acceptable pair. Let B D fx 2 Z n W x2j u  ˙1 .mod n/g :

Since B is closed under multiplication modulo n, it is a subgroup of Z n. By Theorem 31.15, therefore, jBj divides jZ nj. Every nonwitness must be a member of B, since the sequence X produced by a nonwitness must either be all 1s or else contain a 1 no later than the j th position, by the maximality of j . (If .a; j 0/ is acceptable, where a is a nonwitness, we must have j 0  j by how we chose j .) We now use the existence of  to demonstrate that there exists a w 2 Z n  B, and hence that B is a proper subgroup of Z n. Since 2j u  1 .mod n/, we have 2j u  1 .mod n1/ by Corollary 31.29 to the Chinese remainder theorem. By

> **Corollary 31.28, there exists a w simultaneously satisfying the equations**

w   .mod n1/ ; w  1 .mod n2/ : Therefore, w2j u  1 .mod n1/ ; w2j u  .mod n2/ : By Corollary 31.29, w2j u 6 1 .mod n1/ implies w2j u 6 1 .mod n/, and w2j u 6 1 .mod n2/ implies w2j u 6 1 .mod n/. Hence, we conclude that w2j u 6 ˙1 .mod n/, and so w 62 B. It remains to show that w 2 Z n, which we do by ﬁrst working separately modulo n1 and modulo n2. Working modulo n1, we observe that since  2 Z n, we have that gcd.; n/ D 1, and so also gcd.; n1/ D 1; if  does not have any common divisors with n, then it certainly does not have any common divisors with n1.

Since w   .mod n1/, we see that gcd.w; n1/ D 1. Working modulo n2, we observe that w  1 .mod n2/ implies gcd.w; n2/ D 1. To combine these results, we use Theorem 31.6, which implies that gcd.w; n1n2/ D gcd.w; n/ D 1. That is, w 2 Z n. Therefore w 2 Z n  B, and we ﬁnish case 2 with the conclusion that B is a proper subgroup of Z n. In either case, we see that the number of witnesses to the compositeness of n is at least .n  1/=2.

> **Theorem 31.39**

For any odd integer n > 2 and positive integer s, the probability that MILLER- RABIN.n; s/ errs is at most 2s.

Proof Using Theorem 31.38, we see that if n is composite, then each execution of the for loop of lines 1–4 has a probability of at least 1=2 of discovering a witness x to the compositeness of n. MILLER-RABIN makes an error only if it is so unlucky as to miss discovering a witness to the compositeness of n on each of the s iterations of the main loop. The probability of such a sequence of misses is at most 2s. If n is prime, MILLER-RABIN always reports PRIME, and if n is composite, the chance that MILLER-RABIN reports PRIME is at most 2s.

When applying MILLER-RABIN to a large randomly chosen integer n, however, we need to consider as well the prior probability that n is prime, in order to correctly interpret MILLER-RABIN’s result. Suppose that we ﬁx a bit length ˇ and choose at random an integer n of length ˇ bits to be tested for primality. Let A denote the event that n is prime. By the prime number theorem (Theorem 31.37), the probability that n is prime is approximately Pr fAg  1= ln n  1:443=ˇ : Now let B denote the event that MILLER-RABIN returns PRIME. We have that Pr ˚ B j A

D 0 (or equivalently, that Pr fB j Ag D 1) and Pr ˚ B j A

 2s (or equivalently, that Pr ˚ B j A

> 1  2s).

But what is Pr fA j Bg, the probability that n is prime, given that MILLER- RABIN has returned PRIME? By the alternate form of Bayes’s theorem (equation (C.18)) we have Pr fA j Bg D Pr fAg Pr fB j Ag Pr fAg Pr fB j Ag C Pr ˚ A

Pr ˚ B j A

 1 C 2s.ln n  1/ : This probability does not exceed 1=2 until s exceeds lg.ln n  1/. Intuitively, that many initial trials are needed just for the conﬁdence derived from failing to ﬁnd a witness to the compositeness of n to overcome the prior bias in favor of n being composite. For a number with ˇ D 1024 bits, this initial testing requires about lg.ln n  1/  lg.ˇ=1:443/  trials. In any case, choosing s D 50 should sufﬁce for almost any imaginable application. In fact, the situation is much better. If we are trying to ﬁnd large primes by applying MILLER-RABIN to large randomly chosen odd integers, then choosing a small value of s (say 3) is very unlikely to lead to erroneous results, though

## 31.9 Integer factorization

we won’t prove it here. The reason is that for a randomly chosen odd composite integer n, the expected number of nonwitnesses to the compositeness of n is likely to be very much smaller than .n  1/=2. If the integer n is not chosen randomly, however, the best that can be proven is that the number of nonwitnesses is at most .n  1/=4, using an improved version of Theorem 31.38. Furthermore, there do exist integers n for which the number of nonwitnesses is .n  1/=4.

## Exercises

31.8-1 Prove that if an odd integer n > 1 is not a prime or a prime power, then there exists a nontrivial square root of 1 modulo n. 31.8-2 ? It is possible to strengthen Euler’s theorem slightly to the form a	.n/  1 .mod n/ for all a 2 Z n ; where n D pe1 1    per r and .n/ is deﬁned by .n/ D lcm..pe1 1 /; : : : ; .per r // : (31.42) Prove that .n/ j .n/.

A composite number n is a Carmichael number if .n/ j n  1. The smallest Carmichael number is 561 D 3  11  17; here, .n/ D lcm.2; 10; 16/ D 80, which divides 560. Prove that Carmichael numbers must be both “square-free” (not divisible by the square of any prime) and the product of at least three primes. (For this reason, they are not very common.) 31.8-3 Prove that if x is a nontrivial square root of 1, modulo n, then gcd.x  1; n/ and gcd.x C 1; n/ are both nontrivial divisors of n. ?

## 31.9 Integer factorization

Suppose we have an integer n that we wish to factor, that is, to decompose into a product of primes. The primality test of the preceding section may tell us that n is composite, but it does not tell us the prime factors of n. Factoring a large integer n seems to be much more difﬁcult than simply determining whether n is prime or composite. Even with today’s supercomputers and the best algorithms to date, we cannot feasibly factor an arbitrary 1024-bit number.

Pollard’s rho heuristic Trial division by all integers up to R is guaranteed to factor completely any number up to R2. For the same amount of work, the following procedure, POLLARD-RHO, factors any number up to R4 (unless we are unlucky). Since the procedure is only a heuristic, neither its running time nor its success is guaranteed, although the procedure is highly effective in practice. Another advantage of the POLLARD- RHO procedure is that it uses only a constant number of memory locations. (If you wanted to, you could easily implement POLLARD-RHO on a programmable pocket calculator to ﬁnd factors of small numbers.) POLLARD-RHO.n/ i D 1 x1 D RANDOM.0; n  1/ y D x1 k D 2 while TRUE i D i C 1 xi D .x2 i1  1/ mod n d D gcd.y  xi; n/ if d ¤ 1 and d ¤ n print d if i == k y D xi k D 2k The procedure works as follows. Lines 1–2 initialize i to 1 and x1 to a randomly chosen value in Zn. The while loop beginning on line 5 iterates forever, searching for factors of n. During each iteration of the while loop, line 7 uses the recurrence xi D .x2 i1  1/ mod n (31.43) to produce the next value of xi in the inﬁnite sequence x1; x2; x3; x4; : : : ; (31.44) with line 6 correspondingly incrementing i. The pseudocode is written using subscripted variables xi for clarity, but the program works the same if all of the subscripts are dropped, since only the most recent value of xi needs to be maintained.

With this modiﬁcation, the procedure uses only a constant number of memory locations.

Every so often, the program saves the most recently generated xi value in the variable y. Speciﬁcally, the values that are saved are the ones whose subscripts are powers of 2:

## 31.9 Integer factorization

x1; x2; x4; x8; x16; : : : :

Line 3 saves the value x1, and line 12 saves xk whenever i is equal to k. The variable k is initialized to 2 in line 4, and line 13 doubles it whenever line 12 updates y. Therefore, k follows the sequence 1; 2; 4; 8; : : : and always gives the subscript of the next value xk to be saved in y.

Lines 8–10 try to ﬁnd a factor of n, using the saved value of y and the current value of xi.

Speciﬁcally, line 8 computes the greatest common divisor d D gcd.y  xi; n/. If line 9 ﬁnds d to be a nontrivial divisor of n, then line 10 prints d. This procedure for ﬁnding a factor may seem somewhat mysterious at ﬁrst. Note, however, that POLLARD-RHO never prints an incorrect answer; any number it prints is a nontrivial divisor of n. POLLARD-RHO might not print anything at all, though; it comes with no guarantee that it will print any divisors. We shall see, however, that we have good reason to expect POLLARD-RHO to print a factor p of n after ‚.pp/ iterations of the while loop. Thus, if n is composite, we can expect this procedure to discover enough divisors to factor n completely after approximately n1=4 updates, since every prime factor p of n except possibly the largest one is less than pn. We begin our analysis of how this procedure behaves by studying how long it takes a random sequence modulo n to repeat a value. Since Zn is ﬁnite, and since each value in the sequence (31.44) depends only on the previous value, the sequence (31.44) eventually repeats itself. Once we reach an xi such that xi D xj for some j < i, we are in a cycle, since xiC1 D xjC1, xiC2 D xjC2, and so on. The reason for the name “rho heuristic” is that, as Figure 31.7 shows, we can draw the sequence x1; x2; : : : ; xj1 as the “tail” of the rho and the cycle xj; xjC1; : : : ; xi as the “body” of the rho.

Let us consider the question of how long it takes for the sequence of xi to repeat. This information is not exactly what we need, but we shall see later how to modify the argument. For the purpose of this estimation, let us assume that the function fn.x/ D .x2  1/ mod n behaves like a “random” function. Of course, it is not really random, but this assumption yields results consistent with the observed behavior of POLLARD-RHO. We can then consider each xi to have been independently drawn from Zn according to a uniform distribution on Zn. By the birthday-paradox analysis of Section 5.4.1, we expect ‚.pn/ steps to be taken before the sequence cycles. Now for the required modiﬁcation. Let p be a nontrivial factor of n such that gcd.p; n=p/ D 1. For example, if n has the factorization n D pe1 1 pe2 2    per r , then we may take p to be pe1 1 . (If e1 D 1, then p is just the smallest prime factor of n, a good example to keep in mind.)

(b) (c) (a) mod 1387 mod 19 mod 73 x1 x2 x3 x4 x5 x6 x7 x0 x0 x0 x0 x0 x0 x0 x00 x00 x00 x00 x00 x00 x00 Figure 31.7 Pollard’s rho heuristic. (a) The values produced by the recurrence xiC1 D .x2 i  1/ mod 1387, starting with x1 D 2. The prime factorization of 1387 is 19  73. The heavy arrows indicate the iteration steps that are executed before the factor 19 is discovered. The light arrows point to unreached values in the iteration, to illustrate the “rho” shape. The shaded values are the y values stored by POLLARD-RHO. The factor 19 is discovered upon reaching x7 D 177, when gcd.63  177; 1387/ D 19 is computed. The ﬁrst x value that would be repeated is 1186, but the factor 19 is discovered before this value is repeated. (b) The values produced by the same recurrence, modulo 19. Every value xi given in part (a) is equivalent, modulo 19, to the value x0 i shown here.

For example, both x4 D 63 and x7 D 177 are equivalent to 6, modulo 19. (c) The values produced by the same recurrence, modulo 73. Every value xi given in part (a) is equivalent, modulo 73, to the value x00 i shown here. By the Chinese remainder theorem, each node in part (a) corresponds to a pair of nodes, one from part (b) and one from part (c). The sequence hxii induces a corresponding sequence hx0 ii modulo p, where x0 i D xi mod p for all i.

Furthermore, because fn is deﬁned using only arithmetic operations (squaring and subtraction) modulo n, we can compute x0 iC1 from x0 i; the “modulo p” view of

## 31.9 Integer factorization

the sequence is a smaller version of what is happening modulo n: x0 iC1 D xiC1 mod p D fn.xi/ mod p D ..x2 i  1/ mod n/ mod p D .x2 i  1/ mod p (by Exercise 31.1-7) D ..xi mod p/2  1/ mod p D ..x0 i/2  1/ mod p D fp.x0 i/ : Thus, although we are not explicitly computing the sequence hx0 ii, this sequence is well deﬁned and obeys the same recurrence as the sequence hxii.

Reasoning as before, we ﬁnd that the expected number of steps before the sequence hx0 ii repeats is ‚.pp/. If p is small compared to n, the sequence hx0 ii might repeat much more quickly than the sequence hxii. Indeed, as parts (b) and (c) of Figure 31.7 show, the hx0 ii sequence repeats as soon as two elements of the sequence hxii are merely equivalent modulo p, rather than equivalent modulo n.

Let t denote the index of the ﬁrst repeated value in the hx0 ii sequence, and let u > 0 denote the length of the cycle that has been thereby produced. That is, t and u > 0 are the smallest values such that x0 tCi D x0 tCuCi for all i  0. By the above arguments, the expected values of t and u are both ‚.pp/. Note that if x0 tCi D x0 tCuCi, then p j .xtCuCi  xtCi/. Thus, gcd.xtCuCi  xtCi; n/ > 1. Therefore, once POLLARD-RHO has saved as y any value xk such that k  t, then y mod p is always on the cycle modulo p. (If a new value is saved as y, that value is also on the cycle modulo p.) Eventually, k is set to a value that is greater than u, and the procedure then makes an entire loop around the cycle modulo p without changing the value of y. The procedure then discovers a factor of n when xi “runs into” the previously stored value of y, modulo p, that is, when xi  y .mod p/.

Presumably, the factor found is the factor p, although it may occasionally happen that a multiple of p is discovered. Since the expected values of both t and u are ‚.pp/, the expected number of steps required to produce the factor p is ‚.pp/. This algorithm might not perform quite as expected, for two reasons. First, the heuristic analysis of the running time is not rigorous, and it is possible that the cycle of values, modulo p, could be much larger than pp. In this case, the algorithm performs correctly but much more slowly than desired. In practice, this issue seems to be moot. Second, the divisors of n produced by this algorithm might always be one of the trivial factors 1 or n. For example, suppose that n D pq, where p and q are prime. It can happen that the values of t and u for p are identical with the values of t and u for q, and thus the factor p is always revealed in the same gcd operation that reveals the factor q. Since both factors are revealed at the same

time, the trivial factor pq D n is revealed, which is useless. Again, this problem seems to be insigniﬁcant in practice. If necessary, we can restart the heuristic with a different recurrence of the form xiC1 D .x2 i  c/ mod n. (We should avoid the values c D 0 and c D 2 for reasons we will not go into here, but other values are ﬁne.) Of course, this analysis is heuristic and not rigorous, since the recurrence is not really “random.” Nonetheless, the procedure performs well in practice, and it seems to be as efﬁcient as this heuristic analysis indicates. It is the method of choice for ﬁnding small prime factors of a large number. To factor a ˇ-bit composite number n completely, we only need to ﬁnd all prime factors less than bn1=2c, and so we expect POLLARD-RHO to require at most n1=4 D 2ˇ=4 arithmetic operations and at most n1=4ˇ2 D 2ˇ=4ˇ2 bit operations. POLLARD-RHO’s ability to ﬁnd a small factor p of n with an expected number ‚.pp/ of arithmetic operations is often its most appealing feature.

## Exercises

31.9-1 Referring to the execution history shown in Figure 31.7(a), when does POLLARD- RHO print the factor 73 of 1387? 31.9-2 Suppose that we are given a function f W Zn ! Zn and an initial value x0 2 Zn.

Deﬁne xi D f .xi1/ for i D 1; 2; : : :. Let t and u > 0 be the smallest values such that xtCi D xtCuCi for i D 0; 1; : : :. In the terminology of Pollard’s rho algorithm, t is the length of the tail and u is the length of the cycle of the rho. Give an efﬁcient algorithm to determine t and u exactly, and analyze its running time. 31.9-3 How many steps would you expect POLLARD-RHO to require to discover a factor of the form pe, where p is prime and e > 1? 31.9-4 ? One disadvantage of POLLARD-RHO as written is that it requires one gcd computation for each step of the recurrence. Instead, we could batch the gcd computations by accumulating the product of several xi values in a row and then using this product instead of xi in the gcd computation. Describe carefully how you would implement this idea, why it works, and what batch size you would pick as the most effective when working on a ˇ-bit number n.

Problems for Chapter 31

## Problems

31-1 Binary gcd algorithm Most computers can perform the operations of subtraction, testing the parity (odd or even) of a binary integer, and halving more quickly than computing remainders. This problem investigates the binary gcd algorithm, which avoids the remainder computations used in Euclid’s algorithm. a. Prove that if a and b are both even, then gcd.a; b/ D 2  gcd.a=2; b=2/. b. Prove that if a is odd and b is even, then gcd.a; b/ D gcd.a; b=2/. c. Prove that if a and b are both odd, then gcd.a; b/ D gcd..a  b/=2; b/. d. Design an efﬁcient binary gcd algorithm for input integers a and b, where a  b, that runs in O.lg a/ time. Assume that each subtraction, parity test, and halving takes unit time. 31-2 Analysis of bit operations in Euclid’s algorithm a. Consider the ordinary “paper and pencil” algorithm for long division: dividing a by b, which yields a quotient q and remainder r. Show that this method requires O..1 C lg q/ lg b/ bit operations. b. Deﬁne .a; b/ D .1 C lg a/.1 C lg b/. Show that the number of bit operations performed by EUCLID in reducing the problem of computing gcd.a; b/ to that of computing gcd.b; a mod b/ is at most c. .a; b/  .b; a mod b// for some sufﬁciently large constant c > 0. c. Show that EUCLID.a; b/ requires O. .a; b// bit operations in general and O.ˇ2/ bit operations when applied to two ˇ-bit inputs. 31-3 Three algorithms for Fibonacci numbers This problem compares the efﬁciency of three methods for computing the nth Fibonacci number Fn, given n. Assume that the cost of adding, subtracting, or multiplying two numbers is O.1/, independent of the size of the numbers. a. Show that the running time of the straightforward recursive method for computing Fn based on recurrence (3.22) is exponential in n. (See, for example, the FIB procedure on page 775.) b. Show how to compute Fn in O.n/ time using memoization.

c. Show how to compute Fn in O.lg n/ time using only integer addition and multiplication. (Hint: Consider the matrix  0  and its powers.) d. Assume now that adding two ˇ-bit numbers takes ‚.ˇ/ time and that multiplying two ˇ-bit numbers takes ‚.ˇ2/ time. What is the running time of these three methods under this more reasonable cost measure for the elementary arithmetic operations? 31-4 Quadratic residues Let p be an odd prime. A number a 2 Z p is a quadratic residue if the equation x2 D a .mod p/ has a solution for the unknown x. a. Show that there are exactly .p  1/=2 quadratic residues, modulo p. b. If p is prime, we deﬁne the Legendre symbol . a p/, for a 2 Z p, to be 1 if a is a quadratic residue modulo p and 1 otherwise. Prove that if a 2 Z p, then  a p   a.p1/=2 .mod p/ :

Give an efﬁcient algorithm that determines whether a given number a is a quadratic residue modulo p. Analyze the efﬁciency of your algorithm. c. Prove that if p is a prime of the form 4k C 3 and a is a quadratic residue in Z p, then akC1 mod p is a square root of a, modulo p. How much time is required to ﬁnd the square root of a quadratic residue a modulo p? d. Describe an efﬁcient randomized algorithm for ﬁnding a nonquadratic residue, modulo an arbitrary prime p, that is, a member of Z p that is not a quadratic residue. How many arithmetic operations does your algorithm require on average?

Chapter notes Niven and Zuckerman [265] provide an excellent introduction to elementary number theory. Knuth [210] contains a good discussion of algorithms for ﬁnding the

Notes for Chapter 31 greatest common divisor, as well as other basic number-theoretic algorithms. Bach [30] and Riesel [295] provide more recent surveys of computational number theory. Dixon [91] gives an overview of factorization and primality testing. The conference proceedings edited by Pomerance [280] contains several excellent survey articles. More recently, Bach and Shallit [31] have provided an exceptional overview of the basics of computational number theory.

Knuth [210] discusses the origin of Euclid’s algorithm. It appears in Book 7, Propositions 1 and 2, of the Greek mathematician Euclid’s Elements, which was written around 300 B.C. Euclid’s description may have been derived from an algorithm due to Eudoxus around 375 B.C. Euclid’s algorithm may hold the honor of being the oldest nontrivial algorithm; it is rivaled only by an algorithm for multiplication known to the ancient Egyptians. Shallit [312] chronicles the history of the analysis of Euclid’s algorithm.

Knuth attributes a special case of the Chinese remainder theorem (Theorem 31.27) to the Chinese mathematician Sun-Ts˘u, who lived sometime between 200 B.C. and A.D. 200—the date is quite uncertain. The same special case was given by the Greek mathematician Nichomachus around A.D. 100. It was generalized by Chhin Chiu-Shao in 1247. The Chinese remainder theorem was ﬁnally stated and proved in its full generality by L. Euler in 1734. The randomized primality-testing algorithm presented here is due to Miller [255] and Rabin [289]; it is the fastest randomized primality-testing algorithm known, to within constant factors. The proof of Theorem 31.39 is a slight adaptation of one suggested by Bach [29]. A proof of a stronger result for MILLER-RABIN was given by Monier [258, 259]. For many years primality-testing was the classic example of a problem where randomization appeared to be necessary to obtain an efﬁcient (polynomial-time) algorithm. In 2002, however, Agrawal, Kayal, and Saxema [4] surprised everyone with their deterministic polynomial-time primalitytesting algorithm. Until then, the fastest deterministic primality testing algorithm known, due to Cohen and Lenstra [73], ran in time .lg n/O.lg lg lg n/ on input n, which is just slightly superpolynomial. Nonetheless, for practical purposes randomized primality-testing algorithms remain more efﬁcient and are preferred. The problem of ﬁnding large “random” primes is nicely discussed in an article by Beauchemin, Brassard, Cr´epeau, Goutier, and Pomerance [36]. The concept of a public-key cryptosystem is due to Difﬁe and Hellman [87]. The RSA cryptosystem was proposed in 1977 by Rivest, Shamir, and Adleman [296]. Since then, the ﬁeld of cryptography has blossomed. Our understanding of the RSA cryptosystem has deepened, and modern implementations use significant reﬁnements of the basic techniques presented here. In addition, many new techniques have been developed for proving cryptosystems to be secure. For example, Goldwasser and Micali [142] show that randomization can be an effective tool in the design of secure public-key encryption schemes. For signature schemes,

Goldwasser, Micali, and Rivest [143] present a digital-signature scheme for which every conceivable type of forgery is provably as difﬁcult as factoring. Menezes, van Oorschot, and Vanstone [254] provide an overview of applied cryptography. The rho heuristic for integer factorization was invented by Pollard [277]. The version presented here is a variant proposed by Brent [56]. The best algorithms for factoring large numbers have a running time that grows roughly exponentially with the cube root of the length of the number n to be factored. The general number-ﬁeld sieve factoring algorithm (as developed by Buhler, Lenstra, and Pomerance [57] as an extension of the ideas in the number-ﬁeld sieve factoring algorithm by Pollard [278] and Lenstra et al. [232] and reﬁned by Coppersmith [77] and others) is perhaps the most efﬁcient such algorithm in general for large inputs. Although it is difﬁcult to give a rigorous analysis of this algorithm, under reasonable assumptions we can derive a running-time estimate of L.1=3; n/1:902Co.1/, where L.˛; n/ D e.ln n/˛.ln ln n/1˛. The elliptic-curve method due to Lenstra [233] may be more effective for some inputs than the number-ﬁeld sieve method, since, like Pollard’s rho method, it can ﬁnd a small prime factor p quite quickly. With this method, the time to ﬁnd p is estimated to be L.1=2; p/ p 2Co.1/.
