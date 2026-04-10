# 34 NP-Completeness

NP-Completeness
Almost all the algorithms we have studied thus far have been polynomial-time algorithms: on inputs of size n, their worst-case running time is O.nk/ for some constant k. You might wonder whether all problems can be solved in polynomial time.
The answer is no. For example, there are problems, such as Turing’s famous “Halting Problem,” that cannot be solved by any computer, no matter how much time we
allow. There are also problems that can be solved, but not in time O.nk/ for any
constant k. Generally, we think of problems that are solvable by polynomial-time
algorithms as being tractable, or easy, and problems that require superpolynomial
time as being intractable, or hard.
The subject of this chapter, however, is an interesting class of problems, called
the “NP-complete” problems, whose status is unknown. No polynomial-time algorithm has yet been discovered for an NP-complete problem, nor has anyone yet
been able to prove that no polynomial-time algorithm can exist for any one of them.
This so-called P ¤ NP question has been one of the deepest, most perplexing open
research problems in theoretical computer science since it was ﬁrst posed in 1971.
Several NP-complete problems are particularly tantalizing because they seem
on the surface to be similar to problems that we know how to solve in polynomial
time. In each of the following pairs of problems, one is solvable in polynomial
time and the other is NP-complete, but the difference between problems appears to
be slight:
Shortest vs. longest simple paths: In Chapter 24, we saw that even with negative
edge weights, we can ﬁnd shortest paths from a single source in a directed
graph G D .V; E/ in O.VE/ time. Finding a longest simple path between two
vertices is difﬁcult, however. Merely determining whether a graph contains a
simple path with at least a given number of edges is NP-complete.
Euler tour vs. hamiltonian cycle: An Euler tour of a connected, directed graph
G D .V; E/ is a cycle that traverses each edge of G exactly once, although
it is allowed to visit each vertex more than once. By Problem 22-3, we can
determine whether a graph has an Euler tour in only O.E/ time and, in fact,

we can ﬁnd the edges of the Euler tour in O.E/ time. A hamiltonian cycle of
a directed graph G D .V; E/ is a simple cycle that contains each vertex in V .
Determining whether a directed graph has a hamiltonian cycle is NP-complete.
(Later in this chapter, we shall prove that determining whether an undirected
graph has a hamiltonian cycle is NP-complete.)
2-CNF satisﬁability vs. 3-CNF satisﬁability: A boolean formula contains variables whose values are 0 or 1; boolean connectives such as ^ (AND), _ (OR),
and : (NOT); and parentheses. A boolean formula is satisﬁable if there exists
some assignment of the values 0 and 1 to its variables that causes it to evaluate
to 1. We shall deﬁne terms more formally later in this chapter, but informally, a
boolean formula is in k-conjunctive normal form, or k-CNF, if it is the AND
of clauses of ORs of exactly k variables or their negations. For example, the
boolean formula .x1 _ :x2/ ^ .:x1 _ x3/ ^ .:x2 _ :x3/ is in 2-CNF. (It has
the satisfying assignment x1 D 1; x2 D 0; x3 D 1.) Although we can determine in polynomial time whether a 2-CNF formula is satisﬁable, we shall see
later in this chapter that determining whether a 3-CNF formula is satisﬁable is
NP-complete.
NP-completeness and the classes P and NP
Throughout this chapter, we shall refer to three classes of problems: P, NP, and
NPC, the latter class being the NP-complete problems. We describe them informally here, and we shall deﬁne them more formally later on.
The class P consists of those problems that are solvable in polynomial time.
More speciﬁcally, they are problems that can be solved in time O.nk/ for some
constant k, where n is the size of the input to the problem. Most of the problems
examined in previous chapters are in P.
The class NP consists of those problems that are “veriﬁable” in polynomial time.
What do we mean by a problem being veriﬁable? If we were somehow given a
“certiﬁcate” of a solution, then we could verify that the certiﬁcate is correct in time
polynomial in the size of the input to the problem. For example, in the hamiltoniancycle problem, given a directed graph G D .V; E/, a certiﬁcate would be a sequence h1; 2; 3; : : : ; jV ji of jV j vertices. We could easily check in polynomial
time that .i; iC1/ 2 E for i D 1; 2; 3; : : : ; jV j1 and that .jV j; 1/ 2 E as well.
As another example, for 3-CNF satisﬁability, a certiﬁcate would be an assignment
of values to variables. We could check in polynomial time that this assignment
satisﬁes the boolean formula.
Any problem in P is also in NP, since if a problem is in P then we can solve it
in polynomial time without even being supplied a certiﬁcate. We shall formalize
this notion later in this chapter, but for now we can believe that P  NP. The open
question is whether or not P is a proper subset of NP.

Informally, a problem is in the class NPC—and we refer to it as being NPcomplete—if it is in NP and is as “hard” as any problem in NP. We shall formally
deﬁne what it means to be as hard as any problem in NP later in this chapter.
In the meantime, we will state without proof that if any NP-complete problem
can be solved in polynomial time, then every problem in NP has a polynomialtime algorithm. Most theoretical computer scientists believe that the NP-complete
problems are intractable, since given the wide range of NP-complete problems
that have been studied to date—without anyone having discovered a polynomialtime solution to any of them—it would be truly astounding if all of them could
be solved in polynomial time. Yet, given the effort devoted thus far to proving
that NP-complete problems are intractable—without a conclusive outcome—we
cannot rule out the possibility that the NP-complete problems are in fact solvable
in polynomial time.
To become a good algorithm designer, you must understand the rudiments of the
theory of NP-completeness. If you can establish a problem as NP-complete, you
provide good evidence for its intractability. As an engineer, you would then do
better to spend your time developing an approximation algorithm (see Chapter 35)
or solving a tractable special case, rather than searching for a fast algorithm that
solves the problem exactly. Moreover, many natural and interesting problems that
on the surface seem no harder than sorting, graph searching, or network ﬂow are
in fact NP-complete. Therefore, you should become familiar with this remarkable
class of problems.
Overview of showing problems to be NP-complete
The techniques we use to show that a particular problem is NP-complete differ
fundamentally from the techniques used throughout most of this book to design
and analyze algorithms. When we demonstrate that a problem is NP-complete,
we are making a statement about how hard it is (or at least how hard we think it
is), rather than about how easy it is. We are not trying to prove the existence of
an efﬁcient algorithm, but instead that no efﬁcient algorithm is likely to exist. In
this way, NP-completeness proofs bear some similarity to the proof in Section 8.1
of an .n lg n/-time lower bound for any comparison sort algorithm; the speciﬁc
techniques used for showing NP-completeness differ from the decision-tree method
used in Section 8.1, however.
We rely on three key concepts in showing a problem to be NP-complete:
Decision problems vs. optimization problems
Many problems of interest are optimization problems, in which each feasible (i.e.,
“legal”) solution has an associated value, and we wish to ﬁnd a feasible solution
with the best value. For example, in a problem that we call SHORTEST-PATH,

we are given an undirected graph G and vertices u and , and we wish to ﬁnd a
path from u to  that uses the fewest edges. In other words, SHORTEST-PATH
is the single-pair shortest-path problem in an unweighted, undirected graph. NPcompleteness applies directly not to optimization problems, however, but to decision problems, in which the answer is simply “yes” or “no” (or, more formally, “1”
or “0”).
Although NP-complete problems are conﬁned to the realm of decision problems,
we can take advantage of a convenient relationship between optimization problems
and decision problems. We usually can cast a given optimization problem as a related decision problem by imposing a bound on the value to be optimized. For
example, a decision problem related to SHORTEST-PATH is PATH: given a directed graph G, vertices u and , and an integer k, does a path exist from u to 
consisting of at most k edges?
The relationship between an optimization problem and its related decision problem works in our favor when we try to show that the optimization problem is
“hard.” That is because the decision problem is in a sense “easier,” or at least “no
harder.” As a speciﬁc example, we can solve PATH by solving SHORTEST-PATH
and then comparing the number of edges in the shortest path found to the value
of the decision-problem parameter k. In other words, if an optimization problem is easy, its related decision problem is easy as well. Stated in a way that has
more relevance to NP-completeness, if we can provide evidence that a decision
problem is hard, we also provide evidence that its related optimization problem is
hard. Thus, even though it restricts attention to decision problems, the theory of
NP-completeness often has implications for optimization problems as well.
Reductions
The above notion of showing that one problem is no harder or no easier than another applies even when both problems are decision problems. We take advantage
of this idea in almost every NP-completeness proof, as follows. Let us consider a
decision problem A, which we would like to solve in polynomial time. We call the
input to a particular problem an instance of that problem; for example, in PATH,
an instance would be a particular graph G, particular vertices u and  of G, and a
particular integer k. Now suppose that we already know how to solve a different
decision problem B in polynomial time. Finally, suppose that we have a procedure
that transforms any instance ˛ of A into some instance ˇ of B with the following
characteristics:

The transformation takes polynomial time.

The answers are the same. That is, the answer for ˛ is “yes” if and only if the
answer for ˇ is also “yes.”

polynomial-time
reduction algorithm
instance β
polynomial-time
algorithm to decide B
yes
yes
polynomial-time algorithm to decide A
no
no
of B
instance α
of A
Figure 34.1
How to use a polynomial-time reduction algorithm to solve a decision problem A in
polynomial time, given a polynomial-time decision algorithm for another problem B. In polynomial
time, we transform an instance ˛ of A into an instance ˇ of B, we solve B in polynomial time, and
we use the answer for ˇ as the answer for ˛.
We call such a procedure a polynomial-time reduction algorithm and, as Figure 34.1 shows, it provides us a way to solve problem A in polynomial time:
1. Given an instance ˛ of problem A, use a polynomial-time reduction algorithm
to transform it to an instance ˇ of problem B.
2. Run the polynomial-time decision algorithm for B on the instance ˇ.
3. Use the answer for ˇ as the answer for ˛.
As long as each of these steps takes polynomial time, all three together do also, and
so we have a way to decide on ˛ in polynomial time. In other words, by “reducing”
solving problem A to solving problem B, we use the “easiness” of B to prove the
“easiness” of A.
Recalling that NP-completeness is about showing how hard a problem is rather
than how easy it is, we use polynomial-time reductions in the opposite way to show
that a problem is NP-complete. Let us take the idea a step further, and show how we
could use polynomial-time reductions to show that no polynomial-time algorithm
can exist for a particular problem B. Suppose we have a decision problem A for
which we already know that no polynomial-time algorithm can exist. (Let us not
concern ourselves for now with how to ﬁnd such a problem A.) Suppose further
that we have a polynomial-time reduction transforming instances of A to instances
of B. Now we can use a simple proof by contradiction to show that no polynomialtime algorithm can exist for B. Suppose otherwise; i.e., suppose that B has a
polynomial-time algorithm. Then, using the method shown in Figure 34.1, we
would have a way to solve problem A in polynomial time, which contradicts our
assumption that there is no polynomial-time algorithm for A.
For NP-completeness, we cannot assume that there is absolutely no polynomialtime algorithm for problem A. The proof methodology is similar, however, in that
we prove that problem B is NP-complete on the assumption that problem A is also
NP-complete.

## 34.1 Polynomial time

A ﬁrst NP-complete problem
Because the technique of reduction relies on having a problem already known to
be NP-complete in order to prove a different problem NP-complete, we need a
“ﬁrst” NP-complete problem. The problem we shall use is the circuit-satisﬁability
problem, in which we are given a boolean combinational circuit composed of AND,
OR, and NOT gates, and we wish to know whether there exists some set of boolean
inputs to this circuit that causes its output to be 1. We shall prove that this ﬁrst
problem is NP-complete in Section 34.3.
Chapter outline
This chapter studies the aspects of NP-completeness that bear most directly on the
analysis of algorithms. In Section 34.1, we formalize our notion of “problem” and
deﬁne the complexity class P of polynomial-time solvable decision problems. We
also see how these notions ﬁt into the framework of formal-language theory. Section 34.2 deﬁnes the class NP of decision problems whose solutions are veriﬁable
in polynomial time. It also formally poses the P ¤ NP question.
Section 34.3 shows we can relate problems via polynomial-time “reductions.”
It deﬁnes NP-completeness and sketches a proof that one problem, called “circuit
satisﬁability,” is NP-complete. Having found one NP-complete problem, we show
in Section 34.4 how to prove other problems to be NP-complete much more simply
by the methodology of reductions. We illustrate this methodology by showing that
two formula-satisﬁability problems are NP-complete. With additional reductions,
we show in Section 34.5 a variety of other problems to be NP-complete.

## 34.1 Polynomial time

We begin our study of NP-completeness by formalizing our notion of polynomialtime solvable problems. We generally regard these problems as tractable, but for
philosophical, not mathematical, reasons.
We can offer three supporting arguments.
First, although we may reasonably regard a problem that requires time ‚.n100/
to be intractable, very few practical problems require time on the order of such a
high-degree polynomial. The polynomial-time computable problems encountered
in practice typically require much less time. Experience has shown that once the
ﬁrst polynomial-time algorithm for a problem has been discovered, more efﬁcient
algorithms often follow. Even if the current best algorithm for a problem has a
running time of ‚.n100/, an algorithm with a much better running time will likely
soon be discovered.

Second, for many reasonable models of computation, a problem that can be
solved in polynomial time in one model can be solved in polynomial time in another. For example, the class of problems solvable in polynomial time by the serial
random-access machine used throughout most of this book is the same as the class
of problems solvable in polynomial time on abstract Turing machines.1 It is also
the same as the class of problems solvable in polynomial time on a parallel computer when the number of processors grows polynomially with the input size.
Third, the class of polynomial-time solvable problems has nice closure properties, since polynomials are closed under addition, multiplication, and composition.
For example, if the output of one polynomial-time algorithm is fed into the input of
another, the composite algorithm is polynomial. Exercise 34.1-5 asks you to show
that if an algorithm makes a constant number of calls to polynomial-time subroutines and performs an additional amount of work that also takes polynomial time,
then the running time of the composite algorithm is polynomial.
Abstract problems
To understand the class of polynomial-time solvable problems, we must ﬁrst have
a formal notion of what a “problem” is. We deﬁne an abstract problem Q to be a
binary relation on a set I of problem instances and a set S of problem solutions.
For example, an instance for SHORTEST-PATH is a triple consisting of a graph
and two vertices. A solution is a sequence of vertices in the graph, with perhaps
the empty sequence denoting that no path exists. The problem SHORTEST-PATH
itself is the relation that associates each instance of a graph and two vertices with
a shortest path in the graph that connects the two vertices. Since shortest paths are
not necessarily unique, a given problem instance may have more than one solution.
This formulation of an abstract problem is more general than we need for our
purposes. As we saw above, the theory of NP-completeness restricts attention to
decision problems: those having a yes/no solution. In this case, we can view an
abstract decision problem as a function that maps the instance set I to the solution
set f0; 1g. For example, a decision problem related to SHORTEST-PATH is the
problem PATH that we saw earlier. If i D hG;u;;ki is an instance of the decision
problem PATH, then PATH.i/ D 1 (yes) if a shortest path from u to  has at
most k edges, and PATH.i/ D 0 (no) otherwise. Many abstract problems are not
decision problems, but rather optimization problems, which require some value to
be minimized or maximized. As we saw above, however, we can usually recast an
optimization problem as a decision problem that is no harder.
1See Hopcroft and Ullman [180] or Lewis and Papadimitriou [236] for a thorough treatment of the
Turing-machine model.

