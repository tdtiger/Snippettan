import sys
import json
import re
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QScrollArea, QLineEdit, QTextEdit, QDialog, QPushButton, QMenu, QMessageBox, QComboBox
from PyQt6.QtGui import QFont, QTextCursor, QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import Qt, QTimer

LANG_KEYWORDS = {
    "python": ["False", "None", "True", "and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif", "else", "except", "finally", "for", "from", "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try", "while", "with", "yield"],
    "c++": ["alignas", "alignof", "and", "and_eq", "asm", "auto", "bitand", "bitor", "bool", "break", "case", "catch", "char", "char_8t", "char16_t", "char32_t", "class", "compl", "const", "constexpr", "const_cast", "continue", "decltype", "default", "delete", "do", "double", "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false", "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable", "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator", "or", "or_eq", "private", "protected", "public", "register", "reinterpret_cast", "requires", "return", "short", "signed", "sizeof", "static", "static_assert", "static_cast", "struct", "switch", "template", "this", "thread_local", "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned", "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"],
    "javascript": ["break", "case", "catch", "class", "const", "continue", "debugger", "default", "delete", "do", "else", "export", "extends", "false", "finally", "for", "function", "if", "import", "in", "instanceof", "new", "null", "return", "super", "switch", "this", "throw", "true", "try", "typeof", "var", "void", "while", "with"],
    "ruby": ["BEGIN", "END", "alias", "and", "begin", "break", "case", "class", "def", "defined?", "do", "else", "elsif", "end", "ensure", "false", "for", "if", "in", "module", "next", "nil", "not", "or", "redo", "rescue", "retry", "return", "self", "super", "then", "true", "undef", "unless", "until", "when", "while", "yield", "__LINE__", "__FILE__", "__ENCODING__"]
}

