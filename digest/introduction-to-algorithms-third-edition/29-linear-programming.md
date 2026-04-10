# 29 Linear Programming

29
Linear Programming
Many problems take the form of maximizing or minimizing an objective, given
limited resources and competing constraints. If we can specify the objective as
a linear function of certain variables, and if we can specify the constraints on
resources as equalities or inequalities on those variables, then we have a linear-
programming problem. Linear programs arise in a variety of practical applica-
tions. We begin by studying an application in electoral politics.
A political problem
Suppose that you are a politician trying to win an election. Your district has three
different types of areas—urban, suburban, and rural. These areas have, respec-
tively, 100,000, 200,000, and 50,000 registered voters. Although not all the reg-
istered voters actually go to the polls, you decide that to govern effectively, you
would like at least half the registered voters in each of the three regions to vote for
you. You are honorable and would never consider supporting policies in which you
do not believe. You realize, however, that certain issues may be more effective in
winning votes in certain places. Your primary issues are building more roads, gun
control, farm subsidies, and a gasoline tax dedicated to improved public transit.
According to your campaign staff’s research, you can estimate how many votes
you win or lose from each population segment by spending $1,000 on advertising
on each issue. This information appears in the table of Figure 29.1. In this table,
each entry indicates the number of thousands of either urban, suburban, or rural
voters who would be won over by spending $1,000 on advertising in support of a
particular issue. Negative entries denote votes that would be lost. Your task is to
ﬁgure out the minimum amount of money that you need to spend in order to win
50,000 urban votes, 100,000 suburban votes, and 25,000 rural votes.
You could, by trial and error, devise a strategy that wins the required number
of votes, but the strategy you come up with might not be the least expensive one.
For example, you could devote $20,000 of advertising to building roads, $0 to gun
control, $4,000 to farm subsidies, and $9,000 to a gasoline tax. In this case, you

844
Chapter 29
Linear Programming
policy
urban
suburban
rural
build roads
2
5
3
gun control
8
2
5
farm subsidies
0
0
10
gasoline tax
10
0
2
Figure 29.1
The effects of policies on voters. Each entry describes the number of thousands of
urban, suburban, or rural voters who could be won over by spending $1,000 on advertising support
of a policy on a particular issue. Negative entries denote votes that would be lost.
would win 20.2/C0.8/C4.0/C9.10/ D 50 thousand urban votes, 20.5/C0.2/C
4.0/C9.0/ D 100 thousand suburban votes, and 20.3/C0.5/C4.10/C9.2/ D
82 thousand rural votes. You would win the exact number of votes desired in the
urban and suburban areas and more than enough votes in the rural area. (In fact,
in the rural area, you would receive more votes than there are voters.) In order to
garner these votes, you would have paid for 20 C 0 C 4 C 9 D 33 thousand dollars
of advertising.
Naturally, you may wonder whether this strategy is the best possible. That is,
could you achieve your goals while spending less on advertising? Additional trial
and error might help you to answer this question, but wouldn’t you rather have a
systematic method for answering such questions? In order to develop one, we shall
formulate this question mathematically. We introduce 4 variables:

x1 is the number of thousands of dollars spent on advertising on building roads,

x2 is the number of thousands of dollars spent on advertising on gun control,

x3 is the number of thousands of dollars spent on advertising on farm subsidies,
and

x4 is the number of thousands of dollars spent on advertising on a gasoline tax.
We can write the requirement that we win at least 50,000 urban votes as
2x1 C 8x2 C 0x3 C 10x4  50 :
(29.1)
Similarly, we can write the requirements that we win at least 100,000 suburban
votes and 25,000 rural votes as
5x1 C 2x2 C 0x3 C 0x4  100
(29.2)
and
3x1  5x2 C 10x3  2x4  25 :
(29.3)
Any setting of the variables x1; x2; x3; x4 that satisﬁes inequalities (29.1)–(29.3)
yields a strategy that wins a sufﬁcient number of each type of vote. In order to

Chapter 29
Linear Programming
845
keep costs as small as possible, you would like to minimize the amount spent on
advertising. That is, you want to minimize the expression
x1 C x2 C x3 C x4 :
(29.4)
Although negative advertising often occurs in political campaigns, there is no such
thing as negative-cost advertising. Consequently, we require that
x1  0; x2  0; x3  0; and x4  0 :
(29.5)
Combining inequalities (29.1)–(29.3) and (29.5) with the objective of minimiz-
ing (29.4), we obtain what is known as a “linear program.” We format this problem
as
minimize
x1
C
x2
C
x3
C
x4
(29.6)
subject to
2x1
C
8x2
C
0x3
C
10x4

50
(29.7)
5x1
C
2x2
C
0x3
C
0x4

100
(29.8)
3x1

5x2
C
10x3

2x4

25
(29.9)
x1; x2; x3; x4

0 :
(29.10)
The solution of this linear program yields your optimal strategy.
General linear programs
In the general linear-programming problem, we wish to optimize a linear function
subject to a set of linear inequalities. Given a set of real numbers a1; a2; : : : ; an and
a set of variables x1; x2; : : : ; xn, we deﬁne a linear function f on those variables
by
f .x1; x2; : : : ; xn/ D a1x1 C a2x2 C    C anxn D
n
X
jD1
ajxj :
If b is a real number and f is a linear function, then the equation
f .x1; x2; : : : ; xn/ D b
is a linear equality and the inequalities
f .x1; x2; : : : ; xn/  b
and
f .x1; x2; : : : ; xn/  b

846
Chapter 29
Linear Programming
are linear inequalities. We use the general term linear constraints to denote either
linear equalities or linear inequalities. In linear programming, we do not allow
strict inequalities. Formally, a linear-programming problem is the problem of
either minimizing or maximizing a linear function subject to a ﬁnite set of linear
constraints. If we are to minimize, then we call the linear program a minimization
linear program, and if we are to maximize, then we call the linear program a
maximization linear program.
The remainder of this chapter covers how to formulate and solve linear pro-
grams. Although several polynomial-time algorithms for linear programming have
been developed, we will not study them in this chapter. Instead, we shall study the
simplex algorithm, which is the oldest linear-programming algorithm. The simplex
algorithm does not run in polynomial time in the worst case, but it is fairly efﬁcient
and widely used in practice.
An overview of linear programming
In order to describe properties of and algorithms for linear programs, we ﬁnd it
convenient to express them in canonical forms. We shall use two forms, standard
and slack, in this chapter. We will deﬁne them precisely in Section 29.1. Infor-
mally, a linear program in standard form is the maximization of a linear function
subject to linear inequalities, whereas a linear program in slack form is the max-
imization of a linear function subject to linear equalities. We shall typically use
standard form for expressing linear programs, but we ﬁnd it more convenient to
use slack form when we describe the details of the simplex algorithm. For now, we
restrict our attention to maximizing a linear function on n variables subject to a set
of m linear inequalities.
Let us ﬁrst consider the following linear program with two variables:
maximize
x1
C
x2
(29.11)
subject to
4x1

x2

8
(29.12)
2x1
C
x2

10
(29.13)
5x1

2x2

2
(29.14)
x1; x2

0 :
(29.15)
We call any setting of the variables x1 and x2 that satisﬁes all the constraints
(29.12)–(29.15) a feasible solution to the linear program. If we graph the con-
straints in the .x1; x2/-Cartesian coordinate system, as in Figure 29.2(a), we see

Chapter 29
Linear Programming
847
4x1 – x2 ≤ 8
2x1 + x2 ≤ 10
x2
x1
x2 ≥ 0
x1 ≥ 0
5x1 – 2x2 ≥ –2
(a)
x2
x1
(b)
x1 + x2 = 0
x1 + x2 = 4
x1 + x2 = 8
Figure 29.2
(a) The linear program given in (29.12)–(29.15). Each constraint is represented by
a line and a direction. The intersection of the constraints, which is the feasible region, is shaded.
(b) The dotted lines show, respectively, the points for which the objective value is 0, 4, and 8. The
optimal solution to the linear program is x1 D 2 and x2 D 6 with objective value 8.
that the set of feasible solutions (shaded in the ﬁgure) forms a convex region1 in
the two-dimensional space. We call this convex region the feasible region and the
function we wish to maximize the objective function. Conceptually, we could eval-
uate the objective function x1 C x2 at each point in the feasible region; we call the
value of the objective function at a particular point the objective value. We could
then identify a point that has the maximum objective value as an optimal solution.
For this example (and for most linear programs), the feasible region contains an
inﬁnite number of points, and so we need to determine an efﬁcient way to ﬁnd a
point that achieves the maximum objective value without explicitly evaluating the
objective function at every point in the feasible region.
In two dimensions, we can optimize via a graphical procedure. The set of points
for which x1Cx2 D ´, for any ´, is a line with a slope of 1. If we plot x1Cx2 D 0,
we obtain the line with slope 1 through the origin, as in Figure 29.2(b). The
intersection of this line and the feasible region is the set of feasible solutions that
have an objective value of 0. In this case, that intersection of the line with the
feasible region is the single point .0; 0/. More generally, for any ´, the intersection
1An intuitive deﬁnition of a convex region is that it fulﬁlls the requirement that for any two points in
the region, all points on a line segment between them are also in the region.

848
Chapter 29
Linear Programming
of the line x1 C x2 D ´ and the feasible region is the set of feasible solutions that
have objective value ´. Figure 29.2(b) shows the lines x1 C x2 D 0, x1 C x2 D 4,
and x1 C x2 D 8. Because the feasible region in Figure 29.2 is bounded, there
must be some maximum value ´ for which the intersection of the line x1 C x2 D ´
and the feasible region is nonempty. Any point at which this occurs is an optimal
solution to the linear program, which in this case is the point x1 D 2 and x2 D 6
with objective value 8.
It is no accident that an optimal solution to the linear program occurs at a vertex
of the feasible region. The maximum value of ´ for which the line x1 C x2 D ´
intersects the feasible region must be on the boundary of the feasible region, and
thus the intersection of this line with the boundary of the feasible region is either a
single vertex or a line segment. If the intersection is a single vertex, then there is
just one optimal solution, and it is that vertex. If the intersection is a line segment,
every point on that line segment must have the same objective value; in particular,
both endpoints of the line segment are optimal solutions. Since each endpoint of a
line segment is a vertex, there is an optimal solution at a vertex in this case as well.
Although we cannot easily graph linear programs with more than two variables,
the same intuition holds. If we have three variables, then each constraint corre-
sponds to a half-space in three-dimensional space. The intersection of these half-
spaces forms the feasible region. The set of points for which the objective function
obtains a given value ´ is now a plane (assuming no degenerate conditions). If all
coefﬁcients of the objective function are nonnegative, and if the origin is a feasible
solution to the linear program, then as we move this plane away from the origin, in
a direction normal to the objective function, we ﬁnd points of increasing objective
value. (If the origin is not feasible or if some coefﬁcients in the objective function
are negative, the intuitive picture becomes slightly more complicated.) As in two
dimensions, because the feasible region is convex, the set of points that achieve
the optimal objective value must include a vertex of the feasible region. Simi-
larly, if we have n variables, each constraint deﬁnes a half-space in n-dimensional
space. We call the feasible region formed by the intersection of these half-spaces a
simplex. The objective function is now a hyperplane and, because of convexity, an
optimal solution still occurs at a vertex of the simplex.
The simplex algorithm takes as input a linear program and returns an optimal
solution. It starts at some vertex of the simplex and performs a sequence of itera-
tions. In each iteration, it moves along an edge of the simplex from a current vertex
to a neighboring vertex whose objective value is no smaller than that of the current
vertex (and usually is larger.) The simplex algorithm terminates when it reaches
a local maximum, which is a vertex from which all neighboring vertices have a
smaller objective value. Because the feasible region is convex and the objective
function is linear, this local optimum is actually a global optimum. In Section 29.4,

Chapter 29
Linear Programming
849
we shall use a concept called “duality” to show that the solution returned by the
simplex algorithm is indeed optimal.
Although the geometric view gives a good intuitive view of the operations of the
simplex algorithm, we shall not refer to it explicitly when developing the details
of the simplex algorithm in Section 29.3. Instead, we take an algebraic view. We
ﬁrst write the given linear program in slack form, which is a set of linear equalities.
These linear equalities express some of the variables, called “basic variables,” in
terms of other variables, called “nonbasic variables.” We move from one vertex
to another by making a basic variable become nonbasic and making a nonbasic
variable become basic. We call this operation a “pivot” and, viewed algebraically,
it is nothing more than rewriting the linear program in an equivalent slack form.
The two-variable example described above was particularly simple. We shall
need to address several more details in this chapter. These issues include iden-
tifying linear programs that have no solutions, linear programs that have no ﬁnite
optimal solution, and linear programs for which the origin is not a feasible solution.
Applications of linear programming
Linear programming has a large number of applications. Any textbook on opera-
tions research is ﬁlled with examples of linear programming, and linear program-
ming has become a standard tool taught to students in most business schools. The
election scenario is one typical example. Two more examples of linear program-
ming are the following:

An airline wishes to schedule its ﬂight crews. The Federal Aviation Adminis-
tration imposes many constraints, such as limiting the number of consecutive
hours that each crew member can work and insisting that a particular crew work
only on one model of aircraft during each month. The airline wants to schedule
crews on all of its ﬂights using as few crew members as possible.

