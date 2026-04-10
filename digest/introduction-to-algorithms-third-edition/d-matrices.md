# D Matrices

D
Matrices
Matrices arise in numerous applications, including, but by no means limited to,
scientiﬁc computing. If you have seen matrices before, much of the material in this
appendix will be familiar to you, but some of it might be new. Section D.1 covers
basic matrix deﬁnitions and operations, and Section D.2 presents some basic matrix
properties.
D.1
Matrices and matrix operations
In this section, we review some basic concepts of matrix theory and some fundamental properties of matrices.
Matrices and vectors
A matrix is a rectangular array of numbers. For example,
A
D
 a11
a12
a13
a21
a22
a23

D
 1

(D.1)
is a 2 	 3 matrix A D .aij/, where for i D 1; 2 and j D 1; 2; 3, we denote the
element of the matrix in row i and column j by aij. We use uppercase letters
to denote matrices and corresponding subscripted lowercase letters to denote their
elements. We denote the set of all m	n matrices with real-valued entries by Rmn
and, in general, the set of m 	 n matrices with entries drawn from a set S by S mn.
The transpose of a matrix A is the matrix AT obtained by exchanging the rows
and columns of A. For the matrix A of equation (D.1),

Appendix D
Matrices
AT D


:
A vector is a one-dimensional array of numbers. For example,
x D


is a vector of size 3. We sometimes call a vector of length n an n-vector. We
use lowercase letters to denote vectors, and we denote the ith element of a size-n
vector x by xi, for i D 1; 2; : : : ; n. We take the standard form of a vector to be
as a column vector equivalent to an n 	 1 matrix; the corresponding row vector is
obtained by taking the transpose:
xT D . 2
5 / :
The unit vector ei is the vector whose ith element is 1 and all of whose other
elements are 0. Usually, the size of a unit vector is clear from the context.
A zero matrix is a matrix all of whose entries are 0. Such a matrix is often
denoted 0, since the ambiguity between the number 0 and a matrix of 0s is usually
easily resolved from context. If a matrix of 0s is intended, then the size of the
matrix also needs to be derived from the context.
Square matrices
Square n 	 n matrices arise frequently. Several special cases of square matrices
are of particular interest:
1. A diagonal matrix has aij D 0 whenever i ¤ j . Because all of the off-diagonal
elements are zero, we can specify the matrix by listing the elements along the
diagonal:
diag.a11; a22; : : : ; ann/ D
˙
a11
a22
:::
:::
:::
:::
ann

:
2. The n 	 n identity matrix In is a diagonal matrix with 1s along the diagonal:
In
D
diag.1; 1; : : : ; 1/
D
˙
:::
:::
:::
:::

:

D.1
Matrices and matrix operations
When I appears without a subscript, we derive its size from the context. The ith
column of an identity matrix is the unit vector ei.
3. A tridiagonal matrix T is one for which tij D 0 if ji  j j > 1. Nonzero entries
appear only on the main diagonal, immediately above the main diagonal (ti;iC1
for i D 1; 2; : : : ; n  1), or immediately below the main diagonal (tiC1;i for
i D 1; 2; : : : ; n  1):
T D

t11
t12
t21
t22
t23
t32
t33
t34
:::
:::
:::
:::
:::
:::
:::
:::
tn2;n2
tn2;n1
tn1;n2
tn1;n1
tn1;n
tn;n1
tnn
˘
:
4. An upper-triangular matrix U is one for which uij D 0 if i > j . All entries
below the diagonal are zero:
U D
˙
u11
u12
u1n
u22
u2n
:::
:::
:::
:::
unn

:
An upper-triangular matrix is unit upper-triangular if it has all 1s along the
diagonal.
5. A lower-triangular matrix L is one for which lij D 0 if i < j . All entries
above the diagonal are zero:
L D
˙
l11
l21
l22
:::
:::
:::
:::
ln1
ln2
lnn

:
A lower-triangular matrix is unit lower-triangular if it has all 1s along the
diagonal.

