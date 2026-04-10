# 3 Growth of Functions

3
Growth of Functions
The order of growth of the running time of an algorithm, deﬁned in Chapter 2,
gives a simple characterization of the algorithm’s efﬁciency and also allows us to
compare the relative performance of alternative algorithms. Once the input size n
becomes large enough, merge sort, with its ‚.n lg n/ worst-case running time,
beats insertion sort, whose worst-case running time is ‚.n2/. Although we can
sometimes determine the exact running time of an algorithm, as we did for insertion
sort in Chapter 2, the extra precision is not usually worth the effort of computing
it. For large enough inputs, the multiplicative constants and lower-order terms of
an exact running time are dominated by the effects of the input size itself.
When we look at input sizes large enough to make only the order of growth of
the running time relevant, we are studying the asymptotic efﬁciency of algorithms.
That is, we are concerned with how the running time of an algorithm increases with
the size of the input in the limit, as the size of the input increases without bound.
Usually, an algorithm that is asymptotically more efﬁcient will be the best choice
for all but very small inputs.
This chapter gives several standard methods for simplifying the asymptotic anal-
ysis of algorithms. The next section begins by deﬁning several types of “asymp-
totic notation,” of which we have already seen an example in ‚-notation. We then
present several notational conventions used throughout this book, and ﬁnally we
review the behavior of functions that commonly arise in the analysis of algorithms.
3.1
Asymptotic notation
The notations we use to describe the asymptotic running time of an algorithm
are deﬁned in terms of functions whose domains are the set of natural numbers
N D f0; 1; 2; : : :g. Such notations are convenient for describing the worst-case
running-time function T .n/, which usually is deﬁned only on integer input sizes.
We sometimes ﬁnd it convenient, however, to abuse asymptotic notation in a va-

44
Chapter 3
Growth of Functions
riety of ways. For example, we might extend the notation to the domain of real
numbers or, alternatively, restrict it to a subset of the natural numbers. We should
make sure, however, to understand the precise meaning of the notation so that when
we abuse, we do not misuse it. This section deﬁnes the basic asymptotic notations
and also introduces some common abuses.
Asymptotic notation, functions, and running times
We will use asymptotic notation primarily to describe the running times of algo-
rithms, as when we wrote that insertion sort’s worst-case running time is ‚.n2/.
Asymptotic notation actually applies to functions, however. Recall that we charac-
terized insertion sort’s worst-case running time as an2CbnCc, for some constants
a, b, and c. By writing that insertion sort’s running time is ‚.n2/, we abstracted
away some details of this function. Because asymptotic notation applies to func-
tions, what we were writing as ‚.n2/ was the function an2 C bn C c, which in
that case happened to characterize the worst-case running time of insertion sort.
In this book, the functions to which we apply asymptotic notation will usually
characterize the running times of algorithms. But asymptotic notation can apply to
functions that characterize some other aspect of algorithms (the amount of space
they use, for example), or even to functions that have nothing whatsoever to do
with algorithms.
Even when we use asymptotic notation to apply to the running time of an al-
gorithm, we need to understand which running time we mean. Sometimes we are
interested in the worst-case running time. Often, however, we wish to characterize
the running time no matter what the input. In other words, we often wish to make
a blanket statement that covers all inputs, not just the worst case. We shall see
asymptotic notations that are well suited to characterizing running times no matter
what the input.
‚-notation
In Chapter 2, we found that the worst-case running time of insertion sort is
T .n/ D ‚.n2/. Let us deﬁne what this notation means. For a given function g.n/,
we denote by ‚.g.n// the set of functions
‚.g.n// D ff .n/ W there exist positive constants c1, c2, and n0 such that
0  c1g.n/  f .n/  c2g.n/ for all n  n0g :1
1Within set notation, a colon means “such that.”

3.1
Asymptotic notation
45
(b)
(c)
(a)
n
n
n
n0
n0
n0
f .n/ D ‚.g.n//
f .n/ D O.g.n//
f .n/ D .g.n//
f .n/
f .n/
f .n/
cg.n/
cg.n/
c1g.n/
c2g.n/
Figure 3.1
Graphic examples of the ‚, O, and  notations. In each part, the value of n0 shown
is the minimum possible value; any greater value would also work. (a) ‚-notation bounds a func-
tion to within constant factors. We write f .n/ D ‚.g.n// if there exist positive constants n0, c1,
and c2 such that at and to the right of n0, the value of f .n/ always lies between c1g.n/ and c2g.n/
inclusive. (b) O-notation gives an upper bound for a function to within a constant factor. We write
f .n/ D O.g.n// if there are positive constants n0 and c such that at and to the right of n0, the value
of f .n/ always lies on or below cg.n/. (c) -notation gives a lower bound for a function to within
a constant factor. We write f .n/ D .g.n// if there are positive constants n0 and c such that at and
to the right of n0, the value of f .n/ always lies on or above cg.n/.
A function f .n/ belongs to the set ‚.g.n// if there exist positive constants c1
and c2 such that it can be “sandwiched” between c1g.n/ and c2g.n/, for sufﬁ-
ciently large n. Because ‚.g.n// is a set, we could write “f .n/ 2 ‚.g.n//”
to indicate that f .n/ is a member of ‚.g.n//. Instead, we will usually write
“f .n/ D ‚.g.n//” to express the same notion. You might be confused because
we abuse equality in this way, but we shall see later in this section that doing so
has its advantages.
Figure 3.1(a) gives an intuitive picture of functions f .n/ and g.n/, where
f .n/ D ‚.g.n//. For all values of n at and to the right of n0, the value of f .n/
lies at or above c1g.n/ and at or below c2g.n/. In other words, for all n  n0, the
function f .n/ is equal to g.n/ to within a constant factor. We say that g.n/ is an
asymptotically tight bound for f .n/.
The deﬁnition of ‚.g.n// requires that every member f .n/ 2 ‚.g.n// be
asymptotically nonnegative, that is, that f .n/ be nonnegative whenever n is suf-
ﬁciently large. (An asymptotically positive function is one that is positive for all
sufﬁciently large n.) Consequently, the function g.n/ itself must be asymptotically
nonnegative, or else the set ‚.g.n// is empty. We shall therefore assume that every
function used within ‚-notation is asymptotically nonnegative. This assumption
holds for the other asymptotic notations deﬁned in this chapter as well.

