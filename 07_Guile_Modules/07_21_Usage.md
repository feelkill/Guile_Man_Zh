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

