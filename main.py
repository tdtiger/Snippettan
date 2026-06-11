import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton, QMessageBox
from PyQt6.QtCore import QTimer
from themes import LIGHT_THEME, DARK_THEME
from widgets import SnippetCard, AppDialog
from storage import load_data, save_data, create_snippet

# 本体となるクラス
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

        self.dark_mode = False
        self.setStyleSheet(LIGHT_THEME)

        self.theme_button = QPushButton("テーマ切替")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        layout.addWidget(self.theme_button)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        container = QWidget()
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setSpacing(12)

        self.data = load_data()

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
    
    # カードを描画する
    def render_cards(self, data):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for s in data:
            snippet_id = s["id"]
            self.container_layout.addWidget(SnippetCard(s["title"], 
                                                        s["code"], 
                                                        s["tags"], 
                                                        s.get("language", "python"), 
                                                        self.tag_clicked, 
                                                        lambda i = snippet_id: self.edit_snippet(i), 
                                                        lambda i = snippet_id: self.delete_snippet(i), 
                                                        lambda t = s["title"]: self.show_status(f"{t} をコピーしました")
                                                        )
                                            )
        
        self.container_layout.addStretch()
    
    # 検索ワードに基づいてフィルタリングする
    def filter(self):
        keyword = self.search.text().lower()
        filtered = [s for s in self.data if keyword in s["title"].lower() or any(keyword in t.lower() for t in s["tags"])]
        self.render_cards(filtered)
    
    # スニペットを追加するためのダイアログを開く
    def open_add_dialog(self):
        dialog = AppDialog()

        if dialog.exec():
            new_data = dialog.get_data()
            new_data = create_snippet(new_data["title"], new_data["code"], new_data["tags"], new_data["language"])
            self.data.append(new_data)
            save_data(self.data)
            self.render_cards(self.data)
            self.show_status(f"{new_data['title']} を追加しました")
    
    # クリックされたタグを検索対象にする
    def tag_clicked(self, tag):
        self.search.setText(tag)

    # スニペットを編集するためのダイアログを開く
    def edit_snippet(self, snippet_id):
        index, data = self.find_snippet_by_id(snippet_id)
        if data is None:
            self.show_status("スニペットが見つかりません")
            return

        dialog = AppDialog()
        dialog.title_input.setText(data["title"])
        dialog.code_input.setPlainText(data["code"])
        dialog.tag_input.setText(" ".join(data["tags"]))
        dialog.language_input.setCurrentText(data.get("language", "python"))

        dialog.update_language()

        if dialog.exec():
            updated = dialog.get_data()
            updated["id"] = snippet_id

            self.data[index] = updated
            save_data(self.data)
            self.render_cards(self.data)
            self.show_status(f"{data['title']} を更新しました")

    # スニペットを削除する
    def delete_snippet(self, snippet_id):
        index, data = self.find_snippet_by_id(snippet_id)
        if data is None:
            self.show_status("スニペットが見つかりません")
            return

        reply = QMessageBox.question(self, 
                                    "確認", 
                                    "このスニペットを削除しますか？", 
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                                    )
        if reply == QMessageBox.StandardButton.Yes:
            title = data["title"]
            del self.data[index]
            save_data(self.data)
            self.render_cards(self.data)
            self.show_status(f"{title} を削除しました")
    
    # 直前の動作を表示する
    def show_status(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))

    # ライトモードとダークモードを切り替える
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
        else:
            self.setStyleSheet(LIGHT_THEME)
    
    # IDを基にスニペットを検索する
    def find_snippet_by_id(self, snippet_id):
        for i, snippet in enumerate(self.data):
            if snippet["id"] == snippet_id:
                return i, snippet
        return None, None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())