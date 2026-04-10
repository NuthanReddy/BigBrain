# 11 Hash Tables

11
Hash Tables
Many applications require a dynamic set that supports only the dictionary opera-
tions INSERT, SEARCH, and DELETE. For example, a compiler that translates a
programming language maintains a symbol table, in which the keys of elements
are arbitrary character strings corresponding to identiﬁers in the language. A hash
table is an effective data structure for implementing dictionaries. Although search-
ing for an element in a hash table can take as long as searching for an element in a
linked list—‚.n/ time in the worst case—in practice, hashing performs extremely
well. Under reasonable assumptions, the average time to search for an element in
a hash table is O.1/.
A hash table generalizes the simpler notion of an ordinary array. Directly ad-
dressing into an ordinary array makes effective use of our ability to examine an
arbitrary position in an array in O.1/ time. Section 11.1 discusses direct address-
ing in more detail. We can take advantage of direct addressing when we can afford
to allocate an array that has one position for every possible key.
When the number of keys actually stored is small relative to the total number of
possible keys, hash tables become an effective alternative to directly addressing an
array, since a hash table typically uses an array of size proportional to the number
of keys actually stored. Instead of using the key as an array index directly, the array
index is computed from the key. Section 11.2 presents the main ideas, focusing on
“chaining” as a way to handle “collisions,” in which more than one key maps to the
same array index. Section 11.3 describes how we can compute array indices from
keys using hash functions. We present and analyze several variations on the basic
theme. Section 11.4 looks at “open addressing,” which is another way to deal with
collisions. The bottom line is that hashing is an extremely effective and practical
technique: the basic dictionary operations require only O.1/ time on the average.
Section 11.5 explains how “perfect hashing” can support searches in O.1/ worst-
case time, when the set of keys being stored is static (that is, when the set of keys
never changes once stored).

254
Chapter 11
Hash Tables
11.1
Direct-address tables
Direct addressing is a simple technique that works well when the universe U of
keys is reasonably small. Suppose that an application needs a dynamic set in which
each element has a key drawn from the universe U D f0; 1; : : : ; m  1g, where m
is not too large. We shall assume that no two elements have the same key.
To represent the dynamic set, we use an array, or direct-address table, denoted
by T Œ0 : : m  1, in which each position, or slot, corresponds to a key in the uni-
verse U . Figure 11.1 illustrates the approach; slot k points to an element in the set
with key k. If the set contains no element with key k, then T Œk D NIL.
The dictionary operations are trivial to implement:
DIRECT-ADDRESS-SEARCH.T; k/
1
return T Œk
DIRECT-ADDRESS-INSERT.T; x/
1
T Œx:key D x
DIRECT-ADDRESS-DELETE.T; x/
1
T Œx:key D NIL
Each of these operations takes only O.1/ time.
T
U
(universe of keys)
K
(actual
keys)
2
3
5
8
1
9
4
0
7
6
2
3
5
8
key
satellite data
2
0
1
3
4
5
6
7
8
9
Figure 11.1
How to implement a dynamic set by a direct-address table T . Each key in the universe
U D f0; 1; : : : ; 9g corresponds to an index in the table. The set K D f2; 3; 5; 8g of actual keys
determines the slots in the table that contain pointers to elements. The other slots, heavily shaded,
contain NIL.

11.1
Direct-address tables
255
For some applications, the direct-address table itself can hold the elements in the
dynamic set. That is, rather than storing an element’s key and satellite data in an
object external to the direct-address table, with a pointer from a slot in the table to
the object, we can store the object in the slot itself, thus saving space. We would
use a special key within an object to indicate an empty slot. Moreover, it is often
unnecessary to store the key of the object, since if we have the index of an object
in the table, we have its key. If keys are not stored, however, we must have some
way to tell whether the slot is empty.
Exercises
11.1-1
Suppose that a dynamic set S is represented by a direct-address table T of length m.
Describe a procedure that ﬁnds the maximum element of S. What is the worst-case
performance of your procedure?
11.1-2
A bit vector is simply an array of bits (0s and 1s). A bit vector of length m takes
much less space than an array of m pointers. Describe how to use a bit vector
to represent a dynamic set of distinct elements with no satellite data. Dictionary
operations should run in O.1/ time.
11.1-3
Suggest how to implement a direct-address table in which the keys of stored el-
ements do not need to be distinct and the elements can have satellite data. All
three dictionary operations (INSERT, DELETE, and SEARCH) should run in O.1/
time. (Don’t forget that DELETE takes as an argument a pointer to an object to be
deleted, not a key.)
11.1-4
?
We wish to implement a dictionary by using direct addressing on a huge array. At
the start, the array entries may contain garbage, and initializing the entire array
is impractical because of its size. Describe a scheme for implementing a direct-
address dictionary on a huge array. Each stored object should use O.1/ space;
the operations SEARCH, INSERT, and DELETE should take O.1/ time each; and
initializing the data structure should take O.1/ time. (Hint: Use an additional array,
treated somewhat like a stack whose size is the number of keys actually stored in
the dictionary, to help determine whether a given entry in the huge array is valid or
not.)

256
Chapter 11
Hash Tables
11.2
Hash tables
The downside of direct addressing is obvious: if the universe U is large, storing
a table T of size jU j may be impractical, or even impossible, given the memory
available on a typical computer. Furthermore, the set K of keys actually stored
may be so small relative to U that most of the space allocated for T would be
wasted.
When the set K of keys stored in a dictionary is much smaller than the uni-
verse U of all possible keys, a hash table requires much less storage than a direct-
address table. Speciﬁcally, we can reduce the storage requirement to ‚.jKj/ while
we maintain the beneﬁt that searching for an element in the hash table still requires
only O.1/ time. The catch is that this bound is for the average-case time, whereas
for direct addressing it holds for the worst-case time.
With direct addressing, an element with key k is stored in slot k. With hashing,
this element is stored in slot h.k/; that is, we use a hash function h to compute the
slot from the key k. Here, h maps the universe U of keys into the slots of a hash
table T Œ0 : : m  1:
h W U ! f0; 1; : : : ; m  1g ;
where the size m of the hash table is typically much less than jU j. We say that an
element with key k hashes to slot h.k/; we also say that h.k/ is the hash value of
key k. Figure 11.2 illustrates the basic idea. The hash function reduces the range
of array indices and hence the size of the array. Instead of a size of jU j, the array
can have size m.
T
U
(universe of keys)
K
(actual
keys)
0
m–1
k1
k2
k3
k4
k5
h(k1)
h(k4)
h(k3)
h(k2) = h(k5)
Figure 11.2
Using a hash function h to map keys to hash-table slots. Because keys k2 and k5 map
to the same slot, they collide.

11.2
Hash tables
257
T
U
(universe of keys)
K
(actual
keys)
k1
k2
k3
k4
k5
k6
k7
k8
k1
k2
k3
k4
k5
k6
k7
k8
Figure 11.3
Collision resolution by chaining. Each hash-table slot T Œj contains a linked list of
all the keys whose hash value is j. For example, h.k1/ D h.k4/ and h.k5/ D h.k7/ D h.k2/.
The linked list can be either singly or doubly linked; we show it as doubly linked because deletion is
faster that way.
There is one hitch: two keys may hash to the same slot. We call this situation
a collision. Fortunately, we have effective techniques for resolving the conﬂict
created by collisions.
Of course, the ideal solution would be to avoid collisions altogether. We might
try to achieve this goal by choosing a suitable hash function h. One idea is to
make h appear to be “random,” thus avoiding collisions or at least minimizing
their number. The very term “to hash,” evoking images of random mixing and
chopping, captures the spirit of this approach. (Of course, a hash function h must be
deterministic in that a given input k should always produce the same output h.k/.)
Because jU j > m, however, there must be at least two keys that have the same hash
value; avoiding collisions altogether is therefore impossible. Thus, while a well-
designed, “random”-looking hash function can minimize the number of collisions,
we still need a method for resolving the collisions that do occur.
The remainder of this section presents the simplest collision resolution tech-
nique, called chaining. Section 11.4 introduces an alternative method for resolving
collisions, called open addressing.
Collision resolution by chaining
In chaining, we place all the elements that hash to the same slot into the same
linked list, as Figure 11.3 shows. Slot j contains a pointer to the head of the list of
all stored elements that hash to j ; if there are no such elements, slot j contains NIL.

