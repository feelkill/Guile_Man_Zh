5 Programming in C
******************

This part of the manual explains the general concepts that you need to
understand when interfacing to Guile from C. You will learn about how
the latent typing of Scheme is embedded into the static typing of C, how
the garbage collection of Guile is made available to C code, and how
continuations influence the control flow in a C program.

   This knowledge should make it straightforward to add new functions to
Guile that can be called from Scheme.  Adding new data types is also
possible and is done by defining "smobs".

   The *note Programming Overview:: section of this part contains
general musings and guidelines about programming with Guile.  It
explores different ways to design a program around Guile, or how to
embed Guile into existing programs.

   For a pedagogical yet detailed explanation of how the data
representation of Guile is implemented, *Note Data Representation::.
You don’t need to know the details given there to use Guile from C, but
they are useful when you want to modify Guile itself or when you are
just curious about how it is all done.

   For detailed reference information on the variables, functions etc.
that make up Guile’s application programming interface (API), *Note API
Reference::.

5.1 Parallel Installations
==========================

Guile provides strong API and ABI stability guarantees during stable
series, so that if a user writes a program against Guile version 2.0.3,
it will be compatible with some future version 2.0.7.  We say in this
case that 2.0 is the "effective version", composed of the major and
minor versions, in this case 2 and 0.

   Users may install multiple effective versions of Guile, with each
version’s headers, libraries, and Scheme files under their own
directories.  This provides the necessary stability guarantee for users,
while also allowing Guile developers to evolve the language and its
implementation.

   However, parallel installability does have a down-side, in that users
need to know which version of Guile to ask for, when they build against
Guile.  Guile solves this problem by installing a file to be read by the
‘pkg-config’ utility, a tool to query installed packages by name.  Guile
encodes the version into its pkg-config name, so that users can ask for
‘guile-2.0’ or ‘guile-2.2’, as appropriate.

   For effective version 2.0, for example, you would invoke ‘pkg-config
--cflags --libs guile-2.0’ to get the compilation and linking flags
necessary to link to version 2.0 of Guile.  You would typically run
‘pkg-config’ during the configuration phase of your program and use the
obtained information in the Makefile.

   Guile’s ‘pkg-config’ file, ‘guile-2.0.pc’, defines additional useful
variables:

‘sitedir’
     The default directory where Guile looks for Scheme source and
     compiled files (*note %site-dir: Installing Site Packages.).  Run
     ‘pkg-config guile-2.0 --variable=sitedir’ to see its value.  *Note
     GUILE_SITE_DIR: Autoconf Macros, for more on how to use it from
     Autoconf.

‘extensiondir’
     The default directory where Guile looks for extensions—i.e., shared
     libraries providing additional features (*note Modules and
     Extensions::).  Run ‘pkg-config guile-2.0 --variable=extensiondir’
     to see its value.

See the ‘pkg-config’ man page, for more information, or its web site,
<http://pkg-config.freedesktop.org/>.  *Note Autoconf Support::, for
more on checking for Guile from within a ‘configure.ac’ file.

5.2 Linking Programs With Guile
===============================

This section covers the mechanics of linking your program with Guile on
a typical POSIX system.

   The header file ‘<libguile.h>’ provides declarations for all of
Guile’s functions and constants.  You should ‘#include’ it at the head
of any C source file that uses identifiers described in this manual.
Once you’ve compiled your source files, you need to link them against
the Guile object code library, ‘libguile’.

   As noted in the previous section, ‘<libguile.h>’ is not in the
default search path for headers.  The following command lines give
respectively the C compilation and link flags needed to build programs
using Guile 2.0:

     pkg-config guile-2.0 --cflags
     pkg-config guile-2.0 --libs

5.2.1 Guile Initialization Functions
------------------------------------

To initialize Guile, you can use one of several functions.  The first,
‘scm_with_guile’, is the most portable way to initialize Guile.  It will
initialize Guile when necessary and then call a function that you can
specify.  Multiple threads can call ‘scm_with_guile’ concurrently and it
can also be called more than once in a given thread.  The global state
of Guile will survive from one call of ‘scm_with_guile’ to the next.
Your function is called from within ‘scm_with_guile’ since the garbage
collector of Guile needs to know where the stack of each thread is.

   A second function, ‘scm_init_guile’, initializes Guile for the
current thread.  When it returns, you can use the Guile API in the
current thread.  This function employs some non-portable magic to learn
about stack bounds and might thus not be available on all platforms.

   One common way to use Guile is to write a set of C functions which
perform some useful task, make them callable from Scheme, and then link
the program with Guile.  This yields a Scheme interpreter just like
‘guile’, but augmented with extra functions for some specific
application — a special-purpose scripting language.

   In this situation, the application should probably process its
command-line arguments in the same manner as the stock Guile
interpreter.  To make that straightforward, Guile provides the
‘scm_boot_guile’ and ‘scm_shell’ function.

   For more about these functions, see *note Initialization::.

5.2.2 A Sample Guile Main Program
---------------------------------

Here is ‘simple-guile.c’, source code for a ‘main’ and an ‘inner_main’
function that will produce a complete Guile interpreter.

     /* simple-guile.c --- Start Guile from C.  */

     #include <libguile.h>

     static void
     inner_main (void *closure, int argc, char **argv)
     {
       /* preparation */
       scm_shell (argc, argv);
       /* after exit */
     }

     int
     main (int argc, char **argv)
     {
       scm_boot_guile (argc, argv, inner_main, 0);
       return 0; /* never reached, see inner_main */
     }

   The ‘main’ function calls ‘scm_boot_guile’ to initialize Guile,
passing it ‘inner_main’.  Once ‘scm_boot_guile’ is ready, it invokes
‘inner_main’, which calls ‘scm_shell’ to process the command-line
arguments in the usual way.

5.2.3 Building the Example with Make
------------------------------------

Here is a Makefile which you can use to compile the example program.  It
uses ‘pkg-config’ to learn about the necessary compiler and linker
flags.
     # Use GCC, if you have it installed.
     CC=gcc

     # Tell the C compiler where to find <libguile.h>
     CFLAGS=`pkg-config --cflags guile-2.0`

     # Tell the linker what libraries to use and where to find them.
     LIBS=`pkg-config --libs guile-2.0`

     simple-guile: simple-guile.o
             ${CC} simple-guile.o ${LIBS} -o simple-guile

     simple-guile.o: simple-guile.c
             ${CC} -c ${CFLAGS} simple-guile.c

5.2.4 Building the Example with Autoconf
----------------------------------------

If you are using the GNU Autoconf package to make your application more
portable, Autoconf will settle many of the details in the Makefile
automatically, making it much simpler and more portable; we recommend
using Autoconf with Guile.  Here is a ‘configure.ac’ file for
‘simple-guile’ that uses the standard ‘PKG_CHECK_MODULES’ macro to check
for Guile.  Autoconf will process this file into a ‘configure’ script.
We recommend invoking Autoconf via the ‘autoreconf’ utility.

     AC_INIT(simple-guile.c)

     # Find a C compiler.
     AC_PROG_CC

     # Check for Guile
     PKG_CHECK_MODULES([GUILE], [guile-2.0])

     # Generate a Makefile, based on the results.
     AC_OUTPUT(Makefile)

   Run ‘autoreconf -vif’ to generate ‘configure’.

   Here is a ‘Makefile.in’ template, from which the ‘configure’ script
produces a Makefile customized for the host system:
     # The configure script fills in these values.
     CC=@CC@
     CFLAGS=@GUILE_CFLAGS@
     LIBS=@GUILE_LIBS@

     simple-guile: simple-guile.o
             ${CC} simple-guile.o ${LIBS} -o simple-guile
     simple-guile.o: simple-guile.c
             ${CC} -c ${CFLAGS} simple-guile.c

   The developer should use Autoconf to generate the ‘configure’ script
from the ‘configure.ac’ template, and distribute ‘configure’ with the
application.  Here’s how a user might go about building the application:

     $ ls
     Makefile.in     configure*      configure.ac    simple-guile.c
     $ ./configure
     checking for gcc... ccache gcc
     checking whether the C compiler works... yes
     checking for C compiler default output file name... a.out
     checking for suffix of executables...
     checking whether we are cross compiling... no
     checking for suffix of object files... o
     checking whether we are using the GNU C compiler... yes
     checking whether ccache gcc accepts -g... yes
     checking for ccache gcc option to accept ISO C89... none needed
     checking for pkg-config... /usr/bin/pkg-config
     checking pkg-config is at least version 0.9.0... yes
     checking for GUILE... yes
     configure: creating ./config.status
     config.status: creating Makefile
     $ make
     [...]
     $ ./simple-guile
     guile> (+ 1 2 3)
     6
     guile> (getpwnam "jimb")
     #("jimb" "83Z7d75W2tyJQ" 4008 10 "Jim Blandy" "/u/jimb"
       "/usr/local/bin/bash")
     guile> (exit)
     $

5.3 Linking Guile with Libraries
================================

The previous section has briefly explained how to write programs that
make use of an embedded Guile interpreter.  But sometimes, all you want
to do is make new primitive procedures and data types available to the
Scheme programmer.  Writing a new version of ‘guile’ is inconvenient in
this case and it would in fact make the life of the users of your new
features needlessly hard.

   For example, suppose that there is a program ‘guile-db’ that is a
version of Guile with additional features for accessing a database.
People who want to write Scheme programs that use these features would
have to use ‘guile-db’ instead of the usual ‘guile’ program.  Now
suppose that there is also a program ‘guile-gtk’ that extends Guile with
access to the popular Gtk+ toolkit for graphical user interfaces.
People who want to write GUIs in Scheme would have to use ‘guile-gtk’.
Now, what happens when you want to write a Scheme application that uses
a GUI to let the user access a database?  You would have to write a
_third_ program that incorporates both the database stuff and the GUI
stuff.  This might not be easy (because ‘guile-gtk’ might be a quite
obscure program, say) and taking this example further makes it easy to
see that this approach can not work in practice.

   It would have been much better if both the database features and the
GUI feature had been provided as libraries that can just be linked with
‘guile’.  Guile makes it easy to do just this, and we encourage you to
make your extensions to Guile available as libraries whenever possible.

   You write the new primitive procedures and data types in the normal
fashion, and link them into a shared library instead of into a
stand-alone program.  The shared library can then be loaded dynamically
by Guile.

5.3.1 A Sample Guile Extension
------------------------------

This section explains how to make the Bessel functions of the C library
available to Scheme.  First we need to write the appropriate glue code
to convert the arguments and return values of the functions from Scheme
to C and back.  Additionally, we need a function that will add them to
the set of Guile primitives.  Because this is just an example, we will
only implement this for the ‘j0’ function.

   Consider the following file ‘bessel.c’.

     #include <math.h>
     #include <libguile.h>

     SCM
     j0_wrapper (SCM x)
     {
       return scm_from_double (j0 (scm_to_double (x)));
     }

     void
     init_bessel ()
     {
       scm_c_define_gsubr ("j0", 1, 0, 0, j0_wrapper);
     }

   This C source file needs to be compiled into a shared library.  Here
is how to do it on GNU/Linux:

     gcc `pkg-config --cflags guile-2.0` \
       -shared -o libguile-bessel.so -fPIC bessel.c

   For creating shared libraries portably, we recommend the use of GNU
Libtool (*note Introduction: (libtool)Top.).

   A shared library can be loaded into a running Guile process with the
