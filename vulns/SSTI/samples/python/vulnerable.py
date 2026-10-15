# Flask / Jinja2

from flask import Flask, request, render_template_string
from jinja2 import Template

app = Flask(__name__)

# Vuln 1: el nombre se concatena dentro de la plantilla
@app.get("/hello")
def hello():
    name = request.args.get("name", "guest")
    return render_template_string("<h1>Hola " + name + "</h1>")
    # name = {{ cycler.__init__.__globals__.os.popen('cat /data/flag').read() }}

# Vuln 2: f-string dentro de la plantilla (mismo problema)
@app.get("/profile")
def profile():
    bio = request.args.get("bio", "")
    return render_template_string(f"<p>{bio}</p>")

# Vuln 3: plantillas de email editables por el usuario
@app.post("/preview")
def preview():
    return Template(request.form["template"]).render(user="alice")