Appendix D
Matrices
6. A permutation matrix P has exactly one 1 in each row or column, and 0s
elsewhere. An example of a permutation matrix is
P D
ˇ

:
Such a matrix is called a permutation matrix because multiplying a vector x
by a permutation matrix has the effect of permuting (rearranging) the elements
of x. Exercise D.1-4 explores additional properties of permutation matrices.
7. A symmetric matrix A satisﬁes the condition A D AT. For example,


is a symmetric matrix.
Basic matrix operations
The elements of a matrix or vector are numbers from a number system, such as
the real numbers, the complex numbers, or integers modulo a prime. The number
system deﬁnes how to add and multiply numbers. We can extend these deﬁnitions
to encompass addition and multiplication of matrices.
We deﬁne matrix addition as follows. If A D .aij/ and B D .bij/ are m 	 n
matrices, then their matrix sum C D .cij/ D ACB is the m	n matrix deﬁned by
cij D aij C bij
for i D 1; 2; : : : ; m and j D 1; 2; : : : ; n. That is, matrix addition is performed
componentwise. A zero matrix is the identity for matrix addition:
A C 0 D A D 0 C A :
If  is a number and A D .aij/ is a matrix, then A D .aij/ is the scalar
multiple of A obtained by multiplying each of its elements by . As a special case,
we deﬁne the negative of a matrix A D .aij/ to be 1  A D A, so that the ij th
entry of A is aij. Thus,
A C .A/ D 0 D .A/ C A :

D.1
Matrices and matrix operations
We use the negative of a matrix to deﬁne matrix subtraction: A  B D A C .B/.
We deﬁne matrix multiplication as follows. We start with two matrices A and B
that are compatible in the sense that the number of columns of A equals the number
of rows of B. (In general, an expression containing a matrix product AB is always
assumed to imply that matrices A and B are compatible.) If A D .aik/ is an m 	 n
matrix and B D .bkj/ is an n 	 p matrix, then their matrix product C D AB is the
m 	 p matrix C D .cij/, where
cij D
n
X
kD1
aikbkj
(D.2)
for i D 1; 2; : : : ; m and j D 1; 2; : : : ; p. The procedure SQUARE-MATRIXMULTIPLY in Section 4.2 implements matrix multiplication in the straightforward manner based on equation (D.2), assuming that the matrices are square:
m D n D p.
To multiply n 	 n matrices, SQUARE-MATRIX-MULTIPLY performs n3 multiplications and n2.n  1/ additions, and so its running time is ‚.n3/.
Matrices have many (but not all) of the algebraic properties typical of numbers.
Identity matrices are identities for matrix multiplication:
ImA D AIn D A
for any m 	 n matrix A. Multiplying by a zero matrix gives a zero matrix:
A 0 D 0 :
Matrix multiplication is associative:
A.BC/ D .AB/C
for compatible matrices A, B, and C. Matrix multiplication distributes over addition:
A.B C C/
D
AB C AC ;
.B C C/D
D
BD C CD :
For n > 1, multiplication of n 	 n matrices is not commutative. For example, if
A D
 0

and B D
 0

, then
AB D
 1

and
BA D
 0

:

Appendix D
Matrices
We deﬁne matrix-vector products or vector-vector products as if the vector were
the equivalent n 	 1 matrix (or a 1 	 n matrix, in the case of a row vector). Thus,
if A is an m 	 n matrix and x is an n-vector, then Ax is an m-vector. If x and y
are n-vectors, then
xTy D
n
X
iD1
xiyi
is a number (actually a 1 	 1 matrix) called the inner product of x and y. The matrix xyT is an n	n matrix Z called the outer product of x and y, with ´ij D xiyj.
The (euclidean) norm kxk of an n-vector x is deﬁned by
kxk
D
.x2
1 C x2
2 C    C x2
n/1=2
D
.xTx/1=2 :
Thus, the norm of x is its length in n-dimensional euclidean space.

## Exercises

