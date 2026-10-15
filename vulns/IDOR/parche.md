# Parche: IDOR

## Estrategia

1. **Autenticación obligatoria** en todo handler que devuelva datos de usuario (decorador, middleware, dependencia).
2. **Identidad desde la sesión/token verificado**, nunca desde un parámetro del request.
3. **Autorización en la consulta**: filtrar por dueño en la misma query (`WHERE id = ? AND owner_id = ?`). Si no es suyo, la consulta no devuelve nada → `404`.
4. Si el endpoint es para el propio usuario, eliminar el ID de la ruta: `/api/me` en vez de `/api/user/<id>`.
5. Endpoints de debug/backdoor: **borrarlos**, después de confirmar en el tráfico que el checker no los usa.

| Framework | Patrón |
|---|---|
| Flask | `@login_required` + `Note.query.filter_by(id=nid, owner_id=session["user_id"]).first_or_404()` |
| FastAPI | `current: User = Depends(get_current_user)` + filtro por `current.id` |
| aiohttp | `session = await get_session(request)` + `session.get("username") == owner` |
| Express | middleware `requireLogin` + `findOne({ _id, owner: req.session.userId })` |
| Spring | `@AuthenticationPrincipal` + `repo.findByIdAndOwner(id, principal.getName())` |
| Go | `userID` desde el contexto (middleware) + `WHERE id = ? AND owner = ?` |
| PHP | `$_SESSION['user_id']` + `AND owner = ?` |

## Errores comunes

- Verificar `if session` / `if "user" in session` y no comparar con el dueño del recurso.
- Ocultar el link en el frontend: el endpoint sigue accesible.
- Usar `403` en algunos endpoints y `404` en otros: el atacante enumera qué IDs existen. Mejor `404` siempre.
- Reemplazar IDs secuenciales por `md5(id)` o `base64(id)`: sigue siendo predecible. Usar `secrets.token_urlsafe(16)` si el link debe ser compartible.
- Parchear `GET /note/<id>` y olvidar `PUT`, `DELETE`, `/note/<id>/export`, `/search` o la API JSON paralela.
- Cambiar la respuesta de los usuarios legítimos: el checker lee su propio flag por ese mismo endpoint.

## Defensa en profundidad

- Centralizar la verificación en una función `get_owned_or_404(model, id, user)` y usarla en todos los handlers.
- Revisar el listado de rutas completo (`app.url_map`, `app._router.stack`, `@RequestMapping`) en busca de endpoints sin auth.
