# 32 String Matching

32
String Matching
Text-editing programs frequently need to ﬁnd all occurrences of a pattern in the
text. Typically, the text is a document being edited, and the pattern searched for is a
particular word supplied by the user. Efﬁcient algorithms for this problem—called
“string matching”—can greatly aid the responsiveness of the text-editing program.
Among their many other applications, string-matching algorithms search for par-
ticular patterns in DNA sequences. Internet search engines also use them to ﬁnd
Web pages relevant to queries.
We formalize the string-matching problem as follows.
We assume that the
text is an array T Œ1 : : n of length n and that the pattern is an array P Œ1 : : m
of length m  n. We further assume that the elements of P and T are char-
acters drawn from a ﬁnite alphabet †. For example, we may have † D f0,1g
or † D fa; b; : : : ; zg. The character arrays P and T are often called strings of
characters.
Referring to Figure 32.1, we say that pattern P occurs with shift s in text T
(or, equivalently, that pattern P occurs beginning at position s C 1 in text T ) if
0  s  n  m and T Œs C 1 : : s C m D P Œ1 : : m (that is, if T Œs C j  D P Œj , for
1  j  m). If P occurs with shift s in T , then we call s a valid shift; otherwise,
we call s an invalid shift. The string-matching problem is the problem of ﬁnding
all valid shifts with which a given pattern P occurs in a given text T .
a
b
c
a
b
a
a
b
c
a
b
a
c
a
b
a
a
pattern P
text T
s = 3
Figure 32.1
An example of the string-matching problem, where we want to ﬁnd all occurrences of
the pattern P D abaa in the text T D abcabaabcabac. The pattern occurs only once in the text,
at shift s D 3, which we call a valid shift. A vertical line connects each character of the pattern to its
matching character in the text, and all matched characters are shaded.

986
Chapter 32
String Matching
Algorithm
Preprocessing time
Matching time
Naive
0
O..n  m C 1/m/
Rabin-Karp
‚.m/
O..n  m C 1/m/
Finite automaton
O.m j†j/
‚.n/
Knuth-Morris-Pratt
‚.m/
‚.n/
Figure 32.2
The string-matching algorithms in this chapter and their preprocessing and matching
times.
Except for the naive brute-force algorithm, which we review in Section 32.1,
each string-matching algorithm in this chapter performs some preprocessing based
on the pattern and then ﬁnds all valid shifts; we call this latter phase “matching.”
Figure 32.2 shows the preprocessing and matching times for each of the algorithms
in this chapter. The total running time of each algorithm is the sum of the prepro-
cessing and matching times. Section 32.2 presents an interesting string-matching
algorithm, due to Rabin and Karp. Although the ‚..n  m C 1/m/ worst-case
running time of this algorithm is no better than that of the naive method, it works
much better on average and in practice. It also generalizes nicely to other pattern-
matching problems. Section 32.3 then describes a string-matching algorithm that
begins by constructing a ﬁnite automaton speciﬁcally designed to search for occur-
rences of the given pattern P in a text. This algorithm takes O.m j†j/ preprocess-
ing time, but only ‚.n/ matching time. Section 32.4 presents the similar, but much
cleverer, Knuth-Morris-Pratt (or KMP) algorithm; it has the same ‚.n/ matching
time, and it reduces the preprocessing time to only ‚.m/.
Notation and terminology
We denote by † (read “sigma-star”) the set of all ﬁnite-length strings formed
using characters from the alphabet †. In this chapter, we consider only ﬁnite-
length strings. The zero-length empty string, denoted ", also belongs to †. The
length of a string x is denoted jxj. The concatenation of two strings x and y,
denoted xy, has length jxj C jyj and consists of the characters from x followed by
the characters from y.
We say that a string w is a preﬁx of a string x, denoted w < x, if x D wy for
some string y 2 †. Note that if w < x, then jwj  jxj. Similarly, we say that a
string w is a sufﬁx of a string x, denoted w = x, if x D yw for some y 2 †. As
with a preﬁx, w = x implies jwj  jxj. For example, we have ab < abcca and
cca = abcca. The empty string " is both a sufﬁx and a preﬁx of every string. For
any strings x and y and any character a, we have x = y if and only if xa = ya.

Chapter 32
String Matching
987
x
z
x
y
y
(a)
x
z
x
y
y
(b)
x
z
x
y
y
(c)
Figure 32.3
A graphical proof of Lemma 32.1. We suppose that x = ´ and y = ´. The three parts
of the ﬁgure illustrate the three cases of the lemma. Vertical lines connect matching regions (shown
shaded) of the strings. (a) If jxj  jyj, then x = y. (b) If jxj  jyj, then y = x. (c) If jxj D jyj,
then x D y.
Also note that < and = are transitive relations. The following lemma will be useful
later.
Lemma 32.1 (Overlapping-sufﬁx lemma)
Suppose that x, y, and ´ are strings such that x = ´ and y = ´. If jxj  jyj,
then x = y. If jxj  jyj, then y = x. If jxj D jyj, then x D y.
Proof
See Figure 32.3 for a graphical proof.
For brevity of notation, we denote the k-character preﬁx P Œ1 : : k of the pattern
P Œ1 : : m by Pk. Thus, P0 D " and Pm D P D P Œ1 : : m. Similarly, we denote
the k-character preﬁx of the text T by Tk. Using this notation, we can state the
string-matching problem as that of ﬁnding all shifts s in the range 0  s  n  m
such that P = TsCm.
In our pseudocode, we allow two equal-length strings to be compared for equal-
ity as a primitive operation. If the strings are compared from left to right and the
comparison stops when a mismatch is discovered, we assume that the time taken
by such a test is a linear function of the number of matching characters discovered.
To be precise, the test “x == y” is assumed to take time ‚.t C 1/, where t is the
length of the longest string ´ such that ´ < x and ´ < y. (We write ‚.t C 1/
rather than ‚.t/ to handle the case in which t D 0; the ﬁrst characters compared
do not match, but it takes a positive amount of time to perform this comparison.)

988
Chapter 32
String Matching
32.1
The naive string-matching algorithm
The naive algorithm ﬁnds all valid shifts using a loop that checks the condition
P Œ1 : : m D T Œs C 1 : : s C m for each of the n  m C 1 possible values of s.
NAIVE-STRING-MATCHER.T; P /
1
n D T:length
2
m D P:length
3
for s D 0 to n  m
4
if P Œ1 : : m == T Œs C 1 : : s C m
5
print “Pattern occurs with shift” s
Figure 32.4 portrays the naive string-matching procedure as sliding a “template”
containing the pattern over the text, noting for which shifts all of the characters
on the template equal the corresponding characters in the text. The for loop of
lines 3–5 considers each possible shift explicitly. The test in line 4 determines
whether the current shift is valid; this test implicitly loops to check corresponding
character positions until all positions match successfully or a mismatch is found.
Line 5 prints out each valid shift s.
Procedure NAIVE-STRING-MATCHER takes time O..n  m C 1/m/, and this
bound is tight in the worst case. For example, consider the text string an (a string
of n a’s) and the pattern am. For each of the nmC1 possible values of the shift s,
the implicit loop on line 4 to compare corresponding characters must execute m
times to validate the shift. The worst-case running time is thus ‚..n  m C 1/m/,
which is ‚.n2/ if m D bn=2c. Because it requires no preprocessing, NAIVE-
STRING-MATCHER’s running time equals its matching time.
a
c
a
a
b
c
a
a
b
s = 0
(a)
a
c
a
a
b
c
a
a
b
s = 1
(b)
a
c
a
a
b
c
a
a
b
s = 2
(c)
a
c
a
a
b
c
a
a
b
s = 3
(d)
Figure 32.4
The operation of the naive string matcher for the pattern P D aab and the text
T D acaabc. We can imagine the pattern P as a template that we slide next to the text. (a)–(d) The
four successive alignments tried by the naive string matcher. In each part, vertical lines connect cor-
responding regions found to match (shown shaded), and a jagged line connects the ﬁrst mismatched
character found, if any. The algorithm ﬁnds one occurrence of the pattern, at shift s D 2, shown in
part (c).