258
Chapter 11
Hash Tables
The dictionary operations on a hash table T are easy to implement when colli-
sions are resolved by chaining:
CHAINED-HASH-INSERT.T; x/
1
insert x at the head of list T Œh.x:key/
CHAINED-HASH-SEARCH.T; k/
1
search for an element with key k in list T Œh.k/
CHAINED-HASH-DELETE.T; x/
1
delete x from the list T Œh.x:key/
The worst-case running time for insertion is O.1/. The insertion procedure is fast
in part because it assumes that the element x being inserted is not already present in
the table; if necessary, we can check this assumption (at additional cost) by search-
ing for an element whose key is x:key before we insert. For searching, the worst-
case running time is proportional to the length of the list; we shall analyze this
operation more closely below. We can delete an element in O.1/ time if the lists
are doubly linked, as Figure 11.3 depicts. (Note that CHAINED-HASH-DELETE
takes as input an element x and not its key k, so that we don’t have to search for x
ﬁrst. If the hash table supports deletion, then its linked lists should be doubly linked
so that we can delete an item quickly. If the lists were only singly linked, then to
delete element x, we would ﬁrst have to ﬁnd x in the list T Œh.x:key/ so that we
could update the next attribute of x’s predecessor. With singly linked lists, both
deletion and searching would have the same asymptotic running times.)
Analysis of hashing with chaining
How well does hashing with chaining perform? In particular, how long does it take
to search for an element with a given key?
Given a hash table T with m slots that stores n elements, we deﬁne the load
factor ˛ for T as n=m, that is, the average number of elements stored in a chain.
Our analysis will be in terms of ˛, which can be less than, equal to, or greater
than 1.
The worst-case behavior of hashing with chaining is terrible: all n keys hash
to the same slot, creating a list of length n. The worst-case time for searching is
thus ‚.n/ plus the time to compute the hash function—no better than if we used
one linked list for all the elements. Clearly, we do not use hash tables for their
worst-case performance. (Perfect hashing, described in Section 11.5, does provide
good worst-case performance when the set of keys is static, however.)
The average-case performance of hashing depends on how well the hash func-
tion h distributes the set of keys to be stored among the m slots, on the average.

11.2
Hash tables
259
Section 11.3 discusses these issues, but for now we shall assume that any given
element is equally likely to hash into any of the m slots, independently of where
any other element has hashed to. We call this the assumption of simple uniform
hashing.
For j D 0; 1; : : : ; m  1, let us denote the length of the list T Œj  by nj, so that
n D n0 C n1 C    C nm1 ;
(11.1)
and the expected value of nj is E Œnj D ˛ D n=m.
We assume that O.1/ time sufﬁces to compute the hash value h.k/, so that
the time required to search for an element with key k depends linearly on the
length nh.k/ of the list T Œh.k/. Setting aside the O.1/ time required to compute
the hash function and to access slot h.k/, let us consider the expected number of
elements examined by the search algorithm, that is, the number of elements in the
list T Œh.k/ that the algorithm checks to see whether any have a key equal to k. We
shall consider two cases. In the ﬁrst, the search is unsuccessful: no element in the
table has key k. In the second, the search successfully ﬁnds an element with key k.
Theorem 11.1
In a hash table in which collisions are resolved by chaining, an unsuccessful search
takes average-case time ‚.1C˛/, under the assumption of simple uniform hashing.
Proof
Under the assumption of simple uniform hashing, any key k not already
stored in the table is equally likely to hash to any of the m slots. The expected time
to search unsuccessfully for a key k is the expected time to search to the end of
list T Œh.k/, which has expected length E Œnh.k/ D ˛. Thus, the expected number
of elements examined in an unsuccessful search is ˛, and the total time required
(including the time for computing h.k/) is ‚.1 C ˛/.
The situation for a successful search is slightly different, since each list is not
equally likely to be searched. Instead, the probability that a list is searched is pro-
portional to the number of elements it contains. Nonetheless, the expected search
time still turns out to be ‚.1 C ˛/.
Theorem 11.2
In a hash table in which collisions are resolved by chaining, a successful search
takes average-case time ‚.1C˛/, under the assumption of simple uniform hashing.
Proof
We assume that the element being searched for is equally likely to be any
of the n elements stored in the table. The number of elements examined during a
successful search for an element x is one more than the number of elements that

260
Chapter 11
Hash Tables
appear before x in x’s list. Because new elements are placed at the front of the
list, elements before x in the list were all inserted after x was inserted. To ﬁnd
the expected number of elements examined, we take the average, over the n ele-
ments x in the table, of 1 plus the expected number of elements added to x’s list
after x was added to the list. Let xi denote the ith element inserted into the ta-
ble, for i D 1; 2; : : : ; n, and let ki D xi:key. For keys ki and kj, we deﬁne the
indicator random variable Xij D I fh.ki/ D h.kj/g. Under the assumption of sim-
ple uniform hashing, we have Pr fh.ki/ D h.kj/g D 1=m, and so by Lemma 5.1,
E ŒXij D 1=m. Thus, the expected number of elements examined in a successful
search is
E
"
1
n
n
X
iD1
 
1 C
n
X
jDiC1
Xij
!#
D
1
n
n
X
iD1
 
1 C
n
X
jDiC1
E ŒXij
!
(by linearity of expectation)
D
1
n
n
X
iD1
 
1 C
n
X
jDiC1
1
m
!
D
1 C 1
nm
n
X
iD1
.n  i/
D
1 C 1
nm
 n
X
iD1
n 
n
X
iD1
i
!
D
1 C 1
nm

n2  n.n C 1/
2

(by equation (A.1))
D
1 C n  1
2m
D
1 C ˛
2  ˛
2n :
Thus, the total time required for a successful search (including the time for com-
puting the hash function) is ‚.2 C ˛=2  ˛=2n/ D ‚.1 C ˛/.
What does this analysis mean? If the number of hash-table slots is at least pro-
portional to the number of elements in the table, we have n D O.m/ and, con-
sequently, ˛ D n=m D O.m/=m D O.1/. Thus, searching takes constant time
on average. Since insertion takes O.1/ worst-case time and deletion takes O.1/
worst-case time when the lists are doubly linked, we can support all dictionary
operations in O.1/ time on average.

11.2
Hash tables
261
Exercises
11.2-1
Suppose we use a hash function h to hash n distinct keys into an array T of
length m. Assuming simple uniform hashing, what is the expected number of
collisions? More precisely, what is the expected cardinality of ffk; lg W k ¤ l and
h.k/ D h.l/g?
11.2-2
Demonstrate what happens when we insert the keys 5; 28; 19; 15; 20; 33; 12; 17; 10
into a hash table with collisions resolved by chaining. Let the table have 9 slots,
and let the hash function be h.k/ D k mod 9.
11.2-3
Professor Marley hypothesizes that he can obtain substantial performance gains by
modifying the chaining scheme to keep each list in sorted order. How does the pro-
fessor’s modiﬁcation affect the running time for successful searches, unsuccessful
searches, insertions, and deletions?
11.2-4
Suggest how to allocate and deallocate storage for elements within the hash table
itself by linking all unused slots into a free list. Assume that one slot can store
a ﬂag and either one element plus a pointer or two pointers. All dictionary and
free-list operations should run in O.1/ expected time. Does the free list need to be
doubly linked, or does a singly linked free list sufﬁce?
11.2-5
Suppose that we are storing a set of n keys into a hash table of size m. Show that if
the keys are drawn from a universe U with jU j > nm, then U has a subset of size n
consisting of keys that all hash to the same slot, so that the worst-case searching
time for hashing with chaining is ‚.n/.
11.2-6
Suppose we have stored n keys in a hash table of size m, with collisions resolved by
chaining, and that we know the length of each chain, including the length L of the
longest chain. Describe a procedure that selects a key uniformly at random from
among the keys in the hash table and returns it in expected time O.L  .1 C 1=˛//.

