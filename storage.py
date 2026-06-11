import json
import uuid

# スニペットの保存ファイル
DATA_FILE = "snippets.json"

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

    if changed:
        save_data(data)

    return data
    
# JSONファイルにスニペットを書き込む
def save_data(data):
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

# 新規スニペットを作成する
def create_snippet(title, code, tags, language):
    return{
        "id": str(uuid.uuid4()),
        "title": title,
        "code": code,
        "tags": tags,
        "language": language,
        "favorite": False
    }