<!--
1.8 Typographical Conventions
=============================
-->

## 1.8 排版约定

<!--
In examples and procedure descriptions and all other places where the
evaluation of Scheme expression is shown, we use some notation for
denoting the output and evaluation results of expressions.
-->

在描述例子例程,还有书写评估Scheme表达式的其他地方，我们用某些符号来表示表达式的输出和评估结果。

<!--
   The symbol ‘⇒’ is used to tell which value is returned by an
evaluation:
-->

   符号‘⇒’用来说明表达式返回了哪个值：

     (+ 1 2)
     ⇒ 3

<!--
   Some procedures produce some output besides returning a value.  This
is denoted by the symbol ‘⊣’.
-->

一些例程除了返回值还有输出。这用符号⊣’来表示。

     (begin (display 1) (newline) 'hooray')
     ⊣  1
     ⇒  hooray

<!--
   As you can see, this code prints ‘1’ (denoted by ‘⊣’), and returns
‘hooray’ (denoted by ‘⇒’).
-->

正如你所见，这段代码打印'1'(有符号‘⊣’表示)，并且返回了'hooray'(用符号‘⇒’表示)。

