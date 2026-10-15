# Flask / Jinja2

from flask import Flask, request, render_template_string
from markupsafe import escape

app = Flask(__name__)

# Patch 1: escape() explicito al armar HTML a mano
@app.get("/search")
def search():
    return f"<p>Resultados para {escape(request.args.get('q', ''))}</p>"

# Patch 2: sin |safe -> Jinja2 escapa automaticamente
NOTE_TPL = "<div class='note'>{{ body }}</div>"
@app.get("/note")
def note():
    return render_template_string(NOTE_TPL, body=request.args.get("body", ""))

# Patch 3: pasar el string tal cual, sin Markup()
@app.get("/bio")
def bio():
    return render_template_string("<p>{{ bio }}</p>", bio=request.args.get("bio", ""))

# Datos dentro de <script>: usar el filtro tojson
#   <script>const user = {{ user|tojson }};</script>

@app.after_request
def csp(resp):
    resp.headers["Content-Security-Policy"] = "default-src 'self'"
    return resp
