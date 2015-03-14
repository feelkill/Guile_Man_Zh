7.6 R6RS Support
================

*Note R6RS Libraries::, for more information on how to define R6RS
libraries, and their integration with Guile modules.

7.6.1 Incompatibilities with the R6RS
-------------------------------------

There are some incompatibilities between Guile and the R6RS. Some of
them are intentional, some of them are bugs, and some are simply
unimplemented features.  Please let the Guile developers know if you
find one that is not on this list.

   • The R6RS specifies many situations in which a conforming
     implementation must signal a specific error.  Guile doesn’t really
     care about that too much—if a correct R6RS program would not hit
     that error, we don’t bother checking for it.

   • Multiple ‘library’ forms in one file are not yet supported.  This
     is because the expansion of ‘library’ sets the current module, but
     does not restore it.  This is a bug.

   • R6RS unicode escapes within strings are disabled by default,
     because they conflict with Guile’s already-existing escapes.  The
     same is the case for R6RS treatment of escaped newlines in strings.

     R6RS behavior can be turned on via a reader option.  *Note String
     Syntax::, for more information.

   • A ‘set!’ to a variable transformer may only expand to an
     expression, not a definition—even if the original ‘set!’ expression
     was in definition context.

   • Instead of using the algorithm detailed in chapter 10 of the R6RS,
     expansion of toplevel forms happens sequentially.

     For example, while the expansion of the following set of toplevel
     definitions does the correct thing:

          (begin
           (define even?
             (lambda (x)
               (or (= x 0) (odd? (- x 1)))))
           (define-syntax odd?
             (syntax-rules ()
               ((odd? x) (not (even? x)))))
           (even? 10))
          ⇒ #t

     The same definitions outside of the ‘begin’ wrapper do not:

          (define even?
            (lambda (x)
              (or (= x 0) (odd? (- x 1)))))
          (define-syntax odd?
            (syntax-rules ()
              ((odd? x) (not (even? x)))))
          (even? 10)
          <unnamed port>:4:18: In procedure even?:
          <unnamed port>:4:18: Wrong type to apply: #<syntax-transformer odd?>

     This is because when expanding the right-hand-side of ‘even?’, the
     reference to ‘odd?’ is not yet marked as a syntax transformer, so
     it is assumed to be a function.

     This bug will only affect top-level programs, not code in ‘library’
     forms.  Fixing it for toplevel forms seems doable, but tricky to
     implement in a backward-compatible way.  Suggestions and/or patches
     would be appreciated.

   • The ‘(rnrs io ports)’ module is incomplete.  Work is ongoing to fix
     this.

   • Guile does not prevent use of textual I/O procedures on binary
     ports.  More generally, it does not make a sharp distinction
     between binary and textual ports (*note binary-port?: R6RS Port
     Manipulation.).

   • Guile’s implementation of ‘equal?’ may fail to terminate when
     applied to arguments containing cycles.

7.6.2 R6RS Standard Libraries
-----------------------------

In contrast with earlier versions of the Revised Report, the R6RS
organizes the procedures and syntactic forms required of conforming
implementations into a set of “standard libraries” which can be imported
as necessary by user programs and libraries.  Here we briefly list the
libraries that have been implemented for Guile.

   We do not attempt to document these libraries fully here, as most of
their functionality is already available in Guile itself.  The
expectation is that most Guile users will use the well-known and
well-documented Guile modules.  These R6RS libraries are mostly useful
to users who want to port their code to other R6RS systems.

   The documentation in the following sections reproduces some of the
content of the library section of the Report, but is mostly intended to
provide supplementary information about Guile’s implementation of the
R6RS standard libraries.  For complete documentation, design rationales
and further examples, we advise you to consult the “Standard Libraries”
section of the Report (*note R6RS Standard Libraries: (r6rs)Standard
Libraries.).

7.6.2.1 Library Usage
.....................

Guile implements the R6RS ‘library’ form as a transformation to a native
Guile module definition.  As a consequence of this, all of the libraries
described in the following subsections, in addition to being available
for use by R6RS libraries and top-level programs, can also be imported
as if they were normal Guile modules—via a ‘use-modules’ form, say.  For
example, the R6RS “composite” library can be imported by:

       (import (rnrs (6)))

       (use-modules ((rnrs) :version (6)))

   For more information on Guile’s library implementation, see (*note
R6RS Libraries::).

7.6.2.2 rnrs base
.................

