# Flask

import os
import zipfile
from flask import Flask, request, send_file

app = Flask(__name__)
BASE = "/srv/notes"

# Vuln 1: concatenacion directa
@app.get("/download")
def download():
    name = request.args["file"]
    return send_file(BASE + "/" + name)          # payload: ?file=../../etc/passwd

# Vuln 2: os.path.join con ruta absoluta descarta BASE
@app.get("/read")
def read():
    path = os.path.join(BASE, request.args["file"])   # ?file=/etc/passwd -> "/etc/passwd"
    with open(path) as f:
        return f.read()

# Vuln 3: filtro con replace (bypass con ....//)
@app.get("/view")
def view():
    name = request.args["file"].replace("../", "")
    return open(os.path.join(BASE, name)).read()

# Vuln 4: Zip Slip, las entradas pueden llamarse ../../app/app.py
@app.post("/import")
def import_zip():
    zipfile.ZipFile(request.files["zip"]).extractall(BASE)
    return "ok"
