7 Guile Modules
***************

7.1 SLIB
========

SLIB is a portable library of Scheme packages which can be used with
Guile and other Scheme implementations.  SLIB is not included in the
Guile distribution, but can be installed separately (*note SLIB
installation::).  It is available from
<http://people.csail.mit.edu/jaffer/SLIB.html>.

   After SLIB is installed, the following Scheme expression must be
executed before the SLIB facilities can be used:

     (use-modules (ice-9 slib))

‘require’ can then be used in the usual way (*note (slib)Require::).
For example,

     (use-modules (ice-9 slib))
     (require 'primes)
     (prime? 13)
     ⇒ #t

   A few Guile core functions are overridden by the SLIB setups; for
example the SLIB version of ‘delete-file’ returns a boolean indicating
success or failure, whereas the Guile core version throws an error for
failure.  In general (and as might be expected) when SLIB is loaded it’s
the SLIB specifications that are followed.

7.1.1 SLIB installation
-----------------------

The following procedure works, e.g., with SLIB version 3a3 (*note SLIB
installation: (slib)Installation.):

  1. Unpack SLIB and install it using ‘make install’ from its directory.
     By default, this will install SLIB in ‘/usr/local/lib/slib/’.
     Running ‘make install-info’ installs its documentation, by default
     under ‘/usr/local/info/’.

  2. Define the ‘SCHEME_LIBRARY_PATH’ environment variable:

          $ SCHEME_LIBRARY_PATH=/usr/local/lib/slib/
          $ export SCHEME_LIBRARY_PATH

     Alternatively, you can create a symlink in the Guile directory to
     SLIB, e.g.:

          ln -s /usr/local/lib/slib /usr/local/share/guile/2.0/slib

  3. Use Guile to create the catalog file, e.g.,:

          # guile
          guile> (use-modules (ice-9 slib))
          guile> (require 'new-catalog)
          guile> (quit)

     The catalog data should now be in
     ‘/usr/local/share/guile/2.0/slibcat’.

     If instead you get an error such as:

          Unbound variable: scheme-implementation-type

     then a solution is to get a newer version of Guile, or to modify
     ‘ice-9/slib.scm’ to use ‘define-public’ for the offending
     variables.

7.1.2 JACAL
-----------

Jacal is a symbolic math package written in Scheme by Aubrey Jaffer.  It
is usually installed as an extra package in SLIB.

   You can use Guile’s interface to SLIB to invoke Jacal:

     (use-modules (ice-9 slib))
     (slib:load "math")
     (math)

For complete documentation on Jacal, please read the Jacal manual.  If
it has been installed on line, you can look at *note Jacal: (jacal)Top.
Otherwise you can find it on the web at
<http://www-swiss.ai.mit.edu/~jaffer/JACAL.html>

7.2 POSIX System Calls and Networking
=====================================

7.2.1 POSIX Interface Conventions
---------------------------------

These interfaces provide access to operating system facilities.  They
provide a simple wrapping around the underlying C interfaces to make
usage from Scheme more convenient.  They are also used to implement the
Guile port of scsh (*note The Scheme shell (scsh)::).

   Generally there is a single procedure for each corresponding Unix
facility.  There are some exceptions, such as procedures implemented for
speed and convenience in Scheme with no primitive Unix equivalent, e.g.
‘copy-file’.

   The interfaces are intended as far as possible to be portable across
different versions of Unix.  In some cases procedures which can’t be
implemented on particular systems may become no-ops, or perform limited
actions.  In other cases they may throw errors.

   General naming conventions are as follows:

   • The Scheme name is often identical to the name of the underlying
     Unix facility.
   • Underscores in Unix procedure names are converted to hyphens.
   • Procedures which destructively modify Scheme data have exclamation
     marks appended, e.g., ‘recv!’.
   • Predicates (returning only ‘#t’ or ‘#f’) have question marks
     appended, e.g., ‘access?’.
   • Some names are changed to avoid conflict with dissimilar interfaces
     defined by scsh, e.g., ‘primitive-fork’.
   • Unix preprocessor names such as ‘EPERM’ or ‘R_OK’ are converted to
     Scheme variables of the same name (underscores are not replaced
     with hyphens).

   Unexpected conditions are generally handled by raising exceptions.
There are a few procedures which return a special value if they don’t
succeed, e.g., ‘getenv’ returns ‘#f’ if it the requested string is not
found in the environment.  These cases are noted in the documentation.

   For ways to deal with exceptions, see *note Exceptions::.

   Errors which the C library would report by returning a null pointer
or through some other means are reported by raising a ‘system-error’
exception with ‘scm-error’ (*note Error Reporting::).  The DATA
parameter is a list containing the Unix ‘errno’ value (an integer).  For
example,

     (define (my-handler key func fmt fmtargs data)
       (display key) (newline)
       (display func) (newline)
       (apply format #t fmt fmtargs) (newline)
       (display data) (newline))

     (catch 'system-error
       (lambda () (dup2 -123 -456))
       my-handler)

     ⊣
     system-error
     dup2
     Bad file descriptor
     (9)


 -- Function: system-error-errno arglist
     Return the ‘errno’ value from a list which is the arguments to an
     exception handler.  If the exception is not a ‘system-error’, then
     the return is ‘#f’.  For example,

          (catch
           'system-error
           (lambda ()
             (mkdir "/this-ought-to-fail-if-I'm-not-root"))
           (lambda stuff
             (let ((errno (system-error-errno stuff)))
               (cond
                ((= errno EACCES)
                 (display "You're not allowed to do that."))
                ((= errno EEXIST)
                 (display "Already exists."))
                (#t
                 (display (strerror errno))))
               (newline))))

7.2.2 Ports and File Descriptors
--------------------------------

Conventions generally follow those of scsh, *note The Scheme shell
(scsh)::.

   File ports are implemented using low-level operating system I/O
facilities, with optional buffering to improve efficiency; see *note
File Ports::.

   Note that some procedures (e.g., ‘recv!’) will accept ports as
arguments, but will actually operate directly on the file descriptor
underlying the port.  Any port buffering is ignored, including the
buffer which implements ‘peek-char’ and ‘unread-char’.

   The ‘force-output’ and ‘drain-input’ procedures can be used to clear
the buffers.

   Each open file port has an associated operating system file
descriptor.  File descriptors are generally not useful in Scheme
programs; however they may be needed when interfacing with foreign code
and the Unix environment.

   A file descriptor can be extracted from a port and a new port can be
created from a file descriptor.  However a file descriptor is just an
integer and the garbage collector doesn’t recognize it as a reference to
the port.  If all other references to the port were dropped, then it’s
likely that the garbage collector would free the port, with the
side-effect of closing the file descriptor prematurely.

   To assist the programmer in avoiding this problem, each port has an
associated "revealed count" which can be used to keep track of how many
times the underlying file descriptor has been stored in other places.
If a port’s revealed count is greater than zero, the file descriptor
will not be closed when the port is garbage collected.  A programmer can
therefore ensure that the revealed count will be greater than zero if
the file descriptor is needed elsewhere.

   For the simple case where a file descriptor is “imported” once to
become a port, it does not matter if the file descriptor is closed when
the port is garbage collected.  There is no need to maintain a revealed
count.  Likewise when “exporting” a file descriptor to the external
environment, setting the revealed count is not required provided the
port is kept open (i.e., is pointed to by a live Scheme binding) while
the file descriptor is in use.

   To correspond with traditional Unix behaviour, three file descriptors
(0, 1, and 2) are automatically imported when a program starts up and
assigned to the initial values of the current/standard input, output,
and error ports, respectively.  The revealed count for each is initially
set to one, so that dropping references to one of these ports will not
result in its garbage collection: it could be retrieved with ‘fdopen’ or
‘fdes->ports’.

 -- Scheme Procedure: port-revealed port
 -- C Function: scm_port_revealed (port)
     Return the revealed count for PORT.

 -- Scheme Procedure: set-port-revealed! port rcount
 -- C Function: scm_set_port_revealed_x (port, rcount)
     Sets the revealed count for a PORT to RCOUNT.  The return value is
     unspecified.

 -- Scheme Procedure: fileno port
 -- C Function: scm_fileno (port)
     Return the integer file descriptor underlying PORT.  Does not
     change its revealed count.

 -- Scheme Procedure: port->fdes port
     Returns the integer file descriptor underlying PORT.  As a side
     effect the revealed count of PORT is incremented.

 -- Scheme Procedure: fdopen fdes modes
 -- C Function: scm_fdopen (fdes, modes)
     Return a new port based on the file descriptor FDES.  Modes are
     given by the string MODES.  The revealed count of the port is
     initialized to zero.  The MODES string is the same as that accepted
     by ‘open-file’ (*note open-file: File Ports.).

 -- Scheme Procedure: fdes->ports fdes
 -- C Function: scm_fdes_to_ports (fdes)
     Return a list of existing ports which have FDES as an underlying
     file descriptor, without changing their revealed counts.

 -- Scheme Procedure: fdes->inport fdes
     Returns an existing input port which has FDES as its underlying
     file descriptor, if one exists, and increments its revealed count.
     Otherwise, returns a new input port with a revealed count of 1.

 -- Scheme Procedure: fdes->outport fdes
     Returns an existing output port which has FDES as its underlying
     file descriptor, if one exists, and increments its revealed count.
     Otherwise, returns a new output port with a revealed count of 1.

 -- Scheme Procedure: primitive-move->fdes port fdes
 -- C Function: scm_primitive_move_to_fdes (port, fdes)
     Moves the underlying file descriptor for PORT to the integer value
     FDES without changing the revealed count of PORT.  Any other ports
     already using this descriptor will be automatically shifted to new
     descriptors and their revealed counts reset to zero.  The return
     value is ‘#f’ if the file descriptor already had the required value
     or ‘#t’ if it was moved.

 -- Scheme Procedure: move->fdes port fdes
     Moves the underlying file descriptor for PORT to the integer value
     FDES and sets its revealed count to one.  Any other ports already
     using this descriptor will be automatically shifted to new
     descriptors and their revealed counts reset to zero.  The return
     value is unspecified.

 -- Scheme Procedure: release-port-handle port
     Decrements the revealed count for a port.

 -- Scheme Procedure: fsync port_or_fd
 -- C Function: scm_fsync (port_or_fd)
     Copies any unwritten data for the specified output file descriptor
     to disk.  If PORT_OR_FD is a port, its buffer is flushed before the
     underlying file descriptor is fsync’d.  The return value is
     unspecified.

 -- Scheme Procedure: open path flags [mode]
 -- C Function: scm_open (path, flags, mode)
     Open the file named by PATH for reading and/or writing.  FLAGS is
     an integer specifying how the file should be opened.  MODE is an
     integer specifying the permission bits of the file, if it needs to
     be created, before the umask (*note Processes::) is applied.  The
     default is 666 (Unix itself has no default).

     FLAGS can be constructed by combining variables using ‘logior’.
     Basic flags are:

      -- Variable: O_RDONLY
          Open the file read-only.
      -- Variable: O_WRONLY
          Open the file write-only.
      -- Variable: O_RDWR
          Open the file read/write.
      -- Variable: O_APPEND
          Append to the file instead of truncating.
      -- Variable: O_CREAT
          Create the file if it does not already exist.

     *Note (libc)File Status Flags::, for additional flags.

 -- Scheme Procedure: open-fdes path flags [mode]
 -- C Function: scm_open_fdes (path, flags, mode)
     Similar to ‘open’ but return a file descriptor instead of a port.

 -- Scheme Procedure: close fd_or_port
 -- C Function: scm_close (fd_or_port)
     Similar to ‘close-port’ (*note close-port: Closing.), but also
     works on file descriptors.  A side effect of closing a file
     descriptor is that any ports using that file descriptor are moved
     to a different file descriptor and have their revealed counts set
     to zero.

 -- Scheme Procedure: close-fdes fd
 -- C Function: scm_close_fdes (fd)
     A simple wrapper for the ‘close’ system call.  Close file
     descriptor FD, which must be an integer.  Unlike ‘close’, the file
     descriptor will be closed even if a port is using it.  The return
     value is unspecified.

 -- Scheme Procedure: unread-char char [port]
 -- C Function: scm_unread_char (char, port)
     Place CHAR in PORT so that it will be read by the next read
     operation on that port.  If called multiple times, the unread
     characters will be read again in “last-in, first-out” order (i.e. a
     stack).  If PORT is not supplied, the current input port is used.

 -- Scheme Procedure: unread-string str port
     Place the string STR in PORT so that its characters will be read in
     subsequent read operations.  If called multiple times, the unread
     characters will be read again in last-in first-out order.  If PORT
     is not supplied, the current-input-port is used.

 -- Scheme Procedure: pipe
 -- C Function: scm_pipe ()
     Return a newly created pipe: a pair of ports which are linked
     together on the local machine.  The CAR is the input port and the
     CDR is the output port.  Data written (and flushed) to the output
     port can be read from the input port.  Pipes are commonly used for
     communication with a newly forked child process.  The need to flush
     the output port can be avoided by making it unbuffered using
     ‘setvbuf’.

      -- Variable: PIPE_BUF
          A write of up to ‘PIPE_BUF’ many bytes to a pipe is atomic,
          meaning when done it goes into the pipe instantaneously and as
          a contiguous block (*note Atomicity of Pipe I/O: (libc)Pipe
          Atomicity.).

     Note that the output port is likely to block if too much data has
     been written but not yet read from the input port.  Typically the
     capacity is ‘PIPE_BUF’ bytes.

   The next group of procedures perform a ‘dup2’ system call, if NEWFD
(an integer) is supplied, otherwise a ‘dup’.  The file descriptor to be
duplicated can be supplied as an integer or contained in a port.  The
type of value returned varies depending on which procedure is used.

   All procedures also have the side effect when performing ‘dup2’ that
any ports using NEWFD are moved to a different file descriptor and have
their revealed counts set to zero.

 -- Scheme Procedure: dup->fdes fd_or_port [fd]
 -- C Function: scm_dup_to_fdes (fd_or_port, fd)
     Return a new integer file descriptor referring to the open file
     designated by FD_OR_PORT, which must be either an open file port or
     a file descriptor.

 -- Scheme Procedure: dup->inport port/fd [newfd]
     Returns a new input port using the new file descriptor.

 -- Scheme Procedure: dup->outport port/fd [newfd]
     Returns a new output port using the new file descriptor.

 -- Scheme Procedure: dup port/fd [newfd]
     Returns a new port if PORT/FD is a port, with the same mode as the
     supplied port, otherwise returns an integer file descriptor.

 -- Scheme Procedure: dup->port port/fd mode [newfd]
     Returns a new port using the new file descriptor.  MODE supplies a
     mode string for the port (*note open-file: File Ports.).

 -- Scheme Procedure: duplicate-port port modes
     Returns a new port which is opened on a duplicate of the file
     descriptor underlying PORT, with mode string MODES as for *note
     open-file: File Ports.  The two ports will share a file position
     and file status flags.

     Unexpected behaviour can result if both ports are subsequently used
     and the original and/or duplicate ports are buffered.  The mode
     string can include ‘0’ to obtain an unbuffered duplicate port.

     This procedure is equivalent to ‘(dup->port PORT MODES)’.

 -- Scheme Procedure: redirect-port old_port new_port
 -- C Function: scm_redirect_port (old_port, new_port)
     This procedure takes two ports and duplicates the underlying file
     descriptor from OLD_PORT into NEW_PORT.  The current file
     descriptor in NEW_PORT will be closed.  After the redirection the
     two ports will share a file position and file status flags.

     The return value is unspecified.

     Unexpected behaviour can result if both ports are subsequently used
     and the original and/or duplicate ports are buffered.

     This procedure does not have any side effects on other ports or
     revealed counts.

 -- Scheme Procedure: dup2 oldfd newfd
 -- C Function: scm_dup2 (oldfd, newfd)
     A simple wrapper for the ‘dup2’ system call.  Copies the file
     descriptor OLDFD to descriptor number NEWFD, replacing the previous
     meaning of NEWFD.  Both OLDFD and NEWFD must be integers.  Unlike
     for ‘dup->fdes’ or ‘primitive-move->fdes’, no attempt is made to
     move away ports which are using NEWFD.  The return value is
     unspecified.

 -- Scheme Procedure: port-mode port
     Return the port modes associated with the open port PORT.  These
     will not necessarily be identical to the modes used when the port
     was opened, since modes such as “append” which are used only during
     port creation are not retained.

 -- Scheme Procedure: port-for-each proc
 -- C Function: scm_port_for_each (SCM proc)
 -- C Function: scm_c_port_for_each (void (*proc)(void *, SCM), void
          *data)
     Apply PROC to each port in the Guile port table (FIXME: what is the
     Guile port table?)  in turn.  The return value is unspecified.
     More specifically, PROC is applied exactly once to every port that
     exists in the system at the time ‘port-for-each’ is invoked.
     Changes to the port table while ‘port-for-each’ is running have no
     effect as far as ‘port-for-each’ is concerned.

     The C function ‘scm_port_for_each’ takes a Scheme procedure encoded
     as a ‘SCM’ value, while ‘scm_c_port_for_each’ takes a pointer to a
     C function and passes along a arbitrary DATA cookie.

 -- Scheme Procedure: setvbuf port mode [size]
 -- C Function: scm_setvbuf (port, mode, size)
     Set the buffering mode for PORT.  MODE can be:

      -- Variable: _IONBF
          non-buffered
      -- Variable: _IOLBF
          line buffered
      -- Variable: _IOFBF
          block buffered, using a newly allocated buffer of SIZE bytes.
          If SIZE is omitted, a default size will be used.

     Only certain types of ports are supported, most importantly file
     ports.

 -- Scheme Procedure: fcntl port/fd cmd [value]
 -- C Function: scm_fcntl (object, cmd, value)
     Apply CMD on PORT/FD, either a port or file descriptor.  The VALUE
     argument is used by the ‘SET’ commands described below, it’s an
     integer value.

     Values for CMD are:

      -- Variable: F_DUPFD
          Duplicate the file descriptor, the same as ‘dup->fdes’ above
          does.

      -- Variable: F_GETFD
      -- Variable: F_SETFD
          Get or set flags associated with the file descriptor.  The
          only flag is the following,

           -- Variable: FD_CLOEXEC
               “Close on exec”, meaning the file descriptor will be
               closed on an ‘exec’ call (a successful such call).  For
               example to set that flag,

                    (fcntl port F_SETFD FD_CLOEXEC)

               Or better, set it but leave any other possible future
               flags unchanged,

                    (fcntl port F_SETFD (logior FD_CLOEXEC
                                                (fcntl port F_GETFD)))

      -- Variable: F_GETFL
      -- Variable: F_SETFL
          Get or set flags associated with the open file.  These flags
          are ‘O_RDONLY’ etc described under ‘open’ above.

          A common use is to set ‘O_NONBLOCK’ on a network socket.  The
          following sets that flag, and leaves other flags unchanged.

               (fcntl sock F_SETFL (logior O_NONBLOCK
                                           (fcntl sock F_GETFL)))

      -- Variable: F_GETOWN
      -- Variable: F_SETOWN
          Get or set the process ID of a socket’s owner, for ‘SIGIO’
          signals.

 -- Scheme Procedure: flock file operation
 -- C Function: scm_flock (file, operation)
     Apply or remove an advisory lock on an open file.  OPERATION
     specifies the action to be done:

      -- Variable: LOCK_SH
          Shared lock.  More than one process may hold a shared lock for
          a given file at a given time.
      -- Variable: LOCK_EX
          Exclusive lock.  Only one process may hold an exclusive lock
          for a given file at a given time.
      -- Variable: LOCK_UN
          Unlock the file.
      -- Variable: LOCK_NB
          Don’t block when locking.  This is combined with one of the
          other operations using ‘logior’ (*note Bitwise Operations::).
          If ‘flock’ would block an ‘EWOULDBLOCK’ error is thrown (*note
          Conventions::).

     The return value is not specified.  FILE may be an open file
     descriptor or an open file descriptor port.

     Note that ‘flock’ does not lock files across NFS.

 -- Scheme Procedure: select reads writes excepts [secs [usecs]]
 -- C Function: scm_select (reads, writes, excepts, secs, usecs)
     This procedure has a variety of uses: waiting for the ability to
     provide input, accept output, or the existence of exceptional
     conditions on a collection of ports or file descriptors, or waiting
     for a timeout to occur.  It also returns if interrupted by a
     signal.

     READS, WRITES and EXCEPTS can be lists or vectors, with each member
     a port or a file descriptor.  The value returned is a list of three
     corresponding lists or vectors containing only the members which
     meet the specified requirement.  The ability of port buffers to
     provide input or accept output is taken into account.  Ordering of
     the input lists or vectors is not preserved.

     The optional arguments SECS and USECS specify the timeout.  Either
     SECS can be specified alone, as either an integer or a real number,
     or both SECS and USECS can be specified as integers, in which case
     USECS is an additional timeout expressed in microseconds.  If SECS
     is omitted or is ‘#f’ then select will wait for as long as it takes
     for one of the other conditions to be satisfied.

     The scsh version of ‘select’ differs as follows: Only vectors are
     accepted for the first three arguments.  The USECS argument is not
     supported.  Multiple values are returned instead of a list.
     Duplicates in the input vectors appear only once in output.  An
     additional ‘select!’ interface is provided.

7.2.3 File System
-----------------

These procedures allow querying and setting file system attributes (such
as owner, permissions, sizes and types of files); deleting, copying,
renaming and linking files; creating and removing directories and
querying their contents; syncing the file system and creating special
files.

 -- Scheme Procedure: access? path how
 -- C Function: scm_access (path, how)
     Test accessibility of a file under the real UID and GID of the
     calling process.  The return is ‘#t’ if PATH exists and the
     permissions requested by HOW are all allowed, or ‘#f’ if not.

     HOW is an integer which is one of the following values, or a
     bitwise-OR (‘logior’) of multiple values.

      -- Variable: R_OK
          Test for read permission.
      -- Variable: W_OK
          Test for write permission.
      -- Variable: X_OK
          Test for execute permission.
      -- Variable: F_OK
          Test for existence of the file.  This is implied by each of
          the other tests, so there’s no need to combine it with them.

     It’s important to note that ‘access?’ does not simply indicate what
     will happen on attempting to read or write a file.  In normal
     circumstances it does, but in a set-UID or set-GID program it
     doesn’t because ‘access?’ tests the real ID, whereas an open or
     execute attempt uses the effective ID.

     A program which will never run set-UID/GID can ignore the
     difference between real and effective IDs, but for maximum
     generality, especially in library functions, it’s best not to use
     ‘access?’ to predict the result of an open or execute, instead
     simply attempt that and catch any exception.

     The main use for ‘access?’ is to let a set-UID/GID program
     determine what the invoking user would have been allowed to do,
     without the greater (or perhaps lesser) privileges afforded by the
     effective ID. For more on this, see *note (libc)Testing File
     Access::.

 -- Scheme Procedure: stat object
 -- C Function: scm_stat (object)
     Return an object containing various information about the file
     determined by OBJECT.  OBJECT can be a string containing a file
     name or a port or integer file descriptor which is open on a file
     (in which case ‘fstat’ is used as the underlying system call).

     The object returned by ‘stat’ can be passed as a single parameter
     to the following procedures, all of which return integers:

      -- Scheme Procedure: stat:dev st
          The device number containing the file.
      -- Scheme Procedure: stat:ino st
          The file serial number, which distinguishes this file from all
          other files on the same device.
      -- Scheme Procedure: stat:mode st
          The mode of the file.  This is an integer which incorporates
          file type information and file permission bits.  See also
          ‘stat:type’ and ‘stat:perms’ below.
      -- Scheme Procedure: stat:nlink st
          The number of hard links to the file.
      -- Scheme Procedure: stat:uid st
          The user ID of the file’s owner.
      -- Scheme Procedure: stat:gid st
          The group ID of the file.
      -- Scheme Procedure: stat:rdev st
          Device ID; this entry is defined only for character or block
          special files.  On some systems this field is not available at
          all, in which case ‘stat:rdev’ returns ‘#f’.
      -- Scheme Procedure: stat:size st
          The size of a regular file in bytes.
      -- Scheme Procedure: stat:atime st
          The last access time for the file, in seconds.
      -- Scheme Procedure: stat:mtime st
          The last modification time for the file, in seconds.
      -- Scheme Procedure: stat:ctime st
          The last modification time for the attributes of the file, in
          seconds.
      -- Scheme Procedure: stat:atimensec st
      -- Scheme Procedure: stat:mtimensec st
      -- Scheme Procedure: stat:ctimensec st
          The fractional part of a file’s access, modification, or
          attribute modification time, in nanoseconds.  Nanosecond
          timestamps are only available on some operating systems and
          file systems.  If Guile cannot retrieve nanosecond-level
          timestamps for a file, these fields will be set to 0.
      -- Scheme Procedure: stat:blksize st
          The optimal block size for reading or writing the file, in
          bytes.  On some systems this field is not available, in which
          case ‘stat:blksize’ returns a sensible suggested block size.
      -- Scheme Procedure: stat:blocks st
          The amount of disk space that the file occupies measured in
          units of 512 byte blocks.  On some systems this field is not
          available, in which case ‘stat:blocks’ returns ‘#f’.

     In addition, the following procedures return the information from
     ‘stat:mode’ in a more convenient form:

      -- Scheme Procedure: stat:type st
          A symbol representing the type of file.  Possible values are
          ‘regular’, ‘directory’, ‘symlink’, ‘block-special’,
          ‘char-special’, ‘fifo’, ‘socket’, and ‘unknown’.
      -- Scheme Procedure: stat:perms st
          An integer representing the access permission bits.

 -- Scheme Procedure: lstat path
 -- C Function: scm_lstat (path)
     Similar to ‘stat’, but does not follow symbolic links, i.e., it
     will return information about a symbolic link itself, not the file
     it points to.  PATH must be a string.

 -- Scheme Procedure: readlink path
 -- C Function: scm_readlink (path)
     Return the value of the symbolic link named by PATH (a string),
     i.e., the file that the link points to.

 -- Scheme Procedure: chown object owner group
 -- C Function: scm_chown (object, owner, group)
     Change the ownership and group of the file referred to by OBJECT to
     the integer values OWNER and GROUP.  OBJECT can be a string
     containing a file name or, if the platform supports ‘fchown’ (*note
     (libc)File Owner::), a port or integer file descriptor which is
     open on the file.  The return value is unspecified.

     If OBJECT is a symbolic link, either the ownership of the link or
     the ownership of the referenced file will be changed depending on
     the operating system (lchown is unsupported at present).  If OWNER
     or GROUP is specified as ‘-1’, then that ID is not changed.

 -- Scheme Procedure: chmod object mode
 -- C Function: scm_chmod (object, mode)
     Changes the permissions of the file referred to by OBJECT.  OBJECT
     can be a string containing a file name or a port or integer file
     descriptor which is open on a file (in which case ‘fchmod’ is used
     as the underlying system call).  MODE specifies the new permissions
     as a decimal number, e.g., ‘(chmod "foo" #o755)’.  The return value
     is unspecified.

 -- Scheme Procedure: utime pathname [actime [modtime [actimens
          [modtimens [flags]]]]]
 -- C Function: scm_utime (pathname, actime, modtime, actimens,
          modtimens, flags)
     ‘utime’ sets the access and modification times for the file named
     by PATHNAME.  If ACTIME or MODTIME is not supplied, then the
     current time is used.  ACTIME and MODTIME must be integer time
     values as returned by the ‘current-time’ procedure.

     The optional ACTIMENS and MODTIMENS are nanoseconds to add ACTIME
     and MODTIME.  Nanosecond precision is only supported on some
     combinations of file systems and operating systems.
          (utime "foo" (- (current-time) 3600))
     will set the access time to one hour in the past and the
     modification time to the current time.

 -- Scheme Procedure: delete-file str
 -- C Function: scm_delete_file (str)
     Deletes (or “unlinks”) the file whose path is specified by STR.

 -- Scheme Procedure: copy-file oldfile newfile
 -- C Function: scm_copy_file (oldfile, newfile)
     Copy the file specified by OLDFILE to NEWFILE.  The return value is
     unspecified.

 -- Scheme Procedure: sendfile out in count [offset]
 -- C Function: scm_sendfile (out, in, count, offset)
     Send COUNT bytes from IN to OUT, both of which must be either open
     file ports or file descriptors.  When OFFSET is omitted, start
     reading from IN’s current position; otherwise, start reading at
     OFFSET.  Return the number of bytes actually sent.

     When IN is a port, it is often preferable to specify OFFSET,
     because IN’s offset as a port may be different from the offset of
     its underlying file descriptor.

     On systems that support it, such as GNU/Linux, this procedure uses
     the ‘sendfile’ libc function, which usually corresponds to a system
     call.  This is faster than doing a series of ‘read’ and ‘write’
     system calls.  A typical application is to send a file over a
     socket.

     In some cases, the ‘sendfile’ libc function may return ‘EINVAL’ or
     ‘ENOSYS’.  In that case, Guile’s ‘sendfile’ procedure automatically
     falls back to doing a series of ‘read’ and ‘write’ calls.

     In other cases, the libc function may send fewer bytes than
     COUNT—for instance because OUT is a slow or limited device, such as
     a pipe.  When that happens, Guile’s ‘sendfile’ automatically
     retries until exactly COUNT bytes were sent or an error occurs.

 -- Scheme Procedure: rename-file oldname newname
 -- C Function: scm_rename (oldname, newname)
     Renames the file specified by OLDNAME to NEWNAME.  The return value
     is unspecified.

 -- Scheme Procedure: link oldpath newpath
 -- C Function: scm_link (oldpath, newpath)
     Creates a new name NEWPATH in the file system for the file named by
     OLDPATH.  If OLDPATH is a symbolic link, the link may or may not be
     followed depending on the system.

 -- Scheme Procedure: symlink oldpath newpath
 -- C Function: scm_symlink (oldpath, newpath)
     Create a symbolic link named NEWPATH with the value (i.e., pointing
     to) OLDPATH.  The return value is unspecified.

 -- Scheme Procedure: mkdir path [mode]
 -- C Function: scm_mkdir (path, mode)
     Create a new directory named by PATH.  If MODE is omitted then the
     permissions of the directory file are set using the current umask
     (*note Processes::).  Otherwise they are set to the decimal value
     specified with MODE.  The return value is unspecified.

 -- Scheme Procedure: rmdir path
 -- C Function: scm_rmdir (path)
     Remove the existing directory named by PATH.  The directory must be
     empty for this to succeed.  The return value is unspecified.

 -- Scheme Procedure: opendir dirname
 -- C Function: scm_opendir (dirname)
     Open the directory specified by DIRNAME and return a directory
     stream.

     Before using this and the procedures below, make sure to see the
     higher-level procedures for directory traversal that are available
     (*note File Tree Walk::).

 -- Scheme Procedure: directory-stream? object
 -- C Function: scm_directory_stream_p (object)
     Return a boolean indicating whether OBJECT is a directory stream as
     returned by ‘opendir’.

 -- Scheme Procedure: readdir stream
 -- C Function: scm_readdir (stream)
     Return (as a string) the next directory entry from the directory
     stream STREAM.  If there is no remaining entry to be read then the
     end of file object is returned.

 -- Scheme Procedure: rewinddir stream
 -- C Function: scm_rewinddir (stream)
     Reset the directory port STREAM so that the next call to ‘readdir’
     will return the first directory entry.

 -- Scheme Procedure: closedir stream
 -- C Function: scm_closedir (stream)
     Close the directory stream STREAM.  The return value is
     unspecified.

   Here is an example showing how to display all the entries in a
directory:

     (define dir (opendir "/usr/lib"))
     (do ((entry (readdir dir) (readdir dir)))
         ((eof-object? entry))
       (display entry)(newline))
     (closedir dir)

 -- Scheme Procedure: sync
 -- C Function: scm_sync ()
     Flush the operating system disk buffers.  The return value is
     unspecified.

 -- Scheme Procedure: mknod path type perms dev
 -- C Function: scm_mknod (path, type, perms, dev)
     Creates a new special file, such as a file corresponding to a
     device.  PATH specifies the name of the file.  TYPE should be one
     of the following symbols: ‘regular’, ‘directory’, ‘symlink’,
     ‘block-special’, ‘char-special’, ‘fifo’, or ‘socket’.  PERMS (an
     integer) specifies the file permissions.  DEV (an integer)
     specifies which device the special file refers to.  Its exact
     interpretation depends on the kind of special file being created.

     E.g.,
          (mknod "/dev/fd0" 'block-special #o660 (+ (* 2 256) 2))

     The return value is unspecified.

 -- Scheme Procedure: tmpnam
 -- C Function: scm_tmpnam ()
     Return an auto-generated name of a temporary file, a file which
     doesn’t already exist.  The name includes a path, it’s usually in
     ‘/tmp’ but that’s system dependent.

     Care must be taken when using ‘tmpnam’.  In between choosing the
     name and creating the file another program might use that name, or
     an attacker might even make it a symlink pointing at something
     important and causing you to overwrite that.

     The safe way is to create the file using ‘open’ with ‘O_EXCL’ to
     avoid any overwriting.  A loop can try again with another name if
     the file exists (error ‘EEXIST’).  ‘mkstemp!’ below does that.

 -- Scheme Procedure: mkstemp! tmpl
 -- C Function: scm_mkstemp (tmpl)
     Create a new unique file in the file system and return a new
     buffered port open for reading and writing to the file.

     TMPL is a string specifying where the file should be created: it
     must end with ‘XXXXXX’ and those ‘X’s will be changed in the string
     to return the name of the file.  (‘port-filename’ on the port also
     gives the name.)

     POSIX doesn’t specify the permissions mode of the file, on GNU and
     most systems it’s ‘#o600’.  An application can use ‘chmod’ to relax
     that if desired.  For example ‘#o666’ less ‘umask’, which is usual
     for ordinary file creation,

          (let ((port (mkstemp! (string-copy "/tmp/myfile-XXXXXX"))))
            (chmod port (logand #o666 (lognot (umask))))
            ...)

 -- Scheme Procedure: tmpfile
 -- C Function: scm_tmpfile ()
     Return an input/output port to a unique temporary file named using
     the path prefix ‘P_tmpdir’ defined in ‘stdio.h’.  The file is
     automatically deleted when the port is closed or the program
     terminates.

 -- Scheme Procedure: dirname filename
 -- C Function: scm_dirname (filename)
     Return the directory name component of the file name FILENAME.  If
     FILENAME does not contain a directory component, ‘.’ is returned.

 -- Scheme Procedure: basename filename [suffix]
 -- C Function: scm_basename (filename, suffix)
     Return the base name of the file name FILENAME.  The base name is
     the file name without any directory components.  If SUFFIX is
     provided, and is equal to the end of BASENAME, it is removed also.

          (basename "/tmp/test.xml" ".xml")
          ⇒ "test"

 -- Scheme Procedure: file-exists? filename
     Return ‘#t’ if the file named FILENAME exists, ‘#f’ if not.

   Many operating systems, such as GNU, use ‘/’ (forward slash) to
separate the components of a file name; any file name starting with ‘/’
is considered an "absolute file name".  These conventions are specified
by the POSIX Base Definitions, which refer to conforming file names as
“pathnames”.  Some operating systems use a different convention; in
particular, Windows uses ‘\’ (backslash) as the file name separator, and
also has the notion of "volume names" like ‘C:\’ for absolute file
names.  The following procedures and variables provide support for
portable file name manipulations.

 -- Scheme Procedure: system-file-name-convention
     Return either ‘posix’ or ‘windows’, depending on what kind of
     system this Guile is running on.

 -- Scheme Procedure: file-name-separator? c
     Return true if character C is a file name separator on the host
     platform.

 -- Scheme Procedure: absolute-file-name? file-name
     Return true if FILE-NAME denotes an absolute file name on the host
     platform.

 -- Scheme Variable: file-name-separator-string
     The preferred file name separator.

     Note that on MinGW builds for Windows, both ‘/’ and ‘\’ are valid
     separators.  Thus, programs should not assume that
     ‘file-name-separator-string’ is the _only_ file name
     separator—e.g., when extracting the components of a file name.

7.2.4 User Information
----------------------

The facilities in this section provide an interface to the user and
group database.  They should be used with care since they are not
reentrant.

   The following functions accept an object representing user
information and return a selected component:

 -- Scheme Procedure: passwd:name pw
     The name of the userid.
 -- Scheme Procedure: passwd:passwd pw
     The encrypted passwd.
 -- Scheme Procedure: passwd:uid pw
     The user id number.
 -- Scheme Procedure: passwd:gid pw
     The group id number.
 -- Scheme Procedure: passwd:gecos pw
     The full name.
 -- Scheme Procedure: passwd:dir pw
     The home directory.
 -- Scheme Procedure: passwd:shell pw
     The login shell.

 -- Scheme Procedure: getpwuid uid
     Look up an integer userid in the user database.

 -- Scheme Procedure: getpwnam name
     Look up a user name string in the user database.

 -- Scheme Procedure: setpwent
     Initializes a stream used by ‘getpwent’ to read from the user
     database.  The next use of ‘getpwent’ will return the first entry.
     The return value is unspecified.

 -- Scheme Procedure: getpwent
     Read the next entry in the user database stream.  The return is a
     passwd user object as above, or ‘#f’ when no more entries.

 -- Scheme Procedure: endpwent
     Closes the stream used by ‘getpwent’.  The return value is
     unspecified.

 -- Scheme Procedure: setpw [arg]
 -- C Function: scm_setpwent (arg)
     If called with a true argument, initialize or reset the password
     data stream.  Otherwise, close the stream.  The ‘setpwent’ and
     ‘endpwent’ procedures are implemented on top of this.

 -- Scheme Procedure: getpw [user]
 -- C Function: scm_getpwuid (user)
     Look up an entry in the user database.  USER can be an integer, a
     string, or omitted, giving the behaviour of getpwuid, getpwnam or
     getpwent respectively.

   The following functions accept an object representing group
information and return a selected component:

 -- Scheme Procedure: group:name gr
     The group name.
 -- Scheme Procedure: group:passwd gr
     The encrypted group password.
 -- Scheme Procedure: group:gid gr
     The group id number.
 -- Scheme Procedure: group:mem gr
     A list of userids which have this group as a supplementary group.

 -- Scheme Procedure: getgrgid gid
     Look up an integer group id in the group database.

 -- Scheme Procedure: getgrnam name
     Look up a group name in the group database.

 -- Scheme Procedure: setgrent
     Initializes a stream used by ‘getgrent’ to read from the group
     database.  The next use of ‘getgrent’ will return the first entry.
     The return value is unspecified.

 -- Scheme Procedure: getgrent
     Return the next entry in the group database, using the stream set
     by ‘setgrent’.

 -- Scheme Procedure: endgrent
     Closes the stream used by ‘getgrent’.  The return value is
     unspecified.

 -- Scheme Procedure: setgr [arg]
 -- C Function: scm_setgrent (arg)
     If called with a true argument, initialize or reset the group data
     stream.  Otherwise, close the stream.  The ‘setgrent’ and
     ‘endgrent’ procedures are implemented on top of this.

 -- Scheme Procedure: getgr [group]
 -- C Function: scm_getgrgid (group)
     Look up an entry in the group database.  GROUP can be an integer, a
     string, or omitted, giving the behaviour of getgrgid, getgrnam or
     getgrent respectively.

   In addition to the accessor procedures for the user database, the
following shortcut procedure is also available.

 -- Scheme Procedure: getlogin
 -- C Function: scm_getlogin ()
     Return a string containing the name of the user logged in on the
     controlling terminal of the process, or ‘#f’ if this information
     cannot be obtained.

7.2.5 Time
----------

 -- Scheme Procedure: current-time
 -- C Function: scm_current_time ()
     Return the number of seconds since 1970-01-01 00:00:00 UTC,
     excluding leap seconds.

 -- Scheme Procedure: gettimeofday
 -- C Function: scm_gettimeofday ()
     Return a pair containing the number of seconds and microseconds
     since 1970-01-01 00:00:00 UTC, excluding leap seconds.  Note:
     whether true microsecond resolution is available depends on the
     operating system.

   The following procedures either accept an object representing a
broken down time and return a selected component, or accept an object
representing a broken down time and a value and set the component to the
value.  The numbers in parentheses give the usual range.

 -- Scheme Procedure: tm:sec tm
 -- Scheme Procedure: set-tm:sec tm val
     Seconds (0-59).
 -- Scheme Procedure: tm:min tm
 -- Scheme Procedure: set-tm:min tm val
     Minutes (0-59).
 -- Scheme Procedure: tm:hour tm
 -- Scheme Procedure: set-tm:hour tm val
     Hours (0-23).
 -- Scheme Procedure: tm:mday tm
 -- Scheme Procedure: set-tm:mday tm val
     Day of the month (1-31).
 -- Scheme Procedure: tm:mon tm
 -- Scheme Procedure: set-tm:mon tm val
     Month (0-11).
 -- Scheme Procedure: tm:year tm
 -- Scheme Procedure: set-tm:year tm val
     Year (70-), the year minus 1900.
 -- Scheme Procedure: tm:wday tm
 -- Scheme Procedure: set-tm:wday tm val
     Day of the week (0-6) with Sunday represented as 0.
 -- Scheme Procedure: tm:yday tm
 -- Scheme Procedure: set-tm:yday tm val
     Day of the year (0-364, 365 in leap years).
 -- Scheme Procedure: tm:isdst tm
 -- Scheme Procedure: set-tm:isdst tm val
     Daylight saving indicator (0 for “no”, greater than 0 for “yes”,
     less than 0 for “unknown”).
 -- Scheme Procedure: tm:gmtoff tm
 -- Scheme Procedure: set-tm:gmtoff tm val
     Time zone offset in seconds west of UTC (-46800 to 43200).  For
     example on East coast USA (zone ‘EST+5’) this would be 18000 (ie.
     5*60*60) in winter, or 14400 (ie. 4*60*60) during daylight savings.

     Note ‘tm:gmtoff’ is not the same as ‘tm_gmtoff’ in the C ‘tm’
     structure.  ‘tm_gmtoff’ is seconds east and hence the negative of
     the value here.
 -- Scheme Procedure: tm:zone tm
 -- Scheme Procedure: set-tm:zone tm val
     Time zone label (a string), not necessarily unique.

 -- Scheme Procedure: localtime time [zone]
 -- C Function: scm_localtime (time, zone)
     Return an object representing the broken down components of TIME,
     an integer like the one returned by ‘current-time’.  The time zone
     for the calculation is optionally specified by ZONE (a string),
     otherwise the ‘TZ’ environment variable or the system default is
     used.

 -- Scheme Procedure: gmtime time
 -- C Function: scm_gmtime (time)
     Return an object representing the broken down components of TIME,
     an integer like the one returned by ‘current-time’.  The values are
     calculated for UTC.

 -- Scheme Procedure: mktime sbd-time [zone]
 -- C Function: scm_mktime (sbd_time, zone)
     For a broken down time object SBD-TIME, return a pair the ‘car’ of
     which is an integer time like ‘current-time’, and the ‘cdr’ of
     which is a new broken down time with normalized fields.

     ZONE is a timezone string, or the default is the ‘TZ’ environment
     variable or the system default (*note Specifying the Time Zone with
     ‘TZ’: (libc)TZ Variable.).  SBD-TIME is taken to be in that ZONE.

     The following fields of SBD-TIME are used: ‘tm:year’, ‘tm:mon’,
     ‘tm:mday’, ‘tm:hour’, ‘tm:min’, ‘tm:sec’, ‘tm:isdst’.  The values
     can be outside their usual ranges.  For example ‘tm:hour’ normally
     goes up to 23, but a value say 33 would mean 9 the following day.

     ‘tm:isdst’ in SBD-TIME says whether the time given is with daylight
     savings or not.  This is ignored if ZONE doesn’t have any daylight
     savings adjustment amount.

     The broken down time in the return normalizes the values of
     SBD-TIME by bringing them into their usual ranges, and using the
     actual daylight savings rule for that time in ZONE (which may
     differ from what SBD-TIME had).  The easiest way to think of this
     is that SBD-TIME plus ZONE converts to the integer UTC time, then a
     ‘localtime’ is applied to get the normal presentation of that time,
     in ZONE.

 -- Scheme Procedure: tzset
 -- C Function: scm_tzset ()
     Initialize the timezone from the ‘TZ’ environment variable or the
     system default.  It’s not usually necessary to call this procedure
     since it’s done automatically by other procedures that depend on
     the timezone.

 -- Scheme Procedure: strftime format tm
 -- C Function: scm_strftime (format, tm)
     Return a string which is broken-down time structure TM formatted
     according to the given FORMAT string.

     FORMAT contains field specifications introduced by a ‘%’ character.
     See *note (libc)Formatting Calendar Time::, or ‘man 3 strftime’,
     for the available formatting.

          (strftime "%c" (localtime (current-time)))
          ⇒ "Mon Mar 11 20:17:43 2002"

     If ‘setlocale’ has been called (*note Locales::), month and day
     names are from the current locale and in the locale character set.

 -- Scheme Procedure: strptime format string
 -- C Function: scm_strptime (format, string)
     Performs the reverse action to ‘strftime’, parsing STRING according
     to the specification supplied in FORMAT.  The interpretation of
     month and day names is dependent on the current locale.  The value
     returned is a pair.  The CAR has an object with time components in
     the form returned by ‘localtime’ or ‘gmtime’, but the time zone
     components are not usefully set.  The CDR reports the number of
     characters from STRING which were used for the conversion.

 -- Variable: internal-time-units-per-second
     The value of this variable is the number of time units per second
     reported by the following procedures.

 -- Scheme Procedure: times
 -- C Function: scm_times ()
     Return an object with information about real and processor time.
     The following procedures accept such an object as an argument and
     return a selected component:

      -- Scheme Procedure: tms:clock tms
          The current real time, expressed as time units relative to an
          arbitrary base.
      -- Scheme Procedure: tms:utime tms
          The CPU time units used by the calling process.
      -- Scheme Procedure: tms:stime tms
          The CPU time units used by the system on behalf of the calling
          process.
      -- Scheme Procedure: tms:cutime tms
          The CPU time units used by terminated child processes of the
          calling process, whose status has been collected (e.g., using
          ‘waitpid’).
      -- Scheme Procedure: tms:cstime tms
          Similarly, the CPU times units used by the system on behalf of
          terminated child processes.

 -- Scheme Procedure: get-internal-real-time
 -- C Function: scm_get_internal_real_time ()
     Return the number of time units since the interpreter was started.

 -- Scheme Procedure: get-internal-run-time
 -- C Function: scm_get_internal_run_time ()
     Return the number of time units of processor time used by the
     interpreter.  Both _system_ and _user_ time are included but
     subprocesses are not.

7.2.6 Runtime Environment
-------------------------

 -- Scheme Procedure: program-arguments
 -- Scheme Procedure: command-line
 -- Scheme Procedure: set-program-arguments
 -- C Function: scm_program_arguments ()
 -- C Function: scm_set_program_arguments_scm (lst)
     Get the command line arguments passed to Guile, or set new
     arguments.

     The arguments are a list of strings, the first of which is the
     invoked program name.  This is just "guile" (or the executable
     path) when run interactively, or it’s the script name when running
     a script with ‘-s’ (*note Invoking Guile::).

          guile -L /my/extra/dir -s foo.scm abc def

          (program-arguments) ⇒ ("foo.scm" "abc" "def")

     ‘set-program-arguments’ allows a library module or similar to
     modify the arguments, for example to strip options it recognises,
     leaving the rest for the mainline.

     The argument list is held in a fluid, which means it’s separate for
     each thread.  Neither the list nor the strings within it are copied
     at any point and normally should not be mutated.

     The two names ‘program-arguments’ and ‘command-line’ are an
     historical accident, they both do exactly the same thing.  The name
     ‘scm_set_program_arguments_scm’ has an extra ‘_scm’ on the end to
     avoid clashing with the C function below.

 -- C Function: void scm_set_program_arguments (int argc, char **argv,
          char *first)
     Set the list of command line arguments for ‘program-arguments’ and
     ‘command-line’ above.

     ARGV is an array of null-terminated strings, as in a C ‘main’
     function.  ARGC is the number of strings in ARGV, or if it’s
     negative then a ‘NULL’ in ARGV marks its end.

     FIRST is an extra string put at the start of the arguments, or
     ‘NULL’ for no such extra.  This is a convenient way to pass the
     program name after advancing ARGV to strip option arguments.  Eg.

          {
            char *progname = argv[0];
            for (argv++; argv[0] != NULL && argv[0][0] == '-'; argv++)
              {
                /* munch option ... */
              }
            /* remaining args for scheme level use */
            scm_set_program_arguments (-1, argv, progname);
          }

     This sort of thing is often done at startup under ‘scm_boot_guile’
     with options handled at the C level removed.  The given strings are
     all copied, so the C data is not accessed again once
     ‘scm_set_program_arguments’ returns.

 -- Scheme Procedure: getenv name
 -- C Function: scm_getenv (name)
     Looks up the string NAME in the current environment.  The return
     value is ‘#f’ unless a string of the form ‘NAME=VALUE’ is found, in
     which case the string ‘VALUE’ is returned.

 -- Scheme Procedure: setenv name value
     Modifies the environment of the current process, which is also the
     default environment inherited by child processes.

     If VALUE is ‘#f’, then NAME is removed from the environment.
     Otherwise, the string NAME=VALUE is added to the environment,
     replacing any existing string with name matching NAME.

     The return value is unspecified.

 -- Scheme Procedure: unsetenv name
     Remove variable NAME from the environment.  The name can not
     contain a ‘=’ character.

 -- Scheme Procedure: environ [env]
 -- C Function: scm_environ (env)
     If ENV is omitted, return the current environment (in the Unix
     sense) as a list of strings.  Otherwise set the current
     environment, which is also the default environment for child
     processes, to the supplied list of strings.  Each member of ENV
     should be of the form NAME=VALUE and values of NAME should not be
     duplicated.  If ENV is supplied then the return value is
     unspecified.

 -- Scheme Procedure: putenv str
 -- C Function: scm_putenv (str)
     Modifies the environment of the current process, which is also the
     default environment inherited by child processes.

     If STR is of the form ‘NAME=VALUE’ then it will be written directly
     into the environment, replacing any existing environment string
     with name matching ‘NAME’.  If STR does not contain an equal sign,
     then any existing string with name matching STR will be removed.

     The return value is unspecified.

7.2.7 Processes
---------------

 -- Scheme Procedure: chdir str
 -- C Function: scm_chdir (str)
     Change the current working directory to STR.  The return value is
     unspecified.

 -- Scheme Procedure: getcwd
 -- C Function: scm_getcwd ()
     Return the name of the current working directory.

 -- Scheme Procedure: umask [mode]
 -- C Function: scm_umask (mode)
     If MODE is omitted, returns a decimal number representing the
     current file creation mask.  Otherwise the file creation mask is
     set to MODE and the previous value is returned.  *Note Assigning
     File Permissions: (libc)Setting Permissions, for more on how to use
     umasks.

     E.g., ‘(umask #o022)’ sets the mask to octal 22/decimal 18.

 -- Scheme Procedure: chroot path
 -- C Function: scm_chroot (path)
     Change the root directory to that specified in PATH.  This
     directory will be used for path names beginning with ‘/’.  The root
     directory is inherited by all children of the current process.
     Only the superuser may change the root directory.

 -- Scheme Procedure: getpid
 -- C Function: scm_getpid ()
     Return an integer representing the current process ID.

 -- Scheme Procedure: getgroups
 -- C Function: scm_getgroups ()
     Return a vector of integers representing the current supplementary
     group IDs.

 -- Scheme Procedure: getppid
 -- C Function: scm_getppid ()
     Return an integer representing the process ID of the parent
     process.

 -- Scheme Procedure: getuid
 -- C Function: scm_getuid ()
     Return an integer representing the current real user ID.

 -- Scheme Procedure: getgid
 -- C Function: scm_getgid ()
     Return an integer representing the current real group ID.

 -- Scheme Procedure: geteuid
 -- C Function: scm_geteuid ()
     Return an integer representing the current effective user ID. If
     the system does not support effective IDs, then the real ID is
     returned.  ‘(provided? 'EIDs)’ reports whether the system supports
     effective IDs.

 -- Scheme Procedure: getegid
 -- C Function: scm_getegid ()
     Return an integer representing the current effective group ID. If
     the system does not support effective IDs, then the real ID is
     returned.  ‘(provided? 'EIDs)’ reports whether the system supports
     effective IDs.

 -- Scheme Procedure: setgroups vec
 -- C Function: scm_setgroups (vec)
     Set the current set of supplementary group IDs to the integers in
     the given vector VEC.  The return value is unspecified.

     Generally only the superuser can set the process group IDs (*note
     Setting the Group IDs: (libc)Setting Groups.).

 -- Scheme Procedure: setuid id
 -- C Function: scm_setuid (id)
     Sets both the real and effective user IDs to the integer ID,
     provided the process has appropriate privileges.  The return value
     is unspecified.

 -- Scheme Procedure: setgid id
 -- C Function: scm_setgid (id)
     Sets both the real and effective group IDs to the integer ID,
     provided the process has appropriate privileges.  The return value
     is unspecified.

 -- Scheme Procedure: seteuid id
 -- C Function: scm_seteuid (id)
     Sets the effective user ID to the integer ID, provided the process
     has appropriate privileges.  If effective IDs are not supported,
     the real ID is set instead—‘(provided? 'EIDs)’ reports whether the
     system supports effective IDs.  The return value is unspecified.

 -- Scheme Procedure: setegid id
 -- C Function: scm_setegid (id)
     Sets the effective group ID to the integer ID, provided the process
     has appropriate privileges.  If effective IDs are not supported,
     the real ID is set instead—‘(provided? 'EIDs)’ reports whether the
     system supports effective IDs.  The return value is unspecified.

 -- Scheme Procedure: getpgrp
 -- C Function: scm_getpgrp ()
     Return an integer representing the current process group ID. This
     is the POSIX definition, not BSD.

 -- Scheme Procedure: setpgid pid pgid
 -- C Function: scm_setpgid (pid, pgid)
     Move the process PID into the process group PGID.  PID or PGID must
     be integers: they can be zero to indicate the ID of the current
     process.  Fails on systems that do not support job control.  The
     return value is unspecified.

 -- Scheme Procedure: setsid
 -- C Function: scm_setsid ()
     Creates a new session.  The current process becomes the session
     leader and is put in a new process group.  The process will be
     detached from its controlling terminal if it has one.  The return
     value is an integer representing the new process group ID.

 -- Scheme Procedure: getsid pid
 -- C Function: scm_getsid (pid)
     Returns the session ID of process PID.  (The session ID of a
     process is the process group ID of its session leader.)

 -- Scheme Procedure: waitpid pid [options]
 -- C Function: scm_waitpid (pid, options)
     This procedure collects status information from a child process
     which has terminated or (optionally) stopped.  Normally it will
     suspend the calling process until this can be done.  If more than
     one child process is eligible then one will be chosen by the
     operating system.

     The value of PID determines the behaviour:

     PID greater than 0
          Request status information from the specified child process.
     PID equal to -1 or ‘WAIT_ANY’
          Request status information for any child process.
     PID equal to 0 or ‘WAIT_MYPGRP’
          Request status information for any child process in the
          current process group.
     PID less than -1
          Request status information for any child process whose process
          group ID is −PID.

     The OPTIONS argument, if supplied, should be the bitwise OR of the
     values of zero or more of the following variables:

      -- Variable: WNOHANG
          Return immediately even if there are no child processes to be
          collected.

      -- Variable: WUNTRACED
          Report status information for stopped processes as well as
          terminated processes.

     The return value is a pair containing:

       1. The process ID of the child process, or 0 if ‘WNOHANG’ was
          specified and no process was collected.
       2. The integer status value.

   The following three functions can be used to decode the process
status code returned by ‘waitpid’.

 -- Scheme Procedure: status:exit-val status
 -- C Function: scm_status_exit_val (status)
     Return the exit status value, as would be set if a process ended
     normally through a call to ‘exit’ or ‘_exit’, if any, otherwise
     ‘#f’.

 -- Scheme Procedure: status:term-sig status
 -- C Function: scm_status_term_sig (status)
     Return the signal number which terminated the process, if any,
     otherwise ‘#f’.

 -- Scheme Procedure: status:stop-sig status
 -- C Function: scm_status_stop_sig (status)
     Return the signal number which stopped the process, if any,
     otherwise ‘#f’.

 -- Scheme Procedure: system [cmd]
 -- C Function: scm_system (cmd)
     Execute CMD using the operating system’s “command processor”.
     Under Unix this is usually the default shell ‘sh’.  The value
     returned is CMD’s exit status as returned by ‘waitpid’, which can
     be interpreted using the functions above.

     If ‘system’ is called without arguments, return a boolean
     indicating whether the command processor is available.

 -- Scheme Procedure: system* arg1 arg2 …
 -- C Function: scm_system_star (args)
     Execute the command indicated by ARG1 ARG2 ....  The first element
     must be a string indicating the command to be executed, and the
     remaining items must be strings representing each of the arguments
     to that command.

     This function returns the exit status of the command as provided by
     ‘waitpid’.  This value can be handled with ‘status:exit-val’ and
     the related functions.

     ‘system*’ is similar to ‘system’, but accepts only one string
     per-argument, and performs no shell interpretation.  The command is
     executed using fork and execlp.  Accordingly this function may be
     safer than ‘system’ in situations where shell interpretation is not
     required.

     Example: (system* "echo" "foo" "bar")

 -- Scheme Procedure: quit [status]
 -- Scheme Procedure: exit [status]
     Terminate the current process with proper unwinding of the Scheme
     stack.  The exit status zero if STATUS is not supplied.  If STATUS
     is supplied, and it is an integer, that integer is used as the exit
     status.  If STATUS is ‘#t’ or ‘#f’, the exit status is 0 or 1,
     respectively.

     The procedure ‘exit’ is an alias of ‘quit’.  They have the same
     functionality.

 -- Scheme Procedure: primitive-exit [status]
 -- Scheme Procedure: primitive-_exit [status]
 -- C Function: scm_primitive_exit (status)
 -- C Function: scm_primitive__exit (status)
     Terminate the current process without unwinding the Scheme stack.
     The exit status is STATUS if supplied, otherwise zero.

     ‘primitive-exit’ uses the C ‘exit’ function and hence runs usual C
     level cleanups (flush output streams, call ‘atexit’ functions, etc,
     see *note (libc)Normal Termination::)).

     ‘primitive-_exit’ is the ‘_exit’ system call (*note
     (libc)Termination Internals::).  This terminates the program
     immediately, with neither Scheme-level nor C-level cleanups.

     The typical use for ‘primitive-_exit’ is from a child process
     created with ‘primitive-fork’.  For example in a Gdk program the
     child process inherits the X server connection and a C-level
     ‘atexit’ cleanup which will close that connection.  But closing in
     the child would upset the protocol in the parent, so
     ‘primitive-_exit’ should be used to exit without that.

 -- Scheme Procedure: execl filename arg …
 -- C Function: scm_execl (filename, args)
     Executes the file named by FILENAME as a new process image.  The
     remaining arguments are supplied to the process; from a C program
     they are accessible as the ‘argv’ argument to ‘main’.
     Conventionally the first ARG is the same as FILENAME.  All
     arguments must be strings.

     If ARG is missing, FILENAME is executed with a null argument list,
     which may have system-dependent side-effects.

     This procedure is currently implemented using the ‘execv’ system
     call, but we call it ‘execl’ because of its Scheme calling
     interface.

 -- Scheme Procedure: execlp filename arg …
 -- C Function: scm_execlp (filename, args)
     Similar to ‘execl’, however if FILENAME does not contain a slash
     then the file to execute will be located by searching the
     directories listed in the ‘PATH’ environment variable.

     This procedure is currently implemented using the ‘execvp’ system
     call, but we call it ‘execlp’ because of its Scheme calling
     interface.

 -- Scheme Procedure: execle filename env arg …
 -- C Function: scm_execle (filename, env, args)
     Similar to ‘execl’, but the environment of the new process is
     specified by ENV, which must be a list of strings as returned by
     the ‘environ’ procedure.

     This procedure is currently implemented using the ‘execve’ system
     call, but we call it ‘execle’ because of its Scheme calling
     interface.

 -- Scheme Procedure: primitive-fork
 -- C Function: scm_fork ()
     Creates a new “child” process by duplicating the current “parent”
     process.  In the child the return value is 0.  In the parent the
     return value is the integer process ID of the child.

     Note that it is unsafe to fork a process that has multiple threads
     running, as only the thread that calls ‘primitive-fork’ will
     persist in the child.  Any resources that other threads held, such
     as locked mutexes or open file descriptors, are lost.  Indeed,
     POSIX specifies that only async-signal-safe procedures are safe to
     call after a multithreaded fork, which is a very limited set.
     Guile issues a warning if it detects a fork from a multi-threaded
     program.

     If you are going to ‘exec’ soon after forking, the procedures in
     ‘(ice-9 popen)’ may be useful to you, as they fork and exec within
     an async-signal-safe function carefully written to ensure robust
     program behavior, even in the presence of threads.  *Note Pipes::,
     for more.

     This procedure has been renamed from ‘fork’ to avoid a naming
     conflict with the scsh fork.

 -- Scheme Procedure: nice incr
 -- C Function: scm_nice (incr)
     Increment the priority of the current process by INCR.  A higher
     priority value means that the process runs less often.  The return
     value is unspecified.

 -- Scheme Procedure: setpriority which who prio
 -- C Function: scm_setpriority (which, who, prio)
     Set the scheduling priority of the process, process group or user,
     as indicated by WHICH and WHO.  WHICH is one of the variables
     ‘PRIO_PROCESS’, ‘PRIO_PGRP’ or ‘PRIO_USER’, and WHO is interpreted
     relative to WHICH (a process identifier for ‘PRIO_PROCESS’, process
     group identifier for ‘PRIO_PGRP’, and a user identifier for
     ‘PRIO_USER’.  A zero value of WHO denotes the current process,
     process group, or user.  PRIO is a value in the range [−20,20].
     The default priority is 0; lower priorities (in numerical terms)
     cause more favorable scheduling.  Sets the priority of all of the
     specified processes.  Only the super-user may lower priorities.
     The return value is not specified.

 -- Scheme Procedure: getpriority which who
 -- C Function: scm_getpriority (which, who)
     Return the scheduling priority of the process, process group or
     user, as indicated by WHICH and WHO.  WHICH is one of the variables
     ‘PRIO_PROCESS’, ‘PRIO_PGRP’ or ‘PRIO_USER’, and WHO should be
     interpreted depending on WHICH (a process identifier for
     ‘PRIO_PROCESS’, process group identifier for ‘PRIO_PGRP’, and a
     user identifier for ‘PRIO_USER’).  A zero value of WHO denotes the
     current process, process group, or user.  Return the highest
     priority (lowest numerical value) of any of the specified
     processes.

 -- Scheme Procedure: getaffinity pid
 -- C Function: scm_getaffinity (pid)
     Return a bitvector representing the CPU affinity mask for process
     PID.  Each CPU the process has affinity with has its corresponding
     bit set in the returned bitvector.  The number of bits set is a
     good estimate of how many CPUs Guile can use without stepping on
     other processes’ toes.

     Currently this procedure is only defined on GNU variants (*note
     ‘sched_getaffinity’: (libc)CPU Affinity.).

 -- Scheme Procedure: setaffinity pid mask
 -- C Function: scm_setaffinity (pid, mask)
     Install the CPU affinity mask MASK, a bitvector, for the process or
     thread with ID PID.  The return value is unspecified.

     Currently this procedure is only defined on GNU variants (*note
     ‘sched_setaffinity’: (libc)CPU Affinity.).

 -- Scheme Procedure: total-processor-count
 -- C Function: scm_total_processor_count ()
     Return the total number of processors of the machine, which is
     guaranteed to be at least 1.  A “processor” here is a thread
     execution unit, which can be either:

        • an execution core in a (possibly multi-core) chip, in a
          (possibly multi- chip) module, in a single computer, or
        • a thread execution unit inside a core in the case of
          "hyper-threaded" CPUs.

     Which of the two definitions is used, is unspecified.

 -- Scheme Procedure: current-processor-count
 -- C Function: scm_current_processor_count ()
     Like ‘total-processor-count’, but return the number of processors
     available to the current process.  See ‘setaffinity’ and
     ‘getaffinity’ for more information.

7.2.8 Signals
-------------

The following procedures raise, handle and wait for signals.

   Scheme code signal handlers are run via a system async (*note System
asyncs::), so they’re called in the handler’s thread at the next safe
opportunity.  Generally this is after any currently executing primitive
procedure finishes (which could be a long time for primitives that wait
for an external event).

 -- Scheme Procedure: kill pid sig
 -- C Function: scm_kill (pid, sig)
     Sends a signal to the specified process or group of processes.

     PID specifies the processes to which the signal is sent:

     PID greater than 0
          The process whose identifier is PID.
     PID equal to 0
          All processes in the current process group.
     PID less than -1
          The process group whose identifier is -PID
     PID equal to -1
          If the process is privileged, all processes except for some
          special system processes.  Otherwise, all processes with the
          current effective user ID.

     SIG should be specified using a variable corresponding to the Unix
     symbolic name, e.g.,

      -- Variable: SIGHUP
          Hang-up signal.

      -- Variable: SIGINT
          Interrupt signal.

     A full list of signals on the GNU system may be found in *note
     (libc)Standard Signals::.

 -- Scheme Procedure: raise sig
 -- C Function: scm_raise (sig)
     Sends a specified signal SIG to the current process, where SIG is
     as described for the ‘kill’ procedure.

 -- Scheme Procedure: sigaction signum [handler [flags [thread]]]
 -- C Function: scm_sigaction (signum, handler, flags)
 -- C Function: scm_sigaction_for_thread (signum, handler, flags,
          thread)
     Install or report the signal handler for a specified signal.

     SIGNUM is the signal number, which can be specified using the value
     of variables such as ‘SIGINT’.

     If HANDLER is omitted, ‘sigaction’ returns a pair: the CAR is the
     current signal hander, which will be either an integer with the
     value ‘SIG_DFL’ (default action) or ‘SIG_IGN’ (ignore), or the
     Scheme procedure which handles the signal, or ‘#f’ if a non-Scheme
     procedure handles the signal.  The CDR contains the current
     ‘sigaction’ flags for the handler.

     If HANDLER is provided, it is installed as the new handler for
     SIGNUM.  HANDLER can be a Scheme procedure taking one argument, or
     the value of ‘SIG_DFL’ (default action) or ‘SIG_IGN’ (ignore), or
     ‘#f’ to restore whatever signal handler was installed before
     ‘sigaction’ was first used.  When a scheme procedure has been
     specified, that procedure will run in the given THREAD.  When no
     thread has been given, the thread that made this call to
     ‘sigaction’ is used.

     FLAGS is a ‘logior’ (*note Bitwise Operations::) of the following
     (where provided by the system), or ‘0’ for none.

      -- Variable: SA_NOCLDSTOP
          By default, ‘SIGCHLD’ is signalled when a child process stops
          (ie. receives ‘SIGSTOP’), and when a child process terminates.
          With the ‘SA_NOCLDSTOP’ flag, ‘SIGCHLD’ is only signalled for
          termination, not stopping.

          ‘SA_NOCLDSTOP’ has no effect on signals other than ‘SIGCHLD’.

      -- Variable: SA_RESTART
          If a signal occurs while in a system call, deliver the signal
          then restart the system call (as opposed to returning an
          ‘EINTR’ error from that call).

     The return value is a pair with information about the old handler
     as described above.

     This interface does not provide access to the “signal blocking”
     facility.  Maybe this is not needed, since the thread support may
     provide solutions to the problem of consistent access to data
     structures.

 -- Scheme Procedure: restore-signals
 -- C Function: scm_restore_signals ()
     Return all signal handlers to the values they had before any call
     to ‘sigaction’ was made.  The return value is unspecified.

 -- Scheme Procedure: alarm i
 -- C Function: scm_alarm (i)
     Set a timer to raise a ‘SIGALRM’ signal after the specified number
     of seconds (an integer).  It’s advisable to install a signal
     handler for ‘SIGALRM’ beforehand, since the default action is to
     terminate the process.

     The return value indicates the time remaining for the previous
     alarm, if any.  The new value replaces the previous alarm.  If
     there was no previous alarm, the return value is zero.

 -- Scheme Procedure: pause
 -- C Function: scm_pause ()
     Pause the current process (thread?)  until a signal arrives whose
     action is to either terminate the current process or invoke a
     handler procedure.  The return value is unspecified.

 -- Scheme Procedure: sleep secs
 -- Scheme Procedure: usleep usecs
 -- C Function: scm_sleep (secs)
 -- C Function: scm_usleep (usecs)
     Wait the given period SECS seconds or USECS microseconds (both
     integers).  If a signal arrives the wait stops and the return value
     is the time remaining, in seconds or microseconds respectively.  If
     the period elapses with no signal the return is zero.

     On most systems the process scheduler is not microsecond accurate
     and the actual period slept by ‘usleep’ might be rounded to a
     system clock tick boundary, which might be 10 milliseconds for
     instance.

     See ‘scm_std_sleep’ and ‘scm_std_usleep’ for equivalents at the C
     level (*note Blocking::).

 -- Scheme Procedure: getitimer which_timer
 -- Scheme Procedure: setitimer which_timer interval_seconds
          interval_microseconds periodic_seconds periodic_microseconds
 -- C Function: scm_getitimer (which_timer)
 -- C Function: scm_setitimer (which_timer, interval_seconds,
          interval_microseconds, periodic_seconds,
          periodic_microseconds)
     Get or set the periods programmed in certain system timers.  These
     timers have a current interval value which counts down and on
     reaching zero raises a signal.  An optional periodic value can be
     set to restart from there each time, for periodic operation.
     WHICH_TIMER is one of the following values

      -- Variable: ITIMER_REAL
          A real-time timer, counting down elapsed real time.  At zero
          it raises ‘SIGALRM’.  This is like ‘alarm’ above, but with a
          higher resolution period.

      -- Variable: ITIMER_VIRTUAL
          A virtual-time timer, counting down while the current process
          is actually using CPU. At zero it raises ‘SIGVTALRM’.

      -- Variable: ITIMER_PROF
          A profiling timer, counting down while the process is running
          (like ‘ITIMER_VIRTUAL’) and also while system calls are
          running on the process’s behalf.  At zero it raises a
          ‘SIGPROF’.

          This timer is intended for profiling where a program is
          spending its time (by looking where it is when the timer goes
          off).

     ‘getitimer’ returns the current timer value and its programmed
     restart value, as a list containing two pairs.  Each pair is a time
     in seconds and microseconds: ‘((INTERVAL_SECS . INTERVAL_USECS)
     (PERIODIC_SECS . PERIODIC_USECS))’.

     ‘setitimer’ sets the timer values similarly, in seconds and
     microseconds (which must be integers).  The periodic value can be
     zero to have the timer run down just once.  The return value is the
     timer’s previous setting, in the same form as ‘getitimer’ returns.

          (setitimer ITIMER_REAL
                     5 500000     ;; first SIGALRM in 5.5 seconds time
                     2 0)         ;; then repeat every 2 seconds

     Although the timers are programmed in microseconds, the actual
     accuracy might not be that high.

7.2.9 Terminals and Ptys
------------------------

 -- Scheme Procedure: isatty? port
 -- C Function: scm_isatty_p (port)
     Return ‘#t’ if PORT is using a serial non–file device, otherwise
     ‘#f’.

 -- Scheme Procedure: ttyname port
 -- C Function: scm_ttyname (port)
     Return a string with the name of the serial terminal device
     underlying PORT.

 -- Scheme Procedure: ctermid
 -- C Function: scm_ctermid ()
     Return a string containing the file name of the controlling
     terminal for the current process.

 -- Scheme Procedure: tcgetpgrp port
 -- C Function: scm_tcgetpgrp (port)
     Return the process group ID of the foreground process group
     associated with the terminal open on the file descriptor underlying
     PORT.

     If there is no foreground process group, the return value is a
     number greater than 1 that does not match the process group ID of
     any existing process group.  This can happen if all of the
     processes in the job that was formerly the foreground job have
     terminated, and no other job has yet been moved into the
     foreground.

 -- Scheme Procedure: tcsetpgrp port pgid
 -- C Function: scm_tcsetpgrp (port, pgid)
     Set the foreground process group ID for the terminal used by the
     file descriptor underlying PORT to the integer PGID.  The calling
     process must be a member of the same session as PGID and must have
     the same controlling terminal.  The return value is unspecified.

7.2.10 Pipes
------------

The following procedures are similar to the ‘popen’ and ‘pclose’ system
routines.  The code is in a separate “popen” module(1):

     (use-modules (ice-9 popen))

 -- Scheme Procedure: open-pipe command mode
 -- Scheme Procedure: open-pipe* mode prog [args...]
     Execute a command in a subprocess, with a pipe to it or from it, or
     with pipes in both directions.

     ‘open-pipe’ runs the shell COMMAND using ‘/bin/sh -c’.
     ‘open-pipe*’ executes PROG directly, with the optional ARGS
     arguments (all strings).

     MODE should be one of the following values.  ‘OPEN_READ’ is an
     input pipe, ie. to read from the subprocess.  ‘OPEN_WRITE’ is an
     output pipe, ie. to write to it.

      -- Variable: OPEN_READ
      -- Variable: OPEN_WRITE
      -- Variable: OPEN_BOTH

     For an input pipe, the child’s standard output is the pipe and
     standard input is inherited from ‘current-input-port’.  For an
     output pipe, the child’s standard input is the pipe and standard
     output is inherited from ‘current-output-port’.  In all cases cases
     the child’s standard error is inherited from ‘current-error-port’
     (*note Default Ports::).

     If those ‘current-X-ports’ are not files of some kind, and hence
     don’t have file descriptors for the child, then ‘/dev/null’ is used
     instead.

     Care should be taken with ‘OPEN_BOTH’, a deadlock will occur if
     both parent and child are writing, and waiting until the write
     completes before doing any reading.  Each direction has ‘PIPE_BUF’
     bytes of buffering (*note Ports and File Descriptors::), which will
     be enough for small writes, but not for say putting a big file
     through a filter.

 -- Scheme Procedure: open-input-pipe command
     Equivalent to ‘open-pipe’ with mode ‘OPEN_READ’.

          (let* ((port (open-input-pipe "date --utc"))
                 (str  (read-line port)))
            (close-pipe port)
            str)
          ⇒ "Mon Mar 11 20:10:44 UTC 2002"

 -- Scheme Procedure: open-output-pipe command
     Equivalent to ‘open-pipe’ with mode ‘OPEN_WRITE’.

          (let ((port (open-output-pipe "lpr")))
            (display "Something for the line printer.\n" port)
            (if (not (eqv? 0 (status:exit-val (close-pipe port))))
                (error "Cannot print")))

 -- Scheme Procedure: open-input-output-pipe command
     Equivalent to ‘open-pipe’ with mode ‘OPEN_BOTH’.

 -- Scheme Procedure: close-pipe port
     Close a pipe created by ‘open-pipe’, wait for the process to
     terminate, and return the wait status code.  The status is as per
     ‘waitpid’ and can be decoded with ‘status:exit-val’ etc (*note
     Processes::)


   ‘waitpid WAIT_ANY’ should not be used when pipes are open, since it
can reap a pipe’s child process, causing an error from a subsequent
‘close-pipe’.

   ‘close-port’ (*note Closing::) can close a pipe, but it doesn’t reap
the child process.

   The garbage collector will close a pipe no longer in use, and reap
the child process with ‘waitpid’.  If the child hasn’t yet terminated
the garbage collector doesn’t block, but instead checks again in the
next GC.

   Many systems have per-user and system-wide limits on the number of
processes, and a system-wide limit on the number of pipes, so pipes
should be closed explicitly when no longer needed, rather than letting
the garbage collector pick them up at some later time.

   ---------- Footnotes ----------

   (1) This module is only available on systems where the ‘fork’ feature
is provided (*note Common Feature Symbols::).

7.2.11 Networking
-----------------

7.2.11.1 Network Address Conversion
...................................

This section describes procedures which convert internet addresses
between numeric and string formats.

IPv4 Address Conversion
.......................

An IPv4 Internet address is a 4-byte value, represented in Guile as an
integer in host byte order, so that say “0.0.0.1” is 1, or “1.0.0.0” is
16777216.

   Some underlying C functions use network byte order for addresses,
Guile converts as necessary so that at the Scheme level its host byte
order everywhere.

 -- Variable: INADDR_ANY
     For a server, this can be used with ‘bind’ (*note Network Sockets
     and Communication::) to allow connections from any interface on the
     machine.

 -- Variable: INADDR_BROADCAST
     The broadcast address on the local network.

 -- Variable: INADDR_LOOPBACK
     The address of the local host using the loopback device, ie.
     ‘127.0.0.1’.

 -- Scheme Procedure: inet-aton address
 -- C Function: scm_inet_aton (address)
     This function is deprecated in favor of ‘inet-pton’.

     Convert an IPv4 Internet address from printable string (dotted
     decimal notation) to an integer.  E.g.,

          (inet-aton "127.0.0.1") ⇒ 2130706433

 -- Scheme Procedure: inet-ntoa inetid
 -- C Function: scm_inet_ntoa (inetid)
     This function is deprecated in favor of ‘inet-ntop’.

     Convert an IPv4 Internet address to a printable (dotted decimal
     notation) string.  E.g.,

          (inet-ntoa 2130706433) ⇒ "127.0.0.1"

 -- Scheme Procedure: inet-netof address
 -- C Function: scm_inet_netof (address)
     Return the network number part of the given IPv4 Internet address.
     E.g.,

          (inet-netof 2130706433) ⇒ 127

 -- Scheme Procedure: inet-lnaof address
 -- C Function: scm_lnaof (address)
     Return the local-address-with-network part of the given IPv4
     Internet address, using the obsolete class A/B/C system.  E.g.,

          (inet-lnaof 2130706433) ⇒ 1

 -- Scheme Procedure: inet-makeaddr net lna
 -- C Function: scm_inet_makeaddr (net, lna)
     Make an IPv4 Internet address by combining the network number NET
     with the local-address-within-network number LNA.  E.g.,

          (inet-makeaddr 127 1) ⇒ 2130706433

IPv6 Address Conversion
.......................

An IPv6 Internet address is a 16-byte value, represented in Guile as an
integer in host byte order, so that say “::1” is 1.

 -- Scheme Procedure: inet-ntop family address
 -- C Function: scm_inet_ntop (family, address)
     Convert a network address from an integer to a printable string.
     FAMILY can be ‘AF_INET’ or ‘AF_INET6’.  E.g.,

          (inet-ntop AF_INET 2130706433) ⇒ "127.0.0.1"
          (inet-ntop AF_INET6 (- (expt 2 128) 1))
            ⇒ "ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff"

 -- Scheme Procedure: inet-pton family address
 -- C Function: scm_inet_pton (family, address)
     Convert a string containing a printable network address to an
     integer address.  FAMILY can be ‘AF_INET’ or ‘AF_INET6’.  E.g.,

          (inet-pton AF_INET "127.0.0.1") ⇒ 2130706433
          (inet-pton AF_INET6 "::1") ⇒ 1

7.2.11.2 Network Databases
..........................

This section describes procedures which query various network databases.
Care should be taken when using the database routines since they are not
reentrant.

‘getaddrinfo’
.............

The ‘getaddrinfo’ procedure maps host and service names to socket
addresses and associated information in a protocol-independent way.

 -- Scheme Procedure: getaddrinfo name service [hint_flags [hint_family
          [hint_socktype [hint_protocol]]]]
 -- C Function: scm_getaddrinfo (name, service, hint_flags, hint_family,
          hint_socktype, hint_protocol)
     Return a list of ‘addrinfo’ structures containing a socket address
     and associated information for host NAME and/or SERVICE to be used
     in creating a socket with which to address the specified service.

          (let* ((ai (car (getaddrinfo "www.gnu.org" "http")))
                 (s  (socket (addrinfo:fam ai) (addrinfo:socktype ai)
                             (addrinfo:protocol ai))))
            (connect s (addrinfo:addr ai))
            s)

     When SERVICE is omitted or is ‘#f’, return network-level addresses
     for NAME.  When NAME is ‘#f’ SERVICE must be provided and service
     locations local to the caller are returned.

     Additional hints can be provided.  When specified, HINT_FLAGS
     should be a bitwise-or of zero or more constants among the
     following:

     ‘AI_PASSIVE’
          Socket address is intended for ‘bind’.

     ‘AI_CANONNAME’
          Request for canonical host name, available via
          ‘addrinfo:canonname’.  This makes sense mainly when DNS
          lookups are involved.

     ‘AI_NUMERICHOST’
          Specifies that NAME is a numeric host address string (e.g.,
          ‘"127.0.0.1"’), meaning that name resolution will not be used.

     ‘AI_NUMERICSERV’
          Likewise, specifies that SERVICE is a numeric port string
          (e.g., ‘"80"’).

     ‘AI_ADDRCONFIG’
          Return only addresses configured on the local system It is
          highly recommended to provide this flag when the returned
          socket addresses are to be used to make connections;
          otherwise, some of the returned addresses could be unreachable
          or use a protocol that is not supported.

     ‘AI_V4MAPPED’
          When looking up IPv6 addresses, return mapped IPv4 addresses
          if there is no IPv6 address available at all.

     ‘AI_ALL’
          If this flag is set along with ‘AI_V4MAPPED’ when looking up
          IPv6 addresses, return all IPv6 addresses as well as all IPv4
          addresses, the latter mapped to IPv6 format.

     When given, HINT_FAMILY should specify the requested address
     family, e.g., ‘AF_INET6’.  Similarly, HINT_SOCKTYPE should specify
     the requested socket type (e.g., ‘SOCK_DGRAM’), and HINT_PROTOCOL
     should specify the requested protocol (its value is interpreted as
     in calls to ‘socket’).

     On error, an exception with key ‘getaddrinfo-error’ is thrown, with
     an error code (an integer) as its argument:

          (catch 'getaddrinfo-error
            (lambda ()
              (getaddrinfo "www.gnu.org" "gopher"))
            (lambda (key errcode)
              (cond ((= errcode EAI_SERVICE)
          	   (display "doesn't know about Gopher!\n"))
          	  ((= errcode EAI_NONAME)
          	   (display "www.gnu.org not found\\n"))
          	  (else
          	   (format #t "something wrong: ~a\n"
          		   (gai-strerror errcode))))))

     Error codes are:

     ‘EAI_AGAIN’
          The name or service could not be resolved at this time.
          Future attempts may succeed.

     ‘EAI_BADFLAGS’
          HINT_FLAGS contains an invalid value.

     ‘EAI_FAIL’
          A non-recoverable error occurred when attempting to resolve
          the name.

     ‘EAI_FAMILY’
          HINT_FAMILY was not recognized.

     ‘EAI_NONAME’
          Either NAME does not resolve for the supplied parameters, or
          neither NAME nor SERVICE were supplied.

     ‘EAI_NODATA’
          This non-POSIX error code can be returned on some systems (GNU
          and Darwin, at least), for example when NAME is known but
          requests that were made turned out no data.  Error handling
          code should be prepared to handle it when it is defined.

     ‘EAI_SERVICE’
          SERVICE was not recognized for the specified socket type.

     ‘EAI_SOCKTYPE’
          HINT_SOCKTYPE was not recognized.

     ‘EAI_SYSTEM’
          A system error occurred.  In C, the error code can be found in
          ‘errno’; this value is not accessible from Scheme, but in
          practice it provides little information about the actual error
          cause.

     Users are encouraged to read the "POSIX specification
     (http://www.opengroup.org/onlinepubs/9699919799/functions/getaddrinfo.html)
     for more details.

   The following procedures take an ‘addrinfo’ object as returned by
‘getaddrinfo’:

 -- Scheme Procedure: addrinfo:flags ai
     Return flags for AI as a bitwise or of ‘AI_’ values (see above).

 -- Scheme Procedure: addrinfo:fam ai
     Return the address family of AI (a ‘AF_’ value).

 -- Scheme Procedure: addrinfo:socktype ai
     Return the socket type for AI (a ‘SOCK_’ value).

 -- Scheme Procedure: addrinfo:protocol ai
     Return the protocol of AI.

 -- Scheme Procedure: addrinfo:addr ai
     Return the socket address associated with AI as a ‘sockaddr’ object
     (*note Network Socket Address::).

 -- Scheme Procedure: addrinfo:canonname ai
     Return a string for the canonical name associated with AI if the
     ‘AI_CANONNAME’ flag was supplied.

The Host Database
.................

A "host object" is a structure that represents what is known about a
network host, and is the usual way of representing a system’s network
identity inside software.

   The following functions accept a host object and return a selected
component:

 -- Scheme Procedure: hostent:name host
     The “official” hostname for HOST.
 -- Scheme Procedure: hostent:aliases host
     A list of aliases for HOST.
 -- Scheme Procedure: hostent:addrtype host
     The host address type, one of the ‘AF’ constants, such as ‘AF_INET’
     or ‘AF_INET6’.
 -- Scheme Procedure: hostent:length host
     The length of each address for HOST, in bytes.
 -- Scheme Procedure: hostent:addr-list host
     The list of network addresses associated with HOST.  For ‘AF_INET’
     these are integer IPv4 address (*note Network Address
     Conversion::).

   The following procedures can be used to search the host database.
However, ‘getaddrinfo’ should be preferred over them since it’s more
generic and thread-safe.

 -- Scheme Procedure: gethost [host]
 -- Scheme Procedure: gethostbyname hostname
 -- Scheme Procedure: gethostbyaddr address
 -- C Function: scm_gethost (host)
     Look up a host by name or address, returning a host object.  The
     ‘gethost’ procedure will accept either a string name or an integer
     address; if given no arguments, it behaves like ‘gethostent’ (see
     below).  If a name or address is supplied but the address can not
     be found, an error will be thrown to one of the keys:
     ‘host-not-found’, ‘try-again’, ‘no-recovery’ or ‘no-data’,
     corresponding to the equivalent ‘h_error’ values.  Unusual
     conditions may result in errors thrown to the ‘system-error’ or
     ‘misc_error’ keys.

          (gethost "www.gnu.org")
          ⇒ #("www.gnu.org" () 2 4 (3353880842))

          (gethostbyname "www.emacs.org")
          ⇒ #("emacs.org" ("www.emacs.org") 2 4 (1073448978))

   The following procedures may be used to step through the host
database from beginning to end.

 -- Scheme Procedure: sethostent [stayopen]
     Initialize an internal stream from which host objects may be read.
     This procedure must be called before any calls to ‘gethostent’, and
     may also be called afterward to reset the host entry stream.  If
     STAYOPEN is supplied and is not ‘#f’, the database is not closed by
     subsequent ‘gethostbyname’ or ‘gethostbyaddr’ calls, possibly
     giving an efficiency gain.

 -- Scheme Procedure: gethostent
     Return the next host object from the host database, or ‘#f’ if
     there are no more hosts to be found (or an error has been
     encountered).  This procedure may not be used before ‘sethostent’
     has been called.

 -- Scheme Procedure: endhostent
     Close the stream used by ‘gethostent’.  The return value is
     unspecified.

 -- Scheme Procedure: sethost [stayopen]
 -- C Function: scm_sethost (stayopen)
     If STAYOPEN is omitted, this is equivalent to ‘endhostent’.
     Otherwise it is equivalent to ‘sethostent stayopen’.

The Network Database
....................

The following functions accept an object representing a network and
return a selected component:

 -- Scheme Procedure: netent:name net
     The “official” network name.
 -- Scheme Procedure: netent:aliases net
     A list of aliases for the network.
 -- Scheme Procedure: netent:addrtype net
     The type of the network number.  Currently, this returns only
     ‘AF_INET’.
 -- Scheme Procedure: netent:net net
     The network number.

   The following procedures are used to search the network database:

 -- Scheme Procedure: getnet [net]
 -- Scheme Procedure: getnetbyname net-name
 -- Scheme Procedure: getnetbyaddr net-number
 -- C Function: scm_getnet (net)
     Look up a network by name or net number in the network database.
     The NET-NAME argument must be a string, and the NET-NUMBER argument
     must be an integer.  ‘getnet’ will accept either type of argument,
     behaving like ‘getnetent’ (see below) if no arguments are given.

   The following procedures may be used to step through the network
database from beginning to end.

 -- Scheme Procedure: setnetent [stayopen]
     Initialize an internal stream from which network objects may be
     read.  This procedure must be called before any calls to
     ‘getnetent’, and may also be called afterward to reset the net
     entry stream.  If STAYOPEN is supplied and is not ‘#f’, the
     database is not closed by subsequent ‘getnetbyname’ or
     ‘getnetbyaddr’ calls, possibly giving an efficiency gain.

 -- Scheme Procedure: getnetent
     Return the next entry from the network database.

 -- Scheme Procedure: endnetent
     Close the stream used by ‘getnetent’.  The return value is
     unspecified.

 -- Scheme Procedure: setnet [stayopen]
 -- C Function: scm_setnet (stayopen)
     If STAYOPEN is omitted, this is equivalent to ‘endnetent’.
     Otherwise it is equivalent to ‘setnetent stayopen’.

The Protocol Database
.....................

The following functions accept an object representing a protocol and
return a selected component:

 -- Scheme Procedure: protoent:name protocol
     The “official” protocol name.
 -- Scheme Procedure: protoent:aliases protocol
     A list of aliases for the protocol.
 -- Scheme Procedure: protoent:proto protocol
     The protocol number.

   The following procedures are used to search the protocol database:

 -- Scheme Procedure: getproto [protocol]
 -- Scheme Procedure: getprotobyname name
 -- Scheme Procedure: getprotobynumber number
 -- C Function: scm_getproto (protocol)
     Look up a network protocol by name or by number.  ‘getprotobyname’
     takes a string argument, and ‘getprotobynumber’ takes an integer
     argument.  ‘getproto’ will accept either type, behaving like
     ‘getprotoent’ (see below) if no arguments are supplied.

   The following procedures may be used to step through the protocol
database from beginning to end.

 -- Scheme Procedure: setprotoent [stayopen]
     Initialize an internal stream from which protocol objects may be
     read.  This procedure must be called before any calls to
     ‘getprotoent’, and may also be called afterward to reset the
     protocol entry stream.  If STAYOPEN is supplied and is not ‘#f’,
     the database is not closed by subsequent ‘getprotobyname’ or
     ‘getprotobynumber’ calls, possibly giving an efficiency gain.

 -- Scheme Procedure: getprotoent
     Return the next entry from the protocol database.

 -- Scheme Procedure: endprotoent
     Close the stream used by ‘getprotoent’.  The return value is
     unspecified.

 -- Scheme Procedure: setproto [stayopen]
 -- C Function: scm_setproto (stayopen)
     If STAYOPEN is omitted, this is equivalent to ‘endprotoent’.
     Otherwise it is equivalent to ‘setprotoent stayopen’.

The Service Database
....................

The following functions accept an object representing a service and
return a selected component:

 -- Scheme Procedure: servent:name serv
     The “official” name of the network service.
 -- Scheme Procedure: servent:aliases serv
     A list of aliases for the network service.
 -- Scheme Procedure: servent:port serv
     The Internet port used by the service.
 -- Scheme Procedure: servent:proto serv
     The protocol used by the service.  A service may be listed many
     times in the database under different protocol names.

   The following procedures are used to search the service database:

 -- Scheme Procedure: getserv [name [protocol]]
 -- Scheme Procedure: getservbyname name protocol
 -- Scheme Procedure: getservbyport port protocol
 -- C Function: scm_getserv (name, protocol)
     Look up a network service by name or by service number, and return
     a network service object.  The PROTOCOL argument specifies the name
     of the desired protocol; if the protocol found in the network
     service database does not match this name, a system error is
     signalled.

     The ‘getserv’ procedure will take either a service name or number
     as its first argument; if given no arguments, it behaves like
     ‘getservent’ (see below).

          (getserv "imap" "tcp")
          ⇒ #("imap2" ("imap") 143 "tcp")

          (getservbyport 88 "udp")
          ⇒ #("kerberos" ("kerberos5" "krb5") 88 "udp")

   The following procedures may be used to step through the service
database from beginning to end.

 -- Scheme Procedure: setservent [stayopen]
     Initialize an internal stream from which service objects may be
     read.  This procedure must be called before any calls to
     ‘getservent’, and may also be called afterward to reset the service
     entry stream.  If STAYOPEN is supplied and is not ‘#f’, the
     database is not closed by subsequent ‘getservbyname’ or
     ‘getservbyport’ calls, possibly giving an efficiency gain.

 -- Scheme Procedure: getservent
     Return the next entry from the services database.

 -- Scheme Procedure: endservent
     Close the stream used by ‘getservent’.  The return value is
     unspecified.

 -- Scheme Procedure: setserv [stayopen]
 -- C Function: scm_setserv (stayopen)
     If STAYOPEN is omitted, this is equivalent to ‘endservent’.
     Otherwise it is equivalent to ‘setservent stayopen’.

7.2.11.3 Network Socket Address
...............................

A "socket address" object identifies a socket endpoint for
communication.  In the case of ‘AF_INET’ for instance, the socket
address object comprises the host address (or interface on the host) and
a port number which specifies a particular open socket in a running
client or server process.  A socket address object can be created with,

 -- Scheme Procedure: make-socket-address AF_INET ipv4addr port
 -- Scheme Procedure: make-socket-address AF_INET6 ipv6addr port
          [flowinfo [scopeid]]
 -- Scheme Procedure: make-socket-address AF_UNIX path
 -- C Function: scm_make_socket_address (family, address, arglist)
     Return a new socket address object.  The first argument is the
     address family, one of the ‘AF’ constants, then the arguments vary
     according to the family.

     For ‘AF_INET’ the arguments are an IPv4 network address number
     (*note Network Address Conversion::), and a port number.

     For ‘AF_INET6’ the arguments are an IPv6 network address number and
     a port number.  Optional FLOWINFO and SCOPEID arguments may be
     given (both integers, default 0).

     For ‘AF_UNIX’ the argument is a filename (a string).

     The C function ‘scm_make_socket_address’ takes the FAMILY and
     ADDRESS arguments directly, then ARGLIST is a list of further
     arguments, being the port for IPv4, port and optional flowinfo and
     scopeid for IPv6, or the empty list ‘SCM_EOL’ for Unix domain.

The following functions access the fields of a socket address object,

 -- Scheme Procedure: sockaddr:fam sa
     Return the address family from socket address object SA.  This is
     one of the ‘AF’ constants (e.g. ‘AF_INET’).

 -- Scheme Procedure: sockaddr:path sa
     For an ‘AF_UNIX’ socket address object SA, return the filename.

 -- Scheme Procedure: sockaddr:addr sa
     For an ‘AF_INET’ or ‘AF_INET6’ socket address object SA, return the
     network address number.

 -- Scheme Procedure: sockaddr:port sa
     For an ‘AF_INET’ or ‘AF_INET6’ socket address object SA, return the
     port number.

 -- Scheme Procedure: sockaddr:flowinfo sa
     For an ‘AF_INET6’ socket address object SA, return the flowinfo
     value.

 -- Scheme Procedure: sockaddr:scopeid sa
     For an ‘AF_INET6’ socket address object SA, return the scope ID
     value.

   The functions below convert to and from the C ‘struct sockaddr’
(*note (libc)Address Formats::).  That structure is a generic type, an
application can cast to or from ‘struct sockaddr_in’, ‘struct
sockaddr_in6’ or ‘struct sockaddr_un’ according to the address family.

   In a ‘struct sockaddr’ taken or returned, the byte ordering in the
fields follows the C conventions (*note Byte Order Conversion:
(libc)Byte Order.).  This means network byte order for ‘AF_INET’ host
address (‘sin_addr.s_addr’) and port number (‘sin_port’), and ‘AF_INET6’
port number (‘sin6_port’).  But at the Scheme level these values are
taken or returned in host byte order, so the port is an ordinary
integer, and the host address likewise is an ordinary integer (as
described in *note Network Address Conversion::).

 -- C Function: struct sockaddr * scm_c_make_socket_address (SCM family,
          SCM address, SCM args, size_t *outsize)
     Return a newly-‘malloc’ed ‘struct sockaddr’ created from arguments
     like those taken by ‘scm_make_socket_address’ above.

     The size (in bytes) of the ‘struct sockaddr’ return is stored into
     ‘*OUTSIZE’.  An application must call ‘free’ to release the
     returned structure when no longer required.

 -- C Function: SCM scm_from_sockaddr (const struct sockaddr *address,
          unsigned address_size)
     Return a Scheme socket address object from the C ADDRESS structure.
     ADDRESS_SIZE is the size in bytes of ADDRESS.

 -- C Function: struct sockaddr * scm_to_sockaddr (SCM address, size_t
          *address_size)
     Return a newly-‘malloc’ed ‘struct sockaddr’ from a Scheme level
     socket address object.

     The size (in bytes) of the ‘struct sockaddr’ return is stored into
     ‘*OUTSIZE’.  An application must call ‘free’ to release the
     returned structure when no longer required.

7.2.11.4 Network Sockets and Communication
..........................................

Socket ports can be created using ‘socket’ and ‘socketpair’.  The ports
are initially unbuffered, to make reading and writing to the same port
more reliable.  A buffer can be added to the port using ‘setvbuf’; see
*note Ports and File Descriptors::.

   Most systems have limits on how many files and sockets can be open,
so it’s strongly recommended that socket ports be closed explicitly when
no longer required (*note Ports::).

   Some of the underlying C functions take values in network byte order,
but the convention in Guile is that at the Scheme level everything is
ordinary host byte order and conversions are made automatically where
necessary.

 -- Scheme Procedure: socket family style proto
 -- C Function: scm_socket (family, style, proto)
     Return a new socket port of the type specified by FAMILY, STYLE and
     PROTO.  All three parameters are integers.  The possible values for
     FAMILY are as follows, where supported by the system,

      -- Variable: PF_UNIX
      -- Variable: PF_INET
      -- Variable: PF_INET6

     The possible values for STYLE are as follows, again where supported
     by the system,

      -- Variable: SOCK_STREAM
      -- Variable: SOCK_DGRAM
      -- Variable: SOCK_RAW
      -- Variable: SOCK_RDM
      -- Variable: SOCK_SEQPACKET

     PROTO can be obtained from a protocol name using ‘getprotobyname’
     (*note Network Databases::).  A value of zero means the default
     protocol, which is usually right.

     A socket cannot by used for communication until it has been
     connected somewhere, usually with either ‘connect’ or ‘accept’
     below.

 -- Scheme Procedure: socketpair family style proto
 -- C Function: scm_socketpair (family, style, proto)
     Return a pair, the ‘car’ and ‘cdr’ of which are two unnamed socket
     ports connected to each other.  The connection is full-duplex, so
     data can be transferred in either direction between the two.

     FAMILY, STYLE and PROTO are as per ‘socket’ above.  But many
     systems only support socket pairs in the ‘PF_UNIX’ family.  Zero is
     likely to be the only meaningful value for PROTO.

 -- Scheme Procedure: getsockopt sock level optname
 -- Scheme Procedure: setsockopt sock level optname value
 -- C Function: scm_getsockopt (sock, level, optname)
 -- C Function: scm_setsockopt (sock, level, optname, value)
     Get or set an option on socket port SOCK.  ‘getsockopt’ returns the
     current value.  ‘setsockopt’ sets a value and the return is
     unspecified.

     LEVEL is an integer specifying a protocol layer, either
     ‘SOL_SOCKET’ for socket level options, or a protocol number from
     the ‘IPPROTO’ constants or ‘getprotoent’ (*note Network
     Databases::).

      -- Variable: SOL_SOCKET
      -- Variable: IPPROTO_IP
      -- Variable: IPPROTO_TCP
      -- Variable: IPPROTO_UDP

     OPTNAME is an integer specifying an option within the protocol
     layer.

     For ‘SOL_SOCKET’ level the following OPTNAMEs are defined (when
     provided by the system).  For their meaning see *note
     (libc)Socket-Level Options::, or ‘man 7 socket’.

      -- Variable: SO_DEBUG
      -- Variable: SO_REUSEADDR
      -- Variable: SO_STYLE
      -- Variable: SO_TYPE
      -- Variable: SO_ERROR
      -- Variable: SO_DONTROUTE
      -- Variable: SO_BROADCAST
      -- Variable: SO_SNDBUF
      -- Variable: SO_RCVBUF
      -- Variable: SO_KEEPALIVE
      -- Variable: SO_OOBINLINE
      -- Variable: SO_NO_CHECK
      -- Variable: SO_PRIORITY
      -- Variable: SO_REUSEPORT
          The VALUE taken or returned is an integer.

      -- Variable: SO_LINGER
          The VALUE taken or returned is a pair of integers ‘(ENABLE .
          TIMEOUT)’.  On old systems without timeout support (ie.
          without ‘struct linger’), only ENABLE has an effect but the
          value in Guile is always a pair.

     For IP level (‘IPPROTO_IP’) the following OPTNAMEs are defined
     (when provided by the system).  See ‘man ip’ for what they mean.

      -- Variable: IP_MULTICAST_IF
          This sets the source interface used by multicast traffic.

      -- Variable: IP_MULTICAST_TTL
          This sets the default TTL for multicast traffic.  This
          defaults to 1 and should be increased to allow traffic to pass
          beyond the local network.

      -- Variable: IP_ADD_MEMBERSHIP
      -- Variable: IP_DROP_MEMBERSHIP
          These can be used only with ‘setsockopt’, not ‘getsockopt’.
          VALUE is a pair ‘(MULTIADDR . INTERFACEADDR)’ of integer IPv4
          addresses (*note Network Address Conversion::).  MULTIADDR is
          a multicast address to be added to or dropped from the
          interface INTERFACEADDR.  INTERFACEADDR can be ‘INADDR_ANY’ to
          have the system select the interface.  INTERFACEADDR can also
          be an interface index number, on systems supporting that.

 -- Scheme Procedure: shutdown sock how
 -- C Function: scm_shutdown (sock, how)
     Sockets can be closed simply by using ‘close-port’.  The ‘shutdown’
     procedure allows reception or transmission on a connection to be
     shut down individually, according to the parameter HOW:

     0
          Stop receiving data for this socket.  If further data arrives,
          reject it.
     1
          Stop trying to transmit data from this socket.  Discard any
          data waiting to be sent.  Stop looking for acknowledgement of
          data already sent; don’t retransmit it if it is lost.
     2
          Stop both reception and transmission.

     The return value is unspecified.

 -- Scheme Procedure: connect sock sockaddr
 -- Scheme Procedure: connect sock AF_INET ipv4addr port
 -- Scheme Procedure: connect sock AF_INET6 ipv6addr port [flowinfo
          [scopeid]]
 -- Scheme Procedure: connect sock AF_UNIX path
 -- C Function: scm_connect (sock, fam, address, args)
     Initiate a connection on socket port SOCK to a given address.  The
     destination is either a socket address object, or arguments the
     same as ‘make-socket-address’ would take to make such an object
     (*note Network Socket Address::).  The return value is unspecified.

          (connect sock AF_INET INADDR_LOOPBACK 23)
          (connect sock (make-socket-address AF_INET INADDR_LOOPBACK 23))

 -- Scheme Procedure: bind sock sockaddr
 -- Scheme Procedure: bind sock AF_INET ipv4addr port
 -- Scheme Procedure: bind sock AF_INET6 ipv6addr port [flowinfo
          [scopeid]]
 -- Scheme Procedure: bind sock AF_UNIX path
 -- C Function: scm_bind (sock, fam, address, args)
     Bind socket port SOCK to the given address.  The address is either
     a socket address object, or arguments the same as
     ‘make-socket-address’ would take to make such an object (*note
     Network Socket Address::).  The return value is unspecified.

     Generally a socket is only explicitly bound to a particular address
     when making a server, i.e. to listen on a particular port.  For an
     outgoing connection the system will assign a local address
     automatically, if not already bound.

          (bind sock AF_INET INADDR_ANY 12345)
          (bind sock (make-socket-address AF_INET INADDR_ANY 12345))

 -- Scheme Procedure: listen sock backlog
 -- C Function: scm_listen (sock, backlog)
     Enable SOCK to accept connection requests.  BACKLOG is an integer
     specifying the maximum length of the queue for pending connections.
     If the queue fills, new clients will fail to connect until the
     server calls ‘accept’ to accept a connection from the queue.

     The return value is unspecified.

 -- Scheme Procedure: accept sock
 -- C Function: scm_accept (sock)
     Accept a connection from socket port SOCK which has been enabled
     for listening with ‘listen’ above.  If there are no incoming
     connections in the queue, wait until one is available (unless
     ‘O_NONBLOCK’ has been set on the socket, *note ‘fcntl’: Ports and
     File Descriptors.).

     The return value is a pair.  The ‘car’ is a new socket port,
     connected and ready to communicate.  The ‘cdr’ is a socket address
     object (*note Network Socket Address::) which is where the remote
     connection is from (like ‘getpeername’ below).

     All communication takes place using the new socket returned.  The
     given SOCK remains bound and listening, and ‘accept’ may be called
     on it again to get another incoming connection when desired.

 -- Scheme Procedure: getsockname sock
 -- C Function: scm_getsockname (sock)
     Return a socket address object which is the where SOCK is bound
     locally.  SOCK may have obtained its local address from ‘bind’
     (above), or if a ‘connect’ is done with an otherwise unbound socket
     (which is usual) then the system will have assigned an address.

     Note that on many systems the address of a socket in the ‘AF_UNIX’
     namespace cannot be read.

 -- Scheme Procedure: getpeername sock
 -- C Function: scm_getpeername (sock)
     Return a socket address object which is where SOCK is connected to,
     i.e. the remote endpoint.

     Note that on many systems the address of a socket in the ‘AF_UNIX’
     namespace cannot be read.

 -- Scheme Procedure: recv! sock buf [flags]
 -- C Function: scm_recv (sock, buf, flags)
     Receive data from a socket port.  SOCK must already be bound to the
     address from which data is to be received.  BUF is a bytevector
     into which the data will be written.  The size of BUF limits the
     amount of data which can be received: in the case of packet
     protocols, if a packet larger than this limit is encountered then
     some data will be irrevocably lost.

     The optional FLAGS argument is a value or bitwise OR of ‘MSG_OOB’,
     ‘MSG_PEEK’, ‘MSG_DONTROUTE’ etc.

     The value returned is the number of bytes read from the socket.

     Note that the data is read directly from the socket file
     descriptor: any unread buffered port data is ignored.

 -- Scheme Procedure: send sock message [flags]
 -- C Function: scm_send (sock, message, flags)
     Transmit bytevector MESSAGE on socket port SOCK.  SOCK must already
     be bound to a destination address.  The value returned is the
     number of bytes transmitted—it’s possible for this to be less than
     the length of MESSAGE if the socket is set to be non-blocking.  The
     optional FLAGS argument is a value or bitwise OR of ‘MSG_OOB’,
     ‘MSG_PEEK’, ‘MSG_DONTROUTE’ etc.

     Note that the data is written directly to the socket file
     descriptor: any unflushed buffered port data is ignored.

 -- Scheme Procedure: recvfrom! sock buf [flags [start [end]]]
 -- C Function: scm_recvfrom (sock, buf, flags, start, end)
     Receive data from socket port SOCK, returning the originating
     address as well as the data.  This function is usually for datagram
     sockets, but can be used on stream-oriented sockets too.

     The data received is stored in bytevector BUF, using either the
     whole bytevector or just the region between the optional START and
     END positions.  The size of BUF limits the amount of data that can
     be received.  For datagram protocols if a packet larger than this
     is received then excess bytes are irrevocably lost.

     The return value is a pair.  The ‘car’ is the number of bytes read.
     The ‘cdr’ is a socket address object (*note Network Socket
     Address::) which is where the data came from, or ‘#f’ if the origin
     is unknown.

     The optional FLAGS argument is a or bitwise-OR (‘logior’) of
     ‘MSG_OOB’, ‘MSG_PEEK’, ‘MSG_DONTROUTE’ etc.

     Data is read directly from the socket file descriptor, any buffered
     port data is ignored.

     On a GNU/Linux system ‘recvfrom!’ is not multi-threading, all
     threads stop while a ‘recvfrom!’ call is in progress.  An
     application may need to use ‘select’, ‘O_NONBLOCK’ or
     ‘MSG_DONTWAIT’ to avoid this.

 -- Scheme Procedure: sendto sock message sockaddr [flags]
 -- Scheme Procedure: sendto sock message AF_INET ipv4addr port [flags]
 -- Scheme Procedure: sendto sock message AF_INET6 ipv6addr port
          [flowinfo [scopeid [flags]]]
 -- Scheme Procedure: sendto sock message AF_UNIX path [flags]
 -- C Function: scm_sendto (sock, message, fam, address, args_and_flags)
     Transmit bytevector MESSAGE as a datagram socket port SOCK.  The
     destination is specified either as a socket address object, or as
     arguments the same as would be taken by ‘make-socket-address’ to
     create such an object (*note Network Socket Address::).

     The destination address may be followed by an optional FLAGS
     argument which is a ‘logior’ (*note Bitwise Operations::) of
     ‘MSG_OOB’, ‘MSG_PEEK’, ‘MSG_DONTROUTE’ etc.

     The value returned is the number of bytes transmitted – it’s
     possible for this to be less than the length of MESSAGE if the
     socket is set to be non-blocking.  Note that the data is written
     directly to the socket file descriptor: any unflushed buffered port
     data is ignored.

7.2.11.5 Network Socket Examples
................................

The following give examples of how to use network sockets.

Internet Socket Client Example
..............................

The following example demonstrates an Internet socket client.  It
connects to the HTTP daemon running on the local machine and returns the
contents of the root index URL.

     (let ((s (socket PF_INET SOCK_STREAM 0)))
       (connect s AF_INET (inet-pton AF_INET "127.0.0.1") 80)
       (display "GET / HTTP/1.0\r\n\r\n" s)

       (do ((line (read-line s) (read-line s)))
           ((eof-object? line))
         (display line)
         (newline)))

Internet Socket Server Example
..............................

The following example shows a simple Internet server which listens on
port 2904 for incoming connections and sends a greeting back to the
client.

     (let ((s (socket PF_INET SOCK_STREAM 0)))
       (setsockopt s SOL_SOCKET SO_REUSEADDR 1)
       ;; Specific address?
       ;; (bind s AF_INET (inet-pton AF_INET "127.0.0.1") 2904)
       (bind s AF_INET INADDR_ANY 2904)
       (listen s 5)

       (simple-format #t "Listening for clients in pid: ~S" (getpid))
       (newline)

       (while #t
         (let* ((client-connection (accept s))
                (client-details (cdr client-connection))
                (client (car client-connection)))
           (simple-format #t "Got new client connection: ~S"
                          client-details)
           (newline)
           (simple-format #t "Client address: ~S"
                          (gethostbyaddr
                           (sockaddr:addr client-details)))
           (newline)
           ;; Send back the greeting to the client port
           (display "Hello client\r\n" client)
           (close client))))

7.2.12 System Identification
----------------------------

This section lists the various procedures Guile provides for accessing
information about the system it runs on.

 -- Scheme Procedure: uname
 -- C Function: scm_uname ()
     Return an object with some information about the computer system
     the program is running on.

     The following procedures accept an object as returned by ‘uname’
     and return a selected component (all of which are strings).

      -- Scheme Procedure: utsname:sysname un
          The name of the operating system.
      -- Scheme Procedure: utsname:nodename un
          The network name of the computer.
      -- Scheme Procedure: utsname:release un
          The current release level of the operating system
          implementation.
      -- Scheme Procedure: utsname:version un
          The current version level within the release of the operating
          system.
      -- Scheme Procedure: utsname:machine un
          A description of the hardware.

 -- Scheme Procedure: gethostname
 -- C Function: scm_gethostname ()
     Return the host name of the current processor.

 -- Scheme Procedure: sethostname name
 -- C Function: scm_sethostname (name)
     Set the host name of the current processor to NAME.  May only be
     used by the superuser.  The return value is not specified.

7.2.13 Locales
--------------

 -- Scheme Procedure: setlocale category [locale]
 -- C Function: scm_setlocale (category, locale)
     Get or set the current locale, used for various
     internationalizations.  Locales are strings, such as ‘sv_SE’.

     If LOCALE is given then the locale for the given CATEGORY is set
     and the new value returned.  If LOCALE is not given then the
     current value is returned.  CATEGORY should be one of the following
     values (*note Categories of Activities that Locales Affect:
     (libc)Locale Categories.):

      -- Variable: LC_ALL
      -- Variable: LC_COLLATE
      -- Variable: LC_CTYPE
      -- Variable: LC_MESSAGES
      -- Variable: LC_MONETARY
      -- Variable: LC_NUMERIC
      -- Variable: LC_TIME

     A common usage is ‘(setlocale LC_ALL "")’, which initializes all
     categories based on standard environment variables (‘LANG’ etc).
     For full details on categories and locale names *note Locales and
     Internationalization: (libc)Locales.

     Note that ‘setlocale’ affects locale settings for the whole
     process.  *Note locale objects and ‘make-locale’: i18n
     Introduction, for a thread-safe alternative.

7.2.14 Encryption
-----------------

Please note that the procedures in this section are not suited for
strong encryption, they are only interfaces to the well-known and common
system library functions of the same name.  They are just as good (or
bad) as the underlying functions, so you should refer to your system
documentation before using them (*note Encrypting Passwords:
(libc)crypt.).

 -- Scheme Procedure: crypt key salt
 -- C Function: scm_crypt (key, salt)
     Encrypt KEY, with the addition of SALT (both strings), using the
     ‘crypt’ C library call.

   Although ‘getpass’ is not an encryption procedure per se, it appears
here because it is often used in combination with ‘crypt’:

 -- Scheme Procedure: getpass prompt
 -- C Function: scm_getpass (prompt)
     Display PROMPT to the standard error output and read a password
     from ‘/dev/tty’.  If this file is not accessible, it reads from
     standard input.  The password may be up to 127 characters in
     length.  Additional characters and the terminating newline
     character are discarded.  While reading the password, echoing and
     the generation of signals by special characters is disabled.

7.3 HTTP, the Web, and All That
===============================

It has always been possible to connect computers together and share
information between them, but the rise of the World Wide Web over the
last couple of decades has made it much easier to do so.  The result is
a richly connected network of computation, in which Guile forms a part.

   By “the web”, we mean the HTTP protocol(1) as handled by servers,
clients, proxies, caches, and the various kinds of messages and message
components that can be sent and received by that protocol, notably HTML.

   On one level, the web is text in motion: the protocols themselves are
textual (though the payload may be binary), and it’s possible to create
a socket and speak text to the web.  But such an approach is obviously
primitive.  This section details the higher-level data types and
operations provided by Guile: URIs, HTTP request and response records,
and a conventional web server implementation.

   The material in this section is arranged in ascending order, in which
later concepts build on previous ones.  If you prefer to start with the
highest-level perspective, *note Web Examples::, and work your way back.

   ---------- Footnotes ----------

   (1) Yes, the P is for protocol, but this phrase appears repeatedly in
RFC 2616.

7.3.1 Types and the Web
-----------------------

It is a truth universally acknowledged, that a program with good use of
data types, will be free from many common bugs.  Unfortunately, the
common practice in web programming seems to ignore this maxim.  This
subsection makes the case for expressive data types in web programming.

   By “expressive data types”, we mean that the data types _say_
something about how a program solves a problem.  For example, if we
choose to represent dates using SRFI 19 date records (*note SRFI-19::),
this indicates that there is a part of the program that will always have
valid dates.  Error handling for a number of basic cases, like invalid
dates, occurs on the boundary in which we produce a SRFI 19 date record
from other types, like strings.

   With regards to the web, data types are helpful in the two broad
phases of HTTP messages: parsing and generation.

   Consider a server, which has to parse a request, and produce a
response.  Guile will parse the request into an HTTP request object
(*note Requests::), with each header parsed into an appropriate Scheme
data type.  This transition from an incoming stream of characters to
typed data is a state change in a program—the strings might parse, or
they might not, and something has to happen if they do not.  (Guile
throws an error in this case.)  But after you have the parsed request,
“client” code (code built on top of the Guile web framework) will not
have to check for syntactic validity.  The types already make this
information manifest.

   This state change on the parsing boundary makes programs more robust,
as they themselves are freed from the need to do a number of common
error checks, and they can use normal Scheme procedures to handle a
request instead of ad-hoc string parsers.

   The need for types on the response generation side (in a server) is
more subtle, though not less important.  Consider the example of a POST
handler, which prints out the text that a user submits from a form.
Such a handler might include a procedure like this:

     ;; First, a helper procedure
     (define (para . contents)
       (string-append "<p>" (string-concatenate contents) "</p>"))

     ;; Now the meat of our simple web application
     (define (you-said text)
       (para "You said: " text))

     (display (you-said "Hi!"))
     ⊣ <p>You said: Hi!</p>

   This is a perfectly valid implementation, provided that the incoming
text does not contain the special HTML characters ‘<’, ‘>’, or ‘&’.  But
this provision of a restricted character set is not reflected anywhere
in the program itself: we must _assume_ that the programmer understands
this, and performs the check elsewhere.

   Unfortunately, the short history of the practice of programming does
not bear out this assumption.  A "cross-site scripting" (XSS)
vulnerability is just such a common error in which unfiltered user input
is allowed into the output.  A user could submit a crafted comment to
your web site which results in visitors running malicious Javascript,
within the security context of your domain:

     (display (you-said "<script src=\"http://bad.com/nasty.js\" />"))
     ⊣ <p>You said: <script src="http://bad.com/nasty.js" /></p>

   The fundamental problem here is that both user data and the program
template are represented using strings.  This identity means that types
can’t help the programmer to make a distinction between these two, so
they get confused.

   There are a number of possible solutions, but perhaps the best is to
treat HTML not as strings, but as native s-expressions: as SXML. The
basic idea is that HTML is either text, represented by a string, or an
element, represented as a tagged list.  So ‘foo’ becomes ‘"foo"’, and
‘<b>foo</b>’ becomes ‘(b "foo")’.  Attributes, if present, go in a
tagged list headed by ‘@’, like ‘(img (@ (src
"http://example.com/foo.png")))’.  *Note SXML::, for more information.

   The good thing about SXML is that HTML elements cannot be confused
with text.  Let’s make a new definition of ‘para’:

     (define (para . contents)
       `(p ,@contents))

     (use-modules (sxml simple))
     (sxml->xml (you-said "Hi!"))
     ⊣ <p>You said: Hi!</p>

     (sxml->xml (you-said "<i>Rats, foiled again!</i>"))
     ⊣ <p>You said: &lt;i&gt;Rats, foiled again!&lt;/i&gt;</p>

   So we see in the second example that HTML elements cannot be
unwittingly introduced into the output.  However it is now perfectly
acceptable to pass SXML to ‘you-said’; in fact, that is the big
advantage of SXML over everything-as-a-string.

     (sxml->xml (you-said (you-said "<Hi!>")))
     ⊣ <p>You said: <p>You said: &lt;Hi!&gt;</p></p>

   The SXML types allow procedures to _compose_.  The types make
manifest which parts are HTML elements, and which are text.  So you
needn’t worry about escaping user input; the type transition back to a
string handles that for you.  XSS vulnerabilities are a thing of the
past.

   Well.  That’s all very nice and opinionated and such, but how do I
use the thing?  Read on!

7.3.2 Universal Resource Identifiers
------------------------------------

Guile provides a standard data type for Universal Resource Identifiers
(URIs), as defined in RFC 3986.

   The generic URI syntax is as follows:

     URI := scheme ":" ["//" [userinfo "@"] host [":" port]] path \
            [ "?" query ] [ "#" fragment ]

   For example, in the URI, ‘http://www.gnu.org/help/’, the scheme is
‘http’, the host is ‘www.gnu.org’, the path is ‘/help/’, and there is no
userinfo, port, query, or fragment.  All URIs have a scheme and a path
(though the path might be empty).  Some URIs have a host, and some of
those have ports and userinfo.  Any URI might have a query part or a
fragment.

   Userinfo is something of an abstraction, as some legacy URI schemes
allowed userinfo of the form ‘USERNAME:PASSWD’.  But since passwords do
not belong in URIs, the RFC does not want to condone this practice, so
it calls anything before the ‘@’ sign "userinfo".

   Properly speaking, a fragment is not part of a URI. For example, when
a web browser follows a link to ‘http://example.com/#foo’, it sends a
request for ‘http://example.com/’, then looks in the resulting page for
the fragment identified ‘foo’ reference.  A fragment identifies a part
of a resource, not the resource itself.  But it is useful to have a
fragment field in the URI record itself, so we hope you will forgive the
inconsistency.

     (use-modules (web uri))

   The following procedures can be found in the ‘(web uri)’ module.
Load it into your Guile, using a form like the above, to have access to
them.

 -- Scheme Procedure: build-uri scheme [#:userinfo=‘#f’] [#:host=‘#f’]
          [#:port=‘#f’] [#:path=‘""’] [#:query=‘#f’] [#:fragment=‘#f’]
          [#:validate?=‘#t’]
     Construct a URI object.  SCHEME should be a symbol, PORT either a
     positive, exact integer or ‘#f’, and the rest of the fields are
     either strings or ‘#f’.  If VALIDATE? is true, also run some
     consistency checks to make sure that the constructed URI is valid.

 -- Scheme Procedure: uri? obj
 -- Scheme Procedure: uri-scheme uri
 -- Scheme Procedure: uri-userinfo uri
 -- Scheme Procedure: uri-host uri
 -- Scheme Procedure: uri-port uri
 -- Scheme Procedure: uri-path uri
 -- Scheme Procedure: uri-query uri
 -- Scheme Procedure: uri-fragment uri
     A predicate and field accessors for the URI record type.  The URI
     scheme will be a symbol, the port either a positive, exact integer
     or ‘#f’, and the rest either strings or ‘#f’ if not present.

 -- Scheme Procedure: string->uri string
     Parse STRING into a URI object.  Return ‘#f’ if the string could
     not be parsed.

 -- Scheme Procedure: uri->string uri
     Serialize URI to a string.  If the URI has a port that is the
     default port for its scheme, the port is not included in the
     serialization.

 -- Scheme Procedure: declare-default-port! scheme port
     Declare a default port for the given URI scheme.

 -- Scheme Procedure: uri-decode str [#:encoding=‘"utf-8"’]
     Percent-decode the given STR, according to ENCODING, which should
     be the name of a character encoding.

     Note that this function should not generally be applied to a full
     URI string.  For paths, use ‘split-and-decode-uri-path’ instead.
     For query strings, split the query on ‘&’ and ‘=’ boundaries, and
     decode the components separately.

     Note also that percent-encoded strings encode _bytes_, not
     characters.  There is no guarantee that a given byte sequence is a
     valid string encoding.  Therefore this routine may signal an error
     if the decoded bytes are not valid for the given encoding.  Pass
     ‘#f’ for ENCODING if you want decoded bytes as a bytevector
     directly.  *Note ‘set-port-encoding!’: Ports, for more information
     on character encodings.

     Returns a string of the decoded characters, or a bytevector if
     ENCODING was ‘#f’.

   Fixme: clarify return type.  indicate default values.  type of
unescaped-chars.

 -- Scheme Procedure: uri-encode str [#:encoding=‘"utf-8"’]
          [#:unescaped-chars]
     Percent-encode any character not in the character set,
     UNESCAPED-CHARS.

     The default character set includes alphanumerics from ASCII, as
     well as the special characters ‘-’, ‘.’, ‘_’, and ‘~’.  Any other
     character will be percent-encoded, by writing out the character to
     a bytevector within the given ENCODING, then encoding each byte as
     ‘%HH’, where HH is the hexadecimal representation of the byte.

 -- Scheme Procedure: split-and-decode-uri-path path
     Split PATH into its components, and decode each component, removing
     empty components.

     For example, ‘"/foo/bar%20baz/"’ decodes to the two-element list,
     ‘("foo" "bar baz")’.

 -- Scheme Procedure: encode-and-join-uri-path parts
     URI-encode each element of PARTS, which should be a list of
     strings, and join the parts together with ‘/’ as a delimiter.

     For example, the list ‘("scrambled eggs" "biscuits&gravy")’ encodes
     as ‘"scrambled%20eggs/biscuits%26gravy"’.

7.3.3 The Hyper-Text Transfer Protocol
--------------------------------------

The initial motivation for including web functionality in Guile, rather
than rely on an external package, was to establish a standard base on
which people can share code.  To that end, we continue the focus on data
types by providing a number of low-level parsers and unparsers for
elements of the HTTP protocol.

   If you are want to skip the low-level details for now and move on to
web pages, *note Web Client::, and *note Web Server::.  Otherwise, load
the HTTP module, and read on.

     (use-modules (web http))

   The focus of the ‘(web http)’ module is to parse and unparse standard
HTTP headers, representing them to Guile as native data structures.  For
example, a ‘Date:’ header will be represented as a SRFI-19 date record
(*note SRFI-19::), rather than as a string.

   Guile tries to follow RFCs fairly strictly—the road to perdition
being paved with compatibility hacks—though some allowances are made for
not-too-divergent texts.

   Header names are represented as lower-case symbols.

 -- Scheme Procedure: string->header name
     Parse NAME to a symbolic header name.

 -- Scheme Procedure: header->string sym
     Return the string form for the header named SYM.

   For example:

     (string->header "Content-Length")
     ⇒ content-length
     (header->string 'content-length)
     ⇒ "Content-Length"

     (string->header "FOO")
     ⇒ foo
     (header->string 'foo)
     ⇒ "Foo"

   Guile keeps a registry of known headers, their string names, and some
parsing and serialization procedures.  If a header is unknown, its
string name is simply its symbol name in title-case.

 -- Scheme Procedure: known-header? sym
     Return ‘#t’ if SYM is a known header, with associated parsers and
     serialization procedures, or ‘#f’ otherwise.

 -- Scheme Procedure: header-parser sym
     Return the value parser for headers named SYM.  The result is a
     procedure that takes one argument, a string, and returns the parsed
     value.  If the header isn’t known to Guile, a default parser is
     returned that passes through the string unchanged.

 -- Scheme Procedure: header-validator sym
     Return a predicate which returns ‘#t’ if the given value is valid
     for headers named SYM.  The default validator for unknown headers
     is ‘string?’.

 -- Scheme Procedure: header-writer sym
     Return a procedure that writes values for headers named SYM to a
     port.  The resulting procedure takes two arguments: a value and a
     port.  The default writer is ‘display’.

   For more on the set of headers that Guile knows about out of the box,
*note HTTP Headers::.  To add your own, use the ‘declare-header!’
procedure:

 -- Scheme Procedure: declare-header! name parser validator writer
          [#:multiple?=‘#f’]
     Declare a parser, validator, and writer for a given header.

   For example, let’s say you are running a web server behind some sort
of proxy, and your proxy adds an ‘X-Client-Address’ header, indicating
the IPv4 address of the original client.  You would like for the HTTP
request record to parse out this header to a Scheme value, instead of
leaving it as a string.  You could register this header with Guile’s
HTTP stack like this:

     (declare-header! "X-Client-Address"
       (lambda (str)
         (inet-aton str))
       (lambda (ip)
         (and (integer? ip) (exact? ip) (<= 0 ip #xffffffff)))
       (lambda (ip port)
         (display (inet-ntoa ip) port)))

 -- Scheme Procedure: declare-opaque-header! name
     A specialised version of ‘declare-header!’ for the case in which
     you want a header’s value to be returned/written “as-is”.

 -- Scheme Procedure: valid-header? sym val
     Return a true value if VAL is a valid Scheme value for the header
     with name SYM, or ‘#f’ otherwise.

   Now that we have a generic interface for reading and writing headers,
we do just that.

 -- Scheme Procedure: read-header port
     Read one HTTP header from PORT.  Return two values: the header name
     and the parsed Scheme value.  May raise an exception if the header
     was known but the value was invalid.

     Returns the end-of-file object for both values if the end of the
     message body was reached (i.e., a blank line).

 -- Scheme Procedure: parse-header name val
     Parse VAL, a string, with the parser for the header named NAME.
     Returns the parsed value.

 -- Scheme Procedure: write-header name val port
     Write the given header name and value to PORT, using the writer
     from ‘header-writer’.

 -- Scheme Procedure: read-headers port
     Read the headers of an HTTP message from PORT, returning them as an
     ordered alist.

 -- Scheme Procedure: write-headers headers port
     Write the given header alist to PORT.  Doesn’t write the final
     ‘\r\n’, as the user might want to add another header.

   The ‘(web http)’ module also has some utility procedures to read and
write request and response lines.

 -- Scheme Procedure: parse-http-method str [start] [end]
     Parse an HTTP method from STR.  The result is an upper-case symbol,
     like ‘GET’.

 -- Scheme Procedure: parse-http-version str [start] [end]
     Parse an HTTP version from STR, returning it as a major–minor pair.
     For example, ‘HTTP/1.1’ parses as the pair of integers, ‘(1 . 1)’.

 -- Scheme Procedure: parse-request-uri str [start] [end]
     Parse a URI from an HTTP request line.  Note that URIs in requests
     do not have to have a scheme or host name.  The result is a URI
     object.

 -- Scheme Procedure: read-request-line port
     Read the first line of an HTTP request from PORT, returning three
     values: the method, the URI, and the version.

 -- Scheme Procedure: write-request-line method uri version port
     Write the first line of an HTTP request to PORT.

 -- Scheme Procedure: read-response-line port
     Read the first line of an HTTP response from PORT, returning three
     values: the HTTP version, the response code, and the “reason
     phrase”.

 -- Scheme Procedure: write-response-line version code reason-phrase
          port
     Write the first line of an HTTP response to PORT.

7.3.4 HTTP Headers
------------------

In addition to defining the infrastructure to parse headers, the ‘(web
http)’ module defines specific parsers and unparsers for all headers
defined in the HTTP/1.1 standard.

   For example, if you receive a header named ‘Accept-Language’ with a
value ‘en, es;q=0.8’, Guile parses it as a quality list (defined below):

     (parse-header 'accept-language "en, es;q=0.8")
     ⇒ ((1000 . "en") (800 . "es"))

   The format of the value for ‘Accept-Language’ headers is defined
below, along with all other headers defined in the HTTP standard.  (If
the header were unknown, the value would have been returned as a
string.)

   For brevity, the header definitions below are given in the form, TYPE
‘NAME’, indicating that values for the header ‘NAME’ will be of the
given TYPE.  Since Guile internally treats header names in lower case,
in this document we give types title-cased names.  A short description
of the each header’s purpose and an example follow.

   For full details on the meanings of all of these headers, see the
HTTP 1.1 standard, RFC 2616.

7.3.4.1 HTTP Header Types
.........................

Here we define the types that are used below, when defining headers.

 -- HTTP Header Type: Date
     A SRFI-19 date.

 -- HTTP Header Type: KVList
     A list whose elements are keys or key-value pairs.  Keys are parsed
     to symbols.  Values are strings by default.  Non-string values are
     the exception, and are mentioned explicitly below, as appropriate.

 -- HTTP Header Type: SList
     A list of strings.

 -- HTTP Header Type: Quality
     An exact integer between 0 and 1000.  Qualities are used to express
     preference, given multiple options.  An option with a quality of
     870, for example, is preferred over an option with quality 500.

     (Qualities are written out over the wire as numbers between 0.0 and
     1.0, but since the standard only allows three digits after the
     decimal, it’s equivalent to integers between 0 and 1000, so that’s
     what Guile uses.)

 -- HTTP Header Type: QList
     A quality list: a list of pairs, the car of which is a quality, and
     the cdr a string.  Used to express a list of options, along with
     their qualities.

 -- HTTP Header Type: ETag
     An entity tag, represented as a pair.  The car of the pair is an
     opaque string, and the cdr is ‘#t’ if the entity tag is a “strong”
     entity tag, and ‘#f’ otherwise.

7.3.4.2 General Headers
.......................

General HTTP headers may be present in any HTTP message.

 -- HTTP Header: KVList cache-control
     A key-value list of cache-control directives.  See RFC 2616, for
     more details.

     If present, parameters to ‘max-age’, ‘max-stale’, ‘min-fresh’, and
     ‘s-maxage’ are all parsed as non-negative integers.

     If present, parameters to ‘private’ and ‘no-cache’ are parsed as
     lists of header names, as symbols.

          (parse-header 'cache-control "no-cache,no-store"
          ⇒ (no-cache no-store)
          (parse-header 'cache-control "no-cache=\"Authorization,Date\",no-store"
          ⇒ ((no-cache . (authorization date)) no-store)
          (parse-header 'cache-control "no-cache=\"Authorization,Date\",max-age=10"
          ⇒ ((no-cache . (authorization date)) (max-age . 10))

 -- HTTP Header: List connection
     A list of header names that apply only to this HTTP connection, as
     symbols.  Additionally, the symbol ‘close’ may be present, to
     indicate that the server should close the connection after
     responding to the request.
          (parse-header 'connection "close")
          ⇒ (close)

 -- HTTP Header: Date date
     The date that a given HTTP message was originated.
          (parse-header 'date "Tue, 15 Nov 1994 08:12:31 GMT")
          ⇒ #<date ...>

 -- HTTP Header: KVList pragma
     A key-value list of implementation-specific directives.
          (parse-header 'pragma "no-cache, broccoli=tasty")
          ⇒ (no-cache (broccoli . "tasty"))

 -- HTTP Header: List trailer
     A list of header names which will appear after the message body,
     instead of with the message headers.
          (parse-header 'trailer "ETag")
          ⇒ (etag)

 -- HTTP Header: List transfer-encoding
     A list of transfer codings, expressed as key-value lists.  The only
     transfer coding defined by the specification is ‘chunked’.
          (parse-header 'transfer-encoding "chunked")
          ⇒ ((chunked))

 -- HTTP Header: List upgrade
     A list of strings, indicating additional protocols that a server
     could use in response to a request.
          (parse-header 'upgrade "WebSocket")
          ⇒ ("WebSocket")

   FIXME: parse out more fully?
 -- HTTP Header: List via
     A list of strings, indicating the protocol versions and hosts of
     intermediate servers and proxies.  There may be multiple ‘via’
     headers in one message.
          (parse-header 'via "1.0 venus, 1.1 mars")
          ⇒ ("1.0 venus" "1.1 mars")

 -- HTTP Header: List warning
     A list of warnings given by a server or intermediate proxy.  Each
     warning is a itself a list of four elements: a code, as an exact
     integer between 0 and 1000, a host as a string, the warning text as
     a string, and either ‘#f’ or a SRFI-19 date.

     There may be multiple ‘warning’ headers in one message.
          (parse-header 'warning "123 foo \"core breach imminent\"")
          ⇒ ((123 "foo" "core-breach imminent" #f))

7.3.4.3 Entity Headers
......................

Entity headers may be present in any HTTP message, and refer to the
resource referenced in the HTTP request or response.

 -- HTTP Header: List allow
     A list of allowed methods on a given resource, as symbols.
          (parse-header 'allow "GET, HEAD")
          ⇒ (GET HEAD)

 -- HTTP Header: List content-encoding
     A list of content codings, as symbols.
          (parse-header 'content-encoding "gzip")
          ⇒ (gzip)

 -- HTTP Header: List content-language
     The languages that a resource is in, as strings.
          (parse-header 'content-language "en")
          ⇒ ("en")

 -- HTTP Header: UInt content-length
     The number of bytes in a resource, as an exact, non-negative
     integer.
          (parse-header 'content-length "300")
          ⇒ 300

 -- HTTP Header: URI content-location
     The canonical URI for a resource, in the case that it is also
     accessible from a different URI.
          (parse-header 'content-location "http://example.com/foo")
          ⇒ #<<uri> ...>

 -- HTTP Header: String content-md5
     The MD5 digest of a resource.
          (parse-header 'content-md5 "ffaea1a79810785575e29e2bd45e2fa5")
          ⇒ "ffaea1a79810785575e29e2bd45e2fa5"

 -- HTTP Header: List content-range
     A range specification, as a list of three elements: the symbol
     ‘bytes’, either the symbol ‘*’ or a pair of integers, indicating
     the byte rage, and either ‘*’ or an integer, for the instance
     length.  Used to indicate that a response only includes part of a
     resource.
          (parse-header 'content-range "bytes 10-20/*")
          ⇒ (bytes (10 . 20) *)

 -- HTTP Header: List content-type
     The MIME type of a resource, as a symbol, along with any
     parameters.
          (parse-header 'content-length "text/plain")
          ⇒ (text/plain)
          (parse-header 'content-length "text/plain;charset=utf-8")
          ⇒ (text/plain (charset . "utf-8"))
     Note that the ‘charset’ parameter is something is a misnomer, and
     the HTTP specification admits this.  It specifies the _encoding_ of
     the characters, not the character set.

 -- HTTP Header: Date expires
     The date/time after which the resource given in a response is
     considered stale.
          (parse-header 'expires "Tue, 15 Nov 1994 08:12:31 GMT")
          ⇒ #<date ...>

 -- HTTP Header: Date last-modified
     The date/time on which the resource given in a response was last
     modified.
          (parse-header 'expires "Tue, 15 Nov 1994 08:12:31 GMT")
          ⇒ #<date ...>

7.3.4.4 Request Headers
.......................

Request headers may only appear in an HTTP request, not in a response.

 -- HTTP Header: List accept
     A list of preferred media types for a response.  Each element of
     the list is itself a list, in the same format as ‘content-type’.
          (parse-header 'accept "text/html,text/plain;charset=utf-8")
          ⇒ ((text/html) (text/plain (charset . "utf-8")))
     Preference is expressed with quality values:
          (parse-header 'accept "text/html;q=0.8,text/plain;q=0.6")
          ⇒ ((text/html (q . 800)) (text/plain (q . 600)))

 -- HTTP Header: QList accept-charset
     A quality list of acceptable charsets.  Note again that what HTTP
     calls a “charset” is what Guile calls a “character encoding”.
          (parse-header 'accept-charset "iso-8859-5, unicode-1-1;q=0.8")
          ⇒ ((1000 . "iso-8859-5") (800 . "unicode-1-1"))

 -- HTTP Header: QList accept-encoding
     A quality list of acceptable content codings.
          (parse-header 'accept-encoding "gzip,identity=0.8")
          ⇒ ((1000 . "gzip") (800 . "identity"))

 -- HTTP Header: QList accept-language
     A quality list of acceptable languages.
          (parse-header 'accept-language "cn,en=0.75")
          ⇒ ((1000 . "cn") (750 . "en"))

 -- HTTP Header: Pair authorization
     Authorization credentials.  The car of the pair indicates the
     authentication scheme, like ‘basic’.  For basic authentication, the
     cdr of the pair will be the base64-encoded ‘USER:PASS’ string.  For
     other authentication schemes, like ‘digest’, the cdr will be a
     key-value list of credentials.
          (parse-header 'authorization "Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=="
          ⇒ (basic . "QWxhZGRpbjpvcGVuIHNlc2FtZQ==")

 -- HTTP Header: List expect
     A list of expectations that a client has of a server.  The
     expectations are key-value lists.
          (parse-header 'expect "100-continue")
          ⇒ ((100-continue))

 -- HTTP Header: String from
     The email address of a user making an HTTP request.
          (parse-header 'from "bob@example.com")
          ⇒ "bob@example.com"

 -- HTTP Header: Pair host
     The host for the resource being requested, as a hostname-port pair.
     If no port is given, the port is ‘#f’.
          (parse-header 'host "gnu.org:80")
          ⇒ ("gnu.org" . 80)
          (parse-header 'host "gnu.org")
          ⇒ ("gnu.org" . #f)

 -- HTTP Header: *|List if-match
     A set of etags, indicating that the request should proceed if and
     only if the etag of the resource is in that set.  Either the symbol
     ‘*’, indicating any etag, or a list of entity tags.
          (parse-header 'if-match "*")
          ⇒ *
          (parse-header 'if-match "asdfadf")
          ⇒ (("asdfadf" . #t))
          (parse-header 'if-match W/"asdfadf")
          ⇒ (("asdfadf" . #f))

 -- HTTP Header: Date if-modified-since
     Indicates that a response should proceed if and only if the
     resource has been modified since the given date.
          (parse-header 'if-modified-since "Tue, 15 Nov 1994 08:12:31 GMT")
          ⇒ #<date ...>

 -- HTTP Header: *|List if-none-match
     A set of etags, indicating that the request should proceed if and
     only if the etag of the resource is not in the set.  Either the
     symbol ‘*’, indicating any etag, or a list of entity tags.
          (parse-header 'if-none-match "*")
          ⇒ *

 -- HTTP Header: ETag|Date if-range
     Indicates that the range request should proceed if and only if the
     resource matches a modification date or an etag.  Either an entity
     tag, or a SRFI-19 date.
          (parse-header 'if-range "\"original-etag\"")
          ⇒ ("original-etag" . #t)

 -- HTTP Header: Date if-unmodified-since
     Indicates that a response should proceed if and only if the
     resource has not been modified since the given date.
          (parse-header 'if-not-modified-since "Tue, 15 Nov 1994 08:12:31 GMT")
          ⇒ #<date ...>

 -- HTTP Header: UInt max-forwards
     The maximum number of proxy or gateway hops that a request should
     be subject to.
          (parse-header 'max-forwards "10")
          ⇒ 10

 -- HTTP Header: Pair proxy-authorization
     Authorization credentials for a proxy connection.  See the
     documentation for ‘authorization’ above for more information on the
     format.
          (parse-header 'proxy-authorization "Digest foo=bar,baz=qux"
          ⇒ (digest (foo . "bar") (baz . "qux"))

 -- HTTP Header: Pair range
     A range request, indicating that the client wants only part of a
     resource.  The car of the pair is the symbol ‘bytes’, and the cdr
     is a list of pairs.  Each element of the cdr indicates a range; the
     car is the first byte position and the cdr is the last byte
     position, as integers, or ‘#f’ if not given.
          (parse-header 'range "bytes=10-30,50-")
          ⇒ (bytes (10 . 30) (50 . #f))

 -- HTTP Header: URI referer
     The URI of the resource that referred the user to this resource.
     The name of the header is a misspelling, but we are stuck with it.
          (parse-header 'referer "http://www.gnu.org/")
          ⇒ #<uri ...>

 -- HTTP Header: List te
     A list of transfer codings, expressed as key-value lists.  A common
     transfer coding is ‘trailers’.
          (parse-header 'te "trailers")
          ⇒ ((trailers))

 -- HTTP Header: String user-agent
     A string indicating the user agent making the request.  The
     specification defines a structured format for this header, but it
     is widely disregarded, so Guile does not attempt to parse strictly.
          (parse-header 'user-agent "Mozilla/5.0")
          ⇒ "Mozilla/5.0"

7.3.4.5 Response Headers
........................

 -- HTTP Header: List accept-ranges
     A list of range units that the server supports, as symbols.
          (parse-header 'accept-ranges "bytes")
          ⇒ (bytes)

 -- HTTP Header: UInt age
     The age of a cached response, in seconds.
          (parse-header 'age "3600")
          ⇒ 3600

 -- HTTP Header: ETag etag
     The entity-tag of the resource.
          (parse-header 'etag "\"foo\"")
          ⇒ ("foo" . #t)

 -- HTTP Header: URI location
     A URI on which a request may be completed.  Used in combination
     with a redirecting status code to perform client-side redirection.
          (parse-header 'location "http://example.com/other")
          ⇒ #<uri ...>

 -- HTTP Header: List proxy-authenticate
     A list of challenges to a proxy, indicating the need for
     authentication.
          (parse-header 'proxy-authenticate "Basic realm=\"foo\"")
          ⇒ ((basic (realm . "foo")))

 -- HTTP Header: UInt|Date retry-after
     Used in combination with a server-busy status code, like 503, to
     indicate that a client should retry later.  Either a number of
     seconds, or a date.
          (parse-header 'retry-after "60")
          ⇒ 60

 -- HTTP Header: String server
     A string identifying the server.
          (parse-header 'server "My first web server")
          ⇒ "My first web server"

 -- HTTP Header: *|List vary
     A set of request headers that were used in computing this response.
     Used to indicate that server-side content negotiation was
     performed, for example in response to the ‘accept-language’ header.
     Can also be the symbol ‘*’, indicating that all headers were
     considered.
          (parse-header 'vary "Accept-Language, Accept")
          ⇒ (accept-language accept)

 -- HTTP Header: List www-authenticate
     A list of challenges to a user, indicating the need for
     authentication.
          (parse-header 'www-authenticate "Basic realm=\"foo\"")
          ⇒ ((basic (realm . "foo")))

7.3.5 Transfer Codings
----------------------

HTTP 1.1 allows for various transfer codings to be applied to message
bodies.  These include various types of compression, and HTTP chunked
encoding.  Currently, only chunked encoding is supported by guile.

   Chunked coding is an optional coding that may be applied to message
bodies, to allow messages whose length is not known beforehand to be
returned.  Such messages can be split into chunks, terminated by a final
zero length chunk.

   In order to make dealing with encodings more simple, guile provides
procedures to create ports that “wrap” existing ports, applying
transformations transparently under the hood.

   These procedures are in the ‘(web http)’ module.

     (use-modules (web http))

 -- Scheme Procedure: make-chunked-input-port port [#:keep-alive?=#f]
     Returns a new port, that transparently reads and decodes
     chunk-encoded data from PORT.  If no more chunk-encoded data is
     available, it returns the end-of-file object.  When the port is
     closed, PORT will also be closed, unless KEEP-ALIVE? is true.

     (use-modules (ice-9 rdelim))

     (define s "5\r\nFirst\r\nA\r\n line\n Sec\r\n8\r\nond line\r\n0\r\n")
     (define p (make-chunked-input-port (open-input-string s)))
     (read-line s)
     ⇒ "First line"
     (read-line s)
     ⇒ "Second line"

 -- Scheme Procedure: make-chunked-output-port port [#:keep-alive?=#f]
     Returns a new port, which transparently encodes data as
     chunk-encoded before writing it to PORT.  Whenever a write occurs
     on this port, it buffers it, until the port is flushed, at which
     point it writes a chunk containing all the data written so far.
     When the port is closed, the data remaining is written to PORT, as
     is the terminating zero chunk.  It also causes PORT to be closed,
     unless KEEP-ALIVE? is true.

     Note.  Forcing a chunked output port when there is no data is
     buffered does not write a zero chunk, as this would cause the data
     to be interpreted incorrectly by the client.

     (call-with-output-string
       (lambda (out)
         (define out* (make-chunked-output-port out #:keep-alive? #t))
         (display "first chunk" out*)
         (force-output out*)
         (force-output out*) ; note this does not write a zero chunk
         (display "second chunk" out*)
         (close-port out*)))
     ⇒ "b\r\nfirst chunk\r\nc\r\nsecond chunk\r\n0\r\n"

7.3.6 HTTP Requests
-------------------

     (use-modules (web request))

   The request module contains a data type for HTTP requests.

7.3.6.1 An Important Note on Character Sets
...........................................

HTTP requests consist of two parts: the request proper, consisting of a
request line and a set of headers, and (optionally) a body.  The body
might have a binary content-type, and even in the textual case its
length is specified in bytes, not characters.

   Therefore, HTTP is a fundamentally binary protocol.  However the
request line and headers are specified to be in a subset of ASCII, so
they can be treated as text, provided that the port’s encoding is set to
an ASCII-compatible one-byte-per-character encoding.  ISO-8859-1
(latin-1) is just such an encoding, and happens to be very efficient for
Guile.

   So what Guile does when reading requests from the wire, or writing
them out, is to set the port’s encoding to latin-1, and treating the
request headers as text.

   The request body is another issue.  For binary data, the data is
probably in a bytevector, so we use the R6RS binary output procedures to
write out the binary payload.  Textual data usually has to be written
out to some character encoding, usually UTF-8, and then the resulting
bytevector is written out to the port.

   In summary, Guile reads and writes HTTP over latin-1 sockets, without
any loss of generality.

7.3.6.2 Request API
...................

 -- Scheme Procedure: request? obj
 -- Scheme Procedure: request-method request
 -- Scheme Procedure: request-uri request
 -- Scheme Procedure: request-version request
 -- Scheme Procedure: request-headers request
 -- Scheme Procedure: request-meta request
 -- Scheme Procedure: request-port request
     A predicate and field accessors for the request type.  The fields
     are as follows:
     ‘method’
          The HTTP method, for example, ‘GET’.
     ‘uri’
          The URI as a URI record.
     ‘version’
          The HTTP version pair, like ‘(1 . 1)’.
     ‘headers’
          The request headers, as an alist of parsed values.
     ‘meta’
          An arbitrary alist of other data, for example information
          returned in the ‘sockaddr’ from ‘accept’ (*note Network
          Sockets and Communication::).
     ‘port’
          The port on which to read or write a request body, if any.

 -- Scheme Procedure: read-request port [meta='()]
     Read an HTTP request from PORT, optionally attaching the given
     metadata, META.

     As a side effect, sets the encoding on PORT to ISO-8859-1
     (latin-1), so that reading one character reads one byte.  See the
     discussion of character sets above, for more information.

     Note that the body is not part of the request.  Once you have read
     a request, you may read the body separately, and likewise for
     writing requests.

 -- Scheme Procedure: build-request uri [#:method='GET] [#:version='(1 .
          1)] [#:headers='()] [#:port=#f] [#:meta='()]
          [#:validate-headers?=#t]
     Construct an HTTP request object.  If VALIDATE-HEADERS? is true,
     the headers are each run through their respective validators.

 -- Scheme Procedure: write-request r port
     Write the given HTTP request to PORT.

     Return a new request, whose ‘request-port’ will continue writing on
     PORT, perhaps using some transfer encoding.

 -- Scheme Procedure: read-request-body r
     Reads the request body from R, as a bytevector.  Return ‘#f’ if
     there was no request body.

 -- Scheme Procedure: write-request-body r bv
     Write BV, a bytevector, to the port corresponding to the HTTP
     request R.

   The various headers that are typically associated with HTTP requests
may be accessed with these dedicated accessors.  *Note HTTP Headers::,
for more information on the format of parsed headers.

 -- Scheme Procedure: request-accept request [default='()]
 -- Scheme Procedure: request-accept-charset request [default='()]
 -- Scheme Procedure: request-accept-encoding request [default='()]
 -- Scheme Procedure: request-accept-language request [default='()]
 -- Scheme Procedure: request-allow request [default='()]
 -- Scheme Procedure: request-authorization request [default=#f]
 -- Scheme Procedure: request-cache-control request [default='()]
 -- Scheme Procedure: request-connection request [default='()]
 -- Scheme Procedure: request-content-encoding request [default='()]
 -- Scheme Procedure: request-content-language request [default='()]
 -- Scheme Procedure: request-content-length request [default=#f]
 -- Scheme Procedure: request-content-location request [default=#f]
 -- Scheme Procedure: request-content-md5 request [default=#f]
 -- Scheme Procedure: request-content-range request [default=#f]
 -- Scheme Procedure: request-content-type request [default=#f]
 -- Scheme Procedure: request-date request [default=#f]
 -- Scheme Procedure: request-expect request [default='()]
 -- Scheme Procedure: request-expires request [default=#f]
 -- Scheme Procedure: request-from request [default=#f]
 -- Scheme Procedure: request-host request [default=#f]
 -- Scheme Procedure: request-if-match request [default=#f]
 -- Scheme Procedure: request-if-modified-since request [default=#f]
 -- Scheme Procedure: request-if-none-match request [default=#f]
 -- Scheme Procedure: request-if-range request [default=#f]
 -- Scheme Procedure: request-if-unmodified-since request [default=#f]
 -- Scheme Procedure: request-last-modified request [default=#f]
 -- Scheme Procedure: request-max-forwards request [default=#f]
 -- Scheme Procedure: request-pragma request [default='()]
 -- Scheme Procedure: request-proxy-authorization request [default=#f]
 -- Scheme Procedure: request-range request [default=#f]
 -- Scheme Procedure: request-referer request [default=#f]
 -- Scheme Procedure: request-te request [default=#f]
 -- Scheme Procedure: request-trailer request [default='()]
 -- Scheme Procedure: request-transfer-encoding request [default='()]
 -- Scheme Procedure: request-upgrade request [default='()]
 -- Scheme Procedure: request-user-agent request [default=#f]
 -- Scheme Procedure: request-via request [default='()]
 -- Scheme Procedure: request-warning request [default='()]
     Return the given request header, or DEFAULT if none was present.

 -- Scheme Procedure: request-absolute-uri r [default-host=#f]
          [default-port=#f]
     A helper routine to determine the absolute URI of a request, using
     the ‘host’ header and the default host and port.

7.3.7 HTTP Responses
--------------------

     (use-modules (web response))

   As with requests (*note Requests::), Guile offers a data type for
HTTP responses.  Again, the body is represented separately from the
request.

 -- Scheme Procedure: response? obj
 -- Scheme Procedure: response-version response
 -- Scheme Procedure: response-code response
 -- Scheme Procedure: response-reason-phrase response
 -- Scheme Procedure: response-headers response
 -- Scheme Procedure: response-port response
     A predicate and field accessors for the response type.  The fields
     are as follows:
     ‘version’
          The HTTP version pair, like ‘(1 . 1)’.
     ‘code’
          The HTTP response code, like ‘200’.
     ‘reason-phrase’
          The reason phrase, or the standard reason phrase for the
          response’s code.
     ‘headers’
          The response headers, as an alist of parsed values.
     ‘port’
          The port on which to read or write a response body, if any.

 -- Scheme Procedure: read-response port
     Read an HTTP response from PORT.

     As a side effect, sets the encoding on PORT to ISO-8859-1
     (latin-1), so that reading one character reads one byte.  See the
     discussion of character sets in *note Responses::, for more
     information.

 -- Scheme Procedure: build-response [#:version='(1 . 1)] [#:code=200]
          [#:reason-phrase=#f] [#:headers='()] [#:port=#f]
          [#:validate-headers?=#t]
     Construct an HTTP response object.  If VALIDATE-HEADERS? is true,
     the headers are each run through their respective validators.

 -- Scheme Procedure: adapt-response-version response version
     Adapt the given response to a different HTTP version.  Return a new
     HTTP response.

     The idea is that many applications might just build a response for
     the default HTTP version, and this method could handle a number of
     programmatic transformations to respond to older HTTP versions (0.9
     and 1.0).  But currently this function is a bit heavy-handed, just
     updating the version field.

 -- Scheme Procedure: write-response r port
     Write the given HTTP response to PORT.

     Return a new response, whose ‘response-port’ will continue writing
     on PORT, perhaps using some transfer encoding.

 -- Scheme Procedure: response-must-not-include-body? r
     Some responses, like those with status code 304, are specified as
     never having bodies.  This predicate returns ‘#t’ for those
     responses.

     Note also, though, that responses to ‘HEAD’ requests must also not
     have a body.

 -- Scheme Procedure: response-body-port r [#:decode?=#t]
          [#:keep-alive?=#t]
     Return an input port from which the body of R can be read.  The
     encoding of the returned port is set according to R’s
     ‘content-type’ header, when it’s textual, except if DECODE? is
     ‘#f’.  Return ‘#f’ when no body is available.

     When KEEP-ALIVE? is ‘#f’, closing the returned port also closes R’s
     response port.

 -- Scheme Procedure: read-response-body r
     Read the response body from R, as a bytevector.  Returns ‘#f’ if
     there was no response body.

 -- Scheme Procedure: write-response-body r bv
     Write BV, a bytevector, to the port corresponding to the HTTP
     response R.

   As with requests, the various headers that are typically associated
with HTTP responses may be accessed with these dedicated accessors.
*Note HTTP Headers::, for more information on the format of parsed
headers.

 -- Scheme Procedure: response-accept-ranges response [default=#f]
 -- Scheme Procedure: response-age response [default='()]
 -- Scheme Procedure: response-allow response [default='()]
 -- Scheme Procedure: response-cache-control response [default='()]
 -- Scheme Procedure: response-connection response [default='()]
 -- Scheme Procedure: response-content-encoding response [default='()]
 -- Scheme Procedure: response-content-language response [default='()]
 -- Scheme Procedure: response-content-length response [default=#f]
 -- Scheme Procedure: response-content-location response [default=#f]
 -- Scheme Procedure: response-content-md5 response [default=#f]
 -- Scheme Procedure: response-content-range response [default=#f]
 -- Scheme Procedure: response-content-type response [default=#f]
 -- Scheme Procedure: response-date response [default=#f]
 -- Scheme Procedure: response-etag response [default=#f]
 -- Scheme Procedure: response-expires response [default=#f]
 -- Scheme Procedure: response-last-modified response [default=#f]
 -- Scheme Procedure: response-location response [default=#f]
 -- Scheme Procedure: response-pragma response [default='()]
 -- Scheme Procedure: response-proxy-authenticate response [default=#f]
 -- Scheme Procedure: response-retry-after response [default=#f]
 -- Scheme Procedure: response-server response [default=#f]
 -- Scheme Procedure: response-trailer response [default='()]
 -- Scheme Procedure: response-transfer-encoding response [default='()]
 -- Scheme Procedure: response-upgrade response [default='()]
 -- Scheme Procedure: response-vary response [default='()]
 -- Scheme Procedure: response-via response [default='()]
 -- Scheme Procedure: response-warning response [default='()]
 -- Scheme Procedure: response-www-authenticate response [default=#f]
     Return the given response header, or DEFAULT if none was present.

 -- Scheme Procedure: text-content-type? TYPE
     Return ‘#t’ if TYPE, a symbol as returned by
     ‘response-content-type’, represents a textual type such as
     ‘text/plain’.

7.3.8 Web Client
----------------

‘(web client)’ provides a simple, synchronous HTTP client, built on the
lower-level HTTP, request, and response modules.

     (use-modules (web client))

 -- Scheme Procedure: open-socket-for-uri uri
     Return an open input/output port for a connection to URI.

 -- Scheme Procedure: http-get uri arg...
 -- Scheme Procedure: http-head uri arg...
 -- Scheme Procedure: http-post uri arg...
 -- Scheme Procedure: http-put uri arg...
 -- Scheme Procedure: http-delete uri arg...
 -- Scheme Procedure: http-trace uri arg...
 -- Scheme Procedure: http-options uri arg...

     Connect to the server corresponding to URI and make a request over
     HTTP, using the appropriate method (‘GET’, ‘HEAD’, etc.).

     All of these procedures have the same prototype: a URI followed by
     an optional sequence of keyword arguments.  These keyword arguments
     allow you to modify the requests in various ways, for example
     attaching a body to the request, or setting specific headers.  The
     following table lists the keyword arguments and their default
     values.

     ‘#:body #f’
     ‘#:port (open-socket-for-uri URI)]’
     ‘#:version '(1 . 1)’
     ‘#:keep-alive? #f’
     ‘#:headers '()’
     ‘#:decode-body? #t’
     ‘#:streaming? #f’

     If you already have a port open, pass it as PORT.  Otherwise, a
     connection will be opened to the server corresponding to URI.  Any
     extra headers in the alist HEADERS will be added to the request.

     If BODY is not ‘#f’, a message body will also be sent with the HTTP
     request.  If BODY is a string, it is encoded according to the
     content-type in HEADERS, defaulting to UTF-8.  Otherwise BODY
     should be a bytevector, or ‘#f’ for no body.  Although a message
     body may be sent with any request, usually only ‘POST’ and ‘PUT’
     requests have bodies.

     If DECODE-BODY? is true, as is the default, the body of the
     response will be decoded to string, if it is a textual
     content-type.  Otherwise it will be returned as a bytevector.

     However, if STREAMING? is true, instead of eagerly reading the
     response body from the server, this function only reads off the
     headers.  The response body will be returned as a port on which the
     data may be read.

     Unless KEEP-ALIVE? is true, the port will be closed after the full
     response body has been read.

     Returns two values: the response read from the server, and the
     response body as a string, bytevector, #f value, or as a port (if
     STREAMING? is true).

   ‘http-get’ is useful for making one-off requests to web sites.  If
you are writing a web spider or some other client that needs to handle a
number of requests in parallel, it’s better to build an event-driven URL
fetcher, similar in structure to the web server (*note Web Server::).

   Another option, good but not as performant, would be to use threads,
possibly via par-map or futures.

 -- Scheme Parameter: current-http-proxy
     Either ‘#f’ or a non-empty string containing the URL of the HTTP
     proxy server to be used by the procedures in the ‘(web client)’
     module, including ‘open-socket-for-uri’.  Its initial value is
     based on the ‘http_proxy’ environment variable.

          (current-http-proxy) ⇒ "http://localhost:8123/"
          (parameterize ((current-http-proxy #f))
            (http-get "http://example.com/"))  ; temporarily bypass proxy
          (current-http-proxy) ⇒ "http://localhost:8123/"

7.3.9 Web Server
----------------

‘(web server)’ is a generic web server interface, along with a main loop
implementation for web servers controlled by Guile.

     (use-modules (web server))

   The lowest layer is the ‘<server-impl>’ object, which defines a set
of hooks to open a server, read a request from a client, write a
response to a client, and close a server.  These hooks – ‘open’, ‘read’,
‘write’, and ‘close’, respectively – are bound together in a
‘<server-impl>’ object.  Procedures in this module take a
‘<server-impl>’ object, if needed.

   A ‘<server-impl>’ may also be looked up by name.  If you pass the
‘http’ symbol to ‘run-server’, Guile looks for a variable named ‘http’
in the ‘(web server http)’ module, which should be bound to a
‘<server-impl>’ object.  Such a binding is made by instantiation of the
‘define-server-impl’ syntax.  In this way the run-server loop can
automatically load other backends if available.

   The life cycle of a server goes as follows:

  1. The ‘open’ hook is called, to open the server.  ‘open’ takes zero
     or more arguments, depending on the backend, and returns an opaque
     server socket object, or signals an error.

  2. The ‘read’ hook is called, to read a request from a new client.
     The ‘read’ hook takes one argument, the server socket.  It should
     return three values: an opaque client socket, the request, and the
     request body.  The request should be a ‘<request>’ object, from
     ‘(web request)’.  The body should be a string or a bytevector, or
     ‘#f’ if there is no body.

     If the read failed, the ‘read’ hook may return #f for the client
     socket, request, and body.

  3. A user-provided handler procedure is called, with the request and
     body as its arguments.  The handler should return two values: the
     response, as a ‘<response>’ record from ‘(web response)’, and the
     response body as bytevector, or ‘#f’ if not present.

     The respose and response body are run through ‘sanitize-response’,
     documented below.  This allows the handler writer to take some
     convenient shortcuts: for example, instead of a ‘<response>’, the
     handler can simply return an alist of headers, in which case a
     default response object is constructed with those headers.  Instead
     of a bytevector for the body, the handler can return a string,
     which will be serialized into an appropriate encoding; or it can
     return a procedure, which will be called on a port to write out the
     data.  See the ‘sanitize-response’ documentation, for more.

  4. The ‘write’ hook is called with three arguments: the client socket,
     the response, and the body.  The ‘write’ hook returns no values.

  5. At this point the request handling is complete.  For a loop, we
     loop back and try to read a new request.

  6. If the user interrupts the loop, the ‘close’ hook is called on the
     server socket.

   A user may define a server implementation with the following form:

 -- Scheme Syntax: define-server-impl name open read write close
     Make a ‘<server-impl>’ object with the hooks OPEN, READ, WRITE, and
     CLOSE, and bind it to the symbol NAME in the current module.

 -- Scheme Procedure: lookup-server-impl impl
     Look up a server implementation.  If IMPL is a server
     implementation already, it is returned directly.  If it is a
     symbol, the binding named IMPL in the ‘(web server IMPL)’ module is
     looked up.  Otherwise an error is signaled.

     Currently a server implementation is a somewhat opaque type, useful
     only for passing to other procedures in this module, like
     ‘read-client’.

   The ‘(web server)’ module defines a number of routines that use
‘<server-impl>’ objects to implement parts of a web server.  Given that
we don’t expose the accessors for the various fields of a
‘<server-impl>’, indeed these routines are the only procedures with any
access to the impl objects.

 -- Scheme Procedure: open-server impl open-params
     Open a server for the given implementation.  Return one value, the
     new server object.  The implementation’s ‘open’ procedure is
     applied to OPEN-PARAMS, which should be a list.

 -- Scheme Procedure: read-client impl server
     Read a new client from SERVER, by applying the implementation’s
     ‘read’ procedure to the server.  If successful, return three
     values: an object corresponding to the client, a request object,
     and the request body.  If any exception occurs, return ‘#f’ for all
     three values.

 -- Scheme Procedure: handle-request handler request body state
     Handle a given request, returning the response and body.

     The response and response body are produced by calling the given
     HANDLER with REQUEST and BODY as arguments.

     The elements of STATE are also passed to HANDLER as arguments, and
     may be returned as additional values.  The new STATE, collected
     from the HANDLER’s return values, is then returned as a list.  The
     idea is that a server loop receives a handler from the user, along
     with whatever state values the user is interested in, allowing the
     user’s handler to explicitly manage its state.

 -- Scheme Procedure: sanitize-response request response body
     “Sanitize” the given response and body, making them appropriate for
     the given request.

     As a convenience to web handler authors, RESPONSE may be given as
     an alist of headers, in which case it is used to construct a
     default response.  Ensures that the response version corresponds to
     the request version.  If BODY is a string, encodes the string to a
     bytevector, in an encoding appropriate for RESPONSE.  Adds a
     ‘content-length’ and ‘content-type’ header, as necessary.

     If BODY is a procedure, it is called with a port as an argument,
     and the output collected as a bytevector.  In the future we might
     try to instead use a compressing, chunk-encoded port, and call this
     procedure later, in the write-client procedure.  Authors are
     advised not to rely on the procedure being called at any particular
     time.

 -- Scheme Procedure: write-client impl server client response body
     Write an HTTP response and body to CLIENT.  If the server and
     client support persistent connections, it is the implementation’s
     responsibility to keep track of the client thereafter, presumably
     by attaching it to the SERVER argument somehow.

 -- Scheme Procedure: close-server impl server
     Release resources allocated by a previous invocation of
     ‘open-server’.

   Given the procedures above, it is a small matter to make a web
server:

 -- Scheme Procedure: serve-one-client handler impl server state
     Read one request from SERVER, call HANDLER on the request and body,
     and write the response to the client.  Return the new state
     produced by the handler procedure.

 -- Scheme Procedure: run-server handler [impl='http] [open-params='()]
          arg …
     Run Guile’s built-in web server.

     HANDLER should be a procedure that takes two or more arguments, the
     HTTP request and request body, and returns two or more values, the
     response and response body.

     For examples, skip ahead to the next section, *note Web Examples::.

     The response and body will be run through ‘sanitize-response’
     before sending back to the client.

     Additional arguments to HANDLER are taken from ARG ....  These
     arguments comprise a "state".  Additional return values are
     accumulated into a new state, which will be used for subsequent
     requests.  In this way a handler can explicitly manage its state.

   The default web server implementation is ‘http’, which binds to a
socket, listening for request on that port.

 -- HTTP Implementation: http [#:host=#f] [#:family=AF_INET]
          [#:addr=INADDR_LOOPBACK] [#:port 8080] [#:socket]
     The default HTTP implementation.  We document it as a function with
     keyword arguments, because that is precisely the way that it is –
     all of the OPEN-PARAMS to ‘run-server’ get passed to the
     implementation’s open function.

          ;; The defaults: localhost:8080
          (run-server handler)
          ;; Same thing
          (run-server handler 'http '())
          ;; On a different port
          (run-server handler 'http '(#:port 8081))
          ;; IPv6
          (run-server handler 'http '(#:family AF_INET6 #:port 8081))
          ;; Custom socket
          (run-server handler 'http `(#:socket ,(sudo-make-me-a-socket)))

7.3.10 Web Examples
-------------------

Well, enough about the tedious internals.  Let’s make a web application!

7.3.10.1 Hello, World!
......................

The first program we have to write, of course, is “Hello, World!”.  This
means that we have to implement a web handler that does what we want.

   Now we define a handler, a function of two arguments and two return
values:

     (define (handler request request-body)
       (values RESPONSE RESPONSE-BODY))

   In this first example, we take advantage of a short-cut, returning an
alist of headers instead of a proper response object.  The response body
is our payload:

     (define (hello-world-handler request request-body)
       (values '((content-type . (text/plain)))
               "Hello World!"))

   Now let’s test it, by running a server with this handler.  Load up
the web server module if you haven’t yet done so, and run a server with
this handler:

     (use-modules (web server))
     (run-server hello-world-handler)

   By default, the web server listens for requests on ‘localhost:8080’.
Visit that address in your web browser to test.  If you see the string,
‘Hello World!’, sweet!

7.3.10.2 Inspecting the Request
...............................

The Hello World program above is a general greeter, responding to all
URIs.  To make a more exclusive greeter, we need to inspect the request
object, and conditionally produce different results.  So let’s load up
the request, response, and URI modules, and do just that.

     (use-modules (web server)) ; you probably did this already
     (use-modules (web request)
                  (web response)
                  (web uri))

     (define (request-path-components request)
       (split-and-decode-uri-path (uri-path (request-uri request))))

     (define (hello-hacker-handler request body)
       (if (equal? (request-path-components request)
                   '("hacker"))
           (values '((content-type . (text/plain)))
                   "Hello hacker!")
           (not-found request)))

     (run-server hello-hacker-handler)

   Here we see that we have defined a helper to return the components of
the URI path as a list of strings, and used that to check for a request
to ‘/hacker/’.  Then the success case is just as before – visit
‘http://localhost:8080/hacker/’ in your browser to check.

   You should always match against URI path components as decoded by
‘split-and-decode-uri-path’.  The above example will work for
‘/hacker/’, ‘//hacker///’, and ‘/h%61ck%65r’.

   But we forgot to define ‘not-found’!  If you are pasting these
examples into a REPL, accessing any other URI in your web browser will
drop your Guile console into the debugger:

     <unnamed port>:38:7: In procedure module-lookup:
     <unnamed port>:38:7: Unbound variable: not-found

     Entering a new prompt.  Type `,bt' for a backtrace or `,q' to continue.
     scheme@(guile-user) [1]>

   So let’s define the function, right there in the debugger.  As you
probably know, we’ll want to return a 404 response.

     ;; Paste this in your REPL
     (define (not-found request)
       (values (build-response #:code 404)
               (string-append "Resource not found: "
                              (uri->string (request-uri request)))))

     ;; Now paste this to let the web server keep going:
     ,continue

   Now if you access ‘http://localhost/foo/’, you get this error
message.  (Note that some popular web browsers won’t show
server-generated 404 messages, showing their own instead, unless the 404
message body is long enough.)

7.3.10.3 Higher-Level Interfaces
................................

The web handler interface is a common baseline that all kinds of Guile
web applications can use.  You will usually want to build something on
top of it, however, especially when producing HTML. Here is a simple
example that builds up HTML output using SXML (*note SXML::).

   First, load up the modules:

     (use-modules (web server)
                  (web request)
                  (web response)
                  (sxml simple))

   Now we define a simple templating function that takes a list of HTML
body elements, as SXML, and puts them in our super template:

     (define (templatize title body)
       `(html (head (title ,title))
              (body ,@body)))

   For example, the simplest Hello HTML can be produced like this:

     (sxml->xml (templatize "Hello!" '((b "Hi!"))))
     ⊣
     <html><head><title>Hello!</title></head><body><b>Hi!</b></body></html>

   Much better to work with Scheme data types than to work with HTML as
strings.  Now we define a little response helper:

     (define* (respond #:optional body #:key
                       (status 200)
                       (title "Hello hello!")
                       (doctype "<!DOCTYPE html>\n")
                       (content-type-params '((charset . "utf-8")))
                       (content-type 'text/html)
                       (extra-headers '())
                       (sxml (and body (templatize title body))))
       (values (build-response
                #:code status
                #:headers `((content-type
                             . (,content-type ,@content-type-params))
                            ,@extra-headers))
               (lambda (port)
                 (if sxml
                     (begin
                       (if doctype (display doctype port))
                       (sxml->xml sxml port))))))

   Here we see the power of keyword arguments with default initializers.
By the time the arguments are fully parsed, the ‘sxml’ local variable
will hold the templated SXML, ready for sending out to the client.

   Also, instead of returning the body as a string, ‘respond’ gives a
procedure, which will be called by the web server to write out the
response to the client.

   Now, a simple example using this responder, which lays out the
incoming headers in an HTML table.

     (define (debug-page request body)
       (respond
        `((h1 "hello world!")
          (table
           (tr (th "header") (th "value"))
           ,@(map (lambda (pair)
                    `(tr (td (tt ,(with-output-to-string
                                    (lambda () (display (car pair))))))
                         (td (tt ,(with-output-to-string
                                    (lambda ()
                                      (write (cdr pair))))))))
                  (request-headers request))))))

     (run-server debug-page)

   Now if you visit any local address in your web browser, we actually
see some HTML, finally.

7.3.10.4 Conclusion
...................

Well, this is about as far as Guile’s built-in web support goes, for
now.  There are many ways to make a web application, but hopefully by
standardizing the most fundamental data types, users will be able to
choose the approach that suits them best, while also being able to
switch between implementations of the server.  This is a relatively new
part of Guile, so if you have feedback, let us know, and we can take it
into account.  Happy hacking on the web!

7.4 The (ice-9 getopt-long) Module
==================================

The ‘(ice-9 getopt-long)’ module exports two procedures: ‘getopt-long’
and ‘option-ref’.

   • ‘getopt-long’ takes a list of strings — the command line arguments
     — an "option specification", and some optional keyword parameters.
     It parses the command line arguments according to the option
     specification and keyword parameters, and returns a data structure
     that encapsulates the results of the parsing.

   • ‘option-ref’ then takes the parsed data structure and a specific
     option’s name, and returns information about that option in
     particular.

   To make these procedures available to your Guile script, include the
expression ‘(use-modules (ice-9 getopt-long))’ somewhere near the top,
before the first usage of ‘getopt-long’ or ‘option-ref’.

7.4.1 A Short getopt-long Example
---------------------------------

This section illustrates how ‘getopt-long’ is used by presenting and
dissecting a simple example.  The first thing that we need is an "option
specification" that tells ‘getopt-long’ how to parse the command line.
This specification is an association list with the long option name as
the key.  Here is how such a specification might look:

     (define option-spec
       '((version (single-char #\v) (value #f))
         (help    (single-char #\h) (value #f))))

   This alist tells ‘getopt-long’ that it should accept two long
options, called _version_ and _help_, and that these options can also be
selected by the single-letter abbreviations _v_ and _h_, respectively.
The ‘(value #f)’ clauses indicate that neither of the options accepts a
value.

   With this specification we can use ‘getopt-long’ to parse a given
command line:

     (define options (getopt-long (command-line) option-spec))

   After this call, ‘options’ contains the parsed command line and is
ready to be examined by ‘option-ref’.  ‘option-ref’ is called like this:

     (option-ref options 'help #f)

It expects the parsed command line, a symbol indicating the option to
examine, and a default value.  The default value is returned if the
option was not present in the command line, or if the option was present
but without a value; otherwise the value from the command line is
returned.  Usually ‘option-ref’ is called once for each possible option
that a script supports.

   The following example shows a main program which puts all this
together to parse its command line and figure out what the user wanted.

     (define (main args)
       (let* ((option-spec '((version (single-char #\v) (value #f))
                             (help    (single-char #\h) (value #f))))
              (options (getopt-long args option-spec))
              (help-wanted (option-ref options 'help #f))
              (version-wanted (option-ref options 'version #f)))
         (if (or version-wanted help-wanted)
             (begin
               (if version-wanted
                   (display "getopt-long-example version 0.3\n"))
               (if help-wanted
                   (display "\
     getopt-long-example [options]
       -v, --version    Display version
       -h, --help       Display this help
     ")))
             (begin
               (display "Hello, World!") (newline)))))

7.4.2 How to Write an Option Specification
------------------------------------------

An option specification is an association list (*note Association
Lists::) with one list element for each supported option.  The key of
each list element is a symbol that names the option, while the value is
a list of option properties:

     OPTION-SPEC ::=  '( (OPT-NAME1 (PROP-NAME PROP-VALUE) …)
                         (OPT-NAME2 (PROP-NAME PROP-VALUE) …)
                         (OPT-NAME3 (PROP-NAME PROP-VALUE) …)
                         …
                       )

   Each OPT-NAME specifies the long option name for that option.  For
example, a list element with OPT-NAME ‘background’ specifies an option
that can be specified on the command line using the long option
‘--background’.  Further information about the option — whether it takes
a value, whether it is required to be present in the command line, and
so on — is specified by the option properties.

   In the example of the preceding section, we already saw that a long
option name can have a equivalent "short option" character.  The
equivalent short option character can be set for an option by specifying
a ‘single-char’ property in that option’s property list.  For example, a
list element like ‘'(output (single-char #\o) …)’ specifies an option
with long name ‘--output’ that can also be specified by the equivalent
short name ‘-o’.

   The ‘value’ property specifies whether an option requires or accepts
a value.  If the ‘value’ property is set to ‘#t’, the option requires a
value: ‘getopt-long’ will signal an error if the option name is present
without a corresponding value.  If set to ‘#f’, the option does not take
a value; in this case, a non-option word that follows the option name in
the command line will be treated as a non-option argument.  If set to
the symbol ‘optional’, the option accepts a value but does not require
one: a non-option word that follows the option name in the command line
will be interpreted as that option’s value.  If the option name for an
option with ‘'(value optional)’ is immediately followed in the command
line by _another_ option name, the value for the first option is
implicitly ‘#t’.

   The ‘required?’ property indicates whether an option is required to
be present in the command line.  If the ‘required?’ property is set to
‘#t’, ‘getopt-long’ will signal an error if the option is not specified.

   Finally, the ‘predicate’ property can be used to constrain the
possible values of an option.  If used, the ‘predicate’ property should
be set to a procedure that takes one argument — the proposed option
value as a string — and returns either ‘#t’ or ‘#f’ according as the
proposed value is or is not acceptable.  If the predicate procedure
returns ‘#f’, ‘getopt-long’ will signal an error.

   By default, options do not have single-character equivalents, are not
required, and do not take values.  Where the list element for an option
includes a ‘value’ property but no ‘predicate’ property, the option
values are unconstrained.

7.4.3 Expected Command Line Format
----------------------------------

In order for ‘getopt-long’ to correctly parse a command line, that
command line must conform to a standard set of rules for how command
line options are specified.  This section explains what those rules are.

   ‘getopt-long’ splits a given command line into several pieces.  All
elements of the argument list are classified to be either options or
normal arguments.  Options consist of two dashes and an option name
(so-called "long" options), or of one dash followed by a single letter
("short" options).

   Options can behave as switches, when they are given without a value,
or they can be used to pass a value to the program.  The value for an
option may be specified using an equals sign, or else is simply the next
word in the command line, so the following two invocations are
equivalent:

     $ ./foo.scm --output=bar.txt
     $ ./foo.scm --output bar.txt

   Short options can be used instead of their long equivalents and can
be grouped together after a single dash.  For example, the following
commands are equivalent.

     $ ./foo.scm --version --help
     $ ./foo.scm -v --help
     $ ./foo.scm -vh

   If an option requires a value, it can only be grouped together with
other short options if it is the last option in the group; the value is
the next argument.  So, for example, with the following option
specification —

     ((apples    (single-char #\a))
      (blimps    (single-char #\b) (value #t))
      (catalexis (single-char #\c) (value #t)))

— the following command lines would all be acceptable:

     $ ./foo.scm -a -b bang -c couth
     $ ./foo.scm -ab bang -c couth
     $ ./foo.scm -ac couth -b bang

   But the next command line is an error, because ‘-b’ is not the last
option in its combination, and because a group of short options cannot
include two options that both require values:

     $ ./foo.scm -abc couth bang

   If an option’s value is optional, ‘getopt-long’ decides whether the
option has a value by looking at what follows it in the argument list.
If the next element is a string, and it does not appear to be an option
itself, then that string is the option’s value.

   If the option ‘--’ appears in the argument list, argument parsing
stops there and subsequent arguments are returned as ordinary arguments,
even if they resemble options.  So, with the command line

     $ ./foo.scm --apples "Granny Smith" -- --blimp Goodyear

‘getopt-long’ will recognize the ‘--apples’ option as having the value
"Granny Smith", but will not treat ‘--blimp’ as an option.  The strings
‘--blimp’ and ‘Goodyear’ will be returned as ordinary argument strings.

7.4.4 Reference Documentation for ‘getopt-long’
-----------------------------------------------

 -- Scheme Procedure: getopt-long args grammar
          [#:stop-at-first-non-option #t]
     Parse the command line given in ARGS (which must be a list of
     strings) according to the option specification GRAMMAR.

     The GRAMMAR argument is expected to be a list of this form:

     ‘((OPTION (PROPERTY VALUE) …) …)’

     where each OPTION is a symbol denoting the long option, but without
     the two leading dashes (e.g. ‘version’ if the option is called
     ‘--version’).

     For each option, there may be list of arbitrarily many
     property/value pairs.  The order of the pairs is not important, but
     every property may only appear once in the property list.  The
     following table lists the possible properties:

     ‘(single-char CHAR)’
          Accept ‘-CHAR’ as a single-character equivalent to ‘--OPTION’.
          This is how to specify traditional Unix-style flags.
     ‘(required? BOOL)’
          If BOOL is true, the option is required.  ‘getopt-long’ will
          raise an error if it is not found in ARGS.
     ‘(value BOOL)’
          If BOOL is ‘#t’, the option accepts a value; if it is ‘#f’, it
          does not; and if it is the symbol ‘optional’, the option may
          appear in ARGS with or without a value.
     ‘(predicate FUNC)’
          If the option accepts a value (i.e. you specified ‘(value #t)’
          for this option), then ‘getopt-long’ will apply FUNC to the
          value, and throw an exception if it returns ‘#f’.  FUNC should
          be a procedure which accepts a string and returns a boolean
          value; you may need to use quasiquotes to get it into GRAMMAR.

     The ‘#:stop-at-first-non-option’ keyword, if specified with any
     true value, tells ‘getopt-long’ to stop when it gets to the first
     non-option in the command line.  That is, at the first word which
     is neither an option itself, nor the value of an option.
     Everything in the command line from that word onwards will be
     returned as non-option arguments.

   ‘getopt-long’’s ARGS parameter is expected to be a list of strings
like the one returned by ‘command-line’, with the first element being
the name of the command.  Therefore ‘getopt-long’ ignores the first
element in ARGS and starts argument interpretation with the second
element.

   ‘getopt-long’ signals an error if any of the following conditions
hold.

   • The option grammar has an invalid syntax.

   • One of the options in the argument list was not specified by the
     grammar.

   • A required option is omitted.

   • An option which requires an argument did not get one.

   • An option that doesn’t accept an argument does get one (this can
     only happen using the long option ‘--opt=VALUE’ syntax).

   • An option predicate fails.

   ‘#:stop-at-first-non-option’ is useful for command line invocations
like ‘guild [--help | --version] [script [script-options]]’ and ‘cvs
[general-options] command [command-options]’, where there are options at
two levels: some generic and understood by the outer command, and some
that are specific to the particular script or command being invoked.  To
use ‘getopt-long’ in such cases, you would call it twice: firstly with
‘#:stop-at-first-non-option #t’, so as to parse any generic options and
identify the wanted script or sub-command; secondly, and after trimming
off the initial generic command words, with a script- or
sub-command-specific option grammar, so as to process those specific
options.

7.4.5 Reference Documentation for ‘option-ref’
----------------------------------------------

 -- Scheme Procedure: option-ref options key default
     Search OPTIONS for a command line option named KEY and return its
     value, if found.  If the option has no value, but was given, return
     ‘#t’.  If the option was not given, return DEFAULT.  OPTIONS must
     be the result of a call to ‘getopt-long’.

   ‘option-ref’ always succeeds, either by returning the requested
option value from the command line, or the default value.

   The special key ‘'()’ can be used to get a list of all non-option
arguments.

7.5 SRFI Support Modules
========================

SRFI is an acronym for Scheme Request For Implementation.  The SRFI
documents define a lot of syntactic and procedure extensions to standard
Scheme as defined in R5RS.

   Guile has support for a number of SRFIs.  This chapter gives an
overview over the available SRFIs and some usage hints.  For complete
documentation, design rationales and further examples, we advise you to
get the relevant SRFI documents from the SRFI home page
<http://srfi.schemers.org/>.

7.5.1 About SRFI Usage
----------------------

SRFI support in Guile is currently implemented partly in the core
library, and partly as add-on modules.  That means that some SRFIs are
automatically available when the interpreter is started, whereas the
other SRFIs require you to use the appropriate support module
explicitly.

   There are several reasons for this inconsistency.  First, the feature
checking syntactic form ‘cond-expand’ (*note SRFI-0::) must be available
immediately, because it must be there when the user wants to check for
the Scheme implementation, that is, before she can know that it is safe
to use ‘use-modules’ to load SRFI support modules.  The second reason is
that some features defined in SRFIs had been implemented in Guile before
the developers started to add SRFI implementations as modules (for
example SRFI-13 (*note SRFI-13::)).  In the future, it is possible that
SRFIs in the core library might be factored out into separate modules,
requiring explicit module loading when they are needed.  So you should
be prepared to have to use ‘use-modules’ someday in the future to access
SRFI-13 bindings.  If you want, you can do that already.  We have
included the module ‘(srfi srfi-13)’ in the distribution, which
currently does nothing, but ensures that you can write future-safe code.

   Generally, support for a specific SRFI is made available by using
modules named ‘(srfi srfi-NUMBER)’, where NUMBER is the number of the
SRFI needed.  Another possibility is to use the command line option
‘--use-srfi’, which will load the necessary modules automatically (*note
Invoking Guile::).

7.5.2 SRFI-0 - cond-expand
--------------------------

This SRFI lets a portable Scheme program test for the presence of
certain features, and adapt itself by using different blocks of code, or
fail if the necessary features are not available.  There’s no module to
load, this is in the Guile core.

   A program designed only for Guile will generally not need this
mechanism, such a program can of course directly use the various
documented parts of Guile.

 -- syntax: cond-expand (feature body…) …
     Expand to the BODY of the first clause whose FEATURE specification
     is satisfied.  It is an error if no FEATURE is satisfied.

     Features are symbols such as ‘srfi-1’, and a feature specification
     can use ‘and’, ‘or’ and ‘not’ forms to test combinations.  The last
     clause can be an ‘else’, to be used if no other passes.

     For example, define a private version of ‘alist-cons’ if SRFI-1 is
     not available.

          (cond-expand (srfi-1
                        )
                       (else
                        (define (alist-cons key val alist)
                          (cons (cons key val) alist))))

     Or demand a certain set of SRFIs (list operations, string ports,
     ‘receive’ and string operations), failing if they’re not available.

          (cond-expand ((and srfi-1 srfi-6 srfi-8 srfi-13)
                        ))

The Guile core has the following features,

     guile
     guile-2  ;; starting from Guile 2.x
     r5rs
     srfi-0
     srfi-4
     srfi-13
     srfi-14
     srfi-16
     srfi-23
     srfi-30
     srfi-39
     srfi-46
     srfi-55
     srfi-61
     srfi-62
     srfi-87
     srfi-105

   Other SRFI feature symbols are defined once their code has been
loaded with ‘use-modules’, since only then are their bindings available.

   The ‘--use-srfi’ command line option (*note Invoking Guile::) is a
good way to load SRFIs to satisfy ‘cond-expand’ when running a portable
program.

   Testing the ‘guile’ feature allows a program to adapt itself to the
Guile module system, but still run on other Scheme systems.  For example
the following demands SRFI-8 (‘receive’), but also knows how to load it
with the Guile mechanism.

     (cond-expand (srfi-8
                   )
                  (guile
                   (use-modules (srfi srfi-8))))

   Likewise, testing the ‘guile-2’ feature allows code to be portable
between Guile 2.0 and previous versions of Guile.  For instance, it
makes it possible to write code that accounts for Guile 2.0’s compiler,
yet be correctly interpreted on 1.8 and earlier versions:

     (cond-expand (guile-2 (eval-when (compile)
                             ;; This must be evaluated at compile time.
                             (fluid-set! current-reader my-reader)))
                  (guile
                           ;; Earlier versions of Guile do not have a
                           ;; separate compilation phase.
                           (fluid-set! current-reader my-reader)))

   It should be noted that ‘cond-expand’ is separate from the
‘*features*’ mechanism (*note Feature Tracking::), feature symbols in
one are unrelated to those in the other.

7.5.3 SRFI-1 - List library
---------------------------

The list library defined in SRFI-1 contains a lot of useful list
processing procedures for construction, examining, destructuring and
manipulating lists and pairs.

   Since SRFI-1 also defines some procedures which are already contained
in R5RS and thus are supported by the Guile core library, some list and
pair procedures which appear in the SRFI-1 document may not appear in
this section.  So when looking for a particular list/pair processing
procedure, you should also have a look at the sections *note Lists:: and
*note Pairs::.

7.5.3.1 Constructors
....................

New lists can be constructed by calling one of the following procedures.

 -- Scheme Procedure: xcons d a
     Like ‘cons’, but with interchanged arguments.  Useful mostly when
     passed to higher-order procedures.

 -- Scheme Procedure: list-tabulate n init-proc
     Return an N-element list, where each list element is produced by
     applying the procedure INIT-PROC to the corresponding list index.
     The order in which INIT-PROC is applied to the indices is not
     specified.

 -- Scheme Procedure: list-copy lst
     Return a new list containing the elements of the list LST.

     This function differs from the core ‘list-copy’ (*note List
     Constructors::) in accepting improper lists too.  And if LST is not
     a pair at all then it’s treated as the final tail of an improper
     list and simply returned.

 -- Scheme Procedure: circular-list elt1 elt2 …
     Return a circular list containing the given arguments ELT1 ELT2 ….

 -- Scheme Procedure: iota count [start step]
     Return a list containing COUNT numbers, starting from START and
     adding STEP each time.  The default START is 0, the default STEP is
     1.  For example,

          (iota 6)        ⇒ (0 1 2 3 4 5)
          (iota 4 2.5 -2) ⇒ (2.5 0.5 -1.5 -3.5)

     This function takes its name from the corresponding primitive in
     the APL language.

7.5.3.2 Predicates
..................

The procedures in this section test specific properties of lists.

 -- Scheme Procedure: proper-list? obj
     Return ‘#t’ if OBJ is a proper list, or ‘#f’ otherwise.  This is
     the same as the core ‘list?’ (*note List Predicates::).

     A proper list is a list which ends with the empty list ‘()’ in the
     usual way.  The empty list ‘()’ itself is a proper list too.

          (proper-list? '(1 2 3))  ⇒ #t
          (proper-list? '())       ⇒ #t

 -- Scheme Procedure: circular-list? obj
     Return ‘#t’ if OBJ is a circular list, or ‘#f’ otherwise.

     A circular list is a list where at some point the ‘cdr’ refers back
     to a previous pair in the list (either the start or some later
     point), so that following the ‘cdr’s takes you around in a circle,
     with no end.

          (define x (list 1 2 3 4))
          (set-cdr! (last-pair x) (cddr x))
          x ⇒ (1 2 3 4 3 4 3 4 ...)
          (circular-list? x)  ⇒ #t

 -- Scheme Procedure: dotted-list? obj
     Return ‘#t’ if OBJ is a dotted list, or ‘#f’ otherwise.

     A dotted list is a list where the ‘cdr’ of the last pair is not the
     empty list ‘()’.  Any non-pair OBJ is also considered a dotted
     list, with length zero.

          (dotted-list? '(1 2 . 3))  ⇒ #t
          (dotted-list? 99)          ⇒ #t

   It will be noted that any Scheme object passes exactly one of the
above three tests ‘proper-list?’, ‘circular-list?’ and ‘dotted-list?’.
Non-lists are ‘dotted-list?’, finite lists are either ‘proper-list?’ or
‘dotted-list?’, and infinite lists are ‘circular-list?’.


 -- Scheme Procedure: null-list? lst
     Return ‘#t’ if LST is the empty list ‘()’, ‘#f’ otherwise.  If
     something else than a proper or circular list is passed as LST, an
     error is signalled.  This procedure is recommended for checking for
     the end of a list in contexts where dotted lists are not allowed.

 -- Scheme Procedure: not-pair? obj
     Return ‘#t’ is OBJ is not a pair, ‘#f’ otherwise.  This is
     shorthand notation ‘(not (pair? OBJ))’ and is supposed to be used
     for end-of-list checking in contexts where dotted lists are
     allowed.

 -- Scheme Procedure: list= elt= list1 …
     Return ‘#t’ if all argument lists are equal, ‘#f’ otherwise.  List
     equality is determined by testing whether all lists have the same
     length and the corresponding elements are equal in the sense of the
     equality predicate ELT=.  If no or only one list is given, ‘#t’ is
     returned.

7.5.3.3 Selectors
.................

 -- Scheme Procedure: first pair
 -- Scheme Procedure: second pair
 -- Scheme Procedure: third pair
 -- Scheme Procedure: fourth pair
 -- Scheme Procedure: fifth pair
 -- Scheme Procedure: sixth pair
 -- Scheme Procedure: seventh pair
 -- Scheme Procedure: eighth pair
 -- Scheme Procedure: ninth pair
 -- Scheme Procedure: tenth pair
     These are synonyms for ‘car’, ‘cadr’, ‘caddr’, ….

 -- Scheme Procedure: car+cdr pair
     Return two values, the CAR and the CDR of PAIR.

 -- Scheme Procedure: take lst i
 -- Scheme Procedure: take! lst i
     Return a list containing the first I elements of LST.

     ‘take!’ may modify the structure of the argument list LST in order
     to produce the result.

 -- Scheme Procedure: drop lst i
     Return a list containing all but the first I elements of LST.

 -- Scheme Procedure: take-right lst i
     Return a list containing the I last elements of LST.  The return
     shares a common tail with LST.

 -- Scheme Procedure: drop-right lst i
 -- Scheme Procedure: drop-right! lst i
     Return a list containing all but the I last elements of LST.

     ‘drop-right’ always returns a new list, even when I is zero.
     ‘drop-right!’ may modify the structure of the argument list LST in
     order to produce the result.

 -- Scheme Procedure: split-at lst i
 -- Scheme Procedure: split-at! lst i
     Return two values, a list containing the first I elements of the
     list LST and a list containing the remaining elements.

     ‘split-at!’ may modify the structure of the argument list LST in
     order to produce the result.

 -- Scheme Procedure: last lst
     Return the last element of the non-empty, finite list LST.

7.5.3.4 Length, Append, Concatenate, etc.
.........................................

 -- Scheme Procedure: length+ lst
     Return the length of the argument list LST.  When LST is a circular
     list, ‘#f’ is returned.

 -- Scheme Procedure: concatenate list-of-lists
 -- Scheme Procedure: concatenate! list-of-lists
     Construct a list by appending all lists in LIST-OF-LISTS.

     ‘concatenate!’ may modify the structure of the given lists in order
     to produce the result.

     ‘concatenate’ is the same as ‘(apply append LIST-OF-LISTS)’.  It
     exists because some Scheme implementations have a limit on the
     number of arguments a function takes, which the ‘apply’ might
     exceed.  In Guile there is no such limit.

 -- Scheme Procedure: append-reverse rev-head tail
 -- Scheme Procedure: append-reverse! rev-head tail
     Reverse REV-HEAD, append TAIL to it, and return the result.  This
     is equivalent to ‘(append (reverse REV-HEAD) TAIL)’, but its
     implementation is more efficient.

          (append-reverse '(1 2 3) '(4 5 6)) ⇒ (3 2 1 4 5 6)

     ‘append-reverse!’ may modify REV-HEAD in order to produce the
     result.

 -- Scheme Procedure: zip lst1 lst2 …
     Return a list as long as the shortest of the argument lists, where
     each element is a list.  The first list contains the first elements
     of the argument lists, the second list contains the second
     elements, and so on.

 -- Scheme Procedure: unzip1 lst
 -- Scheme Procedure: unzip2 lst
 -- Scheme Procedure: unzip3 lst
 -- Scheme Procedure: unzip4 lst
 -- Scheme Procedure: unzip5 lst
     ‘unzip1’ takes a list of lists, and returns a list containing the
     first elements of each list, ‘unzip2’ returns two lists, the first
     containing the first elements of each lists and the second
     containing the second elements of each lists, and so on.

 -- Scheme Procedure: count pred lst1 lst2 …
     Return a count of the number of times PRED returns true when called
     on elements from the given lists.

     PRED is called with N parameters ‘(PRED ELEM1 … ELEMN )’, each
     element being from the corresponding list.  The first call is with
     the first element of each list, the second with the second element
     from each, and so on.

     Counting stops when the end of the shortest list is reached.  At
     least one list must be non-circular.

7.5.3.5 Fold, Unfold & Map
..........................

 -- Scheme Procedure: fold proc init lst1 lst2 …
 -- Scheme Procedure: fold-right proc init lst1 lst2 …
     Apply PROC to the elements of LST1 LST2 … to build a result, and
     return that result.

     Each PROC call is ‘(PROC ELEM1 ELEM2 … PREVIOUS)’, where ELEM1 is
     from LST1, ELEM2 is from LST2, and so on.  PREVIOUS is the return
     from the previous call to PROC, or the given INIT for the first
     call.  If any list is empty, just INIT is returned.

     ‘fold’ works through the list elements from first to last.  The
     following shows a list reversal and the calls it makes,

          (fold cons '() '(1 2 3))

          (cons 1 '())
          (cons 2 '(1))
          (cons 3 '(2 1)
          ⇒ (3 2 1)

     ‘fold-right’ works through the list elements from last to first,
     ie. from the right.  So for example the following finds the longest
     string, and the last among equal longest,

          (fold-right (lambda (str prev)
                        (if (> (string-length str) (string-length prev))
                            str
                            prev))
                      ""
                      '("x" "abc" "xyz" "jk"))
          ⇒ "xyz"

     If LST1 LST2 … have different lengths, ‘fold’ stops when the end of
     the shortest is reached; ‘fold-right’ commences at the last element
     of the shortest.  Ie. elements past the length of the shortest are
     ignored in the other LSTs.  At least one LST must be non-circular.

     ‘fold’ should be preferred over ‘fold-right’ if the order of
     processing doesn’t matter, or can be arranged either way, since
     ‘fold’ is a little more efficient.

     The way ‘fold’ builds a result from iterating is quite general, it
     can do more than other iterations like say ‘map’ or ‘filter’.  The
     following for example removes adjacent duplicate elements from a
     list,

          (define (delete-adjacent-duplicates lst)
            (fold-right (lambda (elem ret)
                          (if (equal? elem (first ret))
                              ret
                              (cons elem ret)))
                        (list (last lst))
                        lst))
          (delete-adjacent-duplicates '(1 2 3 3 4 4 4 5))
          ⇒ (1 2 3 4 5)

     Clearly the same sort of thing can be done with a ‘for-each’ and a
     variable in which to build the result, but a self-contained PROC
     can be re-used in multiple contexts, where a ‘for-each’ would have
     to be written out each time.

 -- Scheme Procedure: pair-fold proc init lst1 lst2 …
 -- Scheme Procedure: pair-fold-right proc init lst1 lst2 …
     The same as ‘fold’ and ‘fold-right’, but apply PROC to the pairs of
     the lists instead of the list elements.

 -- Scheme Procedure: reduce proc default lst
 -- Scheme Procedure: reduce-right proc default lst
     ‘reduce’ is a variant of ‘fold’, where the first call to PROC is on
     two elements from LST, rather than one element and a given initial
     value.

     If LST is empty, ‘reduce’ returns DEFAULT (this is the only use for
     DEFAULT).  If LST has just one element then that’s the return
     value.  Otherwise PROC is called on the elements of LST.

     Each PROC call is ‘(PROC ELEM PREVIOUS)’, where ELEM is from LST
     (the second and subsequent elements of LST), and PREVIOUS is the
     return from the previous call to PROC.  The first element of LST is
     the PREVIOUS for the first call to PROC.

     For example, the following adds a list of numbers, the calls made
     to ‘+’ are shown.  (Of course ‘+’ accepts multiple arguments and
     can add a list directly, with ‘apply’.)

          (reduce + 0 '(5 6 7)) ⇒ 18

          (+ 6 5)  ⇒ 11
          (+ 7 11) ⇒ 18

     ‘reduce’ can be used instead of ‘fold’ where the INIT value is an
     “identity”, meaning a value which under PROC doesn’t change the
     result, in this case 0 is an identity since ‘(+ 5 0)’ is just 5.
     ‘reduce’ avoids that unnecessary call.

     ‘reduce-right’ is a similar variation on ‘fold-right’, working from
     the end (ie. the right) of LST.  The last element of LST is the
     PREVIOUS for the first call to PROC, and the ELEM values go from
     the second last.

     ‘reduce’ should be preferred over ‘reduce-right’ if the order of
     processing doesn’t matter, or can be arranged either way, since
     ‘reduce’ is a little more efficient.

 -- Scheme Procedure: unfold p f g seed [tail-gen]
     ‘unfold’ is defined as follows:

          (unfold p f g seed) =
             (if (p seed) (tail-gen seed)
                 (cons (f seed)
                       (unfold p f g (g seed))))

     P
          Determines when to stop unfolding.

     F
          Maps each seed value to the corresponding list element.

     G
          Maps each seed value to next seed value.

     SEED
          The state value for the unfold.

     TAIL-GEN
          Creates the tail of the list; defaults to ‘(lambda (x) '())’.

     G produces a series of seed values, which are mapped to list
     elements by F.  These elements are put into a list in left-to-right
     order, and P tells when to stop unfolding.

 -- Scheme Procedure: unfold-right p f g seed [tail]
     Construct a list with the following loop.

          (let lp ((seed seed) (lis tail))
             (if (p seed) lis
                 (lp (g seed)
                     (cons (f seed) lis))))

     P
          Determines when to stop unfolding.

     F
          Maps each seed value to the corresponding list element.

     G
          Maps each seed value to next seed value.

     SEED
          The state value for the unfold.

     TAIL
          The tail of the list; defaults to ‘'()’.

 -- Scheme Procedure: map f lst1 lst2 …
     Map the procedure over the list(s) LST1, LST2, … and return a list
     containing the results of the procedure applications.  This
     procedure is extended with respect to R5RS, because the argument
     lists may have different lengths.  The result list will have the
     same length as the shortest argument lists.  The order in which F
     will be applied to the list element(s) is not specified.

 -- Scheme Procedure: for-each f lst1 lst2 …
     Apply the procedure F to each pair of corresponding elements of the
     list(s) LST1, LST2, ….  The return value is not specified.  This
     procedure is extended with respect to R5RS, because the argument
     lists may have different lengths.  The shortest argument list
     determines the number of times F is called.  F will be applied to
     the list elements in left-to-right order.

 -- Scheme Procedure: append-map f lst1 lst2 …
 -- Scheme Procedure: append-map! f lst1 lst2 …
     Equivalent to

          (apply append (map f clist1 clist2 ...))

     and

          (apply append! (map f clist1 clist2 ...))

     Map F over the elements of the lists, just as in the ‘map’
     function.  However, the results of the applications are appended
     together to make the final result.  ‘append-map’ uses ‘append’ to
     append the results together; ‘append-map!’ uses ‘append!’.

     The dynamic order in which the various applications of F are made
     is not specified.

 -- Scheme Procedure: map! f lst1 lst2 …
     Linear-update variant of ‘map’ – ‘map!’ is allowed, but not
     required, to alter the cons cells of LST1 to construct the result
     list.

     The dynamic order in which the various applications of F are made
     is not specified.  In the n-ary case, LST2, LST3, … must have at
     least as many elements as LST1.

 -- Scheme Procedure: pair-for-each f lst1 lst2 …
     Like ‘for-each’, but applies the procedure F to the pairs from
     which the argument lists are constructed, instead of the list
     elements.  The return value is not specified.

 -- Scheme Procedure: filter-map f lst1 lst2 …
     Like ‘map’, but only results from the applications of F which are
     true are saved in the result list.

7.5.3.6 Filtering and Partitioning
..................................

Filtering means to collect all elements from a list which satisfy a
specific condition.  Partitioning a list means to make two groups of
list elements, one which contains the elements satisfying a condition,
and the other for the elements which don’t.

   The ‘filter’ and ‘filter!’ functions are implemented in the Guile
core, *Note List Modification::.

 -- Scheme Procedure: partition pred lst
 -- Scheme Procedure: partition! pred lst
     Split LST into those elements which do and don’t satisfy the
     predicate PRED.

     The return is two values (*note Multiple Values::), the first being
     a list of all elements from LST which satisfy PRED, the second a
     list of those which do not.

     The elements in the result lists are in the same order as in LST
     but the order in which the calls ‘(PRED elem)’ are made on the list
     elements is unspecified.

     ‘partition’ does not change LST, but one of the returned lists may
     share a tail with it.  ‘partition!’ may modify LST to construct its
     return.

 -- Scheme Procedure: remove pred lst
 -- Scheme Procedure: remove! pred lst
     Return a list containing all elements from LST which do not satisfy
     the predicate PRED.  The elements in the result list have the same
     order as in LST.  The order in which PRED is applied to the list
     elements is not specified.

     ‘remove!’ is allowed, but not required to modify the structure of
     the input list.

7.5.3.7 Searching
.................

The procedures for searching elements in lists either accept a predicate
or a comparison object for determining which elements are to be
searched.

 -- Scheme Procedure: find pred lst
     Return the first element of LST which satisfies the predicate PRED
     and ‘#f’ if no such element is found.

 -- Scheme Procedure: find-tail pred lst
     Return the first pair of LST whose CAR satisfies the predicate PRED
     and ‘#f’ if no such element is found.

 -- Scheme Procedure: take-while pred lst
 -- Scheme Procedure: take-while! pred lst
     Return the longest initial prefix of LST whose elements all satisfy
     the predicate PRED.

     ‘take-while!’ is allowed, but not required to modify the input list
     while producing the result.

 -- Scheme Procedure: drop-while pred lst
     Drop the longest initial prefix of LST whose elements all satisfy
     the predicate PRED.

 -- Scheme Procedure: span pred lst
 -- Scheme Procedure: span! pred lst
 -- Scheme Procedure: break pred lst
 -- Scheme Procedure: break! pred lst
     ‘span’ splits the list LST into the longest initial prefix whose
     elements all satisfy the predicate PRED, and the remaining tail.
     ‘break’ inverts the sense of the predicate.

     ‘span!’ and ‘break!’ are allowed, but not required to modify the
     structure of the input list LST in order to produce the result.

     Note that the name ‘break’ conflicts with the ‘break’ binding
     established by ‘while’ (*note while do::).  Applications wanting to
     use ‘break’ from within a ‘while’ loop will need to make a new
     define under a different name.

 -- Scheme Procedure: any pred lst1 lst2 …
     Test whether any set of elements from LST1 LST2 … satisfies PRED.
     If so, the return value is the return value from the successful
     PRED call, or if not, the return value is ‘#f’.

     If there are n list arguments, then PRED must be a predicate taking
     n arguments.  Each PRED call is ‘(PRED ELEM1 ELEM2 … )’ taking an
     element from each LST.  The calls are made successively for the
     first, second, etc.  elements of the lists, stopping when PRED
     returns non-‘#f’, or when the end of the shortest list is reached.

     The PRED call on the last set of elements (i.e., when the end of
     the shortest list has been reached), if that point is reached, is a
     tail call.

 -- Scheme Procedure: every pred lst1 lst2 …
     Test whether every set of elements from LST1 LST2 … satisfies PRED.
     If so, the return value is the return from the final PRED call, or
     if not, the return value is ‘#f’.

     If there are n list arguments, then PRED must be a predicate taking
     n arguments.  Each PRED call is ‘(PRED ELEM1 ELEM2 …)’ taking an
     element from each LST.  The calls are made successively for the
     first, second, etc.  elements of the lists, stopping if PRED
     returns ‘#f’, or when the end of any of the lists is reached.

     The PRED call on the last set of elements (i.e., when the end of
     the shortest list has been reached) is a tail call.

     If one of LST1 LST2 …is empty then no calls to PRED are made, and
     the return value is ‘#t’.

 -- Scheme Procedure: list-index pred lst1 lst2 …
     Return the index of the first set of elements, one from each of
     LST1 LST2 …, which satisfies PRED.

     PRED is called as ‘(ELEM1 ELEM2 …)’.  Searching stops when the end
     of the shortest LST is reached.  The return index starts from 0 for
     the first set of elements.  If no set of elements pass, then the
     return value is ‘#f’.

          (list-index odd? '(2 4 6 9))      ⇒ 3
          (list-index = '(1 2 3) '(3 1 2))  ⇒ #f

 -- Scheme Procedure: member x lst [=]
     Return the first sublist of LST whose CAR is equal to X.  If X does
     not appear in LST, return ‘#f’.

     Equality is determined by ‘equal?’, or by the equality predicate =
     if given.  = is called ‘(= X elem)’, ie. with the given X first, so
     for example to find the first element greater than 5,

          (member 5 '(3 5 1 7 2 9) <) ⇒ (7 2 9)

     This version of ‘member’ extends the core ‘member’ (*note List
     Searching::) by accepting an equality predicate.

7.5.3.8 Deleting
................

 -- Scheme Procedure: delete x lst [=]
 -- Scheme Procedure: delete! x lst [=]
     Return a list containing the elements of LST but with those equal
     to X deleted.  The returned elements will be in the same order as
     they were in LST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  An equality call is made just once for each element, but
     the order in which the calls are made on the elements is
     unspecified.

     The equality calls are always ‘(= x elem)’, ie. the given X is
     first.  This means for instance elements greater than 5 can be
     deleted with ‘(delete 5 lst <)’.

     ‘delete’ does not modify LST, but the return might share a common
     tail with LST.  ‘delete!’ may modify the structure of LST to
     construct its return.

     These functions extend the core ‘delete’ and ‘delete!’ (*note List
     Modification::) in accepting an equality predicate.  See also
     ‘lset-difference’ (*note SRFI-1 Set Operations::) for deleting
     multiple elements from a list.

 -- Scheme Procedure: delete-duplicates lst [=]
 -- Scheme Procedure: delete-duplicates! lst [=]
     Return a list containing the elements of LST but without
     duplicates.

     When elements are equal, only the first in LST is retained.  Equal
     elements can be anywhere in LST, they don’t have to be adjacent.
     The returned list will have the retained elements in the same order
     as they were in LST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  Calls ‘(= x y)’ are made with element X being before Y in
     LST.  A call is made at most once for each combination, but the
     sequence of the calls across the elements is unspecified.

     ‘delete-duplicates’ does not modify LST, but the return might share
     a common tail with LST.  ‘delete-duplicates!’ may modify the
     structure of LST to construct its return.

     In the worst case, this is an O(N^2) algorithm because it must
     check each element against all those preceding it.  For long lists
     it is more efficient to sort and then compare only adjacent
     elements.

7.5.3.9 Association Lists
.........................

Association lists are described in detail in section *note Association
Lists::.  The present section only documents the additional procedures
for dealing with association lists defined by SRFI-1.

 -- Scheme Procedure: assoc key alist [=]
     Return the pair from ALIST which matches KEY.  This extends the
     core ‘assoc’ (*note Retrieving Alist Entries::) by taking an
     optional = comparison procedure.

     The default comparison is ‘equal?’.  If an = parameter is given
     it’s called ‘(= KEY ALISTCAR)’, i.e. the given target KEY is the
     first argument, and a ‘car’ from ALIST is second.

     For example a case-insensitive string lookup,

          (assoc "yy" '(("XX" . 1) ("YY" . 2)) string-ci=?)
          ⇒ ("YY" . 2)

 -- Scheme Procedure: alist-cons key datum alist
     Cons a new association KEY and DATUM onto ALIST and return the
     result.  This is equivalent to

          (cons (cons KEY DATUM) ALIST)

     ‘acons’ (*note Adding or Setting Alist Entries::) in the Guile core
     does the same thing.

 -- Scheme Procedure: alist-copy alist
     Return a newly allocated copy of ALIST, that means that the spine
     of the list as well as the pairs are copied.

 -- Scheme Procedure: alist-delete key alist [=]
 -- Scheme Procedure: alist-delete! key alist [=]
     Return a list containing the elements of ALIST but with those
     elements whose keys are equal to KEY deleted.  The returned
     elements will be in the same order as they were in ALIST.

     Equality is determined by the = predicate, or ‘equal?’ if not
     given.  The order in which elements are tested is unspecified, but
     each equality call is made ‘(= key alistkey)’, i.e. the given KEY
     parameter is first and the key from ALIST second.  This means for
     instance all associations with a key greater than 5 can be removed
     with ‘(alist-delete 5 alist <)’.

     ‘alist-delete’ does not modify ALIST, but the return might share a
     common tail with ALIST.  ‘alist-delete!’ may modify the list
     structure of ALIST to construct its return.

7.5.3.10 Set Operations on Lists
................................

Lists can be used to represent sets of objects.  The procedures in this
section operate on such lists as sets.

   Note that lists are not an efficient way to implement large sets.
The procedures here typically take time MxN when operating on M and N
element lists.  Other data structures like trees, bitsets (*note Bit
Vectors::) or hash tables (*note Hash Tables::) are faster.

   All these procedures take an equality predicate as the first
argument.  This predicate is used for testing the objects in the list
sets for sameness.  This predicate must be consistent with ‘eq?’ (*note
Equality::) in the sense that if two list elements are ‘eq?’ then they
must also be equal under the predicate.  This simply means a given
object must be equal to itself.

 -- Scheme Procedure: lset<= = list …
     Return ‘#t’ if each list is a subset of the one following it.
     I.e., LIST1 is a subset of LIST2, LIST2 is a subset of LIST3, etc.,
     for as many lists as given.  If only one list or no lists are
     given, the return value is ‘#t’.

     A list X is a subset of Y if each element of X is equal to some
     element in Y.  Elements are compared using the given = procedure,
     called as ‘(= xelem yelem)’.

          (lset<= eq?)                      ⇒ #t
          (lset<= eqv? '(1 2 3) '(1))       ⇒ #f
          (lset<= eqv? '(1 3 2) '(4 3 1 2)) ⇒ #t

 -- Scheme Procedure: lset= = list …
     Return ‘#t’ if all argument lists are set-equal.  LIST1 is compared
     to LIST2, LIST2 to LIST3, etc., for as many lists as given.  If
     only one list or no lists are given, the return value is ‘#t’.

     Two lists X and Y are set-equal if each element of X is equal to
     some element of Y and conversely each element of Y is equal to some
     element of X.  The order of the elements in the lists doesn’t
     matter.  Element equality is determined with the given = procedure,
     called as ‘(= xelem yelem)’, but exactly which calls are made is
     unspecified.

          (lset= eq?)                      ⇒ #t
          (lset= eqv? '(1 2 3) '(3 2 1))   ⇒ #t
          (lset= string-ci=? '("a" "A" "b") '("B" "b" "a")) ⇒ #t

 -- Scheme Procedure: lset-adjoin = list elem …
     Add to LIST any of the given ELEMs not already in the list.  ELEMs
     are ‘cons’ed onto the start of LIST (so the return value shares a
     common tail with LIST), but the order that the ELEMs are added is
     unspecified.

     The given = procedure is used for comparing elements, called as ‘(=
     listelem elem)’, i.e., the second argument is one of the given ELEM
     parameters.

          (lset-adjoin eqv? '(1 2 3) 4 1 5) ⇒ (5 4 1 2 3)

 -- Scheme Procedure: lset-union = list …
 -- Scheme Procedure: lset-union! = list …
     Return the union of the argument list sets.  The result is built by
     taking the union of LIST1 and LIST2, then the union of that with
     LIST3, etc., for as many lists as given.  For one list argument
     that list itself is the result, for no list arguments the result is
     the empty list.

     The union of two lists X and Y is formed as follows.  If X is empty
     then the result is Y.  Otherwise start with X as the result and
     consider each Y element (from first to last).  A Y element not
     equal to something already in the result is ‘cons’ed onto the
     result.

     The given = procedure is used for comparing elements, called as ‘(=
     relem yelem)’.  The first argument is from the result accumulated
     so far, and the second is from the list being union-ed in.  But
     exactly which calls are made is otherwise unspecified.

     Notice that duplicate elements in LIST1 (or the first non-empty
     list) are preserved, but that repeated elements in subsequent lists
     are only added once.

          (lset-union eqv?)                          ⇒ ()
          (lset-union eqv? '(1 2 3))                 ⇒ (1 2 3)
          (lset-union eqv? '(1 2 1 3) '(2 4 5) '(5)) ⇒ (5 4 1 2 1 3)

     ‘lset-union’ doesn’t change the given lists but the result may
     share a tail with the first non-empty list.  ‘lset-union!’ can
     modify all of the given lists to form the result.

 -- Scheme Procedure: lset-intersection = list1 list2 …
 -- Scheme Procedure: lset-intersection! = list1 list2 …
     Return the intersection of LIST1 with the other argument lists,
     meaning those elements of LIST1 which are also in all of LIST2 etc.
     For one list argument, just that list is returned.

     The test for an element of LIST1 to be in the return is simply that
     it’s equal to some element in each of LIST2 etc.  Notice this means
     an element appearing twice in LIST1 but only once in each of LIST2
     etc will go into the return twice.  The return has its elements in
     the same order as they were in LIST1.

     The given = procedure is used for comparing elements, called as ‘(=
     elem1 elemN)’.  The first argument is from LIST1 and the second is
     from one of the subsequent lists.  But exactly which calls are made
     and in what order is unspecified.

          (lset-intersection eqv? '(x y))                        ⇒ (x y)
          (lset-intersection eqv? '(1 2 3) '(4 3 2))             ⇒ (2 3)
          (lset-intersection eqv? '(1 1 2 2) '(1 2) '(2 1) '(2)) ⇒ (2 2)

     The return from ‘lset-intersection’ may share a tail with LIST1.
     ‘lset-intersection!’ may modify LIST1 to form its result.

 -- Scheme Procedure: lset-difference = list1 list2 …
 -- Scheme Procedure: lset-difference! = list1 list2 …
     Return LIST1 with any elements in LIST2, LIST3 etc removed (ie.
     subtracted).  For one list argument, just that list is returned.

     The given = procedure is used for comparing elements, called as ‘(=
     elem1 elemN)’.  The first argument is from LIST1 and the second
     from one of the subsequent lists.  But exactly which calls are made
     and in what order is unspecified.

          (lset-difference eqv? '(x y))             ⇒ (x y)
          (lset-difference eqv? '(1 2 3) '(3 1))    ⇒ (2)
          (lset-difference eqv? '(1 2 3) '(3) '(2)) ⇒ (1)

     The return from ‘lset-difference’ may share a tail with LIST1.
     ‘lset-difference!’ may modify LIST1 to form its result.

 -- Scheme Procedure: lset-diff+intersection = list1 list2 …
 -- Scheme Procedure: lset-diff+intersection! = list1 list2 …
     Return two values (*note Multiple Values::), the difference and
     intersection of the argument lists as per ‘lset-difference’ and
     ‘lset-intersection’ above.

     For two list arguments this partitions LIST1 into those elements of
     LIST1 which are in LIST2 and not in LIST2.  (But for more than two
     arguments there can be elements of LIST1 which are neither part of
     the difference nor the intersection.)

     One of the return values from ‘lset-diff+intersection’ may share a
     tail with LIST1.  ‘lset-diff+intersection!’ may modify LIST1 to
     form its results.

 -- Scheme Procedure: lset-xor = list …
 -- Scheme Procedure: lset-xor! = list …
     Return an XOR of the argument lists.  For two lists this means
     those elements which are in exactly one of the lists.  For more
     than two lists it means those elements which appear in an odd
     number of the lists.

     To be precise, the XOR of two lists X and Y is formed by taking
     those elements of X not equal to any element of Y, plus those
     elements of Y not equal to any element of X.  Equality is
     determined with the given = procedure, called as ‘(= e1 e2)’.  One
     argument is from X and the other from Y, but which way around is
     unspecified.  Exactly which calls are made is also unspecified, as
     is the order of the elements in the result.

          (lset-xor eqv? '(x y))             ⇒ (x y)
          (lset-xor eqv? '(1 2 3) '(4 3 2))  ⇒ (4 1)

     The return from ‘lset-xor’ may share a tail with one of the list
     arguments.  ‘lset-xor!’ may modify LIST1 to form its result.

7.5.4 SRFI-2 - and-let*
-----------------------

The following syntax can be obtained with

     (use-modules (srfi srfi-2))

   or alternatively

     (use-modules (ice-9 and-let-star))

 -- library syntax: and-let* (clause …) body …
     A combination of ‘and’ and ‘let*’.

     Each CLAUSE is evaluated in turn, and if ‘#f’ is obtained then
     evaluation stops and ‘#f’ is returned.  If all are non-‘#f’ then
     BODY is evaluated and the last form gives the return value, or if
     BODY is empty then the result is ‘#t’.  Each CLAUSE should be one
     of the following,

     ‘(symbol expr)’
          Evaluate EXPR, check for ‘#f’, and bind it to SYMBOL.  Like
          ‘let*’, that binding is available to subsequent clauses.
     ‘(expr)’
          Evaluate EXPR and check for ‘#f’.
     ‘symbol’
          Get the value bound to SYMBOL and check for ‘#f’.

     Notice that ‘(expr)’ has an “extra” pair of parentheses, for
     instance ‘((eq? x y))’.  One way to remember this is to imagine the
     ‘symbol’ in ‘(symbol expr)’ is omitted.

     ‘and-let*’ is good for calculations where a ‘#f’ value means
     termination, but where a non-‘#f’ value is going to be needed in
     subsequent expressions.

     The following illustrates this, it returns text between brackets
     ‘[...]’ in a string, or ‘#f’ if there are no such brackets (ie.
     either ‘string-index’ gives ‘#f’).

          (define (extract-brackets str)
            (and-let* ((start (string-index str #\[))
                       (end   (string-index str #\] start)))
              (substring str (1+ start) end)))

     The following shows plain variables and expressions tested too.
     ‘diagnostic-levels’ is taken to be an alist associating a
     diagnostic type with a level.  ‘str’ is printed only if the type is
     known and its level is high enough.

          (define (show-diagnostic type str)
            (and-let* (want-diagnostics
                       (level (assq-ref diagnostic-levels type))
                       ((>= level current-diagnostic-level)))
              (display str)))

     The advantage of ‘and-let*’ is that an extended sequence of
     expressions and tests doesn’t require lots of nesting as would
     arise from separate ‘and’ and ‘let*’, or from ‘cond’ with ‘=>’.

7.5.5 SRFI-4 - Homogeneous numeric vector datatypes
---------------------------------------------------

SRFI-4 provides an interface to uniform numeric vectors: vectors whose
elements are all of a single numeric type.  Guile offers uniform numeric
vectors for signed and unsigned 8-bit, 16-bit, 32-bit, and 64-bit
integers, two sizes of floating point values, and, as an extension to
SRFI-4, complex floating-point numbers of these two sizes.

   The standard SRFI-4 procedures and data types may be included via
loading the appropriate module:

     (use-modules (srfi srfi-4))

   This module is currently a part of the default Guile environment, but
it is a good practice to explicitly import the module.  In the future,
using SRFI-4 procedures without importing the SRFI-4 module will cause a
deprecation message to be printed.  (Of course, one may call the C
functions at any time.  Would that C had modules!)

7.5.5.1 SRFI-4 - Overview
.........................

Uniform numeric vectors can be useful since they consume less memory
than the non-uniform, general vectors.  Also, since the types they can
store correspond directly to C types, it is easier to work with them
efficiently on a low level.  Consider image processing as an example,
where you want to apply a filter to some image.  While you could store
the pixels of an image in a general vector and write a general
convolution function, things are much more efficient with uniform
vectors: the convolution function knows that all pixels are unsigned
8-bit values (say), and can use a very tight inner loop.

   This is implemented in Scheme by having the compiler notice calls to
the SRFI-4 accessors, and inline them to appropriate compiled code.
From C you have access to the raw array; functions for efficiently
working with uniform numeric vectors from C are listed at the end of
this section.

   Uniform numeric vectors are the special case of one dimensional
uniform numeric arrays.

   There are 12 standard kinds of uniform numeric vectors, and they all
have their own complement of constructors, accessors, and so on.
Procedures that operate on a specific kind of uniform numeric vector
have a “tag” in their name, indicating the element type.

u8
     unsigned 8-bit integers

s8
     signed 8-bit integers

u16
     unsigned 16-bit integers

s16
     signed 16-bit integers

u32
     unsigned 32-bit integers

s32
     signed 32-bit integers

u64
     unsigned 64-bit integers

s64
     signed 64-bit integers

f32
     the C type ‘float’

f64
     the C type ‘double’

   In addition, Guile supports uniform arrays of complex numbers, with
the nonstandard tags:

c32
     complex numbers in rectangular form with the real and imaginary
     part being a ‘float’

c64
     complex numbers in rectangular form with the real and imaginary
     part being a ‘double’

   The external representation (ie. read syntax) for these vectors is
similar to normal Scheme vectors, but with an additional tag from the
tables above indicating the vector’s type.  For example,

     #u16(1 2 3)
     #f64(3.1415 2.71)

   Note that the read syntax for floating-point here conflicts with ‘#f’
for false.  In Standard Scheme one can write ‘(1 #f3)’ for a three
element list ‘(1 #f 3)’, but for Guile ‘(1 #f3)’ is invalid.  ‘(1 #f 3)’
is almost certainly what one should write anyway to make the intention
clear, so this is rarely a problem.

7.5.5.2 SRFI-4 - API
....................

Note that the c32 and c64 functions are only available from (srfi srfi-4
gnu).

 -- Scheme Procedure: u8vector? obj
 -- Scheme Procedure: s8vector? obj
 -- Scheme Procedure: u16vector? obj
 -- Scheme Procedure: s16vector? obj
 -- Scheme Procedure: u32vector? obj
 -- Scheme Procedure: s32vector? obj
 -- Scheme Procedure: u64vector? obj
 -- Scheme Procedure: s64vector? obj
 -- Scheme Procedure: f32vector? obj
 -- Scheme Procedure: f64vector? obj
 -- Scheme Procedure: c32vector? obj
 -- Scheme Procedure: c64vector? obj
 -- C Function: scm_u8vector_p (obj)
 -- C Function: scm_s8vector_p (obj)
 -- C Function: scm_u16vector_p (obj)
 -- C Function: scm_s16vector_p (obj)
 -- C Function: scm_u32vector_p (obj)
 -- C Function: scm_s32vector_p (obj)
 -- C Function: scm_u64vector_p (obj)
 -- C Function: scm_s64vector_p (obj)
 -- C Function: scm_f32vector_p (obj)
 -- C Function: scm_f64vector_p (obj)
 -- C Function: scm_c32vector_p (obj)
 -- C Function: scm_c64vector_p (obj)
     Return ‘#t’ if OBJ is a homogeneous numeric vector of the indicated
     type.

 -- Scheme Procedure: make-u8vector n [value]
 -- Scheme Procedure: make-s8vector n [value]
 -- Scheme Procedure: make-u16vector n [value]
 -- Scheme Procedure: make-s16vector n [value]
 -- Scheme Procedure: make-u32vector n [value]
 -- Scheme Procedure: make-s32vector n [value]
 -- Scheme Procedure: make-u64vector n [value]
 -- Scheme Procedure: make-s64vector n [value]
 -- Scheme Procedure: make-f32vector n [value]
 -- Scheme Procedure: make-f64vector n [value]
 -- Scheme Procedure: make-c32vector n [value]
 -- Scheme Procedure: make-c64vector n [value]
 -- C Function: scm_make_u8vector (n, value)
 -- C Function: scm_make_s8vector (n, value)
 -- C Function: scm_make_u16vector (n, value)
 -- C Function: scm_make_s16vector (n, value)
 -- C Function: scm_make_u32vector (n, value)
 -- C Function: scm_make_s32vector (n, value)
 -- C Function: scm_make_u64vector (n, value)
 -- C Function: scm_make_s64vector (n, value)
 -- C Function: scm_make_f32vector (n, value)
 -- C Function: scm_make_f64vector (n, value)
 -- C Function: scm_make_c32vector (n, value)
 -- C Function: scm_make_c64vector (n, value)
     Return a newly allocated homogeneous numeric vector holding N
     elements of the indicated type.  If VALUE is given, the vector is
     initialized with that value, otherwise the contents are
     unspecified.

 -- Scheme Procedure: u8vector value …
 -- Scheme Procedure: s8vector value …
 -- Scheme Procedure: u16vector value …
 -- Scheme Procedure: s16vector value …
 -- Scheme Procedure: u32vector value …
 -- Scheme Procedure: s32vector value …
 -- Scheme Procedure: u64vector value …
 -- Scheme Procedure: s64vector value …
 -- Scheme Procedure: f32vector value …
 -- Scheme Procedure: f64vector value …
 -- Scheme Procedure: c32vector value …
 -- Scheme Procedure: c64vector value …
 -- C Function: scm_u8vector (values)
 -- C Function: scm_s8vector (values)
 -- C Function: scm_u16vector (values)
 -- C Function: scm_s16vector (values)
 -- C Function: scm_u32vector (values)
 -- C Function: scm_s32vector (values)
 -- C Function: scm_u64vector (values)
 -- C Function: scm_s64vector (values)
 -- C Function: scm_f32vector (values)
 -- C Function: scm_f64vector (values)
 -- C Function: scm_c32vector (values)
 -- C Function: scm_c64vector (values)
     Return a newly allocated homogeneous numeric vector of the
     indicated type, holding the given parameter VALUEs.  The vector
     length is the number of parameters given.

 -- Scheme Procedure: u8vector-length vec
 -- Scheme Procedure: s8vector-length vec
 -- Scheme Procedure: u16vector-length vec
 -- Scheme Procedure: s16vector-length vec
 -- Scheme Procedure: u32vector-length vec
 -- Scheme Procedure: s32vector-length vec
 -- Scheme Procedure: u64vector-length vec
 -- Scheme Procedure: s64vector-length vec
 -- Scheme Procedure: f32vector-length vec
 -- Scheme Procedure: f64vector-length vec
 -- Scheme Procedure: c32vector-length vec
 -- Scheme Procedure: c64vector-length vec
 -- C Function: scm_u8vector_length (vec)
 -- C Function: scm_s8vector_length (vec)
 -- C Function: scm_u16vector_length (vec)
 -- C Function: scm_s16vector_length (vec)
 -- C Function: scm_u32vector_length (vec)
 -- C Function: scm_s32vector_length (vec)
 -- C Function: scm_u64vector_length (vec)
 -- C Function: scm_s64vector_length (vec)
 -- C Function: scm_f32vector_length (vec)
 -- C Function: scm_f64vector_length (vec)
 -- C Function: scm_c32vector_length (vec)
 -- C Function: scm_c64vector_length (vec)
     Return the number of elements in VEC.

 -- Scheme Procedure: u8vector-ref vec i
 -- Scheme Procedure: s8vector-ref vec i
 -- Scheme Procedure: u16vector-ref vec i
 -- Scheme Procedure: s16vector-ref vec i
 -- Scheme Procedure: u32vector-ref vec i
 -- Scheme Procedure: s32vector-ref vec i
 -- Scheme Procedure: u64vector-ref vec i
 -- Scheme Procedure: s64vector-ref vec i
 -- Scheme Procedure: f32vector-ref vec i
 -- Scheme Procedure: f64vector-ref vec i
 -- Scheme Procedure: c32vector-ref vec i
 -- Scheme Procedure: c64vector-ref vec i
 -- C Function: scm_u8vector_ref (vec, i)
 -- C Function: scm_s8vector_ref (vec, i)
 -- C Function: scm_u16vector_ref (vec, i)
 -- C Function: scm_s16vector_ref (vec, i)
 -- C Function: scm_u32vector_ref (vec, i)
 -- C Function: scm_s32vector_ref (vec, i)
 -- C Function: scm_u64vector_ref (vec, i)
 -- C Function: scm_s64vector_ref (vec, i)
 -- C Function: scm_f32vector_ref (vec, i)
 -- C Function: scm_f64vector_ref (vec, i)
 -- C Function: scm_c32vector_ref (vec, i)
 -- C Function: scm_c64vector_ref (vec, i)
     Return the element at index I in VEC.  The first element in VEC is
     index 0.

 -- Scheme Procedure: u8vector-set! vec i value
 -- Scheme Procedure: s8vector-set! vec i value
 -- Scheme Procedure: u16vector-set! vec i value
 -- Scheme Procedure: s16vector-set! vec i value
 -- Scheme Procedure: u32vector-set! vec i value
 -- Scheme Procedure: s32vector-set! vec i value
 -- Scheme Procedure: u64vector-set! vec i value
 -- Scheme Procedure: s64vector-set! vec i value
 -- Scheme Procedure: f32vector-set! vec i value
 -- Scheme Procedure: f64vector-set! vec i value
 -- Scheme Procedure: c32vector-set! vec i value
 -- Scheme Procedure: c64vector-set! vec i value
 -- C Function: scm_u8vector_set_x (vec, i, value)
 -- C Function: scm_s8vector_set_x (vec, i, value)
 -- C Function: scm_u16vector_set_x (vec, i, value)
 -- C Function: scm_s16vector_set_x (vec, i, value)
 -- C Function: scm_u32vector_set_x (vec, i, value)
 -- C Function: scm_s32vector_set_x (vec, i, value)
 -- C Function: scm_u64vector_set_x (vec, i, value)
 -- C Function: scm_s64vector_set_x (vec, i, value)
 -- C Function: scm_f32vector_set_x (vec, i, value)
 -- C Function: scm_f64vector_set_x (vec, i, value)
 -- C Function: scm_c32vector_set_x (vec, i, value)
 -- C Function: scm_c64vector_set_x (vec, i, value)
     Set the element at index I in VEC to VALUE.  The first element in
     VEC is index 0.  The return value is unspecified.

 -- Scheme Procedure: u8vector->list vec
 -- Scheme Procedure: s8vector->list vec
 -- Scheme Procedure: u16vector->list vec
 -- Scheme Procedure: s16vector->list vec
 -- Scheme Procedure: u32vector->list vec
 -- Scheme Procedure: s32vector->list vec
 -- Scheme Procedure: u64vector->list vec
 -- Scheme Procedure: s64vector->list vec
 -- Scheme Procedure: f32vector->list vec
 -- Scheme Procedure: f64vector->list vec
 -- Scheme Procedure: c32vector->list vec
 -- Scheme Procedure: c64vector->list vec
 -- C Function: scm_u8vector_to_list (vec)
 -- C Function: scm_s8vector_to_list (vec)
 -- C Function: scm_u16vector_to_list (vec)
 -- C Function: scm_s16vector_to_list (vec)
 -- C Function: scm_u32vector_to_list (vec)
 -- C Function: scm_s32vector_to_list (vec)
 -- C Function: scm_u64vector_to_list (vec)
 -- C Function: scm_s64vector_to_list (vec)
 -- C Function: scm_f32vector_to_list (vec)
 -- C Function: scm_f64vector_to_list (vec)
 -- C Function: scm_c32vector_to_list (vec)
 -- C Function: scm_c64vector_to_list (vec)
     Return a newly allocated list holding all elements of VEC.

 -- Scheme Procedure: list->u8vector lst
 -- Scheme Procedure: list->s8vector lst
 -- Scheme Procedure: list->u16vector lst
 -- Scheme Procedure: list->s16vector lst
 -- Scheme Procedure: list->u32vector lst
 -- Scheme Procedure: list->s32vector lst
 -- Scheme Procedure: list->u64vector lst
 -- Scheme Procedure: list->s64vector lst
 -- Scheme Procedure: list->f32vector lst
 -- Scheme Procedure: list->f64vector lst
 -- Scheme Procedure: list->c32vector lst
 -- Scheme Procedure: list->c64vector lst
 -- C Function: scm_list_to_u8vector (lst)
 -- C Function: scm_list_to_s8vector (lst)
 -- C Function: scm_list_to_u16vector (lst)
 -- C Function: scm_list_to_s16vector (lst)
 -- C Function: scm_list_to_u32vector (lst)
 -- C Function: scm_list_to_s32vector (lst)
 -- C Function: scm_list_to_u64vector (lst)
 -- C Function: scm_list_to_s64vector (lst)
 -- C Function: scm_list_to_f32vector (lst)
 -- C Function: scm_list_to_f64vector (lst)
 -- C Function: scm_list_to_c32vector (lst)
 -- C Function: scm_list_to_c64vector (lst)
     Return a newly allocated homogeneous numeric vector of the
     indicated type, initialized with the elements of the list LST.

 -- C Function: SCM scm_take_u8vector (const scm_t_uint8 *data, size_t
          len)
 -- C Function: SCM scm_take_s8vector (const scm_t_int8 *data, size_t
          len)
 -- C Function: SCM scm_take_u16vector (const scm_t_uint16 *data, size_t
          len)
 -- C Function: SCM scm_take_s16vector (const scm_t_int16 *data, size_t
          len)
 -- C Function: SCM scm_take_u32vector (const scm_t_uint32 *data, size_t
          len)
 -- C Function: SCM scm_take_s32vector (const scm_t_int32 *data, size_t
          len)
 -- C Function: SCM scm_take_u64vector (const scm_t_uint64 *data, size_t
          len)
 -- C Function: SCM scm_take_s64vector (const scm_t_int64 *data, size_t
          len)
 -- C Function: SCM scm_take_f32vector (const float *data, size_t len)
 -- C Function: SCM scm_take_f64vector (const double *data, size_t len)
 -- C Function: SCM scm_take_c32vector (const float *data, size_t len)
 -- C Function: SCM scm_take_c64vector (const double *data, size_t len)
     Return a new uniform numeric vector of the indicated type and
     length that uses the memory pointed to by DATA to store its
     elements.  This memory will eventually be freed with ‘free’.  The
     argument LEN specifies the number of elements in DATA, not its size
     in bytes.

     The ‘c32’ and ‘c64’ variants take a pointer to a C array of
     ‘float’s or ‘double’s.  The real parts of the complex numbers are
     at even indices in that array, the corresponding imaginary parts
     are at the following odd index.

 -- C Function: const scm_t_uint8 * scm_u8vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int8 * scm_s8vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint16 * scm_u16vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int16 * scm_s16vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint32 * scm_u32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int32 * scm_s32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_uint64 * scm_u64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const scm_t_int64 * scm_s64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const float * scm_f32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const double * scm_f64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const float * scm_c32vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: const double * scm_c64vector_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
     Like ‘scm_vector_elements’ (*note Vector Accessing from C::), but
     returns a pointer to the elements of a uniform numeric vector of
     the indicated kind.

 -- C Function: scm_t_uint8 * scm_u8vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int8 * scm_s8vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint16 * scm_u16vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int16 * scm_s16vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint32 * scm_u32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int32 * scm_s32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_uint64 * scm_u64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: scm_t_int64 * scm_s64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: float * scm_f32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: double * scm_f64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: float * scm_c32vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
 -- C Function: double * scm_c64vector_writable_elements (SCM vec,
          scm_t_array_handle *handle, size_t *lenp, ssize_t *incp)
     Like ‘scm_vector_writable_elements’ (*note Vector Accessing from
     C::), but returns a pointer to the elements of a uniform numeric
     vector of the indicated kind.

7.5.5.3 SRFI-4 - Relation to bytevectors
........................................

Guile implements SRFI-4 vectors using bytevectors (*note Bytevectors::).
Often when you have a numeric vector, you end up wanting to write its
bytes somewhere, or have access to the underlying bytes, or read in
bytes from somewhere else.  Bytevectors are very good at this sort of
thing.  But the SRFI-4 APIs are nicer to use when doing
number-crunching, because they are addressed by element and not by byte.

   So as a compromise, Guile allows all bytevector functions to operate
on numeric vectors.  They address the underlying bytes in the native
endianness, as one would expect.

   Following the same reasoning, that it’s just bytes underneath, Guile
also allows uniform vectors of a given type to be accessed as if they
were of any type.  One can fill a u32vector, and access its elements
with u8vector-ref.  One can use f64vector-ref on bytevectors.  It’s all
the same to Guile.

   In this way, uniform numeric vectors may be written to and read from
input/output ports using the procedures that operate on bytevectors.

   *Note Bytevectors::, for more information.

7.5.5.4 SRFI-4 - Guile extensions
.................................

Guile defines some useful extensions to SRFI-4, which are not available
in the default Guile environment.  They may be imported by loading the
extensions module:

     (use-modules (srfi srfi-4 gnu))

 -- Scheme Procedure: any->u8vector obj
 -- Scheme Procedure: any->s8vector obj
 -- Scheme Procedure: any->u16vector obj
 -- Scheme Procedure: any->s16vector obj
 -- Scheme Procedure: any->u32vector obj
 -- Scheme Procedure: any->s32vector obj
 -- Scheme Procedure: any->u64vector obj
 -- Scheme Procedure: any->s64vector obj
 -- Scheme Procedure: any->f32vector obj
 -- Scheme Procedure: any->f64vector obj
 -- Scheme Procedure: any->c32vector obj
 -- Scheme Procedure: any->c64vector obj
 -- C Function: scm_any_to_u8vector (obj)
 -- C Function: scm_any_to_s8vector (obj)
 -- C Function: scm_any_to_u16vector (obj)
 -- C Function: scm_any_to_s16vector (obj)
 -- C Function: scm_any_to_u32vector (obj)
 -- C Function: scm_any_to_s32vector (obj)
 -- C Function: scm_any_to_u64vector (obj)
 -- C Function: scm_any_to_s64vector (obj)
 -- C Function: scm_any_to_f32vector (obj)
 -- C Function: scm_any_to_f64vector (obj)
 -- C Function: scm_any_to_c32vector (obj)
 -- C Function: scm_any_to_c64vector (obj)
     Return a (maybe newly allocated) uniform numeric vector of the
     indicated type, initialized with the elements of OBJ, which must be
     a list, a vector, or a uniform vector.  When OBJ is already a
     suitable uniform numeric vector, it is returned unchanged.

7.5.6 SRFI-6 - Basic String Ports
---------------------------------

SRFI-6 defines the procedures ‘open-input-string’, ‘open-output-string’
and ‘get-output-string’.

   Note that although versions of these procedures are included in the
Guile core, the core versions are not fully conformant with SRFI-6:
attempts to read or write characters that are not supported by the
current ‘%default-port-encoding’ will fail.

   We therefore recommend that you import this module, which supports
all characters:

     (use-modules (srfi srfi-6))

7.5.7 SRFI-8 - receive
----------------------

‘receive’ is a syntax for making the handling of multiple-value
procedures easier.  It is documented in *Note Multiple Values::.

7.5.8 SRFI-9 - define-record-type
---------------------------------

This SRFI is a syntax for defining new record types and creating
predicate, constructor, and field getter and setter functions.  It is
documented in the “Compound Data Types” section of the manual (*note
SRFI-9 Records::).

7.5.9 SRFI-10 - Hash-Comma Reader Extension
-------------------------------------------

This SRFI implements a reader extension ‘#,()’ called hash-comma.  It
allows the reader to give new kinds of objects, for use both in data and
as constants or literals in source code.  This feature is available with

     (use-modules (srfi srfi-10))

The new read syntax is of the form

     #,(TAG ARG…)

where TAG is a symbol and the ARGs are objects taken as parameters.
TAGs are registered with the following procedure.

 -- Scheme Procedure: define-reader-ctor tag proc
     Register PROC as the constructor for a hash-comma read syntax
     starting with symbol TAG, i.e. #,(TAG arg…).  PROC is called with
     the given arguments ‘(PROC arg…)’ and the object it returns is the
     result of the read.

For example, a syntax giving a list of N copies of an object.

     (define-reader-ctor 'repeat
       (lambda (obj reps)
         (make-list reps obj)))

     (display '#,(repeat 99 3))
     ⊣ (99 99 99)

   Notice the quote ’ when the #,( ) is used.  The ‘repeat’ handler
returns a list and the program must quote to use it literally, the same
as any other list.  Ie.

     (display '#,(repeat 99 3))
     ⇒
     (display '(99 99 99))

   When a handler returns an object which is self-evaluating, like a
number or a string, then there’s no need for quoting, just as there’s no
need when giving those directly as literals.  For example an addition,

     (define-reader-ctor 'sum
       (lambda (x y)
         (+ x y)))
     (display #,(sum 123 456)) ⊣ 579

   A typical use for #,() is to get a read syntax for objects which
don’t otherwise have one.  For example, the following allows a hash
table to be given literally, with tags and values, ready for fast
lookup.

     (define-reader-ctor 'hash
       (lambda elems
         (let ((table (make-hash-table)))
           (for-each (lambda (elem)
                       (apply hash-set! table elem))
                     elems)
           table)))

     (define (animal->family animal)
       (hash-ref '#,(hash ("tiger" "cat")
                          ("lion"  "cat")
                          ("wolf"  "dog"))
                 animal))

     (animal->family "lion") ⇒ "cat"

   Or for example the following is a syntax for a compiled regular
expression (*note Regular Expressions::).

     (use-modules (ice-9 regex))

     (define-reader-ctor 'regexp make-regexp)

     (define (extract-angs str)
       (let ((match (regexp-exec '#,(regexp "<([A-Z0-9]+)>") str)))
         (and match
              (match:substring match 1))))

     (extract-angs "foo <BAR> quux") ⇒ "BAR"


   #,() is somewhat similar to ‘define-macro’ (*note Macros::) in that
handler code is run to produce a result, but #,() operates at the read
stage, so it can appear in data for ‘read’ (*note Scheme Read::), not
just in code to be executed.

   Because #,() is handled at read-time it has no direct access to
variables etc.  A symbol in the arguments is just a symbol, not a
variable reference.  The arguments are essentially constants, though the
handler procedure can use them in any complicated way it might want.

   Once ‘(srfi srfi-10)’ has loaded, #,() is available globally, there’s
no need to use ‘(srfi srfi-10)’ in later modules.  Similarly the tags
registered are global and can be used anywhere once registered.

   There’s no attempt to record what previous #,() forms have been seen,
if two identical forms occur then two calls are made to the handler
procedure.  The handler might like to maintain a cache or similar to
avoid making copies of large objects, depending on expected usage.

   In code the best uses of #,() are generally when there’s a lot of
objects of a particular kind as literals or constants.  If there’s just
a few then some local variables and initializers are fine, but that
becomes tedious and error prone when there’s a lot, and the anonymous
and compact syntax of #,() is much better.

7.5.10 SRFI-11 - let-values
---------------------------

This module implements the binding forms for multiple values
‘let-values’ and ‘let*-values’.  These forms are similar to ‘let’ and
‘let*’ (*note Local Bindings::), but they support binding of the values
returned by multiple-valued expressions.

   Write ‘(use-modules (srfi srfi-11))’ to make the bindings available.

     (let-values (((x y) (values 1 2))
                  ((z f) (values 3 4)))
        (+ x y z f))
     ⇒
     10

   ‘let-values’ performs all bindings simultaneously, which means that
no expression in the binding clauses may refer to variables bound in the
same clause list.  ‘let*-values’, on the other hand, performs the
bindings sequentially, just like ‘let*’ does for single-valued
expressions.

7.5.11 SRFI-13 - String Library
-------------------------------

The SRFI-13 procedures are always available, *Note Strings::.

7.5.12 SRFI-14 - Character-set Library
--------------------------------------

The SRFI-14 data type and procedures are always available, *Note
Character Sets::.

7.5.13 SRFI-16 - case-lambda
----------------------------

SRFI-16 defines a variable-arity ‘lambda’ form, ‘case-lambda’.  This
form is available in the default Guile environment.  *Note
Case-lambda::, for more information.

7.5.14 SRFI-17 - Generalized set!
---------------------------------

This SRFI implements a generalized ‘set!’, allowing some “referencing”
functions to be used as the target location of a ‘set!’.  This feature
is available from

     (use-modules (srfi srfi-17))

For example ‘vector-ref’ is extended so that

     (set! (vector-ref vec idx) new-value)

is equivalent to

     (vector-set! vec idx new-value)

   The idea is that a ‘vector-ref’ expression identifies a location,
which may be either fetched or stored.  The same form is used for the
location in both cases, encouraging visual clarity.  This is similar to
the idea of an “lvalue” in C.

   The mechanism for this kind of ‘set!’ is in the Guile core (*note
Procedures with Setters::).  This module adds definitions of the
following functions as procedures with setters, allowing them to be
targets of a ‘set!’,

     car, cdr, caar, cadr, cdar, cddr, caaar, caadr, cadar, caddr,
     cdaar, cdadr, cddar, cdddr, caaaar, caaadr, caadar, caaddr, cadaar,
     cadadr, caddar, cadddr, cdaaar, cdaadr, cdadar, cdaddr, cddaar,
     cddadr, cdddar, cddddr

     string-ref, vector-ref

   The SRFI specifies ‘setter’ (*note Procedures with Setters::) as a
procedure with setter, allowing the setter for a procedure to be
changed, eg. ‘(set! (setter foo) my-new-setter-handler)’.  Currently
Guile does not implement this, a setter can only be specified on
creation (‘getter-with-setter’ below).

 -- Function: getter-with-setter
     The same as the Guile core ‘make-procedure-with-setter’ (*note
     Procedures with Setters::).

7.5.15 SRFI-18 - Multithreading support
---------------------------------------

This is an implementation of the SRFI-18 threading and synchronization
library.  The functions and variables described here are provided by

     (use-modules (srfi srfi-18))

   As a general rule, the data types and functions in this SRFI-18
implementation are compatible with the types and functions in Guile’s
core threading code.  For example, mutexes created with the SRFI-18
‘make-mutex’ function can be passed to the built-in Guile function
‘lock-mutex’ (*note Mutexes and Condition Variables::), and mutexes
created with the built-in Guile function ‘make-mutex’ can be passed to
the SRFI-18 function ‘mutex-lock!’.  Cases in which this does not hold
true are noted in the following sections.

7.5.15.1 SRFI-18 Threads
........................

Threads created by SRFI-18 differ in two ways from threads created by
Guile’s built-in thread functions.  First, a thread created by SRFI-18
‘make-thread’ begins in a blocked state and will not start execution
until ‘thread-start!’ is called on it.  Second, SRFI-18 threads are
constructed with a top-level exception handler that captures any
exceptions that are thrown on thread exit.  In all other regards,
SRFI-18 threads are identical to normal Guile threads.

 -- Function: current-thread
     Returns the thread that called this function.  This is the same
     procedure as the same-named built-in procedure ‘current-thread’
     (*note Threads::).

 -- Function: thread? obj
     Returns ‘#t’ if OBJ is a thread, ‘#f’ otherwise.  This is the same
     procedure as the same-named built-in procedure ‘thread?’ (*note
     Threads::).

 -- Function: make-thread thunk [name]
     Call ‘thunk’ in a new thread and with a new dynamic state,
     returning the new thread and optionally assigning it the object
     name NAME, which may be any Scheme object.

     Note that the name ‘make-thread’ conflicts with the ‘(ice-9
     threads)’ function ‘make-thread’.  Applications wanting to use both
     of these functions will need to refer to them by different names.

 -- Function: thread-name thread
     Returns the name assigned to THREAD at the time of its creation, or
     ‘#f’ if it was not given a name.

 -- Function: thread-specific thread
 -- Function: thread-specific-set! thread obj
     Get or set the “object-specific” property of THREAD.  In Guile’s
     implementation of SRFI-18, this value is stored as an object
     property, and will be ‘#f’ if not set.

 -- Function: thread-start! thread
     Unblocks THREAD and allows it to begin execution if it has not done
     so already.

 -- Function: thread-yield!
     If one or more threads are waiting to execute, calling
     ‘thread-yield!’ forces an immediate context switch to one of them.
     Otherwise, ‘thread-yield!’ has no effect.  ‘thread-yield!’ behaves
     identically to the Guile built-in function ‘yield’.

 -- Function: thread-sleep! timeout
     The current thread waits until the point specified by the time
     object TIMEOUT is reached (*note SRFI-18 Time::).  This blocks the
     thread only if TIMEOUT represents a point in the future.  it is an
     error for TIMEOUT to be ‘#f’.

 -- Function: thread-terminate! thread
     Causes an abnormal termination of THREAD.  If THREAD is not already
     terminated, all mutexes owned by THREAD become unlocked/abandoned.
     If THREAD is the current thread, ‘thread-terminate!’ does not
     return.  Otherwise ‘thread-terminate!’ returns an unspecified
     value; the termination of THREAD will occur before
     ‘thread-terminate!’ returns.  Subsequent attempts to join on THREAD
     will cause a “terminated thread exception” to be raised.

     ‘thread-terminate!’ is compatible with the thread cancellation
     procedures in the core threads API (*note Threads::) in that if a
     cleanup handler has been installed for the target thread, it will
     be called before the thread exits and its return value (or
     exception, if any) will be stored for later retrieval via a call to
     ‘thread-join!’.

 -- Function: thread-join! thread [timeout [timeout-val]]
     Wait for THREAD to terminate and return its exit value.  When a
     time value TIMEOUT is given, it specifies a point in time where the
     waiting should be aborted.  When the waiting is aborted,
     TIMEOUT-VAL is returned if it is specified; otherwise, a
     ‘join-timeout-exception’ exception is raised (*note SRFI-18
     Exceptions::).  Exceptions may also be raised if the thread was
     terminated by a call to ‘thread-terminate!’
     (‘terminated-thread-exception’ will be raised) or if the thread
     exited by raising an exception that was handled by the top-level
     exception handler (‘uncaught-exception’ will be raised; the
     original exception can be retrieved using
     ‘uncaught-exception-reason’).

7.5.15.2 SRFI-18 Mutexes
........................

The behavior of Guile’s built-in mutexes is parameterized via a set of
flags passed to the ‘make-mutex’ procedure in the core (*note Mutexes
and Condition Variables::).  To satisfy the requirements for mutexes
specified by SRFI-18, the ‘make-mutex’ procedure described below sets
the following flags:
   • ‘recursive’: the mutex can be locked recursively
   • ‘unchecked-unlock’: attempts to unlock a mutex that is already
     unlocked will not raise an exception
   • ‘allow-external-unlock’: the mutex can be unlocked by any thread,
     not just the thread that locked it originally

 -- Function: make-mutex [name]
     Returns a new mutex, optionally assigning it the object name NAME,
     which may be any Scheme object.  The returned mutex will be created
     with the configuration described above.  Note that the name
     ‘make-mutex’ conflicts with Guile core function ‘make-mutex’.
     Applications wanting to use both of these functions will need to
     refer to them by different names.

 -- Function: mutex-name mutex
     Returns the name assigned to MUTEX at the time of its creation, or
     ‘#f’ if it was not given a name.

 -- Function: mutex-specific mutex
 -- Function: mutex-specific-set! mutex obj
     Get or set the “object-specific” property of MUTEX.  In Guile’s
     implementation of SRFI-18, this value is stored as an object
     property, and will be ‘#f’ if not set.

 -- Function: mutex-state mutex
     Returns information about the state of MUTEX.  Possible values are:
        • thread ‘T’: the mutex is in the locked/owned state and thread
          T is the owner of the mutex
        • symbol ‘not-owned’: the mutex is in the locked/not-owned state
        • symbol ‘abandoned’: the mutex is in the unlocked/abandoned
          state
        • symbol ‘not-abandoned’: the mutex is in the
          unlocked/not-abandoned state

 -- Function: mutex-lock! mutex [timeout [thread]]
     Lock MUTEX, optionally specifying a time object TIMEOUT after which
     to abort the lock attempt and a thread THREAD giving a new owner
     for MUTEX different than the current thread.  This procedure has
     the same behavior as the ‘lock-mutex’ procedure in the core
     library.

 -- Function: mutex-unlock! mutex [condition-variable [timeout]]
     Unlock MUTEX, optionally specifying a condition variable
     CONDITION-VARIABLE on which to wait, either indefinitely or,
     optionally, until the time object TIMEOUT has passed, to be
     signalled.  This procedure has the same behavior as the
     ‘unlock-mutex’ procedure in the core library.

7.5.15.3 SRFI-18 Condition variables
....................................

SRFI-18 does not specify a “wait” function for condition variables.
Waiting on a condition variable can be simulated using the SRFI-18
‘mutex-unlock!’ function described in the previous section, or Guile’s
built-in ‘wait-condition-variable’ procedure can be used.

 -- Function: condition-variable? obj
     Returns ‘#t’ if OBJ is a condition variable, ‘#f’ otherwise.  This
     is the same procedure as the same-named built-in procedure (*note
     ‘condition-variable?’: Mutexes and Condition Variables.).

 -- Function: make-condition-variable [name]
     Returns a new condition variable, optionally assigning it the
     object name NAME, which may be any Scheme object.  This procedure
     replaces a procedure of the same name in the core library.

 -- Function: condition-variable-name condition-variable
     Returns the name assigned to CONDITION-VARIABLE at the time of its
     creation, or ‘#f’ if it was not given a name.

 -- Function: condition-variable-specific condition-variable
 -- Function: condition-variable-specific-set! condition-variable obj
     Get or set the “object-specific” property of CONDITION-VARIABLE.
     In Guile’s implementation of SRFI-18, this value is stored as an
     object property, and will be ‘#f’ if not set.

 -- Function: condition-variable-signal! condition-variable
 -- Function: condition-variable-broadcast! condition-variable
     Wake up one thread that is waiting for CONDITION-VARIABLE, in the
     case of ‘condition-variable-signal!’, or all threads waiting for
     it, in the case of ‘condition-variable-broadcast!’.  The behavior
     of these procedures is equivalent to that of the procedures
     ‘signal-condition-variable’ and ‘broadcast-condition-variable’ in
     the core library.

7.5.15.4 SRFI-18 Time
.....................

The SRFI-18 time functions manipulate time in two formats: a “time
object” type that represents an absolute point in time in some
implementation-specific way; and the number of seconds since some
unspecified “epoch”.  In Guile’s implementation, the epoch is the Unix
epoch, 00:00:00 UTC, January 1, 1970.

 -- Function: current-time
     Return the current time as a time object.  This procedure replaces
     the procedure of the same name in the core library, which returns
     the current time in seconds since the epoch.

 -- Function: time? obj
     Returns ‘#t’ if OBJ is a time object, ‘#f’ otherwise.

 -- Function: time->seconds time
 -- Function: seconds->time seconds
     Convert between time objects and numerical values representing the
     number of seconds since the epoch.  When converting from a time
     object to seconds, the return value is the number of seconds
     between TIME and the epoch.  When converting from seconds to a time
     object, the return value is a time object that represents a time
     SECONDS seconds after the epoch.

7.5.15.5 SRFI-18 Exceptions
...........................

SRFI-18 exceptions are identical to the exceptions provided by Guile’s
implementation of SRFI-34.  The behavior of exception handlers invoked
to handle exceptions thrown from SRFI-18 functions, however, differs
from the conventional behavior of SRFI-34 in that the continuation of
the handler is the same as that of the call to the function.  Handlers
are called in a tail-recursive manner; the exceptions do not “bubble
up”.

 -- Function: current-exception-handler
     Returns the current exception handler.

 -- Function: with-exception-handler handler thunk
     Installs HANDLER as the current exception handler and calls the
     procedure THUNK with no arguments, returning its value as the value
     of the exception.  HANDLER must be a procedure that accepts a
     single argument.  The current exception handler at the time this
     procedure is called will be restored after the call returns.

 -- Function: raise obj
     Raise OBJ as an exception.  This is the same procedure as the
     same-named procedure defined in SRFI 34.

 -- Function: join-timeout-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of
     performing a timed join on a thread that does not exit within the
     specified timeout, ‘#f’ otherwise.

 -- Function: abandoned-mutex-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of
     attempting to lock a mutex that has been abandoned by its owner
     thread, ‘#f’ otherwise.

 -- Function: terminated-thread-exception? obj
     Returns ‘#t’ if OBJ is an exception raised as the result of joining
     on a thread that exited as the result of a call to
     ‘thread-terminate!’.

 -- Function: uncaught-exception? obj
 -- Function: uncaught-exception-reason exc
     ‘uncaught-exception?’ returns ‘#t’ if OBJ is an exception thrown as
     the result of joining a thread that exited by raising an exception
     that was handled by the top-level exception handler installed by
     ‘make-thread’.  When this occurs, the original exception is
     preserved as part of the exception thrown by ‘thread-join!’ and can
     be accessed by calling ‘uncaught-exception-reason’ on that
     exception.  Note that because this exception-preservation mechanism
     is a side-effect of ‘make-thread’, joining on threads that exited
     as described above but were created by other means will not raise
     this ‘uncaught-exception’ error.

7.5.16 SRFI-19 - Time/Date Library
----------------------------------

This is an implementation of the SRFI-19 time/date library.  The
functions and variables described here are provided by

     (use-modules (srfi srfi-19))

   *Caution*: The current code in this module incorrectly extends the
Gregorian calendar leap year rule back prior to the introduction of
those reforms in 1582 (or the appropriate year in various countries).
The Julian calendar was used prior to 1582, and there were 10 days
skipped for the reform, but the code doesn’t implement that.

   This will be fixed some time.  Until then calculations for 1583
onwards are correct, but prior to that any day/month/year and day of the
week calculations are wrong.

7.5.16.1 SRFI-19 Introduction
.............................

This module implements time and date representations and calculations,
in various time systems, including universal time (UTC) and atomic time
(TAI).

   For those not familiar with these time systems, TAI is based on a
fixed length second derived from oscillations of certain atoms.  UTC
differs from TAI by an integral number of seconds, which is increased or
decreased at announced times to keep UTC aligned to a mean solar day
(the orbit and rotation of the earth are not quite constant).

   So far, only increases in the TAI <-> UTC difference have been
needed.  Such an increase is a “leap second”, an extra second of TAI
introduced at the end of a UTC day.  When working entirely within UTC
this is never seen, every day simply has 86400 seconds.  But when
converting from TAI to a UTC date, an extra 23:59:60 is present, where
normally a day would end at 23:59:59.  Effectively the UTC second from
23:59:59 to 00:00:00 has taken two TAI seconds.

   In the current implementation, the system clock is assumed to be UTC,
and a table of leap seconds in the code converts to TAI. See comments in
‘srfi-19.scm’ for how to update this table.

   Also, for those not familiar with the terminology, a "Julian Day" is
a real number which is a count of days and fraction of a day, in UTC,
starting from -4713-01-01T12:00:00Z, ie. midday Monday 1 Jan 4713 B.C. A
"Modified Julian Day" is the same, but starting from
1858-11-17T00:00:00Z, ie. midnight 17 November 1858 UTC. That time is
julian day 2400000.5.

7.5.16.2 SRFI-19 Time
.....................

A "time" object has type, seconds and nanoseconds fields representing a
point in time starting from some epoch.  This is an arbitrary point in
time, not just a time of day.  Although times are represented in
nanoseconds, the actual resolution may be lower.

   The following variables hold the possible time types.  For instance
‘(current-time time-process)’ would give the current CPU process time.

 -- Variable: time-utc
     Universal Coordinated Time (UTC).

 -- Variable: time-tai
     International Atomic Time (TAI).

 -- Variable: time-monotonic
     Monotonic time, meaning a monotonically increasing time starting
     from an unspecified epoch.

     Note that in the current implementation ‘time-monotonic’ is the
     same as ‘time-tai’, and unfortunately is therefore affected by
     adjustments to the system clock.  Perhaps this will change in the
     future.

 -- Variable: time-duration
     A duration, meaning simply a difference between two times.

 -- Variable: time-process
     CPU time spent in the current process, starting from when the
     process began.

 -- Variable: time-thread
     CPU time spent in the current thread.  Not currently implemented.


 -- Function: time? obj
     Return ‘#t’ if OBJ is a time object, or ‘#f’ if not.

 -- Function: make-time type nanoseconds seconds
     Create a time object with the given TYPE, SECONDS and NANOSECONDS.

 -- Function: time-type time
 -- Function: time-nanosecond time
 -- Function: time-second time
 -- Function: set-time-type! time type
 -- Function: set-time-nanosecond! time nsec
 -- Function: set-time-second! time sec
     Get or set the type, seconds or nanoseconds fields of a time
     object.

     ‘set-time-type!’ merely changes the field, it doesn’t convert the
     time value.  For conversions, see *note SRFI-19 Time/Date
     conversions::.

 -- Function: copy-time time
     Return a new time object, which is a copy of the given TIME.

 -- Function: current-time [type]
     Return the current time of the given TYPE.  The default TYPE is
     ‘time-utc’.

     Note that the name ‘current-time’ conflicts with the Guile core
     ‘current-time’ function (*note Time::) as well as the SRFI-18
     ‘current-time’ function (*note SRFI-18 Time::).  Applications
     wanting to use more than one of these functions will need to refer
     to them by different names.

 -- Function: time-resolution [type]
     Return the resolution, in nanoseconds, of the given time TYPE.  The
     default TYPE is ‘time-utc’.

 -- Function: time<=? t1 t2
 -- Function: time<? t1 t2
 -- Function: time=? t1 t2
 -- Function: time>=? t1 t2
 -- Function: time>? t1 t2
     Return ‘#t’ or ‘#f’ according to the respective relation between
     time objects T1 and T2.  T1 and T2 must be the same time type.

 -- Function: time-difference t1 t2
 -- Function: time-difference! t1 t2
     Return a time object of type ‘time-duration’ representing the
     period between T1 and T2.  T1 and T2 must be the same time type.

     ‘time-difference’ returns a new time object, ‘time-difference!’ may
     modify T1 to form its return.

 -- Function: add-duration time duration
 -- Function: add-duration! time duration
 -- Function: subtract-duration time duration
 -- Function: subtract-duration! time duration
     Return a time object which is TIME with the given DURATION added or
     subtracted.  DURATION must be a time object of type
     ‘time-duration’.

     ‘add-duration’ and ‘subtract-duration’ return a new time object.
     ‘add-duration!’ and ‘subtract-duration!’ may modify the given TIME
     to form their return.

7.5.16.3 SRFI-19 Date
.....................

A "date" object represents a date in the Gregorian calendar and a time
of day on that date in some timezone.

   The fields are year, month, day, hour, minute, second, nanoseconds
and timezone.  A date object is immutable, its fields can be read but
they cannot be modified once the object is created.

 -- Function: date? obj
     Return ‘#t’ if OBJ is a date object, or ‘#f’ if not.

 -- Function: make-date nsecs seconds minutes hours date month year
          zone-offset
     Create a new date object.

 -- Function: date-nanosecond date
     Nanoseconds, 0 to 999999999.

 -- Function: date-second date
     Seconds, 0 to 59, or 60 for a leap second.  60 is never seen when
     working entirely within UTC, it’s only when converting to or from
     TAI.

 -- Function: date-minute date
     Minutes, 0 to 59.

 -- Function: date-hour date
     Hour, 0 to 23.

 -- Function: date-day date
     Day of the month, 1 to 31 (or less, according to the month).

 -- Function: date-month date
     Month, 1 to 12.

 -- Function: date-year date
     Year, eg. 2003.  Dates B.C. are negative, eg. -46 is 46 B.C. There
     is no year 0, year -1 is followed by year 1.

 -- Function: date-zone-offset date
     Time zone, an integer number of seconds east of Greenwich.

 -- Function: date-year-day date
     Day of the year, starting from 1 for 1st January.

 -- Function: date-week-day date
     Day of the week, starting from 0 for Sunday.

 -- Function: date-week-number date dstartw
     Week of the year, ignoring a first partial week.  DSTARTW is the
     day of the week which is taken to start a week, 0 for Sunday, 1 for
     Monday, etc.

 -- Function: current-date [tz-offset]
     Return a date object representing the current date/time, in UTC
     offset by TZ-OFFSET.  TZ-OFFSET is seconds east of Greenwich and
     defaults to the local timezone.

 -- Function: current-julian-day
     Return the current Julian Day.

 -- Function: current-modified-julian-day
     Return the current Modified Julian Day.

7.5.16.4 SRFI-19 Time/Date conversions
......................................

 -- Function: date->julian-day date
 -- Function: date->modified-julian-day date
 -- Function: date->time-monotonic date
 -- Function: date->time-tai date
 -- Function: date->time-utc date
 -- Function: julian-day->date jdn [tz-offset]
 -- Function: julian-day->time-monotonic jdn
 -- Function: julian-day->time-tai jdn
 -- Function: julian-day->time-utc jdn
 -- Function: modified-julian-day->date jdn [tz-offset]
 -- Function: modified-julian-day->time-monotonic jdn
 -- Function: modified-julian-day->time-tai jdn
 -- Function: modified-julian-day->time-utc jdn
 -- Function: time-monotonic->date time [tz-offset]
 -- Function: time-monotonic->time-tai time
 -- Function: time-monotonic->time-tai! time
 -- Function: time-monotonic->time-utc time
 -- Function: time-monotonic->time-utc! time
 -- Function: time-tai->date time [tz-offset]
 -- Function: time-tai->julian-day time
 -- Function: time-tai->modified-julian-day time
 -- Function: time-tai->time-monotonic time
 -- Function: time-tai->time-monotonic! time
 -- Function: time-tai->time-utc time
 -- Function: time-tai->time-utc! time
 -- Function: time-utc->date time [tz-offset]
 -- Function: time-utc->julian-day time
 -- Function: time-utc->modified-julian-day time
 -- Function: time-utc->time-monotonic time
 -- Function: time-utc->time-monotonic! time
 -- Function: time-utc->time-tai time
 -- Function: time-utc->time-tai! time

     Convert between dates, times and days of the respective types.  For
     instance ‘time-tai->time-utc’ accepts a TIME object of type
     ‘time-tai’ and returns an object of type ‘time-utc’.

     The ‘!’ variants may modify their TIME argument to form their
     return.  The plain functions create a new object.

     For conversions to dates, TZ-OFFSET is seconds east of Greenwich.
     The default is the local timezone, at the given time, as provided
     by the system, using ‘localtime’ (*note Time::).

     On 32-bit systems, ‘localtime’ is limited to a 32-bit ‘time_t’, so
     a default TZ-OFFSET is only available for times between Dec 1901
     and Jan 2038.  For prior dates an application might like to use the
     value in 1902, though some locations have zone changes prior to
     that.  For future dates an application might like to assume today’s
     rules extend indefinitely.  But for correct daylight savings
     transitions it will be necessary to take an offset for the same day
     and time but a year in range and which has the same starting
     weekday and same leap/non-leap (to support rules like last Sunday
     in October).

7.5.16.5 SRFI-19 Date to string
...............................

 -- Function: date->string date [format]
     Convert a date to a string under the control of a format.  FORMAT
     should be a string containing ‘~’ escapes, which will be expanded
     as per the following conversion table.  The default FORMAT is ‘~c’,
     a locale-dependent date and time.

     Many of these conversion characters are the same as POSIX
     ‘strftime’ (*note Time::), but there are some extras and some
     variations.

     ~~     literal ~
     ~a     locale abbreviated weekday, eg. ‘Sun’
     ~A     locale full weekday, eg. ‘Sunday’
     ~b     locale abbreviated month, eg. ‘Jan’
     ~B     locale full month, eg. ‘January’
     ~c     locale date and time, eg.
            ‘Fri Jul 14 20:28:42-0400 2000’
     ~d     day of month, zero padded, ‘01’ to ‘31’
            
     ~e     day of month, blank padded, ‘ 1’ to ‘31’
     ~f     seconds and fractional seconds, with locale
            decimal point, eg. ‘5.2’
     ~h     same as ~b
     ~H     hour, 24-hour clock, zero padded, ‘00’ to ‘23’
     ~I     hour, 12-hour clock, zero padded, ‘01’ to ‘12’
     ~j     day of year, zero padded, ‘001’ to ‘366’
     ~k     hour, 24-hour clock, blank padded, ‘ 0’ to ‘23’
     ~l     hour, 12-hour clock, blank padded, ‘ 1’ to ‘12’
     ~m     month, zero padded, ‘01’ to ‘12’
     ~M     minute, zero padded, ‘00’ to ‘59’
     ~n     newline
     ~N     nanosecond, zero padded, ‘000000000’ to
            ‘999999999’
     ~p     locale AM or PM
     ~r     time, 12 hour clock, ‘~I:~M:~S ~p’
     ~s     number of full seconds since “the epoch” in UTC
     ~S     second, zero padded ‘00’ to ‘60’
            (usual limit is 59, 60 is a leap second)
     ~t     horizontal tab character
     ~T     time, 24 hour clock, ‘~H:~M:~S’
     ~U     week of year, Sunday first day of week, ‘00’ to
            ‘52’
     ~V     week of year, Monday first day of week, ‘01’ to
            ‘53’
     ~w     day of week, 0 for Sunday, ‘0’ to ‘6’
     ~W     week of year, Monday first day of week, ‘00’ to
            ‘52’
            
     ~y     year, two digits, ‘00’ to ‘99’
     ~Y     year, full, eg. ‘2003’
     ~z     time zone, RFC-822 style
     ~Z     time zone symbol (not currently implemented)
     ~1     ISO-8601 date, ‘~Y-~m-~d’
     ~2     ISO-8601 time+zone, ‘~H:~M:~S~z’
     ~3     ISO-8601 time, ‘~H:~M:~S’
     ~4     ISO-8601 date/time+zone, ‘~Y-~m-~dT~H:~M:~S~z’
     ~5     ISO-8601 date/time, ‘~Y-~m-~dT~H:~M:~S’

   Conversions ‘~D’, ‘~x’ and ‘~X’ are not currently described here,
since the specification and reference implementation differ.

   Conversion is locale-dependent on systems that support it (*note
Accessing Locale Information::).  *Note ‘setlocale’: Locales, for
information on how to change the current locale.

7.5.16.6 SRFI-19 String to date
...............................

 -- Function: string->date input template
     Convert an INPUT string to a date under the control of a TEMPLATE
     string.  Return a newly created date object.

     Literal characters in TEMPLATE must match characters in INPUT and
     ‘~’ escapes must match the input forms described in the table
     below.  “Skip to” means characters up to one of the given type are
     ignored, or “no skip” for no skipping.  “Read” is what’s then read,
     and “Set” is the field affected in the date object.

     For example ‘~Y’ skips input characters until a digit is reached,
     at which point it expects a year and stores that to the year field
     of the date.

            Skip to            Read                        Set
                                                           
     ~~     no skip            literal ~                   nothing
                                                           
     ~a     char-alphabetic?   locale abbreviated          nothing
                               weekday name                
     ~A     char-alphabetic?   locale full weekday name    nothing
                                                           
     ~b     char-alphabetic?   locale abbreviated month    date-month
                               name                        
     ~B     char-alphabetic?   locale full month name      date-month
                                                           
     ~d     char-numeric?      day of month                date-day
                                                           
     ~e     no skip            day of month, blank         date-day
                               padded                      
     ~h     same as ‘~b’
            
     ~H     char-numeric?      hour                        date-hour
                                                           
     ~k     no skip            hour, blank padded          date-hour
                                                           
     ~m     char-numeric?      month                       date-month
                                                           
     ~M     char-numeric?      minute                      date-minute
                                                           
     ~S     char-numeric?      second                      date-second
                                                           
     ~y     no skip            2-digit year                date-year within
                                                           50 years
                                                           
     ~Y     char-numeric?      year                        date-year
                                                           
     ~z     no skip            time zone                   date-zone-offset

     Notice that the weekday matching forms don’t affect the date object
     returned, instead the weekday will be derived from the day, month
     and year.

     Conversion is locale-dependent on systems that support it (*note
     Accessing Locale Information::).  *Note ‘setlocale’: Locales, for
     information on how to change the current locale.

7.5.17 SRFI-23 - Error Reporting
--------------------------------

The SRFI-23 ‘error’ procedure is always available.

7.5.18 SRFI-26 - specializing parameters
----------------------------------------

This SRFI provides a syntax for conveniently specializing selected
parameters of a function.  It can be used with,

     (use-modules (srfi srfi-26))

 -- library syntax: cut slot1 slot2 …
 -- library syntax: cute slot1 slot2 …
     Return a new procedure which will make a call (SLOT1 SLOT2 …) but
     with selected parameters specialized to given expressions.

     An example will illustrate the idea.  The following is a
     specialization of ‘write’, sending output to ‘my-output-port’,

          (cut write <> my-output-port)
          ⇒
          (lambda (obj) (write obj my-output-port))

     The special symbol ‘<>’ indicates a slot to be filled by an
     argument to the new procedure.  ‘my-output-port’ on the other hand
     is an expression to be evaluated and passed, ie. it specializes the
     behaviour of ‘write’.

     <>
          A slot to be filled by an argument from the created procedure.
          Arguments are assigned to ‘<>’ slots in the order they appear
          in the ‘cut’ form, there’s no way to re-arrange arguments.

          The first argument to ‘cut’ is usually a procedure (or
          expression giving a procedure), but ‘<>’ is allowed there too.
          For example,

               (cut <> 1 2 3)
               ⇒
               (lambda (proc) (proc 1 2 3))

     <...>
          A slot to be filled by all remaining arguments from the new
          procedure.  This can only occur at the end of a ‘cut’ form.

          For example, a procedure taking a variable number of arguments
          like ‘max’ but in addition enforcing a lower bound,

               (define my-lower-bound 123)

               (cut max my-lower-bound <...>)
               ⇒
               (lambda arglist (apply max my-lower-bound arglist))

     For ‘cut’ the specializing expressions are evaluated each time the
     new procedure is called.  For ‘cute’ they’re evaluated just once,
     when the new procedure is created.  The name ‘cute’ stands for
     “‘cut’ with evaluated arguments”.  In all cases the evaluations
     take place in an unspecified order.

     The following illustrates the difference between ‘cut’ and ‘cute’,

          (cut format <> "the time is ~s" (current-time))
          ⇒
          (lambda (port) (format port "the time is ~s" (current-time)))

          (cute format <> "the time is ~s" (current-time))
          ⇒
          (let ((val (current-time)))
            (lambda (port) (format port "the time is ~s" val))

     (There’s no provision for a mixture of ‘cut’ and ‘cute’ where some
     expressions would be evaluated every time but others evaluated only
     once.)

     ‘cut’ is really just a shorthand for the sort of ‘lambda’ forms
     shown in the above examples.  But notice ‘cut’ avoids the need to
     name unspecialized parameters, and is more compact.  Use in
     functional programming style or just with ‘map’, ‘for-each’ or
     similar is typical.

          (map (cut * 2 <>) '(1 2 3 4))

          (for-each (cut write <> my-port) my-list)

7.5.19 SRFI-27 - Sources of Random Bits
---------------------------------------

This subsection is based on the specification of SRFI-27
(http://srfi.schemers.org/srfi-27/srfi-27.html) written by Sebastian
Egner.

   This SRFI provides access to a (pseudo) random number generator; for
Guile’s built-in random number facilities, which SRFI-27 is implemented
upon, *Note Random::.  With SRFI-27, random numbers are obtained from a
_random source_, which encapsulates a random number generation algorithm
and its state.

7.5.19.1 The Default Random Source
..................................

 -- Function: random-integer n
     Return a random number between zero (inclusive) and N (exclusive),
     using the default random source.  The numbers returned have a
     uniform distribution.

 -- Function: random-real
     Return a random number in (0,1), using the default random source.
     The numbers returned have a uniform distribution.

 -- Function: default-random-source
     A random source from which ‘random-integer’ and ‘random-real’ have
     been derived using ‘random-source-make-integers’ and
     ‘random-source-make-reals’ (*note SRFI-27 Random Number
     Generators:: for those procedures).  Note that an assignment to
     ‘default-random-source’ does not change ‘random-integer’ or
     ‘random-real’; it is also strongly recommended not to assign a new
     value.

7.5.19.2 Random Sources
.......................

 -- Function: make-random-source
     Create a new random source.  The stream of random numbers obtained
     from each random source created by this procedure will be
     identical, unless its state is changed by one of the procedures
     below.

 -- Function: random-source? object
     Tests whether OBJECT is a random source.  Random sources are a
     disjoint type.

 -- Function: random-source-randomize! source
     Attempt to set the state of the random source to a truly random
     value.  The current implementation uses a seed based on the current
     system time.

 -- Function: random-source-pseudo-randomize! source i j
     Changes the state of the random source s into the initial state of
     the (I, J)-th independent random source, where I and J are
     non-negative integers.  This procedure provides a mechanism to
     obtain a large number of independent random sources (usually all
     derived from the same backbone generator), indexed by two integers.
     In contrast to ‘random-source-randomize!’, this procedure is
     entirely deterministic.

   The state associated with a random state can be obtained an
reinstated with the following procedures:

 -- Function: random-source-state-ref source
 -- Function: random-source-state-set! source state
     Get and set the state of a random source.  No assumptions should be
     made about the nature of the state object, besides it having an
     external representation (i.e. it can be passed to ‘write’ and
     subsequently ‘read’ back).

7.5.19.3 Obtaining random number generator procedures
.....................................................

 -- Function: random-source-make-integers source
     Obtains a procedure to generate random integers using the random
     source SOURCE.  The returned procedure takes a single argument N,
     which must be a positive integer, and returns the next uniformly
     distributed random integer from the interval {0, ..., N-1} by
     advancing the state of SOURCE.

     If an application obtains and uses several generators for the same
     random source SOURCE, a call to any of these generators advances
     the state of SOURCE.  Hence, the generators do not produce the same
     sequence of random integers each but rather share a state.  This
     also holds for all other types of generators derived from a fixed
     random sources.

     While the SRFI text specifies that “Implementations that support
     concurrency make sure that the state of a generator is properly
     advanced”, this is currently not the case in Guile’s implementation
     of SRFI-27, as it would cause a severe performance penalty.  So in
     multi-threaded programs, you either must perform locking on random
     sources shared between threads yourself, or use different random
     sources for multiple threads.

 -- Function: random-source-make-reals source
 -- Function: random-source-make-reals source unit
     Obtains a procedure to generate random real numbers 0 < x < 1 using
     the random source SOURCE.  The procedure rand is called without
     arguments.

     The optional parameter UNIT determines the type of numbers being
     produced by the returned procedure and the quantization of the
     output.  UNIT must be a number such that 0 < UNIT < 1.  The numbers
     created by the returned procedure are of the same numerical type as
     UNIT and the potential output values are spaced by at most UNIT.
     One can imagine rand to create numbers as X * UNIT where X is a
     random integer in {1, ..., floor(1/unit)-1}.  Note, however, that
     this need not be the way the values are actually created and that
     the actual resolution of rand can be much higher than unit.  In
     case UNIT is absent it defaults to a reasonably small value
     (related to the width of the mantissa of an efficient number
     format).

7.5.20 SRFI-30 - Nested Multi-line Comments
-------------------------------------------

Starting from version 2.0, Guile’s ‘read’ supports SRFI-30/R6RS nested
multi-line comments by default, *note Block Comments::.

7.5.21 SRFI-31 - A special form ‘rec’ for recursive evaluation
--------------------------------------------------------------

SRFI-31 defines a special form that can be used to create
self-referential expressions more conveniently.  The syntax is as
follows:

     <rec expression> --> (rec <variable> <expression>)
     <rec expression> --> (rec (<variable>+) <body>)

   The first syntax can be used to create self-referential expressions,
for example:

       guile> (define tmp (rec ones (cons 1 (delay ones))))

   The second syntax can be used to create anonymous recursive
functions:

       guile> (define tmp (rec (display-n item n)
                            (if (positive? n)
                                (begin (display n) (display-n (- n 1))))))
       guile> (tmp 42 3)
       424242
       guile>

7.5.22 SRFI-34 - Exception handling for programs
------------------------------------------------

Guile provides an implementation of SRFI-34’s exception handling
mechanisms (http://srfi.schemers.org/srfi-34/srfi-34.html) as an
alternative to its own built-in mechanisms (*note Exceptions::).  It can
be made available as follows:

     (use-modules (srfi srfi-34))

7.5.23 SRFI-35 - Conditions
---------------------------

SRFI-35 (http://srfi.schemers.org/srfi-35/srfi-35.html) implements
"conditions", a data structure akin to records designed to convey
information about exceptional conditions between parts of a program.  It
is normally used in conjunction with SRFI-34’s ‘raise’:

     (raise (condition (&message
                         (message "An error occurred"))))

   Users can define "condition types" containing arbitrary information.
Condition types may inherit from one another.  This allows the part of
the program that handles (or “catches”) conditions to get accurate
information about the exceptional condition that arose.

   SRFI-35 conditions are made available using:

     (use-modules (srfi srfi-35))

   The procedures available to manipulate condition types are the
following:

 -- Scheme Procedure: make-condition-type id parent field-names
     Return a new condition type named ID, inheriting from PARENT, and
     with the fields whose names are listed in FIELD-NAMES.  FIELD-NAMES
     must be a list of symbols and must not contain names already used
     by PARENT or one of its supertypes.

 -- Scheme Procedure: condition-type? obj
     Return true if OBJ is a condition type.

   Conditions can be created and accessed with the following procedures:

 -- Scheme Procedure: make-condition type . field+value
     Return a new condition of type TYPE with fields initialized as
     specified by FIELD+VALUE, a sequence of field names (symbols) and
     values as in the following example:

          (let ((&ct (make-condition-type 'foo &condition '(a b c))))
            (make-condition &ct 'a 1 'b 2 'c 3))

     Note that all fields of TYPE and its supertypes must be specified.

 -- Scheme Procedure: make-compound-condition condition1 condition2 …
     Return a new compound condition composed of CONDITION1 CONDITION2
     ....  The returned condition has the type of each condition of
     condition1 condition2 … (per ‘condition-has-type?’).

 -- Scheme Procedure: condition-has-type? c type
     Return true if condition C has type TYPE.

 -- Scheme Procedure: condition-ref c field-name
     Return the value of the field named FIELD-NAME from condition C.

     If C is a compound condition and several underlying condition types
     contain a field named FIELD-NAME, then the value of the first such
     field is returned, using the order in which conditions were passed
     to ‘make-compound-condition’.

 -- Scheme Procedure: extract-condition c type
     Return a condition of condition type TYPE with the field values
     specified by C.

     If C is a compound condition, extract the field values from the
     subcondition belonging to TYPE that appeared first in the call to
     ‘make-compound-condition’ that created the condition.

   Convenience macros are also available to create condition types and
conditions.

 -- library syntax: define-condition-type type supertype predicate
          field-spec...
     Define a new condition type named TYPE that inherits from
     SUPERTYPE.  In addition, bind PREDICATE to a type predicate that
     returns true when passed a condition of type TYPE or any of its
     subtypes.  FIELD-SPEC must have the form ‘(field accessor)’ where
     FIELD is the name of field of TYPE and ACCESSOR is the name of a
     procedure to access field FIELD in conditions of type TYPE.

     The example below defines condition type ‘&foo’, inheriting from
     ‘&condition’ with fields ‘a’, ‘b’ and ‘c’:

          (define-condition-type &foo &condition
            foo-condition?
            (a  foo-a)
            (b  foo-b)
            (c  foo-c))

 -- library syntax: condition type-field-binding1 type-field-binding2 …
     Return a new condition or compound condition, initialized according
     to TYPE-FIELD-BINDING1 TYPE-FIELD-BINDING2 ....  Each
     TYPE-FIELD-BINDING must have the form ‘(type field-specs...)’,
     where TYPE is the name of a variable bound to a condition type;
     each FIELD-SPEC must have the form ‘(field-name value)’ where
     FIELD-NAME is a symbol denoting the field being initialized to
     VALUE.  As for ‘make-condition’, all fields must be specified.

     The following example returns a simple condition:

          (condition (&message (message "An error occurred")))

     The one below returns a compound condition:

          (condition (&message (message "An error occurred"))
                     (&serious))

   Finally, SRFI-35 defines a several standard condition types.

 -- Variable: &condition
     This condition type is the root of all condition types.  It has no
     fields.

 -- Variable: &message
     A condition type that carries a message describing the nature of
     the condition to humans.

 -- Scheme Procedure: message-condition? c
     Return true if C is of type ‘&message’ or one of its subtypes.

 -- Scheme Procedure: condition-message c
     Return the message associated with message condition C.

 -- Variable: &serious
     This type describes conditions serious enough that they cannot
     safely be ignored.  It has no fields.

 -- Scheme Procedure: serious-condition? c
     Return true if C is of type ‘&serious’ or one of its subtypes.

 -- Variable: &error
     This condition describes errors, typically caused by something that
     has gone wrong in the interaction of the program with the external
     world or the user.

 -- Scheme Procedure: error? c
     Return true if C is of type ‘&error’ or one of its subtypes.

7.5.24 SRFI-37 - args-fold
--------------------------

This is a processor for GNU ‘getopt_long’-style program arguments.  It
provides an alternative, less declarative interface than ‘getopt-long’
in ‘(ice-9 getopt-long)’ (*note The (ice-9 getopt-long) Module:
getopt-long.).  Unlike ‘getopt-long’, it supports repeated options and
any number of short and long names per option.  Access it with:

     (use-modules (srfi srfi-37))

   SRFI-37 principally provides an ‘option’ type and the ‘args-fold’
function.  To use the library, create a set of options with ‘option’ and
use it as a specification for invoking ‘args-fold’.

   Here is an example of a simple argument processor for the typical
‘--version’ and ‘--help’ options, which returns a backwards list of
files given on the command line:

     (args-fold (cdr (program-arguments))
                (let ((display-and-exit-proc
                       (lambda (msg)
                         (lambda (opt name arg loads)
                           (display msg) (quit)))))
                  (list (option '(#\v "version") #f #f
                                (display-and-exit-proc "Foo version 42.0\n"))
                        (option '(#\h "help") #f #f
                                (display-and-exit-proc
                                 "Usage: foo scheme-file ..."))))
                (lambda (opt name arg loads)
                  (error "Unrecognized option `~A'" name))
                (lambda (op loads) (cons op loads))
                '())

 -- Scheme Procedure: option names required-arg? optional-arg? processor
     Return an object that specifies a single kind of program option.

     NAMES is a list of command-line option names, and should consist of
     characters for traditional ‘getopt’ short options and strings for
     ‘getopt_long’-style long options.

     REQUIRED-ARG? and OPTIONAL-ARG? are mutually exclusive; one or both
     must be ‘#f’.  If REQUIRED-ARG?, the option must be followed by an
     argument on the command line, such as ‘--opt=value’ for long
     options, or an error will be signalled.  If OPTIONAL-ARG?, an
     argument will be taken if available.

     PROCESSOR is a procedure that takes at least 3 arguments, called
     when ‘args-fold’ encounters the option: the containing option
     object, the name used on the command line, and the argument given
     for the option (or ‘#f’ if none).  The rest of the arguments are
     ‘args-fold’ “seeds”, and the PROCESSOR should return seeds as well.

 -- Scheme Procedure: option-names opt
 -- Scheme Procedure: option-required-arg? opt
 -- Scheme Procedure: option-optional-arg? opt
 -- Scheme Procedure: option-processor opt
     Return the specified field of OPT, an option object, as described
     above for ‘option’.

 -- Scheme Procedure: args-fold args options unrecognized-option-proc
          operand-proc seed …
     Process ARGS, a list of program arguments such as that returned by
     ‘(cdr (program-arguments))’, in order against OPTIONS, a list of
     option objects as described above.  All functions called take the
     “seeds”, or the last multiple-values as multiple arguments,
     starting with SEED …, and must return the new seeds.  Return the
     final seeds.

     Call ‘unrecognized-option-proc’, which is like an option object’s
     processor, for any options not found in OPTIONS.

     Call ‘operand-proc’ with any items on the command line that are not
     named options.  This includes arguments after ‘--’.  It is called
     with the argument in question, as well as the seeds.

7.5.25 SRFI-38 - External Representation for Data With Shared Structure
-----------------------------------------------------------------------

This subsection is based on the specification of SRFI-38
(http://srfi.schemers.org/srfi-38/srfi-38.html) written by Ray
Dillinger.

   This SRFI creates an alternative external representation for data
written and read using ‘write-with-shared-structure’ and
‘read-with-shared-structure’.  It is identical to the grammar for
external representation for data written and read with ‘write’ and
‘read’ given in section 7 of R5RS, except that the single production

     <datum> --> <simple datum> | <compound datum>

   is replaced by the following five productions:

     <datum> --> <defining datum> | <nondefining datum> | <defined datum>
     <defining datum> -->  #<indexnum>=<nondefining datum>
     <defined datum> --> #<indexnum>#
     <nondefining datum> --> <simple datum> | <compound datum>
     <indexnum> --> <digit 10>+

 -- Scheme procedure: write-with-shared-structure obj
 -- Scheme procedure: write-with-shared-structure obj port
 -- Scheme procedure: write-with-shared-structure obj port optarg

     Writes an external representation of OBJ to the given port.
     Strings that appear in the written representation are enclosed in
     doublequotes, and within those strings backslash and doublequote
     characters are escaped by backslashes.  Character objects are
     written using the ‘#\’ notation.

     Objects which denote locations rather than values (cons cells,
     vectors, and non-zero-length strings in R5RS scheme; also Guile’s
     structs, bytevectors and ports and hash-tables), if they appear at
     more than one point in the data being written, are preceded by
     ‘#N=’ the first time they are written and replaced by ‘#N#’ all
     subsequent times they are written, where N is a natural number used
     to identify that particular object.  If objects which denote
     locations occur only once in the structure, then
     ‘write-with-shared-structure’ must produce the same external
     representation for those objects as ‘write’.

     ‘write-with-shared-structure’ terminates in finite time and
     produces a finite representation when writing finite data.

     ‘write-with-shared-structure’ returns an unspecified value.  The
     PORT argument may be omitted, in which case it defaults to the
     value returned by ‘(current-output-port)’.  The OPTARG argument may
     also be omitted.  If present, its effects on the output and return
     value are unspecified but ‘write-with-shared-structure’ must still
     write a representation that can be read by
     ‘read-with-shared-structure’.  Some implementations may wish to use
     OPTARG to specify formatting conventions, numeric radixes, or
     return values.  Guile’s implementation ignores OPTARG.

     For example, the code

          (begin (define a (cons 'val1 'val2))
                 (set-cdr! a a)
                 (write-with-shared-structure a))

     should produce the output ‘#1=(val1 . #1#)’.  This shows a cons
     cell whose ‘cdr’ contains itself.

 -- Scheme procedure: read-with-shared-structure
 -- Scheme procedure: read-with-shared-structure port

     ‘read-with-shared-structure’ converts the external representations
     of Scheme objects produced by ‘write-with-shared-structure’ into
     Scheme objects.  That is, it is a parser for the nonterminal
     ‘<datum>’ in the augmented external representation grammar defined
     above.  ‘read-with-shared-structure’ returns the next object
     parsable from the given input port, updating PORT to point to the
     first character past the end of the external representation of the
     object.

     If an end-of-file is encountered in the input before any characters
     are found that can begin an object, then an end-of-file object is
     returned.  The port remains open, and further attempts to read it
     (by ‘read-with-shared-structure’ or ‘read’ will also return an
     end-of-file object.  If an end of file is encountered after the
     beginning of an object’s external representation, but the external
     representation is incomplete and therefore not parsable, an error
     is signalled.

     The PORT argument may be omitted, in which case it defaults to the
     value returned by ‘(current-input-port)’.  It is an error to read
     from a closed port.

7.5.26 SRFI-39 - Parameters
---------------------------

This SRFI adds support for dynamically-scoped parameters.  SRFI 39 is
implemented in the Guile core; there’s no module needed to get SRFI-39
itself.  Parameters are documented in *note Parameters::.

   This module does export one extra function: ‘with-parameters*’.  This
is a Guile-specific addition to the SRFI, similar to the core
‘with-fluids*’ (*note Fluids and Dynamic States::).

 -- Function: with-parameters* param-list value-list thunk
     Establish a new dynamic scope, as per ‘parameterize’ above, taking
     parameters from PARAM-LIST and corresponding values from
     VALUE-LIST.  A call ‘(THUNK)’ is made in the new scope and the
     result from that THUNK is the return from ‘with-parameters*’.

7.5.27 SRFI-41 - Streams
------------------------

This subsection is based on the specification of SRFI-41
(http://srfi.schemers.org/srfi-41/srfi-41.html) by Philip L. Bewig.

This SRFI implements streams, sometimes called lazy lists, a sequential
data structure containing elements computed only on demand.  A stream is
either null or is a pair with a stream in its cdr.  Since elements of a
stream are computed only when accessed, streams can be infinite.  Once
computed, the value of a stream element is cached in case it is needed
again.  SRFI-41 can be made available with:

     (use-modules (srfi srfi-41))

7.5.27.1 SRFI-41 Stream Fundamentals
....................................

SRFI-41 Streams are based on two mutually-recursive abstract data types:
An object of the ‘stream’ abstract data type is a promise that, when
forced, is either ‘stream-null’ or is an object of type ‘stream-pair’.
An object of the ‘stream-pair’ abstract data type contains a
‘stream-car’ and a ‘stream-cdr’, which must be a ‘stream’.  The
essential feature of streams is the systematic suspensions of the
recursive promises between the two data types.

   The object stored in the ‘stream-car’ of a ‘stream-pair’ is a promise
that is forced the first time the ‘stream-car’ is accessed; its value is
cached in case it is needed again.  The object may have any type, and
different stream elements may have different types.  If the ‘stream-car’
is never accessed, the object stored there is never evaluated.
Likewise, the ‘stream-cdr’ is a promise to return a stream, and is only
forced on demand.

7.5.27.2 SRFI-41 Stream Primitives
..................................

This library provides eight operators: constructors for ‘stream-null’
and ‘stream-pair’s, type predicates for streams and the two kinds of
streams, accessors for both fields of a ‘stream-pair’, and a lambda that
creates procedures that return streams.

 -- Scheme Variable: stream-null
     A promise that, when forced, is a single object, distinguishable
     from all other objects, that represents the null stream.
     ‘stream-null’ is immutable and unique.

 -- Scheme Syntax: stream-cons object-expr stream-expr
     Creates a newly-allocated stream containing a promise that, when
     forced, is a ‘stream-pair’ with OBJECT-EXPR in its ‘stream-car’ and
     STREAM-EXPR in its ‘stream-cdr’.  Neither OBJECT-EXPR nor
     STREAM-EXPR is evaluated when ‘stream-cons’ is called.

     Once created, a ‘stream-pair’ is immutable; there is no
     ‘stream-set-car!’ or ‘stream-set-cdr!’ that modifies an existing
     stream-pair.  There is no dotted-pair or improper stream as with
     lists.

 -- Scheme Procedure: stream? object
     Returns true if OBJECT is a stream, otherwise returns false.  If
     OBJECT is a stream, its promise will not be forced.  If ‘(stream?
     obj)’ returns true, then one of ‘(stream-null? obj)’ or
     ‘(stream-pair? obj)’ will return true and the other will return
     false.

 -- Scheme Procedure: stream-null? object
     Returns true if OBJECT is the distinguished null stream, otherwise
     returns false.  If OBJECT is a stream, its promise will be forced.

 -- Scheme Procedure: stream-pair? object
     Returns true if OBJECT is a ‘stream-pair’ constructed by
     ‘stream-cons’, otherwise returns false.  If OBJECT is a stream, its
     promise will be forced.

 -- Scheme Procedure: stream-car stream
     Returns the object stored in the ‘stream-car’ of STREAM.  An error
     is signalled if the argument is not a ‘stream-pair’.  This causes
     the OBJECT-EXPR passed to ‘stream-cons’ to be evaluated if it had
     not yet been; the value is cached in case it is needed again.

 -- Scheme Procedure: stream-cdr stream
     Returns the stream stored in the ‘stream-cdr’ of STREAM.  An error
     is signalled if the argument is not a ‘stream-pair’.

 -- Scheme Syntax: stream-lambda formals body …
     Creates a procedure that returns a promise to evaluate the BODY of
     the procedure.  The last BODY expression to be evaluated must yield
     a stream.  As with normal ‘lambda’, FORMALS may be a single
     variable name, in which case all the formal arguments are collected
     into a single list, or a list of variable names, which may be null
     if there are no arguments, proper if there are an exact number of
     arguments, or dotted if a fixed number of arguments is to be
     followed by zero or more arguments collected into a list.  BODY
     must contain at least one expression, and may contain internal
     definitions preceding any expressions to be evaluated.

     (define strm123
       (stream-cons 1
         (stream-cons 2
           (stream-cons 3
             stream-null))))

     (stream-car strm123) ⇒ 1
     (stream-car (stream-cdr strm123) ⇒ 2

     (stream-pair?
       (stream-cdr
         (stream-cons (/ 1 0) stream-null))) ⇒ #f

     (stream? (list 1 2 3)) ⇒ #f

     (define iter
       (stream-lambda (f x)
         (stream-cons x (iter f (f x)))))

     (define nats (iter (lambda (x) (+ x 1)) 0))

     (stream-car (stream-cdr nats)) ⇒ 1

     (define stream-add
       (stream-lambda (s1 s2)
         (stream-cons
           (+ (stream-car s1) (stream-car s2))
           (stream-add (stream-cdr s1)
                       (stream-cdr s2)))))

     (define evens (stream-add nats nats))

     (stream-car evens) ⇒ 0
     (stream-car (stream-cdr evens)) ⇒ 2
     (stream-car (stream-cdr (stream-cdr evens))) ⇒ 4

7.5.27.3 SRFI-41 Stream Library
...............................

 -- Scheme Syntax: define-stream (name args …) body …
     Creates a procedure that returns a stream, and may appear anywhere
     a normal ‘define’ may appear, including as an internal definition.
     It may contain internal definitions of its own.  The defined
     procedure takes arguments in the same way as ‘stream-lambda’.
     ‘define-stream’ is syntactic sugar on ‘stream-lambda’; see also
     ‘stream-let’, which is also a sugaring of ‘stream-lambda’.

     A simple version of ‘stream-map’ that takes only a single input
     stream calls itself recursively:

          (define-stream (stream-map proc strm)
            (if (stream-null? strm)
                stream-null
                (stream-cons
                  (proc (stream-car strm))
                  (stream-map proc (stream-cdr strm))))))

 -- Scheme Procedure: list->stream list
     Returns a newly-allocated stream containing the elements from LIST.

 -- Scheme Procedure: port->stream [port]
     Returns a newly-allocated stream containing in its elements the
     characters on the port.  If PORT is not given it defaults to the
     current input port.  The returned stream has finite length and is
     terminated by ‘stream-null’.

     It looks like one use of ‘port->stream’ would be this:

          (define s ;wrong!
            (with-input-from-file filename
              (lambda () (port->stream))))

     But that fails, because ‘with-input-from-file’ is eager, and closes
     the input port prematurely, before the first character is read.  To
     read a file into a stream, say:

          (define-stream (file->stream filename)
            (let ((p (open-input-file filename)))
              (stream-let loop ((c (read-char p)))
                (if (eof-object? c)
                    (begin (close-input-port p)
                           stream-null)
                    (stream-cons c
                      (loop (read-char p)))))))

 -- Scheme Syntax: stream object-expr …
     Creates a newly-allocated stream containing in its elements the
     objects, in order.  The OBJECT-EXPRs are evaluated when they are
     accessed, not when the stream is created.  If no objects are given,
     as in (stream), the null stream is returned.  See also
     ‘list->stream’.

          (define strm123 (stream 1 2 3))

          ; (/ 1 0) not evaluated when stream is created
          (define s (stream 1 (/ 1 0) -1))

 -- Scheme Procedure: stream->list [n] stream
     Returns a newly-allocated list containing in its elements the first
     N items in STREAM.  If STREAM has less than N items, all the items
     in the stream will be included in the returned list.  If N is not
     given it defaults to infinity, which means that unless STREAM is
     finite ‘stream->list’ will never return.

          (stream->list 10
            (stream-map (lambda (x) (* x x))
              (stream-from 0)))
            ⇒ (0 1 4 9 16 25 36 49 64 81)

 -- Scheme Procedure: stream-append stream …
     Returns a newly-allocated stream containing in its elements those
     elements contained in its input STREAMs, in order of input.  If any
     of the input streams is infinite, no elements of any of the
     succeeding input streams will appear in the output stream.  See
     also ‘stream-concat’.

 -- Scheme Procedure: stream-concat stream
     Takes a STREAM consisting of one or more streams and returns a
     newly-allocated stream containing all the elements of the input
     streams.  If any of the streams in the input STREAM is infinite,
     any remaining streams in the input stream will never appear in the
     output stream.  See also ‘stream-append’.

 -- Scheme Procedure: stream-constant object …
     Returns a newly-allocated stream containing in its elements the
     OBJECTs, repeating in succession forever.

          (stream-constant 1) ⇒ 1 1 1 …
          (stream-constant #t #f) ⇒ #t #f #t #f #t #f …

 -- Scheme Procedure: stream-drop n stream
     Returns the suffix of the input STREAM that starts at the next
     element after the first N elements.  The output stream shares
     structure with the input STREAM; thus, promises forced in one
     instance of the stream are also forced in the other instance of the
     stream.  If the input STREAM has less than N elements,
     ‘stream-drop’ returns the null stream.  See also ‘stream-take’.

 -- Scheme Procedure: stream-drop-while pred stream
     Returns the suffix of the input STREAM that starts at the first
     element X for which ‘(pred x)’ returns false.  The output stream
     shares structure with the input STREAM.  See also
     ‘stream-take-while’.

 -- Scheme Procedure: stream-filter pred stream
     Returns a newly-allocated stream that contains only those elements
     X of the input STREAM which satisfy the predicate ‘pred’.

          (stream-filter odd? (stream-from 0))
             ⇒ 1 3 5 7 9 …

 -- Scheme Procedure: stream-fold proc base stream
     Applies a binary procedure PROC to BASE and the first element of
     STREAM to compute a new BASE, then applies the procedure to the new
     BASE and the next element of STREAM to compute a succeeding BASE,
     and so on, accumulating a value that is finally returned as the
     value of ‘stream-fold’ when the end of the stream is reached.
     STREAM must be finite, or ‘stream-fold’ will enter an infinite
     loop.  See also ‘stream-scan’, which is similar to ‘stream-fold’,
     but useful for infinite streams.  For readers familiar with other
     functional languages, this is a left-fold; there is no
     corresponding right-fold, since right-fold relies on finite streams
     that are fully-evaluated, in which case they may as well be
     converted to a list.

 -- Scheme Procedure: stream-for-each proc stream …
     Applies PROC element-wise to corresponding elements of the input
     STREAMs for side-effects; it returns nothing.  ‘stream-for-each’
     stops as soon as any of its input streams is exhausted.

 -- Scheme Procedure: stream-from first [step]
     Creates a newly-allocated stream that contains FIRST as its first
     element and increments each succeeding element by STEP.  If STEP is
     not given it defaults to 1.  FIRST and STEP may be of any numeric
     type.  ‘stream-from’ is frequently useful as a generator in
     ‘stream-of’ expressions.  See also ‘stream-range’ for a similar
     procedure that creates finite streams.

 -- Scheme Procedure: stream-iterate proc base
     Creates a newly-allocated stream containing BASE in its first
     element and applies PROC to each element in turn to determine the
     succeeding element.  See also ‘stream-unfold’ and ‘stream-unfolds’.

 -- Scheme Procedure: stream-length stream
     Returns the number of elements in the STREAM; it does not evaluate
     its elements.  ‘stream-length’ may only be used on finite streams;
     it enters an infinite loop with infinite streams.

 -- Scheme Syntax: stream-let tag ((var expr) …) body …
     Creates a local scope that binds each variable to the value of its
     corresponding expression.  It additionally binds TAG to a procedure
     which takes the bound variables as arguments and BODY as its
     defining expressions, binding the TAG with ‘stream-lambda’.  TAG is
     in scope within body, and may be called recursively.  When the
     expanded expression defined by the ‘stream-let’ is evaluated,
     ‘stream-let’ evaluates the expressions in its BODY in an
     environment containing the newly-bound variables, returning the
     value of the last expression evaluated, which must yield a stream.

     ‘stream-let’ provides syntactic sugar on ‘stream-lambda’, in the
     same manner as normal ‘let’ provides syntactic sugar on normal
     ‘lambda’.  However, unlike normal ‘let’, the TAG is required, not
     optional, because unnamed ‘stream-let’ is meaningless.

     For example, ‘stream-member’ returns the first ‘stream-pair’ of the
     input STRM with a ‘stream-car’ X that satisfies ‘(eql? obj x)’, or
     the null stream if X is not present in STRM.

          (define-stream (stream-member eql? obj strm)
            (stream-let loop ((strm strm))
              (cond ((stream-null? strm) strm)
                    ((eql? obj (stream-car strm)) strm)
                    (else (loop (stream-cdr strm))))))

 -- Scheme Procedure: stream-map proc stream …
     Applies PROC element-wise to corresponding elements of the input
     STREAMs, returning a newly-allocated stream containing elements
     that are the results of those procedure applications.  The output
     stream has as many elements as the minimum-length input stream, and
     may be infinite.

 -- Scheme Syntax: stream-match stream clause …
     Provides pattern-matching for streams.  The input STREAM is an
     expression that evaluates to a stream.  Clauses are of the form
     ‘(pattern [fender] expression)’, consisting of a PATTERN that
     matches a stream of a particular shape, an optional FENDER that
     must succeed if the pattern is to match, and an EXPRESSION that is
     evaluated if the pattern matches.  There are four types of
     patterns:

        • () matches the null stream.

        • (PAT0 PAT1 …) matches a finite stream with length exactly
          equal to the number of pattern elements.

        • (PAT0 PAT1 … ‘.’  PAT-REST) matches an infinite stream, or a
          finite stream with length at least as great as the number of
          pattern elements before the literal dot.

        • PAT matches an entire stream.  Should always appear last in
          the list of clauses; it’s not an error to appear elsewhere,
          but subsequent clauses could never match.

     Each pattern element may be either:

        • An identifier, which matches any stream element.
          Additionally, the value of the stream element is bound to the
          variable named by the identifier, which is in scope in the
          FENDER and EXPRESSION of the corresponding CLAUSE.  Each
          identifier in a single pattern must be unique.

        • A literal underscore (‘_’), which matches any stream element
          but creates no bindings.

     The PATTERNs are tested in order, left-to-right, until a matching
     pattern is found; if FENDER is present, it must evaluate to a true
     value for the match to be successful.  Pattern variables are bound
     in the corresponding FENDER and EXPRESSION.  Once the matching
     PATTERN is found, the corresponding EXPRESSION is evaluated and
     returned as the result of the match.  An error is signaled if no
     pattern matches the input STREAM.

     ‘stream-match’ is often used to distinguish null streams from
     non-null streams, binding HEAD and TAIL:

          (define (len strm)
            (stream-match strm
              (() 0)
              ((head . tail) (+ 1 (len tail)))))

     Fenders can test the common case where two stream elements must be
     identical; the ‘else’ pattern is an identifier bound to the entire
     stream, not a keyword as in ‘cond’.

          (stream-match strm
            ((x y . _) (equal? x y) 'ok)
            (else 'error))

     A more complex example uses two nested matchers to match two
     different stream arguments; ‘(stream-merge lt? . strms)’ stably
     merges two or more streams ordered by the ‘lt?’ predicate:

          (define-stream (stream-merge lt? . strms)
            (define-stream (merge xx yy)
              (stream-match xx (() yy) ((x . xs)
                (stream-match yy (() xx) ((y . ys)
                  (if (lt? y x)
                      (stream-cons y (merge xx ys))
                      (stream-cons x (merge xs yy))))))))
            (stream-let loop ((strms strms))
              (cond ((null? strms) stream-null)
                    ((null? (cdr strms)) (car strms))
                    (else (merge (car strms)
                                 (apply stream-merge lt?
                                   (cdr strms)))))))

 -- Scheme Syntax: stream-of expr clause …
     Provides the syntax of stream comprehensions, which generate
     streams by means of looping expressions.  The result is a stream of
     objects of the type returned by EXPR.  There are four types of
     clauses:

        • (VAR ‘in’ STREAM-EXPR) loops over the elements of STREAM-EXPR,
          in order from the start of the stream, binding each element of
          the stream in turn to VAR.  ‘stream-from’ and ‘stream-range’
          are frequently useful as generators for STREAM-EXPR.

        • (VAR ‘is’ EXPR) binds VAR to the value obtained by evaluating
          EXPR.

        • (PRED EXPR) includes in the output stream only those elements
          X which satisfy the predicate PRED.

     The scope of variables bound in the stream comprehension is the
     clauses to the right of the binding clause (but not the binding
     clause itself) plus the result expression.

     When two or more generators are present, the loops are processed as
     if they are nested from left to right; that is, the rightmost
     generator varies fastest.  A consequence of this is that only the
     first generator may be infinite and all subsequent generators must
     be finite.  If no generators are present, the result of a stream
     comprehension is a stream containing the result expression; thus,
     ‘(stream-of 1)’ produces a finite stream containing only the
     element 1.

          (stream-of (* x x)
            (x in (stream-range 0 10))
            (even? x))
            ⇒ 0 4 16 36 64

          (stream-of (list a b)
            (a in (stream-range 1 4))
            (b in (stream-range 1 3)))
            ⇒ (1 1) (1 2) (2 1) (2 2) (3 1) (3 2)

          (stream-of (list i j)
            (i in (stream-range 1 5))
            (j in (stream-range (+ i 1) 5)))
            ⇒ (1 2) (1 3) (1 4) (2 3) (2 4) (3 4)

 -- Scheme Procedure: stream-range first past [step]
     Creates a newly-allocated stream that contains FIRST as its first
     element and increments each succeeding element by STEP.  The stream
     is finite and ends before PAST, which is not an element of the
     stream.  If STEP is not given it defaults to 1 if FIRST is less
     than past and -1 otherwise.  FIRST, PAST and STEP may be of any
     real numeric type.  ‘stream-range’ is frequently useful as a
     generator in ‘stream-of’ expressions.  See also ‘stream-from’ for a
     similar procedure that creates infinite streams.

          (stream-range 0 10) ⇒ 0 1 2 3 4 5 6 7 8 9
          (stream-range 0 10 2) ⇒ 0 2 4 6 8

     Successive elements of the stream are calculated by adding STEP to
     FIRST, so if any of FIRST, PAST or STEP are inexact, the length of
     the output stream may differ from ‘(ceiling (- (/ (- past first)
     step) 1)’.

 -- Scheme Procedure: stream-ref stream n
     Returns the Nth element of stream, counting from zero.  An error is
     signaled if N is greater than or equal to the length of stream.

          (define (fact n)
            (stream-ref
              (stream-scan * 1 (stream-from 1))
              n))

 -- Scheme Procedure: stream-reverse stream
     Returns a newly-allocated stream containing the elements of the
     input STREAM but in reverse order.  ‘stream-reverse’ may only be
     used with finite streams; it enters an infinite loop with infinite
     streams.  ‘stream-reverse’ does not force evaluation of the
     elements of the stream.

 -- Scheme Procedure: stream-scan proc base stream
     Accumulates the partial folds of an input STREAM into a
     newly-allocated output stream.  The output stream is the BASE
     followed by ‘(stream-fold proc base (stream-take i stream))’ for
     each of the first I elements of STREAM.

          (stream-scan + 0 (stream-from 1))
            ⇒ (stream 0 1 3 6 10 15 …)

          (stream-scan * 1 (stream-from 1))
            ⇒ (stream 1 1 2 6 24 120 …)

 -- Scheme Procedure: stream-take n stream
     Returns a newly-allocated stream containing the first N elements of
     the input STREAM.  If the input STREAM has less than N elements, so
     does the output stream.  See also ‘stream-drop’.

 -- Scheme Procedure: stream-take-while pred stream
     Takes a predicate and a ‘stream’ and returns a newly-allocated
     stream containing those elements ‘x’ that form the maximal prefix
     of the input stream which satisfy PRED.  See also
     ‘stream-drop-while’.

 -- Scheme Procedure: stream-unfold map pred gen base
     The fundamental recursive stream constructor.  It constructs a
     stream by repeatedly applying GEN to successive values of BASE, in
     the manner of ‘stream-iterate’, then applying MAP to each of the
     values so generated, appending each of the mapped values to the
     output stream as long as ‘(pred? base)’ returns a true value.  See
     also ‘stream-iterate’ and ‘stream-unfolds’.

     The expression below creates the finite stream ‘0 1 4 9 16 25 36 49
     64 81’.  Initially the BASE is 0, which is less than 10, so MAP
     squares the BASE and the mapped value becomes the first element of
     the output stream.  Then GEN increments the BASE by 1, so it
     becomes 1; this is less than 10, so MAP squares the new BASE and 1
     becomes the second element of the output stream.  And so on, until
     the base becomes 10, when PRED stops the recursion and stream-null
     ends the output stream.

          (stream-unfold
            (lambda (x) (expt x 2)) ; map
            (lambda (x) (< x 10))   ; pred?
            (lambda (x) (+ x 1))    ; gen
            0)                      ; base

 -- Scheme Procedure: stream-unfolds proc seed
     Returns N newly-allocated streams containing those elements
     produced by successive calls to the generator PROC, which takes the
     current SEED as its argument and returns N+1 values

     (PROC SEED) ⇒ SEED RESULT_0 … RESULT_N-1

     where the returned SEED is the input SEED to the next call to the
     generator and RESULT_I indicates how to produce the next element of
     the Ith result stream:

        • (VALUE): VALUE is the next car of the result stream.

        • ‘#f’: no value produced by this iteration of the generator
          PROC for the result stream.

        • (): the end of the result stream.

     It may require multiple calls of PROC to produce the next element
     of any particular result stream.  See also ‘stream-iterate’ and
     ‘stream-unfold’.

          (define (stream-partition pred? strm)
            (stream-unfolds
              (lambda (s)
                (if (stream-null? s)
                    (values s '() '())
                    (let ((a (stream-car s))
                          (d (stream-cdr s)))
                      (if (pred? a)
                          (values d (list a) #f)
                          (values d #f (list a))))))
              strm))

          (call-with-values
            (lambda ()
              (stream-partition odd?
                (stream-range 1 6)))
            (lambda (odds evens)
              (list (stream->list odds)
                    (stream->list evens))))
            ⇒ ((1 3 5) (2 4))

 -- Scheme Procedure: stream-zip stream …
     Returns a newly-allocated stream in which each element is a list
     (not a stream) of the corresponding elements of the input STREAMs.
     The output stream is as long as the shortest input STREAM, if any
     of the input STREAMs is finite, or is infinite if all the input
     STREAMs are infinite.

7.5.28 SRFI-42 - Eager Comprehensions
-------------------------------------

See the specification of SRFI-42
(http://srfi.schemers.org/srfi-42/srfi-42.html).

7.5.29 SRFI-43 - Vector Library
-------------------------------

This subsection is based on the specification of SRFI-43
(http://srfi.schemers.org/srfi-43/srfi-43.html) by Taylor Campbell.

SRFI-43 implements a comprehensive library of vector operations.  It can
be made available with:

     (use-modules (srfi srfi-43))

7.5.29.1 SRFI-43 Constructors
.............................

 -- Scheme Procedure: make-vector size [fill]
     Create and return a vector of size SIZE, optionally filling it with
     FILL.  The default value of FILL is unspecified.

          (make-vector 5 3) ⇒ #(3 3 3 3 3)

 -- Scheme Procedure: vector x …
     Create and return a vector whose elements are X ....

          (vector 0 1 2 3 4) ⇒ #(0 1 2 3 4)

 -- Scheme Procedure: vector-unfold f length initial-seed …
     The fundamental vector constructor.  Create a vector whose length
     is LENGTH and iterates across each index k from 0 up to LENGTH - 1,
     applying F at each iteration to the current index and current
     seeds, in that order, to receive n + 1 values: first, the element
     to put in the kth slot of the new vector and n new seeds for the
     next iteration.  It is an error for the number of seeds to vary
     between iterations.

          (vector-unfold (lambda (i x) (values x (- x 1)))
                         10 0)
          ⇒ #(0 -1 -2 -3 -4 -5 -6 -7 -8 -9)

          (vector-unfold values 10)
          ⇒ #(0 1 2 3 4 5 6 7 8 9)

 -- Scheme Procedure: vector-unfold-right f length initial-seed …
     Like ‘vector-unfold’, but it uses F to generate elements from
     right-to-left, rather than left-to-right.

          (vector-unfold-right (lambda (i x) (values x (+ x 1)))
                               10 0)
          ⇒ #(9 8 7 6 5 4 3 2 1 0)

 -- Scheme Procedure: vector-copy vec [start [end [fill]]]
     Allocate a new vector whose length is END - START and fills it with
     elements from VEC, taking elements from VEC starting at index START
     and stopping at index END.  START defaults to 0 and END defaults to
     the value of ‘(vector-length vec)’.  If END extends beyond the
     length of VEC, the slots in the new vector that obviously cannot be
     filled by elements from VEC are filled with FILL, whose default
     value is unspecified.

          (vector-copy '#(a b c d e f g h i))
          ⇒ #(a b c d e f g h i)

          (vector-copy '#(a b c d e f g h i) 6)
          ⇒ #(g h i)

          (vector-copy '#(a b c d e f g h i) 3 6)
          ⇒ #(d e f)

          (vector-copy '#(a b c d e f g h i) 6 12 'x)
          ⇒ #(g h i x x x)

 -- Scheme Procedure: vector-reverse-copy vec [start [end]]
     Like ‘vector-copy’, but it copies the elements in the reverse order
     from VEC.

          (vector-reverse-copy '#(5 4 3 2 1 0) 1 5)
          ⇒ #(1 2 3 4)

 -- Scheme Procedure: vector-append vec …
     Return a newly allocated vector that contains all elements in order
     from the subsequent locations in VEC ....

          (vector-append '#(a) '#(b c d))
          ⇒ #(a b c d)

 -- Scheme Procedure: vector-concatenate list-of-vectors
     Append each vector in LIST-OF-VECTORS.  Equivalent to ‘(apply
     vector-append list-of-vectors)’.

          (vector-concatenate '(#(a b) #(c d)))
          ⇒ #(a b c d)

7.5.29.2 SRFI-43 Predicates
...........................

 -- Scheme Procedure: vector? obj
     Return true if OBJ is a vector, else return false.

 -- Scheme Procedure: vector-empty? vec
     Return true if VEC is empty, i.e.  its length is 0, else return
     false.

 -- Scheme Procedure: vector= elt=? vec …
     Return true if the vectors VEC … have equal lengths and equal
     elements according to ELT=?.  ELT=? is always applied to two
     arguments.  Element comparison must be consistent with ‘eq?’ in the
     following sense: if ‘(eq? a b)’ returns true, then ‘(elt=? a b)’
     must also return true.  The order in which comparisons are
     performed is unspecified.

7.5.29.3 SRFI-43 Selectors
..........................

 -- Scheme Procedure: vector-ref vec i
     Return the element at index I in VEC.  Indexing is based on zero.

 -- Scheme Procedure: vector-length vec
     Return the length of VEC.

7.5.29.4 SRFI-43 Iteration
..........................

 -- Scheme Procedure: vector-fold kons knil vec1 vec2 …
     The fundamental vector iterator.  KONS is iterated over each index
     in all of the vectors, stopping at the end of the shortest; KONS is
     applied as
          (kons i state (vector-ref vec1 i) (vector-ref vec2 i) ...)
     where STATE is the current state value, and I is the current index.
     The current state value begins with KNIL, and becomes whatever KONS
     returned at the respective iteration.  The iteration is strictly
     left-to-right.

 -- Scheme Procedure: vector-fold-right kons knil vec1 vec2 …
     Similar to ‘vector-fold’, but it iterates right-to-left instead of
     left-to-right.

 -- Scheme Procedure: vector-map f vec1 vec2 …
     Return a new vector of the shortest size of the vector arguments.
     Each element at index i of the new vector is mapped from the old
     vectors by
          (f i (vector-ref vec1 i) (vector-ref vec2 i) ...)
     The dynamic order of application of F is unspecified.

 -- Scheme Procedure: vector-map! f vec1 vec2 …
     Similar to ‘vector-map’, but rather than mapping the new elements
     into a new vector, the new mapped elements are destructively
     inserted into VEC1.  The dynamic order of application of F is
     unspecified.

 -- Scheme Procedure: vector-for-each f vec1 vec2 …
     Call ‘(f i (vector-ref vec1 i) (vector-ref vec2 i) ...)’ for each
     index i less than the length of the shortest vector passed.  The
     iteration is strictly left-to-right.

 -- Scheme Procedure: vector-count pred? vec1 vec2 …
     Count the number of parallel elements in the vectors that satisfy
     PRED?, which is applied, for each index i less than the length of
     the smallest vector, to i and each parallel element in the vectors
     at that index, in order.

          (vector-count (lambda (i elt) (even? elt))
                        '#(3 1 4 1 5 9 2 5 6))
          ⇒ 3
          (vector-count (lambda (i x y) (< x y))
                        '#(1 3 6 9) '#(2 4 6 8 10 12))
          ⇒ 2

7.5.29.5 SRFI-43 Searching
..........................

 -- Scheme Procedure: vector-index pred? vec1 vec2 …
     Find and return the index of the first elements in VEC1 VEC2 … that
     satisfy PRED?.  If no matching element is found by the end of the
     shortest vector, return ‘#f’.

          (vector-index even? '#(3 1 4 1 5 9))
          ⇒ 2
          (vector-index < '#(3 1 4 1 5 9 2 5 6) '#(2 7 1 8 2))
          ⇒ 1
          (vector-index = '#(3 1 4 1 5 9 2 5 6) '#(2 7 1 8 2))
          ⇒ #f

 -- Scheme Procedure: vector-index-right pred? vec1 vec2 …
     Like ‘vector-index’, but it searches right-to-left, rather than
     left-to-right.  Note that the SRFI 43 specification requires that
     all the vectors must have the same length, but both the SRFI 43
     reference implementation and Guile’s implementation allow vectors
     with unequal lengths, and start searching from the last index of
     the shortest vector.

 -- Scheme Procedure: vector-skip pred? vec1 vec2 …
     Find and return the index of the first elements in VEC1 VEC2 … that
     do not satisfy PRED?.  If no matching element is found by the end
     of the shortest vector, return ‘#f’.  Equivalent to ‘vector-index’
     but with the predicate inverted.

          (vector-skip number? '#(1 2 a b 3 4 c d)) ⇒ 2

 -- Scheme Procedure: vector-skip-right pred? vec1 vec2 …
     Like ‘vector-skip’, but it searches for a non-matching element
     right-to-left, rather than left-to-right.  Note that the SRFI 43
     specification requires that all the vectors must have the same
     length, but both the SRFI 43 reference implementation and Guile’s
     implementation allow vectors with unequal lengths, and start
     searching from the last index of the shortest vector.

 -- Scheme Procedure: vector-binary-search vec value cmp [start [end]]
     Find and return an index of VEC between START and END whose value
     is VALUE using a binary search.  If no matching element is found,
     return ‘#f’.  The default START is 0 and the default END is the
     length of VEC.

     CMP must be a procedure of two arguments such that ‘(cmp a b)’
     returns a negative integer if a < b, a positive integer if a > b,
     or zero if a = b.  The elements of VEC must be sorted in
     non-decreasing order according to CMP.

     Note that SRFI 43 does not document the START and END arguments,
     but both its reference implementation and Guile’s implementation
     support them.

          (define (char-cmp c1 c2)
            (cond ((char<? c1 c2) -1)
                  ((char>? c1 c2) 1)
                  (else 0)))

          (vector-binary-search '#(#\a #\b #\c #\d #\e #\f #\g #\h)
                                #\g
                                char-cmp)
          ⇒ 6

 -- Scheme Procedure: vector-any pred? vec1 vec2 …
     Find the first parallel set of elements from VEC1 VEC2 … for which
     PRED? returns a true value.  If such a parallel set of elements
     exists, ‘vector-any’ returns the value that PRED? returned for that
     set of elements.  The iteration is strictly left-to-right.

 -- Scheme Procedure: vector-every pred? vec1 vec2 …
     If, for every index i between 0 and the length of the shortest
     vector argument, the set of elements ‘(vector-ref vec1 i)’
     ‘(vector-ref vec2 i)’ … satisfies PRED?, ‘vector-every’ returns the
     value that PRED? returned for the last set of elements, at the last
     index of the shortest vector.  Otherwise it returns ‘#f’.  The
     iteration is strictly left-to-right.

7.5.29.6 SRFI-43 Mutators
.........................

 -- Scheme Procedure: vector-set! vec i value
     Assign the contents of the location at I in VEC to VALUE.

 -- Scheme Procedure: vector-swap! vec i j
     Swap the values of the locations in VEC at I and J.

 -- Scheme Procedure: vector-fill! vec fill [start [end]]
     Assign the value of every location in VEC between START and END to
     FILL.  START defaults to 0 and END defaults to the length of VEC.

 -- Scheme Procedure: vector-reverse! vec [start [end]]
     Destructively reverse the contents of VEC between START and END.
     START defaults to 0 and END defaults to the length of VEC.

 -- Scheme Procedure: vector-copy! target tstart source [sstart [send]]
     Copy a block of elements from SOURCE to TARGET, both of which must
     be vectors, starting in TARGET at TSTART and starting in SOURCE at
     SSTART, ending when (SEND - SSTART) elements have been copied.  It
     is an error for TARGET to have a length less than (TSTART + SEND -
     SSTART).  SSTART defaults to 0 and SEND defaults to the length of
     SOURCE.

 -- Scheme Procedure: vector-reverse-copy! target tstart source [sstart
          [send]]
     Like ‘vector-copy!’, but this copies the elements in the reverse
     order.  It is an error if TARGET and SOURCE are identical vectors
     and the TARGET and SOURCE ranges overlap; however, if TSTART =
     SSTART, ‘vector-reverse-copy!’ behaves as ‘(vector-reverse! target
     tstart send)’ would.

7.5.29.7 SRFI-43 Conversion
...........................

 -- Scheme Procedure: vector->list vec [start [end]]
     Return a newly allocated list containing the elements in VEC
     between START and END.  START defaults to 0 and END defaults to the
     length of VEC.

 -- Scheme Procedure: reverse-vector->list vec [start [end]]
     Like ‘vector->list’, but the resulting list contains the specified
     range of elements of VEC in reverse order.

 -- Scheme Procedure: list->vector proper-list [start [end]]
     Return a newly allocated vector of the elements from PROPER-LIST
     with indices between START and END.  START defaults to 0 and END
     defaults to the length of PROPER-LIST.  Note that SRFI 43 does not
     document the START and END arguments, but both its reference
     implementation and Guile’s implementation support them.

 -- Scheme Procedure: reverse-list->vector proper-list [start [end]]
     Like ‘list->vector’, but the resulting vector contains the
     specified range of elements of PROPER-LIST in reverse order.  Note
     that SRFI 43 does not document the START and END arguments, but
     both its reference implementation and Guile’s implementation
     support them.

7.5.30 SRFI-45 - Primitives for Expressing Iterative Lazy Algorithms
--------------------------------------------------------------------

This subsection is based on the specification of SRFI-45
(http://srfi.schemers.org/srfi-45/srfi-45.html) written by André van
Tonder.

   Lazy evaluation is traditionally simulated in Scheme using ‘delay’
and ‘force’.  However, these primitives are not powerful enough to
express a large class of lazy algorithms that are iterative.  Indeed, it
is folklore in the Scheme community that typical iterative lazy
algorithms written using delay and force will often require unbounded
memory.

   This SRFI provides set of three operations: {‘lazy’, ‘delay’,
‘force’}, which allow the programmer to succinctly express lazy
algorithms while retaining bounded space behavior in cases that are
properly tail-recursive.  A general recipe for using these primitives is
provided.  An additional procedure ‘eager’ is provided for the
construction of eager promises in cases where efficiency is a concern.

   Although this SRFI redefines ‘delay’ and ‘force’, the extension is
conservative in the sense that the semantics of the subset {‘delay’,
‘force’} in isolation (i.e., as long as the program does not use ‘lazy’)
agrees with that in R5RS. In other words, no program that uses the R5RS
definitions of delay and force will break if those definition are
replaced by the SRFI-45 definitions of delay and force.

   Guile also adds ‘promise?’ to the list of exports, which is not part
of the official SRFI-45.

 -- Scheme Procedure: promise? obj
     Return true if OBJ is an SRFI-45 promise, otherwise return false.

 -- Scheme Syntax: delay expression
     Takes an expression of arbitrary type A and returns a promise of
     type ‘(Promise A)’ which at some point in the future may be asked
     (by the ‘force’ procedure) to evaluate the expression and deliver
     the resulting value.

 -- Scheme Syntax: lazy expression
     Takes an expression of type ‘(Promise A)’ and returns a promise of
     type ‘(Promise A)’ which at some point in the future may be asked
     (by the ‘force’ procedure) to evaluate the expression and deliver
     the resulting promise.

 -- Scheme Procedure: force expression
     Takes an argument of type ‘(Promise A)’ and returns a value of type
     A as follows: If a value of type A has been computed for the
     promise, this value is returned.  Otherwise, the promise is first
     evaluated, then overwritten by the obtained promise or value, and
     then force is again applied (iteratively) to the promise.

 -- Scheme Procedure: eager expression
     Takes an argument of type A and returns a value of type ‘(Promise
     A)’.  As opposed to ‘delay’, the argument is evaluated eagerly.
     Semantically, writing ‘(eager expression)’ is equivalent to writing

          (let ((value expression)) (delay value)).

     However, the former is more efficient since it does not require
     unnecessary creation and evaluation of thunks.  We also have the
     equivalence

          (delay expression) = (lazy (eager expression))

   The following reduction rules may be helpful for reasoning about
these primitives.  However, they do not express the memoization and
memory usage semantics specified above:

     (force (delay expression)) -> expression
     (force (lazy  expression)) -> (force expression)
     (force (eager value))      -> value

Correct usage
.............

We now provide a general recipe for using the primitives {‘lazy’,
‘delay’, ‘force’} to express lazy algorithms in Scheme.  The
transformation is best described by way of an example: Consider the
stream-filter algorithm, expressed in a hypothetical lazy language as

     (define (stream-filter p? s)
       (if (null? s) '()
           (let ((h (car s))
                 (t (cdr s)))
             (if (p? h)
                 (cons h (stream-filter p? t))
                 (stream-filter p? t)))))

   This algorithm can be expressed as follows in Scheme:

     (define (stream-filter p? s)
       (lazy
          (if (null? (force s)) (delay '())
              (let ((h (car (force s)))
                    (t (cdr (force s))))
                (if (p? h)
                    (delay (cons h (stream-filter p? t)))
                    (stream-filter p? t))))))

   In other words, we

   • wrap all constructors (e.g., ‘'()’, ‘cons’) with ‘delay’,
   • apply ‘force’ to arguments of deconstructors (e.g., ‘car’, ‘cdr’
     and ‘null?’),
   • wrap procedure bodies with ‘(lazy ...)’.

7.5.31 SRFI-46 Basic syntax-rules Extensions
--------------------------------------------

Guile’s core ‘syntax-rules’ supports the extensions specified by
SRFI-46/R7RS. Tail patterns have been supported since at least Guile
2.0, and custom ellipsis identifiers have been supported since Guile
2.0.10.  *Note Syntax Rules::.

7.5.32 SRFI-55 - Requiring Features
-----------------------------------

SRFI-55 provides ‘require-extension’ which is a portable mechanism to
load selected SRFI modules.  This is implemented in the Guile core,
there’s no module needed to get SRFI-55 itself.

 -- library syntax: require-extension clause1 clause2 …
     Require the features of CLAUSE1 CLAUSE2 … , throwing an error if
     any are unavailable.

     A CLAUSE is of the form ‘(IDENTIFIER arg...)’.  The only IDENTIFIER
     currently supported is ‘srfi’ and the arguments are SRFI numbers.
     For example to get SRFI-1 and SRFI-6,

          (require-extension (srfi 1 6))

     ‘require-extension’ can only be used at the top-level.

     A Guile-specific program can simply ‘use-modules’ to load SRFIs not
     already in the core, ‘require-extension’ is for programs designed
     to be portable to other Scheme implementations.

7.5.33 SRFI-60 - Integers as Bits
---------------------------------

This SRFI provides various functions for treating integers as bits and
for bitwise manipulations.  These functions can be obtained with,

     (use-modules (srfi srfi-60))

   Integers are treated as infinite precision twos-complement, the same
as in the core logical functions (*note Bitwise Operations::).  And
likewise bit indexes start from 0 for the least significant bit.  The
following functions in this SRFI are already in the Guile core,

     ‘logand’, ‘logior’, ‘logxor’, ‘lognot’, ‘logtest’, ‘logcount’,
     ‘integer-length’, ‘logbit?’, ‘ash’


 -- Function: bitwise-and n1 ...
 -- Function: bitwise-ior n1 ...
 -- Function: bitwise-xor n1 ...
 -- Function: bitwise-not n
 -- Function: any-bits-set? j k
 -- Function: bit-set? index n
 -- Function: arithmetic-shift n count
 -- Function: bit-field n start end
 -- Function: bit-count n
     Aliases for ‘logand’, ‘logior’, ‘logxor’, ‘lognot’, ‘logtest’,
     ‘logbit?’, ‘ash’, ‘bit-extract’ and ‘logcount’ respectively.

     Note that the name ‘bit-count’ conflicts with ‘bit-count’ in the
     core (*note Bit Vectors::).

 -- Function: bitwise-if mask n1 n0
 -- Function: bitwise-merge mask n1 n0
     Return an integer with bits selected from N1 and N0 according to
     MASK.  Those bits where MASK has 1s are taken from N1, and those
     where MASK has 0s are taken from N0.

          (bitwise-if 3 #b0101 #b1010) ⇒ 9

 -- Function: log2-binary-factors n
 -- Function: first-set-bit n
     Return a count of how many factors of 2 are present in N.  This is
     also the bit index of the lowest 1 bit in N.  If N is 0, the return
     is -1.

          (log2-binary-factors 6) ⇒ 1
          (log2-binary-factors -8) ⇒ 3

 -- Function: copy-bit index n newbit
     Return N with the bit at INDEX set according to NEWBIT.  NEWBIT
     should be ‘#t’ to set the bit to 1, or ‘#f’ to set it to 0.  Bits
     other than at INDEX are unchanged in the return.

          (copy-bit 1 #b0101 #t) ⇒ 7

 -- Function: copy-bit-field n newbits start end
     Return N with the bits from START (inclusive) to END (exclusive)
     changed to the value NEWBITS.

     The least significant bit in NEWBITS goes to START, the next to
     START+1, etc.  Anything in NEWBITS past the END given is ignored.

          (copy-bit-field #b10000 #b11 1 3) ⇒ #b10110

 -- Function: rotate-bit-field n count start end
     Return N with the bit field from START (inclusive) to END
     (exclusive) rotated upwards by COUNT bits.

     COUNT can be positive or negative, and it can be more than the
     field width (it’ll be reduced modulo the width).

          (rotate-bit-field #b0110 2 1 4) ⇒ #b1010

 -- Function: reverse-bit-field n start end
     Return N with the bits from START (inclusive) to END (exclusive)
     reversed.

          (reverse-bit-field #b101001 2 4) ⇒ #b100101

 -- Function: integer->list n [len]
     Return bits from N in the form of a list of ‘#t’ for 1 and ‘#f’ for
     0.  The least significant LEN bits are returned, and the first list
     element is the most significant of those bits.  If LEN is not
     given, the default is ‘(integer-length N)’ (*note Bitwise
     Operations::).

          (integer->list 6)   ⇒ (#t #t #f)
          (integer->list 1 4) ⇒ (#f #f #f #t)

 -- Function: list->integer lst
 -- Function: booleans->integer bool…
     Return an integer formed bitwise from the given LST list of
     booleans, or for ‘booleans->integer’ from the BOOL arguments.

     Each boolean is ‘#t’ for a 1 and ‘#f’ for a 0.  The first element
     becomes the most significant bit in the return.

          (list->integer '(#t #f #t #f)) ⇒ 10

7.5.34 SRFI-61 - A more general ‘cond’ clause
---------------------------------------------

This SRFI extends RnRS ‘cond’ to support test expressions that return
multiple values, as well as arbitrary definitions of test success.  SRFI
61 is implemented in the Guile core; there’s no module needed to get
SRFI-61 itself.  Extended ‘cond’ is documented in *note Simple
Conditional Evaluation: Conditionals.

7.5.35 SRFI-62 - S-expression comments.
---------------------------------------

Starting from version 2.0, Guile’s ‘read’ supports SRFI-62/R7RS
S-expression comments by default.

7.5.36 SRFI-64 - A Scheme API for test suites.
----------------------------------------------

See the specification of SRFI-64
(http://srfi.schemers.org/srfi-64/srfi-64.html).

7.5.37 SRFI-67 - Compare procedures
-----------------------------------

See the specification of SRFI-67
(http://srfi.schemers.org/srfi-67/srfi-67.html).

7.5.38 SRFI-69 - Basic hash tables
----------------------------------

This is a portable wrapper around Guile’s built-in hash table and weak
table support.  *Note Hash Tables::, for information on that built-in
support.  Above that, this hash-table interface provides association of
equality and hash functions with tables at creation time, so variants of
each function are not required, as well as a procedure that takes care
of most uses for Guile hash table handles, which this SRFI does not
provide as such.

   Access it with:

     (use-modules (srfi srfi-69))

7.5.38.1 Creating hash tables
.............................

 -- Scheme Procedure: make-hash-table [equal-proc hash-proc #:weak
          weakness start-size]
     Create and answer a new hash table with EQUAL-PROC as the equality
     function and HASH-PROC as the hashing function.

     By default, EQUAL-PROC is ‘equal?’.  It can be any two-argument
     procedure, and should answer whether two keys are the same for this
     table’s purposes.

     My default HASH-PROC assumes that ‘equal-proc’ is no coarser than
     ‘equal?’ unless it is literally ‘string-ci=?’.  If provided,
     HASH-PROC should be a two-argument procedure that takes a key and
     the current table size, and answers a reasonably good hash integer
     between 0 (inclusive) and the size (exclusive).

     WEAKNESS should be ‘#f’ or a symbol indicating how “weak” the hash
     table is:

     ‘#f’
          An ordinary non-weak hash table.  This is the default.

     ‘key’
          When the key has no more non-weak references at GC, remove
          that entry.

     ‘value’
          When the value has no more non-weak references at GC, remove
          that entry.

     ‘key-or-value’
          When either has no more non-weak references at GC, remove the
          association.

     As a legacy of the time when Guile couldn’t grow hash tables,
     START-SIZE is an optional integer argument that specifies the
     approximate starting size for the hash table, which will be rounded
     to an algorithmically-sounder number.

   By "coarser" than ‘equal?’, we mean that for all X and Y values where
‘(EQUAL-PROC X Y)’, ‘(equal? X Y)’ as well.  If that does not hold for
your EQUAL-PROC, you must provide a HASH-PROC.

   In the case of weak tables, remember that "references" above always
refers to ‘eq?’-wise references.  Just because you have a reference to
some string ‘"foo"’ doesn’t mean that an association with key ‘"foo"’ in
a weak-key table _won’t_ be collected; it only counts as a reference if
the two ‘"foo"’s are ‘eq?’, regardless of EQUAL-PROC.  As such, it is
usually only sensible to use ‘eq?’ and ‘hashq’ as the equivalence and
hash functions for a weak table.  *Note Weak References::, for more
information on Guile’s built-in weak table support.

 -- Scheme Procedure: alist->hash-table alist [equal-proc hash-proc
          #:weak weakness start-size]
     As with ‘make-hash-table’, but initialize it with the associations
     in ALIST.  Where keys are repeated in ALIST, the leftmost
     association takes precedence.

7.5.38.2 Accessing table items
..............................

 -- Scheme Procedure: hash-table-ref table key [default-thunk]
 -- Scheme Procedure: hash-table-ref/default table key default
     Answer the value associated with KEY in TABLE.  If KEY is not
     present, answer the result of invoking the thunk DEFAULT-THUNK,
     which signals an error instead by default.

     ‘hash-table-ref/default’ is a variant that requires a third
     argument, DEFAULT, and answers DEFAULT itself instead of invoking
     it.

 -- Scheme Procedure: hash-table-set! table key new-value
     Set KEY to NEW-VALUE in TABLE.

 -- Scheme Procedure: hash-table-delete! table key
     Remove the association of KEY in TABLE, if present.  If absent, do
     nothing.

 -- Scheme Procedure: hash-table-exists? table key
     Answer whether KEY has an association in TABLE.

 -- Scheme Procedure: hash-table-update! table key modifier
          [default-thunk]
 -- Scheme Procedure: hash-table-update!/default table key modifier
          default
     Replace KEY’s associated value in TABLE by invoking MODIFIER with
     one argument, the old value.

     If KEY is not present, and DEFAULT-THUNK is provided, invoke it
     with no arguments to get the “old value” to be passed to MODIFIER
     as above.  If DEFAULT-THUNK is not provided in such a case, signal
     an error.

     ‘hash-table-update!/default’ is a variant that requires the fourth
     argument, which is used directly as the “old value” rather than as
     a thunk to be invoked to retrieve the “old value”.

7.5.38.3 Table properties
.........................

 -- Scheme Procedure: hash-table-size table
     Answer the number of associations in TABLE.  This is guaranteed to
     run in constant time for non-weak tables.

 -- Scheme Procedure: hash-table-keys table
     Answer an unordered list of the keys in TABLE.

 -- Scheme Procedure: hash-table-values table
     Answer an unordered list of the values in TABLE.

 -- Scheme Procedure: hash-table-walk table proc
     Invoke PROC once for each association in TABLE, passing the key and
     value as arguments.

 -- Scheme Procedure: hash-table-fold table proc init
     Invoke ‘(PROC KEY VALUE PREVIOUS)’ for each KEY and VALUE in TABLE,
     where PREVIOUS is the result of the previous invocation, using INIT
     as the first PREVIOUS value.  Answer the final PROC result.

 -- Scheme Procedure: hash-table->alist table
     Answer an alist where each association in TABLE is an association
     in the result.

7.5.38.4 Hash table algorithms
..............................

Each hash table carries an "equivalence function" and a "hash function",
used to implement key lookups.  Beginning users should follow the rules
for consistency of the default HASH-PROC specified above.  Advanced
users can use these to implement their own equivalence and hash
functions for specialized lookup semantics.

 -- Scheme Procedure: hash-table-equivalence-function hash-table
 -- Scheme Procedure: hash-table-hash-function hash-table
     Answer the equivalence and hash function of HASH-TABLE,
     respectively.

 -- Scheme Procedure: hash obj [size]
 -- Scheme Procedure: string-hash obj [size]
 -- Scheme Procedure: string-ci-hash obj [size]
 -- Scheme Procedure: hash-by-identity obj [size]
     Answer a hash value appropriate for equality predicate ‘equal?’,
     ‘string=?’, ‘string-ci=?’, and ‘eq?’, respectively.

   ‘hash’ is a backwards-compatible replacement for Guile’s built-in
‘hash’.

7.5.39 SRFI-87 => in case clauses
---------------------------------

Starting from version 2.0.6, Guile’s core ‘case’ syntax supports ‘=>’ in
clauses, as specified by SRFI-87/R7RS. *Note Conditionals::.

7.5.40 SRFI-88 Keyword Objects
------------------------------

SRFI-88 (http://srfi.schemers.org/srfi-88/srfi-88.html) provides
"keyword objects", which are equivalent to Guile’s keywords (*note
Keywords::).  SRFI-88 keywords can be entered using the "postfix keyword
syntax", which consists of an identifier followed by ‘:’ (*note
‘postfix’ keyword syntax: Scheme Read.).  SRFI-88 can be made available
with:

     (use-modules (srfi srfi-88))

   Doing so installs the right reader option for keyword syntax, using
‘(read-set! keywords 'postfix)’.  It also provides the procedures
described below.

 -- Scheme Procedure: keyword? obj
     Return ‘#t’ if OBJ is a keyword.  This is the same procedure as the
     same-named built-in procedure (*note ‘keyword?’: Keyword
     Procedures.).

          (keyword? foo:)         ⇒ #t
          (keyword? 'foo:)        ⇒ #t
          (keyword? "foo")        ⇒ #f

 -- Scheme Procedure: keyword->string kw
     Return the name of KW as a string, i.e., without the trailing
     colon.  The returned string may not be modified, e.g., with
     ‘string-set!’.

          (keyword->string foo:)  ⇒ "foo"

 -- Scheme Procedure: string->keyword str
     Return the keyword object whose name is STR.

          (keyword->string (string->keyword "a b c"))     ⇒ "a b c"

7.5.41 SRFI-98 Accessing environment variables.
-----------------------------------------------

This is a portable wrapper around Guile’s built-in support for
interacting with the current environment, *Note Runtime Environment::.

 -- Scheme Procedure: get-environment-variable name
     Returns a string containing the value of the environment variable
     given by the string ‘name’, or ‘#f’ if the named environment
     variable is not found.  This is equivalent to ‘(getenv name)’.

 -- Scheme Procedure: get-environment-variables
     Returns the names and values of all the environment variables as an
     association list in which both the keys and the values are strings.

7.5.42 SRFI-105 Curly-infix expressions.
----------------------------------------

Guile’s built-in reader includes support for SRFI-105 curly-infix
expressions.  See the specification of SRFI-105
(http://srfi.schemers.org/srfi-105/srfi-105.html).  Some examples:

     {n <= 5}                ⇒  (<= n 5)
     {a + b + c}             ⇒  (+ a b c)
     {a * {b + c}}           ⇒  (* a (+ b c))
     {(- a) / b}             ⇒  (/ (- a) b)
     {-(a) / b}              ⇒  (/ (- a) b) as well
     {(f a b) + (g h)}       ⇒  (+ (f a b) (g h))
     {f(a b) + g(h)}         ⇒  (+ (f a b) (g h)) as well
     {f[a b] + g(h)}         ⇒  (+ ($bracket-apply$ f a b) (g h))
     '{a + f(b) + x}         ⇒  '(+ a (f b) x)
     {length(x) >= 6}        ⇒  (>= (length x) 6)
     {n-1 + n-2}             ⇒  (+ n-1 n-2)
     {n * factorial{n - 1}}  ⇒  (* n (factorial (- n 1)))
     {{a > 0} and {b >= 1}}  ⇒  (and (> a 0) (>= b 1))
     {f{n - 1}(x)}           ⇒  ((f (- n 1)) x)
     {a . z}                 ⇒  ($nfx$ a . z)
     {a + b - c}             ⇒  ($nfx$ a + b - c)

   To enable curly-infix expressions within a file, place the reader
directive ‘#!curly-infix’ before the first use of curly-infix notation.
To globally enable curly-infix expressions in Guile’s reader, set the
‘curly-infix’ read option.

   Guile also implements the following non-standard extension to
SRFI-105: if ‘curly-infix’ is enabled and there is no other meaning
assigned to square brackets (i.e.  the ‘square-brackets’ read option is
turned off), then lists within square brackets are read as normal lists
but with the special symbol ‘$bracket-list$’ added to the front.  To
enable this combination of read options within a file, use the reader
directive ‘#!curly-infix-and-bracket-lists’.  For example:

     [a b]    ⇒  ($bracket-list$ a b)
     [a . b]  ⇒  ($bracket-list$ a . b)

   For more information on reader options, *Note Scheme Read::.

7.5.43 SRFI-111 Boxes.
----------------------

SRFI-111 (http://srfi.schemers.org/srfi-111/srfi-111.html) provides
boxes: objects with a single mutable cell.

 -- Scheme Procedure: box value
     Return a newly allocated box whose contents is initialized to
     VALUE.

 -- Scheme Procedure: box? obj
     Return true if OBJ is a box, otherwise return false.

 -- Scheme Procedure: unbox box
     Return the current contents of BOX.

 -- Scheme Procedure: set-box! box value
     Set the contents of BOX to VALUE.

7.6 R6RS Support
================

*Note R6RS Libraries::, for more information on how to define R6RS
libraries, and their integration with Guile modules.

7.6.1 Incompatibilities with the R6RS
-------------------------------------

There are some incompatibilities between Guile and the R6RS. Some of
them are intentional, some of them are bugs, and some are simply
unimplemented features.  Please let the Guile developers know if you
find one that is not on this list.

   • The R6RS specifies many situations in which a conforming
     implementation must signal a specific error.  Guile doesn’t really
     care about that too much—if a correct R6RS program would not hit
     that error, we don’t bother checking for it.

   • Multiple ‘library’ forms in one file are not yet supported.  This
     is because the expansion of ‘library’ sets the current module, but
     does not restore it.  This is a bug.

   • R6RS unicode escapes within strings are disabled by default,
     because they conflict with Guile’s already-existing escapes.  The
     same is the case for R6RS treatment of escaped newlines in strings.

     R6RS behavior can be turned on via a reader option.  *Note String
     Syntax::, for more information.

   • A ‘set!’ to a variable transformer may only expand to an
     expression, not a definition—even if the original ‘set!’ expression
     was in definition context.

   • Instead of using the algorithm detailed in chapter 10 of the R6RS,
     expansion of toplevel forms happens sequentially.

     For example, while the expansion of the following set of toplevel
     definitions does the correct thing:

          (begin
           (define even?
             (lambda (x)
               (or (= x 0) (odd? (- x 1)))))
           (define-syntax odd?
             (syntax-rules ()
               ((odd? x) (not (even? x)))))
           (even? 10))
          ⇒ #t

     The same definitions outside of the ‘begin’ wrapper do not:

          (define even?
            (lambda (x)
              (or (= x 0) (odd? (- x 1)))))
          (define-syntax odd?
            (syntax-rules ()
              ((odd? x) (not (even? x)))))
          (even? 10)
          <unnamed port>:4:18: In procedure even?:
          <unnamed port>:4:18: Wrong type to apply: #<syntax-transformer odd?>

     This is because when expanding the right-hand-side of ‘even?’, the
     reference to ‘odd?’ is not yet marked as a syntax transformer, so
     it is assumed to be a function.

     This bug will only affect top-level programs, not code in ‘library’
     forms.  Fixing it for toplevel forms seems doable, but tricky to
     implement in a backward-compatible way.  Suggestions and/or patches
     would be appreciated.

   • The ‘(rnrs io ports)’ module is incomplete.  Work is ongoing to fix
     this.

   • Guile does not prevent use of textual I/O procedures on binary
     ports.  More generally, it does not make a sharp distinction
     between binary and textual ports (*note binary-port?: R6RS Port
     Manipulation.).

   • Guile’s implementation of ‘equal?’ may fail to terminate when
     applied to arguments containing cycles.

7.6.2 R6RS Standard Libraries
-----------------------------

In contrast with earlier versions of the Revised Report, the R6RS
organizes the procedures and syntactic forms required of conforming
implementations into a set of “standard libraries” which can be imported
as necessary by user programs and libraries.  Here we briefly list the
libraries that have been implemented for Guile.

   We do not attempt to document these libraries fully here, as most of
their functionality is already available in Guile itself.  The
expectation is that most Guile users will use the well-known and
well-documented Guile modules.  These R6RS libraries are mostly useful
to users who want to port their code to other R6RS systems.

   The documentation in the following sections reproduces some of the
content of the library section of the Report, but is mostly intended to
provide supplementary information about Guile’s implementation of the
R6RS standard libraries.  For complete documentation, design rationales
and further examples, we advise you to consult the “Standard Libraries”
section of the Report (*note R6RS Standard Libraries: (r6rs)Standard
Libraries.).

7.6.2.1 Library Usage
.....................

Guile implements the R6RS ‘library’ form as a transformation to a native
Guile module definition.  As a consequence of this, all of the libraries
described in the following subsections, in addition to being available
for use by R6RS libraries and top-level programs, can also be imported
as if they were normal Guile modules—via a ‘use-modules’ form, say.  For
example, the R6RS “composite” library can be imported by:

       (import (rnrs (6)))

       (use-modules ((rnrs) :version (6)))

   For more information on Guile’s library implementation, see (*note
R6RS Libraries::).

7.6.2.2 rnrs base
.................

The ‘(rnrs base (6))’ library exports the procedures and syntactic forms
described in the main section of the Report (*note R6RS Base library:
(r6rs)Base library.).  They are grouped below by the existing manual
sections to which they correspond.

 -- Scheme Procedure: boolean? obj
 -- Scheme Procedure: not x
     *Note Booleans::, for documentation.

 -- Scheme Procedure: symbol? obj
 -- Scheme Procedure: symbol->string sym
 -- Scheme Procedure: string->symbol str
     *Note Symbol Primitives::, for documentation.

 -- Scheme Procedure: char? obj
 -- Scheme Procedure: char=?
 -- Scheme Procedure: char<?
 -- Scheme Procedure: char>?
 -- Scheme Procedure: char<=?
 -- Scheme Procedure: char>=?
 -- Scheme Procedure: integer->char n
 -- Scheme Procedure: char->integer chr
     *Note Characters::, for documentation.

 -- Scheme Procedure: list? x
 -- Scheme Procedure: null? x
     *Note List Predicates::, for documentation.

 -- Scheme Procedure: pair? x
 -- Scheme Procedure: cons x y
 -- Scheme Procedure: car pair
 -- Scheme Procedure: cdr pair
 -- Scheme Procedure: caar pair
 -- Scheme Procedure: cadr pair
 -- Scheme Procedure: cdar pair
 -- Scheme Procedure: cddr pair
 -- Scheme Procedure: caaar pair
 -- Scheme Procedure: caadr pair
 -- Scheme Procedure: cadar pair
 -- Scheme Procedure: cdaar pair
 -- Scheme Procedure: caddr pair
 -- Scheme Procedure: cdadr pair
 -- Scheme Procedure: cddar pair
 -- Scheme Procedure: cdddr pair
 -- Scheme Procedure: caaaar pair
 -- Scheme Procedure: caaadr pair
 -- Scheme Procedure: caadar pair
 -- Scheme Procedure: cadaar pair
 -- Scheme Procedure: cdaaar pair
 -- Scheme Procedure: cddaar pair
 -- Scheme Procedure: cdadar pair
 -- Scheme Procedure: cdaadr pair
 -- Scheme Procedure: cadadr pair
 -- Scheme Procedure: caaddr pair
 -- Scheme Procedure: caddar pair
 -- Scheme Procedure: cadddr pair
 -- Scheme Procedure: cdaddr pair
 -- Scheme Procedure: cddadr pair
 -- Scheme Procedure: cdddar pair
 -- Scheme Procedure: cddddr pair
     *Note Pairs::, for documentation.

 -- Scheme Procedure: number? obj
     *Note Numerical Tower::, for documentation.

 -- Scheme Procedure: string? obj
     *Note String Predicates::, for documentation.

 -- Scheme Procedure: procedure? obj
     *Note Procedure Properties::, for documentation.

 -- Scheme Syntax: define name value
 -- Scheme Syntax: set! variable-name value
     *Note Definition::, for documentation.

 -- Scheme Syntax: define-syntax keyword expression
 -- Scheme Syntax: let-syntax ((keyword transformer) …) exp1 exp2 …
 -- Scheme Syntax: letrec-syntax ((keyword transformer) …) exp1 exp2 …
     *Note Defining Macros::, for documentation.

 -- Scheme Syntax: identifier-syntax exp
     *Note Identifier Macros::, for documentation.

 -- Scheme Syntax: syntax-rules literals (pattern template) ...
     *Note Syntax Rules::, for documentation.

 -- Scheme Syntax: lambda formals body
     *Note Lambda::, for documentation.

 -- Scheme Syntax: let bindings body
 -- Scheme Syntax: let* bindings body
 -- Scheme Syntax: letrec bindings body
 -- Scheme Syntax: letrec* bindings body
     *Note Local Bindings::, for documentation.

 -- Scheme Syntax: let-values bindings body
 -- Scheme Syntax: let*-values bindings body
     *Note SRFI-11::, for documentation.

 -- Scheme Syntax: begin expr1 expr2 ...
     *Note begin::, for documentation.

 -- Scheme Syntax: quote expr
 -- Scheme Syntax: quasiquote expr
 -- Scheme Syntax: unquote expr
 -- Scheme Syntax: unquote-splicing expr
     *Note Expression Syntax::, for documentation.

 -- Scheme Syntax: if test consequence [alternate]
 -- Scheme Syntax: cond clause1 clause2 ...
 -- Scheme Syntax: case key clause1 clause2 ...
     *Note Conditionals::, for documentation.

 -- Scheme Syntax: and expr ...
 -- Scheme Syntax: or expr ...
     *Note and or::, for documentation.

 -- Scheme Procedure: eq? x y
 -- Scheme Procedure: eqv? x y
 -- Scheme Procedure: equal? x y
 -- Scheme Procedure: symbol=? symbol1 symbol2 ...
     *Note Equality::, for documentation.

     ‘symbol=?’ is identical to ‘eq?’.

 -- Scheme Procedure: complex? z
     *Note Complex Numbers::, for documentation.

 -- Scheme Procedure: real-part z
 -- Scheme Procedure: imag-part z
 -- Scheme Procedure: make-rectangular real_part imaginary_part
 -- Scheme Procedure: make-polar x y
 -- Scheme Procedure: magnitude z
 -- Scheme Procedure: angle z
     *Note Complex::, for documentation.

 -- Scheme Procedure: sqrt z
 -- Scheme Procedure: exp z
 -- Scheme Procedure: expt z1 z2
 -- Scheme Procedure: log z
 -- Scheme Procedure: sin z
 -- Scheme Procedure: cos z
 -- Scheme Procedure: tan z
 -- Scheme Procedure: asin z
 -- Scheme Procedure: acos z
 -- Scheme Procedure: atan z
     *Note Scientific::, for documentation.

 -- Scheme Procedure: real? x
 -- Scheme Procedure: rational? x
 -- Scheme Procedure: numerator x
 -- Scheme Procedure: denominator x
 -- Scheme Procedure: rationalize x eps
     *Note Reals and Rationals::, for documentation.

 -- Scheme Procedure: exact? x
 -- Scheme Procedure: inexact? x
 -- Scheme Procedure: exact z
 -- Scheme Procedure: inexact z
     *Note Exactness::, for documentation.  The ‘exact’ and ‘inexact’
     procedures are identical to the ‘inexact->exact’ and
     ‘exact->inexact’ procedures provided by Guile’s code library.

 -- Scheme Procedure: integer? x
     *Note Integers::, for documentation.

 -- Scheme Procedure: odd? n
 -- Scheme Procedure: even? n
 -- Scheme Procedure: gcd x ...
 -- Scheme Procedure: lcm x ...
 -- Scheme Procedure: exact-integer-sqrt k
     *Note Integer Operations::, for documentation.

 -- Scheme Procedure: =
 -- Scheme Procedure: <
 -- Scheme Procedure: >
 -- Scheme Procedure: <=
 -- Scheme Procedure: >=
 -- Scheme Procedure: zero? x
 -- Scheme Procedure: positive? x
 -- Scheme Procedure: negative? x
     *Note Comparison::, for documentation.

 -- Scheme Procedure: for-each f lst1 lst2 ...
     *Note SRFI-1 Fold and Map::, for documentation.

 -- Scheme Procedure: list elem …
     *Note List Constructors::, for documentation.

 -- Scheme Procedure: length lst
 -- Scheme Procedure: list-ref lst k
 -- Scheme Procedure: list-tail lst k
     *Note List Selection::, for documentation.

 -- Scheme Procedure: append lst … obj
 -- Scheme Procedure: append
 -- Scheme Procedure: reverse lst
     *Note Append/Reverse::, for documentation.

 -- Scheme Procedure: number->string n [radix]
 -- Scheme Procedure: string->number str [radix]
     *Note Conversion::, for documentation.

 -- Scheme Procedure: string char ...
 -- Scheme Procedure: make-string k [chr]
 -- Scheme Procedure: list->string lst
     *Note String Constructors::, for documentation.

 -- Scheme Procedure: string->list str [start [end]]
     *Note List/String Conversion::, for documentation.

 -- Scheme Procedure: string-length str
 -- Scheme Procedure: string-ref str k
 -- Scheme Procedure: string-copy str [start [end]]
 -- Scheme Procedure: substring str start [end]
     *Note String Selection::, for documentation.

 -- Scheme Procedure: string=? s1 s2 s3 …
 -- Scheme Procedure: string<? s1 s2 s3 …
 -- Scheme Procedure: string>? s1 s2 s3 …
 -- Scheme Procedure: string<=? s1 s2 s3 …
 -- Scheme Procedure: string>=? s1 s2 s3 …
     *Note String Comparison::, for documentation.

 -- Scheme Procedure: string-append arg …
     *Note Reversing and Appending Strings::, for documentation.

 -- Scheme Procedure: string-for-each proc s [start [end]]
     *Note Mapping Folding and Unfolding::, for documentation.

 -- Scheme Procedure: + z1 ...
 -- Scheme Procedure: - z1 z2 ...
 -- Scheme Procedure: * z1 ...
 -- Scheme Procedure: / z1 z2 ...
 -- Scheme Procedure: max x1 x2 ...
 -- Scheme Procedure: min x1 x2 ...
 -- Scheme Procedure: abs x
 -- Scheme Procedure: truncate x
 -- Scheme Procedure: floor x
 -- Scheme Procedure: ceiling x
 -- Scheme Procedure: round x
     *Note Arithmetic::, for documentation.

 -- Scheme Procedure: div x y
 -- Scheme Procedure: mod x y
 -- Scheme Procedure: div-and-mod x y
     These procedures accept two real numbers X and Y, where the divisor
     Y must be non-zero.  ‘div’ returns the integer Q and ‘mod’ returns
     the real number R such that X = Q*Y + R and 0 <= R < abs(Y).
     ‘div-and-mod’ returns both Q and R, and is more efficient than
     computing each separately.  Note that when Y > 0, ‘div’ returns
     floor(X/Y), otherwise it returns ceiling(X/Y).

          (div 123 10) ⇒ 12
          (mod 123 10) ⇒ 3
          (div-and-mod 123 10) ⇒ 12 and 3
          (div-and-mod 123 -10) ⇒ -12 and 3
          (div-and-mod -123 10) ⇒ -13 and 7
          (div-and-mod -123 -10) ⇒ 13 and 7
          (div-and-mod -123.2 -63.5) ⇒ 2.0 and 3.8
          (div-and-mod 16/3 -10/7) ⇒ -3 and 22/21

 -- Scheme Procedure: div0 x y
 -- Scheme Procedure: mod0 x y
 -- Scheme Procedure: div0-and-mod0 x y
     These procedures accept two real numbers X and Y, where the divisor
     Y must be non-zero.  ‘div0’ returns the integer Q and ‘mod0’
     returns the real number R such that X = Q*Y + R and -abs(Y/2) <= R
     < abs(Y/2).  ‘div0-and-mod0’ returns both Q and R, and is more
     efficient than computing each separately.

     Note that ‘div0’ returns X/Y rounded to the nearest integer.  When
     X/Y lies exactly half-way between two integers, the tie is broken
     according to the sign of Y.  If Y > 0, ties are rounded toward
     positive infinity, otherwise they are rounded toward negative
     infinity.  This is a consequence of the requirement that -abs(Y/2)
     <= R < abs(Y/2).

          (div0 123 10) ⇒ 12
          (mod0 123 10) ⇒ 3
          (div0-and-mod0 123 10) ⇒ 12 and 3
          (div0-and-mod0 123 -10) ⇒ -12 and 3
          (div0-and-mod0 -123 10) ⇒ -12 and -3
          (div0-and-mod0 -123 -10) ⇒ 12 and -3
          (div0-and-mod0 -123.2 -63.5) ⇒ 2.0 and 3.8
          (div0-and-mod0 16/3 -10/7) ⇒ -4 and -8/21

 -- Scheme Procedure: real-valued? obj
 -- Scheme Procedure: rational-valued? obj
 -- Scheme Procedure: integer-valued? obj
     These procedures return ‘#t’ if and only if their arguments can,
     respectively, be coerced to a real, rational, or integer value
     without a loss of numerical precision.

     ‘real-valued?’ will return ‘#t’ for complex numbers whose imaginary
     parts are zero.

 -- Scheme Procedure: nan? x
 -- Scheme Procedure: infinite? x
 -- Scheme Procedure: finite? x
     ‘nan?’ returns ‘#t’ if X is a NaN value, ‘#f’ otherwise.
     ‘infinite?’ returns ‘#t’ if X is an infinite value, ‘#f’ otherwise.
     ‘finite?’ returns ‘#t’ if X is neither infinite nor a NaN value,
     otherwise it returns ‘#f’.  Every real number satisfies exactly one
     of these predicates.  An exception is raised if X is not real.

 -- Scheme Syntax: assert expr
     Raises an ‘&assertion’ condition if EXPR evaluates to ‘#f’;
     otherwise evaluates to the value of EXPR.

 -- Scheme Procedure: error who message irritant1 ...
 -- Scheme Procedure: assertion-violation who message irritant1 ...
     These procedures raise compound conditions based on their
     arguments: If WHO is not ‘#f’, the condition will include a ‘&who’
     condition whose ‘who’ field is set to WHO; a ‘&message’ condition
     will be included with a ‘message’ field equal to MESSAGE; an
     ‘&irritants’ condition will be included with its ‘irritants’ list
     given by ‘irritant1 ...’.

     ‘error’ produces a compound condition with the simple conditions
     described above, as well as an ‘&error’ condition;
     ‘assertion-violation’ produces one that includes an ‘&assertion’
     condition.

 -- Scheme Procedure: vector-map proc v
 -- Scheme Procedure: vector-for-each proc v
     These procedures implement the ‘map’ and ‘for-each’ contracts over
     vectors.

 -- Scheme Procedure: vector arg …
 -- Scheme Procedure: vector? obj
 -- Scheme Procedure: make-vector len
 -- Scheme Procedure: make-vector len fill
 -- Scheme Procedure: list->vector l
 -- Scheme Procedure: vector->list v
     *Note Vector Creation::, for documentation.

 -- Scheme Procedure: vector-length vector
 -- Scheme Procedure: vector-ref vector k
 -- Scheme Procedure: vector-set! vector k obj
 -- Scheme Procedure: vector-fill! v fill
     *Note Vector Accessors::, for documentation.

 -- Scheme Procedure: call-with-current-continuation proc
 -- Scheme Procedure: call/cc proc
     *Note Continuations::, for documentation.

 -- Scheme Procedure: values arg …
 -- Scheme Procedure: call-with-values producer consumer
     *Note Multiple Values::, for documentation.

 -- Scheme Procedure: dynamic-wind in_guard thunk out_guard
     *Note Dynamic Wind::, for documentation.

 -- Scheme Procedure: apply proc arg … arglst
     *Note Fly Evaluation::, for documentation.

7.6.2.3 rnrs unicode
....................

The ‘(rnrs unicode (6))’ library provides procedures for manipulating
Unicode characters and strings.

 -- Scheme Procedure: char-upcase char
 -- Scheme Procedure: char-downcase char
 -- Scheme Procedure: char-titlecase char
 -- Scheme Procedure: char-foldcase char
     These procedures translate their arguments from one Unicode
     character set to another.  ‘char-upcase’, ‘char-downcase’, and
     ‘char-titlecase’ are identical to their counterparts in the Guile
     core library; *Note Characters::, for documentation.

     ‘char-foldcase’ returns the result of applying ‘char-upcase’ to its
     argument, followed by ‘char-downcase’—except in the case of the
     Turkic characters ‘U+0130’ and ‘U+0131’, for which the procedure
     acts as the identity function.

 -- Scheme Procedure: char-ci=? char1 char2 char3 ...
 -- Scheme Procedure: char-ci<? char1 char2 char3 ...
 -- Scheme Procedure: char-ci>? char1 char2 char3 ...
 -- Scheme Procedure: char-ci<=? char1 char2 char3 ...
 -- Scheme Procedure: char-ci>=? char1 char2 char3 ...
     These procedures facilitate case-insensitive comparison of Unicode
     characters.  They are identical to the procedures provided by
     Guile’s core library.  *Note Characters::, for documentation.

 -- Scheme Procedure: char-alphabetic? char
 -- Scheme Procedure: char-numeric? char
 -- Scheme Procedure: char-whitespace? char
 -- Scheme Procedure: char-upper-case? char
 -- Scheme Procedure: char-lower-case? char
 -- Scheme Procedure: char-title-case? char
     These procedures implement various Unicode character set
     predicates.  They are identical to the procedures provided by
     Guile’s core library.  *Note Characters::, for documentation.

 -- Scheme Procedure: char-general-category char
     *Note Characters::, for documentation.

 -- Scheme Procedure: string-upcase string
 -- Scheme Procedure: string-downcase string
 -- Scheme Procedure: string-titlecase string
 -- Scheme Procedure: string-foldcase string
     These procedures perform Unicode case folding operations on their
     input.  *Note Alphabetic Case Mapping::, for documentation.

 -- Scheme Procedure: string-ci=? string1 string2 string3 ...
 -- Scheme Procedure: string-ci<? string1 string2 string3 ...
 -- Scheme Procedure: string-ci>? string1 string2 string3 ...
 -- Scheme Procedure: string-ci<=? string1 string2 string3 ...
 -- Scheme Procedure: string-ci>=? string1 string2 string3 ...
     These procedures perform case-insensitive comparison on their
     input.  *Note String Comparison::, for documentation.

 -- Scheme Procedure: string-normalize-nfd string
 -- Scheme Procedure: string-normalize-nfkd string
 -- Scheme Procedure: string-normalize-nfc string
 -- Scheme Procedure: string-normalize-nfkc string
     These procedures perform Unicode string normalization operations on
     their input.  *Note String Comparison::, for documentation.

7.6.2.4 rnrs bytevectors
........................

The ‘(rnrs bytevectors (6))’ library provides procedures for working
with blocks of binary data.  This functionality is documented in its own
section of the manual; *Note Bytevectors::.

7.6.2.5 rnrs lists
..................

The ‘(rnrs lists (6))’ library provides procedures additional procedures
for working with lists.

 -- Scheme Procedure: find proc list
     This procedure is identical to the one defined in Guile’s SRFI-1
     implementation.  *Note SRFI-1 Searching::, for documentation.

 -- Scheme Procedure: for-all proc list1 list2 ...
 -- Scheme Procedure: exists proc list1 list2 ...

     The ‘for-all’ procedure is identical to the ‘every’ procedure
     defined by SRFI-1; the ‘exists’ procedure is identical to SRFI-1’s
     ‘any’.  *Note SRFI-1 Searching::, for documentation.

 -- Scheme Procedure: filter proc list
 -- Scheme Procedure: partition proc list
     These procedures are identical to the ones provided by SRFI-1.
     *Note List Modification::, for a description of ‘filter’; *Note
     SRFI-1 Filtering and Partitioning::, for ‘partition’.

 -- Scheme Procedure: fold-left combine nil list1 list2 …
 -- Scheme Procedure: fold-right combine nil list1 list2 …
     These procedures are identical to the ‘fold’ and ‘fold-right’
     procedures provided by SRFI-1.  *Note SRFI-1 Fold and Map::, for
     documentation.

 -- Scheme Procedure: remp proc list
 -- Scheme Procedure: remove obj list
 -- Scheme Procedure: remv obj list
 -- Scheme Procedure: remq obj list
     ‘remove’, ‘remv’, and ‘remq’ are identical to the ‘delete’, ‘delv’,
     and ‘delq’ procedures provided by Guile’s core library, (*note List
     Modification::).  ‘remp’ is identical to the alternate ‘remove’
     procedure provided by SRFI-1; *Note SRFI-1 Deleting::.

 -- Scheme Procedure: memp proc list
 -- Scheme Procedure: member obj list
 -- Scheme Procedure: memv obj list
 -- Scheme Procedure: memq obj list
     ‘member’, ‘memv’, and ‘memq’ are identical to the procedures
     provided by Guile’s core library; *Note List Searching::, for their
     documentation.  ‘memp’ uses the specified predicate function ‘proc’
     to test elements of the list LIST—it behaves similarly to ‘find’,
     except that it returns the first sublist of LIST whose ‘car’
     satisfies PROC.

 -- Scheme Procedure: assp proc alist
 -- Scheme Procedure: assoc obj alist
 -- Scheme Procedure: assv obj alist
 -- Scheme Procedure: assq obj alist
     ‘assoc’, ‘assv’, and ‘assq’ are identical to the procedures
     provided by Guile’s core library; *Note Alist Key Equality::, for
     their documentation.  ‘assp’ uses the specified predicate function
     ‘proc’ to test keys in the association list ALIST.

 -- Scheme Procedure: cons* obj1 ... obj
 -- Scheme Procedure: cons* obj
     This procedure is identical to the one exported by Guile’s core
     library.  *Note List Constructors::, for documentation.

7.6.2.6 rnrs sorting
....................

The ‘(rnrs sorting (6))’ library provides procedures for sorting lists
and vectors.

 -- Scheme Procedure: list-sort proc list
 -- Scheme Procedure: vector-sort proc vector
     These procedures return their input sorted in ascending order,
     without modifying the original data.  PROC must be a procedure that
     takes two elements from the input list or vector as arguments, and
     returns a true value if the first is “less” than the second, ‘#f’
     otherwise.  ‘list-sort’ returns a list; ‘vector-sort’ returns a
     vector.

     Both ‘list-sort’ and ‘vector-sort’ are implemented in terms of the
     ‘stable-sort’ procedure from Guile’s core library.  *Note
     Sorting::, for a discussion of the behavior of that procedure.

 -- Scheme Procedure: vector-sort! proc vector
     Performs a destructive, “in-place” sort of VECTOR, using PROC as
     described above to determine an ascending ordering of elements.
     ‘vector-sort!’ returns an unspecified value.

     This procedure is implemented in terms of the ‘sort!’ procedure
     from Guile’s core library.  *Note Sorting::, for more information.

7.6.2.7 rnrs control
....................

The ‘(rnrs control (6))’ library provides syntactic forms useful for
constructing conditional expressions and controlling the flow of
execution.

 -- Scheme Syntax: when test expression1 expression2 ...
 -- Scheme Syntax: unless test expression1 expression2 ...
     The ‘when’ form is evaluated by evaluating the specified TEST
     expression; if the result is a true value, the EXPRESSIONs that
     follow it are evaluated in order, and the value of the final
     EXPRESSION becomes the value of the entire ‘when’ expression.

     The ‘unless’ form behaves similarly, with the exception that the
     specified EXPRESSIONs are only evaluated if the value of TEST is
     false.

 -- Scheme Syntax: do ((variable init step) ...) (test expression ...)
          command ...
     This form is identical to the one provided by Guile’s core library.
     *Note while do::, for documentation.

 -- Scheme Syntax: case-lambda clause ...
     This form is identical to the one provided by Guile’s core library.
     *Note Case-lambda::, for documentation.

7.6.2.8 R6RS Records
....................

The manual sections below describe Guile’s implementation of R6RS
records, which provide support for user-defined data types.  The R6RS
records API provides a superset of the features provided by Guile’s
“native” records, as well as those of the SRFI-9 records API; *Note
Records::, and *note SRFI-9 Records::, for a description of those
interfaces.

   As with SRFI-9 and Guile’s native records, R6RS records are
constructed using a record-type descriptor that specifies attributes
like the record’s name, its fields, and the mutability of those fields.

   R6RS records extend this framework to support single inheritance via
the specification of a “parent” type for a record type at definition
time.  Accessors and mutator procedures for the fields of a parent type
may be applied to records of a subtype of this parent.  A record type
may be "sealed", in which case it cannot be used as the parent of
another record type.

   The inheritance mechanism for record types also informs the process
of initializing the fields of a record and its parents.  Constructor
procedures that generate new instances of a record type are obtained
from a record constructor descriptor, which encapsulates the record-type
descriptor of the record to be constructed along with a "protocol"
procedure that defines how constructors for record subtypes delegate to
the constructors of their parent types.

   A protocol is a procedure used by the record system at construction
time to bind arguments to the fields of the record being constructed.
The protocol procedure is passed a procedure N that accepts the
arguments required to construct the record’s parent type; this
procedure, when invoked, will return a procedure P that accepts the
arguments required to construct a new instance of the record type itself
and returns a new instance of the record type.

   The protocol should in turn return a procedure that uses N and P to
initialize the fields of the record type and its parent type(s).  This
procedure will be the constructor returned by

   As a trivial example, consider the hypothetical record type ‘pixel’,
which encapsulates an x-y location on a screen, and ‘voxel’, which has
‘pixel’ as its parent type and stores an additional coordinate.  The
following protocol produces a constructor procedure that accepts all
three coordinates, uses the first two to initialize the fields of
‘pixel’, and binds the third to the single field of ‘voxel’.

       (lambda (n)
         (lambda (x y z)
           (let ((p (n x y)))
             (p z))))

   It may be helpful to think of protocols as “constructor factories”
that produce chains of delegating constructors glued together by the
helper procedure N.

   An R6RS record type may be declared to be "nongenerative" via the use
of a unique generated or user-supplied symbol—or "uid"—such that
subsequent record type declarations with the same uid and attributes
will return the previously-declared record-type descriptor.

   R6RS record types may also be declared to be "opaque", in which case
the various predicates and introspection procedures defined in ‘(rnrs
records introspection)’ will behave as if records of this type are not
records at all.

   Note that while the R6RS records API shares much of its namespace
with both the SRFI-9 and native Guile records APIs, it is not currently
compatible with either.

7.6.2.9 rnrs records syntactic
..............................

The ‘(rnrs records syntactic (6))’ library exports the syntactic API for
working with R6RS records.

 -- Scheme Syntax: define-record-type name-spec record-clause …
     Defines a new record type, introducing bindings for a record-type
     descriptor, a record constructor descriptor, a constructor
     procedure, a record predicate, and accessor and mutator procedures
     for the new record type’s fields.

     NAME-SPEC must either be an identifier or must take the form
     ‘(record-name constructor-name predicate-name)’, where RECORD-NAME,
     CONSTRUCTOR-NAME, and PREDICATE-NAME are all identifiers and
     specify the names to which, respectively, the record-type
     descriptor, constructor, and predicate procedures will be bound.
     If NAME-SPEC is only an identifier, it specifies the name to which
     the generated record-type descriptor will be bound.

     Each RECORD-CLAUSE must be one of the following:

        • ‘(fields field-spec*)’, where each FIELD-SPEC specifies a
          field of the new record type and takes one of the following
          forms:
             • ‘(immutable field-name accessor-name)’, which specifies
               an immutable field with the name FIELD-NAME and binds an
               accessor procedure for it to the name given by
               ACCESSOR-NAME
             • ‘(mutable field-name accessor-name mutator-name)’, which
               specifies a mutable field with the name FIELD-NAME and
               binds accessor and mutator procedures to ACCESSOR-NAME
               and MUTATOR-NAME, respectively
             • ‘(immutable field-name)’, which specifies an immutable
               field with the name FIELD-NAME; an accessor procedure for
               it will be created and named by appending record name and
               FIELD-NAME with a hyphen separator
             • ‘(mutable field-name’), which specifies a mutable field
               with the name FIELD-NAME; an accessor procedure for it
               will be created and named as described above; a mutator
               procedure will also be created and named by appending
               ‘-set!’ to the accessor name
             • ‘field-name’, which specifies an immutable field with the
               name FIELD-NAME; an access procedure for it will be
               created and named as described above
        • ‘(parent parent-name)’, where PARENT-NAME is a symbol giving
          the name of the record type to be used as the parent of the
          new record type
        • ‘(protocol expression)’, where EXPRESSION evaluates to a
          protocol procedure which behaves as described above, and is
          used to create a record constructor descriptor for the new
          record type
        • ‘(sealed sealed?)’, where SEALED? is a boolean value that
          specifies whether or not the new record type is sealed
        • ‘(opaque opaque?)’, where OPAQUE? is a boolean value that
          specifies whether or not the new record type is opaque
        • ‘(nongenerative [uid])’, which specifies that the record type
          is nongenerative via the optional uid UID.  If UID is not
          specified, a unique uid will be generated at expansion time
        • ‘(parent-rtd parent-rtd parent-cd)’, a more explicit form of
          the ‘parent’ form above; PARENT-RTD and PARENT-CD should
          evaluate to a record-type descriptor and a record constructor
          descriptor, respectively

 -- Scheme Syntax: record-type-descriptor record-name
     Evaluates to the record-type descriptor associated with the type
     specified by RECORD-NAME.

 -- Scheme Syntax: record-constructor-descriptor record-name
     Evaluates to the record-constructor descriptor associated with the
     type specified by RECORD-NAME.

7.6.2.10 rnrs records procedural
................................

The ‘(rnrs records procedural (6))’ library exports the procedural API
for working with R6RS records.

 -- Scheme Procedure: make-record-type-descriptor name parent uid
          sealed? opaque? fields
     Returns a new record-type descriptor with the specified
     characteristics: NAME must be a symbol giving the name of the new
     record type; PARENT must be either ‘#f’ or a non-sealed record-type
     descriptor for the returned record type to extend; UID must be
     either ‘#f’, indicating that the record type is generative, or a
     symbol giving the type’s nongenerative uid; SEALED? and OPAQUE?
     must be boolean values that specify the sealedness and opaqueness
     of the record type; FIELDS must be a vector of zero or more field
     specifiers of the form ‘(mutable name)’ or ‘(immutable name)’,
     where name is a symbol giving a name for the field.

     If UID is not ‘#f’, it must be a symbol

 -- Scheme Procedure: record-type-descriptor? obj
     Returns ‘#t’ if OBJ is a record-type descriptor, ‘#f’ otherwise.

 -- Scheme Procedure: make-record-constructor-descriptor rtd
          parent-constructor-descriptor protocol
     Returns a new record constructor descriptor that can be used to
     produce constructors for the record type specified by the
     record-type descriptor RTD and whose delegation and binding
     behavior are specified by the protocol procedure PROTOCOL.

     PARENT-CONSTRUCTOR-DESCRIPTOR specifies a record constructor
     descriptor for the parent type of RTD, if one exists.  If RTD
     represents a base type, then PARENT-CONSTRUCTOR-DESCRIPTOR must be
     ‘#f’.  If RTD is an extension of another type,
     PARENT-CONSTRUCTOR-DESCRIPTOR may still be ‘#f’, but protocol must
     also be ‘#f’ in this case.

 -- Scheme Procedure: record-constructor rcd
     Returns a record constructor procedure by invoking the protocol
     defined by the record-constructor descriptor RCD.

 -- Scheme Procedure: record-predicate rtd
     Returns the record predicate procedure for the record-type
     descriptor RTD.

 -- Scheme Procedure: record-accessor rtd k
     Returns the record field accessor procedure for the Kth field of
     the record-type descriptor RTD.

 -- Scheme Procedure: record-mutator rtd k
     Returns the record field mutator procedure for the Kth field of the
     record-type descriptor RTD.  An ‘&assertion’ condition will be
     raised if this field is not mutable.

7.6.2.11 rnrs records inspection
................................

The ‘(rnrs records inspection (6))’ library provides procedures useful
for accessing metadata about R6RS records.

 -- Scheme Procedure: record? obj
     Return ‘#t’ if the specified object is a non-opaque R6RS record,
     ‘#f’ otherwise.

 -- Scheme Procedure: record-rtd record
     Returns the record-type descriptor for RECORD.  An ‘&assertion’ is
     raised if RECORD is opaque.

 -- Scheme Procedure: record-type-name rtd
     Returns the name of the record-type descriptor RTD.

 -- Scheme Procedure: record-type-parent rtd
     Returns the parent of the record-type descriptor RTD, or ‘#f’ if it
     has none.

 -- Scheme Procedure: record-type-uid rtd
     Returns the uid of the record-type descriptor RTD, or ‘#f’ if it
     has none.

 -- Scheme Procedure: record-type-generative? rtd
     Returns ‘#t’ if the record-type descriptor RTD is generative, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-sealed? rtd
     Returns ‘#t’ if the record-type descriptor RTD is sealed, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-opaque? rtd
     Returns ‘#t’ if the record-type descriptor RTD is opaque, ‘#f’
     otherwise.

 -- Scheme Procedure: record-type-field-names rtd
     Returns a vector of symbols giving the names of the fields defined
     by the record-type descriptor RTD (and not any of its sub- or
     supertypes).

 -- Scheme Procedure: record-field-mutable? rtd k
     Returns ‘#t’ if the field at index K of the record-type descriptor
     RTD (and not any of its sub- or supertypes) is mutable.

7.6.2.12 rnrs exceptions
........................

The ‘(rnrs exceptions (6))’ library provides functionality related to
signaling and handling exceptional situations.  This functionality is
similar to the exception handling systems provided by Guile’s core
library *Note Exceptions::, and by the SRFI-18 and SRFI-34 modules—*Note
SRFI-18 Exceptions::, and *note SRFI-34::, respectively—but there are
some key differences in concepts and behavior.

   A raised exception may be "continuable" or "non-continuable".  When
an exception is raised non-continuably, another exception, with the
condition type ‘&non-continuable’, will be raised when the exception
handler returns locally.  Raising an exception continuably captures the
current continuation and invokes it after a local return from the
exception handler.

   Like SRFI-18 and SRFI-34, R6RS exceptions are implemented on top of
Guile’s native ‘throw’ and ‘catch’ forms, and use custom “throw keys” to
identify their exception types.  As a consequence, Guile’s ‘catch’ form
can handle exceptions thrown by these APIs, but the reverse is not true:
Handlers registered by the ‘with-exception-handler’ procedure described
below will only be called on exceptions thrown by the corresponding
‘raise’ procedure.

 -- Scheme Procedure: with-exception-handler handler thunk
     Installs HANDLER, which must be a procedure taking one argument, as
     the current exception handler during the invocation of THUNK, a
     procedure taking zero arguments.  The handler in place at the time
     ‘with-exception-handler’ is called is made current again once
     either THUNK returns or HANDLER is invoked after an exception is
     thrown from within THUNK.

     This procedure is similar to the ‘with-throw-handler’ procedure
     provided by Guile’s code library; (*note Throw Handlers::).

 -- Scheme Syntax: guard (variable clause1 clause2 ...) body
     Evaluates the expression given by BODY, first creating an ad hoc
     exception handler that binds a raised exception to VARIABLE and
     then evaluates the specified CLAUSEs as if they were part of a
     ‘cond’ expression, with the value of the first matching clause
     becoming the value of the ‘guard’ expression (*note
     Conditionals::).  If none of the clause’s test expressions
     evaluates to ‘#t’, the exception is re-raised, with the exception
     handler that was current before the evaluation of the ‘guard’ form.

     For example, the expression

          (guard (ex ((eq? ex 'foo) 'bar) ((eq? ex 'bar) 'baz))
            (raise 'bar))

     evaluates to ‘baz’.

 -- Scheme Procedure: raise obj
     Raises a non-continuable exception by invoking the
     currently-installed exception handler on OBJ.  If the handler
     returns, a ‘&non-continuable’ exception will be raised in the
     dynamic context in which the handler was installed.

 -- Scheme Procedure: raise-continuable obj
     Raises a continuable exception by invoking currently-installed
     exception handler on OBJ.

7.6.2.13 rnrs conditions
........................

The ‘(rnrs condition (6))’ library provides forms and procedures for
constructing new condition types, as well as a library of pre-defined
condition types that represent a variety of common exceptional
situations.  Conditions are records of a subtype of the ‘&condition’
record type, which is neither sealed nor opaque.  *Note R6RS Records::.

   Conditions may be manipulated singly, as "simple conditions", or when
composed with other conditions to form "compound conditions".  Compound
conditions do not “nest”—constructing a new compound condition out of
existing compound conditions will “flatten” them into their component
simple conditions.  For example, making a new condition out of a
‘&message’ condition and a compound condition that contains an
‘&assertion’ condition and another ‘&message’ condition will produce a
compound condition that contains two ‘&message’ conditions and one
‘&assertion’ condition.

   The record type predicates and field accessors described below can
operate on either simple or compound conditions.  In the latter case,
the predicate returns ‘#t’ if the compound condition contains a
component simple condition of the appropriate type; the field accessors
return the requisite fields from the first component simple condition
found to be of the appropriate type.

   This library is quite similar to the SRFI-35 conditions module (*note
SRFI-35::).  Among other minor differences, the ‘(rnrs conditions)’
library features slightly different semantics around condition field
accessors, and comes with a larger number of pre-defined condition
types.  The two APIs are not currently compatible, however; the
‘condition?’ predicate from one API will return ‘#f’ when applied to a
condition object created in the other.

 -- Condition Type: &condition
 -- Scheme Procedure: condition? obj
     The base record type for conditions.

 -- Scheme Procedure: condition condition1 ...
 -- Scheme Procedure: simple-conditions condition
     The ‘condition’ procedure creates a new compound condition out of
     its condition arguments, flattening any specified compound
     conditions into their component simple conditions as described
     above.

     ‘simple-conditions’ returns a list of the component simple
     conditions of the compound condition ‘condition’, in the order in
     which they were specified at construction time.

 -- Scheme Procedure: condition-predicate rtd
 -- Scheme Procedure: condition-accessor rtd proc
     These procedures return condition predicate and accessor procedures
     for the specified condition record type RTD.

 -- Scheme Syntax: define-condition-type condition-type supertype
          constructor predicate field-spec ...
     Evaluates to a new record type definition for a condition type with
     the name CONDITION-TYPE that has the condition type SUPERTYPE as
     its parent.  A default constructor, which binds its arguments to
     the fields of this type and its parent types, will be bound to the
     identifier CONSTRUCTOR; a condition predicate will be bound to
     PREDICATE.  The fields of the new type, which are immutable, are
     specified by the FIELD-SPECs, each of which must be of the form:
          (field accessor)
     where FIELD gives the name of the field and ACCESSOR gives the name
     for a binding to an accessor procedure created for this field.

 -- Condition Type: &message
 -- Scheme Procedure: make-message-condition message
 -- Scheme Procedure: message-condition? obj
 -- Scheme Procedure: condition-message condition
     A type that includes a message describing the condition that
     occurred.

 -- Condition Type: &warning
 -- Scheme Procedure: make-warning
 -- Scheme Procedure: warning? obj
     A base type for representing non-fatal conditions during execution.

 -- Condition Type: &serious
 -- Scheme Procedure: make-serious-condition
 -- Scheme Procedure: serious-condition? obj
     A base type for conditions representing errors serious enough that
     cannot be ignored.

 -- Condition Type: &error
 -- Scheme Procedure: make-error
 -- Scheme Procedure: error? obj
     A base type for conditions representing errors.

 -- Condition Type: &violation
 -- Scheme Procedure: make-violation
 -- Scheme Procedure: violation?
     A subtype of ‘&serious’ that can be used to represent violations of
     a language or library standard.

 -- Condition Type: &assertion
 -- Scheme Procedure: make-assertion-violation
 -- Scheme Procedure: assertion-violation? obj
     A subtype of ‘&violation’ that indicates an invalid call to a
     procedure.

 -- Condition Type: &irritants
 -- Scheme Procedure: make-irritants-condition irritants
 -- Scheme Procedure: irritants-condition? obj
 -- Scheme Procedure: condition-irritants condition
     A base type used for storing information about the causes of
     another condition in a compound condition.

 -- Condition Type: &who
 -- Scheme Procedure: make-who-condition who
 -- Scheme Procedure: who-condition? obj
 -- Scheme Procedure: condition-who condition
     A base type used for storing the identity, a string or symbol, of
     the entity responsible for another condition in a compound
     condition.

 -- Condition Type: &non-continuable
 -- Scheme Procedure: make-non-continuable-violation
 -- Scheme Procedure: non-continuable-violation? obj
     A subtype of ‘&violation’ used to indicate that an exception
     handler invoked by ‘raise’ has returned locally.

 -- Condition Type: &implementation-restriction
 -- Scheme Procedure: make-implementation-restriction-violation
 -- Scheme Procedure: implementation-restriction-violation? obj
     A subtype of ‘&violation’ used to indicate a violation of an
     implementation restriction.

 -- Condition Type: &lexical
 -- Scheme Procedure: make-lexical-violation
 -- Scheme Procedure: lexical-violation? obj
     A subtype of ‘&violation’ used to indicate a syntax violation at
     the level of the datum syntax.

 -- Condition Type: &syntax
 -- Scheme Procedure: make-syntax-violation form subform
 -- Scheme Procedure: syntax-violation? obj
 -- Scheme Procedure: syntax-violation-form condition
 -- Scheme Procedure: syntax-violation-subform condition
     A subtype of ‘&violation’ that indicates a syntax violation.  The
     FORM and SUBFORM fields, which must be datum values, indicate the
     syntactic form responsible for the condition.

 -- Condition Type: &undefined
 -- Scheme Procedure: make-undefined-violation
 -- Scheme Procedure: undefined-violation? obj
     A subtype of ‘&violation’ that indicates a reference to an unbound
     identifier.

7.6.2.14 I/O Conditions
.......................

These condition types are exported by both the ‘(rnrs io ports (6))’ and
‘(rnrs io simple (6))’ libraries.

 -- Condition Type: &i/o
 -- Scheme Procedure: make-i/o-error
 -- Scheme Procedure: i/o-error? obj
     A condition supertype for more specific I/O errors.

 -- Condition Type: &i/o-read
 -- Scheme Procedure: make-i/o-read-error
 -- Scheme Procedure: i/o-read-error? obj
     A subtype of ‘&i/o’; represents read-related I/O errors.

 -- Condition Type: &i/o-write
 -- Scheme Procedure: make-i/o-write-error
 -- Scheme Procedure: i/o-write-error? obj
     A subtype of ‘&i/o’; represents write-related I/O errors.

 -- Condition Type: &i/o-invalid-position
 -- Scheme Procedure: make-i/o-invalid-position-error position
 -- Scheme Procedure: i/o-invalid-position-error? obj
 -- Scheme Procedure: i/o-error-position condition
     A subtype of ‘&i/o’; represents an error related to an attempt to
     set the file position to an invalid position.

 -- Condition Type: &i/o-filename
 -- Scheme Procedure: make-io-filename-error filename
 -- Scheme Procedure: i/o-filename-error? obj
 -- Scheme Procedure: i/o-error-filename condition
     A subtype of ‘&i/o’; represents an error related to an operation on
     a named file.

 -- Condition Type: &i/o-file-protection
 -- Scheme Procedure: make-i/o-file-protection-error filename
 -- Scheme Procedure: i/o-file-protection-error? obj
     A subtype of ‘&i/o-filename’; represents an error resulting from an
     attempt to access a named file for which the caller had
     insufficient permissions.

 -- Condition Type: &i/o-file-is-read-only
 -- Scheme Procedure: make-i/o-file-is-read-only-error filename
 -- Scheme Procedure: i/o-file-is-read-only-error? obj
     A subtype of ‘&i/o-file-protection’; represents an error related to
     an attempt to write to a read-only file.

 -- Condition Type: &i/o-file-already-exists
 -- Scheme Procedure: make-i/o-file-already-exists-error filename
 -- Scheme Procedure: i/o-file-already-exists-error? obj
     A subtype of ‘&i/o-filename’; represents an error related to an
     operation on an existing file that was assumed not to exist.

 -- Condition Type: &i/o-file-does-not-exist
 -- Scheme Procedure: make-i/o-file-does-not-exist-error
 -- Scheme Procedure: i/o-file-does-not-exist-error? obj
     A subtype of ‘&i/o-filename’; represents an error related to an
     operation on a non-existent file that was assumed to exist.

 -- Condition Type: &i/o-port
 -- Scheme Procedure: make-i/o-port-error port
 -- Scheme Procedure: i/o-port-error? obj
 -- Scheme Procedure: i/o-error-port condition
     A subtype of ‘&i/o’; represents an error related to an operation on
     the port PORT.

7.6.2.15 rnrs io ports
......................

The ‘(rnrs io ports (6))’ library provides various procedures and
syntactic forms for use in writing to and reading from ports.  This
functionality is documented in its own section of the manual; (*note
R6RS I/O Ports::).

7.6.2.16 rnrs io simple
.......................

The ‘(rnrs io simple (6))’ library provides convenience functions for
performing textual I/O on ports.  This library also exports all of the
condition types and associated procedures described in (*note I/O
Conditions::).  In the context of this section, when stating that a
procedure behaves “identically” to the corresponding procedure in
Guile’s core library, this is modulo the behavior wrt.  conditions: such
procedures raise the appropriate R6RS conditions in case of error, but
otherwise behave identically.

     Note: There are still known issues regarding condition-correctness;
     some errors may still be thrown as native Guile exceptions instead
     of the appropriate R6RS conditions.

 -- Scheme Procedure: eof-object
 -- Scheme Procedure: eof-object? obj
     These procedures are identical to the ones provided by the ‘(rnrs
     io ports (6))’ library.  *Note R6RS I/O Ports::, for documentation.

 -- Scheme Procedure: input-port? obj
 -- Scheme Procedure: output-port? obj
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Ports::, for documentation.

 -- Scheme Procedure: call-with-input-file filename proc
 -- Scheme Procedure: call-with-output-file filename proc
 -- Scheme Procedure: open-input-file filename
 -- Scheme Procedure: open-output-file filename
 -- Scheme Procedure: with-input-from-file filename thunk
 -- Scheme Procedure: with-output-to-file filename thunk
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note File Ports::, for documentation.

 -- Scheme Procedure: close-input-port input-port
 -- Scheme Procedure: close-output-port output-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Closing::, for documentation.

 -- Scheme Procedure: peek-char
 -- Scheme Procedure: peek-char textual-input-port
 -- Scheme Procedure: read-char
 -- Scheme Procedure: read-char textual-input-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Reading::, for documentation.

 -- Scheme Procedure: read
 -- Scheme Procedure: read textual-input-port
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Scheme Read::, for documentation.

 -- Scheme Procedure: display obj
 -- Scheme Procedure: display obj textual-output-port
 -- Scheme Procedure: newline
 -- Scheme Procedure: newline textual-output-port
 -- Scheme Procedure: write obj
 -- Scheme Procedure: write obj textual-output-port
 -- Scheme Procedure: write-char char
 -- Scheme Procedure: write-char char textual-output-port
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Writing::, for documentation.

7.6.2.17 rnrs files
...................

The ‘(rnrs files (6))’ library provides the ‘file-exists?’ and
‘delete-file’ procedures, which test for the existence of a file and
allow the deletion of files from the file system, respectively.

   These procedures are identical to the ones provided by Guile’s core
library.  *Note File System::, for documentation.

7.6.2.18 rnrs programs
......................

The ‘(rnrs programs (6))’ library provides procedures for process
management and introspection.

 -- Scheme Procedure: command-line
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Runtime Environment::, for documentation.

 -- Scheme Procedure: exit [status]
     This procedure is identical to the one provided by Guile’s core
     library.  *Note Processes::, for documentation.

7.6.2.19 rnrs arithmetic fixnums
................................

The ‘(rnrs arithmetic fixnums (6))’ library provides procedures for
performing arithmetic operations on an implementation-dependent range of
exact integer values, which R6RS refers to as "fixnums".  In Guile, the
size of a fixnum is determined by the size of the ‘SCM’ type; a single
SCM struct is guaranteed to be able to hold an entire fixnum, making
fixnum computations particularly efficient—(*note The SCM Type::).  On
32-bit systems, the most negative and most positive fixnum values are,
respectively, -536870912 and 536870911.

   Unless otherwise specified, all of the procedures below take fixnums
as arguments, and will raise an ‘&assertion’ condition if passed a
non-fixnum argument or an ‘&implementation-restriction’ condition if
their result is not itself a fixnum.

 -- Scheme Procedure: fixnum? obj
     Returns ‘#t’ if OBJ is a fixnum, ‘#f’ otherwise.

 -- Scheme Procedure: fixnum-width
 -- Scheme Procedure: least-fixnum
 -- Scheme Procedure: greatest-fixnum
     These procedures return, respectively, the maximum number of bits
     necessary to represent a fixnum value in Guile, the minimum fixnum
     value, and the maximum fixnum value.

 -- Scheme Procedure: fx=? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx>? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx<? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx>=? fx1 fx2 fx3 ...
 -- Scheme Procedure: fx<=? fx1 fx2 fx3 ...
     These procedures return ‘#t’ if their fixnum arguments are
     (respectively): equal, monotonically increasing, monotonically
     decreasing, monotonically nondecreasing, or monotonically
     nonincreasing; ‘#f’ otherwise.

 -- Scheme Procedure: fxzero? fx
 -- Scheme Procedure: fxpositive? fx
 -- Scheme Procedure: fxnegative? fx
 -- Scheme Procedure: fxodd? fx
 -- Scheme Procedure: fxeven? fx
     These numerical predicates return ‘#t’ if FX is, respectively,
     zero, greater than zero, less than zero, odd, or even; ‘#f’
     otherwise.

 -- Scheme Procedure: fxmax fx1 fx2 ...
 -- Scheme Procedure: fxmin fx1 fx2 ...
     These procedures return the maximum or minimum of their arguments.

 -- Scheme Procedure: fx+ fx1 fx2
 -- Scheme Procedure: fx* fx1 fx2
     These procedures return the sum or product of their arguments.

 -- Scheme Procedure: fx- fx1 fx2
 -- Scheme Procedure: fx- fx
     Returns the difference of FX1 and FX2, or the negation of FX, if
     called with a single argument.

     An ‘&assertion’ condition is raised if the result is not itself a
     fixnum.

 -- Scheme Procedure: fxdiv-and-mod fx1 fx2
 -- Scheme Procedure: fxdiv fx1 fx2
 -- Scheme Procedure: fxmod fx1 fx2
 -- Scheme Procedure: fxdiv0-and-mod0 fx1 fx2
 -- Scheme Procedure: fxdiv0 fx1 fx2
 -- Scheme Procedure: fxmod0 fx1 fx2
     These procedures implement number-theoretic division on fixnums;
     *Note (rnrs base)::, for a description of their semantics.

 -- Scheme Procedure: fx+/carry fx1 fx2 fx3
     Returns the two fixnum results of the following computation:
          (let* ((s (+ fx1 fx2 fx3))
                 (s0 (mod0 s (expt 2 (fixnum-width))))
                 (s1 (div0 s (expt 2 (fixnum-width)))))
            (values s0 s1))

 -- Scheme Procedure: fx-/carry fx1 fx2 fx3
     Returns the two fixnum results of the following computation:
          (let* ((d (- fx1 fx2 fx3))
                 (d0 (mod0 d (expt 2 (fixnum-width))))
                 (d1 (div0 d (expt 2 (fixnum-width)))))
            (values d0 d1))

 -- Scheme Procedure: fx*/carry fx1 fx2 fx3
          Returns the two fixnum results of the following computation:
          (let* ((s (+ (* fx1 fx2) fx3))
                 (s0 (mod0 s (expt 2 (fixnum-width))))
                 (s1 (div0 s (expt 2 (fixnum-width)))))
            (values s0 s1))

 -- Scheme Procedure: fxnot fx
 -- Scheme Procedure: fxand fx1 ...
 -- Scheme Procedure: fxior fx1 ...
 -- Scheme Procedure: fxxor fx1 ...
     These procedures are identical to the ‘lognot’, ‘logand’, ‘logior’,
     and ‘logxor’ procedures provided by Guile’s core library.  *Note
     Bitwise Operations::, for documentation.

 -- Scheme Procedure: fxif fx1 fx2 fx3
     Returns the bitwise “if” of its fixnum arguments.  The bit at
     position ‘i’ in the return value will be the ‘i’th bit from FX2 if
     the ‘i’th bit of FX1 is 1, the ‘i’th bit from FX3.

 -- Scheme Procedure: fxbit-count fx
     Returns the number of 1 bits in the two’s complement representation
     of FX.

 -- Scheme Procedure: fxlength fx
     Returns the number of bits necessary to represent FX.

 -- Scheme Procedure: fxfirst-bit-set fx
     Returns the index of the least significant 1 bit in the two’s
     complement representation of FX.

 -- Scheme Procedure: fxbit-set? fx1 fx2
     Returns ‘#t’ if the FX2th bit in the two’s complement
     representation of FX1 is 1, ‘#f’ otherwise.

 -- Scheme Procedure: fxcopy-bit fx1 fx2 fx3
     Returns the result of setting the FX2th bit of FX1 to the FX2th bit
     of FX3.

 -- Scheme Procedure: fxbit-field fx1 fx2 fx3
     Returns the integer representation of the contiguous sequence of
     bits in FX1 that starts at position FX2 (inclusive) and ends at
     position FX3 (exclusive).

 -- Scheme Procedure: fxcopy-bit-field fx1 fx2 fx3 fx4
     Returns the result of replacing the bit field in FX1 with start and
     end positions FX2 and FX3 with the corresponding bit field from
     FX4.

 -- Scheme Procedure: fxarithmetic-shift fx1 fx2
 -- Scheme Procedure: fxarithmetic-shift-left fx1 fx2
 -- Scheme Procedure: fxarithmetic-shift-right fx1 fx2
     Returns the result of shifting the bits of FX1 right or left by the
     FX2 positions.  ‘fxarithmetic-shift’ is identical to
     ‘fxarithmetic-shift-left’.

 -- Scheme Procedure: fxrotate-bit-field fx1 fx2 fx3 fx4
     Returns the result of cyclically permuting the bit field in FX1
     with start and end positions FX2 and FX3 by FX4 bits in the
     direction of more significant bits.

 -- Scheme Procedure: fxreverse-bit-field fx1 fx2 fx3
     Returns the result of reversing the order of the bits of FX1
     between position FX2 (inclusive) and position FX3 (exclusive).

7.6.2.20 rnrs arithmetic flonums
................................

The ‘(rnrs arithmetic flonums (6))’ library provides procedures for
performing arithmetic operations on inexact representations of real
numbers, which R6RS refers to as "flonums".

   Unless otherwise specified, all of the procedures below take flonums
as arguments, and will raise an ‘&assertion’ condition if passed a
non-flonum argument.

 -- Scheme Procedure: flonum? obj
     Returns ‘#t’ if OBJ is a flonum, ‘#f’ otherwise.

 -- Scheme Procedure: real->flonum x
     Returns the flonum that is numerically closest to the real number
     X.

 -- Scheme Procedure: fl=? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl<? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl<=? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl>? fl1 fl2 fl3 ...
 -- Scheme Procedure: fl>=? fl1 fl2 fl3 ...
     These procedures return ‘#t’ if their flonum arguments are
     (respectively): equal, monotonically increasing, monotonically
     decreasing, monotonically nondecreasing, or monotonically
     nonincreasing; ‘#f’ otherwise.

 -- Scheme Procedure: flinteger? fl
 -- Scheme Procedure: flzero? fl
 -- Scheme Procedure: flpositive? fl
 -- Scheme Procedure: flnegative? fl
 -- Scheme Procedure: flodd? fl
 -- Scheme Procedure: fleven? fl
     These numerical predicates return ‘#t’ if FL is, respectively, an
     integer, zero, greater than zero, less than zero, odd, even, ‘#f’
     otherwise.  In the case of ‘flodd?’ and ‘fleven?’, FL must be an
     integer-valued flonum.

 -- Scheme Procedure: flfinite? fl
 -- Scheme Procedure: flinfinite? fl
 -- Scheme Procedure: flnan? fl
     These numerical predicates return ‘#t’ if FL is, respectively, not
     infinite, infinite, or a ‘NaN’ value.

 -- Scheme Procedure: flmax fl1 fl2 ...
 -- Scheme Procedure: flmin fl1 fl2 ...
     These procedures return the maximum or minimum of their arguments.

 -- Scheme Procedure: fl+ fl1 ...
 -- Scheme Procedure: fl* fl ...
     These procedures return the sum or product of their arguments.

 -- Scheme Procedure: fl- fl1 fl2 ...
 -- Scheme Procedure: fl- fl
 -- Scheme Procedure: fl/ fl1 fl2 ...
 -- Scheme Procedure: fl/ fl
     These procedures return, respectively, the difference or quotient
     of their arguments when called with two arguments; when called with
     a single argument, they return the additive or multiplicative
     inverse of FL.

 -- Scheme Procedure: flabs fl
     Returns the absolute value of FL.

 -- Scheme Procedure: fldiv-and-mod fl1 fl2
 -- Scheme Procedure: fldiv fl1 fl2
 -- Scheme Procedure: fldmod fl1 fl2
 -- Scheme Procedure: fldiv0-and-mod0 fl1 fl2
 -- Scheme Procedure: fldiv0 fl1 fl2
 -- Scheme Procedure: flmod0 fl1 fl2
     These procedures implement number-theoretic division on flonums;
     *Note (rnrs base)::, for a description for their semantics.

 -- Scheme Procedure: flnumerator fl
 -- Scheme Procedure: fldenominator fl
     These procedures return the numerator or denominator of FL as a
     flonum.

 -- Scheme Procedure: flfloor fl1
 -- Scheme Procedure: flceiling fl
 -- Scheme Procedure: fltruncate fl
 -- Scheme Procedure: flround fl
     These procedures are identical to the ‘floor’, ‘ceiling’,
     ‘truncate’, and ‘round’ procedures provided by Guile’s core
     library.  *Note Arithmetic::, for documentation.

 -- Scheme Procedure: flexp fl
 -- Scheme Procedure: fllog fl
 -- Scheme Procedure: fllog fl1 fl2
 -- Scheme Procedure: flsin fl
 -- Scheme Procedure: flcos fl
 -- Scheme Procedure: fltan fl
 -- Scheme Procedure: flasin fl
 -- Scheme Procedure: flacos fl
 -- Scheme Procedure: flatan fl
 -- Scheme Procedure: flatan fl1 fl2
     These procedures, which compute the usual transcendental functions,
     are the flonum variants of the procedures provided by the R6RS base
     library (*note (rnrs base)::).

 -- Scheme Procedure: flsqrt fl
     Returns the square root of FL.  If FL is ‘-0.0’, -0.0 is returned;
     for other negative values, a ‘NaN’ value is returned.

 -- Scheme Procedure: flexpt fl1 fl2
     Returns the value of FL1 raised to the power of FL2.

   The following condition types are provided to allow Scheme
implementations that do not support infinities or ‘NaN’ values to
indicate that a computation resulted in such a value.  Guile supports
both of these, so these conditions will never be raised by Guile’s
standard libraries implementation.

 -- Condition Type: &no-infinities
 -- Scheme Procedure: make-no-infinities-violation obj
 -- Scheme Procedure: no-infinities-violation?
     A condition type indicating that a computation resulted in an
     infinite value on a Scheme implementation incapable of representing
     infinities.

 -- Condition Type: &no-nans
 -- Scheme Procedure: make-no-nans-violation obj
 -- Scheme Procedure: no-nans-violation? obj
     A condition type indicating that a computation resulted in a ‘NaN’
     value on a Scheme implementation incapable of representing ‘NaN’s.

 -- Scheme Procedure: fixnum->flonum fx
     Returns the flonum that is numerically closest to the fixnum FX.

7.6.2.21 rnrs arithmetic bitwise
................................

The ‘(rnrs arithmetic bitwise (6))’ library provides procedures for
performing bitwise arithmetic operations on the two’s complement
representations of fixnums.

   This library and the procedures it exports share functionality with
SRFI-60, which provides support for bitwise manipulation of integers
(*note SRFI-60::).

 -- Scheme Procedure: bitwise-not ei
 -- Scheme Procedure: bitwise-and ei1 ...
 -- Scheme Procedure: bitwise-ior ei1 ...
 -- Scheme Procedure: bitwise-xor ei1 ...
     These procedures are identical to the ‘lognot’, ‘logand’, ‘logior’,
     and ‘logxor’ procedures provided by Guile’s core library.  *Note
     Bitwise Operations::, for documentation.

 -- Scheme Procedure: bitwise-if ei1 ei2 ei3
     Returns the bitwise “if” of its arguments.  The bit at position ‘i’
     in the return value will be the ‘i’th bit from EI2 if the ‘i’th bit
     of EI1 is 1, the ‘i’th bit from EI3.

 -- Scheme Procedure: bitwise-bit-count ei
     Returns the number of 1 bits in the two’s complement representation
     of EI.

 -- Scheme Procedure: bitwise-length ei
     Returns the number of bits necessary to represent EI.

 -- Scheme Procedure: bitwise-first-bit-set ei
     Returns the index of the least significant 1 bit in the two’s
     complement representation of EI.

 -- Scheme Procedure: bitwise-bit-set? ei1 ei2
     Returns ‘#t’ if the EI2th bit in the two’s complement
     representation of EI1 is 1, ‘#f’ otherwise.

 -- Scheme Procedure: bitwise-copy-bit ei1 ei2 ei3
     Returns the result of setting the EI2th bit of EI1 to the EI2th bit
     of EI3.

 -- Scheme Procedure: bitwise-bit-field ei1 ei2 ei3
     Returns the integer representation of the contiguous sequence of
     bits in EI1 that starts at position EI2 (inclusive) and ends at
     position EI3 (exclusive).

 -- Scheme Procedure: bitwise-copy-bit-field ei1 ei2 ei3 ei4
     Returns the result of replacing the bit field in EI1 with start and
     end positions EI2 and EI3 with the corresponding bit field from
     EI4.

 -- Scheme Procedure: bitwise-arithmetic-shift ei1 ei2
 -- Scheme Procedure: bitwise-arithmetic-shift-left ei1 ei2
 -- Scheme Procedure: bitwise-arithmetic-shift-right ei1 ei2
     Returns the result of shifting the bits of EI1 right or left by the
     EI2 positions.  ‘bitwise-arithmetic-shift’ is identical to
     ‘bitwise-arithmetic-shift-left’.

 -- Scheme Procedure: bitwise-rotate-bit-field ei1 ei2 ei3 ei4
     Returns the result of cyclically permuting the bit field in EI1
     with start and end positions EI2 and EI3 by EI4 bits in the
     direction of more significant bits.

 -- Scheme Procedure: bitwise-reverse-bit-field ei1 ei2 ei3
     Returns the result of reversing the order of the bits of EI1
     between position EI2 (inclusive) and position EI3 (exclusive).

7.6.2.22 rnrs syntax-case
.........................

The ‘(rnrs syntax-case (6))’ library provides access to the
‘syntax-case’ system for writing hygienic macros.  With one exception,
all of the forms and procedures exported by this library are
“re-exports” of Guile’s native support for ‘syntax-case’; *Note Syntax
Case::, for documentation, examples, and rationale.

 -- Scheme Procedure: make-variable-transformer proc
     Creates a new variable transformer out of PROC, a procedure that
     takes a syntax object as input and returns a syntax object.  If an
     identifier to which the result of this procedure is bound appears
     on the left-hand side of a ‘set!’ expression, PROC will be called
     with a syntax object representing the entire ‘set!’ expression, and
     its return value will replace that ‘set!’ expression.

 -- Scheme Syntax: syntax-case expression (literal ...) clause ...
     The ‘syntax-case’ pattern matching form.

 -- Scheme Syntax: syntax template
 -- Scheme Syntax: quasisyntax template
 -- Scheme Syntax: unsyntax template
 -- Scheme Syntax: unsyntax-splicing template
     These forms allow references to be made in the body of a
     syntax-case output expression subform to datum and non-datum
     values.  They are identical to the forms provided by Guile’s core
     library; *Note Syntax Case::, for documentation.

 -- Scheme Procedure: identifier? obj
 -- Scheme Procedure: bound-identifier=? id1 id2
 -- Scheme Procedure: free-identifier=? id1 id2
     These predicate procedures operate on syntax objects representing
     Scheme identifiers.  ‘identifier?’ returns ‘#t’ if OBJ represents
     an identifier, ‘#f’ otherwise.  ‘bound-identifier=?’ returns ‘#t’
     if and only if a binding for ID1 would capture a reference to ID2
     in the transformer’s output, or vice-versa.  ‘free-identifier=?’
     returns ‘#t’ if and only ID1 and ID2 would refer to the same
     binding in the output of the transformer, independent of any
     bindings introduced by the transformer.

 -- Scheme Procedure: generate-temporaries l
     Returns a list, of the same length as L, which must be a list or a
     syntax object representing a list, of globally unique symbols.

 -- Scheme Procedure: syntax->datum syntax-object
 -- Scheme Procedure: datum->syntax template-id datum
     These procedures convert wrapped syntax objects to and from Scheme
     datum values.  The syntax object returned by ‘datum->syntax’ shares
     contextual information with the syntax object TEMPLATE-ID.

 -- Scheme Procedure: syntax-violation whom message form
 -- Scheme Procedure: syntax-violation whom message form subform
     Constructs a new compound condition that includes the following
     simple conditions:
        • If WHOM is not ‘#f’, a ‘&who’ condition with the WHOM as its
          field
        • A ‘&message’ condition with the specified MESSAGE
        • A ‘&syntax’ condition with the specified FORM and optional
          SUBFORM fields

7.6.2.23 rnrs hashtables
........................

The ‘(rnrs hashtables (6))’ library provides structures and procedures
for creating and accessing hash tables.  The hash tables API defined by
R6RS is substantially similar to both Guile’s native hash tables
implementation as well as the one provided by SRFI-69; *Note Hash
Tables::, and *note SRFI-69::, respectively.  Note that you can write
portable R6RS library code that manipulates SRFI-69 hash tables (by
importing the ‘(srfi :69)’ library); however, hash tables created by one
API cannot be used by another.

   Like SRFI-69 hash tables—and unlike Guile’s native ones—R6RS hash
tables associate hash and equality functions with a hash table at the
time of its creation.  Additionally, R6RS allows for the creation (via
‘hashtable-copy’; see below) of immutable hash tables.

 -- Scheme Procedure: make-eq-hashtable
 -- Scheme Procedure: make-eq-hashtable k
     Returns a new hash table that uses ‘eq?’ to compare keys and
     Guile’s ‘hashq’ procedure as a hash function.  If K is given, it
     specifies the initial capacity of the hash table.

 -- Scheme Procedure: make-eqv-hashtable
 -- Scheme Procedure: make-eqv-hashtable k
     Returns a new hash table that uses ‘eqv?’ to compare keys and
     Guile’s ‘hashv’ procedure as a hash function.  If K is given, it
     specifies the initial capacity of the hash table.

 -- Scheme Procedure: make-hashtable hash-function equiv
 -- Scheme Procedure: make-hashtable hash-function equiv k
     Returns a new hash table that uses EQUIV to compare keys and
     HASH-FUNCTION as a hash function.  EQUIV must be a procedure that
     accepts two arguments and returns a true value if they are
     equivalent, ‘#f’ otherwise; HASH-FUNCTION must be a procedure that
     accepts one argument and returns a non-negative integer.

     If K is given, it specifies the initial capacity of the hash table.

 -- Scheme Procedure: hashtable? obj
     Returns ‘#t’ if OBJ is an R6RS hash table, ‘#f’ otherwise.

 -- Scheme Procedure: hashtable-size hashtable
     Returns the number of keys currently in the hash table HASHTABLE.

 -- Scheme Procedure: hashtable-ref hashtable key default
     Returns the value associated with KEY in the hash table HASHTABLE,
     or DEFAULT if none is found.

 -- Scheme Procedure: hashtable-set! hashtable key obj
     Associates the key KEY with the value OBJ in the hash table
     HASHTABLE, and returns an unspecified value.  An ‘&assertion’
     condition is raised if HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-delete! hashtable key
     Removes any association found for the key KEY in the hash table
     HASHTABLE, and returns an unspecified value.  An ‘&assertion’
     condition is raised if HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-contains? hashtable key
     Returns ‘#t’ if the hash table HASHTABLE contains an association
     for the key KEY, ‘#f’ otherwise.

 -- Scheme Procedure: hashtable-update! hashtable key proc default
     Associates with KEY in the hash table HASHTABLE the result of
     calling PROC, which must be a procedure that takes one argument, on
     the value currently associated KEY in HASHTABLE—or on DEFAULT if no
     such association exists.  An ‘&assertion’ condition is raised if
     HASHTABLE is immutable.

 -- Scheme Procedure: hashtable-copy hashtable
 -- Scheme Procedure: hashtable-copy hashtable mutable
     Returns a copy of the hash table HASHTABLE.  If the optional
     argument MUTABLE is provided and is a true value, the new hash
     table will be mutable.

 -- Scheme Procedure: hashtable-clear! hashtable
 -- Scheme Procedure: hashtable-clear! hashtable k
     Removes all of the associations from the hash table HASHTABLE.  The
     optional argument K, which specifies a new capacity for the hash
     table, is accepted by Guile’s ‘(rnrs hashtables)’ implementation,
     but is ignored.

 -- Scheme Procedure: hashtable-keys hashtable
     Returns a vector of the keys with associations in the hash table
     HASHTABLE, in an unspecified order.

 -- Scheme Procedure: hashtable-entries hashtable
     Return two values—a vector of the keys with associations in the
     hash table HASHTABLE, and a vector of the values to which these
     keys are mapped, in corresponding but unspecified order.

 -- Scheme Procedure: hashtable-equivalence-function hashtable
     Returns the equivalence predicated use by HASHTABLE.  This
     procedure returns ‘eq?’ and ‘eqv?’, respectively, for hash tables
     created by ‘make-eq-hashtable’ and ‘make-eqv-hashtable’.

 -- Scheme Procedure: hashtable-hash-function hashtable
     Returns the hash function used by HASHTABLE.  For hash tables
     created by ‘make-eq-hashtable’ or ‘make-eqv-hashtable’, ‘#f’ is
     returned.

 -- Scheme Procedure: hashtable-mutable? hashtable
     Returns ‘#t’ if HASHTABLE is mutable, ‘#f’ otherwise.

   A number of hash functions are provided for convenience:

 -- Scheme Procedure: equal-hash obj
     Returns an integer hash value for OBJ, based on its structure and
     current contents.  This hash function is suitable for use with
     ‘equal?’ as an equivalence function.

 -- Scheme Procedure: string-hash string
 -- Scheme Procedure: symbol-hash symbol
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Hash Table Reference::, for documentation.

 -- Scheme Procedure: string-ci-hash string
     Returns an integer hash value for STRING based on its contents,
     ignoring case.  This hash function is suitable for use with
     ‘string-ci=?’ as an equivalence function.

7.6.2.24 rnrs enums
...................

The ‘(rnrs enums (6))’ library provides structures and procedures for
working with enumerable sets of symbols.  Guile’s implementation defines
an "enum-set" record type that encapsulates a finite set of distinct
symbols, the "universe", and a subset of these symbols, which define the
enumeration set.

   The SRFI-1 list library provides a number of procedures for
performing set operations on lists; Guile’s ‘(rnrs enums)’
implementation makes use of several of them.  *Note SRFI-1 Set
Operations::, for more information.

 -- Scheme Procedure: make-enumeration symbol-list
     Returns a new enum-set whose universe and enumeration set are both
     equal to SYMBOL-LIST, a list of symbols.

 -- Scheme Procedure: enum-set-universe enum-set
     Returns an enum-set representing the universe of ENUM-SET, an
     enum-set.

 -- Scheme Procedure: enum-set-indexer enum-set
     Returns a procedure that takes a single argument and returns the
     zero-indexed position of that argument in the universe of ENUM-SET,
     or ‘#f’ if its argument is not a member of that universe.

 -- Scheme Procedure: enum-set-constructor enum-set
     Returns a procedure that takes a single argument, a list of symbols
     from the universe of ENUM-SET, an enum-set, and returns a new
     enum-set with the same universe that represents a subset containing
     the specified symbols.

 -- Scheme Procedure: enum-set->list enum-set
     Returns a list containing the symbols of the set represented by
     ENUM-SET, an enum-set, in the order that they appear in the
     universe of ENUM-SET.

 -- Scheme Procedure: enum-set-member? symbol enum-set
 -- Scheme Procedure: enum-set-subset? enum-set1 enum-set2
 -- Scheme Procedure: enum-set=? enum-set1 enum-set2
     These procedures test for membership of symbols and enum-sets in
     other enum-sets.  ‘enum-set-member?’ returns ‘#t’ if and only if
     SYMBOL is a member of the subset specified by ENUM-SET.
     ‘enum-set-subset?’ returns ‘#t’ if and only if the universe of
     ENUM-SET1 is a subset of the universe of ENUM-SET2 and every symbol
     in ENUM-SET1 is present in ENUM-SET2.  ‘enum-set=?’ returns ‘#t’ if
     and only if ENUM-SET1 is a subset, as per ‘enum-set-subset?’ of
     ENUM-SET2 and vice versa.

 -- Scheme Procedure: enum-set-union enum-set1 enum-set2
 -- Scheme Procedure: enum-set-intersection enum-set1 enum-set2
 -- Scheme Procedure: enum-set-difference enum-set1 enum-set2
     These procedures return, respectively, the union, intersection, and
     difference of their enum-set arguments.

 -- Scheme Procedure: enum-set-complement enum-set
     Returns ENUM-SET’s complement (an enum-set), with regard to its
     universe.

 -- Scheme Procedure: enum-set-projection enum-set1 enum-set2
     Returns the projection of the enum-set ENUM-SET1 onto the universe
     of the enum-set ENUM-SET2.

 -- Scheme Syntax: define-enumeration type-name (symbol ...)
          constructor-syntax
     Evaluates to two new definitions: A constructor bound to
     CONSTRUCTOR-SYNTAX that behaves similarly to constructors created
     by ‘enum-set-constructor’, above, and creates new ENUM-SETs in the
     universe specified by ‘(symbol ...)’; and a “predicate macro” bound
     to TYPE-NAME, which has the following form:

          (TYPE-NAME sym)

     If SYM is a member of the universe specified by the SYMBOLs above,
     this form evaluates to SYM.  Otherwise, a ‘&syntax’ condition is
     raised.

7.6.2.25 rnrs
.............

The ‘(rnrs (6))’ library is a composite of all of the other R6RS
standard libraries—it imports and re-exports all of their exported
procedures and syntactic forms—with the exception of the following
libraries:

   • ‘(rnrs eval (6))’
   • ‘(rnrs mutable-pairs (6))’
   • ‘(rnrs mutable-strings (6))’
   • ‘(rnrs r5rs (6))’

7.6.2.26 rnrs eval
..................

The ‘(rnrs eval (6)’ library provides procedures for performing
“on-the-fly” evaluation of expressions.

 -- Scheme Procedure: eval expression environment
     Evaluates EXPRESSION, which must be a datum representation of a
     valid Scheme expression, in the environment specified by
     ENVIRONMENT.  This procedure is identical to the one provided by
     Guile’s code library; *Note Fly Evaluation::, for documentation.

 -- Scheme Procedure: environment import-spec ...
     Constructs and returns a new environment based on the specified
     IMPORT-SPECs, which must be datum representations of the import
     specifications used with the ‘import’ form.  *Note R6RS
     Libraries::, for documentation.

7.6.2.27 rnrs mutable-pairs
...........................

The ‘(rnrs mutable-pairs (6))’ library provides the ‘set-car!’ and
‘set-cdr!’ procedures, which allow the ‘car’ and ‘cdr’ fields of a pair
to be modified.

   These procedures are identical to the ones provide by Guile’s core
library.  *Note Pairs::, for documentation.  All pairs in Guile are
mutable; consequently, these procedures will never throw the
‘&assertion’ condition described in the R6RS libraries specification.

7.6.2.28 rnrs mutable-strings
.............................

The ‘(rnrs mutable-strings (6))’ library provides the ‘string-set!’ and
‘string-fill!’ procedures, which allow the content of strings to be
modified “in-place.”

   These procedures are identical to the ones provided by Guile’s core
library.  *Note String Modification::, for documentation.  All strings
in Guile are mutable; consequently, these procedures will never throw
the ‘&assertion’ condition described in the R6RS libraries
specification.

7.6.2.29 rnrs r5rs
..................

The ‘(rnrs r5rs (6))’ library exports bindings for some procedures
present in R5RS but omitted from the R6RS base library specification.

 -- Scheme Procedure: exact->inexact z
 -- Scheme Procedure: inexact->exact z
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Exactness::, for documentation.

 -- Scheme Procedure: quotient n1 n2
 -- Scheme Procedure: remainder n1 n2
 -- Scheme Procedure: modulo n1 n2
     These procedures are identical to the ones provided by Guile’s core
     library.  *Note Integer Operations::, for documentation.

 -- Scheme Syntax: delay expr
 -- Scheme Procedure: force promise
     The ‘delay’ form and the ‘force’ procedure are identical to their
     counterparts in Guile’s core library.  *Note Delayed Evaluation::,
     for documentation.

 -- Scheme Procedure: null-environment n
 -- Scheme Procedure: scheme-report-environment n
     These procedures are identical to the ones provided by the ‘(ice-9
     r5rs)’ Guile module.  *Note Environments::, for documentation.

7.7 Pattern Matching
====================

The ‘(ice-9 match)’ module provides a "pattern matcher", written by Alex
Shinn, and compatible with Andrew K. Wright’s pattern matcher found in
many Scheme implementations.

   A pattern matcher can match an object against several patterns and
extract the elements that make it up.  Patterns can represent any Scheme
object: lists, strings, symbols, records, etc.  They can optionally
contain "pattern variables".  When a matching pattern is found, an
expression associated with the pattern is evaluated, optionally with all
pattern variables bound to the corresponding elements of the object:

     (let ((l '(hello (world))))
       (match l           ;; <- the input object
         (('hello (who))  ;; <- the pattern
          who)))          ;; <- the expression evaluated upon matching
     ⇒ world

   In this example, list L matches the pattern ‘('hello (who))’, because
it is a two-element list whose first element is the symbol ‘hello’ and
whose second element is a one-element list.  Here WHO is a pattern
variable.  ‘match’, the pattern matcher, locally binds WHO to the value
contained in this one-element list—i.e., the symbol ‘world’.  An error
would be raised if L did not match the pattern.

   The same object can be matched against a simpler pattern:

     (let ((l '(hello (world))))
       (match l
         ((x y)
          (values x y))))
     ⇒ hello
     ⇒ (world)

   Here pattern ‘(x y)’ matches any two-element list, regardless of the
types of these elements.  Pattern variables X and Y are bound to,
respectively, the first and second element of L.

   Patterns can be composed, and nested.  For instance, ‘...’ (ellipsis)
means that the previous pattern may be matched zero or more times in a
list:

     (match lst
       (((heads tails ...) ...)
        heads))

This expression returns the first element of each list within LST.  For
proper lists of proper lists, it is equivalent to ‘(map car lst)’.
However, it performs additional checks to make sure that LST and the
lists therein are proper lists, as prescribed by the pattern, raising an
error if they are not.

   Compared to hand-written code, pattern matching noticeably improves
clarity and conciseness—no need to resort to series of ‘car’ and ‘cdr’
calls when matching lists, for instance.  It also improves robustness,
by making sure the input _completely_ matches the pattern—conversely,
hand-written code often trades robustness for conciseness.  And of
course, ‘match’ is a macro, and the code it expands to is just as
efficient as equivalent hand-written code.

   The pattern matcher is defined as follows:

 -- Scheme Syntax: match exp clause1 clause2 …
     Match object EXP against the patterns in CLAUSE1 CLAUSE2 … in the
     order in which they appear.  Return the value produced by the first
     matching clause.  If no clause matches, throw an exception with key
     ‘match-error’.

     Each clause has the form ‘(pattern body1 body2 …)’.  Each PATTERN
     must follow the syntax described below.  Each body is an arbitrary
     Scheme expression, possibly referring to pattern variables of
     PATTERN.

   The syntax and interpretation of patterns is as follows:

        patterns:                       matches:

pat ::= identifier                      anything, and binds identifier
      | _                               anything
      | ()                              the empty list
      | #t                              #t
      | #f                              #f
      | string                          a string
      | number                          a number
      | character                       a character
      | 'sexp                           an s-expression
      | 'symbol                         a symbol (special case of s-expr)
      | (pat_1 ... pat_n)               list of n elements
      | (pat_1 ... pat_n . pat_{n+1})   list of n or more
      | (pat_1 ... pat_n pat_n+1 ooo)   list of n or more, each element
                                          of remainder must match pat_n+1
      | #(pat_1 ... pat_n)              vector of n elements
      | #(pat_1 ... pat_n pat_n+1 ooo)  vector of n or more, each element
                                          of remainder must match pat_n+1
      | #&pat                           box
      | ($ record-name pat_1 ... pat_n) a record
      | (= field pat)                   a ``field'' of an object
      | (and pat_1 ... pat_n)           if all of pat_1 thru pat_n match
      | (or pat_1 ... pat_n)            if any of pat_1 thru pat_n match
      | (not pat_1 ... pat_n)           if all pat_1 thru pat_n don't match
      | (? predicate pat_1 ... pat_n)   if predicate true and all of
                                          pat_1 thru pat_n match
      | (set! identifier)               anything, and binds setter
      | (get! identifier)               anything, and binds getter
      | `qp                             a quasi-pattern
      | (identifier *** pat)            matches pat in a tree and binds
                                        identifier to the path leading
                                        to the object that matches pat

ooo ::= ...                             zero or more
      | ___                             zero or more
      | ..1                             1 or more

        quasi-patterns:                 matches:

qp  ::= ()                              the empty list
      | #t                              #t
      | #f                              #f
      | string                          a string
      | number                          a number
      | character                       a character
      | identifier                      a symbol
      | (qp_1 ... qp_n)                 list of n elements
      | (qp_1 ... qp_n . qp_{n+1})      list of n or more
      | (qp_1 ... qp_n qp_n+1 ooo)      list of n or more, each element
                                          of remainder must match qp_n+1
      | #(qp_1 ... qp_n)                vector of n elements
      | #(qp_1 ... qp_n qp_n+1 ooo)     vector of n or more, each element
                                          of remainder must match qp_n+1
      | #&qp                            box
      | ,pat                            a pattern
      | ,@pat                           a pattern

   The names ‘quote’, ‘quasiquote’, ‘unquote’, ‘unquote-splicing’, ‘?’,
‘_’, ‘$’, ‘and’, ‘or’, ‘not’, ‘set!’, ‘get!’, ‘...’, and ‘___’ cannot be
used as pattern variables.

   Here is a more complex example:

     (use-modules (srfi srfi-9))

     (let ()
       (define-record-type person
         (make-person name friends)
         person?
         (name    person-name)
         (friends person-friends))

       (letrec ((alice (make-person "Alice" (delay (list bob))))
                (bob   (make-person "Bob" (delay (list alice)))))
         (match alice
           (($ person name (= force (($ person "Bob"))))
            (list 'friend-of-bob name))
           (_ #f))))

     ⇒ (friend-of-bob "Alice")

Here the ‘$’ pattern is used to match a SRFI-9 record of type PERSON
containing two or more slots.  The value of the first slot is bound to
NAME.  The ‘=’ pattern is used to apply ‘force’ on the second slot, and
then checking that the result matches the given pattern.  In other
words, the complete pattern matches any PERSON whose second slot is a
promise that evaluates to a one-element list containing a PERSON whose
first slot is ‘"Bob"’.

   Please refer to the ‘ice-9/match.upstream.scm’ file in your Guile
installation for more details.

   Guile also comes with a pattern matcher specifically tailored to SXML
trees, *Note sxml-match::.

7.8 Readline Support
====================

Guile comes with an interface module to the readline library (*note
(readline)Top::).  This makes interactive use much more convenient,
because of the command-line editing features of readline.  Using ‘(ice-9
readline)’, you can navigate through the current input line with the
cursor keys, retrieve older command lines from the input history and
even search through the history entries.

7.8.1 Loading Readline Support
------------------------------

The module is not loaded by default and so has to be loaded and
activated explicitly.  This is done with two simple lines of code:

     (use-modules (ice-9 readline))
     (activate-readline)

   The first line will load the necessary code, and the second will
activate readline’s features for the REPL. If you plan to use this
module often, you should save these to lines to your ‘.guile’ personal
startup file.

   You will notice that the REPL’s behaviour changes a bit when you have
loaded the readline module.  For example, when you press Enter before
typing in the closing parentheses of a list, you will see the
"continuation" prompt, three dots: ‘...’ This gives you a nice visual
feedback when trying to match parentheses.  To make this even easier,
"bouncing parentheses" are implemented.  That means that when you type
in a closing parentheses, the cursor will jump to the corresponding
opening parenthesis for a short time, making it trivial to make them
match.

   Once the readline module is activated, all lines entered
interactively will be stored in a history and can be recalled later
using the cursor-up and -down keys.  Readline also understands the Emacs
keys for navigating through the command line and history.

   When you quit your Guile session by evaluating ‘(quit)’ or pressing
Ctrl-D, the history will be saved to the file ‘.guile_history’ and read
in when you start Guile for the next time.  Thus you can start a new
Guile session and still have the (probably long-winded) definition
expressions available.

   You can specify a different history file by setting the environment
variable ‘GUILE_HISTORY’.  And you can make Guile specific
customizations to your ‘.inputrc’ by testing for application ‘Guile’
(*note (readline)Conditional Init Constructs::).  For instance to define
a key inserting a matched pair of parentheses,

     $if Guile
       "\C-o": "()\C-b"
     $endif

7.8.2 Readline Options
----------------------

The readline interface module can be tweaked in a few ways to better
suit the user’s needs.  Configuration is done via the readline module’s
options interface, in a similar way to the evaluator and debugging
options (*note Runtime Options::).

 -- Scheme Procedure: readline-options
 -- Scheme Procedure: readline-enable option-name
 -- Scheme Procedure: readline-disable option-name
 -- Scheme Syntax: readline-set! option-name value
     Accessors for the readline options.  Note that unlike the
     enable/disable procedures, ‘readline-set!’ is syntax, which expects
     an unquoted option name.

   Here is the list of readline options generated by typing
‘(readline-options 'help)’ in Guile.  You can also see the default
values.

     history-file    yes     Use history file.
     history-length  200     History length.
     bounce-parens   500     Time (ms) to show matching opening parenthesis
                             (0 = off).

   The readline options interface can only be used _after_ loading the
readline module, because it is defined in that module.

7.8.3 Readline Functions
------------------------

The following functions are provided by

     (use-modules (ice-9 readline))

   There are two ways to use readline from Scheme code, either make
calls to ‘readline’ directly to get line by line input, or use the
readline port below with all the usual reading functions.

 -- Function: readline [prompt]
     Read a line of input from the user and return it as a string
     (without a newline at the end).  PROMPT is the prompt to show, or
     the default is the string set in ‘set-readline-prompt!’ below.

          (readline "Type something: ") ⇒ "hello"

 -- Function: set-readline-input-port! port
 -- Function: set-readline-output-port! port
     Set the input and output port the readline function should read
     from and write to.  PORT must be a file port (*note File Ports::),
     and should usually be a terminal.

     The default is the ‘current-input-port’ and ‘current-output-port’
     (*note Default Ports::) when ‘(ice-9 readline)’ loads, which in an
     interactive user session means the Unix “standard input” and
     “standard output”.

7.8.3.1 Readline Port
.....................

 -- Function: readline-port
     Return a buffered input port (*note Buffered Input::) which calls
     the ‘readline’ function above to get input.  This port can be used
     with all the usual reading functions (‘read’, ‘read-char’, etc),
     and the user gets the interactive editing features of readline.

     There’s only a single readline port created.  ‘readline-port’
     creates it when first called, and on subsequent calls just returns
     what it previously made.

 -- Function: activate-readline
     If the ‘current-input-port’ is a terminal (*note ‘isatty?’:
     Terminals and Ptys.) then enable readline for all reading from
     ‘current-input-port’ (*note Default Ports::) and enable readline
     features in the interactive REPL (*note The REPL::).

          (activate-readline)
          (read-char)

     ‘activate-readline’ enables readline on ‘current-input-port’ simply
     by a ‘set-current-input-port’ to the ‘readline-port’ above.  An
     application can do that directly if the extra REPL features that
     ‘activate-readline’ adds are not wanted.

 -- Function: set-readline-prompt! prompt1 [prompt2]
     Set the prompt string to print when reading input.  This is used
     when reading through ‘readline-port’, and is also the default
     prompt for the ‘readline’ function above.

     PROMPT1 is the initial prompt shown.  If a user might enter an
     expression across multiple lines, then PROMPT2 is a different
     prompt to show further input required.  In the Guile REPL for
     instance this is an ellipsis (‘...’).

     See ‘set-buffered-input-continuation?!’ (*note Buffered Input::)
     for an application to indicate the boundaries of logical
     expressions (assuming of course an application has such a notion).

7.8.3.2 Completion
..................

 -- Function: with-readline-completion-function completer thunk
     Call ‘(THUNK)’ with COMPLETER as the readline tab completion
     function to be used in any readline calls within that THUNK.
     COMPLETER can be ‘#f’ for no completion.

     COMPLETER will be called as ‘(COMPLETER text state)’, as described
     in (*note (readline)How Completing Works::).  TEXT is a partial
     word to be completed, and each COMPLETER call should return a
     possible completion string or ‘#f’ when no more.  STATE is ‘#f’ for
     the first call asking about a new TEXT then ‘#t’ while getting
     further completions of that TEXT.

     Here’s an example COMPLETER for user login names from the password
     file (*note User Information::), much like readline’s own
     ‘rl_username_completion_function’,

          (define (username-completer-function text state)
            (if (not state)
                (setpwent))  ;; new, go to start of database
            (let more ((pw (getpwent)))
              (if pw
                  (if (string-prefix? text (passwd:name pw))
                      (passwd:name pw)     ;; this name matches, return it
                      (more (getpwent)))   ;; doesn't match, look at next
                  (begin
                    ;; end of database, close it and return #f
                    (endpwent)
                    #f))))

 -- Function: apropos-completion-function text state
     A completion function offering completions for Guile functions and
     variables (all ‘define’s).  This is the default completion
     function.

 -- Function: filename-completion-function text state
     A completion function offering filename completions.  This is
     readline’s ‘rl_filename_completion_function’ (*note
     (readline)Completion Functions::).

 -- Function: make-completion-function string-list
     Return a completion function which offers completions from the
     possibilities in STRING-LIST.  Matching is case-sensitive.

7.9 Pretty Printing
===================

The module ‘(ice-9 pretty-print)’ provides the procedure ‘pretty-print’,
which provides nicely formatted output of Scheme objects.  This is
especially useful for deeply nested or complex data structures, such as
lists and vectors.

   The module is loaded by entering the following:

     (use-modules (ice-9 pretty-print))

   This makes the procedure ‘pretty-print’ available.  As an example how
‘pretty-print’ will format the output, see the following:

     (pretty-print '(define (foo) (lambda (x)
     (cond ((zero? x) #t) ((negative? x) -x) (else
     (if (= x 1) 2 (* x x x)))))))
     ⊣
     (define (foo)
       (lambda (x)
         (cond ((zero? x) #t)
               ((negative? x) -x)
               (else (if (= x 1) 2 (* x x x))))))

 -- Scheme Procedure: pretty-print obj [port] [keyword-options]
     Print the textual representation of the Scheme object OBJ to PORT.
     PORT defaults to the current output port, if not given.

     The further KEYWORD-OPTIONS are keywords and parameters as follows,

     #:display? FLAG
          If FLAG is true then print using ‘display’.  The default is
          ‘#f’ which means use ‘write’ style.  (*note Writing::)

     #:per-line-prefix STRING
          Print the given STRING as a prefix on each line.  The default
          is no prefix.

     #:width COLUMNS
          Print within the given COLUMNS.  The default is 79.

   Also exported by the ‘(ice-9 pretty-print)’ module is
‘truncated-print’, a procedure to print Scheme datums, truncating the
output to a certain number of characters.  This is useful when you need
to present an arbitrary datum to the user, but you only have one line in
which to do so.

     (define exp '(a b #(c d e) f . g))
     (truncated-print exp #:width 10) (newline)
     ⊣ (a b . #)
     (truncated-print exp #:width 15) (newline)
     ⊣ (a b # f . g)
     (truncated-print exp #:width 18) (newline)
     ⊣ (a b #(c ...) . #)
     (truncated-print exp #:width 20) (newline)
     ⊣ (a b #(c d e) f . g)
     (truncated-print "The quick brown fox" #:width 20) (newline)
     ⊣ "The quick brown..."
     (truncated-print (current-module) #:width 20) (newline)
     ⊣ #<directory (gui...>

   ‘truncated-print’ will not output a trailing newline.  If an
expression does not fit in the given width, it will be truncated –
possibly ellipsized(1), or in the worst case, displayed as #.

 -- Scheme Procedure: truncated-print obj [port] [keyword-options]
     Print OBJ, truncating the output, if necessary, to make it fit into
     WIDTH characters.  By default, OBJ will be printed using ‘write’,
     though that behavior can be overridden via the DISPLAY? keyword
     argument.

     The default behaviour is to print depth-first, meaning that the
     entire remaining width will be available to each sub-expression of
     OBJ – e.g., if OBJ is a vector, each member of OBJ.  One can
     attempt to “ration” the available width, trying to allocate it
     equally to each sub-expression, via the BREADTH-FIRST? keyword
     argument.

     The further KEYWORD-OPTIONS are keywords and parameters as follows,

     #:display? FLAG
          If FLAG is true then print using ‘display’.  The default is
          ‘#f’ which means use ‘write’ style.  (*note Writing::)

     #:width COLUMNS
          Print within the given COLUMNS.  The default is 79.

     #:breadth-first? FLAG
          If FLAG is true, then allocate the available width
          breadth-first among elements of a compound data structure
          (list, vector, pair, etc.).  The default is ‘#f’ which means
          that any element is allowed to consume all of the available
          width.

   ---------- Footnotes ----------

   (1) On Unicode-capable ports, the ellipsis is represented by
character ‘HORIZONTAL ELLIPSIS’ (U+2026), otherwise it is represented by
three dots.

7.10 Formatted Output
=====================

The ‘format’ function is a powerful way to print numbers, strings and
other objects together with literal text under the control of a format
string.  This function is available from

     (use-modules (ice-9 format))

   A format string is generally more compact and easier than using just
the standard procedures like ‘display’, ‘write’ and ‘newline’.
Parameters in the output string allow various output styles, and
parameters can be taken from the arguments for runtime flexibility.

   ‘format’ is similar to the Common Lisp procedure of the same name,
but it’s not identical and doesn’t have quite all the features found in
Common Lisp.

   C programmers will note the similarity between ‘format’ and ‘printf’,
though escape sequences are marked with ~ instead of %, and are more
powerful.


 -- Scheme Procedure: format dest fmt arg …
     Write output specified by the FMT string to DEST.  DEST can be an
     output port, ‘#t’ for ‘current-output-port’ (*note Default
     Ports::), or ‘#f’ to return the output as a string.

     FMT can contain literal text to be output, and ~ escapes.  Each
     escape has the form

          ~ [param [, param…] [:] [@] code

     code is a character determining the escape sequence.  The : and @
     characters are optional modifiers, one or both of which change the
     way various codes operate.  Optional parameters are accepted by
     some codes too.  Parameters have the following forms,

     [+/-]number
          An integer, with optional + or -.
     ’ (apostrophe)
          The following character in the format string, for instance ’z
          for z.
     v
          The next function argument as the parameter.  v stands for
          “variable”, a parameter can be calculated at runtime and
          included in the arguments.  Upper case V can be used too.
     #
          The number of arguments remaining.  (See ~* below for some
          usages.)

     Parameters are separated by commas (,).  A parameter can be left
     empty to keep its default value when supplying later parameters.


     The following escapes are available.  The code letters are not
     case-sensitive, upper and lower case are the same.

     ~a
     ~s
          Object output.  Parameters: MINWIDTH, PADINC, MINPAD, PADCHAR.

          ~a outputs an argument like ‘display’, ~s outputs an argument
          like ‘write’ (*note Writing::).

               (format #t "~a" "foo") ⊣ foo
               (format #t "~s" "foo") ⊣ "foo"

          ~:a and ~:s put objects that don’t have an external
          representation in quotes like a string.

               (format #t "~:a" car) ⊣ "#<primitive-procedure car>"

          If the output is less than MINWIDTH characters (default 0),
          it’s padded on the right with PADCHAR (default space).  ~@a
          and ~@s put the padding on the left instead.

               (format #f "~5a" 'abc)       ⇒ "abc  "
               (format #f "~5,,,'-@a" 'abc) ⇒ "--abc"

          MINPAD is a minimum for the padding then plus a multiple of
          PADINC.  Ie. the padding is MINPAD + N * PADINC, where N is
          the smallest integer making the total object plus padding
          greater than or equal to MINWIDTH.  The default MINPAD is 0
          and the default PADINC is 1 (imposing no minimum or multiple).

               (format #f "~5,1,4a" 'abc) ⇒ "abc    "

     ~c
          Character.  Parameter: CHARNUM.

          Output a character.  The default is to simply output, as per
          ‘write-char’ (*note Writing::).  ~@c prints in ‘write’ style.
          ~:c prints control characters (ASCII 0 to 31) in ^X form.

               (format #t "~c" #\z)        ⊣ z
               (format #t "~@c" #\z)       ⊣ #\z
               (format #t "~:c" #\newline) ⊣ ^J

          If the CHARNUM parameter is given then an argument is not
          taken but instead the character is ‘(integer->char CHARNUM)’
          (*note Characters::).  This can be used for instance to output
          characters given by their ASCII code.

               (format #t "~65c")  ⊣ A

     ~d
     ~x
     ~o
     ~b
          Integer.  Parameters: MINWIDTH, PADCHAR, COMMACHAR,
          COMMAWIDTH.

          Output an integer argument as a decimal, hexadecimal, octal or
          binary integer (respectively), in a locale-independent way.

               (format #t "~d" 123) ⊣ 123

          ~@d etc shows a + sign is shown on positive numbers.

               (format #t "~@b" 12) ⊣ +1100

          If the output is less than the MINWIDTH parameter (default no
          minimum), it’s padded on the left with the PADCHAR parameter
          (default space).

               (format #t "~5,'*d" 12)   ⊣ ***12
               (format #t "~5,'0d" 12)   ⊣ 00012
               (format #t "~3d"    1234) ⊣ 1234

          ~:d adds commas (or the COMMACHAR parameter) every three
          digits (or the COMMAWIDTH parameter many).  However, when your
          intent is to write numbers in a way that follows typographical
          conventions, using ~h is recommended.

               (format #t "~:d" 1234567)         ⊣ 1,234,567
               (format #t "~10,'*,'/,2:d" 12345) ⊣ ***1/23/45

          Hexadecimal ~x output is in lower case, but the ~( and ~) case
          conversion directives described below can be used to get upper
          case.

               (format #t "~x"       65261) ⊣ feed
               (format #t "~:@(~x~)" 65261) ⊣ FEED

     ~r
          Integer in words, roman numerals, or a specified radix.
          Parameters: RADIX, MINWIDTH, PADCHAR, COMMACHAR, COMMAWIDTH.

          With no parameters output is in words as a cardinal like
          “ten”, or ~:r prints an ordinal like “tenth”.

               (format #t "~r" 9)  ⊣ nine        ;; cardinal
               (format #t "~r" -9) ⊣ minus nine  ;; cardinal
               (format #t "~:r" 9) ⊣ ninth       ;; ordinal

          And also with no parameters, ~@r gives roman numerals and ~:@r
          gives old roman numerals.  In old roman numerals there’s no
          “subtraction”, so 9 is VIIII instead of IX. In both cases only
          positive numbers can be output.

               (format #t "~@r" 89)  ⊣ LXXXIX     ;; roman
               (format #t "~:@r" 89) ⊣ LXXXVIIII  ;; old roman

          When a parameter is given it means numeric output in the
          specified RADIX.  The modifiers and parameters following the
          radix are the same as described for ~d etc above.

               (format #f "~3r" 27)   ⇒ "1000"    ;; base 3
               (format #f "~3,5r" 26) ⇒ "  222"   ;; base 3 width 5

     ~f
          Fixed-point float.  Parameters: WIDTH, DECIMALS, SCALE,
          OVERFLOWCHAR, PADCHAR.

          Output a number or number string in fixed-point format, ie.
          with a decimal point.

               (format #t "~f" 5)      ⊣ 5.0
               (format #t "~f" "123")  ⊣ 123.0
               (format #t "~f" "1e-1") ⊣ 0.1

          ~@f prints a + sign on positive numbers (including zero).

               (format #t "~@f" 0) ⊣ +0.0

          If the output is less than WIDTH characters it’s padded on the
          left with PADCHAR (space by default).  If the output equals or
          exceeds WIDTH then there’s no padding.  The default for WIDTH
          is no padding.

               (format #f "~6f" -1.5)      ⇒ "  -1.5"
               (format #f "~6,,,,'*f" 23)  ⇒ "**23.0"
               (format #f "~6f" 1234567.0) ⇒ "1234567.0"

          DECIMALS is how many digits to print after the decimal point,
          with the value rounded or padded with zeros as necessary.
          (The default is to output as many decimals as required.)

               (format #t "~1,2f" 3.125) ⊣ 3.13
               (format #t "~1,2f" 1.5)   ⊣ 1.50

          SCALE is a power of 10 applied to the value, moving the
          decimal point that many places.  A positive SCALE increases
          the value shown, a negative decreases it.

               (format #t "~,,2f" 1234)  ⊣ 123400.0
               (format #t "~,,-2f" 1234) ⊣ 12.34

          If OVERFLOWCHAR and WIDTH are both given and if the output
          would exceed WIDTH, then that many OVERFLOWCHARs are printed
          instead of the value.

               (format #t "~6,,,'xf" 12345) ⊣ 12345.
               (format #t "~5,,,'xf" 12345) ⊣ xxxxx

     ~h
          Localized number(1).  Parameters: WIDTH, DECIMALS, PADCHAR.

          Like ~f, output an exact or floating point number, but do so
          according to the current locale, or according to the given
          locale object when the ‘:’ modifier is used (*note
          ‘number->locale-string’: Number Input and Output.).

               (format #t "~h" 12345.5678)  ; with "C" as the current locale
               ⊣ 12345.5678

               (format #t "~14,,'*:h" 12345.5678
                       (make-locale LC_ALL "en_US"))
               ⊣ ***12,345.5678

               (format #t "~,2:h" 12345.5678
                       (make-locale LC_NUMERIC "fr_FR"))
               ⊣ 12 345,56

     ~e
          Exponential float.  Parameters: WIDTH, MANTDIGITS, EXPDIGITS,
          INTDIGITS, OVERFLOWCHAR, PADCHAR, EXPCHAR.

          Output a number or number string in exponential notation.

               (format #t "~e" 5000.25) ⊣ 5.00025E+3
               (format #t "~e" "123.4") ⊣ 1.234E+2
               (format #t "~e" "1e4")   ⊣ 1.0E+4

          ~@e prints a + sign on positive numbers (including zero).
          (This is for the mantissa, a + or - sign is always shown on
          the exponent.)

               (format #t "~@e" 5000.0) ⊣ +5.0E+3

          If the output is less than WIDTH characters it’s padded on the
          left with PADCHAR (space by default).  The default for WIDTH
          is to output with no padding.

               (format #f "~10e" 1234.0)     ⇒ "  1.234E+3"
               (format #f "~10,,,,,'*e" 0.5) ⇒ "****5.0E-1"

          MANTDIGITS is the number of digits shown in the mantissa after
          the decimal point.  The value is rounded or trailing zeros are
          added as necessary.  The default MANTDIGITS is to show as much
          as needed by the value.

               (format #f "~,3e" 11111.0) ⇒ "1.111E+4"
               (format #f "~,8e" 123.0)   ⇒ "1.23000000E+2"

          EXPDIGITS is the minimum number of digits shown for the
          exponent, with leading zeros added if necessary.  The default
          for EXPDIGITS is to show only as many digits as required.  At
          least 1 digit is always shown.

               (format #f "~,,1e" 1.0e99) ⇒ "1.0E+99"
               (format #f "~,,6e" 1.0e99) ⇒ "1.0E+000099"

          INTDIGITS (default 1) is the number of digits to show before
          the decimal point in the mantissa.  INTDIGITS can be zero, in
          which case the integer part is a single 0, or it can be
          negative, in which case leading zeros are shown after the
          decimal point.

               (format #t "~,,,3e" 12345.0)  ⊣ 123.45E+2
               (format #t "~,,,0e" 12345.0)  ⊣ 0.12345E+5
               (format #t "~,,,-3e" 12345.0) ⊣ 0.00012345E+8

          If OVERFLOWCHAR is given then WIDTH is a hard limit.  If the
          output would exceed WIDTH then instead that many OVERFLOWCHARs
          are printed.

               (format #f "~6,,,,'xe" 100.0) ⇒ "1.0E+2"
               (format #f "~3,,,,'xe" 100.0) ⇒ "xxx"

          EXPCHAR is the exponent marker character (default E).

               (format #t "~,,,,,,'ee" 100.0) ⊣ 1.0e+2

     ~g
          General float.  Parameters: WIDTH, MANTDIGITS, EXPDIGITS,
          INTDIGITS, OVERFLOWCHAR, PADCHAR, EXPCHAR.

          Output a number or number string in either exponential format
          the same as ~e, or fixed-point format like ~f but aligned
          where the mantissa would have been and followed by padding
          where the exponent would have been.

          Fixed-point is used when the absolute value is 0.1 or more and
          it takes no more space than the mantissa in exponential
          format, ie. basically up to MANTDIGITS digits.

               (format #f "~12,4,2g" 999.0)    ⇒ "   999.0    "
               (format #f "~12,4,2g" "100000") ⇒ "  1.0000E+05"

          The parameters are interpreted as per ~e above.  When
          fixed-point is used, the DECIMALS parameter to ~f is
          established from MANTDIGITS, so as to give a total
          MANTDIGITS+1 figures.

     ~$
          Monetary style fixed-point float.  Parameters: DECIMALS,
          INTDIGITS, WIDTH, PADCHAR.

          Output a number or number string in fixed-point format, ie.
          with a decimal point.  DECIMALS is the number of decimal
          places to show, default 2.

               (format #t "~$" 5)       ⊣ 5.00
               (format #t "~4$" "2.25") ⊣ 2.2500
               (format #t "~4$" "1e-2") ⊣ 0.0100

          ~@$ prints a + sign on positive numbers (including zero).

               (format #t "~@$" 0) ⊣ +0.00

          INTDIGITS is a minimum number of digits to show in the integer
          part of the value (default 1).

               (format #t "~,3$" 9.5)   ⊣ 009.50
               (format #t "~,0$" 0.125) ⊣ .13

          If the output is less than WIDTH characters (default 0), it’s
          padded on the left with PADCHAR (default space).  ~:$ puts the
          padding after the sign.

               (format #f "~,,8$" -1.5)   ⇒ "   -1.50"
               (format #f "~,,8:$" -1.5)  ⇒ "-   1.50"
               (format #f "~,,8,'.:@$" 3) ⇒ "+...3.00"

          Note that floating point for dollar amounts is generally not a
          good idea, because a cent 0.01 cannot be represented exactly
          in the binary floating point Guile uses, which leads to slowly
          accumulating rounding errors.  Keeping values as cents (or
          fractions of a cent) in integers then printing with the scale
          option in ~f may be a better approach.

     ~i
          Complex fixed-point float.  Parameters: WIDTH, DECIMALS,
          SCALE, OVERFLOWCHAR, PADCHAR.

          Output the argument as a complex number, with both real and
          imaginary part shown (even if one or both are zero).

          The parameters and modifiers are the same as for fixed-point
          ~f described above.  The real and imaginary parts are both
          output with the same given parameters and modifiers, except
          that for the imaginary part the @ modifier is always enabled,
          so as to print a + sign between the real and imaginary parts.

               (format #t "~i" 1)  ⊣ 1.0+0.0i

     ~p
          Plural.  No parameters.

          Output nothing if the argument is 1, or ‘s’ for any other
          value.

               (format #t "enter name~p" 1) ⊣ enter name
               (format #t "enter name~p" 2) ⊣ enter names

          ~@p prints ‘y’ for 1 or ‘ies’ otherwise.

               (format #t "pupp~@p" 1) ⊣ puppy
               (format #t "pupp~@p" 2) ⊣ puppies

          ~:p re-uses the preceding argument instead of taking a new
          one, which can be convenient when printing some sort of count.

               (format #t "~d cat~:p" 9)   ⊣ 9 cats
               (format #t "~d pupp~:@p" 5) ⊣ 5 puppies

          ~p is designed for English plurals and there’s no attempt to
          support other languages.  ~[ conditionals (below) may be able
          to help.  When using ‘gettext’ to translate messages
          ‘ngettext’ is probably best though (*note
          Internationalization::).

     ~y
          Structured printing.  Parameters: WIDTH.

          ~y outputs an argument using ‘pretty-print’ (*note Pretty
          Printing::).  The result will be formatted to fit within WIDTH
          columns (79 by default), consuming multiple lines if
          necessary.

          ~@y outputs an argument using ‘truncated-print’ (*note Pretty
          Printing::).  The resulting code will be formatted to fit
          within WIDTH columns (79 by default), on a single line.  The
          output will be truncated if necessary.

          ~:@y is like ~@y, except the WIDTH parameter is interpreted to
          be the maximum column to which to output.  That is to say, if
          you are at column 10, and ~60:@y is seen, the datum will be
          truncated to 50 columns.

     ~?
     ~k
          Sub-format.  No parameters.

          Take a format string argument and a second argument which is a
          list of arguments for that string, and output the result.

               (format #t "~?" "~d ~d" '(1 2))    ⊣ 1 2

          ~@?  takes arguments for the sub-format directly rather than
          in a list.

               (format #t "~@? ~s" "~d ~d" 1 2 "foo") ⊣ 1 2 "foo"

          ~?  and ~k are the same, ~k is provided for T-Scheme
          compatibility.

     ~*
          Argument jumping.  Parameter: N.

          Move forward N arguments (default 1) in the argument list.
          ~:* moves backwards.  (N cannot be negative.)

               (format #f "~d ~2*~d" 1 2 3 4) ⇒ "1 4"
               (format #f "~d ~:*~d" 6)       ⇒ "6 6"

          ~@* moves to argument number N.  The first argument is number
          0 (and that’s the default for N).

               (format #f "~d~d again ~@*~d~d" 1 2) ⇒ "12 again 12"
               (format #f "~d~d~d ~1@*~d~d" 1 2 3)  ⇒ "123 23"

          A # move to the end followed by a : modifier move back can be
          used for an absolute position relative to the end of the
          argument list, a reverse of what the @ modifier does.

               (format #t "~#*~2:*~a" 'a 'b 'c 'd)   ⊣ c

          At the end of the format string the current argument position
          doesn’t matter, any further arguments are ignored.

     ~t
          Advance to a column position.  Parameters: COLNUM, COLINC,
          PADCHAR.

          Output PADCHAR (space by default) to move to the given COLNUM
          column.  The start of the line is column 0, the default for
          COLNUM is 1.

               (format #f "~tX")  ⇒ " X"
               (format #f "~3tX") ⇒ "   X"

          If the current column is already past COLNUM, then the move is
          to there plus a multiple of COLINC, ie. column COLNUM + N *
          COLINC for the smallest N which makes that value greater than
          or equal to the current column.  The default COLINC is 1
          (which means no further move).

               (format #f "abcd~2,5,'.tx") ⇒ "abcd...x"

          ~@t takes COLNUM as an offset from the current column.  COLNUM
          many pad characters are output, then further padding to make
          the current column a multiple of COLINC, if it isn’t already
          so.

               (format #f "a~3,5'*@tx") ⇒ "a****x"

          ~t is implemented using ‘port-column’ (*note Reading::), so it
          works even there has been other output before ‘format’.

     ~~
          Tilde character.  Parameter: N.

          Output a tilde character ~, or N many if a parameter is given.
          Normally ~ introduces an escape sequence, ~~ is the way to
          output a literal tilde.

     ~%
          Newline.  Parameter: N.

          Output a newline character, or N many if a parameter is given.
          A newline (or a few newlines) can of course be output just by
          including them in the format string.

     ~&
          Start a new line.  Parameter: N.

          Output a newline if not already at the start of a line.  With
          a parameter, output that many newlines, but with the first
          only if not already at the start of a line.  So for instance 3
          would be a newline if not already at the start of a line, and
          2 further newlines.

     ~_
          Space character.  Parameter: N.

          Output a space character, or N many if a parameter is given.

          With a variable parameter this is one way to insert runtime
          calculated padding (~t or the various field widths can do
          similar things).

               (format #f "~v_foo" 4) ⇒ "    foo"

     ~/
          Tab character.  Parameter: N.

          Output a tab character, or N many if a parameter is given.

     ~|
          Formfeed character.  Parameter: N.

          Output a formfeed character, or N many if a parameter is
          given.

     ~!
          Force output.  No parameters.

          At the end of output, call ‘force-output’ to flush any buffers
          on the destination (*note Writing::).  ~!  can occur anywhere
          in the format string, but the force is done at the end of
          output.

          When output is to a string (destination ‘#f’), ~!  does
          nothing.

     ~newline (ie. newline character)
          Continuation line.  No parameters.

          Skip this newline and any following whitespace in the format
          string, ie. don’t send it to the output.  This can be used to
          break up a long format string for readability, but not print
          the extra whitespace.

               (format #f "abc~
                           ~d def~
                           ~d" 1 2) ⇒ "abc1 def2"

          ~:newline skips the newline but leaves any further whitespace
          to be printed normally.

          ~@newline prints the newline then skips following whitespace.

     ~( ~)
          Case conversion.  No parameters.

          Between ~( and ~) the case of all output is changed.  The
          modifiers on ~( control the conversion.

               ~( — lower case.
               ~:@( — upper case.

          For example,

               (format #t "~(Hello~)")   ⊣ hello
               (format #t "~:@(Hello~)") ⊣ HELLO

          In the future it’s intended the modifiers : and @ alone will
          capitalize the first letters of words, as per Common Lisp
          ‘format’, but the current implementation of this is flawed and
          not recommended for use.

          Case conversions do not nest, currently.  This might change in
          the future, but if it does then it will be to Common Lisp
          style where the outermost conversion has priority, overriding
          inner ones (making those fairly pointless).

     ~{ ~}
          Iteration.  Parameter: MAXREPS (for ~{).

          The format between ~{ and ~} is iterated.  The modifiers to ~{
          determine how arguments are taken.  The default is a list
          argument with each iteration successively consuming elements
          from it.  This is a convenient way to output a whole list.

               (format #t "~{~d~}"     '(1 2 3))       ⊣ 123
               (format #t "~{~s=~d ~}" '("x" 1 "y" 2)) ⊣ "x"=1 "y"=2

          ~:{ takes a single argument which is a list of lists, each of
          those contained lists gives the arguments for the iterated
          format.

               (format #t "~:{~dx~d ~}" '((1 2) (3 4) (5 6)))
               ⊣ 1x2 3x4 5x6

          ~@{ takes arguments directly, with each iteration successively
          consuming arguments.

               (format #t "~@{~d~}"     1 2 3)       ⊣ 123
               (format #t "~@{~s=~d ~}" "x" 1 "y" 2) ⊣ "x"=1 "y"=2

          ~:@{ takes list arguments, one argument for each iteration,
          using that list for the format.

               (format #t "~:@{~dx~d ~}" '(1 2) '(3 4) '(5 6))
               ⊣ 1x2 3x4 5x6

          Iterating stops when there are no more arguments or when the
          MAXREPS parameter to ~{ is reached (default no maximum).

               (format #t "~2{~d~}" '(1 2 3 4)) ⊣ 12

          If the format between ~{ and ~} is empty, then a format string
          argument is taken (before iteration argument(s)) and used
          instead.  This allows a sub-format (like ~?  above) to be
          iterated.

               (format #t "~{~}" "~d" '(1 2 3)) ⊣ 123

          Iterations can be nested, an inner iteration operates in the
          same way as described, but of course on the arguments the
          outer iteration provides it.  This can be used to work into
          nested list structures.  For example in the following the
          inner ~{~d~}x is applied to ‘(1 2)’ then ‘(3 4 5)’ etc.

               (format #t "~{~{~d~}x~}" '((1 2) (3 4 5))) ⊣ 12x345x

          See also ~^ below for escaping from iteration.

     ~[ ~; ~]
          Conditional.  Parameter: SELECTOR.

          A conditional block is delimited by ~[ and ~], and ~;
          separates clauses within the block.  ~[ takes an integer
          argument and that number clause is used.  The first clause is
          number 0.

               (format #f "~[peach~;banana~;mango~]" 1)  ⇒ "banana"

          The SELECTOR parameter can be used for the clause number,
          instead of taking an argument.

               (format #f "~2[peach~;banana~;mango~]") ⇒ "mango"

          If the clause number is out of range then nothing is output.
          Or the last clause can be ~:; to use that for a number out of
          range.

               (format #f "~[banana~;mango~]"         99) ⇒ ""
               (format #f "~[banana~;mango~:;fruit~]" 99) ⇒ "fruit"

          ~:[ treats the argument as a flag, and expects two clauses.
          The first is used if the argument is ‘#f’ or the second
          otherwise.

               (format #f "~:[false~;not false~]" #f)   ⇒ "false"
               (format #f "~:[false~;not false~]" 'abc) ⇒ "not false"

               (let ((n 3))
                 (format #t "~d gnu~:[s are~; is~] here" n (= 1 n)))
               ⊣ 3 gnus are here

          ~@[ also treats the argument as a flag, and expects one
          clause.  If the argument is ‘#f’ then no output is produced
          and the argument is consumed, otherwise the clause is used and
          the argument is not consumed, it’s left for the clause.  This
          can be used for instance to suppress output if ‘#f’ means
          something not available.

               (format #f "~@[temperature=~d~]" 27) ⇒ "temperature=27"
               (format #f "~@[temperature=~d~]" #f) ⇒ ""

     ~^
          Escape.  Parameters: VAL1, VAL2, VAL3.

          Stop formatting if there are no more arguments.  This can be
          used for instance to have a format string adapt to a variable
          number of arguments.

               (format #t "~d~^ ~d" 1)   ⊣ 1
               (format #t "~d~^ ~d" 1 2) ⊣ 1 2

          Within a ~{ ~} iteration, ~^ stops the current iteration step
          if there are no more arguments to that step, but continuing
          with possible further steps and the rest of the format.  This
          can be used for instance to avoid a separator on the last
          iteration, or to adapt to variable length argument lists.

               (format #f "~{~d~^/~} go"    '(1 2 3))     ⇒ "1/2/3 go"
               (format #f "~:{ ~d~^~d~} go" '((1) (2 3))) ⇒ " 1 23 go"

          Within a ~?  sub-format, ~^ operates just on that sub-format.
          If it terminates the sub-format then the originating format
          will still continue.

               (format #t "~? items" "~d~^ ~d" '(1))   ⊣ 1 items
               (format #t "~? items" "~d~^ ~d" '(1 2)) ⊣ 1 2 items

          The parameters to ~^ (which are numbers) change the condition
          used to terminate.  For a single parameter, termination is
          when that value is zero (notice this makes plain ~^ equivalent
          to ~#^).  For two parameters, termination is when those two
          are equal.  For three parameters, termination is when VAL1 <=
          VAL2 and VAL2 <= VAL3.

     ~q
          Inquiry message.  Insert a copyright message into the output.

          ~:q inserts the format implementation version.


     It’s an error if there are not enough arguments for the escapes in
     the format string, but any excess arguments are ignored.

     Iterations ~{ ~} and conditionals ~[ ~; ~] can be nested, but must
     be properly nested, meaning the inner form must be entirely within
     the outer form.  So it’s not possible, for instance, to try to
     conditionalize the endpoint of an iteration.

          (format #t "~{ ~[ ... ~] ~}" ...)       ;; good
          (format #t "~{ ~[ ... ~} ... ~]" ...)   ;; bad

     The same applies to case conversions ~( ~), they must properly nest
     with respect to iterations and conditionals (though currently a
     case conversion cannot nest within another case conversion).

     When a sub-format (~?)  is used, that sub-format string must be
     self-contained.  It cannot for instance give a ~{ to begin an
     iteration form and have the ~} up in the originating format, or
     similar.


   Guile contains a ‘format’ procedure even when the module ‘(ice-9
format)’ is not loaded.  The default ‘format’ is ‘simple-format’ (*note
Writing::), it doesn’t support all escape sequences documented in this
section, and will signal an error if you try to use one of them.  The
reason for two versions is that the full ‘format’ is fairly large and
requires some time to load.  ‘simple-format’ is often adequate too.

   ---------- Footnotes ----------

   (1) The ~h format specifier first appeared in Guile version 2.0.6.

7.11 File Tree Walk
===================

The functions in this section traverse a tree of files and directories.
They come in two flavors: the first one is a high-level functional
interface, and the second one is similar to the C ‘ftw’ and ‘nftw’
routines (*note (libc)Working with Directory Trees::).

     (use-modules (ice-9 ftw))

 -- Scheme Procedure: file-system-tree file-name [enter? [stat]]
     Return a tree of the form ‘(FILE-NAME STAT CHILDREN ...)’ where
     STAT is the result of ‘(STAT FILE-NAME)’ and CHILDREN are similar
     structures for each file contained in FILE-NAME when it designates
     a directory.

     The optional ENTER? predicate is invoked as ‘(ENTER? NAME STAT)’
     and should return true to allow recursion into directory NAME; the
     default value is a procedure that always returns ‘#t’.  When a
     directory does not match ENTER?, it nonetheless appears in the
     resulting tree, only with zero children.

     The STAT argument is optional and defaults to ‘lstat’, as for
     ‘file-system-fold’ (see below.)

     The example below shows how to obtain a hierarchical listing of the
     files under the ‘module/language’ directory in the Guile source
     tree, discarding their ‘stat’ info:

          (use-modules (ice-9 match))

          (define remove-stat
            ;; Remove the `stat' object the `file-system-tree' provides
            ;; for each file in the tree.
            (match-lambda
              ((name stat)              ; flat file
               name)
              ((name stat children ...) ; directory
               (list name (map remove-stat children)))))

          (let ((dir (string-append (assq-ref %guile-build-info 'top_srcdir)
                                    "/module/language")))
            (remove-stat (file-system-tree dir)))

          ⇒
          ("language"
           (("value" ("spec.go" "spec.scm"))
            ("scheme"
             ("spec.go"
              "spec.scm"
              "compile-tree-il.scm"
              "decompile-tree-il.scm"
              "decompile-tree-il.go"
              "compile-tree-il.go"))
            ("tree-il"
             ("spec.go"
              "fix-letrec.go"
              "inline.go"
              "fix-letrec.scm"
              "compile-glil.go"
              "spec.scm"
              "optimize.scm"
              "primitives.scm"
              …))
            …))

   It is often desirable to process directories entries directly, rather
than building up a tree of entries in memory, like ‘file-system-tree’
does.  The following procedure, a "combinator", is designed to allow
directory entries to be processed directly as a directory tree is
traversed; in fact, ‘file-system-tree’ is implemented in terms of it.

 -- Scheme Procedure: file-system-fold enter? leaf down up skip error
          init file-name [stat]
     Traverse the directory at FILE-NAME, recursively, and return the
     result of the successive applications of the LEAF, DOWN, UP, and
     SKIP procedures as described below.

     Enter sub-directories only when ‘(ENTER? PATH STAT RESULT)’ returns
     true.  When a sub-directory is entered, call ‘(DOWN PATH STAT
     RESULT)’, where PATH is the path of the sub-directory and STAT the
     result of ‘(false-if-exception (STAT PATH))’; when it is left, call
     ‘(UP PATH STAT RESULT)’.

     For each file in a directory, call ‘(LEAF PATH STAT RESULT)’.

     When ENTER? returns ‘#f’, or when an unreadable directory is
     encountered, call ‘(SKIP PATH STAT RESULT)’.

     When FILE-NAME names a flat file, ‘(LEAF PATH STAT INIT)’ is
     returned.

     When an ‘opendir’ or STAT call fails, call ‘(ERROR PATH STAT ERRNO
     RESULT)’, with ERRNO being the operating system error number that
     was raised—e.g., ‘EACCES’—and STAT either ‘#f’ or the result of the
     STAT call for that entry, when available.

     The special ‘.’ and ‘..’ entries are not passed to these
     procedures.  The PATH argument to the procedures is a full file
     name—e.g., ‘"../foo/bar/gnu"’; if FILE-NAME is an absolute file
     name, then PATH is also an absolute file name.  Files and
     directories, as identified by their device/inode number pair, are
     traversed only once.

     The optional STAT argument defaults to ‘lstat’, which means that
     symbolic links are not followed; the ‘stat’ procedure can be used
     instead when symbolic links are to be followed (*note stat: File
     System.).

     The example below illustrates the use of ‘file-system-fold’:

          (define (total-file-size file-name)
            "Return the size in bytes of the files under FILE-NAME (similar
          to `du --apparent-size' with GNU Coreutils.)"

            (define (enter? name stat result)
              ;; Skip version control directories.
              (not (member (basename name) '(".git" ".svn" "CVS"))))
            (define (leaf name stat result)
              ;; Return RESULT plus the size of the file at NAME.
              (+ result (stat:size stat)))

            ;; Count zero bytes for directories.
            (define (down name stat result) result)
            (define (up name stat result) result)

            ;; Likewise for skipped directories.
            (define (skip name stat result) result)

            ;; Ignore unreadable files/directories but warn the user.
            (define (error name stat errno result)
              (format (current-error-port) "warning: ~a: ~a~%"
                      name (strerror errno))
              result)

            (file-system-fold enter? leaf down up skip error
                                     0  ; initial counter is zero bytes
                                     file-name))

          (total-file-size ".")
          ⇒ 8217554

          (total-file-size "/dev/null")
          ⇒ 0

   The alternative C-like functions are described below.

 -- Scheme Procedure: scandir name [select? [entry<?]]
     Return the list of the names of files contained in directory NAME
     that match predicate SELECT? (by default, all files).  The returned
     list of file names is sorted according to ENTRY<?, which defaults
     to ‘string-locale<?’ such that file names are sorted in the
     locale’s alphabetical order (*note Text Collation::).  Return ‘#f’
     when NAME is unreadable or is not a directory.

     This procedure is modeled after the C library function of the same
     name (*note (libc)Scanning Directory Content::).

 -- Scheme Procedure: ftw startname proc ['hash-size n]
     Walk the file system tree descending from STARTNAME, calling PROC
     for each file and directory.

     Hard links and symbolic links are followed.  A file or directory is
     reported to PROC only once, and skipped if seen again in another
     place.  One consequence of this is that ‘ftw’ is safe against
     circularly linked directory structures.

     Each PROC call is ‘(PROC filename statinfo flag)’ and it should
     return ‘#t’ to continue, or any other value to stop.

     FILENAME is the item visited, being STARTNAME plus a further path
     and the name of the item.  STATINFO is the return from ‘stat’
     (*note File System::) on FILENAME.  FLAG is one of the following
     symbols,

     ‘regular’
          FILENAME is a file, this includes special files like devices,
          named pipes, etc.

     ‘directory’
          FILENAME is a directory.

     ‘invalid-stat’
          An error occurred when calling ‘stat’, so nothing is known.
          STATINFO is ‘#f’ in this case.

     ‘directory-not-readable’
          FILENAME is a directory, but one which cannot be read and
          hence won’t be recursed into.

     ‘symlink’
          FILENAME is a dangling symbolic link.  Symbolic links are
          normally followed and their target reported, the link itself
          is reported if the target does not exist.

     The return value from ‘ftw’ is ‘#t’ if it ran to completion, or
     otherwise the non-‘#t’ value from PROC which caused the stop.

     Optional argument symbol ‘hash-size’ and an integer can be given to
     set the size of the hash table used to track items already visited.
     (*note Hash Table Reference::)

     In the current implementation, returning non-‘#t’ from PROC is the
     only valid way to terminate ‘ftw’.  PROC must not use ‘throw’ or
     similar to escape.

 -- Scheme Procedure: nftw startname proc ['chdir] ['depth] ['hash-size
          n] ['mount] ['physical]
     Walk the file system tree starting at STARTNAME, calling PROC for
     each file and directory.  ‘nftw’ has extra features over the basic
     ‘ftw’ described above.

     Like ‘ftw’, hard links and symbolic links are followed.  A file or
     directory is reported to PROC only once, and skipped if seen again
     in another place.  One consequence of this is that ‘nftw’ is safe
     against circular linked directory structures.

     Each PROC call is ‘(PROC filename statinfo flag base level)’ and it
     should return ‘#t’ to continue, or any other value to stop.

     FILENAME is the item visited, being STARTNAME plus a further path
     and the name of the item.  STATINFO is the return from ‘stat’ on
     FILENAME (*note File System::).  BASE is an integer offset into
     FILENAME which is where the basename for this item begins.  LEVEL
     is an integer giving the directory nesting level, starting from 0
     for the contents of STARTNAME (or that item itself if it’s a file).
     FLAG is one of the following symbols,

     ‘regular’
          FILENAME is a file, including special files like devices,
          named pipes, etc.

     ‘directory’
          FILENAME is a directory.

     ‘directory-processed’
          FILENAME is a directory, and its contents have all been
          visited.  This flag is given instead of ‘directory’ when the
          ‘depth’ option below is used.

     ‘invalid-stat’
          An error occurred when applying ‘stat’ to FILENAME, so nothing
          is known about it.  STATINFO is ‘#f’ in this case.

     ‘directory-not-readable’
          FILENAME is a directory, but one which cannot be read and
          hence won’t be recursed into.

     ‘stale-symlink’
          FILENAME is a dangling symbolic link.  Links are normally
          followed and their target reported, the link itself is
          reported if its target does not exist.

     ‘symlink’
          When the ‘physical’ option described below is used, this
          indicates FILENAME is a symbolic link whose target exists (and
          is not being followed).

     The following optional arguments can be given to modify the way
     ‘nftw’ works.  Each is passed as a symbol (and ‘hash-size’ takes a
     following integer value).

     ‘chdir’
          Change to the directory containing the item before calling
          PROC.  When ‘nftw’ returns the original current directory is
          restored.

          Under this option, generally the BASE parameter to each PROC
          call should be used to pick out the base part of the FILENAME.
          The FILENAME is still a path but with a changed directory it
          won’t be valid (unless the STARTNAME directory was absolute).

     ‘depth’
          Visit files “depth first”, meaning PROC is called for the
          contents of each directory before it’s called for the
          directory itself.  Normally a directory is reported first,
          then its contents.

          Under this option, the FLAG to PROC for a directory is
          ‘directory-processed’ instead of ‘directory’.

     ‘hash-size N’
          Set the size of the hash table used to track items already
          visited.  (*note Hash Table Reference::)

     ‘mount’
          Don’t cross a mount point, meaning only visit items on the
          same file system as STARTNAME (ie. the same ‘stat:dev’).

     ‘physical’
          Don’t follow symbolic links, instead report them to PROC as
          ‘symlink’.  Dangling links (those whose target doesn’t exist)
          are still reported as ‘stale-symlink’.

     The return value from ‘nftw’ is ‘#t’ if it ran to completion, or
     otherwise the non-‘#t’ value from PROC which caused the stop.

     In the current implementation, returning non-‘#t’ from PROC is the
     only valid way to terminate ‘ftw’.  PROC must not use ‘throw’ or
     similar to escape.

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

7.15 Expect
===========

The macros in this section are made available with:

     (use-modules (ice-9 expect))

   ‘expect’ is a macro for selecting actions based on the output from a
port.  The name comes from a tool of similar functionality by Don Libes.
Actions can be taken when a particular string is matched, when a timeout
occurs, or when end-of-file is seen on the port.  The ‘expect’ macro is
described below; ‘expect-strings’ is a front-end to ‘expect’ based on
regexec (see the regular expression documentation).

 -- Macro: expect-strings clause …
     By default, ‘expect-strings’ will read from the current input port.
     The first term in each clause consists of an expression evaluating
     to a string pattern (regular expression).  As characters are read
     one-by-one from the port, they are accumulated in a buffer string
     which is matched against each of the patterns.  When a pattern
     matches, the remaining expression(s) in the clause are evaluated
     and the value of the last is returned.  For example:

          (with-input-from-file "/etc/passwd"
            (lambda ()
              (expect-strings
                ("^nobody" (display "Got a nobody user.\n")
                           (display "That's no problem.\n"))
                ("^daemon" (display "Got a daemon user.\n")))))

     The regular expression is compiled with the ‘REG_NEWLINE’ flag, so
     that the ^ and $ anchors will match at any newline, not just at the
     start and end of the string.

     There are two other ways to write a clause:

     The expression(s) to evaluate can be omitted, in which case the
     result of the regular expression match (converted to strings, as
     obtained from regexec with match-pick set to "") will be returned
     if the pattern matches.

     The symbol ‘=>’ can be used to indicate that the expression is a
     procedure which will accept the result of a successful regular
     expression match.  E.g.,

          ("^daemon" => write)
          ("^d(aemon)" => (lambda args (for-each write args)))
          ("^da(em)on" => (lambda (all sub)
                            (write all) (newline)
                            (write sub) (newline)))

     The order of the substrings corresponds to the order in which the
     opening brackets occur.

     A number of variables can be used to control the behaviour of
     ‘expect’ (and ‘expect-strings’).  Most have default top-level
     bindings to the value ‘#f’, which produces the default behaviour.
     They can be redefined at the top level or locally bound in a form
     enclosing the expect expression.

     ‘expect-port’
          A port to read characters from, instead of the current input
          port.
     ‘expect-timeout’
          ‘expect’ will terminate after this number of seconds,
          returning ‘#f’ or the value returned by expect-timeout-proc.
     ‘expect-timeout-proc’
          A procedure called if timeout occurs.  The procedure takes a
          single argument: the accumulated string.
     ‘expect-eof-proc’
          A procedure called if end-of-file is detected on the input
          port.  The procedure takes a single argument: the accumulated
          string.
     ‘expect-char-proc’
          A procedure to be called every time a character is read from
          the port.  The procedure takes a single argument: the
          character which was read.
     ‘expect-strings-compile-flags’
          Flags to be used when compiling a regular expression, which
          are passed to ‘make-regexp’ *Note Regexp Functions::.  The
          default value is ‘regexp/newline’.
     ‘expect-strings-exec-flags’
          Flags to be used when executing a regular expression, which
          are passed to regexp-exec *Note Regexp Functions::.  The
          default value is ‘regexp/noteol’, which prevents ‘$’ from
          matching the end of the string while it is still accumulating,
          but still allows it to match after a line break or at the end
          of file.

     Here’s an example using all of the variables:

          (let ((expect-port (open-input-file "/etc/passwd"))
                (expect-timeout 1)
                (expect-timeout-proc
                  (lambda (s) (display "Times up!\n")))
                (expect-eof-proc
                  (lambda (s) (display "Reached the end of the file!\n")))
                (expect-char-proc display)
                (expect-strings-compile-flags (logior regexp/newline regexp/icase))
                (expect-strings-exec-flags 0))
             (expect-strings
               ("^nobody"  (display "Got a nobody user\n"))))

 -- Macro: expect clause …
     ‘expect’ is used in the same way as ‘expect-strings’, but tests are
     specified not as patterns, but as procedures.  The procedures are
     called in turn after each character is read from the port, with two
     arguments: the value of the accumulated string and a flag to
     indicate whether end-of-file has been reached.  The flag will
     usually be ‘#f’, but if end-of-file is reached, the procedures are
     called an additional time with the final accumulated string and
     ‘#t’.

     The test is successful if the procedure returns a non-false value.

     If the ‘=>’ syntax is used, then if the test succeeds it must
     return a list containing the arguments to be provided to the
     corresponding expression.

     In the following example, a string will only be matched at the
     beginning of the file:

          (let ((expect-port (open-input-file "/etc/passwd")))
            (expect
               ((lambda (s eof?) (string=? s "fnord!"))
                  (display "Got a nobody user!\n"))))

     The control variables described for ‘expect-strings’ also influence
     the behaviour of ‘expect’, with the exception of variables whose
     names begin with ‘expect-strings-’.

7.16 ‘sxml-match’: Pattern Matching of SXML
===========================================

The ‘(sxml match)’ module provides syntactic forms for pattern matching
of SXML trees, in a “by example” style reminiscent of the pattern
matching of the ‘syntax-rules’ and ‘syntax-case’ macro systems.  *Note
SXML::, for more information on SXML.

   The following example(1) provides a brief illustration, transforming
a music album catalog language into HTML.

     (define (album->html x)
       (sxml-match x
         [(album (@ (title ,t)) (catalog (num ,n) (fmt ,f)) ...)
          `(ul (li ,t)
               (li (b ,n) (i ,f)) ...)]))

   Three macros are provided: ‘sxml-match’, ‘sxml-match-let’, and
‘sxml-match-let*’.

   Compared to a standard s-expression pattern matcher (*note Pattern
Matching::), ‘sxml-match’ provides the following benefits:

   • matching of SXML elements does not depend on any degree of
     normalization of the SXML;
   • matching of SXML attributes (within an element) is under-ordered;
     the order of the attributes specified within the pattern need not
     match the ordering with the element being matched;
   • all attributes specified in the pattern must be present in the
     element being matched; in the spirit that XML is ’extensible’, the
     element being matched may include additional attributes not
     specified in the pattern.

   The present module is a descendant of WebIt!, and was inspired by an
s-expression pattern matcher developed by Erik Hilsdale, Dan Friedman,
and Kent Dybvig at Indiana University.

Syntax
------

‘sxml-match’ provides ‘case’-like form for pattern matching of XML
nodes.

 -- Scheme Syntax: sxml-match input-expression clause1 clause2 …
     Match INPUT-EXPRESSION, an SXML tree, according to the given
     CLAUSEs (one or more), each consisting of a pattern and one or more
     expressions to be evaluated if the pattern match succeeds.
     Optionally, each CLAUSE within ‘sxml-match’ may include a "guard
     expression".

   The pattern notation is based on that of Scheme’s ‘syntax-rules’ and
‘syntax-case’ macro systems.  The grammar for the ‘sxml-match’ syntax is
given below:

match-form ::= (sxml-match input-expression
                 clause+)

clause ::= [node-pattern action-expression+]
         | [node-pattern (guard expression*) action-expression+]

node-pattern ::= literal-pattern
               | pat-var-or-cata
               | element-pattern
               | list-pattern

literal-pattern ::= string
                  | character
                  | number
                  | #t
                  | #f

attr-list-pattern ::= (@ attribute-pattern*)
                    | (@ attribute-pattern* . pat-var-or-cata)

attribute-pattern ::= (tag-symbol attr-val-pattern)

attr-val-pattern ::= literal-pattern
                   | pat-var-or-cata
                   | (pat-var-or-cata default-value-expr)

element-pattern ::= (tag-symbol attr-list-pattern?)
                  | (tag-symbol attr-list-pattern? nodeset-pattern)
                  | (tag-symbol attr-list-pattern?
                                nodeset-pattern? . pat-var-or-cata)

list-pattern ::= (list nodeset-pattern)
               | (list nodeset-pattern? . pat-var-or-cata)
               | (list)

nodeset-pattern ::= node-pattern
                  | node-pattern ...
                  | node-pattern nodeset-pattern
                  | node-pattern ... nodeset-pattern

pat-var-or-cata ::= (unquote var-symbol)
                  | (unquote [var-symbol*])
                  | (unquote [cata-expression -> var-symbol*])

   Within a list or element body pattern, ellipses may appear only once,
but may be followed by zero or more node patterns.

   Guard expressions cannot refer to the return values of catamorphisms.

   Ellipses in the output expressions must appear only in an expression
context; ellipses are not allowed in a syntactic form.

   The sections below illustrate specific aspects of the ‘sxml-match’
pattern matcher.

Matching XML Elements
---------------------

The example below illustrates the pattern matching of an XML element:

     (sxml-match '(e (@ (i 1)) 3 4 5)
       [(e (@ (i ,d)) ,a ,b ,c) (list d a b c)]
       [,otherwise #f])

   Each clause in ‘sxml-match’ contains two parts: a pattern and one or
more expressions which are evaluated if the pattern is successfully
match.  The example above matches an element ‘e’ with an attribute ‘i’
and three children.

   Pattern variables are must be “unquoted” in the pattern.  The above
expression binds D to ‘1’, A to ‘3’, B to ‘4’, and C to ‘5’.

Ellipses in Patterns
--------------------

As in ‘syntax-rules’, ellipses may be used to specify a repeated
pattern.  Note that the pattern ‘item ...’ specifies zero-or-more
matches of the pattern ‘item’.

   The use of ellipses in a pattern is illustrated in the code fragment
below, where nested ellipses are used to match the children of repeated
instances of an ‘a’ element, within an element ‘d’.

     (define x '(d (a 1 2 3) (a 4 5) (a 6 7 8) (a 9 10)))

     (sxml-match x
       [(d (a ,b ...) ...)
        (list (list b ...) ...)])

   The above expression returns a value of ‘((1 2 3) (4 5) (6 7 8) (9
10))’.

Ellipses in Quasiquote’d Output
-------------------------------

Within the body of an ‘sxml-match’ form, a slightly extended version of
quasiquote is provided, which allows the use of ellipses.  This is
illustrated in the example below.

     (sxml-match '(e 3 4 5 6 7)
       [(e ,i ... 6 7) `("start" ,(list 'wrap i) ... "end")]
       [,otherwise #f])

   The general pattern is that ‘`(something ,i ...)’ is rewritten as
‘`(something ,@i)’.

Matching Nodesets
-----------------

A nodeset pattern is designated by a list in the pattern, beginning the
identifier list.  The example below illustrates matching a nodeset.

     (sxml-match '("i" "j" "k" "l" "m")
       [(list ,a ,b ,c ,d ,e)
        `((p ,a) (p ,b) (p ,c) (p ,d) (p ,e))])

   This example wraps each nodeset item in an HTML paragraph element.
This example can be rewritten and simplified through using ellipsis:

     (sxml-match '("i" "j" "k" "l" "m")
       [(list ,i ...)
        `((p ,i) ...)])

   This version will match nodesets of any length, and wrap each item in
the nodeset in an HTML paragraph element.

Matching the “Rest” of a Nodeset
--------------------------------

Matching the “rest” of a nodeset is achieved by using a ‘. rest)’
pattern at the end of an element or nodeset pattern.

   This is illustrated in the example below:

     (sxml-match '(e 3 (f 4 5 6) 7)
       [(e ,a (f . ,y) ,d)
        (list a y d)])

   The above expression returns ‘(3 (4 5 6) 7)’.

Matching the Unmatched Attributes
---------------------------------

Sometimes it is useful to bind a list of attributes present in the
element being matched, but which do not appear in the pattern.  This is
achieved by using a ‘. rest)’ pattern at the end of the attribute list
pattern.  This is illustrated in the example below:

     (sxml-match '(a (@ (z 1) (y 2) (x 3)) 4 5 6)
       [(a (@ (y ,www) . ,qqq) ,t ,u ,v)
        (list www qqq t u v)])

   The above expression matches the attribute ‘y’ and binds a list of
the remaining attributes to the variable QQQ.  The result of the above
expression is ‘(2 ((z 1) (x 3)) 4 5 6)’.

   This type of pattern also allows the binding of all attributes:

     (sxml-match '(a (@ (z 1) (y 2) (x 3)))
       [(a (@ . ,qqq))
        qqq])

Default Values in Attribute Patterns
------------------------------------

It is possible to specify a default value for an attribute which is used
if the attribute is not present in the element being matched.  This is
illustrated in the following example:

     (sxml-match '(e 3 4 5)
       [(e (@ (z (,d 1))) ,a ,b ,c) (list d a b c)])

   The value ‘1’ is used when the attribute ‘z’ is absent from the
element ‘e’.

Guards in Patterns
------------------

Guards may be added to a pattern clause via the ‘guard’ keyword.  A
guard expression may include zero or more expressions which are
evaluated only if the pattern is matched.  The body of the clause is
only evaluated if the guard expressions evaluate to ‘#t’.

   The use of guard expressions is illustrated below:

     (sxml-match '(a 2 3)
       ((a ,n) (guard (number? n)) n)
       ((a ,m ,n) (guard (number? m) (number? n)) (+ m n)))

Catamorphisms
-------------

The example below illustrates the use of explicit recursion within an
‘sxml-match’ form.  This example implements a simple calculator for the
basic arithmetic operations, which are represented by the XML elements
‘plus’, ‘minus’, ‘times’, and ‘div’.

     (define simple-eval
       (lambda (x)
         (sxml-match x
           [,i (guard (integer? i)) i]
           [(plus ,x ,y) (+ (simple-eval x) (simple-eval y))]
           [(times ,x ,y) (* (simple-eval x) (simple-eval y))]
           [(minus ,x ,y) (- (simple-eval x) (simple-eval y))]
           [(div ,x ,y) (/ (simple-eval x) (simple-eval y))]
           [,otherwise (error "simple-eval: invalid expression" x)])))

   Using the catamorphism feature of ‘sxml-match’, a more concise
version of ‘simple-eval’ can be written.  The pattern ‘,[x]’ recursively
invokes the pattern matcher on the value bound in this position.

     (define simple-eval
       (lambda (x)
         (sxml-match x
           [,i (guard (integer? i)) i]
           [(plus ,[x] ,[y]) (+ x y)]
           [(times ,[x] ,[y]) (* x y)]
           [(minus ,[x] ,[y]) (- x y)]
           [(div ,[x] ,[y]) (/ x y)]
           [,otherwise (error "simple-eval: invalid expression" x)])))

Named-Catamorphisms
-------------------

It is also possible to explicitly name the operator in the “cata”
position.  Where ‘,[id*]’ recurs to the top of the current ‘sxml-match’,
‘,[cata -> id*]’ recurs to ‘cata’.  ‘cata’ must evaluate to a procedure
which takes one argument, and returns as many values as there are
identifiers following ‘->’.

   Named catamorphism patterns allow processing to be split into
multiple, mutually recursive procedures.  This is illustrated in the
example below: a transformation that formats a “TV Guide” into HTML.

     (define (tv-guide->html g)
       (define (cast-list cl)
         (sxml-match cl
           [(CastList (CastMember (Character (Name ,ch)) (Actor (Name ,a))) ...)
            `(div (ul (li ,ch ": " ,a) ...))]))
       (define (prog p)
         (sxml-match p
           [(Program (Start ,start-time) (Duration ,dur) (Series ,series-title)
                     (Description ,desc ...))
            `(div (p ,start-time
                     (br) ,series-title
                     (br) ,desc ...))]
           [(Program (Start ,start-time) (Duration ,dur) (Series ,series-title)
                     (Description ,desc ...)
                     ,[cast-list -> cl])
            `(div (p ,start-time
                     (br) ,series-title
                     (br) ,desc ...)
                  ,cl)]))
       (sxml-match g
         [(TVGuide (@ (start ,start-date)
                      (end ,end-date))
                   (Channel (Name ,nm) ,[prog -> p] ...) ...)
          `(html (head (title "TV Guide"))
                 (body (h1 "TV Guide")
                       (div (h2 ,nm) ,p ...) ...))]))

‘sxml-match-let’ and ‘sxml-match-let*’
--------------------------------------

 -- Scheme Syntax: sxml-match-let ((pat expr) ...) expression0
          expression ...
 -- Scheme Syntax: sxml-match-let* ((pat expr) ...) expression0
          expression ...
     These forms generalize the ‘let’ and ‘let*’ forms of Scheme to
     allow an XML pattern in the binding position, rather than a simple
     variable.

   For example, the expression below:

     (sxml-match-let ([(a ,i ,j) '(a 1 2)])
       (+ i j))

   binds the variables I and J to ‘1’ and ‘2’ in the XML value given.

   ---------- Footnotes ----------

   (1) This example is taken from a paper by Krishnamurthi et al.  Their
paper was the first to show the usefulness of the ‘syntax-rules’ style
of pattern matching for transformation of XML, though the language
described, XT3D, is an XML language.

7.17 The Scheme shell (scsh)
============================

An incomplete port of the Scheme shell (scsh) was once available for
Guile as a separate package.  However this code has bitrotten somewhat.
The pieces are available in Guile’s legacy CVS repository, which may be
browsed at
<http://cvs.savannah.gnu.org/viewvc/guile/guile-scsh/?root=guile>.

   For information about scsh see <http://www.scsh.net/>.

   This bitrotting is a bit of a shame, as there is a good deal of
well-written Scheme code in scsh.  Adopting this code and porting it to
current Guile should be an educational experience, in addition to
providing something of value to Guile folks.

7.18 Curried Definitions
========================

The macros in this section are provided by
     (use-modules (ice-9 curried-definitions))
and replace those provided by default.

   Prior to Guile 2.0, Guile provided a type of definition known
colloquially as a “curried definition”.  The idea is to extend the
syntax of ‘define’ so that you can conveniently define procedures that
return procedures, up to any desired depth.

   For example,
     (define ((foo x) y)
       (list x y))
   is a convenience form of
     (define foo
       (lambda (x)
         (lambda (y)
           (list x y))))

 -- Scheme Syntax: define (… (name args …) …) body …
 -- Scheme Syntax: define* (… (name args …) …) body …
 -- Scheme Syntax: define-public (… (name args …) …) body …

     Create a top level variable NAME bound to the procedure with
     parameter list ARGS.  If NAME is itself a formal parameter list,
     then a higher order procedure is created using that
     formal-parameter list, and returning a procedure that has parameter
     list ARGS.  This nesting may occur to arbitrary depth.

     ‘define*’ is similar but the formal parameter lists take additional
     options as described in *note lambda* and define*::.  For example,
          (define* ((foo #:keys (bar 'baz) (quux 'zot)) frotz #:rest rest)
            (list bar quux frotz rest))

          ((foo #:quux 'foo) 1 2 3 4 5)
          ⇒ (baz foo 1 (2 3 4 5))

     ‘define-public’ is similar to ‘define’ but it also adds NAME to the
     list of exported bindings of the current module.

7.19 Statprof
=============

‘(statprof)’ is a fairly simple statistical profiler for Guile.

   A simple use of statprof would look like this:

     (statprof-reset 0 50000 #t)
     (statprof-start)
     (do-something)
     (statprof-stop)
     (statprof-display)

   This would reset statprof, clearing all accumulated statistics, then
start profiling, run some code, stop profiling, and finally display a
gprof flat-style table of statistics which will look something like
this:

       %   cumulative      self              self    total
      time    seconds   seconds    calls  ms/call  ms/call  name
      35.29      0.23      0.23     2002     0.11     0.11  -
      23.53      0.15      0.15     2001     0.08     0.08  positive?
      23.53      0.15      0.15     2000     0.08     0.08  +
      11.76      0.23      0.08     2000     0.04     0.11  do-nothing
       5.88      0.64      0.04     2001     0.02     0.32  loop
       0.00      0.15      0.00        1     0.00   150.59  do-something
      ...

   All of the numerical data with the exception of the calls column is
statistically approximate.  In the following column descriptions, and in
all of statprof, "time" refers to execution time (both user and system),
not wall clock time.

% time
     The percent of the time spent inside the procedure itself (not
     counting children).

cumulative seconds
     The total number of seconds spent in the procedure, including
     children.

self seconds
     The total number of seconds spent in the procedure itself (not
     counting children).

calls
     The total number of times the procedure was called.

self ms/call
     The average time taken by the procedure itself on each call, in ms.

total ms/call
     The average time taken by each call to the procedure, including
     time spent in child functions.

name
     The name of the procedure.

   The profiler uses ‘eq?’ and the procedure object itself to identify
the procedures, so it won’t confuse different procedures with the same
name.  They will show up as two different rows in the output.

   Right now the profiler is quite simplistic.  I cannot provide
call-graphs or other higher level information.  What you see in the
table is pretty much all there is.  Patches are welcome :-)

7.20 Implementation notes
=========================

The profiler works by setting the unix profiling signal ‘ITIMER_PROF’ to
go off after the interval you define in the call to ‘statprof-reset’.
When the signal fires, a sampling routine is run which looks at the
current procedure that’s executing, and then crawls up the stack, and
for each procedure encountered, increments that procedure’s sample
count.  Note that if a procedure is encountered multiple times on a
given stack, it is only counted once.  After the sampling is complete,
the profiler resets profiling timer to fire again after the appropriate
interval.

   Meanwhile, the profiler keeps track, via ‘get-internal-run-time’, how
much CPU time (system and user – which is also what ‘ITIMER_PROF’
tracks), has elapsed while code has been executing within a
statprof-start/stop block.

   The profiler also tries to avoid counting or timing its own code as
much as possible.

7.21 Usage
==========

 -- Function: statprof-active?
     Returns ‘#t’ if ‘statprof-start’ has been called more times than
     ‘statprof-stop’, ‘#f’ otherwise.

 -- Function: statprof-start
     Start the profiler.‘’

 -- Function: statprof-stop
     Stop the profiler.‘’

 -- Function: statprof-reset sample-seconds sample-microseconds
          count-calls? [full-stacks?]
     Reset the statprof sampler interval to SAMPLE-SECONDS and
     SAMPLE-MICROSECONDS.  If COUNT-CALLS? is true, arrange to
     instrument procedure calls as well as collecting statistical
     profiling data.  If FULL-STACKS? is true, collect all sampled
     stacks into a list for later analysis.

     Enables traps and debugging as necessary.

 -- Function: statprof-accumulated-time
     Returns the time accumulated during the last statprof run.‘’

 -- Function: statprof-sample-count
     Returns the number of samples taken during the last statprof run.‘’

 -- Function: statprof-fold-call-data proc init
     Fold PROC over the call-data accumulated by statprof.  Cannot be
     called while statprof is active.  PROC should take two arguments,
     ‘(CALL-DATA PRIOR-RESULT)’.

     Note that a given proc-name may appear multiple times, but if it
     does, it represents different functions with the same name.

 -- Function: statprof-proc-call-data proc
     Returns the call-data associated with PROC, or ‘#f’ if none is
     available.

 -- Function: statprof-call-data-name cd

 -- Function: statprof-call-data-calls cd

 -- Function: statprof-call-data-cum-samples cd

 -- Function: statprof-call-data-self-samples cd

 -- Function: statprof-call-data->stats call-data
     Returns an object of type ‘statprof-stats’.

 -- Function: statprof-stats-proc-name stats

 -- Function: statprof-stats-%-time-in-proc stats

 -- Function: statprof-stats-cum-secs-in-proc stats

 -- Function: statprof-stats-self-secs-in-proc stats

 -- Function: statprof-stats-calls stats

 -- Function: statprof-stats-self-secs-per-call stats

 -- Function: statprof-stats-cum-secs-per-call stats

 -- Function: statprof-display . _
     Displays a gprof-like summary of the statistics collected.  Unless
     an optional PORT argument is passed, uses the current output port.

 -- Function: statprof-display-anomolies
     A sanity check that attempts to detect anomolies in statprof’s
     statistics.‘’

 -- Function: statprof-fetch-stacks
     Returns a list of stacks, as they were captured since the last call
     to ‘statprof-reset’.

     Note that stacks are only collected if the FULL-STACKS? argument to
     ‘statprof-reset’ is true.

 -- Function: statprof-fetch-call-tree
     Return a call tree for the previous statprof run.

     The return value is a list of nodes, each of which is of the type:
     @@code
      node ::= (@@var@{proc@} @@var@{count@} . @@var@{nodes@})
     @@end code

 -- Function: statprof thunk [#:loop] [#:hz] [#:count-calls?]
          [#:full-stacks?]
     Profiles the execution of THUNK.

     The stack will be sampled HZ times per second, and the thunk itself
     will be called LOOP times.

     If COUNT-CALLS? is true, all procedure calls will be recorded.
     This operation is somewhat expensive.

     If FULL-STACKS? is true, at each sample, statprof will store away
     the whole call tree, for later analysis.  Use
     ‘statprof-fetch-stacks’ or ‘statprof-fetch-call-tree’ to retrieve
     the last-stored stacks.

 -- Special Form: with-statprof args
     Profiles the expressions in its body.

     Keyword arguments:

     ‘#:loop’
          Execute the body LOOP number of times, or ‘#f’ for no looping

          default: ‘#f’

     ‘#:hz’
          Sampling rate

          default: ‘20’

     ‘#:count-calls?’
          Whether to instrument each function call (expensive)

          default: ‘#f’

     ‘#:full-stacks?’
          Whether to collect away all sampled stacks into a list

          default: ‘#f’

 -- Function: gcprof thunk [#:loop] [#:full-stacks?]
     Do an allocation profile of the execution of THUNK.

     The stack will be sampled soon after every garbage collection,
     yielding an approximate idea of what is causing allocation in your
     program.

     Since GC does not occur very frequently, you may need to use the
     LOOP parameter, to cause THUNK to be called LOOP times.

     If FULL-STACKS? is true, at each sample, statprof will store away
     the whole call tree, for later analysis.  Use
     ‘statprof-fetch-stacks’ or ‘statprof-fetch-call-tree’ to retrieve
     the last-stored stacks.

7.22 SXML
=========

SXML is a native representation of XML in terms of standard Scheme data
types: lists, symbols, and strings.  For example, the simple XML
fragment:

     <parrot type="African Grey"><name>Alfie</name></parrot>

   may be represented with the following SXML:

     (parrot (@ (type "African Grey)) (name "Alfie"))

   SXML is very general, and is capable of representing all of XML.
Formally, this means that SXML is a conforming implementation of the
http://www.w3.org/TR/xml-infoset/ (XML Information Set) standard.

   Guile includes several facilities for working with XML and SXML:
parsers, serializers, and transformers.

7.22.1 SXML Overview
--------------------

(This section needs to be written; volunteers welcome.)

7.22.2 Reading and Writing XML
------------------------------

The ‘(sxml simple)’ module presents a basic interface for parsing XML
from a port into the Scheme SXML format, and for serializing it back to
text.

     (use-modules (sxml simple))

 -- Scheme Procedure: xml->sxml [string-or-port] [#:namespaces='()]
          [#:declare-namespaces?=#t] [#:trim-whitespace?=#f]
          [#:entities='()] [#:default-entity-handler=#f]
          [#:doctype-handler=#f]
     Use SSAX to parse an XML document into SXML. Takes one optional
     argument, STRING-OR-PORT, which defaults to the current input port.
     Returns the resulting SXML document.  If STRING-OR-PORT is a port,
     it will be left pointing at the next available character in the
     port.

   As is normal in SXML, XML elements parse as tagged lists.
Attributes, if any, are placed after the tag, within an ‘@’ element.
The root of the resulting XML will be contained in a special tag,
‘*TOP*’.  This tag will contain the root element of the XML, but also
any prior processing instructions.

     (xml->sxml "<foo/>")
     ⇒ (*TOP* (foo))
     (xml->sxml "<foo>text</foo>")
     ⇒ (*TOP* (foo "text"))
     (xml->sxml "<foo kind=\"bar\">text</foo>")
     ⇒ (*TOP* (foo (@ (kind "bar")) "text"))
     (xml->sxml "<?xml version=\"1.0\"?><foo/>")
     ⇒ (*TOP* (*PI* xml "version=\"1.0\"") (foo))

   All namespaces in the XML document must be declared, via ‘xmlns’
attributes.  SXML elements built from non-default namespaces will have
their tags prefixed with their URI. Users can specify custom prefixes
for certain namespaces with the ‘#:namespaces’ keyword argument to
‘xml->sxml’.

     (xml->sxml "<foo xmlns=\"http://example.org/ns1\">text</foo>")
     ⇒ (*TOP* (http://example.org/ns1:foo "text"))
     (xml->sxml "<foo xmlns=\"http://example.org/ns1\">text</foo>"
                #:namespaces '((ns1 . "http://example.org/ns1")))
     ⇒ (*TOP* (ns1:foo "text"))
     (xml->sxml "<foo xmlns:bar=\"http://example.org/ns2\"><bar:baz/></foo>"
                #:namespaces '((ns2 . "http://example.org/ns2")))
     ⇒ (*TOP* (foo (ns2:baz)))

   By default, namespaces passed to ‘xml->sxml’ are treated as if they
were declared on the root element.  Passing a false
‘#:declare-namespaces?’ argument will disable this behavior, requiring
in-document declarations of namespaces before use..

     (xml->sxml "<foo><ns2:baz/></foo>"
                #:namespaces '((ns2 . "http://example.org/ns2")))
     ⇒ (*TOP* (foo (ns2:baz)))
     (xml->sxml "<foo><ns2:baz/></foo>"
                #:namespaces '((ns2 . "http://example.org/ns2"))
                #:declare-namespaces? #f)
     ⇒ error: undeclared namespace: `bar'

   By default, all whitespace in XML is significant.  Passing the
‘#:trim-whitespace?’ keyword argument to ‘xml->sxml’ will trim
whitespace in front, behind and between elements, treating it as
“unsignificant”.  Whitespace in text fragments is left alone.

     (xml->sxml "<foo>\n<bar> Alfie the parrot! </bar>\n</foo>")
     ⇒ (*TOP* (foo "\n" (bar " Alfie the parrot! ") "\n"))
     (xml->sxml "<foo>\n<bar> Alfie the parrot! </bar>\n</foo>"
                #:trim-whitespace? #t)
     ⇒ (*TOP* (foo (bar " Alfie the parrot! ")))

   Parsed entities may be declared with the ‘#:entities’ keyword
argument, or handled with the ‘#:default-entity-handler’.  By default,
only the standard ‘&lt;’, ‘&gt;’, ‘&amp;’, ‘&apos;’ and ‘&quot;’
entities are defined, as well as the ‘&#N;’ and ‘&#xN;’ (decimal and
hexadecimal) numeric character entities.

     (xml->sxml "<foo>&amp;</foo>")
     ⇒ (*TOP* (foo "&"))
     (xml->sxml "<foo>&nbsp;</foo>")
     ⇒ error: undefined entity: nbsp
     (xml->sxml "<foo>&#xA0;</foo>")
     ⇒ (*TOP* (foo "\xa0"))
     (xml->sxml "<foo>&nbsp;</foo>"
                #:entities '((nbsp . "\xa0")))
     ⇒ (*TOP* (foo "\xa0"))
     (xml->sxml "<foo>&nbsp; &foo;</foo>"
                #:default-entity-handler
                (lambda (port name)
                  (case name
                    ((nbsp) "\xa0")
                    (else
                     (format (current-warning-port)
                             "~a:~a:~a: undefined entitity: ~a\n"
                             (or (port-filename port) "<unknown file>")
                             (port-line port) (port-column port)
                             name)
                     (symbol->string name)))))
     ⊣ <unknown file>:0:17: undefined entitity: foo
     ⇒ (*TOP* (foo "\xa0 foo"))

   By default, ‘xml->sxml’ skips over the ‘<!DOCTYPE>’ declaration, if
any.  This behavior can be overridden with the ‘#:doctype-handler’
argument, which should be a procedure of three arguments: the "docname"
(a symbol), "systemid" (a string), and the internal doctype subset (as a
string or ‘#f’ if not present).

   The handler should return keyword arguments as multiple values, as if
it were calling its continuation with keyword arguments.  The
continuation accepts the ‘#:entities’ and ‘#:namespaces’ keyword
arguments, in the same format that ‘xml->sxml’ itself takes.  These
entities and namespaces will be prepended to those given to the
‘xml->sxml’ invocation.

     (define (handle-foo docname systemid internal-subset)
       (case docname
         ((foo)
          (values #:entities '((greets . "<i>Hello, world!</i>"))))
         (else
          (values))))

     (xml->sxml "<!DOCTYPE foo><p>&greets;</p>"
                #:doctype-handler handle-foo)
     ⇒ (*TOP* (p (i "Hello, world!")))

   If the document has no doctype declaration, the DOCTYPE-HANDLER is
invoked with ‘#f’ for the three arguments.

   In the future, the continuation may accept other keyword arguments,
for example to validate the parsed SXML against the doctype.

 -- Scheme Procedure: sxml->xml tree [port]
     Serialize the SXML tree TREE as XML. The output will be written to
     the current output port, unless the optional argument PORT is
     present.

 -- Scheme Procedure: sxml->string sxml
     Detag an sxml tree SXML into a string.  Does not perform any
     formatting.

7.22.3 SSAX: A Functional XML Parsing Toolkit
---------------------------------------------

Guile’s XML parser is based on Oleg Kiselyov’s powerful XML parsing
toolkit, SSAX.

7.22.3.1 History
................

Back in the 1990s, when the world was young again and XML was the
solution to all of its problems, there were basically two kinds of XML
parsers out there: DOM parsers and SAX parsers.

   A DOM parser reads through an entire XML document, building up a tree
of “DOM objects” representing the document structure.  They are very
easy to use, but sometimes you don’t actually want all of the
information in a document; building an object tree is not necessary if
all you want to do is to count word frequencies in a document, for
example.

   SAX parsers were created to give the programmer more control on the
parsing process.  A programmer gives the SAX parser a number of
“callbacks”: functions that will be called on various features of the
XML stream as they are encountered.  SAX parsers are more efficient, but
much harder to user, as users typically have to manually maintain a
stack of open elements.

   Kiselyov realized that the SAX programming model could be made much
simpler if the callbacks were formulated not as a linear fold across the
features of the XML stream, but as a _tree fold_ over the structure
implicit in the XML. In this way, the user has a very convenient,
functional-style interface that can still generate optimal parsers.

   The ‘xml->sxml’ interface from the ‘(sxml simple)’ module is a
DOM-style parser built using SSAX, though it returns SXML instead of DOM
objects.

7.22.3.2 Implementation
.......................

‘(sxml ssax)’ is a package of low-to-high level lexing and parsing
procedures that can be combined to yield a SAX, a DOM, a validating
parser, or a parser intended for a particular document type.  The
procedures in the package can be used separately to tokenize or parse
various pieces of XML documents.  The package supports XML Namespaces,
internal and external parsed entities, user-controlled handling of
whitespace, and validation.  This module therefore is intended to be a
framework, a set of “Lego blocks” you can use to build a parser
following any discipline and performing validation to any degree.  As an
example of the parser construction, this file includes a semi-validating
SXML parser.

   SSAX has a “sequential” feel of SAX yet a “functional style” of DOM.
Like a SAX parser, the framework scans the document only once and
permits incremental processing.  An application that handles document
elements in order can run as efficiently as possible.  _Unlike_ a SAX
parser, the framework does not require an application register stateful
callbacks and surrender control to the parser.  Rather, it is the
application that can drive the framework – calling its functions to get
the current lexical or syntax element.  These functions do not maintain
or mutate any state save the input port.  Therefore, the framework
permits parsing of XML in a pure functional style, with the input port
being a monad (or a linear, read-once parameter).

   Besides the PORT, there is another monad – SEED.  Most of the middle-
and high-level parsers are single-threaded through the SEED.  The
functions of this framework do not process or affect the SEED in any
way: they simply pass it around as an instance of an opaque datatype.
User functions, on the other hand, can use the seed to maintain user’s
state, to accumulate parsing results, etc.  A user can freely mix his
own functions with those of the framework.  On the other hand, the user
may wish to instantiate a high-level parser: ‘SSAX:make-elem-parser’ or
‘SSAX:make-parser’.  In the latter case, the user must provide functions
of specific signatures, which are called at predictable moments during
the parsing: to handle character data, element data, or processing
instructions (PI). The functions are always given the SEED, among other
parameters, and must return the new SEED.

   From a functional point of view, XML parsing is a combined
pre-post-order traversal of a “tree” that is the XML document itself.
This down-and-up traversal tells the user about an element when its
start tag is encountered.  The user is notified about the element once
more, after all element’s children have been handled.  The process of
XML parsing therefore is a fold over the raw XML document.  Unlike a
fold over trees defined in [1], the parser is necessarily
single-threaded – obviously as elements in a text XML document are laid
down sequentially.  The parser therefore is a tree fold that has been
transformed to accept an accumulating parameter [1,2].

   Formally, the denotational semantics of the parser can be expressed
as

      parser:: (Start-tag -> Seed -> Seed) ->
     	   (Start-tag -> Seed -> Seed -> Seed) ->
     	   (Char-Data -> Seed -> Seed) ->
     	   XML-text-fragment -> Seed -> Seed
      parser fdown fup fchar "<elem attrs> content </elem>" seed
       = fup "<elem attrs>" seed
     	(parser fdown fup fchar "content" (fdown "<elem attrs>" seed))

      parser fdown fup fchar "char-data content" seed
       = parser fdown fup fchar "content" (fchar "char-data" seed)

      parser fdown fup fchar "elem-content content" seed
       = parser fdown fup fchar "content" (
     	parser fdown fup fchar "elem-content" seed)

   Compare the last two equations with the left fold

      fold-left kons elem:list seed = fold-left kons list (kons elem seed)

   The real parser created by ‘SSAX:make-parser’ is slightly more
complicated, to account for processing instructions, entity references,
namespaces, processing of document type declaration, etc.

   The XML standard document referred to in this module is
<http://www.w3.org/TR/1998/REC-xml-19980210.html>

   The present file also defines a procedure that parses the text of an
XML document or of a separate element into SXML, an S-expression-based
model of an XML Information Set.  SXML is also an Abstract Syntax Tree
of an XML document.  SXML is similar but not identical to DOM; SXML is
particularly suitable for Scheme-based XML/HTML authoring, SXPath
queries, and tree transformations.  See SXML.html for more details.
SXML is a term implementation of evaluation of the XML document [3].
The other implementation is context-passing.

   The present frameworks fully supports the XML Namespaces
Recommendation: <http://www.w3.org/TR/REC-xml-names/>.

   Other links:

[1]
     Jeremy Gibbons, Geraint Jones, "The Under-appreciated Unfold,"
     Proc.  ICFP’98, 1998, pp.  273-279.

[2]
     Richard S. Bird, The promotion and accumulation strategies in
     transformational programming, ACM Trans.  Progr.  Lang.  Systems,
     6(4):487-504, October 1984.

[3]
     Ralf Hinze, "Deriving Backtracking Monad Transformers," Functional
     Pearl.  Proc ICFP’00, pp.  186-197.

7.22.3.3 Usage
..............

 -- Scheme Procedure: current-ssax-error-port

 -- Scheme Procedure: with-ssax-error-to-port port thunk

 -- Scheme Procedure: xml-token? _
      -- Scheme Procedure: pair? x
          Return `#t' if X is a pair; otherwise return `#f'.



 -- Scheme Syntax: xml-token-kind token

 -- Scheme Syntax: xml-token-head token

 -- Scheme Procedure: make-empty-attlist

 -- Scheme Procedure: attlist-add attlist name-value

 -- Scheme Procedure: attlist-null? x
     Return ‘#t’ if X is the empty list, else ‘#f’.

 -- Scheme Procedure: attlist-remove-top attlist

 -- Scheme Procedure: attlist->alist attlist

 -- Scheme Procedure: attlist-fold kons knil lis1

 -- Scheme Procedure: define-parsed-entity! entity str
     Define a new parsed entity.  ENTITY should be a symbol.

     Instances of &ENTITY; in XML text will be replaced with the string
     STR, which will then be parsed.

 -- Scheme Procedure: reset-parsed-entity-definitions!
     Restore the set of parsed entity definitions to its initial state.

 -- Scheme Procedure: ssax:uri-string->symbol uri-str

 -- Scheme Procedure: ssax:skip-internal-dtd port

 -- Scheme Procedure: ssax:read-pi-body-as-string port

 -- Scheme Procedure: ssax:reverse-collect-str-drop-ws fragments

 -- Scheme Procedure: ssax:read-markup-token port

 -- Scheme Procedure: ssax:read-cdata-body port str-handler seed

 -- Scheme Procedure: ssax:read-char-ref port

 -- Scheme Procedure: ssax:read-attributes port entities

 -- Scheme Procedure: ssax:complete-start-tag tag-head port elems
          entities namespaces

 -- Scheme Procedure: ssax:read-external-id port

 -- Scheme Procedure: ssax:read-char-data port expect-eof? str-handler
          seed

 -- Scheme Procedure: ssax:xml->sxml port namespace-prefix-assig

 -- Scheme Syntax: ssax:make-parser . kw-val-pairs

 -- Scheme Syntax: ssax:make-pi-parser orig-handlers

 -- Scheme Syntax: ssax:make-elem-parser my-new-level-seed
          my-finish-element my-char-data-handler my-pi-handlers

7.22.4 Transforming SXML
------------------------

7.22.4.1 Overview
.................

SXML expression tree transformers
=================================

Pre-Post-order traversal of a tree and creation of a new tree
-------------------------------------------------------------

     pre-post-order:: <tree> x <bindings> -> <new-tree>

   where

      <bindings> ::= (<binding> ...)
      <binding> ::= (<trigger-symbol> *preorder* . <handler>) |
                    (<trigger-symbol> *macro* . <handler>) |
     		(<trigger-symbol> <new-bindings> . <handler>) |
     		(<trigger-symbol> . <handler>)
      <trigger-symbol> ::= XMLname | *text* | *default*
      <handler> :: <trigger-symbol> x [<tree>] -> <new-tree>

   The pre-post-order function visits the nodes and nodelists
pre-post-order (depth-first).  For each ‘<Node>’ of the form ‘(NAME
<Node> ...)’, it looks up an association with the given NAME among its
<BINDINGS>.  If failed, ‘pre-post-order’ tries to locate a ‘*default*’
binding.  It’s an error if the latter attempt fails as well.  Having
found a binding, the ‘pre-post-order’ function first checks to see if
the binding is of the form

     	(<trigger-symbol> *preorder* . <handler>)

   If it is, the handler is ’applied’ to the current node.  Otherwise,
the pre-post-order function first calls itself recursively for each
child of the current node, with <NEW-BINDINGS> prepended to the
<BINDINGS> in effect.  The result of these calls is passed to the
<HANDLER> (along with the head of the current <NODE>).  To be more
precise, the handler is _applied_ to the head of the current node and
its processed children.  The result of the handler, which should also be
a ‘<tree>’, replaces the current <NODE>.  If the current <NODE> is a
text string or other atom, a special binding with a symbol ‘*text*’ is
looked up.

   A binding can also be of a form

     	(<trigger-symbol> *macro* . <handler>)

   This is equivalent to ‘*preorder*’ described above.  However, the
result is re-processed again, with the current stylesheet.

7.22.4.2 Usage
..............

 -- Scheme Procedure: SRV:send-reply . fragments
     Output the FRAGMENTS to the current output port.

     The fragments are a list of strings, characters, numbers, thunks,
     ‘#f’, ‘#t’ – and other fragments.  The function traverses the tree
     depth-first, writes out strings and characters, executes thunks,
     and ignores ‘#f’ and ‘'()’.  The function returns ‘#t’ if anything
     was written at all; otherwise the result is ‘#f’ If ‘#t’ occurs
     among the fragments, it is not written out but causes the result of
     ‘SRV:send-reply’ to be ‘#t’.

 -- Scheme Procedure: foldts fdown fup fhere seed tree

 -- Scheme Procedure: post-order tree bindings

 -- Scheme Procedure: pre-post-order tree bindings

 -- Scheme Procedure: replace-range beg-pred end-pred forest

7.22.5 SXML Tree Fold
---------------------

7.22.5.1 Overview
.................

‘(sxml fold)’ defines a number of variants of the "fold" algorithm for
use in transforming SXML trees.  Additionally it defines the layout
operator, ‘fold-layout’, which might be described as a context-passing
variant of SSAX’s ‘pre-post-order’.

7.22.5.2 Usage
..............

 -- Scheme Procedure: foldt fup fhere tree
     The standard multithreaded tree fold.

     FUP is of type [a] -> a.  FHERE is of type object -> a.

 -- Scheme Procedure: foldts fdown fup fhere seed tree
     The single-threaded tree fold originally defined in SSAX. *Note
     SSAX::, for more information.

 -- Scheme Procedure: foldts* fdown fup fhere seed tree
     A variant of ‘foldts’ that allows pre-order tree rewrites.
     Originally defined in Andy Wingo’s 2007 paper, _Applications of
     fold to XML transformation_.

 -- Scheme Procedure: fold-values proc list . seeds
     A variant of ‘fold’ that allows multi-valued seeds.  Note that the
     order of the arguments differs from that of ‘fold’.  *Note SRFI-1
     Fold and Map::.

 -- Scheme Procedure: foldts*-values fdown fup fhere tree . seeds
     A variant of ‘foldts*’ that allows multi-valued seeds.  Originally
     defined in Andy Wingo’s 2007 paper, _Applications of fold to XML
     transformation_.

 -- Scheme Procedure: fold-layout tree bindings params layout stylesheet
     A traversal combinator in the spirit of ‘pre-post-order’.  *Note
     Transforming SXML::.

     ‘fold-layout’ was originally presented in Andy Wingo’s 2007 paper,
     _Applications of fold to XML transformation_.

          bindings := (<binding>...)
          binding  := (<tag> <bandler-pair>...)
                    | (*default* . <post-handler>)
                    | (*text* . <text-handler>)
          tag      := <symbol>
          handler-pair := (pre-layout . <pre-layout-handler>)
                    | (post . <post-handler>)
                    | (bindings . <bindings>)
                    | (pre . <pre-handler>)
                    | (macro . <macro-handler>)

     PRE-LAYOUT-HANDLER
          A function of three arguments:

          KIDS
               the kids of the current node, before traversal

          PARAMS
               the params of the current node

          LAYOUT
               the layout coming into this node

          PRE-LAYOUT-HANDLER is expected to use this information to
          return a layout to pass to the kids.  The default
          implementation returns the layout given in the arguments.

     POST-HANDLER
          A function of five arguments:

          TAG
               the current tag being processed

          PARAMS
               the params of the current node

          LAYOUT
               the layout coming into the current node, before any kids
               were processed

          KLAYOUT
               the layout after processing all of the children

          KIDS
               the already-processed child nodes

          POST-HANDLER should return two values, the layout to pass to
          the next node and the final tree.

     TEXT-HANDLER
          TEXT-HANDLER is a function of three arguments:

          TEXT
               the string

          PARAMS
               the current params

          LAYOUT
               the current layout

          TEXT-HANDLER should return two values, the layout to pass to
          the next node and the value to which the string should
          transform.

7.22.6 SXPath
-------------

7.22.6.1 Overview
.................

SXPath: SXML Query Language
===========================

SXPath is a query language for SXML, an instance of XML Information set
(Infoset) in the form of s-expressions.  See ‘(sxml ssax)’ for the
definition of SXML and more details.  SXPath is also a translation into
Scheme of an XML Path Language, XPath (http://www.w3.org/TR/xpath).
XPath and SXPath describe means of selecting a set of Infoset’s items or
their properties.

   To facilitate queries, XPath maps the XML Infoset into an explicit
tree, and introduces important notions of a location path and a current,
context node.  A location path denotes a selection of a set of nodes
relative to a context node.  Any XPath tree has a distinguished, root
node – which serves as the context node for absolute location paths.
Location path is recursively defined as a location step joined with a
location path.  A location step is a simple query of the database
relative to a context node.  A step may include expressions that further
filter the selected set.  Each node in the resulting set is used as a
context node for the adjoining location path.  The result of the step is
a union of the sets returned by the latter location paths.

   The SXML representation of the XML Infoset (see SSAX.scm) is rather
suitable for querying as it is.  Bowing to the XPath specification, we
will refer to SXML information items as ’Nodes’:

      	<Node> ::= <Element> | <attributes-coll> | <attrib>
      		   | "text string" | <PI>

   This production can also be described as

     	<Node> ::= (name . <Nodeset>) | "text string"

   An (ordered) set of nodes is just a list of the constituent nodes:

      	<Nodeset> ::= (<Node> ...)

   Nodesets, and Nodes other than text strings are both lists.  A
<Nodeset> however is either an empty list, or a list whose head is not a
symbol.  A symbol at the head of a node is either an XML name (in which
case it’s a tag of an XML element), or an administrative name such as
’@’.  This uniform list representation makes processing rather simple
and elegant, while avoiding confusion.  The multi-branch tree structure
formed by the mutually-recursive datatypes <Node> and <Nodeset> lends
itself well to processing by functional languages.

   A location path is in fact a composite query over an XPath tree or
its branch.  A singe step is a combination of a projection, selection or
a transitive closure.  Multiple steps are combined via join and union
operations.  This insight allows us to _elegantly_ implement XPath as a
sequence of projection and filtering primitives – converters – joined by
"combinators".  Each converter takes a node and returns a nodeset which
is the result of the corresponding query relative to that node.  A
converter can also be called on a set of nodes.  In that case it returns
a union of the corresponding queries over each node in the set.  The
union is easily implemented as a list append operation as all nodes in a
SXML tree are considered distinct, by XPath conventions.  We also
preserve the order of the members in the union.  Query combinators are
high-order functions: they take converter(s) (which is a Node|Nodeset ->
Nodeset function) and compose or otherwise combine them.  We will be
concerned with only relative location paths [XPath]: an absolute
location path is a relative path applied to the root node.

   Similarly to XPath, SXPath defines full and abbreviated notations for
location paths.  In both cases, the abbreviated notation can be
mechanically expanded into the full form by simple rewriting rules.  In
case of SXPath the corresponding rules are given as comments to a sxpath
function, below.  The regression test suite at the end of this file
shows a representative sample of SXPaths in both notations, juxtaposed
with the corresponding XPath expressions.  Most of the samples are
borrowed literally from the XPath specification, while the others are
adjusted for our running example, tree1.

7.22.6.2 Usage
..............

 -- Scheme Procedure: nodeset? x

 -- Scheme Procedure: node-typeof? crit

 -- Scheme Procedure: node-eq? other

 -- Scheme Procedure: node-equal? other

 -- Scheme Procedure: node-pos n

 -- Scheme Procedure: filter pred?
      -- Scheme Procedure: filter pred list
          Return all the elements of 2nd arg LIST that satisfy predicate
          PRED.  The list is not disordered - elements that appear in the
          result list occur in the same order as they occur in the argument
          list.  The returned list may share a common tail with the argument
          list.  The dynamic order in which the various applications of pred
          are made is not specified.

               (filter even? '(0 7 8 8 43 -4)) => (0 8 8 -4)



 -- Scheme Procedure: take-until pred?

 -- Scheme Procedure: take-after pred?

 -- Scheme Procedure: map-union proc lst

 -- Scheme Procedure: node-reverse node-or-nodeset

 -- Scheme Procedure: node-trace title

 -- Scheme Procedure: select-kids test-pred?

 -- Scheme Procedure: node-self pred?
      -- Scheme Procedure: filter pred list
          Return all the elements of 2nd arg LIST that satisfy predicate
          PRED.  The list is not disordered - elements that appear in the
          result list occur in the same order as they occur in the argument
          list.  The returned list may share a common tail with the argument
          list.  The dynamic order in which the various applications of pred
          are made is not specified.

               (filter even? '(0 7 8 8 43 -4)) => (0 8 8 -4)



 -- Scheme Procedure: node-join . selectors

 -- Scheme Procedure: node-reduce . converters

 -- Scheme Procedure: node-or . converters

 -- Scheme Procedure: node-closure test-pred?

 -- Scheme Procedure: node-parent rootnode

 -- Scheme Procedure: sxpath path

7.22.7 (sxml ssax input-parse)
------------------------------

7.22.7.1 Overview
.................

A simple lexer.

   The procedures in this module surprisingly often suffice to parse an
input stream.  They either skip, or build and return tokens, according
to inclusion or delimiting semantics.  The list of characters to expect,
include, or to break at may vary from one invocation of a function to
another.  This allows the functions to easily parse even
context-sensitive languages.

   EOF is generally frowned on, and thrown up upon if encountered.
Exceptions are mentioned specifically.  The list of expected characters
(characters to skip until, or break-characters) may include an EOF
"character", which is to be coded as the symbol, ‘*eof*’.

   The input stream to parse is specified as a "port", which is usually
the last (and optional) argument.  It defaults to the current input port
if omitted.

   If the parser encounters an error, it will throw an exception to the
key ‘parser-error’.  The arguments will be of the form ‘(PORT MESSAGE
SPECIALISING-MSG*)’.

   The first argument is a port, which typically points to the offending
character or its neighborhood.  You can then use ‘port-column’ and
‘port-line’ to query the current position.  MESSAGE is the description
of the error.  Other arguments supply more details about the problem.

7.22.7.2 Usage
..............

 -- Scheme Procedure: peek-next-char [port]

 -- Scheme Procedure: assert-curr-char expected-chars comment [port]

 -- Scheme Procedure: skip-until arg [port]

 -- Scheme Procedure: skip-while skip-chars [port]

 -- Scheme Procedure: next-token prefix-skipped-chars break-chars
          [comment] [port]

 -- Scheme Procedure: next-token-of incl-list/pred [port]

 -- Scheme Procedure: read-text-line [port]

 -- Scheme Procedure: read-string n [port]

 -- Scheme Procedure: find-string-from-port? _ _ . _
     Looks for STR in <INPUT-PORT>, optionally within the first
     MAX-NO-CHAR characters.

7.22.8 (sxml apply-templates)
-----------------------------

7.22.8.1 Overview
.................

Pre-order traversal of a tree and creation of a new tree:

     	apply-templates:: tree x <templates> -> <new-tree>

   where

      <templates> ::= (<template> ...)
      <template>  ::= (<node-test> <node-test> ... <node-test> . <handler>)
      <node-test> ::= an argument to node-typeof? above
      <handler>   ::= <tree> -> <new-tree>

   This procedure does a _normal_, pre-order traversal of an SXML tree.
It walks the tree, checking at each node against the list of matching
templates.

   If the match is found (which must be unique, i.e., unambiguous), the
corresponding handler is invoked and given the current node as an
argument.  The result from the handler, which must be a ‘<tree>’, takes
place of the current node in the resulting tree.  The name of the
function is not accidental: it resembles rather closely an
‘apply-templates’ function of XSLT.

7.22.8.2 Usage
..............

 -- Scheme Procedure: apply-templates tree templates

7.23 Texinfo Processing
=======================

7.23.1 (texinfo)
----------------

7.23.1.1 Overview
.................

Texinfo processing in scheme
----------------------------

This module parses texinfo into SXML. TeX will always be the processor
of choice for print output, of course.  However, although ‘makeinfo’
works well for info, its output in other formats is not very
customizable, and the program is not extensible as a whole.  This module
aims to provide an extensible framework for texinfo processing that
integrates texinfo into the constellation of SXML processing tools.

Notes on the SXML vocabulary
----------------------------

Consider the following texinfo fragment:

      @deffn Primitive set-car! pair value
      This function...
      @end deffn

   Logically, the category (Primitive), name (set-car!), and arguments
(pair value) are “attributes” of the deffn, with the description as the
content.  However, texinfo allows for @-commands within the arguments to
an environment, like ‘@deffn’, which means that texinfo “attributes” are
PCDATA. XML attributes, on the other hand, are CDATA. For this reason,
“attributes” of texinfo @-commands are called “arguments”, and are
grouped under the special element, ‘%’.

   Because ‘%’ is not a valid NCName, stexinfo is a superset of SXML. In
the interests of interoperability, this module provides a conversion
function to replace the ‘%’ with ‘texinfo-arguments’.

7.23.1.2 Usage
..............

 -- Function: call-with-file-and-dir filename proc
     Call the one-argument procedure PROC with an input port that reads
     from FILENAME.  During the dynamic extent of PROC’s execution, the
     current directory will be ‘(dirname FILENAME)’.  This is useful for
     parsing documents that can include files by relative path name.

 -- Variable: texi-command-specs

 -- Function: texi-command-depth command max-depth
     Given the texinfo command COMMAND, return its nesting level, or
     ‘#f’ if it nests too deep for MAX-DEPTH.

     Examples:

           (texi-command-depth 'chapter 4)        ⇒ 1
           (texi-command-depth 'top 4)            ⇒ 0
           (texi-command-depth 'subsection 4)     ⇒ 3
           (texi-command-depth 'appendixsubsec 4) ⇒ 3
           (texi-command-depth 'subsection 2)     ⇒ #f

 -- Function: texi-fragment->stexi string-or-port
     Parse the texinfo commands in STRING-OR-PORT, and return the
     resultant stexi tree.  The head of the tree will be the special
     command, ‘*fragment*’.

 -- Function: texi->stexi port
     Read a full texinfo document from PORT and return the parsed stexi
     tree.  The parsing will start at the ‘@settitle’ and end at ‘@bye’
     or EOF.

 -- Function: stexi->sxml tree
     Transform the stexi tree TREE into sxml.  This involves replacing
     the ‘%’ element that keeps the texinfo arguments with an element
     for each argument.

     FIXME: right now it just changes % to ‘texinfo-arguments’ – that
     doesn’t hang with the idea of making a dtd at some point

7.23.2 (texinfo docbook)
------------------------

7.23.2.1 Overview
.................

This module exports procedures for transforming a limited subset of the
SXML representation of docbook into stexi.  It is not complete by any
means.  The intention is to gather a number of routines and stylesheets
so that external modules can parse specific subsets of docbook, for
example that set generated by certain tools.

7.23.2.2 Usage
..............

 -- Variable: *sdocbook->stexi-rules*

 -- Variable: *sdocbook-block-commands*

 -- Function: sdocbook-flatten sdocbook
     "Flatten" a fragment of sdocbook so that block elements do not nest
     inside each other.

     Docbook is a nested format, where e.g.  a ‘refsect2’ normally
     appears inside a ‘refsect1’.  Logical divisions in the document are
     represented via the tree topology; a ‘refsect2’ element _contains_
     all of the elements in its section.

     On the contrary, texinfo is a flat format, in which sections are
     marked off by standalone section headers like ‘@subsection’, and
     block elements do not nest inside each other.

     This function takes a nested sdocbook fragment SDOCBOOK and
     flattens all of the sections, such that e.g.

           (refsect1 (refsect2 (para "Hello")))

     becomes

           ((refsect1) (refsect2) (para "Hello"))

     Oftentimes (always?)  sectioning elements have ‘<title>’ as their
     first element child; users interested in processing the ‘refsect*’
     elements into proper sectioning elements like ‘chapter’ might be
     interested in ‘replace-titles’ and ‘filter-empty-elements’.  *Note
     replace-titles: texinfo docbook replace-titles, and *note
     filter-empty-elements: texinfo docbook filter-empty-elements.

     Returns a nodeset; that is to say, an untagged list of stexi
     elements.  *Note SXPath::, for the definition of a nodeset.

 -- Function: filter-empty-elements sdocbook
     Filters out empty elements in an sdocbook nodeset.  Mostly useful
     after running ‘sdocbook-flatten’.

 -- Function: replace-titles sdocbook-fragment
     Iterate over the sdocbook nodeset SDOCBOOK-FRAGMENT, transforming
     contiguous ‘refsect’ and ‘title’ elements into the appropriate
     texinfo sectioning command.  Most useful after having run
     ‘sdocbook-flatten’.

     For example:

           (replace-titles '((refsect1) (title "Foo") (para "Bar.")))
              ⇒ '((chapter "Foo") (para "Bar."))

7.23.3 (texinfo html)
---------------------

7.23.3.1 Overview
.................

This module implements transformation from ‘stexi’ to HTML. Note that
the output of ‘stexi->shtml’ is actually SXML with the HTML vocabulary.
This means that the output can be further processed, and that it must
eventually be serialized by ‘sxml->xml’.  *Note Reading and Writing
XML::.

   References (i.e., the ‘@ref’ family of commands) are resolved by a
"ref-resolver".  *Note add-ref-resolver!: texinfo html
add-ref-resolver!.

7.23.3.2 Usage
..............

 -- Function: add-ref-resolver! proc
     Add PROC to the head of the list of ref-resolvers.  PROC will be
     expected to take the name of a node and the name of a manual and
     return the URL of the referent, or ‘#f’ to pass control to the next
     ref-resolver in the list.

     The default ref-resolver will return the concatenation of the
     manual name, ‘#’, and the node name.

 -- Function: stexi->shtml tree
     Transform the stexi TREE into shtml, resolving references via
     ref-resolvers.  See the module commentary for more details.

 -- Function: urlify str

7.23.4 (texinfo indexing)
-------------------------

7.23.4.1 Overview
.................

Given a piece of stexi, return an index of a specified variety.

   Note that currently, ‘stexi-extract-index’ doesn’t differentiate
between different kinds of index entries.  That’s a bug ;)

7.23.4.2 Usage
..............

 -- Function: stexi-extract-index tree manual-name kind
     Given an stexi tree TREE, index all of the entries of type KIND.
     KIND can be one of the predefined texinfo indices (‘concept’,
     ‘variable’, ‘function’, ‘key’, ‘program’, ‘type’) or one of the
     special symbols ‘auto’ or ‘all’.  ‘auto’ will scan the stext for a
     ‘(printindex)’ statement, and ‘all’ will generate an index from all
     entries, regardless of type.

     The returned index is a list of pairs, the CAR of which is the
     entry (a string) and the CDR of which is a node name (a string).

7.23.5 (texinfo string-utils)
-----------------------------

7.23.5.1 Overview
.................

Module ‘(texinfo string-utils)’ provides various string-related
functions useful to Guile’s texinfo support.

7.23.5.2 Usage
..............

 -- Function: escape-special-chars str special-chars escape-char
     Returns a copy of STR with all given special characters preceded by
     the given ESCAPE-CHAR.

     SPECIAL-CHARS can either be a single character, or a string
     consisting of all the special characters.

          ;; make a string regexp-safe...
           (escape-special-chars "***(Example String)***"
                                "[]()/*."
                                #\\)
          => "\\*\\*\\*\\(Example String\\)\\*\\*\\*"

          ;; also can escape a singe char...
           (escape-special-chars "richardt@vzavenue.net"
                                #\@
                                #\@)
          => "richardt@@vzavenue.net"

 -- Function: transform-string str match? replace [start] [end]
     Uses MATCH? against each character in STR, and performs a
     replacement on each character for which matches are found.

     MATCH? may either be a function, a character, a string, or ‘#t’.
     If MATCH? is a function, then it takes a single character as input,
     and should return ‘#t’ for matches.  MATCH? is a character, it is
     compared to each string character using ‘char=?’.  If MATCH? is a
     string, then any character in that string will be considered a
     match.  ‘#t’ will cause every character to be a match.

     If REPLACE is a function, it is called with the matched character
     as an argument, and the returned value is sent to the output string
     via ‘display’.  If REPLACE is anything else, it is sent through the
     output string via ‘display’.

     Note that te replacement for the matched characters does not need
     to be a single character.  That is what differentiates this
     function from ‘string-map’, and what makes it useful for
     applications such as converting ‘#\&’ to ‘"&amp;"’ in web page
     text.  Some other functions in this module are just wrappers around
     common uses of ‘transform-string’.  Transformations not possible
     with this function should probably be done with regular
     expressions.

     If START and END are given, they control which portion of the
     string undergoes transformation.  The entire input string is still
     output, though.  So, if START is ‘5’, then the first five
     characters of STR will still appear in the returned string.

          ; these two are equivalent...
           (transform-string str #\space #\-) ; change all spaces to -'s
           (transform-string str (lambda (c) (char=? #\space c)) #\-)

 -- Function: expand-tabs str [tab-size]
     Returns a copy of STR with all tabs expanded to spaces.  TAB-SIZE
     defaults to 8.

     Assuming tab size of 8, this is equivalent to:

           (transform-string str #\tab "        ")

 -- Function: center-string str [width] [chr] [rchr]
     Returns a copy of STR centered in a field of WIDTH characters.  Any
     needed padding is done by character CHR, which defaults to
     ‘#\space’.  If RCHR is provided, then the padding to the right will
     use it instead.  See the examples below.  left and RCHR on the
     right.  The default WIDTH is 80.  The default CHR and RCHR is
     ‘#\space’.  The string is never truncated.

           (center-string "Richard Todd" 24)
          => "      Richard Todd      "

           (center-string " Richard Todd " 24 #\=)
          => "===== Richard Todd ====="

           (center-string " Richard Todd " 24 #\< #\>)
          => "<<<<< Richard Todd >>>>>"

 -- Function: left-justify-string str [width] [chr]
     ‘left-justify-string str [width chr]’.  Returns a copy of STR
     padded with CHR such that it is left justified in a field of WIDTH
     characters.  The default WIDTH is 80.  Unlike ‘string-pad’ from
     srfi-13, the string is never truncated.

 -- Function: right-justify-string str [width] [chr]
     Returns a copy of STR padded with CHR such that it is right
     justified in a field of WIDTH characters.  The default WIDTH is 80.
     The default CHR is ‘#\space’.  Unlike ‘string-pad’ from srfi-13,
     the string is never truncated.

 -- Function: collapse-repeated-chars str [chr] [num]
     Returns a copy of STR with all repeated instances of CHR collapsed
     down to at most NUM instances.  The default value for CHR is
     ‘#\space’, and the default value for NUM is 1.

           (collapse-repeated-chars "H  e  l  l  o")
          => "H e l l o"
           (collapse-repeated-chars "H--e--l--l--o" #\-)
          => "H-e-l-l-o"
           (collapse-repeated-chars "H-e--l---l----o" #\- 2)
          => "H-e--l--l--o"

 -- Function: make-text-wrapper [#:line-width] [#:expand-tabs?]
          [#:tab-width] [#:collapse-whitespace?] [#:subsequent-indent]
          [#:initial-indent] [#:break-long-words?]
     Returns a procedure that will split a string into lines according
     to the given parameters.

     ‘#:line-width’
          This is the target length used when deciding where to wrap
          lines.  Default is 80.

     ‘#:expand-tabs?’
          Boolean describing whether tabs in the input should be
          expanded.  Default is #t.

     ‘#:tab-width’
          If tabs are expanded, this will be the number of spaces to
          which they expand.  Default is 8.

     ‘#:collapse-whitespace?’
          Boolean describing whether the whitespace inside the existing
          text should be removed or not.  Default is #t.

          If text is already well-formatted, and is just being wrapped
          to fit in a different width, then set this to ‘#f’.  This way,
          many common text conventions (such as two spaces between
          sentences) can be preserved if in the original text.  If the
          input text spacing cannot be trusted, then leave this setting
          at the default, and all repeated whitespace will be collapsed
          down to a single space.

     ‘#:initial-indent’
          Defines a string that will be put in front of the first line
          of wrapped text.  Default is the empty string, “”.

     ‘#:subsequent-indent’
          Defines a string that will be put in front of all lines of
          wrapped text, except the first one.  Default is the empty
          string, “”.

     ‘#:break-long-words?’
          If a single word is too big to fit on a line, this setting
          tells the wrapper what to do.  Defaults to #t, which will
          break up long words.  When set to #f, the line will be
          allowed, even though it is longer than the defined
          ‘#:line-width’.

     The return value is a procedure of one argument, the input string,
     which returns a list of strings, where each element of the list is
     one line.

 -- Function: fill-string str . kwargs
     Wraps the text given in string STR according to the parameters
     provided in KWARGS, or the default setting if they are not given.
     Returns a single string with the wrapped text.  Valid keyword
     arguments are discussed in ‘make-text-wrapper’.

 -- Function: string->wrapped-lines str . kwargs
     ‘string->wrapped-lines str keywds ...’.  Wraps the text given in
     string STR according to the parameters provided in KEYWDS, or the
     default setting if they are not given.  Returns a list of strings
     representing the formatted lines.  Valid keyword arguments are
     discussed in ‘make-text-wrapper’.

7.23.6 (texinfo plain-text)
---------------------------

7.23.6.1 Overview
.................

Transformation from stexi to plain-text.  Strives to re-create the
output from ‘info’; comes pretty damn close.

7.23.6.2 Usage
..............

 -- Function: stexi->plain-text tree
     Transform TREE into plain text.  Returns a string.

7.23.7 (texinfo serialize)
--------------------------

7.23.7.1 Overview
.................

Serialization of ‘stexi’ to plain texinfo.

7.23.7.2 Usage
..............

 -- Function: stexi->texi tree
     Serialize the stexi TREE into plain texinfo.

7.23.8 (texinfo reflection)
---------------------------

7.23.8.1 Overview
.................

Routines to generare ‘stexi’ documentation for objects and modules.

   Note that in this context, an "object" is just a value associated
with a location.  It has nothing to do with GOOPS.

7.23.8.2 Usage
..............

 -- Function: module-stexi-documentation sym-name [%docs-resolver]
          [#:docs-resolver]
     Return documentation for the module named SYM-NAME.  The
     documentation will be formatted as ‘stexi’ (*note texinfo:
     texinfo.).

 -- Function: script-stexi-documentation scriptpath
     Return documentation for given script.  The documentation will be
     taken from the script’s commentary, and will be returned in the
     ‘stexi’ format (*note texinfo: texinfo.).

 -- Function: object-stexi-documentation _ [_] [#:force]

 -- Function: package-stexi-standard-copying name version updated years
          copyright-holder permissions
     Create a standard texinfo ‘copying’ section.

     YEARS is a list of years (as integers) in which the modules being
     documented were released.  All other arguments are strings.

 -- Function: package-stexi-standard-titlepage name version updated
          authors
     Create a standard GNU title page.

     AUTHORS is a list of ‘(NAME . EMAIL)’ pairs.  All other arguments
     are strings.

     Here is an example of the usage of this procedure:

           (package-stexi-standard-titlepage
            "Foolib"
            "3.2"
            "26 September 2006"
            '(("Alyssa P Hacker" . "alyssa@example.com"))
            '(2004 2005 2006)
            "Free Software Foundation, Inc."
            "Standard GPL permissions blurb goes here")

 -- Function: package-stexi-generic-menu name entries
     Create a menu from a generic alist of entries, the car of which
     should be the node name, and the cdr the description.  As an
     exception, an entry of ‘#f’ will produce a separator.

 -- Function: package-stexi-standard-menu name modules
          module-descriptions extra-entries
     Create a standard top node and menu, suitable for processing by
     makeinfo.

 -- Function: package-stexi-extended-menu name module-pairs script-pairs
          extra-entries
     Create an "extended" menu, like the standard menu but with a
     section for scripts.

 -- Function: package-stexi-standard-prologue name filename category
          description copying titlepage menu
     Create a standard prologue, suitable for later serialization to
     texinfo and .info creation with makeinfo.

     Returns a list of stexinfo forms suitable for passing to
     ‘package-stexi-documentation’ as the prologue.  *Note texinfo
     reflection package-stexi-documentation::, *note
     package-stexi-standard-titlepage: texinfo reflection
     package-stexi-standard-titlepage, *note
     package-stexi-standard-copying: texinfo reflection
     package-stexi-standard-copying, and *note
     package-stexi-standard-menu: texinfo reflection
     package-stexi-standard-menu.

 -- Function: package-stexi-documentation modules name filename prologue
          epilogue [#:module-stexi-documentation-args] [#:scripts]
     Create stexi documentation for a "package", where a package is a
     set of modules that is released together.

     MODULES is expected to be a list of module names, where a module
     name is a list of symbols.  The stexi that is returned will be
     titled NAME and a texinfo filename of FILENAME.

     PROLOGUE and EPILOGUE are lists of stexi forms that will be spliced
     into the output document before and after the generated modules
     documentation, respectively.  *Note texinfo reflection
     package-stexi-standard-prologue::, to create a conventional GNU
     texinfo prologue.

     MODULE-STEXI-DOCUMENTATION-ARGS is an optional argument that, if
     given, will be added to the argument list when
     ‘module-texi-documentation’ is called.  For example, it might be
     useful to define a ‘#:docs-resolver’ argument.

 -- Function: package-stexi-documentation-for-include modules
          module-descriptions [#:module-stexi-documentation-args]
     Create stexi documentation for a "package", where a package is a
     set of modules that is released together.

     MODULES is expected to be a list of module names, where a module
     name is a list of symbols.  Returns an stexinfo fragment.

     Unlike ‘package-stexi-documentation’, this function simply produces
     a menu and the module documentations instead of producing a full
     texinfo document.  This can be useful if you write part of your
     manual by hand, and just use ‘@include’ to pull in the
     automatically generated parts.

     MODULE-STEXI-DOCUMENTATION-ARGS is an optional argument that, if
     given, will be added to the argument list when
     ‘module-texi-documentation’ is called.  For example, it might be
     useful to define a ‘#:docs-resolver’ argument.