32.1
The naive string-matching algorithm
989
As we shall see, NAIVE-STRING-MATCHER is not an optimal procedure for this
problem. Indeed, in this chapter we shall see that the Knuth-Morris-Pratt algorithm
is much better in the worst case. The naive string-matcher is inefﬁcient because
it entirely ignores information gained about the text for one value of s when it
considers other values of s. Such information can be quite valuable, however. For
example, if P D aaab and we ﬁnd that s D 0 is valid, then none of the shifts 1, 2,
or 3 are valid, since T Œ4 D b. In the following sections, we examine several ways
to make effective use of this sort of information.
Exercises
32.1-1
Show the comparisons the naive string matcher makes for the pattern P D 0001
in the text T D 000010001010001.
32.1-2
Suppose that all characters in the pattern P are different. Show how to accelerate
NAIVE-STRING-MATCHER to run in time O.n/ on an n-character text T .
32.1-3
Suppose that pattern P and text T are randomly chosen strings of length m and n,
respectively, from the d-ary alphabet †d D f0; 1; : : : ; d  1g, where d  2. Show
that the expected number of character-to-character comparisons made by the im-
plicit loop in line 4 of the naive algorithm is
.n  m C 1/1  d m
1  d 1  2.n  m C 1/
over all executions of this loop. (Assume that the naive algorithm stops comparing
characters for a given shift once it ﬁnds a mismatch or matches the entire pattern.)
Thus, for randomly chosen strings, the naive algorithm is quite efﬁcient.
32.1-4
Suppose we allow the pattern P to contain occurrences of a gap character } that
can match an arbitrary string of characters (even one of zero length). For example,
the pattern ab}ba}c occurs in the text cabccbacbacab as
c ab’
ab
cc’
}
ba’
ba
cba
“
}
c’
c
ab
and as
c ab’
ab
ccbac
—
}
ba’
ba ’
}
c’
c
ab :

990
Chapter 32
String Matching
Note that the gap character may occur an arbitrary number of times in the pattern
but not at all in the text. Give a polynomial-time algorithm to determine whether
such a pattern P occurs in a given text T , and analyze the running time of your
algorithm.
32.2
The Rabin-Karp algorithm
Rabin and Karp proposed a string-matching algorithm that performs well in prac-
tice and that also generalizes to other algorithms for related problems, such as
two-dimensional pattern matching. The Rabin-Karp algorithm uses ‚.m/ prepro-
cessing time, and its worst-case running time is ‚..nmC1/m/. Based on certain
assumptions, however, its average-case running time is better.
This algorithm makes use of elementary number-theoretic notions such as the
equivalence of two numbers modulo a third number. You might want to refer to
Section 31.1 for the relevant deﬁnitions.
For expository purposes, let us assume that † D f0; 1; 2; : : : ; 9g, so that each
character is a decimal digit. (In the general case, we can assume that each charac-
ter is a digit in radix-d notation, where d D j†j.) We can then view a string of k
consecutive characters as representing a length-k decimal number. The character
string 31415 thus corresponds to the decimal number 31,415. Because we inter-
pret the input characters as both graphical symbols and digits, we ﬁnd it convenient
in this section to denote them as we would digits, in our standard text font.
Given a pattern P Œ1 : : m, let p denote its corresponding decimal value. In a sim-
ilar manner, given a text T Œ1 : : n, let ts denote the decimal value of the length-m
substring T Œs C 1 : : s C m, for s D 0; 1; : : : ; n  m. Certainly, ts D p if and only
if T Œs C 1 : : s C m D P Œ1 : : m; thus, s is a valid shift if and only if ts D p. If we
could compute p in time ‚.m/ and all the ts values in a total of ‚.nmC1/ time,1
then we could determine all valid shifts s in time ‚.m/ C ‚.n  m C 1/ D ‚.n/
by comparing p with each of the ts values. (For the moment, let’s not worry about
the possibility that p and the ts values might be very large numbers.)
We can compute p in time ‚.m/ using Horner’s rule (see Section 30.1):
p D P Œm C 10 .P Œm  1 C 10.P Œm  2 C    C 10.P Œ2 C 10P Œ1/   // :
Similarly, we can compute t0 from T Œ1 : : m in time ‚.m/.
1We write ‚.n  m C 1/ instead of ‚.n  m/ because s takes on n  m C 1 different values. The
“C1” is signiﬁcant in an asymptotic sense because when m D n, computing the lone ts value takes
‚.1/ time, not ‚.0/ time.

32.2
The Rabin-Karp algorithm
991
To compute the remaining values t1; t2; : : : ; tnm in time ‚.n  m/, we observe
that we can compute tsC1 from ts in constant time, since
tsC1 D 10.ts  10m1T Œs C 1/ C T Œs C m C 1 :
(32.1)
Subtracting 10m1T Œs C 1 removes the high-order digit from ts, multiplying the
result by 10 shifts the number left by one digit position, and adding T Œs C m C 1
brings in the appropriate low-order digit. For example, if m D 5 and ts D 31415,
then we wish to remove the high-order digit T Œs C 1 D 3 and bring in the new
low-order digit (suppose it is T Œs C 5 C 1 D 2) to obtain
tsC1
D
10.31415  10000  3/ C 2
D
14152 :
If we precompute the constant 10m1 (which we can do in time O.lg m/ using the
techniques of Section 31.6, although for this application a straightforward O.m/-
time method sufﬁces), then each execution of equation (32.1) takes a constant num-
ber of arithmetic operations. Thus, we can compute p in time ‚.m/, and we can
compute all of t0; t1; : : : ; tnm in time ‚.n  m C 1/. Therefore, we can ﬁnd all
occurrences of the pattern P Œ1 : : m in the text T Œ1 : : n with ‚.m/ preprocessing
time and ‚.n  m C 1/ matching time.
Until now, we have intentionally overlooked one problem: p and ts may be
too large to work with conveniently. If P contains m characters, then we cannot
reasonably assume that each arithmetic operation on p (which is m digits long)
takes “constant time.” Fortunately, we can solve this problem easily, as Figure 32.5
shows: compute p and the ts values modulo a suitable modulus q. We can compute
p modulo q in ‚.m/ time and all the ts values modulo q in ‚.n  m C 1/ time.
If we choose the modulus q as a prime such that 10q just ﬁts within one computer
word, then we can perform all the necessary computations with single-precision
arithmetic. In general, with a d-ary alphabet f0; 1; : : : ; d  1g, we choose q so
that dq ﬁts within a computer word and adjust the recurrence equation (32.1) to
work modulo q, so that it becomes
tsC1 D .d.ts  T Œs C 1h/ C T Œs C m C 1/ mod q ;
(32.2)
where h  d m1 .mod q/ is the value of the digit “1” in the high-order position
of an m-digit text window.
The solution of working modulo q is not perfect, however: ts  p .mod q/
does not imply that ts D p. On the other hand, if ts 6 p .mod q/, then we
deﬁnitely have that ts ¤ p, so that shift s is invalid. We can thus use the test
ts  p .mod q/ as a fast heuristic test to rule out invalid shifts s. Any shift s for
which ts  p .mod q/ must be tested further to see whether s is really valid or
we just have a spurious hit. This additional test explicitly checks the condition

992
Chapter 32
String Matching
2
3
5
9
0
2
3
1
4
1
5
2
6
7
3
9
9
2
1
7
(a)
mod 13
2
3
5
9
0
2
3
1
4
1
5
2
6
7
3
9
9
2
1
7
(b)
mod 13
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
8
9
3 11 0
1
8
5
11
9 11
7
10
4
valid
match
spurious
hit
…
…
…
3
1
4
1
5
2
7
8
old
high-order
digit
new
low-order
digit
≡(31415 – 3·10000)·10 + 2  (mod 13) 
old
high-order
digit
new
low-order
digit
shift
≡(7 – 3·3)·10 + 2  (mod 13) 
≡8  (mod 13) 
(c)
14152
Figure 32.5
The Rabin-Karp algorithm. Each character is a decimal digit, and we compute values
modulo 13. (a) A text string. A window of length 5 is shown shaded. The numerical value of the
shaded number, computed modulo 13, yields the value 7. (b) The same text string with values com-
puted modulo 13 for each possible position of a length-5 window. Assuming the pattern P D 31415,
we look for windows whose value modulo 13 is 7, since 31415  7 .mod 13/. The algorithm ﬁnds
two such windows, shown shaded in the ﬁgure. The ﬁrst, beginning at text position 7, is indeed an
occurrence of the pattern, while the second, beginning at text position 13, is a spurious hit. (c) How
to compute the value for a window in constant time, given the value for the previous window. The
ﬁrst window has value 31415. Dropping the high-order digit 3, shifting left (multiplying by 10), and
then adding in the low-order digit 2 gives us the new value 14152. Because all computations are
performed modulo 13, the value for the ﬁrst window is 7, and the value for the new window is 8.

