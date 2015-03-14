4 Programming in Scheme
***********************

Guile’s core language is Scheme, and a lot can be achieved simply by
using Guile to write and run Scheme programs — as opposed to having to
dive into C code.  In this part of the manual, we explain how to use
Guile in this mode, and describe the tools that Guile provides to help
you with script writing, debugging, and packaging your programs for
distribution.

   For detailed reference information on the variables, functions, and
so on that make up Guile’s application programming interface (API), see
*note API Reference::.

4.1 Guile’s Implementation of Scheme
====================================

Guile’s core language is Scheme, which is specified and described in the
series of reports known as "RnRS". "RnRS" is shorthand for the
"Revised^n Report on the Algorithmic Language Scheme".  Guile complies
fully with R5RS (*note Introduction: (r5rs)Top.), and implements some
aspects of R6RS.

   Guile also has many extensions that go beyond these reports.  Some of
the areas where Guile extends R5RS are:

   • Guile’s interactive documentation system

   • Guile’s support for POSIX-compliant network programming

   • GOOPS – Guile’s framework for object oriented programming.

4.2 Invoking Guile
==================

Many features of Guile depend on and can be changed by information that
the user provides either before or when Guile is started.  Below is a
description of what information to provide and how to provide it.

4.2.1 Command-line Options
--------------------------

Here we describe Guile’s command-line processing in detail.  Guile
processes its arguments from left to right, recognizing the switches
described below.  For examples, see *note Scripting Examples::.

‘SCRIPT ARG...’
‘-s SCRIPT ARG...’
     By default, Guile will read a file named on the command line as a
     script.  Any command-line arguments ARG... following SCRIPT become
     the script’s arguments; the ‘command-line’ function returns a list
     of strings of the form ‘(SCRIPT ARG...)’.

     It is possible to name a file using a leading hyphen, for example,
     ‘-myfile.scm’.  In this case, the file name must be preceded by
     ‘-s’ to tell Guile that a (script) file is being named.

     Scripts are read and evaluated as Scheme source code just as the
     ‘load’ function would.  After loading SCRIPT, Guile exits.

‘-c EXPR ARG...’
     Evaluate EXPR as Scheme code, and then exit.  Any command-line
     arguments ARG... following EXPR become command-line arguments; the
     ‘command-line’ function returns a list of strings of the form
     ‘(GUILE ARG...)’, where GUILE is the path of the Guile executable.

‘-- ARG...’
     Run interactively, prompting the user for expressions and
     evaluating them.  Any command-line arguments ARG... following the
     ‘--’ become command-line arguments for the interactive session; the
     ‘command-line’ function returns a list of strings of the form
     ‘(GUILE ARG...)’, where GUILE is the path of the Guile executable.

‘-L DIRECTORY’
     Add DIRECTORY to the front of Guile’s module load path.  The given
     directories are searched in the order given on the command line and
     before any directories in the ‘GUILE_LOAD_PATH’ environment
     variable.  Paths added here are _not_ in effect during execution of
     the user’s ‘.guile’ file.

‘-C DIRECTORY’
     Like ‘-L’, but adjusts the load path for _compiled_ files.

‘-x EXTENSION’
     Add EXTENSION to the front of Guile’s load extension list (*note
     ‘%load-extensions’: Load Paths.).  The specified extensions are
     tried in the order given on the command line, and before the
     default load extensions.  Extensions added here are _not_ in effect
     during execution of the user’s ‘.guile’ file.

‘-l FILE’
     Load Scheme source code from FILE, and continue processing the
     command line.

‘-e FUNCTION’
     Make FUNCTION the "entry point" of the script.  After loading the
     script file (with ‘-s’) or evaluating the expression (with ‘-c’),
     apply FUNCTION to a list containing the program name and the
     command-line arguments—the list provided by the ‘command-line’
     function.

     A ‘-e’ switch can appear anywhere in the argument list, but Guile
     always invokes the FUNCTION as the _last_ action it performs.  This
     is weird, but because of the way script invocation works under
     POSIX, the ‘-s’ option must always come last in the list.

     The FUNCTION is most often a simple symbol that names a function
     that is defined in the script.  It can also be of the form ‘(@
     MODULE-NAME SYMBOL)’, and in that case, the symbol is looked up in
     the module named MODULE-NAME.

     For compatibility with some versions of Guile 1.4, you can also use
     the form ‘(symbol ...)’ (that is, a list of only symbols that
     doesn’t start with ‘@’), which is equivalent to ‘(@ (symbol ...)
     main)’, or ‘(symbol ...) symbol’ (that is, a list of only symbols
     followed by a symbol), which is equivalent to ‘(@ (symbol ...)
     symbol)’.  We recommend to use the equivalent forms directly since
     they correspond to the ‘(@ ...)’ read syntax that can be used in
     normal code.  See *note Using Guile Modules:: and *note Scripting
     Examples::.

‘-ds’
     Treat a final ‘-s’ option as if it occurred at this point in the
     command line; load the script here.

     This switch is necessary because, although the POSIX script
     invocation mechanism effectively requires the ‘-s’ option to appear
     last, the programmer may well want to run the script before other
     actions requested on the command line.  For examples, see *note
     Scripting Examples::.

‘\’
     Read more command-line arguments, starting from the second line of
     the script file.  *Note The Meta Switch::.

‘--use-srfi=LIST’
     The option ‘--use-srfi’ expects a comma-separated list of numbers,
     each representing a SRFI module to be loaded into the interpreter
     before evaluating a script file or starting the REPL. Additionally,
     the feature identifier for the loaded SRFIs is recognized by the
     procedure ‘cond-expand’ when this option is used.

     Here is an example that loads the modules SRFI-8 (’receive’) and
     SRFI-13 (’string library’) before the GUILE interpreter is started:

          guile --use-srfi=8,13

‘--debug’
     Start with the debugging virtual machine (VM) engine.  Using the
     debugging VM will enable support for VM hooks, which are needed for
     tracing, breakpoints, and accurate call counts when profiling.  The
     debugging VM is slower than the regular VM, though, by about ten
     percent.  *Note VM Hooks::, for more information.

     By default, the debugging VM engine is only used when entering an
     interactive session.  When executing a script with ‘-s’ or ‘-c’,
     the normal, faster VM is used by default.

