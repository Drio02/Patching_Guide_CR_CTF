# Parche: Secretos hardcodeados, sesiones y JWT

## Estrategia

1. **Reemplazar el secreto por uno aleatorio propio** (32+ bytes de CSPRNG).
2. **Persistirlo** en un archivo dentro de un volumen o en una variable de entorno de `docker-compose.yml`, para que:
   - todos los workers (gunicorn, cluster de Node) usen el mismo valor;
   - un reinicio del contenedor no invalide las sesiones del checker.
3. **JWT**: fijar el algoritmo en la verificación (`algorithms=["HS256"]`), usar la función que verifica, ignorar `kid`/`jku`.
4. Cambiar también **credenciales por defecto** (admin/admin, DB root/root) en app *y* base de datos a la vez.

## Errores comunes

- `app.secret_key = os.urandom(32)` sin persistir: con varios workers cada uno tiene una clave distinta → sesiones que funcionan "a veces" → checker en *mumble*.
- Cambiar el secreto de un token que el checker emitió en la ronda anterior y necesita para recuperar el flag. Rotar en el borde de la ronda o aceptar ambos secretos durante una ronda.
- Rotar el secreto y dejar el `alg: none` o el `decode` sin verificar.
- Dejar el secreto viejo como fallback (`os.environ.get("SECRET", "keyboard cat")`) y olvidar setear la variable.
- Cambiar la password de admin en el código pero no el usuario ya creado en la base de datos.

## Defensa en profundidad

- Sesiones del lado del servidor (ID aleatorio en la cookie, datos en Redis/DB).
- Cookies con `HttpOnly`, `SameSite=Lax`.
