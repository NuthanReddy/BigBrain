# 6 Heapsort

In this chapter, we introduce another sorting algorithm: heapsort. Like merge sort, but unlike insertion sort, heapsort’s running time is O.n lg n/. Like insertion sort, but unlike merge sort, heapsort sorts in place: only a constant number of array elements are stored outside the input array at any time. Thus, heapsort combines the better attributes of the two sorting algorithms we have already discussed.

Heapsort also introduces another algorithm design technique: using a data structure, in this case one we call a “heap,” to manage information. Not only is the heap data structure useful for heapsort, but it also makes an efﬁcient priority queue. The heap data structure will reappear in algorithms in later chapters. The term “heap” was originally coined in the context of heapsort, but it has since come to refer to “garbage-collected storage,” such as the programming languages Java and Lisp provide. Our heap data structure is not garbage-collected storage, and whenever we refer to heaps in this book, we shall mean a data structure rather than an aspect of garbage collection.

## 6.1 Heaps

The (binary) heap data structure is an array object that we can view as a nearly complete binary tree (see Section B.5.3), as shown in Figure 6.1. Each node of the tree corresponds to an element of the array. The tree is completely ﬁlled on all levels except possibly the lowest, which is ﬁlled from the left up to a point. An array A that represents a heap is an object with two attributes: A:length, which (as usual) gives the number of elements in the array, and A:heap-size, which represents how many elements in the heap are stored within array A. That is, although AŒ1 : : A:length may contain numbers, only the elements in AŒ1 : : A:heap-size, where 0  A:heap-size  A:length, are valid elements of the heap. The root of the tree is AŒ1, and given the index i of a node, we can easily compute the indices of its parent, left child, and right child:

(a) 16 14 10 8 (b) Figure 6.1 A max-heap viewed as (a) a binary tree and (b) an array. The number within the circle at each node in the tree is the value stored at that node. The number above a node is the corresponding index in the array. Above and below the array are lines showing parent-child relationships; parents are always to the left of their children. The tree has height three; the node at index 4 (with value 8) has height one.

PARENT.i/ return bi=2c LEFT.i/ return 2i RIGHT.i/ return 2i C 1 On most computers, the LEFT procedure can compute 2i in one instruction by simply shifting the binary representation of i left by one bit position. Similarly, the RIGHT procedure can quickly compute 2i C1 by shifting the binary representation of i left by one bit position and then adding in a 1 as the low-order bit. The PARENT procedure can compute bi=2c by shifting i right one bit position. Good implementations of heapsort often implement these procedures as “macros” or “inline” procedures. There are two kinds of binary heaps: max-heaps and min-heaps. In both kinds, the values in the nodes satisfy a heap property, the speciﬁcs of which depend on the kind of heap. In a max-heap, the max-heap property is that for every node i other than the root, AŒPARENT.i/  AŒi ; that is, the value of a node is at most the value of its parent. Thus, the largest element in a max-heap is stored at the root, and the subtree rooted at a node contains

## 6.1 Heaps

values no larger than that contained at the node itself. A min-heap is organized in the opposite way; the min-heap property is that for every node i other than the root, AŒPARENT.i/  AŒi : The smallest element in a min-heap is at the root.

For the heapsort algorithm, we use max-heaps. Min-heaps commonly implement priority queues, which we discuss in Section 6.5. We shall be precise in specifying whether we need a max-heap or a min-heap for any particular application, and when properties apply to either max-heaps or min-heaps, we just use the term “heap.” Viewing a heap as a tree, we deﬁne the height of a node in a heap to be the number of edges on the longest simple downward path from the node to a leaf, and we deﬁne the height of the heap to be the height of its root. Since a heap of n elements is based on a complete binary tree, its height is ‚.lg n/ (see Exercise 6.1-2). We shall see that the basic operations on heaps run in time at most proportional to the height of the tree and thus take O.lg n/ time. The remainder of this chapter presents some basic procedures and shows how they are used in a sorting algorithm and a priority-queue data structure.  The MAX-HEAPIFY procedure, which runs in O.lg n/ time, is the key to maintaining the max-heap property.  The BUILD-MAX-HEAP procedure, which runs in linear time, produces a maxheap from an unordered input array.  The HEAPSORT procedure, which runs in O.n lg n/ time, sorts an array in place.  The MAX-HEAP-INSERT, HEAP-EXTRACT-MAX, HEAP-INCREASE-KEY, and HEAP-MAXIMUM procedures, which run in O.lg n/ time, allow the heap data structure to implement a priority queue.