‘--no-debug’
     Do not use the debugging VM engine, even when entering an
     interactive session.

     Note that, despite the name, Guile running with ‘--no-debug’ _does_
     support the usual debugging facilities, such as printing a detailed
     backtrace upon error.  The only difference with ‘--debug’ is lack
     of support for VM hooks and the facilities that build upon it (see
     above).

‘-q’
     Do not load the initialization file, ‘.guile’.  This option only
     has an effect when running interactively; running scripts does not
     load the ‘.guile’ file.  *Note Init File::.

‘--listen[=P]’
     While this program runs, listen on a local port or a path for REPL
     clients.  If P starts with a number, it is assumed to be a local
     port on which to listen.  If it starts with a forward slash, it is
     assumed to be a path to a UNIX domain socket on which to listen.

     If P is not given, the default is local port 37146.  If you look at
     it upside down, it almost spells “Guile”.  If you have netcat
     installed, you should be able to ‘nc localhost 37146’ and get a
     Guile prompt.  Alternately you can fire up Emacs and connect to the
     process; see *note Using Guile in Emacs:: for more details.

     Note that opening a port allows anyone who can connect to that
     port—in the TCP case, any local user—to do anything Guile can do,
     as the user that the Guile process is running as.  Do not use
     ‘--listen’ on multi-user machines.  Of course, if you do not pass
     ‘--listen’ to Guile, no port will be opened.

     That said, ‘--listen’ is great for interactive debugging and
     development.

‘--auto-compile’
     Compile source files automatically (default behavior).

‘--fresh-auto-compile’
     Treat the auto-compilation cache as invalid, forcing recompilation.

‘--no-auto-compile’
     Disable automatic source file compilation.

‘--language=LANG’
     For the remainder of the command line arguments, assume that files
     mentioned with ‘-l’ and expressions passed with ‘-c’ are written in
     LANG.  LANG must be the name of one of the languages supported by
     the compiler (*note Compiler Tower::).  When run interactively, set
     the REPL’s language to LANG (*note Using Guile Interactively::).

     The default language is ‘scheme’; other interesting values include
     ‘elisp’ (for Emacs Lisp), and ‘ecmascript’.

     The example below shows the evaluation of expressions in Scheme,
     Emacs Lisp, and ECMAScript:

          guile -c "(apply + '(1 2))"
          guile --language=elisp -c "(= (funcall (symbol-function '+) 1 2) 3)"
          guile --language=ecmascript -c '(function (x) { return x * x; })(2);'

     To load a file written in Scheme and one written in Emacs Lisp, and
     then start a Scheme REPL, type:

          guile -l foo.scm --language=elisp -l foo.el --language=scheme

‘-h, --help’
     Display help on invoking Guile, and then exit.

‘-v, --version’
     Display the current version of Guile, and then exit.

4.2.2 Environment Variables
---------------------------

The "environment" is a feature of the operating system; it consists of a
collection of variables with names and values.  Each variable is called
an "environment variable" (or, sometimes, a “shell variable”);
environment variable names are case-sensitive, and it is conventional to
use upper-case letters only.  The values are all text strings, even
those that are written as numerals.  (Note that here we are referring to
names and values that are defined in the operating system shell from
which Guile is invoked.  This is not the same as a Scheme environment
that is defined within a running instance of Guile.  For a description
of Scheme environments, *note About Environments::.)

   How to set environment variables before starting Guile depends on the
operating system and, especially, the shell that you are using.  For
example, here is how to tell Guile to provide detailed warning messages
about deprecated features by setting ‘GUILE_WARN_DEPRECATED’ using Bash:

     $ export GUILE_WARN_DEPRECATED="detailed"
     $ guile

Or, detailed warnings can be turned on for a single invocation using:

     $ env GUILE_WARN_DEPRECATED="detailed" guile

   If you wish to retrieve or change the value of the shell environment
variables that affect the run-time behavior of Guile from within a
running instance of Guile, see *note Runtime Environment::.

   Here are the environment variables that affect the run-time behavior
of Guile:

‘GUILE_AUTO_COMPILE’
     This is a flag that can be used to tell Guile whether or not to
     compile Scheme source files automatically.  Starting with Guile
     2.0, Scheme source files will be compiled automatically, by
     default.

     If a compiled (‘.go’) file corresponding to a ‘.scm’ file is not
     found or is not newer than the ‘.scm’ file, the ‘.scm’ file will be
     compiled on the fly, and the resulting ‘.go’ file stored away.  An
     advisory note will be printed on the console.

     Compiled files will be stored in the directory
     ‘$XDG_CACHE_HOME/guile/ccache’, where ‘XDG_CACHE_HOME’ defaults to
     the directory ‘$HOME/.cache’.  This directory will be created if it
     does not already exist.

     Note that this mechanism depends on the timestamp of the ‘.go’ file
     being newer than that of the ‘.scm’ file; if the ‘.scm’ or ‘.go’
     files are moved after installation, care should be taken to
     preserve their original timestamps.

     Set ‘GUILE_AUTO_COMPILE’ to zero (0), to prevent Scheme files from
     being compiled automatically.  Set this variable to “fresh” to tell
     Guile to compile Scheme files whether they are newer than the
     compiled files or not.

     *Note Compilation::.

‘GUILE_HISTORY’
     This variable names the file that holds the Guile REPL command
     history.  You can specify a different history file by setting this
     environment variable.  By default, the history file is
     ‘$HOME/.guile_history’.

‘GUILE_INSTALL_LOCALE’
     This is a flag that can be used to tell Guile whether or not to
     install the current locale at startup, via a call to ‘(setlocale
     LC_ALL "")’.  *Note Locales::, for more information on locales.

     You may explicitly indicate that you do not want to install the
     locale by setting ‘GUILE_INSTALL_LOCALE’ to ‘0’, or explicitly
     enable it by setting the variable to ‘1’.

     Usually, installing the current locale is the right thing to do.
     It allows Guile to correctly parse and print strings with non-ASCII
     characters.  However, for compatibility with previous Guile 2.0
     releases, this option is off by default.  The next stable release
     series of Guile (the 2.2 series) will install locales by default.

