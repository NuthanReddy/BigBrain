# 10 Elementary Data Structures

Elementary Data Structures
In this chapter, we examine the representation of dynamic sets by simple data structures that use pointers. Although we can construct many complex data structures
using pointers, we present only the rudimentary ones: stacks, queues, linked lists,
and rooted trees. We also show ways to synthesize objects and pointers from arrays.

## 10.1 Stacks and queues

Stacks and queues are dynamic sets in which the element removed from the set
by the DELETE operation is prespeciﬁed. In a stack, the element deleted from
the set is the one most recently inserted: the stack implements a last-in, ﬁrst-out,
or LIFO, policy. Similarly, in a queue, the element deleted is always the one that
has been in the set for the longest time: the queue implements a ﬁrst-in, ﬁrst-out,
or FIFO, policy. There are several efﬁcient ways to implement stacks and queues
on a computer. In this section we show how to use a simple array to implement
each.
Stacks
The INSERT operation on a stack is often called PUSH, and the DELETE operation, which does not take an element argument, is often called POP. These names
are allusions to physical stacks, such as the spring-loaded stacks of plates used
in cafeterias. The order in which plates are popped from the stack is the reverse
of the order in which they were pushed onto the stack, since only the top plate is
accessible.
As Figure 10.1 shows, we can implement a stack of at most n elements with
an array SŒ1 : : n. The array has an attribute S:top that indexes the most recently

## 10.1 Stacks and queues

S 15 6
S
15 6
9 17 3
S
15 6
9 17 3
(a)
(b)
(c)
S:top D 4
S:top D 6
S:top D 5
Figure 10.1
An array implementation of a stack S. Stack elements appear only in the lightly shaded
positions. (a) Stack S has 4 elements. The top element is 9. (b) Stack S after the calls PUSH.S; 17/
and PUSH.S; 3/. (c) Stack S after the call POP.S/ has returned the element 3, which is the one most
recently pushed. Although element 3 still appears in the array, it is no longer in the stack; the top is
element 17.
inserted element. The stack consists of elements SŒ1 : : S:top, where SŒ1 is the
element at the bottom of the stack and SŒS:top is the element at the top.
When S:top D 0, the stack contains no elements and is empty. We can test to
see whether the stack is empty by query operation STACK-EMPTY. If we attempt
to pop an empty stack, we say the stack underﬂows, which is normally an error.
If S:top exceeds n, the stack overﬂows. (In our pseudocode implementation, we
don’t worry about stack overﬂow.)
We can implement each of the stack operations with just a few lines of code:
STACK-EMPTY.S/
if S:top == 0
return TRUE
else return FALSE
PUSH.S; x/
S:top D S:top C 1
SŒS:top D x
POP.S/
if STACK-EMPTY.S/
error “underﬂow”
else S:top D S:top  1
return SŒS:top C 1
Figure 10.1 shows the effects of the modifying operations PUSH and POP. Each of
the three stack operations takes O.1/ time.

Q
(a)
15 6
Q
(b)
15 6
Q
(c)
15 6
Q:head D 7
Q:head D 7
Q:tail D 12
Q:tail D 3
Q:tail D 3
Q:head D 8
Figure 10.2
A queue implemented using an array QŒ1 : : 12. Queue elements appear only in the
lightly shaded positions. (a) The queue has 5 elements, in locations QŒ7 : : 11. (b) The conﬁguration
of the queue after the calls ENQUEUE.Q; 17/, ENQUEUE.Q; 3/, and ENQUEUE.Q; 5/. (c) The
conﬁguration of the queue after the call DEQUEUE.Q/ returns the key value 15 formerly at the
head of the queue. The new head has key 6.
Queues
We call the INSERT operation on a queue ENQUEUE, and we call the DELETE
operation DEQUEUE; like the stack operation POP, DEQUEUE takes no element argument. The FIFO property of a queue causes it to operate like a line of customers
waiting to pay a cashier. The queue has a head and a tail. When an element is enqueued, it takes its place at the tail of the queue, just as a newly arriving customer
takes a place at the end of the line. The element dequeued is always the one at
the head of the queue, like the customer at the head of the line who has waited the
longest.
Figure 10.2 shows one way to implement a queue of at most n  1 elements
using an array QŒ1 : : n. The queue has an attribute Q:head that indexes, or points
to, its head. The attribute Q:tail indexes the next location at which a newly arriving element will be inserted into the queue. The elements in the queue reside in
locations Q:head; Q:head C 1; : : : ; Q:tail  1, where we “wrap around” in the
sense that location 1 immediately follows location n in a circular order. When
Q:head D Q:tail, the queue is empty. Initially, we have Q:head D Q:tail D 1.
If we attempt to dequeue an element from an empty queue, the queue underﬂows.

