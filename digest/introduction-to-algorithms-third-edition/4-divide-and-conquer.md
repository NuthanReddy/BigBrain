# 4 Divide-and-Conquer

4
Divide-and-Conquer
In Section 2.3.1, we saw how merge sort serves as an example of the divide-and-
conquer paradigm. Recall that in divide-and-conquer, we solve a problem recur-
sively, applying three steps at each level of the recursion:
Divide the problem into a number of subproblems that are smaller instances of the
same problem.
Conquer the subproblems by solving them recursively. If the subproblem sizes are
small enough, however, just solve the subproblems in a straightforward manner.
Combine the solutions to the subproblems into the solution for the original prob-
lem.
When the subproblems are large enough to solve recursively, we call that the recur-
sive case. Once the subproblems become small enough that we no longer recurse,
we say that the recursion “bottoms out” and that we have gotten down to the base
case. Sometimes, in addition to subproblems that are smaller instances of the same
problem, we have to solve subproblems that are not quite the same as the original
problem. We consider solving such subproblems as part of the combine step.
In this chapter, we shall see more algorithms based on divide-and-conquer. The
ﬁrst one solves the maximum-subarray problem: it takes as input an array of num-
bers, and it determines the contiguous subarray whose values have the greatest sum.
Then we shall see two divide-and-conquer algorithms for multiplying n 	 n matri-
ces. One runs in ‚.n3/ time, which is no better than the straightforward method of
multiplying square matrices. But the other, Strassen’s algorithm, runs in O.n2:81/
time, which beats the straightforward method asymptotically.
Recurrences
Recurrences go hand in hand with the divide-and-conquer paradigm, because they
give us a natural way to characterize the running times of divide-and-conquer algo-
rithms. A recurrence is an equation or inequality that describes a function in terms