262
Chapter 11
Hash Tables
11.3
Hash functions
In this section, we discuss some issues regarding the design of good hash functions
and then present three schemes for their creation. Two of the schemes, hashing by
division and hashing by multiplication, are heuristic in nature, whereas the third
scheme, universal hashing, uses randomization to provide provably good perfor-
mance.
What makes a good hash function?
A good hash function satisﬁes (approximately) the assumption of simple uniform
hashing: each key is equally likely to hash to any of the m slots, independently of
where any other key has hashed to. Unfortunately, we typically have no way to
check this condition, since we rarely know the probability distribution from which
the keys are drawn. Moreover, the keys might not be drawn independently.
Occasionally we do know the distribution. For example, if we know that the
keys are random real numbers k independently and uniformly distributed in the
range 0  k < 1, then the hash function
h.k/ D bkmc
satisﬁes the condition of simple uniform hashing.
In practice, we can often employ heuristic techniques to create a hash function
that performs well. Qualitative information about the distribution of keys may be
useful in this design process. For example, consider a compiler’s symbol table, in
which the keys are character strings representing identiﬁers in a program. Closely
related symbols, such as pt and pts, often occur in the same program. A good
hash function would minimize the chance that such variants hash to the same slot.
A good approach derives the hash value in a way that we expect to be indepen-
dent of any patterns that might exist in the data. For example, the “division method”
(discussed in Section 11.3.1) computes the hash value as the remainder when the
key is divided by a speciﬁed prime number. This method frequently gives good
results, assuming that we choose a prime number that is unrelated to any patterns
in the distribution of keys.
Finally, we note that some applications of hash functions might require stronger
properties than are provided by simple uniform hashing. For example, we might
want keys that are “close” in some sense to yield hash values that are far apart.
(This property is especially desirable when we are using linear probing, deﬁned in
Section 11.4.) Universal hashing, described in Section 11.3.3, often provides the
desired properties.

11.3
Hash functions
263
Interpreting keys as natural numbers
Most hash functions assume that the universe of keys is the set N D f0; 1; 2; : : :g
of natural numbers. Thus, if the keys are not natural numbers, we ﬁnd a way to
interpret them as natural numbers. For example, we can interpret a character string
as an integer expressed in suitable radix notation. Thus, we might interpret the
identiﬁer pt as the pair of decimal integers .112; 116/, since p D 112 and t D 116
in the ASCII character set; then, expressed as a radix-128 integer, pt becomes
.112  128/ C 116 D 14452. In the context of a given application, we can usually
devise some such method for interpreting each key as a (possibly large) natural
number. In what follows, we assume that the keys are natural numbers.
11.3.1
The division method
In the division method for creating hash functions, we map a key k into one of m
slots by taking the remainder of k divided by m. That is, the hash function is
h.k/ D k mod m :
For example, if the hash table has size m D 12 and the key is k D 100, then
h.k/ D 4. Since it requires only a single division operation, hashing by division is
quite fast.
When using the division method, we usually avoid certain values of m. For
example, m should not be a power of 2, since if m D 2p, then h.k/ is just the p
lowest-order bits of k. Unless we know that all low-order p-bit patterns are equally
likely, we are better off designing the hash function to depend on all the bits of the
key. As Exercise 11.3-3 asks you to show, choosing m D 2p  1 when k is a
character string interpreted in radix 2p may be a poor choice, because permuting
the characters of k does not change its hash value.
A prime not too close to an exact power of 2 is often a good choice for m. For
example, suppose we wish to allocate a hash table, with collisions resolved by
chaining, to hold roughly n D 2000 character strings, where a character has 8 bits.
We don’t mind examining an average of 3 elements in an unsuccessful search, and
so we allocate a hash table of size m D 701. We could choose m D 701 because
it is a prime near 2000=3 but not near any power of 2. Treating each key k as an
integer, our hash function would be
h.k/ D k mod 701 :
11.3.2
The multiplication method
The multiplication method for creating hash functions operates in two steps. First,
we multiply the key k by a constant A in the range 0 < A < 1 and extract the

264
Chapter 11
Hash Tables
×
s D A  2w
w bits
k
r0
r1
h.k/
extract p bits
Figure 11.4
The multiplication method of hashing. The w-bit representation of the key k is multi-
plied by the w-bit value s D A  2w. The p highest-order bits of the lower w-bit half of the product
form the desired hash value h.k/.
fractional part of kA. Then, we multiply this value by m and take the ﬂoor of the
result. In short, the hash function is
h.k/ D bm .kA mod 1/c ;
where “kA mod 1” means the fractional part of kA, that is, kA  bkAc.
An advantage of the multiplication method is that the value of m is not critical.
We typically choose it to be a power of 2 (m D 2p for some integer p), since we
can then easily implement the function on most computers as follows. Suppose
that the word size of the machine is w bits and that k ﬁts into a single word. We
restrict A to be a fraction of the form s=2w, where s is an integer in the range
0 < s < 2w. Referring to Figure 11.4, we ﬁrst multiply k by the w-bit integer
s D A 2w. The result is a 2w-bit value r12w C r0, where r1 is the high-order word
of the product and r0 is the low-order word of the product. The desired p-bit hash
value consists of the p most signiﬁcant bits of r0.
Although this method works with any value of the constant A, it works better
with some values than with others. The optimal choice depends on the character-
istics of the data being hashed. Knuth [211] suggests that
A  .
p
5  1/=2 D 0:6180339887 : : :
(11.2)
is likely to work reasonably well.
As an example, suppose we have k D 123456, p D 14, m D 214 D 16384,
and w D 32. Adapting Knuth’s suggestion, we choose A to be the fraction of the
form s=232 that is closest to .
p
5  1/=2, so that A D 2654435769=232. Then
k  s D 327706022297664 D .76300  232/ C 17612864, and so r1 D 76300
and r0 D 17612864. The 14 most signiﬁcant bits of r0 yield the value h.k/ D 67.