D.1-1
Show that if A and B are symmetric n 	 n matrices, then so are A C B and A  B.
D.1-2
Prove that .AB/T D BTAT and that ATA is always a symmetric matrix.
D.1-3
Prove that the product of two lower-triangular matrices is lower-triangular.
D.1-4
Prove that if P is an n 	 n permutation matrix and A is an n 	 n matrix, then the
matrix product PA is A with its rows permuted, and the matrix product AP is A
with its columns permuted. Prove that the product of two permutation matrices is
a permutation matrix.
D.2
Basic matrix properties
In this section, we deﬁne some basic properties pertaining to matrices: inverses,
linear dependence and independence, rank, and determinants. We also deﬁne the
class of positive-deﬁnite matrices.

D.2
Basic matrix properties
Matrix inverses, ranks, and determinants
We deﬁne the inverse of an n 	 n matrix A to be the n 	 n matrix, denoted A1 (if
it exists), such that AA1 D In D A1A. For example,
 1
1
D
 0
1

:
Many nonzero n 	 n matrices do not have inverses. A matrix without an inverse is
called noninvertible, or singular. An example of a nonzero singular matrix is
 1

:
If a matrix has an inverse, it is called invertible, or nonsingular. Matrix inverses,
when they exist, are unique. (See Exercise D.2-1.) If A and B are nonsingular
n 	 n matrices, then
.BA/1 D A1B1 :
The inverse operation commutes with the transpose operation:
.A1/T D .AT/1 :
The vectors x1; x2; : : : ; xn are linearly dependent if there exist coefﬁcients
c1; c2; : : : ; cn, not all of which are zero, such that c1x1 C c2x2 C    C cnxn D 0.
The row vectors x1 D . 1
3 /, x2 D . 2
4 /, and x3 D . 4
9 / are
linearly dependent, for example, since 2x1 C 3x2  2x3 D 0. If vectors are not
linearly dependent, they are linearly independent. For example, the columns of an
identity matrix are linearly independent.
The column rank of a nonzero m 	 n matrix A is the size of the largest set
of linearly independent columns of A. Similarly, the row rank of A is the size
of the largest set of linearly independent rows of A. A fundamental property of
any matrix A is that its row rank always equals its column rank, so that we can
simply refer to the rank of A. The rank of an m 	 n matrix is an integer between 0
and min.m; n/, inclusive. (The rank of a zero matrix is 0, and the rank of an n 	 n
identity matrix is n.) An alternate, but equivalent and often more useful, deﬁnition
is that the rank of a nonzero m 	 n matrix A is the smallest number r such that
there exist matrices B and C of respective sizes m 	 r and r 	 n such that
A D BC :
A square n 	 n matrix has full rank if its rank is n. An m 	 n matrix has full
column rank if its rank is n. The following theorem gives a fundamental property
of ranks.

Appendix D
Matrices
Theorem D.1
A square matrix has full rank if and only if it is nonsingular.
A null vector for a matrix A is a nonzero vector x such that Ax D 0. The
following theorem (whose proof is left as Exercise D.2-7) and its corollary relate
the notions of column rank and singularity to null vectors.
Theorem D.2
A matrix A has full column rank if and only if it does not have a null vector.
Corollary D.3
A square matrix A is singular if and only if it has a null vector.
The ij th minor of an n	n matrix A, for n > 1, is the .n1/	.n1/ matrix AŒij
obtained by deleting the ith row and j th column of A. We deﬁne the determinant
of an n 	 n matrix A recursively in terms of its minors by
det.A/ D
‚
a11
if n D 1 ;
n
X
jD1
.1/1Cja1j det.AŒ1j/
if n > 1 :
The term .1/iCj det.AŒij/ is known as the cofactor of the element aij.
The following theorems, whose proofs are omitted here, express fundamental
properties of the determinant.
Theorem D.4 (Determinant properties)
The determinant of a square matrix A has the following properties:

If any row or any column of A is zero, then det.A/ D 0.

The determinant of A is multiplied by  if the entries of any one row (or any
one column) of A are all multiplied by .

The determinant of A is unchanged if the entries in one row (respectively, column) are added to those in another row (respectively, column).

The determinant of A equals the determinant of AT.