The ‘(rnrs base (6))’ library exports the procedures and syntactic forms
described in the main section of the Report (*note R6RS Base library:
(r6rs)Base library.).  They are grouped below by the existing manual
sections to which they correspond.

 -- Scheme Procedure: boolean? obj
 -- Scheme Procedure: not x
     *Note Booleans::, for documentation.

 -- Scheme Procedure: symbol? obj
 -- Scheme Procedure: symbol->string sym
 -- Scheme Procedure: string->symbol str
     *Note Symbol Primitives::, for documentation.

 -- Scheme Procedure: char? obj
 -- Scheme Procedure: char=?
 -- Scheme Procedure: char<?
 -- Scheme Procedure: char>?
 -- Scheme Procedure: char<=?
 -- Scheme Procedure: char>=?
 -- Scheme Procedure: integer->char n
 -- Scheme Procedure: char->integer chr
     *Note Characters::, for documentation.

 -- Scheme Procedure: list? x
 -- Scheme Procedure: null? x
     *Note List Predicates::, for documentation.

 -- Scheme Procedure: pair? x
 -- Scheme Procedure: cons x y
 -- Scheme Procedure: car pair
 -- Scheme Procedure: cdr pair
 -- Scheme Procedure: caar pair
 -- Scheme Procedure: cadr pair
 -- Scheme Procedure: cdar pair
 -- Scheme Procedure: cddr pair
 -- Scheme Procedure: caaar pair
 -- Scheme Procedure: caadr pair
 -- Scheme Procedure: cadar pair
 -- Scheme Procedure: cdaar pair
 -- Scheme Procedure: caddr pair
 -- Scheme Procedure: cdadr pair
 -- Scheme Procedure: cddar pair
 -- Scheme Procedure: cdddr pair
 -- Scheme Procedure: caaaar pair
 -- Scheme Procedure: caaadr pair
 -- Scheme Procedure: caadar pair
 -- Scheme Procedure: cadaar pair
 -- Scheme Procedure: cdaaar pair
 -- Scheme Procedure: cddaar pair
 -- Scheme Procedure: cdadar pair
 -- Scheme Procedure: cdaadr pair
 -- Scheme Procedure: cadadr pair
 -- Scheme Procedure: caaddr pair
 -- Scheme Procedure: caddar pair
 -- Scheme Procedure: cadddr pair
 -- Scheme Procedure: cdaddr pair
 -- Scheme Procedure: cddadr pair
 -- Scheme Procedure: cdddar pair
 -- Scheme Procedure: cddddr pair
     *Note Pairs::, for documentation.

 -- Scheme Procedure: number? obj
     *Note Numerical Tower::, for documentation.

 -- Scheme Procedure: string? obj
     *Note String Predicates::, for documentation.

 -- Scheme Procedure: procedure? obj
     *Note Procedure Properties::, for documentation.

 -- Scheme Syntax: define name value
 -- Scheme Syntax: set! variable-name value
     *Note Definition::, for documentation.

 -- Scheme Syntax: define-syntax keyword expression
 -- Scheme Syntax: let-syntax ((keyword transformer) …) exp1 exp2 …
 -- Scheme Syntax: letrec-syntax ((keyword transformer) …) exp1 exp2 …
     *Note Defining Macros::, for documentation.

 -- Scheme Syntax: identifier-syntax exp
     *Note Identifier Macros::, for documentation.

 -- Scheme Syntax: syntax-rules literals (pattern template) ...
     *Note Syntax Rules::, for documentation.

 -- Scheme Syntax: lambda formals body
     *Note Lambda::, for documentation.

 -- Scheme Syntax: let bindings body
 -- Scheme Syntax: let* bindings body
 -- Scheme Syntax: letrec bindings body
 -- Scheme Syntax: letrec* bindings body
     *Note Local Bindings::, for documentation.

 -- Scheme Syntax: let-values bindings body
 -- Scheme Syntax: let*-values bindings body
     *Note SRFI-11::, for documentation.

 -- Scheme Syntax: begin expr1 expr2 ...
     *Note begin::, for documentation.

 -- Scheme Syntax: quote expr
 -- Scheme Syntax: quasiquote expr
 -- Scheme Syntax: unquote expr
 -- Scheme Syntax: unquote-splicing expr
     *Note Expression Syntax::, for documentation.

 -- Scheme Syntax: if test consequence [alternate]
 -- Scheme Syntax: cond clause1 clause2 ...
 -- Scheme Syntax: case key clause1 clause2 ...
     *Note Conditionals::, for documentation.

 -- Scheme Syntax: and expr ...
 -- Scheme Syntax: or expr ...
     *Note and or::, for documentation.

 -- Scheme Procedure: eq? x y
 -- Scheme Procedure: eqv? x y
 -- Scheme Procedure: equal? x y
 -- Scheme Procedure: symbol=? symbol1 symbol2 ...
     *Note Equality::, for documentation.

     ‘symbol=?’ is identical to ‘eq?’.

 -- Scheme Procedure: complex? z
     *Note Complex Numbers::, for documentation.

 -- Scheme Procedure: real-part z
 -- Scheme Procedure: imag-part z
 -- Scheme Procedure: make-rectangular real_part imaginary_part
 -- Scheme Procedure: make-polar x y
 -- Scheme Procedure: magnitude z
 -- Scheme Procedure: angle z
     *Note Complex::, for documentation.

 -- Scheme Procedure: sqrt z
 -- Scheme Procedure: exp z
 -- Scheme Procedure: expt z1 z2
 -- Scheme Procedure: log z
 -- Scheme Procedure: sin z
 -- Scheme Procedure: cos z
 -- Scheme Procedure: tan z
 -- Scheme Procedure: asin z
 -- Scheme Procedure: acos z
 -- Scheme Procedure: atan z
     *Note Scientific::, for documentation.

 -- Scheme Procedure: real? x
 -- Scheme Procedure: rational? x
 -- Scheme Procedure: numerator x
 -- Scheme Procedure: denominator x
 -- Scheme Procedure: rationalize x eps
     *Note Reals and Rationals::, for documentation.

 -- Scheme Procedure: exact? x
 -- Scheme Procedure: inexact? x
 -- Scheme Procedure: exact z
 -- Scheme Procedure: inexact z
     *Note Exactness::, for documentation.  The ‘exact’ and ‘inexact’
     procedures are identical to the ‘inexact->exact’ and
     ‘exact->inexact’ procedures provided by Guile’s code library.

 -- Scheme Procedure: integer? x
     *Note Integers::, for documentation.

 -- Scheme Procedure: odd? n
 -- Scheme Procedure: even? n
 -- Scheme Procedure: gcd x ...
 -- Scheme Procedure: lcm x ...
 -- Scheme Procedure: exact-integer-sqrt k
     *Note Integer Operations::, for documentation.

 -- Scheme Procedure: =
 -- Scheme Procedure: <
 -- Scheme Procedure: >
 -- Scheme Procedure: <=
 -- Scheme Procedure: >=
 -- Scheme Procedure: zero? x
 -- Scheme Procedure: positive? x
 -- Scheme Procedure: negative? x
     *Note Comparison::, for documentation.

 -- Scheme Procedure: for-each f lst1 lst2 ...
     *Note SRFI-1 Fold and Map::, for documentation.

 -- Scheme Procedure: list elem …
     *Note List Constructors::, for documentation.

 -- Scheme Procedure: length lst
 -- Scheme Procedure: list-ref lst k
 -- Scheme Procedure: list-tail lst k
     *Note List Selection::, for documentation.

 -- Scheme Procedure: append lst … obj
 -- Scheme Procedure: append
 -- Scheme Procedure: reverse lst
     *Note Append/Reverse::, for documentation.

 -- Scheme Procedure: number->string n [radix]
 -- Scheme Procedure: string->number str [radix]
     *Note Conversion::, for documentation.

 -- Scheme Procedure: string char ...
 -- Scheme Procedure: make-string k [chr]
 -- Scheme Procedure: list->string lst
     *Note String Constructors::, for documentation.

 -- Scheme Procedure: string->list str [start [end]]
     *Note List/String Conversion::, for documentation.

 -- Scheme Procedure: string-length str
 -- Scheme Procedure: string-ref str k
 -- Scheme Procedure: string-copy str [start [end]]
 -- Scheme Procedure: substring str start [end]
     *Note String Selection::, for documentation.

 -- Scheme Procedure: string=? s1 s2 s3 …
 -- Scheme Procedure: string<? s1 s2 s3 …
 -- Scheme Procedure: string>? s1 s2 s3 …
 -- Scheme Procedure: string<=? s1 s2 s3 …
 -- Scheme Procedure: string>=? s1 s2 s3 …
     *Note String Comparison::, for documentation.

 -- Scheme Procedure: string-append arg …
     *Note Reversing and Appending Strings::, for documentation.

 -- Scheme Procedure: string-for-each proc s [start [end]]
     *Note Mapping Folding and Unfolding::, for documentation.

 -- Scheme Procedure: + z1 ...
 -- Scheme Procedure: - z1 z2 ...
 -- Scheme Procedure: * z1 ...
 -- Scheme Procedure: / z1 z2 ...
 -- Scheme Procedure: max x1 x2 ...
 -- Scheme Procedure: min x1 x2 ...
 -- Scheme Procedure: abs x
 -- Scheme Procedure: truncate x
 -- Scheme Procedure: floor x
 -- Scheme Procedure: ceiling x
 -- Scheme Procedure: round x
     *Note Arithmetic::, for documentation.

 -- Scheme Procedure: div x y
 -- Scheme Procedure: mod x y
 -- Scheme Procedure: div-and-mod x y
     These procedures accept two real numbers X and Y, where the divisor
     Y must be non-zero.  ‘div’ returns the integer Q and ‘mod’ returns
     the real number R such that X = Q*Y + R and 0 <= R < abs(Y).
     ‘div-and-mod’ returns both Q and R, and is more efficient than
     computing each separately.  Note that when Y > 0, ‘div’ returns
     floor(X/Y), otherwise it returns ceiling(X/Y).

          (div 123 10) ⇒ 12
          (mod 123 10) ⇒ 3
          (div-and-mod 123 10) ⇒ 12 and 3
          (div-and-mod 123 -10) ⇒ -12 and 3
          (div-and-mod -123 10) ⇒ -13 and 7
          (div-and-mod -123 -10) ⇒ 13 and 7
          (div-and-mod -123.2 -63.5) ⇒ 2.0 and 3.8
          (div-and-mod 16/3 -10/7) ⇒ -3 and 22/21

 -- Scheme Procedure: div0 x y
 -- Scheme Procedure: mod0 x y
 -- Scheme Procedure: div0-and-mod0 x y
     These procedures accept two real numbers X and Y, where the divisor
     Y must be non-zero.  ‘div0’ returns the integer Q and ‘mod0’
     returns the real number R such that X = Q*Y + R and -abs(Y/2) <= R
     < abs(Y/2).  ‘div0-and-mod0’ returns both Q and R, and is more
     efficient than computing each separately.

     Note that ‘div0’ returns X/Y rounded to the nearest integer.  When
     X/Y lies exactly half-way between two integers, the tie is broken
     according to the sign of Y.  If Y > 0, ties are rounded toward
     positive infinity, otherwise they are rounded toward negative
     infinity.  This is a consequence of the requirement that -abs(Y/2)
     <= R < abs(Y/2).

          (div0 123 10) ⇒ 12
          (mod0 123 10) ⇒ 3
          (div0-and-mod0 123 10) ⇒ 12 and 3
          (div0-and-mod0 123 -10) ⇒ -12 and 3
          (div0-and-mod0 -123 10) ⇒ -12 and -3
          (div0-and-mod0 -123 -10) ⇒ 12 and -3
          (div0-and-mod0 -123.2 -63.5) ⇒ 2.0 and 3.8
          (div0-and-mod0 16/3 -10/7) ⇒ -4 and -8/21

 -- Scheme Procedure: real-valued? obj
 -- Scheme Procedure: rational-valued? obj
 -- Scheme Procedure: integer-valued? obj
     These procedures return ‘#t’ if and only if their arguments can,
     respectively, be coerced to a real, rational, or integer value
     without a loss of numerical precision.

     ‘real-valued?’ will return ‘#t’ for complex numbers whose imaginary
     parts are zero.

 -- Scheme Procedure: nan? x
 -- Scheme Procedure: infinite? x
 -- Scheme Procedure: finite? x
     ‘nan?’ returns ‘#t’ if X is a NaN value, ‘#f’ otherwise.
     ‘infinite?’ returns ‘#t’ if X is an infinite value, ‘#f’ otherwise.
     ‘finite?’ returns ‘#t’ if X is neither infinite nor a NaN value,
     otherwise it returns ‘#f’.  Every real number satisfies exactly one
     of these predicates.  An exception is raised if X is not real.

 -- Scheme Syntax: assert expr
     Raises an ‘&assertion’ condition if EXPR evaluates to ‘#f’;
     otherwise evaluates to the value of EXPR.

 -- Scheme Procedure: error who message irritant1 ...
 -- Scheme Procedure: assertion-violation who message irritant1 ...
     These procedures raise compound conditions based on their
     arguments: If WHO is not ‘#f’, the condition will include a ‘&who’
     condition whose ‘who’ field is set to WHO; a ‘&message’ condition
     will be included with a ‘message’ field equal to MESSAGE; an
     ‘&irritants’ condition will be included with its ‘irritants’ list
     given by ‘irritant1 ...’.

     ‘error’ produces a compound condition with the simple conditions
     described above, as well as an ‘&error’ condition;
     ‘assertion-violation’ produces one that includes an ‘&assertion’
     condition.

 -- Scheme Procedure: vector-map proc v
 -- Scheme Procedure: vector-for-each proc v
     These procedures implement the ‘map’ and ‘for-each’ contracts over
     vectors.

 -- Scheme Procedure: vector arg …
 -- Scheme Procedure: vector? obj
 -- Scheme Procedure: make-vector len
 -- Scheme Procedure: make-vector len fill
 -- Scheme Procedure: list->vector l
 -- Scheme Procedure: vector->list v
     *Note Vector Creation::, for documentation.

 -- Scheme Procedure: vector-length vector
 -- Scheme Procedure: vector-ref vector k
 -- Scheme Procedure: vector-set! vector k obj
 -- Scheme Procedure: vector-fill! v fill
     *Note Vector Accessors::, for documentation.

 -- Scheme Procedure: call-with-current-continuation proc
 -- Scheme Procedure: call/cc proc
     *Note Continuations::, for documentation.

 -- Scheme Procedure: values arg …
 -- Scheme Procedure: call-with-values producer consumer
     *Note Multiple Values::, for documentation.

 -- Scheme Procedure: dynamic-wind in_guard thunk out_guard
     *Note Dynamic Wind::, for documentation.

 -- Scheme Procedure: apply proc arg … arglst
     *Note Fly Evaluation::, for documentation.

7.6.2.3 rnrs unicode
....................

