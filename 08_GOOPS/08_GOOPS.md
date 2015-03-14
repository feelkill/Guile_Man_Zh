8 GOOPS
*******

GOOPS is the object oriented extension to Guile.  Its implementation is
derived from STk-3.99.3 by Erick Gallesio and version 1.3 of Gregor
Kiczales’ ‘Tiny-Clos’.  It is very close in spirit to CLOS, the Common
Lisp Object System, but is adapted for the Scheme language.

   GOOPS is a full object oriented system, with classes, objects,
multiple inheritance, and generic functions with multi-method dispatch.
Furthermore its implementation relies on a meta object protocol — which
means that GOOPS’s core operations are themselves defined as methods on
relevant classes, and can be customised by overriding or redefining
those methods.

   To start using GOOPS you first need to import the ‘(oop goops)’
module.  You can do this at the Guile REPL by evaluating:

     (use-modules (oop goops))

8.1 Copyright Notice
====================

The material in this chapter is partly derived from the STk Reference
Manual written by Erick Gallesio, whose copyright notice is as follows.

   Copyright © 1993-1999 Erick Gallesio - I3S-CNRS/ESSI <eg@unice.fr>
Permission to use, copy, modify, distribute,and license this software
and its documentation for any purpose is hereby granted, provided that
existing copyright notices are retained in all copies and that this
notice is included verbatim in any distributions.  No written agreement,
license, or royalty fee is required for any of the authorized uses.
This software is provided “AS IS” without express or implied warranty.

   The material has been adapted for use in Guile, with the author’s
permission.

8.2 Class Definition
====================

A new class is defined with the ‘define-class’ syntax:

     (define-class CLASS (SUPERCLASS …)
        SLOT-DESCRIPTION …
        CLASS-OPTION …)

   CLASS is the class being defined.  The list of SUPERCLASSes specifies
which existing classes, if any, to inherit slots and properties from.
"Slots" hold per-instance(1) data, for instances of that class — like
“fields” or “member variables” in other object oriented systems.  Each
SLOT-DESCRIPTION gives the name of a slot and optionally some
“properties” of this slot; for example its initial value, the name of a
function which will access its value, and so on.  Class options, slot
descriptions and inheritance are discussed more below.

 -- syntax: define-class name (super …) slot-definition … class-option …
     Define a class called NAME that inherits from SUPERs, with direct
     slots defined by SLOT-DEFINITIONs and CLASS-OPTIONs.  The newly
     created class is bound to the variable name NAME in the current
     environment.

     Each SLOT-DEFINITION is either a symbol that names the slot or a
     list,

          (SLOT-NAME-SYMBOL . SLOT-OPTIONS)

     where SLOT-NAME-SYMBOL is a symbol and SLOT-OPTIONS is a list with
     an even number of elements.  The even-numbered elements of
     SLOT-OPTIONS (counting from zero) are slot option keywords; the
     odd-numbered elements are the corresponding values for those
     keywords.

     Each CLASS-OPTION is an option keyword and corresponding value.

   As an example, let us define a type for representing a complex number
in terms of two real numbers.(2)  This can be done with the following
class definition:

     (define-class <my-complex> (<number>)
        r i)

   This binds the variable ‘<my-complex>’ to a new class whose instances
will contain two slots.  These slots are called ‘r’ and ‘i’ and will
hold the real and imaginary parts of a complex number.  Note that this
class inherits from ‘<number>’, which is a predefined class.(3)

   Slot options are described in the next section.  The possible class
options are as follows.

 -- class option: #:metaclass metaclass
     The ‘#:metaclass’ class option specifies the metaclass of the class
     being defined.  METACLASS must be a class that inherits from
     ‘<class>’.  For the use of metaclasses, see *note Metaobjects and
     the Metaobject Protocol:: and *note Metaclasses::.

     If the ‘#:metaclass’ option is absent, GOOPS reuses or constructs a
     metaclass for the new class by calling ‘ensure-metaclass’ (*note
     ensure-metaclass: Class Definition Protocol.).

 -- class option: #:name name
     The ‘#:name’ class option specifies the new class’s name.  This
     name is used to identify the class whenever related objects - the
     class itself, its instances and its subclasses - are printed.

     If the ‘#:name’ option is absent, GOOPS uses the first argument to
     ‘define-class’ as the class name.

   ---------- Footnotes ----------

   (1) Usually — but see also the ‘#:allocation’ slot option.

   (2) Of course Guile already provides complex numbers, and ‘<complex>’
is in fact a predefined class in GOOPS; but the definition here is still
useful as an example.

   (3) ‘<number>’ is the direct superclass of the predefined class
‘<complex>’; ‘<complex>’ is the superclass of ‘<real>’, and ‘<real>’ is
the superclass of ‘<integer>’.

8.3 Instance Creation and Slot Access
=====================================

An instance (or object) of a defined class can be created with ‘make’.
‘make’ takes one mandatory parameter, which is the class of the instance
to create, and a list of optional arguments that will be used to
initialize the slots of the new instance.  For instance the following
form

     (define c (make <my-complex>))

creates a new ‘<my-complex>’ object and binds it to the Scheme variable
‘c’.

 -- generic: make
 -- method: make (class <class>) initarg …
     Create and return a new instance of class CLASS, initialized using
     INITARG ....

     In theory, INITARG … can have any structure that is understood by
     whatever methods get applied when the ‘initialize’ generic function
     is applied to the newly allocated instance.

     In practice, specialized ‘initialize’ methods would normally call
     ‘(next-method)’, and so eventually the standard GOOPS ‘initialize’
     methods are applied.  These methods expect INITARGS to be a list
     with an even number of elements, where even-numbered elements
     (counting from zero) are keywords and odd-numbered elements are the
     corresponding values.

     GOOPS processes initialization argument keywords automatically for
     slots whose definition includes the ‘#:init-keyword’ option (*note
     init-keyword: Slot Options.).  Other keyword value pairs can only
     be processed by an ‘initialize’ method that is specialized for the
     new instance’s class.  Any unprocessed keyword value pairs are
     ignored.

 -- generic: make-instance
 -- method: make-instance (class <class>) initarg …
     ‘make-instance’ is an alias for ‘make’.

   The slots of the new complex number can be accessed using ‘slot-ref’
