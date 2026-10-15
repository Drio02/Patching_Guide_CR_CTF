# Parche: Path Traversal

La idea central es nunca confiar en la ruta que arma el usuario. Las defensas principales:

1. **Resolver la ruta canónica** (eliminar `..`, symlinks, etc.) y verificar que el resultado quede dentro del directorio permitido. Esta es la defensa más robusta.
2. **Validar/sanitizar el input**: aceptar solo nombres de archivo (sin separadores de ruta), idealmente con una allowlist o una regex restrictiva (`^[A-Za-z0-9_-]{1,64}$`).
3. **Usar solo el nombre base** del archivo (`basename`) descartando cualquier componente de directorio.

| Lenguaje | Canonicalizar | Verificar |
|---|---|---|
| Python | `(BASE / name).resolve()` | `target.is_relative_to(BASE)` (3.9+) |
| Node | `path.resolve(BASE, name)` (+ `fs.realpathSync` para symlinks) | `target.startsWith(BASE + path.sep)` |
| PHP | `realpath($base . '/' . $name)` | `$real !== false && str_starts_with($real, $base . DIRECTORY_SEPARATOR)` |
| Java | `base.resolve(name).normalize()` | `target.startsWith(base)` (compara por componentes) |
| Go | `filepath.IsLocal(name)` (1.20+) | o `os.OpenRoot(base)` + `root.Open(name)` (1.24+, bloquea symlinks) |
| C# | `Path.GetFullPath(Path.Combine(base, name))` | `full.StartsWith(base + Path.DirectorySeparatorChar, StringComparison.Ordinal)` |
| C | `realpath(path, resolved)` | `strncmp(resolved, BASE "/", strlen(BASE "/")) == 0` |

## Errores comunes

- `name.replace("../", "")`: `....//` queda como `../` después del reemplazo.
- `startsWith(base)` sin separador final: `/srv/files_evil` pasa la verificación de `/srv/files`.
- Validar **antes** de decodificar (URL-decode, doble encoding, Unicode) y abrir **después**.
- `os.path.join(base, name)` con `name` absoluto descarta `base` en Python. `Path.Combine` en C# también.
- Verificar con `abspath`/`normpath` y olvidar los symlinks (usar `realpath`/`resolve`).
- Parchear la descarga y olvidar el upload, el borrado o la extracción de ZIP.

## Defensa en profundidad

- Guardar los archivos con nombres generados (UUID) y mapearlos en la base de datos; el usuario nunca envía rutas.
- Correr el servicio con un usuario sin permisos de lectura fuera de su directorio de datos.
- En Flask, `send_from_directory`; en Express, `res.sendFile(name, { root })`: ambos rechazan `..`.
