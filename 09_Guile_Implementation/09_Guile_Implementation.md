9 Guile Implementation
**********************

At some point, after one has been programming in Scheme for some time,
another level of Scheme comes into view: its implementation.  Knowledge
of how Scheme can be implemented turns out to be necessary to become an
expert hacker.  As Peter Norvig notes in his retrospective on PAIP(1),
“The expert Lisp programmer eventually develops a good ‘efficiency
model’.”

   By this Norvig means that over time, the Lisp hacker eventually
develops an understanding of how much her code “costs” in terms of space
and time.

   This chapter describes Guile as an implementation of Scheme: its
history, how it represents and evaluates its data, and its compiler.
This knowledge can help you to make that step from being one who is
merely familiar with Scheme to being a real hacker.

   ---------- Footnotes ----------

   (1) PAIP is the common abbreviation for ‘Paradigms of Artificial
Intelligence Programming’, an old but still useful text on Lisp.
Norvig’s retrospective sums up the lessons of PAIP, and can be found at
<http://norvig.com/Lisp-retro.html>.

9.1 A Brief History of Guile
============================

Guile is an artifact of historical processes, both as code and as a
community of hackers.  It is sometimes useful to know this history when
hacking the source code, to know about past decisions and future
directions.

   Of course, the real history of Guile is written by the hackers
hacking and not the writers writing, so we round up the section with a
note on current status and future directions.

9.1.1 The Emacs Thesis
----------------------

The story of Guile is the story of bringing the development experience
of Emacs to the mass of programs on a GNU system.

   Emacs, when it was first created in its GNU form in 1984, was a new
take on the problem of “how to make a program”.  The Emacs thesis is
that it is delightful to create composite programs based on an
orthogonal kernel written in a low-level language together with a
powerful, high-level extension language.

   Extension languages foster extensible programs, programs which adapt
readily to different users and to changing times.  Proof of this can be
seen in Emacs’ current and continued existence, spanning more than a
quarter-century.

   Besides providing for modification of a program by others, extension
languages are good for _intension_ as well.  Programs built in “the
Emacs way” are pleasurable and easy for their authors to flesh out with
the features that they need.

   After the Emacs experience was appreciated more widely, a number of
hackers started to consider how to spread this experience to the rest of
the GNU system.  It was clear that the easiest way to Emacsify a program
would be to embed a shared language implementation into it.

9.1.2 Early Days
----------------

Tom Lord was the first to fully concentrate his efforts on an embeddable
language runtime, which he named “GEL”, the GNU Extension Language.

   GEL was the product of converting SCM, Aubrey Jaffer’s implementation
of Scheme, into something more appropriate to embedding as a library.
(SCM was itself based on an implementation by George Carrette, SIOD.)

   Lord managed to convince Richard Stallman to dub GEL the official
extension language for the GNU project.  It was a natural fit, given
that Scheme was a cleaner, more modern Lisp than Emacs Lisp.  Part of
the argument was that eventually when GEL became more capable, it could
gain the ability to execute other languages, especially Emacs Lisp.

   Due to a naming conflict with another programming language, Jim
Blandy suggested a new name for GEL: “Guile”.  Besides being a recursive
acronym, “Guile” craftily follows the naming of its ancestors,
“Planner”, “Conniver”, and “Schemer”.  (The latter was truncated to
“Scheme” due to a 6-character file name limit on an old operating
system.)  Finally, “Guile” suggests “guy-ell”, or “Guy L. Steele”, who,
together with Gerald Sussman, originally discovered Scheme.

   Around the same time that Guile (then GEL) was readying itself for
public release, another extension language was gaining in popularity,
Tcl.  Many developers found advantages in Tcl because of its shell-like
syntax and its well-developed graphical widgets library, Tk.  Also, at
the time there was a large marketing push promoting Tcl as a “universal
extension language”.

   Richard Stallman, as the primary author of GNU Emacs, had a
particular vision of what extension languages should be, and Tcl did not
seem to him to be as capable as Emacs Lisp.  He posted a criticism to
the comp.lang.tcl newsgroup, sparking one of the internet’s legendary
flamewars.  As part of these discussions, retrospectively dubbed the
“Tcl Wars”, he announced the Free Software Foundation’s intent to
promote Guile as the extension language for the GNU project.

   It is a common misconception that Guile was created as a reaction to
Tcl.  While it is true that the public announcement of Guile happened at
the same time as the “Tcl wars”, Guile was created out of a condition
that existed outside the polemic.  Indeed, the need for a powerful
language to bridge the gap between extension of existing applications
and a more fully dynamic programming environment is still with us today.

9.1.3 A Scheme of Many Maintainers
----------------------------------

Surveying the field, it seems that Scheme implementations correspond
with their maintainers on an N-to-1 relationship.  That is to say, that
those people that implement Schemes might do so on a number of
occasions, but that the lifetime of a given Scheme is tied to the
maintainership of one individual.

   Guile is atypical in this regard.

   Tom Lord maintained Guile for its first year and a half or so,
corresponding to the end of 1994 through the middle of 1996.  The
releases made in this time constitute an arc from SCM as a standalone
program to Guile as a reusable, embeddable library, but passing through
a explosion of features: embedded Tcl and Tk, a toolchain for compiling
and disassembling Java, addition of a C-like syntax, creation of a
module system, and a start at a rich POSIX interface.

   Only some of those features remain in Guile.  There were ongoing
tensions between providing a small, embeddable language, and one which
had all of the features (e.g. a graphical toolkit) that a modern Emacs
might need.  In the end, as Guile gained in uptake, the development team
decided to focus on depth, documentation and orthogonality rather than
on breadth.  This has been the focus of Guile ever since, although there
is a wide range of third-party libraries for Guile.

   Jim Blandy presided over that period of stabilization, in the three
years until the end of 1999, when he too moved on to other projects.
Since then, Guile has had a group maintainership.  The first group was
Maciej Stachowiak, Mikael Djurfeldt, and Marius Vollmer, with Vollmer
staying on the longest.  By late 2007, Vollmer had mostly moved on to
other things, so Neil Jerram and Ludovic Courtès stepped up to take on
the primary maintenance responsibility.  Jerram and Courtès were joined
by Andy Wingo in late 2009.

   Of course, a large part of the actual work on Guile has come from
other contributors too numerous to mention, but without whom the world
would be a poorer place.

9.1.4 A Timeline of Selected Guile Releases
-------------------------------------------

guile-i — 4 February 1995
     SCM, turned into a library.

guile-ii — 6 April 1995
     A low-level module system was added.  Tcl/Tk support was added,
     allowing extension of Scheme by Tcl or vice versa.  POSIX support
     was improved, and there was an experimental stab at Java
     integration.

guile-iii — 18 August 1995
     The C-like syntax, ctax, was improved, but mostly this release
     featured a start at the task of breaking Guile into pieces.

1.0 — 5 January 1997
     ‘#f’ was distinguished from ‘'()’.  User-level, cooperative
     multi-threading was added.  Source-level debugging became more
     useful, and programmer’s and user’s manuals were begun.  The module
     system gained a high-level interface, which is still used today in
     more or less the same form.

1.1 — 16 May 1997
1.2 — 24 June 1997
     Support for Tcl/Tk and ctax were split off as separate packages,
     and have remained there since.  Guile became more compatible with
     SCSH, and more useful as a UNIX scripting language.  Libguile could
     now be built as a shared library, and third-party extensions
     written in C became loadable via dynamic linking.

1.3.0 — 19 October 1998
     Command-line editing became much more pleasant through the use of
     the readline library.  The initial support for internationalization
     via multi-byte strings was removed; 10 years were to pass before
     proper internationalization would land again.  Initial Emacs Lisp
     support landed, ports gained better support for file descriptors,
     and fluids were added.

1.3.2 — 20 August 1999
1.3.4 — 25 September 1999
1.4 — 21 June 2000
     A long list of lispy features were added: hooks, Common Lisp’s
     ‘format’, optional and keyword procedure arguments, ‘getopt-long’,
     sorting, random numbers, and many other fixes and enhancements.
     Guile also gained an interactive debugger, interactive help, and
     better backtraces.

1.6 — 6 September 2002
     Guile gained support for the R5RS standard, and added a number of
     SRFI modules.  The module system was expanded with programmatic
     support for identifier selection and renaming.  The GOOPS object
     system was merged into Guile core.

1.8 — 20 February 2006
     Guile’s arbitrary-precision arithmetic switched to use the GMP
     library, and added support for exact rationals.  Guile’s embedded
     user-space threading was removed in favor of POSIX pre-emptive
     threads, providing true multiprocessing.  Gettext support was
     added, and Guile’s C API was cleaned up and orthogonalized in a
     massive way.

2.0 — 16 February 2010
     A virtual machine was added to Guile, along with the associated
     compiler and toolchain.  Support for internationalization was
     finally reimplemented, in terms of unicode, locales, and
     libunistring.  Running Guile instances became controllable and
     debuggable from within Emacs, via Geiser.  Guile caught up to
     features found in a number of other Schemes: SRFI-18 threads,
     module-hygienic macros, a profiler, tracer, and debugger, SSAX XML
     integration, bytevectors, a dynamic FFI, delimited continuations,
     module versions, and partial support for R6RS.

9.1.5 Status, or: Your Help Needed
----------------------------------

Guile has achieved much of what it set out to achieve, but there is much
remaining to do.

   There is still the old problem of bringing existing applications into
a more Emacs-like experience.  Guile has had some successes in this
respect, but still most applications in the GNU system are without Guile
integration.

   Getting Guile to those applications takes an investment, the
“hacktivation energy” needed to wire Guile into a program that only pays
off once it is good enough to enable new kinds of behavior.  This would
be a great way for new hackers to contribute: take an application that
you use and that you know well, think of something that it can’t yet do,
and figure out a way to integrate Guile and implement that task in
Guile.

   With time, perhaps this exposure can reverse itself, whereby programs
can run under Guile instead of vice versa, eventually resulting in the
Emacsification of the entire GNU system.  Indeed, this is the reason for
the naming of the many Guile modules that live in the ‘ice-9’ namespace,
a nod to the fictional substance in Kurt Vonnegut’s novel, Cat’s Cradle,
capable of acting as a seed crystal to crystallize the mass of software.

   Implicit to this whole discussion is the idea that dynamic languages
are somehow better than languages like C. While languages like C have
their place, Guile’s take on this question is that yes, Scheme is more
expressive than C, and more fun to write.  This realization carries an
imperative with it to write as much code in Scheme as possible rather
than in other languages.

   These days it is possible to write extensible applications almost
entirely from high-level languages, through byte-code and native
compilation, speed gains in the underlying hardware, and foreign call
interfaces in the high-level language.  Smalltalk systems are like this,
as are Common Lisp-based systems.  While there already are a number of
pure-Guile applications out there, users still need to drop down to C
for some tasks: interfacing to system libraries that don’t have prebuilt
Guile interfaces, and for some tasks requiring high performance.

   The addition of the virtual machine in Guile 2.0, together with the
compiler infrastructure, should go a long way to addressing the speed
issues.  But there is much optimization to be done.  Interested
contributors will find lots of delightful low-hanging fruit, from simple
profile-driven optimization to hacking a just-in-time compiler from VM
bytecode to native code.

   Still, even with an all-Guile application, sometimes you want to
provide an opportunity for users to extend your program from a language
with a syntax that is closer to C, or to Python.  Another interesting
idea to consider is compiling e.g. Python to Guile.  It’s not that
far-fetched of an idea: see for example IronPython or JRuby.

   And then there’s Emacs itself.  Though there is a somewhat-working
Emacs Lisp language frontend for Guile, it cannot yet execute all of
Emacs Lisp.  A serious integration of Guile with Emacs would replace the
Elisp virtual machine with Guile, and provide the necessary C shims so
that Guile could emulate Emacs’ C API. This would give lots of exciting
things to Emacs: native threads, a real object system, more
sophisticated types, cleaner syntax, and access to all of the Guile
extensions.

   Finally, there is another axis of crystallization, the axis between
different Scheme implementations.  Guile does not yet support the latest
Scheme standard, R6RS, and should do so.  Like all standards, R6RS is
imperfect, but supporting it will allow more code to run on Guile
without modification, and will allow Guile hackers to produce code
compatible with other schemes.  Help in this regard would be much
appreciated.

9.2 Data Representation
=======================

Scheme is a latently-typed language; this means that the system cannot,
in general, determine the type of a given expression at compile time.
Types only become apparent at run time.  Variables do not have fixed
types; a variable may hold a pair at one point, an integer at the next,
and a thousand-element vector later.  Instead, values, not variables,
have fixed types.

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

   The following sections will present a simple typing system, and then
make some refinements to correct its major weaknesses.  We then conclude
with a discussion of specific choices that Guile has made regarding
garbage collection and data representation.

9.2.1 A Simple Representation
-----------------------------

The simplest way to represent Scheme values in C would be to represent
each value as a pointer to a structure containing a type indicator,
followed by a union carrying the real value.  Assuming that ‘SCM’ is the
name of our universal type, we can write:

     enum type { integer, pair, string, vector, ... };

     typedef struct value *SCM;

     struct value {
       enum type type;
       union {
         int integer;
         struct { SCM car, cdr; } pair;
         struct { int length; char *elts; } string;
         struct { int length; SCM  *elts; } vector;
         ...
       } value;
     };
   with the ellipses replaced with code for the remaining Scheme types.

   This representation is sufficient to implement all of Scheme’s
semantics.  If X is an ‘SCM’ value:
   • To test if X is an integer, we can write ‘X->type == integer’.
   • To find its value, we can write ‘X->value.integer’.
   • To test if X is a vector, we can write ‘X->type == vector’.
   • If we know X is a vector, we can write ‘X->value.vector.elts[0]’ to
     refer to its first element.
   • If we know X is a pair, we can write ‘X->value.pair.car’ to extract
     its car.

9.2.2 Faster Integers
---------------------

