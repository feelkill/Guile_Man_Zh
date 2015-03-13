<!--
文章原始URL:  http://www.gnu.org/software/guile/manual/html_node/Procedures-as-Values.html#Procedures-as-Values

术语列表
procedure >> 过程
R5RS >> The First Report on Scheme Revisited
-->

<!--
3.2.1 Procedures as Values
-->

# 3.2.1 过程也是值

<!--
One of the great simplifications of Scheme is that a procedure is just another type of value, and that procedure values can be passed around and stored in variables in exactly the same way as, for example, strings and lists. When we talk about a built-in standard Scheme procedure such as open-input-file, what we actually mean is that there is a pre-defined top level variable called open-input-file, whose value is a procedure that implements what R5RS says that open-input-file should do.
-->

Scheme最大的精简点之一在于，过程是另一种类型的值，过程值能够被传递，也能够像字符串和列表一样存储在变量中。当我们谈及一个内建的标准Scheme过程，比方说open-input-file，我们真正所指的是，在最顶级有一个预定义好的变量，它的名字是open-input-file，它的值是实现了R5RS中所说的open-input-file功能的一个过程。

<!--
Note that this is quite different from many dialects of Lisp — including Emacs Lisp — in which a program can use the same name with two quite separate meanings: one meaning identifies a Lisp function, while the other meaning identifies a Lisp variable, whose value need have nothing to do with the function that is associated with the first meaning. In these dialects, functions and variables are said to live in different namespaces.
-->

要注意的是，这一点非常地不同于其他Lisp方言，包括Emacs Lisp在内。在Guile里，程序里可以用相同名字的变量，却有着两个不同的含义：一个标识着一个Lisp函数，另一个标识着一个Lisp变量，而后者与前者相关联的函数是没有任何关系的。在这样的方言中，函数和变量是存活在不同的命名空间里的。

<!--
In Scheme, on the other hand, all names belong to a single unified namespace, and the variables that these names identify can hold any kind of Scheme value, including procedure values.
-->

换句话来说，在Scheme语言里，所有的名字从属于单一的命名空间，而这些名字标识的变量可以容纳任何类型的Scheme值，包括过程值。

<!--
One consequence of the “procedures as values” idea is that, if you don’t happen to like the standard name for a Scheme procedure, you can change it.
-->

过程也是值，这个思想的一个推论就是，如果你不喜欢Scheme过程的标准名字，你就可以给它重起个名字。

<!--
For example, call-with-current-continuation is a very important standard Scheme procedure, but it also has a very long name! So, many programmers use the following definition to assign the same procedure value to the more convenient name call/cc.
-->

比方说，call-with-current-continuation是一个很重要的标准Scheme过程，但是这个名字太长了。所以，许多程序员使用下面的定义来为这个过程值赋予一个更简短的名字call/cc。

<!--
(define call/cc call-with-current-continuation)
-->

(define call/cc call-with-current-continuation)

<!--
Let’s understand exactly how this works. The definition creates a new variable call/cc, and then sets its value to the value of the variable call-with-current-continuation; the latter value is a procedure that implements the behaviour that R5RS specifies under the name “call-with-current-continuation”. So call/cc ends up holding this value as well.
-->

让我们来理解它是怎么工作的。该定义创建了一个新的变量call/cc，然后把call-with-current-continuation的值给了它。后者的值就是一个过程值，它实现了R5RS规定里call-with-current-continuation的行为。所以，结束时call/cc存储了一个过程值。

<!--
Now that call/cc holds the required procedure value, you could choose to use call-with-current-continuation for a completely different purpose, or just change its value so that you will get an error if you accidentally use call-with-current-continuation as a procedure in your program rather than call/cc. For example:
-->

现在call/cc拥有了想要的过程值，你就可以选择让call-with-current-continuation用于其他目的，或者直接改变它的值；那么，如果你恰好在你的程序里把call-with-current-continuation而不是call/cc作为过程进行调用的话，你会获得一个错误。举例讲，

<!--
(set! call-with-current-continuation "Not a procedure any more!")
-->

(set! call-with-current-continuation "Not a procedure any more!")

<!--
Or you could just leave call-with-current-continuation as it was. It’s perfectly fine for more than one variable to hold the same procedure value. 
-->

要么，你可以把call-with-current-continuation闲置不理。当然，对于同一个过程值，你可以使用多个不同的变量，这种做法是相当不错的。