11.3
Hash functions
265
?
11.3.3
Universal hashing
If a malicious adversary chooses the keys to be hashed by some ﬁxed hash function,
then the adversary can choose n keys that all hash to the same slot, yielding an av-
erage retrieval time of ‚.n/. Any ﬁxed hash function is vulnerable to such terrible
worst-case behavior; the only effective way to improve the situation is to choose
the hash function randomly in a way that is independent of the keys that are actually
going to be stored. This approach, called universal hashing, can yield provably
good performance on average, no matter which keys the adversary chooses.
In universal hashing, at the beginning of execution we select the hash function
at random from a carefully designed class of functions. As in the case of quick-
sort, randomization guarantees that no single input will always evoke worst-case
behavior. Because we randomly select the hash function, the algorithm can be-
have differently on each execution, even for the same input, guaranteeing good
average-case performance for any input. Returning to the example of a compiler’s
symbol table, we ﬁnd that the programmer’s choice of identiﬁers cannot now cause
consistently poor hashing performance. Poor performance occurs only when the
compiler chooses a random hash function that causes the set of identiﬁers to hash
poorly, but the probability of this situation occurring is small and is the same for
any set of identiﬁers of the same size.
Let H be a ﬁnite collection of hash functions that map a given universe U of
keys into the range f0; 1; : : : ; m  1g. Such a collection is said to be universal
if for each pair of distinct keys k; l 2 U , the number of hash functions h 2 H
for which h.k/ D h.l/ is at most jHj =m. In other words, with a hash function
randomly chosen from H, the chance of a collision between distinct keys k and l
is no more than the chance 1=m of a collision if h.k/ and h.l/ were randomly and
independently chosen from the set f0; 1; : : : ; m  1g.
The following theorem shows that a universal class of hash functions gives good
average-case behavior. Recall that ni denotes the length of list T Œi.
Theorem 11.3
Suppose that a hash function h is chosen randomly from a universal collection of
hash functions and has been used to hash n keys into a table T of size m, us-
ing chaining to resolve collisions. If key k is not in the table, then the expected
length E Œnh.k/ of the list that key k hashes to is at most the load factor ˛ D n=m.
If key k is in the table, then the expected length E Œnh.k/ of the list containing key k
is at most 1 C ˛.
Proof
We note that the expectations here are over the choice of the hash func-
tion and do not depend on any assumptions about the distribution of the keys.
For each pair k and l of distinct keys, deﬁne the indicator random variable

266
Chapter 11
Hash Tables
Xkl D I fh.k/ D h.l/g. Since by the deﬁnition of a universal collection of hash
functions, a single pair of keys collides with probability at most 1=m, we have
Pr fh.k/ D h.l/g  1=m. By Lemma 5.1, therefore, we have E ŒXkl  1=m.
Next we deﬁne, for each key k, the random variable Yk that equals the number
of keys other than k that hash to the same slot as k, so that
Yk D
X
l2T
l¤k
Xkl :
Thus we have
E ŒYk
D
E
2
4
X
l2T
l¤k
Xkl
3
5
D
X
l2T
l¤k
E ŒXkl
(by linearity of expectation)

X
l2T
l¤k
1
m :
The remainder of the proof depends on whether key k is in table T .

If k 62 T , then nh.k/ D Yk and jfl W l 2 T and l ¤ kgj D n. Thus E Œnh.k/ D
E ŒYk  n=m D ˛.

If k 2 T , then because key k appears in list T Œh.k/ and the count Yk does not
include key k, we have nh.k/ D Yk C 1 and jfl W l 2 T and l ¤ kgj D n  1.
Thus E Œnh.k/ D E ŒYk C 1  .n  1/=m C 1 D 1 C ˛  1=m < 1 C ˛.
The following corollary says universal hashing provides the desired payoff: it
has now become impossible for an adversary to pick a sequence of operations that
forces the worst-case running time. By cleverly randomizing the choice of hash
function at run time, we guarantee that we can process every sequence of operations
with a good average-case running time.
Corollary 11.4
Using universal hashing and collision resolution by chaining in an initially empty
table with m slots, it takes expected time ‚.n/ to handle any sequence of n INSERT,
SEARCH, and DELETE operations containing O.m/ INSERT operations.
Proof
Since the number of insertions is O.m/, we have n D O.m/ and so
˛ D O.1/. The INSERT and DELETE operations take constant time and, by The-
orem 11.3, the expected time for each SEARCH operation is O.1/. By linearity of

11.3
Hash functions
267
expectation, therefore, the expected time for the entire sequence of n operations
is O.n/. Since each operation takes .1/ time, the ‚.n/ bound follows.
Designing a universal class of hash functions
It is quite easy to design a universal class of hash functions, as a little number
theory will help us prove. You may wish to consult Chapter 31 ﬁrst if you are
unfamiliar with number theory.
We begin by choosing a prime number p large enough so that every possible
key k is in the range 0 to p  1, inclusive. Let Zp denote the set f0; 1; : : : ; p  1g,
and let Z
p denote the set f1; 2; : : : ; p  1g. Since p is prime, we can solve equa-
tions modulo p with the methods given in Chapter 31. Because we assume that the
size of the universe of keys is greater than the number of slots in the hash table, we
have p > m.
We now deﬁne the hash function hab for any a 2 Z
p and any b 2 Zp using a
linear transformation followed by reductions modulo p and then modulo m:
hab.k/ D ..ak C b/ mod p/ mod m :
(11.3)
For example, with p D 17 and m D 6, we have h3;4.8/ D 5. The family of all
such hash functions is
Hpm D
˚
hab W a 2 Z
p and b 2 Zp

:
(11.4)
Each hash function hab maps Zp to Zm. This class of hash functions has the nice
property that the size m of the output range is arbitrary—not necessarily prime—a
feature which we shall use in Section 11.5. Since we have p  1 choices for a
and p choices for b, the collection Hpm contains p.p  1/ hash functions.
Theorem 11.5
The class Hpm of hash functions deﬁned by equations (11.3) and (11.4) is universal.
Proof
Consider two distinct keys k and l from Zp, so that k ¤ l. For a given
hash function hab we let
r
D
.ak C b/ mod p ;
s
D
.al C b/ mod p :
We ﬁrst note that r ¤ s. Why? Observe that
r  s  a.k  l/ .mod p/ :
It follows that r ¤ s because p is prime and both a and .k  l/ are nonzero
modulo p, and so their product must also be nonzero modulo p by Theorem 31.6.
Therefore, when computing any hab 2 Hpm, distinct inputs k and l map to distinct

268
Chapter 11
Hash Tables
values r and s modulo p; there are no collisions yet at the “mod p level.” Moreover,
each of the possible p.p1/ choices for the pair .a; b/ with a ¤ 0 yields a different
resulting pair .r; s/ with r ¤ s, since we can solve for a and b given r and s:
a
D

.r  s/..k  l/1 mod p/

mod p ;
b
D
.r  ak/ mod p ;
where ..k  l/1 mod p/ denotes the unique multiplicative inverse, modulo p,
of k  l. Since there are only p.p  1/ possible pairs .r; s/ with r ¤ s, there
is a one-to-one correspondence between pairs .a; b/ with a ¤ 0 and pairs .r; s/
with r ¤ s. Thus, for any given pair of inputs k and l, if we pick .a; b/ uniformly
at random from Z
p 	 Zp, the resulting pair .r; s/ is equally likely to be any pair of
distinct values modulo p.
Therefore, the probability that distinct keys k and l collide is equal to the prob-
ability that r  s .mod m/ when r and s are randomly chosen as distinct values
modulo p. For a given value of r, of the p  1 possible remaining values for s, the
number of values s such that s ¤ r and s  r .mod m/ is at most
dp=me  1

..p C m  1/=m/  1
(by inequality (3.6))
D
.p  1/=m :
The probability that s collides with r when reduced modulo m is at most
..p  1/=m/=.p  1/ D 1=m.
Therefore, for any pair of distinct values k; l 2 Zp,
Pr fhab.k/ D hab.l/g  1=m ;
so that Hpm is indeed universal.
Exercises
11.3-1
Suppose we wish to search a linked list of length n, where each element contains
a key k along with a hash value h.k/. Each key is a long character string. How
might we take advantage of the hash values when searching the list for an element
with a given key?
11.3-2
Suppose that we hash a string of r characters into m slots by treating it as a
radix-128 number and then using the division method. We can easily represent
the number m as a 32-bit computer word, but the string of r characters, treated as
a radix-128 number, takes many words. How can we apply the division method to
compute the hash value of the character string without using more than a constant
number of words of storage outside the string itself?

