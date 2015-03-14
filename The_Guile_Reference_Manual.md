The Guile Reference Manual
**************************

This manual documents Guile version 2.0.11.

   Copyright (C) 1996, 1997, 2000, 2001, 2002, 2003, 2004, 2005, 2009,
2010, 2011, 2012, 2013, 2014 Free Software Foundation.

   Permission is granted to copy, distribute and/or modify this document
under the terms of the GNU Free Documentation License, Version 1.3 or
any later version published by the Free Software Foundation; with no
Invariant Sections, no Front-Cover Texts, and no Back-Cover Texts.  A
copy of the license is included in the section entitled “GNU Free
Documentation License.”

The Guile Reference Manual
Preface
  Contributors to this Manual
  The Guile License
1 Introduction
  1.1 Guile and Scheme
  1.2 Combining with C Code
  1.3 Guile and the GNU Project
  1.4 Interactive Programming
  1.5 Supporting Multiple Languages
  1.6 Obtaining and Installing Guile
  1.7 Organisation of this Manual
  1.8 Typographical Conventions
2 Hello Guile!
  2.1 Running Guile Interactively
  2.2 Running Guile Scripts
  2.3 Linking Guile into Programs
  2.4 Writing Guile Extensions
  2.5 Using the Guile Module System
    2.5.1 Using Modules
    2.5.2 Writing new Modules
    2.5.3 Putting Extensions into Modules
  2.6 Reporting Bugs
3 Hello Scheme!
  3.1 Data Types, Values and Variables
    3.1.1 Latent Typing
    3.1.2 Values and Variables
    3.1.3 Defining and Setting Variables
  3.2 The Representation and Use of Procedures
    3.2.1 Procedures as Values
    3.2.2 Simple Procedure Invocation
    3.2.3 Creating and Using a New Procedure
    3.2.4 Lambda Alternatives
  3.3 Expressions and Evaluation
    3.3.1 Evaluating Expressions and Executing Programs
      3.3.1.1 Evaluating Literal Data
      3.3.1.2 Evaluating a Variable Reference
      3.3.1.3 Evaluating a Procedure Invocation Expression
      3.3.1.4 Evaluating Special Syntactic Expressions
    3.3.2 Tail calls
    3.3.3 Using the Guile REPL
    3.3.4 Summary of Common Syntax
  3.4 The Concept of Closure
    3.4.1 Names, Locations, Values and Environments
    3.4.2 Local Variables and Environments
    3.4.3 Environment Chaining
    3.4.4 Lexical Scope
      3.4.4.1 An Example of Non-Lexical Scoping
    3.4.5 Closure
    3.4.6 Example 1: A Serial Number Generator
    3.4.7 Example 2: A Shared Persistent Variable
    3.4.8 Example 3: The Callback Closure Problem
    3.4.9 Example 4: Object Orientation
  3.5 Further Reading
4 Programming in Scheme
  4.1 Guile’s Implementation of Scheme
  4.2 Invoking Guile
    4.2.1 Command-line Options
    4.2.2 Environment Variables
  4.3 Guile Scripting
    4.3.1 The Top of a Script File
    4.3.2 The Meta Switch
    4.3.3 Command Line Handling
    4.3.4 Scripting Examples
  4.4 Using Guile Interactively
    4.4.1 The Init File, ‘~/.guile’
    4.4.2 Readline
    4.4.3 Value History
    4.4.4 REPL Commands
      4.4.4.1 Help Commands
      4.4.4.2 Module Commands
      4.4.4.3 Language Commands
      4.4.4.4 Compile Commands
      4.4.4.5 Profile Commands
      4.4.4.6 Debug Commands
      4.4.4.7 Inspect Commands
      4.4.4.8 System Commands
    4.4.5 Error Handling
    4.4.6 Interactive Debugging
  4.5 Using Guile in Emacs
  4.6 Using Guile Tools
  4.7 Installing Site Packages
