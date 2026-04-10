# 22 Elementary Graph Algorithms

22
Elementary Graph Algorithms
This chapter presents methods for representing a graph and for searching a graph.
Searching a graph means systematically following the edges of the graph so as to
visit the vertices of the graph. A graph-searching algorithm can discover much
about the structure of a graph. Many algorithms begin by searching their input
graph to obtain this structural information. Several other graph algorithms elabo-
rate on basic graph searching. Techniques for searching a graph lie at the heart of
the ﬁeld of graph algorithms.
Section 22.1 discusses the two most common computational representations of
graphs: as adjacency lists and as adjacency matrices. Section 22.2 presents a sim-
ple graph-searching algorithm called breadth-ﬁrst search and shows how to cre-
ate a breadth-ﬁrst tree. Section 22.3 presents depth-ﬁrst search and proves some
standard results about the order in which depth-ﬁrst search visits vertices. Sec-
tion 22.4 provides our ﬁrst real application of depth-ﬁrst search: topologically sort-
ing a directed acyclic graph. A second application of depth-ﬁrst search, ﬁnding the
strongly connected components of a directed graph, is the topic of Section 22.5.
22.1
Representations of graphs
We can choose between two standard ways to represent a graph G D .V; E/:
as a collection of adjacency lists or as an adjacency matrix. Either way applies
to both directed and undirected graphs. Because the adjacency-list representation
provides a compact way to represent sparse graphs—those for which jEj is much
less than jV j2—it is usually the method of choice. Most of the graph algorithms
presented in this book assume that an input graph is represented in adjacency-
list form. We may prefer an adjacency-matrix representation, however, when the
graph is dense—jEj is close to jV j2—or when we need to be able to tell quickly
if there is an edge connecting two given vertices. For example, two of the all-pairs

590
Chapter 22
Elementary Graph Algorithms
1
2
3
4
5
1
2
3
4
5
2
5
1
2
2
4
1
2
5
3
4
4
5
3
1
0
0
1
0
1
1
1
1
0
1
0
1
1
0
1
1
0
1
0
0
1
0
0
1
1
2
3
4
5
1
2
3
4
5
(a)
(b)
(c)
Figure 22.1
Two representations of an undirected graph. (a) An undirected graph G with 5 vertices
and 7 edges. (b) An adjacency-list representation of G. (c) The adjacency-matrix representation
of G.
1
2
5
4
1
2
3
4
5
2
4
5
6
2
4
6
5
1
0
1
0
0
0
0
1
0
0
0
1
1
0
0
0
0
0
1
0
0
0
0
0
0
1
2
3
4
5
1
2
3
4
5
(a)
(b)
(c)
3
6
6
6
6
0
0
0
0
0
1
0
0
1
0
0
Figure 22.2
Two representations of a directed graph. (a) A directed graph G with 6 vertices and 8
edges. (b) An adjacency-list representation of G. (c) The adjacency-matrix representation of G.
shortest-paths algorithms presented in Chapter 25 assume that their input graphs
are represented by adjacency matrices.
The adjacency-list representation of a graph G D .V; E/ consists of an ar-
ray Adj of jV j lists, one for each vertex in V . For each u 2 V , the adjacency list
AdjŒu contains all the vertices  such that there is an edge .u; / 2 E. That is,
AdjŒu consists of all the vertices adjacent to u in G. (Alternatively, it may contain
pointers to these vertices.) Since the adjacency lists represent the edges of a graph,
in pseudocode we treat the array Adj as an attribute of the graph, just as we treat
the edge set E. In pseudocode, therefore, we will see notation such as G:AdjŒu.
Figure 22.1(b) is an adjacency-list representation of the undirected graph in Fig-
ure 22.1(a). Similarly, Figure 22.2(b) is an adjacency-list representation of the
directed graph in Figure 22.2(a).
If G is a directed graph, the sum of the lengths of all the adjacency lists is jEj,
since an edge of the form .u; / is represented by having  appear in AdjŒu. If G is

