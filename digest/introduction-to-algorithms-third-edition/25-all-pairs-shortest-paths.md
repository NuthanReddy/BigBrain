# 25 All-Pairs Shortest Paths

In this chapter, we consider the problem of ﬁnding shortest paths between all pairs of vertices in a graph. This problem might arise in making a table of distances between all pairs of cities for a road atlas. As in Chapter 24, we are given a weighted, directed graph G D .V; E/ with a weight function w W E ! R that maps edges to real-valued weights. We wish to ﬁnd, for every pair of vertices u;  2 V , a shortest (least-weight) path from u to , where the weight of a path is the sum of the weights of its constituent edges. We typically want the output in tabular form: the entry in u’s row and ’s column should be the weight of a shortest path from u to . We can solve an all-pairs shortest-paths problem by running a single-source shortest-paths algorithm jV j times, once for each vertex as the source. If all edge weights are nonnegative, we can use Dijkstra’s algorithm. If we use the linear-array implementation of the min-priority queue, the running time is O.V 3 C VE/ D O.V 3/. The binary min-heap implementation of the min-priority queue yields a running time of O.VE lg V /, which is an improvement if the graph is sparse. Alternatively, we can implement the min-priority queue with a Fibonacci heap, yielding a running time of O.V 2 lg V C VE/. If the graph has negative-weight edges, we cannot use Dijkstra’s algorithm. Instead, we must run the slower Bellman-Ford algorithm once from each vertex. The resulting running time is O.V 2E/, which on a dense graph is O.V 4/. In this chapter we shall see how to do better. We also investigate the relation of the all-pairs shortest-paths problem to matrix multiplication and study its algebraic structure.

Unlike the single-source algorithms, which assume an adjacency-list representation of the graph, most of the algorithms in this chapter use an adjacencymatrix representation. (Johnson’s algorithm for sparse graphs, in Section 25.3, uses adjacency lists.) For convenience, we assume that the vertices are numbered 1; 2; : : : ; jV j, so that the input is an n 	 n matrix W representing the edge weights of an n-vertex directed graph G D .V; E/. That is, W D .wij/, where