11.4
Open addressing
269
11.3-3
Consider a version of the division method in which h.k/ D k mod m, where
m D 2p  1 and k is a character string interpreted in radix 2p. Show that if we
can derive string x from string y by permuting its characters, then x and y hash to
the same value. Give an example of an application in which this property would be
undesirable in a hash function.
11.3-4
Consider a hash table of size m D 1000 and a corresponding hash function h.k/ D
bm .kA mod 1/c for A D .
p
5  1/=2. Compute the locations to which the keys
61, 62, 63, 64, and 65 are mapped.
11.3-5
?
Deﬁne a family H of hash functions from a ﬁnite set U to a ﬁnite set B to be
-universal if for all pairs of distinct elements k and l in U ,
Pr fh.k/ D h.l/g   ;
where the probability is over the choice of the hash function h drawn at random
from the family H. Show that an -universal family of hash functions must have
 
1
jBj 
1
jU j :
11.3-6
?
Let U be the set of n-tuples of values drawn from Zp, and let B D Zp, where p
is prime. Deﬁne the hash function hb W U ! B for b 2 Zp on an input n-tuple
ha0; a1; : : : ; an1i from U as
hb.ha0; a1; : : : ; an1i/ D
 n1
X
jD0
ajbj
!
mod p ;
and let H D fhb W b 2 Zpg. Argue that H is ..n  1/=p/-universal according to
the deﬁnition of -universal in Exercise 11.3-5. (Hint: See Exercise 31.4-4.)
11.4
Open addressing
In open addressing, all elements occupy the hash table itself. That is, each table
entry contains either an element of the dynamic set or NIL. When searching for
an element, we systematically examine table slots until either we ﬁnd the desired
element or we have ascertained that the element is not in the table. No lists and

270
Chapter 11
Hash Tables
no elements are stored outside the table, unlike in chaining. Thus, in open ad-
dressing, the hash table can “ﬁll up” so that no further insertions can be made; one
consequence is that the load factor ˛ can never exceed 1.
Of course, we could store the linked lists for chaining inside the hash table, in
the otherwise unused hash-table slots (see Exercise 11.2-4), but the advantage of
open addressing is that it avoids pointers altogether. Instead of following pointers,
we compute the sequence of slots to be examined. The extra memory freed by not
storing pointers provides the hash table with a larger number of slots for the same
amount of memory, potentially yielding fewer collisions and faster retrieval.
To perform insertion using open addressing, we successively examine, or probe,
the hash table until we ﬁnd an empty slot in which to put the key. Instead of being
ﬁxed in the order 0; 1; : : : ; m  1 (which requires ‚.n/ search time), the sequence
of positions probed depends upon the key being inserted. To determine which slots
to probe, we extend the hash function to include the probe number (starting from 0)
as a second input. Thus, the hash function becomes
h W U 	 f0; 1; : : : ; m  1g ! f0; 1; : : : ; m  1g :
With open addressing, we require that for every key k, the probe sequence
hh.k; 0/; h.k; 1/; : : : ; h.k; m  1/i
be a permutation of h0;1;: : : ;m1i, so that every hash-table position is eventually
considered as a slot for a new key as the table ﬁlls up. In the following pseudocode,
we assume that the elements in the hash table T are keys with no satellite infor-
mation; the key k is identical to the element containing key k. Each slot contains
either a key or NIL (if the slot is empty). The HASH-INSERT procedure takes as
input a hash table T and a key k. It either returns the slot number where it stores
key k or ﬂags an error because the hash table is already full.
HASH-INSERT.T; k/
1
i D 0
2
repeat
3
j D h.k; i/
4
if T Œj  == NIL
5
T Œj  D k
6
return j
7
else i D i C 1
8
until i == m
9
error “hash table overﬂow”
The algorithm for searching for key k probes the same sequence of slots that the
insertion algorithm examined when key k was inserted. Therefore, the search can

11.4
Open addressing
271
terminate (unsuccessfully) when it ﬁnds an empty slot, since k would have been
inserted there and not later in its probe sequence. (This argument assumes that keys
are not deleted from the hash table.) The procedure HASH-SEARCH takes as input
a hash table T and a key k, returning j if it ﬁnds that slot j contains key k, or NIL
if key k is not present in table T .
HASH-SEARCH.T; k/
1
i D 0
2
repeat
3
j D h.k; i/
4
if T Œj  == k
5
return j
6
i D i C 1
7
until T Œj  == NIL or i == m
8
return NIL
Deletion from an open-address hash table is difﬁcult. When we delete a key
from slot i, we cannot simply mark that slot as empty by storing NIL in it. If
we did, we might be unable to retrieve any key k during whose insertion we had
probed slot i and found it occupied. We can solve this problem by marking the
slot, storing in it the special value DELETED instead of NIL. We would then modify
the procedure HASH-INSERT to treat such a slot as if it were empty so that we can
insert a new key there. We do not need to modify HASH-SEARCH, since it will pass
over DELETED values while searching. When we use the special value DELETED,
however, search times no longer depend on the load factor ˛, and for this reason
chaining is more commonly selected as a collision resolution technique when keys
must be deleted.
In our analysis, we assume uniform hashing: the probe sequence of each key
is equally likely to be any of the mŠ permutations of h0; 1; : : : ; m  1i. Uni-
form hashing generalizes the notion of simple uniform hashing deﬁned earlier to a
hash function that produces not just a single number, but a whole probe sequence.
True uniform hashing is difﬁcult to implement, however, and in practice suitable
approximations (such as double hashing, deﬁned below) are used.
We will examine three commonly used techniques to compute the probe se-
quences required for open addressing: linear probing, quadratic probing, and dou-
ble hashing. These techniques all guarantee that hh.k;0/;h.k;1/;: : : ;h.k;m  1/i
is a permutation of h0; 1; : : : ; m  1i for each key k. None of these techniques ful-
ﬁlls the assumption of uniform hashing, however, since none of them is capable of
generating more than m2 different probe sequences (instead of the mŠ that uniform
hashing requires). Double hashing has the greatest number of probe sequences and,
as one might expect, seems to give the best results.

272
Chapter 11
Hash Tables
Linear probing
Given an ordinary hash function h0 W U ! f0; 1; : : : ; m  1g, which we refer to as
an auxiliary hash function, the method of linear probing uses the hash function
h.k; i/ D .h0.k/ C i/ mod m
for i D 0; 1; : : : ; m  1. Given key k, we ﬁrst probe T Œh0.k/, i.e., the slot given
by the auxiliary hash function. We next probe slot T Œh0.k/ C 1, and so on up to
slot T Œm  1. Then we wrap around to slots T Œ0; T Œ1; : : : until we ﬁnally probe
slot T Œh0.k/  1. Because the initial probe determines the entire probe sequence,
there are only m distinct probe sequences.
Linear probing is easy to implement, but it suffers from a problem known as
primary clustering. Long runs of occupied slots build up, increasing the average
search time. Clusters arise because an empty slot preceded by i full slots gets ﬁlled
next with probability .i C 1/=m. Long runs of occupied slots tend to get longer,
and the average search time increases.
Quadratic probing
Quadratic probing uses a hash function of the form
h.k; i/ D .h0.k/ C c1i C c2i 2/ mod m ;
(11.5)
where h0 is an auxiliary hash function, c1 and c2 are positive auxiliary constants,
and i D 0; 1; : : : ; m  1. The initial position probed is T Œh0.k/; later positions
probed are offset by amounts that depend in a quadratic manner on the probe num-
ber i. This method works much better than linear probing, but to make full use of
the hash table, the values of c1, c2, and m are constrained. Problem 11-3 shows
one way to select these parameters. Also, if two keys have the same initial probe
position, then their probe sequences are the same, since h.k1; 0/ D h.k2; 0/ im-
plies h.k1; i/ D h.k2; i/. This property leads to a milder form of clustering, called
secondary clustering. As in linear probing, the initial probe determines the entire
sequence, and so only m distinct probe sequences are used.
Double hashing
Double hashing offers one of the best methods available for open addressing be-
cause the permutations produced have many of the characteristics of randomly
chosen permutations. Double hashing uses a hash function of the form
h.k; i/ D .h1.k/ C ih2.k// mod m ;
where both h1 and h2 are auxiliary hash functions. The initial probe goes to posi-
tion T Œh1.k/; successive probe positions are offset from previous positions by the

