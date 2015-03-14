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