## 10.1 Stacks and queues

When Q:head D Q:tail C 1, the queue is full, and if we attempt to enqueue an
element, then the queue overﬂows.
In our procedures ENQUEUE and DEQUEUE, we have omitted the error checking
for underﬂow and overﬂow. (Exercise 10.1-4 asks you to supply code that checks
for these two error conditions.) The pseudocode assumes that n D Q:length.
ENQUEUE.Q; x/
QŒQ:tail D x
if Q:tail == Q:length
Q:tail D 1
else Q:tail D Q:tail C 1
DEQUEUE.Q/
x D QŒQ:head
if Q:head == Q:length
Q:head D 1
else Q:head D Q:head C 1
return x
Figure 10.2 shows the effects of the ENQUEUE and DEQUEUE operations. Each
operation takes O.1/ time.

## Exercises

10.1-1
Using Figure 10.1 as a model, illustrate the result of each operation in the sequence
PUSH.S; 4/, PUSH.S; 1/, PUSH.S; 3/, POP.S/, PUSH.S; 8/, and POP.S/ on an
initially empty stack S stored in array SŒ1 : : 6.
10.1-2
Explain how to implement two stacks in one array AŒ1 : : n in such a way that
neither stack overﬂows unless the total number of elements in both stacks together
is n. The PUSH and POP operations should run in O.1/ time.
10.1-3
Using Figure 10.2 as a model, illustrate the result of each operation in the
sequence ENQUEUE.Q; 4/, ENQUEUE.Q; 1/, ENQUEUE.Q; 3/, DEQUEUE.Q/,
ENQUEUE.Q; 8/, and DEQUEUE.Q/ on an initially empty queue Q stored in
array QŒ1 : : 6.
10.1-4
Rewrite ENQUEUE and DEQUEUE to detect underﬂow and overﬂow of a queue.

10.1-5
Whereas a stack allows insertion and deletion of elements at only one end, and a
queue allows insertion at one end and deletion at the other end, a deque (doubleended queue) allows insertion and deletion at both ends. Write four O.1/-time
procedures to insert elements into and delete elements from both ends of a deque
implemented by an array.
10.1-6
Show how to implement a queue using two stacks. Analyze the running time of the
queue operations.
10.1-7
Show how to implement a stack using two queues. Analyze the running time of the
stack operations.

## 10.2 Linked lists

A linked list is a data structure in which the objects are arranged in a linear order.
Unlike an array, however, in which the linear order is determined by the array
indices, the order in a linked list is determined by a pointer in each object. Linked
lists provide a simple, ﬂexible representation for dynamic sets, supporting (though
not necessarily efﬁciently) all the operations listed on page 230.
As shown in Figure 10.3, each element of a doubly linked list L is an object with
an attribute key and two other pointer attributes: next and pre. The object may
also contain other satellite data. Given an element x in the list, x:next points to its
successor in the linked list, and x:pre points to its predecessor. If x:pre D NIL,
the element x has no predecessor and is therefore the ﬁrst element, or head, of
the list. If x:next D NIL, the element x has no successor and is therefore the last
element, or tail, of the list. An attribute L:head points to the ﬁrst element of the
list. If L:head D NIL, the list is empty.
A list may have one of several forms. It may be either singly linked or doubly
linked, it may be sorted or not, and it may be circular or not. If a list is singly
linked, we omit the pre pointer in each element. If a list is sorted, the linear order
of the list corresponds to the linear order of keys stored in elements of the list; the
minimum element is then the head of the list, and the maximum element is the
tail. If the list is unsorted, the elements can appear in any order. In a circular list,
the pre pointer of the head of the list points to the tail, and the next pointer of
the tail of the list points to the head. We can think of a circular list as a ring of

