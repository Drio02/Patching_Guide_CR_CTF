# Flask + sqlite3

import re
import unicodedata
from flask import Flask, request, session, abort

app = Flask(__name__)
MAX_TRANSFER = 1_000_000

# Patch 1: entero (centavos), rango explicito, operacion atomica en la DB
@app.post("/transfer")
def transfer():
    try:
        amount = int(request.form["amount"])      # int() rechaza "nan", "inf", "1e3", "1.5"
    except (KeyError, ValueError):
        abort(400)
    if not 0 < amount <= MAX_TRANSFER:
        abort(400)
    cur = db.execute(
        "UPDATE accounts SET balance = balance - ? WHERE user = ? AND balance >= ?",
        (amount, session["user"], amount))
    if cur.rowcount != 1:                          # sin saldo suficiente (sin race condition)
        return "insufficient funds", 400
    db.execute("UPDATE accounts SET balance = balance + ? WHERE user = ?",
               (amount, request.form["to"]))
    db.commit()
    return "ok"

# Patch 2: solo los campos permitidos
REGISTER_FIELDS = {"username", "password"}

@app.post("/register")
def register():
    data = request.get_json(silent=True) or {}
    clean = {k: data[k] for k in REGISTER_FIELDS if isinstance(data.get(k), str)}
    if clean.keys() != REGISTER_FIELDS:
        abort(400)
    db.session.add(User(**clean))                  # is_admin queda con su valor por defecto
    db.session.commit()
    return "ok"

# Patch 3: fullmatch exige el string completo; longitud en el patron
USER_RE = re.compile(r"[a-z0-9_]{3,32}")

@app.post("/signup")
def signup():
    username = request.form.get("username", "")
    password = request.form.get("password", "")
    if not USER_RE.fullmatch(username):
        abort(400)
    # Patch 4: ningun caracter de control en campos que van a un archivo por lineas
    if any(c in password for c in "\r\n\0:") or not 1 <= len(password) <= 128:
        abort(400)
    with open("/data/users.txt", "a") as f:
        f.write(f"{username}:{password}:0\n")
    return "ok"

# Patch 5: limite de longitud + regex sin cuantificadores anidados
EMAIL_RE = re.compile(r"[a-zA-Z0-9._-]{1,64}@example\.com")

@app.post("/newsletter")
def newsletter():
    email = request.form.get("email", "")
    if len(email) > 100 or not EMAIL_RE.fullmatch(email):
        return "invalid", 400
    return "subscribed"

# Patch 6: normalizar (NFKC + casefold) antes de verificar unicidad y de guardar
def canonical(name: str) -> str:
    return unicodedata.normalize("NFKC", name).casefold()

@app.post("/register2")
def register2():
    name = canonical(request.form.get("username", ""))
    if not USER_RE.fullmatch(name):                # despues de normalizar, allowlist ASCII
        abort(400)
    if db_user_exists(name):
        return "taken", 400
    create_user(name, request.form["password"])
    return "ok"

# Tipos en JSON: bool es subclase de int en Python
def is_int(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)