function ‘load-extension’.  In addition to the name of the library to
load, this function also expects the name of a function from that
library that will be called to initialize it.  For our example, we are
going to call the function ‘init_bessel’ which will make ‘j0_wrapper’
available to Scheme programs with the name ‘j0’.  Note that we do not
specify a filename extension such as ‘.so’ when invoking
‘load-extension’.  The right extension for the host platform will be
provided automatically.

     (load-extension "libguile-bessel" "init_bessel")
     (j0 2)
     ⇒ 0.223890779141236

   For this to work, ‘load-extension’ must be able to find
‘libguile-bessel’, of course.  It will look in the places that are usual
for your operating system, and it will additionally look into the
directories listed in the ‘LTDL_LIBRARY_PATH’ environment variable.

   To see how these Guile extensions via shared libraries relate to the
module system, *Note Putting Extensions into Modules::.

5.4 General concepts for using libguile
=======================================

When you want to embed the Guile Scheme interpreter into your program or
library, you need to link it against the ‘libguile’ library (*note
Linking Programs With Guile::).  Once you have done this, your C code
has access to a number of data types and functions that can be used to
invoke the interpreter, or make new functions that you have written in C
available to be called from Scheme code, among other things.

   Scheme is different from C in a number of significant ways, and Guile
tries to make the advantages of Scheme available to C as well.  Thus, in
addition to a Scheme interpreter, libguile also offers dynamic types,
garbage collection, continuations, arithmetic on arbitrary sized
numbers, and other things.

   The two fundamental concepts are dynamic types and garbage
collection.  You need to understand how libguile offers them to C
programs in order to use the rest of libguile.  Also, the more general
control flow of Scheme caused by continuations needs to be dealt with.

   Running asynchronous signal handlers and multi-threading is known to
C code already, but there are of course a few additional rules when
using them together with libguile.

5.4.1 Dynamic Types
-------------------

Scheme is a dynamically-typed language; this means that the system
cannot, in general, determine the type of a given expression at compile
time.  Types only become apparent at run time.  Variables do not have
fixed types; a variable may hold a pair at one point, an integer at the
next, and a thousand-element vector later.  Instead, values, not
variables, have fixed types.

   In order to implement standard Scheme functions like ‘pair?’ and
‘string?’ and provide garbage collection, the representation of every
value must contain enough information to accurately determine its type
at run time.  Often, Scheme systems also use this information to
determine whether a program has attempted to apply an operation to an
inappropriately typed value (such as taking the ‘car’ of a string).

   Because variables, pairs, and vectors may hold values of any type,
Scheme implementations use a uniform representation for values — a
single type large enough to hold either a complete value or a pointer to
a complete value, along with the necessary typing information.

   In Guile, this uniform representation of all Scheme values is the C
type ‘SCM’.  This is an opaque type and its size is typically equivalent
to that of a pointer to ‘void’.  Thus, ‘SCM’ values can be passed around
efficiently and they take up reasonably little storage on their own.

   The most important rule is: You never access a ‘SCM’ value directly;
you only pass it to functions or macros defined in libguile.

   As an obvious example, although a ‘SCM’ variable can contain
integers, you can of course not compute the sum of two ‘SCM’ values by
adding them with the C ‘+’ operator.  You must use the libguile function
‘scm_sum’.

   Less obvious and therefore more important to keep in mind is that you
also cannot directly test ‘SCM’ values for trueness.  In Scheme, the
value ‘#f’ is considered false and of course a ‘SCM’ variable can
represent that value.  But there is no guarantee that the ‘SCM’
representation of ‘#f’ looks false to C code as well.  You need to use
‘scm_is_true’ or ‘scm_is_false’ to test a ‘SCM’ value for trueness or
falseness, respectively.

   You also can not directly compare two ‘SCM’ values to find out
whether they are identical (that is, whether they are ‘eq?’ in Scheme
terms).  You need to use ‘scm_is_eq’ for this.

   The one exception is that you can directly assign a ‘SCM’ value to a
‘SCM’ variable by using the C ‘=’ operator.

   The following (contrived) example shows how to do it right.  It
implements a function of two arguments (A and FLAG) that returns A+1 if
FLAG is true, else it returns A unchanged.

     SCM
     my_incrementing_function (SCM a, SCM flag)
     {
       SCM result;

       if (scm_is_true (flag))
         result = scm_sum (a, scm_from_int (1));
       else
         result = a;

       return result;
     }

   Often, you need to convert between ‘SCM’ values and appropriate C
values.  For example, we needed to convert the integer ‘1’ to its ‘SCM’
representation in order to add it to A.  Libguile provides many function
to do these conversions, both from C to ‘SCM’ and from ‘SCM’ to C.

   The conversion functions follow a common naming pattern: those that
make a ‘SCM’ value from a C value have names of the form ‘scm_from_TYPE
(…)’ and those that convert a ‘SCM’ value to a C value use the form
‘scm_to_TYPE (…)’.

   However, it is best to avoid converting values when you can.  When
you must combine C values and ‘SCM’ values in a computation, it is often
better to convert the C values to ‘SCM’ values and do the computation by
using libguile functions than to the other way around (converting ‘SCM’
to C and doing the computation some other way).

   As a simple example, consider this version of
‘my_incrementing_function’ from above:

     SCM
     my_other_incrementing_function (SCM a, SCM flag)
     {
       int result;

       if (scm_is_true (flag))
         result = scm_to_int (a) + 1;
       else
         result = scm_to_int (a);

       return scm_from_int (result);
     }

   This version is much less general than the original one: it will only
work for values A that can fit into a ‘int’.  The original function will
work for all values that Guile can represent and that ‘scm_sum’ can
understand, including integers bigger than ‘long long’, floating point
numbers, complex numbers, and new numerical types that have been added
to Guile by third-party libraries.

   Also, computing with ‘SCM’ is not necessarily inefficient.  Small
integers will be encoded directly in the ‘SCM’ value, for example, and
do not need any additional memory on the heap.  See *note Data
Representation:: to find out the details.

   Some special ‘SCM’ values are available to C code without needing to
convert them from C values:

Scheme value   C representation
#f             SCM_BOOL_F
#t             SCM_BOOL_T
()             SCM_EOL

   In addition to ‘SCM’, Guile also defines the related type
‘scm_t_bits’.  This is an unsigned integral type of sufficient size to
hold all information that is directly contained in a ‘SCM’ value.  The
‘scm_t_bits’ type is used internally by Guile to do all the bit
twiddling explained in *note Data Representation::, but you will
encounter it occasionally in low-level user code as well.

5.4.2 Garbage Collection
------------------------

As explained above, the ‘SCM’ type can represent all Scheme values.
Some values fit entirely into a ‘SCM’ value (such as small integers),
but other values require additional storage in the heap (such as strings
and vectors).  This additional storage is managed automatically by
Guile.  You don’t need to explicitly deallocate it when a ‘SCM’ value is
no longer used.

   Two things must be guaranteed so that Guile is able to manage the
storage automatically: it must know about all blocks of memory that have
ever been allocated for Scheme values, and it must know about all Scheme
values that are still being used.  Given this knowledge, Guile can
periodically free all blocks that have been allocated but are not used
by any active Scheme values.  This activity is called "garbage
collection".

   It is easy for Guile to remember all blocks of memory that it has
allocated for use by Scheme values, but you need to help it with finding
all Scheme values that are in use by C code.

   You do this when writing a SMOB mark function, for example (*note
Garbage Collecting Smobs::).  By calling this function, the garbage
collector learns about all references that your SMOB has to other ‘SCM’
values.

   Other references to ‘SCM’ objects, such as global variables of type
‘SCM’ or other random data structures in the heap that contain fields of
type ‘SCM’, can be made visible to the garbage collector by calling the
functions ‘scm_gc_protect’ or ‘scm_permanent_object’.  You normally use
these functions for long lived objects such as a hash table that is
stored in a global variable.  For temporary references in local
variables or function arguments, using these functions would be too
expensive.

   These references are handled differently: Local variables (and
function arguments) of type ‘SCM’ are automatically visible to the
garbage collector.  This works because the collector scans the stack for
potential references to ‘SCM’ objects and considers all referenced
objects to be alive.  The scanning considers each and every word of the
stack, regardless of what it is actually used for, and then decides
whether it could possibly be a reference to a ‘SCM’ object.  Thus, the
scanning is guaranteed to find all actual references, but it might also
find words that only accidentally look like references.  These ‘false
positives’ might keep ‘SCM’ objects alive that would otherwise be
considered dead.  While this might waste memory, keeping an object
around longer than it strictly needs to is harmless.  This is why this
technique is called “conservative garbage collection”.  In practice, the
wasted memory seems to be no problem.

   The stack of every thread is scanned in this way and the registers of
the CPU and all other memory locations where local variables or function
parameters might show up are included in this scan as well.

   The consequence of the conservative scanning is that you can just
declare local variables and function parameters of type ‘SCM’ and be
sure that the garbage collector will not free the corresponding objects.

   However, a local variable or function parameter is only protected as
long as it is really on the stack (or in some register).  As an
optimization, the C compiler might reuse its location for some other
value and the ‘SCM’ object would no longer be protected.  Normally, this
leads to exactly the right behavior: the compiler will only overwrite a
reference when it is no longer needed and thus the object becomes
unprotected precisely when the reference disappears, just as wanted.

   There are situations, however, where a ‘SCM’ object needs to be
around longer than its reference from a local variable or function
parameter.  This happens, for example, when you retrieve some pointer
from a smob and work with that pointer directly.  The reference to the
‘SCM’ smob object might be dead after the pointer has been retrieved,
but the pointer itself (and the memory pointed to) is still in use and
thus the smob object must be protected.  The compiler does not know
about this connection and might overwrite the ‘SCM’ reference too early.

   To get around this problem, you can use ‘scm_remember_upto_here_1’
and its cousins.  It will keep the compiler from overwriting the
reference.  For a typical example of its use, see *note Remembering
During Operations::.

5.4.3 Control Flow
------------------

Scheme has a more general view of program flow than C, both locally and
non-locally.

   Controlling the local flow of control involves things like gotos,
loops, calling functions and returning from them.  Non-local control
flow refers to situations where the program jumps across one or more
levels of function activations without using the normal call or return
operations.

   The primitive means of C for local control flow is the ‘goto’
statement, together with ‘if’.  Loops done with ‘for’, ‘while’ or ‘do’
could in principle be rewritten with just ‘goto’ and ‘if’.  In Scheme,
the primitive means for local control flow is the _function call_
(together with ‘if’).  Thus, the repetition of some computation in a
loop is ultimately implemented by a function that calls itself, that is,
by recursion.

   This approach is theoretically very powerful since it is easier to
reason formally about recursion than about gotos.  In C, using recursion
exclusively would not be practical, though, since it would eat up the
stack very quickly.  In Scheme, however, it is practical: function calls
that appear in a "tail position" do not use any additional stack space
(*note Tail Calls::).

   A function call is in a tail position when it is the last thing the
calling function does.  The value returned by the called function is
immediately returned from the calling function.  In the following
example, the call to ‘bar-1’ is in a tail position, while the call to
‘bar-2’ is not.  (The call to ‘1-’ in ‘foo-2’ is in a tail position,
though.)

     (define (foo-1 x)
       (bar-1 (1- x)))

     (define (foo-2 x)
       (1- (bar-2 x)))

   Thus, when you take care to recurse only in tail positions, the
recursion will only use constant stack space and will be as good as a
loop constructed from gotos.

   Scheme offers a few syntactic abstractions (‘do’ and "named" ‘let’)
