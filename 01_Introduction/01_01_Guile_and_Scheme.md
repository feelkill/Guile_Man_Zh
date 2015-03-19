<!--
1.1 Guile and Scheme
====================
-->

## 1.1 Guile与Scheme

<!--
Guile implements Scheme as described in the Revised^5 Report on the
Algorithmic Language Scheme (usually known as R5RS), providing clean and
general data and control structures.  Guile goes beyond the rather
austere language presented in R5RS, extending it with a module system,
full access to POSIX system calls, networking support, multiple threads,
dynamic linking, a foreign function call interface, powerful string
processing, and many other features needed for programming in the real
world.
-->

Guile实现了R5RS所描述的Scheme语言。此外，Guile又超越了这一朴素无华的语言，它提供了一个模块化的系统，对POSIX系统调用的完全访问，网络支持，多线程，动态链接，外部函数的调用接口，强大的字符串处理，以及其他现实世界里编程需要的特性。

<!--
   The Scheme community has recently agreed and published R6RS, the
latest installment in the RnRS series.  R6RS significantly expands the
core Scheme language, and standardises many non-core functions that
implementations—including Guile—have previously done in different ways.
Guile has been updated to incorporate some of the features of R6RS, and
to adjust some existing features to conform to the R6RS specification,
but it is by no means a complete R6RS implementation.  *Note R6RS
Support::.
-->

Scheme社区最近已经同意并出版了R6RS，它是RnRS系列里的最新版。R6RS大大扩展了Scheme语言的核心（特征），同时标准化了许多非核心函数。其实，包括Guile在内，之前已经通过不同方式完成了这些非核心函数的实现。Guile已经更新，以容纳R6RS的一些特性，并且调整了一些现有特性使之符合R6RS规范。但是，它还不是真正意义上的、完整的R6RS实现。注意只是对R6RS支持了。

<!--
   Between R5RS and R6RS, the SRFI process (<http://srfi.schemers.org/>)
standardised interfaces for many practical needs, such as multithreaded
programming and multidimensional arrays.  Guile supports many SRFIs, as
documented in detail in *note SRFI Support::.
-->

出于许多实践的需要，SRFI(<http://srfi.schemers.org/>)会处理R5RS与R6RS之间的标准化接口，像多线程编程和多维数组。Guile支持许多SRFIs，详细内容见SRFI支持文档。

<!--
   In summary, so far as relationship to the Scheme standards is
concerned, Guile is an R5RS implementation with many extensions, some of
which conform to SRFIs or to the relevant parts of R6RS.
-->

总之，就目前来说，Guile是一个R5RS的实现，同时又扩展了许多特性，其中一部分遵循SRFIs或者R6RS的相关部分。也就是说，Guile关注着Scheme标准的发展，又带有自己的独特特性。

