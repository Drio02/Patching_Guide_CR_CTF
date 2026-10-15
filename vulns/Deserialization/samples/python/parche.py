# Flask

import base64
import io
import json
import pickle
import yaml
from flask import Flask, request, abort

app = Flask(__name__)

# Patch 1 (preferido): JSON en vez de pickle
@app.get("/dashboard")
def dashboard():
    try:
        data = json.loads(base64.b64decode(request.cookies["prefs"]))
    except (ValueError, KeyError):
        abort(400)
    return f"theme: {data.get('theme', 'light')}"

# Patch 1b: si hay que seguir leyendo pickles ya guardados, restringir clases
class SafeUnpickler(pickle.Unpickler):
    ALLOWED = {("builtins", "dict"), ("builtins", "list"), ("builtins", "str"),
               ("builtins", "int"), ("builtins", "set")}

    def find_class(self, module, name):
        if (module, name) in self.ALLOWED:
            return super().find_class(module, name)
        raise pickle.UnpicklingError(f"blocked {module}.{name}")

def safe_pickle_loads(b: bytes):
    return SafeUnpickler(io.BytesIO(b)).load()

# Patch 2: safe_load solo construye tipos basicos
@app.post("/import")
def import_cfg():
    cfg = yaml.safe_load(request.data)
    return str(cfg)
