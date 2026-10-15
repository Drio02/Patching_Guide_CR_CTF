# Flask

import requests
from flask import Flask, request

app = Flask(__name__)

# Vuln 1: la URL del usuario se pide tal cual
@app.post("/preview")
def preview():
    return requests.get(request.form["url"]).text
    # url = http://127.0.0.1:5000/internal/flags  |  http://redis:6379  |  file:// (con otras libs)

# Vuln 2: blacklist de strings
@app.post("/avatar")
def avatar():
    url = request.form["url"]
    if "localhost" in url or "127.0.0.1" in url:
        return "forbidden", 403
    return requests.get(url, timeout=5).content
    # bypass: http://127.1:5000/, http://0x7f000001/, http://[::1]/, redirect desde un host externo

# Endpoint interno que confia en que solo lo llama localhost
@app.get("/internal/flags")
def internal_flags():
    if request.remote_addr != "127.0.0.1":
        return "forbidden", 403
    return open("/data/flags.txt").read()
