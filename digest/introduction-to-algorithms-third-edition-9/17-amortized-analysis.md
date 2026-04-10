# 17 Amortized Analysis

17
Amortized Analysis
In an amortized analysis, we average the time required to perform a sequence of
data-structure operations over all the operations performed. With amortized analy-
sis, we can show that the average cost of an operation is small, if we average over a
sequence of operations, even though a single operation within the sequence might
be expensive. Amortized analysis differs from average-case analysis in that prob-
ability is not involved; an amortized analysis guarantees the average performance
of each operation in the worst case.
The ﬁrst three sections of this chapter cover the three most common techniques
used in amortized analysis. Section 17.1 starts with aggregate analysis, in which
we determine an upper bound T .n/ on the total cost of a sequence of n operations.
The average cost per operation is then T .n/=n. We take the average cost as the
amortized cost of each operation, so that all operations have the same amortized
cost.
Section 17.2 covers the accounting method, in which we determine an amortized
cost of each operation. When there is more than one type of operation, each type of
operation may have a different amortized cost. The accounting method overcharges
some operations early in the sequence, storing the overcharge as “prepaid credit”
on speciﬁc objects in the data structure. Later in the sequence, the credit pays for
operations that are charged less than they actually cost.
Section 17.3 discusses the potential method, which is like the accounting method
in that we determine the amortized cost of each operation and may overcharge op-
erations early on to compensate for undercharges later. The potential method main-
tains the credit as the “potential energy” of the data structure as a whole instead of
associating the credit with individual objects within the data structure.
We shall use two examples to examine these three methods. One is a stack
with the additional operation MULTIPOP, which pops several objects at once. The
other is a binary counter that counts up from 0 by means of the single operation
INCREMENT.

452
Chapter 17
Amortized Analysis
While reading this chapter, bear in mind that the charges assigned during an
amortized analysis are for analysis purposes only. They need not—and should
not—appear in the code. If, for example, we assign a credit to an object x when
using the accounting method, we have no need to assign an appropriate amount to
some attribute, such as x:credit, in the code.
When we perform an amortized analysis, we often gain insight into a particular
data structure, and this insight can help us optimize the design. In Section 17.4,
for example, we shall use the potential method to analyze a dynamically expanding
and contracting table.
17.1
Aggregate analysis
In aggregate analysis, we show that for all n, a sequence of n operations takes
worst-case time T .n/ in total. In the worst case, the average cost, or amortized
cost, per operation is therefore T .n/=n. Note that this amortized cost applies to
each operation, even when there are several types of operations in the sequence.
The other two methods we shall study in this chapter, the accounting method and
the potential method, may assign different amortized costs to different types of
operations.
Stack operations
In our ﬁrst example of aggregate analysis, we analyze stacks that have been aug-
mented with a new operation. Section 10.1 presented the two fundamental stack
operations, each of which takes O.1/ time:
PUSH.S; x/ pushes object x onto stack S.
POP.S/ pops the top of stack S and returns the popped object. Calling POP on an
empty stack generates an error.
Since each of these operations runs in O.1/ time, let us consider the cost of each
to be 1. The total cost of a sequence of n PUSH and POP operations is therefore n,
and the actual running time for n operations is therefore ‚.n/.
Now we add the stack operation MULTIPOP.S; k/, which removes the k top ob-
jects of stack S, popping the entire stack if the stack contains fewer than k objects.
Of course, we assume that k is positive; otherwise the MULTIPOP operation leaves
the stack unchanged. In the following pseudocode, the operation STACK-EMPTY
returns TRUE if there are no objects currently on the stack, and FALSE otherwise.

17.1
Aggregate analysis
453
23
17
6
39
10
47
(a)
top
10
47
(b)
top
(c)
Figure 17.1
The action of MULTIPOP on a stack S, shown initially in (a). The top 4 objects are
popped by MULTIPOP.S; 4/, whose result is shown in (b). The next operation is MULTIPOP.S; 7/,
which empties the stack—shown in (c)—since there were fewer than 7 objects remaining.
MULTIPOP.S; k/
1
while not STACK-EMPTY.S/ and k > 0
2
POP.S/
3
k D k  1
Figure 17.1 shows an example of MULTIPOP.
What is the running time of MULTIPOP.S; k/ on a stack of s objects? The
actual running time is linear in the number of POP operations actually executed,
and thus we can analyze MULTIPOP in terms of the abstract costs of 1 each for
PUSH and POP. The number of iterations of the while loop is the number min.s; k/
of objects popped off the stack. Each iteration of the loop makes one call to POP in
line 2. Thus, the total cost of MULTIPOP is min.s; k/, and the actual running time
is a linear function of this cost.
Let us analyze a sequence of n PUSH, POP, and MULTIPOP operations on an ini-
tially empty stack. The worst-case cost of a MULTIPOP operation in the sequence
is O.n/, since the stack size is at most n. The worst-case time of any stack opera-
tion is therefore O.n/, and hence a sequence of n operations costs O.n2/, since we
may have O.n/ MULTIPOP operations costing O.n/ each. Although this analysis
is correct, the O.n2/ result, which we obtained by considering the worst-case cost
of each operation individually, is not tight.
Using aggregate analysis, we can obtain a better upper bound that considers the
entire sequence of n operations. In fact, although a single MULTIPOP operation
can be expensive, any sequence of n PUSH, POP, and MULTIPOP operations on an
initially empty stack can cost at most O.n/. Why? We can pop each object from the
stack at most once for each time we have pushed it onto the stack. Therefore, the
number of times that POP can be called on a nonempty stack, including calls within
MULTIPOP, is at most the number of PUSH operations, which is at most n. For any
value of n, any sequence of n PUSH, POP, and MULTIPOP operations takes a total
of O.n/ time. The average cost of an operation is O.n/=n D O.1/. In aggregate

454
Chapter 17
Amortized Analysis
analysis, we assign the amortized cost of each operation to be the average cost. In
this example, therefore, all three stack operations have an amortized cost of O.1/.
We emphasize again that although we have just shown that the average cost, and
hence the running time, of a stack operation is O.1/, we did not use probabilistic
reasoning. We actually showed a worst-case bound of O.n/ on a sequence of n
operations. Dividing this total cost by n yielded the average cost per operation, or
the amortized cost.
Incrementing a binary counter
As another example of aggregate analysis, consider the problem of implementing
a k-bit binary counter that counts upward from 0. We use an array AŒ0 : : k  1 of
bits, where A:length D k, as the counter. A binary number x that is stored in the
counter has its lowest-order bit in AŒ0 and its highest-order bit in AŒk  1, so that
x D Pk1
iD0 AŒi  2i. Initially, x D 0, and thus AŒi D 0 for i D 0; 1; : : : ; k  1. To
add 1 (modulo 2k) to the value in the counter, we use the following procedure.
INCREMENT.A/
1
i D 0
2
while i < A:length and AŒi == 1
3
AŒi D 0
4
i D i C 1
5
if i < A:length
6
AŒi D 1
Figure 17.2 shows what happens to a binary counter as we increment it 16 times,
starting with the initial value 0 and ending with the value 16.
At the start of
each iteration of the while loop in lines 2–4, we wish to add a 1 into position i.
If AŒi D 1, then adding 1 ﬂips the bit to 0 in position i and yields a carry of 1,
to be added into position i C 1 on the next iteration of the loop. Otherwise, the
loop ends, and then, if i < k, we know that AŒi D 0, so that line 6 adds a 1 into
position i, ﬂipping the 0 to a 1. The cost of each INCREMENT operation is linear
in the number of bits ﬂipped.
As with the stack example, a cursory analysis yields a bound that is correct but
not tight. A single execution of INCREMENT takes time ‚.k/ in the worst case, in
which array A contains all 1s. Thus, a sequence of n INCREMENT operations on
an initially zero counter takes time O.nk/ in the worst case.
We can tighten our analysis to yield a worst-case cost of O.n/ for a sequence of n
INCREMENT operations by observing that not all bits ﬂip each time INCREMENT
is called. As Figure 17.2 shows, AŒ0 does ﬂip each time INCREMENT is called.
The next bit up, AŒ1, ﬂips only every other time: a sequence of n INCREMENT

