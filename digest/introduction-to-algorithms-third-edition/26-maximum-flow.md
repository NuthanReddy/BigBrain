# 26 Maximum Flow

Just as we can model a road map as a directed graph in order to ﬁnd the shortest path from one point to another, we can also interpret a directed graph as a “ﬂow network” and use it to answer questions about material ﬂows. Imagine a material coursing through a system from a source, where the material is produced, to a sink, where it is consumed. The source produces the material at some steady rate, and the sink consumes the material at the same rate. The “ﬂow” of the material at any point in the system is intuitively the rate at which the material moves.

Flow networks can model many problems, including liquids ﬂowing through pipes, parts through assembly lines, current through electrical networks, and information through communication networks. We can think of each directed edge in a ﬂow network as a conduit for the material. Each conduit has a stated capacity, given as a maximum rate at which the material can ﬂow through the conduit, such as 200 gallons of liquid per hour through a pipe or 20 amperes of electrical current through a wire. Vertices are conduit junctions, and other than the source and sink, material ﬂows through the vertices without collecting in them. In other words, the rate at which material enters a vertex must equal the rate at which it leaves the vertex. We call this property “ﬂow conservation,” and it is equivalent to Kirchhoff’s current law when the material is electrical current. In the maximum-ﬂow problem, we wish to compute the greatest rate at which we can ship material from the source to the sink without violating any capacity constraints. It is one of the simplest problems concerning ﬂow networks and, as we shall see in this chapter, this problem can be solved by efﬁcient algorithms.

Moreover, we can adapt the basic techniques used in maximum-ﬂow algorithms to solve other network-ﬂow problems. This chapter presents two general methods for solving the maximum-ﬂow problem. Section 26.1 formalizes the notions of ﬂow networks and ﬂows, formally deﬁning the maximum-ﬂow problem. Section 26.2 describes the classical method of Ford and Fulkerson for ﬁnding maximum ﬂows. An application of this method,

## 26.1 Flow networks

ﬁnding a maximum matching in an undirected bipartite graph, appears in Section 26.3. Section 26.4 presents the push-relabel method, which underlies many of the fastest algorithms for network-ﬂow problems. Section 26.5 covers the “relabelto-front” algorithm, a particular implementation of the push-relabel method that runs in time O.V 3/. Although this algorithm is not the fastest algorithm known, it illustrates some of the techniques used in the asymptotically fastest algorithms, and it is reasonably efﬁcient in practice.

## 26.1 Flow networks

In this section, we give a graph-theoretic deﬁnition of ﬂow networks, discuss their properties, and deﬁne the maximum-ﬂow problem precisely. We also introduce some helpful notation.

Flow networks and ﬂows A ﬂow network G D .V; E/ is a directed graph in which each edge .u; / 2 E has a nonnegative capacity c.u; /  0. We further require that if E contains an edge .u; /, then there is no edge .; u/ in the reverse direction. (We shall see shortly how to work around this restriction.) If .u; / 62 E, then for convenience we deﬁne c.u; / D 0, and we disallow self-loops. We distinguish two vertices in a ﬂow network: a source s and a sink t. For convenience, we assume that each vertex lies on some path from the source to the sink. That is, for each vertex  2 V , the ﬂow network contains a path s ;  ; t. The graph is therefore connected and, since each vertex other than s has at least one entering edge, jEj  jV j  1.

Figure 26.1 shows an example of a ﬂow network. We are now ready to deﬁne ﬂows more formally. Let G D .V; E/ be a ﬂow network with a capacity function c. Let s be the source of the network, and let t be the sink. A ﬂow in G is a real-valued function f W V 	 V ! R that satisﬁes the following two properties:

Capacity constraint: For all u;  2 V , we require 0  f .u; /  c.u; /.

Flow conservation: For all u 2 V  fs; tg, we require X 2V f .; u/ D X 2V f .u; / :

When .u; / 62 E, there can be no ﬂow from u to , and f .u; / D 0.

s t Edmonton Calgary Saskatoon Regina Vancouver Winnipeg s t 11/16 12/12 15/20 7/7 4/9 1/4 8/13 11/14 4/4 (a) (b) v1 v1 v2 v2 v3 v3 v4 v4 Figure 26.1 (a) A ﬂow network G D .V; E/ for the Lucky Puck Company’s trucking problem. The Vancouver factory is the source s, and the Winnipeg warehouse is the sink t. The company ships pucks through intermediate cities, but only c.u; / crates per day can go from city u to city . Each edge is labeled with its capacity. (b) A ﬂow f in G with value jf j D 19. Each edge .u; / is labeled by f .u;/=c.u; /. The slash notation merely separates the ﬂow and capacity; it does not indicate division. We call the nonnegative quantity f .u; / the ﬂow from vertex u to vertex . The value jf j of a ﬂow f is deﬁned as jf j D X 2V f .s; /  X 2V f .; s/ ; (26.1) that is, the total ﬂow out of the source minus the ﬂow into the source. (Here, the jj notation denotes ﬂow value, not absolute value or cardinality.) Typically, a ﬂow network will not have any edges into the source, and the ﬂow into the source, given by the summation P 2V f .; s/, will be 0. We include it, however, because when we introduce residual networks later in this chapter, the ﬂow into the source will become signiﬁcant. In the maximum-ﬂow problem, we are given a ﬂow network G with source s and sink t, and we wish to ﬁnd a ﬂow of maximum value.

Before seeing an example of a network-ﬂow problem, let us brieﬂy explore the deﬁnition of ﬂow and the two ﬂow properties. The capacity constraint simply says that the ﬂow from one vertex to another must be nonnegative and must not exceed the given capacity. The ﬂow-conservation property says that the total ﬂow into a vertex other than the source or sink must equal the total ﬂow out of that vertex—informally, “ﬂow in equals ﬂow out.” An example of ﬂow A ﬂow network can model the trucking problem shown in Figure 26.1(a). The Lucky Puck Company has a factory (source s) in Vancouver that manufactures hockey pucks, and it has a warehouse (sink t) in Winnipeg that stocks them. Lucky

## 26.1 Flow networks

s t (a) (b) v1 v2 v3 v4 s t v1 v2 v3 v4 v′ Figure 26.2 Converting a network with antiparallel edges to an equivalent one with no antiparallel edges. (a) A ﬂow network containing both the edges .1; 2/ and .2; 1/. (b) An equivalent network with no antiparallel edges. We add the new vertex 0, and we replace edge .1; 2/ by the pair of edges .1; 0/ and .0; 2/, both with the same capacity as .1; 2/.

Puck leases space on trucks from another ﬁrm to ship the pucks from the factory to the warehouse. Because the trucks travel over speciﬁed routes (edges) between cities (vertices) and have a limited capacity, Lucky Puck can ship at most c.u; / crates per day between each pair of cities u and  in Figure 26.1(a). Lucky Puck has no control over these routes and capacities, and so the company cannot alter the ﬂow network shown in Figure 26.1(a). They need to determine the largest number p of crates per day that they can ship and then to produce this amount, since there is no point in producing more pucks than they can ship to their warehouse.

Lucky Puck is not concerned with how long it takes for a given puck to get from the factory to the warehouse; they care only that p crates per day leave the factory and p crates per day arrive at the warehouse. We can model the “ﬂow” of shipments with a ﬂow in this network because the number of crates shipped per day from one city to another is subject to a capacity constraint. Additionally, the model must obey ﬂow conservation, for in a steady state, the rate at which pucks enter an intermediate city must equal the rate at which they leave. Otherwise, crates would accumulate at intermediate cities.

Modeling problems with antiparallel edges Suppose that the trucking ﬁrm offered Lucky Puck the opportunity to lease space for 10 crates in trucks going from Edmonton to Calgary. It would seem natural to add this opportunity to our example and form the network shown in Figure 26.2(a). This network suffers from one problem, however: it violates our original assumption that if an edge .1; 2/ 2 E, then .2; 1/ 62 E. We call the two edges .1; 2/ and .2; 1/ antiparallel. Thus, if we wish to model a ﬂow problem with antiparallel edges, we must transform the network into an equivalent one containing no

antiparallel edges. Figure 26.2(b) displays this equivalent network. We choose one of the two antiparallel edges, in this case .1; 2/, and split it by adding a new vertex 0 and replacing edge .1; 2/ with the pair of edges .1; 0/ and .0; 2/. We also set the capacity of both new edges to the capacity of the original edge. The resulting network satisﬁes the property that if an edge is in the network, the reverse edge is not. Exercise 26.1-1 asks you to prove that the resulting network is equivalent to the original one. Thus, we see that a real-world ﬂow problem might be most naturally modeled by a network with antiparallel edges. It will be convenient to disallow antiparallel edges, however, and so we have a straightforward way to convert a network containing antiparallel edges into an equivalent one with no antiparallel edges.

Networks with multiple sources and sinks A maximum-ﬂow problem may have several sources and sinks, rather than just one of each. The Lucky Puck Company, for example, might actually have a set of m factories fs1; s2; : : : ; smg and a set of n warehouses ft1; t2; : : : ; tng, as shown in Figure 26.3(a). Fortunately, this problem is no harder than ordinary maximum ﬂow. We can reduce the problem of determining a maximum ﬂow in a network with multiple sources and multiple sinks to an ordinary maximum-ﬂow problem. Figure 26.3(b) shows how to convert the network from (a) to an ordinary ﬂow network with only a single source and a single sink. We add a supersource s and add a directed edge .s; si/ with capacity c.s; si/ D 1 for each i D 1; 2; : : : ; m. We also create a new supersink t and add a directed edge .ti; t/ with capacity c.ti; t/ D 1 for each i D 1; 2; : : : ; n. Intuitively, any ﬂow in the network in (a) corresponds to a ﬂow in the network in (b), and vice versa. The single source s simply provides as much ﬂow as desired for the multiple sources si, and the single sink t likewise consumes as much ﬂow as desired for the multiple sinks ti. Exercise 26.1-2 asks you to prove formally that the two problems are equivalent.

## Exercises

26.1-1 Show that splitting an edge in a ﬂow network yields an equivalent network. More formally, suppose that ﬂow network G contains edge .u; /, and we create a new ﬂow network G0 by creating a new vertex x and replacing .u; / by new edges .u; x/ and .x; / with c.u; x/ D c.x; / D c.u; /. Show that a maximum ﬂow in G0 has the same value as a maximum ﬂow in G.

## 26.1 Flow networks

(a) ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ s1 s1 s2 s2 s3 s3 s4 s4 s5 s5 t1 t1 t2 t2 t3 t3 (b) s t Figure 26.3 Converting a multiple-source, multiple-sink maximum-ﬂow problem into a problem with a single source and a single sink. (a) A ﬂow network with ﬁve sources S D fs1; s2; s3; s4; s5g and three sinks T D ft1; t2; t3g. (b) An equivalent single-source, single-sink ﬂow network. We add a supersource s and an edge with inﬁnite capacity from s to each of the multiple sources. We also add a supersink t and an edge with inﬁnite capacity from each of the multiple sinks to t. 26.1-2 Extend the ﬂow properties and deﬁnitions to the multiple-source, multiple-sink problem. Show that any ﬂow in a multiple-source, multiple-sink ﬂow network corresponds to a ﬂow of identical value in the single-source, single-sink network obtained by adding a supersource and a supersink, and vice versa. 26.1-3 Suppose that a ﬂow network G D .V; E/ violates the assumption that the network contains a path s ;  ; t for all vertices  2 V . Let u be a vertex for which there is no path s ; u ; t. Show that there must exist a maximum ﬂow f in G such that f .u; / D f .; u/ D 0 for all vertices  2 V .

26.1-4 Let f be a ﬂow in a network, and let ˛ be a real number. The scalar ﬂow product, denoted ˛f , is a function from V 	 V to R deﬁned by .˛f /.u; / D ˛  f .u; / :

Prove that the ﬂows in a network form a convex set. That is, show that if f1 and f2 are ﬂows, then so is ˛f1 C .1  ˛/f2 for all ˛ in the range 0  ˛  1. 26.1-5 State the maximum-ﬂow problem as a linear-programming problem. 26.1-6 Professor Adam has two children who, unfortunately, dislike each other. The problem is so severe that not only do they refuse to walk to school together, but in fact each one refuses to walk on any block that the other child has stepped on that day. The children have no problem with their paths crossing at a corner. Fortunately both the professor’s house and the school are on corners, but beyond that he is not sure if it is going to be possible to send both of his children to the same school. The professor has a map of his town. Show how to formulate the problem of determining whether both his children can go to the same school as a maximum-ﬂow problem. 26.1-7 Suppose that, in addition to edge capacities, a ﬂow network has vertex capacities. That is each vertex  has a limit l./ on how much ﬂow can pass though . Show how to transform a ﬂow network G D .V; E/ with vertex capacities into an equivalent ﬂow network G0 D .V 0; E0/ without vertex capacities, such that a maximum ﬂow in G0 has the same value as a maximum ﬂow in G. How many vertices and edges does G0 have?

## 26.2 The Ford-Fulkerson method

This section presents the Ford-Fulkerson method for solving the maximum-ﬂow problem. We call it a “method” rather than an “algorithm” because it encompasses several implementations with differing running times. The Ford-Fulkerson method depends on three important ideas that transcend the method and are relevant to many ﬂow algorithms and problems: residual networks, augmenting paths, and cuts. These ideas are essential to the important max-ﬂow min-cut theorem (Theorem 26.6), which characterizes the value of a maximum ﬂow in terms of cuts of

## 26.2 The Ford-Fulkerson method

the ﬂow network. We end this section by presenting one speciﬁc implementation of the Ford-Fulkerson method and analyzing its running time. The Ford-Fulkerson method iteratively increases the value of the ﬂow. We start with f .u; / D 0 for all u;  2 V , giving an initial ﬂow of value 0. At each iteration, we increase the ﬂow value in G by ﬁnding an “augmenting path” in an associated “residual network” Gf . Once we know the edges of an augmenting path in Gf , we can easily identify speciﬁc edges in G for which we can change the ﬂow so that we increase the value of the ﬂow. Although each iteration of the Ford-Fulkerson method increases the value of the ﬂow, we shall see that the ﬂow on any particular edge of G may increase or decrease; decreasing the ﬂow on some edges may be necessary in order to enable an algorithm to send more ﬂow from the source to the sink. We repeatedly augment the ﬂow until the residual network has no more augmenting paths. The max-ﬂow min-cut theorem will show that upon termination, this process yields a maximum ﬂow.

