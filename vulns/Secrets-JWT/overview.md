# Secretos hardcodeados, sesiones y JWT

## Qué es

En A/D **todos los equipos tienen el mismo código fuente**. Cualquier secreto escrito en el código (clave de sesión de Flask/Express, secreto de JWT, clave HMAC, password de admin, credenciales de la base de datos) es público desde el minuto cero. Con él, el atacante firma una cookie o un token para el usuario que quiera.

Bugs relacionados con JWT:

| Bug | Ataque |
|---|---|
| Secreto hardcodeado o débil (`secret`, `changeme`) | Firmar tokens propios / crackear con `hashcat -m 16500` |
| `alg: none` aceptado | Token sin firma |
| `jwt.decode` en vez de `jwt.verify` | La firma nunca se verifica |
| Confusión RS256 → HS256 | Firmar con la clave **pública** como secreto HMAC |
| `kid` / `jku` usados para cargar la clave | Path traversal / SQLi en `kid`, clave remota del atacante |
| Datos sensibles en el payload | El payload de un JWT es base64, no está cifrado |

## Cómo identificarla en código

```bash
rg -n -i '(secret|secret_key|jwt_secret|session_secret|hmac_key|api_key|password)\s*[:=]\s*["\x27][^"\x27]{3,}'
rg -n "keyboard cat|changeme|supersecret|s3cr3t|secret123"
rg -n 'app\.secret_key|SECRET_KEY|session\(\{|cookie-session|cookieParser\('
rg -n -i 'jwt\.decode|verify_signature.*False|algorithms|parseUnsecured|alg.*none'
```

## Impacto en A/D

- **auth-bypass** inmediato: forjar la sesión del usuario que tiene el flag.
- Con sesiones que guardan pickle/objetos serializados → **RCE** (ver [Deserialization](../Deserialization/overview.md)).

## Referencias

- [OWASP JSON Web Token Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)
- [flask-unsign](https://github.com/Paradoxis/Flask-Unsign), [jwt_tool](https://github.com/ticarpi/jwt_tool)
- [CWE-798](https://cwe.mitre.org/data/definitions/798.html), [CWE-347](https://cwe.mitre.org/data/definitions/347.html)
