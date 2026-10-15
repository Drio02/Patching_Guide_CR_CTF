# Flask + pymongo

import hmac
from flask import Flask, request, session, jsonify, abort
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient("mongodb://mongo:27017").app

def as_str(value) -> str:
    # Rechaza dicts/listas: un operador ($ne, $regex, ...) nunca llega al filtro
    if not isinstance(value, str):
        abort(400)
    return value

# Patch: tipos forzados y password comparado en codigo
@app.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    user = db.users.find_one({"username": as_str(data.get("username"))})
    if not user or not hmac.compare_digest(user["password"], as_str(data.get("password"))):
        return "bad credentials", 401
    session["user"] = user["username"]
    return "ok"

# Patch: busqueda exacta, restringida al dueño
@app.get("/notes/search")
def search():
    q = request.get_json(silent=True) or {}
    return jsonify(list(db.notes.find(
        {"title": as_str(q.get("title")), "owner": session.get("user")}, {"_id": 0})))