32.2
The Rabin-Karp algorithm
993
P Œ1 : : m D T Œs C 1 : : s C m. If q is large enough, then we hope that spurious
hits occur infrequently enough that the cost of the extra checking is low.
The following procedure makes these ideas precise. The inputs to the procedure
are the text T , the pattern P , the radix d to use (which is typically taken to be j†j),
and the prime q to use.
RABIN-KARP-MATCHER.T; P; d; q/
1
n D T:length
2
m D P:length
3
h D d m1 mod q
4
p D 0
5
t0 D 0
6
for i D 1 to m
// preprocessing
7
p D .dp C P Œi/ mod q
8
t0 D .dt0 C T Œi/ mod q
9
for s D 0 to n  m
// matching
10
if p == ts
11
if P Œ1 : : m == T Œs C 1 : : s C m
12
print “Pattern occurs with shift” s
13
if s < n  m
14
tsC1 D .d.ts  T Œs C 1h/ C T Œs C m C 1/ mod q
The procedure RABIN-KARP-MATCHER works as follows. All characters are
interpreted as radix-d digits. The subscripts on t are provided only for clarity; the
program works correctly if all the subscripts are dropped. Line 3 initializes h to the
value of the high-order digit position of an m-digit window. Lines 4–8 compute p
as the value of P Œ1 : : m mod q and t0 as the value of T Œ1 : : m mod q. The for
loop of lines 9–14 iterates through all possible shifts s, maintaining the following
invariant:
Whenever line 10 is executed, ts D T Œs C 1 : : s C m mod q.
If p D ts in line 10 (a “hit”), then line 11 checks to see whether P Œ1 : : m D
T Œs C1 : : s Cm in order to rule out the possibility of a spurious hit. Line 12 prints
out any valid shifts that are found. If s < n  m (checked in line 13), then the for
loop will execute at least one more time, and so line 14 ﬁrst executes to ensure that
the loop invariant holds when we get back to line 10. Line 14 computes the value
of tsC1 mod q from the value of ts mod q in constant time using equation (32.2)
directly.
RABIN-KARP-MATCHER takes ‚.m/ preprocessing time, and its matching time
is ‚..n  m C 1/m/ in the worst case, since (like the naive string-matching algo-
rithm) the Rabin-Karp algorithm explicitly veriﬁes every valid shift. If P D am

994
Chapter 32
String Matching
and T D an, then verifying takes time ‚..nmC1/m/, since each of the nmC1
possible shifts is valid.
In many applications, we expect few valid shifts—perhaps some constant c of
them. In such applications, the expected matching time of the algorithm is only
O..n  m C 1/ C cm/ D O.n C m/, plus the time required to process spurious
hits. We can base a heuristic analysis on the assumption that reducing values mod-
ulo q acts like a random mapping from † to Zq. (See the discussion on the use of
division for hashing in Section 11.3.1. It is difﬁcult to formalize and prove such an
assumption, although one viable approach is to assume that q is chosen randomly
from integers of the appropriate size. We shall not pursue this formalization here.)
We can then expect that the number of spurious hits is O.n=q/, since we can es-
timate the chance that an arbitrary ts will be equivalent to p, modulo q, as 1=q.
Since there are O.n/ positions at which the test of line 10 fails and we spend O.m/
time for each hit, the expected matching time taken by the Rabin-Karp algorithm
is
O.n/ C O.m. C n=q// ;
where  is the number of valid shifts. This running time is O.n/ if  D O.1/ and
we choose q  m. That is, if the expected number of valid shifts is small (O.1/)
and we choose the prime q to be larger than the length of the pattern, then we
can expect the Rabin-Karp procedure to use only O.n C m/ matching time. Since
m  n, this expected matching time is O.n/.
Exercises
32.2-1
Working modulo q D 11, how many spurious hits does the Rabin-Karp matcher en-
counter in the text T D 3141592653589793 when looking for the pattern P D 26?
32.2-2
How would you extend the Rabin-Karp method to the problem of searching a text
string for an occurrence of any one of a given set of k patterns? Start by assuming
that all k patterns have the same length. Then generalize your solution to allow the
patterns to have different lengths.
32.2-3
Show how to extend the Rabin-Karp method to handle the problem of looking for
a given m 	 m pattern in an n 	 n array of characters. (The pattern may be shifted
vertically and horizontally, but it may not be rotated.)

32.3
String matching with ﬁnite automata
995
32.2-4
Alice has a copy of a long n-bit ﬁle A D han1; an2; : : : ; a0i, and Bob similarly
has an n-bit ﬁle B D hbn1; bn2; : : : ; b0i. Alice and Bob wish to know if their
ﬁles are identical. To avoid transmitting all of A or B, they use the following fast
probabilistic check. Together, they select a prime q > 1000n and randomly select
an integer x from f0; 1; : : : ; q  1g. Then, Alice evaluates
A.x/ D
 n1
X
iD0
aixi
!
mod q
and Bob similarly evaluates B.x/. Prove that if A ¤ B, there is at most one
chance in 1000 that A.x/ D B.x/, whereas if the two ﬁles are the same, A.x/ is
necessarily the same as B.x/. (Hint: See Exercise 31.4-4.)
32.3
String matching with ﬁnite automata
Many string-matching algorithms build a ﬁnite automaton—a simple machine for
processing information—that scans the text string T for all occurrences of the pat-
tern P . This section presents a method for building such an automaton. These
string-matching automata are very efﬁcient: they examine each text character ex-
actly once, taking constant time per text character. The matching time used—after
preprocessing the pattern to build the automaton—is therefore ‚.n/. The time to
build the automaton, however, can be large if † is large. Section 32.4 describes a
clever way around this problem.
We begin this section with the deﬁnition of a ﬁnite automaton. We then examine
a special string-matching automaton and show how to use it to ﬁnd occurrences
of a pattern in a text. Finally, we shall show how to construct the string-matching
automaton for a given input pattern.
Finite automata
A ﬁnite automaton M, illustrated in Figure 32.6, is a 5-tuple .Q; q0; A; †; ı/,
where

Q is a ﬁnite set of states,

q0 2 Q is the start state,

A  Q is a distinguished set of accepting states,

† is a ﬁnite input alphabet,

ı is a function from Q 	 † into Q, called the transition function of M.

996
Chapter 32
String Matching
1
0
0
0
a
b
input
state
0
1
(a)
a
a
b
b
(b)
0
1
Figure 32.6
A simple two-state ﬁnite automaton with state set Q D f0; 1g, start state q0 D 0,
and input alphabet † D fa; bg. (a) A tabular representation of the transition function ı. (b) An
equivalent state-transition diagram. State 1, shown blackend, is the only accepting state. Directed
edges represent transitions. For example, the edge from state 1 to state 0 labeled b indicates that
ı.1; b/ D 0. This automaton accepts those strings that end in an odd number of a’s. More precisely,
it accepts a string x if and only if x D y´, where y D " or y ends with a b, and ´ D ak, where k is
odd. For example, on input abaaa, including the start state, this automaton enters the sequence of
states h0; 1; 0; 1; 0; 1i, and so it accepts this input. For input abbaa, it enters the sequence of states
h0; 1; 0; 0; 1; 0i, and so it rejects this input.
The ﬁnite automaton begins in state q0 and reads the characters of its input string
one at a time. If the automaton is in state q and reads input character a, it moves
(“makes a transition”) from state q to state ı.q; a/. Whenever its current state q is
a member of A, the machine M has accepted the string read so far. An input that
is not accepted is rejected.
A ﬁnite automaton M induces a function , called the ﬁnal-state function,
from † to Q such that .w/ is the state M ends up in after scanning the string w.
Thus, M accepts a string w if and only if .w/ 2 A. We deﬁne the function 
recursively, using the transition function:
D
q0 ;
.wa/
D
ı..w/; a/
for w 2 †; a 2 † .
String-matching automata
For a given pattern P , we construct a string-matching automaton in a preprocess-
ing step before using it to search the text string. Figure 32.7 illustrates how we
construct the automaton for the pattern P D ababaca. From now on, we shall
assume that P is a given ﬁxed pattern string; for brevity, we shall not indicate the
dependence upon P in our notation.
In order to specify the string-matching automaton corresponding to a given pat-
tern P Œ1 : : m, we ﬁrst deﬁne an auxiliary function 	, called the sufﬁx function
corresponding to P . The function 	 maps † to f0; 1; : : : ; mg such that 	.x/ is the
length of the longest preﬁx of P that is also a sufﬁx of x:
	.x/ D max fk W Pk = xg :
