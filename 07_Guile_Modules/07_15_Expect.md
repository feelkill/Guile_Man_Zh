7.15 Expect
===========

The macros in this section are made available with:

     (use-modules (ice-9 expect))

   ‘expect’ is a macro for selecting actions based on the output from a
port.  The name comes from a tool of similar functionality by Don Libes.
Actions can be taken when a particular string is matched, when a timeout
occurs, or when end-of-file is seen on the port.  The ‘expect’ macro is
described below; ‘expect-strings’ is a front-end to ‘expect’ based on
regexec (see the regular expression documentation).

 -- Macro: expect-strings clause …
     By default, ‘expect-strings’ will read from the current input port.
     The first term in each clause consists of an expression evaluating
     to a string pattern (regular expression).  As characters are read
     one-by-one from the port, they are accumulated in a buffer string
     which is matched against each of the patterns.  When a pattern
     matches, the remaining expression(s) in the clause are evaluated
     and the value of the last is returned.  For example:

          (with-input-from-file "/etc/passwd"
            (lambda ()
              (expect-strings
                ("^nobody" (display "Got a nobody user.\n")
                           (display "That's no problem.\n"))
                ("^daemon" (display "Got a daemon user.\n")))))

     The regular expression is compiled with the ‘REG_NEWLINE’ flag, so
     that the ^ and $ anchors will match at any newline, not just at the
     start and end of the string.

     There are two other ways to write a clause:

     The expression(s) to evaluate can be omitted, in which case the
     result of the regular expression match (converted to strings, as
     obtained from regexec with match-pick set to "") will be returned
     if the pattern matches.

     The symbol ‘=>’ can be used to indicate that the expression is a
     procedure which will accept the result of a successful regular
     expression match.  E.g.,

          ("^daemon" => write)
          ("^d(aemon)" => (lambda args (for-each write args)))
          ("^da(em)on" => (lambda (all sub)
                            (write all) (newline)
                            (write sub) (newline)))

     The order of the substrings corresponds to the order in which the
     opening brackets occur.

     A number of variables can be used to control the behaviour of
     ‘expect’ (and ‘expect-strings’).  Most have default top-level
     bindings to the value ‘#f’, which produces the default behaviour.
     They can be redefined at the top level or locally bound in a form
     enclosing the expect expression.

     ‘expect-port’
          A port to read characters from, instead of the current input
          port.
     ‘expect-timeout’
          ‘expect’ will terminate after this number of seconds,
          returning ‘#f’ or the value returned by expect-timeout-proc.
     ‘expect-timeout-proc’
          A procedure called if timeout occurs.  The procedure takes a
          single argument: the accumulated string.
     ‘expect-eof-proc’
          A procedure called if end-of-file is detected on the input
          port.  The procedure takes a single argument: the accumulated
          string.
     ‘expect-char-proc’
          A procedure to be called every time a character is read from
          the port.  The procedure takes a single argument: the
          character which was read.
     ‘expect-strings-compile-flags’
          Flags to be used when compiling a regular expression, which
          are passed to ‘make-regexp’ *Note Regexp Functions::.  The
          default value is ‘regexp/newline’.
     ‘expect-strings-exec-flags’
          Flags to be used when executing a regular expression, which
          are passed to regexp-exec *Note Regexp Functions::.  The
          default value is ‘regexp/noteol’, which prevents ‘$’ from
          matching the end of the string while it is still accumulating,
          but still allows it to match after a line break or at the end
          of file.

     Here’s an example using all of the variables:

          (let ((expect-port (open-input-file "/etc/passwd"))
                (expect-timeout 1)
                (expect-timeout-proc
                  (lambda (s) (display "Times up!\n")))
                (expect-eof-proc
                  (lambda (s) (display "Reached the end of the file!\n")))
                (expect-char-proc display)
                (expect-strings-compile-flags (logior regexp/newline regexp/icase))
                (expect-strings-exec-flags 0))
             (expect-strings
               ("^nobody"  (display "Got a nobody user\n"))))

 -- Macro: expect clause …
     ‘expect’ is used in the same way as ‘expect-strings’, but tests are
     specified not as patterns, but as procedures.  The procedures are
     called in turn after each character is read from the port, with two
     arguments: the value of the accumulated string and a flag to
     indicate whether end-of-file has been reached.  The flag will
     usually be ‘#f’, but if end-of-file is reached, the procedures are
     called an additional time with the final accumulated string and
     ‘#t’.

     The test is successful if the procedure returns a non-false value.

     If the ‘=>’ syntax is used, then if the test succeeds it must
     return a list containing the arguments to be provided to the
     corresponding expression.

     In the following example, a string will only be matched at the
     beginning of the file:

          (let ((expect-port (open-input-file "/etc/passwd")))
            (expect
               ((lambda (s eof?) (string=? s "fnord!"))
                  (display "Got a nobody user!\n"))))

     The control variables described for ‘expect-strings’ also influence
     the behaviour of ‘expect’, with the exception of variables whose
     names begin with ‘expect-strings-’.

