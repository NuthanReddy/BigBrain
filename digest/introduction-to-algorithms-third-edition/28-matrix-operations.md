# 28 Matrix Operations

Matrix Operations
Because operations on matrices lie at the heart of scientiﬁc computing, efﬁcient algorithms for working with matrices have many practical applications. This chapter
focuses on how to multiply matrices and solve sets of simultaneous linear equations. Appendix D reviews the basics of matrices.
Section 28.1 shows how to solve a set of linear equations using LUP decompositions. Then, Section 28.2 explores the close relationship between multiplying and
inverting matrices. Finally, Section 28.3 discusses the important class of symmetric
positive-deﬁnite matrices and shows how we can use them to ﬁnd a least-squares
solution to an overdetermined set of linear equations.
One important issue that arises in practice is numerical stability. Due to the
limited precision of ﬂoating-point representations in actual computers, round-off
errors in numerical computations may become ampliﬁed over the course of a computation, leading to incorrect results; we call such computations numerically unstable. Although we shall brieﬂy consider numerical stability on occasion, we do
not focus on it in this chapter. We refer you to the excellent book by Golub and
Van Loan [144] for a thorough discussion of stability issues.

## 28.1 Solving systems of linear equations

Numerous applications need to solve sets of simultaneous linear equations. We
can formulate a linear system as a matrix equation in which each matrix or vector
element belongs to a ﬁeld, typically the real numbers R. This section discusses how
to solve a system of linear equations using a method called LUP decomposition.
We start with a set of linear equations in n unknowns x1; x2; : : : ; xn:

a11x1 C a12x2 C    C a1nxn
D
b1 ;
a21x1 C a22x2 C    C a2nxn
D
b2 ;
:::
an1x1 C an2x2 C    C annxn
D
bn :
(28.1)
A solution to the equations (28.1) is a set of values for x1; x2; : : : ; xn that satisfy
all of the equations simultaneously. In this section, we treat only the case in which
there are exactly n equations in n unknowns.
We can conveniently rewrite equations (28.1) as the matrix-vector equation
˙
a11
a12
a1n
a21
a22
a2n
:::
:::
:::
:::
an1
an2
ann
˙
x1
x2
:::
xn

D
˙
b1
b2
:::
bn

or, equivalently, letting A D .aij/, x D .xi/, and b D .bi/, as
Ax D b :
(28.2)
If A is nonsingular, it possesses an inverse A1, and
x D A1b
(28.3)
is the solution vector. We can prove that x is the unique solution to equation (28.2)
as follows. If there are two solutions, x and x0, then Ax D Ax0 D b and, letting I
denote an identity matrix,
x
D
Ix
D
.A1A/x
D
A1.Ax/
D
A1.Ax0/
D
.A1A/x0
D
x0 :
In this section, we shall be concerned predominantly with the case in which A
is nonsingular or, equivalently (by Theorem D.1), the rank of A is equal to the
number n of unknowns. There are other possibilities, however, which merit a brief
discussion. If the number of equations is less than the number n of unknowns—or,
more generally, if the rank of A is less than n—then the system is underdetermined. An underdetermined system typically has inﬁnitely many solutions, although it may have no solutions at all if the equations are inconsistent. If the
number of equations exceeds the number n of unknowns, the system is overdetermined, and there may not exist any solutions. Section 28.3 addresses the important

## 28.1 Solving systems of linear equations

problem of ﬁnding good approximate solutions to overdetermined systems of linear
equations.
Let us return to our problem of solving the system Ax D b of n equations in n
unknowns. We could compute A1 and then, using equation (28.3), multiply b
by A1, yielding x D A1b. This approach suffers in practice from numerical
instability. Fortunately, another approach—LUP decomposition—is numerically
stable and has the further advantage of being faster in practice.
Overview of LUP decomposition
The idea behind LUP decomposition is to ﬁnd three n 	 n matrices L, U , and P
such that
PA D LU ;
(28.4)
where

L is a unit lower-triangular matrix,

U is an upper-triangular matrix, and

P is a permutation matrix.
We call matrices L, U , and P satisfying equation (28.4) an LUP decomposition
of the matrix A. We shall show that every nonsingular matrix A possesses such a
decomposition.
Computing an LUP decomposition for the matrix A has the advantage that we
can more easily solve linear systems when they are triangular, as is the case for
both matrices L and U . Once we have found an LUP decomposition for A, we
can solve equation (28.2), Ax D b, by solving only triangular linear systems, as
follows. Multiplying both sides of Ax D b by P yields the equivalent equation
PAx D Pb, which, by Exercise D.1-4, amounts to permuting the equations (28.1).
Using our decomposition (28.4), we obtain
LUx D Pb :
We can now solve this equation by solving two triangular linear systems. Let us
deﬁne y D Ux, where x is the desired solution vector. First, we solve the lowertriangular system
Ly D Pb
(28.5)
for the unknown vector y by a method called “forward substitution.” Having solved
for y, we then solve the upper-triangular system
Ux D y
(28.6)

for the unknown x by a method called “back substitution.” Because the permutation matrix P is invertible (Exercise D.2-3), multiplying both sides of equation (28.4) by P 1 gives P 1PA D P 1LU , so that
A D P 1LU :
(28.7)
Hence, the vector x is our solution to Ax D b:
Ax
D
P 1LUx
(by equation (28.7))
D
P 1Ly
(by equation (28.6))
D
P 1Pb
(by equation (28.5))
D
b :
Our next step is to show how forward and back substitution work and then attack
the problem of computing the LUP decomposition itself.
Forward and back substitution
Forward substitution can solve the lower-triangular system (28.5) in ‚.n2/ time,
given L, P , and b. For convenience, we represent the permutation P compactly
by an array Œ1 : : n. For i D 1; 2; : : : ; n, the entry Œi indicates that Pi;Œi D 1
and Pij D 0 for j ¤ Œi. Thus, PA has aŒi;j in row i and column j , and Pb
has bŒi as its ith element. Since L is unit lower-triangular, we can rewrite equation (28.5) as
y1
D
bŒ1 ;
l21y1 C
y2
D
bŒ2 ;
l31y1 C l32y2 C
y3
D
bŒ3 ;
:::
ln1y1 C ln2y2 C ln3y3 C    C yn
D
bŒn :
The ﬁrst equation tells us that y1 D bŒ1. Knowing the value of y1, we can
substitute it into the second equation, yielding
y2 D bŒ2  l21y1 :
Now, we can substitute both y1 and y2 into the third equation, obtaining
y3 D bŒ3  .l31y1 C l32y2/ :
In general, we substitute y1; y2; : : : ; yi1 “forward” into the ith equation to solve
for yi:

