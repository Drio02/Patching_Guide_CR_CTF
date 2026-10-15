# Parche: Memory Corruption

## Estrategia

| Vulnerable | Parche |
|---|---|
| `strcpy(d, s)` | `snprintf(d, sizeof d, "%s", s)` |
| `strcat(d, s)` | `strncat(d, s, sizeof d - strlen(d) - 1)` |
| `sprintf(b, fmt, ...)` | `snprintf(b, sizeof b, fmt, ...)` y verificar el valor devuelto |
| `gets(b)` | `fgets(b, sizeof b, stdin)` + quitar `\n` |
| `scanf("%s", b)` | `scanf("%63s", b)` (tamaño − 1) |
| `printf(user)` | `printf("%s", user)` |
| `sprintf(bp, "%02x", c)` | `snprintf(bp, end - bp, "%02x", (unsigned char)c)` |
| `char c = fgetc(f)` | `int c = fgetc(f)` |
| `strncmp(a, b, strlen(a))` | `strlen(a) == strlen(b) && memcmp(a, b, strlen(a)) == 0` (o tiempo constante) |
| `malloc(n * size)` | `calloc(n, size)` |
| `realloc(p, n * size)` | `reallocarray(p, n, size)` (glibc 2.26+) o verificar `n > SIZE_MAX / size` |
| `read(fd, buf, 0x200)` con `buf[0x100]` | `read(fd, buf, sizeof buf)` |
| `int len` del usuario | `size_t len` o `if (len < 0 \|\| len > MAX)` |
| `free(p);` | `free(p); p = NULL;` |

## Errores comunes

- Usar `sizeof(ptr)` en vez del tamaño del buffer cuando el buffer es un parámetro (`char *buf`): da 8. Pasar el tamaño como argumento.
- `strncpy` no garantiza el terminador nulo: agregar `d[sizeof d - 1] = 0` o usar `snprintf`.
- Cambiar el tamaño de un struct que se guarda en disco tal cual (`fwrite(&note, sizeof note, 1, f)`): rompe la lectura de los flags existentes.
- Recompilar con flags/versiones distintas a las del Dockerfile original y romper el binario.

## Defensa en profundidad

Si el Dockerfile compila desde el código fuente, agregar al `CFLAGS`:

```
-O2 -D_FORTIFY_SOURCE=2 -fstack-protector-strong -fPIE -pie -Wl,-z,relro,-z,now
```

`_FORTIFY_SOURCE` convierte muchos overflows de `memcpy`/`sprintf`/`strcpy` en un abort en vez de una corrupción silenciosa. Ojo: un abort cierra la conexión, verificar que el checker siga pasando.