that make writing loops slightly easier.

   But only Scheme functions can call other functions in a tail
position: C functions can not.  This matters when you have, say, two
functions that call each other recursively to form a common loop.  The
following (unrealistic) example shows how one might go about determining
whether a non-negative integer N is even or odd.

     (define (my-even? n)
       (cond ((zero? n) #t)
             (else (my-odd? (1- n)))))

     (define (my-odd? n)
       (cond ((zero? n) #f)
             (else (my-even? (1- n)))))

   Because the calls to ‘my-even?’ and ‘my-odd?’ are in tail positions,
these two procedures can be applied to arbitrary large integers without
overflowing the stack.  (They will still take a lot of time, of course.)

   However, when one or both of the two procedures would be rewritten in
C, it could no longer call its companion in a tail position (since C
does not have this concept).  You might need to take this consideration
into account when deciding which parts of your program to write in
Scheme and which in C.

   In addition to calling functions and returning from them, a Scheme
program can also exit non-locally from a function so that the control
flow returns directly to an outer level.  This means that some functions
might not return at all.

   Even more, it is not only possible to jump to some outer level of
control, a Scheme program can also jump back into the middle of a
function that has already exited.  This might cause some functions to
return more than once.

   In general, these non-local jumps are done by invoking
"continuations" that have previously been captured using
‘call-with-current-continuation’.  Guile also offers a slightly
restricted set of functions, ‘catch’ and ‘throw’, that can only be used
for non-local exits.  This restriction makes them more efficient.  Error
reporting (with the function ‘error’) is implemented by invoking
‘throw’, for example.  The functions ‘catch’ and ‘throw’ belong to the
topic of "exceptions".

   Since Scheme functions can call C functions and vice versa, C code
can experience the more general control flow of Scheme as well.  It is
possible that a C function will not return at all, or will return more
than once.  While C does offer ‘setjmp’ and ‘longjmp’ for non-local
exits, it is still an unusual thing for C code.  In contrast, non-local
exits are very common in Scheme, mostly to report errors.

   You need to be prepared for the non-local jumps in the control flow
whenever you use a function from ‘libguile’: it is best to assume that
any ‘libguile’ function might signal an error or run a pending signal
handler (which in turn can do arbitrary things).

   It is often necessary to take cleanup actions when the control leaves
a function non-locally.  Also, when the control returns non-locally,
some setup actions might be called for.  For example, the Scheme
function ‘with-output-to-port’ needs to modify the global state so that
‘current-output-port’ returns the port passed to ‘with-output-to-port’.
The global output port needs to be reset to its previous value when
‘with-output-to-port’ returns normally or when it is exited non-locally.
Likewise, the port needs to be set again when control enters
non-locally.

   Scheme code can use the ‘dynamic-wind’ function to arrange for the
setting and resetting of the global state.  C code can use the
corresponding ‘scm_internal_dynamic_wind’ function, or a
‘scm_dynwind_begin’/‘scm_dynwind_end’ pair together with suitable
’dynwind actions’ (*note Dynamic Wind::).

   Instead of coping with non-local control flow, you can also prevent
it by erecting a _continuation barrier_, *Note Continuation Barriers::.
The function ‘scm_c_with_continuation_barrier’, for example, is
guaranteed to return exactly once.

5.4.4 Asynchronous Signals
--------------------------

You can not call libguile functions from handlers for POSIX signals, but
you can register Scheme handlers for POSIX signals such as ‘SIGINT’.
These handlers do not run during the actual signal delivery.  Instead,
they are run when the program (more precisely, the thread that the
handler has been registered for) reaches the next _safe point_.

   The libguile functions themselves have many such safe points.
Consequently, you must be prepared for arbitrary actions anytime you
call a libguile function.  For example, even ‘scm_cons’ can contain a
safe point and when a signal handler is pending for your thread, calling
‘scm_cons’ will run this handler and anything might happen, including a
non-local exit although ‘scm_cons’ would not ordinarily do such a thing
on its own.

   If you do not want to allow the running of asynchronous signal
handlers, you can block them temporarily with
‘scm_dynwind_block_asyncs’, for example.  See *Note System asyncs::.

   Since signal handling in Guile relies on safe points, you need to
make sure that your functions do offer enough of them.  Normally,
calling libguile functions in the normal course of action is all that is
needed.  But when a thread might spent a long time in a code section
that calls no libguile function, it is good to include explicit safe
points.  This can allow the user to interrupt your code with <C-c>, for
example.

   You can do this with the macro ‘SCM_TICK’.  This macro is
syntactically a statement.  That is, you could use it like this:

     while (1)
       {
         SCM_TICK;
         do_some_work ();
       }

   Frequent execution of a safe point is even more important in multi
threaded programs, *Note Multi-Threading::.

5.4.5 Multi-Threading
---------------------

Guile can be used in multi-threaded programs just as well as in
single-threaded ones.

   Each thread that wants to use functions from libguile must put itself
into _guile mode_ and must then follow a few rules.  If it doesn’t want
to honor these rules in certain situations, a thread can temporarily
leave guile mode (but can no longer use libguile functions during that
time, of course).

   Threads enter guile mode by calling ‘scm_with_guile’,
‘scm_boot_guile’, or ‘scm_init_guile’.  As explained in the reference
documentation for these functions, Guile will then learn about the stack
bounds of the thread and can protect the ‘SCM’ values that are stored in
local variables.  When a thread puts itself into guile mode for the
first time, it gets a Scheme representation and is listed by
‘all-threads’, for example.

   Threads in guile mode can block (e.g., do blocking I/O) without
causing any problems(1); temporarily leaving guile mode with
‘scm_without_guile’ before blocking slightly improves GC performance,
though.  For some common blocking operations, Guile provides convenience
functions.  For example, if you want to lock a pthread mutex while in
guile mode, you might want to use ‘scm_pthread_mutex_lock’ which is just
like ‘pthread_mutex_lock’ except that it leaves guile mode while
blocking.

   All libguile functions are (intended to be) robust in the face of
multiple threads using them concurrently.  This means that there is no
risk of the internal data structures of libguile becoming corrupted in
such a way that the process crashes.

   A program might still produce nonsensical results, though.  Taking
hashtables as an example, Guile guarantees that you can use them from
multiple threads concurrently and a hashtable will always remain a valid
hashtable and Guile will not crash when you access it.  It does not
guarantee, however, that inserting into it concurrently from two threads
will give useful results: only one insertion might actually happen, none
might happen, or the table might in general be modified in a totally
arbitrary manner.  (It will still be a valid hashtable, but not the one
that you might have expected.)  Guile might also signal an error when it
detects a harmful race condition.

   Thus, you need to put in additional synchronizations when multiple
threads want to use a single hashtable, or any other mutable Scheme
object.

   When writing C code for use with libguile, you should try to make it
robust as well.  An example that converts a list into a vector will help
to illustrate.  Here is a correct version:

     SCM
     my_list_to_vector (SCM list)
     {
       SCM vector = scm_make_vector (scm_length (list), SCM_UNDEFINED);
       size_t len, i;

       len = scm_c_vector_length (vector);
       i = 0;
       while (i < len && scm_is_pair (list))
         {
           scm_c_vector_set_x (vector, i, scm_car (list));
           list = scm_cdr (list);
           i++;
         }

       return vector;
     }

   The first thing to note is that storing into a ‘SCM’ location
concurrently from multiple threads is guaranteed to be robust: you don’t
know which value wins but it will in any case be a valid ‘SCM’ value.

   But there is no guarantee that the list referenced by LIST is not
modified in another thread while the loop iterates over it.  Thus, while
copying its elements into the vector, the list might get longer or
shorter.  For this reason, the loop must check both that it doesn’t
overrun the vector and that it doesn’t overrun the list.  Otherwise,
‘scm_c_vector_set_x’ would raise an error if the index is out of range,
and ‘scm_car’ and ‘scm_cdr’ would raise an error if the value is not a
pair.

   It is safe to use ‘scm_car’ and ‘scm_cdr’ on the local variable LIST
once it is known that the variable contains a pair.  The contents of the
pair might change spontaneously, but it will always stay a valid pair
(and a local variable will of course not spontaneously point to a
different Scheme object).

   Likewise, a vector such as the one returned by ‘scm_make_vector’ is
guaranteed to always stay the same length so that it is safe to only use
scm_c_vector_length once and store the result.  (In the example, VECTOR
is safe anyway since it is a fresh object that no other thread can
possibly know about until it is returned from ‘my_list_to_vector’.)

   Of course the behavior of ‘my_list_to_vector’ is suboptimal when LIST
does indeed get asynchronously lengthened or shortened in another
thread.  But it is robust: it will always return a valid vector.  That
vector might be shorter than expected, or its last elements might be
unspecified, but it is a valid vector and if a program wants to rule out
these cases, it must avoid modifying the list asynchronously.

   Here is another version that is also correct:

     SCM
     my_pedantic_list_to_vector (SCM list)
     {
       SCM vector = scm_make_vector (scm_length (list), SCM_UNDEFINED);
       size_t len, i;

       len = scm_c_vector_length (vector);
       i = 0;
       while (i < len)
         {
           scm_c_vector_set_x (vector, i, scm_car (list));
           list = scm_cdr (list);
           i++;
         }

       return vector;
     }

   This version relies on the error-checking behavior of ‘scm_car’ and
‘scm_cdr’.  When the list is shortened (that is, when LIST holds a
non-pair), ‘scm_car’ will throw an error.  This might be preferable to
just returning a half-initialized vector.

   The API for accessing vectors and arrays of various kinds from C
takes a slightly different approach to thread-robustness.  In order to
get at the raw memory that stores the elements of an array, you need to
_reserve_ that array as long as you need the raw memory.  During the
time an array is reserved, its elements can still spontaneously change
their values, but the memory itself and other things like the size of
the array are guaranteed to stay fixed.  Any operation that would change
these parameters of an array that is currently reserved will signal an
error.  In order to avoid these errors, a program should of course put
suitable synchronization mechanisms in place.  As you can see, Guile
itself is again only concerned about robustness, not about correctness:
without proper synchronization, your program will likely not be correct,
but the worst consequence is an error message.

   Real thread-safety often requires that a critical section of code is
executed in a certain restricted manner.  A common requirement is that
the code section is not entered a second time when it is already being
executed.  Locking a mutex while in that section ensures that no other
thread will start executing it, blocking asyncs ensures that no
asynchronous code enters the section again from the current thread, and
the error checking of Guile mutexes guarantees that an error is
signalled when the current thread accidentally reenters the critical
section via recursive function calls.

   Guile provides two mechanisms to support critical sections as
outlined above.  You can either use the macros
‘SCM_CRITICAL_SECTION_START’ and ‘SCM_CRITICAL_SECTION_END’ for very
simple sections; or use a dynwind context together with a call to
‘scm_dynwind_critical_section’.

   The macros only work reliably for critical sections that are
guaranteed to not cause a non-local exit.  They also do not detect an
accidental reentry by the current thread.  Thus, you should probably
only use them to delimit critical sections that do not contain calls to
libguile functions or to other external functions that might do
complicated things.

   The function ‘scm_dynwind_critical_section’, on the other hand, will
correctly deal with non-local exits because it requires a dynwind
context.  Also, by using a separate mutex for each critical section, it
can detect accidental reentries.

   ---------- Footnotes ----------

   (1) In Guile 1.8, a thread blocking in guile mode would prevent
garbage collection to occur.  Thus, threads had to leave guile mode
whenever they could block.  This is no longer needed with Guile 2.0.

5.5 Defining New Types (Smobs)
==============================

"Smobs" are Guile’s mechanism for adding new primitive types to the
system.  The term “smob” was coined by Aubrey Jaffer, who says it comes
from “small object”, referring to the fact that they are quite limited
in size: they can hold just one pointer to a larger memory block plus 16
extra bits.

   To define a new smob type, the programmer provides Guile with some
essential information about the type — how to print it, how to garbage
collect it, and so on — and Guile allocates a fresh type tag for it.
The programmer can then use ‘scm_c_define_gsubr’ to make a set of C
functions visible to Scheme code that create and operate on these
objects.

   (You can find a complete version of the example code used in this
section in the Guile distribution, in ‘doc/example-smob’.  That
directory includes a makefile and a suitable ‘main’ function, so you can
build a complete interactive Guile shell, extended with the datatypes
described here.)

5.5.1 Describing a New Type
---------------------------

To define a new type, the programmer must write two functions to manage
instances of the type:

‘print’
     Guile will apply this function to each instance of the new type to
     print the value, as for ‘display’ or ‘write’.  The default print
     function prints ‘#<NAME ADDRESS>’ where ‘NAME’ is the first
     argument passed to ‘scm_make_smob_type’.

‘equalp’
     If Scheme code asks the ‘equal?’ function to compare two instances
     of the same smob type, Guile calls this function.  It should return
     ‘SCM_BOOL_T’ if A and B should be considered ‘equal?’, or
     ‘SCM_BOOL_F’ otherwise.  If ‘equalp’ is ‘NULL’, ‘equal?’ will
     assume that two instances of this type are never ‘equal?’ unless
     they are ‘eq?’.

   When the only resource associated with a smob is memory managed by
the garbage collector—i.e., memory allocated with the ‘scm_gc_malloc’
functions—this is sufficient.  However, when a smob is associated with
other kinds of resources, it may be necessary to define one of the
following functions, or both:

‘mark’
     Guile will apply this function to each instance of the new type it
     encounters during garbage collection.  This function is responsible
     for telling the collector about any other ‘SCM’ values that the
     object has stored, and that are in memory regions not already
     scanned by the garbage collector.  *Note Garbage Collecting
     Smobs::, for more details.

‘free’
     Guile will apply this function to each instance of the new type
     that is to be deallocated.  The function should release all
     resources held by the object.  This is analogous to the Java
     finalization method—it is invoked at an unspecified time (when
     garbage collection occurs) after the object is dead.  *Note Garbage
     Collecting Smobs::, for more details.

     This function operates while the heap is in an inconsistent state
     and must therefore be careful.  *Note Smobs::, for details about
     what this function is allowed to do.

   To actually register the new smob type, call ‘scm_make_smob_type’.
It returns a value of type ‘scm_t_bits’ which identifies the new smob
type.

   The four special functions described above are registered by calling
one of ‘scm_set_smob_mark’, ‘scm_set_smob_free’, ‘scm_set_smob_print’,
or ‘scm_set_smob_equalp’, as appropriate.  Each function is intended to
be used at most once per type, and the call should be placed immediately
following the call to ‘scm_make_smob_type’.

   There can only be at most 256 different smob types in the system.
Instead of registering a huge number of smob types (for example, one for
each relevant C struct in your application), it is sometimes better to
register just one and implement a second layer of type dispatching on
top of it.  This second layer might use the 16 extra bits to extend its
type, for example.

   Here is how one might declare and register a new type representing
eight-bit gray-scale images:

     #include <libguile.h>

     struct image {
       int width, height;
       char *pixels;

       /* The name of this image */
       SCM name;

       /* A function to call when this image is
          modified, e.g., to update the screen,
          or SCM_BOOL_F if no action necessary */
       SCM update_func;
     };

     static scm_t_bits image_tag;

     void
     init_image_type (void)
     {
       image_tag = scm_make_smob_type ("image", sizeof (struct image));
       scm_set_smob_mark (image_tag, mark_image);
       scm_set_smob_free (image_tag, free_image);
       scm_set_smob_print (image_tag, print_image);
     }

5.5.2 Creating Smob Instances
-----------------------------

Normally, smobs can have one _immediate_ word of data.  This word stores
either a pointer to an additional memory block that holds the real data,
or it might hold the data itself when it fits.  The word is large enough
for a ‘SCM’ value, a pointer to ‘void’, or an integer that fits into a
‘size_t’ or ‘ssize_t’.

   You can also create smobs that have two or three immediate words, and
when these words suffice to store all data, it is more efficient to use
these super-sized smobs instead of using a normal smob plus a memory
block.  *Note Double Smobs::, for their discussion.

   Guile provides functions for managing memory which are often helpful
when implementing smobs.  *Note Memory Blocks::.

   To retrieve the immediate word of a smob, you use the macro
‘SCM_SMOB_DATA’.  It can be set with ‘SCM_SET_SMOB_DATA’.  The 16 extra
bits can be accessed with ‘SCM_SMOB_FLAGS’ and ‘SCM_SET_SMOB_FLAGS’.

   The two macros ‘SCM_SMOB_DATA’ and ‘SCM_SET_SMOB_DATA’ treat the
immediate word as if it were of type ‘scm_t_bits’, which is an unsigned
integer type large enough to hold a pointer to ‘void’.  Thus you can use
these macros to store arbitrary pointers in the smob word.

   When you want to store a ‘SCM’ value directly in the immediate word
of a smob, you should use the macros ‘SCM_SMOB_OBJECT’ and
‘SCM_SET_SMOB_OBJECT’ to access it.

   Creating a smob instance can be tricky when it consists of multiple
steps that allocate resources.  Most of the time, this is mainly about
allocating memory to hold associated data structures.  Using memory
managed by the garbage collector simplifies things: the garbage
collector will automatically scan those data structures for pointers,
and reclaim them when they are no longer referenced.

   Continuing the example from above, if the global variable ‘image_tag’
contains a tag returned by ‘scm_make_smob_type’, here is how we could
construct a smob whose immediate word contains a pointer to a freshly
allocated ‘struct image’:

     SCM
     make_image (SCM name, SCM s_width, SCM s_height)
     {
       SCM smob;
       struct image *image;
       int width = scm_to_int (s_width);
       int height = scm_to_int (s_height);

       /* Step 1: Allocate the memory block.
        */
       image = (struct image *)
          scm_gc_malloc (sizeof (struct image), "image");

       /* Step 2: Initialize it with straight code.
        */
       image->width = width;
       image->height = height;
       image->pixels = NULL;
       image->name = SCM_BOOL_F;
       image->update_func = SCM_BOOL_F;

       /* Step 3: Create the smob.
        */
       smob = scm_new_smob (image_tag, image);

       /* Step 4: Finish the initialization.
        */
       image->name = name;
       image->pixels =
         scm_gc_malloc_pointerless (width * height, "image pixels");

       return smob;
     }

   We use ‘scm_gc_malloc_pointerless’ for the pixel buffer to tell the
garbage collector not to scan it for pointers.  Calls to
‘scm_gc_malloc’, ‘scm_new_smob’, and ‘scm_gc_malloc_pointerless’ raise
an exception in out-of-memory conditions; the garbage collector is able
to reclaim previously allocated memory if that happens.

5.5.3 Type checking
-------------------

Functions that operate on smobs should check that the passed ‘SCM’ value
indeed is a suitable smob before accessing its data.  They can do this
with ‘scm_assert_smob_type’.

   For example, here is a simple function that operates on an image
smob, and checks the type of its argument.

     SCM
     clear_image (SCM image_smob)
     {
       int area;
       struct image *image;

       scm_assert_smob_type (image_tag, image_smob);

       image = (struct image *) SCM_SMOB_DATA (image_smob);
       area = image->width * image->height;
       memset (image->pixels, 0, area);

       /* Invoke the image's update function.
        */
       if (scm_is_true (image->update_func))
         scm_call_0 (image->update_func);

       scm_remember_upto_here_1 (image_smob);

       return SCM_UNSPECIFIED;
     }

   See *note Remembering During Operations:: for an explanation of the
call to ‘scm_remember_upto_here_1’.

5.5.4 Garbage Collecting Smobs
------------------------------

Once a smob has been released to the tender mercies of the Scheme
system, it must be prepared to survive garbage collection.  In the
example above, all the memory associated with the smob is managed by the
garbage collector because we used the ‘scm_gc_’ allocation functions.
Thus, no special care must be taken: the garbage collector automatically
scans them and reclaims any unused memory.

   However, when data associated with a smob is managed in some other
way—e.g., ‘malloc’’d memory or file descriptors—it is possible to
specify a _free_ function to release those resources when the smob is
reclaimed, and a _mark_ function to mark Scheme objects otherwise
invisible to the garbage collector.

   As described in more detail elsewhere (*note Conservative GC::),
every object in the Scheme system has a "mark bit", which the garbage
collector uses to tell live objects from dead ones.  When collection
starts, every object’s mark bit is clear.  The collector traces pointers
through the heap, starting from objects known to be live, and sets the
mark bit on each object it encounters.  When it can find no more
unmarked objects, the collector walks all objects, live and dead, frees
those whose mark bits are still clear, and clears the mark bit on the
others.

   The two main portions of the collection are called the "mark phase",
during which the collector marks live objects, and the "sweep phase",
during which the collector frees all unmarked objects.

   The mark bit of a smob lives in a special memory region.  When the
collector encounters a smob, it sets the smob’s mark bit, and uses the
smob’s type tag to find the appropriate _mark_ function for that smob.
It then calls this _mark_ function, passing it the smob as its only
argument.

   The _mark_ function is responsible for marking any other Scheme
objects the smob refers to.  If it does not do so, the objects’ mark
bits will still be clear when the collector begins to sweep, and the
collector will free them.  If this occurs, it will probably break, or at
least confuse, any code operating on the smob; the smob’s ‘SCM’ values
will have become dangling references.

   To mark an arbitrary Scheme object, the _mark_ function calls
‘scm_gc_mark’.

   Thus, here is how we might write ‘mark_image’—again this is not
needed in our example since we used the ‘scm_gc_’ allocation routines,
so this is just for the sake of illustration:

     SCM
     mark_image (SCM image_smob)
     {
       /* Mark the image's name and update function.  */
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_gc_mark (image->name);
       scm_gc_mark (image->update_func);

       return SCM_BOOL_F;
     }

   Note that, even though the image’s ‘update_func’ could be an
arbitrarily complex structure (representing a procedure and any values
enclosed in its environment), ‘scm_gc_mark’ will recurse as necessary to
mark all its components.  Because ‘scm_gc_mark’ sets an object’s mark
bit before it recurses, it is not confused by circular structures.

   As an optimization, the collector will mark whatever value is
returned by the _mark_ function; this helps limit depth of recursion
during the mark phase.  Thus, the code above should really be written
as:
     SCM
     mark_image (SCM image_smob)
     {
       /* Mark the image's name and update function.  */
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_gc_mark (image->name);
       return image->update_func;
     }

   Finally, when the collector encounters an unmarked smob during the
sweep phase, it uses the smob’s tag to find the appropriate _free_
function for the smob.  It then calls that function, passing it the smob
as its only argument.

   The _free_ function must release any resources used by the smob.
However, it must not free objects managed by the collector; the
collector will take care of them.  For historical reasons, the return
type of the _free_ function should be ‘size_t’, an unsigned integral
type; the _free_ function should always return zero.

   Here is how we might write the ‘free_image’ function for the image
smob type—again for the sake of illustration, since our example does not
need it thanks to the use of the ‘scm_gc_’ allocation routines:
     size_t
     free_image (SCM image_smob)
     {
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_gc_free (image->pixels,
                    image->width * image->height,
                    "image pixels");
       scm_gc_free (image, sizeof (struct image), "image");

       return 0;
     }

   During the sweep phase, the garbage collector will clear the mark
bits on all live objects.  The code which implements a smob need not do
this itself.

   There is no way for smob code to be notified when collection is
complete.

   It is usually a good idea to minimize the amount of processing done
during garbage collection; keep the _mark_ and _free_ functions very
simple.  Since collections occur at unpredictable times, it is easy for
any unusual activity to interfere with normal code.

5.5.5 Remembering During Operations
-----------------------------------

It’s important that a smob is visible to the garbage collector whenever
its contents are being accessed.  Otherwise it could be freed while code
is still using it.

   For example, consider a procedure to convert image data to a list of
pixel values.

     SCM
     image_to_list (SCM image_smob)
     {
       struct image *image;
       SCM lst;
       int i;

       scm_assert_smob_type (image_tag, image_smob);

       image = (struct image *) SCM_SMOB_DATA (image_smob);
       lst = SCM_EOL;
       for (i = image->width * image->height - 1; i >= 0; i--)
         lst = scm_cons (scm_from_char (image->pixels[i]), lst);

       scm_remember_upto_here_1 (image_smob);
       return lst;
     }

   In the loop, only the ‘image’ pointer is used and the C compiler has
no reason to keep the ‘image_smob’ value anywhere.  If ‘scm_cons’
results in a garbage collection, ‘image_smob’ might not be on the stack
or anywhere else and could be freed, leaving the loop accessing freed
data.  The use of ‘scm_remember_upto_here_1’ prevents this, by creating
a reference to ‘image_smob’ after all data accesses.

   There’s no need to do the same for ‘lst’, since that’s the return
value and the compiler will certainly keep it in a register or somewhere
throughout the routine.

   The ‘clear_image’ example previously shown (*note Type checking::)
also used ‘scm_remember_upto_here_1’ for this reason.

   It’s only in quite rare circumstances that a missing
‘scm_remember_upto_here_1’ will bite, but when it happens the
consequences are serious.  Fortunately the rule is simple: whenever
calling a Guile library function or doing something that might, ensure
that the ‘SCM’ of a smob is referenced past all accesses to its insides.
Do this by adding an ‘scm_remember_upto_here_1’ if there are no other
references.

   In a multi-threaded program, the rule is the same.  As far as a given
thread is concerned, a garbage collection still only occurs within a
Guile library function, not at an arbitrary time.  (Guile waits for all
threads to reach one of its library functions, and holds them there
while the collector runs.)

5.5.6 Double Smobs
------------------

Smobs are called smob because they are small: they normally have only
room for one ‘void*’ or ‘SCM’ value plus 16 bits.  The reason for this
is that smobs are directly implemented by using the low-level, two-word
cells of Guile that are also used to implement pairs, for example.
(*note Data Representation:: for the details.)  One word of the two-word
cells is used for ‘SCM_SMOB_DATA’ (or ‘SCM_SMOB_OBJECT’), the other
contains the 16-bit type tag and the 16 extra bits.

   In addition to the fundamental two-word cells, Guile also has
four-word cells, which are appropriately called "double cells".  You can
use them for "double smobs" and get two more immediate words of type
‘scm_t_bits’.

   A double smob is created with ‘scm_new_double_smob’.  Its immediate
words can be retrieved as ‘scm_t_bits’ with ‘SCM_SMOB_DATA_2’ and
‘SCM_SMOB_DATA_3’ in addition to ‘SCM_SMOB_DATA’.  Unsurprisingly, the
words can be set to ‘scm_t_bits’ values with ‘SCM_SET_SMOB_DATA_2’ and
‘SCM_SET_SMOB_DATA_3’.

   Of course there are also ‘SCM_SMOB_OBJECT_2’, ‘SCM_SMOB_OBJECT_3’,
‘SCM_SET_SMOB_OBJECT_2’, and ‘SCM_SET_SMOB_OBJECT_3’.

5.5.7 The Complete Example
--------------------------

Here is the complete text of the implementation of the image datatype,
as presented in the sections above.  We also provide a definition for
the smob’s _print_ function, and make some objects and functions static,
to clarify exactly what the surrounding code is using.

   As mentioned above, you can find this code in the Guile distribution,
in ‘doc/example-smob’.  That directory includes a makefile and a
suitable ‘main’ function, so you can build a complete interactive Guile
shell, extended with the datatypes described here.)

     /* file "image-type.c" */

     #include <stdlib.h>
     #include <libguile.h>

     static scm_t_bits image_tag;

     struct image {
       int width, height;
       char *pixels;

       /* The name of this image */
       SCM name;

       /* A function to call when this image is
          modified, e.g., to update the screen,
          or SCM_BOOL_F if no action necessary */
       SCM update_func;
     };

     static SCM
     make_image (SCM name, SCM s_width, SCM s_height)
     {
       SCM smob;
       struct image *image;
       int width = scm_to_int (s_width);
       int height = scm_to_int (s_height);

       /* Step 1: Allocate the memory block.
        */
       image = (struct image *)
          scm_gc_malloc (sizeof (struct image), "image");

       /* Step 2: Initialize it with straight code.
        */
       image->width = width;
       image->height = height;
       image->pixels = NULL;
       image->name = SCM_BOOL_F;
       image->update_func = SCM_BOOL_F;

       /* Step 3: Create the smob.
        */
       smob = scm_new_smob (image_tag, image);

       /* Step 4: Finish the initialization.
        */
       image->name = name;
       image->pixels =
          scm_gc_malloc (width * height, "image pixels");

       return smob;
     }

     SCM
     clear_image (SCM image_smob)
     {
       int area;
       struct image *image;

       scm_assert_smob_type (image_tag, image_smob);

       image = (struct image *) SCM_SMOB_DATA (image_smob);
       area = image->width * image->height;
       memset (image->pixels, 0, area);

       /* Invoke the image's update function.
        */
       if (scm_is_true (image->update_func))
         scm_call_0 (image->update_func);

       scm_remember_upto_here_1 (image_smob);

       return SCM_UNSPECIFIED;
     }

     static SCM
     mark_image (SCM image_smob)
     {
       /* Mark the image's name and update function.  */
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_gc_mark (image->name);
       return image->update_func;
     }

     static size_t
     free_image (SCM image_smob)
     {
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_gc_free (image->pixels,
                    image->width * image->height,
                    "image pixels");
       scm_gc_free (image, sizeof (struct image), "image");

       return 0;
     }

     static int
     print_image (SCM image_smob, SCM port, scm_print_state *pstate)
     {
       struct image *image = (struct image *) SCM_SMOB_DATA (image_smob);

       scm_puts ("#<image ", port);
       scm_display (image->name, port);
       scm_puts (">", port);

       /* non-zero means success */
       return 1;
     }

     void
     init_image_type (void)
     {
       image_tag = scm_make_smob_type ("image", sizeof (struct image));
       scm_set_smob_mark (image_tag, mark_image);
       scm_set_smob_free (image_tag, free_image);
       scm_set_smob_print (image_tag, print_image);

       scm_c_define_gsubr ("clear-image", 1, 0, 0, clear_image);
       scm_c_define_gsubr ("make-image", 3, 0, 0, make_image);
     }

   Here is a sample build and interaction with the code from the
‘example-smob’ directory, on the author’s machine:

     zwingli:example-smob$ make CC=gcc
     gcc `pkg-config --cflags guile-2.0` -c image-type.c -o image-type.o
     gcc `pkg-config --cflags guile-2.0` -c myguile.c -o myguile.o
     gcc image-type.o myguile.o `pkg-config --libs guile-2.0` -o myguile
     zwingli:example-smob$ ./myguile
     guile> make-image
     #<primitive-procedure make-image>
     guile> (define i (make-image "Whistler's Mother" 100 100))
     guile> i
     #<image Whistler's Mother>
     guile> (clear-image i)
     guile> (clear-image 4)
     ERROR: In procedure clear-image in expression (clear-image 4):
     ERROR: Wrong type (expecting image): 4
     ABORT: (wrong-type-arg)

     Type "(backtrace)" to get more information.
     guile>

5.6 Function Snarfing
=====================

When writing C code for use with Guile, you typically define a set of C
functions, and then make some of them visible to the Scheme world by
calling ‘scm_c_define_gsubr’ or related functions.  If you have many
functions to publish, it can sometimes be annoying to keep the list of
calls to ‘scm_c_define_gsubr’ in sync with the list of function
definitions.

   Guile provides the ‘guile-snarf’ program to manage this problem.
Using this tool, you can keep all the information needed to define the
function alongside the function definition itself; ‘guile-snarf’ will
extract this information from your source code, and automatically
generate a file of calls to ‘scm_c_define_gsubr’ which you can
‘#include’ into an initialization function.

   The snarfing mechanism works for many kind of initialization actions,
not just for collecting calls to ‘scm_c_define_gsubr’.  For a full list
of what can be done, *Note Snarfing Macros::.

   The ‘guile-snarf’ program is invoked like this:

     guile-snarf [-o OUTFILE] [CPP-ARGS ...]

   This command will extract initialization actions to OUTFILE.  When no
OUTFILE has been specified or when OUTFILE is ‘-’, standard output will
be used.  The C preprocessor is called with CPP-ARGS (which usually
include an input file) and the output is filtered to extract the
initialization actions.

   If there are errors during processing, OUTFILE is deleted and the
program exits with non-zero status.

   During snarfing, the pre-processor macro ‘SCM_MAGIC_SNARFER’ is
defined.  You could use this to avoid including snarfer output files
that don’t yet exist by writing code like this:

     #ifndef SCM_MAGIC_SNARFER
     #include "foo.x"
     #endif

   Here is how you might define the Scheme function ‘clear-image’,
implemented by the C function ‘clear_image’:

     #include <libguile.h>

     SCM_DEFINE (clear_image, "clear-image", 1, 0, 0,
                 (SCM image_smob),
                 "Clear the image.")
     {
       /* C code to clear the image in image_smob... */
     }

     void
     init_image_type ()
     {
     #include "image-type.x"
     }

   The ‘SCM_DEFINE’ declaration says that the C function ‘clear_image’
implements a Scheme function called ‘clear-image’, which takes one
required argument (of type ‘SCM’ and named ‘image_smob’), no optional
arguments, and no rest argument.  The string ‘"Clear the image."’
provides a short help text for the function, it is called a "docstring".

   ‘SCM_DEFINE’ macro also defines a static array of characters
initialized to the Scheme name of the function.  In this case,
‘s_clear_image’ is set to the C string, "clear-image".  You might want
to use this symbol when generating error messages.

   Assuming the text above lives in a file named ‘image-type.c’, you
will need to execute the following command to prepare this file for
compilation:

     guile-snarf -o image-type.x image-type.c

   This scans ‘image-type.c’ for ‘SCM_DEFINE’ declarations, and writes
to ‘image-type.x’ the output:

     scm_c_define_gsubr ("clear-image", 1, 0, 0, (SCM (*)() ) clear_image);

   When compiled normally, ‘SCM_DEFINE’ is a macro which expands to the
function header for ‘clear_image’.

   Note that the output file name matches the ‘#include’ from the input
file.  Also, you still need to provide all the same information you
would if you were using ‘scm_c_define_gsubr’ yourself, but you can place
the information near the function definition itself, so it is less
likely to become incorrect or out-of-date.

   If you have many files that ‘guile-snarf’ must process, you should
consider using a fragment like the following in your Makefile:

     snarfcppopts = $(DEFS) $(INCLUDES) $(CPPFLAGS) $(CFLAGS)
     .SUFFIXES: .x
     .c.x:
     	guile-snarf -o $@ $< $(snarfcppopts)

   This tells make to run ‘guile-snarf’ to produce each needed ‘.x’ file
from the corresponding ‘.c’ file.

   The program ‘guile-snarf’ passes its command-line arguments directly
to the C preprocessor, which it uses to extract the information it needs
from the source code.  this means you can pass normal compilation flags
to ‘guile-snarf’ to define preprocessor symbols, add header file
directories, and so on.

5.7 An Overview of Guile Programming
====================================

Guile is designed as an extension language interpreter that is
straightforward to integrate with applications written in C (and C++).
The big win here for the application developer is that Guile
integration, as the Guile web page says, “lowers your project’s
hacktivation energy.” Lowering the hacktivation energy means that you,
as the application developer, _and your users_, reap the benefits that
flow from being able to extend the application in a high level extension
language rather than in plain old C.

   In abstract terms, it’s difficult to explain what this really means
and what the integration process involves, so instead let’s begin by
jumping straight into an example of how you might integrate Guile into
an existing program, and what you could expect to gain by so doing.
With that example under our belts, we’ll then return to a more general
analysis of the arguments involved and the range of programming options
available.

5.7.1 How One Might Extend Dia Using Guile
------------------------------------------

Dia is a free software program for drawing schematic diagrams like flow
charts and floor plans (<http://www.gnome.org/projects/dia/>).  This
section conducts the thought experiment of adding Guile to Dia.  In so
doing, it aims to illustrate several of the steps and considerations
involved in adding Guile to applications in general.

5.7.1.1 Deciding Why You Want to Add Guile
..........................................

First off, you should understand why you want to add Guile to Dia at
all, and that means forming a picture of what Dia does and how it does
it.  So, what are the constituents of the Dia application?

   • Most importantly, the "application domain objects" — in other
     words, the concepts that differentiate Dia from another application
     such as a word processor or spreadsheet: shapes, templates,
     connectors, pages, plus the properties of all these things.

   • The code that manages the graphical face of the application,
     including the layout and display of the objects above.

   • The code that handles input events, which indicate that the
     application user is wanting to do something.

(In other words, a textbook example of the "model - view - controller"
paradigm.)

   Next question: how will Dia benefit once the Guile integration is
complete?  Several (positive!)  answers are possible here, and the
choice is obviously up to the application developers.  Still, one answer
is that the main benefit will be the ability to manipulate Dia’s
application domain objects from Scheme.

   Suppose that Dia made a set of procedures available in Scheme,
representing the most basic operations on objects such as shapes,
connectors, and so on.  Using Scheme, the application user could then
write code that builds upon these basic operations to create more
complex procedures.  For example, given basic procedures to enumerate
the objects on a page, to determine whether an object is a square, and
to change the fill pattern of a single shape, the user can write a
Scheme procedure to change the fill pattern of all squares on the
current page:

     (define (change-squares'-fill-pattern new-pattern)
       (for-each-shape current-page
         (lambda (shape)
           (if (square? shape)
               (change-fill-pattern shape new-pattern)))))

5.7.1.2 Four Steps Required to Add Guile
........................................

Assuming this objective, four steps are needed to achieve it.

   First, you need a way of representing your application-specific
objects — such as ‘shape’ in the previous example — when they are passed
into the Scheme world.  Unless your objects are so simple that they map
naturally into builtin Scheme data types like numbers and strings, you
will probably want to use Guile’s "SMOB" interface to create a new
Scheme data type for your objects.

   Second, you need to write code for the basic operations like
‘for-each-shape’ and ‘square?’ such that they access and manipulate your
existing data structures correctly, and then make these operations
available as "primitives" on the Scheme level.

   Third, you need to provide some mechanism within the Dia application
that a user can hook into to cause arbitrary Scheme code to be
evaluated.

   Finally, you need to restructure your top-level application C code a
little so that it initializes the Guile interpreter correctly and
declares your "SMOBs" and "primitives" to the Scheme world.

   The following subsections expand on these four points in turn.

5.7.1.3 How to Represent Dia Data in Scheme
...........................................

For all but the most trivial applications, you will probably want to
allow some representation of your domain objects to exist on the Scheme
level.  This is where the idea of SMOBs comes in, and with it issues of
lifetime management and garbage collection.

   To get more concrete about this, let’s look again at the example we
gave earlier of how application users can use Guile to build
higher-level functions from the primitives that Dia itself provides.

     (define (change-squares'-fill-pattern new-pattern)
       (for-each-shape current-page
         (lambda (shape)
           (if (square? shape)
               (change-fill-pattern shape new-pattern)))))

   Consider what is stored here in the variable ‘shape’.  For each shape
on the current page, the ‘for-each-shape’ primitive calls ‘(lambda
(shape) …)’ with an argument representing that shape.  Question is: how
is that argument represented on the Scheme level?  The issues are as
follows.

   • Whatever the representation, it has to be decodable again by the C
     code for the ‘square?’ and ‘change-fill-pattern’ primitives.  In
     other words, a primitive like ‘square?’ has somehow to be able to
     turn the value that it receives back into something that points to
     the underlying C structure describing a shape.

   • The representation must also cope with Scheme code holding on to
     the value for later use.  What happens if the Scheme code stores
     ‘shape’ in a global variable, but then that shape is deleted (in a
     way that the Scheme code is not aware of), and later on some other
     Scheme code uses that global variable again in a call to, say,
     ‘square?’?

   • The lifetime and memory allocation of objects that exist _only_ in
     the Scheme world is managed automatically by Guile’s garbage
     collector using one simple rule: when there are no remaining
     references to an object, the object is considered dead and so its
     memory is freed.  But for objects that exist in both C and Scheme,
     the picture is more complicated; in the case of Dia, where the
     ‘shape’ argument passes transiently in and out of the Scheme world,
     it would be quite wrong the *delete* the underlying C shape just
     because the Scheme code has finished evaluation.  How do we avoid
     this happening?

   One resolution of these issues is for the Scheme-level representation
of a shape to be a new, Scheme-specific C structure wrapped up as a
SMOB. The SMOB is what is passed into and out of Scheme code, and the
Scheme-specific C structure inside the SMOB points to Dia’s underlying C
structure so that the code for primitives like ‘square?’ can get at it.

   To cope with an underlying shape being deleted while Scheme code is
still holding onto a Scheme shape value, the underlying C structure
should have a new field that points to the Scheme-specific SMOB. When a
shape is deleted, the relevant code chains through to the
Scheme-specific structure and sets its pointer back to the underlying
structure to NULL. Thus the SMOB value for the shape continues to exist,
but any primitive code that tries to use it will detect that the
underlying shape has been deleted because the underlying structure
pointer is NULL.

   So, to summarize the steps involved in this resolution of the problem
(and assuming that the underlying C structure for a shape is ‘struct
dia_shape’):

   • Define a new Scheme-specific structure that _points_ to the
     underlying C structure:

          struct dia_guile_shape
          {
            struct dia_shape * c_shape;   /* NULL => deleted */
          }

   • Add a field to ‘struct dia_shape’ that points to its ‘struct
     dia_guile_shape’ if it has one —

          struct dia_shape
          {
            …
            struct dia_guile_shape * guile_shape;
          }

     — so that C code can set ‘guile_shape->c_shape’ to NULL when the
     underlying shape is deleted.

   • Wrap ‘struct dia_guile_shape’ as a SMOB type.

   • Whenever you need to represent a C shape onto the Scheme level,
     create a SMOB instance for it, and pass that.

   • In primitive code that receives a shape SMOB instance, check the
     ‘c_shape’ field when decoding it, to find out whether the
     underlying C shape is still there.

   As far as memory management is concerned, the SMOB values and their
Scheme-specific structures are under the control of the garbage
collector, whereas the underlying C structures are explicitly managed in
exactly the same way that Dia managed them before we thought of adding
Guile.

   When the garbage collector decides to free a shape SMOB value, it
calls the "SMOB free" function that was specified when defining the
shape SMOB type.  To maintain the correctness of the ‘guile_shape’ field
in the underlying C structure, this function should chain through to the
underlying C structure (if it still exists) and set its ‘guile_shape’
field to NULL.

   For full documentation on defining and using SMOB types, see *note
Defining New Types (Smobs)::.

5.7.1.4 Writing Guile Primitives for Dia
........................................

Once the details of object representation are decided, writing the
primitive function code that you need is usually straightforward.

   A primitive is simply a C function whose arguments and return value
are all of type ‘SCM’, and whose body does whatever you want it to do.
As an example, here is a possible implementation of the ‘square?’
primitive:

     static SCM square_p (SCM shape)
     {
       struct dia_guile_shape * guile_shape;

       /* Check that arg is really a shape SMOB. */
       scm_assert_smob_type (shape_tag, shape);

       /* Access Scheme-specific shape structure. */
       guile_shape = SCM_SMOB_DATA (shape);

       /* Find out if underlying shape exists and is a
          square; return answer as a Scheme boolean. */
       return scm_from_bool (guile_shape->c_shape &&
                             (guile_shape->c_shape->type == DIA_SQUARE));
     }

   Notice how easy it is to chain through from the ‘SCM shape’ parameter
that ‘square_p’ receives — which is a SMOB — to the Scheme-specific
structure inside the SMOB, and thence to the underlying C structure for
the shape.

   In this code, ‘scm_assert_smob_type’, ‘SCM_SMOB_DATA’, and
‘scm_from_bool’ are from the standard Guile API. We assume that
‘shape_tag’ was given to us when we made the shape SMOB type, using
‘scm_make_smob_type’.  The call to ‘scm_assert_smob_type’ ensures that
SHAPE is indeed a shape.  This is needed to guard against Scheme code
using the ‘square?’ procedure incorrectly, as in ‘(square? "hello")’;
Scheme’s latent typing means that usage errors like this must be caught
at run time.

   Having written the C code for your primitives, you need to make them
available as Scheme procedures by calling the ‘scm_c_define_gsubr’
function.  ‘scm_c_define_gsubr’ (*note Primitive Procedures::) takes
arguments that specify the Scheme-level name for the primitive and how
many required, optional and rest arguments it can accept.  The ‘square?’
primitive always requires exactly one argument, so the call to make it
available in Scheme reads like this:

     scm_c_define_gsubr ("square?", 1, 0, 0, square_p);

   For where to put this call, see the subsection after next on the
structure of Guile-enabled code (*note Dia Structure::).

5.7.1.5 Providing a Hook for the Evaluation of Scheme Code
..........................................................

To make the Guile integration useful, you have to design some kind of
hook into your application that application users can use to cause their
Scheme code to be evaluated.

   Technically, this is straightforward; you just have to decide on a
mechanism that is appropriate for your application.  Think of Emacs, for
example: when you type ‘<ESC> :’, you get a prompt where you can type in
any Elisp code, which Emacs will then evaluate.  Or, again like Emacs,
you could provide a mechanism (such as an init file) to allow Scheme
code to be associated with a particular key sequence, and evaluate the
code when that key sequence is entered.

   In either case, once you have the Scheme code that you want to
evaluate, as a null terminated string, you can tell Guile to evaluate it
by calling the ‘scm_c_eval_string’ function.

5.7.1.6 Top-level Structure of Guile-enabled Dia
................................................

Let’s assume that the pre-Guile Dia code looks structurally like this:

   • ‘main ()’

        • do lots of initialization and setup stuff
        • enter Gtk main loop

   When you add Guile to a program, one (rather technical) requirement
is that Guile’s garbage collector needs to know where the bottom of the
C stack is.  The easiest way to ensure this is to use ‘scm_boot_guile’
like this:

   • ‘main ()’

        • do lots of initialization and setup stuff
        • ‘scm_boot_guile (argc, argv, inner_main, NULL)’

   • ‘inner_main ()’

        • define all SMOB types
        • export primitives to Scheme using ‘scm_c_define_gsubr’
        • enter Gtk main loop

   In other words, you move the guts of what was previously in your
‘main’ function into a new function called ‘inner_main’, and then add a
‘scm_boot_guile’ call, with ‘inner_main’ as a parameter, to the end of
‘main’.

   Assuming that you are using SMOBs and have written primitive code as
described in the preceding subsections, you also need to insert calls to
declare your new SMOBs and export the primitives to Scheme.  These
declarations must happen _inside_ the dynamic scope of the
‘scm_boot_guile’ call, but also _before_ any code is run that could
possibly use them — the beginning of ‘inner_main’ is an ideal place for
this.

5.7.1.7 Going Further with Dia and Guile
........................................

The steps described so far implement an initial Guile integration that
already gives a lot of additional power to Dia application users.  But
there are further steps that you could take, and it’s interesting to
consider a few of these.

   In general, you could progressively move more of Dia’s source code
from C into Scheme.  This might make the code more maintainable and
extensible, and it could open the door to new programming paradigms that
are tricky to effect in C but straightforward in Scheme.

   A specific example of this is that you could use the guile-gtk
package, which provides Scheme-level procedures for most of the Gtk+
library, to move the code that lays out and displays Dia objects from C
to Scheme.

   As you follow this path, it naturally becomes less useful to maintain
a distinction between Dia’s original non-Guile-related source code, and
its later code implementing SMOBs and primitives for the Scheme world.

   For example, suppose that the original source code had a
‘dia_change_fill_pattern’ function:

     void dia_change_fill_pattern (struct dia_shape * shape,
                                   struct dia_pattern * pattern)
     {
       /* real pattern change work */
     }

   During initial Guile integration, you add a ‘change_fill_pattern’
primitive for Scheme purposes, which accesses the underlying structures
from its SMOB values and uses ‘dia_change_fill_pattern’ to do the real
work:

     SCM change_fill_pattern (SCM shape, SCM pattern)
     {
       struct dia_shape * d_shape;
       struct dia_pattern * d_pattern;

       …

       dia_change_fill_pattern (d_shape, d_pattern);

       return SCM_UNSPECIFIED;
     }

   At this point, it makes sense to keep ‘dia_change_fill_pattern’ and
‘change_fill_pattern’ separate, because ‘dia_change_fill_pattern’ can
also be called without going through Scheme at all, say because the user
clicks a button which causes a C-registered Gtk+ callback to be called.

   But, if the code for creating buttons and registering their callbacks
is moved into Scheme (using guile-gtk), it may become true that
‘dia_change_fill_pattern’ can no longer be called other than through
Scheme.  In which case, it makes sense to abolish it and move its
contents directly into ‘change_fill_pattern’, like this:

     SCM change_fill_pattern (SCM shape, SCM pattern)
     {
       struct dia_shape * d_shape;
       struct dia_pattern * d_pattern;

       …

       /* real pattern change work */

       return SCM_UNSPECIFIED;
     }

   So further Guile integration progressively _reduces_ the amount of
functional C code that you have to maintain over the long term.

   A similar argument applies to data representation.  In the discussion
of SMOBs earlier, issues arose because of the different memory
management and lifetime models that normally apply to data structures in
C and in Scheme.  However, with further Guile integration, you can
resolve this issue in a more radical way by allowing all your data
structures to be under the control of the garbage collector, and kept
alive by references from the Scheme world.  Instead of maintaining an
array or linked list of shapes in C, you would instead maintain a list
in Scheme.

   Rather like the coalescing of ‘dia_change_fill_pattern’ and
‘change_fill_pattern’, the practical upshot of such a change is that you
would no longer have to keep the ‘dia_shape’ and ‘dia_guile_shape’
structures separate, and so wouldn’t need to worry about the pointers
between them.  Instead, you could change the SMOB definition to wrap the
‘dia_shape’ structure directly, and send ‘dia_guile_shape’ off to the
scrap yard.  Cut out the middle man!

   Finally, we come to the holy grail of Guile’s free software /
extension language approach.  Once you have a Scheme representation for
interesting Dia data types like shapes, and a handy bunch of primitives
for manipulating them, it suddenly becomes clear that you have a bundle
of functionality that could have far-ranging use beyond Dia itself.  In
other words, the data types and primitives could now become a library,
and Dia becomes just one of the many possible applications using that
library — albeit, at this early stage, a rather important one!

   In this model, Guile becomes just the glue that binds everything
together.  Imagine an application that usefully combined functionality
from Dia, Gnumeric and GnuCash — it’s tricky right now, because no such
application yet exists; but it’ll happen some day …

5.7.2 Why Scheme is More Hackable Than C
----------------------------------------

Underlying Guile’s value proposition is the assumption that programming
in a high level language, specifically Guile’s implementation of Scheme,
is necessarily better in some way than programming in C. What do we mean
by this claim, and how can we be so sure?

   One class of advantages applies not only to Scheme, but more
generally to any interpretable, high level, scripting language, such as
Emacs Lisp, Python, Ruby, or TeX’s macro language.  Common features of
all such languages, when compared to C, are that:

   • They lend themselves to rapid and experimental development cycles,
     owing usually to a combination of their interpretability and the
     integrated development environment in which they are used.

   • They free developers from some of the low level bookkeeping tasks
     associated with C programming, notably memory management.

   • They provide high level features such as container objects and
     exception handling that make common programming tasks easier.

   In the case of Scheme, particular features that make programming
easier — and more fun!  — are its powerful mechanisms for abstracting
parts of programs (closures — *note About Closure::) and for iteration
(*note while do::).

   The evidence in support of this argument is empirical: the huge
amount of code that has been written in extension languages for
applications that support this mechanism.  Most notable are extensions
written in Emacs Lisp for GNU Emacs, in TeX’s macro language for TeX,
and in Script-Fu for the Gimp, but there is increasingly now a
significant code eco-system for Guile-based applications as well, such
as Lilypond and GnuCash.  It is close to inconceivable that similar
amounts of functionality could have been added to these applications
just by writing new code in their base implementation languages.

5.7.3 Example: Using Guile for an Application Testbed
-----------------------------------------------------

As an example of what this means in practice, imagine writing a testbed
for an application that is tested by submitting various requests (via a
C interface) and validating the output received.  Suppose further that
the application keeps an idea of its current state, and that the
“correct” output for a given request may depend on the current
application state.  A complete “white box”(1) test plan for this
application would aim to submit all possible requests in each
distinguishable state, and validate the output for all request/state
combinations.

   To write all this test code in C would be very tedious.  Suppose
instead that the testbed code adds a single new C function, to submit an
arbitrary request and return the response, and then uses Guile to export
this function as a Scheme procedure.  The rest of the testbed can then
be written in Scheme, and so benefits from all the advantages of
programming in Scheme that were described in the previous section.

   (In this particular example, there is an additional benefit of
writing most of the testbed in Scheme.  A common problem for white box
testing is that mistakes and mistaken assumptions in the application
under test can easily be reproduced in the testbed code.  It is more
difficult to copy mistakes like this when the testbed is written in a
different language from the application.)

   ---------- Footnotes ----------

   (1) A "white box" test plan is one that incorporates knowledge of the
internal design of the application under test.

5.7.4 A Choice of Programming Options
-------------------------------------

The preceding arguments and example point to a model of Guile
programming that is applicable in many cases.  According to this model,
Guile programming involves a balance between C and Scheme programming,
with the aim being to extract the greatest possible Scheme level benefit
from the least amount of C level work.

   The C level work required in this model usually consists of packaging
and exporting functions and application objects such that they can be
seen and manipulated on the Scheme level.  To help with this, Guile’s C
language interface includes utility features that aim to make this kind
of integration very easy for the application developer.  These features
are documented later in this part of the manual: see REFFIXME.

   This model, though, is really just one of a range of possible
programming options.  If all of the functionality that you need is
available from Scheme, you could choose instead to write your whole
application in Scheme (or one of the other high level languages that
Guile supports through translation), and simply use Guile as an
interpreter for Scheme.  (In the future, we hope that Guile will also be
able to compile Scheme code, so lessening the performance gap between C
and Scheme code.)  Or, at the other end of the C–Scheme scale, you could
write the majority of your application in C, and only call out to Guile
occasionally for specific actions such as reading a configuration file
or executing a user-specified extension.  The choices boil down to two
basic questions:

   • Which parts of the application do you write in C, and which in
     Scheme (or another high level translated language)?

   • How do you design the interface between the C and Scheme parts of
     your application?

   These are of course design questions, and the right design for any
given application will always depend upon the particular requirements
that you are trying to meet.  In the context of Guile, however, there
are some generally applicable considerations that can help you when
designing your answers.

5.7.4.1 What Functionality is Already Available?
................................................

Suppose, for the sake of argument, that you would prefer to write your
whole application in Scheme.  Then the API available to you consists of:

   • standard Scheme

   • plus the extensions to standard Scheme provided by Guile in its
     core distribution

   • plus any additional functionality that you or others have packaged
     so that it can be loaded as a Guile Scheme module.

   A module in the last category can either be a pure Scheme module — in
other words a collection of utility procedures coded in Scheme — or a
module that provides a Scheme interface to an extension library coded in
C — in other words a nice package where someone else has done the work
of wrapping up some useful C code for you.  The set of available modules
is growing quickly and already includes such useful examples as ‘(gtk
gtk)’, which makes Gtk+ drawing functions available in Scheme, and
‘(database postgres)’, which provides SQL access to a Postgres database.

   Given the growing collection of pre-existing modules, it is quite
feasible that your application could be implemented by combining a
selection of these modules together with new application code written in
Scheme.

   If this approach is not enough, because the functionality that your
application needs is not already available in this form, and it is
impossible to write the new functionality in Scheme, you will need to
write some C code.  If the required function is already available in C
(e.g. in a library), all you need is a little glue to connect it to the
world of Guile.  If not, you need both to write the basic code and to
plumb it into Guile.

   In either case, two general considerations are important.  Firstly,
what is the interface by which the functionality is presented to the
Scheme world?  Does the interface consist only of function calls (for
example, a simple drawing interface), or does it need to include
"objects" of some kind that can be passed between C and Scheme and
manipulated by both worlds.  Secondly, how does the lifetime and memory
management of objects in the C code relate to the garbage collection
governed approach of Scheme objects?  In the case where the basic C code
is not already written, most of the difficulties of memory management
can be avoided by using Guile’s C interface features from the start.

   For the full documentation on writing C code for Guile and connecting
existing C code to the Guile world, see REFFIXME.

5.7.4.2 Functional and Performance Constraints
..............................................

5.7.4.3 Your Preferred Programming Style
........................................

5.7.4.4 What Controls Program Execution?
........................................

5.7.5 How About Application Users?
----------------------------------

So far we have considered what Guile programming means for an
application developer.  But what if you are instead _using_ an existing
Guile-based application, and want to know what your options are for
programming and extending this application?

   The answer to this question varies from one application to another,
because the options available depend inevitably on whether the
application developer has provided any hooks for you to hang your own
code on and, if there are such hooks, what they allow you to do.(1)  For
example…

   • If the application permits you to load and execute any Guile code,
     the world is your oyster.  You can extend the application in any
     way that you choose.

   • A more cautious application might allow you to load and execute
     Guile code, but only in a "safe" environment, where the interface
     available is restricted by the application from the standard Guile
     API.

   • Or a really fearful application might not provide a hook to really
     execute user code at all, but just use Scheme syntax as a
     convenient way for users to specify application data or
     configuration options.

   In the last two cases, what you can do is, by definition, restricted
by the application, and you should refer to the application’s own manual
to find out your options.

   The most well known example of the first case is Emacs, with its
extension language Emacs Lisp: as well as being a text editor, Emacs
supports the loading and execution of arbitrary Emacs Lisp code.  The
result of such openness has been dramatic: Emacs now benefits from
user-contributed Emacs Lisp libraries that extend the basic editing
function to do everything from reading news to psychoanalysis and
playing adventure games.  The only limitation is that extensions are
restricted to the functionality provided by Emacs’s built-in set of
primitive operations.  For example, you can interact and display data by
manipulating the contents of an Emacs buffer, but you can’t pop-up and
draw a window with a layout that is totally different to the Emacs
standard.

   This situation with a Guile application that supports the loading of
arbitrary user code is similar, except perhaps even more so, because
Guile also supports the loading of extension libraries written in C.
This last point enables user code to add new primitive operations to
Guile, and so to bypass the limitation present in Emacs Lisp.

   At this point, the distinction between an application developer and
an application user becomes rather blurred.  Instead of seeing yourself
as a user extending an application, you could equally well say that you
are developing a new application of your own using some of the primitive
functionality provided by the original application.  As such, all the
discussions of the preceding sections of this chapter are relevant to
how you can proceed with developing your extension.

   ---------- Footnotes ----------

   (1) Of course, in the world of free software, you always have the
freedom to modify the application’s source code to your own
requirements.  Here we are concerned with the extension options that the
application has provided for without your needing to modify its source
code.

5.8 Autoconf Support
====================

Autoconf, a part of the GNU build system, makes it easy for users to
build your package.  This section documents Guile’s Autoconf support.

5.8.1 Autoconf Background
-------------------------

As explained in the ‘GNU Autoconf Manual’, any package needs
configuration at build-time (*note Introduction: (autoconf)Top.).  If
your package uses Guile (or uses a package that in turn uses Guile), you
probably need to know what specific Guile features are available and
details about them.

   The way to do this is to write feature tests and arrange for their
execution by the ‘configure’ script, typically by adding the tests to
‘configure.ac’, and running ‘autoconf’ to create ‘configure’.  Users of
your package then run ‘configure’ in the normal way.

   Macros are a way to make common feature tests easy to express.
Autoconf provides a wide range of macros (*note (autoconf)Existing
Tests::), and Guile installation provides Guile-specific tests in the
areas of: program detection, compilation flags reporting, and Scheme
module checks.

5.8.2 Autoconf Macros
---------------------

As mentioned earlier in this chapter, Guile supports parallel
installation, and uses ‘pkg-config’ to let the user choose which version
of Guile they are interested in.  ‘pkg-config’ has its own set of
Autoconf macros that are probably installed on most every development
system.  The most useful of these macros is ‘PKG_CHECK_MODULES’.

     PKG_CHECK_MODULES([GUILE], [guile-2.0])

   This example looks for Guile and sets the ‘GUILE_CFLAGS’ and
‘GUILE_LIBS’ variables accordingly, or prints an error and exits if
Guile was not found.

   Guile comes with additional Autoconf macros providing more
information, installed as ‘PREFIX/share/aclocal/guile.m4’.  Their names
all begin with ‘GUILE_’.

 -- Autoconf Macro: GUILE_PKG [VERSIONS]

     This macro runs the ‘pkg-config’ tool to find development files for
     an available version of Guile.

     By default, this macro will search for the latest stable version of
     Guile (e.g.  2.0), falling back to the previous stable version
     (e.g.  1.8) if it is available.  If no guile-VERSION.pc file is
     found, an error is signalled.  The found version is stored in
     GUILE_EFFECTIVE_VERSION.

     If ‘GUILE_PROGS’ was already invoked, this macro ensures that the
     development files have the same effective version as the Guile
     program.

     GUILE_EFFECTIVE_VERSION is marked for substitution, as by
     ‘AC_SUBST’.

 -- Autoconf Macro: GUILE_FLAGS

     This macro runs the ‘pkg-config’ tool to find out how to compile
     and link programs against Guile.  It sets four variables:
     GUILE_CFLAGS, GUILE_LDFLAGS, GUILE_LIBS, and GUILE_LTLIBS.

     GUILE_CFLAGS: flags to pass to a C or C++ compiler to build code
     that uses Guile header files.  This is almost always just one or
     more ‘-I’ flags.

     GUILE_LDFLAGS: flags to pass to the compiler to link a program
     against Guile.  This includes ‘-lguile-VERSION’ for the Guile
     library itself, and may also include one or more ‘-L’ flag to tell
     the compiler where to find the libraries.  But it does not include
     flags that influence the program’s runtime search path for
     libraries, and will therefore lead to a program that fails to
     start, unless all necessary libraries are installed in a standard
     location such as ‘/usr/lib’.

     GUILE_LIBS and GUILE_LTLIBS: flags to pass to the compiler or to
     libtool, respectively, to link a program against Guile.  It
     includes flags that augment the program’s runtime search path for
     libraries, so that shared libraries will be found at the location
     where they were during linking, even in non-standard locations.
     GUILE_LIBS is to be used when linking the program directly with the
     compiler, whereas GUILE_LTLIBS is to be used when linking the
     program is done through libtool.

     The variables are marked for substitution, as by ‘AC_SUBST’.

 -- Autoconf Macro: GUILE_SITE_DIR

     This looks for Guile’s "site" directory, usually something like
     PREFIX/share/guile/site, and sets var GUILE_SITE to the path.  Note
     that the var name is different from the macro name.

     The variable is marked for substitution, as by ‘AC_SUBST’.

 -- Autoconf Macro: GUILE_PROGS [VERSION]

     This macro looks for programs ‘guile’ and ‘guild’, setting
     variables GUILE and GUILD to their paths, respectively.  If ‘guile’
     is not found, signal an error.

     By default, this macro will search for the latest stable version of
     Guile (e.g.  2.0).  x.y or x.y.z versions can be specified.  If an
     older version is found, the macro will signal an error.

     The effective version of the found ‘guile’ is set to
     GUILE_EFFECTIVE_VERSION.  This macro ensures that the effective
     version is compatible with the result of a previous invocation of
     ‘GUILE_FLAGS’, if any.

     As a legacy interface, it also looks for ‘guile-config’ and
     ‘guile-tools’, setting GUILE_CONFIG and GUILE_TOOLS.

     The variables are marked for substitution, as by ‘AC_SUBST’.

 -- Autoconf Macro: GUILE_CHECK_RETVAL var check

     VAR is a shell variable name to be set to the return value.  CHECK
     is a Guile Scheme expression, evaluated with "$GUILE -c", and
     returning either 0 or non-#f to indicate the check passed.  Non-0
     number or #f indicates failure.  Avoid using the character "#"
     since that confuses autoconf.

 -- Autoconf Macro: GUILE_MODULE_CHECK var module featuretest
          description

     VAR is a shell variable name to be set to "yes" or "no".  MODULE is
     a list of symbols, like: (ice-9 common-list).  FEATURETEST is an
     expression acceptable to GUILE_CHECK, q.v.  DESCRIPTION is a
     present-tense verb phrase (passed to AC_MSG_CHECKING).

 -- Autoconf Macro: GUILE_MODULE_AVAILABLE var module

     VAR is a shell variable name to be set to "yes" or "no".  MODULE is
     a list of symbols, like: (ice-9 common-list).

 -- Autoconf Macro: GUILE_MODULE_REQUIRED symlist

     SYMLIST is a list of symbols, WITHOUT surrounding parens, like:
     ice-9 common-list.

 -- Autoconf Macro: GUILE_MODULE_EXPORTS var module modvar

     VAR is a shell variable to be set to "yes" or "no".  MODULE is a
     list of symbols, like: (ice-9 common-list).  MODVAR is the Guile
     Scheme variable to check.

 -- Autoconf Macro: GUILE_MODULE_REQUIRED_EXPORT module modvar

     MODULE is a list of symbols, like: (ice-9 common-list).  MODVAR is
     the Guile Scheme variable to check.

5.8.3 Using Autoconf Macros
---------------------------

Using the autoconf macros is straightforward: Add the macro "calls"
(actually instantiations) to ‘configure.ac’, run ‘aclocal’, and finally,
run ‘autoconf’.  If your system doesn’t have guile.m4 installed, place
the desired macro definitions (‘AC_DEFUN’ forms) in ‘acinclude.m4’, and
‘aclocal’ will do the right thing.

   Some of the macros can be used inside normal shell constructs: ‘if
foo ; then GUILE_BAZ ; fi’, but this is not guaranteed.  It’s probably a
good idea to instantiate macros at top-level.

   We now include two examples, one simple and one complicated.

   The first example is for a package that uses libguile, and thus needs
to know how to compile and link against it.  So we use
‘PKG_CHECK_MODULES’ to set the vars ‘GUILE_CFLAGS’ and ‘GUILE_LIBS’,
which are automatically substituted in the Makefile.

     In configure.ac:

       PKG_CHECK_MODULES([GUILE], [guile-2.0])

     In Makefile.in:

       GUILE_CFLAGS  = @GUILE_CFLAGS@
       GUILE_LIBS = @GUILE_LIBS@

       myprog.o: myprog.c
               $(CC) -o $ $(GUILE_CFLAGS) $<
       myprog: myprog.o
               $(CC) -o $ $< $(GUILE_LIBS)

   The second example is for a package of Guile Scheme modules that uses
an external program and other Guile Scheme modules (some might call this
a "pure scheme" package).  So we use the ‘GUILE_SITE_DIR’ macro, a
regular ‘AC_PATH_PROG’ macro, and the ‘GUILE_MODULE_AVAILABLE’ macro.

     In configure.ac:

       GUILE_SITE_DIR

       probably_wont_work=""

       # pgtype pgtable
       GUILE_MODULE_AVAILABLE(have_guile_pg, (database postgres))
       test $have_guile_pg = no &&
           probably_wont_work="(my pgtype) (my pgtable) $probably_wont_work"

       # gpgutils
       AC_PATH_PROG(GNUPG,gpg)
       test x"$GNUPG" = x &&
           probably_wont_work="(my gpgutils) $probably_wont_work"

       if test ! "$probably_wont_work" = "" ; then
           p="         ***"
           echo
           echo "$p"
           echo "$p NOTE:"
           echo "$p The following modules probably won't work:"
           echo "$p   $probably_wont_work"
           echo "$p They can be installed anyway, and will work if their"
           echo "$p dependencies are installed later.  Please see README."
           echo "$p"
           echo
       fi

     In Makefile.in:

       instdir = @GUILE_SITE@/my

       install:
             $(INSTALL) my/*.scm $(instdir)

