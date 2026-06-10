import json

def load_data():
    try:
        with open("snippets.json", "r", encoding = "utf-8") as f:
            return json.load(f)
    except:
        return []
    
def save_data(self):
    with open("snippets.json", "w", encoding = "utf-8") as f:
        json.dump(self.data, f, ensure_ascii = False, indent = 4)