## 28.1 Solving systems of linear equations

yi D bŒi 
i1
X
jD1
lij yj :
Having solved for y, we solve for x in equation (28.6) using back substitution,
which is similar to forward substitution. Here, we solve the nth equation ﬁrst and
work backward to the ﬁrst equation. Like forward substitution, this process runs
in ‚.n2/ time. Since U is upper-triangular, we can rewrite the system (28.6) as
u11x1 C u12x2 C    C
u1;n2xn2 C
u1;n1xn1 C
u1nxn D y1 ;
u22x2 C    C
u2;n2xn2 C
u2;n1xn1 C
u2nxn D y2 ;
:::
un2;n2xn2 C un2;n1xn1 C un2;nxn D yn2 ;
un1;n1xn1 C un1;nxn D yn1 ;
un;nxn D yn :
Thus, we can solve for xn; xn1; : : : ; x1 successively as follows:
xn
D
yn=un;n ;
xn1
D
.yn1  un1;nxn/=un1;n1 ;
xn2
D
.yn2  .un2;n1xn1 C un2;nxn//=un2;n2 ;
:::
or, in general,
xi D

yi 
n
X
jDiC1
uijxj
!
=uii :
Given P , L, U , and b, the procedure LUP-SOLVE solves for x by combining
forward and back substitution. The pseudocode assumes that the dimension n appears in the attribute L:rows and that the permutation matrix P is represented by
the array .
LUP-SOLVE.L; U; ; b/
n D L:rows
let x be a new vector of length n
for i D 1 to n
yi D bŒi  Pi1
jD1 lijyj
for i D n downto 1
xi D

yi  Pn
jDiC1 uij xj

=uii
return x

Procedure LUP-SOLVE solves for y using forward substitution in lines 3–4, and
then it solves for x using backward substitution in lines 5–6. Since the summation
within each of the for loops includes an implicit loop, the running time is ‚.n2/.
As an example of these methods, consider the system of linear equations deﬁned
by

x D


;
where
A
D


;
b
D


;
and we wish to solve for the unknown x. The LUP decomposition is
L
D

0:2
0:6
0:5

;
U
D

0:8
0:6
2:5

;
P
D


:
(You might want to verify that PA D LU .) Using forward substitution, we solve
Ly D Pb for y:

0:2
0:6
0:5

y1
y2
y3

D


;
obtaining
y D

1:4
1:5

by computing ﬁrst y1, then y2, and ﬁnally y3. Using back substitution, we solve
Ux D y for x:

## 28.1 Solving systems of linear equations


0:8
0:6
2:5

x1
x2
x3

D

1:4
1:5

;
thereby obtaining the desired answer
x D

1:4
2:2
0:6

by computing ﬁrst x3, then x2, and ﬁnally x1.
Computing an LU decomposition
We have now shown that if we can create an LUP decomposition for a nonsingular
matrix A, then forward and back substitution can solve the system Ax D b of
linear equations. Now we show how to efﬁciently compute an LUP decomposition
for A. We start with the case in which A is an n 	 n nonsingular matrix and P is
absent (or, equivalently, P D In). In this case, we factor A D LU . We call the
two matrices L and U an LU decomposition of A.
We use a process known as Gaussian elimination to create an LU decomposition. We start by subtracting multiples of the ﬁrst equation from the other equations
in order to remove the ﬁrst variable from those equations. Then, we subtract multiples of the second equation from the third and subsequent equations so that now
the ﬁrst and second variables are removed from them. We continue this process
until the system that remains has an upper-triangular form—in fact, it is the matrix U . The matrix L is made up of the row multipliers that cause variables to be
eliminated.
Our algorithm to implement this strategy is recursive. We wish to construct an
LU decomposition for an n 	 n nonsingular matrix A. If n D 1, then we are done,
since we can choose L D I1 and U D A. For n > 1, we break A into four parts:
A
D
˙
a11
a12
a1n
a21
a22
a2n
:::
:::
:::
:::
an1
an2
ann

D
 a11
wT

A0

;
where  is a column .n  1/-vector, wT is a row .n  1/-vector, and A0 is an
.n  1/ 	 .n  1/ matrix. Then, using matrix algebra (verify the equations by

simply multiplying through), we can factor A as
A
D
 a11
wT

A0

D

=a11
In1
 a11
wT
A0  wT=a11

:
(28.8)
The 0s in the ﬁrst and second matrices of equation (28.8) are row and column .n  1/-vectors, respectively.
The term wT=a11, formed by taking the
outer product of  and w and dividing each element of the result by a11, is an
.n  1/ 	 .n  1/ matrix, which conforms in size to the matrix A0 from which it is
subtracted. The resulting .n  1/ 	 .n  1/ matrix
A0  wT=a11
(28.9)
is called the Schur complement of A with respect to a11.
We claim that if A is nonsingular, then the Schur complement is nonsingular,
too. Why? Suppose that the Schur complement, which is .n  1/ 	 .n  1/, is
singular. Then by Theorem D.1, it has row rank strictly less than n  1. Because
the bottom n  1 entries in the ﬁrst column of the matrix
 a11
wT
A0  wT=a11

are all 0, the bottom n  1 rows of this matrix must have row rank strictly less
than n  1. The row rank of the entire matrix, therefore, is strictly less than n.
Applying Exercise D.2-8 to equation (28.8), A has rank strictly less than n, and
from Theorem D.1 we derive the contradiction that A is singular.
Because the Schur complement is nonsingular, we can now recursively ﬁnd an
LU decomposition for it. Let us say that
A0  wT=a11 D L0U 0 ;
where L0 is unit lower-triangular and U 0 is upper-triangular. Then, using matrix
algebra, we have
A
D

=a11
In1
 a11
wT
A0  wT=a11

D

=a11
In1
 a11
wT
L0U 0

D

=a11
L0
 a11
wT
U 0

D
LU ;
thereby providing our LU decomposition. (Note that because L0 is unit lowertriangular, so is L, and because U 0 is upper-triangular, so is U .)

## 28.1 Solving systems of linear equations

