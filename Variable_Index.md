Variable Index
**************

This is an alphabetical list of all the important variables and
constants in Guile.

   When looking for a particular variable or constant, please look under
its Scheme name as well as under its C name.  The C name can be
constructed from the Scheme names by a simple transformation described
in the section *Note API Overview::.

* Menu:

* %auto-compilation-options:             Compilation.       (line 22868)
* %default-port-encoding:                Ports.             (line 19820)
* %global-locale:                        i18n Introduction. (line 27270)
* %guile-build-info:                     Build Config.      (line 26704)
* %host-type:                            Build Config.      (line 26734)
* %load-compiled-path:                   Load Paths.        (line 23032)
* %load-extensions:                      Load Paths.        (line 23020)
* %load-hook:                            Loading.           (line 22934)
* %load-path:                            Load Paths.        (line 22960)
* %null-pointer:                         Foreign Variables. (line 25232)
* &condition:                            SRFI-35.           (line 36641)
* &error:                                SRFI-35.           (line 36662)
* &message:                              SRFI-35.           (line 36645)
* &serious:                              SRFI-35.           (line 36655)
* *features*:                            Feature Tracking.  (line 26747)
* *random-state*:                        Random.            (line  8391)
* *sdocbook->stexi-rules*:               texinfo docbook.   (line 43698)
* *sdocbook-block-commands*:             texinfo docbook.   (line 43700)
* <standard-vtable>:                     Meta-Vtables.      (line 14102)
* _IOFBF:                                Ports and File Descriptors.
                                                            (line 29436)
* _IOLBF:                                Ports and File Descriptors.
                                                            (line 29434)
* _IONBF:                                Ports and File Descriptors.
                                                            (line 29432)
* accept:                                HTTP Headers.      (line 32617)
* accept-charset:                        HTTP Headers.      (line 32626)
* accept-encoding:                       HTTP Headers.      (line 32632)
* accept-language:                       HTTP Headers.      (line 32637)
* accept-ranges:                         HTTP Headers.      (line 32751)
* after-gc-hook:                         GC Hooks.          (line 17860)
* age:                                   HTTP Headers.      (line 32756)
* allow:                                 HTTP Headers.      (line 32548)
* authorization:                         HTTP Headers.      (line 32642)
* block-growth-factor:                   VLists.            (line 13494)
* cache-control:                         HTTP Headers.      (line 32471)
* char-set:ascii:                        Standard Character Sets.
                                                            (line  9067)
* char-set:blank:                        Standard Character Sets.
                                                            (line  9043)
* char-set:designated:                   Standard Character Sets.
                                                            (line  9075)
* char-set:digit:                        Standard Character Sets.
                                                            (line  9023)
* char-set:empty:                        Standard Character Sets.
                                                            (line  9071)
* char-set:full:                         Standard Character Sets.
                                                            (line  9081)
* char-set:graphic:                      Standard Character Sets.
                                                            (line  9031)
* char-set:hex-digit:                    Standard Character Sets.
                                                            (line  9063)
* char-set:iso-control:                  Standard Character Sets.
                                                            (line  9048)
* char-set:letter:                       Standard Character Sets.
                                                            (line  9016)
* char-set:letter+digit:                 Standard Character Sets.
                                                            (line  9027)
* char-set:lower-case:                   Standard Character Sets.
                                                            (line  9003)
* char-set:printing:                     Standard Character Sets.
                                                            (line  9035)
* char-set:punctuation:                  Standard Character Sets.
                                                            (line  9054)
* char-set:symbol:                       Standard Character Sets.
                                                            (line  9059)
* char-set:title-case:                   Standard Character Sets.
                                                            (line  9011)
* char-set:upper-case:                   Standard Character Sets.
                                                            (line  9007)
* char-set:whitespace:                   Standard Character Sets.
                                                            (line  9039)
