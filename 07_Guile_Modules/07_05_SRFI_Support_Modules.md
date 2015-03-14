7.5 SRFI Support Modules
========================

SRFI is an acronym for Scheme Request For Implementation.  The SRFI
documents define a lot of syntactic and procedure extensions to standard
Scheme as defined in R5RS.

   Guile has support for a number of SRFIs.  This chapter gives an
overview over the available SRFIs and some usage hints.  For complete
documentation, design rationales and further examples, we advise you to
get the relevant SRFI documents from the SRFI home page
<http://srfi.schemers.org/>.

7.5.1 About SRFI Usage
----------------------

SRFI support in Guile is currently implemented partly in the core
library, and partly as add-on modules.  That means that some SRFIs are
automatically available when the interpreter is started, whereas the
other SRFIs require you to use the appropriate support module
explicitly.

   There are several reasons for this inconsistency.  First, the feature
checking syntactic form ‘cond-expand’ (*note SRFI-0::) must be available
immediately, because it must be there when the user wants to check for
the Scheme implementation, that is, before she can know that it is safe
to use ‘use-modules’ to load SRFI support modules.  The second reason is
that some features defined in SRFIs had been implemented in Guile before
the developers started to add SRFI implementations as modules (for
example SRFI-13 (*note SRFI-13::)).  In the future, it is possible that
SRFIs in the core library might be factored out into separate modules,
requiring explicit module loading when they are needed.  So you should
be prepared to have to use ‘use-modules’ someday in the future to access
SRFI-13 bindings.  If you want, you can do that already.  We have
included the module ‘(srfi srfi-13)’ in the distribution, which
currently does nothing, but ensures that you can write future-safe code.

   Generally, support for a specific SRFI is made available by using
modules named ‘(srfi srfi-NUMBER)’, where NUMBER is the number of the
SRFI needed.  Another possibility is to use the command line option
‘--use-srfi’, which will load the necessary modules automatically (*note
Invoking Guile::).

7.5.2 SRFI-0 - cond-expand
--------------------------

This SRFI lets a portable Scheme program test for the presence of
certain features, and adapt itself by using different blocks of code, or
fail if the necessary features are not available.  There’s no module to
load, this is in the Guile core.

   A program designed only for Guile will generally not need this
mechanism, such a program can of course directly use the various
documented parts of Guile.

 -- syntax: cond-expand (feature body…) …
     Expand to the BODY of the first clause whose FEATURE specification
     is satisfied.  It is an error if no FEATURE is satisfied.

     Features are symbols such as ‘srfi-1’, and a feature specification
     can use ‘and’, ‘or’ and ‘not’ forms to test combinations.  The last
     clause can be an ‘else’, to be used if no other passes.

     For example, define a private version of ‘alist-cons’ if SRFI-1 is
     not available.

          (cond-expand (srfi-1
                        )
                       (else
                        (define (alist-cons key val alist)
                          (cons (cons key val) alist))))

     Or demand a certain set of SRFIs (list operations, string ports,
     ‘receive’ and string operations), failing if they’re not available.

          (cond-expand ((and srfi-1 srfi-6 srfi-8 srfi-13)
                        ))

The Guile core has the following features,

     guile
     guile-2  ;; starting from Guile 2.x
     r5rs
     srfi-0
     srfi-4
     srfi-13
     srfi-14
     srfi-16
     srfi-23
     srfi-30
     srfi-39
     srfi-46
     srfi-55
     srfi-61
     srfi-62
     srfi-87
     srfi-105

   Other SRFI feature symbols are defined once their code has been
loaded with ‘use-modules’, since only then are their bindings available.

   The ‘--use-srfi’ command line option (*note Invoking Guile::) is a
good way to load SRFIs to satisfy ‘cond-expand’ when running a portable
program.

   Testing the ‘guile’ feature allows a program to adapt itself to the
Guile module system, but still run on other Scheme systems.  For example
the following demands SRFI-8 (‘receive’), but also knows how to load it
with the Guile mechanism.

     (cond-expand (srfi-8
                   )
                  (guile
                   (use-modules (srfi srfi-8))))

   Likewise, testing the ‘guile-2’ feature allows code to be portable
between Guile 2.0 and previous versions of Guile.  For instance, it
makes it possible to write code that accounts for Guile 2.0’s compiler,
yet be correctly interpreted on 1.8 and earlier versions:

     (cond-expand (guile-2 (eval-when (compile)
                             ;; This must be evaluated at compile time.
                             (fluid-set! current-reader my-reader)))
                  (guile
                           ;; Earlier versions of Guile do not have a
                           ;; separate compilation phase.
                           (fluid-set! current-reader my-reader)))

   It should be noted that ‘cond-expand’ is separate from the
‘*features*’ mechanism (*note Feature Tracking::), feature symbols in
one are unrelated to those in the other.

7.5.3 SRFI-1 - List library
---------------------------

The list library defined in SRFI-1 contains a lot of useful list
processing procedures for construction, examining, destructuring and
manipulating lists and pairs.

   Since SRFI-1 also defines some procedures which are already contained
in R5RS and thus are supported by the Guile core library, some list and
pair procedures which appear in the SRFI-1 document may not appear in
this section.  So when looking for a particular list/pair processing
procedure, you should also have a look at the sections *note Lists:: and
*note Pairs::.

7.5.3.1 Constructors
....................

New lists can be constructed by calling one of the following procedures.

 -- Scheme Procedure: xcons d a
     Like ‘cons’, but with interchanged arguments.  Useful mostly when
     passed to higher-order procedures.

 -- Scheme Procedure: list-tabulate n init-proc
     Return an N-element list, where each list element is produced by
     applying the procedure INIT-PROC to the corresponding list index.
     The order in which INIT-PROC is applied to the indices is not
     specified.

 -- Scheme Procedure: list-copy lst
     Return a new list containing the elements of the list LST.

     This function differs from the core ‘list-copy’ (*note List
     Constructors::) in accepting improper lists too.  And if LST is not
     a pair at all then it’s treated as the final tail of an improper
     list and simply returned.

 -- Scheme Procedure: circular-list elt1 elt2 …
     Return a circular list containing the given arguments ELT1 ELT2 ….

 -- Scheme Procedure: iota count [start step]
     Return a list containing COUNT numbers, starting from START and
     adding STEP each time.  The default START is 0, the default STEP is
     1.  For example,

          (iota 6)        ⇒ (0 1 2 3 4 5)
          (iota 4 2.5 -2) ⇒ (2.5 0.5 -1.5 -3.5)

     This function takes its name from the corresponding primitive in
     the APL language.

7.5.3.2 Predicates
..................