(32.3)

32.3
String matching with ﬁnite automata
997
0
1
2
3
4
5
6
7
a
b
a
b
a
c
a
b
a
a
a
a
b
(a)
1
0
0
1
2
0
3
0
0
1
4
0
5
0
0
1
4
6
7
0
0
1
2
0
0
1
2
3
4
5
6
7
state
input
a
b
c
a
b
a
b
a
c
a
P
(b)
1
2
3
4
5
6
7
8
9 10 11
a
b
a
b
a
b
a
c
a
b
a
0
1
2
3
4
5
4
5
6
7
2
3
—
—
(c)
i
T Œi
state .Ti/
Figure 32.7
(a) A state-transition diagram for the string-matching automaton that accepts all
strings ending in the string ababaca. State 0 is the start state, and state 7 (shown blackened) is
the only accepting state. A directed edge from state i to state j labeled a represents ı.i; a/ D j. The
right-going edges forming the “spine” of the automaton, shown heavy in the ﬁgure, correspond to
successful matches between pattern and input characters. The left-going edges correspond to failing
matches. Some edges corresponding to failing matches are omitted; by convention, if a state i has
no outgoing edge labeled a for some a 2 †, then ı.i; a/ D 0. (b) The corresponding transition
function ı, and the pattern string P D ababaca. The entries corresponding to successful matches
between pattern and input characters are shown shaded. (c) The operation of the automaton on the
text T D abababacaba. Under each text character T Œi appears the state .Ti/ that the automa-
ton is in after processing the preﬁx Ti. The automaton ﬁnds one occurrence of the pattern, ending in
position 9.
The sufﬁx function 	 is well deﬁned since the empty string P0 D " is a suf-
ﬁx of every string. As examples, for the pattern P D ab, we have 	."/ D 0,
	.ccaca/ D 1, and 	.ccab/ D 2. For a pattern P of length m, we have
	.x/ D m if and only if P = x. From the deﬁnition of the sufﬁx function,
x = y implies 	.x/  	.y/.
We deﬁne the string-matching automaton that corresponds to a given pattern
P Œ1 : : m as follows:

998
Chapter 32
String Matching

The state set Q is f0; 1; : : : ; mg. The start state q0 is state 0, and state m is the
only accepting state.

The transition function ı is deﬁned by the following equation, for any state q
and character a:
ı.q; a/ D 	.Pqa/ :
(32.4)
We deﬁne ı.q; a/ D 	.Pqa/ because we want to keep track of the longest pre-
ﬁx of the pattern P that has matched the text string T so far. We consider the
most recently read characters of T . In order for a substring of T —let’s say the
substring ending at T Œi—to match some preﬁx Pj of P , this preﬁx Pj must be a
sufﬁx of Ti. Suppose that q D .Ti/, so that after reading Ti, the automaton is in
state q. We design the transition function ı so that this state number, q, tells us the
length of the longest preﬁx of P that matches a sufﬁx of Ti. That is, in state q,
Pq = Ti and q D 	.Ti/. (Whenever q D m, all m characters of P match a sufﬁx
of Ti, and so we have found a match.) Thus, since .Ti/ and 	.Ti/ both equal q,
we shall see (in Theorem 32.4, below) that the automaton maintains the following
invariant:
.Ti/ D 	.Ti/ :
(32.5)
If the automaton is in state q and reads the next character T Œi C 1 D a, then we
want the transition to lead to the state corresponding to the longest preﬁx of P that
is a sufﬁx of Tia, and that state is 	.Tia/. Because Pq is the longest preﬁx of P
that is a sufﬁx of Ti, the longest preﬁx of P that is a sufﬁx of Tia is not only 	.Tia/,
but also 	.Pqa/. (Lemma 32.3, on page 1000, proves that 	.Tia/ D 	.Pqa/.)
Thus, when the automaton is in state q, we want the transition function on charac-
ter a to take the automaton to state 	.Pqa/.
There are two cases to consider. In the ﬁrst case, a D P Œq C 1, so that the
character a continues to match the pattern; in this case, because ı.q; a/ D qC1, the
transition continues to go along the “spine” of the automaton (the heavy edges in
Figure 32.7). In the second case, a ¤ P ŒqC1, so that a does not continue to match
the pattern. Here, we must ﬁnd a smaller preﬁx of P that is also a sufﬁx of Ti.
Because the preprocessing step matches the pattern against itself when creating the
string-matching automaton, the transition function quickly identiﬁes the longest
such smaller preﬁx of P .
Let’s look at an example. The string-matching automaton of Figure 32.7 has
ı.5; c/ D 6, illustrating the ﬁrst case, in which the match continues. To illus-
trate the second case, observe that the automaton of Figure 32.7 has ı.5; b/ D 4.
We make this transition because if the automaton reads a b in state q D 5, then
Pqb D ababab, and the longest preﬁx of P that is also a sufﬁx of ababab is
P4 D abab.

32.3
String matching with ﬁnite automata
999
x
a
Pr
Pr–1
Figure 32.8
An illustration for the proof of Lemma 32.2. The ﬁgure shows that r  	.x/ C 1,
where r D 	.xa/.
To clarify the operation of a string-matching automaton, we now give a simple,
efﬁcient program for simulating the behavior of such an automaton (represented
by its transition function ı) in ﬁnding occurrences of a pattern P of length m in an
input text T Œ1 : : n. As for any string-matching automaton for a pattern of length m,
the state set Q is f0; 1; : : : ; mg, the start state is 0, and the only accepting state is
state m.
FINITE-AUTOMATON-MATCHER.T; ı; m/
1
n D T:length
2
q D 0
3
for i D 1 to n
4
q D ı.q; T Œi/
5
if q == m
6
print “Pattern occurs with shift” i  m
From the simple loop structure of FINITE-AUTOMATON-MATCHER, we can easily
see that its matching time on a text string of length n is ‚.n/. This matching
time, however, does not include the preprocessing time required to compute the
transition function ı. We address this problem later, after ﬁrst proving that the
procedure FINITE-AUTOMATON-MATCHER operates correctly.
Consider how the automaton operates on an input text T Œ1 : : n. We shall prove
that the automaton is in state 	.Ti/ after scanning character T Œi. Since 	.Ti/ D m
if and only if P = Ti, the machine is in the accepting state m if and only if it has
just scanned the pattern P . To prove this result, we make use of the following two
lemmas about the sufﬁx function 	.
Lemma 32.2 (Sufﬁx-function inequality)
For any string x and character a, we have 	.xa/  	.x/ C 1.
Proof
Referring to Figure 32.8, let r D 	.xa/. If r D 0, then the conclusion
	.xa/ D r  	.x/ C 1 is trivially satisﬁed, by the nonnegativity of 	.x/. Now
assume that r > 0. Then, Pr = xa, by the deﬁnition of 	. Thus, Pr1 = x, by

