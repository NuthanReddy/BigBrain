# A Summations

A
Summations
When an algorithm contains an iterative control construct such as a while or for
loop, we can express its running time as the sum of the times spent on each exe-
cution of the body of the loop. For example, we found in Section 2.2 that the j th
iteration of insertion sort took time proportional to j in the worst case. By adding
up the time spent on each iteration, we obtained the summation (or series)
n
X
jD2
j :
When we evaluated this summation, we attained a bound of ‚.n2/ on the worst-
case running time of the algorithm. This example illustrates why you should know
how to manipulate and bound summations.
Section A.1 lists several basic formulas involving summations. Section A.2 of-
fers useful techniques for bounding summations. We present the formulas in Sec-
tion A.1 without proof, though proofs for some of them appear in Section A.2 to
illustrate the methods of that section. You can ﬁnd most of the other proofs in any
calculus text.
A.1
Summation formulas and properties
Given a sequence a1; a2; : : : ; an of numbers, where n is a nonnegative integer, we
can write the ﬁnite sum a1 C a2 C    C an as
n
X
kD1
ak :
If n D 0, the value of the summation is deﬁned to be 0. The value of a ﬁnite series
is always well deﬁned, and we can add its terms in any order.
Given an inﬁnite sequence a1; a2; : : : of numbers, we can write the inﬁnite sum
a1 C a2 C    as

1146
Appendix A
Summations
1
X
kD1
ak ;
which we interpret to mean
lim
n!1
n
X
kD1
ak :
If the limit does not exist, the series diverges; otherwise, it converges. The terms
of a convergent series cannot always be added in any order. We can, however,
rearrange the terms of an absolutely convergent series, that is, a series P1
kD1 ak
for which the series P1
kD1 jakj also converges.
Linearity
For any real number c and any ﬁnite sequences a1; a2; : : : ; an and b1; b2; : : : ; bn,
n
X
kD1
.cak C bk/ D c
n
X
kD1
ak C
n
X
kD1
bk :
The linearity property also applies to inﬁnite convergent series.
We can exploit the linearity property to manipulate summations incorporating
asymptotic notation. For example,
n
X
kD1
‚.f .k// D ‚
 n
X
kD1
f .k/
!
:
In this equation, the ‚-notation on the left-hand side applies to the variable k, but
on the right-hand side, it applies to n. We can also apply such manipulations to
inﬁnite convergent series.
Arithmetic series
The summation
n
X
kD1
k D 1 C 2 C    C n ;
is an arithmetic series and has the value
n
X
kD1
k
D
1
2n.n C 1/
(A.1)
D
‚.n2/ :
(A.2)

A.1
Summation formulas and properties
1147
Sums of squares and cubes
We have the following summations of squares and cubes:
n
X
kD0
k2
D
n.n C 1/.2n C 1/
6
;
(A.3)
n
X
kD0
k3
D
n2.n C 1/2
4
:
(A.4)
Geometric series
For real x ¤ 1, the summation
n
X
kD0
xk D 1 C x C x2 C    C xn
is a geometric or exponential series and has the value
n
X
kD0
xk D xnC1  1
x  1
:
(A.5)
When the summation is inﬁnite and jxj < 1, we have the inﬁnite decreasing geo-
metric series
1
X
kD0
xk D
1
1  x :
(A.6)
Harmonic series
For positive integers n, the nth harmonic number is
Hn
D
1 C 1
2 C 1
3 C 1
4 C    C 1
n
D
n
X
kD1
1
k
D
ln n C O.1/ :
(A.7)
(We shall prove a related bound in Section A.2.)
Integrating and differentiating series
By integrating or differentiating the formulas above, additional formulas arise. For
example, by differentiating both sides of the inﬁnite geometric series (A.6) and
multiplying by x, we get

