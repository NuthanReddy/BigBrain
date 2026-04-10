# 12 Binary Search Trees

12
Binary Search Trees
The search tree data structure supports many dynamic-set operations, including
SEARCH, MINIMUM, MAXIMUM, PREDECESSOR, SUCCESSOR, INSERT, and
DELETE. Thus, we can use a search tree both as a dictionary and as a priority
queue.
Basic operations on a binary search tree take time proportional to the height of
the tree. For a complete binary tree with n nodes, such operations run in ‚.lg n/
worst-case time. If the tree is a linear chain of n nodes, however, the same oper-
ations take ‚.n/ worst-case time. We shall see in Section 12.4 that the expected
height of a randomly built binary search tree is O.lg n/, so that basic dynamic-set
operations on such a tree take ‚.lg n/ time on average.
In practice, we can’t always guarantee that binary search trees are built ran-
domly, but we can design variations of binary search trees with good guaranteed
worst-case performance on basic operations. Chapter 13 presents one such vari-
ation, red-black trees, which have height O.lg n/. Chapter 18 introduces B-trees,
which are particularly good for maintaining databases on secondary (disk) storage.
After presenting the basic properties of binary search trees, the following sec-
tions show how to walk a binary search tree to print its values in sorted order, how
to search for a value in a binary search tree, how to ﬁnd the minimum or maximum
element, how to ﬁnd the predecessor or successor of an element, and how to insert
into or delete from a binary search tree. The basic mathematical properties of trees
appear in Appendix B.
12.1
What is a binary search tree?
A binary search tree is organized, as the name suggests, in a binary tree, as shown
in Figure 12.1. We can represent such a tree by a linked data structure in which
each node is an object. In addition to a key and satellite data, each node contains
attributes left, right, and p that point to the nodes corresponding to its left child,

12.1
What is a binary search tree?
287
5
2
5
5
8
7
6
(a)
6
8
7
5
2
(b)
Figure 12.1
Binary search trees. For any node x, the keys in the left subtree of x are at most x:key,
and the keys in the right subtree of x are at least x:key. Different binary search trees can represent
the same set of values. The worst-case running time for most search-tree operations is proportional
to the height of the tree. (a) A binary search tree on 6 nodes with height 2. (b) A less efﬁcient binary
search tree with height 4 that contains the same keys.
its right child, and its parent, respectively. If a child or the parent is missing, the
appropriate attribute contains the value NIL. The root node is the only node in the
tree whose parent is NIL.
The keys in a binary search tree are always stored in such a way as to satisfy the
binary-search-tree property:
Let x be a node in a binary search tree. If y is a node in the left subtree
of x, then y:key  x:key. If y is a node in the right subtree of x, then
y:key  x:key.
Thus, in Figure 12.1(a), the key of the root is 6, the keys 2, 5, and 5 in its left
subtree are no larger than 6, and the keys 7 and 8 in its right subtree are no smaller
than 6. The same property holds for every node in the tree. For example, the key 5
in the root’s left child is no smaller than the key 2 in that node’s left subtree and no
larger than the key 5 in the right subtree.
The binary-search-tree property allows us to print out all the keys in a binary
search tree in sorted order by a simple recursive algorithm, called an inorder tree
walk. This algorithm is so named because it prints the key of the root of a subtree
between printing the values in its left subtree and printing those in its right subtree.
(Similarly, a preorder tree walk prints the root before the values in either subtree,
and a postorder tree walk prints the root after the values in its subtrees.) To use
the following procedure to print all the elements in a binary search tree T , we call
INORDER-TREE-WALK.T:root/.

288
Chapter 12
Binary Search Trees
INORDER-TREE-WALK.x/
1
if x ¤ NIL
2
INORDER-TREE-WALK.x:left/
3
print x:key
4
INORDER-TREE-WALK.x:right/
As an example, the inorder tree walk prints the keys in each of the two binary
search trees from Figure 12.1 in the order 2; 5; 5; 6; 7; 8. The correctness of the
algorithm follows by induction directly from the binary-search-tree property.
It takes ‚.n/ time to walk an n-node binary search tree, since after the ini-
tial call, the procedure calls itself recursively exactly twice for each node in the
tree—once for its left child and once for its right child. The following theorem
gives a formal proof that it takes linear time to perform an inorder tree walk.
Theorem 12.1
If x is the root of an n-node subtree, then the call INORDER-TREE-WALK.x/
takes ‚.n/ time.
Proof
Let T .n/ denote the time taken by INORDER-TREE-WALK when it is
called on the root of an n-node subtree. Since INORDER-TREE-WALK visits all n
nodes of the subtree, we have T .n/ D .n/. It remains to show that T .n/ D O.n/.
Since INORDER-TREE-WALK takes a small, constant amount of time on an
empty subtree (for the test x ¤ NIL), we have T .0/ D c for some constant c > 0.
For n > 0, suppose that INORDER-TREE-WALK is called on a node x whose
left subtree has k nodes and whose right subtree has n  k  1 nodes. The time to
perform INORDER-TREE-WALK.x/ is bounded by T .n/  T .k/CT .nk1/Cd
for some constant d > 0 that reﬂects an upper bound on the time to execute the
body of INORDER-TREE-WALK.x/, exclusive of the time spent in recursive calls.
We use the substitution method to show that T .n/ D O.n/ by proving that
T .n/  .c Cd/nCc. For n D 0, we have .c Cd/0Cc D c D T .0/. For n > 0,
we have
T .n/