46
Chapter 3
Growth of Functions
In Chapter 2, we introduced an informal notion of ‚-notation that amounted
to throwing away lower-order terms and ignoring the leading coefﬁcient of the
highest-order term. Let us brieﬂy justify this intuition by using the formal deﬁ-
nition to show that 1
2n2  3n D ‚.n2/. To do so, we must determine positive
constants c1, c2, and n0 such that
c1n2  1
2n2  3n  c2n2
for all n  n0. Dividing by n2 yields
c1  1
2  3
n  c2 :
We can make the right-hand inequality hold for any value of n  1 by choosing any
constant c2  1=2. Likewise, we can make the left-hand inequality hold for any
value of n  7 by choosing any constant c1  1=14. Thus, by choosing c1 D 1=14,
c2 D 1=2, and n0 D 7, we can verify that 1
2n2  3n D ‚.n2/. Certainly, other
choices for the constants exist, but the important thing is that some choice exists.
Note that these constants depend on the function 1
2n2  3n; a different function
belonging to ‚.n2/ would usually require different constants.
We can also use the formal deﬁnition to verify that 6n3 ¤ ‚.n2/. Suppose
for the purpose of contradiction that c2 and n0 exist such that 6n3  c2n2 for
all n  n0. But then dividing by n2 yields n  c2=6, which cannot possibly hold
for arbitrarily large n, since c2 is constant.
Intuitively, the lower-order terms of an asymptotically positive function can be
ignored in determining asymptotically tight bounds because they are insigniﬁcant
for large n. When n is large, even a tiny fraction of the highest-order term suf-
ﬁces to dominate the lower-order terms. Thus, setting c1 to a value that is slightly
smaller than the coefﬁcient of the highest-order term and setting c2 to a value that
is slightly larger permits the inequalities in the deﬁnition of ‚-notation to be sat-
isﬁed. The coefﬁcient of the highest-order term can likewise be ignored, since it
only changes c1 and c2 by a constant factor equal to the coefﬁcient.
As an example, consider any quadratic function f .n/ D an2 C bn C c, where
a, b, and c are constants and a > 0. Throwing away the lower-order terms and
ignoring the constant yields f .n/ D ‚.n2/. Formally, to show the same thing, we
take the constants c1 D a=4, c2 D 7a=4, and n0 D 2  max.jbj =a;
p
jcj =a/. You
may verify that 0  c1n2  an2 C bn C c  c2n2 for all n  n0. In general,
for any polynomial p.n/ D Pd
iD0 aini, where the ai are constants and ad > 0, we
have p.n/ D ‚.nd/ (see Problem 3-1).
Since any constant is a degree-0 polynomial, we can express any constant func-
tion as ‚.n0/, or ‚.1/. This latter notation is a minor abuse, however, because the