1148
Appendix A
Summations
1
X
kD0
kxk D
x
.1  x/2
(A.8)
for jxj < 1.
Telescoping series
For any sequence a0; a1; : : : ; an,
n
X
kD1
.ak  ak1/ D an  a0 ;
(A.9)
since each of the terms a1; a2; : : : ; an1 is added in exactly once and subtracted out
exactly once. We say that the sum telescopes. Similarly,
n1
X
kD0
.ak  akC1/ D a0  an :
As an example of a telescoping sum, consider the series
n1
X
kD1
1
k.k C 1/ :
Since we can rewrite each term as
1
k.k C 1/ D 1
k 
1
k C 1 ;
we get
n1
X
kD1
1
k.k C 1/
D
n1
X
kD1
1
k 
1
k C 1

D
1  1
n :
Products
We can write the ﬁnite product a1a2    an as
n
Y
kD1
ak :
If n D 0, the value of the product is deﬁned to be 1. We can convert a formula with
a product to a formula with a summation by using the identity
lg
 n
Y
kD1
ak
!
D
n
X
kD1
lg ak :

A.2
Bounding summations
1149
Exercises
A.1-1
Find a simple formula for Pn
kD1.2k  1/.
A.1-2
?
Show that Pn
kD1 1=.2k  1/ D ln.pn/ C O.1/ by manipulating the harmonic
series.
A.1-3
Show that P1
kD0 k2xk D x.1 C x/=.1  x/3 for 0 < jxj < 1.
A.1-4
?
Show that P1
kD0.k  1/=2k D 0.
A.1-5
?
Evaluate the sum P1
kD1.2k C 1/x2k.
A.1-6
Prove that Pn
kD1 O.fk.i// D O

 Pn
kD1 fk.i/

by using the linearity property of
summations.
A.1-7
Evaluate the product Qn
kD1 2  4k.
A.1-8
?
Evaluate the product Qn
kD2.1  1=k2/.
A.2
Bounding summations
We have many techniques at our disposal for bounding the summations that de-
scribe the running times of algorithms. Here are some of the most frequently used
methods.
Mathematical induction
The most basic way to evaluate a series is to use mathematical induction. As an
example, let us prove that the arithmetic series Pn
kD1 k evaluates to 1
2n.nC1/. We
can easily verify this assertion for n D 1. We make the inductive assumption that

1150
Appendix A
Summations
it holds for n, and we prove that it holds for n C 1. We have
nC1
X
kD1
k
D
n
X
kD1
k C .n C 1/
D
1
2n.n C 1/ C .n C 1/
D
1
2.n C 1/.n C 2/ :
You don’t always need to guess the exact value of a summation in order to use
mathematical induction. Instead, you can use induction to prove a bound on a sum-
mation. As an example, let us prove that the geometric series Pn
kD0 3k is O.3n/.
More speciﬁcally, let us prove that Pn
kD0 3k  c3n for some constant c. For the
initial condition n D 0, we have P0
kD0 3k D 1  c  1 as long as c  1. Assuming
that the bound holds for n, let us prove that it holds for n C 1. We have
nC1
X
kD0
3k
D
n
X
kD0
3k C 3nC1

c3n C 3nC1
(by the inductive hypothesis)
D
1
3 C 1
c

c3nC1

c3nC1
as long as .1=3 C 1=c/  1 or, equivalently, c  3=2. Thus, Pn
kD0 3k D O.3n/,
as we wished to show.
We have to be careful when we use asymptotic notation to prove bounds by in-
duction. Consider the following fallacious proof that Pn
kD1 k D O.n/. Certainly,
P1
kD1 k D O.1/. Assuming that the bound holds for n, we now prove it for n C 1:
nC1
X
kD1
k
D
n
X
kD1
k C .n C 1/
D
O.n/ C .n C 1/

 wrong!!
D
O.n C 1/ :
The bug in the argument is that the “constant” hidden by the “big-oh” grows with n
and thus is not constant. We have not shown that the same constant works for all n.
Bounding the terms
We can sometimes obtain a good upper bound on a series by bounding each term
of the series, and it often sufﬁces to use the largest term to bound the others. For

