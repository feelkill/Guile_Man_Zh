7.14 Buffered Input
===================

The following functions are provided by

     (use-modules (ice-9 buffered-input))

   A buffered input port allows a reader function to return chunks of
characters which are to be handed out on reading the port.  A notion of
further input for an application level logical expression is maintained
too, and passed through to the reader.

 -- Scheme Procedure: make-buffered-input-port reader
     Create an input port which returns characters obtained from the
     given READER function.  READER is called (READER cont), and should
     return a string or an EOF object.

     The new port gives precisely the characters returned by READER,
     nothing is added, so if any newline characters or other separators
     are desired they must come from the reader function.

     The CONT parameter to READER is ‘#f’ for initial input, or ‘#t’
     when continuing an expression.  This is an application level
     notion, set with ‘set-buffered-input-continuation?!’ below.  If the
     user has entered a partial expression then it allows READER for
     instance to give a different prompt to show more is required.

 -- Scheme Procedure: make-line-buffered-input-port reader
     Create an input port which returns characters obtained from the
     specified READER function, similar to ‘make-buffered-input-port’
     above, but where READER is expected to be a line-oriented.

     READER is called (READER cont), and should return a string or an
     EOF object as above.  Each string is a line of input without a
     newline character, the port code inserts a newline after each
     string.

 -- Scheme Procedure: set-buffered-input-continuation?! port cont
     Set the input continuation flag for a given buffered input PORT.

     An application uses this by calling with a CONT flag of ‘#f’ when
     beginning to read a new logical expression.  For example with the
     Scheme ‘read’ function (*note Scheme Read::),

          (define my-port (make-buffered-input-port my-reader))

          (set-buffered-input-continuation?! my-port #f)
          (let ((obj (read my-port)))
            ...