T .k/ C T .n  k  1/ C d
D
..c C d/k C c/ C ..c C d/.n  k  1/ C c/ C d
D
.c C d/n C c  .c C d/ C c C d
D
.c C d/n C c ;
which completes the proof.

12.2
Querying a binary search tree
289
Exercises
12.1-1
For the set of f1; 4; 5; 10; 16; 17; 21g of keys, draw binary search trees of heights 2,
3, 4, 5, and 6.
12.1-2
What is the difference between the binary-search-tree property and the min-heap
property (see page 153)? Can the min-heap property be used to print out the keys
of an n-node tree in sorted order in O.n/ time? Show how, or explain why not.
12.1-3
Give a nonrecursive algorithm that performs an inorder tree walk. (Hint: An easy
solution uses a stack as an auxiliary data structure. A more complicated, but ele-
gant, solution uses no stack but assumes that we can test two pointers for equality.)
12.1-4
Give recursive algorithms that perform preorder and postorder tree walks in ‚.n/
time on a tree of n nodes.
12.1-5
Argue that since sorting n elements takes .n lg n/ time in the worst case in
the comparison model, any comparison-based algorithm for constructing a binary
search tree from an arbitrary list of n elements takes .n lg n/ time in the worst
case.
12.2
Querying a binary search tree
We often need to search for a key stored in a binary search tree. Besides the
SEARCH operation, binary search trees can support such queries as MINIMUM,
MAXIMUM, SUCCESSOR, and PREDECESSOR. In this section, we shall examine
these operations and show how to support each one in time O.h/ on any binary
search tree of height h.
Searching
We use the following procedure to search for a node with a given key in a binary
search tree. Given a pointer to the root of the tree and a key k, TREE-SEARCH
returns a pointer to a node with key k if one exists; otherwise, it returns NIL.

290
Chapter 12
Binary Search Trees
2
4
3
13
7
6
17
20
18
15
9
Figure 12.2
Queries on a binary search tree. To search for the key 13 in the tree, we follow the path
15 ! 6 ! 7 ! 13 from the root. The minimum key in the tree is 2, which is found by following
left pointers from the root. The maximum key 20 is found by following right pointers from the root.
The successor of the node with key 15 is the node with key 17, since it is the minimum key in the
right subtree of 15. The node with key 13 has no right subtree, and thus its successor is its lowest
ancestor whose left child is also an ancestor. In this case, the node with key 15 is its successor.
TREE-SEARCH.x; k/
1
if x == NIL or k == x:key
2
return x
3
if k < x:key
4
return TREE-SEARCH.x:left; k/
5
else return TREE-SEARCH.x:right; k/
The procedure begins its search at the root and traces a simple path downward in
the tree, as shown in Figure 12.2. For each node x it encounters, it compares the
key k with x:key. If the two keys are equal, the search terminates. If k is smaller
than x:key, the search continues in the left subtree of x, since the binary-search-
tree property implies that k could not be stored in the right subtree. Symmetrically,
if k is larger than x:key, the search continues in the right subtree. The nodes
encountered during the recursion form a simple path downward from the root of
the tree, and thus the running time of TREE-SEARCH is O.h/, where h is the height
of the tree.
We can rewrite this procedure in an iterative fashion by “unrolling” the recursion
into a while loop. On most computers, the iterative version is more efﬁcient.

12.2
Querying a binary search tree
291
ITERATIVE-TREE-SEARCH.x; k/
1
while x ¤ NIL and k ¤ x:key
2
if k < x:key
3
x D x:left
4
else x D x:right
5
return x
Minimum and maximum
We can always ﬁnd an element in a binary search tree whose key is a minimum by
following left child pointers from the root until we encounter a NIL, as shown in
Figure 12.2. The following procedure returns a pointer to the minimum element in
the subtree rooted at a given node x, which we assume to be non-NIL:
TREE-MINIMUM.x/
1
while x:left ¤ NIL
2
x D x:left
3
return x
The binary-search-tree property guarantees that TREE-MINIMUM is correct. If a
node x has no left subtree, then since every key in the right subtree of x is at least as
large as x:key, the minimum key in the subtree rooted at x is x:key. If node x has
a left subtree, then since no key in the right subtree is smaller than x:key and every
key in the left subtree is not larger than x:key, the minimum key in the subtree
rooted at x resides in the subtree rooted at x:left.
The pseudocode for TREE-MAXIMUM is symmetric:
TREE-MAXIMUM.x/
1
while x:right ¤ NIL
2
x D x:right
3
return x
Both of these procedures run in O.h/ time on a tree of height h since, as in TREE-
SEARCH, the sequence of nodes encountered forms a simple path downward from
the root.
Successor and predecessor
Given a node in a binary search tree, sometimes we need to ﬁnd its successor in
the sorted order determined by an inorder tree walk. If all keys are distinct, the

