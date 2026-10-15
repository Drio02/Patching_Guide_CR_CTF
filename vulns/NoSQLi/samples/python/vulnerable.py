# Flask + pymongo

from flask import Flask, request, session, jsonify
from pymongo import MongoClient

app = Flask(__name__)
db = MongoClient("mongodb://mongo:27017").app

# Vuln: el JSON del cliente entra directo en el filtro
@app.post("/login")
def login():
    data = request.get_json()
    user = db.users.find_one({"username": data["username"], "password": data["password"]})
    # {"username": "admin", "password": {"$ne": ""}}
    if not user:
        return "bad credentials", 401
    session["user"] = user["username"]
    return "ok"

# Vuln: $regex controlado por el usuario para extraer flags
@app.get("/notes/search")
def search():
    q = request.get_json()
    return jsonify(list(db.notes.find({"title": q["title"]}, {"_id": 0})))
    # {"title": {"$regex": ".*"}}