17.1
Aggregate analysis
455
0 0 0 0 0 0 0 0
0
0 0 0 0 0 0 0 1
1
0 0 0 0 0 0 1 0
2
0 0 0 0 0 0 1 1
3
0 0 0 0 0 1 0 0
4
0 0 0 0 0 1 0 1
5
0 0 0 0 0 1 1 0
6
0 0 0 0 0 1 1 1
7
0 0 0 0 1 0 0 0
8
0 0 0 0 1 0 0 1
9
0 0 0 0 1 0 1 0
10
0 0 0 0 1 0 1 1
11
0 0 0 0 1 1 0 0
12
0 0 0 0 1 1 0 1
13
0 0 0 0 1 1 1 0
14
0 0 0 0 1 1 1 1
15
0 0 0 1 0 0 0 0
16
A[0]
A[1]
A[2]
A[3]
A[4]
A[5]
A[6]
A[7]
Counter
value
Total
cost
1
3
4
7
8
10
11
15
16
18
19
22
23
25
26
31
0
Figure 17.2
An 8-bit binary counter as its value goes from 0 to 16 by a sequence of 16 INCREMENT
operations. Bits that ﬂip to achieve the next value are shaded. The running cost for ﬂipping bits is
shown at the right. Notice that the total cost is always less than twice the total number of INCREMENT
operations.
operations on an initially zero counter causes AŒ1 to ﬂip bn=2c times. Similarly,
bit AŒ2 ﬂips only every fourth time, or bn=4c times in a sequence of n INCREMENT
operations. In general, for i D 0; 1; : : : ; k  1, bit AŒi ﬂips bn=2ic times in a
sequence of n INCREMENT operations on an initially zero counter. For i  k,
bit AŒi does not exist, and so it cannot ﬂip. The total number of ﬂips in the
sequence is thus
k1
X
iD0
j n
2i
k
<
n
1
X
iD0
1
2i
D
2n ;
by equation (A.6). The worst-case time for a sequence of n INCREMENT operations
on an initially zero counter is therefore O.n/. The average cost of each operation,
and therefore the amortized cost per operation, is O.n/=n D O.1/.

456
Chapter 17
Amortized Analysis
Exercises
17.1-1
If the set of stack operations included a MULTIPUSH operation, which pushes k
items onto the stack, would the O.1/ bound on the amortized cost of stack opera-
tions continue to hold?
17.1-2
Show that if a DECREMENT operation were included in the k-bit counter example,
n operations could cost as much as ‚.nk/ time.
17.1-3
Suppose we perform a sequence of n operations on a data structure in which the ith
operation costs i if i is an exact power of 2, and 1 otherwise. Use aggregate analysis
to determine the amortized cost per operation.
17.2
The accounting method
In the accounting method of amortized analysis, we assign differing charges to
different operations, with some operations charged more or less than they actu-
ally cost. We call the amount we charge an operation its amortized cost. When
an operation’s amortized cost exceeds its actual cost, we assign the difference to
speciﬁc objects in the data structure as credit. Credit can help pay for later oper-
ations whose amortized cost is less than their actual cost. Thus, we can view the
amortized cost of an operation as being split between its actual cost and credit that
is either deposited or used up. Different operations may have different amortized
costs. This method differs from aggregate analysis, in which all operations have
the same amortized cost.
We must choose the amortized costs of operations carefully. If we want to show
that in the worst case the average cost per operation is small by analyzing with
amortized costs, we must ensure that the total amortized cost of a sequence of oper-
ations provides an upper bound on the total actual cost of the sequence. Moreover,
as in aggregate analysis, this relationship must hold for all sequences of opera-
tions. If we denote the actual cost of the ith operation by ci and the amortized cost
of the ith operation by yci, we require
n
X
iD1
yci 
n
X
iD1
ci
(17.1)
for all sequences of n operations.
The total credit stored in the data structure
is the difference between the total amortized cost and the total actual cost, or

17.2
The accounting method
457
Pn
iD1 yci  Pn
iD1 ci. By inequality (17.1), the total credit associated with the data
structure must be nonnegative at all times. If we ever were to allow the total credit
to become negative (the result of undercharging early operations with the promise
of repaying the account later on), then the total amortized costs incurred at that
time would be below the total actual costs incurred; for the sequence of operations
up to that time, the total amortized cost would not be an upper bound on the total
actual cost. Thus, we must take care that the total credit in the data structure never
becomes negative.
Stack operations
To illustrate the accounting method of amortized analysis, let us return to the stack
example. Recall that the actual costs of the operations were
PUSH
1 ,
POP
1 ,
MULTIPOP
min.k; s/ ,
where k is the argument supplied to MULTIPOP and s is the stack size when it is
called. Let us assign the following amortized costs:
PUSH
2 ,
POP
0 ,
MULTIPOP
0 .
Note that the amortized cost of MULTIPOP is a constant (0), whereas the actual cost
is variable. Here, all three amortized costs are constant. In general, the amortized
costs of the operations under consideration may differ from each other, and they
may even differ asymptotically.
We shall now show that we can pay for any sequence of stack operations by
charging the amortized costs. Suppose we use a dollar bill to represent each unit
of cost. We start with an empty stack. Recall the analogy of Section 10.1 between
the stack data structure and a stack of plates in a cafeteria. When we push a plate
on the stack, we use 1 dollar to pay the actual cost of the push and are left with a
credit of 1 dollar (out of the 2 dollars charged), which we leave on top of the plate.
At any point in time, every plate on the stack has a dollar of credit on it.
The dollar stored on the plate serves as prepayment for the cost of popping it
from the stack. When we execute a POP operation, we charge the operation nothing
and pay its actual cost using the credit stored in the stack. To pop a plate, we take
the dollar of credit off the plate and use it to pay the actual cost of the operation.
Thus, by charging the PUSH operation a little bit more, we can charge the POP
operation nothing.