* connection:                            HTTP Headers.      (line 32488)
* content-encoding:                      HTTP Headers.      (line 32553)
* content-language:                      HTTP Headers.      (line 32558)
* content-length:                        HTTP Headers.      (line 32563)
* content-location:                      HTTP Headers.      (line 32569)
* content-md5:                           HTTP Headers.      (line 32575)
* content-range:                         HTTP Headers.      (line 32580)
* content-type:                          HTTP Headers.      (line 32589)
* current-reader:                        Loading.           (line 22914)
* date:                                  HTTP Headers.      (line 32496)
* double:                                Foreign Types.     (line 25161)
* etag:                                  HTTP Headers.      (line 32761)
* expect:                                HTTP Headers.      (line 32651)
* expires:                               HTTP Headers.      (line 32600)
* FD_CLOEXEC:                            Ports and File Descriptors.
                                                            (line 29460)
* file-name-separator-string:            File System.       (line 29903)
* float:                                 Foreign Types.     (line 25160)
* from:                                  HTTP Headers.      (line 32657)
* F_DUPFD:                               Ports and File Descriptors.
                                                            (line 29451)
* F_GETFD:                               Ports and File Descriptors.
                                                            (line 29455)
* F_GETFL:                               Ports and File Descriptors.
                                                            (line 29473)
* F_GETOWN:                              Ports and File Descriptors.
                                                            (line 29484)
* F_OK:                                  File System.       (line 29565)
* F_SETFD:                               Ports and File Descriptors.
                                                            (line 29456)
* F_SETFL:                               Ports and File Descriptors.
                                                            (line 29474)
* F_SETOWN:                              Ports and File Descriptors.
                                                            (line 29485)
* GUILE_AUTO_COMPILE:                    Environment Variables.
                                                            (line  3050)
* GUILE_HISTORY:                         Environment Variables.
                                                            (line  3078)
* GUILE_INSTALL_LOCALE:                  Environment Variables.
                                                            (line  3084)
* GUILE_LOAD_COMPILED_PATH:              Environment Variables.
                                                            (line  3110)
* GUILE_LOAD_PATH:                       Environment Variables.
                                                            (line  3127)
* GUILE_STACK_SIZE:                      Environment Variables.
                                                            (line  3099)
* GUILE_WARN_DEPRECATED:                 Environment Variables.
                                                            (line  3150)
* HOME:                                  Environment Variables.
                                                            (line  3160)
* host:                                  HTTP Headers.      (line 32662)
* if-match:                              HTTP Headers.      (line 32670)
* if-modified-since:                     HTTP Headers.      (line 32681)
* if-none-match:                         HTTP Headers.      (line 32687)
* if-range:                              HTTP Headers.      (line 32694)
* if-unmodified-since:                   HTTP Headers.      (line 32701)
* INADDR_ANY:                            Network Address Conversion.
                                                            (line 30995)
* INADDR_BROADCAST:                      Network Address Conversion.
                                                            (line 31000)
* INADDR_LOOPBACK:                       Network Address Conversion.
                                                            (line 31003)
* int:                                   Foreign Types.     (line 25168)
* int16:                                 Foreign Types.     (line 25155)
* int32:                                 Foreign Types.     (line 25157)
* int64:                                 Foreign Types.     (line 25159)
* int8:                                  Foreign Types.     (line 25152)
* internal-time-units-per-second:        Time.              (line 30153)
* IPPROTO_IP:                            Network Sockets and Communication.
                                                            (line 31616)
* IPPROTO_TCP:                           Network Sockets and Communication.
                                                            (line 31617)
* IPPROTO_UDP:                           Network Sockets and Communication.
                                                            (line 31618)
* IP_ADD_MEMBERSHIP:                     Network Sockets and Communication.
                                                            (line 31660)
* IP_DROP_MEMBERSHIP:                    Network Sockets and Communication.
                                                            (line 31661)
* IP_MULTICAST_IF:                       Network Sockets and Communication.
                                                            (line 31652)
* IP_MULTICAST_TTL:                      Network Sockets and Communication.
                                                            (line 31655)