‘GUILE_STACK_SIZE’
     Guile currently has a limited stack size for Scheme computations.
     Attempting to call too many nested functions will signal an error.
     This is good to detect infinite recursion, but sometimes the limit
     is reached for normal computations.  This environment variable, if
     set to a positive integer, specifies the number of Scheme value
     slots to allocate for the stack.

     In the future we will implement stacks that can grow and shrink,
     but for now this hack will have to do.

‘GUILE_LOAD_COMPILED_PATH’
     This variable may be used to augment the path that is searched for
     compiled Scheme files (‘.go’ files) when loading.  Its value should
     be a colon-separated list of directories.  If it contains the
     special path component ‘...’ (ellipsis), then the default path is
     put in place of the ellipsis, otherwise the default path is placed
     at the end.  The result is stored in ‘%load-compiled-path’ (*note
     Load Paths::).

     Here is an example using the Bash shell that adds the current
     directory, ‘.’, and the relative directory ‘../my-library’ to
     ‘%load-compiled-path’:

          $ export GUILE_LOAD_COMPILED_PATH=".:../my-library"
          $ guile -c '(display %load-compiled-path) (newline)'
          (. ../my-library /usr/local/lib/guile/2.0/ccache)

‘GUILE_LOAD_PATH’
     This variable may be used to augment the path that is searched for
     Scheme files when loading.  Its value should be a colon-separated
     list of directories.  If it contains the special path component
     ‘...’ (ellipsis), then the default path is put in place of the
     ellipsis, otherwise the default path is placed at the end.  The
     result is stored in ‘%load-path’ (*note Load Paths::).

     Here is an example using the Bash shell that prepends the current
     directory to ‘%load-path’, and adds the relative directory
     ‘../srfi’ to the end:

          $ env GUILE_LOAD_PATH=".:...:../srfi" \
          guile -c '(display %load-path) (newline)'
          (. /usr/local/share/guile/2.0 \
          /usr/local/share/guile/site/2.0 \
          /usr/local/share/guile/site \
          /usr/local/share/guile \
          ../srfi)

     (Note: The line breaks, above, are for documentation purposes only,
     and not required in the actual example.)

‘GUILE_WARN_DEPRECATED’
     As Guile evolves, some features will be eliminated or replaced by
     newer features.  To help users migrate their code as this evolution
     occurs, Guile will issue warning messages about code that uses
     features that have been marked for eventual elimination.
     ‘GUILE_WARN_DEPRECATED’ can be set to “no” to tell Guile not to
     display these warning messages, or set to “detailed” to tell Guile
     to display more lengthy messages describing the warning.  *Note
     Deprecation::.

‘HOME’
     Guile uses the environment variable ‘HOME’, the name of your home
     directory, to locate various files, such as ‘.guile’ or
     ‘.guile_history’.

4.3 Guile Scripting
===================

Like AWK, Perl, or any shell, Guile can interpret script files.  A Guile
script is simply a file of Scheme code with some extra information at
the beginning which tells the operating system how to invoke Guile, and
then tells Guile how to handle the Scheme code.

4.3.1 The Top of a Script File
------------------------------

The first line of a Guile script must tell the operating system to use
Guile to evaluate the script, and then tell Guile how to go about doing
that.  Here is the simplest case:

   • The first two characters of the file must be ‘#!’.

     The operating system interprets this to mean that the rest of the
     line is the name of an executable that can interpret the script.
     Guile, however, interprets these characters as the beginning of a
     multi-line comment, terminated by the characters ‘!#’ on a line by
     themselves.  (This is an extension to the syntax described in R5RS,
     added to support shell scripts.)

   • Immediately after those two characters must come the full pathname
     to the Guile interpreter.  On most systems, this would be
     ‘/usr/local/bin/guile’.

   • Then must come a space, followed by a command-line argument to pass
     to Guile; this should be ‘-s’.  This switch tells Guile to run a
     script, instead of soliciting the user for input from the terminal.
     There are more elaborate things one can do here; see *note The Meta
     Switch::.

   • Follow this with a newline.

   • The second line of the script should contain only the characters
     ‘!#’ — just like the top of the file, but reversed.  The operating
     system never reads this far, but Guile treats this as the end of
     the comment begun on the first line by the ‘#!’ characters.

   • If this source code file is not ASCII or ISO-8859-1 encoded, a
     coding declaration such as ‘coding: utf-8’ should appear in a
     comment somewhere in the first five lines of the file: see *note
     Character Encoding of Source Files::.

   • The rest of the file should be a Scheme program.

   Guile reads the program, evaluating expressions in the order that
they appear.  Upon reaching the end of the file, Guile exits.

4.3.2 The Meta Switch
---------------------

Guile’s command-line switches allow the programmer to describe
reasonably complicated actions in scripts.  Unfortunately, the POSIX
script invocation mechanism only allows one argument to appear on the
‘#!’ line after the path to the Guile executable, and imposes arbitrary
limits on that argument’s length.  Suppose you wrote a script starting
like this:
     #!/usr/local/bin/guile -e main -s
     !#
     (define (main args)
       (map (lambda (arg) (display arg) (display " "))
            (cdr args))
       (newline))
   The intended meaning is clear: load the file, and then call ‘main’ on
the command-line arguments.  However, the system will treat everything
after the Guile path as a single argument — the string ‘"-e main -s"’ —
which is not what we want.

   As a workaround, the meta switch ‘\’ allows the Guile programmer to
specify an arbitrary number of options without patching the kernel.  If
the first argument to Guile is ‘\’, Guile will open the script file
whose name follows the ‘\’, parse arguments starting from the file’s
second line (according to rules described below), and substitute them
for the ‘\’ switch.

   Working in concert with the meta switch, Guile treats the characters