The determinant of A is multiplied by 1 if any two rows (or any two columns)
are exchanged.
Also, for any square matrices A and B, we have det.AB/ D det.A/ det.B/.

D.2
Basic matrix properties
Theorem D.5
An n 	 n matrix A is singular if and only if det.A/ D 0.
Positive-deﬁnite matrices
Positive-deﬁnite matrices play an important role in many applications. An n 	 n
matrix A is positive-deﬁnite if xTAx
> 0 for all n-vectors x
¤ 0.
For
example, the identity matrix is positive-deﬁnite, since for any nonzero vector
x D . x1
x2
xn /T,
xTInx
D
xTx
D
n
X
iD1
x2
i
>
0 :
Matrices that arise in applications are often positive-deﬁnite due to the following
theorem.
Theorem D.6
For any matrix A with full column rank, the matrix ATA is positive-deﬁnite.
Proof
We must show that xT.ATA/x > 0 for any nonzero vector x. For any
vector x,
xT.ATA/x
D
.Ax/T.Ax/
(by Exercise D.1-2)
D
kAxk2 :
Note that kAxk2 is just the sum of the squares of the elements of the vector Ax.
Therefore, kAxk2  0. If kAxk2 D 0, every element of Ax is 0, which is to say
Ax D 0. Since A has full column rank, Ax D 0 implies x D 0, by Theorem D.2.
Hence, ATA is positive-deﬁnite.
Section 28.3 explores other properties of positive-deﬁnite matrices.

## Exercises

D.2-1
Prove that matrix inverses are unique, that is, if B and C are inverses of A, then
B D C.
D.2-2
Prove that the determinant of a lower-triangular or upper-triangular matrix is equal
to the product of its diagonal elements. Prove that the inverse of a lower-triangular
matrix, if it exists, is lower-triangular.

Appendix D
Matrices
D.2-3
Prove that if P is a permutation matrix, then P is invertible, its inverse is P T,
and P T is a permutation matrix.
D.2-4
Let A and B be n 	 n matrices such that AB D I. Prove that if A0 is obtained
from A by adding row j into row i, then subtracting column i from column j of B
yields the inverse B0 of A0.
D.2-5
Let A be a nonsingular n 	 n matrix with complex entries. Show that every entry
of A1 is real if and only if every entry of A is real.
D.2-6
Show that if A is a nonsingular, symmetric, n 	 n matrix, then A1 is symmetric.
Show that if B is an arbitrary m 	 n matrix, then the m 	 m matrix given by the
product BABT is symmetric.
D.2-7
Prove Theorem D.2. That is, show that a matrix A has full column rank if and only
if Ax D 0 implies x D 0. (Hint: Express the linear dependence of one column on
the others as a matrix-vector equation.)
D.2-8
Prove that for any two compatible matrices A and B,
rank.AB/  min.rank.A/; rank.B// ;
where equality holds if either A or B is a nonsingular square matrix. (Hint: Use
the alternate deﬁnition of the rank of a matrix.)

## Problems

D-1
Vandermonde matrix
Given numbers x0; x1; : : : ; xn1, prove that the determinant of the Vandermonde
matrix
V.x0; x1; : : : ; xn1/ D
˙ 1
x0
x2
xn1
x1
x2
xn1
:::
:::
:::
:::
:::
xn1
x2
n1
xn1
n1


Problems for Appendix D
is
det.V.x0; x1; : : : ; xn1// D
Y
0j<kn1
.xk  xj/ :
(Hint: Multiply column i by x0 and add it to column i C 1 for i D n  1;
n  2; : : : ; 1, and then use induction.)
D-2
Permutations deﬁned by matrix-vector multiplication over GF.2/
One class of permutations of the integers in the set Sn D f0; 1; 2; : : : ; 2n  1g is
deﬁned by matrix multiplication over GF.2/. For each integer x in Sn, we view its
binary representation as an n-bit vector

x0
x1
x2
:::
xn1

