# 7 Quicksort

7
Quicksort
The quicksort algorithm has a worst-case running time of ‚.n2/ on an input array
of n numbers. Despite this slow worst-case running time, quicksort is often the best
practical choice for sorting because it is remarkably efﬁcient on the average: its
expected running time is ‚.n lg n/, and the constant factors hidden in the ‚.n lg n/
notation are quite small. It also has the advantage of sorting in place (see page 17),
and it works well even in virtual-memory environments.
Section 7.1 describes the algorithm and an important subroutine used by quick-
sort for partitioning. Because the behavior of quicksort is complex, we start with
an intuitive discussion of its performance in Section 7.2 and postpone its precise
analysis to the end of the chapter. Section 7.3 presents a version of quicksort that
uses random sampling. This algorithm has a good expected running time, and no
particular input elicits its worst-case behavior. Section 7.4 analyzes the random-
ized algorithm, showing that it runs in ‚.n2/ time in the worst case and, assuming
distinct elements, in expected O.n lg n/ time.
7.1
Description of quicksort
Quicksort, like merge sort, applies the divide-and-conquer paradigm introduced
in Section 2.3.1. Here is the three-step divide-and-conquer process for sorting a
typical subarray AŒp : : r:
Divide: Partition (rearrange) the array AŒp : : r into two (possibly empty) subar-
rays AŒp : : q  1 and AŒq C 1 : : r such that each element of AŒp : : q  1 is
less than or equal to AŒq, which is, in turn, less than or equal to each element
of AŒq C 1 : : r. Compute the index q as part of this partitioning procedure.
Conquer: Sort the two subarrays AŒp : : q 1 and AŒq C1 : : r by recursive calls
to quicksort.

7.1
Description of quicksort
171
Combine: Because the subarrays are already sorted, no work is needed to combine
them: the entire array AŒp : : r is now sorted.
The following procedure implements quicksort:
QUICKSORT.A; p; r/
1
if p < r
2
q D PARTITION.A; p; r/
3
QUICKSORT.A; p; q  1/
4
QUICKSORT.A; q C 1; r/
To sort an entire array A, the initial call is QUICKSORT.A; 1; A:length/.
Partitioning the array
The key to the algorithm is the PARTITION procedure, which rearranges the subar-
ray AŒp : : r in place.
PARTITION.A; p; r/
1
x D AŒr
2
i D p  1
3
for j D p to r  1
4
if AŒj   x
5
i D i C 1
6
exchange AŒi with AŒj 
7
exchange AŒi C 1 with AŒr
8
return i C 1
Figure 7.1 shows how PARTITION works on an 8-element array. PARTITION
always selects an element x D AŒr as a pivot element around which to partition the
subarray AŒp : : r. As the procedure runs, it partitions the array into four (possibly
empty) regions. At the start of each iteration of the for loop in lines 3–6, the regions
satisfy certain properties, shown in Figure 7.2. We state these properties as a loop
invariant:
At the beginning of each iteration of the loop of lines 3–6, for any array
index k,
1. If p  k  i, then AŒk  x.
2. If i C 1  k  j  1, then AŒk > x.
3. If k D r, then AŒk D x.

172
Chapter 7
Quicksort
2
8
7
1
3
5
6
4
p,j
r
i
(a)
2
8
7
1
3
5
6
4
p,i
r
j
(b)
2
8
7
1
3
5
6
4
p,i
r
j
(c)
2
8
7
1
3
5
6
4
p,i
r
j
(d)
2
8
7
1
3
5
6
4
p
r
j
(e)
i
2
8
7
1
3
5
6
4
p
r
j
(f)
i
2
8
7
1
3
5
6
4
p
r
j
(g)
i
2
8
7
1
3
5
6
4
p
r
(h)
i
2
8
7
1
3
5
6
4
p
r
(i)
i
Figure 7.1
The operation of PARTITION on a sample array. Array entry AŒr becomes the pivot
element x. Lightly shaded array elements are all in the ﬁrst partition with values no greater than x.
Heavily shaded elements are in the second partition with values greater than x. The unshaded el-
ements have not yet been put in one of the ﬁrst two partitions, and the ﬁnal white element is the
pivot x. (a) The initial array and variable settings. None of the elements have been placed in either
of the ﬁrst two partitions. (b) The value 2 is “swapped with itself” and put in the partition of smaller
values. (c)–(d) The values 8 and 7 are added to the partition of larger values. (e) The values 1 and 8
are swapped, and the smaller partition grows. (f) The values 3 and 7 are swapped, and the smaller
partition grows. (g)–(h) The larger partition grows to include 5 and 6, and the loop terminates. (i) In
lines 7–8, the pivot element is swapped so that it lies between the two partitions.
The indices between j and r  1 are not covered by any of the three cases, and the
values in these entries have no particular relationship to the pivot x.
We need to show that this loop invariant is true prior to the ﬁrst iteration, that
each iteration of the loop maintains the invariant, and that the invariant provides a
useful property to show correctness when the loop terminates.