Unfortunately, the above representation has a serious disadvantage.  In
order to return an integer, an expression must allocate a ‘struct
value’, initialize it to represent that integer, and return a pointer to
it.  Furthermore, fetching an integer’s value requires a memory
reference, which is much slower than a register reference on most
processors.  Since integers are extremely common, this representation is
too costly, in both time and space.  Integers should be very cheap to
create and manipulate.

   One possible solution comes from the observation that, on many
architectures, heap-allocated data (i.e., what you get when you call
‘malloc’) must be aligned on an eight-byte boundary.  (Whether or not
the machine actually requires it, we can write our own allocator for
‘struct value’ objects that assures this is true.)  In this case, the
lower three bits of the structure’s address are known to be zero.

   This gives us the room we need to provide an improved representation
for integers.  We make the following rules:
   • If the lower three bits of an ‘SCM’ value are zero, then the SCM
     value is a pointer to a ‘struct value’, and everything proceeds as
     before.
   • Otherwise, the ‘SCM’ value represents an integer, whose value
     appears in its upper bits.

   Here is C code implementing this convention:
     enum type { pair, string, vector, ... };

     typedef struct value *SCM;

     struct value {
       enum type type;
       union {
         struct { SCM car, cdr; } pair;
         struct { int length; char *elts; } string;
         struct { int length; SCM  *elts; } vector;
         ...
       } value;
     };

     #define POINTER_P(x) (((int) (x) & 7) == 0)
     #define INTEGER_P(x) (! POINTER_P (x))

     #define GET_INTEGER(x)  ((int) (x) >> 3)
     #define MAKE_INTEGER(x) ((SCM) (((x) << 3) | 1))

   Notice that ‘integer’ no longer appears as an element of ‘enum type’,
and the union has lost its ‘integer’ member.  Instead, we use the
‘POINTER_P’ and ‘INTEGER_P’ macros to make a coarse classification of
values into integers and non-integers, and do further type testing as
before.

   Here’s how we would answer the questions posed above (again, assume X
is an ‘SCM’ value):
   • To test if X is an integer, we can write ‘INTEGER_P (X)’.
   • To find its value, we can write ‘GET_INTEGER (X)’.
   • To test if X is a vector, we can write:
            POINTER_P (X) && X->type == vector
     Given the new representation, we must make sure X is truly a
     pointer before we dereference it to determine its complete type.
   • If we know X is a vector, we can write ‘X->value.vector.elts[0]’ to
     refer to its first element, as before.
   • If we know X is a pair, we can write ‘X->value.pair.car’ to extract
     its car, just as before.

   This representation allows us to operate more efficiently on integers
than the first.  For example, if X and Y are known to be integers, we
can compute their sum as follows:
     MAKE_INTEGER (GET_INTEGER (X) + GET_INTEGER (Y))
   Now, integer math requires no allocation or memory references.  Most
real Scheme systems actually implement addition and other operations
using an even more efficient algorithm, but this essay isn’t about
bit-twiddling.  (Hint: how do you decide when to overflow to a bignum?
How would you do it in assembly?)

9.2.3 Cheaper Pairs
-------------------

However, there is yet another issue to confront.  Most Scheme heaps
contain more pairs than any other type of object; Jonathan Rees said at
one point that pairs occupy 45% of the heap in his Scheme
implementation, Scheme 48.  However, our representation above spends
three ‘SCM’-sized words per pair — one for the type, and two for the CAR
and CDR.  Is there any way to represent pairs using only two words?

   Let us refine the convention we established earlier.  Let us assert
that:
   • If the bottom three bits of an ‘SCM’ value are ‘#b000’, then it is
     a pointer, as before.
   • If the bottom three bits are ‘#b001’, then the upper bits are an
     integer.  This is a bit more restrictive than before.
   • If the bottom two bits are ‘#b010’, then the value, with the bottom
     three bits masked out, is the address of a pair.

   Here is the new C code:
     enum type { string, vector, ... };

     typedef struct value *SCM;

     struct value {
       enum type type;
       union {
         struct { int length; char *elts; } string;
         struct { int length; SCM  *elts; } vector;
         ...
       } value;
     };

     struct pair {
       SCM car, cdr;
     };

     #define POINTER_P(x) (((int) (x) & 7) == 0)

     #define INTEGER_P(x)  (((int) (x) & 7) == 1)
     #define GET_INTEGER(x)  ((int) (x) >> 3)
     #define MAKE_INTEGER(x) ((SCM) (((x) << 3) | 1))

     #define PAIR_P(x) (((int) (x) & 7) == 2)
     #define GET_PAIR(x) ((struct pair *) ((int) (x) & ~7))

   Notice that ‘enum type’ and ‘struct value’ now only contain
provisions for vectors and strings; both integers and pairs have become
special cases.  The code above also assumes that an ‘int’ is large
enough to hold a pointer, which isn’t generally true.

   Our list of examples is now as follows:
   • To test if X is an integer, we can write ‘INTEGER_P (X)’; this is
     as before.
   • To find its value, we can write ‘GET_INTEGER (X)’, as before.
   • To test if X is a vector, we can write:
            POINTER_P (X) && X->type == vector
     We must still make sure that X is a pointer to a ‘struct value’
     before dereferencing it to find its type.
   • If we know X is a vector, we can write ‘X->value.vector.elts[0]’ to
     refer to its first element, as before.
   • We can write ‘PAIR_P (X)’ to determine if X is a pair, and then
     write ‘GET_PAIR (X)->car’ to refer to its car.

   This change in representation reduces our heap size by 15%.  It also
makes it cheaper to decide if a value is a pair, because no memory
references are necessary; it suffices to check the bottom two bits of
the ‘SCM’ value.  This may be significant when traversing lists, a
common activity in a Scheme system.

   Again, most real Scheme systems use a slightly different
implementation; for example, if GET_PAIR subtracts off the low bits of
‘x’, instead of masking them off, the optimizer will often be able to
combine that subtraction with the addition of the offset of the
structure member we are referencing, making a modified pointer as fast
to use as an unmodified pointer.

9.2.4 Conservative Garbage Collection
-------------------------------------

Aside from the latent typing, the major source of constraints on a
Scheme implementation’s data representation is the garbage collector.
The collector must be able to traverse every live object in the heap, to
determine which objects are not live, and thus collectable.

   There are many ways to implement this.  Guile’s garbage collection is
built on a library, the Boehm-Demers-Weiser conservative garbage
collector (BDW-GC). The BDW-GC “just works”, for the most part.  But
since it is interesting to know how these things work, we include here a
high-level description of what the BDW-GC does.

   Garbage collection has two logical phases: a "mark" phase, in which
the set of live objects is enumerated, and a "sweep" phase, in which
objects not traversed in the mark phase are collected.  Correct
functioning of the collector depends on being able to traverse the
entire set of live objects.

   In the mark phase, the collector scans the system’s global variables
and the local variables on the stack to determine which objects are
immediately accessible by the C code.  It then scans those objects to
find the objects they point to, and so on.  The collector logically sets
a "mark bit" on each object it finds, so each object is traversed only
once.

   When the collector can find no unmarked objects pointed to by marked
objects, it assumes that any objects that are still unmarked will never
be used by the program (since there is no path of dereferences from any
global or local variable that reaches them) and deallocates them.

   In the above paragraphs, we did not specify how the garbage collector
finds the global and local variables; as usual, there are many different
approaches.  Frequently, the programmer must maintain a list of pointers
to all global variables that refer to the heap, and another list
(adjusted upon entry to and exit from each function) of local variables,
for the collector’s benefit.

   The list of global variables is usually not too difficult to
maintain, since global variables are relatively rare.  However, an
explicitly maintained list of local variables (in the author’s personal
experience) is a nightmare to maintain.  Thus, the BDW-GC uses a
technique called "conservative garbage collection", to make the local
variable list unnecessary.

   The trick to conservative collection is to treat the stack as an
ordinary range of memory, and assume that _every_ word on the stack is a
pointer into the heap.  Thus, the collector marks all objects whose
addresses appear anywhere in the stack, without knowing for sure how
that word is meant to be interpreted.

   In addition to the stack, the BDW-GC will also scan static data
sections.  This means that global variables are also scanned when
looking for live Scheme objects.

   Obviously, such a system will occasionally retain objects that are
actually garbage, and should be freed.  In practice, this is not a
problem.  The alternative, an explicitly maintained list of local
variable addresses, is effectively much less reliable, due to programmer
error.  Interested readers should see the BDW-GC web page at
<http://www.hpl.hp.com/personal/Hans_Boehm/gc>, for more information.

9.2.5 The SCM Type in Guile
---------------------------

Guile classifies Scheme objects into two kinds: those that fit entirely
within an ‘SCM’, and those that require heap storage.

   The former class are called "immediates".  The class of immediates
includes small integers, characters, boolean values, the empty list, the
mysterious end-of-file object, and some others.

   The remaining types are called, not surprisingly, "non-immediates".
They include pairs, procedures, strings, vectors, and all other data
types in Guile.  For non-immediates, the ‘SCM’ word contains a pointer
to data on the heap, with further information about the object in
question is stored in that data.

   This section describes how the ‘SCM’ type is actually represented and
used at the C level.  Interested readers should see ‘libguile/tags.h’
for an exposition of how Guile stores type information.

   In fact, there are two basic C data types to represent objects in
Guile: ‘SCM’ and ‘scm_t_bits’.

9.2.5.1 Relationship between ‘SCM’ and ‘scm_t_bits’
...................................................

A variable of type ‘SCM’ is guaranteed to hold a valid Scheme object.  A
variable of type ‘scm_t_bits’, on the other hand, may hold a
representation of a ‘SCM’ value as a C integral type, but may also hold
any C value, even if it does not correspond to a valid Scheme object.

   For a variable X of type ‘SCM’, the Scheme object’s type information
is stored in a form that is not directly usable.  To be able to work on
the type encoding of the scheme value, the ‘SCM’ variable has to be
transformed into the corresponding representation as a ‘scm_t_bits’
variable Y by using the ‘SCM_UNPACK’ macro.  Once this has been done,
the type of the scheme object X can be derived from the content of the
bits of the ‘scm_t_bits’ value Y, in the way illustrated by the example
earlier in this chapter (*note Cheaper Pairs::).  Conversely, a valid
bit encoding of a Scheme value as a ‘scm_t_bits’ variable can be
transformed into the corresponding ‘SCM’ value using the ‘SCM_PACK’
macro.

9.2.5.2 Immediate objects
.........................

A Scheme object may either be an immediate, i.e. carrying all necessary
information by itself, or it may contain a reference to a "cell" with
additional information on the heap.  Although in general it should be
irrelevant for user code whether an object is an immediate or not,
within Guile’s own code the distinction is sometimes of importance.
Thus, the following low level macro is provided:

 -- Macro: int SCM_IMP (SCM X)
     A Scheme object is an immediate if it fulfills the ‘SCM_IMP’
     predicate, otherwise it holds an encoded reference to a heap cell.
     The result of the predicate is delivered as a C style boolean
     value.  User code and code that extends Guile should normally not
     be required to use this macro.

Summary:
   • Given a Scheme object X of unknown type, check first with ‘SCM_IMP
     (X)’ if it is an immediate object.
   • If so, all of the type and value information can be determined from
     the ‘scm_t_bits’ value that is delivered by ‘SCM_UNPACK (X)’.

   There are a number of special values in Scheme, most of them
documented elsewhere in this manual.  It’s not quite the right place to
put them, but for now, here’s a list of the C names given to some of
these values:

 -- Macro: SCM SCM_EOL
     The Scheme empty list object, or “End Of List” object, usually
     written in Scheme as ‘'()’.

 -- Macro: SCM SCM_EOF_VAL
     The Scheme end-of-file value.  It has no standard written
     representation, for obvious reasons.

 -- Macro: SCM SCM_UNSPECIFIED
     The value returned by some (but not all) expressions that the
     Scheme standard says return an “unspecified” value.

     This is sort of a weirdly literal way to take things, but the
     standard read-eval-print loop prints nothing when the expression
     returns this value, so it’s not a bad idea to return this when you
     can’t think of anything else helpful.

 -- Macro: SCM SCM_UNDEFINED
     The “undefined” value.  Its most important property is that is not
     equal to any valid Scheme value.  This is put to various internal
     uses by C code interacting with Guile.

     For example, when you write a C function that is callable from
     Scheme and which takes optional arguments, the interpreter passes
     ‘SCM_UNDEFINED’ for any arguments you did not receive.

     We also use this to mark unbound variables.

 -- Macro: int SCM_UNBNDP (SCM X)
     Return true if X is ‘SCM_UNDEFINED’.  Note that this is not a check
     to see if X is ‘SCM_UNBOUND’.  History will not be kind to us.

9.2.5.3 Non-immediate objects
.............................

A Scheme object of type ‘SCM’ that does not fulfill the ‘SCM_IMP’
predicate holds an encoded reference to a heap cell.  This reference can
be decoded to a C pointer to a heap cell using the ‘SCM2PTR’ macro.  The
encoding of a pointer to a heap cell into a ‘SCM’ value is done using
the ‘PTR2SCM’ macro.

 -- Macro: scm_t_cell * SCM2PTR (SCM X)
     Extract and return the heap cell pointer from a non-immediate ‘SCM’
     object X.

 -- Macro: SCM PTR2SCM (scm_t_cell * X)
     Return a ‘SCM’ value that encodes a reference to the heap cell
     pointer X.

   Note that it is also possible to transform a non-immediate ‘SCM’
value by using ‘SCM_UNPACK’ into a ‘scm_t_bits’ variable.  However, the
result of ‘SCM_UNPACK’ may not be used as a pointer to a ‘scm_t_cell’:
only ‘SCM2PTR’ is guaranteed to transform a ‘SCM’ object into a valid
pointer to a heap cell.  Also, it is not allowed to apply ‘PTR2SCM’ to
anything that is not a valid pointer to a heap cell.

