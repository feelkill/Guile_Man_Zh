<!--
1.6 Obtaining and Installing Guile
==================================
-->

## 1.6 获取并安装Guile

<!--
Guile can be obtained from the main GNU archive site <ftp://ftp.gnu.org>
or any of its mirrors.  The file will be named guile-VERSION.tar.gz.
The current version is 2.0.11, so the file you should grab is:
-->

Guile能够从GNU主站 <ftp://ftp.gnu.org> 或者它的任何镜像站获取得到。文件命名为guile-版本.tar.gz。当前版本是2.0.11，所以你应该抓取的文件是

  <ftp://ftp.gnu.org/gnu/guile/guile-2.0.11.tar.gz>

<!--
   To unbundle Guile use the instruction
-->

解压Guile使用如下命令

     zcat guile-2.0.11.tar.gz | tar xvf -

<!--
which will create a directory called ‘guile-2.0.11’ with all the
sources.  You can look at the file ‘INSTALL’ for detailed instructions
on how to build and install Guile, but you should be able to just do
-->

这将创建一个名为guile-2.0.11的目录，里面是源代码。关于如何构建和安装Guile的详细指导，你可以参考文件INSTALL。但是，你应该能够这样做

     cd guile-2.0.11
     ./configure
     make
     make install

<!--
   This will install the Guile executable ‘guile’, the Guile library
‘libguile’ and various associated header files and support libraries.
It will also install the Guile reference manual.
-->

这会安装Guile可执行文件'guile'，Guile库'libguile'，相关的头文件和支持的库。另外，还会安装Guile引用手册。

<!--
   Since this manual frequently refers to the Scheme “standard”, also
known as R5RS, or the “Revised^5 Report on the Algorithmic Language
Scheme”, we have included the report in the Guile distribution; see
*note Introduction: (r5rs)Top.  This will also be installed in your info
directory.
-->

因为该手册会频繁地引用Scheme标准，即R5RS，我们在Guile的发布里也囊括了此报告，请参考[Introduction](http://www.gnu.org/software/guile/manual/r5rs/index.html#Top)。这也会安装到你的info目录下面。