1000
Chapter 32
String Matching
x
a
a
Pq
Pr
Figure 32.9
An illustration for the proof of Lemma 32.3. The ﬁgure shows that r D 	.Pqa/,
where q D 	.x/ and r D 	.xa/.
dropping the a from the end of Pr and from the end of xa. Therefore, r1  	.x/,
since 	.x/ is the largest k such that Pk = x, and thus 	.xa/ D r  	.x/ C 1.
Lemma 32.3 (Sufﬁx-function recursion lemma)
For any string x and character a, if q D 	.x/, then 	.xa/ D 	.Pqa/.
Proof
From the deﬁnition of 	, we have Pq = x. As Figure 32.9 shows, we
also have Pqa = xa. If we let r D 	.xa/, then Pr = xa and, by Lemma 32.2,
r  q C 1. Thus, we have jPrj D r  q C 1 D jPqaj. Since Pqa = xa, Pr = xa,
and jPrj  jPqaj, Lemma 32.1 implies that Pr = Pqa. Therefore, r  	.Pqa/,
that is, 	.xa/  	.Pqa/. But we also have 	.Pqa/  	.xa/, since Pqa = xa.
Thus, 	.xa/ D 	.Pqa/.
We are now ready to prove our main theorem characterizing the behavior of a
string-matching automaton on a given input text. As noted above, this theorem
shows that the automaton is merely keeping track, at each step, of the longest
preﬁx of the pattern that is a sufﬁx of what has been read so far. In other words,
the automaton maintains the invariant (32.5).
Theorem 32.4
If  is the ﬁnal-state function of a string-matching automaton for a given pattern P
and T Œ1 : : n is an input text for the automaton, then
.Ti/ D 	.Ti/
for i D 0; 1; : : : ; n.
Proof
The proof is by induction on i. For i D 0, the theorem is trivially true,
since T0 D ". Thus, .T0/ D 0 D 	.T0/.

32.3
String matching with ﬁnite automata
1001
Now, we assume that .Ti/ D 	.Ti/ and prove that .TiC1/ D 	.TiC1/. Let q
denote .Ti/, and let a denote T Œi C 1. Then,
.TiC1/
D
.Tia/
(by the deﬁnitions of TiC1 and a)
D
ı..Ti/; a/
(by the deﬁnition of )
D
ı.q; a/
(by the deﬁnition of q)
D
	.Pqa/
(by the deﬁnition (32.4) of ı)
D
	.Tia/
(by Lemma 32.3 and induction)
D
	.TiC1/
(by the deﬁnition of TiC1) .
By Theorem 32.4, if the machine enters state q on line 4, then q is the largest
value such that Pq = Ti. Thus, we have q D m on line 5 if and only if the ma-
chine has just scanned an occurrence of the pattern P . We conclude that FINITE-
AUTOMATON-MATCHER operates correctly.
Computing the transition function
The following procedure computes the transition function ı from a given pattern
P Œ1 : : m.
COMPUTE-TRANSITION-FUNCTION.P; †/
1
m D P:length
2
for q D 0 to m
3
for each character a 2 †
4
k D min.m C 1; q C 2/
5
repeat
6
k D k  1
7
until Pk = Pqa
8
ı.q; a/ D k
9
return ı
This procedure computes ı.q; a/ in a straightforward manner according to its def-
inition in equation (32.4). The nested loops beginning on lines 2 and 3 consider
all states q and all characters a, and lines 4–8 set ı.q; a/ to be the largest k such
that Pk = Pqa. The code starts with the largest conceivable value of k, which is
min.m; q C 1/. It then decreases k until Pk = Pqa, which must eventually occur,
since P0 D " is a sufﬁx of every string.
The running time of COMPUTE-TRANSITION-FUNCTION is O.m3 j†j/, be-
cause the outer loops contribute a factor of m j†j, the inner repeat loop can run
at most m C 1 times, and the test Pk = Pqa on line 7 can require comparing up

1002
Chapter 32
String Matching
to m characters. Much faster procedures exist; by utilizing some cleverly com-
puted information about the pattern P (see Exercise 32.4-8), we can improve the
time required to compute ı from P to O.m j†j/. With this improved procedure for
computing ı, we can ﬁnd all occurrences of a length-m pattern in a length-n text
over an alphabet † with O.m j†j/ preprocessing time and ‚.n/ matching time.
Exercises
32.3-1
Construct the string-matching automaton for the pattern P D aabab and illustrate
its operation on the text string T D aaababaabaababaab.
32.3-2
Draw a state-transition diagram for a string-matching automaton for the pattern
ababbabbababbababbabb over the alphabet † D fa; bg.
32.3-3
We call a pattern P nonoverlappable if Pk = Pq implies k D 0 or k D q. De-
scribe the state-transition diagram of the string-matching automaton for a nonover-
lappable pattern.
32.3-4
?
Given two patterns P and P 0, describe how to construct a ﬁnite automaton that
determines all occurrences of either pattern. Try to minimize the number of states
in your automaton.
32.3-5
Given a pattern P containing gap characters (see Exercise 32.1-4), show how to
build a ﬁnite automaton that can ﬁnd an occurrence of P in a text T in O.n/
matching time, where n D jT j.
?
32.4
The Knuth-Morris-Pratt algorithm
We now present a linear-time string-matching algorithm due to Knuth, Morris, and
Pratt. This algorithm avoids computing the transition function ı altogether, and its
matching time is ‚.n/ using just an auxiliary function , which we precompute
from the pattern in time ‚.m/ and store in an array Œ1 : : m. The array  allows
us to compute the transition function ı efﬁciently (in an amortized sense) “on the
ﬂy” as needed. Loosely speaking, for any state q D 0; 1; : : : ; m and any character

32.4
The Knuth-Morris-Pratt algorithm
1003
a 2 †, the value Œq contains the information we need to compute ı.q; a/ but
that does not depend on a. Since the array  has only m entries, whereas ı has
‚.m j†j/ entries, we save a factor of j†j in the preprocessing time by computing 
rather than ı.
The preﬁx function for a pattern
The preﬁx function  for a pattern encapsulates knowledge about how the pat-
tern matches against shifts of itself. We can take advantage of this information to
avoid testing useless shifts in the naive pattern-matching algorithm and to avoid
precomputing the full transition function ı for a string-matching automaton.
Consider the operation of the naive string matcher. Figure 32.10(a) shows a
particular shift s of a template containing the pattern P D ababaca against a
text T . For this example, q D 5 of the characters have matched successfully, but
the 6th pattern character fails to match the corresponding text character. The infor-
mation that q characters have matched successfully determines the corresponding
text characters. Knowing these q text characters allows us to determine immedi-
ately that certain shifts are invalid. In the example of the ﬁgure, the shift s C 1 is
necessarily invalid, since the ﬁrst pattern character (a) would be aligned with a text
character that we know does not match the ﬁrst pattern character, but does match
the second pattern character (b). The shift s0 D s C 2 shown in part (b) of the ﬁg-
ure, however, aligns the ﬁrst three pattern characters with three text characters that
must necessarily match. In general, it is useful to know the answer to the following
question:
Given that pattern characters P Œ1 : : q match text characters T ŒsC1 : : sCq,
what is the least shift s0 > s such that for some k < q,
P Œ1 : : k D T Œs0 C 1 : : s0 C k ;
(32.6)
where s0 C k D s C q?
In other words, knowing that Pq = TsCq, we want the longest proper preﬁx Pk
of Pq that is also a sufﬁx of TsCq. (Since s0 C k D s C q, if we are given s
and q, then ﬁnding the smallest shift s0 is tantamount to ﬁnding the longest preﬁx
length k.) We add the difference q  k in the lengths of these preﬁxes of P to the
shift s to arrive at our new shift s0, so that s0 D s C.q k/. In the best case, k D 0,
so that s0 D s C q, and we immediately rule out shifts s C 1; s C 2; : : : ; s C q  1.
In any case, at the new shift s0 we don’t need to compare the ﬁrst k characters of P
with the corresponding characters of T , since equation (32.6) guarantees that they
match.
We can precompute the necessary information by comparing the pattern against
itself, as Figure 32.10(c) demonstrates. Since T Œs0 C 1 : : s0 C k is part of the