* ITIMER_PROF:                           Signals.           (line 30818)
* ITIMER_REAL:                           Signals.           (line 30809)
* ITIMER_VIRTUAL:                        Signals.           (line 30814)
* last-modified:                         HTTP Headers.      (line 32606)
* LC_ALL:                                Locales.           (line 31946)
* LC_COLLATE:                            Locales.           (line 31947)
* LC_CTYPE:                              Locales.           (line 31948)
* LC_MESSAGES:                           Locales.           (line 31949)
* LC_MONETARY:                           Locales.           (line 31950)
* LC_NUMERIC:                            Locales.           (line 31951)
* LC_TIME:                               Locales.           (line 31952)
* location:                              HTTP Headers.      (line 32766)
* LOCK_EX:                               Ports and File Descriptors.
                                                            (line 29497)
* LOCK_NB:                               Ports and File Descriptors.
                                                            (line 29502)
* LOCK_SH:                               Ports and File Descriptors.
                                                            (line 29494)
* LOCK_UN:                               Ports and File Descriptors.
                                                            (line 29500)
* long:                                  Foreign Types.     (line 25170)
* max-forwards:                          HTTP Headers.      (line 32707)
* MSG_DONTROUTE:                         Network Sockets and Communication.
                                                            (line 31774)
* MSG_DONTROUTE <1>:                     Network Sockets and Communication.
                                                            (line 31784)
* MSG_DONTROUTE <2>:                     Network Sockets and Communication.
                                                            (line 31811)
* MSG_OOB:                               Network Sockets and Communication.
                                                            (line 31774)
* MSG_OOB <1>:                           Network Sockets and Communication.
                                                            (line 31784)
* MSG_OOB <2>:                           Network Sockets and Communication.
                                                            (line 31811)
* MSG_PEEK:                              Network Sockets and Communication.
                                                            (line 31774)
* MSG_PEEK <1>:                          Network Sockets and Communication.
                                                            (line 31784)
* MSG_PEEK <2>:                          Network Sockets and Communication.
                                                            (line 31811)
* OPEN_BOTH:                             Pipes.             (line 30906)
* OPEN_READ:                             Pipes.             (line 30904)
* OPEN_WRITE:                            Pipes.             (line 30905)
* O_APPEND:                              Ports and File Descriptors.
                                                            (line 29283)
* O_CREAT:                               Ports and File Descriptors.
                                                            (line 29285)
* O_RDONLY:                              Ports and File Descriptors.
                                                            (line 29277)
* O_RDWR:                                Ports and File Descriptors.
                                                            (line 29281)
* O_WRONLY:                              Ports and File Descriptors.
                                                            (line 29279)
* PF_INET:                               Network Sockets and Communication.
                                                            (line 31572)
* PF_INET6:                              Network Sockets and Communication.
                                                            (line 31573)
* PF_UNIX:                               Network Sockets and Communication.
                                                            (line 31571)
* PIPE_BUF:                              Ports and File Descriptors.
                                                            (line 29332)
* pragma:                                HTTP Headers.      (line 32501)
* PRIO_PGRP:                             Processes.         (line 30601)
* PRIO_PGRP <1>:                         Processes.         (line 30615)
* PRIO_PROCESS:                          Processes.         (line 30601)
* PRIO_PROCESS <1>:                      Processes.         (line 30615)
* PRIO_USER:                             Processes.         (line 30601)
* PRIO_USER <1>:                         Processes.         (line 30615)
* proxy-authenticate:                    HTTP Headers.      (line 32772)
* proxy-authorization:                   HTTP Headers.      (line 32713)
* ptrdiff_t:                             Foreign Types.     (line 25174)
* range:                                 HTTP Headers.      (line 32720)
* referer:                               HTTP Headers.      (line 32729)
* regexp/basic:                          Regexp Functions.  (line 21925)
* regexp/extended:                       Regexp Functions.  (line 21934)
* regexp/icase:                          Regexp Functions.  (line 21912)
* regexp/newline:                        Regexp Functions.  (line 21916)
* regexp/notbol:                         Regexp Functions.  (line 21952)
* regexp/noteol:                         Regexp Functions.  (line 21959)
* retry-after:                           HTTP Headers.      (line 32778)
* R_OK:                                  File System.       (line 29559)
* SA_NOCLDSTOP:                          Signals.           (line 30736)
* SA_RESTART:                            Signals.           (line 30744)
* scm_after_gc_c_hook:                   GC Hooks.          (line 17856)
* scm_after_gc_hook:                     GC Hooks.          (line 17861)
* scm_after_sweep_c_hook:                GC Hooks.          (line 17851)
* scm_before_gc_c_hook:                  GC Hooks.          (line 17833)
* scm_before_mark_c_hook:                GC Hooks.          (line 17842)
* scm_before_sweep_c_hook:               GC Hooks.          (line 17846)
* SCM_BOOL_F:                            Booleans.          (line  7030)
* SCM_BOOL_T:                            Booleans.          (line  7027)
* scm_char_set_ascii:                    Standard Character Sets.
                                                            (line  9068)
