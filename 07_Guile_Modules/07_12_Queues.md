7.12 Queues
===========

The functions in this section are provided by

     (use-modules (ice-9 q))

   This module implements queues holding arbitrary scheme objects and
designed for efficient first-in / first-out operations.

   ‘make-q’ creates a queue, and objects are entered and removed with
‘enq!’ and ‘deq!’.  ‘q-push!’ and ‘q-pop!’ can be used too, treating the
front of the queue like a stack.


 -- Scheme Procedure: make-q
     Return a new queue.

 -- Scheme Procedure: q? obj
     Return ‘#t’ if OBJ is a queue, or ‘#f’ if not.

     Note that queues are not a distinct class of objects but are
     implemented with cons cells.  For that reason certain list
     structures can get ‘#t’ from ‘q?’.

 -- Scheme Procedure: enq! q obj
     Add OBJ to the rear of Q, and return Q.

 -- Scheme Procedure: deq! q
 -- Scheme Procedure: q-pop! q
     Remove and return the front element from Q.  If Q is empty, a
     ‘q-empty’ exception is thrown.

     ‘deq!’ and ‘q-pop!’ are the same operation, the two names just let
     an application match ‘enq!’ with ‘deq!’, or ‘q-push!’ with
     ‘q-pop!’.

 -- Scheme Procedure: q-push! q obj
     Add OBJ to the front of Q, and return Q.

 -- Scheme Procedure: q-length q
     Return the number of elements in Q.

 -- Scheme Procedure: q-empty? q
     Return true if Q is empty.

 -- Scheme Procedure: q-empty-check q
     Throw a ‘q-empty’ exception if Q is empty.

 -- Scheme Procedure: q-front q
     Return the first element of Q (without removing it).  If Q is
     empty, a ‘q-empty’ exception is thrown.

 -- Scheme Procedure: q-rear q
     Return the last element of Q (without removing it).  If Q is empty,
     a ‘q-empty’ exception is thrown.

 -- Scheme Procedure: q-remove! q obj
     Remove all occurrences of OBJ from Q, and return Q.  OBJ is
     compared to queue elements using ‘eq?’.


   The ‘q-empty’ exceptions described above are thrown just as ‘(throw
'q-empty)’, there’s no message etc like an error throw.

   A queue is implemented as a cons cell, the ‘car’ containing a list of
queued elements, and the ‘cdr’ being the last cell in that list (for
ease of enqueuing).

     (LIST . LAST-CELL)

If the queue is empty, LIST is the empty list and LAST-CELL is ‘#f’.

   An application can directly access the queue list if desired, for
instance to search the elements or to insert at a specific point.

 -- Scheme Procedure: sync-q! q
     Recompute the LAST-CELL field in Q.

     All the operations above maintain LAST-CELL as described, so
     normally there’s no need for ‘sync-q!’.  But if an application
     modifies the queue LIST then it must either maintain LAST-CELL
     similarly, or call ‘sync-q!’ to recompute it.

