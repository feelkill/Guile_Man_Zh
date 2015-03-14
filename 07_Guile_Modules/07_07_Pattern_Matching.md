7.7 Pattern Matching
====================

The ‘(ice-9 match)’ module provides a "pattern matcher", written by Alex
Shinn, and compatible with Andrew K. Wright’s pattern matcher found in
many Scheme implementations.

   A pattern matcher can match an object against several patterns and
extract the elements that make it up.  Patterns can represent any Scheme
object: lists, strings, symbols, records, etc.  They can optionally
contain "pattern variables".  When a matching pattern is found, an
expression associated with the pattern is evaluated, optionally with all
pattern variables bound to the corresponding elements of the object:

     (let ((l '(hello (world))))
       (match l           ;; <- the input object
         (('hello (who))  ;; <- the pattern
          who)))          ;; <- the expression evaluated upon matching
     ⇒ world

   In this example, list L matches the pattern ‘('hello (who))’, because
it is a two-element list whose first element is the symbol ‘hello’ and
whose second element is a one-element list.  Here WHO is a pattern
variable.  ‘match’, the pattern matcher, locally binds WHO to the value
contained in this one-element list—i.e., the symbol ‘world’.  An error
would be raised if L did not match the pattern.

   The same object can be matched against a simpler pattern:

     (let ((l '(hello (world))))
       (match l
         ((x y)
          (values x y))))
     ⇒ hello
     ⇒ (world)

   Here pattern ‘(x y)’ matches any two-element list, regardless of the
types of these elements.  Pattern variables X and Y are bound to,
respectively, the first and second element of L.

   Patterns can be composed, and nested.  For instance, ‘...’ (ellipsis)
means that the previous pattern may be matched zero or more times in a
list:

     (match lst
       (((heads tails ...) ...)
        heads))

This expression returns the first element of each list within LST.  For
proper lists of proper lists, it is equivalent to ‘(map car lst)’.
However, it performs additional checks to make sure that LST and the
lists therein are proper lists, as prescribed by the pattern, raising an
error if they are not.

   Compared to hand-written code, pattern matching noticeably improves
clarity and conciseness—no need to resort to series of ‘car’ and ‘cdr’
calls when matching lists, for instance.  It also improves robustness,
by making sure the input _completely_ matches the pattern—conversely,
hand-written code often trades robustness for conciseness.  And of
course, ‘match’ is a macro, and the code it expands to is just as
efficient as equivalent hand-written code.

   The pattern matcher is defined as follows:

 -- Scheme Syntax: match exp clause1 clause2 …
     Match object EXP against the patterns in CLAUSE1 CLAUSE2 … in the
     order in which they appear.  Return the value produced by the first
     matching clause.  If no clause matches, throw an exception with key
     ‘match-error’.

     Each clause has the form ‘(pattern body1 body2 …)’.  Each PATTERN
     must follow the syntax described below.  Each body is an arbitrary
     Scheme expression, possibly referring to pattern variables of
     PATTERN.

   The syntax and interpretation of patterns is as follows:

        patterns:                       matches:

pat ::= identifier                      anything, and binds identifier
      | _                               anything
      | ()                              the empty list
      | #t                              #t
      | #f                              #f
      | string                          a string
      | number                          a number
      | character                       a character
      | 'sexp                           an s-expression
      | 'symbol                         a symbol (special case of s-expr)
      | (pat_1 ... pat_n)               list of n elements
      | (pat_1 ... pat_n . pat_{n+1})   list of n or more
      | (pat_1 ... pat_n pat_n+1 ooo)   list of n or more, each element
                                          of remainder must match pat_n+1
      | #(pat_1 ... pat_n)              vector of n elements
      | #(pat_1 ... pat_n pat_n+1 ooo)  vector of n or more, each element
                                          of remainder must match pat_n+1
      | #&pat                           box
      | ($ record-name pat_1 ... pat_n) a record
      | (= field pat)                   a ``field'' of an object
      | (and pat_1 ... pat_n)           if all of pat_1 thru pat_n match
      | (or pat_1 ... pat_n)            if any of pat_1 thru pat_n match
      | (not pat_1 ... pat_n)           if all pat_1 thru pat_n don't match
      | (? predicate pat_1 ... pat_n)   if predicate true and all of
                                          pat_1 thru pat_n match
      | (set! identifier)               anything, and binds setter
      | (get! identifier)               anything, and binds getter
      | `qp                             a quasi-pattern
      | (identifier *** pat)            matches pat in a tree and binds
                                        identifier to the path leading
                                        to the object that matches pat

ooo ::= ...                             zero or more
      | ___                             zero or more
      | ..1                             1 or more

        quasi-patterns:                 matches:

qp  ::= ()                              the empty list
      | #t                              #t
      | #f                              #f
      | string                          a string
      | number                          a number
      | character                       a character
      | identifier                      a symbol
      | (qp_1 ... qp_n)                 list of n elements
      | (qp_1 ... qp_n . qp_{n+1})      list of n or more
      | (qp_1 ... qp_n qp_n+1 ooo)      list of n or more, each element
                                          of remainder must match qp_n+1
      | #(qp_1 ... qp_n)                vector of n elements
      | #(qp_1 ... qp_n qp_n+1 ooo)     vector of n or more, each element
                                          of remainder must match qp_n+1
      | #&qp                            box
      | ,pat                            a pattern
      | ,@pat                           a pattern

   The names ‘quote’, ‘quasiquote’, ‘unquote’, ‘unquote-splicing’, ‘?’,
‘_’, ‘$’, ‘and’, ‘or’, ‘not’, ‘set!’, ‘get!’, ‘...’, and ‘___’ cannot be
used as pattern variables.

   Here is a more complex example:

     (use-modules (srfi srfi-9))

     (let ()
       (define-record-type person
         (make-person name friends)
         person?
         (name    person-name)
         (friends person-friends))

       (letrec ((alice (make-person "Alice" (delay (list bob))))
                (bob   (make-person "Bob" (delay (list alice)))))
         (match alice
           (($ person name (= force (($ person "Bob"))))
            (list 'friend-of-bob name))
           (_ #f))))

     ⇒ (friend-of-bob "Alice")

Here the ‘$’ pattern is used to match a SRFI-9 record of type PERSON
containing two or more slots.  The value of the first slot is bound to
NAME.  The ‘=’ pattern is used to apply ‘force’ on the second slot, and
then checking that the result matches the given pattern.  In other
words, the complete pattern matches any PERSON whose second slot is a
promise that evaluates to a one-element list containing a PERSON whose
first slot is ‘"Bob"’.

   Please refer to the ‘ice-9/match.upstream.scm’ file in your Guile
installation for more details.

   Guile also comes with a pattern matcher specifically tailored to SXML
trees, *Note sxml-match::.

