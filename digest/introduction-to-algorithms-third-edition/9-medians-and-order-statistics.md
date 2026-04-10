# 9 Medians and Order Statistics

Medians and Order Statistics
The ith order statistic of a set of n elements is the ith smallest element. For
example, the minimum of a set of elements is the ﬁrst order statistic (i D 1),
and the maximum is the nth order statistic (i D n). A median, informally, is
the “halfway point” of the set. When n is odd, the median is unique, occurring at
i D .n C 1/=2. When n is even, there are two medians, occurring at i D n=2 and
i D n=2C1. Thus, regardless of the parity of n, medians occur at i D b.n C 1/=2c
(the lower median) and i D d.n C 1/=2e (the upper median). For simplicity in
this text, however, we consistently use the phrase “the median” to refer to the lower
median.
This chapter addresses the problem of selecting the ith order statistic from a
set of n distinct numbers. We assume for convenience that the set contains distinct numbers, although virtually everything that we do extends to the situation in
which a set contains repeated values. We formally specify the selection problem
as follows:
Input: A set A of n (distinct) numbers and an integer i, with 1  i  n.
Output: The element x 2 A that is larger than exactly i  1 other elements of A.
We can solve the selection problem in O.n lg n/ time, since we can sort the numbers using heapsort or merge sort and then simply index the ith element in the
output array. This chapter presents faster algorithms.
In Section 9.1, we examine the problem of selecting the minimum and maximum of a set of elements. More interesting is the general selection problem, which
we investigate in the subsequent two sections. Section 9.2 analyzes a practical
randomized algorithm that achieves an O.n/ expected running time, assuming distinct elements. Section 9.3 contains an algorithm of more theoretical interest that
achieves the O.n/ running time in the worst case.

## 9.1 Minimum and maximum

How many comparisons are necessary to determine the minimum of a set of n
elements? We can easily obtain an upper bound of n  1 comparisons: examine
each element of the set in turn and keep track of the smallest element seen so
far. In the following procedure, we assume that the set resides in array A, where
A:length D n.
MINIMUM.A/
min D AŒ1
for i D 2 to A:length
if min > AŒi
min D AŒi
return min
We can, of course, ﬁnd the maximum with n  1 comparisons as well.
Is this the best we can do? Yes, since we can obtain a lower bound of n  1
comparisons for the problem of determining the minimum. Think of any algorithm
that determines the minimum as a tournament among the elements. Each comparison is a match in the tournament in which the smaller of the two elements wins.
Observing that every element except the winner must lose at least one match, we
conclude that n  1 comparisons are necessary to determine the minimum. Hence,
the algorithm MINIMUM is optimal with respect to the number of comparisons
performed.
Simultaneous minimum and maximum
In some applications, we must ﬁnd both the minimum and the maximum of a set
of n elements. For example, a graphics program may need to scale a set of .x; y/
data to ﬁt onto a rectangular display screen or other graphical output device. To
do so, the program must ﬁrst determine the minimum and maximum value of each
coordinate.
At this point, it should be obvious how to determine both the minimum and the
maximum of n elements using ‚.n/ comparisons, which is asymptotically optimal:
simply ﬁnd the minimum and maximum independently, using n  1 comparisons
for each, for a total of 2n  2 comparisons.
In fact, we can ﬁnd both the minimum and the maximum using at most 3 bn=2c
comparisons. We do so by maintaining both the minimum and maximum elements
seen thus far. Rather than processing each element of the input by comparing it
against the current minimum and maximum, at a cost of 2 comparisons per element,

## 9.2 Selection in expected linear time

we process elements in pairs. We compare pairs of elements from the input ﬁrst
with each other, and then we compare the smaller with the current minimum and
the larger to the current maximum, at a cost of 3 comparisons for every 2 elements.
How we set up initial values for the current minimum and maximum depends
on whether n is odd or even. If n is odd, we set both the minimum and maximum
to the value of the ﬁrst element, and then we process the rest of the elements in
pairs. If n is even, we perform 1 comparison on the ﬁrst 2 elements to determine
the initial values of the minimum and maximum, and then process the rest of the
elements in pairs as in the case for odd n.
Let us analyze the total number of comparisons. If n is odd, then we perform
3 bn=2c comparisons. If n is even, we perform 1 initial comparison followed by
3.n  2/=2 comparisons, for a total of 3n=2  2. Thus, in either case, the total
number of comparisons is at most 3 bn=2c.