7.1
Description of quicksort
173
≤x
> x
unrestricted
x
p
i
j
r
Figure 7.2
The four regions maintained by the procedure PARTITION on a subarray AŒp : : r. The
values in AŒp : : i are all less than or equal to x, the values in AŒi C 1 : : j  1 are all greater than x,
and AŒr D x. The subarray AŒj : : r  1 can take on any values.
Initialization: Prior to the ﬁrst iteration of the loop, i D p  1 and j D p. Be-
cause no values lie between p and i and no values lie between i C 1 and j  1,
the ﬁrst two conditions of the loop invariant are trivially satisﬁed. The assign-
ment in line 1 satisﬁes the third condition.
Maintenance: As Figure 7.3 shows, we consider two cases, depending on the
outcome of the test in line 4. Figure 7.3(a) shows what happens when AŒj  > x;
the only action in the loop is to increment j . After j is incremented, condition 2
holds for AŒj  1 and all other entries remain unchanged. Figure 7.3(b) shows
what happens when AŒj   x; the loop increments i, swaps AŒi and AŒj ,
and then increments j . Because of the swap, we now have that AŒi  x, and
condition 1 is satisﬁed. Similarly, we also have that AŒj  1 > x, since the
item that was swapped into AŒj  1 is, by the loop invariant, greater than x.
Termination: At termination, j D r. Therefore, every entry in the array is in one
of the three sets described by the invariant, and we have partitioned the values
in the array into three sets: those less than or equal to x, those greater than x,
and a singleton set containing x.
The ﬁnal two lines of PARTITION ﬁnish up by swapping the pivot element with
the leftmost element greater than x, thereby moving the pivot into its correct place
in the partitioned array, and then returning the pivot’s new index. The output of
PARTITION now satisﬁes the speciﬁcations given for the divide step. In fact, it
satisﬁes a slightly stronger condition: after line 2 of QUICKSORT, AŒq is strictly
less than every element of AŒq C 1 : : r.
The running time of PARTITION on the subarray AŒp : : r is ‚.n/, where
n D r  p C 1 (see Exercise 7.1-3).
Exercises
7.1-1
Using Figure 7.1 as a model, illustrate the operation of PARTITION on the array
A D h13; 19; 9; 5; 12; 8; 7; 4; 21; 2; 6; 11i.

174
Chapter 7
Quicksort
≤x
> x
x
p
i
j
r
>x
(a)
≤x
> x
x
p
i
j
r
≤x
> x
x
p
i
j
r
≤x
(b)
≤x
> x
x
p
i
j
r
Figure 7.3
The two cases for one iteration of procedure PARTITION. (a) If AŒj > x, the only
action is to increment j, which maintains the loop invariant. (b) If AŒj  x, index i is incremented,
AŒi and AŒj are swapped, and then j is incremented. Again, the loop invariant is maintained.
7.1-2
What value of q does PARTITION return when all elements in the array AŒp : : r
have the same value? Modify PARTITION so that q D b.p C r/=2c when all
elements in the array AŒp : : r have the same value.
7.1-3
Give a brief argument that the running time of PARTITION on a subarray of size n
is ‚.n/.
7.1-4
How would you modify QUICKSORT to sort into nonincreasing order?
7.2
Performance of quicksort
The running time of quicksort depends on whether the partitioning is balanced or
unbalanced, which in turn depends on which elements are used for partitioning.
If the partitioning is balanced, the algorithm runs asymptotically as fast as merge

7.2
Performance of quicksort
175
sort. If the partitioning is unbalanced, however, it can run asymptotically as slowly
as insertion sort. In this section, we shall informally investigate how quicksort
performs under the assumptions of balanced versus unbalanced partitioning.
Worst-case partitioning
The worst-case behavior for quicksort occurs when the partitioning routine pro-
duces one subproblem with n  1 elements and one with 0 elements. (We prove
this claim in Section 7.4.1.) Let us assume that this unbalanced partitioning arises
in each recursive call. The partitioning costs ‚.n/ time. Since the recursive call
on an array of size 0 just returns, T .0/ D ‚.1/, and the recurrence for the running
time is
T .n/
D
T .n  1/ C T .0/ C ‚.n/
D
T .n  1/ C ‚.n/ :
Intuitively, if we sum the costs incurred at each level of the recursion, we get
an arithmetic series (equation (A.2)), which evaluates to ‚.n2/.
Indeed, it is
straightforward to use the substitution method to prove that the recurrence T .n/ D
T .n  1/ C ‚.n/ has the solution T .n/ D ‚.n2/. (See Exercise 7.2-1.)
Thus, if the partitioning is maximally unbalanced at every recursive level of the
algorithm, the running time is ‚.n2/. Therefore the worst-case running time of
quicksort is no better than that of insertion sort. Moreover, the ‚.n2/ running time
occurs when the input array is already completely sorted—a common situation in
which insertion sort runs in O.n/ time.
Best-case partitioning
In the most even possible split, PARTITION produces two subproblems, each of
size no more than n=2, since one is of size bn=2c and one of size dn=2e1. In this
case, quicksort runs much faster. The recurrence for the running time is then
T .n/ D 2T .n=2/ C ‚.n/ ;
where we tolerate the sloppiness from ignoring the ﬂoor and ceiling and from sub-
tracting 1. By case 2 of the master theorem (Theorem 4.1), this recurrence has the
solution T .n/ D ‚.n lg n/. By equally balancing the two sides of the partition at
every level of the recursion, we get an asymptotically faster algorithm.
Balanced partitioning
The average-case running time of quicksort is much closer to the best case than to
the worst case, as the analyses in Section 7.4 will show. The key to understand-

