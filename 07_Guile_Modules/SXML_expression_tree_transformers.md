SXML expression tree transformers
=================================

Pre-Post-order traversal of a tree and creation of a new tree
-------------------------------------------------------------

     pre-post-order:: <tree> x <bindings> -> <new-tree>

   where

      <bindings> ::= (<binding> ...)
      <binding> ::= (<trigger-symbol> *preorder* . <handler>) |
                    (<trigger-symbol> *macro* . <handler>) |
     		(<trigger-symbol> <new-bindings> . <handler>) |
     		(<trigger-symbol> . <handler>)
      <trigger-symbol> ::= XMLname | *text* | *default*
      <handler> :: <trigger-symbol> x [<tree>] -> <new-tree>

   The pre-post-order function visits the nodes and nodelists
pre-post-order (depth-first).  For each ‘<Node>’ of the form ‘(NAME
<Node> ...)’, it looks up an association with the given NAME among its
<BINDINGS>.  If failed, ‘pre-post-order’ tries to locate a ‘*default*’
binding.  It’s an error if the latter attempt fails as well.  Having
found a binding, the ‘pre-post-order’ function first checks to see if
the binding is of the form

     	(<trigger-symbol> *preorder* . <handler>)

   If it is, the handler is ’applied’ to the current node.  Otherwise,
the pre-post-order function first calls itself recursively for each
child of the current node, with <NEW-BINDINGS> prepended to the
<BINDINGS> in effect.  The result of these calls is passed to the
<HANDLER> (along with the head of the current <NODE>).  To be more
precise, the handler is _applied_ to the head of the current node and
its processed children.  The result of the handler, which should also be
a ‘<tree>’, replaces the current <NODE>.  If the current <NODE> is a
text string or other atom, a special binding with a symbol ‘*text*’ is
looked up.

   A binding can also be of a form

     	(<trigger-symbol> *macro* . <handler>)

   This is equivalent to ‘*preorder*’ described above.  However, the
result is re-processed again, with the current stylesheet.

7.22.4.2 Usage
..............

 -- Scheme Procedure: SRV:send-reply . fragments
     Output the FRAGMENTS to the current output port.

     The fragments are a list of strings, characters, numbers, thunks,
     ‘#f’, ‘#t’ – and other fragments.  The function traverses the tree
     depth-first, writes out strings and characters, executes thunks,
     and ignores ‘#f’ and ‘'()’.  The function returns ‘#t’ if anything
     was written at all; otherwise the result is ‘#f’ If ‘#t’ occurs
     among the fragments, it is not written out but causes the result of
     ‘SRV:send-reply’ to be ‘#t’.

 -- Scheme Procedure: foldts fdown fup fhere seed tree

 -- Scheme Procedure: post-order tree bindings

 -- Scheme Procedure: pre-post-order tree bindings

 -- Scheme Procedure: replace-range beg-pred end-pred forest

7.22.5 SXML Tree Fold
---------------------

7.22.5.1 Overview
.................

‘(sxml fold)’ defines a number of variants of the "fold" algorithm for
use in transforming SXML trees.  Additionally it defines the layout
operator, ‘fold-layout’, which might be described as a context-passing
variant of SSAX’s ‘pre-post-order’.

7.22.5.2 Usage
..............

 -- Scheme Procedure: foldt fup fhere tree
     The standard multithreaded tree fold.

     FUP is of type [a] -> a.  FHERE is of type object -> a.

 -- Scheme Procedure: foldts fdown fup fhere seed tree
     The single-threaded tree fold originally defined in SSAX. *Note
     SSAX::, for more information.

 -- Scheme Procedure: foldts* fdown fup fhere seed tree
     A variant of ‘foldts’ that allows pre-order tree rewrites.
     Originally defined in Andy Wingo’s 2007 paper, _Applications of
     fold to XML transformation_.

 -- Scheme Procedure: fold-values proc list . seeds
     A variant of ‘fold’ that allows multi-valued seeds.  Note that the
     order of the arguments differs from that of ‘fold’.  *Note SRFI-1
     Fold and Map::.

 -- Scheme Procedure: foldts*-values fdown fup fhere tree . seeds
     A variant of ‘foldts*’ that allows multi-valued seeds.  Originally
     defined in Andy Wingo’s 2007 paper, _Applications of fold to XML
     transformation_.

 -- Scheme Procedure: fold-layout tree bindings params layout stylesheet
     A traversal combinator in the spirit of ‘pre-post-order’.  *Note
     Transforming SXML::.

     ‘fold-layout’ was originally presented in Andy Wingo’s 2007 paper,
     _Applications of fold to XML transformation_.

          bindings := (<binding>...)
          binding  := (<tag> <bandler-pair>...)
                    | (*default* . <post-handler>)
                    | (*text* . <text-handler>)
          tag      := <symbol>
          handler-pair := (pre-layout . <pre-layout-handler>)
                    | (post . <post-handler>)
                    | (bindings . <bindings>)
                    | (pre . <pre-handler>)
                    | (macro . <macro-handler>)

     PRE-LAYOUT-HANDLER
          A function of three arguments:

          KIDS
               the kids of the current node, before traversal

          PARAMS
               the params of the current node

          LAYOUT
               the layout coming into this node

          PRE-LAYOUT-HANDLER is expected to use this information to
          return a layout to pass to the kids.  The default
          implementation returns the layout given in the arguments.

     POST-HANDLER
          A function of five arguments:

          TAG
               the current tag being processed

          PARAMS
               the params of the current node

          LAYOUT
               the layout coming into the current node, before any kids
               were processed

          KLAYOUT
               the layout after processing all of the children

          KIDS
               the already-processed child nodes

          POST-HANDLER should return two values, the layout to pass to
          the next node and the final tree.

     TEXT-HANDLER
          TEXT-HANDLER is a function of three arguments:

          TEXT
               the string

          PARAMS
               the current params

          LAYOUT
               the current layout

          TEXT-HANDLER should return two values, the layout to pass to
          the next node and the value to which the string should
          transform.

7.22.6 SXPath
-------------

7.22.6.1 Overview
.................

