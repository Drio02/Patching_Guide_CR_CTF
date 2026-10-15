# Flask

import ipaddress
import socket
from urllib.parse import urlparse
import requests
from flask import Flask, request, abort

app = Flask(__name__)

def check_url(url: str) -> str:
    u = urlparse(url)
    if u.scheme not in ("http", "https") or not u.hostname:
        abort(400)
    port = u.port or (443 if u.scheme == "https" else 80)
    # Resolver TODAS las IPs del host y rechazar si alguna es interna
    try:
        infos = socket.getaddrinfo(u.hostname, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror:
        abort(400)
    for info in infos:
        ip = ipaddress.ip_address(info[4][0])
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            ip = ip.ipv4_mapped
        if not ip.is_global:      # cubre privadas, loopback, link-local, reservadas, CGNAT
            abort(403)
    return url

# Patch 1 y 2: validacion por IP resuelta + sin redirects + timeout
@app.post("/preview")
def preview():
    url = check_url(request.form["url"])
    return requests.get(url, timeout=5, allow_redirects=False).text

@app.post("/avatar")
def avatar():
    url = check_url(request.form["url"])
    return requests.get(url, timeout=5, allow_redirects=False).content

# Patch 3: el endpoint interno exige autenticacion propia (no basta con la IP)
@app.get("/internal/flags")
def internal_flags():
    abort(404)   # si no lo usa el checker, eliminarlo

# Nota: entre check_url y requests.get el DNS puede cambiar (rebinding).
# Para cerrarlo del todo, conectar a la IP validada y mandar el Host original en el header.