## Exercises

9.1-1
Show that the second smallest of n elements can be found with n C dlg ne  2
comparisons in the worst case. (Hint: Also ﬁnd the smallest element.)
9.1-2
?
Prove the lower bound of d3n=2e  2 comparisons in the worst case to ﬁnd both
the maximum and minimum of n numbers. (Hint: Consider how many numbers
are potentially either the maximum or minimum, and investigate how a comparison
affects these counts.)

## 9.2 Selection in expected linear time

The general selection problem appears more difﬁcult than the simple problem of
ﬁnding a minimum. Yet, surprisingly, the asymptotic running time for both problems is the same: ‚.n/. In this section, we present a divide-and-conquer algorithm
for the selection problem. The algorithm RANDOMIZED-SELECT is modeled after
the quicksort algorithm of Chapter 7. As in quicksort, we partition the input array
recursively. But unlike quicksort, which recursively processes both sides of the
partition, RANDOMIZED-SELECT works on only one side of the partition. This
difference shows up in the analysis: whereas quicksort has an expected running
time of ‚.n lg n/, the expected running time of RANDOMIZED-SELECT is ‚.n/,
assuming that the elements are distinct.

RANDOMIZED-SELECT uses the procedure RANDOMIZED-PARTITION introduced in Section 7.3. Thus, like RANDOMIZED-QUICKSORT, it is a randomized algorithm, since its behavior is determined in part by the output of a random-number
generator. The following code for RANDOMIZED-SELECT returns the ith smallest
element of the array AŒp : : r.
RANDOMIZED-SELECT.A; p; r; i/
if p == r
return AŒp
q D RANDOMIZED-PARTITION.A; p; r/
k D q  p C 1
if i == k
// the pivot value is the answer
return AŒq
elseif i < k
return RANDOMIZED-SELECT.A; p; q  1; i/
else return RANDOMIZED-SELECT.A; q C 1; r; i  k/
The RANDOMIZED-SELECT procedure works as follows. Line 1 checks for the
base case of the recursion, in which the subarray AŒp : : r consists of just one
element. In this case, i must equal 1, and we simply return AŒp in line 2 as the
ith smallest element. Otherwise, the call to RANDOMIZED-PARTITION in line 3
partitions the array AŒp : : r into two (possibly empty) subarrays AŒp : : q  1
and AŒq C 1 : : r such that each element of AŒp : : q  1 is less than or equal
to AŒq, which in turn is less than each element of AŒq C 1 : : r. As in quicksort,
we will refer to AŒq as the pivot element. Line 4 computes the number k of
elements in the subarray AŒp : : q, that is, the number of elements in the low side
of the partition, plus one for the pivot element. Line 5 then checks whether AŒq is
the ith smallest element. If it is, then line 6 returns AŒq. Otherwise, the algorithm
determines in which of the two subarrays AŒp : : q  1 and AŒq C 1 : : r the ith
smallest element lies. If i < k, then the desired element lies on the low side of
the partition, and line 8 recursively selects it from the subarray. If i > k, however,
then the desired element lies on the high side of the partition. Since we already
know k values that are smaller than the ith smallest element of AŒp : : r—namely,
the elements of AŒp : : q—the desired element is the .i  k/th smallest element
of AŒq C1 : : r, which line 9 ﬁnds recursively. The code appears to allow recursive
calls to subarrays with 0 elements, but Exercise 9.2-1 asks you to show that this
situation cannot happen.
The worst-case running time for RANDOMIZED-SELECT is ‚.n2/, even to ﬁnd
the minimum, because we could be extremely unlucky and always partition around
the largest remaining element, and partitioning takes ‚.n/ time. We will see that

## 9.2 Selection in expected linear time