Summary:
   • Only use ‘SCM2PTR’ on ‘SCM’ values for which ‘SCM_IMP’ is false!
   • Don’t use ‘(scm_t_cell *) SCM_UNPACK (X)’!  Use ‘SCM2PTR (X)’
     instead!
   • Don’t use ‘PTR2SCM’ for anything but a cell pointer!

9.2.5.4 Allocating Cells
........................

Guile provides both ordinary cells with two slots, and double cells with
four slots.  The following two function are the most primitive way to
allocate such cells.

   If the caller intends to use it as a header for some other type, she
must pass an appropriate magic value in WORD_0, to mark it as a member
of that type, and pass whatever value as WORD_1, etc that the type
expects.  You should generally not need these functions, unless you are
implementing a new datatype, and thoroughly understand the code in
‘<libguile/tags.h>’.

   If you just want to allocate pairs, use ‘scm_cons’.

 -- Function: SCM scm_cell (scm_t_bits word_0, scm_t_bits word_1)
     Allocate a new cell, initialize the two slots with WORD_0 and
     WORD_1, and return it.

     Note that WORD_0 and WORD_1 are of type ‘scm_t_bits’.  If you want
     to pass a ‘SCM’ object, you need to use ‘SCM_UNPACK’.

 -- Function: SCM scm_double_cell (scm_t_bits word_0, scm_t_bits word_1,
          scm_t_bits word_2, scm_t_bits word_3)
     Like ‘scm_cell’, but allocates a double cell with four slots.

9.2.5.5 Heap Cell Type Information
..................................

Heap cells contain a number of entries, each of which is either a scheme
object of type ‘SCM’ or a raw C value of type ‘scm_t_bits’.  Which of
the cell entries contain Scheme objects and which contain raw C values
is determined by the first entry of the cell, which holds the cell type
information.

 -- Macro: scm_t_bits SCM_CELL_TYPE (SCM X)
     For a non-immediate Scheme object X, deliver the content of the
     first entry of the heap cell referenced by X.  This value holds the
     information about the cell type.

 -- Macro: void SCM_SET_CELL_TYPE (SCM X, scm_t_bits T)
     For a non-immediate Scheme object X, write the value T into the
     first entry of the heap cell referenced by X.  The value T must
     hold a valid cell type.

9.2.5.6 Accessing Cell Entries
..............................

For a non-immediate Scheme object X, the object type can be determined
by reading the cell type entry using the ‘SCM_CELL_TYPE’ macro.  For
each different type of cell it is known which cell entries hold Scheme
objects and which cell entries hold raw C data.  To access the different
cell entries appropriately, the following macros are provided.

 -- Macro: scm_t_bits SCM_CELL_WORD (SCM X, unsigned int N)
     Deliver the cell entry N of the heap cell referenced by the
     non-immediate Scheme object X as raw data.  It is illegal, to
     access cell entries that hold Scheme objects by using these macros.
     For convenience, the following macros are also provided.
        • SCM_CELL_WORD_0 (X) ⇒ SCM_CELL_WORD (X, 0)
        • SCM_CELL_WORD_1 (X) ⇒ SCM_CELL_WORD (X, 1)
        • …
        • SCM_CELL_WORD_N (X) ⇒ SCM_CELL_WORD (X, N)

 -- Macro: SCM SCM_CELL_OBJECT (SCM X, unsigned int N)
     Deliver the cell entry N of the heap cell referenced by the
     non-immediate Scheme object X as a Scheme object.  It is illegal,
     to access cell entries that do not hold Scheme objects by using
     these macros.  For convenience, the following macros are also
     provided.
        • SCM_CELL_OBJECT_0 (X) ⇒ SCM_CELL_OBJECT (X, 0)
        • SCM_CELL_OBJECT_1 (X) ⇒ SCM_CELL_OBJECT (X, 1)
        • …
        • SCM_CELL_OBJECT_N (X) ⇒ SCM_CELL_OBJECT (X, N)

 -- Macro: void SCM_SET_CELL_WORD (SCM X, unsigned int N, scm_t_bits W)
     Write the raw C value W into entry number N of the heap cell
     referenced by the non-immediate Scheme value X.  Values that are
     written into cells this way may only be read from the cells using
     the ‘SCM_CELL_WORD’ macros or, in case cell entry 0 is written,
     using the ‘SCM_CELL_TYPE’ macro.  For the special case of cell
     entry 0 it has to be made sure that W contains a cell type
     information which does not describe a Scheme object.  For
     convenience, the following macros are also provided.
        • SCM_SET_CELL_WORD_0 (X, W) ⇒ SCM_SET_CELL_WORD (X, 0, W)
        • SCM_SET_CELL_WORD_1 (X, W) ⇒ SCM_SET_CELL_WORD (X, 1, W)
        • …
        • SCM_SET_CELL_WORD_N (X, W) ⇒ SCM_SET_CELL_WORD (X, N, W)

 -- Macro: void SCM_SET_CELL_OBJECT (SCM X, unsigned int N, SCM O)
     Write the Scheme object O into entry number N of the heap cell
     referenced by the non-immediate Scheme value X.  Values that are
     written into cells this way may only be read from the cells using
     the ‘SCM_CELL_OBJECT’ macros or, in case cell entry 0 is written,
     using the ‘SCM_CELL_TYPE’ macro.  For the special case of cell
     entry 0 the writing of a Scheme object into this cell is only
     allowed if the cell forms a Scheme pair.  For convenience, the
     following macros are also provided.
        • SCM_SET_CELL_OBJECT_0 (X, O) ⇒ SCM_SET_CELL_OBJECT (X, 0, O)
        • SCM_SET_CELL_OBJECT_1 (X, O) ⇒ SCM_SET_CELL_OBJECT (X, 1, O)
        • …
        • SCM_SET_CELL_OBJECT_N (X, O) ⇒ SCM_SET_CELL_OBJECT (X, N, O)

Summary:
   • For a non-immediate Scheme object X of unknown type, get the type
     information by using ‘SCM_CELL_TYPE (X)’.
   • As soon as the cell type information is available, only use the
     appropriate access methods to read and write data to the different
     cell entries.

9.3 A Virtual Machine for Guile
===============================

Guile has both an interpreter and a compiler.  To a user, the difference
is transparent—interpreted and compiled procedures can call each other
as they please.

   The difference is that the compiler creates and interprets bytecode
for a custom virtual machine, instead of interpreting the S-expressions
directly.  Loading and running compiled code is faster than loading and
running source code.

   The virtual machine that does the bytecode interpretation is a part
of Guile itself.  This section describes the nature of Guile’s virtual
machine.

9.3.1 Why a VM?
---------------

For a long time, Guile only had an interpreter.  Guile’s interpreter
operated directly on the S-expression representation of Scheme source
code.

   But while the interpreter was highly optimized and hand-tuned, it
still performs many needless computations during the course of
evaluating an expression.  For example, application of a function to
arguments needlessly consed up the arguments in a list.  Evaluation of
an expression always had to figure out what the car of the expression is
– a procedure, a memoized form, or something else.  All values have to
be allocated on the heap.  Et cetera.

   The solution to this problem was to compile the higher-level
language, Scheme, into a lower-level language for which all of the
checks and dispatching have already been done—the code is instead
stripped to the bare minimum needed to “do the job”.

   The question becomes then, what low-level language to choose?  There
are many options.  We could compile to native code directly, but that
poses portability problems for Guile, as it is a highly cross-platform
project.

   So we want the performance gains that compilation provides, but we
also want to maintain the portability benefits of a single code path.
The obvious solution is to compile to a virtual machine that is present
on all Guile installations.

   The easiest (and most fun) way to depend on a virtual machine is to
implement the virtual machine within Guile itself.  This way the virtual
machine provides what Scheme needs (tail calls, multiple values,
‘call/cc’) and can provide optimized inline instructions for Guile
(‘cons’, ‘struct-ref’, etc.).

   So this is what Guile does.  The rest of this section describes that
VM that Guile implements, and the compiled procedures that run on it.

   Before moving on, though, we should note that though we spoke of the
interpreter in the past tense, Guile still has an interpreter.  The
difference is that before, it was Guile’s main evaluator, and so was
implemented in highly optimized C; now, it is actually implemented in
Scheme, and compiled down to VM bytecode, just like any other program.
(There is still a C interpreter around, used to bootstrap the compiler,
but it is not normally used at runtime.)

   The upside of implementing the interpreter in Scheme is that we
preserve tail calls and multiple-value handling between interpreted and
compiled code.  The downside is that the interpreter in Guile 2.0 is
slower than the interpreter in 1.8.  We hope the that the compiler’s
speed makes up for the loss!

   Also note that this decision to implement a bytecode compiler does
not preclude native compilation.  We can compile from bytecode to native
code at runtime, or even do ahead of time compilation.  More
possibilities are discussed in *note Extending the Compiler::.

9.3.2 VM Concepts
-----------------

Compiled code is run by a virtual machine (VM). Each thread has its own
VM. When a compiled procedure is run, Guile looks up the virtual machine
for the current thread and executes the procedure using that VM.

   Guile’s virtual machine is a stack machine—that is, it has few
registers, and the instructions defined in the VM operate by pushing and
popping values from a stack.

   Stack memory is exclusive to the virtual machine that owns it.  In
addition to their stacks, virtual machines also have access to the
global memory (modules, global bindings, etc) that is shared among other
parts of Guile, including other VMs.

   A VM has generic instructions, such as those to reference local
variables, and instructions designed to support Guile’s languages –
mathematical instructions that support the entire numerical tower, an
inlined implementation of ‘cons’, etc.

   The registers that a VM has are as follows:

   • ip - Instruction pointer
   • sp - Stack pointer
   • fp - Frame pointer

   In other architectures, the instruction pointer is sometimes called
the “program counter” (pc).  This set of registers is pretty typical for
stack machines; their exact meanings in the context of Guile’s VM are
described in the next section.

9.3.3 Stack Layout
------------------

While not strictly necessary to understand how to work with the VM, it
is instructive and sometimes entertaining to consider the structure of
the VM stack.

   Logically speaking, a VM stack is composed of “frames”.  Each frame
corresponds to the application of one compiled procedure, and contains
storage space for arguments, local variables, intermediate values, and
some bookkeeping information (such as what to do after the frame
computes its value).

   While the compiler is free to do whatever it wants to, as long as the
semantics of a computation are preserved, in practice every time you
call a function, a new frame is created.  (The notable exception of
course is the tail call case, *note Tail Calls::.)

   Within a frame, you have the data associated with the function
application itself, which is of a fixed size, and the stack space for
intermediate values.  Sometimes only the former is referred to as the
“frame”, and the latter is the “stack”, although all pending application
frames can have some intermediate computations interleaved on the stack.

   The structure of the fixed part of an application frame is as
follows:

                  Stack
        | ...              |
        | Intermed. val. 0 | <- fp + bp->nargs + bp->nlocs = SCM_FRAME_UPPER_ADDRESS (fp)
        +==================+
        | Local variable 1 |
        | Local variable 0 | <- fp + bp->nargs
        | Argument 1       |
        | Argument 0       | <- fp
        | Program          | <- fp - 1
        +------------------+
        | Return address   |
        | MV return address|
        | Dynamic link     | <- fp - 4 = SCM_FRAME_DATA_ADDRESS (fp) = SCM_FRAME_LOWER_ADDRESS (fp)
        +==================+
        |                  |

   In the above drawing, the stack grows upward.  The intermediate
values stored in the application of this frame are stored above
‘SCM_FRAME_UPPER_ADDRESS (fp)’.  ‘bp’ refers to the ‘struct scm_objcode’
data associated with the program at ‘fp - 1’.  ‘nargs’ and ‘nlocs’ are
properties of the compiled procedure, which will be discussed later.

   The individual fields of the frame are as follows:

Return address
     The ‘ip’ that was in effect before this program was applied.  When
     we return from this activation frame, we will jump back to this
     ‘ip’.

MV return address
     The ‘ip’ to return to if this application returns multiple values.
     For continuations that only accept one value, this value will be
     ‘NULL’; for others, it will be an ‘ip’ that points to a
     multiple-value return address in the calling code.  That code will
     expect the top value on the stack to be an integer—the number of
     values being returned—and that below that integer there are the
     values being returned.

Dynamic link
     This is the ‘fp’ in effect before this program was applied.  In
     effect, this and the return address are the registers that are
     always “saved”.  The dynamic link links the current frame to the
     previous frame; computing a stack trace involves traversing these
     frames.

Local variable N
     Lambda-local variables that are all allocated as part of the frame.
     This makes access to variables very cheap.

Argument N
     The calling convention of the VM requires arguments of a function
     application to be pushed on the stack, and here they are.
     References to arguments dispatch to these locations on the stack.

Program
     This is the program being applied.  For more information on how
     programs are implemented, *Note VM Programs::.

9.3.4 Variables and the VM
--------------------------

Consider the following Scheme code as an example:

       (define (foo a)
         (lambda (b) (list foo a b)))

   Within the lambda expression, ‘foo’ is a top-level variable, ‘a’ is a
lexically captured variable, and ‘b’ is a local variable.

   Another way to refer to ‘a’ and ‘b’ is to say that ‘a’ is a “free”
variable, since it is not defined within the lambda, and ‘b’ is a
“bound” variable.  These are the terms used in the "lambda calculus", a
mathematical notation for describing functions.  The lambda calculus is
useful because it allows one to prove statements about functions.  It is
especially good at describing scope relations, and it is for that reason
that we mention it here.

   Guile allocates all variables on the stack.  When a lexically
enclosed procedure with free variables—a "closure"—is created, it copies
those variables into its free variable vector.  References to free
variables are then redirected through the free variable vector.

   If a variable is ever ‘set!’, however, it will need to be
heap-allocated instead of stack-allocated, so that different closures
that capture the same variable can see the same value.  Also, this
allows continuations to capture a reference to the variable, instead of
to its value at one point in time.  For these reasons, ‘set!’ variables
are allocated in “boxes”—actually, in variable cells.  *Note
Variables::, for more information.  References to ‘set!’ variables are
indirected through the boxes.

   Thus perhaps counterintuitively, what would seem “closer to the
