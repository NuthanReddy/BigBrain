# 24 Single-Source Shortest Paths

Single-Source Shortest Paths
Professor Patrick wishes to ﬁnd the shortest possible route from Phoenix to Indianapolis. Given a road map of the United States on which the distance between
each pair of adjacent intersections is marked, how can she determine this shortest
route?
One possible way would be to enumerate all the routes from Phoenix to Indianapolis, add up the distances on each route, and select the shortest. It is easy to
see, however, that even disallowing routes that contain cycles, Professor Patrick
would have to examine an enormous number of possibilities, most of which are
simply not worth considering. For example, a route from Phoenix to Indianapolis
that passes through Seattle is obviously a poor choice, because Seattle is several
hundred miles out of the way.
In this chapter and in Chapter 25, we show how to solve such problems efﬁciently. In a shortest-paths problem, we are given a weighted, directed graph
G D .V; E/, with weight function w W E ! R mapping edges to real-valued
weights. The weight w.p/ of path p D h0; 1; : : : ; ki is the sum of the weights
of its constituent edges:
w.p/ D
k
X
iD1
w.i1; i/ :
We deﬁne the shortest-path weight ı.u; / from u to  by
ı.u; / D
(
minfw.p/ W u
p; g
if there is a path from u to  ;
otherwise :
A shortest path from vertex u to vertex  is then deﬁned as any path p with weight
w.p/ D ı.u; /.
In the Phoenix-to-Indianapolis example, we can model the road map as a graph:
vertices represent intersections, edges represent road segments between intersections, and edge weights represent road distances. Our goal is to ﬁnd a shortest path
from a given intersection in Phoenix to a given intersection in Indianapolis.

Edge weights can represent metrics other than distances, such as time, cost,
penalties, loss, or any other quantity that accumulates linearly along a path and
that we would want to minimize.
The breadth-ﬁrst-search algorithm from Section 22.2 is a shortest-paths algorithm that works on unweighted graphs, that is, graphs in which each edge has unit
weight. Because many of the concepts from breadth-ﬁrst search arise in the study
of shortest paths in weighted graphs, you might want to review Section 22.2 before
proceeding.
Variants
In this chapter, we shall focus on the single-source shortest-paths problem: given
a graph G D .V; E/, we want to ﬁnd a shortest path from a given source vertex
s 2 V to each vertex  2 V . The algorithm for the single-source problem can
solve many other problems, including the following variants.
Single-destination shortest-paths problem: Find a shortest path to a given destination vertex t from each vertex . By reversing the direction of each edge in
the graph, we can reduce this problem to a single-source problem.
Single-pair shortest-path problem: Find a shortest path from u to  for given
vertices u and . If we solve the single-source problem with source vertex u,
we solve this problem also. Moreover, all known algorithms for this problem
have the same worst-case asymptotic running time as the best single-source
algorithms.
All-pairs shortest-paths problem: Find a shortest path from u to  for every pair
of vertices u and . Although we can solve this problem by running a singlesource algorithm once from each vertex, we usually can solve it faster. Additionally, its structure is interesting in its own right. Chapter 25 addresses the
all-pairs problem in detail.
Optimal substructure of a shortest path
Shortest-paths algorithms typically rely on the property that a shortest path between two vertices contains other shortest paths within it. (The Edmonds-Karp
maximum-ﬂow algorithm in Chapter 26 also relies on this property.)
Recall
that optimal substructure is one of the key indicators that dynamic programming
(Chapter 15) and the greedy method (Chapter 16) might apply. Dijkstra’s algorithm, which we shall see in Section 24.3, is a greedy algorithm, and the FloydWarshall algorithm, which ﬁnds shortest paths between all pairs of vertices (see
Section 25.2), is a dynamic-programming algorithm. The following lemma states
the optimal-substructure property of shortest paths more precisely.

> **Lemma 24.1 (Subpaths of shortest paths are shortest paths)**

Given a weighted, directed graph G D .V; E/ with weight function w W E ! R,
let p D h0; 1; : : : ; ki be a shortest path from vertex 0 to vertex k and, for any
i and j such that 0  i  j  k, let pij D hi; iC1; : : : ; ji be the subpath of p
from vertex i to vertex j. Then, pij is a shortest path from i to j.
Proof
If we decompose path p into 0
p0i
; i
pij
; j
pjk
; k, then we have that
w.p/ D w.p0i/ C w.pij/ C w.pjk/. Now, assume that there is a path p0
ij from i
to j with weight w.p0
ij/ < w.pij/. Then, 0
p0i
; i
p0
ij
; j
pjk
; k is a path from 0
to k whose weight w.p0i/Cw.p0
ij /Cw.pjk/ is less than w.p/, which contradicts
the assumption that p is a shortest path from 0 to k.
Negative-weight edges
Some instances of the single-source shortest-paths problem may include edges
whose weights are negative.
If the graph G D .V; E/ contains no negativeweight cycles reachable from the source s, then for all  2 V , the shortest-path
weight ı.s; / remains well deﬁned, even if it has a negative value. If the graph
contains a negative-weight cycle reachable from s, however, shortest-path weights
are not well deﬁned. No path from s to a vertex on the cycle can be a shortest path—we can always ﬁnd a path with lower weight by following the proposed
“shortest” path and then traversing the negative-weight cycle. If there is a negativeweight cycle on some path from s to , we deﬁne ı.s; / D 1.
Figure 24.1 illustrates the effect of negative weights and negative-weight cycles on shortest-path weights. Because there is only one path from s to a (the
path hs; ai), we have ı.s; a/ D w.s; a/ D 3. Similarly, there is only one path
from s to b, and so ı.s; b/ D w.s; a/ C w.a; b/ D 3 C .4/ D 1. There are
inﬁnitely many paths from s to c: hs; ci, hs; c; d; ci, hs; c; d; c; d; ci, and so on.
Because the cycle hc; d; ci has weight 6 C .3/ D 3 > 0, the shortest path from s
to c is hs;ci, with weight ı.s; c/ D w.s; c/ D 5. Similarly, the shortest path from s
to d is hs;c;di, with weight ı.s; d/ D w.s; c/Cw.c; d/ D 11. Analogously, there
are inﬁnitely many paths from s to e: hs; ei, hs; e; f; ei, hs; e; f; e; f; ei, and so
on. Because the cycle he; f; ei has weight 3 C .6/ D 3 < 0, however, there
is no shortest path from s to e. By traversing the negative-weight cycle he; f; ei
arbitrarily many times, we can ﬁnd paths from s to e with arbitrarily large negative
weights, and so ı.s; e/ D 1. Similarly, ı.s; f / D 1. Because g is reachable
from f , we can also ﬁnd paths with arbitrarily large negative weights from s to g,
and so ı.s; g/ D 1. Vertices h, i, and j also form a negative-weight cycle. They
are not reachable from s, however, and so ı.s; h/ D ı.s; i/ D ı.s; j / D 1.

c
d
–3
–∞
e
–∞
f
–6
a
–1
b
s
–∞
g
–4
∞
h
∞
i
∞
j
–8
Figure 24.1
Negative edge weights in a directed graph. The shortest-path weight from source s
appears within each vertex. Because vertices e and f form a negative-weight cycle reachable from s,
they have shortest-path weights of 1. Because vertex g is reachable from a vertex whose shortestpath weight is 1, it, too, has a shortest-path weight of 1. Vertices such as h, i, and j are not
reachable from s, and so their shortest-path weights are 1, even though they lie on a negative-weight
cycle.
Some shortest-paths algorithms, such as Dijkstra’s algorithm, assume that all
edge weights in the input graph are nonnegative, as in the road-map example. Others, such as the Bellman-Ford algorithm, allow negative-weight edges in the input graph and produce a correct answer as long as no negative-weight cycles are
reachable from the source. Typically, if there is such a negative-weight cycle, the
algorithm can detect and report its existence.
Cycles
Can a shortest path contain a cycle? As we have just seen, it cannot contain a
negative-weight cycle. Nor can it contain a positive-weight cycle, since removing the cycle from the path produces a path with the same source and destination
vertices and a lower path weight. That is, if p D h0; 1; : : : ; ki is a path and
c D hi; iC1; : : : ; ji is a positive-weight cycle on this path (so that i D j and
w.c/ > 0), then the path p0 D h0; 1; : : : ; i; jC1; jC2; : : : ; ki has weight
w.p0/ D w.p/  w.c/ < w.p/, and so p cannot be a shortest path from 0 to k.
That leaves only 0-weight cycles. We can remove a 0-weight cycle from any
path to produce another path whose weight is the same. Thus, if there is a shortest
path from a source vertex s to a destination vertex  that contains a 0-weight cycle,
then there is another shortest path from s to  without this cycle. As long as a
shortest path has 0-weight cycles, we can repeatedly remove these cycles from the
path until we have a shortest path that is cycle-free. Therefore, without loss of
generality we can assume that when we are ﬁnding shortest paths, they have no
cycles, i.e., they are simple paths. Since any acyclic path in a graph G D .V; E/

contains at most jV j distinct vertices, it also contains at most jV j  1 edges. Thus,
we can restrict our attention to shortest paths of at most jV j  1 edges.
Representing shortest paths
We often wish to compute not only shortest-path weights, but the vertices on shortest paths as well. We represent shortest paths similarly to how we represented
breadth-ﬁrst trees in Section 22.2. Given a graph G D .V; E/, we maintain for
each vertex  2 V a predecessor : that is either another vertex or NIL. The
shortest-paths algorithms in this chapter set the  attributes so that the chain of predecessors originating at a vertex  runs backwards along a shortest path from s to .
Thus, given a vertex  for which : ¤ NIL, the procedure PRINT-PATH.G; s; /
from Section 22.2 will print a shortest path from s to .
In the midst of executing a shortest-paths algorithm, however, the  values might
not indicate shortest paths. As in breadth-ﬁrst search, we shall be interested in the
predecessor subgraph G D .V; E/ induced by the  values. Here again, we
deﬁne the vertex set V to be the set of vertices of G with non-NIL predecessors,
plus the source s:
V D f 2 V W : ¤ NILg [ fsg :
The directed edge set E is the set of edges induced by the  values for vertices
in V:
E D f.:; / 2 E W  2 V  fsgg :
We shall prove that the  values produced by the algorithms in this chapter have
the property that at termination G is a “shortest-paths tree”—informally, a rooted
tree containing a shortest path from the source s to every vertex that is reachable
from s. A shortest-paths tree is like the breadth-ﬁrst tree from Section 22.2, but it
contains shortest paths from the source deﬁned in terms of edge weights instead of
numbers of edges. To be precise, let G D .V; E/ be a weighted, directed graph
with weight function w W E ! R, and assume that G contains no negative-weight
cycles reachable from the source vertex s 2 V , so that shortest paths are well
deﬁned. A shortest-paths tree rooted at s is a directed subgraph G0 D .V 0; E0/,
where V 0  V and E0  E, such that
1. V 0 is the set of vertices reachable from s in G,
2. G0 forms a rooted tree with root s, and
3. for all  2 V 0, the unique simple path from s to  in G0 is a shortest path from s
to  in G.

(a)
(b)
(c)
s
t
x
y
z
s
t
x
y
z
s
t
x
y
z
Figure 24.2
(a) A weighted, directed graph with shortest-path weights from source s. (b) The
shaded edges form a shortest-paths tree rooted at the source s. (c) Another shortest-paths tree with
the same root.
Shortest paths are not necessarily unique, and neither are shortest-paths trees. For
example, Figure 24.2 shows a weighted, directed graph and two shortest-paths trees
with the same root.
Relaxation
The algorithms in this chapter use the technique of relaxation. For each vertex
 2 V , we maintain an attribute :d, which is an upper bound on the weight of
a shortest path from source s to . We call :d a shortest-path estimate. We
initialize the shortest-path estimates and predecessors by the following ‚.V /-time
procedure:
INITIALIZE-SINGLE-SOURCE.G; s/
for each vertex  2 G:V
:d D 1
: D NIL
s:d D 0
After initialization, we have : D NIL for all  2 V , s:d D 0, and :d D 1 for
 2 V  fsg.
The process of relaxing an edge .u; / consists of testing whether we can improve the shortest path to  found so far by going through u and, if so, updating :d and :. A relaxation step1 may decrease the value of the shortest-path
The use of the term is historical. The outcome of a relaxation step can be viewed as a relaxation
of the constraint :d  u:d C w.u;/, which, by the triangle inequality (Lemma 24.10), must be
satisﬁed if u:d D ı.s; u/ and :d D ı.s; /. That is, if :d  u:d C w.u; /, there is no “pressure”
It may seem strange that the term “relaxation” is used for an operation that tightens an upper bound.
so the constraint is “relaxed.”
to satisfy this constraint,

u
v
u
v

```
RELAX(u,v,w)
(a)
(b)
u
v
u
v

```
RELAX(u,v,w)
Figure 24.3
```

Relaxing an edge .u; / with weight w.u; / D 2. The shortest-path estimate of each
vertex appears within the vertex. (a) Because :d > u:d C w.u;/ prior to relaxation, the value
of :d decreases. (b) Here, :d  u:d C w.u;/ before relaxing the edge, and so the relaxation step
leaves :d unchanged.
estimate :d and update ’s predecessor attribute :. The following code performs a relaxation step on edge .u; / in O.1/ time:
RELAX.u; ; w/
if :d > u:d C w.u; /
:d D u:d C w.u; /
: D u
Figure 24.3 shows two examples of relaxing an edge, one in which a shortest-path
estimate decreases and one in which no estimate changes.
Each algorithm in this chapter calls INITIALIZE-SINGLE-SOURCE and then repeatedly relaxes edges. Moreover, relaxation is the only means by which shortestpath estimates and predecessors change. The algorithms in this chapter differ in
how many times they relax each edge and the order in which they relax edges. Dijkstra’s algorithm and the shortest-paths algorithm for directed acyclic graphs relax
each edge exactly once. The Bellman-Ford algorithm relaxes each edge jV j  1
times.
Properties of shortest paths and relaxation
To prove the algorithms in this chapter correct, we shall appeal to several properties of shortest paths and relaxation. We state these properties here, and Section 24.5 proves them formally. For your reference, each property stated here includes the appropriate lemma or corollary number from Section 24.5. The latter
ﬁve of these properties, which refer to shortest-path estimates or the predecessor
subgraph, implicitly assume that the graph is initialized with a call to INITIALIZESINGLE-SOURCE.G; s/ and that the only way that shortest-path estimates and the
predecessor subgraph change are by some sequence of relaxation steps.

Triangle inequality (Lemma 24.10)
For any edge .u; / 2 E, we have ı.s; /  ı.s; u/ C w.u; /.
Upper-bound property (Lemma 24.11)
We always have :d  ı.s; / for all vertices  2 V , and once :d achieves the
value ı.s; /, it never changes.
No-path property (Corollary 24.12)
If there is no path from s to , then we always have :d D ı.s; / D 1.
Convergence property (Lemma 24.14)
If s ; u !  is a shortest path in G for some u;  2 V , and if u:d D ı.s; u/ at
any time prior to relaxing edge .u; /, then :d D ı.s; / at all times afterward.
Path-relaxation property (Lemma 24.15)
If p D h0; 1; : : : ; ki is a shortest path from s D 0 to k, and we relax the
edges of p in the order .0; 1/; .1; 2/; : : : ; .k1; k/, then k:d D ı.s; k/.
This property holds regardless of any other relaxation steps that occur, even if
they are intermixed with relaxations of the edges of p.
Predecessor-subgraph property (Lemma 24.17)
Once :d D ı.s; / for all  2 V , the predecessor subgraph is a shortest-paths
tree rooted at s.
Chapter outline
Section 24.1 presents the Bellman-Ford algorithm, which solves the single-source
shortest-paths problem in the general case in which edges can have negative weight.
The Bellman-Ford algorithm is remarkably simple, and it has the further beneﬁt
of detecting whether a negative-weight cycle is reachable from the source. Section 24.2 gives a linear-time algorithm for computing shortest paths from a single
source in a directed acyclic graph. Section 24.3 covers Dijkstra’s algorithm, which
has a lower running time than the Bellman-Ford algorithm but requires the edge
weights to be nonnegative. Section 24.4 shows how we can use the Bellman-Ford
algorithm to solve a special case of linear programming. Finally, Section 24.5
proves the properties of shortest paths and relaxation stated above.
We require some conventions for doing arithmetic with inﬁnities. We shall assume that for any real number a ¤ 1, we have a C 1 D 1 C a D 1. Also, to
make our proofs hold in the presence of negative-weight cycles, we shall assume
that for any real number a ¤ 1, we have a C .1/ D .1/ C a D 1.
All algorithms in this chapter assume that the directed graph G is stored in the
adjacency-list representation. Additionally, stored with each edge is its weight, so
that as we traverse each adjacency list, we can determine the edge weights in O.1/
time per edge.

## 24.1 The Bellman-Ford algorithm

## 24.1 The Bellman-Ford algorithm

The Bellman-Ford algorithm solves the single-source shortest-paths problem in
the general case in which edge weights may be negative. Given a weighted, directed graph G D .V; E/ with source s and weight function w W E ! R, the
Bellman-Ford algorithm returns a boolean value indicating whether or not there is
a negative-weight cycle that is reachable from the source. If there is such a cycle, the algorithm indicates that no solution exists. If there is no such cycle, the
algorithm produces the shortest paths and their weights.
The algorithm relaxes edges, progressively decreasing an estimate :d on the
weight of a shortest path from the source s to each vertex  2 V until it achieves
the actual shortest-path weight ı.s; /. The algorithm returns TRUE if and only if
the graph contains no negative-weight cycles that are reachable from the source.
BELLMAN-FORD.G; w; s/
INITIALIZE-SINGLE-SOURCE.G; s/
for i D 1 to jG:Vj  1
for each edge .u; / 2 G:E
RELAX.u; ; w/
for each edge .u; / 2 G:E
if :d > u:d C w.u; /
return FALSE
return TRUE
Figure 24.4 shows the execution of the Bellman-Ford algorithm on a graph
with 5 vertices. After initializing the d and  values of all vertices in line 1,
the algorithm makes jV j  1 passes over the edges of the graph. Each pass is
one iteration of the for loop of lines 2–4 and consists of relaxing each edge of the
graph once. Figures 24.4(b)–(e) show the state of the algorithm after each of the
four passes over the edges. After making jV j  1 passes, lines 5–8 check for a
negative-weight cycle and return the appropriate boolean value. (We’ll see a little
later why this check works.)
The Bellman-Ford algorithm runs in time O.VE/, since the initialization in
line 1 takes ‚.V / time, each of the jV j  1 passes over the edges in lines 2–4
takes ‚.E/ time, and the for loop of lines 5–7 takes O.E/ time.
To prove the correctness of the Bellman-Ford algorithm, we start by showing that
if there are no negative-weight cycles, the algorithm computes correct shortest-path
weights for all vertices reachable from the source.

(a)
(b)
(c)
(d)
(e)
t
x
s
y
z
–4
–3
–2
–2
t
x
s
y
z
–4
–3
–2
t
x
s
y
z
–4
–3
–2
t
x
s
y
z
–4
–3
–2
∞
∞
t
x
s
y
z
–4
–3
–2
∞
∞
∞
∞
Figure 24.4
The execution of the Bellman-Ford algorithm. The source is vertex s. The d values appear within the vertices, and shaded edges indicate predecessor values: if edge .u; / is
shaded, then : D u.
In this particular example, each pass relaxes the edges in the order
.t; x/;.t; y/; .t; ´/; .x; t/; .y; x/; .y; ´/; .´; x/; .´; s/; .s; t/; .s; y/. (a) The situation just before the
ﬁrst pass over the edges. (b)–(e) The situation after each successive pass over the edges. The d
and  values in part (e) are the ﬁnal values. The Bellman-Ford algorithm returns TRUE in this
example.

> **Lemma 24.2**

Let G D .V; E/ be a weighted, directed graph with source s and weight function w W E ! R, and assume that G contains no negative-weight cycles that are
reachable from s. Then, after the jV j  1 iterations of the for loop of lines 2–4
of BELLMAN-FORD, we have :d D ı.s; / for all vertices  that are reachable
from s.
Proof
We prove the lemma by appealing to the path-relaxation property. Consider any vertex  that is reachable from s, and let p D h0; 1; : : : ; ki, where
0 D s and k D , be any shortest path from s to . Because shortest paths are
simple, p has at most jV j  1 edges, and so k  jV j  1. Each of the jV j  1 iterations of the for loop of lines 2–4 relaxes all jEj edges. Among the edges relaxed in
the ith iteration, for i D 1; 2; : : : ; k, is .i1; i/. By the path-relaxation property,
therefore, :d D k:d D ı.s; k/ D ı.s; /.

## 24.1 The Bellman-Ford algorithm

> **Corollary 24.3**

Let G D .V; E/ be a weighted, directed graph with source vertex s and weight
function w W E ! R, and assume that G contains no negative-weight cycles that
are reachable from s. Then, for each vertex  2 V , there is a path from s to  if
and only if BELLMAN-FORD terminates with :d < 1 when it is run on G.
Proof
The proof is left as Exercise 24.1-2.

> **Theorem 24.4 (Correctness of the Bellman-Ford algorithm)**

Let BELLMAN-FORD be run on a weighted, directed graph G D .V; E/ with
source s and weight function w W E ! R. If G contains no negative-weight cycles
that are reachable from s, then the algorithm returns TRUE, we have :d D ı.s; /
for all vertices  2 V , and the predecessor subgraph G is a shortest-paths tree
rooted at s. If G does contain a negative-weight cycle reachable from s, then the
algorithm returns FALSE.
Proof
Suppose that graph G contains no negative-weight cycles that are reachable from the source s. We ﬁrst prove the claim that at termination, :d D ı.s; /
for all vertices  2 V . If vertex  is reachable from s, then Lemma 24.2 proves this
claim. If  is not reachable from s, then the claim follows from the no-path property. Thus, the claim is proven. The predecessor-subgraph property, along with the
claim, implies that G is a shortest-paths tree. Now we use the claim to show that
BELLMAN-FORD returns TRUE. At termination, we have for all edges .u; / 2 E,
:d
D
ı.s; /

ı.s; u/ C w.u; /
(by the triangle inequality)
D
u:d C w.u; / ;
and so none of the tests in line 6 causes BELLMAN-FORD to return FALSE. Therefore, it returns TRUE.
Now, suppose that graph G contains a negative-weight cycle that is reachable
from the source s; let this cycle be c D h0; 1; : : : ; ki, where 0 D k. Then,
k
X
iD1
w.i1; i/ < 0 :
(24.1)
Assume for the purpose of contradiction that the Bellman-Ford algorithm returns
TRUE. Thus, i:d  i1:d C w.i1; i/ for i D 1; 2; : : : ; k. Summing the
inequalities around cycle c gives us

k
X
iD1
i:d

k
X
iD1
.i1:d C w.i1; i//
D
k
X
iD1
i1:d C
k
X
iD1
w.i1; i/ :
Since 0 D k, each vertex in c appears exactly once in each of the summations
Pk
iD1 i:d and Pk
iD1 i1:d, and so
k
X
iD1
i:d D
k
X
iD1
i1:d :
Moreover, by Corollary 24.3, i:d is ﬁnite for i D 1; 2; : : : ; k. Thus,
0 
k
X
iD1
w.i1; i/ ;
which contradicts inequality (24.1). We conclude that the Bellman-Ford algorithm
returns TRUE if graph G contains no negative-weight cycles reachable from the
source, and FALSE otherwise.

## Exercises

24.1-1
Run the Bellman-Ford algorithm on the directed graph of Figure 24.4, using vertex ´ as the source. In each pass, relax edges in the same order as in the ﬁgure, and
show the d and  values after each pass. Now, change the weight of edge .´; x/
to 4 and run the algorithm again, using s as the source.
24.1-2
Prove Corollary 24.3.
24.1-3
Given a weighted, directed graph G D .V; E/ with no negative-weight cycles,
let m be the maximum over all vertices  2 V of the minimum number of edges
in a shortest path from the source s to . (Here, the shortest path is by weight, not
the number of edges.) Suggest a simple change to the Bellman-Ford algorithm that
allows it to terminate in m C 1 passes, even if m is not known in advance.
24.1-4
Modify the Bellman-Ford algorithm so that it sets :d to 1 for all vertices  for
which there is a negative-weight cycle on some path from the source to .

## 24.2 Single-source shortest paths in directed acyclic graphs

24.1-5
?
Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R.
Give an O.VE/-time algorithm to ﬁnd, for each vertex  2 V , the value ı./ D
minu2V fı.u; /g.
24.1-6
?
Suppose that a weighted, directed graph G D .V; E/ has a negative-weight cycle.
Give an efﬁcient algorithm to list the vertices of one such cycle. Prove that your
algorithm is correct.

## 24.2 Single-source shortest paths in directed acyclic graphs

By relaxing the edges of a weighted dag (directed acyclic graph) G D .V; E/
according to a topological sort of its vertices, we can compute shortest paths from
a single source in ‚.V C E/ time. Shortest paths are always well deﬁned in a dag,
since even if there are negative-weight edges, no negative-weight cycles can exist.
The algorithm starts by topologically sorting the dag (see Section 22.4) to impose a linear ordering on the vertices. If the dag contains a path from vertex u to
vertex , then u precedes  in the topological sort. We make just one pass over the
vertices in the topologically sorted order. As we process each vertex, we relax each
edge that leaves the vertex.
DAG-SHORTEST-PATHS.G; w; s/
topologically sort the vertices of G
INITIALIZE-SINGLE-SOURCE.G; s/
for each vertex u, taken in topologically sorted order
for each vertex  2 G:AdjŒu
RELAX.u; ; w/
Figure 24.5 shows the execution of this algorithm.
The running time of this algorithm is easy to analyze. As shown in Section 22.4,
the topological sort of line 1 takes ‚.V C E/ time. The call of INITIALIZESINGLE-SOURCE in line 2 takes ‚.V / time. The for loop of lines 3–5 makes one
iteration per vertex. Altogether, the for loop of lines 4–5 relaxes each edge exactly
once. (We have used an aggregate analysis here.) Because each iteration of the
inner for loop takes ‚.1/ time, the total running time is ‚.V CE/, which is linear
in the size of an adjacency-list representation of the graph.
The following theorem shows that the DAG-SHORTEST-PATHS procedure correctly computes the shortest paths.

∞
∞
∞
∞
∞
–1
–2
(a)
x
t
s
r
y
z
–1
–2
(c)
x
t
s
r
y
z
–1
–2
(e)
x
t
s
r
y
z
–1
–2
(g)
x
t
s
r
y
z
–1
–2
(b)
x
t
s
r
y
z
–1
–2
(d)
x
t
s
r
y
z
–1
–2
(f)
x
t
s
r
y
z
∞
∞
∞
∞
∞
∞
∞
∞
∞
∞
∞
∞
Figure 24.5
The execution of the algorithm for shortest paths in a directed acyclic graph. The
vertices are topologically sorted from left to right. The source vertex is s. The d values appear
within the vertices, and shaded edges indicate the  values. (a) The situation before the ﬁrst iteration
of the for loop of lines 3–5. (b)–(g) The situation after each iteration of the for loop of lines 3–5.
The newly blackened vertex in each iteration was used as u in that iteration. The values shown in
part (g) are the ﬁnal values.

> **Theorem 24.5**

If a weighted, directed graph G D .V; E/ has source vertex s and no cycles, then
at the termination of the DAG-SHORTEST-PATHS procedure, :d D ı.s; / for all
vertices  2 V , and the predecessor subgraph G is a shortest-paths tree.
Proof
We ﬁrst show that :d D ı.s; / for all vertices  2 V at termination.
If  is not reachable from s, then :d D ı.s; / D 1 by the no-path
property.
Now, suppose that  is reachable from s, so that there is a shortest path p D h0; 1; : : : ; ki, where 0 D s and k D . Because we pro24.2
Single-source shortest paths in directed acyclic graphs
cess the vertices in topologically sorted order, we relax the edges on p in the
order .0; 1/; .1; 2/; : : : ; .k1; k/. The path-relaxation property implies that
i:d D ı.s; i/ at termination for i D 0; 1; : : : ; k. Finally, by the predecessorsubgraph property, G is a shortest-paths tree.
An interesting application of this algorithm arises in determining critical paths
in PERT chart2 analysis. Edges represent jobs to be performed, and edge weights
represent the times required to perform particular jobs. If edge .u; / enters vertex  and edge .; x/ leaves , then job .u; / must be performed before job .; x/.
A path through this dag represents a sequence of jobs that must be performed in a
particular order. A critical path is a longest path through the dag, corresponding
to the longest time to perform any sequence of jobs. Thus, the weight of a critical
path provides a lower bound on the total time to perform all the jobs. We can ﬁnd
a critical path by either

negating the edge weights and running DAG-SHORTEST-PATHS, or

running DAG-SHORTEST-PATHS, with the modiﬁcation that we replace “1”
by “1” in line 2 of INITIALIZE-SINGLE-SOURCE and “>” by “<” in the
RELAX procedure.

## Exercises

24.2-1
Run DAG-SHORTEST-PATHS on the directed graph of Figure 24.5, using vertex r
as the source.
24.2-2
Suppose we change line 3 of DAG-SHORTEST-PATHS to read
for the ﬁrst jV j  1 vertices, taken in topologically sorted order
Show that the procedure would remain correct.
24.2-3
The PERT chart formulation given above is somewhat unnatural. In a more natural structure, vertices would represent jobs and edges would represent sequencing
constraints; that is, edge .u; / would indicate that job u must be performed before
job . We would then assign weights to vertices, not edges. Modify the DAGSHORTEST-PATHS procedure so that it ﬁnds a longest path in a directed acyclic
graph with weighted vertices in linear time.
2“PERT” is an acronym for “program evaluation and review technique.”

24.2-4
Give an efﬁcient algorithm to count the total number of paths in a directed acyclic
graph. Analyze your algorithm.

## 24.3 Dijkstra’s algorithm

Dijkstra’s algorithm solves the single-source shortest-paths problem on a weighted,
directed graph G D .V; E/ for the case in which all edge weights are nonnegative.
In this section, therefore, we assume that w.u; /  0 for each edge .u; / 2 E. As
we shall see, with a good implementation, the running time of Dijkstra’s algorithm
is lower than that of the Bellman-Ford algorithm.
Dijkstra’s algorithm maintains a set S of vertices whose ﬁnal shortest-path
weights from the source s have already been determined. The algorithm repeatedly selects the vertex u 2 V S with the minimum shortest-path estimate, adds u
to S, and relaxes all edges leaving u. In the following implementation, we use a
min-priority queue Q of vertices, keyed by their d values.
DIJKSTRA.G; w; s/
INITIALIZE-SINGLE-SOURCE.G; s/
S D ;
Q D G:V
while Q ¤ ;
u D EXTRACT-MIN.Q/
S D S [ fug
for each vertex  2 G:AdjŒu
RELAX.u; ; w/
Dijkstra’s algorithm relaxes edges as shown in Figure 24.6. Line 1 initializes
the d and  values in the usual way, and line 2 initializes the set S to the empty
set. The algorithm maintains the invariant that Q D V  S at the start of each
iteration of the while loop of lines 4–8. Line 3 initializes the min-priority queue Q
to contain all the vertices in V ; since S D ; at that time, the invariant is true after
line 3. Each time through the while loop of lines 4–8, line 5 extracts a vertex u from
Q D V S and line 6 adds it to set S, thereby maintaining the invariant. (The ﬁrst
time through this loop, u D s.) Vertex u, therefore, has the smallest shortest-path
estimate of any vertex in V  S. Then, lines 7–8 relax each edge .u; / leaving u,
thus updating the estimate :d and the predecessor : if we can improve the
shortest path to  found so far by going through u. Observe that the algorithm
never inserts vertices into Q after line 3 and that each vertex is extracted from Q

## 24.3 Dijkstra’s algorithm

∞
∞
∞
∞
∞
∞
(c)
s
t
x
y
z
(f)
s
t
x
y
z
(b)
s
t
x
y
z
(e)
s
t
x
y
z
(a)
s
t
x
y
z
(d)
s
t
x
y
z
Figure 24.6
The execution of Dijkstra’s algorithm.
The source s is the leftmost vertex. The
shortest-path estimates appear within the vertices, and shaded edges indicate predecessor values.
Black vertices are in the set S, and white vertices are in the min-priority queue Q D V  S. (a) The
situation just before the ﬁrst iteration of the while loop of lines 4–8. The shaded vertex has the minimum d value and is chosen as vertex u in line 5. (b)–(f) The situation after each successive iteration
of the while loop. The shaded vertex in each part is chosen as vertex u in line 5 of the next iteration.
The d values and predecessors shown in part (f) are the ﬁnal values.
and added to S exactly once, so that the while loop of lines 4–8 iterates exactly jV j
times.
Because Dijkstra’s algorithm always chooses the “lightest” or “closest” vertex
in V  S to add to set S, we say that it uses a greedy strategy. Chapter 16 explains
greedy strategies in detail, but you need not have read that chapter to understand
Dijkstra’s algorithm. Greedy strategies do not always yield optimal results in general, but as the following theorem and its corollary show, Dijkstra’s algorithm does
indeed compute shortest paths. The key is to show that each time it adds a vertex u
to set S, we have u:d D ı.s; u/.

> **Theorem 24.6 (Correctness of Dijkstra’s algorithm)**

Dijkstra’s algorithm, run on a weighted, directed graph G D .V; E/ with nonnegative weight function w and source s, terminates with u:d D ı.s; u/ for all
vertices u 2 V .

p1
S
p2
u
y
s
x
Figure 24.7
The proof of Theorem 24.6. Set S is nonempty just before vertex u is added to it. We
decompose a shortest path p from source s to vertex u into s
p1
; x ! y
p2
; u, where y is the ﬁrst
vertex on the path that is not in S and x 2 S immediately precedes y. Vertices x and y are distinct,
but we may have s D x or y D u. Path p2 may or may not reenter set S.
Proof
We use the following loop invariant:
At the start of each iteration of the while loop of lines 4–8, :d D ı.s; /
for each vertex  2 S.
It sufﬁces to show for each vertex u 2 V , we have u:d D ı.s; u/ at the time when u
is added to set S. Once we show that u:d D ı.s; u/, we rely on the upper-bound
property to show that the equality holds at all times thereafter.
Initialization: Initially, S D ;, and so the invariant is trivially true.
Maintenance: We wish to show that in each iteration, u:d D ı.s; u/ for the vertex
added to set S. For the purpose of contradiction, let u be the ﬁrst vertex for
which u:d ¤ ı.s; u/ when it is added to set S. We shall focus our attention
on the situation at the beginning of the iteration of the while loop in which u
is added to S and derive the contradiction that u:d D ı.s; u/ at that time by
examining a shortest path from s to u. We must have u ¤ s because s is the
ﬁrst vertex added to set S and s:d D ı.s; s/ D 0 at that time. Because u ¤ s,
we also have that S ¤ ; just before u is added to S. There must be some
path from s to u, for otherwise u:d D ı.s; u/ D 1 by the no-path property,
which would violate our assumption that u:d ¤ ı.s; u/. Because there is at
least one path, there is a shortest path p from s to u. Prior to adding u to S,
path p connects a vertex in S, namely s, to a vertex in V  S, namely u. Let us
consider the ﬁrst vertex y along p such that y 2 V  S, and let x 2 S be y’s
predecessor along p. Thus, as Figure 24.7 illustrates, we can decompose path p
into s
p1
; x ! y
p2
; u. (Either of paths p1 or p2 may have no edges.)
We claim that y:d D ı.s; y/ when u is added to S. To prove this claim, observe that x 2 S. Then, because we chose u as the ﬁrst vertex for which
u:d ¤ ı.s; u/ when it is added to S, we had x:d D ı.s; x/ when x was added

## 24.3 Dijkstra’s algorithm

to S. Edge .x; y/ was relaxed at that time, and the claim follows from the
convergence property.
We can now obtain a contradiction to prove that u:d D ı.s; u/. Because y
appears before u on a shortest path from s to u and all edge weights are nonnegative (notably those on path p2), we have ı.s; y/  ı.s; u/, and thus
y:d
D
ı.s; y/

ı.s; u/
(24.2)

u:d
(by the upper-bound property) .
But because both vertices u and y were in V  S when u was chosen in line 5,
we have u:d  y:d. Thus, the two inequalities in (24.2) are in fact equalities,
giving
y:d D ı.s; y/ D ı.s; u/ D u:d :
Consequently, u:d D ı.s; u/, which contradicts our choice of u. We conclude
that u:d D ı.s; u/ when u is added to S, and that this equality is maintained at
all times thereafter.
Termination: At termination, Q D ; which, along with our earlier invariant that
Q D V S, implies that S D V . Thus, u:d D ı.s; u/ for all vertices u 2 V .

> **Corollary 24.7**

If we run Dijkstra’s algorithm on a weighted, directed graph G D .V; E/ with
nonnegative weight function w and source s, then at termination, the predecessor
subgraph G is a shortest-paths tree rooted at s.
Proof
Immediate from Theorem 24.6 and the predecessor-subgraph property.
Analysis
How fast is Dijkstra’s algorithm? It maintains the min-priority queue Q by calling three priority-queue operations: INSERT (implicit in line 3), EXTRACT-MIN
(line 5), and DECREASE-KEY (implicit in RELAX, which is called in line 8). The
algorithm calls both INSERT and EXTRACT-MIN once per vertex. Because each
vertex u 2 V is added to set S exactly once, each edge in the adjacency list AdjŒu
is examined in the for loop of lines 7–8 exactly once during the course of the algorithm. Since the total number of edges in all the adjacency lists is jEj, this for
loop iterates a total of jEj times, and thus the algorithm calls DECREASE-KEY at
most jEj times overall. (Observe once again that we are using aggregate analysis.)
The running time of Dijkstra’s algorithm depends on how we implement the
min-priority queue. Consider ﬁrst the case in which we maintain the min-priority

queue by taking advantage of the vertices being numbered 1 to jV j. We simply
store :d in the th entry of an array. Each INSERT and DECREASE-KEY operation
takes O.1/ time, and each EXTRACT-MIN operation takes O.V / time (since we
have to search through the entire array), for a total time of O.V 2 C E/ D O.V 2/.
If the graph is sufﬁciently sparse—in particular, E D o.V 2= lg V /—we can
improve the algorithm by implementing the min-priority queue with a binary minheap. (As discussed in Section 6.5, the implementation should make sure that
vertices and corresponding heap elements maintain handles to each other.) Each
EXTRACT-MIN operation then takes time O.lg V /. As before, there are jV j such
operations. The time to build the binary min-heap is O.V /. Each DECREASE-KEY
operation takes time O.lg V /, and there are still at most jEj such operations. The
total running time is therefore O..V C E/ lg V /, which is O.E lg V / if all vertices
are reachable from the source. This running time improves upon the straightforward O.V 2/-time implementation if E D o.V 2= lg V /.
We can in fact achieve a running time of O.V lg V C E/ by implementing the
min-priority queue with a Fibonacci heap (see Chapter 19). The amortized cost
of each of the jV j EXTRACT-MIN operations is O.lg V /, and each DECREASEKEY call, of which there are at most jEj, takes only O.1/ amortized time. Historically, the development of Fibonacci heaps was motivated by the observation
that Dijkstra’s algorithm typically makes many more DECREASE-KEY calls than
EXTRACT-MIN calls, so that any method of reducing the amortized time of each
DECREASE-KEY operation to o.lg V / without increasing the amortized time of
EXTRACT-MIN would yield an asymptotically faster implementation than with binary heaps.
Dijkstra’s algorithm resembles both breadth-ﬁrst search (see Section 22.2) and
Prim’s algorithm for computing minimum spanning trees (see Section 23.2). It is
like breadth-ﬁrst search in that set S corresponds to the set of black vertices in a
breadth-ﬁrst search; just as vertices in S have their ﬁnal shortest-path weights, so
do black vertices in a breadth-ﬁrst search have their correct breadth-ﬁrst distances.
Dijkstra’s algorithm is like Prim’s algorithm in that both algorithms use a minpriority queue to ﬁnd the “lightest” vertex outside a given set (the set S in Dijkstra’s
algorithm and the tree being grown in Prim’s algorithm), add this vertex into the
set, and adjust the weights of the remaining vertices outside the set accordingly.

## Exercises

24.3-1
Run Dijkstra’s algorithm on the directed graph of Figure 24.2, ﬁrst using vertex s
as the source and then using vertex ´ as the source. In the style of Figure 24.6,
show the d and  values and the vertices in set S after each iteration of the while
loop.

## 24.3 Dijkstra’s algorithm

24.3-2
Give a simple example of a directed graph with negative-weight edges for which
Dijkstra’s algorithm produces incorrect answers. Why doesn’t the proof of Theorem 24.6 go through when negative-weight edges are allowed?
24.3-3
Suppose we change line 4 of Dijkstra’s algorithm to the following.
while jQj > 1
This change causes the while loop to execute jV j  1 times instead of jV j times. Is
this proposed algorithm correct?
24.3-4
Professor Gaedel has written a program that he claims implements Dijkstra’s algorithm. The program produces :d and : for each vertex  2 V . Give an
O.V CE/-time algorithm to check the output of the professor’s program. It should
determine whether the d and  attributes match those of some shortest-paths tree.
You may assume that all edge weights are nonnegative.
24.3-5
Professor Newman thinks that he has worked out a simpler proof of correctness
for Dijkstra’s algorithm. He claims that Dijkstra’s algorithm relaxes the edges of
every shortest path in the graph in the order in which they appear on the path, and
therefore the path-relaxation property applies to every vertex reachable from the
source. Show that the professor is mistaken by constructing a directed graph for
which Dijkstra’s algorithm could relax the edges of a shortest path out of order.
24.3-6
We are given a directed graph G D .V; E/ on which each edge .u; / 2 E has an
associated value r.u; /, which is a real number in the range 0  r.u; /  1 that
represents the reliability of a communication channel from vertex u to vertex .
We interpret r.u; / as the probability that the channel from u to  will not fail,
and we assume that these probabilities are independent. Give an efﬁcient algorithm
to ﬁnd the most reliable path between two given vertices.
24.3-7
Let G D .V; E/ be a weighted, directed graph with positive weight function
w W E ! f1; 2; : : : ; W g for some positive integer W , and assume that no two vertices have the same shortest-path weights from source vertex s. Now suppose that
we deﬁne an unweighted, directed graph G0 D .V [ V 0; E0/ by replacing each
edge .u; / 2 E with w.u; / unit-weight edges in series. How many vertices
does G0 have? Now suppose that we run a breadth-ﬁrst search on G0. Show that

the order in which the breadth-ﬁrst search of G0 colors vertices in V black is the
same as the order in which Dijkstra’s algorithm extracts the vertices of V from the
priority queue when it runs on G.
24.3-8
Let G D .V; E/ be a weighted, directed graph with nonnegative weight function
w W E ! f0; 1; : : : ; W g for some nonnegative integer W . Modify Dijkstra’s algorithm to compute the shortest paths from a given source vertex s in O.W V C E/
time.
24.3-9
Modify your algorithm from Exercise 24.3-8 to run in O..V C E/ lg W / time.
(Hint: How many distinct shortest-path estimates can there be in V  S at any
point in time?)
24.3-10
Suppose that we are given a weighted, directed graph G D .V; E/ in which edges
that leave the source vertex s may have negative weights, all other edge weights
are nonnegative, and there are no negative-weight cycles. Argue that Dijkstra’s
algorithm correctly ﬁnds shortest paths from s in this graph.

## 24.4 Difference constraints and shortest paths

Chapter 29 studies the general linear-programming problem, in which we wish to
optimize a linear function subject to a set of linear inequalities. In this section, we
investigate a special case of linear programming that we reduce to ﬁnding shortest
paths from a single source. We can then solve the single-source shortest-paths
problem that results by running the Bellman-Ford algorithm, thereby also solving
the linear-programming problem.
Linear programming
In the general linear-programming problem, we are given an m 	 n matrix A,
an m-vector b, and an n-vector c. We wish to ﬁnd a vector x of n elements that
maximizes the objective function Pn
iD1 cixi subject to the m constraints given by
Ax  b.
Although the simplex algorithm, which is the focus of Chapter 29, does not
always run in time polynomial in the size of its input, there are other linearprogramming algorithms that do run in polynomial time. We offer here two reasons
to understand the setup of linear-programming problems. First, if we know that we

## 24.4 Difference constraints and shortest paths

can cast a given problem as a polynomial-sized linear-programming problem, then
we immediately have a polynomial-time algorithm to solve the problem. Second,
faster algorithms exist for many special cases of linear programming. For example, the single-pair shortest-path problem (Exercise 24.4-4) and the maximum-ﬂow
problem (Exercise 26.1-5) are special cases of linear programming.
Sometimes we don’t really care about the objective function; we just wish to ﬁnd
any feasible solution, that is, any vector x that satisﬁes Ax  b, or to determine
that no feasible solution exists. We shall focus on one such feasibility problem.
Systems of difference constraints
In a system of difference constraints, each row of the linear-programming matrix A
contains one 1 and one 1, and all other entries of A are 0. Thus, the constraints
given by Ax  b are a set of m difference constraints involving n unknowns, in
which each constraint is a simple linear inequality of the form
xj  xi  bk ;
where 1  i; j  n, i ¤ j , and 1  k  m.
For example, consider the problem of ﬁnding a 5-vector x D .xi/ that satisﬁes

1
1
1
1
1
1
1
1
˘
ˇ
x1
x2
x3
x4
x5



1
1
3
3
˘
:
This problem is equivalent to ﬁnding values for the unknowns x1; x2; x3; x4; x5,
satisfying the following 8 difference constraints:
x1  x2

0 ,
(24.3)
x1  x5

1 ,
(24.4)
x2  x5

1 ,
(24.5)
x3  x1

5 ,
(24.6)
x4  x1

4 ,
(24.7)
x4  x3

1 ,
(24.8)
x5  x3

3 ,
(24.9)
x5  x4

3 .
(24.10)

One solution to this problem is x D .5; 3; 0; 1; 4/, which you can verify directly by checking each inequality. In fact, this problem has more than one solution.
Another is x0 D .0; 2; 5; 4; 1/. These two solutions are related: each component
of x0 is 5 larger than the corresponding component of x. This fact is not mere
coincidence.

> **Lemma 24.8**

Let x D .x1; x2; : : : ; xn/ be a solution to a system Ax  b of difference constraints, and let d be any constant. Then x C d D .x1 C d; x2 C d; : : : ; xn C d/
is a solution to Ax  b as well.
Proof
For each xi and xj, we have .xj C d/  .xi C d/ D xj  xi. Thus, if x
satisﬁes Ax  b, so does x C d.
Systems of difference constraints occur in many different applications. For example, the unknowns xi may be times at which events are to occur. Each constraint
states that at least a certain amount of time, or at most a certain amount of time,
must elapse between two events. Perhaps the events are jobs to be performed during the assembly of a product. If we apply an adhesive that takes 2 hours to set at
time x1 and we have to wait until it sets to install a part at time x2, then we have the
constraint that x2  x1 C 2 or, equivalently, that x1  x2  2. Alternatively, we
might require that the part be installed after the adhesive has been applied but no
later than the time that the adhesive has set halfway. In this case, we get the pair of
constraints x2  x1 and x2  x1 C1 or, equivalently, x1 x2  0 and x2 x1  1.
Constraint graphs
We can interpret systems of difference constraints from a graph-theoretic point
of view.
In a system Ax  b of difference constraints, we view the m 	 n
linear-programming matrix A as the transpose of an incidence matrix (see Exercise 22.1-7) for a graph with n vertices and m edges. Each vertex i in the graph,
for i D 1; 2; : : : ; n, corresponds to one of the n unknown variables xi. Each directed edge in the graph corresponds to one of the m inequalities involving two
unknowns.
More formally, given a system Ax  b of difference constraints, the corresponding constraint graph is a weighted, directed graph G D .V; E/, where
V D f0; 1; : : : ; ng
and
E D f.i; j/ W xj  xi  bk is a constraintg
[ f.0; 1/; .0; 2/; .0; 3/; : : : ; .0; n/g :

## 24.4 Difference constraints and shortest paths

–1
–1
–3
–3
–5
–3
–1
–4
v3
v2
v1
v5
v0
v4
Figure 24.8
The constraint graph corresponding to the system (24.3)–(24.10) of difference constraints. The value of ı.0; i/ appears in each vertex i. One feasible solution to the system is
x D .5; 3; 0; 1; 4/.
The constraint graph contains the additional vertex 0, as we shall see shortly, to
guarantee that the graph has some vertex which can reach all other vertices. Thus,
the vertex set V consists of a vertex i for each unknown xi, plus an additional
vertex 0. The edge set E contains an edge for each difference constraint, plus
an edge .0; i/ for each unknown xi. If xj  xi  bk is a difference constraint,
then the weight of edge .i; j/ is w.i; j/ D bk. The weight of each edge leaving 0 is 0. Figure 24.8 shows the constraint graph for the system (24.3)–(24.10)
of difference constraints.
The following theorem shows that we can ﬁnd a solution to a system of difference constraints by ﬁnding shortest-path weights in the corresponding constraint
graph.

> **Theorem 24.9**

Given a system Ax  b of difference constraints, let G D .V; E/ be the corresponding constraint graph. If G contains no negative-weight cycles, then
x D .ı.0; 1/; ı.0; 2/; ı.0; 3/; : : : ; ı.0; n//
(24.11)
is a feasible solution for the system. If G contains a negative-weight cycle, then
there is no feasible solution for the system.
Proof
We ﬁrst show that if the constraint graph contains no negative-weight
cycles, then equation (24.11) gives a feasible solution.
Consider any edge
.i; j/ 2 E. By the triangle inequality, ı.0; j/  ı.0; i/ C w.i; j/ or,
equivalently, ı.0; j/  ı.0; i/  w.i; j/. Thus, letting xi D ı.0; i/ and

xj D ı.0; j/ satisﬁes the difference constraint xj  xi  w.i; j/ that corresponds to edge .i; j/.
Now we show that if the constraint graph contains a negative-weight cycle, then
the system of difference constraints has no feasible solution. Without loss of generality, let the negative-weight cycle be c D h1; 2; : : : ; ki, where 1 D k.
(The vertex 0 cannot be on cycle c, because it has no entering edges.) Cycle c
corresponds to the following difference constraints:
x2  x1

w.1; 2/ ;
x3  x2

w.2; 3/ ;
:::
xk1  xk2

w.k2; k1/ ;
xk  xk1

w.k1; k/ :
We will assume that x has a solution satisfying each of these k inequalities and then
derive a contradiction. The solution must also satisfy the inequality that results
when we sum the k inequalities together. If we sum the left-hand sides, each
unknown xi is added in once and subtracted out once (remember that 1 D k
implies x1 D xk), so that the left-hand side of the sum is 0. The right-hand side
sums to w.c/, and thus we obtain 0  w.c/. But since c is a negative-weight cycle,
w.c/ < 0, and we obtain the contradiction that 0  w.c/ < 0.
Solving systems of difference constraints

> **Theorem 24.9 tells us that we can use the Bellman-Ford algorithm to solve a**

system of difference constraints.
Because the constraint graph contains edges
from the source vertex 0 to all other vertices, any negative-weight cycle in the
constraint graph is reachable from 0.
If the Bellman-Ford algorithm returns
TRUE, then the shortest-path weights give a feasible solution to the system. In
Figure 24.8, for example, the shortest-path weights provide the feasible solution
x D .5; 3; 0; 1; 4/, and by Lemma 24.8, x D .d  5; d  3; d; d  1; d  4/
is also a feasible solution for any constant d. If the Bellman-Ford algorithm returns
FALSE, there is no feasible solution to the system of difference constraints.
A system of difference constraints with m constraints on n unknowns produces
a graph with n C 1 vertices and n C m edges. Thus, using the Bellman-Ford
algorithm, we can solve the system in O..n C 1/.n C m// D O.n2 C nm/ time.
Exercise 24.4-5 asks you to modify the algorithm to run in O.nm/ time, even if m
is much less than n.

## 24.4 Difference constraints and shortest paths

## Exercises

24.4-1
Find a feasible solution or determine that no feasible solution exists for the following system of difference constraints:
x1  x2

1 ,
x1  x4

4 ,
x2  x3

2 ,
x2  x5

7 ,
x2  x6

5 ,
x3  x6

10 ,
x4  x2

2 ,
x5  x1

1 ,
x5  x4

3 ,
x6  x3

8 .
24.4-2
Find a feasible solution or determine that no feasible solution exists for the following system of difference constraints:
x1  x2

4 ,
x1  x5

5 ,
x2  x4

6 ,
x3  x2

1 ,
x4  x1

3 ,
x4  x3

5 ,
x4  x5

10 ,
x5  x3

4 ,
x5  x4

8 .
24.4-3
Can any shortest-path weight from the new vertex 0 in a constraint graph be positive? Explain.
24.4-4
Express the single-pair shortest-path problem as a linear program.

24.4-5
Show how to modify the Bellman-Ford algorithm slightly so that when we use it
to solve a system of difference constraints with m inequalities on n unknowns, the
running time is O.nm/.
24.4-6
Suppose that in addition to a system of difference constraints, we want to handle
equality constraints of the form xi D xj C bk. Show how to adapt the BellmanFord algorithm to solve this variety of constraint system.
24.4-7
Show how to solve a system of difference constraints by a Bellman-Ford-like algorithm that runs on a constraint graph without the extra vertex 0.
24.4-8
?
Let Ax  b be a system of m difference constraints in n unknowns. Show that the
Bellman-Ford algorithm, when run on the corresponding constraint graph, maximizes Pn
iD1 xi subject to Ax  b and xi  0 for all xi.
24.4-9
?
Show that the Bellman-Ford algorithm, when run on the constraint graph for a system Ax  b of difference constraints, minimizes the quantity .max fxigmin fxig/
subject to Ax  b. Explain how this fact might come in handy if the algorithm is
used to schedule construction jobs.
24.4-10
Suppose that every row in the matrix A of a linear program Ax  b corresponds to
a difference constraint, a single-variable constraint of the form xi  bk, or a singlevariable constraint of the form xi  bk. Show how to adapt the Bellman-Ford
algorithm to solve this variety of constraint system.
24.4-11
Give an efﬁcient algorithm to solve a system Ax  b of difference constraints
when all of the elements of b are real-valued and all of the unknowns xi must be
integers.
24.4-12
?
Give an efﬁcient algorithm to solve a system Ax  b of difference constraints
when all of the elements of b are real-valued and a speciﬁed subset of some, but
not necessarily all, of the unknowns xi must be integers.

## 24.5 Proofs of shortest-paths properties

## 24.5 Proofs of shortest-paths properties

Throughout this chapter, our correctness arguments have relied on the triangle
inequality, upper-bound property, no-path property, convergence property, pathrelaxation property, and predecessor-subgraph property. We stated these properties
without proof at the beginning of this chapter. In this section, we prove them.
The triangle inequality
In studying breadth-ﬁrst search (Section 22.2), we proved as Lemma 22.1 a simple property of shortest distances in unweighted graphs. The triangle inequality
generalizes the property to weighted graphs.

> **Lemma 24.10 (Triangle inequality)**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R
and source vertex s. Then, for all edges .u; / 2 E, we have
ı.s; /  ı.s; u/ C w.u; / :
Proof
Suppose that p is a shortest path from source s to vertex . Then p has
no more weight than any other path from s to . Speciﬁcally, path p has no more
weight than the particular path that takes a shortest path from source s to vertex u
and then takes edge .u; /.
Exercise 24.5-3 asks you to handle the case in which there is no shortest path
from s to .
Effects of relaxation on shortest-path estimates
The next group of lemmas describes how shortest-path estimates are affected when
we execute a sequence of relaxation steps on the edges of a weighted, directed
graph that has been initialized by INITIALIZE-SINGLE-SOURCE.

> **Lemma 24.11 (Upper-bound property)**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R.
Let s 2 V be the source vertex, and let the graph be initialized by INITIALIZESINGLE-SOURCE.G; s/. Then, :d  ı.s; / for all  2 V , and this invariant is
maintained over any sequence of relaxation steps on the edges of G. Moreover,
once :d achieves its lower bound ı.s; /, it never changes.

Proof
We prove the invariant :d  ı.s; / for all vertices  2 V by induction
over the number of relaxation steps.
For the basis, :d  ı.s; / is certainly true after initialization, since :d D 1
implies :d  ı.s; / for all  2 V  fsg, and since s:d D 0  ı.s; s/ (note that
ı.s; s/ D 1 if s is on a negative-weight cycle and 0 otherwise).
For the inductive step, consider the relaxation of an edge .u; /. By the inductive
hypothesis, x:d  ı.s; x/ for all x 2 V prior to the relaxation. The only d value
that may change is :d. If it changes, we have
:d
D
u:d C w.u; /

ı.s; u/ C w.u; /
(by the inductive hypothesis)

ı.s; /
(by the triangle inequality) ,
and so the invariant is maintained.
To see that the value of :d never changes once :d D ı.s; /, note that having
achieved its lower bound, :d cannot decrease because we have just shown that
:d  ı.s; /, and it cannot increase because relaxation steps do not increase d
values.

> **Corollary 24.12 (No-path property)**

Suppose that in a weighted, directed graph G D .V; E/ with weight function
w W E ! R, no path connects a source vertex s 2 V to a given vertex  2 V .
Then, after the graph is initialized by INITIALIZE-SINGLE-SOURCE.G; s/, we
have :d D ı.s; / D 1, and this equality is maintained as an invariant over
any sequence of relaxation steps on the edges of G.
Proof
By the upper-bound property, we always have 1 D ı.s; /  :d, and
thus :d D 1 D ı.s; /.

> **Lemma 24.13**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R,
and let .u; / 2 E. Then, immediately after relaxing edge .u; / by executing
RELAX.u; ; w/, we have :d  u:d C w.u; /.
Proof
If, just prior to relaxing edge .u; /, we have :d > u:d C w.u; /, then
:d D u:d C w.u; / afterward. If, instead, :d  u:d C w.u; / just before
the relaxation, then neither u:d nor :d changes, and so :d  u:d C w.u; /
afterward.

> **Lemma 24.14 (Convergence property)**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R,
let s 2 V be a source vertex, and let s ; u !  be a shortest path in G for

## 24.5 Proofs of shortest-paths properties

some vertices u;  2 V . Suppose that G is initialized by INITIALIZE-SINGLESOURCE.G; s/ and then a sequence of relaxation steps that includes the call
RELAX.u; ; w/ is executed on the edges of G. If u:d D ı.s; u/ at any time
prior to the call, then :d D ı.s; / at all times after the call.
Proof
By the upper-bound property, if u:d D ı.s; u/ at some point prior to relaxing edge .u; /, then this equality holds thereafter. In particular, after relaxing
edge .u; /, we have
:d

u:d C w.u; /
(by Lemma 24.13)
D
ı.s; u/ C w.u; /
D
ı.s; /
(by Lemma 24.1) .
By the upper-bound property, :d  ı.s; /, from which we conclude that
:d D ı.s; /, and this equality is maintained thereafter.

> **Lemma 24.15 (Path-relaxation property)**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R,
and let s 2 V be a source vertex. Consider any shortest path p D h0; 1; : : : ; ki
from s D 0 to k. If G is initialized by INITIALIZE-SINGLE-SOURCE.G; s/ and
then a sequence of relaxation steps occurs that includes, in order, relaxing the edges
.0; 1/; .1; 2/; : : : ; .k1; k/, then k:d D ı.s; k/ after these relaxations and
at all times afterward. This property holds no matter what other edge relaxations
occur, including relaxations that are intermixed with relaxations of the edges of p.
Proof
We show by induction that after the ith edge of path p is relaxed, we have
i:d D ı.s; i/. For the basis, i D 0, and before any edges of p have been relaxed,
we have from the initialization that 0:d D s:d D 0 D ı.s; s/. By the upper-bound
property, the value of s:d never changes after initialization.
For the inductive step, we assume that i1:d D ı.s; i1/, and we examine
what happens when we relax edge .i1; i/. By the convergence property, after
relaxing this edge, we have i:d D ı.s; i/, and this equality is maintained at all
times thereafter.
Relaxation and shortest-paths trees
We now show that once a sequence of relaxations has caused the shortest-path estimates to converge to shortest-path weights, the predecessor subgraph G induced
by the resulting  values is a shortest-paths tree for G. We start with the following lemma, which shows that the predecessor subgraph always forms a rooted tree
whose root is the source.

> **Lemma 24.16**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R,
let s 2 V be a source vertex, and assume that G contains no negative-weight
cycles that are reachable from s. Then, after the graph is initialized by INITIALIZESINGLE-SOURCE.G; s/, the predecessor subgraph G forms a rooted tree with
root s, and any sequence of relaxation steps on edges of G maintains this property
as an invariant.
Proof
Initially, the only vertex in G is the source vertex, and the lemma is trivially true. Consider a predecessor subgraph G that arises after a sequence of
relaxation steps. We shall ﬁrst prove that G is acyclic. Suppose for the sake of
contradiction that some relaxation step creates a cycle in the graph G. Let the cycle be c D h0;1;: : : ;ki, where k D 0. Then, i: D i1 for i D 1; 2; : : : ; k
and, without loss of generality, we can assume that relaxing edge .k1; k/ created
the cycle in G.
We claim that all vertices on cycle c are reachable from the source s. Why?
Each vertex on c has a non-NIL predecessor, and so each vertex on c was assigned
a ﬁnite shortest-path estimate when it was assigned its non-NIL  value. By the
upper-bound property, each vertex on cycle c has a ﬁnite shortest-path weight,
which implies that it is reachable from s.
We shall examine the shortest-path estimates on c just prior to the call
RELAX.k1; k; w/ and show that c is a negative-weight cycle, thereby contradicting the assumption that G contains no negative-weight cycles that are reachable
from the source. Just before the call, we have i: D i1 for i D 1; 2; : : : ; k  1.
Thus, for i D 1; 2; : : : ; k  1, the last update to i:d was by the assignment
i:d D i1:dCw.i1; i/. If i1:d changed since then, it decreased. Therefore,
just before the call RELAX.k1; k; w/, we have
i:d  i1:d C w.i1; i/
for all i D 1; 2; : : : ; k  1 :
(24.12)
Because k: is changed by the call, immediately beforehand we also have the
strict inequality
k:d > k1:d C w.k1; k/ :
Summing this strict inequality with the k  1 inequalities (24.12), we obtain the
sum of the shortest-path estimates around cycle c:
k
X
iD1
i:d
>
k
X
iD1
.i1:d C w.i1; i//
D
k
X
iD1
i1:d C
k
X
iD1
w.i1; i/ :

## 24.5 Proofs of shortest-paths properties

s
u
x
y
z
v
Figure 24.9
Showing that a simple path in G from source s to vertex  is unique. If there are two
paths p1 (s ; u ; x ! ´ ; ) and p2 (s ; u ; y ! ´ ; ), where x ¤ y, then ´: D x
and ´: D y, a contradiction.
But
k
X
iD1
i:d D
k
X
iD1
i1:d ;
since each vertex in the cycle c appears exactly once in each summation. This
equality implies
0 >
k
X
iD1
w.i1; i/ :
Thus, the sum of weights around the cycle c is negative, which provides the desired
contradiction.
We have now proven that G is a directed, acyclic graph. To show that it forms
a rooted tree with root s, it sufﬁces (see Exercise B.5-2) to prove that for each
vertex  2 V, there is a unique simple path from s to  in G.
We ﬁrst must show that a path from s exists for each vertex in V. The vertices in V are those with non-NIL  values, plus s. The idea here is to prove by
induction that a path exists from s to all vertices in V. We leave the details as
Exercise 24.5-6.
To complete the proof of the lemma, we must now show that for any vertex
 2 V, the graph G contains at most one simple path from s to . Suppose otherwise. That is, suppose that, as Figure 24.9 illustrates, G contains two simple paths
from s to some vertex : p1, which we decompose into s ; u ; x ! ´ ; ,
and p2, which we decompose into s ; u ; y ! ´ ; , where x ¤ y (though u
could be s and ´ could be ). But then, ´: D x and ´: D y, which implies
the contradiction that x D y. We conclude that G contains a unique simple path
from s to , and thus G forms a rooted tree with root s.
We can now show that if, after we have performed a sequence of relaxation steps,
all vertices have been assigned their true shortest-path weights, then the predecessor subgraph G is a shortest-paths tree.

> **Lemma 24.17 (Predecessor-subgraph property)**

Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R,
let s 2 V be a source vertex, and assume that G contains no negative-weight cycles
that are reachable from s. Let us call INITIALIZE-SINGLE-SOURCE.G; s/ and then
execute any sequence of relaxation steps on edges of G that produces :d D ı.s; /
for all  2 V . Then, the predecessor subgraph G is a shortest-paths tree rooted
at s.
Proof
We must prove that the three properties of shortest-paths trees given on
page 647 hold for G. To show the ﬁrst property, we must show that V is the set
of vertices reachable from s. By deﬁnition, a shortest-path weight ı.s; / is ﬁnite
if and only if  is reachable from s, and thus the vertices that are reachable from s
are exactly those with ﬁnite d values. But a vertex  2 V  fsg has been assigned
a ﬁnite value for :d if and only if : ¤ NIL. Thus, the vertices in V are exactly
those reachable from s.
The second property follows directly from Lemma 24.16.
It remains, therefore, to prove the last property of shortest-paths trees: for each
vertex  2 V, the unique simple path s
p;  in G is a shortest path from s to 
in G. Let p D h0; 1; : : : ; ki, where 0 D s and k D . For i D 1; 2; : : : ; k,
we have both i:d D ı.s; i/ and i:d  i1:d C w.i1; i/, from which we
conclude w.i1; i/  ı.s; i/  ı.s; i1/. Summing the weights along path p
yields
w.p/
D
k
X
iD1
w.i1; i/

k
X
iD1
.ı.s; i/  ı.s; i1//
D
ı.s; k/  ı.s; 0/
(because the sum telescopes)
D
ı.s; k/
(because ı.s; 0/ D ı.s; s/ D 0) .
Thus, w.p/  ı.s; k/. Since ı.s; k/ is a lower bound on the weight of any path
from s to k, we conclude that w.p/ D ı.s; k/, and thus p is a shortest path
from s to  D k.

## Exercises

24.5-1
Give two shortest-paths trees for the directed graph of Figure 24.2 (on page 648)
other than the two shown.

## 24.5 Proofs of shortest-paths properties

24.5-2
Give an example of a weighted, directed graph G D .V; E/ with weight function
w W E ! R and source vertex s such that G satisﬁes the following property: For
every edge .u; / 2 E, there is a shortest-paths tree rooted at s that contains .u; /
and another shortest-paths tree rooted at s that does not contain .u; /.
24.5-3
Embellish the proof of Lemma 24.10 to handle cases in which shortest-path
weights are 1 or 1.
24.5-4
Let G D .V; E/ be a weighted, directed graph with source vertex s, and let G
be initialized by INITIALIZE-SINGLE-SOURCE.G; s/. Prove that if a sequence of
relaxation steps sets s: to a non-NIL value, then G contains a negative-weight
cycle.
24.5-5
Let G D .V; E/ be a weighted, directed graph with no negative-weight edges. Let
s 2 V be the source vertex, and suppose that we allow : to be the predecessor
of  on any shortest path to  from source s if  2 V  fsg is reachable from s,
and NIL otherwise. Give an example of such a graph G and an assignment of 
values that produces a cycle in G. (By Lemma 24.16, such an assignment cannot
be produced by a sequence of relaxation steps.)
24.5-6
Let G D .V; E/ be a weighted, directed graph with weight function w W E ! R
and no negative-weight cycles. Let s 2 V be the source vertex, and let G be initialized by INITIALIZE-SINGLE-SOURCE.G; s/. Prove that for every vertex  2 V,
there exists a path from s to  in G and that this property is maintained as an
invariant over any sequence of relaxations.
24.5-7
Let G D .V; E/ be a weighted, directed graph that contains no negative-weight
cycles. Let s 2 V be the source vertex, and let G be initialized by INITIALIZESINGLE-SOURCE.G; s/. Prove that there exists a sequence of jV j  1 relaxation
steps that produces :d D ı.s; / for all  2 V .
24.5-8
Let G be an arbitrary weighted, directed graph with a negative-weight cycle reachable from the source vertex s. Show how to construct an inﬁnite sequence of relaxations of the edges of G such that every relaxation causes a shortest-path estimate
to change.

## Problems

24-1
Yen’s improvement to Bellman-Ford
Suppose that we order the edge relaxations in each pass of the Bellman-Ford algorithm as follows.
Before the ﬁrst pass, we assign an arbitrary linear order
1; 2; : : : ; jV j to the vertices of the input graph G D .V; E/. Then, we partition the edge set E into Ef [ Eb, where Ef D f.i; j/ 2 E W i < j g and
Eb D f.i; j/ 2 E W i > j g. (Assume that G contains no self-loops, so that every
edge is in either Ef or Eb.) Deﬁne Gf D .V; Ef / and Gb D .V; Eb/.
a. Prove that Gf is acyclic with topological sort h1; 2; : : : ; jV ji and that Gb is
acyclic with topological sort hjV j; jV j1; : : : ; 1i.
Suppose that we implement each pass of the Bellman-Ford algorithm in the following way. We visit each vertex in the order 1; 2; : : : ; jV j, relaxing edges of Ef
that leave the vertex. We then visit each vertex in the order jV j; jV j1; : : : ; 1,
relaxing edges of Eb that leave the vertex.
b. Prove that with this scheme, if G contains no negative-weight cycles that are
reachable from the source vertex s, then after only djV j =2e passes over the
edges, :d D ı.s; / for all vertices  2 V .
c. Does this scheme improve the asymptotic running time of the Bellman-Ford
algorithm?
24-2
Nesting boxes
A d-dimensional box with dimensions .x1; x2; : : : ; xd/ nests within another box
with dimensions .y1; y2; : : : ; yd/ if there exists a permutation  on f1; 2; : : : ; dg
such that x.1/ < y1, x.2/ < y2, . . . , x.d/ < yd.
a. Argue that the nesting relation is transitive.
b. Describe an efﬁcient method to determine whether or not one d-dimensional
box nests inside another.
c. Suppose that you are given a set of n d-dimensional boxes fB1; B2; : : : ; Bng.
Give an efﬁcient algorithm to ﬁnd the longest sequence hBi1; Bi2; : : : ; Biki of
boxes such that Bij nests within BijC1 for j D 1; 2; : : : ; k  1. Express the
running time of your algorithm in terms of n and d.

Problems for Chapter 24
24-3
Arbitrage
Arbitrage is the use of discrepancies in currency exchange rates to transform one
unit of a currency into more than one unit of the same currency. For example,
suppose that 1 U.S. dollar buys 49 Indian rupees, 1 Indian rupee buys 2 Japanese
yen, and 1 Japanese yen buys 0:0107 U.S. dollars. Then, by converting currencies,
a trader can start with 1 U.S. dollar and buy 49	2	0:0107 D 1:0486 U.S. dollars,
thus turning a proﬁt of 4:86 percent.
Suppose that we are given n currencies c1; c2; : : : ; cn and an n 	 n table R of
exchange rates, such that one unit of currency ci buys RŒi; j  units of currency cj.
a. Give an efﬁcient algorithm to determine whether or not there exists a sequence
of currencies hci1; ci2; : : : ; ciki such that
RŒi1; i2  RŒi2; i3    RŒik1; ik  RŒik; i1 > 1 :
Analyze the running time of your algorithm.
b. Give an efﬁcient algorithm to print out such a sequence if one exists. Analyze
the running time of your algorithm.
24-4
Gabow’s scaling algorithm for single-source shortest paths
A scaling algorithm solves a problem by initially considering only the highestorder bit of each relevant input value (such as an edge weight). It then reﬁnes the
initial solution by looking at the two highest-order bits. It progressively looks at
more and more high-order bits, reﬁning the solution each time, until it has examined all bits and computed the correct solution.
In this problem, we examine an algorithm for computing the shortest paths from
a single source by scaling edge weights. We are given a directed graph G D .V; E/
with nonnegative integer edge weights w. Let W D max.u;/2E fw.u; /g. Our
goal is to develop an algorithm that runs in O.E lg W / time. We assume that all
vertices are reachable from the source.
The algorithm uncovers the bits in the binary representation of the edge weights
one at a time, from the most signiﬁcant bit to the least signiﬁcant bit. Speciﬁcally,
let k D dlg.W C 1/e be the number of bits in the binary representation of W ,
and for i D 1; 2; : : : ; k, let wi.u; / D

w.u; /=2ki˘
. That is, wi.u; / is the
“scaled-down” version of w.u; / given by the i most signiﬁcant bits of w.u; /.
(Thus, wk.u; / D w.u; / for all .u; / 2 E.) For example, if k D 5 and
w.u; / D 25, which has the binary representation h11001i, then w3.u; / D
h110i D 6. As another example with k D 5, if w.u; / D h00100i D 4, then
w3.u; / D h001i D 1. Let us deﬁne ıi.u; / as the shortest-path weight from
vertex u to vertex  using weight function wi. Thus, ık.u; / D ı.u; / for all
u;  2 V . For a given source vertex s, the scaling algorithm ﬁrst computes the

shortest-path weights ı1.s; / for all  2 V , then computes ı2.s; / for all  2 V ,
and so on, until it computes ık.s; / for all  2 V . We assume throughout that
jEj  jV j  1, and we shall see that computing ıi from ıi1 takes O.E/ time, so
that the entire algorithm takes O.kE/ D O.E lg W / time.
a. Suppose that for all vertices  2 V , we have ı.s; /  jEj. Show that we can
compute ı.s; / for all  2 V in O.E/ time.
b. Show that we can compute ı1.s; / for all  2 V in O.E/ time.
Let us now focus on computing ıi from ıi1.
c. Prove that for i D 2; 3; : : : ; k, we have either wi.u; / D 2wi1.u; / or
wi.u; / D 2wi1.u; / C 1. Then, prove that
2ıi1.s; /  ıi.s; /  2ıi1.s; / C jV j  1
for all  2 V .
d. Deﬁne for i D 2; 3; : : : ; k and all .u; / 2 E,
ywi.u; / D wi.u; / C 2ıi1.s; u/  2ıi1.s; / :
Prove that for i D 2; 3; : : : ; k and all u;  2 V , the “reweighted” value ywi.u; /
of edge .u; / is a nonnegative integer.
e. Now, deﬁne yıi.s; / as the shortest-path weight from s to  using the weight
function ywi. Prove that for i D 2; 3; : : : ; k and all  2 V ,
ıi.s; / D yıi.s; / C 2ıi1.s; /
and that yıi.s; /  jEj.
f.
Show how to compute ıi.s; / from ıi1.s; / for all  2 V in O.E/ time, and
conclude that we can compute ı.s; / for all  2 V in O.E lg W / time.
24-5
Karp’s minimum mean-weight cycle algorithm
Let G D .V; E/ be a directed graph with weight function w W E ! R, and let
n D jV j. We deﬁne the mean weight of a cycle c D he1; e2; : : : ; eki of edges in E
to be

.c/ D 1
k
k
X
iD1
w.ei/ :

Problems for Chapter 24
Let
 D minc
.c/, where c ranges over all directed cycles in G. We call a cycle c
for which
.c/ D
 a minimum mean-weight cycle. This problem investigates
an efﬁcient algorithm for computing
.
Assume without loss of generality that every vertex  2 V is reachable from a
source vertex s 2 V . Let ı.s; / be the weight of a shortest path from s to , and let
ık.s; / be the weight of a shortest path from s to  consisting of exactly k edges.
If there is no path from s to  with exactly k edges, then ık.s; / D 1.
a. Show that if
 D 0, then G contains no negative-weight cycles and ı.s; / D
min0kn1 ık.s; / for all vertices  2 V .
b. Show that if
 D 0, then
max
0kn1
ın.s; /  ık.s; /
n  k
 0
for all vertices  2 V . (Hint: Use both properties from part (a).)
c. Let c be a 0-weight cycle, and let u and  be any two vertices on c. Suppose
that
 D 0 and that the weight of the simple path from u to  along the cycle
is x. Prove that ı.s; / D ı.s; u/ C x. (Hint: The weight of the simple path
from  to u along the cycle is x.)
d. Show that if
 D 0, then on each minimum mean-weight cycle there exists a
vertex  such that
max
0kn1
ın.s; /  ık.s; /
n  k
D 0 :
(Hint: Show how to extend a shortest path to any vertex on a minimum meanweight cycle along the cycle to make a shortest path to the next vertex on the
cycle.)
e. Show that if
 D 0, then
min
2V
max
0kn1
ın.s; /  ık.s; /
n  k
D 0 :
f. Show that if we add a constant t to the weight of each edge of G, then

increases by t. Use this fact to show that

 D min
2V
max
0kn1
ın.s; /  ık.s; /
n  k
:
g. Give an O.VE/-time algorithm to compute
.

24-6
Bitonic shortest paths
A sequence is bitonic if it monotonically increases and then monotonically decreases, or if by a circular shift it monotonically increases and then monotonically
decreases. For example the sequences h1; 4; 6; 8; 3; 2i, h9; 2; 4; 10; 5i, and
h1; 2; 3; 4i are bitonic, but h1; 3; 12; 4; 2; 10i is not bitonic. (See Problem 15-3 for
the bitonic euclidean traveling-salesman problem.)
Suppose that we are given a directed graph G D .V; E/ with weight function
w W E ! R, where all edge weights are unique, and we wish to ﬁnd single-source
shortest paths from a source vertex s. We are given one additional piece of information: for each vertex  2 V , the weights of the edges along any shortest path
from s to  form a bitonic sequence.
Give the most efﬁcient algorithm you can to solve this problem, and analyze its
running time.
Chapter notes
Dijkstra’s algorithm [88] appeared in 1959, but it contained no mention of a priority
queue. The Bellman-Ford algorithm is based on separate algorithms by Bellman
[38] and Ford [109]. Bellman describes the relation of shortest paths to difference
constraints. Lawler [224] describes the linear-time algorithm for shortest paths in
a dag, which he considers part of the folklore.
When edge weights are relatively small nonnegative integers, we have more efﬁcient algorithms to solve the single-source shortest-paths problem. The sequence
of values returned by the EXTRACT-MIN calls in Dijkstra’s algorithm monotonically increases over time. As discussed in the chapter notes for Chapter 6, in
this case several data structures can implement the various priority-queue operations more efﬁciently than a binary heap or a Fibonacci heap. Ahuja, Mehlhorn,
Orlin, and Tarjan [8] give an algorithm that runs in O.E C V
p
lg W / time on
graphs with nonnegative edge weights, where W is the largest weight of any edge
in the graph. The best bounds are by Thorup [337], who gives an algorithm that
runs in O.E lg lg V / time, and by Raman [291], who gives an algorithm that runs
in O

E C V min
˚
.lg V /1=3C; .lg W /1=4C

time. These two algorithms use an
amount of space that depends on the word size of the underlying machine. Although the amount of space used can be unbounded in the size of the input, it can
be reduced to be linear in the size of the input using randomized hashing.
For undirected graphs with integer weights, Thorup [336] gives an O.V C E/time algorithm for single-source shortest paths. In contrast to the algorithms mentioned in the previous paragraph, this algorithm is not an implementation of DijkNotes for Chapter 24
stra’s algorithm, since the sequence of values returned by EXTRACT-MIN calls
does not monotonically increase over time.
For graphs with negative edge weights, an algorithm due to Gabow and Tarjan [122] runs in O.
p
V E lg.V W // time, and one by Goldberg [137] runs in
O.
p
V E lg W / time, where W D max.u;/2E fjw.u; /jg.
Cherkassky, Goldberg, and Radzik [64] conducted extensive experiments comparing various shortest-path algorithms.
