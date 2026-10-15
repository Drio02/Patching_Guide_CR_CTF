# Parche: NoSQL Injection

## Estrategia

1. **Forzar el tipo** de cada valor que entra a un filtro: `String(x)` en Node, `isinstance(x, str)` en Python, `is_string($x)` en PHP. Un objeto nunca debe llegar como valor.
2. **Sanitizar globalmente** las claves que empiezan con `$` o contienen `.` (`express-mongo-sanitize`), si el paquete ya está en la imagen.
3. **Eliminar `$where`/`$function`** con input del usuario.
4. Comparar passwords **fuera** de la consulta: buscar por username y verificar el hash en código.

## Errores comunes

- Validar solo `req.body` y olvidar `req.query` y `req.params` (Express parsea `?user[$ne]=x` igual).
- `if (!username || !password)`: un objeto `{"$ne": ""}` es truthy y pasa la validación.
- Escapar `$` en el valor string: no es el problema; el problema es que el valor sea un objeto.
- Agregar dependencias (`npm install express-mongo-sanitize`) cuando el build no tiene internet: preferir `String()`.

## Defensa en profundidad

- Schemas tipados (Mongoose con `type: String` castea automáticamente en `find` cuando el schema está definido y `strictQuery` está activo).
- Usuario de Mongo sin permisos de administración y sin `javascriptEnabled` si no se necesita.
