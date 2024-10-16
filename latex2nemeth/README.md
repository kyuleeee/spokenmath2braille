Latex2Nemeth
============

This is the source tree for Latex2Nemeth, a tool for translating TeX files to Braille.


* [Licence](#licence)
* [Dependencies](#dependencies)
* [Installing](#installing)
* [Usage](#usage)

Licence
-------

Copyright 2016-2022 by Andreas Papasalοuros, Antonis Tsolomitis.

This program is distributed under the GPL, version 3 or later. Please see the COPYING file for details.

Dependencies
------------

In order to use the tool, you need the following programs:

1. **Java**

    The tool has been tested with `Java 7` and `Java 8`.

2. **Apache Maven**
   
    Apache Maven is a software project management and comprehension tool.
    - For Windows, download the [latest version](https://maven.apache.org/download.cgi).
    - For Linux, install it from the repositories:

            sudo apt-get install maven


Installing
----------

* Download Latex2Nemeth's sources. E.g. for anonymous access on SourceForge:

        git clone git://git.code.sf.net/p/latex2nemeth/code latex2nemeth-code

* Compile Latex2Nemeth.

        cd /path/to/latex2nemeth
        mvn package -Dmaven.test.skip=true

* **[Optional]** You can compile and also run the tests with `mvn package`

Usage
-----

After compiling the tool the executable `jar` will be located in the `target/` directory,
e.g. `target/latex2nemeth.jar`.

A simple to way to run the tool is

        java -jar latex2nemeth.jar <tex-file> <aux-file>

**Options**

|Option|Description|
|------|-----------|  
|-e,--encoding <arg>  | The encoding table for Braille Mathematical symbols in the form of a JSON file.  If not specified, default 		       Nemeth table is used. |
| -m,--mode <arg>     | The mode of the parser which controls the type of the output Braille files. It can be either 'nemeth' or 'pef'. The default mode is nemeth.|
| -o <arg>            | The output prefix of the Braille files. It can also be prefixed with a path to a specific directory. The default value is the name of the TeX file. The program generates an output file for each chapter in the input TeX file.|

**Examples**
  A simple example:
        java -jar target/latex2nemeth.jar src/test/resources/com/latex2nemeth/bootstrap/mathtest.tex src/test/resources/com/latex2nemeth/bootstrap/mathtest.aux
 
  A more complicated example:
        java -jar target/latex2nemeth.jar src/test/resources/com/latex2nemeth/bootstrap/mathtest.tex src/test/resources/com/latex2nemeth/bootstrap/mathtest.aux -o ch -m nemeth -e src/test/resources/com/latex2nemeth/bootstrap/nemeth.json

  An example with pictures:
        java -jar target/latex2nemeth.jar src/test/resources/com/latex2nemeth/bootstrap/mathpics.tex src/test/resources/com/latex2nemeth/bootstrap/mathpics.aux

**Notes**
-------------
1. Input tex files must be in utf-8. If using another encoding (such as iso-8859-7) 
   run first LaTeX to produce the aux file and then convert the source.tex to utf-8 
   with a command such as

        iconv -f iso8859-7 -t utf-8 source.tex > source-utf8.tex

   or using your editor. Now run "java -jar latex2nemeth.jar" as above with 
   source-utf8.tex as the tex file and source.aux as the aux file. If errors are 
   produced you need to modify the source-utf8.tex at the line indicated. 
   Usually the errors have to do either with non supported shortcuts for macros 
   (in which case replace the shortcut with the true code) or with macros that 
   are irrelevant to the blind (in which case remove them). 

2. Braille/Nemeth output files are encoded in UTF-16. 
   Convert them to utf-8 with a command such as

        iconv -f utf-16 -t utf-8 source.nemeth > source-utf8.nemeth
   
   (This step will be eliminated in future releases and the output will be directly
    in utf-8.)

3. To emboss the output open the produced source-utf8.nemeth in LibreOffice 
   with the odt2braille plugin installed, open it as "Unicode UTF-8 encoded text" 
   and emboss as usually.

4. Pictures are exported separately in text files. Currently only `pstricks` pictures are supported. Currently their preable is hardcoded in `com.latex2nemeth.utils.Preamble`.

5. In order to save space when braille pages are embossed a paragraph change corresponds
to three spaces. Thus commands such as \\ (double backslash) are transcribed as three spaces.
However, there are cases, such as in poems, that a change of line must occur from line to line.
To support these cases, a new latex-type command, named \latextonemethnewline
is understood by the program, which produces a new line. So the double backslash
at the end of each line of a poem must be substituted by \latextonemethnewline. For LaTeX to run 
smoothly a \newcommand can be introduced in the preamble, such as
\newcommand{\latextonemethnewline}{\newline}

6. It is possible to translate TeX files using different Braille alphabets. A different Braille alphabet is  encoded in a JSON file. For example, in order to translate a texfile  into polytonic Greek, the command is as follows:
 
	 java -jar latex2nemeth.jar texfile.tex auxfile.aux  -e /path/to/polytonic.json

Please report issues related to erratic output to a n d p a p a s [AT] a e g e a n . g r
and issues related to the tex file handling/modifying to a n t o n i s . t s o l o m i t i s [AT] g m a i l . c o m 

The project was supported by the Research Unit of the University of the Aegean (project 2625).