The ‘(rnrs unicode (6))’ library provides procedures for manipulating
Unicode characters and strings.

 -- Scheme Procedure: char-upcase char
 -- Scheme Procedure: char-downcase char
 -- Scheme Procedure: char-titlecase char
 -- Scheme Procedure: char-foldcase char
     These procedures translate their arguments from one Unicode
     character set to another.  ‘char-upcase’, ‘char-downcase’, and
     ‘char-titlecase’ are identical to their counterparts in the Guile
     core library; *Note Characters::, for documentation.

     ‘char-foldcase’ returns the result of applying ‘char-upcase’ to its
     argument, followed by ‘char-downcase’—except in the case of the
     Turkic characters ‘U+0130’ and ‘U+0131’, for which the procedure
     acts as the identity function.

 -- Scheme Procedure: char-ci=? char1 char2 char3 ...
 -- Scheme Procedure: char-ci<? char1 char2 char3 ...
 -- Scheme Procedure: char-ci>? char1 char2 char3 ...
 -- Scheme Procedure: char-ci<=? char1 char2 char3 ...
 -- Scheme Procedure: char-ci>=? char1 char2 char3 ...
     These procedures facilitate case-insensitive comparison of Unicode
     characters.  They are identical to the procedures provided by
     Guile’s core library.  *Note Characters::, for documentation.

 -- Scheme Procedure: char-alphabetic? char
 -- Scheme Procedure: char-numeric? char
 -- Scheme Procedure: char-whitespace? char
 -- Scheme Procedure: char-upper-case? char
 -- Scheme Procedure: char-lower-case? char
 -- Scheme Procedure: char-title-case? char
     These procedures implement various Unicode character set
     predicates.  They are identical to the procedures provided by
     Guile’s core library.  *Note Characters::, for documentation.

 -- Scheme Procedure: char-general-category char
     *Note Characters::, for documentation.

 -- Scheme Procedure: string-upcase string
 -- Scheme Procedure: string-downcase string
 -- Scheme Procedure: string-titlecase string
 -- Scheme Procedure: string-foldcase string
     These procedures perform Unicode case folding operations on their
     input.  *Note Alphabetic Case Mapping::, for documentation.

 -- Scheme Procedure: string-ci=? string1 string2 string3 ...
 -- Scheme Procedure: string-ci<? string1 string2 string3 ...
 -- Scheme Procedure: string-ci>? string1 string2 string3 ...
 -- Scheme Procedure: string-ci<=? string1 string2 string3 ...
 -- Scheme Procedure: string-ci>=? string1 string2 string3 ...
     These procedures perform case-insensitive comparison on their
     input.  *Note String Comparison::, for documentation.

 -- Scheme Procedure: string-normalize-nfd string
 -- Scheme Procedure: string-normalize-nfkd string
 -- Scheme Procedure: string-normalize-nfc string
 -- Scheme Procedure: string-normalize-nfkc string
     These procedures perform Unicode string normalization operations on
     their input.  *Note String Comparison::, for documentation.

7.6.2.4 rnrs bytevectors
........................

The ‘(rnrs bytevectors (6))’ library provides procedures for working
with blocks of binary data.  This functionality is documented in its own
section of the manual; *Note Bytevectors::.

7.6.2.5 rnrs lists
..................

The ‘(rnrs lists (6))’ library provides procedures additional procedures
for working with lists.

 -- Scheme Procedure: find proc list
     This procedure is identical to the one defined in Guile’s SRFI-1
     implementation.  *Note SRFI-1 Searching::, for documentation.

 -- Scheme Procedure: for-all proc list1 list2 ...
 -- Scheme Procedure: exists proc list1 list2 ...

     The ‘for-all’ procedure is identical to the ‘every’ procedure
     defined by SRFI-1; the ‘exists’ procedure is identical to SRFI-1’s
     ‘any’.  *Note SRFI-1 Searching::, for documentation.

 -- Scheme Procedure: filter proc list
 -- Scheme Procedure: partition proc list
     These procedures are identical to the ones provided by SRFI-1.
     *Note List Modification::, for a description of ‘filter’; *Note
     SRFI-1 Filtering and Partitioning::, for ‘partition’.

 -- Scheme Procedure: fold-left combine nil list1 list2 …
 -- Scheme Procedure: fold-right combine nil list1 list2 …
     These procedures are identical to the ‘fold’ and ‘fold-right’
     procedures provided by SRFI-1.  *Note SRFI-1 Fold and Map::, for
     documentation.

 -- Scheme Procedure: remp proc list
 -- Scheme Procedure: remove obj list
 -- Scheme Procedure: remv obj list
 -- Scheme Procedure: remq obj list
     ‘remove’, ‘remv’, and ‘remq’ are identical to the ‘delete’, ‘delv’,
     and ‘delq’ procedures provided by Guile’s core library, (*note List
     Modification::).  ‘remp’ is identical to the alternate ‘remove’
     procedure provided by SRFI-1; *Note SRFI-1 Deleting::.

 -- Scheme Procedure: memp proc list
 -- Scheme Procedure: member obj list
 -- Scheme Procedure: memv obj list
 -- Scheme Procedure: memq obj list
     ‘member’, ‘memv’, and ‘memq’ are identical to the procedures
     provided by Guile’s core library; *Note List Searching::, for their
     documentation.  ‘memp’ uses the specified predicate function ‘proc’
     to test elements of the list LIST—it behaves similarly to ‘find’,
     except that it returns the first sublist of LIST whose ‘car’
     satisfies PROC.

 -- Scheme Procedure: assp proc alist
 -- Scheme Procedure: assoc obj alist
 -- Scheme Procedure: assv obj alist
 -- Scheme Procedure: assq obj alist
     ‘assoc’, ‘assv’, and ‘assq’ are identical to the procedures
     provided by Guile’s core library; *Note Alist Key Equality::, for
     their documentation.  ‘assp’ uses the specified predicate function
     ‘proc’ to test keys in the association list ALIST.

 -- Scheme Procedure: cons* obj1 ... obj
 -- Scheme Procedure: cons* obj
     This procedure is identical to the one exported by Guile’s core
     library.  *Note List Constructors::, for documentation.

7.6.2.6 rnrs sorting
....................

The ‘(rnrs sorting (6))’ library provides procedures for sorting lists
and vectors.

 -- Scheme Procedure: list-sort proc list
 -- Scheme Procedure: vector-sort proc vector
     These procedures return their input sorted in ascending order,
     without modifying the original data.  PROC must be a procedure that
     takes two elements from the input list or vector as arguments, and
     returns a true value if the first is “less” than the second, ‘#f’
     otherwise.  ‘list-sort’ returns a list; ‘vector-sort’ returns a
     vector.

     Both ‘list-sort’ and ‘vector-sort’ are implemented in terms of the
     ‘stable-sort’ procedure from Guile’s core library.  *Note
     Sorting::, for a discussion of the behavior of that procedure.

 -- Scheme Procedure: vector-sort! proc vector
     Performs a destructive, “in-place” sort of VECTOR, using PROC as
     described above to determine an ascending ordering of elements.
     ‘vector-sort!’ returns an unspecified value.

     This procedure is implemented in terms of the ‘sort!’ procedure
     from Guile’s core library.  *Note Sorting::, for more information.

7.6.2.7 rnrs control
....................

The ‘(rnrs control (6))’ library provides syntactic forms useful for
constructing conditional expressions and controlling the flow of
execution.

 -- Scheme Syntax: when test expression1 expression2 ...
 -- Scheme Syntax: unless test expression1 expression2 ...
     The ‘when’ form is evaluated by evaluating the specified TEST
     expression; if the result is a true value, the EXPRESSIONs that
     follow it are evaluated in order, and the value of the final
     EXPRESSION becomes the value of the entire ‘when’ expression.

     The ‘unless’ form behaves similarly, with the exception that the
     specified EXPRESSIONs are only evaluated if the value of TEST is
     false.

 -- Scheme Syntax: do ((variable init step) ...) (test expression ...)
          command ...
     This form is identical to the one provided by Guile’s core library.
     *Note while do::, for documentation.

 -- Scheme Syntax: case-lambda clause ...
     This form is identical to the one provided by Guile’s core library.
     *Note Case-lambda::, for documentation.

7.6.2.8 R6RS Records
....................

The manual sections below describe Guile’s implementation of R6RS
records, which provide support for user-defined data types.  The R6RS
records API provides a superset of the features provided by Guile’s
“native” records, as well as those of the SRFI-9 records API; *Note
Records::, and *note SRFI-9 Records::, for a description of those
interfaces.

   As with SRFI-9 and Guile’s native records, R6RS records are
constructed using a record-type descriptor that specifies attributes
like the record’s name, its fields, and the mutability of those fields.

   R6RS records extend this framework to support single inheritance via
the specification of a “parent” type for a record type at definition
time.  Accessors and mutator procedures for the fields of a parent type
may be applied to records of a subtype of this parent.  A record type
may be "sealed", in which case it cannot be used as the parent of
another record type.

   The inheritance mechanism for record types also informs the process
of initializing the fields of a record and its parents.  Constructor
procedures that generate new instances of a record type are obtained
from a record constructor descriptor, which encapsulates the record-type
descriptor of the record to be constructed along with a "protocol"
procedure that defines how constructors for record subtypes delegate to
the constructors of their parent types.

   A protocol is a procedure used by the record system at construction
time to bind arguments to the fields of the record being constructed.
The protocol procedure is passed a procedure N that accepts the
arguments required to construct the record’s parent type; this
procedure, when invoked, will return a procedure P that accepts the
arguments required to construct a new instance of the record type itself
and returns a new instance of the record type.

   The protocol should in turn return a procedure that uses N and P to
initialize the fields of the record type and its parent type(s).  This
procedure will be the constructor returned by

   As a trivial example, consider the hypothetical record type ‘pixel’,
which encapsulates an x-y location on a screen, and ‘voxel’, which has
‘pixel’ as its parent type and stores an additional coordinate.  The
following protocol produces a constructor procedure that accepts all
three coordinates, uses the first two to initialize the fields of
‘pixel’, and binds the third to the single field of ‘voxel’.

       (lambda (n)
         (lambda (x y z)
           (let ((p (n x y)))
             (p z))))

   It may be helpful to think of protocols as “constructor factories”
that produce chains of delegating constructors glued together by the
helper procedure N.

   An R6RS record type may be declared to be "nongenerative" via the use
of a unique generated or user-supplied symbol—or "uid"—such that
subsequent record type declarations with the same uid and attributes
will return the previously-declared record-type descriptor.

   R6RS record types may also be declared to be "opaque", in which case
the various predicates and introspection procedures defined in ‘(rnrs
records introspection)’ will behave as if records of this type are not
records at all.

   Note that while the R6RS records API shares much of its namespace
with both the SRFI-9 and native Guile records APIs, it is not currently
compatible with either.

7.6.2.9 rnrs records syntactic
..............................

