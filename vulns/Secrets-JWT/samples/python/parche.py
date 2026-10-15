# Flask + PyJWT

import os
import secrets
from pathlib import Path
import jwt
from flask import Flask, request, abort

app = Flask(__name__)

def persistent_secret(path: str) -> str:
    # Se genera una sola vez y se guarda en un volumen: mismo valor para todos los workers y reinicios
    p = Path(path)
    if not p.exists():
        p.write_text(secrets.token_hex(32))
    return p.read_text().strip()

# Patch 1 y 2: secretos aleatorios propios
app.secret_key = os.environ.get("FLASK_SECRET") or persistent_secret("/data/flask_secret")
JWT_SECRET = os.environ.get("JWT_SECRET") or persistent_secret("/data/jwt_secret")

def verify(token: str) -> dict:
    try:
        # Patch 3 y 4: siempre verificar y fijar el algoritmo del lado del servidor
        return jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.PyJWTError:
        abort(401)

def bearer() -> str:
    parts = request.headers.get("Authorization", "").split()
    if len(parts) != 2 or parts[0] != "Bearer":
        abort(401)
    return parts[1]

@app.get("/api/me")
def me():
    return {"user": verify(bearer())["sub"]}

@app.get("/api/notes")
def notes():
    return {"user": verify(bearer())["sub"]}
