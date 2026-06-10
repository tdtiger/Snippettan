from highlighter import SimpleHighlighter
from PyQt6.QtWidgets import QTextEdit, QFrame, QLabel, QVBoxLayout, QHBoxLayout, QDialog, QPushButton, QLineEdit, QComboBox, QMenu, QApplication
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class CodeEditor(QTextEdit):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText("    ")
        else:
            super().keyPressEvent(event)

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
        self.code_label.setObjectName("code")
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