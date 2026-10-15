# Parche: XSS

## Estrategia

1. **Escapar en la salida**, según el contexto: HTML (`htmlspecialchars`, autoescape), atributo (comillas + escape), JavaScript (`JSON.stringify` / `tojson`), URL (`encodeURIComponent` + allowlist de esquemas `http`/`https`).
2. **Frontend**: `textContent` en vez de `innerHTML`. Si hace falta HTML: `DOMPurify.sanitize(html)`.
3. Quitar los bypass del autoescape (`|safe`, `<%-`, `{{{ }}}`, `|raw`) donde el valor venga del usuario.

## Errores comunes

- Filtrar `<script>`: hay cientos de vectores (`<img src=x onerror=...>`, `<svg onload=...>`, `javascript:` en `href`).
- Escapar HTML y meter el valor dentro de un `<script>` o de un atributo sin comillas.
- Escapar al guardar en la base de datos y otra vez al mostrar (doble escape → el checker ve `&amp;lt;` y falla).
- Romper el formato que espera el checker: si el checker busca el flag en el HTML, el flag (alfanumérico) no cambia al escaparse.

## Defensa en profundidad

- `Content-Security-Policy: default-src 'self'; script-src 'self'`.
- Cookies de sesión con `HttpOnly` (el bot no entrega la cookie a `document.cookie`) y `SameSite=Lax`.