176
Chapter 7
Quicksort
n
cn
cn
cn
cn
 cn
 cn
1
1
O.n lg n/
log10 n
log10=9 n
1
10 n
9
10 n
1
100 n
9
100 n
9
100 n
81
100 n
81
1000 n
729
1000 n
Figure 7.4
A recursion tree for QUICKSORT in which PARTITION always produces a 9-to-1 split,
yielding a running time of O.n lg n/. Nodes show subproblem sizes, with per-level costs on the right.
The per-level costs include the constant c implicit in the ‚.n/ term.
ing why is to understand how the balance of the partitioning is reﬂected in the
recurrence that describes the running time.
Suppose, for example, that the partitioning algorithm always produces a 9-to-1
proportional split, which at ﬁrst blush seems quite unbalanced. We then obtain the
recurrence
T .n/ D T .9n=10/ C T .n=10/ C cn ;
on the running time of quicksort, where we have explicitly included the constant c
hidden in the ‚.n/ term. Figure 7.4 shows the recursion tree for this recurrence.
Notice that every level of the tree has cost cn, until the recursion reaches a bound-
ary condition at depth log10 n D ‚.lg n/, and then the levels have cost at most cn.
The recursion terminates at depth log10=9 n D ‚.lg n/. The total cost of quick-
sort is therefore O.n lg n/. Thus, with a 9-to-1 proportional split at every level of
recursion, which intuitively seems quite unbalanced, quicksort runs in O.n lg n/
time—asymptotically the same as if the split were right down the middle. Indeed,
even a 99-to-1 split yields an O.n lg n/ running time. In fact, any split of constant
proportionality yields a recursion tree of depth ‚.lg n/, where the cost at each level
is O.n/. The running time is therefore O.n lg n/ whenever the split has constant
proportionality.

7.2
Performance of quicksort
177
n
0
n–1
(n–1)/2 – 1
(n–1)/2
n
(n–1)/2
(a)
(b)
(n–1)/2
Θ(n)
Θ(n)
Figure 7.5
(a) Two levels of a recursion tree for quicksort. The partitioning at the root costs n
and produces a “bad” split: two subarrays of sizes 0 and n  1. The partitioning of the subarray of
size n  1 costs n  1 and produces a “good” split: subarrays of size .n  1/=2  1 and .n  1/=2.
(b) A single level of a recursion tree that is very well balanced. In both parts, the partitioning cost for
the subproblems shown with elliptical shading is ‚.n/. Yet the subproblems remaining to be solved
in (a), shown with square shading, are no larger than the corresponding subproblems remaining to be
solved in (b).
Intuition for the average case
To develop a clear notion of the randomized behavior of quicksort, we must make
an assumption about how frequently we expect to encounter the various inputs.
The behavior of quicksort depends on the relative ordering of the values in the
array elements given as the input, and not by the particular values in the array. As
in our probabilistic analysis of the hiring problem in Section 5.2, we will assume
for now that all permutations of the input numbers are equally likely.
When we run quicksort on a random input array, the partitioning is highly un-
likely to happen in the same way at every level, as our informal analysis has as-
sumed. We expect that some of the splits will be reasonably well balanced and
that some will be fairly unbalanced. For example, Exercise 7.2-6 asks you to show
that about 80 percent of the time PARTITION produces a split that is more balanced
than 9 to 1, and about 20 percent of the time it produces a split that is less balanced
than 9 to 1.
In the average case, PARTITION produces a mix of “good” and “bad” splits. In a
recursion tree for an average-case execution of PARTITION, the good and bad splits
are distributed randomly throughout the tree. Suppose, for the sake of intuition,
that the good and bad splits alternate levels in the tree, and that the good splits
are best-case splits and the bad splits are worst-case splits. Figure 7.5(a) shows
the splits at two consecutive levels in the recursion tree. At the root of the tree,
the cost is n for partitioning, and the subarrays produced have sizes n  1 and 0:
the worst case. At the next level, the subarray of size n  1 undergoes best-case
partitioning into subarrays of size .n  1/=2  1 and .n  1/=2. Let’s assume that
the boundary-condition cost is 1 for the subarray of size 0.