the algorithm has a linear expected running time, though, and because it is randomized, no particular input elicits the worst-case behavior.
To analyze the expected running time of RANDOMIZED-SELECT, we let the running time on an input array AŒp : : r of n elements be a random variable that we
denote by T .n/, and we obtain an upper bound on E ŒT .n/ as follows. The procedure RANDOMIZED-PARTITION is equally likely to return any element as the
pivot. Therefore, for each k such that 1  k  n, the subarray AŒp : : q has k elements (all less than or equal to the pivot) with probability 1=n. For k D 1; 2; : : : ; n,
we deﬁne indicator random variables Xk where
Xk D I fthe subarray AŒp : : q has exactly k elementsg ;
and so, assuming that the elements are distinct, we have
E ŒXk D 1=n :
(9.1)
When we call RANDOMIZED-SELECT and choose AŒq as the pivot element, we
do not know, a priori, if we will terminate immediately with the correct answer,
recurse on the subarray AŒp : : q  1, or recurse on the subarray AŒq C 1 : : r.
This decision depends on where the ith smallest element falls relative to AŒq.
Assuming that T .n/ is monotonically increasing, we can upper-bound the time
needed for the recursive call by the time needed for the recursive call on the largest
possible input. In other words, to obtain an upper bound, we assume that the ith
element is always on the side of the partition with the greater number of elements.
For a given call of RANDOMIZED-SELECT, the indicator random variable Xk has
the value 1 for exactly one value of k, and it is 0 for all other k. When Xk D 1, the
two subarrays on which we might recurse have sizes k  1 and n  k. Hence, we
have the recurrence
T .n/

n
X
kD1
Xk  .T .max.k  1; n  k// C O.n//
D
n
X
kD1
Xk  T .max.k  1; n  k// C O.n/ :

Taking expected values, we have
E ŒT .n/
 E