Of course, if a11 D 0, this method doesn’t work, because it divides by 0. It also
doesn’t work if the upper leftmost entry of the Schur complement A0  wT=a11
is 0, since we divide by it in the next step of the recursion. The elements by
which we divide during LU decomposition are called pivots, and they occupy the
diagonal elements of the matrix U . The reason we include a permutation matrix P
during LUP decomposition is that it allows us to avoid dividing by 0. When we use
permutations to avoid division by 0 (or by small numbers, which would contribute
to numerical instability), we are pivoting.
An important class of matrices for which LU decomposition always works correctly is the class of symmetric positive-deﬁnite matrices. Such matrices require
no pivoting, and thus we can employ the recursive strategy outlined above without fear of dividing by 0. We shall prove this result, as well as several others, in
Section 28.3.
Our code for LU decomposition of a matrix A follows the recursive strategy, except that an iteration loop replaces the recursion. (This transformation is a standard
optimization for a “tail-recursive” procedure—one whose last operation is a recursive call to itself. See Problem 7-4.) It assumes that the attribute A:rows gives
the dimension of A. We initialize the matrix U with 0s below the diagonal and
matrix L with 1s on its diagonal and 0s above the diagonal.
LU-DECOMPOSITION.A/
n D A:rows
let L and U be new n 	 n matrices
initialize U with 0s below the diagonal
initialize L with 1s on the diagonal and 0s above the diagonal
for k D 1 to n
ukk D akk
for i D k C 1 to n
lik D aik=ukk
// lik holds i
uki D aki
// uki holds wT
i
for i D k C 1 to n
for j D k C 1 to n
aij D aij  likukj
return L and U
The outer for loop beginning in line 5 iterates once for each recursive step. Within
this loop, line 6 determines the pivot to be ukk D akk. The for loop in lines 7–9
(which does not execute when k D n), uses the  and wT vectors to update L
and U . Line 8 determines the elements of the  vector, storing i in lik, and line 9
computes the elements of the wT vector, storing wT
i in uki. Finally, lines 10–12
compute the elements of the Schur complement and store them back into the ma822
6 13 5 19
2 19 10 23
4 10 11 31
(a)
1 16 9 18
9 21
(b)
7 17
(c)
(d)
(e)

˘
D

˘ 
˘
A
L
U
Figure 28.1
The operation of LU-DECOMPOSITION. (a) The matrix A. (b) The element a11 D 2
in the black circle is the pivot, the shaded column is =a11, and the shaded row is wT. The elements
of U computed thus far are above the horizontal line, and the elements of L are to the left of the
vertical line. The Schur complement matrix A0  wT=a11 occupies the lower right. (c) We now
operate on the Schur complement matrix produced from part (b). The element a22 D 4 in the black
circle is the pivot, and the shaded column and row are =a22 and wT (in the partitioning of the Schur
complement), respectively. Lines divide the matrix into the elements of U computed so far (above),
the elements of L computed so far (left), and the new Schur complement (lower right). (d) After the
next step, the matrix A is factored. (The element 3 in the new Schur complement becomes part of U
when the recursion terminates.) (e) The factorization A D LU .
trix A. (We don’t need to divide by akk in line 12 because we already did so when
we computed lik in line 8.) Because line 12 is triply nested, LU-DECOMPOSITION
runs in time ‚.n3/.
Figure 28.1 illustrates the operation of LU-DECOMPOSITION. It shows a standard optimization of the procedure in which we store the signiﬁcant elements of L
and U in place in the matrix A. That is, we can set up a correspondence between
each element aij and either lij (if i > j ) or uij (if i  j ) and update the matrix A so that it holds both L and U when the procedure terminates. To obtain
the pseudocode for this optimization from the above pseudocode, just replace each
reference to l or u by a; you can easily verify that this transformation preserves
correctness.
Computing an LUP decomposition
Generally, in solving a system of linear equations Ax D b, we must pivot on offdiagonal elements of A to avoid dividing by 0. Dividing by 0 would, of course,
be disastrous. But we also want to avoid dividing by a small value—even if A is

## 28.1 Solving systems of linear equations

nonsingular—because numerical instabilities can result. We therefore try to pivot
on a large value.
The mathematics behind LUP decomposition is similar to that of LU decomposition. Recall that we are given an n 	 n nonsingular matrix A, and we wish
to ﬁnd a permutation matrix P , a unit lower-triangular matrix L, and an uppertriangular matrix U such that PA D LU . Before we partition the matrix A, as we
did for LU decomposition, we move a nonzero element, say ak1, from somewhere
in the ﬁrst column to the .1; 1/ position of the matrix. For numerical stability, we
choose ak1 as the element in the ﬁrst column with the greatest absolute value. (The
ﬁrst column cannot contain only 0s, for then A would be singular, because its determinant would be 0, by Theorems D.4 and D.5.) In order to preserve the set of
equations, we exchange row 1 with row k, which is equivalent to multiplying A by
a permutation matrix Q on the left (Exercise D.1-4). Thus, we can write QA as
QA D
 ak1
wT

A0

;
where  D .a21; a31; : : : ; an1/T, except that a11 replaces ak1; wT D .ak2; ak3;
: : : ; akn/; and A0 is an .n1/	.n1/ matrix. Since ak1 ¤ 0, we can now perform
much the same linear algebra as for LU decomposition, but now guaranteeing that
we do not divide by 0:
QA
D
 ak1
wT

A0

D

=ak1
In1
 ak1
wT
A0  wT=ak1

:
As we saw for LU decomposition, if A is nonsingular, then the Schur complement A0  wT=ak1 is nonsingular, too. Therefore, we can recursively ﬁnd an
LUP decomposition for it, with unit lower-triangular matrix L0, upper-triangular
matrix U 0, and permutation matrix P 0, such that
P 0.A0  wT=ak1/ D L0U 0 :
Deﬁne
P D
 1
P 0

Q ;
which is a permutation matrix, since it is the product of two permutation matrices
(Exercise D.1-4). We now have

PA
D
 1
P 0

QA
D
 1
P 0

=ak1
In1
 ak1
wT
A0  wT=ak1

D

P 0=ak1
P 0
 ak1
wT
A0  wT=ak1

D

P 0=ak1
In1
 ak1
wT
P 0.A0  wT=ak1/

D

P 0=ak1
In1
 ak1
wT
L0U 0

D

P 0=ak1
L0
 ak1
wT
U 0

D
LU ;
yielding the LUP decomposition. Because L0 is unit lower-triangular, so is L, and
because U 0 is upper-triangular, so is U .
Notice that in this derivation, unlike the one for LU decomposition, we must
multiply both the column vector =ak1 and the Schur complement A0  wT=ak1
by the permutation matrix P 0. Here is the pseudocode for LUP decomposition:
LUP-DECOMPOSITION.A/
n D A:rows
let Œ1 : : n be a new array
for i D 1 to n
Œi D i
for k D 1 to n
p D 0
for i D k to n
if jaikj > p
p D jaikj
k0 D i
if p == 0
error “singular matrix”
exchange Œk with Œk0
for i D 1 to n
exchange aki with ak0i
for i D k C 1 to n
aik D aik=akk
for j D k C 1 to n
aij D aij  aikakj

## 28.1 Solving systems of linear equations

