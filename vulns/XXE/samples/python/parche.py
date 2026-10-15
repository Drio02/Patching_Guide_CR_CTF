# Flask + lxml

from flask import Flask, request
from lxml import etree

app = Flask(__name__)

# Patch 1: lxml sin entidades, sin DTD y sin red
SAFE_PARSER = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)

@app.post("/import")
def import_note():
    root = etree.fromstring(request.data, SAFE_PARSER)
    return root.findtext("body")

# Patch 2 (si defusedxml esta instalado): reemplazo directo de xml.etree
# import defusedxml.ElementTree as ET
# root = ET.fromstring(request.data)    # lanza excepcion ante entidades / DTD