292
Chapter 12
Binary Search Trees
successor of a node x is the node with the smallest key greater than x:key. The
structure of a binary search tree allows us to determine the successor of a node
without ever comparing keys. The following procedure returns the successor of a
node x in a binary search tree if it exists, and NIL if x has the largest key in the
tree:
TREE-SUCCESSOR.x/
1
if x:right ¤ NIL
2
return TREE-MINIMUM.x:right/
3
y D x:p
4
while y ¤ NIL and x == y:right
5
x D y
6
y D y:p
7
return y
We break the code for TREE-SUCCESSOR into two cases. If the right subtree
of node x is nonempty, then the successor of x is just the leftmost node in x’s
right subtree, which we ﬁnd in line 2 by calling TREE-MINIMUM.x:right/. For
example, the successor of the node with key 15 in Figure 12.2 is the node with
key 17.
On the other hand, as Exercise 12.2-6 asks you to show, if the right subtree of
node x is empty and x has a successor y, then y is the lowest ancestor of x whose
left child is also an ancestor of x. In Figure 12.2, the successor of the node with
key 13 is the node with key 15. To ﬁnd y, we simply go up the tree from x until we
encounter a node that is the left child of its parent; lines 3–7 of TREE-SUCCESSOR
handle this case.
The running time of TREE-SUCCESSOR on a tree of height h is O.h/, since we
either follow a simple path up the tree or follow a simple path down the tree. The
procedure TREE-PREDECESSOR, which is symmetric to TREE-SUCCESSOR, also
runs in time O.h/.
Even if keys are not distinct, we deﬁne the successor and predecessor of any
node x as the node returned by calls made to TREE-SUCCESSOR.x/ and TREE-
PREDECESSOR.x/, respectively.
In summary, we have proved the following theorem.
Theorem 12.2
We can implement the dynamic-set operations SEARCH, MINIMUM, MAXIMUM,
SUCCESSOR, and PREDECESSOR so that each one runs in O.h/ time on a binary
search tree of height h.

12.2
Querying a binary search tree
293
Exercises
12.2-1
Suppose that we have numbers between 1 and 1000 in a binary search tree, and we
want to search for the number 363. Which of the following sequences could not be
the sequence of nodes examined?
a. 2, 252, 401, 398, 330, 344, 397, 363.
b. 924, 220, 911, 244, 898, 258, 362, 363.
c. 925, 202, 911, 240, 912, 245, 363.
d. 2, 399, 387, 219, 266, 382, 381, 278, 363.
e. 935, 278, 347, 621, 299, 392, 358, 363.
12.2-2
Write recursive versions of TREE-MINIMUM and TREE-MAXIMUM.
12.2-3
Write the TREE-PREDECESSOR procedure.
12.2-4
Professor Bunyan thinks he has discovered a remarkable property of binary search
trees. Suppose that the search for key k in a binary search tree ends up in a leaf.
Consider three sets: A, the keys to the left of the search path; B, the keys on the
search path; and C, the keys to the right of the search path. Professor Bunyan
claims that any three keys a 2 A, b 2 B, and c 2 C must satisfy a  b  c. Give
a smallest possible counterexample to the professor’s claim.
12.2-5
Show that if a node in a binary search tree has two children, then its successor has
no left child and its predecessor has no right child.
12.2-6
Consider a binary search tree T whose keys are distinct. Show that if the right
subtree of a node x in T is empty and x has a successor y, then y is the lowest
ancestor of x whose left child is also an ancestor of x. (Recall that every node is
its own ancestor.)
12.2-7
An alternative method of performing an inorder tree walk of an n-node binary
search tree ﬁnds the minimum element in the tree by calling TREE-MINIMUM and
then making n  1 calls to TREE-SUCCESSOR. Prove that this algorithm runs
in ‚.n/ time.

