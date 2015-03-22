<!--
1.2 Combining with C Code
=========================
-->

## 1.2 与c代码结合

<!--
Like a shell, Guile can run interactively—reading expressions from the
user, evaluating them, and displaying the results—or as a script
interpreter, reading and executing Scheme code from a file.  Guile also
provides an object library, "libguile", that allows other applications
to easily incorporate a complete Scheme interpreter.  An application can
then use Guile as an extension language, a clean and powerful
configuration language, or as multi-purpose “glue”, connecting
primitives provided by the application.  It is easy to call Scheme code
from C code and vice versa, giving the application designer full control
of how and when to invoke the interpreter.  Applications can add new
functions, data types, control structures, and even syntax to Guile,
creating a domain-specific language tailored to the task at hand, but
based on a robust language design.
-->

Guile可以像Shell一样以交互方式运行:读入用户输入的的表达式,计算这些表达式,并显示结果。Guile也可以作为脚本解释器，从文件读取Scheme代码,然后执行。此外,Guile还提供libguile对象库,这允许其他应用程序能够轻松地加入一个完整的Scheme解释器。然后,应用程序将Guile作为一种扩展语言使用，一个干净而功能强大的配置语言，或者作为一个多用途的粘合剂，连接由应用程序提供的基元。从C代码调用Guile很容易,反之亦然。这赋予了应用程序设计者完全的控制能力，他们可以决定如何以及何时调用Guile解释器。应用程序能够向Guile中添加新的函数,数据类型,控制结构,甚至语法,从而为手头任务定制地创建特定域语言;但是，这基于一个鲁棒性的语言设计。

<!--
   This kind of combination is helped by four aspects of Guile’s design
and history.  First is that Guile has always been targeted as an
extension language.  Hence its C API has always been of great
importance, and has been developed accordingly.  Second and third are
rather technical points—that Guile uses conservative garbage collection,
and that it implements the Scheme concept of continuations by copying
and reinstating the C stack—but whose practical consequence is that most
existing C code can be glued into Guile as is, without needing
modifications to cope with strange Scheme execution flows.  Last is the
module system, which helps extensions to coexist without stepping on
each others’ toes.
-->

这种结合归功于Guile设计和历史的四个方面。首先,Guile的目标总是成为一种扩展语言。因此,其C API一直具有相当的重要性，并得到了相应地发展。Guile采用的主要技术点有：使用保守的垃圾回收机制;通过复制恢复C堆栈来实现了Scheme理念的延续性。但是，第二和第三方面并不是因为这些技术,而是这些技术带来的实际结果，大多数现有的C代码可以平滑地应用到Guile，不需要作修改来应付蹩脚的Scheme执行流。最后是模块系统，它有助于各个扩展共存,相互之间不受影响。

<!--
   Guile’s module system allows one to break up a large program into
manageable sections with well-defined interfaces between them.  Modules
may contain a mixture of interpreted and compiled code; Guile can use
either static or dynamic linking to incorporate compiled code.  Modules
also encourage developers to package up useful collections of routines
for general distribution; as of this writing, one can find Emacs
interfaces, database access routines, compilers, GUI toolkit interfaces,
and HTTP client functions, among others.
-->

Guile的模块系统允许将一个大程序分解成多个便于管理的部分,它们相互间有定义好的接口。模块可能包含有解释型代码，也可能包含编译好的代码，也可能是二者皆有。Guile可以使用静态链接或动态链接来包含编译好的代码。模块也鼓励开发者将有用的例程集合打包，作为一般发布。在撰写本文时，除其他外，人们还可以找到Emacs接口，数据库访问例程，编译器，GUI工具包接口和HTTP客户端功能。

