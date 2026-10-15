# Flask

import re
import zipfile
from pathlib import Path
from flask import Flask, request, send_file, send_from_directory, abort

app = Flask(__name__)
BASE = Path("/srv/notes").resolve()

def safe_path(name: str) -> Path:
    # resolve() elimina .. y sigue symlinks; despues se verifica que siga dentro de BASE
    target = (BASE / name).resolve()
    if not target.is_relative_to(BASE):          # Python 3.9+
        abort(403)
    return target

# Patch 1: canonicalizar + verificar
@app.get("/download")
def download():
    return send_file(safe_path(request.args["file"]))

# Patch 2: send_from_directory usa safe_join internamente
@app.get("/read")
def read():
    return send_from_directory(BASE, request.args["file"])

# Patch 3: allowlist de nombres (sin separadores ni puntos)
NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
@app.get("/view")
def view():
    name = request.args["file"]
    if not NAME_RE.fullmatch(name):
        abort(400)
    return (BASE / name).read_text()

# Patch 4: validar cada entrada del ZIP antes de extraer
@app.post("/import")
def import_zip():
    with zipfile.ZipFile(request.files["zip"]) as zf:
        for member in zf.namelist():
            safe_path(member)                    # aborta si alguna entrada se sale de BASE
        zf.extractall(BASE)
    return "ok"