FORD-FULKERSON-METHOD.G; s; t/ initialize ﬂow f to 0 while there exists an augmenting path p in the residual network Gf augment ﬂow f along p return f In order to implement and analyze the Ford-Fulkerson method, we need to introduce several additional concepts.

Residual networks Intuitively, given a ﬂow network G and a ﬂow f , the residual network Gf consists of edges with capacities that represent how we can change the ﬂow on edges of G. An edge of the ﬂow network can admit an amount of additional ﬂow equal to the edge’s capacity minus the ﬂow on that edge. If that value is positive, we place that edge into Gf with a “residual capacity” of cf .u; / D c.u; /  f .u; /. The only edges of G that are in Gf are those that can admit more ﬂow; those edges .u; / whose ﬂow equals their capacity have cf .u; / D 0, and they are not in Gf . The residual network Gf may also contain edges that are not in G, however. As an algorithm manipulates the ﬂow, with the goal of increasing the total ﬂow, it might need to decrease the ﬂow on a particular edge. In order to represent a possible decrease of a positive ﬂow f .u; / on an edge in G, we place an edge .; u/ into Gf with residual capacity cf .; u/ D f .u; /—that is, an edge that can admit ﬂow in the opposite direction to .u; /, at most canceling out the ﬂow on .u; /. These reverse edges in the residual network allow an algorithm to send back ﬂow

it has already sent along an edge. Sending ﬂow back along an edge is equivalent to decreasing the ﬂow on the edge, which is a necessary operation in many algorithms.

More formally, suppose that we have a ﬂow network G D .V; E/ with source s and sink t. Let f be a ﬂow in G, and consider a pair of vertices u;  2 V . We deﬁne the residual capacity cf .u; / by cf .u; / D  c.u; /  f .u; / if .u; / 2 E ; f .; u/ if .; u/ 2 E ; otherwise : (26.2) Because of our assumption that .u; / 2 E implies .; u/ 62 E, exactly one case in equation (26.2) applies to each ordered pair of vertices. As an example of equation (26.2), if c.u; / D 16 and f .u; / D 11, then we can increase f .u; / by up to cf .u; / D 5 units before we exceed the capacity constraint on edge .u; /. We also wish to allow an algorithm to return up to 11 units of ﬂow from  to u, and hence cf .; u/ D 11.

Given a ﬂow network G D .V; E/ and a ﬂow f , the residual network of G induced by f is Gf D .V; Ef /, where Ef D f.u; / 2 V 	 V W cf .u; / > 0g : (26.3) That is, as promised above, each edge of the residual network, or residual edge, can admit a ﬂow that is greater than 0. Figure 26.4(a) repeats the ﬂow network G and ﬂow f of Figure 26.1(b), and Figure 26.4(b) shows the corresponding residual network Gf . The edges in Ef are either edges in E or their reversals, and thus jEf j  2 jEj :

Observe that the residual network Gf is similar to a ﬂow network with capacities given by cf . It does not satisfy our deﬁnition of a ﬂow network because it may contain both an edge .u; / and its reversal .; u/. Other than this difference, a residual network has the same properties as a ﬂow network, and we can deﬁne a ﬂow in the residual network as one that satisﬁes the deﬁnition of a ﬂow, but with respect to capacities cf in the network Gf .

A ﬂow in a residual network provides a roadmap for adding ﬂow to the original ﬂow network. If f is a ﬂow in G and f 0 is a ﬂow in the corresponding residual network Gf , we deﬁne f " f 0, the augmentation of ﬂow f by f 0, to be a function from V 	 V to R, deﬁned by .f " f 0/.u; / D ( f .u; / C f 0.u; /  f 0.; u/ if .u; / 2 E ; otherwise : (26.4)

## 26.2 The Ford-Fulkerson method

s t s t 11/16 12/12 19/20 7/7 1/4 12/13 11/14 4/4 (b) (c) s t 11/16 12/12 15/20 7/7 4/9 1/4 8/13 11/14 4/4 (d) s t v1 v1 v1 v1 v2 v2 v2 v2 v3 v3 v3 v3 v4 v4 v4 v4 (a) Figure 26.4 (a) The ﬂow network G and ﬂow f of Figure 26.1(b). (b) The residual network Gf with augmenting path p shaded; its residual capacity is cf .p/ D cf .2; 3/ D 4. Edges with residual capacity equal to 0, such as .1; 3/, are not shown, a convention we follow in the remainder of this section. (c) The ﬂow in G that results from augmenting along path p by its residual capacity 4.

Edges carrying no ﬂow, such as .3; 2/, are labeled only by their capacity, another convention we follow throughout. (d) The residual network induced by the ﬂow in (c). The intuition behind this deﬁnition follows the deﬁnition of the residual network. We increase the ﬂow on .u; / by f 0.u; / but decrease it by f 0.; u/ because pushing ﬂow on the reverse edge in the residual network signiﬁes decreasing the ﬂow in the original network. Pushing ﬂow on the reverse edge in the residual network is also known as cancellation. For example, if we send 5 crates of hockey pucks from u to  and send 2 crates from  to u, we could equivalently (from the perspective of the ﬁnal result) just send 3 creates from u to  and none from  to u.

Cancellation of this type is crucial for any maximum-ﬂow algorithm.

> **Lemma 26.1**

Let G D .V; E/ be a ﬂow network with source s and sink t, and let f be a ﬂow in G. Let Gf be the residual network of G induced by f , and let f 0 be a ﬂow in Gf . Then the function f " f 0 deﬁned in equation (26.4) is a ﬂow in G with value jf " f 0j D jf j C jf 0j.

Proof We ﬁrst verify that f " f 0 obeys the capacity constraint for each edge in E and ﬂow conservation at each vertex in V  fs; tg.

For the capacity constraint, ﬁrst observe that if .u; / 2 E, then cf .; u/ D f .u; /. Therefore, we have f 0.; u/  cf .; u/ D f .u; /, and hence .f " f 0/.u; / D f .u; / C f 0.u; /  f 0.; u/ (by equation (26.4))  f .u; / C f 0.u; /  f .u; / (because f 0.; u/  f .u; /) D f 0.u; /  0 : In addition, .f " f 0/.u; / D f .u; / C f 0.u; /  f 0.; u/ (by equation (26.4))  f .u; / C f 0.u; / (because ﬂows are nonnegative)  f .u; / C cf .u; / (capacity constraint) D f .u; / C c.u; /  f .u; / (deﬁnition of cf ) D c.u; / :

For ﬂow conservation, because both f and f 0 obey ﬂow conservation, we have that for all u 2 V  fs; tg, X 2V .f " f 0/.u; / D X 2V .f .u; / C f 0.u; /  f 0.; u// D X 2V f .u; / C X 2V f 0.u; /  X 2V f 0.; u/ D X 2V f .; u/ C X 2V f 0.; u/  X 2V f 0.u; / D X 2V .f .; u/ C f 0.; u/  f 0.u; // D X 2V .f " f 0/.; u/ ; where the third line follows from the second by ﬂow conservation.

Finally, we compute the value of f " f 0. Recall that we disallow antiparallel edges in G (but not in Gf ), and hence for each vertex  2 V , we know that there can be an edge .s; / or .; s/, but never both. We deﬁne V1 D f W .s; / 2 Eg to be the set of vertices with edges from s, and V2 D f W .; s/ 2 Eg to be the set of vertices with edges to s. We have V1 [ V2  V and, because we disallow antiparallel edges, V1 \ V2 D ;. We now compute jf " f 0j D X 2V .f " f 0/ .s; /  X 2V .f " f 0/ .; s/ D X 2V1 .f " f 0/ .s; /  X 2V2 .f " f 0/ .; s/ ; (26.5)

## 26.2 The Ford-Fulkerson method

where the second line follows because .f " f 0/.w; x/ is 0 if .w; x/ 62 E. We now apply the deﬁnition of f " f 0 to equation (26.5), and then reorder and group terms to obtain jf " f 0j D X 2V1 .f .s; / C f 0.s; /  f 0.; s//  X 2V2 .f .; s/ C f 0.; s/  f 0.s; // D X 2V1 f .s; / C X 2V1 f 0.s; /  X 2V1 f 0.; s/  X 2V2 f .; s/  X 2V2 f 0.; s/ C X 2V2 f 0.s; / D X 2V1 f .s; /  X 2V2 f .; s/ C X 2V1 f 0.s; / C X 2V2 f 0.s; /  X 2V1 f 0.; s/  X 2V2 f 0.; s/ D X 2V1 f .s; /  X 2V2 f .; s/ C X 2V1[V2 f 0.s; /  X 2V1[V2 f 0.; s/ : (26.6) In equation (26.6), we can extend all four summations to sum over V , since each additional term has value 0. (Exercise 26.2-1 asks you to prove this formally.) We thus have jf " f 0j D X 2V f .s; /  X 2V f .; s/ C X 2V f 0.s; /  X 2V f 0.; s/ (26.7) D jf j C jf 0j :

Augmenting paths Given a ﬂow network G D .V; E/ and a ﬂow f , an augmenting path p is a simple path from s to t in the residual network Gf . By the deﬁnition of the residual network, we may increase the ﬂow on an edge .u; / of an augmenting path by up to cf .u; / without violating the capacity constraint on whichever of .u; / and .; u/ is in the original ﬂow network G. The shaded path in Figure 26.4(b) is an augmenting path. Treating the residual network Gf in the ﬁgure as a ﬂow network, we can increase the ﬂow through each edge of this path by up to 4 units without violating a capacity constraint, since the smallest residual capacity on this path is cf .2; 3/ D 4. We call the maximum amount by which we can increase the ﬂow on each edge in an augmenting path p the residual capacity of p, given by cf .p/ D min fcf .u; / W .u; / is on pg :

The following lemma, whose proof we leave as Exercise 26.2-7, makes the above argument more precise.

> **Lemma 26.2**

Let G D .V; E/ be a ﬂow network, let f be a ﬂow in G, and let p be an augmenting path in Gf . Deﬁne a function fp W V 	 V ! R by fp.u; / D ( cf .p/ if .u; / is on p ; otherwise : (26.8) Then, fp is a ﬂow in Gf with value jfpj D cf .p/ > 0. The following corollary shows that if we augment f by fp, we get another ﬂow in G whose value is closer to the maximum. Figure 26.4(c) shows the result of augmenting the ﬂow f from Figure 26.4(a) by the ﬂow fp in Figure 26.4(b), and Figure 26.4(d) shows the ensuing residual network.

> **Corollary 26.3**

Let G D .V; E/ be a ﬂow network, let f be a ﬂow in G, and let p be an augmenting path in Gf . Let fp be deﬁned as in equation (26.8), and suppose that we augment f by fp. Then the function f " fp is a ﬂow in G with value jf " fpj D jf j C jfpj > jf j.

Proof Immediate from Lemmas 26.1 and 26.2.

Cuts of ﬂow networks The Ford-Fulkerson method repeatedly augments the ﬂow along augmenting paths until it has found a maximum ﬂow. How do we know that when the algorithm terminates, we have actually found a maximum ﬂow? The max-ﬂow min-cut theorem, which we shall prove shortly, tells us that a ﬂow is maximum if and only if its residual network contains no augmenting path. To prove this theorem, though, we must ﬁrst explore the notion of a cut of a ﬂow network.

A cut .S; T / of ﬂow network G D .V; E/ is a partition of V into S and T D V  S such that s 2 S and t 2 T . (This deﬁnition is similar to the definition of “cut” that we used for minimum spanning trees in Chapter 23, except that here we are cutting a directed graph rather than an undirected graph, and we insist that s 2 S and t 2 T .) If f is a ﬂow, then the net ﬂow f .S; T / across the cut .S; T / is deﬁned to be f .S; T / D X u2S X 2T f .u; /  X u2S X 2T f .; u/ : (26.9)

## 26.2 The Ford-Fulkerson method

s t 11/16 12/12 15/20 7/7 4/9 1/4 8/13 11/14 4/4 S T v4 v3 v1 v2 Figure 26.5 A cut .S; T / in the ﬂow network of Figure 26.1(b), where S D fs; 1; 2g and T D f3; 4; tg. The vertices in S are black, and the vertices in T are white. The net ﬂow across .S; T / is f .S; T / D 19, and the capacity is c.S; T / D 26. The capacity of the cut .S; T / is c.S; T / D X u2S X 2T c.u; / : (26.10) A minimum cut of a network is a cut whose capacity is minimum over all cuts of the network. The asymmetry between the deﬁnitions of ﬂow and capacity of a cut is intentional and important. For capacity, we count only the capacities of edges going from S to T , ignoring edges in the reverse direction. For ﬂow, we consider the ﬂow going from S to T minus the ﬂow going in the reverse direction from T to S. The reason for this difference will become clear later in this section.

Figure 26.5 shows the cut .fs; 1; 2g ; f3; 4; tg/ in the ﬂow network of Figure 26.1(b). The net ﬂow across this cut is f .1; 3/ C f .2; 4/  f .3; 2/ D 12 C 11  4 D 19 ; and the capacity of this cut is c.1; 3/ C c.2; 4/ D 12 C 14 D 26 : The following lemma shows that, for a given ﬂow f , the net ﬂow across any cut is the same, and it equals jf j, the value of the ﬂow.

> **Lemma 26.4**

Let f be a ﬂow in a ﬂow network G with source s and sink t, and let .S; T / be any cut of G. Then the net ﬂow across .S; T / is f .S; T / D jf j.

Proof We can rewrite the ﬂow-conservation condition for any node u 2 V fs; tg as X 2V f .u; /  X 2V f .; u/ D 0 : (26.11) Taking the deﬁnition of jf j from equation (26.1) and adding the left-hand side of equation (26.11), which equals 0, summed over all vertices in S  fsg, gives jf j D X 2V f .s; /  X 2V f .; s/ C X u2Sfsg X 2V f .u; /  X 2V f .; u/ ! :

Expanding the right-hand summation and regrouping terms yields jf j D X 2V f .s; /  X 2V f .; s/ C X u2Sfsg X 2V f .u; /  X u2Sfsg X 2V f .; u/ D X 2V

f .s; / C X u2Sfsg f .u; / !  X 2V

f .; s/ C X u2Sfsg f .; u/ !

D X 2V X u2S f .u; /  X 2V X u2S f .; u/ :

Because V D S [ T and S \ T D ;, we can split each summation over V into summations over S and T to obtain jf j D X 2S X u2S f .u; / C X 2T X u2S f .u; /  X 2S X u2S f .; u/  X 2T X u2S f .; u/ D X 2T X u2S f .u; /  X 2T X u2S f .; u/ C X 2S X u2S f .u; /  X 2S X u2S f .; u/ ! : The two summations within the parentheses are actually the same, since for all vertices x; y 2 V , the term f .x; y/ appears once in each summation. Hence, these summations cancel, and we have jf j D X u2S X 2T f .u; /  X u2S X 2T f .; u/ D f .S; T / :

A corollary to Lemma 26.4 shows how we can use cut capacities to bound the value of a ﬂow.

## 26.2 The Ford-Fulkerson method

> **Corollary 26.5**

The value of any ﬂow f in a ﬂow network G is bounded from above by the capacity of any cut of G.

Proof Let .S; T / be any cut of G and let f be any ﬂow. By Lemma 26.4 and the capacity constraint, jf j D f .S; T / D X u2S X 2T f .u; /  X u2S X 2T f .; u/  X u2S X 2T f .u; /  X u2S X 2T c.u; / D c.S; T / :

> **Corollary 26.5 yields the immediate consequence that the value of a maximum**

ﬂow in a network is bounded from above by the capacity of a minimum cut of the network. The important max-ﬂow min-cut theorem, which we now state and prove, says that the value of a maximum ﬂow is in fact equal to the capacity of a minimum cut.

> **Theorem 26.6 (Max-ﬂow min-cut theorem)**

If f is a ﬂow in a ﬂow network G D .V; E/ with source s and sink t, then the following conditions are equivalent: 1. f is a maximum ﬂow in G. 2. The residual network Gf contains no augmenting paths. 3. jf j D c.S; T / for some cut .S; T / of G.

Proof .1/ ) .2/: Suppose for the sake of contradiction that f is a maximum ﬂow in G but that Gf has an augmenting path p. Then, by Corollary 26.3, the ﬂow found by augmenting f by fp, where fp is given by equation (26.8), is a ﬂow in G with value strictly greater than jf j, contradicting the assumption that f is a maximum ﬂow. .2/ ) .3/: Suppose that Gf has no augmenting path, that is, that Gf contains no path from s to t. Deﬁne S D f 2 V W there exists a path from s to  in Gf g and T D V  S. The partition .S; T / is a cut: we have s 2 S trivially and t 62 S because there is no path from s to t in Gf . Now consider a pair of vertices

u 2 S and  2 T . If .u; / 2 E, we must have f .u; / D c.u; /, since otherwise .u; / 2 Ef , which would place  in set S. If .; u/ 2 E, we must have f .; u/ D 0, because otherwise cf .u; / D f .; u/ would be positive and we would have .u; / 2 Ef , which would place  in S. Of course, if neither .u; / nor .; u/ is in E, then f .u; / D f .; u/ D 0. We thus have f .S; T / D X u2S X 2T f .u; /  X 2T X u2S f .; u/ D X u2S X 2T c.u; /  X 2T X u2S D c.S; T / : By Lemma 26.4, therefore, jf j D f .S; T / D c.S; T /. .3/ ) .1/: By Corollary 26.5, jf j  c.S; T / for all cuts .S; T /. The condition jf j D c.S; T / thus implies that f is a maximum ﬂow. The basic Ford-Fulkerson algorithm In each iteration of the Ford-Fulkerson method, we ﬁnd some augmenting path p and use p to modify the ﬂow f . As Lemma 26.2 and Corollary 26.3 suggest, we replace f by f " fp, obtaining a new ﬂow whose value is jf j C jfpj. The following implementation of the method computes the maximum ﬂow in a ﬂow network G D .V; E/ by updating the ﬂow attribute .u; /:f for each edge .u; / 2 E.1 If .u; / 62 E, we assume implicitly that .u; /:f D 0. We also assume that we are given the capacities c.u; / along with the ﬂow network, and c.u; / D 0 if .u; / 62 E. We compute the residual capacity cf .u; / in accordance with the formula (26.2). The expression cf .p/ in the code is just a temporary variable that stores the residual capacity of the path p.

