# IDOR (Insecure Direct Object Reference)

## Qué es

El servicio expone un identificador de objeto (ID de nota, usuario, factura, archivo) y lo usa para buscar el recurso **sin verificar que pertenezca al usuario autenticado**. Basta con cambiar `/note/41` por `/note/42` para leer datos ajenos.

Variantes frecuentes en A/D:

- Verificar solo que exista *alguna* sesión (`if "username" in session`) y no que el usuario sea el dueño.
- Tomar la identidad de un parámetro (`?user=alice`, campo oculto, header) en vez de la sesión.
- Endpoints "olvidados": `/admin`, `/backdoor`, `/export`, `/debug`, `/api/users` sin autenticación.
- IDs secuenciales o predecibles en links "privados" de compartir.

## Cómo identificarla en código

- Handlers que reciben un ID por ruta/query y hacen `get(id)`, `findById(id)`, `WHERE id = ?` **sin** `AND owner = ?`.
- Rutas con nombres sensibles sin decorador/middleware de auth.
- Comparaciones de sesión que no usan el ID solicitado.

```bash
rg -n -i '(route|get|post|app\.\w+|@\w+Mapping)\(.*(admin|flag|debug|backdoor|export|internal|profile|user)'
rg -n 'findById|query\.get\(|get_or_404|WHERE id ?= ?\?'
rg -n 'in session|session\.get\('
```

## Impacto en A/D

- **flag-leak** directo: el checker guarda el flag en una nota/perfil de un usuario; cualquier equipo itera los IDs.
- Es de los primeros exploits que se automatizan: parchear en los primeros minutos.

## Referencias

- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [OWASP IDOR Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html)
- [CWE-639](https://cwe.mitre.org/data/definitions/639.html), [CWE-306](https://cwe.mitre.org/data/definitions/306.html)
