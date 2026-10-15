# Flask / Jinja2

from flask import Flask, request, render_template_string
from jinja2.sandbox import SandboxedEnvironment

app = Flask(__name__)

# Patch 1: plantilla fija, el input entra como variable (y se auto-escapa)
@app.get("/hello")
def hello():
    name = request.args.get("name", "guest")
    return render_template_string("<h1>Hola {{ name }}</h1>", name=name)

# Patch 2: igual, sin f-string
@app.get("/profile")
def profile():
    return render_template_string("<p>{{ bio }}</p>", bio=request.args.get("bio", ""))

# Patch 3: si el usuario debe escribir plantillas -> sandbox y contexto minimo
sandbox = SandboxedEnvironment(autoescape=True)

@app.post("/preview")
def preview():
    tpl = sandbox.from_string(request.form["template"])
    return tpl.render(user="alice")          # solo datos simples en el contexto

# Alternativa sin motor de plantillas:
#   request.form["template"].replace("{user}", "alice")