178
Chapter 7
Quicksort
The combination of the bad split followed by the good split produces three sub-
arrays of sizes 0, .n  1/=2  1, and .n  1/=2 at a combined partitioning cost
of ‚.n/ C ‚.n  1/ D ‚.n/. Certainly, this situation is no worse than that in
Figure 7.5(b), namely a single level of partitioning that produces two subarrays of
size .n  1/=2, at a cost of ‚.n/. Yet this latter situation is balanced! Intuitively,
the ‚.n  1/ cost of the bad split can be absorbed into the ‚.n/ cost of the good
split, and the resulting split is good. Thus, the running time of quicksort, when lev-
els alternate between good and bad splits, is like the running time for good splits
alone: still O.n lg n/, but with a slightly larger constant hidden by the O-notation.
We shall give a rigorous analysis of the expected running time of a randomized
version of quicksort in Section 7.4.2.
Exercises
7.2-1
Use the substitution method to prove that the recurrence T .n/ D T .n  1/ C ‚.n/
has the solution T .n/ D ‚.n2/, as claimed at the beginning of Section 7.2.
7.2-2
What is the running time of QUICKSORT when all elements of array A have the
same value?
7.2-3
Show that the running time of QUICKSORT is ‚.n2/ when the array A contains
distinct elements and is sorted in decreasing order.
7.2-4
Banks often record transactions on an account in order of the times of the transac-
tions, but many people like to receive their bank statements with checks listed in
order by check number. People usually write checks in order by check number, and
merchants usually cash them with reasonable dispatch. The problem of converting
time-of-transaction ordering to check-number ordering is therefore the problem of
sorting almost-sorted input. Argue that the procedure INSERTION-SORT would
tend to beat the procedure QUICKSORT on this problem.
7.2-5
Suppose that the splits at every level of quicksort are in the proportion 1  ˛ to ˛,
where 0 < ˛  1=2 is a constant. Show that the minimum depth of a leaf in the re-
cursion tree is approximately  lg n= lg ˛ and the maximum depth is approximately
 lg n= lg.1  ˛/. (Don’t worry about integer round-off.)

7.3
A randomized version of quicksort
179
7.2-6
?
Argue that for any constant 0 < ˛  1=2, the probability is approximately 1  2˛
that on a random input array, PARTITION produces a split more balanced than 1˛
to ˛.
7.3
A randomized version of quicksort
In exploring the average-case behavior of quicksort, we have made an assumption
that all permutations of the input numbers are equally likely. In an engineering
situation, however, we cannot always expect this assumption to hold. (See Exer-
cise 7.2-4.) As we saw in Section 5.3, we can sometimes add randomization to an
algorithm in order to obtain good expected performance over all inputs. Many peo-
ple regard the resulting randomized version of quicksort as the sorting algorithm
of choice for large enough inputs.
In Section 5.3, we randomized our algorithm by explicitly permuting the in-
put. We could do so for quicksort also, but a different randomization technique,
called random sampling, yields a simpler analysis. Instead of always using AŒr
as the pivot, we will select a randomly chosen element from the subarray AŒp : : r.
We do so by ﬁrst exchanging element AŒr with an element chosen at random
from AŒp : : r. By randomly sampling the range p; : : : ; r, we ensure that the pivot
element x D AŒr is equally likely to be any of the r  p C 1 elements in the
subarray. Because we randomly choose the pivot element, we expect the split of
the input array to be reasonably well balanced on average.
The changes to PARTITION and QUICKSORT are small. In the new partition
procedure, we simply implement the swap before actually partitioning:
RANDOMIZED-PARTITION.A; p; r/
1
i D RANDOM.p; r/
2
exchange AŒr with AŒi
3
return PARTITION.A; p; r/
The new quicksort calls RANDOMIZED-PARTITION in place of PARTITION:
RANDOMIZED-QUICKSORT.A; p; r/
1
if p < r
2
q D RANDOMIZED-PARTITION.A; p; r/
3
RANDOMIZED-QUICKSORT.A; p; q  1/
4
RANDOMIZED-QUICKSORT.A; q C 1; r/
We analyze this algorithm in the next section.

180
Chapter 7
Quicksort
Exercises
7.3-1
Why do we analyze the expected running time of a randomized algorithm and not
its worst-case running time?
7.3-2
When RANDOMIZED-QUICKSORT runs, how many calls are made to the random-
number generator RANDOM in the worst case? How about in the best case? Give
your answer in terms of ‚-notation.
7.4
Analysis of quicksort
Section 7.2 gave some intuition for the worst-case behavior of quicksort and for
why we expect it to run quickly. In this section, we analyze the behavior of quick-
sort more rigorously. We begin with a worst-case analysis, which applies to either
QUICKSORT or RANDOMIZED-QUICKSORT, and conclude with an analysis of the
expected running time of RANDOMIZED-QUICKSORT.
7.4.1
Worst-case analysis
We saw in Section 7.2 that a worst-case split at every level of recursion in quicksort
produces a ‚.n2/ running time, which, intuitively, is the worst-case running time
of the algorithm. We now prove this assertion.
Using the substitution method (see Section 4.3), we can show that the running
time of quicksort is O.n2/. Let T .n/ be the worst-case time for the procedure
QUICKSORT on an input of size n. We have the recurrence
T .n/ D
max
0qn1.T .q/ C T .n  q  1// C ‚.n/ ;
(7.1)
where the parameter q ranges from 0 to n  1 because the procedure PARTITION
produces two subproblems with total size n  1. We guess that T .n/  cn2 for
some constant c. Substituting this guess into recurrence (7.1), we obtain
T .n/