metal”, viz ‘set!’, actually forces an extra memory allocation and
indirection.

   Going back to our example, ‘b’ may be allocated on the stack, as it
is never mutated.

   ‘a’ may also be allocated on the stack, as it too is never mutated.
Within the enclosed lambda, its value will be copied into (and
referenced from) the free variables vector.

   ‘foo’ is a top-level variable, because ‘foo’ is not lexically bound
in this example.

9.3.5 Compiled Procedures are VM Programs
-----------------------------------------

By default, when you enter in expressions at Guile’s REPL, they are
first compiled to VM object code, then that VM object code is executed
to produce a value.  If the expression evaluates to a procedure, the
result of this process is a compiled procedure.

   A compiled procedure is a compound object, consisting of its
bytecode, a reference to any captured lexical variables, an object
array, and some metadata such as the procedure’s arity, name, and
documentation.  You can pick apart these pieces with the accessors in
‘(system vm program)’.  *Note Compiled Procedures::, for a full API
reference.

   The object array of a compiled procedure, also known as the "object
table", holds all Scheme objects whose values are known not to change
across invocations of the procedure: constant strings, symbols, etc.
The object table of a program is initialized right before a program is
loaded with ‘load-program’.  *Note Loading Instructions::, for more
information.

   Variable objects are one such type of constant object: when a global
binding is defined, a variable object is associated to it and that
object will remain constant over time, even if the value bound to it
changes.  Therefore, toplevel bindings only need to be looked up once.
Thereafter, references to the corresponding toplevel variables from
within the program are then performed via the ‘toplevel-ref’
instruction, which uses the object vector, and are almost as fast as
local variable references.

   We can see how these concepts tie together by disassembling the ‘foo’
