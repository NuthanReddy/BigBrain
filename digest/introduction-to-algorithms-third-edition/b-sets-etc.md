# B Sets, Etc.

B
Sets, Etc.
Many chapters of this book touch on the elements of discrete mathematics. This
appendix reviews more completely the notations, deﬁnitions, and elementary prop-
erties of sets, relations, functions, graphs, and trees. If you are already well versed
in this material, you can probably just skim this chapter.
B.1
Sets
A set is a collection of distinguishable objects, called its members or elements. If
an object x is a member of a set S, we write x 2 S (read “x is a member of S”
or, more brieﬂy, “x is in S”). If x is not a member of S, we write x 62 S. We
can describe a set by explicitly listing its members as a list inside braces. For
example, we can deﬁne a set S to contain precisely the numbers 1, 2, and 3 by
writing S D f1; 2; 3g. Since 2 is a member of the set S, we can write 2 2 S, and
since 4 is not a member, we have 4 … S. A set cannot contain the same object more
than once,1 and its elements are not ordered. Two sets A and B are equal, written
A D B, if they contain the same elements. For example, f1; 2; 3; 1g D f1; 2; 3g D
f3; 2; 1g.
We adopt special notations for frequently encountered sets:

; denotes the empty set, that is, the set containing no members.

Z denotes the set of integers, that is, the set f: : : ; 2; 1; 0; 1; 2; : : :g.

R denotes the set of real numbers.

N denotes the set of natural numbers, that is, the set f0; 1; 2; : : :g.2
1A variation of a set, which can contain the same object more than once, is called a multiset.
2Some authors start the natural numbers with 1 instead of 0. The modern trend seems to be to start
with 0.

B.1
Sets
1159
If all the elements of a set A are contained in a set B, that is, if x 2 A implies
x 2 B, then we write A  B and say that A is a subset of B. A set A is a
proper subset of B, written A 
 B, if A  B but A ¤ B. (Some authors use the
symbol “
” to denote the ordinary subset relation, rather than the proper-subset
relation.) For any set A, we have A  A. For two sets A and B, we have A D B
if and only if A  B and B  A. For any three sets A, B, and C, if A  B
and B  C, then A  C. For any set A, we have ;  A.
We sometimes deﬁne sets in terms of other sets. Given a set A, we can deﬁne a
set B  A by stating a property that distinguishes the elements of B. For example,
we can deﬁne the set of even integers by fx W x 2 Z and x=2 is an integerg. The
colon in this notation is read “such that.” (Some authors use a vertical bar in place
of the colon.)
Given two sets A and B, we can also deﬁne new sets by applying set operations:

The intersection of sets A and B is the set
A \ B D fx W x 2 A and x 2 Bg :

