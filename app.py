from flask import Flask, request, jsonify, render_template
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Firebase 초기화
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return render_template("index.html")

# CREATE
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.json

    doc_ref = db.collection("todos").document()

    todo = {
        "title": data["title"],
        "completed": False
    }

    doc_ref.set(todo)

    return jsonify({
        "id": doc_ref.id,
        **todo
    })

# READ ALL
@app.route("/todos", methods=["GET"])
def get_todos():
    docs = db.collection("todos").stream()

    todos = []

    for doc in docs:
        item = doc.to_dict()
        item["id"] = doc.id
        todos.append(item)

    return jsonify(todos)

# READ ONE
@app.route("/todos/<todo_id>", methods=["GET"])
def get_todo(todo_id):
    doc = db.collection("todos").document(todo_id).get()

    if not doc.exists:
        return jsonify({"error": "Not found"}), 404

    data = doc.to_dict()
    data["id"] = doc.id

    return jsonify(data)

# UPDATE
@app.route("/todos/<todo_id>", methods=["PUT"])
def update_todo(todo_id):
    data = request.json

    db.collection("todos").document(todo_id).update(data)

    return jsonify({
        "message": "updated"
    })

# DELETE
@app.route("/todos/<todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db.collection("todos").document(todo_id).delete()

    return jsonify({
        "message": "deleted"
    })

if __name__ == "__main__":
    app.run(debug=True)
