# Parche: SQL Injection

## Estrategia

1. **Consultas parametrizadas / prepared statements** en todos los sinks. El valor viaja separado del SQL y nunca se interpreta como código.
2. **Allowlist** para lo que no puede ser parámetro: nombres de columna, `ORDER BY`, `ASC/DESC`.
3. **Cast de tipos**: IDs numéricos → `int(x)`; `LIMIT`/`OFFSET` → entero.
4. Parche mínimo: cambia solo la línea del sink. No toques el esquema ni el formato de respuesta (el checker depende de eso).

| Lenguaje / driver | Placeholder |
|---|---|
| Python `sqlite3` | `?` |
| Python `psycopg`, `pymysql`, `mysqlclient` | `%s` (sin comillas alrededor) |
| SQLAlchemy `text()` | `:nombre` |
| Node `mysql2`, `sqlite3`, `better-sqlite3` | `?` |
| Node `pg` | `$1, $2` |
| PHP PDO | `?` o `:nombre` |
| PHP mysqli | `?` + `bind_param("s", $x)` |
| Java JDBC | `?` + `setString(1, x)` |
| Go `database/sql` | `?` (MySQL/SQLite), `$1` (Postgres) |
| C# ADO.NET | `@nombre` |
| Ruby ActiveRecord / Sequel | `?` o hash `where(user: x)` |
| C SQLite / libpq | `?` + `sqlite3_bind_*` / `$1` + `PQexecParams` |

## Errores comunes

- `cur.execute("... '%s'" % x)` o `cur.execute(f"...")` **sigue siendo concatenación**. El valor debe ir en el segundo argumento.
- Comillas alrededor del placeholder: `WHERE user = '?'` busca el literal `?`.
- Escapar a mano (`replace("'", "''")`) o con blacklist (`if "union" in x`): se bypassea con `UnIoN`, comentarios `/**/`, encodings, backslashes.
- `ORDER BY ?`: el placeholder no funciona para identificadores → allowlist.
- Parchear el login y olvidar la búsqueda, el export o el perfil, que usan la misma tabla.
- `LIKE ?` con `%` del usuario: no es inyección, pero permite listar todo. Escapar `%` y `_` si importa.

## Defensa en profundidad

- Usuario de base de datos con permisos mínimos (sin `FILE`, sin superuser en Postgres).
- Deshabilitar stacked queries si el driver lo permite (`multipleStatements: false` en `mysql`).
- No devolver errores SQL al cliente (facilitan inyecciones error-based).