## Exercises

6.1-1 What are the minimum and maximum numbers of elements in a heap of height h? 6.1-2 Show that an n-element heap has height blg nc. 6.1-3 Show that in any subtree of a max-heap, the root of the subtree contains the largest value occurring anywhere in that subtree.

6.1-4 Where in a max-heap might the smallest element reside, assuming that all elements are distinct? 6.1-5 Is an array that is in sorted order a min-heap? 6.1-6 Is the array with values h23; 17; 14; 6; 13; 10; 1; 5; 7; 12i a max-heap? 6.1-7 Show that, with the array representation for storing an n-element heap, the leaves are the nodes indexed by bn=2c C 1; bn=2c C 2; : : : ; n.

## 6.2 Maintaining the heap property

In order to maintain the max-heap property, we call the procedure MAX-HEAPIFY. Its inputs are an array A and an index i into the array. When it is called, MAX- HEAPIFY assumes that the binary trees rooted at LEFT.i/ and RIGHT.i/ are maxheaps, but that AŒi might be smaller than its children, thus violating the max-heap property. MAX-HEAPIFY lets the value at AŒi “ﬂoat down” in the max-heap so that the subtree rooted at index i obeys the max-heap property.

MAX-HEAPIFY.A; i/ l D LEFT.i/ r D RIGHT.i/ if l  A:heap-size and AŒl > AŒi largest D l else largest D i if r  A:heap-size and AŒr > AŒlargest largest D r if largest ¤ i exchange AŒi with AŒlargest MAX-HEAPIFY.A; largest/ Figure 6.2 illustrates the action of MAX-HEAPIFY. At each step, the largest of the elements AŒi, AŒLEFT.i/, and AŒRIGHT.i/ is determined, and its index is stored in largest. If AŒi is largest, then the subtree rooted at node i is already a max-heap and the procedure terminates. Otherwise, one of the two children has the largest element, and AŒi is swapped with AŒlargest, which causes node i and its

## 6.2 Maintaining the heap property

(a) (b) (c) i i i Figure 6.2 The action of MAX-HEAPIFY.A; 2/, where A:heap-size D 10. (a) The initial con- ﬁguration, with AŒ2 at node i D 2 violating the max-heap property since it is not larger than both children. The max-heap property is restored for node 2 in (b) by exchanging AŒ2 with AŒ4, which destroys the max-heap property for node 4. The recursive call MAX-HEAPIFY.A; 4/ now has i D 4. After swapping AŒ4 with AŒ9, as shown in (c), node 4 is ﬁxed up, and the recursive call MAX-HEAPIFY.A; 9/ yields no further change to the data structure. children to satisfy the max-heap property. The node indexed by largest, however, now has the original value AŒi, and thus the subtree rooted at largest might violate the max-heap property. Consequently, we call MAX-HEAPIFY recursively on that subtree. The running time of MAX-HEAPIFY on a subtree of size n rooted at a given node i is the ‚.1/ time to ﬁx up the relationships among the elements AŒi, AŒLEFT.i/, and AŒRIGHT.i/, plus the time to run MAX-HEAPIFY on a subtree rooted at one of the children of node i (assuming that the recursive call occurs). The children’s subtrees each have size at most 2n=3—the worst case occurs when the bottom level of the tree is exactly half full—and therefore we can describe the running time of MAX-HEAPIFY by the recurrence T .n/  T .2n=3/ C ‚.1/ :

The solution to this recurrence, by case 2 of the master theorem (Theorem 4.1), is T .n/ D O.lg n/. Alternatively, we can characterize the running time of MAX- HEAPIFY on a node of height h as O.h/.

## Exercises