## 34.1 Polynomial time

Encodings
In order for a computer program to solve an abstract problem, we must represent
problem instances in a way that the program understands. An encoding of a set S
of abstract objects is a mapping e from S to the set of binary strings.2 For example,
we are all familiar with encoding the natural numbers N D f0; 1; 2; 3; 4; : : :g as
the strings f0; 1; 10; 11; 100; : : :g. Using this encoding, e.17/ D 10001. If you
have looked at computer representations of keyboard characters, you probably have
seen the ASCII code, where, for example, the encoding of A is 1000001. We can
encode a compound object as a binary string by combining the representations of
its constituent parts. Polygons, graphs, functions, ordered pairs, programs—all can
be encoded as binary strings.
Thus, a computer algorithm that “solves” some abstract decision problem actually takes an encoding of a problem instance as input. We call a problem whose
instance set is the set of binary strings a concrete problem. We say that an algorithm solves a concrete problem in time O.T .n// if, when it is provided a problem
instance i of length n D jij, the algorithm can produce the solution in O.T .n//
time.3 A concrete problem is polynomial-time solvable, therefore, if there exists
an algorithm to solve it in time O.nk/ for some constant k.
We can now formally deﬁne the complexity class P as the set of concrete decision problems that are polynomial-time solvable.
We can use encodings to map abstract problems to concrete problems. Given
an abstract decision problem Q mapping an instance set I to f0; 1g, an encoding
e W I ! f0; 1g can induce a related concrete decision problem, which we denote
by e.Q/.4 If the solution to an abstract-problem instance i 2 I is Q.i/ 2 f0; 1g,
then the solution to the concrete-problem instance e.i/ 2 f0; 1g is also Q.i/. As a
technicality, some binary strings might represent no meaningful abstract-problem
instance. For convenience, we shall assume that any such string maps arbitrarily
to 0. Thus, the concrete problem produces the same solutions as the abstract problem on binary-string instances that represent the encodings of abstract-problem
instances.
We would like to extend the deﬁnition of polynomial-time solvability from concrete problems to abstract problems by using encodings as the bridge, but we would
2The codomain of e need not be binary strings; any set of strings over a ﬁnite alphabet having at
least 2 symbols will do.
3We assume that the algorithm’s output is separate from its input. Because it takes at least one time
step to produce each bit of the output and the algorithm takes O.T .n// time steps, the size of the
output is O.T .n//.
4We denote by f0; 1g the set of all strings composed of symbols from the set f0; 1g.

like the deﬁnition to be independent of any particular encoding. That is, the efﬁciency of solving a problem should not depend on how the problem is encoded.
Unfortunately, it depends quite heavily on the encoding. For example, suppose that
an integer k is to be provided as the sole input to an algorithm, and suppose that
the running time of the algorithm is ‚.k/. If the integer k is provided in unary—a
string of k 1s—then the running time of the algorithm is O.n/ on length-n inputs,
which is polynomial time. If we use the more natural binary representation of the
integer k, however, then the input length is n D blg kc C 1. In this case, the running time of the algorithm is ‚.k/ D ‚.2n/, which is exponential in the size of the
input. Thus, depending on the encoding, the algorithm runs in either polynomial
or superpolynomial time.
How we encode an abstract problem matters quite a bit to how we understand
polynomial time. We cannot really talk about solving an abstract problem without
ﬁrst specifying an encoding. Nevertheless, in practice, if we rule out “expensive”
encodings such as unary ones, the actual encoding of a problem makes little difference to whether the problem can be solved in polynomial time. For example,
representing integers in base 3 instead of binary has no effect on whether a problem is solvable in polynomial time, since we can convert an integer represented in
base 3 to an integer represented in base 2 in polynomial time.
We say that a function f W f0; 1g ! f0; 1g is polynomial-time computable
if there exists a polynomial-time algorithm A that, given any input x 2 f0; 1g,
produces as output f .x/. For some set I of problem instances, we say that two encodings e1 and e2 are polynomially related if there exist two polynomial-time computable functions f12 and f21 such that for any i 2 I, we have f12.e1.i// D e2.i/
and f21.e2.i// D e1.i/.5 That is, a polynomial-time algorithm can compute the encoding e2.i/ from the encoding e1.i/, and vice versa. If two encodings e1 and e2 of
an abstract problem are polynomially related, whether the problem is polynomialtime solvable or not is independent of which encoding we use, as the following
lemma shows.

> **Lemma 34.1**

Let Q be an abstract decision problem on an instance set I, and let e1 and e2 be
polynomially related encodings on I. Then, e1.Q/ 2 P if and only if e2.Q/ 2 P.
5Technically, we also require the functions f12 and f21 to “map noninstances to noninstances.”
A noninstance of an encoding e is a string x 2 f0; 1g such that there is no instance i for which
e.i/ D x. We require that f12.x/ D y for every noninstance x of encoding e1, where y is some noninstance of e2, and that f21.x0/ D y0 for every noninstance x0 of e2, where y0 is some noninstance
of e1.

## 34.1 Polynomial time

Proof
We need only prove the forward direction, since the backward direction is
symmetric. Suppose, therefore, that e1.Q/ can be solved in time O.nk/ for some
constant k. Further, suppose that for any problem instance i, the encoding e1.i/
can be computed from the encoding e2.i/ in time O.nc/ for some constant c, where
n D je2.i/j. To solve problem e2.Q/, on input e2.i/, we ﬁrst compute e1.i/ and
then run the algorithm for e1.Q/ on e1.i/. How long does this take? Converting
encodings takes time O.nc/, and therefore je1.i/j D O.nc/, since the output of
a serial computer cannot be longer than its running time. Solving the problem
on e1.i/ takes time O.je1.i/jk/ D O.nck/, which is polynomial since both c and k
are constants.
Thus, whether an abstract problem has its instances encoded in binary or base 3
does not affect its “complexity,” that is, whether it is polynomial-time solvable or
not; but if instances are encoded in unary, its complexity may change. In order to
be able to converse in an encoding-independent fashion, we shall generally assume
that problem instances are encoded in any reasonable, concise fashion, unless we
speciﬁcally say otherwise. To be precise, we shall assume that the encoding of an
integer is polynomially related to its binary representation, and that the encoding of
a ﬁnite set is polynomially related to its encoding as a list of its elements, enclosed
in braces and separated by commas. (ASCII is one such encoding scheme.) With
such a “standard” encoding in hand, we can derive reasonable encodings of other
mathematical objects, such as tuples, graphs, and formulas. To denote the standard
encoding of an object, we shall enclose the object in angle braces. Thus, hGi
denotes the standard encoding of a graph G.
As long as we implicitly use an encoding that is polynomially related to this
standard encoding, we can talk directly about abstract problems without reference
to any particular encoding, knowing that the choice of encoding has no effect on
whether the abstract problem is polynomial-time solvable. Henceforth, we shall
generally assume that all problem instances are binary strings encoded using the
standard encoding, unless we explicitly specify the contrary. We shall also typically
neglect the distinction between abstract and concrete problems. You should watch
out for problems that arise in practice, however, in which a standard encoding is
not obvious and the encoding does make a difference.
A formal-language framework
By focusing on decision problems, we can take advantage of the machinery of
formal-language theory.
Let’s review some deﬁnitions from that theory.
An
alphabet † is a ﬁnite set of symbols.
A language L over † is any set of
strings made up of symbols from †.
For example, if † D f0; 1g, the set
L D f10; 11; 101; 111; 1011; 1101; 10001; : : :g is the language of binary represen1058
tations of prime numbers. We denote the empty string by ", the empty language
by ;, and the language of all strings over † by †. For example, if † D f0; 1g,
then † D f"; 0; 1; 00; 01; 10; 11; 000; : : :g is the set of all binary strings. Every
language L over † is a subset of †.
We can perform a variety of operations on languages. Set-theoretic operations,
such as union and intersection, follow directly from the set-theoretic deﬁnitions.
We deﬁne the complement of L by L D †  L. The concatenation L1L2 of two
languages L1 and L2 is the language
L D fx1x2 W x1 2 L1 and x2 2 L2g :
The closure or Kleene star of a language L is the language
L D f"g [ L [ L2 [ L3 [    ;
where Lk is the language obtained by concatenating L to itself k times.
From the point of view of language theory, the set of instances for any decision
problem Q is simply the set †, where † D f0; 1g. Since Q is entirely characterized by those problem instances that produce a 1 (yes) answer, we can view Q as
a language L over † D f0; 1g, where
L D fx 2 † W Q.x/ D 1g :
For example, the decision problem PATH has the corresponding language
PATH D fhG; u; ; ki W G D .V; E/ is an undirected graph,
u;  2 V;
k  0 is an integer, and
there exists a path from u to  in G
consisting of at most k edgesg :
(Where convenient, we shall sometimes use the same name—PATH in this case—
to refer to both a decision problem and its corresponding language.)
The formal-language framework allows us to express concisely the relation between decision problems and algorithms that solve them.
We say that an algorithm A accepts a string x 2 f0; 1g if, given input x, the algorithm’s output A.x/ is 1. The language accepted by an algorithm A is the set of strings
L D fx 2 f0; 1g W A.x/ D 1g, that is, the set of strings that the algorithm accepts.
An algorithm A rejects a string x if A.x/ D 0.
Even if language L is accepted by an algorithm A, the algorithm will not necessarily reject a string x 62 L provided as input to it. For example, the algorithm may
loop forever. A language L is decided by an algorithm A if every binary string
in L is accepted by A and every binary string not in L is rejected by A. A language L is accepted in polynomial time by an algorithm A if it is accepted by A
and if in addition there exists a constant k such that for any length-n string x 2 L,

## 34.1 Polynomial time

algorithm A accepts x in time O.nk/. A language L is decided in polynomial
time by an algorithm A if there exists a constant k such that for any length-n string
x 2 f0; 1g, the algorithm correctly decides whether x 2 L in time O.nk/. Thus,
to accept a language, an algorithm need only produce an answer when provided a
string in L, but to decide a language, it must correctly accept or reject every string
in f0; 1g.
As an example, the language PATH can be accepted in polynomial time. One
polynomial-time accepting algorithm veriﬁes that G encodes an undirected graph,
veriﬁes that u and  are vertices in G, uses breadth-ﬁrst search to compute a shortest path from u to  in G, and then compares the number of edges on the shortest
path obtained with k. If G encodes an undirected graph and the path found from u
to  has at most k edges, the algorithm outputs 1 and halts. Otherwise, the algorithm runs forever. This algorithm does not decide PATH, however, since it does
not explicitly output 0 for instances in which a shortest path has more than k edges.
A decision algorithm for PATH must explicitly reject binary strings that do not belong to PATH. For a decision problem such as PATH, such a decision algorithm is
easy to design: instead of running forever when there is not a path from u to  with
at most k edges, it outputs 0 and halts. (It must also output 0 and halt if the input
encoding is faulty.) For other problems, such as Turing’s Halting Problem, there
exists an accepting algorithm, but no decision algorithm exists.
We can informally deﬁne a complexity class as a set of languages, membership
in which is determined by a complexity measure, such as running time, of an
algorithm that determines whether a given string x belongs to language L. The
actual deﬁnition of a complexity class is somewhat more technical.6
Using this language-theoretic framework, we can provide an alternative deﬁnition of the complexity class P:
P D fL  f0; 1g W there exists an algorithm A that decides L
in polynomial timeg :
In fact, P is also the class of languages that can be accepted in polynomial time.

> **Theorem 34.2**

P D fL W L is accepted by a polynomial-time algorithmg :
Proof
Because the class of languages decided by polynomial-time algorithms is
a subset of the class of languages accepted by polynomial-time algorithms, we
need only show that if L is accepted by a polynomial-time algorithm, it is decided by a polynomial-time algorithm. Let L be the language accepted by some
6For more on complexity classes, see the seminal paper by Hartmanis and Stearns [162].

polynomial-time algorithm A. We shall use a classic “simulation” argument to
construct another polynomial-time algorithm A0 that decides L. Because A accepts L in time O.nk/ for some constant k, there also exists a constant c such
that A accepts L in at most cnk steps. For any input string x, the algorithm A0
simulates cnk steps of A. After simulating cnk steps, algorithm A0 inspects the behavior of A. If A has accepted x, then A0 accepts x by outputting a 1. If A has not
accepted x, then A0 rejects x by outputting a 0. The overhead of A0 simulating A
does not increase the running time by more than a polynomial factor, and thus A0
is a polynomial-time algorithm that decides L.
Note that the proof of Theorem 34.2 is nonconstructive. For a given language
L 2 P, we may not actually know a bound on the running time for the algorithm A
that accepts L. Nevertheless, we know that such a bound exists, and therefore, that
an algorithm A0 exists that can check the bound, even though we may not be able
to ﬁnd the algorithm A0 easily.

## Exercises

34.1-1
Deﬁne the optimization problem LONGEST-PATH-LENGTH as the relation that
associates each instance of an undirected graph and two vertices with the number of edges in a longest simple path between the two vertices. Deﬁne the decision problem LONGEST-PATH D fhG; u; ; ki W G D .V; E/ is an undirected graph, u;  2 V , k  0 is an integer, and there exists a simple path
from u to  in G consisting of at least k edgesg. Show that the optimization problem LONGEST-PATH-LENGTH can be solved in polynomial time if and only if
LONGEST-PATH 2 P.
34.1-2
Give a formal deﬁnition for the problem of ﬁnding the longest simple cycle in an
undirected graph. Give a related decision problem. Give the language corresponding to the decision problem.
34.1-3
Give a formal encoding of directed graphs as binary strings using an adjacencymatrix representation. Do the same using an adjacency-list representation. Argue
that the two representations are polynomially related.
34.1-4
Is the dynamic-programming algorithm for the 0-1 knapsack problem that is asked
for in Exercise 16.2-2 a polynomial-time algorithm? Explain your answer.

## 34.2 Polynomial-time veriﬁcation

