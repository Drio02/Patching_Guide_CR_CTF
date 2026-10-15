# Path Traversal

## Qué es

Es una vulnerabilidad que permite a un atacante acceder a archivos y directorios fuera del directorio previsto, manipulando la entrada que se usa para construir una ruta de archivo. El truco clásico es inyectar secuencias como `../` (o sus variantes codificadas: `..%2f`, `%2e%2e/`, `....//`, etc.) para "subir" en el árbol de directorios. Una ruta absoluta (`/etc/passwd`) también funciona cuando el código usa `os.path.join` o `Path.Combine`.

Cuando la ruta termina en un `include`/`require` (PHP) se convierte en **LFI**, que puede escalar a RCE (log poisoning, `php://filter`, sesiones).

## Cómo identificarla en código

- `open`, `send_file`, `readFile`, `sendFile`, `fopen`, `file_get_contents`, `include`, `os.Open`, `File.ReadAllText` con un nombre que viene del request.
- Rutas armadas con `+`, f-strings, `os.path.join(base, name)`, `path.join(base, name)`.
- Extracción de ZIP/TAR sin validar los nombres de las entradas (**Zip Slip**).

```bash
rg -n '(open|send_file|readFile|sendFile|fopen|file_get_contents|include|require|os\.Open|ReadAllText)\s*\(.*(req|request|params|args|GET|POST|query|name|file)'
rg -n 'extractall|ZipFile|tarfile|unzip'
```

## Impacto en A/D

- **flag-leak**: leer los archivos de flags del servicio (`/data/notes/<id>`, la base SQLite completa).
- Leer el código, `.env` o claves de sesión, y desde ahí forjar cookies (**auth-bypass**).
- Con escritura (upload, Zip Slip): sobrescribir código o plantillas → **RCE**.

## Referencias

- [OWASP Path Traversal](https://owasp.org/www-community/attacks/Path_Traversal)
- [CWE-22](https://cwe.mitre.org/data/definitions/22.html)
- [Snyk: Zip Slip](https://security.snyk.io/research/zip-slip-vulnerability)
