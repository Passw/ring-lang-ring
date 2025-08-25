# -*- coding: utf-8 -*-
"""
    pygments.lexers.ring
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexer for the Ring language.

    :copyright: Copyright 2016, Mahmoud Fayed <msfclipper@yahoo.com>
"""

import re

from pygments.lexer import RegexLexer, include, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Error

__all__ = ['RingLexer']


class RingLexer(RegexLexer):
    """
    For `Ring <https://ring-lang.net/>`_ source code.

    .. versionadded:: 1.5
    """

    name = 'Ring'
    aliases = ['ring', 'ring']
    filenames = ['*.ring', '*.rh']
    mimetypes = ['text/x-ring']

    flags = re.MULTILINE | re.IGNORECASE | re.UNICODE

    def underscorize(words):
        newWords = []
        new = ""
        for word in words:
            for ch in word:
                new += (ch + "_?")
            newWords.append(new)
            new = ""
        return "|".join(newWords)

    keywords = [
		'again','and','but','bye','call','case','catch','class','def','do','done',
		'else','elseif','end','exit','for','foreach','from','func','get','give','if','import',
		'in','load','loop','new','next','not','off','ok','on','or','other','package',
		'private','put','return','see','step','switch','to','try','while','changeringkeyword',
		'changeringoperator','loadsyntax','endfunc','endclass','endpackage',
		'endif','endfor','endwhile','endswitch','endtry','function','endfunction',
		'break','continue'
    ]

    keywordsPseudo = [
        'null', 'true', 'false'
    ]

    opWords = [
        'and', 'or', 'not'
    ]

    types = [
        'list', 'string', 'stack', 'queue', 'tree', 'hashtable'
	]

    tokens = {
        'root': [
            (r'##.*$', String.Doc),
            (r'#.*$', Comment),
            (r'[*=><+\-/@$~&%!?|\\\[\]]', Operator),
            (r'\.\.|\.|,|\[\.|\.\]|\{\.|\.\}|\(\.|\.\)|\{|\}|\(|\)|:|\^|`|;',
             Punctuation),

            # Strings
            (r'(?:[\w]+)"', String, 'rdqs'),
            (r'"""', String, 'tdqs'),
            ('"', String, 'dqs'),

            # Char
            ("'", String.Char, 'chars'),

            # Keywords
            (r'(%s)\b' % underscorize(opWords), Operator.Word),
            (r'(p_?r_?o_?c_?\s)(?![(\[\]])', Keyword, 'funcname'),
            (r'(%s)\b' % underscorize(keywords), Keyword),
            (r'(%s)\b' % underscorize(['from', 'import', 'include']),
             Keyword.Namespace),
            (r'(v_?a_?r)\b', Keyword.Declaration),
            (r'(%s)\b' % underscorize(types), Keyword.Type),
            (r'(%s)\b' % underscorize(keywordsPseudo), Keyword.Pseudo),
            # Identifiers
            (r'\b((?![_\d])\w)(((?!_)\w)|(_(?!_)\w))*', Name),
            # Numbers
            (r'[0-9][0-9_]*(?=([e.]|\'f(32|64)))',
             Number.Float, ('float-suffix', 'float-number')),
            (r'0x[a-f0-9][a-f0-9_]*', Number.Hex, 'int-suffix'),
            (r'0b[01][01_]*', Number.Bin, 'int-suffix'),
            (r'0o[0-7][0-7_]*', Number.Oct, 'int-suffix'),
            (r'[0-9][0-9_]*', Number.Integer, 'int-suffix'),
            # Whitespace
            (r'\s+', Text),
            (r'.+$', Error),
        ],
        'chars': [
            (r'\\([\\abcefnrtvl"\']|x[a-f0-9]{2}|[0-9]{1,3})', String.Escape),
            (r"'", String.Char, '#pop'),
            (r".", String.Char)
        ],
        'strings': [
            (r'(?<!\$)\$(\d+|#|\w+)+', String.Interpol),
            (r'[^\\\'"$\n]+', String),
            # quotes, dollars and backslashes must be parsed one at a time
            (r'[\'"\\]', String),
            # unhandled string formatting sign
            (r'\$', String)
            # newlines are an error (use "nl" state)
        ],
        'dqs': [
            (r'\\([\\abcefnrtvl"\']|\n|x[a-f0-9]{2}|[0-9]{1,3})',
             String.Escape),
            (r'"', String, '#pop'),
            include('strings')
        ],
        'rdqs': [
            (r'"(?!")', String, '#pop'),
            (r'""', String.Escape),
            include('strings')
        ],
        'tdqs': [
            (r'"""(?!")', String, '#pop'),
            include('strings'),
            include('nl')
        ],
        'funcname': [
            (r'((?![\d_])\w)(((?!_)\w)|(_(?!_)\w))*', Name.Function, '#pop'),
            (r'`.+`', Name.Function, '#pop')
        ],
        'nl': [
            (r'\n', String)
        ],
        'float-number': [
            (r'\.(?!\.)[0-9_]*', Number.Float),
            (r'e[+-]?[0-9][0-9_]*', Number.Float),
            default('#pop')
        ],
        'float-suffix': [
            (r'\'f(32|64)', Number.Float),
            default('#pop')
        ],
        'int-suffix': [
            (r'\'i(32|64)', Number.Integer.Long),
            (r'\'i(8|16)', Number.Integer),
            default('#pop')
        ],
    }
