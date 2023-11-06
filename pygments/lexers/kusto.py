"""
    pygments.lexers.kusto
    ~~~~~~~~~~~~~~~~~~~~~

    Lexers for Kusto Query Language (KQL).

    :copyright: Copyright 2006-2023 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from pygments.lexer import RegexLexer, words
from pygments.token import (Comment, Keyword, Name, Number, Punctuation,
                            String, Whitespace)

__all__ = ["KustoLexer"]

# Although these all seem to be keywords
# https://github.com/microsoft/Kusto-Query-Language/blob/master/src/Kusto.Language/Syntax/SyntaxFacts.cs
# it appears that only the ones with tags here
# https://github.com/microsoft/Kusto-Query-Language/blob/master/src/Kusto.Language/Parser/QueryGrammar.cs
# are highlighted in the Azure portal log query editor.
KUSTO_KEYWORDS = (
    "and",
    "as",
    "between",
    "by",
    "consume",
    "contains",
    "containscs",
    "count",
    "distinct",
    "evaluate",
    "extend",
    "facet",
    "filter",
    "find",
    "fork",
    "getschema",
    "has",
    "invoke",
    "join",
    "limit",
    "lookup",
    "make-series",
    "matches regex",
    "mv-apply",
    "mv-expand",
    "notcontains",
    "notcontainscs",
    "!contains",
    "!has",
    "!startswith",
    "on",
    "or",
    "order",
    "parse",
    "parse-where",
    "parse-kv",
    "partition",
    "print",
    "project",
    "project-away",
    "project-keep",
    "project-rename",
    "project-reorder",
    "range",
    "reduce",
    "regex",
    "render",
    "sample",
    "sample-distinct",
    "scan",
    "search",
    "serialize",
    "sort",
    "startswith",
    "summarize",
    "take",
    "top",
    "top-hitters",
    "top-nested",
    "typeof",
    "union",
    "where",
    "bool",
    "date",
    "datetime",
    "int",
    "long",
    "real",
    "string",
    "time",
)

# From
# https://github.com/microsoft/Kusto-Query-Language/blob/master/src/Kusto.Language/Syntax/SyntaxFacts.cs
KUSTO_PUNCTUATION = (
    "(",
    ")",
    "[",
    "]",
    "{",
    "}",
    "|",
    "<|",
    "+",
    "-",
    "*",
    "/",
    "%",
    ".." "!",
    "<",
    "<=",
    ">",
    ">=",
    "=",
    "==",
    "!=",
    "<>",
    ":",
    ";",
    ",",
    "=~",
    "!~",
    "?",
    "=>",
)


class KustoLexer(RegexLexer):
    """For Kusto Query Language source code."""

    name = "Kusto"
    aliases = ["kql", "kusto"]
    filenames = ["*.kql", "*.kusto", ".csl"]

    tokens = {
        "root": [
            (
                # One or more whitespace characters
                r"\s+",
                Whitespace,
            ),
            (
                # Keywords
                words(KUSTO_KEYWORDS, suffix=r"\b"),
                Keyword,
            ),
            (
                # Single line comments begin with //
                r"//.*",
                Comment,
            ),
            (
                # Punctuation
                words(KUSTO_PUNCTUATION),
                Punctuation,
            ),
            (
                # Names begin with a non-numeric word character
                # followed by zero or more word characters
                r"[^\W\d]\w*",
                Name,
            ),
            # Numbers can take the form 1, .1, 1., 1.1, 1.1111, etc.
            (r"\d+[.]\d*|[.]\d+", Number.Float),
            (r"\d+", Number.Integer),
            (
                # String literals can begin with '...
                r"'",
                String,
                "single_string",
            ),
            (
                # ...or with "
                r'"',
                String,
                "double_string",
            ),
            (
                # Verbatim strings can begin with @'...
                r"@'",
                String,
                "single_verbatim",
            ),
            (
                # ...or with @"
                r'@"',
                String,
                "double_verbatim",
            ),
            (
                # Multi-line strings begin with ```
                r"```",
                String,
                "multi_string",
            ),
        ],
        "single_string": [
            # This string literal ends with an unescaped single quote
            (r"'", String, "#pop"),
            (r"\\", String.Escape, "string_escape"),
            (r"[^'\\]+", String),
        ],
        "double_string": [
            # This string literal ends with an unescaped double quote
            (r'"', String, "#pop"),
            (r"\\", String.Escape, "string_escape"),
            (r'[^"\\]+', String),
        ],
        "string_escape": [
            # Presume, for simplicity, that any single character can be escaped
            (r".", String.Escape, "#pop"),
        ],
        "single_verbatim": [
            # This string literal ends with the first single quote
            (r"[^']+", String),
            (r"'", String, "#pop"),
        ],
        "double_verbatim": [
            # This string literal ends with the first double quote
            (r'[^"]+', String),
            (r'"', String, "#pop"),
        ],
        "multi_string": [
            # This string literal ends with the first ```
            (
                r"[^```]+",
                String,
            ),
            (r"```", String, "#pop"),
        ],
    }
