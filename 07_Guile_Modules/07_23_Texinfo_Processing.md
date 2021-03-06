7.23 Texinfo Processing
=======================

7.23.1 (texinfo)
----------------

7.23.1.1 Overview
.................

Texinfo processing in scheme
----------------------------

This module parses texinfo into SXML. TeX will always be the processor
of choice for print output, of course.  However, although ‘makeinfo’
works well for info, its output in other formats is not very
customizable, and the program is not extensible as a whole.  This module
aims to provide an extensible framework for texinfo processing that
integrates texinfo into the constellation of SXML processing tools.

Notes on the SXML vocabulary
----------------------------

Consider the following texinfo fragment:

      @deffn Primitive set-car! pair value
      This function...
      @end deffn

   Logically, the category (Primitive), name (set-car!), and arguments
(pair value) are “attributes” of the deffn, with the description as the
content.  However, texinfo allows for @-commands within the arguments to
an environment, like ‘@deffn’, which means that texinfo “attributes” are
PCDATA. XML attributes, on the other hand, are CDATA. For this reason,
“attributes” of texinfo @-commands are called “arguments”, and are
grouped under the special element, ‘%’.

   Because ‘%’ is not a valid NCName, stexinfo is a superset of SXML. In
the interests of interoperability, this module provides a conversion
function to replace the ‘%’ with ‘texinfo-arguments’.

