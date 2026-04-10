# 35 Approximation Algorithms

35
Approximation Algorithms
Many problems of practical signiﬁcance are NP-complete, yet they are too impor-
tant to abandon merely because we don’t know how to ﬁnd an optimal solution in
polynomial time. Even if a problem is NP-complete, there may be hope. We have at
least three ways to get around NP-completeness. First, if the actual inputs are small,
an algorithm with exponential running time may be perfectly satisfactory. Second,
we may be able to isolate important special cases that we can solve in polynomial
time. Third, we might come up with approaches to ﬁnd near-optimal solutions in
polynomial time (either in the worst case or the expected case). In practice, near-
optimality is often good enough. We call an algorithm that returns near-optimal
solutions an approximation algorithm. This chapter presents polynomial-time ap-
proximation algorithms for several NP-complete problems.
Performance ratios for approximation algorithms
Suppose that we are working on an optimization problem in which each potential
solution has a positive cost, and we wish to ﬁnd a near-optimal solution. Depending
on the problem, we may deﬁne an optimal solution as one with maximum possi-
ble cost or one with minimum possible cost; that is, the problem may be either a
maximization or a minimization problem.
We say that an algorithm for a problem has an approximation ratio of .n/ if,
for any input of size n, the cost C of the solution produced by the algorithm is
within a factor of .n/ of the cost C  of an optimal solution:
max
 C
C  ; C 
C

 .n/ :
(35.1)
If an algorithm achieves an approximation ratio of .n/, we call it a .n/-approx-
imation algorithm.
The deﬁnitions of the approximation ratio and of a .n/-
approximation algorithm apply to both minimization and maximization problems.
For a maximization problem, 0 < C  C , and the ratio C =C gives the factor
by which the cost of an optimal solution is larger than the cost of the approximate

Chapter 35
Approximation Algorithms
1107
solution. Similarly, for a minimization problem, 0 < C   C, and the ratio C=C 
gives the factor by which the cost of the approximate solution is larger than the
cost of an optimal solution. Because we assume that all solutions have positive
cost, these ratios are always well deﬁned. The approximation ratio of an approx-
imation algorithm is never less than 1, since C=C   1 implies C =C  1.
Therefore, a 1-approximation algorithm1 produces an optimal solution, and an ap-
proximation algorithm with a large approximation ratio may return a solution that
is much worse than optimal.
For many problems, we have polynomial-time approximation algorithms with
small constant approximation ratios, although for other problems, the best known
polynomial-time approximation algorithms have approximation ratios that grow
as functions of the input size n. An example of such a problem is the set-cover
problem presented in Section 35.3.
Some NP-complete problems allow polynomial-time approximation algorithms
that can achieve increasingly better approximation ratios by using more and more
computation time. That is, we can trade computation time for the quality of the
approximation. An example is the subset-sum problem studied in Section 35.5.
This situation is important enough to deserve a name of its own.
An approximation scheme for an optimization problem is an approximation al-
gorithm that takes as input not only an instance of the problem, but also a value
 > 0 such that for any ﬁxed , the scheme is a .1 C /-approximation algorithm.
We say that an approximation scheme is a polynomial-time approximation scheme
if for any ﬁxed  > 0, the scheme runs in time polynomial in the size n of its input
instance.
The running time of a polynomial-time approximation scheme can increase very
rapidly as  decreases. For example, the running time of a polynomial-time ap-
proximation scheme might be O.n2=/. Ideally, if  decreases by a constant factor,
the running time to achieve the desired approximation should not increase by more
than a constant factor (though not necessarily the same constant factor by which 
decreased).
We say that an approximation scheme is a fully polynomial-time approximation
scheme if it is an approximation scheme and its running time is polynomial in
both 1= and the size n of the input instance. For example, the scheme might have
a running time of O..1=/2n3/. With such a scheme, any constant-factor decrease
in  comes with a corresponding constant-factor increase in the running time.
1When the approximation ratio is independent of n, we use the terms “approximation ratio of ” and
“-approximation algorithm,” indicating no dependence on n.

1108
Chapter 35
Approximation Algorithms
Chapter outline
The ﬁrst four sections of this chapter present some examples of polynomial-time
approximation algorithms for NP-complete problems, and the ﬁfth section presents
a fully polynomial-time approximation scheme. Section 35.1 begins with a study
of the vertex-cover problem, an NP-complete minimization problem that has an
approximation algorithm with an approximation ratio of 2. Section 35.2 presents
an approximation algorithm with an approximation ratio of 2 for the case of the
traveling-salesman problem in which the cost function satisﬁes the triangle in-
equality. It also shows that without the triangle inequality, for any constant   1,
a -approximation algorithm cannot exist unless P D NP. In Section 35.3, we
show how to use a greedy method as an effective approximation algorithm for the
set-covering problem, obtaining a covering whose cost is at worst a logarithmic
factor larger than the optimal cost. Section 35.4 presents two more approximation
algorithms. First we study the optimization version of 3-CNF satisﬁability and
give a simple randomized algorithm that produces a solution with an expected ap-
proximation ratio of 8=7. Then we examine a weighted variant of the vertex-cover
problem and show how to use linear programming to develop a 2-approximation
algorithm. Finally, Section 35.5 presents a fully polynomial-time approximation
scheme for the subset-sum problem.
35.1
The vertex-cover problem
Section 34.5.2 deﬁned the vertex-cover problem and proved it NP-complete. Recall
that a vertex cover of an undirected graph G D .V; E/ is a subset V 0  V such
that if .u; / is an edge of G, then either u 2 V 0 or  2 V 0 (or both). The size of a
vertex cover is the number of vertices in it.
The vertex-cover problem is to ﬁnd a vertex cover of minimum size in a given
undirected graph. We call such a vertex cover an optimal vertex cover. This prob-
lem is the optimization version of an NP-complete decision problem.
Even though we don’t know how to ﬁnd an optimal vertex cover in a graph G
in polynomial time, we can efﬁciently ﬁnd a vertex cover that is near-optimal.
The following approximation algorithm takes as input an undirected graph G and
returns a vertex cover whose size is guaranteed to be no more than twice the size
of an optimal vertex cover.