FORD-FULKERSON.G; s; t/ for each edge .u; / 2 G:E .u; /:f D 0 while there exists a path p from s to t in the residual network Gf cf .p/ D min fcf .u; / W .u; / is in pg for each edge .u; / in p if .u; / 2 E .u; /:f D .u; /:f C cf .p/ else .; u/:f D .; u/:f  cf .p/ 1Recall from Section 22.1 that we represent an attribute f for edge .u; / with the same style of notation—.u; /:f —that we use for an attribute of any other object.

## 26.2 The Ford-Fulkerson method

The FORD-FULKERSON algorithm simply expands on the FORD-FULKERSON- METHOD pseudocode given earlier. Figure 26.6 shows the result of each iteration in a sample run. Lines 1–2 initialize the ﬂow f to 0. The while loop of lines 3–8 repeatedly ﬁnds an augmenting path p in Gf and augments ﬂow f along p by the residual capacity cf .p/. Each residual edge in path p is either an edge in the original network or the reversal of an edge in the original network. Lines 6–8 update the ﬂow in each case appropriately, adding ﬂow when the residual edge is an original edge and subtracting it otherwise. When no augmenting paths exist, the ﬂow f is a maximum ﬂow. Analysis of Ford-Fulkerson The running time of FORD-FULKERSON depends on how we ﬁnd the augmenting path p in line 3. If we choose it poorly, the algorithm might not even terminate: the value of the ﬂow will increase with successive augmentations, but it need not even converge to the maximum ﬂow value.2 If we ﬁnd the augmenting path by using a breadth-ﬁrst search (which we saw in Section 22.2), however, the algorithm runs in polynomial time. Before proving this result, we obtain a simple bound for the case in which we choose the augmenting path arbitrarily and all capacities are integers. In practice, the maximum-ﬂow problem often arises with integral capacities. If the capacities are rational numbers, we can apply an appropriate scaling transformation to make them all integral. If f  denotes a maximum ﬂow in the transformed network, then a straightforward implementation of FORD-FULKERSON executes the while loop of lines 3–8 at most jf j times, since the ﬂow value increases by at least one unit in each iteration. We can perform the work done within the while loop efﬁciently if we implement the ﬂow network G D .V; E/ with the right data structure and ﬁnd an augmenting path by a linear-time algorithm. Let us assume that we keep a data structure corresponding to a directed graph G0 D .V; E0/, where E0 D f.u; / W .u; / 2 E or .; u/ 2 Eg. Edges in the network G are also edges in G0, and therefore we can easily maintain capacities and ﬂows in this data structure. Given a ﬂow f on G, the edges in the residual network Gf consist of all edges .u; / of G0 such that cf .u; / > 0, where cf conforms to equation (26.2). The time to ﬁnd a path in a residual network is therefore O.V C E0/ D O.E/ if we use either depth-ﬁrst search or breadth-ﬁrst search. Each iteration of the while loop thus takes O.E/ time, as does the initialization in lines 1–2, making the total running time of the FORD-FULKERSON algorithm O.E jf j/. 2The Ford-Fulkerson method might fail to terminate only if edge capacities are irrational numbers.

4/4 v1 s t v1 s t 4/16 4/12 4/9 4/14 4/4 s t v1 v1 s t 4/16 8/12 4/20 4/9 4/13 4/14 4/4 s t v1 v1 s t 8/16 8/12 8/20 4/13 4/14 4/4 v2 v2 v2 v2 v2 v2 v3 v3 v3 v3 v3 v3 v4 v4 v4 v4 v4 v4 (b) (a) (c) Figure 26.6 The execution of the basic Ford-Fulkerson algorithm. (a)–(e) Successive iterations of the while loop. The left side of each part shows the residual network Gf from line 3 with a shaded augmenting path p. The right side of each part shows the new ﬂow f that results from augmenting f by fp. The residual network in (a) is the input network G.

When the capacities are integral and the optimal ﬂow value jf j is small, the running time of the Ford-Fulkerson algorithm is good. Figure 26.7(a) shows an example of what can happen on a simple ﬂow network for which jf j is large. A maximum ﬂow in this network has value 2,000,000: 1,000,000 units of ﬂow traverse the path s ! u ! t, and another 1,000,000 units traverse the path s !  ! t. If the ﬁrst augmenting path found by FORD-FULKERSON is s ! u !  ! t, shown in Figure 26.7(a), the ﬂow has value 1 after the ﬁrst iteration. The resulting residual network appears in Figure 26.7(b). If the second iteration ﬁnds the augmenting path s !  ! u ! t, as shown in Figure 26.7(b), the ﬂow then has value 2.

Figure 26.7(c) shows the resulting residual network. We can continue, choosing the augmenting path s ! u !  ! t in the odd-numbered iterations and the augmenting path s !  ! u ! t in the even-numbered iterations. We would perform a total of 2,000,000 augmentations, increasing the ﬂow value by only 1 unit in each.

## 26.2 The Ford-Fulkerson method

s t v1 s t 8/16 8/12 15/20 7/7 11/13 11/14 4/4 v1 s t v2 v3 v3 v3 v4 v4 v4 (d) (f) s t v1 s t 12/16 12/12 19/20 7/7 11/13 11/14 4/4 v1 v2 v3 v3 v4 v4 (e) v2 v2 v1 v2 Figure 26.6, continued (f) The residual network at the last while loop test. It has no augmenting paths, and the ﬂow f shown in (e) is therefore a maximum ﬂow. The value of the maximum ﬂow found is 23. The Edmonds-Karp algorithm We can improve the bound on FORD-FULKERSON by ﬁnding the augmenting path p in line 3 with a breadth-ﬁrst search. That is, we choose the augmenting path as a shortest path from s to t in the residual network, where each edge has unit distance (weight). We call the Ford-Fulkerson method so implemented the Edmonds-Karp algorithm. We now prove that the Edmonds-Karp algorithm runs in O.VE2/ time. The analysis depends on the distances to vertices in the residual network Gf . The following lemma uses the notation ıf .u; / for the shortest-path distance from u to  in Gf , where each edge has unit distance.

> **Lemma 26.7**

If the Edmonds-Karp algorithm is run on a ﬂow network G D .V; E/ with source s and sink t, then for all vertices  2 V  fs; tg, the shortest-path distance ıf .s; / in the residual network Gf increases monotonically with each ﬂow augmentation.

999,999 999,999 s t 1,000,000 1,000,000 1,000,000 1,000,000 999,999 999,999 u v s t 1,000,000 1,000,000 u v 999,999 999,999 s t u v (a) (b) (c) Figure 26.7 (a) A ﬂow network for which FORD-FULKERSON can take ‚.E jf j/ time, where f  is a maximum ﬂow, shown here with jf j D 2,000,000. The shaded path is an augmenting path with residual capacity 1. (b) The resulting residual network, with another augmenting path whose residual capacity is 1. (c) The resulting residual network.

Proof We will suppose that for some vertex  2 V  fs; tg, there is a ﬂow augmentation that causes the shortest-path distance from s to  to decrease, and then we will derive a contradiction. Let f be the ﬂow just before the ﬁrst augmentation that decreases some shortest-path distance, and let f 0 be the ﬂow just afterward.

Let  be the vertex with the minimum ıf 0.s; / whose distance was decreased by the augmentation, so that ıf 0.s; / < ıf .s; /. Let p D s ; u !  be a shortest path from s to  in Gf 0, so that .u; / 2 Ef 0 and ıf 0.s; u/ D ıf 0.s; /  1 : (26.12) Because of how we chose , we know that the distance of vertex u from the source s did not decrease, i.e., ıf 0.s; u/  ıf .s; u/ : (26.13) We claim that .u; / 62 Ef . Why? If we had .u; / 2 Ef , then we would also have ıf .s; /  ıf .s; u/ C 1 (by Lemma 24.10, the triangle inequality)  ıf 0.s; u/ C 1 (by inequality (26.13)) D ıf 0.s; / (by equation (26.12)) , which contradicts our assumption that ıf 0.s; / < ıf .s; /.

How can we have .u; / 62 Ef and .u; / 2 Ef 0? The augmentation must have increased the ﬂow from  to u. The Edmonds-Karp algorithm always augments ﬂow along shortest paths, and therefore the shortest path from s to u in Gf has .; u/ as its last edge. Therefore, ıf .s; / D ıf .s; u/  1  ıf 0.s; u/  1 (by inequality (26.13)) D ıf 0.s; /  2 (by equation (26.12)) ,

## 26.2 The Ford-Fulkerson method

which contradicts our assumption that ıf 0.s; / < ıf .s; /. We conclude that our assumption that such a vertex  exists is incorrect. The next theorem bounds the number of iterations of the Edmonds-Karp algorithm.

> **Theorem 26.8**

If the Edmonds-Karp algorithm is run on a ﬂow network G D .V; E/ with source s and sink t, then the total number of ﬂow augmentations performed by the algorithm is O.VE/.

Proof We say that an edge .u; / in a residual network Gf is critical on an augmenting path p if the residual capacity of p is the residual capacity of .u; /, that is, if cf .p/ D cf .u; /. After we have augmented ﬂow along an augmenting path, any critical edge on the path disappears from the residual network. Moreover, at least one edge on any augmenting path must be critical. We will show that each of the jEj edges can become critical at most jV j =2 times.

Let u and  be vertices in V that are connected by an edge in E. Since augmenting paths are shortest paths, when .u; / is critical for the ﬁrst time, we have ıf .s; / D ıf .s; u/ C 1 : Once the ﬂow is augmented, the edge .u; / disappears from the residual network. It cannot reappear later on another augmenting path until after the ﬂow from u to  is decreased, which occurs only if .; u/ appears on an augmenting path. If f 0 is the ﬂow in G when this event occurs, then we have ıf 0.s; u/ D ıf 0.s; / C 1 :

Since ıf .s; /  ıf 0.s; / by Lemma 26.7, we have ıf 0.s; u/ D ıf 0.s; / C 1  ıf .s; / C 1 D ıf .s; u/ C 2 :

Consequently, from the time .u; / becomes critical to the time when it next becomes critical, the distance of u from the source increases by at least 2. The distance of u from the source is initially at least 0. The intermediate vertices on a shortest path from s to u cannot contain s, u, or t (since .u; / on an augmenting path implies that u ¤ t). Therefore, until u becomes unreachable from the source, if ever, its distance is at most jV j  2. Thus, after the ﬁrst time that .u; / becomes critical, it can become critical at most .jV j  2/=2 D jV j =2  1 times more, for a total of at most jV j =2 times. Since there are O.E/ pairs of vertices that can have an edge between them in a residual network, the total number of critical edges during

