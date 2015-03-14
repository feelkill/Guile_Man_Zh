Procedure Index
***************

This is an alphabetical list of all the procedures and macros in Guile.
It also includes Guile’s Autoconf macros.

   When looking for a particular procedure, please look under its Scheme
name as well as under its C name.  The C name can be constructed from
the Scheme names by a simple transformation described in the section
*Note API Overview::.

* Menu:

* #:accessor:                            Slot Options.      (line 44406)
* #:allocation:                          Slot Options.      (line 44455)
* #:class:                               Slot Options.      (line 44467)
* #:each-subclass:                       Slot Options.      (line 44477)
* #:getter:                              Slot Options.      (line 44404)
* #:init-form:                           Slot Options.      (line 44324)
* #:init-keyword:                        Slot Options.      (line 44326)
* #:init-thunk:                          Slot Options.      (line 44325)
* #:init-value:                          Slot Options.      (line 44323)
* #:instance:                            Slot Options.      (line 44461)
* #:metaclass:                           Class Definition.  (line 44225)
* #:name:                                Class Definition.  (line 44235)
* #:setter:                              Slot Options.      (line 44405)
* #:slot-ref:                            Slot Options.      (line 44487)
* #:slot-ref <1>:                        Slot Options.      (line 44500)
* #:slot-ref <2>:                        Slot Description Example.
                                                            (line 44582)
* #:slot-set!:                           Slot Options.      (line 44487)
* #:slot-set! <1>:                       Slot Options.      (line 44501)
* #:slot-set! <2>:                       Slot Description Example.
                                                            (line 44582)
* #:virtual:                             Slot Options.      (line 44487)
* %:                                     Shift and Reset.   (line 18669)
* % <1>:                                 Shift and Reset.   (line 18670)
* % <2>:                                 Shift and Reset.   (line 18671)
* %char-set-dump:                        Querying Character Sets.
                                                            (line  8858)
* %default-port-conversion-strategy:     Ports.             (line 19864)
* %library-dir:                          Build Config.      (line 26682)
* %make-void-port:                       Void Ports.        (line 20707)
* %package-data-dir:                     Build Config.      (line 26676)
* %read-delimited!:                      Line/Delimited.    (line 20218)
* %read-line:                            Line/Delimited.    (line 20236)
* %search-load-path:                     Load Paths.        (line 23011)
* %site-ccache-dir:                      Installing Site Packages.
                                                            (line  4072)
* %site-ccache-dir <1>:                  Build Config.      (line 26698)
* %site-dir:                             Installing Site Packages.
                                                            (line  4072)
* %site-dir <1>:                         Build Config.      (line 26692)
* %string-dump:                          String Internals.  (line 10456)
* &assertion:                            rnrs conditions.   (line 39352)
* &condition:                            rnrs conditions.   (line 39290)
* &error:                                rnrs conditions.   (line 39341)
* &i/o:                                  I/O Conditions.    (line 39412)
* &i/o-decoding:                         R6RS Transcoders.  (line 20915)
* &i/o-encoding:                         R6RS Transcoders.  (line 20932)
* &i/o-file-already-exists:              I/O Conditions.    (line 39454)
* &i/o-file-does-not-exist:              I/O Conditions.    (line 39460)
* &i/o-file-is-read-only:                I/O Conditions.    (line 39448)
* &i/o-file-protection:                  I/O Conditions.    (line 39441)
* &i/o-filename:                         I/O Conditions.    (line 39434)
* &i/o-invalid-position:                 I/O Conditions.    (line 39427)
* &i/o-port:                             I/O Conditions.    (line 39466)
* &i/o-read:                             I/O Conditions.    (line 39417)
* &i/o-write:                            I/O Conditions.    (line 39422)
* &implementation-restriction:           rnrs conditions.   (line 39379)
* &irritants:                            rnrs conditions.   (line 39358)
* &lexical:                              rnrs conditions.   (line 39385)
* &message:                              rnrs conditions.   (line 39323)
* &no-infinities:                        rnrs arithmetic flonums.
                                                            (line 39832)
* &no-nans:                              rnrs arithmetic flonums.
                                                            (line 39839)
* &non-continuable:                      rnrs conditions.   (line 39373)
* &serious:                              rnrs conditions.   (line 39335)
* &syntax:                               rnrs conditions.   (line 39391)
* &undefined:                            rnrs conditions.   (line 39400)
* &violation:                            rnrs conditions.   (line 39346)
* &warning:                              rnrs conditions.   (line 39330)
* &who:                                  rnrs conditions.   (line 39365)
* ':                                     Expression Syntax. (line 22337)
* (oop goops):                           GOOPS.             (line 44155)
* *:                                     Arithmetic.        (line  7871)
* * <1>:                                 rnrs base.         (line 38636)
* *scm_to_latin1_stringn:                Conversion to/from C.
                                                            (line 10415)
* *scm_to_stringn:                       Conversion to/from C.
                                                            (line 10365)
* *scm_to_utf32_stringn:                 Conversion to/from C.
                                                            (line 10417)
* *scm_to_utf8_stringn:                  Conversion to/from C.
                                                            (line 10416)
* +:                                     Arithmetic.        (line  7860)
* + <1>:                                 rnrs base.         (line 38634)
* ,:                                     Expression Syntax. (line 22365)
* ,@:                                    Expression Syntax. (line 22375)
* -:                                     Arithmetic.        (line  7865)
* - <1>:                                 rnrs base.         (line 38635)
* ->char-set:                            Creating Character Sets.
                                                            (line  8845)
* /:                                     Arithmetic.        (line  7876)
* / <1>:                                 rnrs base.         (line 38637)
* 1+:                                    Arithmetic.        (line  7854)
* 1+ <1>:                                Arithmetic.        (line  7881)
* 1-:                                    Arithmetic.        (line  7854)
* 1- <1>:                                Arithmetic.        (line  7885)
* <:                                     Comparison.        (line  7749)
* < <1>:                                 rnrs base.         (line 38578)
* <=:                                    Comparison.        (line  7757)
* <= <1>:                                rnrs base.         (line 38580)
* =:                                     Comparison.        (line  7745)
* = <1>:                                 rnrs base.         (line 38577)
* ==:                                    Equality.          (line 17313)
* >:                                     Comparison.        (line  7753)
* > <1>:                                 rnrs base.         (line 38579)
* >=:                                    Comparison.        (line  7762)
* >= <1>:                                rnrs base.         (line 38581)
* @:                                     Using Guile Modules.
                                                            (line 23963)
* @ <1>:                                 Using Guile Modules.
                                                            (line 23967)
* `:                                     Expression Syntax. (line 22355)
* abandoned-mutex-exception?:            SRFI-18 Exceptions.
                                                            (line 35863)
* abort:                                 Shift and Reset.   (line 18691)
* abort <1>:                             Dynamic Environment Instructions.
                                                            (line 48398)
* abort-to-prompt:                       Prompt Primitives. (line 18547)
* abs:                                   Arithmetic.        (line  7889)
* abs <1>:                               rnrs base.         (line 38640)
* absolute-file-name?:                   File System.       (line 29899)
* accept:                                Network Sockets and Communication.
                                                            (line 31730)
* access?:                               File System.       (line 29550)
* acons:                                 Adding or Setting Alist Entries.
                                                            (line 14474)
* acos:                                  Scientific.        (line  8124)
* acos <1>:                              rnrs base.         (line 38548)
* acosh:                                 Scientific.        (line  8153)
* activate-readline:                     Readline Functions.
                                                            (line 40560)
* adapt-response-version:                Responses.         (line 33049)
* add:                                   Inlined Mathematical Instructions.
                                                            (line 48506)
* add-duration:                          SRFI-19 Time.      (line 36025)
* add-duration!:                         SRFI-19 Time.      (line 36026)
* add-ephemeral-stepping-trap!:          High-Level Traps.  (line 28861)
* add-ephemeral-trap-at-frame-finish!:   High-Level Traps.  (line 28854)
* add-hook!:                             Hook Reference.    (line 17682)
* add-method!:                           Method Definition Internals.
                                                            (line 46287)
* add-method! <1>:                       Method Definition Internals.
                                                            (line 46290)
* add-method! <2>:                       Method Definition Internals.
                                                            (line 46293)
* add-method! <3>:                       Method Definition Internals.
                                                            (line 46299)
* add-method! <4>:                       Method Definition Internals.
                                                            (line 46305)
* add-ref-resolver!:                     texinfo html.      (line 43768)
* add-to-load-path:                      Load Paths.        (line 22978)
* add-trace-at-procedure-call!:          High-Level Traps.  (line 28841)
* add-trap!:                             Trap States.       (line 28762)
* add-trap-at-procedure-call!:           High-Level Traps.  (line 28836)
* add-trap-at-source-location!:          High-Level Traps.  (line 28847)
* add1:                                  Inlined Mathematical Instructions.
                                                            (line 48507)
* addrinfo:addr:                         Network Databases. (line 31214)
* addrinfo:canonname:                    Network Databases. (line 31218)
* addrinfo:fam:                          Network Databases. (line 31205)
* addrinfo:flags:                        Network Databases. (line 31202)
* addrinfo:protocol:                     Network Databases. (line 31211)
* addrinfo:socktype:                     Network Databases. (line 31208)
* alarm:                                 Signals.           (line 30762)
* alignof:                               Foreign Structs.   (line 25415)
* alist->hash-table:                     Hash Table Reference.
                                                            (line 14975)
* alist->hash-table <1>:                 SRFI-69 Creating hash tables.
                                                            (line 38065)
* alist->hashq-table:                    Hash Table Reference.
                                                            (line 14976)
* alist->hashv-table:                    Hash Table Reference.
                                                            (line 14977)
* alist->hashx-table:                    Hash Table Reference.
                                                            (line 14978)
* alist->vhash:                          VHashes.           (line 14813)
* alist-cons:                            SRFI-1 Association Lists.
                                                            (line 34656)
* alist-copy:                            SRFI-1 Association Lists.
                                                            (line 34665)
* alist-delete:                          SRFI-1 Association Lists.
                                                            (line 34669)
* alist-delete!:                         SRFI-1 Association Lists.
                                                            (line 34670)
* all-threads:                           Threads.           (line 25773)
* and:                                   and or.            (line 18350)
* and <1>:                               rnrs base.         (line 38517)
* and-let*:                              SRFI-2.            (line 34865)
* and=>:                                 Higher-Order Functions.
                                                            (line 15923)
* angle:                                 Complex.           (line  7834)
* angle <1>:                             rnrs base.         (line 38537)
* any:                                   SRFI-1 Searching.  (line 34527)
* any->c32vector:                        SRFI-4 Extensions. (line 35369)
* any->c64vector:                        SRFI-4 Extensions. (line 35370)
* any->f32vector:                        SRFI-4 Extensions. (line 35367)
* any->f64vector:                        SRFI-4 Extensions. (line 35368)
* any->s16vector:                        SRFI-4 Extensions. (line 35362)
* any->s32vector:                        SRFI-4 Extensions. (line 35364)
* any->s64vector:                        SRFI-4 Extensions. (line 35366)
* any->s8vector:                         SRFI-4 Extensions. (line 35360)
* any->u16vector:                        SRFI-4 Extensions. (line 35361)
* any->u32vector:                        SRFI-4 Extensions. (line 35363)
* any->u64vector:                        SRFI-4 Extensions. (line 35365)
* any->u8vector:                         SRFI-4 Extensions. (line 35359)
* any-bits-set?:                         SRFI-60.           (line 37890)
* append:                                Append/Reverse.    (line 12081)
* append <1>:                            Append/Reverse.    (line 12082)
* append <2>:                            rnrs base.         (line 38598)
* append <3>:                            rnrs base.         (line 38599)
* append!:                               Append/Reverse.    (line 12083)
* append! <1>:                           Append/Reverse.    (line 12084)
* append-map:                            SRFI-1 Fold and Map.
                                                            (line 34410)
* append-map!:                           SRFI-1 Fold and Map.
                                                            (line 34411)
* append-reverse:                        SRFI-1 Length Append etc.
                                                            (line 34198)
* append-reverse!:                       SRFI-1 Length Append etc.
                                                            (line 34199)
* apply:                                 Fly Evaluation.    (line 22677)
* apply <1>:                             rnrs base.         (line 38758)
* apply <2>:                             Procedure Call and Return Instructions.
                                                            (line 47922)
* apply-templates:                       sxml apply-templates.
                                                            (line 43600)
* apply:nconc2last:                      Fly Evaluation.    (line 22722)
* apropos:                               Help Commands.     (line  3641)
* apropos-completion-function:           Readline Functions.
                                                            (line 40620)
* args-fold:                             SRFI-37.           (line 36730)
* arithmetic-shift:                      SRFI-60.           (line 37892)
* arity:allow-other-keys?:               Compiled Procedures.
                                                            (line 15519)
* arity:end:                             Compiled Procedures.
                                                            (line 15514)
* arity:kw:                              Compiled Procedures.
                                                            (line 15518)
* arity:nopt:                            Compiled Procedures.
                                                            (line 15516)
* arity:nreq:                            Compiled Procedures.
                                                            (line 15515)
* arity:rest?:                           Compiled Procedures.
                                                            (line 15517)
* arity:start:                           Compiled Procedures.
                                                            (line 15513)
* array->list:                           Array Procedures.  (line 12918)
* array-contents:                        Shared Arrays.     (line 13110)
* array-copy!:                           Array Procedures.  (line 12922)
* array-copy-in-order!:                  Array Procedures.  (line 12923)
* array-dimensions:                      Array Procedures.  (line 12891)
* array-equal?:                          Array Procedures.  (line 12934)
* array-fill!:                           Array Procedures.  (line 12929)
* array-for-each:                        Array Procedures.  (line 12955)
* array-in-bounds?:                      Array Procedures.  (line 12872)
* array-index-map!:                      Array Procedures.  (line 12960)
* array-length:                          Array Procedures.  (line 12905)
* array-map!:                            Array Procedures.  (line 12940)
* array-map-in-order!:                   Array Procedures.  (line 12941)
* array-rank:                            Array Procedures.  (line 12911)
* array-ref:                             Array Procedures.  (line 12865)
* array-set!:                            Array Procedures.  (line 12881)
* array-shape:                           Array Procedures.  (line 12890)
* array-type:                            Array Procedures.  (line 12859)
* array?:                                Array Procedures.  (line 12795)
* ash:                                   Bitwise Operations.
                                                            (line  8223)
* ash <1>:                               Inlined Mathematical Instructions.
                                                            (line 48520)
* asin:                                  Scientific.        (line  8121)
* asin <1>:                              rnrs base.         (line 38547)
* asinh:                                 Scientific.        (line  8150)
* assert:                                rnrs base.         (line 38710)
* assert-curr-char:                      sxml ssax input-parse.
                                                            (line 43550)
* assert-nargs-ee:                       Function Prologue Instructions.
                                                            (line 48016)
* assert-nargs-ee/locals:                Function Prologue Instructions.
                                                            (line 48112)
* assert-nargs-ge:                       Function Prologue Instructions.
                                                            (line 48017)
* assert-nargs-ge/locals:                Function Prologue Instructions.
                                                            (line 48113)
* assertion-violation:                   rnrs base.         (line 38715)
* assertion-violation?:                  rnrs conditions.   (line 39354)
* assoc:                                 Retrieving Alist Entries.
                                                            (line 14505)
* assoc <1>:                             SRFI-1 Association Lists.
                                                            (line 34642)
* assoc <2>:                             rnrs lists.        (line 38882)
* assoc-ref:                             Retrieving Alist Entries.
                                                            (line 14519)
* assoc-remove!:                         Removing Alist Entries.
                                                            (line 14592)
* assoc-set!:                            Adding or Setting Alist Entries.
                                                            (line 14483)
* assp:                                  rnrs lists.        (line 38881)
* assq:                                  Retrieving Alist Entries.
                                                            (line 14503)
* assq <1>:                              rnrs lists.        (line 38884)
* assq-ref:                              Retrieving Alist Entries.
                                                            (line 14517)
* assq-remove!:                          Removing Alist Entries.
                                                            (line 14590)
* assq-set!:                             Adding or Setting Alist Entries.
                                                            (line 14481)
* assv:                                  Retrieving Alist Entries.
                                                            (line 14504)
* assv <1>:                              rnrs lists.        (line 38883)
* assv-ref:                              Retrieving Alist Entries.
                                                            (line 14518)
* assv-remove!:                          Removing Alist Entries.
                                                            (line 14591)
* assv-set!:                             Adding or Setting Alist Entries.
                                                            (line 14482)
* async:                                 User asyncs.       (line 25748)
* async-mark:                            User asyncs.       (line 25752)
* atan:                                  Scientific.        (line  8127)
* atan <1>:                              Scientific.        (line  8128)
* atan <2>:                              rnrs base.         (line 38549)
* atanh:                                 Scientific.        (line  8156)
* attlist->alist:                        SSAX.              (line 43140)
* attlist-add:                           SSAX.              (line 43133)
* attlist-fold:                          SSAX.              (line 43142)
* attlist-null?:                         SSAX.              (line 43135)
* attlist-remove-top:                    SSAX.              (line 43138)
* backtrace:                             Debug Commands.    (line  3721)
* backtrace <1>:                         Pre-Unwind Debugging.
                                                            (line 28210)
* basename:                              File System.       (line 29869)
* begin:                                 begin.             (line 18174)
* begin <1>:                             rnrs base.         (line 38503)
* begin-thread:                          Threads.           (line 25873)
* binary-port?:                          R6RS Port Manipulation.
                                                            (line 21055)
* bind:                                  Network Sockets and Communication.
                                                            (line 31702)
* bind <1>:                              Network Sockets and Communication.
                                                            (line 31703)
* bind <2>:                              Network Sockets and Communication.
                                                            (line 31704)
* bind <3>:                              Network Sockets and Communication.
                                                            (line 31706)
* bind-kwargs:                           Function Prologue Instructions.
                                                            (line 48080)
* bind-optionals:                        Function Prologue Instructions.
                                                            (line 48036)
* bind-optionals/shuffle:                Function Prologue Instructions.
                                                            (line 48054)
* bind-optionals/shuffle-or-br:          Function Prologue Instructions.
                                                            (line 48055)
* bind-rest:                             Function Prologue Instructions.
                                                            (line 48050)
* bind-textdomain-codeset:               Gettext Support.   (line 27684)
* binding:                               Module Commands.   (line  3662)
* binding:boxed?:                        Compiled Procedures.
                                                            (line 15481)
* binding:end:                           Compiled Procedures.
                                                            (line 15484)
* binding:index:                         Compiled Procedures.
                                                            (line 15482)
* binding:name:                          Compiled Procedures.
                                                            (line 15480)
* binding:start:                         Compiled Procedures.
                                                            (line 15483)
* bindtextdomain:                        Gettext Support.   (line 27668)
* bit-count:                             Bit Vectors.       (line 12590)
* bit-count <1>:                         SRFI-60.           (line 37894)
* bit-count*:                            Bit Vectors.       (line 12633)
* bit-extract:                           Bitwise Operations.
                                                            (line  8297)
* bit-field:                             SRFI-60.           (line 37893)
* bit-invert!:                           Bit Vectors.       (line 12606)
* bit-position:                          Bit Vectors.       (line 12597)
* bit-set*!:                             Bit Vectors.       (line 12610)
* bit-set?:                              SRFI-60.           (line 37891)
* bitvector:                             Bit Vectors.       (line 12548)
* bitvector->list:                       Bit Vectors.       (line 12585)
* bitvector-fill!:                       Bit Vectors.       (line 12576)
* bitvector-length:                      Bit Vectors.       (line 12552)
* bitvector-ref:                         Bit Vectors.       (line 12560)
* bitvector-set!:                        Bit Vectors.       (line 12567)
* bitvector?:                            Bit Vectors.       (line 12533)
* bitwise-and:                           SRFI-60.           (line 37886)
* bitwise-and <1>:                       rnrs arithmetic bitwise.
                                                            (line 39860)
* bitwise-arithmetic-shift:              rnrs arithmetic bitwise.
                                                            (line 39901)
* bitwise-arithmetic-shift-left:         rnrs arithmetic bitwise.
                                                            (line 39902)
* bitwise-arithmetic-shift-right:        rnrs arithmetic bitwise.
                                                            (line 39903)
* bitwise-bit-count:                     rnrs arithmetic bitwise.
                                                            (line 39872)
* bitwise-bit-field:                     rnrs arithmetic bitwise.
                                                            (line 39891)
* bitwise-bit-set?:                      rnrs arithmetic bitwise.
                                                            (line 39883)
* bitwise-copy-bit:                      rnrs arithmetic bitwise.
                                                            (line 39887)
* bitwise-copy-bit-field:                rnrs arithmetic bitwise.
                                                            (line 39896)
* bitwise-first-bit-set:                 rnrs arithmetic bitwise.
                                                            (line 39879)
* bitwise-if:                            SRFI-60.           (line 37901)
* bitwise-if <1>:                        rnrs arithmetic bitwise.
                                                            (line 39867)
* bitwise-ior:                           SRFI-60.           (line 37887)
* bitwise-ior <1>:                       rnrs arithmetic bitwise.
                                                            (line 39861)
* bitwise-length:                        rnrs arithmetic bitwise.
                                                            (line 39876)
* bitwise-merge:                         SRFI-60.           (line 37902)
* bitwise-not:                           SRFI-60.           (line 37889)
* bitwise-not <1>:                       rnrs arithmetic bitwise.
                                                            (line 39859)
* bitwise-reverse-bit-field:             rnrs arithmetic bitwise.
                                                            (line 39913)
* bitwise-rotate-bit-field:              rnrs arithmetic bitwise.
                                                            (line 39908)
* bitwise-xor:                           SRFI-60.           (line 37888)
* bitwise-xor <1>:                       rnrs arithmetic bitwise.
                                                            (line 39862)
* boolean?:                              Booleans.          (line  7023)
* boolean? <1>:                          rnrs base.         (line 38409)
* booleans->integer:                     SRFI-60.           (line 37960)
* bound-identifier=?:                    Syntax Transformer Helpers.
                                                            (line 16792)
* bound-identifier=? <1>:                rnrs syntax-case.  (line 39947)
* box:                                   SRFI-111.          (line 38266)
* box <1>:                               Lexical Environment Instructions.
                                                            (line 47749)
* box?:                                  SRFI-111.          (line 38270)
* br:                                    Branch Instructions.
                                                            (line 48178)
* br-if:                                 Branch Instructions.
                                                            (line 48181)
* br-if-eq:                              Branch Instructions.
                                                            (line 48187)
* br-if-nargs-gt:                        Function Prologue Instructions.
                                                            (line 48027)
* br-if-nargs-lt:                        Function Prologue Instructions.
                                                            (line 48028)
* br-if-nargs-ne:                        Function Prologue Instructions.
                                                            (line 48026)
* br-if-not:                             Branch Instructions.
                                                            (line 48184)
* br-if-not-eq:                          Branch Instructions.
                                                            (line 48192)
* br-if-not-null:                        Branch Instructions.
                                                            (line 48198)
* br-if-null:                            Branch Instructions.
                                                            (line 48195)
* break:                                 Debug Commands.    (line  3772)
* break <1>:                             while do.          (line 18437)
* break <2>:                             SRFI-1 Searching.  (line 34513)
* break <3>:                             Miscellaneous Instructions.
                                                            (line 48433)
* break!:                                SRFI-1 Searching.  (line 34514)
* break-at-source:                       Debug Commands.    (line  3775)
* broadcast-condition-variable:          Mutexes and Condition Variables.
                                                            (line 26037)
* buffer-mode:                           R6RS Buffer Modes. (line 20825)
* buffer-mode?:                          R6RS Buffer Modes. (line 20833)
* build-request:                         Requests.          (line 32937)
* build-response:                        Responses.         (line 33043)
* build-uri:                             URIs.              (line 32165)
* bv-f32-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48551)
* bv-f32-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48569)
* bv-f32-ref:                            Inlined Bytevector Instructions.
                                                            (line 48559)
* bv-f32-set:                            Inlined Bytevector Instructions.
                                                            (line 48577)
* bv-f64-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48552)
* bv-f64-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48570)
* bv-f64-ref:                            Inlined Bytevector Instructions.
                                                            (line 48560)
* bv-f64-set:                            Inlined Bytevector Instructions.
                                                            (line 48578)
* bv-s16-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48546)
* bv-s16-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48564)
* bv-s16-ref:                            Inlined Bytevector Instructions.
                                                            (line 48554)
* bv-s16-set:                            Inlined Bytevector Instructions.
                                                            (line 48572)
* bv-s32-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48548)
* bv-s32-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48566)
* bv-s32-ref:                            Inlined Bytevector Instructions.
                                                            (line 48556)
* bv-s32-set:                            Inlined Bytevector Instructions.
                                                            (line 48574)
* bv-s64-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48550)
* bv-s64-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48568)
* bv-s64-ref:                            Inlined Bytevector Instructions.
                                                            (line 48558)
* bv-s64-set:                            Inlined Bytevector Instructions.
                                                            (line 48576)
* bv-s8-ref:                             Inlined Bytevector Instructions.
                                                            (line 48544)
* bv-s8-set:                             Inlined Bytevector Instructions.
                                                            (line 48562)
* bv-u16-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48545)
* bv-u16-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48563)
* bv-u16-ref:                            Inlined Bytevector Instructions.
                                                            (line 48553)
* bv-u16-set:                            Inlined Bytevector Instructions.
                                                            (line 48571)
* bv-u32-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48547)
* bv-u32-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48565)
* bv-u32-ref:                            Inlined Bytevector Instructions.
                                                            (line 48555)
* bv-u32-set:                            Inlined Bytevector Instructions.
                                                            (line 48573)
* bv-u64-native-ref:                     Inlined Bytevector Instructions.
                                                            (line 48549)
* bv-u64-native-set:                     Inlined Bytevector Instructions.
                                                            (line 48567)
* bv-u64-ref:                            Inlined Bytevector Instructions.
                                                            (line 48557)
* bv-u64-set:                            Inlined Bytevector Instructions.
                                                            (line 48575)
* bv-u8-ref:                             Inlined Bytevector Instructions.
                                                            (line 48543)
* bv-u8-set:                             Inlined Bytevector Instructions.
                                                            (line 48561)
* bytecode->objcode:                     Bytecode and Objcode.
                                                            (line 49256)
* bytevector->pointer:                   Void Pointers and Byte Access.
                                                            (line 25291)
* bytevector->sint-list:                 Bytevectors and Integer Lists.
                                                            (line 10765)
* bytevector->string:                    Representing Strings as Bytes.
                                                            (line 10217)
* bytevector->string <1>:                R6RS Transcoders.  (line 21013)
* bytevector->u8-list:                   Bytevectors and Integer Lists.
                                                            (line 10750)
* bytevector->uint-list:                 Bytevectors and Integer Lists.
                                                            (line 10760)
* bytevector-copy:                       Bytevector Manipulation.
                                                            (line 10596)
* bytevector-copy!:                      Bytevector Manipulation.
                                                            (line 10587)
* bytevector-fill!:                      Bytevector Manipulation.
                                                            (line 10583)
* bytevector-ieee-double-native-ref:     Bytevectors as Floats.
                                                            (line 10807)
* bytevector-ieee-double-native-set!:    Bytevectors as Floats.
                                                            (line 10814)
* bytevector-ieee-double-ref:            Bytevectors as Floats.
                                                            (line 10788)
* bytevector-ieee-double-set!:           Bytevectors as Floats.
                                                            (line 10796)
* bytevector-ieee-single-native-ref:     Bytevectors as Floats.
                                                            (line 10806)
* bytevector-ieee-single-native-set!:    Bytevectors as Floats.
                                                            (line 10813)
* bytevector-ieee-single-ref:            Bytevectors as Floats.
                                                            (line 10787)
* bytevector-ieee-single-set!:           Bytevectors as Floats.
                                                            (line 10794)
* bytevector-length:                     Bytevector Manipulation.
                                                            (line 10571)
* bytevector-s16-native-ref:             Bytevectors as Integers.
                                                            (line 10709)
* bytevector-s16-native-set!:            Bytevectors as Integers.
                                                            (line 10725)
* bytevector-s16-ref:                    Bytevectors as Integers.
                                                            (line 10669)
* bytevector-s16-set!:                   Bytevectors as Integers.
                                                            (line 10688)
* bytevector-s32-native-ref:             Bytevectors as Integers.
                                                            (line 10711)
* bytevector-s32-native-set!:            Bytevectors as Integers.
                                                            (line 10727)
* bytevector-s32-ref:                    Bytevectors as Integers.
                                                            (line 10671)
* bytevector-s32-set!:                   Bytevectors as Integers.
                                                            (line 10690)
* bytevector-s64-native-ref:             Bytevectors as Integers.
                                                            (line 10713)
* bytevector-s64-native-set!:            Bytevectors as Integers.
                                                            (line 10729)
* bytevector-s64-ref:                    Bytevectors as Integers.
                                                            (line 10673)
* bytevector-s64-set!:                   Bytevectors as Integers.
                                                            (line 10692)
* bytevector-s8-ref:                     Bytevectors as Integers.
                                                            (line 10667)
* bytevector-s8-set!:                    Bytevectors as Integers.
                                                            (line 10686)
* bytevector-sint-ref:                   Bytevectors as Integers.
                                                            (line 10644)
* bytevector-sint-set!:                  Bytevectors as Integers.
                                                            (line 10656)
* bytevector-u16-native-ref:             Bytevectors as Integers.
                                                            (line 10708)
* bytevector-u16-native-set!:            Bytevectors as Integers.
                                                            (line 10724)
* bytevector-u16-ref:                    Bytevectors as Integers.
                                                            (line 10668)
* bytevector-u16-set!:                   Bytevectors as Integers.
                                                            (line 10687)
* bytevector-u32-native-ref:             Bytevectors as Integers.
                                                            (line 10710)
* bytevector-u32-native-set!:            Bytevectors as Integers.
                                                            (line 10726)
* bytevector-u32-ref:                    Bytevectors as Integers.
                                                            (line 10670)
* bytevector-u32-set!:                   Bytevectors as Integers.
                                                            (line 10689)
* bytevector-u64-native-ref:             Bytevectors as Integers.
                                                            (line 10712)
* bytevector-u64-native-set!:            Bytevectors as Integers.
                                                            (line 10728)
* bytevector-u64-ref:                    Bytevectors as Integers.
                                                            (line 10672)
* bytevector-u64-set!:                   Bytevectors as Integers.
                                                            (line 10691)
* bytevector-u8-ref:                     Bytevectors as Integers.
                                                            (line 10666)
* bytevector-u8-set!:                    Bytevectors as Integers.
                                                            (line 10685)
* bytevector-uint-ref:                   Bytevectors as Integers.
                                                            (line 10639)
* bytevector-uint-set!:                  Bytevectors as Integers.
                                                            (line 10649)
* bytevector=?:                          Bytevector Manipulation.
                                                            (line 10578)
* bytevector?:                           Bytevector Manipulation.
                                                            (line 10564)
* c32vector:                             SRFI-4 API.        (line 35087)
* c32vector->list:                       SRFI-4 API.        (line 35195)
* c32vector-length:                      SRFI-4 API.        (line 35115)
* c32vector-ref:                         SRFI-4 API.        (line 35141)
* c32vector-set!:                        SRFI-4 API.        (line 35168)
* c32vector?:                            SRFI-4 API.        (line 35031)
* c64vector:                             SRFI-4 API.        (line 35088)
* c64vector->list:                       SRFI-4 API.        (line 35196)
* c64vector-length:                      SRFI-4 API.        (line 35116)
* c64vector-ref:                         SRFI-4 API.        (line 35142)
* c64vector-set!:                        SRFI-4 API.        (line 35169)
* c64vector?:                            SRFI-4 API.        (line 35032)
* caaaar:                                Pairs.             (line 11869)
* caaaar <1>:                            rnrs base.         (line 38448)
* caaadr:                                Pairs.             (line 11868)
* caaadr <1>:                            rnrs base.         (line 38449)
* caaar:                                 Pairs.             (line 11853)
* caaar <1>:                             rnrs base.         (line 38440)
* caadar:                                Pairs.             (line 11867)
* caadar <1>:                            rnrs base.         (line 38450)
* caaddr:                                Pairs.             (line 11866)
* caaddr <1>:                            rnrs base.         (line 38457)
* caadr:                                 Pairs.             (line 11852)
* caadr <1>:                             rnrs base.         (line 38441)
* caar:                                  Pairs.             (line 11845)
* caar <1>:                              rnrs base.         (line 38436)
* cadaar:                                Pairs.             (line 11865)
* cadaar <1>:                            rnrs base.         (line 38451)
* cadadr:                                Pairs.             (line 11864)
* cadadr <1>:                            rnrs base.         (line 38456)
* cadar:                                 Pairs.             (line 11851)
* cadar <1>:                             rnrs base.         (line 38442)
* caddar:                                Pairs.             (line 11863)
* caddar <1>:                            rnrs base.         (line 38458)
* cadddr:                                Pairs.             (line 11862)
* cadddr <1>:                            rnrs base.         (line 38459)
* caddr:                                 Pairs.             (line 11850)
* caddr <1>:                             rnrs base.         (line 38444)
* cadr:                                  Pairs.             (line 11844)
* cadr <1>:                              rnrs base.         (line 38437)
* call:                                  Procedure Call and Return Instructions.
                                                            (line 47900)
* call-with-blocked-asyncs:              System asyncs.     (line 25705)
* call-with-current-continuation:        Continuations.     (line 18765)
* call-with-current-continuation <1>:    rnrs base.         (line 38747)
* call-with-error-handling:              Pre-Unwind Debugging.
                                                            (line 28228)
* call-with-escape-continuation:         Prompt Primitives. (line 18626)
* call-with-file-and-dir:                texinfo.           (line 43645)
* call-with-input-file:                  File Ports.        (line 20502)
* call-with-input-file <1>:              rnrs io simple.    (line 39507)
* call-with-input-string:                String Ports.      (line 20613)
* call-with-new-thread:                  Threads.           (line 25781)
* call-with-output-encoded-string:       Representing Strings as Bytes.
                                                            (line 10228)
* call-with-output-file:                 File Ports.        (line 20504)
* call-with-output-file <1>:             rnrs io simple.    (line 39508)
* call-with-output-string:               String Ports.      (line 20586)
* call-with-port:                        R6RS Port Manipulation.
                                                            (line 21116)
* call-with-prompt:                      Prompt Primitives. (line 18525)
* call-with-trace:                       Tracing Traps.     (line 28726)
* call-with-unblocked-asyncs:            System asyncs.     (line 25716)
* call-with-values:                      Multiple Values.   (line 18904)
* call-with-values <1>:                  rnrs base.         (line 38752)
* call/cc:                               Continuations.     (line 18766)
* call/cc <1>:                           rnrs base.         (line 38748)
* call/cc <2>:                           Procedure Call and Return Instructions.
                                                            (line 47990)
* call/ec:                               Prompt Primitives. (line 18627)
* call/nargs:                            Procedure Call and Return Instructions.
                                                            (line 47929)
* cancel-thread:                         Threads.           (line 25832)
* car:                                   Pairs.             (line 11827)
* car <1>:                               rnrs base.         (line 38434)
* car <2>:                               Inlined Scheme Instructions.
                                                            (line 48477)
* car+cdr:                               SRFI-1 Selectors.  (line 34143)
* case:                                  Conditionals.      (line 18311)
* case <1>:                              rnrs base.         (line 38514)
* case-lambda:                           Case-lambda.       (line 15775)
* case-lambda <1>:                       rnrs control.      (line 38945)
* case-lambda*:                          Case-lambda.       (line 15823)
* catch:                                 Catch.             (line 19051)
* cd:                                    Processes.         (line 30295)
* cdaaar:                                Pairs.             (line 11861)
* cdaaar <1>:                            rnrs base.         (line 38452)
* cdaadr:                                Pairs.             (line 11860)
* cdaadr <1>:                            rnrs base.         (line 38455)
* cdaar:                                 Pairs.             (line 11849)
* cdaar <1>:                             rnrs base.         (line 38443)
* cdadar:                                Pairs.             (line 11859)
* cdadar <1>:                            rnrs base.         (line 38454)
* cdaddr:                                Pairs.             (line 11858)
* cdaddr <1>:                            rnrs base.         (line 38460)
* cdadr:                                 Pairs.             (line 11848)
* cdadr <1>:                             rnrs base.         (line 38445)
* cdar:                                  Pairs.             (line 11843)
* cdar <1>:                              rnrs base.         (line 38438)
* cddaar:                                Pairs.             (line 11857)
* cddaar <1>:                            rnrs base.         (line 38453)
* cddadr:                                Pairs.             (line 11856)
* cddadr <1>:                            rnrs base.         (line 38461)
* cddar:                                 Pairs.             (line 11847)
* cddar <1>:                             rnrs base.         (line 38446)
* cdddar:                                Pairs.             (line 11855)
* cdddar <1>:                            rnrs base.         (line 38462)
* cddddr:                                Pairs.             (line 11854)
* cddddr <1>:                            rnrs base.         (line 38463)
* cdddr:                                 Pairs.             (line 11846)
* cdddr <1>:                             rnrs base.         (line 38447)
* cddr:                                  Pairs.             (line 11842)
* cddr <1>:                              rnrs base.         (line 38439)
* cdr:                                   Pairs.             (line 11828)
* cdr <1>:                               rnrs base.         (line 38435)
* cdr <2>:                               Inlined Scheme Instructions.
                                                            (line 48478)
* ceiling:                               Arithmetic.        (line  7917)
* ceiling <1>:                           rnrs base.         (line 38643)
* ceiling-quotient:                      Arithmetic.        (line  7978)
* ceiling-remainder:                     Arithmetic.        (line  7979)
* ceiling/:                              Arithmetic.        (line  7977)
* center-string:                         texinfo string-utils.
                                                            (line 43881)
* centered-quotient:                     Arithmetic.        (line  8025)
* centered-remainder:                    Arithmetic.        (line  8026)
* centered/:                             Arithmetic.        (line  8024)
* change-class:                          Changing the Class of an Instance.
                                                            (line 46533)
* change-class <1>:                      Changing the Class of an Instance.
                                                            (line 46535)
* char->integer:                         Characters.        (line  8623)
* char->integer <1>:                     rnrs base.         (line 38425)
* char-alphabetic?:                      Characters.        (line  8575)
* char-alphabetic? <1>:                  rnrs unicode.      (line 38790)
* char-ci<=?:                            Characters.        (line  8563)
* char-ci<=? <1>:                        rnrs unicode.      (line 38784)
* char-ci<?:                             Characters.        (line  8559)
* char-ci<? <1>:                         rnrs unicode.      (line 38782)
* char-ci=?:                             Characters.        (line  8555)
* char-ci=? <1>:                         rnrs unicode.      (line 38781)
* char-ci>=?:                            Characters.        (line  8571)
* char-ci>=? <1>:                        rnrs unicode.      (line 38785)
* char-ci>?:                             Characters.        (line  8567)
* char-ci>? <1>:                         rnrs unicode.      (line 38783)
* char-downcase:                         Characters.        (line  8637)
* char-downcase <1>:                     rnrs unicode.      (line 38768)
* char-foldcase:                         rnrs unicode.      (line 38770)
* char-general-category:                 Characters.        (line  8599)
* char-general-category <1>:             rnrs unicode.      (line 38800)
* char-is-both?:                         Characters.        (line  8595)
* char-locale-ci<?:                      Text Collation.    (line 27308)
* char-locale-ci=?:                      Text Collation.    (line 27317)
* char-locale-ci>?:                      Text Collation.    (line 27310)
* char-locale-downcase:                  Character Case Mapping.
                                                            (line 27337)
* char-locale-titlecase:                 Character Case Mapping.
                                                            (line 27347)
* char-locale-upcase:                    Character Case Mapping.
                                                            (line 27342)
* char-locale<?:                         Text Collation.    (line 27304)
* char-locale>?:                         Text Collation.    (line 27306)
* char-lower-case?:                      Characters.        (line  8591)
* char-lower-case? <1>:                  rnrs unicode.      (line 38794)
* char-numeric?:                         Characters.        (line  8579)
* char-numeric? <1>:                     rnrs unicode.      (line 38791)
* char-ready?:                           Reading.           (line 19889)
* char-set:                              Creating Character Sets.
                                                            (line  8782)
* char-set->list:                        Querying Character Sets.
                                                            (line  8882)
* char-set->string:                      Querying Character Sets.
                                                            (line  8886)
* char-set-adjoin:                       Character-Set Algebra.
                                                            (line  8915)
* char-set-adjoin!:                      Character-Set Algebra.
                                                            (line  8925)
* char-set-any:                          Querying Character Sets.
                                                            (line  8902)
* char-set-complement:                   Character-Set Algebra.
                                                            (line  8935)
* char-set-complement!:                  Character-Set Algebra.
                                                            (line  8966)
* char-set-contains?:                    Querying Character Sets.
                                                            (line  8892)
* char-set-copy:                         Creating Character Sets.
                                                            (line  8777)
* char-set-count:                        Querying Character Sets.
                                                            (line  8877)
* char-set-cursor:                       Iterating Over Character Sets.
                                                            (line  8714)
* char-set-cursor-next:                  Iterating Over Character Sets.
                                                            (line  8724)
* char-set-delete:                       Character-Set Algebra.
                                                            (line  8920)
* char-set-delete!:                      Character-Set Algebra.
                                                            (line  8930)
* char-set-diff+intersection:            Character-Set Algebra.
                                                            (line  8961)
* char-set-diff+intersection!:           Character-Set Algebra.
                                                            (line  8986)
* char-set-difference:                   Character-Set Algebra.
                                                            (line  8953)
* char-set-difference!:                  Character-Set Algebra.
                                                            (line  8978)
* char-set-every:                        Querying Character Sets.
                                                            (line  8897)
* char-set-filter:                       Creating Character Sets.
                                                            (line  8808)
* char-set-filter!:                      Creating Character Sets.
                                                            (line  8814)
* char-set-fold:                         Iterating Over Character Sets.
                                                            (line  8735)
* char-set-for-each:                     Iterating Over Character Sets.
                                                            (line  8762)
* char-set-hash:                         Character Set Predicates/Comparison.
                                                            (line  8695)
* char-set-intersection:                 Character-Set Algebra.
                                                            (line  8949)
* char-set-intersection!:                Character-Set Algebra.
                                                            (line  8974)
* char-set-map:                          Iterating Over Character Sets.
                                                            (line  8767)
* char-set-ref:                          Iterating Over Character Sets.
                                                            (line  8718)
* char-set-size:                         Querying Character Sets.
                                                            (line  8873)
* char-set-unfold:                       Iterating Over Character Sets.
                                                            (line  8740)
* char-set-unfold!:                      Iterating Over Character Sets.
                                                            (line  8751)
* char-set-union:                        Character-Set Algebra.
                                                            (line  8945)
* char-set-union!:                       Character-Set Algebra.
                                                            (line  8970)
* char-set-xor:                          Character-Set Algebra.
                                                            (line  8957)
* char-set-xor!:                         Character-Set Algebra.
                                                            (line  8982)
* char-set<=:                            Character Set Predicates/Comparison.
                                                            (line  8690)
* char-set=:                             Character Set Predicates/Comparison.
                                                            (line  8686)
* char-set?:                             Character Set Predicates/Comparison.
                                                            (line  8682)
* char-title-case?:                      rnrs unicode.      (line 38795)
* char-titlecase:                        Characters.        (line  8641)
* char-titlecase <1>:                    rnrs unicode.      (line 38769)
* char-upcase:                           Characters.        (line  8633)
* char-upcase <1>:                       rnrs unicode.      (line 38767)
* char-upper-case?:                      Characters.        (line  8587)
* char-upper-case? <1>:                  rnrs unicode.      (line 38793)
* char-whitespace?:                      Characters.        (line  8583)
* char-whitespace? <1>:                  rnrs unicode.      (line 38792)
* char<=?:                               Characters.        (line  8533)
* char<=? <1>:                           rnrs base.         (line 38422)
* char<?:                                Characters.        (line  8529)
* char<? <1>:                            rnrs base.         (line 38420)
* char=?:                                Characters.        (line  8525)
* char=? <1>:                            rnrs base.         (line 38419)
* char>=?:                               Characters.        (line  8541)
* char>=? <1>:                           rnrs base.         (line 38423)
* char>?:                                Characters.        (line  8537)
* char>? <1>:                            rnrs base.         (line 38421)
* char?:                                 Characters.        (line  8518)
* char? <1>:                             rnrs base.         (line 38418)
* chdir:                                 Processes.         (line 30295)
* chmod:                                 File System.       (line 29676)
* chown:                                 File System.       (line 29663)
* chroot:                                Processes.         (line 30314)
* circular-list:                         SRFI-1 Constructors.
                                                            (line 34051)
* circular-list?:                        SRFI-1 Predicates. (line 34080)
* class:                                 Class Definition Protocol.
                                                            (line 45965)
* class-direct-methods:                  Classes.           (line 45225)
* class-direct-slots:                    Classes.           (line 45217)
* class-direct-subclasses:               Classes.           (line 45221)
* class-direct-supers:                   Classes.           (line 45213)
* class-methods:                         Classes.           (line 45242)
* class-name:                            Classes.           (line 45209)
* class-of:                              Instances.         (line 45249)
* class-of <1>:                          Inlined Scheme Instructions.
                                                            (line 48485)
* class-precedence-list:                 Classes.           (line 45230)
* class-redefinition:                    Customizing Class Redefinition.
                                                            (line 46464)
* class-redefinition <1>:                Customizing Class Redefinition.
                                                            (line 46469)
* class-slot-definition:                 Slots.             (line 45282)
* class-slot-ref:                        Accessing Slots.   (line 45474)
* class-slot-set!:                       Accessing Slots.   (line 45485)
* class-slots:                           Classes.           (line 45234)
* class-subclasses:                      Classes.           (line 45239)
* clear-value-history!:                  Value History.     (line  3581)
* close:                                 Ports and File Descriptors.
                                                            (line 29294)
* close-fdes:                            Ports and File Descriptors.
                                                            (line 29302)
* close-input-port:                      Closing.           (line 20062)
* close-input-port <1>:                  rnrs io simple.    (line 39516)
* close-output-port:                     Closing.           (line 20063)
* close-output-port <1>:                 rnrs io simple.    (line 39517)
* close-pipe:                            Pipes.             (line 30946)
* close-port:                            Closing.           (line 20054)
* close-server:                          Web Server.        (line 33347)
* closedir:                              File System.       (line 29789)
* collapse-repeated-chars:               texinfo string-utils.
                                                            (line 43910)
* command-line:                          Runtime Environment.
                                                            (line 30193)
* command-line <1>:                      rnrs programs.     (line 39560)
* compile:                               Compile Commands.  (line  3680)
* compile <1>:                           Compilation.       (line 22831)
* compile-file:                          Compile Commands.  (line  3683)
* compile-file <1>:                      Compilation.       (line 22840)
* compiled-file-name:                    Compilation.       (line 22857)
* complex?:                              Complex Numbers.   (line  7515)
* complex? <1>:                          rnrs base.         (line 38529)
* compose:                               Higher-Order Functions.
                                                            (line 15907)
* compute-std-cpl:                       Customizing Class Definition.
                                                            (line 46145)
* concatenate:                           SRFI-1 Length Append etc.
                                                            (line 34186)
* concatenate!:                          SRFI-1 Length Append etc.
                                                            (line 34187)
* cond:                                  Conditionals.      (line 18273)
* cond <1>:                              rnrs base.         (line 38513)
* cond-expand:                           SRFI-0.            (line 33937)
* condition:                             SRFI-35.           (line 36621)
* condition <1>:                         rnrs conditions.   (line 39294)
* condition-accessor:                    rnrs conditions.   (line 39306)
* condition-has-type?:                   SRFI-35.           (line 36581)
* condition-irritants:                   rnrs conditions.   (line 39361)
* condition-message:                     SRFI-35.           (line 36652)
* condition-message <1>:                 rnrs conditions.   (line 39326)
* condition-predicate:                   rnrs conditions.   (line 39305)
* condition-ref:                         SRFI-35.           (line 36584)
* condition-type?:                       SRFI-35.           (line 36561)
* condition-variable-broadcast!:         SRFI-18 Condition variables.
                                                            (line 35799)
* condition-variable-name:               SRFI-18 Condition variables.
                                                            (line 35788)
* condition-variable-signal!:            SRFI-18 Condition variables.
                                                            (line 35798)
* condition-variable-specific:           SRFI-18 Condition variables.
                                                            (line 35792)
* condition-variable-specific-set!:      SRFI-18 Condition variables.
                                                            (line 35793)
* condition-variable?:                   Mutexes and Condition Variables.
                                                            (line 26010)
* condition-variable? <1>:               SRFI-18 Condition variables.
                                                            (line 35778)
* condition-who:                         rnrs conditions.   (line 39368)
* condition?:                            rnrs conditions.   (line 39291)
* connect:                               Network Sockets and Communication.
                                                            (line 31688)
* connect <1>:                           Network Sockets and Communication.
                                                            (line 31689)
* connect <2>:                           Network Sockets and Communication.
                                                            (line 31690)
* connect <3>:                           Network Sockets and Communication.
                                                            (line 31692)
* cons:                                  Pairs.             (line 11802)
* cons <1>:                              rnrs base.         (line 38433)
* cons <2>:                              Inlined Scheme Instructions.
                                                            (line 48476)
* cons*:                                 List Constructors. (line 12014)
* cons* <1>:                             rnrs lists.        (line 38890)
* cons* <2>:                             rnrs lists.        (line 38891)
* cons-source:                           Source Properties. (line 27978)
* const:                                 Higher-Order Functions.
                                                            (line 15887)
* continuation-call:                     Trampoline Instructions.
                                                            (line 48147)
* continue:                              while do.          (line 18440)
* copy-bit:                              SRFI-60.           (line 37918)
* copy-bit-field:                        SRFI-60.           (line 37925)
* copy-file:                             File System.       (line 29705)
* copy-random-state:                     Random.            (line  8319)
* copy-time:                             SRFI-19 Time.      (line 35992)
* copy-tree:                             Copying.           (line 17537)
* cos:                                   Scientific.        (line  8115)
* cos <1>:                               rnrs base.         (line 38545)
* cosh:                                  Scientific.        (line  8144)
* count:                                 SRFI-1 Length Append etc.
                                                            (line 34225)
* coverage-data->lcov:                   Code Coverage.     (line 28925)
* coverage-data?:                        Code Coverage.     (line 28921)
* crypt:                                 Encryption.        (line 31973)
* ctermid:                               Terminals and Ptys.
                                                            (line 30858)
* current-date:                          SRFI-19 Date.      (line 36092)
* current-dynamic-state:                 Fluids and Dynamic States.
                                                            (line 26290)
* current-error-port:                    Default Ports.     (line 20347)
* current-error-port <1>:                R6RS Output Ports. (line 21445)
* current-exception-handler:             SRFI-18 Exceptions.
                                                            (line 35844)
* current-filename:                      Source Properties. (line 27969)
* current-http-proxy:                    Web Client.        (line 33203)
* current-input-port:                    Default Ports.     (line 20315)
* current-input-port <1>:                R6RS Input Ports.  (line 21168)
* current-julian-day:                    SRFI-19 Date.      (line 36097)
* current-load-port:                     Loading.           (line 22948)
* current-modified-julian-day:           SRFI-19 Date.      (line 36100)
* current-module:                        Module System Reflection.
                                                            (line 24455)
* current-output-port:                   Default Ports.     (line 20332)
* current-output-port <1>:               R6RS Output Ports. (line 21444)
* current-processor-count:               Processes.         (line 30657)
* current-source-location:               Source Properties. (line 27965)
* current-ssax-error-port:               SSAX.              (line 43117)
* current-thread:                        Threads.           (line 25777)
* current-thread <1>:                    SRFI-18 Threads.   (line 35639)
* current-time:                          Time.              (line 30022)
* current-time <1>:                      SRFI-18 Time.      (line 35816)
* current-time <2>:                      SRFI-19 Time.      (line 35995)
* cut:                                   SRFI-26.           (line 36302)
* cute:                                  SRFI-26.           (line 36303)
* date->julian-day:                      SRFI-19 Time/Date conversions.
                                                            (line 36106)
* date->modified-julian-day:             SRFI-19 Time/Date conversions.
                                                            (line 36107)
* date->string:                          SRFI-19 Date to string.
                                                            (line 36164)
* date->time-monotonic:                  SRFI-19 Time/Date conversions.
                                                            (line 36108)
* date->time-tai:                        SRFI-19 Time/Date conversions.
                                                            (line 36109)
* date->time-utc:                        SRFI-19 Time/Date conversions.
                                                            (line 36110)
* date-day:                              SRFI-19 Date.      (line 36068)
* date-hour:                             SRFI-19 Date.      (line 36065)
* date-minute:                           SRFI-19 Date.      (line 36062)
* date-month:                            SRFI-19 Date.      (line 36071)
* date-nanosecond:                       SRFI-19 Date.      (line 36054)
* date-second:                           SRFI-19 Date.      (line 36057)
* date-week-day:                         SRFI-19 Date.      (line 36084)
* date-week-number:                      SRFI-19 Date.      (line 36087)
* date-year:                             SRFI-19 Date.      (line 36074)
* date-year-day:                         SRFI-19 Date.      (line 36081)
* date-zone-offset:                      SRFI-19 Date.      (line 36078)
* date?:                                 SRFI-19 Date.      (line 36047)
* datum->random-state:                   Random.            (line  8372)
* datum->syntax:                         Syntax Case.       (line 16653)
* datum->syntax <1>:                     rnrs syntax-case.  (line 39963)
* debug-disable:                         Debug Options.     (line 28294)
* debug-enable:                          Debug Options.     (line 28293)
* debug-options:                         Debug Options.     (line 28268)
* debug-set!:                            Debug Options.     (line 28295)
* declare-default-port!:                 URIs.              (line 32194)
* declare-header!:                       HTTP.              (line 32317)
* declare-opaque-header!:                HTTP.              (line 32336)
* deep-clone:                            GOOPS Object Miscellany.
                                                            (line 45581)
* deep-clone <1>:                        GOOPS Object Miscellany.
                                                            (line 45582)
* default-duplicate-binding-handler:     Creating Guile Modules.
                                                            (line 24129)
* default-prompt-tag:                    Prompt Primitives. (line 18542)
* default-random-source:                 SRFI-27 Default Random Source.
                                                            (line 36401)
* define:                                Top Level.         (line 17918)
* define <1>:                            rnrs base.         (line 38475)
* define <2>:                            Curried Definitions.
                                                            (line 42550)
* define <3>:                            Top-Level Environment Instructions.
                                                            (line 47860)
* define*:                               lambda* and define*.
                                                            (line 15609)
* define* <1>:                           Curried Definitions.
                                                            (line 42551)
* define*-public:                        ice-9 optargs.     (line 15753)
* define-accessor:                       Accessors.         (line 44732)
* define-class:                          Class Definition.  (line 44178)
* define-class <1>:                      Class Definition.  (line 44191)
* define-condition-type:                 SRFI-35.           (line 36603)
* define-condition-type <1>:             rnrs conditions.   (line 39310)
* define-enumeration:                    rnrs enums.        (line 40164)
* define-generic:                        Methods and Generic Functions.
                                                            (line 44662)
* define-generic <1>:                    Methods and Generic Functions.
                                                            (line 44664)
* define-immutable-record-type:          SRFI-9 Records.    (line 13699)
* define-inlinable:                      Inlinable Procedures.
                                                            (line 16089)
* define-language:                       Compiler Tower.    (line 48615)
* define-macro:                          Defmacros.         (line 16925)
* define-method:                         Methods and Generic Functions.
                                                            (line 44662)
* define-method <1>:                     Methods and Generic Functions.
                                                            (line 44673)
* define-module:                         Creating Guile Modules.
                                                            (line 23987)
* define-once:                           Top Level.         (line 17953)
* define-parsed-entity!:                 SSAX.              (line 43144)
* define-public:                         Creating Guile Modules.
                                                            (line 24148)
* define-public <1>:                     Curried Definitions.
                                                            (line 42552)
* define-reader-ctor:                    SRFI-10.           (line 35434)
* define-record-type:                    SRFI-9 Records.    (line 13599)
* define-record-type <1>:                rnrs records syntactic.
                                                            (line 39026)
* define-server-impl:                    Web Server.        (line 33278)
* define-stream:                         SRFI-41 Stream Library.
                                                            (line 36989)
* define-syntax:                         Defining Macros.   (line 16142)
* define-syntax <1>:                     rnrs base.         (line 38479)
* define-syntax-parameter:               Syntax Parameters. (line 17078)
* define-syntax-rule:                    Syntax Rules.      (line 16399)
* define-values:                         Binding Multiple Values.
                                                            (line 18140)
* define-wrapped-pointer-type:           Void Pointers and Byte Access.
                                                            (line 25325)
* defined?:                              Binding Reflection.
                                                            (line 18132)
* defmacro:                              Defmacros.         (line 16925)
* defmacro*:                             ice-9 optargs.     (line 15756)
* defmacro*-public:                      ice-9 optargs.     (line 15757)
* defvar:                                Top Level.         (line 17953)
* delay:                                 Delayed Evaluation.
                                                            (line 23167)
* delay <1>:                             SRFI-45.           (line 37764)
* delay <2>:                             rnrs r5rs.         (line 40251)
* delete:                                List Modification. (line 12148)
* delete <1>:                            SRFI-1 Deleting.   (line 34587)
* delete!:                               List Modification. (line 12160)
* delete! <1>:                           SRFI-1 Deleting.   (line 34588)
* delete-duplicates:                     SRFI-1 Deleting.   (line 34611)
* delete-duplicates!:                    SRFI-1 Deleting.   (line 34612)
* delete-file:                           File System.       (line 29701)
* delete-trap!:                          Trap States.       (line 28786)
* delete1!:                              List Modification. (line 12182)
* delq:                                  List Modification. (line 12136)
* delq!:                                 List Modification. (line 12158)
* delq1!:                                List Modification. (line 12170)
* delv:                                  List Modification. (line 12142)
* delv!:                                 List Modification. (line 12159)
* delv1!:                                List Modification. (line 12176)
* denominator:                           Reals and Rationals.
                                                            (line  7463)
* denominator <1>:                       rnrs base.         (line 38555)
* deq!:                                  Queues.            (line 41809)
* dereference-pointer:                   Void Pointers and Byte Access.
                                                            (line 25299)
* describe:                              Help Commands.     (line  3644)
* directory-stream?:                     File System.       (line 29773)
* dirname:                               File System.       (line 29864)
* disable-trap!:                         Trap States.       (line 28783)
* disable-value-history!:                Value History.     (line  3578)
* disassemble:                           Compile Commands.  (line  3692)
* disassemble-file:                      Compile Commands.  (line  3695)
* display:                               Scheme Write.      (line 22571)
* display <1>:                           rnrs io simple.    (line 39533)
* display <2>:                           rnrs io simple.    (line 39534)
* display <3>:                           GOOPS Object Miscellany.
                                                            (line 45594)
* display-application:                   Frames.            (line 27885)
* display-backtrace:                     Stacks.            (line 27828)
* display-error:                         Handling Errors.   (line 19582)
* div:                                   rnrs base.         (line 38647)
* div <1>:                               Inlined Mathematical Instructions.
                                                            (line 48511)
* div-and-mod:                           rnrs base.         (line 38649)
* div0:                                  rnrs base.         (line 38666)
* div0-and-mod0:                         rnrs base.         (line 38668)
* do:                                    while do.          (line 18376)
* do <1>:                                rnrs control.      (line 38940)
* dotted-list?:                          SRFI-1 Predicates. (line 34093)
* doubly-weak-hash-table?:               Weak hash tables.  (line 23698)
* down:                                  Debug Commands.    (line  3733)
* drain-input:                           Reading.           (line 19956)
* drop:                                  SRFI-1 Selectors.  (line 34153)
* drop <1>:                              Miscellaneous Instructions.
                                                            (line 48436)
* drop-right:                            SRFI-1 Selectors.  (line 34160)
* drop-right!:                           SRFI-1 Selectors.  (line 34161)
* drop-while:                            SRFI-1 Searching.  (line 34507)
* dup:                                   Ports and File Descriptors.
                                                            (line 29363)
* dup <1>:                               Miscellaneous Instructions.
                                                            (line 48439)
* dup->fdes:                             Ports and File Descriptors.
                                                            (line 29351)
* dup->inport:                           Ports and File Descriptors.
                                                            (line 29357)
* dup->outport:                          Ports and File Descriptors.
                                                            (line 29360)
* dup->port:                             Ports and File Descriptors.
                                                            (line 29367)
* dup2:                                  Ports and File Descriptors.
                                                            (line 29398)
* duplicate-port:                        Ports and File Descriptors.
                                                            (line 29371)
* dynamic-call:                          Foreign Functions. (line 24876)
* dynamic-func:                          Foreign Functions. (line 24862)
* dynamic-link:                          Foreign Libraries. (line 24799)
* dynamic-object?:                       Foreign Libraries. (line 24821)
* dynamic-pointer:                       Foreign Variables. (line 25193)
* dynamic-state?:                        Fluids and Dynamic States.
                                                            (line 26281)
* dynamic-unlink:                        Foreign Libraries. (line 24825)
* dynamic-wind:                          Dynamic Wind.      (line 19424)
* dynamic-wind <1>:                      rnrs base.         (line 38755)
* eager:                                 SRFI-45.           (line 37783)
* ee?:                                   Inlined Mathematical Instructions.
                                                            (line 48515)
* effective-version:                     Build Config.      (line 26653)
* eighth:                                SRFI-1 Selectors.  (line 34138)
* empty-box:                             Lexical Environment Instructions.
                                                            (line 47754)
* enable-primitive-generic!:             Extending Primitives.
                                                            (line 44754)
* enable-trap!:                          Trap States.       (line 28780)
* enable-value-history!:                 Value History.     (line  3575)
* encode-and-join-uri-path:              URIs.              (line 32238)
* end-of-char-set?:                      Iterating Over Character Sets.
                                                            (line  8730)
* endgrent:                              User Information.  (line 29994)
* endhostent:                            Network Databases. (line 31287)
* endianness:                            Bytevector Endianness.
                                                            (line 10536)
* endnetent:                             Network Databases. (line 31337)
* endprotoent:                           Network Databases. (line 31384)
* endpwent:                              User Information.  (line 29951)
* endservent:                            Network Databases. (line 31445)
* enq!:                                  Queues.            (line 41806)
* ensure-accessor:                       Generic Function Internals.
                                                            (line 46344)
* ensure-generic:                        Generic Function Internals.
                                                            (line 46319)
* ensure-metaclass:                      Class Definition Protocol.
                                                            (line 46006)
* enum-set->list:                        rnrs enums.        (line 40133)
* enum-set-complement:                   rnrs enums.        (line 40156)
* enum-set-constructor:                  rnrs enums.        (line 40127)
* enum-set-difference:                   rnrs enums.        (line 40152)
* enum-set-indexer:                      rnrs enums.        (line 40122)
* enum-set-intersection:                 rnrs enums.        (line 40151)
* enum-set-member?:                      rnrs enums.        (line 40138)
* enum-set-projection:                   rnrs enums.        (line 40160)
* enum-set-subset?:                      rnrs enums.        (line 40139)
* enum-set-union:                        rnrs enums.        (line 40150)
* enum-set-universe:                     rnrs enums.        (line 40118)
* enum-set=?:                            rnrs enums.        (line 40140)
* environ:                               Runtime Environment.
                                                            (line 30270)
* environment:                           rnrs eval.         (line 40203)
* eof-object:                            R6RS End-of-File.  (line 21035)
* eof-object <1>:                        rnrs io simple.    (line 39497)
* eof-object?:                           Reading.           (line 19885)
* eof-object? <1>:                       R6RS End-of-File.  (line 21029)
* eof-object? <2>:                       rnrs io simple.    (line 39498)
* eol-style:                             R6RS Transcoders.  (line 20873)
* eq?:                                   Equality.          (line 17275)
* eq? <1>:                               rnrs base.         (line 38521)
* eq? <2>:                               Inlined Scheme Instructions.
                                                            (line 48466)
* equal-hash:                            rnrs hashtables.   (line 40085)
* equal?:                                Equality.          (line 17334)
* equal? <1>:                            rnrs base.         (line 38523)
* equal? <2>:                            Inlined Scheme Instructions.
                                                            (line 48471)
* eqv?:                                  Equality.          (line 17318)
* eqv? <1>:                              rnrs base.         (line 38522)
* eqv? <2>:                              Inlined Scheme Instructions.
                                                            (line 48470)
* error:                                 Debug Commands.    (line  3754)
* error <1>:                             Error Reporting.   (line 19326)
* error <2>:                             rnrs base.         (line 38714)
* error-handling-mode:                   R6RS Transcoders.  (line 20948)
* error-message:                         Debug Commands.    (line  3753)
* error?:                                SRFI-35.           (line 36667)
* error? <1>:                            rnrs conditions.   (line 39343)
* escape-special-chars:                  texinfo string-utils.
                                                            (line 43820)
* euclidean-quotient:                    Arithmetic.        (line  7927)
* euclidean-remainder:                   Arithmetic.        (line  7928)
* euclidean/:                            Arithmetic.        (line  7926)
* eval:                                  Fly Evaluation.    (line 22621)
* eval <1>:                              rnrs eval.         (line 40197)
* eval-string:                           Fly Evaluation.    (line 22649)
* eval-when:                             Eval When.         (line 17170)
* eval-when <1>:                         Loading.           (line 22928)
* even?:                                 Integer Operations.
                                                            (line  7674)
* even? <1>:                             rnrs base.         (line 38571)
* every:                                 SRFI-1 Searching.  (line 34542)
* exact:                                 rnrs base.         (line 38561)
* exact->inexact:                        Exactness.         (line  7590)
* exact->inexact <1>:                    rnrs r5rs.         (line 40240)
* exact-integer-sqrt:                    Integer Operations.
                                                            (line  7727)
* exact-integer-sqrt <1>:                rnrs base.         (line 38574)
* exact-integer?:                        Integers.          (line  7211)
* exact?:                                Exactness.         (line  7541)
* exact? <1>:                            rnrs base.         (line 38559)
* execl:                                 Processes.         (line 30534)
* execle:                                Processes.         (line 30559)
* execlp:                                Processes.         (line 30549)
* exists:                                rnrs lists.        (line 38843)
* exit:                                  Processes.         (line 30502)
* exit <1>:                              rnrs programs.     (line 39564)
* exp:                                   Scientific.        (line  8131)
* exp <1>:                               rnrs base.         (line 38541)
* expand:                                Compile Commands.  (line  3686)
* expand-tabs:                           texinfo string-utils.
                                                            (line 43873)
* expect:                                Expect.            (line 42145)
* expect-strings:                        Expect.            (line 42056)
* export:                                Creating Guile Modules.
                                                            (line 24141)
* export!:                               Creating Guile Modules.
                                                            (line 24157)
* expt:                                  Scientific.        (line  8109)
* expt <1>:                              rnrs base.         (line 38542)
* extract-condition:                     SRFI-35.           (line 36592)
* f32vector:                             SRFI-4 API.        (line 35085)
* f32vector->list:                       SRFI-4 API.        (line 35193)
* f32vector-length:                      SRFI-4 API.        (line 35113)
* f32vector-ref:                         SRFI-4 API.        (line 35139)
* f32vector-set!:                        SRFI-4 API.        (line 35166)
* f32vector?:                            SRFI-4 API.        (line 35029)
* f64vector:                             SRFI-4 API.        (line 35086)
* f64vector->list:                       SRFI-4 API.        (line 35194)
* f64vector-length:                      SRFI-4 API.        (line 35114)
* f64vector-ref:                         SRFI-4 API.        (line 35140)
* f64vector-set!:                        SRFI-4 API.        (line 35167)
* f64vector?:                            SRFI-4 API.        (line 35030)
* false-if-exception:                    Error Reporting.   (line 19354)
* fchmod:                                File System.       (line 29676)
* fchown:                                File System.       (line 29663)
* fcntl:                                 Ports and File Descriptors.
                                                            (line 29443)
* fdes->inport:                          Ports and File Descriptors.
                                                            (line 29230)
* fdes->outport:                         Ports and File Descriptors.
                                                            (line 29235)
* fdes->ports:                           Ports and File Descriptors.
                                                            (line 29225)
* fdopen:                                Ports and File Descriptors.
                                                            (line 29218)
* feature?:                              Feature Manipulation.
                                                            (line 26762)
* fflush:                                Writing.           (line 20036)
* fifth:                                 SRFI-1 Selectors.  (line 34135)
* file-encoding:                         Character Encoding of Source Files.
                                                            (line 23147)
* file-exists?:                          File System.       (line 29878)
* file-name-separator?:                  File System.       (line 29895)
* file-options:                          R6RS File Options. (line 20761)
* file-port?:                            File Ports.        (line 20564)
* file-system-fold:                      File Tree Walk.    (line 41552)
* file-system-tree:                      File Tree Walk.    (line 41490)
* filename-completion-function:          Readline Functions.
                                                            (line 40625)
* fileno:                                Ports and File Descriptors.
                                                            (line 29209)
* fill-string:                           texinfo string-utils.
                                                            (line 43972)
* filter:                                List Modification. (line 12188)
* filter <1>:                            rnrs lists.        (line 38849)
* filter <2>:                            SXPath.            (line 43462)
* filter!:                               List Modification. (line 12189)
* filter-empty-elements:                 texinfo docbook.   (line 43734)
* filter-map:                            SRFI-1 Fold and Map.
                                                            (line 34442)
* find:                                  SRFI-1 Searching.  (line 34491)
* find <1>:                              rnrs lists.        (line 38838)
* find-string-from-port?:                sxml ssax input-parse.
                                                            (line 43565)
* find-tail:                             SRFI-1 Searching.  (line 34495)
* finish:                                Debug Commands.    (line  3796)
* finite?:                               Reals and Rationals.
                                                            (line  7446)
* finite? <1>:                           rnrs base.         (line 38703)
* first:                                 SRFI-1 Selectors.  (line 34131)
* first-set-bit:                         SRFI-60.           (line 37910)
* fix-closure:                           Lexical Environment Instructions.
                                                            (line 47788)
* fixnum->flonum:                        rnrs arithmetic flonums.
                                                            (line 39845)
* fixnum-width:                          rnrs arithmetic fixnums.
                                                            (line 39588)
* fixnum?:                               rnrs arithmetic fixnums.
                                                            (line 39585)
* fl*:                                   rnrs arithmetic flonums.
                                                            (line 39768)
* fl+:                                   rnrs arithmetic flonums.
                                                            (line 39767)
* fl-:                                   rnrs arithmetic flonums.
                                                            (line 39771)
* fl- <1>:                               rnrs arithmetic flonums.
                                                            (line 39772)
* fl/:                                   rnrs arithmetic flonums.
                                                            (line 39773)
* fl/ <1>:                               rnrs arithmetic flonums.
                                                            (line 39774)
* fl<=?:                                 rnrs arithmetic flonums.
                                                            (line 39738)
* fl<?:                                  rnrs arithmetic flonums.
                                                            (line 39737)
* fl=?:                                  rnrs arithmetic flonums.
                                                            (line 39736)
* fl>=?:                                 rnrs arithmetic flonums.
                                                            (line 39740)
* fl>?:                                  rnrs arithmetic flonums.
                                                            (line 39739)
* flabs:                                 rnrs arithmetic flonums.
                                                            (line 39780)
* flacos:                                rnrs arithmetic flonums.
                                                            (line 39812)
* flasin:                                rnrs arithmetic flonums.
                                                            (line 39811)
* flatan:                                rnrs arithmetic flonums.
                                                            (line 39813)
* flatan <1>:                            rnrs arithmetic flonums.
                                                            (line 39814)
* flceiling:                             rnrs arithmetic flonums.
                                                            (line 39798)
* flcos:                                 rnrs arithmetic flonums.
                                                            (line 39809)
* fldenominator:                         rnrs arithmetic flonums.
                                                            (line 39793)
* fldiv:                                 rnrs arithmetic flonums.
                                                            (line 39784)
* fldiv-and-mod:                         rnrs arithmetic flonums.
                                                            (line 39783)
* fldiv0:                                rnrs arithmetic flonums.
                                                            (line 39787)
* fldiv0-and-mod0:                       rnrs arithmetic flonums.
                                                            (line 39786)
* fldmod:                                rnrs arithmetic flonums.
                                                            (line 39785)
* fleven?:                               rnrs arithmetic flonums.
                                                            (line 39751)
* flexp:                                 rnrs arithmetic flonums.
                                                            (line 39805)
* flexpt:                                rnrs arithmetic flonums.
                                                            (line 39823)
* flfinite?:                             rnrs arithmetic flonums.
                                                            (line 39757)
* flfloor:                               rnrs arithmetic flonums.
                                                            (line 39797)
* flinfinite?:                           rnrs arithmetic flonums.
                                                            (line 39758)
* flinteger?:                            rnrs arithmetic flonums.
                                                            (line 39746)
* fllog:                                 rnrs arithmetic flonums.
                                                            (line 39806)
* fllog <1>:                             rnrs arithmetic flonums.
                                                            (line 39807)
* flmax:                                 rnrs arithmetic flonums.
                                                            (line 39763)
* flmin:                                 rnrs arithmetic flonums.
                                                            (line 39764)
* flmod0:                                rnrs arithmetic flonums.
                                                            (line 39788)
* flnan?:                                rnrs arithmetic flonums.
                                                            (line 39759)
* flnegative?:                           rnrs arithmetic flonums.
                                                            (line 39749)
* flnumerator:                           rnrs arithmetic flonums.
                                                            (line 39792)
* flock:                                 Ports and File Descriptors.
                                                            (line 29489)
* flodd?:                                rnrs arithmetic flonums.
                                                            (line 39750)
* flonum?:                               rnrs arithmetic flonums.
                                                            (line 39729)
* floor:                                 Arithmetic.        (line  7913)
* floor <1>:                             rnrs base.         (line 38642)
* floor-quotient:                        Arithmetic.        (line  7953)
* floor-remainder:                       Arithmetic.        (line  7954)
* floor/:                                Arithmetic.        (line  7952)
* flpositive?:                           rnrs arithmetic flonums.
                                                            (line 39748)
* flround:                               rnrs arithmetic flonums.
                                                            (line 39800)
* flsin:                                 rnrs arithmetic flonums.
                                                            (line 39808)
* flsqrt:                                rnrs arithmetic flonums.
                                                            (line 39819)
* fltan:                                 rnrs arithmetic flonums.
                                                            (line 39810)
* fltruncate:                            rnrs arithmetic flonums.
                                                            (line 39799)
* fluid->parameter:                      Parameters.        (line 26403)
* fluid-bound?:                          Fluids and Dynamic States.
                                                            (line 26227)
* fluid-ref:                             Fluids and Dynamic States.
                                                            (line 26213)
* fluid-ref <1>:                         Dynamic Environment Instructions.
                                                            (line 48371)
* fluid-set:                             Dynamic Environment Instructions.
                                                            (line 48374)
* fluid-set!:                            Fluids and Dynamic States.
                                                            (line 26219)
* fluid-unset!:                          Fluids and Dynamic States.
                                                            (line 26223)
* fluid?:                                Fluids and Dynamic States.
                                                            (line 26209)
* flush-all-ports:                       Writing.           (line 20046)
* flush-output-port:                     R6RS Output Ports. (line 21403)
* flzero?:                               rnrs arithmetic flonums.
                                                            (line 39747)
* fold:                                  SRFI-1 Fold and Map.
                                                            (line 34240)
* fold-layout:                           SXML Tree Fold.    (line 43298)
* fold-left:                             rnrs lists.        (line 38855)
* fold-matches:                          Regexp Functions.  (line 21995)
* fold-right:                            SRFI-1 Fold and Map.
                                                            (line 34241)
* fold-right <1>:                        rnrs lists.        (line 38856)
* fold-values:                           SXML Tree Fold.    (line 43288)
* foldt:                                 SXML Tree Fold.    (line 43274)
* foldts:                                Transforming SXML. (line 43252)
* foldts <1>:                            SXML Tree Fold.    (line 43279)
* foldts*:                               SXML Tree Fold.    (line 43283)
* foldts*-values:                        SXML Tree Fold.    (line 43293)
* for-all:                               rnrs lists.        (line 38842)
* for-each:                              List Mapping.      (line 12252)
* for-each <1>:                          SRFI-1 Fold and Map.
                                                            (line 34402)
* for-each <2>:                          rnrs base.         (line 38587)
* force:                                 Delayed Evaluation.
                                                            (line 23175)
* force <1>:                             SRFI-45.           (line 37776)
* force <2>:                             rnrs r5rs.         (line 40252)
* force-output:                          Writing.           (line 20036)
* foreign-call:                          Trampoline Instructions.
                                                            (line 48141)
* format:                                Formatted Output.  (line 40758)
* fourth:                                SRFI-1 Selectors.  (line 34134)
* frame:                                 Debug Commands.    (line  3739)
* frame-address:                         Frames.            (line 27861)
* frame-arguments:                       Frames.            (line 27857)
* frame-dynamic-link:                    Frames.            (line 27868)
* frame-instruction-pointer:             Frames.            (line 27862)
* frame-local-ref:                       Frames.            (line 27877)
* frame-local-set!:                      Frames.            (line 27878)
* frame-mv-return-address:               Frames.            (line 27870)
* frame-num-locals:                      Frames.            (line 27876)
* frame-previous:                        Frames.            (line 27847)
* frame-procedure:                       Frames.            (line 27852)
* frame-return-address:                  Frames.            (line 27869)
* frame-stack-pointer:                   Frames.            (line 27863)
* frame?:                                Frames.            (line 27843)
* free-boxed-ref:                        Lexical Environment Instructions.
                                                            (line 47768)
* free-boxed-set:                        Lexical Environment Instructions.
                                                            (line 47769)
* free-identifier=?:                     Syntax Transformer Helpers.
                                                            (line 16796)
* free-identifier=? <1>:                 rnrs syntax-case.  (line 39948)
* free-ref:                              Lexical Environment Instructions.
                                                            (line 47764)
* fstat:                                 File System.       (line 29587)
* fsync:                                 Ports and File Descriptors.
                                                            (line 29259)
* ftell:                                 Random Access.     (line 20099)
* ftruncate:                             Random Access.     (line 20106)
* ftw:                                   File Tree Walk.    (line 41638)
* future:                                Futures.           (line 26502)
* future?:                               Futures.           (line 26518)
* fx*:                                   rnrs arithmetic fixnums.
                                                            (line 39619)
* fx*/carry:                             rnrs arithmetic fixnums.
                                                            (line 39653)
* fx+:                                   rnrs arithmetic fixnums.
                                                            (line 39618)
* fx+/carry:                             rnrs arithmetic fixnums.
                                                            (line 39639)
* fx-:                                   rnrs arithmetic fixnums.
                                                            (line 39622)
* fx- <1>:                               rnrs arithmetic fixnums.
                                                            (line 39623)
* fx-/carry:                             rnrs arithmetic fixnums.
                                                            (line 39646)
* fx<=?:                                 rnrs arithmetic fixnums.
                                                            (line 39599)
* fx<?:                                  rnrs arithmetic fixnums.
                                                            (line 39597)
* fx=?:                                  rnrs arithmetic fixnums.
                                                            (line 39595)
* fx>=?:                                 rnrs arithmetic fixnums.
                                                            (line 39598)
* fx>?:                                  rnrs arithmetic fixnums.
                                                            (line 39596)
* fxand:                                 rnrs arithmetic fixnums.
                                                            (line 39661)
* fxarithmetic-shift:                    rnrs arithmetic fixnums.
                                                            (line 39702)
* fxarithmetic-shift-left:               rnrs arithmetic fixnums.
                                                            (line 39703)
* fxarithmetic-shift-right:              rnrs arithmetic fixnums.
                                                            (line 39704)
* fxbit-count:                           rnrs arithmetic fixnums.
                                                            (line 39673)
* fxbit-field:                           rnrs arithmetic fixnums.
                                                            (line 39692)
* fxbit-set?:                            rnrs arithmetic fixnums.
                                                            (line 39684)
* fxcopy-bit:                            rnrs arithmetic fixnums.
                                                            (line 39688)
* fxcopy-bit-field:                      rnrs arithmetic fixnums.
                                                            (line 39697)
* fxdiv:                                 rnrs arithmetic fixnums.
                                                            (line 39631)
* fxdiv-and-mod:                         rnrs arithmetic fixnums.
                                                            (line 39630)
* fxdiv0:                                rnrs arithmetic fixnums.
                                                            (line 39634)
* fxdiv0-and-mod0:                       rnrs arithmetic fixnums.
                                                            (line 39633)
* fxeven?:                               rnrs arithmetic fixnums.
                                                            (line 39609)
* fxfirst-bit-set:                       rnrs arithmetic fixnums.
                                                            (line 39680)
* fxif:                                  rnrs arithmetic fixnums.
                                                            (line 39668)
* fxior:                                 rnrs arithmetic fixnums.
                                                            (line 39662)
* fxlength:                              rnrs arithmetic fixnums.
                                                            (line 39677)
* fxmax:                                 rnrs arithmetic fixnums.
                                                            (line 39614)
* fxmin:                                 rnrs arithmetic fixnums.
                                                            (line 39615)
* fxmod:                                 rnrs arithmetic fixnums.
                                                            (line 39632)
* fxmod0:                                rnrs arithmetic fixnums.
                                                            (line 39635)
* fxnegative?:                           rnrs arithmetic fixnums.
                                                            (line 39607)
* fxnot:                                 rnrs arithmetic fixnums.
                                                            (line 39660)
* fxodd?:                                rnrs arithmetic fixnums.
                                                            (line 39608)
* fxpositive?:                           rnrs arithmetic fixnums.
                                                            (line 39606)
* fxreverse-bit-field:                   rnrs arithmetic fixnums.
                                                            (line 39714)
* fxrotate-bit-field:                    rnrs arithmetic fixnums.
                                                            (line 39709)
* fxxor:                                 rnrs arithmetic fixnums.
                                                            (line 39663)
* fxzero?:                               rnrs arithmetic fixnums.
                                                            (line 39605)
* gc:                                    System Commands.   (line  3813)
* gc <1>:                                Garbage Collection Functions.
                                                            (line 23389)
* gc-live-object-stats:                  Garbage Collection Functions.
                                                            (line 23439)
* gc-stats:                              Garbage Collection Functions.
                                                            (line 23434)
* gcd:                                   Integer Operations.
                                                            (line  7704)
* gcd <1>:                               rnrs base.         (line 38572)
* gcprof:                                Statprof.          (line 42787)
* ge?:                                   Inlined Mathematical Instructions.
                                                            (line 48519)
* generate-temporaries:                  Syntax Transformer Helpers.
                                                            (line 16800)
* generate-temporaries <1>:              rnrs syntax-case.  (line 39958)
* generic-function-methods:              Generic Functions. (line 45357)
* generic-function-name:                 Generic Functions. (line 45354)
* gensym:                                Symbol Primitives. (line 11245)
* get-bytevector-all:                    R6RS Binary Input. (line 21274)
* get-bytevector-n:                      R6RS Binary Input. (line 21255)
* get-bytevector-n!:                     R6RS Binary Input. (line 21261)
* get-bytevector-some:                   R6RS Binary Input. (line 21267)
* get-char:                              R6RS Textual Input.
                                                            (line 21299)
* get-datum:                             R6RS Textual Input.
                                                            (line 21376)
* get-environment-variable:              SRFI-98.           (line 38209)
* get-environment-variables:             SRFI-98.           (line 38214)
* get-internal-real-time:                Time.              (line 30179)
* get-internal-run-time:                 Time.              (line 30183)
* get-line:                              R6RS Textual Input.
                                                            (line 21358)
* get-output-string:                     String Ports.      (line 20646)
* get-print-state:                       Writing.           (line 19999)
* get-string-all:                        R6RS Textual Input.
                                                            (line 21348)
* get-string-n:                          R6RS Textual Input.
                                                            (line 21313)
* get-string-n!:                         R6RS Textual Input.
                                                            (line 21331)
* get-u8:                                R6RS Binary Input. (line 21245)
* getaddrinfo:                           Network Databases. (line 31082)
* getaffinity:                           Processes.         (line 30625)
* getcwd:                                Processes.         (line 30300)
* getegid:                               Processes.         (line 30350)
* getenv:                                Runtime Environment.
                                                            (line 30250)
* geteuid:                               Processes.         (line 30343)
* getgid:                                Processes.         (line 30339)
* getgr:                                 User Information.  (line 30004)
* getgrent:                              User Information.  (line 29990)
* getgrgid:                              User Information.  (line 29979)
* getgrnam:                              User Information.  (line 29982)
* getgroups:                             Processes.         (line 30325)
* gethost:                               Network Databases. (line 31250)
* gethostbyaddr:                         Network Databases. (line 31252)
* gethostbyname:                         Network Databases. (line 31251)
* gethostent:                            Network Databases. (line 31281)
* gethostname:                           System Identification.
                                                            (line 31923)
* getitimer:                             Signals.           (line 30796)
* getlogin:                              User Information.  (line 30013)
* getnet:                                Network Databases. (line 31314)
* getnetbyaddr:                          Network Databases. (line 31316)
* getnetbyname:                          Network Databases. (line 31315)
* getnetent:                             Network Databases. (line 31334)
* getopt-long:                           getopt-long Reference.
                                                            (line 33790)
* getpass:                               Encryption.        (line 31981)
* getpeername:                           Network Sockets and Communication.
                                                            (line 31757)
* getpgrp:                               Processes.         (line 30391)
* getpid:                                Processes.         (line 30321)
* getppid:                               Processes.         (line 30330)
* getpriority:                           Processes.         (line 30613)
* getproto:                              Network Databases. (line 31361)
* getprotobyname:                        Network Databases. (line 31362)
* getprotobynumber:                      Network Databases. (line 31363)
* getprotoent:                           Network Databases. (line 31381)
* getpw:                                 User Information.  (line 29961)
* getpwent:                              User Information.  (line 29947)
* getpwnam:                              User Information.  (line 29939)
* getpwuid:                              User Information.  (line 29936)
* getserv:                               Network Databases. (line 31411)
* getservbyname:                         Network Databases. (line 31412)
* getservbyport:                         Network Databases. (line 31413)
* getservent:                            Network Databases. (line 31442)
* getsid:                                Processes.         (line 30410)
* getsockname:                           Network Sockets and Communication.
                                                            (line 31747)
* getsockopt:                            Network Sockets and Communication.
                                                            (line 31602)
* getter-with-setter:                    SRFI-17.           (line 35607)
* gettext:                               Gettext Support.   (line 27603)
* gettimeofday:                          Time.              (line 30027)
* getuid:                                Processes.         (line 30335)
* gmtime:                                Time.              (line 30088)
* goops-error:                           GOOPS Error Handling.
                                                            (line 45544)
* greatest-fixnum:                       rnrs arithmetic fixnums.
                                                            (line 39590)
* group:gid:                             User Information.  (line 29974)
* group:mem:                             User Information.  (line 29976)
* group:name:                            User Information.  (line 29970)
* group:passwd:                          User Information.  (line 29972)
* gt?:                                   Inlined Mathematical Instructions.
                                                            (line 48517)
* guard:                                 rnrs exceptions.   (line 39229)
* guild compile:                         Compilation.       (line 22784)
* GUILE_CHECK_RETVAL:                    Autoconf Macros.   (line  6515)
* GUILE_FLAGS:                           Autoconf Macros.   (line  6457)
* GUILE_MODULE_AVAILABLE:                Autoconf Macros.   (line  6531)
* GUILE_MODULE_CHECK:                    Autoconf Macros.   (line  6523)
* GUILE_MODULE_EXPORTS:                  Autoconf Macros.   (line  6541)
* GUILE_MODULE_REQUIRED:                 Autoconf Macros.   (line  6536)
* GUILE_MODULE_REQUIRED_EXPORT:          Autoconf Macros.   (line  6547)
* GUILE_PKG:                             Autoconf Macros.   (line  6439)
* GUILE_PROGS:                           Autoconf Macros.   (line  6495)
* GUILE_SITE_DIR:                        Autoconf Macros.   (line  6487)
* halt:                                  Miscellaneous Instructions.
                                                            (line 48424)
* handle-request:                        Web Server.        (line 33310)
* hash:                                  Hash Table Reference.
                                                            (line 15033)
* hash <1>:                              SRFI-69 Hash table algorithms.
                                                            (line 38150)
* hash-by-identity:                      SRFI-69 Hash table algorithms.
                                                            (line 38153)
* hash-clear!:                           Hash Table Reference.
                                                            (line 14994)
* hash-count:                            Hash Table Reference.
                                                            (line 15128)
* hash-create-handle!:                   Hash Table Reference.
                                                            (line 15068)
* hash-fold:                             Hash Table Reference.
                                                            (line 15109)
* hash-for-each:                         Hash Table Reference.
                                                            (line 15082)
* hash-for-each-handle:                  Hash Table Reference.
                                                            (line 15100)
* hash-get-handle:                       Hash Table Reference.
                                                            (line 15057)
* hash-map->list:                        Hash Table Reference.
                                                            (line 15081)
* hash-ref:                              Hash Table Reference.
                                                            (line 14998)
* hash-remove!:                          Hash Table Reference.
                                                            (line 15022)
* hash-set!:                             Hash Table Reference.
                                                            (line 15010)
* hash-table->alist:                     SRFI-69 Table properties.
                                                            (line 38132)
* hash-table-delete!:                    SRFI-69 Accessing table items.
                                                            (line 38087)
* hash-table-equivalence-function:       SRFI-69 Hash table algorithms.
                                                            (line 38145)
* hash-table-exists?:                    SRFI-69 Accessing table items.
                                                            (line 38091)
* hash-table-fold:                       SRFI-69 Table properties.
                                                            (line 38127)
* hash-table-hash-function:              SRFI-69 Hash table algorithms.
                                                            (line 38146)
* hash-table-keys:                       SRFI-69 Table properties.
                                                            (line 38117)
* hash-table-ref:                        SRFI-69 Accessing table items.
                                                            (line 38074)
* hash-table-ref/default:                SRFI-69 Accessing table items.
                                                            (line 38075)
* hash-table-set!:                       SRFI-69 Accessing table items.
                                                            (line 38084)
* hash-table-size:                       SRFI-69 Table properties.
                                                            (line 38113)
* hash-table-update!:                    SRFI-69 Accessing table items.
                                                            (line 38094)
* hash-table-update!/default:            SRFI-69 Accessing table items.
                                                            (line 38096)
* hash-table-values:                     SRFI-69 Table properties.
                                                            (line 38120)
* hash-table-walk:                       SRFI-69 Table properties.
                                                            (line 38123)
* hash-table?:                           Hash Table Reference.
                                                            (line 14990)
* hashq:                                 Hash Table Reference.
                                                            (line 15034)
* hashq-create-handle!:                  Hash Table Reference.
                                                            (line 15069)
* hashq-get-handle:                      Hash Table Reference.
                                                            (line 15058)
* hashq-ref:                             Hash Table Reference.
                                                            (line 14999)
* hashq-remove!:                         Hash Table Reference.
                                                            (line 15023)
* hashq-set!:                            Hash Table Reference.
                                                            (line 15011)
* hashtable-clear!:                      rnrs hashtables.   (line 40054)
* hashtable-clear! <1>:                  rnrs hashtables.   (line 40055)
* hashtable-contains?:                   rnrs hashtables.   (line 40037)
* hashtable-copy:                        rnrs hashtables.   (line 40048)
* hashtable-copy <1>:                    rnrs hashtables.   (line 40049)
* hashtable-delete!:                     rnrs hashtables.   (line 40032)
* hashtable-entries:                     rnrs hashtables.   (line 40065)
* hashtable-equivalence-function:        rnrs hashtables.   (line 40070)
* hashtable-hash-function:               rnrs hashtables.   (line 40075)
* hashtable-keys:                        rnrs hashtables.   (line 40061)
* hashtable-mutable?:                    rnrs hashtables.   (line 40080)
* hashtable-ref:                         rnrs hashtables.   (line 40023)
* hashtable-set!:                        rnrs hashtables.   (line 40027)
* hashtable-size:                        rnrs hashtables.   (line 40020)
* hashtable-update!:                     rnrs hashtables.   (line 40041)
* hashtable?:                            rnrs hashtables.   (line 40017)
* hashv:                                 Hash Table Reference.
                                                            (line 15035)
* hashv-create-handle!:                  Hash Table Reference.
                                                            (line 15070)
* hashv-get-handle:                      Hash Table Reference.
                                                            (line 15059)
* hashv-ref:                             Hash Table Reference.
                                                            (line 15000)
* hashv-remove!:                         Hash Table Reference.
                                                            (line 15024)
* hashv-set!:                            Hash Table Reference.
                                                            (line 15012)
* hashx-create-handle!:                  Hash Table Reference.
                                                            (line 15071)
* hashx-get-handle:                      Hash Table Reference.
                                                            (line 15060)
* hashx-ref:                             Hash Table Reference.
                                                            (line 15001)
* hashx-remove!:                         Hash Table Reference.
                                                            (line 15025)
* hashx-set!:                            Hash Table Reference.
                                                            (line 15013)
* header->string:                        HTTP.              (line 32274)
* header-parser:                         HTTP.              (line 32297)
* header-validator:                      HTTP.              (line 32303)
* header-writer:                         HTTP.              (line 32308)
* help:                                  Help Commands.     (line  3619)
* hook->list:                            Hook Reference.    (line 17698)
* hook-empty?:                           Hook Reference.    (line 17678)
* hook?:                                 Hook Reference.    (line 17674)
* hostent:addr-list:                     Network Databases. (line 31241)
* hostent:addrtype:                      Network Databases. (line 31236)
* hostent:aliases:                       Network Databases. (line 31234)
* hostent:length:                        Network Databases. (line 31239)
* hostent:name:                          Network Databases. (line 31232)
* http:                                  Web Server.        (line 33380)
* http-delete:                           Web Client.        (line 33146)
* http-get:                              Web Client.        (line 33142)
* http-head:                             Web Client.        (line 33143)
* http-options:                          Web Client.        (line 33148)
* http-post:                             Web Client.        (line 33144)
* http-put:                              Web Client.        (line 33145)
* http-trace:                            Web Client.        (line 33147)
* i/o-decoding-error?:                   R6RS Transcoders.  (line 20917)
* i/o-encoding-error-char:               R6RS Transcoders.  (line 20935)
* i/o-encoding-error?:                   R6RS Transcoders.  (line 20934)
* i/o-error-filename:                    I/O Conditions.    (line 39437)
* i/o-error-port:                        I/O Conditions.    (line 39469)
* i/o-error-position:                    I/O Conditions.    (line 39430)
* i/o-error?:                            I/O Conditions.    (line 39414)
* i/o-file-already-exists-error?:        I/O Conditions.    (line 39456)
* i/o-file-does-not-exist-error?:        I/O Conditions.    (line 39462)
* i/o-file-is-read-only-error?:          I/O Conditions.    (line 39450)
* i/o-file-protection-error?:            I/O Conditions.    (line 39443)
* i/o-filename-error?:                   I/O Conditions.    (line 39436)
* i/o-invalid-position-error?:           I/O Conditions.    (line 39429)
* i/o-port-error?:                       I/O Conditions.    (line 39468)
* i/o-read-error?:                       I/O Conditions.    (line 39419)
* i/o-write-error?:                      I/O Conditions.    (line 39424)
* identifier-syntax:                     Identifier Macros. (line 16995)
* identifier-syntax <1>:                 Identifier Macros. (line 17042)
* identifier-syntax <2>:                 rnrs base.         (line 38484)
* identifier?:                           Syntax Case.       (line 16603)
* identifier? <1>:                       rnrs syntax-case.  (line 39946)
* identity:                              Higher-Order Functions.
                                                            (line 15920)
* if:                                    Conditionals.      (line 18235)
* if <1>:                                rnrs base.         (line 38512)
* imag-part:                             Complex.           (line  7825)
* imag-part <1>:                         rnrs base.         (line 38533)
* implementation-restriction-violation?: rnrs conditions.   (line 39381)
* import:                                Module Commands.   (line  3653)
* import <1>:                            R6RS Libraries.    (line 24370)
* in:                                    Module Commands.   (line  3665)
* in <1>:                                Module Commands.   (line  3666)
* include:                               Local Inclusion.   (line 23244)
* include-from-path:                     Local Inclusion.   (line 23285)
* inet-aton:                             Network Address Conversion.
                                                            (line 31007)
* inet-lnaof:                            Network Address Conversion.
                                                            (line 31032)
* inet-makeaddr:                         Network Address Conversion.
                                                            (line 31039)
* inet-netof:                            Network Address Conversion.
                                                            (line 31025)
* inet-ntoa:                             Network Address Conversion.
                                                            (line 31016)
* inet-ntop:                             Network Address Conversion.
                                                            (line 31052)
* inet-pton:                             Network Address Conversion.
                                                            (line 31061)
* inexact:                               rnrs base.         (line 38562)
* inexact->exact:                        Exactness.         (line  7569)
* inexact->exact <1>:                    rnrs r5rs.         (line 40241)
* inexact?:                              Exactness.         (line  7561)
* inexact? <1>:                          rnrs base.         (line 38560)
* inf:                                   Reals and Rationals.
                                                            (line  7455)
* inf?:                                  Reals and Rationals.
                                                            (line  7437)
* infinite?:                             rnrs base.         (line 38702)
* input-port?:                           Ports.             (line 19798)
* input-port? <1>:                       R6RS Input Ports.  (line 21123)
* input-port? <2>:                       rnrs io simple.    (line 39502)
* inspect:                               Inspect Commands.  (line  3804)
* install-trap-handler!:                 High-Level Traps.  (line 28828)
* instance?:                             Instances.         (line 45252)
* instrumented-source-files:             Code Coverage.     (line 28953)
* instrumented/executed-lines:           Code Coverage.     (line 28962)
* integer->char:                         Characters.        (line  8627)
* integer->char <1>:                     rnrs base.         (line 38424)
* integer->list:                         SRFI-60.           (line 37949)
* integer-expt:                          Bitwise Operations.
                                                            (line  8284)
* integer-length:                        Bitwise Operations.
                                                            (line  8269)
* integer-valued?:                       rnrs base.         (line 38693)
* integer?:                              Integers.          (line  7191)
* integer? <1>:                          rnrs base.         (line 38567)
* interaction-environment:               Fly Evaluation.    (line 22630)
* iota:                                  SRFI-1 Constructors.
                                                            (line 34054)
* irritants-condition?:                  rnrs conditions.   (line 39360)
* is-a?:                                 Instances.         (line 45255)
* isatty?:                               Terminals and Ptys.
                                                            (line 30848)
* join-thread:                           Threads.           (line 25811)
* join-timeout-exception?:               SRFI-18 Exceptions.
                                                            (line 35858)
* julian-day->date:                      SRFI-19 Time/Date conversions.
                                                            (line 36111)
* julian-day->time-monotonic:            SRFI-19 Time/Date conversions.
                                                            (line 36112)
* julian-day->time-tai:                  SRFI-19 Time/Date conversions.
                                                            (line 36113)
* julian-day->time-utc:                  SRFI-19 Time/Date conversions.
                                                            (line 36114)
* keyword->string:                       SRFI-88.           (line 38191)
* keyword->symbol:                       Keyword Procedures.
                                                            (line 11640)
* keyword?:                              Keyword Procedures.
                                                            (line 11636)
* keyword? <1>:                          SRFI-88.           (line 38182)
* kill:                                  Signals.           (line 30674)
* known-header?:                         HTTP.              (line 32293)
* lalr-parser:                           LALR(1) Parsing.   (line 22263)
* lambda:                                Lambda.            (line 15343)
* lambda <1>:                            rnrs base.         (line 38490)
* lambda*:                               lambda* and define*.
                                                            (line 15594)
* language:                              Language Commands. (line  3674)
* last:                                  SRFI-1 Selectors.  (line 34176)
* last-pair:                             List Selection.    (line 12048)
* latin-1-codec:                         R6RS Transcoders.  (line 20862)
* lazy:                                  SRFI-45.           (line 37770)
* lchown:                                File System.       (line 29663)
* lcm:                                   Integer Operations.
                                                            (line  7712)
* lcm <1>:                               rnrs base.         (line 38573)
* le?:                                   Inlined Mathematical Instructions.
                                                            (line 48518)
* least-fixnum:                          rnrs arithmetic fixnums.
                                                            (line 39589)
* left-justify-string:                   texinfo string-utils.
                                                            (line 43898)
* length:                                List Selection.    (line 12044)
* length <1>:                            rnrs base.         (line 38593)
* length+:                               SRFI-1 Length Append etc.
                                                            (line 34182)
* let:                                   Local Bindings.    (line 17978)
* let <1>:                               while do.          (line 18478)
* let <2>:                               rnrs base.         (line 38493)
* let*:                                  Local Bindings.    (line 18006)
* let* <1>:                              rnrs base.         (line 38494)
* let*-values:                           SRFI-11.           (line 35530)
* let*-values <1>:                       rnrs base.         (line 38500)
* let-escape-continuation:               Prompt Primitives. (line 18651)
* let-keywords:                          ice-9 optargs.     (line 15716)
* let-keywords*:                         ice-9 optargs.     (line 15718)
* let-optional:                          ice-9 optargs.     (line 15696)
* let-optional*:                         ice-9 optargs.     (line 15697)
* let-syntax:                            Defining Macros.   (line 16152)
* let-syntax <1>:                        rnrs base.         (line 38480)
* let-values:                            SRFI-11.           (line 35530)
* let-values <1>:                        rnrs base.         (line 38499)
* let/ec:                                Prompt Primitives. (line 18652)
* letpar:                                Parallel Forms.    (line 26546)
* letrec:                                Local Bindings.    (line 18021)
* letrec <1>:                            rnrs base.         (line 38495)
* letrec*:                               Local Bindings.    (line 18045)
* letrec* <1>:                           rnrs base.         (line 38496)
* letrec-syntax:                         Defining Macros.   (line 16173)
* letrec-syntax <1>:                     rnrs base.         (line 38481)
* lexical-violation?:                    rnrs conditions.   (line 39387)
* library:                               R6RS Libraries.    (line 24302)
* line-execution-counts:                 Code Coverage.     (line 28957)
* link:                                  File System.       (line 29741)
* link-now:                              Top-Level Environment Instructions.
                                                            (line 47865)
* list:                                  List Constructors. (line 12000)
* list <1>:                              rnrs base.         (line 38590)
* list <2>:                              Data Constructor Instructions.
                                                            (line 48253)
* list->array:                           Array Procedures.  (line 12844)
* list->bitvector:                       Bit Vectors.       (line 12581)
* list->c32vector:                       SRFI-4 API.        (line 35221)
* list->c64vector:                       SRFI-4 API.        (line 35222)
* list->char-set:                        Creating Character Sets.
                                                            (line  8786)
* list->char-set!:                       Creating Character Sets.
                                                            (line  8792)
* list->f32vector:                       SRFI-4 API.        (line 35219)
* list->f64vector:                       SRFI-4 API.        (line 35220)
* list->integer:                         SRFI-60.           (line 37959)
* list->s16vector:                       SRFI-4 API.        (line 35214)
* list->s32vector:                       SRFI-4 API.        (line 35216)
* list->s64vector:                       SRFI-4 API.        (line 35218)
* list->s8vector:                        SRFI-4 API.        (line 35212)
* list->stream:                          SRFI-41 Stream Library.
                                                            (line 37007)
* list->stream <1>:                      Streams.           (line 41930)
* list->string:                          String Constructors.
                                                            (line  9293)
* list->string <1>:                      rnrs base.         (line 38609)
* list->symbol:                          Symbol Primitives. (line 11139)
* list->typed-array:                     Array Procedures.  (line 12847)
* list->u16vector:                       SRFI-4 API.        (line 35213)
* list->u32vector:                       SRFI-4 API.        (line 35215)
* list->u64vector:                       SRFI-4 API.        (line 35217)
* list->u8vector:                        SRFI-4 API.        (line 35211)
* list->vector:                          Vector Creation.   (line 12305)
* list->vector <1>:                      SRFI-43 Conversion.
                                                            (line 37716)
* list->vector <2>:                      rnrs base.         (line 38737)
* list->vlist:                           VLists.            (line 13548)
* list->weak-vector:                     Weak vectors.      (line 23716)
* list-cdr-ref:                          List Selection.    (line 12058)
* list-cdr-set!:                         List Modification. (line 12132)
* list-copy:                             List Constructors. (line 12021)
* list-copy <1>:                         SRFI-1 Constructors.
                                                            (line 34043)
* list-head:                             List Selection.    (line 12067)
* list-index:                            SRFI-1 Searching.  (line 34559)
* list-matches:                          Regexp Functions.  (line 21986)
* list-ref:                              List Selection.    (line 12053)
* list-ref <1>:                          rnrs base.         (line 38594)
* list-set!:                             List Modification. (line 12128)
* list-sort:                             rnrs sorting.      (line 38901)
* list-tabulate:                         SRFI-1 Constructors.
                                                            (line 34037)
* list-tail:                             List Selection.    (line 12057)
* list-tail <1>:                         rnrs base.         (line 38595)
* list-traps:                            Trap States.       (line 28769)
* list=:                                 SRFI-1 Predicates. (line 34121)
* list?:                                 List Predicates.   (line 11976)
* list? <1>:                             rnrs base.         (line 38428)
* list? <2>:                             Inlined Scheme Instructions.
                                                            (line 48473)
* listen:                                Network Sockets and Communication.
                                                            (line 31721)
* load:                                  Module Commands.   (line  3656)
* load <1>:                              Loading.           (line 22876)
* load-array:                            Loading Instructions.
                                                            (line 48315)
* load-compiled:                         Loading.           (line 22895)
* load-extension:                        Foreign Functions. (line 24907)
* load-from-path:                        Load Paths.        (line 22971)
* load-number:                           Loading Instructions.
                                                            (line 48302)
* load-objcode:                          Bytecode and Objcode.
                                                            (line 49261)
* load-program:                          Loading Instructions.
                                                            (line 48319)
* load-string:                           Loading Instructions.
                                                            (line 48305)
* load-symbol:                           Loading Instructions.
                                                            (line 48311)
* load-wide-string:                      Loading Instructions.
                                                            (line 48308)
* local-bound?:                          Lexical Environment Instructions.
                                                            (line 47806)
* local-boxed-ref:                       Lexical Environment Instructions.
                                                            (line 47758)
* local-boxed-set:                       Lexical Environment Instructions.
                                                            (line 47759)
* local-compile:                         Local Evaluation.  (line 23203)
* local-eval:                            Local Evaluation.  (line 23201)
* local-ref:                             Lexical Environment Instructions.
                                                            (line 47734)
* local-set:                             Lexical Environment Instructions.
                                                            (line 47743)
* locale-am-string:                      Accessing Locale Information.
                                                            (line 27441)
* locale-currency-symbol:                Accessing Locale Information.
                                                            (line 27500)
* locale-currency-symbol-precedes-negative?: Accessing Locale Information.
                                                            (line 27520)
* locale-currency-symbol-precedes-positive?: Accessing Locale Information.
                                                            (line 27518)
* locale-date+time-format:               Accessing Locale Information.
                                                            (line 27446)
* locale-date-format:                    Accessing Locale Information.
                                                            (line 27447)
* locale-day:                            Accessing Locale Information.
                                                            (line 27432)
* locale-day-short:                      Accessing Locale Information.
                                                            (line 27433)
* locale-decimal-point:                  Accessing Locale Information.
                                                            (line 27470)
* locale-digit-grouping:                 Accessing Locale Information.
                                                            (line 27476)
* locale-encoding:                       Accessing Locale Information.
                                                            (line 27426)
* locale-era:                            Accessing Locale Information.
                                                            (line 27459)
* locale-era-date+time-format:           Accessing Locale Information.
                                                            (line 27451)
* locale-era-date-format:                Accessing Locale Information.
                                                            (line 27450)
* locale-era-time-format:                Accessing Locale Information.
                                                            (line 27452)
* locale-era-year:                       Accessing Locale Information.
                                                            (line 27460)
* locale-monetary-decimal-point:         Accessing Locale Information.
                                                            (line 27494)
* locale-monetary-fractional-digits:     Accessing Locale Information.
                                                            (line 27513)
* locale-monetary-grouping:              Accessing Locale Information.
                                                            (line 27496)
* locale-monetary-negative-sign:         Accessing Locale Information.
                                                            (line 27530)
* locale-monetary-positive-sign:         Accessing Locale Information.
                                                            (line 27529)
* locale-monetary-thousands-separator:   Accessing Locale Information.
                                                            (line 27495)
* locale-month:                          Accessing Locale Information.
                                                            (line 27434)
* locale-month-short:                    Accessing Locale Information.
                                                            (line 27435)
* locale-negative-separated-by-space?:   Accessing Locale Information.
                                                            (line 27523)
* locale-negative-sign-position:         Accessing Locale Information.
                                                            (line 27535)
* locale-no-regexp:                      Accessing Locale Information.
                                                            (line 27559)
* locale-pm-string:                      Accessing Locale Information.
                                                            (line 27442)
* locale-positive-separated-by-space?:   Accessing Locale Information.
                                                            (line 27522)
* locale-positive-sign-position:         Accessing Locale Information.
                                                            (line 27534)
* locale-string->inexact:                Number Input and Output.
                                                            (line 27389)
* locale-string->integer:                Number Input and Output.
                                                            (line 27376)
* locale-thousands-separator:            Accessing Locale Information.
                                                            (line 27471)
* locale-time+am/pm-format:              Accessing Locale Information.
                                                            (line 27449)
* locale-time-format:                    Accessing Locale Information.
                                                            (line 27448)
* locale-yes-regexp:                     Accessing Locale Information.
                                                            (line 27558)
* locale?:                               i18n Introduction. (line 27266)
* locals:                                Debug Commands.    (line  3748)
* localtime:                             Time.              (line 30080)
* lock-mutex:                            Mutexes and Condition Variables.
                                                            (line 25927)
* log:                                   Scientific.        (line  8135)
* log <1>:                               rnrs base.         (line 38543)
* log10:                                 Scientific.        (line  8138)
* log2-binary-factors:                   SRFI-60.           (line 37909)
* logand:                                Bitwise Operations.
                                                            (line  8167)
* logand <1>:                            Inlined Mathematical Instructions.
                                                            (line 48521)
* logbit?:                               Bitwise Operations.
                                                            (line  8212)
* logcount:                              Bitwise Operations.
                                                            (line  8255)
* logior:                                Bitwise Operations.
                                                            (line  8175)
* logior <1>:                            Inlined Mathematical Instructions.
                                                            (line 48522)
* lognot:                                Bitwise Operations.
                                                            (line  8193)
* logtest:                               Bitwise Operations.
                                                            (line  8203)
* logxor:                                Bitwise Operations.
                                                            (line  8183)
* logxor <1>:                            Inlined Mathematical Instructions.
                                                            (line 48523)
* long-local-bound?:                     Lexical Environment Instructions.
                                                            (line 47807)
* long-local-ref:                        Lexical Environment Instructions.
                                                            (line 47735)
* long-local-set:                        Lexical Environment Instructions.
                                                            (line 47744)
* long-object-ref:                       Data Constructor Instructions.
                                                            (line 48286)
* long-toplevel-ref:                     Top-Level Environment Instructions.
                                                            (line 47827)
* long-toplevel-set:                     Top-Level Environment Instructions.
                                                            (line 47855)
* lookahead-char:                        R6RS Textual Input.
                                                            (line 21309)
* lookahead-u8:                          R6RS Binary Input. (line 21250)
* lookup-compilation-order:              Compiler Tower.    (line 48660)
* lookup-language:                       Compiler Tower.    (line 48648)
* lookup-server-impl:                    Web Server.        (line 33282)
* lset-adjoin:                           SRFI-1 Set Operations.
                                                            (line 34734)
* lset-diff+intersection:                SRFI-1 Set Operations.
                                                            (line 34818)
* lset-diff+intersection!:               SRFI-1 Set Operations.
                                                            (line 34819)
* lset-difference:                       SRFI-1 Set Operations.
                                                            (line 34801)
* lset-difference!:                      SRFI-1 Set Operations.
                                                            (line 34802)
* lset-intersection:                     SRFI-1 Set Operations.
                                                            (line 34777)
* lset-intersection!:                    SRFI-1 Set Operations.
                                                            (line 34778)
* lset-union:                            SRFI-1 Set Operations.
                                                            (line 34746)
* lset-union!:                           SRFI-1 Set Operations.
                                                            (line 34747)
* lset-xor:                              SRFI-1 Set Operations.
                                                            (line 34833)
* lset-xor!:                             SRFI-1 Set Operations.
                                                            (line 34834)
* lset<=:                                SRFI-1 Set Operations.
                                                            (line 34704)
* lset=:                                 SRFI-1 Set Operations.
                                                            (line 34718)
* lstat:                                 File System.       (line 29652)
* lt?:                                   Inlined Mathematical Instructions.
                                                            (line 48516)
* macro-binding:                         Internal Macros.   (line 17228)
* macro-name:                            Internal Macros.   (line 17224)
* macro-transformer:                     Internal Macros.   (line 17232)
* macro-type:                            Internal Macros.   (line 17219)
* macro?:                                Internal Macros.   (line 17207)
* magnitude:                             Complex.           (line  7829)
* magnitude <1>:                         rnrs base.         (line 38536)
* major-version:                         Build Config.      (line 26654)
* make:                                  Instance Creation. (line 44264)
* make <1>:                              Instance Creation. (line 44269)
* make <2>:                              Instance Creation. (line 44270)
* make <3>:                              Class Definition Protocol.
                                                            (line 46030)
* make-accessor:                         Generic Function Internals.
                                                            (line 46357)
* make-arbiter:                          Arbiters.          (line 25629)
* make-array:                            Array Procedures.  (line 12813)
* make-array <1>:                        Data Constructor Instructions.
                                                            (line 48272)
* make-assertion-violation:              rnrs conditions.   (line 39353)
* make-binding:                          Compiled Procedures.
                                                            (line 15479)
* make-bitvector:                        Bit Vectors.       (line 12540)
* make-buffered-input-port:              Buffered Input.    (line 42004)
* make-bytevector:                       Bytevector Manipulation.
                                                            (line 10558)
* make-c-struct:                         Foreign Structs.   (line 25427)
* make-c32vector:                        SRFI-4 API.        (line 35058)
* make-c64vector:                        SRFI-4 API.        (line 35059)
* make-char32:                           Data Constructor Instructions.
                                                            (line 48243)
* make-char8:                            Data Constructor Instructions.
                                                            (line 48240)
* make-chunked-input-port:               Transfer Codings.  (line 32825)
* make-chunked-output-port:              Transfer Codings.  (line 32840)
* make-class:                            Class Definition Protocol.
                                                            (line 45982)
* make-closure:                          Lexical Environment Instructions.
                                                            (line 47776)
* make-completion-function:              Readline Functions.
                                                            (line 40630)
* make-compound-condition:               SRFI-35.           (line 36576)
* make-condition:                        SRFI-35.           (line 36566)
* make-condition-type:                   SRFI-35.           (line 36555)
* make-condition-variable:               Mutexes and Condition Variables.
                                                            (line 26006)
* make-condition-variable <1>:           SRFI-18 Condition variables.
                                                            (line 35783)
* make-custom-binary-input-port:         R6RS Binary Input. (line 21189)
* make-custom-binary-output-port:        R6RS Binary Output.
                                                            (line 21477)
* make-date:                             SRFI-19 Date.      (line 36050)
* make-doubly-weak-hash-table:           Weak hash tables.  (line 23686)
* make-dynamic-state:                    Fluids and Dynamic States.
                                                            (line 26276)
* make-empty-attlist:                    SSAX.              (line 43131)
* make-enumeration:                      rnrs enums.        (line 40114)
* make-eol:                              Data Constructor Instructions.
                                                            (line 48237)
* make-eq-hashtable:                     rnrs hashtables.   (line 39995)
* make-eq-hashtable <1>:                 rnrs hashtables.   (line 39996)
* make-eqv-hashtable:                    rnrs hashtables.   (line 40001)
* make-eqv-hashtable <1>:                rnrs hashtables.   (line 40002)
* make-error:                            rnrs conditions.   (line 39342)
* make-f32vector:                        SRFI-4 API.        (line 35056)
* make-f64vector:                        SRFI-4 API.        (line 35057)
* make-false:                            Data Constructor Instructions.
                                                            (line 48228)
* make-fluid:                            Fluids and Dynamic States.
                                                            (line 26192)
* make-future:                           Futures.           (line 26507)
* make-generic:                          Generic Function Internals.
                                                            (line 46333)
* make-guardian:                         Guardians.         (line 23747)
* make-hash-table:                       Hash Table Reference.
                                                            (line 14965)
* make-hash-table <1>:                   SRFI-69 Creating hash tables.
                                                            (line 38014)
* make-hashtable:                        rnrs hashtables.   (line 40007)
* make-hashtable <1>:                    rnrs hashtables.   (line 40008)
* make-hook:                             Hook Reference.    (line 17668)
* make-i/o-decoding-error:               R6RS Transcoders.  (line 20916)
* make-i/o-encoding-error:               R6RS Transcoders.  (line 20933)
* make-i/o-error:                        I/O Conditions.    (line 39413)
* make-i/o-file-already-exists-error:    I/O Conditions.    (line 39455)
* make-i/o-file-does-not-exist-error:    I/O Conditions.    (line 39461)
* make-i/o-file-is-read-only-error:      I/O Conditions.    (line 39449)
* make-i/o-file-protection-error:        I/O Conditions.    (line 39442)
* make-i/o-invalid-position-error:       I/O Conditions.    (line 39428)
* make-i/o-port-error:                   I/O Conditions.    (line 39467)
* make-i/o-read-error:                   I/O Conditions.    (line 39418)
* make-i/o-write-error:                  I/O Conditions.    (line 39423)
* make-implementation-restriction-violation: rnrs conditions.
                                                            (line 39380)
* make-instance:                         Instance Creation. (line 44292)
* make-instance <1>:                     Instance Creation. (line 44293)
* make-int16:                            Data Constructor Instructions.
                                                            (line 48216)
* make-int64:                            Data Constructor Instructions.
                                                            (line 48223)
* make-int8:                             Data Constructor Instructions.
                                                            (line 48207)
* make-int8:0:                           Data Constructor Instructions.
                                                            (line 48210)
* make-int8:1:                           Data Constructor Instructions.
                                                            (line 48213)
* make-io-filename-error:                I/O Conditions.    (line 39435)
* make-irritants-condition:              rnrs conditions.   (line 39359)
* make-keyword:                          Data Constructor Instructions.
                                                            (line 48250)
* make-lexical-violation:                rnrs conditions.   (line 39386)
* make-line-buffered-input-port:         Buffered Input.    (line 42019)
* make-list:                             List Constructors. (line 12025)
* make-locale:                           i18n Introduction. (line 27235)
* make-message-condition:                rnrs conditions.   (line 39324)
* make-method:                           Method Definition Internals.
                                                            (line 46275)
* make-mutex:                            Mutexes and Condition Variables.
                                                            (line 25899)
* make-mutex <1>:                        SRFI-18 Mutexes.   (line 35728)
* make-nil:                              Data Constructor Instructions.
                                                            (line 48234)
* make-no-infinities-violation:          rnrs arithmetic flonums.
                                                            (line 39833)
* make-no-nans-violation:                rnrs arithmetic flonums.
                                                            (line 39840)
* make-non-continuable-violation:        rnrs conditions.   (line 39374)
* make-object-property:                  Object Properties. (line 17398)
* make-parameter:                        Parameters.        (line 26349)
* make-pointer:                          Foreign Variables. (line 25224)
* make-polar:                            Complex.           (line  7817)
* make-polar <1>:                        rnrs base.         (line 38535)
* make-procedure-with-setter:            Procedures with Setters.
                                                            (line 16028)
* make-program:                          Bytecode and Objcode.
                                                            (line 49281)
* make-prompt-tag:                       Prompt Primitives. (line 18538)
* make-q:                                Queues.            (line 41796)
* make-random-source:                    SRFI-27 Random Sources.
                                                            (line 36413)
* make-record-constructor-descriptor:    rnrs records procedural.
                                                            (line 39116)
* make-record-type:                      Records.           (line 13792)
* make-record-type-descriptor:           rnrs records procedural.
                                                            (line 39098)
* make-rectangular:                      Complex.           (line  7812)
* make-rectangular <1>:                  rnrs base.         (line 38534)
* make-recursive-mutex:                  Mutexes and Condition Variables.
                                                            (line 25921)
* make-regexp:                           Regexp Functions.  (line 21902)
* make-s16vector:                        SRFI-4 API.        (line 35051)
* make-s32vector:                        SRFI-4 API.        (line 35053)
* make-s64vector:                        SRFI-4 API.        (line 35055)
* make-s8vector:                         SRFI-4 API.        (line 35049)
* make-serious-condition:                rnrs conditions.   (line 39336)
* make-shared-array:                     Shared Arrays.     (line 13009)
* make-socket-address:                   Network Socket Address.
                                                            (line 31463)
* make-socket-address <1>:               Network Socket Address.
                                                            (line 31464)
* make-socket-address <2>:               Network Socket Address.
                                                            (line 31466)
* make-soft-port:                        Soft Ports.        (line 20666)
* make-stack:                            Stack Capture.     (line 27771)
* make-stream:                           Streams.           (line 41911)
* make-string:                           String Constructors.
                                                            (line  9306)
* make-string <1>:                       rnrs base.         (line 38608)
* make-struct:                           Structure Basics.  (line 13948)
* make-struct <1>:                       Data Constructor Instructions.
                                                            (line 48264)
* make-struct-layout:                    Meta-Vtables.      (line 14154)
* make-struct/no-tail:                   Structure Basics.  (line 13949)
* make-symbol:                           Symbol Uninterned. (line 11423)
* make-symbol <1>:                       Data Constructor Instructions.
                                                            (line 48247)
* make-syntax-transformer:               Internal Macros.   (line 17203)
* make-syntax-violation:                 rnrs conditions.   (line 39392)
* make-tcp-server-socket:                REPL Servers.      (line 23310)
* make-text-wrapper:                     texinfo string-utils.
                                                            (line 43922)
* make-thread:                           Threads.           (line 25867)
* make-thread <1>:                       SRFI-18 Threads.   (line 35649)
* make-time:                             SRFI-19 Time.      (line 35976)
* make-transcoder:                       R6RS Transcoders.  (line 20989)
* make-transcoder <1>:                   R6RS Transcoders.  (line 20990)
* make-transcoder <2>:                   R6RS Transcoders.  (line 20991)
* make-true:                             Data Constructor Instructions.
                                                            (line 48231)
* make-typed-array:                      Array Procedures.  (line 12817)
* make-u16vector:                        SRFI-4 API.        (line 35050)
* make-u32vector:                        SRFI-4 API.        (line 35052)
* make-u64vector:                        SRFI-4 API.        (line 35054)
* make-u8vector:                         SRFI-4 API.        (line 35048)
* make-uint64:                           Data Constructor Instructions.
                                                            (line 48219)
* make-unbound-fluid:                    Fluids and Dynamic States.
                                                            (line 26204)
* make-undefined-variable:               Variables.         (line 24410)
* make-undefined-violation:              rnrs conditions.   (line 39401)
* make-unix-domain-server-socket:        REPL Servers.      (line 23317)
* make-variable:                         Variables.         (line 24414)
* make-variable <1>:                     Top-Level Environment Instructions.
                                                            (line 47886)
* make-variable-transformer:             Identifier Macros. (line 17018)
* make-variable-transformer <1>:         rnrs syntax-case.  (line 39926)
* make-vector:                           Vector Creation.   (line 12326)
* make-vector <1>:                       SRFI-43 Constructors.
                                                            (line 37441)
* make-vector <2>:                       rnrs base.         (line 38735)
* make-vector <3>:                       rnrs base.         (line 38736)
* make-violation:                        rnrs conditions.   (line 39347)
* make-vtable:                           Vtables.           (line 13887)
* make-warning:                          rnrs conditions.   (line 39331)
* make-weak-key-hash-table:              Weak hash tables.  (line 23684)
* make-weak-value-hash-table:            Weak hash tables.  (line 23685)
* make-weak-vector:                      Weak vectors.      (line 23709)
* make-who-condition:                    rnrs conditions.   (line 39366)
* malloc-stats:                          Memory Blocks.     (line 23573)
* map:                                   List Mapping.      (line 12241)
* map <1>:                               SRFI-1 Fold and Map.
                                                            (line 34394)
* map!:                                  SRFI-1 Fold and Map.
                                                            (line 34428)
* map-in-order:                          List Mapping.      (line 12242)
* map-union:                             SXPath.            (line 43479)
* match:                                 Pattern Matching.  (line 40326)
* match:count:                           Match Structures.  (line 22168)
* match:end:                             Match Structures.  (line 22144)
* match:prefix:                          Match Structures.  (line 22154)
* match:start:                           Match Structures.  (line 22134)
* match:string:                          Match Structures.  (line 22173)
* match:substring:                       Match Structures.  (line 22119)
* match:suffix:                          Match Structures.  (line 22161)
* max:                                   Arithmetic.        (line  7896)
* max <1>:                               rnrs base.         (line 38638)
* member:                                List Searching.    (line 12221)
* member <1>:                            SRFI-1 Searching.  (line 34571)
* member <2>:                            rnrs lists.        (line 38871)
* memp:                                  rnrs lists.        (line 38870)
* memq:                                  List Searching.    (line 12207)
* memq <1>:                              rnrs lists.        (line 38873)
* memv:                                  List Searching.    (line 12214)
* memv <1>:                              rnrs lists.        (line 38872)
* merge:                                 Sorting.           (line 17449)
* merge!:                                Sorting.           (line 17457)
* message-condition?:                    SRFI-35.           (line 36649)
* message-condition? <1>:                rnrs conditions.   (line 39325)
* method:                                Method Definition Internals.
                                                            (line 46257)
* method-generic-function:               Generic Functions. (line 45365)
* method-procedure:                      Generic Functions. (line 45373)
* method-source:                         Generic Functions. (line 45377)
* method-source <1>:                     Generic Functions. (line 45378)
* method-specializers:                   Generic Functions. (line 45369)
* micro-version:                         Build Config.      (line 26656)
* min:                                   Arithmetic.        (line  7900)
* min <1>:                               rnrs base.         (line 38639)
* minor-version:                         Build Config.      (line 26655)
* mkdir:                                 File System.       (line 29752)
* mknod:                                 File System.       (line 29808)
* mkstemp!:                              File System.       (line 29838)
* mktime:                                Time.              (line 30094)
* mod:                                   rnrs base.         (line 38648)
* mod <1>:                               Inlined Mathematical Instructions.
                                                            (line 48514)
* mod0:                                  rnrs base.         (line 38667)
* modified-julian-day->date:             SRFI-19 Time/Date conversions.
                                                            (line 36115)
* modified-julian-day->time-monotonic:   SRFI-19 Time/Date conversions.
                                                            (line 36116)
* modified-julian-day->time-tai:         SRFI-19 Time/Date conversions.
                                                            (line 36117)
* modified-julian-day->time-utc:         SRFI-19 Time/Date conversions.
                                                            (line 36118)
* module:                                Module Commands.   (line  3650)
* module-add!:                           Module System Reflection.
                                                            (line 24512)
* module-define!:                        Module System Reflection.
                                                            (line 24521)
* module-ref:                            Module System Reflection.
                                                            (line 24516)
* module-set!:                           Module System Reflection.
                                                            (line 24528)
* module-stexi-documentation:            texinfo reflection.
                                                            (line 44028)
* module-use!:                           Module System Reflection.
                                                            (line 24494)
* module-uses:                           Module System Reflection.
                                                            (line 24491)
* module-variable:                       Module System Reflection.
                                                            (line 24508)
* modulo:                                Integer Operations.
                                                            (line  7692)
* modulo <1>:                            rnrs r5rs.         (line 40247)
* modulo-expt:                           Integer Operations.
                                                            (line  7720)
* monetary-amount->locale-string:        Number Input and Output.
                                                            (line 27407)
* monitor:                               Mutexes and Condition Variables.
                                                            (line 26056)
* move->fdes:                            Ports and File Descriptors.
                                                            (line 29249)
* mul:                                   Inlined Mathematical Instructions.
                                                            (line 48510)
* mutex-level:                           Mutexes and Condition Variables.
                                                            (line 25995)
* mutex-lock!:                           SRFI-18 Mutexes.   (line 35756)
* mutex-locked?:                         Mutexes and Condition Variables.
                                                            (line 26001)
* mutex-name:                            SRFI-18 Mutexes.   (line 35736)
* mutex-owner:                           Mutexes and Condition Variables.
                                                            (line 25989)
* mutex-specific:                        SRFI-18 Mutexes.   (line 35740)
* mutex-specific-set!:                   SRFI-18 Mutexes.   (line 35741)
* mutex-state:                           SRFI-18 Mutexes.   (line 35746)
* mutex-unlock!:                         SRFI-18 Mutexes.   (line 35763)
* mutex?:                                Mutexes and Condition Variables.
                                                            (line 25917)
* mv-call:                               Procedure Call and Return Instructions.
                                                            (line 47936)
* n-for-each-par-map:                    Parallel Forms.    (line 26590)
* n-par-for-each:                        Parallel Forms.    (line 26579)
* n-par-map:                             Parallel Forms.    (line 26578)
* nan:                                   Reals and Rationals.
                                                            (line  7451)
* nan?:                                  Reals and Rationals.
                                                            (line  7442)
* nan? <1>:                              rnrs base.         (line 38701)
* native-endianness:                     Bytevector Endianness.
                                                            (line 10532)
* native-eol-style:                      R6RS Transcoders.  (line 20911)
* native-transcoder:                     R6RS Transcoders.  (line 21001)
* negate:                                Higher-Order Functions.
                                                            (line 15895)
* negative?:                             Comparison.        (line  7775)
* negative? <1>:                         rnrs base.         (line 38584)
* netent:addrtype:                       Network Databases. (line 31306)
* netent:aliases:                        Network Databases. (line 31304)
* netent:name:                           Network Databases. (line 31302)
* netent:net:                            Network Databases. (line 31309)
* new-frame:                             Procedure Call and Return Instructions.
                                                            (line 47893)
* newline:                               Writing.           (line 20004)
* newline <1>:                           rnrs io simple.    (line 39535)
* newline <2>:                           rnrs io simple.    (line 39536)
* next:                                  Debug Commands.    (line  3791)
* next-token:                            sxml ssax input-parse.
                                                            (line 43556)
* next-token-of:                         sxml ssax input-parse.
                                                            (line 43559)
* nftw:                                  File Tree Walk.    (line 41686)
* ngettext:                              Gettext Support.   (line 27628)
* nice:                                  Processes.         (line 30593)
* ninth:                                 SRFI-1 Selectors.  (line 34139)
* nl_langinfo:                           Accessing Locale Information.
                                                            (line 27418)
* no-applicable-method:                  Handling Invocation Errors.
                                                            (line 45012)
* no-applicable-method <1>:              Handling Invocation Errors.
                                                            (line 45013)
* no-infinities-violation?:              rnrs arithmetic flonums.
                                                            (line 39834)
* no-method:                             Handling Invocation Errors.
                                                            (line 45005)
* no-method <1>:                         Handling Invocation Errors.
                                                            (line 45006)
* no-nans-violation?:                    rnrs arithmetic flonums.
                                                            (line 39841)
* no-next-method:                        Handling Invocation Errors.
                                                            (line 45019)
* no-next-method <1>:                    Handling Invocation Errors.
                                                            (line 45020)
* node-closure:                          SXPath.            (line 43506)
* node-eq?:                              SXPath.            (line 43456)
* node-equal?:                           SXPath.            (line 43458)
* node-join:                             SXPath.            (line 43500)
* node-or:                               SXPath.            (line 43504)
* node-parent:                           SXPath.            (line 43508)
* node-pos:                              SXPath.            (line 43460)
* node-reduce:                           SXPath.            (line 43502)
* node-reverse:                          SXPath.            (line 43481)
* node-self:                             SXPath.            (line 43487)
* node-trace:                            SXPath.            (line 43483)
* node-typeof?:                          SXPath.            (line 43454)
* nodeset?:                              SXPath.            (line 43452)
* non-continuable-violation?:            rnrs conditions.   (line 39375)
* nop:                                   Miscellaneous Instructions.
                                                            (line 48420)
* not:                                   Booleans.          (line  7019)
* not <1>:                               rnrs base.         (line 38410)
* not <2>:                               Inlined Scheme Instructions.
                                                            (line 48464)
* not-eq?:                               Inlined Scheme Instructions.
                                                            (line 48467)
* not-not:                               Inlined Scheme Instructions.
                                                            (line 48465)
* not-null?:                             Inlined Scheme Instructions.
                                                            (line 48469)
* not-pair?:                             SRFI-1 Predicates. (line 34115)
* null-environment:                      Environments.      (line 24733)
* null-environment <1>:                  rnrs r5rs.         (line 40257)
* null-list?:                            SRFI-1 Predicates. (line 34109)
* null-pointer?:                         Foreign Variables. (line 25235)
* null?:                                 List Predicates.   (line 11985)
* null? <1>:                             rnrs base.         (line 38429)
* null? <2>:                             Inlined Scheme Instructions.
                                                            (line 48468)
* number->locale-string:                 Number Input and Output.
                                                            (line 27400)
* number->string:                        Conversion.        (line  7787)
* number->string <1>:                    rnrs base.         (line 38603)
* number?:                               Numerical Tower.   (line  7108)
* number? <1>:                           rnrs base.         (line 38466)
* numerator:                             Reals and Rationals.
                                                            (line  7459)
* numerator <1>:                         rnrs base.         (line 38554)
* objcode->bytecode:                     Bytecode and Objcode.
                                                            (line 49274)
* objcode?:                              Bytecode and Objcode.
                                                            (line 49252)
* object->string:                        General Conversion.
                                                            (line 17560)
* object-properties:                     Object Properties. (line 17421)
* object-property:                       Object Properties. (line 17429)
* object-ref:                            Data Constructor Instructions.
                                                            (line 48285)
* object-stexi-documentation:            texinfo reflection.
                                                            (line 44039)
* odd?:                                  Integer Operations.
                                                            (line  7670)
* odd? <1>:                              rnrs base.         (line 38570)
* open:                                  Ports and File Descriptors.
                                                            (line 29266)
* open-bytevector-input-port:            R6RS Binary Input. (line 21182)
* open-bytevector-output-port:           R6RS Binary Output.
                                                            (line 21460)
* open-fdes:                             Ports and File Descriptors.
                                                            (line 29290)
* open-file:                             File Ports.        (line 20392)
* open-file-input-port:                  R6RS Input Ports.  (line 21134)
* open-file-input-port <1>:              R6RS Input Ports.  (line 21135)
* open-file-input-port <2>:              R6RS Input Ports.  (line 21136)
* open-file-input-port <3>:              R6RS Input Ports.  (line 21138)
* open-file-output-port:                 R6RS Output Ports. (line 21408)
* open-file-output-port <1>:             R6RS Output Ports. (line 21409)
* open-file-output-port <2>:             R6RS Output Ports. (line 21410)
* open-file-output-port <3>:             R6RS Output Ports. (line 21412)
* open-input-file:                       File Ports.        (line 20479)
* open-input-file <1>:                   rnrs io simple.    (line 39509)
* open-input-output-pipe:                Pipes.             (line 30943)
* open-input-pipe:                       Pipes.             (line 30926)
* open-input-string:                     String Ports.      (line 20632)
* open-output-file:                      File Ports.        (line 20491)
* open-output-file <1>:                  rnrs io simple.    (line 39510)
* open-output-pipe:                      Pipes.             (line 30935)
* open-output-string:                    String Ports.      (line 20639)
* open-pipe:                             Pipes.             (line 30891)
* open-pipe*:                            Pipes.             (line 30892)
* open-server:                           Web Server.        (line 33298)
* open-socket-for-uri:                   Web Client.        (line 33139)
* opendir:                               File System.       (line 29764)
* optimize:                              Compile Commands.  (line  3689)
* option:                                System Commands.   (line  3819)
* option <1>:                            SRFI-37.           (line 36704)
* option-names:                          SRFI-37.           (line 36723)
* option-optional-arg?:                  SRFI-37.           (line 36725)
* option-processor:                      SRFI-37.           (line 36726)
* option-ref:                            option-ref Reference.
                                                            (line 33870)
* option-required-arg?:                  SRFI-37.           (line 36724)
* or:                                    and or.            (line 18359)
* or <1>:                                rnrs base.         (line 38518)
* output-port?:                          Ports.             (line 19803)
* output-port? <1>:                      R6RS Output Ports. (line 21399)
* output-port? <2>:                      rnrs io simple.    (line 39503)
* package-stexi-documentation:           texinfo reflection.
                                                            (line 44096)
* package-stexi-documentation-for-include: texinfo reflection.
                                                            (line 44116)
* package-stexi-extended-menu:           texinfo reflection.
                                                            (line 44076)
* package-stexi-generic-menu:            texinfo reflection.
                                                            (line 44066)
* package-stexi-standard-copying:        texinfo reflection.
                                                            (line 44041)
* package-stexi-standard-menu:           texinfo reflection.
                                                            (line 44071)
* package-stexi-standard-prologue:       texinfo reflection.
                                                            (line 44081)
* package-stexi-standard-titlepage:      texinfo reflection.
                                                            (line 44048)
* pair-fold:                             SRFI-1 Fold and Map.
                                                            (line 34301)
* pair-fold-right:                       SRFI-1 Fold and Map.
                                                            (line 34302)
* pair-for-each:                         SRFI-1 Fold and Map.
                                                            (line 34437)
* pair?:                                 Pairs.             (line 11808)
* pair? <1>:                             rnrs base.         (line 38432)
* pair? <2>:                             Inlined Scheme Instructions.
                                                            (line 48472)
* par-for-each:                          Parallel Forms.    (line 26555)
* par-map:                               Parallel Forms.    (line 26554)
* parallel:                              Parallel Forms.    (line 26541)
* parameterize:                          Parameters.        (line 26367)
* parse-c-struct:                        Foreign Structs.   (line 25433)
* parse-header:                          HTTP.              (line 32355)
* parse-http-method:                     HTTP.              (line 32374)
* parse-http-version:                    HTTP.              (line 32378)
* parse-path:                            Load Paths.        (line 23058)
* parse-path-with-ellipsis:              Load Paths.        (line 23064)
* parse-request-uri:                     HTTP.              (line 32382)
* partial-cont-call:                     Trampoline Instructions.
                                                            (line 48153)
* partition:                             SRFI-1 Filtering and Partitioning.
                                                            (line 34457)
* partition <1>:                         rnrs lists.        (line 38850)
* partition!:                            SRFI-1 Filtering and Partitioning.
                                                            (line 34458)
* passwd:dir:                            User Information.  (line 29931)
* passwd:gecos:                          User Information.  (line 29929)
* passwd:gid:                            User Information.  (line 29927)
* passwd:name:                           User Information.  (line 29921)
* passwd:passwd:                         User Information.  (line 29923)
* passwd:shell:                          User Information.  (line 29933)
* passwd:uid:                            User Information.  (line 29925)
* pause:                                 Signals.           (line 30773)
* pclose:                                Pipes.             (line 30946)
* peek-char:                             Reading.           (line 19922)
* peek-char <1>:                         rnrs io simple.    (line 39521)
* peek-char <2>:                         rnrs io simple.    (line 39522)
* peek-next-char:                        sxml ssax input-parse.
                                                            (line 43548)
* pipe:                                  Ports and File Descriptors.
                                                            (line 29322)
* PKG_CHECK_MODULES:                     Autoconf Macros.   (line  6429)
* pointer->bytevector:                   Void Pointers and Byte Access.
                                                            (line 25274)
* pointer->procedure:                    Dynamic FFI.       (line 25458)
* pointer->scm:                          Foreign Variables. (line 25245)
* pointer->string:                       Void Pointers and Byte Access.
                                                            (line 25311)
* pointer-address:                       Foreign Variables. (line 25217)
* pointer?:                              Foreign Variables. (line 25229)
* poll-coop-repl-server:                 Cooperative REPL Servers.
                                                            (line 23370)
* popen:                                 Pipes.             (line 30891)
* port->fdes:                            Ports and File Descriptors.
                                                            (line 29214)
* port->stream:                          SRFI-41 Stream Library.
                                                            (line 37010)
* port->stream <1>:                      Streams.           (line 41938)
* port-closed?:                          Closing.           (line 20073)
* port-column:                           Reading.           (line 19971)
* port-conversion-strategy:              Ports.             (line 19850)
* port-encoding:                         Ports.             (line 19829)
* port-eof?:                             R6RS Input Ports.  (line 21127)
* port-filename:                         File Ports.        (line 20549)
* port-for-each:                         Ports and File Descriptors.
                                                            (line 29413)
* port-has-port-position?:               R6RS Port Manipulation.
                                                            (line 21102)
* port-has-set-port-position!?:          R6RS Port Manipulation.
                                                            (line 21113)
* port-line:                             Reading.           (line 19972)
* port-mode:                             File Ports.        (line 20542)
* port-mode <1>:                         Ports and File Descriptors.
                                                            (line 29407)
* port-position:                         R6RS Port Manipulation.
                                                            (line 21093)
* port-revealed:                         Ports and File Descriptors.
                                                            (line 29200)
* port-transcoder:                       R6RS Port Manipulation.
                                                            (line 21050)
* port-with-print-state:                 Writing.           (line 20009)
* port?:                                 Ports.             (line 19808)
* port? <1>:                             R6RS Port Manipulation.
                                                            (line 21047)
* positive?:                             Comparison.        (line  7771)
* positive? <1>:                         rnrs base.         (line 38583)
* post-order:                            Transforming SXML. (line 43254)
* pre-post-order:                        Transforming SXML. (line 43256)
* pretty-print:                          Inspect Commands.  (line  3807)
* pretty-print <1>:                      Pretty Printing.   (line 40659)
* primitive-eval:                        Fly Evaluation.    (line 22733)
* primitive-exit:                        Processes.         (line 30512)
* primitive-fork:                        Processes.         (line 30569)
* primitive-generic-generic:             Extending Primitives.
                                                            (line 44760)
* primitive-load:                        Loading.           (line 22902)
* primitive-load-path:                   Load Paths.        (line 22990)
* primitive-move->fdes:                  Ports and File Descriptors.
                                                            (line 29240)
* primitive-_exit:                       Processes.         (line 30513)
* print-options:                         Scheme Write.      (line 22583)
* print-set!:                            Scheme Write.      (line 22610)
* procedure:                             Debug Commands.    (line  3745)
* procedure <1>:                         Procedures with Setters.
                                                            (line 16038)
* procedure->pointer:                    Dynamic FFI.       (line 25554)
* procedure-documentation:               Procedure Properties.
                                                            (line 15981)
* procedure-execution-count:             Code Coverage.     (line 28966)
* procedure-name:                        Procedure Properties.
                                                            (line 15953)
* procedure-properties:                  Procedure Properties.
                                                            (line 15962)
* procedure-property:                    Procedure Properties.
                                                            (line 15966)
* procedure-source:                      Procedure Properties.
                                                            (line 15957)
* procedure-with-setter?:                Procedures with Setters.
                                                            (line 16033)
* procedure?:                            Procedure Properties.
                                                            (line 15940)
* procedure? <1>:                        rnrs base.         (line 38472)
* profile:                               Profile Commands.  (line  3704)
* program-arguments:                     Runtime Environment.
                                                            (line 30192)
* program-arguments-alist:               Compiled Procedures.
                                                            (line 15542)
* program-arities:                       Compiled Procedures.
                                                            (line 15510)
* program-arity:                         Compiled Procedures.
                                                            (line 15512)
* program-bindings:                      Compiled Procedures.
                                                            (line 15478)
* program-free-variables:                Compiled Procedures.
                                                            (line 15456)
* program-lambda-list:                   Compiled Procedures.
                                                            (line 15559)
* program-meta:                          Compiled Procedures.
                                                            (line 15469)
* program-module:                        Compiled Procedures.
                                                            (line 15450)
* program-objcode:                       Compiled Procedures.
                                                            (line 15440)
* program-objects:                       Compiled Procedures.
                                                            (line 15445)
* program-sources:                       Compiled Procedures.
                                                            (line 15495)
* program?:                              Compiled Procedures.
                                                            (line 15436)
* promise?:                              Delayed Evaluation.
                                                            (line 23171)
* promise? <1>:                          SRFI-45.           (line 37761)
* prompt:                                Dynamic Environment Instructions.
                                                            (line 48378)
* proper-list?:                          SRFI-1 Predicates. (line 34070)
* protoent:aliases:                      Network Databases. (line 31354)
* protoent:name:                         Network Databases. (line 31352)
* protoent:proto:                        Network Databases. (line 31356)
* provide:                               Feature Manipulation.
                                                            (line 26768)
* provided?:                             Feature Manipulation.
                                                            (line 26761)
* PTR2SCM:                               Non-immediate objects.
                                                            (line 47252)
* push-rest:                             Function Prologue Instructions.
                                                            (line 48044)
* put-bytevector:                        R6RS Binary Output.
                                                            (line 21500)
* put-char:                              R6RS Textual Output.
                                                            (line 21508)
* put-datum:                             R6RS Textual Output.
                                                            (line 21523)
* put-string:                            R6RS Textual Output.
                                                            (line 21512)
* put-string <1>:                        R6RS Textual Output.
                                                            (line 21513)
* put-string <2>:                        R6RS Textual Output.
                                                            (line 21514)
* put-u8:                                R6RS Binary Output.
                                                            (line 21495)
* putenv:                                Runtime Environment.
                                                            (line 30280)
* pwd:                                   Processes.         (line 30300)
* q-empty-check:                         Queues.            (line 41827)
* q-empty?:                              Queues.            (line 41824)
* q-front:                               Queues.            (line 41830)
* q-length:                              Queues.            (line 41821)
* q-pop!:                                Queues.            (line 41810)
* q-push!:                               Queues.            (line 41818)
* q-rear:                                Queues.            (line 41834)
* q-remove!:                             Queues.            (line 41838)
* q?:                                    Queues.            (line 41799)
* quasiquote:                            Expression Syntax. (line 22355)
* quasiquote <1>:                        rnrs base.         (line 38507)
* quasisyntax:                           rnrs syntax-case.  (line 39938)
* quit:                                  System Commands.   (line  3824)
* quit <1>:                              Processes.         (line 30501)
* quo:                                   Inlined Mathematical Instructions.
                                                            (line 48512)
* quote:                                 Expression Syntax. (line 22337)
* quote <1>:                             rnrs base.         (line 38506)
* quotient:                              Integer Operations.
                                                            (line  7678)
* quotient <1>:                          rnrs r5rs.         (line 40245)
* raise:                                 Signals.           (line 30703)
* raise <1>:                             SRFI-18 Exceptions.
                                                            (line 35854)
* raise <2>:                             rnrs exceptions.   (line 39246)
* raise-continuable:                     rnrs exceptions.   (line 39252)
* random:                                Random.            (line  8323)
* random-integer:                        SRFI-27 Default Random Source.
                                                            (line 36392)
* random-real:                           SRFI-27 Default Random Source.
                                                            (line 36397)
* random-source-make-integers:           SRFI-27 Random Number Generators.
                                                            (line 36450)
* random-source-make-reals:              SRFI-27 Random Number Generators.
                                                            (line 36472)
* random-source-make-reals <1>:          SRFI-27 Random Number Generators.
                                                            (line 36473)
* random-source-pseudo-randomize!:       SRFI-27 Random Sources.
                                                            (line 36428)
* random-source-randomize!:              SRFI-27 Random Sources.
                                                            (line 36423)
* random-source-state-ref:               SRFI-27 Random Sources.
                                                            (line 36440)
* random-source-state-set!:              SRFI-27 Random Sources.
                                                            (line 36441)
* random-source?:                        SRFI-27 Random Sources.
                                                            (line 36419)
* random-state->datum:                   Random.            (line  8377)
* random-state-from-platform:            Random.            (line  8382)
* random:exp:                            Random.            (line  8331)
* random:hollow-sphere!:                 Random.            (line  8337)
* random:normal:                         Random.            (line  8344)
* random:normal-vector!:                 Random.            (line  8351)
* random:solid-sphere!:                  Random.            (line  8357)
* random:uniform:                        Random.            (line  8364)
* rational-valued?:                      rnrs base.         (line 38692)
* rational?:                             Reals and Rationals.
                                                            (line  7418)
* rational? <1>:                         rnrs base.         (line 38553)
* rationalize:                           Reals and Rationals.
                                                            (line  7425)
* rationalize <1>:                       rnrs base.         (line 38556)
* re-export:                             Creating Guile Modules.
                                                            (line 24151)
* read:                                  Scheme Read.       (line 22490)
* read <1>:                              rnrs io simple.    (line 39528)
* read <2>:                              rnrs io simple.    (line 39529)
* read-char:                             Reading.           (line 19904)
* read-char <1>:                         rnrs io simple.    (line 39523)
* read-char <2>:                         rnrs io simple.    (line 39524)
* read-client:                           Web Server.        (line 33303)
* read-delimited:                        Line/Delimited.    (line 20161)
* read-delimited!:                       Line/Delimited.    (line 20167)
* read-disable:                          Scheme Read.       (line 22536)
* read-enable:                           Scheme Read.       (line 22535)
* read-hash-extend:                      Reader Extensions. (line 22479)
* read-header:                           HTTP.              (line 32347)
* read-headers:                          HTTP.              (line 32363)
* read-line:                             Line/Delimited.    (line 20131)
* read-line!:                            Line/Delimited.    (line 20155)
* read-options:                          Scheme Read.       (line 22499)
* read-request:                          Requests.          (line 32925)
* read-request-body:                     Requests.          (line 32949)
* read-request-line:                     HTTP.              (line 32387)
* read-response:                         Responses.         (line 33035)
* read-response-body:                    Responses.         (line 33083)
* read-response-line:                    HTTP.              (line 32394)
* read-set!:                             Scheme Read.       (line 22537)
* read-string:                           Line/Delimited.    (line 20197)
* read-string <1>:                       sxml ssax input-parse.
                                                            (line 43563)
* read-string!:                          Line/Delimited.    (line 20206)
* read-string!/partial:                  Block Reading and Writing.
                                                            (line 20255)
* read-text-line:                        sxml ssax input-parse.
                                                            (line 43561)
* read-with-shared-structure:            SRFI-38.           (line 36812)
* read-with-shared-structure <1>:        SRFI-38.           (line 36813)
* readdir:                               File System.       (line 29778)
* readline:                              Readline Functions.
                                                            (line 40529)
* readline-disable:                      Readline Options.  (line 40500)
* readline-enable:                       Readline Options.  (line 40499)
* readline-options:                      Readline Options.  (line 40498)
* readline-port:                         Readline Functions.
                                                            (line 40550)
* readline-set!:                         Readline Options.  (line 40501)
* readlink:                              File System.       (line 29658)
* real->flonum:                          rnrs arithmetic flonums.
                                                            (line 39732)
* real-part:                             Complex.           (line  7821)
* real-part <1>:                         rnrs base.         (line 38532)
* real-valued?:                          rnrs base.         (line 38691)
* real?:                                 Reals and Rationals.
                                                            (line  7411)
* real? <1>:                             rnrs base.         (line 38552)
* rec:                                   SRFI-31.           (line 36500)
* receive:                               Multiple Values.   (line 18924)
* record-accessor:                       Records.           (line 13825)
* record-accessor <1>:                   rnrs records procedural.
                                                            (line 39138)
* record-constructor:                    Records.           (line 13807)
* record-constructor <1>:                rnrs records procedural.
                                                            (line 39130)
* record-constructor-descriptor:         rnrs records syntactic.
                                                            (line 39088)
* record-field-mutable?:                 rnrs records inspection.
                                                            (line 39189)
* record-modifier:                       Records.           (line 13834)
* record-mutator:                        rnrs records procedural.
                                                            (line 39142)
* record-predicate:                      Records.           (line 13819)
* record-predicate <1>:                  rnrs records procedural.
                                                            (line 39134)
* record-rtd:                            rnrs records inspection.
                                                            (line 39157)
* record-type-descriptor:                Records.           (line 13845)
* record-type-descriptor <1>:            rnrs records syntactic.
                                                            (line 39084)
* record-type-descriptor?:               rnrs records procedural.
                                                            (line 39113)
* record-type-field-names:               rnrs records inspection.
                                                            (line 39184)
* record-type-fields:                    Records.           (line 13860)
* record-type-generative?:               rnrs records inspection.
                                                            (line 39172)
* record-type-name:                      Records.           (line 13854)
* record-type-name <1>:                  rnrs records inspection.
                                                            (line 39161)
* record-type-opaque?:                   rnrs records inspection.
                                                            (line 39180)
* record-type-parent:                    rnrs records inspection.
                                                            (line 39164)
* record-type-sealed?:                   rnrs records inspection.
                                                            (line 39176)
* record-type-uid:                       rnrs records inspection.
                                                            (line 39168)
* record?:                               Records.           (line 13786)
* record? <1>:                           rnrs records inspection.
                                                            (line 39153)
* recv!:                                 Network Sockets and Communication.
                                                            (line 31765)
* recvfrom!:                             Network Sockets and Communication.
                                                            (line 31794)
* redirect-port:                         Ports and File Descriptors.
                                                            (line 29383)
* reduce:                                SRFI-1 Fold and Map.
                                                            (line 34306)
* reduce-right:                          SRFI-1 Fold and Map.
                                                            (line 34307)
* regexp-exec:                           Regexp Functions.  (line 21941)
* regexp-match?:                         Match Structures.  (line 22115)
* regexp-quote:                          Backslash Escapes. (line 22207)
* regexp-substitute:                     Regexp Functions.  (line 22017)
* regexp-substitute/global:              Regexp Functions.  (line 22052)
* regexp?:                               Regexp Functions.  (line 21980)
* registers:                             Debug Commands.    (line  3760)
* release-arbiter:                       Arbiters.          (line 25640)
* release-port-handle:                   Ports and File Descriptors.
                                                            (line 29256)
* reload:                                Module Commands.   (line  3659)
* reload-module:                         Module System Reflection.
                                                            (line 24499)
* rem:                                   Inlined Mathematical Instructions.
                                                            (line 48513)
* remainder:                             Integer Operations.
                                                            (line  7679)
* remainder <1>:                         rnrs r5rs.         (line 40246)
* remove:                                SRFI-1 Filtering and Partitioning.
                                                            (line 34474)
* remove <1>:                            rnrs lists.        (line 38862)
* remove!:                               SRFI-1 Filtering and Partitioning.
                                                            (line 34475)
* remove-class-accessors!:               Customizing Class Redefinition.
                                                            (line 46478)
* remove-hook!:                          Hook Reference.    (line 17688)
* remp:                                  rnrs lists.        (line 38861)
* remq:                                  rnrs lists.        (line 38864)
* remv:                                  rnrs lists.        (line 38863)
* rename:                                File System.       (line 29736)
* rename-file:                           File System.       (line 29736)
* repl-default-option-set!:              System Commands.   (line  3854)
* replace-range:                         Transforming SXML. (line 43258)
* replace-titles:                        texinfo docbook.   (line 43738)
* request-absolute-uri:                  Requests.          (line 33001)
* request-accept:                        Requests.          (line 32961)
* request-accept-charset:                Requests.          (line 32962)
* request-accept-encoding:               Requests.          (line 32963)
* request-accept-language:               Requests.          (line 32964)
* request-allow:                         Requests.          (line 32965)
* request-authorization:                 Requests.          (line 32966)
* request-cache-control:                 Requests.          (line 32967)
* request-connection:                    Requests.          (line 32968)
* request-content-encoding:              Requests.          (line 32969)
* request-content-language:              Requests.          (line 32970)
* request-content-length:                Requests.          (line 32971)
* request-content-location:              Requests.          (line 32972)
* request-content-md5:                   Requests.          (line 32973)
* request-content-range:                 Requests.          (line 32974)
* request-content-type:                  Requests.          (line 32975)
* request-date:                          Requests.          (line 32976)
* request-expect:                        Requests.          (line 32977)
* request-expires:                       Requests.          (line 32978)
* request-from:                          Requests.          (line 32979)
* request-headers:                       Requests.          (line 32905)
* request-host:                          Requests.          (line 32980)
* request-if-match:                      Requests.          (line 32981)
* request-if-modified-since:             Requests.          (line 32982)
* request-if-none-match:                 Requests.          (line 32983)
* request-if-range:                      Requests.          (line 32984)
* request-if-unmodified-since:           Requests.          (line 32985)
* request-last-modified:                 Requests.          (line 32986)
* request-max-forwards:                  Requests.          (line 32987)
* request-meta:                          Requests.          (line 32906)
* request-method:                        Requests.          (line 32902)
* request-port:                          Requests.          (line 32907)
* request-pragma:                        Requests.          (line 32988)
* request-proxy-authorization:           Requests.          (line 32989)
* request-range:                         Requests.          (line 32990)
* request-referer:                       Requests.          (line 32991)
* request-te:                            Requests.          (line 32992)
* request-trailer:                       Requests.          (line 32993)
* request-transfer-encoding:             Requests.          (line 32994)
* request-upgrade:                       Requests.          (line 32995)
* request-uri:                           Requests.          (line 32903)
* request-user-agent:                    Requests.          (line 32996)
* request-version:                       Requests.          (line 32904)
* request-via:                           Requests.          (line 32997)
* request-warning:                       Requests.          (line 32998)
* request?:                              Requests.          (line 32901)
* require:                               SLIB.              (line 28990)
* require-extension:                     SRFI-55.           (line 37853)
* reserve-locals:                        Function Prologue Instructions.
                                                            (line 48102)
* reset:                                 Shift and Reset.   (line 18718)
* reset-hook!:                           Hook Reference.    (line 17693)
* reset-parsed-entity-definitions!:      SSAX.              (line 43150)
* resolve-interface:                     Module System Reflection.
                                                            (line 24485)
* resolve-module:                        Module System Reflection.
                                                            (line 24475)
* response-accept-ranges:                Responses.         (line 33096)
* response-age:                          Responses.         (line 33097)
* response-allow:                        Responses.         (line 33098)
* response-body-port:                    Responses.         (line 33073)
* response-cache-control:                Responses.         (line 33099)
* response-code:                         Responses.         (line 33017)
* response-connection:                   Responses.         (line 33100)
* response-content-encoding:             Responses.         (line 33101)
* response-content-language:             Responses.         (line 33102)
* response-content-length:               Responses.         (line 33103)
* response-content-location:             Responses.         (line 33104)
* response-content-md5:                  Responses.         (line 33105)
* response-content-range:                Responses.         (line 33106)
* response-content-type:                 Responses.         (line 33107)
* response-date:                         Responses.         (line 33108)
* response-etag:                         Responses.         (line 33109)
* response-expires:                      Responses.         (line 33110)
* response-headers:                      Responses.         (line 33019)
* response-last-modified:                Responses.         (line 33111)
* response-location:                     Responses.         (line 33112)
* response-must-not-include-body?:       Responses.         (line 33065)
* response-port:                         Responses.         (line 33020)
* response-pragma:                       Responses.         (line 33113)
* response-proxy-authenticate:           Responses.         (line 33114)
* response-reason-phrase:                Responses.         (line 33018)
* response-retry-after:                  Responses.         (line 33115)
* response-server:                       Responses.         (line 33116)
* response-trailer:                      Responses.         (line 33117)
* response-transfer-encoding:            Responses.         (line 33118)
* response-upgrade:                      Responses.         (line 33119)
* response-vary:                         Responses.         (line 33120)
* response-version:                      Responses.         (line 33016)
* response-via:                          Responses.         (line 33121)
* response-warning:                      Responses.         (line 33122)
* response-www-authenticate:             Responses.         (line 33123)
* response?:                             Responses.         (line 33015)
* restore-signals:                       Signals.           (line 30757)
* restricted-vector-sort!:               Sorting.           (line 17520)
* return:                                Procedure Call and Return Instructions.
                                                            (line 47947)
* return/nvalues:                        Procedure Call and Return Instructions.
                                                            (line 47958)
* return/values:                         Procedure Call and Return Instructions.
                                                            (line 47957)
* return/values*:                        Procedure Call and Return Instructions.
                                                            (line 47972)
* reverse:                               Append/Reverse.    (line 12108)
* reverse <1>:                           rnrs base.         (line 38600)
* reverse!:                              Append/Reverse.    (line 12109)
* reverse-bit-field:                     SRFI-60.           (line 37943)
* reverse-list->string:                  String Constructors.
                                                            (line  9299)
* reverse-list->vector:                  SRFI-43 Conversion.
                                                            (line 37723)
* reverse-vector->list:                  SRFI-43 Conversion.
                                                            (line 37712)
* rewinddir:                             File System.       (line 29784)
* right-justify-string:                  texinfo string-utils.
                                                            (line 43904)
* rmdir:                                 File System.       (line 29759)
* rotate-bit-field:                      SRFI-60.           (line 37934)
* round:                                 Arithmetic.        (line  7908)
* round <1>:                             rnrs base.         (line 38644)
* round-ash:                             Bitwise Operations.
                                                            (line  8238)
* round-quotient:                        Arithmetic.        (line  8059)
* round-remainder:                       Arithmetic.        (line  8060)
* round/:                                Arithmetic.        (line  8058)
* run-asyncs:                            User asyncs.       (line 25756)
* run-hook:                              Hook Reference.    (line 17702)
* run-server:                            REPL Servers.      (line 23321)
* run-server <1>:                        Web Server.        (line 33359)
* s16vector:                             SRFI-4 API.        (line 35080)
* s16vector->list:                       SRFI-4 API.        (line 35188)
* s16vector-length:                      SRFI-4 API.        (line 35108)
* s16vector-ref:                         SRFI-4 API.        (line 35134)
* s16vector-set!:                        SRFI-4 API.        (line 35161)
* s16vector?:                            SRFI-4 API.        (line 35024)
* s32vector:                             SRFI-4 API.        (line 35082)
* s32vector->list:                       SRFI-4 API.        (line 35190)
* s32vector-length:                      SRFI-4 API.        (line 35110)
* s32vector-ref:                         SRFI-4 API.        (line 35136)
* s32vector-set!:                        SRFI-4 API.        (line 35163)
* s32vector?:                            SRFI-4 API.        (line 35026)
* s64vector:                             SRFI-4 API.        (line 35084)
* s64vector->list:                       SRFI-4 API.        (line 35192)
* s64vector-length:                      SRFI-4 API.        (line 35112)
* s64vector-ref:                         SRFI-4 API.        (line 35138)
* s64vector-set!:                        SRFI-4 API.        (line 35165)
* s64vector?:                            SRFI-4 API.        (line 35028)
* s8vector:                              SRFI-4 API.        (line 35078)
* s8vector->list:                        SRFI-4 API.        (line 35186)
* s8vector-length:                       SRFI-4 API.        (line 35106)
* s8vector-ref:                          SRFI-4 API.        (line 35132)
* s8vector-set!:                         SRFI-4 API.        (line 35159)
* s8vector?:                             SRFI-4 API.        (line 35022)
* sanitize-response:                     Web Server.        (line 33323)
* save-module-excursion:                 Module System Reflection.
                                                            (line 24464)
* scandir:                               File Tree Walk.    (line 41627)
* scheme-report-environment:             Environments.      (line 24732)
* scheme-report-environment <1>:         rnrs r5rs.         (line 40258)
* scm->pointer:                          Foreign Variables. (line 25242)
* scm-error:                             Error Reporting.   (line 19330)
* SCM2PTR:                               Non-immediate objects.
                                                            (line 47248)
* scm_abs:                               Arithmetic.        (line  7890)
* scm_accept:                            Network Sockets and Communication.
                                                            (line 31731)
* scm_access:                            File System.       (line 29551)
* scm_acons:                             Adding or Setting Alist Entries.
                                                            (line 14475)
* scm_add_feature:                       Feature Manipulation.
                                                            (line 26775)
* scm_add_hook_x:                        Hook Reference.    (line 17683)
* scm_alarm:                             Signals.           (line 30763)
* scm_alignof:                           Foreign Structs.   (line 25416)
* scm_all_threads:                       Threads.           (line 25774)
* scm_angle:                             Complex.           (line  7835)
* scm_any_to_c32vector:                  SRFI-4 Extensions. (line 35381)
* scm_any_to_c64vector:                  SRFI-4 Extensions. (line 35382)
* scm_any_to_f32vector:                  SRFI-4 Extensions. (line 35379)
* scm_any_to_f64vector:                  SRFI-4 Extensions. (line 35380)
* scm_any_to_s16vector:                  SRFI-4 Extensions. (line 35374)
* scm_any_to_s32vector:                  SRFI-4 Extensions. (line 35376)
* scm_any_to_s64vector:                  SRFI-4 Extensions. (line 35378)
* scm_any_to_s8vector:                   SRFI-4 Extensions. (line 35372)
* scm_any_to_u16vector:                  SRFI-4 Extensions. (line 35373)
* scm_any_to_u32vector:                  SRFI-4 Extensions. (line 35375)
* scm_any_to_u64vector:                  SRFI-4 Extensions. (line 35377)
* scm_any_to_u8vector:                   SRFI-4 Extensions. (line 35371)
* scm_append:                            Append/Reverse.    (line 12085)
* scm_append_x:                          Append/Reverse.    (line 12086)
* scm_apply:                             Fly Evaluation.    (line 22682)
* scm_apply_0:                           Fly Evaluation.    (line 22678)
* scm_apply_1:                           Fly Evaluation.    (line 22679)
* scm_apply_2:                           Fly Evaluation.    (line 22680)
* scm_apply_3:                           Fly Evaluation.    (line 22681)
* SCM_ARG1:                              Handling Errors.   (line 19685)
* SCM_ARG2:                              Handling Errors.   (line 19686)
* SCM_ARG3:                              Handling Errors.   (line 19687)
* SCM_ARG4:                              Handling Errors.   (line 19688)
* SCM_ARG5:                              Handling Errors.   (line 19689)
* SCM_ARG6:                              Handling Errors.   (line 19690)
* SCM_ARG7:                              Handling Errors.   (line 19691)
* SCM_ARGn:                              Handling Errors.   (line 19700)
* scm_array_contents:                    Shared Arrays.     (line 13111)
* scm_array_copy_x:                      Array Procedures.  (line 12924)
* scm_array_dimensions:                  Array Procedures.  (line 12892)
* scm_array_fill_x:                      Array Procedures.  (line 12930)
* scm_array_for_each:                    Array Procedures.  (line 12956)
* scm_array_get_handle:                  Accessing Arrays from C.
                                                            (line 13203)
* scm_array_handle_bit_elements:         Accessing Arrays from C.
                                                            (line 13373)
* scm_array_handle_bit_writable_elements: Accessing Arrays from C.
                                                            (line 13414)
* scm_array_handle_c32_elements:         Accessing Arrays from C.
                                                            (line 13334)
* scm_array_handle_c32_writable_elements: Accessing Arrays from C.
                                                            (line 13366)
* scm_array_handle_c64_elements:         Accessing Arrays from C.
                                                            (line 13336)
* scm_array_handle_c64_writable_elements: Accessing Arrays from C.
                                                            (line 13368)
* scm_array_handle_dims:                 Accessing Arrays from C.
                                                            (line 13235)
* scm_array_handle_elements:             Accessing Arrays from C.
                                                            (line 13286)
* scm_array_handle_f32_elements:         Accessing Arrays from C.
                                                            (line 13330)
* scm_array_handle_f32_writable_elements: Accessing Arrays from C.
                                                            (line 13362)
* scm_array_handle_f64_elements:         Accessing Arrays from C.
                                                            (line 13332)
* scm_array_handle_f64_writable_elements: Accessing Arrays from C.
                                                            (line 13364)
* scm_array_handle_pos:                  Accessing Arrays from C.
                                                            (line 13265)
* scm_array_handle_rank:                 Accessing Arrays from C.
                                                            (line 13217)
* scm_array_handle_ref:                  Accessing Arrays from C.
                                                            (line 13273)
* scm_array_handle_release:              Accessing Arrays from C.
                                                            (line 13212)
* scm_array_handle_s16_elements:         Accessing Arrays from C.
                                                            (line 13320)
* scm_array_handle_s16_writable_elements: Accessing Arrays from C.
                                                            (line 13352)
* scm_array_handle_s32_elements:         Accessing Arrays from C.
                                                            (line 13324)
* scm_array_handle_s32_writable_elements: Accessing Arrays from C.
                                                            (line 13356)
* scm_array_handle_s64_elements:         Accessing Arrays from C.
                                                            (line 13328)
* scm_array_handle_s64_writable_elements: Accessing Arrays from C.
                                                            (line 13360)
* scm_array_handle_s8_elements:          Accessing Arrays from C.
                                                            (line 13316)
* scm_array_handle_s8_writable_elements: Accessing Arrays from C.
                                                            (line 13348)
* scm_array_handle_set:                  Accessing Arrays from C.
                                                            (line 13279)
* scm_array_handle_u16_elements:         Accessing Arrays from C.
                                                            (line 13318)
* scm_array_handle_u16_writable_elements: Accessing Arrays from C.
                                                            (line 13350)
* scm_array_handle_u32_elements:         Accessing Arrays from C.
                                                            (line 13322)
* scm_array_handle_u32_writable_elements: Accessing Arrays from C.
                                                            (line 13354)
* scm_array_handle_u64_elements:         Accessing Arrays from C.
                                                            (line 13326)
* scm_array_handle_u64_writable_elements: Accessing Arrays from C.
                                                            (line 13358)
* scm_array_handle_u8_elements:          Accessing Arrays from C.
                                                            (line 13314)
* scm_array_handle_u8_writable_elements: Accessing Arrays from C.
                                                            (line 13346)
* scm_array_handle_uniform_elements:     Accessing Arrays from C.
                                                            (line 13297)
* scm_array_handle_uniform_element_size: Accessing Arrays from C.
                                                            (line 13309)
* scm_array_handle_uniform_writable_elements: Accessing Arrays from C.
                                                            (line 13304)
* scm_array_handle_writable_elements:    Accessing Arrays from C.
                                                            (line 13292)
* scm_array_index_map_x:                 Array Procedures.  (line 12961)
* scm_array_in_bounds_p:                 Array Procedures.  (line 12873)
* scm_array_length:                      Array Procedures.  (line 12906)
* scm_array_map_x:                       Array Procedures.  (line 12942)
* scm_array_p:                           Array Procedures.  (line 12796)
* scm_array_rank:                        Array Procedures.  (line 12912)
* scm_array_ref:                         Array Procedures.  (line 12866)
* scm_array_set_x:                       Array Procedures.  (line 12882)
* scm_array_to_list:                     Array Procedures.  (line 12919)
* scm_array_type:                        Array Procedures.  (line 12860)
* scm_ash:                               Bitwise Operations.
                                                            (line  8224)
* SCM_ASSERT:                            Handling Errors.   (line 19674)
* scm_assert_smob_type:                  Smobs.             (line 15231)
* SCM_ASSERT_TYPE:                       Handling Errors.   (line 19676)
* scm_assoc:                             Retrieving Alist Entries.
                                                            (line 14508)
* scm_assoc_ref:                         Retrieving Alist Entries.
                                                            (line 14522)
* scm_assoc_remove_x:                    Removing Alist Entries.
                                                            (line 14595)
* scm_assoc_set_x:                       Adding or Setting Alist Entries.
                                                            (line 14486)
* scm_assq:                              Retrieving Alist Entries.
                                                            (line 14506)
* scm_assq_ref:                          Retrieving Alist Entries.
                                                            (line 14520)
* scm_assq_remove_x:                     Removing Alist Entries.
                                                            (line 14593)
* scm_assq_set_x:                        Adding or Setting Alist Entries.
                                                            (line 14484)
* scm_assv:                              Retrieving Alist Entries.
                                                            (line 14507)
* scm_assv_ref:                          Retrieving Alist Entries.
                                                            (line 14521)
* scm_assv_remove_x:                     Removing Alist Entries.
                                                            (line 14594)
* scm_assv_set_x:                        Adding or Setting Alist Entries.
                                                            (line 14485)
* scm_async:                             User asyncs.       (line 25749)
* scm_async_mark:                        User asyncs.       (line 25753)
* scm_backtrace:                         Pre-Unwind Debugging.
                                                            (line 28212)
* scm_backtrace_with_highlights:         Pre-Unwind Debugging.
                                                            (line 28211)
* scm_basename:                          File System.       (line 29870)
* scm_bind:                              Network Sockets and Communication.
                                                            (line 31707)
* scm_bindtextdomain:                    Gettext Support.   (line 27669)
* scm_bind_textdomain_codeset:           Gettext Support.   (line 27685)
* scm_bitvector:                         Bit Vectors.       (line 12549)
* scm_bitvector_elements:                Bit Vectors.       (line 12649)
* scm_bitvector_fill_x:                  Bit Vectors.       (line 12577)
* scm_bitvector_length:                  Bit Vectors.       (line 12553)
* scm_bitvector_p:                       Bit Vectors.       (line 12534)
* scm_bitvector_ref:                     Bit Vectors.       (line 12561)
* scm_bitvector_set_x:                   Bit Vectors.       (line 12568)
* scm_bitvector_to_list:                 Bit Vectors.       (line 12586)
* scm_bitvector_writable_elements:       Bit Vectors.       (line 12658)
* scm_bit_count:                         Bit Vectors.       (line 12591)
* scm_bit_count_star:                    Bit Vectors.       (line 12634)
* scm_bit_extract:                       Bitwise Operations.
                                                            (line  8298)
* scm_bit_invert_x:                      Bit Vectors.       (line 12607)
* scm_bit_position:                      Bit Vectors.       (line 12598)
* scm_bit_set_star_x:                    Bit Vectors.       (line 12611)
* scm_boolean_p:                         Booleans.          (line  7024)
* scm_boot_guile:                        Initialization.    (line  6825)
* scm_broadcast_condition_variable:      Mutexes and Condition Variables.
                                                            (line 26038)
* scm_bytecode_to_objcode:               Bytecode and Objcode.
                                                            (line 49257)
* SCM_BYTEVECTOR_CONTENTS:               Bytevector Manipulation.
                                                            (line 10613)
* scm_bytevector_copy:                   Bytevector Manipulation.
                                                            (line 10597)
* scm_bytevector_copy_x:                 Bytevector Manipulation.
                                                            (line 10589)
* scm_bytevector_eq_p:                   Bytevector Manipulation.
                                                            (line 10579)
* scm_bytevector_fill_x:                 Bytevector Manipulation.
                                                            (line 10584)
* scm_bytevector_ieee_double_native_ref: Bytevectors as Floats.
                                                            (line 10809)
* scm_bytevector_ieee_double_native_set_x: Bytevectors as Floats.
                                                            (line 10817)
* scm_bytevector_ieee_double_ref:        Bytevectors as Floats.
                                                            (line 10790)
* scm_bytevector_ieee_double_set_x:      Bytevectors as Floats.
                                                            (line 10800)
* scm_bytevector_ieee_single_native_ref: Bytevectors as Floats.
                                                            (line 10808)
* scm_bytevector_ieee_single_native_set_x: Bytevectors as Floats.
                                                            (line 10815)
* scm_bytevector_ieee_single_ref:        Bytevectors as Floats.
                                                            (line 10789)
* scm_bytevector_ieee_single_set_x:      Bytevectors as Floats.
                                                            (line 10798)
* scm_bytevector_length:                 Bytevector Manipulation.
                                                            (line 10572)
* SCM_BYTEVECTOR_LENGTH:                 Bytevector Manipulation.
                                                            (line 10610)
* scm_bytevector_p:                      Bytevector Manipulation.
                                                            (line 10565)
* scm_bytevector_s16_native_ref:         Bytevectors as Integers.
                                                            (line 10715)
* scm_bytevector_s16_native_set_x:       Bytevectors as Integers.
                                                            (line 10731)
* scm_bytevector_s16_ref:                Bytevectors as Integers.
                                                            (line 10677)
* scm_bytevector_s16_set_x:              Bytevectors as Integers.
                                                            (line 10696)
* scm_bytevector_s32_native_ref:         Bytevectors as Integers.
                                                            (line 10717)
* scm_bytevector_s32_native_set_x:       Bytevectors as Integers.
                                                            (line 10733)
* scm_bytevector_s32_ref:                Bytevectors as Integers.
                                                            (line 10679)
* scm_bytevector_s32_set_x:              Bytevectors as Integers.
                                                            (line 10698)
* scm_bytevector_s64_native_ref:         Bytevectors as Integers.
                                                            (line 10719)
* scm_bytevector_s64_native_set_x:       Bytevectors as Integers.
                                                            (line 10735)
* scm_bytevector_s64_ref:                Bytevectors as Integers.
                                                            (line 10681)
* scm_bytevector_s64_set_x:              Bytevectors as Integers.
                                                            (line 10700)
* scm_bytevector_s8_ref:                 Bytevectors as Integers.
                                                            (line 10675)
* scm_bytevector_s8_set_x:               Bytevectors as Integers.
                                                            (line 10694)
* scm_bytevector_sint_ref:               Bytevectors as Integers.
                                                            (line 10645)
* scm_bytevector_sint_set_x:             Bytevectors as Integers.
                                                            (line 10658)
* scm_bytevector_to_pointer:             Void Pointers and Byte Access.
                                                            (line 25292)
* scm_bytevector_to_sint_list:           Bytevectors and Integer Lists.
                                                            (line 10766)
* scm_bytevector_to_u8_list:             Bytevectors and Integer Lists.
                                                            (line 10751)
* scm_bytevector_to_uint_list:           Bytevectors and Integer Lists.
                                                            (line 10761)
* scm_bytevector_u16_native_ref:         Bytevectors as Integers.
                                                            (line 10714)
* scm_bytevector_u16_native_set_x:       Bytevectors as Integers.
                                                            (line 10730)
* scm_bytevector_u16_ref:                Bytevectors as Integers.
                                                            (line 10676)
* scm_bytevector_u16_set_x:              Bytevectors as Integers.
                                                            (line 10695)
* scm_bytevector_u32_native_ref:         Bytevectors as Integers.
                                                            (line 10716)
* scm_bytevector_u32_native_set_x:       Bytevectors as Integers.
                                                            (line 10732)
* scm_bytevector_u32_ref:                Bytevectors as Integers.
                                                            (line 10678)
* scm_bytevector_u32_set_x:              Bytevectors as Integers.
                                                            (line 10697)
* scm_bytevector_u64_native_ref:         Bytevectors as Integers.
                                                            (line 10718)
* scm_bytevector_u64_native_set_x:       Bytevectors as Integers.
                                                            (line 10734)
* scm_bytevector_u64_ref:                Bytevectors as Integers.
                                                            (line 10680)
* scm_bytevector_u64_set_x:              Bytevectors as Integers.
                                                            (line 10699)
* scm_bytevector_u8_ref:                 Bytevectors as Integers.
                                                            (line 10674)
* scm_bytevector_u8_set_x:               Bytevectors as Integers.
                                                            (line 10693)
* scm_bytevector_uint_ref:               Bytevectors as Integers.
                                                            (line 10640)
* scm_bytevector_uint_set_x:             Bytevectors as Integers.
                                                            (line 10651)
* scm_c32vector:                         SRFI-4 API.        (line 35099)
* scm_c32vector_elements:                SRFI-4 API.        (line 35289)
* scm_c32vector_length:                  SRFI-4 API.        (line 35127)
* scm_c32vector_p:                       SRFI-4 API.        (line 35043)
* scm_c32vector_ref:                     SRFI-4 API.        (line 35153)
* scm_c32vector_set_x:                   SRFI-4 API.        (line 35180)
* scm_c32vector_to_list:                 SRFI-4 API.        (line 35207)
* scm_c32vector_writable_elements:       SRFI-4 API.        (line 35317)
* scm_c64vector:                         SRFI-4 API.        (line 35100)
* scm_c64vector_elements:                SRFI-4 API.        (line 35291)
* scm_c64vector_length:                  SRFI-4 API.        (line 35128)
* scm_c64vector_p:                       SRFI-4 API.        (line 35044)
* scm_c64vector_ref:                     SRFI-4 API.        (line 35154)
* scm_c64vector_set_x:                   SRFI-4 API.        (line 35181)
* scm_c64vector_to_list:                 SRFI-4 API.        (line 35208)
* scm_c64vector_writable_elements:       SRFI-4 API.        (line 35319)
* scm_caaaar:                            Pairs.             (line 11897)
* scm_caaadr:                            Pairs.             (line 11896)
* scm_caaar:                             Pairs.             (line 11881)
* scm_caadar:                            Pairs.             (line 11895)
* scm_caaddr:                            Pairs.             (line 11894)
* scm_caadr:                             Pairs.             (line 11880)
* scm_caar:                              Pairs.             (line 11873)
* scm_cadaar:                            Pairs.             (line 11893)
* scm_cadadr:                            Pairs.             (line 11892)
* scm_cadar:                             Pairs.             (line 11879)
* scm_caddar:                            Pairs.             (line 11891)
* scm_cadddr:                            Pairs.             (line 11890)
* scm_caddr:                             Pairs.             (line 11878)
* scm_cadr:                              Pairs.             (line 11872)
* scm_call:                              Fly Evaluation.    (line 22709)
* scm_calloc:                            Memory Blocks.     (line 23494)
* scm_call_0:                            Fly Evaluation.    (line 22694)
* scm_call_1:                            Fly Evaluation.    (line 22695)
* scm_call_2:                            Fly Evaluation.    (line 22696)
* scm_call_3:                            Fly Evaluation.    (line 22697)
* scm_call_4:                            Fly Evaluation.    (line 22698)
* scm_call_5:                            Fly Evaluation.    (line 22699)
* scm_call_6:                            Fly Evaluation.    (line 22700)
* scm_call_7:                            Fly Evaluation.    (line 22701)
* scm_call_8:                            Fly Evaluation.    (line 22703)
* scm_call_9:                            Fly Evaluation.    (line 22705)
* scm_call_n:                            Fly Evaluation.    (line 22718)
* scm_call_with_blocked_asyncs:          System asyncs.     (line 25706)
* scm_call_with_input_string:            String Ports.      (line 20614)
* scm_call_with_output_string:           String Ports.      (line 20587)
* scm_call_with_unblocked_asyncs:        System asyncs.     (line 25717)
* scm_cancel_thread:                     Threads.           (line 25833)
* scm_car:                               Pairs.             (line 11829)
* SCM_CAR:                               Pairs.             (line 11833)
* scm_catch:                             Catch.             (line 19054)
* scm_catch_with_pre_unwind_handler:     Catch.             (line 19052)
* scm_cdaaar:                            Pairs.             (line 11889)
* scm_cdaadr:                            Pairs.             (line 11888)
* scm_cdaar:                             Pairs.             (line 11877)
* scm_cdadar:                            Pairs.             (line 11887)
* scm_cdaddr:                            Pairs.             (line 11886)
* scm_cdadr:                             Pairs.             (line 11876)
* scm_cdar:                              Pairs.             (line 11871)
* scm_cddaar:                            Pairs.             (line 11885)
* scm_cddadr:                            Pairs.             (line 11884)
* scm_cddar:                             Pairs.             (line 11875)
* scm_cdddar:                            Pairs.             (line 11883)
* scm_cddddr:                            Pairs.             (line 11882)
* scm_cdddr:                             Pairs.             (line 11874)
* scm_cddr:                              Pairs.             (line 11870)
* scm_cdr:                               Pairs.             (line 11830)
* SCM_CDR:                               Pairs.             (line 11834)
* scm_ceiling:                           Arithmetic.        (line  7918)
* scm_ceiling_divide:                    Arithmetic.        (line  7980)
* scm_ceiling_quotient:                  Arithmetic.        (line  7981)
* scm_ceiling_remainder:                 Arithmetic.        (line  7982)
* scm_cell:                              Allocating Cells.  (line 47285)
* SCM_CELL_OBJECT:                       Accessing Cell Entries.
                                                            (line 47334)
* SCM_CELL_TYPE:                         Heap Cell Type Information.
                                                            (line 47305)
* SCM_CELL_WORD:                         Accessing Cell Entries.
                                                            (line 47324)
* scm_centered_divide:                   Arithmetic.        (line  8027)
* scm_centered_quotient:                 Arithmetic.        (line  8028)
* scm_centered_remainder:                Arithmetic.        (line  8029)
* scm_char_alphabetic_p:                 Characters.        (line  8576)
* scm_char_downcase:                     Characters.        (line  8638)
* scm_char_general_category:             Characters.        (line  8600)
* scm_char_is_both_p:                    Characters.        (line  8596)
* scm_char_locale_ci_eq:                 Text Collation.    (line 27318)
* scm_char_locale_ci_gt:                 Text Collation.    (line 27311)
* scm_char_locale_ci_lt:                 Text Collation.    (line 27309)
* scm_char_locale_downcase:              Character Case Mapping.
                                                            (line 27343)
* scm_char_locale_gt:                    Text Collation.    (line 27307)
* scm_char_locale_lt:                    Text Collation.    (line 27305)
* scm_char_locale_titlecase:             Character Case Mapping.
                                                            (line 27348)
* scm_char_locale_upcase:                Character Case Mapping.
                                                            (line 27338)
* scm_char_lower_case_p:                 Characters.        (line  8592)
* scm_char_numeric_p:                    Characters.        (line  8580)
* scm_char_p:                            Characters.        (line  8519)
* scm_char_ready_p:                      Reading.           (line 19890)
* scm_char_set:                          Creating Character Sets.
                                                            (line  8783)
* scm_char_set_adjoin:                   Character-Set Algebra.
                                                            (line  8916)
* scm_char_set_adjoin_x:                 Character-Set Algebra.
                                                            (line  8926)
* scm_char_set_any:                      Querying Character Sets.
                                                            (line  8903)
* scm_char_set_complement:               Character-Set Algebra.
                                                            (line  8936)
* scm_char_set_complement_x:             Character-Set Algebra.
                                                            (line  8967)
* scm_char_set_contains_p:               Querying Character Sets.
                                                            (line  8893)
* scm_char_set_copy:                     Creating Character Sets.
                                                            (line  8778)
* scm_char_set_count:                    Querying Character Sets.
                                                            (line  8878)
* scm_char_set_cursor:                   Iterating Over Character Sets.
                                                            (line  8715)
* scm_char_set_cursor_next:              Iterating Over Character Sets.
                                                            (line  8725)
* scm_char_set_delete:                   Character-Set Algebra.
                                                            (line  8921)
* scm_char_set_delete_x:                 Character-Set Algebra.
                                                            (line  8931)
* scm_char_set_difference:               Character-Set Algebra.
                                                            (line  8954)
* scm_char_set_difference_x:             Character-Set Algebra.
                                                            (line  8979)
* scm_char_set_diff_plus_intersection:   Character-Set Algebra.
                                                            (line  8962)
* scm_char_set_diff_plus_intersection_x: Character-Set Algebra.
                                                            (line  8987)
* scm_char_set_eq:                       Character Set Predicates/Comparison.
                                                            (line  8687)
* scm_char_set_every:                    Querying Character Sets.
                                                            (line  8898)
* scm_char_set_filter:                   Creating Character Sets.
                                                            (line  8809)
* scm_char_set_filter_x:                 Creating Character Sets.
                                                            (line  8815)
* scm_char_set_fold:                     Iterating Over Character Sets.
                                                            (line  8736)
* scm_char_set_for_each:                 Iterating Over Character Sets.
                                                            (line  8763)
* scm_char_set_hash:                     Character Set Predicates/Comparison.
                                                            (line  8696)
* scm_char_set_intersection:             Character-Set Algebra.
                                                            (line  8950)
* scm_char_set_intersection_x:           Character-Set Algebra.
                                                            (line  8975)
* scm_char_set_leq:                      Character Set Predicates/Comparison.
                                                            (line  8691)
* scm_char_set_map:                      Iterating Over Character Sets.
                                                            (line  8768)
* scm_char_set_p:                        Character Set Predicates/Comparison.
                                                            (line  8683)
* scm_char_set_ref:                      Iterating Over Character Sets.
                                                            (line  8719)
* scm_char_set_size:                     Querying Character Sets.
                                                            (line  8874)
* scm_char_set_to_list:                  Querying Character Sets.
                                                            (line  8883)
* scm_char_set_to_string:                Querying Character Sets.
                                                            (line  8887)
* scm_char_set_unfold:                   Iterating Over Character Sets.
                                                            (line  8741)
* scm_char_set_unfold_x:                 Iterating Over Character Sets.
                                                            (line  8752)
* scm_char_set_union:                    Character-Set Algebra.
                                                            (line  8946)
* scm_char_set_union_x:                  Character-Set Algebra.
                                                            (line  8971)
* scm_char_set_xor:                      Character-Set Algebra.
                                                            (line  8958)
* scm_char_set_xor_x:                    Character-Set Algebra.
                                                            (line  8983)
* scm_char_titlecase:                    Characters.        (line  8642)
* scm_char_to_integer:                   Characters.        (line  8624)
* scm_char_upcase:                       Characters.        (line  8634)
* scm_char_upper_case_p:                 Characters.        (line  8588)
* scm_char_whitespace_p:                 Characters.        (line  8584)
* scm_chdir:                             Processes.         (line 30296)
* scm_chmod:                             File System.       (line 29677)
* scm_chown:                             File System.       (line 29664)
* scm_chroot:                            Processes.         (line 30315)
* scm_close:                             Ports and File Descriptors.
                                                            (line 29295)
* scm_closedir:                          File System.       (line 29790)
* scm_close_fdes:                        Ports and File Descriptors.
                                                            (line 29303)
* scm_close_input_port:                  Closing.           (line 20064)
* scm_close_output_port:                 Closing.           (line 20065)
* scm_close_port:                        Closing.           (line 20055)
* scm_complex_p:                         Complex Numbers.   (line  7516)
* scm_condition_variable_p:              Mutexes and Condition Variables.
                                                            (line 26011)
* scm_connect:                           Network Sockets and Communication.
                                                            (line 31693)
* scm_cons:                              Pairs.             (line 11803)
* scm_cons_source:                       Source Properties. (line 27979)
* scm_copy_file:                         File System.       (line 29706)
* scm_copy_random_state:                 Random.            (line  8320)
* scm_copy_tree:                         Copying.           (line 17538)
* SCM_CRITICAL_SECTION_END:              Critical Sections. (line 26131)
* SCM_CRITICAL_SECTION_START:            Critical Sections. (line 26130)
* scm_crypt:                             Encryption.        (line 31974)
* scm_ctermid:                           Terminals and Ptys.
                                                            (line 30859)
* scm_current_dynamic_state:             Fluids and Dynamic States.
                                                            (line 26291)
* scm_current_error_port:                Default Ports.     (line 20348)
* scm_current_input_port:                Default Ports.     (line 20316)
* scm_current_load_port:                 Loading.           (line 22949)
* scm_current_module:                    Module System Reflection.
                                                            (line 24456)
* scm_current_output_port:               Default Ports.     (line 20333)
* scm_current_processor_count:           Processes.         (line 30658)
* scm_current_thread:                    Threads.           (line 25778)
* scm_current_time:                      Time.              (line 30023)
* scm_c_angle:                           Complex.           (line  7848)
* scm_c_array_rank:                      Array Procedures.  (line 12915)
* scm_c_bind_keyword_arguments:          Keyword Procedures.
                                                            (line 11670)
* scm_c_bitvector_length:                Bit Vectors.       (line 12556)
* scm_c_bitvector_ref:                   Bit Vectors.       (line 12564)
* scm_c_bitvector_set_x:                 Bit Vectors.       (line 12572)
* scm_c_bytevector_length:               Bytevector Manipulation.
                                                            (line 10575)
* scm_c_bytevector_ref:                  Bytevector Manipulation.
                                                            (line 10600)
* scm_c_bytevector_set_x:                Bytevector Manipulation.
                                                            (line 10603)
* scm_c_call_with_blocked_asyncs:        System asyncs.     (line 25712)
* scm_c_call_with_current_module:        Accessing Modules from C.
                                                            (line 24545)
* scm_c_call_with_unblocked_asyncs:      System asyncs.     (line 25723)
* scm_c_catch:                           Catch.             (line 19105)
* scm_c_define:                          Top Level.         (line 17928)
* scm_c_define <1>:                      Accessing Modules from C.
                                                            (line 24630)
* scm_c_define_gsubr:                    Primitive Procedures.
                                                            (line 15398)
* scm_c_define_module:                   Accessing Modules from C.
                                                            (line 24659)
* scm_c_downcase:                        Characters.        (line  8653)
* scm_c_eval_string:                     Fly Evaluation.    (line 22673)
* scm_c_export:                          Accessing Modules from C.
                                                            (line 24682)
* scm_c_hook_add:                        C Hooks.           (line 17801)
* scm_c_hook_init:                       C Hooks.           (line 17773)
* scm_c_hook_remove:                     C Hooks.           (line 17807)
* scm_c_hook_run:                        C Hooks.           (line 17817)
* scm_c_imag_part:                       Complex.           (line  7844)
* scm_c_locale_stringn_to_number:        Conversion.        (line  7802)
* scm_c_lookup:                          Accessing Modules from C.
                                                            (line 24611)
* scm_c_magnitude:                       Complex.           (line  7847)
* scm_c_make_bitvector:                  Bit Vectors.       (line 12545)
* scm_c_make_bytevector:                 Bytevector Manipulation.
                                                            (line 10560)
* scm_c_make_gsubr:                      Primitive Procedures.
                                                            (line 15386)
* scm_c_make_polar:                      Complex.           (line  7839)
* scm_c_make_rectangular:                Complex.           (line  7838)
* scm_c_make_socket_address:             Network Socket Address.
                                                            (line 31525)
* scm_c_make_string:                     String Constructors.
                                                            (line  9312)
* scm_c_make_struct:                     Structure Basics.  (line 13981)
* scm_c_make_structv:                    Structure Basics.  (line 13983)
* scm_c_make_vector:                     Vector Creation.   (line 12332)
* scm_c_module_define:                   Accessing Modules from C.
                                                            (line 24638)
* scm_c_module_lookup:                   Accessing Modules from C.
                                                            (line 24619)
* scm_c_nvalues:                         Multiple Values.   (line 18894)
* scm_c_port_for_each:                   Ports and File Descriptors.
                                                            (line 29415)
* scm_c_primitive_load:                  Loading.           (line 22911)
* scm_c_private_lookup:                  Accessing Modules from C.
                                                            (line 24576)
* scm_c_private_ref:                     Accessing Modules from C.
                                                            (line 24601)
* scm_c_private_variable:                Accessing Modules from C.
                                                            (line 24565)
* scm_c_public_lookup:                   Accessing Modules from C.
                                                            (line 24573)
* scm_c_public_ref:                      Accessing Modules from C.
                                                            (line 24598)
* scm_c_public_variable:                 Accessing Modules from C.
                                                            (line 24552)
* scm_c_read:                            Reading.           (line 19914)
* scm_c_real_part:                       Complex.           (line  7843)
* scm_c_resolve_module:                  Accessing Modules from C.
                                                            (line 24671)
* scm_c_round:                           Arithmetic.        (line  7922)
* scm_c_run_hook:                        Hook Reference.    (line 17712)
* scm_c_string_length:                   String Selection.  (line  9389)
* scm_c_string_ref:                      String Selection.  (line  9397)
* scm_c_string_set_x:                    String Modification.
                                                            (line  9516)
* scm_c_substring:                       String Selection.  (line  9436)
* scm_c_substring_copy:                  String Selection.  (line  9439)
* scm_c_substring_read_only:             String Selection.  (line  9441)
* scm_c_substring_shared:                String Selection.  (line  9437)
* scm_c_symbol_length:                   Symbol Primitives. (line 11238)
* scm_c_titlecase:                       Characters.        (line  8654)
* scm_c_truncate:                        Arithmetic.        (line  7921)
* scm_c_upcase:                          Characters.        (line  8652)
* scm_c_use_module:                      Accessing Modules from C.
                                                            (line 24677)
* scm_c_values:                          Multiple Values.   (line 18886)
* scm_c_value_ref:                       Multiple Values.   (line 18898)
* scm_c_vector_length:                   Vector Accessors.  (line 12356)
* scm_c_vector_ref:                      Vector Accessors.  (line 12370)
* scm_c_vector_set_x:                    Vector Accessors.  (line 12390)
* scm_c_with_continuation_barrier:       Continuation Barriers.
                                                            (line 19725)
* scm_c_with_dynamic_state:              Fluids and Dynamic States.
                                                            (line 26307)
* scm_c_with_fluid:                      Fluids and Dynamic States.
                                                            (line 26259)
* scm_c_with_fluids:                     Fluids and Dynamic States.
                                                            (line 26257)
* scm_c_with_throw_handler:              Throw Handlers.    (line 19185)
* scm_c_write:                           Writing.           (line 20029)
* scm_datum_to_random_state:             Random.            (line  8373)
* SCM_DEFINE:                            Snarfing Macros.   (line  6872)
* scm_define:                            Top Level.         (line 17927)
* scm_define <1>:                        Accessing Modules from C.
                                                            (line 24635)
* scm_defined_p:                         Binding Reflection.
                                                            (line 18133)
* scm_delete:                            List Modification. (line 12149)
* scm_delete1_x:                         List Modification. (line 12183)
* scm_delete_file:                       File System.       (line 29702)
* scm_delete_x:                          List Modification. (line 12163)
* scm_delq:                              List Modification. (line 12137)
* scm_delq1_x:                           List Modification. (line 12171)
* scm_delq_x:                            List Modification. (line 12161)
* scm_delv:                              List Modification. (line 12143)
* scm_delv1_x:                           List Modification. (line 12177)
* scm_delv_x:                            List Modification. (line 12162)
* scm_denominator:                       Reals and Rationals.
                                                            (line  7464)
* scm_difference:                        Arithmetic.        (line  7866)
* scm_directory_stream_p:                File System.       (line 29774)
* scm_dirname:                           File System.       (line 29865)
* scm_display_application:               Frames.            (line 27886)
* scm_display_backtrace:                 Stacks.            (line 27832)
* scm_display_backtrace_with_highlights: Stacks.            (line 27830)
* scm_display_error:                     Handling Errors.   (line 19583)
* scm_divide:                            Arithmetic.        (line  7877)
* scm_done_free:                         Memory Blocks.     (line 23610)
* scm_done_malloc:                       Memory Blocks.     (line 23610)
* scm_double_cell:                       Allocating Cells.  (line 47292)
* scm_doubly_weak_hash_table_p:          Weak hash tables.  (line 23701)
* scm_drain_input:                       Reading.           (line 19957)
* scm_dup2:                              Ports and File Descriptors.
                                                            (line 29399)
* scm_dup_to_fdes:                       Ports and File Descriptors.
                                                            (line 29352)
* scm_dynamic_call:                      Foreign Functions. (line 24877)
* scm_dynamic_func:                      Foreign Functions. (line 24863)
* scm_dynamic_link:                      Foreign Libraries. (line 24800)
* scm_dynamic_object_p:                  Foreign Libraries. (line 24822)
* scm_dynamic_pointer:                   Foreign Variables. (line 25194)
* scm_dynamic_state_p:                   Fluids and Dynamic States.
                                                            (line 26282)
* scm_dynamic_unlink:                    Foreign Libraries. (line 24826)
* scm_dynamic_wind:                      Dynamic Wind.      (line 19425)
* scm_dynwind_begin:                     Dynamic Wind.      (line 19482)
* scm_dynwind_block_asyncs:              System asyncs.     (line 25727)
* scm_dynwind_critical_section:          Critical Sections. (line 26154)
* scm_dynwind_current_dynamic_state:     Fluids and Dynamic States.
                                                            (line 26303)
* scm_dynwind_current_error_port:        Default Ports.     (line 20367)
* scm_dynwind_current_input_port:        Default Ports.     (line 20365)
* scm_dynwind_current_output_port:       Default Ports.     (line 20366)
* scm_dynwind_end:                       Dynamic Wind.      (line 19508)
* scm_dynwind_fluid:                     Fluids and Dynamic States.
                                                            (line 26267)
* scm_dynwind_free:                      Dynamic Wind.      (line 19545)
* scm_dynwind_free <1>:                  Memory Blocks.     (line 23567)
* scm_dynwind_lock_mutex:                Mutexes and Condition Variables.
                                                            (line 25958)
* scm_dynwind_rewind_handler:            Dynamic Wind.      (line 19533)
* scm_dynwind_rewind_handler_with_scm:   Dynamic Wind.      (line 19535)
* scm_dynwind_unblock_asyncs:            System asyncs.     (line 25732)
* scm_dynwind_unwind_handler:            Dynamic Wind.      (line 19521)
* scm_dynwind_unwind_handler_with_scm:   Dynamic Wind.      (line 19523)
* scm_effective_version:                 Build Config.      (line 26658)
* scm_end_of_char_set_p:                 Iterating Over Character Sets.
                                                            (line  8731)
* scm_environ:                           Runtime Environment.
                                                            (line 30271)
* scm_eof_object:                        R6RS End-of-File.  (line 21036)
* scm_eof_object_p:                      Reading.           (line 19886)
* scm_eof_object_p <1>:                  R6RS End-of-File.  (line 21030)
* SCM_EOF_VAL:                           Immediate objects. (line 47211)
* SCM_EOL:                               Immediate objects. (line 47207)
* scm_equal_p:                           Equality.          (line 17335)
* scm_eqv_p:                             Equality.          (line 17319)
* scm_eq_p:                              Equality.          (line 17276)
* scm_error:                             Handling Errors.   (line 19629)
* scm_error_scm:                         Error Reporting.   (line 19331)
* scm_euclidean_divide:                  Arithmetic.        (line  7929)
* scm_euclidean_quotient:                Arithmetic.        (line  7930)
* scm_euclidean_remainder:               Arithmetic.        (line  7931)
* scm_eval:                              Fly Evaluation.    (line 22622)
* scm_eval_string:                       Fly Evaluation.    (line 22668)
* scm_eval_string_in_module:             Fly Evaluation.    (line 22669)
* scm_even_p:                            Integer Operations.
                                                            (line  7675)
* scm_exact_integer_p:                   Integers.          (line  7212)
* scm_exact_integer_sqrt:                Integer Operations.
                                                            (line  7728)
* scm_exact_p:                           Exactness.         (line  7542)
* scm_exact_to_inexact:                  Exactness.         (line  7591)
* scm_execl:                             Processes.         (line 30535)
* scm_execle:                            Processes.         (line 30560)
* scm_execlp:                            Processes.         (line 30550)
* scm_f32vector:                         SRFI-4 API.        (line 35097)
* scm_f32vector_elements:                SRFI-4 API.        (line 35285)
* scm_f32vector_length:                  SRFI-4 API.        (line 35125)
* scm_f32vector_p:                       SRFI-4 API.        (line 35041)
* scm_f32vector_ref:                     SRFI-4 API.        (line 35151)
* scm_f32vector_set_x:                   SRFI-4 API.        (line 35178)
* scm_f32vector_to_list:                 SRFI-4 API.        (line 35205)
* scm_f32vector_writable_elements:       SRFI-4 API.        (line 35313)
* scm_f64vector:                         SRFI-4 API.        (line 35098)
* scm_f64vector_elements:                SRFI-4 API.        (line 35287)
* scm_f64vector_length:                  SRFI-4 API.        (line 35126)
* scm_f64vector_p:                       SRFI-4 API.        (line 35042)
* scm_f64vector_ref:                     SRFI-4 API.        (line 35152)
* scm_f64vector_set_x:                   SRFI-4 API.        (line 35179)
* scm_f64vector_to_list:                 SRFI-4 API.        (line 35206)
* scm_f64vector_writable_elements:       SRFI-4 API.        (line 35315)
* scm_fcntl:                             Ports and File Descriptors.
                                                            (line 29444)
* scm_fdes_to_ports:                     Ports and File Descriptors.
                                                            (line 29226)
* scm_fdopen:                            Ports and File Descriptors.
                                                            (line 29219)
* scm_fileno:                            Ports and File Descriptors.
                                                            (line 29210)
* scm_file_encoding:                     Character Encoding of Source Files.
                                                            (line 23148)
* scm_file_port_p:                       File Ports.        (line 20565)
* scm_finite_p:                          Reals and Rationals.
                                                            (line  7447)
* scm_flock:                             Ports and File Descriptors.
                                                            (line 29490)
* scm_floor:                             Arithmetic.        (line  7914)
* scm_floor_divide:                      Arithmetic.        (line  7955)
* scm_floor_quotient:                    Arithmetic.        (line  7956)
* scm_floor_remainder:                   Arithmetic.        (line  7957)
* scm_fluid_bound_p:                     Fluids and Dynamic States.
                                                            (line 26228)
* scm_fluid_p:                           Fluids and Dynamic States.
                                                            (line 26210)
* scm_fluid_ref:                         Fluids and Dynamic States.
                                                            (line 26214)
* scm_fluid_set_x:                       Fluids and Dynamic States.
                                                            (line 26220)
* scm_fluid_unset_x:                     Fluids and Dynamic States.
                                                            (line 26224)
* scm_flush_all_ports:                   Writing.           (line 20047)
* scm_force:                             Delayed Evaluation.
                                                            (line 23176)
* scm_force_output:                      Writing.           (line 20037)
* scm_fork:                              Processes.         (line 30570)
* scm_frame_arguments:                   Frames.            (line 27858)
* scm_frame_p:                           Frames.            (line 27844)
* scm_frame_previous:                    Frames.            (line 27848)
* scm_frame_procedure:                   Frames.            (line 27853)
* scm_from_bool:                         Booleans.          (line  7042)
* scm_from_char:                         Integers.          (line  7304)
* scm_from_double:                       Reals and Rationals.
                                                            (line  7477)
* scm_from_int:                          Integers.          (line  7309)
* scm_from_int16:                        Integers.          (line  7320)
* scm_from_int32:                        Integers.          (line  7322)
* scm_from_int64:                        Integers.          (line  7324)
* scm_from_int8:                         Integers.          (line  7318)
* scm_from_intmax:                       Integers.          (line  7326)
* scm_from_latin1_keyword:               Keyword Procedures.
                                                            (line 11664)
* scm_from_latin1_string:                Conversion to/from C.
                                                            (line 10396)
* scm_from_latin1_stringn:               Conversion to/from C.
                                                            (line 10404)
* scm_from_latin1_symbol:                Symbol Primitives. (line 11208)
* scm_from_locale_keyword:               Keyword Procedures.
                                                            (line 11651)
* scm_from_locale_keywordn:              Keyword Procedures.
                                                            (line 11652)
* scm_from_locale_string:                Conversion to/from C.
                                                            (line 10269)
* scm_from_locale_stringn:               Conversion to/from C.
                                                            (line 10270)
* scm_from_locale_symbol:                Symbol Primitives. (line 11214)
* scm_from_locale_symboln:               Symbol Primitives. (line 11215)
* scm_from_long:                         Integers.          (line  7311)
* scm_from_long_long:                    Integers.          (line  7313)
* scm_from_mpz:                          Integers.          (line  7339)
* scm_from_pointer:                      Foreign Variables. (line 25254)
* scm_from_ptrdiff_t:                    Integers.          (line  7317)
* scm_from_schar:                        Integers.          (line  7305)
* scm_from_short:                        Integers.          (line  7307)
* scm_from_signed_integer:               Integers.          (line  7265)
* scm_from_size_t:                       Integers.          (line  7315)
* scm_from_sockaddr:                     Network Socket Address.
                                                            (line 31534)
* scm_from_ssize_t:                      Integers.          (line  7316)
* scm_from_stringn:                      Conversion to/from C.
                                                            (line 10381)
* scm_from_uchar:                        Integers.          (line  7306)
* scm_from_uint:                         Integers.          (line  7310)
* scm_from_uint16:                       Integers.          (line  7321)
* scm_from_uint32:                       Integers.          (line  7323)
* scm_from_uint64:                       Integers.          (line  7325)
* scm_from_uint8:                        Integers.          (line  7319)
* scm_from_uintmax:                      Integers.          (line  7327)
* scm_from_ulong:                        Integers.          (line  7312)
* scm_from_ulong_long:                   Integers.          (line  7314)
* scm_from_unsigned_integer:             Integers.          (line  7266)
* scm_from_ushort:                       Integers.          (line  7308)
* scm_from_utf32_string:                 Conversion to/from C.
                                                            (line 10398)
* scm_from_utf32_stringn:                Conversion to/from C.
                                                            (line 10407)
* scm_from_utf8_keyword:                 Keyword Procedures.
                                                            (line 11665)
* scm_from_utf8_string:                  Conversion to/from C.
                                                            (line 10397)
* scm_from_utf8_stringn:                 Conversion to/from C.
                                                            (line 10406)
* scm_from_utf8_symbol:                  Symbol Primitives. (line 11209)
* scm_fsync:                             Ports and File Descriptors.
                                                            (line 29260)
* scm_ftell:                             Random Access.     (line 20100)
* scm_gc:                                Garbage Collection Functions.
                                                            (line 23390)
* scm_gcd:                               Integer Operations.
                                                            (line  7705)
* scm_gc_calloc:                         Memory Blocks.     (line 23529)
* scm_gc_free:                           Memory Blocks.     (line 23543)
* scm_gc_live_object_stats:              Garbage Collection Functions.
                                                            (line 23440)
* scm_gc_malloc:                         Memory Blocks.     (line 23524)
* scm_gc_malloc_pointerless:             Memory Blocks.     (line 23525)
* scm_gc_mark:                           Garbage Collection Functions.
                                                            (line 23443)
* scm_gc_protect_object:                 Garbage Collection Functions.
                                                            (line 23395)
* scm_gc_realloc:                        Memory Blocks.     (line 23527)
* scm_gc_register_allocation:            Memory Blocks.     (line 23554)
* scm_gc_stats:                          Garbage Collection Functions.
                                                            (line 23435)
* scm_gc_unprotect_object:               Garbage Collection Functions.
                                                            (line 23408)
* scm_gensym:                            Symbol Primitives. (line 11246)
* scm_geq_p:                             Comparison.        (line  7763)
* scm_getaddrinfo:                       Network Databases. (line 31084)
* scm_getaffinity:                       Processes.         (line 30626)
* scm_getcwd:                            Processes.         (line 30301)
* scm_getegid:                           Processes.         (line 30351)
* scm_getenv:                            Runtime Environment.
                                                            (line 30251)
* scm_geteuid:                           Processes.         (line 30344)
* scm_getgid:                            Processes.         (line 30340)
* scm_getgrgid:                          User Information.  (line 30005)
* scm_getgroups:                         Processes.         (line 30326)
* scm_gethost:                           Network Databases. (line 31253)
* scm_gethostname:                       System Identification.
                                                            (line 31924)
* scm_getitimer:                         Signals.           (line 30799)
* scm_getlogin:                          User Information.  (line 30014)
* scm_getnet:                            Network Databases. (line 31317)
* scm_getpass:                           Encryption.        (line 31982)
* scm_getpeername:                       Network Sockets and Communication.
                                                            (line 31758)
* scm_getpgrp:                           Processes.         (line 30392)
* scm_getpid:                            Processes.         (line 30322)
* scm_getppid:                           Processes.         (line 30331)
* scm_getpriority:                       Processes.         (line 30614)
* scm_getproto:                          Network Databases. (line 31364)
* scm_getpwuid:                          User Information.  (line 29962)
* scm_getserv:                           Network Databases. (line 31414)
* scm_getsid:                            Processes.         (line 30411)
* scm_getsockname:                       Network Sockets and Communication.
                                                            (line 31748)
* scm_getsockopt:                        Network Sockets and Communication.
                                                            (line 31604)
* scm_gettext:                           Gettext Support.   (line 27604)
* scm_gettimeofday:                      Time.              (line 30028)
* scm_getuid:                            Processes.         (line 30336)
* scm_get_bytevector_all:                R6RS Binary Input. (line 21275)
* scm_get_bytevector_n:                  R6RS Binary Input. (line 21256)
* scm_get_bytevector_n_x:                R6RS Binary Input. (line 21262)
* scm_get_bytevector_some:               R6RS Binary Input. (line 21268)
* scm_get_internal_real_time:            Time.              (line 30180)
* scm_get_internal_run_time:             Time.              (line 30184)
* scm_get_output_string:                 String Ports.      (line 20647)
* scm_get_print_state:                   Writing.           (line 20000)
* scm_get_u8:                            R6RS Binary Input. (line 21246)
* SCM_GLOBAL_KEYWORD:                    Snarfing Macros.   (line  6911)
* SCM_GLOBAL_SYMBOL:                     Snarfing Macros.   (line  6893)
* SCM_GLOBAL_VARIABLE:                   Snarfing Macros.   (line  6929)
* SCM_GLOBAL_VARIABLE_INIT:              Snarfing Macros.   (line  6935)
* scm_gmtime:                            Time.              (line 30089)
* scm_gr_p:                              Comparison.        (line  7754)
* scm_hash:                              Hash Table Reference.
                                                            (line 15036)
* scm_hashq:                             Hash Table Reference.
                                                            (line 15037)
* scm_hashq_create_handle_x:             Hash Table Reference.
                                                            (line 15073)
* scm_hashq_get_handle:                  Hash Table Reference.
                                                            (line 15062)
* scm_hashq_ref:                         Hash Table Reference.
                                                            (line 15003)
* scm_hashq_remove_x:                    Hash Table Reference.
                                                            (line 15027)
* scm_hashq_set_x:                       Hash Table Reference.
                                                            (line 15015)
* scm_hashv:                             Hash Table Reference.
                                                            (line 15038)
* scm_hashv_create_handle_x:             Hash Table Reference.
                                                            (line 15074)
* scm_hashv_get_handle:                  Hash Table Reference.
                                                            (line 15063)
* scm_hashv_ref:                         Hash Table Reference.
                                                            (line 15004)
* scm_hashv_remove_x:                    Hash Table Reference.
                                                            (line 15028)
* scm_hashv_set_x:                       Hash Table Reference.
                                                            (line 15016)
* scm_hashx_create_handle_x:             Hash Table Reference.
                                                            (line 15075)
* scm_hashx_get_handle:                  Hash Table Reference.
                                                            (line 15064)
* scm_hashx_ref:                         Hash Table Reference.
                                                            (line 15005)
* scm_hashx_remove_x:                    Hash Table Reference.
                                                            (line 15029)
* scm_hashx_set_x:                       Hash Table Reference.
                                                            (line 15017)
* scm_hash_clear_x:                      Hash Table Reference.
                                                            (line 14995)
* scm_hash_count:                        Hash Table Reference.
                                                            (line 15129)
* scm_hash_create_handle_x:              Hash Table Reference.
                                                            (line 15072)
* scm_hash_fold:                         Hash Table Reference.
                                                            (line 15110)
* scm_hash_for_each:                     Hash Table Reference.
                                                            (line 15084)
* scm_hash_for_each_handle:              Hash Table Reference.
                                                            (line 15101)
* scm_hash_get_handle:                   Hash Table Reference.
                                                            (line 15061)
* scm_hash_map_to_list:                  Hash Table Reference.
                                                            (line 15083)
* scm_hash_ref:                          Hash Table Reference.
                                                            (line 15002)
* scm_hash_remove_x:                     Hash Table Reference.
                                                            (line 15026)
* scm_hash_set_x:                        Hash Table Reference.
                                                            (line 15014)
* scm_hash_table_p:                      Hash Table Reference.
                                                            (line 14991)
* SCM_HOOKP:                             Hook Reference.    (line 17719)
* scm_hook_empty_p:                      Hook Reference.    (line 17679)
* scm_hook_p:                            Hook Reference.    (line 17675)
* scm_hook_to_list:                      Hook Reference.    (line 17699)
* scm_imag_part:                         Complex.           (line  7826)
* SCM_IMP:                               Immediate objects. (line 47189)
* scm_inet_aton:                         Network Address Conversion.
                                                            (line 31008)
* scm_inet_makeaddr:                     Network Address Conversion.
                                                            (line 31040)
* scm_inet_netof:                        Network Address Conversion.
                                                            (line 31026)
* scm_inet_ntoa:                         Network Address Conversion.
                                                            (line 31017)
* scm_inet_ntop:                         Network Address Conversion.
                                                            (line 31053)
* scm_inet_pton:                         Network Address Conversion.
                                                            (line 31062)
* scm_inexact_p:                         Exactness.         (line  7562)
* scm_inexact_to_exact:                  Exactness.         (line  7570)
* scm_inf:                               Reals and Rationals.
                                                            (line  7456)
* scm_inf_p:                             Reals and Rationals.
                                                            (line  7438)
* scm_init_guile:                        Initialization.    (line  6799)
* scm_input_port_p:                      Ports.             (line 19799)
* scm_integer_expt:                      Bitwise Operations.
                                                            (line  8285)
* scm_integer_length:                    Bitwise Operations.
                                                            (line  8270)
* scm_integer_p:                         Integers.          (line  7192)
* scm_integer_to_char:                   Characters.        (line  8628)
* scm_interaction_environment:           Fly Evaluation.    (line 22631)
* scm_internal_catch:                    Catch.             (line 19109)
* scm_isatty_p:                          Terminals and Ptys.
                                                            (line 30849)
* scm_is_array:                          Array Procedures.  (line 12807)
* scm_is_bitvector:                      Bit Vectors.       (line 12537)
* scm_is_bool:                           Booleans.          (line  7039)
* scm_is_bytevector:                     Bytevector Manipulation.
                                                            (line 10568)
* scm_is_complex:                        Complex Numbers.   (line  7522)
* scm_is_dynamic_state:                  Fluids and Dynamic States.
                                                            (line 26286)
* scm_is_eq:                             Equality.          (line 17309)
* scm_is_exact:                          Exactness.         (line  7554)
* scm_is_exact_integer:                  Integers.          (line  7221)
* scm_is_false:                          Booleans.          (line  7036)
* scm_is_inexact:                        Exactness.         (line  7565)
* scm_is_integer:                        Integers.          (line  7208)
* scm_is_keyword:                        Keyword Procedures.
                                                            (line 11648)
* scm_is_null:                           List Predicates.   (line 11989)
* scm_is_number:                         Numerical Tower.   (line  7124)
* scm_is_pair:                           Pairs.             (line 11812)
* scm_is_rational:                       Reals and Rationals.
                                                            (line  7468)
* scm_is_real:                           Reals and Rationals.
                                                            (line  7467)
* scm_is_signed_integer:                 Integers.          (line  7244)
* scm_is_simple_vector:                  Vector Accessing from C.
                                                            (line 12440)
* scm_is_string:                         String Predicates. (line  9234)
* scm_is_symbol:                         Symbol Primitives. (line 11099)
* scm_is_true:                           Booleans.          (line  7033)
* scm_is_typed_array:                    Array Procedures.  (line 12810)
* scm_is_unsigned_integer:               Integers.          (line  7246)
* scm_is_vector:                         Vector Creation.   (line 12342)
* scm_join_thread:                       Threads.           (line 25812)
* scm_join_thread_timed:                 Threads.           (line 25813)
* SCM_KEYWORD:                           Snarfing Macros.   (line  6910)
* scm_keyword_p:                         Keyword Procedures.
                                                            (line 11637)
* scm_keyword_to_symbol:                 Keyword Procedures.
                                                            (line 11641)
* scm_kill:                              Signals.           (line 30675)
* scm_last_pair:                         List Selection.    (line 12049)
* scm_lcm:                               Integer Operations.
                                                            (line  7713)
* scm_length:                            List Selection.    (line 12045)
* scm_leq_p:                             Comparison.        (line  7758)
* scm_less_p:                            Comparison.        (line  7750)
* scm_link:                              File System.       (line 29742)
* scm_listen:                            Network Sockets and Communication.
                                                            (line 31722)
* scm_list_1:                            List Constructors. (line 12001)
* scm_list_2:                            List Constructors. (line 12002)
* scm_list_3:                            List Constructors. (line 12003)
* scm_list_4:                            List Constructors. (line 12004)
* scm_list_5:                            List Constructors. (line 12005)
* scm_list_cdr_set_x:                    List Modification. (line 12133)
* scm_list_copy:                         List Constructors. (line 12022)
* scm_list_head:                         List Selection.    (line 12068)
* scm_list_n:                            List Constructors. (line 12006)
* scm_list_p:                            List Predicates.   (line 11977)
* scm_list_ref:                          List Selection.    (line 12054)
* scm_list_set_x:                        List Modification. (line 12129)
* scm_list_tail:                         List Selection.    (line 12059)
* scm_list_to_bitvector:                 Bit Vectors.       (line 12582)
* scm_list_to_c32vector:                 SRFI-4 API.        (line 35233)
* scm_list_to_c64vector:                 SRFI-4 API.        (line 35234)
* scm_list_to_char_set:                  Creating Character Sets.
                                                            (line  8787)
* scm_list_to_char_set_x:                Creating Character Sets.
                                                            (line  8793)
* scm_list_to_f32vector:                 SRFI-4 API.        (line 35231)
* scm_list_to_f64vector:                 SRFI-4 API.        (line 35232)
* scm_list_to_s16vector:                 SRFI-4 API.        (line 35226)
* scm_list_to_s32vector:                 SRFI-4 API.        (line 35228)
* scm_list_to_s64vector:                 SRFI-4 API.        (line 35230)
* scm_list_to_s8vector:                  SRFI-4 API.        (line 35224)
* scm_list_to_typed_array:               Array Procedures.  (line 12848)
* scm_list_to_u16vector:                 SRFI-4 API.        (line 35225)
* scm_list_to_u32vector:                 SRFI-4 API.        (line 35227)
* scm_list_to_u64vector:                 SRFI-4 API.        (line 35229)
* scm_list_to_u8vector:                  SRFI-4 API.        (line 35223)
* scm_lnaof:                             Network Address Conversion.
                                                            (line 31033)
* scm_load_extension:                    Foreign Functions. (line 24908)
* scm_load_objcode:                      Bytecode and Objcode.
                                                            (line 49262)
* scm_locale_p:                          i18n Introduction. (line 27267)
* scm_locale_string_to_inexact:          Number Input and Output.
                                                            (line 27390)
* scm_locale_string_to_integer:          Number Input and Output.
                                                            (line 27377)
* scm_localtime:                         Time.              (line 30081)
* scm_local_eval:                        Local Evaluation.  (line 23202)
* scm_lock_mutex:                        Mutexes and Condition Variables.
                                                            (line 25928)
* scm_lock_mutex_timed:                  Mutexes and Condition Variables.
                                                            (line 25929)
* scm_logand:                            Bitwise Operations.
                                                            (line  8168)
* scm_logbit_p:                          Bitwise Operations.
                                                            (line  8213)
* scm_logcount:                          Bitwise Operations.
                                                            (line  8256)
* scm_logior:                            Bitwise Operations.
                                                            (line  8176)
* scm_lognot:                            Bitwise Operations.
                                                            (line  8194)
* scm_logtest:                           Bitwise Operations.
                                                            (line  8204)
* scm_lookahead_u8:                      R6RS Binary Input. (line 21251)
* scm_lookup:                            Accessing Modules from C.
                                                            (line 24616)
* scm_loxor:                             Bitwise Operations.
                                                            (line  8184)
* scm_lstat:                             File System.       (line 29653)
* scm_macro_binding:                     Internal Macros.   (line 17229)
* scm_macro_name:                        Internal Macros.   (line 17225)
* scm_macro_p:                           Internal Macros.   (line 17208)
* scm_macro_transformer:                 Internal Macros.   (line 17233)
* scm_macro_type:                        Internal Macros.   (line 17220)
* scm_magnitude:                         Complex.           (line  7830)
* scm_major_version:                     Build Config.      (line 26659)
* scm_make_arbiter:                      Arbiters.          (line 25630)
* scm_make_array:                        Array Procedures.  (line 12814)
* scm_make_bitvector:                    Bit Vectors.       (line 12541)
* scm_make_bytevector:                   Bytevector Manipulation.
                                                            (line 10559)
* scm_make_c32vector:                    SRFI-4 API.        (line 35070)
* scm_make_c64vector:                    SRFI-4 API.        (line 35071)
* scm_make_condition_variable:           Mutexes and Condition Variables.
                                                            (line 26007)
* scm_make_custom_binary_input_port:     R6RS Binary Input. (line 21191)
* scm_make_custom_binary_output_port:    R6RS Binary Output.
                                                            (line 21479)
* scm_make_doubly_weak_hash_table:       Weak hash tables.  (line 23689)
* scm_make_dynamic_state:                Fluids and Dynamic States.
                                                            (line 26277)
* scm_make_f32vector:                    SRFI-4 API.        (line 35068)
* scm_make_f64vector:                    SRFI-4 API.        (line 35069)
* scm_make_fluid:                        Fluids and Dynamic States.
                                                            (line 26193)
* scm_make_fluid_with_default:           Fluids and Dynamic States.
                                                            (line 26194)
* scm_make_guardian:                     Guardians.         (line 23748)
* scm_make_hook:                         Hook Reference.    (line 17669)
* scm_make_locale:                       i18n Introduction. (line 27237)
* scm_make_mutex:                        Mutexes and Condition Variables.
                                                            (line 25900)
* scm_make_mutex_with_flags:             Mutexes and Condition Variables.
                                                            (line 25901)
* scm_make_polar:                        Complex.           (line  7818)
* scm_make_port_type:                    Port Implementation.
                                                            (line 21649)
* scm_make_procedure_with_setter:        Procedures with Setters.
                                                            (line 16029)
* scm_make_program:                      Bytecode and Objcode.
                                                            (line 49282)
* scm_make_rectangular:                  Complex.           (line  7813)
* scm_make_recursive_mutex:              Mutexes and Condition Variables.
                                                            (line 25922)
* scm_make_regexp:                       Regexp Functions.  (line 21903)
* scm_make_s16vector:                    SRFI-4 API.        (line 35063)
* scm_make_s32vector:                    SRFI-4 API.        (line 35065)
* scm_make_s64vector:                    SRFI-4 API.        (line 35067)
* scm_make_s8vector:                     SRFI-4 API.        (line 35061)
* scm_make_shared_array:                 Shared Arrays.     (line 13010)
* scm_make_smob_type:                    Smobs.             (line 15141)
* scm_make_socket_address:               Network Socket Address.
                                                            (line 31467)
* scm_make_soft_port:                    Soft Ports.        (line 20667)
* scm_make_stack:                        Stack Capture.     (line 27772)
* scm_make_string:                       String Constructors.
                                                            (line  9307)
* scm_make_struct:                       Structure Basics.  (line 13979)
* scm_make_struct_layout:                Meta-Vtables.      (line 14155)
* scm_make_symbol:                       Symbol Uninterned. (line 11424)
* scm_make_typed_array:                  Array Procedures.  (line 12818)
* scm_make_u16vector:                    SRFI-4 API.        (line 35062)
* scm_make_u32vector:                    SRFI-4 API.        (line 35064)
* scm_make_u64vector:                    SRFI-4 API.        (line 35066)
* scm_make_u8vector:                     SRFI-4 API.        (line 35060)
* scm_make_unbound_fluid:                Fluids and Dynamic States.
                                                            (line 26205)
* scm_make_undefined_variable:           Variables.         (line 24411)
* scm_make_variable:                     Variables.         (line 24415)
* scm_make_vector:                       Vector Creation.   (line 12327)
* scm_make_weak_key_hash_table:          Weak hash tables.  (line 23687)
* scm_make_weak_value_hash_table:        Weak hash tables.  (line 23688)
* scm_make_weak_vector:                  Weak vectors.      (line 23710)
* scm_malloc:                            Memory Blocks.     (line 23493)
* scm_map:                               List Mapping.      (line 12243)
* scm_markcdr:                           Smobs.             (line 15297)
* scm_max:                               Arithmetic.        (line  7897)
* scm_member:                            List Searching.    (line 12222)
* scm_memory_error:                      Handling Errors.   (line 19650)
* scm_memq:                              List Searching.    (line 12208)
* scm_memv:                              List Searching.    (line 12215)
* scm_merge:                             Sorting.           (line 17450)
* scm_merge_x:                           Sorting.           (line 17458)
* scm_micro_version:                     Build Config.      (line 26661)
* scm_min:                               Arithmetic.        (line  7901)
* scm_minor_version:                     Build Config.      (line 26660)
* scm_misc_error:                        Handling Errors.   (line 19651)
* scm_mkdir:                             File System.       (line 29753)
* scm_mknod:                             File System.       (line 29809)
* scm_mkstemp:                           File System.       (line 29839)
* scm_mktime:                            Time.              (line 30095)
* scm_module_define:                     Accessing Modules from C.
                                                            (line 24640)
* scm_module_ensure_local_variable:      Accessing Modules from C.
                                                            (line 24649)
* scm_module_lookup:                     Accessing Modules from C.
                                                            (line 24620)
* scm_module_reverse_lookup:             Accessing Modules from C.
                                                            (line 24655)
* scm_module_variable:                   Accessing Modules from C.
                                                            (line 24624)
* scm_modulo:                            Integer Operations.
                                                            (line  7693)
* scm_modulo_expt:                       Integer Operations.
                                                            (line  7721)
* scm_must_calloc:                       Memory Blocks.     (line 23589)
* scm_must_free:                         Memory Blocks.     (line 23589)
* scm_must_malloc:                       Memory Blocks.     (line 23589)
* scm_must_realloc:                      Memory Blocks.     (line 23589)
* scm_mutex_level:                       Mutexes and Condition Variables.
                                                            (line 25996)
* scm_mutex_locked_p:                    Mutexes and Condition Variables.
                                                            (line 26002)
* scm_mutex_owner:                       Mutexes and Condition Variables.
                                                            (line 25990)
* scm_mutex_p:                           Mutexes and Condition Variables.
                                                            (line 25918)
* scm_nan:                               Reals and Rationals.
                                                            (line  7452)
* scm_nan_p:                             Reals and Rationals.
                                                            (line  7443)
* scm_native_endianness:                 Bytevector Endianness.
                                                            (line 10533)
* scm_nconc2last:                        Fly Evaluation.    (line 22723)
* scm_negative_p:                        Comparison.        (line  7776)
* scm_newline:                           Writing.           (line 20005)
* scm_new_double_smob:                   Smobs.             (line 15241)
* scm_new_smob:                          Smobs.             (line 15240)
* scm_ngettext:                          Gettext Support.   (line 27629)
* scm_nice:                              Processes.         (line 30594)
* scm_not:                               Booleans.          (line  7020)
* scm_null_p:                            List Predicates.   (line 11986)
* scm_number_p:                          Numerical Tower.   (line  7109)
* scm_number_to_string:                  Conversion.        (line  7788)
* scm_numerator:                         Reals and Rationals.
                                                            (line  7460)
* scm_num_eq_p:                          Comparison.        (line  7746)
* scm_num_overflow:                      Handling Errors.   (line 19643)
* scm_objcode_p:                         Bytecode and Objcode.
                                                            (line 49253)
* scm_objcode_to_bytecode:               Bytecode and Objcode.
                                                            (line 49275)
* scm_object_properties:                 Object Properties. (line 17422)
* scm_object_property:                   Object Properties. (line 17430)
* scm_object_to_string:                  General Conversion.
                                                            (line 17561)
* scm_odd_p:                             Integer Operations.
                                                            (line  7671)
* scm_oneminus:                          Arithmetic.        (line  7886)
* scm_oneplus:                           Arithmetic.        (line  7882)
* scm_open:                              Ports and File Descriptors.
                                                            (line 29267)
* scm_opendir:                           File System.       (line 29765)
* scm_open_bytevector_input_port:        R6RS Binary Input. (line 21183)
* scm_open_bytevector_output_port:       R6RS Binary Output.
                                                            (line 21461)
* scm_open_fdes:                         Ports and File Descriptors.
                                                            (line 29291)
* scm_open_file:                         File Ports.        (line 20396)
* scm_open_file_with_encoding:           File Ports.        (line 20394)
* scm_open_input_string:                 String Ports.      (line 20633)
* scm_open_output_string:                String Ports.      (line 20640)
* scm_output_port_p:                     Ports.             (line 19804)
* scm_out_of_range:                      Handling Errors.   (line 19644)
* SCM_PACK:                              The SCM Type.      (line  6746)
* scm_pair_p:                            Pairs.             (line 11809)
* scm_parse_path:                        Load Paths.        (line 23059)
* scm_parse_path_with_ellipsis:          Load Paths.        (line 23065)
* scm_pause:                             Signals.           (line 30774)
* scm_peek_char:                         Reading.           (line 19923)
* scm_permanent_object:                  Garbage Collection Functions.
                                                            (line 23414)
* scm_pipe:                              Ports and File Descriptors.
                                                            (line 29323)
* scm_pointer_address:                   Foreign Variables. (line 25218)
* scm_pointer_to_bytevector:             Void Pointers and Byte Access.
                                                            (line 25276)
* scm_pointer_to_procedure:              Dynamic FFI.       (line 25459)
* scm_port_closed_p:                     Closing.           (line 20074)
* scm_port_column:                       Reading.           (line 19973)
* scm_port_conversion_strategy:          Ports.             (line 19851)
* scm_port_encoding:                     Ports.             (line 19830)
* scm_port_filename:                     File Ports.        (line 20550)
* scm_port_for_each:                     Ports and File Descriptors.
                                                            (line 29414)
* scm_port_line:                         Reading.           (line 19974)
* scm_port_mode:                         File Ports.        (line 20543)
* scm_port_p:                            Ports.             (line 19809)
* scm_port_revealed:                     Ports and File Descriptors.
                                                            (line 29201)
* scm_port_with_print_state:             Writing.           (line 20010)
* scm_positive_p:                        Comparison.        (line  7772)
* scm_primitive_eval:                    Fly Evaluation.    (line 22734)
* scm_primitive_exit:                    Processes.         (line 30514)
* scm_primitive_load:                    Loading.           (line 22903)
* scm_primitive_load_path:               Load Paths.        (line 22992)
* scm_primitive_move_to_fdes:            Ports and File Descriptors.
                                                            (line 29241)
* scm_primitive__exit:                   Processes.         (line 30515)
* scm_private_lookup:                    Accessing Modules from C.
                                                            (line 24575)
* scm_private_ref:                       Accessing Modules from C.
                                                            (line 24600)
* scm_private_variable:                  Accessing Modules from C.
                                                            (line 24564)
* scm_procedure:                         Procedures with Setters.
                                                            (line 16039)
* scm_procedure_documentation:           Procedure Properties.
                                                            (line 15982)
* scm_procedure_name:                    Procedure Properties.
                                                            (line 15954)
* scm_procedure_p:                       Procedure Properties.
                                                            (line 15941)
* scm_procedure_properties:              Procedure Properties.
                                                            (line 15963)
* scm_procedure_property:                Procedure Properties.
                                                            (line 15967)
* scm_procedure_source:                  Procedure Properties.
                                                            (line 15958)
* scm_procedure_to_pointer:              Dynamic FFI.       (line 25555)
* scm_procedure_with_setter_p:           Procedures with Setters.
                                                            (line 16034)
* scm_product:                           Arithmetic.        (line  7872)
* scm_program_arguments:                 Runtime Environment.
                                                            (line 30195)
* scm_program_arities:                   Compiled Procedures.
                                                            (line 15511)
* scm_program_free_variables:            Compiled Procedures.
                                                            (line 15457)
* scm_program_meta:                      Compiled Procedures.
                                                            (line 15470)
* scm_program_module:                    Compiled Procedures.
                                                            (line 15451)
* scm_program_objcode:                   Compiled Procedures.
                                                            (line 15441)
* scm_program_objects:                   Compiled Procedures.
                                                            (line 15446)
* scm_program_p:                         Compiled Procedures.
                                                            (line 15437)
* scm_promise_p:                         Delayed Evaluation.
                                                            (line 23172)
* SCM_PTAB_ENTRY:                        C Port Interface.  (line 21555)
* scm_pthread_cond_timedwait:            Blocking.          (line 26108)
* scm_pthread_cond_wait:                 Blocking.          (line 26106)
* scm_pthread_mutex_lock:                Blocking.          (line 26102)
* SCM_PTOBNUM:                           C Port Interface.  (line 21555)
* scm_public_lookup:                     Accessing Modules from C.
                                                            (line 24572)
* scm_public_ref:                        Accessing Modules from C.
                                                            (line 24597)
* scm_public_variable:                   Accessing Modules from C.
                                                            (line 24551)
* scm_putenv:                            Runtime Environment.
                                                            (line 30281)
* scm_put_bytevector:                    R6RS Binary Output.
                                                            (line 21501)
* scm_put_u8:                            R6RS Binary Output.
                                                            (line 21496)
* scm_quotient:                          Integer Operations.
                                                            (line  7680)
* scm_raise:                             Signals.           (line 30704)
* scm_random:                            Random.            (line  8324)
* scm_random_exp:                        Random.            (line  8332)
* scm_random_hollow_sphere_x:            Random.            (line  8338)
* scm_random_normal:                     Random.            (line  8345)
* scm_random_normal_vector_x:            Random.            (line  8352)
* scm_random_solid_sphere_x:             Random.            (line  8358)
* scm_random_state_from_platform:        Random.            (line  8383)
* scm_random_state_to_datum:             Random.            (line  8378)
* scm_random_uniform:                    Random.            (line  8365)
* scm_rationalize:                       Reals and Rationals.
                                                            (line  7426)
* scm_rational_p:                        Reals and Rationals.
                                                            (line  7419)
* scm_read:                              Scheme Read.       (line 22491)
* scm_readdir:                           File System.       (line 29779)
* scm_readlink:                          File System.       (line 29659)
* scm_read_char:                         Reading.           (line 19905)
* scm_read_delimited_x:                  Line/Delimited.    (line 20220)
* scm_read_hash_extend:                  Reader Extensions. (line 22480)
* scm_read_line:                         Line/Delimited.    (line 20237)
* scm_read_string_x_partial:             Block Reading and Writing.
                                                            (line 20257)
* scm_realloc:                           Memory Blocks.     (line 23511)
* scm_real_p:                            Reals and Rationals.
                                                            (line  7412)
* scm_real_part:                         Complex.           (line  7822)
* scm_recv:                              Network Sockets and Communication.
                                                            (line 31766)
* scm_recvfrom:                          Network Sockets and Communication.
                                                            (line 31795)
* scm_redirect_port:                     Ports and File Descriptors.
                                                            (line 29384)
* scm_regexp_exec:                       Regexp Functions.  (line 21942)
* scm_regexp_p:                          Regexp Functions.  (line 21981)
* scm_release_arbiter:                   Arbiters.          (line 25641)
* scm_remainder:                         Integer Operations.
                                                            (line  7681)
* scm_remember_upto_here_1:              Garbage Collection Functions.
                                                            (line 23423)
* scm_remember_upto_here_2:              Garbage Collection Functions.
                                                            (line 23424)
* scm_remove_hook_x:                     Hook Reference.    (line 17689)
* scm_rename:                            File System.       (line 29737)
* scm_reset_hook_x:                      Hook Reference.    (line 17694)
* scm_resolve_module:                    Module System Reflection.
                                                            (line 24477)
* scm_restore_signals:                   Signals.           (line 30758)
* scm_restricted_vector_sort_x:          Sorting.           (line 17521)
* scm_reverse:                           Append/Reverse.    (line 12110)
* scm_reverse_list_to_string:            String Constructors.
                                                            (line  9300)
* scm_reverse_x:                         Append/Reverse.    (line 12111)
* scm_rewinddir:                         File System.       (line 29785)
* scm_rmdir:                             File System.       (line 29760)
* scm_round_ash:                         Bitwise Operations.
                                                            (line  8239)
* scm_round_divide:                      Arithmetic.        (line  8061)
* scm_round_number:                      Arithmetic.        (line  7909)
* scm_round_quotient:                    Arithmetic.        (line  8062)
* scm_round_remainder:                   Arithmetic.        (line  8063)
* scm_run_asyncs:                        User asyncs.       (line 25757)
* scm_run_hook:                          Hook Reference.    (line 17703)
* scm_s16vector:                         SRFI-4 API.        (line 35092)
* scm_s16vector_elements:                SRFI-4 API.        (line 35275)
* scm_s16vector_length:                  SRFI-4 API.        (line 35120)
* scm_s16vector_p:                       SRFI-4 API.        (line 35036)
* scm_s16vector_ref:                     SRFI-4 API.        (line 35146)
* scm_s16vector_set_x:                   SRFI-4 API.        (line 35173)
* scm_s16vector_to_list:                 SRFI-4 API.        (line 35200)
* scm_s16vector_writable_elements:       SRFI-4 API.        (line 35303)
* scm_s32vector:                         SRFI-4 API.        (line 35094)
* scm_s32vector_elements:                SRFI-4 API.        (line 35279)
* scm_s32vector_length:                  SRFI-4 API.        (line 35122)
* scm_s32vector_p:                       SRFI-4 API.        (line 35038)
* scm_s32vector_ref:                     SRFI-4 API.        (line 35148)
* scm_s32vector_set_x:                   SRFI-4 API.        (line 35175)
* scm_s32vector_to_list:                 SRFI-4 API.        (line 35202)
* scm_s32vector_writable_elements:       SRFI-4 API.        (line 35307)
* scm_s64vector:                         SRFI-4 API.        (line 35096)
* scm_s64vector_elements:                SRFI-4 API.        (line 35283)
* scm_s64vector_length:                  SRFI-4 API.        (line 35124)
* scm_s64vector_p:                       SRFI-4 API.        (line 35040)
* scm_s64vector_ref:                     SRFI-4 API.        (line 35150)
* scm_s64vector_set_x:                   SRFI-4 API.        (line 35177)
* scm_s64vector_to_list:                 SRFI-4 API.        (line 35204)
* scm_s64vector_writable_elements:       SRFI-4 API.        (line 35311)
* scm_s8vector:                          SRFI-4 API.        (line 35090)
* scm_s8vector_elements:                 SRFI-4 API.        (line 35271)
* scm_s8vector_length:                   SRFI-4 API.        (line 35118)
* scm_s8vector_p:                        SRFI-4 API.        (line 35034)
* scm_s8vector_ref:                      SRFI-4 API.        (line 35144)
* scm_s8vector_set_x:                    SRFI-4 API.        (line 35171)
* scm_s8vector_to_list:                  SRFI-4 API.        (line 35198)
* scm_s8vector_writable_elements:        SRFI-4 API.        (line 35299)
* scm_search_path:                       Load Paths.        (line 23073)
* scm_seed_to_random_state:              Random.            (line  8369)
* scm_seek:                              Random Access.     (line 20081)
* scm_select:                            Ports and File Descriptors.
                                                            (line 29514)
* scm_send:                              Network Sockets and Communication.
                                                            (line 31783)
* scm_sendfile:                          File System.       (line 29711)
* scm_sendto:                            Network Sockets and Communication.
                                                            (line 31827)
* scm_setaffinity:                       Processes.         (line 30637)
* scm_setegid:                           Processes.         (line 30385)
* scm_seteuid:                           Processes.         (line 30378)
* scm_setgid:                            Processes.         (line 30372)
* scm_setgrent:                          User Information.  (line 29999)
* scm_setgroups:                         Processes.         (line 30358)
* scm_sethost:                           Network Databases. (line 31292)
* scm_sethostname:                       System Identification.
                                                            (line 31928)
* scm_setitimer:                         Signals.           (line 30800)
* scm_setlocale:                         Locales.           (line 31936)
* scm_setnet:                            Network Databases. (line 31342)
* scm_setpgid:                           Processes.         (line 30397)
* scm_setpriority:                       Processes.         (line 30600)
* scm_setproto:                          Network Databases. (line 31389)
* scm_setpwent:                          User Information.  (line 29956)
* scm_setserv:                           Network Databases. (line 31450)
* scm_setsid:                            Processes.         (line 30404)
* scm_setsockopt:                        Network Sockets and Communication.
                                                            (line 31605)
* scm_setuid:                            Processes.         (line 30366)
* scm_setvbuf:                           Ports and File Descriptors.
                                                            (line 29429)
* scm_set_car_x:                         Pairs.             (line 11909)
* scm_set_cdr_x:                         Pairs.             (line 11914)
* SCM_SET_CELL_OBJECT:                   Accessing Cell Entries.
                                                            (line 47359)
* SCM_SET_CELL_TYPE:                     Heap Cell Type Information.
                                                            (line 47310)
* SCM_SET_CELL_WORD:                     Accessing Cell Entries.
                                                            (line 47345)
* scm_set_current_dynamic_state:         Fluids and Dynamic States.
                                                            (line 26295)
* scm_set_current_error_port:            Default Ports.     (line 20360)
* scm_set_current_input_port:            Default Ports.     (line 20358)
* scm_set_current_module:                Module System Reflection.
                                                            (line 24460)
* scm_set_current_output_port:           Default Ports.     (line 20359)
* scm_set_object_properties_x:           Object Properties. (line 17426)
* scm_set_object_property_x:             Object Properties. (line 17434)
* scm_set_port_close:                    Port Implementation.
                                                            (line 21701)
* scm_set_port_column_x:                 Reading.           (line 19986)
* scm_set_port_conversion_strategy_x:    Ports.             (line 19836)
* scm_set_port_encoding_x:               Ports.             (line 19814)
* scm_set_port_end_input:                Port Implementation.
                                                            (line 21721)
* scm_set_port_equalp:                   Port Implementation.
                                                            (line 21694)
* scm_set_port_filename_x:               File Ports.        (line 20558)
* scm_set_port_flush:                    Port Implementation.
                                                            (line 21713)
* scm_set_port_free:                     Port Implementation.
                                                            (line 21678)
* scm_set_port_input_waiting:            Port Implementation.
                                                            (line 21734)
* scm_set_port_line_x:                   Reading.           (line 19987)
* scm_set_port_mark:                     Port Implementation.
                                                            (line 21671)
* scm_set_port_print:                    Port Implementation.
                                                            (line 21686)
* scm_set_port_revealed_x:               Ports and File Descriptors.
                                                            (line 29205)
* scm_set_port_seek:                     Port Implementation.
                                                            (line 21756)
* scm_set_port_truncate:                 Port Implementation.
                                                            (line 21764)
* scm_set_procedure_properties_x:        Procedure Properties.
                                                            (line 15971)
* scm_set_procedure_property_x:          Procedure Properties.
                                                            (line 15975)
* scm_set_program_arguments:             Runtime Environment.
                                                            (line 30222)
* scm_set_program_arguments_scm:         Runtime Environment.
                                                            (line 30196)
* SCM_SET_SMOB_DATA:                     Smobs.             (line 15268)
* SCM_SET_SMOB_DATA_2:                   Smobs.             (line 15269)
* SCM_SET_SMOB_DATA_3:                   Smobs.             (line 15270)
* scm_set_smob_equalp:                   Smobs.             (line 15221)
* SCM_SET_SMOB_FLAGS:                    Smobs.             (line 15257)
* scm_set_smob_free:                     Smobs.             (line 15161)
* scm_set_smob_mark:                     Smobs.             (line 15184)
* SCM_SET_SMOB_OBJECT:                   Smobs.             (line 15282)
* SCM_SET_SMOB_OBJECT_2:                 Smobs.             (line 15283)
* SCM_SET_SMOB_OBJECT_3:                 Smobs.             (line 15284)
* scm_set_smob_print:                    Smobs.             (line 15205)
* scm_set_source_properties_x:           Source Properties. (line 27937)
* scm_set_source_property_x:             Source Properties. (line 27942)
* scm_set_struct_vtable_name_x:          Vtable Contents.   (line 14061)
* scm_set_thread_cleanup_x:              Threads.           (line 25847)
* scm_shared_array_increments:           Shared Arrays.     (line 13098)
* scm_shared_array_offset:               Shared Arrays.     (line 13103)
* scm_shared_array_root:                 Shared Arrays.     (line 13107)
* scm_shell:                             Initialization.    (line  6841)
* scm_shutdown:                          Network Sockets and Communication.
                                                            (line 31671)
* scm_sigaction:                         Signals.           (line 30709)
* scm_sigaction_for_thread:              Signals.           (line 30710)
* scm_signal_condition_variable:         Mutexes and Condition Variables.
                                                            (line 26034)
* scm_simple_format:                     Writing.           (line 20016)
* SCM_SIMPLE_VECTOR_LENGTH:              Vector Accessing from C.
                                                            (line 12449)
* SCM_SIMPLE_VECTOR_REF:                 Vector Accessing from C.
                                                            (line 12453)
* SCM_SIMPLE_VECTOR_SET:                 Vector Accessing from C.
                                                            (line 12457)
* scm_sint_list_to_bytevector:           Bytevectors and Integer Lists.
                                                            (line 10776)
* scm_sizeof:                            Foreign Structs.   (line 25407)
* scm_sleep:                             Signals.           (line 30781)
* scm_sloppy_assoc:                      Sloppy Alist Functions.
                                                            (line 14650)
* scm_sloppy_assq:                       Sloppy Alist Functions.
                                                            (line 14640)
* scm_sloppy_assv:                       Sloppy Alist Functions.
                                                            (line 14645)
* SCM_SMOB_DATA:                         Smobs.             (line 15261)
* SCM_SMOB_DATA_2:                       Smobs.             (line 15262)
* SCM_SMOB_DATA_3:                       Smobs.             (line 15263)
* SCM_SMOB_FLAGS:                        Smobs.             (line 15253)
* SCM_SMOB_OBJECT:                       Smobs.             (line 15275)
* SCM_SMOB_OBJECT_2:                     Smobs.             (line 15276)
* SCM_SMOB_OBJECT_2_LOC:                 Smobs.             (line 15290)
* SCM_SMOB_OBJECT_3:                     Smobs.             (line 15277)
* SCM_SMOB_OBJECT_3_LOC:                 Smobs.             (line 15291)
* SCM_SMOB_OBJECT_LOC:                   Smobs.             (line 15289)
* SCM_SMOB_PREDICATE:                    Smobs.             (line 15235)
* SCM_SNARF_INIT:                        Snarfing Macros.   (line  6863)
* scm_socket:                            Network Sockets and Communication.
                                                            (line 31566)
* scm_socketpair:                        Network Sockets and Communication.
                                                            (line 31593)
* scm_sort:                              Sorting.           (line 17482)
* scm_sorted_p:                          Sorting.           (line 17476)
* scm_sort_list:                         Sorting.           (line 17510)
* scm_sort_list_x:                       Sorting.           (line 17515)
* scm_sort_x:                            Sorting.           (line 17488)
* scm_source_properties:                 Source Properties. (line 27947)
* scm_source_property:                   Source Properties. (line 27951)
* scm_spawn_thread:                      Threads.           (line 25793)
* scm_stable_sort:                       Sorting.           (line 17495)
* scm_stable_sort_x:                     Sorting.           (line 17500)
* scm_stack_id:                          Stacks.            (line 27817)
* scm_stack_length:                      Stacks.            (line 27821)
* scm_stack_p:                           Stacks.            (line 27813)
* scm_stack_ref:                         Stacks.            (line 27825)
* scm_stat:                              File System.       (line 29588)
* scm_status_exit_val:                   Processes.         (line 30457)
* scm_status_stop_sig:                   Processes.         (line 30468)
* scm_status_term_sig:                   Processes.         (line 30463)
* scm_std_select:                        Blocking.          (line 26113)
* scm_std_sleep:                         Blocking.          (line 26119)
* scm_std_usleep:                        Blocking.          (line 26123)
* scm_strerror:                          Error Reporting.   (line 19346)
* scm_strftime:                          Time.              (line 30129)
* scm_string:                            String Constructors.
                                                            (line  9294)
* scm_string_any:                        String Predicates. (line  9245)
* scm_string_append:                     Reversing and Appending Strings.
                                                            (line  9991)
* scm_string_append_shared:              Reversing and Appending Strings.
                                                            (line 10000)
* scm_string_bytes_per_char:             String Internals.  (line 10452)
* scm_string_capitalize:                 Alphabetic Case Mapping.
                                                            (line  9955)
* scm_string_capitalize_x:               Alphabetic Case Mapping.
                                                            (line  9960)
* scm_string_ci_eq:                      String Comparison. (line  9668)
* scm_string_ci_ge:                      String Comparison. (line  9693)
* scm_string_ci_gt:                      String Comparison. (line  9683)
* scm_string_ci_le:                      String Comparison. (line  9688)
* scm_string_ci_lt:                      String Comparison. (line  9678)
* scm_string_ci_neq:                     String Comparison. (line  9673)
* scm_string_ci_to_symbol:               Symbol Primitives. (line 11161)
* scm_string_compare:                    String Comparison. (line  9624)
* scm_string_compare_ci:                 String Comparison. (line  9634)
* scm_string_concatenate:                Reversing and Appending Strings.
                                                            (line 10005)
* scm_string_concatenate_reverse:        Reversing and Appending Strings.
                                                            (line 10010)
* scm_string_concatenate_reverse_shared: Reversing and Appending Strings.
                                                            (line 10029)
* scm_string_concatenate_shared:         Reversing and Appending Strings.
                                                            (line 10023)
* scm_string_contains:                   String Searching.  (line  9895)
* scm_string_contains_ci:                String Searching.  (line  9902)
* scm_string_copy:                       String Selection.  (line  9403)
* scm_string_copy_x:                     String Modification.
                                                            (line  9541)
* scm_string_count:                      String Searching.  (line  9884)
* scm_string_delete:                     Miscellaneous String Operations.
                                                            (line 10162)
* scm_string_downcase:                   Alphabetic Case Mapping.
                                                            (line  9939)
* scm_string_downcase_x:                 Alphabetic Case Mapping.
                                                            (line  9944)
* scm_string_drop:                       String Selection.  (line  9450)
* scm_string_drop_right:                 String Selection.  (line  9458)
* scm_string_eq:                         String Comparison. (line  9643)
* scm_string_every:                      String Predicates. (line  9262)
* scm_string_fill_x:                     String Modification.
                                                            (line  9521)
* scm_string_filter:                     Miscellaneous String Operations.
                                                            (line 10153)
* scm_string_fold:                       Mapping Folding and Unfolding.
                                                            (line 10072)
* scm_string_fold_right:                 Mapping Folding and Unfolding.
                                                            (line 10078)
* scm_string_for_each:                   Mapping Folding and Unfolding.
                                                            (line 10051)
* scm_string_for_each_index:             Mapping Folding and Unfolding.
                                                            (line 10056)
* scm_string_ge:                         String Comparison. (line  9664)
* scm_string_gt:                         String Comparison. (line  9656)
* scm_string_index:                      String Searching.  (line  9773)
* scm_string_index_right:                String Searching.  (line  9847)
* scm_string_join:                       String Constructors.
                                                            (line  9323)
* scm_string_le:                         String Comparison. (line  9660)
* scm_string_length:                     String Selection.  (line  9386)
* scm_string_locale_ci_eq:               Text Collation.    (line 27298)
* scm_string_locale_ci_gt:               Text Collation.    (line 27290)
* scm_string_locale_ci_lt:               Text Collation.    (line 27288)
* scm_string_locale_downcase:            Character Case Mapping.
                                                            (line 27358)
* scm_string_locale_gt:                  Text Collation.    (line 27286)
* scm_string_locale_lt:                  Text Collation.    (line 27284)
* scm_string_locale_titlecase:           Character Case Mapping.
                                                            (line 27363)
* scm_string_locale_upcase:              Character Case Mapping.
                                                            (line 27353)
* scm_string_lt:                         String Comparison. (line  9651)
* scm_string_map:                        Mapping Folding and Unfolding.
                                                            (line 10038)
* scm_string_map_x:                      Mapping Folding and Unfolding.
                                                            (line 10044)
* scm_string_neq:                        String Comparison. (line  9647)
* scm_string_normalize_nfc:              String Comparison. (line  9762)
* scm_string_normalize_nfd:              String Comparison. (line  9754)
* scm_string_normalize_nfkc:             String Comparison. (line  9766)
* scm_string_normalize_nfkd:             String Comparison. (line  9758)
* scm_string_null_p:                     String Predicates. (line  9238)
* scm_string_p:                          String Predicates. (line  9231)
* scm_string_pad:                        String Selection.  (line  9463)
* scm_string_pad_right:                  String Selection.  (line  9464)
* scm_string_prefix_ci_p:                String Searching.  (line  9831)
* scm_string_prefix_length:              String Searching.  (line  9800)
* scm_string_prefix_length_ci:           String Searching.  (line  9806)
* scm_string_prefix_p:                   String Searching.  (line  9826)
* scm_string_ref:                        String Selection.  (line  9393)
* scm_string_replace:                    Miscellaneous String Operations.
                                                            (line 10140)
* scm_string_reverse:                    Reversing and Appending Strings.
                                                            (line  9980)
* scm_string_reverse_x:                  Reversing and Appending Strings.
                                                            (line  9985)
* scm_string_rindex:                     String Searching.  (line  9786)
* scm_string_set_x:                      String Modification.
                                                            (line  9512)
* scm_string_skip:                       String Searching.  (line  9860)
* scm_string_skip_right:                 String Searching.  (line  9872)
* scm_string_split:                      List/String Conversion.
                                                            (line  9353)
* scm_string_suffix_ci_p:                String Searching.  (line  9842)
* scm_string_suffix_length:              String Searching.  (line  9813)
* scm_string_suffix_length_ci:           String Searching.  (line  9819)
* scm_string_suffix_p:                   String Searching.  (line  9837)
* scm_string_tabulate:                   String Constructors.
                                                            (line  9316)
* scm_string_take:                       String Selection.  (line  9446)
* scm_string_take_right:                 String Selection.  (line  9454)
* scm_string_titlecase:                  Alphabetic Case Mapping.
                                                            (line  9969)
* scm_string_titlecase_x:                Alphabetic Case Mapping.
                                                            (line  9973)
* scm_string_tokenize:                   Miscellaneous String Operations.
                                                            (line 10145)
* scm_string_to_char_set:                Creating Character Sets.
                                                            (line  8798)
* scm_string_to_char_set_x:              Creating Character Sets.
                                                            (line  8804)
* scm_string_to_list:                    List/String Conversion.
                                                            (line  9349)
* scm_string_to_number:                  Conversion.        (line  7793)
* scm_string_to_symbol:                  Symbol Primitives. (line 11153)
* scm_string_to_utf16:                   Bytevectors as Strings.
                                                            (line 10839)
* scm_string_to_utf32:                   Bytevectors as Strings.
                                                            (line 10840)
* scm_string_to_utf8:                    Bytevectors as Strings.
                                                            (line 10838)
* scm_string_trim:                       String Selection.  (line  9481)
* scm_string_trim_both:                  String Selection.  (line  9483)
* scm_string_trim_right:                 String Selection.  (line  9482)
* scm_string_unfold:                     Mapping Folding and Unfolding.
                                                            (line 10084)
* scm_string_unfold_right:               Mapping Folding and Unfolding.
                                                            (line 10099)
* scm_string_upcase:                     Alphabetic Case Mapping.
                                                            (line  9924)
* scm_string_upcase_x:                   Alphabetic Case Mapping.
                                                            (line  9929)
* scm_string_xcopy_x:                    Miscellaneous String Operations.
                                                            (line 10131)
* scm_strptime:                          Time.              (line 30144)
* scm_struct_p:                          Structure Basics.  (line 13991)
* scm_struct_ref:                        Structure Basics.  (line 13995)
* scm_struct_set_x:                      Structure Basics.  (line 14003)
* scm_struct_vtable:                     Structure Basics.  (line 14011)
* scm_struct_vtable_name:                Vtable Contents.   (line 14060)
* scm_struct_vtable_p:                   Meta-Vtables.      (line 14118)
* scm_substring:                         String Selection.  (line  9410)
* scm_substring_copy:                    String Selection.  (line  9402)
* scm_substring_copy <1>:                String Selection.  (line  9428)
* scm_substring_downcase:                Alphabetic Case Mapping.
                                                            (line  9938)
* scm_substring_downcase_x:              Alphabetic Case Mapping.
                                                            (line  9943)
* scm_substring_fill_x:                  String Modification.
                                                            (line  9520)
* scm_substring_fill_x <1>:              String Modification.
                                                            (line  9526)
* scm_substring_hash:                    String Comparison. (line  9698)
* scm_substring_hash_ci:                 String Comparison. (line  9705)
* scm_substring_move_x:                  String Modification.
                                                            (line  9535)
* scm_substring_read_only:               String Selection.  (line  9433)
* scm_substring_shared:                  String Selection.  (line  9422)
* scm_substring_to_list:                 List/String Conversion.
                                                            (line  9348)
* scm_substring_upcase:                  Alphabetic Case Mapping.
                                                            (line  9923)
* scm_substring_upcase_x:                Alphabetic Case Mapping.
                                                            (line  9928)
* scm_sum:                               Arithmetic.        (line  7861)
* scm_supports_source_properties_p:      Source Properties. (line 27925)
* SCM_SYMBOL:                            Snarfing Macros.   (line  6892)
* scm_symbol_fref:                       Symbol Props.      (line 11286)
* scm_symbol_fset_x:                     Symbol Props.      (line 11290)
* scm_symbol_hash:                       Symbol Keys.       (line 11062)
* scm_symbol_interned_p:                 Symbol Uninterned. (line 11430)
* scm_symbol_p:                          Symbol Primitives. (line 11096)
* scm_symbol_pref:                       Symbol Props.      (line 11294)
* scm_symbol_pset_x:                     Symbol Props.      (line 11298)
* scm_symbol_to_keyword:                 Keyword Procedures.
                                                            (line 11645)
* scm_symbol_to_string:                  Symbol Primitives. (line 11108)
* scm_symlink:                           File System.       (line 29748)
* scm_sync:                              File System.       (line 29804)
* scm_syserror:                          Handling Errors.   (line 19633)
* scm_syserror_msg:                      Handling Errors.   (line 19634)
* scm_system:                            Processes.         (line 30473)
* scm_system_async_mark:                 System asyncs.     (line 25694)
* scm_system_async_mark_for_thread:      System asyncs.     (line 25695)
* scm_system_star:                       Processes.         (line 30483)
* scm_sys_library_dir:                   Build Config.      (line 26683)
* scm_sys_make_void_port:                Void Ports.        (line 20708)
* scm_sys_package_data_dir:              Build Config.      (line 26677)
* scm_sys_search_load_path:              Load Paths.        (line 23012)
* scm_sys_site_ccache_dir:               Build Config.      (line 26699)
* scm_sys_site_dir:                      Build Config.      (line 26693)
* scm_sys_string_dump:                   String Internals.  (line 10457)
* scm_take_c32vector:                    SRFI-4 API.        (line 35256)
* scm_take_c64vector:                    SRFI-4 API.        (line 35257)
* scm_take_f32vector:                    SRFI-4 API.        (line 35254)
* scm_take_f64vector:                    SRFI-4 API.        (line 35255)
* scm_take_locale_string:                Conversion to/from C.
                                                            (line 10291)
* scm_take_locale_stringn:               Conversion to/from C.
                                                            (line 10292)
* scm_take_locale_symbol:                Symbol Primitives. (line 11228)
* scm_take_locale_symboln:               Symbol Primitives. (line 11229)
* scm_take_s16vector:                    SRFI-4 API.        (line 35244)
* scm_take_s32vector:                    SRFI-4 API.        (line 35248)
* scm_take_s64vector:                    SRFI-4 API.        (line 35252)
* scm_take_s8vector:                     SRFI-4 API.        (line 35240)
* scm_take_u16vector:                    SRFI-4 API.        (line 35242)
* scm_take_u32vector:                    SRFI-4 API.        (line 35246)
* scm_take_u64vector:                    SRFI-4 API.        (line 35250)
* scm_take_u8vector:                     SRFI-4 API.        (line 35238)
* scm_tcgetpgrp:                         Terminals and Ptys.
                                                            (line 30864)
* scm_tcsetpgrp:                         Terminals and Ptys.
                                                            (line 30877)
* scm_textdomain:                        Gettext Support.   (line 27659)
* scm_thread_cleanup:                    Threads.           (line 25859)
* scm_thread_exited_p:                   Threads.           (line 25824)
* scm_thread_p:                          Threads.           (line 25808)
* scm_throw:                             Throw.             (line 19247)
* scm_thunk_p:                           Procedure Properties.
                                                            (line 15945)
* scm_times:                             Time.              (line 30158)
* scm_tmpfile:                           File System.       (line 29858)
* scm_tmpnam:                            File System.       (line 29824)
* scm_total_processor_count:             Processes.         (line 30645)
* scm_to_bool:                           Booleans.          (line  7045)
* scm_to_char:                           Integers.          (line  7271)
* scm_to_char_set:                       Creating Character Sets.
                                                            (line  8846)
* scm_to_double:                         Reals and Rationals.
                                                            (line  7472)
* scm_to_int:                            Integers.          (line  7276)
* scm_to_int16:                          Integers.          (line  7287)
* scm_to_int32:                          Integers.          (line  7289)
* scm_to_int64:                          Integers.          (line  7291)
* scm_to_int8:                           Integers.          (line  7285)
* scm_to_intmax:                         Integers.          (line  7293)
* scm_to_locale_string:                  Conversion to/from C.
                                                            (line 10299)
* scm_to_locale_stringbuf:               Conversion to/from C.
                                                            (line 10325)
* scm_to_locale_stringn:                 Conversion to/from C.
                                                            (line 10300)
* scm_to_long:                           Integers.          (line  7278)
* scm_to_long_long:                      Integers.          (line  7280)
* scm_to_mpz:                            Integers.          (line  7332)
* scm_to_pointer:                        Foreign Variables. (line 25261)
* scm_to_ptrdiff_t:                      Integers.          (line  7284)
* scm_to_schar:                          Integers.          (line  7272)
* scm_to_short:                          Integers.          (line  7274)
* scm_to_signed_integer:                 Integers.          (line  7256)
* scm_to_size_t:                         Integers.          (line  7282)
* scm_to_sockaddr:                       Network Socket Address.
                                                            (line 31539)
* scm_to_ssize_t:                        Integers.          (line  7283)
* scm_to_uchar:                          Integers.          (line  7273)
* scm_to_uint:                           Integers.          (line  7277)
* scm_to_uint16:                         Integers.          (line  7288)
* scm_to_uint32:                         Integers.          (line  7290)
* scm_to_uint64:                         Integers.          (line  7292)
* scm_to_uint8:                          Integers.          (line  7286)
* scm_to_uintmax:                        Integers.          (line  7294)
* scm_to_ulong:                          Integers.          (line  7279)
* scm_to_ulong_long:                     Integers.          (line  7281)
* scm_to_unsigned_integer:               Integers.          (line  7258)
* scm_to_ushort:                         Integers.          (line  7275)
* scm_transpose_array:                   Shared Arrays.     (line 13124)
* scm_truncate_divide:                   Arithmetic.        (line  8002)
* scm_truncate_file:                     Random Access.     (line 20107)
* scm_truncate_number:                   Arithmetic.        (line  7905)
* scm_truncate_quotient:                 Arithmetic.        (line  8003)
* scm_truncate_remainder:                Arithmetic.        (line  8004)
* scm_try_arbiter:                       Arbiters.          (line 25636)
* scm_try_mutex:                         Mutexes and Condition Variables.
                                                            (line 25963)
* scm_ttyname:                           Terminals and Ptys.
                                                            (line 30854)
* scm_typed_array_p:                     Array Procedures.  (line 12804)
* scm_tzset:                             Time.              (line 30122)
* scm_u16vector:                         SRFI-4 API.        (line 35091)
* scm_u16vector_elements:                SRFI-4 API.        (line 35273)
* scm_u16vector_length:                  SRFI-4 API.        (line 35119)
* scm_u16vector_p:                       SRFI-4 API.        (line 35035)
* scm_u16vector_ref:                     SRFI-4 API.        (line 35145)
* scm_u16vector_set_x:                   SRFI-4 API.        (line 35172)
* scm_u16vector_to_list:                 SRFI-4 API.        (line 35199)
* scm_u16vector_writable_elements:       SRFI-4 API.        (line 35301)
* scm_u32vector:                         SRFI-4 API.        (line 35093)
* scm_u32vector_elements:                SRFI-4 API.        (line 35277)
* scm_u32vector_length:                  SRFI-4 API.        (line 35121)
* scm_u32vector_p:                       SRFI-4 API.        (line 35037)
* scm_u32vector_ref:                     SRFI-4 API.        (line 35147)
* scm_u32vector_set_x:                   SRFI-4 API.        (line 35174)
* scm_u32vector_to_list:                 SRFI-4 API.        (line 35201)
* scm_u32vector_writable_elements:       SRFI-4 API.        (line 35305)
* scm_u64vector:                         SRFI-4 API.        (line 35095)
* scm_u64vector_elements:                SRFI-4 API.        (line 35281)
* scm_u64vector_length:                  SRFI-4 API.        (line 35123)
* scm_u64vector_p:                       SRFI-4 API.        (line 35039)
* scm_u64vector_ref:                     SRFI-4 API.        (line 35149)
* scm_u64vector_set_x:                   SRFI-4 API.        (line 35176)
* scm_u64vector_to_list:                 SRFI-4 API.        (line 35203)
* scm_u64vector_writable_elements:       SRFI-4 API.        (line 35309)
* scm_u8vector:                          SRFI-4 API.        (line 35089)
* scm_u8vector_elements:                 SRFI-4 API.        (line 35269)
* scm_u8vector_length:                   SRFI-4 API.        (line 35117)
* scm_u8vector_p:                        SRFI-4 API.        (line 35033)
* scm_u8vector_ref:                      SRFI-4 API.        (line 35143)
* scm_u8vector_set_x:                    SRFI-4 API.        (line 35170)
* scm_u8vector_to_list:                  SRFI-4 API.        (line 35197)
* scm_u8vector_writable_elements:        SRFI-4 API.        (line 35297)
* scm_u8_list_to_bytevector:             Bytevectors and Integer Lists.
                                                            (line 10756)
* scm_ucs_range_to_char_set:             Creating Character Sets.
                                                            (line  8821)
* scm_ucs_range_to_char_set_x:           Creating Character Sets.
                                                            (line  8833)
* scm_uint_list_to_bytevector:           Bytevectors and Integer Lists.
                                                            (line 10771)
* scm_umask:                             Processes.         (line 30305)
* scm_uname:                             System Identification.
                                                            (line 31903)
* SCM_UNBNDP:                            Immediate objects. (line 47235)
* SCM_UNDEFINED:                         Immediate objects. (line 47224)
* scm_unget_bytevector:                  R6RS Binary Input. (line 21284)
* scm_uniform_array_read_x:              Array Procedures.  (line 12981)
* scm_uniform_array_write:               Array Procedures.  (line 12996)
* scm_unlock_mutex:                      Mutexes and Condition Variables.
                                                            (line 25970)
* scm_unlock_mutex_timed:                Mutexes and Condition Variables.
                                                            (line 25971)
* SCM_UNPACK:                            The SCM Type.      (line  6741)
* scm_unread_char:                       Reading.           (line 19942)
* scm_unread_char <1>:                   Ports and File Descriptors.
                                                            (line 29310)
* scm_unread_string:                     Reading.           (line 19949)
* SCM_UNSPECIFIED:                       Immediate objects. (line 47215)
* scm_usleep:                            Signals.           (line 30782)
* scm_utf16_to_string:                   Bytevectors as Strings.
                                                            (line 10850)
* scm_utf32_to_string:                   Bytevectors as Strings.
                                                            (line 10851)
* scm_utf8_to_string:                    Bytevectors as Strings.
                                                            (line 10849)
* scm_utime:                             File System.       (line 29687)
* scm_values:                            Multiple Values.   (line 18874)
* SCM_VARIABLE:                          Snarfing Macros.   (line  6928)
* scm_variable_bound_p:                  Variables.         (line 24419)
* SCM_VARIABLE_INIT:                     Snarfing Macros.   (line  6934)
* scm_variable_p:                        Variables.         (line 24438)
* scm_variable_ref:                      Variables.         (line 24424)
* scm_variable_set_x:                    Variables.         (line 24429)
* scm_variable_unset_x:                  Variables.         (line 24434)
* scm_vector:                            Vector Creation.   (line 12306)
* scm_vector_copy:                       Vector Accessors.  (line 12399)
* scm_vector_elements:                   Vector Accessing from C.
                                                            (line 12461)
* scm_vector_fill_x:                     Vector Accessors.  (line 12394)
* scm_vector_length:                     Vector Accessors.  (line 12353)
* scm_vector_move_left_x:                Vector Accessors.  (line 12403)
* scm_vector_move_right_x:               Vector Accessors.  (line 12415)
* scm_vector_p:                          Vector Creation.   (line 12339)
* scm_vector_ref:                        Vector Accessors.  (line 12360)
* scm_vector_set_x:                      Vector Accessors.  (line 12383)
* scm_vector_to_list:                    Vector Creation.   (line 12315)
* scm_vector_writable_elements:          Vector Accessing from C.
                                                            (line 12490)
* scm_version:                           Build Config.      (line 26657)
* scm_waitpid:                           Processes.         (line 30416)
* scm_wait_condition_variable:           Mutexes and Condition Variables.
                                                            (line 26015)
* scm_weak_key_hash_table_p:             Weak hash tables.  (line 23699)
* scm_weak_value_hash_table_p:           Weak hash tables.  (line 23700)
* scm_weak_vector:                       Weak vectors.      (line 23717)
* scm_weak_vector_p:                     Weak vectors.      (line 23723)
* scm_weak_vector_ref:                   Weak vectors.      (line 23727)
* scm_weak_vector_set_x:                 Weak vectors.      (line 23732)
* scm_without_guile:                     Blocking.          (line 26086)
* scm_with_continuation_barrier:         Continuation Barriers.
                                                            (line 19713)
* scm_with_dynamic_state:                Fluids and Dynamic States.
                                                            (line 26300)
* scm_with_fluid:                        Fluids and Dynamic States.
                                                            (line 26237)
* scm_with_fluids:                       Fluids and Dynamic States.
                                                            (line 26242)
* scm_with_guile:                        Initialization.    (line  6766)
* scm_with_throw_handler:                Throw Handlers.    (line 19149)
* scm_write_char:                        Writing.           (line 20026)
* scm_write_line:                        Line/Delimited.    (line 20182)
* scm_write_objcode:                     Bytecode and Objcode.
                                                            (line 49270)
* scm_write_string_partial:              Block Reading and Writing.
                                                            (line 20284)
* scm_wrong_num_args:                    Handling Errors.   (line 19645)
* scm_wrong_type_arg:                    Handling Errors.   (line 19646)
* scm_wrong_type_arg_msg:                Handling Errors.   (line 19648)
* scm_xsubstring:                        Miscellaneous String Operations.
                                                            (line 10118)
* scm_zero_p:                            Comparison.        (line  7768)
* script-stexi-documentation:            texinfo reflection.
                                                            (line 44034)
* sdocbook-flatten:                      texinfo docbook.   (line 43702)
* search-path:                           Load Paths.        (line 23071)
* second:                                SRFI-1 Selectors.  (line 34132)
* seconds->time:                         SRFI-18 Time.      (line 35825)
* seed->random-state:                    Random.            (line  8368)
* seek:                                  Random Access.     (line 20080)
* select:                                Ports and File Descriptors.
                                                            (line 29513)
* select-kids:                           SXPath.            (line 43485)
* send:                                  Network Sockets and Communication.
                                                            (line 31782)
* sendfile:                              File System.       (line 29710)
* sendto:                                Network Sockets and Communication.
                                                            (line 31822)
* sendto <1>:                            Network Sockets and Communication.
                                                            (line 31823)
* sendto <2>:                            Network Sockets and Communication.
                                                            (line 31824)
* sendto <3>:                            Network Sockets and Communication.
                                                            (line 31826)
* serious-condition?:                    SRFI-35.           (line 36659)
* serious-condition? <1>:                rnrs conditions.   (line 39337)
* serve-one-client:                      Web Server.        (line 33354)
* servent:aliases:                       Network Databases. (line 31401)
* servent:name:                          Network Databases. (line 31399)
* servent:port:                          Network Databases. (line 31403)
* servent:proto:                         Network Databases. (line 31405)
* set!:                                  rnrs base.         (line 38476)
* set! <1>:                              Slot Description Example.
                                                            (line 44536)
* set-box!:                              SRFI-111.          (line 38276)
* set-buffered-input-continuation?!:     Buffered Input.    (line 42029)
* set-car!:                              Pairs.             (line 11908)
* set-car! <1>:                          Inlined Scheme Instructions.
                                                            (line 48474)
* set-cdr!:                              Pairs.             (line 11913)
* set-cdr! <1>:                          Inlined Scheme Instructions.
                                                            (line 48475)
* set-current-dynamic-state:             Fluids and Dynamic States.
                                                            (line 26294)
* set-current-error-port:                Default Ports.     (line 20357)
* set-current-input-port:                Default Ports.     (line 20355)
* set-current-module:                    Module System Reflection.
                                                            (line 24459)
* set-current-output-port:               Default Ports.     (line 20356)
* set-field:                             SRFI-9 Records.    (line 13713)
* set-fields:                            SRFI-9 Records.    (line 13723)
* set-object-properties!:                Object Properties. (line 17425)
* set-object-property!:                  Object Properties. (line 17433)
* set-port-column!:                      Reading.           (line 19984)
* set-port-conversion-strategy!:         Ports.             (line 19835)
* set-port-encoding!:                    Ports.             (line 19813)
* set-port-encoding! <1>:                Character Encoding of Source Files.
                                                            (line 23126)
* set-port-filename!:                    File Ports.        (line 20557)
* set-port-line!:                        Reading.           (line 19985)
* set-port-position!:                    R6RS Port Manipulation.
                                                            (line 21105)
* set-port-revealed!:                    Ports and File Descriptors.
                                                            (line 29204)
* set-procedure-properties!:             Procedure Properties.
                                                            (line 15970)
* set-procedure-property!:               Procedure Properties.
                                                            (line 15974)
* set-program-arguments:                 Runtime Environment.
                                                            (line 30194)
* set-readline-input-port!:              Readline Functions.
                                                            (line 40536)
* set-readline-output-port!:             Readline Functions.
                                                            (line 40537)
* set-readline-prompt!:                  Readline Functions.
                                                            (line 40574)
* set-record-type-printer!:              SRFI-9 Records.    (line 13672)
* set-source-properties!:                Source Properties. (line 27936)
* set-source-property!:                  Source Properties. (line 27941)
* set-struct-vtable-name!:               Vtable Contents.   (line 14059)
* set-symbol-property!:                  Symbol Props.      (line 11308)
* set-thread-cleanup!:                   Threads.           (line 25846)
* set-time-nanosecond!:                  SRFI-19 Time.      (line 35983)
* set-time-second!:                      SRFI-19 Time.      (line 35984)
* set-time-type!:                        SRFI-19 Time.      (line 35982)
* set-tm:gmtoff:                         Time.              (line 30068)
* set-tm:hour:                           Time.              (line 30046)
* set-tm:isdst:                          Time.              (line 30064)
* set-tm:mday:                           Time.              (line 30049)
* set-tm:min:                            Time.              (line 30043)
* set-tm:mon:                            Time.              (line 30052)
* set-tm:sec:                            Time.              (line 30040)
* set-tm:wday:                           Time.              (line 30058)
* set-tm:yday:                           Time.              (line 30061)
* set-tm:year:                           Time.              (line 30055)
* set-tm:zone:                           Time.              (line 30077)
* set-vm-trace-level!:                   VM Hooks.          (line 28466)
* setaffinity:                           Processes.         (line 30636)
* setegid:                               Processes.         (line 30384)
* setenv:                                Runtime Environment.
                                                            (line 30256)
* seteuid:                               Processes.         (line 30377)
* setgid:                                Processes.         (line 30371)
* setgr:                                 User Information.  (line 29998)
* setgrent:                              User Information.  (line 29985)
* setgroups:                             Processes.         (line 30357)
* sethost:                               Network Databases. (line 31291)
* sethostent:                            Network Databases. (line 31273)
* sethostname:                           System Identification.
                                                            (line 31927)
* setitimer:                             Signals.           (line 30797)
* setlocale:                             Locales.           (line 31935)
* setnet:                                Network Databases. (line 31341)
* setnetent:                             Network Databases. (line 31326)
* setpgid:                               Processes.         (line 30396)
* setpriority:                           Processes.         (line 30599)
* setproto:                              Network Databases. (line 31388)
* setprotoent:                           Network Databases. (line 31373)
* setpw:                                 User Information.  (line 29955)
* setpwent:                              User Information.  (line 29942)
* setserv:                               Network Databases. (line 31449)
* setservent:                            Network Databases. (line 31434)
* setsid:                                Processes.         (line 30403)
* setsockopt:                            Network Sockets and Communication.
                                                            (line 31603)
* setter:                                Procedures with Setters.
                                                            (line 16042)
* setuid:                                Processes.         (line 30365)
* setvbuf:                               Ports and File Descriptors.
                                                            (line 29428)
* seventh:                               SRFI-1 Selectors.  (line 34137)
* shallow-clone:                         GOOPS Object Miscellany.
                                                            (line 45574)
* shallow-clone <1>:                     GOOPS Object Miscellany.
                                                            (line 45575)
* shared-array-increments:               Shared Arrays.     (line 13097)
* shared-array-offset:                   Shared Arrays.     (line 13102)
* shared-array-root:                     Shared Arrays.     (line 13106)
* shift:                                 Shift and Reset.   (line 18724)
* show:                                  Help Commands.     (line  3632)
* shutdown:                              Network Sockets and Communication.
                                                            (line 31670)
* sigaction:                             Signals.           (line 30708)
* signal-condition-variable:             Mutexes and Condition Variables.
                                                            (line 26033)
* simple-conditions:                     rnrs conditions.   (line 39295)
* simple-format:                         Writing.           (line 20015)
* sin:                                   Scientific.        (line  8112)
* sin <1>:                               rnrs base.         (line 38544)
* sinh:                                  Scientific.        (line  8141)
* sint-list->bytevector:                 Bytevectors and Integer Lists.
                                                            (line 10775)
* sixth:                                 SRFI-1 Selectors.  (line 34136)
* sizeof:                                Foreign Structs.   (line 25406)
* size_t:                                Array Procedures.  (line 12907)
* skip-until:                            sxml ssax input-parse.
                                                            (line 43552)
* skip-while:                            sxml ssax input-parse.
                                                            (line 43554)
* sleep:                                 Signals.           (line 30779)
* sloppy-assoc:                          Sloppy Alist Functions.
                                                            (line 14649)
* sloppy-assq:                           Sloppy Alist Functions.
                                                            (line 14639)
* sloppy-assv:                           Sloppy Alist Functions.
                                                            (line 14644)
* slot-bound-using-class?:               Accessing Slots.   (line 45442)
* slot-bound?:                           Accessing Slots.   (line 45400)
* slot-definition-accessor:              Slots.             (line 45307)
* slot-definition-allocation:            Slots.             (line 45292)
* slot-definition-getter:                Slots.             (line 45297)
* slot-definition-init-form:             Slots.             (line 45318)
* slot-definition-init-keyword:          Slots.             (line 45329)
* slot-definition-init-thunk:            Slots.             (line 45324)
* slot-definition-init-value:            Slots.             (line 45312)
* slot-definition-name:                  Slots.             (line 45286)
* slot-definition-options:               Slots.             (line 45289)
* slot-definition-setter:                Slots.             (line 45302)
* slot-exists-using-class?:              Accessing Slots.   (line 45438)
* slot-exists?:                          Accessing Slots.   (line 45397)
* slot-init-function:                    Slots.             (line 45335)
* slot-missing:                          Accessing Slots.   (line 45498)
* slot-missing <1>:                      Accessing Slots.   (line 45499)
* slot-missing <2>:                      Accessing Slots.   (line 45500)
* slot-missing <3>:                      Accessing Slots.   (line 45501)
* slot-ref:                              Instance Creation. (line 44300)
* slot-ref <1>:                          Accessing Slots.   (line 45408)
* slot-ref <2>:                          Inlined Scheme Instructions.
                                                            (line 48486)
* slot-ref-using-class:                  Accessing Slots.   (line 45451)
* slot-set:                              Inlined Scheme Instructions.
                                                            (line 48487)
* slot-set!:                             Instance Creation. (line 44300)
* slot-set! <1>:                         Accessing Slots.   (line 45419)
* slot-set-using-class!:                 Accessing Slots.   (line 45463)
* slot-unbound:                          Accessing Slots.   (line 45511)
* slot-unbound <1>:                      Accessing Slots.   (line 45512)
* slot-unbound <2>:                      Accessing Slots.   (line 45513)
* slot-unbound <3>:                      Accessing Slots.   (line 45514)
* sockaddr:addr:                         Network Socket Address.
                                                            (line 31495)
* sockaddr:fam:                          Network Socket Address.
                                                            (line 31488)
* sockaddr:flowinfo:                     Network Socket Address.
                                                            (line 31503)
* sockaddr:path:                         Network Socket Address.
                                                            (line 31492)
* sockaddr:port:                         Network Socket Address.
                                                            (line 31499)
* sockaddr:scopeid:                      Network Socket Address.
                                                            (line 31507)
* socket:                                Network Sockets and Communication.
                                                            (line 31565)
* socketpair:                            Network Sockets and Communication.
                                                            (line 31592)
* sort:                                  Sorting.           (line 17481)
* sort!:                                 Sorting.           (line 17487)
* sort-list:                             Sorting.           (line 17509)
* sort-list!:                            Sorting.           (line 17514)
* sorted?:                               Sorting.           (line 17475)
* source-properties:                     Source Properties. (line 27946)
* source-property:                       Source Properties. (line 27950)
* source:addr:                           Compiled Procedures.
                                                            (line 15496)
* source:column:                         Compiled Procedures.
                                                            (line 15498)
* source:file:                           Compiled Procedures.
                                                            (line 15499)
* source:line:                           Compiled Procedures.
                                                            (line 15497)
* span:                                  SRFI-1 Searching.  (line 34511)
* span!:                                 SRFI-1 Searching.  (line 34512)
* spawn-coop-repl-server:                Cooperative REPL Servers.
                                                            (line 23363)
* spawn-server:                          REPL Servers.      (line 23322)
* split-and-decode-uri-path:             URIs.              (line 32231)
* split-at:                              SRFI-1 Selectors.  (line 34168)
* split-at!:                             SRFI-1 Selectors.  (line 34169)
* sqrt:                                  Scientific.        (line  8099)
* sqrt <1>:                              rnrs base.         (line 38540)
* SRV:send-reply:                        Transforming SXML. (line 43241)
* ssax:complete-start-tag:               SSAX.              (line 43169)
* ssax:make-elem-parser:                 SSAX.              (line 43183)
* ssax:make-parser:                      SSAX.              (line 43179)
* ssax:make-pi-parser:                   SSAX.              (line 43181)
* ssax:read-attributes:                  SSAX.              (line 43167)
* ssax:read-cdata-body:                  SSAX.              (line 43163)
* ssax:read-char-data:                   SSAX.              (line 43174)
* ssax:read-char-ref:                    SSAX.              (line 43165)
* ssax:read-external-id:                 SSAX.              (line 43172)
* ssax:read-markup-token:                SSAX.              (line 43161)
* ssax:read-pi-body-as-string:           SSAX.              (line 43157)
* ssax:reverse-collect-str-drop-ws:      SSAX.              (line 43159)
* ssax:skip-internal-dtd:                SSAX.              (line 43155)
* ssax:uri-string->symbol:               SSAX.              (line 43153)
* ssax:xml->sxml:                        SSAX.              (line 43177)
* stable-sort:                           Sorting.           (line 17494)
* stable-sort!:                          Sorting.           (line 17499)
* stack-id:                              Stacks.            (line 27816)
* stack-length:                          Stacks.            (line 27820)
* stack-ref:                             Stacks.            (line 27824)
* stack?:                                Stacks.            (line 27812)
* standard-error-port:                   R6RS Output Ports. (line 21438)
* standard-input-port:                   R6RS Input Ports.  (line 21163)
* standard-output-port:                  R6RS Output Ports. (line 21437)
* start-stack:                           Stack Capture.     (line 27802)
* stat:                                  File System.       (line 29587)
* stat:atime:                            File System.       (line 29618)
* stat:atimensec:                        File System.       (line 29625)
* stat:blksize:                          File System.       (line 29633)
* stat:blocks:                           File System.       (line 29637)
* stat:ctime:                            File System.       (line 29622)
* stat:ctimensec:                        File System.       (line 29627)
* stat:dev:                              File System.       (line 29597)
* stat:gid:                              File System.       (line 29610)
* stat:ino:                              File System.       (line 29599)
* stat:mode:                             File System.       (line 29602)
* stat:mtime:                            File System.       (line 29620)
* stat:mtimensec:                        File System.       (line 29626)
* stat:nlink:                            File System.       (line 29606)
* stat:perms:                            File System.       (line 29649)
* stat:rdev:                             File System.       (line 29612)
* stat:size:                             File System.       (line 29616)
* stat:type:                             File System.       (line 29645)
* stat:uid:                              File System.       (line 29608)
* statistics:                            System Commands.   (line  3816)
* statprof:                              Statprof.          (line 42747)
* statprof-accumulated-time:             Statprof.          (line 42681)
* statprof-active?:                      Statprof.          (line 42661)
* statprof-call-data->stats:             Statprof.          (line 42707)
* statprof-call-data-calls:              Statprof.          (line 42701)
* statprof-call-data-cum-samples:        Statprof.          (line 42703)
* statprof-call-data-name:               Statprof.          (line 42699)
* statprof-call-data-self-samples:       Statprof.          (line 42705)
* statprof-display:                      Statprof.          (line 42724)
* statprof-display-anomolies:            Statprof.          (line 42728)
* statprof-fetch-call-tree:              Statprof.          (line 42739)
* statprof-fetch-stacks:                 Statprof.          (line 42732)
* statprof-fold-call-data:               Statprof.          (line 42687)
* statprof-proc-call-data:               Statprof.          (line 42695)
* statprof-reset:                        Statprof.          (line 42671)
* statprof-sample-count:                 Statprof.          (line 42684)
* statprof-start:                        Statprof.          (line 42665)
* statprof-stats-%-time-in-proc:         Statprof.          (line 42712)
* statprof-stats-calls:                  Statprof.          (line 42718)
* statprof-stats-cum-secs-in-proc:       Statprof.          (line 42714)
* statprof-stats-cum-secs-per-call:      Statprof.          (line 42722)
* statprof-stats-proc-name:              Statprof.          (line 42710)
* statprof-stats-self-secs-in-proc:      Statprof.          (line 42716)
* statprof-stats-self-secs-per-call:     Statprof.          (line 42720)
* statprof-stop:                         Statprof.          (line 42668)
* status:exit-val:                       Processes.         (line 30456)
* status:stop-sig:                       Processes.         (line 30467)
* status:term-sig:                       Processes.         (line 30462)
* step:                                  Debug Commands.    (line  3788)
* stexi->plain-text:                     texinfo plain-text.
                                                            (line 43997)
* stexi->shtml:                          texinfo html.      (line 43777)
* stexi->sxml:                           texinfo.           (line 43675)
* stexi->texi:                           texinfo serialize. (line 44011)
* stexi-extract-index:                   texinfo indexing.  (line 43797)
* stop-server-and-clients!:              REPL Servers.      (line 23331)
* stream:                                SRFI-41 Stream Library.
                                                            (line 37035)
* stream->list:                          SRFI-41 Stream Library.
                                                            (line 37047)
* stream->list <1>:                      Streams.           (line 41947)
* stream->list&length:                   Streams.           (line 41954)
* stream->reversed-list:                 Streams.           (line 41950)
* stream->reversed-list&length:          Streams.           (line 41959)
* stream->vector:                        Streams.           (line 41964)
* stream-append:                         SRFI-41 Stream Library.
                                                            (line 37059)
* stream-car:                            SRFI-41 Stream Primitives.
                                                            (line 36928)
* stream-car <1>:                        Streams.           (line 41920)
* stream-cdr:                            SRFI-41 Stream Primitives.
                                                            (line 36934)
* stream-cdr <1>:                        Streams.           (line 41923)
* stream-concat:                         SRFI-41 Stream Library.
                                                            (line 37066)
* stream-cons:                           SRFI-41 Stream Primitives.
                                                            (line 36901)
* stream-constant:                       SRFI-41 Stream Library.
                                                            (line 37073)
* stream-drop:                           SRFI-41 Stream Library.
                                                            (line 37080)
* stream-drop-while:                     SRFI-41 Stream Library.
                                                            (line 37088)
* stream-filter:                         SRFI-41 Stream Library.
                                                            (line 37094)
* stream-fold:                           SRFI-41 Stream Library.
                                                            (line 37101)
* stream-fold <1>:                       Streams.           (line 41967)
* stream-for-each:                       SRFI-41 Stream Library.
                                                            (line 37115)
* stream-for-each <1>:                   Streams.           (line 41976)
* stream-from:                           SRFI-41 Stream Library.
                                                            (line 37120)
* stream-iterate:                        SRFI-41 Stream Library.
                                                            (line 37128)
* stream-lambda:                         SRFI-41 Stream Primitives.
                                                            (line 36938)
* stream-length:                         SRFI-41 Stream Library.
                                                            (line 37133)
* stream-let:                            SRFI-41 Stream Library.
                                                            (line 37138)
* stream-map:                            SRFI-41 Stream Library.
                                                            (line 37164)
* stream-map <1>:                        Streams.           (line 41984)
* stream-match:                          SRFI-41 Stream Library.
                                                            (line 37171)
* stream-null?:                          SRFI-41 Stream Primitives.
                                                            (line 36919)
* stream-null? <1>:                      Streams.           (line 41927)
* stream-of:                             SRFI-41 Stream Library.
                                                            (line 37246)
* stream-pair?:                          SRFI-41 Stream Primitives.
                                                            (line 36923)
* stream-range:                          SRFI-41 Stream Library.
                                                            (line 37291)
* stream-ref:                            SRFI-41 Stream Library.
                                                            (line 37309)
* stream-reverse:                        SRFI-41 Stream Library.
                                                            (line 37318)
* stream-scan:                           SRFI-41 Stream Library.
                                                            (line 37325)
* stream-take:                           SRFI-41 Stream Library.
                                                            (line 37337)
* stream-take-while:                     SRFI-41 Stream Library.
                                                            (line 37342)
* stream-unfold:                         SRFI-41 Stream Library.
                                                            (line 37348)
* stream-unfolds:                        SRFI-41 Stream Library.
                                                            (line 37371)
* stream-zip:                            SRFI-41 Stream Library.
                                                            (line 37414)
* stream?:                               SRFI-41 Stream Primitives.
                                                            (line 36912)
* strerror:                              Error Reporting.   (line 19345)
* strftime:                              Time.              (line 30128)
* string:                                String Constructors.
                                                            (line  9286)
* string <1>:                            rnrs base.         (line 38607)
* string->bytevector:                    Representing Strings as Bytes.
                                                            (line 10203)
* string->bytevector <1>:                R6RS Transcoders.  (line 21018)
* string->char-set:                      Creating Character Sets.
                                                            (line  8797)
* string->char-set!:                     Creating Character Sets.
                                                            (line  8803)
* string->date:                          SRFI-19 String to date.
                                                            (line 36232)
* string->header:                        HTTP.              (line 32271)
* string->keyword:                       SRFI-88.           (line 38198)
* string->list:                          List/String Conversion.
                                                            (line  9347)
* string->list <1>:                      rnrs base.         (line 38612)
* string->number:                        Conversion.        (line  7792)
* string->number <1>:                    rnrs base.         (line 38604)
* string->pointer:                       Void Pointers and Byte Access.
                                                            (line 25303)
* string->symbol:                        Symbol Primitives. (line 11152)
* string->symbol <1>:                    rnrs base.         (line 38415)
* string->uri:                           URIs.              (line 32185)
* string->utf16:                         Bytevectors as Strings.
                                                            (line 10836)
* string->utf32:                         Bytevectors as Strings.
                                                            (line 10837)
* string->utf8:                          Bytevectors as Strings.
                                                            (line 10835)
* string->wrapped-lines:                 texinfo string-utils.
                                                            (line 43978)
* string-any:                            String Predicates. (line  9244)
* string-append:                         Reversing and Appending Strings.
                                                            (line  9990)
* string-append <1>:                     rnrs base.         (line 38628)
* string-append/shared:                  Reversing and Appending Strings.
                                                            (line  9999)
* string-bytes-per-char:                 String Internals.  (line 10451)
* string-capitalize:                     Alphabetic Case Mapping.
                                                            (line  9954)
* string-capitalize!:                    Alphabetic Case Mapping.
                                                            (line  9959)
* string-ci->symbol:                     Symbol Primitives. (line 11160)
* string-ci-hash:                        SRFI-69 Hash table algorithms.
                                                            (line 38152)
* string-ci-hash <1>:                    rnrs hashtables.   (line 40095)
* string-ci<:                            String Comparison. (line  9677)
* string-ci<=:                           String Comparison. (line  9687)
* string-ci<=?:                          String Comparison. (line  9605)
* string-ci<=? <1>:                      rnrs unicode.      (line 38813)
* string-ci<>:                           String Comparison. (line  9672)
* string-ci<?:                           String Comparison. (line  9600)
* string-ci<? <1>:                       rnrs unicode.      (line 38811)
* string-ci=:                            String Comparison. (line  9667)
* string-ci=?:                           String Comparison. (line  9595)
* string-ci=? <1>:                       rnrs unicode.      (line 38810)
* string-ci>:                            String Comparison. (line  9682)
* string-ci>=:                           String Comparison. (line  9692)
* string-ci>=?:                          String Comparison. (line  9616)
* string-ci>=? <1>:                      rnrs unicode.      (line 38814)
* string-ci>?:                           String Comparison. (line  9611)
* string-ci>? <1>:                       rnrs unicode.      (line 38812)
* string-compare:                        String Comparison. (line  9622)
* string-compare-ci:                     String Comparison. (line  9632)
* string-concatenate:                    Reversing and Appending Strings.
                                                            (line 10004)
* string-concatenate-reverse:            Reversing and Appending Strings.
                                                            (line 10009)
* string-concatenate-reverse/shared:     Reversing and Appending Strings.
                                                            (line 10027)
* string-concatenate/shared:             Reversing and Appending Strings.
                                                            (line 10022)
* string-contains:                       String Searching.  (line  9893)
* string-contains-ci:                    String Searching.  (line  9900)
* string-copy:                           String Selection.  (line  9401)
* string-copy <1>:                       rnrs base.         (line 38617)
* string-copy!:                          String Modification.
                                                            (line  9540)
* string-count:                          String Searching.  (line  9883)
* string-delete:                         Miscellaneous String Operations.
                                                            (line 10161)
* string-downcase:                       Alphabetic Case Mapping.
                                                            (line  9937)
* string-downcase <1>:                   rnrs unicode.      (line 38804)
* string-downcase!:                      Alphabetic Case Mapping.
                                                            (line  9942)
* string-drop:                           String Selection.  (line  9449)
* string-drop-right:                     String Selection.  (line  9457)
* string-every:                          String Predicates. (line  9261)
* string-fill!:                          String Modification.
                                                            (line  9519)
* string-filter:                         Miscellaneous String Operations.
                                                            (line 10152)
* string-fold:                           Mapping Folding and Unfolding.
                                                            (line 10071)
* string-fold-right:                     Mapping Folding and Unfolding.
                                                            (line 10077)
* string-foldcase:                       rnrs unicode.      (line 38806)
* string-for-each:                       Mapping Folding and Unfolding.
                                                            (line 10050)
* string-for-each <1>:                   rnrs base.         (line 38631)
* string-for-each-index:                 Mapping Folding and Unfolding.
                                                            (line 10055)
* string-hash:                           String Comparison. (line  9697)
* string-hash <1>:                       SRFI-69 Hash table algorithms.
                                                            (line 38151)
* string-hash <2>:                       rnrs hashtables.   (line 40090)
* string-hash-ci:                        String Comparison. (line  9704)
* string-index:                          String Searching.  (line  9772)
* string-index-right:                    String Searching.  (line  9846)
* string-join:                           String Constructors.
                                                            (line  9322)
* string-length:                         String Selection.  (line  9385)
* string-length <1>:                     rnrs base.         (line 38615)
* string-locale-ci<?:                    Text Collation.    (line 27287)
* string-locale-ci=?:                    Text Collation.    (line 27297)
* string-locale-ci>?:                    Text Collation.    (line 27289)
* string-locale-downcase:                Character Case Mapping.
                                                            (line 27357)
* string-locale-titlecase:               Character Case Mapping.
                                                            (line 27362)
* string-locale-upcase:                  Character Case Mapping.
                                                            (line 27352)
* string-locale<?:                       Text Collation.    (line 27283)
* string-locale>?:                       Text Collation.    (line 27285)
* string-map:                            Mapping Folding and Unfolding.
                                                            (line 10037)
* string-map!:                           Mapping Folding and Unfolding.
                                                            (line 10043)
* string-match:                          Regexp Functions.  (line 21875)
* string-normalize-nfc:                  String Comparison. (line  9761)
* string-normalize-nfc <1>:              rnrs unicode.      (line 38820)
* string-normalize-nfd:                  String Comparison. (line  9753)
* string-normalize-nfd <1>:              rnrs unicode.      (line 38818)
* string-normalize-nfkc:                 String Comparison. (line  9765)
* string-normalize-nfkc <1>:             rnrs unicode.      (line 38821)
* string-normalize-nfkd:                 String Comparison. (line  9757)
* string-normalize-nfkd <1>:             rnrs unicode.      (line 38819)
* string-null?:                          String Predicates. (line  9237)
* string-pad:                            String Selection.  (line  9461)
* string-pad-right:                      String Selection.  (line  9462)
* string-prefix-ci?:                     String Searching.  (line  9829)
* string-prefix-length:                  String Searching.  (line  9798)
* string-prefix-length-ci:               String Searching.  (line  9804)
* string-prefix?:                        String Searching.  (line  9824)
* string-ref:                            String Selection.  (line  9392)
* string-ref <1>:                        rnrs base.         (line 38616)
* string-replace:                        Miscellaneous String Operations.
                                                            (line 10138)
* string-reverse:                        Reversing and Appending Strings.
                                                            (line  9979)
* string-reverse!:                       Reversing and Appending Strings.
                                                            (line  9984)
* string-rindex:                         String Searching.  (line  9785)
* string-set!:                           String Modification.
                                                            (line  9511)
* string-skip:                           String Searching.  (line  9859)
* string-skip-right:                     String Searching.  (line  9871)
* string-split:                          List/String Conversion.
                                                            (line  9352)
* string-suffix-ci?:                     String Searching.  (line  9840)
* string-suffix-length:                  String Searching.  (line  9811)
* string-suffix-length-ci:               String Searching.  (line  9817)
* string-suffix?:                        String Searching.  (line  9835)
* string-tabulate:                       String Constructors.
                                                            (line  9315)
* string-take:                           String Selection.  (line  9445)
* string-take-right:                     String Selection.  (line  9453)
* string-titlecase:                      Alphabetic Case Mapping.
                                                            (line  9968)
* string-titlecase <1>:                  rnrs unicode.      (line 38805)
* string-titlecase!:                     Alphabetic Case Mapping.
                                                            (line  9972)
* string-tokenize:                       Miscellaneous String Operations.
                                                            (line 10144)
* string-trim:                           String Selection.  (line  9478)
* string-trim-both:                      String Selection.  (line  9480)
* string-trim-right:                     String Selection.  (line  9479)
* string-unfold:                         Mapping Folding and Unfolding.
                                                            (line 10083)
* string-unfold-right:                   Mapping Folding and Unfolding.
                                                            (line 10098)
* string-upcase:                         Alphabetic Case Mapping.
                                                            (line  9922)
* string-upcase <1>:                     rnrs unicode.      (line 38803)
* string-upcase!:                        Alphabetic Case Mapping.
                                                            (line  9927)
* string-xcopy!:                         Miscellaneous String Operations.
                                                            (line 10129)
* string<:                               String Comparison. (line  9650)
* string<=:                              String Comparison. (line  9659)
* string<=?:                             String Comparison. (line  9580)
* string<=? <1>:                         rnrs base.         (line 38624)
* string<>:                              String Comparison. (line  9646)
* string<?:                              String Comparison. (line  9575)
* string<? <1>:                          rnrs base.         (line 38622)
* string=:                               String Comparison. (line  9642)
* string=?:                              String Comparison. (line  9566)
* string=? <1>:                          rnrs base.         (line 38621)
* string>:                               String Comparison. (line  9655)
* string>=:                              String Comparison. (line  9663)
* string>=?:                             String Comparison. (line  9590)
* string>=? <1>:                         rnrs base.         (line 38625)
* string>?:                              String Comparison. (line  9585)
* string>? <1>:                          rnrs base.         (line 38623)
* string?:                               String Predicates. (line  9230)
* string? <1>:                           rnrs base.         (line 38469)
* strptime:                              Time.              (line 30143)
* strtod:                                Number Input and Output.
                                                            (line 27376)
* strtod <1>:                            Number Input and Output.
                                                            (line 27389)
* struct-ref:                            Structure Basics.  (line 13994)
* struct-ref <1>:                        Inlined Scheme Instructions.
                                                            (line 48482)
* struct-set:                            Inlined Scheme Instructions.
                                                            (line 48483)
* struct-set!:                           Structure Basics.  (line 14002)
* struct-vtable:                         Structure Basics.  (line 14010)
* struct-vtable <1>:                     Inlined Scheme Instructions.
                                                            (line 48484)
* struct-vtable-name:                    Vtable Contents.   (line 14058)
* struct-vtable?:                        Meta-Vtables.      (line 14117)
* struct?:                               Structure Basics.  (line 13990)
* struct? <1>:                           Inlined Scheme Instructions.
                                                            (line 48481)
* sub:                                   Inlined Mathematical Instructions.
                                                            (line 48508)
* sub1:                                  Inlined Mathematical Instructions.
                                                            (line 48509)
* subr-call:                             Trampoline Instructions.
                                                            (line 48135)
* substring:                             String Selection.  (line  9409)
* substring <1>:                         rnrs base.         (line 38618)
* substring-fill!:                       String Modification.
                                                            (line  9525)
* substring-move!:                       String Modification.
                                                            (line  9534)
* substring/copy:                        String Selection.  (line  9427)
* substring/read-only:                   String Selection.  (line  9432)
* substring/shared:                      String Selection.  (line  9421)
* subtract-duration:                     SRFI-19 Time.      (line 36027)
* subtract-duration!:                    SRFI-19 Time.      (line 36028)
* supports-source-properties?:           Source Properties. (line 27924)
* sxml->string:                          Reading and Writing XML.
                                                            (line 42965)
* sxml->xml:                             Reading and Writing XML.
                                                            (line 42960)
* sxml-match:                            sxml-match.        (line 42216)
* sxml-match-let:                        sxml-match.        (line 42491)
* sxml-match-let*:                       sxml-match.        (line 42493)
* sxpath:                                SXPath.            (line 43510)
* symbol:                                Symbol Primitives. (line 11133)
* symbol->keyword:                       Keyword Procedures.
                                                            (line 11644)
* symbol->string:                        Symbol Primitives. (line 11107)
* symbol->string <1>:                    rnrs base.         (line 38414)
* symbol-append:                         Symbol Primitives. (line 11144)
* symbol-fref:                           Symbol Props.      (line 11285)
* symbol-fset!:                          Symbol Props.      (line 11289)
* symbol-hash:                           Symbol Keys.       (line 11061)
* symbol-hash <1>:                       rnrs hashtables.   (line 40091)
* symbol-interned?:                      Symbol Uninterned. (line 11429)
* symbol-pref:                           Symbol Props.      (line 11293)
* symbol-prefix-proc:                    Using Guile Modules.
                                                            (line 23920)
* symbol-property:                       Symbol Props.      (line 11301)
* symbol-property-remove!:               Symbol Props.      (line 11313)
* symbol-pset!:                          Symbol Props.      (line 11297)
* symbol=?:                              rnrs base.         (line 38524)
* symbol?:                               Symbol Primitives. (line 11095)
* symbol? <1>:                           rnrs base.         (line 38413)
* symlink:                               File System.       (line 29747)
* sync:                                  File System.       (line 29803)
* sync-q!:                               Queues.            (line 41857)
* syntax:                                Syntax Case.       (line 16535)
* syntax <1>:                            rnrs syntax-case.  (line 39937)
* syntax->datum:                         Syntax Case.       (line 16660)
* syntax->datum <1>:                     rnrs syntax-case.  (line 39962)
* syntax-case:                           Syntax Case.       (line 16481)
* syntax-case <1>:                       rnrs syntax-case.  (line 39934)
* syntax-error:                          Syntax Rules.      (line 16410)
* syntax-local-binding:                  Syntax Transformer Helpers.
                                                            (line 16821)
* syntax-locally-bound-identifiers:      Syntax Transformer Helpers.
                                                            (line 16882)
* syntax-module:                         Syntax Transformer Helpers.
                                                            (line 16817)
* syntax-parameterize:                   Syntax Parameters. (line 17090)
* syntax-rules:                          Syntax Rules.      (line 16201)
* syntax-rules <1>:                      rnrs base.         (line 38487)
* syntax-source:                         Syntax Transformer Helpers.
                                                            (line 16803)
* syntax-violation:                      rnrs syntax-case.  (line 39968)
* syntax-violation <1>:                  rnrs syntax-case.  (line 39969)
* syntax-violation-form:                 rnrs conditions.   (line 39394)
* syntax-violation-subform:              rnrs conditions.   (line 39395)
* syntax-violation?:                     rnrs conditions.   (line 39393)
* system:                                Processes.         (line 30472)
* system*:                               Processes.         (line 30482)
* system-async-mark:                     System asyncs.     (line 25693)
* system-error-errno:                    Conventions.       (line 29126)
* system-file-name-convention:           File System.       (line 29891)
* tail-apply:                            Procedure Call and Return Instructions.
                                                            (line 47923)
* tail-call:                             Procedure Call and Return Instructions.
                                                            (line 47913)
* tail-call/cc:                          Procedure Call and Return Instructions.
                                                            (line 47991)
* tail-call/nargs:                       Procedure Call and Return Instructions.
                                                            (line 47930)
* take:                                  SRFI-1 Selectors.  (line 34146)
* take!:                                 SRFI-1 Selectors.  (line 34147)
* take-after:                            SXPath.            (line 43477)
* take-right:                            SRFI-1 Selectors.  (line 34156)
* take-until:                            SXPath.            (line 43475)
* take-while:                            SRFI-1 Searching.  (line 34499)
* take-while!:                           SRFI-1 Searching.  (line 34500)
* tan:                                   Scientific.        (line  8118)
* tan <1>:                               rnrs base.         (line 38546)
* tanh:                                  Scientific.        (line  8147)
* tcgetpgrp:                             Terminals and Ptys.
                                                            (line 30863)
* tcsetpgrp:                             Terminals and Ptys.
                                                            (line 30876)
* tenth:                                 SRFI-1 Selectors.  (line 34140)
* terminated-thread-exception?:          SRFI-18 Exceptions.
                                                            (line 35868)
* texi->stexi:                           texinfo.           (line 43670)
* texi-command-depth:                    texinfo.           (line 43653)
* texi-fragment->stexi:                  texinfo.           (line 43665)
* text-content-type?:                    Responses.         (line 33126)
* textdomain:                            Gettext Support.   (line 27658)
* textual-port?:                         R6RS Port Manipulation.
                                                            (line 21073)
* the-environment:                       Local Evaluation.  (line 23197)
* third:                                 SRFI-1 Selectors.  (line 34133)
* thread-cleanup:                        Threads.           (line 25858)
* thread-exited?:                        Threads.           (line 25823)
* thread-join!:                          SRFI-18 Threads.   (line 35700)
* thread-name:                           SRFI-18 Threads.   (line 35658)
* thread-sleep!:                         SRFI-18 Threads.   (line 35678)
* thread-specific:                       SRFI-18 Threads.   (line 35662)
* thread-specific-set!:                  SRFI-18 Threads.   (line 35663)
* thread-start!:                         SRFI-18 Threads.   (line 35668)
* thread-terminate!:                     SRFI-18 Threads.   (line 35684)
* thread-yield!:                         SRFI-18 Threads.   (line 35672)
* thread?:                               Threads.           (line 25807)
* thread? <1>:                           SRFI-18 Threads.   (line 35644)
* throw:                                 Throw.             (line 19246)
* thunk?:                                Procedure Properties.
                                                            (line 15944)
* time:                                  Profile Commands.  (line  3701)
* time->seconds:                         SRFI-18 Time.      (line 35824)
* time-difference:                       SRFI-19 Time.      (line 36017)
* time-difference!:                      SRFI-19 Time.      (line 36018)
* time-monotonic->date:                  SRFI-19 Time/Date conversions.
                                                            (line 36119)
* time-monotonic->time-tai:              SRFI-19 Time/Date conversions.
                                                            (line 36120)
* time-monotonic->time-tai!:             SRFI-19 Time/Date conversions.
                                                            (line 36121)
* time-monotonic->time-utc:              SRFI-19 Time/Date conversions.
                                                            (line 36122)
* time-monotonic->time-utc!:             SRFI-19 Time/Date conversions.
                                                            (line 36123)
* time-nanosecond:                       SRFI-19 Time.      (line 35980)
* time-resolution:                       SRFI-19 Time.      (line 36005)
* time-second:                           SRFI-19 Time.      (line 35981)
* time-tai->date:                        SRFI-19 Time/Date conversions.
                                                            (line 36124)
* time-tai->julian-day:                  SRFI-19 Time/Date conversions.
                                                            (line 36125)
* time-tai->modified-julian-day:         SRFI-19 Time/Date conversions.
                                                            (line 36126)
* time-tai->time-monotonic:              SRFI-19 Time/Date conversions.
                                                            (line 36127)
* time-tai->time-monotonic!:             SRFI-19 Time/Date conversions.
                                                            (line 36128)
* time-tai->time-utc:                    SRFI-19 Time/Date conversions.
                                                            (line 36129)
* time-tai->time-utc!:                   SRFI-19 Time/Date conversions.
                                                            (line 36130)
* time-type:                             SRFI-19 Time.      (line 35979)
* time-utc->date:                        SRFI-19 Time/Date conversions.
                                                            (line 36131)
* time-utc->julian-day:                  SRFI-19 Time/Date conversions.
                                                            (line 36132)
* time-utc->modified-julian-day:         SRFI-19 Time/Date conversions.
                                                            (line 36133)
* time-utc->time-monotonic:              SRFI-19 Time/Date conversions.
                                                            (line 36134)
* time-utc->time-monotonic!:             SRFI-19 Time/Date conversions.
                                                            (line 36135)
* time-utc->time-tai:                    SRFI-19 Time/Date conversions.
                                                            (line 36136)
* time-utc->time-tai!:                   SRFI-19 Time/Date conversions.
                                                            (line 36137)
* time<=?:                               SRFI-19 Time.      (line 36009)
* time<?:                                SRFI-19 Time.      (line 36010)
* time=?:                                SRFI-19 Time.      (line 36011)
* time>=?:                               SRFI-19 Time.      (line 36012)
* time>?:                                SRFI-19 Time.      (line 36013)
* time?:                                 SRFI-18 Time.      (line 35821)
* time? <1>:                             SRFI-19 Time.      (line 35973)
* times:                                 Time.              (line 30157)
* tm:gmtoff:                             Time.              (line 30067)
* tm:hour:                               Time.              (line 30045)
* tm:isdst:                              Time.              (line 30063)
* tm:mday:                               Time.              (line 30048)
* tm:min:                                Time.              (line 30042)
* tm:mon:                                Time.              (line 30051)
* tm:sec:                                Time.              (line 30039)
* tm:wday:                               Time.              (line 30057)
* tm:yday:                               Time.              (line 30060)
* tm:year:                               Time.              (line 30054)
* tm:zone:                               Time.              (line 30076)
* tmpfile:                               File System.       (line 29857)
* tmpnam:                                File System.       (line 29823)
* tms:clock:                             Time.              (line 30163)
* tms:cstime:                            Time.              (line 30175)
* tms:cutime:                            Time.              (line 30171)
* tms:stime:                             Time.              (line 30168)
* tms:utime:                             Time.              (line 30166)
* toplevel-ref:                          Top-Level Environment Instructions.
                                                            (line 47826)
* toplevel-set:                          Top-Level Environment Instructions.
                                                            (line 47854)
* total-processor-count:                 Processes.         (line 30644)
* touch:                                 Futures.           (line 26521)
* trace:                                 Profile Commands.  (line  3707)
* trace-calls-in-procedure:              Tracing Traps.     (line 28713)
* trace-calls-to-procedure:              Tracing Traps.     (line 28709)
* trace-instructions-in-procedure:       Tracing Traps.     (line 28718)
* tracepoint:                            Debug Commands.    (line  3778)
* transcoded-port:                       R6RS Port Manipulation.
                                                            (line 21077)
* transcoder-codec:                      R6RS Transcoders.  (line 21005)
* transcoder-eol-style:                  R6RS Transcoders.  (line 21006)
* transcoder-error-handling-mode:        R6RS Transcoders.  (line 21007)
* transform-string:                      texinfo string-utils.
                                                            (line 43839)
* transpose-array:                       Shared Arrays.     (line 13123)
* trap-at-procedure-call:                Low-Level Traps.   (line 28560)
* trap-at-procedure-ip-in-range:         Low-Level Traps.   (line 28586)
* trap-at-source-location:               Low-Level Traps.   (line 28593)
* trap-calls-in-dynamic-extent:          Low-Level Traps.   (line 28614)
* trap-calls-to-procedure:               Low-Level Traps.   (line 28625)
* trap-enabled?:                         Trap States.       (line 28777)
* trap-frame-finish:                     Low-Level Traps.   (line 28599)
* trap-in-dynamic-extent:                Low-Level Traps.   (line 28606)
* trap-in-procedure:                     Low-Level Traps.   (line 28564)
* trap-instructions-in-dynamic-extent:   Low-Level Traps.   (line 28620)
* trap-instructions-in-procedure:        Low-Level Traps.   (line 28581)
* trap-matching-instructions:            Low-Level Traps.   (line 28634)
* trap-name:                             Trap States.       (line 28773)
* truncate:                              Arithmetic.        (line  7904)
* truncate <1>:                          Random Access.     (line 20106)
* truncate <2>:                          rnrs base.         (line 38641)
* truncate-file:                         Random Access.     (line 20106)
* truncate-quotient:                     Arithmetic.        (line  8000)
* truncate-remainder:                    Arithmetic.        (line  8001)
* truncate-values:                       Procedure Call and Return Instructions.
                                                            (line 47977)
* truncate/:                             Arithmetic.        (line  7999)
* truncated-print:                       Pretty Printing.   (line 40700)
* try-arbiter:                           Arbiters.          (line 25635)
* try-mutex:                             Mutexes and Condition Variables.
                                                            (line 25962)
* ttyname:                               Terminals and Ptys.
                                                            (line 30853)
* typed-array?:                          Array Procedures.  (line 12803)
* tzset:                                 Time.              (line 30121)
* u16vector:                             SRFI-4 API.        (line 35079)
* u16vector->list:                       SRFI-4 API.        (line 35187)
* u16vector-length:                      SRFI-4 API.        (line 35107)
* u16vector-ref:                         SRFI-4 API.        (line 35133)
* u16vector-set!:                        SRFI-4 API.        (line 35160)
* u16vector?:                            SRFI-4 API.        (line 35023)
* u32vector:                             SRFI-4 API.        (line 35081)
* u32vector->list:                       SRFI-4 API.        (line 35189)
* u32vector-length:                      SRFI-4 API.        (line 35109)
* u32vector-ref:                         SRFI-4 API.        (line 35135)
* u32vector-set!:                        SRFI-4 API.        (line 35162)
* u32vector?:                            SRFI-4 API.        (line 35025)
* u64vector:                             SRFI-4 API.        (line 35083)
* u64vector->list:                       SRFI-4 API.        (line 35191)
* u64vector-length:                      SRFI-4 API.        (line 35111)
* u64vector-ref:                         SRFI-4 API.        (line 35137)
* u64vector-set!:                        SRFI-4 API.        (line 35164)
* u64vector?:                            SRFI-4 API.        (line 35027)
* u8-list->bytevector:                   Bytevectors and Integer Lists.
                                                            (line 10755)
* u8vector:                              SRFI-4 API.        (line 35077)
* u8vector->list:                        SRFI-4 API.        (line 35185)
* u8vector-length:                       SRFI-4 API.        (line 35105)
* u8vector-ref:                          SRFI-4 API.        (line 35131)
* u8vector-set!:                         SRFI-4 API.        (line 35158)
* u8vector?:                             SRFI-4 API.        (line 35021)
* ucs-range->char-set:                   Creating Character Sets.
                                                            (line  8820)
* ucs-range->char-set!:                  Creating Character Sets.
                                                            (line  8832)
* uint-list->bytevector:                 Bytevectors and Integer Lists.
                                                            (line 10770)
* umask:                                 Processes.         (line 30304)
* uname:                                 System Identification.
                                                            (line 31902)
* unbox:                                 SRFI-111.          (line 38273)
* uncaught-exception-reason:             SRFI-18 Exceptions.
                                                            (line 35874)
* uncaught-exception?:                   SRFI-18 Exceptions.
                                                            (line 35873)
* undefined-violation?:                  rnrs conditions.   (line 39402)
* unfold:                                SRFI-1 Fold and Map.
                                                            (line 34344)
* unfold-right:                          SRFI-1 Fold and Map.
                                                            (line 34371)
* unget-bytevector:                      R6RS Binary Input. (line 21283)
* uniform-array-read!:                   Array Procedures.  (line 12980)
* uniform-array-write:                   Array Procedures.  (line 12995)
* unless:                                Conditionals.      (line 18259)
* unless <1>:                            rnrs control.      (line 38930)
* unlink:                                File System.       (line 29701)
* unlock-mutex:                          Mutexes and Condition Variables.
                                                            (line 25969)
* unquote:                               Expression Syntax. (line 22365)
* unquote <1>:                           rnrs base.         (line 38508)
* unquote-splicing:                      Expression Syntax. (line 22375)
* unquote-splicing <1>:                  rnrs base.         (line 38509)
* unread-char:                           Reading.           (line 19941)
* unread-char <1>:                       Ports and File Descriptors.
                                                            (line 29309)
* unread-string:                         Reading.           (line 19948)
* unread-string <1>:                     Ports and File Descriptors.
                                                            (line 29316)
* unsetenv:                              Runtime Environment.
                                                            (line 30266)
* unsyntax:                              rnrs syntax-case.  (line 39939)
* unsyntax-splicing:                     rnrs syntax-case.  (line 39940)
* unwind:                                Dynamic Environment Instructions.
                                                            (line 48354)
* unwind-fluids:                         Dynamic Environment Instructions.
                                                            (line 48365)
* unzip1:                                SRFI-1 Length Append etc.
                                                            (line 34215)
* unzip2:                                SRFI-1 Length Append etc.
                                                            (line 34216)
* unzip3:                                SRFI-1 Length Append etc.
                                                            (line 34217)
* unzip4:                                SRFI-1 Length Append etc.
                                                            (line 34218)
* unzip5:                                SRFI-1 Length Append etc.
                                                            (line 34219)
* up:                                    Debug Commands.    (line  3727)
* update-direct-method!:                 Customizing Class Redefinition.
                                                            (line 46482)
* update-direct-subclass!:               Customizing Class Redefinition.
                                                            (line 46486)
* update-instance-for-different-class:   Changing the Class of an Instance.
                                                            (line 46552)
* uri->string:                           URIs.              (line 32189)
* uri-decode:                            URIs.              (line 32197)
* uri-encode:                            URIs.              (line 32220)
* uri-fragment:                          URIs.              (line 32180)
* uri-host:                              URIs.              (line 32176)
* uri-path:                              URIs.              (line 32178)
* uri-port:                              URIs.              (line 32177)
* uri-query:                             URIs.              (line 32179)
* uri-scheme:                            URIs.              (line 32174)
* uri-userinfo:                          URIs.              (line 32175)
* uri?:                                  URIs.              (line 32173)
* urlify:                                texinfo html.      (line 43781)
* use-modules:                           Using Guile Modules.
                                                            (line 23924)
* usleep:                                Signals.           (line 30780)
* utf-16-codec:                          R6RS Transcoders.  (line 20864)
* utf-8-codec:                           R6RS Transcoders.  (line 20863)
* utf16->string:                         Bytevectors as Strings.
                                                            (line 10847)
* utf32->string:                         Bytevectors as Strings.
                                                            (line 10848)
* utf8->string:                          Bytevectors as Strings.
                                                            (line 10846)
* utime:                                 File System.       (line 29685)
* utsname:machine:                       System Identification.
                                                            (line 31920)
* utsname:nodename:                      System Identification.
                                                            (line 31912)
* utsname:release:                       System Identification.
                                                            (line 31914)
* utsname:sysname:                       System Identification.
                                                            (line 31910)
* utsname:version:                       System Identification.
                                                            (line 31917)
* valid-header?:                         HTTP.              (line 32340)
* value-history-enabled?:                Value History.     (line  3572)
* values:                                Multiple Values.   (line 18873)
* values <1>:                            rnrs base.         (line 38751)
* variable-bound?:                       Variables.         (line 24418)
* variable-bound? <1>:                   Top-Level Environment Instructions.
                                                            (line 47881)
* variable-ref:                          Variables.         (line 24423)
* variable-ref <1>:                      Top-Level Environment Instructions.
                                                            (line 47873)
* variable-set:                          Top-Level Environment Instructions.
                                                            (line 47877)
* variable-set!:                         Variables.         (line 24428)
* variable-unset!:                       Variables.         (line 24433)
* variable?:                             Variables.         (line 24437)
* vector:                                Vector Creation.   (line 12304)
* vector <1>:                            SRFI-43 Constructors.
                                                            (line 37447)
* vector <2>:                            rnrs base.         (line 38733)
* vector <3>:                            Data Constructor Instructions.
                                                            (line 48259)
* vector->list:                          Vector Creation.   (line 12314)
* vector->list <1>:                      SRFI-43 Conversion.
                                                            (line 37707)
* vector->list <2>:                      rnrs base.         (line 38738)
* vector->stream:                        Streams.           (line 41931)
* vector-any:                            SRFI-43 Searching. (line 37657)
* vector-append:                         SRFI-43 Constructors.
                                                            (line 37504)
* vector-binary-search:                  SRFI-43 Searching. (line 37632)
* vector-concatenate:                    SRFI-43 Constructors.
                                                            (line 37511)
* vector-copy:                           Vector Accessors.  (line 12398)
* vector-copy <1>:                       SRFI-43 Constructors.
                                                            (line 37476)
* vector-copy!:                          SRFI-43 Mutators.  (line 37688)
* vector-count:                          SRFI-43 Iteration. (line 37580)
* vector-empty?:                         SRFI-43 Predicates.
                                                            (line 37524)
* vector-every:                          SRFI-43 Searching. (line 37663)
* vector-fill!:                          Vector Accessors.  (line 12393)
* vector-fill! <1>:                      SRFI-43 Mutators.  (line 37680)
* vector-fill! <2>:                      rnrs base.         (line 38744)
* vector-fold:                           SRFI-43 Iteration. (line 37548)
* vector-fold-right:                     SRFI-43 Iteration. (line 37558)
* vector-for-each:                       SRFI-43 Iteration. (line 37575)
* vector-for-each <1>:                   rnrs base.         (line 38729)
* vector-index:                          SRFI-43 Searching. (line 37596)
* vector-index-right:                    SRFI-43 Searching. (line 37608)
* vector-length:                         Vector Accessors.  (line 12352)
* vector-length <1>:                     SRFI-43 Selectors. (line 37542)
* vector-length <2>:                     rnrs base.         (line 38741)
* vector-map:                            SRFI-43 Iteration. (line 37562)
* vector-map <1>:                        rnrs base.         (line 38728)
* vector-map!:                           SRFI-43 Iteration. (line 37569)
* vector-move-left!:                     Vector Accessors.  (line 12402)
* vector-move-right!:                    Vector Accessors.  (line 12414)
* vector-ref:                            Vector Accessors.  (line 12359)
* vector-ref <1>:                        SRFI-43 Selectors. (line 37539)
* vector-ref <2>:                        rnrs base.         (line 38742)
* vector-ref <3>:                        Inlined Scheme Instructions.
                                                            (line 48479)
* vector-reverse!:                       SRFI-43 Mutators.  (line 37684)
* vector-reverse-copy:                   SRFI-43 Constructors.
                                                            (line 37497)
* vector-reverse-copy!:                  SRFI-43 Mutators.  (line 37696)
* vector-set:                            Inlined Scheme Instructions.
                                                            (line 48480)
* vector-set!:                           Vector Accessors.  (line 12382)
* vector-set! <1>:                       SRFI-43 Mutators.  (line 37674)
* vector-set! <2>:                       rnrs base.         (line 38743)
* vector-skip:                           SRFI-43 Searching. (line 37616)
* vector-skip-right:                     SRFI-43 Searching. (line 37624)
* vector-sort:                           rnrs sorting.      (line 38902)
* vector-sort!:                          rnrs sorting.      (line 38914)
* vector-swap!:                          SRFI-43 Mutators.  (line 37677)
* vector-unfold:                         SRFI-43 Constructors.
                                                            (line 37452)
* vector-unfold-right:                   SRFI-43 Constructors.
                                                            (line 37468)
* vector=:                               SRFI-43 Predicates.
                                                            (line 37528)
* vector?:                               Vector Creation.   (line 12338)
* vector? <1>:                           SRFI-43 Predicates.
                                                            (line 37521)
* vector? <2>:                           rnrs base.         (line 38734)
* version:                               Build Config.      (line 26652)
* vhash-assoc:                           VHashes.           (line 14757)
* vhash-assq:                            VHashes.           (line 14758)
* vhash-assv:                            VHashes.           (line 14759)
* vhash-cons:                            VHashes.           (line 14743)
* vhash-consq:                           VHashes.           (line 14744)
* vhash-consv:                           VHashes.           (line 14745)
* vhash-delete:                          VHashes.           (line 14771)
* vhash-delq:                            VHashes.           (line 14772)
* vhash-delv:                            VHashes.           (line 14773)
* vhash-fold:                            VHashes.           (line 14783)
* vhash-fold*:                           VHashes.           (line 14790)
* vhash-fold-right:                      VHashes.           (line 14784)
* vhash-foldq*:                          VHashes.           (line 14791)
* vhash-foldv*:                          VHashes.           (line 14792)
* vhash?:                                VHashes.           (line 14740)
* violation?:                            rnrs conditions.   (line 39348)
* vlist->list:                           VLists.            (line 13551)
* vlist-append:                          VLists.            (line 13545)
* vlist-cons:                            VLists.            (line 13485)
* vlist-delete:                          VLists.            (line 13536)
* vlist-drop:                            VLists.            (line 13524)
* vlist-filter:                          VLists.            (line 13532)
* vlist-fold:                            VLists.            (line 13501)
* vlist-fold-right:                      VLists.            (line 13502)
* vlist-for-each:                        VLists.            (line 13521)
* vlist-head:                            VLists.            (line 13488)
* vlist-length:                          VLists.            (line 13510)
* vlist-map:                             VLists.            (line 13518)
* vlist-null?:                           VLists.            (line 13482)
* vlist-ref:                             VLists.            (line 13506)
* vlist-reverse:                         VLists.            (line 13514)
* vlist-tail:                            VLists.            (line 13491)
* vlist-take:                            VLists.            (line 13528)
* vlist-unfold:                          VLists.            (line 13540)
* vlist-unfold-right:                    VLists.            (line 13541)
* vlist?:                                VLists.            (line 13474)
* vm-abort-continuation-hook:            VM Hooks.          (line 28441)
* vm-apply-hook:                         VM Hooks.          (line 28431)
* vm-next-hook:                          VM Hooks.          (line 28413)
* vm-pop-continuation-hook:              VM Hooks.          (line 28422)
* vm-push-continuation-hook:             VM Hooks.          (line 28417)
* vm-restore-continuation-hook:          VM Hooks.          (line 28446)
* vm-trace-level:                        VM Hooks.          (line 28462)
* void:                                  Miscellaneous Instructions.
                                                            (line 48442)
* wait-condition-variable:               Mutexes and Condition Variables.
                                                            (line 26014)
* waitpid:                               Processes.         (line 30415)
* warning?:                              rnrs conditions.   (line 39332)
* weak-key-hash-table?:                  Weak hash tables.  (line 23696)
* weak-value-hash-table?:                Weak hash tables.  (line 23697)
* weak-vector:                           Weak vectors.      (line 23715)
* weak-vector-ref:                       Weak vectors.      (line 23726)
* weak-vector-set!:                      Weak vectors.      (line 23731)
* weak-vector?:                          Weak vectors.      (line 23722)
* when:                                  Conditionals.      (line 18258)
* when <1>:                              rnrs control.      (line 38929)
* while:                                 while do.          (line 18429)
* who-condition?:                        rnrs conditions.   (line 39367)
* width:                                 Debug Commands.    (line  3765)
* wind:                                  Dynamic Environment Instructions.
                                                            (line 48344)
* wind-fluids:                           Dynamic Environment Instructions.
                                                            (line 48359)
* with-code-coverage:                    Code Coverage.     (line 28916)
* with-continuation-barrier:             Continuation Barriers.
                                                            (line 19712)
* with-default-trap-handler:             High-Level Traps.  (line 28812)
* with-dynamic-state:                    Fluids and Dynamic States.
                                                            (line 26299)
* with-ellipsis:                         Syntax Case.       (line 16757)
* with-error-to-file:                    File Ports.        (line 20520)
* with-exception-handler:                SRFI-18 Exceptions.
                                                            (line 35847)
* with-exception-handler <1>:            rnrs exceptions.   (line 39218)
* with-fluid*:                           Fluids and Dynamic States.
                                                            (line 26236)
* with-fluids:                           Fluids and Dynamic States.
                                                            (line 26250)
* with-fluids*:                          Fluids and Dynamic States.
                                                            (line 26241)
* with-input-from-file:                  File Ports.        (line 20516)
* with-input-from-file <1>:              rnrs io simple.    (line 39511)
* with-input-from-string:                String Ports.      (line 20627)
* with-mutex:                            Mutexes and Condition Variables.
                                                            (line 26047)
* with-output-to-file:                   File Ports.        (line 20518)
* with-output-to-file <1>:               rnrs io simple.    (line 39512)
* with-output-to-string:                 String Ports.      (line 20619)
* with-parameters*:                      SRFI-39.           (line 36848)
* with-readline-completion-function:     Readline Functions.
                                                            (line 40591)
* with-ssax-error-to-port:               SSAX.              (line 43119)
* with-statprof:                         Statprof.          (line 42762)
* with-syntax:                           Syntax Case.       (line 16707)
* with-throw-handler:                    Throw Handlers.    (line 19148)
* write:                                 Scheme Write.      (line 22562)
* write <1>:                             rnrs io simple.    (line 39537)
* write <2>:                             rnrs io simple.    (line 39538)
* write <3>:                             GOOPS Object Miscellany.
                                                            (line 45593)
* write-char:                            Writing.           (line 20025)
* write-char <1>:                        rnrs io simple.    (line 39539)
* write-char <2>:                        rnrs io simple.    (line 39540)
* write-client:                          Web Server.        (line 33341)
* write-header:                          HTTP.              (line 32359)
* write-headers:                         HTTP.              (line 32367)
* write-line:                            Line/Delimited.    (line 20181)
* write-objcode:                         Bytecode and Objcode.
                                                            (line 49269)
* write-request:                         Requests.          (line 32943)
* write-request-body:                    Requests.          (line 32953)
* write-request-line:                    HTTP.              (line 32391)
* write-response:                        Responses.         (line 33059)
* write-response-body:                   Responses.         (line 33087)
* write-response-line:                   HTTP.              (line 32399)
* write-string/partial:                  Block Reading and Writing.
                                                            (line 20282)
* write-with-shared-structure:           SRFI-38.           (line 36769)
* write-with-shared-structure <1>:       SRFI-38.           (line 36770)
* write-with-shared-structure <2>:       SRFI-38.           (line 36771)
* xcons:                                 SRFI-1 Constructors.
                                                            (line 34033)
* xml->sxml:                             Reading and Writing XML.
                                                            (line 42836)
* xml-token-head:                        SSAX.              (line 43129)
* xml-token-kind:                        SSAX.              (line 43127)
* xml-token?:                            SSAX.              (line 43121)
* xsubstring:                            Miscellaneous String Operations.
                                                            (line 10117)
* yield:                                 Threads.           (line 25827)
* zero?:                                 Comparison.        (line  7767)
* zero? <1>:                             rnrs base.         (line 38582)
* zip:                                   SRFI-1 Length Append etc.
                                                            (line 34209)