11.4
Open addressing
273
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
79
69
98
72
14
50
Figure 11.5
Insertion by double hashing. Here we have a hash table of size 13 with h1.k/ D
k mod 13 and h2.k/ D 1 C .k mod 11/. Since 14  1 .mod 13/ and 14  3 .mod 11/, we insert
the key 14 into empty slot 9, after examining slots 1 and 5 and ﬁnding them to be occupied.
amount h2.k/, modulo m. Thus, unlike the case of linear or quadratic probing, the
probe sequence here depends in two ways upon the key k, since the initial probe
position, the offset, or both, may vary. Figure 11.5 gives an example of insertion
by double hashing.
The value h2.k/ must be relatively prime to the hash-table size m for the entire
hash table to be searched. (See Exercise 11.4-4.) A convenient way to ensure this
condition is to let m be a power of 2 and to design h2 so that it always produces an
odd number. Another way is to let m be prime and to design h2 so that it always
returns a positive integer less than m. For example, we could choose m prime and
let
h1.k/
D
k mod m ;
h2.k/
D
1 C .k mod m0/ ;
where m0 is chosen to be slightly less than m (say, m  1).
For example, if
k D 123456, m D 701, and m0 D 700, we have h1.k/ D 80 and h2.k/ D 257, so
that we ﬁrst probe position 80, and then we examine every 257th slot (modulo m)
until we ﬁnd the key or have examined every slot.
When m is prime or a power of 2, double hashing improves over linear or qua-
dratic probing in that ‚.m2/ probe sequences are used, rather than ‚.m/, since
each possible .h1.k/; h2.k// pair yields a distinct probe sequence. As a result, for

274
Chapter 11
Hash Tables
such values of m, the performance of double hashing appears to be very close to
the performance of the “ideal” scheme of uniform hashing.
Although values of m other than primes or powers of 2 could in principle be
used with double hashing, in practice it becomes more difﬁcult to efﬁciently gen-
erate h2.k/ in a way that ensures that it is relatively prime to m, in part because the
relative density .m/=m of such numbers may be small (see equation (31.24)).
Analysis of open-address hashing
As in our analysis of chaining, we express our analysis of open addressing in terms
of the load factor ˛ D n=m of the hash table. Of course, with open addressing, at
most one element occupies each slot, and thus n  m, which implies ˛  1.
We assume that we are using uniform hashing. In this idealized scheme, the
probe sequence hh.k; 0/; h.k; 1/; : : : ; h.k; m  1/i used to insert or search for
each key k is equally likely to be any permutation of h0; 1; : : : ; m  1i. Of course,
a given key has a unique ﬁxed probe sequence associated with it; what we mean
here is that, considering the probability distribution on the space of keys and the
operation of the hash function on the keys, each possible probe sequence is equally
likely.
We now analyze the expected number of probes for hashing with open address-
ing under the assumption of uniform hashing, beginning with an analysis of the
number of probes made in an unsuccessful search.
Theorem 11.6
Given an open-address hash table with load factor ˛ D n=m < 1, the expected
number of probes in an unsuccessful search is at most 1=.1˛/, assuming uniform
hashing.
Proof
In an unsuccessful search, every probe but the last accesses an occupied
slot that does not contain the desired key, and the last slot probed is empty. Let us
deﬁne the random variable X to be the number of probes made in an unsuccessful
search, and let us also deﬁne the event Ai, for i D 1; 2; : : :, to be the event that
an ith probe occurs and it is to an occupied slot. Then the event fX  ig is the
intersection of events A1\A2\  \Ai1. We will bound Pr fX  ig by bounding
Pr fA1 \ A2 \    \ Ai1g. By Exercise C.2-5,
Pr fA1 \ A2 \    \ Ai1g D Pr fA1g  Pr fA2 j A1g  Pr fA3 j A1 \ A2g   
Pr fAi1 j A1 \ A2 \    \ Ai2g :
Since there are n elements and m slots, Pr fA1g D n=m. For j > 1, the probability
that there is a j th probe and it is to an occupied slot, given that the ﬁrst j  1
probes were to occupied slots, is .nj C1/=.mj C1/. This probability follows

11.4
Open addressing
275
because we would be ﬁnding one of the remaining .n  .j  1// elements in one
of the .m  .j  1// unexamined slots, and by the assumption of uniform hashing,
the probability is the ratio of these quantities. Observing that n < m implies that
.n  j /=.m  j /  n=m for all j such that 0  j < m, we have for all i such that
1  i  m,
Pr fX  ig
D
n
m  n  1
m  1  n  2
m  2    n  i C 2
m  i C 2

 n
m
i1
D
˛i1 :
Now, we use equation (C.25) to bound the expected number of probes:
E ŒX
D
1
X
iD1
Pr fX  ig

1
X
iD1
˛i1
D
1
X
iD0
˛i
D
1
1  ˛ :
This bound of 1=.1˛/ D 1C˛ C˛2 C˛3 C   has an intuitive interpretation.
We always make the ﬁrst probe. With probability approximately ˛, the ﬁrst probe
ﬁnds an occupied slot, so that we need to probe a second time. With probability
approximately ˛2, the ﬁrst two slots are occupied so that we make a third probe,
and so on.
If ˛ is a constant, Theorem 11.6 predicts that an unsuccessful search runs in O.1/
time. For example, if the hash table is half full, the average number of probes in an
unsuccessful search is at most 1=.1  :5/ D 2. If it is 90 percent full, the average
number of probes is at most 1=.1  :9/ D 10.
Theorem 11.6 gives us the performance of the HASH-INSERT procedure almost
immediately.
Corollary 11.7
Inserting an element into an open-address hash table with load factor ˛ requires at
most 1=.1  ˛/ probes on average, assuming uniform hashing.

276
Chapter 11
Hash Tables
Proof
An element is inserted only if there is room in the table, and thus ˛ < 1.
Inserting a key requires an unsuccessful search followed by placing the key into the
ﬁrst empty slot found. Thus, the expected number of probes is at most 1=.1˛/.
We have to do a little more work to compute the expected number of probes for
a successful search.
Theorem 11.8
Given an open-address hash table with load factor ˛ < 1, the expected number of
probes in a successful search is at most
1
˛ ln
1
1  ˛ ;
assuming uniform hashing and assuming that each key in the table is equally likely
to be searched for.
Proof
A search for a key k reproduces the same probe sequence as when the
element with key k was inserted. By Corollary 11.7, if k was the .i C 1/st key
inserted into the hash table, the expected number of probes made in a search for k
is at most 1=.1  i=m/ D m=.m  i/. Averaging over all n keys in the hash table
gives us the expected number of probes in a successful search:
1
n
n1
X
iD0
m
m  i
D
m
n
n1
X
iD0
1
m  i
D
1
˛
m
X
kDmnC1
1
k

1
˛
Z m
mn
.1=x/ dx
(by inequality (A.12))
D
1
˛ ln
m
m  n
D
1
˛ ln
1
1  ˛ :
If the hash table is half full, the expected number of probes in a successful search
is less than 1:387. If the hash table is 90 percent full, the expected number of probes
is less than 2:559.