the entire execution of the Edmonds-Karp algorithm is O.VE/. Each augmenting path has at least one critical edge, and hence the theorem follows.

Because we can implement each iteration of FORD-FULKERSON in O.E/ time when we ﬁnd the augmenting path by breadth-ﬁrst search, the total running time of the Edmonds-Karp algorithm is O.VE2/. We shall see that push-relabel algorithms can yield even better bounds. The algorithm of Section 26.4 gives a method for achieving an O.V 2E/ running time, which forms the basis for the O.V 3/-time algorithm of Section 26.5.

## Exercises

26.2-1 Prove that the summations in equation (26.6) equal the summations in equation (26.7). 26.2-2 In Figure 26.1(b), what is the ﬂow across the cut .fs; 2; 4g ; f1; 3; tg/? What is the capacity of this cut? 26.2-3 Show the execution of the Edmonds-Karp algorithm on the ﬂow network of Figure 26.1(a). 26.2-4 In the example of Figure 26.6, what is the minimum cut corresponding to the maximum ﬂow shown? Of the augmenting paths appearing in the example, which one cancels ﬂow? 26.2-5 Recall that the construction in Section 26.1 that converts a ﬂow network with multiple sources and sinks into a single-source, single-sink network adds edges with inﬁnite capacity. Prove that any ﬂow in the resulting network has a ﬁnite value if the edges of the original network with multiple sources and sinks have ﬁnite capacity. 26.2-6 Suppose that each source si in a ﬂow network with multiple sources and sinks produces exactly pi units of ﬂow, so that P 2V f .si; / D pi. Suppose also that each sink tj consumes exactly qj units, so that P 2V f .; tj/ D qj, where P i pi D P j qj. Show how to convert the problem of ﬁnding a ﬂow f that obeys

## 26.2 The Ford-Fulkerson method

these additional constraints into the problem of ﬁnding a maximum ﬂow in a singlesource, single-sink ﬂow network. 26.2-7 Prove Lemma 26.2. 26.2-8 Suppose that we redeﬁne the residual network to disallow edges into s. Argue that the procedure FORD-FULKERSON still correctly computes a maximum ﬂow. 26.2-9 Suppose that both f and f 0 are ﬂows in a network G and we compute ﬂow f " f 0.

Does the augmented ﬂow satisfy the ﬂow conservation property? Does it satisfy the capacity constraint? 26.2-10 Show how to ﬁnd a maximum ﬂow in a network G D .V; E/ by a sequence of at most jEj augmenting paths. (Hint: Determine the paths after ﬁnding the maximum ﬂow.) 26.2-11 The edge connectivity of an undirected graph is the minimum number k of edges that must be removed to disconnect the graph. For example, the edge connectivity of a tree is 1, and the edge connectivity of a cyclic chain of vertices is 2. Show how to determine the edge connectivity of an undirected graph G D .V; E/ by running a maximum-ﬂow algorithm on at most jV j ﬂow networks, each having O.V / vertices and O.E/ edges. 26.2-12 Suppose that you are given a ﬂow network G, and G has edges entering the source s. Let f be a ﬂow in G in which one of the edges .; s/ entering the source has f .; s/ D 1. Prove that there must exist another ﬂow f 0 with f 0.; s/ D 0 such that jf j D jf 0j. Give an O.E/-time algorithm to compute f 0, given f , and assuming that all edge capacities are integers. 26.2-13 Suppose that you wish to ﬁnd, among all minimum cuts in a ﬂow network G with integral capacities, one that contains the smallest number of edges. Show how to modify the capacities of G to create a new ﬂow network G0 in which any minimum cut in G0 is a minimum cut with the smallest number of edges in G.

## 26.3 Maximum bipartite matching