class CodeEditor(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")
        else:
            super().keyPressEvent(event)

class SimpleHighlighter(QSyntaxHighlighter):
    def __init__(self, document, language = "python"):
        super().__init__(document)
        self.language = language
        self.update_rules()

    def update_rules(self):
        self.rules = []

        keywords = LANG_KEYWORDS.get(self.language, [])
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#007acc"))

        for word in keywords:
            pattern = re.compile(rf"\b{word}\b")
            self.rules.append((pattern, keyword_format))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#a31515"))
        self.rules.append((re.compile(r'".*?"'), string_format))
        self.rules.append((re.compile(r"'.*?'"), string_format))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955"))
        self.rules.append((re.compile(r"#.*"), comment_format)) 
        self.rules.append((re.compile(r"//.*"), comment_format))

    def highlightBlock(self, text):
        for pattern, fmt in self.rules:
            for match in pattern.finditer(text):
                start, end = match.span()
                self.setFormat(start, end - start, fmt)
                
    def set_language(self, language):
        self.language = language
        self.update_rules()
        self.rehighlight()
        
class SnippetCard(QFrame):
    def __init__(self, title, code, tags, language, on_tag_click, on_edit, on_delete, on_copy):
        super().__init__()
        self.code = code
        self.on_tag_click = on_tag_click
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.on_copy = on_copy
        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setStyleSheet("""
            font-weight: bold;
            font-size: 16px;
            margin-bottom: 4px;
        """)
        layout.addWidget(self.title)

        self.language_label = QLabel(language)
        self.language_label.setStyleSheet("""
            font-size: 11px;
            color: #007acc;
            background: #e6f2ff;
            padding: 2px 6px;
            margin-bottom: 4px;
            max-width: 80px; 
        """)
        language_layout = QHBoxLayout()
        language_layout.addWidget(self.language_label)
        language_layout.addStretch()
        layout.addLayout(language_layout)

        self.code_label = QLabel(code)
        self.code_label.setFont(QFont("Courier New"))
        self.code_label.setStyleSheet("""
            color: #333;
            background: #f8f8f8;
            padding: 6px;
            border-radius: 4px;
        """)
        self.code_label.setWordWrap(True)
        layout.addWidget(self.code_label)

        tag_layout = QHBoxLayout()
        for tag in tags:
            tag_label = QLabel(tag)
            tag_label.setStyleSheet("""
                background: #eee;
                border-radius: 6px;
                padding: 2px 6px;
                font-size: 11px;
                color: #555;
            """)
            tag_label.setCursor(Qt.CursorShape.PointingHandCursor)
            tag_label.mousePressEvent = lambda e, t = tag: self.on_tag_click(t)
            tag_layout.addWidget(tag_label)
        tag_layout.addStretch()
        layout.addLayout(tag_layout)

        self.setLayout(layout)
        self.setObjectName("card")
        self.setStyleSheet("""
            QFrame#card {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                background: white;
            }
            QFrame#card:hover{
                background: #f5f5f5;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.code)
            self.on_copy()
        elif event.button() == Qt.MouseButton.RightButton:
            menu = QMenu()
            edit_action = menu.addAction("編集")
            delete_action = menu.addAction("削除")
            action = menu.exec(event.globalPosition().toPoint())

            if action == edit_action:
                self.on_edit()
            elif action == delete_action:
                self.on_delete()

class AppDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("スニペット追加")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("タイトル")
        layout.addWidget(self.title_input)

        self.language_input = QComboBox()
        self.language_input.addItems(["python", "c++", "javascript", "ruby"])
        self.language_input.currentTextChanged.connect(self.update_language)
        layout.addWidget(self.language_input)

        self.code_input = CodeEditor()
        self.code_input.setPlaceholderText("コード")
        layout.addWidget(self.code_input)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("タグ (スペース区切り)")
        self.tag_input.textChanged.connect(self.update_language)
        layout.addWidget(self.tag_input)

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

        self.highlighter = SimpleHighlighter(self.code_input.document(), "python")

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "code": self.code_input.toPlainText(),
            "tags": self.tag_input.text().split(),
            "language": self.language_input.currentText()
        }

    def update_language(self):
        lang = self.language_input.currentText()
        self.highlighter.set_language(lang)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("すにぺったん")
        self.resize(500, 400)

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("検索(タイトル・タグ)")
        layout.addWidget(self.search)

        self.search.textChanged.connect(self.filter)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(12)

        self.data = self.load_data()

        self.render_cards(self.data)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.add_button = QPushButton("スニペット追加")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #666;
            padding: 6px;
            border-top: 1px solid #ddd;
        """)
        layout.addWidget(self.status_label)

        self.setLayout(layout)
    
    def load_data(self):
        try:
            with open("snippets.json", "r", encoding = "utf-8") as f:
                return json.load(f)
        except:
            return []
    
    def save_data(self):
        with open("snippets.json", "w", encoding = "utf-8") as f:
            json.dump(self.data, f, ensure_ascii = False, indent = 4)
    
    def render_cards(self, data):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for s in data:
            index = self.data.index(s)
            self.container_layout.addWidget(SnippetCard(s["title"], s["code"], s["tags"], s.get("language", "python"),self.tag_clicked, lambda i = index: self.edit_snippet(i), lambda i = index: self.delete_snippet(i), lambda t = s["title"]: self.show_status(f"{t} をコピーしました")))
        
        self.container_layout.addStretch()
    
    def filter(self):
        keyword = self.search.text().lower()
        filtered = [s for s in self.data if keyword in s["title"].lower() or any(keyword in t.lower() for t in s["tags"])]
        self.render_cards(filtered)
    
    def open_add_dialog(self):
        dialog = AppDialog()

        if dialog.exec():
            new_data = dialog.get_data()
            self.data.append(new_data)
            self.save_data()
            self.render_cards(self.data)
            self.show_status(f"{new_data['title']} を追加しました")
    
    def tag_clicked(self, tag):
        self.search.setText(tag)

    def edit_snippet(self, index):
        data = self.data[index]

        dialog = AppDialog()
        dialog.title_input.setText(data["title"])
        dialog.code_input.setPlainText(data["code"])
        dialog.tag_input.setText(" ".join(data["tags"]))
        dialog.language_input.setCurrentText(data.get("language", "python"))

        dialog.update_language()

        if dialog.exec():
            updated = dialog.get_data()
            self.data[index] = updated
            self.save_data()
            self.render_cards(self.data)
            self.show_status(f"{data['title']} を更新しました")

    def delete_snippet(self, index):
        reply = QMessageBox.question(self, "確認", "このスニペットを削除しますか？", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            title = self.data[index]["title"]
            del self.data[index]
            self.save_data()
            self.render_cards(self.data)
            self.show_status(f"{title} を削除しました")
    
    def show_status(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())