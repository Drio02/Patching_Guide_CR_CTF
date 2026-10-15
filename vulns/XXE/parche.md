# Parche: XXE

## Estrategia

**Deshabilitar DTDs** (o al menos las entidades externas) en el parser. Es una línea de configuración.

| Lenguaje | Parche |
|---|---|
| Python | `defusedxml.ElementTree.fromstring(x)`; lxml: `XMLParser(resolve_entities=False, no_network=True, load_dtd=False)` |
| Java | `dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true)` |
| PHP 8 | No pasar `LIBXML_NOENT` ni `LIBXML_DTDLOAD` (entidades externas desactivadas por defecto desde libxml 2.9) |
| PHP < 8 | `libxml_disable_entity_loader(true)` |
| .NET | `XmlReaderSettings { DtdProcessing = DtdProcessing.Prohibit, XmlResolver = null }` |

## Errores comunes

- Configurar un `DocumentBuilderFactory` y olvidar el `SAXParserFactory` o el `TransformerFactory` que procesan el mismo input en otro endpoint.
- Filtrar la palabra `<!ENTITY` o `SYSTEM`: se bypassea con encodings (UTF-16) o entidades de parámetro.
- Olvidar los uploads de SVG/DOCX: también son XML.
- Deshabilitar DTDs cuando el checker envía XML con un `<!DOCTYPE>` legítimo: en ese caso usar solo `resolve_entities=False` / `setExpandEntityReferences(false)` en vez de prohibir el DOCTYPE.

## Defensa en profundidad

- Si el feature no necesita XML, aceptar JSON.
- El usuario del servicio no debería poder leer archivos fuera de su directorio de datos.
