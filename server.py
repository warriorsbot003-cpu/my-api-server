from flask import Flask, request, jsonify
import os, json, time

app = Flask(__name__)
DATA_FILE = "data.json"

def load_all():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_all(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

@app.get("/health")
def health():
    return jsonify({"ok": True, "time": int(time.time())})

@app.post("/upload")
def upload():
    payload = request.get_json(silent=True)
    if payload is None:
        return jsonify({"ok": False, "error": "Send JSON body"}), 400

    items = load_all()
    record = {
        "ts": int(time.time()),
        "data": payload
    }
    items.append(record)
    items = items[-200:]
    save_all(items)

    return jsonify({"ok": True, "saved": True})

@app.get("/latest")
def latest():
    items = load_all()
    return jsonify(items[-1] if items else {"empty": True})

@app.get("/all")
def all_data():
    return jsonify(load_all())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)