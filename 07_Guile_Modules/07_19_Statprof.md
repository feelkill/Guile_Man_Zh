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

