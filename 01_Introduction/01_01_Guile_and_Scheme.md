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