6.2-1 Using Figure 6.2 as a model, illustrate the operation of MAX-HEAPIFY.A; 3/ on the array A D h27; 17; 3; 16; 13; 10; 1; 5; 7; 12; 4; 8; 9; 0i. 6.2-2 Starting with the procedure MAX-HEAPIFY, write pseudocode for the procedure MIN-HEAPIFY.A; i/, which performs the corresponding manipulation on a minheap. How does the running time of MIN-HEAPIFY compare to that of MAX- HEAPIFY? 6.2-3 What is the effect of calling MAX-HEAPIFY.A; i/ when the element AŒi is larger than its children? 6.2-4 What is the effect of calling MAX-HEAPIFY.A; i/ for i > A:heap-size=2? 6.2-5 The code for MAX-HEAPIFY is quite efﬁcient in terms of constant factors, except possibly for the recursive call in line 10, which might cause some compilers to produce inefﬁcient code. Write an efﬁcient MAX-HEAPIFY that uses an iterative control construct (a loop) instead of recursion. 6.2-6 Show that the worst-case running time of MAX-HEAPIFY on a heap of size n is .lg n/. (Hint: For a heap with n nodes, give node values that cause MAX- HEAPIFY to be called recursively at every node on a simple path from the root down to a leaf.)

## 6.3 Building a heap

We can use the procedure MAX-HEAPIFY in a bottom-up manner to convert an array AŒ1 : : n, where n D A:length, into a max-heap. By Exercise 6.1-7, the elements in the subarray AŒ.bn=2cC1/ : : n are all leaves of the tree, and so each is

## 6.3 Building a heap

a 1-element heap to begin with. The procedure BUILD-MAX-HEAP goes through the remaining nodes of the tree and runs MAX-HEAPIFY on each one.

BUILD-MAX-HEAP.A/ A:heap-size D A:length for i D bA:length=2c downto 1 MAX-HEAPIFY.A; i/ Figure 6.3 shows an example of the action of BUILD-MAX-HEAP. To show why BUILD-MAX-HEAP works correctly, we use the following loop invariant:

At the start of each iteration of the for loop of lines 2–3, each node i C 1; i C 2; : : : ; n is the root of a max-heap. We need to show that this invariant is true prior to the ﬁrst loop iteration, that each iteration of the loop maintains the invariant, and that the invariant provides a useful property to show correctness when the loop terminates. Initialization: Prior to the ﬁrst iteration of the loop, i D bn=2c. Each node bn=2c C 1; bn=2c C 2; : : : ; n is a leaf and is thus the root of a trivial max-heap.

Maintenance: To see that each iteration maintains the loop invariant, observe that the children of node i are numbered higher than i. By the loop invariant, therefore, they are both roots of max-heaps. This is precisely the condition required for the call MAX-HEAPIFY.A; i/ to make node i a max-heap root. Moreover, the MAX-HEAPIFY call preserves the property that nodes i C 1; i C 2; : : : ; n are all roots of max-heaps. Decrementing i in the for loop update reestablishes the loop invariant for the next iteration.

Termination: At termination, i D 0. By the loop invariant, each node 1; 2; : : : ; n is the root of a max-heap. In particular, node 1 is. We can compute a simple upper bound on the running time of BUILD-MAX- HEAP as follows. Each call to MAX-HEAPIFY costs O.lg n/ time, and BUILD- MAX-HEAP makes O.n/ such calls. Thus, the running time is O.n lg n/. This upper bound, though correct, is not asymptotically tight. We can derive a tighter bound by observing that the time for MAX-HEAPIFY to run at a node varies with the height of the node in the tree, and the heights of most nodes are small. Our tighter analysis relies on the properties that an n-element heap has height blg nc (see Exercise 6.1-2) and at most ˙ n=2hC1 nodes of any height h (see Exercise 6.3-3). The time required by MAX-HEAPIFY when called on a node of height h is O.h/, and so we can express the total cost of BUILD-MAX-HEAP as being bounded from above by

(a) 16 9 10 14 8 (b) (c) (d) (e) (f) A i i i i i Figure 6.3 The operation of BUILD-MAX-HEAP, showing the data structure before the call to MAX-HEAPIFY in line 3 of BUILD-MAX-HEAP. (a) A 10-element input array A and the binary tree it represents. The ﬁgure shows that the loop index i refers to node 5 before the call MAX-HEAPIFY.A; i/. (b) The data structure that results. The loop index i for the next iteration refers to node 4. (c)–(e) Subsequent iterations of the for loop in BUILD-MAX-HEAP. Observe that whenever MAX-HEAPIFY is called on a node, the two subtrees of that node are both max-heaps. (f) The max-heap after BUILD-MAX-HEAP ﬁnishes.