5 Programming in C
  5.1 Parallel Installations
  5.2 Linking Programs With Guile
    5.2.1 Guile Initialization Functions
    5.2.2 A Sample Guile Main Program
    5.2.3 Building the Example with Make
    5.2.4 Building the Example with Autoconf
  5.3 Linking Guile with Libraries
    5.3.1 A Sample Guile Extension
  5.4 General concepts for using libguile
    5.4.1 Dynamic Types
    5.4.2 Garbage Collection
    5.4.3 Control Flow
    5.4.4 Asynchronous Signals
    5.4.5 Multi-Threading
  5.5 Defining New Types (Smobs)
    5.5.1 Describing a New Type
    5.5.2 Creating Smob Instances
    5.5.3 Type checking
    5.5.4 Garbage Collecting Smobs
    5.5.5 Remembering During Operations
    5.5.6 Double Smobs
    5.5.7 The Complete Example
  5.6 Function Snarfing
  5.7 An Overview of Guile Programming
    5.7.1 How One Might Extend Dia Using Guile
      5.7.1.1 Deciding Why You Want to Add Guile
      5.7.1.2 Four Steps Required to Add Guile
      5.7.1.3 How to Represent Dia Data in Scheme
      5.7.1.4 Writing Guile Primitives for Dia
      5.7.1.5 Providing a Hook for the Evaluation of Scheme Code
      5.7.1.6 Top-level Structure of Guile-enabled Dia
      5.7.1.7 Going Further with Dia and Guile
    5.7.2 Why Scheme is More Hackable Than C
    5.7.3 Example: Using Guile for an Application Testbed
    5.7.4 A Choice of Programming Options
      5.7.4.1 What Functionality is Already Available?
      5.7.4.2 Functional and Performance Constraints
      5.7.4.3 Your Preferred Programming Style
      5.7.4.4 What Controls Program Execution?
    5.7.5 How About Application Users?
  5.8 Autoconf Support
    5.8.1 Autoconf Background
    5.8.2 Autoconf Macros
    5.8.3 Using Autoconf Macros
