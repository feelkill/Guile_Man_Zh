1 Introduction
**************

Guile is an implementation of the Scheme programming language.  Scheme
(<http://schemers.org/>) is an elegant and conceptually simple dialect
of Lisp, originated by Guy Steele and Gerald Sussman, and since evolved
by the series of reports known as RnRS (the Revised^n Reports on
Scheme).

   Unlike, for example, Python or Perl, Scheme has no benevolent
dictator.  There are many Scheme implementations, with different
characteristics and with communities and academic activities around
them, and the language develops as a result of the interplay between
these.  Guile’s particular characteristics are that

   • it is easy to combine with other code written in C
   • it has a historical and continuing connection with the GNU Project
   • it emphasizes interactive and incremental programming
   • it actually supports several languages, not just Scheme.

The next few sections explain what we mean by these points.  The
sections after that cover how you can obtain and install Guile, and the
typographical conventions that we use in this manual.

1.1 Guile and Scheme
====================

Guile implements Scheme as described in the Revised^5 Report on the
Algorithmic Language Scheme (usually known as R5RS), providing clean and
general data and control structures.  Guile goes beyond the rather
austere language presented in R5RS, extending it with a module system,
full access to POSIX system calls, networking support, multiple threads,
dynamic linking, a foreign function call interface, powerful string
processing, and many other features needed for programming in the real
world.

   The Scheme community has recently agreed and published R6RS, the
latest installment in the RnRS series.  R6RS significantly expands the
core Scheme language, and standardises many non-core functions that
implementations—including Guile—have previously done in different ways.
Guile has been updated to incorporate some of the features of R6RS, and
to adjust some existing features to conform to the R6RS specification,
but it is by no means a complete R6RS implementation.  *Note R6RS
Support::.

   Between R5RS and R6RS, the SRFI process (<http://srfi.schemers.org/>)
standardised interfaces for many practical needs, such as multithreaded
programming and multidimensional arrays.  Guile supports many SRFIs, as
documented in detail in *note SRFI Support::.

   In summary, so far as relationship to the Scheme standards is
concerned, Guile is an R5RS implementation with many extensions, some of
which conform to SRFIs or to the relevant parts of R6RS.

1.2 Combining with C Code
=========================

Like a shell, Guile can run interactively—reading expressions from the
user, evaluating them, and displaying the results—or as a script
interpreter, reading and executing Scheme code from a file.  Guile also
provides an object library, "libguile", that allows other applications
to easily incorporate a complete Scheme interpreter.  An application can
then use Guile as an extension language, a clean and powerful
configuration language, or as multi-purpose “glue”, connecting
primitives provided by the application.  It is easy to call Scheme code
from C code and vice versa, giving the application designer full control
of how and when to invoke the interpreter.  Applications can add new
functions, data types, control structures, and even syntax to Guile,
creating a domain-specific language tailored to the task at hand, but
based on a robust language design.

   This kind of combination is helped by four aspects of Guile’s design
and history.  First is that Guile has always been targeted as an
extension language.  Hence its C API has always been of great
importance, and has been developed accordingly.  Second and third are
rather technical points—that Guile uses conservative garbage collection,
and that it implements the Scheme concept of continuations by copying
and reinstating the C stack—but whose practical consequence is that most
existing C code can be glued into Guile as is, without needing
modifications to cope with strange Scheme execution flows.  Last is the
module system, which helps extensions to coexist without stepping on
each others’ toes.

   Guile’s module system allows one to break up a large program into
manageable sections with well-defined interfaces between them.  Modules
may contain a mixture of interpreted and compiled code; Guile can use
either static or dynamic linking to incorporate compiled code.  Modules
also encourage developers to package up useful collections of routines
for general distribution; as of this writing, one can find Emacs
interfaces, database access routines, compilers, GUI toolkit interfaces,
and HTTP client functions, among others.

1.3 Guile and the GNU Project
=============================

Guile was conceived by the GNU Project following the fantastic success
of Emacs Lisp as an extension language within Emacs.  Just as Emacs Lisp
allowed complete and unanticipated applications to be written within the
Emacs environment, the idea was that Guile should do the same for other
GNU Project applications.  This remains true today.

   The idea of extensibility is closely related to the GNU project’s
primary goal, that of promoting software freedom.  Software freedom
means that people receiving a software package can modify or enhance it
to their own desires, including in ways that may not have occurred at
all to the software’s original developers.  For programs written in a
compiled language like C, this freedom covers modifying and rebuilding
the C code; but if the program also provides an extension language, that
is usually a much friendlier and lower-barrier-of-entry way for the user
to start making their own changes.

   Guile is now used by GNU project applications such as AutoGen,
Lilypond, Denemo, Mailutils, TeXmacs and Gnucash, and we hope that there
will be many more in future.

1.4 Interactive Programming
===========================

Non-free software has no interest in its users being able to see how it
works.  They are supposed to just accept it, or to report problems and
hope that the source code owners will choose to work on them.

   Free software aims to work reliably just as much as non-free software
does, but it should also empower its users by making its workings
available.  This is useful for many reasons, including education,
auditing and enhancements, as well as for debugging problems.

   The ideal free software system achieves this by making it easy for
interested users to see the source code for a feature that they are
using, and to follow through that source code step-by-step, as it runs.
In Emacs, good examples of this are the source code hyperlinks in the
help system, and ‘edebug’.  Then, for bonus points and maximising the
ability for the user to experiment quickly with code changes, the system
should allow parts of the source code to be modified and reloaded into
the running program, to take immediate effect.

   Guile is designed for this kind of interactive programming, and this
distinguishes it from many Scheme implementations that instead
prioritise running a fixed Scheme program as fast as possible—because
there are tradeoffs between performance and the ability to modify parts
of an already running program.  There are faster Schemes than Guile, but
Guile is a GNU project and so prioritises the GNU vision of programming
freedom and experimentation.

1.5 Supporting Multiple Languages
=================================

Since the 2.0 release, Guile’s architecture supports compiling any
language to its core virtual machine bytecode, and Scheme is just one of
the supported languages.  Other supported languages are Emacs Lisp,
ECMAScript (commonly known as Javascript) and Brainfuck, and work is
under discussion for Lua, Ruby and Python.

   This means that users can program applications which use Guile in the
language of their choice, rather than having the tastes of the
application’s author imposed on them.

1.6 Obtaining and Installing Guile
==================================

Guile can be obtained from the main GNU archive site <ftp://ftp.gnu.org>
or any of its mirrors.  The file will be named guile-VERSION.tar.gz.
The current version is 2.0.11, so the file you should grab is:

   <ftp://ftp.gnu.org/gnu/guile/guile-2.0.11.tar.gz>

   To unbundle Guile use the instruction

     zcat guile-2.0.11.tar.gz | tar xvf -

which will create a directory called ‘guile-2.0.11’ with all the
sources.  You can look at the file ‘INSTALL’ for detailed instructions
on how to build and install Guile, but you should be able to just do

     cd guile-2.0.11
     ./configure
     make
     make install

   This will install the Guile executable ‘guile’, the Guile library
‘libguile’ and various associated header files and support libraries.
It will also install the Guile reference manual.

   Since this manual frequently refers to the Scheme “standard”, also
known as R5RS, or the “Revised^5 Report on the Algorithmic Language
Scheme”, we have included the report in the Guile distribution; see
*note Introduction: (r5rs)Top.  This will also be installed in your info
directory.

1.7 Organisation of this Manual
===============================

The rest of this manual is organised into the following chapters.

*Chapter 2: Hello Guile!*
     A whirlwind tour shows how Guile can be used interactively and as a
     script interpreter, how to link Guile into your own applications,
     and how to write modules of interpreted and compiled code for use
     with Guile.  Everything introduced here is documented again and in
     full by the later parts of the manual.

*Chapter 3: Hello Scheme!*
     For readers new to Scheme, this chapter provides an introduction to
     the basic ideas of the Scheme language.  This material would apply
     to any Scheme implementation and so does not make reference to
     anything Guile-specific.

*Chapter 4: Programming in Scheme*
     Provides an overview of programming in Scheme with Guile.  It
     covers how to invoke the ‘guile’ program from the command-line and
     how to write scripts in Scheme.  It also introduces the extensions
     that Guile offers beyond standard Scheme.

*Chapter 5: Programming in C*
     Provides an overview of how to use Guile in a C program.  It
     discusses the fundamental concepts that you need to understand to
     access the features of Guile, such as dynamic types and the garbage
     collector.  It explains in a tutorial like manner how to define new
     data types and functions for the use by Scheme programs.

*Chapter 6: Guile API Reference*
     This part of the manual documents the Guile API in
     functionality-based groups with the Scheme and C interfaces
     presented side by side.

*Chapter 7: Guile Modules*
     Describes some important modules, distributed as part of the Guile
     distribution, that extend the functionality provided by the Guile
     Scheme core.

*Chapter 8: GOOPS*
     Describes GOOPS, an object oriented extension to Guile that
     provides classes, multiple inheritance and generic functions.

1.8 Typographical Conventions
=============================

In examples and procedure descriptions and all other places where the
evaluation of Scheme expression is shown, we use some notation for
denoting the output and evaluation results of expressions.

   The symbol ‘⇒’ is used to tell which value is returned by an
evaluation:

     (+ 1 2)
     ⇒ 3

   Some procedures produce some output besides returning a value.  This
is denoted by the symbol ‘⊣’.

     (begin (display 1) (newline) 'hooray)
     ⊣ 1
     ⇒ hooray

   As you can see, this code prints ‘1’ (denoted by ‘⊣’), and returns
‘hooray’ (denoted by ‘⇒’).

