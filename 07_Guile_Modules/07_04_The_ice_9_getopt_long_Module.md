7.4 The (ice-9 getopt-long) Module
==================================

The ‘(ice-9 getopt-long)’ module exports two procedures: ‘getopt-long’
and ‘option-ref’.

   • ‘getopt-long’ takes a list of strings — the command line arguments
     — an "option specification", and some optional keyword parameters.
     It parses the command line arguments according to the option
     specification and keyword parameters, and returns a data structure
     that encapsulates the results of the parsing.

   • ‘option-ref’ then takes the parsed data structure and a specific
     option’s name, and returns information about that option in
     particular.

   To make these procedures available to your Guile script, include the
expression ‘(use-modules (ice-9 getopt-long))’ somewhere near the top,
before the first usage of ‘getopt-long’ or ‘option-ref’.

7.4.1 A Short getopt-long Example
---------------------------------

This section illustrates how ‘getopt-long’ is used by presenting and
dissecting a simple example.  The first thing that we need is an "option
specification" that tells ‘getopt-long’ how to parse the command line.
This specification is an association list with the long option name as
the key.  Here is how such a specification might look:

     (define option-spec
       '((version (single-char #\v) (value #f))
         (help    (single-char #\h) (value #f))))

   This alist tells ‘getopt-long’ that it should accept two long
options, called _version_ and _help_, and that these options can also be
selected by the single-letter abbreviations _v_ and _h_, respectively.
The ‘(value #f)’ clauses indicate that neither of the options accepts a
value.

   With this specification we can use ‘getopt-long’ to parse a given
command line:

     (define options (getopt-long (command-line) option-spec))

   After this call, ‘options’ contains the parsed command line and is
ready to be examined by ‘option-ref’.  ‘option-ref’ is called like this:

     (option-ref options 'help #f)

It expects the parsed command line, a symbol indicating the option to
examine, and a default value.  The default value is returned if the
option was not present in the command line, or if the option was present
but without a value; otherwise the value from the command line is
returned.  Usually ‘option-ref’ is called once for each possible option
that a script supports.

   The following example shows a main program which puts all this
together to parse its command line and figure out what the user wanted.

     (define (main args)
       (let* ((option-spec '((version (single-char #\v) (value #f))
                             (help    (single-char #\h) (value #f))))
              (options (getopt-long args option-spec))
              (help-wanted (option-ref options 'help #f))
              (version-wanted (option-ref options 'version #f)))
         (if (or version-wanted help-wanted)
             (begin
               (if version-wanted
                   (display "getopt-long-example version 0.3\n"))
               (if help-wanted
                   (display "\
     getopt-long-example [options]
       -v, --version    Display version
       -h, --help       Display this help
     ")))
             (begin
               (display "Hello, World!") (newline)))))

7.4.2 How to Write an Option Specification
------------------------------------------

An option specification is an association list (*note Association
Lists::) with one list element for each supported option.  The key of
each list element is a symbol that names the option, while the value is
a list of option properties:

     OPTION-SPEC ::=  '( (OPT-NAME1 (PROP-NAME PROP-VALUE) …)
                         (OPT-NAME2 (PROP-NAME PROP-VALUE) …)
                         (OPT-NAME3 (PROP-NAME PROP-VALUE) …)
                         …
                       )

   Each OPT-NAME specifies the long option name for that option.  For
example, a list element with OPT-NAME ‘background’ specifies an option
that can be specified on the command line using the long option
‘--background’.  Further information about the option — whether it takes
a value, whether it is required to be present in the command line, and
so on — is specified by the option properties.

   In the example of the preceding section, we already saw that a long
option name can have a equivalent "short option" character.  The
equivalent short option character can be set for an option by specifying
a ‘single-char’ property in that option’s property list.  For example, a
list element like ‘'(output (single-char #\o) …)’ specifies an option
with long name ‘--output’ that can also be specified by the equivalent
short name ‘-o’.

   The ‘value’ property specifies whether an option requires or accepts
a value.  If the ‘value’ property is set to ‘#t’, the option requires a
value: ‘getopt-long’ will signal an error if the option name is present
without a corresponding value.  If set to ‘#f’, the option does not take
a value; in this case, a non-option word that follows the option name in
the command line will be treated as a non-option argument.  If set to
the symbol ‘optional’, the option accepts a value but does not require
one: a non-option word that follows the option name in the command line
will be interpreted as that option’s value.  If the option name for an
option with ‘'(value optional)’ is immediately followed in the command
line by _another_ option name, the value for the first option is
implicitly ‘#t’.

   The ‘required?’ property indicates whether an option is required to
be present in the command line.  If the ‘required?’ property is set to
‘#t’, ‘getopt-long’ will signal an error if the option is not specified.

   Finally, the ‘predicate’ property can be used to constrain the
possible values of an option.  If used, the ‘predicate’ property should
be set to a procedure that takes one argument — the proposed option
value as a string — and returns either ‘#t’ or ‘#f’ according as the
proposed value is or is not acceptable.  If the predicate procedure
returns ‘#f’, ‘getopt-long’ will signal an error.

   By default, options do not have single-character equivalents, are not
required, and do not take values.  Where the list element for an option
includes a ‘value’ property but no ‘predicate’ property, the option
values are unconstrained.

7.4.3 Expected Command Line Format
----------------------------------

In order for ‘getopt-long’ to correctly parse a command line, that
command line must conform to a standard set of rules for how command
line options are specified.  This section explains what those rules are.

   ‘getopt-long’ splits a given command line into several pieces.  All
elements of the argument list are classified to be either options or
normal arguments.  Options consist of two dashes and an option name
(so-called "long" options), or of one dash followed by a single letter
("short" options).

   Options can behave as switches, when they are given without a value,
or they can be used to pass a value to the program.  The value for an
option may be specified using an equals sign, or else is simply the next
word in the command line, so the following two invocations are
equivalent:

     $ ./foo.scm --output=bar.txt
     $ ./foo.scm --output bar.txt

   Short options can be used instead of their long equivalents and can
be grouped together after a single dash.  For example, the following
commands are equivalent.

     $ ./foo.scm --version --help
     $ ./foo.scm -v --help
     $ ./foo.scm -vh

   If an option requires a value, it can only be grouped together with
other short options if it is the last option in the group; the value is
the next argument.  So, for example, with the following option
specification —

     ((apples    (single-char #\a))
      (blimps    (single-char #\b) (value #t))
      (catalexis (single-char #\c) (value #t)))

— the following command lines would all be acceptable:

     $ ./foo.scm -a -b bang -c couth
     $ ./foo.scm -ab bang -c couth
     $ ./foo.scm -ac couth -b bang

   But the next command line is an error, because ‘-b’ is not the last
option in its combination, and because a group of short options cannot
include two options that both require values:

     $ ./foo.scm -abc couth bang

   If an option’s value is optional, ‘getopt-long’ decides whether the
option has a value by looking at what follows it in the argument list.
If the next element is a string, and it does not appear to be an option
itself, then that string is the option’s value.

   If the option ‘--’ appears in the argument list, argument parsing
stops there and subsequent arguments are returned as ordinary arguments,
even if they resemble options.  So, with the command line

     $ ./foo.scm --apples "Granny Smith" -- --blimp Goodyear

‘getopt-long’ will recognize the ‘--apples’ option as having the value
"Granny Smith", but will not treat ‘--blimp’ as an option.  The strings
‘--blimp’ and ‘Goodyear’ will be returned as ordinary argument strings.

7.4.4 Reference Documentation for ‘getopt-long’
-----------------------------------------------

 -- Scheme Procedure: getopt-long args grammar
          [#:stop-at-first-non-option #t]
     Parse the command line given in ARGS (which must be a list of
     strings) according to the option specification GRAMMAR.

     The GRAMMAR argument is expected to be a list of this form:

     ‘((OPTION (PROPERTY VALUE) …) …)’

     where each OPTION is a symbol denoting the long option, but without
     the two leading dashes (e.g. ‘version’ if the option is called
     ‘--version’).

     For each option, there may be list of arbitrarily many
     property/value pairs.  The order of the pairs is not important, but
     every property may only appear once in the property list.  The
     following table lists the possible properties:

     ‘(single-char CHAR)’
          Accept ‘-CHAR’ as a single-character equivalent to ‘--OPTION’.
          This is how to specify traditional Unix-style flags.
     ‘(required? BOOL)’
          If BOOL is true, the option is required.  ‘getopt-long’ will
          raise an error if it is not found in ARGS.
     ‘(value BOOL)’
          If BOOL is ‘#t’, the option accepts a value; if it is ‘#f’, it
          does not; and if it is the symbol ‘optional’, the option may
          appear in ARGS with or without a value.
     ‘(predicate FUNC)’
          If the option accepts a value (i.e. you specified ‘(value #t)’
          for this option), then ‘getopt-long’ will apply FUNC to the
          value, and throw an exception if it returns ‘#f’.  FUNC should
          be a procedure which accepts a string and returns a boolean
          value; you may need to use quasiquotes to get it into GRAMMAR.

     The ‘#:stop-at-first-non-option’ keyword, if specified with any
     true value, tells ‘getopt-long’ to stop when it gets to the first
     non-option in the command line.  That is, at the first word which
     is neither an option itself, nor the value of an option.
     Everything in the command line from that word onwards will be
     returned as non-option arguments.

   ‘getopt-long’’s ARGS parameter is expected to be a list of strings
like the one returned by ‘command-line’, with the first element being
the name of the command.  Therefore ‘getopt-long’ ignores the first
element in ARGS and starts argument interpretation with the second
element.

   ‘getopt-long’ signals an error if any of the following conditions
hold.

   • The option grammar has an invalid syntax.

   • One of the options in the argument list was not specified by the
     grammar.

   • A required option is omitted.

   • An option which requires an argument did not get one.

   • An option that doesn’t accept an argument does get one (this can
     only happen using the long option ‘--opt=VALUE’ syntax).

   • An option predicate fails.

   ‘#:stop-at-first-non-option’ is useful for command line invocations
like ‘guild [--help | --version] [script [script-options]]’ and ‘cvs
[general-options] command [command-options]’, where there are options at
two levels: some generic and understood by the outer command, and some
that are specific to the particular script or command being invoked.  To
use ‘getopt-long’ in such cases, you would call it twice: firstly with
‘#:stop-at-first-non-option #t’, so as to parse any generic options and
identify the wanted script or sub-command; secondly, and after trimming
off the initial generic command words, with a script- or
sub-command-specific option grammar, so as to process those specific
options.

7.4.5 Reference Documentation for ‘option-ref’
----------------------------------------------

 -- Scheme Procedure: option-ref options key default
     Search OPTIONS for a command line option named KEY and return its
     value, if found.  If the option has no value, but was given, return
     ‘#t’.  If the option was not given, return DEFAULT.  OPTIONS must
     be the result of a call to ‘getopt-long’.

   ‘option-ref’ always succeeds, either by returning the requested
option value from the command line, or the default value.

   The special key ‘'()’ can be used to get a list of all non-option
arguments.