294
Chapter 12
Binary Search Trees
12.2-8
Prove that no matter what node we start at in a height-h binary search tree, k
successive calls to TREE-SUCCESSOR take O.k C h/ time.
12.2-9
Let T be a binary search tree whose keys are distinct, let x be a leaf node, and let y
be its parent. Show that y:key is either the smallest key in T larger than x:key or
the largest key in T smaller than x:key.
12.3
Insertion and deletion
The operations of insertion and deletion cause the dynamic set represented by a
binary search tree to change. The data structure must be modiﬁed to reﬂect this
change, but in such a way that the binary-search-tree property continues to hold.
As we shall see, modifying the tree to insert a new element is relatively straight-
forward, but handling deletion is somewhat more intricate.
Insertion
To insert a new value  into a binary search tree T , we use the procedure TREE-
INSERT.
The procedure takes a node ´ for which ´:key D , ´:left D NIL,
and ´:right D NIL. It modiﬁes T and some of the attributes of ´ in such a way that
it inserts ´ into an appropriate position in the tree.
TREE-INSERT.T; ´/
1
y D NIL
2
x D T:root
3
while x ¤ NIL
4
y D x
5
if ´:key < x:key
6
x D x:left
7
else x D x:right
8
´:p D y
9
if y == NIL
10
T:root D ´
// tree T was empty
11
elseif ´:key < y:key
12
y:left D ´
13
else y:right D ´

12.3
Insertion and deletion
295
2
9
5
13
17
15
19
18
12
Figure 12.3
Inserting an item with key 13 into a binary search tree. Lightly shaded nodes indicate
the simple path from the root down to the position where the item is inserted. The dashed line
indicates the link in the tree that is added to insert the item.
Figure 12.3 shows how TREE-INSERT works. Just like the procedures TREE-
SEARCH and ITERATIVE-TREE-SEARCH, TREE-INSERT begins at the root of the
tree and the pointer x traces a simple path downward looking for a NIL to replace
with the input item ´. The procedure maintains the trailing pointer y as the parent
of x. After initialization, the while loop in lines 3–7 causes these two pointers
to move down the tree, going left or right depending on the comparison of ´:key
with x:key, until x becomes NIL. This NIL occupies the position where we wish to
place the input item ´. We need the trailing pointer y, because by the time we ﬁnd
the NIL where ´ belongs, the search has proceeded one step beyond the node that
needs to be changed. Lines 8–13 set the pointers that cause ´ to be inserted.
Like the other primitive operations on search trees, the procedure TREE-INSERT
runs in O.h/ time on a tree of height h.
Deletion
The overall strategy for deleting a node ´ from a binary search tree T has three
basic cases but, as we shall see, one of the cases is a bit tricky.

If ´ has no children, then we simply remove it by modifying its parent to re-
place ´ with NIL as its child.

If ´ has just one child, then we elevate that child to take ´’s position in the tree
by modifying ´’s parent to replace ´ by ´’s child.

If ´ has two children, then we ﬁnd ´’s successor y—which must be in ´’s right
subtree—and have y take ´’s position in the tree. The rest of ´’s original right
subtree becomes y’s new right subtree, and ´’s left subtree becomes y’s new
left subtree. This case is the tricky one because, as we shall see, it matters
whether y is ´’s right child.

296
Chapter 12
Binary Search Trees
The procedure for deleting a given node ´ from a binary search tree T takes as
arguments pointers to T and ´. It organizes its cases a bit differently from the three
cases outlined previously by considering the four cases shown in Figure 12.4.

If ´ has no left child (part (a) of the ﬁgure), then we replace ´ by its right child,
which may or may not be NIL. When ´’s right child is NIL, this case deals with
the situation in which ´ has no children. When ´’s right child is non-NIL, this
case handles the situation in which ´ has just one child, which is its right child.

If ´ has just one child, which is its left child (part (b) of the ﬁgure), then we
replace ´ by its left child.

Otherwise, ´ has both a left and a right child. We ﬁnd ´’s successor y, which
lies in ´’s right subtree and has no left child (see Exercise 12.2-5). We want to
splice y out of its current location and have it replace ´ in the tree.
 If y is ´’s right child (part (c)), then we replace ´ by y, leaving y’s right
child alone.
 Otherwise, y lies within ´’s right subtree but is not ´’s right child (part (d)).
In this case, we ﬁrst replace y by its own right child, and then we replace ´
by y.
In order to move subtrees around within the binary search tree, we deﬁne a
subroutine TRANSPLANT, which replaces one subtree as a child of its parent with
another subtree. When TRANSPLANT replaces the subtree rooted at node u with
the subtree rooted at node , node u’s parent becomes node ’s parent, and u’s
parent ends up having  as its appropriate child.
TRANSPLANT.T; u; /
1
if u:p == NIL
2
T:root D 
3
elseif u == u:p:left
4
u:p:left D 
5
else u:p:right D 
6
if  ¤ NIL
7
:p D u:p
Lines 1–2 handle the case in which u is the root of T . Otherwise, u is either a left
child or a right child of its parent. Lines 3–4 take care of updating u:p:left if u
is a left child, and line 5 updates u:p:right if u is a right child. We allow  to be
NIL, and lines 6–7 update :p if  is non-NIL. Note that TRANSPLANT does not
attempt to update :left and :right; doing so, or not doing so, is the responsibility
of TRANSPLANT’s caller.