A.2
Bounding summations
1151
example, a quick upper bound on the arithmetic series (A.1) is
n
X
kD1
k

n
X
kD1
n
D
n2 :
In general, for a series Pn
kD1 ak, if we let amax D max1kn ak, then
n
X
kD1
ak  n  amax :
The technique of bounding each term in a series by the largest term is a weak
method when the series can in fact be bounded by a geometric series. Given the
series Pn
kD0 ak, suppose that akC1=ak  r for all k  0, where 0 < r < 1 is a
constant. We can bound the sum by an inﬁnite decreasing geometric series, since
ak  a0rk, and thus
n
X
kD0
ak

1
X
kD0
a0rk
D
a0
1
X
kD0
rk
D
a0
1
1  r :
We can apply this method to bound the summation P1
kD1.k=3k/. In order to
start the summation at k D 0, we rewrite it as P1
kD0..k C 1/=3kC1/. The ﬁrst
term (a0) is 1=3, and the ratio (r) of consecutive terms is
.k C 2/=3kC2
.k C 1/=3kC1
D
1
3  k C 2
k C 1

2
3
for all k  0. Thus, we have
1
X
kD1
k
3k
D
1
X
kD0
k C 1
3kC1

1
3 
1
1  2=3
D
1 :

1152
Appendix A
Summations
A common bug in applying this method is to show that the ratio of consecu-
tive terms is less than 1 and then to assume that the summation is bounded by a
geometric series. An example is the inﬁnite harmonic series, which diverges since
1
X
kD1
1
k
D
lim
n!1
n
X
kD1
1
k
D
lim
n!1 ‚.lg n/
D
1 :
The ratio of the .kC1/st and kth terms in this series is k=.kC1/ < 1, but the series
is not bounded by a decreasing geometric series. To bound a series by a geometric
series, we must show that there is an r < 1, which is a constant, such that the ratio
of all pairs of consecutive terms never exceeds r. In the harmonic series, no such r
exists because the ratio becomes arbitrarily close to 1.
Splitting summations
One way to obtain bounds on a difﬁcult summation is to express the series as the
sum of two or more series by partitioning the range of the index and then to bound
each of the resulting series. For example, suppose we try to ﬁnd a lower bound
on the arithmetic series Pn
kD1 k, which we have already seen has an upper bound
of n2. We might attempt to bound each term in the summation by the smallest term,
but since that term is 1, we get a lower bound of n for the summation—far off from
our upper bound of n2.
We can obtain a better lower bound by ﬁrst splitting the summation. Assume for
convenience that n is even. We have
n
X
kD1
k
D
n=2
X
kD1
k C
n
X
kDn=2C1
k

n=2
X
kD1
0 C
n
X
kDn=2C1
.n=2/
D
.n=2/2
D
.n2/ ;
which is an asymptotically tight bound, since Pn
kD1 k D O.n2/.
For a summation arising from the analysis of an algorithm, we can often split
the summation and ignore a constant number of the initial terms. Generally, this
technique applies when each term ak in a summation Pn
kD0 ak is independent of n.

A.2
Bounding summations
1153
Then for any constant k0 > 0, we can write
n
X
kD0
ak
D
k01
X
kD0
ak C
n
X
kDk0
ak
D
‚.1/ C
n
X
kDk0
ak ;
since the initial terms of the summation are all constant and there are a constant
number of them. We can then use other methods to bound Pn
kDk0 ak. This tech-
nique applies to inﬁnite summations as well. For example, to ﬁnd an asymptotic
upper bound on
1
X
kD0
k2
2k ;
we observe that the ratio of consecutive terms is
.k C 1/2=2kC1
k2=2k
D
.k C 1/2
2k2

8
9
if k  3. Thus, the summation can be split into
1
X
kD0
k2
2k
D
2
X
kD0
k2
2k C
1
X
kD3
k2
2k