function we defined earlier to see what is going on:

     scheme@(guile-user)> (define (foo a) (lambda (b) (list foo a b)))
     scheme@(guile-user)> ,x foo
        0    (assert-nargs-ee/locals 1)
        2    (object-ref 1)                  ;; #<procedure 8ebec20 at <current input>:0:17 (b)>
        4    (local-ref 0)                   ;; `a'
        6    (make-closure 0 1)
        9    (return)

     ----------------------------------------
     Disassembly of #<procedure 8ebec20 at <current input>:0:17 (b)>:

        0    (assert-nargs-ee/locals 1)
        2    (toplevel-ref 1)                ;; `foo'
        4    (free-ref 0)                    ;; (closure variable)
        6    (local-ref 0)                   ;; `b'
        8    (list 0 3)                      ;; 3 elements         at (unknown file):0:29
       11    (return)

   First there’s some prelude, where ‘foo’ checks that it was called
with only 1 argument.  Then at ‘ip’ 2, we load up the compiled lambda.
‘Ip’ 4 loads up ‘a’, so that it can be captured into a closure by at
‘ip’ 6—binding code (from the compiled lambda) with data (the
free-variable vector).  Finally we return the closure.

   The second stanza disassembles the compiled lambda.  After the
prelude, we note that toplevel variables are resolved relative to the
module that was current when the procedure was created.  This lookup
occurs lazily, at the first time the variable is actually referenced,
and the location of the lookup is cached so that future references are
very cheap.  *Note Top-Level Environment Instructions::, for more
details.

   Then we see a reference to a free variable, corresponding to ‘a’.
The disassembler doesn’t have enough information to give a name to that
variable, so it just marks it as being a “closure variable”.  Finally we
see the reference to ‘b’, then the ‘list’ opcode, an inline
implementation of the ‘list’ scheme routine.

9.3.6 Instruction Set
---------------------

There are about 180 instructions in Guile’s virtual machine.  These
instructions represent atomic units of a program’s execution.  Ideally,
they perform one task without conditional branches, then dispatch to the
next instruction in the stream.

   Instructions themselves are one byte long.  Some instructions take
parameters, which follow the instruction byte in the instruction stream.

   Sometimes the compiler can figure out that it is compiling a special
case that can be run more efficiently.  So, for example, while Guile
offers a generic test-and-branch instruction, it also offers specific
instructions for special cases, so that the following cases all have
their own test-and-branch instructions:

     (if pred then else)
     (if (not pred) then else)
     (if (null? l) then else)
     (if (not (null? l)) then else)

   In addition, some Scheme primitives have their own inline
implementations, e.g. ‘cons’, and ‘list’, as we saw in the previous
section.

   So Guile’s instruction set is a _complete_ instruction set, in that
it provides the instructions that are suited to the problem, and is not
concerned with making a minimal, orthogonal set of instructions.  More
instructions may be added over time.

9.3.6.1 Lexical Environment Instructions
........................................

These instructions access and mutate the lexical environment of a
compiled procedure—its free and bound variables.

   Some of these instructions have ‘long-’ variants, the difference
being that they take 16-bit arguments, encoded in big-endianness,
instead of the normal 8-bit range.

   *Note Stack Layout::, for more information on the format of stack
frames.

 -- Instruction: local-ref index
 -- Instruction: long-local-ref index
     Push onto the stack the value of the local variable located at
     INDEX within the current stack frame.

     Note that arguments and local variables are all in one block.  Thus
     the first argument, if any, is at index 0, and local bindings
     follow the arguments.

 -- Instruction: local-set index
 -- Instruction: long-local-set index
     Pop the Scheme object located on top of the stack and make it the
     new value of the local variable located at INDEX within the current
     stack frame.

 -- Instruction: box index
     Pop a value off the stack, and set the INDEXnth local variable to a
     box containing that value.  A shortcut for ‘make-variable’ then
     ‘local-set’, used when binding boxed variables.

 -- Instruction: empty-box index
     Set the INDEXth local variable to a box containing a variable whose
     value is unbound.  Used when compiling some ‘letrec’ expressions.

 -- Instruction: local-boxed-ref index
 -- Instruction: local-boxed-set index
     Get or set the value of the variable located at INDEX within the
     current stack frame.  A shortcut for ‘local-ref’ then
     ‘variable-ref’ or ‘variable-set’, respectively.

 -- Instruction: free-ref index
     Push the value of the captured variable located at position INDEX
     within the program’s vector of captured variables.

 -- Instruction: free-boxed-ref index
 -- Instruction: free-boxed-set index
     Get or set a boxed free variable.  A shortcut for ‘free-ref’ then
     ‘variable-ref’ or ‘variable-set’, respectively.

     Note that there is no ‘free-set’ instruction, as variables that are
     ‘set!’ must be boxed.

 -- Instruction: make-closure num-free-vars
     Pop NUM-FREE-VARS values and a program object off the stack in that
     order, and push a new program object closing over the given free
     variables.  NUM-FREE-VARS is encoded as a two-byte big-endian
     value.

     The free variables are stored in an array, inline to the new
     program object, in the order that they were on the stack (not the
     order they are popped off).  The new closure shares state with the
     original program.  At the time of this writing, the space overhead
     of closures is 3 words, plus one word for each free variable.

 -- Instruction: fix-closure index
     Fix up the free variables array of the closure stored in the
     INDEXth local variable.  INDEX is a two-byte big-endian integer.

     This instruction will pop as many values from the stack as are in
     the corresponding closure’s free variables array.  The topmost
     value on the stack will be stored as the closure’s last free
     variable, with other values filling in free variable slots in
     order.

     ‘fix-closure’ is part of a hack for allocating mutually recursive
     procedures.  The hack is to store the procedures in their
     corresponding local variable slots, with space already allocated
     for free variables.  Then once they are all in place, this
     instruction fixes up their procedures’ free variable bindings in
     place.  This allows most ‘letrec’-bound procedures to be allocated
     unboxed on the stack.

 -- Instruction: local-bound? index
 -- Instruction: long-local-bound? index
     Push ‘#t’ on the stack if the ‘index’th local variable has been
     assigned, or ‘#f’ otherwise.  Mostly useful for handling optional
     arguments in procedure prologues.

9.3.6.2 Top-Level Environment Instructions
..........................................

These instructions access values in the top-level environment: bindings
that were not lexically apparent at the time that the code in question
was compiled.

   The location in which a toplevel binding is stored can be looked up
once and cached for later.  The binding itself may change over time, but
its location will stay constant.

   Currently only toplevel references within procedures are cached, as
only procedures have a place to cache them, in their object tables.

 -- Instruction: toplevel-ref index
 -- Instruction: long-toplevel-ref index
     Push the value of the toplevel binding whose location is stored in
     at position INDEX in the current procedure’s object table.  The
     ‘long-’ variant encodes the index over two bytes.

     Initially, a cell in a procedure’s object table that is used by
     ‘toplevel-ref’ is initialized to one of two forms.  The normal case
     is that the cell holds a symbol, whose binding will be looked up
     relative to the module that was current when the current program
     was created.

     Alternately, the lookup may be performed relative to a particular
     module, determined at compile-time (e.g. via ‘@’ or ‘@@’).  In that
     case, the cell in the object table holds a list: ‘(MODNAME SYM
     PUBLIC?)’.  The symbol SYM will be looked up in the module named
     MODNAME (a list of symbols).  The lookup will be performed against
     the module’s public interface, unless PUBLIC? is ‘#f’, which it is
     for example when compiling ‘@@’.

     In any case, if the symbol is unbound, an error is signalled.
     Otherwise the initial form is replaced with the looked-up variable,
     an in-place mutation of the object table.  This mechanism provides
     for lazy variable resolution, and an important cached fast-path
     once the variable has been successfully resolved.

     This instruction pushes the value of the variable onto the stack.

 -- Instruction: toplevel-set index
 -- Instruction: long-toplevel-set index
     Pop a value off the stack, and set it as the value of the toplevel
     variable stored at INDEX in the object table.  If the variable has
     not yet been looked up, we do the lookup as in ‘toplevel-ref’.

 -- Instruction: define
     Pop a symbol and a value from the stack, in that order.  Look up
     its binding in the current toplevel environment, creating the
     binding if necessary.  Set the variable to the value.

 -- Instruction: link-now
     Pop a value, X, from the stack.  Look up the binding for X,
     according to the rules for ‘toplevel-ref’, and push that variable
     on the stack.  If the lookup fails, an error will be signalled.

     This instruction is mostly used when loading programs, because it
     can do toplevel variable lookups without an object table.

 -- Instruction: variable-ref
     Dereference the variable object which is on top of the stack and
     replace it by the value of the variable it represents.

 -- Instruction: variable-set
     Pop off two objects from the stack, a variable and a value, and set
     the variable to the value.

 -- Instruction: variable-bound?
     Pop off the variable object from top of the stack and push ‘#t’ if
     it is bound, or ‘#f’ otherwise.  Mostly useful in procedure
     prologues for defining default values for boxed optional variables.

 -- Instruction: make-variable
     Replace the top object on the stack with a variable containing it.
     Used in some circumstances when compiling ‘letrec’ expressions.

9.3.6.3 Procedure Call and Return Instructions
..............................................

 -- Instruction: new-frame
     Push a new frame on the stack, reserving space for the dynamic
     link, return address, and the multiple-values return address.  The
     frame pointer is not yet updated, because the frame is not yet
     active – it has to be patched by a ‘call’ instruction to get the
     return address.

 -- Instruction: call nargs
     Call the procedure located at ‘sp[-nargs]’ with the NARGS arguments
     located from ‘sp[-nargs + 1]’ to ‘sp[0]’.

     This instruction requires that a new frame be pushed on the stack
     before the procedure, via ‘new-frame’.  *Note Stack Layout::, for
     more information.  It patches up that frame with the current ‘ip’
     as the return address, then dispatches to the first instruction in
     the called procedure, relying on the called procedure to return one
     value to the newly-created continuation.  Because the new frame
     pointer will point to ‘sp[-nargs + 1]’, the arguments don’t have to
     be shuffled around – they are already in place.

 -- Instruction: tail-call nargs
     Transfer control to the procedure located at ‘sp[-nargs]’ with the
     NARGS arguments located from ‘sp[-nargs + 1]’ to ‘sp[0]’.

     Unlike ‘call’, which requires a new frame to be pushed onto the
     stack, ‘tail-call’ simply shuffles down the procedure and arguments
     to the current stack frame.  This instruction implements tail calls
     as required by RnRS.

 -- Instruction: apply nargs
 -- Instruction: tail-apply nargs
     Like ‘call’ and ‘tail-call’, except that the top item on the stack
     must be a list.  The elements of that list are then pushed on the
     stack and treated as additional arguments, replacing the list
     itself, then the procedure is invoked as usual.

 -- Instruction: call/nargs
 -- Instruction: tail-call/nargs
     These are like ‘call’ and ‘tail-call’, except they take the number
     of arguments from the stack instead of the instruction stream.
     These instructions are used in the implementation of multiple value
     returns, where the actual number of values is pushed on the stack.

 -- Instruction: mv-call nargs offset
     Like ‘call’, except that a multiple-value continuation is created
     in addition to a single-value continuation.

     The offset (a three-byte value) is an offset within the instruction
     stream; the multiple-value return address in the new frame (*note
     Stack Layout::) will be set to the normal return address plus this
     offset.  Instructions at that offset will expect the top value of
     the stack to be the number of values, and below that values
     themselves, pushed separately.

 -- Instruction: return
     Free the program’s frame, returning the top value from the stack to
     the current continuation.  (The stack should have exactly one value
     on it.)

     Specifically, the ‘sp’ is decremented to one below the current
     ‘fp’, the ‘ip’ is reset to the current return address, the ‘fp’ is
     reset to the value of the current dynamic link, and then the
     returned value is pushed on the stack.

 -- Instruction: return/values nvalues
 -- Instruction: return/nvalues
     Return the top NVALUES to the current continuation.  In the case of
     ‘return/nvalues’, NVALUES itself is first popped from the top of
     the stack.

     If the current continuation is a multiple-value continuation,
     ‘return/values’ pushes the number of values on the stack, then
     returns as in ‘return’, but to the multiple-value return address.

     Otherwise if the current continuation accepts only one value, i.e.
     the multiple-value return address is ‘NULL’, then we assume the
     user only wants one value, and we give them the first one.  If
     there are no values, an error is signaled.

 -- Instruction: return/values* nvalues
     Like a combination of ‘apply’ and ‘return/values’, in which the top
     value on the stack is interpreted as a list of additional values.
     This is an optimization for the common ‘(apply values ...)’ case.

 -- Instruction: truncate-values nbinds nrest
     Used in multiple-value continuations, this instruction takes the
     values that are on the stack (including the number-of-values
     marker) and truncates them for a binding construct.

     For example, a call to ‘(receive (x y . z) (foo) ...)’ would,
     logically speaking, pop off the values returned from ‘(foo)’ and
     push them as three values, corresponding to ‘x’, ‘y’, and ‘z’.  In
     that case, NBINDS would be 3, and NREST would be 1 (to indicate
     that one of the bindings was a rest argument).

     Signals an error if there is an insufficient number of values.

 -- Instruction: call/cc
 -- Instruction: tail-call/cc
     Capture the current continuation, and then call (or tail-call) the
     procedure on the top of the stack, with the continuation as the
     argument.

     ‘call/cc’ does not require a ‘new-frame’ to be pushed on the stack,
     as ‘call’ does, because it needs to capture the stack before the
     frame is pushed.

     Both the VM continuation and the C continuation are captured.

9.3.6.4 Function Prologue Instructions
......................................

A function call in Guile is very cheap: the VM simply hands control to
the procedure.  The procedure itself is responsible for asserting that
it has been passed an appropriate number of arguments.  This strategy
allows arbitrarily complex argument parsing idioms to be developed,
without harming the common case.

   For example, only calls to keyword-argument procedures “pay” for the
cost of parsing keyword arguments.  (At the time of this writing,
calling procedures with keyword arguments is typically two to four times
as costly as calling procedures with a fixed set of arguments.)

 -- Instruction: assert-nargs-ee n
 -- Instruction: assert-nargs-ge n
     Assert that the current procedure has been passed exactly N
     arguments, for the ‘-ee’ case, or N or more arguments, for the
     ‘-ge’ case.  N is encoded over two bytes.

     The number of arguments is determined by subtracting the frame
     pointer from the stack pointer (‘sp - (fp -1)’).  *Note Stack
     Layout::, for more details on stack frames.

 -- Instruction: br-if-nargs-ne n offset
 -- Instruction: br-if-nargs-gt n offset
 -- Instruction: br-if-nargs-lt n offset
     Jump to OFFSET if the number of arguments is not equal to, greater
     than, or less than N.  N is encoded over two bytes, and OFFSET has
     the normal three-byte encoding.

     These instructions are used to implement multiple arities, as in
     ‘case-lambda’.  *Note Case-lambda::, for more information.

 -- Instruction: bind-optionals n
     If the procedure has been called with fewer than N arguments, fill
     in the remaining arguments with an unbound value (‘SCM_UNDEFINED’).
     N is encoded over two bytes.

     The optionals can be later initialized conditionally via the
     ‘local-bound?’ instruction.

 -- Instruction: push-rest n
     Pop off excess arguments (more than N), collecting them into a
     list, and push that list.  Used to bind a rest argument, if the
     procedure has no keyword arguments.  Procedures with keyword
     arguments use ‘bind-rest’ instead.

 -- Instruction: bind-rest n idx
     Pop off excess arguments (more than N), collecting them into a
     list.  The list is then assigned to the IDXth local variable.

 -- Instruction: bind-optionals/shuffle nreq nreq-and-opt ntotal
 -- Instruction: bind-optionals/shuffle-or-br nreq nreq-and-opt ntotal
          offset
     Shuffle keyword arguments to the top of the stack, filling in the
     holes with ‘SCM_UNDEFINED’.  Each argument is encoded over two
     bytes.

     This instruction is used by procedures with keyword arguments.
     NREQ is the number of required arguments to the procedure, and
     NREQ-AND-OPT is the total number of positional arguments (required
     plus optional).  ‘bind-optionals/shuffle’ will scan the stack from
     the NREQth argument up to the NREQ-AND-OPTth, and start shuffling
     when it sees the first keyword argument or runs out of positional
     arguments.

     ‘bind-optionals/shuffle-or-br’ does the same, except that it checks
     if there are too many positional arguments before shuffling.  If
     this is the case, it jumps to OFFSET, encoded using the normal
     three-byte encoding.

     Shuffling simply moves the keyword arguments past the total number
     of arguments, NTOTAL, which includes keyword and rest arguments.
     The free slots created by the shuffle are filled in with
     ‘SCM_UNDEFINED’, so they may be conditionally initialized later in
     the function’s prologue.

 -- Instruction: bind-kwargs idx ntotal flags
     Parse keyword arguments, assigning their values to the
     corresponding local variables.  The keyword arguments should
     already have been shuffled above the NTOTALth stack slot by
     ‘bind-optionals/shuffle’.

     The parsing is driven by a keyword arguments association list,
     looked up from the IDXth element of the procedures object array.
     The alist is a list of pairs of the form ‘(KW . INDEX)’, mapping
     keyword arguments to their local variable indices.

     There are two bitflags that affect the parser, ‘allow-other-keys?’
     (‘0x1’) and ‘rest?’ (‘0x2’).  Unless ‘allow-other-keys?’ is set,
     the parser will signal an error if an unknown key is found.  If
     ‘rest?’ is set, errors parsing the keyword arguments will be
     ignored, as a later ‘bind-rest’ instruction will collect all of the
     tail arguments, including the keywords, into a list.  Otherwise if
     the keyword arguments are invalid, an error is signalled.

     IDX and NTOTAL are encoded over two bytes each, and FLAGS is
     encoded over one byte.

 -- Instruction: reserve-locals n
     Resets the stack pointer to have space for N local variables,
     including the arguments.  If this operation increments the stack
     pointer, as in a push, the new slots are filled with ‘SCM_UNBOUND’.
     If this operation decrements the stack pointer, any excess values
     are dropped.

     ‘reserve-locals’ is typically used after argument parsing to
     reserve space for local variables.

 -- Instruction: assert-nargs-ee/locals n
 -- Instruction: assert-nargs-ge/locals n
     A combination of ‘assert-nargs-ee’ and ‘reserve-locals’.  The
     number of arguments is encoded in the lower three bits of N, a
     one-byte value.  The number of additional local variables is take
     from the upper 5 bits of N.

9.3.6.5 Trampoline Instructions
...............................

Though most applicable objects in Guile are procedures implemented in
bytecode, not all are.  There are primitives, continuations, and other
procedure-like objects that have their own calling convention.  Instead
of adding special cases to the ‘call’ instruction, Guile wraps these
other applicable objects in VM trampoline procedures, then provides
special support for these objects in bytecode.

   Trampoline procedures are typically generated by Guile at runtime,
for example in response to a call to ‘scm_c_make_gsubr’.  As such, a
compiler probably shouldn’t emit code with these instructions.  However,
it’s still interesting to know how these things work, so we document
these trampoline instructions here.

 -- Instruction: subr-call nargs
     Pop off a foreign pointer (which should have been pushed on by the
     trampoline), and call it directly, with the NARGS arguments from
     the stack.  Return the resulting value or values to the calling
     procedure.

 -- Instruction: foreign-call nargs
     Pop off an internal foreign object (which should have been pushed
     on by the trampoline), and call that foreign function with the
     NARGS arguments from the stack.  Return the resulting value to the
     calling procedure.

 -- Instruction: continuation-call
     Pop off an internal continuation object (which should have been
     pushed on by the trampoline), and reinstate that continuation.  All
     of the procedure’s arguments are passed to the continuation.  Does
     not return.

 -- Instruction: partial-cont-call
     Pop off two objects from the stack: the dynamic winds associated
     with the partial continuation, and the VM continuation object.
     Unroll the continuation onto the stack, rewinding the dynamic
     environment and overwriting the current frame, and pass all
     arguments to the continuation.  Control flow proceeds where the
     continuation was captured.

9.3.6.6 Branch Instructions
...........................

All the conditional branch instructions described below work in the same
way:

   • They pop off Scheme object(s) located on the stack for use in the
     branch condition
   • If the condition is true, then the instruction pointer is increased
     by the offset passed as an argument to the branch instruction;
   • Program execution proceeds with the next instruction (that is, the
     one to which the instruction pointer points).

   Note that the offset passed to the instruction is encoded as three
8-bit integers, in big-endian order, effectively giving Guile a 24-bit
relative address space.

 -- Instruction: br offset
     Jump to OFFSET.  No values are popped.

 -- Instruction: br-if offset
     Jump to OFFSET if the object on the stack is not false.

 -- Instruction: br-if-not offset
     Jump to OFFSET if the object on the stack is false.

 -- Instruction: br-if-eq offset
     Jump to OFFSET if the two objects located on the stack are equal in
     the sense of ‘eq?’.  Note that, for this instruction, the stack
     pointer is decremented by two Scheme objects instead of only one.

 -- Instruction: br-if-not-eq offset
     Same as ‘br-if-eq’ for non-‘eq?’ objects.

 -- Instruction: br-if-null offset
     Jump to OFFSET if the object on the stack is ‘'()’.

 -- Instruction: br-if-not-null offset
     Jump to OFFSET if the object on the stack is not ‘'()’.

9.3.6.7 Data Constructor Instructions
.....................................

These instructions push simple immediate values onto the stack, or
construct compound data structures from values on the stack.

 -- Instruction: make-int8 value
     Push VALUE, an 8-bit integer, onto the stack.

 -- Instruction: make-int8:0
     Push the immediate value ‘0’ onto the stack.

 -- Instruction: make-int8:1
     Push the immediate value ‘1’ onto the stack.

 -- Instruction: make-int16 value
     Push VALUE, a 16-bit integer, onto the stack.

 -- Instruction: make-uint64 value
     Push VALUE, an unsigned 64-bit integer, onto the stack.  The value
     is encoded in 8 bytes, most significant byte first (big-endian).

 -- Instruction: make-int64 value
     Push VALUE, a signed 64-bit integer, onto the stack.  The value is
     encoded in 8 bytes, most significant byte first (big-endian), in
     twos-complement arithmetic.

 -- Instruction: make-false
     Push ‘#f’ onto the stack.

 -- Instruction: make-true
     Push ‘#t’ onto the stack.

 -- Instruction: make-nil
     Push ‘#nil’ onto the stack.

 -- Instruction: make-eol
     Push ‘'()’ onto the stack.

 -- Instruction: make-char8 value
     Push VALUE, an 8-bit character, onto the stack.

 -- Instruction: make-char32 value
     Push VALUE, an 32-bit character, onto the stack.  The value is
     encoded in big-endian order.

 -- Instruction: make-symbol
     Pops a string off the stack, and pushes a symbol.

 -- Instruction: make-keyword value
     Pops a symbol off the stack, and pushes a keyword.

 -- Instruction: list n
     Pops off the top N values off of the stack, consing them up into a
     list, then pushes that list on the stack.  What was the topmost
     value will be the last element in the list.  N is a two-byte value,
     most significant byte first.

 -- Instruction: vector n
     Create and fill a vector with the top N values from the stack,
     popping off those values and pushing on the resulting vector.  N is
     a two-byte value, like in ‘vector’.

 -- Instruction: make-struct n
     Make a new struct from the top N values on the stack.  The values
     are popped, and the new struct is pushed.

     The deepest value is used as the vtable for the struct, and the
     rest are used in order as the field initializers.  Tail arrays are
     not supported by this instruction.

 -- Instruction: make-array n
     Pop an array shape from the stack, then pop the remaining N values,
     pushing a new array.  N is encoded over three bytes.

     The array shape should be appropriate to store N values.  *Note
     Array Procedures::, for more information on array shapes.

   Many of these data structures are constant, never changing over the
course of the different invocations of the procedure.  In that case it
is often advantageous to make them once when the procedure is created,
and just reference them from the object table thereafter.  *Note
Variables and the VM::, for more information on the object table.

 -- Instruction: object-ref n
 -- Instruction: long-object-ref n
     Push Nth value from the current program’s object vector.  The
     “long” variant has a 16-bit index instead of an 8-bit index.

9.3.6.8 Loading Instructions
............................

In addition to VM instructions, an instruction stream may contain
variable-length data embedded within it.  This data is always preceded
by special loading instructions, which interpret the data and advance
the instruction pointer to the next VM instruction.

   All of these loading instructions have a ‘length’ parameter,
indicating the size of the embedded data, in bytes.  The length itself
is encoded in 3 bytes.

 -- Instruction: load-number length
     Load an arbitrary number from the instruction stream.  The number
     is embedded in the stream as a string.
 -- Instruction: load-string length
     Load a string from the instruction stream.  The string is assumed
     to be encoded in the “latin1” locale.
 -- Instruction: load-wide-string length
     Load a UTF-32 string from the instruction stream.  LENGTH is the
     length in bytes, not in codepoints.
 -- Instruction: load-symbol length
     Load a symbol from the instruction stream.  The symbol is assumed
     to be encoded in the “latin1” locale.  Symbols backed by wide
     strings may be loaded via ‘load-wide-string’ then ‘make-symbol’.
 -- Instruction: load-array length
     Load a uniform array from the instruction stream.  The shape and
     type of the array are popped off the stack, in that order.

 -- Instruction: load-program
     Load bytecode from the instruction stream, and push a compiled
     procedure.

     This instruction pops one value from the stack: the program’s
     object table, as a vector, or ‘#f’ in the case that the program has
     no object table.  A program that does not reference toplevel
     bindings and does not use ‘object-ref’ does not need an object
     table.

     This instruction is unlike the rest of the loading instructions,
     because instead of parsing its data, it directly maps the
     instruction stream onto a C structure, ‘struct scm_objcode’.  *Note
     Bytecode and Objcode::, for more information.

     The resulting compiled procedure will not have any free variables
     captured, so it may be loaded only once but used many times to
     create closures.

9.3.6.9 Dynamic Environment Instructions
........................................

Guile’s virtual machine has low-level support for ‘dynamic-wind’,
dynamic binding, and composable prompts and aborts.

 -- Instruction: wind
     Pop an unwind thunk and a wind thunk from the stack, in that order,
     and push them onto the “dynamic stack”.  The unwind thunk will be
     called on nonlocal exits, and the wind thunk on reentries.  Used to
     implement ‘dynamic-wind’.

     Note that neither thunk is actually called; the compiler should
     emit calls to wind and unwind for the normal dynamic-wind control
     flow.  *Note Dynamic Wind::.

 -- Instruction: unwind
     Pop off the top entry from the “dynamic stack”, for example, a
     wind/unwind thunk pair.  ‘unwind’ instructions should be properly
     paired with their winding instructions, like ‘wind’.

 -- Instruction: wind-fluids n
     Pop off N values and N fluids from the stack, in that order.  Set
     the fluids to the values by creating a with-fluids object and
     pushing that object on the dynamic stack.  *Note Fluids and Dynamic
     States::.

 -- Instruction: unwind-fluids
     Pop a with-fluids object from the dynamic stack, and swap the
     current values of its fluids with the saved values of its fluids.
     In this way, the dynamic environment is left as it was before the
     corresponding ‘wind-fluids’ instruction was processed.

 -- Instruction: fluid-ref
     Pop a fluid from the stack, and push its current value.

 -- Instruction: fluid-set
     Pop a value and a fluid from the stack, in that order, and set the
     fluid to the value.

 -- Instruction: prompt escape-only? offset
     Establish a dynamic prompt.  *Note Prompts::, for more information
     on prompts.

     The prompt will be pushed on the dynamic stack.  The normal control
     flow should ensure that the prompt is popped off at the end, via
     ‘unwind’.

     If an abort is made to this prompt, control will jump to OFFSET, a
     three-byte relative address.  The continuation and all arguments to
     the abort will be pushed on the stack, along with the total number
     of arguments (including the continuation.  If control returns to
     the handler, the prompt is already popped off by the abort
     mechanism.  (Guile’s ‘prompt’ implements Felleisen’s "–F–"
     operator.)

     If ESCAPE-ONLY? is nonzero, the prompt will be marked as
     escape-only, which allows an abort to this prompt to avoid reifying
     the continuation.

 -- Instruction: abort n
     Abort to a dynamic prompt.

     This instruction pops one tail argument list, N arguments, and a
     prompt tag from the stack.  The dynamic environment is then
     searched for a prompt having the given tag.  If none is found, an
     error is signalled.  Otherwise all arguments are passed to the
     prompt’s handler, along with the captured continuation, if
     necessary.

     If the prompt’s handler can be proven to not reference the captured
     continuation, no continuation is allocated.  This decision happens
     dynamically, at run-time; the general case is that the continuation
     may be captured, and thus resumed.  A reinstated continuation will
     have its arguments pushed on the stack, along with the number of
     arguments, as in the multiple-value return convention.  Therefore
     an ‘abort’ instruction should be followed by code ready to handle
     the equivalent of a multiply-valued return.

9.3.6.10 Miscellaneous Instructions
...................................

 -- Instruction: nop
     Does nothing!  Used for padding other instructions to certain
     alignments.

 -- Instruction: halt
     Exits the VM, returning a SCM value.  Normally, this instruction is
     only part of the “bootstrap program”, a program run when a virtual
     machine is first entered; compiled Scheme procedures will not
     contain this instruction.

     If multiple values have been returned, the SCM value will be a
     multiple-values object (*note Multiple Values::).

 -- Instruction: break
     Does nothing, but invokes the break hook.

 -- Instruction: drop
     Pops off the top value from the stack, throwing it away.

 -- Instruction: dup
     Re-pushes the top value onto the stack.

 -- Instruction: void
     Pushes “the unspecified value” onto the stack.

9.3.6.11 Inlined Scheme Instructions
....................................

The Scheme compiler can recognize the application of standard Scheme
procedures.  It tries to inline these small operations to avoid the
overhead of creating new stack frames.

   Since most of these operations are historically implemented as C
primitives, not inlining them would entail constantly calling out from
the VM to the interpreter, which has some costs—registers must be saved,
the interpreter has to dispatch, called procedures have to do much type
checking, etc.  It’s much more efficient to inline these operations in
the virtual machine itself.

   All of these instructions pop their arguments from the stack and push
their results, and take no parameters from the instruction stream.
Thus, unlike in the previous sections, these instruction definitions
show stack parameters instead of parameters from the instruction stream.

 -- Instruction: not x
 -- Instruction: not-not x
 -- Instruction: eq? x y
 -- Instruction: not-eq? x y
 -- Instruction: null?
 -- Instruction: not-null?
 -- Instruction: eqv? x y
 -- Instruction: equal? x y
 -- Instruction: pair? x y
 -- Instruction: list? x
 -- Instruction: set-car! pair x
 -- Instruction: set-cdr! pair x
 -- Instruction: cons x y
 -- Instruction: car x
 -- Instruction: cdr x
 -- Instruction: vector-ref x y
 -- Instruction: vector-set x n y
 -- Instruction: struct? x
 -- Instruction: struct-ref x n
 -- Instruction: struct-set x n v
 -- Instruction: struct-vtable x
 -- Instruction: class-of x
 -- Instruction: slot-ref struct n
 -- Instruction: slot-set struct n x
     Inlined implementations of their Scheme equivalents.

   Note that ‘caddr’ and friends compile to a series of ‘car’ and ‘cdr’
instructions.

9.3.6.12 Inlined Mathematical Instructions
..........................................

Inlining mathematical operations has the obvious advantage of handling
fixnums without function calls or allocations.  The trick, of course, is
knowing when the result of an operation will be a fixnum, and there
might be a couple bugs here.

   More instructions could be added here over time.

   As in the previous section, the definitions below show stack
parameters instead of instruction stream parameters.

 -- Instruction: add x y
 -- Instruction: add1 x
 -- Instruction: sub x y
 -- Instruction: sub1 x
 -- Instruction: mul x y
 -- Instruction: div x y
 -- Instruction: quo x y
 -- Instruction: rem x y
 -- Instruction: mod x y
 -- Instruction: ee? x y
 -- Instruction: lt? x y
 -- Instruction: gt? x y
 -- Instruction: le? x y
 -- Instruction: ge? x y
 -- Instruction: ash x n
 -- Instruction: logand x y
 -- Instruction: logior x y
 -- Instruction: logxor x y
     Inlined implementations of the corresponding mathematical
     operations.

9.3.6.13 Inlined Bytevector Instructions
........................................

Bytevector operations correspond closely to what the current hardware
can do, so it makes sense to inline them to VM instructions, providing a
clear path for eventual native compilation.  Without this, Scheme
programs would need other primitives for accessing raw bytes – but these
primitives are as good as any.

   As in the previous section, the definitions below show stack
parameters instead of instruction stream parameters.

   The multibyte formats (‘u16’, ‘f64’, etc) take an extra endianness
argument.  Only aligned native accesses are currently fast-pathed in
Guile’s VM.

 -- Instruction: bv-u8-ref bv n
 -- Instruction: bv-s8-ref bv n
 -- Instruction: bv-u16-native-ref bv n
 -- Instruction: bv-s16-native-ref bv n
 -- Instruction: bv-u32-native-ref bv n
 -- Instruction: bv-s32-native-ref bv n
 -- Instruction: bv-u64-native-ref bv n
 -- Instruction: bv-s64-native-ref bv n
 -- Instruction: bv-f32-native-ref bv n
 -- Instruction: bv-f64-native-ref bv n
 -- Instruction: bv-u16-ref bv n endianness
 -- Instruction: bv-s16-ref bv n endianness
 -- Instruction: bv-u32-ref bv n endianness
 -- Instruction: bv-s32-ref bv n endianness
 -- Instruction: bv-u64-ref bv n endianness
 -- Instruction: bv-s64-ref bv n endianness
 -- Instruction: bv-f32-ref bv n endianness
 -- Instruction: bv-f64-ref bv n endianness
 -- Instruction: bv-u8-set bv n val
 -- Instruction: bv-s8-set bv n val
 -- Instruction: bv-u16-native-set bv n val
 -- Instruction: bv-s16-native-set bv n val
 -- Instruction: bv-u32-native-set bv n val
 -- Instruction: bv-s32-native-set bv n val
 -- Instruction: bv-u64-native-set bv n val
 -- Instruction: bv-s64-native-set bv n val
 -- Instruction: bv-f32-native-set bv n val
 -- Instruction: bv-f64-native-set bv n val
 -- Instruction: bv-u16-set bv n val endianness
 -- Instruction: bv-s16-set bv n val endianness
 -- Instruction: bv-u32-set bv n val endianness
 -- Instruction: bv-s32-set bv n val endianness
 -- Instruction: bv-u64-set bv n val endianness
 -- Instruction: bv-s64-set bv n val endianness
 -- Instruction: bv-f32-set bv n val endianness
 -- Instruction: bv-f64-set bv n val endianness
     Inlined implementations of the corresponding bytevector operations.

9.4 Compiling to the Virtual Machine
====================================

Compilers have a mystique about them that is attractive and off-putting
at the same time.  They are attractive because they are magical – they
transform inert text into live results, like throwing the switch on
Frankenstein’s monster.  However, this magic is perceived by many to be
impenetrable.

   This section aims to pay attention to the small man behind the
curtain.

   *Note Read/Load/Eval/Compile::, if you’re lost and you just wanted to
know how to compile your ‘.scm’ file.

9.4.1 Compiler Tower
--------------------

Guile’s compiler is quite simple, actually – its _compilers_, to put it
more accurately.  Guile defines a tower of languages, starting at Scheme
and progressively simplifying down to languages that resemble the VM
instruction set (*note Instruction Set::).

   Each language knows how to compile to the next, so each step is
simple and understandable.  Furthermore, this set of languages is not
hardcoded into Guile, so it is possible for the user to add new
high-level languages, new passes, or even different compilation targets.

   Languages are registered in the module, ‘(system base language)’:

     (use-modules (system base language))

   They are registered with the ‘define-language’ form.

 -- Scheme Syntax: define-language [#:name] [#:title] [#:reader]
          [#:printer] [#:parser=#f] [#:compilers='()]
          [#:decompilers='()] [#:evaluator=#f] [#:joiner=#f]
          [#:for-humans?=#t]
          [#:make-default-environment=make-fresh-user-module]
     Define a language.

     This syntax defines a ‘#<language>’ object, bound to NAME in the
     current environment.  In addition, the language will be added to
     the global language set.  For example, this is the language
     definition for Scheme:

          (define-language scheme
            #:title	"Scheme"
            #:reader      (lambda (port env) ...)
            #:compilers   `((tree-il . ,compile-tree-il))
            #:decompilers `((tree-il . ,decompile-tree-il))
            #:evaluator	(lambda (x module) (primitive-eval x))
            #:printer	write
            #:make-default-environment (lambda () ...))

   The interesting thing about having languages defined this way is that