‘#!’ as the beginning of a comment which extends through the next line
containing only the characters ‘!#’.  This sort of comment may appear
anywhere in a Guile program, but it is most useful at the top of a file,
meshing magically with the POSIX script invocation mechanism.

   Thus, consider a script named ‘/u/jimb/ekko’ which starts like this:
     #!/usr/local/bin/guile \
     -e main -s
     !#
     (define (main args)
             (map (lambda (arg) (display arg) (display " "))
                  (cdr args))
             (newline))

   Suppose a user invokes this script as follows:
     $ /u/jimb/ekko a b c

   Here’s what happens:

   • the operating system recognizes the ‘#!’ token at the top of the
     file, and rewrites the command line to:
          /usr/local/bin/guile \ /u/jimb/ekko a b c
     This is the usual behavior, prescribed by POSIX.

   • When Guile sees the first two arguments, ‘\ /u/jimb/ekko’, it opens
     ‘/u/jimb/ekko’, parses the three arguments ‘-e’, ‘main’, and ‘-s’
     from it, and substitutes them for the ‘\’ switch.  Thus, Guile’s
     command line now reads:
          /usr/local/bin/guile -e main -s /u/jimb/ekko a b c

   • Guile then processes these switches: it loads ‘/u/jimb/ekko’ as a
     file of Scheme code (treating the first three lines as a comment),
     and then performs the application ‘(main "/u/jimb/ekko" "a" "b"
     "c")’.

   When Guile sees the meta switch ‘\’, it parses command-line argument
from the script file according to the following rules:

   • Each space character terminates an argument.  This means that two
     spaces in a row introduce an argument ‘""’.

   • The tab character is not permitted (unless you quote it with the
     backslash character, as described below), to avoid confusion.

   • The newline character terminates the sequence of arguments, and
     will also terminate a final non-empty argument.  (However, a
     newline following a space will not introduce a final empty-string
     argument; it only terminates the argument list.)

   • The backslash character is the escape character.  It escapes
     backslash, space, tab, and newline.  The ANSI C escape sequences
     like ‘\n’ and ‘\t’ are also supported.  These produce argument
     constituents; the two-character combination ‘\n’ doesn’t act like a
     terminating newline.  The escape sequence ‘\NNN’ for exactly three
     octal digits reads as the character whose ASCII code is NNN.  As
     above, characters produced this way are argument constituents.
     Backslash followed by other characters is not allowed.

4.3.3 Command Line Handling
---------------------------

The ability to accept and handle command line arguments is very
important when writing Guile scripts to solve particular problems, such
as extracting information from text files or interfacing with existing
command line applications.  This chapter describes how Guile makes
command line arguments available to a Guile script, and the utilities
that Guile provides to help with the processing of command line
arguments.

   When a Guile script is invoked, Guile makes the command line
arguments accessible via the procedure ‘command-line’, which returns the
arguments as a list of strings.

   For example, if the script

     #! /usr/local/bin/guile -s
     !#
     (write (command-line))
     (newline)

is saved in a file ‘cmdline-test.scm’ and invoked using the command line
‘./cmdline-test.scm bar.txt -o foo -frumple grob’, the output is

     ("./cmdline-test.scm" "bar.txt" "-o" "foo" "-frumple" "grob")

   If the script invocation includes a ‘-e’ option, specifying a
procedure to call after loading the script, Guile will call that
procedure with ‘(command-line)’ as its argument.  So a script that uses
‘-e’ doesn’t need to refer explicitly to ‘command-line’ in its code.
For example, the script above would have identical behaviour if it was
written instead like this:

     #! /usr/local/bin/guile \
     -e main -s
     !#
     (define (main args)
       (write args)
       (newline))

   (Note the use of the meta switch ‘\’ so that the script invocation
can include more than one Guile option: *Note The Meta Switch::.)

   These scripts use the ‘#!’ POSIX convention so that they can be
executed using their own file names directly, as in the example command
line ‘./cmdline-test.scm bar.txt -o foo -frumple grob’.  But they can
also be executed by typing out the implied Guile command line in full,
as in:

     $ guile -s ./cmdline-test.scm bar.txt -o foo -frumple grob

or

     $ guile -e main -s ./cmdline-test2.scm bar.txt -o foo -frumple grob

   Even when a script is invoked using this longer form, the arguments
that the script receives are the same as if it had been invoked using
the short form.  Guile ensures that the ‘(command-line)’ or ‘-e’
arguments are independent of how the script is invoked, by stripping off
the arguments that Guile itself processes.

   A script is free to parse and handle its command line arguments in
any way that it chooses.  Where the set of possible options and
arguments is complex, however, it can get tricky to extract all the
options, check the validity of given arguments, and so on.  This task
can be greatly simplified by taking advantage of the module ‘(ice-9
getopt-long)’, which is distributed with Guile, *Note getopt-long::.

4.3.4 Scripting Examples
------------------------

To start with, here are some examples of invoking Guile directly:

‘guile -- a b c’
     Run Guile interactively; ‘(command-line)’ will return
     ‘("/usr/local/bin/guile" "a" "b" "c")’.

‘guile -s /u/jimb/ex2 a b c’
     Load the file ‘/u/jimb/ex2’; ‘(command-line)’ will return
     ‘("/u/jimb/ex2" "a" "b" "c")’.

‘guile -c '(write %load-path) (newline)'’
     Write the value of the variable ‘%load-path’, print a newline, and
     exit.

‘guile -e main -s /u/jimb/ex4 foo’
     Load the file ‘/u/jimb/ex4’, and then call the function ‘main’,
     passing it the list ‘("/u/jimb/ex4" "foo")’.

‘guile -l first -ds -l last -s script’
     Load the files ‘first’, ‘script’, and ‘last’, in that order.  The
     ‘-ds’ switch says when to process the ‘-s’ switch.  For a more
     motivated example, see the scripts below.

   Here is a very simple Guile script:
     #!/usr/local/bin/guile -s
     !#
     (display "Hello, world!")
     (newline)
   The first line marks the file as a Guile script.  When the user
