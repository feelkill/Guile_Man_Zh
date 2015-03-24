<!--
1.4 Interactive Programming
===========================
-->

## 1.4 交互式编程

<!--
Non-free software has no interest in its users being able to see how it
works.  They are supposed to just accept it, or to report problems and
hope that the source code owners will choose to work on them.
-->

非自由软件对用户理解它是如何工作的这种事情并不感兴趣。用户要么接受它，要么反馈问题。用户只能寄希望于源码作者，选择性地修复这些问题。

<!--
   Free software aims to work reliably just as much as non-free software
does, but it should also empower its users by making its workings
available.  This is useful for many reasons, including education,
auditing and enhancements, as well as for debugging problems.
-->

正如非自由软件所作的那样，自由软件的目标是可靠地工作。但是，它应该同时授权它的用户，让他们理解它工作的原理。这样做是有用的，也是有原因的，像教育，审计，功能增强，还有调试问题。

<!--
   The ideal free software system achieves this by making it easy for
interested users to see the source code for a feature that they are
using, and to follow through that source code step-by-step, as it runs.
In Emacs, good examples of this are the source code hyperlinks in the
help system, and ‘edebug’.  Then, for bonus points and maximising the
ability for the user to experiment quickly with code changes, the system
should allow parts of the source code to be modified and reloaded into
the running program, to take immediate effect.
-->

完美的自由软件系统会让感兴趣的用户看到他们正在使用的特性的源代码，会让他们在运行时一步一步地跟踪源代码流程，以方便用户的方式来做到“授权”。在Emacs中，较好的例子是帮助系统里的hyperlinks源代码，还有edebug。然后，为了使用户能够获得快速体验代码变化的最大能力，该系统还应该允许部分代码加以修改，并加载进正在运行的程序里，从而达到立竿见影的效果。

<!--
   Guile is designed for this kind of interactive programming, and this
distinguishes it from many Scheme implementations that instead
prioritise running a fixed Scheme program as fast as possible—because
there are tradeoffs between performance and the ability to modify parts
of an already running program.  There are faster Schemes than Guile, but
Guile is a GNU project and so prioritises the GNU vision of programming
freedom and experimentation.
-->

Guile正是设计为此类的交互式编程语言。这区别于许多其他的Scheme实现，它们都是优先让一个修复好的Scheme程序尽可能快的运行起来。原因在于，修改已经正在运行程序的一部分这种能力和运行性能之间是需要权衡和取舍的。比Guile运行快的Scheme有的是，但是Guile是一个GNU项目，所以它优先关注了编程自由和编程体验这个GNU范围。