they present a uniform interface to the read-eval-print loop.  This
allows the user to change the current language of the REPL:

     scheme@(guile-user)> ,language tree-il
     Happy hacking with Tree Intermediate Language!  To switch back, type `,L scheme'.
     tree-il@(guile-user)> ,L scheme
     Happy hacking with Scheme!  To switch back, type `,L tree-il'.
     scheme@(guile-user)>

   Languages can be looked up by name, as they were above.

 -- Scheme Procedure: lookup-language name
     Looks up a language named NAME, autoloading it if necessary.

     Languages are autoloaded by looking for a variable named NAME in a
     module named ‘(language NAME spec)’.

     The language object will be returned, or ‘#f’ if there does not
     exist a language with that name.

   Defining languages this way allows us to programmatically determine
the necessary steps for compiling code from one language to another.

 -- Scheme Procedure: lookup-compilation-order from to
     Recursively traverses the set of languages to which FROM can
     compile, depth-first, and return the first path that can transform
     FROM to TO.  Returns ‘#f’ if no path is found.

     This function memoizes its results in a cache that is invalidated
     by subsequent calls to ‘define-language’, so it should be quite
     fast.

   There is a notion of a “current language”, which is maintained in the
‘current-language’ parameter, defined in the core ‘(guile)’ module.
This language is normally Scheme, and may be rebound by the user.  The
run-time compilation interfaces (*note Read/Load/Eval/Compile::) also
allow you to choose other source and target languages.

   The normal tower of languages when compiling Scheme goes like this:

   • Scheme
   • Tree Intermediate Language (Tree-IL)
   • Guile Lowlevel Intermediate Language (GLIL)
   • Assembly
   • Bytecode
   • Objcode

   Object code may be serialized to disk directly, though it has a
cookie and version prepended to the front.  But when compiling Scheme at
run time, you want a Scheme value: for example, a compiled procedure.
For this reason, so as not to break the abstraction, Guile defines a
fake language at the bottom of the tower:

   • Value

   Compiling to ‘value’ loads the object code into a procedure, and
wakes the sleeping giant.

   Perhaps this strangeness can be explained by example: ‘compile-file’
defaults to compiling to object code, because it produces object code
that has to live in the barren world outside the Guile runtime; but
‘compile’ defaults to compiling to ‘value’, as its product re-enters the
Guile world.

   Indeed, the process of compilation can circulate through these
