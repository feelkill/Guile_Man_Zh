SXPath: SXML Query Language
===========================

SXPath is a query language for SXML, an instance of XML Information set
(Infoset) in the form of s-expressions.  See ‘(sxml ssax)’ for the
definition of SXML and more details.  SXPath is also a translation into
Scheme of an XML Path Language, XPath (http://www.w3.org/TR/xpath).
XPath and SXPath describe means of selecting a set of Infoset’s items or
their properties.

   To facilitate queries, XPath maps the XML Infoset into an explicit
tree, and introduces important notions of a location path and a current,
context node.  A location path denotes a selection of a set of nodes
relative to a context node.  Any XPath tree has a distinguished, root
node – which serves as the context node for absolute location paths.
Location path is recursively defined as a location step joined with a
location path.  A location step is a simple query of the database
relative to a context node.  A step may include expressions that further
filter the selected set.  Each node in the resulting set is used as a
context node for the adjoining location path.  The result of the step is
a union of the sets returned by the latter location paths.

   The SXML representation of the XML Infoset (see SSAX.scm) is rather
suitable for querying as it is.  Bowing to the XPath specification, we
will refer to SXML information items as ’Nodes’:

      	<Node> ::= <Element> | <attributes-coll> | <attrib>
      		   | "text string" | <PI>

   This production can also be described as

     	<Node> ::= (name . <Nodeset>) | "text string"

   An (ordered) set of nodes is just a list of the constituent nodes:

      	<Nodeset> ::= (<Node> ...)

   Nodesets, and Nodes other than text strings are both lists.  A
<Nodeset> however is either an empty list, or a list whose head is not a
symbol.  A symbol at the head of a node is either an XML name (in which
case it’s a tag of an XML element), or an administrative name such as
’@’.  This uniform list representation makes processing rather simple
and elegant, while avoiding confusion.  The multi-branch tree structure
formed by the mutually-recursive datatypes <Node> and <Nodeset> lends
itself well to processing by functional languages.

   A location path is in fact a composite query over an XPath tree or
its branch.  A singe step is a combination of a projection, selection or
a transitive closure.  Multiple steps are combined via join and union
operations.  This insight allows us to _elegantly_ implement XPath as a
sequence of projection and filtering primitives – converters – joined by
"combinators".  Each converter takes a node and returns a nodeset which
is the result of the corresponding query relative to that node.  A
converter can also be called on a set of nodes.  In that case it returns
a union of the corresponding queries over each node in the set.  The
union is easily implemented as a list append operation as all nodes in a
SXML tree are considered distinct, by XPath conventions.  We also
preserve the order of the members in the union.  Query combinators are
high-order functions: they take converter(s) (which is a Node|Nodeset ->
Nodeset function) and compose or otherwise combine them.  We will be
concerned with only relative location paths [XPath]: an absolute
location path is a relative path applied to the root node.

   Similarly to XPath, SXPath defines full and abbreviated notations for
location paths.  In both cases, the abbreviated notation can be
mechanically expanded into the full form by simple rewriting rules.  In
case of SXPath the corresponding rules are given as comments to a sxpath
function, below.  The regression test suite at the end of this file
shows a representative sample of SXPaths in both notations, juxtaposed
with the corresponding XPath expressions.  Most of the samples are
borrowed literally from the XPath specification, while the others are
adjusted for our running example, tree1.

7.22.6.2 Usage
..............

 -- Scheme Procedure: nodeset? x

 -- Scheme Procedure: node-typeof? crit

 -- Scheme Procedure: node-eq? other

 -- Scheme Procedure: node-equal? other

 -- Scheme Procedure: node-pos n

 -- Scheme Procedure: filter pred?
      -- Scheme Procedure: filter pred list
          Return all the elements of 2nd arg LIST that satisfy predicate
          PRED.  The list is not disordered - elements that appear in the
          result list occur in the same order as they occur in the argument
          list.  The returned list may share a common tail with the argument
          list.  The dynamic order in which the various applications of pred
          are made is not specified.

               (filter even? '(0 7 8 8 43 -4)) => (0 8 8 -4)



 -- Scheme Procedure: take-until pred?

 -- Scheme Procedure: take-after pred?

 -- Scheme Procedure: map-union proc lst

 -- Scheme Procedure: node-reverse node-or-nodeset

 -- Scheme Procedure: node-trace title

 -- Scheme Procedure: select-kids test-pred?

 -- Scheme Procedure: node-self pred?
      -- Scheme Procedure: filter pred list
          Return all the elements of 2nd arg LIST that satisfy predicate
          PRED.  The list is not disordered - elements that appear in the
          result list occur in the same order as they occur in the argument
          list.  The returned list may share a common tail with the argument
          list.  The dynamic order in which the various applications of pred
          are made is not specified.

               (filter even? '(0 7 8 8 43 -4)) => (0 8 8 -4)



 -- Scheme Procedure: node-join . selectors

 -- Scheme Procedure: node-reduce . converters

 -- Scheme Procedure: node-or . converters

 -- Scheme Procedure: node-closure test-pred?

 -- Scheme Procedure: node-parent rootnode

 -- Scheme Procedure: sxpath path

7.22.7 (sxml ssax input-parse)
------------------------------

7.22.7.1 Overview
.................

A simple lexer.

   The procedures in this module surprisingly often suffice to parse an
input stream.  They either skip, or build and return tokens, according
to inclusion or delimiting semantics.  The list of characters to expect,
include, or to break at may vary from one invocation of a function to
another.  This allows the functions to easily parse even
context-sensitive languages.

   EOF is generally frowned on, and thrown up upon if encountered.
Exceptions are mentioned specifically.  The list of expected characters
(characters to skip until, or break-characters) may include an EOF
"character", which is to be coded as the symbol, ‘*eof*’.

   The input stream to parse is specified as a "port", which is usually
the last (and optional) argument.  It defaults to the current input port
if omitted.

   If the parser encounters an error, it will throw an exception to the
key ‘parser-error’.  The arguments will be of the form ‘(PORT MESSAGE
SPECIALISING-MSG*)’.

   The first argument is a port, which typically points to the offending
character or its neighborhood.  You can then use ‘port-column’ and
‘port-line’ to query the current position.  MESSAGE is the description
of the error.  Other arguments supply more details about the problem.

7.22.7.2 Usage
..............

 -- Scheme Procedure: peek-next-char [port]

 -- Scheme Procedure: assert-curr-char expected-chars comment [port]

 -- Scheme Procedure: skip-until arg [port]

 -- Scheme Procedure: skip-while skip-chars [port]

 -- Scheme Procedure: next-token prefix-skipped-chars break-chars
          [comment] [port]

 -- Scheme Procedure: next-token-of incl-list/pred [port]

 -- Scheme Procedure: read-text-line [port]

 -- Scheme Procedure: read-string n [port]

 -- Scheme Procedure: find-string-from-port? _ _ . _
     Looks for STR in <INPUT-PORT>, optionally within the first
     MAX-NO-CHAR characters.

7.22.8 (sxml apply-templates)
-----------------------------

7.22.8.1 Overview
.................

Pre-order traversal of a tree and creation of a new tree:

     	apply-templates:: tree x <templates> -> <new-tree>

   where

      <templates> ::= (<template> ...)
      <template>  ::= (<node-test> <node-test> ... <node-test> . <handler>)
      <node-test> ::= an argument to node-typeof? above
      <handler>   ::= <tree> -> <new-tree>

   This procedure does a _normal_, pre-order traversal of an SXML tree.
It walks the tree, checking at each node against the list of matching
templates.

   If the match is found (which must be unique, i.e., unambiguous), the
corresponding handler is invoked and given the current node as an
argument.  The result from the handler, which must be a ‘<tree>’, takes
place of the current node in the resulting tree.  The name of the
function is not accidental: it resembles rather closely an
‘apply-templates’ function of XSLT.

7.22.8.2 Usage
..............

 -- Scheme Procedure: apply-templates tree templates