invokes it, the system runs ‘/usr/local/bin/guile’ to interpret the
script, passing ‘-s’, the script’s filename, and any arguments given to
the script as command-line arguments.  When Guile sees ‘-s SCRIPT’, it
loads SCRIPT.  Thus, running this program produces the output:
     Hello, world!

   Here is a script which prints the factorial of its argument:
     #!/usr/local/bin/guile -s
     !#
     (define (fact n)
       (if (zero? n) 1
         (* n (fact (- n 1)))))

     (display (fact (string->number (cadr (command-line)))))
     (newline)
   In action:
     $ ./fact 5
     120
     $

   However, suppose we want to use the definition of ‘fact’ in this file
from another script.  We can’t simply ‘load’ the script file, and then
use ‘fact’’s definition, because the script will try to compute and
display a factorial when we load it.  To avoid this problem, we might
write the script this way:

     #!/usr/local/bin/guile \
     -e main -s
     !#
     (define (fact n)
       (if (zero? n) 1
         (* n (fact (- n 1)))))

     (define (main args)
       (display (fact (string->number (cadr args))))
       (newline))
   This version packages the actions the script should perform in a
function, ‘main’.  This allows us to load the file purely for its
definitions, without any extraneous computation taking place.  Then we
used the meta switch ‘\’ and the entry point switch ‘-e’ to tell Guile
to call ‘main’ after loading the script.
     $ ./fact 50
     30414093201713378043612608166064768844377641568960512000000000000

   Suppose that we now want to write a script which computes the
‘choose’ function: given a set of M distinct objects, ‘(choose N M)’ is
the number of distinct subsets containing N objects each.  It’s easy to
write ‘choose’ given ‘fact’, so we might write the script this way:
     #!/usr/local/bin/guile \
     -l fact -e main -s
     !#
     (define (choose n m)
       (/ (fact m) (* (fact (- m n)) (fact n))))

     (define (main args)
       (let ((n (string->number (cadr args)))
             (m (string->number (caddr args))))
         (display (choose n m))
         (newline)))

   The command-line arguments here tell Guile to first load the file
‘fact’, and then run the script, with ‘main’ as the entry point.  In
other words, the ‘choose’ script can use definitions made in the ‘fact’
script.  Here are some sample runs:
     $ ./choose 0 4
     1
     $ ./choose 1 4
     4
     $ ./choose 2 4
     6
     $ ./choose 3 4
     4
     $ ./choose 4 4
     1
     $ ./choose 50 100
     100891344545564193334812497256

4.4 Using Guile Interactively
=============================

When you start up Guile by typing just ‘guile’, without a ‘-c’ argument
or the name of a script to execute, you get an interactive interpreter
where you can enter Scheme expressions, and Guile will evaluate them and
print the results for you.  Here are some simple examples.

     scheme@(guile-user)> (+ 3 4 5)
     $1 = 12
     scheme@(guile-user)> (display "Hello world!\n")
     Hello world!
     scheme@(guile-user)> (values 'a 'b)
     $2 = a
     $3 = b

This mode of use is called a "REPL", which is short for “Read-Eval-Print
Loop”, because the Guile interpreter first reads the expression that you
have typed, then evaluates it, and then prints the result.

   The prompt shows you what language and module you are in.  In this
case, the current language is ‘scheme’, and the current module is
‘(guile-user)’.  *Note Other Languages::, for more information on
Guile’s support for languages other than Scheme.

4.4.1 The Init File, ‘~/.guile’
-------------------------------

When run interactively, Guile will load a local initialization file from
‘~/.guile’.  This file should contain Scheme expressions for evaluation.

   This facility lets the user customize their interactive Guile
environment, pulling in extra modules or parameterizing the REPL
implementation.

   To run Guile without loading the init file, use the ‘-q’ command-line
option.

4.4.2 Readline
--------------

To make it easier for you to repeat and vary previously entered
expressions, or to edit the expression that you’re typing in, Guile can
use the GNU Readline library.  This is not enabled by default because of
licensing reasons, but all you need to activate Readline is the
following pair of lines.

     scheme@(guile-user)> (use-modules (ice-9 readline))
     scheme@(guile-user)> (activate-readline)

   It’s a good idea to put these two lines (without the
‘scheme@(guile-user)>’ prompts) in your ‘.guile’ file.  *Note Init
File::, for more on ‘.guile’.

4.4.3 Value History
-------------------

Just as Readline helps you to reuse a previous input line, "value
history" allows you to use the _result_ of a previous evaluation in a
new expression.  When value history is enabled, each evaluation result
is automatically assigned to the next in the sequence of variables ‘$1’,
‘$2’, ….  You can then use these variables in subsequent expressions.

     scheme@(guile-user)> (iota 10)
     $1 = (0 1 2 3 4 5 6 7 8 9)
     scheme@(guile-user)> (apply * (cdr $1))
     $2 = 362880
     scheme@(guile-user)> (sqrt $2)
     $3 = 602.3952191045344
     scheme@(guile-user)> (cons $2 $1)
     $4 = (362880 0 1 2 3 4 5 6 7 8 9)

   Value history is enabled by default, because Guile’s REPL imports the
‘(ice-9 history)’ module.  Value history may be turned off or on within
the repl, using the options interface:

     scheme@(guile-user)> ,option value-history #f
     scheme@(guile-user)> 'foo
     foo
     scheme@(guile-user)> ,option value-history #t
     scheme@(guile-user)> 'bar
     $5 = bar

   Note that previously recorded values are still accessible, even if
value history is off.  In rare cases, these references to past
computations can cause Guile to use too much memory.  One may clear
these values, possibly enabling garbage collection, via the
‘clear-value-history!’ procedure, described below.

   The programmatic interface to value history is in a module:

     (use-modules (ice-9 history))

 -- Scheme Procedure: value-history-enabled?
     Return true if value history is enabled, or false otherwise.

 -- Scheme Procedure: enable-value-history!
     Turn on value history, if it was off.

 -- Scheme Procedure: disable-value-history!
     Turn off value history, if it was on.

 -- Scheme Procedure: clear-value-history!
     Clear the value history.  If the stored values are not captured by
     some other data structure or closure, they may then be reclaimed by
     the garbage collector.