different worlds indefinitely, as shown by the following quine:

     ((lambda (x) ((compile x) x)) '(lambda (x) ((compile x) x)))

9.4.2 The Scheme Compiler
-------------------------

The job of the Scheme compiler is to expand all macros and all of Scheme
to its most primitive expressions.  The definition of “primitive” is
given by the inventory of constructs provided by Tree-IL, the target
language of the Scheme compiler: procedure applications, conditionals,
lexical references, etc.  This is described more fully in the next
section.

   The tricky and amusing thing about the Scheme-to-Tree-IL compiler is
that it is completely implemented by the macro expander.  Since the
macro expander has to run over all of the source code already in order
to expand macros, it might as well do the analysis at the same time,
producing Tree-IL expressions directly.

   Because this compiler is actually the macro expander, it is
extensible.  Any macro which the user writes becomes part of the
compiler.

   The Scheme-to-Tree-IL expander may be invoked using the generic
‘compile’ procedure:

     (compile '(+ 1 2) #:from 'scheme #:to 'tree-il)
     ⇒
      #<<application> src: #f
                      proc: #<<toplevel-ref> src: #f name: +>
                      args: (#<<const> src: #f exp: 1>
                             #<<const> src: #f exp: 2>)>

   Or, since Tree-IL is so close to Scheme, it is often useful to expand
Scheme to Tree-IL, then translate back to Scheme.  For that reason the
expander provides two interfaces.  The former is equivalent to calling
‘(macroexpand '(+ 1 2) 'c)’, where the ‘'c’ is for “compile”.  With ‘'e’
(the default), the result is translated back to Scheme:

     (macroexpand '(+ 1 2))
     ⇒ (+ 1 2)
     (macroexpand '(let ((x 10)) (* x x)))
     ⇒ (let ((x84 10)) (* x84 x84))

   The second example shows that as part of its job, the macro expander
renames lexically-bound variables.  The original names are preserved
when compiling to Tree-IL, but can’t be represented in Scheme: a lexical
binding only has one name.  It is for this reason that the _native_
output of the expander is _not_ Scheme.  There’s too much information we
would lose if we translated to Scheme directly: lexical variable names,
source locations, and module hygiene.

   Note however that ‘macroexpand’ does not have the same signature as
‘compile-tree-il’.  ‘compile-tree-il’ is a small wrapper around
‘macroexpand’, to make it conform to the general form of compiler
procedures in Guile’s language tower.

   Compiler procedures take three arguments: an expression, an
environment, and a keyword list of options.  They return three values:
the compiled expression, the corresponding environment for the target
language, and a “continuation environment”.  The compiled expression and
environment will serve as input to the next language’s compiler.  The
“continuation environment” can be used to compile another expression
from the same source language within the same module.

   For example, you might compile the expression, ‘(define-module
(foo))’.  This will result in a Tree-IL expression and environment.  But
if you compiled a second expression, you would want to take into account
the compile-time effect of compiling the previous expression, which puts
the user in the ‘(foo)’ module.  That is purpose of the “continuation
environment”; you would pass it as the environment when compiling the
subsequent expression.

   For Scheme, an environment is a module.  By default, the ‘compile’
and ‘compile-file’ procedures compile in a fresh module, such that
bindings and macros introduced by the expression being compiled are
isolated:

     (eq? (current-module) (compile '(current-module)))
     ⇒ #f

     (compile '(define hello 'world))
     (defined? 'hello)
     ⇒ #f

     (define / *)
     (eq? (compile '/) /)
     ⇒ #f

   Similarly, changes to the ‘current-reader’ fluid (*note
‘current-reader’: Loading.) are isolated:

     (compile '(fluid-set! current-reader (lambda args 'fail)))
     (fluid-ref current-reader)
     ⇒ #f

   Nevertheless, having the compiler and "compilee" share the same name
space can be achieved by explicitly passing ‘(current-module)’ as the
compilation environment:

     (define hello 'world)
     (compile 'hello #:env (current-module))
     ⇒ world

9.4.3 Tree-IL
-------------

Tree Intermediate Language (Tree-IL) is a structured intermediate
language that is close in expressive power to Scheme.  It is an
expanded, pre-analyzed Scheme.

   Tree-IL is “structured” in the sense that its representation is based
on records, not S-expressions.  This gives a rigidity to the language
that ensures that compiling to a lower-level language only requires a
limited set of transformations.  For example, the Tree-IL type ‘<const>’
is a record type with two fields, ‘src’ and ‘exp’.  Instances of this
type are created via ‘make-const’.  Fields of this type are accessed via
the ‘const-src’ and ‘const-exp’ procedures.  There is also a predicate,
‘const?’.  *Note Records::, for more information on records.

   All Tree-IL types have a ‘src’ slot, which holds source location
information for the expression.  This information, if present, will be
residualized into the compiled object code, allowing backtraces to show
source information.  The format of ‘src’ is the same as that returned by
Guile’s ‘source-properties’ function.  *Note Source Properties::, for
more information.

   Although Tree-IL objects are represented internally using records,
there is also an equivalent S-expression external representation for
each kind of Tree-IL. For example, the S-expression representation of
‘#<const src: #f exp: 3>’ expression would be:

     (const 3)

   Users may program with this format directly at the REPL:

     scheme@(guile-user)> ,language tree-il
     Happy hacking with Tree Intermediate Language!  To switch back, type `,L scheme'.
     tree-il@(guile-user)> (apply (primitive +) (const 32) (const 10))
     ⇒ 42

   The ‘src’ fields are left out of the external representation.

   One may create Tree-IL objects from their external representations
via calling ‘parse-tree-il’, the reader for Tree-IL. If any source
information is attached to the input S-expression, it will be propagated
to the resulting Tree-IL expressions.  This is probably the easiest way
to compile to Tree-IL: just make the appropriate external
representations in S-expression format, and let ‘parse-tree-il’ take
care of the rest.

 -- Scheme Variable: <void> src
 -- External Representation: (void)
     An empty expression.  In practice, equivalent to Scheme’s ‘(if #f
     #f)’.
 -- Scheme Variable: <const> src exp
 -- External Representation: (const EXP)
     A constant.
 -- Scheme Variable: <primitive-ref> src name
 -- External Representation: (primitive NAME)
     A reference to a “primitive”.  A primitive is a procedure that,
     when compiled, may be open-coded.  For example, ‘cons’ is usually
     recognized as a primitive, so that it compiles down to a single
     instruction.

     Compilation of Tree-IL usually begins with a pass that resolves
     some ‘<module-ref>’ and ‘<toplevel-ref>’ expressions to
     ‘<primitive-ref>’ expressions.  The actual compilation pass has
     special cases for applications of certain primitives, like ‘apply’
     or ‘cons’.
 -- Scheme Variable: <lexical-ref> src name gensym
 -- External Representation: (lexical NAME GENSYM)
     A reference to a lexically-bound variable.  The NAME is the
     original name of the variable in the source program.  GENSYM is a
     unique identifier for this variable.
 -- Scheme Variable: <lexical-set> src name gensym exp
 -- External Representation: (set! (lexical NAME GENSYM) EXP)
     Sets a lexically-bound variable.
 -- Scheme Variable: <module-ref> src mod name public?
 -- External Representation: ( @ MOD NAME)
 -- External Representation: ( @@ MOD NAME)
     A reference to a variable in a specific module.  MOD should be the
     name of the module, e.g. ‘(guile-user)’.

     If PUBLIC? is true, the variable named NAME will be looked up in
     MOD’s public interface, and serialized with ‘@’; otherwise it will
     be looked up among the module’s private bindings, and is serialized
     with ‘@@’.
 -- Scheme Variable: <module-set> src mod name public? exp
 -- External Representation: (set! (@ MOD NAME) EXP)
 -- External Representation: (set! (@@ MOD NAME) EXP)
     Sets a variable in a specific module.
 -- Scheme Variable: <toplevel-ref> src name
 -- External Representation: (toplevel NAME)
     References a variable from the current procedure’s module.
 -- Scheme Variable: <toplevel-set> src name exp
 -- External Representation: (set! (toplevel NAME) EXP)
     Sets a variable in the current procedure’s module.
 -- Scheme Variable: <toplevel-define> src name exp
 -- External Representation: (define (toplevel NAME) EXP)
     Defines a new top-level variable in the current procedure’s module.
 -- Scheme Variable: <conditional> src test then else
 -- External Representation: (if TEST THEN ELSE)
     A conditional.  Note that ELSE is not optional.
 -- Scheme Variable: <application> src proc args
 -- External Representation: (apply PROC . ARGS)
     A procedure call.
 -- Scheme Variable: <sequence> src exps
 -- External Representation: (begin . EXPS)
     Like Scheme’s ‘begin’.
 -- Scheme Variable: <lambda> src meta body
 -- External Representation: (lambda META BODY)
     A closure.  META is an association list of properties for the
     procedure.  BODY is a single Tree-IL expression of type
     ‘<lambda-case>’.  As the ‘<lambda-case>’ clause can chain to an
     alternate clause, this makes Tree-IL’s ‘<lambda>’ have the
     expressiveness of Scheme’s ‘case-lambda’.
 -- Scheme Variable: <lambda-case> req opt rest kw inits gensyms body
          alternate
 -- External Representation: (lambda-case ((REQ OPT REST KW INITS
          GENSYMS) BODY) [ALTERNATE])
     One clause of a ‘case-lambda’.  A ‘lambda’ expression in Scheme is
     treated as a ‘case-lambda’ with one clause.

     REQ is a list of the procedure’s required arguments, as symbols.
     OPT is a list of the optional arguments, or ‘#f’ if there are no
     optional arguments.  REST is the name of the rest argument, or
     ‘#f’.

     KW is a list of the form, ‘(ALLOW-OTHER-KEYS? (KEYWORD NAME VAR)
     ...)’, where KEYWORD is the keyword corresponding to the argument
     named NAME, and whose corresponding gensym is VAR.  INITS are
     tree-il expressions corresponding to all of the optional and
     keyword arguments, evaluated to bind variables whose value is not
     supplied by the procedure caller.  Each INIT expression is
     evaluated in the lexical context of previously bound variables,
     from left to right.

     GENSYMS is a list of gensyms corresponding to all arguments: first
     all of the required arguments, then the optional arguments if any,
     then the rest argument if any, then all of the keyword arguments.

     BODY is the body of the clause.  If the procedure is called with an
     appropriate number of arguments, BODY is evaluated in tail
     position.  Otherwise, if there is an ALTERNATE, it should be a
     ‘<lambda-case>’ expression, representing the next clause to try.
     If there is no ALTERNATE, a wrong-number-of-arguments error is
     signaled.
 -- Scheme Variable: <let> src names gensyms vals exp
 -- External Representation: (let NAMES GENSYMS VALS EXP)
     Lexical binding, like Scheme’s ‘let’.  NAMES are the original
     binding names, GENSYMS are gensyms corresponding to the NAMES, and
     VALS are Tree-IL expressions for the values.  EXP is a single
     Tree-IL expression.
 -- Scheme Variable: <letrec> in-order? src names gensyms vals exp
 -- External Representation: (letrec NAMES GENSYMS VALS EXP)
 -- External Representation: (letrec* NAMES GENSYMS VALS EXP)
     A version of ‘<let>’ that creates recursive bindings, like Scheme’s
     ‘letrec’, or ‘letrec*’ if IN-ORDER? is true.
 -- Scheme Variable: <dynlet> fluids vals body
 -- External Representation: (dynlet FLUIDS VALS BODY)
     Dynamic binding; the equivalent of Scheme’s ‘with-fluids’.  FLUIDS
     should be a list of Tree-IL expressions that will evaluate to
     fluids, and VALS a corresponding list of expressions to bind to the
     fluids during the dynamic extent of the evaluation of BODY.
 -- Scheme Variable: <dynref> fluid
 -- External Representation: (dynref FLUID)
     A dynamic variable reference.  FLUID should be a Tree-IL expression
     evaluating to a fluid.
 -- Scheme Variable: <dynset> fluid exp
 -- External Representation: (dynset FLUID EXP)
     A dynamic variable set.  FLUID, a Tree-IL expression evaluating to
     a fluid, will be set to the result of evaluating EXP.
 -- Scheme Variable: <dynwind> winder body unwinder
 -- External Representation: (dynwind WINDER BODY UNWINDER)
     A ‘dynamic-wind’.  WINDER and UNWINDER should both evaluate to
     thunks.  Ensure that the winder and the unwinder are called before
     entering and after leaving BODY.  Note that BODY is an expression,
     without a thunk wrapper.
 -- Scheme Variable: <prompt> tag body handler
 -- External Representation: (prompt TAG BODY HANDLER)
     A dynamic prompt.  Instates a prompt named TAG, an expression,
     during the dynamic extent of the execution of BODY, also an
     expression.  If an abort occurs to this prompt, control will be
     passed to HANDLER, a ‘<lambda-case>’ expression with no optional or
     keyword arguments, and no alternate.  The first argument to the
     ‘<lambda-case>’ will be the captured continuation, and then all of
     the values passed to the abort.  *Note Prompts::, for more
     information.
 -- Scheme Variable: <abort> tag args tail
 -- External Representation: (abort TAG ARGS TAIL)
     An abort to the nearest prompt with the name TAG, an expression.
     ARGS should be a list of expressions to pass to the prompt’s
     handler, and TAIL should be an expression that will evaluate to a
     list of additional arguments.  An abort will save the partial
     continuation, which may later be reinstated, resulting in the
     ‘<abort>’ expression evaluating to some number of values.

   There are two Tree-IL constructs that are not normally produced by
higher-level compilers, but instead are generated during the
source-to-source optimization and analysis passes that the Tree-IL
compiler does.  Users should not generate these expressions directly,
unless they feel very clever, as the default analysis pass will generate
them as necessary.

 -- Scheme Variable: <let-values> src names gensyms exp body
 -- External Representation: (let-values NAMES GENSYMS EXP BODY)
     Like Scheme’s ‘receive’ – binds the values returned by evaluating
     ‘exp’ to the ‘lambda’-like bindings described by GENSYMS.  That is
     to say, GENSYMS may be an improper list.

     ‘<let-values>’ is an optimization of ‘<application>’ of the
     primitive, ‘call-with-values’.
 -- Scheme Variable: <fix> src names gensyms vals body
 -- External Representation: (fix NAMES GENSYMS VALS BODY)
     Like ‘<letrec>’, but only for VALS that are unset ‘lambda’
     expressions.

     ‘fix’ is an optimization of ‘letrec’ (and ‘let’).

   Tree-IL implements a compiler to GLIL that recursively traverses
Tree-IL expressions, writing out GLIL expressions into a linear list.
The compiler also keeps some state as to whether the current expression
is in tail context, and whether its value will be used in future
computations.  This state allows the compiler not to emit code for
constant expressions that will not be used (e.g. docstrings), and to
perform tail calls when in tail position.

   Most optimization, such as it currently is, is performed on Tree-IL
expressions as source-to-source transformations.  There will be more
optimizations added in the future.

   Interested readers are encouraged to read the implementation in
‘(language tree-il compile-glil)’ for more details.

9.4.4 GLIL
----------

Guile Lowlevel Intermediate Language (GLIL) is a structured intermediate
language whose expressions more closely approximate Guile’s VM
instruction set.  Its expression types are defined in ‘(language glil)’.

 -- Scheme Variable: <glil-program> meta . body
     A unit of code that at run-time will correspond to a compiled
     procedure.  META should be an alist of properties, as in Tree-IL’s
     ‘<lambda>’.  BODY is an ordered list of GLIL expressions.
 -- Scheme Variable: <glil-std-prelude> nreq nlocs else-label
     A prologue for a function with no optional, keyword, or rest
     arguments.  NREQ is the number of required arguments.  NLOCS the
     total number of local variables, including the arguments.  If the
     procedure was not given exactly NREQ arguments, control will jump
     to ELSE-LABEL, if given, or otherwise signal an error.
 -- Scheme Variable: <glil-opt-prelude> nreq nopt rest nlocs else-label
     A prologue for a function with optional or rest arguments.  Like
     ‘<glil-std-prelude>’, with the addition that NOPT is the number of
     optional arguments (possibly zero) and REST is an index of a local
     variable at which to bind a rest argument, or ‘#f’ if there is no
     rest argument.
 -- Scheme Variable: <glil-kw-prelude> nreq nopt rest kw
          allow-other-keys? nlocs else-label
     A prologue for a function with keyword arguments.  Like
     ‘<glil-opt-prelude>’, with the addition that KW is a list of
     keyword arguments, and ALLOW-OTHER-KEYS? is a flag indicating
     whether to allow unknown keys.  *Note ‘bind-kwargs’: Function
     Prologue Instructions, for details on the format of KW.
 -- Scheme Variable: <glil-bind> . vars
     An advisory expression that notes a liveness extent for a set of
     variables.  VARS is a list of ‘(NAME TYPE INDEX)’, where TYPE
     should be either ‘argument’, ‘local’, or ‘external’.

     ‘<glil-bind>’ expressions end up being serialized as part of a
     program’s metadata and do not form part of a program’s code path.
 -- Scheme Variable: <glil-mv-bind> vars rest
     A multiple-value binding of the values on the stack to VARS.  If
     REST is true, the last element of VARS will be treated as a rest
     argument.

     In addition to pushing a binding annotation on the stack, like
     ‘<glil-bind>’, an expression is emitted at compilation time to make
     sure that there are enough values available to bind.  See the notes
     on ‘truncate-values’ in *note Procedure Call and Return
     Instructions::, for more information.
 -- Scheme Variable: <glil-unbind>
     Closes the liveness extent of the most recently encountered
     ‘<glil-bind>’ or ‘<glil-mv-bind>’ expression.  As GLIL expressions
     are compiled, a parallel stack of live bindings is maintained; this
     expression pops off the top element from that stack.

     Bindings are written into the program’s metadata so that debuggers
     and other tools can determine the set of live local variables at a
     given offset within a VM program.
 -- Scheme Variable: <glil-source> loc
     Records source information for the preceding expression.  LOC
     should be an association list of containing ‘line’ ‘column’, and
     ‘filename’ keys, e.g. as returned by ‘source-properties’.
 -- Scheme Variable: <glil-void>
     Pushes “the unspecified value” on the stack.
 -- Scheme Variable: <glil-const> obj
     Pushes a constant value onto the stack.  OBJ must be a number,
     string, symbol, keyword, boolean, character, uniform array, the
     empty list, or a pair or vector of constants.
 -- Scheme Variable: <glil-lexical> local? boxed? op index
     Accesses a lexically bound variable.  If the variable is not LOCAL?
     it is free.  All variables may have ‘ref’, ‘set’, and ‘bound?’ as
     their OP.  Boxed variables may also have the OPs ‘box’,
     ‘empty-box’, and ‘fix’, which correspond in semantics to the VM
     instructions ‘box’, ‘empty-box’, and ‘fix-closure’.  *Note Stack
     Layout::, for more information.
 -- Scheme Variable: <glil-toplevel> op name
     Accesses a toplevel variable.  OP may be ‘ref’, ‘set’, or ‘define’.
 -- Scheme Variable: <glil-module> op mod name public?
     Accesses a variable within a specific module.  See Tree-IL’s
     ‘<module-ref>’, for more information.
 -- Scheme Variable: <glil-label> label
     Creates a new label.  LABEL can be any Scheme value, and should be
     unique.
 -- Scheme Variable: <glil-branch> inst label
     Branch to a label.  LABEL should be a ‘<ghil-label>’.  ‘inst’ is a
     branching instruction: ‘br-if’, ‘br’, etc.
 -- Scheme Variable: <glil-call> inst nargs
     This expression is probably misnamed, as it does not correspond to
     function calls.  ‘<glil-call>’ invokes the VM instruction named
     INST, noting that it is called with NARGS stack arguments.  The
     arguments should be pushed on the stack already.  What happens to
     the stack afterwards depends on the instruction.
 -- Scheme Variable: <glil-mv-call> nargs ra
     Performs a multiple-value call.  RA is a ‘<glil-label>’
     corresponding to the multiple-value return address for the call.
     See the notes on ‘mv-call’ in *note Procedure Call and Return
     Instructions::, for more information.
 -- Scheme Variable: <glil-prompt> label escape-only?
     Push a dynamic prompt into the stack, with a handler at LABEL.
     ESCAPE-ONLY? is a flag that is propagated to the prompt, allowing
     an abort to avoid capturing a continuation in some cases.  *Note
     Prompts::, for more information.

   Users may enter in GLIL at the REPL as well, though there is a bit
more bookkeeping to do:

     scheme@(guile-user)> ,language glil
     Happy hacking with Guile Lowlevel Intermediate Language (GLIL)!
     To switch back, type `,L scheme'.
     glil@(guile-user)> (program () (std-prelude 0 0 #f)
                            (const 3) (call return 1))
     ⇒ 3

   Just as in all of Guile’s compilers, an environment is passed to the
GLIL-to-object code compiler, and one is returned as well, along with
the object code.

9.4.5 Assembly
--------------

Assembly is an S-expression-based, human-readable representation of the
actual bytecodes that will be emitted for the VM. As such, it is a
useful intermediate language both for compilation and for decompilation.

   Besides the fact that it is not a record-based language, assembly
differs from GLIL in four main ways:

   • Labels have been resolved to byte offsets in the program.
   • Constants inside procedures have either been expressed as inline
     instructions or cached in object arrays.
   • Procedures with metadata (source location information, liveness
     extents, procedure names, generic properties, etc) have had their
     metadata serialized out to thunks.
   • All expressions correspond directly to VM instructions – i.e.,
     there is no ‘<glil-lexical>’ which can be a ref or a set.

   Assembly is isomorphic to the bytecode that it compiles to.  You can
compile to bytecode, then decompile back to assembly, and you have the
same assembly code.

   The general form of assembly instructions is the following:

     (INST ARG ...)

   The INST names a VM instruction, and its ARGs will be embedded in the
instruction stream.  The easiest way to see assembly is to play around
with it at the REPL, as can be seen in this annotated example:

     scheme@(guile-user)> ,pp (compile '(+ 32 10) #:to 'assembly)
     (load-program
       ((:LCASE16 . 2))  ; Labels, unused in this case.
       8                 ; Length of the thunk that was compiled.
       (load-program     ; Metadata thunk.
         ()
         17
         #f              ; No metadata thunk for the metadata thunk.
         (make-eol)
         (make-eol)
         (make-int8 2)   ; Liveness extents, source info, and arities,
         (make-int8 8)   ; in a format that Guile knows how to parse.
         (make-int8:0)
         (list 0 3)
         (list 0 1)
         (list 0 3)
         (return))
       (assert-nargs-ee/locals 0)  ; Prologue.
       (make-int8 32)    ; Actual code starts here.
       (make-int8 10)
       (add)
       (return))

   Of course you can switch the REPL to assembly and enter in assembly
S-expressions directly, like with other languages, though it is more
difficult, given that the length fields have to be correct.

9.4.6 Bytecode and Objcode
--------------------------

Finally, the raw bytes.  There are actually two different “languages”
here, corresponding to two different ways to represent the bytes.

   “Bytecode” represents code as uniform byte vectors, useful for
structuring and destructuring code on the Scheme level.  Bytecode is the
next step down from assembly:

     scheme@(guile-user)> (compile '(+ 32 10) #:to 'bytecode)
     ⇒ #vu8(8 0 0 0 25 0 0 0            ; Header.
            95 0                            ; Prologue.
            10 32 10 10 148 66 17           ; Actual code.
            0 0 0 0 0 0 0 9                 ; Metadata thunk.
            9 10 2 10 8 11 18 0 3 18 0 1 18 0 3 66)

   “Objcode” is bytecode, but mapped directly to a C structure, ‘struct
scm_objcode’:

     struct scm_objcode {
       scm_t_uint32 len;
       scm_t_uint32 metalen;
       scm_t_uint8 base[0];
     };

   As one might imagine, objcode imposes a minimum length on the
bytecode.  Also, the ‘len’ and ‘metalen’ fields are in native
endianness, which makes objcode (and bytecode) system-dependent.

   Objcode also has a couple of important efficiency hacks.  First,
objcode may be mapped directly from disk, allowing compiled code to be
loaded quickly, often from the system’s disk cache, and shared among
multiple processes.  Secondly, objcode may be embedded in other objcode,
allowing procedures to have the text of other procedures inlined into
their bodies, without the need for separate allocation of the code.  Of
course, the objcode object itself does need to be allocated.

   Procedures related to objcode are defined in the ‘(system vm
objcode)’ module.

 -- Scheme Procedure: objcode? obj
 -- C Function: scm_objcode_p (obj)
     Returns ‘#f’ if OBJ is object code, ‘#f’ otherwise.

 -- Scheme Procedure: bytecode->objcode bytecode
 -- C Function: scm_bytecode_to_objcode (bytecode)
     Makes a bytecode object from BYTECODE, which should be a
     bytevector.  *Note Bytevectors::.

 -- Scheme Variable: load-objcode file
 -- C Function: scm_load_objcode (file)
     Load object code from a file named FILE.  The file will be mapped
     into memory via ‘mmap’, so this is a very fast operation.

     On disk, object code has an sixteen-byte cookie prepended to it, to
     prevent accidental loading of arbitrary garbage.

 -- Scheme Variable: write-objcode objcode file
 -- C Function: scm_write_objcode (objcode)
     Write object code out to a file, prepending the sixteen-byte
     cookie.

 -- Scheme Variable: objcode->bytecode objcode
 -- C Function: scm_objcode_to_bytecode (objcode)
     Copy object code out to a bytevector for analysis by Scheme.

   The following procedure is actually in ‘(system vm program)’, but
we’ll mention it here:

 -- Scheme Variable: make-program objcode objtable [free-vars=#f]
 -- C Function: scm_make_program (objcode, objtable, free_vars)
     Load up object code into a Scheme program.  The resulting program
     will have OBJTABLE as its object table, which should be a vector or
     ‘#f’, and will capture the free variables from FREE-VARS.

   Object code from a file may be disassembled at the REPL via the
meta-command ‘,disassemble-file’, abbreviated as ‘,xx’.  Programs may be
disassembled via ‘,disassemble’, abbreviated as ‘,x’.

   Compiling object code to the fake language, ‘value’, is performed via
loading objcode into a program, then executing that thunk with respect
to the compilation environment.  Normally the environment propagates
through the compiler transparently, but users may specify the
compilation environment manually as well, as a module.

9.4.7 Writing New High-Level Languages
--------------------------------------

In order to integrate a new language LANG into Guile’s compiler system,
one has to create the module ‘(language LANG spec)’ containing the
language definition and referencing the parser, compiler and other
routines processing it.  The module hierarchy in ‘(language brainfuck)’
defines a very basic Brainfuck implementation meant to serve as
easy-to-understand example on how to do this.  See for instance
<http://en.wikipedia.org/wiki/Brainfuck> for more information about the
Brainfuck language itself.

9.4.8 Extending the Compiler
----------------------------

At this point we take a detour from the impersonal tone of the rest of
the manual.  Admit it: if you’ve read this far into the compiler
internals manual, you are a junkie.  Perhaps a course at your university
left you unsated, or perhaps you’ve always harbored a desire to hack the
holy of computer science holies: a compiler.  Well you’re in good
company, and in a good position.  Guile’s compiler needs your help.

   There are many possible avenues for improving Guile’s compiler.
Probably the most important improvement, speed-wise, will be some form
of native compilation, both just-in-time and ahead-of-time.  This could
be done in many ways.  Probably the easiest strategy would be to extend
the compiled procedure structure to include a pointer to a native code
vector, and compile from bytecode to native code at run-time after a
procedure is called a certain number of times.

   The name of the game is a profiling-based harvest of the low-hanging
fruit, running programs of interest under a system-level profiler and
determining which improvements would give the most bang for the buck.
It’s really getting to the point though that native compilation is the
next step.

   The compiler also needs help at the top end, enhancing the Scheme
that it knows to also understand R6RS, and adding new high-level
compilers.  We have JavaScript and Emacs Lisp mostly complete, but they
could use some love; Lua would be nice as well, but whatever language it
is that strikes your fancy would be welcome too.

   Compilers are for hacking, not for admiring or for complaining about.
Get to it!