3.1
Asymptotic notation
47
expression does not indicate what variable is tending to inﬁnity.2 We shall often
use the notation ‚.1/ to mean either a constant or a constant function with respect
to some variable.
O-notation
The ‚-notation asymptotically bounds a function from above and below. When
we have only an asymptotic upper bound, we use O-notation. For a given func-
tion g.n/, we denote by O.g.n// (pronounced “big-oh of g of n” or sometimes
just “oh of g of n”) the set of functions
O.g.n// D ff .n/ W there exist positive constants c and n0 such that
0  f .n/  cg.n/ for all n  n0g :
We use O-notation to give an upper bound on a function, to within a constant
factor. Figure 3.1(b) shows the intuition behind O-notation. For all values n at and
to the right of n0, the value of the function f .n/ is on or below cg.n/.
We write f .n/ D O.g.n// to indicate that a function f .n/ is a member of the
set O.g.n//. Note that f .n/ D ‚.g.n// implies f .n/ D O.g.n//, since ‚-
notation is a stronger notion than O-notation. Written set-theoretically, we have
‚.g.n//  O.g.n//. Thus, our proof that any quadratic function an2 C bn C c,
where a > 0, is in ‚.n2/ also shows that any such quadratic function is in O.n2/.
What may be more surprising is that when a > 0, any linear function an C b is
in O.n2/, which is easily veriﬁed by taking c D a C jbj and n0 D max.1; b=a/.
If you have seen O-notation before, you might ﬁnd it strange that we should
write, for example, n D O.n2/. In the literature, we sometimes ﬁnd O-notation
informally describing asymptotically tight bounds, that is, what we have deﬁned
using ‚-notation. In this book, however, when we write f .n/ D O.g.n//, we
are merely claiming that some constant multiple of g.n/ is an asymptotic upper
bound on f .n/, with no claim about how tight an upper bound it is. Distinguish-
ing asymptotic upper bounds from asymptotically tight bounds is standard in the
algorithms literature.
Using O-notation, we can often describe the running time of an algorithm
merely by inspecting the algorithm’s overall structure. For example, the doubly
nested loop structure of the insertion sort algorithm from Chapter 2 immediately
yields an O.n2/ upper bound on the worst-case running time: the cost of each it-
eration of the inner loop is bounded from above by O.1/ (constant), the indices i
2The real problem is that our ordinary notation for functions does not distinguish functions from
values. In -calculus, the parameters to a function are clearly speciﬁed: the function n2 could be
written as n:n2, or even r:r2. Adopting a more rigorous notation, however, would complicate
algebraic manipulations, and so we choose to tolerate the abuse.

48
Chapter 3
Growth of Functions
and j are both at most n, and the inner loop is executed at most once for each of
the n2 pairs of values for i and j .
Since O-notation describes an upper bound, when we use it to bound the worst-
case running time of an algorithm, we have a bound on the running time of the algo-
rithm on every input—the blanket statement we discussed earlier. Thus, the O.n2/
bound on worst-case running time of insertion sort also applies to its running time
on every input. The ‚.n2/ bound on the worst-case running time of insertion sort,
however, does not imply a ‚.n2/ bound on the running time of insertion sort on
every input. For example, we saw in Chapter 2 that when the input is already
sorted, insertion sort runs in ‚.n/ time.
Technically, it is an abuse to say that the running time of insertion sort is O.n2/,
since for a given n, the actual running time varies, depending on the particular
input of size n. When we say “the running time is O.n2/,” we mean that there is a
function f .n/ that is O.n2/ such that for any value of n, no matter what particular
input of size n is chosen, the running time on that input is bounded from above by
the value f .n/. Equivalently, we mean that the worst-case running time is O.n2/.
-notation
Just as O-notation provides an asymptotic upper bound on a function, -notation
provides an asymptotic lower bound.
For a given function g.n/, we denote
by .g.n// (pronounced “big-omega of g of n” or sometimes just “omega of g
of n”) the set of functions
.g.n// D ff .n/ W there exist positive constants c and n0 such that
0  cg.n/  f .n/ for all n  n0g :
Figure 3.1(c) shows the intuition behind -notation. For all values n at or to the
right of n0, the value of f .n/ is on or above cg.n/.
From the deﬁnitions of the asymptotic notations we have seen thus far, it is easy
to prove the following important theorem (see Exercise 3.1-5).
Theorem 3.1
For any two functions f .n/ and g.n/, we have f .n/ D ‚.g.n// if and only if
f .n/ D O.g.n// and f .n/ D .g.n//.
As an example of the application of this theorem, our proof that an2 C bn C c D
‚.n2/ for any constants a, b, and c, where a > 0, immediately implies that
an2 C bn C c D .n2/ and an2 CbnCc D O.n2/. In practice, rather than using
Theorem 3.1 to obtain asymptotic upper and lower bounds from asymptotically
tight bounds, as we did for this example, we usually use it to prove asymptotically
tight bounds from asymptotic upper and lower bounds.

3.1
Asymptotic notation
49
When we say that the running time (no modiﬁer) of an algorithm is .g.n//,
we mean that no matter what particular input of size n is chosen for each value
of n, the running time on that input is at least a constant times g.n/, for sufﬁciently
large n. Equivalently, we are giving a lower bound on the best-case running time
of an algorithm. For example, the best-case running time of insertion sort is .n/,
which implies that the running time of insertion sort is .n/.
The running time of insertion sort therefore belongs to both .n/ and O.n2/,
since it falls anywhere between a linear function of n and a quadratic function of n.
Moreover, these bounds are asymptotically as tight as possible: for instance, the
running time of insertion sort is not .n2/, since there exists an input for which
insertion sort runs in ‚.n/ time (e.g., when the input is already sorted). It is not
contradictory, however, to say that the worst-case running time of insertion sort
is .n2/, since there exists an input that causes the algorithm to take .n2/ time.
Asymptotic notation in equations and inequalities
We have already seen how asymptotic notation can be used within mathematical
formulas. For example, in introducing O-notation, we wrote “n D O.n2/.” We
might also write 2n2 C3nC1 D 2n2 C‚.n/. How do we interpret such formulas?
When the asymptotic notation stands alone (that is, not within a larger formula)
on the right-hand side of an equation (or inequality), as in n D O.n2/, we have
already deﬁned the equal sign to mean set membership: n 2 O.n2/. In general,
however, when asymptotic notation appears in a formula, we interpret it as stand-
ing for some anonymous function that we do not care to name. For example, the
formula 2n2 C 3n C 1 D 2n2 C ‚.n/ means that 2n2 C 3n C 1 D 2n2 C f .n/,
where f .n/ is some function in the set ‚.n/. In this case, we let f .n/ D 3n C 1,
which indeed is in ‚.n/.
Using asymptotic notation in this manner can help eliminate inessential detail
and clutter in an equation. For example, in Chapter 2 we expressed the worst-case
running time of merge sort as the recurrence
T .n/ D 2T .n=2/ C ‚.n/ :
If we are interested only in the asymptotic behavior of T .n/, there is no point in
specifying all the lower-order terms exactly; they are all understood to be included
in the anonymous function denoted by the term ‚.n/.
The number of anonymous functions in an expression is understood to be equal
to the number of times the asymptotic notation appears. For example, in the ex-
pression
n
X
iD1
O.i/ ;