6 API Reference
  6.1 Overview of the Guile API
  6.2 Deprecation
  6.3 The SCM Type
  6.4 Initializing Guile
  6.5 Snarfing Macros
  6.6 Simple Generic Data Types
    6.6.1 Booleans
    6.6.2 Numerical data types
      6.6.2.1 Scheme’s Numerical “Tower”
      6.6.2.2 Integers
      6.6.2.3 Real and Rational Numbers
      6.6.2.4 Complex Numbers
      6.6.2.5 Exact and Inexact Numbers
      6.6.2.6 Read Syntax for Numerical Data
      6.6.2.7 Operations on Integer Values
      6.6.2.8 Comparison Predicates
      6.6.2.9 Converting Numbers To and From Strings
      6.6.2.10 Complex Number Operations
      6.6.2.11 Arithmetic Functions
      6.6.2.12 Scientific Functions
      6.6.2.13 Bitwise Operations
      6.6.2.14 Random Number Generation
    6.6.3 Characters
    6.6.4 Character Sets
      6.6.4.1 Character Set Predicates/Comparison
      6.6.4.2 Iterating Over Character Sets
      6.6.4.3 Creating Character Sets
      6.6.4.4 Querying Character Sets
      6.6.4.5 Character-Set Algebra
      6.6.4.6 Standard Character Sets
    6.6.5 Strings
      6.6.5.1 String Read Syntax
      6.6.5.2 String Predicates
      6.6.5.3 String Constructors
      6.6.5.4 List/String conversion
      6.6.5.5 String Selection
      6.6.5.6 String Modification
      6.6.5.7 String Comparison
      6.6.5.8 String Searching
      6.6.5.9 Alphabetic Case Mapping
      6.6.5.10 Reversing and Appending Strings
      6.6.5.11 Mapping, Folding, and Unfolding
      6.6.5.12 Miscellaneous String Operations
      6.6.5.13 Representing Strings as Bytes
      6.6.5.14 Conversion to/from C
      6.6.5.15 String Internals
    6.6.6 Bytevectors
      6.6.6.1 Endianness
      6.6.6.2 Manipulating Bytevectors
      6.6.6.3 Interpreting Bytevector Contents as Integers
      6.6.6.4 Converting Bytevectors to/from Integer Lists
      6.6.6.5 Interpreting Bytevector Contents as Floating Point Numbers
      6.6.6.6 Interpreting Bytevector Contents as Unicode Strings
      6.6.6.7 Accessing Bytevectors with the Array API
      6.6.6.8 Accessing Bytevectors with the SRFI-4 API
    6.6.7 Symbols
      6.6.7.1 Symbols as Discrete Data
      6.6.7.2 Symbols as Lookup Keys
      6.6.7.3 Symbols as Denoting Variables
      6.6.7.4 Operations Related to Symbols
      6.6.7.5 Function Slots and Property Lists
      6.6.7.6 Extended Read Syntax for Symbols
      6.6.7.7 Uninterned Symbols
    6.6.8 Keywords
      6.6.8.1 Why Use Keywords?
      6.6.8.2 Coding With Keywords
      6.6.8.3 Keyword Read Syntax
      6.6.8.4 Keyword Procedures
    6.6.9 “Functionality-Centric” Data Types
  6.7 Compound Data Types
    6.7.1 Pairs
    6.7.2 Lists
      6.7.2.1 List Read Syntax
      6.7.2.2 List Predicates
      6.7.2.3 List Constructors
      6.7.2.4 List Selection
      6.7.2.5 Append and Reverse
      6.7.2.6 List Modification
      6.7.2.7 List Searching
      6.7.2.8 List Mapping
    6.7.3 Vectors
      6.7.3.1 Read Syntax for Vectors
      6.7.3.2 Dynamic Vector Creation and Validation
      6.7.3.3 Accessing and Modifying Vector Contents
      6.7.3.4 Vector Accessing from C
      6.7.3.5 Uniform Numeric Vectors
    6.7.4 Bit Vectors
    6.7.5 Arrays
      6.7.5.1 Array Syntax
      6.7.5.2 Array Procedures
      6.7.5.3 Shared Arrays
      6.7.5.4 Accessing Arrays from C
    6.7.6 VLists
    6.7.7 Record Overview
    6.7.8 SRFI-9 Records
      Non-toplevel Record Definitions
      Custom Printers
      Functional “Setters”
    6.7.9 Records
    6.7.10 Structures
      6.7.10.1 Vtables
      6.7.10.2 Structure Basics
      6.7.10.3 Vtable Contents
      6.7.10.4 Meta-Vtables
      6.7.10.5 Vtable Example
      6.7.10.6 Tail Arrays
    6.7.11 Dictionary Types
    6.7.12 Association Lists
      6.7.12.1 Alist Key Equality
      6.7.12.2 Adding or Setting Alist Entries
      6.7.12.3 Retrieving Alist Entries
      6.7.12.4 Removing Alist Entries
      6.7.12.5 Sloppy Alist Functions
      6.7.12.6 Alist Example
    6.7.13 VList-Based Hash Lists or “VHashes”
    6.7.14 Hash Tables
      6.7.14.1 Hash Table Examples
      6.7.14.2 Hash Table Reference
  6.8 Smobs
  6.9 Procedures
    6.9.1 Lambda: Basic Procedure Creation
    6.9.2 Primitive Procedures
    6.9.3 Compiled Procedures
    6.9.4 Optional Arguments
      6.9.4.1 lambda* and define*.
      6.9.4.2 (ice-9 optargs)
    6.9.5 Case-lambda
    6.9.6 Higher-Order Functions
    6.9.7 Procedure Properties and Meta-information
    6.9.8 Procedures with Setters
    6.9.9 Inlinable Procedures
  6.10 Macros
    6.10.1 Defining Macros
    6.10.2 Syntax-rules Macros
      6.10.2.1 Patterns
      6.10.2.2 Hygiene
      6.10.2.3 Shorthands
      6.10.2.4 Reporting Syntax Errors in Macros
      6.10.2.5 Specifying a Custom Ellipsis Identifier
      6.10.2.6 Further Information
    6.10.3 Support for the ‘syntax-case’ System
      6.10.3.1 Why ‘syntax-case’?
      6.10.3.2 Custom Ellipsis Identifiers for syntax-case Macros
    6.10.4 Syntax Transformer Helpers
    6.10.5 Lisp-style Macro Definitions
    6.10.6 Identifier Macros
    6.10.7 Syntax Parameters
    6.10.8 Eval-when
    6.10.9 Internal Macros
  6.11 General Utility Functions
    6.11.1 Equality
    6.11.2 Object Properties
    6.11.3 Sorting
    6.11.4 Copying Deep Structures
    6.11.5 General String Conversion
    6.11.6 Hooks
      6.11.6.1 Hook Usage by Example
      6.11.6.2 Hook Reference
      6.11.6.3 Handling Scheme-level hooks from C code
      6.11.6.4 Hooks For C Code.
      6.11.6.5 Hooks for Garbage Collection
      6.11.6.6 Hooks into the Guile REPL
  6.12 Definitions and Variable Bindings
    6.12.1 Top Level Variable Definitions
    6.12.2 Local Variable Bindings
    6.12.3 Internal definitions
    6.12.4 Querying variable bindings
    6.12.5 Binding multiple return values
  6.13 Controlling the Flow of Program Execution
    6.13.1 Sequencing and Splicing
    6.13.2 Simple Conditional Evaluation
    6.13.3 Conditional Evaluation of a Sequence of Expressions
    6.13.4 Iteration mechanisms
    6.13.5 Prompts
      6.13.5.1 Prompt Primitives
      6.13.5.2 Shift, Reset, and All That
    6.13.6 Continuations
    6.13.7 Returning and Accepting Multiple Values
    6.13.8 Exceptions
      6.13.8.1 Exception Terminology
      6.13.8.2 Catching Exceptions
      6.13.8.3 Throw Handlers
      6.13.8.4 Throwing Exceptions
      6.13.8.5 How Guile Implements Exceptions
    6.13.9 Procedures for Signaling Errors
    6.13.10 Dynamic Wind
    6.13.11 How to Handle Errors
      6.13.11.1 C Support
      6.13.11.2 Signalling Type Errors
    6.13.12 Continuation Barriers
  6.14 Input and Output
    6.14.1 Ports
    6.14.2 Reading
    6.14.3 Writing
    6.14.4 Closing
    6.14.5 Random Access
    6.14.6 Line Oriented and Delimited Text
    6.14.7 Block reading and writing
    6.14.8 Default Ports for Input, Output and Errors
    6.14.9 Types of Port
      6.14.9.1 File Ports
      6.14.9.2 String Ports
      6.14.9.3 Soft Ports
      6.14.9.4 Void Ports
    6.14.10 R6RS I/O Ports
      6.14.10.1 File Names
      6.14.10.2 File Options
      6.14.10.3 Buffer Modes
      6.14.10.4 Transcoders
      6.14.10.5 The End-of-File Object
      6.14.10.6 Port Manipulation
      6.14.10.7 Input Ports
      6.14.10.8 Binary Input
      6.14.10.9 Textual Input
      6.14.10.10 Output Ports
      6.14.10.11 Binary Output
      6.14.10.12 Textual Output
    6.14.11 Using and Extending Ports in C
      6.14.11.1 C Port Interface
      6.14.11.2 Port Implementation
    6.14.12 Handling of Unicode byte order marks.
  6.15 Regular Expressions
    6.15.1 Regexp Functions
    6.15.2 Match Structures
    6.15.3 Backslash Escapes
  6.16 LALR(1) Parsing
  6.17 Reading and Evaluating Scheme Code
    6.17.1 Scheme Syntax: Standard and Guile Extensions
      6.17.1.1 Expression Syntax
      6.17.1.2 Comments
      6.17.1.3 Block Comments
      6.17.1.4 Case Sensitivity
      6.17.1.5 Keyword Syntax
      6.17.1.6 Reader Extensions
    6.17.2 Reading Scheme Code
    6.17.3 Writing Scheme Values
    6.17.4 Procedures for On the Fly Evaluation
    6.17.5 Compiling Scheme Code
    6.17.6 Loading Scheme Code from File
    6.17.7 Load Paths
    6.17.8 Character Encoding of Source Files
    6.17.9 Delayed Evaluation
    6.17.10 Local Evaluation
    6.17.11 Local Inclusion
    6.17.12 REPL Servers
    6.17.13 Cooperative REPL Servers
  6.18 Memory Management and Garbage Collection
    6.18.1 Function related to Garbage Collection
    6.18.2 Memory Blocks
      6.18.2.1 Upgrading from scm_must_malloc et al.
    6.18.3 Weak References
      6.18.3.1 Weak hash tables
      6.18.3.2 Weak vectors
    6.18.4 Guardians
  6.19 Modules
    6.19.1 General Information about Modules
    6.19.2 Using Guile Modules
    6.19.3 Creating Guile Modules
    6.19.4 Modules and the File System
    6.19.5 R6RS Version References
    6.19.6 R6RS Libraries
    6.19.7 Variables
    6.19.8 Module System Reflection
    6.19.9 Accessing Modules from C
    6.19.10 provide and require
    6.19.11 Environments
  6.20 Foreign Function Interface
    6.20.1 Foreign Libraries
    6.20.2 Foreign Functions
    6.20.3 C Extensions
    6.20.4 Modules and Extensions
    6.20.5 Foreign Pointers
      6.20.5.1 Foreign Types
      6.20.5.2 Foreign Variables
      6.20.5.3 Void Pointers and Byte Access
      6.20.5.4 Foreign Structs
    6.20.6 Dynamic FFI
  6.21 Threads, Mutexes, Asyncs and Dynamic Roots
    6.21.1 Arbiters
    6.21.2 Asyncs
      6.21.2.1 System asyncs
      6.21.2.2 User asyncs
    6.21.3 Threads
    6.21.4 Mutexes and Condition Variables
    6.21.5 Blocking in Guile Mode
    6.21.6 Critical Sections
    6.21.7 Fluids and Dynamic States
    6.21.8 Parameters
    6.21.9 Futures
    6.21.10 Parallel forms
  6.22 Configuration, Features and Runtime Options
    6.22.1 Configuration, Build and Installation
    6.22.2 Feature Tracking
      6.22.2.1 Feature Manipulation
      6.22.2.2 Common Feature Symbols
    6.22.3 Runtime Options
      6.22.3.1 Examples of option use
  6.23 Support for Other Languages
    6.23.1 Using Other Languages
    6.23.2 Emacs Lisp
      6.23.2.1 Nil
      6.23.2.2 Equality
      6.23.2.3 Dynamic Binding
      6.23.2.4 Other Elisp Features
    6.23.3 ECMAScript
  6.24 Support for Internationalization
    6.24.1 Internationalization with Guile
    6.24.2 Text Collation
    6.24.3 Character Case Mapping
    6.24.4 Number Input and Output
    6.24.5 Accessing Locale Information
    6.24.6 Gettext Support
  6.25 Debugging Infrastructure
    6.25.1 Evaluation and the Scheme Stack
      6.25.1.1 Stack Capture
      6.25.1.2 Stacks
      6.25.1.3 Frames
    6.25.2 Source Properties
    6.25.3 Programmatic Error Handling
      6.25.3.1 Catching Exceptions
      6.25.3.2 Capturing the full error stack
      6.25.3.3 Pre-Unwind Debugging
      6.25.3.4 Debug options
    6.25.4 Traps
      6.25.4.1 VM Hooks
      6.25.4.2 Trap Interface
      6.25.4.3 Low-Level Traps
      6.25.4.4 Tracing Traps
      6.25.4.5 Trap States
      6.25.4.6 High-Level Traps
    6.25.5 GDB Support
  6.26 Code Coverage Reports
