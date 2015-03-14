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