The union of sets A and B is the set
A [ B D fx W x 2 A or x 2 Bg :

The difference between two sets A and B is the set
A  B D fx W x 2 A and x … Bg :
Set operations obey the following laws:
Empty set laws:
A \ ;
D
; ;
A [ ;
D
A :
Idempotency laws:
A \ A
D
A ;
A [ A
D
A :
Commutative laws:
A \ B
D
B \ A ;
A [ B
D
B [ A :

1160
Appendix B
Sets, Etc.
A
A
A
A
A
A
B
B
B
B
B


.B \ C/
[
[
D
D
D
D
A  .B \ C/
.A  B/
.A  C/
C
C
C
C
C
Figure B.1
A Venn diagram illustrating the ﬁrst of DeMorgan’s laws (B.2). Each of the sets A, B,
and C is represented as a circle.
Associative laws:
A \ .B \ C/
D
.A \ B/ \ C ;
A [ .B [ C/
D
.A [ B/ [ C :
Distributive laws:
A \ .B [ C/
D
.A \ B/ [ .A \ C/ ;
A [ .B \ C/
D
.A [ B/ \ .A [ C/ :
(B.1)
Absorption laws:
A \ .A [ B/
D
A ;
A [ .A \ B/
D
A :
DeMorgan’s laws:
A  .B \ C/
D
.A  B/ [ .A  C/ ;
A  .B [ C/
D
.A  B/ \ .A  C/ :
(B.2)
Figure B.1 illustrates the ﬁrst of DeMorgan’s laws, using a Venn diagram: a graph-
ical picture in which sets are represented as regions of the plane.
Often, all the sets under consideration are subsets of some larger set U called the
universe. For example, if we are considering various sets made up only of integers,
the set Z of integers is an appropriate universe. Given a universe U , we deﬁne the
complement of a set A as A D U  A D fx W x 2 U and x 62 Ag. For any set
A  U , we have the following laws:
A
D
A ;
A \ A
D
; ;
A [ A
D
U :

B.1
Sets
1161
We can rewrite DeMorgan’s laws (B.2) with set complements. For any two sets
B; C  U , we have
B \ C
D
B [ C ;
B [ C
D
B \ C :
Two sets A and B are disjoint if they have no elements in common, that is, if
A\B D ;. A collection S D fSig of nonempty sets forms a partition of a set S if

the sets are pairwise disjoint, that is, Si; Sj 2 S and i ¤ j imply Si \ Sj D ;,
and

their union is S, that is,
S D
[
Si 2S
Si :
In other words, S forms a partition of S if each element of S appears in exactly
one Si 2 S.
The number of elements in a set is the cardinality (or size) of the set, denoted jSj.
Two sets have the same cardinality if their elements can be put into a one-to-one
correspondence. The cardinality of the empty set is j;j D 0. If the cardinality of a
set is a natural number, we say the set is ﬁnite; otherwise, it is inﬁnite. An inﬁnite
set that can be put into a one-to-one correspondence with the natural numbers N is
countably inﬁnite; otherwise, it is uncountable. For example, the integers Z are
countable, but the reals R are uncountable.
For any two ﬁnite sets A and B, we have the identity
jA [ Bj D jAj C jBj  jA \ Bj ;
(B.3)
from which we can conclude that
jA [ Bj  jAj C jBj :
If A and B are disjoint, then jA \ Bj D 0 and thus jA [ Bj D jAj C jBj. If
A  B, then jAj  jBj.
A ﬁnite set of n elements is sometimes called an n-set. A 1-set is called a
singleton. A subset of k elements of a set is sometimes called a k-subset.
We denote the set of all subsets of a set S, including the empty set and S itself,
by 2S; we call 2S the power set of S. For example, 2fa;bg D f;; fag ; fbg ; fa; bgg.
The power set of a ﬁnite set S has cardinality 2jSj (see Exercise B.1-5).
We sometimes care about setlike structures in which the elements are ordered.
An ordered pair of two elements a and b is denoted .a; b/ and is deﬁned formally
as the set .a; b/ D fa; fa; bgg. Thus, the ordered pair .a; b/ is not the same as the
ordered pair .b; a/.

1162
Appendix B
Sets, Etc.
The Cartesian product of two sets A and B, denoted A 	 B, is the set of all
ordered pairs such that the ﬁrst element of the pair is an element of A and the
second is an element of B. More formally,
A 	 B D f.a; b/ W a 2 A and b 2 Bg :
For example, fa; bg	fa; b; cg D f.a; a/; .a; b/; .a; c/; .b; a/; .b; b/; .b; c/g. When
A and B are ﬁnite sets, the cardinality of their Cartesian product is
jA 	 Bj D jAj  jBj :
(B.4)
The Cartesian product of n sets A1; A2; : : : ; An is the set of n-tuples
A1 	 A2 	    	 An D f.a1; a2; : : : ; an/ W ai 2 Ai for i D 1; 2; : : : ; ng ;
whose cardinality is
jA1 	 A2 	    	 Anj D jA1j  jA2j    jAnj
if all sets are ﬁnite. We denote an n-fold Cartesian product over a single set A by
the set
An D A 	 A 	    	 A ;
whose cardinality is jAnj D jAjn if A is ﬁnite. We can also view an n-tuple as a
ﬁnite sequence of length n (see page 1166).
Exercises
B.1-1
Draw Venn diagrams that illustrate the ﬁrst of the distributive laws (B.1).
B.1-2
Prove the generalization of DeMorgan’s laws to any ﬁnite collection of sets:
A1 \ A2 \    \ An
D
A1 [ A2 [    [ An ;
A1 [ A2 [    [ An
D
A1 \ A2 \    \ An :

B.2
Relations
1163
B.1-3
?
Prove the generalization of equation (B.3), which is called the principle of inclu-
sion and exclusion:
jA1 [ A2 [    [ Anj D
jA1j C jA2j C    C jAnj
 jA1 \ A2j  jA1 \ A3j    
(all pairs)
C jA1 \ A2 \ A3j C   
(all triples)
:::
C .1/n1 jA1 \ A2 \    \ Anj :
B.1-4
Show that the set of odd natural numbers is countable.
B.1-5
Show that for any ﬁnite set S, the power set 2S has 2jSj elements (that is, there
are 2jSj distinct subsets of S).
B.1-6
Give an inductive deﬁnition for an n-tuple by extending the set-theoretic deﬁnition
for an ordered pair.
B.2
Relations
A binary relation R on two sets A and B is a subset of the Cartesian product A	B.
If .a; b/ 2 R, we sometimes write a R b. When we say that R is a binary relation
on a set A, we mean that R is a subset of A 	 A. For example, the “less than”
relation on the natural numbers is the set f.a; b/ W a; b 2 N and a < bg. An n-ary
relation on sets A1; A2; : : : ; An is a subset of A1 	 A2 	    	 An.
A binary relation R  A 	 A is reﬂexive if
a R a
for all a 2 A. For example, “D” and “” are reﬂexive relations on N, but “<” is
not. The relation R is symmetric if
a R b implies b R a
for all a; b 2 A. For example, “D” is symmetric, but “<” and “” are not. The
relation R is transitive if
a R b and b R c imply a R c

1164
Appendix B
Sets, Etc.
for all a; b; c 2 A. For example, the relations “<,” “,” and “D” are transitive, but
the relation R D f.a; b/ W a; b 2 N and a D b  1g is not, since 3 R 4 and 4 R 5
do not imply 3 R 5.
A relation that is reﬂexive, symmetric, and transitive is an equivalence relation.
For example, “D” is an equivalence relation on the natural numbers, but “<” is not.
If R is an equivalence relation on a set A, then for a 2 A, the equivalence class
of a is the set Œa D fb 2 A W a R bg, that is, the set of all elements equivalent to a.
For example, if we deﬁne R D f.a; b/ W a; b 2 N and a C b is an even numberg,
then R is an equivalence relation, since a C a is even (reﬂexive), a C b is even
implies b C a is even (symmetric), and a C b is even and b C c is even imply
a C c is even (transitive). The equivalence class of 4 is Œ4 D f0; 2; 4; 6; : : :g, and
the equivalence class of 3 is Œ3 D f1; 3; 5; 7; : : :g. A basic theorem of equivalence
classes is the following.
Theorem B.1 (An equivalence relation is the same as a partition)
The equivalence classes of any equivalence relation R on a set A form a partition
of A, and any partition of A determines an equivalence relation on A for which the
sets in the partition are the equivalence classes.
Proof
For the ﬁrst part of the proof, we must show that the equivalence classes
of R are nonempty, pairwise-disjoint sets whose union is A. Because R is reﬂex-
ive, a 2 Œa, and so the equivalence classes are nonempty; moreover, since every
element a 2 A belongs to the equivalence class Œa, the union of the equivalence
classes is A. It remains to show that the equivalence classes are pairwise disjoint,
that is, if two equivalence classes Œa and Œb have an element c in common, then
they are in fact the same set. Suppose that a R c and b R c. By symmetry, c R b,
and by transitivity, a R b. Thus, for any arbitrary element x 2 Œa, we have x R a
and, by transitivity, x R b, and thus Œa  Œb. Similarly, Œb  Œa, and thus
Œa D Œb.
For the second part of the proof, let A D fAig be a partition of A, and deﬁne
R D f.a; b/ W there exists i such that a 2 Ai and b 2 Aig. We claim that R is an
equivalence relation on A. Reﬂexivity holds, since a 2 Ai implies a R a. Symme-
try holds, because if a R b, then a and b are in the same set Ai, and hence b R a.
If a R b and b R c, then all three elements are in the same set Ai, and thus a R c
and transitivity holds. To see that the sets in the partition are the equivalence
classes of R, observe that if a 2 Ai, then x 2 Œa implies x 2 Ai, and x 2 Ai
implies x 2 Œa.
A binary relation R on a set A is antisymmetric if
a R b and b R a imply a D b :

B.2
Relations
1165
For example, the “” relation on the natural numbers is antisymmetric, since a  b
and b  a imply a D b. A relation that is reﬂexive, antisymmetric, and transitive
is a partial order, and we call a set on which a partial order is deﬁned a partially
ordered set. For example, the relation “is a descendant of” is a partial order on the
set of all people (if we view individuals as being their own descendants).
In a partially ordered set A, there may be no single “maximum” element a such
that b R a for all b 2 A. Instead, the set may contain several maximal elements a
such that for no b 2 A, where b ¤ a, is it the case that a R b. For example, a
collection of different-sized boxes may contain several maximal boxes that don’t
ﬁt inside any other box, yet it has no single “maximum” box into which any other
box will ﬁt.3
A relation R on a set A is a total relation if for all a; b 2 A, we have a R b
or b R a (or both), that is, if every pairing of elements of A is related by R. A
partial order that is also a total relation is a total order or linear order. For example,
the relation “” is a total order on the natural numbers, but the “is a descendant
of” relation is not a total order on the set of all people, since there are individuals
neither of whom is descended from the other. A total relation that is transitive, but
not necessarily reﬂexive and antisymmetric, is a total preorder.
Exercises
B.2-1
Prove that the subset relation “” on all subsets of Z is a partial order but not a
total order.
B.2-2
Show that for any positive integer n, the relation “equivalent modulo n” is an equiv-
alence relation on the integers. (We say that a  b .mod n/ if there exists an
integer q such that a  b D qn.) Into what equivalence classes does this relation
partition the integers?
B.2-3
Give examples of relations that are
a. reﬂexive and symmetric but not transitive,
b. reﬂexive and transitive but not symmetric,
c. symmetric and transitive but not reﬂexive.
3To be precise, in order for the “ﬁt inside” relation to be a partial order, we need to view a box as
ﬁtting inside itself.

1166
Appendix B
Sets, Etc.
B.2-4
Let S be a ﬁnite set, and let R be an equivalence relation on S 	 S. Show that if
in addition R is antisymmetric, then the equivalence classes of S with respect to R
are singletons.
B.2-5
Professor Narcissus claims that if a relation R is symmetric and transitive, then it is
also reﬂexive. He offers the following proof. By symmetry, a R b implies b R a.
Transitivity, therefore, implies a R a. Is the professor correct?
B.3
Functions
Given two sets A and B, a function f is a binary relation on A and B such that
for all a 2 A, there exists precisely one b 2 B such that .a; b/ 2 f . The set A is
called the domain of f , and the set B is called the codomain of f . We sometimes
write f W A ! B; and if .a; b/ 2 f , we write b D f .a/, since b is uniquely
determined by the choice of a.
Intuitively, the function f assigns an element of B to each element of A. No
element of A is assigned two different elements of B, but the same element of B
can be assigned to two different elements of A. For example, the binary relation
f D f.a; b/ W a; b 2 N and b D a mod 2g
is a function f W N ! f0; 1g, since for each natural number a, there is exactly one
value b in f0; 1g such that b D a mod 2. For this example, 0 D f .0/, 1 D f .1/,
0 D f .2/, etc. In contrast, the binary relation
g D f.a; b/ W a; b 2 N and a C b is eveng
is not a function, since .1; 3/ and .1; 5/ are both in g, and thus for the choice a D 1,
there is not precisely one b such that .a; b/ 2 g.
Given a function f W A ! B, if b D f .a/, we say that a is the argument of f
and that b is the value of f at a. We can deﬁne a function by stating its value for
every element of its domain. For example, we might deﬁne f .n/ D 2n for n 2 N,
which means f D f.n; 2n/ W n 2 Ng. Two functions f and g are equal if they
have the same domain and codomain and if, for all a in the domain, f .a/ D g.a/.
A ﬁnite sequence of length n is a function f whose domain is the set of n
integers f0; 1; : : : ; n  1g. We often denote a ﬁnite sequence by listing its values:
hf .0/; f .1/; : : : ; f .n  1/i. An inﬁnite sequence is a function whose domain is
the set N of natural numbers. For example, the Fibonacci sequence, deﬁned by
recurrence (3.22), is the inﬁnite sequence h0; 1; 1; 2; 3; 5; 8; 13; 21; : : :i.

B.3
Functions
1167
When the domain of a function f is a Cartesian product, we often omit the extra
parentheses surrounding the argument of f . For example, if we had a function
f W A1 	 A2 	    	 An ! B, we would write b D f .a1; a2; : : : ; an/ instead
of b D f ..a1; a2; : : : ; an//. We also call each ai an argument to the function f ,
though technically the (single) argument to f is the n-tuple .a1; a2; : : : ; an/.
If f W A ! B is a function and b D f .a/, then we sometimes say that b is the
image of a under f . The image of a set A0  A under f is deﬁned by
f .A0/ D fb 2 B W b D f .a/ for some a 2 A0g :
The range of f is the image of its domain, that is, f .A/. For example, the range
of the function f W N ! N deﬁned by f .n/ D 2n is f .N/ D fm W m D 2n for
some n 2 Ng, in other words, the set of nonnegative even integers.
A function is a surjection if its range is its codomain. For example, the function
f .n/ D bn=2c is a surjective function from N to N, since every element in N
appears as the value of f for some argument. In contrast, the function f .n/ D 2n
is not a surjective function from N to N, since no argument to f can produce 3 as a
value. The function f .n/ D 2n is, however, a surjective function from the natural
numbers to the even numbers. A surjection f W A ! B is sometimes described as
mapping A onto B. When we say that f is onto, we mean that it is surjective.
A function f W A ! B is an injection if distinct arguments to f produce
distinct values, that is, if a ¤ a0 implies f .a/ ¤ f .a0/. For example, the function
f .n/ D 2n is an injective function from N to N, since each even number b is the
image under f of at most one element of the domain, namely b=2. The function
f .n/ D bn=2c is not injective, since the value 1 is produced by two arguments: 2
and 3. An injection is sometimes called a one-to-one function.
A function f W A ! B is a bijection if it is injective and surjective. For example,
the function f .n/ D .1/n dn=2e is a bijection from N to Z:
0
!
0 ;
1
!
1 ;
2
!
1 ;
3
!
2 ;
4
!
2 ;
:::
The function is injective, since no element of Z is the image of more than one
element of N. It is surjective, since every element of Z appears as the image of
some element of N. Hence, the function is bijective. A bijection is sometimes
called a one-to-one correspondence, since it pairs elements in the domain and
codomain. A bijection from a set A to itself is sometimes called a permutation.
When a function f is bijective, we deﬁne its inverse f 1 as
f 1.b/ D a if and only if f .a/ D b :

1168
Appendix B
Sets, Etc.
For example, the inverse of the function f .n/ D .1/n dn=2e is
f 1.m/ D
(
2m
if m  0 ;
2m  1
if m < 0 :
Exercises
B.3-1
Let A and B be ﬁnite sets, and let f W A ! B be a function. Show that
a. if f is injective, then jAj  jBj;
b. if f is surjective, then jAj  jBj.
B.3-2
Is the function f .x/ D x C 1 bijective when the domain and the codomain are N?
Is it bijective when the domain and the codomain are Z?
B.3-3
Give a natural deﬁnition for the inverse of a binary relation such that if a relation
is in fact a bijective function, its relational inverse is its functional inverse.
B.3-4
?
Give a bijection from Z to Z 	 Z.
B.4
Graphs
This section presents two kinds of graphs: directed and undirected. Certain def-
initions in the literature differ from those given here, but for the most part, the
differences are slight. Section 22.1 shows how we can represent graphs in com-
puter memory.
A directed graph (or digraph) G is a pair .V; E/, where V is a ﬁnite set and E
is a binary relation on V . The set V is called the vertex set of G, and its elements
are called vertices (singular: vertex). The set E is called the edge set of G, and its
elements are called edges. Figure B.2(a) is a pictorial representation of a directed
graph on the vertex set f1; 2; 3; 4; 5; 6g. Vertices are represented by circles in the
ﬁgure, and edges are represented by arrows. Note that self-loops—edges from a
vertex to itself—are possible.
In an undirected graph G D .V; E/, the edge set E consists of unordered
pairs of vertices, rather than ordered pairs. That is, an edge is a set fu; g, where

B.4
Graphs
1169
1
2
3
4
5
6
(a)
1
2
3
4
5
6
(b)
1
2
3
6
(c)
Figure B.2
Directed and undirected graphs.
(a) A directed graph G D .V; E/, where V D
f1; 2; 3; 4; 5; 6g and E D f.1; 2/; .2; 2/; .2; 4/; .2; 5/; .4; 1/; .4; 5/; .5; 4/; .6; 3/g. The edge .2; 2/
is a self-loop.
(b) An undirected graph G D .V; E/, where V
D f1; 2; 3; 4; 5; 6g and E D
f.1; 2/; .1; 5/; .2; 5/; .3; 6/g. The vertex 4 is isolated. (c) The subgraph of the graph in part (a)
induced by the vertex set f1; 2; 3; 6g.
u;  2 V and u ¤ . By convention, we use the notation .u; / for an edge, rather
than the set notation fu; g, and we consider .u; / and .; u/ to be the same edge.
In an undirected graph, self-loops are forbidden, and so every edge consists of two
distinct vertices. Figure B.2(b) is a pictorial representation of an undirected graph
on the vertex set f1; 2; 3; 4; 5; 6g.
Many deﬁnitions for directed and undirected graphs are the same, although cer-
tain terms have slightly different meanings in the two contexts. If .u; / is an edge
in a directed graph G D .V; E/, we say that .u; / is incident from or leaves
vertex u and is incident to or enters vertex . For example, the edges leaving ver-
tex 2 in Figure B.2(a) are .2; 2/, .2; 4/, and .2; 5/. The edges entering vertex 2 are
.1; 2/ and .2; 2/. If .u; / is an edge in an undirected graph G D .V; E/, we say
that .u; / is incident on vertices u and . In Figure B.2(b), the edges incident on
vertex 2 are .1; 2/ and .2; 5/.
If .u; / is an edge in a graph G D .V; E/, we say that vertex  is adjacent to
vertex u. When the graph is undirected, the adjacency relation is symmetric. When
the graph is directed, the adjacency relation is not necessarily symmetric. If  is
adjacent to u in a directed graph, we sometimes write u ! . In parts (a) and (b)
of Figure B.2, vertex 2 is adjacent to vertex 1, since the edge .1; 2/ belongs to both
graphs. Vertex 1 is not adjacent to vertex 2 in Figure B.2(a), since the edge .2; 1/
does not belong to the graph.
The degree of a vertex in an undirected graph is the number of edges incident on
it. For example, vertex 2 in Figure B.2(b) has degree 2. A vertex whose degree is 0,
such as vertex 4 in Figure B.2(b), is isolated. In a directed graph, the out-degree
of a vertex is the number of edges leaving it, and the in-degree of a vertex is the
number of edges entering it. The degree of a vertex in a directed graph is its in-

1170
Appendix B
Sets, Etc.
degree plus its out-degree. Vertex 2 in Figure B.2(a) has in-degree 2, out-degree 3,
and degree 5.
A path of length k from a vertex u to a vertex u0 in a graph G D .V; E/
is a sequence h0; 1; 2; : : : ; ki of vertices such that u D 0, u0 D k, and
.i1; i/ 2 E for i D 1; 2; : : : ; k. The length of the path is the number of
edges in the path. The path contains the vertices 0; 1; : : : ; k and the edges
.0; 1/; .1; 2/; : : : ; .k1; k/. (There is always a 0-length path from u to u.) If
there is a path p from u to u0, we say that u0 is reachable from u via p, which we
sometimes write as u
p; u0 if G is directed. A path is simple4 if all vertices in the
path are distinct. In Figure B.2(a), the path h1; 2; 5; 4i is a simple path of length 3.
The path h2; 5; 4; 5i is not simple.
A subpath of path p D h0; 1; : : : ; ki is a contiguous subsequence of its ver-
tices. That is, for any 0  i  j  k, the subsequence of vertices hi; iC1; : : : ; ji
is a subpath of p.
In a directed graph, a path h0; 1; : : : ; ki forms a cycle if 0 D k and the
path contains at least one edge. The cycle is simple if, in addition, 1; 2; : : : ; k
are distinct. A self-loop is a cycle of length 1. Two paths h0; 1; 2; : : : ; k1; 0i
and h0
0; 0
1; 0
2; : : : ; 0
k1; 0
0i form the same cycle if there exists an integer j such
that 0
i D .iCj/ mod k for i D 0; 1; : : : ; k  1. In Figure B.2(a), the path h1; 2; 4; 1i
forms the same cycle as the paths h2; 4; 1; 2i and h4; 1; 2; 4i. This cycle is simple,
but the cycle h1; 2; 4; 5; 4; 1i is not. The cycle h2; 2i formed by the edge .2; 2/ is
a self-loop. A directed graph with no self-loops is simple. In an undirected graph,
a path h0; 1; : : : ; ki forms a cycle if k  3 and 0 D k; the cycle is simple if
1; 2; : : : ; k are distinct. For example, in Figure B.2(b), the path h1; 2; 5; 1i is a
simple cycle. A graph with no cycles is acyclic.
An undirected graph is connected if every vertex is reachable from all other
vertices. The connected components of a graph are the equivalence classes of
vertices under the “is reachable from” relation. The graph in Figure B.2(b) has
three connected components: f1; 2; 5g, f3; 6g, and f4g. Every vertex in f1; 2; 5g is
reachable from every other vertex in f1; 2; 5g. An undirected graph is connected
if it has exactly one connected component. The edges of a connected component
are those that are incident on only the vertices of the component; in other words,
edge .u; / is an edge of a connected component only if both u and  are vertices
of the component.
A directed graph is strongly connected if every two vertices are reachable from
each other. The strongly connected components of a directed graph are the equiv-
4Some authors refer to what we call a path as a “walk” and to what we call a simple path as just a
“path.” We use the terms “path” and “simple path” throughout this book in a manner consistent with
their deﬁnitions.

B.4
Graphs
1171
1
2
3
4
5
6
u
v
w
x
y
z
(a)
1
2
3
4
5
u
v
w
x
y
(b)
G
G′
Figure B.3
(a) A pair of isomorphic graphs. The vertices of the top graph are mapped to the
vertices of the bottom graph by f .1/ D u; f .2/ D ; f .3/ D w; f .4/ D x; f .5/ D y; f .6/ D ´.
(b) Two graphs that are not isomorphic, since the top graph has a vertex of degree 4 and the bottom
graph does not.
alence classes of vertices under the “are mutually reachable” relation. A directed
graph is strongly connected if it has only one strongly connected component. The
graph in Figure B.2(a) has three strongly connected components: f1; 2; 4; 5g, f3g,
and f6g.
All pairs of vertices in f1; 2; 4; 5g are mutually reachable.
The ver-
tices f3; 6g do not form a strongly connected component, since vertex 6 cannot
be reached from vertex 3.
Two graphs G D .V; E/ and G0 D .V 0; E0/ are isomorphic if there exists a
bijection f W V ! V 0 such that .u; / 2 E if and only if .f .u/; f .// 2 E0.
In other words, we can relabel the vertices of G to be vertices of G0, maintain-
ing the corresponding edges in G and G0. Figure B.3(a) shows a pair of iso-
morphic graphs G and G0 with respective vertex sets V D f1; 2; 3; 4; 5; 6g and
V 0 D fu; ; w; x; y; ´g. The mapping from V to V 0 given by f .1/ D u; f .2/ D ;
f .3/ D w; f .4/ D x; f .5/ D y; f .6/ D ´ provides the required bijective func-
tion. The graphs in Figure B.3(b) are not isomorphic. Although both graphs have
5 vertices and 7 edges, the top graph has a vertex of degree 4 and the bottom graph
does not.
We say that a graph G0 D .V 0; E0/ is a subgraph of G D .V; E/ if V 0  V
and E0  E. Given a set V 0  V , the subgraph of G induced by V 0 is the graph
G0 D .V 0; E0/, where
E0 D f.u; / 2 E W u;  2 V 0g :

1172
Appendix B
Sets, Etc.
The subgraph induced by the vertex set f1; 2; 3; 6g in Figure B.2(a) appears in
Figure B.2(c) and has the edge set f.1; 2/; .2; 2/; .6; 3/g.
Given an undirected graph G D .V; E/, the directed version of G is the directed
graph G0 D .V; E0/, where .u; / 2 E0 if and only if .u; / 2 E. That is, we
replace each undirected edge .u; / in G by the two directed edges .u; / and .; u/
in the directed version. Given a directed graph G D .V; E/, the undirected version
of G is the undirected graph G0 D .V; E0/, where .u; / 2 E0 if and only if u ¤ 
and .u; / 2 E. That is, the undirected version contains the edges of G “with
their directions removed” and with self-loops eliminated. (Since .u; / and .; u/
are the same edge in an undirected graph, the undirected version of a directed
graph contains it only once, even if the directed graph contains both edges .u; /
and .; u/.) In a directed graph G D .V; E/, a neighbor of a vertex u is any vertex
that is adjacent to u in the undirected version of G. That is,  is a neighbor of u if
u ¤  and either .u; / 2 E or .; u/ 2 E. In an undirected graph, u and  are
neighbors if they are adjacent.
Several kinds of graphs have special names. A complete graph is an undirected
graph in which every pair of vertices is adjacent. A bipartite graph is an undirected
graph G D .V; E/ in which V can be partitioned into two sets V1 and V2 such that
.u; / 2 E implies either u 2 V1 and  2 V2 or u 2 V2 and  2 V1. That is, all
edges go between the two sets V1 and V2. An acyclic, undirected graph is a forest,
and a connected, acyclic, undirected graph is a (free) tree (see Section B.5). We
often take the ﬁrst letters of “directed acyclic graph” and call such a graph a dag.
There are two variants of graphs that you may occasionally encounter. A multi-
graph is like an undirected graph, but it can have both multiple edges between ver-
tices and self-loops. A hypergraph is like an undirected graph, but each hyperedge,
rather than connecting two vertices, connects an arbitrary subset of vertices. Many
algorithms written for ordinary directed and undirected graphs can be adapted to
run on these graphlike structures.
The contraction of an undirected graph G D .V; E/ by an edge e D .u; / is a
graph G0 D .V 0; E0/, where V 0 D V  fu; g [ fxg and x is a new vertex. The set
of edges E0 is formed from E by deleting the edge .u; / and, for each vertex w
incident on u or , deleting whichever of .u; w/ and .; w/ is in E and adding the
new edge .x; w/. In effect, u and  are “contracted” into a single vertex.
Exercises
B.4-1
Attendees of a faculty party shake hands to greet each other, and each professor
remembers how many times he or she shook hands. At the end of the party, the
department head adds up the number of times that each professor shook hands.

B.5
Trees
1173
Show that the result is even by proving the handshaking lemma: if G D .V; E/ is
an undirected graph, then
X
2V
degree./ D 2 jEj :
B.4-2
Show that if a directed or undirected graph contains a path between two vertices u
and , then it contains a simple path between u and . Show that if a directed graph
contains a cycle, then it contains a simple cycle.
B.4-3
Show that any connected, undirected graph G D .V; E/ satisﬁes jEj  jV j  1.
B.4-4
Verify that in an undirected graph, the “is reachable from” relation is an equiv-
alence relation on the vertices of the graph. Which of the three properties of an
equivalence relation hold in general for the “is reachable from” relation on the
vertices of a directed graph?
B.4-5
What is the undirected version of the directed graph in Figure B.2(a)? What is the
directed version of the undirected graph in Figure B.2(b)?
B.4-6
?
Show that we can represent a hypergraph by a bipartite graph if we let incidence in
the hypergraph correspond to adjacency in the bipartite graph. (Hint: Let one set
of vertices in the bipartite graph correspond to vertices of the hypergraph, and let
the other set of vertices of the bipartite graph correspond to hyperedges.)
B.5
Trees
As with graphs, there are many related, but slightly different, notions of trees. This
section presents deﬁnitions and mathematical properties of several kinds of trees.
Sections 10.4 and 22.1 describe how we can represent trees in computer memory.
B.5.1
Free trees
As deﬁned in Section B.4, a free tree is a connected, acyclic, undirected graph. We
often omit the adjective “free” when we say that a graph is a tree. If an undirected
graph is acyclic but possibly disconnected, it is a forest. Many algorithms that work

1174
Appendix B
Sets, Etc.
(a)
(b)
(c)
Figure B.4
(a) A free tree. (b) A forest. (c) A graph that contains a cycle and is therefore neither
a tree nor a forest.
for trees also work for forests. Figure B.4(a) shows a free tree, and Figure B.4(b)
shows a forest. The forest in Figure B.4(b) is not a tree because it is not connected.
The graph in Figure B.4(c) is connected but neither a tree nor a forest, because it
contains a cycle.
The following theorem captures many important facts about free trees.
Theorem B.2 (Properties of free trees)
Let G D .V; E/ be an undirected graph. The following statements are equivalent.
1. G is a free tree.
2. Any two vertices in G are connected by a unique simple path.
3. G is connected, but if any edge is removed from E, the resulting graph is dis-
connected.
4. G is connected, and jEj D jV j  1.
5. G is acyclic, and jEj D jV j  1.
6. G is acyclic, but if any edge is added to E, the resulting graph contains a cycle.
Proof
(1) ) (2): Since a tree is connected, any two vertices in G are connected
by at least one simple path. Suppose, for the sake of contradiction, that vertices u
and  are connected by two distinct simple paths p1 and p2, as shown in Figure B.5.
Let w be the vertex at which the paths ﬁrst diverge; that is, w is the ﬁrst vertex
on both p1 and p2 whose successor on p1 is x and whose successor on p2 is y,
where x ¤ y. Let ´ be the ﬁrst vertex at which the paths reconverge; that is, ´ is
the ﬁrst vertex following w on p1 that is also on p2. Let p0 be the subpath of p1
from w through x to ´, and let p00 be the subpath of p2 from w through y to ´.
Paths p0 and p00 share no vertices except their endpoints. Thus, the path obtained by
concatenating p0 and the reverse of p00 is a cycle, which contradicts our assumption

B.5
Trees
1175
u
w
z
v
x
y
p′
p′′
Figure B.5
A step in the proof of Theorem B.2: if (1) G is a free tree, then (2) any two vertices
in G are connected by a unique simple path. Assume for the sake of contradiction that vertices u
and  are connected by two distinct simple paths p1 and p2. These paths ﬁrst diverge at vertex w,
and they ﬁrst reconverge at vertex ´. The path p0 concatenated with the reverse of the path p00 forms
a cycle, which yields the contradiction.
that G is a tree. Thus, if G is a tree, there can be at most one simple path between
two vertices.
(2) ) (3): If any two vertices in G are connected by a unique simple path,
then G is connected. Let .u; / be any edge in E. This edge is a path from u to ,
and so it must be the unique path from u to . If we remove .u; / from G, there
is no path from u to , and hence its removal disconnects G.
(3) ) (4): By assumption, the graph G is connected, and by Exercise B.4-3, we
have jEj  jV j  1. We shall prove jEj  jV j  1 by induction. A connected
graph with n D 1 or n D 2 vertices has n  1 edges. Suppose that G has n  3
vertices and that all graphs satisfying (3) with fewer than n vertices also satisfy
jEj  jV j  1. Removing an arbitrary edge from G separates the graph into k  2
connected components (actually k D 2). Each component satisﬁes (3), or else G
would not satisfy (3). If we view each connected component Vi, with edge set Ei,
as its own free tree, then because each component has fewer than jV j vertices, by
the inductive hypothesis we have jEij  jVij  1. Thus, the number of edges in all
components combined is at most jV j  k  jV j  2. Adding in the removed edge
yields jEj  jV j  1.
(4) ) (5): Suppose that G is connected and that jEj D jV j  1. We must show
that G is acyclic. Suppose that G has a cycle containing k vertices 1; 2; : : : ; k,
and without loss of generality assume that this cycle is simple. Let Gk D .Vk; Ek/
be the subgraph of G consisting of the cycle.
Note that jVkj D jEkj D k.
If k < jV j, there must be a vertex kC1 2 V  Vk that is adjacent to some ver-
tex i 2 Vk, since G is connected. Deﬁne GkC1 D .VkC1; EkC1/ to be the sub-
graph of G with VkC1 D Vk [ fkC1g and EkC1 D Ek [ f.i; kC1/g. Note that
jVkC1j D jEkC1j D k C 1. If k C 1 < jV j, we can continue, deﬁning GkC2 in
the same manner, and so forth, until we obtain Gn D .Vn; En/, where n D jV j,

1176
Appendix B
Sets, Etc.
Vn D V , and jEnj D jVnj D jV j. Since Gn is a subgraph of G, we have En  E,
and hence jEj  jV j, which contradicts the assumption that jEj D jV j  1. Thus,
G is acyclic.
(5) ) (6): Suppose that G is acyclic and that jEj D jV j  1. Let k be the
number of connected components of G. Each connected component is a free tree
by deﬁnition, and since (1) implies (5), the sum of all edges in all connected com-
ponents of G is jV j  k. Consequently, we must have k D 1, and G is in fact a
tree. Since (1) implies (2), any two vertices in G are connected by a unique simple
path. Thus, adding any edge to G creates a cycle.
(6) ) (1): Suppose that G is acyclic but that adding any edge to E creates a
cycle. We must show that G is connected. Let u and  be arbitrary vertices in G.
If u and  are not already adjacent, adding the edge .u; / creates a cycle in which
all edges but .u; / belong to G. Thus, the cycle minus edge .u; / must contain a
path from u to , and since u and  were chosen arbitrarily, G is connected.
B.5.2
Rooted and ordered trees
A rooted tree is a free tree in which one of the vertices is distinguished from the
others. We call the distinguished vertex the root of the tree. We often refer to a
vertex of a rooted tree as a node5 of the tree. Figure B.6(a) shows a rooted tree on
a set of 12 nodes with root 7.
Consider a node x in a rooted tree T with root r. We call any node y on the
unique simple path from r to x an ancestor of x. If y is an ancestor of x, then x is
a descendant of y. (Every node is both an ancestor and a descendant of itself.) If y
is an ancestor of x and x ¤ y, then y is a proper ancestor of x and x is a proper
descendant of y. The subtree rooted at x is the tree induced by descendants of x,
rooted at x. For example, the subtree rooted at node 8 in Figure B.6(a) contains
nodes 8, 6, 5, and 9.
If the last edge on the simple path from the root r of a tree T to a node x is .y; x/,
then y is the parent of x, and x is a child of y. The root is the only node in T with
no parent. If two nodes have the same parent, they are siblings. A node with no
children is a leaf or external node. A nonleaf node is an internal node.
5The term “node” is often used in the graph theory literature as a synonym for “vertex.” We reserve
the term “node” to mean a vertex of a rooted tree.

B.5
Trees
1177
9
6
5
8
1
12
3
10
7
11
2
4
height = 4
depth 0
depth 1
depth 2
depth 3
depth 4
(a)
9
6
5
8
12
3
10
7
11
2
4
(b)
1
Figure B.6
Rooted and ordered trees. (a) A rooted tree with height 4. The tree is drawn in a
standard way: the root (node 7) is at the top, its children (nodes with depth 1) are beneath it, their
children (nodes with depth 2) are beneath them, and so forth. If the tree is ordered, the relative left-
to-right order of the children of a node matters; otherwise it doesn’t. (b) Another rooted tree. As a
rooted tree, it is identical to the tree in (a), but as an ordered tree it is different, since the children of
node 3 appear in a different order.
The number of children of a node x in a rooted tree T equals the degree of x.6
The length of the simple path from the root r to a node x is the depth of x in T .
A level of a tree consists of all nodes at the same depth. The height of a node in a
tree is the number of edges on the longest simple downward path from the node to
a leaf, and the height of a tree is the height of its root. The height of a tree is also
equal to the largest depth of any node in the tree.
An ordered tree is a rooted tree in which the children of each node are ordered.
That is, if a node has k children, then there is a ﬁrst child, a second child, . . . ,
and a kth child. The two trees in Figure B.6 are different when considered to be
ordered trees, but the same when considered to be just rooted trees.
B.5.3
Binary and positional trees
We deﬁne binary trees recursively. A binary tree T is a structure deﬁned on a ﬁnite
set of nodes that either

contains no nodes, or
6Notice that the degree of a node depends on whether we consider T to be a rooted tree or a free tree.
The degree of a vertex in a free tree is, as in any undirected graph, the number of adjacent vertices.
In a rooted tree, however, the degree is the number of children—the parent of a node does not count
toward its degree.

1178
Appendix B
Sets, Etc.
3
2
4
1
6
7
5
(a)
3
2
4
1
6
7
5
(b)
3
2
4
1
6
7
5
(c)
Figure B.7
Binary trees. (a) A binary tree drawn in a standard way. The left child of a node is
drawn beneath the node and to the left. The right child is drawn beneath and to the right. (b) A binary
tree different from the one in (a). In (a), the left child of node 7 is 5 and the right child is absent.
In (b), the left child of node 7 is absent and the right child is 5. As ordered trees, these trees are
the same, but as binary trees, they are distinct. (c) The binary tree in (a) represented by the internal
nodes of a full binary tree: an ordered tree in which each internal node has degree 2. The leaves in
the tree are shown as squares.

is composed of three disjoint sets of nodes: a root node, a binary tree called its
left subtree, and a binary tree called its right subtree.
The binary tree that contains no nodes is called the empty tree or null tree, some-
times denoted NIL. If the left subtree is nonempty, its root is called the left child of
the root of the entire tree. Likewise, the root of a nonnull right subtree is the right
child of the root of the entire tree. If a subtree is the null tree NIL, we say that the
child is absent or missing. Figure B.7(a) shows a binary tree.
A binary tree is not simply an ordered tree in which each node has degree at
most 2. For example, in a binary tree, if a node has just one child, the position
of the child—whether it is the left child or the right child—matters. In an or-
dered tree, there is no distinguishing a sole child as being either left or right. Fig-
ure B.7(b) shows a binary tree that differs from the tree in Figure B.7(a) because of
the position of one node. Considered as ordered trees, however, the two trees are
identical.
We can represent the positioning information in a binary tree by the internal
nodes of an ordered tree, as shown in Figure B.7(c). The idea is to replace each
missing child in the binary tree with a node having no children. These leaf nodes
are drawn as squares in the ﬁgure. The tree that results is a full binary tree: each
node is either a leaf or has degree exactly 2. There are no degree-1 nodes. Conse-
quently, the order of the children of a node preserves the position information.
We can extend the positioning information that distinguishes binary trees from
ordered trees to trees with more than 2 children per node. In a positional tree, the

B.5
Trees
1179
height = 3
depth 0
depth 1
depth 2
depth 3
Figure B.8
A complete binary tree of height 3 with 8 leaves and 7 internal nodes.
children of a node are labeled with distinct positive integers. The ith child of a
node is absent if no child is labeled with integer i. A k-ary tree is a positional tree
in which for every node, all children with labels greater than k are missing. Thus,
a binary tree is a k-ary tree with k D 2.
A complete k-ary tree is a k-ary tree in which all leaves have the same depth
and all internal nodes have degree k. Figure B.8 shows a complete binary tree of
height 3. How many leaves does a complete k-ary tree of height h have? The root
has k children at depth 1, each of which has k children at depth 2, etc. Thus, the
number of leaves at depth h is kh. Consequently, the height of a complete k-ary
tree with n leaves is logk n. The number of internal nodes of a complete k-ary tree
of height h is
1 C k C k2 C    C kh1
D
h1
X
iD0
ki
D
kh  1
k  1
by equation (A.5). Thus, a complete binary tree has 2h  1 internal nodes.
Exercises
B.5-1
Draw all the free trees composed of the three vertices x, y, and ´. Draw all the
rooted trees with nodes x, y, and ´ with x as the root. Draw all the ordered trees
with nodes x, y, and ´ with x as the root. Draw all the binary trees with nodes x,
y, and ´ with x as the root.

1180
Appendix B
Sets, Etc.
B.5-2
Let G D .V; E/ be a directed acyclic graph in which there is a vertex 0 2 V
such that there exists a unique path from 0 to every vertex  2 V . Prove that the
undirected version of G forms a tree.
B.5-3
Show by induction that the number of degree-2 nodes in any nonempty binary tree
is 1 fewer than the number of leaves. Conclude that the number of internal nodes
in a full binary tree is 1 fewer than the number of leaves.
B.5-4
Use induction to show that a nonempty binary tree with n nodes has height at
least blg nc.
B.5-5
?
The internal path length of a full binary tree is the sum, taken over all internal
nodes of the tree, of the depth of each node. Likewise, the external path length is
the sum, taken over all leaves of the tree, of the depth of each leaf. Consider a full
binary tree with n internal nodes, internal path length i, and external path length e.
Prove that e D i C 2n.
B.5-6
?
Let us associate a “weight” w.x/ D 2d with each leaf x of depth d in a binary
tree T , and let L be the set of leaves of T . Prove that P
x2L w.x/  1. (This is
known as the Kraft inequality.)
B.5-7
?
Show that if L  2, then every binary tree with L leaves contains a subtree having
between L=3 and 2L=3 leaves, inclusive.
Problems
B-1
Graph coloring
Given an undirected graph G D .V; E/, a k-coloring of G is a function c W V !
f0; 1; : : : ; k  1g such that c.u/ ¤ c./ for every edge .u; / 2 E. In other words,
the numbers 0; 1; : : : ; k  1 represent the k colors, and adjacent vertices must have
different colors.
a. Show that any tree is 2-colorable.

Problems for Appendix B
1181
b. Show that the following are equivalent:
1. G is bipartite.
2. G is 2-colorable.
3. G has no cycles of odd length.
c. Let d be the maximum degree of any vertex in a graph G. Prove that we can
color G with d C 1 colors.
d. Show that if G has O.jV j/ edges, then we can color G with O.
p
jV j/ colors.
B-2
Friendly graphs
Reword each of the following statements as a theorem about undirected graphs,
and then prove it. Assume that friendship is symmetric but not reﬂexive.
a. Any group of at least two people contains at least two people with the same
number of friends in the group.
b. Every group of six people contains either at least three mutual friends or at least
three mutual strangers.
c. Any group of people can be partitioned into two subgroups such that at least
half the friends of each person belong to the subgroup of which that person is
not a member.
d. If everyone in a group is the friend of at least half the people in the group, then
the group can be seated around a table in such a way that everyone is seated
between two friends.
B-3
Bisecting trees
Many divide-and-conquer algorithms that operate on graphs require that the graph
be bisected into two nearly equal-sized subgraphs, which are induced by a partition
of the vertices. This problem investigates bisections of trees formed by removing a
small number of edges. We require that whenever two vertices end up in the same
subtree after removing edges, then they must be in the same partition.
a. Show that we can partition the vertices of any n-vertex binary tree into two
sets A and B, such that jAj  3n=4 and jBj  3n=4, by removing a single
edge.
b. Show that the constant 3=4 in part (a) is optimal in the worst case by giving
an example of a simple binary tree whose most evenly balanced partition upon
removal of a single edge has jAj D 3n=4.

1182
Appendix B
Sets, Etc.
c. Show that by removing at most O.lg n/ edges, we can partition the vertices
of any n-vertex binary tree into two sets A and B such that jAj D bn=2c
and jBj D dn=2e.
Appendix notes
G. Boole pioneered the development of symbolic logic, and he introduced many of
the basic set notations in a book published in 1854. Modern set theory was created
by G. Cantor during the period 1874–1895. Cantor focused primarily on sets of
inﬁnite cardinality. The term “function” is attributed to G. W. Leibniz, who used it
to refer to several kinds of mathematical formulas. His limited deﬁnition has been
generalized many times. Graph theory originated in 1736, when L. Euler proved
that it was impossible to cross each of the seven bridges in the city of K¨onigsberg
exactly once and return to the starting point.
The book by Harary [160] provides a useful compendium of many deﬁnitions
and results from graph theory.