## 6.4 The heapsort algorithm

blg nc X hD0 l n 2hC1 m O.h/ D O

n blg nc X hD0 h 2h ! : We evalaute the last summation by substituting x D 1=2 in the formula (A.8), yielding X hD0 h 2h D 1=2 .1  1=2/2 D 2 : Thus, we can bound the running time of BUILD-MAX-HEAP as O

n blg nc X hD0 h 2h !

D O

n X hD0 h 2h !

D O.n/ :

Hence, we can build a max-heap from an unordered array in linear time. We can build a min-heap by the procedure BUILD-MIN-HEAP, which is the same as BUILD-MAX-HEAP but with the call to MAX-HEAPIFY in line 3 replaced by a call to MIN-HEAPIFY (see Exercise 6.2-2). BUILD-MIN-HEAP produces a min-heap from an unordered linear array in linear time.

## Exercises

6.3-1 Using Figure 6.3 as a model, illustrate the operation of BUILD-MAX-HEAP on the array A D h5; 3; 17; 10; 84; 19; 6; 22; 9i. 6.3-2 Why do we want the loop index i in line 2 of BUILD-MAX-HEAP to decrease from bA:length=2c to 1 rather than increase from 1 to bA:length=2c? 6.3-3 Show that there are at most ˙ n=2hC1 nodes of height h in any n-element heap.

## 6.4 The heapsort algorithm

The heapsort algorithm starts by using BUILD-MAX-HEAP to build a max-heap on the input array AŒ1 : : n, where n D A:length. Since the maximum element of the array is stored at the root AŒ1, we can put it into its correct ﬁnal position

by exchanging it with AŒn. If we now discard node n from the heap—and we can do so by simply decrementing A:heap-size—we observe that the children of the root remain max-heaps, but the new root element might violate the max-heap property. All we need to do to restore the max-heap property, however, is call MAX-HEAPIFY.A; 1/, which leaves a max-heap in AŒ1 : : n  1. The heapsort algorithm then repeats this process for the max-heap of size n  1 down to a heap of size 2. (See Exercise 6.4-2 for a precise loop invariant.) HEAPSORT.A/ BUILD-MAX-HEAP.A/ for i D A:length downto 2 exchange AŒ1 with AŒi A:heap-size D A:heap-size  1 MAX-HEAPIFY.A; 1/ Figure 6.4 shows an example of the operation of HEAPSORT after line 1 has built the initial max-heap. The ﬁgure shows the max-heap before the ﬁrst iteration of the for loop of lines 2–5 and after each iteration. The HEAPSORT procedure takes time O.n lg n/, since the call to BUILD-MAX- HEAP takes time O.n/ and each of the n  1 calls to MAX-HEAPIFY takes time O.lg n/.

## Exercises

6.4-1 Using Figure 6.4 as a model, illustrate the operation of HEAPSORT on the array A D h5; 13; 2; 25; 7; 17; 20; 8; 4i. 6.4-2 Argue the correctness of HEAPSORT using the following loop invariant:

At the start of each iteration of the for loop of lines 2–5, the subarray AŒ1 : : i is a max-heap containing the i smallest elements of AŒ1 : : n, and the subarray AŒi C 1 : : n contains the n  i largest elements of AŒ1 : : n, sorted. 6.4-3 What is the running time of HEAPSORT on an array A of length n that is already sorted in increasing order? What about decreasing order? 6.4-4 Show that the worst-case running time of HEAPSORT is .n lg n/.

## 6.4 The heapsort algorithm

(a) (b) (c) (d) (e) (f) (g) (h) (i) (j) (k) 9 10 14 16 A i i i i i i i i i Figure 6.4 The operation of HEAPSORT. (a) The max-heap data structure just after BUILD-MAX- HEAP has built it in line 1. (b)–(j) The max-heap just after each call of MAX-HEAPIFY in line 5, showing the value of i at that time. Only lightly shaded nodes remain in the heap. (k) The resulting sorted array A.

6.4-5 ?

Show that when all elements are distinct, the best-case running time of HEAPSORT is .n lg n/.

## 6.5 Priority queues