35.1
The vertex-cover problem
1109
b
c
d
a
e
f
g
(a)
b
c
d
a
e
f
g
(b)
b
c
d
a
e
f
g
(c)
b
c
d
a
e
f
g
(d)
b
c
d
a
e
f
g
(e)
b
c
d
a
e
f
g
(f)
Figure 35.1
The operation of APPROX-VERTEX-COVER. (a) The input graph G, which has 7
vertices and 8 edges. (b) The edge .b;c/, shown heavy, is the ﬁrst edge chosen by APPROX-VERTEX-
COVER. Vertices b and c, shown lightly shaded, are added to the set C containing the vertex cover
being created. Edges .a; b/, .c; e/, and .c; d/, shown dashed, are removed since they are now covered
by some vertex in C. (c) Edge .e; f / is chosen; vertices e and f are added to C. (d) Edge .d; g/
is chosen; vertices d and g are added to C. (e) The set C, which is the vertex cover produced by
APPROX-VERTEX-COVER, contains the six vertices b; c; d; e; f; g. (f) The optimal vertex cover for
this problem contains only three vertices: b, d, and e.
APPROX-VERTEX-COVER.G/
1
C D ;
2
E0 D G:E
3
while E0 ¤ ;
4
let .u; / be an arbitrary edge of E0
5
C D C [ fu; g
6
remove from E0 every edge incident on either u or 
7
return C
Figure 35.1 illustrates how APPROX-VERTEX-COVER operates on an example
graph. The variable C contains the vertex cover being constructed. Line 1 ini-
tializes C to the empty set. Line 2 sets E0 to be a copy of the edge set G:E of
the graph. The loop of lines 3–6 repeatedly picks an edge .u; / from E0, adds its

1110
Chapter 35
Approximation Algorithms
endpoints u and  to C, and deletes all edges in E0 that are covered by either u
or . Finally, line 7 returns the vertex cover C. The running time of this algorithm
is O.V C E/, using adjacency lists to represent E0.
Theorem 35.1
APPROX-VERTEX-COVER is a polynomial-time 2-approximation algorithm.
Proof
We have already shown that APPROX-VERTEX-COVER runs in polyno-
mial time.
The set C of vertices that is returned by APPROX-VERTEX-COVER is a vertex
cover, since the algorithm loops until every edge in G:E has been covered by some
vertex in C.
To see that APPROX-VERTEX-COVER returns a vertex cover that is at most twice
the size of an optimal cover, let A denote the set of edges that line 4 of APPROX-
VERTEX-COVER picked. In order to cover the edges in A, any vertex cover—in
particular, an optimal cover C —must include at least one endpoint of each edge
in A. No two edges in A share an endpoint, since once an edge is picked in line 4,
all other edges that are incident on its endpoints are deleted from E0 in line 6. Thus,
no two edges in A are covered by the same vertex from C , and we have the lower
bound
jC j  jAj
(35.2)
on the size of an optimal vertex cover. Each execution of line 4 picks an edge for
which neither of its endpoints is already in C, yielding an upper bound (an exact
upper bound, in fact) on the size of the vertex cover returned:
jCj D 2 jAj :
(35.3)
Combining equations (35.2) and (35.3), we obtain
jCj
D
2 jAj

2 jC j ;
thereby proving the theorem.
Let us reﬂect on this proof. At ﬁrst, you might wonder how we can possibly
prove that the size of the vertex cover returned by APPROX-VERTEX-COVER is at
most twice the size of an optimal vertex cover, when we do not even know the size
of an optimal vertex cover. Instead of requiring that we know the exact size of an
optimal vertex cover, we rely on a lower bound on the size. As Exercise 35.1-2 asks
you to show, the set A of edges that line 4 of APPROX-VERTEX-COVER selects is
actually a maximal matching in the graph G. (A maximal matching is a matching
that is not a proper subset of any other matching.) The size of a maximal matching

35.2
The traveling-salesman problem
1111
is, as we argued in the proof of Theorem 35.1, a lower bound on the size of an
optimal vertex cover. The algorithm returns a vertex cover whose size is at most
twice the size of the maximal matching A. By relating the size of the solution
returned to the lower bound, we obtain our approximation ratio. We will use this
methodology in later sections as well.
Exercises
35.1-1
Give an example of a graph for which APPROX-VERTEX-COVER always yields a
suboptimal solution.
35.1-2
Prove that the set of edges picked in line 4 of APPROX-VERTEX-COVER forms a
maximal matching in the graph G.
35.1-3
?
Professor B¨undchen proposes the following heuristic to solve the vertex-cover
problem. Repeatedly select a vertex of highest degree, and remove all of its in-
cident edges. Give an example to show that the professor’s heuristic does not have
an approximation ratio of 2. (Hint: Try a bipartite graph with vertices of uniform
degree on the left and vertices of varying degree on the right.)
35.1-4
Give an efﬁcient greedy algorithm that ﬁnds an optimal vertex cover for a tree in
linear time.
35.1-5
From the proof of Theorem 34.12, we know that the vertex-cover problem and the
NP-complete clique problem are complementary in the sense that an optimal vertex
cover is the complement of a maximum-size clique in the complement graph. Does
this relationship imply that there is a polynomial-time approximation algorithm
with a constant approximation ratio for the clique problem? Justify your answer.
35.2
The traveling-salesman problem
In the traveling-salesman problem introduced in Section 34.5.4, we are given a
complete undirected graph G D .V; E/ that has a nonnegative integer cost c.u; /
associated with each edge .u; / 2 E, and we must ﬁnd a hamiltonian cycle (a
tour) of G with minimum cost. As an extension of our notation, let c.A/ denote
the total cost of the edges in the subset A  E:

1112
Chapter 35
Approximation Algorithms
c.A/ D
X
.u;/2A
c.u; / :
In many practical situations, the least costly way to go from a place u to a place w
is to go directly, with no intermediate steps. Put another way, cutting out an inter-
mediate stop never increases the cost. We formalize this notion by saying that the
cost function c satisﬁes the triangle inequality if, for all vertices u; ; w 2 V ,
c.u; w/  c.u; / C c.; w/ :
The triangle inequality seems as though it should naturally hold, and it is au-
tomatically satisﬁed in several applications. For example, if the vertices of the
graph are points in the plane and the cost of traveling between two vertices is the
ordinary euclidean distance between them, then the triangle inequality is satisﬁed.
Furthermore, many cost functions other than euclidean distance satisfy the triangle
inequality.
As Exercise 35.2-2 shows, the traveling-salesman problem is NP-complete even
if we require that the cost function satisfy the triangle inequality. Thus, we should
not expect to ﬁnd a polynomial-time algorithm for solving this problem exactly.
Instead, we look for good approximation algorithms.
In Section 35.2.1, we examine a 2-approximation algorithm for the traveling-
salesman problem with the triangle inequality. In Section 35.2.2, we show that
without the triangle inequality, a polynomial-time approximation algorithm with a
constant approximation ratio does not exist unless P D NP.
35.2.1
The traveling-salesman problem with the triangle inequality
Applying the methodology of the previous section, we shall ﬁrst compute a struc-
ture—a minimum spanning tree—whose weight gives a lower bound on the length
of an optimal traveling-salesman tour. We shall then use the minimum spanning
tree to create a tour whose cost is no more than twice that of the minimum spanning
tree’s weight, as long as the cost function satisﬁes the triangle inequality. The fol-
lowing algorithm implements this approach, calling the minimum-spanning-tree
algorithm MST-PRIM from Section 23.2 as a subroutine. The parameter G is a
complete undirected graph, and the cost function c satisﬁes the triangle inequality.
APPROX-TSP-TOUR.G; c/
1
select a vertex r 2 G:V to be a “root” vertex
2
compute a minimum spanning tree T for G from root r
using MST-PRIM.G; c; r/
3
let H be a list of vertices, ordered according to when they are ﬁrst visited
in a preorder tree walk of T
4
return the hamiltonian cycle H

35.2
The traveling-salesman problem
1113
(a)
a
d
b
f
e
g
c
h
(b)
a
d
b
f
e
g
c
h
(c)
a
d
e
c
h
(d)
a
d
b
f
e
g
c
h
(e)
b
f
g
e
h
c
a
b
f
g
d
Figure 35.2
The operation of APPROX-TSP-TOUR. (a) A complete undirected graph. Vertices lie
on intersections of integer grid lines. For example, f is one unit to the right and two units up from h.
The cost function between two points is the ordinary euclidean distance. (b) A minimum spanning
tree T of the complete graph, as computed by MST-PRIM. Vertex a is the root vertex. Only edges
in the minimum spanning tree are shown. The vertices happen to be labeled in such a way that they
are added to the main tree by MST-PRIM in alphabetical order. (c) A walk of T , starting at a. A
full walk of the tree visits the vertices in the order a; b; c; b; h; b; a; d; e; f; e; g; e; d; a. A preorder
walk of T lists a vertex just when it is ﬁrst encountered, as indicated by the dot next to each vertex,
yielding the ordering a; b; c; h; d; e; f; g. (d) A tour obtained by visiting the vertices in the order
given by the preorder walk, which is the tour H returned by APPROX-TSP-TOUR. Its total cost
is approximately 19:074. (e) An optimal tour H  for the original complete graph. Its total cost is
approximately 14:715.
Recall from Section 12.1 that a preorder tree walk recursively visits every vertex
in the tree, listing a vertex when it is ﬁrst encountered, before visiting any of its
children.
Figure 35.2 illustrates the operation of APPROX-TSP-TOUR. Part (a) of the ﬁg-
ure shows a complete undirected graph, and part (b) shows the minimum spanning
tree T grown from root vertex a by MST-PRIM. Part (c) shows how a preorder
walk of T visits the vertices, and part (d) displays the corresponding tour, which is
the tour returned by APPROX-TSP-TOUR. Part (e) displays an optimal tour, which
is about 23% shorter.

1114
Chapter 35
Approximation Algorithms
By Exercise 23.2-2, even with a simple implementation of MST-PRIM, the run-
ning time of APPROX-TSP-TOUR is ‚.V 2/. We now show that if the cost function
for an instance of the traveling-salesman problem satisﬁes the triangle inequality,
then APPROX-TSP-TOUR returns a tour whose cost is not more than twice the cost
of an optimal tour.
Theorem 35.2
APPROX-TSP-TOUR is a polynomial-time 2-approximation algorithm for the
traveling-salesman problem with the triangle inequality.
Proof
We have already seen that APPROX-TSP-TOUR runs in polynomial time.
Let H  denote an optimal tour for the given set of vertices. We obtain a spanning
tree by deleting any edge from a tour, and each edge cost is nonnegative. Therefore,
the weight of the minimum spanning tree T computed in line 2 of APPROX-TSP-
TOUR provides a lower bound on the cost of an optimal tour:
c.T /  c.H / :
(35.4)
A full walk of T lists the vertices when they are ﬁrst visited and also whenever
they are returned to after a visit to a subtree. Let us call this full walk W . The full
walk of our example gives the order
a; b; c; b; h; b; a; d; e; f; e; g; e; d; a :
Since the full walk traverses every edge of T exactly twice, we have (extending
our deﬁnition of the cost c in the natural manner to handle multisets of edges)
c.W / D 2c.T / :
(35.5)
Inequality (35.4) and equation (35.5) imply that
c.W /  2c.H / ;
(35.6)
and so the cost of W is within a factor of 2 of the cost of an optimal tour.
Unfortunately, the full walk W is generally not a tour, since it visits some ver-
tices more than once. By the triangle inequality, however, we can delete a visit to
any vertex from W and the cost does not increase. (If we delete a vertex  from W
between visits to u and w, the resulting ordering speciﬁes going directly from u
to w.) By repeatedly applying this operation, we can remove from W all but the
ﬁrst visit to each vertex. In our example, this leaves the ordering
a; b; c; h; d; e; f; g :
This ordering is the same as that obtained by a preorder walk of the tree T . Let H
be the cycle corresponding to this preorder walk. It is a hamiltonian cycle, since ev-

35.2
The traveling-salesman problem
1115
ery vertex is visited exactly once, and in fact it is the cycle computed by APPROX-
TSP-TOUR. Since H is obtained by deleting vertices from the full walk W , we
have
c.H/  c.W / :
(35.7)
Combining inequalities (35.6) and (35.7) gives c.H/  2c.H /, which completes
the proof.
In spite of the nice approximation ratio provided by Theorem 35.2, APPROX-
TSP-TOUR is usually not the best practical choice for this problem. There are other
approximation algorithms that typically perform much better in practice. (See the
references at the end of this chapter.)
35.2.2
The general traveling-salesman problem
If we drop the assumption that the cost function c satisﬁes the triangle inequality,
then we cannot ﬁnd good approximate tours in polynomial time unless P D NP.
Theorem 35.3
If P ¤ NP, then for any constant   1, there is no polynomial-time approximation
algorithm with approximation ratio  for the general traveling-salesman problem.
Proof
The proof is by contradiction. Suppose to the contrary that for some num-
ber   1, there is a polynomial-time approximation algorithm A with approx-
imation ratio . Without loss of generality, we assume that  is an integer, by
rounding it up if necessary. We shall then show how to use A to solve instances
of the hamiltonian-cycle problem (deﬁned in Section 34.2) in polynomial time.
Since Theorem 34.13 tells us that the hamiltonian-cycle problem is NP-complete,
Theorem 34.4 implies that if we can solve it in polynomial time, then P D NP.
Let G D .V; E/ be an instance of the hamiltonian-cycle problem. We wish to
determine efﬁciently whether G contains a hamiltonian cycle by making use of
the hypothesized approximation algorithm A. We turn G into an instance of the
traveling-salesman problem as follows. Let G0 D .V; E0/ be the complete graph
on V ; that is,
E0 D f.u; / W u;  2 V and u ¤ g :
Assign an integer cost to each edge in E0 as follows:
c.u; / D
(
1
if .u; / 2 E ;
 jV j C 1
otherwise :
We can create representations of G0 and c from a representation of G in time poly-
nomial in jV j and jEj.

1116
Chapter 35
Approximation Algorithms
Now, consider the traveling-salesman problem .G0; c/. If the original graph G
has a hamiltonian cycle H, then the cost function c assigns to each edge of H a
cost of 1, and so .G0; c/ contains a tour of cost jV j. On the other hand, if G does
not contain a hamiltonian cycle, then any tour of G0 must use some edge not in E.
But any tour that uses an edge not in E has a cost of at least
. jV j C 1/ C .jV j  1/
D
 jV j C jV j
>
 jV j :
Because edges not in G are so costly, there is a gap of at least  jV j between the cost
of a tour that is a hamiltonian cycle in G (cost jV j) and the cost of any other tour
(cost at least  jV j C jV j). Therefore, the cost of a tour that is not a hamiltonian
cycle in G is at least a factor of  C 1 greater than the cost of a tour that is a
hamiltonian cycle in G.
Now, suppose that we apply the approximation algorithm A to the traveling-
salesman problem .G0; c/. Because A is guaranteed to return a tour of cost no
more than  times the cost of an optimal tour, if G contains a hamiltonian cycle,
then A must return it. If G has no hamiltonian cycle, then A returns a tour of cost
more than  jV j. Therefore, we can use A to solve the hamiltonian-cycle problem
in polynomial time.
The proof of Theorem 35.3 serves as an example of a general technique for
proving that we cannot approximate a problem very well. Suppose that given an
NP-hard problem X, we can produce in polynomial time a minimization prob-
lem Y such that “yes” instances of X correspond to instances of Y with value at
most k (for some k), but that “no” instances of X correspond to instances of Y
with value greater than k. Then, we have shown that, unless P D NP, there is no
polynomial-time -approximation algorithm for problem Y .
Exercises
35.2-1
Suppose that a complete undirected graph G D .V; E/ with at least 3 vertices has
a cost function c that satisﬁes the triangle inequality. Prove that c.u; /  0 for all
u;  2 V .
35.2-2
Show how in polynomial time we can transform one instance of the traveling-
salesman problem into another instance whose cost function satisﬁes the triangle
inequality. The two instances must have the same set of optimal tours. Explain
why such a polynomial-time transformation does not contradict Theorem 35.3, as-
suming that P ¤ NP.

35.3
The set-covering problem
1117
35.2-3
Consider the following closest-point heuristic for building an approximate trav-
eling-salesman tour whose cost function satisﬁes the triangle inequality. Begin
with a trivial cycle consisting of a single arbitrarily chosen vertex. At each step,
identify the vertex u that is not on the cycle but whose distance to any vertex on the
cycle is minimum. Suppose that the vertex on the cycle that is nearest u is vertex .
Extend the cycle to include u by inserting u just after . Repeat until all vertices
are on the cycle. Prove that this heuristic returns a tour whose total cost is not more
than twice the cost of an optimal tour.
35.2-4
In the bottleneck traveling-salesman problem, we wish to ﬁnd the hamiltonian cy-
cle that minimizes the cost of the most costly edge in the cycle. Assuming that the
cost function satisﬁes the triangle inequality, show that there exists a polynomial-
time approximation algorithm with approximation ratio 3 for this problem. (Hint:
Show recursively that we can visit all the nodes in a bottleneck spanning tree, as
discussed in Problem 23-3, exactly once by taking a full walk of the tree and skip-
ping nodes, but without skipping more than two consecutive intermediate nodes.
Show that the costliest edge in a bottleneck spanning tree has a cost that is at most
the cost of the costliest edge in a bottleneck hamiltonian cycle.)
35.2-5
Suppose that the vertices for an instance of the traveling-salesman problem are
points in the plane and that the cost c.u; / is the euclidean distance between
points u and . Show that an optimal tour never crosses itself.
35.3
The set-covering problem
The set-covering problem is an optimization problem that models many problems
that require resources to be allocated. Its corresponding decision problem general-
izes the NP-complete vertex-cover problem and is therefore also NP-hard. The ap-
proximation algorithm developed to handle the vertex-cover problem doesn’t apply
here, however, and so we need to try other approaches. We shall examine a simple
greedy heuristic with a logarithmic approximation ratio. That is, as the size of the
instance gets larger, the size of the approximate solution may grow, relative to the
size of an optimal solution. Because the logarithm function grows rather slowly,
however, this approximation algorithm may nonetheless give useful results.

1118
Chapter 35
Approximation Algorithms
S3
S6
S4
S5
S2
S1
Figure 35.3
An instance .X; F / of the set-covering problem, where X consists of the 12 black
points and F D fS1; S2; S3; S4; S5; S6g. A minimum-size set cover is C D fS3; S4; S5g, with
size 3. The greedy algorithm produces a cover of size 4 by selecting either the sets S1, S4, S5,
and S3 or the sets S1, S4, S5, and S6, in order.
An instance .X; F / of the set-covering problem consists of a ﬁnite set X and
a family F of subsets of X, such that every element of X belongs to at least one
subset in F :
X D
[
S2F
S :
We say that a subset S 2 F covers its elements. The problem is to ﬁnd a minimum-
size subset C  F whose members cover all of X:
X D
[
S2C
S :
(35.8)
We say that any C satisfying equation (35.8) covers X. Figure 35.3 illustrates the
set-covering problem. The size of C is the number of sets it contains, rather than
the number of individual elements in these sets, since every subset C that covers X
must contain all jXj individual elements. In Figure 35.3, the minimum set cover
has size 3.
The set-covering problem abstracts many commonly arising combinatorial prob-
lems. As a simple example, suppose that X represents a set of skills that are needed
to solve a problem and that we have a given set of people available to work on the
problem. We wish to form a committee, containing as few people as possible,
such that for every requisite skill in X, at least one member of the committee has
that skill. In the decision version of the set-covering problem, we ask whether a
covering exists with size at most k, where k is an additional parameter speciﬁed
in the problem instance. The decision version of the problem is NP-complete, as
Exercise 35.3-2 asks you to show.

35.3
The set-covering problem
1119
A greedy approximation algorithm
The greedy method works by picking, at each stage, the set S that covers the great-
est number of remaining elements that are uncovered.
GREEDY-SET-COVER.X; F /
1
U D X
2
C D ;
3
while U ¤ ;
4
select an S 2 F that maximizes jS \ U j
5
U D U  S
6
C D C [ fSg
7
return C
In the example of Figure 35.3, GREEDY-SET-COVER adds to C, in order, the sets
S1, S4, and S5, followed by either S3 or S6.
The algorithm works as follows. The set U contains, at each stage, the set of
remaining uncovered elements. The set C contains the cover being constructed.
Line 4 is the greedy decision-making step, choosing a subset S that covers as many
uncovered elements as possible (breaking ties arbitrarily). After S is selected,
line 5 removes its elements from U , and line 6 places S into C. When the algorithm
terminates, the set C contains a subfamily of F that covers X.
We can easily implement GREEDY-SET-COVER to run in time polynomial in jXj
and jF j. Since the number of iterations of the loop on lines 3–6 is bounded from
above by min.jXj ; jF j/, and we can implement the loop body to run in time
O.jXj jF j/, a simple implementation runs in time O.jXj jF j min.jXj ; jF j//. Ex-
ercise 35.3-3 asks for a linear-time algorithm.
Analysis
We now show that the greedy algorithm returns a set cover that is not too much
larger than an optimal set cover. For convenience, in this chapter we denote the dth
harmonic number Hd D Pd
iD1 1=i (see Section A.1) by H.d/. As a boundary
condition, we deﬁne H.0/ D 0.
Theorem 35.4
GREEDY-SET-COVER is a polynomial-time .n/-approximation algorithm, where
.n/ D H.max fjSj W S 2 F g/ :
Proof
We have already shown that GREEDY-SET-COVER runs in polynomial
time.

1120
Chapter 35
Approximation Algorithms
To show that GREEDY-SET-COVER is a .n/-approximation algorithm, we as-
sign a cost of 1 to each set selected by the algorithm, distribute this cost over
the elements covered for the ﬁrst time, and then use these costs to derive the de-
sired relationship between the size of an optimal set cover C  and the size of the
set cover C returned by the algorithm. Let Si denote the ith subset selected by
GREEDY-SET-COVER; the algorithm incurs a cost of 1 when it adds Si to C. We
spread this cost of selecting Si evenly among the elements covered for the ﬁrst time
by Si. Let cx denote the cost allocated to element x, for each x 2 X. Each element
is assigned a cost only once, when it is covered for the ﬁrst time. If x is covered
for the ﬁrst time by Si, then
cx D
1
jSi  .S1 [ S2 [    [ Si1/j :
Each step of the algorithm assigns 1 unit of cost, and so
jCj D
X
x2X
cx :
(35.9)
Each element x 2 X is in at least one set in the optimal cover C , and so we have
X
S2C
X
x2S
cx 
X
x2X
cx :
(35.10)
Combining equation (35.9) and inequality (35.10), we have that
jCj 
X
S2C
X
x2S
cx :
(35.11)
The remainder of the proof rests on the following key inequality, which we shall
prove shortly. For any set S belonging to the family F ,
X
x2S
cx  H.jSj/ :
(35.12)
From inequalities (35.11) and (35.12), it follows that
jCj

X
S2C
H.jSj/

jC j  H.max fjSj W S 2 F g/ ;
thus proving the theorem.
All that remains is to prove inequality (35.12). Consider any set S 2 F and any
i D 1; 2; : : : ; jCj, and let
ui D jS  .S1 [ S2 [    [ Si/j
be the number of elements in S that remain uncovered after the algorithm has
selected sets S1; S2; : : : ; Si. We deﬁne u0 D jSj to be the number of elements

35.3
The set-covering problem
1121
of S, which are all initially uncovered. Let k be the least index such that uk D 0,
so that every element in S is covered by at least one of the sets S1; S2; : : : ; Sk and
some element in S is uncovered by S1 [ S2 [    [ Sk1. Then, ui1  ui, and
ui1  ui elements of S are covered for the ﬁrst time by Si, for i D 1; 2; : : : ; k.
Thus,
X
x2S
cx
D
k
X
iD1
.ui1  ui/ 
1
jSi  .S1 [ S2 [    [ Si1/j :
Observe that
jSi  .S1 [ S2 [    [ Si1/j

jS  .S1 [ S2 [    [ Si1/j
D
ui1 ;
because the greedy choice of Si guarantees that S cannot cover more new ele-
ments than Si does (otherwise, the algorithm would have chosen S instead of Si).
Consequently, we obtain
X
x2S
cx

k
X
iD1
.ui1  ui/ 
1
ui1
:
We now bound this quantity as follows:
X
x2S
cx

k
X
iD1
.ui1  ui/ 
1
ui1
D
k
X
iD1
ui1
X
jDuiC1
1
ui1

k
X
iD1
ui1
X
jDuiC1
1
j
(because j  ui1)
D
k
X
iD1
 ui1
X
jD1
1
j 
ui
X
jD1
1
j
!
D
k
X
iD1
.H.ui1/  H.ui//
D
H.u0/  H.uk/
(because the sum telescopes)
D
H.u0/  H.0/
D
H.u0/
(because H.0/ D 0)
D
H.jSj/ ;
which completes the proof of inequality (35.12).

1122
Chapter 35
Approximation Algorithms
Corollary 35.5
GREEDY-SET-COVER is a polynomial-time .ln jXjC1/-approximation algorithm.
Proof
Use inequality (A.14) and Theorem 35.4.
In some applications, max fjSj W S 2 F g is a small constant, and so the solution
returned by GREEDY-SET-COVER is at most a small constant times larger than
optimal. One such application occurs when this heuristic ﬁnds an approximate
vertex cover for a graph whose vertices have degree at most 3. In this case, the
solution found by GREEDY-SET-COVER is not more than H.3/ D 11=6 times as
large as an optimal solution, a performance guarantee that is slightly better than
that of APPROX-VERTEX-COVER.
Exercises
35.3-1
Consider each of the following words as a set of letters: farid; dash; drain;
heard; lost; nose; shun; slate; snare; threadg. Show which set cover
GREEDY-SET-COVER produces when we break ties in favor of the word that ap-
pears ﬁrst in the dictionary.
35.3-2
Show that the decision version of the set-covering problem is NP-complete by
reducing it from the vertex-cover problem.
35.3-3
Show how to implement GREEDY-SET-COVER in such a way that it runs in time
O
P
S2F jSj

.
35.3-4
Show that the following weaker form of Theorem 35.4 is trivially true:
jCj  jC j max fjSj W S 2 F g :
35.3-5
GREEDY-SET-COVER can return a number of different solutions, depending on
how we break ties in line 4. Give a procedure BAD-SET-COVER-INSTANCE.n/
that returns an n-element instance of the set-covering problem for which, depend-
ing on how we break ties in line 4, GREEDY-SET-COVER can return a number of
different solutions that is exponential in n.

35.4
Randomization and linear programming
1123
35.4
Randomization and linear programming
In this section, we study two useful techniques for designing approximation algo-
rithms: randomization and linear programming. We shall give a simple randomized
algorithm for an optimization version of 3-CNF satisﬁability, and then we shall use
linear programming to help design an approximation algorithm for a weighted ver-
sion of the vertex-cover problem. This section only scratches the surface of these
two powerful techniques. The chapter notes give references for further study of
these areas.
A randomized approximation algorithm for MAX-3-CNF satisﬁability
Just as some randomized algorithms compute exact solutions, some randomized
algorithms compute approximate solutions. We say that a randomized algorithm
for a problem has an approximation ratio of .n/ if, for any input of size n, the
expected cost C of the solution produced by the randomized algorithm is within a
factor of .n/ of the cost C  of an optimal solution:
max
 C
C  ; C 
C

 .n/ :
(35.13)
We call a randomized algorithm that achieves an approximation ratio of .n/ a
randomized .n/-approximation algorithm. In other words, a randomized ap-
proximation algorithm is like a deterministic approximation algorithm, except that
the approximation ratio is for an expected cost.
A particular instance of 3-CNF satisﬁability, as deﬁned in Section 34.4, may or
may not be satisﬁable. In order to be satisﬁable, there must exist an assignment of
the variables so that every clause evaluates to 1. If an instance is not satisﬁable, we
may want to compute how “close” to satisﬁable it is, that is, we may wish to ﬁnd an
assignment of the variables that satisﬁes as many clauses as possible. We call the
resulting maximization problem MAX-3-CNF satisﬁability. The input to MAX-3-
CNF satisﬁability is the same as for 3-CNF satisﬁability, and the goal is to return
an assignment of the variables that maximizes the number of clauses evaluating
to 1. We now show that randomly setting each variable to 1 with probability 1=2
and to 0 with probability 1=2 yields a randomized 8=7-approximation algorithm.
According to the deﬁnition of 3-CNF satisﬁability from Section 34.4, we require
each clause to consist of exactly three distinct literals. We further assume that
no clause contains both a variable and its negation. (Exercise 35.4-1 asks you to
remove this last assumption.)

1124
Chapter 35
Approximation Algorithms
Theorem 35.6
Given an instance of MAX-3-CNF satisﬁability with n variables x1; x2; : : : ; xn
and m clauses, the randomized algorithm that independently sets each vari-
able to 1 with probability 1=2 and to 0 with probability 1=2 is a randomized
8=7-approximation algorithm.
Proof
Suppose that we have independently set each variable to 1 with probabil-
ity 1=2 and to 0 with probability 1=2. For i D 1; 2; : : : ; m, we deﬁne the indicator
random variable
Yi D I fclause i is satisﬁedg ;
so that Yi D 1 as long as we have set at least one of the literals in the ith clause
to 1. Since no literal appears more than once in the same clause, and since we have
assumed that no variable and its negation appear in the same clause, the settings of
the three literals in each clause are independent. A clause is not satisﬁed only if all
three of its literals are set to 0, and so Pr fclause i is not satisﬁedg D .1=2/3 D 1=8.
Thus, we have Pr fclause i is satisﬁedg D 1  1=8 D 7=8, and by Lemma 5.1,
we have E ŒYi D 7=8. Let Y be the number of satisﬁed clauses overall, so that
Y D Y1 C Y2 C    C Ym. Then, we have
E ŒY 
D
E
" m
X
iD1
Yi
#
D
m
X
iD1
E ŒYi
(by linearity of expectation)
D
m
X
iD1
7=8
D
7m=8 :
Clearly, m is an upper bound on the number of satisﬁed clauses, and hence the
approximation ratio is at most m=.7m=8/ D 8=7.
Approximating weighted vertex cover using linear programming
In the minimum-weight vertex-cover problem, we are given an undirected graph
G D .V; E/ in which each vertex  2 V has an associated positive weight w./.
For any vertex cover V 0  V , we deﬁne the weight of the vertex cover w.V 0/ D
P
2V 0 w./. The goal is to ﬁnd a vertex cover of minimum weight.
We cannot apply the algorithm used for unweighted vertex cover, nor can we use
a random solution; both methods may return solutions that are far from optimal.
We shall, however, compute a lower bound on the weight of the minimum-weight

35.4
Randomization and linear programming
1125
vertex cover, by using a linear program. We shall then “round” this solution and
use it to obtain a vertex cover.
Suppose that we associate a variable x./ with each vertex  2 V , and let us
require that x./ equals either 0 or 1 for each  2 V . We put  into the vertex cover
if and only if x./ D 1. Then, we can write the constraint that for any edge .u; /,
at least one of u and  must be in the vertex cover as x.u/ C x./  1. This view
gives rise to the following 0-1 integer program for ﬁnding a minimum-weight
vertex cover:
minimize
X
2V
w./ x./
(35.14)
subject to
x.u/ C x./

1
for each .u; / 2 E
(35.15)
x./
2
f0; 1g
for each  2 V :
(35.16)
In the special case in which all the weights w./ are equal to 1, this formu-
lation is the optimization version of the NP-hard vertex-cover problem.
Sup-
pose, however, that we remove the constraint that x./ 2 f0; 1g and replace it
by 0  x./  1. We then obtain the following linear program, which is known as
the linear-programming relaxation:
minimize
X
2V
w./ x./
(35.17)
subject to
x.u/ C x./

1
for each .u; / 2 E
(35.18)
x./

1
for each  2 V
(35.19)
x./

0
for each  2 V :
(35.20)
Any feasible solution to the 0-1 integer program in lines (35.14)–(35.16) is also
a feasible solution to the linear program in lines (35.17)–(35.20). Therefore, the
value of an optimal solution to the linear program gives a lower bound on the value
of an optimal solution to the 0-1 integer program, and hence a lower bound on the
optimal weight in the minimum-weight vertex-cover problem.
The following procedure uses the solution to the linear-programming relaxation
to construct an approximate solution to the minimum-weight vertex-cover problem:

1126
Chapter 35
Approximation Algorithms
APPROX-MIN-WEIGHT-VC.G; w/
1
C D ;
2
compute Nx, an optimal solution to the linear program in lines (35.17)–(35.20)
3
for each  2 V
4
if Nx./  1=2
5
C D C [ fg
6
return C
The APPROX-MIN-WEIGHT-VC procedure works as follows. Line 1 initial-
izes the vertex cover to be empty.
Line 2 formulates the linear program in
lines (35.17)–(35.20) and then solves this linear program. An optimal solution
gives each vertex  an associated value Nx./, where 0  Nx./  1. We use this
value to guide the choice of which vertices to add to the vertex cover C in lines 3–5.
If Nx./  1=2, we add  to C; otherwise we do not. In effect, we are “rounding”
each fractional variable in the solution to the linear program to 0 or 1 in order to
obtain a solution to the 0-1 integer program in lines (35.14)–(35.16). Finally, line 6
returns the vertex cover C.
Theorem 35.7
Algorithm APPROX-MIN-WEIGHT-VC is a polynomial-time 2-approximation al-
gorithm for the minimum-weight vertex-cover problem.
Proof
Because there is a polynomial-time algorithm to solve the linear program
in line 2, and because the for loop of lines 3–5 runs in polynomial time, APPROX-
MIN-WEIGHT-VC is a polynomial-time algorithm.
Now we show that APPROX-MIN-WEIGHT-VC is a 2-approximation algo-
rithm. Let C  be an optimal solution to the minimum-weight vertex-cover prob-
lem, and let ´ be the value of an optimal solution to the linear program in
lines (35.17)–(35.20). Since an optimal vertex cover is a feasible solution to the
linear program, ´ must be a lower bound on w.C /, that is,
´  w.C / :
(35.21)
Next, we claim that by rounding the fractional values of the variables Nx./, we
produce a set C that is a vertex cover and satisﬁes w.C/  2´. To see that C is
a vertex cover, consider any edge .u; / 2 E. By constraint (35.18), we know that
x.u/ C x./  1, which implies that at least one of Nx.u/ and Nx./ is at least 1=2.
Therefore, at least one of u and  is included in the vertex cover, and so every edge
is covered.
Now, we consider the weight of the cover. We have

35.4
Randomization and linear programming
1127
´
D
X
2V
w./ Nx./

X
2V W Nx./1=2
w./ Nx./

X
2V W Nx./1=2
w./  1
2
D
X
2C
w./  1
2
D
1
2
X
2C
w./
D
1
2w.C/ :
(35.22)
Combining inequalities (35.21) and (35.22) gives
w.C/  2´  2w.C / ;
and hence APPROX-MIN-WEIGHT-VC is a 2-approximation algorithm.
Exercises
35.4-1
Show that even if we allow a clause to contain both a variable and its negation, ran-
domly setting each variable to 1 with probability 1=2 and to 0 with probability 1=2
still yields a randomized 8=7-approximation algorithm.
35.4-2
The MAX-CNF satisﬁability problem is like the MAX-3-CNF satisﬁability prob-
lem, except that it does not restrict each clause to have exactly 3 literals. Give a
randomized 2-approximation algorithm for the MAX-CNF satisﬁability problem.
35.4-3
In the MAX-CUT problem, we are given an unweighted undirected graph G D
.V; E/. We deﬁne a cut .S; V  S/ as in Chapter 23 and the weight of a cut as the
number of edges crossing the cut. The goal is to ﬁnd a cut of maximum weight.
Suppose that for each vertex , we randomly and independently place  in S with
probability 1=2 and in V  S with probability 1=2. Show that this algorithm is a
randomized 2-approximation algorithm.

1128
Chapter 35
Approximation Algorithms
35.4-4
Show that the constraints in line (35.19) are redundant in the sense that if we re-
move them from the linear program in lines (35.17)–(35.20), any optimal solution
to the resulting linear program must satisfy x./  1 for each  2 V .
35.5
The subset-sum problem
Recall from Section 34.5.5 that an instance of the subset-sum problem is a
pair .S; t/, where S is a set fx1; x2; : : : ; xng of positive integers and t is a posi-
tive integer. This decision problem asks whether there exists a subset of S that
adds up exactly to the target value t. As we saw in Section 34.5.5, this problem is
NP-complete.
The optimization problem associated with this decision problem arises in prac-
tical applications.
In the optimization problem, we wish to ﬁnd a subset of
fx1; x2; : : : ; xng whose sum is as large as possible but not larger than t. For ex-
ample, we may have a truck that can carry no more than t pounds, and n different
boxes to ship, the ith of which weighs xi pounds. We wish to ﬁll the truck with as
heavy a load as possible without exceeding the given weight limit.
In this section, we present an exponential-time algorithm that computes the op-
timal value for this optimization problem, and then we show how to modify the
algorithm so that it becomes a fully polynomial-time approximation scheme. (Re-
call that a fully polynomial-time approximation scheme has a running time that is
polynomial in 1= as well as in the size of the input.)
An exponential-time exact algorithm
Suppose that we computed, for each subset S 0 of S, the sum of the elements
in S 0, and then we selected, among the subsets whose sum does not exceed t,
the one whose sum was closest to t. Clearly this algorithm would return the op-
timal solution, but it could take exponential time. To implement this algorithm,
we could use an iterative procedure that, in iteration i, computes the sums of
all subsets of fx1; x2; : : : ; xig, using as a starting point the sums of all subsets
of fx1; x2; : : : ; xi1g. In doing so, we would realize that once a particular subset S 0
had a sum exceeding t, there would be no reason to maintain it, since no super-
set of S 0 could be the optimal solution. We now give an implementation of this
strategy.
The procedure EXACT-SUBSET-SUM takes an input set S D fx1; x2; : : : ; xng
and a target value t; we’ll see its pseudocode in a moment. This procedure it-

35.5
The subset-sum problem
1129
eratively computes Li, the list of sums of all subsets of fx1; : : : ; xig that do not
exceed t, and then it returns the maximum value in Ln.
If L is a list of positive integers and x is another positive integer, then we let
L C x denote the list of integers derived from L by increasing each element of L
by x. For example, if L D h1;2;3;5;9i, then L C 2 D h3;4;5;7;11i. We also use
this notation for sets, so that
S C x D fs C x W s 2 Sg :
We also use an auxiliary procedure MERGE-LISTS.L; L0/, which returns the
sorted list that is the merge of its two sorted input lists L and L0 with duplicate
values removed. Like the MERGE procedure we used in merge sort (Section 2.3.1),
MERGE-LISTS runs in time O.jLj C jL0j/. We omit the pseudocode for MERGE-
LISTS.
EXACT-SUBSET-SUM.S; t/
1
n D jSj
2
L0 D h0i
3
for i D 1 to n
4
Li D MERGE-LISTS.Li1; Li1 C xi/
5
remove from Li every element that is greater than t
6
return the largest element in Ln
To see how EXACT-SUBSET-SUM works, let Pi denote the set of all values
obtained by selecting a (possibly empty) subset of fx1; x2; : : : ; xig and summing
its members. For example, if S D f1; 4; 5g, then
P1
D
f0; 1g ;
P2
D
f0; 1; 4; 5g ;
P3
D
f0; 1; 4; 5; 6; 9; 10g :
Given the identity
Pi D Pi1 [ .Pi1 C xi/ ;
(35.23)
we can prove by induction on i (see Exercise 35.5-1) that the list Li is a sorted list
containing every element of Pi whose value is not more than t. Since the length
of Li can be as much as 2i, EXACT-SUBSET-SUM is an exponential-time algorithm
in general, although it is a polynomial-time algorithm in the special cases in which t
is polynomial in jSj or all the numbers in S are bounded by a polynomial in jSj.
A fully polynomial-time approximation scheme
We can derive a fully polynomial-time approximation scheme for the subset-sum
problem by “trimming” each list Li after it is created. The idea behind trimming is

1130
Chapter 35
Approximation Algorithms
that if two values in L are close to each other, then since we want just an approxi-
mate solution, we do not need to maintain both of them explicitly. More precisely,
we use a trimming parameter ı such that 0 < ı < 1. When we trim a list L by ı,
we remove as many elements from L as possible, in such a way that if L0 is the
result of trimming L, then for every element y that was removed from L, there is
an element ´ still in L0 that approximates y, that is,
y
1 C ı  ´  y :
(35.24)
We can think of such a ´ as “representing” y in the new list L0. Each removed
element y is represented by a remaining element ´ satisfying inequality (35.24).
For example, if ı D 0:1 and
L D h10; 11; 12; 15; 20; 21; 22; 23; 24; 29i ;
then we can trim L to obtain
L0 D h10; 12; 15; 20; 23; 29i ;
where the deleted value 11 is represented by 10, the deleted values 21 and 22
are represented by 20, and the deleted value 24 is represented by 23. Because
every element of the trimmed version of the list is also an element of the original
version of the list, trimming can dramatically decrease the number of elements kept
while keeping a close (and slightly smaller) representative value in the list for each
deleted element.
The following procedure trims list L D hy1; y2; : : : ; ymi in time ‚.m/, given L
and ı, and assuming that L is sorted into monotonically increasing order. The
output of the procedure is a trimmed, sorted list.
TRIM.L; ı/
1
let m be the length of L
2
L0 D hy1i
3
last D y1
4
for i D 2 to m
5
if yi > last  .1 C ı/
// yi  last because L is sorted
6
append yi onto the end of L0
7
last D yi
8
return L0
The procedure scans the elements of L in monotonically increasing order. A num-
ber is appended onto the returned list L0 only if it is the ﬁrst element of L or if it
cannot be represented by the most recent number placed into L0.
Given the procedure TRIM, we can construct our approximation scheme as fol-
lows. This procedure takes as input a set S D fx1; x2; : : : ; xng of n integers (in
arbitrary order), a target integer t, and an “approximation parameter” , where

35.5
The subset-sum problem
1131
0 <  < 1 :
(35.25)
It returns a value ´ whose value is within a 1 C  factor of the optimal solution.
APPROX-SUBSET-SUM.S; t; /
1
n D jSj
2
L0 D h0i
3
for i D 1 to n
4
Li D MERGE-LISTS.Li1; Li1 C xi/
5
Li D TRIM.Li; =2n/
6
remove from Li every element that is greater than t
7
let ´ be the largest value in Ln
8
return ´
Line 2 initializes the list L0 to be the list containing just the element 0. The for
loop in lines 3–6 computes Li as a sorted list containing a suitably trimmed ver-
sion of the set Pi, with all elements larger than t removed. Since we create Li
from Li1, we must ensure that the repeated trimming doesn’t introduce too much
compounded inaccuracy. In a moment, we shall see that APPROX-SUBSET-SUM
returns a correct approximation if one exists.
As an example, suppose we have the instance
S D h104; 102; 201; 101i
with t D 308 and  D 0:40. The trimming parameter ı is =8 D 0:05. APPROX-
SUBSET-SUM computes the following values on the indicated lines:
line 2:
L0
D
h0i ;
line 4:
L1
D
h0; 104i ;
line 5:
L1
D
h0; 104i ;
line 6:
L1
D
h0; 104i ;
line 4:
L2
D
h0; 102; 104; 206i ;
line 5:
L2
D
h0; 102; 206i ;
line 6:
L2
D
h0; 102; 206i ;
line 4:
L3
D
h0; 102; 201; 206; 303; 407i ;
line 5:
L3
D
h0; 102; 201; 303; 407i ;
line 6:
L3
D
h0; 102; 201; 303i ;
line 4:
L4
D
h0; 101; 102; 201; 203; 302; 303; 404i ;
line 5:
L4
D
h0; 101; 201; 302; 404i ;
line 6:
L4
D
h0; 101; 201; 302i :

1132
Chapter 35
Approximation Algorithms
The algorithm returns ´ D 302 as its answer, which is well within  D 40% of
the optimal answer 307 D 104 C 102 C 101; in fact, it is within 2%.
Theorem 35.8
APPROX-SUBSET-SUM is a fully polynomial-time approximation scheme for the
subset-sum problem.
Proof
The operations of trimming Li in line 5 and removing from Li every ele-
ment that is greater than t maintain the property that every element of Li is also a
member of Pi. Therefore, the value ´ returned in line 8 is indeed the sum of some
subset of S. Let y 2 Pn denote an optimal solution to the subset-sum problem.
Then, from line 6, we know that ´  y. By inequality (35.1), we need to show
that y=´  1 C . We must also show that the running time of this algorithm is
polynomial in both 1= and the size of the input.
As Exercise 35.5-2 asks you to show, for every element y in Pi that is at most t,
there exists an element ´ 2 Li such that
y
.1 C =2n/i  ´  y :
(35.26)
Inequality (35.26) must hold for y 2 Pn, and therefore there exists an element
´ 2 Ln such that
y
.1 C =2n/n  ´  y ;
and thus
y
´ 

1 C 
2n
n
:
(35.27)
Since there exists an element ´ 2 Ln fulﬁlling inequality (35.27), the inequality
must hold for ´, which is the largest value in Ln; that is,
y

1 C 
2n
n
:
(35.28)
Now, we show that y=´  1 C . We do so by showing that .1 C =2n/n 
1 C . By equation (3.14), we have limn!1.1 C =2n/n D e=2. Exercise 35.5-3
asks you to show that
d
dn

1 C 
2n
n
> 0 :
(35.29)
Therefore, the function .1 C =2n/n increases with n as it approaches its limit
of e=2, and we have

35.5
The subset-sum problem
1133

1 C 
2n
n

e=2

1 C =2 C .=2/2
(by inequality (3.13))

1 C 
(by inequality (35.25)) .
(35.30)
Combining inequalities (35.28) and (35.30) completes the analysis of the approxi-
mation ratio.
To show that APPROX-SUBSET-SUM is a fully polynomial-time approximation
scheme, we derive a bound on the length of Li. After trimming, successive ele-
ments ´ and ´0 of Li must have the relationship ´0=´ > 1C=2n. That is, they must
differ by a factor of at least 1 C =2n. Each list, therefore, contains the value 0,
possibly the value 1, and up to

log1C=2n t
˘
additional values. The number of
elements in each list Li is at most
log1C=2n t C 2
D
ln t
ln.1 C =2n/ C 2

2n.1 C =2n/ ln t

C 2
(by inequality (3.17))
<
3n ln t

C 2
(by inequality (35.25)) .
This bound is polynomial in the size of the input—which is the number of bits lg t
needed to represent t plus the number of bits needed to represent the set S, which is
in turn polynomial in n—and in 1=. Since the running time of APPROX-SUBSET-
SUM is polynomial in the lengths of the Li, we conclude that APPROX-SUBSET-
SUM is a fully polynomial-time approximation scheme.
Exercises
35.5-1
Prove equation (35.23). Then show that after executing line 5 of EXACT-SUBSET-
SUM, Li is a sorted list containing every element of Pi whose value is not more
than t.
35.5-2
Using induction on i, prove inequality (35.26).
35.5-3
Prove inequality (35.29).

1134
Chapter 35
Approximation Algorithms
35.5-4
How would you modify the approximation scheme presented in this section to ﬁnd
a good approximation to the smallest value not less than t that is a sum of some
subset of the given input list?
35.5-5
Modify the APPROX-SUBSET-SUM procedure to also return the subset of S that
sums to the value ´.
Problems
35-1
Bin packing
Suppose that we are given a set of n objects, where the size si of the ith object
satisﬁes 0 < si < 1. We wish to pack all the objects into the minimum number of
unit-size bins. Each bin can hold any subset of the objects whose total size does
not exceed 1.
a. Prove that the problem of determining the minimum number of bins required is
NP-hard. (Hint: Reduce from the subset-sum problem.)
The ﬁrst-ﬁt heuristic takes each object in turn and places it into the ﬁrst bin that
can accommodate it. Let S D Pn
iD1 si.
b. Argue that the optimal number of bins required is at least dSe.
c. Argue that the ﬁrst-ﬁt heuristic leaves at most one bin less than half full.
d. Prove that the number of bins used by the ﬁrst-ﬁt heuristic is never more
than d2Se.
e. Prove an approximation ratio of 2 for the ﬁrst-ﬁt heuristic.
f.
Give an efﬁcient implementation of the ﬁrst-ﬁt heuristic, and analyze its running
time.
35-2
Approximating the size of a maximum clique
Let G D .V; E/ be an undirected graph. For any k  1, deﬁne G.k/ to be the undi-
rected graph .V .k/; E.k//, where V .k/ is the set of all ordered k-tuples of vertices
from V and E.k/ is deﬁned so that .1; 2; : : : ; k/ is adjacent to .w1; w2; : : : ; wk/
if and only if for i D 1; 2; : : : ; k, either vertex i is adjacent to wi in G, or else
i D wi.

Problems for Chapter 35
1135
a. Prove that the size of the maximum clique in G.k/ is equal to the kth power of
the size of the maximum clique in G.
b. Argue that if there is an approximation algorithm that has a constant approxi-
mation ratio for ﬁnding a maximum-size clique, then there is a polynomial-time
approximation scheme for the problem.
35-3
Weighted set-covering problem
Suppose that we generalize the set-covering problem so that each set Si in the
family F has an associated weight wi and the weight of a cover C is P
Si 2C wi.
We wish to determine a minimum-weight cover. (Section 35.3 handles the case in
which wi D 1 for all i.)
Show how to generalize the greedy set-covering heuristic in a natural manner
to provide an approximate solution for any instance of the weighted set-covering
problem. Show that your heuristic has an approximation ratio of H.d/, where d is
the maximum size of any set Si.
35-4
Maximum matching
Recall that for an undirected graph G, a matching is a set of edges such that no
two edges in the set are incident on the same vertex. In Section 26.3, we saw how
to ﬁnd a maximum matching in a bipartite graph. In this problem, we will look at
matchings in undirected graphs in general (i.e., the graphs are not required to be
bipartite).
a. A maximal matching is a matching that is not a proper subset of any other
matching. Show that a maximal matching need not be a maximum matching by
exhibiting an undirected graph G and a maximal matching M in G that is not a
maximum matching. (Hint: You can ﬁnd such a graph with only four vertices.)
b. Consider an undirected graph G D .V; E/. Give an O.E/-time greedy algo-
rithm to ﬁnd a maximal matching in G.
In this problem, we shall concentrate on a polynomial-time approximation algo-
rithm for maximum matching. Whereas the fastest known algorithm for maximum
matching takes superlinear (but polynomial) time, the approximation algorithm
here will run in linear time. You will show that the linear-time greedy algorithm
for maximal matching in part (b) is a 2-approximation algorithm for maximum
matching.
c. Show that the size of a maximum matching in G is a lower bound on the size
of any vertex cover for G.

1136
Chapter 35
Approximation Algorithms
d. Consider a maximal matching M in G D .V; E/. Let
T D f 2 V W some edge in M is incident on g :
What can you say about the subgraph of G induced by the vertices of G that
are not in T ?
e. Conclude from part (d) that 2 jMj is the size of a vertex cover for G.
f.
Using parts (c) and (e), prove that the greedy algorithm in part (b) is a 2-approx-
imation algorithm for maximum matching.
35-5
Parallel machine scheduling
In the parallel-machine-scheduling problem, we are given n jobs, J1; J2; : : : ; Jn,
where each job Jk has an associated nonnegative processing time of pk. We are
also given m identical machines, M1; M2; : : : ; Mm. Any job can run on any ma-
chine. A schedule speciﬁes, for each job Jk, the machine on which it runs and
the time period during which it runs. Each job Jk must run on some machine Mi
for pk consecutive time units, and during that time period no other job may run
on Mi. Let Ck denote the completion time of job Jk, that is, the time at which
job Jk completes processing. Given a schedule, we deﬁne Cmax D max1jn Cj to
be the makespan of the schedule. The goal is to ﬁnd a schedule whose makespan
is minimum.
For example, suppose that we have two machines M1 and M2 and that we have
four jobs J1; J2; J3; J4, with p1 D 2, p2 D 12, p3 D 4, and p4 D 5. Then one
possible schedule runs, on machine M1, job J1 followed by job J2, and on ma-
chine M2, it runs job J4 followed by job J3. For this schedule, C1 D 2, C2 D 14,
C3 D 9, C4 D 5, and Cmax D 14. An optimal schedule runs J2 on machine M1, and
it runs jobs J1, J3, and J4 on machine M2. For this schedule, C1 D 2, C2 D 12,
C3 D 6, C4 D 11, and Cmax D 12.
Given a parallel-machine-scheduling problem, we let C 
max denote the makespan
of an optimal schedule.
a. Show that the optimal makespan is at least as large as the greatest processing
time, that is,
C 
max  max
1kn pk :
b. Show that the optimal makespan is at least as large as the average machine load,
that is,
C 
max  1
m
X
1kn
pk :

Problems for Chapter 35
1137
Suppose that we use the following greedy algorithm for parallel machine schedul-
ing: whenever a machine is idle, schedule any job that has not yet been scheduled.
c. Write pseudocode to implement this greedy algorithm. What is the running
time of your algorithm?
d. For the schedule returned by the greedy algorithm, show that
Cmax  1
m
X
1kn
pk C max
1kn pk :
Conclude that this algorithm is a polynomial-time 2-approximation algorithm.
35-6
Approximating a maximum spanning tree
Let G D .V; E/ be an undirected graph with distinct edge weights w.u; / on each
edge .u; / 2 E. For each vertex  2 V , let max./ D max.u;/2E fw.u; /g be
the maximum-weight edge incident on that vertex. Let SG D fmax./ W  2 V g
be the set of maximum-weight edges incident on each vertex, and let TG be the
maximum-weight spanning tree of G, that is, the spanning tree of maximum total
weight. For any subset of edges E0  E, deﬁne w.E0/ D P
.u;/2E0 w.u; /.
a. Give an example of a graph with at least 4 vertices for which SG D TG.
b. Give an example of a graph with at least 4 vertices for which SG ¤ TG.
c. Prove that SG  TG for any graph G.
d. Prove that w.TG/  w.SG/=2 for any graph G.
e. Give an O.V C E/-time algorithm to compute a 2-approximation to the maxi-
mum spanning tree.
35-7
An approximation algorithm for the 0-1 knapsack problem
Recall the knapsack problem from Section 16.2. There are n items, where the ith
item is worth i dollars and weighs wi pounds. We are also given a knapsack
that can hold at most W pounds. Here, we add the further assumptions that each
weight wi is at most W and that the items are indexed in monotonically decreasing
order of their values: 1  2      n.
In the 0-1 knapsack problem, we wish to ﬁnd a subset of the items whose total
weight is at most W and whose total value is maximum. The fractional knapsack
problem is like the 0-1 knapsack problem, except that we are allowed to take a
fraction of each item, rather than being restricted to taking either all or none of

1138
Chapter 35
Approximation Algorithms
each item. If we take a fraction xi of item i, where 0  xi  1, we contribute
xiwi to the weight of the knapsack and receive value xii. Our goal is to develop
a polynomial-time 2-approximation algorithm for the 0-1 knapsack problem.
In order to design a polynomial-time algorithm, we consider restricted instances
of the 0-1 knapsack problem. Given an instance I of the knapsack problem, we
form restricted instances Ij, for j D 1; 2; : : : ; n, by removing items 1; 2; : : : ; j 1
and requiring the solution to include item j (all of item j in both the fractional
and 0-1 knapsack problems). No items are removed in instance I1. For instance Ij,
let Pj denote an optimal solution to the 0-1 problem and Qj denote an optimal
solution to the fractional problem.
a. Argue that an optimal solution to instance I of the 0-1 knapsack problem is one
of fP1; P2; : : : ; Png.
b. Prove that we can ﬁnd an optimal solution Qj to the fractional problem for in-
stance Ij by including item j and then using the greedy algorithm in which
at each step, we take as much as possible of the unchosen item in the set
fj C 1; j C 2; : : : ; ng with maximum value per pound i=wi.
c. Prove that we can always construct an optimal solution Qj to the fractional
problem for instance Ij that includes at most one item fractionally. That is, for
all items except possibly one, we either include all of the item or none of the
item in the knapsack.
d. Given an optimal solution Qj to the fractional problem for instance Ij, form
solution Rj from Qj by deleting any fractional items from Qj. Let .S/ denote
the total value of items taken in a solution S. Prove that .Rj/  .Qj/=2 
.Pj/=2.
e. Give a polynomial-time algorithm that returns a maximum-value solution from
the set fR1; R2; : : : ; Rng, and prove that your algorithm is a polynomial-time
2-approximation algorithm for the 0-1 knapsack problem.
Chapter notes
Although methods that do not necessarily compute exact solutions have been
known for thousands of years (for example, methods to approximate the value
of ), the notion of an approximation algorithm is much more recent. Hochbaum
[172] credits Garey, Graham, and Ullman [128] and Johnson [190] with formal-
izing the concept of a polynomial-time approximation algorithm. The ﬁrst such
algorithm is often credited to Graham [149].

Notes for Chapter 35
1139
Since this early work, thousands of approximation algorithms have been de-
signed for a wide range of problems, and there is a wealth of literature on this
ﬁeld. Recent texts by Ausiello et al. [26], Hochbaum [172], and Vazirani [345]
deal exclusively with approximation algorithms, as do surveys by Shmoys [315]
and Klein and Young [207]. Several other texts, such as Garey and Johnson [129]
and Papadimitriou and Steiglitz [271], have signiﬁcant coverage of approximation
algorithms as well. Lawler, Lenstra, Rinnooy Kan, and Shmoys [225] provide an
extensive treatment of approximation algorithms for the traveling-salesman prob-
lem.
Papadimitriou and Steiglitz attribute the algorithm APPROX-VERTEX-COVER
to F. Gavril and M. Yannakakis. The vertex-cover problem has been studied exten-
sively (Hochbaum [172] lists 16 different approximation algorithms for this prob-
lem), but all the approximation ratios are at least 2  o.1/.
The algorithm APPROX-TSP-TOUR appears in a paper by Rosenkrantz, Stearns,
and Lewis [298]. Christoﬁdes improved on this algorithm and gave a 3=2-approx-
imation algorithm for the traveling-salesman problem with the triangle inequality.
Arora [22] and Mitchell [257] have shown that if the points are in the euclidean
plane, there is a polynomial-time approximation scheme. Theorem 35.3 is due to
Sahni and Gonzalez [301].
The analysis of the greedy heuristic for the set-covering problem is modeled
after the proof published by Chv´atal [68] of a more general result; the basic result
as presented here is due to Johnson [190] and Lov´asz [238].
The algorithm APPROX-SUBSET-SUM and its analysis are loosely modeled after
related approximation algorithms for the knapsack and subset-sum problems by
Ibarra and Kim [187].
Problem 35-7 is a combinatorial version of a more general result on approximat-
ing knapsack-type integer programs by Bienstock and McClosky [45].
The randomized algorithm for MAX-3-CNF satisﬁability is implicit in the work
of Johnson [190]. The weighted vertex-cover algorithm is by Hochbaum [171].
Section 35.4 only touches on the power of randomization and linear program-
ming in the design of approximation algorithms. A combination of these two ideas
yields a technique called “randomized rounding,” which formulates a problem as
an integer linear program, solves the linear-programming relaxation, and interprets
the variables in the solution as probabilities. These probabilities then help guide
the solution of the original problem. This technique was ﬁrst used by Raghavan
and Thompson [290], and it has had many subsequent uses. (See Motwani, Naor,
and Raghavan [261] for a survey.) Several other notable recent ideas in the ﬁeld
of approximation algorithms include the primal-dual method (see Goemans and
Williamson [135] for a survey), ﬁnding sparse cuts for use in divide-and-conquer
algorithms [229], and the use of semideﬁnite programming [134].

1140
Chapter 35
Approximation Algorithms
As mentioned in the chapter notes for Chapter 34, recent results in probabilisti-
cally checkable proofs have led to lower bounds on the approximability of many
problems, including several in this chapter. In addition to the references there,
the chapter by Arora and Lund [23] contains a good description of the relation-
ship between probabilistically checkable proofs and the hardness of approximating
various problems.