50
Chapter 3
Growth of Functions
there is only a single anonymous function (a function of i). This expression is thus
not the same as O.1/ C O.2/ C    C O.n/, which doesn’t really have a clean
interpretation.
In some cases, asymptotic notation appears on the left-hand side of an equation,
as in
2n2 C ‚.n/ D ‚.n2/ :
We interpret such equations using the following rule: No matter how the anony-
mous functions are chosen on the left of the equal sign, there is a way to choose
the anonymous functions on the right of the equal sign to make the equation valid.
Thus, our example means that for any function f .n/ 2 ‚.n/, there is some func-
tion g.n/ 2 ‚.n2/ such that 2n2 C f .n/ D g.n/ for all n. In other words, the
right-hand side of an equation provides a coarser level of detail than the left-hand
side.
We can chain together a number of such relationships, as in
2n2 C 3n C 1
D
2n2 C ‚.n/
D
‚.n2/ :
We can interpret each equation separately by the rules above.
The ﬁrst equa-
tion says that there is some function f .n/ 2 ‚.n/ such that 2n2 C 3n C 1 D
2n2 C f .n/ for all n. The second equation says that for any function g.n/ 2 ‚.n/
(such as the f .n/ just mentioned), there is some function h.n/ 2 ‚.n2/ such
that 2n2 C g.n/ D h.n/ for all n.
Note that this interpretation implies that
2n2 C 3n C 1 D ‚.n2/, which is what the chaining of equations intuitively gives
us.
o-notation
The asymptotic upper bound provided by O-notation may or may not be asymp-
totically tight. The bound 2n2 D O.n2/ is asymptotically tight, but the bound
2n D O.n2/ is not. We use o-notation to denote an upper bound that is not asymp-
totically tight. We formally deﬁne o.g.n// (“little-oh of g of n”) as the set
o.g.n// D ff .n/ W for any positive constant c > 0, there exists a constant
n0 > 0 such that 0  f .n/ < cg.n/ for all n  n0g :
For example, 2n D o.n2/, but 2n2 ¤ o.n2/.
The deﬁnitions of O-notation and o-notation are similar. The main difference
is that in f .n/ D O.g.n//, the bound 0  f .n/  cg.n/ holds for some con-
stant c > 0, but in f .n/ D o.g.n//, the bound 0  f .n/ < cg.n/ holds for all
constants c > 0. Intuitively, in o-notation, the function f .n/ becomes insigniﬁcant
relative to g.n/ as n approaches inﬁnity; that is,

3.1
Asymptotic notation
51
lim
n!1
f .n/
g.n/ D 0 :
(3.1)
Some authors use this limit as a deﬁnition of the o-notation; the deﬁnition in this
book also restricts the anonymous functions to be asymptotically nonnegative.
!-notation
By analogy, !-notation is to -notation as o-notation is to O-notation. We use
!-notation to denote a lower bound that is not asymptotically tight. One way to
deﬁne it is by
f .n/ 2 !.g.n// if and only if g.n/ 2 o.f .n// :
Formally, however, we deﬁne !.g.n// (“little-omega of g of n”) as the set
!.g.n// D ff .n/ W for any positive constant c > 0, there exists a constant
n0 > 0 such that 0  cg.n/ < f .n/ for all n  n0g :
For example, n2=2 D !.n/, but n2=2 ¤ !.n2/. The relation f .n/ D !.g.n//
implies that
lim
n!1
f .n/
g.n/ D 1 ;
if the limit exists. That is, f .n/ becomes arbitrarily large relative to g.n/ as n
approaches inﬁnity.
Comparing functions
Many of the relational properties of real numbers apply to asymptotic comparisons
as well. For the following, assume that f .n/ and g.n/ are asymptotically positive.
Transitivity:
f .n/ D ‚.g.n// and g.n/ D ‚.h.n//
imply
f .n/ D ‚.h.n// ;
f .n/ D O.g.n// and g.n/ D O.h.n//
imply
f .n/ D O.h.n// ;
f .n/ D .g.n// and g.n/ D .h.n//
imply
f .n/ D .h.n// ;
f .n/ D o.g.n//
and g.n/ D o.h.n//
imply
f .n/ D o.h.n// ;
f .n/ D !.g.n// and g.n/ D !.h.n//
imply
f .n/ D !.h.n// :
Reﬂexivity:
f .n/
D
‚.f .n// ;
f .n/
D
O.f .n// ;
f .n/
D
.f .n// :