Like LU-DECOMPOSITION, our LUP-DECOMPOSITION procedure replaces
the recursion with an iteration loop. As an improvement over a direct implementation of the recursion, we dynamically maintain the permutation matrix P as an
array , where Œi D j means that the ith row of P contains a 1 in column j .
We also implement the code to compute L and U “in place” in the matrix A. Thus,
when the procedure terminates,
aij D
(
lij
if i > j ;
uij
if i  j :
Figure 28.2 illustrates how LUP-DECOMPOSITION factors a matrix. Lines 3–4
initialize the array  to represent the identity permutation. The outer for loop
beginning in line 5 implements the recursion. Each time through the outer loop,
lines 6–10 determine the element ak0k with largest absolute value of those in the
current ﬁrst column (column k) of the .n  k C 1/ 	 .n  k C 1/ matrix whose
LUP decomposition we are ﬁnding. If all elements in the current ﬁrst column are
zero, lines 11–12 report that the matrix is singular. To pivot, we exchange Œk0
with Œk in line 13 and exchange the kth and k0th rows of A in lines 14–15,
thereby making the pivot element akk. (The entire rows are swapped because in
the derivation of the method above, not only is A0  wT=ak1 multiplied by P 0, but
so is =ak1.) Finally, the Schur complement is computed by lines 16–19 in much
the same way as it is computed by lines 7–12 of LU-DECOMPOSITION, except that
here the operation is written to work in place.
Because of its triply nested loop structure, LUP-DECOMPOSITION has a running time of ‚.n3/, which is the same as that of LU-DECOMPOSITION. Thus,
pivoting costs us at most a constant factor in time.

## Exercises

28.1-1
Solve the equation

6

x1
x2
x3

D

7

by using forward substitution.
28.1-2
Find an LU decomposition of the matrix

5
6
7

:

0.6
–2
–1
–2
3.4
–1
(a)
0.6
–2
–1
–2
3.4
–1
(b)
0.4
–2
0.4
–.2
0.6
1.6 –3.2
–0.2
–1
4.2 –0.6
(c)
0.4
–2
0.4 –0.2
0.6
1.6 –3.2
–0.2
–1
4.2 –0.6
(d)
0.4
–2
0.4 –0.2
0.6
1.6 –3.2
–0.2
–1
4.2 –0.6
(e)
0.4
–2
0.4 –0.2
0.6
1.6 –3.2
–0.2 0.5
–0.5
(f)
0.4
–2
0.4 –0.2
0.6
1.6 –3.2
–0.2 0.5
–0.5
(g)
0.4
–2
0.4 –0.2
0.6
1.6 –3.2
–0.2 0.5
–0.5
(h)
0.4
–2
0.4 –0.2
0.6
0.4
–3
–0.2 0.5
–0.5
(i)
(j)

˘ 
0:6
2
1
2
3:4
1
˘
D

0:4
0:2
0:5
0:6
0:4
˘ 
2
0:4
0:2
0:5
3
˘
P
A
L
U
Figure 28.2
The operation of LUP-DECOMPOSITION. (a) The input matrix A with the identity
permutation of the rows on the left. The ﬁrst step of the algorithm determines that the element 5
in the black circle in the third row is the pivot for the ﬁrst column. (b) Rows 1 and 3 are swapped
and the permutation is updated. The shaded column and row represent  and wT. (c) The vector 
is replaced by =5, and the lower right of the matrix is updated with the Schur complement. Lines
divide the matrix into three regions: elements of U (above), elements of L (left), and elements of the
Schur complement (lower right). (d)–(f) The second step. (g)–(i) The third step. No further changes
occur on the fourth (ﬁnal) step. (j) The LUP decomposition PA D LU .

## 28.2 Inverting matrices

28.1-3
Solve the equation


x1
x2
x3

D


by using an LUP decomposition.
28.1-4
Describe the LUP decomposition of a diagonal matrix.
28.1-5
Describe the LUP decomposition of a permutation matrix A, and prove that it is
unique.
28.1-6
Show that for all n  1, there exists a singular n 	 n matrix that has an LU decomposition.
28.1-7
In LU-DECOMPOSITION, is it necessary to perform the outermost for loop iteration when k D n? How about in LUP-DECOMPOSITION?

## 28.2 Inverting matrices

Although in practice we do not generally use matrix inverses to solve systems of
linear equations, preferring instead to use more numerically stable techniques such
as LUP decomposition, sometimes we need to compute a matrix inverse. In this
section, we show how to use LUP decomposition to compute a matrix inverse.
We also prove that matrix multiplication and computing the inverse of a matrix
are equivalently hard problems, in that (subject to technical conditions) we can
use an algorithm for one to solve the other in the same asymptotic running time.
Thus, we can use Strassen’s algorithm (see Section 4.2) for matrix multiplication
to invert a matrix. Indeed, Strassen’s original paper was motivated by the problem
of showing that a set of a linear equations could be solved more quickly than by
the usual method.

Computing a matrix inverse from an LUP decomposition
Suppose that we have an LUP decomposition of a matrix A in the form of three
matrices L, U , and P such that PA D LU . Using LUP-SOLVE, we can solve
an equation of the form Ax D b in time ‚.n2/. Since the LUP decomposition
depends on A but not b, we can run LUP-SOLVE on a second set of equations of
the form Ax D b0 in additional time ‚.n2/. In general, once we have the LUP
decomposition of A, we can solve, in time ‚.kn2/, k versions of the equation
Ax D b that differ only in b.
We can think of the equation
AX D In ;
(28.10)
which deﬁnes the matrix X, the inverse of A, as a set of n distinct equations of the
form Ax D b. To be precise, let Xi denote the ith column of X, and recall that the
unit vector ei is the ith column of In. We can then solve equation (28.10) for X by
using the LUP decomposition for A to solve each equation
AXi D ei
separately for Xi. Once we have the LUP decomposition, we can compute each of
the n columns Xi in time ‚.n2/, and so we can compute X from the LUP decomposition of A in time ‚.n3/. Since we can determine the LUP decomposition of A
in time ‚.n3/, we can compute the inverse A1 of a matrix A in time ‚.n3/.
Matrix multiplication and matrix inversion
We now show that the theoretical speedups obtained for matrix multiplication
translate to speedups for matrix inversion. In fact, we prove something stronger:
matrix inversion is equivalent to matrix multiplication, in the following sense.
If M.n/ denotes the time to multiply two n 	 n matrices, then we can invert a
nonsingular n 	 n matrix in time O.M.n//. Moreover, if I.n/ denotes the time
to invert a nonsingular n 	 n matrix, then we can multiply two n 	 n matrices in
time O.I.n//. We prove these results as two separate theorems.

> **Theorem 28.1 (Multiplication is no harder than inversion)**

If we can invert an n 	 n matrix in time I.n/, where I.n/ D .n2/ and I.n/
satisﬁes the regularity condition I.3n/ D O.I.n//, then we can multiply two n	n
matrices in time O.I.n//.
Proof
Let A and B be n 	 n matrices whose matrix product C we wish to compute. We deﬁne the 3n 	 3n matrix D by

## 28.2 Inverting matrices

D D

In
A
In
B
In

:
The inverse of D is
D1 D

In
A
AB
In
B
In

;
and thus we can compute the product AB by taking the upper right n	n submatrix
of D1.
We can construct matrix D in ‚.n2/ time, which is O.I.n// because we assume
that I.n/ D .n2/, and we can invert D in O.I.3n// D O.I.n// time, by the
regularity condition on I.n/. We thus have M.n/ D O.I.n//.
Note that I.n/ satisﬁes the regularity condition whenever I.n/ D ‚.nc lgd n/
for any constants c > 0 and d  0.
The proof that matrix inversion is no harder than matrix multiplication relies
on some properties of symmetric positive-deﬁnite matrices that we will prove in
Section 28.3.

> **Theorem 28.2 (Inversion is no harder than multiplication)**

Suppose we can multiply two n 	 n real matrices in time M.n/, where M.n/ D
.n2/ and M.n/ satisﬁes the two regularity conditions M.n C k/ D O.M.n// for
any k in the range 0  k  n and M.n=2/  cM.n/ for some constant c < 1=2.
Then we can compute the inverse of any real nonsingular n 	 n matrix in time
O.M.n//.
Proof
We prove the theorem here for real matrices. Exercise 28.2-6 asks you to
generalize the proof for matrices whose entries are complex numbers.
We can assume that n is an exact power of 2, since we have
 A
Ik
1
D
 A1
Ik

for any k > 0. Thus, by choosing k such that n C k is a power of 2, we enlarge
the matrix to a size that is the next power of 2 and obtain the desired answer A1
from the answer to the enlarged problem. The ﬁrst regularity condition on M.n/
ensures that this enlargement does not cause the running time to increase by more
than a constant factor.
For the moment, let us assume that the n	n matrix A is symmetric and positivedeﬁnite. We partition each of A and its inverse A1 into four n=2 	 n=2 submatrices:

A D
 B
C T
C
D

and A1 D
 R
T
U
V

:
(28.11)
Then, if we let
S D D  CB1C T
(28.12)
be the Schur complement of A with respect to B (we shall see more about this form
of Schur complement in Section 28.3), we have
A1 D
 R
T
U
V

D
 B1 C B1C TS 1CB1
B1C TS 1
S 1CB1
S 1

;
(28.13)
since AA1 D In, as you can verify by performing the matrix multiplication. Because A is symmetric and positive-deﬁnite, Lemmas 28.4 and 28.5 in Section 28.3
imply that B and S are both symmetric and positive-deﬁnite. By Lemma 28.3 in
Section 28.3, therefore, the inverses B1 and S 1 exist, and by Exercise D.2-6,
B1 and S 1 are symmetric, so that .B1/T D B1 and .S 1/T D S 1. Therefore, we can compute the submatrices R, T , U , and V of A1 as follows, where
all matrices mentioned are n=2 	 n=2:
1. Form the submatrices B, C, C T, and D of A.
2. Recursively compute the inverse B1 of B.
3. Compute the matrix product W D CB1, and then compute its transpose W T,
which equals B1C T (by Exercise D.1-2 and .B1/T D B1).
4. Compute the matrix product X D W C T, which equals CB1C T, and then
compute the matrix S D D  X D D  CB1C T.
5. Recursively compute the inverse S 1 of S, and set V to S 1.
6. Compute the matrix product Y
D S 1W , which equals S 1CB1, and
then compute its transpose Y T, which equals B1C TS 1 (by Exercise D.1-2,
.B1/T D B1, and .S 1/T D S 1). Set T to Y T and U to Y .
7. Compute the matrix product Z D W TY , which equals B1C TS 1CB1, and
set R to B1 C Z.
Thus, we can invert an n	n symmetric positive-deﬁnite matrix by inverting two
n=2 	 n=2 matrices in steps 2 and 5; performing four multiplications of n=2 	 n=2
matrices in steps 3, 4, 6, and 7; plus an additional cost of O.n2/ for extracting
submatrices from A, inserting submatrices into A1, and performing a constant
number of additions, subtractions, and transposes on n=2 	 n=2 matrices. We get
the recurrence
I.n/

2I.n=2/ C 4M.n=2/ C O.n2/
D
2I.n=2/ C ‚.M.n//
D
O.M.n// :

## 28.2 Inverting matrices

The second line holds because the second regularity condition in the statement
of the theorem implies that 4M.n=2/ < 2M.n/ and because we assume that
M.n/ D .n2/. The third line follows because the second regularity condition
allows us to apply case 3 of the master theorem (Theorem 4.1).
It remains to prove that we can obtain the same asymptotic running time for matrix multiplication as for matrix inversion when A is invertible but not symmetric
and positive-deﬁnite. The basic idea is that for any nonsingular matrix A, the matrix ATA is symmetric (by Exercise D.1-2) and positive-deﬁnite (by Theorem D.6).
The trick, then, is to reduce the problem of inverting A to the problem of inverting ATA.
The reduction is based on the observation that when A is an n 	 n nonsingular
matrix, we have
A1 D .ATA/1AT ;
since ..ATA/1AT/A D .ATA/1.ATA/ D In and a matrix inverse is unique.
Therefore, we can compute A1 by ﬁrst multiplying AT by A to obtain ATA, then
inverting the symmetric positive-deﬁnite matrix ATA using the above divide-andconquer algorithm, and ﬁnally multiplying the result by AT. Each of these three
steps takes O.M.n// time, and thus we can invert any nonsingular matrix with real
entries in O.M.n// time.
The proof of Theorem 28.2 suggests a means of solving the equation Ax D b
by using LU decomposition without pivoting, so long as A is nonsingular. We
multiply both sides of the equation by AT, yielding .ATA/x D ATb. This transformation doesn’t affect the solution x, since AT is invertible, and so we can factor the symmetric positive-deﬁnite matrix ATA by computing an LU decomposition. We then use forward and back substitution to solve for x with the right-hand
side ATb. Although this method is theoretically correct, in practice the procedure
LUP-DECOMPOSITION works much better. LUP decomposition requires fewer
arithmetic operations by a constant factor, and it has somewhat better numerical
properties.

## Exercises

28.2-1
Let M.n/ be the time to multiply two n 	 n matrices, and let S.n/ denote the time
required to square an n 	 n matrix. Show that multiplying and squaring matrices have essentially the same difﬁculty: an M.n/-time matrix-multiplication algorithm implies an O.M.n//-time squaring algorithm, and an S.n/-time squaring
algorithm implies an O.S.n//-time matrix-multiplication algorithm.

28.2-2
Let M.n/ be the time to multiply two n 	 n matrices, and let L.n/ be the time to
compute the LUP decomposition of an n 	 n matrix. Show that multiplying matrices and computing LUP decompositions of matrices have essentially the same difﬁculty: an M.n/-time matrix-multiplication algorithm implies an O.M.n//-time
LUP-decomposition algorithm, and an L.n/-time LUP-decomposition algorithm
implies an O.L.n//-time matrix-multiplication algorithm.
28.2-3
Let M.n/ be the time to multiply two n 	 n matrices, and let D.n/ denote the
time required to ﬁnd the determinant of an n 	 n matrix. Show that multiplying matrices and computing the determinant have essentially the same difﬁculty:
an M.n/-time matrix-multiplication algorithm implies an O.M.n//-time determinant algorithm, and a D.n/-time determinant algorithm implies an O.D.n//-time
matrix-multiplication algorithm.
28.2-4
Let M.n/ be the time to multiply two n 	 n boolean matrices, and let T .n/ be the
time to ﬁnd the transitive closure of an n 	 n boolean matrix. (See Section 25.2.)
Show that an M.n/-time boolean matrix-multiplication algorithm implies an
O.M.n/ lg n/-time transitive-closure algorithm, and a T .n/-time transitive-closure
algorithm implies an O.T .n//-time boolean matrix-multiplication algorithm.
28.2-5
Does the matrix-inversion algorithm based on Theorem 28.2 work when matrix
elements are drawn from the ﬁeld of integers modulo 2? Explain.
28.2-6
?
Generalize the matrix-inversion algorithm of Theorem 28.2 to handle matrices of
complex numbers, and prove that your generalization works correctly. (Hint: Instead of the transpose of A, use the conjugate transpose A, which you obtain from
the transpose of A by replacing every entry with its complex conjugate. Instead of
symmetric matrices, consider Hermitian matrices, which are matrices A such that
A D A.)

## 28.3 Symmetric positive-deﬁnite matrices and least-squares approximation

Symmetric positive-deﬁnite matrices have many interesting and desirable properties. For example, they are nonsingular, and we can perform LU decomposition
on them without having to worry about dividing by 0. In this section, we shall

## 28.3 Symmetric positive-deﬁnite matrices and least-squares approximation

prove several other important properties of symmetric positive-deﬁnite matrices
and show an interesting application to curve ﬁtting by a least-squares approximation.
The ﬁrst property we prove is perhaps the most basic.

> **Lemma 28.3**

Any positive-deﬁnite matrix is nonsingular.
Proof
Suppose that a matrix A is singular. Then by Corollary D.3, there exists a
nonzero vector x such that Ax D 0. Hence, xTAx D 0, and A cannot be positivedeﬁnite.
The proof that we can perform LU decomposition on a symmetric positivedeﬁnite matrix A without dividing by 0 is more involved. We begin by proving
properties about certain submatrices of A. Deﬁne the kth leading submatrix of A
to be the matrix Ak consisting of the intersection of the ﬁrst k rows and ﬁrst k
columns of A.

> **Lemma 28.4**

If A is a symmetric positive-deﬁnite matrix, then every leading submatrix of A is
symmetric and positive-deﬁnite.
Proof
That each leading submatrix Ak is symmetric is obvious. To prove that Ak
is positive-deﬁnite, we assume that it is not and derive a contradiction. If Ak is not
positive-deﬁnite, then there exists a k-vector xk ¤ 0 such that xT
kAkxk  0. Let A
be n 	 n, and
A D
 Ak
BT
B
C

(28.14)
for submatrices B (which is .nk/	k) and C (which is .nk/	.nk/). Deﬁne
the n-vector x D . xT
k
0 /T, where n  k 0s follow xk. Then we have
xTAx
D
. xT
k
0 /
 Ak
BT
B
C
 xk

D
. xT
k
0 /
 Akxk
Bxk

D
xT
kAkxk

0 ;
which contradicts A being positive-deﬁnite.

We now turn to some essential properties of the Schur complement. Let A be
a symmetric positive-deﬁnite matrix, and let Ak be a leading k 	 k submatrix
of A. Partition A once again according to equation (28.14). We generalize equation (28.9) to deﬁne the Schur complement S of A with respect to Ak as
S D C  BA1
k BT :
(28.15)
(By Lemma 28.4, Ak is symmetric and positive-deﬁnite; therefore, A1
k
exists by

> **Lemma 28.3, and S is well deﬁned.) Note that our earlier deﬁnition (28.9) of the**

Schur complement is consistent with equation (28.15), by letting k D 1.
The next lemma shows that the Schur-complement matrices of symmetric positive-deﬁnite matrices are themselves symmetric and positive-deﬁnite. We used this
result in Theorem 28.2, and we need its corollary to prove the correctness of LU
decomposition for symmetric positive-deﬁnite matrices.

> **Lemma 28.5 (Schur complement lemma)**

If A is a symmetric positive-deﬁnite matrix and Ak is a leading k 	 k submatrix
of A, then the Schur complement S of A with respect to Ak is symmetric and
positive-deﬁnite.
Proof
Because A is symmetric, so is the submatrix C. By Exercise D.2-6, the
product BA1
k BT is symmetric, and by Exercise D.1-1, S is symmetric.
It remains to show that S is positive-deﬁnite. Consider the partition of A given in
equation (28.14). For any nonzero vector x, we have xTAx > 0 by the assumption
that A is positive-deﬁnite. Let us break x into two subvectors y and ´ compatible
with Ak and C, respectively. Because A1
k exists, we have
xTAx
D
. yT
´T /
 Ak
BT
B
C
 y
´

D
. yT
´T /
 Aky C BT´
By C C´

D
yTAky C yTBT´ C ´TBy C ´TC´
D
.y C A1
k BT´/TAk.y C A1
k BT´/ C ´T.C  BA1
k BT/´ ;
(28.16)
by matrix magic. (Verify by multiplying through.) This last equation amounts to
“completing the square” of the quadratic form. (See Exercise 28.3-2.)
Since xTAx > 0 holds for any nonzero x, let us pick any nonzero ´ and then
choose y D A1
k BT´, which causes the ﬁrst term in equation (28.16) to vanish,
leaving
´T.C  BA1
k BT/´ D ´TS´
as the value of the expression.
For any ´ ¤ 0, we therefore have ´TS´ D
xTAx > 0, and thus S is positive-deﬁnite.

## 28.3 Symmetric positive-deﬁnite matrices and least-squares approximation

> **Corollary 28.6**

LU decomposition of a symmetric positive-deﬁnite matrix never causes a division
by 0.
Proof
Let A be a symmetric positive-deﬁnite matrix. We shall prove something
stronger than the statement of the corollary: every pivot is strictly positive. The ﬁrst
pivot is a11. Let e1 be the ﬁrst unit vector, from which we obtain a11 D eT
1Ae1 > 0.
Since the ﬁrst step of LU decomposition produces the Schur complement of A
with respect to A1 D .a11/, Lemma 28.5 implies by induction that all pivots are
positive.
Least-squares approximation
One important application of symmetric positive-deﬁnite matrices arises in ﬁtting
curves to given sets of data points. Suppose that we are given a set of m data points
.x1; y1/; .x2; y2/; : : : ; .xm; ym/ ;
where we know that the yi are subject to measurement errors. We would like to
determine a function F.x/ such that the approximation errors
i D F.xi/  yi
(28.17)
are small for i D 1; 2; : : : ; m. The form of the function F depends on the problem
at hand. Here, we assume that it has the form of a linearly weighted sum,
F.x/ D
n
X
jD1
cjfj.x/ ;
where the number of summands n and the speciﬁc basis functions fj are chosen
based on knowledge of the problem at hand. A common choice is fj.x/ D xj1,
which means that
F.x/ D c1 C c2x C c3x2 C    C cnxn1
is a polynomial of degree n  1 in x. Thus, given m data points .x1; y1/; .x2; y2/;
: : : ; .xm; ym/, we wish to calculate n coefﬁcients c1; c2; : : : ; cn that minimize the
approximation errors 1; 2; : : : ; m.
By choosing n D m, we can calculate each yi exactly in equation (28.17). Such
a high-degree F “ﬁts the noise” as well as the data, however, and generally gives
poor results when used to predict y for previously unseen values of x. It is usually better to choose n signiﬁcantly smaller than m and hope that by choosing the
coefﬁcients cj well, we can obtain a function F that ﬁnds the signiﬁcant patterns
in the data points without paying undue attention to the noise. Some theoretical

principles exist for choosing n, but they are beyond the scope of this text. In any
case, once we choose a value of n that is less than m, we end up with an overdetermined set of equations whose solution we wish to approximate. We now show
how to do so.
Let
A D
˙
f1.x1/
f2.x1/
fn.x1/
f1.x2/
f2.x2/
fn.x2/
:::
:::
:::
:::
f1.xm/
f2.xm/
fn.xm/

denote the matrix of values of the basis functions at the given points; that is,
aij D fj.xi/. Let c D .ck/ denote the desired n-vector of coefﬁcients. Then,
Ac
D
˙
f1.x1/
f2.x1/
fn.x1/
f1.x2/
f2.x2/
fn.x2/
:::
:::
:::
:::
f1.xm/
f2.xm/
fn.xm/
˙
c1
c2
:::
cn

D
˙
F.x1/
F.x2/
:::
F.xm/

is the m-vector of “predicted values” for y. Thus,
 D Ac  y
is the m-vector of approximation errors.
To minimize approximation errors, we choose to minimize the norm of the error
vector , which gives us a least-squares solution, since
kk D
m
X
iD1
2
i
!1=2
:
Because
kk2 D kAc  yk2 D
m
X
iD1
n
X
jD1
aijcj  yi
!2
;
we can minimize kk by differentiating kk2 with respect to each ck and then
setting the result to 0:

## 28.3 Symmetric positive-deﬁnite matrices and least-squares approximation

d kk2
dck
D
m
X
iD1

n
X
jD1
aijcj  yi
!
aik D 0 :
(28.18)
The n equations (28.18) for k D 1; 2; : : : ; n are equivalent to the single matrix
equation
.Ac  y/TA D 0
or, equivalently (using Exercise D.1-2), to
AT.Ac  y/ D 0 ;
which implies
ATAc D ATy :
(28.19)
In statistics, this is called the normal equation. The matrix ATA is symmetric
by Exercise D.1-2, and if A has full column rank, then by Theorem D.6, ATA
is positive-deﬁnite as well.
Hence, .ATA/1 exists, and the solution to equation (28.19) is
c
D

.ATA/1AT

y
D
ACy ;
(28.20)
where the matrix AC D ..ATA/1AT/ is the pseudoinverse of the matrix A. The
pseudoinverse naturally generalizes the notion of a matrix inverse to the case in
which A is not square. (Compare equation (28.20) as the approximate solution to
Ac D y with the solution A1b as the exact solution to Ax D b.)
As an example of producing a least-squares ﬁt, suppose that we have ﬁve data
points
.x1; y1/
D
.1; 2/ ;
.x2; y2/
D
.1; 1/ ;
.x3; y3/
D
.2; 1/ ;
.x4; y4/
D
.3; 0/ ;
.x5; y5/
D
.5; 3/ ;
shown as black dots in Figure 28.3. We wish to ﬁt these points with a quadratic
polynomial
F.x/ D c1 C c2x C c3x2 :
We start with the matrix of basis-function values

0.5
1.0
1.5
2.0
2.5
3.0
0.0
–1
–2
x
y
F(x) = 1.2 – 0.757x + 0.214x2
Figure 28.3
The least-squares ﬁt of a quadratic polynomial to the set of ﬁve data points
f.1; 2/; .1; 1/; .2; 1/; .3; 0/; .5; 3/g. The black dots are the data points, and the white dots are their
estimated values predicted by the polynomial F.x/ D 1:2  0:757x C 0:214x2, the quadratic polynomial that minimizes the sum of the squared errors. Each shaded line shows the error for one data
point.
A D

x1
x2
x2
x2
x3
x2
x4
x2
x5
x2

D

1

;
whose pseudoinverse is
AC D

0:500
0:300
0:200
0:100
0:100
0:388
0:093
0:190
0:193
0:088
0:060
0:036
0:048
0:036
0:060

:
Multiplying y by AC, we obtain the coefﬁcient vector
c D

1:200
0:757
0:214

;
which corresponds to the quadratic polynomial

## 28.3 Symmetric positive-deﬁnite matrices and least-squares approximation

F.x/ D 1:200  0:757x C 0:214x2
as the closest-ﬁtting quadratic to the given data, in a least-squares sense.
As a practical matter, we solve the normal equation (28.19) by multiplying y
by AT and then ﬁnding an LU decomposition of ATA. If A has full rank, the
matrix ATA is guaranteed to be nonsingular, because it is symmetric and positivedeﬁnite. (See Exercise D.1-2 and Theorem D.6.)

## Exercises

28.3-1
Prove that every diagonal element of a symmetric positive-deﬁnite matrix is positive.
28.3-2
Let A D
 a
b
b
c

be a 2 	 2 symmetric positive-deﬁnite matrix. Prove that its
determinant ac  b2 is positive by “completing the square” in a manner similar to
that used in the proof of Lemma 28.5.
28.3-3
Prove that the maximum element in a symmetric positive-deﬁnite matrix lies on
the diagonal.
28.3-4
Prove that the determinant of each leading submatrix of a symmetric positivedeﬁnite matrix is positive.
28.3-5
Let Ak denote the kth leading submatrix of a symmetric positive-deﬁnite matrix A.
Prove that det.Ak/= det.Ak1/ is the kth pivot during LU decomposition, where,
by convention, det.A0/ D 1.
28.3-6
Find the function of the form
F.x/ D c1 C c2x lg x C c3ex
that is the best least-squares ﬁt to the data points
.1; 1/; .2; 1/; .3; 3/; .4; 8/ :

28.3-7
Show that the pseudoinverse AC satisﬁes the following four equations:
AACA
D
A ;
ACAAC
D
AC ;
.AAC/T
D
AAC ;
.ACA/T
D
ACA :

## Problems

28-1
Tridiagonal systems of linear equations
Consider the tridiagonal matrix
A D
ˇ
1
1
1
1
1
1
1
1

:
a. Find an LU decomposition of A.
b. Solve the equation Ax D

T by using forward and back substitution.
c. Find the inverse of A.
d. Show how, for any n 	 n symmetric positive-deﬁnite, tridiagonal matrix A and
any n-vector b, to solve the equation Ax D b in O.n/ time by performing an
LU decomposition. Argue that any method based on forming A1 is asymptotically more expensive in the worst case.
e. Show how, for any n	n nonsingular, tridiagonal matrix A and any n-vector b, to
solve the equation Ax D b in O.n/ time by performing an LUP decomposition.
28-2
Splines
A practical method for interpolating a set of points with a curve is to use cubic splines. We are given a set f.xi; yi/ W i D 0; 1; : : : ; ng of n C 1 point-value
pairs, where x0 < x1 <    < xn.
We wish to ﬁt a piecewise-cubic curve
(spline) f .x/ to the points. That is, the curve f .x/ is made up of n cubic polynomials fi.x/ D ai C bix C cix2 C dix3 for i D 0; 1; : : : ; n  1, where if x falls in

Problems for Chapter 28
the range xi  x  xiC1, then the value of the curve is given by f .x/ D fi.xxi/.
The points xi at which the cubic polynomials are “pasted” together are called knots.
For simplicity, we shall assume that xi D i for i D 0; 1; : : : ; n.
To ensure continuity of f .x/, we require that
f .xi/
D
fi.0/
D
yi ;
f .xiC1/
D
fi.1/
D
yiC1
for i D 0; 1; : : : ; n  1. To ensure that f .x/ is sufﬁciently smooth, we also insist
that the ﬁrst derivative be continuous at each knot:
f 0.xiC1/ D f 0
i .1/ D f 0
iC1.0/
for i D 0; 1; : : : ; n  2.
a. Suppose that for i D 0; 1; : : : ; n, we are given not only the point-value pairs
f.xi; yi/g but also the ﬁrst derivatives Di D f 0.xi/ at each knot. Express each
coefﬁcient ai, bi, ci, and di in terms of the values yi, yiC1, Di, and DiC1.
(Remember that xi D i.) How quickly can we compute the 4n coefﬁcients
from the point-value pairs and ﬁrst derivatives?
The question remains of how to choose the ﬁrst derivatives of f .x/ at the knots.
One method is to require the second derivatives to be continuous at the knots:
f 00.xiC1/ D f 00
i .1/ D f 00
iC1.0/
for i D 0; 1; : : : ; n  2. At the ﬁrst and last knots, we assume that f 00.x0/ D
f 00
0 .0/ D 0 and f 00.xn/ D f 00
n1.1/ D 0; these assumptions make f .x/ a natural
cubic spline.
b. Use the continuity constraints on the second derivative to show that for i D
1; 2; : : : ; n  1,
Di1 C 4Di C DiC1 D 3.yiC1  yi1/ :
(28.21)
c. Show that
2D0 C D1
D
3.y1  y0/ ;
(28.22)
Dn1 C 2Dn
D
3.yn  yn1/ :
(28.23)
d. Rewrite equations (28.21)–(28.23) as a matrix equation involving the vector
D D hD0; D1; : : : ; Dni of unknowns. What attributes does the matrix in your
equation have?
e. Argue that a natural cubic spline can interpolate a set of n C 1 point-value pairs
in O.n/ time (see Problem 28-1).

f.
Show how to determine a natural cubic spline that interpolates a set of n C 1
points .xi; yi/ satisfying x0 < x1 <    < xn, even when xi is not necessarily
equal to i. What matrix equation must your method solve, and how quickly
does your algorithm run?
Chapter notes
Many excellent texts describe numerical and scientiﬁc computation in much greater
detail than we have room for here. The following are especially readable: George
and Liu [132], Golub and Van Loan [144], Press, Teukolsky, Vetterling, and Flannery [283, 284], and Strang [323, 324].
Golub and Van Loan [144] discuss numerical stability. They show why det.A/
is not necessarily a good indicator of the stability of a matrix A, proposing instead
to use kAk1 kA1k1, where kAk1 D max1in
Pn
jD1 jaijj. They also address
the question of how to compute this value without actually computing A1.
Gaussian elimination, upon which the LU and LUP decompositions are based,
was the ﬁrst systematic method for solving linear systems of equations. It was also
one of the earliest numerical algorithms. Although it was known earlier, its discovery is commonly attributed to C. F. Gauss (1777–1855). In his famous paper
[325], Strassen showed that an n	n matrix can be inverted in O.nlg 7/ time. Winograd [358] originally proved that matrix multiplication is no harder than matrix
inversion, and the converse is due to Aho, Hopcroft, and Ullman [5].
Another important matrix decomposition is the singular value decomposition,
or SVD. The SVD factors an m 	 n matrix A into A D Q1†QT
2, where † is an
m	n matrix with nonzero values only on the diagonal, Q1 is m	m with mutually
orthonormal columns, and Q2 is n 	 n, also with mutually orthonormal columns.
Two vectors are orthonormal if their inner product is 0 and each vector has a norm
of 1. The books by Strang [323, 324] and Golub and Van Loan [144] contain good
treatments of the SVD.
Strang [324] has an excellent presentation of symmetric positive-deﬁnite matrices and of linear algebra in general.
