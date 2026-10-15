# Parche: Command Injection

## Estrategia

1. **Evitar el subproceso**: si existe una función de librería, usarla (`socket`/`requests` en vez de `curl`, `zipfile` en vez de `unzip`, `os.listdir` en vez de `ls`).
2. **Sin shell**: pasar el comando como lista de argumentos. Así `;`, `|` y `$()` son caracteres literales.
3. **Cortar la argument injection**: poner `--` antes de los argumentos del usuario (si el programa lo soporta) y rechazar valores que empiecen con `-`.
4. **Validar la forma** del valor: IP con `ipaddress`, hostname con regex, número con `int()`.

| Lenguaje | Forma segura |
|---|---|
| Python | `subprocess.run(["ping", "-c", "1", "--", host], timeout=5)` |
| Node | `execFile("ping", ["-c", "1", "--", host])` / `spawn(cmd, args)` |
| PHP | `escapeshellarg($host)` (o `proc_open` con array en PHP 7.4+) |
| Java | `new ProcessBuilder("ping", "-c", "1", "--", host)` |
| Go | `exec.Command("ping", "-c", "1", "--", host)` |
| Ruby | `system("ping", "-c", "1", "--", host)` (varios argumentos) |
| C | `fork()` + `execvp("ping", argv)` |

## Errores comunes

- Blacklist de caracteres (`;`, `|`, `&`): se bypassea con `$()`, backticks, `\n`, `${IFS}`, `%0a`.
- `shlex.quote` / `escapeshellarg` y después poner el resultado **entre comillas** otra vez → se rompe el quoting.
- `escapeshellcmd` en PHP: no impide agregar argumentos (argument injection).
- Pasar a lista pero mantener `shell=True` en Python: con lista + `shell=True`, solo el primer elemento es el comando y el resto va a la shell.
- Olvidar `timeout`: un `ping -c 100000` deja el worker bloqueado (DoS sobre tu propio SLA).

## Defensa en profundidad

- Correr el servicio como usuario sin privilegios y con sistema de archivos de solo lectura cuando sea posible.
- Limitar binarios disponibles en la imagen (imágenes distroless/slim).
