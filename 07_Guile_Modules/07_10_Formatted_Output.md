7.10 Formatted Output
=====================

The ‘format’ function is a powerful way to print numbers, strings and
other objects together with literal text under the control of a format
string.  This function is available from

     (use-modules (ice-9 format))

   A format string is generally more compact and easier than using just
the standard procedures like ‘display’, ‘write’ and ‘newline’.
Parameters in the output string allow various output styles, and
parameters can be taken from the arguments for runtime flexibility.

   ‘format’ is similar to the Common Lisp procedure of the same name,
but it’s not identical and doesn’t have quite all the features found in
Common Lisp.

   C programmers will note the similarity between ‘format’ and ‘printf’,
though escape sequences are marked with ~ instead of %, and are more
powerful.


 -- Scheme Procedure: format dest fmt arg …
     Write output specified by the FMT string to DEST.  DEST can be an
     output port, ‘#t’ for ‘current-output-port’ (*note Default
     Ports::), or ‘#f’ to return the output as a string.

     FMT can contain literal text to be output, and ~ escapes.  Each
     escape has the form

          ~ [param [, param…] [:] [@] code

     code is a character determining the escape sequence.  The : and @
     characters are optional modifiers, one or both of which change the
     way various codes operate.  Optional parameters are accepted by
     some codes too.  Parameters have the following forms,

     [+/-]number
          An integer, with optional + or -.
     ’ (apostrophe)
          The following character in the format string, for instance ’z
          for z.
     v
          The next function argument as the parameter.  v stands for
          “variable”, a parameter can be calculated at runtime and
          included in the arguments.  Upper case V can be used too.
     #
          The number of arguments remaining.  (See ~* below for some
          usages.)

     Parameters are separated by commas (,).  A parameter can be left
     empty to keep its default value when supplying later parameters.


     The following escapes are available.  The code letters are not
     case-sensitive, upper and lower case are the same.

     ~a
     ~s
          Object output.  Parameters: MINWIDTH, PADINC, MINPAD, PADCHAR.

          ~a outputs an argument like ‘display’, ~s outputs an argument
          like ‘write’ (*note Writing::).

               (format #t "~a" "foo") ⊣ foo
               (format #t "~s" "foo") ⊣ "foo"

          ~:a and ~:s put objects that don’t have an external
          representation in quotes like a string.

               (format #t "~:a" car) ⊣ "#<primitive-procedure car>"

          If the output is less than MINWIDTH characters (default 0),
          it’s padded on the right with PADCHAR (default space).  ~@a
          and ~@s put the padding on the left instead.

               (format #f "~5a" 'abc)       ⇒ "abc  "
               (format #f "~5,,,'-@a" 'abc) ⇒ "--abc"

          MINPAD is a minimum for the padding then plus a multiple of
          PADINC.  Ie. the padding is MINPAD + N * PADINC, where N is
          the smallest integer making the total object plus padding
          greater than or equal to MINWIDTH.  The default MINPAD is 0
          and the default PADINC is 1 (imposing no minimum or multiple).

               (format #f "~5,1,4a" 'abc) ⇒ "abc    "

     ~c
          Character.  Parameter: CHARNUM.

          Output a character.  The default is to simply output, as per
          ‘write-char’ (*note Writing::).  ~@c prints in ‘write’ style.
          ~:c prints control characters (ASCII 0 to 31) in ^X form.

               (format #t "~c" #\z)        ⊣ z
               (format #t "~@c" #\z)       ⊣ #\z
               (format #t "~:c" #\newline) ⊣ ^J

          If the CHARNUM parameter is given then an argument is not
          taken but instead the character is ‘(integer->char CHARNUM)’
          (*note Characters::).  This can be used for instance to output
          characters given by their ASCII code.

               (format #t "~65c")  ⊣ A

     ~d
     ~x
     ~o
     ~b
          Integer.  Parameters: MINWIDTH, PADCHAR, COMMACHAR,
          COMMAWIDTH.

          Output an integer argument as a decimal, hexadecimal, octal or
          binary integer (respectively), in a locale-independent way.

               (format #t "~d" 123) ⊣ 123

          ~@d etc shows a + sign is shown on positive numbers.

               (format #t "~@b" 12) ⊣ +1100

          If the output is less than the MINWIDTH parameter (default no
          minimum), it’s padded on the left with the PADCHAR parameter
          (default space).

               (format #t "~5,'*d" 12)   ⊣ ***12
               (format #t "~5,'0d" 12)   ⊣ 00012
               (format #t "~3d"    1234) ⊣ 1234

          ~:d adds commas (or the COMMACHAR parameter) every three
          digits (or the COMMAWIDTH parameter many).  However, when your
          intent is to write numbers in a way that follows typographical
          conventions, using ~h is recommended.

               (format #t "~:d" 1234567)         ⊣ 1,234,567
               (format #t "~10,'*,'/,2:d" 12345) ⊣ ***1/23/45

          Hexadecimal ~x output is in lower case, but the ~( and ~) case
          conversion directives described below can be used to get upper
          case.

               (format #t "~x"       65261) ⊣ feed
               (format #t "~:@(~x~)" 65261) ⊣ FEED

     ~r
          Integer in words, roman numerals, or a specified radix.
          Parameters: RADIX, MINWIDTH, PADCHAR, COMMACHAR, COMMAWIDTH.

          With no parameters output is in words as a cardinal like
          “ten”, or ~:r prints an ordinal like “tenth”.

               (format #t "~r" 9)  ⊣ nine        ;; cardinal
               (format #t "~r" -9) ⊣ minus nine  ;; cardinal
               (format #t "~:r" 9) ⊣ ninth       ;; ordinal

          And also with no parameters, ~@r gives roman numerals and ~:@r
          gives old roman numerals.  In old roman numerals there’s no
          “subtraction”, so 9 is VIIII instead of IX. In both cases only
          positive numbers can be output.

               (format #t "~@r" 89)  ⊣ LXXXIX     ;; roman
               (format #t "~:@r" 89) ⊣ LXXXVIIII  ;; old roman

          When a parameter is given it means numeric output in the
          specified RADIX.  The modifiers and parameters following the
          radix are the same as described for ~d etc above.

               (format #f "~3r" 27)   ⇒ "1000"    ;; base 3
               (format #f "~3,5r" 26) ⇒ "  222"   ;; base 3 width 5

     ~f
          Fixed-point float.  Parameters: WIDTH, DECIMALS, SCALE,
          OVERFLOWCHAR, PADCHAR.

          Output a number or number string in fixed-point format, ie.
          with a decimal point.

               (format #t "~f" 5)      ⊣ 5.0
               (format #t "~f" "123")  ⊣ 123.0
               (format #t "~f" "1e-1") ⊣ 0.1

          ~@f prints a + sign on positive numbers (including zero).

               (format #t "~@f" 0) ⊣ +0.0

          If the output is less than WIDTH characters it’s padded on the
          left with PADCHAR (space by default).  If the output equals or
          exceeds WIDTH then there’s no padding.  The default for WIDTH
          is no padding.

               (format #f "~6f" -1.5)      ⇒ "  -1.5"
               (format #f "~6,,,,'*f" 23)  ⇒ "**23.0"
               (format #f "~6f" 1234567.0) ⇒ "1234567.0"

          DECIMALS is how many digits to print after the decimal point,
          with the value rounded or padded with zeros as necessary.
          (The default is to output as many decimals as required.)

               (format #t "~1,2f" 3.125) ⊣ 3.13
               (format #t "~1,2f" 1.5)   ⊣ 1.50

          SCALE is a power of 10 applied to the value, moving the
          decimal point that many places.  A positive SCALE increases
          the value shown, a negative decreases it.

               (format #t "~,,2f" 1234)  ⊣ 123400.0
               (format #t "~,,-2f" 1234) ⊣ 12.34

          If OVERFLOWCHAR and WIDTH are both given and if the output
          would exceed WIDTH, then that many OVERFLOWCHARs are printed
          instead of the value.

               (format #t "~6,,,'xf" 12345) ⊣ 12345.
               (format #t "~5,,,'xf" 12345) ⊣ xxxxx

     ~h
          Localized number(1).  Parameters: WIDTH, DECIMALS, PADCHAR.

          Like ~f, output an exact or floating point number, but do so
          according to the current locale, or according to the given
          locale object when the ‘:’ modifier is used (*note
          ‘number->locale-string’: Number Input and Output.).

               (format #t "~h" 12345.5678)  ; with "C" as the current locale
               ⊣ 12345.5678

               (format #t "~14,,'*:h" 12345.5678
                       (make-locale LC_ALL "en_US"))
               ⊣ ***12,345.5678

               (format #t "~,2:h" 12345.5678
                       (make-locale LC_NUMERIC "fr_FR"))
               ⊣ 12 345,56

     ~e
          Exponential float.  Parameters: WIDTH, MANTDIGITS, EXPDIGITS,
          INTDIGITS, OVERFLOWCHAR, PADCHAR, EXPCHAR.

          Output a number or number string in exponential notation.

               (format #t "~e" 5000.25) ⊣ 5.00025E+3
               (format #t "~e" "123.4") ⊣ 1.234E+2
               (format #t "~e" "1e4")   ⊣ 1.0E+4

          ~@e prints a + sign on positive numbers (including zero).
          (This is for the mantissa, a + or - sign is always shown on
          the exponent.)

               (format #t "~@e" 5000.0) ⊣ +5.0E+3

          If the output is less than WIDTH characters it’s padded on the
          left with PADCHAR (space by default).  The default for WIDTH
          is to output with no padding.

               (format #f "~10e" 1234.0)     ⇒ "  1.234E+3"
               (format #f "~10,,,,,'*e" 0.5) ⇒ "****5.0E-1"

          MANTDIGITS is the number of digits shown in the mantissa after
          the decimal point.  The value is rounded or trailing zeros are
          added as necessary.  The default MANTDIGITS is to show as much
          as needed by the value.

               (format #f "~,3e" 11111.0) ⇒ "1.111E+4"
               (format #f "~,8e" 123.0)   ⇒ "1.23000000E+2"

          EXPDIGITS is the minimum number of digits shown for the
          exponent, with leading zeros added if necessary.  The default
          for EXPDIGITS is to show only as many digits as required.  At
          least 1 digit is always shown.

               (format #f "~,,1e" 1.0e99) ⇒ "1.0E+99"
               (format #f "~,,6e" 1.0e99) ⇒ "1.0E+000099"

          INTDIGITS (default 1) is the number of digits to show before
          the decimal point in the mantissa.  INTDIGITS can be zero, in
          which case the integer part is a single 0, or it can be
          negative, in which case leading zeros are shown after the
          decimal point.

               (format #t "~,,,3e" 12345.0)  ⊣ 123.45E+2
               (format #t "~,,,0e" 12345.0)  ⊣ 0.12345E+5
               (format #t "~,,,-3e" 12345.0) ⊣ 0.00012345E+8

          If OVERFLOWCHAR is given then WIDTH is a hard limit.  If the
          output would exceed WIDTH then instead that many OVERFLOWCHARs
          are printed.

               (format #f "~6,,,,'xe" 100.0) ⇒ "1.0E+2"
               (format #f "~3,,,,'xe" 100.0) ⇒ "xxx"

          EXPCHAR is the exponent marker character (default E).

               (format #t "~,,,,,,'ee" 100.0) ⊣ 1.0e+2

     ~g
          General float.  Parameters: WIDTH, MANTDIGITS, EXPDIGITS,
          INTDIGITS, OVERFLOWCHAR, PADCHAR, EXPCHAR.

          Output a number or number string in either exponential format
          the same as ~e, or fixed-point format like ~f but aligned
          where the mantissa would have been and followed by padding
          where the exponent would have been.

          Fixed-point is used when the absolute value is 0.1 or more and
          it takes no more space than the mantissa in exponential
          format, ie. basically up to MANTDIGITS digits.

               (format #f "~12,4,2g" 999.0)    ⇒ "   999.0    "
               (format #f "~12,4,2g" "100000") ⇒ "  1.0000E+05"

          The parameters are interpreted as per ~e above.  When
          fixed-point is used, the DECIMALS parameter to ~f is
          established from MANTDIGITS, so as to give a total
          MANTDIGITS+1 figures.

     ~$
          Monetary style fixed-point float.  Parameters: DECIMALS,
          INTDIGITS, WIDTH, PADCHAR.

          Output a number or number string in fixed-point format, ie.
          with a decimal point.  DECIMALS is the number of decimal
          places to show, default 2.

               (format #t "~$" 5)       ⊣ 5.00
               (format #t "~4$" "2.25") ⊣ 2.2500
               (format #t "~4$" "1e-2") ⊣ 0.0100

          ~@$ prints a + sign on positive numbers (including zero).

               (format #t "~@$" 0) ⊣ +0.00

          INTDIGITS is a minimum number of digits to show in the integer
          part of the value (default 1).

               (format #t "~,3$" 9.5)   ⊣ 009.50
               (format #t "~,0$" 0.125) ⊣ .13

          If the output is less than WIDTH characters (default 0), it’s
          padded on the left with PADCHAR (default space).  ~:$ puts the
          padding after the sign.

               (format #f "~,,8$" -1.5)   ⇒ "   -1.50"
               (format #f "~,,8:$" -1.5)  ⇒ "-   1.50"
               (format #f "~,,8,'.:@$" 3) ⇒ "+...3.00"

          Note that floating point for dollar amounts is generally not a
          good idea, because a cent 0.01 cannot be represented exactly
          in the binary floating point Guile uses, which leads to slowly
          accumulating rounding errors.  Keeping values as cents (or
          fractions of a cent) in integers then printing with the scale
          option in ~f may be a better approach.

     ~i
          Complex fixed-point float.  Parameters: WIDTH, DECIMALS,
          SCALE, OVERFLOWCHAR, PADCHAR.

          Output the argument as a complex number, with both real and
          imaginary part shown (even if one or both are zero).

          The parameters and modifiers are the same as for fixed-point
          ~f described above.  The real and imaginary parts are both
          output with the same given parameters and modifiers, except
          that for the imaginary part the @ modifier is always enabled,
          so as to print a + sign between the real and imaginary parts.

               (format #t "~i" 1)  ⊣ 1.0+0.0i

     ~p
          Plural.  No parameters.

          Output nothing if the argument is 1, or ‘s’ for any other
          value.

               (format #t "enter name~p" 1) ⊣ enter name
               (format #t "enter name~p" 2) ⊣ enter names

          ~@p prints ‘y’ for 1 or ‘ies’ otherwise.

               (format #t "pupp~@p" 1) ⊣ puppy
               (format #t "pupp~@p" 2) ⊣ puppies

          ~:p re-uses the preceding argument instead of taking a new
          one, which can be convenient when printing some sort of count.

               (format #t "~d cat~:p" 9)   ⊣ 9 cats
               (format #t "~d pupp~:@p" 5) ⊣ 5 puppies

          ~p is designed for English plurals and there’s no attempt to
          support other languages.  ~[ conditionals (below) may be able
          to help.  When using ‘gettext’ to translate messages
          ‘ngettext’ is probably best though (*note
          Internationalization::).

     ~y
          Structured printing.  Parameters: WIDTH.

          ~y outputs an argument using ‘pretty-print’ (*note Pretty
          Printing::).  The result will be formatted to fit within WIDTH
          columns (79 by default), consuming multiple lines if
          necessary.

          ~@y outputs an argument using ‘truncated-print’ (*note Pretty
          Printing::).  The resulting code will be formatted to fit
          within WIDTH columns (79 by default), on a single line.  The
          output will be truncated if necessary.

          ~:@y is like ~@y, except the WIDTH parameter is interpreted to
          be the maximum column to which to output.  That is to say, if
          you are at column 10, and ~60:@y is seen, the datum will be
          truncated to 50 columns.

     ~?
     ~k
          Sub-format.  No parameters.

          Take a format string argument and a second argument which is a
          list of arguments for that string, and output the result.

               (format #t "~?" "~d ~d" '(1 2))    ⊣ 1 2

          ~@?  takes arguments for the sub-format directly rather than
          in a list.

               (format #t "~@? ~s" "~d ~d" 1 2 "foo") ⊣ 1 2 "foo"

          ~?  and ~k are the same, ~k is provided for T-Scheme
          compatibility.

     ~*
          Argument jumping.  Parameter: N.

          Move forward N arguments (default 1) in the argument list.
          ~:* moves backwards.  (N cannot be negative.)

               (format #f "~d ~2*~d" 1 2 3 4) ⇒ "1 4"
               (format #f "~d ~:*~d" 6)       ⇒ "6 6"

          ~@* moves to argument number N.  The first argument is number
          0 (and that’s the default for N).

               (format #f "~d~d again ~@*~d~d" 1 2) ⇒ "12 again 12"
               (format #f "~d~d~d ~1@*~d~d" 1 2 3)  ⇒ "123 23"

          A # move to the end followed by a : modifier move back can be
          used for an absolute position relative to the end of the
          argument list, a reverse of what the @ modifier does.

               (format #t "~#*~2:*~a" 'a 'b 'c 'd)   ⊣ c

          At the end of the format string the current argument position
          doesn’t matter, any further arguments are ignored.

     ~t
          Advance to a column position.  Parameters: COLNUM, COLINC,
          PADCHAR.

          Output PADCHAR (space by default) to move to the given COLNUM
          column.  The start of the line is column 0, the default for
          COLNUM is 1.

               (format #f "~tX")  ⇒ " X"
               (format #f "~3tX") ⇒ "   X"

          If the current column is already past COLNUM, then the move is
          to there plus a multiple of COLINC, ie. column COLNUM + N *
          COLINC for the smallest N which makes that value greater than
          or equal to the current column.  The default COLINC is 1
          (which means no further move).

               (format #f "abcd~2,5,'.tx") ⇒ "abcd...x"

          ~@t takes COLNUM as an offset from the current column.  COLNUM
          many pad characters are output, then further padding to make
          the current column a multiple of COLINC, if it isn’t already
          so.

               (format #f "a~3,5'*@tx") ⇒ "a****x"

          ~t is implemented using ‘port-column’ (*note Reading::), so it
          works even there has been other output before ‘format’.

     ~~
          Tilde character.  Parameter: N.

          Output a tilde character ~, or N many if a parameter is given.
          Normally ~ introduces an escape sequence, ~~ is the way to
          output a literal tilde.

     ~%
          Newline.  Parameter: N.

          Output a newline character, or N many if a parameter is given.
          A newline (or a few newlines) can of course be output just by
          including them in the format string.

     ~&
          Start a new line.  Parameter: N.

          Output a newline if not already at the start of a line.  With
          a parameter, output that many newlines, but with the first
          only if not already at the start of a line.  So for instance 3
          would be a newline if not already at the start of a line, and
          2 further newlines.

     ~_
          Space character.  Parameter: N.

          Output a space character, or N many if a parameter is given.

          With a variable parameter this is one way to insert runtime
          calculated padding (~t or the various field widths can do
          similar things).

               (format #f "~v_foo" 4) ⇒ "    foo"

     ~/
          Tab character.  Parameter: N.

          Output a tab character, or N many if a parameter is given.

     ~|
          Formfeed character.  Parameter: N.

          Output a formfeed character, or N many if a parameter is
          given.

     ~!
          Force output.  No parameters.

          At the end of output, call ‘force-output’ to flush any buffers
          on the destination (*note Writing::).  ~!  can occur anywhere
          in the format string, but the force is done at the end of
          output.

          When output is to a string (destination ‘#f’), ~!  does
          nothing.

     ~newline (ie. newline character)
          Continuation line.  No parameters.

          Skip this newline and any following whitespace in the format
          string, ie. don’t send it to the output.  This can be used to
          break up a long format string for readability, but not print
          the extra whitespace.

               (format #f "abc~
                           ~d def~
                           ~d" 1 2) ⇒ "abc1 def2"

          ~:newline skips the newline but leaves any further whitespace
          to be printed normally.

          ~@newline prints the newline then skips following whitespace.

     ~( ~)
          Case conversion.  No parameters.

          Between ~( and ~) the case of all output is changed.  The
          modifiers on ~( control the conversion.

               ~( — lower case.
               ~:@( — upper case.

          For example,

               (format #t "~(Hello~)")   ⊣ hello
               (format #t "~:@(Hello~)") ⊣ HELLO

          In the future it’s intended the modifiers : and @ alone will
          capitalize the first letters of words, as per Common Lisp
          ‘format’, but the current implementation of this is flawed and
          not recommended for use.

          Case conversions do not nest, currently.  This might change in
          the future, but if it does then it will be to Common Lisp
          style where the outermost conversion has priority, overriding
          inner ones (making those fairly pointless).

     ~{ ~}
          Iteration.  Parameter: MAXREPS (for ~{).

          The format between ~{ and ~} is iterated.  The modifiers to ~{
          determine how arguments are taken.  The default is a list
          argument with each iteration successively consuming elements
          from it.  This is a convenient way to output a whole list.

               (format #t "~{~d~}"     '(1 2 3))       ⊣ 123
               (format #t "~{~s=~d ~}" '("x" 1 "y" 2)) ⊣ "x"=1 "y"=2

          ~:{ takes a single argument which is a list of lists, each of
          those contained lists gives the arguments for the iterated
          format.

               (format #t "~:{~dx~d ~}" '((1 2) (3 4) (5 6)))
               ⊣ 1x2 3x4 5x6

          ~@{ takes arguments directly, with each iteration successively
          consuming arguments.

               (format #t "~@{~d~}"     1 2 3)       ⊣ 123
               (format #t "~@{~s=~d ~}" "x" 1 "y" 2) ⊣ "x"=1 "y"=2

          ~:@{ takes list arguments, one argument for each iteration,
          using that list for the format.

               (format #t "~:@{~dx~d ~}" '(1 2) '(3 4) '(5 6))
               ⊣ 1x2 3x4 5x6

          Iterating stops when there are no more arguments or when the
          MAXREPS parameter to ~{ is reached (default no maximum).

               (format #t "~2{~d~}" '(1 2 3 4)) ⊣ 12

          If the format between ~{ and ~} is empty, then a format string
          argument is taken (before iteration argument(s)) and used
          instead.  This allows a sub-format (like ~?  above) to be
          iterated.

               (format #t "~{~}" "~d" '(1 2 3)) ⊣ 123

          Iterations can be nested, an inner iteration operates in the
          same way as described, but of course on the arguments the
          outer iteration provides it.  This can be used to work into
          nested list structures.  For example in the following the
          inner ~{~d~}x is applied to ‘(1 2)’ then ‘(3 4 5)’ etc.

               (format #t "~{~{~d~}x~}" '((1 2) (3 4 5))) ⊣ 12x345x

          See also ~^ below for escaping from iteration.

     ~[ ~; ~]
          Conditional.  Parameter: SELECTOR.

          A conditional block is delimited by ~[ and ~], and ~;
          separates clauses within the block.  ~[ takes an integer
          argument and that number clause is used.  The first clause is
          number 0.

               (format #f "~[peach~;banana~;mango~]" 1)  ⇒ "banana"

          The SELECTOR parameter can be used for the clause number,
          instead of taking an argument.

               (format #f "~2[peach~;banana~;mango~]") ⇒ "mango"

          If the clause number is out of range then nothing is output.
          Or the last clause can be ~:; to use that for a number out of
          range.

               (format #f "~[banana~;mango~]"         99) ⇒ ""
               (format #f "~[banana~;mango~:;fruit~]" 99) ⇒ "fruit"

          ~:[ treats the argument as a flag, and expects two clauses.
          The first is used if the argument is ‘#f’ or the second
          otherwise.

               (format #f "~:[false~;not false~]" #f)   ⇒ "false"
               (format #f "~:[false~;not false~]" 'abc) ⇒ "not false"

               (let ((n 3))
                 (format #t "~d gnu~:[s are~; is~] here" n (= 1 n)))
               ⊣ 3 gnus are here

          ~@[ also treats the argument as a flag, and expects one
          clause.  If the argument is ‘#f’ then no output is produced
          and the argument is consumed, otherwise the clause is used and
          the argument is not consumed, it’s left for the clause.  This
          can be used for instance to suppress output if ‘#f’ means
          something not available.

               (format #f "~@[temperature=~d~]" 27) ⇒ "temperature=27"
               (format #f "~@[temperature=~d~]" #f) ⇒ ""

     ~^
          Escape.  Parameters: VAL1, VAL2, VAL3.

          Stop formatting if there are no more arguments.  This can be
          used for instance to have a format string adapt to a variable
          number of arguments.

               (format #t "~d~^ ~d" 1)   ⊣ 1
               (format #t "~d~^ ~d" 1 2) ⊣ 1 2

          Within a ~{ ~} iteration, ~^ stops the current iteration step
          if there are no more arguments to that step, but continuing
          with possible further steps and the rest of the format.  This
          can be used for instance to avoid a separator on the last
          iteration, or to adapt to variable length argument lists.

               (format #f "~{~d~^/~} go"    '(1 2 3))     ⇒ "1/2/3 go"
               (format #f "~:{ ~d~^~d~} go" '((1) (2 3))) ⇒ " 1 23 go"

          Within a ~?  sub-format, ~^ operates just on that sub-format.
          If it terminates the sub-format then the originating format
          will still continue.

               (format #t "~? items" "~d~^ ~d" '(1))   ⊣ 1 items
               (format #t "~? items" "~d~^ ~d" '(1 2)) ⊣ 1 2 items

          The parameters to ~^ (which are numbers) change the condition
          used to terminate.  For a single parameter, termination is
          when that value is zero (notice this makes plain ~^ equivalent
          to ~#^).  For two parameters, termination is when those two
          are equal.  For three parameters, termination is when VAL1 <=
          VAL2 and VAL2 <= VAL3.

     ~q
          Inquiry message.  Insert a copyright message into the output.

          ~:q inserts the format implementation version.


     It’s an error if there are not enough arguments for the escapes in
     the format string, but any excess arguments are ignored.

     Iterations ~{ ~} and conditionals ~[ ~; ~] can be nested, but must
     be properly nested, meaning the inner form must be entirely within
     the outer form.  So it’s not possible, for instance, to try to
     conditionalize the endpoint of an iteration.

          (format #t "~{ ~[ ... ~] ~}" ...)       ;; good
          (format #t "~{ ~[ ... ~} ... ~]" ...)   ;; bad

     The same applies to case conversions ~( ~), they must properly nest
     with respect to iterations and conditionals (though currently a
     case conversion cannot nest within another case conversion).

     When a sub-format (~?)  is used, that sub-format string must be
     self-contained.  It cannot for instance give a ~{ to begin an
     iteration form and have the ~} up in the originating format, or
     similar.


   Guile contains a ‘format’ procedure even when the module ‘(ice-9
format)’ is not loaded.  The default ‘format’ is ‘simple-format’ (*note
Writing::), it doesn’t support all escape sequences documented in this
section, and will signal an error if you try to use one of them.  The
reason for two versions is that the full ‘format’ is fairly large and
requires some time to load.  ‘simple-format’ is often adequate too.

   ---------- Footnotes ----------

   (1) The ~h format specifier first appeared in Guile version 2.0.6.

