# SQL Injection

## Qué es

La aplicación construye una consulta SQL concatenando input del usuario (`+`, f-strings, `.format()`, `%`, `sprintf`, template literals). El atacante cierra el literal (`'`) y agrega su propio SQL: `admin' --`, `' OR 1=1 --`, `' UNION SELECT flag FROM flags --`.

## Cómo identificarla en código

- Llamadas a `execute`, `query`, `exec`, `raw`, `sqlite3_exec`, `PQexec`, `db.Query` cuyo primer argumento se arma con variables.
- Patrones típicos: `"... WHERE user = '" + user + "'"`, `f"... {id}"`, `"... %s" % x`, `` `... ${req.query.id}` ``, `sprintf(q, "... '%s'", name)`.
- `ORDER BY`, nombres de tabla/columna o `LIMIT` construidos con input (los placeholders no los cubren).

```bash
rg -n --pcre2 '(execute|query|exec|raw)\s*\(\s*(f"|".*"\s*(\+|%|\.format))'
rg -n -i 'sprintf\(.*(SELECT|INSERT|UPDATE|DELETE)'
rg -n -i '(SELECT|WHERE|INSERT).*\$\{'
```

## Impacto en A/D

- **flag-leak**: `UNION SELECT` sobre la tabla de notas/usuarios devuelve todos los flags.
- **auth-bypass**: `admin' --` en el login.
- A veces **RCE**: stacked queries + `COPY ... PROGRAM` en Postgres, `INTO OUTFILE` en MySQL, `load_extension` en SQLite.

## Referencias

- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [PayloadsAllTheThings: SQL Injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)
