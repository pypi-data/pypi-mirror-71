This is a fork of https://github.com/zikzakmedia/python-mediawiki aka https://pypi.org/project/mediawiki/

It has updates to run with Python 3.  No further maintenance or feature development is planned at this point.

This updated version is published at https://pypi.org/project/mediawiki2html/ (:code:`pip install mediawiki2html`) but still
provides the ":code:`mediawiki`" module that you import.

Presentation
============

Convert MediaWiki Syntax to HTML

How to use in a program
=======================

Example for HTML
----------------
In order to use this tool to render wikitext into HTML in a Python program, you can use the following lines:

::

 from mediawiki import *

 source = ''
 with open("syntax") as f:
    for line in f:
        source += line

 wiki_content = wiki2html(source, True)
 print(wiki_content)


Doc about Syntax
----------------
See doc dir more about syntax and HTML code generated and example