max
0qn1.cq2 C c.n  q  1/2/ C ‚.n/
D
c  max
0qn1.q2 C .n  q  1/2/ C ‚.n/ :
The expression q2 C .n  q  1/2 achieves a maximum over the parameter’s
range 0  q  n  1 at either endpoint. To verify this claim, note that the second
derivative of the expression with respect to q is positive (see Exercise 7.4-3). This

7.4
Analysis of quicksort
181
observation gives us the bound max0qn1.q2 C .n  q  1/2/  .n  1/2 D
n2  2n C 1. Continuing with our bounding of T .n/, we obtain
T .n/

cn2  c.2n  1/ C ‚.n/

cn2 ;
since we can pick the constant c large enough so that the c.2n  1/ term dom-
inates the ‚.n/ term. Thus, T .n/ D O.n2/. We saw in Section 7.2 a speciﬁc
case in which quicksort takes .n2/ time: when partitioning is unbalanced. Al-
ternatively, Exercise 7.4-1 asks you to show that recurrence (7.1) has a solution of
T .n/ D .n2/. Thus, the (worst-case) running time of quicksort is ‚.n2/.
7.4.2
Expected running time
We have already seen the intuition behind why the expected running time of
RANDOMIZED-QUICKSORT is O.n lg n/: if, in each level of recursion, the split
induced by RANDOMIZED-PARTITION puts any constant fraction of the elements
on one side of the partition, then the recursion tree has depth ‚.lg n/, and O.n/
work is performed at each level. Even if we add a few new levels with the most un-
balanced split possible between these levels, the total time remains O.n lg n/. We
can analyze the expected running time of RANDOMIZED-QUICKSORT precisely
by ﬁrst understanding how the partitioning procedure operates and then using this
understanding to derive an O.n lg n/ bound on the expected running time. This
upper bound on the expected running time, combined with the ‚.n lg n/ best-case
bound we saw in Section 7.2, yields a ‚.n lg n/ expected running time. We assume
throughout that the values of the elements being sorted are distinct.
Running time and comparisons
The QUICKSORT and RANDOMIZED-QUICKSORT procedures differ only in how
they select pivot elements; they are the same in all other respects. We can therefore
couch our analysis of RANDOMIZED-QUICKSORT by discussing the QUICKSORT
and PARTITION procedures, but with the assumption that pivot elements are se-
lected randomly from the subarray passed to RANDOMIZED-PARTITION.
The running time of QUICKSORT is dominated by the time spent in the PARTI-
TION procedure. Each time the PARTITION procedure is called, it selects a pivot
element, and this element is never included in any future recursive calls to QUICK-
SORT and PARTITION. Thus, there can be at most n calls to PARTITION over the
entire execution of the quicksort algorithm. One call to PARTITION takes O.1/
time plus an amount of time that is proportional to the number of iterations of the
for loop in lines 3–6. Each iteration of this for loop performs a comparison in
line 4, comparing the pivot element to another element of the array A. Therefore,

182
Chapter 7
Quicksort
if we can count the total number of times that line 4 is executed, we can bound the
total time spent in the for loop during the entire execution of QUICKSORT.
Lemma 7.1
Let X be the number of comparisons performed in line 4 of PARTITION over the
entire execution of QUICKSORT on an n-element array. Then the running time of
QUICKSORT is O.n C X/.
Proof
By the discussion above, the algorithm makes at most n calls to PARTI-
TION, each of which does a constant amount of work and then executes the for
loop some number of times. Each iteration of the for loop executes line 4.
Our goal, therefore, is to compute X, the total number of comparisons performed
in all calls to PARTITION. We will not attempt to analyze how many comparisons
are made in each call to PARTITION. Rather, we will derive an overall bound on the
total number of comparisons. To do so, we must understand when the algorithm
compares two elements of the array and when it does not. For ease of analysis, we
rename the elements of the array A as ´1; ´2; : : : ; ´n, with ´i being the ith smallest
element. We also deﬁne the set Zij D f´i; ´iC1; : : : ; ´jg to be the set of elements
between ´i and ´j, inclusive.
When does the algorithm compare ´i and ´j? To answer this question, we ﬁrst
observe that each pair of elements is compared at most once. Why? Elements
are compared only to the pivot element and, after a particular call of PARTITION
ﬁnishes, the pivot element used in that call is never again compared to any other
elements.
Our analysis uses indicator random variables (see Section 5.2). We deﬁne
Xij D I f´i is compared to ´jg ;
where we are considering whether the comparison takes place at any time during
the execution of the algorithm, not just during one iteration or one call of PARTI-
TION. Since each pair is compared at most once, we can easily characterize the
total number of comparisons performed by the algorithm:
X D
n1
X
iD1
n
X
jDiC1
Xij :
Taking expectations of both sides, and then using linearity of expectation and
Lemma 5.1, we obtain
E ŒX
D
E
"n1
X
iD1
n
X
jDiC1
Xij
#

