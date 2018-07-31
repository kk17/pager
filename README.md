pager
===============================

version number: 0.0.1
author: Zhike Chen

Overview
--------

A python command line tool that can parse html page, extract and print html elements.

Installation / Usage
--------------------

To install use pip(not publish yet):

    # $ pip install pager


Or clone the repo:

    $ git clone https://github.com/kk17/pager.git
    $ python setup.py install

Usage
-------

    $ pager --help
    Usage: pager [OPTIONS] URL [SELECTORS]...

    Options:
      -P, --pipe            pipe mode
      -e, --encoding TEXT   page encoding
      -s, --separator TEXT  separator between multi elements, default to empty
      -F, --format TEXT     print format, available formats are: `markdown-text`,
                            `html`, `pretty-html`, default to `markdown-text`
      --help                Show this message and exit.

Example
-------

    pager -e gb2312  http://www.meijutt.com/content/meiju158.html 'div.down_list' [0] 'ul li a' [href]

    pager -s --- https://www.qiushibaike.com/hot 'div.content' | mdv -

    pager -s --- https://mnemonicdictionary.com/\?word\=vague 'div.media-body > div' [1] and 'div.mnemonic-card div.card-body div.card-text p' [:3] | mdv -

The `mdv` above is a [Styled Terminal Markdown Viewer](https://github.com/axiros/terminal_markdown_viewer), mdv is currently python2 only, for python 3 you can install this branch: [rachmadaniHaryono/terminal_markdown_viewer at fix-python35](https://github.com/rachmadaniHaryono/terminal_markdown_viewer/tree/fix-python35) or use [axiros/mdvl: Lightweight markdown terminal renderer](https://github.com/axiros/mdvl) instead.

Contributing
------------

TBD