1004
Chapter 32
String Matching
b
a
c
b
a
b
a
b
a
(a)
a
b
a
a
b
c
b
a
b
b
a
c
a
s
T
P
q
b
a
c
b
a
b
a
b
a
(b)
a
b
a
a
b
c
b
a
b
b
a
c
a
s′ = s + 2
T
P
k
a
b
a
b
a
a
b
a
(c)
Pq
Pk
Figure 32.10
The preﬁx function . (a) The pattern P D ababaca aligns with a text T so that
the ﬁrst q D 5 characters match. Matching characters, shown shaded, are connected by vertical lines.
(b) Using only our knowledge of the 5 matched characters, we can deduce that a shift of s C 1 is
invalid, but that a shift of s0 D sC2 is consistent with everything we know about the text and therefore
is potentially valid. (c) We can precompute useful information for such deductions by comparing the
pattern with itself. Here, we see that the longest preﬁx of P that is also a proper sufﬁx of P5 is P3.
We represent this precomputed information in the array , so that Œ5 D 3. Given that q characters
have matched successfully at shift s, the next potentially valid shift is at s0 D sC.qŒq/ as shown
in part (b).
known portion of the text, it is a sufﬁx of the string Pq. Therefore, we can interpret
equation (32.6) as asking for the greatest k < q such that Pk = Pq. Then, the new
shift s0 D sC.qk/ is the next potentially valid shift. We will ﬁnd it convenient to
store, for each value of q, the number k of matching characters at the new shift s0,
rather than storing, say, s0  s.
We formalize the information that we precompute as follows. Given a pattern
P Œ1 : : m, the preﬁx function for the pattern P is the function  W f1; 2; : : : ; mg !
f0; 1; : : : ; m  1g such that
Œq D max fk W k < q and Pk = Pqg :
That is, Œq is the length of the longest preﬁx of P that is a proper sufﬁx of Pq.
Figure 32.11(a) gives the complete preﬁx function  for the pattern ababaca.

32.4
The Knuth-Morris-Pratt algorithm
1005
1
2
3
4
5
6
7
0
0
1
2
3
0
1
a
b
a
b
a
c
a
(a)
a
b
a
b
a
c
a
a
b
a
b
a
c
a
a
b
a
b
a
c
a
a
b
a
b
a
c
a
(b)
"
i
P Œi
Œi
P5
P3
P1
P0
Œ5 D 3
Œ3 D 1
Œ1 D 0
Figure 32.11
An illustration of Lemma 32.5 for the pattern P D ababaca and q D 5. (a) The 
function for the given pattern. Since Œ5 D 3, Œ3 D 1, and Œ1 D 0, by iterating  we obtain
Œ5 D f3; 1; 0g. (b) We slide the template containing the pattern P to the right and note when some
preﬁx Pk of P matches up with some proper sufﬁx of P5; we get matches when k D 3, 1, and 0. In
the ﬁgure, the ﬁrst row gives P , and the dotted vertical line is drawn just after P5. Successive rows
show all the shifts of P that cause some preﬁx Pk of P to match some sufﬁx of P5. Successfully
matched characters are shown shaded. Vertical lines connect aligned matching characters. Thus,
fk W k < 5 and Pk = P5g D f3; 1; 0g. Lemma 32.5 claims that Œq D fk W k < q and Pk = Pqg
for all q.
The pseudocode below gives the Knuth-Morris-Pratt matching algorithm as
the procedure KMP-MATCHER. For the most part, the procedure follows from
FINITE-AUTOMATON-MATCHER, as we shall see. KMP-MATCHER calls the aux-
iliary procedure COMPUTE-PREFIX-FUNCTION to compute .
KMP-MATCHER.T; P /
1
n D T:length
2
m D P:length
3
 D COMPUTE-PREFIX-FUNCTION.P /
4
q D 0
// number of characters matched
5
for i D 1 to n
// scan the text from left to right
6
while q > 0 and P Œq C 1 ¤ T Œi
7
q D Œq
// next character does not match
8
if P Œq C 1 == T Œi
9
q D q C 1
// next character matches
10
if q == m
// is all of P matched?
11
print “Pattern occurs with shift” i  m
12
q D Œq
// look for the next match

1006
Chapter 32
String Matching
COMPUTE-PREFIX-FUNCTION.P /
1
m D P:length
2
let Œ1 : : m be a new array
3
Œ1 D 0
4
k D 0
5
for q D 2 to m
6
while k > 0 and P Œk C 1 ¤ P Œq
7
k D Œk
8
if P Œk C 1 == P Œq
9
k D k C 1
10
Œq D k
11
return 
These two procedures have much in common, because both match a string against
the pattern P : KMP-MATCHER matches the text T against P , and COMPUTE-
PREFIX-FUNCTION matches P against itself.
We begin with an analysis of the running times of these procedures. Proving
these procedures correct will be more complicated.
Running-time analysis
The running time of COMPUTE-PREFIX-FUNCTION is ‚.m/, which we show by
using the aggregate method of amortized analysis (see Section 17.1). The only
tricky part is showing that the while loop of lines 6–7 executes O.m/ times alto-
gether. We shall show that it makes at most m  1 iterations. We start by making
some observations about k. First, line 4 starts k at 0, and the only way that k
increases is by the increment operation in line 9, which executes at most once per
iteration of the for loop of lines 5–10. Thus, the total increase in k is at most m1.
Second, since k < q upon entering the for loop and each iteration of the loop in-
crements q, we always have k < q. Therefore, the assignments in lines 3 and 10
ensure that Œq < q for all q D 1; 2; : : : ; m, which means that each iteration of
the while loop decreases k. Third, k never becomes negative. Putting these facts
together, we see that the total decrease in k from the while loop is bounded from
above by the total increase in k over all iterations of the for loop, which is m  1.
Thus, the while loop iterates at most m  1 times in all, and COMPUTE-PREFIX-
FUNCTION runs in time ‚.m/.
Exercise 32.4-4 asks you to show, by a similar aggregate analysis, that the match-
ing time of KMP-MATCHER is ‚.n/.
Compared with FINITE-AUTOMATON-MATCHER, by using  rather than ı, we
have reduced the time for preprocessing the pattern from O.m j†j/ to ‚.m/, while
keeping the actual matching time bounded by ‚.n/.

32.4
The Knuth-Morris-Pratt algorithm
1007
Correctness of the preﬁx-function computation
We shall see a little later that the preﬁx function  helps us simulate the transition
function ı in a string-matching automaton. But ﬁrst, we need to prove that the
procedure COMPUTE-PREFIX-FUNCTION does indeed compute the preﬁx func-
tion correctly. In order to do so, we will need to ﬁnd all preﬁxes Pk that are proper
sufﬁxes of a given preﬁx Pq. The value of Œq gives us the longest such preﬁx, but
the following lemma, illustrated in Figure 32.11, shows that by iterating the preﬁx
function , we can indeed enumerate all the preﬁxes Pk that are proper sufﬁxes
of Pq. Let
Œq D fŒq; .2/Œq; .3/Œq; : : : ; .t/Œqg ;
where .i/Œq is deﬁned in terms of functional iteration, so that .0/Œq D q and
.i/Œq D Œ.i1/Œq for i  1, and where the sequence in Œq stops upon
reaching .t/Œq D 0.
Lemma 32.5 (Preﬁx-function iteration lemma)
Let P be a pattern of length m with preﬁx function . Then, for q D 1; 2; : : : ; m,
we have Œq D fk W k < q and Pk = Pqg.
Proof
We ﬁrst prove that Œq  fk W k < q and Pk = Pqg or, equivalently,
i 2 Œq implies Pi = Pq :
(32.7)
If i 2 Œq, then i D .u/Œq for some u > 0. We prove equation (32.7) by
induction on u. For u D 1, we have i D Œq, and the claim follows since i < q
and PŒq = Pq by the deﬁnition of . Using the relations Œi < i and PŒi = Pi
and the transitivity of < and = establishes the claim for all i in Œq. Therefore,
Œq  fk W k < q and Pk = Pqg.
We now prove that fk W k < q and Pk = Pqg  Œq by contradiction. Sup-
pose to the contrary that the set fk W k < q and Pk = Pqg  Œq is nonempty,
and let j be the largest number in the set. Because Œq is the largest value in
fk W k < q and Pk = Pqg and Œq 2 Œq, we must have j < Œq, and so we
let j 0 denote the smallest integer in Œq that is greater than j . (We can choose
j 0 D Œq if no other number in Œq is greater than j .) We have Pj = Pq because
j 2 fk W k < q and Pk = Pqg, and from j 0 2 Œq and equation (32.7), we have
Pj 0 = Pq. Thus, Pj = Pj 0 by Lemma 32.1, and j is the largest value less than j 0
with this property. Therefore, we must have Œj 0 D j and, since j 0 2 Œq, we
must have j 2 Œq as well. This contradiction proves the lemma.
The algorithm COMPUTE-PREFIX-FUNCTION computes Œq, in order, for q D
1; 2; : : : ; m. Setting Œ1 to 0 in line 3 of COMPUTE-PREFIX-FUNCTION is cer-
tainly correct, since Œq < q for all q. We shall use the following lemma and

