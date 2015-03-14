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