7 Guile Modules
  7.1 SLIB
    7.1.1 SLIB installation
    7.1.2 JACAL
  7.2 POSIX System Calls and Networking
    7.2.1 POSIX Interface Conventions
    7.2.2 Ports and File Descriptors
    7.2.3 File System
    7.2.4 User Information
    7.2.5 Time
    7.2.6 Runtime Environment
    7.2.7 Processes
    7.2.8 Signals
    7.2.9 Terminals and Ptys
    7.2.10 Pipes
    7.2.11 Networking
      7.2.11.1 Network Address Conversion
      7.2.11.2 Network Databases
      7.2.11.3 Network Socket Address
      7.2.11.4 Network Sockets and Communication
      7.2.11.5 Network Socket Examples
    7.2.12 System Identification
    7.2.13 Locales
    7.2.14 Encryption
  7.3 HTTP, the Web, and All That
    7.3.1 Types and the Web
    7.3.2 Universal Resource Identifiers
    7.3.3 The Hyper-Text Transfer Protocol
    7.3.4 HTTP Headers
      7.3.4.1 HTTP Header Types
      7.3.4.2 General Headers
      7.3.4.3 Entity Headers
      7.3.4.4 Request Headers
      7.3.4.5 Response Headers
    7.3.5 Transfer Codings
    7.3.6 HTTP Requests
      7.3.6.1 An Important Note on Character Sets
      7.3.6.2 Request API
    7.3.7 HTTP Responses
    7.3.8 Web Client
    7.3.9 Web Server
    7.3.10 Web Examples
      7.3.10.1 Hello, World!
      7.3.10.2 Inspecting the Request
      7.3.10.3 Higher-Level Interfaces
      7.3.10.4 Conclusion
  7.4 The (ice-9 getopt-long) Module
    7.4.1 A Short getopt-long Example
    7.4.2 How to Write an Option Specification
    7.4.3 Expected Command Line Format
    7.4.4 Reference Documentation for ‘getopt-long’
    7.4.5 Reference Documentation for ‘option-ref’
  7.5 SRFI Support Modules
    7.5.1 About SRFI Usage
    7.5.2 SRFI-0 - cond-expand
    7.5.3 SRFI-1 - List library
      7.5.3.1 Constructors
      7.5.3.2 Predicates
      7.5.3.3 Selectors
      7.5.3.4 Length, Append, Concatenate, etc.
      7.5.3.5 Fold, Unfold & Map
      7.5.3.6 Filtering and Partitioning
      7.5.3.7 Searching
      7.5.3.8 Deleting
      7.5.3.9 Association Lists
      7.5.3.10 Set Operations on Lists
    7.5.4 SRFI-2 - and-let*
    7.5.5 SRFI-4 - Homogeneous numeric vector datatypes
      7.5.5.1 SRFI-4 - Overview
      7.5.5.2 SRFI-4 - API
      7.5.5.3 SRFI-4 - Relation to bytevectors
      7.5.5.4 SRFI-4 - Guile extensions
    7.5.6 SRFI-6 - Basic String Ports
    7.5.7 SRFI-8 - receive
    7.5.8 SRFI-9 - define-record-type
    7.5.9 SRFI-10 - Hash-Comma Reader Extension
    7.5.10 SRFI-11 - let-values
    7.5.11 SRFI-13 - String Library
    7.5.12 SRFI-14 - Character-set Library
    7.5.13 SRFI-16 - case-lambda
    7.5.14 SRFI-17 - Generalized set!
    7.5.15 SRFI-18 - Multithreading support
      7.5.15.1 SRFI-18 Threads
      7.5.15.2 SRFI-18 Mutexes
      7.5.15.3 SRFI-18 Condition variables
      7.5.15.4 SRFI-18 Time
      7.5.15.5 SRFI-18 Exceptions
    7.5.16 SRFI-19 - Time/Date Library
      7.5.16.1 SRFI-19 Introduction
      7.5.16.2 SRFI-19 Time
      7.5.16.3 SRFI-19 Date
      7.5.16.4 SRFI-19 Time/Date conversions
      7.5.16.5 SRFI-19 Date to string
      7.5.16.6 SRFI-19 String to date
    7.5.17 SRFI-23 - Error Reporting
    7.5.18 SRFI-26 - specializing parameters
    7.5.19 SRFI-27 - Sources of Random Bits
      7.5.19.1 The Default Random Source
      7.5.19.2 Random Sources
      7.5.19.3 Obtaining random number generator procedures
    7.5.20 SRFI-30 - Nested Multi-line Comments
    7.5.21 SRFI-31 - A special form ‘rec’ for recursive evaluation
    7.5.22 SRFI-34 - Exception handling for programs
    7.5.23 SRFI-35 - Conditions
    7.5.24 SRFI-37 - args-fold
    7.5.25 SRFI-38 - External Representation for Data With Shared Structure
    7.5.26 SRFI-39 - Parameters
    7.5.27 SRFI-41 - Streams
      7.5.27.1 SRFI-41 Stream Fundamentals
      7.5.27.2 SRFI-41 Stream Primitives
      7.5.27.3 SRFI-41 Stream Library
    7.5.28 SRFI-42 - Eager Comprehensions
    7.5.29 SRFI-43 - Vector Library
      7.5.29.1 SRFI-43 Constructors
      7.5.29.2 SRFI-43 Predicates
      7.5.29.3 SRFI-43 Selectors
      7.5.29.4 SRFI-43 Iteration
      7.5.29.5 SRFI-43 Searching
      7.5.29.6 SRFI-43 Mutators
      7.5.29.7 SRFI-43 Conversion
    7.5.30 SRFI-45 - Primitives for Expressing Iterative Lazy Algorithms
    7.5.31 SRFI-46 Basic syntax-rules Extensions
    7.5.32 SRFI-55 - Requiring Features
    7.5.33 SRFI-60 - Integers as Bits
    7.5.34 SRFI-61 - A more general ‘cond’ clause
    7.5.35 SRFI-62 - S-expression comments.
    7.5.36 SRFI-64 - A Scheme API for test suites.
    7.5.37 SRFI-67 - Compare procedures
    7.5.38 SRFI-69 - Basic hash tables
      7.5.38.1 Creating hash tables
      7.5.38.2 Accessing table items
      7.5.38.3 Table properties
      7.5.38.4 Hash table algorithms
    7.5.39 SRFI-87 => in case clauses
    7.5.40 SRFI-88 Keyword Objects
    7.5.41 SRFI-98 Accessing environment variables.
    7.5.42 SRFI-105 Curly-infix expressions.
    7.5.43 SRFI-111 Boxes.
  7.6 R6RS Support
    7.6.1 Incompatibilities with the R6RS
    7.6.2 R6RS Standard Libraries
      7.6.2.1 Library Usage
      7.6.2.2 rnrs base
      7.6.2.3 rnrs unicode
      7.6.2.4 rnrs bytevectors
      7.6.2.5 rnrs lists
      7.6.2.6 rnrs sorting
      7.6.2.7 rnrs control
      7.6.2.8 R6RS Records
      7.6.2.9 rnrs records syntactic
      7.6.2.10 rnrs records procedural
      7.6.2.11 rnrs records inspection
      7.6.2.12 rnrs exceptions
      7.6.2.13 rnrs conditions
      7.6.2.14 I/O Conditions
      7.6.2.15 rnrs io ports
      7.6.2.16 rnrs io simple
      7.6.2.17 rnrs files
      7.6.2.18 rnrs programs
      7.6.2.19 rnrs arithmetic fixnums
      7.6.2.20 rnrs arithmetic flonums
      7.6.2.21 rnrs arithmetic bitwise
      7.6.2.22 rnrs syntax-case
      7.6.2.23 rnrs hashtables
      7.6.2.24 rnrs enums
      7.6.2.25 rnrs
      7.6.2.26 rnrs eval
      7.6.2.27 rnrs mutable-pairs
      7.6.2.28 rnrs mutable-strings
      7.6.2.29 rnrs r5rs
  7.7 Pattern Matching
  7.8 Readline Support
    7.8.1 Loading Readline Support
    7.8.2 Readline Options
    7.8.3 Readline Functions
      7.8.3.1 Readline Port
      7.8.3.2 Completion
  7.9 Pretty Printing
  7.10 Formatted Output
  7.11 File Tree Walk
  7.12 Queues
  7.13 Streams
  7.14 Buffered Input
  7.15 Expect
  7.16 ‘sxml-match’: Pattern Matching of SXML
    Syntax
    Matching XML Elements
    Ellipses in Patterns
    Ellipses in Quasiquote’d Output
    Matching Nodesets
    Matching the “Rest” of a Nodeset
    Matching the Unmatched Attributes
    Default Values in Attribute Patterns
    Guards in Patterns
    Catamorphisms
    Named-Catamorphisms
    ‘sxml-match-let’ and ‘sxml-match-let*’
  7.17 The Scheme shell (scsh)
  7.18 Curried Definitions
  7.19 Statprof
  7.20 Implementation notes
  7.21 Usage
  7.22 SXML
    7.22.1 SXML Overview
    7.22.2 Reading and Writing XML
    7.22.3 SSAX: A Functional XML Parsing Toolkit
      7.22.3.1 History
      7.22.3.2 Implementation
      7.22.3.3 Usage
    7.22.4 Transforming SXML
      7.22.4.1 Overview
      7.22.4.2 Usage
    7.22.5 SXML Tree Fold
      7.22.5.1 Overview
      7.22.5.2 Usage
    7.22.6 SXPath
      7.22.6.1 Overview
      7.22.6.2 Usage
    7.22.7 (sxml ssax input-parse)
      7.22.7.1 Overview
      7.22.7.2 Usage
    7.22.8 (sxml apply-templates)
      7.22.8.1 Overview
      7.22.8.2 Usage
  7.23 Texinfo Processing
    7.23.1 (texinfo)
      7.23.1.1 Overview
      7.23.1.2 Usage
    7.23.2 (texinfo docbook)
      7.23.2.1 Overview
      7.23.2.2 Usage
    7.23.3 (texinfo html)
      7.23.3.1 Overview
      7.23.3.2 Usage
    7.23.4 (texinfo indexing)
      7.23.4.1 Overview
      7.23.4.2 Usage
    7.23.5 (texinfo string-utils)
      7.23.5.1 Overview
      7.23.5.2 Usage
    7.23.6 (texinfo plain-text)
      7.23.6.1 Overview
      7.23.6.2 Usage
    7.23.7 (texinfo serialize)
      7.23.7.1 Overview
      7.23.7.2 Usage
    7.23.8 (texinfo reflection)
      7.23.8.1 Overview
      7.23.8.2 Usage