Some combinatorial problems can easily be cast as maximum-ﬂow problems. The multiple-source, multiple-sink maximum-ﬂow problem from Section 26.1 gave us one example. Some other combinatorial problems seem on the surface to have little to do with ﬂow networks, but can in fact be reduced to maximum-ﬂow problems. This section presents one such problem: ﬁnding a maximum matching in a bipartite graph. In order to solve this problem, we shall take advantage of an integrality property provided by the Ford-Fulkerson method. We shall also see how to use the Ford-Fulkerson method to solve the maximum-bipartite-matching problem on a graph G D .V; E/ in O.VE/ time. The maximum-bipartite-matching problem Given an undirected graph G D .V; E/, a matching is a subset of edges M  E such that for all vertices  2 V , at most one edge of M is incident on . We say that a vertex  2 V is matched by the matching M if some edge in M is incident on ; otherwise,  is unmatched. A maximum matching is a matching of maximum cardinality, that is, a matching M such that for any matching M 0, we have jMj  jM 0j. In this section, we shall restrict our attention to ﬁnding maximum matchings in bipartite graphs: graphs in which the vertex set can be partitioned into V D L [ R, where L and R are disjoint and all edges in E go between L and R. We further assume that every vertex in V has at least one incident edge. Figure 26.8 illustrates the notion of a matching in a bipartite graph. The problem of ﬁnding a maximum matching in a bipartite graph has many practical applications. As an example, we might consider matching a set L of machines with a set R of tasks to be performed simultaneously. We take the presence of edge .u; / in E to mean that a particular machine u 2 L is capable of performing a particular task  2 R. A maximum matching provides work for as many machines as possible.

Finding a maximum bipartite matching We can use the Ford-Fulkerson method to ﬁnd a maximum matching in an undirected bipartite graph G D .V; E/ in time polynomial in jV j and jEj. The trick is to construct a ﬂow network in which ﬂows correspond to matchings, as shown in Figure 26.8(c). We deﬁne the corresponding ﬂow network G0 D .V 0; E0/ for the bipartite graph G as follows. We let the source s and sink t be new vertices not in V , and we let V 0 D V [ fs; tg. If the vertex partition of G is V D L [ R, the

## 26.3 Maximum bipartite matching

L R L R s t (a) (c) L R (b) Figure 26.8 A bipartite graph G D .V; E/ with vertex partition V D L [ R. (a) A matching with cardinality 2, indicated by shaded edges. (b) A maximum matching with cardinality 3. (c) The corresponding ﬂow network G0 with a maximum ﬂow shown. Each edge has unit capacity. Shaded edges have a ﬂow of 1, and all other edges carry no ﬂow. The shaded edges from L to R correspond to those in the maximum matching from (b). directed edges of G0 are the edges of E, directed from L to R, along with jV j new directed edges:

E0 D f.s; u/ W u 2 Lg [ f.u; / W .u; / 2 Eg [ f.; t/ W  2 Rg : To complete the construction, we assign unit capacity to each edge in E0. Since each vertex in V has at least one incident edge, jEj  jV j =2. Thus, jEj  jE0j D jEj C jV j  3 jEj, and so jE0j D ‚.E/. The following lemma shows that a matching in G corresponds directly to a ﬂow in G’s corresponding ﬂow network G0. We say that a ﬂow f on a ﬂow network G D .V; E/ is integer-valued if f .u; / is an integer for all .u; / 2 V 	 V .

> **Lemma 26.9**

Let G D .V; E/ be a bipartite graph with vertex partition V D L [ R, and let G0 D .V 0; E0/ be its corresponding ﬂow network. If M is a matching in G, then there is an integer-valued ﬂow f in G0 with value jf j D jMj. Conversely, if f is an integer-valued ﬂow in G0, then there is a matching M in G with cardinality jMj D jf j.

Proof We ﬁrst show that a matching M in G corresponds to an integer-valued ﬂow f in G0. Deﬁne f as follows. If .u; / 2 M, then f .s; u/ D f .u; / D f .; t/ D 1. For all other edges .u; / 2 E0, we deﬁne f .u; / D 0. It is simple to verify that f satisﬁes the capacity constraint and ﬂow conservation.

Intuitively, each edge .u; / 2 M corresponds to one unit of ﬂow in G0 that traverses the path s ! u !  ! t. Moreover, the paths induced by edges in M are vertex-disjoint, except for s and t. The net ﬂow across cut .L [ fsg ; R [ ftg/ is equal to jMj; thus, by Lemma 26.4, the value of the ﬂow is jf j D jMj. To prove the converse, let f be an integer-valued ﬂow in G0, and let M D f.u; / W u 2 L;  2 R; and f .u; / > 0g :

Each vertex u 2 L has only one entering edge, namely .s; u/, and its capacity is 1. Thus, each u 2 L has at most one unit of ﬂow entering it, and if one unit of ﬂow does enter, by ﬂow conservation, one unit of ﬂow must leave. Furthermore, since f is integer-valued, for each u 2 L, the one unit of ﬂow can enter on at most one edge and can leave on at most one edge. Thus, one unit of ﬂow enters u if and only if there is exactly one vertex  2 R such that f .u; / D 1, and at most one edge leaving each u 2 L carries positive ﬂow. A symmetric argument applies to each  2 R. The set M is therefore a matching. To see that jMj D jf j, observe that for every matched vertex u 2 L, we have f .s; u/ D 1, and for every edge .u; / 2 E  M, we have f .u; / D 0. Consequently, f .L [ fsg ; R [ ftg/, the net ﬂow across cut .L [ fsg ; R [ ftg/, is equal to jMj. Applying Lemma 26.4, we have that jf j D f .L[fsg ; R[ftg/ D jMj.

Based on Lemma 26.9, we would like to conclude that a maximum matching in a bipartite graph G corresponds to a maximum ﬂow in its corresponding ﬂow network G0, and we can therefore compute a maximum matching in G by running a maximum-ﬂow algorithm on G0. The only hitch in this reasoning is that the maximum-ﬂow algorithm might return a ﬂow in G0 for which some f .u; / is not an integer, even though the ﬂow value jf j must be an integer. The following theorem shows that if we use the Ford-Fulkerson method, this difﬁculty cannot arise.

> **Theorem 26.10 (Integrality theorem)**

If the capacity function c takes on only integral values, then the maximum ﬂow f produced by the Ford-Fulkerson method has the property that jf j is an integer.

Moreover, for all vertices u and , the value of f .u; / is an integer.

Proof The proof is by induction on the number of iterations. We leave it as Exercise 26.3-2. We can now prove the following corollary to Lemma 26.9.

## 26.3 Maximum bipartite matching

> **Corollary 26.11**

The cardinality of a maximum matching M in a bipartite graph G equals the value of a maximum ﬂow f in its corresponding ﬂow network G0.

Proof We use the nomenclature from Lemma 26.9. Suppose that M is a maximum matching in G and that the corresponding ﬂow f in G0 is not maximum. Then there is a maximum ﬂow f 0 in G0 such that jf 0j > jf j. Since the capacities in G0 are integer-valued, by Theorem 26.10, we can assume that f 0 is integer-valued. Thus, f 0 corresponds to a matching M 0 in G with cardinality jM 0j D jf 0j > jf j D jMj, contradicting our assumption that M is a maximum matching. In a similar manner, we can show that if f is a maximum ﬂow in G0, its corresponding matching is a maximum matching on G. Thus, given a bipartite undirected graph G, we can ﬁnd a maximum matching by creating the ﬂow network G0, running the Ford-Fulkerson method, and directly obtaining a maximum matching M from the integer-valued maximum ﬂow f found.

Since any matching in a bipartite graph has cardinality at most min.L; R/ D O.V /, the value of the maximum ﬂow in G0 is O.V /. We can therefore ﬁnd a maximum matching in a bipartite graph in time O.VE0/ D O.VE/, since jE0j D ‚.E/.

## Exercises

26.3-1 Run the Ford-Fulkerson algorithm on the ﬂow network in Figure 26.8(c) and show the residual network after each ﬂow augmentation. Number the vertices in L top to bottom from 1 to 5 and in R top to bottom from 6 to 9. For each iteration, pick the augmenting path that is lexicographically smallest. 26.3-2 Prove Theorem 26.10. 26.3-3 Let G D .V; E/ be a bipartite graph with vertex partition V D L [ R, and let G0 be its corresponding ﬂow network. Give a good upper bound on the length of any augmenting path found in G0 during the execution of FORD-FULKERSON. 26.3-4 ?

A perfect matching is a matching in which every vertex is matched. Let G D .V; E/ be an undirected bipartite graph with vertex partition V D L [ R, where jLj D jRj. For any X  V , deﬁne the neighborhood of X as N.X/ D fy 2 V W .x; y/ 2 E for some x 2 Xg ;

that is, the set of vertices adjacent to some member of X. Prove Hall’s theorem: there exists a perfect matching in G if and only if jAj  jN.A/j for every subset A  L. 26.3-5 ? We say that a bipartite graph G D .V; E/, where V D L[R, is d-regular if every vertex  2 V has degree exactly d. Every d-regular bipartite graph has jLj D jRj.

Prove that every d-regular bipartite graph has a matching of cardinality jLj by arguing that a minimum cut of the corresponding ﬂow network has capacity jLj. ?

## 26.4 Push-relabel algorithms

In this section, we present the “push-relabel” approach to computing maximum ﬂows. To date, many of the asymptotically fastest maximum-ﬂow algorithms are push-relabel algorithms, and the fastest actual implementations of maximum-ﬂow algorithms are based on the push-relabel method. Push-relabel methods also efﬁ- ciently solve other ﬂow problems, such as the minimum-cost ﬂow problem. This section introduces Goldberg’s “generic” maximum-ﬂow algorithm, which has a simple implementation that runs in O.V 2E/ time, thereby improving upon the O.VE2/ bound of the Edmonds-Karp algorithm. Section 26.5 reﬁnes the generic algorithm to obtain another push-relabel algorithm that runs in O.V 3/ time.

Push-relabel algorithms work in a more localized manner than the Ford- Fulkerson method. Rather than examine the entire residual network to ﬁnd an augmenting path, push-relabel algorithms work on one vertex at a time, looking only at the vertex’s neighbors in the residual network. Furthermore, unlike the Ford- Fulkerson method, push-relabel algorithms do not maintain the ﬂow-conservation property throughout their execution. They do, however, maintain a preﬂow, which is a function f W V 	V ! R that satisﬁes the capacity constraint and the following relaxation of ﬂow conservation:

X 2V f .; u/  X 2V f .u; /  0 for all vertices u 2 V  fsg. That is, the ﬂow into a vertex may exceed the ﬂow out. We call the quantity e.u/ D X 2V f .; u/  X 2V f .u; / (26.14) the excess ﬂow into vertex u. The excess at a vertex is the amount by which the ﬂow in exceeds the ﬂow out. We say that a vertex u 2 V  fs; tg is overﬂowing if e.u/ > 0.

## 26.4 Push-relabel algorithms

We shall begin this section by describing the intuition behind the push-relabel method. We shall then investigate the two operations employed by the method: “pushing” preﬂow and “relabeling” a vertex. Finally, we shall present a generic push-relabel algorithm and analyze its correctness and running time. Intuition You can understand the intuition behind the push-relabel method in terms of ﬂuid ﬂows: we consider a ﬂow network G D .V; E/ to be a system of interconnected pipes of given capacities. Applying this analogy to the Ford-Fulkerson method, we might say that each augmenting path in the network gives rise to an additional stream of ﬂuid, with no branch points, ﬂowing from the source to the sink. The Ford-Fulkerson method iteratively adds more streams of ﬂow until no more can be added. The generic push-relabel algorithm has a rather different intuition. As before, directed edges correspond to pipes. Vertices, which are pipe junctions, have two interesting properties. First, to accommodate excess ﬂow, each vertex has an out- ﬂow pipe leading to an arbitrarily large reservoir that can accumulate ﬂuid. Second, each vertex, its reservoir, and all its pipe connections sit on a platform whose height increases as the algorithm progresses.

Vertex heights determine how ﬂow is pushed: we push ﬂow only downhill, that is, from a higher vertex to a lower vertex. The ﬂow from a lower vertex to a higher vertex may be positive, but operations that push ﬂow push it only downhill. We ﬁx the height of the source at jV j and the height of the sink at 0. All other vertex heights start at 0 and increase with time. The algorithm ﬁrst sends as much ﬂow as possible downhill from the source toward the sink. The amount it sends is exactly enough to ﬁll each outgoing pipe from the source to capacity; that is, it sends the capacity of the cut .s; V  fsg/. When ﬂow ﬁrst enters an intermediate vertex, it collects in the vertex’s reservoir. From there, we eventually push it downhill. We may eventually ﬁnd that the only pipes that leave a vertex u and are not already saturated with ﬂow connect to vertices that are on the same level as u or are uphill from u. In this case, to rid an overﬂowing vertex u of its excess ﬂow, we must increase its height—an operation called “relabeling” vertex u. We increase its height to one unit more than the height of the lowest of its neighbors to which it has an unsaturated pipe. After a vertex is relabeled, therefore, it has at least one outgoing pipe through which we can push more ﬂow.

Eventually, all the ﬂow that can possibly get through to the sink has arrived there. No more can arrive, because the pipes obey the capacity constraints; the amount of ﬂow across any cut is still limited by the capacity of the cut. To make the preﬂow a “legal” ﬂow, the algorithm then sends the excess collected in the reservoirs of overﬂowing vertices back to the source by continuing to relabel vertices to above

the ﬁxed height jV j of the source. As we shall see, once we have emptied all the reservoirs, the preﬂow is not only a “legal” ﬂow, it is also a maximum ﬂow. The basic operations From the preceding discussion, we see that a push-relabel algorithm performs two basic operations: pushing ﬂow excess from a vertex to one of its neighbors and relabeling a vertex. The situations in which these operations apply depend on the heights of vertices, which we now deﬁne precisely.

Let G D .V; E/ be a ﬂow network with source s and sink t, and let f be a preﬂow in G. A function h W V ! N is a height function3 if h.s/ D jV j, h.t/ D 0, and h.u/  h./ C 1 for every residual edge .u; / 2 Ef . We immediately obtain the following lemma.

> **Lemma 26.12**

Let G D .V; E/ be a ﬂow network, let f be a preﬂow in G, and let h be a height function on V . For any two vertices u;  2 V , if h.u/ > h./ C 1, then .u; / is not an edge in the residual network. The push operation The basic operation PUSH.u; / applies if u is an overﬂowing vertex, cf .u; / > 0, and h.u/ D h./C1. The pseudocode below updates the preﬂow f and the excess ﬂows for u and . It assumes that we can compute residual capacity cf .u; / in constant time given c and f . We maintain the excess ﬂow stored at a vertex u as the attribute u:e and the height of u as the attribute u:h. The expression f .u; / is a temporary variable that stores the amount of ﬂow that we can push from u to . 3In the literature, a height function is typically called a “distance function,” and the height of a vertex is called a “distance label.” We use the term “height” because it is more suggestive of the intuition behind the algorithm. We retain the use of the term “relabel” to refer to the operation that increases the height of a vertex. The height of a vertex is related to its distance from the sink t, as would be found in a breadth-ﬁrst search of the transpose GT.

## 26.4 Push-relabel algorithms

PUSH.u; / // Applies when: u is overﬂowing, cf .u; / > 0, and u:h D :h C 1. // Action: Push f .u; / D min.u:e; cf .u; // units of ﬂow from u to .

f .u; / D min.u:e; cf .u; // if .u; / 2 E .u; /:f D .u; /:f C f .u; / else .; u/:f D .; u/:f  f .u; / u:e D u:e  f .u; / :e D :e C f .u; / The code for PUSH operates as follows. Because vertex u has a positive excess u:e and the residual capacity of .u; / is positive, we can increase the ﬂow from u to  by f .u; / D min.u:e; cf .u; // without causing u:e to become negative or the capacity c.u; / to be exceeded. Line 3 computes the value f .u; /, and lines 4–6 update f . Line 5 increases the ﬂow on edge .u; /, because we are pushing ﬂow over a residual edge that is also an original edge. Line 6 decreases the ﬂow on edge .; u/, because the residual edge is actually the reverse of an edge in the original network. Finally, lines 7–8 update the excess ﬂows into vertices u and . Thus, if f is a preﬂow before PUSH is called, it remains a preﬂow afterward.

Observe that nothing in the code for PUSH depends on the heights of u and , yet we prohibit it from being invoked unless u:h D :h C 1. Thus, we push excess ﬂow downhill only by a height differential of 1. By Lemma 26.12, no residual edges exist between two vertices whose heights differ by more than 1, and thus, as long as the attribute h is indeed a height function, we would gain nothing by allowing ﬂow to be pushed downhill by a height differential of more than 1. We call the operation PUSH.u; / a push from u to . If a push operation applies to some edge .u; / leaving a vertex u, we also say that the push operation applies to u. It is a saturating push if edge .u; / in the residual network becomes saturated (cf .u; / D 0 afterward); otherwise, it is a nonsaturating push. If an edge becomes saturated, it disappears from the residual network. A simple lemma characterizes one result of a nonsaturating push.

> **Lemma 26.13**

After a nonsaturating push from u to , the vertex u is no longer overﬂowing.

Proof Since the push was nonsaturating, the amount of ﬂow f .u; / actually pushed must equal u:e prior to the push. Since u:e is reduced by this amount, it becomes 0 after the push.

The relabel operation The basic operation RELABEL.u/ applies if u is overﬂowing and if u:h  :h for all edges .u; / 2 Ef . In other words, we can relabel an overﬂowing vertex u if for every vertex  for which there is residual capacity from u to , ﬂow cannot be pushed from u to  because  is not downhill from u. (Recall that by deﬁnition, neither the source s nor the sink t can be overﬂowing, and so s and t are ineligible for relabeling.) RELABEL.u/ // Applies when: u is overﬂowing and for all  2 V such that .u; / 2 Ef , we have u:h  :h. // Action: Increase the height of u. u:h D 1 C min f:h W .u; / 2 Ef g When we call the operation RELABEL.u/, we say that vertex u is relabeled. Note that when u is relabeled, Ef must contain at least one edge that leaves u, so that the minimization in the code is over a nonempty set. This property follows from the assumption that u is overﬂowing, which in turn tells us that u:e D X 2V f .; u/  X 2V f .u; / > 0 :

Since all ﬂows are nonnegative, we must therefore have at least one vertex  such that .; u/:f > 0. But then, cf .u; / > 0, which implies that .u; / 2 Ef . The operation RELABEL.u/ thus gives u the greatest height allowed by the constraints on height functions. The generic algorithm The generic push-relabel algorithm uses the following subroutine to create an initial preﬂow in the ﬂow network.

INITIALIZE-PREFLOW.G; s/ for each vertex  2 G:V :h D 0 :e D 0 for each edge .u; / 2 G:E .u; /:f D 0 s:h D jG:Vj for each vertex  2 s:Adj .s; /:f D c.s; / :e D c.s; / s:e D s:e  c.s; /

## 26.4 Push-relabel algorithms

INITIALIZE-PREFLOW creates an initial preﬂow f deﬁned by .u; /:f D ( c.u; / if u D s ; otherwise : (26.15) That is, we ﬁll to capacity each edge leaving the source s, and all other edges carry no ﬂow. For each vertex  adjacent to the source, we initially have :e D c.s; /, and we initialize s:e to the negative of the sum of these capacities. The generic algorithm also begins with an initial height function h, given by u:h D ( jV j if u D s ; otherwise : (26.16) Equation (26.16) deﬁnes a height function because the only edges .u; / for which u:h > :h C 1 are those for which u D s, and those edges are saturated, which means that they are not in the residual network. Initialization, followed by a sequence of push and relabel operations, executed in no particular order, yields the GENERIC-PUSH-RELABEL algorithm:

GENERIC-PUSH-RELABEL.G/ INITIALIZE-PREFLOW.G; s/ while there exists an applicable push or relabel operation select an applicable push or relabel operation and perform it The following lemma tells us that as long as an overﬂowing vertex exists, at least one of the two basic operations applies.

> **Lemma 26.14 (An overﬂowing vertex can be either pushed or relabeled)**

Let G D .V; E/ be a ﬂow network with source s and sink t, let f be a preﬂow, and let h be any height function for f . If u is any overﬂowing vertex, then either a push or relabel operation applies to it.

Proof For any residual edge .u; /, we have h.u/  h./ C 1 because h is a height function. If a push operation does not apply to an overﬂowing vertex u, then for all residual edges .u; /, we must have h.u/ < h./ C 1, which implies h.u/  h./. Thus, a relabel operation applies to u.

Correctness of the push-relabel method To show that the generic push-relabel algorithm solves the maximum-ﬂow problem, we shall ﬁrst prove that if it terminates, the preﬂow f is a maximum ﬂow. We shall later prove that it terminates. We start with some observations about the height function h.

> **Lemma 26.15 (Vertex heights never decrease)**

During the execution of the GENERIC-PUSH-RELABEL procedure on a ﬂow network G D .V; E/, for each vertex u 2 V , the height u:h never decreases. Moreover, whenever a relabel operation is applied to a vertex u, its height u:h increases by at least 1.

Proof Because vertex heights change only during relabel operations, it sufﬁces to prove the second statement of the lemma. If vertex u is about to be relabeled, then for all vertices  such that .u; / 2 Ef , we have u:h  :h. Thus, u:h < 1 C min f:h W .u; / 2 Ef g, and so the operation must increase u:h.

> **Lemma 26.16**

Let G D .V; E/ be a ﬂow network with source s and sink t. Then the execution of GENERIC-PUSH-RELABEL on G maintains the attribute h as a height function.

Proof The proof is by induction on the number of basic operations performed. Initially, h is a height function, as we have already observed. We claim that if h is a height function, then an operation RELABEL.u/ leaves h a height function. If we look at a residual edge .u; / 2 Ef that leaves u, then the operation RELABEL.u/ ensures that u:h  :h C 1 afterward. Now consider a residual edge .w; u/ that enters u. By Lemma 26.15, w:h  u:h C 1 before the operation RELABEL.u/ implies w:h < u:h C 1 afterward. Thus, the operation RELABEL.u/ leaves h a height function. Now, consider an operation PUSH.u; /. This operation may add the edge .; u/ to Ef , and it may remove .u; / from Ef . In the former case, we have :h D u:h  1 < u:h C 1, and so h remains a height function. In the latter case, removing .u; / from the residual network removes the corresponding constraint, and h again remains a height function. The following lemma gives an important property of height functions.

> **Lemma 26.17**

Let G D .V; E/ be a ﬂow network with source s and sink t, let f be a preﬂow in G, and let h be a height function on V . Then there is no path from the source s to the sink t in the residual network Gf .

Proof Assume for the sake of contradiction that Gf contains a path p from s to t, where p D h0; 1; : : : ; ki, 0 D s, and k D t. Without loss of generality, p is a simple path, and so k < jV j. For i D 0; 1; : : : ; k  1, edge .i; iC1/ 2 Ef .

Because h is a height function, h.i/  h.iC1/ C 1 for i D 0; 1; : : : ; k  1. Combining these inequalities over path p yields h.s/  h.t/Ck. But because h.t/ D 0,

## 26.4 Push-relabel algorithms

we have h.s/  k < jV j, which contradicts the requirement that h.s/ D jV j in a height function. We are now ready to show that if the generic push-relabel algorithm terminates, the preﬂow it computes is a maximum ﬂow.

> **Theorem 26.18 (Correctness of the generic push-relabel algorithm)**

If the algorithm GENERIC-PUSH-RELABEL terminates when run on a ﬂow network G D .V; E/ with source s and sink t, then the preﬂow f it computes is a maximum ﬂow for G.

Proof We use the following loop invariant:

Each time the while loop test in line 2 in GENERIC-PUSH-RELABEL is executed, f is a preﬂow. Initialization: INITIALIZE-PREFLOW makes f a preﬂow.

Maintenance: The only operations within the while loop of lines 2–3 are push and relabel. Relabel operations affect only height attributes and not the ﬂow values; hence they do not affect whether f is a preﬂow. As argued on page 739, if f is a preﬂow prior to a push operation, it remains a preﬂow afterward.

Termination: At termination, each vertex in V  fs; tg must have an excess of 0, because by Lemma 26.14 and the invariant that f is always a preﬂow, there are no overﬂowing vertices. Therefore, f is a ﬂow. Lemma 26.16 shows that h is a height function at termination, and thus Lemma 26.17 tells us that there is no path from s to t in the residual network Gf . By the max-ﬂow min-cut theorem (Theorem 26.6), therefore, f is a maximum ﬂow. Analysis of the push-relabel method To show that the generic push-relabel algorithm indeed terminates, we shall bound the number of operations it performs. We bound separately each of the three types of operations: relabels, saturating pushes, and nonsaturating pushes. With knowledge of these bounds, it is a straightforward problem to construct an algorithm that runs in O.V 2E/ time. Before beginning the analysis, however, we prove an important lemma. Recall that we allow edges into the source in the residual network.

> **Lemma 26.19**

Let G D .V; E/ be a ﬂow network with source s and sink t, and let f be a preﬂow in G. Then, for any overﬂowing vertex x, there is a simple path from x to s in the residual network Gf .

Proof For an overﬂowing vertex x, let U D f W there exists a simple path from x to  in Gf g, and suppose for the sake of contradiction that s 62 U . Let U D V U . We take the deﬁnition of excess from equation (26.14), sum over all vertices in U , and note that V D U [ U , to obtain X u2U e.u/ D X u2U X 2V f .; u/  X 2V f .u; / !

D X u2U X 2U f .; u/ C X 2U f .; u/ !  X 2U f .u; / C X 2U f .u; / !!

D X u2U X 2U f .; u/ C X u2U X 2U f .; u/  X u2U X 2U f .u; /  X u2U X 2U f .u; / D X u2U X 2U f .; u/  X u2U X 2U f .u; / : We know that the quantity P u2U e.u/ must be positive because e.x/ > 0, x 2 U , all vertices other than s have nonnegative excess, and, by assumption, s 62 U . Thus, we have X u2U X 2U f .; u/  X u2U X 2U f .u; / > 0 : (26.17) All edge ﬂows are nonnegative, and so for equation (26.17) to hold, we must have P u2U P 2U f .; u/ > 0. Hence, there must exist at least one pair of vertices u0 2 U and 0 2 U with f .0; u0/ > 0. But, if f .0; u0/ > 0, there must be a residual edge .u0; 0/, which means that there is a simple path from x to 0 (the path x ; u0 ! 0), thus contradicting the deﬁnition of U . The next lemma bounds the heights of vertices, and its corollary bounds the number of relabel operations that are performed in total.

> **Lemma 26.20**

Let G D .V; E/ be a ﬂow network with source s and sink t. At any time during the execution of GENERIC-PUSH-RELABEL on G, we have u:h  2 jV j1 for all vertices u 2 V .

Proof The heights of the source s and the sink t never change because these vertices are by deﬁnition not overﬂowing. Thus, we always have s:h D jV j and t:h D 0, both of which are no greater than 2 jV j  1. Now consider any vertex u 2 V fs; tg. Initially, u:h D 0  2 jV j1. We shall show that after each relabeling operation, we still have u:h  2 jV j  1. When u is

## 26.4 Push-relabel algorithms

relabeled, it is overﬂowing, and Lemma 26.19 tells us that there is a simple path p from u to s in Gf . Let p D h0;1;: : : ;ki, where 0 D u, k D s, and k  jV j1 because p is simple. For i D 0; 1; : : : ; k  1, we have .i; iC1/ 2 Ef , and therefore, by Lemma 26.16, i:h  iC1:h C 1. Expanding these inequalities over path p yields u:h D 0:h  k:h C k  s:h C .jV j  1/ D 2 jV j  1.

> **Corollary 26.21 (Bound on relabel operations)**

Let G D .V; E/ be a ﬂow network with source s and sink t. Then, during the execution of GENERIC-PUSH-RELABEL on G, the number of relabel operations is at most 2 jV j  1 per vertex and at most .2 jV j  1/.jV j  2/ < 2 jV j2 overall.

Proof Only the jV j2 vertices in V fs; tg may be relabeled. Let u 2 V fs; tg. The operation RELABEL.u/ increases u:h. The value of u:h is initially 0 and by

> **Lemma 26.20, it grows to at most 2 jV j  1. Thus, each vertex u 2 V  fs; tg**

is relabeled at most 2 jV j  1 times, and the total number of relabel operations performed is at most .2 jV j  1/.jV j  2/ < 2 jV j2.

> **Lemma 26.20 also helps us to bound the number of saturating pushes.**

> **Lemma 26.22 (Bound on saturating pushes)**

During the execution of GENERIC-PUSH-RELABEL on any ﬂow network G D .V; E/, the number of saturating pushes is less than 2 jV j jEj.

Proof For any pair of vertices u;  2 V , we will count the saturating pushes from u to  and from  to u together, calling them the saturating pushes between u and . If there are any such pushes, at least one of .u; / and .; u/ is actually an edge in E. Now, suppose that a saturating push from u to  has occurred.

At that time, :h D u:h  1. In order for another push from u to  to occur later, the algorithm must ﬁrst push ﬂow from  to u, which cannot happen until :h D u:h C 1. Since u:h never decreases, in order for :h D u:h C 1, the value of :h must increase by at least 2. Likewise, u:h must increase by at least 2 between saturating pushes from  to u. Heights start at 0 and, by Lemma 26.20, never exceed 2 jV j1, which implies that the number of times any vertex can have its height increase by 2 is less than jV j. Since at least one of u:h and :h must increase by 2 between any two saturating pushes between u and , there are fewer than 2 jV j saturating pushes between u and . Multiplying by the number of edges gives a bound of less than 2 jV j jEj on the total number of saturating pushes. The following lemma bounds the number of nonsaturating pushes in the generic push-relabel algorithm.

> **Lemma 26.23 (Bound on nonsaturating pushes)**

During the execution of GENERIC-PUSH-RELABEL on any ﬂow network G D .V; E/, the number of nonsaturating pushes is less than 4 jV j2 .jV j C jEj/.

Proof Deﬁne a potential function ˆ D P We./>0 :h. Initially, ˆ D 0, and the value of ˆ may change after each relabeling, saturating push, and nonsaturating push. We will bound the amount that saturating pushes and relabelings can contribute to the increase of ˆ. Then we will show that each nonsaturating push must decrease ˆ by at least 1, and will use these bounds to derive an upper bound on the number of nonsaturating pushes.

Let us examine the two ways in which ˆ might increase. First, relabeling a vertex u increases ˆ by less than 2 jV j, since the set over which the sum is taken is the same and the relabeling cannot increase u’s height by more than its maximum possible height, which, by Lemma 26.20, is at most 2 jV j  1. Second, a saturating push from a vertex u to a vertex  increases ˆ by less than 2 jV j, since no heights change and only vertex , whose height is at most 2 jV j  1, can possibly become overﬂowing. Now we show that a nonsaturating push from u to  decreases ˆ by at least 1.

Why? Before the nonsaturating push, u was overﬂowing, and  may or may not have been overﬂowing. By Lemma 26.13, u is no longer overﬂowing after the push. In addition, unless  is the source, it may or may not be overﬂowing after the push. Therefore, the potential function ˆ has decreased by exactly u:h, and it has increased by either 0 or :h. Since u:h  :h D 1, the net effect is that the potential function has decreased by at least 1. Thus, during the course of the algorithm, the total amount of increase in ˆ is due to relabelings and saturated pushes, and Corollary 26.21 and Lemma 26.22 constrain the increase to be less than .2 jV j/.2 jV j2/ C .2 jV j/.2 jV j jEj/ D 4 jV j2 .jV j C jEj/. Since ˆ  0, the total amount of decrease, and therefore the total number of nonsaturating pushes, is less than 4 jV j2 .jV j C jEj/.

Having bounded the number of relabelings, saturating pushes, and nonsaturating push, we have set the stage for the following analysis of the GENERIC- PUSH-RELABEL procedure, and hence of any algorithm based on the push-relabel method.

> **Theorem 26.24**

During the execution of GENERIC-PUSH-RELABEL on any ﬂow network G D .V; E/, the number of basic operations is O.V 2E/.

Proof Immediate from Corollary 26.21 and Lemmas 26.22 and 26.23.

## 26.4 Push-relabel algorithms

Thus, the algorithm terminates after O.V 2E/ operations. All that remains is to give an efﬁcient method for implementing each operation and for choosing an appropriate operation to execute.

> **Corollary 26.25**

There is an implementation of the generic push-relabel algorithm that runs in O.V 2E/ time on any ﬂow network G D .V; E/.

Proof Exercise 26.4-2 asks you to show how to implement the generic algorithm with an overhead of O.V / per relabel operation and O.1/ per push. It also asks you to design a data structure that allows you to pick an applicable operation in O.1/ time. The corollary then follows.

## Exercises

26.4-1 Prove that, after the procedure INITIALIZE-PREFLOW.G; s/ terminates, we have s:e   jf j, where f  is a maximum ﬂow for G. 26.4-2 Show how to implement the generic push-relabel algorithm using O.V / time per relabel operation, O.1/ time per push, and O.1/ time to select an applicable operation, for a total time of O.V 2E/. 26.4-3 Prove that the generic push-relabel algorithm spends a total of only O.VE/ time in performing all the O.V 2/ relabel operations. 26.4-4 Suppose that we have found a maximum ﬂow in a ﬂow network G D .V; E/ using a push-relabel algorithm. Give a fast algorithm to ﬁnd a minimum cut in G. 26.4-5 Give an efﬁcient push-relabel algorithm to ﬁnd a maximum matching in a bipartite graph. Analyze your algorithm. 26.4-6 Suppose that all edge capacities in a ﬂow network G D .V; E/ are in the set f1; 2; : : : ; kg. Analyze the running time of the generic push-relabel algorithm in terms of jV j, jEj, and k. (Hint: How many times can each edge support a nonsaturating push before it becomes saturated?)

26.4-7 Show that we could change line 6 of INITIALIZE-PREFLOW to s:h D jG:Vj  2 without affecting the correctness or asymptotic performance of the generic pushrelabel algorithm. 26.4-8 Let ıf .u; / be the distance (number of edges) from u to  in the residual network Gf .

Show that the GENERIC-PUSH-RELABEL procedure maintains the properties that u:h < jV j implies u:h  ıf .u; t/ and that u:h  jV j implies u:h  jV j  ıf .u; s/. 26.4-9 ? As in the previous exercise, let ıf .u; / be the distance from u to  in the residual network Gf . Show how to modify the generic push-relabel algorithm to maintain the property that u:h < jV j implies u:h D ıf .u; t/ and that u:h  jV j implies u:h  jV j D ıf .u; s/. The total time that your implementation dedicates to maintaining this property should be O.VE/. 26.4-10 Show that the number of nonsaturating pushes executed by the GENERIC-PUSH- RELABEL procedure on a ﬂow network G D .V; E/ is at most 4 jV j2 jEj for jV j  4. ?

## 26.5 The relabel-to-front algorithm

The push-relabel method allows us to apply the basic operations in any order at all. By choosing the order carefully and managing the network data structure efﬁ- ciently, however, we can solve the maximum-ﬂow problem faster than the O.V 2E/ bound given by Corollary 26.25. We shall now examine the relabel-to-front algorithm, a push-relabel algorithm whose running time is O.V 3/, which is asymptotically at least as good as O.V 2E/, and even better for dense networks. The relabel-to-front algorithm maintains a list of the vertices in the network.

Beginning at the front, the algorithm scans the list, repeatedly selecting an over- ﬂowing vertex u and then “discharging” it, that is, performing push and relabel operations until u no longer has a positive excess. Whenever we relabel a vertex, we move it to the front of the list (hence the name “relabel-to-front”) and the algorithm begins its scan anew.

## 26.5 The relabel-to-front algorithm

The correctness and analysis of the relabel-to-front algorithm depend on the notion of “admissible” edges: those edges in the residual network through which ﬂow can be pushed. After proving some properties about the network of admissible edges, we shall investigate the discharge operation and then present and analyze the relabel-to-front algorithm itself.

Admissible edges and networks If G D .V; E/ is a ﬂow network with source s and sink t, f is a preﬂow in G, and h is a height function, then we say that .u; / is an admissible edge if cf .u; / > 0 and h.u/ D h./ C 1. Otherwise, .u; / is inadmissible. The admissible network is Gf;h D .V; Ef;h/, where Ef;h is the set of admissible edges. The admissible network consists of those edges through which we can push ﬂow. The following lemma shows that this network is a directed acyclic graph (dag).

> **Lemma 26.26 (The admissible network is acyclic)**

If G D .V; E/ is a ﬂow network, f is a preﬂow in G, and h is a height function on G, then the admissible network Gf;h D .V; Ef;h/ is acyclic.

Proof The proof is by contradiction. Suppose that Gf;h contains a cycle p D h0;1;: : : ;ki, where 0 D k and k > 0. Since each edge in p is admissible, we have h.i1/ D h.i/ C 1 for i D 1; 2; : : : ; k. Summing around the cycle gives k X iD1 h.i1/ D k X iD1 .h.i/ C 1/ D k X iD1 h.i/ C k :

Because each vertex in cycle p appears once in each of the summations, we derive the contradiction that 0 D k. The next two lemmas show how push and relabel operations change the admissible network.

> **Lemma 26.27**

Let G D .V; E/ be a ﬂow network, let f be a preﬂow in G, and suppose that the attribute h is a height function. If a vertex u is overﬂowing and .u; / is an admissible edge, then PUSH.u; / applies. The operation does not create any new admissible edges, but it may cause .u; / to become inadmissible.

Proof By the deﬁnition of an admissible edge, we can push ﬂow from u to .

Since u is overﬂowing, the operation PUSH.u; / applies. The only new residual edge that pushing ﬂow from u to  can create is .; u/. Since :h D u:h  1, edge .; u/ cannot become admissible. If the operation is a saturating push, then cf .u; / D 0 afterward and .u; / becomes inadmissible.

> **Lemma 26.28**

Let G D .V; E/ be a ﬂow network, let f be a preﬂow in G, and suppose that the attribute h is a height function. If a vertex u is overﬂowing and there are no admissible edges leaving u, then RELABEL.u/ applies. After the relabel operation, there is at least one admissible edge leaving u, but there are no admissible edges entering u.

Proof If u is overﬂowing, then by Lemma 26.14, either a push or a relabel operation applies to it. If there are no admissible edges leaving u, then no ﬂow can be pushed from u and so RELABEL.u/ applies. After the relabel operation, u:h D 1 C min f:h W .u; / 2 Ef g. Thus, if  is a vertex that realizes the minimum in this set, the edge .u; / becomes admissible. Hence, after the relabel, there is at least one admissible edge leaving u. To show that no admissible edges enter u after a relabel operation, suppose that there is a vertex  such that .; u/ is admissible. Then, :h D u:h C 1 after the relabel, and so :h > u:h C 1 just before the relabel. But by Lemma 26.12, no residual edges exist between vertices whose heights differ by more than 1. Moreover, relabeling a vertex does not change the residual network. Thus, .; u/ is not in the residual network, and hence it cannot be in the admissible network.

Neighbor lists Edges in the relabel-to-front algorithm are organized into “neighbor lists.” Given a ﬂow network G D .V; E/, the neighbor list u:N for a vertex u 2 V is a singly linked list of the neighbors of u in G. Thus, vertex  appears in the list u:N if .u; / 2 E or .; u/ 2 E. The neighbor list u:N contains exactly those vertices  for which there may be a residual edge .u; /. The attribute u:N:head points to the ﬁrst vertex in u:N, and :next-neighbor points to the vertex following  in a neighbor list; this pointer is NIL if  is the last vertex in the neighbor list. The relabel-to-front algorithm cycles through each neighbor list in an arbitrary order that is ﬁxed throughout the execution of the algorithm. For each vertex u, the attribute u:current points to the vertex currently under consideration in u:N. Initially, u:current is set to u:N:head.

## 26.5 The relabel-to-front algorithm

Discharging an overﬂowing vertex An overﬂowing vertex u is discharged by pushing all of its excess ﬂow through admissible edges to neighboring vertices, relabeling u as necessary to cause edges leaving u to become admissible. The pseudocode goes as follows.

DISCHARGE.u/ while u:e > 0  D u:current if  == NIL RELABEL.u/ u:current D u:N:head elseif cf .u; / > 0 and u:h == :h C 1 PUSH.u; / else u:current D :next-neighbor Figure 26.9 steps through several iterations of the while loop of lines 1–8, which executes as long as vertex u has positive excess. Each iteration performs exactly one of three actions, depending on the current vertex  in the neighbor list u:N. 1. If  is NIL, then we have run off the end of u:N. Line 4 relabels vertex u, and then line 5 resets the current neighbor of u to be the ﬁrst one in u:N. (Lemma 26.29 below states that the relabel operation applies in this situation.) 2. If  is non-NIL and .u; / is an admissible edge (determined by the test in line 6), then line 7 pushes some (or possibly all) of u’s excess to vertex . 3. If  is non-NIL but .u; / is inadmissible, then line 8 advances u:current one position further in the neighbor list u:N.

Observe that if DISCHARGE is called on an overﬂowing vertex u, then the last action performed by DISCHARGE must be a push from u. Why? The procedure terminates only when u:e becomes zero, and neither the relabel operation nor advancing the pointer u:current affects the value of u:e. We must be sure that when PUSH or RELABEL is called by DISCHARGE, the operation applies. The next lemma proves this fact.

> **Lemma 26.29**

If DISCHARGE calls PUSH.u; / in line 7, then a push operation applies to .u; /. If DISCHARGE calls RELABEL.u/ in line 4, then a relabel operation applies to u.

Proof The tests in lines 1 and 6 ensure that a push operation occurs only if the operation applies, which proves the ﬁrst statement in the lemma.

s –26 x y z 5/5 14/14 s x z s –26 x y z 14/14 s x z 5/5 s –26 x y z 8/8 14/14 5/5 s x z s x z s x z s x z s x z s x z s x z (a) (b) (c) Figure 26.9 Discharging a vertex y. It takes 15 iterations of the while loop of DISCHARGE to push all the excess ﬂow from y. Only the neighbors of y and edges of the ﬂow network that enter or leave y are shown. In each part of the ﬁgure, the number inside each vertex is its excess at the beginning of the ﬁrst iteration shown in the part, and each vertex is shown at its height throughout the part. The neighbor list y:N at the beginning of each iteration appears on the right, with the iteration number on top. The shaded neighbor is y:current. (a) Initially, there are 19 units of excess to push from y, and y:current D s. Iterations 1, 2, and 3 just advance y:current, since there are no admissible edges leaving y. In iteration 4, y:current D NIL (shown by the shading being below the neighbor list), and so y is relabeled and y:current is reset to the head of the neighbor list. (b) After relabeling, vertex y has height 1. In iterations 5 and 6, edges .y; s/ and .y; x/ are found to be inadmissible, but iteration 7 pushes 8 units of excess ﬂow from y to ´. Because of the push, y:current does not advance in this iteration. (c) Because the push in iteration 7 saturated edge .y; ´/, it is found inadmissible in iteration 8. In iteration 9, y:current D NIL, and so vertex y is again relabeled and y:current is reset.

## 26.5 The relabel-to-front algorithm

s –26 x y z 8/8 14/14 s –26 x y z 8/8 14/14 5/5 s –26 x y z 8/8 14/14 s –20 x y z 8/8 8/14 s x z s x z s x z s x z s x z s x z (f) (d) (e) (g) Figure 26.9, continued (d) In iteration 10, .y; s/ is inadmissible, but iteration 11 pushes 5 units of excess ﬂow from y to x. (e) Because y:current did not advance in iteration 11, iteration 12 ﬁnds .y; x/ to be inadmissible. Iteration 13 ﬁnds .y;´/ inadmissible, and iteration 14 relabels vertex y and resets y:current. (f) Iteration 15 pushes 6 units of excess ﬂow from y to s. (g) Vertex y now has no excess ﬂow, and DISCHARGE terminates. In this example, DISCHARGE both starts and ﬁnishes with the current pointer at the head of the neighbor list, but in general this need not be the case.

To prove the second statement, according to the test in line 1 and Lemma 26.28, we need only show that all edges leaving u are inadmissible. If a call to DISCHARGE.u/ starts with the pointer u:current at the head of u’s neighbor list and ﬁnishes with it off the end of the list, then all of u’s outgoing edges are inadmissible and a relabel operation applies. It is possible, however, that during a call to DISCHARGE.u/, the pointer u:current traverses only part of the list before the procedure returns. Calls to DISCHARGE on other vertices may then occur, but u:current will continue moving through the list during the next call to DISCHARGE.u/. We now consider what happens during a complete pass through the list, which begins at the head of u:N and ﬁnishes with u:current D NIL. Once u:current reaches the end of the list, the procedure relabels u and begins a new pass. For the u:current pointer to advance past a vertex  2 u:N during a pass, the edge .u; / must be deemed inadmissible by the test in line 6. Thus, by the time the pass completes, every edge leaving u has been determined to be inadmissible at some time during the pass. The key observation is that at the end of the pass, every edge leaving u is still inadmissible. Why? By Lemma 26.27, pushes cannot create any admissible edges, regardless of which vertex the ﬂow is pushed from. Thus, any admissible edge must be created by a relabel operation. But the vertex u is not relabeled during the pass, and by Lemma 26.28, any other vertex  that is relabeled during the pass (resulting from a call of DISCHARGE./) has no entering admissible edges after relabeling. Thus, at the end of the pass, all edges leaving u remain inadmissible, which completes the proof. The relabel-to-front algorithm In the relabel-to-front algorithm, we maintain a linked list L consisting of all vertices in V  fs; tg. A key property is that the vertices in L are topologically sorted according to the admissible network, as we shall see in the loop invariant that follows. (Recall from Lemma 26.26 that the admissible network is a dag.) The pseudocode for the relabel-to-front algorithm assumes that the neighbor lists u:N have already been created for each vertex u. It also assumes that u:next points to the vertex that follows u in list L and that, as usual, u:next D NIL if u is the last vertex in the list.

## 26.5 The relabel-to-front algorithm

RELABEL-TO-FRONT.G; s; t/ INITIALIZE-PREFLOW.G; s/ L D G:V  fs; tg, in any order for each vertex u 2 G:V  fs; tg u:current D u:N:head u D L:head while u ¤ NIL old-height D u:h DISCHARGE.u/ if u:h > old-height move u to the front of list L u D u:next The relabel-to-front algorithm works as follows. Line 1 initializes the preﬂow and heights to the same values as in the generic push-relabel algorithm. Line 2 initializes the list L to contain all potentially overﬂowing vertices, in any order.

Lines 3–4 initialize the current pointer of each vertex u to the ﬁrst vertex in u’s neighbor list. As Figure 26.10 illustrates, the while loop of lines 6–11 runs through the list L, discharging vertices. Line 5 makes it start with the ﬁrst vertex in the list. Each time through the loop, line 8 discharges a vertex u. If u was relabeled by the DISCHARGE procedure, line 10 moves it to the front of list L. We can determine whether u was relabeled by comparing its height before the discharge operation, saved into the variable old-height in line 7, with its height afterward, in line 9.

Line 11 makes the next iteration of the while loop use the vertex following u in list L. If line 10 moved u to the front of the list, the vertex used in the next iteration is the one following u in its new position in the list. To show that RELABEL-TO-FRONT computes a maximum ﬂow, we shall show that it is an implementation of the generic push-relabel algorithm.

First, observe that it performs push and relabel operations only when they apply, since

> **Lemma 26.29 guarantees that DISCHARGE performs them only when they apply.**

It remains to show that when RELABEL-TO-FRONT terminates, no basic operations apply. The remainder of the correctness argument relies on the following loop invariant:

At each test in line 6 of RELABEL-TO-FRONT, list L is a topological sort of the vertices in the admissible network Gf;h D .V; Ef;h/, and no vertex before u in the list has excess ﬂow. Initialization: Immediately after INITIALIZE-PREFLOW has been run, s:h D jV j and :h D 0 for all  2 V  fsg. Since jV j  2 (because V contains at

s –26 x y z t 14/14 12/12 L: x y z N: s y z t s x z x y t (a) s –26 x y z t 5/5 14/14 12/12 L: x y z N: s y z t s x z x y t (b) 7/16 s –20 x y z t 8/8 8/14 12/12 L: x y z N: s y z t s x z x y t (c) 7/16 Figure 26.10 The action of RELABEL-TO-FRONT. (a) A ﬂow network just before the ﬁrst iteration of the while loop. Initially, 26 units of ﬂow leave source s. On the right is shown the initial list L D hx; y; ´i, where initially u D x. Under each vertex in list L is its neighbor list, with the current neighbor shaded. Vertex x is discharged. It is relabeled to height 1, 5 units of excess ﬂow are pushed to y, and the 7 remaining units of excess are pushed to the sink t. Because x is relabeled, it moves to the head of L, which in this case does not change the structure of L. (b) After x, the next vertex in L that is discharged is y. Figure 26.9 shows the detailed action of discharging y in this situation.

Because y is relabeled, it is moved to the head of L. (c) Vertex x now follows y in L, and so it is again discharged, pushing all 5 units of excess ﬂow to t. Because vertex x is not relabeled in this discharge operation, it remains in place in list L.

## 26.5 The relabel-to-front algorithm

s –20 x y z t 8/8 8/14 12/12 L: x y z N: s y z t s x z x y t (d) 12/16 s –20 x y z t 8/8 8/10 8/14 12/12 L: x y z N: s y z t s x z x y t (e) 12/16 Figure 26.10, continued (d) Since vertex ´ follows vertex x in L, it is discharged. It is relabeled to height 1 and all 8 units of excess ﬂow are pushed to t. Because ´ is relabeled, it moves to the front of L. (e) Vertex y now follows vertex ´ in L and is therefore discharged. But because y has no excess, DISCHARGE immediately returns, and y remains in place in L. Vertex x is then discharged.

Because it, too, has no excess, DISCHARGE again returns, and x remains in place in L. RELABEL- TO-FRONT has reached the end of list L and terminates. There are no overﬂowing vertices, and the preﬂow is a maximum ﬂow. least s and t), no edge can be admissible. Thus, Ef;h D ;, and any ordering of V  fs; tg is a topological sort of Gf;h.

Because u is initially the head of the list L, there are no vertices before it and so there are none before it with excess ﬂow.

Maintenance: To see that each iteration of the while loop maintains the topological sort, we start by observing that the admissible network is changed only by push and relabel operations. By Lemma 26.27, push operations do not cause edges to become admissible. Thus, only relabel operations can create admissible edges. After a vertex u is relabeled, however, Lemma 26.28 states that there are no admissible edges entering u but there may be admissible edges leaving u. Thus, by moving u to the front of L, the algorithm ensures that any admissible edges leaving u satisfy the topological sort ordering.

To see that no vertex preceding u in L has excess ﬂow, we denote the vertex that will be u in the next iteration by u0. The vertices that will precede u0 in the next iteration include the current u (due to line 11) and either no other vertices (if u is relabeled) or the same vertices as before (if u is not relabeled). When u is discharged, it has no excess ﬂow afterward. Thus, if u is relabeled during the discharge, no vertices preceding u0 have excess ﬂow. If u is not relabeled during the discharge, no vertices before it on the list acquired excess ﬂow during this discharge, because L remained topologically sorted at all times during the discharge (as just pointed out, admissible edges are created only by relabeling, not pushing), and so each push operation causes excess ﬂow to move only to vertices further down the list (or to s or t). Again, no vertices preceding u0 have excess ﬂow.

Termination: When the loop terminates, u is just past the end of L, and so the loop invariant ensures that the excess of every vertex is 0. Thus, no basic operations apply. Analysis We shall now show that RELABEL-TO-FRONT runs in O.V 3/ time on any ﬂow network G D .V; E/. Since the algorithm is an implementation of the generic push-relabel algorithm, we shall take advantage of Corollary 26.21, which provides an O.V / bound on the number of relabel operations executed per vertex and an O.V 2/ bound on the total number of relabel operations overall. In addition, Exercise 26.4-3 provides an O.VE/ bound on the total time spent performing relabel operations, and Lemma 26.22 provides an O.VE/ bound on the total number of saturating push operations.

> **Theorem 26.30**

The running time of RELABEL-TO-FRONT on any ﬂow network G D .V; E/ is O.V 3/.

Proof Let us consider a “phase” of the relabel-to-front algorithm to be the time between two consecutive relabel operations. There are O.V 2/ phases, since there are O.V 2/ relabel operations. Each phase consists of at most jV j calls to DIS- CHARGE, which we can see as follows. If DISCHARGE does not perform a relabel operation, then the next call to DISCHARGE is further down the list L, and the length of L is less than jV j. If DISCHARGE does perform a relabel, the next call to DISCHARGE belongs to a different phase. Since each phase contains at most jV j calls to DISCHARGE and there are O.V 2/ phases, the number of times DISCHARGE is called in line 8 of RELABEL-TO-FRONT is O.V 3/. Thus, the total

## 26.5 The relabel-to-front algorithm

work performed by the while loop in RELABEL-TO-FRONT, excluding the work performed within DISCHARGE, is at most O.V 3/. We must now bound the work performed within DISCHARGE during the execution of the algorithm. Each iteration of the while loop within DISCHARGE performs one of three actions. We shall analyze the total amount of work involved in performing each of these actions. We start with relabel operations (lines 4–5). Exercise 26.4-3 provides an O.VE/ time bound on all the O.V 2/ relabels that are performed. Now, suppose that the action updates the u:current pointer in line 8. This action occurs O.degree.u// times each time a vertex u is relabeled, and O.V degree.u// times overall for the vertex. For all vertices, therefore, the total amount of work done in advancing pointers in neighbor lists is O.VE/ by the handshaking lemma (Exercise B.4-1). The third type of action performed by DISCHARGE is a push operation (line 7). We already know that the total number of saturating push operations is O.VE/.

Observe that if a nonsaturating push is executed, DISCHARGE immediately returns, since the push reduces the excess to 0. Thus, there can be at most one nonsaturating push per call to DISCHARGE. As we have observed, DISCHARGE is called O.V 3/ times, and thus the total time spent performing nonsaturating pushes is O.V 3/. The running time of RELABEL-TO-FRONT is therefore O.V 3 C VE/, which is O.V 3/.

## Exercises

26.5-1 Illustrate the execution of RELABEL-TO-FRONT in the manner of Figure 26.10 for the ﬂow network in Figure 26.1(a). Assume that the initial ordering of vertices in L is h1; 2; 3; 4i and that the neighbor lists are 1:N D hs; 2; 3i ; 2:N D hs; 1; 3; 4i ; 3:N D h1; 2; 4; ti ; 4:N D h2; 3; ti : 26.5-2 ? We would like to implement a push-relabel algorithm in which we maintain a ﬁrstin, ﬁrst-out queue of overﬂowing vertices. The algorithm repeatedly discharges the vertex at the head of the queue, and any vertices that were not overﬂowing before the discharge but are overﬂowing afterward are placed at the end of the queue.

After the vertex at the head of the queue is discharged, it is removed. When the

queue is empty, the algorithm terminates. Show how to implement this algorithm to compute a maximum ﬂow in O.V 3/ time. 26.5-3 Show that the generic algorithm still works if RELABEL updates u:h by simply computing u:h D u:h C 1. How would this change affect the analysis of RELABEL-TO-FRONT? 26.5-4 ?

Show that if we always discharge a highest overﬂowing vertex, we can make the push-relabel method run in O.V 3/ time. 26.5-5 Suppose that at some point in the execution of a push-relabel algorithm, there exists an integer 0 < k  jV j  1 for which no vertex has :h D k. Show that all vertices with :h > k are on the source side of a minimum cut. If such a k exists, the gap heuristic updates every vertex  2 V  fsg for which :h > k, to set :h D max.:h; jV j C 1/. Show that the resulting attribute h is a height function. (The gap heuristic is crucial in making implementations of the push-relabel method perform well in practice.)

## Problems

26-1 Escape problem An n	n grid is an undirected graph consisting of n rows and n columns of vertices, as shown in Figure 26.11. We denote the vertex in the ith row and the j th column by .i; j /. All vertices in a grid have exactly four neighbors, except for the boundary vertices, which are the points .i; j / for which i D 1, i D n, j D 1, or j D n.

Given m  n2 starting points .x1; y1/; .x2; y2/; : : : ; .xm; ym/ in the grid, the escape problem is to determine whether or not there are m vertex-disjoint paths from the starting points to any m different points on the boundary. For example, the grid in Figure 26.11(a) has an escape, but the grid in Figure 26.11(b) does not. a. Consider a ﬂow network in which vertices, as well as edges, have capacities. That is, the total positive ﬂow entering any given vertex is subject to a capacity constraint. Show that determining the maximum ﬂow in a network with edge and vertex capacities can be reduced to an ordinary maximum-ﬂow problem on a ﬂow network of comparable size.

Problems for Chapter 26 (a) (b) Figure 26.11 Grids for the escape problem. Starting points are black, and other grid vertices are white. (a) A grid with an escape, shown by shaded paths. (b) A grid with no escape. b. Describe an efﬁcient algorithm to solve the escape problem, and analyze its running time. 26-2 Minimum path cover A path cover of a directed graph G D .V; E/ is a set P of vertex-disjoint paths such that every vertex in V is included in exactly one path in P . Paths may start and end anywhere, and they may be of any length, including 0. A minimum path cover of G is a path cover containing the fewest possible paths. a. Give an efﬁcient algorithm to ﬁnd a minimum path cover of a directed acyclic graph G D .V; E/. (Hint: Assuming that V D f1; 2; : : : ; ng, construct the graph G0 D .V 0; E0/, where V 0 D fx0; x1; : : : ; xng [ fy0; y1; : : : ; yng ; E0 D f.x0; xi/ W i 2 V g [ f.yi; y0/ W i 2 V g [ f.xi; yj/ W .i; j / 2 Eg ; and run a maximum-ﬂow algorithm.) b. Does your algorithm work for directed graphs that contain cycles? Explain. 26-3 Algorithmic consulting Professor Gore wants to open up an algorithmic consulting company. He has identiﬁed n important subareas of algorithms (roughly corresponding to different portions of this textbook), which he represents by the set A D fA1; A2; : : : ; Ang. In each subarea Ak, he can hire an expert in that area for ck dollars. The consulting company has lined up a set J D fJ1; J2; : : : ; Jmg of potential jobs. In order to perform job Ji, the company needs to have hired experts in a subset Ri  A of

subareas. Each expert can work on multiple jobs simultaneously. If the company chooses to accept job Ji, it must have hired experts in all subareas in Ri, and it will take in revenue of pi dollars.

Professor Gore’s job is to determine which subareas to hire experts in and which jobs to accept in order to maximize the net revenue, which is the total income from jobs accepted minus the total cost of employing the experts.

Consider the following ﬂow network G. It contains a source vertex s, vertices A1; A2; : : : ; An, vertices J1; J2; : : : ; Jm, and a sink vertex t. For k D 1; 2 : : : ; n, the ﬂow network contains an edge .s; Ak/ with capacity c.s; Ak/ D ck, and for i D 1; 2; : : : ; m, the ﬂow network contains an edge .Ji; t/ with capacity c.Ji; t/ D pi. For k D 1; 2; : : : ; n and i D 1; 2; : : : ; m, if Ak 2 Ri, then G contains an edge .Ak; Ji/ with capacity c.Ak; Ji/ D 1. a. Show that if Ji 2 T for a ﬁnite-capacity cut .S; T / of G, then Ak 2 T for each Ak 2 Ri. b. Show how to determine the maximum net revenue from the capacity of a minimum cut of G and the given pi values. c. Give an efﬁcient algorithm to determine which jobs to accept and which experts to hire. Analyze the running time of your algorithm in terms of m, n, and r D Pm iD1 jRij. 26-4 Updating maximum ﬂow Let G D .V; E/ be a ﬂow network with source s, sink t, and integer capacities.

Suppose that we are given a maximum ﬂow in G. a. Suppose that we increase the capacity of a single edge .u; / 2 E by 1. Give an O.V C E/-time algorithm to update the maximum ﬂow. b. Suppose that we decrease the capacity of a single edge .u; / 2 E by 1. Give an O.V C E/-time algorithm to update the maximum ﬂow. 26-5 Maximum ﬂow by scaling Let G D .V; E/ be a ﬂow network with source s, sink t, and an integer capacity c.u; / on each edge .u; / 2 E. Let C D max.u;/2E c.u; /. a. Argue that a minimum cut of G has capacity at most C jEj. b. For a given number K, show how to ﬁnd an augmenting path of capacity at least K in O.E/ time, if such a path exists.

Problems for Chapter 26 We can use the following modiﬁcation of FORD-FULKERSON-METHOD to compute a maximum ﬂow in G:

MAX-FLOW-BY-SCALING.G; s; t/ C D max.u;/2E c.u; / initialize ﬂow f to 0 K D 2blg Cc while K  1 while there exists an augmenting path p of capacity at least K augment ﬂow f along p K D K=2 return f c. Argue that MAX-FLOW-BY-SCALING returns a maximum ﬂow. d. Show that the capacity of a minimum cut of the residual network Gf is at most 2K jEj each time line 4 is executed. e. Argue that the inner while loop of lines 5–6 executes O.E/ times for each value of K. f. Conclude that MAX-FLOW-BY-SCALING can be implemented so that it runs in O.E2 lg C/ time. 26-6 The Hopcroft-Karp bipartite matching algorithm In this problem, we describe a faster algorithm, due to Hopcroft and Karp, for ﬁnding a maximum matching in a bipartite graph. The algorithm runs in O. p V E/ time. Given an undirected, bipartite graph G D .V; E/, where V D L [ R and all edges have exactly one endpoint in L, let M be a matching in G. We say that a simple path P in G is an augmenting path with respect to M if it starts at an unmatched vertex in L, ends at an unmatched vertex in R, and its edges belong alternately to M and E  M. (This deﬁnition of an augmenting path is related to, but different from, an augmenting path in a ﬂow network.) In this problem, we treat a path as a sequence of edges, rather than as a sequence of vertices. A shortest augmenting path with respect to a matching M is an augmenting path with a minimum number of edges.

Given two sets A and B, the symmetric difference A˚B is deﬁned as .AB/[ .B  A/, that is, the elements that are in exactly one of the two sets.

a. Show that if M is a matching and P is an augmenting path with respect to M, then the symmetric difference M ˚ P is a matching and jM ˚ P j D jMj C 1.

Show that if P1; P2; : : : ; Pk are vertex-disjoint augmenting paths with respect to M, then the symmetric difference M ˚ .P1 [ P2 [    [ Pk/ is a matching with cardinality jMj C k. The general structure of our algorithm is the following:

HOPCROFT-KARP.G/ M D ; repeat let P D fP1; P2; : : : ; Pkg be a maximal set of vertex-disjoint shortest augmenting paths with respect to M M D M ˚ .P1 [ P2 [    [ Pk/ until P == ; return M The remainder of this problem asks you to analyze the number of iterations in the algorithm (that is, the number of iterations in the repeat loop) and to describe an implementation of line 3. b. Given two matchings M and M  in G, show that every vertex in the graph G0 D .V; M ˚ M / has degree at most 2. Conclude that G0 is a disjoint union of simple paths or cycles. Argue that edges in each such simple path or cycle belong alternately to M or M . Prove that if jMj  jM j, then M ˚ M  contains at least jM j  jMj vertex-disjoint augmenting paths with respect to M.

Let l be the length of a shortest augmenting path with respect to a matching M, and let P1; P2; : : : ; Pk be a maximal set of vertex-disjoint augmenting paths of length l with respect to M. Let M 0 D M ˚.P1[  [Pk/, and suppose that P is a shortest augmenting path with respect to M 0. c. Show that if P is vertex-disjoint from P1; P2; : : : ; Pk, then P has more than l edges. d. Now suppose that P is not vertex-disjoint from P1; P2; : : : ; Pk. Let A be the set of edges .M ˚ M 0/ ˚ P . Show that A D .P1 [ P2 [    [ Pk/ ˚ P and that jAj  .k C 1/l. Conclude that P has more than l edges. e. Prove that if a shortest augmenting path with respect to M has l edges, the size of the maximum matching is at most jMj C jV j =.l C 1/.

Notes for Chapter 26 f. Show that the number of repeat loop iterations in the algorithm is at most 2 p jV j. (Hint: By how much can M grow after iteration number p jV j?) g. Give an algorithm that runs in O.E/ time to ﬁnd a maximal set of vertexdisjoint shortest augmenting paths P1; P2; : : : ; Pk for a given matching M.

Conclude that the total running time of HOPCROFT-KARP is O. p V E/.

Chapter notes Ahuja, Magnanti, and Orlin [7], Even [103], Lawler [224], Papadimitriou and Steiglitz [271], and Tarjan [330] are good references for network ﬂow and related algorithms. Goldberg, Tardos, and Tarjan [139] also provide a nice survey of algorithms for network-ﬂow problems, and Schrijver [304] has written an interesting review of historical developments in the ﬁeld of network ﬂows. The Ford-Fulkerson method is due to Ford and Fulkerson [109], who originated the formal study of many of the problems in the area of network ﬂow, including the maximum-ﬂow and bipartite-matching problems. Many early implementations of the Ford-Fulkerson method found augmenting paths using breadth-ﬁrst search; Edmonds and Karp [102], and independently Dinic [89], proved that this strategy yields a polynomial-time algorithm. A related idea, that of using “blocking ﬂows,” was also ﬁrst developed by Dinic [89]. Karzanov [202] ﬁrst developed the idea of preﬂows. The push-relabel method is due to Goldberg [136] and Goldberg and Tarjan [140]. Goldberg and Tarjan gave an O.V 3/-time algorithm that uses a queue to maintain the set of overﬂowing vertices, as well as an algorithm that uses dynamic trees to achieve a running time of O.VE lg.V 2=E C2//. Several other researchers have developed push-relabel maximum-ﬂow algorithms. Ahuja and Orlin [9] and Ahuja, Orlin, and Tarjan [10] gave algorithms that used scaling. Cheriyan and Maheshwari [62] proposed pushing ﬂow from the overﬂowing vertex of maximum height. Cheriyan and Hagerup [61] suggested randomly permuting the neighbor lists, and several researchers [14, 204, 276] developed clever derandomizations of this idea, leading to a sequence of faster algorithms. The algorithm of King, Rao, and Tarjan [204] is the fastest such algorithm and runs in O.VE logE=.V lg V / V / time. The asymptotically fastest algorithm to date for the maximum-ﬂow problem, by Goldberg and Rao [138], runs in time O.min.V 2=3; E1=2/E lg.V 2=E C 2/ lg C/, where C D max.u;/2E c.u; /. This algorithm does not use the push-relabel method but instead is based on ﬁnding blocking ﬂows. All previous maximum- ﬂow algorithms, including the ones in this chapter, use some notion of distance (the push-relabel algorithms use the analogous notion of height), with a length of 1

assigned implicitly to each edge. This new algorithm takes a different approach and assigns a length of 0 to high-capacity edges and a length of 1 to low-capacity edges. Informally, with respect to these lengths, shortest paths from the source to the sink tend have high capacity, which means that fewer iterations need be performed. In practice, push-relabel algorithms currently dominate augmenting-path or linear-programming based algorithms for the maximum-ﬂow problem. A study by Cherkassky and Goldberg [63] underscores the importance of using two heuristics when implementing a push-relabel algorithm. The ﬁrst heuristic is to periodically perform a breadth-ﬁrst search of the residual network in order to obtain more accurate height values. The second heuristic is the gap heuristic, described in Exercise 26.5-5. Cherkassky and Goldberg conclude that the best choice of pushrelabel variants is the one that chooses to discharge the overﬂowing vertex with the maximum height. The best algorithm to date for maximum bipartite matching, discovered by Hopcroft and Karp [176], runs in O. p V E/ time and is described in Problem 26-6. The book by Lov´asz and Plummer [239] is an excellent reference on matching problems.
