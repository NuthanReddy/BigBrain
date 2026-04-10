# 15 Dynamic Programming

Dynamic Programming
Dynamic programming, like the divide-and-conquer method, solves problems by
combining the solutions to subproblems. (“Programming” in this context refers
to a tabular method, not to writing computer code.) As we saw in Chapters 2
and 4, divide-and-conquer algorithms partition the problem into disjoint subproblems, solve the subproblems recursively, and then combine their solutions to solve
the original problem. In contrast, dynamic programming applies when the subproblems overlap—that is, when subproblems share subsubproblems. In this context,
a divide-and-conquer algorithm does more work than necessary, repeatedly solving the common subsubproblems. A dynamic-programming algorithm solves each
subsubproblem just once and then saves its answer in a table, thereby avoiding the
work of recomputing the answer every time it solves each subsubproblem.
We typically apply dynamic programming to optimization problems. Such problems can have many possible solutions. Each solution has a value, and we wish to
ﬁnd a solution with the optimal (minimum or maximum) value. We call such a
solution an optimal solution to the problem, as opposed to the optimal solution,
since there may be several solutions that achieve the optimal value.
When developing a dynamic-programming algorithm, we follow a sequence of
four steps:
1. Characterize the structure of an optimal solution.
2. Recursively deﬁne the value of an optimal solution.
3. Compute the value of an optimal solution, typically in a bottom-up fashion.
4. Construct an optimal solution from computed information.
Steps 1–3 form the basis of a dynamic-programming solution to a problem. If we
need only the value of an optimal solution, and not the solution itself, then we
can omit step 4. When we do perform step 4, we sometimes maintain additional
information during step 3 so that we can easily construct an optimal solution.
The sections that follow use the dynamic-programming method to solve some
optimization problems. Section 15.1 examines the problem of cutting a rod into

rods of smaller length in way that maximizes their total value. Section 15.2 asks
how we can multiply a chain of matrices while performing the fewest total scalar
multiplications. Given these examples of dynamic programming, Section 15.3 discusses two key characteristics that a problem must have for dynamic programming
to be a viable solution technique. Section 15.4 then shows how to ﬁnd the longest
common subsequence of two sequences via dynamic programming. Finally, Section 15.5 uses dynamic programming to construct binary search trees that are optimal, given a known distribution of keys to be looked up.

## 15.1 Rod cutting

Our ﬁrst example uses dynamic programming to solve a simple problem in deciding where to cut steel rods. Serling Enterprises buys long steel rods and cuts them
into shorter rods, which it then sells. Each cut is free. The management of Serling
Enterprises wants to know the best way to cut up the rods.
We assume that we know, for i D 1; 2; : : :, the price pi in dollars that Serling
Enterprises charges for a rod of length i inches. Rod lengths are always an integral
number of inches. Figure 15.1 gives a sample price table.
The rod-cutting problem is the following. Given a rod of length n inches and a
table of prices pi for i D 1; 2; : : : ; n, determine the maximum revenue rn obtainable by cutting up the rod and selling the pieces. Note that if the price pn for a rod
of length n is large enough, an optimal solution may require no cutting at all.
Consider the case when n D 4. Figure 15.2 shows all the ways to cut up a rod
of 4 inches in length, including the way with no cuts at all. We see that cutting a
4-inch rod into two 2-inch pieces produces revenue p2 C p2 D 5 C 5 D 10, which
is optimal.
We can cut up a rod of length n in 2n1 different ways, since we have an independent option of cutting, or not cutting, at distance i inches from the left end,
length i
price pi
Figure 15.1
A sample price table for rods. Each rod of length i inches earns the company pi
dollars of revenue.

## 15.1 Rod cutting

(a)
(b)
(c)
(d)
(e)
(f)
(g)
(h)
Figure 15.2
The 8 possible ways of cutting up a rod of length 4.
Above each piece is the
value of that piece, according to the sample price chart of Figure 15.1. The optimal strategy is
part (c)—cutting the rod into two pieces of length 2—which has total value 10.
for i D 1; 2; : : : ; n  1.1 We denote a decomposition into pieces using ordinary
additive notation, so that 7 D 2 C 2 C 3 indicates that a rod of length 7 is cut into
three pieces—two of length 2 and one of length 3. If an optimal solution cuts the
rod into k pieces, for some 1  k  n, then an optimal decomposition
n D i1 C i2 C    C ik
of the rod into pieces of lengths i1, i2, . . . , ik provides maximum corresponding
revenue
rn D pi1 C pi2 C    C pik :
For our sample problem, we can determine the optimal revenue ﬁgures ri, for
i D 1; 2; : : : ; 10, by inspection, with the corresponding optimal decompositions
1If we required the pieces to be cut in order of nondecreasing size, there would be fewer ways
to consider. For n D 4, we would consider only 5 such ways: parts (a), (b), (c), (e), and (h)
in Figure 15.2. The number of ways is called the partition function; it is approximately equal to
e
p
2n=3=4n
p
3. This quantity is less than 2n1, but still much greater than any polynomial in n.
We shall not pursue this line of inquiry further, however.

r1 D 1
from solution 1 D 1
(no cuts) ;
r2 D 5
from solution 2 D 2
(no cuts) ;
r3 D 8
from solution 3 D 3
(no cuts) ;
r4 D 10 from solution 4 D 2 C 2 ;
r5 D 13 from solution 5 D 2 C 3 ;
r6 D 17 from solution 6 D 6
(no cuts) ;
r7 D 18 from solution 7 D 1 C 6 or 7 D 2 C 2 C 3 ;
r8 D 22 from solution 8 D 2 C 6 ;
r9 D 25 from solution 9 D 3 C 6 ;
r10 D 30 from solution 10 D 10
(no cuts) :
More generally, we can frame the values rn for n  1 in terms of optimal revenues from shorter rods:
rn D max .pn; r1 C rn1; r2 C rn2; : : : ; rn1 C r1/ :
(15.1)
The ﬁrst argument, pn, corresponds to making no cuts at all and selling the rod of
length n as is. The other n  1 arguments to max correspond to the maximum revenue obtained by making an initial cut of the rod into two pieces of size i and n  i,
for each i D 1; 2; : : : ; n  1, and then optimally cutting up those pieces further,
obtaining revenues ri and rni from those two pieces. Since we don’t know ahead
of time which value of i optimizes revenue, we have to consider all possible values
for i and pick the one that maximizes revenue. We also have the option of picking
no i at all if we can obtain more revenue by selling the rod uncut.
Note that to solve the original problem of size n, we solve smaller problems of
the same type, but of smaller sizes. Once we make the ﬁrst cut, we may consider
the two pieces as independent instances of the rod-cutting problem. The overall
optimal solution incorporates optimal solutions to the two related subproblems,
maximizing revenue from each of those two pieces. We say that the rod-cutting
problem exhibits optimal substructure: optimal solutions to a problem incorporate
optimal solutions to related subproblems, which we may solve independently.
In a related, but slightly simpler, way to arrange a recursive structure for the rodcutting problem, we view a decomposition as consisting of a ﬁrst piece of length i
cut off the left-hand end, and then a right-hand remainder of length n  i. Only
the remainder, and not the ﬁrst piece, may be further divided. We may view every
decomposition of a length-n rod in this way: as a ﬁrst piece followed by some
decomposition of the remainder. When doing so, we can couch the solution with
no cuts at all as saying that the ﬁrst piece has size i D n and revenue pn and that
the remainder has size 0 with corresponding revenue r0 D 0. We thus obtain the
following simpler version of equation (15.1):
rn D max
1in .pi C rni/ :
(15.2)

## 15.1 Rod cutting

In this formulation, an optimal solution embodies the solution to only one related
subproblem—the remainder—rather than two.
Recursive top-down implementation
The following procedure implements the computation implicit in equation (15.2)
in a straightforward, top-down, recursive manner.
CUT-ROD.p; n/
if n == 0
return 0
q D 1
for i D 1 to n
q D max.q; pŒi C CUT-ROD.p; n  i//
return q
Procedure CUT-ROD takes as input an array pŒ1 : : n of prices and an integer n,
and it returns the maximum revenue possible for a rod of length n. If n D 0, no
revenue is possible, and so CUT-ROD returns 0 in line 2. Line 3 initializes the
maximum revenue q to 1, so that the for loop in lines 4–5 correctly computes
q D max1in.pi C CUT-ROD.p; n  i//; line 6 then returns this value. A simple
induction on n proves that this answer is equal to the desired answer rn, using
equation (15.2).
If you were to code up CUT-ROD in your favorite programming language and run
it on your computer, you would ﬁnd that once the input size becomes moderately
large, your program would take a long time to run. For n D 40, you would ﬁnd that
your program takes at least several minutes, and most likely more than an hour. In
fact, you would ﬁnd that each time you increase n by 1, your program’s running
time would approximately double.
Why is CUT-ROD so inefﬁcient? The problem is that CUT-ROD calls itself
recursively over and over again with the same parameter values; it solves the
same subproblems repeatedly. Figure 15.3 illustrates what happens for n D 4:
CUT-ROD.p; n/ calls CUT-ROD.p; n  i/ for i D 1; 2; : : : ; n.
Equivalently,
CUT-ROD.p; n/ calls CUT-ROD.p; j / for each j D 0; 1; : : : ; n  1. When this
process unfolds recursively, the amount of work done, as a function of n, grows
explosively.
To analyze the running time of CUT-ROD, let T .n/ denote the total number of
calls made to CUT-ROD when called with its second parameter equal to n. This
expression equals the number of nodes in a subtree whose root is labeled n in the
recursion tree. The count includes the initial call at its root. Thus, T .0/ D 1 and

Figure 15.3
The recursion tree showing recursive calls resulting from a call CUT-ROD.p; n/ for
n D 4. Each node label gives the size n of the corresponding subproblem, so that an edge from
a parent with label s to a child with label t corresponds to cutting off an initial piece of size s  t
and leaving a remaining subproblem of size t. A path from the root to a leaf corresponds to one of
the 2n1 ways of cutting up a rod of length n. In general, this recursion tree has 2n nodes and 2n1
leaves.
T .n/ D 1 C
n1
X
jD0
T .j / :
(15.3)
The initial 1 is for the call at the root, and the term T .j / counts the number of calls
(including recursive calls) due to the call CUT-ROD.p; n  i/, where j D n  i.
As Exercise 15.1-1 asks you to show,
T .n/ D 2n ;
(15.4)
and so the running time of CUT-ROD is exponential in n.
In retrospect, this exponential running time is not so surprising. CUT-ROD explicitly considers all the 2n1 possible ways of cutting up a rod of length n. The
tree of recursive calls has 2n1 leaves, one for each possible way of cutting up the
rod. The labels on the simple path from the root to a leaf give the sizes of each
remaining right-hand piece before making each cut. That is, the labels give the
corresponding cut points, measured from the right-hand end of the rod.
Using dynamic programming for optimal rod cutting
We now show how to convert CUT-ROD into an efﬁcient algorithm, using dynamic
programming.
The dynamic-programming method works as follows. Having observed that a
naive recursive solution is inefﬁcient because it solves the same subproblems repeatedly, we arrange for each subproblem to be solved only once, saving its solution. If we need to refer to this subproblem’s solution again later, we can just look it

## 15.1 Rod cutting

up, rather than recompute it. Dynamic programming thus uses additional memory
to save computation time; it serves an example of a time-memory trade-off. The
savings may be dramatic: an exponential-time solution may be transformed into a
polynomial-time solution. A dynamic-programming approach runs in polynomial
time when the number of distinct subproblems involved is polynomial in the input
size and we can solve each such subproblem in polynomial time.
There are usually two equivalent ways to implement a dynamic-programming
approach. We shall illustrate both of them with our rod-cutting example.
The ﬁrst approach is top-down with memoization.2 In this approach, we write
the procedure recursively in a natural manner, but modiﬁed to save the result of
each subproblem (usually in an array or hash table). The procedure now ﬁrst checks
to see whether it has previously solved this subproblem. If so, it returns the saved
value, saving further computation at this level; if not, the procedure computes the
value in the usual manner. We say that the recursive procedure has been memoized;
it “remembers” what results it has computed previously.
The second approach is the bottom-up method. This approach typically depends
on some natural notion of the “size” of a subproblem, such that solving any particular subproblem depends only on solving “smaller” subproblems. We sort the
subproblems by size and solve them in size order, smallest ﬁrst. When solving a
particular subproblem, we have already solved all of the smaller subproblems its
solution depends upon, and we have saved their solutions. We solve each subproblem only once, and when we ﬁrst see it, we have already solved all of its
prerequisite subproblems.
These two approaches yield algorithms with the same asymptotic running time,
except in unusual circumstances where the top-down approach does not actually
recurse to examine all possible subproblems. The bottom-up approach often has
much better constant factors, since it has less overhead for procedure calls.
Here is the the pseudocode for the top-down CUT-ROD procedure, with memoization added:
MEMOIZED-CUT-ROD.p; n/
let rŒ0 : : n be a new array
for i D 0 to n
rŒi D 1
return MEMOIZED-CUT-ROD-AUX.p; n; r/
2This is not a misspelling. The word really is memoization, not memorization. Memoization comes
from memo, since the technique consists of recording a value so that we can look it up later.

MEMOIZED-CUT-ROD-AUX.p; n; r/
if rŒn  0
return rŒn
if n == 0
q D 0
else q D 1
for i D 1 to n
q D max.q; pŒi C MEMOIZED-CUT-ROD-AUX.p; n  i; r//
rŒn D q
return q
Here, the main procedure MEMOIZED-CUT-ROD initializes a new auxiliary array rŒ0 : : n with the value 1, a convenient choice with which to denote “unknown.” (Known revenue values are always nonnegative.) It then calls its helper
routine, MEMOIZED-CUT-ROD-AUX.
The procedure MEMOIZED-CUT-ROD-AUX is just the memoized version of our
previous procedure, CUT-ROD. It ﬁrst checks in line 1 to see whether the desired
value is already known and, if it is, then line 2 returns it. Otherwise, lines 3–7
compute the desired value q in the usual manner, line 8 saves it in rŒn, and line 9
returns it.
The bottom-up version is even simpler:
BOTTOM-UP-CUT-ROD.p; n/
let rŒ0 : : n be a new array
rŒ0 D 0
for j D 1 to n
q D 1
for i D 1 to j
q D max.q; pŒi C rŒj  i/
rŒj  D q
return rŒn
For the bottom-up dynamic-programming approach, BOTTOM-UP-CUT-ROD
uses the natural ordering of the subproblems: a problem of size i is “smaller”
than a subproblem of size j if i < j . Thus, the procedure solves subproblems of
sizes j D 0; 1; : : : ; n, in that order.
Line 1 of procedure BOTTOM-UP-CUT-ROD creates a new array rŒ0 : : n in
which to save the results of the subproblems, and line 2 initializes rŒ0 to 0, since
a rod of length 0 earns no revenue. Lines 3–6 solve each subproblem of size j , for
j D 1; 2; : : : ; n, in order of increasing size. The approach used to solve a problem
of a particular size j is the same as that used by CUT-ROD, except that line 6 now