52
Chapter 3
Growth of Functions
Symmetry:
f .n/ D ‚.g.n// if and only if g.n/ D ‚.f .n// :
Transpose symmetry:
f .n/ D O.g.n// if and only if g.n/ D .f .n// ;
f .n/ D o.g.n//
if and only if g.n/ D !.f .n// :
Because these properties hold for asymptotic notations, we can draw an analogy
between the asymptotic comparison of two functions f and g and the comparison
of two real numbers a and b:
f .n/ D O.g.n//
is like
a  b ;
f .n/ D .g.n//
is like
a  b ;
f .n/ D ‚.g.n//
is like
a D b ;
f .n/ D o.g.n//
is like
a < b ;
f .n/ D !.g.n//
is like
a > b :
We say that f .n/ is asymptotically smaller than g.n/ if f .n/ D o.g.n//, and f .n/
is asymptotically larger than g.n/ if f .n/ D !.g.n//.
One property of real numbers, however, does not carry over to asymptotic nota-
tion:
Trichotomy: For any two real numbers a and b, exactly one of the following must
hold: a < b, a D b, or a > b.
Although any two real numbers can be compared, not all functions are asymptot-
ically comparable. That is, for two functions f .n/ and g.n/, it may be the case
that neither f .n/ D O.g.n// nor f .n/ D .g.n// holds. For example, we cannot
compare the functions n and n1Csin n using asymptotic notation, since the value of
the exponent in n1Csin n oscillates between 0 and 2, taking on all values in between.
Exercises
3.1-1
Let f .n/ and g.n/ be asymptotically nonnegative functions. Using the basic deﬁ-
nition of ‚-notation, prove that max.f .n/; g.n// D ‚.f .n/ C g.n//.
3.1-2
Show that for any real constants a and b, where b > 0,
.n C a/b D ‚.nb/ :
(3.2)

3.2
Standard notations and common functions
53
3.1-3
Explain why the statement, “The running time of algorithm A is at least O.n2/,” is
meaningless.
3.1-4
Is 2nC1 D O.2n/? Is 22n D O.2n/?
3.1-5
Prove Theorem 3.1.
3.1-6
Prove that the running time of an algorithm is ‚.g.n// if and only if its worst-case
running time is O.g.n// and its best-case running time is .g.n//.
3.1-7
Prove that o.g.n// \ !.g.n// is the empty set.
3.1-8
We can extend our notation to the case of two parameters n and m that can go to
inﬁnity independently at different rates. For a given function g.n; m/, we denote
by O.g.n; m// the set of functions
O.g.n; m// D ff .n; m/ W there exist positive constants c, n0, and m0
such that 0  f .n; m/  cg.n; m/
for all n  n0 or m  m0g :
Give corresponding deﬁnitions for .g.n; m// and ‚.g.n; m//.
3.2
Standard notations and common functions
This section reviews some standard mathematical functions and notations and ex-
plores the relationships among them. It also illustrates the use of the asymptotic
notations.
Monotonicity
A function f .n/ is monotonically increasing if m  n implies f .m/  f .n/.
Similarly, it is monotonically decreasing if m  n implies f .m/  f .n/. A
function f .n/ is strictly increasing if m < n implies f .m/ < f .n/ and strictly
decreasing if m < n implies f .m/ > f .n/.

54
Chapter 3
Growth of Functions
Floors and ceilings
For any real number x, we denote the greatest integer less than or equal to x by bxc
(read “the ﬂoor of x”) and the least integer greater than or equal to x by dxe (read
“the ceiling of x”). For all real x,
x  1 < bxc  x  dxe < x C 1 :
(3.3)
For any integer n,
dn=2e C bn=2c D n ;
and for any real number x  0 and integers a; b > 0,
dx=ae
b

D
l x
ab
m
;
(3.4)
bx=ac
b
	
D
j x
ab
k
;
(3.5)
la
b
m

a C .b  1/
b
;
(3.6)
ja
b
k

a  .b  1/
b
:
(3.7)
The ﬂoor function f .x/ D bxc is monotonically increasing, as is the ceiling func-
tion f .x/ D dxe.
Modular arithmetic
For any integer a and any positive integer n, the value a mod n is the remainder
(or residue) of the quotient a=n:
a mod n D a  n ba=nc :
(3.8)
It follows that
0  a mod n < n :
(3.9)
Given a well-deﬁned notion of the remainder of one integer when divided by an-
other, it is convenient to provide special notation to indicate equality of remainders.
If .a mod n/ D .b mod n/, we write a  b .mod n/ and say that a is equivalent
to b, modulo n. In other words, a  b .mod n/ if a and b have the same remain-
der when divided by n. Equivalently, a  b .mod n/ if and only if n is a divisor
of b  a. We write a 6 b .mod n/ if a is not equivalent to b, modulo n.

