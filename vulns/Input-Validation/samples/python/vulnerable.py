# Flask + sqlite3

import re
from flask import Flask, request, session

app = Flask(__name__)

# Vuln 1: monto sin validar -> negativo o NaN
@app.post("/transfer")
def transfer():
    amount = float(request.form["amount"])       # "-1000" o "nan"
    balance = get_balance(session["user"])
    if amount > balance:                          # NaN > x es False -> pasa
        return "insufficient funds", 400
    move_money(session["user"], request.form["to"], amount)
    return "ok"

# Vuln 2: mass assignment
@app.post("/register")
def register():
    user = User(**request.get_json())             # {"username": "x", "password": "y", "is_admin": true}
    db.session.add(user)
    db.session.commit()
    return "ok"

# Vuln 3: $ acepta un "\n" final y re.match no exige el final del string
USER_RE = re.compile(r"^[a-z0-9_]+$")

@app.post("/signup")
def signup():
    username = request.form["username"]           # "eve\nadmin:x:1"
    if not USER_RE.match(username):
        return "bad username", 400
    # Vuln 4: almacenamiento por lineas -> el "\n" crea un registro extra
    with open("/data/users.txt", "a") as f:
        f.write(f"{username}:{request.form['password']}:0\n")
    return "ok"

# Vuln 5: ReDoS (cuantificadores anidados) y sin limite de longitud
EMAIL_RE = re.compile(r"^([a-zA-Z0-9]+)*@example\.com$")

@app.post("/newsletter")
def newsletter():
    if EMAIL_RE.match(request.form["email"]):     # "aaaaaaaaaaaaaaaaaaaaaaaaaaaa!" -> segundos de CPU
        return "subscribed"
    return "invalid", 400

# Vuln 6: unicidad sin normalizar
@app.post("/register2")
def register2():
    name = request.form["username"]               # "Admin" o "ａｄｍｉｎ" cuando ya existe "admin"
    if db_user_exists(name):
        return "taken", 400
    create_user(name, request.form["password"])
    return "ok"