7.4
Analysis of quicksort
183
D
n1
X
iD1
n
X
jDiC1
E ŒXij
D
n1
X
iD1
n
X
jDiC1
Pr f´i is compared to ´jg :
(7.2)
It remains to compute Pr f´i is compared to ´jg. Our analysis assumes that the
RANDOMIZED-PARTITION procedure chooses each pivot randomly and indepen-
dently.
Let us think about when two items are not compared. Consider an input to
quicksort of the numbers 1 through 10 (in any order), and suppose that the ﬁrst
pivot element is 7. Then the ﬁrst call to PARTITION separates the numbers into two
sets: f1; 2; 3; 4; 5; 6g and f8; 9; 10g. In doing so, the pivot element 7 is compared
to all other elements, but no number from the ﬁrst set (e.g., 2) is or ever will be
compared to any number from the second set (e.g., 9).
In general, because we assume that element values are distinct, once a pivot x
is chosen with ´i < x < ´j, we know that ´i and ´j cannot be compared at any
subsequent time. If, on the other hand, ´i is chosen as a pivot before any other item
in Zij, then ´i will be compared to each item in Zij , except for itself. Similarly,
if ´j is chosen as a pivot before any other item in Zij , then ´j will be compared to
each item in Zij , except for itself. In our example, the values 7 and 9 are compared
because 7 is the ﬁrst item from Z7;9 to be chosen as a pivot. In contrast, 2 and 9 will
never be compared because the ﬁrst pivot element chosen from Z2;9 is 7. Thus, ´i
and ´j are compared if and only if the ﬁrst element to be chosen as a pivot from Zij
is either ´i or ´j.
We now compute the probability that this event occurs. Prior to the point at
which an element from Zij has been chosen as a pivot, the whole set Zij is together
in the same partition. Therefore, any element of Zij is equally likely to be the ﬁrst
one chosen as a pivot. Because the set Zij has j iC1 elements, and because pivots
are chosen randomly and independently, the probability that any given element is
the ﬁrst one chosen as a pivot is 1=.j  i C 1/. Thus, we have
Pr f´i is compared to ´jg
D
Pr f´i or ´j is ﬁrst pivot chosen from Zij g
D
Pr f´i is ﬁrst pivot chosen from Zij g
C Pr f´j is ﬁrst pivot chosen from Zijg
D
1
j  i C 1 C
1
j  i C 1
D
2
j  i C 1 :
(7.3)

184
Chapter 7
Quicksort
The second line follows because the two events are mutually exclusive. Combining
equations (7.2) and (7.3), we get that
E ŒX D
n1
X
iD1
n
X
jDiC1
2
j  i C 1 :
We can evaluate this sum using a change of variables (k D j  i) and the bound
on the harmonic series in equation (A.7):
E ŒX
D
n1
X
iD1
n
X
jDiC1
2
j  i C 1
D
n1
X
iD1
ni
X
kD1
2
k C 1
<
n1
X
iD1
n
X
kD1
2
k
D
n1
X
iD1
O.lg n/
D
O.n lg n/ :
(7.4)
Thus we conclude that, using RANDOMIZED-PARTITION, the expected running
time of quicksort is O.n lg n/ when element values are distinct.
Exercises
7.4-1
Show that in the recurrence
T .n/ D
max
0qn1.T .q/ C T .n  q  1// C ‚.n/ ;
T .n/ D .n2/.
7.4-2
Show that quicksort’s best-case running time is .n lg n/.
7.4-3
Show that the expression q2 C .n  q  1/2 achieves a maximum over q D
0; 1; : : : ; n  1 when q D 0 or q D n  1.
7.4-4
Show that RANDOMIZED-QUICKSORT’s expected running time is .n lg n/.