* scm_char_set_blank:                    Standard Character Sets.
                                                            (line  9044)
* scm_char_set_designated:               Standard Character Sets.
                                                            (line  9076)
* scm_char_set_digit:                    Standard Character Sets.
                                                            (line  9024)
* scm_char_set_empty:                    Standard Character Sets.
                                                            (line  9072)
* scm_char_set_full:                     Standard Character Sets.
                                                            (line  9082)
* scm_char_set_graphic:                  Standard Character Sets.
                                                            (line  9032)
* scm_char_set_hex_digit:                Standard Character Sets.
                                                            (line  9064)
* scm_char_set_iso_control:              Standard Character Sets.
                                                            (line  9049)
* scm_char_set_letter:                   Standard Character Sets.
                                                            (line  9017)
* scm_char_set_letter_and_digit:         Standard Character Sets.
                                                            (line  9028)
* scm_char_set_lower_case:               Standard Character Sets.
                                                            (line  9004)
* scm_char_set_printing:                 Standard Character Sets.
                                                            (line  9036)
* scm_char_set_punctuation:              Standard Character Sets.
                                                            (line  9055)
* scm_char_set_symbol:                   Standard Character Sets.
                                                            (line  9060)
* scm_char_set_title_case:               Standard Character Sets.
                                                            (line  9012)
* scm_char_set_upper_case:               Standard Character Sets.
                                                            (line  9008)
* scm_char_set_whitespace:               Standard Character Sets.
                                                            (line  9040)
* SCM_C_HOOK_AND:                        C Hooks.           (line 17769)
* SCM_C_HOOK_NORMAL:                     C Hooks.           (line 17762)
* SCM_C_HOOK_OR:                         C Hooks.           (line 17765)
* scm_endianness_big:                    Bytevector Endianness.
                                                            (line 10541)
* scm_endianness_little:                 Bytevector Endianness.
                                                            (line 10542)
* SCM_F_WIND_EXPLICITLY:                 Dynamic Wind.      (line 19518)
* scm_global_locale:                     i18n Introduction. (line 27271)
* scm_ptobs:                             C Port Interface.  (line 21555)
* scm_t_int16:                           Integers.          (line  7226)
* scm_t_int32:                           Integers.          (line  7228)
* scm_t_int64:                           Integers.          (line  7230)
* scm_t_int8:                            Integers.          (line  7224)
* scm_t_intmax:                          Integers.          (line  7232)
* scm_t_uint16:                          Integers.          (line  7227)
* scm_t_uint32:                          Integers.          (line  7229)
* scm_t_uint64:                          Integers.          (line  7231)
* scm_t_uint8:                           Integers.          (line  7225)
* scm_t_uintmax:                         Integers.          (line  7233)
* scm_vtable_index_layout:               Vtable Contents.   (line 14033)
* scm_vtable_index_printer:              Vtable Contents.   (line 14046)
* SEEK_CUR:                              Random Access.     (line 20088)
* SEEK_END:                              Random Access.     (line 20090)
* SEEK_SET:                              Random Access.     (line 20086)
* server:                                HTTP Headers.      (line 32785)
* SIGHUP:                                Signals.           (line 30694)
* SIGINT:                                Signals.           (line 30697)
* size_t:                                Foreign Types.     (line 25172)
* SOCK_DGRAM:                            Network Sockets and Communication.
                                                            (line 31579)
