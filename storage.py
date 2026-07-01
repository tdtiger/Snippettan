import json
import uuid
from datetime import datetime

# スニペットの保存ファイル
DATA_FILE = "snippets.json"

# 設定用ファイル
SETTINGS_FILE = "settings.json"

# JSONファイルからスニペットを読み取る
def load_data():
    try:
        with open(DATA_FILE, "r", encoding = "utf-8") as f:
            data = json.load(f)
    except:
        return []
    
    changed = False

    # アップデートに伴う旧データ整形
    for item in data:
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            changed = True
        
        if "favorite" not in item:
            item["favorite"] = False
            changed = True

        if "created_at" not in item:
            item["created_at"] = now_iso()
            changed = True

        if "updated_at" not in item:
            item["updated_at"] = item["created_at"]
            changed = True

        if "last_used" not in item:
            item["last_used"] = None
            changed = True

        if "author" not in item:
            item["author"] = ""
            changed = True

        if "is_remote" not in item:
            item["is_remote"] = False
            changed = True

        if "remote_id" not in item:
            item["remote_id"] = None
            changed = True

        if "version" not in item:
            item["version"] = 1
            changed = True

    if changed:
        save_data(data)

    return data
    
# JSONファイルにスニペットを書き込む
def save_data(data):
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

# 新規スニペットを作成する
def create_snippet(title, code, tags, language):
    now = now_iso()

    return{
        "id": str(uuid.uuid4()),
        "title": title,
        "code": code,
        "tags": tags,
        "language": language,
        "favorite": False,
        "created_at": now,
        "updated_at": now,
        "last_used": None,
        "author": "",
        "is_remote": False,
        "remote_id": None,
        "version": 1
    }

# 設定をJSONファイルから読み込む
def load_settings():
    try:
        with open(SETTINGS_FILE, "r", encoding = "utf-8") as f:
            return json.load(f)
    except:
        return {"theme": "light"}
    
# 設定をJSONファイルに保存する
def save_settings(settings):
    with open(SETTINGS_FILE, "w", encoding = "utf-8") as f:
        json.dump(settings, f, ensure_ascii = False, indent = 4)

# 時間を取得
def now_iso():
    return datetime.now().isoformat(timespec = "seconds")