" n
X
kD1
Xk  T .max.k  1; n  k// C O.n/
#
D
n
X
kD1
E ŒXk  T .max.k  1; n  k// C O.n/
(by linearity of expectation)
D
n
X
kD1
E ŒXk  E ŒT .max.k  1; n  k// C O.n/ (by equation (C.24))
D
n
X
kD1
n  E ŒT .max.k  1; n  k// C O.n/
(by equation (9.1)) .
In order to apply equation (C.24), we rely on Xk and T .max.k  1; n  k// being
independent random variables. Exercise 9.2-2 asks you to justify this assertion.
Let us consider the expression max.k  1; n  k/. We have
max.k  1; n  k/ D
(
k  1
if k > dn=2e ;
n  k
if k  dn=2e :
If n is even, each term from T .dn=2e/ up to T .n  1/ appears exactly twice in
the summation, and if n is odd, all these terms appear twice and T .bn=2c/ appears
once. Thus, we have
E ŒT .n/  2
n
n1
X
kDbn=2c
E ŒT .k/ C O.n/ :
We show that E ŒT .n/ D O.n/ by substitution. Assume that E ŒT .n/  cn for
some constant c that satisﬁes the initial conditions of the recurrence. We assume
that T .n/ D O.1/ for n less than some constant; we shall pick this constant later.
We also pick a constant a such that the function described by the O.n/ term above
(which describes the non-recursive component of the running time of the algorithm) is bounded from above by an for all n > 0. Using this inductive hypothesis,
we have
E ŒT .n/

n
n1
X
kDbn=2c
ck C an
D
2c
n
n1
X
kD1
k 
bn=2c1
X
kD1
k
!
C an

## 9.2 Selection in expected linear time

D
2c
n
.n  1/n
 .bn=2c  1/ bn=2c

C an

2c
n
.n  1/n
 .n=2  2/.n=2  1/

C an
D
2c
n
n2  n
 n2=4  3n=2 C 2

C an
D
c
n
3n2
C n
2  2

C an
D
c
3n
4 C 1
2  2
n

C an

3cn
C c
2 C an
D
cn 
cn
4  c
2  an

:
In order to complete the proof, we need to show that for sufﬁciently large n, this
last expression is at most cn or, equivalently, that cn=4  c=2  an  0. If we
add c=2 to both sides and factor out n, we get n.c=4  a/  c=2. As long as we
choose the constant c so that c=4  a > 0, i.e., c > 4a, we can divide both sides
by c=4  a, giving
n 
c=2
c=4  a D
2c
c  4a :
Thus, if we assume that T .n/ D O.1/ for n < 2c=.c4a/, then E ŒT .n/ D O.n/.
We conclude that we can ﬁnd any order statistic, and in particular the median, in
expected linear time, assuming that the elements are distinct.

## Exercises

9.2-1
Show that RANDOMIZED-SELECT never makes a recursive call to a 0-length array.
9.2-2
Argue that the indicator random variable Xk and the value T .max.k  1; n  k//
are independent.
9.2-3
Write an iterative version of RANDOMIZED-SELECT.

9.2-4
Suppose we use RANDOMIZED-SELECT to select the minimum element of the
array A D h3; 2; 9; 0; 7; 5; 4; 8; 6; 1i. Describe a sequence of partitions that results
in a worst-case performance of RANDOMIZED-SELECT.

## 9.3 Selection in worst-case linear time

We now examine a selection algorithm whose running time is O.n/ in the worst
case. Like RANDOMIZED-SELECT, the algorithm SELECT ﬁnds the desired element by recursively partitioning the input array. Here, however, we guarantee a
good split upon partitioning the array. SELECT uses the deterministic partitioning
algorithm PARTITION from quicksort (see Section 7.1), but modiﬁed to take the
element to partition around as an input parameter.
The SELECT algorithm determines the ith smallest of an input array of n > 1
distinct elements by executing the following steps. (If n D 1, then SELECT merely
returns its only input value as the ith smallest.)
1. Divide the n elements of the input array into bn=5c groups of 5 elements each
and at most one group made up of the remaining n mod 5 elements.
2. Find the median of each of the dn=5e groups by ﬁrst insertion-sorting the elements of each group (of which there are at most 5) and then picking the median
from the sorted list of group elements.
3. Use SELECT recursively to ﬁnd the median x of the dn=5e medians found in
step 2. (If there are an even number of medians, then by our convention, x is
the lower median.)
4. Partition the input array around the median-of-medians x using the modiﬁed
version of PARTITION. Let k be one more than the number of elements on the
low side of the partition, so that x is the kth smallest element and there are nk
elements on the high side of the partition.
5. If i D k, then return x. Otherwise, use SELECT recursively to ﬁnd the ith
smallest element on the low side if i < k, or the .i  k/th smallest element on
the high side if i > k.
To analyze the running time of SELECT, we ﬁrst determine a lower bound on the
number of elements that are greater than the partitioning element x. Figure 9.1
helps us to visualize this bookkeeping.
At least half of the medians found in

## 9.3 Selection in worst-case linear time

x
Figure 9.1
Analysis of the algorithm SELECT. The n elements are represented by small circles,
and each group of 5 elements occupies a column. The medians of the groups are whitened, and the
median-of-medians x is labeled. (When ﬁnding the median of an even number of elements, we use
the lower median.) Arrows go from larger elements to smaller, from which we can see that 3 out
of every full group of 5 elements to the right of x are greater than x, and 3 out of every group of 5
elements to the left of x are less than x. The elements known to be greater than x appear on a shaded
background.
step 2 are greater than or equal to the median-of-medians x.1 Thus, at least half
of the dn=5e groups contribute at least 3 elements that are greater than x, except
for the one group that has fewer than 5 elements if 5 does not divide n exactly, and
the one group containing x itself. Discounting these two groups, it follows that the
number of elements greater than x is at least
1
ln
m
 2

 3n
10  6 :
Similarly, at least 3n=10  6 elements are less than x. Thus, in the worst case,
step 5 calls SELECT recursively on at most 7n=10 C 6 elements.
We can now develop a recurrence for the worst-case running time T .n/ of the
algorithm SELECT. Steps 1, 2, and 4 take O.n/ time. (Step 2 consists of O.n/
calls of insertion sort on sets of size O.1/.) Step 3 takes time T .dn=5e/, and step 5
takes time at most T .7n=10 C 6/, assuming that T is monotonically increasing.
We make the assumption, which seems unmotivated at ﬁrst, that any input of fewer
than 140 elements requires O.1/ time; the origin of the magic constant 140 will be
clear shortly. We can therefore obtain the recurrence
1Because of our assumption that the numbers are distinct, all medians except x are either greater
than or less than x.

T .n/ 
(
O.1/
if n < 140 ;
T .dn=5e/ C T .7n=10 C 6/ C O.n/
if n  140 :
We show that the running time is linear by substitution. More speciﬁcally, we will
show that T .n/  cn for some suitably large constant c and all n > 0. We begin by
assuming that T .n/  cn for some suitably large constant c and all n < 140; this
assumption holds if c is large enough. We also pick a constant a such that the function described by the O.n/ term above (which describes the non-recursive component of the running time of the algorithm) is bounded above by an for all n > 0.
Substituting this inductive hypothesis into the right-hand side of the recurrence
yields
T .n/

c dn=5e C c.7n=10 C 6/ C an

cn=5 C c C 7cn=10 C 6c C an
D
9cn=10 C 7c C an
D
cn C .cn=10 C 7c C an/ ;
which is at most cn if
cn=10 C 7c C an  0 :
(9.2)
Inequality (9.2) is equivalent to the inequality c  10a.n=.n  70// when n > 70.
Because we assume that n  140, we have n=.n  70/  2, and so choosing c  20a will satisfy inequality (9.2). (Note that there is nothing special about
the constant 140; we could replace it by any integer strictly greater than 70 and
then choose c accordingly.) The worst-case running time of SELECT is therefore
linear.
As in a comparison sort (see Section 8.1), SELECT and RANDOMIZED-SELECT
determine information about the relative order of elements only by comparing elements. Recall from Chapter 8 that sorting requires .n lg n/ time in the comparison model, even on average (see Problem 8-1). The linear-time sorting algorithms
in Chapter 8 make assumptions about the input. In contrast, the linear-time selection algorithms in this chapter do not require any assumptions about the input.
They are not subject to the .n lg n/ lower bound because they manage to solve
the selection problem without sorting. Thus, solving the selection problem by sorting and indexing, as presented in the introduction to this chapter, is asymptotically
inefﬁcient.

## 9.3 Selection in worst-case linear time

## Exercises

9.3-1
In the algorithm SELECT, the input elements are divided into groups of 5. Will
the algorithm work in linear time if they are divided into groups of 7? Argue that
SELECT does not run in linear time if groups of 3 are used.
9.3-2
Analyze SELECT to show that if n  140, then at least dn=4e elements are greater
than the median-of-medians x and at least dn=4e elements are less than x.
9.3-3
Show how quicksort can be made to run in O.n lg n/ time in the worst case, assuming that all elements are distinct.
9.3-4
?
Suppose that an algorithm uses only comparisons to ﬁnd the ith smallest element
in a set of n elements. Show that it can also ﬁnd the i  1 smaller elements and
the n  i larger elements without performing any additional comparisons.
9.3-5
Suppose that you have a “black-box” worst-case linear-time median subroutine.
Give a simple, linear-time algorithm that solves the selection problem for an arbitrary order statistic.
9.3-6
The kth quantiles of an n-element set are the k  1 order statistics that divide the
sorted set into k equal-sized sets (to within 1). Give an O.n lg k/-time algorithm
to list the kth quantiles of a set.
9.3-7
Describe an O.n/-time algorithm that, given a set S of n distinct numbers and
a positive integer k  n, determines the k numbers in S that are closest to the
median of S.
9.3-8
Let XŒ1 : : n and Y Œ1 : : n be two arrays, each containing n numbers already in
sorted order. Give an O.lg n/-time algorithm to ﬁnd the median of all 2n elements
in arrays X and Y .
9.3-9
Professor Olay is consulting for an oil company, which is planning a large pipeline
running east to west through an oil ﬁeld of n wells. The company wants to connect

Figure 9.2
Professor Olay needs to determine the position of the east-west oil pipeline that minimizes the total length of the north-south spurs.
a spur pipeline from each well directly to the main pipeline along a shortest route
(either north or south), as shown in Figure 9.2. Given the x- and y-coordinates of
the wells, how should the professor pick the optimal location of the main pipeline,
which would be the one that minimizes the total length of the spurs? Show how to
determine the optimal location in linear time.

## Problems

9-1
Largest i numbers in sorted order
Given a set of n numbers, we wish to ﬁnd the i largest in sorted order using a
comparison-based algorithm. Find the algorithm that implements each of the following methods with the best asymptotic worst-case running time, and analyze the
running times of the algorithms in terms of n and i.
a. Sort the numbers, and list the i largest.
b. Build a max-priority queue from the numbers, and call EXTRACT-MAX i times.
c. Use an order-statistic algorithm to ﬁnd the ith largest number, partition around
that number, and sort the i largest numbers.

Problems for Chapter 9
9-2
Weighted median
For n distinct elements x1; x2; : : : ; xn with positive weights w1; w2; : : : ; wn such
that Pn
iD1 wi D 1, the weighted (lower) median is the element xk satisfying
X
xi<xk
wi < 1
and
X
xi>xk
wi  1
2 :
For example, if the elements are 0:1; 0:35; 0:05; 0:1; 0:15; 0:05; 0:2 and each element equals its weight (that is, wi D xi for i D 1; 2; : : : ; 7), then the median is 0:1,
but the weighted median is 0:2.
a. Argue that the median of x1; x2; : : : ; xn is the weighted median of the xi with
weights wi D 1=n for i D 1; 2; : : : ; n.
b. Show how to compute the weighted median of n elements in O.n lg n/ worstcase time using sorting.
c. Show how to compute the weighted median in ‚.n/ worst-case time using a
linear-time median algorithm such as SELECT from Section 9.3.
The post-ofﬁce location problem is deﬁned as follows. We are given n points
p1; p2; : : : ; pn with associated weights w1; w2; : : : ; wn. We wish to ﬁnd a point p
(not necessarily one of the input points) that minimizes the sum Pn
iD1 wi d.p; pi/,
where d.a; b/ is the distance between points a and b.
d. Argue that the weighted median is a best solution for the 1-dimensional postofﬁce location problem, in which points are simply real numbers and the distance between points a and b is d.a; b/ D ja  bj.
e. Find the best solution for the 2-dimensional post-ofﬁce location problem, in
which the points are .x; y/ coordinate pairs and the distance between points
a D .x1; y1/ and b D .x2; y2/ is the Manhattan distance given by d.a; b/ D
jx1  x2j C jy1  y2j.
9-3
Small order statistics
We showed that the worst-case number T .n/ of comparisons used by SELECT
to select the ith order statistic from n numbers satisﬁes T .n/ D ‚.n/, but the
constant hidden by the ‚-notation is rather large. When i is small relative to n, we
can implement a different procedure that uses SELECT as a subroutine but makes
fewer comparisons in the worst case.

a. Describe an algorithm that uses Ui.n/ comparisons to ﬁnd the ith smallest of n
elements, where
Ui.n/ D
(
T .n/
if i  n=2 ;
bn=2c C Ui.dn=2e/ C T .2i/
otherwise :
(Hint: Begin with bn=2c disjoint pairwise comparisons, and recurse on the set
containing the smaller element from each pair.)
b. Show that, if i < n=2, then Ui.n/ D n C O.T .2i/ lg.n=i//.
c. Show that if i is a constant less than n=2, then Ui.n/ D n C O.lg n/.
d. Show that if i D n=k for k  2, then Ui.n/ D n C O.T .2n=k/ lg k/.
9-4
Alternative analysis of randomized selection
In this problem, we use indicator random variables to analyze the RANDOMIZEDSELECT procedure in a manner akin to our analysis of RANDOMIZED-QUICKSORT
in Section 7.4.2.
As in the quicksort analysis, we assume that all elements are distinct, and we
rename the elements of the input array A as ´1; ´2; : : : ; ´n, where ´i is the ith
smallest element. Thus, the call RANDOMIZED-SELECT.A; 1; n; k/ returns ´k.
For 1  i < j  n, let
Xijk D I f´i is compared with ´j sometime during the execution of the algorithm
to ﬁnd ´kg :
a. Give an exact expression for E ŒXijk. (Hint: Your expression may have different values, depending on the values of i, j , and k.)
b. Let Xk denote the total number of comparisons between elements of array A
when ﬁnding ´k. Show that
E ŒXk  2
k
X
iD1
n
X
jDk
j  i C 1 C
n
X
jDkC1
j  k  1
j  k C 1 C
k2
X
iD1
k  i  1
k  i C 1
!
:
c. Show that E ŒXk  4n.
d. Conclude that, assuming all elements of array A are distinct, RANDOMIZEDSELECT runs in expected time O.n/.

Notes for Chapter 9
Chapter notes
The worst-case linear-time median-ﬁnding algorithm was devised by Blum, Floyd,
Pratt, Rivest, and Tarjan [50]. The fast randomized version is due to Hoare [169].
Floyd and Rivest [108] have developed an improved randomized version that partitions around an element recursively selected from a small sample of the elements.
It is still unknown exactly how many comparisons are needed to determine the
median. Bent and John [41] gave a lower bound of 2n comparisons for median
ﬁnding, and Sch¨onhage, Paterson, and Pippenger [302] gave an upper bound of 3n.
Dor and Zwick have improved on both of these bounds. Their upper bound [93]
is slightly less than 2:95n, and their lower bound [94] is .2 C /n, for a small
positive constant , thereby improving slightly on related work by Dor et al. [92].
Paterson [272] describes some of these results along with other related work.
