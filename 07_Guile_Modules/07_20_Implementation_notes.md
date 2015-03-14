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

