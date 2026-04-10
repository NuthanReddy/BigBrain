# 16 Greedy Algorithms

16
Greedy Algorithms
Algorithms for optimization problems typically go through a sequence of steps,
with a set of choices at each step. For many optimization problems, using dynamic
programming to determine the best choices is overkill; simpler, more efﬁcient al-
gorithms will do. A greedy algorithm always makes the choice that looks best at
the moment. That is, it makes a locally optimal choice in the hope that this choice
will lead to a globally optimal solution. This chapter explores optimization prob-
lems for which greedy algorithms provide optimal solutions. Before reading this
chapter, you should read about dynamic programming in Chapter 15, particularly
Section 15.3.
Greedy algorithms do not always yield optimal solutions, but for many problems
they do. We shall ﬁrst examine, in Section 16.1, a simple but nontrivial problem,
the activity-selection problem, for which a greedy algorithm efﬁciently computes
an optimal solution. We shall arrive at the greedy algorithm by ﬁrst consider-
ing a dynamic-programming approach and then showing that we can always make
greedy choices to arrive at an optimal solution. Section 16.2 reviews the basic
elements of the greedy approach, giving a direct approach for proving greedy al-
gorithms correct. Section 16.3 presents an important application of greedy tech-
niques: designing data-compression (Huffman) codes. In Section 16.4, we inves-
tigate some of the theory underlying combinatorial structures called “matroids,”
for which a greedy algorithm always produces an optimal solution. Finally, Sec-
tion 16.5 applies matroids to solve a problem of scheduling unit-time tasks with
deadlines and penalties.
The greedy method is quite powerful and works well for a wide range of prob-
lems. Later chapters will present many algorithms that we can view as applica-
tions of the greedy method, including minimum-spanning-tree algorithms (Chap-
ter 23), Dijkstra’s algorithm for shortest paths from a single source (Chapter 24),
and Chv´atal’s greedy set-covering heuristic (Chapter 35). Minimum-spanning-tree
algorithms furnish a classic example of the greedy method. Although you can read

16.1
An activity-selection problem
415
this chapter and Chapter 23 independently of each other, you might ﬁnd it useful
to read them together.
16.1
An activity-selection problem
Our ﬁrst example is the problem of scheduling several competing activities that re-
quire exclusive use of a common resource, with a goal of selecting a maximum-size
set of mutually compatible activities. Suppose we have a set S D fa1; a2; : : : ; ang
of n proposed activities that wish to use a resource, such as a lecture hall, which
can serve only one activity at a time. Each activity ai has a start time si and a ﬁnish
time fi, where 0  si < fi < 1. If selected, activity ai takes place during the
half-open time interval Œsi; fi/. Activities ai and aj are compatible if the intervals
Œsi; fi/ and Œsj; fj/ do not overlap. That is, ai and aj are compatible if si  fj
or sj  fi. In the activity-selection problem, we wish to select a maximum-size
subset of mutually compatible activities. We assume that the activities are sorted
in monotonically increasing order of ﬁnish time:
f1  f2  f3      fn1  fn :
(16.1)
(We shall see later the advantage that this assumption provides.) For example,
consider the following set S of activities:
i
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
si
1
3
0
5
3
5
6
8
8
2
12
fi
4
5
6
7
9
9
10
11
12
14
16
For this example, the subset fa3; a9; a11g consists of mutually compatible activities.
It is not a maximum subset, however, since the subset fa1; a4; a8; a11g is larger. In
fact, fa1; a4; a8; a11g is a largest subset of mutually compatible activities; another
largest subset is fa2; a4; a9; a11g.
We shall solve this problem in several steps.
We start by thinking about a
dynamic-programming solution, in which we consider several choices when deter-
mining which subproblems to use in an optimal solution. We shall then observe that
we need to consider only one choice—the greedy choice—and that when we make
the greedy choice, only one subproblem remains. Based on these observations, we
shall develop a recursive greedy algorithm to solve the activity-scheduling prob-
lem. We shall complete the process of developing a greedy solution by converting
the recursive algorithm to an iterative one. Although the steps we shall go through
in this section are slightly more involved than is typical when developing a greedy
algorithm, they illustrate the relationship between greedy algorithms and dynamic
programming.

