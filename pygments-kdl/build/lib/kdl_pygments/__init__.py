"""A Pygments lexer for KDL, the document language OpenLych configs are written in.

Implements the parts of the KDL spec the config dialect uses: node names,
positional arguments, `key=value` properties, `#true`/`#false`/`#null`,
numbers (signs, hex, exponents), quoted strings with escapes and multiline
raw strings, `//` and `/* */` comments, slashdash (`/-`) hiding, `;`
separators, `{ ... }` child blocks, and `\\` line continuation.

The lexer tracks "node position" (line start, or right after `{` / `;`) with
the state stack: a node name switches to `args`, a newline in `args` pops back
to node position, and `{` pushes a fresh node position for the block's
children. Pygments states are pushed, not replaced, so every transition here
is written with that in mind.
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

_comments = [
    (r"//[^\n]*", Comment.Single),
    (r"/\*.*?\*/", Comment.Multiline),
    (r"/-[^\n]*", Comment.Single),
]


class KdlLexer(RegexLexer):
    name = "KDL"
    aliases = ["kdl"]
    filenames = ["*.kdl"]
    mimetypes = ["text/kdl"]
    url = "https://kdl.dev"

    tokens = {
        "root": [  # node position: line start, or just after `{` / `;`
            *_comments,
            (r"\n", Text),
            (r"[ \t]+", Text),
            (r"\}", Punctuation),
            (r'@?"', String, ("#push", "str-or-node")),
            (_ident, Name.Tag, "args"),
            (r".", Error),
        ],
        "args": [
            *_comments,
            (r"\\[ \t]*\n", Text),  # line continuation: stay in args
            (r"\n", Text, ("#pop",)),  # next line starts in node position
            (r"[ \t]+", Text),
            (r"\{", Punctuation, "root"),
            (r"\}", Punctuation, ("#pop",)),
            (r";", Punctuation, ("#pop", "#push")),
            (r"#[a-zA-Z]+", Keyword.Constant),
            (r"-?0[xX][0-9a-fA-F_]+", Number.Hex),
            (r"-?\d[\d_]*\.[\d_]+([eE][-+]?\d+)?", Number.Float),
            (r"-?\d[\d_]*([eE][-+]?\d+)?", Number.Integer),
            (r'@?"', String, "string"),
            (_ident + r'(?=\s*=(?!=))', Name.Attribute),
            (_ident, Text),
            (r"=", Operator),
            (r"[<>\[\](),]", Punctuation),
        ],
        "str-or-node": [
            (_ident + r'(?=")', Name.Tag, ("#pop", "args")),
            (r'"', String, "#pop"),
            (r".", Error),
        ],
        "string": [
            (r'""[ \t]*\n', String, ("#pop", "multiline")),
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
