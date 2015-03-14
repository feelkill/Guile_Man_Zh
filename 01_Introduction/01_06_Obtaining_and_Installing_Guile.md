1.6 Obtaining and Installing Guile
==================================

Guile can be obtained from the main GNU archive site <ftp://ftp.gnu.org>
or any of its mirrors.  The file will be named guile-VERSION.tar.gz.
The current version is 2.0.11, so the file you should grab is:

   <ftp://ftp.gnu.org/gnu/guile/guile-2.0.11.tar.gz>

   To unbundle Guile use the instruction

     zcat guile-2.0.11.tar.gz | tar xvf -

which will create a directory called ‘guile-2.0.11’ with all the
sources.  You can look at the file ‘INSTALL’ for detailed instructions
on how to build and install Guile, but you should be able to just do

     cd guile-2.0.11
     ./configure
     make
     make install

   This will install the Guile executable ‘guile’, the Guile library
‘libguile’ and various associated header files and support libraries.
It will also install the Guile reference manual.

   Since this manual frequently refers to the Scheme “standard”, also
known as R5RS, or the “Revised^5 Report on the Algorithmic Language
Scheme”, we have included the report in the Guile distribution; see
*note Introduction: (r5rs)Top.  This will also be installed in your info
directory.

