7.9 Pretty Printing
===================

The module ‘(ice-9 pretty-print)’ provides the procedure ‘pretty-print’,
which provides nicely formatted output of Scheme objects.  This is
especially useful for deeply nested or complex data structures, such as
lists and vectors.

   The module is loaded by entering the following:

     (use-modules (ice-9 pretty-print))

   This makes the procedure ‘pretty-print’ available.  As an example how
‘pretty-print’ will format the output, see the following:

     (pretty-print '(define (foo) (lambda (x)
     (cond ((zero? x) #t) ((negative? x) -x) (else
     (if (= x 1) 2 (* x x x)))))))
     ⊣
     (define (foo)
       (lambda (x)
         (cond ((zero? x) #t)
               ((negative? x) -x)
               (else (if (= x 1) 2 (* x x x))))))

 -- Scheme Procedure: pretty-print obj [port] [keyword-options]
     Print the textual representation of the Scheme object OBJ to PORT.
     PORT defaults to the current output port, if not given.

     The further KEYWORD-OPTIONS are keywords and parameters as follows,

     #:display? FLAG
          If FLAG is true then print using ‘display’.  The default is
          ‘#f’ which means use ‘write’ style.  (*note Writing::)

     #:per-line-prefix STRING
          Print the given STRING as a prefix on each line.  The default
          is no prefix.

     #:width COLUMNS
          Print within the given COLUMNS.  The default is 79.

   Also exported by the ‘(ice-9 pretty-print)’ module is
‘truncated-print’, a procedure to print Scheme datums, truncating the
output to a certain number of characters.  This is useful when you need
to present an arbitrary datum to the user, but you only have one line in
which to do so.

     (define exp '(a b #(c d e) f . g))
     (truncated-print exp #:width 10) (newline)
     ⊣ (a b . #)
     (truncated-print exp #:width 15) (newline)
     ⊣ (a b # f . g)
     (truncated-print exp #:width 18) (newline)
     ⊣ (a b #(c ...) . #)
     (truncated-print exp #:width 20) (newline)
     ⊣ (a b #(c d e) f . g)
     (truncated-print "The quick brown fox" #:width 20) (newline)
     ⊣ "The quick brown..."
     (truncated-print (current-module) #:width 20) (newline)
     ⊣ #<directory (gui...>

   ‘truncated-print’ will not output a trailing newline.  If an
expression does not fit in the given width, it will be truncated –
possibly ellipsized(1), or in the worst case, displayed as #.

 -- Scheme Procedure: truncated-print obj [port] [keyword-options]
     Print OBJ, truncating the output, if necessary, to make it fit into
     WIDTH characters.  By default, OBJ will be printed using ‘write’,
     though that behavior can be overridden via the DISPLAY? keyword
     argument.

     The default behaviour is to print depth-first, meaning that the
     entire remaining width will be available to each sub-expression of
     OBJ – e.g., if OBJ is a vector, each member of OBJ.  One can
     attempt to “ration” the available width, trying to allocate it
     equally to each sub-expression, via the BREADTH-FIRST? keyword
     argument.

     The further KEYWORD-OPTIONS are keywords and parameters as follows,

     #:display? FLAG
          If FLAG is true then print using ‘display’.  The default is
          ‘#f’ which means use ‘write’ style.  (*note Writing::)

     #:width COLUMNS
          Print within the given COLUMNS.  The default is 79.

     #:breadth-first? FLAG
          If FLAG is true, then allocate the available width
          breadth-first among elements of a compound data structure
          (list, vector, pair, etc.).  The default is ‘#f’ which means
          that any element is allowed to consume all of the available
          width.

   ---------- Footnotes ----------

   (1) On Unicode-capable ports, the ellipsis is represented by
character ‘HORIZONTAL ELLIPSIS’ (U+2026), otherwise it is represented by
three dots.