The ‘(rnrs records syntactic (6))’ library exports the syntactic API for
working with R6RS records.

 -- Scheme Syntax: define-record-type name-spec record-clause …
     Defines a new record type, introducing bindings for a record-type
     descriptor, a record constructor descriptor, a constructor
     procedure, a record predicate, and accessor and mutator procedures
     for the new record type’s fields.

     NAME-SPEC must either be an identifier or must take the form
     ‘(record-name constructor-name predicate-name)’, where RECORD-NAME,
     CONSTRUCTOR-NAME, and PREDICATE-NAME are all identifiers and
     specify the names to which, respectively, the record-type
     descriptor, constructor, and predicate procedures will be bound.
     If NAME-SPEC is only an identifier, it specifies the name to which
     the generated record-type descriptor will be bound.

     Each RECORD-CLAUSE must be one of the following:

        • ‘(fields field-spec*)’, where each FIELD-SPEC specifies a
          field of the new record type and takes one of the following
          forms:
             • ‘(immutable field-name accessor-name)’, which specifies
               an immutable field with the name FIELD-NAME and binds an
               accessor procedure for it to the name given by
               ACCESSOR-NAME
             • ‘(mutable field-name accessor-name mutator-name)’, which
               specifies a mutable field with the name FIELD-NAME and
               binds accessor and mutator procedures to ACCESSOR-NAME
               and MUTATOR-NAME, respectively
             • ‘(immutable field-name)’, which specifies an immutable
               field with the name FIELD-NAME; an accessor procedure for
               it will be created and named by appending record name and
               FIELD-NAME with a hyphen separator
             • ‘(mutable field-name’), which specifies a mutable field
               with the name FIELD-NAME; an accessor procedure for it
               will be created and named as described above; a mutator
               procedure will also be created and named by appending
               ‘-set!’ to the accessor name
             • ‘field-name’, which specifies an immutable field with the
               name FIELD-NAME; an access procedure for it will be
               created and named as described above
        • ‘(parent parent-name)’, where PARENT-NAME is a symbol giving
          the name of the record type to be used as the parent of the
          new record type
        • ‘(protocol expression)’, where EXPRESSION evaluates to a
          protocol procedure which behaves as described above, and is
          used to create a record constructor descriptor for the new
          record type
        • ‘(sealed sealed?)’, where SEALED? is a boolean value that
          specifies whether or not the new record type is sealed
        • ‘(opaque opaque?)’, where OPAQUE? is a boolean value that
          specifies whether or not the new record type is opaque
        • ‘(nongenerative [uid])’, which specifies that the record type
          is nongenerative via the optional uid UID.  If UID is not
          specified, a unique uid will be generated at expansion time
        • ‘(parent-rtd parent-rtd parent-cd)’, a more explicit form of
          the ‘parent’ form above; PARENT-RTD and PARENT-CD should
          evaluate to a record-type descriptor and a record constructor
          descriptor, respectively

 -- Scheme Syntax: record-type-descriptor record-name
     Evaluates to the record-type descriptor associated with the type
     specified by RECORD-NAME.

 -- Scheme Syntax: record-constructor-descriptor record-name
     Evaluates to the record-constructor descriptor associated with the
     type specified by RECORD-NAME.

7.6.2.10 rnrs records procedural
................................

The ‘(rnrs records procedural (6))’ library exports the procedural API
for working with R6RS records.

 -- Scheme Procedure: make-record-type-descriptor name parent uid
          sealed? opaque? fields
     Returns a new record-type descriptor with the specified
     characteristics: NAME must be a symbol giving the name of the new
     record type; PARENT must be either ‘#f’ or a non-sealed record-type
     descriptor for the returned record type to extend; UID must be
     either ‘#f’, indicating that the record type is generative, or a
     symbol giving the type’s nongenerative uid; SEALED? and OPAQUE?
     must be boolean values that specify the sealedness and opaqueness
     of the record type; FIELDS must be a vector of zero or more field
     specifiers of the form ‘(mutable name)’ or ‘(immutable name)’,
     where name is a symbol giving a name for the field.

     If UID is not ‘#f’, it must be a symbol

 -- Scheme Procedure: record-type-descriptor? obj
     Returns ‘#t’ if OBJ is a record-type descriptor, ‘#f’ otherwise.

 -- Scheme Procedure: make-record-constructor-descriptor rtd
          parent-constructor-descriptor protocol
     Returns a new record constructor descriptor that can be used to
     produce constructors for the record type specified by the
     record-type descriptor RTD and whose delegation and binding
     behavior are specified by the protocol procedure PROTOCOL.

     PARENT-CONSTRUCTOR-DESCRIPTOR specifies a record constructor
     descriptor for the parent type of RTD, if one exists.  If RTD
     represents a base type, then PARENT-CONSTRUCTOR-DESCRIPTOR must be
     ‘#f’.  If RTD is an extension of another type,
     PARENT-CONSTRUCTOR-DESCRIPTOR may still be ‘#f’, but protocol must
     also be ‘#f’ in this case.

 -- Scheme Procedure: record-constructor rcd
     Returns a record constructor procedure by invoking the protocol
     defined by the record-constructor descriptor RCD.

 -- Scheme Procedure: record-predicate rtd
     Returns the record predicate procedure for the record-type
     descriptor RTD.

 -- Scheme Procedure: record-accessor rtd k
     Returns the record field accessor procedure for the Kth field of
     the record-type descriptor RTD.

 -- Scheme Procedure: record-mutator rtd k
     Returns the record field mutator procedure for the Kth field of the
     record-type descriptor RTD.  An ‘&assertion’ condition will be
     raised if this field is not mutable.

7.6.2.11 rnrs records inspection
................................

The ‘(rnrs records inspection (6))’ library provides procedures useful
for accessing metadata about R6RS records.

 -- Scheme Procedure: record? obj
     Return ‘#t’ if the specified object is a non-opaque R6RS record,
     ‘#f’ otherwise.

 -- Scheme Procedure: record-rtd record
     Returns the record-type descriptor for RECORD.  An ‘&assertion’ is
     raised if RECORD is opaque.

 -- Scheme Procedure: record-type-name rtd
     Returns the name of the record-type descriptor RTD.

 -- Scheme Procedure: record-type-parent rtd
     Returns the parent of the record-type descriptor RTD, or ‘#f’ if it
     has none.

 -- Scheme Procedure: record-type-uid rtd
     Returns the uid of the record-type descriptor RTD, or ‘#f’ if it
     has none.

 -- Scheme Procedure: record-type-generative? rtd
     Returns ‘#t’ if the record-type descriptor RTD is generative, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-sealed? rtd
     Returns ‘#t’ if the record-type descriptor RTD is sealed, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-opaque? rtd
     Returns ‘#t’ if the record-type descriptor RTD is opaque, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-field-names rtd
     Returns a vector of symbols giving the names of the fields defined
     by the record-type descriptor RTD (and not any of its sub- or
     supertypes).

 -- Scheme Procedure: record-field-mutable? rtd k
     Returns ‘#t’ if the field at index K of the record-type descriptor
     RTD (and not any of its sub- or supertypes) is mutable.

7.6.2.12 rnrs exceptions
........................

The ‘(rnrs exceptions (6))’ library provides functionality related to
signaling and handling exceptional situations.  This functionality is
similar to the exception handling systems provided by Guile’s core
library *Note Exceptions::, and by the SRFI-18 and SRFI-34 modules—*Note
SRFI-18 Exceptions::, and *note SRFI-34::, respectively—but there are
some key differences in concepts and behavior.

   A raised exception may be "continuable" or "non-continuable".  When
an exception is raised non-continuably, another exception, with the
condition type ‘&non-continuable’, will be raised when the exception
handler returns locally.  Raising an exception continuably captures the
current continuation and invokes it after a local return from the
exception handler.

   Like SRFI-18 and SRFI-34, R6RS exceptions are implemented on top of
