# Flask / Jinja2

from flask import Flask, request, render_template_string
from markupsafe import Markup

app = Flask(__name__)

# Vuln 1: HTML armado con f-string (sin autoescape)
@app.get("/search")
def search():
    return f"<p>Resultados para {request.args.get('q', '')}</p>"

# Vuln 2: |safe desactiva el autoescape
NOTE_TPL = "<div class='note'>{{ body|safe }}</div>"
@app.get("/note")
def note():
    return render_template_string(NOTE_TPL, body=request.args.get("body", ""))

# Vuln 3: Markup() marca el string como seguro
@app.get("/bio")
def bio():
    return render_template_string("<p>{{ bio }}</p>", bio=Markup(request.args.get("bio", "")))
