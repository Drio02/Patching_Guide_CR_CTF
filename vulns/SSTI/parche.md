# Parche: SSTI

## Estrategia

1. **La plantilla es fija; el input es un dato**: pasar el valor como variable de contexto (`render_template_string("Hola {{ name }}", name=name)`) o usar un archivo de plantilla.
2. Si el feature *requiere* que el usuario escriba plantillas: **motor en sandbox** (`jinja2.sandbox.SandboxedEnvironment`, Twig `SandboxExtension`) o reemplazarlo por sustitución simple (`str.replace("{name}", name)`).
3. Freemarker: `TemplateClassResolver.ALLOWS_NOTHING_RESOLVER` y `setAPIBuiltinEnabled(false)`.

## Errores comunes

- Blacklist de `{{`, `__class__`, `config`, `.`: se bypassea con `{% %}`, `|attr()`, `request.args`, hex escapes (`\x5f\x5f`).
- Escapar HTML del input (`escape(name)`) **no** previene SSTI: `{{7*7}}` no tiene caracteres HTML.
- Parchear el endpoint principal y olvidar el de "preview", el de emails o el de exportar a PDF, que suelen renderizar con el mismo motor.
- Sandbox de Jinja2 con objetos peligrosos en el contexto (`os`, `config`, el modelo ORM completo).

## Defensa en profundidad

- No exponer `config`/`SECRET_KEY` en el contexto de las plantillas.
- En Flask, `app.jinja_env.globals` y context processors: revisar qué objetos se inyectan.