## 10.2 Linked lists

prev
key
next
(a)
(b)
(c)
L:head
L:head
L:head
Figure 10.3
(a) A doubly linked list L representing the dynamic set f1; 4; 9; 16g. Each element in
the list is an object with attributes for the key and pointers (shown by arrows) to the next and previous
objects. The next attribute of the tail and the pre attribute of the head are NIL, indicated by a diagonal
slash. The attribute L:head points to the head. (b) Following the execution of LIST-INSERT.L; x/,
where x:key D 25, the linked list has a new object with key 25 as the new head. This new object
points to the old head with key 9. (c) The result of the subsequent call LIST-DELETE.L; x/, where x
points to the object with key 4.
elements. In the remainder of this section, we assume that the lists with which we
are working are unsorted and doubly linked.
Searching a linked list
The procedure LIST-SEARCH.L; k/ ﬁnds the ﬁrst element with key k in list L
by a simple linear search, returning a pointer to this element. If no object with
key k appears in the list, then the procedure returns NIL. For the linked list in
Figure 10.3(a), the call LIST-SEARCH.L; 4/ returns a pointer to the third element,
and the call LIST-SEARCH.L; 7/ returns NIL.
LIST-SEARCH.L; k/
x D L:head
while x ¤ NIL and x:key ¤ k
x D x:next
return x
To search a list of n objects, the LIST-SEARCH procedure takes ‚.n/ time in the
worst case, since it may have to search the entire list.
Inserting into a linked list
Given an element x whose key attribute has already been set, the LIST-INSERT
procedure “splices” x onto the front of the linked list, as shown in Figure 10.3(b).

LIST-INSERT.L; x/
x:next D L:head
if L:head ¤ NIL
L:head:pre D x
L:head D x
x:pre D NIL
(Recall that our attribute notation can cascade, so that L:head:pre denotes the
pre attribute of the object that L:head points to.) The running time for LISTINSERT on a list of n elements is O.1/.
Deleting from a linked list
The procedure LIST-DELETE removes an element x from a linked list L. It must
be given a pointer to x, and it then “splices” x out of the list by updating pointers.
If we wish to delete an element with a given key, we must ﬁrst call LIST-SEARCH
to retrieve a pointer to the element.
LIST-DELETE.L; x/
if x:pre ¤ NIL
x:pre:next D x:next
else L:head D x:next
if x:next ¤ NIL
x:next:pre D x:pre
Figure 10.3(c) shows how an element is deleted from a linked list. LIST-DELETE
runs in O.1/ time, but if we wish to delete an element with a given key, ‚.n/ time
is required in the worst case because we must ﬁrst call LIST-SEARCH to ﬁnd the
element.
Sentinels
The code for LIST-DELETE would be simpler if we could ignore the boundary
conditions at the head and tail of the list:
LIST-DELETE0.L; x/
x:pre:next D x:next
x:next:pre D x:pre
A sentinel is a dummy object that allows us to simplify boundary conditions. For
example, suppose that we provide with list L an object L:nil that represents NIL

## 10.2 Linked lists

(a)
(b)
(c)
(d)
L:nil
L:nil
L:nil
L:nil
Figure 10.4
A circular, doubly linked list with a sentinel. The sentinel L:nil appears between the
head and tail. The attribute L:head is no longer needed, since we can access the head of the list
by L:nil:next. (a) An empty list. (b) The linked list from Figure 10.3(a), with key 9 at the head and
key 1 at the tail. (c) The list after executing LIST-INSERT0.L; x/, where x:key D 25. The new object
becomes the head of the list. (d) The list after deleting the object with key 1. The new tail is the
object with key 4.
but has all the attributes of the other objects in the list. Wherever we have a reference to NIL in list code, we replace it by a reference to the sentinel L:nil. As
shown in Figure 10.4, this change turns a regular doubly linked list into a circular, doubly linked list with a sentinel, in which the sentinel L:nil lies between the
head and tail. The attribute L:nil:next points to the head of the list, and L:nil:pre
points to the tail. Similarly, both the next attribute of the tail and the pre attribute of the head point to L:nil. Since L:nil:next points to the head, we can
eliminate the attribute L:head altogether, replacing references to it by references
to L:nil:next. Figure 10.4(a) shows that an empty list consists of just the sentinel,
and both L:nil:next and L:nil:pre point to L:nil.
The code for LIST-SEARCH remains the same as before, but with the references
to NIL and L:head changed as speciﬁed above:
LIST-SEARCH0.L; k/
x D L:nil:next
while x ¤ L:nil and x:key ¤ k
x D x:next
return x
We use the two-line procedure LIST-DELETE0 from before to delete an element
from the list. The following procedure inserts an element into the list:

