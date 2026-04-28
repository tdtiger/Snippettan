import sys
import json
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame, QScrollArea, QLineEdit, QTextEdit, QDialog, QPushButton
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

class SnippetCard(QFrame):
    def __init__(self, title, code, tags):
        super().__init__()
        self.code = code
        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title)

        self.code_label = QLabel(code)
        self.code_label.setFont(QFont("Courier New"))
        self.code_label.setStyleSheet("color: #333;")
        self.code_label.setWordWrap(True)
        layout.addWidget(self.code_label)

        self.tag_label = QLabel(" ".join(tags))
        self.tag_label.setStyleSheet("color: #888; font-size: 12px;")
        layout.addWidget(self.tag_label)

        self.setLayout(layout)
        self.setStyleSheet("""
            QFrame {
                border: 1px solid #ddd;
                border-radius: 10px;
                padding: 10px;
                background: white;
            }
            QFrame:hover{
                background: #f5f5f5;
            }
        """)

    def mousePressEvent(self, event):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code)
        print("Copied!")

class AppDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("スニペット追加")

        layout = QVBoxLayout()

        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("タイトル")
        layout.addWidget(self.title_input)

        self.code_input = QTextEdit()
        self.code_input.setPlaceholderText("コード")
        layout.addWidget(self.code_input)

        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("タグ (スペース区切り)")
        layout.addWidget(self.tag_input)

        self.save_btn = QPushButton("保存")
        self.save_btn.clicked.connect(self.accept)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def get_data(self):
        return {
            "title": self.title_input.text(),
            "code": self.code_input.toPlainText(),
            "tags": self.tag_input.text().split()
        }

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

        self.data = self.load_data()

        self.render_cards(self.data)

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.add_button = QPushButton("スニペット追加")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

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
            self.container_layout.addWidget(SnippetCard(s["title"], s["code"], s["tags"]))
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())