458
Chapter 17
Amortized Analysis
Moreover, we can also charge MULTIPOP operations nothing. To pop the ﬁrst
plate, we take the dollar of credit off the plate and use it to pay the actual cost of a
POP operation. To pop a second plate, we again have a dollar of credit on the plate
to pay for the POP operation, and so on. Thus, we have always charged enough
up front to pay for MULTIPOP operations. In other words, since each plate on the
stack has 1 dollar of credit on it, and the stack always has a nonnegative number of
plates, we have ensured that the amount of credit is always nonnegative. Thus, for
any sequence of n PUSH, POP, and MULTIPOP operations, the total amortized cost
is an upper bound on the total actual cost. Since the total amortized cost is O.n/,
so is the total actual cost.
Incrementing a binary counter
As another illustration of the accounting method, we analyze the INCREMENT op-
eration on a binary counter that starts at zero. As we observed earlier, the running
time of this operation is proportional to the number of bits ﬂipped, which we shall
use as our cost for this example. Let us once again use a dollar bill to represent
each unit of cost (the ﬂipping of a bit in this example).
For the amortized analysis, let us charge an amortized cost of 2 dollars to set a
bit to 1. When a bit is set, we use 1 dollar (out of the 2 dollars charged) to pay
for the actual setting of the bit, and we place the other dollar on the bit as credit to
be used later when we ﬂip the bit back to 0. At any point in time, every 1 in the
counter has a dollar of credit on it, and thus we can charge nothing to reset a bit
to 0; we just pay for the reset with the dollar bill on the bit.
Now we can determine the amortized cost of INCREMENT. The cost of resetting
the bits within the while loop is paid for by the dollars on the bits that are reset. The
INCREMENT procedure sets at most one bit, in line 6, and therefore the amortized
cost of an INCREMENT operation is at most 2 dollars. The number of 1s in the
counter never becomes negative, and thus the amount of credit stays nonnegative
at all times. Thus, for n INCREMENT operations, the total amortized cost is O.n/,
which bounds the total actual cost.
Exercises
17.2-1
Suppose we perform a sequence of stack operations on a stack whose size never
exceeds k. After every k operations, we make a copy of the entire stack for backup
purposes. Show that the cost of n stack operations, including copying the stack,
is O.n/ by assigning suitable amortized costs to the various stack operations.

17.3
The potential method
459
17.2-2
Redo Exercise 17.1-3 using an accounting method of analysis.
17.2-3
Suppose we wish not only to increment a counter but also to reset it to zero (i.e.,
make all bits in it 0). Counting the time to examine or modify a bit as ‚.1/,
show how to implement a counter as an array of bits so that any sequence of n
INCREMENT and RESET operations takes time O.n/ on an initially zero counter.
(Hint: Keep a pointer to the high-order 1.)
17.3
The potential method
Instead of representing prepaid work as credit stored with speciﬁc objects in the
data structure, the potential method of amortized analysis represents the prepaid
work as “potential energy,” or just “potential,” which can be released to pay for
future operations. We associate the potential with the data structure as a whole
rather than with speciﬁc objects within the data structure.
The potential method works as follows. We will perform n operations, starting
with an initial data structure D0. For each i D 1; 2; : : : ; n, we let ci be the actual
cost of the ith operation and Di be the data structure that results after applying
the ith operation to data structure Di1. A potential function ˆ maps each data
structure Di to a real number ˆ.Di/, which is the potential associated with data
structure Di. The amortized cost yci of the ith operation with respect to potential
function ˆ is deﬁned by
yci D ci C ˆ.Di/  ˆ.Di1/ :
(17.2)
The amortized cost of each operation is therefore its actual cost plus the change in
potential due to the operation. By equation (17.2), the total amortized cost of the n
operations is
n
X
iD1
yci
D
n
X
iD1
.ci C ˆ.Di/  ˆ.Di1//
D
n
X
iD1
ci C ˆ.Dn/  ˆ.D0/ :
(17.3)
The second equality follows from equation (A.9) because the ˆ.Di/ terms tele-
scope.
If we can deﬁne a potential function ˆ so that ˆ.Dn/  ˆ.D0/, then the total
amortized cost Pn
iD1 yci gives an upper bound on the total actual cost Pn
iD1 ci.

460
Chapter 17
Amortized Analysis
In practice, we do not always know how many operations might be performed.
Therefore, if we require that ˆ.Di/  ˆ.D0/ for all i, then we guarantee, as in
the accounting method, that we pay in advance. We usually just deﬁne ˆ.D0/ to
be 0 and then show that ˆ.Di/  0 for all i. (See Exercise 17.3-1 for an easy way
to handle cases in which ˆ.D0/ ¤ 0.)
Intuitively, if the potential difference ˆ.Di/  ˆ.Di1/ of the ith operation is
positive, then the amortized cost yci represents an overcharge to the ith operation,
and the potential of the data structure increases. If the potential difference is neg-
ative, then the amortized cost represents an undercharge to the ith operation, and
the decrease in the potential pays for the actual cost of the operation.
The amortized costs deﬁned by equations (17.2) and (17.3) depend on the choice
of the potential function ˆ. Different potential functions may yield different amor-
tized costs yet still be upper bounds on the actual costs. We often ﬁnd trade-offs
that we can make in choosing a potential function; the best potential function to
use depends on the desired time bounds.
Stack operations
To illustrate the potential method, we return once again to the example of the stack
operations PUSH, POP, and MULTIPOP. We deﬁne the potential function ˆ on a
stack to be the number of objects in the stack. For the empty stack D0 with which
we start, we have ˆ.D0/ D 0. Since the number of objects in the stack is never
negative, the stack Di that results after the ith operation has nonnegative potential,
and thus
ˆ.Di/

0
D
ˆ.D0/ :
The total amortized cost of n operations with respect to ˆ therefore represents an
upper bound on the actual cost.
Let us now compute the amortized costs of the various stack operations. If the ith
operation on a stack containing s objects is a PUSH operation, then the potential
difference is
ˆ.Di/  ˆ.Di1/
D
.s C 1/  s
D
1 :
By equation (17.2), the amortized cost of this PUSH operation is
yci
D
ci C ˆ.Di/  ˆ.Di1/
D
1 C 1
D
2 :

17.3
The potential method
461
Suppose that the ith operation on the stack is MULTIPOP.S; k/, which causes
k0 D min.k; s/ objects to be popped off the stack. The actual cost of the opera-
tion is k0, and the potential difference is
ˆ.Di/  ˆ.Di1/ D k0 :
Thus, the amortized cost of the MULTIPOP operation is
yci
D
ci C ˆ.Di/  ˆ.Di1/
D
k0  k0
D
0 :
Similarly, the amortized cost of an ordinary POP operation is 0.
The amortized cost of each of the three operations is O.1/, and thus the total
amortized cost of a sequence of n operations is O.n/. Since we have already argued
that ˆ.Di/  ˆ.D0/, the total amortized cost of n operations is an upper bound
on the total actual cost. The worst-case cost of n operations is therefore O.n/.
Incrementing a binary counter
As another example of the potential method, we again look at incrementing a binary
counter. This time, we deﬁne the potential of the counter after the ith INCREMENT
operation to be bi, the number of 1s in the counter after the ith operation.
Let us compute the amortized cost of an INCREMENT operation. Suppose that
the ith INCREMENT operation resets ti bits. The actual cost of the operation is
therefore at most ti C 1, since in addition to resetting ti bits, it sets at most one
bit to 1. If bi D 0, then the ith operation resets all k bits, and so bi1 D ti D k.
If bi > 0, then bi D bi1  ti C 1. In either case, bi  bi1  ti C 1, and the
potential difference is
ˆ.Di/  ˆ.Di1/

