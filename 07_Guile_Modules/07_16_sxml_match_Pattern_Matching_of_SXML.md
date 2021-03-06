7.16 ‘sxml-match’: Pattern Matching of SXML
===========================================

The ‘(sxml match)’ module provides syntactic forms for pattern matching
of SXML trees, in a “by example” style reminiscent of the pattern
matching of the ‘syntax-rules’ and ‘syntax-case’ macro systems.  *Note
SXML::, for more information on SXML.

   The following example(1) provides a brief illustration, transforming
a music album catalog language into HTML.

     (define (album->html x)
       (sxml-match x
         [(album (@ (title ,t)) (catalog (num ,n) (fmt ,f)) ...)
          `(ul (li ,t)
               (li (b ,n) (i ,f)) ...)]))

   Three macros are provided: ‘sxml-match’, ‘sxml-match-let’, and
‘sxml-match-let*’.

   Compared to a standard s-expression pattern matcher (*note Pattern
Matching::), ‘sxml-match’ provides the following benefits:

   • matching of SXML elements does not depend on any degree of
     normalization of the SXML;
   • matching of SXML attributes (within an element) is under-ordered;
     the order of the attributes specified within the pattern need not
     match the ordering with the element being matched;
   • all attributes specified in the pattern must be present in the
     element being matched; in the spirit that XML is ’extensible’, the
     element being matched may include additional attributes not
     specified in the pattern.

   The present module is a descendant of WebIt!, and was inspired by an
s-expression pattern matcher developed by Erik Hilsdale, Dan Friedman,
and Kent Dybvig at Indiana University.

Syntax
------

‘sxml-match’ provides ‘case’-like form for pattern matching of XML
nodes.

 -- Scheme Syntax: sxml-match input-expression clause1 clause2 …
     Match INPUT-EXPRESSION, an SXML tree, according to the given
     CLAUSEs (one or more), each consisting of a pattern and one or more
     expressions to be evaluated if the pattern match succeeds.
     Optionally, each CLAUSE within ‘sxml-match’ may include a "guard
     expression".

   The pattern notation is based on that of Scheme’s ‘syntax-rules’ and
‘syntax-case’ macro systems.  The grammar for the ‘sxml-match’ syntax is
given below:

match-form ::= (sxml-match input-expression
                 clause+)

clause ::= [node-pattern action-expression+]
         | [node-pattern (guard expression*) action-expression+]

node-pattern ::= literal-pattern
               | pat-var-or-cata
               | element-pattern
               | list-pattern

literal-pattern ::= string
                  | character
                  | number
                  | #t
                  | #f

attr-list-pattern ::= (@ attribute-pattern*)
                    | (@ attribute-pattern* . pat-var-or-cata)

attribute-pattern ::= (tag-symbol attr-val-pattern)

attr-val-pattern ::= literal-pattern
                   | pat-var-or-cata
                   | (pat-var-or-cata default-value-expr)

element-pattern ::= (tag-symbol attr-list-pattern?)
                  | (tag-symbol attr-list-pattern? nodeset-pattern)
                  | (tag-symbol attr-list-pattern?
                                nodeset-pattern? . pat-var-or-cata)

list-pattern ::= (list nodeset-pattern)
               | (list nodeset-pattern? . pat-var-or-cata)
               | (list)

nodeset-pattern ::= node-pattern
                  | node-pattern ...
                  | node-pattern nodeset-pattern
                  | node-pattern ... nodeset-pattern

pat-var-or-cata ::= (unquote var-symbol)
                  | (unquote [var-symbol*])
                  | (unquote [cata-expression -> var-symbol*])

   Within a list or element body pattern, ellipses may appear only once,
but may be followed by zero or more node patterns.

   Guard expressions cannot refer to the return values of catamorphisms.

   Ellipses in the output expressions must appear only in an expression
context; ellipses are not allowed in a syntactic form.

   The sections below illustrate specific aspects of the ‘sxml-match’
pattern matcher.

Matching XML Elements
---------------------

The example below illustrates the pattern matching of an XML element:

     (sxml-match '(e (@ (i 1)) 3 4 5)
       [(e (@ (i ,d)) ,a ,b ,c) (list d a b c)]
       [,otherwise #f])

   Each clause in ‘sxml-match’ contains two parts: a pattern and one or
more expressions which are evaluated if the pattern is successfully
match.  The example above matches an element ‘e’ with an attribute ‘i’
and three children.

   Pattern variables are must be “unquoted” in the pattern.  The above
expression binds D to ‘1’, A to ‘3’, B to ‘4’, and C to ‘5’.

Ellipses in Patterns
--------------------

As in ‘syntax-rules’, ellipses may be used to specify a repeated
pattern.  Note that the pattern ‘item ...’ specifies zero-or-more
matches of the pattern ‘item’.

   The use of ellipses in a pattern is illustrated in the code fragment
below, where nested ellipses are used to match the children of repeated
instances of an ‘a’ element, within an element ‘d’.

     (define x '(d (a 1 2 3) (a 4 5) (a 6 7 8) (a 9 10)))

     (sxml-match x
       [(d (a ,b ...) ...)
        (list (list b ...) ...)])

   The above expression returns a value of ‘((1 2 3) (4 5) (6 7 8) (9
10))’.

Ellipses in Quasiquote’d Output
-------------------------------

Within the body of an ‘sxml-match’ form, a slightly extended version of
quasiquote is provided, which allows the use of ellipses.  This is
illustrated in the example below.

     (sxml-match '(e 3 4 5 6 7)
       [(e ,i ... 6 7) `("start" ,(list 'wrap i) ... "end")]
       [,otherwise #f])

   The general pattern is that ‘`(something ,i ...)’ is rewritten as
‘`(something ,@i)’.

Matching Nodesets
-----------------

A nodeset pattern is designated by a list in the pattern, beginning the
identifier list.  The example below illustrates matching a nodeset.

     (sxml-match '("i" "j" "k" "l" "m")
       [(list ,a ,b ,c ,d ,e)
        `((p ,a) (p ,b) (p ,c) (p ,d) (p ,e))])

   This example wraps each nodeset item in an HTML paragraph element.
This example can be rewritten and simplified through using ellipsis:

     (sxml-match '("i" "j" "k" "l" "m")
       [(list ,i ...)
        `((p ,i) ...)])

   This version will match nodesets of any length, and wrap each item in
the nodeset in an HTML paragraph element.

Matching the “Rest” of a Nodeset
--------------------------------

Matching the “rest” of a nodeset is achieved by using a ‘. rest)’
pattern at the end of an element or nodeset pattern.

   This is illustrated in the example below:

     (sxml-match '(e 3 (f 4 5 6) 7)
       [(e ,a (f . ,y) ,d)
        (list a y d)])

   The above expression returns ‘(3 (4 5 6) 7)’.

Matching the Unmatched Attributes
---------------------------------

Sometimes it is useful to bind a list of attributes present in the
element being matched, but which do not appear in the pattern.  This is
achieved by using a ‘. rest)’ pattern at the end of the attribute list
pattern.  This is illustrated in the example below:

     (sxml-match '(a (@ (z 1) (y 2) (x 3)) 4 5 6)
       [(a (@ (y ,www) . ,qqq) ,t ,u ,v)
        (list www qqq t u v)])

   The above expression matches the attribute ‘y’ and binds a list of
the remaining attributes to the variable QQQ.  The result of the above
expression is ‘(2 ((z 1) (x 3)) 4 5 6)’.

   This type of pattern also allows the binding of all attributes:

     (sxml-match '(a (@ (z 1) (y 2) (x 3)))
       [(a (@ . ,qqq))
        qqq])

Default Values in Attribute Patterns
------------------------------------

It is possible to specify a default value for an attribute which is used
if the attribute is not present in the element being matched.  This is
illustrated in the following example:

     (sxml-match '(e 3 4 5)
       [(e (@ (z (,d 1))) ,a ,b ,c) (list d a b c)])

   The value ‘1’ is used when the attribute ‘z’ is absent from the
element ‘e’.

Guards in Patterns
------------------

Guards may be added to a pattern clause via the ‘guard’ keyword.  A
guard expression may include zero or more expressions which are
evaluated only if the pattern is matched.  The body of the clause is
only evaluated if the guard expressions evaluate to ‘#t’.

   The use of guard expressions is illustrated below:

     (sxml-match '(a 2 3)
       ((a ,n) (guard (number? n)) n)
       ((a ,m ,n) (guard (number? m) (number? n)) (+ m n)))

Catamorphisms
-------------

The example below illustrates the use of explicit recursion within an
‘sxml-match’ form.  This example implements a simple calculator for the
basic arithmetic operations, which are represented by the XML elements
‘plus’, ‘minus’, ‘times’, and ‘div’.

     (define simple-eval
       (lambda (x)
         (sxml-match x
           [,i (guard (integer? i)) i]
           [(plus ,x ,y) (+ (simple-eval x) (simple-eval y))]
           [(times ,x ,y) (* (simple-eval x) (simple-eval y))]
           [(minus ,x ,y) (- (simple-eval x) (simple-eval y))]
           [(div ,x ,y) (/ (simple-eval x) (simple-eval y))]
           [,otherwise (error "simple-eval: invalid expression" x)])))

   Using the catamorphism feature of ‘sxml-match’, a more concise
version of ‘simple-eval’ can be written.  The pattern ‘,[x]’ recursively
invokes the pattern matcher on the value bound in this position.

     (define simple-eval
       (lambda (x)
         (sxml-match x
           [,i (guard (integer? i)) i]
           [(plus ,[x] ,[y]) (+ x y)]
           [(times ,[x] ,[y]) (* x y)]
           [(minus ,[x] ,[y]) (- x y)]
           [(div ,[x] ,[y]) (/ x y)]
           [,otherwise (error "simple-eval: invalid expression" x)])))

Named-Catamorphisms
-------------------

It is also possible to explicitly name the operator in the “cata”
position.  Where ‘,[id*]’ recurs to the top of the current ‘sxml-match’,
‘,[cata -> id*]’ recurs to ‘cata’.  ‘cata’ must evaluate to a procedure
which takes one argument, and returns as many values as there are
identifiers following ‘->’.

   Named catamorphism patterns allow processing to be split into
multiple, mutually recursive procedures.  This is illustrated in the
example below: a transformation that formats a “TV Guide” into HTML.

     (define (tv-guide->html g)
       (define (cast-list cl)
         (sxml-match cl
           [(CastList (CastMember (Character (Name ,ch)) (Actor (Name ,a))) ...)
            `(div (ul (li ,ch ": " ,a) ...))]))
       (define (prog p)
         (sxml-match p
           [(Program (Start ,start-time) (Duration ,dur) (Series ,series-title)
                     (Description ,desc ...))
            `(div (p ,start-time
                     (br) ,series-title
                     (br) ,desc ...))]
           [(Program (Start ,start-time) (Duration ,dur) (Series ,series-title)
                     (Description ,desc ...)
                     ,[cast-list -> cl])
            `(div (p ,start-time
                     (br) ,series-title
                     (br) ,desc ...)
                  ,cl)]))
       (sxml-match g
         [(TVGuide (@ (start ,start-date)
                      (end ,end-date))
                   (Channel (Name ,nm) ,[prog -> p] ...) ...)
          `(html (head (title "TV Guide"))
                 (body (h1 "TV Guide")
                       (div (h2 ,nm) ,p ...) ...))]))

‘sxml-match-let’ and ‘sxml-match-let*’
--------------------------------------

 -- Scheme Syntax: sxml-match-let ((pat expr) ...) expression0
          expression ...
 -- Scheme Syntax: sxml-match-let* ((pat expr) ...) expression0
          expression ...
     These forms generalize the ‘let’ and ‘let*’ forms of Scheme to
     allow an XML pattern in the binding position, rather than a simple
     variable.

   For example, the expression below:

     (sxml-match-let ([(a ,i ,j) '(a 1 2)])
       (+ i j))

   binds the variables I and J to ‘1’ and ‘2’ in the XML value given.

   ---------- Footnotes ----------

   (1) This example is taken from a paper by Krishnamurthi et al.  Their
paper was the first to show the usefulness of the ‘syntax-rules’ style
of pattern matching for transformation of XML, though the language
described, XT3D, is an XML language.

