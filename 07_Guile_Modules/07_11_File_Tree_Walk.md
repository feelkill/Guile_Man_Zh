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