11.5
Perfect hashing
277
Exercises
11.4-1
Consider inserting the keys 10; 22; 31; 4; 15; 28; 17; 88; 59 into a hash table of
length m D 11 using open addressing with the auxiliary hash function h0.k/ D k.
Illustrate the result of inserting these keys using linear probing, using quadratic
probing with c1 D 1 and c2 D 3, and using double hashing with h1.k/ D k and
h2.k/ D 1 C .k mod .m  1//.
11.4-2
Write pseudocode for HASH-DELETE as outlined in the text, and modify HASH-
INSERT to handle the special value DELETED.
11.4-3
Consider an open-address hash table with uniform hashing. Give upper bounds
on the expected number of probes in an unsuccessful search and on the expected
number of probes in a successful search when the load factor is 3=4 and when it
is 7=8.
11.4-4
?
Suppose that we use double hashing to resolve collisions—that is, we use the hash
function h.k; i/ D .h1.k/ C ih2.k// mod m. Show that if m and h2.k/ have
greatest common divisor d  1 for some key k, then an unsuccessful search for
key k examines .1=d/th of the hash table before returning to slot h1.k/. Thus,
when d D 1, so that m and h2.k/ are relatively prime, the search may examine the
entire hash table. (Hint: See Chapter 31.)
11.4-5
?
Consider an open-address hash table with a load factor ˛. Find the nonzero value ˛
for which the expected number of probes in an unsuccessful search equals twice
the expected number of probes in a successful search. Use the upper bounds given
by Theorems 11.6 and 11.8 for these expected numbers of probes.
?
11.5
Perfect hashing
Although hashing is often a good choice for its excellent average-case perfor-
mance, hashing can also provide excellent worst-case performance when the set of
keys is static: once the keys are stored in the table, the set of keys never changes.
Some applications naturally have static sets of keys: consider the set of reserved
words in a programming language, or the set of ﬁle names on a CD-ROM. We

278
Chapter 11
Hash Tables
0
1
2
3
4
5
6
7
8
1
0
0 10
9 10 18
60
75
0
1
2
3
1
0
0 70
0
0
16 23 88
40
37
0
1
2
3
4
5
6
7
8
52
m2
S2
a2 b2
m0
S0
a0 b0
m5
S5
a5 b5
m7
S7
a7 b7
T
4
5
6
7
8
72
9
10
11
12
13
14
15
22
Figure 11.6
Using perfect hashing to store the set K D f10; 22; 37; 40; 52; 60; 70; 72; 75g. The
outer hash function is h.k/ D ..ak C b/ mod p/ mod m, where a D 3, b D 42, p D 101, and
m D 9. For example, h.75/ D 2, and so key 75 hashes to slot 2 of table T . A secondary hash
table Sj stores all keys hashing to slot j. The size of hash table Sj is mj D n2
j , and the associated
hash function is hj .k/ D ..aj k C bj / mod p/ mod mj . Since h2.75/ D 7, key 75 is stored in slot 7
of secondary hash table S2. No collisions occur in any of the secondary hash tables, and so searching
takes constant time in the worst case.
call a hashing technique perfect hashing if O.1/ memory accesses are required to
perform a search in the worst case.
To create a perfect hashing scheme, we use two levels of hashing, with universal
hashing at each level. Figure 11.6 illustrates the approach.
The ﬁrst level is essentially the same as for hashing with chaining: we hash
the n keys into m slots using a hash function h carefully selected from a family of
universal hash functions.
Instead of making a linked list of the keys hashing to slot j , however, we use a
small secondary hash table Sj with an associated hash function hj . By choosing
the hash functions hj carefully, we can guarantee that there are no collisions at the
secondary level.
In order to guarantee that there are no collisions at the secondary level, however,
we will need to let the size mj of hash table Sj be the square of the number nj of
keys hashing to slot j . Although you might think that the quadratic dependence
of mj on nj may seem likely to cause the overall storage requirement to be exces-
sive, we shall show that by choosing the ﬁrst-level hash function well, we can limit
the expected total amount of space used to O.n/.
We use hash functions chosen from the universal classes of hash functions of
Section 11.3.3. The ﬁrst-level hash function comes from the class Hpm, where as
in Section 11.3.3, p is a prime number greater than any key value. Those keys

11.5
Perfect hashing
279
hashing to slot j are re-hashed into a secondary hash table Sj of size mj using a
hash function hj chosen from the class Hp;mj .1
We shall proceed in two steps. First, we shall determine how to ensure that
the secondary tables have no collisions. Second, we shall show that the expected
amount of memory used overall—for the primary hash table and all the secondary
hash tables—is O.n/.
Theorem 11.9
Suppose that we store n keys in a hash table of size m D n2 using a hash function h
randomly chosen from a universal class of hash functions. Then, the probability is
less than 1=2 that there are any collisions.
Proof
There are

n
2

pairs of keys that may collide; each pair collides with prob-
ability 1=m if h is chosen at random from a universal family H of hash functions.
Let X be a random variable that counts the number of collisions. When m D n2,
the expected number of collisions is
E ŒX
D
 
n
2
!
 1
n2
D
n2  n
2
 1
n2
<
1=2 :
(This analysis is similar to the analysis of the birthday paradox in Section 5.4.1.)
Applying Markov’s inequality (C.30), Pr fX  tg  E ŒX =t, with t D 1, com-
pletes the proof.
In the situation described in Theorem 11.9, where m D n2, it follows that a hash
function h chosen at random from H is more likely than not to have no collisions.
Given the set K of n keys to be hashed (remember that K is static), it is thus easy
to ﬁnd a collision-free hash function h with a few random trials.
When n is large, however, a hash table of size m D n2 is excessive. Therefore,
we adopt the two-level hashing approach, and we use the approach of Theorem 11.9
only to hash the entries within each slot. We use an outer, or ﬁrst-level, hash
function h to hash the keys into m D n slots. Then, if nj keys hash to slot j , we
use a secondary hash table Sj of size mj D n2
j to provide collision-free constant-
time lookup.
1When nj D mj D 1, we don’t really need a hash function for slot j; when we choose a hash
function hab.k/ D ..ak C b/ mod p/ mod mj for such a slot, we just use a D b D 0.

280
Chapter 11
Hash Tables
We now turn to the issue of ensuring that the overall memory used is O.n/.
Since the size mj of the j th secondary hash table grows quadratically with the
number nj of keys stored, we run the risk that the overall amount of storage could
be excessive.
If the ﬁrst-level table size is m D n, then the amount of memory used is O.n/
for the primary hash table, for the storage of the sizes mj of the secondary hash
tables, and for the storage of the parameters aj and bj deﬁning the secondary hash
functions hj drawn from the class Hp;mj of Section 11.3.3 (except when nj D 1
and we use a D b D 0). The following theorem and a corollary provide a bound on
the expected combined sizes of all the secondary hash tables. A second corollary
bounds the probability that the combined size of all the secondary hash tables is
superlinear (actually, that it equals or exceeds 4n).
Theorem 11.10
Suppose that we store n keys in a hash table of size m D n using a hash function h
randomly chosen from a universal class of hash functions. Then, we have
E
"m1
X
jD0
n2
j
#
< 2n ;
where nj is the number of keys hashing to slot j .
Proof
We start with the following identity, which holds for any nonnegative inte-
ger a:
a2 D a C 2
 
a
2
!
:
(11.6)
We have
E
"m1
X
jD0
n2
j
#
D
E
"m1
X
jD0
 
nj C 2
 
nj
2
!!#
(by equation (11.6))
D
E
"m1
X
jD0
nj
#
C 2 E
"m1
X
jD0
 
nj
2
!#
(by linearity of expectation)
D
E Œn C 2 E
"m1
X
jD0
 
nj
2
!#
(by equation (11.1))

11.5
Perfect hashing
281
D
n C 2 E
"m1
X
jD0
 
nj
2
!#
(since n is not a random variable) .
To evaluate the summation Pm1
jD0

nj
2

, we observe that it is just the total number
of pairs of keys in the hash table that collide. By the properties of universal hashing,
the expected value of this summation is at most
 