The procedures in this section test specific properties of lists.

 -- Scheme Procedure: proper-list? obj
     Return ‘#t’ if OBJ is a proper list, or ‘#f’ otherwise.  This is
     the same as the core ‘list?’ (*note List Predicates::).

     A proper list is a list which ends with the empty list ‘()’ in the
     usual way.  The empty list ‘()’ itself is a proper list too.

          (proper-list? '(1 2 3))  ⇒ #t
          (proper-list? '())       ⇒ #t

 -- Scheme Procedure: circular-list? obj
     Return ‘#t’ if OBJ is a circular list, or ‘#f’ otherwise.

     A circular list is a list where at some point the ‘cdr’ refers back
     to a previous pair in the list (either the start or some later
     point), so that following the ‘cdr’s takes you around in a circle,
     with no end.

          (define x (list 1 2 3 4))
          (set-cdr! (last-pair x) (cddr x))
          x ⇒ (1 2 3 4 3 4 3 4 ...)
          (circular-list? x)  ⇒ #t

 -- Scheme Procedure: dotted-list? obj
     Return ‘#t’ if OBJ is a dotted list, or ‘#f’ otherwise.

     A dotted list is a list where the ‘cdr’ of the last pair is not the
     empty list ‘()’.  Any non-pair OBJ is also considered a dotted
     list, with length zero.

          (dotted-list? '(1 2 . 3))  ⇒ #t
          (dotted-list? 99)          ⇒ #t

   It will be noted that any Scheme object passes exactly one of the
above three tests ‘proper-list?’, ‘circular-list?’ and ‘dotted-list?’.
Non-lists are ‘dotted-list?’, finite lists are either ‘proper-list?’ or
‘dotted-list?’, and infinite lists are ‘circular-list?’.


 -- Scheme Procedure: null-list? lst
     Return ‘#t’ if LST is the empty list ‘()’, ‘#f’ otherwise.  If
     something else than a proper or circular list is passed as LST, an
     error is signalled.  This procedure is recommended for checking for
     the end of a list in contexts where dotted lists are not allowed.

 -- Scheme Procedure: not-pair? obj
     Return ‘#t’ is OBJ is not a pair, ‘#f’ otherwise.  This is
     shorthand notation ‘(not (pair? OBJ))’ and is supposed to be used
     for end-of-list checking in contexts where dotted lists are
     allowed.

 -- Scheme Procedure: list= elt= list1 …
     Return ‘#t’ if all argument lists are equal, ‘#f’ otherwise.  List
     equality is determined by testing whether all lists have the same
     length and the corresponding elements are equal in the sense of the
     equality predicate ELT=.  If no or only one list is given, ‘#t’ is
     returned.

7.5.3.3 Selectors
.................

 -- Scheme Procedure: first pair
 -- Scheme Procedure: second pair
 -- Scheme Procedure: third pair
 -- Scheme Procedure: fourth pair
 -- Scheme Procedure: fifth pair
 -- Scheme Procedure: sixth pair
 -- Scheme Procedure: seventh pair
 -- Scheme Procedure: eighth pair
 -- Scheme Procedure: ninth pair
 -- Scheme Procedure: tenth pair
     These are synonyms for ‘car’, ‘cadr’, ‘caddr’, ….

 -- Scheme Procedure: car+cdr pair
     Return two values, the CAR and the CDR of PAIR.

 -- Scheme Procedure: take lst i
 -- Scheme Procedure: take! lst i
     Return a list containing the first I elements of LST.

     ‘take!’ may modify the structure of the argument list LST in order
     to produce the result.

 -- Scheme Procedure: drop lst i
     Return a list containing all but the first I elements of LST.

 -- Scheme Procedure: take-right lst i
     Return a list containing the I last elements of LST.  The return
     shares a common tail with LST.

 -- Scheme Procedure: drop-right lst i
 -- Scheme Procedure: drop-right! lst i
     Return a list containing all but the I last elements of LST.

     ‘drop-right’ always returns a new list, even when I is zero.
     ‘drop-right!’ may modify the structure of the argument list LST in
     order to produce the result.

 -- Scheme Procedure: split-at lst i
 -- Scheme Procedure: split-at! lst i
     Return two values, a list containing the first I elements of the
     list LST and a list containing the remaining elements.

     ‘split-at!’ may modify the structure of the argument list LST in
     order to produce the result.

 -- Scheme Procedure: last lst
     Return the last element of the non-empty, finite list LST.

7.5.3.4 Length, Append, Concatenate, etc.
.........................................

 -- Scheme Procedure: length+ lst
     Return the length of the argument list LST.  When LST is a circular
     list, ‘#f’ is returned.

 -- Scheme Procedure: concatenate list-of-lists
 -- Scheme Procedure: concatenate! list-of-lists
     Construct a list by appending all lists in LIST-OF-LISTS.

     ‘concatenate!’ may modify the structure of the given lists in order
     to produce the result.

     ‘concatenate’ is the same as ‘(apply append LIST-OF-LISTS)’.  It
     exists because some Scheme implementations have a limit on the
     number of arguments a function takes, which the ‘apply’ might
     exceed.  In Guile there is no such limit.

 -- Scheme Procedure: append-reverse rev-head tail
 -- Scheme Procedure: append-reverse! rev-head tail
     Reverse REV-HEAD, append TAIL to it, and return the result.  This
     is equivalent to ‘(append (reverse REV-HEAD) TAIL)’, but its
     implementation is more efficient.

          (append-reverse '(1 2 3) '(4 5 6)) ⇒ (3 2 1 4 5 6)

     ‘append-reverse!’ may modify REV-HEAD in order to produce the
     result.

 -- Scheme Procedure: zip lst1 lst2 …
     Return a list as long as the shortest of the argument lists, where
     each element is a list.  The first list contains the first elements
     of the argument lists, the second list contains the second
     elements, and so on.

 -- Scheme Procedure: unzip1 lst
 -- Scheme Procedure: unzip2 lst
 -- Scheme Procedure: unzip3 lst
 -- Scheme Procedure: unzip4 lst
 -- Scheme Procedure: unzip5 lst
     ‘unzip1’ takes a list of lists, and returns a list containing the
     first elements of each list, ‘unzip2’ returns two lists, the first
     containing the first elements of each lists and the second
     containing the second elements of each lists, and so on.

 -- Scheme Procedure: count pred lst1 lst2 …
     Return a count of the number of times PRED returns true when called
     on elements from the given lists.

     PRED is called with N parameters ‘(PRED ELEM1 … ELEMN )’, each
     element being from the corresponding list.  The first call is with
     the first element of each list, the second with the second element
     from each, and so on.

     Counting stops when the end of the shortest list is reached.  At
     least one list must be non-circular.

7.5.3.5 Fold, Unfold & Map
..........................

 -- Scheme Procedure: fold proc init lst1 lst2 …
 -- Scheme Procedure: fold-right proc init lst1 lst2 …
     Apply PROC to the elements of LST1 LST2 … to build a result, and
     return that result.

     Each PROC call is ‘(PROC ELEM1 ELEM2 … PREVIOUS)’, where ELEM1 is
     from LST1, ELEM2 is from LST2, and so on.  PREVIOUS is the return
     from the previous call to PROC, or the given INIT for the first
     call.  If any list is empty, just INIT is returned.

     ‘fold’ works through the list elements from first to last.  The
     following shows a list reversal and the calls it makes,

          (fold cons '() '(1 2 3))

          (cons 1 '())
          (cons 2 '(1))
          (cons 3 '(2 1)
          ⇒ (3 2 1)

     ‘fold-right’ works through the list elements from last to first,
     ie. from the right.  So for example the following finds the longest
     string, and the last among equal longest,

          (fold-right (lambda (str prev)
                        (if (> (string-length str) (string-length prev))
                            str
                            prev))
                      ""
                      '("x" "abc" "xyz" "jk"))
          ⇒ "xyz"

     If LST1 LST2 … have different lengths, ‘fold’ stops when the end of
     the shortest is reached; ‘fold-right’ commences at the last element
     of the shortest.  Ie. elements past the length of the shortest are
     ignored in the other LSTs.  At least one LST must be non-circular.

     ‘fold’ should be preferred over ‘fold-right’ if the order of
     processing doesn’t matter, or can be arranged either way, since
     ‘fold’ is a little more efficient.

     The way ‘fold’ builds a result from iterating is quite general, it
     can do more than other iterations like say ‘map’ or ‘filter’.  The
     following for example removes adjacent duplicate elements from a
     list,

          (define (delete-adjacent-duplicates lst)
            (fold-right (lambda (elem ret)
                          (if (equal? elem (first ret))
                              ret
                              (cons elem ret)))
                        (list (last lst))
                        lst))
          (delete-adjacent-duplicates '(1 2 3 3 4 4 4 5))
          ⇒ (1 2 3 4 5)

     Clearly the same sort of thing can be done with a ‘for-each’ and a
     variable in which to build the result, but a self-contained PROC
     can be re-used in multiple contexts, where a ‘for-each’ would have
     to be written out each time.

 -- Scheme Procedure: pair-fold proc init lst1 lst2 …
 -- Scheme Procedure: pair-fold-right proc init lst1 lst2 …
     The same as ‘fold’ and ‘fold-right’, but apply PROC to the pairs of
     the lists instead of the list elements.

 -- Scheme Procedure: reduce proc default lst
 -- Scheme Procedure: reduce-right proc default lst
     ‘reduce’ is a variant of ‘fold’, where the first call to PROC is on
     two elements from LST, rather than one element and a given initial
     value.

     If LST is empty, ‘reduce’ returns DEFAULT (this is the only use for
     DEFAULT).  If LST has just one element then that’s the return
     value.  Otherwise PROC is called on the elements of LST.

     Each PROC call is ‘(PROC ELEM PREVIOUS)’, where ELEM is from LST
     (the second and subsequent elements of LST), and PREVIOUS is the
     return from the previous call to PROC.  The first element of LST is
     the PREVIOUS for the first call to PROC.

     For example, the following adds a list of numbers, the calls made
     to ‘+’ are shown.  (Of course ‘+’ accepts multiple arguments and
     can add a list directly, with ‘apply’.)

          (reduce + 0 '(5 6 7)) ⇒ 18

          (+ 6 5)  ⇒ 11
          (+ 7 11) ⇒ 18

     ‘reduce’ can be used instead of ‘fold’ where the INIT value is an
     “identity”, meaning a value which under PROC doesn’t change the
     result, in this case 0 is an identity since ‘(+ 5 0)’ is just 5.
     ‘reduce’ avoids that unnecessary call.

     ‘reduce-right’ is a similar variation on ‘fold-right’, working from
     the end (ie. the right) of LST.  The last element of LST is the
     PREVIOUS for the first call to PROC, and the ELEM values go from
     the second last.

     ‘reduce’ should be preferred over ‘reduce-right’ if the order of
     processing doesn’t matter, or can be arranged either way, since
     ‘reduce’ is a little more efficient.

 -- Scheme Procedure: unfold p f g seed [tail-gen]
     ‘unfold’ is defined as follows:

          (unfold p f g seed) =
             (if (p seed) (tail-gen seed)
                 (cons (f seed)
                       (unfold p f g (g seed))))

     P
          Determines when to stop unfolding.

     F
          Maps each seed value to the corresponding list element.

     G
          Maps each seed value to next seed value.

     SEED
          The state value for the unfold.

     TAIL-GEN
          Creates the tail of the list; defaults to ‘(lambda (x) '())’.

     G produces a series of seed values, which are mapped to list
     elements by F.  These elements are put into a list in left-to-right
     order, and P tells when to stop unfolding.

 -- Scheme Procedure: unfold-right p f g seed [tail]
     Construct a list with the following loop.

          (let lp ((seed seed) (lis tail))
             (if (p seed) lis
                 (lp (g seed)
                     (cons (f seed) lis))))

     P
          Determines when to stop unfolding.

     F
          Maps each seed value to the corresponding list element.

     G
          Maps each seed value to next seed value.

     SEED
          The state value for the unfold.

     TAIL
          The tail of the list; defaults to ‘'()’.

 -- Scheme Procedure: map f lst1 lst2 …
     Map the procedure over the list(s) LST1, LST2, … and return a list
     containing the results of the procedure applications.  This
     procedure is extended with respect to R5RS, because the argument
     lists may have different lengths.  The result list will have the
     same length as the shortest argument lists.  The order in which F
     will be applied to the list element(s) is not specified.

 -- Scheme Procedure: for-each f lst1 lst2 …
     Apply the procedure F to each pair of corresponding elements of the
     list(s) LST1, LST2, ….  The return value is not specified.  This
     procedure is extended with respect to R5RS, because the argument
     lists may have different lengths.  The shortest argument list
     determines the number of times F is called.  F will be applied to
     the list elements in left-to-right order.

 -- Scheme Procedure: append-map f lst1 lst2 …
 -- Scheme Procedure: append-map! f lst1 lst2 …
     Equivalent to

          (apply append (map f clist1 clist2 ...))

     and

          (apply append! (map f clist1 clist2 ...))

     Map F over the elements of the lists, just as in the ‘map’
     function.  However, the results of the applications are appended
     together to make the final result.  ‘append-map’ uses ‘append’ to
     append the results together; ‘append-map!’ uses ‘append!’.

     The dynamic order in which the various applications of F are made
     is not specified.

 -- Scheme Procedure: map! f lst1 lst2 …
     Linear-update variant of ‘map’ – ‘map!’ is allowed, but not
     required, to alter the cons cells of LST1 to construct the result
     list.

     The dynamic order in which the various applications of F are made
     is not specified.  In the n-ary case, LST2, LST3, … must have at
     least as many elements as LST1.

 -- Scheme Procedure: pair-for-each f lst1 lst2 …
     Like ‘for-each’, but applies the procedure F to the pairs from
     which the argument lists are constructed, instead of the list
     elements.  The return value is not specified.

 -- Scheme Procedure: filter-map f lst1 lst2 …
     Like ‘map’, but only results from the applications of F which are
     true are saved in the result list.

7.5.3.6 Filtering and Partitioning
..................................

Filtering means to collect all elements from a list which satisfy a
specific condition.  Partitioning a list means to make two groups of
list elements, one which contains the elements satisfying a condition,
and the other for the elements which don’t.

   The ‘filter’ and ‘filter!’ functions are implemented in the Guile
core, *Note List Modification::.

 -- Scheme Procedure: partition pred lst
 -- Scheme Procedure: partition! pred lst
     Split LST into those elements which do and don’t satisfy the
     predicate PRED.

     The return is two values (*note Multiple Values::), the first being
     a list of all elements from LST which satisfy PRED, the second a
     list of those which do not.

     The elements in the result lists are in the same order as in LST
     but the order in which the calls ‘(PRED elem)’ are made on the list
     elements is unspecified.

     ‘partition’ does not change LST, but one of the returned lists may
     share a tail with it.  ‘partition!’ may modify LST to construct its
     return.

 -- Scheme Procedure: remove pred lst
 -- Scheme Procedure: remove! pred lst
     Return a list containing all elements from LST which do not satisfy
     the predicate PRED.  The elements in the result list have the same
     order as in LST.  The order in which PRED is applied to the list
     elements is not specified.

     ‘remove!’ is allowed, but not required to modify the structure of
     the input list.

7.5.3.7 Searching
.................

The procedures for searching elements in lists either accept a predicate
or a comparison object for determining which elements are to be
searched.

 -- Scheme Procedure: find pred lst
     Return the first element of LST which satisfies the predicate PRED
     and ‘#f’ if no such element is found.

 -- Scheme Procedure: find-tail pred lst
     Return the first pair of LST whose CAR satisfies the predicate PRED
     and ‘#f’ if no such element is found.

 -- Scheme Procedure: take-while pred lst
 -- Scheme Procedure: take-while! pred lst
     Return the longest initial prefix of LST whose elements all satisfy
     the predicate PRED.

     ‘take-while!’ is allowed, but not required to modify the input list
     while producing the result.

 -- Scheme Procedure: drop-while pred lst
     Drop the longest initial prefix of LST whose elements all satisfy
     the predicate PRED.

 -- Scheme Procedure: span pred lst
 -- Scheme Procedure: span! pred lst
 -- Scheme Procedure: break pred lst
 -- Scheme Procedure: break! pred lst
     ‘span’ splits the list LST into the longest initial prefix whose
     elements all satisfy the predicate PRED, and the remaining tail.
     ‘break’ inverts the sense of the predicate.

     ‘span!’ and ‘break!’ are allowed, but not required to modify the
     structure of the input list LST in order to produce the result.

     Note that the name ‘break’ conflicts with the ‘break’ binding
     established by ‘while’ (*note while do::).  Applications wanting to
     use ‘break’ from within a ‘while’ loop will need to make a new
     define under a different name.

 -- Scheme Procedure: any pred lst1 lst2 …
     Test whether any set of elements from LST1 LST2 … satisfies PRED.
     If so, the return value is the return value from the successful
     PRED call, or if not, the return value is ‘#f’.

     If there are n list arguments, then PRED must be a predicate taking
     n arguments.  Each PRED call is ‘(PRED ELEM1 ELEM2 … )’ taking an
     element from each LST.  The calls are made successively for the
     first, second, etc.  elements of the lists, stopping when PRED
     returns non-‘#f’, or when the end of the shortest list is reached.

     The PRED call on the last set of elements (i.e., when the end of
     the shortest list has been reached), if that point is reached, is a
     tail call.

 -- Scheme Procedure: every pred lst1 lst2 …
     Test whether every set of elements from LST1 LST2 … satisfies PRED.
     If so, the return value is the return from the final PRED call, or
     if not, the return value is ‘#f’.

     If there are n list arguments, then PRED must be a predicate taking
     n arguments.  Each PRED call is ‘(PRED ELEM1 ELEM2 …)’ taking an
     element from each LST.  The calls are made successively for the
     first, second, etc.  elements of the lists, stopping if PRED
     returns ‘#f’, or when the end of any of the lists is reached.

     The PRED call on the last set of elements (i.e., when the end of
     the shortest list has been reached) is a tail call.

     If one of LST1 LST2 …is empty then no calls to PRED are made, and
     the return value is ‘#t’.

 -- Scheme Procedure: list-index pred lst1 lst2 …
     Return the index of the first set of elements, one from each of
     LST1 LST2 …, which satisfies PRED.

     PRED is called as ‘(ELEM1 ELEM2 …)’.  Searching stops when the end
     of the shortest LST is reached.  The return index starts from 0 for
     the first set of elements.  If no set of elements pass, then the
     return value is ‘#f’.

          (list-index odd? '(2 4 6 9))      ⇒ 3
          (list-index = '(1 2 3) '(3 1 2))  ⇒ #f

 -- Scheme Procedure: member x lst [=]
     Return the first sublist of LST whose CAR is equal to X.  If X does
     not appear in LST, return ‘#f’.

     Equality is determined by ‘equal?’, or by the equality predicate =
     if given.  = is called ‘(= X elem)’, ie. with the given X first, so
     for example to find the first element greater than 5,

          (member 5 '(3 5 1 7 2 9) <) ⇒ (7 2 9)

     This version of ‘member’ extends the core ‘member’ (*note List
     Searching::) by accepting an equality predicate.

7.5.3.8 Deleting
................

 -- Scheme Procedure: delete x lst [=]
 -- Scheme Procedure: delete! x lst [=]
     Return a list containing the elements of LST but with those equal
     to X deleted.  The returned elements will be in the same order as
     they were in LST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  An equality call is made just once for each element, but
     the order in which the calls are made on the elements is
     unspecified.

     The equality calls are always ‘(= x elem)’, ie. the given X is
     first.  This means for instance elements greater than 5 can be
     deleted with ‘(delete 5 lst <)’.

     ‘delete’ does not modify LST, but the return might share a common
     tail with LST.  ‘delete!’ may modify the structure of LST to
     construct its return.

     These functions extend the core ‘delete’ and ‘delete!’ (*note List
     Modification::) in accepting an equality predicate.  See also
     ‘lset-difference’ (*note SRFI-1 Set Operations::) for deleting
     multiple elements from a list.

 -- Scheme Procedure: delete-duplicates lst [=]
 -- Scheme Procedure: delete-duplicates! lst [=]
     Return a list containing the elements of LST but without
     duplicates.

     When elements are equal, only the first in LST is retained.  Equal
     elements can be anywhere in LST, they don’t have to be adjacent.
     The returned list will have the retained elements in the same order
     as they were in LST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  Calls ‘(= x y)’ are made with element X being before Y in
     LST.  A call is made at most once for each combination, but the
     sequence of the calls across the elements is unspecified.

     ‘delete-duplicates’ does not modify LST, but the return might share
     a common tail with LST.  ‘delete-duplicates!’ may modify the
     structure of LST to construct its return.

     In the worst case, this is an O(N^2) algorithm because it must
     check each element against all those preceding it.  For long lists
     it is more efficient to sort and then compare only adjacent
     elements.

7.5.3.9 Association Lists
.........................

Association lists are described in detail in section *note Association
Lists::.  The present section only documents the additional procedures
for dealing with association lists defined by SRFI-1.

 -- Scheme Procedure: assoc key alist [=]
     Return the pair from ALIST which matches KEY.  This extends the
     core ‘assoc’ (*note Retrieving Alist Entries::) by taking an
     optional = comparison procedure.

     The default comparison is ‘equal?’.  If an = parameter is given
     it’s called ‘(= KEY ALISTCAR)’, i.e. the given target KEY is the
     first argument, and a ‘car’ from ALIST is second.

     For example a case-insensitive string lookup,

          (assoc "yy" '(("XX" . 1) ("YY" . 2)) string-ci=?)
          ⇒ ("YY" . 2)

 -- Scheme Procedure: alist-cons key datum alist
     Cons a new association KEY and DATUM onto ALIST and return the
     result.  This is equivalent to

          (cons (cons KEY DATUM) ALIST)

     ‘acons’ (*note Adding or Setting Alist Entries::) in the Guile core
     does the same thing.

 -- Scheme Procedure: alist-copy alist
     Return a newly allocated copy of ALIST, that means that the spine
     of the list as well as the pairs are copied.

 -- Scheme Procedure: alist-delete key alist [=]
 -- Scheme Procedure: alist-delete! key alist [=]
     Return a list containing the elements of ALIST but with those
     elements whose keys are equal to KEY deleted.  The returned
     elements will be in the same order as they were in ALIST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  The order in which elements are tested is unspecified, but
     each equality call is made ‘(= key alistkey)’, i.e. the given KEY
     parameter is first and the key from ALIST second.  This means for
     instance all associations with a key greater than 5 can be removed
     with ‘(alist-delete 5 alist <)’.

     ‘alist-delete’ does not modify ALIST, but the return might share a
     common tail with ALIST.  ‘alist-delete!’ may modify the list
     structure of ALIST to construct its return.

7.5.3.10 Set Operations on Lists
................................

Lists can be used to represent sets of objects.  The procedures in this
section operate on such lists as sets.

   Note that lists are not an efficient way to implement large sets.
The procedures here typically take time MxN when operating on M and N
element lists.  Other data structures like trees, bitsets (*note Bit
Vectors::) or hash tables (*note Hash Tables::) are faster.

   All these procedures take an equality predicate as the first
argument.  This predicate is used for testing the objects in the list
sets for sameness.  This predicate must be consistent with ‘eq?’ (*note
Equality::) in the sense that if two list elements are ‘eq?’ then they
must also be equal under the predicate.  This simply means a given
object must be equal to itself.

 -- Scheme Procedure: lset<= = list …
     Return ‘#t’ if each list is a subset of the one following it.
     I.e., LIST1 is a subset of LIST2, LIST2 is a subset of LIST3, etc.,
     for as many lists as given.  If only one list or no lists are
     given, the return value is ‘#t’.

     A list X is a subset of Y if each element of X is equal to some
     element in Y.  Elements are compared using the given = procedure,
     called as ‘(= xelem yelem)’.

          (lset<= eq?)                      ⇒ #t
          (lset<= eqv? '(1 2 3) '(1))       ⇒ #f
          (lset<= eqv? '(1 3 2) '(4 3 1 2)) ⇒ #t

 -- Scheme Procedure: lset= = list …
     Return ‘#t’ if all argument lists are set-equal.  LIST1 is compared
     to LIST2, LIST2 to LIST3, etc., for as many lists as given.  If
     only one list or no lists are given, the return value is ‘#t’.

     Two lists X and Y are set-equal if each element of X is equal to
     some element of Y and conversely each element of Y is equal to some
     element of X.  The order of the elements in the lists doesn’t
     matter.  Element equality is determined with the given = procedure,
     called as ‘(= xelem yelem)’, but exactly which calls are made is
     unspecified.

          (lset= eq?)                      ⇒ #t
          (lset= eqv? '(1 2 3) '(3 2 1))   ⇒ #t
          (lset= string-ci=? '("a" "A" "b") '("B" "b" "a")) ⇒ #t

 -- Scheme Procedure: lset-adjoin = list elem …
     Add to LIST any of the given ELEMs not already in the list.  ELEMs
     are ‘cons’ed onto the start of LIST (so the return value shares a
     common tail with LIST), but the order that the ELEMs are added is
     unspecified.

     The given = procedure is used for comparing elements, called as ‘(=
     listelem elem)’, i.e., the second argument is one of the given ELEM
     parameters.

          (lset-adjoin eqv? '(1 2 3) 4 1 5) ⇒ (5 4 1 2 3)

 -- Scheme Procedure: lset-union = list …
 -- Scheme Procedure: lset-union! = list …
     Return the union of the argument list sets.  The result is built by
     taking the union of LIST1 and LIST2, then the union of that with
     LIST3, etc., for as many lists as given.  For one list argument
     that list itself is the result, for no list arguments the result is
     the empty list.

     The union of two lists X and Y is formed as follows.  If X is empty
     then the result is Y.  Otherwise start with X as the result and
     consider each Y element (from first to last).  A Y element not
     equal to something already in the result is ‘cons’ed onto the
     result.

     The given = procedure is used for comparing elements, called as ‘(=
     relem yelem)’.  The first argument is from the result accumulated
     so far, and the second is from the list being union-ed in.  But
     exactly which calls are made is otherwise unspecified.

     Notice that duplicate elements in LIST1 (or the first non-empty
     list) are preserved, but that repeated elements in subsequent lists
     are only added once.

          (lset-union eqv?)                          ⇒ ()
          (lset-union eqv? '(1 2 3))                 ⇒ (1 2 3)
          (lset-union eqv? '(1 2 1 3) '(2 4 5) '(5)) ⇒ (5 4 1 2 1 3)

     ‘lset-union’ doesn’t change the given lists but the result may
     share a tail with the first non-empty list.  ‘lset-union!’ can
     modify all of the given lists to form the result.

 -- Scheme Procedure: lset-intersection = list1 list2 …
 -- Scheme Procedure: lset-intersection! = list1 list2 …
     Return the intersection of LIST1 with the other argument lists,
     meaning those elements of LIST1 which are also in all of LIST2 etc.
     For one list argument, just that list is returned.

     The test for an element of LIST1 to be in the return is simply that
     it’s equal to some element in each of LIST2 etc.  Notice this means
     an element appearing twice in LIST1 but only once in each of LIST2
     etc will go into the return twice.  The return has its elements in
     the same order as they were in LIST1.

     The given = procedure is used for comparing elements, called as ‘(=
     elem1 elemN)’.  The first argument is from LIST1 and the second is
     from one of the subsequent lists.  But exactly which calls are made
     and in what order is unspecified.

          (lset-intersection eqv? '(x y))                        ⇒ (x y)
          (lset-intersection eqv? '(1 2 3) '(4 3 2))             ⇒ (2 3)
          (lset-intersection eqv? '(1 1 2 2) '(1 2) '(2 1) '(2)) ⇒ (2 2)

     The return from ‘lset-intersection’ may share a tail with LIST1.
     ‘lset-intersection!’ may modify LIST1 to form its result.

 -- Scheme Procedure: lset-difference = list1 list2 …
 -- Scheme Procedure: lset-difference! = list1 list2 …
     Return LIST1 with any elements in LIST2, LIST3 etc removed (ie.
     subtracted).  For one list argument, just that list is returned.

     The given = procedure is used for comparing elements, called as ‘(=
     elem1 elemN)’.  The first argument is from LIST1 and the second
     from one of the subsequent lists.  But exactly which calls are made
     and in what order is unspecified.

          (lset-difference eqv? '(x y))             ⇒ (x y)
          (lset-difference eqv? '(1 2 3) '(3 1))    ⇒ (2)
          (lset-difference eqv? '(1 2 3) '(3) '(2)) ⇒ (1)

     The return from ‘lset-difference’ may share a tail with LIST1.
     ‘lset-difference!’ may modify LIST1 to form its result.

 -- Scheme Procedure: lset-diff+intersection = list1 list2 …
 -- Scheme Procedure: lset-diff+intersection! = list1 list2 …
     Return two values (*note Multiple Values::), the difference and
     intersection of the argument lists as per ‘lset-difference’ and
     ‘lset-intersection’ above.

     For two list arguments this partitions LIST1 into those elements of
     LIST1 which are in LIST2 and not in LIST2.  (But for more than two
     arguments there can be elements of LIST1 which are neither part of
     the difference nor the intersection.)

     One of the return values from ‘lset-diff+intersection’ may share a
     tail with LIST1.  ‘lset-diff+intersection!’ may modify LIST1 to
     form its results.

 -- Scheme Procedure: lset-xor = list …
 -- Scheme Procedure: lset-xor! = list …
     Return an XOR of the argument lists.  For two lists this means
     those elements which are in exactly one of the lists.  For more
     than two lists it means those elements which appear in an odd
     number of the lists.

     To be precise, the XOR of two lists X and Y is formed by taking
     those elements of X not equal to any element of Y, plus those
     elements of Y not equal to any element of X.  Equality is
     determined with the given = procedure, called as ‘(= e1 e2)’.  One
     argument is from X and the other from Y, but which way around is
     unspecified.  Exactly which calls are made is also unspecified, as
     is the order of the elements in the result.

          (lset-xor eqv? '(x y))             ⇒ (x y)
          (lset-xor eqv? '(1 2 3) '(4 3 2))  ⇒ (4 1)

     The return from ‘lset-xor’ may share a tail with one of the list
     arguments.  ‘lset-xor!’ may modify LIST1 to form its result.

7.5.4 SRFI-2 - and-let*
-----------------------

The following syntax can be obtained with

     (use-modules (srfi srfi-2))

   or alternatively

     (use-modules (ice-9 and-let-star))

 -- library syntax: and-let* (clause …) body …
     A combination of ‘and’ and ‘let*’.

     Each CLAUSE is evaluated in turn, and if ‘#f’ is obtained then
     evaluation stops and ‘#f’ is returned.  If all are non-‘#f’ then
     BODY is evaluated and the last form gives the return value, or if
     BODY is empty then the result is ‘#t’.  Each CLAUSE should be one
     of the following,

     ‘(symbol expr)’
          Evaluate EXPR, check for ‘#f’, and bind it to SYMBOL.  Like
          ‘let*’, that binding is available to subsequent clauses.
     ‘(expr)’
          Evaluate EXPR and check for ‘#f’.
     ‘symbol’
          Get the value bound to SYMBOL and check for ‘#f’.

     Notice that ‘(expr)’ has an “extra” pair of parentheses, for
     instance ‘((eq? x y))’.  One way to remember this is to imagine the
     ‘symbol’ in ‘(symbol expr)’ is omitted.

     ‘and-let*’ is good for calculations where a ‘#f’ value means
     termination, but where a non-‘#f’ value is going to be needed in
     subsequent expressions.

     The following illustrates this, it returns text between brackets
     ‘[...]’ in a string, or ‘#f’ if there are no such brackets (ie.
     either ‘string-index’ gives ‘#f’).

          (define (extract-brackets str)
            (and-let* ((start (string-index str #\[))
                       (end   (string-index str #\] start)))
              (substring str (1+ start) end)))

     The following shows plain variables and expressions tested too.
     ‘diagnostic-levels’ is taken to be an alist associating a
     diagnostic type with a level.  ‘str’ is printed only if the type is
     known and its level is high enough.

          (define (show-diagnostic type str)
            (and-let* (want-diagnostics
                       (level (assq-ref diagnostic-levels type))
                       ((>= level current-diagnostic-level)))
              (display str)))

     The advantage of ‘and-let*’ is that an extended sequence of
     expressions and tests doesn’t require lots of nesting as would
     arise from separate ‘and’ and ‘let*’, or from ‘cond’ with ‘=>’.

7.5.5 SRFI-4 - Homogeneous numeric vector datatypes
---------------------------------------------------

SRFI-4 provides an interface to uniform numeric vectors: vectors whose
elements are all of a single numeric type.  Guile offers uniform numeric
vectors for signed and unsigned 8-bit, 16-bit, 32-bit, and 64-bit
integers, two sizes of floating point values, and, as an extension to
SRFI-4, complex floating-point numbers of these two sizes.

   The standard SRFI-4 procedures and data types may be included via
loading the appropriate module:

     (use-modules (srfi srfi-4))

   This module is currently a part of the default Guile environment, but
it is a good practice to explicitly import the module.  In the future,
using SRFI-4 procedures without importing the SRFI-4 module will cause a
deprecation message to be printed.  (Of course, one may call the C
functions at any time.  Would that C had modules!)

7.5.5.1 SRFI-4 - Overview
.........................

Uniform numeric vectors can be useful since they consume less memory
than the non-uniform, general vectors.  Also, since the types they can
store correspond directly to C types, it is easier to work with them
efficiently on a low level.  Consider image processing as an example,
where you want to apply a filter to some image.  While you could store
the pixels of an image in a general vector and write a general
convolution function, things are much more efficient with uniform
vectors: the convolution function knows that all pixels are unsigned
8-bit values (say), and can use a very tight inner loop.

   This is implemented in Scheme by having the compiler notice calls to
the SRFI-4 accessors, and inline them to appropriate compiled code.
From C you have access to the raw array; functions for efficiently
working with uniform numeric vectors from C are listed at the end of
this section.

   Uniform numeric vectors are the special case of one dimensional
uniform numeric arrays.

   There are 12 standard kinds of uniform numeric vectors, and they all
have their own complement of constructors, accessors, and so on.
Procedures that operate on a specific kind of uniform numeric vector
have a “tag” in their name, indicating the element type.

u8
     unsigned 8-bit integers

s8
     signed 8-bit integers

u16
     unsigned 16-bit integers

s16
     signed 16-bit integers

u32
     unsigned 32-bit integers

s32
     signed 32-bit integers

u64
     unsigned 64-bit integers

s64
     signed 64-bit integers

f32
     the C type ‘float’

f64
     the C type ‘double’

   In addition, Guile supports uniform arrays of complex numbers, with
the nonstandard tags:

c32
     complex numbers in rectangular form with the real and imaginary
     part being a ‘float’

c64
     complex numbers in rectangular form with the real and imaginary
     part being a ‘double’

   The external representation (ie. read syntax) for these vectors is
similar to normal Scheme vectors, but with an additional tag from the
tables above indicating the vector’s type.  For example,

     #u16(1 2 3)
     #f64(3.1415 2.71)

   Note that the read syntax for floating-point here conflicts with ‘#f’
for false.  In Standard Scheme one can write ‘(1 #f3)’ for a three
element list ‘(1 #f 3)’, but for Guile ‘(1 #f3)’ is invalid.  ‘(1 #f 3)’
is almost certainly what one should write anyway to make the intention
clear, so this is rarely a problem.

7.5.5.2 SRFI-4 - API
....................

Note that the c32 and c64 functions are only available from (srfi srfi-4
gnu).

 -- Scheme Procedure: u8vector? obj
 -- Scheme Procedure: s8vector? obj
 -- Scheme Procedure: u16vector? obj
 -- Scheme Procedure: s16vector? obj
 -- Scheme Procedure: u32vector? obj
 -- Scheme Procedure: s32vector? obj
 -- Scheme Procedure: u64vector? obj
 -- Scheme Procedure: s64vector? obj
 -- Scheme Procedure: f32vector? obj
 -- Scheme Procedure: f64vector? obj
 -- Scheme Procedure: c32vector? obj
 -- Scheme Procedure: c64vector? obj
 -- C Function: scm_u8vector_p (obj)
 -- C Function: scm_s8vector_p (obj)
 -- C Function: scm_u16vector_p (obj)
 -- C Function: scm_s16vector_p (obj)
 -- C Function: scm_u32vector_p (obj)
 -- C Function: scm_s32vector_p (obj)
 -- C Function: scm_u64vector_p (obj)
 -- C Function: scm_s64vector_p (obj)
 -- C Function: scm_f32vector_p (obj)
 -- C Function: scm_f64vector_p (obj)
 -- C Function: scm_c32vector_p (obj)
 -- C Function: scm_c64vector_p (obj)
     Return ‘#t’ if OBJ is a homogeneous numeric vector of the indicated
     type.

 -- Scheme Procedure: make-u8vector n [value]
 -- Scheme Procedure: make-s8vector n [value]
 -- Scheme Procedure: make-u16vector n [value]
 -- Scheme Procedure: make-s16vector n [value]
 -- Scheme Procedure: make-u32vector n [value]
 -- Scheme Procedure: make-s32vector n [value]
 -- Scheme Procedure: make-u64vector n [value]
 -- Scheme Procedure: make-s64vector n [value]
 -- Scheme Procedure: make-f32vector n [value]
 -- Scheme Procedure: make-f64vector n [value]
 -- Scheme Procedure: make-c32vector n [value]
 -- Scheme Procedure: make-c64vector n [value]
 -- C Function: scm_make_u8vector (n, value)
 -- C Function: scm_make_s8vector (n, value)
 -- C Function: scm_make_u16vector (n, value)
 -- C Function: scm_make_s16vector (n, value)
 -- C Function: scm_make_u32vector (n, value)
 -- C Function: scm_make_s32vector (n, value)
 -- C Function: scm_make_u64vector (n, value)
 -- C Function: scm_make_s64vector (n, value)
 -- C Function: scm_make_f32vector (n, value)
 -- C Function: scm_make_f64vector (n, value)
 -- C Function: scm_make_c32vector (n, value)
 -- C Function: scm_make_c64vector (n, value)
     Return a newly allocated homogeneous numeric vector holding N
     elements of the indicated type.  If VALUE is given, the vector is
     initialized with that value, otherwise the contents are
     unspecified.

 -- Scheme Procedure: u8vector value …
 -- Scheme Procedure: s8vector value …
 -- Scheme Procedure: u16vector value …
 -- Scheme Procedure: s16vector value …
 -- Scheme Procedure: u32vector value …
 -- Scheme Procedure: s32vector value …
 -- Scheme Procedure: u64vector value …
 -- Scheme Procedure: s64vector value …
 -- Scheme Procedure: f32vector value …
 -- Scheme Procedure: f64vector value …
 -- Scheme Procedure: c32vector value …
 -- Scheme Procedure: c64vector value …
 -- C Function: scm_u8vector (values)
 -- C Function: scm_s8vector (values)
 -- C Function: scm_u16vector (values)
 -- C Function: scm_s16vector (values)
 -- C Function: scm_u32vector (values)
 -- C Function: scm_s32vector (values)
 -- C Function: scm_u64vector (values)
 -- C Function: scm_s64vector (values)
 -- C Function: scm_f32vector (values)
 -- C Function: scm_f64vector (values)
 -- C Function: scm_c32vector (values)
 -- C Function: scm_c64vector (values)
     Return a newly allocated homogeneous numeric vector of the
     indicated type, holding the given parameter VALUEs.  The vector
     length is the number of parameters given.

 -- Scheme Procedure: u8vector-length vec
 -- Scheme Procedure: s8vector-length vec
 -- Scheme Procedure: u16vector-length vec
 -- Scheme Procedure: s16vector-length vec
 -- Scheme Procedure: u32vector-length vec
 -- Scheme Procedure: s32vector-length vec
 -- Scheme Procedure: u64vector-length vec
 -- Scheme Procedure: s64vector-length vec
 -- Scheme Procedure: f32vector-length vec
 -- Scheme Procedure: f64vector-length vec
 -- Scheme Procedure: c32vector-length vec
 -- Scheme Procedure: c64vector-length vec
 -- C Function: scm_u8vector_length (vec)
 -- C Function: scm_s8vector_length (vec)
 -- C Function: scm_u16vector_length (vec)
 -- C Function: scm_s16vector_length (vec)
 -- C Function: scm_u32vector_length (vec)
 -- C Function: scm_s32vector_length (vec)
 -- C Function: scm_u64vector_length (vec)
 -- C Function: scm_s64vector_length (vec)
 -- C Function: scm_f32vector_length (vec)
 -- C Function: scm_f64vector_length (vec)
 -- C Function: scm_c32vector_length (vec)
 -- C Function: scm_c64vector_length (vec)
     Return the number of elements in VEC.

 -- Scheme Procedure: u8vector-ref vec i
 -- Scheme Procedure: s8vector-ref vec i
 -- Scheme Procedure: u16vector-ref vec i
 -- Scheme Procedure: s16vector-ref vec i
 -- Scheme Procedure: u32vector-ref vec i
 -- Scheme Procedure: s32vector-ref vec i
 -- Scheme Procedure: u64vector-ref vec i
 -- Scheme Procedure: s64vector-ref vec i
 -- Scheme Procedure: f32vector-ref vec i
 -- Scheme Procedure: f64vector-ref vec i
 -- Scheme Procedure: c32vector-ref vec i
 -- Scheme Procedure: c64vector-ref vec i
 -- C Function: scm_u8vector_ref (vec, i)
 -- C Function: scm_s8vector_ref (vec, i)
 -- C Function: scm_u16vector_ref (vec, i)
 -- C Function: scm_s16vector_ref (vec, i)
 -- C Function: scm_u32vector_ref (vec, i)
 -- C Function: scm_s32vector_ref (vec, i)
 -- C Function: scm_u64vector_ref (vec, i)
 -- C Function: scm_s64vector_ref (vec, i)
 -- C Function: scm_f32vector_ref (vec, i)
 -- C Function: scm_f64vector_ref (vec, i)
 -- C Function: scm_c32vector_ref (vec, i)
 -- C Function: scm_c64vector_ref (vec, i)
     Return the element at index I in VEC.  The first element in VEC is
     index 0.

 -- Scheme Procedure: u8vector-set! vec i value
 -- Scheme Procedure: s8vector-set! vec i value
 -- Scheme Procedure: u16vector-set! vec i value
 -- Scheme Procedure: s16vector-set! vec i value
 -- Scheme Procedure: u32vector-set! vec i value
 -- Scheme Procedure: s32vector-set! vec i value
 -- Scheme Procedure: u64vector-set! vec i value
 -- Scheme Procedure: s64vector-set! vec i value
 -- Scheme Procedure: f32vector-set! vec i value
 -- Scheme Procedure: f64vector-set! vec i value
 -- Scheme Procedure: c32vector-set! vec i value
 -- Scheme Procedure: c64vector-set! vec i value
 -- C Function: scm_u8vector_set_x (vec, i, value)
 -- C Function: scm_s8vector_set_x (vec, i, value)
 -- C Function: scm_u16vector_set_x (vec, i, value)
 -- C Function: scm_s16vector_set_x (vec, i, value)
 -- C Function: scm_u32vector_set_x (vec, i, value)
 -- C Function: scm_s32vector_set_x (vec, i, value)
 -- C Function: scm_u64vector_set_x (vec, i, value)
 -- C Function: scm_s64vector_set_x (vec, i, value)
 -- C Function: scm_f32vector_set_x (vec, i, value)
 -- C Function: scm_f64vector_set_x (vec, i, value)
 -- C Function: scm_c32vector_set_x (vec, i, value)
 -- C Function: scm_c64vector_set_x (vec, i, value)
     Set the element at index I in VEC to VALUE.  The first element in
     VEC is index 0.  The return value is unspecified.

 -- Scheme Procedure: u8vector->list vec
 -- Scheme Procedure: s8vector->list vec
 -- Scheme Procedure: u16vector->list vec
 -- Scheme Procedure: s16vector->list vec
 -- Scheme Procedure: u32vector->list vec
 -- Scheme Procedure: s32vector->list vec
 -- Scheme Procedure: u64vector->list vec
 -- Scheme Procedure: s64vector->list vec
 -- Scheme Procedure: f32vector->list vec
 -- Scheme Procedure: f64vector->list vec
 -- Scheme Procedure: c32vector->list vec
 -- Scheme Procedure: c64vector->list vec
 -- C Function: scm_u8vector_to_list (vec)
 -- C Function: scm_s8vector_to_list (vec)
 -- C Function: scm_u16vector_to_list (vec)
 -- C Function: scm_s16vector_to_list (vec)
 -- C Function: scm_u32vector_to_list (vec)
 -- C Function: scm_s32vector_to_list (vec)
 -- C Function: scm_u64vector_to_list (vec)
 -- C Function: scm_s64vector_to_list (vec)
 -- C Function: scm_f32vector_to_list (vec)
 -- C Function: scm_f64vector_to_list (vec)
 -- C Function: scm_c32vector_to_list (vec)
 -- C Function: scm_c64vector_to_list (vec)
     Return a newly allocated list holding all elements of VEC.

 -- Scheme Procedure: list->u8vector lst
 -- Scheme Procedure: list->s8vector lst
 -- Scheme Procedure: list->u16vector lst
 -- Scheme Procedure: list->s16vector lst
 -- Scheme Procedure: list->u32vector lst
 -- Scheme Procedure: list->s32vector lst
 -- Scheme Procedure: list->u64vector lst
 -- Scheme Procedure: list->s64vector lst
 -- Scheme Procedure: list->f32vector lst
 -- Scheme Procedure: list->f64vector lst
 -- Scheme Procedure: list->c32vector lst
 -- Scheme Procedure: list->c64vector lst
 -- C Function: scm_list_to_u8vector (lst)
 -- C Function: scm_list_to_s8vector (lst)
 -- C Function: scm_list_to_u16vector (lst)
 -- C Function: scm_list_to_s16vector (lst)
 -- C Function: scm_list_to_u32vector (lst)
 -- C Function: scm_list_to_s32vector (lst)
 -- C Function: scm_list_to_u64vector (lst)
 -- C Function: scm_list_to_s64vector (lst)
 -- C Function: scm_list_to_f32vector (lst)
 -- C Function: scm_list_to_f64vector (lst)
 -- C Function: scm_list_to_c32vector (lst)
 -- C Function: scm_list_to_c64vector (lst)
     Return a newly allocated homogeneous numeric vector of the
     indicated type, initialized with the elements of the list LST.

 -- C Function: SCM scm_take_u8vector (const scm_t_uint8 *data, size_t
          len)
 -- C Function: SCM scm_take_s8vector (const scm_t_int8 *data, size_t
          len)
 -- C Function: SCM scm_take_u16vector (const scm_t_uint16 *data, size_t
          len)
 -- C Function: SCM scm_take_s16vector (const scm_t_int16 *data, size_t
          len)
 -- C Function: SCM scm_take_u32vector (const scm_t_uint32 *data, size_t
          len)
 -- C Function: SCM scm_take_s32vector (const scm_t_int32 *data, size_t
          len)
 -- C Function: SCM scm_take_u64vector (const scm_t_uint64 *data, size_t
          len)
 -- C Function: SCM scm_take_s64vector (const scm_t_int64 *data, size_t
          len)
 -- C Function: SCM scm_take_f32vector (const float *data, size_t len)
 -- C Function: SCM scm_take_f64vector (const double *data, size_t len)
 -- C Function: SCM scm_take_c32vector (const float *data, size_t len)
 -- C Function: SCM scm_take_c64vector (const double *data, size_t len)
     Return a new uniform numeric vector of the indicated type and
     length that uses the memory pointed to by DATA to store its
     elements.  This memory will eventually be freed with ‘free’.  The
     argument LEN specifies the number of elements in DATA, not its size
     in bytes.

     The ‘c32’ and ‘c64’ variants take a pointer to a C array of
     ‘float’s or ‘double’s.  The real parts of the complex numbers are
     at even indices in that array, the corresponding imaginary parts
     are at the following odd index.

 -- C Function: const scm_t_uint8 * scm_u8vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int8 * scm_s8vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint16 * scm_u16vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int16 * scm_s16vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint32 * scm_u32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int32 * scm_s32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint64 * scm_u64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int64 * scm_s64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const float * scm_f32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const double * scm_f64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const float * scm_c32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const double * scm_c64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
     Like ‘scm_vector_elements’ (*note Vector Accessing from C::), but
     returns a pointer to the elements of a uniform numeric vector of
     the indicated kind.

 -- C Function: scm_t_uint8 * scm_u8vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int8 * scm_s8vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint16 * scm_u16vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int16 * scm_s16vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint32 * scm_u32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int32 * scm_s32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint64 * scm_u64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int64 * scm_s64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: float * scm_f32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: double * scm_f64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: float * scm_c32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: double * scm_c64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
     Like ‘scm_vector_writable_elements’ (*note Vector Accessing from
     C::), but returns a pointer to the elements of a uniform numeric
     vector of the indicated kind.

7.5.5.3 SRFI-4 - Relation to bytevectors
........................................

Guile implements SRFI-4 vectors using bytevectors (*note Bytevectors::).
Often when you have a numeric vector, you end up wanting to write its
bytes somewhere, or have access to the underlying bytes, or read in
bytes from somewhere else.  Bytevectors are very good at this sort of
thing.  But the SRFI-4 APIs are nicer to use when doing
number-crunching, because they are addressed by element and not by byte.

   So as a compromise, Guile allows all bytevector functions to operate
on numeric vectors.  They address the underlying bytes in the native
endianness, as one would expect.

   Following the same reasoning, that it’s just bytes underneath, Guile
also allows uniform vectors of a given type to be accessed as if they
were of any type.  One can fill a u32vector, and access its elements
with u8vector-ref.  One can use f64vector-ref on bytevectors.  It’s all
the same to Guile.

   In this way, uniform numeric vectors may be written to and read from
input/output ports using the procedures that operate on bytevectors.

   *Note Bytevectors::, for more information.

7.5.5.4 SRFI-4 - Guile extensions
.................................

Guile defines some useful extensions to SRFI-4, which are not available
in the default Guile environment.  They may be imported by loading the
extensions module:

     (use-modules (srfi srfi-4 gnu))

 -- Scheme Procedure: any->u8vector obj
 -- Scheme Procedure: any->s8vector obj
 -- Scheme Procedure: any->u16vector obj
 -- Scheme Procedure: any->s16vector obj
 -- Scheme Procedure: any->u32vector obj
 -- Scheme Procedure: any->s32vector obj
 -- Scheme Procedure: any->u64vector obj
 -- Scheme Procedure: any->s64vector obj
 -- Scheme Procedure: any->f32vector obj
 -- Scheme Procedure: any->f64vector obj
 -- Scheme Procedure: any->c32vector obj
 -- Scheme Procedure: any->c64vector obj
 -- C Function: scm_any_to_u8vector (obj)
 -- C Function: scm_any_to_s8vector (obj)
 -- C Function: scm_any_to_u16vector (obj)
 -- C Function: scm_any_to_s16vector (obj)
 -- C Function: scm_any_to_u32vector (obj)
 -- C Function: scm_any_to_s32vector (obj)
 -- C Function: scm_any_to_u64vector (obj)
 -- C Function: scm_any_to_s64vector (obj)
 -- C Function: scm_any_to_f32vector (obj)
 -- C Function: scm_any_to_f64vector (obj)
 -- C Function: scm_any_to_c32vector (obj)
 -- C Function: scm_any_to_c64vector (obj)
     Return a (maybe newly allocated) uniform numeric vector of the
     indicated type, initialized with the elements of OBJ, which must be
     a list, a vector, or a uniform vector.  When OBJ is already a
     suitable uniform numeric vector, it is returned unchanged.

7.5.6 SRFI-6 - Basic String Ports
---------------------------------

SRFI-6 defines the procedures ‘open-input-string’, ‘open-output-string’
and ‘get-output-string’.

   Note that although versions of these procedures are included in the
Guile core, the core versions are not fully conformant with SRFI-6:
attempts to read or write characters that are not supported by the
current ‘%default-port-encoding’ will fail.

   We therefore recommend that you import this module, which supports
all characters:

     (use-modules (srfi srfi-6))

7.5.7 SRFI-8 - receive
----------------------

‘receive’ is a syntax for making the handling of multiple-value
procedures easier.  It is documented in *Note Multiple Values::.

7.5.8 SRFI-9 - define-record-type
---------------------------------

This SRFI is a syntax for defining new record types and creating
predicate, constructor, and field getter and setter functions.  It is
documented in the “Compound Data Types” section of the manual (*note
SRFI-9 Records::).

7.5.9 SRFI-10 - Hash-Comma Reader Extension
-------------------------------------------

This SRFI implements a reader extension ‘#,()’ called hash-comma.  It
allows the reader to give new kinds of objects, for use both in data and
as constants or literals in source code.  This feature is available with

     (use-modules (srfi srfi-10))

The new read syntax is of the form

     #,(TAG ARG…)

where TAG is a symbol and the ARGs are objects taken as parameters.
TAGs are registered with the following procedure.

 -- Scheme Procedure: define-reader-ctor tag proc
     Register PROC as the constructor for a hash-comma read syntax
     starting with symbol TAG, i.e. #,(TAG arg…).  PROC is called with
     the given arguments ‘(PROC arg…)’ and the object it returns is the
     result of the read.

For example, a syntax giving a list of N copies of an object.

     (define-reader-ctor 'repeat
       (lambda (obj reps)
         (make-list reps obj)))

     (display '#,(repeat 99 3))
     ⊣ (99 99 99)

   Notice the quote ’ when the #,( ) is used.  The ‘repeat’ handler
returns a list and the program must quote to use it literally, the same
as any other list.  Ie.

     (display '#,(repeat 99 3))
     ⇒
     (display '(99 99 99))

   When a handler returns an object which is self-evaluating, like a
number or a string, then there’s no need for quoting, just as there’s no
need when giving those directly as literals.  For example an addition,

     (define-reader-ctor 'sum
       (lambda (x y)
         (+ x y)))
     (display #,(sum 123 456)) ⊣ 579

   A typical use for #,() is to get a read syntax for objects which
don’t otherwise have one.  For example, the following allows a hash
table to be given literally, with tags and values, ready for fast
lookup.

     (define-reader-ctor 'hash
       (lambda elems
         (let ((table (make-hash-table)))
           (for-each (lambda (elem)
                       (apply hash-set! table elem))
                     elems)
           table)))

     (define (animal->family animal)
       (hash-ref '#,(hash ("tiger" "cat")
                          ("lion"  "cat")
                          ("wolf"  "dog"))
                 animal))

     (animal->family "lion") ⇒ "cat"

   Or for example the following is a syntax for a compiled regular
expression (*note Regular Expressions::).

     (use-modules (ice-9 regex))

     (define-reader-ctor 'regexp make-regexp)

     (define (extract-angs str)
       (let ((match (regexp-exec '#,(regexp "<([A-Z0-9]+)>") str)))
         (and match
              (match:substring match 1))))

     (extract-angs "foo <BAR> quux") ⇒ "BAR"


   #,() is somewhat similar to ‘define-macro’ (*note Macros::) in that
handler code is run to produce a result, but #,() operates at the read
stage, so it can appear in data for ‘read’ (*note Scheme Read::), not
just in code to be executed.

   Because #,() is handled at read-time it has no direct access to
variables etc.  A symbol in the arguments is just a symbol, not a
variable reference.  The arguments are essentially constants, though the
handler procedure can use them in any complicated way it might want.

   Once ‘(srfi srfi-10)’ has loaded, #,() is available globally, there’s
no need to use ‘(srfi srfi-10)’ in later modules.  Similarly the tags
registered are global and can be used anywhere once registered.

   There’s no attempt to record what previous #,() forms have been seen,
if two identical forms occur then two calls are made to the handler
procedure.  The handler might like to maintain a cache or similar to
avoid making copies of large objects, depending on expected usage.

   In code the best uses of #,() are generally when there’s a lot of
objects of a particular kind as literals or constants.  If there’s just
a few then some local variables and initializers are fine, but that
becomes tedious and error prone when there’s a lot, and the anonymous
and compact syntax of #,() is much better.

7.5.10 SRFI-11 - let-values
---------------------------

This module implements the binding forms for multiple values
‘let-values’ and ‘let*-values’.  These forms are similar to ‘let’ and
‘let*’ (*note Local Bindings::), but they support binding of the values
returned by multiple-valued expressions.

   Write ‘(use-modules (srfi srfi-11))’ to make the bindings available.

     (let-values (((x y) (values 1 2))
                  ((z f) (values 3 4)))
        (+ x y z f))
     ⇒
     10

   ‘let-values’ performs all bindings simultaneously, which means that
no expression in the binding clauses may refer to variables bound in the
same clause list.  ‘let*-values’, on the other hand, performs the
bindings sequentially, just like ‘let*’ does for single-valued
expressions.

7.5.11 SRFI-13 - String Library
-------------------------------

The SRFI-13 procedures are always available, *Note Strings::.

7.5.12 SRFI-14 - Character-set Library
--------------------------------------

The SRFI-14 data type and procedures are always available, *Note
Character Sets::.

7.5.13 SRFI-16 - case-lambda
----------------------------

SRFI-16 defines a variable-arity ‘lambda’ form, ‘case-lambda’.  This
form is available in the default Guile environment.  *Note
Case-lambda::, for more information.

7.5.14 SRFI-17 - Generalized set!
---------------------------------

This SRFI implements a generalized ‘set!’, allowing some “referencing”
functions to be used as the target location of a ‘set!’.  This feature
is available from

     (use-modules (srfi srfi-17))

For example ‘vector-ref’ is extended so that

     (set! (vector-ref vec idx) new-value)

is equivalent to

     (vector-set! vec idx new-value)

   The idea is that a ‘vector-ref’ expression identifies a location,
which may be either fetched or stored.  The same form is used for the
location in both cases, encouraging visual clarity.  This is similar to
the idea of an “lvalue” in C.

   The mechanism for this kind of ‘set!’ is in the Guile core (*note
Procedures with Setters::).  This module adds definitions of the
following functions as procedures with setters, allowing them to be
targets of a ‘set!’,

     car, cdr, caar, cadr, cdar, cddr, caaar, caadr, cadar, caddr,
     cdaar, cdadr, cddar, cdddr, caaaar, caaadr, caadar, caaddr, cadaar,
     cadadr, caddar, cadddr, cdaaar, cdaadr, cdadar, cdaddr, cddaar,
     cddadr, cdddar, cddddr

     string-ref, vector-ref

   The SRFI specifies ‘setter’ (*note Procedures with Setters::) as a
procedure with setter, allowing the setter for a procedure to be
changed, eg. ‘(set! (setter foo) my-new-setter-handler)’.  Currently
Guile does not implement this, a setter can only be specified on
creation (‘getter-with-setter’ below).

 -- Function: getter-with-setter
     The same as the Guile core ‘make-procedure-with-setter’ (*note
     Procedures with Setters::).

7.5.15 SRFI-18 - Multithreading support
---------------------------------------

This is an implementation of the SRFI-18 threading and synchronization
library.  The functions and variables described here are provided by

     (use-modules (srfi srfi-18))

   As a general rule, the data types and functions in this SRFI-18
implementation are compatible with the types and functions in Guile’s
core threading code.  For example, mutexes created with the SRFI-18
‘make-mutex’ function can be passed to the built-in Guile function
‘lock-mutex’ (*note Mutexes and Condition Variables::), and mutexes
created with the built-in Guile function ‘make-mutex’ can be passed to
the SRFI-18 function ‘mutex-lock!’.  Cases in which this does not hold
true are noted in the following sections.

7.5.15.1 SRFI-18 Threads
........................

Threads created by SRFI-18 differ in two ways from threads created by
Guile’s built-in thread functions.  First, a thread created by SRFI-18
‘make-thread’ begins in a blocked state and will not start execution
until ‘thread-start!’ is called on it.  Second, SRFI-18 threads are
constructed with a top-level exception handler that captures any
exceptions that are thrown on thread exit.  In all other regards,
SRFI-18 threads are identical to normal Guile threads.

 -- Function: current-thread
     Returns the thread that called this function.  This is the same
     procedure as the same-named built-in procedure ‘current-thread’
     (*note Threads::).

 -- Function: thread? obj
     Returns ‘#t’ if OBJ is a thread, ‘#f’ otherwise.  This is the same
     procedure as the same-named built-in procedure ‘thread?’ (*note
     Threads::).

 -- Function: make-thread thunk [name]
     Call ‘thunk’ in a new thread and with a new dynamic state,
     returning the new thread and optionally assigning it the object
     name NAME, which may be any Scheme object.

     Note that the name ‘make-thread’ conflicts with the ‘(ice-9
     threads)’ function ‘make-thread’.  Applications wanting to use both
     of these functions will need to refer to them by different names.

 -- Function: thread-name thread
     Returns the name assigned to THREAD at the time of its creation, or
     ‘#f’ if it was not given a name.

 -- Function: thread-specific thread
 -- Function: thread-specific-set! thread obj
     Get or set the “object-specific” property of THREAD.  In Guile’s
     implementation of SRFI-18, this value is stored as an object
     property, and will be ‘#f’ if not set.

 -- Function: thread-start! thread
     Unblocks THREAD and allows it to begin execution if it has not done
     so already.

 -- Function: thread-yield!
     If one or more threads are waiting to execute, calling
     ‘thread-yield!’ forces an immediate context switch to one of them.
     Otherwise, ‘thread-yield!’ has no effect.  ‘thread-yield!’ behaves
     identically to the Guile built-in function ‘yield’.

 -- Function: thread-sleep! timeout
     The current thread waits until the point specified by the time
     object TIMEOUT is reached (*note SRFI-18 Time::).  This blocks the
     thread only if TIMEOUT represents a point in the future.  it is an
     error for TIMEOUT to be ‘#f’.

 -- Function: thread-terminate! thread
     Causes an abnormal termination of THREAD.  If THREAD is not already
     terminated, all mutexes owned by THREAD become unlocked/abandoned.
     If THREAD is the current thread, ‘thread-terminate!’ does not
     return.  Otherwise ‘thread-terminate!’ returns an unspecified
     value; the termination of THREAD will occur before
     ‘thread-terminate!’ returns.  Subsequent attempts to join on THREAD
     will cause a “terminated thread exception” to be raised.

     ‘thread-terminate!’ is compatible with the thread cancellation
     procedures in the core threads API (*note Threads::) in that if a
     cleanup handler has been installed for the target thread, it will
     be called before the thread exits and its return value (or
     exception, if any) will be stored for later retrieval via a call to
     ‘thread-join!’.

 -- Function: thread-join! thread [timeout [timeout-val]]
     Wait for THREAD to terminate and return its exit value.  When a
     time value TIMEOUT is given, it specifies a point in time where the
     waiting should be aborted.  When the waiting is aborted,
     TIMEOUT-VAL is returned if it is specified; otherwise, a
     ‘join-timeout-exception’ exception is raised (*note SRFI-18
     Exceptions::).  Exceptions may also be raised if the thread was
     terminated by a call to ‘thread-terminate!’
     (‘terminated-thread-exception’ will be raised) or if the thread
     exited by raising an exception that was handled by the top-level
     exception handler (‘uncaught-exception’ will be raised; the
     original exception can be retrieved using
     ‘uncaught-exception-reason’).

7.5.15.2 SRFI-18 Mutexes
........................

The behavior of Guile’s built-in mutexes is parameterized via a set of
flags passed to the ‘make-mutex’ procedure in the core (*note Mutexes
and Condition Variables::).  To satisfy the requirements for mutexes
specified by SRFI-18, the ‘make-mutex’ procedure described below sets
the following flags:
   • ‘recursive’: the mutex can be locked recursively
   • ‘unchecked-unlock’: attempts to unlock a mutex that is already
     unlocked will not raise an exception
   • ‘allow-external-unlock’: the mutex can be unlocked by any thread,
     not just the thread that locked it originally

 -- Function: make-mutex [name]
     Returns a new mutex, optionally assigning it the object name NAME,
     which may be any Scheme object.  The returned mutex will be created
     with the configuration described above.  Note that the name
     ‘make-mutex’ conflicts with Guile core function ‘make-mutex’.
     Applications wanting to use both of these functions will need to
     refer to them by different names.

 -- Function: mutex-name mutex
     Returns the name assigned to MUTEX at the time of its creation, or
     ‘#f’ if it was not given a name.

 -- Function: mutex-specific mutex
 -- Function: mutex-specific-set! mutex obj
     Get or set the “object-specific” property of MUTEX.  In Guile’s
     implementation of SRFI-18, this value is stored as an object
     property, and will be ‘#f’ if not set.

 -- Function: mutex-state mutex
     Returns information about the state of MUTEX.  Possible values are:
        • thread ‘T’: the mutex is in the locked/owned state and thread
          T is the owner of the mutex
        • symbol ‘not-owned’: the mutex is in the locked/not-owned state
        • symbol ‘abandoned’: the mutex is in the unlocked/abandoned
          state
        • symbol ‘not-abandoned’: the mutex is in the
          unlocked/not-abandoned state

 -- Function: mutex-lock! mutex [timeout [thread]]
     Lock MUTEX, optionally specifying a time object TIMEOUT after which
     to abort the lock attempt and a thread THREAD giving a new owner
     for MUTEX different than the current thread.  This procedure has
     the same behavior as the ‘lock-mutex’ procedure in the core
     library.

 -- Function: mutex-unlock! mutex [condition-variable [timeout]]
     Unlock MUTEX, optionally specifying a condition variable
     CONDITION-VARIABLE on which to wait, either indefinitely or,
     optionally, until the time object TIMEOUT has passed, to be
     signalled.  This procedure has the same behavior as the
     ‘unlock-mutex’ procedure in the core library.

7.5.15.3 SRFI-18 Condition variables
....................................

SRFI-18 does not specify a “wait” function for condition variables.
Waiting on a condition variable can be simulated using the SRFI-18
‘mutex-unlock!’ function described in the previous section, or Guile’s
built-in ‘wait-condition-variable’ procedure can be used.

 -- Function: condition-variable? obj
     Returns ‘#t’ if OBJ is a condition variable, ‘#f’ otherwise.  This
     is the same procedure as the same-named built-in procedure (*note
     ‘condition-variable?’: Mutexes and Condition Variables.).

 -- Function: make-condition-variable [name]
     Returns a new condition variable, optionally assigning it the
     object name NAME, which may be any Scheme object.  This procedure
     replaces a procedure of the same name in the core library.

 -- Function: condition-variable-name condition-variable
     Returns the name assigned to CONDITION-VARIABLE at the time of its
     creation, or ‘#f’ if it was not given a name.

 -- Function: condition-variable-specific condition-variable
 -- Function: condition-variable-specific-set! condition-variable obj
     Get or set the “object-specific” property of CONDITION-VARIABLE.
     In Guile’s implementation of SRFI-18, this value is stored as an
     object property, and will be ‘#f’ if not set.

 -- Function: condition-variable-signal! condition-variable
 -- Function: condition-variable-broadcast! condition-variable
     Wake up one thread that is waiting for CONDITION-VARIABLE, in the
     case of ‘condition-variable-signal!’, or all threads waiting for
     it, in the case of ‘condition-variable-broadcast!’.  The behavior
     of these procedures is equivalent to that of the procedures
     ‘signal-condition-variable’ and ‘broadcast-condition-variable’ in
     the core library.

7.5.15.4 SRFI-18 Time
.....................

The SRFI-18 time functions manipulate time in two formats: a “time
object” type that represents an absolute point in time in some
implementation-specific way; and the number of seconds since some
unspecified “epoch”.  In Guile’s implementation, the epoch is the Unix
epoch, 00:00:00 UTC, January 1, 1970.

 -- Function: current-time
     Return the current time as a time object.  This procedure replaces
     the procedure of the same name in the core library, which returns
     the current time in seconds since the epoch.

 -- Function: time? obj
     Returns ‘#t’ if OBJ is a time object, ‘#f’ otherwise.

 -- Function: time->seconds time
 -- Function: seconds->time seconds
     Convert between time objects and numerical values representing the
     number of seconds since the epoch.  When converting from a time
     object to seconds, the return value is the number of seconds
     between TIME and the epoch.  When converting from seconds to a time
     object, the return value is a time object that represents a time
     SECONDS seconds after the epoch.

7.5.15.5 SRFI-18 Exceptions
...........................

SRFI-18 exceptions are identical to the exceptions provided by Guile’s
implementation of SRFI-34.  The behavior of exception handlers invoked
to handle exceptions thrown from SRFI-18 functions, however, differs
from the conventional behavior of SRFI-34 in that the continuation of
the handler is the same as that of the call to the function.  Handlers
are called in a tail-recursive manner; the exceptions do not “bubble
up”.

 -- Function: current-exception-handler
     Returns the current exception handler.

 -- Function: with-exception-handler handler thunk
     Installs HANDLER as the current exception handler and calls the
     procedure THUNK with no arguments, returning its value as the value
     of the exception.  HANDLER must be a procedure that accepts a
     single argument.  The current exception handler at the time this
     procedure is called will be restored after the call returns.

 -- Function: raise obj
     Raise OBJ as an exception.  This is the same procedure as the
     same-named procedure defined in SRFI 34.

 -- Function: join-timeout-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of
     performing a timed join on a thread that does not exit within the
     specified timeout, ‘#f’ otherwise.

 -- Function: abandoned-mutex-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of
     attempting to lock a mutex that has been abandoned by its owner
     thread, ‘#f’ otherwise.

 -- Function: terminated-thread-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of joining
     on a thread that exited as the result of a call to
     ‘thread-terminate!’.

 -- Function: uncaught-exception? obj
 -- Function: uncaught-exception-reason exc
     ‘uncaught-exception?’ returns ‘#t’ if OBJ is an exception thrown as
     the result of joining a thread that exited by raising an exception
     that was handled by the top-level exception handler installed by
     ‘make-thread’.  When this occurs, the original exception is
     preserved as part of the exception thrown by ‘thread-join!’ and can
     be accessed by calling ‘uncaught-exception-reason’ on that
     exception.  Note that because this exception-preservation mechanism
     is a side-effect of ‘make-thread’, joining on threads that exited
     as described above but were created by other means will not raise
     this ‘uncaught-exception’ error.

7.5.16 SRFI-19 - Time/Date Library
----------------------------------

This is an implementation of the SRFI-19 time/date library.  The
functions and variables described here are provided by

     (use-modules (srfi srfi-19))

   *Caution*: The current code in this module incorrectly extends the
Gregorian calendar leap year rule back prior to the introduction of
those reforms in 1582 (or the appropriate year in various countries).
The Julian calendar was used prior to 1582, and there were 10 days
skipped for the reform, but the code doesn’t implement that.

   This will be fixed some time.  Until then calculations for 1583
onwards are correct, but prior to that any day/month/year and day of the
week calculations are wrong.

7.5.16.1 SRFI-19 Introduction
.............................

This module implements time and date representations and calculations,
in various time systems, including universal time (UTC) and atomic time
(TAI).

   For those not familiar with these time systems, TAI is based on a
fixed length second derived from oscillations of certain atoms.  UTC
differs from TAI by an integral number of seconds, which is increased or
decreased at announced times to keep UTC aligned to a mean solar day
(the orbit and rotation of the earth are not quite constant).

   So far, only increases in the TAI <-> UTC difference have been
needed.  Such an increase is a “leap second”, an extra second of TAI
introduced at the end of a UTC day.  When working entirely within UTC
this is never seen, every day simply has 86400 seconds.  But when
converting from TAI to a UTC date, an extra 23:59:60 is present, where
normally a day would end at 23:59:59.  Effectively the UTC second from
23:59:59 to 00:00:00 has taken two TAI seconds.

   In the current implementation, the system clock is assumed to be UTC,
and a table of leap seconds in the code converts to TAI. See comments in
‘srfi-19.scm’ for how to update this table.

   Also, for those not familiar with the terminology, a "Julian Day" is
a real number which is a count of days and fraction of a day, in UTC,
starting from -4713-01-01T12:00:00Z, ie. midday Monday 1 Jan 4713 B.C. A
"Modified Julian Day" is the same, but starting from
1858-11-17T00:00:00Z, ie. midnight 17 November 1858 UTC. That time is
julian day 2400000.5.

7.5.16.2 SRFI-19 Time
.....................

A "time" object has type, seconds and nanoseconds fields representing a
point in time starting from some epoch.  This is an arbitrary point in
time, not just a time of day.  Although times are represented in
nanoseconds, the actual resolution may be lower.

   The following variables hold the possible time types.  For instance
‘(current-time time-process)’ would give the current CPU process time.

 -- Variable: time-utc
     Universal Coordinated Time (UTC).

 -- Variable: time-tai
     International Atomic Time (TAI).

 -- Variable: time-monotonic
     Monotonic time, meaning a monotonically increasing time starting
     from an unspecified epoch.

     Note that in the current implementation ‘time-monotonic’ is the
     same as ‘time-tai’, and unfortunately is therefore affected by
     adjustments to the system clock.  Perhaps this will change in the
     future.

 -- Variable: time-duration
     A duration, meaning simply a difference between two times.

 -- Variable: time-process
     CPU time spent in the current process, starting from when the
     process began.

 -- Variable: time-thread
     CPU time spent in the current thread.  Not currently implemented.


 -- Function: time? obj
     Return ‘#t’ if OBJ is a time object, or ‘#f’ if not.

 -- Function: make-time type nanoseconds seconds
     Create a time object with the given TYPE, SECONDS and NANOSECONDS.

 -- Function: time-type time
 -- Function: time-nanosecond time
 -- Function: time-second time
 -- Function: set-time-type! time type
 -- Function: set-time-nanosecond! time nsec
 -- Function: set-time-second! time sec
     Get or set the type, seconds or nanoseconds fields of a time
     object.

     ‘set-time-type!’ merely changes the field, it doesn’t convert the
     time value.  For conversions, see *note SRFI-19 Time/Date
     conversions::.

 -- Function: copy-time time
     Return a new time object, which is a copy of the given TIME.

 -- Function: current-time [type]
     Return the current time of the given TYPE.  The default TYPE is
     ‘time-utc’.

     Note that the name ‘current-time’ conflicts with the Guile core
     ‘current-time’ function (*note Time::) as well as the SRFI-18
     ‘current-time’ function (*note SRFI-18 Time::).  Applications
     wanting to use more than one of these functions will need to refer
     to them by different names.

 -- Function: time-resolution [type]
     Return the resolution, in nanoseconds, of the given time TYPE.  The
     default TYPE is ‘time-utc’.

 -- Function: time<=? t1 t2
 -- Function: time<? t1 t2
 -- Function: time=? t1 t2
 -- Function: time>=? t1 t2
 -- Function: time>? t1 t2
     Return ‘#t’ or ‘#f’ according to the respective relation between
     time objects T1 and T2.  T1 and T2 must be the same time type.

 -- Function: time-difference t1 t2
 -- Function: time-difference! t1 t2
     Return a time object of type ‘time-duration’ representing the
     period between T1 and T2.  T1 and T2 must be the same time type.

     ‘time-difference’ returns a new time object, ‘time-difference!’ may
     modify T1 to form its return.

 -- Function: add-duration time duration
 -- Function: add-duration! time duration
 -- Function: subtract-duration time duration
 -- Function: subtract-duration! time duration
     Return a time object which is TIME with the given DURATION added or
     subtracted.  DURATION must be a time object of type
     ‘time-duration’.

     ‘add-duration’ and ‘subtract-duration’ return a new time object.
     ‘add-duration!’ and ‘subtract-duration!’ may modify the given TIME
     to form their return.

7.5.16.3 SRFI-19 Date
.....................

A "date" object represents a date in the Gregorian calendar and a time
of day on that date in some timezone.

   The fields are year, month, day, hour, minute, second, nanoseconds
and timezone.  A date object is immutable, its fields can be read but
they cannot be modified once the object is created.

 -- Function: date? obj
     Return ‘#t’ if OBJ is a date object, or ‘#f’ if not.

 -- Function: make-date nsecs seconds minutes hours date month year
          zone-offset
     Create a new date object.

 -- Function: date-nanosecond date
     Nanoseconds, 0 to 999999999.

 -- Function: date-second date
     Seconds, 0 to 59, or 60 for a leap second.  60 is never seen when
     working entirely within UTC, it’s only when converting to or from
     TAI.

 -- Function: date-minute date
     Minutes, 0 to 59.

 -- Function: date-hour date
     Hour, 0 to 23.

 -- Function: date-day date
     Day of the month, 1 to 31 (or less, according to the month).

 -- Function: date-month date
     Month, 1 to 12.

 -- Function: date-year date
     Year, eg. 2003.  Dates B.C. are negative, eg. -46 is 46 B.C. There
     is no year 0, year -1 is followed by year 1.

 -- Function: date-zone-offset date
     Time zone, an integer number of seconds east of Greenwich.

 -- Function: date-year-day date
     Day of the year, starting from 1 for 1st January.

 -- Function: date-week-day date
     Day of the week, starting from 0 for Sunday.

 -- Function: date-week-number date dstartw
     Week of the year, ignoring a first partial week.  DSTARTW is the
     day of the week which is taken to start a week, 0 for Sunday, 1 for
     Monday, etc.

 -- Function: current-date [tz-offset]
     Return a date object representing the current date/time, in UTC
     offset by TZ-OFFSET.  TZ-OFFSET is seconds east of Greenwich and
     defaults to the local timezone.

 -- Function: current-julian-day
     Return the current Julian Day.

 -- Function: current-modified-julian-day
     Return the current Modified Julian Day.

7.5.16.4 SRFI-19 Time/Date conversions
......................................

 -- Function: date->julian-day date
 -- Function: date->modified-julian-day date
 -- Function: date->time-monotonic date
 -- Function: date->time-tai date
 -- Function: date->time-utc date
 -- Function: julian-day->date jdn [tz-offset]
 -- Function: julian-day->time-monotonic jdn
 -- Function: julian-day->time-tai jdn
 -- Function: julian-day->time-utc jdn
 -- Function: modified-julian-day->date jdn [tz-offset]
 -- Function: modified-julian-day->time-monotonic jdn
 -- Function: modified-julian-day->time-tai jdn
 -- Function: modified-julian-day->time-utc jdn
 -- Function: time-monotonic->date time [tz-offset]
 -- Function: time-monotonic->time-tai time
 -- Function: time-monotonic->time-tai! time
 -- Function: time-monotonic->time-utc time
 -- Function: time-monotonic->time-utc! time
 -- Function: time-tai->date time [tz-offset]
 -- Function: time-tai->julian-day time
 -- Function: time-tai->modified-julian-day time
 -- Function: time-tai->time-monotonic time
 -- Function: time-tai->time-monotonic! time
 -- Function: time-tai->time-utc time
 -- Function: time-tai->time-utc! time
 -- Function: time-utc->date time [tz-offset]
 -- Function: time-utc->julian-day time
 -- Function: time-utc->modified-julian-day time
 -- Function: time-utc->time-monotonic time
 -- Function: time-utc->time-monotonic! time
 -- Function: time-utc->time-tai time
 -- Function: time-utc->time-tai! time

     Convert between dates, times and days of the respective types.  For
     instance ‘time-tai->time-utc’ accepts a TIME object of type
     ‘time-tai’ and returns an object of type ‘time-utc’.

     The ‘!’ variants may modify their TIME argument to form their
     return.  The plain functions create a new object.

     For conversions to dates, TZ-OFFSET is seconds east of Greenwich.
     The default is the local timezone, at the given time, as provided
     by the system, using ‘localtime’ (*note Time::).

     On 32-bit systems, ‘localtime’ is limited to a 32-bit ‘time_t’, so
     a default TZ-OFFSET is only available for times between Dec 1901
     and Jan 2038.  For prior dates an application might like to use the
     value in 1902, though some locations have zone changes prior to
     that.  For future dates an application might like to assume today’s
     rules extend indefinitely.  But for correct daylight savings
     transitions it will be necessary to take an offset for the same day
     and time but a year in range and which has the same starting
     weekday and same leap/non-leap (to support rules like last Sunday
     in October).

7.5.16.5 SRFI-19 Date to string
...............................

 -- Function: date->string date [format]
     Convert a date to a string under the control of a format.  FORMAT
     should be a string containing ‘~’ escapes, which will be expanded
     as per the following conversion table.  The default FORMAT is ‘~c’,
     a locale-dependent date and time.

     Many of these conversion characters are the same as POSIX
     ‘strftime’ (*note Time::), but there are some extras and some
     variations.

     ~~     literal ~
     ~a     locale abbreviated weekday, eg. ‘Sun’
     ~A     locale full weekday, eg. ‘Sunday’
     ~b     locale abbreviated month, eg. ‘Jan’
     ~B     locale full month, eg. ‘January’
     ~c     locale date and time, eg.
            ‘Fri Jul 14 20:28:42-0400 2000’
     ~d     day of month, zero padded, ‘01’ to ‘31’
            
     ~e     day of month, blank padded, ‘ 1’ to ‘31’
     ~f     seconds and fractional seconds, with locale
            decimal point, eg. ‘5.2’
     ~h     same as ~b
     ~H     hour, 24-hour clock, zero padded, ‘00’ to ‘23’
     ~I     hour, 12-hour clock, zero padded, ‘01’ to ‘12’
     ~j     day of year, zero padded, ‘001’ to ‘366’
     ~k     hour, 24-hour clock, blank padded, ‘ 0’ to ‘23’
     ~l     hour, 12-hour clock, blank padded, ‘ 1’ to ‘12’
     ~m     month, zero padded, ‘01’ to ‘12’
     ~M     minute, zero padded, ‘00’ to ‘59’
     ~n     newline
     ~N     nanosecond, zero padded, ‘000000000’ to
            ‘999999999’
     ~p     locale AM or PM
     ~r     time, 12 hour clock, ‘~I:~M:~S ~p’
     ~s     number of full seconds since “the epoch” in UTC
     ~S     second, zero padded ‘00’ to ‘60’
            (usual limit is 59, 60 is a leap second)
     ~t     horizontal tab character
     ~T     time, 24 hour clock, ‘~H:~M:~S’
     ~U     week of year, Sunday first day of week, ‘00’ to
            ‘52’
     ~V     week of year, Monday first day of week, ‘01’ to
            ‘53’
     ~w     day of week, 0 for Sunday, ‘0’ to ‘6’
     ~W     week of year, Monday first day of week, ‘00’ to
            ‘52’
            
     ~y     year, two digits, ‘00’ to ‘99’
     ~Y     year, full, eg. ‘2003’
     ~z     time zone, RFC-822 style
     ~Z     time zone symbol (not currently implemented)
     ~1     ISO-8601 date, ‘~Y-~m-~d’
     ~2     ISO-8601 time+zone, ‘~H:~M:~S~z’
     ~3     ISO-8601 time, ‘~H:~M:~S’
     ~4     ISO-8601 date/time+zone, ‘~Y-~m-~dT~H:~M:~S~z’
     ~5     ISO-8601 date/time, ‘~Y-~m-~dT~H:~M:~S’

   Conversions ‘~D’, ‘~x’ and ‘~X’ are not currently described here,
since the specification and reference implementation differ.

   Conversion is locale-dependent on systems that support it (*note
Accessing Locale Information::).  *Note ‘setlocale’: Locales, for
information on how to change the current locale.

7.5.16.6 SRFI-19 String to date
...............................

 -- Function: string->date input template
     Convert an INPUT string to a date under the control of a TEMPLATE
     string.  Return a newly created date object.

     Literal characters in TEMPLATE must match characters in INPUT and
     ‘~’ escapes must match the input forms described in the table
     below.  “Skip to” means characters up to one of the given type are
     ignored, or “no skip” for no skipping.  “Read” is what’s then read,
     and “Set” is the field affected in the date object.

     For example ‘~Y’ skips input characters until a digit is reached,
     at which point it expects a year and stores that to the year field
     of the date.

            Skip to            Read                        Set
                                                           
     ~~     no skip            literal ~                   nothing
                                                           
     ~a     char-alphabetic?   locale abbreviated          nothing
                               weekday name                
     ~A     char-alphabetic?   locale full weekday name    nothing
                                                           
     ~b     char-alphabetic?   locale abbreviated month    date-month
                               name                        
     ~B     char-alphabetic?   locale full month name      date-month
                                                           
     ~d     char-numeric?      day of month                date-day
                                                           
     ~e     no skip            day of month, blank         date-day
                               padded                      
     ~h     same as ‘~b’
            
     ~H     char-numeric?      hour                        date-hour
                                                           
     ~k     no skip            hour, blank padded          date-hour
                                                           
     ~m     char-numeric?      month                       date-month
                                                           
     ~M     char-numeric?      minute                      date-minute
                                                           
     ~S     char-numeric?      second                      date-second
                                                           
     ~y     no skip            2-digit year                date-year within
                                                           50 years
                                                           
     ~Y     char-numeric?      year                        date-year
                                                           
     ~z     no skip            time zone                   date-zone-offset

     Notice that the weekday matching forms don’t affect the date object
     returned, instead the weekday will be derived from the day, month
     and year.

     Conversion is locale-dependent on systems that support it (*note
     Accessing Locale Information::).  *Note ‘setlocale’: Locales, for
     information on how to change the current locale.

7.5.17 SRFI-23 - Error Reporting
--------------------------------

The SRFI-23 ‘error’ procedure is always available.

7.5.18 SRFI-26 - specializing parameters
----------------------------------------

This SRFI provides a syntax for conveniently specializing selected
parameters of a function.  It can be used with,

     (use-modules (srfi srfi-26))

 -- library syntax: cut slot1 slot2 …
 -- library syntax: cute slot1 slot2 …
     Return a new procedure which will make a call (SLOT1 SLOT2 …) but
     with selected parameters specialized to given expressions.

     An example will illustrate the idea.  The following is a
     specialization of ‘write’, sending output to ‘my-output-port’,

          (cut write <> my-output-port)
          ⇒
          (lambda (obj) (write obj my-output-port))

     The special symbol ‘<>’ indicates a slot to be filled by an
     argument to the new procedure.  ‘my-output-port’ on the other hand
     is an expression to be evaluated and passed, ie. it specializes the
     behaviour of ‘write’.

     <>
          A slot to be filled by an argument from the created procedure.
          Arguments are assigned to ‘<>’ slots in the order they appear
          in the ‘cut’ form, there’s no way to re-arrange arguments.

          The first argument to ‘cut’ is usually a procedure (or
          expression giving a procedure), but ‘<>’ is allowed there too.
          For example,

               (cut <> 1 2 3)
               ⇒
               (lambda (proc) (proc 1 2 3))

     <...>
          A slot to be filled by all remaining arguments from the new
          procedure.  This can only occur at the end of a ‘cut’ form.

          For example, a procedure taking a variable number of arguments
          like ‘max’ but in addition enforcing a lower bound,

               (define my-lower-bound 123)

               (cut max my-lower-bound <...>)
               ⇒
               (lambda arglist (apply max my-lower-bound arglist))

     For ‘cut’ the specializing expressions are evaluated each time the
     new procedure is called.  For ‘cute’ they’re evaluated just once,
     when the new procedure is created.  The name ‘cute’ stands for
     “‘cut’ with evaluated arguments”.  In all cases the evaluations
     take place in an unspecified order.

     The following illustrates the difference between ‘cut’ and ‘cute’,

          (cut format <> "the time is ~s" (current-time))
          ⇒
          (lambda (port) (format port "the time is ~s" (current-time)))

          (cute format <> "the time is ~s" (current-time))
          ⇒
          (let ((val (current-time)))
            (lambda (port) (format port "the time is ~s" val))

     (There’s no provision for a mixture of ‘cut’ and ‘cute’ where some
     expressions would be evaluated every time but others evaluated only
     once.)

     ‘cut’ is really just a shorthand for the sort of ‘lambda’ forms
     shown in the above examples.  But notice ‘cut’ avoids the need to
     name unspecialized parameters, and is more compact.  Use in
     functional programming style or just with ‘map’, ‘for-each’ or
     similar is typical.

          (map (cut * 2 <>) '(1 2 3 4))

          (for-each (cut write <> my-port) my-list)

7.5.19 SRFI-27 - Sources of Random Bits
---------------------------------------

This subsection is based on the specification of SRFI-27
(http://srfi.schemers.org/srfi-27/srfi-27.html) written by Sebastian
Egner.

   This SRFI provides access to a (pseudo) random number generator; for
Guile’s built-in random number facilities, which SRFI-27 is implemented
upon, *Note Random::.  With SRFI-27, random numbers are obtained from a
_random source_, which encapsulates a random number generation algorithm
and its state.

7.5.19.1 The Default Random Source
..................................

 -- Function: random-integer n
     Return a random number between zero (inclusive) and N (exclusive),
     using the default random source.  The numbers returned have a
     uniform distribution.

 -- Function: random-real
     Return a random number in (0,1), using the default random source.
     The numbers returned have a uniform distribution.

 -- Function: default-random-source
     A random source from which ‘random-integer’ and ‘random-real’ have
     been derived using ‘random-source-make-integers’ and
     ‘random-source-make-reals’ (*note SRFI-27 Random Number
     Generators:: for those procedures).  Note that an assignment to
     ‘default-random-source’ does not change ‘random-integer’ or
     ‘random-real’; it is also strongly recommended not to assign a new
     value.

7.5.19.2 Random Sources
.......................

 -- Function: make-random-source
     Create a new random source.  The stream of random numbers obtained
     from each random source created by this procedure will be
     identical, unless its state is changed by one of the procedures
     below.

 -- Function: random-source? object
     Tests whether OBJECT is a random source.  Random sources are a
     disjoint type.

 -- Function: random-source-randomize! source
     Attempt to set the state of the random source to a truly random
     value.  The current implementation uses a seed based on the current
     system time.

 -- Function: random-source-pseudo-randomize! source i j
     Changes the state of the random source s into the initial state of
     the (I, J)-th independent random source, where I and J are
     non-negative integers.  This procedure provides a mechanism to
     obtain a large number of independent random sources (usually all
     derived from the same backbone generator), indexed by two integers.
     In contrast to ‘random-source-randomize!’, this procedure is
     entirely deterministic.

   The state associated with a random state can be obtained an
reinstated with the following procedures:

 -- Function: random-source-state-ref source
 -- Function: random-source-state-set! source state
     Get and set the state of a random source.  No assumptions should be
     made about the nature of the state object, besides it having an
     external representation (i.e. it can be passed to ‘write’ and
     subsequently ‘read’ back).

7.5.19.3 Obtaining random number generator procedures
.....................................................

 -- Function: random-source-make-integers source
     Obtains a procedure to generate random integers using the random
     source SOURCE.  The returned procedure takes a single argument N,
     which must be a positive integer, and returns the next uniformly
     distributed random integer from the interval {0, ..., N-1} by
     advancing the state of SOURCE.

     If an application obtains and uses several generators for the same
     random source SOURCE, a call to any of these generators advances
     the state of SOURCE.  Hence, the generators do not produce the same
     sequence of random integers each but rather share a state.  This
     also holds for all other types of generators derived from a fixed
     random sources.

     While the SRFI text specifies that “Implementations that support
     concurrency make sure that the state of a generator is properly
     advanced”, this is currently not the case in Guile’s implementation
     of SRFI-27, as it would cause a severe performance penalty.  So in
     multi-threaded programs, you either must perform locking on random
     sources shared between threads yourself, or use different random
     sources for multiple threads.

 -- Function: random-source-make-reals source
 -- Function: random-source-make-reals source unit
     Obtains a procedure to generate random real numbers 0 < x < 1 using
     the random source SOURCE.  The procedure rand is called without
     arguments.

     The optional parameter UNIT determines the type of numbers being
     produced by the returned procedure and the quantization of the
     output.  UNIT must be a number such that 0 < UNIT < 1.  The numbers
     created by the returned procedure are of the same numerical type as
     UNIT and the potential output values are spaced by at most UNIT.
     One can imagine rand to create numbers as X * UNIT where X is a
     random integer in {1, ..., floor(1/unit)-1}.  Note, however, that
     this need not be the way the values are actually created and that
     the actual resolution of rand can be much higher than unit.  In
     case UNIT is absent it defaults to a reasonably small value
     (related to the width of the mantissa of an efficient number
     format).

7.5.20 SRFI-30 - Nested Multi-line Comments
-------------------------------------------

Starting from version 2.0, Guile’s ‘read’ supports SRFI-30/R6RS nested
multi-line comments by default, *note Block Comments::.

7.5.21 SRFI-31 - A special form ‘rec’ for recursive evaluation
--------------------------------------------------------------

SRFI-31 defines a special form that can be used to create
self-referential expressions more conveniently.  The syntax is as
follows:

     <rec expression> --> (rec <variable> <expression>)
     <rec expression> --> (rec (<variable>+) <body>)

   The first syntax can be used to create self-referential expressions,
for example:

       guile> (define tmp (rec ones (cons 1 (delay ones))))

   The second syntax can be used to create anonymous recursive
functions:

       guile> (define tmp (rec (display-n item n)
                            (if (positive? n)
                                (begin (display n) (display-n (- n 1))))))
       guile> (tmp 42 3)
       424242
       guile>

7.5.22 SRFI-34 - Exception handling for programs
------------------------------------------------

Guile provides an implementation of SRFI-34’s exception handling
mechanisms (http://srfi.schemers.org/srfi-34/srfi-34.html) as an
alternative to its own built-in mechanisms (*note Exceptions::).  It can
be made available as follows:

     (use-modules (srfi srfi-34))

7.5.23 SRFI-35 - Conditions
---------------------------

SRFI-35 (http://srfi.schemers.org/srfi-35/srfi-35.html) implements
"conditions", a data structure akin to records designed to convey
information about exceptional conditions between parts of a program.  It
is normally used in conjunction with SRFI-34’s ‘raise’:

     (raise (condition (&message
                         (message "An error occurred"))))

   Users can define "condition types" containing arbitrary information.
Condition types may inherit from one another.  This allows the part of
the program that handles (or “catches”) conditions to get accurate
information about the exceptional condition that arose.

   SRFI-35 conditions are made available using:

     (use-modules (srfi srfi-35))

   The procedures available to manipulate condition types are the
following:

 -- Scheme Procedure: make-condition-type id parent field-names
     Return a new condition type named ID, inheriting from PARENT, and
     with the fields whose names are listed in FIELD-NAMES.  FIELD-NAMES
     must be a list of symbols and must not contain names already used
     by PARENT or one of its supertypes.

 -- Scheme Procedure: condition-type? obj
     Return true if OBJ is a condition type.

   Conditions can be created and accessed with the following procedures:

 -- Scheme Procedure: make-condition type . field+value
     Return a new condition of type TYPE with fields initialized as
     specified by FIELD+VALUE, a sequence of field names (symbols) and
     values as in the following example:

          (let ((&ct (make-condition-type 'foo &condition '(a b c))))
            (make-condition &ct 'a 1 'b 2 'c 3))

     Note that all fields of TYPE and its supertypes must be specified.

 -- Scheme Procedure: make-compound-condition condition1 condition2 …
     Return a new compound condition composed of CONDITION1 CONDITION2
     ....  The returned condition has the type of each condition of
     condition1 condition2 … (per ‘condition-has-type?’).

 -- Scheme Procedure: condition-has-type? c type
     Return true if condition C has type TYPE.

 -- Scheme Procedure: condition-ref c field-name
     Return the value of the field named FIELD-NAME from condition C.

     If C is a compound condition and several underlying condition types
     contain a field named FIELD-NAME, then the value of the first such
     field is returned, using the order in which conditions were passed
     to ‘make-compound-condition’.

 -- Scheme Procedure: extract-condition c type
     Return a condition of condition type TYPE with the field values
     specified by C.

     If C is a compound condition, extract the field values from the
     subcondition belonging to TYPE that appeared first in the call to
     ‘make-compound-condition’ that created the condition.

   Convenience macros are also available to create condition types and
conditions.

 -- library syntax: define-condition-type type supertype predicate
          field-spec...
     Define a new condition type named TYPE that inherits from
     SUPERTYPE.  In addition, bind PREDICATE to a type predicate that
     returns true when passed a condition of type TYPE or any of its
     subtypes.  FIELD-SPEC must have the form ‘(field accessor)’ where
     FIELD is the name of field of TYPE and ACCESSOR is the name of a
     procedure to access field FIELD in conditions of type TYPE.

     The example below defines condition type ‘&foo’, inheriting from
     ‘&condition’ with fields ‘a’, ‘b’ and ‘c’:

          (define-condition-type &foo &condition
            foo-condition?
            (a  foo-a)
            (b  foo-b)
            (c  foo-c))

 -- library syntax: condition type-field-binding1 type-field-binding2 …
     Return a new condition or compound condition, initialized according
     to TYPE-FIELD-BINDING1 TYPE-FIELD-BINDING2 ....  Each
     TYPE-FIELD-BINDING must have the form ‘(type field-specs...)’,
     where TYPE is the name of a variable bound to a condition type;
     each FIELD-SPEC must have the form ‘(field-name value)’ where
     FIELD-NAME is a symbol denoting the field being initialized to
     VALUE.  As for ‘make-condition’, all fields must be specified.

     The following example returns a simple condition:

          (condition (&message (message "An error occurred")))

     The one below returns a compound condition:

          (condition (&message (message "An error occurred"))
                     (&serious))

   Finally, SRFI-35 defines a several standard condition types.

 -- Variable: &condition
     This condition type is the root of all condition types.  It has no
     fields.

 -- Variable: &message
     A condition type that carries a message describing the nature of
     the condition to humans.

 -- Scheme Procedure: message-condition? c
     Return true if C is of type ‘&message’ or one of its subtypes.

 -- Scheme Procedure: condition-message c
     Return the message associated with message condition C.

 -- Variable: &serious
     This type describes conditions serious enough that they cannot
     safely be ignored.  It has no fields.

 -- Scheme Procedure: serious-condition? c
     Return true if C is of type ‘&serious’ or one of its subtypes.

 -- Variable: &error
     This condition describes errors, typically caused by something that
     has gone wrong in the interaction of the program with the external
     world or the user.

 -- Scheme Procedure: error? c
     Return true if C is of type ‘&error’ or one of its subtypes.

7.5.24 SRFI-37 - args-fold
--------------------------

This is a processor for GNU ‘getopt_long’-style program arguments.  It
provides an alternative, less declarative interface than ‘getopt-long’
in ‘(ice-9 getopt-long)’ (*note The (ice-9 getopt-long) Module:
getopt-long.).  Unlike ‘getopt-long’, it supports repeated options and
any number of short and long names per option.  Access it with:

     (use-modules (srfi srfi-37))

   SRFI-37 principally provides an ‘option’ type and the ‘args-fold’
function.  To use the library, create a set of options with ‘option’ and
use it as a specification for invoking ‘args-fold’.

   Here is an example of a simple argument processor for the typical
‘--version’ and ‘--help’ options, which returns a backwards list of
files given on the command line:

     (args-fold (cdr (program-arguments))
                (let ((display-and-exit-proc
                       (lambda (msg)
                         (lambda (opt name arg loads)
                           (display msg) (quit)))))
                  (list (option '(#\v "version") #f #f
                                (display-and-exit-proc "Foo version 42.0\n"))
                        (option '(#\h "help") #f #f
                                (display-and-exit-proc
                                 "Usage: foo scheme-file ..."))))
                (lambda (opt name arg loads)
                  (error "Unrecognized option `~A'" name))
                (lambda (op loads) (cons op loads))
                '())

 -- Scheme Procedure: option names required-arg? optional-arg? processor
     Return an object that specifies a single kind of program option.

     NAMES is a list of command-line option names, and should consist of
     characters for traditional ‘getopt’ short options and strings for
     ‘getopt_long’-style long options.

     REQUIRED-ARG? and OPTIONAL-ARG? are mutually exclusive; one or both
     must be ‘#f’.  If REQUIRED-ARG?, the option must be followed by an
     argument on the command line, such as ‘--opt=value’ for long
     options, or an error will be signalled.  If OPTIONAL-ARG?, an
     argument will be taken if available.

     PROCESSOR is a procedure that takes at least 3 arguments, called
     when ‘args-fold’ encounters the option: the containing option
     object, the name used on the command line, and the argument given
     for the option (or ‘#f’ if none).  The rest of the arguments are
     ‘args-fold’ “seeds”, and the PROCESSOR should return seeds as well.

 -- Scheme Procedure: option-names opt
 -- Scheme Procedure: option-required-arg? opt
 -- Scheme Procedure: option-optional-arg? opt
 -- Scheme Procedure: option-processor opt
     Return the specified field of OPT, an option object, as described
     above for ‘option’.

 -- Scheme Procedure: args-fold args options unrecognized-option-proc
          operand-proc seed …
     Process ARGS, a list of program arguments such as that returned by
     ‘(cdr (program-arguments))’, in order against OPTIONS, a list of
     option objects as described above.  All functions called take the
     “seeds”, or the last multiple-values as multiple arguments,
     starting with SEED …, and must return the new seeds.  Return the
     final seeds.

     Call ‘unrecognized-option-proc’, which is like an option object’s
     processor, for any options not found in OPTIONS.

     Call ‘operand-proc’ with any items on the command line that are not
     named options.  This includes arguments after ‘--’.  It is called
     with the argument in question, as well as the seeds.

7.5.25 SRFI-38 - External Representation for Data With Shared Structure
-----------------------------------------------------------------------

This subsection is based on the specification of SRFI-38
(http://srfi.schemers.org/srfi-38/srfi-38.html) written by Ray
Dillinger.

   This SRFI creates an alternative external representation for data
written and read using ‘write-with-shared-structure’ and
‘read-with-shared-structure’.  It is identical to the grammar for
external representation for data written and read with ‘write’ and
‘read’ given in section 7 of R5RS, except that the single production

     <datum> --> <simple datum> | <compound datum>

   is replaced by the following five productions:

     <datum> --> <defining datum> | <nondefining datum> | <defined datum>
     <defining datum> -->  #<indexnum>=<nondefining datum>
     <defined datum> --> #<indexnum>#
     <nondefining datum> --> <simple datum> | <compound datum>
     <indexnum> --> <digit 10>+

 -- Scheme procedure: write-with-shared-structure obj
 -- Scheme procedure: write-with-shared-structure obj port
 -- Scheme procedure: write-with-shared-structure obj port optarg

     Writes an external representation of OBJ to the given port.
     Strings that appear in the written representation are enclosed in
     doublequotes, and within those strings backslash and doublequote
     characters are escaped by backslashes.  Character objects are
     written using the ‘#\’ notation.

     Objects which denote locations rather than values (cons cells,
     vectors, and non-zero-length strings in R5RS scheme; also Guile’s
     structs, bytevectors and ports and hash-tables), if they appear at
     more than one point in the data being written, are preceded by
     ‘#N=’ the first time they are written and replaced by ‘#N#’ all
     subsequent times they are written, where N is a natural number used
     to identify that particular object.  If objects which denote
     locations occur only once in the structure, then
     ‘write-with-shared-structure’ must produce the same external
     representation for those objects as ‘write’.

     ‘write-with-shared-structure’ terminates in finite time and
     produces a finite representation when writing finite data.

     ‘write-with-shared-structure’ returns an unspecified value.  The
     PORT argument may be omitted, in which case it defaults to the
     value returned by ‘(current-output-port)’.  The OPTARG argument may
     also be omitted.  If present, its effects on the output and return
     value are unspecified but ‘write-with-shared-structure’ must still
     write a representation that can be read by
     ‘read-with-shared-structure’.  Some implementations may wish to use
     OPTARG to specify formatting conventions, numeric radixes, or
     return values.  Guile’s implementation ignores OPTARG.

     For example, the code

          (begin (define a (cons 'val1 'val2))
                 (set-cdr! a a)
                 (write-with-shared-structure a))

     should produce the output ‘#1=(val1 . #1#)’.  This shows a cons
     cell whose ‘cdr’ contains itself.

 -- Scheme procedure: read-with-shared-structure
 -- Scheme procedure: read-with-shared-structure port

     ‘read-with-shared-structure’ converts the external representations
     of Scheme objects produced by ‘write-with-shared-structure’ into
     Scheme objects.  That is, it is a parser for the nonterminal
     ‘<datum>’ in the augmented external representation grammar defined
     above.  ‘read-with-shared-structure’ returns the next object
     parsable from the given input port, updating PORT to point to the
     first character past the end of the external representation of the
     object.

     If an end-of-file is encountered in the input before any characters
     are found that can begin an object, then an end-of-file object is
     returned.  The port remains open, and further attempts to read it
     (by ‘read-with-shared-structure’ or ‘read’ will also return an
     end-of-file object.  If an end of file is encountered after the
     beginning of an object’s external representation, but the external
     representation is incomplete and therefore not parsable, an error
     is signalled.

     The PORT argument may be omitted, in which case it defaults to the
     value returned by ‘(current-input-port)’.  It is an error to read
     from a closed port.

7.5.26 SRFI-39 - Parameters
---------------------------

This SRFI adds support for dynamically-scoped parameters.  SRFI 39 is
implemented in the Guile core; there’s no module needed to get SRFI-39
itself.  Parameters are documented in *note Parameters::.

   This module does export one extra function: ‘with-parameters*’.  This
is a Guile-specific addition to the SRFI, similar to the core
‘with-fluids*’ (*note Fluids and Dynamic States::).

 -- Function: with-parameters* param-list value-list thunk
     Establish a new dynamic scope, as per ‘parameterize’ above, taking
     parameters from PARAM-LIST and corresponding values from
     VALUE-LIST.  A call ‘(THUNK)’ is made in the new scope and the
     result from that THUNK is the return from ‘with-parameters*’.

7.5.27 SRFI-41 - Streams
------------------------

This subsection is based on the specification of SRFI-41
(http://srfi.schemers.org/srfi-41/srfi-41.html) by Philip L. Bewig.

This SRFI implements streams, sometimes called lazy lists, a sequential
data structure containing elements computed only on demand.  A stream is
either null or is a pair with a stream in its cdr.  Since elements of a
stream are computed only when accessed, streams can be infinite.  Once
computed, the value of a stream element is cached in case it is needed
again.  SRFI-41 can be made available with:

     (use-modules (srfi srfi-41))

7.5.27.1 SRFI-41 Stream Fundamentals
....................................

SRFI-41 Streams are based on two mutually-recursive abstract data types:
An object of the ‘stream’ abstract data type is a promise that, when
forced, is either ‘stream-null’ or is an object of type ‘stream-pair’.
An object of the ‘stream-pair’ abstract data type contains a
‘stream-car’ and a ‘stream-cdr’, which must be a ‘stream’.  The
essential feature of streams is the systematic suspensions of the
recursive promises between the two data types.

   The object stored in the ‘stream-car’ of a ‘stream-pair’ is a promise
that is forced the first time the ‘stream-car’ is accessed; its value is
cached in case it is needed again.  The object may have any type, and
different stream elements may have different types.  If the ‘stream-car’
is never accessed, the object stored there is never evaluated.
Likewise, the ‘stream-cdr’ is a promise to return a stream, and is only
forced on demand.

7.5.27.2 SRFI-41 Stream Primitives
..................................

This library provides eight operators: constructors for ‘stream-null’
and ‘stream-pair’s, type predicates for streams and the two kinds of
streams, accessors for both fields of a ‘stream-pair’, and a lambda that
creates procedures that return streams.

 -- Scheme Variable: stream-null
     A promise that, when forced, is a single object, distinguishable
     from all other objects, that represents the null stream.
     ‘stream-null’ is immutable and unique.

 -- Scheme Syntax: stream-cons object-expr stream-expr
     Creates a newly-allocated stream containing a promise that, when
     forced, is a ‘stream-pair’ with OBJECT-EXPR in its ‘stream-car’ and
     STREAM-EXPR in its ‘stream-cdr’.  Neither OBJECT-EXPR nor
     STREAM-EXPR is evaluated when ‘stream-cons’ is called.

     Once created, a ‘stream-pair’ is immutable; there is no
     ‘stream-set-car!’ or ‘stream-set-cdr!’ that modifies an existing
     stream-pair.  There is no dotted-pair or improper stream as with
     lists.

 -- Scheme Procedure: stream? object
     Returns true if OBJECT is a stream, otherwise returns false.  If
     OBJECT is a stream, its promise will not be forced.  If ‘(stream?
     obj)’ returns true, then one of ‘(stream-null? obj)’ or
     ‘(stream-pair? obj)’ will return true and the other will return
     false.

 -- Scheme Procedure: stream-null? object
     Returns true if OBJECT is the distinguished null stream, otherwise
     returns false.  If OBJECT is a stream, its promise will be forced.

 -- Scheme Procedure: stream-pair? object
     Returns true if OBJECT is a ‘stream-pair’ constructed by
     ‘stream-cons’, otherwise returns false.  If OBJECT is a stream, its
     promise will be forced.

 -- Scheme Procedure: stream-car stream
     Returns the object stored in the ‘stream-car’ of STREAM.  An error
     is signalled if the argument is not a ‘stream-pair’.  This causes
     the OBJECT-EXPR passed to ‘stream-cons’ to be evaluated if it had
     not yet been; the value is cached in case it is needed again.

 -- Scheme Procedure: stream-cdr stream
     Returns the stream stored in the ‘stream-cdr’ of STREAM.  An error
     is signalled if the argument is not a ‘stream-pair’.

 -- Scheme Syntax: stream-lambda formals body …
     Creates a procedure that returns a promise to evaluate the BODY of
     the procedure.  The last BODY expression to be evaluated must yield
     a stream.  As with normal ‘lambda’, FORMALS may be a single
     variable name, in which case all the formal arguments are collected
     into a single list, or a list of variable names, which may be null
     if there are no arguments, proper if there are an exact number of
     arguments, or dotted if a fixed number of arguments is to be
     followed by zero or more arguments collected into a list.  BODY
     must contain at least one expression, and may contain internal
     definitions preceding any expressions to be evaluated.

     (define strm123
       (stream-cons 1
         (stream-cons 2
           (stream-cons 3
             stream-null))))

     (stream-car strm123) ⇒ 1
     (stream-car (stream-cdr strm123) ⇒ 2

     (stream-pair?
       (stream-cdr
         (stream-cons (/ 1 0) stream-null))) ⇒ #f

     (stream? (list 1 2 3)) ⇒ #f

     (define iter
       (stream-lambda (f x)
         (stream-cons x (iter f (f x)))))

     (define nats (iter (lambda (x) (+ x 1)) 0))

     (stream-car (stream-cdr nats)) ⇒ 1

     (define stream-add
       (stream-lambda (s1 s2)
         (stream-cons
           (+ (stream-car s1) (stream-car s2))
           (stream-add (stream-cdr s1)
                       (stream-cdr s2)))))

     (define evens (stream-add nats nats))

     (stream-car evens) ⇒ 0
     (stream-car (stream-cdr evens)) ⇒ 2
     (stream-car (stream-cdr (stream-cdr evens))) ⇒ 4

7.5.27.3 SRFI-41 Stream Library
...............................

 -- Scheme Syntax: define-stream (name args …) body …
     Creates a procedure that returns a stream, and may appear anywhere
     a normal ‘define’ may appear, including as an internal definition.
     It may contain internal definitions of its own.  The defined
     procedure takes arguments in the same way as ‘stream-lambda’.
     ‘define-stream’ is syntactic sugar on ‘stream-lambda’; see also
     ‘stream-let’, which is also a sugaring of ‘stream-lambda’.

     A simple version of ‘stream-map’ that takes only a single input
     stream calls itself recursively:

          (define-stream (stream-map proc strm)
            (if (stream-null? strm)
                stream-null
                (stream-cons
                  (proc (stream-car strm))
                  (stream-map proc (stream-cdr strm))))))

 -- Scheme Procedure: list->stream list
     Returns a newly-allocated stream containing the elements from LIST.

 -- Scheme Procedure: port->stream [port]
     Returns a newly-allocated stream containing in its elements the
     characters on the port.  If PORT is not given it defaults to the
     current input port.  The returned stream has finite length and is
     terminated by ‘stream-null’.

     It looks like one use of ‘port->stream’ would be this:

          (define s ;wrong!
            (with-input-from-file filename
              (lambda () (port->stream))))

     But that fails, because ‘with-input-from-file’ is eager, and closes
     the input port prematurely, before the first character is read.  To
     read a file into a stream, say:

          (define-stream (file->stream filename)
            (let ((p (open-input-file filename)))
              (stream-let loop ((c (read-char p)))
                (if (eof-object? c)
                    (begin (close-input-port p)
                           stream-null)
                    (stream-cons c
                      (loop (read-char p)))))))

 -- Scheme Syntax: stream object-expr …
     Creates a newly-allocated stream containing in its elements the
     objects, in order.  The OBJECT-EXPRs are evaluated when they are
     accessed, not when the stream is created.  If no objects are given,
     as in (stream), the null stream is returned.  See also
     ‘list->stream’.

          (define strm123 (stream 1 2 3))

          ; (/ 1 0) not evaluated when stream is created
          (define s (stream 1 (/ 1 0) -1))

 -- Scheme Procedure: stream->list [n] stream
     Returns a newly-allocated list containing in its elements the first
     N items in STREAM.  If STREAM has less than N items, all the items
     in the stream will be included in the returned list.  If N is not
     given it defaults to infinity, which means that unless STREAM is
     finite ‘stream->list’ will never return.

          (stream->list 10
            (stream-map (lambda (x) (* x x))
              (stream-from 0)))
            ⇒ (0 1 4 9 16 25 36 49 64 81)

 -- Scheme Procedure: stream-append stream …
     Returns a newly-allocated stream containing in its elements those
     elements contained in its input STREAMs, in order of input.  If any
     of the input streams is infinite, no elements of any of the
     succeeding input streams will appear in the output stream.  See
     also ‘stream-concat’.

 -- Scheme Procedure: stream-concat stream
     Takes a STREAM consisting of one or more streams and returns a
     newly-allocated stream containing all the elements of the input
     streams.  If any of the streams in the input STREAM is infinite,
     any remaining streams in the input stream will never appear in the
     output stream.  See also ‘stream-append’.

 -- Scheme Procedure: stream-constant object …
     Returns a newly-allocated stream containing in its elements the
     OBJECTs, repeating in succession forever.

          (stream-constant 1) ⇒ 1 1 1 …
          (stream-constant #t #f) ⇒ #t #f #t #f #t #f …

 -- Scheme Procedure: stream-drop n stream
     Returns the suffix of the input STREAM that starts at the next
     element after the first N elements.  The output stream shares
     structure with the input STREAM; thus, promises forced in one
     instance of the stream are also forced in the other instance of the
     stream.  If the input STREAM has less than N elements,
     ‘stream-drop’ returns the null stream.  See also ‘stream-take’.

 -- Scheme Procedure: stream-drop-while pred stream
     Returns the suffix of the input STREAM that starts at the first
     element X for which ‘(pred x)’ returns false.  The output stream
     shares structure with the input STREAM.  See also
     ‘stream-take-while’.

 -- Scheme Procedure: stream-filter pred stream
     Returns a newly-allocated stream that contains only those elements
     X of the input STREAM which satisfy the predicate ‘pred’.

          (stream-filter odd? (stream-from 0))
             ⇒ 1 3 5 7 9 …

 -- Scheme Procedure: stream-fold proc base stream
     Applies a binary procedure PROC to BASE and the first element of
     STREAM to compute a new BASE, then applies the procedure to the new
     BASE and the next element of STREAM to compute a succeeding BASE,
     and so on, accumulating a value that is finally returned as the
     value of ‘stream-fold’ when the end of the stream is reached.
     STREAM must be finite, or ‘stream-fold’ will enter an infinite
     loop.  See also ‘stream-scan’, which is similar to ‘stream-fold’,
     but useful for infinite streams.  For readers familiar with other
     functional languages, this is a left-fold; there is no
     corresponding right-fold, since right-fold relies on finite streams
     that are fully-evaluated, in which case they may as well be
     converted to a list.

 -- Scheme Procedure: stream-for-each proc stream …
     Applies PROC element-wise to corresponding elements of the input
     STREAMs for side-effects; it returns nothing.  ‘stream-for-each’
     stops as soon as any of its input streams is exhausted.

 -- Scheme Procedure: stream-from first [step]
     Creates a newly-allocated stream that contains FIRST as its first
     element and increments each succeeding element by STEP.  If STEP is
     not given it defaults to 1.  FIRST and STEP may be of any numeric
     type.  ‘stream-from’ is frequently useful as a generator in
     ‘stream-of’ expressions.  See also ‘stream-range’ for a similar
     procedure that creates finite streams.

 -- Scheme Procedure: stream-iterate proc base
     Creates a newly-allocated stream containing BASE in its first
     element and applies PROC to each element in turn to determine the
     succeeding element.  See also ‘stream-unfold’ and ‘stream-unfolds’.

 -- Scheme Procedure: stream-length stream
     Returns the number of elements in the STREAM; it does not evaluate
     its elements.  ‘stream-length’ may only be used on finite streams;
     it enters an infinite loop with infinite streams.

 -- Scheme Syntax: stream-let tag ((var expr) …) body …
     Creates a local scope that binds each variable to the value of its
     corresponding expression.  It additionally binds TAG to a procedure
     which takes the bound variables as arguments and BODY as its
     defining expressions, binding the TAG with ‘stream-lambda’.  TAG is
     in scope within body, and may be called recursively.  When the
     expanded expression defined by the ‘stream-let’ is evaluated,
     ‘stream-let’ evaluates the expressions in its BODY in an
     environment containing the newly-bound variables, returning the
     value of the last expression evaluated, which must yield a stream.

     ‘stream-let’ provides syntactic sugar on ‘stream-lambda’, in the
     same manner as normal ‘let’ provides syntactic sugar on normal
     ‘lambda’.  However, unlike normal ‘let’, the TAG is required, not
     optional, because unnamed ‘stream-let’ is meaningless.

     For example, ‘stream-member’ returns the first ‘stream-pair’ of the
     input STRM with a ‘stream-car’ X that satisfies ‘(eql? obj x)’, or
     the null stream if X is not present in STRM.

          (define-stream (stream-member eql? obj strm)
            (stream-let loop ((strm strm))
              (cond ((stream-null? strm) strm)
                    ((eql? obj (stream-car strm)) strm)
                    (else (loop (stream-cdr strm))))))

 -- Scheme Procedure: stream-map proc stream …
     Applies PROC element-wise to corresponding elements of the input
     STREAMs, returning a newly-allocated stream containing elements
     that are the results of those procedure applications.  The output
     stream has as many elements as the minimum-length input stream, and
     may be infinite.

 -- Scheme Syntax: stream-match stream clause …
     Provides pattern-matching for streams.  The input STREAM is an
     expression that evaluates to a stream.  Clauses are of the form
     ‘(pattern [fender] expression)’, consisting of a PATTERN that
     matches a stream of a particular shape, an optional FENDER that
     must succeed if the pattern is to match, and an EXPRESSION that is
     evaluated if the pattern matches.  There are four types of
     patterns:

        • () matches the null stream.

        • (PAT0 PAT1 …) matches a finite stream with length exactly
          equal to the number of pattern elements.

        • (PAT0 PAT1 … ‘.’  PAT-REST) matches an infinite stream, or a
          finite stream with length at least as great as the number of
          pattern elements before the literal dot.

        • PAT matches an entire stream.  Should always appear last in
          the list of clauses; it’s not an error to appear elsewhere,
          but subsequent clauses could never match.

     Each pattern element may be either:

        • An identifier, which matches any stream element.
          Additionally, the value of the stream element is bound to the
          variable named by the identifier, which is in scope in the
          FENDER and EXPRESSION of the corresponding CLAUSE.  Each
          identifier in a single pattern must be unique.

        • A literal underscore (‘_’), which matches any stream element
          but creates no bindings.

     The PATTERNs are tested in order, left-to-right, until a matching
     pattern is found; if FENDER is present, it must evaluate to a true
     value for the match to be successful.  Pattern variables are bound
     in the corresponding FENDER and EXPRESSION.  Once the matching
     PATTERN is found, the corresponding EXPRESSION is evaluated and
     returned as the result of the match.  An error is signaled if no
     pattern matches the input STREAM.

     ‘stream-match’ is often used to distinguish null streams from
     non-null streams, binding HEAD and TAIL:

          (define (len strm)
            (stream-match strm
              (() 0)
              ((head . tail) (+ 1 (len tail)))))

     Fenders can test the common case where two stream elements must be
     identical; the ‘else’ pattern is an identifier bound to the entire
     stream, not a keyword as in ‘cond’.

          (stream-match strm
            ((x y . _) (equal? x y) 'ok)
            (else 'error))

     A more complex example uses two nested matchers to match two
     different stream arguments; ‘(stream-merge lt? . strms)’ stably
     merges two or more streams ordered by the ‘lt?’ predicate:

          (define-stream (stream-merge lt? . strms)
            (define-stream (merge xx yy)
              (stream-match xx (() yy) ((x . xs)
                (stream-match yy (() xx) ((y . ys)
                  (if (lt? y x)
                      (stream-cons y (merge xx ys))
                      (stream-cons x (merge xs yy))))))))
            (stream-let loop ((strms strms))
              (cond ((null? strms) stream-null)
                    ((null? (cdr strms)) (car strms))
                    (else (merge (car strms)
                                 (apply stream-merge lt?
                                   (cdr strms)))))))

 -- Scheme Syntax: stream-of expr clause …
     Provides the syntax of stream comprehensions, which generate
     streams by means of looping expressions.  The result is a stream of
     objects of the type returned by EXPR.  There are four types of
     clauses:

        • (VAR ‘in’ STREAM-EXPR) loops over the elements of STREAM-EXPR,
          in order from the start of the stream, binding each element of
          the stream in turn to VAR.  ‘stream-from’ and ‘stream-range’
          are frequently useful as generators for STREAM-EXPR.

        • (VAR ‘is’ EXPR) binds VAR to the value obtained by evaluating
          EXPR.

        • (PRED EXPR) includes in the output stream only those elements
          X which satisfy the predicate PRED.

     The scope of variables bound in the stream comprehension is the
     clauses to the right of the binding clause (but not the binding
     clause itself) plus the result expression.

     When two or more generators are present, the loops are processed as
     if they are nested from left to right; that is, the rightmost
     generator varies fastest.  A consequence of this is that only the
     first generator may be infinite and all subsequent generators must
     be finite.  If no generators are present, the result of a stream
     comprehension is a stream containing the result expression; thus,
     ‘(stream-of 1)’ produces a finite stream containing only the
     element 1.

          (stream-of (* x x)
            (x in (stream-range 0 10))
            (even? x))
            ⇒ 0 4 16 36 64

          (stream-of (list a b)
            (a in (stream-range 1 4))
            (b in (stream-range 1 3)))
            ⇒ (1 1) (1 2) (2 1) (2 2) (3 1) (3 2)

          (stream-of (list i j)
            (i in (stream-range 1 5))
            (j in (stream-range (+ i 1) 5)))
            ⇒ (1 2) (1 3) (1 4) (2 3) (2 4) (3 4)

 -- Scheme Procedure: stream-range first past [step]
     Creates a newly-allocated stream that contains FIRST as its first
     element and increments each succeeding element by STEP.  The stream
     is finite and ends before PAST, which is not an element of the
     stream.  If STEP is not given it defaults to 1 if FIRST is less
     than past and -1 otherwise.  FIRST, PAST and STEP may be of any
     real numeric type.  ‘stream-range’ is frequently useful as a
     generator in ‘stream-of’ expressions.  See also ‘stream-from’ for a
     similar procedure that creates infinite streams.

          (stream-range 0 10) ⇒ 0 1 2 3 4 5 6 7 8 9
          (stream-range 0 10 2) ⇒ 0 2 4 6 8

     Successive elements of the stream are calculated by adding STEP to
     FIRST, so if any of FIRST, PAST or STEP are inexact, the length of
     the output stream may differ from ‘(ceiling (- (/ (- past first)
     step) 1)’.

 -- Scheme Procedure: stream-ref stream n
     Returns the Nth element of stream, counting from zero.  An error is
     signaled if N is greater than or equal to the length of stream.

          (define (fact n)
            (stream-ref
              (stream-scan * 1 (stream-from 1))
              n))

 -- Scheme Procedure: stream-reverse stream
     Returns a newly-allocated stream containing the elements of the
     input STREAM but in reverse order.  ‘stream-reverse’ may only be
     used with finite streams; it enters an infinite loop with infinite
     streams.  ‘stream-reverse’ does not force evaluation of the
     elements of the stream.

 -- Scheme Procedure: stream-scan proc base stream
     Accumulates the partial folds of an input STREAM into a
     newly-allocated output stream.  The output stream is the BASE
     followed by ‘(stream-fold proc base (stream-take i stream))’ for
     each of the first I elements of STREAM.

          (stream-scan + 0 (stream-from 1))
            ⇒ (stream 0 1 3 6 10 15 …)

          (stream-scan * 1 (stream-from 1))
            ⇒ (stream 1 1 2 6 24 120 …)

 -- Scheme Procedure: stream-take n stream
     Returns a newly-allocated stream containing the first N elements of
     the input STREAM.  If the input STREAM has less than N elements, so
     does the output stream.  See also ‘stream-drop’.

 -- Scheme Procedure: stream-take-while pred stream
     Takes a predicate and a ‘stream’ and returns a newly-allocated
     stream containing those elements ‘x’ that form the maximal prefix
     of the input stream which satisfy PRED.  See also
     ‘stream-drop-while’.

 -- Scheme Procedure: stream-unfold map pred gen base
     The fundamental recursive stream constructor.  It constructs a
     stream by repeatedly applying GEN to successive values of BASE, in
     the manner of ‘stream-iterate’, then applying MAP to each of the
     values so generated, appending each of the mapped values to the
     output stream as long as ‘(pred? base)’ returns a true value.  See
     also ‘stream-iterate’ and ‘stream-unfolds’.

     The expression below creates the finite stream ‘0 1 4 9 16 25 36 49
     64 81’.  Initially the BASE is 0, which is less than 10, so MAP
     squares the BASE and the mapped value becomes the first element of
     the output stream.  Then GEN increments the BASE by 1, so it
     becomes 1; this is less than 10, so MAP squares the new BASE and 1
     becomes the second element of the output stream.  And so on, until
     the base becomes 10, when PRED stops the recursion and stream-null
     ends the output stream.

          (stream-unfold
            (lambda (x) (expt x 2)) ; map
            (lambda (x) (< x 10))   ; pred?
            (lambda (x) (+ x 1))    ; gen
            0)                      ; base

 -- Scheme Procedure: stream-unfolds proc seed
     Returns N newly-allocated streams containing those elements
     produced by successive calls to the generator PROC, which takes the
     current SEED as its argument and returns N+1 values

     (PROC SEED) ⇒ SEED RESULT_0 … RESULT_N-1

     where the returned SEED is the input SEED to the next call to the
     generator and RESULT_I indicates how to produce the next element of
     the Ith result stream:

        • (VALUE): VALUE is the next car of the result stream.

        • ‘#f’: no value produced by this iteration of the generator
          PROC for the result stream.

        • (): the end of the result stream.

     It may require multiple calls of PROC to produce the next element
     of any particular result stream.  See also ‘stream-iterate’ and
     ‘stream-unfold’.

          (define (stream-partition pred? strm)
            (stream-unfolds
              (lambda (s)
                (if (stream-null? s)
                    (values s '() '())
                    (let ((a (stream-car s))
                          (d (stream-cdr s)))
                      (if (pred? a)
                          (values d (list a) #f)
                          (values d #f (list a))))))
              strm))

          (call-with-values
            (lambda ()
              (stream-partition odd?
                (stream-range 1 6)))
            (lambda (odds evens)
              (list (stream->list odds)
                    (stream->list evens))))
            ⇒ ((1 3 5) (2 4))

 -- Scheme Procedure: stream-zip stream …
     Returns a newly-allocated stream in which each element is a list
     (not a stream) of the corresponding elements of the input STREAMs.
     The output stream is as long as the shortest input STREAM, if any
     of the input STREAMs is finite, or is infinite if all the input
     STREAMs are infinite.

7.5.28 SRFI-42 - Eager Comprehensions
-------------------------------------

See the specification of SRFI-42
(http://srfi.schemers.org/srfi-42/srfi-42.html).

7.5.29 SRFI-43 - Vector Library
-------------------------------

This subsection is based on the specification of SRFI-43
(http://srfi.schemers.org/srfi-43/srfi-43.html) by Taylor Campbell.

SRFI-43 implements a comprehensive library of vector operations.  It can
be made available with:

     (use-modules (srfi srfi-43))

7.5.29.1 SRFI-43 Constructors
.............................

 -- Scheme Procedure: make-vector size [fill]
     Create and return a vector of size SIZE, optionally filling it with
     FILL.  The default value of FILL is unspecified.

          (make-vector 5 3) ⇒ #(3 3 3 3 3)

 -- Scheme Procedure: vector x …
     Create and return a vector whose elements are X ....

          (vector 0 1 2 3 4) ⇒ #(0 1 2 3 4)

 -- Scheme Procedure: vector-unfold f length initial-seed …
     The fundamental vector constructor.  Create a vector whose length
     is LENGTH and iterates across each index k from 0 up to LENGTH - 1,
     applying F at each iteration to the current index and current
     seeds, in that order, to receive n + 1 values: first, the element
     to put in the kth slot of the new vector and n new seeds for the
     next iteration.  It is an error for the number of seeds to vary
     between iterations.

          (vector-unfold (lambda (i x) (values x (- x 1)))
                         10 0)
          ⇒ #(0 -1 -2 -3 -4 -5 -6 -7 -8 -9)

          (vector-unfold values 10)
          ⇒ #(0 1 2 3 4 5 6 7 8 9)

 -- Scheme Procedure: vector-unfold-right f length initial-seed …
     Like ‘vector-unfold’, but it uses F to generate elements from
     right-to-left, rather than left-to-right.

          (vector-unfold-right (lambda (i x) (values x (+ x 1)))
                               10 0)
          ⇒ #(9 8 7 6 5 4 3 2 1 0)

 -- Scheme Procedure: vector-copy vec [start [end [fill]]]
     Allocate a new vector whose length is END - START and fills it with
     elements from VEC, taking elements from VEC starting at index START
     and stopping at index END.  START defaults to 0 and END defaults to
     the value of ‘(vector-length vec)’.  If END extends beyond the
     length of VEC, the slots in the new vector that obviously cannot be
     filled by elements from VEC are filled with FILL, whose default
     value is unspecified.

          (vector-copy '#(a b c d e f g h i))
          ⇒ #(a b c d e f g h i)

          (vector-copy '#(a b c d e f g h i) 6)
          ⇒ #(g h i)

          (vector-copy '#(a b c d e f g h i) 3 6)
          ⇒ #(d e f)

          (vector-copy '#(a b c d e f g h i) 6 12 'x)
          ⇒ #(g h i x x x)

 -- Scheme Procedure: vector-reverse-copy vec [start [end]]
     Like ‘vector-copy’, but it copies the elements in the reverse order
     from VEC.

          (vector-reverse-copy '#(5 4 3 2 1 0) 1 5)
          ⇒ #(1 2 3 4)

 -- Scheme Procedure: vector-append vec …
     Return a newly allocated vector that contains all elements in order
     from the subsequent locations in VEC ....

          (vector-append '#(a) '#(b c d))
          ⇒ #(a b c d)

 -- Scheme Procedure: vector-concatenate list-of-vectors
     Append each vector in LIST-OF-VECTORS.  Equivalent to ‘(apply
     vector-append list-of-vectors)’.

          (vector-concatenate '(#(a b) #(c d)))
          ⇒ #(a b c d)

7.5.29.2 SRFI-43 Predicates
...........................

 -- Scheme Procedure: vector? obj
     Return true if OBJ is a vector, else return false.

 -- Scheme Procedure: vector-empty? vec
     Return true if VEC is empty, i.e.  its length is 0, else return
     false.

 -- Scheme Procedure: vector= elt=? vec …
     Return true if the vectors VEC … have equal lengths and equal
     elements according to ELT=?.  ELT=? is always applied to two
     arguments.  Element comparison must be consistent with ‘eq?’ in the
     following sense: if ‘(eq? a b)’ returns true, then ‘(elt=? a b)’
     must also return true.  The order in which comparisons are
     performed is unspecified.

7.5.29.3 SRFI-43 Selectors
..........................

 -- Scheme Procedure: vector-ref vec i
     Return the element at index I in VEC.  Indexing is based on zero.

 -- Scheme Procedure: vector-length vec
     Return the length of VEC.

7.5.29.4 SRFI-43 Iteration
..........................

 -- Scheme Procedure: vector-fold kons knil vec1 vec2 …
     The fundamental vector iterator.  KONS is iterated over each index
     in all of the vectors, stopping at the end of the shortest; KONS is
     applied as
          (kons i state (vector-ref vec1 i) (vector-ref vec2 i) ...)
     where STATE is the current state value, and I is the current index.
     The current state value begins with KNIL, and becomes whatever KONS
     returned at the respective iteration.  The iteration is strictly
     left-to-right.

 -- Scheme Procedure: vector-fold-right kons knil vec1 vec2 …
     Similar to ‘vector-fold’, but it iterates right-to-left instead of
     left-to-right.

 -- Scheme Procedure: vector-map f vec1 vec2 …
     Return a new vector of the shortest size of the vector arguments.
     Each element at index i of the new vector is mapped from the old
     vectors by
          (f i (vector-ref vec1 i) (vector-ref vec2 i) ...)
     The dynamic order of application of F is unspecified.

 -- Scheme Procedure: vector-map! f vec1 vec2 …
     Similar to ‘vector-map’, but rather than mapping the new elements
     into a new vector, the new mapped elements are destructively
     inserted into VEC1.  The dynamic order of application of F is
     unspecified.

 -- Scheme Procedure: vector-for-each f vec1 vec2 …
     Call ‘(f i (vector-ref vec1 i) (vector-ref vec2 i) ...)’ for each
     index i less than the length of the shortest vector passed.  The
     iteration is strictly left-to-right.

 -- Scheme Procedure: vector-count pred? vec1 vec2 …
     Count the number of parallel elements in the vectors that satisfy
     PRED?, which is applied, for each index i less than the length of
     the smallest vector, to i and each parallel element in the vectors
     at that index, in order.

          (vector-count (lambda (i elt) (even? elt))
                        '#(3 1 4 1 5 9 2 5 6))
          ⇒ 3
          (vector-count (lambda (i x y) (< x y))
                        '#(1 3 6 9) '#(2 4 6 8 10 12))
          ⇒ 2

7.5.29.5 SRFI-43 Searching
..........................

 -- Scheme Procedure: vector-index pred? vec1 vec2 …
     Find and return the index of the first elements in VEC1 VEC2 … that
     satisfy PRED?.  If no matching element is found by the end of the
     shortest vector, return ‘#f’.

          (vector-index even? '#(3 1 4 1 5 9))
          ⇒ 2
          (vector-index < '#(3 1 4 1 5 9 2 5 6) '#(2 7 1 8 2))
          ⇒ 1
          (vector-index = '#(3 1 4 1 5 9 2 5 6) '#(2 7 1 8 2))
          ⇒ #f

 -- Scheme Procedure: vector-index-right pred? vec1 vec2 …
     Like ‘vector-index’, but it searches right-to-left, rather than
     left-to-right.  Note that the SRFI 43 specification requires that
     all the vectors must have the same length, but both the SRFI 43
     reference implementation and Guile’s implementation allow vectors
     with unequal lengths, and start searching from the last index of
     the shortest vector.

 -- Scheme Procedure: vector-skip pred? vec1 vec2 …
     Find and return the index of the first elements in VEC1 VEC2 … that
     do not satisfy PRED?.  If no matching element is found by the end
     of the shortest vector, return ‘#f’.  Equivalent to ‘vector-index’
     but with the predicate inverted.

          (vector-skip number? '#(1 2 a b 3 4 c d)) ⇒ 2

 -- Scheme Procedure: vector-skip-right pred? vec1 vec2 …
     Like ‘vector-skip’, but it searches for a non-matching element
     right-to-left, rather than left-to-right.  Note that the SRFI 43
     specification requires that all the vectors must have the same
     length, but both the SRFI 43 reference implementation and Guile’s
     implementation allow vectors with unequal lengths, and start
     searching from the last index of the shortest vector.

 -- Scheme Procedure: vector-binary-search vec value cmp [start [end]]
     Find and return an index of VEC between START and END whose value
     is VALUE using a binary search.  If no matching element is found,
     return ‘#f’.  The default START is 0 and the default END is the
     length of VEC.

     CMP must be a procedure of two arguments such that ‘(cmp a b)’
     returns a negative integer if a < b, a positive integer if a > b,
     or zero if a = b.  The elements of VEC must be sorted in
     non-decreasing order according to CMP.

     Note that SRFI 43 does not document the START and END arguments,
     but both its reference implementation and Guile’s implementation
     support them.

          (define (char-cmp c1 c2)
            (cond ((char<? c1 c2) -1)
                  ((char>? c1 c2) 1)
                  (else 0)))

          (vector-binary-search '#(#\a #\b #\c #\d #\e #\f #\g #\h)
                                #\g
                                char-cmp)
          ⇒ 6

 -- Scheme Procedure: vector-any pred? vec1 vec2 …
     Find the first parallel set of elements from VEC1 VEC2 … for which
     PRED? returns a true value.  If such a parallel set of elements
     exists, ‘vector-any’ returns the value that PRED? returned for that
     set of elements.  The iteration is strictly left-to-right.

 -- Scheme Procedure: vector-every pred? vec1 vec2 …
     If, for every index i between 0 and the length of the shortest
     vector argument, the set of elements ‘(vector-ref vec1 i)’
     ‘(vector-ref vec2 i)’ … satisfies PRED?, ‘vector-every’ returns the
     value that PRED? returned for the last set of elements, at the last
     index of the shortest vector.  Otherwise it returns ‘#f’.  The
     iteration is strictly left-to-right.

7.5.29.6 SRFI-43 Mutators
.........................

 -- Scheme Procedure: vector-set! vec i value
     Assign the contents of the location at I in VEC to VALUE.

 -- Scheme Procedure: vector-swap! vec i j
     Swap the values of the locations in VEC at I and J.

 -- Scheme Procedure: vector-fill! vec fill [start [end]]
     Assign the value of every location in VEC between START and END to
     FILL.  START defaults to 0 and END defaults to the length of VEC.

 -- Scheme Procedure: vector-reverse! vec [start [end]]
     Destructively reverse the contents of VEC between START and END.
     START defaults to 0 and END defaults to the length of VEC.

 -- Scheme Procedure: vector-copy! target tstart source [sstart [send]]
     Copy a block of elements from SOURCE to TARGET, both of which must
     be vectors, starting in TARGET at TSTART and starting in SOURCE at
     SSTART, ending when (SEND - SSTART) elements have been copied.  It
     is an error for TARGET to have a length less than (TSTART + SEND -
     SSTART).  SSTART defaults to 0 and SEND defaults to the length of
     SOURCE.

 -- Scheme Procedure: vector-reverse-copy! target tstart source [sstart
          [send]]
     Like ‘vector-copy!’, but this copies the elements in the reverse
     order.  It is an error if TARGET and SOURCE are identical vectors
     and the TARGET and SOURCE ranges overlap; however, if TSTART =
     SSTART, ‘vector-reverse-copy!’ behaves as ‘(vector-reverse! target
     tstart send)’ would.

7.5.29.7 SRFI-43 Conversion
...........................

 -- Scheme Procedure: vector->list vec [start [end]]
     Return a newly allocated list containing the elements in VEC
     between START and END.  START defaults to 0 and END defaults to the
     length of VEC.

 -- Scheme Procedure: reverse-vector->list vec [start [end]]
     Like ‘vector->list’, but the resulting list contains the specified
     range of elements of VEC in reverse order.

 -- Scheme Procedure: list->vector proper-list [start [end]]
     Return a newly allocated vector of the elements from PROPER-LIST
     with indices between START and END.  START defaults to 0 and END
     defaults to the length of PROPER-LIST.  Note that SRFI 43 does not
     document the START and END arguments, but both its reference
     implementation and Guile’s implementation support them.

 -- Scheme Procedure: reverse-list->vector proper-list [start [end]]
     Like ‘list->vector’, but the resulting vector contains the
     specified range of elements of PROPER-LIST in reverse order.  Note
     that SRFI 43 does not document the START and END arguments, but
     both its reference implementation and Guile’s implementation
     support them.

7.5.30 SRFI-45 - Primitives for Expressing Iterative Lazy Algorithms
--------------------------------------------------------------------

This subsection is based on the specification of SRFI-45
(http://srfi.schemers.org/srfi-45/srfi-45.html) written by André van
Tonder.

   Lazy evaluation is traditionally simulated in Scheme using ‘delay’
and ‘force’.  However, these primitives are not powerful enough to
express a large class of lazy algorithms that are iterative.  Indeed, it
is folklore in the Scheme community that typical iterative lazy
algorithms written using delay and force will often require unbounded
memory.

   This SRFI provides set of three operations: {‘lazy’, ‘delay’,
‘force’}, which allow the programmer to succinctly express lazy
algorithms while retaining bounded space behavior in cases that are
properly tail-recursive.  A general recipe for using these primitives is
provided.  An additional procedure ‘eager’ is provided for the
construction of eager promises in cases where efficiency is a concern.

   Although this SRFI redefines ‘delay’ and ‘force’, the extension is
conservative in the sense that the semantics of the subset {‘delay’,
‘force’} in isolation (i.e., as long as the program does not use ‘lazy’)
agrees with that in R5RS. In other words, no program that uses the R5RS
definitions of delay and force will break if those definition are
replaced by the SRFI-45 definitions of delay and force.

   Guile also adds ‘promise?’ to the list of exports, which is not part
of the official SRFI-45.

 -- Scheme Procedure: promise? obj
     Return true if OBJ is an SRFI-45 promise, otherwise return false.

 -- Scheme Syntax: delay expression
     Takes an expression of arbitrary type A and returns a promise of
     type ‘(Promise A)’ which at some point in the future may be asked
     (by the ‘force’ procedure) to evaluate the expression and deliver
     the resulting value.

 -- Scheme Syntax: lazy expression
     Takes an expression of type ‘(Promise A)’ and returns a promise of
     type ‘(Promise A)’ which at some point in the future may be asked
     (by the ‘force’ procedure) to evaluate the expression and deliver
     the resulting promise.

 -- Scheme Procedure: force expression
     Takes an argument of type ‘(Promise A)’ and returns a value of type
     A as follows: If a value of type A has been computed for the
     promise, this value is returned.  Otherwise, the promise is first
     evaluated, then overwritten by the obtained promise or value, and
     then force is again applied (iteratively) to the promise.

 -- Scheme Procedure: eager expression
     Takes an argument of type A and returns a value of type ‘(Promise
     A)’.  As opposed to ‘delay’, the argument is evaluated eagerly.
     Semantically, writing ‘(eager expression)’ is equivalent to writing

          (let ((value expression)) (delay value)).

     However, the former is more efficient since it does not require
     unnecessary creation and evaluation of thunks.  We also have the
     equivalence

          (delay expression) = (lazy (eager expression))

   The following reduction rules may be helpful for reasoning about
these primitives.  However, they do not express the memoization and
memory usage semantics specified above:

     (force (delay expression)) -> expression
     (force (lazy  expression)) -> (force expression)
     (force (eager value))      -> value

Correct usage
.............

We now provide a general recipe for using the primitives {‘lazy’,
‘delay’, ‘force’} to express lazy algorithms in Scheme.  The
transformation is best described by way of an example: Consider the
stream-filter algorithm, expressed in a hypothetical lazy language as

     (define (stream-filter p? s)
       (if (null? s) '()
           (let ((h (car s))
                 (t (cdr s)))
             (if (p? h)
                 (cons h (stream-filter p? t))
                 (stream-filter p? t)))))

   This algorithm can be expressed as follows in Scheme:

     (define (stream-filter p? s)
       (lazy
          (if (null? (force s)) (delay '())
              (let ((h (car (force s)))
                    (t (cdr (force s))))
                (if (p? h)
                    (delay (cons h (stream-filter p? t)))
                    (stream-filter p? t))))))

   In other words, we

   • wrap all constructors (e.g., ‘'()’, ‘cons’) with ‘delay’,
   • apply ‘force’ to arguments of deconstructors (e.g., ‘car’, ‘cdr’
     and ‘null?’),
   • wrap procedure bodies with ‘(lazy ...)’.

7.5.31 SRFI-46 Basic syntax-rules Extensions
--------------------------------------------

Guile’s core ‘syntax-rules’ supports the extensions specified by
SRFI-46/R7RS. Tail patterns have been supported since at least Guile
2.0, and custom ellipsis identifiers have been supported since Guile
2.0.10.  *Note Syntax Rules::.

7.5.32 SRFI-55 - Requiring Features
-----------------------------------

SRFI-55 provides ‘require-extension’ which is a portable mechanism to
load selected SRFI modules.  This is implemented in the Guile core,
there’s no module needed to get SRFI-55 itself.

 -- library syntax: require-extension clause1 clause2 …
     Require the features of CLAUSE1 CLAUSE2 … , throwing an error if
     any are unavailable.

     A CLAUSE is of the form ‘(IDENTIFIER arg...)’.  The only IDENTIFIER
     currently supported is ‘srfi’ and the arguments are SRFI numbers.
     For example to get SRFI-1 and SRFI-6,

          (require-extension (srfi 1 6))

     ‘require-extension’ can only be used at the top-level.

     A Guile-specific program can simply ‘use-modules’ to load SRFIs not
     already in the core, ‘require-extension’ is for programs designed
     to be portable to other Scheme implementations.

7.5.33 SRFI-60 - Integers as Bits
---------------------------------

This SRFI provides various functions for treating integers as bits and
for bitwise manipulations.  These functions can be obtained with,

     (use-modules (srfi srfi-60))

   Integers are treated as infinite precision twos-complement, the same
as in the core logical functions (*note Bitwise Operations::).  And
likewise bit indexes start from 0 for the least significant bit.  The
following functions in this SRFI are already in the Guile core,

     ‘logand’, ‘logior’, ‘logxor’, ‘lognot’, ‘logtest’, ‘logcount’,
     ‘integer-length’, ‘logbit?’, ‘ash’


 -- Function: bitwise-and n1 ...
 -- Function: bitwise-ior n1 ...
 -- Function: bitwise-xor n1 ...
 -- Function: bitwise-not n
 -- Function: any-bits-set? j k
 -- Function: bit-set? index n
 -- Function: arithmetic-shift n count
 -- Function: bit-field n start end
 -- Function: bit-count n
     Aliases for ‘logand’, ‘logior’, ‘logxor’, ‘lognot’, ‘logtest’,
     ‘logbit?’, ‘ash’, ‘bit-extract’ and ‘logcount’ respectively.

     Note that the name ‘bit-count’ conflicts with ‘bit-count’ in the
     core (*note Bit Vectors::).

 -- Function: bitwise-if mask n1 n0
 -- Function: bitwise-merge mask n1 n0
     Return an integer with bits selected from N1 and N0 according to
     MASK.  Those bits where MASK has 1s are taken from N1, and those
     where MASK has 0s are taken from N0.

          (bitwise-if 3 #b0101 #b1010) ⇒ 9

 -- Function: log2-binary-factors n
 -- Function: first-set-bit n
     Return a count of how many factors of 2 are present in N.  This is
     also the bit index of the lowest 1 bit in N.  If N is 0, the return
     is -1.

          (log2-binary-factors 6) ⇒ 1
          (log2-binary-factors -8) ⇒ 3

 -- Function: copy-bit index n newbit
     Return N with the bit at INDEX set according to NEWBIT.  NEWBIT
     should be ‘#t’ to set the bit to 1, or ‘#f’ to set it to 0.  Bits
     other than at INDEX are unchanged in the return.

          (copy-bit 1 #b0101 #t) ⇒ 7

 -- Function: copy-bit-field n newbits start end
     Return N with the bits from START (inclusive) to END (exclusive)
     changed to the value NEWBITS.

     The least significant bit in NEWBITS goes to START, the next to
     START+1, etc.  Anything in NEWBITS past the END given is ignored.

          (copy-bit-field #b10000 #b11 1 3) ⇒ #b10110

 -- Function: rotate-bit-field n count start end
     Return N with the bit field from START (inclusive) to END
     (exclusive) rotated upwards by COUNT bits.

     COUNT can be positive or negative, and it can be more than the
     field width (it’ll be reduced modulo the width).

          (rotate-bit-field #b0110 2 1 4) ⇒ #b1010

 -- Function: reverse-bit-field n start end
     Return N with the bits from START (inclusive) to END (exclusive)
     reversed.

          (reverse-bit-field #b101001 2 4) ⇒ #b100101

 -- Function: integer->list n [len]
     Return bits from N in the form of a list of ‘#t’ for 1 and ‘#f’ for
     0.  The least significant LEN bits are returned, and the first list
     element is the most significant of those bits.  If LEN is not
     given, the default is ‘(integer-length N)’ (*note Bitwise
     Operations::).

          (integer->list 6)   ⇒ (#t #t #f)
          (integer->list 1 4) ⇒ (#f #f #f #t)

 -- Function: list->integer lst
 -- Function: booleans->integer bool…
     Return an integer formed bitwise from the given LST list of
     booleans, or for ‘booleans->integer’ from the BOOL arguments.

     Each boolean is ‘#t’ for a 1 and ‘#f’ for a 0.  The first element
     becomes the most significant bit in the return.

          (list->integer '(#t #f #t #f)) ⇒ 10

7.5.34 SRFI-61 - A more general ‘cond’ clause
---------------------------------------------

This SRFI extends RnRS ‘cond’ to support test expressions that return
multiple values, as well as arbitrary definitions of test success.  SRFI
61 is implemented in the Guile core; there’s no module needed to get
SRFI-61 itself.  Extended ‘cond’ is documented in *note Simple
Conditional Evaluation: Conditionals.

7.5.35 SRFI-62 - S-expression comments.
---------------------------------------

Starting from version 2.0, Guile’s ‘read’ supports SRFI-62/R7RS
S-expression comments by default.

7.5.36 SRFI-64 - A Scheme API for test suites.
----------------------------------------------

See the specification of SRFI-64
(http://srfi.schemers.org/srfi-64/srfi-64.html).

7.5.37 SRFI-67 - Compare procedures
-----------------------------------

See the specification of SRFI-67
(http://srfi.schemers.org/srfi-67/srfi-67.html).

7.5.38 SRFI-69 - Basic hash tables
----------------------------------

This is a portable wrapper around Guile’s built-in hash table and weak
table support.  *Note Hash Tables::, for information on that built-in
support.  Above that, this hash-table interface provides association of
equality and hash functions with tables at creation time, so variants of
each function are not required, as well as a procedure that takes care
of most uses for Guile hash table handles, which this SRFI does not
provide as such.

   Access it with:

     (use-modules (srfi srfi-69))

7.5.38.1 Creating hash tables
.............................

 -- Scheme Procedure: make-hash-table [equal-proc hash-proc #:weak
          weakness start-size]
     Create and answer a new hash table with EQUAL-PROC as the equality
     function and HASH-PROC as the hashing function.

     By default, EQUAL-PROC is ‘equal?’.  It can be any two-argument
     procedure, and should answer whether two keys are the same for this
     table’s purposes.

     My default HASH-PROC assumes that ‘equal-proc’ is no coarser than
     ‘equal?’ unless it is literally ‘string-ci=?’.  If provided,
     HASH-PROC should be a two-argument procedure that takes a key and
     the current table size, and answers a reasonably good hash integer
     between 0 (inclusive) and the size (exclusive).

     WEAKNESS should be ‘#f’ or a symbol indicating how “weak” the hash
     table is:

     ‘#f’
          An ordinary non-weak hash table.  This is the default.

     ‘key’
          When the key has no more non-weak references at GC, remove
          that entry.

     ‘value’
          When the value has no more non-weak references at GC, remove
          that entry.

     ‘key-or-value’
          When either has no more non-weak references at GC, remove the
          association.

     As a legacy of the time when Guile couldn’t grow hash tables,
     START-SIZE is an optional integer argument that specifies the
     approximate starting size for the hash table, which will be rounded
     to an algorithmically-sounder number.

   By "coarser" than ‘equal?’, we mean that for all X and Y values where
‘(EQUAL-PROC X Y)’, ‘(equal? X Y)’ as well.  If that does not hold for
your EQUAL-PROC, you must provide a HASH-PROC.

   In the case of weak tables, remember that "references" above always
refers to ‘eq?’-wise references.  Just because you have a reference to
some string ‘"foo"’ doesn’t mean that an association with key ‘"foo"’ in
a weak-key table _won’t_ be collected; it only counts as a reference if
the two ‘"foo"’s are ‘eq?’, regardless of EQUAL-PROC.  As such, it is
usually only sensible to use ‘eq?’ and ‘hashq’ as the equivalence and
hash functions for a weak table.  *Note Weak References::, for more
information on Guile’s built-in weak table support.

 -- Scheme Procedure: alist->hash-table alist [equal-proc hash-proc
          #:weak weakness start-size]
     As with ‘make-hash-table’, but initialize it with the associations
     in ALIST.  Where keys are repeated in ALIST, the leftmost
     association takes precedence.

7.5.38.2 Accessing table items
..............................

 -- Scheme Procedure: hash-table-ref table key [default-thunk]
 -- Scheme Procedure: hash-table-ref/default table key default
     Answer the value associated with KEY in TABLE.  If KEY is not
     present, answer the result of invoking the thunk DEFAULT-THUNK,
     which signals an error instead by default.

     ‘hash-table-ref/default’ is a variant that requires a third
     argument, DEFAULT, and answers DEFAULT itself instead of invoking
     it.

 -- Scheme Procedure: hash-table-set! table key new-value
     Set KEY to NEW-VALUE in TABLE.

 -- Scheme Procedure: hash-table-delete! table key
     Remove the association of KEY in TABLE, if present.  If absent, do
     nothing.

 -- Scheme Procedure: hash-table-exists? table key
     Answer whether KEY has an association in TABLE.

 -- Scheme Procedure: hash-table-update! table key modifier
          [default-thunk]
 -- Scheme Procedure: hash-table-update!/default table key modifier
          default
     Replace KEY’s associated value in TABLE by invoking MODIFIER with
     one argument, the old value.

     If KEY is not present, and DEFAULT-THUNK is provided, invoke it
     with no arguments to get the “old value” to be passed to MODIFIER
     as above.  If DEFAULT-THUNK is not provided in such a case, signal
     an error.

     ‘hash-table-update!/default’ is a variant that requires the fourth
     argument, which is used directly as the “old value” rather than as
     a thunk to be invoked to retrieve the “old value”.

7.5.38.3 Table properties
.........................

 -- Scheme Procedure: hash-table-size table
     Answer the number of associations in TABLE.  This is guaranteed to
     run in constant time for non-weak tables.

 -- Scheme Procedure: hash-table-keys table
     Answer an unordered list of the keys in TABLE.

 -- Scheme Procedure: hash-table-values table
     Answer an unordered list of the values in TABLE.

 -- Scheme Procedure: hash-table-walk table proc
     Invoke PROC once for each association in TABLE, passing the key and
     value as arguments.

 -- Scheme Procedure: hash-table-fold table proc init
     Invoke ‘(PROC KEY VALUE PREVIOUS)’ for each KEY and VALUE in TABLE,
     where PREVIOUS is the result of the previous invocation, using INIT
     as the first PREVIOUS value.  Answer the final PROC result.

 -- Scheme Procedure: hash-table->alist table
     Answer an alist where each association in TABLE is an association
     in the result.

7.5.38.4 Hash table algorithms
..............................

Each hash table carries an "equivalence function" and a "hash function",
used to implement key lookups.  Beginning users should follow the rules
for consistency of the default HASH-PROC specified above.  Advanced
users can use these to implement their own equivalence and hash
functions for specialized lookup semantics.

 -- Scheme Procedure: hash-table-equivalence-function hash-table
 -- Scheme Procedure: hash-table-hash-function hash-table
     Answer the equivalence and hash function of HASH-TABLE,
     respectively.

 -- Scheme Procedure: hash obj [size]
 -- Scheme Procedure: string-hash obj [size]
 -- Scheme Procedure: string-ci-hash obj [size]
 -- Scheme Procedure: hash-by-identity obj [size]
     Answer a hash value appropriate for equality predicate ‘equal?’,
     ‘string=?’, ‘string-ci=?’, and ‘eq?’, respectively.

   ‘hash’ is a backwards-compatible replacement for Guile’s built-in
‘hash’.

7.5.39 SRFI-87 => in case clauses
---------------------------------

Starting from version 2.0.6, Guile’s core ‘case’ syntax supports ‘=>’ in
clauses, as specified by SRFI-87/R7RS. *Note Conditionals::.

7.5.40 SRFI-88 Keyword Objects
------------------------------

SRFI-88 (http://srfi.schemers.org/srfi-88/srfi-88.html) provides
"keyword objects", which are equivalent to Guile’s keywords (*note
Keywords::).  SRFI-88 keywords can be entered using the "postfix keyword
syntax", which consists of an identifier followed by ‘:’ (*note
‘postfix’ keyword syntax: Scheme Read.).  SRFI-88 can be made available
with:

     (use-modules (srfi srfi-88))

   Doing so installs the right reader option for keyword syntax, using
‘(read-set! keywords 'postfix)’.  It also provides the procedures
described below.

 -- Scheme Procedure: keyword? obj
     Return ‘#t’ if OBJ is a keyword.  This is the same procedure as the
     same-named built-in procedure (*note ‘keyword?’: Keyword
     Procedures.).

          (keyword? foo:)         ⇒ #t
          (keyword? 'foo:)        ⇒ #t
          (keyword? "foo")        ⇒ #f

 -- Scheme Procedure: keyword->string kw
     Return the name of KW as a string, i.e., without the trailing
     colon.  The returned string may not be modified, e.g., with
     ‘string-set!’.

          (keyword->string foo:)  ⇒ "foo"

 -- Scheme Procedure: string->keyword str
     Return the keyword object whose name is STR.

          (keyword->string (string->keyword "a b c"))     ⇒ "a b c"

7.5.41 SRFI-98 Accessing environment variables.
-----------------------------------------------

This is a portable wrapper around Guile’s built-in support for
interacting with the current environment, *Note Runtime Environment::.

 -- Scheme Procedure: get-environment-variable name
     Returns a string containing the value of the environment variable
     given by the string ‘name’, or ‘#f’ if the named environment
     variable is not found.  This is equivalent to ‘(getenv name)’.

 -- Scheme Procedure: get-environment-variables
     Returns the names and values of all the environment variables as an
     association list in which both the keys and the values are strings.

7.5.42 SRFI-105 Curly-infix expressions.
----------------------------------------

Guile’s built-in reader includes support for SRFI-105 curly-infix
expressions.  See the specification of SRFI-105
(http://srfi.schemers.org/srfi-105/srfi-105.html).  Some examples:

     {n <= 5}                ⇒  (<= n 5)
     {a + b + c}             ⇒  (+ a b c)
     {a * {b + c}}           ⇒  (* a (+ b c))
     {(- a) / b}             ⇒  (/ (- a) b)
     {-(a) / b}              ⇒  (/ (- a) b) as well
     {(f a b) + (g h)}       ⇒  (+ (f a b) (g h))
     {f(a b) + g(h)}         ⇒  (+ (f a b) (g h)) as well
     {f[a b] + g(h)}         ⇒  (+ ($bracket-apply$ f a b) (g h))
     '{a + f(b) + x}         ⇒  '(+ a (f b) x)
     {length(x) >= 6}        ⇒  (>= (length x) 6)
     {n-1 + n-2}             ⇒  (+ n-1 n-2)
     {n * factorial{n - 1}}  ⇒  (* n (factorial (- n 1)))
     {{a > 0} and {b >= 1}}  ⇒  (and (> a 0) (>= b 1))
     {f{n - 1}(x)}           ⇒  ((f (- n 1)) x)
     {a . z}                 ⇒  ($nfx$ a . z)
     {a + b - c}             ⇒  ($nfx$ a + b - c)

   To enable curly-infix expressions within a file, place the reader
directive ‘#!curly-infix’ before the first use of curly-infix notation.
To globally enable curly-infix expressions in Guile’s reader, set the
‘curly-infix’ read option.

   Guile also implements the following non-standard extension to
SRFI-105: if ‘curly-infix’ is enabled and there is no other meaning
assigned to square brackets (i.e.  the ‘square-brackets’ read option is
turned off), then lists within square brackets are read as normal lists
but with the special symbol ‘$bracket-list$’ added to the front.  To
enable this combination of read options within a file, use the reader
directive ‘#!curly-infix-and-bracket-lists’.  For example:

     [a b]    ⇒  ($bracket-list$ a b)
     [a . b]  ⇒  ($bracket-list$ a . b)

   For more information on reader options, *Note Scheme Read::.

7.5.43 SRFI-111 Boxes.
----------------------

SRFI-111 (http://srfi.schemers.org/srfi-111/srfi-111.html) provides
boxes: objects with a single mutable cell.

 -- Scheme Procedure: box value
     Return a newly allocated box whose contents is initialized to
     VALUE.

 -- Scheme Procedure: box? obj
     Return true if OBJ is a box, otherwise return false.

 -- Scheme Procedure: unbox box
     Return the current contents of BOX.

 -- Scheme Procedure: set-box! box value
     Set the contents of BOX to VALUE.