* SOCK_RAW:                              Network Sockets and Communication.
                                                            (line 31580)
* SOCK_RDM:                              Network Sockets and Communication.
                                                            (line 31581)
* SOCK_SEQPACKET:                        Network Sockets and Communication.
                                                            (line 31582)
* SOCK_STREAM:                           Network Sockets and Communication.
                                                            (line 31578)
* SOL_SOCKET:                            Network Sockets and Communication.
                                                            (line 31615)
* SO_BROADCAST:                          Network Sockets and Communication.
                                                            (line 31633)
* SO_DEBUG:                              Network Sockets and Communication.
                                                            (line 31627)
* SO_DONTROUTE:                          Network Sockets and Communication.
                                                            (line 31632)
* SO_ERROR:                              Network Sockets and Communication.
                                                            (line 31631)
* SO_KEEPALIVE:                          Network Sockets and Communication.
                                                            (line 31636)
* SO_LINGER:                             Network Sockets and Communication.
                                                            (line 31643)
* SO_NO_CHECK:                           Network Sockets and Communication.
                                                            (line 31638)
* SO_OOBINLINE:                          Network Sockets and Communication.
                                                            (line 31637)
* SO_PRIORITY:                           Network Sockets and Communication.
                                                            (line 31639)
* SO_RCVBUF:                             Network Sockets and Communication.
                                                            (line 31635)
* SO_REUSEADDR:                          Network Sockets and Communication.
                                                            (line 31628)
* SO_REUSEPORT:                          Network Sockets and Communication.
                                                            (line 31640)
* SO_SNDBUF:                             Network Sockets and Communication.
                                                            (line 31634)
* SO_STYLE:                              Network Sockets and Communication.
                                                            (line 31629)
* SO_TYPE:                               Network Sockets and Communication.
                                                            (line 31630)
* ssize_t:                               Foreign Types.     (line 25173)
* standard-vtable-fields:                Meta-Vtables.      (line 14147)
* stream-null:                           SRFI-41 Stream Primitives.
                                                            (line 36896)
* te:                                    HTTP Headers.      (line 32735)
* texi-command-specs:                    texinfo.           (line 43651)
* time-duration:                         SRFI-19 Time.      (line 35962)
* time-monotonic:                        SRFI-19 Time.      (line 35953)
* time-process:                          SRFI-19 Time.      (line 35965)
* time-tai:                              SRFI-19 Time.      (line 35950)
* time-thread:                           SRFI-19 Time.      (line 35969)
* time-utc:                              SRFI-19 Time.      (line 35947)
* trailer:                               HTTP Headers.      (line 32506)
* transfer-encoding:                     HTTP Headers.      (line 32512)
* uint16:                                Foreign Types.     (line 25154)
* uint32:                                Foreign Types.     (line 25156)
* uint64:                                Foreign Types.     (line 25158)
* uint8:                                 Foreign Types.     (line 25153)
* unsigned-int:                          Foreign Types.     (line 25169)
* unsigned-long:                         Foreign Types.     (line 25171)
* upgrade:                               HTTP Headers.      (line 32518)
* user-agent:                            HTTP Headers.      (line 32741)
* vary:                                  HTTP Headers.      (line 32790)
* via:                                   HTTP Headers.      (line 32525)
* vlist-null:                            VLists.            (line 13477)
* void:                                  Foreign Types.     (line 25179)
* vtable-index-layout:                   Vtable Contents.   (line 14032)
* vtable-index-printer:                  Vtable Contents.   (line 14045)
* vtable-offset-user:                    Meta-Vtables.      (line 14151)
* WAIT_ANY:                              Processes.         (line 30428)
* WAIT_MYPGRP:                           Processes.         (line 30430)
* warning:                               HTTP Headers.      (line 32532)
* WNOHANG:                               Processes.         (line 30439)
* WUNTRACED:                             Processes.         (line 30443)
* www-authenticate:                      HTTP Headers.      (line 32799)
* W_OK:                                  File System.       (line 29561)
* X_OK:                                  File System.       (line 29563)