3.2
Standard notations and common functions
55
Polynomials
Given a nonnegative integer d, a polynomial in n of degree d is a function p.n/
of the form
p.n/ D
d
X
iD0
aini ;
where the constants a0; a1; : : : ; ad are the coefﬁcients of the polynomial and
ad ¤ 0. A polynomial is asymptotically positive if and only if ad > 0. For an
asymptotically positive polynomial p.n/ of degree d, we have p.n/ D ‚.nd/. For
any real constant a  0, the function na is monotonically increasing, and for any
real constant a  0, the function na is monotonically decreasing. We say that a
function f .n/ is polynomially bounded if f .n/ D O.nk/ for some constant k.
Exponentials
For all real a > 0, m, and n, we have the following identities:
a0
D
1 ;
a1
D
a ;
a1
D
1=a ;
.am/n
D
amn ;
.am/n
D
.an/m ;
aman
D
amCn :
For all n and a  1, the function an is monotonically increasing in n. When
convenient, we shall assume 00 D 1.
We can relate the rates of growth of polynomials and exponentials by the fol-
lowing fact. For all real constants a and b such that a > 1,
lim
n!1
nb
an D 0 ;
(3.10)
from which we can conclude that
nb D o.an/ :
Thus, any exponential function with a base strictly greater than 1 grows faster than
any polynomial function.
Using e to denote 2:71828 : : :, the base of the natural logarithm function, we
have for all real x,
ex D 1 C x C x2
2Š C x3
3Š C    D
1
X
iD0
xi
iŠ ;
(3.11)

56
Chapter 3
Growth of Functions
where “Š” denotes the factorial function deﬁned later in this section. For all real x,
we have the inequality
ex  1 C x ;
(3.12)
where equality holds only when x D 0. When jxj  1, we have the approximation
1 C x  ex  1 C x C x2 :
(3.13)
When x ! 0, the approximation of ex by 1 C x is quite good:
ex D 1 C x C ‚.x2/ :
(In this equation, the asymptotic notation is used to describe the limiting behavior
as x ! 0 rather than as x ! 1.) We have for all x,
lim
n!1

1 C x
n
n
D ex :
(3.14)
Logarithms
We shall use the following notations:
lg n
D
log2 n
(binary logarithm) ,
ln n
D
loge n
(natural logarithm) ,
lgk n
D
.lg n/k
(exponentiation) ,
lg lg n
D
lg.lg n/
(composition) .
An important notational convention we shall adopt is that logarithm functions will
apply only to the next term in the formula, so that lg n C k will mean .lg n/ C k
and not lg.n C k/. If we hold b > 1 constant, then for n > 0, the function logb n
is strictly increasing.
For all real a > 0, b > 0, c > 0, and n,
a
D
blogb a ;
logc.ab/
D
logc a C logc b ;
logb an
D
n logb a ;
logb a
D
logc a
logc b ;
(3.15)
logb.1=a/
D
 logb a ;
logb a
D
1
loga b ;
alogb c
D
clogb a ;
(3.16)
where, in each equation above, logarithm bases are not 1.