Problems for Chapter 7
185
7.4-5
We can improve the running time of quicksort in practice by taking advantage of the
fast running time of insertion sort when its input is “nearly” sorted. Upon calling
quicksort on a subarray with fewer than k elements, let it simply return without
sorting the subarray. After the top-level call to quicksort returns, run insertion sort
on the entire array to ﬁnish the sorting process. Argue that this sorting algorithm
runs in O.nk C n lg.n=k// expected time. How should we pick k, both in theory
and in practice?
7.4-6
?
Consider modifying the PARTITION procedure by randomly picking three elements
from array A and partitioning about their median (the middle value of the three
elements). Approximate the probability of getting at worst an ˛-to-.1 ˛/ split, as
a function of ˛ in the range 0 < ˛ < 1.
Problems
7-1
Hoare partition correctness
The version of PARTITION given in this chapter is not the original partitioning
algorithm. Here is the original partition algorithm, which is due to C. A. R. Hoare:
HOARE-PARTITION.A; p; r/
1
x D AŒp
2
i D p  1
3
j D r C 1
4
while TRUE
5
repeat
6
j D j  1
7
until AŒj   x
8
repeat
9
i D i C 1
10
until AŒi  x
11
if i < j
12
exchange AŒi with AŒj 
13
else return j
a. Demonstrate the operation of HOARE-PARTITION on the array A D h13; 19; 9;
5; 12; 8; 7; 4; 11; 2; 6; 21i, showing the values of the array and auxiliary values
after each iteration of the while loop in lines 4–13.

186
Chapter 7
Quicksort
The next three questions ask you to give a careful argument that the procedure
HOARE-PARTITION is correct. Assuming that the subarray AŒp : : r contains at
least two elements, prove the following:
b. The indices i and j are such that we never access an element of A outside the
subarray AŒp : : r.
c. When HOARE-PARTITION terminates, it returns a value j such that p  j < r.
d. Every element of AŒp : : j  is less than or equal to every element of AŒj C1 : : r
when HOARE-PARTITION terminates.
The PARTITION procedure in Section 7.1 separates the pivot value (originally
in AŒr) from the two partitions it forms. The HOARE-PARTITION procedure, on
the other hand, always places the pivot value (originally in AŒp) into one of the
two partitions AŒp : : j  and AŒj C 1 : : r. Since p  j < r, this split is always
nontrivial.
e. Rewrite the QUICKSORT procedure to use HOARE-PARTITION.
7-2
Quicksort with equal element values
The analysis of the expected running time of randomized quicksort in Section 7.4.2
assumes that all element values are distinct. In this problem, we examine what
happens when they are not.
a. Suppose that all element values are equal. What would be randomized quick-
sort’s running time in this case?
b. The PARTITION procedure returns an index q such that each element of
AŒp : : q  1 is less than or equal to AŒq and each element of AŒq C 1 : : r
is greater than AŒq. Modify the PARTITION procedure to produce a procedure
PARTITION0.A; p; r/, which permutes the elements of AŒp : : r and returns two
indices q and t, where p  q  t  r, such that
 all elements of AŒq : : t are equal,
 each element of AŒp : : q  1 is less than AŒq, and
 each element of AŒt C 1 : : r is greater than AŒq.
Like PARTITION, your PARTITION0 procedure should take ‚.r  p/ time.
c. Modify the RANDOMIZED-QUICKSORT procedure to call PARTITION0, and
name the new procedure RANDOMIZED-QUICKSORT0.
Then modify the
QUICKSORT procedure to produce a procedure QUICKSORT0.p; r/ that calls

Problems for Chapter 7
187
RANDOMIZED-PARTITION0 and recurses only on partitions of elements not
known to be equal to each other.
d. Using QUICKSORT0, how would you adjust the analysis in Section 7.4.2 to
avoid the assumption that all elements are distinct?
7-3
Alternative quicksort analysis
An alternative analysis of the running time of randomized quicksort focuses on
the expected running time of each individual recursive call to RANDOMIZED-
QUICKSORT, rather than on the number of comparisons performed.
a. Argue that, given an array of size n, the probability that any particular element
is chosen as the pivot is 1=n. Use this to deﬁne indicator random variables
Xi D I fith smallest element is chosen as the pivotg. What is E ŒXi?
b. Let T .n/ be a random variable denoting the running time of quicksort on an
array of size n. Argue that
E ŒT .n/ D E
" n
X
qD1
Xq .T .q  1/ C T .n  q/ C ‚.n//
#
:
(7.5)
c. Show that we can rewrite equation (7.5) as
E ŒT .n/ D 2
n
n1
X
qD2
E ŒT .q/ C ‚.n/ :
(7.6)
d. Show that
n1
X
kD2
k lg k  1
2n2 lg n  1
8n2 :
(7.7)
(Hint: Split the summation into two parts, one for k D 2; 3; : : : ; dn=2e  1 and
one for k D dn=2e ; : : : ; n  1.)
e. Using the bound from equation (7.7), show that the recurrence in equation (7.6)
has the solution E ŒT .n/ D ‚.n lg n/.
(Hint: Show, by substitution, that
E ŒT .n/  an lg n for sufﬁciently large n and for some positive constant a.)