.bi1  ti C 1/  bi1
D
1  ti :
The amortized cost is therefore
yci
D
ci C ˆ.Di/  ˆ.Di1/

.ti C 1/ C .1  ti/
D
2 :
If the counter starts at zero, then ˆ.D0/ D 0. Since ˆ.Di/  0 for all i, the total
amortized cost of a sequence of n INCREMENT operations is an upper bound on the
total actual cost, and so the worst-case cost of n INCREMENT operations is O.n/.
The potential method gives us an easy way to analyze the counter even when
it does not start at zero. The counter starts with b0 1s, and after n INCREMENT

462
Chapter 17
Amortized Analysis
operations it has bn 1s, where 0  b0; bn  k. (Recall that k is the number of bits
in the counter.) We can rewrite equation (17.3) as
n
X
iD1
ci D
n
X
iD1
yci  ˆ.Dn/ C ˆ.D0/ :
(17.4)
We have yci  2 for all 1  i  n. Since ˆ.D0/ D b0 and ˆ.Dn/ D bn, the total
actual cost of n INCREMENT operations is
n
X
iD1
ci

n
X
iD1
2  bn C b0
D
2n  bn C b0 :
Note in particular that since b0  k, as long as k D O.n/, the total actual cost
is O.n/. In other words, if we execute at least n D .k/ INCREMENT operations,
the total actual cost is O.n/, no matter what initial value the counter contains.
Exercises
17.3-1
Suppose we have a potential function ˆ such that ˆ.Di/  ˆ.D0/ for all i, but
ˆ.D0/ ¤ 0. Show that there exists a potential function ˆ0 such that ˆ0.D0/ D 0,
ˆ0.Di/  0 for all i  1, and the amortized costs using ˆ0 are the same as the
amortized costs using ˆ.
17.3-2
Redo Exercise 17.1-3 using a potential method of analysis.
17.3-3
Consider an ordinary binary min-heap data structure with n elements supporting
the instructions INSERT and EXTRACT-MIN in O.lg n/ worst-case time. Give a
potential function ˆ such that the amortized cost of INSERT is O.lg n/ and the
amortized cost of EXTRACT-MIN is O.1/, and show that it works.
17.3-4
What is the total cost of executing n of the stack operations PUSH, POP, and
MULTIPOP, assuming that the stack begins with s0 objects and ﬁnishes with sn
objects?
17.3-5
Suppose that a counter begins at a number with b 1s in its binary representa-
tion, rather than at 0. Show that the cost of performing n INCREMENT operations
is O.n/ if n D .b/. (Do not assume that b is constant.)

17.4
Dynamic tables
463
17.3-6
Show how to implement a queue with two ordinary stacks (Exercise 10.1-6) so that
the amortized cost of each ENQUEUE and each DEQUEUE operation is O.1/.
17.3-7
Design a data structure to support the following two operations for a dynamic
multiset S of integers, which allows duplicate values:
INSERT.S; x/ inserts x into S.
DELETE-LARGER-HALF.S/ deletes the largest djSj =2e elements from S.
Explain how to implement this data structure so that any sequence of m INSERT
and DELETE-LARGER-HALF operations runs in O.m/ time. Your implementation
should also include a way to output the elements of S in O.jSj/ time.
17.4
Dynamic tables
We do not always know in advance how many objects some applications will store
in a table. We might allocate space for a table, only to ﬁnd out later that it is not
enough. We must then reallocate the table with a larger size and copy all objects
stored in the original table over into the new, larger table. Similarly, if many objects
have been deleted from the table, it may be worthwhile to reallocate the table with
a smaller size. In this section, we study this problem of dynamically expanding and
contracting a table. Using amortized analysis, we shall show that the amortized cost
of insertion and deletion is only O.1/, even though the actual cost of an operation
is large when it triggers an expansion or a contraction. Moreover, we shall see how
to guarantee that the unused space in a dynamic table never exceeds a constant
fraction of the total space.
We assume that the dynamic table supports the operations TABLE-INSERT and
TABLE-DELETE. TABLE-INSERT inserts into the table an item that occupies a sin-
gle slot, that is, a space for one item. Likewise, TABLE-DELETE removes an item
from the table, thereby freeing a slot. The details of the data-structuring method
used to organize the table are unimportant; we might use a stack (Section 10.1),
a heap (Chapter 6), or a hash table (Chapter 11). We might also use an array or
collection of arrays to implement object storage, as we did in Section 10.3.
We shall ﬁnd it convenient to use a concept introduced in our analysis of hashing
(Chapter 11). We deﬁne the load factor ˛.T / of a nonempty table T to be the
number of items stored in the table divided by the size (number of slots) of the
table. We assign an empty table (one with no items) size 0, and we deﬁne its load
factor to be 1. If the load factor of a dynamic table is bounded below by a constant,

464
Chapter 17
Amortized Analysis
the unused space in the table is never more than a constant fraction of the total
amount of space.
We start by analyzing a dynamic table in which we only insert items. We then
consider the more general case in which we both insert and delete items.
17.4.1
Table expansion
Let us assume that storage for a table is allocated as an array of slots. A table ﬁlls
up when all slots have been used or, equivalently, when its load factor is 1.1 In some
software environments, upon attempting to insert an item into a full table, the only
alternative is to abort with an error. We shall assume, however, that our software
environment, like many modern ones, provides a memory-management system that
can allocate and free blocks of storage on request. Thus, upon inserting an item
into a full table, we can expand the table by allocating a new table with more slots
than the old table had. Because we always need the table to reside in contiguous
memory, we must allocate a new array for the larger table and then copy items from
the old table into the new table.
A common heuristic allocates a new table with twice as many slots as the old
one. If the only table operations are insertions, then the load factor of the table is
always at least 1=2, and thus the amount of wasted space never exceeds half the
total space in the table.
In the following pseudocode, we assume that T is an object representing the
table. The attribute T:table contains a pointer to the block of storage representing
the table, T:num contains the number of items in the table, and T:size gives the total
number of slots in the table. Initially, the table is empty: T:num D T:size D 0.
TABLE-INSERT.T; x/
1
if T:size == 0
2
allocate T:table with 1 slot
3
T:size D 1
4
if T:num == T:size
5
allocate new-table with 2  T:size slots
6
insert all items in T:table into new-table
7
free T:table
8
T:table D new-table
9
T:size D 2  T:size
10
insert x into T:table
11
T:num D T:num C 1
1In some situations, such as an open-address hash table, we may wish to consider a table to be full if
its load factor equals some constant strictly less than 1. (See Exercise 17.4-1.)