3.2
Standard notations and common functions
57
By equation (3.15), changing the base of a logarithm from one constant to an-
other changes the value of the logarithm by only a constant factor, and so we shall
often use the notation “lg n” when we don’t care about constant factors, such as in
O-notation. Computer scientists ﬁnd 2 to be the most natural base for logarithms
because so many algorithms and data structures involve splitting a problem into
two parts.
There is a simple series expansion for ln.1 C x/ when jxj < 1:
ln.1 C x/ D x  x2
2 C x3
3  x4
4 C x5
5     :
We also have the following inequalities for x > 1:
x
1 C x  ln.1 C x/  x ;
(3.17)
where equality holds only for x D 0.
We say that a function f .n/ is polylogarithmically bounded if f .n/ D O.lgk n/
for some constant k. We can relate the growth of polynomials and polylogarithms
by substituting lg n for n and 2a for a in equation (3.10), yielding
lim
n!1
lgb n
.2a/lg n D lim
n!1
lgb n
na
D 0 :
From this limit, we can conclude that
lgb n D o.na/
for any constant a > 0. Thus, any positive polynomial function grows faster than
any polylogarithmic function.
Factorials
The notation nŠ (read “n factorial”) is deﬁned for integers n  0 as
nŠ D
(
1
if n D 0 ;
n  .n  1/Š
if n > 0 :
Thus, nŠ D 1  2  3    n.
A weak upper bound on the factorial function is nŠ  nn, since each of the n
terms in the factorial product is at most n. Stirling’s approximation,
nŠ D
p
2n
n
e
n 
1 C ‚
1
n

;
(3.18)

58
Chapter 3
Growth of Functions
where e is the base of the natural logarithm, gives us a tighter upper bound, and a
lower bound as well. As Exercise 3.2-3 asks you to prove,
nŠ
D
o.nn/ ;
nŠ
D
!.2n/ ;
lg.nŠ/
D
‚.n lg n/ ;
(3.19)
where Stirling’s approximation is helpful in proving equation (3.19). The following
equation also holds for all n  1:
nŠ D
p
2n
n
e
n
e˛n
(3.20)
where
1
12n C 1 < ˛n <
1
12n :
(3.21)
Functional iteration
We use the notation f .i/.n/ to denote the function f .n/ iteratively applied i times
to an initial value of n. Formally, let f .n/ be a function over the reals. For non-
negative integers i, we recursively deﬁne
f .i/.n/ D
(
n
if i D 0 ;
f .f .i1/.n//
if i > 0 :
For example, if f .n/ D 2n, then f .i/.n/ D 2in.
The iterated logarithm function
We use the notation lg n (read “log star of n”) to denote the iterated logarithm, de-
ﬁned as follows. Let lg.i/ n be as deﬁned above, with f .n/ D lg n. Because the log-
arithm of a nonpositive number is undeﬁned, lg.i/ n is deﬁned only if lg.i1/ n > 0.
Be sure to distinguish lg.i/ n (the logarithm function applied i times in succession,
starting with argument n) from lgi n (the logarithm of n raised to the ith power).
Then we deﬁne the iterated logarithm function as
lg n D min
˚
i  0 W lg.i/ n  1

:
The iterated logarithm is a very slowly growing function:
lg 2
D
1 ;
lg 4
D
2 ;
lg 16
D
3 ;
lg 65536
D
4 ;
lg.265536/
D
5 :

3.2
Standard notations and common functions
59
Since the number of atoms in the observable universe is estimated to be about 1080,
which is much less than 265536, we rarely encounter an input size n such that
lg n > 5.
Fibonacci numbers
We deﬁne the Fibonacci numbers by the following recurrence:
F0
D
0 ;
F1
D
1 ;
(3.22)
Fi
D
Fi1 C Fi2
for i  2 :
Thus, each Fibonacci number is the sum of the two previous ones, yielding the
sequence
0; 1; 1; 2; 3; 5; 8; 13; 21; 34; 55; : : : :
Fibonacci numbers are related to the golden ratio  and to its conjugate y, which
are the two roots of the equation
x2 D x C 1
(3.23)
and are given by the following formulas (see Exercise 3.2-6):

D
1 C
p
5
2
(3.24)
D
1:61803 : : : ;
y
D
1 
p
5
2
D
:61803 : : : :
Speciﬁcally, we have
Fi D i  yi
p
5
;
which we can prove by induction (Exercise 3.2-7). Since
ˇˇy
ˇˇ < 1, we have
ˇˇyiˇˇ
p
5
<
1
p
5
<
1
2 ;
which implies that

60
Chapter 3
Growth of Functions
Fi D
 i
p
5
C 1
2
	
;
(3.25)
which is to say that the ith Fibonacci number Fi is equal to i=
p
5 rounded to the
nearest integer. Thus, Fibonacci numbers grow exponentially.
Exercises
3.2-1
Show that if f .n/ and g.n/ are monotonically increasing functions, then so are
the functions f .n/ C g.n/ and f .g.n//, and if f .n/ and g.n/ are in addition
nonnegative, then f .n/  g.n/ is monotonically increasing.
3.2-2
Prove equation (3.16).
3.2-3
Prove equation (3.19). Also prove that nŠ D !.2n/ and nŠ D o.nn/.
3.2-4
?
Is the function dlg neŠ polynomially bounded? Is the function dlg lg neŠ polynomi-
ally bounded?
3.2-5
?
Which is asymptotically larger: lg.lg n/ or lg.lg n/?
3.2-6
Show that the golden ratio  and its conjugate y both satisfy the equation
x2 D x C 1.
3.2-7
Prove by induction that the ith Fibonacci number satisﬁes the equality
Fi D i  yi
p
5
;
where  is the golden ratio and y is its conjugate.
3.2-8
Show that k ln k D ‚.n/ implies k D ‚.n= ln n/.

Problems for Chapter 3
61
Problems
3-1
Asymptotic behavior of polynomials
Let
p.n/ D
d
X
iD0
aini ;
where ad > 0, be a degree-d polynomial in n, and let k be a constant. Use the
deﬁnitions of the asymptotic notations to prove the following properties.
a. If k  d, then p.n/ D O.nk/.
b. If k  d, then p.n/ D .nk/.
c. If k D d, then p.n/ D ‚.nk/.
d. If k > d, then p.n/ D o.nk/.
e. If k < d, then p.n/ D !.nk/.
3-2
Relative asymptotic growths
Indicate, for each pair of expressions .A; B/ in the table below, whether A is O, o,
, !, or ‚ of B. Assume that k  1,  > 0, and c > 1 are constants. Your answer
should be in the form of the table with “yes” or “no” written in each box.
A
B
O
o

!
‚
a.
lgk n
n
b.
nk
cn
c.
pn
nsin n
d.
2n
2n=2
e.
nlg c
clg n
f.
lg.nŠ/
lg.nn/
3-3
Ordering by asymptotic growth rates
a. Rank the following functions by order of growth; that is, ﬁnd an arrangement
g1; g2; : : : ; g30 of the functions satisfying g1 D .g2/, g2 D .g3/, . . . ,
g29 D .g30/. Partition your list into equivalence classes such that functions
f .n/ and g.n/ are in the same class if and only if f .n/ D ‚.g.n//.

62
Chapter 3
Growth of Functions
lg.lg n/
2lg n
.
p
2/lg n
n2
nŠ
.lg n/Š
. 3
2/n
n3
lg2 n
lg.nŠ/
22n
n1= lg n
ln ln n
lg n
n  2n
nlg lg n
ln n
1
2lg n
.lg n/lg n
en
4lg n
.n C 1/Š
p
lg n
lg.lg n/
2
p2 lg n
n
2n
n lg n
22nC1
b. Give an example of a single nonnegative function f .n/ such that for all func-
tions gi.n/ in part (a), f .n/ is neither O.gi.n// nor .gi.n//.
3-4
Asymptotic notation properties
Let f .n/ and g.n/ be asymptotically positive functions. Prove or disprove each of
the following conjectures.
a. f .n/ D O.g.n// implies g.n/ D O.f .n//.
b. f .n/ C g.n/ D ‚.min.f .n/; g.n///.
c. f .n/ D O.g.n// implies lg.f .n// D O.lg.g.n///, where lg.g.n//  1 and
f .n/  1 for all sufﬁciently large n.
d. f .n/ D O.g.n// implies 2f.n/ D O

2g.n/

.
e. f .n/ D O ..f .n//2/.
f.
f .n/ D O.g.n// implies g.n/ D .f .n//.
g. f .n/ D ‚.f .n=2//.
h. f .n/ C o.f .n// D ‚.f .n//.
3-5
Variations on O and ˝
Some authors deﬁne  in a slightly different way than we do; let’s use
1 (read
“omega inﬁnity”) for this alternative deﬁnition. We say that f .n/ D
1.g.n// if
there exists a positive constant c such that f .n/  cg.n/  0 for inﬁnitely many
integers n.
a. Show that for any two functions f .n/ and g.n/ that are asymptotically nonneg-
ative, either f .n/ D O.g.n// or f .n/ D
1.g.n// or both, whereas this is not
true if we use  in place of
1.

Problems for Chapter 3
63
b. Describe the potential advantages and disadvantages of using
1 instead of  to
characterize the running times of programs.
Some authors also deﬁne O in a slightly different manner; let’s use O0 for the
alternative deﬁnition. We say that f .n/ D O0.g.n// if and only if jf .n/j D
O.g.n//.
c. What happens to each direction of the “if and only if” in Theorem 3.1 if we
substitute O0 for O but still use ?
Some authors deﬁne eO (read “soft-oh”) to mean O with logarithmic factors ig-
nored:
eO.g.n// D ff .n/ W there exist positive constants c, k, and n0 such that
0  f .n/  cg.n/ lgk.n/ for all n  n0g :
d. Deﬁne e and e‚ in a similar manner. Prove the corresponding analog to Theo-
rem 3.1.
3-6
Iterated functions
We can apply the iteration operator  used in the lg function to any monotonically
increasing function f .n/ over the reals. For a given constant c 2 R, we deﬁne the
iterated function f 
c by
f 
c .n/ D min
˚
i  0 W f .i/.n/  c

;
which need not be well deﬁned in all cases. In other words, the quantity f 
c .n/ is
the number of iterated applications of the function f required to reduce its argu-
ment down to c or less.
For each of the following functions f .n/ and constants c, give as tight a bound
as possible on f 
c .n/.
f .n/
c
f 
c .n/
a.
n  1
0
b.
lg n
1
c.
n=2
1
d.
n=2
2
e.
pn
2
f.
pn
1
g.
n1=3
2
h.
n= lg n
2

64
Chapter 3
Growth of Functions
Chapter notes
Knuth [209] traces the origin of the O-notation to a number-theory text by P. Bach-
mann in 1892. The o-notation was invented by E. Landau in 1909 for his discussion
of the distribution of prime numbers. The  and ‚ notations were advocated by
Knuth [213] to correct the popular, but technically sloppy, practice in the literature
of using O-notation for both upper and lower bounds. Many people continue to
use the O-notation where the ‚-notation is more technically precise. Further dis-
cussion of the history and development of asymptotic notations appears in works
by Knuth [209, 213] and Brassard and Bratley [54].
Not all authors deﬁne the asymptotic notations in the same way, although the
various deﬁnitions agree in most common situations. Some of the alternative def-
initions encompass functions that are not asymptotically nonnegative, as long as
their absolute values are appropriately bounded.
Equation (3.20) is due to Robbins [297]. Other properties of elementary math-
ematical functions can be found in any good mathematical reference, such as
Abramowitz and Stegun [1] or Zwillinger [362], or in a calculus book, such as
Apostol [18] or Thomas et al. [334]. Knuth [209] and Graham, Knuth, and Patash-
nik [152] contain a wealth of material on discrete mathematics as used in computer
science.

## Figures

![Page 66 figure](images/3-growth-of-functions/p66_figure1.png)