188
Chapter 7
Quicksort
7-4
Stack depth for quicksort
The QUICKSORT algorithm of Section 7.1 contains two recursive calls to itself.
After QUICKSORT calls PARTITION, it recursively sorts the left subarray and then
it recursively sorts the right subarray. The second recursive call in QUICKSORT
is not really necessary; we can avoid it by using an iterative control structure.
This technique, called tail recursion, is provided automatically by good compilers.
Consider the following version of quicksort, which simulates tail recursion:
TAIL-RECURSIVE-QUICKSORT.A; p; r/
1
while p < r
2
// Partition and sort left subarray.
3
q D PARTITION.A; p; r/
4
TAIL-RECURSIVE-QUICKSORT.A; p; q  1/
5
p D q C 1
a. Argue that TAIL-RECURSIVE-QUICKSORT.A; 1; A:length/ correctly sorts the
array A.
Compilers usually execute recursive procedures by using a stack that contains per-
tinent information, including the parameter values, for each recursive call. The
information for the most recent call is at the top of the stack, and the information
for the initial call is at the bottom. Upon calling a procedure, its information is
pushed onto the stack; when it terminates, its information is popped. Since we
assume that array parameters are represented by pointers, the information for each
procedure call on the stack requires O.1/ stack space. The stack depth is the max-
imum amount of stack space used at any time during a computation.
b. Describe a scenario in which TAIL-RECURSIVE-QUICKSORT’s stack depth is
‚.n/ on an n-element input array.
c. Modify the code for TAIL-RECURSIVE-QUICKSORT so that the worst-case
stack depth is ‚.lg n/. Maintain the O.n lg n/ expected running time of the
algorithm.
7-5
Median-of-3 partition
One way to improve the RANDOMIZED-QUICKSORT procedure is to partition
around a pivot that is chosen more carefully than by picking a random element
from the subarray. One common approach is the median-of-3 method: choose
the pivot as the median (middle element) of a set of 3 elements randomly selected
from the subarray. (See Exercise 7.4-6.) For this problem, let us assume that the
elements in the input array AŒ1 : : n are distinct and that n  3. We denote the

Problems for Chapter 7
189
sorted output array by A0Œ1 : : n. Using the median-of-3 method to choose the
pivot element x, deﬁne pi D Pr fx D A0Œig.
a. Give an exact formula for pi as a function of n and i for i D 2; 3; : : : ; n  1.
(Note that p1 D pn D 0.)
b. By what amount have we increased the likelihood of choosing the pivot as
x D A0Œb.n C 1/=2c, the median of AŒ1 : : n, compared with the ordinary
implementation? Assume that n ! 1, and give the limiting ratio of these
probabilities.
c. If we deﬁne a “good” split to mean choosing the pivot as x D A0Œi, where
n=3  i  2n=3, by what amount have we increased the likelihood of getting
a good split compared with the ordinary implementation? (Hint: Approximate
the sum by an integral.)
d. Argue that in the .n lg n/ running time of quicksort, the median-of-3 method
affects only the constant factor.
7-6
Fuzzy sorting of intervals
Consider a sorting problem in which we do not know the numbers exactly. In-
stead, for each number, we know an interval on the real line to which it belongs.
That is, we are given n closed intervals of the form Œai; bi, where ai  bi. We
wish to fuzzy-sort these intervals, i.e., to produce a permutation hi1; i2; : : : ; ini of
the intervals such that for j D 1; 2; : : : ; n, there exist cj 2 Œaij ; bij  satisfying
c1  c2      cn.
a. Design a randomized algorithm for fuzzy-sorting n intervals. Your algorithm
should have the general structure of an algorithm that quicksorts the left end-
points (the ai values), but it should take advantage of overlapping intervals to
improve the running time. (As the intervals overlap more and more, the prob-
lem of fuzzy-sorting the intervals becomes progressively easier. Your algorithm
should take advantage of such overlapping, to the extent that it exists.)
b. Argue that your algorithm runs in expected time ‚.n lg n/ in general, but runs
in expected time ‚.n/ when all of the intervals overlap (i.e., when there exists a
value x such that x 2 Œai; bi for all i). Your algorithm should not be checking
for this case explicitly; rather, its performance should naturally improve as the
amount of overlap increases.

190
Chapter 7
Quicksort
Chapter notes
The quicksort procedure was invented by Hoare [170]; Hoare’s version appears in
Problem 7-1. The PARTITION procedure given in Section 7.1 is due to N. Lomuto.
The analysis in Section 7.4 is due to Avrim Blum. Sedgewick [305] and Bent-
ley [43] provide a good reference on the details of implementation and how they
matter.
McIlroy [248] showed how to engineer a “killer adversary” that produces an
array on which virtually any implementation of quicksort takes ‚.n2/ time. If the
implementation is randomized, the adversary produces the array after seeing the
random choices of the quicksort algorithm.

## Figures

![Page 193 figure](images/7-quicksort/p193_figure1.png)

![Page 194 figure](images/7-quicksort/p194_figure2.png)

![Page 195 figure](images/7-quicksort/p195_figure3.png)

![Page 197 figure](images/7-quicksort/p197_figure4.png)

![Page 198 figure](images/7-quicksort/p198_figure5.png)