12.3
Insertion and deletion
297
q
q
z
(a)
r
q
q
z
l
(b)
q
z
l
(c)
q
y
l
y
q
z
l
(d)
r
q
z
l
r
y
q
l
r
y
r
l
x
x
x
y
x
x
NIL
NIL
NIL
NIL
NIL
Figure 12.4
Deleting a node ´ from a binary search tree. Node ´ may be the root, a left child of
node q, or a right child of q. (a) Node ´ has no left child. We replace ´ by its right child r, which
may or may not be NIL. (b) Node ´ has a left child l but no right child. We replace ´ by l. (c) Node ´
has two children; its left child is node l, its right child is its successor y, and y’s right child is node x.
We replace ´ by y, updating y’s left child to become l, but leaving x as y’s right child. (d) Node ´
has two children (left child l and right child r), and its successor y ¤ r lies within the subtree rooted
at r. We replace y by its own right child x, and we set y to be r’s parent. Then, we set y to be q’s
child and the parent of l.

298
Chapter 12
Binary Search Trees
With the TRANSPLANT procedure in hand, here is the procedure that deletes
node ´ from binary search tree T :
TREE-DELETE.T; ´/
1
if ´:left == NIL
2
TRANSPLANT.T; ´; ´:right/
3
elseif ´:right == NIL
4
TRANSPLANT.T; ´; ´:left/
5
else y D TREE-MINIMUM.´:right/
6
if y:p ¤ ´
7
TRANSPLANT.T; y; y:right/
8
y:right D ´:right
9
y:right:p D y
10
TRANSPLANT.T; ´; y/
11
y:left D ´:left
12
y:left:p D y
The TREE-DELETE procedure executes the four cases as follows. Lines 1–2
handle the case in which node ´ has no left child, and lines 3–4 handle the case in
which ´ has a left child but no right child. Lines 5–12 deal with the remaining two
cases, in which ´ has two children. Line 5 ﬁnds node y, which is the successor
of ´. Because ´ has a nonempty right subtree, its successor must be the node in
that subtree with the smallest key; hence the call to TREE-MINIMUM.´:right/. As
we noted before, y has no left child. We want to splice y out of its current location,
and it should replace ´ in the tree. If y is ´’s right child, then lines 10–12 replace ´
as a child of its parent by y and replace y’s left child by ´’s left child. If y is
not ´’s left child, lines 7–9 replace y as a child of its parent by y’s right child and
turn ´’s right child into y’s right child, and then lines 10–12 replace ´ as a child of
its parent by y and replace y’s left child by ´’s left child.
Each line of TREE-DELETE, including the calls to TRANSPLANT, takes constant
time, except for the call to TREE-MINIMUM in line 5. Thus, TREE-DELETE runs
in O.h/ time on a tree of height h.
In summary, we have proved the following theorem.
Theorem 12.3
We can implement the dynamic-set operations INSERT and DELETE so that each
one runs in O.h/ time on a binary search tree of height h.

12.4
Randomly built binary search trees
299
Exercises
12.3-1
Give a recursive version of the TREE-INSERT procedure.
12.3-2
Suppose that we construct a binary search tree by repeatedly inserting distinct val-
ues into the tree. Argue that the number of nodes examined in searching for a
value in the tree is one plus the number of nodes examined when the value was
ﬁrst inserted into the tree.
12.3-3
We can sort a given set of n numbers by ﬁrst building a binary search tree contain-
ing these numbers (using TREE-INSERT repeatedly to insert the numbers one by
one) and then printing the numbers by an inorder tree walk. What are the worst-
case and best-case running times for this sorting algorithm?
12.3-4
Is the operation of deletion “commutative” in the sense that deleting x and then y
from a binary search tree leaves the same tree as deleting y and then x? Argue why
it is or give a counterexample.
12.3-5
Suppose that instead of each node x keeping the attribute x:p, pointing to x’s
parent, it keeps x:succ, pointing to x’s successor. Give pseudocode for SEARCH,
INSERT, and DELETE on a binary search tree T using this representation. These
procedures should operate in time O.h/, where h is the height of the tree T . (Hint:
You may wish to implement a subroutine that returns the parent of a node.)
12.3-6
When node ´ in TREE-DELETE has two children, we could choose node y as
its predecessor rather than its successor. What other changes to TREE-DELETE
would be necessary if we did so? Some have argued that a fair strategy, giving
equal priority to predecessor and successor, yields better empirical performance.
How might TREE-DELETE be changed to implement such a fair strategy?
?
12.4
Randomly built binary search trees
We have shown that each of the basic operations on a binary search tree runs
in O.h/ time, where h is the height of the tree. The height of a binary search

