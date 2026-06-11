from syntax_rules import LANG_RULES
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
import re

# 予約語、文字列、コメントを検出して色付けする。
# 自動検出とかではなく、愚直に決め打ち。
class SimpleHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language = "python"):
        super().__init__(document)
        self.language = language
        self.update_rules()

    # 選択されている言語が更新された時、ハイライトのルールも更新
    def update_rules(self):
        self.rules = []

        lang_rules = LANG_RULES.get(self.language, {})
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#007acc"))

        for color, words in lang_rules.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))

            for word in words:
                pattern = re.compile(rf"\b{word}\b")
                self.rules.append((pattern, fmt))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a31515"))
        self.rules.append((re.compile(r'".*?"'), string_format))
        self.rules.append((re.compile(r"'.*?'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955"))
        self.rules.append((re.compile(r"#.*"), comment_format)) 
        self.rules.append((re.compile(r"//.*"), comment_format))

    # ハイライトする部分を検出して、対応するフォーマットを適用する
    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
                
    # 言語を変更する
    def set_language(self, language):
        self.language = language
        self.update_rules()
        self.rehighlight()
        