2
X
kD0
k2
2k C 9
8
1
X
kD0
8
9
k
D
O.1/ ;
since the ﬁrst summation has a constant number of terms and the second summation
is a decreasing geometric series.
The technique of splitting summations can help us determine asymptotic bounds
in much more difﬁcult situations. For example, we can obtain a bound of O.lg n/
on the harmonic series (A.7):
Hn D
n
X
kD1
1
k :
We do so by splitting the range 1 to n into blg nc C 1 pieces and upper-bounding
the contribution of each piece by 1. For i D 0; 1; : : : ; blg nc, the ith piece consists

1154
Appendix A
Summations
of the terms starting at 1=2i and going up to but not including 1=2iC1. The last
piece might contain terms not in the original harmonic series, and thus we have
n
X
kD1
1
k

blg nc
X
iD0
2i1
X
jD0
1
2i C j

blg nc
X
iD0
2i1
X
jD0
1
2i
D
blg nc
X
iD0
1

lg n C 1 :
(A.10)
Approximation by integrals
When a summation has the form Pn
kDm f .k/, where f .k/ is a monotonically in-
creasing function, we can approximate it by integrals:
Z n
m1
f .x/ dx 
n
X
kDm
f .k/ 
Z nC1
m
f .x/ dx :
(A.11)
Figure A.1 justiﬁes this approximation. The summation is represented as the area
of the rectangles in the ﬁgure, and the integral is the shaded region under the curve.
When f .k/ is a monotonically decreasing function, we can use a similar method
to provide the bounds
Z nC1
m
f .x/ dx 
n
X
kDm
f .k/ 
Z n
m1
f .x/ dx :
(A.12)
The integral approximation (A.12) gives a tight estimate for the nth harmonic
number. For a lower bound, we obtain
n
X
kD1
1
k

Z nC1
1
dx
x
D
ln.n C 1/ :
(A.13)
For the upper bound, we derive the inequality
n
X
kD2
1
k

Z n
1
dx
x
D
ln n ;

A.2
Bounding summations
1155
n+1
n–1
n–2
m+2
m
m –1
f (m)
f (m+1)
f (m+2)
f (n–2)
f (n–1)
f (n)
f (x)
x
…
…
n
…
…
(a)
m+1
n+1
n–1
n–2
m+2
m
m –1
f (m)
f (m+1)
f (m+2)
f (n–2)
f (n–1)
f (n)
f (x)
x
…
…
n
…
…
(b)
m+1
Figure A.1
Approximation of Pn
kDm f .k/ by integrals. The area of each rectangle is shown
within the rectangle, and the total rectangle area represents the value of the summation. The in-
tegral is represented by the shaded area under the curve.
By comparing areas in (a), we get
R n
m1 f .x/dx  Pn
kDm f .k/, and then by shifting the rectangles one unit to the right, we get
Pn
kDm f .k/ 
R nC1
m
f .x/dx in (b).

1156
Appendix A
Summations
which yields the bound
n
X
kD1
1
k  ln n C 1 :
(A.14)
Exercises
A.2-1
Show that Pn
kD1 1=k2 is bounded above by a constant.
A.2-2
Find an asymptotic upper bound on the summation
blg nc
X
kD0
˙
n=2k
:
A.2-3
Show that the nth harmonic number is .lg n/ by splitting the summation.
A.2-4
Approximate Pn
kD1 k3 with an integral.
A.2-5
Why didn’t we use the integral approximation (A.12) directly on Pn
kD1 1=k to
obtain an upper bound on the nth harmonic number?
Problems
A-1
Bounding summations
Give asymptotically tight bounds on the following summations. Assume that r  0
and s  0 are constants.
a.
n
X
kD1
kr.
b.
n
X
kD1
lgs k.

Notes for Appendix A
1157
c.
n
X
kD1
kr lgs k.
Appendix notes
Knuth [209] provides an excellent reference for the material presented here. You
can ﬁnd basic properties of series in any good calculus book, such as Apostol [18]
or Thomas et al. [334].
