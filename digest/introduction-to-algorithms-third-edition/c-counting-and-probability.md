# C Counting and Probability

C
Counting and Probability
This appendix reviews elementary combinatorics and probability theory. If you
have a good background in these areas, you may want to skim the beginning of this
appendix lightly and concentrate on the later sections. Most of this book’s chapters
do not require probability, but for some chapters it is essential.
Section C.1 reviews elementary results in counting theory, including standard
formulas for counting permutations and combinations. The axioms of probability
and basic facts concerning probability distributions form Section C.2. Random
variables are introduced in Section C.3, along with the properties of expectation
and variance. Section C.4 investigates the geometric and binomial distributions
that arise from studying Bernoulli trials. The study of the binomial distribution
continues in Section C.5, an advanced discussion of the “tails” of the distribution.
C.1
Counting
Counting theory tries to answer the question “How many?” without actually enumerating all the choices. For example, we might ask, “How many different n-bit
numbers are there?” or “How many orderings of n distinct elements are there?” In
this section, we review the elements of counting theory. Since some of the material
assumes a basic understanding of sets, you might wish to start by reviewing the
material in Section B.1.
Rules of sum and product
We can sometimes express a set of items that we wish to count as a union of disjoint
sets or as a Cartesian product of sets.
The rule of sum says that the number of ways to choose one element from one
of two disjoint sets is the sum of the cardinalities of the sets. That is, if A and B
are two ﬁnite sets with no members in common, then jA [ Bj D jAj C jBj, which

Appendix C
Counting and Probability
follows from equation (B.3). For example, each position on a car’s license plate
is a letter or a digit. The number of possibilities for each position is therefore
26 C 10 D 36, since there are 26 choices if it is a letter and 10 choices if it is a
digit.
The rule of product says that the number of ways to choose an ordered pair is the
number of ways to choose the ﬁrst element times the number of ways to choose the
second element. That is, if A and B are two ﬁnite sets, then jA 	 Bj D jAj  jBj,
which is simply equation (B.4). For example, if an ice-cream parlor offers 28
ﬂavors of ice cream and 4 toppings, the number of possible sundaes with one scoop
of ice cream and one topping is 28  4 D 112.
Strings
A string over a ﬁnite set S is a sequence of elements of S. For example, there are 8
binary strings of length 3:
000; 001; 010; 011; 100; 101; 110; 111 :
We sometimes call a string of length k a k-string. A substring s0 of a string s
is an ordered sequence of consecutive elements of s. A k-substring of a string
is a substring of length k. For example, 010 is a 3-substring of 01101001 (the
3-substring that begins in position 4), but 111 is not a substring of 01101001.
We can view a k-string over a set S as an element of the Cartesian product S k
of k-tuples; thus, there are jSjk strings of length k. For example, the number of
binary k-strings is 2k. Intuitively, to construct a k-string over an n-set, we have n
ways to pick the ﬁrst element; for each of these choices, we have n ways to pick the
second element; and so forth k times. This construction leads to the k-fold product
n  n    n D nk as the number of k-strings.
Permutations
A permutation of a ﬁnite set S is an ordered sequence of all the elements of S,
with each element appearing exactly once. For example, if S D fa; b; cg, then S
has 6 permutations:
abc; acb; bac; bca; cab; cba :
There are nŠ permutations of a set of n elements, since we can choose the ﬁrst
element of the sequence in n ways, the second in n  1 ways, the third in n  2
ways, and so on.
A k-permutation of S is an ordered sequence of k elements of S, with no element appearing more than once in the sequence. (Thus, an ordinary permutation is
an n-permutation of an n-set.) The twelve 2-permutations of the set fa; b; c; dg are

C.1
Counting
ab; ac; ad; ba; bc; bd; ca; cb; cd; da; db; dc :
The number of k-permutations of an n-set is
n.n  1/.n  2/    .n  k C 1/ D
nŠ
.n  k/Š ;
(C.1)
since we have n ways to choose the ﬁrst element, n  1 ways to choose the second
element, and so on, until we have selected k elements, the last being a selection
from the remaining n  k C 1 elements.
Combinations
A k-combination of an n-set S is simply a k-subset of S. For example, the 4-set
fa; b; c; dg has six 2-combinations:
ab; ac; ad; bc; bd; cd :
(Here we use the shorthand of denoting the 2-subset fa; bg by ab, and so on.)
We can construct a k-combination of an n-set by choosing k distinct (different)
elements from the n-set. The order in which we select the elements does not matter.
We can express the number of k-combinations of an n-set in terms of the number
of k-permutations of an n-set. Every k-combination has exactly kŠ permutations
of its elements, each of which is a distinct k-permutation of the n-set. Thus, the
number of k-combinations of an n-set is the number of k-permutations divided
by kŠ; from equation (C.1), this quantity is
nŠ
kŠ .n  k/Š :
(C.2)
For k D 0, this formula tells us that the number of ways to choose 0 elements from
an n-set is 1 (not 0), since 0Š D 1.
Binomial coefﬁcients
The notation

n
k

(read “n choose k”) denotes the number of k-combinations of
an n-set. From equation (C.2), we have

n
k
!
D
nŠ
kŠ .n  k/Š :
This formula is symmetric in k and n  k:

n
k
!
D

n
n  k
!
:
(C.3)

Appendix C
Counting and Probability
These numbers are also known as binomial coefﬁcients, due to their appearance in
the binomial expansion:
.x C y/n D
n
X
kD0

n
k
!
xkynk :
(C.4)
A special case of the binomial expansion occurs when x D y D 1:
2n D
n
X
kD0

n
k
!
:
This formula corresponds to counting the 2n binary n-strings by the number of 1s
they contain:

n
k

binary n-strings contain exactly k 1s, since we have

n
k

ways to
choose k out of the n positions in which to place the 1s.
Many identities involve binomial coefﬁcients. The exercises at the end of this
section give you the opportunity to prove a few.
Binomial bounds
We sometimes need to bound the size of a binomial coefﬁcient. For 1  k  n,
we have the lower bound

n
k
!
D
n.n  1/    .n  k C 1/
k.k  1/    1
D
n
k
 n  1
k  1

n  k C 1


n
k
k
:
Taking advantage of the inequality kŠ  .k=e/k derived from Stirling’s approximation (3.18), we obtain the upper bounds

n
k
!
D
n.n  1/    .n  k C 1/
k.k  1/    1

nk
kŠ

en
k
k
:
(C.5)
For all integers k such that 0  k  n, we can use induction (see Exercise C.1-12)
to prove the bound

C.1
Counting

n
k
!

nn
kk.n  k/nk ;
(C.6)
where for convenience we assume that 00 D 1. For k D n, where 0    1, we
can rewrite this bound as

n
n
!

nn
.n/	n..1  /n/.1	/n
D
1

1  
1	!n
D
2n H.	/ ;
where
H./ D  lg   .1  / lg.1  /
(C.7)
is the (binary) entropy function and where, for convenience, we assume that
0 lg 0 D 0, so that H.0/ D H.1/ D 0.

## Exercises

C.1-1
How many k-substrings does an n-string have? (Consider identical k-substrings at
different positions to be different.) How many substrings does an n-string have in
total?
C.1-2
An n-input, m-output boolean function is a function from fTRUE; FALSEgn to
fTRUE; FALSEgm. How many n-input, 1-output boolean functions are there? How
many n-input, m-output boolean functions are there?
C.1-3
In how many ways can n professors sit around a circular conference table? Consider two seatings to be the same if one can be rotated to form the other.
C.1-4
In how many ways can we choose three distinct numbers from the set f1; 2; : : : ; 99g
so that their sum is even?

Appendix C
Counting and Probability
C.1-5
Prove the identity

n
k
!
D n
k

n  1
k  1
!
(C.8)
for 0 < k  n.
C.1-6
Prove the identity

n
k
!
D
n
n  k

n  1
k
!
for 0  k < n.
C.1-7
To choose k objects from n, you can make one of the objects distinguished and
consider whether the distinguished object is chosen. Use this approach to prove
that

n
k
!
D

n  1
k
!
C

n  1
k  1
!
:
C.1-8
Using the result of Exercise C.1-7, make a table for n D 0; 1; : : : ; 6 and 0  k  n
of the binomial coefﬁcients

n
k

with

at the top,

and

on the next line, and
so forth. Such a table of binomial coefﬁcients is called Pascal’s triangle.
C.1-9
Prove that
n
X
iD1
i D

n C 1
!
:
C.1-10
Show that for any integers n  0 and 0  k  n, the expression

n
k

achieves its
maximum value when k D bn=2c or k D dn=2e.
C.1-11
?
Argue that for any integers n  0, j  0, k  0, and j C k  n,

n
j C k
!


n
j
!
n  j
k
!
:
(C.9)

C.2
Probability
Provide both an algebraic proof and an argument based on a method for choosing
j C k items out of n. Give an example in which equality does not hold.
C.1-12
?
Use induction on all integers k such that 0  k  n=2 to prove inequality (C.6),
and use equation (C.3) to extend it to all integers k such that 0  k  n.
C.1-13
?
Use Stirling’s approximation to prove that

2n
n
!
D
22n
pn.1 C O.1=n// :
(C.10)
C.1-14
?
By differentiating the entropy function H./, show that it achieves its maximum
value at  D 1=2. What is H.1=2/?
C.1-15
?
Show that for any integer n  0,
n
X
kD0

n
k
!
k D n2n1 :
(C.11)
C.2
Probability
Probability is an essential tool for the design and analysis of probabilistic and randomized algorithms. This section reviews basic probability theory.
We deﬁne probability in terms of a sample space S, which is a set whose elements are called elementary events. We can think of each elementary event as a
possible outcome of an experiment. For the experiment of ﬂipping two distinguishable coins, with each individual ﬂip resulting in a head (H) or a tail (T), we can view
the sample space as consisting of the set of all possible 2-strings over fH; Tg:
S D fHH; HT; TH; TTg :

Appendix C
Counting and Probability
An event is a subset1 of the sample space S. For example, in the experiment of
ﬂipping two coins, the event of obtaining one head and one tail is fHT; THg. The
event S is called the certain event, and the event ; is called the null event. We say
that two events A and B are mutually exclusive if A\B D ;. We sometimes treat
an elementary event s 2 S as the event fsg. By deﬁnition, all elementary events
are mutually exclusive.
Axioms of probability
A probability distribution Pr fg on a sample space S is a mapping from events of S
to real numbers satisfying the following probability axioms:
1. Pr fAg  0 for any event A.
2. Pr fSg D 1.
3. Pr fA [ Bg D Pr fAg C Pr fBg for any two mutually exclusive events A
and B. More generally, for any (ﬁnite or countably inﬁnite) sequence of events
A1; A2; : : : that are pairwise mutually exclusive,
Pr
([
i
Ai
)
D
X
i
Pr fAig :
We call Pr fAg the probability of the event A. We note here that axiom 2 is a
normalization requirement: there is really nothing fundamental about choosing 1
as the probability of the certain event, except that it is natural and convenient.
Several results follow immediately from these axioms and basic set theory (see
Section B.1). The null event ; has probability Pr f;g D 0. If A  B, then
Pr fAg  Pr fBg. Using A to denote the event S  A (the complement of A),
we have Pr
˚
A

D 1  Pr fAg. For any two events A and B,
Pr fA [ Bg
D
Pr fAg C Pr fBg  Pr fA \ Bg
(C.12)

Pr fAg C Pr fBg :
(C.13)
1For a general probability distribution, there may be some subsets of the sample space S that are not
considered to be events. This situation usually arises when the sample space is uncountably inﬁnite.
The main requirement for what subsets are events is that the set of events of a sample space be closed
under the operations of taking the complement of an event, forming the union of a ﬁnite or countable
number of events, and taking the intersection of a ﬁnite or countable number of events. Most of
the probability distributions we shall see are over ﬁnite or countable sample spaces, and we shall
generally consider all subsets of a sample space to be events. A notable exception is the continuous
uniform probability distribution, which we shall see shortly.

C.2
Probability
In our coin-ﬂipping example, suppose that each of the four elementary events
has probability 1=4. Then the probability of getting at least one head is
Pr fHH; HT; THg
D
Pr fHHg C Pr fHTg C Pr fTHg
D
3=4 :
Alternatively, since the probability of getting strictly less than one head is
Pr fTTg D 1=4, the probability of getting at least one head is 1  1=4 D 3=4.
Discrete probability distributions
A probability distribution is discrete if it is deﬁned over a ﬁnite or countably inﬁnite
sample space. Let S be the sample space. Then for any event A,
Pr fAg D
X
s2A
Pr fsg ;
since elementary events, speciﬁcally those in A, are mutually exclusive. If S is
ﬁnite and every elementary event s 2 S has probability
Pr fsg D 1= jSj ;
then we have the uniform probability distribution on S. In such a case the experiment is often described as “picking an element of S at random.”
As an example, consider the process of ﬂipping a fair coin, one for which the
probability of obtaining a head is the same as the probability of obtaining a tail, that
is, 1=2. If we ﬂip the coin n times, we have the uniform probability distribution
deﬁned on the sample space S D fH; Tgn, a set of size 2n. We can represent each
elementary event in S as a string of length n over fH; Tg, each string occurring with
probability 1=2n. The event
A D fexactly k heads and exactly n  k tails occurg
is a subset of S of size jAj D

n
k

, since

n
k

strings of length n over fH; Tg contain
exactly k H’s. The probability of event A is thus Pr fAg D

n
k

=2n.
Continuous uniform probability distribution
The continuous uniform probability distribution is an example of a probability
distribution in which not all subsets of the sample space are considered to be
events. The continuous uniform probability distribution is deﬁned over a closed
interval Œa; b of the reals, where a < b. Our intuition is that each point in the interval Œa; b should be “equally likely.” There are an uncountable number of points,
however, so if we give all points the same ﬁnite, positive probability, we cannot simultaneously satisfy axioms 2 and 3. For this reason, we would like to associate a

Appendix C
Counting and Probability
probability only with some of the subsets of S, in such a way that the axioms are
satisﬁed for these events.
For any closed interval Œc; d, where a  c  d  b, the continuous uniform
probability distribution deﬁnes the probability of the event Œc; d to be
Pr fŒc; dg D d  c
b  a :
Note that for any point x D Œx; x, the probability of x is 0.
If we remove
the endpoints of an interval Œc; d, we obtain the open interval .c; d/.
Since
Œc; d D Œc; c [ .c; d/ [ Œd; d, axiom 3 gives us Pr fŒc; dg D Pr f.c; d/g. Generally, the set of events for the continuous uniform probability distribution contains
any subset of the sample space Œa; b that can be obtained by a ﬁnite or countable
union of open and closed intervals, as well as certain more complicated sets.
Conditional probability and independence
Sometimes we have some prior partial knowledge about the outcome of an experiment. For example, suppose that a friend has ﬂipped two fair coins and has told
you that at least one of the coins showed a head. What is the probability that both
coins are heads? The information given eliminates the possibility of two tails. The
three remaining elementary events are equally likely, so we infer that each occurs
with probability 1=3. Since only one of these elementary events shows two heads,
the answer to our question is 1=3.
Conditional probability formalizes the notion of having prior partial knowledge
of the outcome of an experiment. The conditional probability of an event A given
that another event B occurs is deﬁned to be
Pr fA j Bg D Pr fA \ Bg
Pr fBg
(C.14)
whenever Pr fBg ¤ 0. (We read “Pr fA j Bg” as “the probability of A given B.”)
Intuitively, since we are given that event B occurs, the event that A also occurs
is A \ B. That is, A \ B is the set of outcomes in which both A and B occur.
Because the outcome is one of the elementary events in B, we normalize the probabilities of all the elementary events in B by dividing them by Pr fBg, so that they
sum to 1. The conditional probability of A given B is, therefore, the ratio of the
probability of event A \ B to the probability of event B. In the example above, A
is the event that both coins are heads, and B is the event that at least one coin is a
head. Thus, Pr fA j Bg D .1=4/=.3=4/ D 1=3.
Two events are independent if
Pr fA \ Bg D Pr fAg Pr fBg ;
(C.15)
which is equivalent, if Pr fBg ¤ 0, to the condition

C.2
Probability
Pr fA j Bg D Pr fAg :
For example, suppose that we ﬂip two fair coins and that the outcomes are independent. Then the probability of two heads is .1=2/.1=2/ D 1=4. Now suppose
that one event is that the ﬁrst coin comes up heads and the other event is that the
coins come up differently. Each of these events occurs with probability 1=2, and
the probability that both events occur is 1=4; thus, according to the deﬁnition of
independence, the events are independent—even though you might think that both
events depend on the ﬁrst coin. Finally, suppose that the coins are welded together so that they both fall heads or both fall tails and that the two possibilities are
equally likely. Then the probability that each coin comes up heads is 1=2, but the
probability that they both come up heads is 1=2 ¤ .1=2/.1=2/. Consequently, the
event that one comes up heads and the event that the other comes up heads are not
independent.
A collection A1; A2; : : : ; An of events is said to be pairwise independent if
Pr fAi \ Ajg D Pr fAig Pr fAjg
for all 1  i < j  n. We say that the events of the collection are (mutually)
independent if every k-subset Ai1; Ai2; : : : ; Aik of the collection, where 2  k  n
and 1  i1 < i2 <    < ik  n, satisﬁes
Pr fAi1 \ Ai2 \    \ Aikg D Pr fAi1g Pr fAi2g    Pr fAikg :
For example, suppose we ﬂip two fair coins. Let A1 be the event that the ﬁrst coin
is heads, let A2 be the event that the second coin is heads, and let A3 be the event
that the two coins are different. We have
Pr fA1g
D
1=2 ;
Pr fA2g
D
1=2 ;
Pr fA3g
D
1=2 ;
Pr fA1 \ A2g
D
1=4 ;
Pr fA1 \ A3g
D
1=4 ;
Pr fA2 \ A3g
D
1=4 ;
Pr fA1 \ A2 \ A3g
D
0 :
Since for 1  i < j  3, we have Pr fAi \ Ajg D Pr fAig Pr fAjg D 1=4, the
events A1, A2, and A3 are pairwise independent. The events are not mutually independent, however, because Pr fA1 \ A2 \ A3g D 0 and Pr fA1g Pr fA2g Pr fA3g D
1=8 ¤ 0.

Appendix C
Counting and Probability
Bayes’s theorem
From the deﬁnition of conditional probability (C.14) and the commutative law
A \ B D B \ A, it follows that for two events A and B, each with nonzero
probability,
Pr fA \ Bg
D
Pr fBg Pr fA j Bg
(C.16)
D
Pr fAg Pr fB j Ag :
Solving for Pr fA j Bg, we obtain
Pr fA j Bg D Pr fAg Pr fB j Ag
Pr fBg
;
(C.17)
which is known as Bayes’s theorem. The denominator Pr fBg is a normalizing
constant, which we can reformulate as follows. Since B D .B \ A/ [ .B \ A/,
and since B \ A and B \ A are mutually exclusive events,
Pr fBg
D
Pr fB \ Ag C Pr
˚
B \ A

D
Pr fAg Pr fB j Ag C Pr
˚
A

Pr
˚
B j A

:
Substituting into equation (C.17), we obtain an equivalent form of Bayes’s theorem:
Pr fA j Bg D
Pr fAg Pr fB j Ag
Pr fAg Pr fB j Ag C Pr
˚
A

Pr
˚
B j A

:
(C.18)
Bayes’s theorem can simplify the computing of conditional probabilities. For
example, suppose that we have a fair coin and a biased coin that always comes up
heads. We run an experiment consisting of three independent events: we choose
one of the two coins at random, we ﬂip that coin once, and then we ﬂip it again.
Suppose that the coin we have chosen comes up heads both times. What is the
probability that it is biased?
We solve this problem using Bayes’s theorem. Let A be the event that we choose
the biased coin, and let B be the event that the chosen coin comes up heads both
times. We wish to determine Pr fA j Bg. We have Pr fAg D 1=2, Pr fB j Ag D 1,
Pr
˚
A

D 1=2, and Pr
˚
B j A

D 1=4; hence,
Pr fA j Bg
D
.1=2/  1
.1=2/  1 C .1=2/  .1=4/
D
4=5 :

## Exercises

C.2-1
Professor Guildenstern ﬂips a fair
?
coin twice. What is the probability that Professor Rosencrantz obtains more heads
Professor Rosencrantz ﬂips a fair coin once.
than Professor Guildenstern

C.2
Probability
C.2-2
Prove Boole’s inequality: For any ﬁnite or countably inﬁnite sequence of events
A1; A2; : : :,
Pr fA1 [ A2 [   g  Pr fA1g C Pr fA2g C    :
(C.19)
C.2-3
Suppose we shufﬂe a deck of 10 cards, each bearing a distinct number from 1 to 10,
to mix the cards thoroughly. We then remove three cards, one at a time, from the
deck. What is the probability that we select the three cards in sorted (increasing)
order?
C.2-4
Prove that
Pr fA j Bg C Pr
˚
A j B

D 1 :
C.2-5
Prove that for any collection of events A1; A2; : : : ; An,
Pr fA1 \ A2 \    \ Ang D Pr fA1g  Pr fA2 j A1g  Pr fA3 j A1 \ A2g   
Pr fAn j A1 \ A2 \    \ An1g :
C.2-6
?
Describe a procedure that takes as input two integers a and b such that 0 < a < b
and, using fair coin ﬂips, produces as output heads with probability a=b and tails
with probability .b  a/=b. Give a bound on the expected number of coin ﬂips,
which should be O.1/. (Hint: Represent a=b in binary.)
C.2-7
?
Show how to construct a set of n events that are pairwise independent but such that
no subset of k > 2 of them is mutually independent.
C.2-8
?
Two events A and B are conditionally independent, given C, if
Pr fA \ B j Cg D Pr fA j Cg  Pr fB j Cg :
Give a simple but nontrivial example of two events that are not independent but are
conditionally independent given a third event.
C.2-9
?
You are a contestant in a game show in which a prize is hidden behind one of
three curtains. You will win the prize if you select the correct curtain. After you

Appendix C
Counting and Probability
have picked one curtain but before the curtain is lifted, the emcee lifts one of the
other curtains, knowing that it will reveal an empty stage, and asks if you would
like to switch from your current selection to the remaining curtain. How would
your chances change if you switch? (This question is the celebrated Monty Hall
problem, named after a game-show host who often presented contestants with just
this dilemma.)
C.2-10
?
A prison warden has randomly picked one prisoner among three to go free. The
other two will be executed. The guard knows which one will go free but is forbidden to give any prisoner information regarding his status. Let us call the prisoners
X, Y , and Z. Prisoner X asks the guard privately which of Y or Z will be executed, arguing that since he already knows that at least one of them must die, the
guard won’t be revealing any information about his own status. The guard tells X
that Y is to be executed. Prisoner X feels happier now, since he ﬁgures that either
he or prisoner Z will go free, which means that his probability of going free is
now 1=2. Is he right, or are his chances still 1=3? Explain.
C.3
Discrete random variables
A (discrete) random variable X is a function from a ﬁnite or countably inﬁnite
sample space S to the real numbers. It associates a real number with each possible
outcome of an experiment, which allows us to work with the probability distribution induced on the resulting set of numbers. Random variables can also be deﬁned
for uncountably inﬁnite sample spaces, but they raise technical issues that are unnecessary to address for our purposes. Henceforth, we shall assume that random
variables are discrete.
For a random variable X and a real number x, we deﬁne the event X D x to be
fs 2 S W X.s/ D xg; thus,
Pr fX D xg D
X
s2SWX.s/Dx
Pr fsg :
The function
f .x/ D Pr fX D xg
is the probability density function of the random variable X. From the probability
axioms, Pr fX D xg  0 and P
x Pr fX D xg D 1.
As an example, consider the experiment of rolling a pair of ordinary, 6-sided
dice. There are 36 possible elementary events in the sample space. We assume

C.3
Discrete random variables
that the probability distribution is uniform, so that each elementary event s 2 S is
equally likely: Pr fsg D 1=36. Deﬁne the random variable X to be the maximum of
the two values showing on the dice. We have Pr fX D 3g D 5=36, since X assigns
a value of 3 to 5 of the 36 possible elementary events, namely, .1; 3/, .2; 3/, .3; 3/,
.3; 2/, and .3; 1/.
We often deﬁne several random variables on the same sample space. If X and Y
are random variables, the function
f .x; y/ D Pr fX D x and Y D yg
is the joint probability density function of X and Y . For a ﬁxed value y,
Pr fY D yg D
X
x
Pr fX D x and Y D yg ;
and similarly, for a ﬁxed value x,
Pr fX D xg D
X
y
Pr fX D x and Y D yg :
Using the deﬁnition (C.14) of conditional probability, we have
Pr fX D x j Y D yg D Pr fX D x and Y D yg
Pr fY D yg
:
We deﬁne two random variables X and Y to be independent if for all x and y, the
events X D x and Y D y are independent or, equivalently, if for all x and y, we
have Pr fX D x and Y D yg D Pr fX D xg Pr fY D yg.
Given a set of random variables deﬁned over the same sample space, we can
deﬁne new random variables as sums, products, or other functions of the original
variables.
Expected value of a random variable
The simplest and most useful summary of the distribution of a random variable is
the “average” of the values it takes on. The expected value (or, synonymously,
expectation or mean) of a discrete random variable X is
E ŒX D
X
x
x  Pr fX D xg ;
(C.20)
which is well deﬁned if the sum is ﬁnite or converges absolutely. Sometimes the
expectation of X is denoted by
X or, when the random variable is apparent from
context, simply by
.
Consider a game in which you ﬂip two fair coins. You earn $3 for each head but
lose $2 for each tail. The expected value of the random variable X representing

Appendix C
Counting and Probability
your earnings is
E ŒX
D
6  Pr f2 H’sg C 1  Pr f1 H, 1 Tg  4  Pr f2 T’sg
D
6.1=4/ C 1.1=2/  4.1=4/
D
1 :
The expectation of the sum of two random variables is the sum of their expectations, that is,
E ŒX C Y  D E ŒX C E ŒY  ;
(C.21)
whenever E ŒX and E ŒY  are deﬁned. We call this property linearity of expectation, and it holds even if X and Y are not independent. It also extends to ﬁnite and
absolutely convergent summations of expectations. Linearity of expectation is the
key property that enables us to perform probabilistic analyses by using indicator
random variables (see Section 5.2).
If X is any random variable, any function g.x/ deﬁnes a new random variable g.X/. If the expectation of g.X/ is deﬁned, then
E Œg.X/ D
X
x
g.x/  Pr fX D xg :
Letting g.x/ D ax, we have for any constant a,
E ŒaX D aE ŒX :
(C.22)
Consequently, expectations are linear: for any two random variables X and Y and
any constant a,
E ŒaX C Y  D aE ŒX C E ŒY  :
(C.23)
When two random variables X and Y are independent and each has a deﬁned
expectation,
E ŒXY 
D
X
x
X
y
xy  Pr fX D x and Y D yg
D
X
x
X
y
xy  Pr fX D xg Pr fY D yg
D
X
x
x  Pr fX D xg
!  X
y
y  Pr fY D yg
!
D
E ŒX E ŒY  :
In general, when n random variables X1; X2; : : : ; Xn are mutually independent,
E ŒX1X2    Xn D E ŒX1 E ŒX2    E ŒXn :
(C.24)

C.3
Discrete random variables
When a random variable X takes on values from the set of natural numbers
N D f0; 1; 2; : : :g, we have a nice formula for its expectation:
E ŒX
D
X
iD0
i  Pr fX D ig
D
X
iD0
i.Pr fX  ig  Pr fX  i C 1g/
D
X
iD1
Pr fX  ig ;
(C.25)
since each term Pr fX  ig is added in i times and subtracted out i  1 times
(except Pr fX  0g, which is added in 0 times and not subtracted out at all).
When we apply a convex function f .x/ to a random variable X, Jensen’s inequality gives us
E Œf .X/  f .E ŒX/ ;
(C.26)
provided that the expectations exist and are ﬁnite. (A function f .x/ is convex
if for all x and y and for all 0    1, we have f .x C .1  /y/ 
f .x/ C .1  /f .y/.)
Variance and standard deviation
The expected value of a random variable does not tell us how “spread out” the
variable’s values are. For example, if we have random variables X and Y for which
Pr fX D 1=4g D Pr fX D 3=4g D 1=2 and Pr fY D 0g D Pr fY D 1g D 1=2,
then both E ŒX and E ŒY  are 1=2, yet the actual values taken on by Y are farther
from the mean than the actual values taken on by X.
The notion of variance mathematically expresses how far from the mean a random variable’s values are likely to be. The variance of a random variable X with
mean E ŒX is
Var ŒX
D
E

.X  E ŒX/2
D
E

X 2  2XE ŒX C E2 ŒX

D
E

X 2
 2E ŒXE ŒX C E2 ŒX
D
E

X 2
 2E2 ŒX C E2 ŒX
D
E

X 2
 E2 ŒX :
(C.27)
To justify the equality E ŒE2 ŒX D E2 ŒX, note that because E ŒX is a real number and not a random variable, so is E2 ŒX. The equality E ŒXE ŒX D E2 ŒX

Appendix C
Counting and Probability
follows from equation (C.22), with a D E ŒX. Rewriting equation (C.27) yields
an expression for the expectation of the square of a random variable:
E

X 2
D Var ŒX C E2 ŒX :
(C.28)
The variance of a random variable X and the variance of aX are related (see
Exercise C.3-10):
Var ŒaX D a2Var ŒX :
When X and Y are independent random variables,
Var ŒX C Y  D Var ŒX C Var ŒY  :
In general, if n random variables X1; X2; : : : ; Xn are pairwise independent, then
Var
" n
X
iD1
Xi
#
D
n
X
iD1
Var ŒXi :
(C.29)
The standard deviation of a random variable X is the nonnegative square root
of the variance of X. The standard deviation of a random variable X is sometimes
denoted 	X or simply 	 when the random variable X is understood from context.
With this notation, the variance of X is denoted 	 2.

## Exercises

C.3-1
Suppose we roll two ordinary, 6-sided dice. What is the expectation of the sum
of the two values showing? What is the expectation of the maximum of the two
values showing?
C.3-2
An array AŒ1 : : n contains n distinct numbers that are randomly ordered, with each
permutation of the n numbers being equally likely. What is the expectation of the
index of the maximum element in the array? What is the expectation of the index
of the minimum element in the array?
C.3-3
A carnival game consists of three dice in a cage. A player can bet a dollar on any
of the numbers 1 through 6. The cage is shaken, and the payoff is as follows. If the
player’s number doesn’t appear on any of the dice, he loses his dollar. Otherwise,
if his number appears on exactly k of the three dice, for k D 1; 2; 3, he keeps his
dollar and wins k more dollars. What is his expected gain from playing the carnival
game once?

C.4
The geometric and binomial distributions
C.3-4
Argue that if X and Y are nonnegative random variables, then
E Œmax.X; Y /  E ŒX C E ŒY  :
C.3-5
?
Let X and Y be independent random variables. Prove that f .X/ and g.Y / are
independent for any choice of functions f and g.
C.3-6
?
Let X be a nonnegative random variable, and suppose that E ŒX is well deﬁned.
Prove Markov’s inequality:
Pr fX  tg  E ŒX =t
(C.30)
for all t > 0.
C.3-7
?
Let S be a sample space, and let X and X 0 be random variables such that
X.s/  X 0.s/ for all s 2 S. Prove that for any real constant t,
Pr fX  tg  Pr fX 0  tg :
C.3-8
Which is larger: the expectation of the square of a random variable, or the square
of its expectation?
C.3-9
Show that for any random variable X that takes on only the values 0 and 1, we have
Var ŒX D E ŒX E Œ1  X.
C.3-10
Prove that Var ŒaX D a2Var ŒX from the deﬁnition (C.27) of variance.
C.4
The geometric and binomial distributions
We can think of a coin ﬂip as an instance of a Bernoulli trial, which is an experiment with only two possible outcomes: success, which occurs with probability p,
and failure, which occurs with probability q D 1p. When we speak of Bernoulli
trials collectively, we mean that the trials are mutually independent and, unless we
speciﬁcally say otherwise, that each has the same probability p for success. Two

Appendix C
Counting and Probability
0.05
0.10
0.15
0.20
0.25
9 10 11 12 13 14 15
0.30
0.35
k
2
k1 1

Figure C.1
A geometric distribution with probability p D 1=3 of success and a probability
q D 1  p of failure. The expectation of the distribution is 1=p D 3.
important distributions arise from Bernoulli trials: the geometric distribution and
the binomial distribution.
The geometric distribution
Suppose we have a sequence of Bernoulli trials, each with a probability p of success and a probability q D 1p of failure. How many trials occur before we obtain
a success? Let us deﬁne the random variable X be the number of trials needed to
obtain a success. Then X has values in the range f1; 2; : : :g, and for k  1,
Pr fX D kg D qk1p ;
(C.31)
since we have k  1 failures before the one success. A probability distribution satisfying equation (C.31) is said to be a geometric distribution. Figure C.1 illustrates
such a distribution.

C.4
The geometric and binomial distributions
Assuming that q < 1, we can calculate the expectation of a geometric distribution using identity (A.8):
E ŒX
D
X
kD1
kqk1p
D
p
q
X
kD0
kqk
D
p
q 
q
.1  q/2
D
p
q  q
p2
D
1=p :
(C.32)
Thus, on average, it takes 1=p trials before we obtain a success, an intuitive result.
The variance, which can be calculated similarly, but using Exercise A.1-3, is
Var ŒX D q=p2 :
(C.33)
As an example, suppose we repeatedly roll two dice until we obtain either a
seven or an eleven. Of the 36 possible outcomes, 6 yield a seven and 2 yield an
eleven. Thus, the probability of success is p D 8=36 D 2=9, and we must roll
1=p D 9=2 D 4:5 times on average to obtain a seven or eleven.
The binomial distribution
How many successes occur during n Bernoulli trials, where a success occurs with
probability p and a failure with probability q D 1  p? Deﬁne the random variable X to be the number of successes in n trials. Then X has values in the range
f0; 1; : : : ; ng, and for k D 0; 1; : : : ; n,
Pr fX D kg D

n
k
!
pkqnk ;
(C.34)
since there are

n
k

ways to pick which k of the n trials are successes, and the
probability that each occurs is pkqnk. A probability distribution satisfying equation (C.34) is said to be a binomial distribution. For convenience, we deﬁne the
family of binomial distributions using the notation
b.kI n; p/ D

n
k
!
pk.1  p/nk :
(C.35)
Figure C.2 illustrates a binomial distribution. The name “binomial” comes from the
right-hand side of equation (C.34) being the kth term of the expansion of .p Cq/n.
Consequently, since p C q D 1,

Appendix C
Counting and Probability
0.05
0.10
0.15
0.20
0.25
k
9 10 11 12 13 14 15
b (k; 15, 1/3)
Figure C.2
The binomial distribution b.kI 15; 1=3/ resulting from n D 15 Bernoulli trials, each
with probability p D 1=3 of success. The expectation of the distribution is np D 5.
n
X
kD0
b.kI n; p/ D 1 ;
(C.36)
as axiom 2 of the probability axioms requires.
We can compute the expectation of a random variable having a binomial distribution from equations (C.8) and (C.36). Let X be a random variable that follows
the binomial distribution b.kI n; p/, and let q D 1  p. By the deﬁnition of expectation, we have
E ŒX
D
n
X
kD0
k  Pr fX D kg
D
n
X
kD0
k  b.kI n; p/
D
n
X
kD1
k

n
k
!
pkqnk
D
np
n
X
kD1

n  1
k  1
!
pk1qnk
(by equation (C.8))
D
np
n1
X
kD0

n  1
k
!
pkq.n1/k

C.4
The geometric and binomial distributions
D
np
n1
X
kD0
b.kI n  1; p/
D
np
(by equation (C.36)) .
(C.37)
By using the linearity of expectation, we can obtain the same result with substantially less algebra. Let Xi be the random variable describing the number of
successes in the ith trial. Then E ŒXi D p  1 C q  0 D p, and by linearity of
expectation (equation (C.21)), the expected number of successes for n trials is
E ŒX
D
E
" n
X
iD1
Xi
#
D
n
X
iD1
E ŒXi
D
n
X
iD1
p
D
np :
(C.38)
We can use the same approach to calculate the variance of the distribution. Using
equation (C.27), we have Var ŒXi D E ŒX 2
i   E2 ŒXi. Since Xi only takes on the
values 0 and 1, we have X 2
i D Xi, which implies E ŒX 2
i  D E ŒXi D p. Hence,
Var ŒXi D p  p2 D p.1  p/ D pq :
(C.39)
To compute the variance of X, we take advantage of the independence of the n
trials; thus, by equation (C.29),
Var ŒX
D
Var
" n
X
iD1
Xi
#
D
n
X
iD1
Var ŒXi
D
n
X
iD1
pq
D
npq :
(C.40)
As Figure C.2 shows, the binomial distribution b.kI n; p/ increases with k until
it reaches the mean np, and then it decreases. We can prove that the distribution
always behaves in this manner by looking at the ratio of successive terms:

Appendix C
Counting and Probability
b.kI n; p/
b.k  1I n; p/
D

n
k

pkqnk

n
k1

pk1qnkC1
D
nŠ.k  1/Š.n  k C 1/Šp
kŠ.n  k/ŠnŠq
D
.n  k C 1/p
kq
(C.41)
D
1 C .n C 1/p  k
kq
:
This ratio is greater than 1 precisely when .n C 1/p  k is positive.
Consequently, b.kI n; p/ > b.k  1I n; p/ for k < .n C 1/p (the distribution increases),
and b.kI n; p/ < b.k  1I n; p/ for k > .n C 1/p (the distribution decreases).
If k D .n C 1/p is an integer, then b.kI n; p/ D b.k  1I n; p/, and so the distribution then has two maxima: at k D .nC1/p and at k1 D .nC1/p1 D np  q.
Otherwise, it attains a maximum at the unique integer k that lies in the range
np  q < k < .n C 1/p.
The following lemma provides an upper bound on the binomial distribution.
Lemma C.1
Let n  0, let 0 < p < 1, let q D 1  p, and let 0  k  n. Then
b.kI n; p/ 
np
k
k  nq
n  k
nk
:
Proof
Using equation (C.6), we have
b.kI n; p/
D

n
k
!
pkqnk

n
k
k 
n
n  k
nk
pkqnk
D
np
k
k  nq
n  k
nk
:

## Exercises

C.4-1
Verify axiom 2 of the probability axioms for the geometric distribution.
C.4-2
How many times on average must we ﬂip 6 fair coins before we obtain 3 heads
and 3 tails?

C.4
The geometric and binomial distributions
C.4-3
Show that b.kI n; p/ D b.n  kI n; q/, where q D 1  p.
C.4-4
Show that value of the maximum of the binomial distribution b.kI n; p/ is approximately 1=p2npq, where q D 1  p.
C.4-5
?
Show that the probability of no successes in n Bernoulli trials, each with probability
p D 1=n, is approximately 1=e. Show that the probability of exactly one success
is also approximately 1=e.
C.4-6
?
Professor Rosencrantz ﬂips a fair coin n times, and so does Professor Guildenstern.
Show that the probability that they get the same number of heads is

2n
n

=4n. (Hint:
For Professor Rosencrantz, call a head a success; for Professor Guildenstern, call
a tail a success.) Use your argument to verify the identity
n
X
kD0

n
k
!2
D

2n
n
!
:
C.4-7
?
Show that for 0  k  n,
b.kI n; 1=2/  2n H.k=n/n ;
where H.x/ is the entropy function (C.7).
C.4-8
?
Consider n Bernoulli trials, where for i D 1; 2; : : : ; n, the ith trial has probability pi of success, and let X be the random variable denoting the total number of
successes. Let p  pi for all i D 1; 2; : : : ; n. Prove that for 1  k  n,
Pr fX < kg 
k1
X
iD0
b.iI n; p/ :
C.4-9
?
Let X be the random variable for the total number of successes in a set A of n
Bernoulli trials, where the ith trial has a probability pi of success, and let X 0
be the random variable for the total number of successes in a second set A0 of n
Bernoulli trials, where the ith trial has a probability p0
i  pi of success. Prove that
for 0  k  n,

Appendix C
Counting and Probability
Pr fX 0  kg  Pr fX  kg :
(Hint: Show how to obtain the Bernoulli trials in A0 by an experiment involving
the trials of A, and use the result of Exercise C.3-7.)
?
C.5
The tails of the binomial distribution
The probability of having at least, or at most, k successes in n Bernoulli trials,
each with probability p of success, is often of more interest than the probability of
having exactly k successes. In this section, we investigate the tails of the binomial
distribution: the two regions of the distribution b.kI n; p/ that are far from the
mean np. We shall prove several important bounds on (the sum of all terms in) a
tail.
We ﬁrst provide a bound on the right tail of the distribution b.kI n; p/. We can
determine bounds on the left tail by inverting the roles of successes and failures.
Theorem C.2
Consider a sequence of n Bernoulli trials, where success occurs with probability p.
Let X be the random variable denoting the total number of successes. Then for
0  k  n, the probability of at least k successes is
Pr fX  kg
D
n
X
iDk
b.iI n; p/


n
k
!
pk :
Proof
For S  f1; 2; : : : ; ng, we let AS denote the event that the ith trial is a
success for every i 2 S. Clearly Pr fASg D pk if jSj D k. We have
Pr fX  kg
D
Pr fthere exists S  f1; 2; : : : ; ng W jSj D k and ASg
D
Pr

[
Sf1;2;:::;ngWjSjDk
AS


X
Sf1;2;:::;ngWjSjDk
Pr fASg
(by inequality (C.19))
D

n
k
!
pk :

C.5
The tails of the binomial distribution
The following corollary restates the theorem for the left tail of the binomial
distribution. In general, we shall leave it to you to adapt the proofs from one tail to
the other.
Corollary C.3
Consider a sequence of n Bernoulli trials, where success occurs with probability p. If X is the random variable denoting the total number of successes, then for
0  k  n, the probability of at most k successes is
Pr fX  kg
D
k
X
iD0
b.iI n; p/


n
n  k
!
.1  p/nk
D

n
k
!
.1  p/nk :
Our next bound concerns the left tail of the binomial distribution. Its corollary
shows that, far from the mean, the left tail diminishes exponentially.
Theorem C.4
Consider a sequence of n Bernoulli trials, where success occurs with probability p
and failure with probability q D 1  p. Let X be the random variable denoting the
total number of successes. Then for 0 < k < np, the probability of fewer than k
successes is
Pr fX < kg
D
k1
X
iD0
b.iI n; p/
<
kq
np  k b.kI n; p/ :
Proof
We bound the series Pk1
iD0 b.iI n; p/ by a geometric series using the technique from Section A.2, page 1151. For i D 1; 2; : : : ; k, we have from equation (C.41),
b.i  1I n; p/
b.iI n; p/
D
iq
.n  i C 1/p
<
iq
.n  i/p

kq
.n  k/p :

Appendix C
Counting and Probability
If we let
x
D
kq
.n  k/p
<
kq
.n  np/p
D
kq
nqp
D
k
np
<
1 ;
it follows that
b.i  1I n; p/ < x b.iI n; p/
for 0 < i  k. Iteratively applying this inequality k  i times, we obtain
b.iI n; p/ < xki b.kI n; p/
for 0  i < k, and hence
k1
X
iD0
b.iI n; p/
<
k1
X
iD0
xkib.kI n; p/
<
b.kI n; p/
X
iD0
xi
D
x
1  x b.kI n; p/
D
kq
np  k b.kI n; p/ :
Corollary C.5
Consider a sequence of n Bernoulli trials, where success occurs with probability p
and failure with probability q D 1  p. Then for 0 < k  np=2, the probability of
fewer than k successes is less than one half of the probability of fewer than k C 1
successes.
Proof
Because k  np=2, we have
kq
np  k

.np=2/q
np  .np=2/

C.5
The tails of the binomial distribution
D
.np=2/q
np=2

1 ;
(C.42)
since q  1. Letting X be the random variable denoting the number of successes,
Theorem C.4 and inequality (C.42) imply that the probability of fewer than k successes is
Pr fX < kg D
k1
X
iD0
b.iI n; p/ < b.kI n; p/ :
Thus we have
Pr fX < kg
Pr fX < k C 1g
D
Pk1
iD0 b.iI n; p/
Pk
iD0 b.iI n; p/
D
Pk1
iD0 b.iI n; p/
Pk1
iD0 b.iI n; p/ C b.kI n; p/
<
1=2 ;
since Pk1
iD0 b.iI n; p/ < b.kI n; p/.
Bounds on the right tail follow similarly. Exercise C.5-2 asks you to prove them.
Corollary C.6
Consider a sequence of n Bernoulli trials, where success occurs with probability p.
Let X be the random variable denoting the total number of successes. Then for
np < k < n, the probability of more than k successes is
Pr fX > kg
D
n
X
iDkC1
b.iI n; p/
<
.n  k/p
k  np b.kI n; p/ :
Corollary C.7
Consider a sequence of n Bernoulli trials, where success occurs with probability p
and failure with probability q D 1  p. Then for .np C n/=2 < k < n, the
probability of more than k successes is less than one half of the probability of
more than k  1 successes.
The next theorem considers n Bernoulli trials, each with a probability pi of
success, for i D 1; 2; : : : ; n. As the subsequent corollary shows, we can use the

Appendix C
Counting and Probability
theorem to provide a bound on the right tail of the binomial distribution by setting
pi D p for each trial.
Theorem C.8
Consider a sequence of n Bernoulli trials, where in the ith trial, for i D 1; 2; : : : ; n,
success occurs with probability pi and failure occurs with probability qi D 1  pi.
Let X be the random variable describing the total number of successes, and let

D E ŒX. Then for r >
,
Pr fX 
 rg 

e
r
r
:
Proof
Since for any ˛ > 0, the function e˛x is strictly increasing in x,
Pr fX 
 rg D Pr
˚
e˛.X
/  e˛r
;
(C.43)
where we will determine ˛ later. Using Markov’s inequality (C.30), we obtain
Pr
˚
e˛.X
/  e˛r
 E

e˛.X
/
e˛r :
(C.44)
The bulk of the proof consists of bounding E

e˛.X
/
and substituting a suitable value for ˛ in inequality (C.44). First, we evaluate E

e˛.X
/
. Using the
technique of indicator random variables (see Section 5.2), let Xi D I fthe ith
Bernoulli trial is a successg for i D 1; 2; : : : ; n; that is, Xi is the random variable that is 1 if the ith Bernoulli trial is a success and 0 if it is a failure. Thus,
X D
n
X
iD1
Xi ;
and by linearity of expectation,

D E ŒX D E
" n
X
iD1
Xi
#
D
n
X
iD1
E ŒXi D
n
X
iD1
pi ;
which implies
X 
D
n
X
iD1
.Xi  pi/ :
To evaluate E

e˛.X
/
, we substitute for X 
, obtaining
E

e˛.X
/
D
E

e˛ Pn
iD1.Xi pi/
D
E
" n
Y
iD1
e˛.Xi pi/
#
D
n
Y
iD1
E

e˛.Xi pi /
;

C.5
The tails of the binomial distribution
which follows from (C.24), since the mutual independence of the random variables Xi implies the mutual independence of the random variables e˛.Xi pi / (see
Exercise C.3-5). By the deﬁnition of expectation,
E

e˛.Xi pi /
D
e˛.1pi /pi C e˛.0pi /qi
D
pie˛qi C qie˛pi

pie˛ C 1
(C.45)

exp.pie˛/ ;
where exp.x/ denotes the exponential function: exp.x/ D ex. (Inequality (C.45)
follows from the inequalities ˛ > 0, qi  1, e˛qi  e˛, and e˛pi  1, and the last
line follows from inequality (3.12).) Consequently,
E

e˛.X
/
D
n
Y
iD1
E

e˛.Xi pi /

n
Y
iD1
exp.pie˛/
D
exp
n
X
iD1
pie˛
!
D
exp.
e˛/ ;
(C.46)
since
D Pn
iD1 pi. Therefore, from equation (C.43) and inequalities (C.44)
and (C.46), it follows that
Pr fX 
 rg  exp.
e˛  ˛r/ :
(C.47)
Choosing ˛ D ln.r=
/ (see Exercise C.5-7), we obtain
Pr fX 
 rg

exp.
eln.r=
/  r ln.r=
//
D
exp.r  r ln.r=
//
D
er
.r=
/r
D

e
r
r
:
When applied to Bernoulli trials in which each trial has the same probability of
success, Theorem C.8 yields the following corollary bounding the right tail of a
binomial distribution.

Appendix C
Counting and Probability
Corollary C.9
Consider a sequence of n Bernoulli trials, where in each trial success occurs with
probability p and failure occurs with probability q D 1  p. Then for r > np,
Pr fX  np  rg
D
n
X
kDdnpCre
b.kI n; p/

npe
r
r
:
Proof
By equation (C.37), we have
D E ŒX D np.

## Exercises

C.5-1
?
Which is less likely: obtaining no heads when you ﬂip a fair coin n times, or
obtaining fewer than n heads when you ﬂip the coin 4n times?
C.5-2
?
Prove Corollaries C.6 and C.7.
C.5-3
?
Show that
k1
X
iD0

n
i
!
ai < .a C 1/n
k
na  k.a C 1/ b.kI n; a=.a C 1//
for all a > 0 and all k such that 0 < k < na=.a C 1/.
C.5-4
?
Prove that if 0 < k < np, where 0 < p < 1 and q D 1  p, then
k1
X
iD0
piqni <
kq
np  k
np
k
k  nq
n  k
nk
:
C.5-5
?
Show that the conditions of Theorem C.8 imply that
Pr f
 X  rg 
.n 
/e
r
r
:
Similarly, show that the conditions of Corollary C.9 imply that
Pr fnp  X  rg 
nqe
r
r
:

Problems for Appendix C
C.5-6
?
Consider a sequence of n Bernoulli trials, where in the ith trial, for i D 1; 2; : : : ; n,
success occurs with probability pi and failure occurs with probability qi D 1  pi.
Let X be the random variable describing the total number of successes, and let

D E ŒX. Show that for r  0,
Pr fX 
 rg  er2=2n :
(Hint: Prove that pie˛qi C qie˛pi  e˛2=2. Then follow the outline of the proof
of Theorem C.8, using this inequality in place of inequality (C.45).)
C.5-7
?
Show that choosing ˛ D ln.r=
/ minimizes the right-hand side of inequality (C.47).

## Problems

C-1
Balls and bins
In this problem, we investigate the effect of various assumptions on the number of
ways of placing n balls into b distinct bins.
a. Suppose that the n balls are distinct and that their order within a bin does not
matter. Argue that the number of ways of placing the balls in the bins is bn.
b. Suppose that the balls are distinct and that the balls in each bin are ordered.
Prove that there are exactly .b C n  1/Š=.b  1/Š ways to place the balls in the
bins. (Hint: Consider the number of ways of arranging n distinct balls and b1
indistinguishable sticks in a row.)
c. Suppose that the balls are identical, and hence their order within a bin does not
matter. Show that the number of ways of placing the balls in the bins is

bCn1
n

.
(Hint: Of the arrangements in part (b), how many are repeated if the balls are
made identical?)
d. Suppose that the balls are identical and that no bin may contain more than one
ball, so that n  b. Show that the number of ways of placing the balls is

b
n

.
e. Suppose that the balls are identical and that no bin may be left empty. Assuming
that n  b, show that the number of ways of placing the balls is

n1
b1

.

Appendix C
Counting and Probability
Appendix notes
The ﬁrst general methods for solving probability problems were discussed in a
famous correspondence between B. Pascal and P. de Fermat, which began in 1654,
and in a book by C. Huygens in 1657. Rigorous probability theory began with the
work of J. Bernoulli in 1713 and A. De Moivre in 1730. Further developments of
the theory were provided by P.-S. Laplace, S.-D. Poisson, and C. F. Gauss.
Sums of random variables were originally studied by P. L. Chebyshev and A. A.
Markov. A. N. Kolmogorov axiomatized probability theory in 1933. Chernoff [66]
and Hoeffding [173] provided bounds on the tails of distributions. Seminal work
in random combinatorial structures was done by P. Erd¨os.
Knuth [209] and Liu [237] are good references for elementary combinatorics
and counting. Standard textbooks such as Billingsley [46], Chung [67], Drake [95],
Feller [104], and Rozanov [300] offer comprehensive introductions to probability.