An oil company wants to decide where to drill for oil. Siting a drill at a particu-
lar location has an associated cost and, based on geological surveys, an expected
payoff of some number of barrels of oil. The company has a limited budget for
locating new drills and wants to maximize the amount of oil it expects to ﬁnd,
given this budget.
With linear programs, we also model and solve graph and combinatorial prob-
lems, such as those appearing in this textbook. We have already seen a special
case of linear programming used to solve systems of difference constraints in Sec-
tion 24.4. In Section 29.2, we shall study how to formulate several graph and
network-ﬂow problems as linear programs. In Section 35.4, we shall use linear
programming as a tool to ﬁnd an approximate solution to another graph problem.

850
Chapter 29
Linear Programming
Algorithms for linear programming
This chapter studies the simplex algorithm. This algorithm, when implemented
carefully, often solves general linear programs quickly in practice. With some
carefully contrived inputs, however, the simplex algorithm can require exponential
time. The ﬁrst polynomial-time algorithm for linear programming was the ellipsoid
algorithm, which runs slowly in practice. A second class of polynomial-time algo-
rithms are known as interior-point methods. In contrast to the simplex algorithm,
which moves along the exterior of the feasible region and maintains a feasible solu-
tion that is a vertex of the simplex at each iteration, these algorithms move through
the interior of the feasible region. The intermediate solutions, while feasible, are
not necessarily vertices of the simplex, but the ﬁnal solution is a vertex. For large
inputs, interior-point algorithms can run as fast as, and sometimes faster than, the
simplex algorithm. The chapter notes point you to more information about these
algorithms.
If we add to a linear program the additional requirement that all variables take
on integer values, we have an integer linear program. Exercise 34.5-3 asks you
to show that just ﬁnding a feasible solution to this problem is NP-hard; since
no polynomial-time algorithms are known for any NP-hard problems, there is no
known polynomial-time algorithm for integer linear programming. In contrast, we
can solve a general linear-programming problem in polynomial time.
In this chapter, if we have a linear program with variables x D .x1; x2; : : : ; xn/
and wish to refer to a particular setting of the variables, we shall use the notation
Nx D . Nx1; Nx2; : : : ; Nxn/.
29.1
Standard and slack forms
This section describes two formats, standard form and slack form, that are use-
ful when we specify and work with linear programs. In standard form, all the
constraints are inequalities, whereas in slack form, all constraints are equalities
(except for those that require the variables to be nonnegative).
Standard form
In standard form, we are given n real numbers c1; c2; : : : ; cn; m real numbers
b1; b2; : : : ; bm; and mn real numbers aij for i D 1; 2; : : : ; m and j D 1; 2; : : : ; n.
We wish to ﬁnd n real numbers x1; x2; : : : ; xn that

29.1
Standard and slack forms
851
maximize
n
X
jD1
cjxj
(29.16)
subject to
n
X
jD1
aijxj

bi
for i D 1; 2; : : : ; m
(29.17)
xj

0
for j D 1; 2; : : : ; n :
(29.18)
Generalizing the terminology we introduced for the two-variable linear program,
we call expression (29.16) the objective function and the n C m inequalities in
lines (29.17) and (29.18) the constraints. The n constraints in line (29.18) are the
nonnegativity constraints. An arbitrary linear program need not have nonnegativ-
ity constraints, but standard form requires them. Sometimes we ﬁnd it convenient
to express a linear program in a more compact form. If we create an m 	 n matrix
A D .aij/, an m-vector b D .bi/, an n-vector c D .cj/, and an n-vector x D .xj/,
then we can rewrite the linear program deﬁned in (29.16)–(29.18) as
maximize
cTx
(29.19)
subject to
Ax

b
(29.20)
x

0 :
(29.21)
In line (29.19), cTx is the inner product of two vectors. In inequality (29.20), Ax
is a matrix-vector product, and in inequality (29.21), x  0 means that each entry
of the vector x must be nonnegative. We see that we can specify a linear program
in standard form by a tuple .A; b; c/, and we shall adopt the convention that A, b,
and c always have the dimensions given above.
We now introduce terminology to describe solutions to linear programs. We used
some of this terminology in the earlier example of a two-variable linear program.
We call a setting of the variables Nx that satisﬁes all the constraints a feasible solu-
tion, whereas a setting of the variables Nx that fails to satisfy at least one constraint
is an infeasible solution. We say that a solution Nx has objective value cT Nx. A fea-
sible solution Nx whose objective value is maximum over all feasible solutions is an
optimal solution, and we call its objective value cT Nx the optimal objective value.
If a linear program has no feasible solutions, we say that the linear program is in-
feasible; otherwise it is feasible. If a linear program has some feasible solutions
but does not have a ﬁnite optimal objective value, we say that the linear program
is unbounded. Exercise 29.1-9 asks you to show that a linear program can have a
ﬁnite optimal objective value even if the feasible region is not bounded.

852
Chapter 29
Linear Programming
Converting linear programs into standard form
It is always possible to convert a linear program, given as minimizing or maxi-
mizing a linear function subject to linear constraints, into standard form. A linear
program might not be in standard form for any of four possible reasons:
1. The objective function might be a minimization rather than a maximization.
2. There might be variables without nonnegativity constraints.
3. There might be equality constraints, which have an equal sign rather than a
less-than-or-equal-to sign.
4. There might be inequality constraints, but instead of having a less-than-or-
equal-to sign, they have a greater-than-or-equal-to sign.
When converting one linear program L into another linear program L0, we would
like the property that an optimal solution to L0 yields an optimal solution to L. To
capture this idea, we say that two maximization linear programs L and L0 are
equivalent if for each feasible solution Nx to L with objective value ´, there is
a corresponding feasible solution Nx0 to L0 with objective value ´, and for each
feasible solution Nx0 to L0 with objective value ´, there is a corresponding feasible
solution Nx to L with objective value ´. (This deﬁnition does not imply a one-to-
one correspondence between feasible solutions.) A minimization linear program L
and a maximization linear program L0 are equivalent if for each feasible solution Nx
to L with objective value ´, there is a corresponding feasible solution Nx0 to L0 with
objective value ´, and for each feasible solution Nx0 to L0 with objective value ´,
there is a corresponding feasible solution Nx to L with objective value ´.
We now show how to remove, one by one, each of the possible problems in the
list above. After removing each one, we shall argue that the new linear program is
equivalent to the old one.
To convert a minimization linear program L into an equivalent maximization lin-
ear program L0, we simply negate the coefﬁcients in the objective function. Since
L and L0 have identical sets of feasible solutions and, for any feasible solution, the
objective value in L is the negative of the objective value in L0, these two linear
programs are equivalent. For example, if we have the linear program
minimize
2x1
C
3x2
subject to
x1
C
x2
D
7
x1

2x2

4
x1

0 ;
and we negate the coefﬁcients of the objective function, we obtain

29.1
Standard and slack forms
853
maximize
2x1

3x2
subject to
x1
C
x2
D
7
x1

2x2

4
x1

0 :
Next, we show how to convert a linear program in which some of the variables
do not have nonnegativity constraints into one in which each variable has a non-
negativity constraint. Suppose that some variable xj does not have a nonnegativity
constraint. Then, we replace each occurrence of xj by x0
j  x00
j , and add the non-
negativity constraints x0
j  0 and x00
j  0. Thus, if the objective function has a
term cjxj, we replace it by cjx0
j  cjx00
j , and if constraint i has a term aijxj, we
replace it by aijx0
j  aijx00
j . Any feasible solution yx to the new linear program cor-
responds to a feasible solution Nx to the original linear program with Nxj D yx0
j  yx00
j
and with the same objective value. Also, any feasible solution Nx to the original
linear program corresponds to a feasible solution yx to the new linear program with
yx0
j D Nxj and yx00
j D 0 if Nxj  0, or with yx00
j D Nxj and yx0
j D 0 if Nxj < 0. The two
linear programs have the same objective value regardless of the sign of Nxj. Thus,
the two linear programs are equivalent. We apply this conversion scheme to each
variable that does not have a nonnegativity constraint to yield an equivalent linear
program in which all variables have nonnegativity constraints.
Continuing the example, we want to ensure that each variable has a correspond-
ing nonnegativity constraint. Variable x1 has such a constraint, but variable x2 does
not. Therefore, we replace x2 by two variables x0
2 and x00
2, and we modify the linear
program to obtain
maximize
2x1

3x0
2
C
3x00
2
subject to
x1
C
x0
2

x00
2
D
7
(29.22)
x1

2x0
2
C
2x00
2

4
x1; x0
2; x00
2

0 :
Next, we convert equality constraints into inequality constraints. Suppose that a
linear program has an equality constraint f .x1; x2; : : : ; xn/ D b. Since x D y if
and only if both x  y and x  y, we can replace this equality constraint by the
pair of inequality constraints f .x1; x2; : : : ; xn/  b and f .x1; x2; : : : ; xn/  b.
Repeating this conversion for each equality constraint yields a linear program in
which all constraints are inequalities.
Finally, we can convert the greater-than-or-equal-to constraints to less-than-or-
equal-to constraints by multiplying these constraints through by 1. That is, any
inequality of the form

854
Chapter 29
Linear Programming
n
X
jD1
aijxj  bi
is equivalent to
n
X
jD1
aijxj  bi :
Thus, by replacing each coefﬁcient aij by aij and each value bi by bi, we obtain
an equivalent less-than-or-equal-to constraint.
Finishing our example, we replace the equality in constraint (29.22) by two in-
equalities, obtaining
maximize
2x1

3x0
2
C
3x00
2
subject to
x1
C
x0
2

x00
2

7
x1
C
x0
2

x00
2

7
(29.23)
x1

2x0
2
C
2x00
2

4
x1; x0
2; x00
2

0 :
Finally, we negate constraint (29.23). For consistency in variable names, we re-
name x0
2 to x2 and x00
2 to x3, obtaining the standard form
maximize
2x1

3x2
C
3x3
(29.24)
subject to
x1
C
x2

x3

7
(29.25)
x1

x2
C
x3

7
(29.26)
x1

2x2
C
2x3

4
(29.27)
x1; x2; x3

0 :
(29.28)
Converting linear programs into slack form
To efﬁciently solve a linear program with the simplex algorithm, we prefer to ex-
press it in a form in which some of the constraints are equality constraints. More
precisely, we shall convert it into a form in which the nonnegativity constraints are
the only inequality constraints, and the remaining constraints are equalities. Let
n
X
jD1
aijxj  bi
(29.29)

29.1
Standard and slack forms
855
be an inequality constraint. We introduce a new variable s and rewrite inequal-
ity (29.29) as the two constraints
s
D
bi 
n
X
jD1
aijxj ;
(29.30)
s

0 :
(29.31)
We call s a slack variable because it measures the slack, or difference, between
the left-hand and right-hand sides of equation (29.29). (We shall soon see why we
ﬁnd it convenient to write the constraint with only the slack variable on the left-
hand side.) Because inequality (29.29) is true if and only if both equation (29.30)
and inequality (29.31) are true, we can convert each inequality constraint of a lin-
ear program in this way to obtain an equivalent linear program in which the only
inequality constraints are the nonnegativity constraints. When converting from
standard to slack form, we shall use xnCi (instead of s) to denote the slack variable
associated with the ith inequality. The ith constraint is therefore
xnCi D bi 
n
X
jD1
aijxj ;
(29.32)
along with the nonnegativity constraint xnCi  0.
By converting each constraint of a linear program in standard form, we obtain a
linear program in a different form. For example, for the linear program described
in (29.24)–(29.28), we introduce slack variables x4, x5, and x6, obtaining
maximize
2x1

3x2
C
3x3
(29.33)
subject to
x4
D
7

x1

x2
C
x3
(29.34)
x5
D
7
C
x1
C
x2

x3
(29.35)
x6
D
4

x1
C
2x2

2x3
(29.36)
x1; x2; x3; x4; x5; x6

0
:
(29.37)
In this linear program, all the constraints except for the nonnegativity constraints
are equalities, and each variable is subject to a nonnegativity constraint. We write
each equality constraint with one of the variables on the left-hand side of the equal-
ity and all others on the right-hand side. Furthermore, each equation has the same
set of variables on the right-hand side, and these variables are also the only ones
that appear in the objective function. We call the variables on the left-hand side of
the equalities basic variables and those on the right-hand side nonbasic variables.
For linear programs that satisfy these conditions, we shall sometimes omit the
words “maximize” and “subject to,” as well as the explicit nonnegativity con-
straints. We shall also use the variable ´ to denote the value of the objective func-

856
Chapter 29
Linear Programming
tion. We call the resulting format slack form. If we write the linear program given
in (29.33)–(29.37) in slack form, we obtain
´
D
2x1

3x2
C
3x3
(29.38)
x4
D
7

x1

x2
C
x3
(29.39)
x5
D
7
C
x1
C
x2

x3
(29.40)
x6
D
4

x1
C
2x2

