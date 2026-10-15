# SSRF (Server-Side Request Forgery)

## Qué es

El servicio hace una petición HTTP (o de otro protocolo) a una URL que controla el usuario: "importar desde URL", "preview de link", webhooks, descargar avatar, generar PDF desde URL. El atacante apunta la petición a **destinos internos** a los que no tiene acceso directo:

- `http://127.0.0.1:5000/admin`, `http://localhost:8080/internal/flags`
- Otros contenedores del `docker-compose` por nombre: `http://redis:6379`, `http://db:5432`, `http://backend/api/...`
- Esquemas peligrosos: `file:///etc/passwd`, `gopher://` (para hablar con Redis/SMTP), `dict://`

## Cómo identificarla en código

```bash
rg -n 'requests\.(get|post|head)|urlopen|urllib\.request|httpx\.|aiohttp\.ClientSession'
rg -n 'axios|fetch\(|got\(|node-fetch|http\.get\('
rg -n 'http\.Get\(|http\.NewRequest|curl_exec|file_get_contents\(\$|HttpClient|URL\(.*openStream'
```

Buscar llamadas cuya URL sale de `request.args`, `req.body`, `$_GET`, o de un campo guardado por el usuario (webhook, avatar URL).

## Impacto en A/D

- **flag-leak**: endpoints internos sin autenticación (`/internal`, `/admin` que confía en `127.0.0.1`), base de datos o Redis accesibles desde el contenedor.
- **RCE**: `gopher://` hacia Redis → escribir una tarea/cron/clave que se ejecuta.

## Referencias

- [OWASP SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html)
- [PayloadsAllTheThings: SSRF](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Server%20Side%20Request%20Forgery)
- [CWE-918](https://cwe.mitre.org/data/definitions/918.html)
