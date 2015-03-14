7.18 Curried Definitions
========================

The macros in this section are provided by
     (use-modules (ice-9 curried-definitions))
and replace those provided by default.

   Prior to Guile 2.0, Guile provided a type of definition known
colloquially as a “curried definition”.  The idea is to extend the
syntax of ‘define’ so that you can conveniently define procedures that
return procedures, up to any desired depth.

   For example,
     (define ((foo x) y)
       (list x y))
   is a convenience form of
     (define foo
       (lambda (x)
         (lambda (y)
           (list x y))))

 -- Scheme Syntax: define (… (name args …) …) body …
 -- Scheme Syntax: define* (… (name args …) …) body …
 -- Scheme Syntax: define-public (… (name args …) …) body …

     Create a top level variable NAME bound to the procedure with
     parameter list ARGS.  If NAME is itself a formal parameter list,
     then a higher order procedure is created using that
     formal-parameter list, and returning a procedure that has parameter
     list ARGS.  This nesting may occur to arbitrary depth.

     ‘define*’ is similar but the formal parameter lists take additional
     options as described in *note lambda* and define*::.  For example,
          (define* ((foo #:keys (bar 'baz) (quux 'zot)) frotz #:rest rest)
            (list bar quux frotz rest))

          ((foo #:quux 'foo) 1 2 3 4 5)
          ⇒ (baz foo 1 (2 3 4 5))

     ‘define-public’ is similar to ‘define’ but it also adds NAME to the
     list of exported bindings of the current module.