8 GOOPS
  8.1 Copyright Notice
  8.2 Class Definition
  8.3 Instance Creation and Slot Access
  8.4 Slot Options
  8.5 Illustrating Slot Description
  8.6 Methods and Generic Functions
    8.6.1 Accessors
    8.6.2 Extending Primitives
    8.6.3 Merging Generics
    8.6.4 Next-method
    8.6.5 Generic Function and Method Examples
    8.6.6 Handling Invocation Errors
  8.7 Inheritance
    8.7.1 Class Precedence List
    8.7.2 Sorting Methods
  8.8 Introspection
    8.8.1 Classes
    8.8.2 Instances
    8.8.3 Slots
    8.8.4 Generic Functions
    8.8.5 Accessing Slots
  8.9 Error Handling
  8.10 GOOPS Object Miscellany
  8.11 The Metaobject Protocol
    8.11.1 Metaobjects and the Metaobject Protocol
    8.11.2 Metaclasses
    8.11.3 MOP Specification
    8.11.4 Instance Creation Protocol
    8.11.5 Class Definition Protocol
    8.11.6 Customizing Class Definition
    8.11.7 Method Definition
    8.11.8 Method Definition Internals
    8.11.9 Generic Function Internals
    8.11.10 Generic Function Invocation
  8.12 Redefining a Class
    8.12.1 Default Class Redefinition Behaviour
    8.12.2 Customizing Class Redefinition
  8.13 Changing the Class of an Instance