300
Chapter 12
Binary Search Trees
tree varies, however, as items are inserted and deleted. If, for example, the n items
are inserted in strictly increasing order, the tree will be a chain with height n  1.
On the other hand, Exercise B.5-4 shows that h  blg nc. As with quicksort, we
can show that the behavior of the average case is much closer to the best case than
to the worst case.
Unfortunately, little is known about the average height of a binary search tree
when both insertion and deletion are used to create it. When the tree is created
by insertion alone, the analysis becomes more tractable. Let us therefore deﬁne a
randomly built binary search tree on n keys as one that arises from inserting the
keys in random order into an initially empty tree, where each of the nŠ permutations
of the input keys is equally likely. (Exercise 12.4-3 asks you to show that this notion
is different from assuming that every binary search tree on n keys is equally likely.)
In this section, we shall prove the following theorem.
Theorem 12.4
The expected height of a randomly built binary search tree on n distinct keys is
O.lg n/.
Proof
We start by deﬁning three random variables that help measure the height
of a randomly built binary search tree. We denote the height of a randomly built
binary search on n keys by Xn, and we deﬁne the exponential height Yn D 2Xn.
When we build a binary search tree on n keys, we choose one key as that of the
root, and we let Rn denote the random variable that holds this key’s rank within
the set of n keys; that is, Rn holds the position that this key would occupy if the
set of keys were sorted. The value of Rn is equally likely to be any element of the
set f1; 2; : : : ; ng. If Rn D i, then the left subtree of the root is a randomly built
binary search tree on i  1 keys, and the right subtree is a randomly built binary
search tree on n  i keys. Because the height of a binary tree is 1 more than the
larger of the heights of the two subtrees of the root, the exponential height of a
binary tree is twice the larger of the exponential heights of the two subtrees of the
root. If we know that Rn D i, it follows that
Yn D 2  max.Yi1; Yni/ :
As base cases, we have that Y1 D 1, because the exponential height of a tree with 1
node is 20 D 1 and, for convenience, we deﬁne Y0 D 0.
Next, deﬁne indicator random variables Zn;1; Zn;2; : : : ; Zn;n, where
Zn;i D I fRn D ig :
Because Rn is equally likely to be any element of f1; 2; : : : ; ng, it follows that
Pr fRn D ig D 1=n for i D 1; 2; : : : ; n, and hence, by Lemma 5.1, we have
E ŒZn;i D 1=n ;
(12.1)

12.4
Randomly built binary search trees
301
for i D 1; 2; : : : ; n. Because exactly one value of Zn;i is 1 and all others are 0, we
also have
Yn D
n
X
iD1
Zn;i .2  max.Yi1; Yni// :
We shall show that E ŒYn is polynomial in n, which will ultimately imply that
E ŒXn D O.lg n/.
We claim that the indicator random variable Zn;i D I fRn D ig is independent
of the values of Yi1 and Yni. Having chosen Rn D i, the left subtree (whose
exponential height is Yi1) is randomly built on the i  1 keys whose ranks are
less than i. This subtree is just like any other randomly built binary search tree
on i  1 keys. Other than the number of keys it contains, this subtree’s structure
is not affected at all by the choice of Rn D i, and hence the random variables
Yi1 and Zn;i are independent. Likewise, the right subtree, whose exponential
height is Yni, is randomly built on the n  i keys whose ranks are greater than i.
Its structure is independent of the value of Rn, and so the random variables Yni
and Zn;i are independent. Hence, we have
E ŒYn
D
E
" n
X
iD1
Zn;i .2  max.Yi1; Yni//
#
D
n
X
iD1
E ŒZn;i .2  max.Yi1; Yni//
(by linearity of expectation)
D
n
X
iD1
E ŒZn;i E Œ2  max.Yi1; Yni/
(by independence)
D
n
X
iD1
1
n  E Œ2  max.Yi1; Yni/
(by equation (12.1))
D
2
n
n
X
iD1
E Œmax.Yi1; Yni/
(by equation (C.22))

2
n
n
X
iD1
.E ŒYi1 C E ŒYni/
(by Exercise C.3-4) .
Since each term E ŒY0 ; E ŒY1 ; : : : ; E ŒYn1 appears twice in the last summation,
once as E ŒYi1 and once as E ŒYni, we have the recurrence
E ŒYn  4
n
n1
X
iD0
E ŒYi :
(12.2)

302
Chapter 12
Binary Search Trees
Using the substitution method, we shall show that for all positive integers n, the
recurrence (12.2) has the solution
E ŒYn  1
4
 
n C 3
3
!
:
In doing so, we shall use the identity
n1
X
iD0
 