7.23.1.2 Usage
..............

 -- Function: call-with-file-and-dir filename proc
     Call the one-argument procedure PROC with an input port that reads
     from FILENAME.  During the dynamic extent of PROC’s execution, the
     current directory will be ‘(dirname FILENAME)’.  This is useful for
     parsing documents that can include files by relative path name.

 -- Variable: texi-command-specs

 -- Function: texi-command-depth command max-depth
     Given the texinfo command COMMAND, return its nesting level, or
     ‘#f’ if it nests too deep for MAX-DEPTH.

     Examples:

           (texi-command-depth 'chapter 4)        ⇒ 1
           (texi-command-depth 'top 4)            ⇒ 0
           (texi-command-depth 'subsection 4)     ⇒ 3
           (texi-command-depth 'appendixsubsec 4) ⇒ 3
           (texi-command-depth 'subsection 2)     ⇒ #f

 -- Function: texi-fragment->stexi string-or-port
     Parse the texinfo commands in STRING-OR-PORT, and return the
     resultant stexi tree.  The head of the tree will be the special
     command, ‘*fragment*’.

 -- Function: texi->stexi port
     Read a full texinfo document from PORT and return the parsed stexi
     tree.  The parsing will start at the ‘@settitle’ and end at ‘@bye’
     or EOF.

 -- Function: stexi->sxml tree
     Transform the stexi tree TREE into sxml.  This involves replacing
     the ‘%’ element that keeps the texinfo arguments with an element
     for each argument.

     FIXME: right now it just changes % to ‘texinfo-arguments’ – that
     doesn’t hang with the idea of making a dtd at some point

7.23.2 (texinfo docbook)
------------------------

7.23.2.1 Overview
.................

This module exports procedures for transforming a limited subset of the
SXML representation of docbook into stexi.  It is not complete by any
means.  The intention is to gather a number of routines and stylesheets
so that external modules can parse specific subsets of docbook, for
example that set generated by certain tools.

7.23.2.2 Usage
..............

 -- Variable: *sdocbook->stexi-rules*

 -- Variable: *sdocbook-block-commands*

 -- Function: sdocbook-flatten sdocbook
     "Flatten" a fragment of sdocbook so that block elements do not nest
     inside each other.

     Docbook is a nested format, where e.g.  a ‘refsect2’ normally
     appears inside a ‘refsect1’.  Logical divisions in the document are
     represented via the tree topology; a ‘refsect2’ element _contains_
     all of the elements in its section.

     On the contrary, texinfo is a flat format, in which sections are
     marked off by standalone section headers like ‘@subsection’, and
     block elements do not nest inside each other.

     This function takes a nested sdocbook fragment SDOCBOOK and
     flattens all of the sections, such that e.g.

           (refsect1 (refsect2 (para "Hello")))

     becomes

           ((refsect1) (refsect2) (para "Hello"))

     Oftentimes (always?)  sectioning elements have ‘<title>’ as their
     first element child; users interested in processing the ‘refsect*’
     elements into proper sectioning elements like ‘chapter’ might be
     interested in ‘replace-titles’ and ‘filter-empty-elements’.  *Note
     replace-titles: texinfo docbook replace-titles, and *note
     filter-empty-elements: texinfo docbook filter-empty-elements.

     Returns a nodeset; that is to say, an untagged list of stexi
     elements.  *Note SXPath::, for the definition of a nodeset.

 -- Function: filter-empty-elements sdocbook
     Filters out empty elements in an sdocbook nodeset.  Mostly useful
     after running ‘sdocbook-flatten’.

 -- Function: replace-titles sdocbook-fragment
     Iterate over the sdocbook nodeset SDOCBOOK-FRAGMENT, transforming
     contiguous ‘refsect’ and ‘title’ elements into the appropriate
     texinfo sectioning command.  Most useful after having run
     ‘sdocbook-flatten’.

     For example:

           (replace-titles '((refsect1) (title "Foo") (para "Bar.")))
              ⇒ '((chapter "Foo") (para "Bar."))

7.23.3 (texinfo html)
---------------------

7.23.3.1 Overview
.................

This module implements transformation from ‘stexi’ to HTML. Note that
the output of ‘stexi->shtml’ is actually SXML with the HTML vocabulary.
This means that the output can be further processed, and that it must
eventually be serialized by ‘sxml->xml’.  *Note Reading and Writing
XML::.

   References (i.e., the ‘@ref’ family of commands) are resolved by a
"ref-resolver".  *Note add-ref-resolver!: texinfo html
add-ref-resolver!.

7.23.3.2 Usage
..............

 -- Function: add-ref-resolver! proc
     Add PROC to the head of the list of ref-resolvers.  PROC will be
     expected to take the name of a node and the name of a manual and
     return the URL of the referent, or ‘#f’ to pass control to the next
     ref-resolver in the list.

     The default ref-resolver will return the concatenation of the
     manual name, ‘#’, and the node name.

 -- Function: stexi->shtml tree
     Transform the stexi TREE into shtml, resolving references via
     ref-resolvers.  See the module commentary for more details.

 -- Function: urlify str

7.23.4 (texinfo indexing)
-------------------------

7.23.4.1 Overview
.................

Given a piece of stexi, return an index of a specified variety.

   Note that currently, ‘stexi-extract-index’ doesn’t differentiate
between different kinds of index entries.  That’s a bug ;)

7.23.4.2 Usage
..............

 -- Function: stexi-extract-index tree manual-name kind
     Given an stexi tree TREE, index all of the entries of type KIND.
     KIND can be one of the predefined texinfo indices (‘concept’,
     ‘variable’, ‘function’, ‘key’, ‘program’, ‘type’) or one of the
     special symbols ‘auto’ or ‘all’.  ‘auto’ will scan the stext for a
     ‘(printindex)’ statement, and ‘all’ will generate an index from all
     entries, regardless of type.

     The returned index is a list of pairs, the CAR of which is the
     entry (a string) and the CDR of which is a node name (a string).

7.23.5 (texinfo string-utils)
-----------------------------

7.23.5.1 Overview
.................

Module ‘(texinfo string-utils)’ provides various string-related
functions useful to Guile’s texinfo support.

7.23.5.2 Usage
..............

 -- Function: escape-special-chars str special-chars escape-char
     Returns a copy of STR with all given special characters preceded by
     the given ESCAPE-CHAR.

     SPECIAL-CHARS can either be a single character, or a string
     consisting of all the special characters.

          ;; make a string regexp-safe...
           (escape-special-chars "***(Example String)***"
                                "[]()/*."
                                #\\)
          => "\\*\\*\\*\\(Example String\\)\\*\\*\\*"

          ;; also can escape a singe char...
           (escape-special-chars "richardt@vzavenue.net"
                                #\@
                                #\@)
          => "richardt@@vzavenue.net"

 -- Function: transform-string str match? replace [start] [end]
     Uses MATCH? against each character in STR, and performs a
     replacement on each character for which matches are found.

     MATCH? may either be a function, a character, a string, or ‘#t’.
     If MATCH? is a function, then it takes a single character as input,
     and should return ‘#t’ for matches.  MATCH? is a character, it is
     compared to each string character using ‘char=?’.  If MATCH? is a
     string, then any character in that string will be considered a
     match.  ‘#t’ will cause every character to be a match.

     If REPLACE is a function, it is called with the matched character
     as an argument, and the returned value is sent to the output string
     via ‘display’.  If REPLACE is anything else, it is sent through the
     output string via ‘display’.

     Note that te replacement for the matched characters does not need
     to be a single character.  That is what differentiates this
     function from ‘string-map’, and what makes it useful for
     applications such as converting ‘#\&’ to ‘"&amp;"’ in web page
     text.  Some other functions in this module are just wrappers around
     common uses of ‘transform-string’.  Transformations not possible
     with this function should probably be done with regular
     expressions.

     If START and END are given, they control which portion of the
     string undergoes transformation.  The entire input string is still
     output, though.  So, if START is ‘5’, then the first five
     characters of STR will still appear in the returned string.

          ; these two are equivalent...
           (transform-string str #\space #\-) ; change all spaces to -'s
           (transform-string str (lambda (c) (char=? #\space c)) #\-)

 -- Function: expand-tabs str [tab-size]
     Returns a copy of STR with all tabs expanded to spaces.  TAB-SIZE
     defaults to 8.

     Assuming tab size of 8, this is equivalent to:

           (transform-string str #\tab "        ")

 -- Function: center-string str [width] [chr] [rchr]
     Returns a copy of STR centered in a field of WIDTH characters.  Any
     needed padding is done by character CHR, which defaults to
     ‘#\space’.  If RCHR is provided, then the padding to the right will
     use it instead.  See the examples below.  left and RCHR on the
     right.  The default WIDTH is 80.  The default CHR and RCHR is
     ‘#\space’.  The string is never truncated.

           (center-string "Richard Todd" 24)
          => "      Richard Todd      "

           (center-string " Richard Todd " 24 #\=)
          => "===== Richard Todd ====="

           (center-string " Richard Todd " 24 #\< #\>)
          => "<<<<< Richard Todd >>>>>"

 -- Function: left-justify-string str [width] [chr]
     ‘left-justify-string str [width chr]’.  Returns a copy of STR
     padded with CHR such that it is left justified in a field of WIDTH
     characters.  The default WIDTH is 80.  Unlike ‘string-pad’ from
     srfi-13, the string is never truncated.

 -- Function: right-justify-string str [width] [chr]
     Returns a copy of STR padded with CHR such that it is right
     justified in a field of WIDTH characters.  The default WIDTH is 80.
     The default CHR is ‘#\space’.  Unlike ‘string-pad’ from srfi-13,
     the string is never truncated.

 -- Function: collapse-repeated-chars str [chr] [num]
     Returns a copy of STR with all repeated instances of CHR collapsed
     down to at most NUM instances.  The default value for CHR is
     ‘#\space’, and the default value for NUM is 1.

           (collapse-repeated-chars "H  e  l  l  o")
          => "H e l l o"
           (collapse-repeated-chars "H--e--l--l--o" #\-)
          => "H-e-l-l-o"
           (collapse-repeated-chars "H-e--l---l----o" #\- 2)
          => "H-e--l--l--o"

 -- Function: make-text-wrapper [#:line-width] [#:expand-tabs?]
          [#:tab-width] [#:collapse-whitespace?] [#:subsequent-indent]
          [#:initial-indent] [#:break-long-words?]
     Returns a procedure that will split a string into lines according
     to the given parameters.

     ‘#:line-width’
          This is the target length used when deciding where to wrap
          lines.  Default is 80.

     ‘#:expand-tabs?’
          Boolean describing whether tabs in the input should be
          expanded.  Default is #t.

     ‘#:tab-width’
          If tabs are expanded, this will be the number of spaces to
          which they expand.  Default is 8.

     ‘#:collapse-whitespace?’
          Boolean describing whether the whitespace inside the existing
          text should be removed or not.  Default is #t.

          If text is already well-formatted, and is just being wrapped
          to fit in a different width, then set this to ‘#f’.  This way,
          many common text conventions (such as two spaces between
          sentences) can be preserved if in the original text.  If the
          input text spacing cannot be trusted, then leave this setting
          at the default, and all repeated whitespace will be collapsed
          down to a single space.

     ‘#:initial-indent’
          Defines a string that will be put in front of the first line
          of wrapped text.  Default is the empty string, “”.

     ‘#:subsequent-indent’
          Defines a string that will be put in front of all lines of
          wrapped text, except the first one.  Default is the empty
          string, “”.

     ‘#:break-long-words?’
          If a single word is too big to fit on a line, this setting
          tells the wrapper what to do.  Defaults to #t, which will
          break up long words.  When set to #f, the line will be
          allowed, even though it is longer than the defined
          ‘#:line-width’.

     The return value is a procedure of one argument, the input string,
     which returns a list of strings, where each element of the list is
     one line.

 -- Function: fill-string str . kwargs
     Wraps the text given in string STR according to the parameters
     provided in KWARGS, or the default setting if they are not given.
     Returns a single string with the wrapped text.  Valid keyword
     arguments are discussed in ‘make-text-wrapper’.

 -- Function: string->wrapped-lines str . kwargs
     ‘string->wrapped-lines str keywds ...’.  Wraps the text given in
     string STR according to the parameters provided in KEYWDS, or the
     default setting if they are not given.  Returns a list of strings
     representing the formatted lines.  Valid keyword arguments are
     discussed in ‘make-text-wrapper’.

7.23.6 (texinfo plain-text)
---------------------------

7.23.6.1 Overview
.................

Transformation from stexi to plain-text.  Strives to re-create the
output from ‘info’; comes pretty damn close.

7.23.6.2 Usage
..............

 -- Function: stexi->plain-text tree
     Transform TREE into plain text.  Returns a string.

7.23.7 (texinfo serialize)
--------------------------

7.23.7.1 Overview
.................

Serialization of ‘stexi’ to plain texinfo.

7.23.7.2 Usage
..............

 -- Function: stexi->texi tree
     Serialize the stexi TREE into plain texinfo.

7.23.8 (texinfo reflection)
---------------------------

7.23.8.1 Overview
.................

Routines to generare ‘stexi’ documentation for objects and modules.

   Note that in this context, an "object" is just a value associated
with a location.  It has nothing to do with GOOPS.

7.23.8.2 Usage
..............

 -- Function: module-stexi-documentation sym-name [%docs-resolver]
          [#:docs-resolver]
     Return documentation for the module named SYM-NAME.  The
     documentation will be formatted as ‘stexi’ (*note texinfo:
     texinfo.).

 -- Function: script-stexi-documentation scriptpath
     Return documentation for given script.  The documentation will be
     taken from the script’s commentary, and will be returned in the
     ‘stexi’ format (*note texinfo: texinfo.).

 -- Function: object-stexi-documentation _ [_] [#:force]

 -- Function: package-stexi-standard-copying name version updated years
          copyright-holder permissions
     Create a standard texinfo ‘copying’ section.

     YEARS is a list of years (as integers) in which the modules being
     documented were released.  All other arguments are strings.

 -- Function: package-stexi-standard-titlepage name version updated
          authors
     Create a standard GNU title page.

     AUTHORS is a list of ‘(NAME . EMAIL)’ pairs.  All other arguments
     are strings.

     Here is an example of the usage of this procedure:

           (package-stexi-standard-titlepage
            "Foolib"
            "3.2"
            "26 September 2006"
            '(("Alyssa P Hacker" . "alyssa@example.com"))
            '(2004 2005 2006)
            "Free Software Foundation, Inc."
            "Standard GPL permissions blurb goes here")

 -- Function: package-stexi-generic-menu name entries
     Create a menu from a generic alist of entries, the car of which
     should be the node name, and the cdr the description.  As an
     exception, an entry of ‘#f’ will produce a separator.

 -- Function: package-stexi-standard-menu name modules
          module-descriptions extra-entries
     Create a standard top node and menu, suitable for processing by
     makeinfo.

 -- Function: package-stexi-extended-menu name module-pairs script-pairs
          extra-entries
     Create an "extended" menu, like the standard menu but with a
     section for scripts.

 -- Function: package-stexi-standard-prologue name filename category
          description copying titlepage menu
     Create a standard prologue, suitable for later serialization to
     texinfo and .info creation with makeinfo.

     Returns a list of stexinfo forms suitable for passing to
     ‘package-stexi-documentation’ as the prologue.  *Note texinfo
     reflection package-stexi-documentation::, *note
     package-stexi-standard-titlepage: texinfo reflection
     package-stexi-standard-titlepage, *note
     package-stexi-standard-copying: texinfo reflection
     package-stexi-standard-copying, and *note
     package-stexi-standard-menu: texinfo reflection
     package-stexi-standard-menu.

 -- Function: package-stexi-documentation modules name filename prologue
          epilogue [#:module-stexi-documentation-args] [#:scripts]
     Create stexi documentation for a "package", where a package is a
     set of modules that is released together.

     MODULES is expected to be a list of module names, where a module
     name is a list of symbols.  The stexi that is returned will be
     titled NAME and a texinfo filename of FILENAME.

     PROLOGUE and EPILOGUE are lists of stexi forms that will be spliced
     into the output document before and after the generated modules
     documentation, respectively.  *Note texinfo reflection
     package-stexi-standard-prologue::, to create a conventional GNU
     texinfo prologue.

     MODULE-STEXI-DOCUMENTATION-ARGS is an optional argument that, if
     given, will be added to the argument list when
     ‘module-texi-documentation’ is called.  For example, it might be
     useful to define a ‘#:docs-resolver’ argument.

 -- Function: package-stexi-documentation-for-include modules
          module-descriptions [#:module-stexi-documentation-args]
     Create stexi documentation for a "package", where a package is a
     set of modules that is released together.

     MODULES is expected to be a list of module names, where a module
     name is a list of symbols.  Returns an stexinfo fragment.

     Unlike ‘package-stexi-documentation’, this function simply produces
     a menu and the module documentations instead of producing a full
     texinfo document.  This can be useful if you write part of your
     manual by hand, and just use ‘@include’ to pull in the
     automatically generated parts.

     MODULE-STEXI-DOCUMENTATION-ARGS is an optional argument that, if
     given, will be added to the argument list when
     ‘module-texi-documentation’ is called.  For example, it might be
     useful to define a ‘#:docs-resolver’ argument.