1008
Chapter 32
String Matching
its corollary to prove that COMPUTE-PREFIX-FUNCTION computes Œq correctly
for q > 1.
Lemma 32.6
Let P be a pattern of length m, and let  be the preﬁx function for P . For q D
1; 2; : : : ; m, if Œq > 0, then Œq  1 2 Œq  1.
Proof
Let r D Œq > 0, so that r < q and Pr = Pq; thus, r  1 < q  1 and
Pr1 = Pq1 (by dropping the last character from Pr and Pq, which we can do
because r > 0). By Lemma 32.5, therefore, r  1 2 Œq  1. Thus, we have
Œq  1 D r  1 2 Œq  1.
For q D 2; 3; : : : ; m, deﬁne the subset Eq1  Œq  1 by
Eq1 D fk 2 Œq  1 W P Œk C 1 D P Œqg
D fk W k < q  1 and Pk = Pq1 and P Œk C 1 D P Œqg (by Lemma 32.5)
D fk W k < q  1 and PkC1 = Pqg :
The set Eq1 consists of the values k < q  1 for which Pk = Pq1 and for which,
because P Œk C 1 D P Œq, we have PkC1 = Pq. Thus, Eq1 consists of those
values k 2 Œq  1 such that we can extend Pk to PkC1 and get a proper sufﬁx
of Pq.
Corollary 32.7
Let P be a pattern of length m, and let  be the preﬁx function for P . For q D
2; 3; : : : ; m,
Œq D
(
0
if Eq1 D ; ;
1 C max fk 2 Eq1g
if Eq1 ¤ ; :
Proof
If Eq1 is empty, there is no k 2 Œq  1 (including k D 0) for which
we can extend Pk to PkC1 and get a proper sufﬁx of Pq. Therefore Œq D 0.
If Eq1 is nonempty, then for each k 2 Eq1 we have kC1 < q and PkC1 = Pq.
Therefore, from the deﬁnition of Œq, we have
Œq  1 C max fk 2 Eq1g :
(32.8)
Note that Œq > 0.
Let r D Œq  1, so that r C 1 D Œq and there-
fore PrC1 = Pq. Since r C 1 > 0, we have P Œr C 1 D P Œq. Furthermore,
by Lemma 32.6, we have r 2 Œq  1. Therefore, r 2 Eq1, and so r 
max fk 2 Eq1g or, equivalently,
Œq  1 C max fk 2 Eq1g :
(32.9)
Combining equations (32.8) and (32.9) completes the proof.

32.4
The Knuth-Morris-Pratt algorithm
1009
We now ﬁnish the proof that COMPUTE-PREFIX-FUNCTION computes  cor-
rectly. In the procedure COMPUTE-PREFIX-FUNCTION, at the start of each iter-
ation of the for loop of lines 5–10, we have that k D Œq  1. This condition
is enforced by lines 3 and 4 when the loop is ﬁrst entered, and it remains true in
each successive iteration because of line 10. Lines 6–9 adjust k so that it becomes
the correct value of Œq. The while loop of lines 6–7 searches through all values
k 2 Œq  1 until it ﬁnds a value of k for which P Œk C 1 D P Œq; at that point,
k is the largest value in the set Eq1, so that, by Corollary 32.7, we can set Œq
to k C 1. If the while loop cannot ﬁnd a k 2 Œq  1 such that P Œk C 1 D P Œq,
then k equals 0 at line 8. If P Œ1 D P Œq, then we should set both k and Œq to 1;
otherwise we should leave k alone and set Œq to 0. Lines 8–10 set k and Œq
correctly in either case. This completes our proof of the correctness of COMPUTE-
PREFIX-FUNCTION.
Correctness of the Knuth-Morris-Pratt algorithm
We can think of the procedure KMP-MATCHER as a reimplemented version of
the procedure FINITE-AUTOMATON-MATCHER, but using the preﬁx function 
to compute state transitions. Speciﬁcally, we shall prove that in the ith iteration of
the for loops of both KMP-MATCHER and FINITE-AUTOMATON-MATCHER, the
state q has the same value when we test for equality with m (at line 10 in KMP-
MATCHER and at line 5 in FINITE-AUTOMATON-MATCHER).
Once we have
argued that KMP-MATCHER simulates the behavior of FINITE-AUTOMATON-
MATCHER, the correctness of KMP-MATCHER follows from the correctness of
FINITE-AUTOMATON-MATCHER (though we shall see a little later why line 12 in
KMP-MATCHER is necessary).
Before we formally prove that KMP-MATCHER correctly simulates FINITE-
AUTOMATON-MATCHER, let’s take a moment to understand how the preﬁx func-
tion  replaces the ı transition function.
Recall that when a string-matching
automaton is in state q and it scans a character a D T Œi, it moves to a new
state ı.q; a/. If a D P Œq C 1, so that a continues to match the pattern, then
ı.q; a/ D q C 1. Otherwise, a ¤ P Œq C 1, so that a does not continue to match
the pattern, and 0  ı.q; a/  q. In the ﬁrst case, when a continues to match,
KMP-MATCHER moves to state q C 1 without referring to the  function: the
while loop test in line 6 comes up false the ﬁrst time, the test in line 8 comes up
true, and line 9 increments q.
The  function comes into play when the character a does not continue to match
the pattern, so that the new state ı.q; a/ is either q or to the left of q along the spine
of the automaton. The while loop of lines 6–7 in KMP-MATCHER iterates through
the states in Œq, stopping either when it arrives in a state, say q0, such that a
matches P Œq0 C 1 or q0 has gone all the way down to 0. If a matches P Œq0 C 1,

1010
Chapter 32
String Matching
then line 9 sets the new state to q0C1, which should equal ı.q; a/ for the simulation
to work correctly. In other words, the new state ı.q; a/ should be either state 0 or
one greater than some state in Œq.
Let’s look at the example in Figures 32.7 and 32.11, which are for the pattern
P D ababaca. Suppose that the automaton is in state q D 5; the states in
Œ5 are, in descending order, 3, 1, and 0. If the next character scanned is c, then
we can easily see that the automaton moves to state ı.5; c/ D 6 in both FINITE-
AUTOMATON-MATCHER and KMP-MATCHER. Now suppose that the next char-
acter scanned is instead b, so that the automaton should move to state ı.5; b/ D 4.
The while loop in KMP-MATCHER exits having executed line 7 once, and it ar-
rives in state q0 D Œ5 D 3. Since P Œq0 C 1 D P Œ4 D b, the test in line 8
comes up true, and KMP-MATCHER moves to the new state q0 C1 D 4 D ı.5; b/.
Finally, suppose that the next character scanned is instead a, so that the automa-
ton should move to state ı.5; a/ D 1. The ﬁrst three times that the test in line 6
executes, the test comes up true. The ﬁrst time, we ﬁnd that P Œ6 D c ¤ a, and
KMP-MATCHER moves to state Œ5 D 3 (the ﬁrst state in Œ5). The second
time, we ﬁnd that P Œ4 D b ¤ a and move to state Œ3 D 1 (the second state
in Œ5). The third time, we ﬁnd that P Œ2 D b ¤ a and move to state Œ1 D 0
(the last state in Œ5). The while loop exits once it arrives in state q0 D 0. Now,
line 8 ﬁnds that P Œq0 C1 D P Œ1 D a, and line 9 moves the automaton to the new
state q0 C 1 D 1 D ı.5; a/.
Thus, our intuition is that KMP-MATCHER iterates through the states in Œq in
decreasing order, stopping at some state q0 and then possibly moving to state q0C1.
Although that might seem like a lot of work just to simulate computing ı.q; a/,
bear in mind that asymptotically, KMP-MATCHER is no slower than FINITE-
AUTOMATON-MATCHER.
We are now ready to formally prove the correctness of the Knuth-Morris-Pratt
algorithm. By Theorem 32.4, we have that q D 	.Ti/ after each time we execute
line 4 of FINITE-AUTOMATON-MATCHER. Therefore, it sufﬁces to show that the
same property holds with regard to the for loop in KMP-MATCHER. The proof
proceeds by induction on the number of loop iterations. Initially, both procedures
set q to 0 as they enter their respective for loops for the ﬁrst time. Consider itera-
tion i of the for loop in KMP-MATCHER, and let q0 be state at the start of this loop
iteration. By the inductive hypothesis, we have q0 D 	.Ti1/. We need to show
that q D 	.Ti/ at line 10. (Again, we shall handle line 12 separately.)
When we consider the character T Œi, the longest preﬁx of P that is a sufﬁx of Ti
is either Pq0C1 (if P Œq0 C 1 D T Œi) or some preﬁx (not necessarily proper, and
possibly empty) of Pq0. We consider separately the three cases in which 	.Ti/ D 0,
	.Ti/ D q0 C 1, and 0 < 	.Ti/  q0.

32.4
The Knuth-Morris-Pratt algorithm
1011

If 	.Ti/ D 0, then P0 D " is the only preﬁx of P that is a sufﬁx of Ti. The while
loop of lines 6–7 iterates through the values in Œq0, but although Pq = Ti for
every q 2 Œq0, the loop never ﬁnds a q such that P Œq C 1 D T Œi. The loop
terminates when q reaches 0, and of course line 9 does not execute. Therefore,
q D 0 at line 10, so that q D 	.Ti/.

If 	.Ti/ D q0 C 1, then P Œq0 C 1 D T Œi, and the while loop test in line 6
fails the ﬁrst time through. Line 9 executes, incrementing q so that afterward
we have q D q0 C 1 D 	.Ti/.

If 0 < 	.Ti/  q0, then the while loop of lines 6–7 iterates at least once,
checking in decreasing order each value q 2 Œq0 until it stops at some q < q0.
Thus, Pq is the longest preﬁx of Pq0 for which P ŒqC1 D T Œi, so that when the
while loop terminates, q C 1 D 	.Pq0T Œi/. Since q0 D 	.Ti1/, Lemma 32.3
implies that 	.Ti1T Œi/ D 	.Pq0T Œi/. Thus, we have
q C 1
D
	.Pq0T Œi/
D
	.Ti1T Œi/
D
	.Ti/
when the while loop terminates. After line 9 increments q, we have q D 	.Ti/.
Line 12 is necessary in KMP-MATCHER, because otherwise, we might refer-
ence P Œm C 1 on line 6 after ﬁnding an occurrence of P . (The argument that
q D 	.Ti1/ upon the next execution of line 6 remains valid by the hint given in
Exercise 32.4-8: ı.m; a/ D ı.Œm; a/ or, equivalently, 	.Pa/ D 	.PŒma/ for
any a 2 †.) The remaining argument for the correctness of the Knuth-Morris-
Pratt algorithm follows from the correctness of FINITE-AUTOMATON-MATCHER,
since we have shown that KMP-MATCHER simulates the behavior of FINITE-
AUTOMATON-MATCHER.
Exercises
32.4-1
Compute the preﬁx function  for the pattern ababbabbabbababbabb.
32.4-2
Give an upper bound on the size of Œq as a function of q. Give an example to
show that your bound is tight.
32.4-3
Explain how to determine the occurrences of pattern P in the text T by examining
the  function for the string P T (the string of length mCn that is the concatenation
of P and T ).

1012
Chapter 32
String Matching
32.4-4
Use an aggregate analysis to show that the running time of KMP-MATCHER
is ‚.n/.
32.4-5
Use a potential function to show that the running time of KMP-MATCHER is ‚.n/.
32.4-6
Show how to improve KMP-MATCHER by replacing the occurrence of  in line 7
(but not line 12) by 0, where 0 is deﬁned recursively for q D 1; 2; : : : ; m  1 by
the equation
0Œq D

0
if Œq D 0 ;
0ŒŒq
if Œq ¤ 0 and P ŒŒq C 1 D P Œq C 1 ;
Œq
if Œq ¤ 0 and P ŒŒq C 1 ¤ P Œq C 1 :
Explain why the modiﬁed algorithm is correct, and explain in what sense this
change constitutes an improvement.
32.4-7
Give a linear-time algorithm to determine whether a text T is a cyclic rotation of
another string T 0. For example, arc and car are cyclic rotations of each other.
32.4-8
?
Give an O.m j†j/-time algorithm for computing the transition function ı for the
string-matching automaton corresponding to a given pattern P . (Hint: Prove that
ı.q; a/ D ı.Œq; a/ if q D m or P Œq C 1 ¤ a.)
Problems
32-1
String matching based on repetition factors
Let yi denote the concatenation of string y with itself i times.
For example,
.ab/3 D ababab. We say that a string x 2 † has repetition factor r if x D yr
for some string y 2 † and some r > 0. Let .x/ denote the largest r such that x
has repetition factor r.
a. Give an efﬁcient algorithm that takes as input a pattern P Œ1 : : m and computes
the value .Pi/ for i D 1; 2; : : : ; m. What is the running time of your algo-
rithm?

Notes for Chapter 32
1013
b. For any pattern P Œ1 : : m, let .P / be deﬁned as max1im .Pi/. Prove that if
the pattern P is chosen randomly from the set of all binary strings of length m,
then the expected value of .P / is O.1/.
c. Argue that the following string-matching algorithm correctly ﬁnds all occur-
rences of pattern P in a text T Œ1 : : n in time O..P /n C m/:
REPETITION-MATCHER.P; T /
1
m D P:length
2
n D T:length
3
k D 1 C .P /
4
q D 0
5
s D 0
6
while s  n  m
7
if T Œs C q C 1 == P Œq C 1
8
q D q C 1
9
if q == m
10
print “Pattern occurs with shift” s
11
if q == m or T Œs C q C 1 ¤ P Œq C 1
12
s D s C max.1; dq=ke/
13
q D 0
This algorithm is due to Galil and Seiferas. By extending these ideas greatly,
they obtained a linear-time string-matching algorithm that uses only O.1/ stor-
age beyond what is required for P and T .
Chapter notes
The relation of string matching to the theory of ﬁnite automata is discussed by
Aho, Hopcroft, and Ullman [5].
The Knuth-Morris-Pratt algorithm [214] was
invented independently by Knuth and Pratt and by Morris; they published their
work jointly. Reingold, Urban, and Gries [294] give an alternative treatment of the
Knuth-Morris-Pratt algorithm. The Rabin-Karp algorithm was proposed by Karp
and Rabin [201]. Galil and Seiferas [126] give an interesting deterministic linear-
time string-matching algorithm that uses only O.1/ space beyond that required to
store the pattern and text.

## Figures

![Page 1006 figure](images/32-string-matching/p1006_figure1.png)

![Page 1008 figure](images/32-string-matching/p1008_figure2.png)

![Page 1009 figure](images/32-string-matching/p1009_figure3.png)

![Page 1013 figure](images/32-string-matching/p1013_figure4.png)

![Page 1017 figure](images/32-string-matching/p1017_figure5.png)

![Page 1018 figure](images/32-string-matching/p1018_figure6.png)

![Page 1020 figure](images/32-string-matching/p1020_figure7.png)

![Page 1021 figure](images/32-string-matching/p1021_figure8.png)

![Page 1025 figure](images/32-string-matching/p1025_figure9.png)

![Page 1026 figure](images/32-string-matching/p1026_figure10.png)
