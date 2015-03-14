1.8 Typographical Conventions
=============================

In examples and procedure descriptions and all other places where the
evaluation of Scheme expression is shown, we use some notation for
denoting the output and evaluation results of expressions.

   The symbol ‘⇒’ is used to tell which value is returned by an
evaluation:

     (+ 1 2)
     ⇒ 3

   Some procedures produce some output besides returning a value.  This
is denoted by the symbol ‘⊣’.

     (begin (display 1) (newline) 'hooray)
     ⊣ 1
     ⇒ hooray

   As you can see, this code prints ‘1’ (denoted by ‘⊣’), and returns
‘hooray’ (denoted by ‘⇒’).