and ‘slot-set!’.  ‘slot-set!’ sets the value of an object slot and
‘slot-ref’ retrieves it.

     (slot-set! c 'r 10)
     (slot-set! c 'i 3)
     (slot-ref c 'r) ⇒ 10
     (slot-ref c 'i) ⇒ 3

   The ‘(oop goops describe)’ module provides a ‘describe’ function that
is useful for seeing all the slots of an object; it prints the slots and
their values to standard output.

     (describe c)
     ⊣
     #<<my-complex> 401d8638> is an instance of class <my-complex>
     Slots are:
          r = 10
          i = 3

8.4 Slot Options
================

When specifying a slot (in a ‘(define-class …)’ form), various options
can be specified in addition to the slot’s name.  Each option is
specified by a keyword.  The list of possible keywords is as follows.

 -- slot option: #:init-value init-value
 -- slot option: #:init-form init-form
 -- slot option: #:init-thunk init-thunk
 -- slot option: #:init-keyword init-keyword
     These options provide various ways to specify how to initialize the
     slot’s value at instance creation time.

     INIT-VALUE specifies a fixed initial slot value (shared across all
     new instances of the class).

     INIT-THUNK specifies a thunk that will provide a default value for
     the slot.  The thunk is called when a new instance is created and
     should return the desired initial slot value.

     INIT-FORM specifies a form that, when evaluated, will return an
     initial value for the slot.  The form is evaluated each time that
     an instance of the class is created, in the lexical environment of
     the containing ‘define-class’ expression.

     INIT-KEYWORD specifies a keyword that can be used to pass an
     initial slot value to ‘make’ when creating a new instance.

     Note that, since an ‘init-value’ value is shared across all
     instances of a class, you should only use it when the initial value
     is an immutable value, like a constant.  If you want to initialize
     a slot with a fresh, independently mutable value, you should use
     ‘init-thunk’ or ‘init-form’ instead.  Consider the following
     example.

          (define-class <chbouib> ()
            (hashtab #:init-value (make-hash-table)))

     Here only one hash table is created and all instances of
     ‘<chbouib>’ have their ‘hashtab’ slot refer to it.  In order to
     have each instance of ‘<chbouib>’ refer to a new hash table, you
     should instead write:

          (define-class <chbouib> ()
            (hashtab #:init-thunk make-hash-table))

     or:

          (define-class <chbouib> ()
            (hashtab #:init-form (make-hash-table)))

     If more than one of these options is specified for the same slot,
     the order of precedence, highest first is

        • ‘#:init-keyword’, if INIT-KEYWORD is present in the options
          passed to ‘make’

        • ‘#:init-thunk’, ‘#:init-form’ or ‘#:init-value’.

     If the slot definition contains more than one initialization option
     of the same precedence, the later ones are ignored.  If a slot is
     not initialized at all, its value is unbound.

     In general, slots that are shared between more than one instance
     are only initialized at new instance creation time if the slot
     value is unbound at that time.  However, if the new instance
     creation specifies a valid init keyword and value for a shared
     slot, the slot is re-initialized regardless of its previous value.

     Note, however, that the power of GOOPS’ metaobject protocol means
     that everything written here may be customized or overridden for
     particular classes!  The slot initializations described here are
     performed by the least specialized method of the generic function
     ‘initialize’, whose signature is

          (define-method (initialize (object <object>) initargs) ...)

     The initialization of instances of any given class can be
     customized by defining a ‘initialize’ method that is specialized
     for that class, and the author of the specialized method may decide
     to call ‘next-method’ - which will result in a call to the next
     less specialized ‘initialize’ method - at any point within the
     specialized code, or maybe not at all.  In general, therefore, the
     initialization mechanisms described here may be modified or
     overridden by more specialized code, or may not be supported at all
     for particular classes.

 -- slot option: #:getter getter
 -- slot option: #:setter setter
 -- slot option: #:accessor accessor
     Given an object OBJ with slots named ‘foo’ and ‘bar’, it is always
     possible to read and write those slots by calling ‘slot-ref’ and
     ‘slot-set!’ with the relevant slot name; for example:

          (slot-ref OBJ 'foo)
          (slot-set! OBJ 'bar 25)

     The ‘#:getter’, ‘#:setter’ and ‘#:accessor’ options, if present,
     tell GOOPS to create generic function and method definitions that
     can be used to get and set the slot value more conveniently.
     GETTER specifies a generic function to which GOOPS will add a
     method for getting the slot value.  SETTER specifies a generic
     function to which GOOPS will add a method for setting the slot
     value.  ACCESSOR specifies an accessor to which GOOPS will add
     methods for both getting and setting the slot value.

     So if a class includes a slot definition like this:

          (c #:getter get-count #:setter set-count #:accessor count)

     GOOPS defines generic function methods such that the slot value can
     be referenced using either the getter or the accessor -

          (let ((current-count (get-count obj))) …)
          (let ((current-count (count obj))) …)

     - and set using either the setter or the accessor -

          (set-count obj (+ 1 current-count))
          (set! (count obj) (+ 1 current-count))

     Note that

        • with an accessor, the slot value is set using the generalized
          ‘set!’ syntax

        • in practice, it is unusual for a slot to use all three of
          these options: read-only, write-only and read-write slots
          would typically use only ‘#:getter’, ‘#:setter’ and
          ‘#:accessor’ options respectively.

     The binding of the specified names is done in the environment of
     the ‘define-class’ expression.  If the names are already bound (in
     that environment) to values that cannot be upgraded to generic
     functions, those values are overwritten when the ‘define-class’
     expression is evaluated.  For more detail, see *note
     ensure-generic: Generic Function Internals.

 -- slot option: #:allocation allocation
     The ‘#:allocation’ option tells GOOPS how to allocate storage for
     the slot.  Possible values for ALLOCATION are

        • ‘#:instance’

          Indicates that GOOPS should create separate storage for this
          slot in each new instance of the containing class (and its
          subclasses).  This is the default.

        • ‘#:class’

          Indicates that GOOPS should create storage for this slot that
          is shared by all instances of the containing class (and its
          subclasses).  In other words, a slot in class C with
          allocation ‘#:class’ is shared by all INSTANCEs for which
          ‘(is-a? INSTANCE C)’.  This permits defining a kind of global
          variable which can be accessed only by (in)direct instances of
          the class which defines the slot.

        • ‘#:each-subclass’

          Indicates that GOOPS should create storage for this slot that
          is shared by all _direct_ instances of the containing class,
          and that whenever a subclass of the containing class is
          defined, GOOPS should create a new storage for the slot that
          is shared by all _direct_ instances of the subclass.  In other
          words, a slot with allocation ‘#:each-subclass’ is shared by
          all instances with the same ‘class-of’.

        • ‘#:virtual’

          Indicates that GOOPS should not allocate storage for this
          slot.  The slot definition must also include the ‘#:slot-ref’
          and ‘#:slot-set!’ options to specify how to reference and set
          the value for this slot.  See the example below.

     Slot allocation options are processed when defining a new class by
     the generic function ‘compute-get-n-set’, which is specialized by
     the class’s metaclass.  Hence new types of slot allocation can be
     implemented by defining a new metaclass and a method for
     ‘compute-get-n-set’ that is specialized for the new metaclass.  For
     an example of how to do this, see *note Customizing Class
     Definition::.

 -- slot option: #:slot-ref getter
 -- slot option: #:slot-set! setter
     The ‘#:slot-ref’ and ‘#:slot-set!’ options must be specified if the
     slot allocation is ‘#:virtual’, and are ignored otherwise.

     GETTER should be a closure taking a single INSTANCE parameter that
     returns the current slot value.  SETTER should be a closure taking
     two parameters - INSTANCE and NEW-VAL - that sets the slot value to
     NEW-VAL.

8.5 Illustrating Slot Description
=================================

To illustrate slot description, we can redefine the ‘<my-complex>’ class
seen before.  A definition could be:

     (define-class <my-complex> (<number>)
        (r #:init-value 0 #:getter get-r #:setter set-r! #:init-keyword #:r)
        (i #:init-value 0 #:getter get-i #:setter set-i! #:init-keyword #:i))

With this definition, the ‘r’ and ‘i’ slots are set to 0 by default, and
can be initialised to other values by calling ‘make’ with the ‘#:r’ and
‘#:i’ keywords.  Also the generic functions ‘get-r’, ‘set-r!’, ‘get-i’
and ‘set-i!’ are automatically defined to read and write the slots.

     (define c1 (make <my-complex> #:r 1 #:i 2))
     (get-r c1) ⇒ 1
     (set-r! c1 12)
     (get-r c1) ⇒ 12
     (define c2 (make <my-complex> #:r 2))
     (get-r c2) ⇒ 2
     (get-i c2) ⇒ 0

   Accessors can both read and write a slot.  So, another definition of
the ‘<my-complex>’ class, using the ‘#:accessor’ option, could be:

     (define-class <my-complex> (<number>)
        (r #:init-value 0 #:accessor real-part #:init-keyword #:r)
        (i #:init-value 0 #:accessor imag-part #:init-keyword #:i))

With this definition, the ‘r’ slot can be read with:
     (real-part c)
and set with:
     (set! (real-part c) new-value)

   Suppose now that we want to manipulate complex numbers with both
rectangular and polar coordinates.  One solution could be to have a
definition of complex numbers which uses one particular representation
and some conversion functions to pass from one representation to the
other.  A better solution is to use virtual slots, like this:

     (define-class <my-complex> (<number>)
        ;; True slots use rectangular coordinates
        (r #:init-value 0 #:accessor real-part #:init-keyword #:r)
        (i #:init-value 0 #:accessor imag-part #:init-keyword #:i)
        ;; Virtual slots access do the conversion
        (m #:accessor magnitude #:init-keyword #:magn
           #:allocation #:virtual
           #:slot-ref (lambda (o)
                       (let ((r (slot-ref o 'r)) (i (slot-ref o 'i)))
                         (sqrt (+ (* r r) (* i i)))))
           #:slot-set! (lambda (o m)
                         (let ((a (slot-ref o 'a)))
                           (slot-set! o 'r (* m (cos a)))
                           (slot-set! o 'i (* m (sin a))))))
        (a #:accessor angle #:init-keyword #:angle
           #:allocation #:virtual
           #:slot-ref (lambda (o)
                       (atan (slot-ref o 'i) (slot-ref o 'r)))
           #:slot-set! (lambda(o a)
                        (let ((m (slot-ref o 'm)))
                           (slot-set! o 'r (* m (cos a)))
                           (slot-set! o 'i (* m (sin a)))))))


   In this class definition, the magnitude ‘m’ and angle ‘a’ slots are
virtual, and are calculated, when referenced, from the normal (i.e.
‘#:allocation #:instance’) slots ‘r’ and ‘i’, by calling the function
defined in the relevant ‘#:slot-ref’ option.  Correspondingly, writing
‘m’ or ‘a’ leads to calling the function defined in the ‘#:slot-set!’
option.  Thus the following expression

     (slot-set! c 'a 3)

permits to set the angle of the ‘c’ complex number.

     (define c (make <my-complex> #:r 12 #:i 20))
     (real-part c) ⇒ 12
     (angle c) ⇒ 1.03037682652431
     (slot-set! c 'i 10)
     (set! (real-part c) 1)
     (describe c)
     ⊣
     #<<my-complex> 401e9b58> is an instance of class <my-complex>
     Slots are:
          r = 1
          i = 10
          m = 10.0498756211209
          a = 1.47112767430373

   Since initialization keywords have been defined for the four slots,
we can now define the standard Scheme primitives ‘make-rectangular’ and
‘make-polar’.

     (define make-rectangular
        (lambda (x y) (make <my-complex> #:r x #:i y)))

     (define make-polar
        (lambda (x y) (make <my-complex> #:magn x #:angle y)))

8.6 Methods and Generic Functions
=================================

A GOOPS method is like a Scheme procedure except that it is specialized
for a particular set of argument classes, and will only be used when the
actual arguments in a call match the classes in the method definition.

     (define-method (+ (x <string>) (y <string>))
       (string-append x y))

     (+ "abc" "de") ⇒ "abcde"

   A method is not formally associated with any single class (as it is
in many other object oriented languages), because a method can be
specialized for a combination of several classes.  If you’ve studied
object orientation in non-Lispy languages, you may remember discussions
such as whether a method to stretch a graphical image around a surface
should be a method of the image class, with a surface as a parameter, or
a method of the surface class, with an image as a parameter.  In GOOPS
you’d just write

     (define-method (stretch (im <image>) (sf <surface>))
       ...)

and the question of which class the method is more associated with does
not need answering.

   There can simultaneously be several methods with the same name but
different sets of specializing argument classes; for example:

     (define-method (+ (x <string>) (y <string)) ...)
     (define-method (+ (x <matrix>) (y <matrix>)) ...)
     (define-method (+ (f <fish>) (b <bicycle>)) ...)
     (define-method (+ (a <foo>) (b <bar>) (c <baz>)) ...)

A generic function is a container for the set of such methods that a
program intends to use.

   If you look at a program’s source code, and see ‘(+ x y)’ somewhere
in it, conceptually what is happening is that the program at that point
calls a generic function (in this case, the generic function bound to
the identifier ‘+’).  When that happens, Guile works out which of the
generic function’s methods is the most appropriate for the arguments
that the function is being called with; then it evaluates the method’s
code with the arguments as formal parameters.  This happens every time
that a generic function call is evaluated — it isn’t assumed that a
given source code call will end up invoking the same method every time.

   Defining an identifier as a generic function is done with the
‘define-generic’ macro.  Definition of a new method is done with the
‘define-method’ macro.  Note that ‘define-method’ automatically does a
‘define-generic’ if the identifier concerned is not already a generic
function, so often an explicit ‘define-generic’ call is not needed.

 -- syntax: define-generic symbol
     Create a generic function with name SYMBOL and bind it to the
     variable SYMBOL.  If SYMBOL was previously bound to a Scheme
     procedure (or procedure-with-setter), the old procedure (and
     setter) is incorporated into the new generic function as its
     default procedure (and setter).  Any other previous value,
     including an existing generic function, is discarded and replaced
     by a new, empty generic function.

 -- syntax: define-method (generic parameter …) body …
     Define a method for the generic function or accessor GENERIC with
     parameters PARAMETERs and body BODY ....

     GENERIC is a generic function.  If GENERIC is a variable which is
     not yet bound to a generic function object, the expansion of
     ‘define-method’ will include a call to ‘define-generic’.  If
     GENERIC is ‘(setter GENERIC-WITH-SETTER)’, where
     GENERIC-WITH-SETTER is a variable which is not yet bound to a
     generic-with-setter object, the expansion will include a call to
     ‘define-accessor’.

     Each PARAMETER must be either a symbol or a two-element list
     ‘(SYMBOL CLASS)’.  The symbols refer to variables in the body forms
     that will be bound to the parameters supplied by the caller when
     calling this method.  The CLASSes, if present, specify the possible
     combinations of parameters to which this method can be applied.

     BODY … are the bodies of the method definition.

   ‘define-method’ expressions look a little like Scheme procedure
definitions of the form

     (define (name formals …) . body)

   The important difference is that each formal parameter, apart from
the possible “rest” argument, can be qualified by a class name: ‘FORMAL’
becomes ‘(FORMAL CLASS)’.  The meaning of this qualification is that the
method being defined will only be applicable in a particular generic
function invocation if the corresponding argument is an instance of
‘CLASS’ (or one of its subclasses).  If more than one of the formal
parameters is qualified in this way, then the method will only be
applicable if each of the corresponding arguments is an instance of its
respective qualifying class.

   Note that unqualified formal parameters act as though they are
qualified by the class ‘<top>’, which GOOPS uses to mean the superclass
of all valid Scheme types, including both primitive types and GOOPS
classes.

   For example, if a generic function method is defined with PARAMETERs
‘(s1 <square>)’ and ‘(n <number>)’, that method is only applicable to
invocations of its generic function that have two parameters where the
first parameter is an instance of the ‘<square>’ class and the second
parameter is a number.

8.6.1 Accessors
---------------

An accessor is a generic function that can also be used with the
generalized ‘set!’ syntax (*note Procedures with Setters::).  Guile will
handle a call like

     (set! (accessor args…) value)

by calling the most specialized method of ‘accessor’ that matches the
classes of ‘args’ and ‘value’.  ‘define-accessor’ is used to bind an
identifier to an accessor.

 -- syntax: define-accessor symbol
     Create an accessor with name SYMBOL and bind it to the variable
     SYMBOL.  If SYMBOL was previously bound to a Scheme procedure (or
     procedure-with-setter), the old procedure (and setter) is
     incorporated into the new accessor as its default procedure (and
     setter).  Any other previous value, including an existing generic
     function or accessor, is discarded and replaced by a new, empty
     accessor.

8.6.2 Extending Primitives
--------------------------

Many of Guile’s primitive procedures can be extended by giving them a
generic function definition that operates in conjunction with their
normal C-coded implementation.  When a primitive is extended in this
way, it behaves like a generic function with the C-coded implementation
as its default method.

   This extension happens automatically if a method is defined (by a
‘define-method’ call) for a variable whose current value is a primitive.
But it can also be forced by calling ‘enable-primitive-generic!’.

 -- primitive procedure: enable-primitive-generic! primitive
     Force the creation of a generic function definition for PRIMITIVE.

   Once the generic function definition for a primitive has been
created, it can be retrieved using ‘primitive-generic-generic’.

 -- primitive procedure: primitive-generic-generic primitive
     Return the generic function definition of PRIMITIVE.

     ‘primitive-generic-generic’ raises an error if PRIMITIVE is not a
     primitive with generic capability.

8.6.3 Merging Generics
----------------------

GOOPS generic functions and accessors often have short, generic names.
For example, if a vector package provides an accessor for the X
coordinate of a vector, that accessor may just be called ‘x’.  It
doesn’t need to be called, for example, ‘vector:x’, because GOOPS will
work out, when it sees code like ‘(x OBJ)’, that the vector-specific
method of ‘x’ should be called if OBJ is a vector.

   That raises the question, though, of what happens when different
packages define a generic function with the same name.  Suppose we work
with a graphical package which needs to use two independent vector
packages for 2D and 3D vectors respectively.  If both packages export
‘x’, what does the code using those packages end up with?

   *note duplicate binding handlers: Creating Guile Modules. explains
how this is resolved for conflicting bindings in general.  For generics,
there is a special duplicates handler, ‘merge-generics’, which tells the
module system to merge generic functions with the same name.  Here is an
example:

     (define-module (math 2D-vectors)
       #:use-module (oop goops)
       #:export (x y ...))

     (define-module (math 3D-vectors)
       #:use-module (oop goops)
       #:export (x y z ...))

     (define-module (my-module)
       #:use-module (oop goops)
       #:use-module (math 2D-vectors)
       #:use-module (math 3D-vectors)
       #:duplicates (merge-generics))

   The generic function ‘x’ in ‘(my-module)’ will now incorporate all of
the methods of ‘x’ from both imported modules.

   To be precise, there will now be three distinct generic functions
named ‘x’: ‘x’ in ‘(math 2D-vectors)’, ‘x’ in ‘(math 3D-vectors)’, and
‘x’ in ‘(my-module)’; and these functions share their methods in an
interesting and dynamic way.

   To explain, let’s call the imported generic functions (in ‘(math
2D-vectors)’ and ‘(math 3D-vectors)’) the "ancestors", and the merged
generic function (in ‘(my-module)’), the "descendant".  The general rule
is that for any generic function G, the applicable methods are selected
from the union of the methods of G’s descendant functions, the methods
of G itself and the methods of G’s ancestor functions.

   Thus ancestor functions effectively share methods with their
descendants, and vice versa.  In the example above, ‘x’ in ‘(math
2D-vectors)’ will share the methods of ‘x’ in ‘(my-module)’ and vice
versa.(1)  Sharing is dynamic, so adding another new method to a
descendant implies adding it to that descendant’s ancestors too.

   ---------- Footnotes ----------

   (1) But note that ‘x’ in ‘(math 2D-vectors)’ doesn’t share methods
with ‘x’ in ‘(math 3D-vectors)’, so modularity is still preserved.

8.6.4 Next-method
-----------------

When you call a generic function, with a particular set of arguments,
GOOPS builds a list of all the methods that are applicable to those
arguments and orders them by how closely the method definitions match
the actual argument types.  It then calls the method at the top of this
list.  If the selected method’s code wants to call on to the next method
in this list, it can do so by using ‘next-method’.

     (define-method (Test (a <integer>)) (cons 'integer (next-method)))
     (define-method (Test (a <number>))  (cons 'number  (next-method)))
     (define-method (Test a)             (list 'top))

   With these definitions,

     (Test 1)   ⇒ (integer number top)
     (Test 1.0) ⇒ (number top)
     (Test #t)  ⇒ (top)

   ‘next-method’ is always called as just ‘(next-method)’.  The
arguments for the next method call are always implicit, and always the
same as for the original method call.

   If you want to call on to a method with the same name but with a
different set of arguments (as you might with overloaded methods in C++,
for example), you do not use ‘next-method’, but instead simply write the
new call as usual:

     (define-method (Test (a <number>) min max)
       (if (and (>= a min) (<= a max))
           (display "Number is in range\n"))
       (Test a))

     (Test 2 1 10)
     ⊣
     Number is in range
     ⇒
     (integer number top)

   (You should be careful in this case that the ‘Test’ calls do not lead
to an infinite recursion, but this consideration is just the same as in
Scheme code in general.)

8.6.5 Generic Function and Method Examples
------------------------------------------

Consider the following definitions:

     (define-generic G)
     (define-method (G (a <integer>) b) 'integer)
     (define-method (G (a <real>) b) 'real)
     (define-method (G a b) 'top)

   The ‘define-generic’ call defines G as a generic function.  The three
next lines define methods for G.  Each method uses a sequence of
"parameter specializers" that specify when the given method is
applicable.  A specializer permits to indicate the class a parameter
must belong to (directly or indirectly) to be applicable.  If no
specializer is given, the system defaults it to ‘<top>’.  Thus, the
first method definition is equivalent to

     (define-method (G (a <integer>) (b <top>)) 'integer)

   Now, let’s look at some possible calls to the generic function G:

     (G 2 3)    ⇒ integer
     (G 2 #t)   ⇒ integer
     (G 1.2 'a) ⇒ real
     (G #t #f)  ⇒ top
     (G 1 2 3)  ⇒ error (since no method exists for 3 parameters)

   The methods above use only one specializer per parameter list.  But
in general, any or all of a method’s parameters may be specialized.
Suppose we define now:

     (define-method (G (a <integer>) (b <number>))  'integer-number)
     (define-method (G (a <integer>) (b <real>))    'integer-real)
     (define-method (G (a <integer>) (b <integer>)) 'integer-integer)
     (define-method (G a (b <number>))              'top-number)

With these definitions:

     (G 1 2)   ⇒ integer-integer
     (G 1 1.0) ⇒ integer-real
     (G 1 #t)  ⇒ integer
     (G 'a 1)  ⇒ top-number

   As a further example we shall continue to define operations on the
‘<my-complex>’ class.  Suppose that we want to use it to implement
complex numbers completely.  For instance a definition for the addition
of two complex numbers could be

     (define-method (new-+ (a <my-complex>) (b <my-complex>))
       (make-rectangular (+ (real-part a) (real-part b))
                         (+ (imag-part a) (imag-part b))))

   To be sure that the ‘+’ used in the method ‘new-+’ is the standard
addition we can do:

     (define-generic new-+)

     (let ((+ +))
       (define-method (new-+ (a <my-complex>) (b <my-complex>))
         (make-rectangular (+ (real-part a) (real-part b))
                           (+ (imag-part a) (imag-part b)))))

   The ‘define-generic’ ensures here that ‘new-+’ will be defined in the
global environment.  Once this is done, we can add methods to the
generic function ‘new-+’ which make a closure on the ‘+’ symbol.  A
complete writing of the ‘new-+’ methods is shown in *note Figure 8.1:
fig:newplus.

     (define-generic new-+)

     (let ((+ +))

       (define-method (new-+ (a <real>) (b <real>)) (+ a b))

       (define-method (new-+ (a <real>) (b <my-complex>))
         (make-rectangular (+ a (real-part b)) (imag-part b)))

       (define-method (new-+ (a <my-complex>) (b <real>))
         (make-rectangular (+ (real-part a) b) (imag-part a)))

       (define-method (new-+ (a <my-complex>) (b <my-complex>))
         (make-rectangular (+ (real-part a) (real-part b))
                           (+ (imag-part a) (imag-part b))))

       (define-method (new-+ (a <number>))  a)

       (define-method (new-+) 0)

       (define-method (new-+ . args)
         (new-+ (car args)
           (apply new-+ (cdr args)))))

     (set! + new-+)

Figure 8.1: Extending ‘+’ to handle complex numbers

   We take advantage here of the fact that generic function are not
obliged to have a fixed number of parameters.  The four first methods
implement dyadic addition.  The fifth method says that the addition of a
single element is this element itself.  The sixth method says that using
the addition with no parameter always return 0 (as is also true for the
primitive ‘+’).  The last method takes an arbitrary number of
parameters(1).  This method acts as a kind of ‘reduce’: it calls the
dyadic addition on the _car_ of the list and on the result of applying
it on its rest.  To finish, the ‘set!’ permits to redefine the ‘+’
symbol to our extended addition.

   To conclude our implementation (integration?)  of complex numbers, we
could redefine standard Scheme predicates in the following manner:

     (define-method (complex? c <my-complex>) #t)
     (define-method (complex? c)           #f)

     (define-method (number? n <number>) #t)
     (define-method (number? n)          #f)
     …

   Standard primitives in which complex numbers are involved could also
be redefined in the same manner.

   ---------- Footnotes ----------

   (1) The parameter list for a ‘define-method’ follows the conventions
used for Scheme procedures.  In particular it can use the dot notation
or a symbol to denote an arbitrary number of parameters

8.6.6 Handling Invocation Errors
--------------------------------

If a generic function is invoked with a combination of parameters for
which there is no applicable method, GOOPS raises an error.

 -- generic: no-method
 -- method: no-method (gf <generic>) args
     When an application invokes a generic function, and no methods at
     all have been defined for that generic function, GOOPS calls the
     ‘no-method’ generic function.  The default method calls
     ‘goops-error’ with an appropriate message.

 -- generic: no-applicable-method
 -- method: no-applicable-method (gf <generic>) args
     When an application applies a generic function to a set of
     arguments, and no methods have been defined for those argument
     types, GOOPS calls the ‘no-applicable-method’ generic function.
     The default method calls ‘goops-error’ with an appropriate message.

 -- generic: no-next-method
 -- method: no-next-method (gf <generic>) args
     When a generic function method calls ‘(next-method)’ to invoke the
     next less specialized method for that generic function, and no less
     specialized methods have been defined for the current generic
     function arguments, GOOPS calls the ‘no-next-method’ generic
     function.  The default method calls ‘goops-error’ with an
     appropriate message.

8.7 Inheritance
===============

Here are some class definitions to help illustrate inheritance:

     (define-class A () a)
     (define-class B () b)
     (define-class C () c)
     (define-class D (A B) d a)
     (define-class E (A C) e c)
     (define-class F (D E) f)

   ‘A’, ‘B’, ‘C’ have a null list of superclasses.  In this case, the
system will replace the null list by a list which only contains
‘<object>’, the root of all the classes defined by ‘define-class’.  ‘D’,
‘E’, ‘F’ use multiple inheritance: each class inherits from two
previously defined classes.  Those class definitions define a hierarchy
which is shown in *note Figure 8.2: fig:hier.  In this figure, the class
‘<top>’ is also shown; this class is the superclass of all Scheme
objects.  In particular, ‘<top>’ is the superclass of all standard
Scheme types.

          <top>
          / \\\_____________________
         /   \\___________          \
        /     \           \          \
    <object>  <pair>  <procedure>  <number>
    /  |  \                           |
   /   |   \                          |
  A    B    C                      <complex>
  |\__/__   |                         |
   \ /   \ /                          |
    D     E                         <real>
     \   /                            |
       F                              |
                                   <integer>

Figure 8.2: A class hierarchy.

   When a class has superclasses, its set of slots is calculated by
taking the union of its own slots and those of all its superclasses.
Thus each instance of D will have three slots, ‘a’, ‘b’ and ‘d’).  The
slots of a class can be discovered using the ‘class-slots’ primitive.
For instance,

     (class-slots A) ⇒ ((a))
     (class-slots E) ⇒ ((a) (e) (c))
     (class-slots F) ⇒ ((e) (c) (b) (d) (a) (f))

The ordering of the returned slots is not significant.

8.7.1 Class Precedence List
---------------------------

What happens when a class inherits from two or more superclasses that
have a slot with the same name but incompatible definitions — for
example, different init values or slot allocations?  We need a rule for
deciding which slot definition the derived class ends up with, and this
rule is provided by the class’s "Class Precedence List".(1)

   Another problem arises when invoking a generic function, and there is
more than one method that could apply to the call arguments.  Here we
need a way of ordering the applicable methods, so that Guile knows which
method to use first, which to use next if that method calls
‘next-method’, and so on.  One of the ingredients for this ordering is
determining, for each given call argument, which of the specializing
classes, from each applicable method’s definition, is the most specific
for that argument; and here again the class precedence list helps.

   If inheritance was restricted such that each class could only have
one superclass — which is known as "single" inheritance — class ordering
would be easy.  The rule would be simply that a subclass is considered
more specific than its superclass.

   With multiple inheritance, ordering is less obvious, and we have to
impose an arbitrary rule to determine precedence.  Suppose we have

     (define-class X ()
        (x #:init-value 1))

     (define-class Y ()
        (x #:init-value 2))

     (define-class Z (X Y)
        (…))

Clearly the ‘Z’ class is more specific than ‘X’ or ‘Y’, for instances of
‘Z’.  But which is more specific out of ‘X’ and ‘Y’ — and hence, for the
definitions above, which ‘#:init-value’ will take effect when creating
an instance of ‘Z’?  The rule in GOOPS is that the superclasses listed
earlier are more specific than those listed later.  Hence ‘X’ is more
specific than ‘Y’, and the ‘#:init-value’ for slot ‘x’ in instances of
‘Z’ will be 1.

   Hence there is a linear ordering for a class and all its
superclasses, from most specific to least specific, and this ordering is
called the Class Precedence List of the class.

   In fact the rules above are not quite enough to always determine a
unique order, but they give an idea of how things work.  For example,
for the ‘F’ class shown in *note Figure 8.2: fig:hier, the class
precedence list is

     (f d e a c b <object> <top>)

In cases where there is any ambiguity (like this one), it is a bad idea
for programmers to rely on exactly what the order is.  If the order for
some superclasses is important, it can be expressed directly in the
class definition.

   The precedence list of a class can be obtained by calling
‘class-precedence-list’.  This function returns a ordered list whose
first element is the most specific class.  For instance:

     (class-precedence-list B) ⇒ (#<<class> B 401b97c8>
                                          #<<class> <object> 401e4a10>
                                          #<<class> <top> 4026a9d8>)

Or for a more immediately readable result:

     (map class-name (class-precedence-list B)) ⇒ (B <object> <top>)

   ---------- Footnotes ----------

   (1) This section is an adaptation of material from Jeff Dalton’s
(J.Dalton@ed.ac.uk) ‘Brief introduction to CLOS’

8.7.2 Sorting Methods
---------------------

Now, with the idea of the class precedence list, we can state precisely
how the possible methods are sorted when more than one of the methods of
a generic function are applicable to the call arguments.

   The rules are that
   • the applicable methods are sorted in order of specificity, and the
     most specific method is used first, then the next if that method
     calls ‘next-method’, and so on

   • a method M1 is more specific than another method M2 if the first
     specializing class that differs, between the definitions of M1 and
     M2, is more specific, in M1’s definition, for the corresponding
     actual call argument, than the specializing class in M2’s
     definition

   • a class C1 is more specific than another class C2, for an object of
     actual class C, if C1 comes before C2 in C’s class precedence list.

8.8 Introspection
=================

"Introspection", or "reflection", means being able to obtain information
dynamically about GOOPS objects.  It is perhaps best illustrated by
considering an object oriented language that does not provide any
introspection, namely C++.

   Nothing in C++ allows a running program to obtain answers to the
following types of question:

   • What are the data members of this object or class?

   • What classes does this class inherit from?

   • Is this method call virtual or non-virtual?

   • If I invoke ‘Employee::adjustHoliday()’, what class contains the
     ‘adjustHoliday()’ method that will be applied?

   In C++, answers to such questions can only be determined by looking
at the source code, if you have access to it.  GOOPS, on the other hand,
includes procedures that allow answers to these questions — or their
GOOPS equivalents — to be obtained dynamically, at run time.

8.8.1 Classes
-------------

A GOOPS class is itself an instance of the ‘<class>’ class, or of a
subclass of ‘<class>’.  The definition of the ‘<class>’ class has slots
that are used to describe the properties of a class, including the
following.

 -- primitive procedure: class-name class
     Return the name of class CLASS.  This is the value of CLASS’s
     ‘name’ slot.

 -- primitive procedure: class-direct-supers class
     Return a list containing the direct superclasses of CLASS.  This is
     the value of CLASS’s ‘direct-supers’ slot.

 -- primitive procedure: class-direct-slots class
     Return a list containing the slot definitions of the direct slots
     of CLASS.  This is the value of CLASS’s ‘direct-slots’ slot.

 -- primitive procedure: class-direct-subclasses class
     Return a list containing the direct subclasses of CLASS.  This is
     the value of CLASS’s ‘direct-subclasses’ slot.

 -- primitive procedure: class-direct-methods class
     Return a list of all the generic function methods that use CLASS as
     a formal parameter specializer.  This is the value of CLASS’s
     ‘direct-methods’ slot.

 -- primitive procedure: class-precedence-list class
     Return the class precedence list for class CLASS (*note Class
     Precedence List::).  This is the value of CLASS’s ‘cpl’ slot.

 -- primitive procedure: class-slots class
     Return a list containing the slot definitions for all CLASS’s
     slots, including any slots that are inherited from superclasses.
     This is the value of CLASS’s ‘slots’ slot.

 -- procedure: class-subclasses class
     Return a list of all subclasses of CLASS.

 -- procedure: class-methods class
     Return a list of all methods that use CLASS or a subclass of CLASS
     as one of its formal parameter specializers.

8.8.2 Instances
---------------

 -- primitive procedure: class-of value
     Return the GOOPS class of any Scheme VALUE.

 -- primitive procedure: instance? object
     Return ‘#t’ if OBJECT is any GOOPS instance, otherwise ‘#f’.

 -- procedure: is-a? object class
     Return ‘#t’ if OBJECT is an instance of CLASS or one of its
     subclasses.

   You can use the ‘is-a?’ predicate to ask whether any given value
belongs to a given class, or ‘class-of’ to discover the class of a given
value.  Note that when GOOPS is loaded (by code using the ‘(oop goops)’
module) built-in classes like ‘<string>’, ‘<list>’ and ‘<number>’ are
automatically set up, corresponding to all Guile Scheme types.

     (is-a? 2.3 <number>) ⇒ #t
     (is-a? 2.3 <real>) ⇒ #t
     (is-a? 2.3 <string>) ⇒ #f
     (is-a? '("a" "b") <string>) ⇒ #f
     (is-a? '("a" "b") <list>) ⇒ #t
     (is-a? (car '("a" "b")) <string>) ⇒ #t
     (is-a? <string> <class>) ⇒ #t
     (is-a? <class> <string>) ⇒ #f

     (class-of 2.3) ⇒ #<<class> <real> 908c708>
     (class-of #(1 2 3)) ⇒ #<<class> <vector> 908cd20>
     (class-of <string>) ⇒ #<<class> <class> 8bd3e10>
     (class-of <class>) ⇒ #<<class> <class> 8bd3e10>

8.8.3 Slots
-----------

 -- procedure: class-slot-definition class slot-name
     Return the slot definition for the slot named SLOT-NAME in class
     CLASS.  SLOT-NAME should be a symbol.

 -- procedure: slot-definition-name slot-def
     Extract and return the slot name from SLOT-DEF.

 -- procedure: slot-definition-options slot-def
     Extract and return the slot options from SLOT-DEF.

 -- procedure: slot-definition-allocation slot-def
     Extract and return the slot allocation option from SLOT-DEF.  This
     is the value of the ‘#:allocation’ keyword (*note allocation: Slot
     Options.), or ‘#:instance’ if the ‘#:allocation’ keyword is absent.

 -- procedure: slot-definition-getter slot-def
     Extract and return the slot getter option from SLOT-DEF.  This is
     the value of the ‘#:getter’ keyword (*note getter: Slot Options.),
     or ‘#f’ if the ‘#:getter’ keyword is absent.

 -- procedure: slot-definition-setter slot-def
     Extract and return the slot setter option from SLOT-DEF.  This is
     the value of the ‘#:setter’ keyword (*note setter: Slot Options.),
     or ‘#f’ if the ‘#:setter’ keyword is absent.

 -- procedure: slot-definition-accessor slot-def
     Extract and return the slot accessor option from SLOT-DEF.  This is
     the value of the ‘#:accessor’ keyword (*note accessor: Slot
     Options.), or ‘#f’ if the ‘#:accessor’ keyword is absent.

 -- procedure: slot-definition-init-value slot-def
     Extract and return the slot init-value option from SLOT-DEF.  This
     is the value of the ‘#:init-value’ keyword (*note init-value: Slot
     Options.), or the unbound value if the ‘#:init-value’ keyword is
     absent.

 -- procedure: slot-definition-init-form slot-def
     Extract and return the slot init-form option from SLOT-DEF.  This
     is the value of the ‘#:init-form’ keyword (*note init-form: Slot
     Options.), or the unbound value if the ‘#:init-form’ keyword is
     absent.

 -- procedure: slot-definition-init-thunk slot-def
     Extract and return the slot init-thunk option from SLOT-DEF.  This
     is the value of the ‘#:init-thunk’ keyword (*note init-thunk: Slot
     Options.), or ‘#f’ if the ‘#:init-thunk’ keyword is absent.

 -- procedure: slot-definition-init-keyword slot-def
     Extract and return the slot init-keyword option from SLOT-DEF.
     This is the value of the ‘#:init-keyword’ keyword (*note
     init-keyword: Slot Options.), or ‘#f’ if the ‘#:init-keyword’
     keyword is absent.

 -- procedure: slot-init-function class slot-name
     Return the initialization function for the slot named SLOT-NAME in
     class CLASS.  SLOT-NAME should be a symbol.

     The returned initialization function incorporates the effects of
     the standard ‘#:init-thunk’, ‘#:init-form’ and ‘#:init-value’ slot
     options.  These initializations can be overridden by the
     ‘#:init-keyword’ slot option or by a specialized ‘initialize’
     method, so, in general, the function returned by
     ‘slot-init-function’ may be irrelevant.  For a fuller discussion,
     see *note init-value: Slot Options.

8.8.4 Generic Functions
-----------------------

A generic function is an instance of the ‘<generic>’ class, or of a
subclass of ‘<generic>’.  The definition of the ‘<generic>’ class has
slots that are used to describe the properties of a generic function.

 -- primitive procedure: generic-function-name gf
     Return the name of generic function GF.

 -- primitive procedure: generic-function-methods gf
     Return a list of the methods of generic function GF.  This is the
     value of GF’s ‘methods’ slot.

   Similarly, a method is an instance of the ‘<method>’ class, or of a
subclass of ‘<method>’; and the definition of the ‘<method>’ class has
slots that are used to describe the properties of a method.

 -- primitive procedure: method-generic-function method
     Return the generic function that METHOD belongs to.  This is the
     value of METHOD’s ‘generic-function’ slot.

 -- primitive procedure: method-specializers method
     Return a list of METHOD’s formal parameter specializers .  This is
     the value of METHOD’s ‘specializers’ slot.

 -- primitive procedure: method-procedure method
     Return the procedure that implements METHOD.  This is the value of
     METHOD’s ‘procedure’ slot.

 -- generic: method-source
 -- method: method-source (m <method>)
     Return an expression that prints to show the definition of method
     M.

          (define-generic cube)

          (define-method (cube (n <number>))
            (* n n n))

          (map method-source (generic-function-methods cube))
          ⇒
          ((method ((n <number>)) (* n n n)))

8.8.5 Accessing Slots
---------------------

Any slot, regardless of its allocation, can be queried, referenced and
set using the following four primitive procedures.

 -- primitive procedure: slot-exists? obj slot-name
     Return ‘#t’ if OBJ has a slot with name SLOT-NAME, otherwise ‘#f’.

 -- primitive procedure: slot-bound? obj slot-name
     Return ‘#t’ if the slot named SLOT-NAME in OBJ has a value,
     otherwise ‘#f’.

     ‘slot-bound?’ calls the generic function ‘slot-missing’ if OBJ does
     not have a slot called SLOT-NAME (*note slot-missing: Accessing
     Slots.).

 -- primitive procedure: slot-ref obj slot-name
     Return the value of the slot named SLOT-NAME in OBJ.

     ‘slot-ref’ calls the generic function ‘slot-missing’ if OBJ does
     not have a slot called SLOT-NAME (*note slot-missing: Accessing
     Slots.).

     ‘slot-ref’ calls the generic function ‘slot-unbound’ if the named
     slot in OBJ does not have a value (*note slot-unbound: Accessing
     Slots.).

 -- primitive procedure: slot-set! obj slot-name value
     Set the value of the slot named SLOT-NAME in OBJ to VALUE.

     ‘slot-set!’ calls the generic function ‘slot-missing’ if OBJ does
     not have a slot called SLOT-NAME (*note slot-missing: Accessing
     Slots.).

   GOOPS stores information about slots in classes.  Internally, all of
these procedures work by looking up the slot definition for the slot
named SLOT-NAME in the class ‘(class-of OBJ)’, and then using the slot
definition’s “getter” and “setter” closures to get and set the slot
value.

   The next four procedures differ from the previous ones in that they
take the class as an explicit argument, rather than assuming ‘(class-of
OBJ)’.  Therefore they allow you to apply the “getter” and “setter”
closures of a slot definition in one class to an instance of a different
class.

 -- primitive procedure: slot-exists-using-class? class obj slot-name
     Return ‘#t’ if CLASS has a slot definition for a slot with name
     SLOT-NAME, otherwise ‘#f’.

 -- primitive procedure: slot-bound-using-class? class obj slot-name
     Return ‘#t’ if applying ‘slot-ref-using-class’ to the same
     arguments would call the generic function ‘slot-unbound’, otherwise
     ‘#f’.

     ‘slot-bound-using-class?’ calls the generic function ‘slot-missing’
     if CLASS does not have a slot definition for a slot called
     SLOT-NAME (*note slot-missing: Accessing Slots.).

 -- primitive procedure: slot-ref-using-class class obj slot-name
     Apply the “getter” closure for the slot named SLOT-NAME in CLASS to
     OBJ, and return its result.

     ‘slot-ref-using-class’ calls the generic function ‘slot-missing’ if
     CLASS does not have a slot definition for a slot called SLOT-NAME
     (*note slot-missing: Accessing Slots.).

     ‘slot-ref-using-class’ calls the generic function ‘slot-unbound’ if
     the application of the “getter” closure to OBJ returns an unbound
     value (*note slot-unbound: Accessing Slots.).

 -- primitive procedure: slot-set-using-class! class obj slot-name value
     Apply the “setter” closure for the slot named SLOT-NAME in CLASS to
     OBJ and VALUE.

     ‘slot-set-using-class!’ calls the generic function ‘slot-missing’
     if CLASS does not have a slot definition for a slot called
     SLOT-NAME (*note slot-missing: Accessing Slots.).

   Slots whose allocation is per-class rather than per-instance can be
referenced and set without needing to specify any particular instance.

 -- procedure: class-slot-ref class slot-name
     Return the value of the slot named SLOT-NAME in class CLASS.  The
     named slot must have ‘#:class’ or ‘#:each-subclass’ allocation
     (*note allocation: Slot Options.).

     If there is no such slot with ‘#:class’ or ‘#:each-subclass’
     allocation, ‘class-slot-ref’ calls the ‘slot-missing’ generic
     function with arguments CLASS and SLOT-NAME.  Otherwise, if the
     slot value is unbound, ‘class-slot-ref’ calls the ‘slot-unbound’
     generic function, with the same arguments.

 -- procedure: class-slot-set! class slot-name value
     Set the value of the slot named SLOT-NAME in class CLASS to VALUE.
     The named slot must have ‘#:class’ or ‘#:each-subclass’ allocation
     (*note allocation: Slot Options.).

     If there is no such slot with ‘#:class’ or ‘#:each-subclass’
     allocation, ‘class-slot-ref’ calls the ‘slot-missing’ generic
     function with arguments CLASS and SLOT-NAME.

   When a ‘slot-ref’ or ‘slot-set!’ call specifies a non-existent slot
name, or tries to reference a slot whose value is unbound, GOOPS calls
one of the following generic functions.

 -- generic: slot-missing
 -- method: slot-missing (class <class>) slot-name
 -- method: slot-missing (class <class>) (object <object>) slot-name
 -- method: slot-missing (class <class>) (object <object>) slot-name
          value
     When an application attempts to reference or set a class or
     instance slot by name, and the slot name is invalid for the
     specified CLASS or OBJECT, GOOPS calls the ‘slot-missing’ generic
     function.

     The default methods all call ‘goops-error’ with an appropriate
     message.

 -- generic: slot-unbound
 -- method: slot-unbound (object <object>)
 -- method: slot-unbound (class <class>) slot-name
 -- method: slot-unbound (class <class>) (object <object>) slot-name
     When an application attempts to reference a class or instance slot,
     and the slot’s value is unbound, GOOPS calls the ‘slot-unbound’
     generic function.

     The default methods all call ‘goops-error’ with an appropriate
     message.

8.9 Error Handling
==================

The procedure ‘goops-error’ is called to raise an appropriate error by
the default methods of the following generic functions:

   • ‘slot-missing’ (*note slot-missing: Accessing Slots.)

   • ‘slot-unbound’ (*note slot-unbound: Accessing Slots.)

   • ‘no-method’ (*note no-method: Handling Invocation Errors.)

   • ‘no-applicable-method’ (*note no-applicable-method: Handling
     Invocation Errors.)

   • ‘no-next-method’ (*note no-next-method: Handling Invocation
     Errors.)

   If you customize these functions for particular classes or
metaclasses, you may still want to use ‘goops-error’ to signal any error
conditions that you detect.

 -- procedure: goops-error format-string arg …
     Raise an error with key ‘goops-error’ and error message constructed
     from FORMAT-STRING and ARG ....  Error message formatting is as
     done by ‘scm-error’.

8.10 GOOPS Object Miscellany
============================

Here we cover some points about GOOPS objects that aren’t substantial
enough to merit sections on their own.

Object Equality
---------------

When GOOPS is loaded, ‘eqv?’, ‘equal?’ and ‘=’ become generic functions,
and you can define methods for them, specialized for your own classes,
so as to control what the various kinds of equality mean for your
classes.

   For example, the ‘assoc’ procedure, for looking up an entry in an
alist, is specified as using ‘equal?’ to determine when the car of an
entry in the alist is the same as the key parameter that ‘assoc’ is
called with.  Hence, if you had defined a new class, and wanted to use
instances of that class as the keys in an alist, you could define a
method for ‘equal?’, for your class, to control ‘assoc’’s lookup
precisely.

Cloning Objects
---------------

 -- generic: shallow-clone
 -- method: shallow-clone (self <object>)
     Return a “shallow” clone of SELF.  The default method makes a
     shallow clone by allocating a new instance and copying slot values
     from self to the new instance.  Each slot value is copied either as
     an immediate value or by reference.

 -- generic: deep-clone
 -- method: deep-clone (self <object>)
     Return a “deep” clone of SELF.  The default method makes a deep
     clone by allocating a new instance and copying or cloning slot
     values from self to the new instance.  If a slot value is an
     instance (satisfies ‘instance?’), it is cloned by calling
     ‘deep-clone’ on that value.  Other slot values are copied either as
     immediate values or by reference.

Write and Display
-----------------

 -- primitive generic: write object port
 -- primitive generic: display object port
     When GOOPS is loaded, ‘write’ and ‘display’ become generic
     functions with special methods for printing

        • objects - instances of the class ‘<object>’

        • foreign objects - instances of the class ‘<foreign-object>’

        • classes - instances of the class ‘<class>’

        • generic functions - instances of the class ‘<generic>’

        • methods - instances of the class ‘<method>’.

     ‘write’ and ‘display’ print non-GOOPS values in the same way as the
     Guile primitive ‘write’ and ‘display’ functions.

   In addition to the cases mentioned, you can of course define ‘write’
and ‘display’ methods for your own classes, to customize how instances
of those classes are printed.

8.11 The Metaobject Protocol
============================

At this point, we’ve said about as much as can be said about GOOPS
without having to confront the idea of the metaobject protocol.  There
are a couple more topics that could be discussed in isolation first —
class redefinition, and changing the class of existing instances — but
in practice developers using them will be advanced enough to want to
understand the metaobject protocol too, and will probably be using the
protocol to customize exactly what happens during these events.

   So let’s plunge in.  GOOPS is based on a “metaobject protocol” (aka
“MOP”) derived from the ones used in CLOS (the Common Lisp Object
System), tiny-clos (a small Scheme implementation of a subset of CLOS
functionality) and STKlos.

   The MOP underlies many possible GOOPS customizations — such as
defining an ‘initialize’ method to customize the initialization of
instances of an application-defined class — and an understanding of the
MOP makes it much easier to explain such customizations in a precise
way.  And at a deeper level, understanding the MOP is a key part of
understanding GOOPS, and of taking full advantage of GOOPS’ power, by
customizing the behaviour of GOOPS itself.

8.11.1 Metaobjects and the Metaobject Protocol
----------------------------------------------

The building blocks of GOOPS are classes, slot definitions, instances,
generic functions and methods.  A class is a grouping of inheritance
relations and slot definitions.  An instance is an object with slots
that are allocated following the rules implied by its class’s
superclasses and slot definitions.  A generic function is a collection
of methods and rules for determining which of those methods to apply
when the generic function is invoked.  A method is a procedure and a set
of specializers that specify the type of arguments to which the
procedure is applicable.

   Of these entities, GOOPS represents classes, generic functions and
methods as “metaobjects”.  In other words, the values in a GOOPS program
that describe classes, generic functions and methods, are themselves
instances (or “objects”) of special GOOPS classes that encapsulate the
behaviour, respectively, of classes, generic functions, and methods.

   (The other two entities are slot definitions and instances.  Slot
definitions are not strictly instances, but every slot definition is
associated with a GOOPS class that specifies the behaviour of the slot
as regards accessibility and protection from garbage collection.
Instances are of course objects in the usual sense, and there is no
benefit from thinking of them as metaobjects.)

   The “metaobject protocol” (or “MOP”) is the specification of the
generic functions which determine the behaviour of these metaobjects and
the circumstances in which these generic functions are invoked.

   For a concrete example of what this means, consider how GOOPS
calculates the set of slots for a class that is being defined using
‘define-class’.  The desired set of slots is the union of the new
class’s direct slots and the slots of all its superclasses.  But
‘define-class’ itself does not perform this calculation.  Instead, there
is a method of the ‘initialize’ generic function that is specialized for
instances of type ‘<class>’, and it is this method that performs the
slot calculation.

   ‘initialize’ is a generic function which GOOPS calls whenever a new
instance is created, immediately after allocating memory for a new
instance, in order to initialize the new instance’s slots.  The sequence
of steps is as follows.

   • ‘define-class’ uses ‘make’ to make a new instance of the ‘<class>’
     class, passing as initialization arguments the superclasses, slot
     definitions and class options that were specified in the
     ‘define-class’ form.

   • ‘make’ allocates memory for the new instance, and invokes the
     ‘initialize’ generic function to initialize the new instance’s
     slots.

   • The ‘initialize’ generic function applies the method that is
     specialized for instances of type ‘<class>’, and this method
     performs the slot calculation.

   In other words, rather than being hardcoded in ‘define-class’, the
default behaviour of class definition is encapsulated by generic
function methods that are specialized for the class ‘<class>’.

   It is possible to create a new class that inherits from ‘<class>’,
which is called a “metaclass”, and to write a new ‘initialize’ method
that is specialized for instances of the new metaclass.  Then, if the
‘define-class’ form includes a ‘#:metaclass’ class option whose value is
the new metaclass, the class that is defined by the ‘define-class’ form
will be an instance of the new metaclass rather than of the default
‘<class>’, and will be defined in accordance with the new ‘initialize’
method.  Thus the default slot calculation, as well as any other aspect
of the new class’s relationship with its superclasses, can be modified
or overridden.

   In a similar way, the behaviour of generic functions can be modified
or overridden by creating a new class that inherits from the standard
generic function class ‘<generic>’, writing appropriate methods that are
specialized to the new class, and creating new generic functions that
are instances of the new class.

   The same is true for method metaobjects.  And the same basic
mechanism allows the application class author to write an ‘initialize’
method that is specialized to their application class, to initialize
instances of that class.

   Such is the power of the MOP. Note that ‘initialize’ is just one of a
large number of generic functions that can be customized to modify the
behaviour of application objects and classes and of GOOPS itself.  Each
following section covers a particular area of GOOPS functionality, and
describes the generic functions that are relevant for customization of
that area.

8.11.2 Metaclasses
------------------

A "metaclass" is the class of an object which represents a GOOPS class.
Put more succinctly, a metaclass is a class’s class.

   Most GOOPS classes have the metaclass ‘<class>’ and, by default, any
new class that is created using ‘define-class’ has the metaclass
‘<class>’.

   But what does this really mean?  To find out, let’s look in more
detail at what happens when a new class is created using ‘define-class’:

     (define-class <my-class> (<object>) . slots)

Guile expands this to something like:

     (define <my-class> (class (<object>) . slots))

which in turn expands to:

     (define <my-class>
       (make <class> #:dsupers (list <object>) #:slots slots))

   As this expansion makes clear, the resulting value of ‘<my-class>’ is
an instance of the class ‘<class>’ with slot values specifying the
superclasses and slot definitions for the class ‘<my-class>’.
(‘#:dsupers’ and ‘#:slots’ are initialization keywords for the ‘dsupers’
and ‘dslots’ slots of the ‘<class>’ class.)

   Now suppose that you want to define a new class with a metaclass
other than the default ‘<class>’.  This is done by writing:

     (define-class <my-class2> (<object>)
        slot …
        #:metaclass <my-metaclass>)

and Guile expands _this_ to something like:

     (define <my-class2>
       (make <my-metaclass> #:dsupers (list <object>) #:slots slots))

   In this case, the value of ‘<my-class2>’ is an instance of the more
specialized class ‘<my-metaclass>’.  Note that ‘<my-metaclass>’ itself
must previously have been defined as a subclass of ‘<class>’.  For a
full discussion of when and how it is useful to define new metaclasses,
see *note MOP Specification::.

   Now let’s make an instance of ‘<my-class2>’:

     (define my-object (make <my-class2> ...))

   All of the following statements are correct expressions of the
relationships between ‘my-object’, ‘<my-class2>’, ‘<my-metaclass>’ and
‘<class>’.

   • ‘my-object’ is an instance of the class ‘<my-class2>’.

   • ‘<my-class2>’ is an instance of the class ‘<my-metaclass>’.

   • ‘<my-metaclass>’ is an instance of the class ‘<class>’.

   • The class of ‘my-object’ is ‘<my-class2>’.

   • The class of ‘<my-class2>’ is ‘<my-metaclass>’.

   • The class of ‘<my-metaclass>’ is ‘<class>’.

8.11.3 MOP Specification
------------------------

The aim of the MOP specification in this chapter is to specify all the
customizable generic function invocations that can be made by the
standard GOOPS syntax, procedures and methods, and to explain the
protocol for customizing such invocations.

   A generic function invocation is customizable if the types of the
arguments to which it is applied are not completely determined by the
lexical context in which the invocation appears.  For example, the
‘(initialize INSTANCE INITARGS)’ invocation in the default
‘make-instance’ method is customizable, because the type of the
‘INSTANCE’ argument is determined by the class that was passed to
‘make-instance’.

   (Whereas — to give a counter-example — the ‘(make <generic> #:name
',name)’ invocation in ‘define-generic’ is not customizable, because all
of its arguments have lexically determined types.)

   When using this rule to decide whether a given generic function
invocation is customizable, we ignore arguments that are expected to be
handled in method definitions as a single “rest” list argument.

   For each customizable generic function invocation, the "invocation
protocol" is explained by specifying

   • what, conceptually, the applied method is intended to do

   • what assumptions, if any, the caller makes about the applied
     method’s side effects

   • what the caller expects to get as the applied method’s return
     value.

8.11.4 Instance Creation Protocol
---------------------------------

‘make <class> . INITARGS’ (method)

   • ‘allocate-instance CLASS INITARGS’ (generic)

     The applied ‘allocate-instance’ method should allocate storage for
     a new instance of class CLASS and return the uninitialized
     instance.

   • ‘initialize INSTANCE INITARGS’ (generic)

     INSTANCE is the uninitialized instance returned by
     ‘allocate-instance’.  The applied method should initialize the new
     instance in whatever sense is appropriate for its class.  The
     method’s return value is ignored.

   ‘make’ itself is a generic function.  Hence the ‘make’ invocation
itself can be customized in the case where the new instance’s metaclass
is more specialized than the default ‘<class>’, by defining a ‘make’
method that is specialized to that metaclass.

   Normally, however, the method for classes with metaclass ‘<class>’
will be applied.  This method calls two generic functions:

   • (allocate-instance CLASS .  INITARGS)

   • (initialize INSTANCE .  INITARGS)

   ‘allocate-instance’ allocates storage for and returns the new
instance, uninitialized.  You might customize ‘allocate-instance’, for
example, if you wanted to provide a GOOPS wrapper around some other
object programming system.

   To do this, you would create a specialized metaclass, which would act
as the metaclass for all classes and instances from the other system.
Then define an ‘allocate-instance’ method, specialized to that
metaclass, which calls a Guile primitive C function (or FFI code), which
in turn allocates the new instance using the interface of the other
object system.

   In this case, for a complete system, you would also need to customize
a number of other generic functions like ‘make’ and ‘initialize’, so
that GOOPS knows how to make classes from the other system, access
instance slots, and so on.

   ‘initialize’ initializes the instance that is returned by
‘allocate-instance’.  The standard GOOPS methods perform initializations
appropriate to the instance class.

   • At the least specialized level, the method for instances of type
     ‘<object>’ performs internal GOOPS instance initialization, and
     initializes the instance’s slots according to the slot definitions
     and any slot initialization keywords that appear in INITARGS.

   • The method for instances of type ‘<class>’ calls ‘(next-method)’,
     then performs the class initializations described in *note Class
     Definition Protocol::.

   • and so on for generic functions, methods, operator classes …

   Similarly, you can customize the initialization of instances of any
application-defined class by defining an ‘initialize’ method specialized
to that class.

   Imagine a class whose instances’ slots need to be initialized at
instance creation time by querying a database.  Although it might be
possible to achieve this a combination of ‘#:init-thunk’ keywords and
closures in the slot definitions, it may be neater to write an
‘initialize’ method for the class that queries the database once and
initializes all the dependent slot values according to the results.

8.11.5 Class Definition Protocol
--------------------------------

Here is a summary diagram of the syntax, procedures and generic
functions that may be involved in class definition.

‘define-class’ (syntax)

   • ‘class’ (syntax)

        • ‘make-class’ (procedure)

             • ‘ensure-metaclass’ (procedure)

             • ‘make METACLASS …’ (generic)

                  • ‘allocate-instance’ (generic)

                  • ‘initialize’ (generic)

                       • ‘compute-cpl’ (generic)

                            • ‘compute-std-cpl’ (procedure)

                       • ‘compute-slots’ (generic)

                       • ‘compute-get-n-set’ (generic)

                       • ‘compute-getter-method’ (generic)

                       • ‘compute-setter-method’ (generic)

   • ‘class-redefinition’ (generic)

        • ‘remove-class-accessors’ (generic)

        • ‘update-direct-method!’ (generic)

        • ‘update-direct-subclass!’ (generic)

   Wherever a step above is marked as “generic”, it can be customized,
and the detail shown below it is only “correct” insofar as it describes
what the default method of that generic function does.  For example, if
you write an ‘initialize’ method, for some metaclass, that does not call
‘next-method’ and does not call ‘compute-cpl’, then ‘compute-cpl’ will
not be called when a class is defined with that metaclass.

   A ‘(define-class ...)’ form (*note Class Definition::) expands to an
expression which

   • checks that it is being evaluated only at top level

   • defines any accessors that are implied by the SLOT-DEFINITIONs

   • uses ‘class’ to create the new class

   • checks for a previous class definition for NAME and, if found,
     handles the redefinition by invoking ‘class-redefinition’ (*note
     Redefining a Class::).

 -- syntax: class name (super …) slot-definition … class-option …
     Return a newly created class that inherits from SUPERs, with direct
     slots defined by SLOT-DEFINITIONs and CLASS-OPTIONs.  For the
     format of SLOT-DEFINITIONs and CLASS-OPTIONs, see *note
     define-class: Class Definition.

‘class’ expands to an expression which

   • processes the class and slot definition options to check that they
     are well-formed, to convert the ‘#:init-form’ option to an
     ‘#:init-thunk’ option, to supply a default environment parameter
     (the current top-level environment) and to evaluate all the bits
     that need to be evaluated

   • calls ‘make-class’ to create the class with the processed and
     evaluated parameters.

 -- procedure: make-class supers slots class-option …
     Return a newly created class that inherits from SUPERS, with direct
     slots defined by SLOTS and CLASS-OPTIONs.  For the format of SLOTS
     and CLASS-OPTIONs, see *note define-class: Class Definition, except
     note that for ‘make-class’, SLOTS is a separate list of slot
     definitions.

‘make-class’

   • adds ‘<object>’ to the SUPERS list if SUPERS is empty or if none of
     the classes in SUPERS have ‘<object>’ in their class precedence
     list

   • defaults the ‘#:environment’, ‘#:name’ and ‘#:metaclass’ options,
     if they are not specified by OPTIONS, to the current top-level
     environment, the unbound value, and ‘(ensure-metaclass SUPERS)’
     respectively

   • checks for duplicate classes in SUPERS and duplicate slot names in
     SLOTS, and signals an error if there are any duplicates

   • calls ‘make’, passing the metaclass as the first parameter and all
     other parameters as option keywords with values.

 -- procedure: ensure-metaclass supers env
     Return a metaclass suitable for a class that inherits from the list
     of classes in SUPERS.  The returned metaclass is the union by
     inheritance of the metaclasses of the classes in SUPERS.

     In the simplest case, where all the SUPERS are straightforward
     classes with metaclass ‘<class>’, the returned metaclass is just
     ‘<class>’.

     For a more complex example, suppose that SUPERS contained one class
     with metaclass ‘<operator-class>’ and one with metaclass
     ‘<foreign-object-class>’.  Then the returned metaclass would be a
     class that inherits from both ‘<operator-class>’ and
     ‘<foreign-object-class>’.

     If SUPERS is the empty list, ‘ensure-metaclass’ returns the default
     GOOPS metaclass ‘<class>’.

     GOOPS keeps a list of the metaclasses created by
     ‘ensure-metaclass’, so that each required type of metaclass only
     has to be created once.

     The ‘env’ parameter is ignored.

 -- generic: make metaclass initarg …
     METACLASS is the metaclass of the class being defined, either taken
     from the ‘#:metaclass’ class option or computed by
     ‘ensure-metaclass’.  The applied method must create and return the
     fully initialized class metaobject for the new class definition.

   The ‘(make METACLASS INITARG …)’ invocation is a particular case of
the instance creation protocol covered in the previous section.  It will
create an class metaobject with metaclass METACLASS.  By default, this
metaobject will be initialized by the ‘initialize’ method that is
specialized for instances of type ‘<class>’.

   The ‘initialize’ method for classes (signature ‘(initialize <class>
initargs)’) calls the following generic functions.

   • ‘compute-cpl CLASS’ (generic)

     The applied method should compute and return the class precedence
     list for CLASS as a list of class metaobjects.  When ‘compute-cpl’
     is called, the following CLASS metaobject slots have all been
     initialized: ‘name’, ‘direct-supers’, ‘direct-slots’,
     ‘direct-subclasses’ (empty), ‘direct-methods’.  The value returned
     by ‘compute-cpl’ will be stored in the ‘cpl’ slot.

   • ‘compute-slots CLASS’ (generic)

     The applied method should compute and return the slots (union of
     direct and inherited) for CLASS as a list of slot definitions.
     When ‘compute-slots’ is called, all the CLASS metaobject slots
     mentioned for ‘compute-cpl’ have been initialized, plus the
     following: ‘cpl’, ‘redefined’ (‘#f’), ‘environment’.  The value
     returned by ‘compute-slots’ will be stored in the ‘slots’ slot.

   • ‘compute-get-n-set CLASS SLOT-DEF’ (generic)

     ‘initialize’ calls ‘compute-get-n-set’ for each slot computed by
     ‘compute-slots’.  The applied method should compute and return a
     pair of closures that, respectively, get and set the value of the
     specified slot.  The get closure should have arity 1 and expect a
     single argument that is the instance whose slot value is to be
     retrieved.  The set closure should have arity 2 and expect two
     arguments, where the first argument is the instance whose slot
     value is to be set and the second argument is the new value for
     that slot.  The closures should be returned in a two element list:
     ‘(list GET SET)’.

     The closures returned by ‘compute-get-n-set’ are stored as part of
     the value of the CLASS metaobject’s ‘getters-n-setters’ slot.
     Specifically, the value of this slot is a list with the same number
     of elements as there are slots in the class, and each element looks
     either like

          (SLOT-NAME-SYMBOL INIT-FUNCTION . INDEX)

     or like

          (SLOT-NAME-SYMBOL INIT-FUNCTION GET SET)

     Where the get and set closures are replaced by INDEX, the slot is
     an instance slot and INDEX is the slot’s index in the underlying
     structure: GOOPS knows how to get and set the value of such slots
     and so does not need specially constructed get and set closures.
     Otherwise, GET and SET are the closures returned by
     ‘compute-get-n-set’.

     The structure of the ‘getters-n-setters’ slot value is important
     when understanding the next customizable generic functions that
     ‘initialize’ calls…

   • ‘compute-getter-method CLASS GNS’ (generic)

     ‘initialize’ calls ‘compute-getter-method’ for each of the class’s
     slots (as determined by ‘compute-slots’) that includes a ‘#:getter’
     or ‘#:accessor’ slot option.  GNS is the element of the CLASS
     metaobject’s ‘getters-n-setters’ slot that specifies how the slot
     in question is referenced and set, as described above under
     ‘compute-get-n-set’.  The applied method should create and return a
     method that is specialized for instances of type CLASS and uses the
     get closure to retrieve the slot’s value.  ‘initialize’ uses
     ‘add-method!’ to add the returned method to the generic function
     named by the slot definition’s ‘#:getter’ or ‘#:accessor’ option.

   • ‘compute-setter-method CLASS GNS’ (generic)

     ‘compute-setter-method’ is invoked with the same arguments as
     ‘compute-getter-method’, for each of the class’s slots that
     includes a ‘#:setter’ or ‘#:accessor’ slot option.  The applied
     method should create and return a method that is specialized for
     instances of type CLASS and uses the set closure to set the slot’s
     value.  ‘initialize’ then uses ‘add-method!’ to add the returned
     method to the generic function named by the slot definition’s
     ‘#:setter’ or ‘#:accessor’ option.

8.11.6 Customizing Class Definition
-----------------------------------

If the metaclass of the new class is something more specialized than the
default ‘<class>’, then the type of CLASS in the calls above is more
specialized than ‘<class>’, and hence it becomes possible to define
generic function methods, specialized for the new class’s metaclass,
that can modify or override the default behaviour of ‘initialize’,
‘compute-cpl’ or ‘compute-get-n-set’.

   ‘compute-cpl’ computes the class precedence list (“CPL”) for the new
class (*note Class Precedence List::), and returns it as a list of class
objects.  The CPL is important because it defines a superclass ordering
that is used, when a generic function is invoked upon an instance of the
class, to decide which of the available generic function methods is the
most specific.  Hence ‘compute-cpl’ could be customized in order to
modify the CPL ordering algorithm for all classes with a special
metaclass.

   The default CPL algorithm is encapsulated by the ‘compute-std-cpl’
procedure, which is called by the default ‘compute-cpl’ method.

 -- procedure: compute-std-cpl class
     Compute and return the class precedence list for CLASS according to
     the algorithm described in *note Class Precedence List::.

   ‘compute-slots’ computes and returns a list of all slot definitions
for the new class.  By default, this list includes the direct slot
definitions from the ‘define-class’ form, plus the slot definitions that
are inherited from the new class’s superclasses.  The default
‘compute-slots’ method uses the CPL computed by ‘compute-cpl’ to
calculate this union of slot definitions, with the rule that slots
inherited from superclasses are shadowed by direct slots with the same
name.  One possible reason for customizing ‘compute-slots’ would be to
implement an alternative resolution strategy for slot name conflicts.

   ‘compute-get-n-set’ computes the low-level closures that will be used
to get and set the value of a particular slot, and returns them in a
list with two elements.

   The closures returned depend on how storage for that slot is
allocated.  The standard ‘compute-get-n-set’ method, specialized for
classes of type ‘<class>’, handles the standard GOOPS values for the
‘#:allocation’ slot option (*note allocation: Slot Options.).  By
defining a new ‘compute-get-n-set’ method for a more specialized
metaclass, it is possible to support new types of slot allocation.

   Suppose you wanted to create a large number of instances of some
class with a slot that should be shared between some but not all
instances of that class - say every 10 instances should share the same
slot storage.  The following example shows how to implement and use a
new type of slot allocation to do this.

     (define-class <batched-allocation-metaclass> (<class>))

     (let ((batch-allocation-count 0)
           (batch-get-n-set #f))
       (define-method (compute-get-n-set
                          (class <batched-allocation-metaclass>) s)
         (case (slot-definition-allocation s)
           ((#:batched)
            ;; If we've already used the same slot storage for 10 instances,
            ;; reset variables.
            (if (= batch-allocation-count 10)
                (begin
                  (set! batch-allocation-count 0)
                  (set! batch-get-n-set #f)))
            ;; If we don't have a current pair of get and set closures,
            ;; create one.  make-closure-variable returns a pair of closures
            ;; around a single Scheme variable - see goops.scm for details.
            (or batch-get-n-set
                (set! batch-get-n-set (make-closure-variable)))
            ;; Increment the batch allocation count.
            (set! batch-allocation-count (+ batch-allocation-count 1))
            batch-get-n-set)

           ;; Call next-method to handle standard allocation types.
           (else (next-method)))))

     (define-class <class-using-batched-slot> ()
       ...
       (c #:allocation #:batched)
       ...
       #:metaclass <batched-allocation-metaclass>)

   The usage of ‘compute-getter-method’ and ‘compute-setter-method’ is
described in *note Class Definition Protocol::.

   ‘compute-cpl’ and ‘compute-get-n-set’ are called by the standard
‘initialize’ method for classes whose metaclass is ‘<class>’.  But
‘initialize’ itself can also be modified, by defining an ‘initialize’
method specialized to the new class’s metaclass.  Such a method could
complete override the standard behaviour, by not calling ‘(next-method)’
at all, but more typically it would perform additional class
initialization steps before and/or after calling ‘(next-method)’ for the
standard behaviour.

8.11.7 Method Definition
------------------------

‘define-method’ (syntax)

   • ‘add-method! TARGET METHOD’ (generic)

‘define-method’ invokes the ‘add-method!’ generic function to handle
adding the new method to a variety of possible targets.  GOOPS includes
methods to handle TARGET as

   • a generic function (the most common case)

   • a procedure

   • a primitive generic (*note Extending Primitives::)

   By defining further methods for ‘add-method!’, you can theoretically
handle adding methods to further types of target.

8.11.8 Method Definition Internals
----------------------------------

‘define-method’:

   • checks the form of the first parameter, and applies the following
     steps to the accessor’s setter if it has the ‘(setter …)’ form

   • interpolates a call to ‘define-generic’ or ‘define-accessor’ if a
     generic function is not already defined with the supplied name

   • calls ‘method’ with the PARAMETERs and BODY, to make a new method
     instance

   • calls ‘add-method!’ to add this method to the relevant generic
     function.

 -- syntax: method (parameter …) body …
     Make a method whose specializers are defined by the classes in
     PARAMETERs and whose procedure definition is constructed from the
     PARAMETER symbols and BODY forms.

     The PARAMETER and BODY parameters should be as for ‘define-method’
     (*note define-method: Methods and Generic Functions.).

‘method’:

   • extracts formals and specializing classes from the PARAMETERs,
     defaulting the class for unspecialized parameters to ‘<top>’

   • creates a closure using the formals and the BODY forms

   • calls ‘make’ with metaclass ‘<method>’ and the specializers and
     closure using the ‘#:specializers’ and ‘#:procedure’ keywords.

 -- procedure: make-method specializers procedure
     Make a method using SPECIALIZERS and PROCEDURE.

     SPECIALIZERS should be a list of classes that specifies the
     parameter combinations to which this method will be applicable.

     PROCEDURE should be the closure that will applied to the generic
     function parameters when this method is invoked.

‘make-method’ is a simple wrapper around ‘make’ with metaclass
‘<method>’.

 -- generic: add-method! target method
     Generic function for adding method METHOD to TARGET.

 -- method: add-method! (generic <generic>) (method <method>)
     Add method METHOD to the generic function GENERIC.

 -- method: add-method! (proc <procedure>) (method <method>)
     If PROC is a procedure with generic capability (*note
     generic-capability?: Extending Primitives.), upgrade it to a
     primitive generic and add METHOD to its generic function
     definition.

 -- method: add-method! (pg <primitive-generic>) (method <method>)
     Add method METHOD to the generic function definition of PG.

     Implementation: ‘(add-method! (primitive-generic-generic pg)
     method)’.

 -- method: add-method! (whatever <top>) (method <method>)
     Raise an error indicating that WHATEVER is not a valid generic
     function.

8.11.9 Generic Function Internals
---------------------------------

‘define-generic’ calls ‘ensure-generic’ to upgrade a pre-existing
procedure value, or ‘make’ with metaclass ‘<generic>’ to create a new
generic function.

   ‘define-accessor’ calls ‘ensure-accessor’ to upgrade a pre-existing
procedure value, or ‘make-accessor’ to create a new accessor.

 -- procedure: ensure-generic old-definition [name]
     Return a generic function with name NAME, if possible by using or
     upgrading OLD-DEFINITION.  If unspecified, NAME defaults to ‘#f’.

     If OLD-DEFINITION is already a generic function, it is returned
     unchanged.

     If OLD-DEFINITION is a Scheme procedure or procedure-with-setter,
     ‘ensure-generic’ returns a new generic function that uses
     OLD-DEFINITION for its default procedure and setter.

     Otherwise ‘ensure-generic’ returns a new generic function with no
     defaults and no methods.

 -- procedure: make-generic [name]
     Return a new generic function with name ‘(car NAME)’.  If
     unspecified, NAME defaults to ‘#f’.

   ‘ensure-generic’ calls ‘make’ with metaclasses ‘<generic>’ and
‘<generic-with-setter>’, depending on the previous value of the variable
that it is trying to upgrade.

   ‘make-generic’ is a simple wrapper for ‘make’ with metaclass
‘<generic>’.

 -- procedure: ensure-accessor proc [name]
     Return an accessor with name NAME, if possible by using or
     upgrading PROC.  If unspecified, NAME defaults to ‘#f’.

     If PROC is already an accessor, it is returned unchanged.

     If PROC is a Scheme procedure, procedure-with-setter or generic
     function, ‘ensure-accessor’ returns an accessor that reuses the
     reusable elements of PROC.

     Otherwise ‘ensure-accessor’ returns a new accessor with no defaults
     and no methods.

 -- procedure: make-accessor [name]
     Return a new accessor with name ‘(car NAME)’.  If unspecified, NAME
     defaults to ‘#f’.

   ‘ensure-accessor’ calls ‘make’ with metaclass
‘<generic-with-setter>’, as well as calls to ‘ensure-generic’,
‘make-accessor’ and (tail recursively) ‘ensure-accessor’.

   ‘make-accessor’ calls ‘make’ twice, first with metaclass ‘<generic>’
to create a generic function for the setter, then with metaclass
‘<generic-with-setter>’ to create the accessor, passing the setter
generic function as the value of the ‘#:setter’ keyword.

8.11.10 Generic Function Invocation
-----------------------------------

There is a detailed and customizable protocol involved in the process of
invoking a generic function — i.e., in the process of deciding which of
the generic function’s methods are applicable to the current arguments,
and which one of those to apply.  Here is a summary diagram of the
generic functions involved.

‘apply-generic’ (generic)

   • ‘no-method’ (generic)

   • ‘compute-applicable-methods’ (generic)

   • ‘sort-applicable-methods’ (generic)

        • ‘method-more-specific?’ (generic)

   • ‘apply-methods’ (generic)

        • ‘apply-method’ (generic)

        • ‘no-next-method’ (generic)

   • ‘no-applicable-method’

   We do not yet have full documentation for these.  Please refer to the
code (‘oop/goops.scm’) for details.

8.12 Redefining a Class
=======================

Suppose that a class ‘<my-class>’ is defined using ‘define-class’ (*note
define-class: Class Definition.), with slots that have accessor
functions, and that an application has created several instances of
‘<my-class>’ using ‘make’ (*note make: Instance Creation.).  What then
happens if ‘<my-class>’ is redefined by calling ‘define-class’ again?

8.12.1 Default Class Redefinition Behaviour
-------------------------------------------

GOOPS’ default answer to this question is as follows.

   • All existing direct instances of ‘<my-class>’ are converted to be
     instances of the new class.  This is achieved by preserving the
     values of slots that exist in both the old and new definitions, and
     initializing the values of new slots in the usual way (*note make:
     Instance Creation.).

   • All existing subclasses of ‘<my-class>’ are redefined, as though
     the ‘define-class’ expressions that defined them were re-evaluated
     following the redefinition of ‘<my-class>’, and the class
     redefinition process described here is applied recursively to the
     redefined subclasses.

   • Once all of its instances and subclasses have been updated, the
     class metaobject previously bound to the variable ‘<my-class>’ is
     no longer needed and so can be allowed to be garbage collected.

   To keep things tidy, GOOPS also needs to do a little housekeeping on
methods that are associated with the redefined class.

   • Slot accessor methods for slots in the old definition should be
     removed from their generic functions.  They will be replaced by
     accessor methods for the slots of the new class definition.

   • Any generic function method that uses the old ‘<my-class>’
     metaobject as one of its formal parameter specializers must be
     updated to refer to the new ‘<my-class>’ metaobject.  (Whenever a
     new generic function method is defined, ‘define-method’ adds the
     method to a list stored in the class metaobject for each class used
     as a formal parameter specializer, so it is easy to identify all
     the methods that must be updated when a class is redefined.)

   If this class redefinition strategy strikes you as rather
counter-intuitive, bear in mind that it is derived from similar
behaviour in other object systems such as CLOS, and that experience in
those systems has shown it to be very useful in practice.

   Also bear in mind that, like most of GOOPS’ default behaviour, it can
be customized…

8.12.2 Customizing Class Redefinition
-------------------------------------

When ‘define-class’ notices that a class is being redefined, it
constructs the new class metaobject as usual, then invokes the
‘class-redefinition’ generic function with the old and new classes as
arguments.  Therefore, if the old or new classes have metaclasses other
than the default ‘<class>’, class redefinition behaviour can be
customized by defining a ‘class-redefinition’ method that is specialized
for the relevant metaclasses.

 -- generic: class-redefinition
     Handle the class redefinition from OLD-CLASS to NEW-CLASS, and
     return the new class metaobject that should be bound to the
     variable specified by ‘define-class’’s first argument.

 -- method: class-redefinition (old-class <class>) (new-class <class>)
     Implements GOOPS’ default class redefinition behaviour, as
     described in *note Default Class Redefinition Behaviour::.  Returns
     the metaobject for the new class definition.

   The default ‘class-redefinition’ method, for classes with the default
metaclass ‘<class>’, calls the following generic functions, which could
of course be individually customized.

 -- generic: remove-class-accessors! old
     The default ‘remove-class-accessors!’ method removes the accessor
     methods of the old class from all classes which they specialize.

 -- generic: update-direct-method! method old new
     The default ‘update-direct-method!’ method substitutes the new
     class for the old in all methods specialized to the old class.

 -- generic: update-direct-subclass! subclass old new
     The default ‘update-direct-subclass!’ method invokes
     ‘class-redefinition’ recursively to handle the redefinition of
     subclasses.

   An alternative class redefinition strategy could be to leave all
existing instances as instances of the old class, but accepting that the
old class is now “nameless”, since its name has been taken over by the
new definition.  In this strategy, any existing subclasses could also be
left as they are, on the understanding that they inherit from a nameless
superclass.

   This strategy is easily implemented in GOOPS, by defining a new
metaclass, that will be used as the metaclass for all classes to which
the strategy should apply, and then defining a ‘class-redefinition’
method that is specialized for this metaclass:

     (define-class <can-be-nameless> (<class>))

     (define-method (class-redefinition (old <can-be-nameless>)
                                        (new <class>))
       new)

   When customization can be as easy as this, aren’t you glad that GOOPS
implements the far more difficult strategy as its default!

8.13 Changing the Class of an Instance
======================================

When a class is redefined, any existing instance of the redefined class
will be modified for the new class definition before the next time that
any of the instance’s slots is referenced or set.  GOOPS modifies each
instance by calling the generic function ‘change-class’.

   More generally, you can change the class of an existing instance at
any time by invoking the generic function ‘change-class’ with two
arguments: the instance and the new class.

   The default method for ‘change-class’ decides how to implement the
change of class by looking at the slot definitions for the instance’s
existing class and for the new class.  If the new class has slots with
the same name as slots in the existing class, the values for those slots
are preserved.  Slots that are present only in the existing class are
discarded.  Slots that are present only in the new class are initialized
using the corresponding slot definition’s init function (*note
slot-init-function: Classes.).

 -- generic: change-class instance new-class

 -- method: change-class (obj <object>) (new <class>)
     Modify instance OBJ to make it an instance of class NEW.

     The value of each of OBJ’s slots is preserved only if a similarly
     named slot exists in NEW; any other slot values are discarded.

     The slots in NEW that do not correspond to any of OBJ’s
     pre-existing slots are initialized according to NEW’s slot
     definitions’ init functions.

   The default ‘change-class’ method also invokes another generic
function, ‘update-instance-for-different-class’, as the last thing that
it does before returning.  The applied
‘update-instance-for-different-class’ method can make any further
adjustments to NEW-INSTANCE that are required to complete or modify the
change of class.  The return value from the applied method is ignored.

 -- generic: update-instance-for-different-class old-instance
          new-instance
     A generic function that can be customized to put finishing touches
     to an instance whose class has just been changed.  The default
     ‘update-instance-for-different-class’ method does nothing.

   Customized change of class behaviour can be implemented by defining
‘change-class’ methods that are specialized either by the class of the
instances to be modified or by the metaclass of the new class.

