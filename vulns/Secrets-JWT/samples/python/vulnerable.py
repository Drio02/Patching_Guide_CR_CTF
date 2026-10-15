# Flask + PyJWT

import jwt
from flask import Flask, request, session

app = Flask(__name__)

# Vuln 1: clave de sesion hardcodeada -> flask-unsign --sign --cookie "{'user': 'admin'}" --secret 'dev'
app.secret_key = "dev"

# Vuln 2: secreto de JWT hardcodeado
JWT_SECRET = "supersecret"

# Vuln 3: verificacion desactivada
@app.get("/api/me")
def me():
    token = request.headers["Authorization"].split()[1]
    claims = jwt.decode(token, options={"verify_signature": False})
    return {"user": claims["sub"]}

# Vuln 4: algoritmo elegido por el token (en PyJWT viejo, "none" o confusion RS/HS)
@app.get("/api/notes")
def notes():
    token = request.headers["Authorization"].split()[1]
    header = jwt.get_unverified_header(token)
    claims = jwt.decode(token, JWT_SECRET, algorithms=[header["alg"]])
    return {"user": claims["sub"]}
