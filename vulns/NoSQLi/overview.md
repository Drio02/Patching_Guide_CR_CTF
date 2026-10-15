# NoSQL Injection

## Qué es

El valor que manda el usuario llega a un filtro de MongoDB (u otra base NoSQL) como **objeto** en vez de como string. Express (`qs`), PHP y los bodies JSON convierten `password[$ne]=x` o `{"password": {"$ne": "x"}}` en un operador de consulta:

```
POST /login   {"username": "admin", "password": {"$ne": ""}}
→ db.users.findOne({username: "admin", password: {$ne: ""}})   // login sin password
```

Otros operadores útiles para el atacante: `$gt`, `$regex` (extraer un secreto carácter por carácter), `$where` y `$function` (JavaScript del lado del servidor), `$in`.

## Cómo identificarla en código

- `find`, `findOne`, `updateOne`, `deleteMany`, `aggregate` con `req.body.*`, `req.query.*`, `request.json[...]`, `$_POST[...]` directos dentro del filtro.
- Uso de `$where` o `mapReduce` con strings concatenados.

```bash
rg -n 'find(One)?\(\{[^}]*(req\.(body|query|params)|request\.(json|args|form)|\$_(GET|POST))'
rg -n '\$where|\$function|mapReduce'
```

## Impacto en A/D

- **auth-bypass**: login como cualquier usuario (incluido el del checker que tiene el flag).
- **flag-leak**: `$regex` sobre el campo del flag, o `{"owner": {"$ne": null}}` en listados.
- `$where` → ejecución de JavaScript en el servidor de Mongo (DoS o lectura de datos).

## Referencias

- [OWASP: Testing for NoSQL Injection](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/05.6-Testing_for_NoSQL_Injection)
- [PayloadsAllTheThings: NoSQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/NoSQL%20Injection)
- [CWE-943](https://cwe.mitre.org/data/definitions/943.html)