i C 3
3
!
D
 
n C 3
4
!
:
(12.3)
(Exercise 12.4-1 asks you to prove this identity.)
For the base cases, we note that the bounds 0 D Y0 D E ŒY0  .1=4/

3
3

D 1=4
and 1 D Y1 D E ŒY1  .1=4/

1C3
3

D 1 hold. For the inductive case, we have that
E ŒYn

4
n
n1
X
iD0
E ŒYi

4
n
n1
X
iD0
1
4
 
i C 3
3
!
(by the inductive hypothesis)
D
1
n
n1
X
iD0
 
i C 3
3
!
D
1
n
 
n C 3
4
!
(by equation (12.3))
D
1
n  .n C 3/Š
4Š .n  1/Š
D
1
4  .n C 3/Š
3Š nŠ
D
1
4
 
n C 3
3
!
:
We have bounded E ŒYn, but our ultimate goal is to bound E ŒXn. As Exer-
cise 12.4-4 asks you to show, the function f .x/ D 2x is convex (see page 1199).
Therefore, we can employ Jensen’s inequality (C.26), which says that
2EŒXn

E

2Xn
D
E ŒYn ;
as follows:
2EŒXn

1
4
 
n C 3
3
!

Problems for Chapter 12
303
D
1
4  .n C 3/.n C 2/.n C 1/
6
D
n3 C 6n2 C 11n C 6
24
:
Taking logarithms of both sides gives E ŒXn D O.lg n/.
Exercises
12.4-1
Prove equation (12.3).
12.4-2
Describe a binary search tree on n nodes such that the average depth of a node in
the tree is ‚.lg n/ but the height of the tree is !.lg n/. Give an asymptotic upper
bound on the height of an n-node binary search tree in which the average depth of
a node is ‚.lg n/.
12.4-3
Show that the notion of a randomly chosen binary search tree on n keys, where
each binary search tree of n keys is equally likely to be chosen, is different from
the notion of a randomly built binary search tree given in this section. (Hint: List
the possibilities when n D 3.)
12.4-4
Show that the function f .x/ D 2x is convex.
12.4-5
?
Consider RANDOMIZED-QUICKSORT operating on a sequence of n distinct input
numbers. Prove that for any constant k > 0, all but O.1=nk/ of the nŠ input
permutations yield an O.n lg n/ running time.
Problems
12-1
Binary search trees with equal keys
Equal keys pose a problem for the implementation of binary search trees.
a. What is the asymptotic performance of TREE-INSERT when used to insert n
items with identical keys into an initially empty binary search tree?
We propose to improve TREE-INSERT by testing before line 5 to determine whether
´:key D x:key and by testing before line 11 to determine whether ´:key D y:key.

304
Chapter 12
Binary Search Trees
If equality holds, we implement one of the following strategies. For each strategy,
ﬁnd the asymptotic performance of inserting n items with identical keys into an
initially empty binary search tree. (The strategies are described for line 5, in which
we compare the keys of ´ and x. Substitute y for x to arrive at the strategies for
line 11.)
b. Keep a boolean ﬂag x:b at node x, and set x to either x:left or x:right based
on the value of x:b, which alternates between FALSE and TRUE each time we
visit x while inserting a node with the same key as x.
c. Keep a list of nodes with equal keys at x, and insert ´ into the list.
d. Randomly set x to either x:left or x:right. (Give the worst-case performance
and informally derive the expected running time.)
12-2
Radix trees
Given two strings a D a0a1 : : : ap and b D b0b1 : : : bq, where each ai and each bj
is in some ordered set of characters, we say that string a is lexicographically less
than string b if either
1. there exists an integer j , where 0  j  min.p; q/, such that ai D bi for all
i D 0; 1; : : : ; j  1 and aj < bj, or
2. p < q and ai D bi for all i D 0; 1; : : : ; p.
For example, if a and b are bit strings, then 10100 < 10110 by rule 1 (letting
j D 3) and 10100 < 101000 by rule 2. This ordering is similar to that used in
English-language dictionaries.
The radix tree data structure shown in Figure 12.5 stores the bit strings 1011,
10, 011, 100, and 0. When searching for a key a D a0a1 : : : ap, we go left at a
node of depth i if ai D 0 and right if ai D 1. Let S be a set of distinct bit strings
whose lengths sum to n. Show how to use a radix tree to sort S lexicographically
in ‚.n/ time. For the example in Figure 12.5, the output of the sort should be the
sequence 0, 011, 10, 100, 1011.
12-3
Average node depth in a randomly built binary search tree
In this problem, we prove that the average depth of a node in a randomly built
binary search tree with n nodes is O.lg n/. Although this result is weaker than
that of Theorem 12.4, the technique we shall use reveals a surprising similarity
between the building of a binary search tree and the execution of RANDOMIZED-
QUICKSORT from Section 7.3.
We deﬁne the total path length P.T / of a binary tree T as the sum, over all
nodes x in T , of the depth of node x, which we denote by d.x; T /.