;
where x D Pn1
iD0 xi2i. If A is an n 	 n matrix in which each entry is either 0
or 1, then we can deﬁne a permutation mapping each value x in Sn to the number
whose binary representation is the matrix-vector product Ax. Here, we perform
all arithmetic over GF.2/: all values are either 0 or 1, and with one exception the
usual rules of addition and multiplication apply. The exception is that 1 C 1 D 0.
You can think of arithmetic over GF.2/ as being just like regular integer arithmetic,
except that you use only the least signiﬁcant bit.
As an example, for S2 D f0; 1; 2; 3g, the matrix
A D
 1

deﬁnes the following permutation A: A.0/ D 0, A.1/ D 3, A.2/ D 2,
A.3/ D 1. To see why A.3/ D 1, observe that, working in GF.2/,
A.3/
D
 1
 1

D
 1  1 C 0  1
1  1 C 1  1

D
 1

;
which is the binary representation of 1.

Appendix D
Matrices
For the remainder of this problem, we work over GF.2/, and all matrix and
vector entries are 0 or 1. We deﬁne the rank of a 0-1 matrix (a matrix for which
each entry is either 0 or 1) over GF.2/ the same as for a regular matrix, but with all
arithmetic that determines linear independence performed over GF.2/. We deﬁne
the range of an n 	 n 0-1 matrix A by
R.A/ D fy W y D Ax for some x 2 Sng ;
so that R.A/ is the set of numbers in Sn that we can produce by multiplying each
value x in Sn by A.
a. If r is the rank of matrix A, prove that jR.A/j D 2r. Conclude that A deﬁnes a
permutation on Sn only if A has full rank.
For a given n 	 n matrix A and a given value y 2 R.A/, we deﬁne the preimage
of y by
P .A; y/ D fx W Ax D yg ;
so that P .A; y/ is the set of values in Sn that map to y when multiplied by A.
b. If r is the rank of n 	 n matrix A and y 2 R.A/, prove that jP .A; y/j D 2nr.
Let 0  m  n, and suppose we partition the set Sn into blocks of consecutive numbers, where the ith block consists of the 2m numbers i2m; i2m C 1;
i2m C 2; : : : ; .i C 1/2m  1. For any subset S  Sn, deﬁne B.S; m/ to be the
set of size-2m blocks of Sn containing some element of S. As an example, when
n D 3, m D 1, and S D f1; 4; 5g, then B.S; m/ consists of blocks 0 (since 1 is in
the 0th block) and 2 (since both 4 and 5 are in block 2).
c. Let r be the rank of the lower left .n  m/ 	 m submatrix of A, that is, the
matrix formed by taking the intersection of the bottom n  m rows and the
leftmost m columns of A. Let S be any size-2m block of Sn, and let S 0 D
fy W y D Ax for some x 2 Sg. Prove that jB.S 0; m/j D 2r and that for each
block in B.S 0; m/, exactly 2mr numbers in S map to that block.
Because multiplying the zero vector by any matrix yields a zero vector, the set
of permutations of Sn deﬁned by multiplying by n 	 n 0-1 matrices with full rank
over GF.2/ cannot include all permutations of Sn. Let us extend the class of permutations deﬁned by matrix-vector multiplication to include an additive term, so
that x 2 Sn maps to Ax C c, where c is an n-bit vector and addition is performed
over GF.2/. For example, when
A D
 1


Notes for Appendix D
and
c D
 0

;
we get the following permutation A;c: A;c.0/ D 2, A;c.1/ D 1, A;c.2/ D 0,
A;c.3/ D 3. We call any permutation that maps x 2 Sn to Ax C c, for some n 	 n
0-1 matrix A with full rank and some n-bit vector c, a linear permutation.
d. Use a counting argument to show that the number of linear permutations of Sn
is much less than the number of permutations of Sn.
e. Give an example of a value of n and a permutation of Sn that cannot be achieved
by any linear permutation. (Hint: For a given permutation, think about how
multiplying a matrix by a unit vector relates to the columns of the matrix.)
Appendix notes
Linear-algebra textbooks provide plenty of background information on matrices.
The books by Strang [323, 324] are particularly good.
