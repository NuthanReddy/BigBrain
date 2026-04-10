# III Data Structures

III
Data Structures

Introduction
Sets are as fundamental to computer science as they are to mathematics. Whereas
mathematical sets are unchanging, the sets manipulated by algorithms can grow,
shrink, or otherwise change over time. We call such sets dynamic. The next ﬁve
chapters present some basic techniques for representing ﬁnite dynamic sets and
manipulating them on a computer.
Algorithms may require several different types of operations to be performed on
sets. For example, many algorithms need only the ability to insert elements into,
delete elements from, and test membership in a set. We call a dynamic set that
supports these operations a dictionary. Other algorithms require more complicated
operations. For example, min-priority queues, which Chapter 6 introduced in the
context of the heap data structure, support the operations of inserting an element
into and extracting the smallest element from a set. The best way to implement a
dynamic set depends upon the operations that must be supported.
Elements of a dynamic set
In a typical implementation of a dynamic set, each element is represented by an
object whose attributes can be examined and manipulated if we have a pointer to
the object. (Section 10.3 discusses the implementation of objects and pointers in
programming environments that do not contain them as basic data types.) Some
kinds of dynamic sets assume that one of the object’s attributes is an identifying
key. If the keys are all different, we can think of the dynamic set as being a set
of key values. The object may contain satellite data, which are carried around in
other object attributes but are otherwise unused by the set implementation. It may

Part III
Data Structures
also have attributes that are manipulated by the set operations; these attributes may
contain data or pointers to other objects in the set.
Some dynamic sets presuppose that the keys are drawn from a totally ordered
set, such as the real numbers, or the set of all words under the usual alphabetic
ordering. A total ordering allows us to deﬁne the minimum element of the set, for
example, or to speak of the next element larger than a given element in a set.
Operations on dynamic sets
Operations on a dynamic set can be grouped into two categories: queries, which
simply return information about the set, and modifying operations, which change
the set. Here is a list of typical operations. Any speciﬁc application will usually
require only a few of these to be implemented.
SEARCH.S; k/
A query that, given a set S and a key value k, returns a pointer x to an element
in S such that x:key D k, or NIL if no such element belongs to S.
INSERT.S; x/
A modifying operation that augments the set S with the element pointed to
by x. We usually assume that any attributes in element x needed by the set
implementation have already been initialized.
DELETE.S; x/
A modifying operation that, given a pointer x to an element in the set S, removes x from S. (Note that this operation takes a pointer to an element x, not
a key value.)
MINIMUM.S/
A query on a totally ordered set S that returns a pointer to the element of S
with the smallest key.
MAXIMUM.S/
A query on a totally ordered set S that returns a pointer to the element of S
with the largest key.
SUCCESSOR.S; x/
A query that, given an element x whose key is from a totally ordered set S,
returns a pointer to the next larger element in S, or NIL if x is the maximum
element.
PREDECESSOR.S; x/
A query that, given an element x whose key is from a totally ordered set S,
returns a pointer to the next smaller element in S, or NIL if x is the minimum
element.

Part III
Data Structures
In some situations, we can extend the queries SUCCESSOR and PREDECESSOR
so that they apply to sets with nondistinct keys. For a set on n keys, the normal
presumption is that a call to MINIMUM followed by n  1 calls to SUCCESSOR
enumerates the elements in the set in sorted order.
We usually measure the time taken to execute a set operation in terms of the size
of the set. For example, Chapter 13 describes a data structure that can support any
of the operations listed above on a set of size n in time O.lg n/.
Overview of Part III
Chapters 10–14 describe several data structures that we can use to implement
dynamic sets; we shall use many of these later to construct efﬁcient algorithms
for a variety of problems. We already saw another important data structure—the
heap—in Chapter 6.
Chapter 10 presents the essentials of working with simple data structures such
as stacks, queues, linked lists, and rooted trees. It also shows how to implement
objects and pointers in programming environments that do not support them as
primitives. If you have taken an introductory programming course, then much of
this material should be familiar to you.
Chapter 11 introduces hash tables, which support the dictionary operations INSERT, DELETE, and SEARCH. In the worst case, hashing requires ‚.n/ time to perform a SEARCH operation, but the expected time for hash-table operations is O.1/.
The analysis of hashing relies on probability, but most of the chapter requires no
background in the subject.
Binary search trees, which are covered in Chapter 12, support all the dynamicset operations listed above. In the worst case, each operation takes ‚.n/ time on a
tree with n elements, but on a randomly built binary search tree, the expected time
for each operation is O.lg n/. Binary search trees serve as the basis for many other
data structures.
Chapter 13 introduces red-black trees, which are a variant of binary search trees.
Unlike ordinary binary search trees, red-black trees are guaranteed to perform well:
operations take O.lg n/ time in the worst case. A red-black tree is a balanced search
tree; Chapter 18 in Part V presents another kind of balanced search tree, called a
B-tree. Although the mechanics of red-black trees are somewhat intricate, you can
glean most of their properties from the chapter without studying the mechanics in
detail. Nevertheless, you probably will ﬁnd walking through the code to be quite
instructive.
In Chapter 14, we show how to augment red-black trees to support operations
other than the basic ones listed above. First, we augment them so that we can
dynamically maintain order statistics for a set of keys. Then, we augment them in
a different way to maintain intervals of real numbers.