Problems for Chapter 12
305
011
0
100
10
1011
0
1
1
0
1
0
1
1
Figure 12.5
A radix tree storing the bit strings 1011, 10, 011, 100, and 0. We can determine each
node’s key by traversing the simple path from the root to that node. There is no need, therefore, to
store the keys in the nodes; the keys appear here for illustrative purposes only. Nodes are heavily
shaded if the keys corresponding to them are not in the tree; such nodes are present only to establish
a path to other nodes.
a. Argue that the average depth of a node in T is
1
n
X
x2T
d.x; T / D 1
nP.T / :
Thus, we wish to show that the expected value of P.T / is O.n lg n/.
b. Let TL and TR denote the left and right subtrees of tree T , respectively. Argue
that if T has n nodes, then
P.T / D P.TL/ C P.TR/ C n  1 :
c. Let P.n/ denote the average total path length of a randomly built binary search
tree with n nodes. Show that
P.n/ D 1
n
n1
X
iD0
.P.i/ C P.n  i  1/ C n  1/ :
d. Show how to rewrite P.n/ as
P.n/ D 2
n
n1
X
kD1
P.k/ C ‚.n/ :
e. Recalling the alternative analysis of the randomized version of quicksort given
in Problem 7-3, conclude that P.n/ D O.n lg n/.

306
Chapter 12
Binary Search Trees
At each recursive invocation of quicksort, we choose a random pivot element to
partition the set of elements being sorted. Each node of a binary search tree parti-
tions the set of elements that fall into the subtree rooted at that node.
f.
Describe an implementation of quicksort in which the comparisons to sort a set
of elements are exactly the same as the comparisons to insert the elements into
a binary search tree. (The order in which comparisons are made may differ, but
the same comparisons must occur.)
12-4
Number of different binary trees
Let bn denote the number of different binary trees with n nodes. In this problem,
you will ﬁnd a formula for bn, as well as an asymptotic estimate.
a. Show that b0 D 1 and that, for n  1,
bn D
n1
X
kD0
bkbn1k :
b. Referring to Problem 4-4 for the deﬁnition of a generating function, let B.x/
be the generating function
B.x/ D
1
X
nD0
bnxn :
Show that B.x/ D xB.x/2 C 1, and hence one way to express B.x/ in closed
form is
B.x/ D 1
2x

1 
p
1  4x

:
The Taylor expansion of f .x/ around the point x D a is given by
f .x/ D
1
X
kD0
f .k/.a/
kŠ
.x  a/k ;
where f .k/.x/ is the kth derivative of f evaluated at x.
c. Show that
bn D
1
n C 1
 
2n
n
!

Notes for Chapter 12
307
(the nth Catalan number) by using the Taylor expansion of
p
1  4x around
x D 0. (If you wish, instead of using the Taylor expansion, you may use
the generalization of the binomial expansion (C.4) to nonintegral exponents n,
where for any real number n and for any integer k, we interpret

n
k

to be
n.n  1/    .n  k C 1/=kŠ if k  0, and 0 otherwise.)
d. Show that
bn D
4n
pn3=2 .1 C O.1=n// :
Chapter notes
Knuth [211] contains a good discussion of simple binary search trees as well as
many variations. Binary search trees seem to have been independently discovered
by a number of people in the late 1950s. Radix trees are often called “tries,” which
comes from the middle letters in the word retrieval. Knuth [211] also discusses
them.
Many texts, including the ﬁrst two editions of this book, have a somewhat sim-
pler method of deleting a node from a binary search tree when both of its children
are present. Instead of replacing node ´ by its successor y, we delete node y but
copy its key and satellite data into node ´. The downside of this approach is that
the node actually deleted might not be the node passed to the delete procedure. If
other components of a program maintain pointers to nodes in the tree, they could
mistakenly end up with “stale” pointers to nodes that have been deleted. Although
the deletion method presented in this edition of this book is a bit more complicated,
it guarantees that a call to delete node ´ deletes node ´ and only node ´.
Section 15.5 will show how to construct an optimal binary search tree when
we know the search frequencies before constructing the tree. That is, given the
frequencies of searching for each key and the frequencies of searching for values
that fall between keys in the tree, we construct a binary search tree for which a
set of searches that follows these frequencies examines the minimum number of
nodes.
The proof in Section 12.4 that bounds the expected height of a randomly built
binary search tree is due to Aslam [24]. Mart´ınez and Roura [243] give randomized
algorithms for insertion into and deletion from binary search trees in which the
result of either operation is a random binary search tree. Their deﬁnition of a
random binary search tree differs—only slightly—from that of a randomly built
binary search tree in this chapter, however.