34.1-5
Show that if an algorithm makes at most a constant number of calls to polynomialtime subroutines and performs an additional amount of work that also takes polynomial time, then it runs in polynomial time. Also show that a polynomial number of
calls to polynomial-time subroutines may result in an exponential-time algorithm.
34.1-6
Show that the class P, viewed as a set of languages, is closed under union, intersection, concatenation, complement, and Kleene star. That is, if L1; L2 2 P, then
L1 [ L2 2 P, L1 \ L2 2 P, L1L2 2 P, L1 2 P, and L
1 2 P.

## 34.2 Polynomial-time veriﬁcation

We now look at algorithms that verify membership in languages. For example,
suppose that for a given instance hG; u; ; ki of the decision problem PATH, we
are also given a path p from u to . We can easily check whether p is a path in G
and whether the length of p is at most k, and if so, we can view p as a “certiﬁcate”
that the instance indeed belongs to PATH. For the decision problem PATH, this
certiﬁcate doesn’t seem to buy us much. After all, PATH belongs to P—in fact,
we can solve PATH in linear time—and so verifying membership from a given
certiﬁcate takes as long as solving the problem from scratch. We shall now examine
a problem for which we know of no polynomial-time decision algorithm and yet,
given a certiﬁcate, veriﬁcation is easy.
Hamiltonian cycles
The problem of ﬁnding a hamiltonian cycle in an undirected graph has been studied for over a hundred years. Formally, a hamiltonian cycle of an undirected graph
G D .V; E/ is a simple cycle that contains each vertex in V . A graph that contains a hamiltonian cycle is said to be hamiltonian; otherwise, it is nonhamiltonian. The name honors W. R. Hamilton, who described a mathematical game on
the dodecahedron (Figure 34.2(a)) in which one player sticks ﬁve pins in any ﬁve
consecutive vertices and the other player must complete the path to form a cycle

(a)
(b)
Figure 34.2
(a) A graph representing the vertices, edges, and faces of a dodecahedron, with a
hamiltonian cycle shown by shaded edges. (b) A bipartite graph with an odd number of vertices.
Any such graph is nonhamiltonian.
containing all the vertices.7 The dodecahedron is hamiltonian, and Figure 34.2(a)
shows one hamiltonian cycle. Not all graphs are hamiltonian, however. For example, Figure 34.2(b) shows a bipartite graph with an odd number of vertices.
Exercise 34.2-2 asks you to show that all such graphs are nonhamiltonian.
We can deﬁne the hamiltonian-cycle problem, “Does a graph G have a hamiltonian cycle?” as a formal language:
HAM-CYCLE D fhGi W G is a hamiltonian graphg :
How might an algorithm decide the language HAM-CYCLE? Given a problem
instance hGi, one possible decision algorithm lists all permutations of the vertices
of G and then checks each permutation to see if it is a hamiltonian path. What is
the running time of this algorithm? If we use the “reasonable” encoding of a graph
as its adjacency matrix, the number m of vertices in the graph is .pn/, where
n D jhGij is the length of the encoding of G. There are mŠ possible permutations
7In a letter dated 17 October 1856 to his friend John T. Graves, Hamilton [157, p. 624] wrote, “I
have found that some young persons have been much amused by trying a new mathematical game
which the Icosion furnishes, one person sticking ﬁve pins in any ﬁve consecutive points . . . and the
other player then aiming to insert, which by the theory in this letter can always be done, ﬁfteen other
pins, in cyclical succession, so as to cover all the other points, and to end in immediate proximity to
the pin wherewith his antagonist had begun.”

## 34.2 Polynomial-time veriﬁcation

of the vertices, and therefore the running time is .mŠ/ D .pn Š/ D .2
pn/,
which is not O.nk/ for any constant k. Thus, this naive algorithm does not run
in polynomial time. In fact, the hamiltonian-cycle problem is NP-complete, as we
shall prove in Section 34.5.
Veriﬁcation algorithms
Consider a slightly easier problem. Suppose that a friend tells you that a given
graph G is hamiltonian, and then offers to prove it by giving you the vertices in
order along the hamiltonian cycle. It would certainly be easy enough to verify the
proof: simply verify that the provided cycle is hamiltonian by checking whether
it is a permutation of the vertices of V and whether each of the consecutive edges
along the cycle actually exists in the graph. You could certainly implement this
veriﬁcation algorithm to run in O.n2/ time, where n is the length of the encoding
of G. Thus, a proof that a hamiltonian cycle exists in a graph can be veriﬁed in
polynomial time.
We deﬁne a veriﬁcation algorithm as being a two-argument algorithm A, where
one argument is an ordinary input string x and the other is a binary string y called
a certiﬁcate. A two-argument algorithm A veriﬁes an input string x if there exists
a certiﬁcate y such that A.x; y/ D 1. The language veriﬁed by a veriﬁcation
algorithm A is
L D fx 2 f0; 1g W there exists y 2 f0; 1g such that A.x; y/ D 1g :
Intuitively, an algorithm A veriﬁes a language L if for any string x 2 L, there
exists a certiﬁcate y that A can use to prove that x 2 L. Moreover, for any string
x 62 L, there must be no certiﬁcate proving that x 2 L. For example, in the
hamiltonian-cycle problem, the certiﬁcate is the list of vertices in some hamiltonian cycle. If a graph is hamiltonian, the hamiltonian cycle itself offers enough
information to verify this fact. Conversely, if a graph is not hamiltonian, there
can be no list of vertices that fools the veriﬁcation algorithm into believing that the
graph is hamiltonian, since the veriﬁcation algorithm carefully checks the proposed
“cycle” to be sure.

The complexity class NP
The complexity class NP is the class of languages that can be veriﬁed by a polynomial-time algorithm.8 More precisely, a language L belongs to NP if and only if
there exist a two-input polynomial-time algorithm A and a constant c such that
L D fx 2 f0; 1g W there exists a certiﬁcate y with jyj D O.jxjc/
such that A.x; y/ D 1g :
We say that algorithm A veriﬁes language L in polynomial time.
From our earlier discussion on the hamiltonian-cycle problem, we now see that
HAM-CYCLE 2 NP. (It is always nice to know that an important set is nonempty.)
Moreover, if L 2 P, then L 2 NP, since if there is a polynomial-time algorithm
to decide L, the algorithm can be easily converted to a two-argument veriﬁcation
algorithm that simply ignores any certiﬁcate and accepts exactly those input strings
it determines to be in L. Thus, P  NP.
It is unknown whether P D NP, but most researchers believe that P and NP are
not the same class. Intuitively, the class P consists of problems that can be solved
quickly. The class NP consists of problems for which a solution can be veriﬁed
quickly. You may have learned from experience that it is often more difﬁcult to
solve a problem from scratch than to verify a clearly presented solution, especially
when working under time constraints. Theoretical computer scientists generally
believe that this analogy extends to the classes P and NP, and thus that NP includes
languages that are not in P.
There is more compelling, though not conclusive, evidence that P ¤ NP—the
existence of languages that are “NP-complete.” We shall study this class in Section 34.3.
Many other fundamental questions beyond the P ¤ NP question remain unresolved. Figure 34.3 shows some possible scenarios. Despite much work by many
researchers, no one even knows whether the class NP is closed under complement. That is, does L 2 NP imply L 2 NP? We can deﬁne the complexity class
co-NP as the set of languages L such that L 2 NP. We can restate the question
of whether NP is closed under complement as whether NP D co-NP. Since P is
closed under complement (Exercise 34.1-6), it follows from Exercise 34.2-9 that
P  NP \ co-NP. Once again, however, no one knows whether P D NP \ co-NP
or whether there is some language in NP \ co-NP  P.
8The name “NP” stands for “nondeterministic polynomial time.” The class NP was originally studied
in the context of nondeterminism, but this book uses the somewhat simpler yet equivalent notion of
veriﬁcation. Hopcroft and Ullman [180] give a good presentation of NP-completeness in terms of
nondeterministic models of computation.

## 34.2 Polynomial-time veriﬁcation

co-NP
NP
(c)
P = NP ∩ co-NP
co-NP
NP
(d)
P
P = NP = co-NP
(a)
NP = co-NP
(b)
P
NP ∩ co-NP
Figure 34.3
Four possibilities for relationships among complexity classes. In each diagram, one
region enclosing another indicates a proper-subset relation. (a) P D NP D co-NP. Most researchers
regard this possibility as the most unlikely. (b) If NP is closed under complement, then NP D co-NP,
but it need not be the case that P D NP. (c) P D NP\co-NP, but NP is not closed under complement.
(d) NP ¤ co-NP and P ¤ NP \ co-NP. Most researchers regard this possibility as the most likely.
Thus, our understanding of the precise relationship between P and NP is woefully incomplete. Nevertheless, even though we might not be able to prove that a
particular problem is intractable, if we can prove that it is NP-complete, then we
have gained valuable information about it.

## Exercises

34.2-1
Consider the language GRAPH-ISOMORPHISM D fhG1; G2i W G1 and G2 are
isomorphic graphsg. Prove that GRAPH-ISOMORPHISM 2 NP by describing a
polynomial-time algorithm to verify the language.
34.2-2
Prove that if G is an undirected bipartite graph with an odd number of vertices,
then G is nonhamiltonian.
34.2-3
Show that if HAM-CYCLE 2 P, then the problem of listing the vertices of a
hamiltonian cycle, in order, is polynomial-time solvable.

34.2-4
Prove that the class NP of languages is closed under union, intersection, concatenation, and Kleene star. Discuss the closure of NP under complement.
34.2-5
Show that any language in NP can be decided by an algorithm running in
time 2O.nk/ for some constant k.
34.2-6
A hamiltonian path in a graph is a simple path that visits every vertex exactly
once. Show that the language HAM-PATH D fhG; u; i W there is a hamiltonian
path from u to  in graph Gg belongs to NP.
34.2-7
Show that the hamiltonian-path problem from Exercise 34.2-6 can be solved in
polynomial time on directed acyclic graphs. Give an efﬁcient algorithm for the
problem.
34.2-8
Let  be a boolean formula constructed from the boolean input variables x1; x2;
: : : ; xk, negations (:), ANDs (^), ORs (_), and parentheses. The formula  is a
tautology if it evaluates to 1 for every assignment of 1 and 0 to the input variables.
Deﬁne TAUTOLOGY as the language of boolean formulas that are tautologies.
Show that TAUTOLOGY 2 co-NP.
34.2-9
Prove that P  co-NP.
34.2-10
Prove that if NP ¤ co-NP, then P ¤ NP.
34.2-11
Let G be a connected, undirected graph with at least 3 vertices, and let G3 be the
graph obtained by connecting all pairs of vertices that are connected by a path in G
of length at most 3. Prove that G3 is hamiltonian. (Hint: Construct a spanning tree
for G, and use an inductive argument.)

## 34.3 NP-completeness and reducibility

## 34.3 NP-completeness and reducibility

Perhaps the most compelling reason why theoretical computer scientists believe
that P ¤ NP comes from the existence of the class of “NP-complete” problems.
This class has the intriguing property that if any NP-complete problem can be
solved in polynomial time, then every problem in NP has a polynomial-time solution, that is, P D NP. Despite years of study, though, no polynomial-time algorithm
has ever been discovered for any NP-complete problem.
The language HAM-CYCLE is one NP-complete problem. If we could decide
HAM-CYCLE in polynomial time, then we could solve every problem in NP in
polynomial time. In fact, if NP  P should turn out to be nonempty, we could say
with certainty that HAM-CYCLE 2 NP  P.
The NP-complete languages are, in a sense, the “hardest” languages in NP. In
this section, we shall show how to compare the relative “hardness” of languages
using a precise notion called “polynomial-time reducibility.” Then we formally
deﬁne the NP-complete languages, and we ﬁnish by sketching a proof that one
such language, called CIRCUIT-SAT, is NP-complete. In Sections 34.4 and 34.5,
we shall use the notion of reducibility to show that many other problems are NPcomplete.
Reducibility
Intuitively, a problem Q can be reduced to another problem Q0 if any instance of Q
can be “easily rephrased” as an instance of Q0, the solution to which provides a
solution to the instance of Q. For example, the problem of solving linear equations
in an indeterminate x reduces to the problem of solving quadratic equations. Given
an instance ax C b D 0, we transform it to 0x2 C ax C b D 0, whose solution
provides a solution to ax C b D 0. Thus, if a problem Q reduces to another
problem Q0, then Q is, in a sense, “no harder to solve” than Q0.
Returning to our formal-language framework for decision problems, we say that
a language L1 is polynomial-time reducible to a language L2, written L1 P L2,
if there exists a polynomial-time computable function f W f0; 1g ! f0; 1g such
that for all x 2 f0; 1g,
x 2 L1 if and only if f .x/ 2 L2 :
(34.1)
We call the function f the reduction function, and a polynomial-time algorithm F
that computes f is a reduction algorithm.
Figure 34.4 illustrates the idea of a polynomial-time reduction from a language L1 to another language L2. Each language is a subset of f0; 1g. The
reduction function f provides a polynomial-time mapping such that if x 2 L1,

L2
L1
{0,1}*
{0,1}*
f
Figure 34.4
An illustration of a polynomial-time reduction from a language L1 to a language L2
via a reduction function f . For any input x 2 f0; 1g, the question of whether x 2 L1 has the same
answer as the question of whether f .x/ 2 L2.
then f .x/ 2 L2. Moreover, if x 62 L1, then f .x/ 62 L2. Thus, the reduction function maps any instance x of the decision problem represented by the language L1
to an instance f .x/ of the problem represented by L2. Providing an answer to
whether f .x/ 2 L2 directly provides the answer to whether x 2 L1.
Polynomial-time reductions give us a powerful tool for proving that various languages belong to P.

> **Lemma 34.3**

If L1; L2  f0; 1g are languages such that L1 P L2, then L2 2 P implies
L1 2 P.
Proof
Let A2 be a polynomial-time algorithm that decides L2, and let F be a
polynomial-time reduction algorithm that computes the reduction function f . We
shall construct a polynomial-time algorithm A1 that decides L1.
Figure 34.5 illustrates how we construct A1. For a given input x 2 f0; 1g,
algorithm A1 uses F to transform x into f .x/, and then it uses A2 to test whether
f .x/ 2 L2. Algorithm A1 takes the output from algorithm A2 and produces that
answer as its own output.
The correctness of A1 follows from condition (34.1). The algorithm runs in polynomial time, since both F and A2 run in polynomial time (see Exercise 34.1-5).
NP-completeness
Polynomial-time reductions provide a formal means for showing that one problem is at least as hard as another, to within a polynomial-time factor. That is, if
L1 P L2, then L1 is not more than a polynomial factor harder than L2, which is

## 34.3 NP-completeness and reducibility

x
F
f .x/
A1
A2
yes, f .x/ 2 L2
no, f .x/ 62 L2
yes, x 2 L1
no, x 62 L1
Figure 34.5
The proof of Lemma 34.3. The algorithm F is a reduction algorithm that computes the
reduction function f from L1 to L2 in polynomial time, and A2 is a polynomial-time algorithm that
decides L2. Algorithm A1 decides whether x 2 L1 by using F to transform any input x into f .x/
and then using A2 to decide whether f .x/ 2 L2.
why the “less than or equal to” notation for reduction is mnemonic. We can now
deﬁne the set of NP-complete languages, which are the hardest problems in NP.
A language L  f0; 1g is NP-complete if
1. L 2 NP, and
2. L0 P L for every L0 2 NP.
If a language L satisﬁes property 2, but not necessarily property 1, we say that L
is NP-hard. We also deﬁne NPC to be the class of NP-complete languages.
As the following theorem shows, NP-completeness is at the crux of deciding
whether P is in fact equal to NP.

> **Theorem 34.4**

If any NP-complete problem is polynomial-time solvable, then P D NP. Equivalently, if any problem in NP is not polynomial-time solvable, then no NP-complete
problem is polynomial-time solvable.
Proof
Suppose that L 2 P and also that L 2 NPC. For any L0 2 NP, we
have L0 P L by property 2 of the deﬁnition of NP-completeness.
Thus, by

> **Lemma 34.3, we also have that L0 2 P, which proves the ﬁrst statement of the**

theorem.
To prove the second statement, note that it is the contrapositive of the ﬁrst statement.
It is for this reason that research into the P ¤ NP question centers around the
NP-complete problems. Most theoretical computer scientists believe that P ¤ NP,
which leads to the relationships among P, NP, and NPC shown in Figure 34.6.
But, for all we know, someone may yet come up with a polynomial-time algorithm for an NP-complete problem, thus proving that P D NP. Nevertheless, since
no polynomial-time algorithm for any NP-complete problem has yet been discov1070
NPC
P
NP
Figure 34.6
How most theoretical computer scientists view the relationships among P, NP,
and NPC. Both P and NPC are wholly contained within NP, and P \ NPC D ;.
ered, a proof that a problem is NP-complete provides excellent evidence that it is
intractable.
Circuit satisﬁability
We have deﬁned the notion of an NP-complete problem, but up to this point, we
have not actually proved that any problem is NP-complete. Once we prove that at
least one problem is NP-complete, we can use polynomial-time reducibility as a
tool to prove other problems to be NP-complete. Thus, we now focus on demonstrating the existence of an NP-complete problem: the circuit-satisﬁability problem.
Unfortunately, the formal proof that the circuit-satisﬁability problem is NPcomplete requires technical detail beyond the scope of this text. Instead, we shall
informally describe a proof that relies on a basic understanding of boolean combinational circuits.
Boolean combinational circuits are built from boolean combinational elements
that are interconnected by wires. A boolean combinational element is any circuit
element that has a constant number of boolean inputs and outputs and that performs
a well-deﬁned function. Boolean values are drawn from the set f0; 1g, where 0
represents FALSE and 1 represents TRUE.
The boolean combinational elements that we use in the circuit-satisﬁability problem compute simple boolean functions, and they are known as logic gates. Figure 34.7 shows the three basic logic gates that we use in the circuit-satisﬁability
problem: the NOT gate (or inverter), the AND gate, and the OR gate. The NOT
gate takes a single binary input x, whose value is either 0 or 1, and produces a
binary output ´ whose value is opposite that of the input value. Each of the other
two gates takes two binary inputs x and y and produces a single binary output ´.
We can describe the operation of each gate, and of any boolean combinational
element, by a truth table, shown under each gate in Figure 34.7. A truth table gives
the outputs of the combinational element for each possible setting of the inputs. For

## 34.3 NP-completeness and reducibility

x
y
z
x
y
z
(b)
(c)
x
z
(a)
x
x
x
y
y
:x
x ^ y
x _ y
Figure 34.7
Three basic logic gates, with binary inputs and outputs. Under each gate is the truth
table that describes the gate’s operation. (a) The NOT gate. (b) The AND gate. (c) The OR gate.
example, the truth table for the OR gate tells us that when the inputs are x D 0
and y D 1, the output value is ´ D 1. We use the symbols : to denote the NOT
function, ^ to denote the AND function, and _ to denote the OR function. Thus,
for example, 0 _ 1 D 1.
We can generalize AND and OR gates to take more than two inputs. An AND
gate’s output is 1 if all of its inputs are 1, and its output is 0 otherwise. An OR gate’s
output is 1 if any of its inputs are 1, and its output is 0 otherwise.
A boolean combinational circuit consists of one or more boolean combinational
elements interconnected by wires. A wire can connect the output of one element
to the input of another, thereby providing the output value of the ﬁrst element as an
input value of the second. Figure 34.8 shows two similar boolean combinational
circuits, differing in only one gate. Part (a) of the ﬁgure also shows the values on
the individual wires, given the input hx1 D 1; x2 D 1; x3 D 0i. Although a single
wire may have no more than one combinational-element output connected to it, it
can feed several element inputs. The number of element inputs fed by a wire is
called the fan-out of the wire. If no element output is connected to a wire, the wire
is a circuit input, accepting input values from an external source. If no element
input is connected to a wire, the wire is a circuit output, providing the results of
the circuit’s computation to the outside world. (An internal wire can also fan out
to a circuit output.) For the purpose of deﬁning the circuit-satisﬁability problem,
we limit the number of circuit outputs to 1, though in actual hardware design, a
boolean combinational circuit may have multiple outputs.
Boolean combinational circuits contain no cycles. In other words, suppose we
create a directed graph G D .V; E/ with one vertex for each combinational element
and with k directed edges for each wire whose fan-out is k; the graph contains
a directed edge .u; / if a wire connects the output of element u to an input of
element . Then G must be acyclic.

x3
x2
x1
(a)
x3
x2
x1
(b)
Figure 34.8
Two instances of the circuit-satisﬁability problem.
(a) The assignment hx1 D 1;
x2 D 1; x3 D 0i to the inputs of this circuit causes the output of the circuit to be 1. The circuit
is therefore satisﬁable. (b) No assignment to the inputs of this circuit can cause the output of the
circuit to be 1. The circuit is therefore unsatisﬁable.
A truth assignment for a boolean combinational circuit is a set of boolean input
values. We say that a one-output boolean combinational circuit is satisﬁable if it
has a satisfying assignment: a truth assignment that causes the output of the circuit
to be 1. For example, the circuit in Figure 34.8(a) has the satisfying assignment
hx1 D 1; x2 D 1; x3 D 0i, and so it is satisﬁable. As Exercise 34.3-1 asks you to
show, no assignment of values to x1, x2, and x3 causes the circuit in Figure 34.8(b)
to produce a 1 output; it always produces 0, and so it is unsatisﬁable.
The circuit-satisﬁability problem is, “Given a boolean combinational circuit
composed of AND, OR, and NOT gates, is it satisﬁable?” In order to pose this
question formally, however, we must agree on a standard encoding for circuits.
The size of a boolean combinational circuit is the number of boolean combinational elements plus the number of wires in the circuit. We could devise a graphlike
encoding that maps any given circuit C into a binary string hCi whose length is
polynomial in the size of the circuit itself. As a formal language, we can therefore
deﬁne
CIRCUIT-SAT D fhCi W C is a satisﬁable boolean combinational circuitg :
The circuit-satisﬁability problem arises in the area of computer-aided hardware
optimization. If a subcircuit always produces 0, that subcircuit is unnecessary;
the designer can replace it by a simpler subcircuit that omits all logic gates and
provides the constant 0 value as its output. You can see why we would like to have
a polynomial-time algorithm for this problem.
Given a circuit C, we might attempt to determine whether it is satisﬁable by
simply checking all possible assignments to the inputs. Unfortunately, if the circuit
has k inputs, then we would have to check up to 2k possible assignments. When

## 34.3 NP-completeness and reducibility

the size of C is polynomial in k, checking each one takes .2k/ time, which is
superpolynomial in the size of the circuit.9 In fact, as we have claimed, there is
strong evidence that no polynomial-time algorithm exists that solves the circuitsatisﬁability problem because circuit satisﬁability is NP-complete. We break the
proof of this fact into two parts, based on the two parts of the deﬁnition of NPcompleteness.

> **Lemma 34.5**

The circuit-satisﬁability problem belongs to the class NP.
Proof
We shall provide a two-input, polynomial-time algorithm A that can verify
CIRCUIT-SAT. One of the inputs to A is (a standard encoding of) a boolean combinational circuit C. The other input is a certiﬁcate corresponding to an assignment
of boolean values to the wires in C. (See Exercise 34.3-4 for a smaller certiﬁcate.)
We construct the algorithm A as follows. For each logic gate in the circuit, it
checks that the value provided by the certiﬁcate on the output wire is correctly
computed as a function of the values on the input wires. Then, if the output of the
entire circuit is 1, the algorithm outputs 1, since the values assigned to the inputs
of C provide a satisfying assignment. Otherwise, A outputs 0.
Whenever a satisﬁable circuit C is input to algorithm A, there exists a certiﬁcate
whose length is polynomial in the size of C and that causes A to output a 1. Whenever an unsatisﬁable circuit is input, no certiﬁcate can fool A into believing that
the circuit is satisﬁable. Algorithm A runs in polynomial time: with a good implementation, linear time sufﬁces. Thus, we can verify CIRCUIT-SAT in polynomial
time, and CIRCUIT-SAT 2 NP.
The second part of proving that CIRCUIT-SAT is NP-complete is to show that
the language is NP-hard. That is, we must show that every language in NP is
polynomial-time reducible to CIRCUIT-SAT. The actual proof of this fact is full
of technical intricacies, and so we shall settle for a sketch of the proof based on
some understanding of the workings of computer hardware.
A computer program is stored in the computer memory as a sequence of instructions. A typical instruction encodes an operation to be performed, addresses
of operands in memory, and an address where the result is to be stored. A special memory location, called the program counter, keeps track of which instruc9On the other hand, if the size of the circuit C is ‚.2k/, then an algorithm whose running time
is O.2k/ has a running time that is polynomial in the circuit size. Even if P ¤ NP, this situation would not contradict the NP-completeness of the problem; the existence of a polynomial-time
algorithm for a special case does not imply that there is a polynomial-time algorithm for all cases.

tion is to be executed next. The program counter automatically increments upon
fetching each instruction, thereby causing the computer to execute instructions sequentially. The execution of an instruction can cause a value to be written to the
program counter, however, which alters the normal sequential execution and allows
the computer to loop and perform conditional branches.
At any point during the execution of a program, the computer’s memory holds
the entire state of the computation. (We take the memory to include the program
itself, the program counter, working storage, and any of the various bits of state
that a computer maintains for bookkeeping.) We call any particular state of computer memory a conﬁguration. We can view the execution of an instruction as
mapping one conﬁguration to another. The computer hardware that accomplishes
this mapping can be implemented as a boolean combinational circuit, which we
denote by M in the proof of the following lemma.

> **Lemma 34.6**

The circuit-satisﬁability problem is NP-hard.
Proof
Let L be any language in NP. We shall describe a polynomial-time algorithm F computing a reduction function f that maps every binary string x to a
circuit C D f .x/ such that x 2 L if and only if C 2 CIRCUIT-SAT.
Since L 2 NP, there must exist an algorithm A that veriﬁes L in polynomial
time. The algorithm F that we shall construct uses the two-input algorithm A to
compute the reduction function f .
Let T .n/ denote the worst-case running time of algorithm A on length-n input
strings, and let k  1 be a constant such that T .n/ D O.nk/ and the length of the
certiﬁcate is O.nk/. (The running time of A is actually a polynomial in the total
input size, which includes both an input string and a certiﬁcate, but since the length
of the certiﬁcate is polynomial in the length n of the input string, the running time
is polynomial in n.)
The basic idea of the proof is to represent the computation of A as a sequence
of conﬁgurations. As Figure 34.9 illustrates, we can break each conﬁguration into
parts consisting of the program for A, the program counter and auxiliary machine
state, the input x, the certiﬁcate y, and working storage. The combinational circuit M, which implements the computer hardware, maps each conﬁguration ci to
the next conﬁguration ciC1, starting from the initial conﬁguration c0. Algorithm A
writes its output—0 or 1—to some designated location by the time it ﬁnishes executing, and if we assume that thereafter A halts, the value never changes. Thus,
if the algorithm runs for at most T .n/ steps, the output appears as one of the bits
in cT .n/.
The reduction algorithm F constructs a single combinational circuit that computes all conﬁgurations produced by a given initial conﬁguration. The idea is to

## 34.3 NP-completeness and reducibility

M
A
PC
aux machine state
x
y
working storage
A
PC
aux machine state
x
y
working storage
M
A
PC
aux machine state
x
y
working storage
M
A
PC
aux machine state
x
y
…
working storage
0/1 output
M
c0
c1
c2
cT(n)
Figure 34.9
The sequence of conﬁgurations produced by an algorithm A running on an input x and
certiﬁcate y. Each conﬁguration represents the state of the computer for one step of the computation
and, besides A, x, and y, includes the program counter (PC), auxiliary machine state, and working
storage. Except for the certiﬁcate y, the initial conﬁguration c0 is constant. A boolean combinational
circuit M maps each conﬁguration to the next conﬁguration. The output is a distinguished bit in the
working storage.

paste together T .n/ copies of the circuit M. The output of the ith circuit, which
produces conﬁguration ci, feeds directly into the input of the .i C1/st circuit. Thus,
the conﬁgurations, rather than being stored in the computer’s memory, simply reside as values on the wires connecting copies of M.
Recall what the polynomial-time reduction algorithm F must do. Given an input x, it must compute a circuit C D f .x/ that is satisﬁable if and only if there
exists a certiﬁcate y such that A.x; y/ D 1. When F obtains an input x, it ﬁrst
computes n D jxj and constructs a combinational circuit C 0 consisting of T .n/
copies of M. The input to C 0 is an initial conﬁguration corresponding to a computation on A.x; y/, and the output is the conﬁguration cT .n/.
Algorithm F modiﬁes circuit C 0 slightly to construct the circuit C D f .x/.
First, it wires the inputs to C 0 corresponding to the program for A, the initial program counter, the input x, and the initial state of memory directly to these known
values. Thus, the only remaining inputs to the circuit correspond to the certiﬁcate y. Second, it ignores all outputs from C 0, except for the one bit of cT .n/
corresponding to the output of A.
This circuit C, so constructed, computes
C.y/ D A.x; y/ for any input y of length O.nk/. The reduction algorithm F ,
when provided an input string x, computes such a circuit C and outputs it.
We need to prove two properties. First, we must show that F correctly computes
a reduction function f . That is, we must show that C is satisﬁable if and only if
there exists a certiﬁcate y such that A.x; y/ D 1. Second, we must show that F
runs in polynomial time.
To show that F correctly computes a reduction function, let us suppose that there
exists a certiﬁcate y of length O.nk/ such that A.x; y/ D 1. Then, if we apply the
bits of y to the inputs of C, the output of C is C.y/ D A.x; y/ D 1. Thus, if a
certiﬁcate exists, then C is satisﬁable. For the other direction, suppose that C is
satisﬁable. Hence, there exists an input y to C such that C.y/ D 1, from which
we conclude that A.x; y/ D 1. Thus, F correctly computes a reduction function.
To complete the proof sketch, we need only show that F runs in time polynomial
in n D jxj. The ﬁrst observation we make is that the number of bits required to
represent a conﬁguration is polynomial in n. The program for A itself has constant
size, independent of the length of its input x. The length of the input x is n, and
the length of the certiﬁcate y is O.nk/. Since the algorithm runs for at most O.nk/
steps, the amount of working storage required by A is polynomial in n as well.
(We assume that this memory is contiguous; Exercise 34.3-5 asks you to extend
the argument to the situation in which the locations accessed by A are scattered
across a much larger region of memory and the particular pattern of scattering can
differ for each input x.)
The combinational circuit M implementing the computer hardware has size
polynomial in the length of a conﬁguration, which is O.nk/; hence, the size of M
is polynomial in n. (Most of this circuitry implements the logic of the memory

## 34.3 NP-completeness and reducibility

system.) The circuit C consists of at most t D O.nk/ copies of M, and hence it
has size polynomial in n. The reduction algorithm F can construct C from x in
polynomial time, since each step of the construction takes polynomial time.
The language CIRCUIT-SAT is therefore at least as hard as any language in NP,
and since it belongs to NP, it is NP-complete.

> **Theorem 34.7**

The circuit-satisﬁability problem is NP-complete.
Proof
Immediate from Lemmas 34.5 and 34.6 and from the deﬁnition of NPcompleteness.

## Exercises

34.3-1
Verify that the circuit in Figure 34.8(b) is unsatisﬁable.
34.3-2
Show that the P relation is a transitive relation on languages. That is, show that if
L1 P L2 and L2 P L3, then L1 P L3.
34.3-3
Prove that L P L if and only if L P L.
34.3-4
Show that we could have used a satisfying assignment as a certiﬁcate in an alternative proof of Lemma 34.5. Which certiﬁcate makes for an easier proof?
34.3-5
The proof of Lemma 34.6 assumes that the working storage for algorithm A occupies a contiguous region of polynomial size. Where in the proof do we exploit this
assumption? Argue that this assumption does not involve any loss of generality.
34.3-6
A language L is complete for a language class C with respect to polynomial-time
reductions if L 2 C and L0 P L for all L0 2 C. Show that ; and f0; 1g are the
only languages in P that are not complete for P with respect to polynomial-time
reductions.

34.3-7
Show that, with respect to polynomial-time reductions (see Exercise 34.3-6), L is
complete for NP if and only if L is complete for co-NP.
34.3-8
The reduction algorithm F in the proof of Lemma 34.6 constructs the circuit
C D f .x/ based on knowledge of x, A, and k. Professor Sartre observes that
the string x is input to F , but only the existence of A, k, and the constant factor
implicit in the O.nk/ running time is known to F (since the language L belongs
to NP), not their actual values. Thus, the professor concludes that F can’t possibly construct the circuit C and that the language CIRCUIT-SAT is not necessarily
NP-hard. Explain the ﬂaw in the professor’s reasoning.

## 34.4 NP-completeness proofs

We proved that the circuit-satisﬁability problem is NP-complete by a direct proof
that L P CIRCUIT-SAT for every language L 2 NP. In this section, we shall
show how to prove that languages are NP-complete without directly reducing every
language in NP to the given language. We shall illustrate this methodology by
proving that various formula-satisﬁability problems are NP-complete. Section 34.5
provides many more examples of the methodology.
The following lemma is the basis of our method for showing that a language is
NP-complete.

> **Lemma 34.8**

If L is a language such that L0 P L for some L0 2 NPC, then L is NP-hard. If, in
addition, L 2 NP, then L 2 NPC.
Proof
Since L0 is NP-complete, for all L00 2 NP, we have L00 P L0. By supposition, L0 P L, and thus by transitivity (Exercise 34.3-2), we have L00 P L,
which shows that L is NP-hard. If L 2 NP, we also have L 2 NPC.
In other words, by reducing a known NP-complete language L0 to L, we implicitly reduce every language in NP to L. Thus, Lemma 34.8 gives us a method for
proving that a language L is NP-complete:
1. Prove L 2 NP.
2. Select a known NP-complete language L0.

## 34.4 NP-completeness proofs

3. Describe an algorithm that computes a function f mapping every instance
x 2 f0; 1g of L0 to an instance f .x/ of L.
4. Prove that the function f satisﬁes x 2 L0 if and only if f .x/ 2 L for all
x 2 f0; 1g.
5. Prove that the algorithm computing f runs in polynomial time.
(Steps 2–5 show that L is NP-hard.) This methodology of reducing from a single known NP-complete language is far simpler than the more complicated process of showing directly how to reduce from every language in NP.
Proving
CIRCUIT-SAT 2 NPC has given us a “foot in the door.” Because we know that the
circuit-satisﬁability problem is NP-complete, we now can prove much more easily
that other problems are NP-complete. Moreover, as we develop a catalog of known
NP-complete problems, we will have more and more choices for languages from
which to reduce.
Formula satisﬁability
We illustrate the reduction methodology by giving an NP-completeness proof for
the problem of determining whether a boolean formula, not a circuit, is satisﬁable.
This problem has the historical honor of being the ﬁrst problem ever shown to be
NP-complete.
We formulate the (formula) satisﬁability problem in terms of the language SAT
as follows. An instance of SAT is a boolean formula  composed of
1. n boolean variables: x1; x2; : : : ; xn;
2. m boolean connectives: any boolean function with one or two inputs and one
output, such as ^ (AND), _ (OR), : (NOT), ! (implication), $ (if and only
if); and
3. parentheses. (Without loss of generality, we assume that there are no redundant
parentheses, i.e., a formula contains at most one pair of parentheses per boolean
connective.)
We can easily encode a boolean formula  in a length that is polynomial in n C m.
As in boolean combinational circuits, a truth assignment for a boolean formula 
is a set of values for the variables of , and a satisfying assignment is a truth
assignment that causes it to evaluate to 1. A formula with a satisfying assignment
is a satisﬁable formula. The satisﬁability problem asks whether a given boolean
formula is satisﬁable; in formal-language terms,
SAT D fhi W  is a satisﬁable boolean formulag :
As an example, the formula

 D ..x1 ! x2/ _ :..:x1 $ x3/ _ x4// ^ :x2
has the satisfying assignment hx1 D 0; x2 D 0; x3 D 1; x4 D 1i, since

D
..0 ! 0/ _ :..:0 $ 1/ _ 1// ^ :0
(34.2)
D
.1 _ :.1 _ 1// ^ 1
D
.1 _ 0/ ^ 1
D
1 ;
and thus this formula  belongs to SAT.
The naive algorithm to determine whether an arbitrary boolean formula is satisﬁable does not run in polynomial time. A formula with n variables has 2n possible
assignments. If the length of hi is polynomial in n, then checking every assignment requires .2n/ time, which is superpolynomial in the length of hi. As the
following theorem shows, a polynomial-time algorithm is unlikely to exist.

> **Theorem 34.9**

Satisﬁability of boolean formulas is NP-complete.
Proof
We start by arguing that SAT 2 NP. Then we prove that SAT is NP-hard by
showing that CIRCUIT-SAT P SAT; by Lemma 34.8, this will prove the theorem.
To show that SAT belongs to NP, we show that a certiﬁcate consisting of a
satisfying assignment for an input formula  can be veriﬁed in polynomial time.
The verifying algorithm simply replaces each variable in the formula with its corresponding value and then evaluates the expression, much as we did in equation (34.2) above. This task is easy to do in polynomial time. If the expression
evaluates to 1, then the algorithm has veriﬁed that the formula is satisﬁable. Thus,
the ﬁrst condition of Lemma 34.8 for NP-completeness holds.
To prove that SAT is NP-hard, we show that CIRCUIT-SAT P SAT. In other
words, we need to show how to reduce any instance of circuit satisﬁability to an
instance of formula satisﬁability in polynomial time. We can use induction to
express any boolean combinational circuit as a boolean formula. We simply look
at the gate that produces the circuit output and inductively express each of the
gate’s inputs as formulas. We then obtain the formula for the circuit by writing an
expression that applies the gate’s function to its inputs’ formulas.
Unfortunately, this straightforward method does not amount to a polynomialtime reduction. As Exercise 34.4-1 asks you to show, shared subformulas—which
arise from gates whose output wires have fan-out of 2 or more—can cause the
size of the generated formula to grow exponentially. Thus, the reduction algorithm
must be somewhat more clever.
Figure 34.10 illustrates how we overcome this problem, using as an example
the circuit from Figure 34.8(a). For each wire xi in the circuit C, the formula 

## 34.4 NP-completeness proofs

x6
x3
x4
x7
x10
x9
x8
x5
x2
x1
Figure 34.10
Reducing circuit satisﬁability to formula satisﬁability. The formula produced by the
reduction algorithm has a variable for each wire in the circuit.
has a variable xi. We can now express how each gate operates as a small formula
involving the variables of its incident wires. For example, the operation of the
output AND gate is x10 $ .x7 ^ x8 ^ x9/. We call each of these small formulas a
clause.
The formula  produced by the reduction algorithm is the AND of the circuitoutput variable with the conjunction of clauses describing the operation of each
gate. For the circuit in the ﬁgure, the formula is
 D x10 ^ .x4 $ :x3/
^ .x5 $ .x1 _ x2//
^ .x6 $ :x4/
^ .x7 $ .x1 ^ x2 ^ x4//
^ .x8 $ .x5 _ x6//
^ .x9 $ .x6 _ x7//
^ .x10 $ .x7 ^ x8 ^ x9// :
Given a circuit C, it is straightforward to produce such a formula  in polynomial
time.
Why is the circuit C satisﬁable exactly when the formula  is satisﬁable? If C
has a satisfying assignment, then each wire of the circuit has a well-deﬁned value,
and the output of the circuit is 1.
Therefore, when we assign wire values to
variables in , each clause of  evaluates to 1, and thus the conjunction of all
evaluates to 1. Conversely, if some assignment causes  to evaluate to 1, the
circuit C is satisﬁable by an analogous argument.
Thus, we have shown that
CIRCUIT-SAT P SAT, which completes the proof.

3-CNF satisﬁability
We can prove many problems NP-complete by reducing from formula satisﬁability.
The reduction algorithm must handle any input formula, though, and this requirement can lead to a huge number of cases that we must consider. We often prefer
to reduce from a restricted language of boolean formulas, so that we need to consider fewer cases. Of course, we must not restrict the language so much that it
becomes polynomial-time solvable. One convenient language is 3-CNF satisﬁability, or 3-CNF-SAT.
We deﬁne 3-CNF satisﬁability using the following terms. A literal in a boolean
formula is an occurrence of a variable or its negation. A boolean formula is in
conjunctive normal form, or CNF, if it is expressed as an AND of clauses, each
of which is the OR of one or more literals. A boolean formula is in 3-conjunctive
normal form, or 3-CNF, if each clause has exactly three distinct literals.
For example, the boolean formula
.x1 _ :x1 _ :x2/ ^ .x3 _ x2 _ x4/ ^ .:x1 _ :x3 _ :x4/
is in 3-CNF. The ﬁrst of its three clauses is .x1 _ :x1 _ :x2/, which contains the
three literals x1, :x1, and :x2.
In 3-CNF-SAT, we are asked whether a given boolean formula  in 3-CNF is
satisﬁable. The following theorem shows that a polynomial-time algorithm that
can determine the satisﬁability of boolean formulas is unlikely to exist, even when
they are expressed in this simple normal form.

> **Theorem 34.10**

Satisﬁability of boolean formulas in 3-conjunctive normal form is NP-complete.
Proof
The argument we used in the proof of Theorem 34.9 to show that SAT 2
NP applies equally well here to show that 3-CNF-SAT 2 NP. By Lemma 34.8,
therefore, we need only show that SAT P 3-CNF-SAT.
We break the reduction algorithm into three basic steps. Each step progressively
transforms the input formula  closer to the desired 3-conjunctive normal form.
The ﬁrst step is similar to the one used to prove CIRCUIT-SAT P SAT in

> **Theorem 34.9. First, we construct a binary “parse” tree for the input formula ,**

with literals as leaves and connectives as internal nodes. Figure 34.11 shows such
a parse tree for the formula
 D ..x1 ! x2/ _ :..:x1 $ x3/ _ x4// ^ :x2 :
(34.3)
Should the input formula contain a clause such as the OR of several literals, we use
associativity to parenthesize the expression fully so that every internal node in the
resulting tree has 1 or 2 children. We can now think of the binary parse tree as a
circuit for computing the function.

## 34.4 NP-completeness proofs

:x1
x1
:x2
x2
x3
x4
y1
y2
y3
y4
y5
y6
^
$
_
_
:
!
Figure 34.11
The tree corresponding to the formula  D ..x1 !x2/_:..:x1 $x3/_x4//^:x2:
Mimicking the reduction in the proof of Theorem 34.9, we introduce a variable yi for the output of each internal node. Then, we rewrite the original formula  as the AND of the root variable and a conjunction of clauses describing the
operation of each node. For the formula (34.3), the resulting expression is
0 D y1 ^ .y1 $ .y2 ^ :x2//
^ .y2 $ .y3 _ y4//
^ .y3 $ .x1 ! x2//
^ .y4 $ :y5/
^ .y5 $ .y6 _ x4//
^ .y6 $ .:x1 $ x3// :
Observe that the formula 0 thus obtained is a conjunction of clauses 0
i, each of
which has at most 3 literals. The only requirement that we might fail to meet is
that each clause has to be an OR of 3 literals.
The second step of the reduction converts each clause 0
i into conjunctive normal
form. We construct a truth table for 0
i by evaluating all possible assignments to
its variables. Each row of the truth table consists of a possible assignment of the
variables of the clause, together with the value of the clause under that assignment.
Using the truth-table entries that evaluate to 0, we build a formula in disjunctive
normal form (or DNF)—an OR of ANDs—that is equivalent to :0
i. We then
negate this formula and convert it into a CNF formula 00
i by using DeMorgan’s

y1
y2
x2
.y1 $ .y2 ^ :x2//
Figure 34.12
The truth table for the clause .y1 $ .y2 ^ :x2//.
laws for propositional logic,
:.a ^ b/
D
:a _ :b ;
:.a _ b/
D
:a ^ :b ;
to complement all literals, change ORs into ANDs, and change ANDs into ORs.
In our example, we convert the clause 0
1 D .y1 $ .y2 ^ :x2// into CNF
as follows. The truth table for 0
1 appears in Figure 34.12. The DNF formula
equivalent to :0
1 is
.y1 ^ y2 ^ x2/ _ .y1 ^ :y2 ^ x2/ _ .y1 ^ :y2 ^ :x2/ _ .:y1 ^ y2 ^ :x2/ :
Negating and applying DeMorgan’s laws, we get the CNF formula
00
D
.:y1 _ :y2 _ :x2/ ^ .:y1 _ y2 _ :x2/
^ .:y1 _ y2 _ x2/ ^ .y1 _ :y2 _ x2/ ;
which is equivalent to the original clause 0
1.
At this point, we have converted each clause 0
i of the formula 0 into a CNF
formula 00
i , and thus 0 is equivalent to the CNF formula 00 consisting of the
conjunction of the 00
i . Moreover, each clause of 00 has at most 3 literals.
The third and ﬁnal step of the reduction further transforms the formula so that
each clause has exactly 3 distinct literals. We construct the ﬁnal 3-CNF formula 000
from the clauses of the CNF formula 00. The formula 000 also uses two auxiliary
variables that we shall call p and q. For each clause Ci of 00, we include the
following clauses in 000:

If Ci has 3 distinct literals, then simply include Ci as a clause of 000.

If Ci has 2 distinct literals, that is, if Ci D .l1 _ l2/, where l1 and l2 are literals,
then include .l1 _ l2 _ p/ ^ .l1 _ l2 _ :p/ as clauses of 000. The literals
p and :p merely fulﬁll the syntactic requirement that each clause of 000 has

## 34.4 NP-completeness proofs

exactly 3 distinct literals. Whether p D 0 or p D 1, one of the clauses is
equivalent to l1 _l2, and the other evaluates to 1, which is the identity for AND.

If Ci has just 1 distinct literal l, then include .l _ p _ q/ ^ .l _ p _ :q/ ^
.l _ :p _ q/ ^ .l _ :p _ :q/ as clauses of 000. Regardless of the values of p
and q, one of the four clauses is equivalent to l, and the other 3 evaluate to 1.
We can see that the 3-CNF formula 000 is satisﬁable if and only if  is satisﬁable
by inspecting each of the three steps. Like the reduction from CIRCUIT-SAT to
SAT, the construction of 0 from  in the ﬁrst step preserves satisﬁability. The
second step produces a CNF formula 00 that is algebraically equivalent to 0. The
third step produces a 3-CNF formula 000 that is effectively equivalent to 00, since
any assignment to the variables p and q produces a formula that is algebraically
equivalent to 00.
We must also show that the reduction can be computed in polynomial time. Constructing 0 from  introduces at most 1 variable and 1 clause per connective in .
Constructing 00 from 0 can introduce at most 8 clauses into 00 for each clause
from 0, since each clause of 0 has at most 3 variables, and the truth table for
each clause has at most 23 D 8 rows. The construction of 000 from 00 introduces
at most 4 clauses into 000 for each clause of 00. Thus, the size of the resulting
formula 000 is polynomial in the length of the original formula. Each of the constructions can easily be accomplished in polynomial time.

## Exercises

34.4-1
Consider the straightforward (nonpolynomial-time) reduction in the proof of Theorem 34.9. Describe a circuit of size n that, when converted to a formula by this
method, yields a formula whose size is exponential in n.
34.4-2
Show the 3-CNF formula that results when we use the method of Theorem 34.10
on the formula (34.3).
34.4-3
Professor Jagger proposes to show that SAT P 3-CNF-SAT by using only the
truth-table technique in the proof of Theorem 34.10, and not the other steps. That
is, the professor proposes to take the boolean formula , form a truth table for
its variables, derive from the truth table a formula in 3-DNF that is equivalent
to :, and then negate and apply DeMorgan’s laws to produce a 3-CNF formula
equivalent to . Show that this strategy does not yield a polynomial-time reduction.

34.4-4
Show that the problem of determining whether a boolean formula is a tautology is
complete for co-NP. (Hint: See Exercise 34.3-7.)
34.4-5
Show that the problem of determining the satisﬁability of boolean formulas in disjunctive normal form is polynomial-time solvable.
34.4-6
Suppose that someone gives you a polynomial-time algorithm to decide formula
satisﬁability. Describe how to use this algorithm to ﬁnd satisfying assignments in
polynomial time.
34.4-7
Let 2-CNF-SAT be the set of satisﬁable boolean formulas in CNF with exactly 2
literals per clause. Show that 2-CNF-SAT 2 P. Make your algorithm as efﬁcient as
possible. (Hint: Observe that x _ y is equivalent to :x ! y. Reduce 2-CNF-SAT
to an efﬁciently solvable problem on a directed graph.)

## 34.5 NP-complete problems

NP-complete problems arise in diverse domains: boolean logic, graphs, arithmetic,
network design, sets and partitions, storage and retrieval, sequencing and scheduling, mathematical programming, algebra and number theory, games and puzzles,
automata and language theory, program optimization, biology, chemistry, physics,
and more. In this section, we shall use the reduction methodology to provide NPcompleteness proofs for a variety of problems drawn from graph theory and set
partitioning.
Figure 34.13 outlines the structure of the NP-completeness proofs in this section
and Section 34.4. We prove each language in the ﬁgure to be NP-complete by
reduction from the language that points to it. At the root is CIRCUIT-SAT, which
we proved NP-complete in Theorem 34.7.

## 34.5.1 The clique problem

A clique in an undirected graph G D .V; E/ is a subset V 0  V of vertices, each
pair of which is connected by an edge in E. In other words, a clique is a complete
subgraph of G. The size of a clique is the number of vertices it contains. The
clique problem is the optimization problem of ﬁnding a clique of maximum size in

## 34.5 NP-complete problems

CIRCUIT-SAT
SAT
3-CNF-SAT
CLIQUE
VERTEX-COVER
SUBSET-SUM
HAM-CYCLE
TSP
Figure 34.13
The structure of NP-completeness proofs in Sections 34.4 and 34.5. All proofs ultimately follow by reduction from the NP-completeness of CIRCUIT-SAT.
a graph. As a decision problem, we ask simply whether a clique of a given size k
exists in the graph. The formal deﬁnition is
CLIQUE D fhG; ki W G is a graph containing a clique of size kg :
A naive algorithm for determining whether a graph G D .V; E/ with jV j vertices has a clique of size k is to list all k-subsets of V , and check each one to
see whether it forms a clique. The running time of this algorithm is .k2
jV j
k

/,
which is polynomial if k is a constant. In general, however, k could be near jV j =2,
in which case the algorithm runs in superpolynomial time. Indeed, an efﬁcient
algorithm for the clique problem is unlikely to exist.

> **Theorem 34.11**

The clique problem is NP-complete.
Proof
To show that CLIQUE 2 NP, for a given graph G D .V; E/, we use the
set V 0  V of vertices in the clique as a certiﬁcate for G. We can check whether V 0
is a clique in polynomial time by checking whether, for each pair u;  2 V 0, the
edge .u; / belongs to E.
We next prove that 3-CNF-SAT P CLIQUE, which shows that the clique problem is NP-hard. You might be surprised that we should be able to prove such a
result, since on the surface logical formulas seem to have little to do with graphs.
The reduction algorithm begins with an instance of 3-CNF-SAT.
Let  D
C1 ^ C2 ^    ^ Ck be a boolean formula in 3-CNF with k clauses. For r D

x1
x1
x2
x2
x3
x3
:x1
:x2
:x3
C1 D x1 _ :x2 _ :x3
C2 D :x1 _ x2 _ x3
C3 D x1 _ x2 _ x3
Figure 34.14
The graph G derived from the 3-CNF formula  D C1 ^ C2 ^ C3, where C1 D
.x1 _ :x2 _ :x3/, C2 D .:x1 _ x2 _ x3/, and C3 D .x1 _ x2 _ x3/, in reducing 3-CNF-SAT to
CLIQUE. A satisfying assignment of the formula has x2 D 0, x3 D 1, and x1 either 0 or 1. This
assignment satisﬁes C1 with :x2, and it satisﬁes C2 and C3 with x3, corresponding to the clique
with lightly shaded vertices.
1; 2; : : : ; k, each clause Cr has exactly three distinct literals lr
1, lr
2, and lr
3. We shall
construct a graph G such that  is satisﬁable if and only if G has a clique of size k.
We construct the graph G D .V; E/ as follows.
For each clause Cr
D
.lr
1 _ lr
2 _ lr
3/ in , we place a triple of vertices r
1, r
2, and r
3 into V . We put
an edge between two vertices r
i and s
j if both of the following hold:

r
i and s
j are in different triples, that is, r ¤ s, and

their corresponding literals are consistent, that is, lr
i is not the negation of ls
j .
We can easily build this graph from  in polynomial time. As an example of this
construction, if we have
 D .x1 _ :x2 _ :x3/ ^ .:x1 _ x2 _ x3/ ^ .x1 _ x2 _ x3/ ;
then G is the graph shown in Figure 34.14.
We must show that this transformation of  into G is a reduction. First, suppose
that  has a satisfying assignment. Then each clause Cr contains at least one
literal lr
i that is assigned 1, and each such literal corresponds to a vertex r
i . Picking
one such “true” literal from each clause yields a set V 0 of k vertices. We claim that
V 0 is a clique. For any two vertices r
i ; s
j 2 V 0, where r ¤ s, both corresponding
literals lr
i and ls
j map to 1 by the given satisfying assignment, and thus the literals

## 34.5 NP-complete problems

cannot be complements. Thus, by the construction of G, the edge .r
i ; s
j / belongs
to E.
Conversely, suppose that G has a clique V 0 of size k. No edges in G connect
vertices in the same triple, and so V 0 contains exactly one vertex per triple. We can
assign 1 to each literal lr
i such that r
i 2 V 0 without fear of assigning 1 to both a
literal and its complement, since G contains no edges between inconsistent literals.
Each clause is satisﬁed, and so  is satisﬁed. (Any variables that do not correspond
to a vertex in the clique may be set arbitrarily.)
In the example of Figure 34.14, a satisfying assignment of  has x2 D 0 and
x3 D 1. A corresponding clique of size k D 3 consists of the vertices corresponding to :x2 from the ﬁrst clause, x3 from the second clause, and x3 from the third
clause. Because the clique contains no vertices corresponding to either x1 or :x1,
we can set x1 to either 0 or 1 in this satisfying assignment.
Observe that in the proof of Theorem 34.11, we reduced an arbitrary instance
of 3-CNF-SAT to an instance of CLIQUE with a particular structure. You might
think that we have shown only that CLIQUE is NP-hard in graphs in which the
vertices are restricted to occur in triples and in which there are no edges between
vertices in the same triple. Indeed, we have shown that CLIQUE is NP-hard only
in this restricted case, but this proof sufﬁces to show that CLIQUE is NP-hard in
general graphs. Why? If we had a polynomial-time algorithm that solved CLIQUE
on general graphs, it would also solve CLIQUE on restricted graphs.
The opposite approach—reducing instances of 3-CNF-SAT with a special structure to general instances of CLIQUE—would not have sufﬁced, however. Why
not? Perhaps the instances of 3-CNF-SAT that we chose to reduce from were
“easy,” and so we would not have reduced an NP-hard problem to CLIQUE.
Observe also that the reduction used the instance of 3-CNF-SAT, but not the
solution. We would have erred if the polynomial-time reduction had relied on
knowing whether the formula  is satisﬁable, since we do not know how to decide
whether  is satisﬁable in polynomial time.

## 34.5.2 The vertex-cover problem

A vertex cover of an undirected graph G D .V; E/ is a subset V 0  V such that
if .u; / 2 E, then u 2 V 0 or  2 V 0 (or both). That is, each vertex “covers” its
incident edges, and a vertex cover for G is a set of vertices that covers all the edges
in E. The size of a vertex cover is the number of vertices in it. For example, the
graph in Figure 34.15(b) has a vertex cover fw; ´g of size 2.
The vertex-cover problem is to ﬁnd a vertex cover of minimum size in a given
graph. Restating this optimization problem as a decision problem, we wish to

u
v
y
x
z
w
(a)
u
v
y
x
z
w
(b)
Figure 34.15
Reducing CLIQUE to VERTEX-COVER. (a) An undirected graph G D .V; E/ with
clique V 0 D fu; ; x; yg. (b) The graph G produced by the reduction algorithm that has vertex cover
V  V 0 D fw; ´g.
determine whether a graph has a vertex cover of a given size k. As a language, we
deﬁne
VERTEX-COVER D fhG; ki W graph G has a vertex cover of size kg :
The following theorem shows that this problem is NP-complete.

> **Theorem 34.12**

The vertex-cover problem is NP-complete.
Proof
We ﬁrst show that VERTEX-COVER 2 NP. Suppose we are given a graph
G D .V; E/ and an integer k. The certiﬁcate we choose is the vertex cover V 0  V
itself. The veriﬁcation algorithm afﬁrms that jV 0j D k, and then it checks, for each
edge .u; / 2 E, that u 2 V 0 or  2 V 0. We can easily verify the certiﬁcate in
polynomial time.
We prove that the vertex-cover problem is NP-hard by showing that CLIQUE P
VERTEX-COVER. This reduction relies on the notion of the “complement” of a
graph. Given an undirected graph G D .V; E/, we deﬁne the complement of G
as G D .V; E/, where E D f.u; / W u;  2 V; u ¤ ; and .u; / 62 Eg. In other
words, G is the graph containing exactly those edges that are not in G. Figure 34.15
shows a graph and its complement and illustrates the reduction from CLIQUE to
VERTEX-COVER.
The reduction algorithm takes as input an instance hG;ki of the clique problem.
It computes the complement G, which we can easily do in polynomial time. The
output of the reduction algorithm is the instance hG; jV j  ki of the vertex-cover
problem. To complete the proof, we show that this transformation is indeed a

## 34.5 NP-complete problems

reduction: the graph G has a clique of size k if and only if the graph G has a vertex
cover of size jV j  k.
Suppose that G has a clique V 0  V with jV 0j D k. We claim that V  V 0 is a
vertex cover in G. Let .u; / be any edge in E. Then, .u; / 62 E, which implies
that at least one of u or  does not belong to V 0, since every pair of vertices in V 0 is
connected by an edge of E. Equivalently, at least one of u or  is in V  V 0, which
means that edge .u; / is covered by V  V 0. Since .u; / was chosen arbitrarily
from E, every edge of E is covered by a vertex in V  V 0. Hence, the set V  V 0,
which has size jV j  k, forms a vertex cover for G.
Conversely, suppose that G has a vertex cover V 0  V , where jV 0j D jV j  k.
Then, for all u;  2 V , if .u; / 2 E, then u 2 V 0 or  2 V 0 or both. The
contrapositive of this implication is that for all u;  2 V , if u 62 V 0 and  62 V 0,
then .u; / 2 E. In other words, V V 0 is a clique, and it has size jV jjV 0j D k.
Since VERTEX-COVER is NP-complete, we don’t expect to ﬁnd a polynomialtime algorithm for ﬁnding a minimum-size vertex cover. Section 35.1 presents a
polynomial-time “approximation algorithm,” however, which produces “approximate” solutions for the vertex-cover problem. The size of a vertex cover produced
by the algorithm is at most twice the minimum size of a vertex cover.
Thus, we shouldn’t give up hope just because a problem is NP-complete. We
may be able to design a polynomial-time approximation algorithm that obtains
near-optimal solutions, even though ﬁnding an optimal solution is NP-complete.
Chapter 35 gives several approximation algorithms for NP-complete problems.

## 34.5.3 The hamiltonian-cycle problem

We now return to the hamiltonian-cycle problem deﬁned in Section 34.2.

> **Theorem 34.13**

The hamiltonian cycle problem is NP-complete.
Proof
We ﬁrst show that HAM-CYCLE belongs to NP. Given a graph G D
.V; E/, our certiﬁcate is the sequence of jV j vertices that makes up the hamiltonian
cycle. The veriﬁcation algorithm checks that this sequence contains each vertex
in V exactly once and that with the ﬁrst vertex repeated at the end, it forms a cycle
in G. That is, it checks that there is an edge between each pair of consecutive
vertices and between the ﬁrst and last vertices. We can verify the certiﬁcate in
polynomial time.
We now prove that VERTEX-COVER P HAM-CYCLE, which shows that
HAM-CYCLE is NP-complete. Given an undirected graph G D .V; E/ and an

[u,v,1]
[u,v,2]
[u,v,3]
[u,v,4]
[u,v,5]
[u,v,6]
[v,u,1]
[v,u,2]
[v,u,3]
[v,u,4]
[v,u,5]
[v,u,6]
Wuv
(a)
Wuv
(b)
[u,v,1]
[u,v,6]
[v,u,1]
[v,u,6]
Wuv
(c)
[u,v,1]
[u,v,6]
[v,u,1]
[v,u,6]
Wuv
(d)
[u,v,1]
[u,v,6]
[v,u,1]
[v,u,6]
Figure 34.16
The widget used in reducing the vertex-cover problem to the hamiltonian-cycle problem. An edge .u; / of graph G corresponds to widget Wu in the graph G0 created in the reduction.
(a) The widget, with individual vertices labeled. (b)–(d) The shaded paths are the only possible ones
through the widget that include all vertices, assuming that the only connections from the widget to
the remainder of G0 are through vertices Œu; ; 1, Œu; ; 6, Œ; u; 1, and Œ; u; 6.
integer k, we construct an undirected graph G0 D .V 0; E0/ that has a hamiltonian
cycle if and only if G has a vertex cover of size k.
Our construction uses a widget, which is a piece of a graph that enforces certain
properties. Figure 34.16(a) shows the widget we use. For each edge .u; / 2 E, the
graph G0 that we construct will contain one copy of this widget, which we denote
by Wu. We denote each vertex in Wu by Œu; ; i or Œ; u; i, where 1  i  6, so
that each widget Wu contains 12 vertices. Widget Wu also contains the 14 edges
shown in Figure 34.16(a).
Along with the internal structure of the widget, we enforce the properties we
want by limiting the connections between the widget and the remainder of the
graph G0 that we construct. In particular, only vertices Œu; ; 1, Œu; ; 6, Œ; u; 1,
and Œ; u; 6 will have edges incident from outside Wu. Any hamiltonian cycle
of G0 must traverse the edges of Wu in one of the three ways shown in Figures 34.16(b)–(d). If the cycle enters through vertex Œu; ; 1, it must exit through
vertex Œu; ; 6, and it either visits all 12 of the widget’s vertices (Figure 34.16(b))
or the six vertices Œu; ; 1 through Œu; ; 6 (Figure 34.16(c)). In the latter case,
the cycle will have to reenter the widget to visit vertices Œ; u; 1 through Œ; u; 6.
Similarly, if the cycle enters through vertex Œ; u; 1, it must exit through vertex Œ; u; 6, and it either visits all 12 of the widget’s vertices (Figure 34.16(d)) or
the six vertices Œ; u; 1 through Œ; u; 6 (Figure 34.16(c)). No other paths through
the widget that visit all 12 vertices are possible. In particular, it is impossible to
construct two vertex-disjoint paths, one of which connects Œu; ; 1 to Œ; u; 6 and
the other of which connects Œ; u; 1 to Œu; ; 6, such that the union of the two paths
contains all of the widget’s vertices.

## 34.5 NP-complete problems

[w,x,1]
[w,x,6]
[x,w,1]
[x,w,6]
Wwx
(b)
[x,y,1]
[x,y,6]
[y,x,1]
[y,x,6]
Wxy
[w,y,1]
[w,y,6]
[y,w,1]
[y,w,6]
Wwy
[w,z,1]
[w,z,6]
[z,w,1]
[z,w,6]
Wwz
s1
s2
w
x
z
y
(a)
Figure 34.17
Reducing an instance of the vertex-cover problem to an instance of the hamiltoniancycle problem. (a) An undirected graph G with a vertex cover of size 2, consisting of the lightly
shaded vertices w and y. (b) The undirected graph G0 produced by the reduction, with the hamiltonian path corresponding to the vertex cover shaded. The vertex cover fw; yg corresponds to edges
.s1; Œw; x; 1/ and .s2; Œy; x; 1/ appearing in the hamiltonian cycle.
The only other vertices in V 0 other than those of widgets are selector vertices
s1; s2; : : : ; sk. We use edges incident on selector vertices in G0 to select the k
vertices of the cover in G.
In addition to the edges in widgets, E0 contains two other types of edges, which
Figure 34.17 shows. First, for each vertex u 2 V , we add edges to join pairs
of widgets in order to form a path containing all widgets corresponding to edges
incident on u in G.
We arbitrarily order the vertices adjacent to each vertex
u 2 V as u.1/; u.2/; : : : ; u.degree.u//, where degree.u/ is the number of vertices
adjacent to u.
We create a path in G0 through all the widgets corresponding
to edges incident on u by adding to E0 the edges f.Œu; u.i/; 6; Œu; u.iC1/; 1/ W
1  i  degree.u/  1g. In Figure 34.17, for example, we order the vertices adjacent to w as x; y; ´, and so graph G0 in part (b) of the ﬁgure includes the edges

.Œw; x; 6; Œw; y; 1/ and .Œw; y; 6; Œw; ´; 1/. For each vertex u 2 V , these edges
in G0 ﬁll in a path containing all widgets corresponding to edges incident on u
in G.
The intuition behind these edges is that if we choose a vertex u 2 V in the vertex
cover of G, we can construct a path from Œu; u.1/; 1 to Œu; u.degree.u//; 6 in G0 that
“covers” all widgets corresponding to edges incident on u. That is, for each of these
widgets, say Wu;u.i/, the path either includes all 12 vertices (if u is in the vertex
cover but u.i/ is not) or just the six vertices Œu; u.i/; 1; Œu; u.i/; 2; : : : ; Œu; u.i/; 6 (if
both u and u.i/ are in the vertex cover).
The ﬁnal type of edge in E0 joins the ﬁrst vertex Œu; u.1/; 1 and the last vertex
Œu; u.degree.u//; 6 of each of these paths to each of the selector vertices. That is, we
include the edges
f.sj; Œu; u.1/; 1/ W u 2 V and 1  j  kg
[ f.sj; Œu; u.degree.u//; 6/ W u 2 V and 1  j  kg :
Next, we show that the size of G0 is polynomial in the size of G, and hence we
can construct G0 in time polynomial in the size of G. The vertices of G0 are those
in the widgets, plus the selector vertices. With 12 vertices per widget, plus k  jV j
selector vertices, we have a total of
jV 0j
D
12 jEj C k

12 jEj C jV j
vertices. The edges of G0 are those in the widgets, those that go between widgets,
and those connecting selector vertices to widgets. Each widget contains 14 edges,
totaling 14 jEj in all widgets. For each vertex u 2 V , graph G0 has degree.u/  1
edges going between widgets, so that summed over all vertices in V ,
X
u2V
.degree.u/  1/ D 2 jEj  jV j
edges go between widgets. Finally, G0 has two edges for each pair consisting of a
selector vertex and a vertex of V , totaling 2k jV j such edges. The total number of
edges of G0 is therefore
jE0j
D
.14 jEj/ C .2 jEj  jV j/ C .2k jV j/
D
16 jEj C .2k  1/ jV j

16 jEj C .2 jV j  1/ jV j :
Now we show that the transformation from graph G to G0 is a reduction. That is,
we must show that G has a vertex cover of size k if and only if G0 has a hamiltonian
cycle.

## 34.5 NP-complete problems

Suppose that G D .V; E/ has a vertex cover V   V of size k.
Let
V  D fu1; u2; : : : ; ukg.
As Figure 34.17 shows, we form a hamiltonian cycle in G0 by including the following edges10 for each vertex uj 2 V . Include
edges
˚
.Œuj; u.i/
j ; 6; Œuj ; u.iC1/
j
; 1/ W 1  i  degree.uj/  1

, which connect all
widgets corresponding to edges incident on uj. We also include the edges within
these widgets as Figures 34.16(b)–(d) show, depending on whether the edge is covered by one or two vertices in V . The hamiltonian cycle also includes the edges
f.sj; Œuj; u.1/
j ; 1/ W 1  j  kg
[ f.sjC1; Œuj; u
.degree.uj //
j
; 6/ W 1  j  k  1g
[ f.s1; Œuk; u.degree.uk//
k
; 6/g :
By inspecting Figure 34.17, you can verify that these edges form a cycle. The cycle
starts at s1, visits all widgets corresponding to edges incident on u1, then visits s2,
visits all widgets corresponding to edges incident on u2, and so on, until it returns
to s1. The cycle visits each widget either once or twice, depending on whether one
or two vertices of V  cover its corresponding edge. Because V  is a vertex cover
for G, each edge in E is incident on some vertex in V , and so the cycle visits each
vertex in each widget of G0. Because the cycle also visits every selector vertex, it
is hamiltonian.
Conversely, suppose that G0 D .V 0; E0/ has a hamiltonian cycle C  E0. We
claim that the set
V  D fu 2 V W .sj; Œu; u.1/; 1/ 2 C for some 1  j  kg
(34.4)
is a vertex cover for G. To see why, partition C into maximal paths that start at
some selector vertex si, traverse an edge .si; Œu; u.1/; 1/ for some u 2 V , and end
at a selector vertex sj without passing through any other selector vertex. Let us call
each such path a “cover path.” From how G0 is constructed, each cover path must
start at some si, take the edge .si; Œu; u.1/; 1/ for some vertex u 2 V , pass through
all the widgets corresponding to edges in E incident on u, and then end at some
selector vertex sj. We refer to this cover path as pu, and by equation (34.4), we
put u into V . Each widget visited by pu must be Wu or Wu for some  2 V .
For each widget visited by pu, its vertices are visited by either one or two cover
paths. If they are visited by one cover path, then edge .u; / 2 E is covered in G
by vertex u. If two cover paths visit the widget, then the other cover path must
be p, which implies that  2 V , and edge .u; / 2 E is covered by both u and .
10Technically, we deﬁne a cycle in terms of vertices rather than edges (see Section B.4). In the
interest of clarity, we abuse notation here and deﬁne the hamiltonian cycle in terms of edges.

u
v
x
w
Figure 34.18
An instance of the traveling-salesman problem. Shaded edges represent a minimumcost tour, with cost 7.
Because each vertex in each widget is visited by some cover path, we see that each
edge in E is covered by some vertex in V .

## 34.5.4 The traveling-salesman problem

In the traveling-salesman problem, which is closely related to the hamiltoniancycle problem, a salesman must visit n cities. Modeling the problem as a complete
graph with n vertices, we can say that the salesman wishes to make a tour, or
hamiltonian cycle, visiting each city exactly once and ﬁnishing at the city he starts
from. The salesman incurs a nonnegative integer cost c.i; j / to travel from city i
to city j , and the salesman wishes to make the tour whose total cost is minimum,
where the total cost is the sum of the individual costs along the edges of the tour.
For example, in Figure 34.18, a minimum-cost tour is hu; w; ; x; ui, with cost 7.
The formal language for the corresponding decision problem is
TSP D fhG; c; ki W G D .V; E/ is a complete graph;
c is a function from V 	 V ! Z;
k 2 Z, and
G has a traveling-salesman tour with cost at most kg :
The following theorem shows that a fast algorithm for the traveling-salesman
problem is unlikely to exist.

> **Theorem 34.14**

The traveling-salesman problem is NP-complete.
Proof
We ﬁrst show that TSP belongs to NP. Given an instance of the problem,
we use as a certiﬁcate the sequence of n vertices in the tour. The veriﬁcation
algorithm checks that this sequence contains each vertex exactly once, sums up the
edge costs, and checks whether the sum is at most k. This process can certainly be
done in polynomial time.

## 34.5 NP-complete problems

To prove that TSP is NP-hard, we show that HAM-CYCLE P TSP.
Let
G D .V; E/ be an instance of HAM-CYCLE. We construct an instance of TSP as
follows. We form the complete graph G0 D .V; E0/, where E0 D f.i; j / W i; j 2 V
and i ¤ j g, and we deﬁne the cost function c by
c.i; j / D
(
if .i; j / 2 E ;
if .i; j / 62 E :
(Note that because G is undirected, it has no self-loops, and so c.; / D 1 for all
vertices  2 V .) The instance of TSP is then hG0; c; 0i, which we can easily create
in polynomial time.
We now show that graph G has a hamiltonian cycle if and only if graph G0 has a
tour of cost at most 0. Suppose that graph G has a hamiltonian cycle h. Each edge
in h belongs to E and thus has cost 0 in G0. Thus, h is a tour in G0 with cost 0.
Conversely, suppose that graph G0 has a tour h0 of cost at most 0. Since the costs
of the edges in E0 are 0 and 1, the cost of tour h0 is exactly 0 and each edge on the
tour must have cost 0. Therefore, h0 contains only edges in E. We conclude that h0
is a hamiltonian cycle in graph G.

## 34.5.5 The subset-sum problem

We next consider an arithmetic NP-complete problem. In the subset-sum problem,
we are given a ﬁnite set S of positive integers and an integer target t > 0. We ask
whether there exists a subset S 0  S whose elements sum to t. For example,
if S D f1; 2; 7; 14; 49; 98; 343; 686; 2409; 2793; 16808; 17206; 117705; 117993g
and t D 138457, then the subset S 0 D f1; 2; 7; 98; 343; 686; 2409; 17206; 117705g
is a solution.
As usual, we deﬁne the problem as a language:
SUBSET-SUM D fhS; ti W there exists a subset S 0  S such that t D P
s2S0 sg :
As with any arithmetic problem, it is important to recall that our standard encoding
assumes that the input integers are coded in binary. With this assumption in mind,
we can show that the subset-sum problem is unlikely to have a fast algorithm.

> **Theorem 34.15**

The subset-sum problem is NP-complete.
Proof
To show that SUBSET-SUM is in NP, for an instance hS;ti of the problem,
we let the subset S 0 be the certiﬁcate. A veriﬁcation algorithm can check whether
t D P
s2S0 s in polynomial time.
We now show that 3-CNF-SAT P SUBSET-SUM. Given a 3-CNF formula 
over variables x1; x2; : : : ; xn with clauses C1; C2; : : : ; Ck, each containing exactly

three distinct literals, the reduction algorithm constructs an instance hS; ti of the
subset-sum problem such that  is satisﬁable if and only if there exists a subset
of S whose sum is exactly t. Without loss of generality, we make two simplifying
assumptions about the formula . First, no clause contains both a variable and its
negation, for such a clause is automatically satisﬁed by any assignment of values
to the variables. Second, each variable appears in at least one clause, because it
does not matter what value is assigned to a variable that appears in no clauses.
The reduction creates two numbers in set S for each variable xi and two numbers
in S for each clause Cj. We shall create numbers in base 10, where each number
contains nCk digits and each digit corresponds to either one variable or one clause.
Base 10 (and other bases, as we shall see) has the property we need of preventing
carries from lower digits to higher digits.
As Figure 34.19 shows, we construct set S and target t as follows. We label
each digit position by either a variable or a clause. The least signiﬁcant k digits are
labeled by the clauses, and the most signiﬁcant n digits are labeled by variables.

The target t has a 1 in each digit labeled by a variable and a 4 in each digit
labeled by a clause.

For each variable xi, set S contains two integers i and 0
i. Each of i and 0
i
has a 1 in the digit labeled by xi and 0s in the other variable digits. If literal xi
appears in clause Cj, then the digit labeled by Cj in i contains a 1. If literal :xi appears in clause Cj, then the digit labeled by Cj in 0
i contains a 1.
All other digits labeled by clauses in i and 0
i are 0.
All i and 0
i values in set S are unique. Why? For l ¤ i, no l or 0
l values can
equal i and 0
i in the most signiﬁcant n digits. Furthermore, by our simplifying
assumptions above, no i and 0
i can be equal in all k least signiﬁcant digits.
If i and 0
i were equal, then xi and :xi would have to appear in exactly the
same set of clauses. But we assume that no clause contains both xi and :xi
and that either xi or :xi appears in some clause, and so there must be some
clause Cj for which i and 0
i differ.

For each clause Cj, set S contains two integers sj and s0
j. Each of sj and s0
j has
0s in all digits other than the one labeled by Cj. For sj, there is a 1 in the Cj
digit, and s0
j has a 2 in this digit. These integers are “slack variables,” which we
use to get each clause-labeled digit position to add to the target value of 4.
Simple inspection of Figure 34.19 demonstrates that all sj and s0
j values in S
are unique in set S.
Note that the greatest sum of digits in any one digit position is 6, which occurs in
the digits labeled by clauses (three 1s from the i and 0
i values, plus 1 and 2 from

## 34.5 NP-complete problems

=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
x1
x2
x3
C1
C2
C3
C4
1
0
2
0
3
0
s1
s0
s2
s0
s3
s0
s4
s0
t
Figure 34.19
The reduction of 3-CNF-SAT to SUBSET-SUM. The formula in 3-CNF is  D
C1^C2^C3^C4, where C1 D .x1_:x2_:x3/, C2 D .:x1_:x2_:x3/, C3 D .:x1_:x2_x3/,
and C4 D .x1 _ x2 _ x3/. A satisfying assignment of  is hx1 D 0; x2 D 0; x3 D 1i. The set S
produced by the reduction consists of the base-10 numbers shown; reading from top to bottom, S D
f1001001; 1000110; 100001; 101110; 10011; 11100; 1000; 2000; 100; 200; 10; 20; 1; 2g. The target t
is 1114444. The subset S0  S is lightly shaded, and it contains 0
1, 0
2, and 3, corresponding to the
satisfying assignment. It also contains slack variables s1, s0
1, s0
2, s3, s4, and s0
4 to achieve the target
value of 4 in the digits labeled by C1 through C4.
the sj and s0
j values). Interpreting these numbers in base 10, therefore, no carries
can occur from lower digits to higher digits.11
We can perform the reduction in polynomial time. The set S contains 2n C 2k
values, each of which has n C k digits, and the time to produce each digit is polynomial in n C k. The target t has n C k digits, and the reduction produces each in
constant time.
We now show that the 3-CNF formula  is satisﬁable if and only if there exists
a subset S 0  S whose sum is t. First, suppose that  has a satisfying assignment.
For i D 1; 2; : : : ; n, if xi D 1 in this assignment, then include i in S 0. Otherwise,
include 0
i. In other words, we include in S 0 exactly the i and 0
i values that cor11In fact, any base b, where b  7, would work. The instance at the beginning of this subsection is
the set S and target t in Figure 34.19 interpreted in base 7, with S listed in sorted order.

respond to literals with the value 1 in the satisfying assignment. Having included
either i or 0
i, but not both, for all i, and having put 0 in the digits labeled by
variables in all sj and s0
j , we see that for each variable-labeled digit, the sum of the
values of S 0 must be 1, which matches those digits of the target t. Because each
clause is satisﬁed, the clause contains some literal with the value 1. Therefore,
each digit labeled by a clause has at least one 1 contributed to its sum by a i or 0
i
value in S 0. In fact, 1, 2, or 3 literals may be 1 in each clause, and so each clauselabeled digit has a sum of 1, 2, or 3 from the i and 0
i values in S 0. In Figure 34.19
for example, literals :x1, :x2, and x3 have the value 1 in a satisfying assignment.
Each of clauses C1 and C4 contains exactly one of these literals, and so together 0
1,
0
2, and 3 contribute 1 to the sum in the digits for C1 and C4. Clause C2 contains
two of these literals, and 0
1, 0
2, and 3 contribute 2 to the sum in the digit for C2.
Clause C3 contains all three of these literals, and 0
1, 0
2, and 3 contribute 3 to the
sum in the digit for C3. We achieve the target of 4 in each digit labeled by clause Cj
by including in S 0 the appropriate nonempty subset of slack variables fsj; s0
j g. In
Figure 34.19, S 0 includes s1, s0
1, s0
2, s3, s4, and s0
4. Since we have matched the target
in all digits of the sum, and no carries can occur, the values of S 0 sum to t.
Now, suppose that there is a subset S 0  S that sums to t. The subset S 0 must
include exactly one of i and 0
i for each i D 1; 2; : : : ; n, for otherwise the digits
labeled by variables would not sum to 1. If i 2 S 0, we set xi D 1. Otherwise,
0
i 2 S 0, and we set xi D 0. We claim that every clause Cj, for j D 1; 2; : : : ; k, is
satisﬁed by this assignment. To prove this claim, note that to achieve a sum of 4 in
the digit labeled by Cj, the subset S 0 must include at least one i or 0
i value that
has a 1 in the digit labeled by Cj, since the contributions of the slack variables sj
and s0
j together sum to at most 3. If S 0 includes a i that has a 1 in Cj’s position,
then the literal xi appears in clause Cj. Since we have set xi D 1 when i 2 S 0,
clause Cj is satisﬁed. If S 0 includes a 0
i that has a 1 in that position, then the
literal :xi appears in Cj. Since we have set xi D 0 when 0
i 2 S 0, clause Cj is
again satisﬁed. Thus, all clauses of  are satisﬁed, which completes the proof.

## Exercises

34.5-1
The subgraph-isomorphism problem takes two undirected graphs G1 and G2, and
it asks whether G1 is isomorphic to a subgraph of G2. Show that the subgraphisomorphism problem is NP-complete.
34.5-2
Given an integer m 	 n matrix A and an integer m-vector b, the 0-1 integerprogramming problem asks whether there exists an integer n-vector x with eleProblems for Chapter 34
ments in the set f0; 1g such that Ax  b. Prove that 0-1 integer programming is
NP-complete. (Hint: Reduce from 3-CNF-SAT.)
34.5-3
The integer linear-programming problem is like the 0-1 integer-programming
problem given in Exercise 34.5-2, except that the values of the vector x may be
any integers rather than just 0 or 1. Assuming that the 0-1 integer-programming
problem is NP-hard, show that the integer linear-programming problem is NPcomplete.
34.5-4
Show how to solve the subset-sum problem in polynomial time if the target value t
is expressed in unary.
34.5-5
The set-partition problem takes as input a set S of numbers. The question is
whether the numbers can be partitioned into two sets A and A D S  A such
that P
x2A x D P
x2A x. Show that the set-partition problem is NP-complete.
34.5-6
Show that the hamiltonian-path problem is NP-complete.
34.5-7
The longest-simple-cycle problem is the problem of determining a simple cycle
(no repeated vertices) of maximum length in a graph. Formulate a related decision
problem, and show that the decision problem is NP-complete.
34.5-8
In the half 3-CNF satisﬁability problem, we are given a 3-CNF formula  with n
variables and m clauses, where m is even. We wish to determine whether there
exists a truth assignment to the variables of  such that exactly half the clauses
evaluate to 0 and exactly half the clauses evaluate to 1. Prove that the half 3-CNF
satisﬁability problem is NP-complete.

## Problems

34-1
Independent set
An independent set of a graph G D .V; E/ is a subset V 0  V of vertices such
that each edge in E is incident on at most one vertex in V 0. The independent-set
problem is to ﬁnd a maximum-size independent set in G.

a. Formulate a related decision problem for the independent-set problem, and
prove that it is NP-complete. (Hint: Reduce from the clique problem.)
b. Suppose that you are given a “black-box” subroutine to solve the decision problem you deﬁned in part (a). Give an algorithm to ﬁnd an independent set of maximum size. The running time of your algorithm should be polynomial in jV j
and jEj, counting queries to the black box as a single step.
Although the independent-set decision problem is NP-complete, certain special
cases are polynomial-time solvable.
c. Give an efﬁcient algorithm to solve the independent-set problem when each vertex in G has degree 2. Analyze the running time, and prove that your algorithm
works correctly.
d. Give an efﬁcient algorithm to solve the independent-set problem when G is
bipartite. Analyze the running time, and prove that your algorithm works correctly. (Hint: Use the results of Section 26.3.)
34-2
Bonnie and Clyde
Bonnie and Clyde have just robbed a bank. They have a bag of money and want
to divide it up. For each of the following scenarios, either give a polynomial-time
algorithm, or prove that the problem is NP-complete. The input in each case is a
list of the n items in the bag, along with the value of each.
a. The bag contains n coins, but only 2 different denominations: some coins are
worth x dollars, and some are worth y dollars. Bonnie and Clyde wish to divide
the money exactly evenly.
b. The bag contains n coins, with an arbitrary number of different denominations,
but each denomination is a nonnegative integer power of 2, i.e., the possible
denominations are 1 dollar, 2 dollars, 4 dollars, etc. Bonnie and Clyde wish to
divide the money exactly evenly.
c. The bag contains n checks, which are, in an amazing coincidence, made out to
“Bonnie or Clyde.” They wish to divide the checks so that they each get the
exact same amount of money.
d. The bag contains n checks as in part (c), but this time Bonnie and Clyde are
willing to accept a split in which the difference is no larger than 100 dollars.

Problems for Chapter 34
34-3
Graph coloring
Mapmakers try to use as few colors as possible when coloring countries on a map,
as long as no two countries that share a border have the same color. We can model
this problem with an undirected graph G D .V; E/ in which each vertex represents a country and vertices whose respective countries share a border are adjacent.
Then, a k-coloring is a function c W V ! f1; 2; : : : ; kg such that c.u/ ¤ c./ for
every edge .u; / 2 E. In other words, the numbers 1; 2; : : : ; k represent the k colors, and adjacent vertices must have different colors. The graph-coloring problem
is to determine the minimum number of colors needed to color a given graph.
a. Give an efﬁcient algorithm to determine a 2-coloring of a graph, if one exists.
b. Cast the graph-coloring problem as a decision problem. Show that your decision problem is solvable in polynomial time if and only if the graph-coloring
problem is solvable in polynomial time.
c. Let the language 3-COLOR be the set of graphs that can be 3-colored. Show
that if 3-COLOR is NP-complete, then your decision problem from part (b) is
NP-complete.
To prove that 3-COLOR is NP-complete, we use a reduction from 3-CNF-SAT.
Given a formula  of m clauses on n variables x1, x2, . . . , xn, we construct a graph
G D .V; E/ as follows. The set V consists of a vertex for each variable, a vertex
for the negation of each variable, 5 vertices for each clause, and 3 special vertices:
TRUE, FALSE, and RED. The edges of the graph are of two types: “literal” edges
that are independent of the clauses and “clause” edges that depend on the clauses.
The literal edges form a triangle on the special vertices and also form a triangle on
xi, :xi, and RED for i D 1; 2; : : : ; n.
d. Argue that in any 3-coloring c of a graph containing the literal edges, exactly
one of a variable and its negation is colored c.TRUE/ and the other is colored
c.FALSE/. Argue that for any truth assignment for , there exists a 3-coloring
of the graph containing just the literal edges.
The widget shown in Figure 34.20 helps to enforce the condition corresponding to
a clause .x _ y _ ´/. Each clause requires a unique copy of the 5 vertices that are
heavily shaded in the ﬁgure; they connect as shown to the literals of the clause and
the special vertex TRUE.
e. Argue that if each of x, y, and ´ is colored c.TRUE/ or c.FALSE/, then the
widget is 3-colorable if and only if at least one of x, y, or ´ is colored c.TRUE/.
f. Complete the proof that 3-COLOR is NP-complete.

x
y
z
TRUE
Figure 34.20
The widget corresponding to a clause .x _ y _ ´/, used in Problem 34-3.
34-4
Scheduling with proﬁts and deadlines
Suppose that we have one machine and a set of n tasks a1; a2; : : : ; an, each of
which requires time on the machine. Each task aj requires tj time units on the
machine (its processing time), yields a proﬁt of pj, and has a deadline dj. The
machine can process only one task at a time, and task aj must run without interruption for tj consecutive time units. If we complete task aj by its deadline dj, we
receive a proﬁt pj, but if we complete it after its deadline, we receive no proﬁt. As
an optimization problem, we are given the processing times, proﬁts, and deadlines
for a set of n tasks, and we wish to ﬁnd a schedule that completes all the tasks and
returns the greatest amount of proﬁt. The processing times, proﬁts, and deadlines
are all nonnegative numbers.
a. State this problem as a decision problem.
b. Show that the decision problem is NP-complete.
c. Give a polynomial-time algorithm for the decision problem, assuming that all
processing times are integers from 1 to n. (Hint: Use dynamic programming.)
d. Give a polynomial-time algorithm for the optimization problem, assuming that
all processing times are integers from 1 to n.
Chapter notes
The book by Garey and Johnson [129] provides a wonderful guide to NP-completeness, discussing the theory at length and providing a catalogue of many problems
that were known to be NP-complete in 1979. The proof of Theorem 34.13 is
adapted from their book, and the list of NP-complete problem domains at the beginning of Section 34.5 is drawn from their table of contents. Johnson wrote a series

Notes for Chapter 34
of 23 columns in the Journal of Algorithms between 1981 and 1992 reporting new
developments in NP-completeness. Hopcroft, Motwani, and Ullman [177], Lewis
and Papadimitriou [236], Papadimitriou [270], and Sipser [317] have good treatments of NP-completeness in the context of complexity theory. NP-completeness
and several reductions also appear in books by Aho, Hopcroft, and Ullman [5];
Dasgupta, Papadimitriou, and Vazirani [82]; Johnsonbaugh and Schaefer [193];
and Kleinberg and Tardos [208].
The class P was introduced in 1964 by Cobham [72] and, independently, in 1965
by Edmonds [100], who also introduced the class NP and conjectured that P ¤ NP.
The notion of NP-completeness was proposed in 1971 by Cook [75], who gave
the ﬁrst NP-completeness proofs for formula satisﬁability and 3-CNF satisﬁability. Levin [234] independently discovered the notion, giving an NP-completeness
proof for a tiling problem. Karp [199] introduced the methodology of reductions
in 1972 and demonstrated the rich variety of NP-complete problems. Karp’s paper included the original NP-completeness proofs of the clique, vertex-cover, and
hamiltonian-cycle problems. Since then, thousands of problems have been proven
to be NP-complete by many researchers. In a talk at a meeting celebrating Karp’s
60th birthday in 1995, Papadimitriou remarked, “about 6000 papers each year have
the term ‘NP-complete’ on their title, abstract, or list of keywords. This is more
than each of the terms ‘compiler,’ ‘database,’ ‘expert,’ ‘neural network,’ or ‘operating system.’ ”
Recent work in complexity theory has shed light on the complexity of computing
approximate solutions. This work gives a new deﬁnition of NP using “probabilistically checkable proofs.” This new deﬁnition implies that for problems such as
clique, vertex cover, the traveling-salesman problem with the triangle inequality,
and many others, computing good approximate solutions is NP-hard and hence no
easier than computing optimal solutions. An introduction to this area can be found
in Arora’s thesis [20]; a chapter by Arora and Lund in Hochbaum [172]; a survey
article by Arora [21]; a book edited by Mayr, Pr¨omel, and Steger [246]; and a
survey article by Johnson [191].