22.1
Representations of graphs
591
an undirected graph, the sum of the lengths of all the adjacency lists is 2 jEj, since
if .u; / is an undirected edge, then u appears in ’s adjacency list and vice versa.
For both directed and undirected graphs, the adjacency-list representation has the
desirable property that the amount of memory it requires is ‚.V C E/.
We can readily adapt adjacency lists to represent weighted graphs, that is, graphs
for which each edge has an associated weight, typically given by a weight function
w W E ! R. For example, let G D .V; E/ be a weighted graph with weight
function w. We simply store the weight w.u; / of the edge .u; / 2 E with
vertex  in u’s adjacency list. The adjacency-list representation is quite robust in
that we can modify it to support many other graph variants.
A potential disadvantage of the adjacency-list representation is that it provides
no quicker way to determine whether a given edge .u; / is present in the graph
than to search for  in the adjacency list AdjŒu. An adjacency-matrix representa-
tion of the graph remedies this disadvantage, but at the cost of using asymptotically
more memory. (See Exercise 22.1-8 for suggestions of variations on adjacency lists
that permit faster edge lookup.)
For the adjacency-matrix representation of a graph G D .V; E/, we assume
that the vertices are numbered 1; 2; : : : ; jV j in some arbitrary manner. Then the
adjacency-matrix representation of a graph G consists of a jV j 	 jV j matrix
A D .aij/ such that
aij D
(
1
if .i; j / 2 E ;
0
otherwise :
Figures 22.1(c) and 22.2(c) are the adjacency matrices of the undirected and di-
rected graphs in Figures 22.1(a) and 22.2(a), respectively. The adjacency matrix of
a graph requires ‚.V 2/ memory, independent of the number of edges in the graph.
Observe the symmetry along the main diagonal of the adjacency matrix in Fig-
ure 22.1(c). Since in an undirected graph, .u; / and .; u/ represent the same
edge, the adjacency matrix A of an undirected graph is its own transpose: A D AT.
In some applications, it pays to store only the entries on and above the diagonal of
the adjacency matrix, thereby cutting the memory needed to store the graph almost
in half.
Like the adjacency-list representation of a graph, an adjacency matrix can repre-
sent a weighted graph. For example, if G D .V; E/ is a weighted graph with edge-
weight function w, we can simply store the weight w.u; / of the edge .u; / 2 E
as the entry in row u and column  of the adjacency matrix. If an edge does not
exist, we can store a NIL value as its corresponding matrix entry, though for many
problems it is convenient to use a value such as 0 or 1.
Although the adjacency-list representation is asymptotically at least as space-
efﬁcient as the adjacency-matrix representation, adjacency matrices are simpler,
and so we may prefer them when graphs are reasonably small. Moreover, adja-

592
Chapter 22
Elementary Graph Algorithms
cency matrices carry a further advantage for unweighted graphs: they require only
one bit per entry.
Representing attributes
Most algorithms that operate on graphs need to maintain attributes for vertices
and/or edges. We indicate these attributes using our usual notation, such as :d
for an attribute d of a vertex . When we indicate edges as pairs of vertices, we
use the same style of notation. For example, if edges have an attribute f , then we
denote this attribute for edge .u; / by .u; /:f. For the purpose of presenting and
understanding algorithms, our attribute notation sufﬁces.
Implementing vertex and edge attributes in real programs can be another story
entirely. There is no one best way to store and access vertex and edge attributes.
For a given situation, your decision will likely depend on the programming lan-
guage you are using, the algorithm you are implementing, and how the rest of your
program uses the graph. If you represent a graph using adjacency lists, one design
represents vertex attributes in additional arrays, such as an array dŒ1 : : jV j that
parallels the Adj array. If the vertices adjacent to u are in AdjŒu, then what we call
the attribute u:d would actually be stored in the array entry dŒu. Many other ways
of implementing attributes are possible. For example, in an object-oriented pro-
gramming language, vertex attributes might be represented as instance variables
within a subclass of a Vertex class.
Exercises
22.1-1
Given an adjacency-list representation of a directed graph, how long does it take
to compute the out-degree of every vertex? How long does it take to compute the
in-degrees?
22.1-2
Give an adjacency-list representation for a complete binary tree on 7 vertices. Give
an equivalent adjacency-matrix representation. Assume that vertices are numbered
from 1 to 7 as in a binary heap.
22.1-3
The transpose of a directed graph G D .V; E/ is the graph GT D .V; ET/, where
ET D f.; u/ 2 V 	 V W .u; / 2 Eg. Thus, GT is G with all its edges reversed.
Describe efﬁcient algorithms for computing GT from G, for both the adjacency-
list and adjacency-matrix representations of G. Analyze the running times of your
algorithms.

22.1
Representations of graphs
593
22.1-4
Given an adjacency-list representation of a multigraph G D .V; E/, describe an
O.V C E/-time algorithm to compute the adjacency-list representation of the
“equivalent” undirected graph G0 D .V; E0/, where E0 consists of the edges in E
with all multiple edges between two vertices replaced by a single edge and with all
self-loops removed.
22.1-5
The square of a directed graph G D .V; E/ is the graph G2 D .V; E2/ such that
.u; / 2 E2 if and only G contains a path with at most two edges between u and .
Describe efﬁcient algorithms for computing G2 from G for both the adjacency-
list and adjacency-matrix representations of G. Analyze the running times of your
algorithms.
22.1-6
Most graph algorithms that take an adjacency-matrix representation as input re-
quire time .V 2/, but there are some exceptions. Show how to determine whether
a directed graph G contains a universal sink—a vertex with in-degree jV j  1 and
out-degree 0—in time O.V /, given an adjacency matrix for G.
22.1-7
The incidence matrix of a directed graph G D .V; E/ with no self-loops is a
jV j 	 jEj matrix B D .bij/ such that
bij D

1
if edge j leaves vertex i ;
1
if edge j enters vertex i ;
0
otherwise :
Describe what the entries of the matrix product BBT represent, where BT is the
transpose of B.
22.1-8
Suppose that instead of a linked list, each array entry AdjŒu is a hash table contain-
ing the vertices  for which .u; / 2 E. If all edge lookups are equally likely, what
is the expected time to determine whether an edge is in the graph? What disadvan-
tages does this scheme have? Suggest an alternate data structure for each edge list
that solves these problems. Does your alternative have disadvantages compared to
the hash table?

594
Chapter 22
Elementary Graph Algorithms
22.2
Breadth-ﬁrst search
Breadth-ﬁrst search is one of the simplest algorithms for searching a graph and
the archetype for many important graph algorithms. Prim’s minimum-spanning-
tree algorithm (Section 23.2) and Dijkstra’s single-source shortest-paths algorithm
(Section 24.3) use ideas similar to those in breadth-ﬁrst search.
Given a graph G D .V; E/ and a distinguished source vertex s, breadth-ﬁrst
search systematically explores the edges of G to “discover” every vertex that is
reachable from s. It computes the distance (smallest number of edges) from s
to each reachable vertex. It also produces a “breadth-ﬁrst tree” with root s that
contains all reachable vertices. For any vertex  reachable from s, the simple path
in the breadth-ﬁrst tree from s to  corresponds to a “shortest path” from s to 
in G, that is, a path containing the smallest number of edges. The algorithm works
on both directed and undirected graphs.
Breadth-ﬁrst search is so named because it expands the frontier between discov-
ered and undiscovered vertices uniformly across the breadth of the frontier. That
is, the algorithm discovers all vertices at distance k from s before discovering any
vertices at distance k C 1.
To keep track of progress, breadth-ﬁrst search colors each vertex white, gray, or
black. All vertices start out white and may later become gray and then black. A
vertex is discovered the ﬁrst time it is encountered during the search, at which time
it becomes nonwhite. Gray and black vertices, therefore, have been discovered, but
breadth-ﬁrst search distinguishes between them to ensure that the search proceeds
in a breadth-ﬁrst manner.1 If .u; / 2 E and vertex u is black, then vertex 
is either gray or black; that is, all vertices adjacent to black vertices have been
discovered. Gray vertices may have some adjacent white vertices; they represent
the frontier between discovered and undiscovered vertices.
Breadth-ﬁrst search constructs a breadth-ﬁrst tree, initially containing only its
root, which is the source vertex s. Whenever the search discovers a white vertex 
in the course of scanning the adjacency list of an already discovered vertex u, the
vertex  and the edge .u; / are added to the tree. We say that u is the predecessor
or parent of  in the breadth-ﬁrst tree. Since a vertex is discovered at most once, it
has at most one parent. Ancestor and descendant relationships in the breadth-ﬁrst
tree are deﬁned relative to the root s as usual: if u is on the simple path in the tree
from the root s to vertex , then u is an ancestor of  and  is a descendant of u.
1We distinguish between gray and black vertices to help us understand how breadth-ﬁrst search op-
erates. In fact, as Exercise 22.2-3 shows, we would get the same result even if we did not distinguish
between gray and black vertices.

22.2
Breadth-ﬁrst search
595
The breadth-ﬁrst-search procedure BFS below assumes that the input graph
G D .V; E/ is represented using adjacency lists. It attaches several additional
attributes to each vertex in the graph. We store the color of each vertex u 2 V
in the attribute u:color and the predecessor of u in the attribute u:. If u has no
predecessor (for example, if u D s or u has not been discovered), then u: D NIL.
The attribute u:d holds the distance from the source s to vertex u computed by the
algorithm. The algorithm also uses a ﬁrst-in, ﬁrst-out queue Q (see Section 10.1)
to manage the set of gray vertices.
BFS.G; s/
1
for each vertex u 2 G:V  fsg
2
u:color D WHITE
3
u:d D 1
4
u: D NIL
5
s:color D GRAY
6
s:d D 0
7
s: D NIL
8
Q D ;
9
ENQUEUE.Q; s/
10
while Q ¤ ;
11
u D DEQUEUE.Q/
12
for each  2 G:AdjŒu
13
if :color == WHITE
14
:color D GRAY
15
:d D u:d C 1
16
: D u
17
ENQUEUE.Q; /
18
u:color D BLACK
Figure 22.3 illustrates the progress of BFS on a sample graph.
The procedure BFS works as follows. With the exception of the source vertex s,
lines 1–4 paint every vertex white, set u:d to be inﬁnity for each vertex u, and set
the parent of every vertex to be NIL. Line 5 paints s gray, since we consider it to be
discovered as the procedure begins. Line 6 initializes s:d to 0, and line 7 sets the
predecessor of the source to be NIL. Lines 8–9 initialize Q to the queue containing
just the vertex s.
The while loop of lines 10–18 iterates as long as there remain gray vertices,
which are discovered vertices that have not yet had their adjacency lists fully ex-
amined. This while loop maintains the following invariant:
At the test in line 10, the queue Q consists of the set of gray vertices.

596
Chapter 22
Elementary Graph Algorithms
r
s
t
u
v
w
x
y
0
∞
∞
∞
∞
∞
∞
∞
s
0
Q
(a)
t
u
v
w
x
y
0
1
∞
∞
∞
∞
∞
1
w
1
Q
(b)
r
1
t
u
v
w
x
y
0
1
2
∞
∞
2
∞
1
Q
(c)
r
1
t
u
v
w
x
y
0
1
∞
∞
Q
(d)
(e)
(f)
(g)
(h)
Q
(i)
r
s
r
s
r
s
t
2
x
2
2
2
1
2
t
2
x
2
v
2
t
u
v
w
x
y
0
1
∞
Q
r
s
2
2
1
2
x
2
v
2
u
3
3
t
u
v
w
x
y
0
1
3
Q
r
s
2
2
1
2
v
2
u
3
3
y
3
t
u
v
w
x
y
0
1
3
Q
r
s
2
2
1
u
3
3
y
3
2
t
u
v
w
x
y
0
1
3
Q
r
s
2
2
1
3
y
3
2
t
u
v
w
x
y
0
1
r
s
2
2
1
3
2
3
;
Figure 22.3
The operation of BFS on an undirected graph. Tree edges are shown shaded as they
are produced by BFS. The value of u:d appears within each vertex u. The queue Q is shown at the
beginning of each iteration of the while loop of lines 10–18. Vertex distances appear below vertices
in the queue.
Although we won’t use this loop invariant to prove correctness, it is easy to see
that it holds prior to the ﬁrst iteration and that each iteration of the loop maintains
the invariant. Prior to the ﬁrst iteration, the only gray vertex, and the only vertex
in Q, is the source vertex s. Line 11 determines the gray vertex u at the head of
the queue Q and removes it from Q. The for loop of lines 12–17 considers each
vertex  in the adjacency list of u. If  is white, then it has not yet been discovered,
and the procedure discovers it by executing lines 14–17. The procedure paints
vertex  gray, sets its distance :d to u:dC1, records u as its parent :, and places
it at the tail of the queue Q. Once the procedure has examined all the vertices on u’s

22.2
Breadth-ﬁrst search
597
adjacency list, it blackens u in line 18. The loop invariant is maintained because
whenever a vertex is painted gray (in line 14) it is also enqueued (in line 17), and
whenever a vertex is dequeued (in line 11) it is also painted black (in line 18).
The results of breadth-ﬁrst search may depend upon the order in which the neigh-
bors of a given vertex are visited in line 12: the breadth-ﬁrst tree may vary, but the
distances d computed by the algorithm will not. (See Exercise 22.2-5.)
Analysis
Before proving the various properties of breadth-ﬁrst search, we take on the some-
what easier job of analyzing its running time on an input graph G D .V; E/. We
use aggregate analysis, as we saw in Section 17.1. After initialization, breadth-ﬁrst
search never whitens a vertex, and thus the test in line 13 ensures that each vertex
is enqueued at most once, and hence dequeued at most once. The operations of
enqueuing and dequeuing take O.1/ time, and so the total time devoted to queue
operations is O.V /. Because the procedure scans the adjacency list of each vertex
only when the vertex is dequeued, it scans each adjacency list at most once. Since
the sum of the lengths of all the adjacency lists is ‚.E/, the total time spent in
scanning adjacency lists is O.E/. The overhead for initialization is O.V /, and
thus the total running time of the BFS procedure is O.V C E/. Thus, breadth-ﬁrst
search runs in time linear in the size of the adjacency-list representation of G.
Shortest paths
At the beginning of this section, we claimed that breadth-ﬁrst search ﬁnds the dis-
tance to each reachable vertex in a graph G D .V; E/ from a given source vertex
s 2 V . Deﬁne the shortest-path distance ı.s; / from s to  as the minimum num-
ber of edges in any path from vertex s to vertex ; if there is no path from s to ,
then ı.s; / D 1. We call a path of length ı.s; / from s to  a shortest path2
from s to . Before showing that breadth-ﬁrst search correctly computes shortest-
path distances, we investigate an important property of shortest-path distances.
2In Chapters 24 and 25, we shall generalize our study of shortest paths to weighted graphs, in which
every edge has a real-valued weight and the weight of a path is the sum of the weights of its con-
stituent edges. The graphs considered in the present chapter are unweighted or, equivalently, all
edges have unit weight.

598
Chapter 22
Elementary Graph Algorithms
Lemma 22.1
Let G D .V; E/ be a directed or undirected graph, and let s 2 V be an arbitrary
vertex. Then, for any edge .u; / 2 E,
ı.s; /  ı.s; u/ C 1 :
Proof
If u is reachable from s, then so is . In this case, the shortest path from s
to  cannot be longer than the shortest path from s to u followed by the edge .u; /,
and thus the inequality holds. If u is not reachable from s, then ı.s; u/ D 1, and
the inequality holds.
We want to show that BFS properly computes :d D ı.s; / for each ver-
tex  2 V . We ﬁrst show that :d bounds ı.s; / from above.
Lemma 22.2
Let G D .V; E/ be a directed or undirected graph, and suppose that BFS is run
on G from a given source vertex s 2 V . Then upon termination, for each ver-
tex  2 V , the value :d computed by BFS satisﬁes :d  ı.s; /.
Proof
We use induction on the number of ENQUEUE operations. Our inductive
hypothesis is that :d  ı.s; / for all  2 V .
The basis of the induction is the situation immediately after enqueuing s in line 9
of BFS. The inductive hypothesis holds here, because s:d D 0 D ı.s; s/ and
:d D 1  ı.s; / for all  2 V  fsg.
For the inductive step, consider a white vertex  that is discovered during the
search from a vertex u. The inductive hypothesis implies that u:d  ı.s; u/. From
the assignment performed by line 15 and from Lemma 22.1, we obtain
:d
D
u:d C 1

ı.s; u/ C 1

ı.s; / :
Vertex  is then enqueued, and it is never enqueued again because it is also grayed
and the then clause of lines 14–17 is executed only for white vertices. Thus, the
value of :d never changes again, and the inductive hypothesis is maintained.
To prove that :d D ı.s; /, we must ﬁrst show more precisely how the queue Q
operates during the course of BFS. The next lemma shows that at all times, the
queue holds at most two distinct d values.

22.2
Breadth-ﬁrst search
599
Lemma 22.3
Suppose that during the execution of BFS on a graph G D .V; E/, the queue Q
contains the vertices h1; 2; : : : ; ri, where 1 is the head of Q and r is the tail.
Then, r:d  1:d C 1 and i:d  iC1:d for i D 1; 2; : : : ; r  1.
Proof
The proof is by induction on the number of queue operations. Initially,
when the queue contains only s, the lemma certainly holds.
For the inductive step, we must prove that the lemma holds after both dequeuing
and enqueuing a vertex. If the head 1 of the queue is dequeued, 2 becomes the
new head. (If the queue becomes empty, then the lemma holds vacuously.) By the
inductive hypothesis, 1:d  2:d. But then we have r:d  1:d C 1  2:d C 1,
and the remaining inequalities are unaffected. Thus, the lemma follows with 2 as
the head.
In order to understand what happens upon enqueuing a vertex, we need to ex-
amine the code more closely. When we enqueue a vertex  in line 17 of BFS, it
becomes rC1. At that time, we have already removed vertex u, whose adjacency
list is currently being scanned, from the queue Q, and by the inductive hypothesis,
the new head 1 has 1:d  u:d. Thus, rC1:d D :d D u:dC1  1:dC1. From
the inductive hypothesis, we also have r:d  u:d C 1, and so r:d  u:d C 1 D
:d D rC1:d, and the remaining inequalities are unaffected. Thus, the lemma
follows when  is enqueued.
The following corollary shows that the d values at the time that vertices are
enqueued are monotonically increasing over time.
Corollary 22.4
Suppose that vertices i and j are enqueued during the execution of BFS, and
that i is enqueued before j. Then i:d  j:d at the time that j is enqueued.
Proof
Immediate from Lemma 22.3 and the property that each vertex receives a
ﬁnite d value at most once during the course of BFS.
We can now prove that breadth-ﬁrst search correctly ﬁnds shortest-path dis-
tances.
Theorem 22.5 (Correctness of breadth-ﬁrst search)
Let G D .V; E/ be a directed or undirected graph, and suppose that BFS is run
on G from a given source vertex s 2 V . Then, during its execution, BFS discovers
every vertex  2 V that is reachable from the source s, and upon termination,
:d D ı.s; / for all  2 V . Moreover, for any vertex  ¤ s that is reachable

600
Chapter 22
Elementary Graph Algorithms
from s, one of the shortest paths from s to  is a shortest path from s to :
followed by the edge .:; /.
Proof
Assume, for the purpose of contradiction, that some vertex receives a d
value not equal to its shortest-path distance.
Let  be the vertex with min-
imum ı.s; / that receives such an incorrect d value; clearly 
¤ s.
By
Lemma 22.2, :d  ı.s; /, and thus we have that :d > ı.s; /. Vertex  must be
reachable from s, for if it is not, then ı.s; / D 1  :d. Let u be the vertex im-
mediately preceding  on a shortest path from s to , so that ı.s; / D ı.s; u/ C 1.
Because ı.s; u/ < ı.s; /, and because of how we chose , we have u:d D ı.s; u/.
Putting these properties together, we have
:d > ı.s; / D ı.s; u/ C 1 D u:d C 1 :
(22.1)
Now consider the time when BFS chooses to dequeue vertex u from Q in
line 11. At this time, vertex  is either white, gray, or black. We shall show
that in each of these cases, we derive a contradiction to inequality (22.1). If  is
white, then line 15 sets :d D u:d C 1, contradicting inequality (22.1). If  is
black, then it was already removed from the queue and, by Corollary 22.4, we have
:d  u:d, again contradicting inequality (22.1). If  is gray, then it was painted
gray upon dequeuing some vertex w, which was removed from Q earlier than u
and for which :d D w:d C 1. By Corollary 22.4, however, w:d  u:d, and so we
have :d D w:d C 1  u:d C 1, once again contradicting inequality (22.1).
Thus we conclude that :d D ı.s; / for all  2 V . All vertices  reachable
from s must be discovered, for otherwise they would have 1 D :d > ı.s; /. To
conclude the proof of the theorem, observe that if : D u, then :d D u:d C 1.
Thus, we can obtain a shortest path from s to  by taking a shortest path from s
to : and then traversing the edge .:; /.
Breadth-ﬁrst trees
The procedure BFS builds a breadth-ﬁrst tree as it searches the graph, as Fig-
ure 22.3 illustrates. The tree corresponds to the  attributes. More formally, for
a graph G D .V; E/ with source s, we deﬁne the predecessor subgraph of G as
G D .V; E/, where
V D f 2 V W : ¤ NILg [ fsg
and
E D f.:; / W  2 V  fsgg :
The predecessor subgraph G is a breadth-ﬁrst tree if V consists of the vertices
reachable from s and, for all  2 V, the subgraph G contains a unique simple

22.2
Breadth-ﬁrst search
601
path from s to  that is also a shortest path from s to  in G. A breadth-ﬁrst tree
is in fact a tree, since it is connected and jEj D jVj  1 (see Theorem B.2). We
call the edges in E tree edges.
The following lemma shows that the predecessor subgraph produced by the BFS
procedure is a breadth-ﬁrst tree.
Lemma 22.6
When applied to a directed or undirected graph G D .V; E/, procedure BFS con-
structs  so that the predecessor subgraph G D .V; E/ is a breadth-ﬁrst tree.
Proof
Line 16 of BFS sets : D u if and only if .u; / 2 E and ı.s; / < 1—
that is, if  is reachable from s—and thus V consists of the vertices in V reachable
from s. Since G forms a tree, by Theorem B.2, it contains a unique simple path
from s to each vertex in V. By applying Theorem 22.5 inductively, we conclude
that every such path is a shortest path in G.
The following procedure prints out the vertices on a shortest path from s to ,
assuming that BFS has already computed a breadth-ﬁrst tree:
PRINT-PATH.G; s; /
1
if  == s
2
print s
3
elseif : == NIL
4
print “no path from” s “to”  “exists”
5
else PRINT-PATH.G; s; :/
6
print 
This procedure runs in time linear in the number of vertices in the path printed,
since each recursive call is for a path one vertex shorter.
Exercises
22.2-1
Show the d and  values that result from running breadth-ﬁrst search on the di-
rected graph of Figure 22.2(a), using vertex 3 as the source.
22.2-2
Show the d and  values that result from running breadth-ﬁrst search on the undi-
rected graph of Figure 22.3, using vertex u as the source.

602
Chapter 22
Elementary Graph Algorithms
22.2-3
Show that using a single bit to store each vertex color sufﬁces by arguing that the
BFS procedure would produce the same result if lines 5 and 14 were removed.
22.2-4
What is the running time of BFS if we represent its input graph by an adjacency
matrix and modify the algorithm to handle this form of input?
22.2-5
Argue that in a breadth-ﬁrst search, the value u:d assigned to a vertex u is inde-
pendent of the order in which the vertices appear in each adjacency list. Using
Figure 22.3 as an example, show that the breadth-ﬁrst tree computed by BFS can
depend on the ordering within adjacency lists.
22.2-6
Give an example of a directed graph G D .V; E/, a source vertex s 2 V , and a
set of tree edges E  E such that for each vertex  2 V , the unique simple path
in the graph .V; E/ from s to  is a shortest path in G, yet the set of edges E
cannot be produced by running BFS on G, no matter how the vertices are ordered
in each adjacency list.
22.2-7
There are two types of professional wrestlers: “babyfaces” (“good guys”) and
“heels” (“bad guys”). Between any pair of professional wrestlers, there may or
may not be a rivalry. Suppose we have n professional wrestlers and we have a list
of r pairs of wrestlers for which there are rivalries. Give an O.n C r/-time algo-
rithm that determines whether it is possible to designate some of the wrestlers as
babyfaces and the remainder as heels such that each rivalry is between a babyface
and a heel. If it is possible to perform such a designation, your algorithm should
produce it.
22.2-8
?
The diameter of a tree T D .V; E/ is deﬁned as maxu;2V ı.u; /, that is, the
largest of all shortest-path distances in the tree. Give an efﬁcient algorithm to
compute the diameter of a tree, and analyze the running time of your algorithm.
22.2-9
Let G D .V; E/ be a connected, undirected graph. Give an O.V C E/-time algo-
rithm to compute a path in G that traverses each edge in E exactly once in each
direction. Describe how you can ﬁnd your way out of a maze if you are given a
large supply of pennies.

22.3
Depth-ﬁrst search
603
22.3
Depth-ﬁrst search
The strategy followed by depth-ﬁrst search is, as its name implies, to search
“deeper” in the graph whenever possible. Depth-ﬁrst search explores edges out
of the most recently discovered vertex  that still has unexplored edges leaving it.
Once all of ’s edges have been explored, the search “backtracks” to explore edges
leaving the vertex from which  was discovered. This process continues until we
have discovered all the vertices that are reachable from the original source vertex.
If any undiscovered vertices remain, then depth-ﬁrst search selects one of them as
a new source, and it repeats the search from that source. The algorithm repeats this
entire process until it has discovered every vertex.3
As in breadth-ﬁrst search, whenever depth-ﬁrst search discovers a vertex  dur-
ing a scan of the adjacency list of an already discovered vertex u, it records this
event by setting ’s predecessor attribute : to u. Unlike breadth-ﬁrst search,
whose predecessor subgraph forms a tree, the predecessor subgraph produced by
a depth-ﬁrst search may be composed of several trees, because the search may
repeat from multiple sources. Therefore, we deﬁne the predecessor subgraph of
a depth-ﬁrst search slightly differently from that of a breadth-ﬁrst search: we let
G D .V; E/, where
E D f.:; / W  2 V and : ¤ NILg :
The predecessor subgraph of a depth-ﬁrst search forms a depth-ﬁrst forest com-
prising several depth-ﬁrst trees. The edges in E are tree edges.
As in breadth-ﬁrst search, depth-ﬁrst search colors vertices during the search to
indicate their state. Each vertex is initially white, is grayed when it is discovered
in the search, and is blackened when it is ﬁnished, that is, when its adjacency list
has been examined completely. This technique guarantees that each vertex ends up
in exactly one depth-ﬁrst tree, so that these trees are disjoint.
Besides creating a depth-ﬁrst forest, depth-ﬁrst search also timestamps each ver-
tex. Each vertex  has two timestamps: the ﬁrst timestamp :d records when 
is ﬁrst discovered (and grayed), and the second timestamp :f records when the
search ﬁnishes examining ’s adjacency list (and blackens ). These timestamps
3It may seem arbitrary that breadth-ﬁrst search is limited to only one source whereas depth-ﬁrst
search may search from multiple sources. Although conceptually, breadth-ﬁrst search could proceed
from multiple sources and depth-ﬁrst search could be limited to one source, our approach reﬂects how
the results of these searches are typically used. Breadth-ﬁrst search usually serves to ﬁnd shortest-
path distances (and the associated predecessor subgraph) from a given source. Depth-ﬁrst search is
often a subroutine in another algorithm, as we shall see later in this chapter.

604
Chapter 22
Elementary Graph Algorithms
provide important information about the structure of the graph and are generally
helpful in reasoning about the behavior of depth-ﬁrst search.
The procedure DFS below records when it discovers vertex u in the attribute u:d
and when it ﬁnishes vertex u in the attribute u:f. These timestamps are integers
between 1 and 2 jV j, since there is one discovery event and one ﬁnishing event for
each of the jV j vertices. For every vertex u,
u:d < u:f :
(22.2)
Vertex u is WHITE before time u:d, GRAY between time u:d and time u:f, and
BLACK thereafter.
The following pseudocode is the basic depth-ﬁrst-search algorithm. The input
graph G may be undirected or directed. The variable time is a global variable that
we use for timestamping.
DFS.G/
1
for each vertex u 2 G:V
2
u:color D WHITE
3
u: D NIL
4
time D 0
5
for each vertex u 2 G:V
6
if u:color == WHITE
7
DFS-VISIT.G; u/
DFS-VISIT.G; u/
1
time D time C 1
// white vertex u has just been discovered
2
u:d D time
3
u:color D GRAY
4
for each  2 G:AdjŒu
// explore edge .u; /
5
if :color == WHITE
6
: D u
7
DFS-VISIT.G; /
8
u:color D BLACK
// blacken u; it is ﬁnished
9
time D time C 1
10
u:f D time
Figure 22.4 illustrates the progress of DFS on the graph shown in Figure 22.2.
Procedure DFS works as follows. Lines 1–3 paint all vertices white and ini-
tialize their  attributes to NIL. Line 4 resets the global time counter. Lines 5–7
check each vertex in V in turn and, when a white vertex is found, visit it using
DFS-VISIT. Every time DFS-VISIT.G; u/ is called in line 7, vertex u becomes

22.3
Depth-ﬁrst search
605
u
v
w
x
y
z
1/
1/
2/
1/
2/
3/
1/
2/
3/
4/
1/
2/
3/
4/
B
1/
2/
3/
B
4/5
1/
2/
B
4/5
3/6
1/
B
4/5
3/6
2/7
1/
B
4/5
3/6
2/7
F
B
4/5
3/6
2/7
F
1/8
B
4/5
3/6
2/7
F
1/8
9/
B
4/5
3/6
2/7
F
1/8
9/
C
B
4/5
3/6
2/7
F
1/8
9/
C
B
4/5
3/6
2/7
F
1/8
9/
C
B
B
4/5
3/6
2/7
F
1/8
9/
C
B
10/11
B
4/5
3/6
2/7
F
1/8
C
B
10/11
9/12
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
u
v
w
x
y
z
(m)
(n)
(o)
(p)
(i)
(j)
(k)
(l)
(e)
(f)
(g)
(h)
(a)
(b)
(c)
(d)
10/
10/
Figure 22.4
The progress of the depth-ﬁrst-search algorithm DFS on a directed graph. As edges
are explored by the algorithm, they are shown as either shaded (if they are tree edges) or dashed
(otherwise). Nontree edges are labeled B, C, or F according to whether they are back, cross, or
forward edges. Timestamps within vertices indicate discovery time/ﬁnishing times.
the root of a new tree in the depth-ﬁrst forest. When DFS returns, every vertex u
has been assigned a discovery time u:d and a ﬁnishing time u:f.
In each call DFS-VISIT.G; u/, vertex u is initially white. Line 1 increments
the global variable time, line 2 records the new value of time as the discovery
time u:d, and line 3 paints u gray. Lines 4–7 examine each vertex  adjacent to u
and recursively visit  if it is white. As each vertex  2 AdjŒu is considered in
line 4, we say that edge .u; / is explored by the depth-ﬁrst search. Finally, after
every edge leaving u has been explored, lines 8–10 paint u black, increment time,
and record the ﬁnishing time in u:f.
Note that the results of depth-ﬁrst search may depend upon the order in which
line 5 of DFS examines the vertices and upon the order in which line 4 of DFS-
VISIT visits the neighbors of a vertex. These different visitation orders tend not

606
Chapter 22
Elementary Graph Algorithms
to cause problems in practice, as we can usually use any depth-ﬁrst search result
effectively, with essentially equivalent results.
What is the running time of DFS? The loops on lines 1–3 and lines 5–7 of DFS
take time ‚.V /, exclusive of the time to execute the calls to DFS-VISIT. As we did
for breadth-ﬁrst search, we use aggregate analysis. The procedure DFS-VISIT is
called exactly once for each vertex  2 V , since the vertex u on which DFS-VISIT
is invoked must be white and the ﬁrst thing DFS-VISIT does is paint vertex u gray.
During an execution of DFS-VISIT.G; /, the loop on lines 4–7 executes jAdjŒj
times. Since
X
2V
jAdjŒj D ‚.E/ ;
the total cost of executing lines 4–7 of DFS-VISIT is ‚.E/. The running time of
DFS is therefore ‚.V C E/.
Properties of depth-ﬁrst search
Depth-ﬁrst search yields valuable information about the structure of a graph. Per-
haps the most basic property of depth-ﬁrst search is that the predecessor sub-
graph G does indeed form a forest of trees, since the structure of the depth-
ﬁrst trees exactly mirrors the structure of recursive calls of DFS-VISIT. That is,
u D : if and only if DFS-VISIT.G; / was called during a search of u’s ad-
jacency list. Additionally, vertex  is a descendant of vertex u in the depth-ﬁrst
forest if and only if  is discovered during the time in which u is gray.
Another important property of depth-ﬁrst search is that discovery and ﬁnishing
times have parenthesis structure. If we represent the discovery of vertex u with
a left parenthesis “.u” and represent its ﬁnishing by a right parenthesis “u/”, then
the history of discoveries and ﬁnishings makes a well-formed expression in the
sense that the parentheses are properly nested. For example, the depth-ﬁrst search
of Figure 22.5(a) corresponds to the parenthesization shown in Figure 22.5(b). The
following theorem provides another way to characterize the parenthesis structure.
Theorem 22.7 (Parenthesis theorem)
In any depth-ﬁrst search of a (directed or undirected) graph G D .V; E/, for any
two vertices u and , exactly one of the following three conditions holds:

the intervals Œu:d; u:f and Œ:d; :f are entirely disjoint, and neither u nor 
is a descendant of the other in the depth-ﬁrst forest,

the interval Œu:d; u:f is contained entirely within the interval Œ:d; :f, and u
is a descendant of  in a depth-ﬁrst tree, or

the interval Œ:d; :f is contained entirely within the interval Œu:d; u:f, and 
is a descendant of u in a depth-ﬁrst tree.

22.3
Depth-ﬁrst search
607
3/6
2/9
1/10
11/16
14/15
12/13
7/8
4/5
y
z
s
t
u
v
w
x
B
C
F
C
C
C
B
1
2
3
4
5
6
7
8
9 10 11 12 13 14 15 16
s
t
z
y
w
x
v
u
s
z
y
w
x
t
v
u
C
F
B
C
C
B
C
(a)
(b)
(c)
(s (z (y (x
x) y) (w w) z) s) (t
(v v) (u u)
t)
Figure 22.5
Properties of depth-ﬁrst search. (a) The result of a depth-ﬁrst search of a directed
graph. Vertices are timestamped and edge types are indicated as in Figure 22.4. (b) Intervals for
the discovery time and ﬁnishing time of each vertex correspond to the parenthesization shown. Each
rectangle spans the interval given by the discovery and ﬁnishing times of the corresponding vertex.
Only tree edges are shown. If two intervals overlap, then one is nested within the other, and the
vertex corresponding to the smaller interval is a descendant of the vertex corresponding to the larger.
(c) The graph of part (a) redrawn with all tree and forward edges going down within a depth-ﬁrst tree
and all back edges going up from a descendant to an ancestor.

608
Chapter 22
Elementary Graph Algorithms
Proof
We begin with the case in which u:d < :d. We consider two subcases,
according to whether :d < u:f or not. The ﬁrst subcase occurs when :d < u:f,
so  was discovered while u was still gray, which implies that  is a descendant
of u. Moreover, since  was discovered more recently than u, all of its outgo-
ing edges are explored, and  is ﬁnished, before the search returns to and ﬁn-
ishes u. In this case, therefore, the interval Œ:d; :f is entirely contained within
the interval Œu:d; u:f. In the other subcase, u:f < :d, and by inequality (22.2),
u:d < u:f < :d < :f; thus the intervals Œu:d; u:f and Œ:d; :f are disjoint.
Because the intervals are disjoint, neither vertex was discovered while the other
was gray, and so neither vertex is a descendant of the other.
The case in which :d < u:d is similar, with the roles of u and  reversed in the
above argument.
Corollary 22.8 (Nesting of descendants’ intervals)
Vertex  is a proper descendant of vertex u in the depth-ﬁrst forest for a (directed
or undirected) graph G if and only if u:d < :d < :f < u:f.
Proof
Immediate from Theorem 22.7.
The next theorem gives another important characterization of when one vertex
is a descendant of another in the depth-ﬁrst forest.
Theorem 22.9 (White-path theorem)
In a depth-ﬁrst forest of a (directed or undirected) graph G D .V; E/, vertex  is
a descendant of vertex u if and only if at the time u:d that the search discovers u,
there is a path from u to  consisting entirely of white vertices.
Proof
): If  D u, then the path from u to  contains just vertex u, which is still
white when we set the value of u:d. Now, suppose that  is a proper descendant
of u in the depth-ﬁrst forest. By Corollary 22.8, u:d < :d, and so  is white at
time u:d. Since  can be any descendant of u, all vertices on the unique simple
path from u to  in the depth-ﬁrst forest are white at time u:d.
(: Suppose that there is a path of white vertices from u to  at time u:d, but 
does not become a descendant of u in the depth-ﬁrst tree. Without loss of general-
ity, assume that every vertex other than  along the path becomes a descendant of u.
(Otherwise, let  be the closest vertex to u along the path that doesn’t become a de-
scendant of u.) Let w be the predecessor of  in the path, so that w is a descendant
of u (w and u may in fact be the same vertex). By Corollary 22.8, w:f  u:f. Be-
cause  must be discovered after u is discovered, but before w is ﬁnished, we have
u:d < :d < w:f  u:f. Theorem 22.7 then implies that the interval Œ:d; :f

22.3
Depth-ﬁrst search
609
is contained entirely within the interval Œu:d; u:f. By Corollary 22.8,  must after
all be a descendant of u.
Classiﬁcation of edges
Another interesting property of depth-ﬁrst search is that the search can be used
to classify the edges of the input graph G D .V; E/. The type of each edge can
provide important information about a graph. For example, in the next section, we
shall see that a directed graph is acyclic if and only if a depth-ﬁrst search yields no
“back” edges (Lemma 22.11).
We can deﬁne four edge types in terms of the depth-ﬁrst forest G produced by
a depth-ﬁrst search on G:
1. Tree edges are edges in the depth-ﬁrst forest G. Edge .u; / is a tree edge if 
was ﬁrst discovered by exploring edge .u; /.
2. Back edges are those edges .u; / connecting a vertex u to an ancestor  in a
depth-ﬁrst tree. We consider self-loops, which may occur in directed graphs, to
be back edges.
3. Forward edges are those nontree edges .u; / connecting a vertex u to a de-
scendant  in a depth-ﬁrst tree.
4. Cross edges are all other edges. They can go between vertices in the same
depth-ﬁrst tree, as long as one vertex is not an ancestor of the other, or they can
go between vertices in different depth-ﬁrst trees.
In Figures 22.4 and 22.5, edge labels indicate edge types. Figure 22.5(c) also shows
how to redraw the graph of Figure 22.5(a) so that all tree and forward edges head
downward in a depth-ﬁrst tree and all back edges go up. We can redraw any graph
in this fashion.
The DFS algorithm has enough information to classify some edges as it encoun-
ters them. The key idea is that when we ﬁrst explore an edge .u; /, the color of
vertex  tells us something about the edge:
1.
WHITE indicates a tree edge,
2.
GRAY indicates a back edge, and
3.
BLACK indicates a forward or cross edge.
The ﬁrst case is immediate from the speciﬁcation of the algorithm. For the sec-
ond case, observe that the gray vertices always form a linear chain of descendants
corresponding to the stack of active DFS-VISIT invocations; the number of gray
vertices is one more than the depth in the depth-ﬁrst forest of the vertex most re-
cently discovered. Exploration always proceeds from the deepest gray vertex, so

610
Chapter 22
Elementary Graph Algorithms
an edge that reaches another gray vertex has reached an ancestor. The third case
handles the remaining possibility; Exercise 22.3-5 asks you to show that such an
edge .u; / is a forward edge if u:d < :d and a cross edge if u:d > :d.
An undirected graph may entail some ambiguity in how we classify edges,
since .u; / and .; u/ are really the same edge. In such a case, we classify the
edge as the ﬁrst type in the classiﬁcation list that applies. Equivalently (see Ex-
ercise 22.3-6), we classify the edge according to whichever of .u; / or .; u/ the
search encounters ﬁrst.
We now show that forward and cross edges never occur in a depth-ﬁrst search of
an undirected graph.
Theorem 22.10
In a depth-ﬁrst search of an undirected graph G, every edge of G is either a tree
edge or a back edge.
Proof
Let .u; / be an arbitrary edge of G, and suppose without loss of generality
that u:d < :d. Then the search must discover and ﬁnish  before it ﬁnishes u
(while u is gray), since  is on u’s adjacency list. If the ﬁrst time that the search
explores edge .u; /, it is in the direction from u to , then  is undiscovered
(white) until that time, for otherwise the search would have explored this edge
already in the direction from  to u. Thus, .u; / becomes a tree edge. If the
search explores .u; / ﬁrst in the direction from  to u, then .u; / is a back edge,
since u is still gray at the time the edge is ﬁrst explored.
We shall see several applications of these theorems in the following sections.
Exercises
22.3-1
Make a 3-by-3 chart with row and column labels WHITE, GRAY, and BLACK. In
each cell .i; j /, indicate whether, at any point during a depth-ﬁrst search of a di-
rected graph, there can be an edge from a vertex of color i to a vertex of color j .
For each possible edge, indicate what edge types it can be. Make a second such
chart for depth-ﬁrst search of an undirected graph.
22.3-2
Show how depth-ﬁrst search works on the graph of Figure 22.6. Assume that the
for loop of lines 5–7 of the DFS procedure considers the vertices in alphabetical
order, and assume that each adjacency list is ordered alphabetically. Show the
discovery and ﬁnishing times for each vertex, and show the classiﬁcation of each
edge.

22.3
Depth-ﬁrst search
611
q
r
s
t
u
v
w
x
y
z
Figure 22.6
A directed graph for use in Exercises 22.3-2 and 22.5-2.
22.3-3
Show the parenthesis structure of the depth-ﬁrst search of Figure 22.4.
22.3-4
Show that using a single bit to store each vertex color sufﬁces by arguing that
the DFS procedure would produce the same result if line 3 of DFS-VISIT was
removed.
22.3-5
Show that edge .u; / is
a. a tree edge or forward edge if and only if u:d < :d < :f < u:f,
b. a back edge if and only if :d  u:d < u:f  :f, and
c. a cross edge if and only if :d < :f < u:d < u:f.
22.3-6
Show that in an undirected graph, classifying an edge .u; / as a tree edge or a back
edge according to whether .u; / or .; u/ is encountered ﬁrst during the depth-ﬁrst
search is equivalent to classifying it according to the ordering of the four types in
the classiﬁcation scheme.
22.3-7
Rewrite the procedure DFS, using a stack to eliminate recursion.
22.3-8
Give a counterexample to the conjecture that if a directed graph G contains a path
from u to , and if u:d < :d in a depth-ﬁrst search of G, then  is a descendant
of u in the depth-ﬁrst forest produced.

612
Chapter 22
Elementary Graph Algorithms
22.3-9
Give a counterexample to the conjecture that if a directed graph G contains a path
from u to , then any depth-ﬁrst search must result in :d  u:f.
22.3-10
Modify the pseudocode for depth-ﬁrst search so that it prints out every edge in the
directed graph G, together with its type. Show what modiﬁcations, if any, you need
to make if G is undirected.
22.3-11
Explain how a vertex u of a directed graph can end up in a depth-ﬁrst tree contain-
ing only u, even though u has both incoming and outgoing edges in G.
22.3-12
Show that we can use a depth-ﬁrst search of an undirected graph G to identify the
connected components of G, and that the depth-ﬁrst forest contains as many trees
as G has connected components. More precisely, show how to modify depth-ﬁrst
search so that it assigns to each vertex  an integer label :cc between 1 and k,
where k is the number of connected components of G, such that u:cc D :cc if
and only if u and  are in the same connected component.
22.3-13
?
A directed graph G D .V; E/ is singly connected if u ;  implies that G contains
at most one simple path from u to  for all vertices u;  2 V . Give an efﬁcient
algorithm to determine whether or not a directed graph is singly connected.
22.4
Topological sort
This section shows how we can use depth-ﬁrst search to perform a topological sort
of a directed acyclic graph, or a “dag” as it is sometimes called. A topological sort
of a dag G D .V; E/ is a linear ordering of all its vertices such that if G contains an
edge .u; /, then u appears before  in the ordering. (If the graph contains a cycle,
then no linear ordering is possible.) We can view a topological sort of a graph as
an ordering of its vertices along a horizontal line so that all directed edges go from
left to right. Topological sorting is thus different from the usual kind of “sorting”
studied in Part II.
Many applications use directed acyclic graphs to indicate precedences among
events. Figure 22.7 gives an example that arises when Professor Bumstead gets
dressed in the morning. The professor must don certain garments before others
(e.g., socks before shoes). Other items may be put on in any order (e.g., socks and

22.4
Topological sort
613
11/16
12/15
6/7
1/8
2/5
3/4
17/18
13/14
9/10
17/18
11/16
12/15
13/14
9/10
1/8
6/7
2/5
3/4
(a)
(b)
undershorts
pants
belt
shirt
tie
jacket
socks
shoes
watch
socks
undershorts
pants
shoes
watch
shirt
belt
tie
jacket
Figure 22.7
(a) Professor Bumstead topologically sorts his clothing when getting dressed. Each
directed edge .u; / means that garment u must be put on before garment . The discovery and
ﬁnishing times from a depth-ﬁrst search are shown next to each vertex. (b) The same graph shown
topologically sorted, with its vertices arranged from left to right in order of decreasing ﬁnishing time.
All directed edges go from left to right.
pants). A directed edge .u; / in the dag of Figure 22.7(a) indicates that garment u
must be donned before garment . A topological sort of this dag therefore gives an
order for getting dressed. Figure 22.7(b) shows the topologically sorted dag as an
ordering of vertices along a horizontal line such that all directed edges go from left
to right.
The following simple algorithm topologically sorts a dag:
TOPOLOGICAL-SORT.G/
1
call DFS.G/ to compute ﬁnishing times :f for each vertex 
2
as each vertex is ﬁnished, insert it onto the front of a linked list
3
return the linked list of vertices
Figure 22.7(b) shows how the topologically sorted vertices appear in reverse order
of their ﬁnishing times.
We can perform a topological sort in time ‚.V C E/, since depth-ﬁrst search
takes ‚.V C E/ time and it takes O.1/ time to insert each of the jV j vertices onto
the front of the linked list.
We prove the correctness of this algorithm using the following key lemma char-
acterizing directed acyclic graphs.

614
Chapter 22
Elementary Graph Algorithms
Lemma 22.11
A directed graph G is acyclic if and only if a depth-ﬁrst search of G yields no back
edges.
Proof
): Suppose that a depth-ﬁrst search produces a back edge .u; /. Then
vertex  is an ancestor of vertex u in the depth-ﬁrst forest. Thus, G contains a path
from  to u, and the back edge .u; / completes a cycle.
(: Suppose that G contains a cycle c. We show that a depth-ﬁrst search of G
yields a back edge. Let  be the ﬁrst vertex to be discovered in c, and let .u; / be
the preceding edge in c. At time :d, the vertices of c form a path of white vertices
from  to u. By the white-path theorem, vertex u becomes a descendant of  in the
depth-ﬁrst forest. Therefore, .u; / is a back edge.
Theorem 22.12
TOPOLOGICAL-SORT produces a topological sort of the directed acyclic graph
provided as its input.
Proof
Suppose that DFS is run on a given dag G D .V; E/ to determine ﬁn-
ishing times for its vertices. It sufﬁces to show that for any pair of distinct ver-
tices u;  2 V , if G contains an edge from u to , then :f < u:f. Consider any
edge .u; / explored by DFS.G/. When this edge is explored,  cannot be gray,
since then  would be an ancestor of u and .u; / would be a back edge, contra-
dicting Lemma 22.11. Therefore,  must be either white or black. If  is white,
it becomes a descendant of u, and so :f < u:f. If  is black, it has already been
ﬁnished, so that :f has already been set. Because we are still exploring from u, we
have yet to assign a timestamp to u:f, and so once we do, we will have :f < u:f
as well. Thus, for any edge .u; / in the dag, we have :f < u:f, proving the
theorem.
Exercises
22.4-1
Show the ordering of vertices produced by TOPOLOGICAL-SORT when it is run on
the dag of Figure 22.8, under the assumption of Exercise 22.3-2.
22.4-2
Give a linear-time algorithm that takes as input a directed acyclic graph G D
.V; E/ and two vertices s and t, and returns the number of simple paths from s
to t in G. For example, the directed acyclic graph of Figure 22.8 contains exactly
four simple paths from vertex p to vertex : po, pory, posry, and psry.
(Your algorithm needs only to count the simple paths, not list them.)

22.5
Strongly connected components
615
z
y
x
w
v
u
t
s
r
q
p
o
n
m
Figure 22.8
A dag for topological sorting.
22.4-3
Give an algorithm that determines whether or not a given undirected graph G D
.V; E/ contains a cycle. Your algorithm should run in O.V / time, independent
of jEj.
22.4-4
Prove or disprove: If a directed graph G contains cycles, then TOPOLOGICAL-
SORT.G/ produces a vertex ordering that minimizes the number of “bad” edges
that are inconsistent with the ordering produced.
22.4-5
Another way to perform topological sorting on a directed acyclic graph G D
.V; E/ is to repeatedly ﬁnd a vertex of in-degree 0, output it, and remove it and
all of its outgoing edges from the graph. Explain how to implement this idea so
that it runs in time O.V C E/. What happens to this algorithm if G has cycles?
22.5
Strongly connected components
We now consider a classic application of depth-ﬁrst search: decomposing a di-
rected graph into its strongly connected components. This section shows how to do
so using two depth-ﬁrst searches. Many algorithms that work with directed graphs
begin with such a decomposition. After decomposing the graph into strongly con-
nected components, such algorithms run separately on each one and then combine
the solutions according to the structure of connections among components.
Recall from Appendix B that a strongly connected component of a directed
graph G D .V; E/ is a maximal set of vertices C  V such that for every pair
of vertices u and  in C, we have both u ;  and  ; u; that is, vertices u and 
are reachable from each other. Figure 22.9 shows an example.

616
Chapter 22
Elementary Graph Algorithms
13/14
11/16
12/15
3/4
1/10
2/7
8/9
5/6
a
b
c
d
e
f
g
h
a
b
c
d
e
f
g
h
abe
cd
fg
h
(c)
(b)
(a)
Figure 22.9
(a) A directed graph G. Each shaded region is a strongly connected component of G.
Each vertex is labeled with its discovery and ﬁnishing times in a depth-ﬁrst search, and tree edges
are shaded. (b) The graph GT, the transpose of G, with the depth-ﬁrst forest computed in line 3
of STRONGLY-CONNECTED-COMPONENTS shown and tree edges shaded. Each strongly connected
component corresponds to one depth-ﬁrst tree. Vertices b, c, g, and h, which are heavily shaded, are
the roots of the depth-ﬁrst trees produced by the depth-ﬁrst search of GT. (c) The acyclic component
graph GSCC obtained by contracting all edges within each strongly connected component of G so
that only a single vertex remains in each component.
Our algorithm for ﬁnding strongly connected components of a graph G D
.V; E/ uses the transpose of G, which we deﬁned in Exercise 22.1-3 to be the
graph GT D .V; ET/, where ET D f.u; / W .; u/ 2 Eg. That is, ET consists of
the edges of G with their directions reversed. Given an adjacency-list representa-
tion of G, the time to create GT is O.V C E/. It is interesting to observe that G
and GT have exactly the same strongly connected components: u and  are reach-
able from each other in G if and only if they are reachable from each other in GT.
Figure 22.9(b) shows the transpose of the graph in Figure 22.9(a), with the strongly
connected components shaded.

22.5
Strongly connected components
617
The following linear-time (i.e., ‚.V CE/-time) algorithm computes the strongly
connected components of a directed graph G D .V; E/ using two depth-ﬁrst
searches, one on G and one on GT.
STRONGLY-CONNECTED-COMPONENTS.G/
1
call DFS.G/ to compute ﬁnishing times u:f for each vertex u
2
compute GT
3
call DFS.GT/, but in the main loop of DFS, consider the vertices
in order of decreasing u:f (as computed in line 1)
4
output the vertices of each tree in the depth-ﬁrst forest formed in line 3 as a
separate strongly connected component
The idea behind this algorithm comes from a key property of the component
graph GSCC D .V SCC; ESCC/, which we deﬁne as follows.
Suppose that G
has strongly connected components C1; C2; : : : ; Ck.
The vertex set V SCC is
f1; 2; : : : ; kg, and it contains a vertex i for each strongly connected compo-
nent Ci of G. There is an edge .i; j/ 2 ESCC if G contains a directed edge .x; y/
for some x 2 Ci and some y 2 Cj. Looked at another way, by contracting all
edges whose incident vertices are within the same strongly connected component
of G, the resulting graph is GSCC. Figure 22.9(c) shows the component graph of
the graph in Figure 22.9(a).
The key property is that the component graph is a dag, which the following
lemma implies.
Lemma 22.13
Let C and C 0 be distinct strongly connected components in directed graph G D
.V; E/, let u;  2 C, let u0; 0 2 C 0, and suppose that G contains a path u ; u0.
Then G cannot also contain a path 0 ; .
Proof
If G contains a path 0 ; , then it contains paths u ; u0 ; 0 and
0 ;  ; u. Thus, u and 0 are reachable from each other, thereby contradicting
the assumption that C and C 0 are distinct strongly connected components.
We shall see that by considering vertices in the second depth-ﬁrst search in de-
creasing order of the ﬁnishing times that were computed in the ﬁrst depth-ﬁrst
search, we are, in essence, visiting the vertices of the component graph (each of
which corresponds to a strongly connected component of G) in topologically sorted
order.
Because the STRONGLY-CONNECTED-COMPONENTS procedure performs two
depth-ﬁrst searches, there is the potential for ambiguity when we discuss u:d
or u:f. In this section, these values always refer to the discovery and ﬁnishing
times as computed by the ﬁrst call of DFS, in line 1.

618
Chapter 22
Elementary Graph Algorithms
We extend the notation for discovery and ﬁnishing times to sets of vertices.
If U  V , then we deﬁne d.U / D minu2U fu:dg and f .U / D maxu2U fu:fg.
That is, d.U / and f .U / are the earliest discovery time and latest ﬁnishing time,
respectively, of any vertex in U .
The following lemma and its corollary give a key property relating strongly con-
nected components and ﬁnishing times in the ﬁrst depth-ﬁrst search.
Lemma 22.14
Let C and C 0 be distinct strongly connected components in directed graph G D
.V; E/. Suppose that there is an edge .u; / 2 E, where u 2 C and  2 C 0. Then
f .C/ > f .C 0/.
Proof
We consider two cases, depending on which strongly connected compo-
nent, C or C 0, had the ﬁrst discovered vertex during the depth-ﬁrst search.
If d.C/ < d.C 0/, let x be the ﬁrst vertex discovered in C. At time x:d, all ver-
tices in C and C 0 are white. At that time, G contains a path from x to each vertex
in C consisting only of white vertices. Because .u; / 2 E, for any vertex w 2 C 0,
there is also a path in G at time x:d from x to w consisting only of white vertices:
x ; u !  ; w. By the white-path theorem, all vertices in C and C 0 become
descendants of x in the depth-ﬁrst tree. By Corollary 22.8, x has the latest ﬁnishing
time of any of its descendants, and so x:f D f .C/ > f .C 0/.
If instead we have d.C/ > d.C 0/, let y be the ﬁrst vertex discovered in C 0.
At time y:d, all vertices in C 0 are white and G contains a path from y to each
vertex in C 0 consisting only of white vertices. By the white-path theorem, all ver-
tices in C 0 become descendants of y in the depth-ﬁrst tree, and by Corollary 22.8,
y:f D f .C 0/. At time y:d, all vertices in C are white. Since there is an edge .u; /
from C to C 0, Lemma 22.13 implies that there cannot be a path from C 0 to C.
Hence, no vertex in C is reachable from y. At time y:f, therefore, all vertices in C
are still white. Thus, for any vertex w 2 C, we have w:f > y:f, which implies
that f .C/ > f .C 0/.
The following corollary tells us that each edge in GT that goes between different
strongly connected components goes from a component with an earlier ﬁnishing
time (in the ﬁrst depth-ﬁrst search) to a component with a later ﬁnishing time.
Corollary 22.15
Let C and C 0 be distinct strongly connected components in directed graph G D
.V; E/. Suppose that there is an edge .u; / 2 ET, where u 2 C and  2 C 0. Then
f .C/ < f .C 0/.

22.5
Strongly connected components
619
Proof
Since .u; / 2 ET, we have .; u/ 2 E.
Because the strongly con-
nected components of G and GT are the same, Lemma 22.14 implies that
f .C/ < f .C 0/.
Corollary 22.15 provides the key to understanding why the strongly connected
components algorithm works. Let us examine what happens when we perform the
second depth-ﬁrst search, which is on GT. We start with the strongly connected
component C whose ﬁnishing time f .C/ is maximum. The search starts from
some vertex x 2 C, and it visits all vertices in C. By Corollary 22.15, GT contains
no edges from C to any other strongly connected component, and so the search
from x will not visit vertices in any other component. Thus, the tree rooted at x
contains exactly the vertices of C. Having completed visiting all vertices in C,
the search in line 3 selects as a root a vertex from some other strongly connected
component C 0 whose ﬁnishing time f .C 0/ is maximum over all components other
than C. Again, the search will visit all vertices in C 0, but by Corollary 22.15,
the only edges in GT from C 0 to any other component must be to C, which we
have already visited. In general, when the depth-ﬁrst search of GT in line 3 visits
any strongly connected component, any edges out of that component must be to
components that the search already visited. Each depth-ﬁrst tree, therefore, will be
exactly one strongly connected component. The following theorem formalizes this
argument.
Theorem 22.16
The STRONGLY-CONNECTED-COMPONENTS procedure correctly computes the
strongly connected components of the directed graph G provided as its input.
Proof
We argue by induction on the number of depth-ﬁrst trees found in the
depth-ﬁrst search of GT in line 3 that the vertices of each tree form a strongly
connected component. The inductive hypothesis is that the ﬁrst k trees produced
in line 3 are strongly connected components. The basis for the induction, when
k D 0, is trivial.
In the inductive step, we assume that each of the ﬁrst k depth-ﬁrst trees produced
in line 3 is a strongly connected component, and we consider the .k C 1/st tree
produced. Let the root of this tree be vertex u, and let u be in strongly connected
component C. Because of how we choose roots in the depth-ﬁrst search in line 3,
u:f D f .C/ > f .C 0/ for any strongly connected component C 0 other than C
that has yet to be visited. By the inductive hypothesis, at the time that the search
visits u, all other vertices of C are white. By the white-path theorem, therefore, all
other vertices of C are descendants of u in its depth-ﬁrst tree. Moreover, by the
inductive hypothesis and by Corollary 22.15, any edges in GT that leave C must be
to strongly connected components that have already been visited. Thus, no vertex

620
Chapter 22
Elementary Graph Algorithms
in any strongly connected component other than C will be a descendant of u during
the depth-ﬁrst search of GT. Thus, the vertices of the depth-ﬁrst tree in GT that is
rooted at u form exactly one strongly connected component, which completes the
inductive step and the proof.
Here is another way to look at how the second depth-ﬁrst search operates. Con-
sider the component graph .GT/SCC of GT. If we map each strongly connected
component visited in the second depth-ﬁrst search to a vertex of .GT/SCC, the sec-
ond depth-ﬁrst search visits vertices of .GT/SCC in the reverse of a topologically
sorted order. If we reverse the edges of .GT/SCC, we get the graph ..GT/SCC/T.
Because ..GT/SCC/T D GSCC (see Exercise 22.5-4), the second depth-ﬁrst search
visits the vertices of GSCC in topologically sorted order.
Exercises
22.5-1
How can the number of strongly connected components of a graph change if a new
edge is added?
22.5-2
Show how the procedure STRONGLY-CONNECTED-COMPONENTS works on the
graph of Figure 22.6. Speciﬁcally, show the ﬁnishing times computed in line 1 and
the forest produced in line 3. Assume that the loop of lines 5–7 of DFS considers
vertices in alphabetical order and that the adjacency lists are in alphabetical order.
22.5-3
Professor Bacon claims that the algorithm for strongly connected components
would be simpler if it used the original (instead of the transpose) graph in the
second depth-ﬁrst search and scanned the vertices in order of increasing ﬁnishing
times. Does this simpler algorithm always produce correct results?
22.5-4
Prove that for any directed graph G, we have ..GT/SCC/T D GSCC. That is, the
transpose of the component graph of GT is the same as the component graph of G.
22.5-5
Give an O.V C E/-time algorithm to compute the component graph of a directed
graph G D .V; E/. Make sure that there is at most one edge between two vertices
in the component graph your algorithm produces.

Problems for Chapter 22
621
22.5-6
Given a directed graph G D .V; E/, explain how to create another graph G0 D
.V; E0/ such that (a) G0 has the same strongly connected components as G, (b) G0
has the same component graph as G, and (c) E0 is as small as possible. Describe a
fast algorithm to compute G0.
22.5-7
A directed graph G D .V; E/ is semiconnected if, for all pairs of vertices u;  2 V ,
we have u ;  or  ; u. Give an efﬁcient algorithm to determine whether
or not G is semiconnected. Prove that your algorithm is correct, and analyze its
running time.
Problems
22-1
Classifying edges by breadth-ﬁrst search
A depth-ﬁrst forest classiﬁes the edges of a graph into tree, back, forward, and
cross edges. A breadth-ﬁrst tree can also be used to classify the edges reachable
from the source of the search into the same four categories.
a. Prove that in a breadth-ﬁrst search of an undirected graph, the following prop-
erties hold:
1. There are no back edges and no forward edges.
2. For each tree edge .u; /, we have :d D u:d C 1.
3. For each cross edge .u; /, we have :d D u:d or :d D u:d C 1.
b. Prove that in a breadth-ﬁrst search of a directed graph, the following properties
hold:
1. There are no forward edges.
2. For each tree edge .u; /, we have :d D u:d C 1.
3. For each cross edge .u; /, we have :d  u:d C 1.
4. For each back edge .u; /, we have 0  :d  u:d.
22-2
Articulation points, bridges, and biconnected components
Let G D .V; E/ be a connected, undirected graph. An articulation point of G is
a vertex whose removal disconnects G. A bridge of G is an edge whose removal
disconnects G. A biconnected component of G is a maximal set of edges such
that any two edges in the set lie on a common simple cycle. Figure 22.10 illustrates

622
Chapter 22
Elementary Graph Algorithms
1
2
3
4
5
6
Figure 22.10
The articulation points, bridges, and biconnected components of a connected, undi-
rected graph for use in Problem 22-2. The articulation points are the heavily shaded vertices, the
bridges are the heavily shaded edges, and the biconnected components are the edges in the shaded
regions, with a bcc numbering shown.
these deﬁnitions. We can determine articulation points, bridges, and biconnected
components using depth-ﬁrst search. Let G D .V; E/ be a depth-ﬁrst tree of G.
a. Prove that the root of G is an articulation point of G if and only if it has at
least two children in G.
b. Let  be a nonroot vertex of G. Prove that  is an articulation point of G if and
only if  has a child s such that there is no back edge from s or any descendant
of s to a proper ancestor of .
c. Let
:low D min
(
:d ;
w:d W .u; w/ is a back edge for some descendant u of  :
Show how to compute :low for all vertices  2 V in O.E/ time.
d. Show how to compute all articulation points in O.E/ time.
e. Prove that an edge of G is a bridge if and only if it does not lie on any simple
cycle of G.
f.
Show how to compute all the bridges of G in O.E/ time.
g. Prove that the biconnected components of G partition the nonbridge edges of G.
h. Give an O.E/-time algorithm to label each edge e of G with a positive in-
teger e:bcc such that e:bcc D e0:bcc if and only if e and e0 are in the same
biconnected component.

Notes for Chapter 22
623
22-3
Euler tour
An Euler tour of a strongly connected, directed graph G D .V; E/ is a cycle that
traverses each edge of G exactly once, although it may visit a vertex more than
once.
a. Show that G has an Euler tour if and only if in-degree./ D out-degree./ for
each vertex  2 V .
b. Describe an O.E/-time algorithm to ﬁnd an Euler tour of G if one exists. (Hint:
Merge edge-disjoint cycles.)
22-4
Reachability
Let G D .V; E/ be a directed graph in which each vertex u 2 V is labeled with
a unique integer L.u/ from the set f1; 2; : : : ; jV jg. For each vertex u 2 V , let
R.u/ D f 2 V W u ; g be the set of vertices that are reachable from u. Deﬁne
min.u/ to be the vertex in R.u/ whose label is minimum, i.e., min.u/ is the vertex 
such that L./ D min fL.w/ W w 2 R.u/g. Give an O.V CE/-time algorithm that
computes min.u/ for all vertices u 2 V .
Chapter notes
Even [103] and Tarjan [330] are excellent references for graph algorithms.
Breadth-ﬁrst search was discovered by Moore [260] in the context of ﬁnding
paths through mazes. Lee [226] independently discovered the same algorithm in
the context of routing wires on circuit boards.
Hopcroft and Tarjan [178] advocated the use of the adjacency-list representation
over the adjacency-matrix representation for sparse graphs and were the ﬁrst to
recognize the algorithmic importance of depth-ﬁrst search. Depth-ﬁrst search has
been widely used since the late 1950s, especially in artiﬁcial intelligence programs.
Tarjan [327] gave a linear-time algorithm for ﬁnding strongly connected compo-
nents. The algorithm for strongly connected components in Section 22.5 is adapted
from Aho, Hopcroft, and Ullman [6], who credit it to S. R. Kosaraju (unpublished)
and M. Sharir [314]. Gabow [119] also developed an algorithm for strongly con-
nected components that is based on contracting cycles and uses two stacks to make
it run in linear time. Knuth [209] was the ﬁrst to give a linear-time algorithm for
topological sorting.
