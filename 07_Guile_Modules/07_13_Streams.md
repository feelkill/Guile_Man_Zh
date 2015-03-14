7.13 Streams
============

This section documents Guile’s legacy stream module.  For a more
complete and portable stream library, *note SRFI-41::.

   A stream represents a sequence of values, each of which is calculated
only when required.  This allows large or even infinite sequences to be
represented and manipulated with familiar operations like “car”, “cdr”,
“map” or “fold”.  In such manipulations only as much as needed is
actually held in memory at any one time.  The functions in this section
are available from

     (use-modules (ice-9 streams))

   Streams are implemented using promises (*note Delayed Evaluation::),
which is how the underlying calculation of values is made only when
needed, and the values then retained so the calculation is not repeated.

Here is a simple example producing a stream of all odd numbers,

     (define odds (make-stream (lambda (state)
                                 (cons state (+ state 2)))
                               1))
     (stream-car odds)              ⇒ 1
     (stream-car (stream-cdr odds)) ⇒ 3

‘stream-map’ could be used to derive a stream of odd squares,

     (define (square n) (* n n))
     (define oddsquares (stream-map square odds))

   These are infinite sequences, so it’s not possible to convert them to
a list, but they could be printed (infinitely) with for example

     (stream-for-each (lambda (n sq)
                        (format #t "~a squared is ~a\n" n sq))
                      odds oddsquares)
     ⊣
     1 squared is 1
     3 squared is 9
     5 squared is 25
     7 squared is 49
     …


 -- Scheme Procedure: make-stream proc initial-state
     Return a new stream, formed by calling PROC successively.

     Each call is ‘(PROC STATE)’, it should return a pair, the ‘car’
     being the value for the stream, and the ‘cdr’ being the new STATE
     for the next call.  For the first call STATE is the given
     INITIAL-STATE.  At the end of the stream, PROC should return some
     non-pair object.

 -- Scheme Procedure: stream-car stream
     Return the first element from STREAM.  STREAM must not be empty.

 -- Scheme Procedure: stream-cdr stream
     Return a stream which is the second and subsequent elements of
     STREAM.  STREAM must not be empty.

 -- Scheme Procedure: stream-null? stream
     Return true if STREAM is empty.

 -- Scheme Procedure: list->stream list
 -- Scheme Procedure: vector->stream vector
     Return a stream with the contents of LIST or VECTOR.

     LIST or VECTOR should not be modified subsequently, since it’s
     unspecified whether changes there will be reflected in the stream
     returned.

 -- Scheme Procedure: port->stream port readproc
     Return a stream which is the values obtained by reading from PORT
     using READPROC.  Each read call is ‘(READPROC PORT)’, and it should
     return an EOF object (*note Reading::) at the end of input.

     For example a stream of characters from a file,

          (port->stream (open-input-file "/foo/bar.txt") read-char)

 -- Scheme Procedure: stream->list stream
     Return a list which is the entire contents of STREAM.

 -- Scheme Procedure: stream->reversed-list stream
     Return a list which is the entire contents of STREAM, but in
     reverse order.

 -- Scheme Procedure: stream->list&length stream
     Return two values (*note Multiple Values::), being firstly a list
     which is the entire contents of STREAM, and secondly the number of
     elements in that list.

 -- Scheme Procedure: stream->reversed-list&length stream
     Return two values (*note Multiple Values::) being firstly a list
     which is the entire contents of STREAM, but in reverse order, and
     secondly the number of elements in that list.

 -- Scheme Procedure: stream->vector stream
     Return a vector which is the entire contents of STREAM.

 -- Function: stream-fold proc init stream1 stream2 …
     Apply PROC successively over the elements of the given streams,
     from first to last until the end of the shortest stream is reached.
     Return the result from the last PROC call.

     Each call is ‘(PROC elem1 elem2 … prev)’, where each ELEM is from
     the corresponding STREAM.  PREV is the return from the previous
     PROC call, or the given INIT for the first call.

 -- Function: stream-for-each proc stream1 stream2 …
     Call PROC on the elements from the given STREAMs.  The return value
     is unspecified.

     Each call is ‘(PROC elem1 elem2 …)’, where each ELEM is from the
     corresponding STREAM.  ‘stream-for-each’ stops when it reaches the
     end of the shortest STREAM.

 -- Function: stream-map proc stream1 stream2 …
     Return a new stream which is the results of applying PROC to the
     elements of the given STREAMs.

     Each call is ‘(PROC elem1 elem2 …)’, where each ELEM is from the
     corresponding STREAM.  The new stream ends when the end of the
     shortest given STREAM is reached.