LIST-INSERT0.L; x/
x:next D L:nil:next
L:nil:next:pre D x
L:nil:next D x
x:pre D L:nil
Figure 10.4 shows the effects of LIST-INSERT0 and LIST-DELETE0 on a sample list.
Sentinels rarely reduce the asymptotic time bounds of data structure operations,
but they can reduce constant factors. The gain from using sentinels within loops
is usually a matter of clarity of code rather than speed; the linked list code, for
example, becomes simpler when we use sentinels, but we save only O.1/ time in
the LIST-INSERT0 and LIST-DELETE0 procedures. In other situations, however, the
use of sentinels helps to tighten the code in a loop, thus reducing the coefﬁcient of,
say, n or n2 in the running time.
We should use sentinels judiciously. When there are many small lists, the extra
storage used by their sentinels can represent signiﬁcant wasted memory. In this
book, we use sentinels only when they truly simplify the code.

## Exercises

10.2-1
Can you implement the dynamic-set operation INSERT on a singly linked list
in O.1/ time? How about DELETE?
10.2-2
Implement a stack using a singly linked list L. The operations PUSH and POP
should still take O.1/ time.
10.2-3
Implement a queue by a singly linked list L. The operations ENQUEUE and DEQUEUE should still take O.1/ time.
10.2-4
As written, each loop iteration in the LIST-SEARCH0 procedure requires two tests:
one for x ¤ L:nil and one for x:key ¤ k. Show how to eliminate the test for
x ¤ L:nil in each iteration.
10.2-5
Implement the dictionary operations INSERT, DELETE, and SEARCH using singly
linked, circular lists. What are the running times of your procedures?

## 10.3 Implementing pointers and objects