4.4.4 REPL Commands
-------------------

The REPL exists to read expressions, evaluate them, and then print their
results.  But sometimes one wants to tell the REPL to evaluate an
expression in a different way, or to do something else altogether.  A
user can affect the way the REPL works with a "REPL command".

   The previous section had an example of a command, in the form of
‘,option’.

     scheme@(guile-user)> ,option value-history #t

Commands are distinguished from expressions by their initial comma
(‘,’).  Since a comma cannot begin an expression in most languages, it
is an effective indicator to the REPL that the following text forms a
command, not an expression.

   REPL commands are convenient because they are always there.  Even if
the current module doesn’t have a binding for ‘pretty-print’, one can
always ‘,pretty-print’.

   The following sections document the various commands, grouped
together by functionality.  Many of the commands have abbreviations; see
the online help (‘,help’) for more information.

4.4.4.1 Help Commands
.....................

When Guile starts interactively, it notifies the user that help can be
had by typing ‘,help’.  Indeed, ‘help’ is a command, and a particularly
useful one, as it allows the user to discover the rest of the commands.

 -- REPL Command: help [‘all’ | group | ‘[-c]’ command]
     Show help.

     With one argument, tries to look up the argument as a group name,
     giving help on that group if successful.  Otherwise tries to look
     up the argument as a command, giving help on the command.

     If there is a command whose name is also a group name, use the ‘-c
     COMMAND’ form to give help on the command instead of the group.

     Without any argument, a list of help commands and command groups
     are displayed.

 -- REPL Command: show [topic]
     Gives information about Guile.

     With one argument, tries to show a particular piece of information;
     currently supported topics are ‘warranty’ (or ‘w’), ‘copying’ (or
     ‘c’), and ‘version’ (or ‘v’).

     Without any argument, a list of topics is displayed.

 -- REPL Command: apropos regexp
     Find bindings/modules/packages.

 -- REPL Command: describe obj
     Show description/documentation.

4.4.4.2 Module Commands
.......................

 -- REPL Command: module [module]
     Change modules / Show current module.

 -- REPL Command: import module …
     Import modules / List those imported.

 -- REPL Command: load file
     Load a file in the current module.

 -- REPL Command: reload [module]
     Reload the given module, or the current module if none was given.

 -- REPL Command: binding
     List current bindings.

 -- REPL Command: in module expression
 -- REPL Command: in module command arg …
     Evaluate an expression, or alternatively, execute another
     meta-command in the context of a module.  For example, ‘,in (foo
     bar) ,binding’ will show the bindings in the module ‘(foo bar)’.

4.4.4.3 Language Commands
.........................

 -- REPL Command: language language
     Change languages.

4.4.4.4 Compile Commands
........................

 -- REPL Command: compile exp
     Generate compiled code.

 -- REPL Command: compile-file file
     Compile a file.

 -- REPL Command: expand exp
     Expand any macros in a form.

 -- REPL Command: optimize exp
     Run the optimizer on a piece of code and print the result.

 -- REPL Command: disassemble exp
     Disassemble a compiled procedure.

 -- REPL Command: disassemble-file file
     Disassemble a file.