wij D  if i D j ; the weight of directed edge .i; j / if i ¤ j and .i; j / 2 E ; if i ¤ j and .i; j / 62 E : (25.1) We allow negative-weight edges, but we assume for the time being that the input graph contains no negative-weight cycles. The tabular output of the all-pairs shortest-paths algorithms presented in this chapter is an n 	 n matrix D D .dij/, where entry dij contains the weight of a shortest path from vertex i to vertex j . That is, if we let ı.i; j / denote the shortestpath weight from vertex i to vertex j (as in Chapter 24), then dij D ı.i; j / at termination. To solve the all-pairs shortest-paths problem on an input adjacency matrix, we need to compute not only the shortest-path weights but also a predecessor matrix … D .ij /, where ij is NIL if either i D j or there is no path from i to j , and otherwise ij is the predecessor of j on some shortest path from i. Just as the predecessor subgraph G from Chapter 24 is a shortest-paths tree for a given source vertex, the subgraph induced by the ith row of the … matrix should be a shortest-paths tree with root i. For each vertex i 2 V , we deﬁne the predecessor subgraph of G for i as G;i D .V;i; E;i/ , where V;i D fj 2 V W ij ¤ NILg [ fig and E;i D f.ij; j / W j 2 V;i  figg : If G;i is a shortest-paths tree, then the following procedure, which is a modiﬁed version of the PRINT-PATH procedure from Chapter 22, prints a shortest path from vertex i to vertex j .

PRINT-ALL-PAIRS-SHORTEST-PATH.…; i; j / if i == j print i elseif ij == NIL print “no path from” i “to” j “exists” else PRINT-ALL-PAIRS-SHORTEST-PATH.…; i; ij / print j In order to highlight the essential features of the all-pairs algorithms in this chapter, we won’t cover the creation and properties of predecessor matrices as extensively as we dealt with predecessor subgraphs in Chapter 24. Some of the exercises cover the basics.

Chapter outline Section 25.1 presents a dynamic-programming algorithm based on matrix multiplication to solve the all-pairs shortest-paths problem. Using the technique of “repeated squaring,” we can achieve a running time of ‚.V 3 lg V /. Section 25.2 gives another dynamic-programming algorithm, the Floyd-Warshall algorithm, which runs in time ‚.V 3/. Section 25.2 also covers the problem of ﬁnding the transitive closure of a directed graph, which is related to the all-pairs shortest-paths problem. Finally, Section 25.3 presents Johnson’s algorithm, which solves the allpairs shortest-paths problem in O.V 2 lg V C VE/ time and is a good choice for large, sparse graphs.

Before proceeding, we need to establish some conventions for adjacency-matrix representations. First, we shall generally assume that the input graph G D .V; E/ has n vertices, so that n D jV j. Second, we shall use the convention of denoting matrices by uppercase letters, such as W , L, or D, and their individual elements by subscripted lowercase letters, such as wij, lij, or dij. Some matrices will have parenthesized superscripts, as in L.m/ D

l.m/ ij

or D.m/ D

d .m/ ij

, to indicate iterates. Finally, for a given n 	 n matrix A, we shall assume that the value of n is stored in the attribute A:rows.

## 25.1 Shortest paths and matrix multiplication

This section presents a dynamic-programming algorithm for the all-pairs shortestpaths problem on a directed graph G D .V; E/. Each major loop of the dynamic program will invoke an operation that is very similar to matrix multiplication, so that the algorithm will look like repeated matrix multiplication. We shall start by developing a ‚.V 4/-time algorithm for the all-pairs shortest-paths problem and then improve its running time to ‚.V 3 lg V /.

Before proceeding, let us brieﬂy recap the steps given in Chapter 15 for developing a dynamic-programming algorithm. 1. Characterize the structure of an optimal solution. 2. Recursively deﬁne the value of an optimal solution. 3. Compute the value of an optimal solution in a bottom-up fashion. We reserve the fourth step—constructing an optimal solution from computed information—for the exercises.

## 25.1 Shortest paths and matrix multiplication

The structure of a shortest path We start by characterizing the structure of an optimal solution. For the all-pairs shortest-paths problem on a graph G D .V; E/, we have proven (Lemma 24.1) that all subpaths of a shortest path are shortest paths. Suppose that we represent the graph by an adjacency matrix W D .wij/. Consider a shortest path p from vertex i to vertex j , and suppose that p contains at most m edges. Assuming that there are no negative-weight cycles, m is ﬁnite. If i D j , then p has weight 0 and no edges. If vertices i and j are distinct, then we decompose path p into i p0 ; k ! j , where path p0 now contains at most m  1 edges. By Lemma 24.1, p0 is a shortest path from i to k, and so ı.i; j / D ı.i; k/ C wkj.

A recursive solution to the all-pairs shortest-paths problem Now, let l.m/ ij be the minimum weight of any path from vertex i to vertex j that contains at most m edges. When m D 0, there is a shortest path from i to j with no edges if and only if i D j . Thus, l.0/ ij D ( if i D j ; if i ¤ j :

For m  1, we compute l.m/ ij as the minimum of l.m1/ ij (the weight of a shortest path from i to j consisting of at most m1 edges) and the minimum weight of any path from i to j consisting of at most m edges, obtained by looking at all possible predecessors k of j . Thus, we recursively deﬁne l.m/ ij D min  l.m1/ ij ; min 1kn ˚ l.m1/ ik C wkj

 D min 1kn ˚ l.m1/ ik C wkj

: (25.2) The latter equality follows since wjj D 0 for all j .

What are the actual shortest-path weights ı.i; j /? If the graph contains no negative-weight cycles, then for every pair of vertices i and j for which ı.i; j / < 1, there is a shortest path from i to j that is simple and thus contains at most n  1 edges. A path from vertex i to vertex j with more than n  1 edges cannot have lower weight than a shortest path from i to j . The actual shortest-path weights are therefore given by ı.i; j / D l.n1/ ij D l.n/ ij D l.nC1/ ij D    : (25.3)

Computing the shortest-path weights bottom up Taking as our input the matrix W D .wij/, we now compute a series of matrices L.1/; L.2/; : : : ; L.n1/, where for m D 1; 2; : : : ; n  1, we have L.m/ D

l.m/ ij

. The ﬁnal matrix L.n1/ contains the actual shortest-path weights. Observe that l.1/ ij D wij for all vertices i; j 2 V , and so L.1/ D W . The heart of the algorithm is the following procedure, which, given matrices L.m1/ and W , returns the matrix L.m/. That is, it extends the shortest paths computed so far by one more edge.

EXTEND-SHORTEST-PATHS.L; W / n D L:rows let L0 D

l0 ij

be a new n 	 n matrix for i D 1 to n for j D 1 to n l0 ij D 1 for k D 1 to n l0 ij D min.l0 ij; lik C wkj/ return L0 The procedure computes a matrix L0 D .l0 ij /, which it returns at the end. It does so by computing equation (25.2) for all i and j , using L for L.m1/ and L0 for L.m/. (It is written without the superscripts to make its input and output matrices independent of m.) Its running time is ‚.n3/ due to the three nested for loops. Now we can see the relation to matrix multiplication. Suppose we wish to compute the matrix product C D A  B of two n 	 n matrices A and B. Then, for i; j D 1; 2; : : : ; n, we compute cij D n X kD1 aik  bkj : (25.4) Observe that if we make the substitutions l.m1/ ! a ; w ! b ; l.m/ ! c ; min !

C ; C !  in equation (25.2), we obtain equation (25.4). Thus, if we make these changes to EXTEND-SHORTEST-PATHS and also replace 1 (the identity for min) by 0 (the

## 25.1 Shortest paths and matrix multiplication

identity for C), we obtain the same ‚.n3/-time procedure for multiplying square matrices that we saw in Section 4.2:

SQUARE-MATRIX-MULTIPLY.A; B/ n D A:rows let C be a new n 	 n matrix for i D 1 to n for j D 1 to n cij D 0 for k D 1 to n cij D cij C aik  bkj return C Returning to the all-pairs shortest-paths problem, we compute the shortest-path weights by extending shortest paths edge by edge. Letting A  B denote the matrix “product” returned by EXTEND-SHORTEST-PATHS.A; B/, we compute the sequence of n  1 matrices L.1/ D L.0/  W D W ; L.2/ D L.1/  W D W 2 ; L.3/ D L.2/  W D W 3 ; :::

L.n1/ D L.n2/  W D W n1 : As we argued above, the matrix L.n1/ D W n1 contains the shortest-path weights. The following procedure computes this sequence in ‚.n4/ time.

SLOW-ALL-PAIRS-SHORTEST-PATHS.W / n D W:rows L.1/ D W for m D 2 to n  1 let L.m/ be a new n 	 n matrix L.m/ D EXTEND-SHORTEST-PATHS.L.m1/; W / return L.n1/ Figure 25.1 shows a graph and the matrices L.m/ computed by the procedure SLOW-ALL-PAIRS-SHORTEST-PATHS.

Improving the running time Our goal, however, is not to compute all the L.m/ matrices: we are interested only in matrix L.n1/. Recall that in the absence of negative-weight cycles, equa-

–4 –5 L.1/ D  4 5 ˘ L.2/ D  4 4 1 5 2 ˘ L.3/ D  0 3 4 4 1 1 5 2 ˘ L.4/ D  0 3 4 4 1 1 5 2 ˘ Figure 25.1 A directed graph and the sequence of matrices L.m/ computed by SLOW-ALL-PAIRS- SHORTEST-PATHS. You might want to verify that L.5/, deﬁned as L.4/  W , equals L.4/, and thus L.m/ D L.4/ for all m  4. tion (25.3) implies L.m/ D L.n1/ for all integers m  n  1. Just as traditional matrix multiplication is associative, so is matrix multiplication deﬁned by the EXTEND-SHORTEST-PATHS procedure (see Exercise 25.1-4). Therefore, we can compute L.n1/ with only dlg.n  1/e matrix products by computing the sequence L.1/ D W ; L.2/ D W 2 D W  W ; L.4/ D W 4 D W 2  W 2 L.8/ D W 8 D W 4  W 4 ; :::

L.2dlg.n1/e/ D W 2dlg.n1/e D W 2dlg.n1/e1  W 2dlg.n1/e1 :

Since 2dlg.n1/e  n  1, the ﬁnal product L.2dlg.n1/e/ is equal to L.n1/. The following procedure computes the above sequence of matrices by using this technique of repeated squaring.

## 25.1 Shortest paths and matrix multiplication

–1 –4 –8 Figure 25.2 A weighted, directed graph for use in Exercises 25.1-1, 25.2-1, and 25.3-1.

FASTER-ALL-PAIRS-SHORTEST-PATHS.W / n D W:rows L.1/ D W m D 1 while m < n  1 let L.2m/ be a new n 	 n matrix L.2m/ D EXTEND-SHORTEST-PATHS.L.m/; L.m// m D 2m return L.m/ In each iteration of the while loop of lines 4–7, we compute L.2m/ D

L.m/ 2, starting with m D 1.

At the end of each iteration, we double the value of m. The ﬁnal iteration computes L.n1/ by actually computing L.2m/ for some n  1  2m < 2n  2. By equation (25.3), L.2m/ D L.n1/. The next time the test in line 4 is performed, m has been doubled, so now m  n  1, the test fails, and the procedure returns the last matrix it computed.

Because each of the dlg.n  1/e matrix products takes ‚.n3/ time, FASTER- ALL-PAIRS-SHORTEST-PATHS runs in ‚.n3 lg n/ time. Observe that the code is tight, containing no elaborate data structures, and the constant hidden in the ‚-notation is therefore small.

## Exercises

25.1-1 Run SLOW-ALL-PAIRS-SHORTEST-PATHS on the weighted, directed graph of Figure 25.2, showing the matrices that result for each iteration of the loop. Then do the same for FASTER-ALL-PAIRS-SHORTEST-PATHS. 25.1-2 Why do we require that wii D 0 for all 1  i  n?

25.1-3 What does the matrix L.0/ D  ::: ::: ::: ::: :::  used in the shortest-paths algorithms correspond to in regular matrix multiplication? 25.1-4 Show that matrix multiplication deﬁned by EXTEND-SHORTEST-PATHS is associative. 25.1-5 Show how to express the single-source shortest-paths problem as a product of matrices and a vector. Describe how evaluating this product corresponds to a Bellman- Ford-like algorithm (see Section 24.1). 25.1-6 Suppose we also wish to compute the vertices on shortest paths in the algorithms of this section. Show how to compute the predecessor matrix … from the completed matrix L of shortest-path weights in O.n3/ time. 25.1-7 We can also compute the vertices on shortest paths as we compute the shortestpath weights. Deﬁne .m/ ij as the predecessor of vertex j on any minimum-weight path from i to j that contains at most m edges. Modify the EXTEND-SHORTEST- PATHS and SLOW-ALL-PAIRS-SHORTEST-PATHS procedures to compute the matrices ….1/; ….2/; : : : ; ….n1/ as the matrices L.1/; L.2/; : : : ; L.n1/ are computed. 25.1-8 The FASTER-ALL-PAIRS-SHORTEST-PATHS procedure, as written, requires us to store dlg.n  1/e matrices, each with n2 elements, for a total space requirement of ‚.n2 lg n/. Modify the procedure to require only ‚.n2/ space by using only two n 	 n matrices. 25.1-9 Modify FASTER-ALL-PAIRS-SHORTEST-PATHS so that it can determine whether the graph contains a negative-weight cycle.

## 25.2 The Floyd-Warshall algorithm

25.1-10 Give an efﬁcient algorithm to ﬁnd the length (number of edges) of a minimumlength negative-weight cycle in a graph.

## 25.2 The Floyd-Warshall algorithm

In this section, we shall use a different dynamic-programming formulation to solve the all-pairs shortest-paths problem on a directed graph G D .V; E/. The resulting algorithm, known as the Floyd-Warshall algorithm, runs in ‚.V 3/ time. As before, negative-weight edges may be present, but we assume that there are no negative-weight cycles. As in Section 25.1, we follow the dynamic-programming process to develop the algorithm.

After studying the resulting algorithm, we present a similar method for ﬁnding the transitive closure of a directed graph. The structure of a shortest path In the Floyd-Warshall algorithm, we characterize the structure of a shortest path differently from how we characterized it in Section 25.1. The Floyd-Warshall algorithm considers the intermediate vertices of a shortest path, where an intermediate vertex of a simple path p D h1; 2; : : : ; li is any vertex of p other than 1 or l, that is, any vertex in the set f2; 3; : : : ; l1g. The Floyd-Warshall algorithm relies on the following observation. Under our assumption that the vertices of G are V D f1; 2; : : : ; ng, let us consider a subset f1; 2; : : : ; kg of vertices for some k. For any pair of vertices i; j 2 V , consider all paths from i to j whose intermediate vertices are all drawn from f1; 2; : : : ; kg, and let p be a minimum-weight path from among them. (Path p is simple.) The Floyd- Warshall algorithm exploits a relationship between path p and shortest paths from i to j with all intermediate vertices in the set f1; 2; : : : ; k  1g. The relationship depends on whether or not k is an intermediate vertex of path p.  If k is not an intermediate vertex of path p, then all intermediate vertices of path p are in the set f1; 2; : : : ; k  1g. Thus, a shortest path from vertex i to vertex j with all intermediate vertices in the set f1; 2; : : : ; k  1g is also a shortest path from i to j with all intermediate vertices in the set f1; 2; : : : ; kg.  If k is an intermediate vertex of path p, then we decompose p into i p1 ; k p2 ; j , as Figure 25.3 illustrates. By Lemma 24.1, p1 is a shortest path from i to k with all intermediate vertices in the set f1; 2; : : : ; kg. In fact, we can make a slightly stronger statement. Because vertex k is not an intermediate vertex of path p1, all intermediate vertices of p1 are in the set f1; 2; : : : ; k  1g. There-

i k j p1 p2 p: all intermediate vertices in f1; 2; : : : ; kg all intermediate vertices in f1; 2; : : : ; k  1g all intermediate vertices in f1; 2; : : : ; k  1g Figure 25.3 Path p is a shortest path from vertex i to vertex j, and k is the highest-numbered intermediate vertex of p. Path p1, the portion of path p from vertex i to vertex k, has all intermediate vertices in the set f1; 2; : : : ; k  1g. The same holds for path p2 from vertex k to vertex j. fore, p1 is a shortest path from i to k with all intermediate vertices in the set f1; 2; : : : ; k  1g. Similarly, p2 is a shortest path from vertex k to vertex j with all intermediate vertices in the set f1; 2; : : : ; k  1g.

A recursive solution to the all-pairs shortest-paths problem Based on the above observations, we deﬁne a recursive formulation of shortestpath estimates that differs from the one in Section 25.1. Let d .k/ ij be the weight of a shortest path from vertex i to vertex j for which all intermediate vertices are in the set f1; 2; : : : ; kg. When k D 0, a path from vertex i to vertex j with no intermediate vertex numbered higher than 0 has no intermediate vertices at all.

Such a path has at most one edge, and hence d .0/ ij D wij. Following the above discussion, we deﬁne d .k/ ij recursively by d .k/ ij D ( wij if k D 0 ; min

d .k1/ ij ; d .k1/ ik C d .k1/ kj

if k  1 : (25.5) Because for any path, all intermediate vertices are in the set f1; 2; : : : ; ng, the matrix D.n/ D

d .n/ ij

gives the ﬁnal answer: d .n/ ij D ı.i; j / for all i; j 2 V .

Computing the shortest-path weights bottom up Based on recurrence (25.5), we can use the following bottom-up procedure to compute the values d .k/ ij in order of increasing values of k. Its input is an n	n matrix W deﬁned as in equation (25.1). The procedure returns the matrix D.n/ of shortestpath weights.

## 25.2 The Floyd-Warshall algorithm

FLOYD-WARSHALL.W / n D W:rows D.0/ D W for k D 1 to n let D.k/ D

d .k/ ij

be a new n 	 n matrix for i D 1 to n for j D 1 to n d .k/ ij D min

d .k1/ ij ; d .k1/ ik C d .k1/ kj

return D.n/ Figure 25.4 shows the matrices D.k/ computed by the Floyd-Warshall algorithm for the graph in Figure 25.1. The running time of the Floyd-Warshall algorithm is determined by the triply nested for loops of lines 3–7. Because each execution of line 7 takes O.1/ time, the algorithm runs in time ‚.n3/. As in the ﬁnal algorithm in Section 25.1, the code is tight, with no elaborate data structures, and so the constant hidden in the ‚-notation is small. Thus, the Floyd-Warshall algorithm is quite practical for even moderate-sized input graphs.

Constructing a shortest path There are a variety of different methods for constructing shortest paths in the Floyd- Warshall algorithm. One way is to compute the matrix D of shortest-path weights and then construct the predecessor matrix … from the D matrix. Exercise 25.1-6 asks you to implement this method so that it runs in O.n3/ time. Given the predecessor matrix …, the PRINT-ALL-PAIRS-SHORTEST-PATH procedure will print the vertices on a given shortest path.

Alternatively, we can compute the predecessor matrix … while the algorithm computes the matrices D.k/. Speciﬁcally, we compute a sequence of matrices ….0/; ….1/; : : : ; ….n/, where … D ….n/ and we deﬁne .k/ ij as the predecessor of vertex j on a shortest path from vertex i with all intermediate vertices in the set f1; 2; : : : ; kg. We can give a recursive formulation of .k/ ij . When k D 0, a shortest path from i to j has no intermediate vertices at all. Thus, .0/ ij D ( NIL if i D j or wij D 1 ; i if i ¤ j and wij < 1 : (25.6) For k  1, if we take the path i ; k ; j , where k ¤ j , then the predecessor of j we choose is the same as the predecessor of j we chose on a shortest path from k with all intermediate vertices in the set f1; 2; : : : ; k  1g. Otherwise, we

D.0/ D  4 5 ˘ ….0/ D  NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL ˘ D.1/ D  4 5 2 ˘ ….1/ D  NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL ˘ D.2/ D  4 5 2 ˘ ….2/ D  NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL ˘ D.3/ D  4 1 5 2 ˘ ….3/ D  NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL NIL ˘ D.4/ D  0 1 4 4 1 1 5 2 ˘ ….4/ D  NIL NIL NIL NIL NIL ˘ D.5/ D  0 3 4 4 1 1 5 2 ˘ ….5/ D  NIL NIL NIL NIL NIL ˘ Figure 25.4 The sequence of matrices D.k/ and ….k/ computed by the Floyd-Warshall algorithm for the graph in Figure 25.1.

## 25.2 The Floyd-Warshall algorithm

choose the same predecessor of j that we chose on a shortest path from i with all intermediate vertices in the set f1; 2; : : : ; k  1g. Formally, for k  1, .k/ ij D ( .k1/ ij if d .k1/ ij  d .k1/ ik C d .k1/ kj ; .k1/ kj if d .k1/ ij > d .k1/ ik C d .k1/ kj : (25.7) We leave the incorporation of the ….k/ matrix computations into the FLOYD- WARSHALL procedure as Exercise 25.2-3. Figure 25.4 shows the sequence of ….k/ matrices that the resulting algorithm computes for the graph of Figure 25.1. The exercise also asks for the more difﬁcult task of proving that the predecessor subgraph G;i is a shortest-paths tree with root i. Exercise 25.2-7 asks for yet another way to reconstruct shortest paths.

Transitive closure of a directed graph Given a directed graph G D .V; E/ with vertex set V D f1; 2; : : : ; ng, we might wish to determine whether G contains a path from i to j for all vertex pairs i; j 2 V . We deﬁne the transitive closure of G as the graph G D .V; E/, where E D f.i; j / W there is a path from vertex i to vertex j in Gg : One way to compute the transitive closure of a graph in ‚.n3/ time is to assign a weight of 1 to each edge of E and run the Floyd-Warshall algorithm. If there is a path from vertex i to vertex j , we get dij < n. Otherwise, we get dij D 1. There is another, similar way to compute the transitive closure of G in ‚.n3/ time that can save time and space in practice. This method substitutes the logical operations _ (logical OR) and ^ (logical AND) for the arithmetic operations min and C in the Floyd-Warshall algorithm. For i; j; k D 1; 2; : : : ; n, we deﬁne t.k/ ij to be 1 if there exists a path in graph G from vertex i to vertex j with all intermediate vertices in the set f1; 2; : : : ; kg, and 0 otherwise. We construct the transitive closure G D .V; E/ by putting edge .i; j / into E if and only if t.n/ ij D 1. A recursive deﬁnition of t.k/ ij , analogous to recurrence (25.5), is t.0/ ij D ( if i ¤ j and .i; j / 62 E ; if i D j or .i; j / 2 E ; and for k  1, t.k/ ij D t.k1/ ij _

t.k1/ ik ^ t.k1/ kj

: (25.8) As in the Floyd-Warshall algorithm, we compute the matrices T .k/ D

t.k/ ij

in order of increasing k.

T .0/ D  1  T .1/ D  1  T .2/ D  1  T .3/ D  1  T .4/ D  1  Figure 25.5 A directed graph and the matrices T .k/ computed by the transitive-closure algorithm.

TRANSITIVE-CLOSURE.G/ n D jG:Vj let T .0/ D

t.0/ ij

be a new n 	 n matrix for i D 1 to n for j D 1 to n if i == j or .i; j / 2 G:E t.0/ ij D 1 else t.0/ ij D 0 for k D 1 to n let T .k/ D

t.k/ ij

be a new n 	 n matrix for i D 1 to n for j D 1 to n t.k/ ij D t.k1/ ij _

t.k1/ ik ^ t.k1/ kj

return T .n/ Figure 25.5 shows the matrices T .k/ computed by the TRANSITIVE-CLOSURE procedure on a sample graph. The TRANSITIVE-CLOSURE procedure, like the Floyd-Warshall algorithm, runs in ‚.n3/ time. On some computers, though, logical operations on single-bit values execute faster than arithmetic operations on integer words of data. Moreover, because the direct transitive-closure algorithm uses only boolean values rather than integer values, its space requirement is less

## 25.2 The Floyd-Warshall algorithm

than the Floyd-Warshall algorithm’s by a factor corresponding to the size of a word of computer storage.

## Exercises

25.2-1 Run the Floyd-Warshall algorithm on the weighted, directed graph of Figure 25.2.

Show the matrix D.k/ that results for each iteration of the outer loop. 25.2-2 Show how to compute the transitive closure using the technique of Section 25.1. 25.2-3 Modify the FLOYD-WARSHALL procedure to compute the ….k/ matrices according to equations (25.6) and (25.7). Prove rigorously that for all i 2 V , the predecessor subgraph G;i is a shortest-paths tree with root i. (Hint: To show that G;i is acyclic, ﬁrst show that .k/ ij D l implies d .k/ ij  d .k/ il C wlj, according to the deﬁnition of .k/ ij . Then, adapt the proof of Lemma 24.16.) 25.2-4 As it appears above, the Floyd-Warshall algorithm requires ‚.n3/ space, since we compute d .k/ ij for i; j; k D 1; 2; : : : ; n. Show that the following procedure, which simply drops all the superscripts, is correct, and thus only ‚.n2/ space is required.

FLOYD-WARSHALL0.W / n D W:rows D D W for k D 1 to n for i D 1 to n for j D 1 to n dij D min .dij; dik C dkj / return D 25.2-5 Suppose that we modify the way in which equation (25.7) handles equality: .k/ ij D ( .k1/ ij if d .k1/ ij < d .k1/ ik C d .k1/ kj ; .k1/ kj if d .k1/ ij  d .k1/ ik C d .k1/ kj :

Is this alternative deﬁnition of the predecessor matrix … correct?

25.2-6 How can we use the output of the Floyd-Warshall algorithm to detect the presence of a negative-weight cycle? 25.2-7 Another way to reconstruct shortest paths in the Floyd-Warshall algorithm uses values .k/ ij for i; j; k D 1; 2; : : : ; n, where .k/ ij is the highest-numbered intermediate vertex of a shortest path from i to j in which all intermediate vertices are in the set f1; 2; : : : ; kg. Give a recursive formulation for .k/ ij , modify the FLOYD- WARSHALL procedure to compute the .k/ ij values, and rewrite the PRINT-ALL- PAIRS-SHORTEST-PATH procedure to take the matrix ˆ D

.n/ ij

as an input.

How is the matrix ˆ like the s table in the matrix-chain multiplication problem of Section 15.2? 25.2-8 Give an O.VE/-time algorithm for computing the transitive closure of a directed graph G D .V; E/. 25.2-9 Suppose that we can compute the transitive closure of a directed acyclic graph in f .jV j ; jEj/ time, where f is a monotonically increasing function of jV j and jEj.

Show that the time to compute the transitive closure G D .V; E/ of a general directed graph G D .V; E/ is then f .jV j ; jEj/ C O.V C E/.

## 25.3 Johnson’s algorithm for sparse graphs

Johnson’s algorithm ﬁnds shortest paths between all pairs in O.V 2 lg V C VE/ time. For sparse graphs, it is asymptotically faster than either repeated squaring of matrices or the Floyd-Warshall algorithm. The algorithm either returns a matrix of shortest-path weights for all pairs of vertices or reports that the input graph contains a negative-weight cycle. Johnson’s algorithm uses as subroutines both Dijkstra’s algorithm and the Bellman-Ford algorithm, which Chapter 24 describes.

Johnson’s algorithm uses the technique of reweighting, which works as follows. If all edge weights w in a graph G D .V; E/ are nonnegative, we can ﬁnd shortest paths between all pairs of vertices by running Dijkstra’s algorithm once from each vertex; with the Fibonacci-heap min-priority queue, the running time of this all-pairs algorithm is O.V 2 lg V C VE/. If G has negative-weight edges but no negative-weight cycles, we simply compute a new set of nonnegative edge weights

## 25.3 Johnson’s algorithm for sparse graphs

that allows us to use the same method. The new set of edge weights yw must satisfy two important properties: 1. For all pairs of vertices u;  2 V , a path p is a shortest path from u to  using weight function w if and only if p is also a shortest path from u to  using weight function yw. 2. For all edges .u; /, the new weight yw.u; / is nonnegative. As we shall see in a moment, we can preprocess G to determine the new weight function yw in O.VE/ time.

Preserving shortest paths by reweighting The following lemma shows how easily we can reweight the edges to satisfy the ﬁrst property above. We use ı to denote shortest-path weights derived from weight function w and yı to denote shortest-path weights derived from weight function yw.

> **Lemma 25.1 (Reweighting does not change shortest paths)**

Given a weighted, directed graph G D .V; E/ with weight function w W E ! R, let h W V ! R be any function mapping vertices to real numbers. For each edge .u; / 2 E, deﬁne yw.u; / D w.u; / C h.u/  h./ : (25.9) Let p D h0; 1; : : : ; ki be any path from vertex 0 to vertex k. Then p is a shortest path from 0 to k with weight function w if and only if it is a shortest path with weight function yw. That is, w.p/ D ı.0; k/ if and only if yw.p/ D yı.0; k/.

Furthermore, G has a negative-weight cycle using weight function w if and only if G has a negative-weight cycle using weight function yw.

Proof We start by showing that yw.p/ D w.p/ C h.0/  h.k/ : (25.10) We have yw.p/ D k X iD1 yw.i1; i/ D k X iD1 .w.i1; i/ C h.i1/  h.i// D k X iD1 w.i1; i/ C h.0/  h.k/ (because the sum telescopes) D w.p/ C h.0/  h.k/ :

Therefore, any path p from 0 to k has yw.p/ D w.p/ C h.0/  h.k/. Because h.0/ and h.k/ do not depend on the path, if one path from 0 to k is shorter than another using weight function w, then it is also shorter using yw. Thus, w.p/ D ı.0; k/ if and only if yw.p/ D yı.0; k/.

Finally, we show that G has a negative-weight cycle using weight function w if and only if G has a negative-weight cycle using weight function yw. Consider any cycle c D h0; 1; : : : ; ki, where 0 D k. By equation (25.10), yw.c/ D w.c/ C h.0/  h.k/ D w.c/ ; and thus c has negative weight using w if and only if it has negative weight using yw.

Producing nonnegative weights by reweighting Our next goal is to ensure that the second property holds: we want yw.u; / to be nonnegative for all edges .u; / 2 E. Given a weighted, directed graph G D .V; E/ with weight function w W E ! R, we make a new graph G0 D .V 0; E0/, where V 0 D V [ fsg for some new vertex s 62 V and E0 D E [ f.s; / W  2 V g. We extend the weight function w so that w.s; / D 0 for all  2 V . Note that because s has no edges that enter it, no shortest paths in G0, other than those with source s, contain s. Moreover, G0 has no negative-weight cycles if and only if G has no negative-weight cycles. Figure 25.6(a) shows the graph G0 corresponding to the graph G of Figure 25.1. Now suppose that G and G0 have no negative-weight cycles.

Let us deﬁne h./ D ı.s; / for all  2 V 0. By the triangle inequality (Lemma 24.10), we have h./  h.u/ C w.u; / for all edges .u; / 2 E0. Thus, if we de- ﬁne the new weights yw by reweighting according to equation (25.9), we have yw.u; / D w.u; / C h.u/  h./  0, and we have satisﬁed the second property.

Figure 25.6(b) shows the graph G0 from Figure 25.6(a) with reweighted edges.

Computing all-pairs shortest paths Johnson’s algorithm to compute all-pairs shortest paths uses the Bellman-Ford algorithm (Section 24.1) and Dijkstra’s algorithm (Section 24.3) as subroutines. It assumes implicitly that the edges are stored in adjacency lists. The algorithm returns the usual jV j 	 jV j matrix D D dij, where dij D ı.i; j /, or it reports that the input graph contains a negative-weight cycle. As is typical for an all-pairs shortest-paths algorithm, we assume that the vertices are numbered from 1 to jV j.

## 25.3 Johnson’s algorithm for sparse graphs

2/1 2/–3 2/2 0/–4 2/3 0/–4 0/1 2/–1 2/7 0/4 0/5 2/3 2/2 0/–1 0/–5 2/–2 4/8 2/5 2/1 2/6 (a) (c) (b) –4 –4 –1 –5 –5 –4 –1 –5 (d) (e) (f) (g) 0/0 0/0 0/0 0/0 0/0 Figure 25.6 Johnson’s all-pairs shortest-paths algorithm run on the graph of Figure 25.1. Vertex numbers appear outside the vertices. (a) The graph G0 with the original weight function w. The new vertex s is black. Within each vertex  is h./ D ı.s; /. (b) After reweighting each edge .u; / with weight function yw.u; / D w.u; / C h.u/  h./. (c)–(g) The result of running is black, and shaded edges are in the shortest-paths tree computed by the algorithm. Within each vertex  are the values yı.u; / and ı.u; /, separated by a slash. The value du D ı.u; / is equal to yı. / C h./  h.u/ Dijkstra’s algorithm on each vertex of G using weight function wy. In each part, the source vertex u . u;

JOHNSON.G; w/ compute G0, where G0:V D G:V [ fsg, G0:E D G:E [ f.s; / W  2 G:Vg, and w.s; / D 0 for all  2 G:V if BELLMAN-FORD.G0; w; s/ == FALSE print “the input graph contains a negative-weight cycle” else for each vertex  2 G0:V set h./ to the value of ı.s; / computed by the Bellman-Ford algorithm for each edge .u; / 2 G0:E yw.u; / D w.u; / C h.u/  h./ let D D .du/ be a new n 	 n matrix for each vertex u 2 G:V run DIJKSTRA.G; yw; u/ to compute yı.u; / for all  2 G:V for each vertex  2 G:V du D yı.u; / C h./  h.u/ return D This code simply performs the actions we speciﬁed earlier. Line 1 produces G0.

Line 2 runs the Bellman-Ford algorithm on G0 with weight function w and source vertex s. If G0, and hence G, contains a negative-weight cycle, line 3 reports the problem. Lines 4–12 assume that G0 contains no negative-weight cycles. Lines 4–5 set h./ to the shortest-path weight ı.s; / computed by the Bellman-Ford algorithm for all  2 V 0. Lines 6–7 compute the new weights yw. For each pair of vertices u;  2 V , the for loop of lines 9–12 computes the shortest-path weight yı.u; / by calling Dijkstra’s algorithm once from each vertex in V . Line 12 stores in matrix entry du the correct shortest-path weight ı.u; /, calculated using equation (25.10). Finally, line 13 returns the completed D matrix. Figure 25.6 depicts the execution of Johnson’s algorithm. If we implement the min-priority queue in Dijkstra’s algorithm by a Fibonacci heap, Johnson’s algorithm runs in O.V 2 lg V CVE/ time. The simpler binary minheap implementation yields a running time of O.VE lg V /, which is still asymptotically faster than the Floyd-Warshall algorithm if the graph is sparse.

## Exercises

25.3-1 Use Johnson’s algorithm to ﬁnd the shortest paths between all pairs of vertices in the graph of Figure 25.2. Show the values of h and yw computed by the algorithm.

Problems for Chapter 25 25.3-2 What is the purpose of adding the new vertex s to V , yielding V 0? 25.3-3 Suppose that w.u; /  0 for all edges .u; / 2 E. What is the relationship between the weight functions w and yw? 25.3-4 Professor Greenstreet claims that there is a simpler way to reweight edges than the method used in Johnson’s algorithm. Letting w D min.u;/2E fw.u; /g, just deﬁne yw.u; / D w.u; /  w for all edges .u; / 2 E. What is wrong with the professor’s method of reweighting? 25.3-5 Suppose that we run Johnson’s algorithm on a directed graph G with weight function w. Show that if G contains a 0-weight cycle c, then yw.u; / D 0 for every edge .u; / in c. 25.3-6 Professor Michener claims that there is no need to create a new source vertex in line 1 of JOHNSON. He claims that instead we can just use G0 D G and let s be any vertex. Give an example of a weighted, directed graph G for which incorporating the professor’s idea into JOHNSON causes incorrect answers. Then show that if G is strongly connected (every vertex is reachable from every other vertex), the results returned by JOHNSON with the professor’s modiﬁcation are correct.

## Problems

25-1 Transitive closure of a dynamic graph Suppose that we wish to maintain the transitive closure of a directed graph G D .V; E/ as we insert edges into E. That is, after each edge has been inserted, we want to update the transitive closure of the edges inserted so far. Assume that the graph G has no edges initially and that we represent the transitive closure as a boolean matrix. a. Show how to update the transitive closure G D .V; E/ of a graph G D .V; E/ in O.V 2/ time when a new edge is added to G. b. Give an example of a graph G and an edge e such that .V 2/ time is required to update the transitive closure after the insertion of e into G, no matter what algorithm is used.

c. Describe an efﬁcient algorithm for updating the transitive closure as edges are inserted into the graph. For any sequence of n insertions, your algorithm should run in total time Pn iD1 ti D O.V 3/, where ti is the time to update the transitive closure upon inserting the ith edge. Prove that your algorithm attains this time bound. 25-2 Shortest paths in -dense graphs A graph G D .V; E/ is -dense if jEj D ‚.V 1C/ for some constant  in the range 0 <   1. By using d-ary min-heaps (see Problem 6-2) in shortest-paths algorithms on -dense graphs, we can match the running times of Fibonacci-heapbased algorithms without using as complicated a data structure. a. What are the asymptotic running times for INSERT, EXTRACT-MIN, and DECREASE-KEY, as a function of d and the number n of elements in a d-ary min-heap? What are these running times if we choose d D ‚.n˛/ for some constant 0 < ˛  1? Compare these running times to the amortized costs of these operations for a Fibonacci heap. b. Show how to compute shortest paths from a single source on an -dense directed graph G D .V; E/ with no negative-weight edges in O.E/ time. (Hint: Pick d as a function of .) c. Show how to solve the all-pairs shortest-paths problem on an -dense directed graph G D .V; E/ with no negative-weight edges in O.VE/ time. d. Show how to solve the all-pairs shortest-paths problem in O.VE/ time on an -dense directed graph G D .V; E/ that may have negative-weight edges but has no negative-weight cycles.

Chapter notes Lawler [224] has a good discussion of the all-pairs shortest-paths problem, although he does not analyze solutions for sparse graphs. He attributes the matrixmultiplication algorithm to the folklore. The Floyd-Warshall algorithm is due to Floyd [105], who based it on a theorem of Warshall [349] that describes how to compute the transitive closure of boolean matrices. Johnson’s algorithm is taken from [192].

Several researchers have given improved algorithms for computing shortest paths via matrix multiplication.

Fredman [111] shows how to solve the allpairs shortest paths problem using O.V 5=2/ comparisons between sums of edge

Notes for Chapter 25 weights and obtains an algorithm that runs in O.V 3.lg lg V= lg V /1=3/ time, which is slightly better than the running time of the Floyd-Warshall algorithm. Han [159] reduced the running time to O.V 3.lg lg V= lg V /5=4/. Another line of research demonstrates that we can apply algorithms for fast matrix multiplication (see the chapter notes for Chapter 4) to the all-pairs shortest paths problem. Let O.n!/ be the running time of the fastest algorithm for multiplying n 	 n matrices; currently ! < 2:376 [78]. Galil and Margalit [123, 124] and Seidel [308] designed algorithms that solve the all-pairs shortest paths problem in undirected, unweighted graphs in .V !p.V // time, where p.n/ denotes a particular function that is polylogarithmically bounded in n. In dense graphs, these algorithms are faster than the O.VE/ time needed to perform jV j breadth-ﬁrst searches. Several researchers have extended these results to give algorithms for solving the all-pairs shortest paths problem in undirected graphs in which the edge weights are integers in the range f1; 2; : : : ; W g. The asymptotically fastest such algorithm, by Shoshan and Zwick [316], runs in time O.W V !p.V W //.

Karger, Koller, and Phillips [196] and independently McGeoch [247] have given a time bound that depends on E, the set of edges in E that participate in some shortest path. Given a graph with nonnegative edge weights, their algorithms run in O.VE C V 2 lg V / time and improve upon running Dijkstra’s algorithm jV j times when jEj D o.E/.

Baswana, Hariharan, and Sen [33] examined decremental algorithms for maintaining all-pairs shortest paths and transitive-closure information.

Decremental algorithms allow a sequence of intermixed edge deletions and queries; by comparison, Problem 25-1, in which edges are inserted, asks for an incremental algorithm. The algorithms by Baswana, Hariharan, and Sen are randomized and, when a path exists, their transitive-closure algorithm can fail to report it with probability 1=nc for an arbitrary c > 0. The query times are O.1/ with high probability.

For transitive closure, the amortized time for each update is O.V 4=3 lg1=3 V /.

For all-pairs shortest paths, the update times depend on the queries. For queries just giving the shortest-path weights, the amortized time per update is O.V 3=E lg2 V /. To report the actual shortest path, the amortized update time is min.O.V 3=2p lg V /; O.V 3=E lg2 V //. Demetrescu and Italiano [84] showed how to handle update and query operations when edges are both inserted and deleted, as long as each given edge has a bounded range of possible values drawn from the real numbers.

Aho, Hopcroft, and Ullman [5] deﬁned an algebraic structure known as a “closed semiring,” which serves as a general framework for solving path problems in directed graphs. Both the Floyd-Warshall algorithm and the transitive-closure algorithm from Section 25.2 are instantiations of an all-pairs algorithm based on closed semirings. Maggs and Plotkin [240] showed how to ﬁnd minimum spanning trees using a closed semiring.