66
Chapter 4
Divide-and-Conquer
of its value on smaller inputs. For example, in Section 2.3.2 we described the
worst-case running time T .n/ of the MERGE-SORT procedure by the recurrence
T .n/ D
(
‚.1/
if n D 1 ;
2T .n=2/ C ‚.n/
if n > 1 ;
(4.1)
whose solution we claimed to be T .n/ D ‚.n lg n/.
Recurrences can take many forms. For example, a recursive algorithm might
divide subproblems into unequal sizes, such as a 2=3-to-1=3 split. If the divide and
combine steps take linear time, such an algorithm would give rise to the recurrence
T .n/ D T .2n=3/ C T .n=3/ C ‚.n/.
Subproblems are not necessarily constrained to being a constant fraction of
the original problem size.
For example, a recursive version of linear search
(see Exercise 2.1-3) would create just one subproblem containing only one el-
ement fewer than the original problem.
Each recursive call would take con-
stant time plus the time for the recursive calls it makes, yielding the recurrence
T .n/ D T .n  1/ C ‚.1/.
This chapter offers three methods for solving recurrences—that is, for obtaining
asymptotic “‚” or “O” bounds on the solution:

In the substitution method, we guess a bound and then use mathematical in-
duction to prove our guess correct.

The recursion-tree method converts the recurrence into a tree whose nodes
represent the costs incurred at various levels of the recursion. We use techniques
for bounding summations to solve the recurrence.

The master method provides bounds for recurrences of the form
T .n/ D aT .n=b/ C f .n/ ;
(4.2)
where a  1, b > 1, and f .n/ is a given function. Such recurrences arise
frequently. A recurrence of the form in equation (4.2) characterizes a divide-
and-conquer algorithm that creates a subproblems, each of which is 1=b the
size of the original problem, and in which the divide and combine steps together
take f .n/ time.
To use the master method, you will need to memorize three cases, but once
you do that, you will easily be able to determine asymptotic bounds for many
simple recurrences. We will use the master method to determine the running
times of the divide-and-conquer algorithms for the maximum-subarray problem
and for matrix multiplication, as well as for other algorithms based on divide-
and-conquer elsewhere in this book.

Chapter 4
Divide-and-Conquer
67
Occasionally, we shall see recurrences that are not equalities but rather inequal-
ities, such as T .n/  2T .n=2/ C ‚.n/. Because such a recurrence states only
an upper bound on T .n/, we will couch its solution using O-notation rather than
‚-notation. Similarly, if the inequality were reversed to T .n/  2T .n=2/ C ‚.n/,
then because the recurrence gives only a lower bound on T .n/, we would use
-notation in its solution.
Technicalities in recurrences
In practice, we neglect certain technical details when we state and solve recur-
rences. For example, if we call MERGE-SORT on n elements when n is odd, we
end up with subproblems of size bn=2c and dn=2e. Neither size is actually n=2,
because n=2 is not an integer when n is odd. Technically, the recurrence describing
the worst-case running time of MERGE-SORT is really
T .n/ D
(
‚.1/
if n D 1 ;
T .dn=2e/ C T .bn=2c/ C ‚.n/
if n > 1 :
(4.3)
Boundary conditions represent another class of details that we typically ignore.
Since the running time of an algorithm on a constant-sized input is a constant,
the recurrences that arise from the running times of algorithms generally have
T .n/ D ‚.1/ for sufﬁciently small n. Consequently, for convenience, we shall
generally omit statements of the boundary conditions of recurrences and assume
that T .n/ is constant for small n. For example, we normally state recurrence (4.1)
as
T .n/ D 2T .n=2/ C ‚.n/ ;
(4.4)
without explicitly giving values for small n. The reason is that although changing
the value of T .1/ changes the exact solution to the recurrence, the solution typi-
cally doesn’t change by more than a constant factor, and so the order of growth is
unchanged.
When we state and solve recurrences, we often omit ﬂoors, ceilings, and bound-
ary conditions. We forge ahead without these details and later determine whether
or not they matter. They usually do not, but you should know when they do. Ex-
perience helps, and so do some theorems stating that these details do not affect the
asymptotic bounds of many recurrences characterizing divide-and-conquer algo-
rithms (see Theorem 4.1). In this chapter, however, we shall address some of these
details and illustrate the ﬁne points of recurrence solution methods.

68
Chapter 4
Divide-and-Conquer
4.1
The maximum-subarray problem
Suppose that you been offered the opportunity to invest in the Volatile Chemical
Corporation. Like the chemicals the company produces, the stock price of the
Volatile Chemical Corporation is rather volatile. You are allowed to buy one unit
of stock only one time and then sell it at a later date, buying and selling after the
close of trading for the day. To compensate for this restriction, you are allowed to
learn what the price of the stock will be in the future. Your goal is to maximize
your proﬁt. Figure 4.1 shows the price of the stock over a 17-day period. You
may buy the stock at any one time, starting after day 0, when the price is $100
per share. Of course, you would want to “buy low, sell high”—buy at the lowest
possible price and later on sell at the highest possible price—to maximize your
proﬁt. Unfortunately, you might not be able to buy at the lowest price and then sell
at the highest price within a given period. In Figure 4.1, the lowest price occurs
after day 7, which occurs after the highest price, after day 1.
You might think that you can always maximize proﬁt by either buying at the
lowest price or selling at the highest price. For example, in Figure 4.1, we would
maximize proﬁt by buying at the lowest price, after day 7. If this strategy always
worked, then it would be easy to determine how to maximize proﬁt: ﬁnd the highest
and lowest prices, and then work left from the highest price to ﬁnd the lowest prior
price, work right from the lowest price to ﬁnd the highest later price, and take
the pair with the greater difference. Figure 4.2 shows a simple counterexample,
0
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
120
110
100
90
80
70
60
Day
0
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
13 14
15 16
Price
100 113 110
85 105 102
86
63 81 101
94 106 101
79 94
90 97
Change
13
3 25
20
3 16 23 18
20 7
12
5 22 15 4
7
Figure 4.1
Information about the price of stock in the Volatile Chemical Corporation after the close
of trading over a period of 17 days. The horizontal axis of the chart indicates the day, and the vertical
axis shows the price. The bottom row of the table gives the change in price from the previous day.

4.1
The maximum-subarray problem
69
0
1
2
3
4
11
10
9
8
7
6
Day
0
1
2
3
4
Price
10
11
7
10
6
Change
1
4
3
4
Figure 4.2
An example showing that the maximum proﬁt does not always start at the lowest price
or end at the highest price. Again, the horizontal axis indicates the day, and the vertical axis shows
the price. Here, the maximum proﬁt of $3 per share would be earned by buying after day 2 and
selling after day 3. The price of $7 after day 2 is not the lowest price overall, and the price of $10
after day 3 is not the highest price overall.
demonstrating that the maximum proﬁt sometimes comes neither by buying at the
lowest price nor by selling at the highest price.
A brute-force solution
We can easily devise a brute-force solution to this problem: just try every possible
pair of buy and sell dates in which the buy date precedes the sell date. A period of n
days has

n
2

such pairs of dates. Since

n
2

is ‚.n2/, and the best we can hope for
is to evaluate each pair of dates in constant time, this approach would take .n2/
time. Can we do better?
A transformation
In order to design an algorithm with an o.n2/ running time, we will look at the
input in a slightly different way. We want to ﬁnd a sequence of days over which
the net change from the ﬁrst day to the last is maximum. Instead of looking at the
daily prices, let us instead consider the daily change in price, where the change on
day i is the difference between the prices after day i  1 and after day i. The table
in Figure 4.1 shows these daily changes in the bottom row. If we treat this row as
an array A, shown in Figure 4.3, we now want to ﬁnd the nonempty, contiguous
subarray of A whose values have the largest sum. We call this contiguous subarray
the maximum subarray. For example, in the array of Figure 4.3, the maximum
subarray of AŒ1 : : 16 is AŒ8 : : 11, with the sum 43. Thus, you would want to buy
the stock just before day 8 (that is, after day 7) and sell it after day 11, earning a
proﬁt of $43 per share.
At ﬁrst glance, this transformation does not help.
We still need to check

n1
2

D ‚.n2/ subarrays for a period of n days. Exercise 4.1-2 asks you to show

70
Chapter 4
Divide-and-Conquer
13
1
–3
2
–25
3
20
4
–3
5
–16
6
–23
7
8
9
10
maximum subarray
11
18
12
20
13
–7
14
12
15
7
16
–5 –22 15
–4
A
Figure 4.3
The change in stock prices as a maximum-subarray problem.
Here, the subar-
ray AŒ8 : : 11, with sum 43, has the greatest sum of any contiguous subarray of array A.
that although computing the cost of one subarray might take time proportional to
the length of the subarray, when computing all ‚.n2/ subarray sums, we can orga-
nize the computation so that each subarray sum takes O.1/ time, given the values
of previously computed subarray sums, so that the brute-force solution takes ‚.n2/
time.
So let us seek a more efﬁcient solution to the maximum-subarray problem.
When doing so, we will usually speak of “a” maximum subarray rather than “the”
maximum subarray, since there could be more than one subarray that achieves the
maximum sum.
The maximum-subarray problem is interesting only when the array contains
some negative numbers.
If all the array entries were nonnegative, then the
maximum-subarray problem would present no challenge, since the entire array
would give the greatest sum.
A solution using divide-and-conquer
Let’s think about how we might solve the maximum-subarray problem using
the divide-and-conquer technique. Suppose we want to ﬁnd a maximum subar-
ray of the subarray AŒlow : : high. Divide-and-conquer suggests that we divide
the subarray into two subarrays of as equal size as possible.
That is, we ﬁnd
the midpoint, say mid, of the subarray, and consider the subarrays AŒlow : : mid
and AŒmid C 1 : : high. As Figure 4.4(a) shows, any contiguous subarray AŒi : : j 
of AŒlow : : high must lie in exactly one of the following places:

entirely in the subarray AŒlow : : mid, so that low  i  j  mid,

entirely in the subarray AŒmid C 1 : : high, so that mid < i  j  high, or

crossing the midpoint, so that low  i  mid < j  high.
Therefore, a maximum subarray of AŒlow : : high must lie in exactly one of these
places.
In fact, a maximum subarray of AŒlow : : high must have the greatest
sum over all subarrays entirely in AŒlow : : mid, entirely in AŒmid C 1 : : high,
or crossing the midpoint. We can ﬁnd maximum subarrays of AŒlow : : mid and
AŒmidC1 : : high recursively, because these two subproblems are smaller instances
of the problem of ﬁnding a maximum subarray. Thus, all that is left to do is ﬁnd a

4.1
The maximum-subarray problem
71
(a)
(b)
low
low
mid
mid
high
high
crosses the midpoint
mid C 1
mid C 1
entirely in AŒlow : : mid
entirely in AŒmid C 1 : : high
i
j
AŒi : : mid
AŒmid C 1 : : j 
Figure 4.4
(a) Possible locations of subarrays of AŒlow : : high: entirely in AŒlow : : mid, entirely
in AŒmid C 1 : : high, or crossing the midpoint mid. (b) Any subarray of AŒlow : : high crossing
the midpoint comprises two subarrays AŒi : : mid and AŒmid C 1 : : j, where low  i  mid and
mid < j  high.
maximum subarray that crosses the midpoint, and take a subarray with the largest
sum of the three.
We can easily ﬁnd a maximum subarray crossing the midpoint in time linear
in the size of the subarray AŒlow : : high. This problem is not a smaller instance
of our original problem, because it has the added restriction that the subarray it
chooses must cross the midpoint. As Figure 4.4(b) shows, any subarray crossing
the midpoint is itself made of two subarrays AŒi : : mid and AŒmid C 1 : : j , where
low  i  mid and mid < j  high. Therefore, we just need to ﬁnd maximum
subarrays of the form AŒi : : mid and AŒmid C 1 : : j  and then combine them. The
procedure FIND-MAX-CROSSING-SUBARRAY takes as input the array A and the
indices low, mid, and high, and it returns a tuple containing the indices demarcating
a maximum subarray that crosses the midpoint, along with the sum of the values in
a maximum subarray.
FIND-MAX-CROSSING-SUBARRAY.A; low; mid; high/
1
left-sum D 1
2
sum D 0
3
for i D mid downto low
4
sum D sum C AŒi
5
if sum > left-sum
6
left-sum D sum
7
max-left D i
8
right-sum D 1
9
sum D 0
10
for j D mid C 1 to high
11
sum D sum C AŒj 
12
if sum > right-sum
13
right-sum D sum
14
max-right D j
15
return .max-left; max-right; left-sum C right-sum/

72
Chapter 4
Divide-and-Conquer
This procedure works as follows. Lines 1–7 ﬁnd a maximum subarray of the
left half, AŒlow : : mid. Since this subarray must contain AŒmid, the for loop of
lines 3–7 starts the index i at mid and works down to low, so that every subarray
it considers is of the form AŒi : : mid. Lines 1–2 initialize the variables left-sum,
which holds the greatest sum found so far, and sum, holding the sum of the entries
in AŒi : : mid. Whenever we ﬁnd, in line 5, a subarray AŒi : : mid with a sum of
values greater than left-sum, we update left-sum to this subarray’s sum in line 6, and
in line 7 we update the variable max-left to record this index i. Lines 8–14 work
analogously for the right half, AŒmidC1 : : high. Here, the for loop of lines 10–14
starts the index j at midC1 and works up to high, so that every subarray it considers
is of the form AŒmid C 1 : : j . Finally, line 15 returns the indices max-left and
max-right that demarcate a maximum subarray crossing the midpoint, along with
the sum left-sumCright-sum of the values in the subarray AŒmax-left : : max-right.
If the subarray AŒlow : : high contains n entries (so that n D high  low C 1),
we claim that the call FIND-MAX-CROSSING-SUBARRAY.A; low; mid; high/
takes ‚.n/ time. Since each iteration of each of the two for loops takes ‚.1/
time, we just need to count up how many iterations there are altogether. The for
loop of lines 3–7 makes mid  low C 1 iterations, and the for loop of lines 10–14
makes high  mid iterations, and so the total number of iterations is
.mid  low C 1/ C .high  mid/
D
high  low C 1
D
n :
With a linear-time FIND-MAX-CROSSING-SUBARRAY procedure in hand, we
can write pseudocode for a divide-and-conquer algorithm to solve the maximum-
subarray problem:
FIND-MAXIMUM-SUBARRAY.A; low; high/
1
if high == low
2
return .low; high; AŒlow/
// base case: only one element
3
else mid D b.low C high/=2c
4
.left-low; left-high; left-sum/ D
FIND-MAXIMUM-SUBARRAY.A; low; mid/
5
.right-low; right-high; right-sum/ D
FIND-MAXIMUM-SUBARRAY.A; mid C 1; high/
6
.cross-low; cross-high; cross-sum/ D
FIND-MAX-CROSSING-SUBARRAY.A; low; mid; high/
7
if left-sum  right-sum and left-sum  cross-sum
8
return .left-low; left-high; left-sum/
9
elseif right-sum  left-sum and right-sum  cross-sum
10
return .right-low; right-high; right-sum/
11
else return .cross-low; cross-high; cross-sum/

4.1
The maximum-subarray problem
73
The initial call FIND-MAXIMUM-SUBARRAY.A; 1; A:length/ will ﬁnd a maxi-
mum subarray of AŒ1 : : n.
Similar to FIND-MAX-CROSSING-SUBARRAY, the recursive procedure FIND-
MAXIMUM-SUBARRAY returns a tuple containing the indices that demarcate a
maximum subarray, along with the sum of the values in a maximum subarray.
Line 1 tests for the base case, where the subarray has just one element. A subar-
ray with just one element has only one subarray—itself—and so line 2 returns a
tuple with the starting and ending indices of just the one element, along with its
value. Lines 3–11 handle the recursive case. Line 3 does the divide part, comput-
ing the index mid of the midpoint. Let’s refer to the subarray AŒlow : : mid as the
left subarray and to AŒmid C 1 : : high as the right subarray. Because we know
that the subarray AŒlow : : high contains at least two elements, each of the left and
right subarrays must have at least one element. Lines 4 and 5 conquer by recur-
sively ﬁnding maximum subarrays within the left and right subarrays, respectively.
Lines 6–11 form the combine part. Line 6 ﬁnds a maximum subarray that crosses
the midpoint. (Recall that because line 6 solves a subproblem that is not a smaller
instance of the original problem, we consider it to be in the combine part.) Line 7
tests whether the left subarray contains a subarray with the maximum sum, and
line 8 returns that maximum subarray. Otherwise, line 9 tests whether the right
subarray contains a subarray with the maximum sum, and line 10 returns that max-
imum subarray. If neither the left nor right subarrays contain a subarray achieving
the maximum sum, then a maximum subarray must cross the midpoint, and line 11
returns it.
Analyzing the divide-and-conquer algorithm
Next we set up a recurrence that describes the running time of the recursive FIND-
MAXIMUM-SUBARRAY procedure. As we did when we analyzed merge sort in
Section 2.3.2, we make the simplifying assumption that the original problem size
is a power of 2, so that all subproblem sizes are integers. We denote by T .n/ the
running time of FIND-MAXIMUM-SUBARRAY on a subarray of n elements. For
starters, line 1 takes constant time. The base case, when n D 1, is easy: line 2
takes constant time, and so
T .1/ D ‚.1/ :
(4.5)
The recursive case occurs when n > 1. Lines 1 and 3 take constant time. Each
of the subproblems solved in lines 4 and 5 is on a subarray of n=2 elements (our
assumption that the original problem size is a power of 2 ensures that n=2 is an
integer), and so we spend T .n=2/ time solving each of them. Because we have
to solve two subproblems—for the left subarray and for the right subarray—the
contribution to the running time from lines 4 and 5 comes to 2T .n=2/. As we have

74
Chapter 4
Divide-and-Conquer
already seen, the call to FIND-MAX-CROSSING-SUBARRAY in line 6 takes ‚.n/
time. Lines 7–11 take only ‚.1/ time. For the recursive case, therefore, we have
T .n/
D
‚.1/ C 2T .n=2/ C ‚.n/ C ‚.1/
D
2T .n=2/ C ‚.n/ :
(4.6)
Combining equations (4.5) and (4.6) gives us a recurrence for the running
time T .n/ of FIND-MAXIMUM-SUBARRAY:
T .n/ D
(
‚.1/
if n D 1 ;
2T .n=2/ C ‚.n/
if n > 1 :
(4.7)
This recurrence is the same as recurrence (4.1) for merge sort.
As we shall
see from the master method in Section 4.5, this recurrence has the solution
T .n/ D ‚.n lg n/. You might also revisit the recursion tree in Figure 2.5 to un-
derstand why the solution should be T .n/ D ‚.n lg n/.
Thus, we see that the divide-and-conquer method yields an algorithm that is
asymptotically faster than the brute-force method. With merge sort and now the
maximum-subarray problem, we begin to get an idea of how powerful the divide-
and-conquer method can be. Sometimes it will yield the asymptotically fastest
algorithm for a problem, and other times we can do even better. As Exercise 4.1-5
shows, there is in fact a linear-time algorithm for the maximum-subarray problem,
and it does not use divide-and-conquer.
Exercises
4.1-1
What does FIND-MAXIMUM-SUBARRAY return when all elements of A are nega-
tive?
4.1-2
Write pseudocode for the brute-force method of solving the maximum-subarray
problem. Your procedure should run in ‚.n2/ time.
4.1-3
Implement both the brute-force and recursive algorithms for the maximum-
subarray problem on your own computer. What problem size n0 gives the crossover
point at which the recursive algorithm beats the brute-force algorithm?
Then,
change the base case of the recursive algorithm to use the brute-force algorithm
whenever the problem size is less than n0. Does that change the crossover point?
4.1-4
Suppose we change the deﬁnition of the maximum-subarray problem to allow the
result to be an empty subarray, where the sum of the values of an empty subar-

4.2
Strassen’s algorithm for matrix multiplication
75
ray is 0. How would you change any of the algorithms that do not allow empty
subarrays to permit an empty subarray to be the result?
4.1-5
Use the following ideas to develop a nonrecursive, linear-time algorithm for the
maximum-subarray problem. Start at the left end of the array, and progress toward
the right, keeping track of the maximum subarray seen so far. Knowing a maximum
subarray of AŒ1 : : j , extend the answer to ﬁnd a maximum subarray ending at in-
dex j C1 by using the following observation: a maximum subarray of AŒ1 : : j C 1
is either a maximum subarray of AŒ1 : : j  or a subarray AŒi : : j C 1, for some
1  i  j C 1. Determine a maximum subarray of the form AŒi : : j C 1 in
constant time based on knowing a maximum subarray ending at index j .
4.2
Strassen’s algorithm for matrix multiplication
If you have seen matrices before, then you probably know how to multiply them.
(Otherwise, you should read Section D.1 in Appendix D.)
If A D .aij/ and
B D .bij/ are square n 	 n matrices, then in the product C D A  B, we deﬁne the
entry cij, for i; j D 1; 2; : : : ; n, by
cij D
n
X
kD1
aik  bkj :
(4.8)
We must compute n2 matrix entries, and each is the sum of n values. The following
procedure takes n 	 n matrices A and B and multiplies them, returning their n 	 n
product C. We assume that each matrix has an attribute rows, giving the number
of rows in the matrix.
SQUARE-MATRIX-MULTIPLY.A; B/
1
n D A:rows
2
let C be a new n 	 n matrix
3
for i D 1 to n
4
for j D 1 to n
5
cij D 0
6
for k D 1 to n
7
cij D cij C aik  bkj
8
return C
The SQUARE-MATRIX-MULTIPLY procedure works as follows. The for loop
of lines 3–7 computes the entries of each row i, and within a given row i, the

76
Chapter 4
Divide-and-Conquer
for loop of lines 4–7 computes each of the entries cij, for each column j . Line 5
initializes cij to 0 as we start computing the sum given in equation (4.8), and each
iteration of the for loop of lines 6–7 adds in one more term of equation (4.8).
Because each of the triply-nested for loops runs exactly n iterations, and each
execution of line 7 takes constant time, the SQUARE-MATRIX-MULTIPLY proce-
dure takes ‚.n3/ time.
You might at ﬁrst think that any matrix multiplication algorithm must take .n3/
time, since the natural deﬁnition of matrix multiplication requires that many mul-
tiplications. You would be incorrect, however: we have a way to multiply matrices
in o.n3/ time. In this section, we shall see Strassen’s remarkable recursive algo-
rithm for multiplying n 	 n matrices. It runs in ‚.nlg 7/ time, which we shall show
in Section 4.5. Since lg 7 lies between 2:80 and 2:81, Strassen’s algorithm runs in
O.n2:81/ time, which is asymptotically better than the simple SQUARE-MATRIX-
MULTIPLY procedure.
A simple divide-and-conquer algorithm
To keep things simple, when we use a divide-and-conquer algorithm to compute
the matrix product C D A  B, we assume that n is an exact power of 2 in each of
the n 	 n matrices. We make this assumption because in each divide step, we will
divide n 	 n matrices into four n=2 	 n=2 matrices, and by assuming that n is an
exact power of 2, we are guaranteed that as long as n  2, the dimension n=2 is an
integer.
Suppose that we partition each of A, B, and C into four n=2 	 n=2 matrices
A D
 A11
A12
A21
A22

;
B D
 B11
B12
B21
B22

;
C D
 C11
C12
C21
C22

;
(4.9)
so that we rewrite the equation C D A  B as
 C11
C12
C21
C22

D
 A11
A12
A21
A22


 B11
B12
B21
B22

:
(4.10)
Equation (4.10) corresponds to the four equations
C11
D
A11  B11 C A12  B21 ;
(4.11)
C12
D
A11  B12 C A12  B22 ;
(4.12)
C21
D
A21  B11 C A22  B21 ;
(4.13)
C22
D
A21  B12 C A22  B22 :
(4.14)
Each of these four equations speciﬁes two multiplications of n=2 	 n=2 matrices
and the addition of their n=2 	 n=2 products. We can use these equations to create
a straightforward, recursive, divide-and-conquer algorithm:

4.2
Strassen’s algorithm for matrix multiplication
77
SQUARE-MATRIX-MULTIPLY-RECURSIVE.A; B/
1
n D A:rows
2
let C be a new n 	 n matrix
3
if n == 1
4
c11 D a11  b11
5
else partition A, B, and C as in equations (4.9)
6
C11 D SQUARE-MATRIX-MULTIPLY-RECURSIVE.A11; B11/
C SQUARE-MATRIX-MULTIPLY-RECURSIVE.A12; B21/
7
C12 D SQUARE-MATRIX-MULTIPLY-RECURSIVE.A11; B12/
C SQUARE-MATRIX-MULTIPLY-RECURSIVE.A12; B22/
8
C21 D SQUARE-MATRIX-MULTIPLY-RECURSIVE.A21; B11/
C SQUARE-MATRIX-MULTIPLY-RECURSIVE.A22; B21/
9
C22 D SQUARE-MATRIX-MULTIPLY-RECURSIVE.A21; B12/
C SQUARE-MATRIX-MULTIPLY-RECURSIVE.A22; B22/
10
return C
This pseudocode glosses over one subtle but important implementation detail.
How do we partition the matrices in line 5? If we were to create 12 new n=2 	 n=2
matrices, we would spend ‚.n2/ time copying entries. In fact, we can partition
the matrices without copying entries. The trick is to use index calculations. We
identify a submatrix by a range of row indices and a range of column indices of
the original matrix. We end up representing a submatrix a little differently from
how we represent the original matrix, which is the subtlety we are glossing over.
The advantage is that, since we can specify submatrices by index calculations,
executing line 5 takes only ‚.1/ time (although we shall see that it makes no
difference asymptotically to the overall running time whether we copy or partition
in place).
Now, we derive a recurrence to characterize the running time of SQUARE-
MATRIX-MULTIPLY-RECURSIVE. Let T .n/ be the time to multiply two n 	 n
matrices using this procedure. In the base case, when n D 1, we perform just the
one scalar multiplication in line 4, and so
T .1/ D ‚.1/ :
(4.15)
The recursive case occurs when n > 1. As discussed, partitioning the matrices in
line 5 takes ‚.1/ time, using index calculations. In lines 6–9, we recursively call
SQUARE-MATRIX-MULTIPLY-RECURSIVE a total of eight times. Because each
recursive call multiplies two n=2 	 n=2 matrices, thereby contributing T .n=2/ to
the overall running time, the time taken by all eight recursive calls is 8T .n=2/. We
also must account for the four matrix additions in lines 6–9. Each of these matrices
contains n2=4 entries, and so each of the four matrix additions takes ‚.n2/ time.
Since the number of matrix additions is a constant, the total time spent adding ma-

78
Chapter 4
Divide-and-Conquer
trices in lines 6–9 is ‚.n2/. (Again, we use index calculations to place the results
of the matrix additions into the correct positions of matrix C, with an overhead
of ‚.1/ time per entry.) The total time for the recursive case, therefore, is the sum
of the partitioning time, the time for all the recursive calls, and the time to add the
matrices resulting from the recursive calls:
T .n/
D
‚.1/ C 8T .n=2/ C ‚.n2/
D
8T .n=2/ C ‚.n2/ :
(4.16)
Notice that if we implemented partitioning by copying matrices, which would cost
‚.n2/ time, the recurrence would not change, and hence the overall running time
would increase by only a constant factor.
Combining equations (4.15) and (4.16) gives us the recurrence for the running
time of SQUARE-MATRIX-MULTIPLY-RECURSIVE:
T .n/ D
(
‚.1/
if n D 1 ;
8T .n=2/ C ‚.n2/
if n > 1 :
(4.17)
As we shall see from the master method in Section 4.5, recurrence (4.17) has the
solution T .n/ D ‚.n3/. Thus, this simple divide-and-conquer approach is no
faster than the straightforward SQUARE-MATRIX-MULTIPLY procedure.
Before we continue on to examining Strassen’s algorithm, let us review where
the components of equation (4.16) came from. Partitioning each n 	 n matrix by
index calculation takes ‚.1/ time, but we have two matrices to partition. Although
you could say that partitioning the two matrices takes ‚.2/ time, the constant of 2
is subsumed by the ‚-notation. Adding two matrices, each with, say, k entries,
takes ‚.k/ time. Since the matrices we add each have n2=4 entries, you could
say that adding each pair takes ‚.n2=4/ time. Again, however, the ‚-notation
subsumes the constant factor of 1=4, and we say that adding two n2=4 	 n2=4
matrices takes ‚.n2/ time. We have four such matrix additions, and once again,
instead of saying that they take ‚.4n2/ time, we say that they take ‚.n2/ time.
(Of course, you might observe that we could say that the four matrix additions
take ‚.4n2=4/ time, and that 4n2=4 D n2, but the point here is that ‚-notation
subsumes constant factors, whatever they are.) Thus, we end up with two terms
of ‚.n2/, which we can combine into one.
When we account for the eight recursive calls, however, we cannot just sub-
sume the constant factor of 8. In other words, we must say that together they take
8T .n=2/ time, rather than just T .n=2/ time. You can get a feel for why by looking
back at the recursion tree in Figure 2.5, for recurrence (2.1) (which is identical to
recurrence (4.7)), with the recursive case T .n/ D 2T .n=2/C‚.n/. The factor of 2
determined how many children each tree node had, which in turn determined how
many terms contributed to the sum at each level of the tree. If we were to ignore

4.2
Strassen’s algorithm for matrix multiplication
79
the factor of 8 in equation (4.16) or the factor of 2 in recurrence (4.1), the recursion
tree would just be linear, rather than “bushy,” and each level would contribute only
one term to the sum.
Bear in mind, therefore, that although asymptotic notation subsumes constant
multiplicative factors, recursive notation such as T .n=2/ does not.
Strassen’s method
The key to Strassen’s method is to make the recursion tree slightly less bushy. That
is, instead of performing eight recursive multiplications of n=2 	 n=2 matrices,
it performs only seven. The cost of eliminating one matrix multiplication will be
several new additions of n=2 	 n=2 matrices, but still only a constant number of
additions. As before, the constant number of matrix additions will be subsumed
by ‚-notation when we set up the recurrence equation to characterize the running
time.
Strassen’s method is not at all obvious. (This might be the biggest understate-
ment in this book.) It has four steps:
1. Divide the input matrices A and B and output matrix C into n=2 	 n=2 subma-
trices, as in equation (4.9). This step takes ‚.1/ time by index calculation, just
as in SQUARE-MATRIX-MULTIPLY-RECURSIVE.
2. Create 10 matrices S1; S2; : : : ; S10, each of which is n=2 	 n=2 and is the sum
or difference of two matrices created in step 1. We can create all 10 matrices in
‚.n2/ time.
3. Using the submatrices created in step 1 and the 10 matrices created in step 2,
recursively compute seven matrix products P1; P2; : : : ; P7. Each matrix Pi is
n=2 	 n=2.
4. Compute the desired submatrices C11; C12; C21; C22 of the result matrix C by
adding and subtracting various combinations of the Pi matrices. We can com-
pute all four submatrices in ‚.n2/ time.
We shall see the details of steps 2–4 in a moment, but we already have enough
information to set up a recurrence for the running time of Strassen’s method. Let us
assume that once the matrix size n gets down to 1, we perform a simple scalar mul-
tiplication, just as in line 4 of SQUARE-MATRIX-MULTIPLY-RECURSIVE. When
n > 1, steps 1, 2, and 4 take a total of ‚.n2/ time, and step 3 requires us to per-
form seven multiplications of n=2 	 n=2 matrices. Hence, we obtain the following
recurrence for the running time T .n/ of Strassen’s algorithm:
T .n/ D
(
‚.1/
if n D 1 ;
7T .n=2/ C ‚.n2/
if n > 1 :
(4.18)

80
Chapter 4
Divide-and-Conquer
We have traded off one matrix multiplication for a constant number of matrix ad-
ditions. Once we understand recurrences and their solutions, we shall see that this
tradeoff actually leads to a lower asymptotic running time. By the master method
in Section 4.5, recurrence (4.18) has the solution T .n/ D ‚.nlg 7/.
We now proceed to describe the details. In step 2, we create the following 10
matrices:
S1
D
B12  B22 ;
S2
D
A11 C A12 ;
S3
D
A21 C A22 ;
S4
D
B21  B11 ;
S5
D
A11 C A22 ;
S6
D
B11 C B22 ;
S7
D
A12  A22 ;
S8
D
B21 C B22 ;
S9
D
A11  A21 ;
S10
D
B11 C B12 :
Since we must add or subtract n=2 	 n=2 matrices 10 times, this step does indeed
take ‚.n2/ time.
In step 3, we recursively multiply n=2	n=2 matrices seven times to compute the
following n=2 	 n=2 matrices, each of which is the sum or difference of products
of A and B submatrices:
P1 D A11  S1 D A11  B12  A11  B22 ;
P2 D S2  B22 D A11  B22 C A12  B22 ;
P3 D S3  B11 D A21  B11 C A22  B11 ;
P4 D A22  S4 D A22  B21  A22  B11 ;
P5 D S5  S6
D A11  B11 C A11  B22 C A22  B11 C A22  B22 ;
P6 D S7  S8
D A12  B21 C A12  B22  A22  B21  A22  B22 ;
P7 D S9  S10
D A11  B11 C A11  B12  A21  B11  A21  B12 :
Note that the only multiplications we need to perform are those in the middle col-
umn of the above equations. The right-hand column just shows what these products
equal in terms of the original submatrices created in step 1.
Step 4 adds and subtracts the Pi matrices created in step 3 to construct the four
n=2 	 n=2 submatrices of the product C. We start with
C11 D P5 C P4  P2 C P6 :

4.2
Strassen’s algorithm for matrix multiplication
81
Expanding out the right-hand side, with the expansion of each Pi on its own line
and vertically aligning terms that cancel out, we see that C11 equals
A11 B11 CA11 B22 CA22 B11 CA22 B22
 A22 B11
CA22 B21
 A11 B22
 A12 B22
 A22 B22  A22 B21 CA12 B22 CA12 B21
A11 B11
CA12 B21 ;
which corresponds to equation (4.11).
Similarly, we set
C12 D P1 C P2 ;
and so C12 equals
A11 B12  A11 B22
C A11 B22 C A12 B22
A11 B12
C A12 B22 ;
corresponding to equation (4.12).
Setting
C21 D P3 C P4
makes C21 equal
A21 B11 C A22 B11
 A22 B11 C A22 B21
A21 B11
C A22 B21 ;
corresponding to equation (4.13).
Finally, we set
C22 D P5 C P1  P3  P7 ;
so that C22 equals
A11 B11 CA11 B22 CA22 B11 CA22 B22
 A11 B22
CA11 B12
 A22 B11
 A21 B11
A11 B11
 A11 B12 CA21 B11 CA21 B12
A22 B22
CA21 B12 ;

82
Chapter 4
Divide-and-Conquer
which corresponds to equation (4.14). Altogether, we add or subtract n=2 	 n=2
matrices eight times in step 4, and so this step indeed takes ‚.n2/ time.
Thus, we see that Strassen’s algorithm, comprising steps 1–4, produces the cor-
rect matrix product and that recurrence (4.18) characterizes its running time. Since
we shall see in Section 4.5 that this recurrence has the solution T .n/ D ‚.nlg 7/,
Strassen’s method is asymptotically faster than the straightforward SQUARE-
MATRIX-MULTIPLY procedure. The notes at the end of this chapter discuss some
of the practical aspects of Strassen’s algorithm.
Exercises
Note: Although Exercises 4.2-3, 4.2-4, and 4.2-5 are about variants on Strassen’s
algorithm, you should read Section 4.5 before trying to solve them.
4.2-1
Use Strassen’s algorithm to compute the matrix product
 1
3
7
5
 6
8
4
2

:
Show your work.
4.2-2
Write pseudocode for Strassen’s algorithm.
4.2-3
How would you modify Strassen’s algorithm to multiply n	n matrices in which n
is not an exact power of 2? Show that the resulting algorithm runs in time ‚.nlg 7/.
4.2-4
What is the largest k such that if you can multiply 3 	 3 matrices using k multi-
plications (not assuming commutativity of multiplication), then you can multiply
n 	 n matrices in time o.nlg 7/? What would the running time of this algorithm be?
4.2-5
V. Pan has discovered a way of multiplying 68 	 68 matrices using 132,464 mul-
tiplications, a way of multiplying 70 	 70 matrices using 143,640 multiplications,
and a way of multiplying 72 	 72 matrices using 155,424 multiplications. Which
method yields the best asymptotic running time when used in a divide-and-conquer
matrix-multiplication algorithm? How does it compare to Strassen’s algorithm?

4.3
The substitution method for solving recurrences
83
4.2-6
How quickly can you multiply a kn	n matrix by an n	kn matrix, using Strassen’s
algorithm as a subroutine? Answer the same question with the order of the input
matrices reversed.
4.2-7
Show how to multiply the complex numbers a C bi and c C di using only three
multiplications of real numbers. The algorithm should take a, b, c, and d as input
and produce the real component ac  bd and the imaginary component ad C bc
separately.
4.3
The substitution method for solving recurrences
Now that we have seen how recurrences characterize the running times of divide-
and-conquer algorithms, we will learn how to solve recurrences. We start in this
section with the “substitution” method.
The substitution method for solving recurrences comprises two steps:
1. Guess the form of the solution.
2. Use mathematical induction to ﬁnd the constants and show that the solution
works.
We substitute the guessed solution for the function when applying the inductive
hypothesis to smaller values; hence the name “substitution method.” This method
is powerful, but we must be able to guess the form of the answer in order to apply it.
We can use the substitution method to establish either upper or lower bounds on
a recurrence. As an example, let us determine an upper bound on the recurrence
T .n/ D 2T .bn=2c/ C n ;
(4.19)
which is similar to recurrences (4.3) and (4.4).
We guess that the solution is
T .n/ D O.n lg n/.
The substitution method requires us to prove that T .n/ 
cn lg n for an appropriate choice of the constant c > 0. We start by assuming
that this bound holds for all positive m < n, in particular for m D bn=2c, yielding
T .bn=2c/  c bn=2c lg.bn=2c/. Substituting into the recurrence yields
T .n/

2.c bn=2c lg.bn=2c// C n

cn lg.n=2/ C n
D
cn lg n  cn lg 2 C n
D
cn lg n  cn C n

cn lg n ;

84
Chapter 4
Divide-and-Conquer
where the last step holds as long as c  1.
Mathematical induction now requires us to show that our solution holds for the
boundary conditions. Typically, we do so by showing that the boundary condi-
tions are suitable as base cases for the inductive proof. For the recurrence (4.19),
we must show that we can choose the constant c large enough so that the bound
T .n/  cn lg n works for the boundary conditions as well.
This requirement
can sometimes lead to problems. Let us assume, for the sake of argument, that
T .1/ D 1 is the sole boundary condition of the recurrence. Then for n D 1, the
bound T .n/  cn lg n yields T .1/  c1 lg 1 D 0, which is at odds with T .1/ D 1.
Consequently, the base case of our inductive proof fails to hold.
We can overcome this obstacle in proving an inductive hypothesis for a spe-
ciﬁc boundary condition with only a little more effort. In the recurrence (4.19),
for example, we take advantage of asymptotic notation requiring us only to prove
T .n/  cn lg n for n  n0, where n0 is a constant that we get to choose. We
keep the troublesome boundary condition T .1/ D 1, but remove it from consid-
eration in the inductive proof. We do so by ﬁrst observing that for n > 3, the
recurrence does not depend directly on T .1/. Thus, we can replace T .1/ by T .2/
and T .3/ as the base cases in the inductive proof, letting n0 D 2. Note that we
make a distinction between the base case of the recurrence (n D 1) and the base
cases of the inductive proof (n D 2 and n D 3). With T .1/ D 1, we derive from
the recurrence that T .2/ D 4 and T .3/ D 5. Now we can complete the inductive
proof that T .n/  cn lg n for some constant c  1 by choosing c large enough
so that T .2/  c2 lg 2 and T .3/  c3 lg 3. As it turns out, any choice of c  2
sufﬁces for the base cases of n D 2 and n D 3 to hold. For most of the recurrences
we shall examine, it is straightforward to extend boundary conditions to make the
inductive assumption work for small n, and we shall not always explicitly work out
the details.
Making a good guess
Unfortunately, there is no general way to guess the correct solutions to recurrences.
Guessing a solution takes experience and, occasionally, creativity. Fortunately,
though, you can use some heuristics to help you become a good guesser. You
can also use recursion trees, which we shall see in Section 4.4, to generate good
guesses.
If a recurrence is similar to one you have seen before, then guessing a similar
solution is reasonable. As an example, consider the recurrence
T .n/ D 2T .bn=2c C 17/ C n ;
which looks difﬁcult because of the added “17” in the argument to T on the right-
hand side. Intuitively, however, this additional term cannot substantially affect the

4.3
The substitution method for solving recurrences
85
solution to the recurrence. When n is large, the difference between bn=2c and
bn=2c C 17 is not that large: both cut n nearly evenly in half. Consequently, we
make the guess that T .n/ D O.n lg n/, which you can verify as correct by using
the substitution method (see Exercise 4.3-6).
Another way to make a good guess is to prove loose upper and lower bounds on
the recurrence and then reduce the range of uncertainty. For example, we might
start with a lower bound of T .n/ D .n/ for the recurrence (4.19), since we
have the term n in the recurrence, and we can prove an initial upper bound of
T .n/ D O.n2/. Then, we can gradually lower the upper bound and raise the
lower bound until we converge on the correct, asymptotically tight solution of
T .n/ D ‚.n lg n/.
Subtleties
Sometimes you might correctly guess an asymptotic bound on the solution of a
recurrence, but somehow the math fails to work out in the induction. The problem
frequently turns out to be that the inductive assumption is not strong enough to
prove the detailed bound. If you revise the guess by subtracting a lower-order term
when you hit such a snag, the math often goes through.
Consider the recurrence
T .n/ D T .bn=2c/ C T .dn=2e/ C 1 :
We guess that the solution is T .n/ D O.n/, and we try to show that T .n/  cn for
an appropriate choice of the constant c. Substituting our guess in the recurrence,
we obtain
T .n/

c bn=2c C c dn=2e C 1
D
cn C 1 ;
which does not imply T .n/  cn for any choice of c. We might be tempted to try
a larger guess, say T .n/ D O.n2/. Although we can make this larger guess work,
our original guess of T .n/ D O.n/ is correct. In order to show that it is correct,
however, we must make a stronger inductive hypothesis.
Intuitively, our guess is nearly right: we are off only by the constant 1, a
lower-order term. Nevertheless, mathematical induction does not work unless we
prove the exact form of the inductive hypothesis.
We overcome our difﬁculty
by subtracting a lower-order term from our previous guess. Our new guess is
T .n/  cn  d, where d  0 is a constant. We now have
T .n/

.c bn=2c  d/ C .c dn=2e  d/ C 1
D
cn  2d C 1

cn  d ;

86
Chapter 4
Divide-and-Conquer
as long as d  1. As before, we must choose the constant c large enough to handle
the boundary conditions.
You might ﬁnd the idea of subtracting a lower-order term counterintuitive. Af-
ter all, if the math does not work out, we should increase our guess, right?
Not necessarily! When proving an upper bound by induction, it may actually be
more difﬁcult to prove that a weaker upper bound holds, because in order to prove
the weaker bound, we must use the same weaker bound inductively in the proof.
In our current example, when the recurrence has more than one recursive term, we
get to subtract out the lower-order term of the proposed bound once per recursive
term. In the above example, we subtracted out the constant d twice, once for the
T .bn=2c/ term and once for the T .dn=2e/ term. We ended up with the inequality
T .n/  cn  2d C 1, and it was easy to ﬁnd values of d to make cn  2d C 1 be
less than or equal to cn  d.
Avoiding pitfalls
It is easy to err in the use of asymptotic notation.
For example, in the recur-
rence (4.19) we can falsely “prove” T .n/ D O.n/ by guessing T .n/  cn and
then arguing
T .n/

2.c bn=2c/ C n

cn C n
D
O.n/ ;

 wrong!!
since c is a constant. The error is that we have not proved the exact form of the
inductive hypothesis, that is, that T .n/  cn. We therefore will explicitly prove
that T .n/  cn when we want to show that T .n/ D O.n/.
Changing variables
Sometimes, a little algebraic manipulation can make an unknown recurrence simi-
lar to one you have seen before. As an example, consider the recurrence
T .n/ D 2T

pn
˘

C lg n ;
which looks difﬁcult. We can simplify this recurrence, though, with a change of
variables. For convenience, we shall not worry about rounding off values, such
as pn, to be integers. Renaming m D lg n yields
T .2m/ D 2T .2m=2/ C m :
We can now rename S.m/ D T .2m/ to produce the new recurrence
S.m/ D 2S.m=2/ C m ;

4.3
The substitution method for solving recurrences
87
which is very much like recurrence (4.19). Indeed, this new recurrence has the
same solution: S.m/ D O.m lg m/. Changing back from S.m/ to T .n/, we obtain
T .n/ D T .2m/ D S.m/ D O.m lg m/ D O.lg n lg lg n/ :
Exercises
4.3-1
Show that the solution of T .n/ D T .n  1/ C n is O.n2/.
4.3-2
Show that the solution of T .n/ D T .dn=2e/ C 1 is O.lg n/.
4.3-3
We saw that the solution of T .n/ D 2T .bn=2c/Cn is O.n lg n/. Show that the so-
lution of this recurrence is also .n lg n/. Conclude that the solution is ‚.n lg n/.
4.3-4
Show that by making a different inductive hypothesis, we can overcome the difﬁ-
culty with the boundary condition T .1/ D 1 for recurrence (4.19) without adjusting
the boundary conditions for the inductive proof.
4.3-5
Show that ‚.n lg n/ is the solution to the “exact” recurrence (4.3) for merge sort.
4.3-6
Show that the solution to T .n/ D 2T .bn=2c C 17/ C n is O.n lg n/.
4.3-7
Using the master method in Section 4.5, you can show that the solution to the
recurrence T .n/ D 4T .n=3/ C n is T .n/ D ‚.nlog3 4/. Show that a substitution
proof with the assumption T .n/  cnlog3 4 fails. Then show how to subtract off a
lower-order term to make a substitution proof work.
4.3-8
Using the master method in Section 4.5, you can show that the solution to the
recurrence T .n/ D 4T .n=2/ C n2 is T .n/ D ‚.n2/. Show that a substitution
proof with the assumption T .n/  cn2 fails. Then show how to subtract off a
lower-order term to make a substitution proof work.

88
Chapter 4
Divide-and-Conquer
4.3-9
Solve the recurrence T .n/ D 3T .pn/ C log n by making a change of variables.
Your solution should be asymptotically tight. Do not worry about whether values
are integral.
4.4
The recursion-tree method for solving recurrences
Although you can use the substitution method to provide a succinct proof that
a solution to a recurrence is correct, you might have trouble coming up with a
good guess. Drawing out a recursion tree, as we did in our analysis of the merge
sort recurrence in Section 2.3.2, serves as a straightforward way to devise a good
guess. In a recursion tree, each node represents the cost of a single subproblem
somewhere in the set of recursive function invocations. We sum the costs within
each level of the tree to obtain a set of per-level costs, and then we sum all the
per-level costs to determine the total cost of all levels of the recursion.
A recursion tree is best used to generate a good guess, which you can then verify
by the substitution method. When using a recursion tree to generate a good guess,
you can often tolerate a small amount of “sloppiness,” since you will be verifying
your guess later on. If you are very careful when drawing out a recursion tree and
summing the costs, however, you can use a recursion tree as a direct proof of a
solution to a recurrence. In this section, we will use recursion trees to generate
good guesses, and in Section 4.6, we will use recursion trees directly to prove the
theorem that forms the basis of the master method.
For example, let us see how a recursion tree would provide a good guess for
the recurrence T .n/ D 3T .bn=4c/ C ‚.n2/. We start by focusing on ﬁnding an
upper bound for the solution. Because we know that ﬂoors and ceilings usually do
not matter when solving recurrences (here’s an example of sloppiness that we can
tolerate), we create a recursion tree for the recurrence T .n/ D 3T .n=4/ C cn2,
having written out the implied constant coefﬁcient c > 0.
Figure 4.5 shows how we derive the recursion tree for T .n/ D 3T .n=4/ C cn2.
For convenience, we assume that n is an exact power of 4 (another example of
tolerable sloppiness) so that all subproblem sizes are integers. Part (a) of the ﬁgure
shows T .n/, which we expand in part (b) into an equivalent tree representing the
recurrence. The cn2 term at the root represents the cost at the top level of recursion,
and the three subtrees of the root represent the costs incurred by the subproblems
of size n=4. Part (c) shows this process carried one step further by expanding each
node with cost T .n=4/ from part (b). The cost for each of the three children of the
root is c.n=4/2. We continue expanding each node in the tree by breaking it into
its constituent parts as determined by the recurrence.

4.4
The recursion-tree method for solving recurrences
89
…
…
(d)
(c)
(b)
(a)
T .n/
cn2
cn2
cn2
T

 n
4

T

 n
4

T

 n
4

T

 n
16

T

 n
16

T

 n
16

T

 n
16

T

 n
16

T

 n
16

T

 n
16

T

 n
16

T

 n
16

cn2
c

 n
4

2
c

 n
4

2
c

 n
4

2
c

 n
4

2
c

 n
4

2
c

 n
4

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
c

 n
16

2
3
16 cn2

 3
16

2 cn2
log4 n
nlog4 3
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
T .1/
‚.nlog4 3/
Total: O.n2/
Figure 4.5
Constructing a recursion tree for the recurrence T .n/ D 3T .n=4/ C cn2. Part (a)
shows T .n/, which progressively expands in (b)–(d) to form the recursion tree. The fully expanded
tree in part (d) has height log4 n (it has log4 n C 1 levels).

90
Chapter 4
Divide-and-Conquer
Because subproblem sizes decrease by a factor of 4 each time we go down one
level, we eventually must reach a boundary condition. How far from the root do
we reach one? The subproblem size for a node at depth i is n=4i. Thus, the
subproblem size hits n D 1 when n=4i D 1 or, equivalently, when i D log4 n.
Thus, the tree has log4 n C 1 levels (at depths 0; 1; 2; : : : ; log4 n).
Next we determine the cost at each level of the tree. Each level has three times
more nodes than the level above, and so the number of nodes at depth i is 3i.
Because subproblem sizes reduce by a factor of 4 for each level we go down
from the root, each node at depth i, for i D 0; 1; 2; : : : ; log4 n  1, has a cost
of c.n=4i/2. Multiplying, we see that the total cost over all nodes at depth i, for
i D 0; 1; 2; : : : ; log4 n  1, is 3ic.n=4i/2 D .3=16/icn2. The bottom level, at
depth log4 n, has 3log4 n D nlog4 3 nodes, each contributing cost T .1/, for a total
cost of nlog4 3T .1/, which is ‚.nlog4 3/, since we assume that T .1/ is a constant.
Now we add up the costs over all levels to determine the cost for the entire tree:
T .n/
D
cn2 C 3
16 cn2 C
 3
16
2
cn2 C    C
 3
16
log4 n1
cn2 C ‚.nlog4 3/
D
log4 n1
X
iD0
 3
16
i
cn2 C ‚.nlog4 3/
D
.3=16/log4 n  1
.3=16/  1
cn2 C ‚.nlog4 3/
(by equation (A.5)) :
This last formula looks somewhat messy until we realize that we can again take
advantage of small amounts of sloppiness and use an inﬁnite decreasing geometric
series as an upper bound. Backing up one step and applying equation (A.6), we
have
T .n/
D
log4 n1
X
iD0
 3
16
i
cn2 C ‚.nlog4 3/
<
1
X
iD0
 3
16
i
cn2 C ‚.nlog4 3/
D
1
1  .3=16/ cn2 C ‚.nlog4 3/
D
16
13 cn2 C ‚.nlog4 3/
D
O.n2/ :
Thus, we have derived a guess of T .n/ D O.n2/ for our original recurrence
T .n/ D 3T .bn=4c/ C ‚.n2/. In this example, the coefﬁcients of cn2 form a
decreasing geometric series and, by equation (A.6), the sum of these coefﬁcients

4.4
The recursion-tree method for solving recurrences
91
…
…
cn
cn
cn
cn
c

 n
3

c

 2n
3

c

 n
9

c

 2n
9

c

 2n
9

c

 4n
9

log3=2 n
Total: O.n lg n/
Figure 4.6
A recursion tree for the recurrence T .n/ D T .n=3/ C T .2n=3/ C cn.
is bounded from above by the constant 16=13. Since the root’s contribution to the
total cost is cn2, the root contributes a constant fraction of the total cost. In other
words, the cost of the root dominates the total cost of the tree.
In fact, if O.n2/ is indeed an upper bound for the recurrence (as we shall verify in
a moment), then it must be a tight bound. Why? The ﬁrst recursive call contributes
a cost of ‚.n2/, and so .n2/ must be a lower bound for the recurrence.
Now we can use the substitution method to verify that our guess was cor-
rect, that is, T .n/ D O.n2/ is an upper bound for the recurrence T .n/ D
3T .bn=4c/ C ‚.n2/. We want to show that T .n/  dn2 for some constant d > 0.
Using the same constant c > 0 as before, we have
T .n/

3T .bn=4c/ C cn2

3d bn=4c2 C cn2

3d.n=4/2 C cn2
D
3
16 dn2 C cn2

dn2 ;
where the last step holds as long as d  .16=13/c.
In another, more intricate, example, Figure 4.6 shows the recursion tree for
T .n/ D T .n=3/ C T .2n=3/ C O.n/ :
(Again, we omit ﬂoor and ceiling functions for simplicity.) As before, we let c
represent the constant factor in the O.n/ term. When we add the values across the
levels of the recursion tree shown in the ﬁgure, we get a value of cn for every level.

92
Chapter 4
Divide-and-Conquer
The longest simple path from the root to a leaf is n ! .2=3/n ! .2=3/2n !
   ! 1. Since .2=3/kn D 1 when k D log3=2 n, the height of the tree is log3=2 n.
Intuitively, we expect the solution to the recurrence to be at most the number
of levels times the cost of each level, or O.cn log3=2 n/ D O.n lg n/. Figure 4.6
shows only the top levels of the recursion tree, however, and not every level in the
tree contributes a cost of cn. Consider the cost of the leaves. If this recursion tree
were a complete binary tree of height log3=2 n, there would be 2log3=2 n D nlog3=2 2
leaves. Since the cost of each leaf is a constant, the total cost of all leaves would
then be ‚.nlog3=2 2/ which, since log3=2 2 is a constant strictly greater than 1,
is !.n lg n/. This recursion tree is not a complete binary tree, however, and so
it has fewer than nlog3=2 2 leaves. Moreover, as we go down from the root, more
and more internal nodes are absent. Consequently, levels toward the bottom of the
recursion tree contribute less than cn to the total cost. We could work out an accu-
rate accounting of all costs, but remember that we are just trying to come up with a
guess to use in the substitution method. Let us tolerate the sloppiness and attempt
to show that a guess of O.n lg n/ for the upper bound is correct.
Indeed, we can use the substitution method to verify that O.n lg n/ is an upper
bound for the solution to the recurrence. We show that T .n/  dn lg n, where d is
a suitable positive constant. We have
T .n/

T .n=3/ C T .2n=3/ C cn

d.n=3/ lg.n=3/ C d.2n=3/ lg.2n=3/ C cn
D
.d.n=3/ lg n  d.n=3/ lg 3/
C .d.2n=3/ lg n  d.2n=3/ lg.3=2// C cn
D
dn lg n  d..n=3/ lg 3 C .2n=3/ lg.3=2// C cn
D
dn lg n  d..n=3/ lg 3 C .2n=3/ lg 3  .2n=3/ lg 2/ C cn
D
dn lg n  dn.lg 3  2=3/ C cn

dn lg n ;
as long as d  c=.lg 3.2=3//. Thus, we did not need to perform a more accurate
accounting of costs in the recursion tree.
Exercises
4.4-1
Use a recursion tree to determine a good asymptotic upper bound on the recurrence
T .n/ D 3T .bn=2c/ C n. Use the substitution method to verify your answer.
4.4-2
Use a recursion tree to determine a good asymptotic upper bound on the recurrence
T .n/ D T .n=2/ C n2. Use the substitution method to verify your answer.

4.5
The master method for solving recurrences
93
4.4-3
Use a recursion tree to determine a good asymptotic upper bound on the recurrence
T .n/ D 4T .n=2 C 2/ C n. Use the substitution method to verify your answer.
4.4-4
Use a recursion tree to determine a good asymptotic upper bound on the recurrence
T .n/ D 2T .n  1/ C 1. Use the substitution method to verify your answer.
4.4-5
Use a recursion tree to determine a good asymptotic upper bound on the recurrence
T .n/ D T .n1/CT .n=2/Cn. Use the substitution method to verify your answer.
4.4-6
Argue that the solution to the recurrence T .n/ D T .n=3/CT .2n=3/Ccn, where c
is a constant, is .n lg n/ by appealing to a recursion tree.
4.4-7
Draw the recursion tree for T .n/ D 4T .bn=2c/ C cn, where c is a constant, and
provide a tight asymptotic bound on its solution. Verify your bound by the substi-
tution method.
4.4-8
Use a recursion tree to give an asymptotically tight solution to the recurrence
T .n/ D T .n  a/ C T .a/ C cn, where a  1 and c > 0 are constants.
4.4-9
Use a recursion tree to give an asymptotically tight solution to the recurrence
T .n/ D T .˛n/ C T ..1  ˛/n/ C cn, where ˛ is a constant in the range 0 < ˛ < 1
and c > 0 is also a constant.
4.5
The master method for solving recurrences
The master method provides a “cookbook” method for solving recurrences of the
form
T .n/ D aT .n=b/ C f .n/ ;
(4.20)
where a  1 and b > 1 are constants and f .n/ is an asymptotically positive
function. To use the master method, you will need to memorize three cases, but
then you will be able to solve many recurrences quite easily, often without pencil
and paper.

94
Chapter 4
Divide-and-Conquer
The recurrence (4.20) describes the running time of an algorithm that divides a
problem of size n into a subproblems, each of size n=b, where a and b are positive
constants. The a subproblems are solved recursively, each in time T .n=b/. The
function f .n/ encompasses the cost of dividing the problem and combining the
results of the subproblems. For example, the recurrence arising from Strassen’s
algorithm has a D 7, b D 2, and f .n/ D ‚.n2/.
As a matter of technical correctness, the recurrence is not actually well deﬁned,
because n=b might not be an integer. Replacing each of the a terms T .n=b/ with
either T .bn=bc/ or T .dn=be/ will not affect the asymptotic behavior of the recur-
rence, however. (We will prove this assertion in the next section.) We normally
ﬁnd it convenient, therefore, to omit the ﬂoor and ceiling functions when writing
divide-and-conquer recurrences of this form.
The master theorem
The master method depends on the following theorem.
Theorem 4.1 (Master theorem)
Let a  1 and b > 1 be constants, let f .n/ be a function, and let T .n/ be deﬁned
on the nonnegative integers by the recurrence
T .n/ D aT .n=b/ C f .n/ ;
where we interpret n=b to mean either bn=bc or dn=be. Then T .n/ has the follow-
ing asymptotic bounds:
1. If f .n/ D O.nlogb a/ for some constant  > 0, then T .n/ D ‚.nlogb a/.
2. If f .n/ D ‚.nlogb a/, then T .n/ D ‚.nlogb a lg n/.
3. If f .n/ D .nlogb aC/ for some constant  > 0, and if af .n=b/  cf .n/ for
some constant c < 1 and all sufﬁciently large n, then T .n/ D ‚.f .n//.
Before applying the master theorem to some examples, let’s spend a moment
trying to understand what it says. In each of the three cases, we compare the
function f .n/ with the function nlogb a. Intuitively, the larger of the two functions
determines the solution to the recurrence. If, as in case 1, the function nlogb a is the
larger, then the solution is T .n/ D ‚.nlogb a/. If, as in case 3, the function f .n/
is the larger, then the solution is T .n/ D ‚.f .n//. If, as in case 2, the two func-
tions are the same size, we multiply by a logarithmic factor, and the solution is
T .n/ D ‚.nlogb a lg n/ D ‚.f .n/ lgn/.
Beyond this intuition, you need to be aware of some technicalities. In the ﬁrst
case, not only must f .n/ be smaller than nlogb a, it must be polynomially smaller.

4.5
The master method for solving recurrences
95
That is, f .n/ must be asymptotically smaller than nlogb a by a factor of n for some
constant  > 0. In the third case, not only must f .n/ be larger than nlogb a, it also
must be polynomially larger and in addition satisfy the “regularity” condition that
af .n=b/  cf .n/. This condition is satisﬁed by most of the polynomially bounded
functions that we shall encounter.
Note that the three cases do not cover all the possibilities for f .n/. There is
a gap between cases 1 and 2 when f .n/ is smaller than nlogb a but not polynomi-
ally smaller. Similarly, there is a gap between cases 2 and 3 when f .n/ is larger
than nlogb a but not polynomially larger. If the function f .n/ falls into one of these
gaps, or if the regularity condition in case 3 fails to hold, you cannot use the master
method to solve the recurrence.
Using the master method
To use the master method, we simply determine which case (if any) of the master
theorem applies and write down the answer.
As a ﬁrst example, consider
T .n/ D 9T .n=3/ C n :
For this recurrence, we have a D 9, b D 3, f .n/ D n, and thus we have that
nlogb a D nlog3 9 D ‚.n2). Since f .n/ D O.nlog3 9/, where  D 1, we can apply
case 1 of the master theorem and conclude that the solution is T .n/ D ‚.n2/.
Now consider
T .n/ D T .2n=3/ C 1;
in which a D 1, b D 3=2, f .n/ D 1, and nlogb a D nlog3=2 1 D n0 D 1. Case 2
applies, since f .n/ D ‚.nlogb a/ D ‚.1/, and thus the solution to the recurrence
is T .n/ D ‚.lg n/.
For the recurrence
T .n/ D 3T .n=4/ C n lg n ;
we have a D 3, b D 4, f .n/ D n lg n, and nlogb a D nlog4 3 D O.n0:793/.
Since f .n/ D .nlog4 3C/, where   0:2, case 3 applies if we can show that
the regularity condition holds for f .n/. For sufﬁciently large n, we have that
af .n=b/ D 3.n=4/ lg.n=4/  .3=4/n lg n D cf .n/ for c D 3=4. Consequently,
by case 3, the solution to the recurrence is T .n/ D ‚.n lg n/.
The master method does not apply to the recurrence
T .n/ D 2T .n=2/ C n lg n ;
even though it appears to have the proper form: a D 2, b D 2, f .n/ D n lg n,
and nlogb a D n.
You might mistakenly think that case 3 should apply, since

96
Chapter 4
Divide-and-Conquer
f .n/ D n lg n is asymptotically larger than nlogb a D n. The problem is that it
is not polynomially larger. The ratio f .n/=nlogb a D .n lg n/=n D lg n is asymp-
totically less than n for any positive constant . Consequently, the recurrence falls
into the gap between case 2 and case 3. (See Exercise 4.6-2 for a solution.)
Let’s use the master method to solve the recurrences we saw in Sections 4.1
and 4.2. Recurrence (4.7),
T .n/ D 2T .n=2/ C ‚.n/ ;
characterizes the running times of the divide-and-conquer algorithm for both the
maximum-subarray problem and merge sort. (As is our practice, we omit stating
the base case in the recurrence.) Here, we have a D 2, b D 2, f .n/ D ‚.n/, and
thus we have that nlogb a D nlog2 2 D n. Case 2 applies, since f .n/ D ‚.n/, and so
we have the solution T .n/ D ‚.n lg n/.
Recurrence (4.17),
T .n/ D 8T .n=2/ C ‚.n2/ ;
describes the running time of the ﬁrst divide-and-conquer algorithm that we saw
for matrix multiplication. Now we have a D 8, b D 2, and f .n/ D ‚.n2/,
and so nlogb a D nlog2 8 D n3. Since n3 is polynomially larger than f .n/ (that is,
f .n/ D O.n3/ for  D 1), case 1 applies, and T .n/ D ‚.n3/.
Finally, consider recurrence (4.18),
T .n/ D 7T .n=2/ C ‚.n2/ ;
which describes the running time of Strassen’s algorithm. Here, we have a D 7,
b D 2, f .n/ D ‚.n2/, and thus nlogb a D nlog2 7. Rewriting log2 7 as lg 7 and
recalling that 2:80 < lg 7 < 2:81, we see that f .n/ D O.nlg 7/ for  D 0:8.
Again, case 1 applies, and we have the solution T .n/ D ‚.nlg 7/.
Exercises
4.5-1
Use the master method to give tight asymptotic bounds for the following recur-
rences.
a. T .n/ D 2T .n=4/ C 1.
b. T .n/ D 2T .n=4/ C pn.
c. T .n/ D 2T .n=4/ C n.
d. T .n/ D 2T .n=4/ C n2.

4.6
Proof of the master theorem
97
4.5-2
Professor Caesar wishes to develop a matrix-multiplication algorithm that is
asymptotically faster than Strassen’s algorithm. His algorithm will use the divide-
and-conquer method, dividing each matrix into pieces of size n=4 	 n=4, and the
divide and combine steps together will take ‚.n2/ time. He needs to determine
how many subproblems his algorithm has to create in order to beat Strassen’s algo-
rithm. If his algorithm creates a subproblems, then the recurrence for the running
time T .n/ becomes T .n/ D aT .n=4/ C ‚.n2/. What is the largest integer value
of a for which Professor Caesar’s algorithm would be asymptotically faster than
Strassen’s algorithm?
4.5-3
Use the master method to show that the solution to the binary-search recurrence
T .n/ D T .n=2/ C ‚.1/ is T .n/ D ‚.lg n/. (See Exercise 2.3-5 for a description
of binary search.)
4.5-4
Can the master method be applied to the recurrence T .n/ D 4T .n=2/ C n2 lg n?
Why or why not? Give an asymptotic upper bound for this recurrence.
4.5-5
?
Consider the regularity condition af .n=b/  cf .n/ for some constant c < 1,
which is part of case 3 of the master theorem. Give an example of constants a  1
and b > 1 and a function f .n/ that satisﬁes all the conditions in case 3 of the
master theorem except the regularity condition.
?
4.6
Proof of the master theorem
This section contains a proof of the master theorem (Theorem 4.1). You do not
need to understand the proof in order to apply the master theorem.
The proof appears in two parts.
The ﬁrst part analyzes the master recur-
rence (4.20), under the simplifying assumption that T .n/ is deﬁned only on ex-
act powers of b > 1, that is, for n D 1; b; b2; : : :. This part gives all the intuition
needed to understand why the master theorem is true. The second part shows how
to extend the analysis to all positive integers n; it applies mathematical technique
to the problem of handling ﬂoors and ceilings.
In this section, we shall sometimes abuse our asymptotic notation slightly by
using it to describe the behavior of functions that are deﬁned only over exact
powers of b.
Recall that the deﬁnitions of asymptotic notations require that

98
Chapter 4
Divide-and-Conquer
bounds be proved for all sufﬁciently large numbers, not just those that are pow-
ers of b. Since we could make new asymptotic notations that apply only to the set
fbi W i D 0; 1; 2; : : :g, instead of to the nonnegative numbers, this abuse is minor.
Nevertheless, we must always be on guard when we use asymptotic notation over
a limited domain lest we draw improper conclusions. For example, proving that
T .n/ D O.n/ when n is an exact power of 2 does not guarantee that T .n/ D O.n/.
The function T .n/ could be deﬁned as
T .n/ D
(
n
if n D 1; 2; 4; 8; : : : ;
n2
otherwise ;
in which case the best upper bound that applies to all values of n is T .n/ D O.n2/.
Because of this sort of drastic consequence, we shall never use asymptotic notation
over a limited domain without making it absolutely clear from the context that we
are doing so.
4.6.1
The proof for exact powers
The ﬁrst part of the proof of the master theorem analyzes the recurrence (4.20)
T .n/ D aT .n=b/ C f .n/ ;
for the master method, under the assumption that n is an exact power of b > 1,
where b need not be an integer. We break the analysis into three lemmas. The ﬁrst
reduces the problem of solving the master recurrence to the problem of evaluating
an expression that contains a summation. The second determines bounds on this
summation. The third lemma puts the ﬁrst two together to prove a version of the
master theorem for the case in which n is an exact power of b.
Lemma 4.2
Let a  1 and b > 1 be constants, and let f .n/ be a nonnegative function deﬁned
on exact powers of b. Deﬁne T .n/ on exact powers of b by the recurrence
T .n/ D
(
‚.1/
if n D 1 ;
aT .n=b/ C f .n/
if n D bi ;
where i is a positive integer. Then
T .n/ D ‚.nlogb a/ C
logb n1
X
jD0
ajf .n=bj/ :
(4.21)
Proof
We use the recursion tree in Figure 4.7. The root of the tree has cost f .n/,
and it has a children, each with cost f .n=b/. (It is convenient to think of a as being

4.6
Proof of the master theorem
99
…
…
…
…
…
…
…
…
…
…
…
…
…
…
…
f .n/
f .n/
a
a
a
a
a
a
a
a
a
a
a
a
a
f .n=b/
f .n=b/
f .n=b/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
f .n=b2/
af .n=b/
a2f .n=b2/
logb n
nlogb a
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.nlogb a/
Total: ‚.nlogb a/ C
logb n1
X
jD0
ajf .n=bj/
Figure 4.7
The recursion tree generated by T .n/ D aT .n=b/ Cf .n/. The tree is a complete a-ary
tree with nlogb a leaves and height logb n. The cost of the nodes at each depth is shown at the right,
and their sum is given in equation (4.21).
an integer, especially when visualizing the recursion tree, but the mathematics does
not require it.) Each of these children has a children, making a2 nodes at depth 2,
and each of the a children has cost f .n=b2/. In general, there are aj nodes at
depth j , and each has cost f .n=bj/. The cost of each leaf is T .1/ D ‚.1/, and
each leaf is at depth logb n, since n=blogb n D 1. There are alogb n D nlogb a leaves
in the tree.
We can obtain equation (4.21) by summing the costs of the nodes at each depth
in the tree, as shown in the ﬁgure. The cost for all internal nodes at depth j is
ajf .n=bj/, and so the total cost of all internal nodes is
logb n1
X
jD0
ajf .n=bj/ :
In the underlying divide-and-conquer algorithm, this sum represents the costs of
dividing problems into subproblems and then recombining the subproblems. The

100
Chapter 4
Divide-and-Conquer
cost of all the leaves, which is the cost of doing all nlogb a subproblems of size 1,
is ‚.nlogb a/.
In terms of the recursion tree, the three cases of the master theorem correspond
to cases in which the total cost of the tree is (1) dominated by the costs in the
leaves, (2) evenly distributed among the levels of the tree, or (3) dominated by the
cost of the root.
The summation in equation (4.21) describes the cost of the dividing and com-
bining steps in the underlying divide-and-conquer algorithm. The next lemma pro-
vides asymptotic bounds on the summation’s growth.
Lemma 4.3
Let a  1 and b > 1 be constants, and let f .n/ be a nonnegative function deﬁned
on exact powers of b. A function g.n/ deﬁned over exact powers of b by
g.n/ D
logb n1
X
jD0
ajf .n=bj/
(4.22)
has the following asymptotic bounds for exact powers of b:
1. If f .n/ D O.nlogb a/ for some constant  > 0, then g.n/ D O.nlogb a/.
2. If f .n/ D ‚.nlogb a/, then g.n/ D ‚.nlogb a lg n/.
3. If af .n=b/  cf .n/ for some constant c < 1 and for all sufﬁciently large n,
then g.n/ D ‚.f .n//.
Proof
For case 1, we have f .n/ D O.nlogb a/, which implies that f .n=bj/ D
O..n=bj /logb a/. Substituting into equation (4.22) yields
g.n/ D O
 logb n1
X
jD0
aj  n
bj
logb a!
:
(4.23)
We bound the summation within the O-notation by factoring out terms and simpli-
fying, which leaves an increasing geometric series:
logb n1
X
jD0
aj  n
bj
logb a
D
nlogb a
logb n1
X
jD0
 ab
blogb a
j
D
nlogb a
logb n1
X
jD0
.b/j
D
nlogb a
b logb n  1
b  1


4.6
Proof of the master theorem
101
D
nlogb a
n  1
b  1

:
Since b and  are constants, we can rewrite the last expression as nlogb aO.n/ D
O.nlogb a/. Substituting this expression for the summation in equation (4.23) yields
g.n/ D O.nlogb a/ ;
thereby proving case 1.
Because case 2 assumes that f .n/ D ‚.nlogb a/, we have that f .n=bj/ D
‚..n=bj/logb a/. Substituting into equation (4.22) yields
g.n/ D ‚
 logb n1
X
jD0
aj  n
bj
logb a!
:
(4.24)
We bound the summation within the ‚-notation as in case 1, but this time we do not
obtain a geometric series. Instead, we discover that every term of the summation
is the same:
logb n1
X
jD0
aj  n
bj
logb a
D
nlogb a
logb n1
X
jD0

a
blogb a
j
D
nlogb a
logb n1
X
jD0
1
D
nlogb a logb n :
Substituting this expression for the summation in equation (4.24) yields
g.n/
D
‚.nlogb a logb n/
D
‚.nlogb a lg n/ ;
proving case 2.
We prove case 3 similarly. Since f .n/ appears in the deﬁnition (4.22) of g.n/
and all terms of g.n/ are nonnegative, we can conclude that g.n/ D .f .n// for
exact powers of b. We assume in the statement of the lemma that af .n=b/  cf .n/
for some constant c < 1 and all sufﬁciently large n. We rewrite this assumption
as f .n=b/  .c=a/f .n/ and iterate j times, yielding f .n=bj/  .c=a/jf .n/ or,
equivalently, ajf .n=bj/  cjf .n/, where we assume that the values we iterate
on are sufﬁciently large. Since the last, and smallest, such value is n=bj1, it is
enough to assume that n=bj1 is sufﬁciently large.
Substituting into equation (4.22) and simplifying yields a geometric series, but
unlike the series in case 1, this one has decreasing terms. We use an O.1/ term to

102
Chapter 4
Divide-and-Conquer
capture the terms that are not covered by our assumption that n is sufﬁciently large:
g.n/
D
logb n1
X
jD0
ajf .n=bj/

logb n1
X
jD0
cjf .n/ C O.1/

f .n/
1
X
jD0
cj C O.1/
D
f .n/

1
1  c

C O.1/
D
O.f .n// ;
since c is a constant. Thus, we can conclude that g.n/ D ‚.f .n// for exact powers
of b. With case 3 proved, the proof of the lemma is complete.
We can now prove a version of the master theorem for the case in which n is an
exact power of b.
Lemma 4.4
Let a  1 and b > 1 be constants, and let f .n/ be a nonnegative function deﬁned
on exact powers of b. Deﬁne T .n/ on exact powers of b by the recurrence
T .n/ D
(
‚.1/
if n D 1 ;
aT .n=b/ C f .n/
if n D bi ;
where i is a positive integer. Then T .n/ has the following asymptotic bounds for
exact powers of b:
1. If f .n/ D O.nlogb a/ for some constant  > 0, then T .n/ D ‚.nlogb a/.
2. If f .n/ D ‚.nlogb a/, then T .n/ D ‚.nlogb a lg n/.
3. If f .n/ D .nlogb aC/ for some constant  > 0, and if af .n=b/  cf .n/ for
some constant c < 1 and all sufﬁciently large n, then T .n/ D ‚.f .n//.
Proof
We use the bounds in Lemma 4.3 to evaluate the summation (4.21) from
Lemma 4.2. For case 1, we have
T .n/
D
‚.nlogb a/ C O.nlogb a/
D
‚.nlogb a/ ;

4.6
Proof of the master theorem
103
and for case 2,
T .n/
D
‚.nlogb a/ C ‚.nlogb a lg n/
D
‚.nlogb a lg n/ :
For case 3,
T .n/
D
‚.nlogb a/ C ‚.f .n//
D
‚.f .n// ;
because f .n/ D .nlogb aC/.
4.6.2
Floors and ceilings
To complete the proof of the master theorem, we must now extend our analysis to
the situation in which ﬂoors and ceilings appear in the master recurrence, so that
the recurrence is deﬁned for all integers, not for just exact powers of b. Obtaining
a lower bound on
T .n/ D aT .dn=be/ C f .n/
(4.25)
and an upper bound on
T .n/ D aT .bn=bc/ C f .n/
(4.26)
is routine, since we can push through the bound dn=be  n=b in the ﬁrst case to
yield the desired result, and we can push through the bound bn=bc  n=b in the
second case. We use much the same technique to lower-bound the recurrence (4.26)
as to upper-bound the recurrence (4.25), and so we shall present only this latter
bound.
We modify the recursion tree of Figure 4.7 to produce the recursion tree in Fig-
ure 4.8. As we go down in the recursion tree, we obtain a sequence of recursive
invocations on the arguments
n ;
dn=be ;
ddn=be =be ;
dddn=be =be =be ;
:::
Let us denote the j th element in the sequence by nj, where
nj D
(
n
if j D 0 ;
dnj1=be
if j > 0 :
(4.27)

104
Chapter 4
Divide-and-Conquer
…
…
…
…
…
…
…
…
…
…
…
…
…
…
…
f .n/
f .n/
a
a
a
a
a
a
a
a
a
a
a
a
a
f .n1/
f .n1/
f .n1/
f .n2/
f .n2/
f .n2/
f .n2/
f .n2/
f .n2/
f .n2/
f .n2/
f .n2/
af .n1/
a2f .n2/
blogb nc
‚.nlogb a/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.1/
‚.nlogb a/
Total: ‚.nlogb a/ C
blogb nc1
X
j D0
ajf .nj/
Figure 4.8
The recursion tree generated by T .n/ D aT .dn=be/Cf .n/. The recursive argument nj
is given by equation (4.27).
Our ﬁrst goal is to determine the depth k such that nk is a constant. Using the
inequality dxe  x C 1, we obtain
n0

n ;
n1

n
b C 1 ;
n2

n
b2 C 1
b C 1 ;
n3

n
b3 C 1
b2 C 1
b C 1 ;
:::
In general, we have

4.6
Proof of the master theorem
105
nj

n
bj C
j1
X
iD0
1
bi
<
n
bj C
1
X
iD0
1
bi
D
n
bj C
b
b  1 :
Letting j D blogb nc, we obtain
nblogb nc
<
n
bblogb nc C
b
b  1
<
n
blogb n1 C
b
b  1
D
n
n=b C
b
b  1
D
b C
b
b  1
D
O.1/ ;
and thus we see that at depth blogb nc, the problem size is at most a constant.
From Figure 4.8, we see that
T .n/ D ‚.nlogb a/ C
blogb nc1
X
jD0
ajf .nj/ ;
(4.28)
which is much the same as equation (4.21), except that n is an arbitrary integer and
not restricted to be an exact power of b.
We can now evaluate the summation
g.n/ D
blogb nc1
X
jD0
ajf .nj/
(4.29)
from equation (4.28) in a manner analogous to the proof of Lemma 4.3. Beginning
with case 3, if af .dn=be/  cf .n/ for n > bCb=.b1/, where c < 1 is a constant,
then it follows that ajf .nj/  cjf .n/. Therefore, we can evaluate the sum in
equation (4.29) just as in Lemma 4.3. For case 2, we have f .n/ D ‚.nlogb a/. If we
can show that f .nj/ D O.nlogb a=aj/ D O..n=bj /logb a/, then the proof for case 2
of Lemma 4.3 will go through. Observe that j  blogb nc implies bj=n  1. The
bound f .n/ D O.nlogb a/ implies that there exists a constant c > 0 such that for all
sufﬁciently large nj,

106
Chapter 4
Divide-and-Conquer
f .nj/

c
 n
bj C
b
b  1
logb a
D
c
 n
bj

1 C bj
n 
b
b  1
logb a
D
c
nlogb a
aj
 
1 C
bj
n 
b
b  1
logb a

c
nlogb a
aj
 
1 C
b
b  1
logb a
D
O
nlogb a
aj

;
since c.1 C b=.b  1//logb a is a constant. Thus, we have proved case 2. The proof
of case 1 is almost identical. The key is to prove the bound f .nj/ D O.nlogb a/,
which is similar to the corresponding proof of case 2, though the algebra is more
intricate.
We have now proved the upper bounds in the master theorem for all integers n.
The proof of the lower bounds is similar.
Exercises
4.6-1
?
Give a simple and exact expression for nj in equation (4.27) for the case in which b
is a positive integer instead of an arbitrary real number.
4.6-2
?
Show that if f .n/ D ‚.nlogb a lgk n/, where k  0, then the master recurrence has
solution T .n/ D ‚.nlogb a lgkC1 n/. For simplicity, conﬁne your analysis to exact
powers of b.
4.6-3
?
Show that case 3 of the master theorem is overstated, in the sense that the regularity
condition af .n=b/  cf .n/ for some constant c < 1 implies that there exists a
constant  > 0 such that f .n/ D .nlogb aC/.

Problems for Chapter 4
107
Problems
4-1
Recurrence examples
Give asymptotic upper and lower bounds for T .n/ in each of the following recur-
rences. Assume that T .n/ is constant for n  2. Make your bounds as tight as
possible, and justify your answers.
a. T .n/ D 2T .n=2/ C n4.
b. T .n/ D T .7n=10/ C n.
c. T .n/ D 16T .n=4/ C n2.
d. T .n/ D 7T .n=3/ C n2.
e. T .n/ D 7T .n=2/ C n2.
f. T .n/ D 2T .n=4/ C pn.
g. T .n/ D T .n  2/ C n2.
4-2
Parameter-passing costs
Throughout this book, we assume that parameter passing during procedure calls
takes constant time, even if an N -element array is being passed. This assumption
is valid in most systems because a pointer to the array is passed, not the array itself.
This problem examines the implications of three parameter-passing strategies:
1. An array is passed by pointer. Time D ‚.1/.
2. An array is passed by copying. Time D ‚.N /, where N is the size of the array.
3. An array is passed by copying only the subrange that might be accessed by the
called procedure. Time D ‚.q  p C 1/ if the subarray AŒp : : q is passed.
a. Consider the recursive binary search algorithm for ﬁnding a number in a sorted
array (see Exercise 2.3-5). Give recurrences for the worst-case running times
of binary search when arrays are passed using each of the three methods above,
and give good upper bounds on the solutions of the recurrences. Let N be the
size of the original problem and n be the size of a subproblem.
b. Redo part (a) for the MERGE-SORT algorithm from Section 2.3.1.

108
Chapter 4
Divide-and-Conquer
4-3
More recurrence examples
Give asymptotic upper and lower bounds for T .n/ in each of the following recur-
rences. Assume that T .n/ is constant for sufﬁciently small n. Make your bounds
as tight as possible, and justify your answers.
a. T .n/ D 4T .n=3/ C n lg n.
b. T .n/ D 3T .n=3/ C n= lg n.
c. T .n/ D 4T .n=2/ C n2pn.
d. T .n/ D 3T .n=3  2/ C n=2.
e. T .n/ D 2T .n=2/ C n= lg n.
f.
T .n/ D T .n=2/ C T .n=4/ C T .n=8/ C n.
g. T .n/ D T .n  1/ C 1=n.
h. T .n/ D T .n  1/ C lg n.
i.
T .n/ D T .n  2/ C 1= lg n.
j.
T .n/ D pnT .pn/ C n.
4-4
Fibonacci numbers
This problem develops properties of the Fibonacci numbers, which are deﬁned
by recurrence (3.22). We shall use the technique of generating functions to solve
the Fibonacci recurrence. Deﬁne the generating function (or formal power se-
ries) F as
F .´/
D
1
X
iD0
Fi´i
D
0 C ´ C ´2 C 2´3 C 3´4 C 5´5 C 8´6 C 13´7 C 21´8 C    ;
where Fi is the ith Fibonacci number.
a. Show that F .´/ D ´ C ´F .´/ C ´2F .´/.

Problems for Chapter 4
109
b. Show that
F .´/
D
´
1  ´  ´2
D
´
.1  ´/.1  y´/
D
1
p
5

1
1  ´ 
1
1  y´

;
where
 D 1 C
p
5
2
D 1:61803 : : :
and
y D 1 
p
5
2
D 0:61803 : : : :
c. Show that
F .´/ D
1
X
iD0
1
p
5
.i  yi/´i :
d. Use part (c) to prove that Fi D i=
p
5 for i > 0, rounded to the nearest integer.
(Hint: Observe that
ˇˇy
ˇˇ < 1.)
4-5
Chip testing
Professor Diogenes has n supposedly identical integrated-circuit chips that in prin-
ciple are capable of testing each other. The professor’s test jig accommodates two
chips at a time. When the jig is loaded, each chip tests the other and reports whether
it is good or bad. A good chip always reports accurately whether the other chip is
good or bad, but the professor cannot trust the answer of a bad chip. Thus, the four
possible outcomes of a test are as follows:
Chip A says
Chip B says
Conclusion
B is good
A is good
both are good, or both are bad
B is good
A is bad
at least one is bad
B is bad
A is good
at least one is bad
B is bad
A is bad
at least one is bad
a. Show that if more than n=2 chips are bad, the professor cannot necessarily de-
termine which chips are good using any strategy based on this kind of pairwise
test. Assume that the bad chips can conspire to fool the professor.

110
Chapter 4
Divide-and-Conquer
b. Consider the problem of ﬁnding a single good chip from among n chips, as-
suming that more than n=2 of the chips are good. Show that bn=2c pairwise
tests are sufﬁcient to reduce the problem to one of nearly half the size.
c. Show that the good chips can be identiﬁed with ‚.n/ pairwise tests, assuming
that more than n=2 of the chips are good. Give and solve the recurrence that
describes the number of tests.
4-6
Monge arrays
An m 	 n array A of real numbers is a Monge array if for all i, j , k, and l such
that 1  i < k  m and 1  j < l  n, we have
AŒi; j  C AŒk; l  AŒi; l C AŒk; j  :
In other words, whenever we pick two rows and two columns of a Monge array and
consider the four elements at the intersections of the rows and the columns, the sum
of the upper-left and lower-right elements is less than or equal to the sum of the
lower-left and upper-right elements. For example, the following array is Monge:
10
17
13
28
23
17
22
16
29
23
24
28
22
34
24
11
13
6
17
7
45
44
32
37
23
36
33
19
21
6
75
66
51
53
34
a. Prove that an array is Monge if and only if for all i D 1; 2; :::; m  1 and
j D 1; 2; :::; n  1, we have
AŒi; j  C AŒi C 1; j C 1  AŒi; j C 1 C AŒi C 1; j  :
(Hint: For the “if” part, use induction separately on rows and columns.)
b. The following array is not Monge. Change one element in order to make it
Monge. (Hint: Use part (a).)
37
23
22
32
21
6
7
10
53
34
30
31
32
13
9
6
43
21
15
8

Notes for Chapter 4
111
c. Let f .i/ be the index of the column containing the leftmost minimum element
of row i. Prove that f .1/  f .2/      f .m/ for any m 	 n Monge array.
d. Here is a description of a divide-and-conquer algorithm that computes the left-
most minimum element in each row of an m 	 n Monge array A:
Construct a submatrix A0 of A consisting of the even-numbered rows of A.
Recursively determine the leftmost minimum for each row of A0. Then
compute the leftmost minimum in the odd-numbered rows of A.
Explain how to compute the leftmost minimum in the odd-numbered rows of A
(given that the leftmost minimum of the even-numbered rows is known) in
O.m C n/ time.
e. Write the recurrence describing the running time of the algorithm described in
part (d). Show that its solution is O.m C n log m/.
Chapter notes
Divide-and-conquer as a technique for designing algorithms dates back to at least
1962 in an article by Karatsuba and Ofman [194]. It might have been used well be-
fore then, however; according to Heideman, Johnson, and Burrus [163], C. F. Gauss
devised the ﬁrst fast Fourier transform algorithm in 1805, and Gauss’s formulation
breaks the problem into smaller subproblems whose solutions are combined.
The maximum-subarray problem in Section 4.1 is a minor variation on a problem
studied by Bentley [43, Chapter 7].
Strassen’s algorithm [325] caused much excitement when it was published
in 1969. Before then, few imagined the possibility of an algorithm asymptotically
faster than the basic SQUARE-MATRIX-MULTIPLY procedure. The asymptotic
upper bound for matrix multiplication has been improved since then. The most
asymptotically efﬁcient algorithm for multiplying n 	 n matrices to date, due to
Coppersmith and Winograd [78], has a running time of O.n2:376/. The best lower
bound known is just the obvious .n2/ bound (obvious because we must ﬁll in n2
elements of the product matrix).
From a practical point of view, Strassen’s algorithm is often not the method of
choice for matrix multiplication, for four reasons:
1. The constant factor hidden in the ‚.nlg 7/ running time of Strassen’s algo-
rithm is larger than the constant factor in the ‚.n3/-time SQUARE-MATRIX-
MULTIPLY procedure.
2. When the matrices are sparse, methods tailored for sparse matrices are faster.

112
Chapter 4
Divide-and-Conquer
3. Strassen’s algorithm is not quite as numerically stable as SQUARE-MATRIX-
MULTIPLY. In other words, because of the limited precision of computer arith-
metic on noninteger values, larger errors accumulate in Strassen’s algorithm
than in SQUARE-MATRIX-MULTIPLY.
4. The submatrices formed at the levels of recursion consume space.
The latter two reasons were mitigated around 1990. Higham [167] demonstrated
that the difference in numerical stability had been overemphasized; although
Strassen’s algorithm is too numerically unstable for some applications, it is within
acceptable limits for others. Bailey, Lee, and Simon [32] discuss techniques for
reducing the memory requirements for Strassen’s algorithm.
In practice, fast matrix-multiplication implementations for dense matrices use
Strassen’s algorithm for matrix sizes above a “crossover point,” and they switch
to a simpler method once the subproblem size reduces to below the crossover
point. The exact value of the crossover point is highly system dependent. Analyses
that count operations but ignore effects from caches and pipelining have produced
crossover points as low as n D 8 (by Higham [167]) or n D 12 (by Huss-Lederman
et al. [186]). D’Alberto and Nicolau [81] developed an adaptive scheme, which
determines the crossover point by benchmarking when their software package is
installed. They found crossover points on various systems ranging from n D 400
to n D 2150, and they could not ﬁnd a crossover point on a couple of systems.
Recurrences were studied as early as 1202 by L. Fibonacci, for whom the Fi-
bonacci numbers are named. A. De Moivre introduced the method of generating
functions (see Problem 4-4) for solving recurrences. The master method is adapted
from Bentley, Haken, and Saxe [44], which provides the extended method justiﬁed
by Exercise 4.6-2. Knuth [209] and Liu [237] show how to solve linear recurrences
using the method of generating functions. Purdom and Brown [287] and Graham,
Knuth, and Patashnik [152] contain extended discussions of recurrence solving.
Several researchers, including Akra and Bazzi [13], Roura [299], Verma [346],
and Yap [360], have given methods for solving more general divide-and-conquer
recurrences than are solved by the master method. We describe the result of Akra
and Bazzi here, as modiﬁed by Leighton [228]. The Akra-Bazzi method works for
recurrences of the form
T .x/ D
(
‚.1/
if 1  x  x0 ;
Pk
iD1 aiT .bix/ C f .x/
if x > x0 ;
(4.30)
where

x  1 is a real number,

x0 is a constant such that x0  1=bi and x0  1=.1  bi/ for i D 1; 2; : : : ; k,

ai is a positive constant for i D 1; 2; : : : ; k,

Notes for Chapter 4
113

bi is a constant in the range 0 < bi < 1 for i D 1; 2; : : : ; k,

k  1 is an integer constant, and

f .x/ is a nonnegative function that satisﬁes the polynomial-growth condi-
tion: there exist positive constants c1 and c2 such that for all x  1, for
i D 1; 2; : : : ; k, and for all u such that bix  u  x, we have c1f .x/ 
f .u/  c2f .x/. (If jf 0.x/j is upper-bounded by some polynomial in x, then
f .x/ satisﬁes the polynomial-growth condition. For example, f .x/ D x˛ lgˇ x
satisﬁes this condition for any real constants ˛ and ˇ.)
Although the master method does not apply to a recurrence such as T .n/ D
T .bn=3c/ C T .b2n=3c/ C O.n/, the Akra-Bazzi method does. To solve the re-
currence (4.30), we ﬁrst ﬁnd the unique real number p such that Pk
iD1 aibp
i D 1.
(Such a p always exists.) The solution to the recurrence is then
T .n/ D ‚

xp

1 C
Z x
1
f .u/
upC1 du

:
The Akra-Bazzi method can be somewhat difﬁcult to use, but it serves in solving
recurrences that model division of the problem into substantially unequally sized
subproblems. The master method is simpler to use, but it applies only when sub-
problem sizes are equal.