## 15.1 Rod cutting

Figure 15.4
The subproblem graph for the rod-cutting problem with n D 4. The vertex labels
give the sizes of the corresponding subproblems. A directed edge .x; y/ indicates that we need a
solution to subproblem y when solving subproblem x. This graph is a reduced version of the tree of
Figure 15.3, in which all nodes with the same label are collapsed into a single vertex and all edges
go from parent to child.
directly references array entry rŒj  i instead of making a recursive call to solve
the subproblem of size j  i. Line 7 saves in rŒj  the solution to the subproblem
of size j . Finally, line 8 returns rŒn, which equals the optimal value rn.
The bottom-up and top-down versions have the same asymptotic running time.
The running time of procedure BOTTOM-UP-CUT-ROD is ‚.n2/, due to its
doubly-nested loop structure. The number of iterations of its inner for loop, in
lines 5–6, forms an arithmetic series. The running time of its top-down counterpart,
MEMOIZED-CUT-ROD, is also ‚.n2/, although this running time may be a little
harder to see. Because a recursive call to solve a previously solved subproblem
returns immediately, MEMOIZED-CUT-ROD solves each subproblem just once. It
solves subproblems for sizes 0; 1; : : : ; n. To solve a subproblem of size n, the for
loop of lines 6–7 iterates n times. Thus, the total number of iterations of this for
loop, over all recursive calls of MEMOIZED-CUT-ROD, forms an arithmetic series,
giving a total of ‚.n2/ iterations, just like the inner for loop of BOTTOM-UPCUT-ROD. (We actually are using a form of aggregate analysis here. We shall see
aggregate analysis in detail in Section 17.1.)
Subproblem graphs
When we think about a dynamic-programming problem, we should understand the
set of subproblems involved and how subproblems depend on one another.
The subproblem graph for the problem embodies exactly this information. Figure 15.4 shows the subproblem graph for the rod-cutting problem with n D 4. It
is a directed graph, containing one vertex for each distinct subproblem. The sub368
problem graph has a directed edge from the vertex for subproblem x to the vertex
for subproblem y if determining an optimal solution for subproblem x involves
directly considering an optimal solution for subproblem y. For example, the subproblem graph contains an edge from x to y if a top-down recursive procedure for
solving x directly calls itself to solve y. We can think of the subproblem graph
as a “reduced” or “collapsed” version of the recursion tree for the top-down recursive method, in which we coalesce all nodes for the same subproblem into a single
vertex and direct all edges from parent to child.
The bottom-up method for dynamic programming considers the vertices of the
subproblem graph in such an order that we solve the subproblems y adjacent to
a given subproblem x before we solve subproblem x. (Recall from Section B.4
that the adjacency relation is not necessarily symmetric.) Using the terminology
from Chapter 22, in a bottom-up dynamic-programming algorithm, we consider the
vertices of the subproblem graph in an order that is a “reverse topological sort,” or
a “topological sort of the transpose” (see Section 22.4) of the subproblem graph. In
other words, no subproblem is considered until all of the subproblems it depends
upon have been solved. Similarly, using notions from the same chapter, we can
view the top-down method (with memoization) for dynamic programming as a
“depth-ﬁrst search” of the subproblem graph (see Section 22.3).
The size of the subproblem graph G D .V; E/ can help us determine the running
time of the dynamic programming algorithm. Since we solve each subproblem just
once, the running time is the sum of the times needed to solve each subproblem.
Typically, the time to compute the solution to a subproblem is proportional to the
degree (number of outgoing edges) of the corresponding vertex in the subproblem
graph, and the number of subproblems is equal to the number of vertices in the subproblem graph. In this common case, the running time of dynamic programming
is linear in the number of vertices and edges.
Reconstructing a solution
Our dynamic-programming solutions to the rod-cutting problem return the value of
an optimal solution, but they do not return an actual solution: a list of piece sizes.
We can extend the dynamic-programming approach to record not only the optimal
value computed for each subproblem, but also a choice that led to the optimal
value. With this information, we can readily print an optimal solution.
Here is an extended version of BOTTOM-UP-CUT-ROD that computes, for each
rod size j , not only the maximum revenue rj, but also sj, the optimal size of the
ﬁrst piece to cut off:

## 15.1 Rod cutting

EXTENDED-BOTTOM-UP-CUT-ROD.p; n/
let rŒ0 : : n and sŒ0 : : n be new arrays
rŒ0 D 0
for j D 1 to n
q D 1
for i D 1 to j
if q < pŒi C rŒj  i
q D pŒi C rŒj  i
sŒj  D i
rŒj  D q
return r and s
This procedure is similar to BOTTOM-UP-CUT-ROD, except that it creates the array s in line 1, and it updates sŒj  in line 8 to hold the optimal size i of the ﬁrst
piece to cut off when solving a subproblem of size j .
The following procedure takes a price table p and a rod size n, and it calls
EXTENDED-BOTTOM-UP-CUT-ROD to compute the array sŒ1 : : n of optimal
ﬁrst-piece sizes and then prints out the complete list of piece sizes in an optimal
decomposition of a rod of length n:
PRINT-CUT-ROD-SOLUTION.p; n/
.r; s/ D EXTENDED-BOTTOM-UP-CUT-ROD.p; n/
while n > 0
print sŒn
n D n  sŒn
In our rod-cutting example, the call EXTENDED-BOTTOM-UP-CUT-ROD.p; 10/
would return the following arrays:
i
rŒi
sŒi
A call to PRINT-CUT-ROD-SOLUTION.p; 10/ would print just 10, but a call with
n D 7 would print the cuts 1 and 6, corresponding to the ﬁrst optimal decomposition for r7 given earlier.

## Exercises

15.1-1
Show that equation (15.4) follows from equation (15.3) and the initial condition
T .0/ D 1.

15.1-2
Show, by means of a counterexample, that the following “greedy” strategy does
not always determine an optimal way to cut rods. Deﬁne the density of a rod of
length i to be pi=i, that is, its value per inch. The greedy strategy for a rod of
length n cuts off a ﬁrst piece of length i, where 1  i  n, having maximum
density. It then continues by applying the greedy strategy to the remaining piece of
length n  i.
15.1-3
Consider a modiﬁcation of the rod-cutting problem in which, in addition to a
price pi for each rod, each cut incurs a ﬁxed cost of c. The revenue associated with
a solution is now the sum of the prices of the pieces minus the costs of making the
cuts. Give a dynamic-programming algorithm to solve this modiﬁed problem.
15.1-4
Modify MEMOIZED-CUT-ROD to return not only the value but the actual solution,
too.
15.1-5
The Fibonacci numbers are deﬁned by recurrence (3.22).
Give an O.n/-time
dynamic-programming algorithm to compute the nth Fibonacci number. Draw the
subproblem graph. How many vertices and edges are in the graph?

## 15.2 Matrix-chain multiplication

Our next example of dynamic programming is an algorithm that solves the problem
of matrix-chain multiplication. We are given a sequence (chain) hA1; A2; : : : ; Ani
of n matrices to be multiplied, and we wish to compute the product
A1A2    An :
(15.5)
We can evaluate the expression (15.5) using the standard algorithm for multiplying pairs of matrices as a subroutine once we have parenthesized it to resolve all
ambiguities in how the matrices are multiplied together. Matrix multiplication is
associative, and so all parenthesizations yield the same product. A product of matrices is fully parenthesized if it is either a single matrix or the product of two fully
parenthesized matrix products, surrounded by parentheses. For example, if the
chain of matrices is hA1; A2; A3; A4i, then we can fully parenthesize the product
A1A2A3A4 in ﬁve distinct ways:

## 15.2 Matrix-chain multiplication

.A1.A2.A3A4/// ;
.A1..A2A3/A4// ;
..A1A2/.A3A4// ;
..A1.A2A3//A4/ ;
...A1A2/A3/A4/ :
How we parenthesize a chain of matrices can have a dramatic impact on the cost
of evaluating the product. Consider ﬁrst the cost of multiplying two matrices. The
standard algorithm is given by the following pseudocode, which generalizes the
SQUARE-MATRIX-MULTIPLY procedure from Section 4.2. The attributes rows
and columns are the numbers of rows and columns in a matrix.
MATRIX-MULTIPLY.A; B/
if A:columns ¤ B:rows
error “incompatible dimensions”
else let C be a new A:rows 	 B:columns matrix
for i D 1 to A:rows
for j D 1 to B:columns
cij D 0
for k D 1 to A:columns
cij D cij C aik  bkj
return C
We can multiply two matrices A and B only if they are compatible: the number of
columns of A must equal the number of rows of B. If A is a p 	 q matrix and B is
a q 	 r matrix, the resulting matrix C is a p 	 r matrix. The time to compute C is
dominated by the number of scalar multiplications in line 8, which is pqr. In what
follows, we shall express costs in terms of the number of scalar multiplications.
To illustrate the different costs incurred by different parenthesizations of a matrix
product, consider the problem of a chain hA1; A2; A3i of three matrices. Suppose
that the dimensions of the matrices are 10 	 100, 100 	 5, and 5 	 50, respectively. If we multiply according to the parenthesization ..A1A2/A3/, we perform
10  100  5 D 5000 scalar multiplications to compute the 10 	 5 matrix product A1A2, plus another 10  5  50 D 2500 scalar multiplications to multiply this
matrix by A3, for a total of 7500 scalar multiplications. If instead we multiply
according to the parenthesization .A1.A2A3//, we perform 100  5  50 D 25,000
scalar multiplications to compute the 100 	 50 matrix product A2A3, plus another
10  100  50 D 50,000 scalar multiplications to multiply A1 by this matrix, for a
total of 75,000 scalar multiplications. Thus, computing the product according to
the ﬁrst parenthesization is 10 times faster.
We state the matrix-chain multiplication problem as follows: given a chain
hA1;A2;: : : ;Ani of n matrices, where for i D 1; 2; : : : ; n, matrix Ai has dimension

pi1 	 pi, fully parenthesize the product A1A2    An in a way that minimizes the
number of scalar multiplications.
Note that in the matrix-chain multiplication problem, we are not actually multiplying matrices. Our goal is only to determine an order for multiplying matrices
that has the lowest cost. Typically, the time invested in determining this optimal
order is more than paid for by the time saved later on when actually performing the
matrix multiplications (such as performing only 7500 scalar multiplications instead
of 75,000).
Counting the number of parenthesizations
Before solving the matrix-chain multiplication problem by dynamic programming,
let us convince ourselves that exhaustively checking all possible parenthesizations
does not yield an efﬁcient algorithm. Denote the number of alternative parenthesizations of a sequence of n matrices by P.n/. When n D 1, we have just one
matrix and therefore only one way to fully parenthesize the matrix product. When
n  2, a fully parenthesized matrix product is the product of two fully parenthesized matrix subproducts, and the split between the two subproducts may occur
between the kth and .k C 1/st matrices for any k D 1; 2; : : : ; n  1. Thus, we
obtain the recurrence
P.n/ D

if n D 1 ;
n1
X
kD1
P.k/P.n  k/
if n  2 :
(15.6)
Problem 12-4 asked you to show that the solution to a similar recurrence is the
sequence of Catalan numbers, which grows as .4n=n3=2/. A simpler exercise
(see Exercise 15.2-3) is to show that the solution to the recurrence (15.6) is .2n/.
The number of solutions is thus exponential in n, and the brute-force method of
exhaustive search makes for a poor strategy when determining how to optimally
parenthesize a matrix chain.
Applying dynamic programming
We shall use the dynamic-programming method to determine how to optimally
parenthesize a matrix chain. In so doing, we shall follow the four-step sequence
that we stated at the beginning of this chapter:
1. Characterize the structure of an optimal solution.
2. Recursively deﬁne the value of an optimal solution.
3. Compute the value of an optimal solution.

## 15.2 Matrix-chain multiplication

4. Construct an optimal solution from computed information.
We shall go through these steps in order, demonstrating clearly how we apply each
step to the problem.
Step 1: The structure of an optimal parenthesization
For our ﬁrst step in the dynamic-programming paradigm, we ﬁnd the optimal substructure and then use it to construct an optimal solution to the problem from optimal solutions to subproblems. In the matrix-chain multiplication problem, we can
perform this step as follows. For convenience, let us adopt the notation Ai::j, where
i  j , for the matrix that results from evaluating the product AiAiC1    Aj. Observe that if the problem is nontrivial, i.e., i < j , then to parenthesize the product
AiAiC1    Aj, we must split the product between Ak and AkC1 for some integer k
in the range i  k < j . That is, for some value of k, we ﬁrst compute the matrices
Ai::k and AkC1::j and then multiply them together to produce the ﬁnal product Ai::j.
The cost of parenthesizing this way is the cost of computing the matrix Ai::k, plus
the cost of computing AkC1::j, plus the cost of multiplying them together.
The optimal substructure of this problem is as follows. Suppose that to optimally parenthesize AiAiC1    Aj, we split the product between Ak and AkC1.
Then the way we parenthesize the “preﬁx” subchain AiAiC1    Ak within this
optimal parenthesization of AiAiC1    Aj must be an optimal parenthesization of
AiAiC1    Ak. Why? If there were a less costly way to parenthesize AiAiC1    Ak,
then we could substitute that parenthesization in the optimal parenthesization
of AiAiC1    Aj to produce another way to parenthesize AiAiC1    Aj whose cost
was lower than the optimum: a contradiction. A similar observation holds for how
we parenthesize the subchain AkC1AkC2    Aj in the optimal parenthesization of
AiAiC1    Aj: it must be an optimal parenthesization of AkC1AkC2    Aj.
Now we use our optimal substructure to show that we can construct an optimal
solution to the problem from optimal solutions to subproblems. We have seen that
any solution to a nontrivial instance of the matrix-chain multiplication problem
requires us to split the product, and that any optimal solution contains within it optimal solutions to subproblem instances. Thus, we can build an optimal solution to
an instance of the matrix-chain multiplication problem by splitting the problem into
two subproblems (optimally parenthesizing AiAiC1    Ak and AkC1AkC2    Aj),
ﬁnding optimal solutions to subproblem instances, and then combining these optimal subproblem solutions. We must ensure that when we search for the correct
place to split the product, we have considered all possible places, so that we are
sure of having examined the optimal one.

