# XXE (XML External Entity)

## Qué es

El servicio parsea XML del usuario con un parser que **resuelve entidades externas** declaradas en el DTD. El atacante define una entidad que apunta a un archivo local o a una URL interna y el parser la expande en el resultado:

```xml
<?xml version="1.0"?>
<!DOCTYPE r [ <!ENTITY x SYSTEM "file:///data/flags.txt"> ]>
<note><body>&x;</body></note>
```

Variantes: XXE ciega con exfiltración por DTD externo, SSRF (`SYSTEM "http://127.0.0.1/admin"`), DoS con "billion laughs" (entidades anidadas). Formatos que son XML por dentro: SVG, DOCX/XLSX, SOAP, RSS, SAML.

## Cómo identificarla en código

| Lenguaje | Parser a revisar |
|---|---|
| Python | `lxml.etree.XMLParser(resolve_entities=True)` (valor por defecto en lxml < 5), `xml.dom.pulldom`, `xml.sax` con `feature_external_ges` |
| Java | `DocumentBuilderFactory`, `SAXParserFactory`, `XMLInputFactory`, `TransformerFactory`, `SchemaFactory` sin features seguras (vulnerables por defecto) |
| PHP | `loadXML`/`simplexml_load_string` con `LIBXML_NOENT` o `LIBXML_DTDLOAD` |
| .NET | `XmlDocument` con `XmlResolver` asignado, `XmlReaderSettings.DtdProcessing = Parse` |

```bash
rg -n 'XMLParser|etree\.(parse|fromstring)|DocumentBuilderFactory|SAXParserFactory|XMLInputFactory|LIBXML_NOENT|LIBXML_DTDLOAD|simplexml_load|DtdProcessing|XmlResolver'
```

## Impacto en A/D

- **flag-leak**: leer archivos de flags o la base SQLite desde el disco.
- **SSRF** hacia servicios internos.

## Referencias

- [OWASP XXE Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings: XXE](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/XXE%20Injection)
- [CWE-611](https://cwe.mitre.org/data/definitions/611.html)