416
Chapter 16
Greedy Algorithms
The optimal substructure of the activity-selection problem
We can easily verify that the activity-selection problem exhibits optimal substruc-
ture. Let us denote by Sij the set of activities that start after activity ai ﬁnishes and
that ﬁnish before activity aj starts. Suppose that we wish to ﬁnd a maximum set of
mutually compatible activities in Sij , and suppose further that such a maximum set
is Aij, which includes some activity ak. By including ak in an optimal solution, we
are left with two subproblems: ﬁnding mutually compatible activities in the set Sik
(activities that start after activity ai ﬁnishes and that ﬁnish before activity ak starts)
and ﬁnding mutually compatible activities in the set Skj (activities that start after
activity ak ﬁnishes and that ﬁnish before activity aj starts). Let Aik D Aij \ Sik
and Akj D Aij \ Skj , so that Aik contains the activities in Aij that ﬁnish before ak
starts and Akj contains the activities in Aij that start after ak ﬁnishes. Thus, we
have Aij D Aik [ fakg [ Akj, and so the maximum-size set Aij of mutually com-
patible activities in Sij consists of jAijj D jAikj C jAkjj C 1 activities.
The usual cut-and-paste argument shows that the optimal solution Aij must also
include optimal solutions to the two subproblems for Sik and Skj . If we could
ﬁnd a set A0
kj of mutually compatible activities in Skj where jA0
kjj > jAkjj, then
we could use A0
kj, rather than Akj, in a solution to the subproblem for Sij. We
would have constructed a set of jAikj C jA0
kjj C 1 > jAikj C jAkjj C 1 D jAijj
mutually compatible activities, which contradicts the assumption that Aij is an
optimal solution. A symmetric argument applies to the activities in Sik.
This way of characterizing optimal substructure suggests that we might solve
the activity-selection problem by dynamic programming. If we denote the size of
an optimal solution for the set Sij by cŒi; j , then we would have the recurrence
cŒi; j  D cŒi; k C cŒk; j  C 1 :
Of course, if we did not know that an optimal solution for the set Sij includes
activity ak, we would have to examine all activities in Sij to ﬁnd which one to
choose, so that
cŒi; j  D
( 0
if Sij D ; ;
max
ak2Sij fcŒi; k C cŒk; j  C 1g
if Sij ¤ ; :
(16.2)
We could then develop a recursive algorithm and memoize it, or we could work
bottom-up and ﬁll in table entries as we go along. But we would be overlooking
another important characteristic of the activity-selection problem that we can use
to great advantage.

16.1
An activity-selection problem
417
Making the greedy choice
What if we could choose an activity to add to our optimal solution without having
to ﬁrst solve all the subproblems? That could save us from having to consider all
the choices inherent in recurrence (16.2). In fact, for the activity-selection problem,
we need consider only one choice: the greedy choice.
What do we mean by the greedy choice for the activity-selection problem? Intu-
ition suggests that we should choose an activity that leaves the resource available
for as many other activities as possible. Now, of the activities we end up choos-
ing, one of them must be the ﬁrst one to ﬁnish. Our intuition tells us, therefore,
to choose the activity in S with the earliest ﬁnish time, since that would leave the
resource available for as many of the activities that follow it as possible. (If more
than one activity in S has the earliest ﬁnish time, then we can choose any such
activity.) In other words, since the activities are sorted in monotonically increasing
order by ﬁnish time, the greedy choice is activity a1. Choosing the ﬁrst activity
to ﬁnish is not the only way to think of making a greedy choice for this problem;
Exercise 16.1-3 asks you to explore other possibilities.
If we make the greedy choice, we have only one remaining subproblem to solve:
ﬁnding activities that start after a1 ﬁnishes. Why don’t we have to consider ac-
tivities that ﬁnish before a1 starts? We have that s1 < f1, and f1 is the earliest
ﬁnish time of any activity, and therefore no activity can have a ﬁnish time less than
or equal to s1. Thus, all activities that are compatible with activity a1 must start
after a1 ﬁnishes.
Furthermore, we have already established that the activity-selection problem ex-
hibits optimal substructure. Let Sk D fai 2 S W si  fkg be the set of activities that
start after activity ak ﬁnishes. If we make the greedy choice of activity a1, then S1
remains as the only subproblem to solve.1 Optimal substructure tells us that if a1
is in the optimal solution, then an optimal solution to the original problem consists
of activity a1 and all the activities in an optimal solution to the subproblem S1.
One big question remains: is our intuition correct? Is the greedy choice—in
which we choose the ﬁrst activity to ﬁnish—always part of some optimal solution?
The following theorem shows that it is.
1We sometimes refer to the sets Sk as subproblems rather than as just sets of activities. It will always
be clear from the context whether we are referring to Sk as a set of activities or as a subproblem
whose input is that set.

418
Chapter 16
Greedy Algorithms
Theorem 16.1
Consider any nonempty subproblem Sk, and let am be an activity in Sk with the
earliest ﬁnish time. Then am is included in some maximum-size subset of mutually
compatible activities of Sk.
Proof
Let Ak be a maximum-size subset of mutually compatible activities in Sk,
and let aj be the activity in Ak with the earliest ﬁnish time. If aj D am, we are
done, since we have shown that am is in some maximum-size subset of mutually
compatible activities of Sk. If aj ¤ am, let the set A0
k D Ak  fajg [ famg be Ak
but substituting am for aj. The activities in A0
k are disjoint, which follows because
the activities in Ak are disjoint, aj is the ﬁrst activity in Ak to ﬁnish, and fm  fj.
Since jA0
kj D jAkj, we conclude that A0
k is a maximum-size subset of mutually
compatible activities of Sk, and it includes am.
Thus, we see that although we might be able to solve the activity-selection prob-
lem with dynamic programming, we don’t need to. (Besides, we have not yet
examined whether the activity-selection problem even has overlapping subprob-
lems.) Instead, we can repeatedly choose the activity that ﬁnishes ﬁrst, keep only
the activities compatible with this activity, and repeat until no activities remain.
Moreover, because we always choose the activity with the earliest ﬁnish time, the
ﬁnish times of the activities we choose must strictly increase. We can consider
each activity just once overall, in monotonically increasing order of ﬁnish times.
An algorithm to solve the activity-selection problem does not need to work
bottom-up, like a table-based dynamic-programming algorithm. Instead, it can
work top-down, choosing an activity to put into the optimal solution and then solv-
ing the subproblem of choosing activities from those that are compatible with those
already chosen. Greedy algorithms typically have this top-down design: make a
choice and then solve a subproblem, rather than the bottom-up technique of solving
subproblems before making a choice.
A recursive greedy algorithm
Now that we have seen how to bypass the dynamic-programming approach and in-
stead use a top-down, greedy algorithm, we can write a straightforward, recursive
procedure to solve the activity-selection problem. The procedure RECURSIVE-
ACTIVITY-SELECTOR takes the start and ﬁnish times of the activities, represented
as arrays s and f ,2 the index k that deﬁnes the subproblem Sk it is to solve, and
2Because the pseudocode takes s and f as arrays, it indexes into them with square brackets rather
than subscripts.

16.1
An activity-selection problem
419
the size n of the original problem. It returns a maximum-size set of mutually com-
patible activities in Sk. We assume that the n input activities are already ordered
by monotonically increasing ﬁnish time, according to equation (16.1). If not, we
can sort them into this order in O.n lg n/ time, breaking ties arbitrarily. In order
to start, we add the ﬁctitious activity a0 with f0 D 0, so that subproblem S0 is
the entire set of activities S. The initial call, which solves the entire problem, is
RECURSIVE-ACTIVITY-SELECTOR.s; f; 0; n/.
RECURSIVE-ACTIVITY-SELECTOR.s; f; k; n/
1
m D k C 1
2
while m  n and sŒm < f Œk
// ﬁnd the ﬁrst activity in Sk to ﬁnish
3
m D m C 1
4
if m  n
5
return famg [ RECURSIVE-ACTIVITY-SELECTOR.s; f; m; n/
6
else return ;
Figure 16.1 shows the operation of the algorithm.
In a given recursive call
RECURSIVE-ACTIVITY-SELECTOR.s; f; k; n/, the while loop of lines 2–3 looks
for the ﬁrst activity in Sk to ﬁnish. The loop examines akC1; akC2; : : : ; an, un-
til it ﬁnds the ﬁrst activity am that is compatible with ak; such an activity has
sm  fk. If the loop terminates because it ﬁnds such an activity, line 5 returns
the union of famg and the maximum-size subset of Sm returned by the recursive
call RECURSIVE-ACTIVITY-SELECTOR.s; f; m; n/. Alternatively, the loop may
terminate because m > n, in which case we have examined all activities in Sk
without ﬁnding one that is compatible with ak. In this case, Sk D ;, and so the
procedure returns ; in line 6.
Assuming that the activities have already been sorted by ﬁnish times, the running
time of the call RECURSIVE-ACTIVITY-SELECTOR.s; f; 0; n/ is ‚.n/, which we
can see as follows. Over all recursive calls, each activity is examined exactly once
in the while loop test of line 2. In particular, activity ai is examined in the last call
made in which k < i.
An iterative greedy algorithm
We easily can convert our recursive procedure to an iterative one. The procedure
RECURSIVE-ACTIVITY-SELECTOR is almost “tail recursive” (see Problem 7-4):
it ends with a recursive call to itself followed by a union operation. It is usually a
straightforward task to transform a tail-recursive procedure to an iterative form; in
fact, some compilers for certain programming languages perform this task automat-
ically. As written, RECURSIVE-ACTIVITY-SELECTOR works for subproblems Sk,
i.e., subproblems that consist of the last activities to ﬁnish.

420
Chapter 16
Greedy Algorithms
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
time
2
3
5
3
0
6
4
5
7
5
3
9
6
5
9
7
6
10
8
8
11
9
8
12
10
2
14
11
12
16
1
1
4
k
sk
fk
a1
a2
a1
a3
a1
a4
a1
a4
a5
a1
a4
a6
a1
a4
a7
a1
a4
a8
a1
a4
a8
a9
a1
a4
a8
a10
a1
a4
a8
a11
a1
a4
a8
a11
0
–
0
a1
a0
a0
RECURSIVE-ACTIVITY-SELECTOR(s, f, 0, 11)
RECURSIVE-ACTIVITY-SELECTOR(s, f, 1, 11)
RECURSIVE-ACTIVITY-SELECTOR(s, f, 4, 11)
RECURSIVE-ACTIVITY-SELECTOR(s, f, 8, 11)
m = 1
m = 4
m = 8
m = 11
RECURSIVE-ACTIVITY-SELECTOR(s, f, 11, 11)
15
16
Figure 16.1
The operation of RECURSIVE-ACTIVITY-SELECTOR on the 11 activities given ear-
lier. Activities considered in each recursive call appear between horizontal lines. The ﬁctitious
activity a0 ﬁnishes at time 0, and the initial call RECURSIVE-ACTIVITY-SELECTOR.s; f; 0; 11/, se-
lects activity a1. In each recursive call, the activities that have already been selected are shaded,
and the activity shown in white is being considered. If the starting time of an activity occurs before
the ﬁnish time of the most recently added activity (the arrow between them points left), it is re-
jected. Otherwise (the arrow points directly up or to the right), it is selected. The last recursive call,
RECURSIVE-ACTIVITY-SELECTOR.s; f; 11; 11/, returns ;. The resulting set of selected activities is
fa1; a4; a8; a11g.

16.1
An activity-selection problem
421
The procedure GREEDY-ACTIVITY-SELECTOR is an iterative version of the pro-
cedure RECURSIVE-ACTIVITY-SELECTOR. It also assumes that the input activi-
ties are ordered by monotonically increasing ﬁnish time. It collects selected activ-
ities into a set A and returns this set when it is done.
GREEDY-ACTIVITY-SELECTOR.s; f /
1
n D s:length
2
A D fa1g
3
k D 1
4
for m D 2 to n
5
if sŒm  f Œk
6
A D A [ famg
7
k D m
8
return A
The procedure works as follows. The variable k indexes the most recent addition
to A, corresponding to the activity ak in the recursive version. Since we consider
the activities in order of monotonically increasing ﬁnish time, fk is always the
maximum ﬁnish time of any activity in A. That is,
fk D max ffi W ai 2 Ag :
(16.3)
Lines 2–3 select activity a1, initialize A to contain just this activity, and initialize k
to index this activity. The for loop of lines 4–7 ﬁnds the earliest activity in Sk to
ﬁnish. The loop considers each activity am in turn and adds am to A if it is compat-
ible with all previously selected activities; such an activity is the earliest in Sk to
ﬁnish. To see whether activity am is compatible with every activity currently in A,
it sufﬁces by equation (16.3) to check (in line 5) that its start time sm is not earlier
than the ﬁnish time fk of the activity most recently added to A. If activity am is
compatible, then lines 6–7 add activity am to A and set k to m. The set A returned
by the call GREEDY-ACTIVITY-SELECTOR.s; f / is precisely the set returned by
the call RECURSIVE-ACTIVITY-SELECTOR.s; f; 0; n/.
Like the recursive version, GREEDY-ACTIVITY-SELECTOR schedules a set of n
activities in ‚.n/ time, assuming that the activities were already sorted initially by
their ﬁnish times.
Exercises
16.1-1
Give a dynamic-programming algorithm for the activity-selection problem, based
on recurrence (16.2). Have your algorithm compute the sizes cŒi; j  as deﬁned
above and also produce the maximum-size subset of mutually compatible activities.

422
Chapter 16
Greedy Algorithms
Assume that the inputs have been sorted as in equation (16.1). Compare the running
time of your solution to the running time of GREEDY-ACTIVITY-SELECTOR.
16.1-2
Suppose that instead of always selecting the ﬁrst activity to ﬁnish, we instead select
the last activity to start that is compatible with all previously selected activities. De-
scribe how this approach is a greedy algorithm, and prove that it yields an optimal
solution.
16.1-3
Not just any greedy approach to the activity-selection problem produces a max-
imum-size set of mutually compatible activities. Give an example to show that
the approach of selecting the activity of least duration from among those that are
compatible with previously selected activities does not work. Do the same for
the approaches of always selecting the compatible activity that overlaps the fewest
other remaining activities and always selecting the compatible remaining activity
with the earliest start time.
16.1-4
Suppose that we have a set of activities to schedule among a large number of lecture
halls, where any activity can take place in any lecture hall. We wish to schedule
all the activities using as few lecture halls as possible. Give an efﬁcient greedy
algorithm to determine which activity should use which lecture hall.
(This problem is also known as the interval-graph coloring problem. We can
create an interval graph whose vertices are the given activities and whose edges
connect incompatible activities. The smallest number of colors required to color
every vertex so that no two adjacent vertices have the same color corresponds to
ﬁnding the fewest lecture halls needed to schedule all of the given activities.)
16.1-5
Consider a modiﬁcation to the activity-selection problem in which each activity ai
has, in addition to a start and ﬁnish time, a value i. The objective is no longer
to maximize the number of activities scheduled, but instead to maximize the total
value of the activities scheduled. That is, we wish to choose a set A of compatible
activities such that P
ak2A k is maximized. Give a polynomial-time algorithm for
this problem.

16.2
Elements of the greedy strategy
423
16.2
Elements of the greedy strategy
A greedy algorithm obtains an optimal solution to a problem by making a sequence
of choices. At each decision point, the algorithm makes choice that seems best at
the moment. This heuristic strategy does not always produce an optimal solution,
but as we saw in the activity-selection problem, sometimes it does. This section
discusses some of the general properties of greedy methods.
The process that we followed in Section 16.1 to develop a greedy algorithm was
a bit more involved than is typical. We went through the following steps:
1. Determine the optimal substructure of the problem.
2. Develop a recursive solution. (For the activity-selection problem, we formu-
lated recurrence (16.2), but we bypassed developing a recursive algorithm based
on this recurrence.)
3. Show that if we make the greedy choice, then only one subproblem remains.
4. Prove that it is always safe to make the greedy choice. (Steps 3 and 4 can occur
in either order.)
5. Develop a recursive algorithm that implements the greedy strategy.
6. Convert the recursive algorithm to an iterative algorithm.
In going through these steps, we saw in great detail the dynamic-programming un-
derpinnings of a greedy algorithm. For example, in the activity-selection problem,
we ﬁrst deﬁned the subproblems Sij, where both i and j varied. We then found
that if we always made the greedy choice, we could restrict the subproblems to be
of the form Sk.
Alternatively, we could have fashioned our optimal substructure with a greedy
choice in mind, so that the choice leaves just one subproblem to solve. In the
activity-selection problem, we could have started by dropping the second subscript
and deﬁning subproblems of the form Sk. Then, we could have proven that a greedy
choice (the ﬁrst activity am to ﬁnish in Sk), combined with an optimal solution to
the remaining set Sm of compatible activities, yields an optimal solution to Sk.
More generally, we design greedy algorithms according to the following sequence
of steps:
1. Cast the optimization problem as one in which we make a choice and are left
with one subproblem to solve.
2. Prove that there is always an optimal solution to the original problem that makes
the greedy choice, so that the greedy choice is always safe.

424
Chapter 16
Greedy Algorithms
3. Demonstrate optimal substructure by showing that, having made the greedy
choice, what remains is a subproblem with the property that if we combine an
optimal solution to the subproblem with the greedy choice we have made, we
arrive at an optimal solution to the original problem.
We shall use this more direct process in later sections of this chapter. Neverthe-
less, beneath every greedy algorithm, there is almost always a more cumbersome
dynamic-programming solution.
How can we tell whether a greedy algorithm will solve a particular optimization
problem? No way works all the time, but the greedy-choice property and optimal
substructure are the two key ingredients. If we can demonstrate that the problem
has these properties, then we are well on the way to developing a greedy algorithm
for it.
Greedy-choice property
The ﬁrst key ingredient is the greedy-choice property: we can assemble a globally
optimal solution by making locally optimal (greedy) choices. In other words, when
we are considering which choice to make, we make the choice that looks best in
the current problem, without considering results from subproblems.
Here is where greedy algorithms differ from dynamic programming. In dynamic
programming, we make a choice at each step, but the choice usually depends on the
solutions to subproblems. Consequently, we typically solve dynamic-programming
problems in a bottom-up manner, progressing from smaller subproblems to larger
subproblems. (Alternatively, we can solve them top down, but memoizing. Of
course, even though the code works top down, we still must solve the subprob-
lems before making a choice.) In a greedy algorithm, we make whatever choice
seems best at the moment and then solve the subproblem that remains. The choice
made by a greedy algorithm may depend on choices so far, but it cannot depend on
any future choices or on the solutions to subproblems. Thus, unlike dynamic pro-
gramming, which solves the subproblems before making the ﬁrst choice, a greedy
algorithm makes its ﬁrst choice before solving any subproblems.
A dynamic-
programming algorithm proceeds bottom up, whereas a greedy strategy usually
progresses in a top-down fashion, making one greedy choice after another, reduc-
ing each given problem instance to a smaller one.
Of course, we must prove that a greedy choice at each step yields a globally
optimal solution. Typically, as in the case of Theorem 16.1, the proof examines
a globally optimal solution to some subproblem. It then shows how to modify
the solution to substitute the greedy choice for some other choice, resulting in one
similar, but smaller, subproblem.
We can usually make the greedy choice more efﬁciently than when we have to
consider a wider set of choices. For example, in the activity-selection problem, as-

16.2
Elements of the greedy strategy
425
suming that we had already sorted the activities in monotonically increasing order
of ﬁnish times, we needed to examine each activity just once. By preprocessing the
input or by using an appropriate data structure (often a priority queue), we often
can make greedy choices quickly, thus yielding an efﬁcient algorithm.
Optimal substructure
A problem exhibits optimal substructure if an optimal solution to the problem
contains within it optimal solutions to subproblems. This property is a key in-
gredient of assessing the applicability of dynamic programming as well as greedy
algorithms. As an example of optimal substructure, recall how we demonstrated in
Section 16.1 that if an optimal solution to subproblem Sij includes an activity ak,
then it must also contain optimal solutions to the subproblems Sik and Skj . Given
this optimal substructure, we argued that if we knew which activity to use as ak, we
could construct an optimal solution to Sij by selecting ak along with all activities
in optimal solutions to the subproblems Sik and Skj . Based on this observation of
optimal substructure, we were able to devise the recurrence (16.2) that described
the value of an optimal solution.
We usually use a more direct approach regarding optimal substructure when
applying it to greedy algorithms. As mentioned above, we have the luxury of
assuming that we arrived at a subproblem by having made the greedy choice in
the original problem. All we really need to do is argue that an optimal solution to
the subproblem, combined with the greedy choice already made, yields an optimal
solution to the original problem. This scheme implicitly uses induction on the
subproblems to prove that making the greedy choice at every step produces an
optimal solution.
Greedy versus dynamic programming
Because both the greedy and dynamic-programming strategies exploit optimal sub-
structure, you might be tempted to generate a dynamic-programming solution to a
problem when a greedy solution sufﬁces or, conversely, you might mistakenly think
that a greedy solution works when in fact a dynamic-programming solution is re-
quired. To illustrate the subtleties between the two techniques, let us investigate
two variants of a classical optimization problem.
The 0-1 knapsack problem is the following. A thief robbing a store ﬁnds n
items. The ith item is worth i dollars and weighs wi pounds, where i and wi are
integers. The thief wants to take as valuable a load as possible, but he can carry at
most W pounds in his knapsack, for some integer W . Which items should he take?
(We call this the 0-1 knapsack problem because for each item, the thief must either

426
Chapter 16
Greedy Algorithms
take it or leave it behind; he cannot take a fractional amount of an item or take an
item more than once.)
In the fractional knapsack problem, the setup is the same, but the thief can take
fractions of items, rather than having to make a binary (0-1) choice for each item.
You can think of an item in the 0-1 knapsack problem as being like a gold ingot
and an item in the fractional knapsack problem as more like gold dust.
Both knapsack problems exhibit the optimal-substructure property. For the 0-1
problem, consider the most valuable load that weighs at most W pounds. If we
remove item j from this load, the remaining load must be the most valuable load
weighing at most W  wj that the thief can take from the n  1 original items
excluding j . For the comparable fractional problem, consider that if we remove
a weight w of one item j from the optimal load, the remaining load must be the
most valuable load weighing at most W  w that the thief can take from the n  1
original items plus wj  w pounds of item j .
Although the problems are similar, we can solve the fractional knapsack problem
by a greedy strategy, but we cannot solve the 0-1 problem by such a strategy. To
solve the fractional problem, we ﬁrst compute the value per pound i=wi for each
item. Obeying a greedy strategy, the thief begins by taking as much as possible of
the item with the greatest value per pound. If the supply of that item is exhausted
and he can still carry more, he takes as much as possible of the item with the next
greatest value per pound, and so forth, until he reaches his weight limit W . Thus,
by sorting the items by value per pound, the greedy algorithm runs in O.n lg n/
time. We leave the proof that the fractional knapsack problem has the greedy-
choice property as Exercise 16.2-1.
To see that this greedy strategy does not work for the 0-1 knapsack problem,
consider the problem instance illustrated in Figure 16.2(a). This example has 3
items and a knapsack that can hold 50 pounds. Item 1 weighs 10 pounds and
is worth 60 dollars. Item 2 weighs 20 pounds and is worth 100 dollars. Item 3
weighs 30 pounds and is worth 120 dollars. Thus, the value per pound of item 1 is
6 dollars per pound, which is greater than the value per pound of either item 2 (5
dollars per pound) or item 3 (4 dollars per pound). The greedy strategy, therefore,
would take item 1 ﬁrst. As you can see from the case analysis in Figure 16.2(b),
however, the optimal solution takes items 2 and 3, leaving item 1 behind. The two
possible solutions that take item 1 are both suboptimal.
For the comparable fractional problem, however, the greedy strategy, which
takes item 1 ﬁrst, does yield an optimal solution, as shown in Figure 16.2(c). Tak-
ing item 1 doesn’t work in the 0-1 problem because the thief is unable to ﬁll his
knapsack to capacity, and the empty space lowers the effective value per pound of
his load. In the 0-1 problem, when we consider whether to include an item in the
knapsack, we must compare the solution to the subproblem that includes the item
with the solution to the subproblem that excludes the item before we can make the

16.2
Elements of the greedy strategy
427
10
$60
item 1
20
$100
item 2
30
$120
item 3
50
knapsack
(a)
+
$120
$100
= $220
+
$60
$100
= $160
+
$60
$120
= $180
(b)
+
$60
$100
= $240
$80
+
(c)
20
30
10
20
10
30
10
20
20
30
Figure 16.2
An example showing that the greedy strategy does not work for the 0-1 knapsack
problem. (a) The thief must select a subset of the three items shown whose weight must not exceed
50 pounds. (b) The optimal subset includes items 2 and 3. Any solution with item 1 is suboptimal,
even though item 1 has the greatest value per pound. (c) For the fractional knapsack problem, taking
the items in order of greatest value per pound yields an optimal solution.
choice. The problem formulated in this way gives rise to many overlapping sub-
problems—a hallmark of dynamic programming, and indeed, as Exercise 16.2-2
asks you to show, we can use dynamic programming to solve the 0-1 problem.
Exercises
16.2-1
Prove that the fractional knapsack problem has the greedy-choice property.
16.2-2
Give a dynamic-programming solution to the 0-1 knapsack problem that runs in
O.n W / time, where n is the number of items and W is the maximum weight of
items that the thief can put in his knapsack.
16.2-3
Suppose that in a 0-1 knapsack problem, the order of the items when sorted by
increasing weight is the same as their order when sorted by decreasing value. Give
an efﬁcient algorithm to ﬁnd an optimal solution to this variant of the knapsack
problem, and argue that your algorithm is correct.
16.2-4
Professor Gekko has always dreamed of inline skating across North Dakota. He
plans to cross the state on highway U.S. 2, which runs from Grand Forks, on the
eastern border with Minnesota, to Williston, near the western border with Montana.

428
Chapter 16
Greedy Algorithms
The professor can carry two liters of water, and he can skate m miles before running
out of water. (Because North Dakota is relatively ﬂat, the professor does not have
to worry about drinking water at a greater rate on uphill sections than on ﬂat or
downhill sections.) The professor will start in Grand Forks with two full liters of
water. His ofﬁcial North Dakota state map shows all the places along U.S. 2 at
which he can reﬁll his water and the distances between these locations.
The professor’s goal is to minimize the number of water stops along his route
across the state. Give an efﬁcient method by which he can determine which water
stops he should make. Prove that your strategy yields an optimal solution, and give
its running time.
16.2-5
Describe an efﬁcient algorithm that, given a set fx1; x2; : : : ; xng of points on the
real line, determines the smallest set of unit-length closed intervals that contains
all of the given points. Argue that your algorithm is correct.
16.2-6
?
Show how to solve the fractional knapsack problem in O.n/ time.
16.2-7
Suppose you are given two sets A and B, each containing n positive integers. You
can choose to reorder each set however you like. After reordering, let ai be the ith
element of set A, and let bi be the ith element of set B. You then receive a payoff
of Qn
iD1 ai
bi. Give an algorithm that will maximize your payoff. Prove that your
algorithm maximizes the payoff, and state its running time.
16.3
Huffman codes
Huffman codes compress data very effectively: savings of 20% to 90% are typical,
depending on the characteristics of the data being compressed. We consider the
data to be a sequence of characters. Huffman’s greedy algorithm uses a table giving
how often each character occurs (i.e., its frequency) to build up an optimal way of
representing each character as a binary string.
Suppose we have a 100,000-character data ﬁle that we wish to store compactly.
We observe that the characters in the ﬁle occur with the frequencies given by Fig-
ure 16.3. That is, only 6 different characters appear, and the character a occurs
45,000 times.
We have many options for how to represent such a ﬁle of information. Here,
we consider the problem of designing a binary character code (or code for short)

16.3
Huffman codes
429
a
b
c
d
e
f
Frequency (in thousands)
45
13
12
16
9
5
Fixed-length codeword
000
001
010
011
100
101
Variable-length codeword
0
101
100
111
1101
1100
Figure 16.3
A character-coding problem. A data ﬁle of 100,000 characters contains only the char-
acters a–f, with the frequencies indicated. If we assign each character a 3-bit codeword, we can
encode the ﬁle in 300,000 bits. Using the variable-length code shown, we can encode the ﬁle in only
224,000 bits.
in which each character is represented by a unique binary string, which we call a
codeword. If we use a ﬁxed-length code, we need 3 bits to represent 6 characters:
a = 000, b = 001, . . . , f = 101. This method requires 300,000 bits to code the
entire ﬁle. Can we do better?
A variable-length code can do considerably better than a ﬁxed-length code, by
giving frequent characters short codewords and infrequent characters long code-
words. Figure 16.3 shows such a code; here the 1-bit string 0 represents a, and the
4-bit string 1100 represents f. This code requires
.45  1 C 13  3 C 12  3 C 16  3 C 9  4 C 5  4/  1,000 D 224,000 bits
to represent the ﬁle, a savings of approximately 25%. In fact, this is an optimal
character code for this ﬁle, as we shall see.
Preﬁx codes
We consider here only codes in which no codeword is also a preﬁx of some other
codeword. Such codes are called preﬁx codes.3 Although we won’t prove it here, a
preﬁx code can always achieve the optimal data compression among any character
code, and so we suffer no loss of generality by restricting our attention to preﬁx
codes.
Encoding is always simple for any binary character code; we just concatenate the
codewords representing each character of the ﬁle. For example, with the variable-
length preﬁx code of Figure 16.3, we code the 3-character ﬁle abc as 0101100 D
0101100, where “” denotes concatenation.
Preﬁx codes are desirable because they simplify decoding. Since no codeword
is a preﬁx of any other, the codeword that begins an encoded ﬁle is unambiguous.
We can simply identify the initial codeword, translate it back to the original char-
3Perhaps “preﬁx-free codes” would be a better name, but the term “preﬁx codes” is standard in the
literature.

430
Chapter 16
Greedy Algorithms
a:45
b:13
c:12
d:16
e:9
f:5
58
28
14
86
14
100
0
1
0
1
0
1
0
1
0
0
1
e:9
f:5
14
0
1
c:12
b:13
25
0
1
d:16
30
0
1
55
0
1
a:45
100
0
1
(a)
(b)
Figure 16.4
Trees corresponding to the coding schemes in Figure 16.3. Each leaf is labeled with
a character and its frequency of occurrence. Each internal node is labeled with the sum of the fre-
quencies of the leaves in its subtree. (a) The tree corresponding to the ﬁxed-length code a = 000, . . . ,
f = 101. (b) The tree corresponding to the optimal preﬁx code a = 0, b = 101, . . . , f = 1100.
acter, and repeat the decoding process on the remainder of the encoded ﬁle. In our
example, the string 001011101 parses uniquely as 0  0  101  1101, which decodes
to aabe.
The decoding process needs a convenient representation for the preﬁx code so
that we can easily pick off the initial codeword. A binary tree whose leaves are
the given characters provides one such representation.
We interpret the binary
codeword for a character as the simple path from the root to that character, where 0
means “go to the left child” and 1 means “go to the right child.” Figure 16.4 shows
the trees for the two codes of our example. Note that these are not binary search
trees, since the leaves need not appear in sorted order and internal nodes do not
contain character keys.
An optimal code for a ﬁle is always represented by a full binary tree, in which
every nonleaf node has two children (see Exercise 16.3-2). The ﬁxed-length code
in our example is not optimal since its tree, shown in Figure 16.4(a), is not a full bi-
nary tree: it contains codewords beginning 10. . . , but none beginning 11. . . . Since
we can now restrict our attention to full binary trees, we can say that if C is the
alphabet from which the characters are drawn and all character frequencies are pos-
itive, then the tree for an optimal preﬁx code has exactly jCj leaves, one for each
letter of the alphabet, and exactly jCj  1 internal nodes (see Exercise B.5-3).
Given a tree T corresponding to a preﬁx code, we can easily compute the number
of bits required to encode a ﬁle. For each character c in the alphabet C, let the
attribute c:freq denote the frequency of c in the ﬁle and let dT .c/ denote the depth

16.3
Huffman codes
431
of c’s leaf in the tree. Note that dT .c/ is also the length of the codeword for
character c. The number of bits required to encode a ﬁle is thus
B.T / D
X
c2C
c:freq  dT .c/ ;
(16.4)
which we deﬁne as the cost of the tree T .
Constructing a Huffman code
Huffman invented a greedy algorithm that constructs an optimal preﬁx code called
a Huffman code. In line with our observations in Section 16.2, its proof of cor-
rectness relies on the greedy-choice property and optimal substructure. Rather
than demonstrating that these properties hold and then developing pseudocode, we
present the pseudocode ﬁrst. Doing so will help clarify how the algorithm makes
greedy choices.
In the pseudocode that follows, we assume that C is a set of n characters and
that each character c 2 C is an object with an attribute c:freq giving its frequency.
The algorithm builds the tree T corresponding to the optimal code in a bottom-up
manner. It begins with a set of jCj leaves and performs a sequence of jCj  1
“merging” operations to create the ﬁnal tree. The algorithm uses a min-priority
queue Q, keyed on the freq attribute, to identify the two least-frequent objects to
merge together. When we merge two objects, the result is a new object whose
frequency is the sum of the frequencies of the two objects that were merged.
HUFFMAN.C/
1
n D jCj
2
Q D C
3
for i D 1 to n  1
4
allocate a new node ´
5
´:left D x D EXTRACT-MIN.Q/
6
´:right D y D EXTRACT-MIN.Q/
7
´:freq D x:freq C y:freq
8
INSERT.Q; ´/
9
return EXTRACT-MIN.Q/
// return the root of the tree
For our example, Huffman’s algorithm proceeds as shown in Figure 16.5. Since
the alphabet contains 6 letters, the initial queue size is n D 6, and 5 merge steps
build the tree. The ﬁnal tree represents the optimal preﬁx code. The codeword for
a letter is the sequence of edge labels on the simple path from the root to the letter.
Line 2 initializes the min-priority queue Q with the characters in C. The for
loop in lines 3–8 repeatedly extracts the two nodes x and y of lowest frequency

432
Chapter 16
Greedy Algorithms
e:9
f:5
14
0
1
c:12
b:13
25
0
1
d:16
30
0
1
55
0
1
a:45
100
0
1
e:9
f:5
14
0
1
c:12
b:13
25
0
1
d:16
30
0
1
55
0
1
a:45
e:9
f:5
14
0
1
c:12
b:13
25
0
1
d:16
30
0
1
a:45
e:9
f:5
14
0
1
c:12
b:13
25
0
1
d:16
a:45
e:9
f:5
14
0
1
c:12
b:13
d:16
a:45
e:9
f:5
c:12
b:13
d:16
a:45
(a)
(c)
(e)
(b)
(d)
(f)
Figure 16.5
The steps of Huffman’s algorithm for the frequencies given in Figure 16.3. Each part
shows the contents of the queue sorted into increasing order by frequency. At each step, the two
trees with lowest frequencies are merged. Leaves are shown as rectangles containing a character
and its frequency. Internal nodes are shown as circles containing the sum of the frequencies of their
children. An edge connecting an internal node with its children is labeled 0 if it is an edge to a left
child and 1 if it is an edge to a right child. The codeword for a letter is the sequence of labels on the
edges connecting the root to the leaf for that letter. (a) The initial set of n D 6 nodes, one for each
letter. (b)–(e) Intermediate stages. (f) The ﬁnal tree.
from the queue, replacing them in the queue with a new node ´ representing their
merger. The frequency of ´ is computed as the sum of the frequencies of x and y
in line 7. The node ´ has x as its left child and y as its right child. (This order is
arbitrary; switching the left and right child of any node yields a different code of
the same cost.) After n  1 mergers, line 9 returns the one node left in the queue,
which is the root of the code tree.
Although the algorithm would produce the same result if we were to excise the
variables x and y—assigning directly to ´:left and ´:right in lines 5 and 6, and
changing line 7 to ´:freq D ´:left:freq C ´:right:freq—we shall use the node

16.3
Huffman codes
433
names x and y in the proof of correctness. Therefore, we ﬁnd it convenient to
leave them in.
To analyze the running time of Huffman’s algorithm, we assume that Q is im-
plemented as a binary min-heap (see Chapter 6). For a set C of n characters, we
can initialize Q in line 2 in O.n/ time using the BUILD-MIN-HEAP procedure dis-
cussed in Section 6.3. The for loop in lines 3–8 executes exactly n  1 times, and
since each heap operation requires time O.lg n/, the loop contributes O.n lg n/ to
the running time. Thus, the total running time of HUFFMAN on a set of n charac-
ters is O.n lg n/. We can reduce the running time to O.n lg lg n/ by replacing the
binary min-heap with a van Emde Boas tree (see Chapter 20).
Correctness of Huffman’s algorithm
To prove that the greedy algorithm HUFFMAN is correct, we show that the prob-
lem of determining an optimal preﬁx code exhibits the greedy-choice and optimal-
substructure properties. The next lemma shows that the greedy-choice property
holds.
Lemma 16.2
Let C be an alphabet in which each character c 2 C has frequency c:freq. Let
x and y be two characters in C having the lowest frequencies. Then there exists
an optimal preﬁx code for C in which the codewords for x and y have the same
length and differ only in the last bit.
Proof
The idea of the proof is to take the tree T representing an arbitrary optimal
preﬁx code and modify it to make a tree representing another optimal preﬁx code
such that the characters x and y appear as sibling leaves of maximum depth in the
new tree. If we can construct such a tree, then the codewords for x and y will have
the same length and differ only in the last bit.
Let a and b be two characters that are sibling leaves of maximum depth in T .
Without loss of generality, we assume that a:freq  b:freq and x:freq  y:freq.
Since x:freq and y:freq are the two lowest leaf frequencies, in order, and a:freq
and b:freq are two arbitrary frequencies, in order, we have x:freq  a:freq and
y:freq  b:freq.
In the remainder of the proof, it is possible that we could have x:freq D a:freq
or y:freq D b:freq. However, if we had x:freq D b:freq, then we would also have
a:freq D b:freq D x:freq D y:freq (see Exercise 16.3-1), and the lemma would
be trivially true. Thus, we will assume that x:freq ¤ b:freq, which means that
x ¤ b.
As Figure 16.6 shows, we exchange the positions in T of a and x to produce a
tree T 0, and then we exchange the positions in T 0 of b and y to produce a tree T 00

434
Chapter 16
Greedy Algorithms
x
y
a
b
x
y
a
b
x
y
a
b
T′′
T
T′
Figure 16.6
An illustration of the key step in the proof of Lemma 16.2. In the optimal tree T ,
leaves a and b are two siblings of maximum depth. Leaves x and y are the two characters with the
lowest frequencies; they appear in arbitrary positions in T . Assuming that x ¤ b, swapping leaves a
and x produces tree T 0, and then swapping leaves b and y produces tree T 00. Since each swap does
not increase the cost, the resulting tree T 00 is also an optimal tree.
in which x and y are sibling leaves of maximum depth. (Note that if x D b but
y ¤ a, then tree T 00 does not have x and y as sibling leaves of maximum depth.
Because we assume that x ¤ b, this situation cannot occur.) By equation (16.4),
the difference in cost between T and T 0 is
B.T /  B.T 0/
D
X
c2C
c:freq  dT .c/ 
X
c2C
c:freq  dT 0.c/
D
x:freq  dT .x/ C a:freq  dT .a/  x:freq  dT 0.x/  a:freq  dT 0.a/
D
x:freq  dT .x/ C a:freq  dT .a/  x:freq  dT .a/  a:freq  dT .x/
D
.a:freq  x:freq/.dT .a/  dT .x//

0 ;
because both a:freq  x:freq and dT .a/  dT .x/ are nonnegative. More speciﬁ-
cally, a:freq  x:freq is nonnegative because x is a minimum-frequency leaf, and
dT .a/dT .x/ is nonnegative because a is a leaf of maximum depth in T . Similarly,
exchanging y and b does not increase the cost, and so B.T 0/  B.T 00/ is nonnega-
tive. Therefore, B.T 00/  B.T /, and since T is optimal, we have B.T /  B.T 00/,
which implies B.T 00/ D B.T /. Thus, T 00 is an optimal tree in which x and y
appear as sibling leaves of maximum depth, from which the lemma follows.
Lemma 16.2 implies that the process of building up an optimal tree by mergers
can, without loss of generality, begin with the greedy choice of merging together
those two characters of lowest frequency. Why is this a greedy choice? We can
view the cost of a single merger as being the sum of the frequencies of the two items
being merged. Exercise 16.3-4 shows that the total cost of the tree constructed
equals the sum of the costs of its mergers. Of all possible mergers at each step,
HUFFMAN chooses the one that incurs the least cost.

16.3
Huffman codes
435
The next lemma shows that the problem of constructing optimal preﬁx codes has
the optimal-substructure property.
Lemma 16.3
Let C be a given alphabet with frequency c:freq deﬁned for each character c 2 C.
Let x and y be two characters in C with minimum frequency. Let C 0 be the
alphabet C with the characters x and y removed and a new character ´ added,
so that C 0
D C  fx; yg [ f´g.
Deﬁne f for C 0 as for C, except that
´:freq D x:freq C y:freq. Let T 0 be any tree representing an optimal preﬁx code
for the alphabet C 0. Then the tree T , obtained from T 0 by replacing the leaf node
for ´ with an internal node having x and y as children, represents an optimal preﬁx
code for the alphabet C.
Proof
We ﬁrst show how to express the cost B.T / of tree T in terms of the
cost B.T 0/ of tree T 0, by considering the component costs in equation (16.4).
For each character c 2 C  fx; yg, we have that dT .c/ D dT 0.c/, and hence
c:freq  dT .c/ D c:freq  dT 0.c/. Since dT .x/ D dT .y/ D dT 0.´/ C 1, we have
x:freq  dT .x/ C y:freq  dT .y/
D
.x:freq C y:freq/.dT 0.´/ C 1/
D
´:freq  dT 0.´/ C .x:freq C y:freq/ ;
from which we conclude that
B.T / D B.T 0/ C x:freq C y:freq
or, equivalently,
B.T 0/ D B.T /  x:freq  y:freq :
We now prove the lemma by contradiction. Suppose that T does not repre-
sent an optimal preﬁx code for C. Then there exists an optimal tree T 00 such that
B.T 00/ < B.T /. Without loss of generality (by Lemma 16.2), T 00 has x and y as
siblings. Let T 000 be the tree T 00 with the common parent of x and y replaced by a
leaf ´ with frequency ´:freq D x:freq C y:freq. Then
B.T 000/
D
B.T 00/  x:freq  y:freq
<
B.T /  x:freq  y:freq
D
B.T 0/ ;
yielding a contradiction to the assumption that T 0 represents an optimal preﬁx code
for C 0. Thus, T must represent an optimal preﬁx code for the alphabet C.
Theorem 16.4
Procedure HUFFMAN produces an optimal preﬁx code.
Proof
Immediate from Lemmas 16.2 and 16.3.

436
Chapter 16
Greedy Algorithms
Exercises
16.3-1
Explain why, in the proof of Lemma 16.2, if x:freq D b:freq, then we must have
a:freq D b:freq D x:freq D y:freq.
16.3-2
Prove that a binary tree that is not full cannot correspond to an optimal preﬁx code.
16.3-3
What is an optimal Huffman code for the following set of frequencies, based on
the ﬁrst 8 Fibonacci numbers?
a:1 b:1 c:2 d:3 e:5 f:8 g:13 h:21
Can you generalize your answer to ﬁnd the optimal code when the frequencies are
the ﬁrst n Fibonacci numbers?
16.3-4
Prove that we can also express the total cost of a tree for a code as the sum, over
all internal nodes, of the combined frequencies of the two children of the node.
16.3-5
Prove that if we order the characters in an alphabet so that their frequencies
are monotonically decreasing, then there exists an optimal code whose codeword
lengths are monotonically increasing.
16.3-6
Suppose we have an optimal preﬁx code on a set C D f0; 1; : : : ; n  1g of charac-
ters and we wish to transmit this code using as few bits as possible. Show how to
represent any optimal preﬁx code on C using only 2n  1 C n dlg ne bits. (Hint:
Use 2n  1 bits to specify the structure of the tree, as discovered by a walk of the
tree.)
16.3-7
Generalize Huffman’s algorithm to ternary codewords (i.e., codewords using the
symbols 0, 1, and 2), and prove that it yields optimal ternary codes.
16.3-8
Suppose that a data ﬁle contains a sequence of 8-bit characters such that all 256
characters are about equally common: the maximum character frequency is less
than twice the minimum character frequency. Prove that Huffman coding in this
case is no more efﬁcient than using an ordinary 8-bit ﬁxed-length code.

16.4
Matroids and greedy methods
437
16.3-9
Show that no compression scheme can expect to compress a ﬁle of randomly cho-
sen 8-bit characters by even a single bit. (Hint: Compare the number of possible
ﬁles with the number of possible encoded ﬁles.)
?
16.4
Matroids and greedy methods
In this section, we sketch a beautiful theory about greedy algorithms. This theory
describes many situations in which the greedy method yields optimal solutions. It
involves combinatorial structures known as “matroids.” Although this theory does
not cover all cases for which a greedy method applies (for example, it does not
cover the activity-selection problem of Section 16.1 or the Huffman-coding prob-
lem of Section 16.3), it does cover many cases of practical interest. Furthermore,
this theory has been extended to cover many applications; see the notes at the end
of this chapter for references.
Matroids
A matroid is an ordered pair M D .S; / satisfying the following conditions.
1. S is a ﬁnite set.
2.  is a nonempty family of subsets of S, called the independent subsets of S,
such that if B 2  and A  B, then A 2 . We say that  is hereditary if it
satisﬁes this property. Note that the empty set ; is necessarily a member of .
3. If A 2 , B 2 , and jAj < jBj, then there exists some element x 2 B  A
such that A [ fxg 2 . We say that M satisﬁes the exchange property.
The word “matroid” is due to Hassler Whitney. He was studying matric ma-
troids, in which the elements of S are the rows of a given matrix and a set of rows is
independent if they are linearly independent in the usual sense. As Exercise 16.4-2
asks you to show, this structure deﬁnes a matroid.
As another example of matroids, consider the graphic matroid MG D .SG; G/
deﬁned in terms of a given undirected graph G D .V; E/ as follows:

The set SG is deﬁned to be E, the set of edges of G.

If A is a subset of E, then A 2 G if and only if A is acyclic. That is, a set of
edges A is independent if and only if the subgraph GA D .V; A/ forms a forest.
The graphic matroid MG is closely related to the minimum-spanning-tree problem,
which Chapter 23 covers in detail.

438
Chapter 16
Greedy Algorithms
Theorem 16.5
If G D .V; E/ is an undirected graph, then MG D .SG; G/ is a matroid.
Proof
Clearly, SG D E is a ﬁnite set. Furthermore, G is hereditary, since a
subset of a forest is a forest. Putting it another way, removing edges from an
acyclic set of edges cannot create cycles.
Thus, it remains to show that MG satisﬁes the exchange property. Suppose that
GA D .V; A/ and GB D .V; B/ are forests of G and that jBj > jAj. That is, A
and B are acyclic sets of edges, and B contains more edges than A does.
We claim that a forest F D .VF ; EF / contains exactly jVF j  jEF j trees. To
see why, suppose that F consists of t trees, where the ith tree contains i vertices
and ei edges. Then, we have
jEF j
D
tX
iD1
ei
D
tX
iD1
.i  1/
(by Theorem B.2)
D
tX
iD1
i  t
D
jVF j  t ;
which implies that t D jVF j  jEF j. Thus, forest GA contains jV j  jAj trees, and
forest GB contains jV j  jBj trees.
Since forest GB has fewer trees than forest GA does, forest GB must contain
some tree T whose vertices are in two different trees in forest GA. Moreover,
since T is connected, it must contain an edge .u; / such that vertices u and 
are in different trees in forest GA. Since the edge .u; / connects vertices in two
different trees in forest GA, we can add the edge .u; / to forest GA without creating
a cycle. Therefore, MG satisﬁes the exchange property, completing the proof that
MG is a matroid.
Given a matroid M D .S; /, we call an element x … A an extension of A 2 
if we can add x to A while preserving independence; that is, x is an extension
of A if A [ fxg 2 . As an example, consider a graphic matroid MG. If A is an
independent set of edges, then edge e is an extension of A if and only if e is not
in A and the addition of e to A does not create a cycle.
If A is an independent subset in a matroid M, we say that A is maximal if it has
no extensions. That is, A is maximal if it is not contained in any larger independent
subset of M. The following property is often useful.

16.4
Matroids and greedy methods
439
Theorem 16.6
All maximal independent subsets in a matroid have the same size.
Proof
Suppose to the contrary that A is a maximal independent subset of M
and there exists another larger maximal independent subset B of M. Then, the
exchange property implies that for some x 2 B  A, we can extend A to a larger
independent set A [ fxg, contradicting the assumption that A is maximal.
As an illustration of this theorem, consider a graphic matroid MG for a con-
nected, undirected graph G. Every maximal independent subset of MG must be a
free tree with exactly jV j  1 edges that connects all the vertices of G. Such a tree
is called a spanning tree of G.
We say that a matroid M D .S; / is weighted if it is associated with a weight
function w that assigns a strictly positive weight w.x/ to each element x 2 S. The
weight function w extends to subsets of S by summation:
w.A/ D
X
x2A
w.x/
for any A  S. For example, if we let w.e/ denote the weight of an edge e in a
graphic matroid MG, then w.A/ is the total weight of the edges in edge set A.
Greedy algorithms on a weighted matroid
Many problems for which a greedy approach provides optimal solutions can be for-
mulated in terms of ﬁnding a maximum-weight independent subset in a weighted
matroid. That is, we are given a weighted matroid M D .S; /, and we wish to
ﬁnd an independent set A 2  such that w.A/ is maximized. We call such a sub-
set that is independent and has maximum possible weight an optimal subset of the
matroid. Because the weight w.x/ of any element x 2 S is positive, an optimal
subset is always a maximal independent subset—it always helps to make A as large
as possible.
For example, in the minimum-spanning-tree problem, we are given a connected
undirected graph G D .V; E/ and a length function w such that w.e/ is the (posi-
tive) length of edge e. (We use the term “length” here to refer to the original edge
weights for the graph, reserving the term “weight” to refer to the weights in the
associated matroid.) We wish to ﬁnd a subset of the edges that connects all of
the vertices together and has minimum total length. To view this as a problem of
ﬁnding an optimal subset of a matroid, consider the weighted matroid MG with
weight function w0, where w0.e/ D w0  w.e/ and w0 is larger than the maximum
length of any edge. In this weighted matroid, all weights are positive and an opti-
mal subset is a spanning tree of minimum total length in the original graph. More
speciﬁcally, each maximal independent subset A corresponds to a spanning tree

440
Chapter 16
Greedy Algorithms
with jV j  1 edges, and since
w0.A/
D
X
e2A
w0.e/
D
X
e2A
.w0  w.e//
D
.jV j  1/w0 
X
e2A
w.e/
D
.jV j  1/w0  w.A/
for any maximal independent subset A, an independent subset that maximizes the
quantity w0.A/ must minimize w.A/. Thus, any algorithm that can ﬁnd an optimal
subset A in an arbitrary matroid can solve the minimum-spanning-tree problem.
Chapter 23 gives algorithms for the minimum-spanning-tree problem, but here
we give a greedy algorithm that works for any weighted matroid. The algorithm
takes as input a weighted matroid M D .S; / with an associated positive weight
function w, and it returns an optimal subset A. In our pseudocode, we denote the
components of M by M:S and M: and the weight function by w. The algorithm
is greedy because it considers in turn each element x 2 S, in order of monotoni-
cally decreasing weight, and immediately adds it to the set A being accumulated if
A [ fxg is independent.
GREEDY.M; w/
1
A D ;
2
sort M:S into monotonically decreasing order by weight w
3
for each x 2 M:S, taken in monotonically decreasing order by weight w.x/
4
if A [ fxg 2 M:
5
A D A [ fxg
6
return A
Line 4 checks whether adding each element x to A would maintain A as an inde-
pendent set. If A would remain independent, then line 5 adds x to A. Otherwise, x
is discarded. Since the empty set is independent, and since each iteration of the for
loop maintains A’s independence, the subset A is always independent, by induc-
tion. Therefore, GREEDY always returns an independent subset A. We shall see in
a moment that A is a subset of maximum possible weight, so that A is an optimal
subset.
The running time of GREEDY is easy to analyze. Let n denote jSj. The sorting
phase of GREEDY takes time O.n lg n/. Line 4 executes exactly n times, once for
each element of S. Each execution of line 4 requires a check on whether or not
the set A [ fxg is independent. If each such check takes time O.f .n//, the entire
algorithm runs in time O.n lg n C nf .n//.

16.4
Matroids and greedy methods
441
We now prove that GREEDY returns an optimal subset.
Lemma 16.7 (Matroids exhibit the greedy-choice property)
Suppose that M D .S; / is a weighted matroid with weight function w and that S
is sorted into monotonically decreasing order by weight. Let x be the ﬁrst element
of S such that fxg is independent, if any such x exists. If x exists, then there exists
an optimal subset A of S that contains x.
Proof
If no such x exists, then the only independent subset is the empty set and
the lemma is vacuously true. Otherwise, let B be any nonempty optimal subset.
Assume that x … B; otherwise, letting A D B gives an optimal subset of S that
contains x.
No element of B has weight greater than w.x/. To see why, observe that y 2 B
implies that fyg is independent, since B 2  and  is hereditary. Our choice of x
therefore ensures that w.x/  w.y/ for any y 2 B.
Construct the set A as follows. Begin with A D fxg. By the choice of x, set A is
independent. Using the exchange property, repeatedly ﬁnd a new element of B that
we can add to A until jAj D jBj, while preserving the independence of A. At that
point, A and B are the same except that A has x and B has some other element y.
That is, A D B  fyg [ fxg for some y 2 B, and so
w.A/
D
w.B/  w.y/ C w.x/

w.B/ :
Because set B is optimal, set A, which contains x, must also be optimal.
We next show that if an element is not an option initially, then it cannot be an
option later.
Lemma 16.8
Let M D .S; / be any matroid. If x is an element of S that is an extension of
some independent subset A of S, then x is also an extension of ;.
Proof
Since x is an extension of A, we have that A[fxg is independent. Since 
is hereditary, fxg must be independent. Thus, x is an extension of ;.
Corollary 16.9
Let M D .S; / be any matroid. If x is an element of S such that x is not an
extension of ;, then x is not an extension of any independent subset A of S.
Proof
This corollary is simply the contrapositive of Lemma 16.8.

442
Chapter 16
Greedy Algorithms
Corollary 16.9 says that any element that cannot be used immediately can never
be used. Therefore, GREEDY cannot make an error by passing over any initial
elements in S that are not an extension of ;, since they can never be used.
Lemma 16.10 (Matroids exhibit the optimal-substructure property)
Let x be the ﬁrst element of S chosen by GREEDY for the weighted matroid
M D .S; /. The remaining problem of ﬁnding a maximum-weight indepen-
dent subset containing x reduces to ﬁnding a maximum-weight independent subset
of the weighted matroid M 0 D .S 0;  0/, where
S 0
D
fy 2 S W fx; yg 2 g ;
 0
D
fB  S  fxg W B [ fxg 2 g ;
and the weight function for M 0 is the weight function for M, restricted to S 0. (We
call M 0 the contraction of M by the element x.)
Proof
If A is any maximum-weight independent subset of M containing x, then
A0 D A  fxg is an independent subset of M 0. Conversely, any independent sub-
set A0 of M 0 yields an independent subset A D A0 [ fxg of M. Since we have in
both cases that w.A/ D w.A0/Cw.x/, a maximum-weight solution in M contain-
ing x yields a maximum-weight solution in M 0, and vice versa.
Theorem 16.11 (Correctness of the greedy algorithm on matroids)
If M D .S; / is a weighted matroid with weight function w, then GREEDY.M; w/
returns an optimal subset.
Proof
By Corollary 16.9, any elements that GREEDY passes over initially be-
cause they are not extensions of ; can be forgotten about, since they can never
be useful. Once GREEDY selects the ﬁrst element x, Lemma 16.7 implies that
the algorithm does not err by adding x to A, since there exists an optimal subset
containing x. Finally, Lemma 16.10 implies that the remaining problem is one of
ﬁnding an optimal subset in the matroid M 0 that is the contraction of M by x.
After the procedure GREEDY sets A to fxg, we can interpret all of its remaining
steps as acting in the matroid M 0 D .S 0;  0/, because B is independent in M 0 if
and only if B [ fxg is independent in M, for all sets B 2  0. Thus, the subsequent
operation of GREEDY will ﬁnd a maximum-weight independent subset for M 0, and
the overall operation of GREEDY will ﬁnd a maximum-weight independent subset
for M.

16.5
A task-scheduling problem as a matroid
443
Exercises
16.4-1
Show that .S; k/ is a matroid, where S is any ﬁnite set and k is the set of all
subsets of S of size at most k, where k  jSj.
16.4-2
?
Given an m 	 n matrix T over some ﬁeld (such as the reals), show that .S; / is a
matroid, where S is the set of columns of T and A 2  if and only if the columns
in A are linearly independent.
16.4-3
?
Show that if .S; / is a matroid, then .S;  0/ is a matroid, where
 0 D fA0 W S  A0 contains some maximal A 2 g :
That is, the maximal independent sets of .S;  0/ are just the complements of the
maximal independent sets of .S; /.
16.4-4
?
Let S be a ﬁnite set and let S1; S2; : : : ; Sk be a partition of S into nonempty disjoint
subsets. Deﬁne the structure .S; / by the condition that  D fA W jA \ Sij  1
for i D 1; 2; : : : ; kg. Show that .S; / is a matroid. That is, the set of all sets A
that contain at most one member of each subset in the partition determines the
independent sets of a matroid.
16.4-5
Show how to transform the weight function of a weighted matroid problem, where
the desired optimal solution is a minimum-weight maximal independent subset, to
make it a standard weighted-matroid problem. Argue carefully that your transfor-
mation is correct.
?
16.5
A task-scheduling problem as a matroid
An interesting problem that we can solve using matroids is the problem of op-
timally scheduling unit-time tasks on a single processor, where each task has a
deadline, along with a penalty paid if the task misses its deadline. The problem
looks complicated, but we can solve it in a surprisingly simple manner by casting
it as a matroid and using a greedy algorithm.
A unit-time task is a job, such as a program to be run on a computer, that requires
exactly one unit of time to complete. Given a ﬁnite set S of unit-time tasks, a

444
Chapter 16
Greedy Algorithms
schedule for S is a permutation of S specifying the order in which to perform
these tasks. The ﬁrst task in the schedule begins at time 0 and ﬁnishes at time 1,
the second task begins at time 1 and ﬁnishes at time 2, and so on.
The problem of scheduling unit-time tasks with deadlines and penalties for a
single processor has the following inputs:

a set S D fa1; a2; : : : ; ang of n unit-time tasks;

a set of n integer deadlines d1; d2; : : : ; dn, such that each di satisﬁes 1  di  n
and task ai is supposed to ﬁnish by time di; and

a set of n nonnegative weights or penalties w1; w2; : : : ; wn, such that we incur
a penalty of wi if task ai is not ﬁnished by time di, and we incur no penalty if
a task ﬁnishes by its deadline.
We wish to ﬁnd a schedule for S that minimizes the total penalty incurred for
missed deadlines.
Consider a given schedule. We say that a task is late in this schedule if it ﬁnishes
after its deadline. Otherwise, the task is early in the schedule. We can always trans-
form an arbitrary schedule into early-ﬁrst form, in which the early tasks precede
the late tasks. To see why, note that if some early task ai follows some late task aj,
then we can switch the positions of ai and aj, and ai will still be early and aj will
still be late.
Furthermore, we claim that we can always transform an arbitrary schedule into
canonical form, in which the early tasks precede the late tasks and we schedule
the early tasks in order of monotonically increasing deadlines. To do so, we put
the schedule into early-ﬁrst form. Then, as long as there exist two early tasks ai
and aj ﬁnishing at respective times k and k C 1 in the schedule such that dj < di,
we swap the positions of ai and aj. Since aj is early before the swap, k C 1  dj.
Therefore, k C 1 < di, and so ai is still early after the swap. Because task aj is
moved earlier in the schedule, it remains early after the swap.
The search for an optimal schedule thus reduces to ﬁnding a set A of tasks that
we assign to be early in the optimal schedule. Having determined A, we can create
the actual schedule by listing the elements of A in order of monotonically increas-
ing deadlines, then listing the late tasks (i.e., S  A) in any order, producing a
canonical ordering of the optimal schedule.
We say that a set A of tasks is independent if there exists a schedule for these
tasks such that no tasks are late. Clearly, the set of early tasks for a schedule forms
an independent set of tasks. Let  denote the set of all independent sets of tasks.
Consider the problem of determining whether a given set A of tasks is indepen-
dent. For t D 0; 1; 2; : : : ; n, let Nt.A/ denote the number of tasks in A whose
deadline is t or earlier. Note that N0.A/ D 0 for any set A.

16.5
A task-scheduling problem as a matroid
445
Lemma 16.12
For any set of tasks A, the following statements are equivalent.
1. The set A is independent.
2. For t D 0; 1; 2; : : : ; n, we have Nt.A/  t.
3. If the tasks in A are scheduled in order of monotonically increasing deadlines,
then no task is late.
Proof
To show that (1) implies (2), we prove the contrapositive: if Nt.A/ > t for
some t, then there is no way to make a schedule with no late tasks for set A, because
more than t tasks must ﬁnish before time t. Therefore, (1) implies (2). If (2) holds,
then (3) must follow: there is no way to “get stuck” when scheduling the tasks in
order of monotonically increasing deadlines, since (2) implies that the ith largest
deadline is at least i. Finally, (3) trivially implies (1).
Using property 2 of Lemma 16.12, we can easily compute whether or not a given
set of tasks is independent (see Exercise 16.5-2).
The problem of minimizing the sum of the penalties of the late tasks is the same
as the problem of maximizing the sum of the penalties of the early tasks. The
following theorem thus ensures that we can use the greedy algorithm to ﬁnd an
independent set A of tasks with the maximum total penalty.
Theorem 16.13
If S is a set of unit-time tasks with deadlines, and  is the set of all independent
sets of tasks, then the corresponding system .S; / is a matroid.
Proof
Every subset of an independent set of tasks is certainly independent. To
prove the exchange property, suppose that B and A are independent sets of tasks
and that jBj > jAj. Let k be the largest t such that Nt.B/  Nt.A/. (Such a value
of t exists, since N0.A/ D N0.B/ D 0.) Since Nn.B/ D jBj and Nn.A/ D jAj,
but jBj > jAj, we must have that k < n and that Nj.B/ > Nj.A/ for all j in
the range k C 1  j  n. Therefore, B contains more tasks with deadline k C 1
than A does. Let ai be a task in B  A with deadline k C 1. Let A0 D A [ faig.
We now show that A0 must be independent by using property 2 of Lemma 16.12.
For 0  t  k, we have Nt.A0/ D Nt.A/  t, since A is independent. For
k < t  n, we have Nt.A0/  Nt.B/  t, since B is independent. Therefore, A0
is independent, completing our proof that .S; / is a matroid.
By Theorem 16.11, we can use a greedy algorithm to ﬁnd a maximum-weight
independent set of tasks A. We can then create an optimal schedule having the
tasks in A as its early tasks. This method is an efﬁcient algorithm for scheduling

446
Chapter 16
Greedy Algorithms
Task
ai
1
2
3
4
5
6
7
di
4
2
4
3
1
4
6
wi
70
60
50
40
30
20
10
Figure 16.7
An instance of the problem of scheduling unit-time tasks with deadlines and penalties
for a single processor.
unit-time tasks with deadlines and penalties for a single processor. The running
time is O.n2/ using GREEDY, since each of the O.n/ independence checks made
by that algorithm takes time O.n/ (see Exercise 16.5-2). Problem 16-4 gives a
faster implementation.
Figure 16.7 demonstrates an example of the problem of scheduling unit-time
tasks with deadlines and penalties for a single processor. In this example, the
greedy algorithm selects, in order, tasks a1, a2, a3, and a4, then rejects a5 (because
N4.fa1; a2; a3; a4; a5g/ D 5) and a6 (because N4.fa1; a2; a3; a4; a6g/ D 5), and
ﬁnally accepts a7. The ﬁnal optimal schedule is
ha2; a4; a1; a3; a7; a5; a6i ;
which has a total penalty incurred of w5 C w6 D 50.
Exercises
16.5-1
Solve the instance of the scheduling problem given in Figure 16.7, but with each
penalty wi replaced by 80  wi.
16.5-2
Show how to use property 2 of Lemma 16.12 to determine in time O.jAj/ whether
or not a given set A of tasks is independent.
Problems
16-1
Coin changing
Consider the problem of making change for n cents using the fewest number of
coins. Assume that each coin’s value is an integer.
a. Describe a greedy algorithm to make change consisting of quarters, dimes,
nickels, and pennies. Prove that your algorithm yields an optimal solution.

Problems for Chapter 16
447
b. Suppose that the available coins are in the denominations that are powers of c,
i.e., the denominations are c0; c1; : : : ; ck for some integers c > 1 and k  1.
Show that the greedy algorithm always yields an optimal solution.
c. Give a set of coin denominations for which the greedy algorithm does not yield
an optimal solution. Your set should include a penny so that there is a solution
for every value of n.
d. Give an O.nk/-time algorithm that makes change for any set of k different coin
denominations, assuming that one of the coins is a penny.
16-2
Scheduling to minimize average completion time
Suppose you are given a set S D fa1; a2; : : : ; ang of tasks, where task ai re-
quires pi units of processing time to complete, once it has started. You have one
computer on which to run these tasks, and the computer can run only one task at a
time. Let ci be the completion time of task ai, that is, the time at which task ai com-
pletes processing. Your goal is to minimize the average completion time, that is,
to minimize .1=n/ Pn
iD1 ci. For example, suppose there are two tasks, a1 and a2,
with p1 D 3 and p2 D 5, and consider the schedule in which a2 runs ﬁrst, followed
by a1. Then c2 D 5, c1 D 8, and the average completion time is .5 C 8/=2 D 6:5.
If task a1 runs ﬁrst, however, then c1 D 3, c2 D 8, and the average completion
time is .3 C 8/=2 D 5:5.
a. Give an algorithm that schedules the tasks so as to minimize the average com-
pletion time. Each task must run non-preemptively, that is, once task ai starts, it
must run continuously for pi units of time. Prove that your algorithm minimizes
the average completion time, and state the running time of your algorithm.
b. Suppose now that the tasks are not all available at once. That is, each task
cannot start until its release time ri. Suppose also that we allow preemption, so
that a task can be suspended and restarted at a later time. For example, a task ai
with processing time pi D 6 and release time ri D 1 might start running at
time 1 and be preempted at time 4. It might then resume at time 10 but be
preempted at time 11, and it might ﬁnally resume at time 13 and complete at
time 15. Task ai has run for a total of 6 time units, but its running time has been
divided into three pieces. In this scenario, ai’s completion time is 15. Give
an algorithm that schedules the tasks so as to minimize the average completion
time in this new scenario. Prove that your algorithm minimizes the average
completion time, and state the running time of your algorithm.

448
Chapter 16
Greedy Algorithms
16-3
Acyclic subgraphs
a. The incidence matrix for an undirected graph G D .V; E/ is a jV j 	 jEj ma-
trix M such that Me D 1 if edge e is incident on vertex , and Me D 0 other-
wise. Argue that a set of columns of M is linearly independent over the ﬁeld
of integers modulo 2 if and only if the corresponding set of edges is acyclic.
Then, use the result of Exercise 16.4-2 to provide an alternate proof that .E; /
of part (a) is a matroid.
b. Suppose that we associate a nonnegative weight w.e/ with each edge in an
undirected graph G D .V; E/. Give an efﬁcient algorithm to ﬁnd an acyclic
subset of E of maximum total weight.
c. Let G.V; E/ be an arbitrary directed graph, and let .E; / be deﬁned so that
A 2  if and only if A does not contain any directed cycles. Give an example
of a directed graph G such that the associated system .E; / is not a matroid.
Specify which deﬁning condition for a matroid fails to hold.
d. The incidence matrix for a directed graph G D .V; E/ with no self-loops is a
jV j 	 jEj matrix M such that Me D 1 if edge e leaves vertex , Me D 1 if
edge e enters vertex , and Me D 0 otherwise. Argue that if a set of columns
of M is linearly independent, then the corresponding set of edges does not
contain a directed cycle.
e. Exercise 16.4-2 tells us that the set of linearly independent sets of columns of
any matrix M forms a matroid. Explain carefully why the results of parts (d)
and (e) are not contradictory. How can there fail to be a perfect correspon-
dence between the notion of a set of edges being acyclic and the notion of the
associated set of columns of the incidence matrix being linearly independent?
16-4
Scheduling variations
Consider the following algorithm for the problem from Section 16.5 of scheduling
unit-time tasks with deadlines and penalties. Let all n time slots be initially empty,
where time slot i is the unit-length slot of time that ﬁnishes at time i. We consider
the tasks in order of monotonically decreasing penalty. When considering task aj,
if there exists a time slot at or before aj’s deadline dj that is still empty, assign aj
to the latest such slot, ﬁlling it. If there is no such slot, assign task aj to the latest
of the as yet unﬁlled slots.
a. Argue that this algorithm always gives an optimal answer.
b. Use the fast disjoint-set forest presented in Section 21.3 to implement the algo-
rithm efﬁciently. Assume that the set of input tasks has already been sorted into

Problems for Chapter 16
449
monotonically decreasing order by penalty. Analyze the running time of your
implementation.
16-5
Off-line caching
Modern computers use a cache to store a small amount of data in a fast memory.
Even though a program may access large amounts of data, by storing a small subset
of the main memory in the cache—a small but faster memory—overall access time
can greatly decrease. When a computer program executes, it makes a sequence
hr1; r2; : : : ; rni of n memory requests, where each request is for a particular data
element. For example, a program that accesses 4 distinct elements fa; b; c; dg
might make the sequence of requests hd; b; d; b; d; a; c; d; b; a; c; bi. Let k be the
size of the cache. When the cache contains k elements and the program requests the
.k C 1/st element, the system must decide, for this and each subsequent request,
which k elements to keep in the cache. More precisely, for each request ri, the
cache-management algorithm checks whether element ri is already in the cache. If
it is, then we have a cache hit; otherwise, we have a cache miss. Upon a cache
miss, the system retrieves ri from the main memory, and the cache-management
algorithm must decide whether to keep ri in the cache. If it decides to keep ri and
the cache already holds k elements, then it must evict one element to make room
for ri. The cache-management algorithm evicts data with the goal of minimizing
the number of cache misses over the entire sequence of requests.
Typically, caching is an on-line problem. That is, we have to make decisions
about which data to keep in the cache without knowing the future requests. Here,
however, we consider the off-line version of this problem, in which we are given
in advance the entire sequence of n requests and the cache size k, and we wish to
minimize the total number of cache misses.
We can solve this off-line problem by a greedy strategy called furthest-in-future,
which chooses to evict the item in the cache whose next access in the request
sequence comes furthest in the future.
a. Write pseudocode for a cache manager that uses the furthest-in-future strategy.
The input should be a sequence hr1; r2; : : : ; rni of requests and a cache size k,
and the output should be a sequence of decisions about which data element (if
any) to evict upon each request. What is the running time of your algorithm?
b. Show that the off-line caching problem exhibits optimal substructure.
c. Prove that furthest-in-future produces the minimum possible number of cache
misses.

450
Chapter 16
Greedy Algorithms
Chapter notes
Much more material on greedy algorithms and matroids can be found in Lawler
[224] and Papadimitriou and Steiglitz [271].
The greedy algorithm ﬁrst appeared in the combinatorial optimization literature
in a 1971 article by Edmonds [101], though the theory of matroids dates back to
a 1935 article by Whitney [355].
Our proof of the correctness of the greedy algorithm for the activity-selection
problem is based on that of Gavril [131]. The task-scheduling problem is studied
in Lawler [224]; Horowitz, Sahni, and Rajasekaran [181]; and Brassard and Bratley
[54].
Huffman codes were invented in 1952 [185]; Lelewer and Hirschberg [231] sur-
veys data-compression techniques known as of 1987.
An extension of matroid theory to greedoid theory was pioneered by Korte and
Lov´asz [216, 217, 218, 219], who greatly generalize the theory presented here.