Guile’s native ‘throw’ and ‘catch’ forms, and use custom “throw keys” to
identify their exception types.  As a consequence, Guile’s ‘catch’ form
can handle exceptions thrown by these APIs, but the reverse is not true:
Handlers registered by the ‘with-exception-handler’ procedure described
below will only be called on exceptions thrown by the corresponding
‘raise’ procedure.

 -- Scheme Procedure: with-exception-handler handler thunk
     Installs HANDLER, which must be a procedure taking one argument, as
     the current exception handler during the invocation of THUNK, a
     procedure taking zero arguments.  The handler in place at the time
     ‘with-exception-handler’ is called is made current again once
     either THUNK returns or HANDLER is invoked after an exception is
     thrown from within THUNK.

     This procedure is similar to the ‘with-throw-handler’ procedure
     provided by Guile’s code library; (*note Throw Handlers::).

 -- Scheme Syntax: guard (variable clause1 clause2 ...) body
     Evaluates the expression given by BODY, first creating an ad hoc
     exception handler that binds a raised exception to VARIABLE and
     then evaluates the specified CLAUSEs as if they were part of a
     ‘cond’ expression, with the value of the first matching clause
     becoming the value of the ‘guard’ expression (*note
     Conditionals::).  If none of the clause’s test expressions
     evaluates to ‘#t’, the exception is re-raised, with the exception
     handler that was current before the evaluation of the ‘guard’ form.

     For example, the expression

          (guard (ex ((eq? ex 'foo) 'bar) ((eq? ex 'bar) 'baz))
            (raise 'bar))

     evaluates to ‘baz’.

 -- Scheme Procedure: raise obj
     Raises a non-continuable exception by invoking the
     currently-installed exception handler on OBJ.  If the handler
     returns, a ‘&non-continuable’ exception will be raised in the
     dynamic context in which the handler was installed.

 -- Scheme Procedure: raise-continuable obj
     Raises a continuable exception by invoking currently-installed
     exception handler on OBJ.

7.6.2.13 rnrs conditions
........................

The ‘(rnrs condition (6))’ library provides forms and procedures for
constructing new condition types, as well as a library of pre-defined
condition types that represent a variety of common exceptional
situations.  Conditions are records of a subtype of the ‘&condition’
record type, which is neither sealed nor opaque.  *Note R6RS Records::.

   Conditions may be manipulated singly, as "simple conditions", or when
composed with other conditions to form "compound conditions".  Compound
conditions do not “nest”—constructing a new compound condition out of
existing compound conditions will “flatten” them into their component
simple conditions.  For example, making a new condition out of a
‘&message’ condition and a compound condition that contains an
‘&assertion’ condition and another ‘&message’ condition will produce a
compound condition that contains two ‘&message’ conditions and one
‘&assertion’ condition.

   The record type predicates and field accessors described below can
operate on either simple or compound conditions.  In the latter case,
the predicate returns ‘#t’ if the compound condition contains a
component simple condition of the appropriate type; the field accessors
return the requisite fields from the first component simple condition
found to be of the appropriate type.

   This library is quite similar to the SRFI-35 conditions module (*note
SRFI-35::).  Among other minor differences, the ‘(rnrs conditions)’
library features slightly different semantics around condition field
accessors, and comes with a larger number of pre-defined condition
types.  The two APIs are not currently compatible, however; the
‘condition?’ predicate from one API will return ‘#f’ when applied to a
condition object created in the other.

 -- Condition Type: &condition
 -- Scheme Procedure: condition? obj
     The base record type for conditions.

 -- Scheme Procedure: condition condition1 ...
 -- Scheme Procedure: simple-conditions condition
     The ‘condition’ procedure creates a new compound condition out of
     its condition arguments, flattening any specified compound
     conditions into their component simple conditions as described
     above.

     ‘simple-conditions’ returns a list of the component simple
     conditions of the compound condition ‘condition’, in the order in
     which they were specified at construction time.

 -- Scheme Procedure: condition-predicate rtd
 -- Scheme Procedure: condition-accessor rtd proc
     These procedures return condition predicate and accessor procedures
     for the specified condition record type RTD.

 -- Scheme Syntax: define-condition-type condition-type supertype
          constructor predicate field-spec ...
     Evaluates to a new record type definition for a condition type with
     the name CONDITION-TYPE that has the condition type SUPERTYPE as
     its parent.  A default constructor, which binds its arguments to
     the fields of this type and its parent types, will be bound to the
     identifier CONSTRUCTOR; a condition predicate will be bound to
     PREDICATE.  The fields of the new type, which are immutable, are
     specified by the FIELD-SPECs, each of which must be of the form:
          (field accessor)
     where FIELD gives the name of the field and ACCESSOR gives the name
     for a binding to an accessor procedure created for this field.

 -- Condition Type: &message
 -- Scheme Procedure: make-message-condition message
 -- Scheme Procedure: message-condition? obj
 -- Scheme Procedure: condition-message condition
     A type that includes a message describing the condition that
     occurred.

 -- Condition Type: &warning
 -- Scheme Procedure: make-warning
 -- Scheme Procedure: warning? obj
     A base type for representing non-fatal conditions during execution.

 -- Condition Type: &serious
 -- Scheme Procedure: make-serious-condition
 -- Scheme Procedure: serious-condition? obj
     A base type for conditions representing errors serious enough that
     cannot be ignored.

 -- Condition Type: &error
 -- Scheme Procedure: make-error
 -- Scheme Procedure: error? obj
     A base type for conditions representing errors.

 -- Condition Type: &violation
 -- Scheme Procedure: make-violation
 -- Scheme Procedure: violation?
     A subtype of ‘&serious’ that can be used to represent violations of
     a language or library standard.

 -- Condition Type: &assertion
 -- Scheme Procedure: make-assertion-violation
 -- Scheme Procedure: assertion-violation? obj
     A subtype of ‘&violation’ that indicates an invalid call to a
     procedure.

 -- Condition Type: &irritants
 -- Scheme Procedure: make-irritants-condition irritants
 -- Scheme Procedure: irritants-condition? obj
 -- Scheme Procedure: condition-irritants condition
     A base type used for storing information about the causes of
     another condition in a compound condition.

 -- Condition Type: &who
 -- Scheme Procedure: make-who-condition who
 -- Scheme Procedure: who-condition? obj
 -- Scheme Procedure: condition-who condition
     A base type used for storing the identity, a string or symbol, of
     the entity responsible for another condition in a compound
     condition.

 -- Condition Type: &non-continuable
 -- Scheme Procedure: make-non-continuable-violation
 -- Scheme Procedure: non-continuable-violation? obj
     A subtype of ‘&violation’ used to indicate that an exception
     handler invoked by ‘raise’ has returned locally.

 -- Condition Type: &implementation-restriction
 -- Scheme Procedure: make-implementation-restriction-violation
 -- Scheme Procedure: implementation-restriction-violation? obj
     A subtype of ‘&violation’ used to indicate a violation of an
     implementation restriction.

 -- Condition Type: &lexical
 -- Scheme Procedure: make-lexical-violation
 -- Scheme Procedure: lexical-violation? obj
     A subtype of ‘&violation’ used to indicate a syntax violation at
     the level of the datum syntax.

 -- Condition Type: &syntax
 -- Scheme Procedure: make-syntax-violation form subform
 -- Scheme Procedure: syntax-violation? obj
 -- Scheme Procedure: syntax-violation-form condition
 -- Scheme Procedure: syntax-violation-subform condition
     A subtype of ‘&violation’ that indicates a syntax violation.  The
     FORM and SUBFORM fields, which must be datum values, indicate the
     syntactic form responsible for the condition.

 -- Condition Type: &undefined
 -- Scheme Procedure: make-undefined-violation
 -- Scheme Procedure: undefined-violation? obj
     A subtype of ‘&violation’ that indicates a reference to an unbound
     identifier.

7.6.2.14 I/O Conditions
.......................

These condition types are exported by both the ‘(rnrs io ports (6))’ and
‘(rnrs io simple (6))’ libraries.

 -- Condition Type: &i/o
 -- Scheme Procedure: make-i/o-error
 -- Scheme Procedure: i/o-error? obj
     A condition supertype for more specific I/O errors.

 -- Condition Type: &i/o-read
 -- Scheme Procedure: make-i/o-read-error
 -- Scheme Procedure: i/o-read-error? obj
     A subtype of ‘&i/o’; represents read-related I/O errors.

 -- Condition Type: &i/o-write
 -- Scheme Procedure: make-i/o-write-error
 -- Scheme Procedure: i/o-write-error? obj
     A subtype of ‘&i/o’; represents write-related I/O errors.

 -- Condition Type: &i/o-invalid-position
 -- Scheme Procedure: make-i/o-invalid-position-error position
 -- Scheme Procedure: i/o-invalid-position-error? obj
 -- Scheme Procedure: i/o-error-position condition
     A subtype of ‘&i/o’; represents an error related to an attempt to
     set the file position to an invalid position.

 -- Condition Type: &i/o-filename
 -- Scheme Procedure: make-io-filename-error filename
 -- Scheme Procedure: i/o-filename-error? obj
 -- Scheme Procedure: i/o-error-filename condition
     A subtype of ‘&i/o’; represents an error related to an operation on
     a named file.

 -- Condition Type: &i/o-file-protection
 -- Scheme Procedure: make-i/o-file-protection-error filename
 -- Scheme Procedure: i/o-file-protection-error? obj
     A subtype of ‘&i/o-filename’; represents an error resulting from an
     attempt to access a named file for which the caller had
     insufficient permissions.

 -- Condition Type: &i/o-file-is-read-only
 -- Scheme Procedure: make-i/o-file-is-read-only-error filename
 -- Scheme Procedure: i/o-file-is-read-only-error? obj
     A subtype of ‘&i/o-file-protection’; represents an error related to
     an attempt to write to a read-only file.

 -- Condition Type: &i/o-file-already-exists
 -- Scheme Procedure: make-i/o-file-already-exists-error filename
 -- Scheme Procedure: i/o-file-already-exists-error? obj
     A subtype of ‘&i/o-filename’; represents an error related to an
     operation on an existing file that was assumed not to exist.

 -- Condition Type: &i/o-file-does-not-exist
 -- Scheme Procedure: make-i/o-file-does-not-exist-error
 -- Scheme Procedure: i/o-file-does-not-exist-error? obj
     A subtype of ‘&i/o-filename’; represents an error related to an
     operation on a non-existent file that was assumed to exist.

 -- Condition Type: &i/o-port
 -- Scheme Procedure: make-i/o-port-error port
 -- Scheme Procedure: i/o-port-error? obj
 -- Scheme Procedure: i/o-error-port condition
     A subtype of ‘&i/o’; represents an error related to an operation on
     the port PORT.

7.6.2.15 rnrs io ports
......................

The ‘(rnrs io ports (6))’ library provides various procedures and
syntactic forms for use in writing to and reading from ports.  This
functionality is documented in its own section of the manual; (*note
R6RS I/O Ports::).

7.6.2.16 rnrs io simple
.......................

The ‘(rnrs io simple (6))’ library provides convenience functions for
performing textual I/O on ports.  This library also exports all of the
condition types and associated procedures described in (*note I/O
Conditions::).  In the context of this section, when stating that a
procedure behaves “identically” to the corresponding procedure in
Guile’s core library, this is modulo the behavior wrt.  conditions: such
procedures raise the appropriate R6RS conditions in case of error, but
otherwise behave identically.

     Note: There are still known issues regarding condition-correctness;
     some errors may still be thrown as native Guile exceptions instead
     of the appropriate R6RS conditions.

 -- Scheme Procedure: eof-object
 -- Scheme Procedure: eof-object? obj
     These procedures are identical to the ones provided by the ‘(rnrs
     io ports (6))’ library.  *Note R6RS I/O Ports::, for documentation.

 -- Scheme Procedure: input-port? obj
 -- Scheme Procedure: output-port? obj
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Ports::, for documentation.

 -- Scheme Procedure: call-with-input-file filename proc
 -- Scheme Procedure: call-with-output-file filename proc
 -- Scheme Procedure: open-input-file filename
 -- Scheme Procedure: open-output-file filename
 -- Scheme Procedure: with-input-from-file filename thunk
 -- Scheme Procedure: with-output-to-file filename thunk
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note File Ports::, for documentation.

 -- Scheme Procedure: close-input-port input-port
 -- Scheme Procedure: close-output-port output-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Closing::, for documentation.

 -- Scheme Procedure: peek-char
 -- Scheme Procedure: peek-char textual-input-port
 -- Scheme Procedure: read-char
 -- Scheme Procedure: read-char textual-input-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Reading::, for documentation.

 -- Scheme Procedure: read
 -- Scheme Procedure: read textual-input-port
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Scheme Read::, for documentation.

 -- Scheme Procedure: display obj
 -- Scheme Procedure: display obj textual-output-port
 -- Scheme Procedure: newline
 -- Scheme Procedure: newline textual-output-port
 -- Scheme Procedure: write obj
 -- Scheme Procedure: write obj textual-output-port
 -- Scheme Procedure: write-char char
 -- Scheme Procedure: write-char char textual-output-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Writing::, for documentation.

7.6.2.17 rnrs files
...................

The ‘(rnrs files (6))’ library provides the ‘file-exists?’ and
‘delete-file’ procedures, which test for the existence of a file and
allow the deletion of files from the file system, respectively.

   These procedures are identical to the ones provided by Guile’s core
library.  *Note File System::, for documentation.

7.6.2.18 rnrs programs
......................

The ‘(rnrs programs (6))’ library provides procedures for process
management and introspection.

 -- Scheme Procedure: command-line
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Runtime Environment::, for documentation.

 -- Scheme Procedure: exit [status]
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Processes::, for documentation.

7.6.2.19 rnrs arithmetic fixnums
................................

The ‘(rnrs arithmetic fixnums (6))’ library provides procedures for
performing arithmetic operations on an implementation-dependent range of
exact integer values, which R6RS refers to as "fixnums".  In Guile, the
size of a fixnum is determined by the size of the ‘SCM’ type; a single
SCM struct is guaranteed to be able to hold an entire fixnum, making
fixnum computations particularly efficient—(*note The SCM Type::).  On
32-bit systems, the most negative and most positive fixnum values are,
respectively, -536870912 and 536870911.

   Unless otherwise specified, all of the procedures below take fixnums
as arguments, and will raise an ‘&assertion’ condition if passed a
non-fixnum argument or an ‘&implementation-restriction’ condition if
their result is not itself a fixnum.

 -- Scheme Procedure: fixnum? obj
     Returns ‘#t’ if OBJ is a fixnum, ‘#f’ otherwise.

 -- Scheme Procedure: fixnum-width
 -- Scheme Procedure: least-fixnum
 -- Scheme Procedure: greatest-fixnum
     These procedures return, respectively, the maximum number of bits
     necessary to represent a fixnum value in Guile, the minimum fixnum
     value, and the maximum fixnum value.

 -- Scheme Procedure: fx=? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx>? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx<? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx>=? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx<=? fx1 fx2 fx3 ...
     These procedures return ‘#t’ if their fixnum arguments are
     (respectively): equal, monotonically increasing, monotonically
     decreasing, monotonically nondecreasing, or monotonically
     nonincreasing; ‘#f’ otherwise.

 -- Scheme Procedure: fxzero? fx
 -- Scheme Procedure: fxpositive? fx
 -- Scheme Procedure: fxnegative? fx
 -- Scheme Procedure: fxodd? fx
 -- Scheme Procedure: fxeven? fx
     These numerical predicates return ‘#t’ if FX is, respectively,
     zero, greater than zero, less than zero, odd, or even; ‘#f’
     otherwise.

 -- Scheme Procedure: fxmax fx1 fx2 ...
 -- Scheme Procedure: fxmin fx1 fx2 ...
     These procedures return the maximum or minimum of their arguments.

 -- Scheme Procedure: fx+ fx1 fx2
 -- Scheme Procedure: fx* fx1 fx2
     These procedures return the sum or product of their arguments.

 -- Scheme Procedure: fx- fx1 fx2
 -- Scheme Procedure: fx- fx
     Returns the difference of FX1 and FX2, or the negation of FX, if
     called with a single argument.

     An ‘&assertion’ condition is raised if the result is not itself a
     fixnum.

 -- Scheme Procedure: fxdiv-and-mod fx1 fx2
 -- Scheme Procedure: fxdiv fx1 fx2
 -- Scheme Procedure: fxmod fx1 fx2
 -- Scheme Procedure: fxdiv0-and-mod0 fx1 fx2
 -- Scheme Procedure: fxdiv0 fx1 fx2
 -- Scheme Procedure: fxmod0 fx1 fx2
     These procedures implement number-theoretic division on fixnums;
     *Note (rnrs base)::, for a description of their semantics.

 -- Scheme Procedure: fx+/carry fx1 fx2 fx3
     Returns the two fixnum results of the following computation:
          (let* ((s (+ fx1 fx2 fx3))
                 (s0 (mod0 s (expt 2 (fixnum-width))))
                 (s1 (div0 s (expt 2 (fixnum-width)))))
            (values s0 s1))

 -- Scheme Procedure: fx-/carry fx1 fx2 fx3
     Returns the two fixnum results of the following computation:
          (let* ((d (- fx1 fx2 fx3))
                 (d0 (mod0 d (expt 2 (fixnum-width))))
                 (d1 (div0 d (expt 2 (fixnum-width)))))
            (values d0 d1))

 -- Scheme Procedure: fx*/carry fx1 fx2 fx3
          Returns the two fixnum results of the following computation:
          (let* ((s (+ (* fx1 fx2) fx3))
                 (s0 (mod0 s (expt 2 (fixnum-width))))
                 (s1 (div0 s (expt 2 (fixnum-width)))))
            (values s0 s1))

 -- Scheme Procedure: fxnot fx
 -- Scheme Procedure: fxand fx1 ...
 -- Scheme Procedure: fxior fx1 ...
 -- Scheme Procedure: fxxor fx1 ...
     These procedures are identical to the ‘lognot’, ‘logand’, ‘logior’,
     and ‘logxor’ procedures provided by Guile’s core library.  *Note
     Bitwise Operations::, for documentation.

 -- Scheme Procedure: fxif fx1 fx2 fx3
     Returns the bitwise “if” of its fixnum arguments.  The bit at
     position ‘i’ in the return value will be the ‘i’th bit from FX2 if
     the ‘i’th bit of FX1 is 1, the ‘i’th bit from FX3.

 -- Scheme Procedure: fxbit-count fx
     Returns the number of 1 bits in the two’s complement representation
     of FX.

 -- Scheme Procedure: fxlength fx
     Returns the number of bits necessary to represent FX.

 -- Scheme Procedure: fxfirst-bit-set fx
     Returns the index of the least significant 1 bit in the two’s
     complement representation of FX.

 -- Scheme Procedure: fxbit-set? fx1 fx2
     Returns ‘#t’ if the FX2th bit in the two’s complement
     representation of FX1 is 1, ‘#f’ otherwise.

 -- Scheme Procedure: fxcopy-bit fx1 fx2 fx3
     Returns the result of setting the FX2th bit of FX1 to the FX2th bit
     of FX3.

 -- Scheme Procedure: fxbit-field fx1 fx2 fx3
     Returns the integer representation of the contiguous sequence of
     bits in FX1 that starts at position FX2 (inclusive) and ends at
     position FX3 (exclusive).

 -- Scheme Procedure: fxcopy-bit-field fx1 fx2 fx3 fx4
     Returns the result of replacing the bit field in FX1 with start and
     end positions FX2 and FX3 with the corresponding bit field from
     FX4.

 -- Scheme Procedure: fxarithmetic-shift fx1 fx2
 -- Scheme Procedure: fxarithmetic-shift-left fx1 fx2
 -- Scheme Procedure: fxarithmetic-shift-right fx1 fx2
     Returns the result of shifting the bits of FX1 right or left by the
     FX2 positions.  ‘fxarithmetic-shift’ is identical to
     ‘fxarithmetic-shift-left’.

 -- Scheme Procedure: fxrotate-bit-field fx1 fx2 fx3 fx4
     Returns the result of cyclically permuting the bit field in FX1
     with start and end positions FX2 and FX3 by FX4 bits in the
     direction of more significant bits.

 -- Scheme Procedure: fxreverse-bit-field fx1 fx2 fx3
     Returns the result of reversing the order of the bits of FX1
     between position FX2 (inclusive) and position FX3 (exclusive).

7.6.2.20 rnrs arithmetic flonums
................................

The ‘(rnrs arithmetic flonums (6))’ library provides procedures for
performing arithmetic operations on inexact representations of real
numbers, which R6RS refers to as "flonums".

   Unless otherwise specified, all of the procedures below take flonums
as arguments, and will raise an ‘&assertion’ condition if passed a
non-flonum argument.

 -- Scheme Procedure: flonum? obj
     Returns ‘#t’ if OBJ is a flonum, ‘#f’ otherwise.

 -- Scheme Procedure: real->flonum x
     Returns the flonum that is numerically closest to the real number
     X.

 -- Scheme Procedure: fl=? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl<? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl<=? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl>? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl>=? fl1 fl2 fl3 ...
     These procedures return ‘#t’ if their flonum arguments are
     (respectively): equal, monotonically increasing, monotonically
     decreasing, monotonically nondecreasing, or monotonically
     nonincreasing; ‘#f’ otherwise.

 -- Scheme Procedure: flinteger? fl
 -- Scheme Procedure: flzero? fl
 -- Scheme Procedure: flpositive? fl
 -- Scheme Procedure: flnegative? fl
 -- Scheme Procedure: flodd? fl
 -- Scheme Procedure: fleven? fl
     These numerical predicates return ‘#t’ if FL is, respectively, an
     integer, zero, greater than zero, less than zero, odd, even, ‘#f’
     otherwise.  In the case of ‘flodd?’ and ‘fleven?’, FL must be an
     integer-valued flonum.

 -- Scheme Procedure: flfinite? fl
 -- Scheme Procedure: flinfinite? fl
 -- Scheme Procedure: flnan? fl
     These numerical predicates return ‘#t’ if FL is, respectively, not
     infinite, infinite, or a ‘NaN’ value.

 -- Scheme Procedure: flmax fl1 fl2 ...
 -- Scheme Procedure: flmin fl1 fl2 ...
     These procedures return the maximum or minimum of their arguments.

 -- Scheme Procedure: fl+ fl1 ...
 -- Scheme Procedure: fl* fl ...
     These procedures return the sum or product of their arguments.

 -- Scheme Procedure: fl- fl1 fl2 ...
 -- Scheme Procedure: fl- fl
 -- Scheme Procedure: fl/ fl1 fl2 ...
 -- Scheme Procedure: fl/ fl
     These procedures return, respectively, the difference or quotient
     of their arguments when called with two arguments; when called with
     a single argument, they return the additive or multiplicative
     inverse of FL.

 -- Scheme Procedure: flabs fl
     Returns the absolute value of FL.

 -- Scheme Procedure: fldiv-and-mod fl1 fl2
 -- Scheme Procedure: fldiv fl1 fl2
 -- Scheme Procedure: fldmod fl1 fl2
 -- Scheme Procedure: fldiv0-and-mod0 fl1 fl2
 -- Scheme Procedure: fldiv0 fl1 fl2
 -- Scheme Procedure: flmod0 fl1 fl2
     These procedures implement number-theoretic division on flonums;
     *Note (rnrs base)::, for a description for their semantics.

 -- Scheme Procedure: flnumerator fl
 -- Scheme Procedure: fldenominator fl
     These procedures return the numerator or denominator of FL as a
     flonum.

 -- Scheme Procedure: flfloor fl1
 -- Scheme Procedure: flceiling fl
 -- Scheme Procedure: fltruncate fl
 -- Scheme Procedure: flround fl
     These procedures are identical to the ‘floor’, ‘ceiling’,
     ‘truncate’, and ‘round’ procedures provided by Guile’s core
     library.  *Note Arithmetic::, for documentation.

 -- Scheme Procedure: flexp fl
 -- Scheme Procedure: fllog fl
 -- Scheme Procedure: fllog fl1 fl2
 -- Scheme Procedure: flsin fl
 -- Scheme Procedure: flcos fl
 -- Scheme Procedure: fltan fl
 -- Scheme Procedure: flasin fl
 -- Scheme Procedure: flacos fl
 -- Scheme Procedure: flatan fl
 -- Scheme Procedure: flatan fl1 fl2
     These procedures, which compute the usual transcendental functions,
     are the flonum variants of the procedures provided by the R6RS base
     library (*note (rnrs base)::).

 -- Scheme Procedure: flsqrt fl
     Returns the square root of FL.  If FL is ‘-0.0’, -0.0 is returned;
     for other negative values, a ‘NaN’ value is returned.

 -- Scheme Procedure: flexpt fl1 fl2
     Returns the value of FL1 raised to the power of FL2.

   The following condition types are provided to allow Scheme
implementations that do not support infinities or ‘NaN’ values to
indicate that a computation resulted in such a value.  Guile supports
both of these, so these conditions will never be raised by Guile’s
standard libraries implementation.

 -- Condition Type: &no-infinities
 -- Scheme Procedure: make-no-infinities-violation obj
 -- Scheme Procedure: no-infinities-violation?
     A condition type indicating that a computation resulted in an
     infinite value on a Scheme implementation incapable of representing
     infinities.

 -- Condition Type: &no-nans
 -- Scheme Procedure: make-no-nans-violation obj
 -- Scheme Procedure: no-nans-violation? obj
     A condition type indicating that a computation resulted in a ‘NaN’
     value on a Scheme implementation incapable of representing ‘NaN’s.

 -- Scheme Procedure: fixnum->flonum fx
     Returns the flonum that is numerically closest to the fixnum FX.

7.6.2.21 rnrs arithmetic bitwise
................................

The ‘(rnrs arithmetic bitwise (6))’ library provides procedures for
performing bitwise arithmetic operations on the two’s complement
representations of fixnums.

   This library and the procedures it exports share functionality with
SRFI-60, which provides support for bitwise manipulation of integers
(*note SRFI-60::).

 -- Scheme Procedure: bitwise-not ei
 -- Scheme Procedure: bitwise-and ei1 ...
 -- Scheme Procedure: bitwise-ior ei1 ...
 -- Scheme Procedure: bitwise-xor ei1 ...
     These procedures are identical to the ‘lognot’, ‘logand’, ‘logior’,
     and ‘logxor’ procedures provided by Guile’s core library.  *Note
     Bitwise Operations::, for documentation.

 -- Scheme Procedure: bitwise-if ei1 ei2 ei3
     Returns the bitwise “if” of its arguments.  The bit at position ‘i’
     in the return value will be the ‘i’th bit from EI2 if the ‘i’th bit
     of EI1 is 1, the ‘i’th bit from EI3.

 -- Scheme Procedure: bitwise-bit-count ei
     Returns the number of 1 bits in the two’s complement representation
     of EI.

 -- Scheme Procedure: bitwise-length ei
     Returns the number of bits necessary to represent EI.

 -- Scheme Procedure: bitwise-first-bit-set ei
     Returns the index of the least significant 1 bit in the two’s
     complement representation of EI.

 -- Scheme Procedure: bitwise-bit-set? ei1 ei2
     Returns ‘#t’ if the EI2th bit in the two’s complement
     representation of EI1 is 1, ‘#f’ otherwise.

 -- Scheme Procedure: bitwise-copy-bit ei1 ei2 ei3
     Returns the result of setting the EI2th bit of EI1 to the EI2th bit
     of EI3.

 -- Scheme Procedure: bitwise-bit-field ei1 ei2 ei3
     Returns the integer representation of the contiguous sequence of
     bits in EI1 that starts at position EI2 (inclusive) and ends at
     position EI3 (exclusive).

 -- Scheme Procedure: bitwise-copy-bit-field ei1 ei2 ei3 ei4
     Returns the result of replacing the bit field in EI1 with start and
     end positions EI2 and EI3 with the corresponding bit field from
     EI4.

 -- Scheme Procedure: bitwise-arithmetic-shift ei1 ei2
 -- Scheme Procedure: bitwise-arithmetic-shift-left ei1 ei2
 -- Scheme Procedure: bitwise-arithmetic-shift-right ei1 ei2
     Returns the result of shifting the bits of EI1 right or left by the
     EI2 positions.  ‘bitwise-arithmetic-shift’ is identical to
     ‘bitwise-arithmetic-shift-left’.

 -- Scheme Procedure: bitwise-rotate-bit-field ei1 ei2 ei3 ei4
     Returns the result of cyclically permuting the bit field in EI1
     with start and end positions EI2 and EI3 by EI4 bits in the
     direction of more significant bits.

 -- Scheme Procedure: bitwise-reverse-bit-field ei1 ei2 ei3
     Returns the result of reversing the order of the bits of EI1
     between position EI2 (inclusive) and position EI3 (exclusive).

7.6.2.22 rnrs syntax-case
.........................

The ‘(rnrs syntax-case (6))’ library provides access to the
‘syntax-case’ system for writing hygienic macros.  With one exception,
all of the forms and procedures exported by this library are
“re-exports” of Guile’s native support for ‘syntax-case’; *Note Syntax
Case::, for documentation, examples, and rationale.

 -- Scheme Procedure: make-variable-transformer proc
     Creates a new variable transformer out of PROC, a procedure that
     takes a syntax object as input and returns a syntax object.  If an
     identifier to which the result of this procedure is bound appears
     on the left-hand side of a ‘set!’ expression, PROC will be called
     with a syntax object representing the entire ‘set!’ expression, and
     its return value will replace that ‘set!’ expression.

 -- Scheme Syntax: syntax-case expression (literal ...) clause ...
     The ‘syntax-case’ pattern matching form.

 -- Scheme Syntax: syntax template
 -- Scheme Syntax: quasisyntax template
 -- Scheme Syntax: unsyntax template
 -- Scheme Syntax: unsyntax-splicing template
     These forms allow references to be made in the body of a
     syntax-case output expression subform to datum and non-datum
     values.  They are identical to the forms provided by Guile’s core
     library; *Note Syntax Case::, for documentation.

 -- Scheme Procedure: identifier? obj
 -- Scheme Procedure: bound-identifier=? id1 id2
 -- Scheme Procedure: free-identifier=? id1 id2
     These predicate procedures operate on syntax objects representing
     Scheme identifiers.  ‘identifier?’ returns ‘#t’ if OBJ represents
     an identifier, ‘#f’ otherwise.  ‘bound-identifier=?’ returns ‘#t’
     if and only if a binding for ID1 would capture a reference to ID2
     in the transformer’s output, or vice-versa.  ‘free-identifier=?’
     returns ‘#t’ if and only ID1 and ID2 would refer to the same
     binding in the output of the transformer, independent of any
     bindings introduced by the transformer.

 -- Scheme Procedure: generate-temporaries l
     Returns a list, of the same length as L, which must be a list or a
     syntax object representing a list, of globally unique symbols.

 -- Scheme Procedure: syntax->datum syntax-object
 -- Scheme Procedure: datum->syntax template-id datum
     These procedures convert wrapped syntax objects to and from Scheme
     datum values.  The syntax object returned by ‘datum->syntax’ shares
     contextual information with the syntax object TEMPLATE-ID.

 -- Scheme Procedure: syntax-violation whom message form
 -- Scheme Procedure: syntax-violation whom message form subform
     Constructs a new compound condition that includes the following
     simple conditions:
        • If WHOM is not ‘#f’, a ‘&who’ condition with the WHOM as its
          field
        • A ‘&message’ condition with the specified MESSAGE
        • A ‘&syntax’ condition with the specified FORM and optional
          SUBFORM fields

7.6.2.23 rnrs hashtables
........................

The ‘(rnrs hashtables (6))’ library provides structures and procedures
for creating and accessing hash tables.  The hash tables API defined by
R6RS is substantially similar to both Guile’s native hash tables
implementation as well as the one provided by SRFI-69; *Note Hash
Tables::, and *note SRFI-69::, respectively.  Note that you can write
portable R6RS library code that manipulates SRFI-69 hash tables (by
importing the ‘(srfi :69)’ library); however, hash tables created by one
API cannot be used by another.

   Like SRFI-69 hash tables—and unlike Guile’s native ones—R6RS hash
tables associate hash and equality functions with a hash table at the
time of its creation.  Additionally, R6RS allows for the creation (via
‘hashtable-copy’; see below) of immutable hash tables.

 -- Scheme Procedure: make-eq-hashtable
 -- Scheme Procedure: make-eq-hashtable k
     Returns a new hash table that uses ‘eq?’ to compare keys and
     Guile’s ‘hashq’ procedure as a hash function.  If K is given, it
     specifies the initial capacity of the hash table.

 -- Scheme Procedure: make-eqv-hashtable
 -- Scheme Procedure: make-eqv-hashtable k
     Returns a new hash table that uses ‘eqv?’ to compare keys and
     Guile’s ‘hashv’ procedure as a hash function.  If K is given, it
     specifies the initial capacity of the hash table.

 -- Scheme Procedure: make-hashtable hash-function equiv
 -- Scheme Procedure: make-hashtable hash-function equiv k
     Returns a new hash table that uses EQUIV to compare keys and
     HASH-FUNCTION as a hash function.  EQUIV must be a procedure that
     accepts two arguments and returns a true value if they are
     equivalent, ‘#f’ otherwise; HASH-FUNCTION must be a procedure that
     accepts one argument and returns a non-negative integer.

     If K is given, it specifies the initial capacity of the hash table.

 -- Scheme Procedure: hashtable? obj
     Returns ‘#t’ if OBJ is an R6RS hash table, ‘#f’ otherwise.

 -- Scheme Procedure: hashtable-size hashtable
     Returns the number of keys currently in the hash table HASHTABLE.

 -- Scheme Procedure: hashtable-ref hashtable key default
     Returns the value associated with KEY in the hash table HASHTABLE,
     or DEFAULT if none is found.

 -- Scheme Procedure: hashtable-set! hashtable key obj
     Associates the key KEY with the value OBJ in the hash table
     HASHTABLE, and returns an unspecified value.  An ‘&assertion’
     condition is raised if HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-delete! hashtable key
     Removes any association found for the key KEY in the hash table
     HASHTABLE, and returns an unspecified value.  An ‘&assertion’
     condition is raised if HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-contains? hashtable key
     Returns ‘#t’ if the hash table HASHTABLE contains an association
     for the key KEY, ‘#f’ otherwise.

 -- Scheme Procedure: hashtable-update! hashtable key proc default
     Associates with KEY in the hash table HASHTABLE the result of
     calling PROC, which must be a procedure that takes one argument, on
     the value currently associated KEY in HASHTABLE—or on DEFAULT if no
     such association exists.  An ‘&assertion’ condition is raised if
     HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-copy hashtable
 -- Scheme Procedure: hashtable-copy hashtable mutable
     Returns a copy of the hash table HASHTABLE.  If the optional
     argument MUTABLE is provided and is a true value, the new hash
     table will be mutable.

 -- Scheme Procedure: hashtable-clear! hashtable
 -- Scheme Procedure: hashtable-clear! hashtable k
     Removes all of the associations from the hash table HASHTABLE.  The
     optional argument K, which specifies a new capacity for the hash
     table, is accepted by Guile’s ‘(rnrs hashtables)’ implementation,
     but is ignored.

 -- Scheme Procedure: hashtable-keys hashtable
     Returns a vector of the keys with associations in the hash table
     HASHTABLE, in an unspecified order.

 -- Scheme Procedure: hashtable-entries hashtable
     Return two values—a vector of the keys with associations in the
     hash table HASHTABLE, and a vector of the values to which these
     keys are mapped, in corresponding but unspecified order.

 -- Scheme Procedure: hashtable-equivalence-function hashtable
     Returns the equivalence predicated use by HASHTABLE.  This
     procedure returns ‘eq?’ and ‘eqv?’, respectively, for hash tables
     created by ‘make-eq-hashtable’ and ‘make-eqv-hashtable’.

 -- Scheme Procedure: hashtable-hash-function hashtable
     Returns the hash function used by HASHTABLE.  For hash tables
     created by ‘make-eq-hashtable’ or ‘make-eqv-hashtable’, ‘#f’ is
     returned.

 -- Scheme Procedure: hashtable-mutable? hashtable
     Returns ‘#t’ if HASHTABLE is mutable, ‘#f’ otherwise.

   A number of hash functions are provided for convenience:

 -- Scheme Procedure: equal-hash obj
     Returns an integer hash value for OBJ, based on its structure and
     current contents.  This hash function is suitable for use with
     ‘equal?’ as an equivalence function.

 -- Scheme Procedure: string-hash string
 -- Scheme Procedure: symbol-hash symbol
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Hash Table Reference::, for documentation.

 -- Scheme Procedure: string-ci-hash string
     Returns an integer hash value for STRING based on its contents,
     ignoring case.  This hash function is suitable for use with
     ‘string-ci=?’ as an equivalence function.

7.6.2.24 rnrs enums
...................

The ‘(rnrs enums (6))’ library provides structures and procedures for
working with enumerable sets of symbols.  Guile’s implementation defines
an "enum-set" record type that encapsulates a finite set of distinct
symbols, the "universe", and a subset of these symbols, which define the
enumeration set.

   The SRFI-1 list library provides a number of procedures for
performing set operations on lists; Guile’s ‘(rnrs enums)’
implementation makes use of several of them.  *Note SRFI-1 Set
Operations::, for more information.

 -- Scheme Procedure: make-enumeration symbol-list
     Returns a new enum-set whose universe and enumeration set are both
     equal to SYMBOL-LIST, a list of symbols.

 -- Scheme Procedure: enum-set-universe enum-set
     Returns an enum-set representing the universe of ENUM-SET, an
     enum-set.

 -- Scheme Procedure: enum-set-indexer enum-set
     Returns a procedure that takes a single argument and returns the
     zero-indexed position of that argument in the universe of ENUM-SET,
     or ‘#f’ if its argument is not a member of that universe.

 -- Scheme Procedure: enum-set-constructor enum-set
     Returns a procedure that takes a single argument, a list of symbols
     from the universe of ENUM-SET, an enum-set, and returns a new
     enum-set with the same universe that represents a subset containing
     the specified symbols.

 -- Scheme Procedure: enum-set->list enum-set
     Returns a list containing the symbols of the set represented by
     ENUM-SET, an enum-set, in the order that they appear in the
     universe of ENUM-SET.

 -- Scheme Procedure: enum-set-member? symbol enum-set
 -- Scheme Procedure: enum-set-subset? enum-set1 enum-set2
 -- Scheme Procedure: enum-set=? enum-set1 enum-set2
     These procedures test for membership of symbols and enum-sets in
     other enum-sets.  ‘enum-set-member?’ returns ‘#t’ if and only if
     SYMBOL is a member of the subset specified by ENUM-SET.
     ‘enum-set-subset?’ returns ‘#t’ if and only if the universe of
     ENUM-SET1 is a subset of the universe of ENUM-SET2 and every symbol
     in ENUM-SET1 is present in ENUM-SET2.  ‘enum-set=?’ returns ‘#t’ if
     and only if ENUM-SET1 is a subset, as per ‘enum-set-subset?’ of
     ENUM-SET2 and vice versa.

 -- Scheme Procedure: enum-set-union enum-set1 enum-set2
 -- Scheme Procedure: enum-set-intersection enum-set1 enum-set2
 -- Scheme Procedure: enum-set-difference enum-set1 enum-set2
     These procedures return, respectively, the union, intersection, and
     difference of their enum-set arguments.

 -- Scheme Procedure: enum-set-complement enum-set
     Returns ENUM-SET’s complement (an enum-set), with regard to its
     universe.

 -- Scheme Procedure: enum-set-projection enum-set1 enum-set2
     Returns the projection of the enum-set ENUM-SET1 onto the universe
     of the enum-set ENUM-SET2.

 -- Scheme Syntax: define-enumeration type-name (symbol ...)
          constructor-syntax
     Evaluates to two new definitions: A constructor bound to
     CONSTRUCTOR-SYNTAX that behaves similarly to constructors created
     by ‘enum-set-constructor’, above, and creates new ENUM-SETs in the
     universe specified by ‘(symbol ...)’; and a “predicate macro” bound
     to TYPE-NAME, which has the following form:

          (TYPE-NAME sym)

     If SYM is a member of the universe specified by the SYMBOLs above,
     this form evaluates to SYM.  Otherwise, a ‘&syntax’ condition is
     raised.

7.6.2.25 rnrs
.............

The ‘(rnrs (6))’ library is a composite of all of the other R6RS
standard libraries—it imports and re-exports all of their exported
procedures and syntactic forms—with the exception of the following
libraries:

   • ‘(rnrs eval (6))’
   • ‘(rnrs mutable-pairs (6))’
   • ‘(rnrs mutable-strings (6))’
   • ‘(rnrs r5rs (6))’

7.6.2.26 rnrs eval
..................

The ‘(rnrs eval (6)’ library provides procedures for performing
“on-the-fly” evaluation of expressions.

 -- Scheme Procedure: eval expression environment
     Evaluates EXPRESSION, which must be a datum representation of a
     valid Scheme expression, in the environment specified by
     ENVIRONMENT.  This procedure is identical to the one provided by
     Guile’s code library; *Note Fly Evaluation::, for documentation.

 -- Scheme Procedure: environment import-spec ...
     Constructs and returns a new environment based on the specified
     IMPORT-SPECs, which must be datum representations of the import
     specifications used with the ‘import’ form.  *Note R6RS
     Libraries::, for documentation.

7.6.2.27 rnrs mutable-pairs
...........................

The ‘(rnrs mutable-pairs (6))’ library provides the ‘set-car!’ and
‘set-cdr!’ procedures, which allow the ‘car’ and ‘cdr’ fields of a pair
to be modified.

   These procedures are identical to the ones provide by Guile’s core
library.  *Note Pairs::, for documentation.  All pairs in Guile are
mutable; consequently, these procedures will never throw the
‘&assertion’ condition described in the R6RS libraries specification.

7.6.2.28 rnrs mutable-strings
.............................

The ‘(rnrs mutable-strings (6))’ library provides the ‘string-set!’ and
‘string-fill!’ procedures, which allow the content of strings to be
modified “in-place.”

   These procedures are identical to the ones provided by Guile’s core
library.  *Note String Modification::, for documentation.  All strings
in Guile are mutable; consequently, these procedures will never throw
the ‘&assertion’ condition described in the R6RS libraries
specification.

7.6.2.29 rnrs r5rs
..................

The ‘(rnrs r5rs (6))’ library exports bindings for some procedures
present in R5RS but omitted from the R6RS base library specification.

 -- Scheme Procedure: exact->inexact z
 -- Scheme Procedure: inexact->exact z
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Exactness::, for documentation.

 -- Scheme Procedure: quotient n1 n2
 -- Scheme Procedure: remainder n1 n2
 -- Scheme Procedure: modulo n1 n2
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Integer Operations::, for documentation.

 -- Scheme Syntax: delay expr
 -- Scheme Procedure: force promise
     The ‘delay’ form and the ‘force’ procedure are identical to their
     counterparts in Guile’s core library.  *Note Delayed Evaluation::,
     for documentation.

 -- Scheme Procedure: null-environment n
 -- Scheme Procedure: scheme-report-environment n
     These procedures are identical to the ones provided by the ‘(ice-9
     r5rs)’ Guile module.  *Note Environments::, for documentation.

