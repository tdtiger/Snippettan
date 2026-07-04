import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QLineEdit, QPushButton, QMessageBox, QComboBox
from PyQt6.QtCore import QTimer
from themes import LIGHT_THEME, DARK_THEME
from widgets import SnippetCard, AppDialog
from storage import load_data, save_data, create_snippet, load_settings, save_settings, now_iso

# 本体となるクラス
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("すにぺったん")
        self.resize(700, 600)
        
        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("検索(タイトル・タグ)")
        layout.addWidget(self.search)

        self.search.textChanged.connect(self.filter)

        filter_layout = QHBoxLayout()

        language_label = QLabel("言語：")
        self.language_filter = QComboBox()
        self.language_filter.addItems(["すべて", "python", "c++", "javascript", "ruby"])
        self.language_filter.currentTextChanged.connect(self.filter)

        favorite_label = QLabel("表示：")
        self.favorite_filter = QComboBox()
        self.favorite_filter.addItems(["すべて", "お気に入りのみ"])
        self.favorite_filter.currentTextChanged.connect(self.filter)

        sort_label = QLabel("並び順：")
        self.sort_filter = QComboBox()
        self.sort_filter.addItems(["作成順", "タイトル順", "言語順", "お気に入り優先", "最近使った順", "使用回数順"])
        self.sort_filter.currentTextChanged.connect(self.filter)

        filter_layout.addWidget(language_label)
        filter_layout.addWidget(self.language_filter)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(favorite_label)
        filter_layout.addWidget(self.favorite_filter)
        filter_layout.addSpacing(20)
        filter_layout.addWidget(sort_label)
        filter_layout.addWidget(self.sort_filter)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        self.settings = load_settings()
        self.dark_mode = self.settings.get("theme") == "dark"
        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
        else:
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

        scroll.setWidget(container)
        layout.addWidget(scroll)

        self.add_button = QPushButton("スニペット追加")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.count_label = QLabel("")
        self.count_label.setStyleSheet("""
            color: #666;
            padding: 4px 6px;
            font-size: 12px;
        """)
        layout.addWidget(self.count_label)

        self.status_label = QLabel("")
        self.status_label.setStyleSheet("""
            color: #666;
            padding: 6px;
            border-top: 1px solid #ddd;
        """)
        layout.addWidget(self.status_label)

        self.render_cards(self.data)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.create_menu_bar()

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
                                                        s.get("favorite", False),
                                                        self.tag_clicked, 
                                                        lambda i = snippet_id: self.edit_snippet(i), 
                                                        lambda i = snippet_id: self.delete_snippet(i), 
                                                        lambda sid = snippet_id: self.update_snippet_usage(sid),
                                                        lambda sid = snippet_id: self.toggle_favorite(sid),
                                                    )
                                            )
        
        self.container_layout.addStretch()

        self.count_label.setText(f"{len(data)}件表示中 / 全{len(self.data)}件")
    
    # 検索ワードに基づいてフィルタリングする
    # タイトルの検索と、言語タグ両方にマッチしたもののみを表示する
    # 並び替え機能も提供
    def filter(self):
        keyword = self.search.text().lower()
        selected_language = self.language_filter.currentText()
        selected_favorite = self.favorite_filter.currentText()
        selected_sort = self.sort_filter.currentText()
        filtered = []

        for snippet in self.data:
            keyword_match = (
                keyword in snippet.get("title", "").lower()
                or keyword in snippet.get("code", "").lower()
                or keyword in snippet.get("language", "").lower()
                or any(
                    keyword in tag.lower()
                    for tag in snippet.get("tags", [])
                )
            )

            language_match = (
                selected_language == "すべて"
                or snippet.get("language") == selected_language
            )

            favorite_match = (
                selected_favorite == "すべて"
                or snippet.get("favorite", False)
            )

            if keyword_match and language_match and favorite_match:
                filtered.append(snippet)
        
        if selected_sort == "タイトル順":
            filtered.sort(key = lambda s: s.get("title", "").lower())
        elif selected_sort == "言語順":
            filtered.sort(key = lambda s: (s.get("language", ""), s.get("title", "").lower()))
        elif selected_sort == "お気に入り優先":
            filtered.sort(key = lambda s: (not s.get("favorite", False), s.get("title", "").lower()))
        elif selected_sort == "最近使った順":
            filtered.sort(key = lambda s: s.get("last_used") or "", reverse = True)
        elif selected_sort == "使用回数順":
            filtered.sort(key = lambda s: s.get("use_count", 0), reverse = True)
        self.render_cards(filtered)
    
    # スニペットを追加するためのダイアログを開く
    def open_add_dialog(self):
        dialog = AppDialog()

        if dialog.exec():
            new_data = dialog.get_data()
            new_data = create_snippet(new_data["title"], new_data["code"], new_data["tags"], new_data["language"])
            self.data.append(new_data)
            save_data(self.data)
            self.filter()
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
            updated["favorite"] = data.get("favorite", False)
            updated["created_at"] = data.get("created_at")
            updated["updated_at"] = now_iso()
            updated["last_used"] = data.get("last_used")
            updated["author"] = data.get("author", "")
            updated["is_remote"] = data.get("is_remote")
            updated["remote_id"] = data.get("remote_id")
            updated["version"] = data.get("version", 1)
            self.data[index] = updated
            save_data(self.data)
            self.filter()
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
            self.filter()
            self.show_status(f"{title} を削除しました")

    # スニペットの使用履歴を更新する
    def update_snippet_usage(self, snippet_id):
        index, data = self.find_snippet_by_id(snippet_id)

        if data is None:
            self.show_status("スニペットが見つかりません")
            return
        
        data["last_used"] = now_iso()
        data["use_count"] = data.get("use_count", 0) + 1

        save_data(self.data)
        self.filter()
    
        self.show_status(f"{data['title']} をコピーしました")

    # 直前の動作を表示する
    def show_status(self, message):
        self.status_label.setText(message)
        QTimer.singleShot(2000, lambda: self.status_label.setText(""))

    # ライトモードとダークモードを切り替える
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.setStyleSheet(DARK_THEME)
            self.settings["theme"] = "dark"
        else:
            self.setStyleSheet(LIGHT_THEME)
            self.settings["theme"] = "light"
        
        save_settings(self.settings)
    
    # IDを基にスニペットを検索する
    def find_snippet_by_id(self, snippet_id):
        for i, snippet in enumerate(self.data):
            if snippet["id"] == snippet_id:
                return i, snippet
        return None, None
    
    # スニペットのお気に入りのオン・オフを切り替える
    def toggle_favorite(self, snippet_id):
        index, data = self.find_snippet_by_id(snippet_id)

        if data is None:
            return
        
        data["favorite"] = not data["favorite"]
        save_data(self.data)
        self.filter()

        state = "お気に入りに追加" if data["favorite"] else "お気に入り解除"
        self.show_status(f"{data['title']} を{state}しました")

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("ファイル")
        view_menu = menu_bar.addMenu("表示")
        help_menu = menu_bar.addMenu("ヘルプ")

        new_action = file_menu.addAction("新規スニペット")
        new_action.triggered.connect(self.open_add_dialog)

        file_menu.addSeparator()

        import_action = file_menu.addAction("インポート…")
        import_action.triggered.connect(self.import_snippets)

        export_action = file_menu.addAction("エクスポート…")
        export_action.triggered.connect(self.export_snippets)

        file_menu.addSeparator()

        quit_action = file_menu.addAction("終了")
        quit_action.triggered.connect(self.close)

        theme_action = view_menu.addAction("テーマ切替")
        theme_action.triggered.connect(self.toggle_theme)

        shortcut_action = help_menu.addAction("ショートカット一覧")
        shortcut_action.triggered.connect(self.show_shortcuts)

        about_action = help_menu.addAction("このアプリについて")
        about_action.triggered.connect(self.show_about)

    def import_snippets(self):
        self.show_status("インポート機能はまだ実装されていません")

    def export_snippets(self):
        self.show_status("エクスポート機能はまだ実装されていません")

    def show_shortcuts(self):
        self.show_status("ショートカット一覧はまだ実装されていません")

    def show_about(self):
        QMessageBox.information(self, "このアプリについて", "すにぺったん\nローカルで動作するスニペット管理アプリケーションです。")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())