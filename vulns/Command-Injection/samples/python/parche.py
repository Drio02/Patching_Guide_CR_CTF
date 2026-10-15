# Flask

import ipaddress
import re
import subprocess
import requests
from flask import Flask, request, abort

app = Flask(__name__)

# Patch 1: validar como IP + lista de argumentos sin shell + timeout
@app.post("/ping")
def ping():
    try:
        host = str(ipaddress.ip_address(request.form["host"]))
    except ValueError:
        abort(400)
    subprocess.run(["ping", "-c", "1", host], timeout=5, check=False)
    return "done"

# Patch 2: regex de hostname + "--" para cortar opciones
HOST_RE = re.compile(r"^[A-Za-z0-9.-]{1,253}$")
@app.get("/lookup")
def lookup():
    domain = request.args["domain"]
    if not HOST_RE.fullmatch(domain) or domain.startswith("-"):
        abort(400)
    return subprocess.run(["nslookup", "--", domain], capture_output=True, timeout=5).stdout

# Patch 3: reemplazar el binario por una libreria
@app.get("/fetch")
def fetch():
    url = request.args["url"]
    if not url.startswith(("http://", "https://")):
        abort(400)
    return requests.get(url, timeout=5, allow_redirects=False).text   # revisar SSRF (ver vulns/SSRF)
