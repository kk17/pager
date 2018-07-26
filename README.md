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
    
Contributing
------------

TBD

Example
-------

    pager -e gb2312  http://www.meijutt.com/content/meiju158.html 'div.down_list' [0] 'ul li a' [href]

    pager -b 2 https://www.qiushibaike.com/hot 'div.content span'

    pager -b 2 https://mnemonicdictionary.com/\?word\=vague 'div.media-body > div' [1] and 'div.mnemonic-card div.card-body div.card-text p' [0]