4.4.4.5 Profile Commands
........................

 -- REPL Command: time exp
     Time execution.

 -- REPL Command: profile exp
     Profile execution.

 -- REPL Command: trace exp [#:width w] [#:max-indent i]
     Trace execution.

     By default, the trace will limit its width to the width of your
     terminal, or WIDTH if specified.  Nested procedure invocations will
     be printed farther to the right, though if the width of the
     indentation passes the MAX-INDENT, the indentation is abbreviated.

4.4.4.6 Debug Commands
......................

These debugging commands are only available within a recursive REPL;
they do not work at the top level.

 -- REPL Command: backtrace [count] [#:width w] [#:full? f]
     Print a backtrace.

     Print a backtrace of all stack frames, or innermost COUNT frames.
     If COUNT is negative, the last COUNT frames will be shown.

 -- REPL Command: up [count]
     Select a calling stack frame.

     Select and print stack frames that called this one.  An argument
     says how many frames up to go.

 -- REPL Command: down [count]
     Select a called stack frame.

     Select and print stack frames called by this one.  An argument says
     how many frames down to go.

 -- REPL Command: frame [idx]
     Show a frame.

     Show the selected frame.  With an argument, select a frame by
     index, then show it.

 -- REPL Command: procedure
     Print the procedure for the selected frame.

 -- REPL Command: locals
     Show local variables.

     Show locally-bound variables in the selected frame.

 -- REPL Command: error-message
 -- REPL Command: error
     Show error message.

     Display the message associated with the error that started the
     current debugging REPL.

 -- REPL Command: registers
     Show the VM registers associated with the current frame.

     *Note Stack Layout::, for more information on VM stack frames.

 -- REPL Command: width [cols]
     Sets the number of display columns in the output of ‘,backtrace’
     and ‘,locals’ to COLS.  If COLS is not given, the width of the
     terminal is used.

   The next 3 commands work at any REPL.

 -- REPL Command: break proc
     Set a breakpoint at PROC.

 -- REPL Command: break-at-source file line
     Set a breakpoint at the given source location.

 -- REPL Command: tracepoint proc
     Set a tracepoint on the given procedure.  This will cause all calls
     to the procedure to print out a tracing message.  *Note Tracing
     Traps::, for more information.

   The rest of the commands in this subsection all apply only when the
stack is "continuable" — in other words when it makes sense for the
program that the stack comes from to continue running.  Usually this
means that the program stopped because of a trap or a breakpoint.

 -- REPL Command: step
     Tell the debugged program to step to the next source location.

 -- REPL Command: next
     Tell the debugged program to step to the next source location in
     the same frame.  (See *note Traps:: for the details of how this
     works.)

 -- REPL Command: finish
     Tell the program being debugged to continue running until the
     completion of the current stack frame, and at that time to print
     the result and reenter the REPL.

4.4.4.7 Inspect Commands
........................

 -- REPL Command: inspect exp
     Inspect the result(s) of evaluating EXP.

 -- REPL Command: pretty-print exp
     Pretty-print the result(s) of evaluating EXP.

4.4.4.8 System Commands
.......................

 -- REPL Command: gc
     Garbage collection.

 -- REPL Command: statistics
     Display statistics.

 -- REPL Command: option [name] [exp]
     With no arguments, lists all options.  With one argument, shows the
     current value of the NAME option.  With two arguments, sets the
     NAME option to the result of evaluating the Scheme expression EXP.

 -- REPL Command: quit
     Quit this session.

   Current REPL options include:

‘compile-options’
     The options used when compiling expressions entered at the REPL.
     *Note Compilation::, for more on compilation options.
‘interp’
     Whether to interpret or compile expressions given at the REPL, if
     such a choice is available.  Off by default (indicating
     compilation).
‘prompt’
     A customized REPL prompt.  ‘#f’ by default, indicating the default
     prompt.
‘print’
     A procedure of two arguments used to print the result of evaluating
     each expression.  The arguments are the current REPL and the value
     to print.  By default, ‘#f’, to use the default procedure.
‘value-history’
     Whether value history is on or not.  *Note Value History::.
‘on-error’
     What to do when an error happens.  By default, ‘debug’, meaning to
     enter the debugger.  Other values include ‘backtrace’, to show a
     backtrace without entering the debugger, or ‘report’, to simply
     show a short error printout.

   Default values for REPL options may be set using
‘repl-default-option-set!’ from ‘(system repl common)’:

 -- Scheme Procedure: repl-default-option-set! key value
     Set the default value of a REPL option.  This function is
     particularly useful in a user’s init file.  *Note Init File::.

4.4.5 Error Handling
--------------------

When code being evaluated from the REPL hits an error, Guile enters a
new prompt, allowing you to inspect the context of the error.

     scheme@(guile-user)> (map string-append '("a" "b") '("c" #\d))
     ERROR: In procedure string-append:
     ERROR: Wrong type (expecting string): #\d
     Entering a new prompt.  Type `,bt' for a backtrace or `,q' to continue.
     scheme@(guile-user) [1]>

   The new prompt runs inside the old one, in the dynamic context of the
error.  It is a recursive REPL, augmented with a reified representation
of the stack, ready for debugging.

   ‘,backtrace’ (abbreviated ‘,bt’) displays the Scheme call stack at
the point where the error occurred:

     scheme@(guile-user) [1]> ,bt
                1 (map #<procedure string-append _> ("a" "b") ("c" #\d))
                0 (string-append "b" #\d)

   In the above example, the backtrace doesn’t have much source
information, as ‘map’ and ‘string-append’ are both primitives.  But in
the general case, the space on the left of the backtrace indicates the
line and column in which a given procedure calls another.

   You can exit a recursive REPL in the same way that you exit any REPL:
via ‘(quit)’, ‘,quit’ (abbreviated ‘,q’), or ‘C-d’, among other options.

4.4.6 Interactive Debugging
---------------------------

A recursive debugging REPL exposes a number of other meta-commands that
inspect the state of the computation at the time of the error.  These
commands allow you to

   • display the Scheme call stack at the point where the error
     occurred;

   • move up and down the call stack, to see in detail the expression
     being evaluated, or the procedure being applied, in each "frame";
     and

   • examine the values of variables and expressions in the context of
     each frame.

*Note Debug Commands::, for documentation of the individual commands.
This section aims to give more of a walkthrough of a typical debugging
session.

   First, we’re going to need a good error.  Let’s try to macroexpand
the expression ‘(unquote foo)’, outside of a ‘quasiquote’ form, and see
how the macroexpander reports this error.

     scheme@(guile-user)> (macroexpand '(unquote foo))
     ERROR: In procedure macroexpand:
     ERROR: unquote: expression not valid outside of quasiquote in (unquote foo)
     Entering a new prompt.  Type `,bt' for a backtrace or `,q' to continue.
     scheme@(guile-user) [1]>

   The ‘backtrace’ command, which can also be invoked as ‘bt’, displays
the call stack (aka backtrace) at the point where the debugger was
entered:

     scheme@(guile-user) [1]> ,bt
     In ice-9/psyntax.scm:
       1130:21  3 (chi-top (unquote foo) () ((top)) e (eval) (hygiene #))
       1071:30  2 (syntax-type (unquote foo) () ((top)) #f #f (# #) #f)
       1368:28  1 (chi-macro #<procedure de9360 at ice-9/psyntax.scm...> ...)
     In unknown file:
                0 (scm-error syntax-error macroexpand "~a: ~a in ~a" # #f)

   A call stack consists of a sequence of stack "frames", with each
frame describing one procedure which is waiting to do something with the
values returned by another.  Here we see that there are four frames on
the stack.

   Note that ‘macroexpand’ is not on the stack – it must have made a
tail call to ‘chi-top’, as indeed we would find if we searched
‘ice-9/psyntax.scm’ for its definition.

   When you enter the debugger, the innermost frame is selected, which
means that the commands for getting information about the “current”
frame, or for evaluating expressions in the context of the current
frame, will do so by default with respect to the innermost frame.  To
select a different frame, so that these operations will apply to it
instead, use the ‘up’, ‘down’ and ‘frame’ commands like this:

     scheme@(guile-user) [1]> ,up
     In ice-9/psyntax.scm:
       1368:28  1 (chi-macro #<procedure de9360 at ice-9/psyntax.scm...> ...)
     scheme@(guile-user) [1]> ,frame 3
     In ice-9/psyntax.scm:
       1130:21  3 (chi-top (unquote foo) () ((top)) e (eval) (hygiene #))
     scheme@(guile-user) [1]> ,down
     In ice-9/psyntax.scm:
       1071:30  2 (syntax-type (unquote foo) () ((top)) #f #f (# #) #f)

   Perhaps we’re interested in what’s going on in frame 2, so we take a
look at its local variables:

     scheme@(guile-user) [1]> ,locals
       Local variables:
       $1 = e = (unquote foo)
       $2 = r = ()
       $3 = w = ((top))
       $4 = s = #f
       $5 = rib = #f
       $6 = mod = (hygiene guile-user)
       $7 = for-car? = #f
       $8 = first = unquote
       $9 = ftype = macro
       $10 = fval = #<procedure de9360 at ice-9/psyntax.scm:2817:2 (x)>
       $11 = fe = unquote
       $12 = fw = ((top))
       $13 = fs = #f
       $14 = fmod = (hygiene guile-user)

   All of the values are accessible by their value-history names (‘$N’):

     scheme@(guile-user) [1]> $10
     $15 = #<procedure de9360 at ice-9/psyntax.scm:2817:2 (x)>

   We can even invoke the procedure at the REPL directly:

     scheme@(guile-user) [1]> ($10 'not-going-to-work)
     ERROR: In procedure macroexpand:
     ERROR: source expression failed to match any pattern in not-going-to-work
     Entering a new prompt.  Type `,bt' for a backtrace or `,q' to continue.

   Well at this point we’ve caused an error within an error.  Let’s just
quit back to the top level:

     scheme@(guile-user) [2]> ,q
     scheme@(guile-user) [1]> ,q
     scheme@(guile-user)>

   Finally, as a word to the wise: hackers close their REPL prompts with
‘C-d’.

4.5 Using Guile in Emacs
========================

Any text editor can edit Scheme, but some are better than others.  Emacs
is the best, of course, and not just because it is a fine text editor.
Emacs has good support for Scheme out of the box, with sensible
indentation rules, parenthesis-matching, syntax highlighting, and even a
set of keybindings for structural editing, allowing navigation,
cut-and-paste, and transposition operations that work on balanced
S-expressions.

   As good as it is, though, two things will vastly improve your
experience with Emacs and Guile.

   The first is Taylor Campbell’s Paredit
(http://www.emacswiki.org/emacs/ParEdit).  You should not code in any
dialect of Lisp without Paredit.  (They say that unopinionated writing
is boring—hence this tone—but it’s the truth, regardless.)  Paredit is
the bee’s knees.

   The second is José Antonio Ortega Ruiz’s Geiser
(http://www.nongnu.org/geiser/).  Geiser complements Emacs’
‘scheme-mode’ with tight integration to running Guile processes via a
‘comint-mode’ REPL buffer.

   Of course there are keybindings to switch to the REPL, and a good
REPL environment, but Geiser goes beyond that, providing:

   • Form evaluation in the context of the current file’s module.
   • Macro expansion.
   • File/module loading and/or compilation.
   • Namespace-aware identifier completion (including local bindings,
     names visible in the current module, and module names).
   • Autodoc: the echo area shows information about the signature of the
     procedure/macro around point automatically.
   • Jump to definition of identifier at point.
   • Access to documentation (including docstrings when the
     implementation provides it).
   • Listings of identifiers exported by a given module.
   • Listings of callers/callees of procedures.
   • Rudimentary support for debugging and error navigation.
   • Support for multiple, simultaneous REPLs.

   See Geiser’s web page at <http://www.nongnu.org/geiser/>, for more
information.

4.6 Using Guile Tools
=====================

Guile also comes with a growing number of command-line utilities: a
compiler, a disassembler, some module inspectors, and in the future, a
system to install Guile packages from the internet.  These tools may be
invoked using the ‘guild’ program.

     $ guild compile -o foo.go foo.scm
     wrote `foo.go'

   This program used to be called ‘guile-tools’ up to Guile version
2.0.1, and for backward compatibility it still may be called as such.
However we changed the name to ‘guild’, not only because it is
pleasantly shorter and easier to read, but also because this tool will
serve to bind Guile wizards together, by allowing hackers to share code
with each other using a CPAN-like system.

   *Note Compilation::, for more on ‘guild compile’.

   A complete list of guild scripts can be had by invoking ‘guild list’,
or simply ‘guild’.

4.7 Installing Site Packages
============================

At some point, you will probably want to share your code with other
people.  To do so effectively, it is important to follow a set of common
conventions, to make it easy for the user to install and use your
package.

   The first thing to do is to install your Scheme files where Guile can
find them.  When Guile goes to find a Scheme file, it will search a
"load path" to find the file: first in Guile’s own path, then in paths
for "site packages".  A site package is any Scheme code that is
installed and not part of Guile itself.  *Note Load Paths::, for more on
load paths.

   There are several site paths, for historical reasons, but the one
that should generally be used can be obtained by invoking the
‘%site-dir’ procedure.  *Note Build Config::.  If Guile 2.0 is installed
on your system in ‘/usr/’, then ‘(%site-dir)’ will be
‘/usr/share/guile/site/2.0’.  Scheme files should be installed there.

   If you do not install compiled ‘.go’ files, Guile will compile your
modules and programs when they are first used, and cache them in the
user’s home directory.  *Note Compilation::, for more on
auto-compilation.  However, it is better to compile the files before
they are installed, and to just copy the files to a place that Guile can
find them.

   As with Scheme files, Guile searches a path to find compiled ‘.go’
files, the ‘%load-compiled-path’.  By default, this path has two
entries: a path for Guile’s files, and a path for site packages.  You
should install your ‘.go’ files into the latter directory, whose value
is returned by invoking the ‘%site-ccache-dir’ procedure.  As in the
previous example, if Guile 2.0 is installed on your system in ‘/usr/’,
then ‘(%site-ccache-dir)’ site packages will be
‘/usr/lib/guile/2.0/site-ccache’.

   Note that a ‘.go’ file will only be loaded in preference to a ‘.scm’
file if it is newer.  For that reason, you should install your Scheme
files first, and your compiled files second.  ‘Load Paths’, for more on
the loading process.

   Finally, although this section is only about Scheme, sometimes you
need to install C extensions too.  Shared libraries should be installed
in the "extensions dir".  This value can be had from the build config
(*note Build Config::).  Again, if Guile 2.0 is installed on your system
in ‘/usr/’, then the extensions dir will be
‘/usr/lib/guile/2.0/extensions’.