Heapsort is an excellent algorithm, but a good implementation of quicksort, presented in Chapter 7, usually beats it in practice. Nevertheless, the heap data structure itself has many uses. In this section, we present one of the most popular applications of a heap: as an efﬁcient priority queue. As with heaps, priority queues come in two forms: max-priority queues and min-priority queues. We will focus here on how to implement max-priority queues, which are in turn based on maxheaps; Exercise 6.5-3 asks you to write the procedures for min-priority queues.

A priority queue is a data structure for maintaining a set S of elements, each with an associated value called a key. A max-priority queue supports the following operations:

INSERT.S; x/ inserts the element x into the set S, which is equivalent to the operation S D S [ fxg.

MAXIMUM.S/ returns the element of S with the largest key.

EXTRACT-MAX.S/ removes and returns the element of S with the largest key.

INCREASE-KEY.S; x; k/ increases the value of element x’s key to the new value k, which is assumed to be at least as large as x’s current key value.

Among their other applications, we can use max-priority queues to schedule jobs on a shared computer. The max-priority queue keeps track of the jobs to be performed and their relative priorities. When a job is ﬁnished or interrupted, the scheduler selects the highest-priority job from among those pending by calling EXTRACT-MAX. The scheduler can add a new job to the queue at any time by calling INSERT.

Alternatively, a min-priority queue supports the operations INSERT, MINIMUM, EXTRACT-MIN, and DECREASE-KEY. A min-priority queue can be used in an event-driven simulator. The items in the queue are events to be simulated, each with an associated time of occurrence that serves as its key. The events must be simulated in order of their time of occurrence, because the simulation of an event can cause other events to be simulated in the future. The simulation program calls EXTRACT-MIN at each step to choose the next event to simulate. As new events are produced, the simulator inserts them into the min-priority queue by calling INSERT.

## 6.5 Priority queues

We shall see other uses for min-priority queues, highlighting the DECREASE-KEY operation, in Chapters 23 and 24. Not surprisingly, we can use a heap to implement a priority queue. In a given application, such as job scheduling or event-driven simulation, elements of a priority queue correspond to objects in the application. We often need to determine which application object corresponds to a given priority-queue element, and vice versa.

When we use a heap to implement a priority queue, therefore, we often need to store a handle to the corresponding application object in each heap element. The exact makeup of the handle (such as a pointer or an integer) depends on the application. Similarly, we need to store a handle to the corresponding heap element in each application object. Here, the handle would typically be an array index.

Because heap elements change locations within the array during heap operations, an actual implementation, upon relocating a heap element, would also have to update the array index in the corresponding application object. Because the details of accessing application objects depend heavily on the application and its implementation, we shall not pursue them here, other than noting that in practice, these handles do need to be correctly maintained. Now we discuss how to implement the operations of a max-priority queue. The procedure HEAP-MAXIMUM implements the MAXIMUM operation in ‚.1/ time.

HEAP-MAXIMUM.A/ return AŒ1 The procedure HEAP-EXTRACT-MAX implements the EXTRACT-MAX operation. It is similar to the for loop body (lines 3–5) of the HEAPSORT procedure.

HEAP-EXTRACT-MAX.A/ if A:heap-size < 1 error “heap underﬂow” max D AŒ1 AŒ1 D AŒA:heap-size A:heap-size D A:heap-size  1 MAX-HEAPIFY.A; 1/ return max The running time of HEAP-EXTRACT-MAX is O.lg n/, since it performs only a constant amount of work on top of the O.lg n/ time for MAX-HEAPIFY. The procedure HEAP-INCREASE-KEY implements the INCREASE-KEY operation. An index i into the array identiﬁes the priority-queue element whose key we wish to increase. The procedure ﬁrst updates the key of element AŒi to its new value. Because increasing the key of AŒi might violate the max-heap property,

the procedure then, in a manner reminiscent of the insertion loop (lines 5–7) of INSERTION-SORT from Section 2.1, traverses a simple path from this node toward the root to ﬁnd a proper place for the newly increased key. As HEAP-INCREASE- KEY traverses this path, it repeatedly compares an element to its parent, exchanging their keys and continuing if the element’s key is larger, and terminating if the element’s key is smaller, since the max-heap property now holds. (See Exercise 6.5-5 for a precise loop invariant.) HEAP-INCREASE-KEY.A; i; key/ if key < AŒi error “new key is smaller than current key” AŒi D key while i > 1 and AŒPARENT.i/ < AŒi exchange AŒi with AŒPARENT.i/ i D PARENT.i/ Figure 6.5 shows an example of a HEAP-INCREASE-KEY operation. The running time of HEAP-INCREASE-KEY on an n-element heap is O.lg n/, since the path traced from the node updated in line 3 to the root has length O.lg n/. The procedure MAX-HEAP-INSERT implements the INSERT operation. It takes as an input the key of the new element to be inserted into max-heap A. The procedure ﬁrst expands the max-heap by adding to the tree a new leaf whose key is 1. Then it calls HEAP-INCREASE-KEY to set the key of this new node to its correct value and maintain the max-heap property.

MAX-HEAP-INSERT.A; key/ A:heap-size D A:heap-size C 1 AŒA:heap-size D 1 HEAP-INCREASE-KEY.A; A:heap-size; key/ The running time of MAX-HEAP-INSERT on an n-element heap is O.lg n/. In summary, a heap can support any priority-queue operation on a set of size n in O.lg n/ time.

## Exercises

6.5-1 Illustrate the operation of HEAP-EXTRACT-MAX on the heap A D h15; 13; 9; 5; 12; 8; 7; 4; 0; 6; 2; 1i.

## 6.5 Priority queues

(a) i (b) (c) i i (d) i Figure 6.5 The operation of HEAP-INCREASE-KEY. (a) The max-heap of Figure 6.4(a) with a node whose index is i heavily shaded. (b) This node has its key increased to 15. (c) After one iteration of the while loop of lines 4–6, the node and its parent have exchanged keys, and the index i moves up to the parent. (d) The max-heap after one more iteration of the while loop. At this point, AŒPARENT.i/  AŒi. The max-heap property now holds and the procedure terminates. 6.5-2 Illustrate the operation of MAX-HEAP-INSERT.A; 10/ on the heap A D h15;13;9; 5; 12; 8; 7; 4; 0; 6; 2; 1i. 6.5-3 Write pseudocode for the procedures HEAP-MINIMUM, HEAP-EXTRACT-MIN, HEAP-DECREASE-KEY, and MIN-HEAP-INSERT that implement a min-priority queue with a min-heap. 6.5-4 Why do we bother setting the key of the inserted node to 1 in line 2 of MAX- HEAP-INSERT when the next thing we do is increase its key to the desired value?

6.5-5 Argue the correctness of HEAP-INCREASE-KEY using the following loop invariant:

At the start of each iteration of the while loop of lines 4–6, the subarray AŒ1 : : A:heap-size satisﬁes the max-heap property, except that there may be one violation: AŒi may be larger than AŒPARENT.i/.

You may assume that the subarray AŒ1 : : A:heap-size satisﬁes the max-heap property at the time HEAP-INCREASE-KEY is called. 6.5-6 Each exchange operation on line 5 of HEAP-INCREASE-KEY typically requires three assignments. Show how to use the idea of the inner loop of INSERTION- SORT to reduce the three assignments down to just one assignment. 6.5-7 Show how to implement a ﬁrst-in, ﬁrst-out queue with a priority queue. Show how to implement a stack with a priority queue. (Queues and stacks are deﬁned in Section 10.1.) 6.5-8 The operation HEAP-DELETE.A; i/ deletes the item in node i from heap A. Give an implementation of HEAP-DELETE that runs in O.lg n/ time for an n-element max-heap. 6.5-9 Give an O.n lg k/-time algorithm to merge k sorted lists into one sorted list, where n is the total number of elements in all the input lists. (Hint: Use a minheap for k-way merging.)

## Problems

6-1 Building a heap using insertion We can build a heap by repeatedly calling MAX-HEAP-INSERT to insert the elements into the heap. Consider the following variation on the BUILD-MAX-HEAP procedure:

Problems for Chapter 6 BUILD-MAX-HEAP0.A/ A:heap-size D 1 for i D 2 to A:length MAX-HEAP-INSERT.A; AŒi/ a. Do the procedures BUILD-MAX-HEAP and BUILD-MAX-HEAP0 always create the same heap when run on the same input array? Prove that they do, or provide a counterexample. b. Show that in the worst case, BUILD-MAX-HEAP0 requires ‚.n lg n/ time to build an n-element heap. 6-2 Analysis of d-ary heaps A d-ary heap is like a binary heap, but (with one possible exception) non-leaf nodes have d children instead of 2 children. a. How would you represent a d-ary heap in an array? b. What is the height of a d-ary heap of n elements in terms of n and d? c. Give an efﬁcient implementation of EXTRACT-MAX in a d-ary max-heap. Analyze its running time in terms of d and n. d. Give an efﬁcient implementation of INSERT in a d-ary max-heap. Analyze its running time in terms of d and n. e. Give an efﬁcient implementation of INCREASE-KEY.A; i; k/, which ﬂags an error if k < AŒi, but otherwise sets AŒi D k and then updates the d-ary maxheap structure appropriately. Analyze its running time in terms of d and n. 6-3 Young tableaus An m 	 n Young tableau is an m 	 n matrix such that the entries of each row are in sorted order from left to right and the entries of each column are in sorted order from top to bottom. Some of the entries of a Young tableau may be 1, which we treat as nonexistent elements. Thus, a Young tableau can be used to hold r  mn ﬁnite numbers. a. Draw a 4	4 Young tableau containing the elements f9; 16; 3; 2; 4; 8; 5; 14; 12g. b. Argue that an m 	 n Young tableau Y is empty if Y Œ1; 1 D 1. Argue that Y is full (contains mn elements) if Y Œm; n < 1.

c. Give an algorithm to implement EXTRACT-MIN on a nonempty m 	 n Young tableau that runs in O.m C n/ time.

Your algorithm should use a recursive subroutine that solves an m 	 n problem by recursively solving either an .m  1/ 	 n or an m 	 .n  1/ subproblem. (Hint: Think about MAX- HEAPIFY.) Deﬁne T .p/, where p D m C n, to be the maximum running time of EXTRACT-MIN on any m 	 n Young tableau. Give and solve a recurrence for T .p/ that yields the O.m C n/ time bound. d. Show how to insert a new element into a nonfull m 	 n Young tableau in O.m C n/ time. e. Using no other sorting method as a subroutine, show how to use an n	n Young tableau to sort n2 numbers in O.n3/ time. f.

Give an O.m C n/-time algorithm to determine whether a given number is stored in a given m 	 n Young tableau.

Chapter notes The heapsort algorithm was invented by Williams [357], who also described how to implement a priority queue with a heap. The BUILD-MAX-HEAP procedure was suggested by Floyd [106]. We use min-heaps to implement min-priority queues in Chapters 16, 23, and 24. We also give an implementation with improved time bounds for certain operations in Chapter 19 and, assuming that the keys are drawn from a bounded set of nonnegative integers, Chapter 20. If the data are b-bit integers, and the computer memory consists of addressable b-bit words, Fredman and Willard [115] showed how to implement MINIMUM in O.1/ time and INSERT and EXTRACT-MIN in O. p lg n/ time. Thorup [337] has improved the O. p lg n/ bound to O.lg lg n/ time. This bound uses an amount of space unbounded in n, but it can be implemented in linear space by using randomized hashing. An important special case of priority queues occurs when the sequence of EXTRACT-MIN operations is monotone, that is, the values returned by successive EXTRACT-MIN operations are monotonically increasing over time. This case arises in several important applications, such as Dijkstra’s single-source shortestpaths algorithm, which we discuss in Chapter 24, and in discrete-event simulation. For Dijkstra’s algorithm it is particularly important that the DECREASE-KEY operation be implemented efﬁciently. For the monotone case, if the data are integers in the range 1; 2; : : : ; C, Ahuja, Mehlhorn, Orlin, and Tarjan [8] describe

Notes for Chapter 6 how to implement EXTRACT-MIN and INSERT in O.lg C/ amortized time (see Chapter 17 for more on amortized analysis) and DECREASE-KEY in O.1/ time, using a data structure called a radix heap. The O.lg C/ bound can be improved to O. p lg C/ using Fibonacci heaps (see Chapter 19) in conjunction with radix heaps. Cherkassky, Goldberg, and Silverstein [65] further improved the bound to O.lg1=3C C/ expected time by combining the multilevel bucketing structure of Denardo and Fox [85] with the heap of Thorup mentioned earlier. Raman [291] further improved these results to obtain a bound of O.min.lg1=4C C; lg1=3C n//, for any ﬁxed  > 0.