n
2
!
1
m
D
n.n  1/
2m
D
n  1
2
;
since m D n. Thus,
E
"m1
X
jD0
n2
j
#

n C 2 n  1
2
D
2n  1
<
2n :
Corollary 11.11
Suppose that we store n keys in a hash table of size m D n using a hash func-
tion h randomly chosen from a universal class of hash functions, and we set the
size of each secondary hash table to mj D n2
j for j D 0; 1; : : : ; m  1. Then,
the expected amount of storage required for all secondary hash tables in a perfect
hashing scheme is less than 2n.
Proof
Since mj D n2
j for j D 0; 1; : : : ; m  1, Theorem 11.10 gives
E
"m1
X
jD0
mj
#
D
E
"m1
X
jD0
n2
j
#
<
2n ;
(11.7)
which completes the proof.
Corollary 11.12
Suppose that we store n keys in a hash table of size m D n using a hash function h
randomly chosen from a universal class of hash functions, and we set the size
of each secondary hash table to mj D n2
j for j D 0; 1; : : : ; m  1. Then, the
probability is less than 1=2 that the total storage used for secondary hash tables
equals or exceeds 4n.

282
Chapter 11
Hash Tables
Proof
Again we apply Markov’s inequality (C.30), Pr fX  tg  E ŒX =t, this
time to inequality (11.7), with X D Pm1
jD0 mj and t D 4n:
Pr
(m1
X
jD0
mj  4n
)

E
Pm1
jD0 mj

4n
<
2n
4n
D
1=2 :
From Corollary 11.12, we see that if we test a few randomly chosen hash func-
tions from the universal family, we will quickly ﬁnd one that uses a reasonable
amount of storage.
Exercises
11.5-1
?
Suppose that we insert n keys into a hash table of size m using open addressing
and uniform hashing. Let p.n; m/ be the probability that no collisions occur. Show
that p.n; m/  en.n1/=2m. (Hint: See equation (3.12).) Argue that when n ex-
ceeds pm, the probability of avoiding collisions goes rapidly to zero.
Problems
11-1
Longest-probe bound for hashing
Suppose that we use an open-addressed hash table of size m to store n  m=2
items.
a. Assuming uniform hashing, show that for i D 1; 2; : : : ; n, the probability is at
most 2k that the ith insertion requires strictly more than k probes.
b. Show that for i D 1; 2; : : : ; n, the probability is O.1=n2/ that the ith insertion
requires more than 2 lg n probes.
Let the random variable Xi denote the number of probes required by the ith inser-
tion. You have shown in part (b) that Pr fXi > 2 lg ng D O.1=n2/. Let the random
variable X D max1in Xi denote the maximum number of probes required by
any of the n insertions.
c. Show that Pr fX > 2 lg ng D O.1=n/.
d. Show that the expected length E ŒX of the longest probe sequence is O.lg n/.

Problems for Chapter 11
283
11-2
Slot-size bound for chaining
Suppose that we have a hash table with n slots, with collisions resolved by chain-
ing, and suppose that n keys are inserted into the table. Each key is equally likely
to be hashed to each slot. Let M be the maximum number of keys in any slot after
all the keys have been inserted. Your mission is to prove an O.lg n= lg lg n/ upper
bound on E ŒM, the expected value of M.
a. Argue that the probability Qk that exactly k keys hash to a particular slot is
given by
Qk D
1
n
k
1  1
n
nk 
n
k
!
:
b. Let Pk be the probability that M D k, that is, the probability that the slot
containing the most keys contains k keys. Show that Pk  nQk.
c. Use Stirling’s approximation, equation (3.18), to show that Qk < ek=kk.
d. Show that there exists a constant c > 1 such that Qk0 < 1=n3 for k0 D
c lg n= lg lg n. Conclude that Pk < 1=n2 for k  k0 D c lg n= lg lg n.
e. Argue that
E ŒM  Pr

M > c lg n
lg lg n

 n C Pr

M  c lg n
lg lg n

 c lg n
lg lg n :
Conclude that E ŒM D O.lg n= lg lg n/.
11-3
Quadratic probing
Suppose that we are given a key k to search for in a hash table with positions
0; 1; : : : ; m1, and suppose that we have a hash function h mapping the key space
into the set f0; 1; : : : ; m  1g. The search scheme is as follows:
1. Compute the value j D h.k/, and set i D 0.
2. Probe in position j for the desired key k. If you ﬁnd it, or if this position is
empty, terminate the search.
3. Set i D i C 1. If i now equals m, the table is full, so terminate the search.
Otherwise, set j D .i C j / mod m, and return to step 2.
Assume that m is a power of 2.
a. Show that this scheme is an instance of the general “quadratic probing” scheme
by exhibiting the appropriate constants c1 and c2 for equation (11.5).
b. Prove that this algorithm examines every table position in the worst case.

284
Chapter 11
Hash Tables
11-4
Hashing and authentication
Let H be a class of hash functions in which each hash function h 2 H maps the
universe U of keys to f0; 1; : : : ; m  1g. We say that H is k-universal if, for every
ﬁxed sequence of k distinct keys hx.1/; x.2/; : : : ; x.k/i and for any h chosen at
random from H, the sequence hh.x.1//;h.x.2//;: : : ;h.x.k//i is equally likely to be
any of the mk sequences of length k with elements drawn from f0; 1; : : : ; m  1g.
a. Show that if the family H of hash functions is 2-universal, then it is universal.
b. Suppose that the universe U is the set of n-tuples of values drawn from
Zp
D f0; 1; : : : ; p  1g, where p is prime.
Consider an element x D
hx0; x1; : : : ; xn1i 2 U . For any n-tuple a D ha0; a1; : : : ; an1i 2 U , de-
ﬁne the hash function ha by
ha.x/ D
 n1
X
jD0
ajxj
!
mod p :
Let H D fhag. Show that H is universal, but not 2-universal. (Hint: Find a key
for which all hash functions in H produce the same value.)
c. Suppose that we modify H slightly from part (b): for any a 2 U and for any
b 2 Zp, deﬁne
h0
ab.x/ D
 n1
X
jD0
ajxj C b
!
mod p
and H 0 D fh0
abg. Argue that H 0 is 2-universal. (Hint: Consider ﬁxed n-tuples
x 2 U and y 2 U , with xi ¤ yi for some i. What happens to h0
ab.x/
and h0
ab.y/ as ai and b range over Zp?)
d. Suppose that Alice and Bob secretly agree on a hash function h from a
2-universal family H of hash functions. Each h 2 H maps from a universe of
keys U to Zp, where p is prime. Later, Alice sends a message m to Bob over the
Internet, where m 2 U . She authenticates this message to Bob by also sending
an authentication tag t D h.m/, and Bob checks that the pair .m; t/ he receives
indeed satisﬁes t D h.m/. Suppose that an adversary intercepts .m; t/ en route
and tries to fool Bob by replacing the pair .m; t/ with a different pair .m0; t0/.
Argue that the probability that the adversary succeeds in fooling Bob into ac-
cepting .m0; t0/ is at most 1=p, no matter how much computing power the ad-
versary has, and even if the adversary knows the family H of hash functions
used.

Notes for Chapter 11
285
Chapter notes
Knuth [211] and Gonnet [145] are excellent references for the analysis of hash-
ing algorithms. Knuth credits H. P. Luhn (1953) for inventing hash tables, along
with the chaining method for resolving collisions. At about the same time, G. M.
Amdahl originated the idea of open addressing.
Carter and Wegman introduced the notion of universal classes of hash functions
in 1979 [58].
Fredman, Koml´os, and Szemer´edi [112] developed the perfect hashing scheme
for static sets presented in Section 11.5. An extension of their method to dynamic
sets, handling insertions and deletions in amortized expected time O.1/, has been
given by Dietzfelbinger et al. [86].
