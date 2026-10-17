"""A Pygments lexer for KDL, the document language OpenLych configs are written in.

Implements the parts of the KDL spec the config dialect uses: node names,
positional arguments, `key=value` properties, `#true`/`#false`/`#null`,
numbers (signs, hex, exponents), quoted strings with escapes and multiline
raw strings, `//` and `/* */` comments, slashdash (`/-`) hiding, `;`
separators, `{ ... }` child blocks, and `\\` line continuation.
"""

from pygments.lexer import RegexLexer, include
from pygments.token import (
    Comment,
    Error,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
)

__all__ = ["KdlLexer"]

# Bare identifiers per the KDL spec: letters, digits, and the symbol set.
_ident = r"[a-zA-Z0-9_\-+.!$%&*?<>=@^~|/][a-zA-Z0-9_\-.!$%&*+?<>=@^~|/]*"


class KdlLexer(RegexLexer):
    name = "KDL"
    aliases = ["kdl"]
    filenames = ["*.kdl"]
    mimetypes = ["text/kdl"]
    url = "https://kdl.dev"

    tokens = {
        "root": [include("node")],
        "whitespace": [
            (r"\s+", Text),
            (r"//[^\n]*", Comment.Single),
            (r"/\*.*?\*/", Comment.Multiline),
            (r"/-[^\n]*", Comment.Single),
        ],
        "node": [
            include("whitespace"),
            (r"\}", Punctuation, "#pop"),
            (r'@?"', String, ("#push", "str-or-node")),
            (_ident, Name.Tag, "args"),
            (r".", Error),
        ],
        "args": [
            include("whitespace"),
            (r"\{", Punctuation, ("#push", "node")),
            (r"\}", Punctuation, "#pop"),
            (r";", Punctuation),
            (r"\\[ \t]*\n", Text),
            (r"#[a-zA-Z]+", Keyword.Constant),
            (r"-?0[xX][0-9a-fA-F_]+", Number.Hex),
            (r"-?\d[\d_]*\.[\d_]+([eE][-+]?\d+)?", Number.Float),
            (r"-?\d[\d_]*([eE][-+]?\d+)?", Number.Integer),
            (r'@?"', String, "string"),
            (_ident + r'(?=\s*=(?!=))', Name.Attribute),
            (_ident, Text),
            (r"=", Operator),
            (r"[<>(),]", Punctuation),
        ],
        "str-or-node": [
            (_ident + r'(?=")', Name.Tag, ("#pop", "args")),
            (r'"', String, "#pop"),
            (r".", Error),
        ],
        "string": [
            (r'""[ \t]*\n', String.Doc, "multiline"),
            (r"\\.", String.Escape),
            (r'"', String, "#pop"),
            (r'[^"\\\n]+', String),
            (r"\\", String.Escape),
        ],
        "multiline": [
            (r'"""', String.Doc, "#pop"),
            (r'""(?!")', String.Doc),
            (r'"', String.Doc),
            (r'[^"]+', String.Doc),
        ],
    }