9 Guile Implementation
  9.1 A Brief History of Guile
    9.1.1 The Emacs Thesis
    9.1.2 Early Days
    9.1.3 A Scheme of Many Maintainers
    9.1.4 A Timeline of Selected Guile Releases
    9.1.5 Status, or: Your Help Needed
  9.2 Data Representation
    9.2.1 A Simple Representation
    9.2.2 Faster Integers
    9.2.3 Cheaper Pairs
    9.2.4 Conservative Garbage Collection
    9.2.5 The SCM Type in Guile
      9.2.5.1 Relationship between ‘SCM’ and ‘scm_t_bits’
      9.2.5.2 Immediate objects
      9.2.5.3 Non-immediate objects
      9.2.5.4 Allocating Cells
      9.2.5.5 Heap Cell Type Information
      9.2.5.6 Accessing Cell Entries
  9.3 A Virtual Machine for Guile
    9.3.1 Why a VM?
    9.3.2 VM Concepts
    9.3.3 Stack Layout
    9.3.4 Variables and the VM
    9.3.5 Compiled Procedures are VM Programs
    9.3.6 Instruction Set
      9.3.6.1 Lexical Environment Instructions
      9.3.6.2 Top-Level Environment Instructions
      9.3.6.3 Procedure Call and Return Instructions
      9.3.6.4 Function Prologue Instructions
      9.3.6.5 Trampoline Instructions
      9.3.6.6 Branch Instructions
      9.3.6.7 Data Constructor Instructions
      9.3.6.8 Loading Instructions
      9.3.6.9 Dynamic Environment Instructions
      9.3.6.10 Miscellaneous Instructions
      9.3.6.11 Inlined Scheme Instructions
      9.3.6.12 Inlined Mathematical Instructions
      9.3.6.13 Inlined Bytevector Instructions
  9.4 Compiling to the Virtual Machine
    9.4.1 Compiler Tower
    9.4.2 The Scheme Compiler
    9.4.3 Tree-IL
    9.4.4 GLIL
    9.4.5 Assembly
    9.4.6 Bytecode and Objcode
    9.4.7 Writing New High-Level Languages
    9.4.8 Extending the Compiler
Appendix A GNU Free Documentation License
Concept Index
Procedure Index
Variable Index
Type Index
R5RS Index