17.4
Dynamic tables
465
Notice that we have two “insertion” procedures here: the TABLE-INSERT proce-
dure itself and the elementary insertion into a table in lines 6 and 10. We can
analyze the running time of TABLE-INSERT in terms of the number of elementary
insertions by assigning a cost of 1 to each elementary insertion. We assume that
the actual running time of TABLE-INSERT is linear in the time to insert individual
items, so that the overhead for allocating an initial table in line 2 is constant and
the overhead for allocating and freeing storage in lines 5 and 7 is dominated by
the cost of transferring items in line 6. We call the event in which lines 5–9 are
executed an expansion.
Let us analyze a sequence of n TABLE-INSERT operations on an initially empty
table. What is the cost ci of the ith operation? If the current table has room for the
new item (or if this is the ﬁrst operation), then ci D 1, since we need only perform
the one elementary insertion in line 10. If the current table is full, however, and an
expansion occurs, then ci D i: the cost is 1 for the elementary insertion in line 10
plus i  1 for the items that we must copy from the old table to the new table in
line 6. If we perform n operations, the worst-case cost of an operation is O.n/,
which leads to an upper bound of O.n2/ on the total running time for n operations.
This bound is not tight, because we rarely expand the table in the course of n
TABLE-INSERT operations. Speciﬁcally, the ith operation causes an expansion
only when i  1 is an exact power of 2. The amortized cost of an operation is in
fact O.1/, as we can show using aggregate analysis. The cost of the ith operation
is
ci D
(
i
if i  1 is an exact power of 2 ;
1
otherwise :
The total cost of n TABLE-INSERT operations is therefore
n
X
iD1
ci

n C
blg nc
X
jD0
2j
<
n C 2n
D
3n ;
because at most n operations cost 1 and the costs of the remaining operations form
a geometric series. Since the total cost of n TABLE-INSERT operations is bounded
by 3n, the amortized cost of a single operation is at most 3.
By using the accounting method, we can gain some feeling for why the amor-
tized cost of a TABLE-INSERT operation should be 3. Intuitively, each item pays
for 3 elementary insertions: inserting itself into the current table, moving itself
when the table expands, and moving another item that has already been moved
once when the table expands. For example, suppose that the size of the table is m
immediately after an expansion. Then the table holds m=2 items, and it contains

466
Chapter 17
Amortized Analysis
no credit. We charge 3 dollars for each insertion. The elementary insertion that
occurs immediately costs 1 dollar. We place another dollar as credit on the item
inserted. We place the third dollar as credit on one of the m=2 items already in the
table. The table will not ﬁll again until we have inserted another m=2  1 items,
and thus, by the time the table contains m items and is full, we will have placed a
dollar on each item to pay to reinsert it during the expansion.
We can use the potential method to analyze a sequence of n TABLE-INSERT
operations, and we shall use it in Section 17.4.2 to design a TABLE-DELETE op-
eration that has an O.1/ amortized cost as well. We start by deﬁning a potential
function ˆ that is 0 immediately after an expansion but builds to the table size by
the time the table is full, so that we can pay for the next expansion by the potential.
The function
ˆ.T / D 2  T:num  T:size
(17.5)
is one possibility. Immediately after an expansion, we have T:num D T:size=2,
and thus ˆ.T / D 0, as desired.
Immediately before an expansion, we have
T:num D T:size, and thus ˆ.T / D T:num, as desired. The initial value of the
potential is 0, and since the table is always at least half full, T:num  T:size=2,
which implies that ˆ.T / is always nonnegative. Thus, the sum of the amortized
costs of n TABLE-INSERT operations gives an upper bound on the sum of the actual
costs.
To analyze the amortized cost of the ith TABLE-INSERT operation, we let numi
denote the number of items stored in the table after the ith operation, sizei denote
the total size of the table after the ith operation, and ˆi denote the potential after
the ith operation. Initially, we have num0 D 0, size0 D 0, and ˆ0 D 0.
If the ith TABLE-INSERT operation does not trigger an expansion, then we have
sizei D sizei1 and the amortized cost of the operation is
yci
D
ci C ˆi  ˆi1
D
1 C .2  numi  sizei/  .2  numi1  sizei1/
D
1 C .2  numi  sizei/  .2.numi  1/  sizei/
D
3 :
If the ith operation does trigger an expansion, then we have sizei D 2  sizei1 and
sizei1 D numi1 D numi  1, which implies that sizei D 2  .numi  1/. Thus,
the amortized cost of the operation is
yci
D
ci C ˆi  ˆi1
D
numi C .2  numi  sizei/  .2  numi1  sizei1/
D
numi C .2  numi  2  .numi  1//  .2.numi  1/  .numi  1//
D
numi C 2  .numi  1/
D
3 :

17.4
Dynamic tables
467
Φi
numi
sizei
0
8
16
24
32
0
8
16
24
32
i
Figure 17.3
The effect of a sequence of n TABLE-INSERT operations on the number numi of items
in the table, the number sizei of slots in the table, and the potential ˆi D 2  numi  sizei, each
being measured after the ith operation. The thin line shows numi, the dashed line shows sizei, and
the thick line shows ˆi. Notice that immediately before an expansion, the potential has built up to
the number of items in the table, and therefore it can pay for moving all the items to the new table.
Afterwards, the potential drops to 0, but it is immediately increased by 2 upon inserting the item that
caused the expansion.
Figure 17.3 plots the values of numi, sizei, and ˆi against i. Notice how the
potential builds to pay for expanding the table.
17.4.2
Table expansion and contraction
To implement a TABLE-DELETE operation, it is simple enough to remove the spec-
iﬁed item from the table. In order to limit the amount of wasted space, however,
we might wish to contract the table when the load factor becomes too small. Table
contraction is analogous to table expansion: when the number of items in the table
drops too low, we allocate a new, smaller table and then copy the items from the
old table into the new one. We can then free the storage for the old table by return-
ing it to the memory-management system. Ideally, we would like to preserve two
properties:

the load factor of the dynamic table is bounded below by a positive constant,
and

the amortized cost of a table operation is bounded above by a constant.

468
Chapter 17
Amortized Analysis
We assume that we measure the cost in terms of elementary insertions and dele-
tions.
You might think that we should double the table size upon inserting an item into
a full table and halve the size when a deleting an item would cause the table to
become less than half full. This strategy would guarantee that the load factor of
the table never drops below 1=2, but unfortunately, it can cause the amortized cost
of an operation to be quite large. Consider the following scenario. We perform n
operations on a table T , where n is an exact power of 2. The ﬁrst n=2 operations are
insertions, which by our previous analysis cost a total of ‚.n/. At the end of this
sequence of insertions, T:num D T:size D n=2. For the second n=2 operations,
we perform the following sequence:
insert, delete, delete, insert, insert, delete, delete, insert, insert, . . . .
The ﬁrst insertion causes the table to expand to size n. The two following deletions
cause the table to contract back to size n=2. Two further insertions cause another
expansion, and so forth. The cost of each expansion and contraction is ‚.n/, and
there are ‚.n/ of them. Thus, the total cost of the n operations is ‚.n2/, making
the amortized cost of an operation ‚.n/.
The downside of this strategy is obvious: after expanding the table, we do not
delete enough items to pay for a contraction. Likewise, after contracting the table,
we do not insert enough items to pay for an expansion.
We can improve upon this strategy by allowing the load factor of the table to
drop below 1=2. Speciﬁcally, we continue to double the table size upon inserting
an item into a full table, but we halve the table size when deleting an item causes
the table to become less than 1=4 full, rather than 1=2 full as before. The load
factor of the table is therefore bounded below by the constant 1=4.
Intuitively, we would consider a load factor of 1=2 to be ideal, and the table’s
potential would then be 0. As the load factor deviates from 1=2, the potential
increases so that by the time we expand or contract the table, the table has garnered
sufﬁcient potential to pay for copying all the items into the newly allocated table.
Thus, we will need a potential function that has grown to T:num by the time that
the load factor has either increased to 1 or decreased to 1=4. After either expanding
or contracting the table, the load factor goes back to 1=2 and the table’s potential
reduces back to 0.
We omit the code for TABLE-DELETE, since it is analogous to TABLE-INSERT.
For our analysis, we shall assume that whenever the number of items in the table
drops to 0, we free the storage for the table. That is, if T:num D 0, then T:size D 0.
We can now use the potential method to analyze the cost of a sequence of n
TABLE-INSERT and TABLE-DELETE operations. We start by deﬁning a poten-
tial function ˆ that is 0 immediately after an expansion or contraction and builds
as the load factor increases to 1 or decreases to 1=4. Let us denote the load fac-

17.4
Dynamic tables
469
numi
Φi
sizei
0
8
16
24
32
40
48
0
8
16
24
32
i
Figure 17.4
The effect of a sequence of n TABLE-INSERT and TABLE-DELETE operations on the
number numi of items in the table, the number sizei of slots in the table, and the potential
ˆi D

2  numi  sizei
if ˛i  1=2 ;
sizei=2  numi
if ˛i < 1=2 ;
each measured after the ith operation. The thin line shows numi, the dashed line shows sizei, and
the thick line shows ˆi. Notice that immediately before an expansion, the potential has built up to
the number of items in the table, and therefore it can pay for moving all the items to the new table.
Likewise, immediately before a contraction, the potential has built up to the number of items in the
table.
tor of a nonempty table T by ˛.T / D T:num=T:size. Since for an empty table,
T:num D T:size D 0 and ˛.T / D 1, we always have T:num D ˛.T /  T:size,
whether the table is empty or not. We shall use as our potential function
ˆ.T / D
(
2  T:num  T:size
if ˛.T /  1=2 ;
T:size=2  T:num
if ˛.T / < 1=2 :
(17.6)
Observe that the potential of an empty table is 0 and that the potential is never
negative. Thus, the total amortized cost of a sequence of operations with respect
to ˆ provides an upper bound on the actual cost of the sequence.
Before proceeding with a precise analysis, we pause to observe some properties
of the potential function, as illustrated in Figure 17.4. Notice that when the load
factor is 1=2, the potential is 0. When the load factor is 1, we have T:size D T:num,
which implies ˆ.T / D T:num, and thus the potential can pay for an expansion if
an item is inserted. When the load factor is 1=4, we have T:size D 4T:num, which

470
Chapter 17
Amortized Analysis
implies ˆ.T / D T:num, and thus the potential can pay for a contraction if an item
is deleted.
To analyze a sequence of n TABLE-INSERT and TABLE-DELETE operations,
we let ci denote the actual cost of the ith operation, yci denote its amortized cost
with respect to ˆ, numi denote the number of items stored in the table after the ith
operation, sizei denote the total size of the table after the ith operation, ˛i denote
the load factor of the table after the ith operation, and ˆi denote the potential after
the ith operation. Initially, num0 D 0, size0 D 0, ˛0 D 1, and ˆ0 D 0.
We start with the case in which the ith operation is TABLE-INSERT. The analy-
sis is identical to that for table expansion in Section 17.4.1 if ˛i1  1=2. Whether
the table expands or not, the amortized cost yci of the operation is at most 3.
If ˛i1 < 1=2, the table cannot expand as a result of the operation, since the ta-
ble expands only when ˛i1 D 1. If ˛i < 1=2 as well, then the amortized cost of
the ith operation is
yci
D
ci C ˆi  ˆi1
D
1 C .sizei=2  numi/  .sizei1=2  numi1/
D
1 C .sizei=2  numi/  .sizei=2  .numi  1//
D
0 :
If ˛i1 < 1=2 but ˛i  1=2, then
yci
D
ci C ˆi  ˆi1
D
1 C .2  numi  sizei/  .sizei1=2  numi1/
D
1 C .2.numi1 C 1/  sizei1/  .sizei1=2  numi1/
D
3  numi1  3
2sizei1 C 3
D
3˛i1sizei1  3
2sizei1 C 3
<
3
2sizei1  3
2sizei1 C 3
D
3 :
Thus, the amortized cost of a TABLE-INSERT operation is at most 3.
We now turn to the case in which the ith operation is TABLE-DELETE. In this
case, numi D numi1  1. If ˛i1 < 1=2, then we must consider whether the
operation causes the table to contract. If it does not, then sizei D sizei1 and the
amortized cost of the operation is
yci
D
ci C ˆi  ˆi1
D
1 C .sizei=2  numi/  .sizei1=2  numi1/
D
1 C .sizei=2  numi/  .sizei=2  .numi C 1//
D
2 :

17.4
Dynamic tables
471
If ˛i1 < 1=2 and the ith operation does trigger a contraction, then the actual cost
of the operation is ci D numi C 1, since we delete one item and move numi items.
We have sizei=2 D sizei1=4 D numi1 D numi C 1, and the amortized cost of
the operation is
yci
D
ci C ˆi  ˆi1
D
.numi C 1/ C .sizei=2  numi/  .sizei1=2  numi1/
D
.numi C 1/ C ..numi C 1/  numi/  ..2  numi C 2/  .numi C 1//
D
1 :
When the ith operation is a TABLE-DELETE and ˛i1  1=2, the amortized cost
is also bounded above by a constant. We leave the analysis as Exercise 17.4-2.
In summary, since the amortized cost of each operation is bounded above by
a constant, the actual time for any sequence of n operations on a dynamic table
is O.n/.
Exercises
17.4-1
Suppose that we wish to implement a dynamic, open-address hash table. Why
might we consider the table to be full when its load factor reaches some value ˛
that is strictly less than 1? Describe brieﬂy how to make insertion into a dynamic,
open-address hash table run in such a way that the expected value of the amortized
cost per insertion is O.1/. Why is the expected value of the actual cost per insertion
not necessarily O.1/ for all insertions?
17.4-2
Show that if ˛i1  1=2 and the ith operation on a dynamic table is TABLE-
DELETE, then the amortized cost of the operation with respect to the potential
function (17.6) is bounded above by a constant.
17.4-3
Suppose that instead of contracting a table by halving its size when its load factor
drops below 1=4, we contract it by multiplying its size by 2=3 when its load factor
drops below 1=3. Using the potential function
ˆ.T / D j2  T:num  T:sizej ;
show that the amortized cost of a TABLE-DELETE that uses this strategy is bounded
above by a constant.

472
Chapter 17
Amortized Analysis
Problems
17-1
Bit-reversed binary counter
Chapter 30 examines an important algorithm called the fast Fourier transform,
or FFT. The ﬁrst step of the FFT algorithm performs a bit-reversal permutation on
an input array AŒ0 : : n1 whose length is n D 2k for some nonnegative integer k.
This permutation swaps elements whose indices have binary representations that
are the reverse of each other.
We can express each index a as a k-bit sequence hak1; ak2; : : : ; a0i, where
a D Pk1
iD0 ai 2i. We deﬁne
revk.hak1; ak2; : : : ; a0i/ D ha0; a1; : : : ; ak1i I
thus,
revk.a/ D
k1
X
iD0
aki12i :
For example, if n D 16 (or, equivalently, k D 4), then revk.3/ D 12, since
the 4-bit representation of 3 is 0011, which when reversed gives 1100, the 4-bit
representation of 12.
a. Given a function revk that runs in ‚.k/ time, write an algorithm to perform the
bit-reversal permutation on an array of length n D 2k in O.nk/ time.
We can use an algorithm based on an amortized analysis to improve the running
time of the bit-reversal permutation. We maintain a “bit-reversed counter” and a
procedure BIT-REVERSED-INCREMENT that, when given a bit-reversed-counter
value a, produces revk.revk.a/ C 1/. If k D 4, for example, and the bit-reversed
counter starts at 0, then successive calls to BIT-REVERSED-INCREMENT produce
the sequence
0000; 1000; 0100; 1100; 0010; 1010; : : : D 0; 8; 4; 12; 2; 10; : : : :
b. Assume that the words in your computer store k-bit values and that in unit time,
your computer can manipulate the binary values with operations such as shifting
left or right by arbitrary amounts, bitwise-AND, bitwise-OR, etc. Describe
an implementation of the BIT-REVERSED-INCREMENT procedure that allows
the bit-reversal permutation on an n-element array to be performed in a total
of O.n/ time.
c. Suppose that you can shift a word left or right by only one bit in unit time. Is it
still possible to implement an O.n/-time bit-reversal permutation?

Problems for Chapter 17
473
17-2
Making binary search dynamic
Binary search of a sorted array takes logarithmic search time, but the time to insert
a new element is linear in the size of the array. We can improve the time for
insertion by keeping several sorted arrays.
Speciﬁcally, suppose that we wish to support SEARCH and INSERT on a set
of n elements.
Let k D dlg.n C 1/e, and let the binary representation of n
be hnk1; nk2; : : : ; n0i. We have k sorted arrays A0; A1; : : : ; Ak1, where for
i D 0; 1; : : : ; k  1, the length of array Ai is 2i. Each array is either full or empty,
depending on whether ni D 1 or ni D 0, respectively. The total number of ele-
ments held in all k arrays is therefore Pk1
iD0 ni 2i D n. Although each individual
array is sorted, elements in different arrays bear no particular relationship to each
other.
a. Describe how to perform the SEARCH operation for this data structure. Analyze
its worst-case running time.
b. Describe how to perform the INSERT operation. Analyze its worst-case and
amortized running times.
c. Discuss how to implement DELETE.
17-3
Amortized weight-balanced trees
Consider an ordinary binary search tree augmented by adding to each node x the
attribute x:size giving the number of keys stored in the subtree rooted at x. Let ˛
be a constant in the range 1=2  ˛ < 1. We say that a given node x is ˛-balanced
if x:left:size  ˛  x:size and x:right:size  ˛  x:size. The tree as a whole
is ˛-balanced if every node in the tree is ˛-balanced. The following amortized
approach to maintaining weight-balanced trees was suggested by G. Varghese.
a. A 1=2-balanced tree is, in a sense, as balanced as it can be. Given a node x
in an arbitrary binary search tree, show how to rebuild the subtree rooted at x
so that it becomes 1=2-balanced. Your algorithm should run in time ‚.x:size/,
and it can use O.x:size/ auxiliary storage.
b. Show that performing a search in an n-node ˛-balanced binary search tree
takes O.lg n/ worst-case time.
For the remainder of this problem, assume that the constant ˛ is strictly greater
than 1=2. Suppose that we implement INSERT and DELETE as usual for an n-node
binary search tree, except that after every such operation, if any node in the tree
is no longer ˛-balanced, then we “rebuild” the subtree rooted at the highest such
node in the tree so that it becomes 1=2-balanced.

474
Chapter 17
Amortized Analysis
We shall analyze this rebuilding scheme using the potential method. For a node x
in a binary search tree T , we deﬁne

.x/ D jx:left:size  x:right:sizej ;
and we deﬁne the potential of T as
ˆ.T / D c
X
x2T W.x/2

.x/ ;
where c is a sufﬁciently large constant that depends on ˛.
c. Argue that any binary search tree has nonnegative potential and that a 1=2-
balanced tree has potential 0.
d. Suppose that m units of potential can pay for rebuilding an m-node subtree.
How large must c be in terms of ˛ in order for it to take O.1/ amortized time
to rebuild a subtree that is not ˛-balanced?
e. Show that inserting a node into or deleting a node from an n-node ˛-balanced
tree costs O.lg n/ amortized time.
17-4
The cost of restructuring red-black trees
There are four basic operations on red-black trees that perform structural modi-
ﬁcations: node insertions, node deletions, rotations, and color changes. We have
seen that RB-INSERT and RB-DELETE use only O.1/ rotations, node insertions,
and node deletions to maintain the red-black properties, but they may make many
more color changes.
a. Describe a legal red-black tree with n nodes such that calling RB-INSERT to
add the .n C 1/st node causes .lg n/ color changes. Then describe a legal
red-black tree with n nodes for which calling RB-DELETE on a particular node
causes .lg n/ color changes.
Although the worst-case number of color changes per operation can be logarithmic,
we shall prove that any sequence of m RB-INSERT and RB-DELETE operations on
an initially empty red-black tree causes O.m/ structural modiﬁcations in the worst
case. Note that we count each color change as a structural modiﬁcation.
b. Some of the cases handled by the main loop of the code of both RB-INSERT-
FIXUP and RB-DELETE-FIXUP are terminating: once encountered, they cause
the loop to terminate after a constant number of additional operations. For each
of the cases of RB-INSERT-FIXUP and RB-DELETE-FIXUP, specify which are
terminating and which are not. (Hint: Look at Figures 13.5, 13.6, and 13.7.)

Problems for Chapter 17
475
We shall ﬁrst analyze the structural modiﬁcations when only insertions are per-
formed. Let T be a red-black tree, and deﬁne ˆ.T / to be the number of red nodes
in T . Assume that 1 unit of potential can pay for the structural modiﬁcations per-
formed by any of the three cases of RB-INSERT-FIXUP.
c. Let T 0 be the result of applying Case 1 of RB-INSERT-FIXUP to T . Argue that
ˆ.T 0/ D ˆ.T /  1.
d. When we insert a node into a red-black tree using RB-INSERT, we can break
the operation into three parts. List the structural modiﬁcations and potential
changes resulting from lines 1–16 of RB-INSERT, from nonterminating cases
of RB-INSERT-FIXUP, and from terminating cases of RB-INSERT-FIXUP.
e. Using part (d), argue that the amortized number of structural modiﬁcations per-
formed by any call of RB-INSERT is O.1/.
We now wish to prove that there are O.m/ structural modiﬁcations when there are
both insertions and deletions. Let us deﬁne, for each node x,
w.x/ D
„
0
if x is red ;
1
if x is black and has no red children ;
0
if x is black and has one red child ;
2
if x is black and has two red children :
Now we redeﬁne the potential of a red-black tree T as
ˆ.T / D
X
x2T
w.x/ ;
and let T 0 be the tree that results from applying any nonterminating case of RB-
INSERT-FIXUP or RB-DELETE-FIXUP to T .
f. Show that ˆ.T 0/  ˆ.T /  1 for all nonterminating cases of RB-INSERT-
FIXUP. Argue that the amortized number of structural modiﬁcations performed
by any call of RB-INSERT-FIXUP is O.1/.
g. Show that ˆ.T 0/  ˆ.T /  1 for all nonterminating cases of RB-DELETE-
FIXUP. Argue that the amortized number of structural modiﬁcations performed
by any call of RB-DELETE-FIXUP is O.1/.
h. Complete the proof that in the worst case, any sequence of m RB-INSERT and
RB-DELETE operations performs O.m/ structural modiﬁcations.

476
Chapter 17
Amortized Analysis
17-5
Competitive analysis of self-organizing lists with move-to-front
A self-organizing list is a linked list of n elements, in which each element has a
unique key. When we search for an element in the list, we are given a key, and we
want to ﬁnd an element with that key.
A self-organizing list has two important properties:
1. To ﬁnd an element in the list, given its key, we must traverse the list from the
beginning until we encounter the element with the given key. If that element is
the kth element from the start of the list, then the cost to ﬁnd the element is k.
2. We may reorder the list elements after any operation, according to a given rule
with a given cost. We may choose any heuristic we like to decide how to reorder
the list.
Assume that we start with a given list of n elements, and we are given an access
sequence 	 D h	1; 	2; : : : ; 	mi of keys to ﬁnd, in order. The cost of the sequence
is the sum of the costs of the individual accesses in the sequence.
Out of the various possible ways to reorder the list after an operation, this prob-
lem focuses on transposing adjacent list elements—switching their positions in the
list—with a unit cost for each transpose operation. You will show, by means of a
potential function, that a particular heuristic for reordering the list, move-to-front,
entails a total cost no worse than 4 times that of any other heuristic for maintaining
the list order—even if the other heuristic knows the access sequence in advance!
We call this type of analysis a competitive analysis.
For a heuristic H and a given initial ordering of the list, denote the access cost of
sequence 	 by CH.	/. Let m be the number of accesses in 	.
a. Argue that if heuristic H does not know the access sequence in advance, then
the worst-case cost for H on an access sequence 	 is CH.	/ D .mn/.
With the move-to-front heuristic, immediately after searching for an element x,
we move x to the ﬁrst position on the list (i.e., the front of the list).
Let rankL.x/ denote the rank of element x in list L, that is, the position of x in
list L. For example, if x is the fourth element in L, then rankL.x/ D 4. Let ci
denote the cost of access 	i using the move-to-front heuristic, which includes the
cost of ﬁnding the element in the list and the cost of moving it to the front of the
list by a series of transpositions of adjacent list elements.
b. Show that if 	i accesses element x in list L using the move-to-front heuristic,
then ci D 2  rankL.x/  1.
Now we compare move-to-front with any other heuristic H that processes an
access sequence according to the two properties above. Heuristic H may transpose

Problems for Chapter 17
477
elements in the list in any way it wants, and it might even know the entire access
sequence in advance.
Let Li be the list after access 	i using move-to-front, and let L
i be the list after
access 	i using heuristic H. We denote the cost of access 	i by ci for move-to-
front and by c
i for heuristic H. Suppose that heuristic H performs t
i transpositions
during access 	i.
c. In part (b), you showed that ci D 2  rankLi1.x/  1. Now show that c
i D
rankL
i1.x/ C t
i .
We deﬁne an inversion in list Li as a pair of elements y and ´ such that y
precedes ´ in Li and ´ precedes y in list L
i . Suppose that list Li has qi inversions
after processing the access sequence h	1; 	2; : : : ; 	ii. Then, we deﬁne a potential
function ˆ that maps Li to a real number by ˆ.Li/ D 2qi. For example, if Li has
the elements he; c; a; d; bi and L
i has the elements hc; a; b; d; ei, then Li has 5
inversions (.e; c/; .e; a/; .e; d/; .e; b/; .d; b/), and so ˆ.Li/ D 10. Observe that
ˆ.Li/  0 for all i and that, if move-to-front and heuristic H start with the same
list L0, then ˆ.L0/ D 0.
d. Argue that a transposition either increases the potential by 2 or decreases the
potential by 2.
Suppose that access 	i ﬁnds the element x. To understand how the potential
changes due to 	i, let us partition the elements other than x into four sets, depend-
ing on where they are in the lists just before the ith access:

Set A consists of elements that precede x in both Li1 and L
i1.

Set B consists of elements that precede x in Li1 and follow x in L
i1.

Set C consists of elements that follow x in Li1 and precede x in L
i1.

Set D consists of elements that follow x in both Li1 and L
i1.
e. Argue that rankLi1.x/ D jAj C jBj C 1 and rankL
i1.x/ D jAj C jCj C 1.
f. Show that access 	i causes a change in potential of
ˆ.Li/  ˆ.Li1/  2.jAj  jBj C t
i / ;
where, as before, heuristic H performs t
i transpositions during access 	i.
Deﬁne the amortized cost yci of access 	i by yci D ci C ˆ.Li/  ˆ.Li1/.
g. Show that the amortized cost yci of access 	i is bounded from above by 4c
i .
h. Conclude that the cost CMTF.	/ of access sequence 	 with move-to-front is at
most 4 times the cost CH.	/ of 	 with any other heuristic H, assuming that
both heuristics start with the same list.

478
Chapter 17
Amortized Analysis
Chapter notes
Aho, Hopcroft, and Ullman [5] used aggregate analysis to determine the running
time of operations on a disjoint-set forest; we shall analyze this data structure us-
ing the potential method in Chapter 21. Tarjan [331] surveys the accounting and
potential methods of amortized analysis and presents several applications. He at-
tributes the accounting method to several authors, including M. R. Brown, R. E.
Tarjan, S. Huddleston, and K. Mehlhorn. He attributes the potential method to
D. D. Sleator. The term “amortized” is due to D. D. Sleator and R. E. Tarjan.
Potential functions are also useful for proving lower bounds for certain types of
problems. For each conﬁguration of the problem, we deﬁne a potential function
that maps the conﬁguration to a real number. Then we determine the potential ˆinit
of the initial conﬁguration, the potential ˆﬁnal of the ﬁnal conﬁguration, and the
maximum change in potential 
ˆmax due to any step. The number of steps must
therefore be at least jˆﬁnal  ˆinitj = j
ˆmaxj. Examples of potential functions to
prove lower bounds in I/O complexity appear in works by Cormen, Sundquist, and
Wisniewski [79]; Floyd [107]; and Aggarwal and Vitter [3]. Krumme, Cybenko,
and Venkataraman [221] applied potential functions to prove lower bounds on gos-
siping: communicating a unique item from each vertex in a graph to every other
vertex.
The move-to-front heuristic from Problem 17-5 works quite well in practice.
Moreover, if we recognize that when we ﬁnd an element, we can splice it out of its
position in the list and relocate it to the front of the list in constant time, we can
show that the cost of move-to-front is at most twice the cost of any other heuristic
including, again, one that knows the entire access sequence in advance.
