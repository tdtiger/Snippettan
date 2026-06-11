# 各言語の構文ルールを定義する辞書
PYTHON_RULES = {
    "#c678dd":[
        "if", "elif", "else", "for", "while", "break", "continue", "return", "yield", "try", "except", "finally", "raise", "with", "pass"
    ],
    "#e5c70b": [
        "def", "class", "lambda", "global", "nonlocal", "del"
    ],
    "#98c379":[
        "import", "from", "as"
    ],
    "#56b6c2":[
        "and", "or", "not", "in", "is"
    ],
    "#e06c75":[
        "async", "await"
    ],
    "#61afef":[
        "True", "False", "None"
    ],
    "#d19a66":[
        "assert"
    ]
}

CPP_RULES = {
    "#c678dd":[
        "if", "else", "switch", "case", "default", "for", "while", "do", "break", "continue", "return", "try", "catch", "throw", "goto"
    ],
    "#61afef":[
        "bool", "char", "char8_t", "char16_t", "char32_t", "wchar_t", "short", "int", "long", "signed", "unsigned", "float", "double", "void", "auto"
    ],
    "#e5c70b":[
        "class", "struct", "union", "enum", "template", "typename", "typedef", "using", "namespace", "public", "private", "protected", "friend", "virtual", "this"
    ],
    "#e06c75":[
        "new", "delete", "nullptr", "const_cast",  "static_cast", "reinterpret_cast", "dynamic_cast"
    ],
    "#98c379":[
        "const", "constexpr", "static", "inline", "volatile", "mutable", "thread_local", "extern", "register", "noexcept"
    ],
    "#56b6c2":[
        "and", "or", "not", "xor", "and_eq", "or_eq", "not_eq", "xor_eq", "bitand", "bitor", "compl"
    ],
    "#d19a66":[
        "true", "false", "sizeof", "typeid", "operator", "requires", "asm", "export"
    ]
}

LANG_RULES = {
    "python": PYTHON_RULES,
    "c++": CPP_RULES,
    # "javascript": ["break", "case", "catch", "class", "const", "continue", "debugger", "default", "delete", "do", "else", "export", "extends", "false", "finally", "for", "function", "if", "import", "in", "instanceof", "new", "null", "return", "super", "switch", "this", "throw", "true", "try", "typeof", "var", "void", "while", "with"],
    # "ruby": ["BEGIN", "END", "alias", "and", "begin", "break", "case", "class", "def", "defined?", "do", "else", "elsif", "end", "ensure", "false", "for", "if", "in", "module", "next", "nil", "not", "or", "redo", "rescue", "retry", "return", "self", "super", "then", "true", "undef", "unless", "until", "when", "while", "yield", "__LINE__", "__FILE__", "__ENCODING__"]
}