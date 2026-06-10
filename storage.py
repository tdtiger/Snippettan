import json
import uuid

DATA_FILE = "snippets.json"

def load_data():
    try:
        with open(DATA_FILE, "r", encoding = "utf-8") as f:
            data = json.load(f)
    except:
        return []
    
    changed = False

    for item in data:
        if "id" not in item:
            item["id"] = str(uuid.uuid4())
            changed = True

    if changed:
        save_data(data)

    return data
    
def save_data(data):
    with open(DATA_FILE, "w", encoding = "utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def create_snippet(title, code, tags, language):
    return{
        "id": str(uuid.uuid4()),
        "title": title,
        "code": code,
        "tags": tags,
        "language": language
    }