10.2-6
The dynamic-set operation UNION takes two disjoint sets S1 and S2 as input, and
it returns a set S D S1 [ S2 consisting of all the elements of S1 and S2. The
sets S1 and S2 are usually destroyed by the operation. Show how to support UNION
in O.1/ time using a suitable list data structure.
10.2-7
Give a ‚.n/-time nonrecursive procedure that reverses a singly linked list of n
elements. The procedure should use no more than constant storage beyond that
needed for the list itself.
10.2-8
?
Explain how to implement doubly linked lists using only one pointer value x:np per
item instead of the usual two (next and pre). Assume that all pointer values can be
interpreted as k-bit integers, and deﬁne x:np to be x:np D x:next XOR x:pre,
the k-bit “exclusive-or” of x:next and x:pre. (The value NIL is represented by 0.)
Be sure to describe what information you need to access the head of the list. Show
how to implement the SEARCH, INSERT, and DELETE operations on such a list.
Also show how to reverse such a list in O.1/ time.

## 10.3 Implementing pointers and objects

How do we implement pointers and objects in languages that do not provide them?
In this section, we shall see two ways of implementing linked data structures without an explicit pointer data type. We shall synthesize objects and pointers from
arrays and array indices.
A multiple-array representation of objects
We can represent a collection of objects that have the same attributes by using an
array for each attribute. As an example, Figure 10.5 shows how we can implement
the linked list of Figure 10.3(a) with three arrays. The array key holds the values
of the keys currently in the dynamic set, and the pointers reside in the arrays next
and pre. For a given array index x, the array entries keyŒx, nextŒx, and preŒx
represent an object in the linked list. Under this interpretation, a pointer x is simply
a common index into the key, next, and pre arrays.
In Figure 10.3(a), the object with key 4 follows the object with key 16 in the
linked list. In Figure 10.5, key 4 appears in keyŒ2, and key 16 appears in keyŒ5,
and so nextŒ5 D 2 and preŒ2 D 5. Although the constant NIL appears in the next

key
next
prev
L
Figure 10.5
The linked list of Figure 10.3(a) represented by the arrays key, next, and pre. Each
vertical slice of the arrays represents a single object. Stored pointers correspond to the array indices
shown at the top; the arrows show how to interpret them. Lightly shaded object positions contain list
elements. The variable L keeps the index of the head.
attribute of the tail and the pre attribute of the head, we usually use an integer
(such as 0 or 1) that cannot possibly represent an actual index into the arrays. A
variable L holds the index of the head of the list.
A single-array representation of objects
The words in a computer memory are typically addressed by integers from 0
to M  1, where M is a suitably large integer. In many programming languages,
an object occupies a contiguous set of locations in the computer memory. A pointer
is simply the address of the ﬁrst memory location of the object, and we can address
other memory locations within the object by adding an offset to the pointer.
We can use the same strategy for implementing objects in programming environments that do not provide explicit pointer data types. For example, Figure 10.6
shows how to use a single array A to store the linked list from Figures 10.3(a)
and 10.5. An object occupies a contiguous subarray AŒj : : k. Each attribute of
the object corresponds to an offset in the range from 0 to k  j , and a pointer to
the object is the index j . In Figure 10.6, the offsets corresponding to key, next, and
pre are 0, 1, and 2, respectively. To read the value of i:pre, given a pointer i, we
add the value i of the pointer to the offset 2, thus reading AŒi C 2.
The single-array representation is ﬂexible in that it permits objects of different
lengths to be stored in the same array. The problem of managing such a heterogeneous collection of objects is more difﬁcult than the problem of managing a homogeneous collection, where all objects have the same attributes. Since most of the
data structures we shall consider are composed of homogeneous elements, it will
be sufﬁcient for our purposes to use the multiple-array representation of objects.

## 10.3 Implementing pointers and objects

A
L
prev
next
key
Figure 10.6
The linked list of Figures 10.3(a) and 10.5 represented in a single array A. Each list
element is an object that occupies a contiguous subarray of length 3 within the array. The three
attributes key, next, and pre correspond to the offsets 0, 1, and 2, respectively, within each object.
A pointer to an object is the index of the ﬁrst element of the object. Objects containing list elements
are lightly shaded, and arrows show the list ordering.
Allocating and freeing objects
To insert a key into a dynamic set represented by a doubly linked list, we must allocate a pointer to a currently unused object in the linked-list representation. Thus,
it is useful to manage the storage of objects not currently used in the linked-list
representation so that one can be allocated. In some systems, a garbage collector is responsible for determining which objects are unused. Many applications,
however, are simple enough that they can bear responsibility for returning an unused object to a storage manager. We shall now explore the problem of allocating
and freeing (or deallocating) homogeneous objects using the example of a doubly
linked list represented by multiple arrays.
Suppose that the arrays in the multiple-array representation have length m and
that at some moment the dynamic set contains n  m elements. Then n objects
represent elements currently in the dynamic set, and the remaining mn objects are
free; the free objects are available to represent elements inserted into the dynamic
set in the future.
We keep the free objects in a singly linked list, which we call the free list. The
free list uses only the next array, which stores the next pointers within the list.
The head of the free list is held in the global variable free. When the dynamic
set represented by linked list L is nonempty, the free list may be intertwined with
list L, as shown in Figure 10.7. Note that each object in the representation is either
in list L or in the free list, but not in both.
The free list acts like a stack: the next object allocated is the last one freed. We
can use a list implementation of the stack operations PUSH and POP to implement
the procedures for allocating and freeing objects, respectively. We assume that the
global variable free used in the following procedures points to the ﬁrst element of
the free list.

key
next
prev
L
free
(a)
key
next
prev
L
free
(b)
key
next
prev
L
free
(c)
Figure 10.7
The effect of the ALLOCATE-OBJECT and FREE-OBJECT procedures. (a) The list
of Figure 10.5 (lightly shaded) and a free list (heavily shaded). Arrows show the free-list structure.
(b) The result of calling ALLOCATE-OBJECT./ (which returns index 4), setting keyŒ4 to 25, and
calling LIST-INSERT.L; 4/. The new free-list head is object 8, which had been nextŒ4 on the free
list. (c) After executing LIST-DELETE.L; 5/, we call FREE-OBJECT.5/. Object 5 becomes the new
free-list head, with object 8 following it on the free list.
ALLOCATE-OBJECT./
if free == NIL
error “out of space”
else x D free
free D x:next
return x
FREE-OBJECT.x/
x:next D free
free D x
The free list initially contains all n unallocated objects. Once the free list has been
exhausted, running the ALLOCATE-OBJECT procedure signals an error. We can
even service several linked lists with just a single free list. Figure 10.8 shows two
linked lists and a free list intertwined through key, next, and pre arrays.
The two procedures run in O.1/ time, which makes them quite practical. We
can modify them to work for any homogeneous collection of objects by letting any
one of the attributes in the object act like a next attribute in the free list.

## 10.3 Implementing pointers and objects

next
key
prev
free
L2
L1
k1 k2 k3
k5 k6 k7
k9
Figure 10.8
Two linked lists, L1 (lightly shaded) and L2 (heavily shaded), and a free list (darkened) intertwined.

## Exercises

10.3-1
Draw a picture of the sequence h13; 4; 8; 19; 5; 11i stored as a doubly linked list
using the multiple-array representation. Do the same for the single-array representation.
10.3-2
Write the procedures ALLOCATE-OBJECT and FREE-OBJECT for a homogeneous
collection of objects implemented by the single-array representation.
10.3-3
Why don’t we need to set or reset the pre attributes of objects in the implementation of the ALLOCATE-OBJECT and FREE-OBJECT procedures?
10.3-4
It is often desirable to keep all elements of a doubly linked list compact in storage,
using, for example, the ﬁrst m index locations in the multiple-array representation.
(This is the case in a paged, virtual-memory computing environment.) Explain
how to implement the procedures ALLOCATE-OBJECT and FREE-OBJECT so that
the representation is compact. Assume that there are no pointers to elements of the
linked list outside the list itself. (Hint: Use the array implementation of a stack.)
10.3-5
Let L be a doubly linked list of length n stored in arrays key, pre, and next of
length m. Suppose that these arrays are managed by ALLOCATE-OBJECT and
FREE-OBJECT procedures that keep a doubly linked free list F . Suppose further
that of the m items, exactly n are on list L and m  n are on the free list. Write
a procedure COMPACTIFY-LIST.L; F / that, given the list L and the free list F ,
moves the items in L so that they occupy array positions 1; 2; : : : ; n and adjusts the
free list F so that it remains correct, occupying array positions nC1; nC2; : : : ; m.
The running time of your procedure should be ‚.n/, and it should use only a
constant amount of extra space. Argue that your procedure is correct.

## 10.4 Representing rooted trees

The methods for representing lists given in the previous section extend to any homogeneous data structure. In this section, we look speciﬁcally at the problem of
representing rooted trees by linked data structures. We ﬁrst look at binary trees,
and then we present a method for rooted trees in which nodes can have an arbitrary
number of children.
We represent each node of a tree by an object. As with linked lists, we assume
that each node contains a key attribute. The remaining attributes of interest are
pointers to other nodes, and they vary according to the type of tree.
Binary trees
Figure 10.9 shows how we use the attributes p, left, and right to store pointers to
the parent, left child, and right child of each node in a binary tree T . If x:p D NIL,
then x is the root. If node x has no left child, then x:left D NIL, and similarly for
the right child. The root of the entire tree T is pointed to by the attribute T:root. If
T:root D NIL, then the tree is empty.
Rooted trees with unbounded branching
We can extend the scheme for representing a binary tree to any class of trees in
which the number of children of each node is at most some constant k: we replace
the left and right attributes by child1; child2; : : : ; childk. This scheme no longer
works when the number of children of a node is unbounded, since we do not know
how many attributes (arrays in the multiple-array representation) to allocate in advance. Moreover, even if the number of children k is bounded by a large constant
but most nodes have a small number of children, we may waste a lot of memory.
Fortunately, there is a clever scheme to represent trees with arbitrary numbers of
children. It has the advantage of using only O.n/ space for any n-node rooted tree.
The left-child, right-sibling representation appears in Figure 10.10. As before,
each node contains a parent pointer p, and T:root points to the root of tree T .
Instead of having a pointer to each of its children, however, each node x has only
two pointers:
1. x:left-child points to the leftmost child of node x, and
2. x:right-sibling points to the sibling of x immediately to its right.
If node x has no children, then x:left-child D NIL, and if node x is the rightmost
child of its parent, then x:right-sibling D NIL.

## 10.4 Representing rooted trees

T:root
Figure 10.9
The representation of a binary tree T . Each node x has the attributes x:p (top), x:left
(lower left), and x:right (lower right). The key attributes are not shown.
T:root
Figure 10.10
The left-child, right-sibling representation of a tree T . Each node x has attributes x:p
(top), x:left-child (lower left), and x:right-sibling (lower right). The key attributes are not shown.

Other tree representations
We sometimes represent rooted trees in other ways. In Chapter 6, for example,
we represented a heap, which is based on a complete binary tree, by a single array
plus the index of the last node in the heap. The trees that appear in Chapter 21 are
traversed only toward the root, and so only the parent pointers are present; there
are no pointers to children. Many other schemes are possible. Which scheme is
best depends on the application.

## Exercises

10.4-1
Draw the binary tree rooted at index 6 that is represented by the following attributes:
index
key
left
right
NIL
NIL
NIL
NIL
NIL
NIL
NIL
NIL
NIL
NIL
10.4-2
Write an O.n/-time recursive procedure that, given an n-node binary tree, prints
out the key of each node in the tree.
10.4-3
Write an O.n/-time nonrecursive procedure that, given an n-node binary tree,
prints out the key of each node in the tree. Use a stack as an auxiliary data structure.
10.4-4
Write an O.n/-time procedure that prints all the keys of an arbitrary rooted tree
with n nodes, where the tree is stored using the left-child, right-sibling representation.
10.4-5
?
Write an O.n/-time nonrecursive procedure that, given an n-node binary tree,
prints out the key of each node. Use no more than constant extra space outside

Problems for Chapter 10
of the tree itself and do not modify the tree, even temporarily, during the procedure.
10.4-6
?
The left-child, right-sibling representation of an arbitrary rooted tree uses three
pointers in each node: left-child, right-sibling, and parent. From any node, its
parent can be reached and identiﬁed in constant time and all its children can be
reached and identiﬁed in time linear in the number of children. Show how to use
only two pointers and one boolean value in each node so that the parent of a node
or all of its children can be reached and identiﬁed in time linear in the number of
children.

## Problems

10-1
Comparisons among lists
For each of the four types of lists in the following table, what is the asymptotic
worst-case running time for each dynamic-set operation listed?
unsorted,
sorted,
unsorted,
sorted,
singly
singly
doubly
doubly
linked
linked
linked
linked
SEARCH.L; k/
INSERT.L; x/
DELETE.L; x/
SUCCESSOR.L; x/
PREDECESSOR.L; x/
MINIMUM.L/
MAXIMUM.L/

10-2
Mergeable heaps using linked lists
A mergeable heap supports the following operations: MAKE-HEAP (which creates
an empty mergeable heap), INSERT, MINIMUM, EXTRACT-MIN, and UNION.1
Show how to implement mergeable heaps using linked lists in each of the following
cases. Try to make each operation as efﬁcient as possible. Analyze the running
time of each operation in terms of the size of the dynamic set(s) being operated on.
a. Lists are sorted.
b. Lists are unsorted.
c. Lists are unsorted, and dynamic sets to be merged are disjoint.
10-3
Searching a sorted compact list
Exercise 10.3-4 asked how we might maintain an n-element list compactly in the
ﬁrst n positions of an array. We shall assume that all keys are distinct and that the
compact list is also sorted, that is, keyŒi < keyŒnextŒi for all i D 1; 2; : : : ; n such
that nextŒi ¤ NIL. We will also assume that we have a variable L that contains
the index of the ﬁrst element on the list. Under these assumptions, you will show
that we can use the following randomized algorithm to search the list in O.pn/
expected time.
COMPACT-LIST-SEARCH.L; n; k/
i D L
while i ¤ NIL and keyŒi < k
j D RANDOM.1; n/
if keyŒi < keyŒj  and keyŒj   k
i D j
if keyŒi == k
return i
i D nextŒi
if i == NIL or keyŒi > k
return NIL
else return i
If we ignore lines 3–7 of the procedure, we have an ordinary algorithm for
searching a sorted linked list, in which index i points to each position of the list in
1Because we have deﬁned a mergeable heap to support MINIMUM and EXTRACT-MIN, we can also
refer to it as a mergeable min-heap. Alternatively, if it supported MAXIMUM and EXTRACT-MAX,
it would be a mergeable max-heap.

Problems for Chapter 10
turn. The search terminates once the index i “falls off” the end of the list or once
keyŒi  k. In the latter case, if keyŒi D k, clearly we have found a key with the
value k. If, however, keyŒi > k, then we will never ﬁnd a key with the value k,
and so terminating the search was the right thing to do.
Lines 3–7 attempt to skip ahead to a randomly chosen position j . Such a skip
beneﬁts us if keyŒj  is larger than keyŒi and no larger than k; in such a case, j
marks a position in the list that i would have to reach during an ordinary list search.
Because the list is compact, we know that any choice of j between 1 and n indexes
some object in the list rather than a slot on the free list.
Instead of analyzing the performance of COMPACT-LIST-SEARCH directly, we
shall analyze a related algorithm, COMPACT-LIST-SEARCH0, which executes two
separate loops. This algorithm takes an additional parameter t which determines
an upper bound on the number of iterations of the ﬁrst loop.
COMPACT-LIST-SEARCH0.L; n; k; t/
i D L
for q D 1 to t
j D RANDOM.1; n/
if keyŒi < keyŒj  and keyŒj   k
i D j
if keyŒi == k
return i
while i ¤ NIL and keyŒi < k
i D nextŒi
if i == NIL or keyŒi > k
return NIL
else return i
To compare the execution of the algorithms COMPACT-LIST-SEARCH.L; n; k/
and COMPACT-LIST-SEARCH0.L; n; k; t/, assume that the sequence of integers returned by the calls of RANDOM.1; n/ is the same for both algorithms.
a. Suppose that COMPACT-LIST-SEARCH.L; n; k/ takes t iterations of the while
loop of lines 2–8. Argue that COMPACT-LIST-SEARCH0.L; n; k; t/ returns the
same answer and that the total number of iterations of both the for and while
loops within COMPACT-LIST-SEARCH0 is at least t.
In the call COMPACT-LIST-SEARCH0.L; n; k; t/, let Xt be the random variable that
describes the distance in the linked list (that is, through the chain of next pointers)
from position i to the desired key k after t iterations of the for loop of lines 2–7
have occurred.

b. Argue that the expected running time of COMPACT-LIST-SEARCH0.L; n; k; t/
is O.t C E ŒXt/.
c. Show that E ŒXt  Pn
rD1.1  r=n/t. (Hint: Use equation (C.25).)
d. Show that Pn1
rD0 rt  ntC1=.t C 1/.
e. Prove that E ŒXt  n=.t C 1/.
f.
Show that COMPACT-LIST-SEARCH0.L; n; k; t/ runs in O.t C n=t/ expected
time.
g. Conclude that COMPACT-LIST-SEARCH runs in O.pn/ expected time.
h. Why do we assume that all keys are distinct in COMPACT-LIST-SEARCH? Argue that random skips do not necessarily help asymptotically when the list contains repeated key values.
Chapter notes
Aho, Hopcroft, and Ullman [6] and Knuth [209] are excellent references for elementary data structures. Many other texts cover both basic data structures and their
implementation in a particular programming language. Examples of these types of
textbooks include Goodrich and Tamassia [147], Main [241], Shaffer [311], and
Weiss [352, 353, 354]. Gonnet [145] provides experimental data on the performance of many data-structure operations.
The origin of stacks and queues as data structures in computer science is unclear, since corresponding notions already existed in mathematics and paper-based
business practices before the introduction of digital computers. Knuth [209] cites
A. M. Turing for the development of stacks for subroutine linkage in 1947.
Pointer-based data structures also seem to be a folk invention. According to
Knuth, pointers were apparently used in early computers with drum memories. The
A-1 language developed by G. M. Hopper in 1951 represented algebraic formulas
as binary trees. Knuth credits the IPL-II language, developed in 1956 by A. Newell,
J. C. Shaw, and H. A. Simon, for recognizing the importance and promoting the
use of pointers. Their IPL-III language, developed in 1957, included explicit stack
operations.