2x3 :
(29.41)
As with standard form, we ﬁnd it convenient to have a more concise notation
for describing a slack form. As we shall see in Section 29.3, the sets of basic and
nonbasic variables will change as the simplex algorithm runs. We use N to denote
the set of indices of the nonbasic variables and B to denote the set of indices of
the basic variables. We always have that jN j D n, jBj D m, and N [ B D
f1; 2; : : : ; n C mg. The equations are indexed by the entries of B, and the variables
on the right-hand sides are indexed by the entries of N . As in standard form, we use
bi, cj, and aij to denote constant terms and coefﬁcients. We also use  to denote
an optional constant term in the objective function. (We shall see a little later that
including the constant term in the objective function makes it easy to determine the
value of the objective function.) Thus we can concisely deﬁne a slack form by a
tuple .N; B; A; b; c; /, denoting the slack form
´
D

C
X
j2N
cjxj
(29.42)
xi
D
bi

X
j2N
aijxj
for i 2 B ;
(29.43)
in which all variables x are constrained to be nonnegative. Because we subtract
the sum P
j2N aijxj in (29.43), the values aij are actually the negatives of the
coefﬁcients as they “appear” in the slack form.
For example, in the slack form
´
D
28

x3
6

x5
6

2x6
3
x1
D
8
C
x3
6
C
x5
6

x6
3
x2
D
4

8x3
3

2x5
3
C
x6
3
x4
D
18

x3
2
C
x5
2
;
we have B D f1; 2; 4g, N D f3; 5; 6g,

29.1
Standard and slack forms
857
A D

a13
a15
a16
a23
a25
a26
a43
a45
a46

D

1=6
1=6
1=3
8=3
2=3
1=3
1=2
1=2
0

;
b D

b1
b2
b4

D

8
4
18

;
c D

 c3
c5
c6

T D

 1=6
1=6
2=3 
T, and  D 28. Note that the
indices into A, b, and c are not necessarily sets of contiguous integers; they depend
on the index sets B and N . As an example of the entries of A being the negatives
of the coefﬁcients as they appear in the slack form, observe that the equation for x1
includes the term x3=6, yet the coefﬁcient a13 is actually 1=6 rather than C1=6.
Exercises
29.1-1
If we express the linear program in (29.24)–(29.28) in the compact notation of
(29.19)–(29.21), what are n, m, A, b, and c?
29.1-2
Give three feasible solutions to the linear program in (29.24)–(29.28). What is the
objective value of each one?
29.1-3
For the slack form in (29.38)–(29.41), what are N , B, A, b, c, and ?
29.1-4
Convert the following linear program into standard form:
minimize
2x1
C
7x2
C
x3
subject to
x1

x3
D
7
3x1
C
x2

24
x2

0
x3

0 :

858
Chapter 29
Linear Programming
29.1-5
Convert the following linear program into slack form:
maximize
2x1

6x3
subject to
x1
C
x2

x3

7
3x1

x2

8
x1
C
2x2
C
2x3

0
x1; x2; x3

0 :
What are the basic and nonbasic variables?
29.1-6
Show that the following linear program is infeasible:
maximize
3x1

2x2
subject to
x1
C
x2

2
2x1

2x2

10
x1; x2

0 :
29.1-7
Show that the following linear program is unbounded:
maximize
x1

x2
subject to
2x1
C
x2

1
x1

2x2

2
x1; x2

0 :
29.1-8
Suppose that we have a general linear program with n variables and m constraints,
and suppose that we convert it into standard form. Give an upper bound on the
number of variables and constraints in the resulting linear program.
29.1-9
Give an example of a linear program for which the feasible region is not bounded,
but the optimal objective value is ﬁnite.

29.2
Formulating problems as linear programs
859
29.2
Formulating problems as linear programs
Although we shall focus on the simplex algorithm in this chapter, it is also impor-
tant to be able to recognize when we can formulate a problem as a linear program.
Once we cast a problem as a polynomial-sized linear program, we can solve it
in polynomial time by the ellipsoid algorithm or interior-point methods. Several
linear-programming software packages can solve problems efﬁciently, so that once
the problem is in the form of a linear program, such a package can solve it.
We shall look at several concrete examples of linear-programming problems. We
start with two problems that we have already studied: the single-source shortest-
paths problem (see Chapter 24) and the maximum-ﬂow problem (see Chapter 26).
We then describe the minimum-cost-ﬂow problem. Although the minimum-cost-
ﬂow problem has a polynomial-time algorithm that is not based on linear program-
ming, we won’t describe the algorithm. Finally, we describe the multicommodity-
ﬂow problem, for which the only known polynomial-time algorithm is based on
linear programming.
When we solved graph problems in Part VI, we used attribute notation, such
as :d and .u; /:f. Linear programs typically use subscripted variables rather
than objects with attached attributes, however. Therefore, when we express vari-
ables in linear programs, we shall indicate vertices and edges through subscripts.
For example, we denote the shortest-path weight for vertex  not by :d but by d.
Similarly, we denote the ﬂow from vertex u to vertex  not by .u; /:f but by fu.
For quantities that are given as inputs to problems, such as edge weights or capac-
ities, we shall continue to use notations such as w.u; / and c.u:/.
Shortest paths
We can formulate the single-source shortest-paths problem as a linear program.
In this section, we shall focus on how to formulate the single-pair shortest-path
problem, leaving the extension to the more general single-source shortest-paths
problem as Exercise 29.2-3.
In the single-pair shortest-path problem, we are given a weighted, directed graph
G D .V; E/, with weight function w W E ! R mapping edges to real-valued
weights, a source vertex s, and destination vertex t. We wish to compute the
value dt, which is the weight of a shortest path from s to t. To express this prob-
lem as a linear program, we need to determine a set of variables and constraints that
deﬁne when we have a shortest path from s to t. Fortunately, the Bellman-Ford al-
gorithm does exactly this. When the Bellman-Ford algorithm terminates, it has
computed, for each vertex , a value d (using subscript notation here rather than
attribute notation) such that for each edge .u; / 2 E, we have d  du C w.u; /.

860
Chapter 29
Linear Programming
The source vertex initially receives a value ds D 0, which never changes. Thus
we obtain the following linear program to compute the shortest-path weight from s
to t:
maximize
dt
(29.44)
subject to
d

du C w.u; /
for each edge .u; / 2 E ;
(29.45)
ds
D
0 :
(29.46)
You might be surprised that this linear program maximizes an objective function
when it is supposed to compute shortest paths. We do not want to minimize the
objective function, since then setting Nd D 0 for all  2 V would yield an optimal
solution to the linear program without solving the shortest-paths problem. We
maximize because an optimal solution to the shortest-paths problem sets each Nd
to minuW.u;/2E
˚ Ndu C w.u; /

, so that Nd is the largest value that is less than or
equal to all of the values in the set
˚ Ndu C w.u; /

. We want to maximize d
for all vertices  on a shortest path from s to t subject to these constraints on all
vertices , and maximizing dt achieves this goal.
This linear program has jV j variables d, one for each vertex  2 V . It also
has jEj C 1 constraints: one for each edge, plus the additional constraint that the
source vertex’s shortest-path weight always has the value 0.
Maximum ﬂow
Next, we express the maximum-ﬂow problem as a linear program. Recall that we
are given a directed graph G D .V; E/ in which each edge .u; / 2 E has a
nonnegative capacity c.u; /  0, and two distinguished vertices: a source s and
a sink t. As deﬁned in Section 26.1, a ﬂow is a nonnegative real-valued function
f W V 	 V ! R that satisﬁes the capacity constraint and ﬂow conservation. A
maximum ﬂow is a ﬂow that satisﬁes these constraints and maximizes the ﬂow
value, which is the total ﬂow coming out of the source minus the total ﬂow into the
source. A ﬂow, therefore, satisﬁes linear constraints, and the value of a ﬂow is a
linear function. Recalling also that we assume that c.u; / D 0 if .u; / 62 E and
that there are no antiparallel edges, we can express the maximum-ﬂow problem as
a linear program:
maximize
X
2V
fs

X
2V
fs
(29.47)
subject to
fu

c.u; /
for each u;  2 V ;
(29.48)
X
2V
fu
D
X
2V
fu
for each u 2 V  fs; tg ;
(29.49)
fu

0
for each u;  2 V :
(29.50)

29.2
Formulating problems as linear programs
861
This linear program has jV j2 variables, corresponding to the ﬂow between each
pair of vertices, and it has 2 jV j2 C jV j  2 constraints.
It is usually more efﬁcient to solve a smaller-sized linear program. The linear
program in (29.47)–(29.50) has, for ease of notation, a ﬂow and capacity of 0 for
each pair of vertices u;  with .u; / 62 E. It would be more efﬁcient to rewrite the
linear program so that it has O.V C E/ constraints. Exercise 29.2-5 asks you to
do so.
Minimum-cost ﬂow
In this section, we have used linear programming to solve problems for which we
already knew efﬁcient algorithms. In fact, an efﬁcient algorithm designed specif-
ically for a problem, such as Dijkstra’s algorithm for the single-source shortest-
paths problem, or the push-relabel method for maximum ﬂow, will often be more
efﬁcient than linear programming, both in theory and in practice.
The real power of linear programming comes from the ability to solve new prob-
lems. Recall the problem faced by the politician in the beginning of this chapter.
The problem of obtaining a sufﬁcient number of votes, while not spending too
much money, is not solved by any of the algorithms that we have studied in this
book, yet we can solve it by linear programming. Books abound with such real-
world problems that linear programming can solve. Linear programming is also
particularly useful for solving variants of problems for which we may not already
know of an efﬁcient algorithm.
Consider, for example, the following generalization of the maximum-ﬂow prob-
lem. Suppose that, in addition to a capacity c.u; / for each edge .u; /, we are
given a real-valued cost a.u; /. As in the maximum-ﬂow problem, we assume that
c.u; / D 0 if .u; / 62 E, and that there are no antiparallel edges. If we send fu
units of ﬂow over edge .u; /, we incur a cost of a.u; /fu. We are also given a
ﬂow demand d. We wish to send d units of ﬂow from s to t while minimizing the
total cost P
.u;/2E a.u; /fu incurred by the ﬂow. This problem is known as the
minimum-cost-ﬂow problem.
Figure 29.3(a) shows an example of the minimum-cost-ﬂow problem. We wish
to send 4 units of ﬂow from s to t while incurring the minimum total cost. Any
particular legal ﬂow, that is, a function f satisfying constraints (29.48)–(29.49),
incurs a total cost of P
.u;/2E a.u; /fu. We wish to ﬁnd the particular 4-unit
ﬂow that minimizes this cost. Figure 29.3(b) shows an optimal solution, with total
cost P
.u;/2E a.u; /fu D .2  2/ C .5  2/ C .3  1/ C .7  1/ C .1  3/ D 27:
There are polynomial-time algorithms speciﬁcally designed for the minimum-
cost-ﬂow problem, but they are beyond the scope of this book. We can, however,
express the minimum-cost-ﬂow problem as a linear program. The linear program
looks similar to the one for the maximum-ﬂow problem with the additional con-

862
Chapter 29
Linear Programming
s
x
t
y
(a)
c = 1
a = 3
c = 5
a = 2
c = 4
a = 1
c = 2
a = 7
c = 2
a = 5
s
x
t
y
(b)
1/1
a = 3
2/5
a = 2
3/4
a = 1
1/2
a = 7
2/2
a = 5
Figure 29.3
(a) An example of a minimum-cost-ﬂow problem. We denote the capacities by c and
the costs by a. Vertex s is the source and vertex t is the sink, and we wish to send 4 units of ﬂow
from s to t. (b) A solution to the minimum-cost ﬂow problem in which 4 units of ﬂow are sent from s
to t. For each edge, the ﬂow and capacity are written as ﬂow/capacity.
straint that the value of the ﬂow be exactly d units, and with the new objective
function of minimizing the cost:
minimize
X
.u;/2E
a.u; /fu
(29.51)
subject to
fu

c.u; /
for each u;  2 V ;
X
2V
fu 
X
2V
fu
D
0
for each u 2 V  fs; tg ;
X
2V
fs 
X
2V
fs
D
d ;
fu

0
for each u;  2 V :
(29.52)
Multicommodity ﬂow
As a ﬁnal example, we consider another ﬂow problem. Suppose that the Lucky
Puck company from Section 26.1 decides to diversify its product line and ship
not only hockey pucks, but also hockey sticks and hockey helmets. Each piece of
equipment is manufactured in its own factory, has its own warehouse, and must
be shipped, each day, from factory to warehouse. The sticks are manufactured in
Vancouver and must be shipped to Saskatoon, and the helmets are manufactured in
Edmonton and must be shipped to Regina. The capacity of the shipping network
does not change, however, and the different items, or commodities, must share the
same network.
This example is an instance of a multicommodity-ﬂow problem. In this problem,
we are again given a directed graph G D .V; E/ in which each edge .u; / 2 E
has a nonnegative capacity c.u; /  0. As in the maximum-ﬂow problem, we im-
plicitly assume that c.u; / D 0 for .u; / 62 E, and that the graph has no antipar-

29.2
Formulating problems as linear programs
863
allel edges. In addition, we are given k different commodities, K1; K2; : : : ; Kk,
where we specify commodity i by the triple Ki D .si; ti; di/. Here, vertex si is
the source of commodity i, vertex ti is the sink of commodity i, and di is the de-
mand for commodity i, which is the desired ﬂow value for the commodity from si
to ti. We deﬁne a ﬂow for commodity i, denoted by fi, (so that fiu is the ﬂow of
commodity i from vertex u to vertex ) to be a real-valued function that satisﬁes
the ﬂow-conservation and capacity constraints. We now deﬁne fu, the aggregate
ﬂow, to be the sum of the various commodity ﬂows, so that fu D Pk
iD1 fiu. The
aggregate ﬂow on edge .u; / must be no more than the capacity of edge .u; /.
We are not trying to minimize any objective function in this problem; we need
only determine whether such a ﬂow exists. Thus, we write a linear program with a
“null” objective function:
minimize
0
subject to
k
X
iD1
fiu

c.u; /
for each u;  2 V ;
X
2V
fiu 
X
2V
fiu
D
0
for each i D 1; 2; : : : ; k and
for each u 2 V  fsi; tig ;
X
2V
fi;si; 
X
2V
fi;;si
D
di
for each i D 1; 2; : : : ; k ;
fiu

0
for each u;  2 V and
for each i D 1; 2; : : : ; k :
The only known polynomial-time algorithm for this problem expresses it as a linear
program and then solves it with a polynomial-time linear-programming algorithm.
Exercises
29.2-1
Put the single-pair shortest-path linear program from (29.44)–(29.46) into standard
form.
29.2-2
Write out explicitly the linear program corresponding to ﬁnding the shortest path
from node s to node y in Figure 24.2(a).
29.2-3
In the single-source shortest-paths problem, we want to ﬁnd the shortest-path
weights from a source vertex s to all vertices  2 V . Given a graph G, write a

864
Chapter 29
Linear Programming
linear program for which the solution has the property that d is the shortest-path
weight from s to  for each vertex  2 V .
29.2-4
Write out explicitly the linear program corresponding to ﬁnding the maximum ﬂow
in Figure 26.1(a).
29.2-5
Rewrite the linear program for maximum ﬂow (29.47)–(29.50) so that it uses only
O.V C E/ constraints.
29.2-6
Write a linear program that, given a bipartite graph G D .V; E/, solves the maxi-
mum-bipartite-matching problem.
29.2-7
In the minimum-cost multicommodity-ﬂow problem, we are given directed graph
G D .V; E/ in which each edge .u; / 2 E has a nonnegative capacity c.u; /  0
and a cost a.u; /. As in the multicommodity-ﬂow problem, we are given k dif-
ferent commodities, K1; K2; : : : ; Kk, where we specify commodity i by the triple
Ki D .si; ti; di/. We deﬁne the ﬂow fi for commodity i and the aggregate ﬂow fu
on edge .u; / as in the multicommodity-ﬂow problem. A feasible ﬂow is one
in which the aggregate ﬂow on each edge .u; / is no more than the capacity of
edge .u; /. The cost of a ﬂow is P
u;2V a.u; /fu, and the goal is to ﬁnd the
feasible ﬂow of minimum cost. Express this problem as a linear program.
29.3
The simplex algorithm
The simplex algorithm is the classical method for solving linear programs. In con-
trast to most of the other algorithms in this book, its running time is not polynomial
in the worst case. It does yield insight into linear programs, however, and is often
remarkably fast in practice.
In addition to having a geometric interpretation, described earlier in this chapter,
the simplex algorithm bears some similarity to Gaussian elimination, discussed in
Section 28.1. Gaussian elimination begins with a system of linear equalities whose
solution is unknown. In each iteration, we rewrite this system in an equivalent
form that has some additional structure. After some number of iterations, we have
rewritten the system so that the solution is simple to obtain. The simplex algo-
rithm proceeds in a similar manner, and we can view it as Gaussian elimination for
inequalities.

29.3
The simplex algorithm
865
We now describe the main idea behind an iteration of the simplex algorithm.
Associated with each iteration will be a “basic solution” that we can easily obtain
from the slack form of the linear program: set each nonbasic variable to 0 and
compute the values of the basic variables from the equality constraints. An iteration
converts one slack form into an equivalent slack form. The objective value of the
associated basic feasible solution will be no less than that at the previous iteration,
and usually greater. To achieve this increase in the objective value, we choose a
nonbasic variable such that if we were to increase that variable’s value from 0, then
the objective value would increase, too. The amount by which we can increase
the variable is limited by the other constraints. In particular, we raise it until some
basic variable becomes 0. We then rewrite the slack form, exchanging the roles
of that basic variable and the chosen nonbasic variable. Although we have used a
particular setting of the variables to guide the algorithm, and we shall use it in our
proofs, the algorithm does not explicitly maintain this solution. It simply rewrites
the linear program until an optimal solution becomes “obvious.”
An example of the simplex algorithm
We begin with an extended example. Consider the following linear program in
standard form:
maximize
3x1
C
x2
C
2x3
(29.53)
subject to
x1
C
x2
C
3x3

30
(29.54)
2x1
C
2x2
C
5x3

24
(29.55)
4x1
C
x2
C
2x3

36
(29.56)
x1; x2; x3

0 :
(29.57)
In order to use the simplex algorithm, we must convert the linear program into
slack form; we saw how to do so in Section 29.1. In addition to being an algebraic
manipulation, slack is a useful algorithmic concept. Recalling from Section 29.1
that each variable has a corresponding nonnegativity constraint, we say that an
equality constraint is tight for a particular setting of its nonbasic variables if they
cause the constraint’s basic variable to become 0. Similarly, a setting of the non-
basic variables that would make a basic variable become negative violates that
constraint. Thus, the slack variables explicitly maintain how far each constraint is
from being tight, and so they help to determine how much we can increase values
of nonbasic variables without violating any constraints.
Associating the slack variables x4, x5, and x6 with inequalities (29.54)–(29.56),
respectively, and putting the linear program into slack form, we obtain

866
Chapter 29
Linear Programming
´
D
3x1
C
x2
C
2x3
(29.58)
x4
D
30

x1

x2

3x3
(29.59)
x5
D
24

2x1

2x2

5x3
(29.60)
x6
D
36

4x1

x2

2x3 :
(29.61)
The system of constraints (29.59)–(29.61) has 3 equations and 6 variables. Any
setting of the variables x1, x2, and x3 deﬁnes values for x4, x5, and x6; therefore,
we have an inﬁnite number of solutions to this system of equations. A solution is
feasible if all of x1; x2; : : : ; x6 are nonnegative, and there can be an inﬁnite num-
ber of feasible solutions as well. The inﬁnite number of possible solutions to a
system such as this one will be useful in later proofs. We focus on the basic solu-
tion: set all the (nonbasic) variables on the right-hand side to 0 and then compute
the values of the (basic) variables on the left-hand side. In this example, the ba-
sic solution is . Nx1; Nx2; : : : ; Nx6/ D .0; 0; 0; 30; 24; 36/ and it has objective value
´ D .3  0/ C .1  0/ C .2  0/ D 0. Observe that this basic solution sets Nxi D bi
for each i 2 B. An iteration of the simplex algorithm rewrites the set of equations
and the objective function so as to put a different set of variables on the right-
hand side. Thus, a different basic solution is associated with the rewritten problem.
We emphasize that the rewrite does not in any way change the underlying linear-
programming problem; the problem at one iteration has the identical set of feasible
solutions as the problem at the previous iteration. The problem does, however,
have a different basic solution than that of the previous iteration.
If a basic solution is also feasible, we call it a basic feasible solution. As we run
the simplex algorithm, the basic solution is almost always a basic feasible solution.
We shall see in Section 29.5, however, that for the ﬁrst few iterations of the simplex
algorithm, the basic solution might not be feasible.
Our goal, in each iteration, is to reformulate the linear program so that the basic
solution has a greater objective value. We select a nonbasic variable xe whose
coefﬁcient in the objective function is positive, and we increase the value of xe as
much as possible without violating any of the constraints. The variable xe becomes
basic, and some other variable xl becomes nonbasic. The values of other basic
variables and of the objective function may also change.
To continue the example, let’s think about increasing the value of x1. As we
increase x1, the values of x4, x5, and x6 all decrease. Because we have a nonnega-
tivity constraint for each variable, we cannot allow any of them to become negative.
If x1 increases above 30, then x4 becomes negative, and x5 and x6 become nega-
tive when x1 increases above 12 and 9, respectively. The third constraint (29.61) is
the tightest constraint, and it limits how much we can increase x1. Therefore, we
switch the roles of x1 and x6. We solve equation (29.61) for x1 and obtain
x1 D 9  x2
4  x3
2  x6
4 :
(29.62)

29.3
The simplex algorithm
867
To rewrite the other equations with x6 on the right-hand side, we substitute for x1
using equation (29.62). Doing so for equation (29.59), we obtain
x4
D
30  x1  x2  3x3
D
30 

9  x2
4  x3
2  x6
4

 x2  3x3
D
21  3x2
4
 5x3
2
C x6
4 :
(29.63)
Similarly, we combine equation (29.62) with constraint (29.60) and with objective
function (29.58) to rewrite our linear program in the following form:
´
D
27
C
x2
4
C
x3
2

3x6
4
(29.64)
x1
D
9

x2
4

x3
2

x6
4
(29.65)
x4
D
21

3x2
4

5x3
2
C
x6
4
(29.66)
x5
D
6

3x2
2

4x3
C
x6
2
:
(29.67)
We call this operation a pivot. As demonstrated above, a pivot chooses a nonbasic
variable xe, called the entering variable, and a basic variable xl, called the leaving
variable, and exchanges their roles.
The linear program described in equations (29.64)–(29.67) is equivalent to the
linear program described in equations (29.58)–(29.61). We perform two operations
in the simplex algorithm: rewrite equations so that variables move between the left-
hand side and the right-hand side, and substitute one equation into another. The ﬁrst
operation trivially creates an equivalent problem, and the second, by elementary
linear algebra, also creates an equivalent problem. (See Exercise 29.3-3.)
To demonstrate this equivalence, observe that our original basic solution .0; 0;
0; 30; 24; 36/ satisﬁes the new equations (29.65)–(29.67) and has objective value
27 C .1=4/  0 C .1=2/  0  .3=4/  36 D 0. The basic solution associated with the
new linear program sets the nonbasic values to 0 and is .9; 0; 0; 21; 6; 0/, with ob-
jective value ´ D 27. Simple arithmetic veriﬁes that this solution also satisﬁes
equations (29.59)–(29.61) and, when plugged into objective function (29.58), has
objective value .3  9/ C .1  0/ C .2  0/ D 27.
Continuing the example, we wish to ﬁnd a new variable whose value we wish to
increase. We do not want to increase x6, since as its value increases, the objective
value decreases. We can attempt to increase either x2 or x3; let us choose x3. How
far can we increase x3 without violating any of the constraints? Constraint (29.65)
limits it to 18, constraint (29.66) limits it to 42=5, and constraint (29.67) limits
it to 3=2. The third constraint is again the tightest one, and therefore we rewrite
the third constraint so that x3 is on the left-hand side and x5 is on the right-hand

868
Chapter 29
Linear Programming
side. We then substitute this new equation, x3 D 3=2  3x2=8  x5=4 C x6=8, into
equations (29.64)–(29.66) and obtain the new, but equivalent, system
´
D
111
4
C
x2
16

x5
8

11x6
16
(29.68)
x1
D
33
4

x2
16
C
x5
8

5x6
16
(29.69)
x3
D
3
2

3x2
8

x5
4
C
x6
8
(29.70)
x4
D
69
4
C
3x2
16
C
5x5
8

x6
16 :
(29.71)
This system has the associated basic solution .33=4; 0; 3=2; 69=4; 0; 0/, with ob-
jective value 111=4. Now the only way to increase the objective value is to in-
crease x2. The three constraints give upper bounds of 132, 4, and 1, respectively.
(We get an upper bound of 1 from constraint (29.71) because, as we increase x2,
the value of the basic variable x4 increases also. This constraint, therefore, places
no restriction on how much we can increase x2.) We increase x2 to 4, and it be-
comes nonbasic. Then we solve equation (29.70) for x2 and substitute in the other
equations to obtain
´
D
28

x3
6

x5
6

2x6
3
(29.72)
x1
D
8
C
x3
6
C
x5
6

x6
3
(29.73)
x2
D
4

8x3
3

2x5
3
C
x6
3
(29.74)
x4
D
18

x3
2
C
x5
2
:
(29.75)
At this point, all coefﬁcients in the objective function are negative. As we shall see
later in this chapter, this situation occurs only when we have rewritten the linear
program so that the basic solution is an optimal solution. Thus, for this problem,
the solution .8; 4; 0; 18; 0; 0/, with objective value 28, is optimal. We can now
return to our original linear program given in (29.53)–(29.57). The only variables
in the original linear program are x1, x2, and x3, and so our solution is x1 D 8,
x2 D 4, and x3 D 0, with objective value .3  8/ C .1  4/ C .2  0/ D 28. Note
that the values of the slack variables in the ﬁnal solution measure how much slack
remains in each inequality. Slack variable x4 is 18, and in inequality (29.54), the
left-hand side, with value 8 C 4 C 0 D 12, is 18 less than the right-hand side of 30.
Slack variables x5 and x6 are 0 and indeed, in inequalities (29.55) and (29.56),
the left-hand and right-hand sides are equal. Observe also that even though the
coefﬁcients in the original slack form are integral, the coefﬁcients in the other
linear programs are not necessarily integral, and the intermediate solutions are not

29.3
The simplex algorithm
869
necessarily integral. Furthermore, the ﬁnal solution to a linear program need not
be integral; it is purely coincidental that this example has an integral solution.
Pivoting
We now formalize the procedure for pivoting. The procedure PIVOT takes as in-
put a slack form, given by the tuple .N; B; A; b; c; /, the index l of the leav-
ing variable xl, and the index e of the entering variable xe. It returns the tuple
. yN; yB; y
A; yb; yc; y/ describing the new slack form. (Recall again that the entries of
the m	n matrices A and y
A are actually the negatives of the coefﬁcients that appear
in the slack form.)
PIVOT.N; B; A; b; c; ; l; e/
1
// Compute the coefﬁcients of the equation for new basic variable xe.
2
let y
A be a new m 	 n matrix
3
ybe D bl=ale
4
for each j 2 N  feg
5
yaej D alj=ale
6
yael D 1=ale
7
// Compute the coefﬁcients of the remaining constraints.
8
for each i 2 B  flg
9
ybi D bi  aieybe
10
for each j 2 N  feg
11
yaij D aij  aieyaej
12
yail D aieyael
13
// Compute the objective function.
14
y D  C ceybe
15
for each j 2 N  feg
16
ycj D cj  ceyaej
17
ycl D ceyael
18
// Compute new sets of basic and nonbasic variables.
19
yN D N  feg [ flg
20
yB D B  flg [ feg
21
return . yN; yB; y
A; yb; yc; y/
PIVOT works as follows. Lines 3–6 compute the coefﬁcients in the new equation
for xe by rewriting the equation that has xl on the left-hand side to instead have xe
on the left-hand side. Lines 8–12 update the remaining equations by substituting
the right-hand side of this new equation for each occurrence of xe. Lines 14–17
do the same substitution for the objective function, and lines 19 and 20 update the

870
Chapter 29
Linear Programming
sets of nonbasic and basic variables. Line 21 returns the new slack form. As given,
if ale D 0, PIVOT would cause an error by dividing by 0, but as we shall see in the
proofs of Lemmas 29.2 and 29.12, we call PIVOT only when ale ¤ 0.
We now summarize the effect that PIVOT has on the values of the variables in
the basic solution.
Lemma 29.1
Consider a call to PIVOT.N; B; A; b; c; ; l; e/ in which ale ¤ 0. Let the values
returned from the call be . yN; yB; y
A; yb; yc; y/, and let Nx denote the basic solution after
the call. Then
1. Nxj D 0 for each j 2 yN .
2. Nxe D bl=ale.
3. Nxi D bi  aieybe for each i 2 yB  feg.
Proof
The ﬁrst statement is true because the basic solution always sets all non-
basic variables to 0. When we set each nonbasic variable to 0 in a constraint
xi D ybi 
X
j2 y
N
yaijxj ;
we have that Nxi D ybi for each i 2 yB. Since e 2 yB, line 3 of PIVOT gives
Nxe D ybe D bl=ale ;
which proves the second statement. Similarly, using line 9 for each i 2 yB  feg,
we have
Nxi D ybi D bi  aieybe ;
which proves the third statement.
The formal simplex algorithm
We are now ready to formalize the simplex algorithm, which we demonstrated by
example. That example was a particularly nice one, and we could have had several
other issues to address:

How do we determine whether a linear program is feasible?

What do we do if the linear program is feasible, but the initial basic solution is
not feasible?

How do we determine whether a linear program is unbounded?

How do we choose the entering and leaving variables?

29.3
The simplex algorithm
871
In Section 29.5, we shall show how to determine whether a problem is feasible,
and if so, how to ﬁnd a slack form in which the initial basic solution is feasible.
Therefore, let us assume that we have a procedure INITIALIZE-SIMPLEX.A; b; c/
that takes as input a linear program in standard form, that is, an m 	 n matrix
A D .aij/, an m-vector b D .bi/, and an n-vector c D .cj/. If the problem is
infeasible, the procedure returns a message that the program is infeasible and then
terminates. Otherwise, the procedure returns a slack form for which the initial
basic solution is feasible.
The procedure SIMPLEX takes as input a linear program in standard form, as just
described. It returns an n-vector Nx D . Nxj/ that is an optimal solution to the linear
program described in (29.19)–(29.21).
SIMPLEX.A; b; c/
1
.N; B; A; b; c; / D INITIALIZE-SIMPLEX.A; b; c/
2
let 
 be a new vector of length n
3
while some index j 2 N has cj > 0
4
choose an index e 2 N for which ce > 0
5
for each index i 2 B
6
if aie > 0
7

i D bi=aie
8
else 
i D 1
9
choose an index l 2 B that minimizes 
i
10
if 
l == 1
11
return “unbounded”
12
else .N; B; A; b; c; / D PIVOT.N; B; A; b; c; ; l; e/
13
for i D 1 to n
14
if i 2 B
15
Nxi D bi
16
else Nxi D 0
17
return . Nx1; Nx2; : : : ; Nxn/
The SIMPLEX procedure works as follows. In line 1, it calls the procedure
INITIALIZE-SIMPLEX.A; b; c/, described above, which either determines that the
linear program is infeasible or returns a slack form for which the basic solution is
feasible. The while loop of lines 3–12 forms the main part of the algorithm. If all
coefﬁcients in the objective function are negative, then the while loop terminates.
Otherwise, line 4 selects a variable xe, whose coefﬁcient in the objective function
is positive, as the entering variable. Although we may choose any such variable as
the entering variable, we assume that we use some prespeciﬁed deterministic rule.
Next, lines 5–9 check each constraint and pick the one that most severely limits
the amount by which we can increase xe without violating any of the nonnegativ-

872
Chapter 29
Linear Programming
ity constraints; the basic variable associated with this constraint is xl. Again, we
are free to choose one of several variables as the leaving variable, but we assume
that we use some prespeciﬁed deterministic rule. If none of the constraints lim-
its the amount by which the entering variable can increase, the algorithm returns
“unbounded” in line 11. Otherwise, line 12 exchanges the roles of the entering
and leaving variables by calling PIVOT.N; B; A; b; c; ; l; e/, as described above.
Lines 13–16 compute a solution Nx1; Nx2; : : : ; Nxn for the original linear-programming
variables by setting all the nonbasic variables to 0 and each basic variable Nxi to bi,
and line 17 returns these values.
To show that SIMPLEX is correct, we ﬁrst show that if SIMPLEX has an initial
feasible solution and eventually terminates, then it either returns a feasible solution
or determines that the linear program is unbounded. Then, we show that SIMPLEX
terminates. Finally, in Section 29.4 (Theorem 29.10) we show that the solution
returned is optimal.
Lemma 29.2
Given a linear program .A; b; c/, suppose that the call to INITIALIZE-SIMPLEX in
line 1 of SIMPLEX returns a slack form for which the basic solution is feasible.
Then if SIMPLEX returns a solution in line 17, that solution is a feasible solution to
the linear program. If SIMPLEX returns “unbounded” in line 11, the linear program
is unbounded.
Proof
We use the following three-part loop invariant:
At the start of each iteration of the while loop of lines 3–12,
1. the slack form is equivalent to the slack form returned by the call of
INITIALIZE-SIMPLEX,
2. for each i 2 B, we have bi  0, and
3. the basic solution associated with the slack form is feasible.
Initialization: The equivalence of the slack forms is trivial for the ﬁrst itera-
tion. We assume, in the statement of the lemma, that the call to INITIALIZE-
SIMPLEX in line 1 of SIMPLEX returns a slack form for which the basic solution
is feasible. Thus, the third part of the invariant is true. Because the basic so-
lution is feasible, each basic variable xi is nonnegative. Furthermore, since the
basic solution sets each basic variable xi to bi, we have that bi  0 for all
i 2 B. Thus, the second part of the invariant holds.
Maintenance: We shall show that each iteration of the while loop maintains the
loop invariant, assuming that the return statement in line 11 does not execute.
We shall handle the case in which line 11 executes when we discuss termination.

29.3
The simplex algorithm
873
An iteration of the while loop exchanges the role of a basic and a nonbasic
variable by calling the PIVOT procedure. By Exercise 29.3-3, the slack form is
equivalent to the one from the previous iteration which, by the loop invariant,
is equivalent to the initial slack form.
We now demonstrate the second part of the loop invariant. We assume that at
the start of each iteration of the while loop, bi  0 for each i 2 B, and we shall
show that these inequalities remain true after the call to PIVOT in line 12. Since
the only changes to the variables bi and the set B of basic variables occur in this
assignment, it sufﬁces to show that line 12 maintains this part of the invariant.
We let bi, aij, and B refer to values before the call of PIVOT, and ybi refer to
values returned from PIVOT.
First, we observe that ybe  0 because bl  0 by the loop invariant, ale > 0 by
lines 6 and 9 of SIMPLEX, and ybe D bl=ale by line 3 of PIVOT.
For the remaining indices i 2 B  flg, we have that
ybi
D
bi  aieybe
(by line 9 of PIVOT)
D
bi  aie.bl=ale/
(by line 3 of PIVOT) .
(29.76)
We have two cases to consider, depending on whether aie > 0 or aie  0.
If aie > 0, then since we chose l such that
bl=ale  bi=aie
for all i 2 B ;
(29.77)
we have
ybi
D
bi  aie.bl=ale/
(by equation (29.76))

bi  aie.bi=aie/
(by inequality (29.77))
D
bi  bi
D
0 ;
and thus ybi  0. If aie  0, then because ale, bi, and bl are all nonnegative,
equation (29.76) implies that ybi must be nonnegative, too.
We now argue that the basic solution is feasible, i.e., that all variables have non-
negative values. The nonbasic variables are set to 0 and thus are nonnegative.
Each basic variable xi is deﬁned by the equation
xi D bi 
X
j2N
aijxj :
The basic solution sets Nxi D bi. Using the second part of the loop invariant, we
conclude that each basic variable Nxi is nonnegative.

874
Chapter 29
Linear Programming
Termination: The while loop can terminate in one of two ways. If it terminates
because of the condition in line 3, then the current basic solution is feasible and
line 17 returns this solution. The other way it terminates is by returning “un-
bounded” in line 11. In this case, for each iteration of the for loop in lines 5–8,
when line 6 is executed, we ﬁnd that aie  0. Consider the solution Nx deﬁned as
Nxi D

1
if i D e ;
0
if i 2 N  feg ;
bi  P
j2N aij Nxj
if i 2 B :
We now show that this solution is feasible, i.e., that all variables are nonneg-
ative. The nonbasic variables other than Nxe are 0, and Nxe D 1 > 0; thus all
nonbasic variables are nonnegative. For each basic variable Nxi, we have
Nxi
D
bi 
X
j2N
aij Nxj
D
bi  aie Nxe :
The loop invariant implies that bi  0, and we have aie  0 and Nxe D 1 > 0.
Thus, Nxi  0.
Now we show that the objective value for the solution Nx is unbounded. From
equation (29.42), the objective value is
´
D
 C
X
j2N
cj Nxj
D
 C ce Nxe :
Since ce > 0 (by line 4 of SIMPLEX) and Nxe D 1, the objective value is 1,
and thus the linear program is unbounded.
It remains to show that SIMPLEX terminates, and when it does terminate, the
solution it returns is optimal. Section 29.4 will address optimality. We now discuss
termination.
Termination
In the example given in the beginning of this section, each iteration of the simplex
algorithm increased the objective value associated with the basic solution. As Ex-
ercise 29.3-2 asks you to show, no iteration of SIMPLEX can decrease the objective
value associated with the basic solution. Unfortunately, it is possible that an itera-
tion leaves the objective value unchanged. This phenomenon is called degeneracy,
and we shall now study it in greater detail.

29.3
The simplex algorithm
875
The assignment in line 14 of PIVOT, y D  C ceybe, changes the objective value.
Since SIMPLEX calls PIVOT only when ce > 0, the only way for the objective
value to remain unchanged (i.e., y D ) is for ybe to be 0. This value is assigned
as ybe D bl=ale in line 3 of PIVOT. Since we always call PIVOT with ale ¤ 0, we
see that for ybe to equal 0, and hence the objective value to be unchanged, we must
have bl D 0.
Indeed, this situation can occur. Consider the linear program
´
D
x1
C
x2
C
x3
x4
D
8

x1

x2
x5
D
x2

x3 :
Suppose that we choose x1 as the entering variable and x4 as the leaving variable.
After pivoting, we obtain
´
D
8
C
x3

x4
x1
D
8

x2

x4
x5
D
x2

x3
:
At this point, our only choice is to pivot with x3 entering and x5 leaving. Since
b5 D 0, the objective value of 8 remains unchanged after pivoting:
´
D
8
C
x2

x4

x5
x1
D
8

x2

x4
x3
D
x2

x5 :
The objective value has not changed, but our slack form has. Fortunately, if we
pivot again, with x2 entering and x1 leaving, the objective value increases (to 16),
and the simplex algorithm can continue.
Degeneracy can prevent the simplex algorithm from terminating, because it can
lead to a phenomenon known as cycling: the slack forms at two different itera-
tions of SIMPLEX are identical. Because of degeneracy, SIMPLEX could choose a
sequence of pivot operations that leave the objective value unchanged but repeat
a slack form within the sequence. Since SIMPLEX is a deterministic algorithm, if
it cycles, then it will cycle through the same series of slack forms forever, never
terminating.
Cycling is the only reason that SIMPLEX might not terminate. To show this fact,
we must ﬁrst develop some additional machinery.
At each iteration, SIMPLEX maintains A, b, c, and  in addition to the sets
N and B. Although we need to explicitly maintain A, b, c, and  in order to
implement the simplex algorithm efﬁciently, we can get by without maintaining
them. In other words, the sets of basic and nonbasic variables sufﬁce to uniquely
determine the slack form. Before proving this fact, we prove a useful algebraic
lemma.

876
Chapter 29
Linear Programming
Lemma 29.3
Let I be a set of indices. For each j 2 I, let ˛j and ˇj be real numbers, and let xj
be a real-valued variable. Let 
 be any real number. Suppose that for any settings
of the xj, we have
X
j2I
˛jxj D 
 C
X
j2I
ˇjxj :
(29.78)
Then ˛j D ˇj for each j 2 I, and 
 D 0.
Proof
Since equation (29.78) holds for any values of the xj, we can use particular
values to draw conclusions about ˛, ˇ, and 
. If we let xj D 0 for each j 2 I,
we conclude that 
 D 0. Now pick an arbitrary index j 2 I, and set xj D 1 and
xk D 0 for all k ¤ j . Then we must have ˛j D ˇj. Since we picked j as any
index in I, we conclude that ˛j D ˇj for each j 2 I.
A particular linear program has many different slack forms; recall that each slack
form has the same set of feasible and optimal solutions as the original linear pro-
gram. We now show that the slack form of a linear program is uniquely determined
by the set of basic variables. That is, given the set of basic variables, a unique slack
form (unique set of coefﬁcients and right-hand sides) is associated with those basic
variables.
Lemma 29.4
Let .A; b; c/ be a linear program in standard form. Given a set B of basic variables,
the associated slack form is uniquely determined.
Proof
Assume for the purpose of contradiction that there are two different slack
forms with the same set B of basic variables. The slack forms must also have
identical sets N D f1; 2; : : : ; n C mg  B of nonbasic variables. We write the ﬁrst
slack form as
´
D
 C
X
j2N
cjxj
(29.79)
xi
D
bi 
X
j2N
aijxj for i 2 B ;
(29.80)
and the second as
´
D
0 C
X
j2N
c0
jxj
(29.81)
xi
D
b0
i 
X
j2N
a0
ijxj for i 2 B :
(29.82)

29.3
The simplex algorithm
877
Consider the system of equations formed by subtracting each equation in
line (29.82) from the corresponding equation in line (29.80). The resulting sys-
tem is
0 D .bi  b0
i/ 
X
j2N
.aij  a0
ij/xj
for i 2 B
or, equivalently,
X
j2N
aijxj D .bi  b0
i/ C
X
j2N
a0
ijxj
for i 2 B :
Now, for each i 2 B, apply Lemma 29.3 with ˛j D aij, ˇj D a0
ij, 
 D bi b0
i, and
I D N . Since ˛i D ˇi, we have that aij D a0
ij for each j 2 N , and since 
 D 0,
we have that bi D b0
i. Thus, for the two slack forms, A and b are identical to A0
and b0. Using a similar argument, Exercise 29.3-1 shows that it must also be the
case that c D c0 and  D 0, and hence that the slack forms must be identical.
We can now show that cycling is the only possible reason that SIMPLEX might
not terminate.
Lemma 29.5
If SIMPLEX fails to terminate in at most

nCm
m

iterations, then it cycles.
Proof
By Lemma 29.4, the set B of basic variables uniquely determines a slack
form. There are n C m variables and jBj D m, and therefore, there are at most

nCm
m

ways to choose B. Thus, there are only at most

nCm
m

unique slack forms.
Therefore, if SIMPLEX runs for more than

nCm
m

iterations, it must cycle.
Cycling is theoretically possible, but extremely rare. We can prevent it by choos-
ing the entering and leaving variables somewhat more carefully. One option is to
perturb the input slightly so that it is impossible to have two solutions with the
same objective value. Another option is to break ties by always choosing the vari-
able with the smallest index, a strategy known as Bland’s rule. We omit the proof
that these strategies avoid cycling.
Lemma 29.6
If lines 4 and 9 of SIMPLEX always break ties by choosing the variable with the
smallest index, then SIMPLEX must terminate.
We conclude this section with the following lemma.

878
Chapter 29
Linear Programming
Lemma 29.7
Assuming that INITIALIZE-SIMPLEX returns a slack form for which the basic so-
lution is feasible, SIMPLEX either reports that a linear program is unbounded, or it
terminates with a feasible solution in at most

nCm
m

iterations.
Proof
Lemmas 29.2 and 29.6 show that if INITIALIZE-SIMPLEX returns a slack
form for which the basic solution is feasible, SIMPLEX either reports that a linear
program is unbounded, or it terminates with a feasible solution. By the contra-
positive of Lemma 29.5, if SIMPLEX terminates with a feasible solution, then it
terminates in at most

nCm
m

iterations.
Exercises
29.3-1
Complete the proof of Lemma 29.4 by showing that it must be the case that c D c0
and  D 0.
29.3-2
Show that the call to PIVOT in line 12 of SIMPLEX never decreases the value of .
29.3-3
Prove that the slack form given to the PIVOT procedure and the slack form that the
procedure returns are equivalent.
29.3-4
Suppose we convert a linear program .A; b; c/ in standard form to slack form.
Show that the basic solution is feasible if and only if bi  0 for i D 1; 2; : : : ; m.
29.3-5
Solve the following linear program using SIMPLEX:
maximize
18x1
C
12:5x2
subject to
x1
C
x2

20
x1

12
x2

16
x1; x2

0 :

29.4
Duality
879
29.3-6
Solve the following linear program using SIMPLEX:
maximize
5x1

3x2
subject to
x1

x2

1
2x1
C
x2

2
x1; x2

0 :
29.3-7
Solve the following linear program using SIMPLEX:
minimize
x1
C
x2
C
x3
subject to
2x1
C
7:5x2
C
3x3

10000
20x1
C
5x2
C
10x3

30000
x1; x2; x3

0 :
29.3-8
In the proof of Lemma 29.5, we argued that there are at most

mCn
n

ways to choose
a set B of basic variables. Give an example of a linear program in which there are
strictly fewer than

mCn
n

ways to choose the set B.
29.4
Duality
We have proven that, under certain assumptions, SIMPLEX terminates. We have not
yet shown that it actually ﬁnds an optimal solution to a linear program, however.
In order to do so, we introduce a powerful concept called linear-programming
duality.
Duality enables us to prove that a solution is indeed optimal. We saw an exam-
ple of duality in Chapter 26 with Theorem 26.6, the max-ﬂow min-cut theorem.
Suppose that, given an instance of a maximum-ﬂow problem, we ﬁnd a ﬂow f
with value jf j. How do we know whether f is a maximum ﬂow? By the max-ﬂow
min-cut theorem, if we can ﬁnd a cut whose value is also jf j, then we have ver-
iﬁed that f is indeed a maximum ﬂow. This relationship provides an example of
duality: given a maximization problem, we deﬁne a related minimization problem
such that the two problems have the same optimal objective values.
Given a linear program in which the objective is to maximize, we shall describe
how to formulate a dual linear program in which the objective is to minimize and

880
Chapter 29
Linear Programming
whose optimal value is identical to that of the original linear program. When refer-
ring to dual linear programs, we call the original linear program the primal.
Given a primal linear program in standard form, as in (29.16)–(29.18), we deﬁne
the dual linear program as
minimize
m
X
iD1
biyi
(29.83)
subject to
m
X
iD1
aijyi

cj
for j D 1; 2; : : : ; n ;
(29.84)
yi

0
for i D 1; 2; : : : ; m :
(29.85)
To form the dual, we change the maximization to a minimization, exchange the
roles of coefﬁcients on the right-hand sides and the objective function, and replace
each less-than-or-equal-to by a greater-than-or-equal-to. Each of the m constraints
in the primal has an associated variable yi in the dual, and each of the n constraints
in the dual has an associated variable xj in the primal. For example, consider the
linear program given in (29.53)–(29.57). The dual of this linear program is
minimize
30y1
C
24y2
C
36y3
(29.86)
subject to
y1
C
2y2
C
4y3

3
(29.87)
y1
C
2y2
C
y3

1
(29.88)
3y1
C
5y2
C
2y3

2
(29.89)
y1; y2; y3

0 :
(29.90)
We shall show in Theorem 29.10 that the optimal value of the dual linear pro-
gram is always equal to the optimal value of the primal linear program. Further-
more, the simplex algorithm actually implicitly solves both the primal and the dual
linear programs simultaneously, thereby providing a proof of optimality.
We begin by demonstrating weak duality, which states that any feasible solu-
tion to the primal linear program has a value no greater than that of any feasible
solution to the dual linear program.
Lemma 29.8 (Weak linear-programming duality)
Let Nx be any feasible solution to the primal linear program in (29.16)–(29.18) and
let Ny be any feasible solution to the dual linear program in (29.83)–(29.85). Then,
we have
n
X
jD1
cj Nxj 
m
X
iD1
bi Nyi :

29.4
Duality
881
Proof
We have
n
X
jD1
cj Nxj

n
X
jD1
 m
X
iD1
aij Nyi
!
Nxj
(by inequalities (29.84))
D
m
X
iD1
 n
X
jD1
aij Nxj
!
Nyi

m
X
iD1
bi Nyi
(by inequalities (29.17)) .
Corollary 29.9
Let Nx be a feasible solution to a primal linear program .A; b; c/, and let Ny be a
feasible solution to the corresponding dual linear program. If
n
X
jD1
cj Nxj D
m
X
iD1
bi Nyi ;
then Nx and Ny are optimal solutions to the primal and dual linear programs, respec-
tively.
Proof
By Lemma 29.8, the objective value of a feasible solution to the primal
cannot exceed that of a feasible solution to the dual. The primal linear program is
a maximization problem and the dual is a minimization problem. Thus, if feasible
solutions Nx and Ny have the same objective value, neither can be improved.
Before proving that there always is a dual solution whose value is equal to that
of an optimal primal solution, we describe how to ﬁnd such a solution. When
we ran the simplex algorithm on the linear program in (29.53)–(29.57), the ﬁnal
iteration yielded the slack form (29.72)–(29.75) with objective ´ D 28  x3=6 
x5=62x6=3, B D f1; 2; 4g, and N D f3; 5; 6g. As we shall show below, the basic
solution associated with the ﬁnal slack form is indeed an optimal solution to the
linear program; an optimal solution to linear program (29.53)–(29.57) is therefore
. Nx1; Nx2; Nx3/ D .8; 4; 0/, with objective value .3  8/ C .1  4/ C .2  0/ D 28. As
we also show below, we can read off an optimal dual solution: the negatives of the
coefﬁcients of the primal objective function are the values of the dual variables.
More precisely, suppose that the last slack form of the primal is
´
D
0 C
X
j2N
c0
jxj
xi
D
b0
i 
X
j2N
a0
ijxj
for i 2 B :

882
Chapter 29
Linear Programming
Then, to produce an optimal dual solution, we set
Nyi D
(
c0
nCi
if .n C i/ 2 N ;
0
otherwise :
(29.91)
Thus, an optimal solution to the dual linear program deﬁned in (29.86)–(29.90)
is Ny1 D 0 (since n C 1 D 4 2 B), Ny2 D c0
5 D 1=6, and Ny3 D c0
6 D 2=3.
Evaluating the dual objective function (29.86), we obtain an objective value of
.30  0/ C .24  .1=6// C .36  .2=3// D 28, which conﬁrms that the objective value
of the primal is indeed equal to the objective value of the dual. Combining these
calculations with Lemma 29.8 yields a proof that the optimal objective value of the
primal linear program is 28. We now show that this approach applies in general:
we can ﬁnd an optimal solution to the dual and simultaneously prove that a solution
to the primal is optimal.
Theorem 29.10 (Linear-programming duality)
Suppose that SIMPLEX returns values Nx D . Nx1; Nx2; : : : ; Nxn/ for the primal lin-
ear program .A; b; c/. Let N and B denote the nonbasic and basic variables for
the ﬁnal slack form, let c0 denote the coefﬁcients in the ﬁnal slack form, and let
Ny D . Ny1; Ny2; : : : ; Nym/ be deﬁned by equation (29.91). Then Nx is an optimal so-
lution to the primal linear program, Ny is an optimal solution to the dual linear
program, and
n
X
jD1
cj Nxj D
m
X
iD1
bi Nyi :
(29.92)
Proof
By Corollary 29.9, if we can ﬁnd feasible solutions Nx and Ny that satisfy
equation (29.92), then Nx and Ny must be optimal primal and dual solutions. We
shall now show that the solutions Nx and Ny described in the statement of the theorem
satisfy equation (29.92).
Suppose that we run SIMPLEX on a primal linear program, as given in lines
(29.16)–(29.18). The algorithm proceeds through a series of slack forms until it
terminates with a ﬁnal slack form with objective function
´ D 0 C
X
j2N
c0
jxj :
(29.93)
Since SIMPLEX terminated with a solution, by the condition in line 3 we know that
c0
j  0 for all j 2 N :
(29.94)

29.4
Duality
883
If we deﬁne
c0
j D 0 for all j 2 B ;
(29.95)
we can rewrite equation (29.93) as
´ D 0 C
X
j2N
c0
jxj
D 0 C
X
j2N
c0
jxj C
X
j2B
c0
jxj (because c0
j D 0 if j 2 B)
D 0 C
nCm
X
jD1
c0
jxj
(because N [ B D f1; 2; : : : ; n C mg) .
(29.96)
For the basic solution Nx associated with this ﬁnal slack form, Nxj D 0 for all j 2 N,
and ´ D 0. Since all slack forms are equivalent, if we evaluate the original objec-
tive function on Nx, we must obtain the same objective value:
n
X
jD1
cj Nxj
D
0 C
nCm
X
jD1
c0
j Nxj
(29.97)
D
0 C
X
j2N
c0
j Nxj C
X
j2B
c0
j Nxj
D
0 C
X
j2N
.c0
j  0/ C
X
j2B
.0  Nxj/
(29.98)
D
0 :
We shall now show that Ny, deﬁned by equation (29.91), is feasible for the dual
linear program and that its objective value Pm
iD1 bi Nyi equals Pn
jD1 cj Nxj. Equa-
tion (29.97) says that the ﬁrst and last slack forms, evaluated at Nx, are equal. More
generally, the equivalence of all slack forms implies that for any set of values
x D .x1; x2; : : : ; xn/, we have
n
X
jD1
cjxj D 0 C
nCm
X
jD1
c0
jxj :
Therefore, for any particular set of values Nx D . Nx1; Nx2; : : : ; Nxn/, we have

884
Chapter 29
Linear Programming
n
X
jD1
cj Nxj
D
0 C
nCm
X
jD1
c0
j Nxj
D
0 C
n
X
jD1
c0
j Nxj C
nCm
X
jDnC1
c0
j Nxj
D
0 C
n
X
jD1
c0
j Nxj C
m
X
iD1
c0
nCi NxnCi
D
0 C
n
X
jD1
c0
j Nxj C
m
X
iD1
. Nyi/ NxnCi
(by equations (29.91) and (29.95))
D
0 C
n
X
jD1
c0
j Nxj C
m
X
iD1
. Nyi/
 
bi 
n
X
jD1
aij Nxj
!
(by equation (29.32))
D
0 C
n
X
jD1
c0
j Nxj 
m
X
iD1
bi Nyi C
m
X
iD1
n
X
jD1
.aij Nxj/ Nyi
D
0 C
n
X
jD1
c0
j Nxj 
m
X
iD1
bi Nyi C
n
X
jD1
m
X
iD1
.aij Nyi/ Nxj
D
 
0 
m
X
iD1
bi Nyi
!
C
n
X
jD1
 
c0
j C
m
X
iD1
aij Nyi
!
Nxj ;
so that
n
X
jD1
cj Nxj D
 
0 
m
X
iD1
bi Nyi
!
C
n
X
jD1
 
c0
j C
m
X
iD1
aij Nyi
!
Nxj :
(29.99)
Applying Lemma 29.3 to equation (29.99), we obtain
0 
m
X
iD1
bi Nyi
D
0 ;
(29.100)
c0
j C
m
X
iD1
aij Nyi
D
cj
for j D 1; 2; : : : ; n :
(29.101)
By equation (29.100), we have that Pm
iD1 bi Nyi D 0, and hence the objective value
of the dual
Pm
iD1 bi Nyi

is equal to that of the primal (0). It remains to show

29.4
Duality
885
that the solution Ny is feasible for the dual problem. From inequalities (29.94) and
equations (29.95), we have that c0
j  0 for all j D 1; 2; : : : ; n C m. Hence, for any
j D 1; 2; : : : ; n, equations (29.101) imply that
cj
D
c0
j C
m
X
iD1
aij Nyi

m
X
iD1
aij Nyi ;
which satisﬁes the constraints (29.84) of the dual. Finally, since c0
j  0 for each
j 2 N [B, when we set Ny according to equation (29.91), we have that each Nyi  0,
and so the nonnegativity constraints are satisﬁed as well.
We have shown that, given a feasible linear program, if INITIALIZE-SIMPLEX
returns a feasible solution, and if SIMPLEX terminates without returning “un-
bounded,” then the solution returned is indeed an optimal solution. We have also
shown how to construct an optimal solution to the dual linear program.
Exercises
29.4-1
Formulate the dual of the linear program given in Exercise 29.3-5.
29.4-2
Suppose that we have a linear program that is not in standard form. We could
produce the dual by ﬁrst converting it to standard form, and then taking the dual.
It would be more convenient, however, to be able to produce the dual directly.
Explain how we can directly take the dual of an arbitrary linear program.
29.4-3
Write down the dual of the maximum-ﬂow linear program, as given in lines
(29.47)–(29.50) on page 860.
Explain how to interpret this formulation as a
minimum-cut problem.
29.4-4
Write down the dual of the minimum-cost-ﬂow linear program, as given in lines
(29.51)–(29.52) on page 862. Explain how to interpret this problem in terms of
graphs and ﬂows.
29.4-5
Show that the dual of the dual of a linear program is the primal linear program.

886
Chapter 29
Linear Programming
29.4-6
Which result from Chapter 26 can be interpreted as weak duality for the maximum-
ﬂow problem?
29.5
The initial basic feasible solution
In this section, we ﬁrst describe how to test whether a linear program is feasible,
and if it is, how to produce a slack form for which the basic solution is feasible.
We conclude by proving the fundamental theorem of linear programming, which
says that the SIMPLEX procedure always produces the correct result.
Finding an initial solution
In Section 29.3, we assumed that we had a procedure INITIALIZE-SIMPLEX that
determines whether a linear program has any feasible solutions, and if it does, gives
a slack form for which the basic solution is feasible. We describe this procedure
here.
A linear program can be feasible, yet the initial basic solution might not be
feasible. Consider, for example, the following linear program:
maximize
2x1

x2
(29.102)
subject to
2x1

x2

2
(29.103)
x1

5x2

4
(29.104)
x1; x2

0 :
(29.105)
If we were to convert this linear program to slack form, the basic solution would
set x1 D 0 and x2 D 0. This solution violates constraint (29.104), and so it is not a
feasible solution. Thus, INITIALIZE-SIMPLEX cannot just return the obvious slack
form. In order to determine whether a linear program has any feasible solutions,
we will formulate an auxiliary linear program. For this auxiliary linear program,
we can ﬁnd (with a little work) a slack form for which the basic solution is feasible.
Furthermore, the solution of this auxiliary linear program determines whether the
initial linear program is feasible and if so, it provides a feasible solution with which
we can initialize SIMPLEX.
Lemma 29.11
Let L be a linear program in standard form, given as in (29.16)–(29.18). Let x0 be
a new variable, and let Laux be the following linear program with n C 1 variables:

29.5
The initial basic feasible solution
887
maximize
x0
(29.106)
subject to
n
X
jD1
aijxj  x0

bi
for i D 1; 2; : : : ; m ;
(29.107)
xj

0
for j D 0; 1; : : : ; n :
(29.108)
Then L is feasible if and only if the optimal objective value of Laux is 0.
Proof
Suppose that L has a feasible solution Nx D . Nx1; Nx2; : : : ; Nxn/. Then the
solution Nx0 D 0 combined with Nx is a feasible solution to Laux with objective
value 0. Since x0  0 is a constraint of Laux and the objective function is to
maximize x0, this solution must be optimal for Laux.
Conversely, suppose that the optimal objective value of Laux is 0. Then Nx0 D 0,
and the remaining solution values of Nx satisfy the constraints of L.
We now describe our strategy to ﬁnd an initial basic feasible solution for a linear
program L in standard form:
INITIALIZE-SIMPLEX.A; b; c/
1
let k be the index of the minimum bi
2
if bk  0
// is the initial basic solution feasible?
3
return .f1; 2; : : : ; ng ; fn C 1; n C 2; : : : ; n C mg ; A; b; c; 0/
4
form Laux by adding x0 to the left-hand side of each constraint
and setting the objective function to x0
5
let .N; B; A; b; c; / be the resulting slack form for Laux
6
l D n C k
7
// Laux has n C 1 nonbasic variables and m basic variables.
8
.N; B; A; b; c; / D PIVOT.N; B; A; b; c; ; l; 0/
9
// The basic solution is now feasible for Laux.
10
iterate the while loop of lines 3–12 of SIMPLEX until an optimal solution
to Laux is found
11
if the optimal solution to Laux sets Nx0 to 0
12
if Nx0 is basic
13
perform one (degenerate) pivot to make it nonbasic
14
from the ﬁnal slack form of Laux, remove x0 from the constraints and
restore the original objective function of L, but replace each basic
variable in this objective function by the right-hand side of its
associated constraint
15
return the modiﬁed ﬁnal slack form
16
else return “infeasible”

888
Chapter 29
Linear Programming
INITIALIZE-SIMPLEX works as follows. In lines 1–3, we implicitly test the
basic solution to the initial slack form for L given by N D f1; 2; : : : ; ng, B D
fn C 1; n C 2; : : : ; n C mg, Nxi D bi for all i 2 B, and Nxj D 0 for all j 2 N .
(Creating the slack form requires no explicit effort, as the values of A, b, and c are
the same in both slack and standard forms.) If line 2 ﬁnds this basic solution to be
feasible—that is, Nxi  0 for all i 2 N [ B—then line 3 returns the slack form.
Otherwise, in line 4, we form the auxiliary linear program Laux as in Lemma 29.11.
Since the initial basic solution to L is not feasible, the initial basic solution to the
slack form for Laux cannot be feasible either. To ﬁnd a basic feasible solution, we
perform a single pivot operation. Line 6 selects l D n C k as the index of the
basic variable that will be the leaving variable in the upcoming pivot operation.
Since the basic variables are xnC1; xnC2; : : : ; xnCm, the leaving variable xl will be
the one with the most negative value. Line 8 performs that call of PIVOT, with
x0 entering and xl leaving. We shall see shortly that the basic solution resulting
from this call of PIVOT will be feasible. Now that we have a slack form for which
the basic solution is feasible, we can, in line 10, repeatedly call PIVOT to fully
solve the auxiliary linear program. As the test in line 11 demonstrates, if we ﬁnd
an optimal solution to Laux with objective value 0, then in lines 12–14, we create
a slack form for L for which the basic solution is feasible. To do so, we ﬁrst,
in lines 12–13, handle the degenerate case in which x0 may still be basic with
value Nx0 D 0. In this case, we perform a pivot step to remove x0 from the basis,
using any e 2 N such that a0e ¤ 0 as the entering variable. The new basic
solution remains feasible; the degenerate pivot does not change the value of any
variable. Next we delete all x0 terms from the constraints and restore the original
objective function for L. The original objective function may contain both basic
and nonbasic variables. Therefore, in the objective function we replace each basic
variable by the right-hand side of its associated constraint. Line 15 then returns
this modiﬁed slack form. If, on the other hand, line 11 discovers that the original
linear program L is infeasible, then line 16 returns this information.
We now demonstrate the operation of INITIALIZE-SIMPLEX on the linear pro-
gram (29.102)–(29.105). This linear program is feasible if we can ﬁnd nonneg-
ative values for x1 and x2 that satisfy inequalities (29.103) and (29.104). Using
Lemma 29.11, we formulate the auxiliary linear program
maximize
x0
(29.109)
subject to
2x1

x2

x0

2
(29.110)
x1

5x2

x0

4
(29.111)
x1; x2; x0

0 :
By Lemma 29.11, if the optimal objective value of this auxiliary linear program
is 0, then the original linear program has a feasible solution. If the optimal objective

29.5
The initial basic feasible solution
889
value of this auxiliary linear program is negative, then the original linear program
does not have a feasible solution.
We write this linear program in slack form, obtaining
´
D

x0
x3
D
2

2x1
C
x2
C
x0
x4
D
4

x1
C
5x2
C
x0 :
We are not out of the woods yet, because the basic solution, which would set
x4 D 4, is not feasible for this auxiliary linear program. We can, however, with
one call to PIVOT, convert this slack form into one in which the basic solution is
feasible. As line 8 indicates, we choose x0 to be the entering variable. In line 6, we
choose as the leaving variable x4, which is the basic variable whose value in the
basic solution is most negative. After pivoting, we have the slack form
´
D
4

x1
C
5x2

x4
x0
D
4
C
x1

5x2
C
x4
x3
D
6

x1

4x2
C
x4 :
The associated basic solution is . Nx0; Nx1; Nx2; Nx3; Nx4/ D .4; 0; 0; 6; 0/, which is feasi-
ble. We now repeatedly call PIVOT until we obtain an optimal solution to Laux. In
this case, one call to PIVOT with x2 entering and x0 leaving yields
´
D

x0
x2
D
4
5

x0
5
C
x1
5
C
x4
5
x3
D
14
5
C
4x0
5

9x1
5
C
x4
5
:
This slack form is the ﬁnal solution to the auxiliary problem. Since this solution
has x0 D 0, we know that our initial problem was feasible. Furthermore, since
x0 D 0, we can just remove it from the set of constraints. We then restore the
original objective function, with appropriate substitutions made to include only
nonbasic variables. In our example, we get the objective function
2x1  x2 D 2x1 
4
5  x0
5 C x1
5 C x4
5

:
Setting x0 D 0 and simplifying, we get the objective function
4
5 C 9x1
5
 x4
5 ;
and the slack form

890
Chapter 29
Linear Programming
´
D
4
5
C
9x1
5

x4
5
x2
D
4
5
C
x1
5
C
x4
5
x3
D
14
5

9x1
5
C
x4
5
:
This slack form has a feasible basic solution, and we can return it to procedure
SIMPLEX.
We now formally show the correctness of INITIALIZE-SIMPLEX.
Lemma 29.12
If a linear program L has no feasible solution, then INITIALIZE-SIMPLEX returns
“infeasible.” Otherwise, it returns a valid slack form for which the basic solution
is feasible.
Proof
First suppose that the linear program L has no feasible solution. Then by
Lemma 29.11, the optimal objective value of Laux, deﬁned in (29.106)–(29.108),
is nonzero, and by the nonnegativity constraint on x0, the optimal objective value
must be negative. Furthermore, this objective value must be ﬁnite, since setting
xi D 0, for i D 1; 2; : : : ; n, and x0 D jminm
iD1 fbigj is feasible, and this solution
has objective value  jminm
iD1 fbigj. Therefore, line 10 of INITIALIZE-SIMPLEX
ﬁnds a solution with a nonpositive objective value. Let Nx be the basic solution
associated with the ﬁnal slack form. We cannot have Nx0 D 0, because then Laux
would have objective value 0, which contradicts that the objective value is negative.
Thus the test in line 11 results in line 16 returning “infeasible.”
Suppose now that the linear program L does have a feasible solution. From
Exercise 29.3-4, we know that if bi  0 for i D 1; 2; : : : ; m, then the basic solution
associated with the initial slack form is feasible. In this case, lines 2–3 return the
slack form associated with the input. (Converting the standard form to slack form
is easy, since A, b, and c are the same in both.)
In the remainder of the proof, we handle the case in which the linear program is
feasible but we do not return in line 3. We argue that in this case, lines 4–10 ﬁnd a
feasible solution to Laux with objective value 0. First, by lines 1–2, we must have
bk < 0 ;
and
bk  bi
for each i 2 B :
(29.112)
In line 8, we perform one pivot operation in which the leaving variable xl (recall
that l D n C k, so that bl < 0) is the left-hand side of the equation with mini-
mum bi, and the entering variable is x0, the extra added variable. We now show

29.5
The initial basic feasible solution
891
that after this pivot, all entries of b are nonnegative, and hence the basic solution
to Laux is feasible. Letting Nx be the basic solution after the call to PIVOT, and
letting yb and yB be values returned by PIVOT, Lemma 29.1 implies that
Nxi D
(
bi  aieybe
if i 2 yB  feg ;
bl=ale
if i D e :
(29.113)
The call to PIVOT in line 8 has e D 0. If we rewrite inequalities (29.107), to
include coefﬁcients ai0,
n
X
jD0
aijxj  bi
for i D 1; 2; : : : ; m ;
(29.114)
then
ai0 D aie D 1 for each i 2 B :
(29.115)
(Note that ai0 is the coefﬁcient of x0 as it appears in inequalities (29.114), not
the negation of the coefﬁcient, because Laux is in standard rather than slack form.)
Since l 2 B, we also have that ale D 1. Thus, bl=ale > 0, and so Nxe > 0. For
the remaining basic variables, we have
Nxi
D
bi  aieybe
(by equation (29.113))
D
bi  aie.bl=ale/
(by line 3 of PIVOT)
D
bi  bl
(by equation (29.115) and ale D 1)

0
(by inequality (29.112)) ,
which implies that each basic variable is now nonnegative. Hence the basic solu-
tion after the call to PIVOT in line 8 is feasible. We next execute line 10, which
solves Laux. Since we have assumed that L has a feasible solution, Lemma 29.11
implies that Laux has an optimal solution with objective value 0. Since all the slack
forms are equivalent, the ﬁnal basic solution to Laux must have Nx0 D 0, and after
removing x0 from the linear program, we obtain a slack form that is feasible for L.
Line 15 then returns this slack form.
Fundamental theorem of linear programming
We conclude this chapter by showing that the SIMPLEX procedure works. In par-
ticular, any linear program either is infeasible, is unbounded, or has an optimal
solution with a ﬁnite objective value. In each case, SIMPLEX acts appropriately.

892
Chapter 29
Linear Programming
Theorem 29.13 (Fundamental theorem of linear programming)
Any linear program L, given in standard form, either
1. has an optimal solution with a ﬁnite objective value,
2. is infeasible, or
3. is unbounded.
If L is infeasible, SIMPLEX returns “infeasible.” If L is unbounded, SIMPLEX
returns “unbounded.” Otherwise, SIMPLEX returns an optimal solution with a ﬁnite
objective value.
Proof
By Lemma 29.12, if linear program L is infeasible, then SIMPLEX returns
“infeasible.” Now suppose that the linear program L is feasible. By Lemma 29.12,
INITIALIZE-SIMPLEX returns a slack form for which the basic solution is feasible.
By Lemma 29.7, therefore, SIMPLEX either returns “unbounded” or terminates
with a feasible solution. If it terminates with a ﬁnite solution, then Theorem 29.10
tells us that this solution is optimal. On the other hand, if SIMPLEX returns “un-
bounded,” Lemma 29.2 tells us the linear program L is indeed unbounded. Since
SIMPLEX always terminates in one of these ways, the proof is complete.
Exercises
29.5-1
Give detailed pseudocode to implement lines 5 and 14 of INITIALIZE-SIMPLEX.
29.5-2
Show that when the main loop of SIMPLEX is run by INITIALIZE-SIMPLEX, it can
never return “unbounded.”
29.5-3
Suppose that we are given a linear program L in standard form, and suppose that
for both L and the dual of L, the basic solutions associated with the initial slack
forms are feasible. Show that the optimal objective value of L is 0.
29.5-4
Suppose that we allow strict inequalities in a linear program. Show that in this
case, the fundamental theorem of linear programming does not hold.

29.5
The initial basic feasible solution
893
29.5-5
Solve the following linear program using SIMPLEX:
maximize
x1
C
3x2
subject to
x1

x2

8
x1

x2

3
x1
C
4x2

2
x1; x2

0 :
29.5-6
Solve the following linear program using SIMPLEX:
maximize
x1

2x2
subject to
x1
C
2x2

4
2x1

6x2

12
x2

1
x1; x2

0 :
29.5-7
Solve the following linear program using SIMPLEX:
maximize
x1
C
3x2
subject to
x1
C
x2

1
x1

x2

3
x1
C
4x2

2
x1; x2

0 :
29.5-8
Solve the linear program given in (29.6)–(29.10).
29.5-9
Consider the following 1-variable linear program, which we call P :
maximize
tx
subject to
rx

s
x

0 ;
where r, s, and t are arbitrary real numbers. Let D be the dual of P .

894
Chapter 29
Linear Programming
State for which values of r, s, and t you can assert that
1. Both P and D have optimal solutions with ﬁnite objective values.
2. P is feasible, but D is infeasible.
3. D is feasible, but P is infeasible.
4. Neither P nor D is feasible.
Problems
29-1
Linear-inequality feasibility
Given a set of m linear inequalities on n variables x1; x2; : : : ; xn, the linear-
inequality feasibility problem asks whether there is a setting of the variables that
simultaneously satisﬁes each of the inequalities.
a. Show that if we have an algorithm for linear programming, we can use it to
solve a linear-inequality feasibility problem. The number of variables and con-
straints that you use in the linear-programming problem should be polynomial
in n and m.
b. Show that if we have an algorithm for the linear-inequality feasibility problem,
we can use it to solve a linear-programming problem. The number of variables
and linear inequalities that you use in the linear-inequality feasibility problem
should be polynomial in n and m, the number of variables and constraints in
the linear program.
29-2
Complementary slackness
Complementary slackness describes a relationship between the values of primal
variables and dual constraints and between the values of dual variables and pri-
mal constraints. Let Nx be a feasible solution to the primal linear program given
in (29.16)–(29.18), and let Ny be a feasible solution to the dual linear program given
in (29.83)–(29.85). Complementary slackness states that the following conditions
are necessary and sufﬁcient for Nx and Ny to be optimal:
m
X
iD1
aij Nyi D cj or Nxj D 0
for j D 1; 2; : : : ; n
and
n
X
jD1
aij Nxj D bi or Nyi D 0
for i D 1; 2; : : : ; m :

Problems for Chapter 29
895
a. Verify that complementary slackness holds for the linear program in lines
(29.53)–(29.57).
b. Prove that complementary slackness holds for any primal linear program and
its corresponding dual.
c. Prove that a feasible solution Nx to a primal linear program given in lines
(29.16)–(29.18) is optimal if and only if there exist values Ny D . Ny1; Ny2; : : : ; Nym/
such that
1. Ny is a feasible solution to the dual linear program given in (29.83)–(29.85),
2. Pm
iD1 aij Nyi D cj for all j such that Nxj > 0, and
3. Nyi D 0 for all i such that Pn
jD1 aij Nxj < bi.
29-3
Integer linear programming
An integer linear-programming problem is a linear-programming problem with
the additional constraint that the variables x must take on integral values. Exer-
cise 34.5-3 shows that just determining whether an integer linear program has a
feasible solution is NP-hard, which means that there is no known polynomial-time
algorithm for this problem.
a. Show that weak duality (Lemma 29.8) holds for an integer linear program.
b. Show that duality (Theorem 29.10) does not always hold for an integer linear
program.
c. Given a primal linear program in standard form, let us deﬁne P to be the opti-
mal objective value for the primal linear program, D to be the optimal objective
value for its dual, IP to be the optimal objective value for the integer version of
the primal (that is, the primal with the added constraint that the variables take
on integer values), and ID to be the optimal objective value for the integer ver-
sion of the dual. Assuming that both the primal integer program and the dual
integer program are feasible and bounded, show that
IP  P D D  ID :
29-4
Farkas’s lemma
Let A be an m 	 n matrix and c be an n-vector. Then Farkas’s lemma states that
exactly one of the systems

896
Chapter 29
Linear Programming
Ax

0 ;
cTx
>
0
and
ATy
D
c ;
y

0
is solvable, where x is an n-vector and y is an m-vector. Prove Farkas’s lemma.
29-5
Minimum-cost circulation
In this problem, we consider a variant of the minimum-cost-ﬂow problem from
Section 29.2 in which we are not given a demand, a source, or a sink. Instead,
we are given, as before, a ﬂow network and edge costs a.u; /. A ﬂow is feasible
if it satisﬁes the capacity constraint on every edge and ﬂow conservation at every
vertex. The goal is to ﬁnd, among all feasible ﬂows, the one of minimum cost. We
call this problem the minimum-cost-circulation problem.
a. Formulate the minimum-cost-circulation problem as a linear program.
b. Suppose that for all edges .u; / 2 E, we have a.u; / > 0. Characterize an
optimal solution to the minimum-cost-circulation problem.
c. Formulate the maximum-ﬂow problem as a minimum-cost-circulation problem
linear program. That is given a maximum-ﬂow problem instance G D .V; E/
with source s, sink t and edge capacities c, create a minimum-cost-circulation
problem by giving a (possibly different) network G0 D .V 0; E0/ with edge
capacities c0 and edge costs a0 such that you can discern a solution to the
maximum-ﬂow problem from a solution to the minimum-cost-circulation prob-
lem.
d. Formulate the single-source shortest-path problem as a minimum-cost-circu-
lation problem linear program.
Chapter notes
This chapter only begins to study the wide ﬁeld of linear programming. A num-
ber of books are devoted exclusively to linear programming, including those by
Chv´atal [69], Gass [130], Karloff [197], Schrijver [303], and Vanderbei [344].
Many other books give a good coverage of linear programming, including those
by Papadimitriou and Steiglitz [271] and Ahuja, Magnanti, and Orlin [7]. The
coverage in this chapter draws on the approach taken by Chv´atal.

Notes for Chapter 29
897
The simplex algorithm for linear programming was invented by G. Dantzig
in 1947. Shortly after, researchers discovered how to formulate a number of prob-
lems in a variety of ﬁelds as linear programs and solve them with the simplex
algorithm. As a result, applications of linear programming ﬂourished, along with
several algorithms. Variants of the simplex algorithm remain the most popular
methods for solving linear-programming problems. This history appears in a num-
ber of places, including the notes in [69] and [197].
The ellipsoid algorithm was the ﬁrst polynomial-time algorithm for linear pro-
gramming and is due to L. G. Khachian in 1979; it was based on earlier work by
N. Z. Shor, D. B. Judin, and A. S. Nemirovskii. Gr¨otschel, Lov´asz, and Schrijver
[154] describe how to use the ellipsoid algorithm to solve a variety of problems in
combinatorial optimization. To date, the ellipsoid algorithm does not appear to be
competitive with the simplex algorithm in practice.
Karmarkar’s paper [198] includes a description of the ﬁrst interior-point algo-
rithm. Many subsequent researchers designed interior-point algorithms. Good sur-
veys appear in the article of Goldfarb and Todd [141] and the book by Ye [361].
Analysis of the simplex algorithm remains an active area of research. V. Klee
and G. J. Minty constructed an example on which the simplex algorithm runs
through 2n  1 iterations. The simplex algorithm usually performs very well in
practice and many researchers have tried to give theoretical justiﬁcation for this
empirical observation. A line of research begun by K. H. Borgwardt, and carried
on by many others, shows that under certain probabilistic assumptions on the in-
put, the simplex algorithm converges in expected polynomial time. Spielman and
Teng [322] made progress in this area, introducing the “smoothed analysis of algo-
rithms” and applying it to the simplex algorithm.
The simplex algorithm is known to run efﬁciently in certain special cases. Par-
ticularly noteworthy is the network-simplex algorithm, which is the simplex al-
gorithm, specialized to network-ﬂow problems. For certain network problems,
including the shortest-paths, maximum-ﬂow, and minimum-cost-ﬂow problems,
variants of the network-simplex algorithm run in polynomial time. See, for exam-
ple, the article by Orlin [268] and the citations therein.