Step 2: A recursive solution
Next, we deﬁne the cost of an optimal solution recursively in terms of the optimal
solutions to subproblems. For the matrix-chain multiplication problem, we pick as
our subproblems the problems of determining the minimum cost of parenthesizing
AiAiC1    Aj for 1  i  j  n. Let mŒi; j  be the minimum number of scalar
multiplications needed to compute the matrix Ai::j; for the full problem, the lowestcost way to compute A1::n would thus be mŒ1; n.
We can deﬁne mŒi; j  recursively as follows. If i D j , the problem is trivial;
the chain consists of just one matrix Ai::i D Ai, so that no scalar multiplications
are necessary to compute the product. Thus, mŒi; i D 0 for i D 1; 2; : : : ; n. To
compute mŒi; j  when i < j , we take advantage of the structure of an optimal
solution from step 1. Let us assume that to optimally parenthesize, we split the
product AiAiC1    Aj between Ak and AkC1, where i  k < j . Then, mŒi; j 
equals the minimum cost for computing the subproducts Ai::k and AkC1::j, plus the
cost of multiplying these two matrices together. Recalling that each matrix Ai is
pi1 	 pi, we see that computing the matrix product Ai::kAkC1::j takes pi1pkpj
scalar multiplications. Thus, we obtain
mŒi; j  D mŒi; k C mŒk C 1; j  C pi1pkpj :
This recursive equation assumes that we know the value of k, which we do not.
There are only j i possible values for k, however, namely k D i; i C1; : : : ; j 1.
Since the optimal parenthesization must use one of these values for k, we need only
check them all to ﬁnd the best. Thus, our recursive deﬁnition for the minimum cost
of parenthesizing the product AiAiC1    Aj becomes
mŒi; j  D
( 0
if i D j ;
min
ik<j fmŒi; k C mŒk C 1; j  C pi1pkpjg
if i < j :
(15.7)
The mŒi; j  values give the costs of optimal solutions to subproblems, but they
do not provide all the information we need to construct an optimal solution. To
help us do so, we deﬁne sŒi; j  to be a value of k at which we split the product
AiAiC1    Aj in an optimal parenthesization. That is, sŒi; j  equals a value k such
that mŒi; j  D mŒi; k C mŒk C 1; j  C pi1pkpj.
Step 3: Computing the optimal costs
At this point, we could easily write a recursive algorithm based on recurrence (15.7)
to compute the minimum cost mŒ1; n for multiplying A1A2    An. As we saw for
the rod-cutting problem, and as we shall see in Section 15.3, this recursive algorithm takes exponential time, which is no better than the brute-force method of
checking each way of parenthesizing the product.

## 15.2 Matrix-chain multiplication

Observe that we have relatively few distinct subproblems: one subproblem for
each choice of i and j satisfying 1  i  j  n, or

n

C n D ‚.n2/ in all.
A recursive algorithm may encounter each subproblem many times in different
branches of its recursion tree. This property of overlapping subproblems is the
second hallmark of when dynamic programming applies (the ﬁrst hallmark being
optimal substructure).
Instead of computing the solution to recurrence (15.7) recursively, we compute
the optimal cost by using a tabular, bottom-up approach. (We present the corresponding top-down approach using memoization in Section 15.3.)
We shall implement the tabular, bottom-up method in the procedure MATRIXCHAIN-ORDER, which appears below. This procedure assumes that matrix Ai
has dimensions pi1 	 pi for i D 1; 2; : : : ; n.
Its input is a sequence p D
hp0; p1; : : : ; pni, where p:length D n C 1.
The procedure uses an auxiliary
table mŒ1 : : n; 1 : : n for storing the mŒi; j  costs and another auxiliary table
sŒ1 : : n  1; 2 : : n that records which index of k achieved the optimal cost in computing mŒi; j . We shall use the table s to construct an optimal solution.
In order to implement the bottom-up approach, we must determine which entries
of the table we refer to when computing mŒi; j . Equation (15.7) shows that the
cost mŒi; j  of computing a matrix-chain product of j iC1 matrices depends only
on the costs of computing matrix-chain products of fewer than j  i C 1 matrices.
That is, for k D i; i C 1; : : : ; j  1, the matrix Ai::k is a product of k  i C 1 <
j  i C 1 matrices and the matrix AkC1::j is a product of j  k < j  i C 1
matrices. Thus, the algorithm should ﬁll in the table m in a manner that corresponds
to solving the parenthesization problem on matrix chains of increasing length. For
the subproblem of optimally parenthesizing the chain AiAiC1    Aj, we consider
the subproblem size to be the length j  i C 1 of the chain.
MATRIX-CHAIN-ORDER.p/
n D p:length  1
let mŒ1 : : n; 1 : : n and sŒ1 : : n  1; 2 : : n be new tables
for i D 1 to n
mŒi; i D 0
for l D 2 to n
// l is the chain length
for i D 1 to n  l C 1
j D i C l  1
mŒi; j  D 1
for k D i to j  1
q D mŒi; k C mŒk C 1; j  C pi1pkpj
if q < mŒi; j 
mŒi; j  D q
sŒi; j  D k
return m and s

A6
A5
A4
A3
A2
A1
15,750
2,625
1,000
5,000
7,875
4,375
2,500
3,500
9,375
7,125
5,375
11,875
10,500
15,125
j
i
m
j
i
s
Figure 15.5
The m and s tables computed by MATRIX-CHAIN-ORDER for n D 6 and the following matrix dimensions:
matrix
A1
A2
A3
A4
A5
A6
dimension
30 	 35
35 	 15
15 	 5
5 	 10
10 	 20
20 	 25
The tables are rotated so that the main diagonal runs horizontally. The m table uses only the main
diagonal and upper triangle, and the s table uses only the upper triangle. The minimum number of
scalar multiplications to multiply the 6 matrices is mŒ1; 6 D 15,125. Of the darker entries, the pairs
that have the same shading are taken together in line 10 when computing
mŒ2; 5 D min
ˆ<
ˆ:
mŒ2; 2 C mŒ3; 5 C p1p2p5 D 0 C 2500 C 35  15  20
D 13,000 ;
mŒ2; 3 C mŒ4; 5 C p1p3p5 D 2625 C 1000 C 35  5  20 D 7125 ;
mŒ2; 4 C mŒ5; 5 C p1p4p5 D 4375 C 0 C 35  10  20
D 11,375
D 7125 :
The algorithm ﬁrst computes mŒi; i D 0 for i D 1; 2; : : : ; n (the minimum
costs for chains of length 1) in lines 3–4. It then uses recurrence (15.7) to compute
mŒi; i C 1 for i D 1; 2; : : : ; n  1 (the minimum costs for chains of length l D 2)
during the ﬁrst execution of the for loop in lines 5–13. The second time through the
loop, it computes mŒi; iC2 for i D 1; 2; : : : ; n2 (the minimum costs for chains of
length l D 3), and so forth. At each step, the mŒi; j  cost computed in lines 10–13
depends only on table entries mŒi; k and mŒk C 1; j  already computed.
Figure 15.5 illustrates this procedure on a chain of n D 6 matrices.
Since
we have deﬁned mŒi; j  only for i  j , only the portion of the table m strictly
above the main diagonal is used. The ﬁgure shows the table rotated to make the
main diagonal run horizontally. The matrix chain is listed along the bottom. Using this layout, we can ﬁnd the minimum cost mŒi; j  for multiplying a subchain
AiAiC1    Aj of matrices at the intersection of lines running northeast from Ai and

## 15.2 Matrix-chain multiplication

northwest from Aj. Each horizontal row in the table contains the entries for matrix
chains of the same length. MATRIX-CHAIN-ORDER computes the rows from bottom to top and from left to right within each row. It computes each entry mŒi; j 
using the products pi1pkpj for k D i; i C 1; : : : ; j  1 and all entries southwest
and southeast from mŒi; j .
A simple inspection of the nested loop structure of MATRIX-CHAIN-ORDER
yields a running time of O.n3/ for the algorithm. The loops are nested three deep,
and each loop index (l, i, and k) takes on at most n1 values. Exercise 15.2-5 asks
you to show that the running time of this algorithm is in fact also .n3/. The algorithm requires ‚.n2/ space to store the m and s tables. Thus, MATRIX-CHAINORDER is much more efﬁcient than the exponential-time method of enumerating
all possible parenthesizations and checking each one.
Step 4: Constructing an optimal solution
Although MATRIX-CHAIN-ORDER determines the optimal number of scalar multiplications needed to compute a matrix-chain product, it does not directly show
how to multiply the matrices. The table sŒ1 : : n  1; 2 : : n gives us the information we need to do so. Each entry sŒi; j  records a value of k such that an optimal parenthesization of AiAiC1    Aj splits the product between Ak and AkC1.
Thus, we know that the ﬁnal matrix multiplication in computing A1::n optimally
is A1::sŒ1;nAsŒ1;nC1::n. We can determine the earlier matrix multiplications recursively, since sŒ1; sŒ1; n determines the last matrix multiplication when computing
A1::sŒ1;n and sŒsŒ1; n C 1; n determines the last matrix multiplication when computing AsŒ1;nC1::n. The following recursive procedure prints an optimal parenthesization of hAi; AiC1; : : : ; Aji, given the s table computed by MATRIX-CHAINORDER and the indices i and j . The initial call PRINT-OPTIMAL-PARENS.s; 1; n/
prints an optimal parenthesization of hA1; A2; : : : ; Ani.
PRINT-OPTIMAL-PARENS.s; i; j /
if i == j
print “A”i
else print “(”
PRINT-OPTIMAL-PARENS.s; i; sŒi; j /
PRINT-OPTIMAL-PARENS.s; sŒi; j  C 1; j /
print “)”
In the example of Figure 15.5, the call PRINT-OPTIMAL-PARENS.s; 1; 6/ prints
the parenthesization ..A1.A2A3//..A4A5/A6//.

## Exercises

15.2-1
Find an optimal parenthesization of a matrix-chain product whose sequence of
dimensions is h5; 10; 3; 12; 5; 50; 6i.
15.2-2
Give a recursive algorithm MATRIX-CHAIN-MULTIPLY.A; s; i; j / that actually
performs the optimal matrix-chain multiplication, given the sequence of matrices
hA1; A2; : : : ; Ani, the s table computed by MATRIX-CHAIN-ORDER, and the indices i and j . (The initial call would be MATRIX-CHAIN-MULTIPLY.A; s; 1; n/.)
15.2-3
Use the substitution method to show that the solution to the recurrence (15.6)
is .2n/.
15.2-4
Describe the subproblem graph for matrix-chain multiplication with an input chain
of length n. How many vertices does it have? How many edges does it have, and
which edges are they?
15.2-5
Let R.i; j / be the number of times that table entry mŒi; j  is referenced while
computing other table entries in a call of MATRIX-CHAIN-ORDER. Show that the
total number of references for the entire table is
n
X
iD1
n
X
jDi
R.i; j / D n3  n
:
(Hint: You may ﬁnd equation (A.3) useful.)
15.2-6
Show that a full parenthesization of an n-element expression has exactly n1 pairs
of parentheses.

## 15.3 Elements of dynamic programming

Although we have just worked through two examples of the dynamic-programming
method, you might still be wondering just when the method applies. From an engineering perspective, when should we look for a dynamic-programming solution
to a problem? In this section, we examine the two key ingredients that an opti15.3
Elements of dynamic programming
mization problem must have in order for dynamic programming to apply: optimal
substructure and overlapping subproblems. We also revisit and discuss more fully
how memoization might help us take advantage of the overlapping-subproblems
property in a top-down recursive approach.
Optimal substructure
The ﬁrst step in solving an optimization problem by dynamic programming is to
characterize the structure of an optimal solution. Recall that a problem exhibits
optimal substructure if an optimal solution to the problem contains within it optimal solutions to subproblems. Whenever a problem exhibits optimal substructure,
we have a good clue that dynamic programming might apply. (As Chapter 16 discusses, it also might mean that a greedy strategy applies, however.) In dynamic
programming, we build an optimal solution to the problem from optimal solutions
to subproblems. Consequently, we must take care to ensure that the range of subproblems we consider includes those used in an optimal solution.
We discovered optimal substructure in both of the problems we have examined
in this chapter so far. In Section 15.1, we observed that the optimal way of cutting up a rod of length n (if we make any cuts at all) involves optimally cutting
up the two pieces resulting from the ﬁrst cut. In Section 15.2, we observed that
an optimal parenthesization of AiAiC1    Aj that splits the product between Ak
and AkC1 contains within it optimal solutions to the problems of parenthesizing
AiAiC1    Ak and AkC1AkC2    Aj.
You will ﬁnd yourself following a common pattern in discovering optimal substructure:
1. You show that a solution to the problem consists of making a choice, such as
choosing an initial cut in a rod or choosing an index at which to split the matrix
chain. Making this choice leaves one or more subproblems to be solved.
2. You suppose that for a given problem, you are given the choice that leads to an
optimal solution. You do not concern yourself yet with how to determine this
choice. You just assume that it has been given to you.
3. Given this choice, you determine which subproblems ensue and how to best
characterize the resulting space of subproblems.
4. You show that the solutions to the subproblems used within an optimal solution
to the problem must themselves be optimal by using a “cut-and-paste” technique. You do so by supposing that each of the subproblem solutions is not
optimal and then deriving a contradiction. In particular, by “cutting out” the
nonoptimal solution to each subproblem and “pasting in” the optimal one, you
show that you can get a better solution to the original problem, thus contradicting your supposition that you already had an optimal solution. If an optimal

solution gives rise to more than one subproblem, they are typically so similar
that you can modify the cut-and-paste argument for one to apply to the others
with little effort.
To characterize the space of subproblems, a good rule of thumb says to try to
keep the space as simple as possible and then expand it as necessary. For example,
the space of subproblems that we considered for the rod-cutting problem contained
the problems of optimally cutting up a rod of length i for each size i. This subproblem space worked well, and we had no need to try a more general space of
subproblems.
Conversely, suppose that we had tried to constrain our subproblem space for
matrix-chain multiplication to matrix products of the form A1A2    Aj. As before,
an optimal parenthesization must split this product between Ak and AkC1 for some
1  k < j . Unless we could guarantee that k always equals j  1, we would ﬁnd
that we had subproblems of the form A1A2    Ak and AkC1AkC2    Aj, and that
the latter subproblem is not of the form A1A2    Aj. For this problem, we needed
to allow our subproblems to vary at “both ends,” that is, to allow both i and j to
vary in the subproblem AiAiC1    Aj.
Optimal substructure varies across problem domains in two ways:
1. how many subproblems an optimal solution to the original problem uses, and
2. how many choices we have in determining which subproblem(s) to use in an
optimal solution.
In the rod-cutting problem, an optimal solution for cutting up a rod of size n
uses just one subproblem (of size n  i), but we must consider n choices for i
in order to determine which one yields an optimal solution. Matrix-chain multiplication for the subchain AiAiC1    Aj serves as an example with two subproblems and j  i choices. For a given matrix Ak at which we split the product, we have two subproblems—parenthesizing AiAiC1    Ak and parenthesizing
AkC1AkC2    Aj—and we must solve both of them optimally. Once we determine
the optimal solutions to subproblems, we choose from among j  i candidates for
the index k.
Informally, the running time of a dynamic-programming algorithm depends on
the product of two factors: the number of subproblems overall and how many
choices we look at for each subproblem. In rod cutting, we had ‚.n/ subproblems
overall, and at most n choices to examine for each, yielding an O.n2/ running time.
Matrix-chain multiplication had ‚.n2/ subproblems overall, and in each we had at
most n  1 choices, giving an O.n3/ running time (actually, a ‚.n3/ running time,
by Exercise 15.2-5).
Usually, the subproblem graph gives an alternative way to perform the same
analysis. Each vertex corresponds to a subproblem, and the choices for a sub15.3
Elements of dynamic programming
problem are the edges incident to that subproblem. Recall that in rod cutting,
the subproblem graph had n vertices and at most n edges per vertex, yielding an
O.n2/ running time. For matrix-chain multiplication, if we were to draw the subproblem graph, it would have ‚.n2/ vertices and each vertex would have degree at
most n  1, giving a total of O.n3/ vertices and edges.
Dynamic programming often uses optimal substructure in a bottom-up fashion.
That is, we ﬁrst ﬁnd optimal solutions to subproblems and, having solved the subproblems, we ﬁnd an optimal solution to the problem. Finding an optimal solution to the problem entails making a choice among subproblems as to which we
will use in solving the problem. The cost of the problem solution is usually the
subproblem costs plus a cost that is directly attributable to the choice itself. In
rod cutting, for example, ﬁrst we solved the subproblems of determining optimal
ways to cut up rods of length i for i D 0; 1; : : : ; n  1, and then we determined
which such subproblem yielded an optimal solution for a rod of length n, using
equation (15.2). The cost attributable to the choice itself is the term pi in equation (15.2). In matrix-chain multiplication, we determined optimal parenthesizations of subchains of AiAiC1    Aj, and then we chose the matrix Ak at which to
split the product. The cost attributable to the choice itself is the term pi1pkpj.
In Chapter 16, we shall examine “greedy algorithms,” which have many similarities to dynamic programming. In particular, problems to which greedy algorithms
apply have optimal substructure. One major difference between greedy algorithms
and dynamic programming is that instead of ﬁrst ﬁnding optimal solutions to subproblems and then making an informed choice, greedy algorithms ﬁrst make a
“greedy” choice—the choice that looks best at the time—and then solve a resulting
subproblem, without bothering to solve all possible related smaller subproblems.
Surprisingly, in some cases this strategy works!
Subtleties
You should be careful not to assume that optimal substructure applies when it does
not. Consider the following two problems in which we are given a directed graph
G D .V; E/ and vertices u;  2 V .
Unweighted shortest path:3 Find a path from u to  consisting of the fewest
edges. Such a path must be simple, since removing a cycle from a path produces a path with fewer edges.
3We use the term “unweighted” to distinguish this problem from that of ﬁnding shortest paths with
weighted edges, which we shall see in Chapters 24 and 25. We can use the breadth-ﬁrst search
technique of Chapter 22 to solve the unweighted problem.

q
r
s
t
Figure 15.6
A directed graph showing that the problem of ﬁnding a longest simple path in an
unweighted directed graph does not have optimal substructure. The path q ! r ! t is a longest
simple path from q to t, but the subpath q ! r is not a longest simple path from q to r, nor is the
subpath r ! t a longest simple path from r to t.
Unweighted longest simple path: Find a simple path from u to  consisting of
the most edges. We need to include the requirement of simplicity because otherwise we can traverse a cycle as many times as we like to create paths with an
arbitrarily large number of edges.
The unweighted shortest-path problem exhibits optimal substructure, as follows.
Suppose that u ¤ , so that the problem is nontrivial. Then, any path p from u
to  must contain an intermediate vertex, say w. (Note that w may be u or .)
Thus, we can decompose the path u
p;  into subpaths u
p1
; w
p2
; . Clearly, the
number of edges in p equals the number of edges in p1 plus the number of edges
in p2. We claim that if p is an optimal (i.e., shortest) path from u to , then p1
must be a shortest path from u to w. Why? We use a “cut-and-paste” argument:
if there were another path, say p0
1, from u to w with fewer edges than p1, then we
could cut out p1 and paste in p0
1 to produce a path u
p0
; w
p2
;  with fewer edges
than p, thus contradicting p’s optimality. Symmetrically, p2 must be a shortest
path from w to . Thus, we can ﬁnd a shortest path from u to  by considering
all intermediate vertices w, ﬁnding a shortest path from u to w and a shortest path
from w to , and choosing an intermediate vertex w that yields the overall shortest
path. In Section 25.2, we use a variant of this observation of optimal substructure
to ﬁnd a shortest path between every pair of vertices on a weighted, directed graph.
You might be tempted to assume that the problem of ﬁnding an unweighted
longest simple path exhibits optimal substructure as well. After all, if we decompose a longest simple path u
p;  into subpaths u
p1
; w
p2
; , then mustn’t p1
be a longest simple path from u to w, and mustn’t p2 be a longest simple path
from w to ? The answer is no! Figure 15.6 supplies an example. Consider the
path q ! r ! t, which is a longest simple path from q to t. Is q ! r a longest
simple path from q to r? No, for the path q ! s ! t ! r is a simple path
that is longer. Is r ! t a longest simple path from r to t? No again, for the path
r ! q ! s ! t is a simple path that is longer.

## 15.3 Elements of dynamic programming

This example shows that for longest simple paths, not only does the problem
lack optimal substructure, but we cannot necessarily assemble a “legal” solution
to the problem from solutions to subproblems. If we combine the longest simple
paths q ! s ! t ! r and r ! q ! s ! t, we get the path q ! s ! t ! r !
q ! s ! t, which is not simple. Indeed, the problem of ﬁnding an unweighted
longest simple path does not appear to have any sort of optimal substructure. No
efﬁcient dynamic-programming algorithm for this problem has ever been found. In
fact, this problem is NP-complete, which—as we shall see in Chapter 34—means
that we are unlikely to ﬁnd a way to solve it in polynomial time.
Why is the substructure of a longest simple path so different from that of a shortest path? Although a solution to a problem for both longest and shortest paths uses
two subproblems, the subproblems in ﬁnding the longest simple path are not independent, whereas for shortest paths they are. What do we mean by subproblems
being independent? We mean that the solution to one subproblem does not affect
the solution to another subproblem of the same problem. For the example of Figure 15.6, we have the problem of ﬁnding a longest simple path from q to t with two
subproblems: ﬁnding longest simple paths from q to r and from r to t. For the ﬁrst
of these subproblems, we choose the path q ! s ! t ! r, and so we have also
used the vertices s and t. We can no longer use these vertices in the second subproblem, since the combination of the two solutions to subproblems would yield a
path that is not simple. If we cannot use vertex t in the second problem, then we
cannot solve it at all, since t is required to be on the path that we ﬁnd, and it is
not the vertex at which we are “splicing” together the subproblem solutions (that
vertex being r). Because we use vertices s and t in one subproblem solution, we
cannot use them in the other subproblem solution. We must use at least one of them
to solve the other subproblem, however, and we must use both of them to solve it
optimally. Thus, we say that these subproblems are not independent. Looked at
another way, using resources in solving one subproblem (those resources being
vertices) renders them unavailable for the other subproblem.
Why, then, are the subproblems independent for ﬁnding a shortest path? The
answer is that by nature, the subproblems do not share resources. We claim that
if a vertex w is on a shortest path p from u to , then we can splice together any
shortest path u
p1
; w and any shortest path w
p2
;  to produce a shortest path from u
to . We are assured that, other than w, no vertex can appear in both paths p1
and p2. Why? Suppose that some vertex x ¤ w appears in both p1 and p2, so that
we can decompose p1 as u
pux
; x ; w and p2 as w ; x
px
; . By the optimal
substructure of this problem, path p has as many edges as p1 and p2 together; let’s
say that p has e edges. Now let us construct a path p0 D u
pux
; x
px
;  from u to .
Because we have excised the paths from x to w and from w to x, each of which
contains at least one edge, path p0 contains at most e  2 edges, which contradicts

the assumption that p is a shortest path. Thus, we are assured that the subproblems
for the shortest-path problem are independent.
Both problems examined in Sections 15.1 and 15.2 have independent subproblems. In matrix-chain multiplication, the subproblems are multiplying subchains
AiAiC1    Ak and AkC1AkC2    Aj. These subchains are disjoint, so that no matrix could possibly be included in both of them. In rod cutting, to determine the
best way to cut up a rod of length n, we look at the best ways of cutting up rods
of length i for i D 0; 1; : : : ; n  1. Because an optimal solution to the length-n
problem includes just one of these subproblem solutions (after we have cut off the
ﬁrst piece), independence of subproblems is not an issue.
Overlapping subproblems
The second ingredient that an optimization problem must have for dynamic programming to apply is that the space of subproblems must be “small” in the sense
that a recursive algorithm for the problem solves the same subproblems over and
over, rather than always generating new subproblems. Typically, the total number
of distinct subproblems is a polynomial in the input size. When a recursive algorithm revisits the same problem repeatedly, we say that the optimization problem
has overlapping subproblems.4 In contrast, a problem for which a divide-andconquer approach is suitable usually generates brand-new problems at each step
of the recursion. Dynamic-programming algorithms typically take advantage of
overlapping subproblems by solving each subproblem once and then storing the
solution in a table where it can be looked up when needed, using constant time per
lookup.
In Section 15.1, we brieﬂy examined how a recursive solution to rod cutting makes exponentially many calls to ﬁnd solutions of smaller subproblems.
Our dynamic-programming solution takes an exponential-time recursive algorithm
down to quadratic time.
To illustrate the overlapping-subproblems property in greater detail, let us reexamine the matrix-chain multiplication problem. Referring back to Figure 15.5,
observe that MATRIX-CHAIN-ORDER repeatedly looks up the solution to subproblems in lower rows when solving subproblems in higher rows. For example, it
references entry mŒ3; 4 four times: during the computations of mŒ2; 4, mŒ1; 4,
4It may seem strange that dynamic programming relies on subproblems being both independent
and overlapping. Although these requirements may sound contradictory, they describe two different
notions, rather than two points on the same axis. Two subproblems of the same problem are independent if they do not share resources. Two subproblems are overlapping if they are really the same
subproblem that occurs as a subproblem of different problems.

## 15.3 Elements of dynamic programming

1..4
1..1
2..4
1..2
3..4
1..3
4..4
2..2
3..4
2..3
4..4
1..1
2..2
3..3
4..4
1..1
2..3
1..2
3..3
3..3
4..4
2..2
3..3
2..2
3..3
1..1
2..2
Figure 15.7
The recursion tree for the computation of RECURSIVE-MATRIX-CHAIN.p; 1; 4/.
Each node contains the parameters i and j. The computations performed in a shaded subtree are
replaced by a single table lookup in MEMOIZED-MATRIX-CHAIN.
mŒ3; 5, and mŒ3; 6. If we were to recompute mŒ3; 4 each time, rather than just
looking it up, the running time would increase dramatically. To see how, consider
the following (inefﬁcient) recursive procedure that determines mŒi; j , the minimum number of scalar multiplications needed to compute the matrix-chain product
Ai::j D AiAiC1    Aj. The procedure is based directly on the recurrence (15.7).
RECURSIVE-MATRIX-CHAIN.p; i; j /
if i == j
return 0
mŒi; j  D 1
for k D i to j  1
q D RECURSIVE-MATRIX-CHAIN.p; i; k/
C RECURSIVE-MATRIX-CHAIN.p; k C 1; j /
C pi1pkpj
if q < mŒi; j 
mŒi; j  D q
return mŒi; j 
Figure 15.7 shows the recursion tree produced by the call RECURSIVE-MATRIXCHAIN.p; 1; 4/. Each node is labeled by the values of the parameters i and j .
Observe that some pairs of values occur many times.
In fact, we can show that the time to compute mŒ1; n by this recursive procedure is at least exponential in n. Let T .n/ denote the time taken by RECURSIVEMATRIX-CHAIN to compute an optimal parenthesization of a chain of n matrices.
Because the execution of lines 1–2 and of lines 6–7 each take at least unit time, as

does the multiplication in line 5, inspection of the procedure yields the recurrence
T .1/

1 ;
T .n/

1 C
n1
X
kD1
.T .k/ C T .n  k/ C 1/
for n > 1 :
Noting that for i D 1; 2; : : : ; n  1, each term T .i/ appears once as T .k/ and once
as T .n  k/, and collecting the n  1 1s in the summation together with the 1 out
front, we can rewrite the recurrence as
T .n/  2
n1
X
iD1
T .i/ C n :
(15.8)
We shall prove that T .n/ D .2n/ using the substitution method. Speciﬁcally, we shall show that T .n/  2n1 for all n  1. The basis is easy, since
T .1/  1 D 20. Inductively, for n  2 we have
T .n/

n1
X
iD1
2i1 C n
D
n2
X
iD0
2i C n
D
2.2n1  1/ C n
(by equation (A.5))
D
2n  2 C n

2n1 ;
which completes the proof. Thus, the total amount of work performed by the call
RECURSIVE-MATRIX-CHAIN.p; 1; n/ is at least exponential in n.
Compare this top-down, recursive algorithm (without memoization) with the
bottom-up dynamic-programming algorithm. The latter is more efﬁcient because
it takes advantage of the overlapping-subproblems property. Matrix-chain multiplication has only ‚.n2/ distinct subproblems, and the dynamic-programming
algorithm solves each exactly once. The recursive algorithm, on the other hand,
must again solve each subproblem every time it reappears in the recursion tree.
Whenever a recursion tree for the natural recursive solution to a problem contains
the same subproblem repeatedly, and the total number of distinct subproblems is
small, dynamic programming can improve efﬁciency, sometimes dramatically.

## 15.3 Elements of dynamic programming

Reconstructing an optimal solution
As a practical matter, we often store which choice we made in each subproblem in
a table so that we do not have to reconstruct this information from the costs that we
stored.
For matrix-chain multiplication, the table sŒi; j  saves us a signiﬁcant amount of
work when reconstructing an optimal solution. Suppose that we did not maintain
the sŒi; j  table, having ﬁlled in only the table mŒi; j  containing optimal subproblem costs. We choose from among j  i possibilities when we determine which
subproblems to use in an optimal solution to parenthesizing AiAiC1    Aj, and
j  i is not a constant. Therefore, it would take ‚.j  i/ D !.1/ time to reconstruct which subproblems we chose for a solution to a given problem. By storing
in sŒi; j  the index of the matrix at which we split the product AiAiC1    Aj, we
can reconstruct each choice in O.1/ time.
Memoization
As we saw for the rod-cutting problem, there is an alternative approach to dynamic programming that often offers the efﬁciency of the bottom-up dynamicprogramming approach while maintaining a top-down strategy.
The idea is to
memoize the natural, but inefﬁcient, recursive algorithm. As in the bottom-up approach, we maintain a table with subproblem solutions, but the control structure
for ﬁlling in the table is more like the recursive algorithm.
A memoized recursive algorithm maintains an entry in a table for the solution to
each subproblem. Each table entry initially contains a special value to indicate that
the entry has yet to be ﬁlled in. When the subproblem is ﬁrst encountered as the
recursive algorithm unfolds, its solution is computed and then stored in the table.
Each subsequent time that we encounter this subproblem, we simply look up the
value stored in the table and return it.5
Here is a memoized version of RECURSIVE-MATRIX-CHAIN. Note where it
resembles the memoized top-down method for the rod-cutting problem.
5This approach presupposes that we know the set of all possible subproblem parameters and that we
have established the relationship between table positions and subproblems. Another, more general,
approach is to memoize by using hashing with the subproblem parameters as keys.

MEMOIZED-MATRIX-CHAIN.p/
n D p:length  1
let mŒ1 : : n; 1 : : n be a new table
for i D 1 to n
for j D i to n
mŒi; j  D 1
return LOOKUP-CHAIN.m; p; 1; n/
LOOKUP-CHAIN.m; p; i; j /
if mŒi; j  < 1
return mŒi; j 
if i == j
mŒi; j  D 0
else for k D i to j  1
q D LOOKUP-CHAIN.m; p; i; k/
C LOOKUP-CHAIN.m; p; k C 1; j / C pi1pkpj
if q < mŒi; j 
mŒi; j  D q
return mŒi; j 
The MEMOIZED-MATRIX-CHAIN procedure, like MATRIX-CHAIN-ORDER,
maintains a table mŒ1 : : n; 1 : : n of computed values of mŒi; j , the minimum number of scalar multiplications needed to compute the matrix Ai::j. Each table entry
initially contains the value 1 to indicate that the entry has yet to be ﬁlled in. Upon
calling LOOKUP-CHAIN.m; p; i; j /, if line 1 ﬁnds that mŒi; j  < 1, then the procedure simply returns the previously computed cost mŒi; j  in line 2. Otherwise,
the cost is computed as in RECURSIVE-MATRIX-CHAIN, stored in mŒi; j , and
returned. Thus, LOOKUP-CHAIN.m; p; i; j / always returns the value of mŒi; j ,
but it computes it only upon the ﬁrst call of LOOKUP-CHAIN with these speciﬁc
values of i and j .
Figure 15.7 illustrates how MEMOIZED-MATRIX-CHAIN saves time compared
with RECURSIVE-MATRIX-CHAIN. Shaded subtrees represent values that it looks
up rather than recomputes.
Like the bottom-up dynamic-programming algorithm MATRIX-CHAIN-ORDER,
the procedure MEMOIZED-MATRIX-CHAIN runs in O.n3/ time.
Line 5 of
MEMOIZED-MATRIX-CHAIN executes ‚.n2/ times. We can categorize the calls
of LOOKUP-CHAIN into two types:
1. calls in which mŒi; j  D 1, so that lines 3–9 execute, and
2. calls in which mŒi; j  < 1, so that LOOKUP-CHAIN simply returns in line 2.

## 15.3 Elements of dynamic programming

There are ‚.n2/ calls of the ﬁrst type, one per table entry. All calls of the second type are made as recursive calls by calls of the ﬁrst type. Whenever a given
call of LOOKUP-CHAIN makes recursive calls, it makes O.n/ of them. Therefore, there are O.n3/ calls of the second type in all. Each call of the second type
takes O.1/ time, and each call of the ﬁrst type takes O.n/ time plus the time spent
in its recursive calls. The total time, therefore, is O.n3/. Memoization thus turns
an .2n/-time algorithm into an O.n3/-time algorithm.
In summary, we can solve the matrix-chain multiplication problem by either a
top-down, memoized dynamic-programming algorithm or a bottom-up dynamicprogramming algorithm in O.n3/ time.
Both methods take advantage of the
overlapping-subproblems property. There are only ‚.n2/ distinct subproblems in
total, and either of these methods computes the solution to each subproblem only
once. Without memoization, the natural recursive algorithm runs in exponential
time, since solved subproblems are repeatedly solved.
In general practice, if all subproblems must be solved at least once, a bottom-up
dynamic-programming algorithm usually outperforms the corresponding top-down
memoized algorithm by a constant factor, because the bottom-up algorithm has no
overhead for recursion and less overhead for maintaining the table. Moreover, for
some problems we can exploit the regular pattern of table accesses in the dynamicprogramming algorithm to reduce time or space requirements even further. Alternatively, if some subproblems in the subproblem space need not be solved at all,
the memoized solution has the advantage of solving only those subproblems that
are deﬁnitely required.

## Exercises

15.3-1
Which is a more efﬁcient way to determine the optimal number of multiplications
in a matrix-chain multiplication problem: enumerating all the ways of parenthesizing the product and computing the number of multiplications for each, or running
RECURSIVE-MATRIX-CHAIN? Justify your answer.
15.3-2
Draw the recursion tree for the MERGE-SORT procedure from Section 2.3.1 on an
array of 16 elements. Explain why memoization fails to speed up a good divideand-conquer algorithm such as MERGE-SORT.
15.3-3
Consider a variant of the matrix-chain multiplication problem in which the goal is
to parenthesize the sequence of matrices so as to maximize, rather than minimize,

the number of scalar multiplications. Does this problem exhibit optimal substructure?
15.3-4
As stated, in dynamic programming we ﬁrst solve the subproblems and then choose
which of them to use in an optimal solution to the problem. Professor Capulet
claims that we do not always need to solve all the subproblems in order to ﬁnd an
optimal solution. She suggests that we can ﬁnd an optimal solution to the matrixchain multiplication problem by always choosing the matrix Ak at which to split
the subproduct AiAiC1    Aj (by selecting k to minimize the quantity pi1pkpj)
before solving the subproblems. Find an instance of the matrix-chain multiplication problem for which this greedy approach yields a suboptimal solution.
15.3-5
Suppose that in the rod-cutting problem of Section 15.1, we also had limit li on the
number of pieces of length i that we are allowed to produce, for i D 1; 2; : : : ; n.
Show that the optimal-substructure property described in Section 15.1 no longer
holds.
15.3-6
Imagine that you wish to exchange one currency for another. You realize that
instead of directly exchanging one currency for another, you might be better off
making a series of trades through other currencies, winding up with the currency
you want. Suppose that you can trade n different currencies, numbered 1; 2; : : : ; n,
where you start with currency 1 and wish to wind up with currency n. You are
given, for each pair of currencies i and j , an exchange rate rij, meaning that if
you start with d units of currency i, you can trade for drij units of currency j .
A sequence of trades may entail a commission, which depends on the number of
trades you make. Let ck be the commission that you are charged when you make k
trades. Show that, if ck D 0 for all k D 1; 2; : : : ; n, then the problem of ﬁnding the
best sequence of exchanges from currency 1 to currency n exhibits optimal substructure. Then show that if commissions ck are arbitrary values, then the problem
of ﬁnding the best sequence of exchanges from currency 1 to currency n does not
necessarily exhibit optimal substructure.

## 15.4 Longest common subsequence

Biological applications often need to compare the DNA of two (or more) different organisms.
A strand of DNA consists of a string of molecules called

## 15.4 Longest common subsequence

bases, where the possible bases are adenine, guanine, cytosine, and thymine.
Representing each of these bases by its initial letter, we can express a strand
of DNA as a string over the ﬁnite set fA; C; G; Tg.
(See Appendix C for
the deﬁnition of a string.)
For example, the DNA of one organism may be
S1 D ACCGGTCGAGTGCGCGGAAGCCGGCCGAA, and the DNA of another organism may be S2 D GTCGTTCGGAATGCCGTTGCTCTGTAAA. One reason to compare two strands of DNA is to determine how “similar” the two strands are, as some
measure of how closely related the two organisms are. We can, and do, deﬁne similarity in many different ways. For example, we can say that two DNA strands are
similar if one is a substring of the other. (Chapter 32 explores algorithms to solve
this problem.) In our example, neither S1 nor S2 is a substring of the other. Alternatively, we could say that two strands are similar if the number of changes needed
to turn one into the other is small. (Problem 15-5 looks at this notion.) Yet another
way to measure the similarity of strands S1 and S2 is by ﬁnding a third strand S3
in which the bases in S3 appear in each of S1 and S2; these bases must appear
in the same order, but not necessarily consecutively. The longer the strand S3 we
can ﬁnd, the more similar S1 and S2 are. In our example, the longest strand S3 is
GTCGTCGGAAGCCGGCCGAA.
We formalize this last notion of similarity as the longest-common-subsequence
problem. A subsequence of a given sequence is just the given sequence with zero or
more elements left out. Formally, given a sequence X D hx1; x2; : : : ; xmi, another
sequence Z D h´1; ´2; : : : ; ´ki is a subsequence of X if there exists a strictly
increasing sequence hi1;i2;: : : ;iki of indices of X such that for all j D 1; 2; : : : ; k,
we have xij D ´j. For example, Z D hB; C; D; Bi is a subsequence of X D
hA; B; C; B; D; A; Bi with corresponding index sequence h2; 3; 5; 7i.
Given two sequences X and Y , we say that a sequence Z is a common subsequence of X and Y if Z is a subsequence of both X and Y . For example, if
X D hA;B;C;B;D;A;Bi and Y D hB;D;C;A;B;Ai, the sequence hB;C;Ai is
a common subsequence of both X and Y . The sequence hB; C; Ai is not a longest
common subsequence (LCS) of X and Y , however, since it has length 3 and the
sequence hB; C; B; Ai, which is also common to both X and Y , has length 4. The
sequence hB; C; B; Ai is an LCS of X and Y , as is the sequence hB; D; A; Bi,
since X and Y have no common subsequence of length 5 or greater.
In the longest-common-subsequence problem, we are given two sequences
X D hx1; x2; : : : ; xmi and Y D hy1; y2; : : : ; yni and wish to ﬁnd a maximumlength common subsequence of X and Y . This section shows how to efﬁciently
solve the LCS problem using dynamic programming.

Step 1: Characterizing a longest common subsequence
In a brute-force approach to solving the LCS problem, we would enumerate all
subsequences of X and check each subsequence to see whether it is also a subsequence of Y , keeping track of the longest subsequence we ﬁnd. Each subsequence
of X corresponds to a subset of the indices f1; 2; : : : ; mg of X. Because X has 2m
subsequences, this approach requires exponential time, making it impractical for
long sequences.
The LCS problem has an optimal-substructure property, however, as the following theorem shows. As we shall see, the natural classes of subproblems correspond to pairs of “preﬁxes” of the two input sequences. To be precise, given a
sequence X D hx1;x2;: : : ;xmi, we deﬁne the ith preﬁx of X, for i D 0; 1; : : : ; m,
as Xi D hx1; x2; : : : ; xii. For example, if X D hA; B; C; B; D; A; Bi, then
X4 D hA; B; C; Bi and X0 is the empty sequence.

> **Theorem 15.1 (Optimal substructure of an LCS)**

Let X D hx1; x2; : : : ; xmi and Y D hy1; y2; : : : ; yni be sequences, and let Z D
h´1; ´2; : : : ; ´ki be any LCS of X and Y .
1. If xm D yn, then ´k D xm D yn and Zk1 is an LCS of Xm1 and Yn1.
2. If xm ¤ yn, then ´k ¤ xm implies that Z is an LCS of Xm1 and Y .
3. If xm ¤ yn, then ´k ¤ yn implies that Z is an LCS of X and Yn1.
Proof
(1) If ´k ¤ xm, then we could append xm D yn to Z to obtain a common
subsequence of X and Y of length k C 1, contradicting the supposition that Z is
a longest common subsequence of X and Y . Thus, we must have ´k D xm D yn.
Now, the preﬁx Zk1 is a length-.k  1/ common subsequence of Xm1 and Yn1.
We wish to show that it is an LCS. Suppose for the purpose of contradiction
that there exists a common subsequence W of Xm1 and Yn1 with length greater
than k  1. Then, appending xm D yn to W produces a common subsequence of
X and Y whose length is greater than k, which is a contradiction.
(2) If ´k ¤ xm, then Z is a common subsequence of Xm1 and Y . If there were a
common subsequence W of Xm1 and Y with length greater than k, then W would
also be a common subsequence of Xm and Y , contradicting the assumption that Z
is an LCS of X and Y .
(3) The proof is symmetric to (2).
The way that Theorem 15.1 characterizes longest common subsequences tells
us that an LCS of two sequences contains within it an LCS of preﬁxes of the two
sequences. Thus, the LCS problem has an optimal-substructure property. A recur15.4
Longest common subsequence
sive solution also has the overlapping-subproblems property, as we shall see in a
moment.
Step 2: A recursive solution

> **Theorem 15.1 implies that we should examine either one or two subproblems when**

ﬁnding an LCS of X D hx1; x2; : : : ; xmi and Y D hy1; y2; : : : ; yni. If xm D yn,
we must ﬁnd an LCS of Xm1 and Yn1. Appending xm D yn to this LCS yields
an LCS of X and Y . If xm ¤ yn, then we must solve two subproblems: ﬁnding an
LCS of Xm1 and Y and ﬁnding an LCS of X and Yn1. Whichever of these two
LCSs is longer is an LCS of X and Y . Because these cases exhaust all possibilities,
we know that one of the optimal subproblem solutions must appear within an LCS
of X and Y .
We can readily see the overlapping-subproblems property in the LCS problem.
To ﬁnd an LCS of X and Y , we may need to ﬁnd the LCSs of X and Yn1 and
of Xm1 and Y . But each of these subproblems has the subsubproblem of ﬁnding
an LCS of Xm1 and Yn1. Many other subproblems share subsubproblems.
As in the matrix-chain multiplication problem, our recursive solution to the LCS
problem involves establishing a recurrence for the value of an optimal solution.
Let us deﬁne cŒi; j  to be the length of an LCS of the sequences Xi and Yj. If
either i D 0 or j D 0, one of the sequences has length 0, and so the LCS has
length 0. The optimal substructure of the LCS problem gives the recursive formula
cŒi; j  D

if i D 0 or j D 0 ;
cŒi  1; j  1 C 1
if i; j > 0 and xi D yj ;
max.cŒi; j  1; cŒi  1; j /
if i; j > 0 and xi ¤ yj :
(15.9)
Observe that in this recursive formulation, a condition in the problem restricts
which subproblems we may consider. When xi D yj, we can and should consider
the subproblem of ﬁnding an LCS of Xi1 and Yj1. Otherwise, we instead consider the two subproblems of ﬁnding an LCS of Xi and Yj1 and of Xi1 and Yj. In
the previous dynamic-programming algorithms we have examined—for rod cutting
and matrix-chain multiplication—we ruled out no subproblems due to conditions
in the problem. Finding an LCS is not the only dynamic-programming algorithm
that rules out subproblems based on conditions in the problem. For example, the
edit-distance problem (see Problem 15-5) has this characteristic.
Step 3: Computing the length of an LCS
Based on equation (15.9), we could easily write an exponential-time recursive algorithm to compute the length of an LCS of two sequences. Since the LCS problem

has only ‚.mn/ distinct subproblems, however, we can use dynamic programming
to compute the solutions bottom up.
Procedure LCS-LENGTH takes two sequences X D hx1; x2; : : : ; xmi and
Y D hy1;y2;: : : ;yni as inputs. It stores the cŒi; j  values in a table cŒ0 : : m; 0 : : n,
and it computes the entries in row-major order. (That is, the procedure ﬁlls in the
ﬁrst row of c from left to right, then the second row, and so on.) The procedure also
maintains the table bŒ1 : : m; 1 : : n to help us construct an optimal solution. Intuitively, bŒi; j  points to the table entry corresponding to the optimal subproblem
solution chosen when computing cŒi; j . The procedure returns the b and c tables;
cŒm; n contains the length of an LCS of X and Y .
LCS-LENGTH.X; Y /
m D X:length
n D Y:length
let bŒ1 : : m; 1 : : n and cŒ0 : : m; 0 : : n be new tables
for i D 1 to m
cŒi; 0 D 0
for j D 0 to n
cŒ0; j  D 0
for i D 1 to m
for j D 1 to n
if xi == yj
cŒi; j  D cŒi  1; j  1 C 1
bŒi; j  D “-”
elseif cŒi  1; j   cŒi; j  1
cŒi; j  D cŒi  1; j 
bŒi; j  D “"”
else cŒi; j  D cŒi; j  1
bŒi; j  D “ ”
return c and b
Figure 15.8 shows the tables produced by LCS-LENGTH on the sequences X D
hA; B; C; B; D; A; Bi and Y D hB; D; C; A; B; Ai. The running time of the
procedure is ‚.mn/, since each table entry takes ‚.1/ time to compute.
Step 4: Constructing an LCS
The b table returned by LCS-LENGTH enables us to quickly construct an LCS of
X D hx1; x2; : : : ; xmi and Y D hy1; y2; : : : ; yni. We simply begin at bŒm; n and
trace through the table by following the arrows. Whenever we encounter a “-” in
entry bŒi; j , it implies that xi D yj is an element of the LCS that LCS-LENGTH

## 15.4 Longest common subsequence

B
D
C
A
B
A
A
B
C
B
D
A
B
j
i
xi
yj
Figure 15.8
The c and b tables computed by LCS-LENGTH on the sequences X D hA; B; C; B;
D;A;Bi and Y D hB;D;C;A;B;Ai. The square in row i and column j contains the value of cŒi; j
and the appropriate arrow for the value of bŒi; j. The entry 4 in cŒ7; 6—the lower right-hand corner
of the table—is the length of an LCS hB; C; B; Ai of X and Y . For i; j > 0, entry cŒi; j depends
only on whether xi D yj and the values in entries cŒi  1; j, cŒi; j  1, and cŒi  1; j  1, which
are computed before cŒi; j. To reconstruct the elements of an LCS, follow the bŒi; j arrows from
the lower right-hand corner; the sequence is shaded. Each “-” on the shaded sequence corresponds
to an entry (highlighted) for which xi D yj is a member of an LCS.
found. With this method, we encounter the elements of this LCS in reverse order.
The following recursive procedure prints out an LCS of X and Y in the proper,
forward order. The initial call is PRINT-LCS.b; X; X:length; Y:length/.
PRINT-LCS.b; X; i; j /
if i == 0 or j == 0
return
if bŒi; j  == “-”
PRINT-LCS.b; X; i  1; j  1/
print xi
elseif bŒi; j  == “"”
PRINT-LCS.b; X; i  1; j /
else PRINT-LCS.b; X; i; j  1/
For the b table in Figure 15.8, this procedure prints BCBA. The procedure takes
time O.m C n/, since it decrements at least one of i and j in each recursive call.

Improving the code
Once you have developed an algorithm, you will often ﬁnd that you can improve
on the time or space it uses. Some changes can simplify the code and improve
constant factors but otherwise yield no asymptotic improvement in performance.
Others can yield substantial asymptotic savings in time and space.
In the LCS algorithm, for example, we can eliminate the b table altogether. Each
cŒi; j  entry depends on only three other c table entries: cŒi  1; j  1, cŒi  1; j ,
and cŒi; j  1. Given the value of cŒi; j , we can determine in O.1/ time which of
these three values was used to compute cŒi; j , without inspecting table b. Thus, we
can reconstruct an LCS in O.mCn/ time using a procedure similar to PRINT-LCS.
(Exercise 15.4-2 asks you to give the pseudocode.) Although we save ‚.mn/ space
by this method, the auxiliary space requirement for computing an LCS does not
asymptotically decrease, since we need ‚.mn/ space for the c table anyway.
We can, however, reduce the asymptotic space requirements for LCS-LENGTH,
since it needs only two rows of table c at a time: the row being computed and the
previous row. (In fact, as Exercise 15.4-4 asks you to show, we can use only slightly
more than the space for one row of c to compute the length of an LCS.) This
improvement works if we need only the length of an LCS; if we need to reconstruct
the elements of an LCS, the smaller table does not keep enough information to
retrace our steps in O.m C n/ time.

## Exercises

15.4-1
Determine an LCS of h1; 0; 0; 1; 0; 1; 0; 1i and h0; 1; 0; 1; 1; 0; 1; 1; 0i.
15.4-2
Give pseudocode to reconstruct an LCS from the completed c table and the original
sequences X D hx1; x2; : : : ; xmi and Y D hy1; y2; : : : ; yni in O.m C n/ time,
without using the b table.
15.4-3
Give a memoized version of LCS-LENGTH that runs in O.mn/ time.
15.4-4
Show how to compute the length of an LCS using only 2min.m; n/ entries in the c
table plus O.1/ additional space. Then show how to do the same thing, but using
min.m; n/ entries plus O.1/ additional space.

## 15.5 Optimal binary search trees

15.4-5
Give an O.n2/-time algorithm to ﬁnd the longest monotonically increasing subsequence of a sequence of n numbers.
15.4-6
?
Give an O.n lg n/-time algorithm to ﬁnd the longest monotonically increasing subsequence of a sequence of n numbers. (Hint: Observe that the last element of a
candidate subsequence of length i is at least as large as the last element of a candidate subsequence of length i  1. Maintain candidate subsequences by linking
them through the input sequence.)

## 15.5 Optimal binary search trees

Suppose that we are designing a program to translate text from English to French.
For each occurrence of each English word in the text, we need to look up its French
equivalent. We could perform these lookup operations by building a binary search
tree with n English words as keys and their French equivalents as satellite data.
Because we will search the tree for each individual word in the text, we want the
total time spent searching to be as low as possible. We could ensure an O.lg n/
search time per occurrence by using a red-black tree or any other balanced binary
search tree. Words appear with different frequencies, however, and a frequently
used word such as the may appear far from the root while a rarely used word such
as machicolation appears near the root. Such an organization would slow down the
translation, since the number of nodes visited when searching for a key in a binary
search tree equals one plus the depth of the node containing the key. We want
words that occur frequently in the text to be placed nearer the root.6 Moreover,
some words in the text might have no French translation,7 and such words would
not appear in the binary search tree at all. How do we organize a binary search tree
so as to minimize the number of nodes visited in all searches, given that we know
how often each word occurs?
What we need is known as an optimal binary search tree. Formally, we are
given a sequence K D hk1; k2; : : : ; kni of n distinct keys in sorted order (so that
k1 < k2 <    < kn), and we wish to build a binary search tree from these keys.
For each key ki, we have a probability pi that a search will be for ki. Some
searches may be for values not in K, and so we also have n C 1 “dummy keys”
6If the subject of the text is castle architecture, we might want machicolation to appear near the root.
7Yes, machicolation has a French counterpart: mˆachicoulis.

k2
k1
k4
k3
k5
d0
d1
d2
d3
d4
d5
(a)
k2
k1
k4
k3
k5
d0
d1
d2
d3
d4
d5
(b)
Figure 15.9
Two binary search trees for a set of n D 5 keys with the following probabilities:
i
pi
0.15
0.10
0.05
0.10
0.20
qi
0.05
0.10
0.05
0.05
0.05
0.10
(a) A binary search tree with expected search cost 2.80. (b) A binary search tree with expected search
cost 2.75. This tree is optimal.
d0; d1; d2; : : : ; dn representing values not in K. In particular, d0 represents all values less than k1, dn represents all values greater than kn, and for i D 1; 2; : : : ; n1,
the dummy key di represents all values between ki and kiC1. For each dummy
key di, we have a probability qi that a search will correspond to di. Figure 15.9
shows two binary search trees for a set of n D 5 keys. Each key ki is an internal
node, and each dummy key di is a leaf. Every search is either successful (ﬁnding
some key ki) or unsuccessful (ﬁnding some dummy key di), and so we have
n
X
iD1
pi C
n
X
iD0
qi D 1 :
(15.10)
Because we have probabilities of searches for each key and each dummy key,
we can determine the expected cost of a search in a given binary search tree T . Let
us assume that the actual cost of a search equals the number of nodes examined,
i.e., the depth of the node found by the search in T , plus 1. Then the expected cost
of a search in T is
E Œsearch cost in T  D
n
X
iD1
.depthT .ki/ C 1/  pi C
n
X
iD0
.depthT .di/ C 1/  qi
D 1 C
n
X
iD1
depthT .ki/  pi C
n
X
iD0
depthT .di/  qi ;
(15.11)

## 15.5 Optimal binary search trees

where depthT denotes a node’s depth in the tree T . The last equality follows from
equation (15.10). In Figure 15.9(a), we can calculate the expected search cost node
by node:
node
depth
probability
contribution
k1
0.15
0.30
k2
0.10
0.10
k3
0.05
0.15
k4
0.10
0.20
k5
0.20
0.60
d0
0.05
0.15
d1
0.10
0.30
d2
0.05
0.20
d3
0.05
0.20
d4
0.05
0.20
d5
0.10

## 0.40 Total

## 2.80 For a given set of probabilities, we wish to construct a binary search tree whose

expected search cost is smallest. We call such a tree an optimal binary search tree.
Figure 15.9(b) shows an optimal binary search tree for the probabilities given in
the ﬁgure caption; its expected cost is 2.75. This example shows that an optimal
binary search tree is not necessarily a tree whose overall height is smallest. Nor
can we necessarily construct an optimal binary search tree by always putting the
key with the greatest probability at the root. Here, key k5 has the greatest search
probability of any key, yet the root of the optimal binary search tree shown is k2.
(The lowest expected cost of any binary search tree with k5 at the root is 2.85.)
As with matrix-chain multiplication, exhaustive checking of all possibilities fails
to yield an efﬁcient algorithm. We can label the nodes of any n-node binary tree
with the keys k1; k2; : : : ; kn to construct a binary search tree, and then add in the
dummy keys as leaves. In Problem 12-4, we saw that the number of binary trees
with n nodes is .4n=n3=2/, and so we would have to examine an exponential
number of binary search trees in an exhaustive search. Not surprisingly, we shall
solve this problem with dynamic programming.
Step 1: The structure of an optimal binary search tree
To characterize the optimal substructure of optimal binary search trees, we start
with an observation about subtrees. Consider any subtree of a binary search tree.
It must contain keys in a contiguous range ki; : : : ; kj, for some 1  i  j  n.
In addition, a subtree that contains keys ki; : : : ; kj must also have as its leaves the
dummy keys di1; : : : ; dj .
Now we can state the optimal substructure: if an optimal binary search tree T
has a subtree T 0 containing keys ki; : : : ; kj, then this subtree T 0 must be optimal as

well for the subproblem with keys ki; : : : ; kj and dummy keys di1; : : : ; dj. The
usual cut-and-paste argument applies. If there were a subtree T 00 whose expected
cost is lower than that of T 0, then we could cut T 0 out of T and paste in T 00,
resulting in a binary search tree of lower expected cost than T , thus contradicting
the optimality of T .
We need to use the optimal substructure to show that we can construct an optimal solution to the problem from optimal solutions to subproblems. Given keys
ki; : : : ; kj , one of these keys, say kr (i  r  j ), is the root of an optimal
subtree containing these keys. The left subtree of the root kr contains the keys
ki; : : : ; kr1 (and dummy keys di1; : : : ; dr1), and the right subtree contains the
keys krC1; : : : ; kj (and dummy keys dr; : : : ; dj). As long as we examine all candidate roots kr, where i  r  j , and we determine all optimal binary search trees
containing ki; : : : ; kr1 and those containing krC1; : : : ; kj , we are guaranteed that
we will ﬁnd an optimal binary search tree.
There is one detail worth noting about “empty” subtrees. Suppose that in a
subtree with keys ki; : : : ; kj, we select ki as the root. By the above argument, ki’s
left subtree contains the keys ki; : : : ; ki1. We interpret this sequence as containing
no keys. Bear in mind, however, that subtrees also contain dummy keys. We adopt
the convention that a subtree containing keys ki; : : : ; ki1 has no actual keys but
does contain the single dummy key di1. Symmetrically, if we select kj as the root,
then kj’s right subtree contains the keys kjC1; : : : ; kj ; this right subtree contains
no actual keys, but it does contain the dummy key dj.
Step 2: A recursive solution
We are ready to deﬁne the value of an optimal solution recursively. We pick our
subproblem domain as ﬁnding an optimal binary search tree containing the keys
ki; : : : ; kj , where i  1, j  n, and j  i  1. (When j D i  1, there
are no actual keys; we have just the dummy key di1.) Let us deﬁne eŒi; j  as
the expected cost of searching an optimal binary search tree containing the keys
ki; : : : ; kj . Ultimately, we wish to compute eŒ1; n.
The easy case occurs when j D i  1. Then we have just the dummy key di1.
The expected search cost is eŒi; i  1 D qi1.
When j  i, we need to select a root kr from among ki; : : : ; kj and then make an
optimal binary search tree with keys ki; : : : ; kr1 as its left subtree and an optimal
binary search tree with keys krC1; : : : ; kj as its right subtree. What happens to the
expected search cost of a subtree when it becomes a subtree of a node? The depth
of each node in the subtree increases by 1. By equation (15.11), the expected search
cost of this subtree increases by the sum of all the probabilities in the subtree. For
a subtree with keys ki; : : : ; kj , let us denote this sum of probabilities as

## 15.5 Optimal binary search trees

w.i; j / D
j
X
lDi
pl C
j
X
lDi1
ql :
(15.12)
Thus, if kr is the root of an optimal subtree containing keys ki; : : : ; kj, we have
eŒi; j  D pr C .eŒi; r  1 C w.i; r  1// C .eŒr C 1; j  C w.r C 1; j // :
Noting that
w.i; j / D w.i; r  1/ C pr C w.r C 1; j / ;
we rewrite eŒi; j  as
eŒi; j  D eŒi; r  1 C eŒr C 1; j  C w.i; j / :
(15.13)
The recursive equation (15.13) assumes that we know which node kr to use as
the root. We choose the root that gives the lowest expected search cost, giving us
our ﬁnal recursive formulation:
eŒi; j  D
(
qi1
if j D i  1 ;
min
irj feŒi; r  1 C eŒr C 1; j  C w.i; j /g if i  j :
(15.14)
The eŒi; j  values give the expected search costs in optimal binary search trees.
To help us keep track of the structure of optimal binary search trees, we deﬁne
rootŒi; j , for 1  i  j  n, to be the index r for which kr is the root of an
optimal binary search tree containing keys ki; : : : ; kj . Although we will see how
to compute the values of rootŒi; j , we leave the construction of an optimal binary
search tree from these values as Exercise 15.5-1.
Step 3: Computing the expected search cost of an optimal binary search tree
At this point, you may have noticed some similarities between our characterizations
of optimal binary search trees and matrix-chain multiplication. For both problem
domains, our subproblems consist of contiguous index subranges. A direct, recursive implementation of equation (15.14) would be as inefﬁcient as a direct, recursive matrix-chain multiplication algorithm. Instead, we store the eŒi; j  values in a
table eŒ1 : : nC1; 0 : : n. The ﬁrst index needs to run to nC1 rather than n because
in order to have a subtree containing only the dummy key dn, we need to compute
and store eŒn C 1; n. The second index needs to start from 0 because in order to
have a subtree containing only the dummy key d0, we need to compute and store
eŒ1; 0. We use only the entries eŒi; j  for which j  i  1. We also use a table
rootŒi; j , for recording the root of the subtree containing keys ki; : : : ; kj . This
table uses only the entries for which 1  i  j  n.
We will need one other table for efﬁciency. Rather than compute the value
of w.i; j / from scratch every time we are computing eŒi; j —which would take

‚.j  i/ additions—we store these values in a table wŒ1 : : n C 1; 0 : : n. For the
base case, we compute wŒi; i  1 D qi1 for 1  i  n C 1. For j  i, we
compute
wŒi; j  D wŒi; j  1 C pj C qj :
(15.15)
Thus, we can compute the ‚.n2/ values of wŒi; j  in ‚.1/ time each.
The pseudocode that follows takes as inputs the probabilities p1; : : : ; pn and
q0; : : : ; qn and the size n, and it returns the tables e and root.
OPTIMAL-BST.p; q; n/
let eŒ1 : : n C 1; 0 : : n, wŒ1 : : n C 1; 0 : : n,
and rootŒ1 : : n; 1 : : n be new tables
for i D 1 to n C 1
eŒi; i  1 D qi1
wŒi; i  1 D qi1
for l D 1 to n
for i D 1 to n  l C 1
j D i C l  1
eŒi; j  D 1
wŒi; j  D wŒi; j  1 C pj C qj
for r D i to j
t D eŒi; r  1 C eŒr C 1; j  C wŒi; j 
if t < eŒi; j 
eŒi; j  D t
rootŒi; j  D r
return e and root
From the description above and the similarity to the MATRIX-CHAIN-ORDER procedure in Section 15.2, you should ﬁnd the operation of this procedure to be fairly
straightforward.
The for loop of lines 2–4 initializes the values of eŒi; i  1
and wŒi; i  1. The for loop of lines 5–14 then uses the recurrences (15.14)
and (15.15) to compute eŒi; j  and wŒi; j  for all 1  i  j  n. In the ﬁrst iteration, when l D 1, the loop computes eŒi; i and wŒi; i for i D 1; 2; : : : ; n. The second iteration, with l D 2, computes eŒi; iC1 and wŒi; iC1 for i D 1; 2; : : : ; n1,
and so forth. The innermost for loop, in lines 10–14, tries each candidate index r
to determine which key kr to use as the root of an optimal binary search tree containing keys ki; : : : ; kj . This for loop saves the current value of the index r in
rootŒi; j  whenever it ﬁnds a better key to use as the root.
Figure 15.10 shows the tables eŒi; j , wŒi; j , and rootŒi; j  computed by the
procedure OPTIMAL-BST on the key distribution shown in Figure 15.9. As in the
matrix-chain multiplication example of Figure 15.5, the tables are rotated to make

## 15.5 Optimal binary search trees

2.75
1.75
1.25
0.90
0.45
0.05
2.00
1.20
0.70
0.40
0.10
1.30
0.60
0.25
0.05
0.90
0.30
0.05
0.50
0.05
0.10
e
j
i
1.00
0.70
0.55
0.45
0.30
0.05
0.80
0.50
0.35
0.25
0.10
0.60
0.30
0.15
0.05
0.50
0.20
0.05
0.35
0.05
0.10
w
j
i
root
j
i
Figure 15.10
The tables eŒi; j, wŒi; j, and rootŒi; j computed by OPTIMAL-BST on the key
distribution shown in Figure 15.9. The tables are rotated so that the diagonals run horizontally.
the diagonals run horizontally. OPTIMAL-BST computes the rows from bottom to
top and from left to right within each row.
The OPTIMAL-BST procedure takes ‚.n3/ time, just like MATRIX-CHAINORDER. We can easily see that its running time is O.n3/, since its for loops are
nested three deep and each loop index takes on at most n values. The loop indices in
OPTIMAL-BST do not have exactly the same bounds as those in MATRIX-CHAINORDER, but they are within at most 1 in all directions. Thus, like MATRIX-CHAINORDER, the OPTIMAL-BST procedure takes .n3/ time.

## Exercises

15.5-1
Write pseudocode for the procedure CONSTRUCT-OPTIMAL-BST.root/ which,
given the table root, outputs the structure of an optimal binary search tree. For the
example in Figure 15.10, your procedure should print out the structure

k2 is the root
k1 is the left child of k2
d0 is the left child of k1
d1 is the right child of k1
k5 is the right child of k2
k4 is the left child of k5
k3 is the left child of k4
d2 is the left child of k3
d3 is the right child of k3
d4 is the right child of k4
d5 is the right child of k5
corresponding to the optimal binary search tree shown in Figure 15.9(b).
15.5-2
Determine the cost and structure of an optimal binary search tree for a set of n D 7
keys with the following probabilities:
i
pi
0.04
0.06
0.08
0.02
0.10
0.12
0.14
qi
0.06
0.06
0.06
0.06
0.05
0.05
0.05
0.05
15.5-3
Suppose that instead of maintaining the table wŒi; j , we computed the value
of w.i; j / directly from equation (15.12) in line 9 of OPTIMAL-BST and used this
computed value in line 11. How would this change affect the asymptotic running
time of OPTIMAL-BST?
15.5-4
?
Knuth [212] has shown that there are always roots of optimal subtrees such that
rootŒi; j  1  rootŒi; j   rootŒi C 1; j  for all 1  i < j  n. Use this fact to
modify the OPTIMAL-BST procedure to run in ‚.n2/ time.

## Problems

15-1
Longest simple path in a directed acyclic graph
Suppose that we are given a directed acyclic graph G D .V; E/ with realvalued edge weights and two distinguished vertices s and t. Describe a dynamicprogramming approach for ﬁnding a longest weighted simple path from s to t.
What does the subproblem graph look like? What is the efﬁciency of your algorithm?

Problems for Chapter 15
(a)
(b)
Figure 15.11
Seven points in the plane, shown on a unit grid. (a) The shortest closed tour, with
length approximately 24:89. This tour is not bitonic. (b) The shortest bitonic tour for the same set of
points. Its length is approximately 25:58.
15-2
Longest palindrome subsequence
A palindrome is a nonempty string over some alphabet that reads the same forward and backward. Examples of palindromes are all strings of length 1, civic,
racecar, and aibohphobia (fear of palindromes).
Give an efﬁcient algorithm to ﬁnd the longest palindrome that is a subsequence
of a given input string. For example, given the input character, your algorithm
should return carac. What is the running time of your algorithm?
15-3
Bitonic euclidean traveling-salesman problem
In the euclidean traveling-salesman problem, we are given a set of n points in
the plane, and we wish to ﬁnd the shortest closed tour that connects all n points.
Figure 15.11(a) shows the solution to a 7-point problem. The general problem is
NP-hard, and its solution is therefore believed to require more than polynomial
time (see Chapter 34).
J. L. Bentley has suggested that we simplify the problem by restricting our attention to bitonic tours, that is, tours that start at the leftmost point, go strictly
rightward to the rightmost point, and then go strictly leftward back to the starting
point. Figure 15.11(b) shows the shortest bitonic tour of the same 7 points. In this
case, a polynomial-time algorithm is possible.
Describe an O.n2/-time algorithm for determining an optimal bitonic tour. You
may assume that no two points have the same x-coordinate and that all operations
on real numbers take unit time. (Hint: Scan left to right, maintaining optimal possibilities for the two parts of the tour.)
15-4
Printing neatly
Consider the problem of neatly printing a paragraph with a monospaced font (all
characters having the same width) on a printer. The input text is a sequence of n

words of lengths l1; l2; : : : ; ln, measured in characters. We want to print this paragraph neatly on a number of lines that hold a maximum of M characters each. Our
criterion of “neatness” is as follows. If a given line contains words i through j ,
where i  j , and we leave exactly one space between words, the number of extra
space characters at the end of the line is M  j C i  Pj
kDi lk, which must be
nonnegative so that the words ﬁt on the line. We wish to minimize the sum, over
all lines except the last, of the cubes of the numbers of extra space characters at the
ends of lines. Give a dynamic-programming algorithm to print a paragraph of n
words neatly on a printer. Analyze the running time and space requirements of
your algorithm.
15-5
Edit distance
In order to transform one source string of text xŒ1 : : m to a target string yŒ1 : : n,
we can perform various transformation operations. Our goal is, given x and y,
to produce a series of transformations that change x to y.
We use an array ´—assumed to be large enough to hold all the characters it will need—to hold
the intermediate results. Initially, ´ is empty, and at termination, we should have
´Œj  D yŒj  for j D 1; 2; : : : ; n. We maintain current indices i into x and j into ´,
and the operations are allowed to alter ´ and these indices. Initially, i D j D 1.
We are required to examine every character in x during the transformation, which
means that at the end of the sequence of transformation operations, we must have
i D m C 1.
We may choose from among six transformation operations:
Copy a character from x to ´ by setting ´Œj  D xŒi and then incrementing both i
and j . This operation examines xŒi.
Replace a character from x by another character c, by setting ´Œj  D c, and then
incrementing both i and j . This operation examines xŒi.
Delete a character from x by incrementing i but leaving j alone. This operation
examines xŒi.
Insert the character c into ´ by setting ´Œj  D c and then incrementing j , but
leaving i alone. This operation examines no characters of x.
Twiddle (i.e., exchange) the next two characters by copying them from x to ´ but
in the opposite order; we do so by setting ´Œj  D xŒi C 1 and ´Œj C 1 D xŒi
and then setting i D i C 2 and j D j C 2. This operation examines xŒi
and xŒi C 1.
Kill the remainder of x by setting i D m C 1. This operation examines all characters in x that have not yet been examined. This operation, if performed, must
be the ﬁnal operation.

Problems for Chapter 15
As an example, one way to transform the source string algorithm to the target
string altruistic is to use the following sequence of operations, where the
underlined characters are xŒi and ´Œj  after the operation:
Operation
x
´
initial strings
algorithm
copy
algorithm
a
copy
algorithm
al
replace by t
algorithm
alt
delete
algorithm
alt
copy
algorithm
altr
insert u
algorithm
altru
insert i
algorithm
altrui
insert s
algorithm
altruis
twiddle
algorithm
altruisti
insert c
algorithm
altruistic
kill
algorithm
altruistic
Note that there are several other sequences of transformation operations that transform algorithm to altruistic.
Each of the transformation operations has an associated cost. The cost of an
operation depends on the speciﬁc application, but we assume that each operation’s
cost is a constant that is known to us. We also assume that the individual costs of
the copy and replace operations are less than the combined costs of the delete and
insert operations; otherwise, the copy and replace operations would not be used.
The cost of a given sequence of transformation operations is the sum of the costs
of the individual operations in the sequence. For the sequence above, the cost of
transforming algorithm to altruistic is
.3  cost.copy// C cost.replace/ C cost.delete/ C .4  cost.insert//
C cost.twiddle/ C cost.kill/ :
a. Given two sequences xŒ1 : : m and yŒ1 : : n and set of transformation-operation
costs, the edit distance from x to y is the cost of the least expensive operation
sequence that transforms x to y. Describe a dynamic-programming algorithm
that ﬁnds the edit distance from xŒ1 : : m to yŒ1 : : n and prints an optimal operation sequence. Analyze the running time and space requirements of your
algorithm.
The edit-distance problem generalizes the problem of aligning two DNA sequences
(see, for example, Setubal and Meidanis [310, Section 3.2]). There are several
methods for measuring the similarity of two DNA sequences by aligning them.
One such method to align two sequences x and y consists of inserting spaces at

arbitrary locations in the two sequences (including at either end) so that the resulting sequences x0 and y0 have the same length but do not have a space in the same
position (i.e., for no position j are both x0Œj  and y0Œj  a space). Then we assign a
“score” to each position. Position j receives a score as follows:

C1 if x0Œj  D y0Œj  and neither is a space,

1 if x0Œj  ¤ y0Œj  and neither is a space,

2 if either x0Œj  or y0Œj  is a space.
The score for the alignment is the sum of the scores of the individual positions. For
example, given the sequences x D GATCGGCAT and y D CAATGTGAATC, one
alignment is
G ATCG GCAT
CAAT GTGAATC
A + under a position indicates a score of C1 for that position, a - indicates a score
of 1, and a * indicates a score of 2, so that this alignment has a total score of
6  1  2  1  4  2 D 4.
b. Explain how to cast the problem of ﬁnding an optimal alignment as an edit
distance problem using a subset of the transformation operations copy, replace,
delete, insert, twiddle, and kill.
15-6
Planning a company party
Professor Stewart is consulting for the president of a corporation that is planning
a company party. The company has a hierarchical structure; that is, the supervisor
relation forms a tree rooted at the president. The personnel ofﬁce has ranked each
employee with a conviviality rating, which is a real number. In order to make the
party fun for all attendees, the president does not want both an employee and his
or her immediate supervisor to attend.
Professor Stewart is given the tree that describes the structure of the corporation,
using the left-child, right-sibling representation described in Section 10.4. Each
node of the tree holds, in addition to the pointers, the name of an employee and
that employee’s conviviality ranking. Describe an algorithm to make up a guest
list that maximizes the sum of the conviviality ratings of the guests. Analyze the
running time of your algorithm.
15-7
Viterbi algorithm
We can use dynamic programming on a directed graph G D .V; E/ for speech
recognition. Each edge .u; / 2 E is labeled with a sound 	.u; / from a ﬁnite set † of sounds. The labeled graph is a formal model of a person speaking

Problems for Chapter 15
a restricted language. Each path in the graph starting from a distinguished vertex 0 2 V corresponds to a possible sequence of sounds produced by the model.
We deﬁne the label of a directed path to be the concatenation of the labels of the
edges on that path.
a. Describe an efﬁcient algorithm that, given an edge-labeled graph G with distinguished vertex 0 and a sequence s D h	1; 	2; : : : ; 	ki of sounds from †,
returns a path in G that begins at 0 and has s as its label, if any such path exists.
Otherwise, the algorithm should return NO-SUCH-PATH. Analyze the running
time of your algorithm. (Hint: You may ﬁnd concepts from Chapter 22 useful.)
Now, suppose that every edge .u; / 2 E has an associated nonnegative probability p.u; / of traversing the edge .u; / from vertex u and thus producing the
corresponding sound. The sum of the probabilities of the edges leaving any vertex
equals 1. The probability of a path is deﬁned to be the product of the probabilities of its edges. We can view the probability of a path beginning at 0 as the
probability that a “random walk” beginning at 0 will follow the speciﬁed path,
where we randomly choose which edge to take leaving a vertex u according to the
probabilities of the available edges leaving u.
b. Extend your answer to part (a) so that if a path is returned, it is a most probable path starting at 0 and having label s. Analyze the running time of your
algorithm.
15-8
Image compression by seam carving
We are given a color picture consisting of an m 	 n array AŒ1 : : m; 1 : : n of pixels,
where each pixel speciﬁes a triple of red, green, and blue (RGB) intensities. Suppose that we wish to compress this picture slightly. Speciﬁcally, we wish to remove
one pixel from each of the m rows, so that the whole picture becomes one pixel
narrower. To avoid disturbing visual effects, however, we require that the pixels
removed in two adjacent rows be in the same or adjacent columns; the pixels removed form a “seam” from the top row to the bottom row where successive pixels
in the seam are adjacent vertically or diagonally.
a. Show that the number of such possible seams grows at least exponentially in m,
assuming that n > 1.
b. Suppose now that along with each pixel AŒi; j , we have calculated a realvalued disruption measure dŒi; j , indicating how disruptive it would be to
remove pixel AŒi; j . Intuitively, the lower a pixel’s disruption measure, the
more similar the pixel is to its neighbors. Suppose further that we deﬁne the
disruption measure of a seam to be the sum of the disruption measures of its
pixels.

Give an algorithm to ﬁnd a seam with the lowest disruption measure. How
efﬁcient is your algorithm?
15-9
Breaking a string
A certain string-processing language allows a programmer to break a string into
two pieces. Because this operation copies the string, it costs n time units to break
a string of n characters into two pieces. Suppose a programmer wants to break
a string into many pieces. The order in which the breaks occur can affect the
total amount of time used. For example, suppose that the programmer wants to
break a 20-character string after characters 2, 8, and 10 (numbering the characters
in ascending order from the left-hand end, starting from 1). If she programs the
breaks to occur in left-to-right order, then the ﬁrst break costs 20 time units, the
second break costs 18 time units (breaking the string from characters 3 to 20 at
character 8), and the third break costs 12 time units, totaling 50 time units. If she
programs the breaks to occur in right-to-left order, however, then the ﬁrst break
costs 20 time units, the second break costs 10 time units, and the third break costs
8 time units, totaling 38 time units. In yet another order, she could break ﬁrst at 8
(costing 20), then break the left piece at 2 (costing 8), and ﬁnally the right piece
at 10 (costing 12), for a total cost of 40.
Design an algorithm that, given the numbers of characters after which to break,
determines a least-cost way to sequence those breaks. More formally, given a
string S with n characters and an array LŒ1 : : m containing the break points, compute the lowest cost for a sequence of breaks, along with a sequence of breaks that
achieves this cost.
15-10
Planning an investment strategy
Your knowledge of algorithms helps you obtain an exciting job with the Acme
Computer Company, along with a $10,000 signing bonus. You decide to invest
this money with the goal of maximizing your return at the end of 10 years. You
decide to use the Amalgamated Investment Company to manage your investments.
Amalgamated Investments requires you to observe the following rules. It offers n
different investments, numbered 1 through n. In each year j , investment i provides
a return rate of rij. In other words, if you invest d dollars in investment i in year j ,
then at the end of year j , you have drij dollars. The return rates are guaranteed,
that is, you are given all the return rates for the next 10 years for each investment.
You make investment decisions only once per year. At the end of each year, you
can leave the money made in the previous year in the same investments, or you
can shift money to other investments, by either shifting money between existing
investments or moving money to a new investement. If you do not move your
money between two consecutive years, you pay a fee of f1 dollars, whereas if you
switch your money, you pay a fee of f2 dollars, where f2 > f1.

Problems for Chapter 15
a. The problem, as stated, allows you to invest your money in multiple investments
in each year. Prove that there exists an optimal investment strategy that, in
each year, puts all the money into a single investment. (Recall that an optimal
investment strategy maximizes the amount of money after 10 years and is not
concerned with any other objectives, such as minimizing risk.)
b. Prove that the problem of planning your optimal investment strategy exhibits
optimal substructure.
c. Design an algorithm that plans your optimal investment strategy. What is the
running time of your algorithm?
d. Suppose that Amalgamated Investments imposed the additional restriction that,
at any point, you can have no more than $15,000 in any one investment. Show
that the problem of maximizing your income at the end of 10 years no longer
exhibits optimal substructure.
15-11
Inventory planning
The Rinky Dink Company makes machines that resurface ice rinks. The demand
for such products varies from month to month, and so the company needs to develop a strategy to plan its manufacturing given the ﬂuctuating, but predictable,
demand. The company wishes to design a plan for the next n months. For each
month i, the company knows the demand di, that is, the number of machines that
it will sell. Let D D Pn
iD1 di be the total demand over the next n months. The
company keeps a full-time staff who provide labor to manufacture up to m machines per month. If the company needs to make more than m machines in a given
month, it can hire additional, part-time labor, at a cost that works out to c dollars
per machine. Furthermore, if, at the end of a month, the company is holding any
unsold machines, it must pay inventory costs. The cost for holding j machines is
given as a function h.j / for j D 1; 2; : : : ; D, where h.j /  0 for 1  j  D and
h.j /  h.j C 1/ for 1  j  D  1.
Give an algorithm that calculates a plan for the company that minimizes its costs
while fulﬁlling all the demand. The running time should be polyomial in n and D.
15-12
Signing free-agent baseball players
Suppose that you are the general manager for a major-league baseball team. During
the off-season, you need to sign some free-agent players for your team. The team
owner has given you a budget of $X to spend on free agents. You are allowed to
spend less than $X altogether, but the owner will ﬁre you if you spend any more
than $X.

You are considering N different positions, and for each position, P free-agent
players who play that position are available.8 Because you do not want to overload
your roster with too many players at any position, for each position you may sign
at most one free agent who plays that position. (If you do not sign any players at a
particular position, then you plan to stick with the players you already have at that
position.)
To determine how valuable a player is going to be, you decide to use a sabermetric statistic9 known as “VORP,” or “value over replacement player.” A player with
a higher VORP is more valuable than a player with a lower VORP. A player with a
higher VORP is not necessarily more expensive to sign than a player with a lower
VORP, because factors other than a player’s value determine how much it costs to
sign him.
For each available free-agent player, you have three pieces of information:

the player’s position,

the amount of money it will cost to sign the player, and

the player’s VORP.
Devise an algorithm that maximizes the total VORP of the players you sign while
spending no more than $X altogether. You may assume that each player signs for a
multiple of $100,000. Your algorithm should output the total VORP of the players
you sign, the total amount of money you spend, and a list of which players you
sign. Analyze the running time and space requirement of your algorithm.
Chapter notes
R. Bellman began the systematic study of dynamic programming in 1955. The
word “programming,” both here and in linear programming, refers to using a tabular solution method. Although optimization techniques incorporating elements of
dynamic programming were known earlier, Bellman provided the area with a solid
mathematical basis [37].
8Although there are nine positions on a baseball team, N is not necesarily equal to 9 because some
general managers have particular ways of thinking about positions. For example, a general manager
might consider right-handed pitchers and left-handed pitchers to be separate “positions,” as well as
starting pitchers, long relief pitchers (relief pitchers who can pitch several innings), and short relief
pitchers (relief pitchers who normally pitch at most only one inning).
9Sabermetrics is the application of statistical analysis to baseball records. It provides several ways
to compare the relative values of individual players.

Notes for Chapter 15
Galil and Park [125] classify dynamic-programming algorithms according to the
size of the table and the number of other table entries each entry depends on. They
call a dynamic-programming algorithm tD=eD if its table size is O.nt/ and each
entry depends on O.ne/ other entries. For example, the matrix-chain multiplication
algorithm in Section 15.2 would be 2D=1D, and the longest-common-subsequence
algorithm in Section 15.4 would be 2D=0D.
Hu and Shing [182, 183] give an O.n lg n/-time algorithm for the matrix-chain
multiplication problem.
The O.mn/-time algorithm for the longest-common-subsequence problem appears to be a folk algorithm. Knuth [70] posed the question of whether subquadratic
algorithms for the LCS problem exist. Masek and Paterson [244] answered this
question in the afﬁrmative by giving an algorithm that runs in O.mn= lg n/ time,
where n  m and the sequences are drawn from a set of bounded size. For the
special case in which no element appears more than once in an input sequence,
Szymanski [326] shows how to solve the problem in O..n C m/ lg.n C m// time.
Many of these results extend to the problem of computing string edit distances
(Problem 15-5).
An early paper on variable-length binary encodings by Gilbert and Moore [133]
had applications to constructing optimal binary search trees for the case in which all
probabilities pi are 0; this paper contains an O.n3/-time algorithm. Aho, Hopcroft,
and Ullman [5] present the algorithm from Section 15.5. Exercise 15.5-4 is due to
Knuth [212]. Hu and Tucker [184] devised an algorithm for the case in which all
probabilities pi are 0 that uses O.n2/ time and O.n/ space; subsequently, Knuth
[211] reduced the time to O.n lg n/.
Problem 15-8 is due to Avidan and Shamir [27], who have posted on the Web a
wonderful video illustrating this image-compression technique.
